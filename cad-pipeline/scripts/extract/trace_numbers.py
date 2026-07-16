#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
trace_numbers.py — Truy vết SỐ trong tài liệu AI sinh về qtcn-seed (harness tầng 3)

Rule cốt lõi (đặc tả WX-QT-EXTRACT-SENSOR-01 §7 — "sensor áp nguyên vẹn cho đầu ra
AI"): **mọi giá trị số KÈM ĐƠN VỊ trong tài liệu do AI sinh (QTCN, định mức, dự toán,
biên bản) phải truy được về một trường trong seed, một biến đổi đơn vị của nó
(×1000/÷1000), một tích với số lượng, hoặc một hằng số kỹ thuật khai báo.**
Số mồ côi (orphan) = dấu hiệu AI bịa số → FAIL, tài liệu không được phát hành.

Dùng (chạy sau khi AI sinh bản nháp, trước khi trình duyệt):
    python cad-pipeline/scripts/extract/trace_numbers.py --doc <bao-cao.md|.txt>
        --seed <qtcn-seed-final.json> [--seed <seed-khác.json> ...]
        [--constants <json>] [--tol-pct 0.5] [--report <path>]

Chỉ truy số CÓ ĐƠN VỊ (kg, mm, m, %, giờ, cái…) — số trần (mục lục, mã hiệu, số
thứ tự) bỏ qua có chủ đích. Hiểu định dạng số Việt: "1.020.575,22" / "408,065" /
"38.633" (nhập nhằng chấm nghìn/thập phân → thử cả hai cách đọc).

Exit: 0 = 100%% truy được · 2 = có số mồ côi (chặn phát hành) · 3 = lỗi dùng.
Nối với skill /qc và /aigate: bước kiểm máy chạy TRƯỚC khi người duyệt đọc.
"""
import argparse, json, os, re, sys

VERSION = "0.1.0"
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Đơn vị được truy vết (kèm biến thể ²³ và tiếng Việt). Nhóm quy đổi về "đơn vị seed".
UNITS = r"(?:kg|g|t[ấa]n|mm[²2]|cm[²2]|m[²2]|mm[³3]|cm[³3]|m[³3]|mm|cm|dm|m|%|gi[ờo]|h|kW|c[áa]i|chi[ếe]c|b[ộo]|ng[ườuoi]+)"
NUM_UNIT_RE = re.compile(r"(?<![\w./-])(\d[\d.,]*)\s*(" + UNITS + r")(?![\w²³])", re.IGNORECASE)

# Hằng số kỹ thuật được phép xuất hiện mà không cần có trong seed (khai báo tường minh)
DEFAULT_CONSTANTS = [7.85, 2.70, 2.66, 1.70, 0.55, 7.93, 1.025, 1.5, 2.0, 9.81, 100.0]

def parse_vn_number(tok):
    """'1.020.575,22'→[1020575.22]; '38,633'→[38.633]; '408.065'→[408.065, 408065] (nhập nhằng)."""
    tok = tok.strip().rstrip(".,")
    if "," in tok and "." in tok:                       # chấm nghìn + phẩy thập phân
        return [float(tok.replace(".", "").replace(",", "."))]
    if "," in tok:                                      # phẩy = thập phân (chuẩn VN)
        return [float(tok.replace(",", "."))]
    if tok.count(".") == 1:                             # 1 chấm: thập phân HAY nghìn -> cả hai
        a = float(tok)
        b = float(tok.replace(".", ""))
        return [a] if a == b else [a, b]
    if tok.count(".") > 1:                              # nhiều chấm = chấm nghìn
        return [float(tok.replace(".", ""))]
    return [float(tok)]

def dim_of_path(p):
    """Thứ nguyên của trường seed theo TÊN (đơn vị nằm trong tên trường — Guides §2.1).
    None = loại khỏi vũ trụ (pos/score/threshold… khớp vào chỉ gây dương tính giả)."""
    pl = p.lower()
    last = pl.rsplit(".", 1)[-1]
    if "score" in last or "threshold" in last or last == "pos" or "header" in last:
        return None
    if "mass" in pl:
        return "mass"
    if "_cm3" in pl:
        return "vol"
    if "_cm2" in pl:
        return "area"
    if "_mm" in pl:                       # bbox_mm.x, envelope_mm.L, plate_mm, *_mm
        return "len"
    if last == "qty" or last.startswith("qty"):
        return "count"
    return "other"                        # trường số khác — không cho đơn vị vật lý khớp bừa

def walk(obj, path, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, "%s.%s" % (path, k), out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, "%s[%d]" % (path, i), out)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if obj != 0:
            d = dim_of_path(path)
            if d:
                out.append((float(obj), path, d))

# Quy đổi GIÁ TRỊ TRONG TÀI LIỆU về đơn vị gốc của seed (kg / mm / cm³ / cm²)
# theo ĐÚNG đơn vị đi kèm số — không nhân hệ số mù quáng (bài học test đầu:
# vũ trụ ×10/÷10 vô tội vạ làm số bịa 43,9 kg khớp nhầm và lọt lưới).
UNIT_FACTORS = {
    "kg": [1.0], "g": [0.001], "tan": [1000.0],
    "mm": [1.0], "cm": [10.0], "dm": [100.0], "m": [1000.0],
    "mm2": [0.01], "cm2": [1.0], "m2": [10000.0],          # → cm²
    "mm3": [0.001], "cm3": [1.0], "m3": [1e6],             # → cm³
}
NO_SHIFT = [1.0]   # %, cái, giờ, kW… so trực tiếp

def unit_key(u):
    import unicodedata
    u = "".join(c for c in unicodedata.normalize("NFD", u.lower())
                if unicodedata.category(c) != "Mn")
    u = u.replace("²", "2").replace("³", "3")
    return u

def factors_for(unit):
    return UNIT_FACTORS.get(unit_key(unit), NO_SHIFT)

# Đơn vị trong tài liệu → thứ nguyên seed được phép khớp ("const" = hằng số khai báo).
# Bài học test: "43,9 kg" từng khớp bom[12].qty=44 (0,23%) — kg mà so với SỐ LƯỢNG.
UNIT_DIMS = {
    "kg": {"mass", "const"}, "g": {"mass", "const"}, "tan": {"mass", "const"},
    "mm": {"len", "const"}, "cm": {"len", "const"}, "dm": {"len", "const"}, "m": {"len", "const"},
    "mm2": {"area", "const"}, "cm2": {"area", "const"}, "m2": {"area", "const"},
    "mm3": {"vol", "const"}, "cm3": {"vol", "const"}, "m3": {"vol", "const"},
}
COUNT_UNITS = {"cai", "chiec", "bo", "nguoi"}

def dims_for(unit):
    k = unit_key(unit)
    if k in UNIT_DIMS:
        return UNIT_DIMS[k]
    if k in COUNT_UNITS:
        return {"count"}
    return {"const"}                      # %, giờ, kW… chỉ được khớp hằng số khai báo

def build_universe(seed_paths, constants):
    """(giá trị, nguồn): giá trị GỐC trong seed + tích qty×est_mass + hằng số khai báo.
    Không sinh biến thể nhân/chia — quy đổi làm ở phía số-trong-tài-liệu theo đơn vị."""
    uni = []
    for sp in seed_paths:
        with open(sp, encoding="utf-8-sig") as f:
            seed = json.load(f)
        tag = os.path.basename(sp)
        vals = []
        walk(seed, tag, vals)
        uni.extend(vals)
        # tích khối lượng đơn × số lượng (dòng "44 cái × 0,385 kg = 16,94 kg")
        for part in seed.get("bom", []) or []:
            q = part.get("qty")
            m = (part.get("specs") or {}).get("est_mass_kg")
            if isinstance(q, (int, float)) and isinstance(m, (int, float)):
                uni.append((q * m, "%s/%s qty×est_mass" % (tag, part.get("name")), "mass"))
    for c in constants:
        uni.append((float(c), "hằng số kỹ thuật khai báo", "const"))
    return uni

def match(value, universe, allowed_dims, tol_pct, tol_abs=0.005):
    best = None
    for s, src, dim in universe:
        if dim not in allowed_dims:
            continue
        tol = max(abs(s) * tol_pct / 100.0, tol_abs)
        d = abs(value - s)
        if d <= tol and (best is None or d < best[0]):
            best = (d, s, src)
    return best

def main():
    ap = argparse.ArgumentParser(description="Truy vết số tài liệu AI sinh về qtcn-seed")
    ap.add_argument("--doc", required=True, help="tài liệu .md/.txt cần kiểm")
    ap.add_argument("--seed", action="append", required=True, help="seed nguồn (lặp lại được)")
    ap.add_argument("--constants", default=None, help="JSON list hằng số kỹ thuật được phép")
    ap.add_argument("--tol-pct", type=float, default=0.5)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    if not os.path.exists(a.doc):
        sys.stderr.write("[!] Không thấy tài liệu: %s\n" % a.doc); sys.exit(3)
    constants = DEFAULT_CONSTANTS
    if a.constants:
        with open(a.constants, encoding="utf-8-sig") as f:
            constants = json.load(f)
    universe = build_universe(a.seed, constants)

    with open(a.doc, encoding="utf-8-sig") as f:
        lines = f.readlines()
    findings, n_ok = [], 0
    for ln, line in enumerate(lines, 1):
        for mo in NUM_UNIT_RE.finditer(line):
            tok, unit = mo.group(1), mo.group(2)
            cands = parse_vn_number(tok)
            hit = None
            dims = dims_for(unit)
            for v in cands:
                for k in factors_for(unit):        # quy đổi theo ĐƠN VỊ của số trong doc
                    hit = match(v * k, universe, dims, a.tol_pct)
                    if hit:
                        break
                if hit:
                    break
            if hit:
                n_ok += 1
                findings.append({"line": ln, "text": "%s %s" % (tok, unit), "status": "TRACED",
                                 "source": hit[2], "seed_value": hit[1]})
            else:
                findings.append({"line": ln, "text": "%s %s" % (tok, unit), "status": "ORPHAN",
                                 "context": line.strip()[:90]})
    orphans = [f0 for f0 in findings if f0["status"] == "ORPHAN"]

    rep_path = a.report or (os.path.splitext(a.doc)[0] + ".trace.json")
    with open(rep_path, "w", encoding="utf-8") as f:
        json.dump({"tool": "trace_numbers", "version": VERSION, "doc": os.path.abspath(a.doc),
                   "seeds": [os.path.abspath(s) for s in a.seed],
                   "verdict": "FAIL" if orphans else "PASS",
                   "counts": {"traced": n_ok, "orphan": len(orphans)},
                   "findings": findings}, f, ensure_ascii=False, indent=2)

    print("Wrote %s" % rep_path)
    print("VERDICT: %s — truy được %d/%d số có đơn vị"
          % ("FAIL (số mồ côi)" if orphans else "PASS", n_ok, len(findings)))
    for o in orphans:
        print("  [ORPHAN] dòng %d: \"%s\" — %s" % (o["line"], o["text"], o["context"]))
    if orphans:
        print("  → Số không truy được về seed = nghi AI BỊA — sửa tài liệu hoặc bổ sung dữ liệu nguồn.")
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
