"""Chính sách đường dẫn (deny-by-default) và allow-list lệnh AutoCAD.

Đường dẫn: realpath (giải junction/symlink/..) rồi commonpath với gốc — không dùng startswith
(bài học CVE-2025-53110/53109 của filesystem MCP). Danh sách gốc rỗng ⇒ từ chối tất cả.
Lệnh: SendCommand là luồng phím — mỗi dấu cách là Enter, tham số thừa sau khi lệnh xong sẽ chạy như
lệnh MỚI. Vì vậy kiểm cả động từ lẫn từng tham số theo mẫu của động từ đó, và tự dựng chuỗi.
"""
import os
import re
from pathlib import Path

from core.errors import BridgeError

READ_EXT = {".dwg", ".dxf"}
WRITE_EXT = {".dwg", ".dxf", ".csv", ".json", ".png", ".jsonl"}

DEFAULT_READ = [r"D:\AutoCAD\Workspace"]
DEFAULT_WRITE = [r"D:\AutoCAD\Workspace\output"]
DEFAULT_DENY = [r"D:\AutoCAD\AutoCAD 2025"]


def _drive_is_remote(p: str) -> bool:
    try:
        import win32file
        drive = os.path.splitdrive(p)[0]
        return bool(drive) and win32file.GetDriveType(drive + "\\") == win32file.DRIVE_REMOTE
    except Exception:  # noqa: BLE001 — không xác định được ⇒ không chặn theo tiêu chí này
        return False


class PathPolicy:
    def __init__(self, read_roots, write_roots, deny_roots):
        norm = lambda roots: [os.path.realpath(str(r)) for r in roots]  # noqa: E731
        self.read_roots, self.write_roots, self.deny_roots = norm(read_roots), norm(write_roots), norm(deny_roots)

    @classmethod
    def from_env(cls):
        def split(name, default):
            return [p for p in os.environ.get(name, os.pathsep.join(default)).split(os.pathsep) if p]
        return cls(split("AUTOCAD_BRIDGE_READ_ROOTS", DEFAULT_READ), split("AUTOCAD_BRIDGE_WRITE_ROOTS", DEFAULT_WRITE),
                   split("AUTOCAD_BRIDGE_DENY_ROOTS", DEFAULT_DENY))

    @staticmethod
    def _within(path: str, root: str) -> bool:
        try:
            return os.path.commonpath([os.path.normcase(path), os.path.normcase(root)]) == os.path.normcase(root)
        except ValueError:          # khác ổ đĩa
            return False

    def _check(self, path, roots, exts, kind) -> Path:
        raw = str(path)

        def deny(why):
            return BridgeError("PATH_DENIED", hint=f"{kind}: {why}")

        if raw.startswith(("\\\\", "//")):
            raise deny("không nhận đường dẫn mạng/UNC hay \\\\?\\")
        if ":" in os.path.splitdrive(raw)[1]:
            raise deny("không nhận alternate data stream")
        real = os.path.realpath(raw)
        if _drive_is_remote(real):
            raise deny("không nhận ổ mạng ánh xạ")
        if any(self._within(real, d) for d in self.deny_roots):
            raise deny("thư mục bị cấm")
        if not any(self._within(real, r) for r in roots):
            raise deny("ngoài các gốc được phép" if roots else "chưa cấu hình gốc nào ⇒ từ chối tất cả")
        if exts and Path(real).suffix.lower() not in exts:
            raise deny(f"đuôi tệp không được phép (cho phép: {', '.join(sorted(exts))})")
        return Path(real)

    def check_read(self, path) -> Path:
        return self._check(path, self.read_roots, READ_EXT, "đọc")

    def check_read_dir(self, path) -> Path:
        p = self._check(path, self.read_roots, set(), "đọc thư mục")
        if not p.is_dir():
            raise BridgeError("PATH_DENIED", hint="không phải thư mục")
        return p

    def check_write(self, path) -> Path:
        return self._check(path, self.write_roots, WRITE_EXT, "ghi")

    def allows(self, check, path) -> bool:
        try:
            check(path)
            return True
        except BridgeError:
            return False


# động từ → danh sách mẫu cho từng tham số (đúng số lượng)
ALLOWED_COMMANDS = {
    "ZOOM": [r"E|A|P"],
    "REGEN": [],
    "REGENALL": [],
}
_TOKEN = re.compile(r"[A-Za-z0-9._-]+")


class CommandPolicy:
    def __init__(self, allowed=None):
        self.allowed = allowed or ALLOWED_COMMANDS

    def build(self, verb: str, args=()) -> str:
        args = list(args or [])
        v = (verb or "").strip().lstrip("_.").upper()
        if v not in self.allowed:
            raise BridgeError("COMMAND_DENIED", hint=f"cho phép: {', '.join(sorted(self.allowed))}")
        patterns = self.allowed[v]
        if len(args) != len(patterns):
            raise BridgeError("COMMAND_DENIED", hint=f"{v} cần đúng {len(patterns)} tham số")
        out = []
        for a, pat in zip(args, patterns):
            a = str(a).strip()
            if not _TOKEN.fullmatch(a) or not re.fullmatch(pat, a, re.I):
                raise BridgeError("COMMAND_DENIED", hint=f"tham số không khớp mẫu {pat}")
            out.append("_" + a.upper())
        return " ".join(["_" + v, *out]) + " "
