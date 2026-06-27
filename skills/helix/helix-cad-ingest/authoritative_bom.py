#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Authoritative parts master — emits PARTS_MASTER.md/.csv + FAB_ROUTING.md from a
versioned per-product CSV (the corrected source of truth that OVERRIDES the stale
title-block codes found in DXF/PDF detail sheets).

Data lives in masters/parts_master.<PRODUCT>.csv (NOT in this code) so a new
product = add one CSV, no code change. Columns:
  code,name,qty,material,stock,process,parent,note

  python authoritative_bom.py --out <dir>                         # default master (GIÁ TRƯỢT UUV)
  python authoritative_bom.py --master masters/parts_master.X.csv --product "X" --out <dir>
"""
import io, os, csv, argparse
from collections import defaultdict

COLS = ["code", "name", "qty", "material", "stock", "process", "parent", "note"]
_HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MASTER = os.path.join(_HERE, "masters", "parts_master.GIA-TRUOT-UUV.csv")
# Display names with full diacritics (filenames are ASCII-safe). Optional per master.
DISPLAY_NAMES = {"parts_master.GIA-TRUOT-UUV.csv": "GIÁ TRƯỢT UUV"}
# Optional per-master provenance note; falls back to a generic line.
GENERIC_SOURCE_NOTE = ("Nguồn chân lý: BOM PDF + tờ sắp hình laser. Mã đã **sửa** theo tờ BOM; "
                       "cột note đánh dấu mã khung tên sai trên tờ chi tiết.")
SOURCE_NOTES = {"parts_master.GIA-TRUOT-UUV.csv":
                ("Nguồn chân lý: BOM 3 PDF (nhóm 1/3/4) + 2 tờ sắp hình laser. Mã đã **sửa** theo tờ BOM; "
                 "cột note đánh dấu mã khung tên sai trên tờ chi tiết.")}


def load_master(path):
    """Read the versioned parts-master CSV → list of row-dicts (schema = COLS).
    Fail-safe: missing file / missing column = hard error, never fabricate."""
    if not os.path.isfile(path):
        raise SystemExit(f"[authoritative_bom] KHÔNG thấy master CSV: {path}\n"
                         f"  → tạo masters/parts_master.<PRODUCT>.csv với cột: {','.join(COLS)}")
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        rd = csv.DictReader(f)
        missing = [c for c in COLS if c not in (rd.fieldnames or [])]
        if missing:
            raise SystemExit(f"[authoritative_bom] master thiếu cột {missing} trong {path}")
        rows = []
        for r in rd:
            rows.append({c: (r.get(c) or "").strip() for c in COLS})
    if not rows:
        raise SystemExit(f"[authoritative_bom] master rỗng: {path}")
    return rows


def derive_product(master_path):
    base = os.path.basename(master_path)
    if base in DISPLAY_NAMES:
        return DISPLAY_NAMES[base]
    stem = base
    for pre in ("parts_master.", "parts-master."):
        if stem.startswith(pre):
            stem = stem[len(pre):]
    return os.path.splitext(stem)[0].replace("-", " ").replace("_", " ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=".")
    ap.add_argument("--master", default=DEFAULT_MASTER, help="parts_master CSV (versioned source of truth)")
    ap.add_argument("--product", default=None, help="tên sản phẩm cho tiêu đề (mặc định suy từ tên file master)")
    a = ap.parse_args()
    out = a.out
    os.makedirs(out, exist_ok=True)

    rows = load_master(a.master)
    product = a.product or derive_product(a.master)
    src_note = SOURCE_NOTES.get(os.path.basename(a.master), GENERIC_SOURCE_NOTE)

    # CSV (round-trip: re-emit canonical schema)
    with io.open(os.path.join(out, "PARTS_MASTER.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # PARTS_MASTER.md
    M = [f"# PARTS MASTER (authoritative) — {product}", "",
         f"> {src_note}", "",
         "| Mã đúng | Tên | SL | Vật liệu | Phôi/dày | Công nghệ | Thuộc cụm | Ghi chú |",
         "|---|---|--:|---|---|---|---|---|"]
    for r in rows:
        M.append(f"| {r['code']} | {r['name']} | {r['qty']} | {r['material']} | "
                 f"{r['stock']} | {r['process']} | {r['parent']} | {r['note']} |")
    with io.open(os.path.join(out, "PARTS_MASTER.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(M))

    # FAB_ROUTING.md — group by process + material/thickness for nesting
    leaf = [r for r in rows if r["process"] not in ("WELD-ASSY",)]
    R = [f"# FAB ROUTING — {product}", "",
         "Cut-list & routing theo trạm. SL = tổng/sản phẩm (đã nhân cụm con).", ""]
    laser = [r for r in leaf if "LASER" in r["process"]]
    nest = defaultdict(list)
    for r in laser:
        nest[(r["material"], r["stock"])].append(r)
    R.append("## TRẠM LASER + CHẤN (nhóm theo vật liệu × bề dày → sắp hình)")
    for (mat, th), items in sorted(nest.items()):
        tot = sum(int(i["qty"]) for i in items if i["qty"].isdigit())
        R.append(f"\n### {mat} — {th}  ({len(items)} loại, {tot} tấm)")
        for i in items:
            R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) {i['note']}")
    turn = [r for r in leaf if r["process"].startswith("TURN") or "MILL" in r["process"]]
    R.append("\n## TRẠM TIỆN / PHAY")
    for i in turn:
        R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) — {i['material']} {i['stock']} {i['note']}")
    buy = [r for r in leaf if "PURCHASE" in r["process"]]
    R.append("\n## MUA NGOÀI / CẮT PHÔI")
    for i in buy:
        R.append(f"- [{i['qty']}×] {i['name']} ({i['code']}) — {i['material']} {i['stock']}")
    R.append("\n## TRẠM HÀN (cụm lắp)")
    for r in rows:
        if r["process"] == "WELD-ASSY" or "WELD" in r["process"]:
            R.append(f"- {r['name']} ({r['code']}) ×{r['qty']} ⟶ thuộc {r['parent']}")
    with io.open(os.path.join(out, "FAB_ROUTING.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(R))

    # rollups
    mat = defaultdict(int)
    for r in leaf:
        if r["qty"].isdigit():
            mat[r["material"]] += int(r["qty"])
    print("master =", a.master)
    print("parts(rows)=", len(rows), " leaf=", len(leaf))
    print("material totals (pieces):", dict(mat))
    print("laser nesting groups:", {f"{m} {t}": len(v) for (m, t), v in nest.items()})
    print("wrote PARTS_MASTER.md/.csv + FAB_ROUTING.md ->", out)


if __name__ == "__main__":
    main()
