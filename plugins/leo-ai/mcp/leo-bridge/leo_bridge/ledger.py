"""Ledger JSONL append-only — traceability mọi exchange Leo (prompt, classification, verify, route)."""
import json
from datetime import datetime
from pathlib import Path


class Ledger:
    def __init__(self, dir_path):
        self.dir = Path(dir_path)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "ledger.jsonl"

    def _read_all(self) -> list[dict]:
        if not self.file.exists():
            return []
        return [
            json.loads(line)
            for line in self.file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def new_id(self) -> str:
        prefix = f"LEO-{datetime.now().strftime('%Y%m%d')}-"
        n = sum(
            1 for r in self._read_all()
            if r["exchange_id"].startswith(prefix) and r.get("event") == "created"
        )
        return f"{prefix}{n + 1:03d}"

    def append(self, exchange_id: str, event: str, **fields) -> dict:
        rec = {
            "exchange_id": exchange_id,
            "event": event,
            "ts": datetime.now().isoformat(timespec="seconds"),
            **fields,
        }
        with self.file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    def get(self, exchange_id: str) -> dict:
        merged: dict = {}
        for r in self._read_all():
            if r["exchange_id"] == exchange_id:
                merged.update(r)
        if not merged:
            raise KeyError(f"Không có exchange {exchange_id} trong ledger")
        return merged

    def list(self, status: str | None = None) -> list[dict]:
        by_id: dict[str, dict] = {}
        for r in self._read_all():
            by_id.setdefault(r["exchange_id"], {}).update(r)
        rows = list(by_id.values())
        return [r for r in rows if status is None or r.get("status") == status]
