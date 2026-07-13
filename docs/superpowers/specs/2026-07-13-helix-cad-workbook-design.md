# helix-cad-workbook — Template + Excel DB nhẹ cho chuỗi trích xuất bản vẽ CAD

> Design spec — đã duyệt qua brainstorming với CEO 2026-07-13.
> Mục tiêu: đảm bảo dữ liệu trích từ bản vẽ ĐỦ thông số cho 5 đầu ra:
> (1) qui trình công nghệ, (2) định mức kỹ thuật, (3) sổ tay quản lý chất lượng (theo dự án),
> (4) BOM, (5) dự toán.

## 1. Bối cảnh & vấn đề

Chuỗi hiện có: `helix-cad-ingest` → `helix-cad-validate` → `helix-cad-nest` → `helix-cad-to-fab` → `forge-fabrication` F0-F5.

Gap đã xác nhận (khảo sát 2026-07-13):
1. Không có checklist thông số nào khai báo "bản vẽ phải cung cấp gì cho từng đầu ra" — sufficiency không kiểm được trước handoff.
2. BOM là chuỗi CSV duy nhất có cấu trúc; định mức, dự toán, QC đều dừng ở markdown viết tay.
3. Hao hụt trong template QTCN hardcode theo lớp vật liệu, không tính từ mass/area đã trích.
4. Không có động cơ dự toán per-part nào tiêu thụ MASTER_BOM.csv + mass + routing (forge-cost là so sánh chiến lược ACH, không phải dự toán).
5. Không có "sổ tay QC" hợp nhất — QC nằm rải ở p4-inspection + QTCN §8.
6. Decode tên tiếng Việt garbled + reconcile mã stale làm lại thủ công mỗi run.

## 2. Quyết định kiến trúc (đã chốt với CEO)

| # | Quyết định | Lựa chọn |
|---|---|---|
| 1 | Vai trò Excel | **Hai chiều**: vừa master data đầu vào, vừa nhận dữ liệu trích xuất có cấu trúc |
| 2 | Quan hệ WX-OPS.xlsx | **Mỗi dự án một workbook** + 1 workbook master data dùng chung; KHÔNG đụng WX-OPS.xlsx |
| 3 | Định dạng 5 đầu ra | **Lai**: QTCN + sổ tay QC = markdown→DOCX; định mức/BOM/dự toán = sheet Excel công thức sống |
| 4 | Sổ tay QLCL | **Theo dự án** (hợp nhất kế hoạch kiểm per-part + gate + biểu mẫu), không phải QMS công ty |
| 5 | Pilot | **Generic + fixture test** trước, áp dự án thật sau |
| 6 | ERP | **Excel trước, schema chuẩn ERPNext** — ERPNext là đích dài hạn, mọi sheet đặt cột theo schema ERP (item_code, item_name, qty_per_unit, uom, rate, operation, workstation, time_in_mins) để khi ERP live import thẳng |

## 3. Kiến trúc

Skill mới **`skills/helix/helix-cad-workbook/`** + script `scripts/fab_workbook.py` (codify, ghi `scripts/_codify_ledger.md`).

```
cad/ingested/*.cad_extract.json ──┐
MASTER_BOM.csv, FAB_ROUTING.md ───┤
                                  ├──► fab_workbook.py ──► {PROJECT}_FAB-DB.xlsx
WX-MASTER-DATA.xlsx (dùng chung) ─┘         │                (workbook dự án, công thức sống)
                                            ▼
                              sheet CHECKLIST ──► helix-cad-validate rule `param_sufficiency`
                                                   (Sensor+Gate, chặn handoff nếu thiếu)
                    {PROJECT}_FAB-DB.xlsx ──► QTCN.docx (template hiện có, đổi nguồn số liệu)
                                          ──► So_tay_QC.docx (template mới)
                                          ──► erp-bom import-cad (feeder, CEO duyệt diff)
```

- **Hook**: `helix-cad-to-fab` / `cad_fab_pipeline.py` thêm stage `workbook` sau `ingest`, trước `nest`. Skill chạy được standalone: `/helix-cad-workbook <ingested-dir> [--master <path>] [--project <code>]`.
- **Guardrail giữ nguyên**: workbook là FEEDER — BOM Master (WX-OPS.xlsx/ERPNext) vẫn là source of truth sau khi CEO duyệt diff qua `erp-bom import-cad`. Không bao giờ ghi thẳng.
- Thư viện: `openpyxl` (đã dùng trong hệ scripts; công thức Excel ghi dạng chuỗi `=...`).

## 4. Cấu trúc workbook

### 4.1 `WX-MASTER-DATA.xlsx` — master data kỹ thuật dùng chung

Vị trí mặc định: `D:\Workshop_X\3_Resources\Master-Data\WX-MASTER-DATA.xlsx`; script nhận `--master <path>` để override. Chỉ kỹ sư định danh sửa; sheet `_META` giữ version + ngày hiệu lực + người duyệt (triết lý contract của helix-cad-validate).

| Sheet | Nội dung | Cột chính |
|---|---|---|
| `_META` | version, effective_date, approved_by, changelog | |
| `MATERIALS` | Đơn giá vật tư + KLR | item_code, item_name, uom, rate_vnd, density_kg_m3, standard |
| `LABOR_RATES` | Đơn giá nhân công theo bậc thợ | grade (3/7→7/7), rate_per_hour_vnd |
| `WORKSTATIONS` | Máy + giá giờ máy | workstation, hour_rate_vnd, capacity_notes |
| `WASTE_FACTORS` | Hệ số hao hụt nguyên công × lớp vật liệu | operation, material_class, waste_pct (thay bảng hardcode trong template QTCN) |
| `CUT_REGIMES` | Chế độ cắt tham khảo | operation, material, thickness_range, speed, feed, tool |
| `PART_DICTIONARY` | Từ điển mã↔tên VN decode (đóng gap #6) | part_code, name_vi_clean, name_raw_garbled, project |

Seed mẫu (fixture): SS400, 5083, các nguyên công laser/tiện/hàn/dập với waste % từ template QTCN hiện hành.

### 4.2 `{PROJECT}_FAB-DB.xlsx` — workbook dự án (sinh máy)

Vị trí: cạnh folder `cad/` của dự án. 6 sheet:

| Sheet | Nguồn | Vai trò |
|---|---|---|
| `PARTS` | cad_extract.json từng part | 1 dòng/part: part_id, name (tra PART_DICTIONARY), material, thickness_mm, mass_kg, qty, confidence tổng hợp, đường dẫn file nguồn |
| `BOM` | MASTER_BOM.csv | Schema ERPNext BOM — feeder cho `erp-bom import-cad` |
| `DINH_MUC` | PARTS × WASTE_FACTORS × LABOR_RATES | Công thức sống: VT = mass_kg × (1 + waste_pct); NC = time_in_mins × grade rate |
| `DU_TOAN` | DINH_MUC × MATERIALS.rate × LABOR/WORKSTATIONS | Công thức sống: sửa đơn giá master → dự toán tự cập nhật. Kèm cột snapshot giá tại thời điểm sinh (audit) |
| `QC_DIMS` | tolerances[]/gdt[]/critical dims | Kích thước kiểm, dung sai, dụng cụ đo đề xuất — nguồn cho sổ tay QC |
| `CHECKLIST` | tính từ các sheet trên | Ma trận part × 5 đầu ra: `ĐỦ` / `THIẾU <field>` / `LOW-CONF <field>`, conditional formatting đỏ ô thiếu |

Liên kết master: external reference tới WX-MASTER-DATA.xlsx + giá trị snapshot (2 cột: `=link` và `value_at_gen`) — mở workbook không có master vẫn đọc được snapshot.

## 5. Checklist đủ thông số + Gate

`param_requirements.json` (versioned, trong skill, kỹ sư định danh sửa) khai ma trận yêu cầu:

| Thông số (từ cad_extract) | QTCN | Định mức | Sổ tay QC | BOM | Dự toán |
|---|:-:|:-:|:-:|:-:|:-:|
| part_id + tên sạch | ✔ | ✔ | ✔ | ✔ | ✔ |
| material (khớp MATERIALS master) | ✔ | ✔ | | ✔ | ✔ |
| thickness / kích thước phôi | ✔ | ✔ | | ✔ | ✔ |
| mass_kg (confidence ≥ MED) | | ✔ | | | ✔ |
| qty | ✔ | ✔ | | ✔ | ✔ |
| routing (nguyên công/station từ FAB_ROUTING) | ✔ | ✔ | ✔ | | ✔ |
| tolerances/GD&T critical | ✔ | | ✔ | | |
| surface_finish / weld notes | ✔ | | ✔ | | |
| holes[] (DFM) | ✔ | | ✔ | | |

Cơ chế:
1. `fab_workbook.py` chấm ma trận khi sinh `CHECKLIST` (Computational, không ML).
2. Rule mới **`param_sufficiency`** trong `design_rules.json` của helix-cad-validate: trường `requirements_json` (đường dẫn), `required_outputs[]` (vd `["QTCN","BOM","DU_TOAN"]`), `severity`. Part thiếu thông số cho đầu ra bắt buộc → FAIL, đóng gate handoff (exit 2). Fail-safe: thiếu dữ liệu ≠ SKIP.
3. Material không khớp MATERIALS master → FAIL kèm `fix_hint` ("thêm vật liệu vào master hoặc sửa title block").
4. Cập nhật `design_rules.schema.md` với rule mới.

## 6. Templates

### 6.1 QTCN (sửa nguồn số liệu)
`forge-fabrication/references/quy-trinh-cong-nghe-template.md`: §4 BOM tổng + §7 định mức/hao hụt đổi nguồn từ bảng hardcode → đọc sheet `BOM`/`DINH_MUC` của workbook dự án. Thêm dòng ghi nguồn: "Số liệu sinh từ {PROJECT}_FAB-DB.xlsx, master data v{n}, ngày {d}".

### 6.2 Sổ tay QC theo dự án (mới)
`helix-cad-workbook/references/so-tay-qc-template.md`, xuất DOCX qua `convert_md_to_docx`:
1. Bìa + kiểm soát tài liệu + phê duyệt (theo mẫu QTCN)
2. Chính sách & trách nhiệm QC (tĩnh, tùy biến nhẹ theo dự án)
3. Kế hoạch kiểm per-part — bảng từ `QC_DIMS`: kích thước, dung sai, dụng cụ đo, tần suất kiểm
4. Gate QC: CKCX/DT/DC/VL/Final — tái dùng logic helix-p4-inspection
5. Biểu mẫu nghiệm thu + NCR
6. Ma trận truy xuất (part → bản vẽ → phép kiểm → biên bản)

## 7. Luồng chạy & xử lý lỗi

Luồng đầy đủ: `/helix-cad-to-fab <folder>` → ingest → **workbook** → validate (gate mở rộng) → nest → fab F0.

Fail-safe:
- Thiếu WX-MASTER-DATA.xlsx → dừng + hướng dẫn tạo từ template seed. KHÔNG tự bịa đơn giá (guardrail "never generate quantities from general knowledge" áp cho cả giá).
- Thiếu đơn giá/hao hụt cho 1 vật liệu → dòng DU_TOAN ghi `#THIẾU-GIÁ`, CHECKLIST đỏ, gate FAIL nếu dự toán thuộc required_outputs.
- Workbook dự án tồn tại → chỉ refresh sheet sinh máy, không ghi đè cột nhập tay; backup `.bak` trước khi ghi.
- Tên part garbled không tra được PART_DICTIONARY → giữ raw + cờ `NEEDS-DECODE` trong PARTS, không chặn (decode là judgment tail).

## 8. Kiểm thử & eval

- Fixture: `evals/fixtures/cad-workbook/` — 2-3 bộ cad_extract.json mẫu (SS400 tấm + 5083) + WX-MASTER-DATA seed + 1 part cố tình thiếu material.
- Eval spec: `evals/helix-cad-workbook.json`, `mode: "static"` (skill là orchestrator đa bước); tính đúng của script kiểm bằng pytest smoke test trên fixture (chạy trong eval checks). Kiểm:
  1. Workbook sinh đủ 6 sheet, cột đúng schema ERP
  2. Công thức DINH_MUC/DU_TOAN khớp tính tay (mass × waste × rate)
  3. CHECKLIST bắt đúng part thiếu material
  4. Gate `param_sufficiency` FAIL đúng ca, PASS đúng ca
- Smoke test chạy script thật end-to-end trên fixture, không chỉ import (bài học leo-ai templates.py).

## 9. Phạm vi thay đổi

| Thành phần | Loại |
|---|---|
| `skills/helix/helix-cad-workbook/SKILL.md` + `references/so-tay-qc-template.md` + `references/param_requirements.json` + `references/master-data-seed/` | MỚI |
| `scripts/fab_workbook.py` + ledger entry | MỚI |
| `helix-cad-validate`: rule `param_sufficiency` (validate.py + schema doc) | SỬA |
| `helix-cad-to-fab`: stage workbook trong cad_fab_pipeline.py + SKILL.md | SỬA |
| `forge-fabrication/references/quy-trinh-cong-nghe-template.md`: §4/§7 đổi nguồn | SỬA |
| `evals/helix-cad-workbook.json` + `evals/fixtures/cad-workbook/` | MỚI |
| VERSION bump + CHANGELOG + CLAUDE.md skill count | SỬA |

Ngoài phạm vi (YAGNI): đồng bộ 2 chiều Excel↔ERPNext (chờ ERP live, dùng import-cad feeder); sổ tay QMS cấp công ty; tự động decode tên garbled (giữ judgment tail, chỉ persist kết quả decode vào PART_DICTIONARY).
