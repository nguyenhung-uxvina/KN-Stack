"""Propose-only routing — chỉ ghi khi CEO confirm; chặn UNVERIFIED vào BOM/parts_master.

parts_master_csv = file STAGING do CEO cấp đường dẫn — CEO merge tay vào parts_master
thật (không blind-append vào BOM production).
"""
import csv
from datetime import datetime
from pathlib import Path

BOM_TARGETS = {"parts_master_csv"}
NOTE_TARGETS = {"journal_md", "calc_md"}


class RouteBlockedError(Exception):
    pass


def propose_routes(mode: str, parsed: dict) -> list[dict]:
    routes = []
    if parsed.get("parts"):
        routes.append({
            "target_type": "parts_master_csv",
            "description": "Append part rows vào STAGING CSV (BOM mua ngoài — mọi mục phải VERIFIED trước)",
        })
    if mode in ("B", "C"):
        routes.append({
            "target_type": "calc_md",
            "description": "Lưu calc sheet markdown (mục UNVERIFIED được gắn nhãn rõ)",
        })
    routes.append({
        "target_type": "journal_md",
        "description": "Ghi design journal (luôn được phép, gắn nhãn UNVERIFIED nếu có)",
    })
    return routes


def write_route(exchange: dict, target_type: str, target_path: str, confirm: bool = False) -> str:
    if not confirm:
        raise RouteBlockedError("Propose-only: cần CEO ra lệnh rõ (confirm=true) mới ghi.")
    unverified = [c for c in exchange.get("checklist", []) if c.get("status") == "UNVERIFIED"]
    if target_type in BOM_TARGETS and unverified:
        raise RouteBlockedError(
            f"{len(unverified)} mục UNVERIFIED — CẤM ghi vào parts_master/BOM. "
            "Verify từng mục (leo_route verified_items=[...]) rồi gọi lại."
        )
    path = Path(target_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if target_type == "parts_master_csv":
        _append_parts_csv(path, exchange)
    elif target_type in NOTE_TARGETS:
        _append_note_md(path, exchange, unverified)
    else:
        raise RouteBlockedError(
            f"target_type '{target_type}' không hỗ trợ. Hợp lệ: {sorted(BOM_TARGETS | NOTE_TARGETS)}"
        )
    return str(path)


def _append_parts_csv(path: Path, exchange: dict) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "exchange_id", "source", "part_raw"])
        for p in exchange.get("parsed", {}).get("parts", []):
            w.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                exchange["exchange_id"],
                "leo",
                " | ".join(p["raw_cells"]),
            ])


def _append_note_md(path: Path, exchange: dict, unverified: list) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    label = f" — ⚠️ {len(unverified)} mục UNVERIFIED (không dùng cho BOM/bản vẽ)" if unverified else ""
    entry = (
        f"\n## Leo {exchange['exchange_id']} ({stamp}){label}\n"
        f"Mode: {exchange.get('mode')}\n\n{exchange.get('raw', '').strip()}\n"
    )
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
