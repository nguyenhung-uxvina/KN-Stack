#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bom_xlsx_to_seed.py — Bridge: Inventor BOM export (.xlsx/.csv)  ->  qtcn-seed.json

Biến bảng kê vật tư (BOM) do **Autodesk Inventor xuất thẳng** từ file lắp (.iam)
thành **qtcn-seed.json** — CÙNG schema `qtcn-seed/v1` như extract_to_qtcn_seed.py,
nhưng đây là **nguồn vàng**: Part Number = mã bản vẽ THẬT, QTY = số lượng lắp THẬT,
Material = vật liệu THẬT, và **Mass = khối lượng do Inventor tính** (est_mass_kg != None).

⇒ Xoá 3 sai số lớn nhất khi suy từ STEP/bản vẽ:
   • khối lượng phải đoán ρ theo tên  → lấy thẳng cột Mass
   • SL lệch (STEP chỉ 1 instance)     → lấy thẳng cột QTY của BOM lắp
   • drawing_no = null ở seed 3D       → chính là cột Part Number

COD: Offload (biến BOM.xlsx -> seed QTCN là biến đổi tất định, codify Python).

Dùng:
    python scripts/extract/bom_xlsx_to_seed.py --bom <BOM.xlsx|BOM.csv> [--out <dir>]
        [--name qtcn-seed-inventor] [--mass-unit kg|g] [--sheet <ten_sheet>]
        [--assembly-code <ma>] [--product-name <ten>] [--include-subassemblies]

Auto-nhận cột theo tên tiêu đề (chịu được biến thể Anh/Việt). Xuất qtcn-seed/v1.
In một dòng tóm tắt; thoát 0 nếu OK, 2 nếu không nhận được cột bắt buộc, 3 nếu thiếu openpyxl.

⚙️  Cấu hình Inventor cần có (BOM Export → chọn các cột):
    Part Number · Description · QTY · Material · Mass · Stock Number
    (+ tùy chọn: Item/STT, BOM Structure). Đặt đơn vị Mass rõ ràng (kg hoặc g).
"""
import argparse, csv, json, os, re, sys

# Console Windows mặc định cp1252 -> ép UTF-8 để in tiếng Việt / ký hiệu không vỡ
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# --- Dùng lại logic rút thép hình / bề dày tấm từ script seed 2D (giữ nhất quán) ---
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)
try:
    from extract_to_qtcn_seed import find_sections, plate_mm
except Exception:  # fallback nội tuyến nếu chạy lẻ
    _SP = [r"L\s*\d+\s*[x×]\s*\d+\s*[x×]\s*\d+", r"h[ộo]p\s*\d+\s*[x×]\s*\d+\s*[x×]\s*[\d,\.]+",
           r"t[ấa]m\s*[\d,\.]+\s*mm", r"[ØÐ]\s*\d+"]
    def find_sections(material):
        out = []
        for p in _SP:
            for m in re.finditer(p, material or "", flags=re.I):
                s = re.sub(r"\s+", "", m.group(0)).replace("x", "×")
                if s not in out: out.append(s)
        return out
    def plate_mm(material):
        m = re.search(r"t[ấa]m\s*([\d,\.]+)\s*mm", material or "", flags=re.I)
        return m.group(1).replace(",", ".") if m else None

# --- Bản đồ tiêu đề cột: khoá chuẩn -> các biến thể (đã bỏ dấu, thường hoá) ---
COLMAP = {
    "drawing_no": ["part number", "partnumber", "part no", "ma ban ve", "ma bv", "ma so", "part_number", "so hieu"],
    "name":       ["description", "ten goi", "ten chi tiet", "ten", "part name", "mo ta", "ten_goi"],
    "qty":        ["qty", "quantity", "sl", "so luong", "so_luong", "item qty"],
    "material":   ["material", "vat lieu", "vatlieu", "material name"],
    "mass":       ["mass", "khoi luong", "weight", "trong luong", "mass (kg)", "mass (g)", "khoi_luong"],
    "stock":      ["stock number", "stock no", "quy cach", "section", "stocknumber", "kich thuoc phoi", "phoi"],
    "pos":        ["item", "stt", "pos", "vi tri", "no", "tt"],
    "structure":  ["bom structure", "structure", "ket cau", "loai", "type"],
}

def strip_accents(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn")

def norm(s):
    return re.sub(r"\s+", " ", strip_accents(str(s or "")).lower()).strip()

def build_col_index(header):
    """header: list[str] -> {khoá chuẩn: chỉ số cột}. Khớp chính xác trước, rồi chứa-substring."""
    hnorm = [norm(h) for h in header]
    idx = {}
    for key, variants in COLMAP.items():
        found = None
        for v in variants:                       # khớp bằng nhau trước
            if v in hnorm:
                found = hnorm.index(v); break
        if found is None:                         # rồi khớp chứa
            for i, h in enumerate(hnorm):
                if h and any(v in h for v in variants):
                    found = i; break
        if found is not None:
            idx[key] = found
    return idx

def read_xlsx(path, sheet=None):
    try:
        import openpyxl
    except ImportError:
        sys.stderr.write("[!] Thiếu openpyxl. Cài: pip install openpyxl\n"); sys.exit(3)
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb[sheet] if sheet else wb.active
    rows = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    wb.close()
    return rows

def read_csv(path):
    # thử vài encoding hay gặp khi Inventor/Excel xuất CSV
    for enc in ("utf-8-sig", "utf-8", "cp1258", "latin-1"):
        try:
            with open(path, encoding=enc, newline="") as f:
                return [row for row in csv.reader(f)]
        except UnicodeDecodeError:
            continue
    with open(path, encoding="utf-8", errors="replace", newline="") as f:
        return [row for row in csv.reader(f)]

def find_header_row(rows):
    """Dòng tiêu đề = dòng đầu tiên mà build_col_index nhận được cả drawing_no|name và qty."""
    for i, r in enumerate(rows[:25]):
        cells = [str(c) if c is not None else "" for c in r]
        idx = build_col_index(cells)
        if ("qty" in idx) and (("drawing_no" in idx) or ("name" in idx)):
            return i, idx
    return None, None

def to_float(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip()
    s = re.sub(r"(kg|g|gam|gram|gm|lb)\b", "", s, flags=re.I).strip()
    s = s.replace(",", ".")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None

def to_int_qty(v):
    f = to_float(v)
    if f is None: return None
    return int(round(f)) if abs(f - round(f)) < 1e-6 else f

def is_assembly_row(structure_val, material_val):
    st = norm(structure_val)
    if st in ("assembly", "phantom", "lap", "cum", "sub-assembly", "subassembly", "reference"):
        return True
    # heuristic: không có vật liệu + có cấu trúc lắp
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bom", required=True, help="BOM Inventor xuất: .xlsx hoặc .csv")
    ap.add_argument("--out", default=None)
    ap.add_argument("--name", default="qtcn-seed-inventor")
    ap.add_argument("--sheet", default=None, help="Tên sheet trong xlsx (mặc định sheet active)")
    ap.add_argument("--mass-unit", default="auto", choices=["auto", "kg", "g"],
                    help="Đơn vị cột Mass. 'auto': đoán theo tiêu đề (kg)/(g), mặc định kg.")
    ap.add_argument("--assembly-code", default=None, help="Mã sản phẩm (nếu BOM không có)")
    ap.add_argument("--product-name", default=None)
    ap.add_argument("--include-subassemblies", action="store_true",
                    help="Giữ cả dòng cụm lắp (mặc định bỏ, chỉ giữ chi tiết chế tạo)")
    a = ap.parse_args()

    ext = os.path.splitext(a.bom)[1].lower()
    if ext in (".xlsx", ".xlsm"):
        rows = read_xlsx(a.bom, a.sheet)
    elif ext in (".csv", ".txt"):
        rows = read_csv(a.bom)
    else:
        sys.stderr.write("[!] Chỉ nhận .xlsx hoặc .csv. Trong Inventor: BOM → Export → Excel/CSV.\n")
        sys.exit(2)

    hrow, idx = find_header_row(rows)
    if hrow is None:
        sys.stderr.write(
            "[!] Không nhận ra dòng tiêu đề BOM. Cần tối thiểu cột QTY và (Part Number hoặc Description).\n"
            "    Trong Inventor: Assemble → Bill of Materials → cấu hình cột rồi Export.\n"
            "    Cột nên có: Part Number · Description · QTY · Material · Mass · Stock Number.\n")
        sys.exit(2)

    header = [str(c) if c is not None else "" for c in rows[hrow]]
    # đơn vị khối lượng
    mass_unit = a.mass_unit
    if mass_unit == "auto":
        mh = norm(header[idx["mass"]]) if "mass" in idx else ""
        mass_unit = "g" if re.search(r"\(g\)|gam|gram|\bg\b", mh) else "kg"

    def cell(r, key):
        i = idx.get(key)
        if i is None or i >= len(r): return None
        v = r[i]
        return v

    seed_bom, vt_n = [], 0
    total_mass, n_mass, n_skip_asm = 0.0, 0, 0
    for r in rows[hrow + 1:]:
        if r is None: continue
        cells = list(r)
        dno = cell(cells, "drawing_no"); nm = cell(cells, "name")
        qty = cell(cells, "qty")
        if (dno in (None, "")) and (nm in (None, "")):  # dòng trống
            continue
        if qty in (None, ""):                            # không có SL -> bỏ (dòng tiêu đề phụ/ghi chú)
            continue
        structure = cell(cells, "structure")
        material = str(cell(cells, "material") or "").strip()
        if (not a.include_subassemblies) and is_assembly_row(structure, material):
            n_skip_asm += 1; continue

        mass_raw = to_float(cell(cells, "mass"))
        est_mass_kg = None
        if mass_raw is not None:
            est_mass_kg = round(mass_raw / 1000.0, 4) if mass_unit == "g" else round(mass_raw, 4)
            total_mass += est_mass_kg; n_mass += 1

        stock = str(cell(cells, "stock") or "").strip()
        sect_src = " ".join(x for x in (material, stock) if x)   # thép hình có thể ở cột Stock

        vt_n += 1
        seed_bom.append({
            "vt": "VT%d" % vt_n,
            "pos": (str(cell(cells, "pos")).strip() if cell(cells, "pos") not in (None, "") else None),
            "drawing_no": (str(dno).strip() if dno not in (None, "") else None),
            "name": (str(nm).strip() if nm not in (None, "") else None),
            "name_en": None,
            "qty": to_int_qty(qty),
            "material": material or None,
            "specs": {
                "sections": find_sections(sect_src),
                "plate_mm": plate_mm(sect_src),
                "stock_number": stock or None,
                "tolerances": [],          # BOM không mang dung sai -> lấy từ DXF (mech-drawing-extract)
                "key_dims": [],            # nt
                "est_mass_kg": est_mass_kg,  # ⭐ THẬT từ Inventor (không đoán ρ)
                "sheets": [],
            },
        })

    if not seed_bom:
        sys.stderr.write("[!] Nhận được tiêu đề nhưng 0 dòng chi tiết hợp lệ. Kiểm tra lại cột QTY.\n")
        sys.exit(2)

    product = {
        "code": a.assembly_code,
        "name": a.product_name,
        "name_en": None,
        "type": None,
        "units": "mm",
        "principal_particulars": {},
    }

    seed = {
        "schema": "qtcn-seed/v1",
        "product": product,
        "source": {
            "kind": "inventor-bom-export",
            "bom_file": os.path.abspath(a.bom),
            "header_row": hrow,
            "columns_mapped": {k: header[v] for k, v in idx.items()},
            "mass_unit_in": mass_unit,
        },
        "bom": seed_bom,
        "consumables": [],       # BOM lắp thường không có vật tư phụ -> qtcn bổ sung
        "relationships": [],     # STUB — qtcn suy ra mối ghép ở Bước 2
        "flags": {
            "mass_source": "inventor" if n_mass else "missing",
            "mass_complete": (n_mass == len(seed_bom)),
            "material_complete": all(p["material"] for p in seed_bom),
            "drawing_no_complete": all(p["drawing_no"] for p in seed_bom),
        },
        "_note": ("Nguồn VÀNG: BOM do Inventor xuất. est_mass_kg lấy thẳng cột Mass "
                  "(không đoán khối lượng riêng). QTY = số lượng lắp thật, khắc phục lệch "
                  "so với STEP (1 instance). drawing_no = Part Number. "
                  "Dung sai/GD&T KHÔNG có trong BOM — ghép thêm từ seed 2D (DXF) qua "
                  "merge_qtcn_seeds.py nếu cần."),
    }

    out_dir = a.out or os.path.dirname(os.path.abspath(a.bom))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, a.name + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

    print("Wrote %s" % out_path)
    print("  parts(VT)=%d | có Mass=%d/%d (Σ=%.3f kg) | bỏ cụm lắp=%d | mass_unit=%s"
          % (len(seed_bom), n_mass, len(seed_bom), total_mass, n_skip_asm, mass_unit))
    miss = [k for k, v in seed["flags"].items() if k.endswith("_complete") and not v]
    if miss:
        print("  ⚠ chưa đủ: %s — bổ sung trong Inventor rồi xuất lại." % ", ".join(miss))

if __name__ == "__main__":
    main()
