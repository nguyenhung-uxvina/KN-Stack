#!/usr/bin/env python3
"""fab_workbook.py — {PROJECT}_FAB-DB.xlsx generator (helix-cad-workbook).

Đọc cad_extract.json + MASTER_BOM.csv (helix-cad-ingest) + WX-MASTER-DATA.xlsx
(master data kỹ thuật: đơn giá, hao hụt, định mức giờ, chế độ cắt, từ điển mã)
→ sinh workbook dự án nhiều sheet công thức sống, cột theo schema ERPNext,
kèm CHECKLIST đủ-thiếu thông số cho 5 đầu ra (QTCN / định mức / sổ tay QC /
BOM / dự toán) theo references/param_requirements.json.

Guardrail: workbook là FEEDER (BOM Master qua erp-bom import-cad mới là source
of truth); KHÔNG bịa đơn giá — thiếu master → dừng có hướng dẫn; thiếu giá
1 vật liệu → ô "#THIẾU-GIÁ" + CHECKLIST đỏ. Master data được COPY vào workbook
tại thời điểm sinh (snapshot audit + công thức nội bộ, không external link);
chạy lại = refresh (backup .bak, sheet NOTES nhập tay không bị đụng).

Usage:
  python fab_workbook.py <ingested_dir> --master WX-MASTER-DATA.xlsx \
         --project VN-TGT-F [--out path.xlsx] [--requirements param_requirements.json]
  python fab_workbook.py --init-master <path.xlsx>   # tạo master seed
"""
import argparse
import csv
import glob
import io
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill
except ImportError:
    print("[fab_workbook] cần openpyxl: python -m pip install openpyxl", file=sys.stderr)
    sys.exit(3)

HERE = os.path.dirname(os.path.abspath(__file__))
REQUIREMENTS_DEFAULT = os.path.join(HERE, "references", "param_requirements.json")
MISSING = "#THIẾU-GIÁ"
MASTER_SHEETS = ["MATERIALS", "LABOR_RATES", "WORKSTATIONS", "WASTE_FACTORS",
                 "LABOR_NORMS", "CUT_REGIMES", "PART_DICTIONARY"]
CONF_RANK = {"LOW": 0, "MED": 1, "HIGH": 2}
OP_KEYWORDS = [("laser", "laser"), ("tiện", "tien"), ("tien", "tien"),
               ("chấn", "chan"), ("chan", "chan"), ("hàn", "han"), ("han", "han"),
               ("dập", "dap"), ("dap", "dap"), ("phay", "phay"), ("khoan", "khoan")]
BOLD = Font(bold=True)
RED = PatternFill("solid", fgColor="FFC7CE")
YELLOW = PatternFill("solid", fgColor="FFEB9C")

# Seed master data — GIÁ MẪU cho fixture/khởi tạo; kỹ sư định danh THAY bằng giá thật
# trước khi dùng cho dự toán nộp (sheet _META có cột approved_by để ký).
SEED = {
    "MATERIALS": (
        ["item_code", "item_name", "material_class", "uom", "rate", "density_kg_m3", "standard"],
        [["MAT-SS400", "THÉP SS400", "thep_tam", "kg", 18500, 7850, "JIS G3101"],
         ["MAT-5083", "NHÔM 5083", "nhom_tam", "kg", 115000, 2660, "ASTM B928"],
         ["MAT-C45", "THÉP C45", "thep_tron", "kg", 21000, 7850, "TCVN 1766"]]),
    "LABOR_RATES": (
        ["grade", "rate"],
        [["3/7", 45000], ["4/7", 55000], ["5/7", 70000], ["6/7", 90000], ["7/7", 120000]]),
    "WORKSTATIONS": (
        ["workstation", "hour_rate", "capacity_notes"],
        [["laser", 450000, "tấm ≤12mm, bàn 1500×3000"], ["tien", 180000, "Ø max 400"],
         ["chan", 220000, "3m / 100T"], ["han", 150000, "MIG/TIG"],
         ["dap", 250000, "máy dập 63T"], ["phay", 200000, ""], ["khoan", 120000, ""]]),
    "WASTE_FACTORS": (
        ["operation", "material_class", "waste_pct"],
        [["laser", "thep_tam", 8], ["laser", "nhom_tam", 8], ["tien", "thep_tron", 15],
         ["chan", "thep_tam", 5], ["chan", "nhom_tam", 5], ["han", "thep_tam", 3],
         ["dap", "thep_tam", 6], ["phay", "thep_tam", 10], ["khoan", "thep_tam", 2]]),
    "LABOR_NORMS": (
        ["operation", "material_class", "time_in_mins", "grade"],
        [["laser", "thep_tam", 6, "4/7"], ["laser", "nhom_tam", 6, "4/7"],
         ["tien", "thep_tron", 45, "5/7"], ["chan", "thep_tam", 8, "4/7"],
         ["chan", "nhom_tam", 8, "4/7"], ["han", "thep_tam", 30, "5/7"],
         ["dap", "thep_tam", 4, "4/7"], ["phay", "thep_tam", 25, "5/7"],
         ["khoan", "thep_tam", 5, "3/7"]]),
    "CUT_REGIMES": (
        ["operation", "material", "thickness_range", "speed", "feed", "tool"],
        [["laser", "SS400", "2-6mm", "2500 mm/min", "-", "O2 3kW"],
         ["laser", "5083", "2-6mm", "3200 mm/min", "-", "N2 3kW"],
         ["tien", "C45", "-", "180 m/min", "0.25 mm/vg", "CNMG12"]]),
    "PART_DICTIONARY": (
        ["part_code", "name_vi_clean", "name_raw_garbled", "project"], []),
}


def _norm(s):
    return str(s or "").strip().lower()


def _ws_write(ws, cols, rows):
    ws.append(cols)
    for c in ws[1]:
        c.font = BOLD
    for row in rows:
        ws.append(row)


def init_master(path):
    """Ghi WX-MASTER-DATA.xlsx seed. Fail nếu file đã tồn tại (không ghi đè master)."""
    if os.path.exists(path):
        raise SystemExit(f"[fab_workbook] master đã tồn tại, không ghi đè: {path}")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    wb = openpyxl.Workbook()
    meta = wb.active
    meta.title = "_META"
    _ws_write(meta, ["version", "effective_date", "approved_by", "note"],
              [["0.1-seed", datetime.now(timezone.utc).date().isoformat(), "",
                "GIÁ MẪU — kỹ sư định danh thay giá thật + ký approved_by trước khi dùng dự toán"]])
    for name in MASTER_SHEETS:
        cols, rows = SEED[name]
        _ws_write(wb.create_sheet(name), cols, rows)
    wb.save(path)
    print(f"[fab_workbook] đã tạo master seed: {path} (GIÁ MẪU — cần kỹ sư duyệt)")


def load_master(path):
    """Đọc master xlsx → {sheet: {'cols': [...], 'rows': [[...]]}}. Fail-safe: thiếu file/sheet = lỗi cứng."""
    if not os.path.isfile(path):
        raise SystemExit(f"[fab_workbook] KHÔNG thấy master data: {path}\n"
                         f"  → tạo seed: python fab_workbook.py --init-master \"{path}\"")
    wb = openpyxl.load_workbook(path, data_only=True)
    out = {}
    for name in ["_META"] + MASTER_SHEETS:
        if name not in wb.sheetnames:
            raise SystemExit(f"[fab_workbook] master thiếu sheet {name}: {path}")
        ws = wb[name]
        rows = list(ws.iter_rows(values_only=True))
        out[name] = {"cols": list(rows[0]) if rows else [], "rows": [list(r) for r in rows[1:]]}
    return out


def load_extracts(ingested_dir):
    files = sorted(glob.glob(os.path.join(ingested_dir, "*.cad_extract.json")))
    if not files:
        raise SystemExit(f"[fab_workbook] không có *.cad_extract.json trong {ingested_dir}")
    out = []
    for f in files:
        with io.open(f, encoding="utf-8") as fh:
            out.append((os.path.basename(f), json.load(fh)))
    return out


def load_master_bom(ingested_dir):
    """MASTER_BOM.csv (aggregate.py) → {norm(code_in_dxf): row}. Không có file → {} (checklist sẽ báo thiếu qty)."""
    p = os.path.join(ingested_dir, "MASTER_BOM.csv")
    if not os.path.isfile(p):
        return {}
    with io.open(p, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    return {_norm(r.get("code_in_dxf")): r for r in rows if r.get("code_in_dxf")}


def ops_from_process(s):
    """'laser+chấn' → ['laser','chan'] (giữ thứ tự, khử trùng)."""
    found = []
    low = _norm(s)
    for token in re.split(r"[+,/;→\s]+", low):
        for kw, op in OP_KEYWORDS:
            if kw in token and op not in found:
                found.append(op)
    return found


def material_class(material, master):
    n = _norm(material)
    if not n:
        return ""
    for row in master["MATERIALS"]["rows"]:
        code, name, mclass = row[0], row[1], row[2]
        if _norm(name) in n or n in _norm(name) or any(t and t in n for t in _norm(name).split()):
            return mclass or ""
    return ""


def material_code(material, master):
    n = _norm(material)
    if not n:
        return ""
    for row in master["MATERIALS"]["rows"]:
        code, name = row[0], row[1]
        toks = [t for t in _norm(name).split() if len(t) >= 3]
        if _norm(name) in n or n in _norm(name) or any(t in n for t in toks):
            return code or ""
    return ""


def resolve_param(extract, bomrow, name):
    """Giá trị + confidence của 1 thông số theo ma trận param_requirements. (None,'LOW') = thiếu."""
    meta = extract.get("meta", {}) or {}
    ebom = (extract.get("bom") or [{}])[0]
    if name == "part_id":
        return meta.get("part_id") or meta.get("code_in_dxf") or ebom.get("code"), "HIGH"
    if name == "material":
        return meta.get("material") or ebom.get("material"), "MED"
    if name == "thickness_mm":
        for b in extract.get("bom", []) or []:
            if b.get("thickness_mm") is not None:
                return b["thickness_mm"], "MED"
        for d in extract.get("dimensions", []) or []:
            p = _norm(d.get("param"))
            if any(k in p for k in ("thickness", "độ dày", "do day", "dày", "tôn", "plate")):
                return d.get("value"), d.get("confidence", "LOW")
        return None, "LOW"
    if name == "mass_kg":
        return meta.get("mass_kg"), ("MED" if meta.get("mass_kg") is not None else "LOW")
    if name == "qty":
        q = (bomrow or {}).get("qty") or ebom.get("qty")
        return (q if q not in ("", None) else None), "MED"
    if name == "process":
        p = (bomrow or {}).get("process") or meta.get("process") or ebom.get("process")
        return (p if p not in ("", None) else None), "MED"
    if name == "tolerances":
        return (extract.get("tolerances") or None), "MED"
    if name == "surface_finish":
        sf = extract.get("surface_finish")
        if sf:
            return sf, "MED"
        notes = " ".join(extract.get("process_notes", []) or [])
        m = re.search(r"Ra\s*[\d.,]+", notes, re.I)
        return (m.group(0) if m else None), "MED"
    if name == "holes":
        return (extract.get("holes") or None), "MED"
    return None, "LOW"


def norm_gaps(extract, bomrow, master):
    """Python-side: các thông số ĐỊNH MỨC/DỰ TOÁN bị thiếu cho 1 part (mirror công thức Excel).
    Trả {'missing': [...], 'no_rate': [...]} — dùng cho CHECKLIST + báo cáo CLI."""
    missing, no_rate = [], []
    mat, _ = resolve_param(extract, bomrow, "material")
    mass, _ = resolve_param(extract, bomrow, "mass_kg")
    qty, _ = resolve_param(extract, bomrow, "qty")
    proc, _ = resolve_param(extract, bomrow, "process")
    if not mat:
        missing.append("material")
    elif not material_code(mat, master):
        no_rate.append(f"material '{mat}' không khớp MATERIALS master")
    if mass is None:
        missing.append("mass_kg")
    if qty in (None, ""):
        missing.append("qty")
    if not proc:
        missing.append("process")
    else:
        mclass = material_class(mat, master)
        waste_keys = {f"{r[0]}|{r[1]}" for r in master["WASTE_FACTORS"]["rows"]}
        norm_keys = {f"{r[0]}|{r[1]}" for r in master["LABOR_NORMS"]["rows"]}
        for op in ops_from_process(proc):
            k = f"{op}|{mclass}"
            if k not in waste_keys:
                no_rate.append(f"waste {k}")
            if k not in norm_keys:
                no_rate.append(f"norm {k}")
    return {"missing": missing, "no_rate": no_rate}


def _gauge(tol):
    try:
        t = abs(float(tol))
    except (TypeError, ValueError):
        return "theo bản vẽ"
    if t <= 0.05:
        return "CMM / panme điện tử"
    if t <= 0.2:
        return "panme"
    return "thước cặp / dưỡng"


def check_part(extract, bomrow, master, requirements):
    """Chấm ma trận đủ-thiếu 1 part × 5 đầu ra theo param_requirements.json.
    → {output: {'missing_critical': [...], 'missing_warning': [...], 'low_conf': [...], 'no_rate': [...]}}"""
    outputs = requirements["meta"]["outputs"]
    res = {o: {"missing_critical": [], "missing_warning": [], "low_conf": [], "no_rate": []}
           for o in outputs}
    for pname, pcfg in requirements["params"].items():
        val, conf = resolve_param(extract, bomrow, pname)
        sev = pcfg.get("severity", "critical")
        for o in pcfg.get("required_for", []):
            if val in (None, "", []):
                res[o]["missing_critical" if sev == "critical" else "missing_warning"].append(pname)
            elif pcfg.get("min_confidence") and \
                    CONF_RANK.get(str(conf).upper(), 0) < CONF_RANK.get(pcfg["min_confidence"], 2):
                res[o]["low_conf"].append(pname)
            elif pname == "material" and pcfg.get("must_match_master") and \
                    not material_code(val, master):
                res[o]["no_rate"].append(f"material '{val}' không khớp MATERIALS")
    gaps = norm_gaps(extract, bomrow, master)
    for o in ("DINH_MUC", "DU_TOAN"):
        res[o]["no_rate"].extend(x for x in gaps["no_rate"] if x not in res[o]["no_rate"])
    return res


def _part_name(extract, master):
    """Tên sạch: tra PART_DICTIONARY trước, garble → cờ NEEDS-DECODE."""
    meta = extract.get("meta", {}) or {}
    pid = _norm(meta.get("part_id"))
    for row in master["PART_DICTIONARY"]["rows"]:
        if _norm(row[0]) == pid and row[1]:
            return row[1], False
    name = meta.get("name") or ""
    garbled = bool(re.search(r"\\u[0-9a-f]{4}|�", name))
    return name, garbled


def build_workbook(extracts, master, bom_csv, out_path, project, requirements):
    if os.path.exists(out_path):
        shutil.copy2(out_path, out_path + ".bak")
        print(f"[fab_workbook] backup: {out_path}.bak")
    wb = openpyxl.Workbook()

    # _META — snapshot provenance
    meta_ws = wb.active
    meta_ws.title = "_META"
    mmeta = master["_META"]["rows"][0] if master["_META"]["rows"] else ["?", "?", "", ""]
    _ws_write(meta_ws, ["project", "generated_at", "master_version", "master_approved_by",
                        "requirements_version", "n_parts", "note"],
              [[project, datetime.now(timezone.utc).isoformat(), mmeta[0], mmeta[2],
                requirements.get("version", "?"), len(extracts),
                "FEEDER — BOM Master (erp-bom import-cad) mới là source of truth; "
                "master sheets là SNAPSHOT tại thời điểm sinh, sửa giá tại đây → dự toán recalc, "
                "refresh → re-sync từ WX-MASTER-DATA"]])

    # Copy master sheets (WASTE_FACTORS/LABOR_NORMS thêm cột key=op|class ở cột A cho VLOOKUP)
    for name in MASTER_SHEETS:
        ws = wb.create_sheet(name)
        cols, rows = master[name]["cols"], master[name]["rows"]
        if name in ("WASTE_FACTORS", "LABOR_NORMS"):
            _ws_write(ws, ["key"] + list(cols),
                      [[f"{r[0]}|{r[1]}"] + list(r) for r in rows])
        else:
            _ws_write(ws, list(cols), rows)

    # PARTS
    parts_rows = []
    for fname, e in extracts:
        meta = e.get("meta", {}) or {}
        pid = meta.get("part_id") or ""
        bomrow = bom_csv.get(_norm(pid))
        name, garbled = _part_name(e, master)
        mat, _ = resolve_param(e, bomrow, "material")
        thk, _ = resolve_param(e, bomrow, "thickness_mm")
        mass, _ = resolve_param(e, bomrow, "mass_kg")
        qty, _ = resolve_param(e, bomrow, "qty")
        proc, _ = resolve_param(e, bomrow, "process")
        confs = [t.get("confidence", "LOW") for t in (e.get("tolerances") or [])] or ["MED"]
        conf_min = min(confs, key=lambda c: CONF_RANK.get(str(c).upper(), 0))
        parts_rows.append([pid, name + (" [NEEDS-DECODE]" if garbled else ""),
                           material_code(mat, master), mat or "", material_class(mat, master),
                           thk, mass, int(qty) if str(qty or "").isdigit() else qty,
                           proc or "", conf_min, fname])
    ws = wb.create_sheet("PARTS")
    _ws_write(ws, ["part_id", "item_name", "item_code_vt", "material", "material_class",
                   "thickness_mm", "mass_kg", "qty", "process", "confidence_min", "source_file"],
              parts_rows)

    # BOM — schema ERPNext (feeder cho erp-bom import-cad)
    bom_rows = []
    for row in parts_rows:
        bom_rows.append([row[0], row[1], row[1], row[7], "Nos", row[3],
                         (f"t={row[5]}mm" if row[5] is not None else ""), row[8]])
    ws = wb.create_sheet("BOM")
    _ws_write(ws, ["item_code", "item_name", "description", "qty_per_unit",
                   "uom", "material", "spec", "process"], bom_rows)

    # DINH_MUC — 1 dòng per part×operation, công thức sống VLOOKUP vào master copy
    dm_ws = wb.create_sheet("DINH_MUC")
    dm_ws.append(["part_id", "material_class", "item_code_vt", "qty", "mass_kg",
                  "operation", "key", "waste_pct", "vt_kg", "time_in_mins", "grade", "nc_gio"])
    for c in dm_ws[1]:
        c.font = BOLD
    op_index = []  # (part_row, op) theo thứ tự dòng — DU_TOAN dùng lại 1:1
    for row in parts_rows:
        for op in (ops_from_process(row[8]) or [""]):
            op_index.append((row, op))
    for i, (row, op) in enumerate(op_index):
        n = i + 2
        dm_ws.append([
            row[0], row[4], row[2], row[7], row[6], op,
            f'=F{n}&"|"&B{n}',
            f'=IFERROR(VLOOKUP(G{n},WASTE_FACTORS!$A:$D,4,FALSE),"{MISSING}")',
            f'=IF(OR(H{n}="{MISSING}",E{n}="",D{n}=""),"{MISSING}",E{n}*(1+H{n}/100)*D{n})',
            f'=IFERROR(VLOOKUP(G{n},LABOR_NORMS!$A:$E,4,FALSE),"{MISSING}")',
            f'=IFERROR(VLOOKUP(G{n},LABOR_NORMS!$A:$E,5,FALSE),"{MISSING}")',
            f'=IF(OR(J{n}="{MISSING}",D{n}=""),"{MISSING}",J{n}*D{n}/60)',
        ])

    # DU_TOAN — 1:1 với DINH_MUC + dòng TỔNG. rate lookup master copy; lỗi → #THIẾU-GIÁ
    dt_ws = wb.create_sheet("DU_TOAN")
    dt_ws.append(["part_id", "item_code_vt", "vt_kg", "rate_vt", "tt_vat_tu",
                  "nc_gio", "grade", "rate_nc", "tt_nhan_cong",
                  "workstation", "hour_rate", "tt_may", "tong_vnd"])
    for c in dt_ws[1]:
        c.font = BOLD
    for i, (row, op) in enumerate(op_index):
        n = i + 2
        dt_ws.append([
            row[0], row[2],
            f"=DINH_MUC!I{n}",
            f'=IFERROR(VLOOKUP(B{n},MATERIALS!$A:$E,5,FALSE),"{MISSING}")',
            f'=IFERROR(C{n}*D{n},"{MISSING}")',
            f"=DINH_MUC!L{n}",
            f"=DINH_MUC!K{n}",
            f'=IFERROR(VLOOKUP(G{n},LABOR_RATES!$A:$B,2,FALSE),"{MISSING}")',
            f'=IFERROR(F{n}*H{n},"{MISSING}")',
            f"=DINH_MUC!F{n}",
            f'=IFERROR(VLOOKUP(J{n},WORKSTATIONS!$A:$B,2,FALSE),"{MISSING}")',
            f'=IFERROR(F{n}*K{n},"{MISSING}")',
            f'=IFERROR(E{n}+I{n}+L{n},"{MISSING}")',
        ])
    last = len(op_index) + 1
    dt_ws.append(["TỔNG", "", "", "", "", "", "", "", "", "", "", "",
                  f"=SUM(M2:M{last})"])
    for c in dt_ws[last + 1]:
        c.font = BOLD

    # QC_DIMS — kích thước kiểm + dụng cụ đo (nguồn sổ tay QC)
    qc_ws = wb.create_sheet("QC_DIMS")
    qc_ws.append(["part_id", "feature", "value", "tolerance", "confidence", "source", "gauge"])
    for c in qc_ws[1]:
        c.font = BOLD
    for fname, e in extracts:
        pid = (e.get("meta", {}) or {}).get("part_id") or ""
        for t in (e.get("tolerances") or []):
            qc_ws.append([pid, t.get("rule") or t.get("param") or "", t.get("nominal"),
                          t.get("value"), t.get("confidence", "LOW"),
                          t.get("source", ""), _gauge(t.get("value"))])
        for g in (e.get("gdt") or []):
            qc_ws.append([pid, g.get("type") or "GD&T", g.get("datum"), g.get("value"),
                          g.get("confidence", "LOW"), g.get("source", ""), _gauge(g.get("value"))])

    # CHECKLIST — part × 5 đầu ra, đỏ THIẾU / vàng LOW-CONF hoặc thiếu-giá
    ck_ws = wb.create_sheet("CHECKLIST")
    outputs = requirements["meta"]["outputs"]
    ck_ws.append(["part_id"] + outputs)
    for c in ck_ws[1]:
        c.font = BOLD
    for fname, e in extracts:
        pid = (e.get("meta", {}) or {}).get("part_id") or ""
        res = check_part(e, bom_csv.get(_norm(pid)), master, requirements)
        row = [pid]
        fills = [None]
        for o in outputs:
            r = res[o]
            if r["missing_critical"]:
                row.append("THIẾU: " + ", ".join(r["missing_critical"]))
                fills.append(RED)
            elif r["low_conf"] or r["no_rate"]:
                row.append("LOW-CONF/THIẾU-GIÁ: " + ", ".join(r["low_conf"] + r["no_rate"]))
                fills.append(YELLOW)
            elif r["missing_warning"]:
                row.append("ĐỦ (thiếu phụ: " + ", ".join(r["missing_warning"]) + ")")
                fills.append(YELLOW)
            else:
                row.append("ĐỦ")
                fills.append(None)
        ck_ws.append(row)
        for cell, fill in zip(ck_ws[ck_ws.max_row], fills):
            if fill:
                cell.fill = fill

    wb.save(out_path)
    return out_path


def main(argv=None):
    ap = argparse.ArgumentParser(description="{PROJECT}_FAB-DB.xlsx generator (helix-cad-workbook)")
    ap.add_argument("ingested_dir", nargs="?", help="thư mục ingested/ (cad_extract + MASTER_BOM.csv)")
    ap.add_argument("--master", help="WX-MASTER-DATA.xlsx")
    ap.add_argument("--project", help="mã dự án (tên workbook)")
    ap.add_argument("--out", help="đường dẫn xlsx ra (mặc định <ingested>/../{PROJECT}_FAB-DB.xlsx)")
    ap.add_argument("--requirements", default=REQUIREMENTS_DEFAULT)
    ap.add_argument("--init-master", metavar="PATH", help="tạo WX-MASTER-DATA.xlsx seed rồi thoát")
    a = ap.parse_args(argv)

    if a.init_master:
        init_master(a.init_master)
        return 0
    if not a.ingested_dir or not a.master:
        ap.error("cần <ingested_dir> và --master (hoặc --init-master PATH)")
    project = a.project or os.path.basename(os.path.abspath(os.path.join(a.ingested_dir, "..")))
    out = a.out or os.path.join(a.ingested_dir, "..", f"{project}_FAB-DB.xlsx")
    with io.open(a.requirements, encoding="utf-8") as f:
        requirements = json.load(f)
    master = load_master(a.master)
    extracts = load_extracts(a.ingested_dir)
    bom_csv = load_master_bom(a.ingested_dir)
    p = build_workbook(extracts, master, bom_csv, os.path.abspath(out), project, requirements)
    print(f"[fab_workbook] ✅ {p} ({len(extracts)} parts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
