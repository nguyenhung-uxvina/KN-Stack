"""Transport layer — hybrid-ready.

ClipboardTransport: bán tự động (CEO dán vào app.getleo.ai). Đường duy nhất hiện nay.
ApiTransport: STUB — implement khi Leo cấp API access (getleo.ai/api, business-only).
KHÔNG bao giờ thêm browser automation (Cloudflare + ToS + khóa account — spec §8).
"""
import os
import subprocess
import tempfile


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
            # Piping text through PowerShell's stdin gets re-decoded via the
            # console/OEM code page and corrupts non-ASCII (Vietnamese diacritics).
            # Round-trip through a UTF-8 temp file instead — .NET's
            # File::ReadAllText auto-detects "no BOM -> UTF-8" for files we
            # write ourselves, sidestepping the code-page issue entirely.
            fd, path = tempfile.mkstemp(suffix=".txt")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(text)
                ps_path = path.replace("'", "''")
                p = subprocess.run(
                    [
                        "powershell", "-NoProfile", "-Command",
                        f"[System.IO.File]::ReadAllText('{ps_path}') | Set-Clipboard",
                    ],
                    capture_output=True, text=True, encoding="utf-8",
                )
                if p.returncode != 0:
                    raise TransportError(f"Không copy được vào clipboard: {p.stderr.strip()}")
            finally:
                os.remove(path)

    def _paste(self) -> str:
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            # Same rationale as _copy: capture via a UTF-8 (no BOM) temp file
            # instead of decoding PowerShell's stdout through the console
            # code page.
            fd, path = tempfile.mkstemp(suffix=".txt")
            os.close(fd)
            try:
                ps_path = path.replace("'", "''")
                p = subprocess.run(
                    [
                        "powershell", "-NoProfile", "-Command",
                        f"$c = Get-Clipboard -Raw; "
                        f"[System.IO.File]::WriteAllText('{ps_path}', $c, "
                        f"(New-Object System.Text.UTF8Encoding($false)))",
                    ],
                    capture_output=True, text=True, encoding="utf-8",
                )
                if p.returncode != 0:
                    raise TransportError(f"Không đọc được clipboard: {p.stderr.strip()}")
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
            finally:
                os.remove(path)


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
