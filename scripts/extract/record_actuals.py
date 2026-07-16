#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
record_actuals.py — Ghi số liệu THẬT từ xưởng + tính hệ số hiệu chỉnh định mức
(Giai đoạn 4 pipeline — vòng phản hồi; schema: schemas/qtcn-actuals.schema.json)

Hai chế độ:

  GHI (append-only, kiểm schema trước khi ghi):
    python record_actuals.py --file actuals.jsonl --add '{"schema":"qtcn-actuals/v1",
        "product_code":"BM-01","nguyen_cong":"NC05-HAN","date":"2026-07-20",
        "recorded_by":"Hùng","type":"labor","labor":{"est_hours":12,"actual_hours":15.5,
        "weld_length_m":38.4,"position":"PB"}}'
    (hoặc --add-file record.json — tiện khi ghi từ form/Excel xuất ra)

  BÁO CÁO HIỆU CHỈNH (đọc cả file → hệ số thật trên từng nhóm):
    python record_actuals.py --file actuals.jsonl --report [--out calibration.json]
      • labor  : hệ số giờ công = Σactual/Σest (theo nguyên công + bậc thợ + tư thế);
                 suất hàn thật = Σweld_length_m/Σactual_hours (m/giờ theo tư thế)
      • material: hệ số hao hụt thật = Σissued/Σ(net|est); tỷ lệ thu hồi đầu mẩu
      • ndt    : tỷ lệ khuyết tật = Σdefects/Σchecked theo phương pháp
    calibration.json là ĐẦU VÀO cho lần lập định mức kế tiếp — sau 3–5 sản phẩm,
    định mức chuyển từ ước tính sang dữ liệu thật.

Exit: 0 OK · 2 record sai schema (không ghi) · 3 lỗi dùng.
"""
import argparse, json, os, sys
from collections import defaultdict

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCHEMA_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                            "..", "..", "schemas", "qtcn-actuals.schema.json"))

def validate_record(rec):
    """Trả list lỗi (rỗng = đạt). Dùng jsonschema nếu có, fallback kiểm tối thiểu."""
    try:
        import jsonschema
        with open(SCHEMA_PATH, encoding="utf-8-sig") as f:
            sch = json.load(f)
        return [e.message for e in jsonschema.Draft202012Validator(sch).iter_errors(rec)]
    except ImportError:
        errs = []
        for k in ("schema", "product_code", "nguyen_cong", "date", "type", "recorded_by"):
            if not rec.get(k):
                errs.append("thiếu %r" % k)
        if rec.get("schema") != "qtcn-actuals/v1":
            errs.append("schema phải là qtcn-actuals/v1")
        return errs

def load_all(path):
    out = []
    if os.path.exists(path):
        with open(path, encoding="utf-8-sig") as f:
            for i, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except Exception:
                    sys.stderr.write("[!] dòng %d hỏng JSON — bỏ qua\n" % i)
    return out

def ratio(num, den):
    return round(num / den, 3) if den else None

def report(records, out_path):
    labor = defaultdict(lambda: {"est": 0.0, "act": 0.0, "weld_m": 0.0, "n": 0})
    mat = defaultdict(lambda: {"base": 0.0, "issued": 0.0, "scrap": 0.0, "n": 0})
    ndt = defaultdict(lambda: {"checked": 0, "defects": 0, "n": 0})
    for r in records:
        if r.get("type") == "labor" and r.get("labor"):
            L = r["labor"]
            key = "%s|%s|%s" % (r["nguyen_cong"], L.get("grade") or "-", L.get("position") or "-")
            g = labor[key]
            g["est"] += L.get("est_hours") or 0
            g["act"] += L["actual_hours"]
            g["weld_m"] += L.get("weld_length_m") or 0
            g["n"] += 1
        elif r.get("type") == "material" and r.get("material"):
            M = r["material"]
            key = M.get("item") or r["nguyen_cong"]
            g = mat[key]
            g["base"] += M.get("net_kg") or M.get("est_kg") or 0
            g["issued"] += M["issued_kg"]
            g["scrap"] += M.get("scrap_kg") or 0
            g["n"] += 1
        elif r.get("type") == "ndt" and r.get("ndt"):
            N = r["ndt"]
            g = ndt[N["method"]]
            g["checked"] += N["checked"]
            g["defects"] += N.get("defects") or 0
            g["n"] += 1

    cal = {"schema": "qtcn-calibration/v1", "records": len(records), "labor": {}, "material": {}, "ndt": {}}
    print("— HỆ SỐ GIỜ CÔNG (nguyên công | bậc | tư thế) —")
    for k in sorted(labor):
        g = labor[k]
        hs = ratio(g["act"], g["est"])
        rate = ratio(g["weld_m"], g["act"])
        cal["labor"][k] = {"heso_giocong": hs, "suat_han_m_per_h": rate,
                           "act_hours": round(g["act"], 1), "n": g["n"]}
        print("  %-28s hệ số=%s (n=%d)%s" % (k, hs if hs else "— (chưa có est)", g["n"],
              ("  suất hàn=%.2f m/h" % rate) if rate else ""))
    print("— HỆ SỐ HAO HỤT VẬT TƯ (xuất kho / CAD thuần) —")
    for k in sorted(mat):
        g = mat[k]
        hs = ratio(g["issued"], g["base"])
        cal["material"][k] = {"heso_haohut": hs, "issued_kg": round(g["issued"], 1),
                              "scrap_kg": round(g["scrap"], 1), "n": g["n"]}
        print("  %-28s hệ số=%s | thu hồi %.1f kg (n=%d)" % (k, hs or "—", g["scrap"], g["n"]))
    print("— TỶ LỆ KHUYẾT TẬT NDT —")
    for k in sorted(ndt):
        g = ndt[k]
        rate = ratio(g["defects"], g["checked"])
        cal["ndt"][k] = {"tyle_khuyettat": rate, "checked": g["checked"], "defects": g["defects"]}
        print("  %-6s %d/%d = %s" % (k, g["defects"], g["checked"], rate))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cal, f, ensure_ascii=False, indent=2)
        print("Wrote %s (đầu vào cho lần lập định mức kế tiếp)" % out_path)

def main():
    ap = argparse.ArgumentParser(description="Ghi actuals + hệ số hiệu chỉnh định mức")
    ap.add_argument("--file", required=True, help="actuals.jsonl (append-only)")
    ap.add_argument("--add", default=None, help="record JSON inline")
    ap.add_argument("--add-file", default=None, help="record từ file JSON")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--out", default=None, help="ghi calibration.json (với --report)")
    a = ap.parse_args()

    if a.add or a.add_file:
        try:
            rec = json.loads(a.add) if a.add else json.load(open(a.add_file, encoding="utf-8-sig"))
        except Exception as e:
            sys.stderr.write("[!] JSON hỏng: %s\n" % e); sys.exit(3)
        errs = validate_record(rec)
        if errs:
            for e in errs[:10]:
                sys.stderr.write("  [SCHEMA] %s\n" % e)
            sys.stderr.write("[!] Record sai schema — KHÔNG ghi (dữ liệu bẩn ở đây phá hệ số về sau).\n")
            sys.exit(2)
        with open(a.file, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print("Đã ghi 1 record (%s / %s / %s) → %s"
              % (rec["product_code"], rec["nguyen_cong"], rec["type"], a.file))
    if a.report:
        records = load_all(a.file)
        if not records:
            sys.stderr.write("[!] Chưa có record nào trong %s\n" % a.file); sys.exit(3)
        report(records, a.out)
    if not (a.add or a.add_file or a.report):
        sys.stderr.write("[!] Cần --add/--add-file hoặc --report\n"); sys.exit(3)
    sys.exit(0)

if __name__ == "__main__":
    main()
