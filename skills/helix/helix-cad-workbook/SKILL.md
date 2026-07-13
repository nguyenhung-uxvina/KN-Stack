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
