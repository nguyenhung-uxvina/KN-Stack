#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rhino_check.py — Sensor tầng bản vẽ cho file Rhino .3dm (HU-rules, WX-QT-DRAWING-SENSOR-01)

Đọc .3dm bằng rhino3dm (openNURBS thuần — KHÔNG cần cài Rhino) và kiểm quy ước hull:
  HU-01  Thân vỏ là solid/polysurface KÍN (IsSolid)          — mặt hở → FAIL
  HU-02  Đơn vị mm + model absolute tolerance ≤ 0,01 mm      — sai → FAIL
  HU-03  Layer theo quy ước (VO_* / BOONG* / MOONPOOL* / DUONG_KC* / KET_CAU*)
  HU-04  UserText bắt buộc trên object: material (+ plate_mm với tấm) — Rhino không
         có vật liệu native, đây là quy ước THAY THẾ bắt buộc; material phải thuộc
         danh mục duyệt (schemas/materials.json)

GIỚI HẠN THÀNH THẬT: rhino3dm không tính được diện tích/thể tích (đó là RhinoCommon/
Rhino.Compute). HÌNH HỌC đi đường chuẩn WX-QT-CAD-IO-01: Rhino export STEP AP214 →
freecad_extract.py. Script này lo phần QUY ƯỚC + xuất **hull-material-map.json**
(tên object → material/plate_mm/layer) để gắn vật liệu vào seed STEP qua khớp tên.

Dùng:
    python rhino_check.py --file <hull.3dm> [--out <dir>] [--materials <json>]
Xuất <out>/rhino-check.json (dạng rule-entry F01) + <out>/hull-material-map.json
Exit: 0 PASS · 1 WARNING · 2 FAIL (không Released) · 3 thiếu môi trường/file.
"""
import argparse, json, os, sys

VERSION = "0.1.0"
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)
from validate_qtcn_seed import DEFAULT_MATERIALS, material_entry   # noqa: E402

LAYER_PREFIXES = ("VO", "BOONG", "MOONPOOL", "DUONG_KC", "KET_CAU", "THAM_CHIEU")

def main():
    ap = argparse.ArgumentParser(description="Sensor HU-rules cho Rhino .3dm")
    ap.add_argument("--file", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--materials", default=None)
    a = ap.parse_args()

    try:
        import rhino3dm as r3
    except ImportError:
        sys.stderr.write("[!] Thiếu rhino3dm. Cài: pip install rhino3dm\n"); sys.exit(3)
    if not os.path.exists(a.file):
        sys.stderr.write("[!] Không thấy file: %s\n" % a.file); sys.exit(3)
    catalog = DEFAULT_MATERIALS
    if a.materials:
        with open(a.materials, encoding="utf-8-sig") as f:
            catalog = json.load(f)

    m = r3.File3dm.Read(a.file)
    if m is None:
        sys.stderr.write("[!] rhino3dm không đọc được file (version quá mới/hỏng?)\n"); sys.exit(3)

    entries, matmap = [], []
    def add(rule, level, where, msg):
        entries.append({"rule": rule, "level": level, "where": where, "msg": msg})

    # ---------- HU-02: đơn vị + tolerance ----------
    units = str(m.Settings.ModelUnitSystem)
    if "Millimeters" not in units:
        add("HU-02", "FAIL", os.path.basename(a.file),
            "đơn vị model = %s (phải Millimeters) — nguồn số 1 của lỗi scale khi export STEP" % units)
    tol = m.Settings.ModelAbsoluteTolerance
    if tol > 0.01 + 1e-9:
        add("HU-02", "FAIL", os.path.basename(a.file),
            "model tolerance = %g (phải ≤ 0,01 mm) — tolerance lỏng làm SolidWorks/STEP không knit được solid kín" % tol)

    # ---------- duyệt object ----------
    layers = {i: (m.Layers[i].Name or "?") for i in range(len(m.Layers))}
    n_geom = 0
    for obj in m.Objects:
        g = obj.Geometry
        gtype = type(g).__name__
        if gtype in ("Light", "AnnotationBase", "TextDot", "InstanceReference"):
            continue
        name = obj.Attributes.Name or ("(không tên #%d)" % n_geom)
        lname = layers.get(obj.Attributes.LayerIndex, "?")
        n_geom += 1

        # HU-01: kín
        solid = getattr(g, "IsSolid", None)
        if solid is False:
            add("HU-01", "FAIL", name,
                "%s KHÔNG kín (surface hở) — Join + kiểm naked edges trong Rhino trước khi export" % gtype)
        elif solid is None and gtype == "Mesh":
            add("HU-01", "WARNING", name, "object là MESH, không phải NURBS — không dùng cho chế tạo")

        # HU-03: layer quy ước
        lnorm = lname.upper().replace(" ", "_")
        if not any(lnorm.startswith(p) for p in LAYER_PREFIXES):
            add("HU-03", "WARNING", name, "layer %r ngoài quy ước (VO_*/BOONG*/MOONPOOL*/DUONG_KC*/KET_CAU*)" % lname)

        # HU-04: UserText material (+ plate_mm)
        mat = obj.Attributes.GetUserString("material") or ""
        plate = obj.Attributes.GetUserString("plate_mm") or ""
        if not mat:
            add("HU-04", "FAIL", name,
                "thiếu UserText 'material' — Rhino không có vật liệu native, quy ước này BẮT BUỘC")
        elif material_entry(mat, catalog) is None:
            add("HU-04", "FAIL", name, "material %r ngoài danh mục duyệt" % mat)
        if mat and not plate:
            add("HU-04", "WARNING", name, "thiếu UserText 'plate_mm' (chiều dày tôn) — cần cho khối lượng tấm")
        matmap.append({"name": name, "layer": lname, "material": mat or None,
                       "plate_mm": plate or None, "closed": bool(solid)})

    if n_geom == 0:
        add("HU-01", "FAIL", os.path.basename(a.file), "không có object hình học nào")

    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_warn = sum(1 for e in entries if e["level"] == "WARNING")
    verdict = "FAIL" if n_fail else ("WARNING" if n_warn else "PASS")

    out_dir = a.out or os.path.dirname(os.path.abspath(a.file))
    os.makedirs(out_dir, exist_ok=True)
    rep = os.path.join(out_dir, os.path.splitext(os.path.basename(a.file))[0] + ".rhino-check.json")
    with open(rep, "w", encoding="utf-8") as f:
        json.dump({"form": "WX-QT-DRAWING-F01/rhino", "checker_version": VERSION,
                   "source": os.path.abspath(a.file), "verdict": verdict,
                   "released_allowed": verdict != "FAIL",
                   "counts": {"FAIL": n_fail, "WARNING": n_warn, "objects": n_geom},
                   "rules": entries}, f, ensure_ascii=False, indent=2)
    mm = os.path.join(out_dir, os.path.splitext(os.path.basename(a.file))[0] + ".material-map.json")
    with open(mm, "w", encoding="utf-8") as f:
        json.dump({"schema": "hull-material-map/v1", "source": os.path.abspath(a.file),
                   "objects": matmap,
                   "_note": "Gắn vật liệu vào seed STEP (freecad_extract) bằng khớp TÊN object — "
                            "hình học đi đường STEP AP214 theo WX-QT-CAD-IO-01."}, f,
                  ensure_ascii=False, indent=2)

    print("Wrote %s" % rep)
    print("Wrote %s (bản đồ vật liệu cho seed STEP)" % mm)
    print("VERDICT: %s  (FAIL=%d WARNING=%d | %d object)" % (verdict, n_fail, n_warn, n_geom))
    for e in entries:
        if e["level"] in ("FAIL", "WARNING"):
            print("  [%s] %s @ %s — %s" % (e["level"], e["rule"], e["where"], e["msg"]))
    sys.exit({"PASS": 0, "WARNING": 1, "FAIL": 2}[verdict])

if __name__ == "__main__":
    main()
