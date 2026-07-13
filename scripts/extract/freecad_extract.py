#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freecad_extract.py — Headless FreeCAD extractor (3D engine cho product-dossier)

Mở file CAD **3D** (STEP/IGES/FCStd, hoặc DWG/DXF-3D) bằng FreeCAD chạy nền, tính
**khối lượng thật** (V×ρ), bao hình (bounding box), diện tích bề mặt, và cây lắp ráp,
rồi xuất thẳng **qtcn-seed.json** (schema qtcn-seed/v1) — cắm nguyên vào pipeline hiện
có (qtcn --seed / product-dossier). Bổ trợ, KHÔNG thay parse_mech_drawing.py:
  - 2D DXF (chữ/dims/dung sai, TCVN3)  -> parse_mech_drawing.py  (engine 2D)
  - 3D solid (khối lượng/assembly/BOM) -> freecad_extract.py     (engine 3D)  ← file này

COD: Offload (đọc CAD -> JSON là biến đổi tất định; codify).

CHẠY (cần FreeCAD cài sẵn — script chạy TRONG python của FreeCAD).
KHUYẾN NGHỊ dùng **biến môi trường** (FreeCAD không đụng env → không có nhiễu
"File format not supported" và không mở nhầm file):
    FC_FILE=<part.step> FC_OUT=<dir> FC_NAME=<slug> freecadcmd freecad_extract.py
  (Windows PowerShell:)
    $env:FC_FILE="part.step"; $env:FC_OUT="out"; & "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" freecad_extract.py
Cách khác — truyền args qua '--pass' (freecadcmd sẽ in cảnh báo mở file, vô hại):
    freecadcmd freecad_extract.py --pass --file <part.step> --out <dir> --name <slug>

Thoát 0 nếu OK; 3 nếu không import được FreeCAD (kèm hướng dẫn); 2 nếu thiếu file.
"""
import argparse, json, os, re, sys

# --- density map (g/cm³) theo từ khóa vật liệu/label ---
DENSITY = [
    (("sus", "inox", "stainless", "304", "316"), 7.93, "SUS/inox"),
    (("eh32", "ct4", "thép", "thep", "steel", "carbon"), 7.85, "thép"),
    (("nhôm", "nhom", "alumin", "al5083", "5083", "6061"), 2.70, "nhôm"),
    (("composite", "frp", "grp", "glass", "sợi thủy tinh", "thuy tinh"), 1.70, "composite"),
    (("gỗ", "go ", "wood", "pine", "thông", "thong"), 0.55, "gỗ"),
    (("đồng", "dong", "brass", "bronze", "copper"), 8.5, "đồng/hợp kim"),
]
DEFAULT_DENSITY = 7.85  # thép — mặc định khi không nhận diện được

# --- suy VẬT LIỆU theo TÊN chi tiết (khi STEP mất nhãn vật liệu) ---
# Thứ tự: cụ thể trước. Mỗi rule: (từ khóa trong tên, tên vật liệu gán, ρ g/cm³).
# 'than phao' (thân phao/hull) = composite; 'hõm gỗ' = gỗ; CÒN LẠI = thép EH32.
# Lưu ý: 'phao' đơn thuần KHÔNG phải composite — Tai phao / Mã phao là mã thép.
NAME_MATERIAL = [
    (("than phao", "thanphao", "thân phao", "hull", "pontoon"), "Composite sợi thủy tinh", 1.70),
    (("hõm gỗ", "hom go", "hom_go", "wood chock"), "Gỗ thông", 0.55),
    (("khuôn phao", "khuon phao", "mould", "mold"), "Composite (khuôn — trang bị CN)", 1.70),
]
DEFAULT_MATERIAL = ("Thép EH32", 7.85)   # 'còn lại → thép EH32'

# --- MỘT NGUỒN: nạp đè từ schemas/materials.json nếu có (bảng trên = fallback khi
#     chạy lẻ ngoài repo). Sửa danh mục ở FILE, không sửa trong code. ---
_MAT_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                          "..", "..", "schemas", "materials.json"))
try:
    with open(_MAT_PATH, encoding="utf-8-sig") as _f:
        _m = json.load(_f)
    DENSITY = [(tuple(e["names"]), e["density_g_cm3"], e.get("label", "")) for e in _m["materials"]]
    NAME_MATERIAL = [(tuple(r["keys"]), r["material"], r["density_g_cm3"])
                     for r in _m.get("name_rules", [])]
    _d = _m.get("default_material")
    if _d:
        DEFAULT_MATERIAL = (_d["material"], _d["density_g_cm3"])
        DEFAULT_DENSITY = _d["density_g_cm3"]
except Exception:
    pass   # fallback nội tuyến ở trên

def density_for(text, default):
    t = (text or "").lower()
    for keys, rho, _label in DENSITY:
        if any(k in t for k in keys):
            return rho, False   # nhận diện được
    return default, True        # phải giả định

def material_for_name(label):
    """Suy (tên vật liệu, ρ) từ TÊN chi tiết. Trả None nếu không rule nào khớp -> dùng default."""
    t = (label or "").lower()
    for keys, mat, rho in NAME_MATERIAL:
        if any(k in t for k in keys):
            return mat, rho
    return None

def base_label(label):
    """'Dam_ngang_003' / 'Dam ngang (2)' / 'Bich (mat duoi)001' -> base để gộp instance đếm SL.
    Cắt hậu tố instance: (a) có DẤU PHÂN CÁCH (_001, (2), -1, .3, ' 2'); (b) hậu tố STEP
    zero-padded DÍNH LIỀN sau ký tự KHÔNG-phải-số (…duoi)001, …phao001) — Inventor→STEP
    nối '001','002' không có dấu phân cách. Vẫn KHÔNG cắt số dính chữ ngắn (EH32, M12) vì
    yêu cầu ≥3 chữ số cho nhánh (b)."""
    s = re.sub(r"(?:\(\d+\)|[ _\-.]\d{1,4}|(?<=\D)\d{3,})\s*$", "", label or "").strip(" _-.")
    return s or (label or "part")

def build_seed(doc, name=None, source_file=None, default_density=DEFAULT_DENSITY):
    """Duyệt tài liệu FreeCAD -> (seed_dict, raw_parts, meta). Dùng chung cho CLI & MCP addon.
    - Bỏ object 'container' (assembly wrapper) để tránh đếm trùng khối lượng.
    - Tính khối lượng thật (V×ρ), bbox, area; gộp instance theo base label -> BOM qty."""
    import FreeCAD
    def shape_children(o):
        return [l for l in (getattr(o, "OutList", []) or [])
                if getattr(l, "Shape", None) is not None and getattr(l.Shape, "Solids", None)]
    containers = {o.Name for o in doc.Objects if shape_children(o)}
    raw_parts, no_solid, overall = [], 0, None
    for obj in doc.Objects:
        if obj.Name in containers:
            continue
        shape = getattr(obj, "Shape", None)
        if shape is None or not getattr(shape, "Solids", None):
            continue
        solids = shape.Solids
        if not solids:
            no_solid += 1
            continue
        try:
            vol_mm3 = float(shape.Volume); area_mm2 = float(shape.Area); bb = shape.BoundBox
        except Exception:
            continue
        mat_name = ""
        for attr in ("ShapeMaterial", "Material"):
            m = getattr(obj, attr, None)
            if m is not None:
                mat_name = getattr(m, "Name", "") or getattr(m, "Label", "") or (m if isinstance(m, str) else "")
                if mat_name:
                    break
        # nhãn rỗng NGHĨA (STEP/Inventor hay gán 'Default'/'Generic') = coi như KHÔNG có vật liệu
        if mat_name.strip().lower() in ("", "default", "generic", "material", "<generic>", "none"):
            mat_name = ""
        # 1) vật liệu từ nhãn CAD (nếu có) → 2) suy theo TÊN chi tiết → 3) mặc định EH32
        if mat_name:
            rho, assumed = density_for(mat_name + " " + (obj.Label or ""), default_density)
            mat_source = "label"
        else:
            by_name = material_for_name(obj.Label or "")
            if by_name:
                mat_name, rho = by_name
                assumed, mat_source = False, "name_rule"   # gán chủ đích theo tên
            else:
                mat_name, rho = DEFAULT_MATERIAL
                assumed, mat_source = True, "default"       # 'còn lại → thép EH32' (giả định)
        raw_parts.append({
            "label": obj.Label, "base": base_label(obj.Label), "solids_n": len(solids),
            "volume_cm3": round(vol_mm3 / 1000.0, 2), "area_cm2": round(area_mm2 / 100.0, 2),
            "bbox_mm": {"x": round(bb.XLength, 2), "y": round(bb.YLength, 2), "z": round(bb.ZLength, 2)},
            "material": mat_name or None, "material_source": mat_source,
            "density_g_cm3": rho, "density_assumed": assumed,
            "mass_kg": round(vol_mm3 * rho / 1e6, 3),
        })
        overall = bb if overall is None else (overall.united(bb) if hasattr(overall, "united") else overall)

    groups = {}
    for p in raw_parts:
        g = groups.setdefault(p["base"], {"name": p["base"], "qty": 0, "masses": [], "_rep_mass": None,
                                          "material": p["material"], "material_source": p["material_source"],
                                          "density_g_cm3": p["density_g_cm3"],
                                          "density_assumed": p["density_assumed"], "bbox_mm": p["bbox_mm"],
                                          "volume_cm3": p["volume_cm3"], "area_cm2": p["area_cm2"]})
        g["qty"] += 1
        g["masses"].append(p["mass_kg"])
        # Instance ĐẠI DIỆN của nhóm = instance NHẸ NHẤT — khớp est_mass_kg (= min khi
        # mass_varies). Trước đây volume/bbox lấy từ instance ĐẦU TIÊN còn est_mass lấy
        # min → cặp mass↔volume thuộc 2 thanh khác nhau, sensor S1-01 FAIL đúng
        # (bắt trên Tong lap.iam thật: ISO L40x40x4 est 0,133 kg vs vol thanh dài 151 cm³).
        if g["_rep_mass"] is None or p["mass_kg"] < g["_rep_mass"]:
            g["_rep_mass"] = p["mass_kg"]
            g["bbox_mm"], g["volume_cm3"], g["area_cm2"] = p["bbox_mm"], p["volume_cm3"], p["area_cm2"]
    seed_bom = []
    for i, (base, g) in enumerate(sorted(groups.items()), 1):
        masses = g["masses"]
        mn, mx = min(masses), max(masses)
        # instance cùng base nhưng KHÁC khối lượng (vd thanh profile cùng loại, khác chiều dài
        # do Frame Generator) -> total = TỔNG THẬT các instance, không phải unit×qty.
        varies = (mx - mn) > max(0.005, 0.01 * mx)
        total = round(sum(masses), 3)
        spec = {"sections": [], "plate_mm": None, "tolerances": [], "key_dims": [],
                "est_mass_kg": round(mn, 3) if varies else masses[0],
                "total_mass_kg": total, "mass_varies": varies,
                "bbox_mm": g["bbox_mm"], "volume_cm3": g["volume_cm3"], "area_cm2": g["area_cm2"],
                "density_g_cm3": g["density_g_cm3"], "density_assumed": g["density_assumed"],
                "material_source": g["material_source"], "sheets": []}
        if varies:
            spec["unit_mass_range_kg"] = [round(mn, 3), round(mx, 3)]
        seed_bom.append({
            "vt": "VT%d" % i, "pos": i, "drawing_no": None, "name": g["name"], "qty": g["qty"],
            "material": g["material"] or "[CẦN VẬT LIỆU]", "specs": spec,
        })
    name = name or (os.path.splitext(os.path.basename(source_file))[0] if source_file else (getattr(doc, "Label", None) or "product"))
    principal = {}
    if overall is not None:
        principal = {"envelope_mm": {"L": round(overall.XLength, 1), "W": round(overall.YLength, 1),
                                     "H": round(overall.ZLength, 1)}}
    total_mass = round(sum(p["specs"]["total_mass_kg"] for p in seed_bom), 3)
    seed = {
        "schema": "qtcn-seed/v1", "engine": "freecad",
        "freecad_version": ".".join(str(x) for x in FreeCAD.Version()[:3]),
        "product": {"code": None, "name": name, "type": None, "units": "mm",
                    "principal_particulars": principal, "total_mass_kg": total_mass},
        "source": {"file": os.path.abspath(source_file) if source_file else None,
                   "objects": len(doc.Objects), "solid_parts": len(raw_parts)},
        "bom": seed_bom, "consumables": [], "relationships": [],
        "flags": {"from_3d_solids": True,
                  "some_density_assumed": any(p["specs"]["density_assumed"] for p in seed_bom),
                  "material_sources": {
                      k: sum(1 for p in seed_bom if p["specs"]["material_source"] == k)
                      for k in ("label", "name_rule", "default")}},
        "_note": "Nền tảng cho qtcn (--seed). est_mass_kg là KHỐI LƯỢNG THẬT từ solid 3D. "
                 "VT gán tự động; drawing_no/consumables/relationships để trống (điền tay/gộp seed 2D).",
    }
    return seed, raw_parts, {"groups": len(groups), "no_solid": no_solid}


def parse_args(argv):
    # freecadcmd: sys.argv = [freecadcmd.exe, script.py, <args…>] và chuyển args qua
    # '--pass'. Tách phần args CỦA SCRIPT: sau '--pass'/'--' nếu có, ngược lại bỏ mọi
    # token tới đường dẫn .py cuối cùng (là chính script này).
    for sep in ("--pass", "--"):
        if sep in argv:
            argv = argv[argv.index(sep) + 1:]
            break
    else:
        pyidx = [i for i, t in enumerate(argv) if isinstance(t, str) and t.lower().endswith(".py")]
        if pyidx:
            argv = argv[pyidx[-1] + 1:]
    ap = argparse.ArgumentParser(description="FreeCAD headless 3D extractor -> qtcn-seed.json")
    ap.add_argument("--file", default=None, help="STEP/IGES/FCStd/DWG/DXF 3D (hoặc env FC_FILE)")
    ap.add_argument("--out", default=None, help="thư mục ghi (mặc định = cạnh file; hoặc env FC_OUT)")
    ap.add_argument("--name", default=None, help="slug sản phẩm (mặc định từ tên file; hoặc env FC_NAME)")
    ap.add_argument("--default-density", type=float, default=DEFAULT_DENSITY,
                    help="ρ (g/cm³) khi không nhận diện vật liệu (mặc định thép 7,85)")
    a = ap.parse_args(argv)
    # fallback biến môi trường (cách gọi sạch nhất: FreeCAD không đụng tới env)
    a.file = a.file or os.environ.get("FC_FILE")
    a.out  = a.out  or os.environ.get("FC_OUT")
    a.name = a.name or os.environ.get("FC_NAME")
    return a

def main():
    for stream in (sys.stdout, sys.stderr):   # cp1252-safe (console Windows) — JSON luôn utf-8
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    a = parse_args(sys.argv[1:])
    if not a.file:
        sys.stderr.write("[!] Thiếu --file (hoặc env FC_FILE). Xem hướng dẫn ở đầu script.\n"); sys.exit(2)
    if not os.path.exists(a.file):
        sys.stderr.write("[!] Không thấy file: %s\n" % a.file); sys.exit(2)

    try:
        import FreeCAD  # noqa
    except Exception:
        sys.stderr.write(
            "[!] Không import được FreeCAD — script này phải chạy TRONG python của FreeCAD.\n"
            "    Cài FreeCAD rồi chạy (dùng --pass để chuyển args cho script):\n"
            "      freecadcmd freecad_extract.py --pass --file <part.step> --out <dir>\n"
            "    Windows (đường dẫn đầy đủ nếu freecadcmd không trên PATH):\n"
            "      \"C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe\" freecad_extract.py --pass --file ...\n"
            "    Lưu ý: DWG cần ODA File Converter khai trong FreeCAD Preferences > Import-Export > DWG.\n")
        sys.exit(3)

    import FreeCAD
    ext = os.path.splitext(a.file)[1].lower()
    doc = None
    try:
        if ext in (".fcstd",):
            doc = FreeCAD.open(a.file)
        else:
            import Import
            Import.open(a.file)          # STEP/IGES/BREP/… (DWG/DXF qua addon nếu bật)
            doc = FreeCAD.ActiveDocument
    except Exception as e:
        sys.stderr.write("[!] FreeCAD mở file thất bại: %s\n"
                         "    STEP/IGES/FCStd chạy tốt; DWG cần ODA; DXF-2D nên dùng parse_mech_drawing.py.\n" % e)
        sys.exit(1)
    if doc is None:
        sys.stderr.write("[!] Không tạo được tài liệu FreeCAD.\n"); sys.exit(1)

    seed, raw_parts, meta = build_seed(doc, a.name, a.file, a.default_density)
    name = seed["product"]["name"]
    out_dir = a.out or os.path.dirname(os.path.abspath(a.file))
    os.makedirs(out_dir, exist_ok=True)
    seed_path = os.path.join(out_dir, (a.name or "qtcn-seed") + ".json")
    raw_path = os.path.join(out_dir, name + ".freecad.json")
    with open(seed_path, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump({"parts": raw_parts, "groups": meta["groups"]}, f, ensure_ascii=False, indent=2)

    print("Wrote %s" % seed_path)
    ms = seed["flags"]["material_sources"]
    print("  parts=%d groups(BOM)=%d total_mass=%.3f kg | no_solid_objs=%d"
          % (len(raw_parts), meta["groups"], seed["product"]["total_mass_kg"], meta["no_solid"]))
    print("  material: label=%d name_rule=%d default_EH32=%d (density_assumed=%s)"
          % (ms["label"], ms["name_rule"], ms["default"], seed["flags"]["some_density_assumed"]))
    if not raw_parts:
        print("  [!] Không thấy solid 3D nào — có thể là bản vẽ 2D. Dùng parse_mech_drawing.py cho DXF 2D.")

# freecadcmd đặt __name__ = tên module (vd 'freecad_extract'), KHÔNG phải '__main__'.
# Chạy main() khi: (a) chạy trực tiếp bằng python, hoặc (b) file này là script entry
# mà freecadcmd đang thực thi (có trong sys.argv). Không chạy khi bị import bởi script khác.
_entry = any(isinstance(t, str) and t.replace("\\", "/").lower().endswith("freecad_extract.py")
             for t in sys.argv)
if __name__ == "__main__" or _entry:
    main()
