"""Sổ kiểm toán cục bộ: JSONL chỉ nối thêm, nối chuỗi băm (sửa 1 dòng ⇒ verify() báo hỏng).

Chỉ ghi băm tham số, không ghi đường dẫn hay chữ trong bản vẽ (nội dung MẬT không vào log).
Mẫu từ mcp/leo-bridge.
"""
import hashlib
import json
import os
import threading
import time
from pathlib import Path

GENESIS = "0" * 64


def _canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str, separators=(",", ":"))


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    @classmethod
    def from_env(cls):
        default = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "autocad-bridge" / "ledger.jsonl"
        return cls(os.environ.get("AUTOCAD_BRIDGE_LEDGER", str(default)))

    def _last_hash(self) -> str:
        last = GENESIS
        if self.path.exists():
            with self.path.open(encoding="utf-8") as fh:
                for line in fh:
                    if line.strip():
                        last = json.loads(line)["hash"]
        return last

    def record(self, tool, args, target=None, outcome="ok"):
        with self._lock:
            rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": tool, "args_sha": _sha(_canon(args))[:16],
                   "target": target, "outcome": outcome, "prev": self._last_hash()}
            rec["hash"] = _sha(_canon(rec))
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(_canon(rec) + "\n")

    def verify(self) -> bool:
        prev = GENESIS
        if not self.path.exists():
            return True
        with self.path.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                rec = json.loads(line)
                h = rec.pop("hash", None)
                if rec.get("prev") != prev or _sha(_canon(rec)) != h:
                    return False
                prev = h
        return True
