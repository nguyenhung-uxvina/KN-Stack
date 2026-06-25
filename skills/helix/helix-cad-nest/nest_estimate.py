#!/usr/bin/env python3
"""
nest_estimate.py — material-ordering cut-plan ESTIMATE for helix-cad-nest.

Honest scope (LLM Spatial Blindness boundary): this does NOT produce a
production nest. It groups sheet parts by material x thickness and runs a
bounding-box shelf bin-pack to give a LOWER-BOUND sheet count + utilization
for material ordering. True-shape nesting (which does the same or better)
is handed to a LOCAL tool (Deepnest/SVGnest/shop CAM) or the human nester.

Input (one of):
  --parts parts.csv   columns: code,material,thickness_mm,bbox_w,bbox_h,qty[,area_mm2]
  --parts parts.json  list of {code,material,thickness_mm,bbox_w,bbox_h,qty,area_mm2?}
  --dxf  <dir>        harvest closed-LWPOLYLINE bbox+area per .dxf (needs ezdxf);
                      material/thickness/qty must still come via --meta CSV/JSON.

Output (to --out dir):
  NEST_PLAN.md   CEO-readable per-group estimate
  CUT_LIST.csv   per-sheet rows for ERP / shop import

All file output is UTF-8. Run with PYTHONUTF8=1 on Windows.
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict


def _f(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def load_parts_csv(path):
    parts = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            parts.append(_norm_part(row))
    return parts


def load_parts_json(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return [_norm_part(r) for r in data]


def _norm_part(r):
    w = _f(r.get("bbox_w"))
    h = _f(r.get("bbox_h"))
    area = _f(r.get("area_mm2")) or (w * h)  # fall back to bbox area
    qty = int(_f(r.get("qty"), 1)) or 1
    return {
        "code": str(r.get("code") or r.get("item") or "?").strip(),
        "material": str(r.get("material") or "?").strip(),
        "thickness_mm": _f(r.get("thickness_mm")),
        "bbox_w": w,
        "bbox_h": h,
        "area_mm2": area,
        "qty": qty,
    }


def harvest_dxf(dxf_dir, meta_by_code):
    """bbox + closed-polyline area per DXF; merges material/thickness/qty from meta."""
    try:
        import ezdxf
    except ImportError:
        sys.exit("[ERR] --dxf needs ezdxf: pip install ezdxf")
    parts = []
    for fn in sorted(os.listdir(dxf_dir)):
        if not fn.lower().endswith(".dxf"):
            continue
        code = os.path.splitext(fn)[0]
        try:
            doc = ezdxf.readfile(os.path.join(dxf_dir, fn))
        except Exception:
            from ezdxf import recover
            doc, _ = recover.readfile(os.path.join(dxf_dir, fn))
        msp = doc.modelspace()
        xs, ys, area = [], [], 0.0
        for e in msp.query("LWPOLYLINE"):
            pts = [(p[0], p[1]) for p in e.get_points()]
            xs += [p[0] for p in pts]
            ys += [p[1] for p in pts]
            if e.closed and len(pts) >= 3:  # shoelace
                a = 0.0
                for i in range(len(pts)):
                    x1, y1 = pts[i]
                    x2, y2 = pts[(i + 1) % len(pts)]
                    a += x1 * y2 - x2 * y1
                area = max(area, abs(a) / 2.0)
        bbox_w = (max(xs) - min(xs)) if xs else 0.0
        bbox_h = (max(ys) - min(ys)) if ys else 0.0
        meta = meta_by_code.get(code, {})
        parts.append(_norm_part({
            "code": code, "material": meta.get("material", "?"),
            "thickness_mm": meta.get("thickness_mm", 0),
            "bbox_w": bbox_w, "bbox_h": bbox_h,
            "area_mm2": area or bbox_w * bbox_h, "qty": meta.get("qty", 1),
        }))
    return parts


def shelf_pack(rects, sheet_w, sheet_h, gap):
    """First-fit-decreasing shelf bin-pack of (w,h) rects. Returns sheet count.
    Each part is oriented long-side along the sheet's long side (so a part longer
    than the sheet width but shorter than its length still fits). A part that
    exceeds the sheet in BOTH orientations is flagged oversize."""
    sheet_short, sheet_long = sorted((sheet_w, sheet_h))
    # pack space oriented as W=sheet_long (shelf run), H=sheet_short (shelf stack)
    sheet_w, sheet_h = sheet_long, sheet_short
    norm = []
    oversize = []
    for w, h, code in rects:
        p_long, p_short = max(w, h), min(w, h)   # long side runs along sheet_long
        if p_long + gap > sheet_w or p_short + gap > sheet_h:
            oversize.append(code)
            continue
        norm.append((p_long, p_short))
    norm.sort(key=lambda r: r[1], reverse=True)

    sheets = 0
    # shelves: list of [remaining_width, shelf_height]; y-cursor tracked per sheet
    def new_sheet():
        return {"y": 0.0, "shelf_w_left": 0.0, "shelf_h": 0.0}

    sheet = None
    sheets_list = []
    for w, h in norm:
        placed = False
        for sh in sheets_list:
            # try current open shelf
            if w + gap <= sh["shelf_w_left"] and h <= sh["shelf_h"]:
                sh["shelf_w_left"] -= (w + gap)
                placed = True
                break
            # try opening a new shelf on this sheet
            if sh["y"] + h + gap <= sheet_h:
                sh["y"] += sh["shelf_h"] + gap if sh["shelf_h"] else 0.0
                if sh["y"] + h <= sheet_h:
                    sh["shelf_h"] = h
                    sh["shelf_w_left"] = sheet_w - (w + gap)
                    placed = True
                    break
        if not placed:
            sh = new_sheet()
            sh["shelf_h"] = h
            sh["shelf_w_left"] = sheet_w - (w + gap)
            sheets_list.append(sh)
    return max(len(sheets_list), 0), oversize


def selftest():
    """DXF-mode self-test: generate flat-pattern DXFs in a temp dir, harvest via
    ezdxf, group + pack, and assert the pipeline holds. No fixtures committed."""
    import tempfile
    try:
        import ezdxf
    except ImportError:
        sys.exit("[SKIP] selftest needs ezdxf: pip install ezdxf")
    d = tempfile.mkdtemp(prefix="nest_selftest_")

    def rect(name, w, h):
        doc = ezdxf.new("R2013")
        doc.modelspace().add_lwpolyline([(0, 0), (w, 0), (w, h), (0, h)], close=True)
        doc.saveas(os.path.join(d, name))

    rect("BR-01.dxf", 400, 300)
    rect("BR-02.dxf", 250, 180)
    rect("PL-09.dxf", 900, 650)
    meta = {
        "BR-01": {"code": "BR-01", "material": "Nhom 5083", "thickness_mm": 3, "qty": 6},
        "BR-02": {"code": "BR-02", "material": "Nhom 5083", "thickness_mm": 3, "qty": 10},
        "PL-09": {"code": "PL-09", "material": "SS400", "thickness_mm": 6, "qty": 3},
    }
    parts = harvest_dxf(d, meta)
    assert len(parts) == 3, f"expected 3 parts, got {len(parts)}"
    by_code = {p["code"]: p for p in parts}
    # closed-polyline area read from DXF (shoelace), not bbox fallback
    assert abs(by_code["BR-01"]["area_mm2"] - 400 * 300) < 1, "BR-01 area mis-read"
    assert abs(by_code["PL-09"]["bbox_w"] - 900) < 1, "PL-09 bbox mis-read"
    groups = defaultdict(list)
    for p in parts:
        groups[(p["material"], p["thickness_mm"])].append(p)
    assert len(groups) == 2, f"expected 2 material x thickness groups, got {len(groups)}"
    sheets, oversize = shelf_pack(
        [(p["bbox_w"], p["bbox_h"], p["code"]) for p in parts for _ in range(p["qty"])],
        1500, 3000, 5.2)
    assert sheets >= 1 and not oversize, "pack failed / unexpected oversize"
    print(f"[PASS] selftest: 3 DXF harvested, 2 groups, areas+bbox OK, pack={sheets} sheet(s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="run DXF-mode self-test and exit")
    ap.add_argument("--parts", help="parts.csv or parts.json")
    ap.add_argument("--dxf", help="dir of flat-pattern .dxf")
    ap.add_argument("--meta", help="CSV/JSON of code->material,thickness_mm,qty (for --dxf)")
    ap.add_argument("--sheet", default="1500x3000", help="stock sheet WxH mm")
    ap.add_argument("--kerf", type=float, default=0.2, help="cut kerf mm")
    ap.add_argument("--gap", type=float, default=5.0, help="part-to-part gap mm")
    ap.add_argument("--out", default=".", help="output dir")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return

    sw, sh = (float(x) for x in args.sheet.lower().split("x"))
    spacing = args.gap + args.kerf

    if args.parts and args.parts.lower().endswith(".json"):
        parts = load_parts_json(args.parts)
    elif args.parts:
        parts = load_parts_csv(args.parts)
    elif args.dxf:
        meta_by_code = {}
        if args.meta:
            rows = (load_parts_json(args.meta) if args.meta.endswith(".json")
                    else load_parts_csv(args.meta))
            meta_by_code = {r["code"]: r for r in rows}
        parts = harvest_dxf(args.dxf, meta_by_code)
    else:
        sys.exit("[ERR] supply --parts or --dxf")

    groups = defaultdict(list)
    for p in parts:
        groups[(p["material"], p["thickness_mm"])].append(p)

    os.makedirs(args.out, exist_ok=True)
    sheet_area = sw * sh
    md = ["# NEST PLAN (ESTIMATE — bbox lower bound, NOT a production nest)\n",
          f"Sheet: {sw:.0f}x{sh:.0f} mm | kerf {args.kerf} | gap {args.gap} mm\n",
          "> True-shape nesting on a local tool needs the SAME or FEWER sheets.\n"]
    cut_rows = [("group_material", "thickness_mm", "code", "qty",
                 "bbox_w", "bbox_h", "area_mm2", "sheets_est", "util_pct_est")]

    tot_sheets = 0
    for (mat, thk), gparts in sorted(groups.items()):
        rects = []
        part_area = 0.0
        for p in gparts:
            for _ in range(p["qty"]):
                rects.append((p["bbox_w"], p["bbox_h"], p["code"]))
            part_area += p["area_mm2"] * p["qty"]
        sheets, oversize = shelf_pack(rects, sw, sh, spacing)
        sheets = max(sheets, 1)
        util = 100.0 * part_area / (sheets * sheet_area) if sheets else 0.0
        scrap = 100.0 - util
        tot_sheets += sheets
        md.append(f"\n## {mat} — {thk:g} mm\n")
        md.append(f"- Parts: {len(gparts)} ({sum(p['qty'] for p in gparts)} pcs)\n")
        md.append(f"- Sheets needed (ESTIMATE): **{sheets}**  ·  "
                  f"utilization ~{util:.0f}%  ·  scrap ~{scrap:.0f}%\n")
        if oversize:
            md.append(f"- ⚠️ OVERSIZE (won't fit sheet): {', '.join(oversize)}\n")
        for p in gparts:
            cut_rows.append((mat, f"{thk:g}", p["code"], p["qty"],
                             f"{p['bbox_w']:.0f}", f"{p['bbox_h']:.0f}",
                             f"{p['area_mm2']:.0f}", sheets, f"{util:.0f}"))

    md.append(f"\n---\n**Total sheets (estimate): {tot_sheets}** across "
              f"{len(groups)} material×thickness groups.\n")
    md.append("\n_Estimate only — confirm against the nesting/sắp-hình sheet "
              "(authoritative cut-list) and run the true-shape nest locally._\n")

    with open(os.path.join(args.out, "NEST_PLAN.md"), "w", encoding="utf-8") as fh:
        fh.writelines(md)
    with open(os.path.join(args.out, "CUT_LIST.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(cut_rows)
    print(f"[OK] {len(groups)} groups, ~{tot_sheets} sheets -> {args.out}/NEST_PLAN.md + CUT_LIST.csv")


if __name__ == "__main__":
    main()
