#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drawing_check.py — Script thẩm định bản vẽ đầu vào, LỚP D1 + D5 (WX-QT-DRAWING-SENSOR-01)

Sensor tầng 1 (bản vẽ) — chạy TRƯỚC tầng trích xuất. Đọc .ipt/.iam qua Apprentice
Server (read-only, không mở Inventor UI, máy chỉ cần Inventor/Inventor View) và kiểm:

  D1-01 Part Number có (+ đúng quy ước nếu truyền --pn-regex; lệch tên file → WARNING)
  D1-02 Material đã gán (≠ Generic/Default/rỗng) và thuộc danh mục duyệt
  D1-03 Revision có          D1-04 Designer có (W)        D1-05 Description có (W)
  D1-06 Mass cache có và ≈ V×ρ(material) ±2%
  D1-08 Thép hình/tấm phải có Stock Number (W)
  D1-09 Part phi-chế-tạo (Skeleton/KT/Mẫu/Khuôn) phải BOM Structure = Reference/Phantom
  D1-10 iProperty WX_PartType có và hợp lệ {WA,WS,MC,SM,CP,HU,AS,STD}
  SEC-01 iProperty WX_Classification có, thuộc {THUONG,NOIBO,MAT}
  (D1-07 đơn vị, D1-11 BOM view, D2/D3: cần Inventor sống/DXF — ngoài phạm vi script này)

Xuất:  <out>/drawing_report.json  (= biểu mẫu WX-QT-DRAWING-F01)
       <out>/giao-viec.csv        (--ticket: phiếu giao việc cho bên thiết kế, mở Excel)
Exit:  0 PASS · 1 chỉ WARNING · 2 có FAIL (không cấp Released) · 3 thiếu môi trường

Dùng:
    python drawing_check.py --file "D:\\...\\Tong lap.iam" [--out <dir>] [--ticket]
        [--pn-regex "^BM01\\.\\d{2}\\.\\d{2}"] [--materials materials.json]
"""
import argparse, csv, json, os, re, sys
from datetime import datetime, timezone

VERSION = "0.1.0"

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)
from validate_qtcn_seed import DEFAULT_MATERIALS, material_entry, norm          # noqa: E402
from inventor_apprentice_extract import get_prop, walk_assembly, sha256_of      # noqa: E402

PART_TYPES = {"WA", "WS", "MC", "SM", "CP", "HU", "AS", "STD"}
CLASSIFICATIONS = {"THUONG", "NOIBO", "MAT"}
BAD_MATERIALS = {"", "generic", "default", "material", "<generic>", "none"}
# tên gợi ý part phi-chế-tạo (D1-09) và thép hình/tấm (D1-08)
NON_MFG_PAT = re.compile(r"skeleton|^kt\b|^kt |^mau |khuon|master|khung xuong", re.I)
PROFILE_PAT = re.compile(r"\bL\s*\d+\s*x\s*\d+|h[ộo]p\s*\d+|t[ấa]m\s*\d|ISO |JIS |^U\d|thep hinh", re.I)
REFERENCE_STRUCTS = {"reference", "phantom", "5", "4"}   # chuỗi hoặc enum thô từ iProperty

def user_prop(doc, name):
    """iProperty tự định nghĩa (Inventor User Defined Properties)."""
    return get_prop(doc, "Inventor User Defined Properties", name)

def check_part(doc, path, catalog, pn_regex, rows, rpt_add):
    dt = "Design Tracking Properties"
    fname = os.path.splitext(os.path.basename(path))[0]
    pn = (get_prop(doc, dt, "Part Number") or "").strip()
    w = pn or fname
    need = []   # mục cho phiếu giao việc

    # --- D1-01 Part Number
    if not pn:
        rpt_add("D1-01", "FAIL", w, "thiếu Part Number"); need.append("Part Number")
    else:
        if pn_regex and not re.match(pn_regex, pn):
            rpt_add("D1-01", "FAIL", w, "Part Number %r sai quy ước %r" % (pn, pn_regex))
            need.append("PN đúng quy ước")
        if norm(pn) != norm(fname):
            rpt_add("D1-01", "WARNING", w, "Part Number %r ≠ tên file %r" % (pn, fname))

    # --- D1-02 Material
    mat = (get_prop(doc, dt, "Material") or "").strip()
    ent = material_entry(mat, catalog)
    if mat.lower() in BAD_MATERIALS:
        rpt_add("D1-02", "FAIL", w, "vật liệu chưa gán (%r)" % (mat or "rỗng"))
        need.append("gán Material từ thư viện")
    elif ent is None:
        rpt_add("D1-02", "FAIL", w, "vật liệu %r ngoài danh mục duyệt" % mat)
        need.append("Material thuộc danh mục")

    # --- D1-03/04/05
    rev = (get_prop(doc, "Inventor Summary Information", "Revision Number") or "").strip()
    if not rev:
        rpt_add("D1-03", "FAIL", w, "thiếu Revision"); need.append("Revision")
    designer = (get_prop(doc, dt, "Designer") or get_prop(doc, dt, "Engineer") or "").strip()
    if not designer:
        rpt_add("D1-04", "WARNING", w, "thiếu Designer/Engineer")
    desc = (get_prop(doc, dt, "Description") or "").strip()
    if not desc:
        rpt_add("D1-05", "WARNING", w, "thiếu Description (tên gọi)")

    # --- D1-06 Mass cache + khớp V×ρ
    mass = get_prop(doc, dt, "Mass")
    vol = get_prop(doc, dt, "Volume")
    try:
        mass = float(mass) if mass not in (None, "") else None
        vol = float(vol) if vol not in (None, "") else None
    except Exception:
        mass = vol = None
    if not mass:
        rpt_add("D1-06", "FAIL", w, "chưa có mass cache (Update mass + Save trong Inventor)")
        need.append("Update mass + Save")
    elif vol and ent:
        m_ref = vol * ent["density_g_cm3"] / 1000.0    # Volume DB cm³, mass kg
        rel = abs(mass - m_ref) / mass if mass else 1
        if rel > 0.02:
            rpt_add("D1-06", "FAIL", w, "mass cache %.4g kg lệch V×ρ(%s)=%.4g kg (%.0f%%) — cache cũ hoặc ρ sai"
                    % (mass, mat, m_ref, rel * 100))
            need.append("Update mass (cache lệch)")

    # --- D1-08 quy cách phôi cho thép hình/tấm
    stock = (get_prop(doc, dt, "Stock Number") or "").strip()
    if not stock and (PROFILE_PAT.search(fname) or PROFILE_PAT.search(desc or "")):
        rpt_add("D1-08", "WARNING", w, "thép hình/tấm nhưng thiếu Stock Number (quy cách phôi)")

    # --- D1-09 part phi-chế-tạo phải Reference/Phantom
    bom_struct = str(get_prop(doc, dt, "BOM Structure") or "").strip().lower()
    if NON_MFG_PAT.search(fname) or NON_MFG_PAT.search(desc or ""):
        if bom_struct not in REFERENCE_STRUCTS:
            rpt_add("D1-09", "FAIL", w, "part phi-chế-tạo (skeleton/KT/mẫu) nhưng BOM Structure=%r — phải Reference/Phantom"
                    % (bom_struct or "Normal"))
            need.append("BOM Structure=Reference")

    # --- D1-10 WX_PartType
    ptype = (user_prop(doc, "WX_PartType") or "").strip().upper()
    if ptype not in PART_TYPES:
        rpt_add("D1-10", "FAIL", w, "thiếu/sai WX_PartType (%r) — cần một trong %s"
                % (ptype or "rỗng", "/".join(sorted(PART_TYPES))))
        need.append("WX_PartType")

    # --- SEC-01 phân loại mật
    cls = (user_prop(doc, "WX_Classification") or "").strip().upper()
    if cls not in CLASSIFICATIONS:
        rpt_add("SEC-01", "FAIL", w, "thiếu/sai WX_Classification (%r)" % (cls or "rỗng"))
        need.append("WX_Classification")

    rows.append({"file": os.path.basename(path), "part_number": pn, "description": desc,
                 "material": mat, "revision": rev, "wx_parttype": ptype,
                 "can_bo_sung": "; ".join(dict.fromkeys(need)) or "ĐẠT D1"})

def main():
    ap = argparse.ArgumentParser(description="Thẩm định bản vẽ lớp D1+SEC (WX-QT-DRAWING-SENSOR-01)")
    ap.add_argument("--file", required=True, help=".ipt hoặc .iam")
    ap.add_argument("--out", default=None)
    ap.add_argument("--pn-regex", default=None, help="regex quy ước Part Number (thiếu = chỉ kiểm không rỗng)")
    ap.add_argument("--materials", default=None, help="JSON danh mục vật liệu duyệt")
    ap.add_argument("--ticket", action="store_true", help="xuất giao-viec.csv cho bên thiết kế")
    a = ap.parse_args()

    if not os.path.exists(a.file):
        sys.stderr.write("[!] Không thấy file: %s\n" % a.file); sys.exit(3)
    try:
        import win32com.client
    except ImportError:
        sys.stderr.write("[!] Thiếu pywin32. Cài: pip install pywin32\n"); sys.exit(3)
    appr = None
    for progid in ("Inventor.ApprenticeServer", "Inventor.ApprenticeServerComponent"):
        try:
            appr = win32com.client.Dispatch(progid); break
        except Exception:
            continue
    if appr is None:
        sys.stderr.write("[!] Không khởi tạo được Apprentice (cần Inventor/Inventor View).\n"); sys.exit(3)

    catalog = DEFAULT_MATERIALS
    if a.materials:
        with open(a.materials, encoding="utf-8-sig") as f:
            catalog = json.load(f)

    src = os.path.abspath(a.file)
    doc = appr.Open(src)
    entries, rows = [], []
    def rpt_add(rule, level, where, msg):
        entries.append({"rule": rule, "level": level, "where": where, "msg": msg})

    if src.lower().endswith(".iam"):
        for rd, p in walk_assembly(appr, doc, set()):
            check_part(rd, p, catalog, a.pn_regex, rows, rpt_add)
        rpt_add("D1-11", "INFO", os.path.basename(src),
                "BOM view / D2-04 interference / D3 bản vẽ: cần Inventor sống (iLogic) — ngoài phạm vi Apprentice")
    else:
        check_part(doc, src, catalog, a.pn_regex, rows, rpt_add)

    n_fail = sum(1 for e in entries if e["level"] == "FAIL")
    n_warn = sum(1 for e in entries if e["level"] == "WARNING")
    verdict = "FAIL" if n_fail else ("WARNING" if n_warn else "PASS")

    out_dir = a.out or os.path.dirname(src)
    os.makedirs(out_dir, exist_ok=True)
    rep_path = os.path.join(out_dir, "drawing_report.json")
    with open(rep_path, "w", encoding="utf-8") as f:
        json.dump({"form": "WX-QT-DRAWING-F01", "checker_version": VERSION,
                   "source": {"file": src, "sha256": sha256_of(src),
                              "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                   "verdict": verdict, "released_allowed": verdict != "FAIL",
                   "counts": {"FAIL": n_fail, "WARNING": n_warn, "parts": len(rows)},
                   "rules": entries, "parts": rows}, f, ensure_ascii=False, indent=2)

    if a.ticket:
        tick_path = os.path.join(out_dir, "giao-viec.csv")
        with open(tick_path, "w", encoding="utf-8-sig", newline="") as f:   # BOM cho Excel
            wcsv = csv.DictWriter(f, fieldnames=["file", "part_number", "description",
                                                 "material", "revision", "wx_parttype", "can_bo_sung"])
            wcsv.writeheader(); wcsv.writerows(rows)
        print("Wrote %s (phiếu giao việc — mở bằng Excel)" % tick_path)

    # --- tóm tắt console: gộp theo rule cho đỡ ngợp ---
    print("Wrote %s" % rep_path)
    print("VERDICT: %s  (FAIL=%d WARNING=%d | %d part)" % (verdict, n_fail, n_warn, len(rows)))
    agg = {}
    for e in entries:
        if e["level"] in ("FAIL", "WARNING"):
            agg.setdefault((e["rule"], e["level"]), []).append(e["where"])
    for (rule, lv), names in sorted(agg.items()):
        sample = ", ".join(names[:3]) + ("…" if len(names) > 3 else "")
        print("  [%s] %s × %d — vd: %s" % (lv, rule, len(names), sample))
    if verdict == "FAIL":
        print("  → Gate 1 CHẶN: không cấp trạng thái Released. Xem giao-viec.csv để bổ sung.")
    sys.exit({"PASS": 0, "WARNING": 1, "FAIL": 2}[verdict])

if __name__ == "__main__":
    main()
