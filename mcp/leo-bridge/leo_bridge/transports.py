"""Transport layer — hybrid-ready.

ClipboardTransport: bán tự động (CEO dán vào app.getleo.ai). Đường duy nhất hiện nay.
ApiTransport: STUB — implement khi Leo cấp API access (getleo.ai/api, business-only).
KHÔNG bao giờ thêm browser automation (Cloudflare + ToS + khóa account — spec §8).
"""
import os
import subprocess


class TransportError(Exception):
    pass


class ClipboardTransport:
    name = "clipboard"

    def send(self, prompt: str) -> str:
        self._copy(prompt)
        return (
            "Prompt đã nằm trong clipboard. Các bước: "
            "(1) Mở app.getleo.ai, dán (Ctrl+V) và gửi. "
            "(2) Chờ kết quả, bôi đen TOÀN BỘ kết quả, Ctrl+C. "
            "(3) Gọi leo_ingest với exchange_id để parse + verify."
        )

    def receive(self) -> str:
        text = self._paste()
        if not text or not text.strip():
            raise TransportError("Clipboard rỗng — copy TOÀN BỘ kết quả Leo trước khi gọi leo_ingest.")
        return text

    def _copy(self, text: str) -> None:
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
                input=text, text=True, capture_output=True,
            )
            if p.returncode != 0:
                raise TransportError(f"Không copy được vào clipboard: {p.stderr.strip()}")

    def _paste(self) -> str:
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
                text=True, capture_output=True,
            )
            if p.returncode != 0:
                raise TransportError(f"Không đọc được clipboard: {p.stderr.strip()}")
            return p.stdout


class ApiTransport:
    name = "api"

    def __init__(self):
        if not os.environ.get("LEO_API_KEY"):
            raise TransportError("LEO_API_KEY chưa có — Leo chưa cấp API access.")

    def send(self, prompt: str) -> str:
        raise NotImplementedError("ApiTransport: implement khi Leo cấp API docs (đã gửi request — xem docs/api-access-request-draft.md).")

    def receive(self) -> str:
        raise NotImplementedError("ApiTransport: implement khi Leo cấp API docs.")


def get_transport():
    if os.environ.get("LEO_API_KEY"):
        return ApiTransport()
    return ClipboardTransport()
