#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aggregate helix-cad-ingest per-part JSON -> master BOM + critical-dims +
material/process rollup for forge-fabrication. Local only.

  python aggregate.py <dir_of_cad_extract_json> [--out <dir>]
"""
import sys, os, re, io, json, glob, argparse

# qty + accented names known from the PDF BOM (khung co so group only); others blank.
PDF_BOM = {
    "2.1": ("Tấm cơ sở", 1), "2.5": ("Gối đỡ đuôi xi lanh", 1),
    "2.2": ("Tai gá giá phụ", 1), "2.6": ("Trục quay giá phụ", 1),
    "2.7": ("Cữ chặn vị trí ban đầu", 1), "2.8": ("Thanh chống", 2),
    "2.9": ("Tai gá thanh chống", 2), "2.10": ("Con lăn cơ sở", 1),
    "2.3": ("Tai bắt khung cơ sở", 8), "2.4": ("Gân tăng cứng cơ sở", 5),
}


def clean_name(idx, fname):
    if idx in PDF_BOM:
        return PDF_BOM[idx][0]
    base = os.path.basename(fname)
    base = re.sub(r"\.cad_extract$", "", os.path.splitext(base)[0])
    base = re.sub(r"^\s*[\d.]+\s*", "", base)            # drop leading index
    base = re.sub(r"[-_]?tong lap", " (tổng lắp)", base)
    return base.strip().capitalize() or base


def process_of(notes):
    j = " ".join(notes).lower()
    tags = []
    if "laze" in j or "laser" in j or "chấn" in j:
        tags.append("laser-cut+bend")
    if "hàn" in j:
        tags.append("weld")
    if not tags:
        tags.append("machine/turn")
    return "+".join(tags)


def dims_brief(dims):
    vals = [d["value"] for d in dims if isinstance(d.get("value"), (int, float))]
    vals = sorted(set(round(v) for v in vals), reverse=True)
    return ", ".join(str(v) for v in vals[:6])


def holes_brief(holes):
    return " · ".join(f"Ø{h['dia']}×{h['count']}" for h in holes) or "-"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or a.dir
    files = sorted(glob.glob(os.path.join(a.dir, "*.cad_extract.json")))

    rows = []
    for fp in files:
        with io.open(fp, encoding="utf-8") as f:
            r = json.load(f)
        m = r["meta"]
        idx = m.get("file_index") or "?"
        rows.append({
            "idx": idx,
            "name": clean_name(idx, m["source_files"]["dxf"]),
            "code_dxf": m.get("code_in_dxf") or "—",
            "material": m.get("material") or "—",
            "qty": PDF_BOM.get(idx, ("", ""))[1] or "",
            "dims": dims_brief(r["dimensions"]),
            "holes": holes_brief(r["holes"]),
            "process": process_of(r.get("process_notes", [])),
            "confl": len(r.get("conflicts", [])),
            "dimrows": r["dimensions"],
            "surface": (r.get("surface_finish") or {}).get("value") or "",
        })

    def keyf(x):
        return [int(p) if p.isdigit() else 0 for p in str(x["idx"]).split(".")]
    rows.sort(key=keyf)

    # ---- MASTER BOM ----
    B = ["# MASTER BOM — GIÁ TRƯỢT UUV", "",
         f"> Nguồn: {len(rows)} file DXF (helix-cad-ingest). Khoá = file_index (tin cậy); code_in_dxf = LOW.", "",
         "| Idx | Tên | SL | Vật liệu | Process | KT chính (mm) | Lỗ | code_in_dxf | Conf |",
         "|---|---|---|---|---|---|---|---|---|"]
    for x in rows:
        B.append(f"| {x['idx']} | {x['name']} | {x['qty']} | {x['material']} | {x['process']} | {x['dims']} | {x['holes']} | {x['code_dxf']} | {x['confl']} |")

    # ---- MATERIAL ROLLUP ----
    from collections import Counter
    mat = Counter(x["material"] for x in rows)
    B += ["", "## Tổng hợp vật liệu (mua sắm)", "", "| Vật liệu | Số part |", "|---|---|"]
    for k, v in mat.most_common():
        B.append(f"| {k} | {v} |")

    proc = Counter(x["process"] for x in rows)
    B += ["", "## Tổng hợp công nghệ", "", "| Process | Số part |", "|---|---|"]
    for k, v in proc.most_common():
        B.append(f"| {k} | {v} |")

    # data-quality flags
    bad = [x for x in rows if x["code_dxf"].startswith("GT.00.01") and not str(x["idx"]).startswith("2")]
    nocode = [x for x in rows if x["code_dxf"] == "—"]
    B += ["", "## ⚠️ Cảnh báo chất lượng dữ liệu (sửa trước chế tạo)", ""]
    if bad:
        B.append("**Mã khung tên sai (mã nhóm khung cơ sở dán nhầm sang part khác):**")
        for x in bad:
            B.append(f"- `{x['idx']}` {x['name']} → code_in_dxf {x['code_dxf']} (cần đánh lại mã đúng nhóm)")
    if nocode:
        B.append("")
        B.append("**Không có mã trong khung tên:** " + ", ".join(x["idx"] for x in nocode))

    with io.open(os.path.join(out, "MASTER_BOM.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(B))

    # ---- CRITICAL DIMS ----
    D = ["# Critical dimensions — GIÁ TRƯỢT UUV", ""]
    for x in rows:
        if not x["dimrows"]:
            continue
        D.append(f"## [{x['idx']}] {x['name']}  ({x['material']})")
        D.append("| Value | Tol | Conf | Note |")
        D.append("|---|---|---|---|")
        for d in x["dimrows"]:
            D.append(f"| {d['value']} | {d['tolerance']} | {d['confidence']} | {d.get('note','')} |")
        D.append("")
    with io.open(os.path.join(out, "CRITICAL_DIMS.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(D))

    # ---- CSV for ERP ----
    C = ["idx,name,qty,material,process,key_dims_mm,holes,code_in_dxf,conflicts"]
    for x in rows:
        nm = x["name"].replace(",", " ")
        C.append(f'{x["idx"]},{nm},{x["qty"]},{x["material"]},{x["process"]},"{x["dims"]}","{x["holes"]}",{x["code_dxf"]},{x["confl"]}')
    with io.open(os.path.join(out, "MASTER_BOM.csv"), "w", encoding="utf-8") as f:
        f.write("\n".join(C))

    print(f"parts={len(rows)}  materials={dict(mat)}  process={dict(proc)}")
    print(f"stale-code parts={len(bad)}  no-code parts={len(nocode)}")
    print("wrote: MASTER_BOM.md, CRITICAL_DIMS.md, MASTER_BOM.csv ->", out)


if __name__ == "__main__":
    main()
