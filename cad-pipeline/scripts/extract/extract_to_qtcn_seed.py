#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_to_qtcn_seed.py — Bridge: mech-drawing-extract JSON  ->  qtcn-seed.json

Lấy đầu ra của skill `mech-drawing-extract` (BOM.json do skill lập + trang-*.json do
parse_mech_drawing.py sinh) và kết xuất **qtcn-seed.json** — nền tảng dữ liệu cho skill
`qtcn` (và pha P2 của `product-dossier`). Gán mã VT tự động, gộp vật liệu/số lượng, rút
specs (tolerances, kích thước, thép hình) theo từng chi tiết.

COD: Offload (biến JSON trích xuất -> seed QTCN là biến đổi tất định, codify Python).

Dùng:
    python cad-pipeline/scripts/extract/extract_to_qtcn_seed.py --extracted <dir> [--out <dir>] [--name <slug>]

`--extracted`  thư mục chứa BOM.json + trang-*.json (thư mục `extracted/` của mech-drawing-extract).
`--out`        nơi ghi qtcn-seed.json (mặc định = --extracted).
`--name`       slug tên file (mặc định 'qtcn-seed').

In một dòng tóm tắt; thoát 0 nếu OK, 2 nếu thiếu BOM.json.
"""
import argparse, glob, json, os, re, sys

SECTION_PATTS = [
    r"L\s*\d+\s*[x×]\s*\d+\s*[x×]\s*\d+",          # L40x40x4
    r"h[ộo]p\s*\d+\s*[x×]\s*\d+\s*[x×]\s*[\d,\.]+", # hộp 30x60x1,8
    r"t[ấa]m\s*[\d,\.]+\s*mm",                      # tấm 15 mm
    r"[ØÐ]\s*\d+",                                  # Ø tube
]

def find_sections(material: str):
    out = []
    for p in SECTION_PATTS:
        for m in re.finditer(p, material or "", flags=re.I):
            s = re.sub(r"\s+", "", m.group(0)).replace("x", "×")
            if s not in out:
                out.append(s)
    return out

def plate_mm(material: str):
    m = re.search(r"t[ấa]m\s*([\d,\.]+)\s*mm", material or "", flags=re.I)
    return m.group(1).replace(",", ".") if m else None

def sheet_to_json(sheet: str, extracted: str):
    """'Trang-4' -> path of trang-4.json (case-insensitive)."""
    base = sheet.strip().lower()
    cand = os.path.join(extracted, base + ".json")
    if os.path.exists(cand):
        return cand
    for f in glob.glob(os.path.join(extracted, "*.json")):
        if os.path.splitext(os.path.basename(f))[0].lower() == base:
            return f
    return None

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def collect_specs(part, extracted):
    """Aggregate tolerances / key dims / flags across a part's sheets."""
    tols, dims = [], []
    tcvn3 = pdf_scanned = mojibake = False
    for sh in part.get("sheets", []):
        p = sheet_to_json(sh, extracted)
        if not p:
            continue
        d = load(p)
        sm = d.get("specs_merged", {})
        for t in sm.get("tolerances", []):
            raw = t.get("raw") or ""
            if raw and raw not in tols:
                tols.append(raw)
        for dim in d.get("dxf", {}).get("dimensions", []):
            t = (dim.get("text") or "").strip()
            if t and t not in dims:
                dims.append(t)
        if d.get("dxf", {}).get("tcvn3", {}).get("detected"):
            tcvn3 = True
        pdfm = d.get("pdf", {})
        if pdfm.get("scanned_no_text_layer"):
            pdf_scanned = True
        if pdfm.get("encoding_warning") or (pdfm.get("mojibake_ratio") or 0) > 0.2:
            mojibake = True
    return tols, dims, dict(tcvn3=tcvn3, pdf_scanned=pdf_scanned, mojibake_pdf=mojibake)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--name", default="qtcn-seed")
    a = ap.parse_args()

    extracted = a.extracted
    out_dir = a.out or extracted
    bom_path = os.path.join(extracted, "BOM.json")
    if not os.path.exists(bom_path):
        sys.stderr.write(
            "[!] Không thấy BOM.json trong %s.\n"
            "    Chạy skill mech-drawing-extract để lập BOM trước (gói nhiều chi tiết),\n"
            "    hoặc trỏ --extracted vào đúng thư mục 'extracted/'.\n" % extracted)
        sys.exit(2)

    bom = load(bom_path)
    assembly_code = bom.get("assembly")
    product = {
        "code": assembly_code,
        "name": bom.get("title"),
        "name_en": bom.get("title_en"),
        "type": bom.get("type"),
        "units": bom.get("units", "mm"),
        "principal_particulars": bom.get("principal_particulars", {}),
    }

    seed_bom, flags_any = [], dict(tcvn3=False, pdf_scanned=False, mojibake_pdf=False)
    vt_n = 0
    for part in bom.get("parts", []):
        is_assembly = (part.get("pos") in (None, "", "—")) or (part.get("drawing_no") == assembly_code)
        tols, dims, flags = collect_specs(part, extracted)
        for k in flags_any:
            flags_any[k] = flags_any[k] or flags[k]
        if is_assembly:
            continue  # bản lắp = sản phẩm, không phải chi tiết chế tạo
        vt_n += 1
        material = part.get("material", "")
        seed_bom.append({
            "vt": "VT%d" % vt_n,
            "pos": part.get("pos"),
            "drawing_no": part.get("drawing_no"),
            "name": part.get("name_vi") or part.get("name"),
            "name_en": part.get("name_en"),
            "qty": part.get("qty"),
            "material": material,
            "specs": {
                "sections": find_sections(material),
                "plate_mm": plate_mm(material),
                "tolerances": tols,
                "key_dims": dims[:12],
                "est_mass_kg": None,          # bản vẽ scale -> cần bóc tách/cân
                "sheets": part.get("sheets", []),
            },
        })

    consumables = [
        {"name": it.get("name"), "qty": it.get("qty"), "note": it.get("note")}
        for it in bom.get("purchased_standard_items", [])
    ]

    seed = {
        "schema": "qtcn-seed/v1",
        "product": product,
        "source": {
            "extracted_dir": os.path.abspath(extracted),
            "bom_json": os.path.abspath(bom_path),
            "sheets_n": len(glob.glob(os.path.join(extracted, "trang-*.json")))
                        or len(glob.glob(os.path.join(extracted, "*.json"))),
        },
        "bom": seed_bom,
        "consumables": consumables,
        "relationships": [],   # STUB — skill qtcn điền mối ghép (bu lông/hàn/cáp) ở Bước 2
        "flags": flags_any,
        "_note": "Nền tảng cho skill qtcn. VT gán tự động theo thứ tự bảng kê; "
                 "relationships để trống — qtcn suy ra mối ghép từ bản vẽ bố trí. "
                 "est_mass_kg=None vì bản vẽ ở tỷ lệ scale (cần bóc tách khối lượng).",
    }

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, a.name + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(seed, f, ensure_ascii=False, indent=2)

    print("Wrote %s" % out_path)
    print("  product=%s | parts(VT)=%d | consumables=%d | flags=%s"
          % (product.get("code"), len(seed_bom), len(consumables),
             ",".join(k for k, v in flags_any.items() if v) or "none"))

if __name__ == "__main__":
    main()
