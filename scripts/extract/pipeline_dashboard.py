#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline_dashboard.py — Bảng trạng thái 1 TRANG cho CEO: gộp mọi report của pipeline

Quét cây thư mục (vd _QTCN_export/ hoặc thư mục dự án) tìm mọi report mà pipeline
sinh ra và gộp thành 1 bảng + danh sách "việc đang chặn":

  *.validation.json        — tầng trích xuất (G1/S2/G3)
  drawing_report.json      — tầng bản vẽ D1+SEC (drawing_check.py / Apprentice)
  drawing_live_report.json — tầng bản vẽ D2/D3 (iLogic sống)
  *.rhino-check.json       — tầng bản vẽ HU (Rhino)
  weld-report.json         — chiều dài hàn + interference + trùng hình học
  *.trace.json             — tầng AI (truy vết số)
  giao-viec.csv            — phiếu giao việc còn tồn

Dùng:  python pipeline_dashboard.py --root <thư mục> [--out dashboard.md]
Exit 0 luôn (công cụ nhìn, không phải gate).
"""
import argparse, csv, json, os, sys
from collections import defaultdict

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

ICON = {"PASS": "✅", "WARNING": "⚠️", "FAIL": "❌", None: "—"}

def jload(p):
    try:
        with open(p, encoding="utf-8-sig") as f:
            return json.load(f)
    except Exception:
        return None

def main():
    ap = argparse.ArgumentParser(description="Dashboard 1 trang cho CAD pipeline")
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", default=None, help="ghi markdown (mặc định <root>/dashboard.md)")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        sys.stderr.write("[!] Không thấy thư mục %s\n" % root); sys.exit(3)

    prods = defaultdict(dict)   # thư mục sản phẩm -> khối trạng thái
    blockers = []

    for dirpath, _dirs, files in os.walk(root):
        rel = os.path.relpath(dirpath, root) or "."
        P = prods[rel]
        for fn in files:
            p = os.path.join(dirpath, fn)
            low = fn.lower()
            if low.endswith(".validation.json"):
                d = jload(p)
                if d:
                    which = "cross" if "cross" in low else "extract"
                    cur = P.get(which)
                    v = d.get("verdict")
                    # giữ verdict XẤU nhất trong thư mục
                    rank = {"FAIL": 2, "WARNING": 1, "PASS": 0}
                    if cur is None or rank.get(v, 0) > rank.get(cur, 0):
                        P[which] = v
                    if v == "FAIL":
                        blockers.append("%s: %s FAIL (Gate G1%s)" % (rel, fn, " kiểm chéo" if which == "cross" else ""))
            elif low == "drawing_report.json" or low == "drawing_live_report.json" or low.endswith(".rhino-check.json"):
                d = jload(p)
                if d:
                    v = d.get("verdict")
                    rank = {"FAIL": 2, "WARNING": 1, "PASS": 0}
                    if rank.get(v, 0) > rank.get(P.get("drawing"), -1 if P.get("drawing") is None else rank.get(P.get("drawing"), 0)):
                        P["drawing"] = v
                    if v == "FAIL":
                        blockers.append("%s: %s FAIL (Gate 1 bản vẽ — xem giao-viec.csv)" % (rel, fn))
            elif low == "weld-report.json":
                d = jload(p)
                if d:
                    P["weld_m"] = d.get("total_joint_line_m")
                    P["intf"] = d.get("interference_pairs")
                    P["dup"] = d.get("duplicate_pairs")
                    if d.get("duplicate_pairs"):
                        blockers.append("%s: %d cặp TRÙNG hình học trong STEP — nghi đếm trùng khối lượng"
                                        % (rel, d["duplicate_pairs"]))
            elif low.endswith(".trace.json"):
                d = jload(p)
                if d:
                    P["ai"] = d.get("verdict")
                    if d.get("verdict") == "FAIL":
                        blockers.append("%s: %s — %d số mồ côi (nghi AI bịa)"
                                        % (rel, fn, d.get("counts", {}).get("orphan", 0)))
            elif low == "giao-viec.csv":
                try:
                    with open(p, encoding="utf-8-sig", newline="") as f:
                        todo = sum(1 for r in csv.DictReader(f)
                                   if (r.get("can_bo_sung") or "").strip() not in ("", "ĐẠT D1"))
                    P["ticket"] = todo
                    if todo:
                        blockers.append("%s: giao-viec.csv còn %d part chờ bên thiết kế" % (rel, todo))
                except Exception:
                    pass

    rows = {k: v for k, v in prods.items() if v}
    lines = ["# CAD PIPELINE — DASHBOARD", "", "Root: `%s`" % root, "",
             "| Sản phẩm/thư mục | Bản vẽ | Trích xuất | Kiểm chéo | Đầu ra AI | Hàn (m) | INTF | Trùng | Giao việc |",
             "|---|---|---|---|---|---|---|---|---|"]
    for k in sorted(rows):
        P = rows[k]
        lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            k, ICON.get(P.get("drawing")), ICON.get(P.get("extract")), ICON.get(P.get("cross")),
            ICON.get(P.get("ai")),
            P.get("weld_m", "—"), P.get("intf", "—"), P.get("dup", "—"),
            ("%d part" % P["ticket"]) if P.get("ticket") else ("0" if "ticket" in P else "—")))
    lines += ["", "## Việc đang chặn (%d)" % len(blockers), ""]
    lines += (["- %s" % b for b in blockers] or ["- (không có — pipeline sạch)"])

    out = a.out or os.path.join(root, "dashboard.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nWrote %s" % out)
    sys.exit(0)

if __name__ == "__main__":
    main()
