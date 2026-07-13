#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventor_apprentice_extract.py — Adapter Inventor HEADLESS qua Apprentice Server
Phiên bản: 0.1.0 (skeleton)

Đọc .ipt/.iam KHÔNG cần mở Inventor UI: Apprentice Server đi kèm bộ cài Inventor
hoặc **Inventor View (miễn phí)** — máy batch trích xuất trong vùng nội bộ không
tốn seat license. Xuất qtcn-seed.json (schema qtcn-seed/v1) — drop-in cho
merge_qtcn_seeds.py / qtcn --seed, cùng pipeline với bom_xlsx_to_seed.py.

⚠️ LƯU Ý TRUNG THỰC:
  - ĐÃ chạy sống lần đầu 2026-07-02 trên Tong lap.iam thật (Inventor 2018, 49 part:
    Part Number/material/hash đọc đúng; file legacy đó 0/49 có mass cache nên nhánh
    mass chưa được kiểm chứng thật). Theo Gate G3 (docs/WX-QT-EXTRACT-SENSOR-01.md):
    **vẫn bắt buộc qua golden set nhánh inventor/ có đáp án đo tay trước khi tin
    số khối lượng cho sản xuất.**
  - Khối lượng/thể tích đọc từ iProperties "Design Tracking Properties" là giá trị
    Inventor CACHE ở lần lưu cuối — nếu model sửa mà chưa Update/Save thì số cũ.
    Sensor S1-01/S1-08 nhúng sẵn bên dưới sẽ kiểm chéo mass ↔ V×ρ để lộ cả lỗi
    cache lẫn lỗi quy đổi đơn vị.
  - QTY trong assembly: Apprentice không expose BOM đầy đủ như Inventor thật —
    script đếm số THAM CHIẾU duy nhất (qty_source="unique_refs" = KHÔNG tin cậy cho
    chi tiết lặp). Số lượng lắp THẬT lấy từ BOM export (bom_xlsx_to_seed.py) rồi
    merge_qtcn_seeds.py — đây vẫn là nguồn vàng cho QTY.

BẪY ĐƠN VỊ INVENTOR (lý do có khối UNIT_* tường minh):
  API trả theo đơn vị database: length cm, volume cm³, area cm², mass kg —
  KHÔNG phải mm như hiển thị. Golden set nhánh Inventor phải có mẫu kiểm chứng
  chính các hằng số quy đổi này (rule S1-08 bắt hệ số 10/1000 nếu quy đổi sai).

DÙNG:
    pip install pywin32
    python inventor_apprentice_extract.py --file <part.ipt|asm.iam> [--out <dir>]
        [--name qtcn-seed-apprentice] [--operator <ten>] [--product-name <ten>]
Thoát: 0 OK · 1 OK kèm WARNING nội bộ · 2 sensor S1 nhúng FAIL (seed vẫn ghi,
validated=false) · 3 thiếu pywin32/Apprentice/file.
Sau khi xuất, chạy bộ sensor đầy đủ:  validate_qtcn_seed.py --seed <seed.json>
"""
import argparse, getpass, hashlib, json, os, sys
from datetime import datetime, timezone

EXTRACTOR_VERSION = "0.1.0"

# ----- Quy đổi đơn vị database Inventor -> đơn vị schema (tường minh, một chỗ) -----
UNIT_LEN_CM_TO_MM = 10.0        # length DB: cm  -> bbox_mm
UNIT_VOL_DB_TO_CM3 = 1.0        # volume DB: cm³ -> volume_cm3 (giữ nguyên)
UNIT_AREA_DB_TO_CM2 = 1.0       # area DB:   cm² -> area_cm2  (giữ nguyên)
UNIT_MASS_DB_TO_KG = 1.0        # mass DB:   kg  -> est_mass_kg (đối chiếu 1 lần với UI!)

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Danh mục vật liệu + ρ (g/cm³) — PHẢI khớp chuỗi bên thiết kế gõ trong iProperties
# Material (chốt quy ước với bên thiết kế, đưa vào Guides tầng bản vẽ). Đồng bộ với
# DEFAULT_MATERIALS của validate_qtcn_seed.py.
try:
    from validate_qtcn_seed import DEFAULT_MATERIALS, material_entry, norm
except Exception:
    sys.stderr.write("[!] Không import được validate_qtcn_seed.py (cần cùng thư mục)\n")
    sys.exit(3)

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def get_prop(doc, set_name, prop_name):
    """Đọc 1 iProperty, trả None nếu không có (read-only tuyệt đối)."""
    try:
        return doc.PropertySets.Item(set_name).Item(prop_name).Value
    except Exception:
        return None

def read_part(doc, path):
    """Đọc 1 document (.ipt hoặc node .iam) -> dict trường thô theo đơn vị schema."""
    dt = "Design Tracking Properties"
    mass = get_prop(doc, dt, "Mass")
    vol = get_prop(doc, dt, "Volume")
    area = get_prop(doc, dt, "SurfaceArea") or get_prop(doc, dt, "Surface Area")
    density = get_prop(doc, dt, "Density")           # DB: g/cm³
    return {
        "file": path,
        "part_number": get_prop(doc, dt, "Part Number"),
        "description": get_prop(doc, dt, "Description"),
        "material": get_prop(doc, dt, "Material"),
        "stock": get_prop(doc, dt, "Stock Number"),
        "revision": get_prop(doc, "Inventor Summary Information", "Revision Number"),
        "designer": get_prop(doc, dt, "Designer") or get_prop(doc, dt, "Engineer"),
        "mass_kg": (float(mass) * UNIT_MASS_DB_TO_KG) if mass else None,
        "volume_cm3": (float(vol) * UNIT_VOL_DB_TO_CM3) if vol else None,
        "area_cm2": (float(area) * UNIT_AREA_DB_TO_CM2) if area else None,
        "density_g_cm3": float(density) if density else None,
    }

def walk_assembly(app, doc, seen):
    """Duyệt đệ quy AllReferencedDocuments -> list document part DUY NHẤT.
    Apprentice không cho occurrence count -> qty đếm ở mức 'file được tham chiếu'
    (không tin cậy cho chi tiết lặp — xem LƯU Ý đầu file)."""
    parts = []
    try:
        refs = doc.AllReferencedDocuments
    except Exception:
        refs = None
    if not refs:
        return parts
    for i in range(1, refs.Count + 1):
        rd = refs.Item(i)
        p = str(rd.FullFileName)
        if p.lower() in seen:
            continue
        seen.add(p.lower())
        if p.lower().endswith(".ipt"):
            parts.append((rd, p))
    return parts

def main():
    ap = argparse.ArgumentParser(description="Inventor Apprentice (headless) -> qtcn-seed.json")
    ap.add_argument("--file", required=True, help=".ipt hoặc .iam")
    ap.add_argument("--out", default=None)
    ap.add_argument("--name", default="qtcn-seed-apprentice")
    ap.add_argument("--operator", default=None)
    ap.add_argument("--product-name", default=None)
    a = ap.parse_args()

    if not os.path.exists(a.file):
        sys.stderr.write("[!] Không thấy file: %s\n" % a.file); sys.exit(3)
    try:
        import win32com.client
    except ImportError:
        sys.stderr.write("[!] Thiếu pywin32. Cài: pip install pywin32\n"); sys.exit(3)
    appr = None
    # ProgID khác nhau theo bản cài: Inventor 2018 thật đăng ký "Inventor.ApprenticeServer"
    # (xác nhận trên máy Workshop X), tài liệu API ghi "...ServerComponent" — thử cả hai.
    for progid in ("Inventor.ApprenticeServer", "Inventor.ApprenticeServerComponent"):
        try:
            appr = win32com.client.Dispatch(progid)
            break
        except Exception:
            continue
    if appr is None:
        sys.stderr.write("[!] Không khởi tạo được Apprentice Server (thử cả 2 ProgID).\n"
                         "    Máy cần cài Inventor hoặc Inventor View (miễn phí).\n")
        sys.exit(3)

    src = os.path.abspath(a.file)
    doc = appr.Open(src)                      # Apprentice = read-only theo thiết kế
    ext = os.path.splitext(src)[1].lower()

    rows = []
    if ext == ".iam":
        seen = set()
        for rd, p in walk_assembly(appr, doc, seen):
            rows.append(read_part(rd, p))
        qty_source = "unique_refs"            # KHÔNG tin cậy cho chi tiết lặp
    else:
        rows.append(read_part(doc, src))
        qty_source = "single_part"

    # ---- Sensor S1 nhúng (self-check trước khi nộp; bộ đầy đủ: validate_qtcn_seed.py)
    fails, warns = [], []
    seed_bom = []
    for i, r in enumerate(rows, 1):
        w = r["part_number"] or os.path.basename(r["file"])
        ent = material_entry(r["material"], DEFAULT_MATERIALS)
        if not r["material"]:
            fails.append("S1-02 %s: thiếu Material trong iProperties" % w)
        elif ent is None:
            fails.append("S1-02 %s: vật liệu %r ngoài danh mục duyệt" % (w, r["material"]))
        if r["mass_kg"] is not None and r["mass_kg"] <= 0:
            fails.append("S1-07 %s: mass = %r" % (w, r["mass_kg"]))
        rho = r["density_g_cm3"] or (ent["density_g_cm3"] if ent else None)
        if r["mass_kg"] and r["volume_cm3"] and rho:
            m_ref = r["volume_cm3"] * rho / 1000.0
            rel = abs(r["mass_kg"] - m_ref) / r["mass_kg"]
            if rel > 0.02:
                fails.append("S1-01/08 %s: mass=%.4g kg vs V×ρ=%.4g kg (%.0f%%) — "
                             "nghi quy đổi đơn vị/cache cũ" % (w, r["mass_kg"], m_ref, rel * 100))
        if r["mass_kg"] is None:
            warns.append("%s: chưa có Mass cache (Update+Save trong Inventor rồi trích lại)" % w)
        seed_bom.append({
            "vt": "VT%d" % i, "pos": i,
            "drawing_no": r["part_number"], "name": r["description"] or r["part_number"],
            "name_en": None,
            "qty": 1,                          # xem qty_source — QTY thật lấy từ BOM export
            "material": r["material"],
            "specs": {"sections": [], "plate_mm": None,
                      "stock_number": r["stock"], "tolerances": [], "key_dims": [],
                      "est_mass_kg": round(r["mass_kg"], 4) if r["mass_kg"] else None,
                      "volume_cm3": round(r["volume_cm3"], 2) if r["volume_cm3"] else None,
                      "area_cm2": round(r["area_cm2"], 2) if r["area_cm2"] else None,
                      "density_g_cm3": r["density_g_cm3"], "sheets": [],
                      "source_file": r["file"], "revision": r["revision"]},
        })

    seed = {
        "schema": "qtcn-seed/v1",
        "product": {"code": None, "name": a.product_name, "name_en": None, "type": None,
                    "units": "mm", "principal_particulars": {}},
        "source": {
            "kind": "inventor-apprentice",
            "file": src,
            "sha256": sha256_of(src),                         # truy vết (mục 2.1 đặc tả)
            "extractor_version": EXTRACTOR_VERSION,
            "extracted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "operator": a.operator or getpass.getuser(),
            "qty_source": qty_source,
        },
        "bom": seed_bom, "consumables": [], "relationships": [],
        "flags": {
            "validated": not fails,           # Gate G1 sơ bộ — bộ đầy đủ chạy validator
            "mass_source": "inventor-cached-iproperties",
            "qty_reliable": qty_source == "single_part",
            "embedded_sensor_fails": fails, "embedded_sensor_warnings": warns,
        },
        "_note": ("Adapter Apprentice 0.1.0 — CHƯA qua Gate G3 golden set, chưa dùng "
                  "sản xuất. Mass/Volume là cache iProperties lần lưu cuối. QTY=1 mọi "
                  "dòng (Apprentice không có occurrence count) — merge với seed từ "
                  "bom_xlsx_to_seed.py để có QTY thật. Chạy tiếp: "
                  "validate_qtcn_seed.py --seed <file này>."),
    }

    out_dir = a.out or os.path.dirname(src)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, a.name + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

    print("Wrote %s" % out_path)
    print("  parts=%d | qty_source=%s | sha256=%s..." % (len(seed_bom), qty_source,
                                                         seed["source"]["sha256"][:12]))
    for m in fails:
        print("  [FAIL] %s" % m)
    for m in warns:
        print("  [WARN] %s" % m)
    if fails:
        print("  → Gate G1: seed ghi ra nhưng validated=false — pipeline từ chối nhận.")
        sys.exit(2)
    sys.exit(1 if warns else 0)

if __name__ == "__main__":
    main()
