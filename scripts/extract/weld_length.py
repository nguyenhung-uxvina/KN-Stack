#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
weld_length.py — v0: ước lượng CHIỀU DÀI MỐI HÀN từ solid 3D (FreeCAD headless)

Đóng lỗ hổng dữ liệu lớn nhất của định mức (U1 hội đồng CAD-AI): giờ công hàn =
chiều dài hàn × định mức m/giờ theo tư thế — trước giờ chiều dài hàn nhập tay.

NGUYÊN LÝ v0 (heuristic hàn góc/giáp mối cho kết cấu tấm + thép hình):
  Hai solid TIẾP XÚC nhau → đường bao vùng tiếp xúc (giao tuyến bề mặt) chính là
  đường chân mối hàn chạy quanh chỗ ghép. Script lấy section(A,B) từng cặp solid có
  bbox chạm nhau, tổng chiều dài cạnh giao tuyến = `joint_line_mm` của cặp đó.

ĐỌC SỐ CHO ĐÚNG (ghi thẳng vào report):
  - joint_line_mm = CHU VI vùng tiếp xúc. Mối hàn góc 2 phía suốt ≈ chu vi (2 cạnh
    dài ≈ 2L); hàn 1 phía ≈ chu vi/2; hàn ngắt quãng → nhân hệ số bước. Tức đây là
    CẬN TRÊN hình học — hệ số quy đổi theo WPS/tư thế hiệu chỉnh ở tầng định mức.
  - KHÔNG phân biệt được cặp "hàn" với cặp "bắt bulông/tiếp xúc lắp" — kỹ sư rà cột
    `welded?` trong report (mặc định true, sửa false cho mối bulông) trước khi dùng.
  - Gate G3: số phải kiểm trên golden/case thật đo tay trước khi vào định mức chính thức.

CHẠY (trong python của FreeCAD, như freecad_extract — dùng ENV, không args):
    FC_FILE=<asm.step> FC_OUT=<dir> freecadcmd weld_length.py
    FC_SELFTEST=1 freecadcmd weld_length.py            # kiểm giải tích chữ T (420 mm)
  (Quirk freecadcmd: có args thừa sau tên script thì stdout bị nuốt dù script vẫn
   chạy đúng — vì vậy mọi tham số đi qua env var.)
Xuất <out>/weld-report.json. Exit 0 OK · 1 selftest sai · 2 thiếu file · 3 thiếu FreeCAD.
"""
import json, os, sys

TOUCH_TOL_MM = 0.5      # nới bbox khi tìm cặp chạm nhau
MIN_EDGE_MM = 5.0       # bỏ giao tuyến vụn (nhiễu tiếp xúc điểm/cạnh)
VERSION = "0.1.0"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

def collect_solids(doc):
    """Danh sách (label, shape) — bỏ container assembly như freecad_extract."""
    def kids(o):
        return [l for l in (getattr(o, "OutList", []) or [])
                if getattr(l, "Shape", None) is not None and getattr(l.Shape, "Solids", None)]
    containers = {o.Name for o in doc.Objects if kids(o)}
    out = []
    for o in doc.Objects:
        if o.Name in containers:
            continue
        sh = getattr(o, "Shape", None)
        if sh is not None and getattr(sh, "Solids", None):
            out.append((o.Label, sh))
    return out

def bbox_touch(a, b, tol):
    ba, bb = a.BoundBox, b.BoundBox
    return not (ba.XMax + tol < bb.XMin or bb.XMax + tol < ba.XMin or
                ba.YMax + tol < bb.YMin or bb.YMax + tol < ba.YMin or
                ba.ZMax + tol < bb.ZMin or bb.ZMax + tol < ba.ZMin)

def joint_line(sa, sb):
    """Tổng chiều dài giao tuyến bề mặt giữa 2 solid (mm); 0 nếu không chạm."""
    try:
        sec = sa.section(sb)
        return sum(e.Length for e in sec.Edges if e.Length >= MIN_EDGE_MM)
    except Exception:
        return 0.0

def overlap_volume(sa, sb):
    """Thể tích giao (mm³) — >0 nghĩa là 2 solid CÀI vào nhau (interference)."""
    try:
        return float(sa.common(sb).Volume)
    except Exception:
        return 0.0

def analyze(doc, out_dir, source_file=None):
    """Phân loại từng cặp solid chạm nhau (bài học field Tong lap: v0 cộng dồn cả cặp
    trùng hình học 18 m/cặp → 1989 m phi lý):
      - weld        : chạm mặt, thể tích giao ≈ 0 → giao tuyến là ứng viên mối hàn
      - interference: thể tích giao > 1 mm³ → hai chi tiết CÀI nhau — chính là rule
                      D2-04 (WX-QT-DRAWING-SENSOR-01) đo bằng FreeCAD; loại khỏi tổng hàn
      - duplicate   : thể tích giao ≈ thể tích chi tiết nhỏ hơn → hình học TRÙNG LẶP
                      trong STEP (xuất đúp) — lỗi dữ liệu nguồn, phải rà"""
    solids = collect_solids(doc)
    welds, inters, dups, checked = [], [], [], 0
    for i in range(len(solids)):
        for j in range(i + 1, len(solids)):
            la, sa = solids[i]
            lb, sb = solids[j]
            if not bbox_touch(sa, sb, TOUCH_TOL_MM):
                continue
            checked += 1
            L = joint_line(sa, sb)
            if L <= 0:
                continue
            vol = overlap_volume(sa, sb)
            if vol > 1.0:
                vmin = min(sa.Volume, sb.Volume)
                if vmin > 0 and vol >= 0.98 * vmin:
                    dups.append({"a": la, "b": lb, "overlap_mm3": round(vol, 1)})
                else:
                    inters.append({"a": la, "b": lb, "overlap_mm3": round(vol, 1),
                                   "joint_line_mm": round(L, 1)})
            else:
                welds.append({"a": la, "b": lb, "joint_line_mm": round(L, 1), "welded?": True})
    total = round(sum(p["joint_line_mm"] for p in welds), 1)
    report = {
        "schema": "weld-report/v0.2", "version": VERSION,
        "source": os.path.abspath(source_file) if source_file else None,
        "solids": len(solids), "pairs_checked": checked,
        "weld_pairs": len(welds), "interference_pairs": len(inters), "duplicate_pairs": len(dups),
        "total_joint_line_mm": total,
        "total_joint_line_m": round(total / 1000.0, 2),
        "pairs": sorted(welds, key=lambda p: -p["joint_line_mm"]),
        "interferences": sorted(inters, key=lambda p: -p["overlap_mm3"])[:200],
        "duplicates": dups,
        "_note": ("v0.2: joint_line_mm = CHU VI vùng tiếp xúc (cận trên; hàn 2 phía suốt "
                  "≈ chu vi, 1 phía ≈ /2, ngắt quãng × hệ số bước). Kỹ sư rà 'welded?' "
                  "(bulông → false). interferences = D2-04 (chi tiết cài nhau — mối ghép "
                  "chưa cắt vát HOẶC lỗi model); duplicates = hình học xuất đúp trong STEP "
                  "(lỗi dữ liệu nguồn). Chưa qua G3 — chưa dùng cho hồ sơ chính thức."),
    }
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "weld-report.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("Wrote %s" % path)
    print("  solids=%d | cặp weld=%d | interference(D2-04)=%d | trùng hình học=%d"
          % (len(solids), len(welds), len(inters), len(dups)))
    print("  Σ giao tuyến HÀN = %.1f mm (%.2f m)" % (total, total / 1000.0))
    for p in report["pairs"][:8]:
        print("    %-28s ↔ %-28s %8.1f mm" % (p["a"][:28], p["b"][:28], p["joint_line_mm"]))
    return report

def selftest():
    """Chữ T giải tích: tấm đế 200×100×10 + sườn 200×10×50 đặt giữa mặt trên.
    Vùng tiếp xúc 200×10 → chu vi giao tuyến = 2×(200+10) = 420 mm."""
    import FreeCAD, Part
    doc = FreeCAD.newDocument("weldtest")
    base = doc.addObject("Part::Feature", "TamDe"); base.Shape = Part.makeBox(200, 100, 10)
    rib = doc.addObject("Part::Feature", "SuonDung")
    rib.Shape = Part.makeBox(200, 10, 50, FreeCAD.Vector(0, 45, 10))
    rep = analyze(doc, os.environ.get("FC_OUT") or os.getcwd(), "selftest-T-joint")
    got = rep["total_joint_line_mm"]
    ok = abs(got - 420.0) <= 1.0
    print("SELFTEST chữ T: kỳ vọng 420.0 mm — đo được %.1f mm → %s" % (got, "ĐẠT" if ok else "SAI"))
    return ok

def main():
    argv = sys.argv[1:]
    if "--pass" in argv:
        argv = argv[argv.index("--pass") + 1:]
    try:
        import FreeCAD  # noqa
    except Exception:
        sys.stderr.write("[!] Phải chạy trong python của FreeCAD:  freecadcmd weld_length.py\n")
        sys.exit(3)
    if "--selftest" in argv or os.environ.get("FC_SELFTEST"):
        sys.exit(0 if selftest() else 1)

    src = os.environ.get("FC_FILE")
    if not src or not os.path.exists(src):
        sys.stderr.write("[!] Thiếu env FC_FILE (file STEP/FCStd) hoặc file không tồn tại.\n")
        sys.exit(2)
    import FreeCAD
    if src.lower().endswith(".fcstd"):
        doc = FreeCAD.open(src)
    else:
        import Import
        Import.open(src)
        doc = FreeCAD.ActiveDocument
    analyze(doc, os.environ.get("FC_OUT") or os.path.dirname(os.path.abspath(src)), src)
    sys.exit(0)

_entry = any(isinstance(t, str) and t.replace("\\", "/").lower().endswith("weld_length.py")
             for t in sys.argv)
if __name__ == "__main__" or _entry:
    main()
