"""Mọi lời gọi COM chạy trên MỘT luồng STA riêng, có timeout.

Vì sao: FastMCP 1.27 gọi tool sync thẳng trên event loop (một lời gọi chậm chặn cả server), còn
SDK 2.x lại đẩy sang thread pool (COM bị gọi từ nhiều luồng). Hàng đợi 1 worker cố định mô hình luồng
bất kể phiên bản SDK. pywin32 311 KHÔNG có CoRegisterMessageFilter ⇒ xử lý "AutoCAD bận" bằng retry
ở mức lời gọi — và CHỈ cho lời gọi đọc: chạy lại một thao tác ghi có thể vẽ trùng.
"""
import asyncio
import concurrent.futures
import time

import pythoncom

from core.errors import BridgeError

BUSY_HRESULTS = {-2147418111, -2147417846}   # RPC_E_CALL_REJECTED, RPC_E_SERVERCALL_RETRYLATER


def is_busy(exc) -> bool:
    return isinstance(exc, pythoncom.com_error) and exc.hresult in BUSY_HRESULTS


def is_lost_typeinfo(exc) -> bool:
    """win32com dynamic ném AttributeError('<unknown>.X') khi AutoCAD đang chuyển tài liệu (đo: ngay sau Close)."""
    return isinstance(exc, AttributeError) and str(exc).startswith("<unknown>.")


def _sta_init():
    pythoncom.CoInitialize()


class ComWorker:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self._ex = self._new_executor()

    @staticmethod
    def _new_executor():
        return concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix="acad-sta",
                                                     initializer=_sta_init)

    async def run(self, fn, timeout: float | None = None):
        fut = self._ex.submit(fn)
        afut = asyncio.wrap_future(fut)
        done, _ = await asyncio.wait({afut}, timeout=timeout or self.timeout)
        if done:
            return afut.result()          # lấy từ future asyncio, nếu không asyncio log "exception was never retrieved"
        if fut.cancel():
            raise BridgeError("ACAD_TIMEOUT")
        # đang chạy và không huỷ được: bỏ luồng kẹt, dựng luồng mới cho lời gọi sau
        stuck, self._ex = self._ex, self._new_executor()
        stuck.shutdown(wait=False, cancel_futures=True)
        raise BridgeError("UNKNOWN_COMMIT")


def com_read(fn, budget: float = 20.0, backoff: float = 0.25):
    """Chạy hàm ĐỌC; AutoCAD bận ⇒ chờ lùi dần rồi thử lại trong ngân sách thời gian."""
    deadline = time.monotonic() + budget
    delay = backoff
    while True:
        try:
            return fn()
        except (pythoncom.com_error, AttributeError) as e:
            if not (is_busy(e) or is_lost_typeinfo(e)):
                raise
            if time.monotonic() + delay > deadline:
                if is_busy(e):
                    raise BridgeError("ACAD_BUSY", hint="Đóng hộp thoại / kết thúc lệnh đang chạy trong AutoCAD rồi gọi lại.") from e
                raise BridgeError("COM_ERROR", hint="AutoCAD tạm mất thông tin kiểu (vừa đóng/mở bản vẽ) — gọi lại sau.") from e
            time.sleep(delay)
            delay = min(delay * 2, 1.0)


def com_write(fn, partial=None):
    """Chạy MỘT lời gọi GHI đúng một lần. Bận ⇒ ACAD_BUSY kèm danh sách handle đã tạo trước đó (partial)."""
    try:
        return fn()
    except pythoncom.com_error as e:
        if is_busy(e):
            raise BridgeError("ACAD_BUSY", hint="Không tự chạy lại để tránh ghi trùng. Kiểm 'partial' trước khi gọi tiếp.",
                              data={"partial": list(partial or [])}) from e
        raise
