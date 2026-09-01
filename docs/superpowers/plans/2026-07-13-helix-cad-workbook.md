# helix-cad-workbook Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sinh workbook Excel `{PROJECT}_FAB-DB.xlsx` (công thức sống, schema chuẩn ERPNext) từ dữ liệu trích xuất CAD + master data kỹ thuật, kèm gate `param_sufficiency` chặn handoff khi thiếu thông số cho 5 đầu ra (QTCN, định mức, sổ tay QC, BOM, dự toán).

**Architecture:** Script `fab_workbook.py` đặt TRONG skill folder `skills/helix/helix-cad-workbook/` (cùng pattern `ingest.py` của helix-cad-ingest — pipeline gọi qua đường dẫn tương đối `HERE/../helix-cad-workbook/`; đây là điều chỉnh so với spec ghi `scripts/`, vẫn đăng ký codify ledger). Master data copy VÀO workbook dự án tại thời điểm sinh (sheet MATERIALS/LABOR_RATES/... nội bộ) — công thức VLOOKUP tham chiếu nội bộ, tránh external-link mong manh của openpyxl; bản copy chính là snapshot audit, CEO sửa giá trong workbook → dự toán recalc ngay, chạy refresh → re-sync từ master. Gate `param_sufficiency` là rule mới trong `validate.py` (stdlib-only), đọc `param_requirements.json` — độc lập với workbook.

**Tech Stack:** Python 3.x; `openpyxl` (CHỈ cho fab_workbook.py); `validate.py` giữ stdlib-only (air-gapped); pytest cho test; bash cho eval.

## Global Constraints

- `validate.py` KHÔNG được import gì ngoài stdlib (air-gapped contract, xem docstring v2.0 của nó).
- Mọi file I/O `encoding="utf-8"`; chạy script trên Windows với `PYTHONUTF8=1`.
- Tên sheet ASCII không dấu: `PARTS`, `BOM`, `DINH_MUC`, `DU_TOAN`, `QC_DIMS`, `CHECKLIST`, `_META` + 7 sheet master copy.
- Cột theo schema ERPNext đúng chữ: `item_code`, `item_name`, `qty_per_unit`, `uom`, `rate`, `operation`, `workstation`, `hour_rate`, `time_in_mins`, `grade`.
- Chuỗi thiếu giá thống nhất: `#THIẾU-GIÁ` (hằng `MISSING` trong code).
- Guardrail: KHÔNG bịa đơn giá/định mức — thiếu master data → dừng có hướng dẫn; workbook là FEEDER, không phải source of truth (BOM Master qua `erp-bom import-cad`).
- Ma trận thông số: param `severity: critical` thiếu → gate FAIL; `severity: warning` (tolerances/surface_finish/holes — tấm không lỗ là hợp lệ) → WARN không đóng gate. Đây là tinh chỉnh đã cân nhắc so với ma trận spec §5.
- Commit prefix `[HELIX]`; mọi commit kết thúc bằng `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- Làm việc trên branch mới `feature/helix-cad-workbook` tách từ HEAD hiện tại.

## Dữ kiện nguồn (đã xác minh trong repo)

- `cad_extract.json`: `meta{part_id, product, name, material, classification, mass_kg?, code_in_dxf?}`, `dimensions[]`, `tolerances[{value, rule?, confidence, source}]`, `holes[{dia, count, positions, depth_mm?, source, confidence}]`, `bom[{code, item, name, material, thickness_mm}]`, `conflicts[]`, `process_notes[]`. Xem `skills/helix/helix-cad-validate/examples/pass_case.cad_extract.json`.
- `MASTER_BOM.csv` (từ `aggregate.py:135`): header `idx,name,qty,material,process,key_dims_mm,holes,code_in_dxf,conflicts`.
- `validate.py`: rule đọc từ `rules.get("rules", {})`, report qua `r.add(rule_id, status, severity, observed, expected, message, fix, source)`; status `FAIL` nào cũng gate (exit 2); `SKIP`/`WARN` không gate. Helper sẵn: `_load`, `_norm`, `_conf_ok`, `_thickness_rows`, `_materials`.
- `cad_fab_pipeline.py`: 4 step (`step_ingest`, `step_aggregate`, `step_pdf`, `step_report`), gọi script skill khác qua `os.path.join(HERE, "..", "helix-cad-ingest", ...)`.
- Eval static mode: JSON `{"skill", "mode": "static", "test_input", "assertions": [{id, name, check, regex, required}]}` — regex chấm trên SKILL.md (xem `evals/wx-diagram.json`).
- QTCN template: `skills/forge/forge-fabrication/references/quy-trinh-cong-nghe-template.md` — dòng 22 là §7 định mức với % hao hụt hardcode.
- Codify ledger: `scripts/_codify_ledger.md`, bảng `| Date | Target Skill | Script | LOC | Tests | Annual LLM saving (est.) | CEO sign-off |`.
- VERSION hiện `1.7.0` → bump `1.8.0`. CLAUDE.md: helix (55)→(56), header 255→256 skills.

---

### Task 0: Branch + thư mục khung

**Files:**
- Create: `skills/helix/helix-cad-workbook/` (dir), `skills/helix/helix-cad-workbook/references/` (dir), `skills/helix/helix-cad-workbook/tests/` (dir), `evals/fixtures/cad-workbook/` (dir)

- [ ] **Step 1: Tạo branch**

```bash
cd /d/KN-Stack && git checkout -b feature/helix-cad-workbook
```

- [ ] **Step 2: Tạo thư mục**

```bash
mkdir -p skills/helix/helix-cad-workbook/references skills/helix/helix-cad-workbook/tests evals/fixtures/cad-workbook
```

- [ ] **Step 3: Cài dependency test**

```bash
python -m pip install --quiet openpyxl pytest && python -c "import openpyxl; print(openpyxl.__version__)"
```
Expected: in ra version (vd `3.1.x`).

---

### Task 1: Fixtures — 3 cad_extract + MASTER_BOM.csv

**Files:**
- Create: `evals/fixtures/cad-workbook/P-001_rev0.cad_extract.json`
- Create: `evals/fixtures/cad-workbook/P-002_rev0.cad_extract.json`
- Create: `evals/fixtures/cad-workbook/P-003_rev0.cad_extract.json`
- Create: `evals/fixtures/cad-workbook/MASTER_BOM.csv`

**Interfaces:**
- Produces: bộ input chuẩn cho mọi test sau. P-001/P-002 đầy đủ thông số; P-003 CỐ TÌNH thiếu `material` + `mass_kg` (test CHECKLIST + gate FAIL).

- [ ] **Step 1: Viết P-001 (SS400 đầy đủ)**

`evals/fixtures/cad-workbook/P-001_rev0.cad_extract.json`:
```json
{
  "meta": {"part_id": "P-001", "product": "FIXTURE", "name": "tấm đế", "material": "SS400", "mass_kg": 4.2, "classification": "THƯỜNG"},
  "dimensions": [{"param": "thickness", "value": 6.0, "confidence": "HIGH", "source": "dxf"}],
  "tolerances": [{"value": 0.1, "rule": "±0.1 lỗ định vị", "confidence": "HIGH", "source": "dxf"}],
  "holes": [{"dia": 8.0, "count": 2, "positions": [[0, 0], [0, 30]], "source": "dxf", "confidence": "HIGH"}],
  "bom": [{"code": "P-001", "item": "1", "name": "tấm đế", "material": "SS400", "thickness_mm": 6.0}],
  "conflicts": [],
  "process_notes": ["Ra 6.3 mặt trên"]
}
```

- [ ] **Step 2: Viết P-002 (5083 đầy đủ)**

`evals/fixtures/cad-workbook/P-002_rev0.cad_extract.json`:
```json
{
  "meta": {"part_id": "P-002", "product": "FIXTURE", "name": "vách ngăn", "material": "5083", "mass_kg": 1.8, "classification": "THƯỜNG"},
  "dimensions": [{"param": "thickness", "value": 4.0, "confidence": "HIGH", "source": "dxf"}],
  "tolerances": [{"value": 0.2, "rule": "±0.2 biên dạng", "confidence": "MED", "source": "pdf"}],
  "holes": [],
  "bom": [{"code": "P-002", "item": "2", "name": "vách ngăn", "material": "5083", "thickness_mm": 4.0}],
  "conflicts": [],
  "process_notes": []
}
```

- [ ] **Step 3: Viết P-003 (thiếu material + mass)**

`evals/fixtures/cad-workbook/P-003_rev0.cad_extract.json`:
```json
{
  "meta": {"part_id": "P-003", "product": "FIXTURE", "name": "gân tăng cứng", "classification": "THƯỜNG"},
  "dimensions": [],
  "tolerances": [],
  "holes": [],
  "bom": [{"code": "P-003", "item": "3", "name": "gân tăng cứng", "thickness_mm": 6.0}],
  "conflicts": [],
  "process_notes": []
}
```

- [ ] **Step 4: Viết MASTER_BOM.csv (đúng header aggregate.py)**

`evals/fixtures/cad-workbook/MASTER_BOM.csv`:
```csv
idx,name,qty,material,process,key_dims_mm,holes,code_in_dxf,conflicts
1,tấm đế,2,SS400,laser+chấn,"420x300x6","2xØ8",P-001,
2,vách ngăn,4,5083,laser,"300x200x4","",P-002,
3,gân tăng cứng,6,,laser,"250x40x6","",P-003,
```

- [ ] **Step 5: Commit**

```bash
git add evals/fixtures/cad-workbook/ && git commit -m "[HELIX] Fixture cad-workbook: 3 extract + MASTER_BOM (P-003 thieu material)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: param_requirements.json + fab_workbook.py phần 1 (loaders, seed master, PARTS/BOM)

**Files:**
- Create: `skills/helix/helix-cad-workbook/references/param_requirements.json`
- Create: `skills/helix/helix-cad-workbook/fab_workbook.py`
- Test: `skills/helix/helix-cad-workbook/tests/test_fab_workbook.py`

**Interfaces:**
- Produces (dùng bởi Task 3-6):
  - `load_extracts(ingested_dir) -> list[tuple[str, dict]]` — (filename, extract)
  - `load_master(path) -> dict[str, dict]` — `{sheet: {"cols": [...], "rows": [[...]]}}`
  - `load_master_bom(dir) -> dict[str, dict]` — key = mã part chuẩn hóa
  - `init_master(path) -> None` — ghi WX-MASTER-DATA.xlsx từ SEED
  - `resolve_param(extract, bomrow, name) -> tuple[value, conf]`
  - `ops_from_process(s) -> list[str]`, `material_class(mat, master) -> str`, `material_code(mat, master) -> str`
  - `build_workbook(extracts, master, bom_csv, out_path, project, requirements) -> str` (Task 2 dựng PARTS/BOM/_META; Task 3-4 mở rộng)
  - Hằng: `MISSING = "#THIẾU-GIÁ"`, `MASTER_SHEETS`, `REQUIREMENTS_DEFAULT`
  - CLI: `python fab_workbook.py <ingested_dir> --master <xlsx> --project <code> [--out <xlsx>]` và `python fab_workbook.py --init-master <xlsx>`

- [ ] **Step 1: Viết param_requirements.json**

`skills/helix/helix-cad-workbook/references/param_requirements.json`:
```json
{
  "version": "1.0",
  "meta": {
    "note": "Ma trận thông số bắt buộc per đầu ra (spec 2026-07-13). Chỉ kỹ sư định danh sửa; bump version khi đổi.",
    "outputs": ["QTCN", "DINH_MUC", "SO_TAY_QC", "BOM", "DU_TOAN"]
  },
  "params": {
    "part_id":        {"severity": "critical", "required_for": ["QTCN", "DINH_MUC", "SO_TAY_QC", "BOM", "DU_TOAN"]},
    "material":       {"severity": "critical", "required_for": ["QTCN", "DINH_MUC", "BOM", "DU_TOAN"], "must_match_master": true},
    "thickness_mm":   {"severity": "critical", "required_for": ["QTCN", "DINH_MUC", "BOM", "DU_TOAN"]},
    "mass_kg":        {"severity": "critical", "required_for": ["DINH_MUC", "DU_TOAN"], "min_confidence": "MED"},
    "qty":            {"severity": "critical", "required_for": ["QTCN", "DINH_MUC", "BOM", "DU_TOAN"]},
    "process":        {"severity": "critical", "required_for": ["QTCN", "DINH_MUC", "SO_TAY_QC", "DU_TOAN"]},
    "tolerances":     {"severity": "warning",  "required_for": ["QTCN", "SO_TAY_QC"]},
    "surface_finish": {"severity": "warning",  "required_for": ["QTCN", "SO_TAY_QC"]},
    "holes":          {"severity": "warning",  "required_for": ["QTCN", "SO_TAY_QC"]}
  }
}
```
Ghi chú: `must_match_master` chỉ được cưỡng chế trong fab_workbook.py CHECKLIST (validate.py không đọc xlsx — whitelist vật liệu ở gate dùng rule `materials` sẵn có).

- [ ] **Step 2: Viết test fail trước (loaders + init-master + PARTS/BOM)**

`skills/helix/helix-cad-workbook/tests/test_fab_workbook.py`:
```python
import json
import os
import subprocess
import sys

import openpyxl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(SKILL, "..", "..", ".."))
FIX = os.path.join(REPO, "evals", "fixtures", "cad-workbook")
sys.path.insert(0, SKILL)

import fab_workbook as fw  # noqa: E402


@pytest.fixture()
def master_path(tmp_path):
    p = str(tmp_path / "WX-MASTER-DATA.xlsx")
    fw.init_master(p)
    return p


def test_init_master_seed(master_path):
    wb = openpyxl.load_workbook(master_path)
    for s in ["_META"] + fw.MASTER_SHEETS:
        assert s in wb.sheetnames
    ws = wb["MATERIALS"]
    header = [c.value for c in ws[1]]
    assert header[:5] == ["item_code", "item_name", "material_class", "uom", "rate"]
    rates = {r[0].value: r[4].value for r in ws.iter_rows(min_row=2)}
    assert rates["MAT-SS400"] == 18500


def test_load_extracts_and_bom():
    extracts = fw.load_extracts(FIX)
    assert [e["meta"]["part_id"] for _, e in extracts] == ["P-001", "P-002", "P-003"]
    bom = fw.load_master_bom(FIX)
    assert bom["p-001"]["qty"] == "2"
    assert bom["p-003"]["material"] == ""


def test_resolve_param():
    extracts = dict((e["meta"]["part_id"], e) for _, e in fw.load_extracts(FIX))
    bom = fw.load_master_bom(FIX)
    v, conf = fw.resolve_param(extracts["P-001"], bom.get("p-001"), "mass_kg")
    assert v == 4.2 and conf == "MED"
    v, _ = fw.resolve_param(extracts["P-001"], bom.get("p-001"), "qty")
    assert v == "2"
    v, _ = fw.resolve_param(extracts["P-003"], bom.get("p-003"), "material")
    assert v in (None, "")


def test_helpers(master_path):
    master = fw.load_master(master_path)
    assert fw.ops_from_process("laser+chấn") == ["laser", "chan"]
    assert fw.material_class("SS400", master) == "thep_tam"
    assert fw.material_code("NHÔM 5083", master) == "MAT-5083"
    assert fw.material_code("titan", master) == ""


def test_build_parts_bom(tmp_path, master_path):
    out = str(tmp_path / "FIXTURE_FAB-DB.xlsx")
    fw.main([FIX, "--master", master_path, "--project", "FIXTURE", "--out", out])
    wb = openpyxl.load_workbook(out)
    for s in ["_META", "PARTS", "BOM"] + fw.MASTER_SHEETS:
        assert s in wb.sheetnames
    parts = {r[0].value: r for r in wb["PARTS"].iter_rows(min_row=2)}
    assert parts["P-001"][6].value == 4.2          # mass_kg
    assert parts["P-001"][7].value == 2            # qty
    bom_header = [c.value for c in wb["BOM"][1]]
    assert bom_header == ["item_code", "item_name", "description", "qty_per_unit",
                          "uom", "material", "spec", "process"]
```

- [ ] **Step 3: Chạy test — phải FAIL**

```bash
cd /d/KN-Stack && python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q
```
Expected: FAIL/ERROR `ModuleNotFoundError: No module named 'fab_workbook'`.

- [ ] **Step 4: Viết fab_workbook.py phần 1**

`skills/helix/helix-cad-workbook/fab_workbook.py`:
```python
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
        if ebom.get("thickness_mm") is not None:
            return ebom["thickness_mm"], "MED"
        for d in extract.get("dimensions", []) or []:
            if "thick" in _norm(d.get("param")) or "dày" in _norm(d.get("param")):
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
```

- [ ] **Step 5: Chạy test — phải PASS**

```bash
python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q
```
Expected: 5 passed. Nếu `material_class`/`material_code` fail vì matching: sửa matching (token ≥3 ký tự), KHÔNG sửa assertion.

- [ ] **Step 6: Commit**

```bash
git add skills/helix/helix-cad-workbook/ && git commit -m "[HELIX] fab_workbook.py phan 1: loaders + init-master seed + PARTS/BOM (schema ERPNext)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: DINH_MUC + DU_TOAN (công thức sống)

**Files:**
- Modify: `skills/helix/helix-cad-workbook/fab_workbook.py` (thêm vào `build_workbook`, ngay TRƯỚC `wb.save(out_path)`)
- Test: `skills/helix/helix-cad-workbook/tests/test_fab_workbook.py` (thêm test)

**Interfaces:**
- Consumes: `parts_rows` (Task 2 — index: 0 part_id, 4 material_class, 6 mass_kg, 7 qty, 8 process), sheet master copy đã có cột `key`.
- Produces: sheet `DINH_MUC` (1 dòng per part×operation, cột A-L) và `DU_TOAN` (1:1 với DINH_MUC + dòng TỔNG). Task 4 CHECKLIST dùng cùng logic thiếu-giá python-side qua `norm_gaps()`.

- [ ] **Step 1: Thêm test fail**

Thêm vào `test_fab_workbook.py`:
```python
def _build(tmp_path, master_path):
    out = str(tmp_path / "FIXTURE_FAB-DB.xlsx")
    fw.main([FIX, "--master", master_path, "--project", "FIXTURE", "--out", out])
    return openpyxl.load_workbook(out)


def test_dinh_muc_formulas(tmp_path, master_path):
    wb = _build(tmp_path, master_path)
    ws = wb["DINH_MUC"]
    header = [c.value for c in ws[1]]
    assert header == ["part_id", "material_class", "item_code_vt", "qty", "mass_kg",
                      "operation", "key", "waste_pct", "vt_kg", "time_in_mins", "grade", "nc_gio"]
    rows = {(r[0].value, r[5].value): r for r in ws.iter_rows(min_row=2)}
    # P-001 process 'laser+chấn' → 2 dòng
    assert ("P-001", "laser") in rows and ("P-001", "chan") in rows
    r = rows[("P-001", "laser")]
    assert r[6].value == '=F2&"|"&B2'
    assert "VLOOKUP" in r[7].value and "WASTE_FACTORS" in r[7].value
    assert "1+H2/100" in r[8].value            # vt = mass*(1+waste%)*qty
    assert "LABOR_NORMS" in r[9].value


def test_du_toan_formulas_and_missing(tmp_path, master_path):
    wb = _build(tmp_path, master_path)
    ws = wb["DU_TOAN"]
    header = [c.value for c in ws[1]]
    assert header == ["part_id", "item_code_vt", "vt_kg", "rate_vt", "tt_vat_tu",
                      "nc_gio", "grade", "rate_nc", "tt_nhan_cong",
                      "workstation", "hour_rate", "tt_may", "tong_vnd"]
    body = list(ws.iter_rows(min_row=2))
    data, total = body[:-1], body[-1]
    r1 = data[0]
    assert "MATERIALS" in r1[3].value and "VLOOKUP" in r1[3].value
    assert "LABOR_RATES" in r1[7].value
    assert "WORKSTATIONS" in r1[10].value
    assert r1[12].value.startswith("=IFERROR(")
    assert total[0].value == "TỔNG" and total[12].value.startswith("=SUM(")
    # P-003 thiếu material → item_code_vt rỗng → rate VLOOKUP bọc IFERROR ra MISSING khi mở Excel;
    # python-side: norm_gaps báo thiếu
    gaps = fw.norm_gaps(dict((e["meta"]["part_id"], e) for _, e in fw.load_extracts(FIX))["P-003"],
                        fw.load_master_bom(FIX).get("p-003"), fw.load_master(master_path))
    assert "material" in gaps["missing"]
    assert "mass_kg" in gaps["missing"]
```

Chạy: `python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q` → Expected FAIL (`KeyError: 'DINH_MUC'`).

- [ ] **Step 2: Thêm `norm_gaps` (module-level, sau `resolve_param`) và block DINH_MUC/DU_TOAN trong `build_workbook`**

Thêm hàm module-level:
```python
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
```

Thêm vào `build_workbook` (sau block BOM, trước `wb.save`):
```python
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
```

- [ ] **Step 3: Chạy test — PASS**

```bash
python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q
```
Expected: 7 passed. Lưu ý openpyxl trả formula string khi load không `data_only` — đúng như test đọc.

- [ ] **Step 4: Kiểm tra công thức bằng tay (1 lần, ghi vào commit message)**

P-001: mass 4.2 × (1+8%) × qty 2 = **9.072 kg** VT laser; NC laser = 6 phút × 2 / 60 = **0.2 giờ**; tt_vat_tu = 9.072 × 18500 = **167 832 VND**. Mở file bằng Excel/LibreOffice nếu có; không có thì xác nhận chuỗi công thức đúng ô như test.

- [ ] **Step 5: Commit**

```bash
git add -u && git commit -m "[HELIX] fab_workbook.py phan 2: DINH_MUC + DU_TOAN cong thuc song (P-001 = 9.072kg/167832d verified)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: QC_DIMS + CHECKLIST (ma trận đủ-thiếu, tô màu)

**Files:**
- Modify: `skills/helix/helix-cad-workbook/fab_workbook.py`
- Test: `skills/helix/helix-cad-workbook/tests/test_fab_workbook.py`

**Interfaces:**
- Consumes: `resolve_param`, `norm_gaps`, `requirements` (param_requirements.json đã load), `CONF_RANK`.
- Produces: `check_part(extract, bomrow, master, requirements) -> dict[output_name, dict]` (module-level — Task 8 eval + SKILL.md viện dẫn); sheet `QC_DIMS`, `CHECKLIST`.

- [ ] **Step 1: Thêm test fail**

```python
def test_qc_dims(tmp_path, master_path):
    wb = _build(tmp_path, master_path)
    ws = wb["QC_DIMS"]
    assert [c.value for c in ws[1]] == ["part_id", "feature", "value", "tolerance",
                                        "confidence", "source", "gauge"]
    rows = [[c.value for c in r] for r in ws.iter_rows(min_row=2)]
    r1 = [r for r in rows if r[0] == "P-001"][0]
    assert r1[3] == 0.1 and r1[6] == "panme"


def test_checklist_flags_missing(tmp_path, master_path):
    wb = _build(tmp_path, master_path)
    ws = wb["CHECKLIST"]
    assert [c.value for c in ws[1]] == ["part_id", "QTCN", "DINH_MUC", "SO_TAY_QC", "BOM", "DU_TOAN"]
    rows = {r[0].value: r for r in ws.iter_rows(min_row=2)}
    assert rows["P-001"][4].value == "ĐỦ"                       # BOM đủ
    assert "THIẾU" in rows["P-003"][4].value and "material" in rows["P-003"][4].value
    assert rows["P-003"][4].fill.fgColor.rgb.endswith("FFC7CE")  # đỏ
    assert str(rows["P-002"][1].value).startswith("ĐỦ")   # holes/surface chỉ là warning phụ


def test_check_part_api(master_path):
    master = fw.load_master(master_path)
    reqs = json.load(open(os.path.join(SKILL, "references", "param_requirements.json"), encoding="utf-8"))
    e3 = dict((e["meta"]["part_id"], e) for _, e in fw.load_extracts(FIX))["P-003"]
    res = fw.check_part(e3, fw.load_master_bom(FIX).get("p-003"), master, reqs)
    assert "material" in res["BOM"]["missing_critical"]
    assert "mass_kg" in res["DU_TOAN"]["missing_critical"]
    assert res["SO_TAY_QC"]["missing_warning"]  # tolerances/holes trống


def test_refresh_creates_bak(tmp_path, master_path):
    out = str(tmp_path / "FIXTURE_FAB-DB.xlsx")
    fw.main([FIX, "--master", master_path, "--project", "FIXTURE", "--out", out])
    fw.main([FIX, "--master", master_path, "--project", "FIXTURE", "--out", out])
    assert os.path.exists(out + ".bak")
```

Chạy → Expected FAIL (`KeyError: 'QC_DIMS'`).

- [ ] **Step 2: Thêm `check_part` + `_gauge` module-level và block QC_DIMS/CHECKLIST trong `build_workbook`**

```python
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
```

Block sheet (trong `build_workbook`, sau DU_TOAN, trước `wb.save`):
```python
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
```
Lưu ý test `test_checklist_flags_missing` cho P-002: tolerances có nhưng holes rỗng → holes là warning → ô QTCN = "ĐỦ (thiếu phụ: holes...)" hoặc surface — assertion đã viết chấp nhận cả hai dạng.

- [ ] **Step 3: Chạy test — PASS**

```bash
python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q
```
Expected: 11 passed.

- [ ] **Step 4: Chạy CLI end-to-end trên fixture (smoke — chạy tool thật, không chỉ import)**

```bash
cd /d/KN-Stack && PYTHONUTF8=1 python skills/helix/helix-cad-workbook/fab_workbook.py --init-master /tmp/wx-master-smoke.xlsx && PYTHONUTF8=1 python skills/helix/helix-cad-workbook/fab_workbook.py evals/fixtures/cad-workbook --master /tmp/wx-master-smoke.xlsx --project FIXTURE --out /tmp/FIXTURE_FAB-DB.xlsx
```
Expected: `[fab_workbook] ✅ ... (3 parts)`.

- [ ] **Step 5: Commit**

```bash
git add -u && git commit -m "[HELIX] fab_workbook.py phan 3: QC_DIMS + CHECKLIST ma tran du-thieu (do/vang)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Rule `param_sufficiency` trong validate.py (stdlib-only)

**Files:**
- Modify: `skills/helix/helix-cad-validate/validate.py` (thêm rule 12 cuối `run_checks`, trước `return r`; + 2 helper)
- Modify: `skills/helix/helix-cad-validate/references/design_rules.schema.md` (thêm dòng bảng rule)
- Create: `evals/fixtures/cad-workbook/design_rules.param.json`
- Test: `skills/helix/helix-cad-workbook/tests/test_param_sufficiency.py`

**Interfaces:**
- Consumes: `param_requirements.json` (Task 2), fixtures (Task 1), helper sẵn `_load`, `_norm`, `_conf_ok`, `_thickness_rows`.
- Produces: rule config trong design_rules.json: `{"param_sufficiency": {"requirements_json": "<path>", "required_outputs": ["QTCN","BOM","DU_TOAN"], "master_bom_csv": "<path optional>", "severity": "critical"}}`. Status `WARN` mới (không gate).

- [ ] **Step 1: Viết design_rules fixture**

`evals/fixtures/cad-workbook/design_rules.param.json` (đường dẫn tương đối resolve từ CWD repo-root — test chạy từ repo root):
```json
{
  "meta": {"product": "FIXTURE", "rev": "A", "contract_version": "1.0.0",
           "classification": "THƯỜNG", "engineer_of_record": "fixture",
           "notes": "Fixture cho rule param_sufficiency"},
  "rules": {
    "param_sufficiency": {
      "requirements_json": "skills/helix/helix-cad-workbook/references/param_requirements.json",
      "required_outputs": ["QTCN", "BOM", "DU_TOAN"],
      "master_bom_csv": "evals/fixtures/cad-workbook/MASTER_BOM.csv",
      "severity": "critical"
    }
  }
}
```

- [ ] **Step 2: Viết test fail (chạy CLI thật — exit code là contract)**

`skills/helix/helix-cad-workbook/tests/test_param_sufficiency.py`:
```python
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
VALIDATE = os.path.join(REPO, "skills", "helix", "helix-cad-validate", "validate.py")
FIX = os.path.join(REPO, "evals", "fixtures", "cad-workbook")
RULES = os.path.join(FIX, "design_rules.param.json")


def run_validate(extract, tmp_path):
    return subprocess.run(
        [sys.executable, VALIDATE, "--extract", os.path.join(FIX, extract),
         "--rules", RULES, "--out", str(tmp_path / "rep"), "--quiet"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"))


def test_pass_when_sufficient(tmp_path):
    r = run_validate("P-001_rev0.cad_extract.json", tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    rep = json.load(open(str(tmp_path / "rep") + ".json", encoding="utf-8"))
    ids = {c["rule_id"]: c["status"] for c in rep["checks"] if c["rule_id"] == "param_sufficiency"}
    assert ids and "FAIL" not in ids.values()


def test_fail_when_missing_material(tmp_path):
    r = run_validate("P-003_rev0.cad_extract.json", tmp_path)
    assert r.returncode == 2
    rep = json.load(open(str(tmp_path / "rep") + ".json", encoding="utf-8"))
    fails = [c for c in rep["checks"] if c["rule_id"] == "param_sufficiency" and c["status"] == "FAIL"]
    assert any("material" in c["observed"] for c in fails)
    assert any("mass_kg" in c["observed"] for c in fails)


def test_fail_safe_missing_requirements(tmp_path):
    bad = tmp_path / "rules_bad.json"
    rules = json.load(open(RULES, encoding="utf-8"))
    rules["rules"]["param_sufficiency"]["requirements_json"] = "KHONG_TON_TAI.json"
    bad.write_text(json.dumps(rules), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, VALIDATE, "--extract", os.path.join(FIX, "P-001_rev0.cad_extract.json"),
         "--rules", str(bad), "--out", str(tmp_path / "rep2"), "--quiet"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"))
    assert r.returncode == 2   # fail-safe: thiếu requirements = FAIL, không SKIP
```

Chạy → Expected: 3 FAIL (rule chưa tồn tại nên P-003 exit 0).

- [ ] **Step 3: Thêm rule vào validate.py**

Thêm 2 helper module-level (sau `_holes`):
```python
def _bom_csv_row(path, extract):
    """MASTER_BOM.csv row khớp part (qty/process fallback cho param_sufficiency). None nếu không có."""
    if not path or not os.path.isfile(path):
        return None
    try:
        with io.open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return None
    meta = extract.get("meta", {}) or {}
    code = _norm(meta.get("code_in_dxf") or meta.get("part_id"))
    for r in rows:
        if _norm(r.get("code_in_dxf")) == code:
            return r
    return None


def _param_value(extract, bomrow, name):
    """Trích (value, confidence) của thông số theo param_requirements — stdlib mirror
    của fab_workbook.resolve_param (giữ đồng bộ khi sửa: cả hai đọc CHUNG param_requirements.json)."""
    meta = extract.get("meta", {}) or {}
    ebom = (extract.get("bom") or [{}])[0]
    if name == "part_id":
        return meta.get("part_id") or meta.get("code_in_dxf") or ebom.get("code"), "HIGH"
    if name == "material":
        return meta.get("material") or ebom.get("material"), "MED"
    if name == "thickness_mm":
        if ebom.get("thickness_mm") is not None:
            return ebom["thickness_mm"], "MED"
        rows = _thickness_rows(extract)
        return (rows[0][0], rows[0][1]) if rows else (None, "LOW")
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
        if extract.get("surface_finish"):
            return extract["surface_finish"], "MED"
        notes = " ".join(extract.get("process_notes", []) or [])
        m = re.search(r"Ra\s*[\d.,]+", notes, re.I)
        return (m.group(0) if m else None), "MED"
    if name == "holes":
        return (extract.get("holes") or None), "MED"
    return None, "LOW"
```
LƯU Ý: thêm `import re` vào khối import đầu validate.py (stdlib, hợp lệ với contract air-gapped) — validate.py hiện chưa import `re`. Logic `Ra\s*[\d.,]+` đồng bộ với `fab_workbook.resolve_param`.

Thêm rule 12 vào cuối `run_checks` (sau block `hole_depth_ratio`, trước `return r`):
```python
    # 12. Param sufficiency — đủ thông số cho các đầu ra bắt buộc (QTCN/BOM/DU_TOAN...).
    #     Ma trận = param_requirements.json (helix-cad-workbook). critical thiếu → FAIL (gate đóng);
    #     warning thiếu → WARN (không gate — tấm không lỗ là hợp lệ). Fail-safe: thiếu ma trận → FAIL.
    ps = rs.get("param_sufficiency")
    if ps:
        sev = ps.get("severity", "critical")
        req_path = ps.get("requirements_json")
        required_outputs = {str(o).upper() for o in ps.get("required_outputs", [])}
        reqs = None
        if req_path and os.path.isfile(req_path):
            try:
                reqs = _load(req_path)
            except (OSError, json.JSONDecodeError):
                reqs = None
        if reqs is None:
            r.add("param_sufficiency", "FAIL", sev, "(no requirements)",
                  req_path or "param_requirements.json",
                  "Thiếu/không đọc được param_requirements.json — không thể chấm đủ thông số (fail-safe).",
                  fix="Trỏ requirements_json tới skills/helix/helix-cad-workbook/references/param_requirements.json.",
                  source="param_sufficiency.requirements_json")
        else:
            bomrow = _bom_csv_row(ps.get("master_bom_csv"), extract)
            for pname, pcfg in (reqs.get("params") or {}).items():
                hit = [o for o in pcfg.get("required_for", []) if str(o).upper() in required_outputs]
                if not hit:
                    continue
                val, conf = _param_value(extract, bomrow, pname)
                crit = pcfg.get("severity", "critical") == "critical"
                if val in (None, "", []):
                    r.add("param_sufficiency", "FAIL" if crit else "WARN", sev,
                          f"{pname}=(none)", f"present for {hit}",
                          f"Thiếu thông số '{pname}' cho đầu ra {hit}.",
                          fix=f"Bổ sung '{pname}' vào bản vẽ/BOM rồi re-ingest "
                              f"(hoặc MASTER_BOM.csv cho qty/process).",
                          source="param_requirements")
                elif pcfg.get("min_confidence") and not _conf_ok(conf, pcfg["min_confidence"]):
                    r.add("param_sufficiency", "FAIL" if crit else "WARN", sev,
                          f"{pname} (conf={conf})", f"conf >= {pcfg['min_confidence']}",
                          f"'{pname}' độ tin cậy {conf} < {pcfg['min_confidence']} — chưa chứng nhận.",
                          fix="CEO/kỹ sư xác nhận giá trị hoặc re-ingest nguồn tốt hơn.",
                          source="param_requirements")
                else:
                    r.add("param_sufficiency", "PASS", sev, pname, f"for {hit}",
                          f"Đủ '{pname}'.", source="param_requirements")
```

- [ ] **Step 4: Cập nhật schema doc**

Trong `references/design_rules.schema.md`, thêm dòng vào bảng Rules (sau `hole_depth_ratio`):
```markdown
| `param_sufficiency` | Đủ thông số cho 5 đầu ra hạ nguồn (QTCN/định mức/sổ tay QC/BOM/dự toán) theo ma trận param_requirements.json của [[helix-cad-workbook]] | `requirements_json` (path), `required_outputs[]`, `master_bom_csv` (optional — qty/process fallback), `severity` — param `critical` thiếu = FAIL, `warning` = WARN không gate |
```
Và thêm ghi chú dưới phần Severity: `**WARN** (mới, v2.1): không gate — dùng cho thông số phụ (tolerances/surface/holes) trong param_sufficiency.`  Bump docstring validate.py `tool_version` `"2.0"` → `"2.1"` (2 chỗ: provenance + out_json version).

- [ ] **Step 5: Chạy test — PASS, và regression cũ**

```bash
python -m pytest skills/helix/helix-cad-workbook/tests/ -x -q && PYTHONUTF8=1 python skills/helix/helix-cad-validate/examples/eval_harness.py
```
Expected: 14 passed; eval_harness PASS (không phá rule cũ).

- [ ] **Step 6: Commit**

```bash
git add -u skills/helix/helix-cad-validate/ && git add skills/helix/helix-cad-workbook/tests/test_param_sufficiency.py evals/fixtures/cad-workbook/design_rules.param.json && git commit -m "[HELIX] validate.py v2.1: rule param_sufficiency (gate du thong so 5 dau ra, WARN khong gate)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Hook stage workbook vào cad_fab_pipeline.py

**Files:**
- Modify: `skills/helix/helix-cad-to-fab/cad_fab_pipeline.py`

**Interfaces:**
- Consumes: CLI fab_workbook.py (Task 2). Đường dẫn pattern sẵn có: `os.path.join(HERE, "..", "helix-cad-workbook", "fab_workbook.py")`.
- Produces: pipeline 5 step; args mới `--master` (default `D:\Workshop_X\3_Resources\Master-Data\WX-MASTER-DATA.xlsx`), `--project`, `--no-workbook`.

- [ ] **Step 1: Sửa cad_fab_pipeline.py**

Thêm sau dòng `AGGREGATE = ...`:
```python
WORKBOOK = os.path.join(HERE, "..", "helix-cad-workbook", "fab_workbook.py")
DEFAULT_MASTER = r"D:\Workshop_X\3_Resources\Master-Data\WX-MASTER-DATA.xlsx"
```

Thêm hàm (sau `step_report`):
```python
def step_workbook(out, project, master):
    """Sinh {PROJECT}_FAB-DB.xlsx (helix-cad-workbook). Skip có hướng dẫn nếu thiếu master —
    KHÔNG bịa đơn giá (fail-safe)."""
    if not os.path.isfile(WORKBOOK):
        print(f"  [workbook] không thấy fab_workbook.py ({WORKBOOK}) — skip")
        return None
    if not master or not os.path.isfile(master):
        print(f"  [workbook] KHÔNG thấy master data: {master}")
        print(f"  → tạo seed: python \"{WORKBOOK}\" --init-master \"{master}\" (kỹ sư duyệt giá trước khi dùng)")
        return None
    r = run([sys.executable, WORKBOOK, out, "--master", master, "--project", project])
    print(r.stdout.strip()[-600:] or r.stderr.strip()[-600:])
    return os.path.join(out, "..", f"{project}_FAB-DB.xlsx")
```

Trong `main()`: thêm args + đổi banner 4→5 step:
```python
    ap.add_argument("--master", default=DEFAULT_MASTER, help="WX-MASTER-DATA.xlsx (đơn giá/hao hụt/định mức)")
    ap.add_argument("--project", default=None, help="mã dự án cho tên FAB-DB.xlsx (mặc định tên folder)")
    ap.add_argument("--no-workbook", action="store_true")
```
Đổi 4 print `[n/4]` → `[n/5]`, và sau `step_report(...)` thêm:
```python
    wbk = None
    if not a.no_workbook:
        print("\n[5/5] workbook (→ {PROJECT}_FAB-DB.xlsx: PARTS/BOM/DINH_MUC/DU_TOAN/QC_DIMS/CHECKLIST)")
        wbk = step_workbook(out, a.project or os.path.basename(os.path.abspath(folder)), a.master)
```
Và dòng `✅ DONE` thêm ` · FAB-DB.xlsx` khi `wbk`. Trong `step_report`, chèn thêm bullet vào mục "Bước AI/CEO finalize" (sau bullet 4):
```python
        "5. **Kiểm CHECKLIST** trong {PROJECT}_FAB-DB.xlsx — ô đỏ THIẾU phải xử lý trước handoff "
        "(gate param_sufficiency của helix-cad-validate sẽ chặn).",
        "6. **CEO chốt** cờ §11 + classification, ký phát hành.",
```
(bỏ bullet 5 cũ, đánh lại số).

- [ ] **Step 2: Smoke pipeline stage với fixture (giả lập ingested/)**

```bash
mkdir -p /tmp/fab-smoke/ingested && cp evals/fixtures/cad-workbook/*.json evals/fixtures/cad-workbook/MASTER_BOM.csv /tmp/fab-smoke/ingested/ && rm /tmp/fab-smoke/ingested/design_rules.param.json && PYTHONUTF8=1 python -c "
import sys; sys.path.insert(0, 'skills/helix/helix-cad-to-fab')
import cad_fab_pipeline as p
p.step_workbook('/tmp/fab-smoke/ingested', 'SMOKE', '/tmp/wx-master-smoke.xlsx')
import os; assert os.path.isfile('/tmp/fab-smoke/SMOKE_FAB-DB.xlsx'), 'workbook missing'
print('SMOKE OK')"
```
Expected: `SMOKE OK`. Chạy thêm nhánh skip: gọi lại với master không tồn tại → in hướng dẫn `--init-master`, không crash.

- [ ] **Step 3: Commit**

```bash
git add -u && git commit -m "[HELIX] cad_fab_pipeline: stage [5/5] workbook (FAB-DB.xlsx) + --master/--project/--no-workbook

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: SKILL.md + sổ tay QC template + sửa QTCN template

**Files:**
- Create: `skills/helix/helix-cad-workbook/SKILL.md`
- Create: `skills/helix/helix-cad-workbook/references/so-tay-qc-template.md`
- Modify: `skills/forge/forge-fabrication/references/quy-trinh-cong-nghe-template.md`

**Interfaces:**
- Consumes: mọi behavior Task 2-6 (SKILL.md mô tả đúng cái đã build, không hứa thêm).
- Produces: skill routing (frontmatter description EN+VN) — eval Task 8 chấm regex trên file này.

- [ ] **Step 1: Viết SKILL.md**

`skills/helix/helix-cad-workbook/SKILL.md` — nội dung đầy đủ:
```markdown
---
name: helix-cad-workbook
description: Sinh workbook Excel {PROJECT}_FAB-DB.xlsx từ dữ liệu trích xuất bản vẽ CAD (cad_extract.json + MASTER_BOM.csv) + master data kỹ thuật WX-MASTER-DATA.xlsx — 6 sheet dữ liệu (PARTS, BOM schema ERPNext, DINH_MUC, DU_TOAN công thức sống, QC_DIMS, CHECKLIST đủ-thiếu) đảm bảo đủ thông số cho 5 đầu ra: qui trình công nghệ, định mức kỹ thuật, sổ tay quản lý chất lượng, BOM, dự toán. Nối gate param_sufficiency (helix-cad-validate) chặn handoff khi thiếu. Triggers on: "cad workbook", "fab db", "FAB-DB", "định mức từ bản vẽ", "dự toán từ CAD", "trích xuất bản vẽ ra excel", "sổ tay chất lượng dự án", "master data kỹ thuật", "WX-MASTER-DATA", "đủ thông số bản vẽ", "extract drawing to excel", "cost estimate from CAD", "technical norms workbook".
---

# helix-cad-workbook — Tầng dữ liệu Excel giữa ingest và fabrication

> **Vị trí trong chuỗi:** helix-cad-ingest → **helix-cad-workbook** → helix-cad-validate (gate) → helix-cad-nest → forge-fabrication F0.
> **COD:** Offload (script sinh workbook + checklist) / Core (CEO/kỹ sư duyệt giá master, xử lý ô đỏ CHECKLIST, ký dự toán).

## Why This Skill Exists
BOM là chuỗi CSV duy nhất có cấu trúc trong pipeline cũ — định mức, dự toán, QC dừng ở markdown viết tay; mass/area trích được nhưng bị bỏ rơi; không checklist nào khai báo "bản vẽ phải cung cấp gì cho từng đầu ra". Skill này đóng cả 4 gap bằng MỘT workbook công thức sống + MỘT ma trận thông số cưỡng chế được.

## Commands
```
python fab_workbook.py <ingested_dir> --master WX-MASTER-DATA.xlsx --project <CODE> [--out x.xlsx]
python fab_workbook.py --init-master <path>     # tạo master seed (GIÁ MẪU — kỹ sư duyệt trước khi dùng)
```
Tự động chạy trong `/helix-cad-to-fab` stage [5/5] (tắt: `--no-workbook`).

## Hai workbook
1. **WX-MASTER-DATA.xlsx** (dùng chung, mặc định `D:\Workshop_X\3_Resources\Master-Data\`): `_META` (version/approved_by) + MATERIALS (item_code, item_name, material_class, uom, rate, density_kg_m3, standard) + LABOR_RATES (grade, rate) + WORKSTATIONS (workstation, hour_rate) + WASTE_FACTORS (operation, material_class, waste_pct) + LABOR_NORMS (operation, material_class, time_in_mins, grade) + CUT_REGIMES + PART_DICTIONARY (part_code, name_vi_clean — decode 1 lần, dùng mãi). CHỈ kỹ sư định danh sửa, bump version.
2. **{PROJECT}_FAB-DB.xlsx** (per dự án, cạnh folder cad/): master sheets COPY vào (= snapshot audit; sửa giá tại đây → recalc ngay; chạy lại script = refresh có backup `.bak`) + PARTS + BOM (schema ERPNext: item_code, item_name, qty_per_unit, uom — feeder cho `/erp-bom import-cad`, CEO duyệt diff) + DINH_MUC (VT = mass×(1+waste%)×qty; NC = time_in_mins×qty/60 — VLOOKUP sống) + DU_TOAN (×rate vật tư/nhân công/giờ máy, dòng TỔNG) + QC_DIMS (dung sai + dụng cụ đo — nguồn sổ tay QC) + CHECKLIST (part × 5 đầu ra: ĐỦ / THIẾU đỏ / LOW-CONF‑THIẾU-GIÁ vàng).

## Ma trận đủ thông số + Gate
`references/param_requirements.json` (versioned, kỹ sư định danh sửa) khai thông số bắt buộc per đầu ra. Nối vào helix-cad-validate qua rule `param_sufficiency` trong design_rules.json:
```json
"param_sufficiency": {"requirements_json": "skills/helix/helix-cad-workbook/references/param_requirements.json",
                      "required_outputs": ["QTCN", "BOM", "DU_TOAN"],
                      "master_bom_csv": "<ingested>/MASTER_BOM.csv", "severity": "critical"}
```
Param `critical` (part_id, material, thickness, mass, qty, process) thiếu → FAIL exit 2, **handoff BLOCKED**. Param `warning` (tolerances, surface_finish, holes) thiếu → WARN không gate (tấm không lỗ là hợp lệ). Fail-safe: thiếu ma trận/master = FAIL, không SKIP.

## Sổ tay QC theo dự án
AI điền `references/so-tay-qc-template.md` từ sheet QC_DIMS + PARTS (KHÔNG bịa phép kiểm — mỗi dòng kế hoạch kiểm phải truy về 1 dòng QC_DIMS), xuất DOCX qua `/convert_md_to_docx`. Cấu trúc: bìa/kiểm soát tài liệu → trách nhiệm QC → kế hoạch kiểm per-part → gate CKCX/DT/DC/VL/Final → biểu mẫu nghiệm thu + NCR → ma trận truy xuất.

## Guardrails
- **FEEDER, không phải source of truth** — BOM Master (WX-OPS.xlsx/ERPNext) vẫn authoritative sau khi CEO duyệt diff `/erp-bom import-cad`. NEVER ghi thẳng ERPNext.
- **NEVER bịa đơn giá/định mức/giờ công** — thiếu master → dừng + hướng dẫn `--init-master`; seed là GIÁ MẪU phải được kỹ sư duyệt (`_META.approved_by`) trước khi dự toán rời xưởng.
- Thiếu giá 1 vật liệu → ô `#THIẾU-GIÁ` + CHECKLIST vàng — không đoán.
- Refresh không đụng sheet người dùng tự thêm ngoài danh sách sinh máy; luôn backup `.bak`.
- Tên garbled → `[NEEDS-DECODE]`, decode là judgment CEO/AI; kết quả persist vào PART_DICTIONARY (sửa 1 lần).
- Dự toán từ workbook là **nội bộ/feeder** — dự toán nộp chính thức theo quy trình dự toán của dự án.
```

- [ ] **Step 2: Viết so-tay-qc-template.md**

`skills/helix/helix-cad-workbook/references/so-tay-qc-template.md`:
```markdown
# Template — SỔ TAY QUẢN LÝ CHẤT LƯỢNG DỰ ÁN {{PROJECT}}

> Điền từ {PROJECT}_FAB-DB.xlsx (sheet QC_DIMS + PARTS + CHECKLIST). QUY TẮC: mỗi dòng kế hoạch
> kiểm PHẢI truy về 1 dòng QC_DIMS — không bịa phép kiểm. Xuất DOCX: /convert_md_to_docx.

## 0. Bìa + kiểm soát tài liệu
| Trường | Giá trị |
|---|---|
| Tài liệu | STCL-{{PROJECT}}-{{REV}} |
| Dự án / Sản phẩm | {{PROJECT}} — {{PRODUCT_NAME}} |
| Soạn / Kiểm tra / Phê duyệt | {{AUTHOR}} / {{REVIEWER}} / {{APPROVER}} (ký, ngày) |
| Phân loại | {{CLASSIFICATION}} |
| Nguồn dữ liệu | {{PROJECT}}_FAB-DB.xlsx (master data v{{MASTER_VERSION}}, sinh {{GENERATED_AT}}) |

Bảng sửa đổi: | Rev | Ngày | Nội dung | Người duyệt |

## 1. Chính sách & trách nhiệm QC
- Quản đốc phân xưởng: kiểm trong-nguyên-công (tự kiểm 100% kích thước tới hạn).
- QC xưởng: gate CKCX / DT / DC / VL / Final; lập biên bản; quyền dừng chuyền.
- Kỹ sư định danh: duyệt NCR, ký xuất xưởng. PASS validator ≠ an toàn — chữ ký người thật là gate cuối.

## 2. Kế hoạch kiểm per-part (từ sheet QC_DIMS)
| Part | Đặc tính kiểm | Danh nghĩa | Dung sai | Dụng cụ đo | Tần suất | Tiêu chí chấp nhận |
|---|---|---|---|---|---|---|
| {{PART_ID}} | {{FEATURE}} | {{VALUE}} | {{TOLERANCE}} | {{GAUGE}} | 100% tới hạn / AQL còn lại | trong dung sai |

Part có CHECKLIST cột SO_TAY_QC ≠ "ĐỦ": liệt kê + biện pháp bổ sung dữ liệu TRƯỚC khi sản xuất.

## 3. Gate QC
| Gate | Nội dung | Hồ sơ |
|---|---|---|
| CKCX | Cơ khí chính xác — kích thước tới hạn sau gia công | Phiếu đo từng part |
| DT | Điện/điện tử (nếu có) | Biên bản test |
| DC | Dung sai cụm — lắp thử | Biên bản lắp |
| VL | Vật liệu — CO/CQ, đối chiếu MATERIALS master | CO/CQ |
| Final | Nghiệm thu xuất xưởng | Biên bản + ảnh |

## 4. Biểu mẫu
- Phiếu đo kích thước (part_id / đặc tính / thực đo / KL đạt-không / người đo / ngày)
- Biên bản NCR (mô tả / nguyên nhân / xử lý: sửa-loại-nhân nhượng / người duyệt = kỹ sư định danh)
- Biên bản nghiệm thu Final

## 5. Ma trận truy xuất
| Part | Bản vẽ (rev) | Dòng QC_DIMS | Phiếu đo | Biên bản gate | NCR (nếu có) |
|---|---|---|---|---|---|

Lưu hồ sơ ≥ 5 năm. Dụng cụ đo có tem hiệu chuẩn còn hạn (sổ hiệu chuẩn riêng).
```

- [ ] **Step 3: Sửa QTCN template (đổi nguồn §4/§7)**

Trong `skills/forge/forge-fabrication/references/quy-trinh-cong-nghe-template.md`: tìm dòng bắt đầu `9. **§7 Định mức vật tư**` (dòng 22) và thay phần "(đề xuất: tấm laser +8%, ...)" bằng:
```
9. **§7 Định mức vật tư** — bảng theo nhóm vật liệu + **% hao hụt công nghệ**. NGUỒN SỐ LIỆU: sheet `DINH_MUC` của `{PROJECT}_FAB-DB.xlsx` (helix-cad-workbook; waste % từ WASTE_FACTORS master data — KHÔNG hardcode; fallback khi chưa có workbook: tấm laser +8%, phôi tiện +15%, định hình/cắt +5%, Teflon/cao su +10%). Ghi rõ nguồn: "Số liệu từ {PROJECT}_FAB-DB.xlsx, master data v{n}". "Viện/bộ phận định mức xác nhận trước khi cấp phôi".
```
Tương tự tìm mục §4 BOM tổng (grep `§4`) và nối vào cuối mô tả của nó: ` NGUỒN SỐ LIỆU: sheet \`BOM\` của \`{PROJECT}_FAB-DB.xlsx\` (schema ERPNext, feeder erp-bom import-cad).`

- [ ] **Step 4: Verify skill được deploy qua junction**

```bash
bash setup.sh --status
```
Expected: helix count tăng 1 (56). Nếu skill mới CHƯA có junction trong `~/.claude/commands/`, chạy lệnh install theo README/setup.sh (`bash setup.sh --install <vault>` đã dùng trước đây) rồi `bash setup.sh --verify`.

- [ ] **Step 5: Commit**

```bash
git add skills/helix/helix-cad-workbook/SKILL.md skills/helix/helix-cad-workbook/references/so-tay-qc-template.md skills/forge/forge-fabrication/references/quy-trinh-cong-nghe-template.md && git commit -m "[HELIX] SKILL.md helix-cad-workbook + so tay QC template + QTCN doi nguon so lieu sang FAB-DB.xlsx

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: Eval spec + ledger + version bump

**Files:**
- Create: `evals/helix-cad-workbook.json`
- Modify: `scripts/_codify_ledger.md`, `VERSION`, `CHANGELOG.md`, `CLAUDE.md`

- [ ] **Step 1: Viết eval spec (static)**

`evals/helix-cad-workbook.json`:
```json
{
  "skill": "helix-cad-workbook",
  "version": "1.0",
  "description": "Binary assertions for helix-cad-workbook (Excel data layer + param sufficiency gate)",
  "mode": "static",
  "test_input": "helix-cad-workbook evals/fixtures/cad-workbook --master WX-MASTER-DATA.xlsx --project FIXTURE",
  "assertions": [
    {"id": "WBK-ROLE", "name": "two_way_excel_role",
     "check": "skill states Excel is both master-data input and structured extraction output",
     "regex": "master data.*(sinh|trích xuất|extract)|hai chiều|WX-MASTER-DATA.*FAB-DB", "required": true},
    {"id": "WBK-SHEETS", "name": "six_data_sheets",
     "check": "all 6 data sheets named",
     "regex": "PARTS[\\s\\S]*BOM[\\s\\S]*DINH_MUC[\\s\\S]*DU_TOAN[\\s\\S]*QC_DIMS[\\s\\S]*CHECKLIST", "required": true},
    {"id": "WBK-ERP", "name": "erpnext_schema_columns",
     "check": "ERPNext column names verbatim",
     "regex": "item_code.*item_name.*qty_per_unit|qty_per_unit.*uom", "required": true},
    {"id": "WBK-FEEDER", "name": "feeder_guardrail",
     "check": "workbook is feeder, erp-bom import-cad diff remains source-of-truth path",
     "regex": "FEEDER|feeder.*import-cad|import-cad.*(duyệt|diff)", "required": true},
    {"id": "WBK-NOFAB", "name": "never_fabricate_rates",
     "check": "never invent prices; missing master halts with init-master guidance; #THIẾU-GIÁ",
     "regex": "NEVER bịa|KHÔNG bịa|#THIẾU-GIÁ", "required": true},
    {"id": "WBK-GATE", "name": "param_sufficiency_gate",
     "check": "gate rule wiring documented with required_outputs and fail-safe",
     "regex": "param_sufficiency[\\s\\S]*required_outputs[\\s\\S]*(FAIL|BLOCKED)", "required": true},
    {"id": "WBK-QC", "name": "qc_handbook_template",
     "check": "per-project QC handbook from QC_DIMS via template, no invented inspections",
     "regex": "so-tay-qc-template|sổ tay.*QC_DIMS|QC_DIMS.*sổ tay", "required": true},
    {"id": "WBK-REFRESH", "name": "refresh_backup",
     "check": "re-run refreshes machine sheets with .bak backup",
     "regex": "\\.bak", "required": true},
    {"id": "WBK-DECODE", "name": "part_dictionary_persist",
     "check": "garbled-name decode persisted once into PART_DICTIONARY",
     "regex": "PART_DICTIONARY", "required": true}
  ]
}
```

- [ ] **Step 2: Chạy eval**

```bash
bash evals/run-eval.sh helix-cad-workbook
```
Expected: 9/9 PASS. Assertion fail → sửa SKILL.md (bổ sung nội dung thật, không nhồi keyword rỗng).

- [ ] **Step 3: Ledger + VERSION + CHANGELOG + CLAUDE.md**

`scripts/_codify_ledger.md` thêm dòng:
```markdown
| 2026-07-13 | helix-cad-workbook | skills/helix/helix-cad-workbook/fab_workbook.py | ~430 | 15 pytest | ~40 giờ AI-soạn định mức/dự toán/năm | pending |
```
(LOC/test-count cập nhật theo số thật lúc đó.)

`VERSION`: `1.7.0` → `1.8.0` (nếu file đang giá trị khác do nhánh Assay đã merge, bump minor từ giá trị hiện tại).

`CHANGELOG.md` thêm entry đầu file:
```markdown
## v1.8.0 — 2026-07-13
- NEW skill `helix/helix-cad-workbook` — tầng dữ liệu Excel giữa ingest và fab: {PROJECT}_FAB-DB.xlsx
  (PARTS/BOM schema ERPNext/DINH_MUC/DU_TOAN công thức sống/QC_DIMS/CHECKLIST) + WX-MASTER-DATA.xlsx
  seed + param_requirements.json (ma trận đủ thông số 5 đầu ra).
- helix-cad-validate v2.1: rule `param_sufficiency` (+ status WARN không gate).
- helix-cad-to-fab: stage [5/5] workbook (--master/--project/--no-workbook).
- forge-fabrication QTCN template: §4/§7 đổi nguồn số liệu sang FAB-DB.xlsx.
- Eval: evals/helix-cad-workbook.json (static 9 assertions) + fixtures/cad-workbook.
```

`CLAUDE.md`: header `255 skills` → `256`; dòng `helix/ (55)` → `(56)` và nối vào mô tả helix: `; helix-cad-workbook tầng dữ liệu Excel FAB-DB.xlsx + gate đủ-thông-số param_sufficiency`. Xác minh số đếm: `bash setup.sh --status` (hoặc `find skills -name SKILL.md | wc -l`).

- [ ] **Step 4: Full test + commit**

```bash
python -m pytest skills/helix/helix-cad-workbook/tests/ -q && bash evals/run-eval.sh helix-cad-workbook && git add -A && git commit -m "[HELIX] Eval helix-cad-workbook 9/9 + ledger + bump v1.8.0 (256 skills)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

- [ ] **Step 5: Push + PR (KHÔNG merge — CEO review)**

```bash
git push -u origin feature/helix-cad-workbook
gh pr create --title "[HELIX] helix-cad-workbook — Excel data layer + param sufficiency gate (v1.8.0)" --body "Spec: docs/superpowers/specs/2026-07-13-helix-cad-workbook-design.md

- fab_workbook.py: {PROJECT}_FAB-DB.xlsx 6 sheet công thức sống, schema ERPNext, seed WX-MASTER-DATA
- validate.py v2.1: rule param_sufficiency (critical FAIL gate / warning WARN)
- cad_fab_pipeline stage [5/5]; QTCN template đổi nguồn; sổ tay QC template
- pytest 15 + eval static 9/9 + smoke CLI end-to-end fixture

🤖 Generated with [Claude Code](https://claude.com/claude-code)"
```

---

## Self-review đã chạy (spec coverage)

| Spec § | Task |
|---|---|
| §3 kiến trúc + hook + standalone CLI | 2, 6 |
| §4.1 master workbook 7 sheet + _META + seed | 2 (`init_master`) |
| §4.2 workbook dự án 6 sheet + snapshot | 2, 3, 4 (snapshot = master copy nội bộ — điều chỉnh có chủ đích khỏi external-link, ghi ở Architecture) |
| §5 ma trận + gate param_sufficiency + fail-safe + fix_hint material | 2 (JSON), 4 (CHECKLIST + must_match_master), 5 (gate; material-khớp-master ở CHECKLIST vì validate.py stdlib-only — whitelist gate dùng rule `materials` sẵn có) |
| §6.1 QTCN đổi nguồn | 7 |
| §6.2 sổ tay QC template | 7 |
| §7 luồng + fail-safe (thiếu master, #THIẾU-GIÁ, .bak, NEEDS-DECODE) | 2, 4, 6 |
| §8 fixture + eval + smoke chạy thật | 1, 4 (smoke), 8 |
| §9 phạm vi + VERSION/CHANGELOG/CLAUDE.md | 8 |

Điều chỉnh so với spec (đã nêu lý do trong plan): (1) script ở skill folder thay vì `scripts/` — theo pattern INGEST/AGGREGATE sẵn có, ledger vẫn ghi; (2) snapshot = copy master sheet nội bộ thay external link — openpyxl không hỗ trợ tốt external link, hành vi CEO-sửa-giá-thấy-ngay vẫn giữ; (3) thêm sheet LABOR_NORMS (spec chưa khai chỗ chứa giờ định mức); (4) tolerances/surface/holes hạ xuống warning không gate — tránh false-fail part hợp lệ không lỗ.
