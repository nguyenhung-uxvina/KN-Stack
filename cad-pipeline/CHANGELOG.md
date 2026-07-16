# CHANGELOG — CAD Pipeline

> Quy ước: mỗi phát hành = tag `cad-pipeline-vX.Y`; chi tiết kiểm chứng từng script
> nằm trong `scripts/_codify_ledger.md` (append-only). File này là bản đọc nhanh.

## v0.4 — 2026-07-13 · Gom về `cad-pipeline/` + tài liệu hub

- Toàn bộ pipeline (docs/schemas/scripts/golden/hooks) chuyển về **một thư mục
  `cad-pipeline/`** bằng `git mv` (giữ lịch sử); mọi đường dẫn hiển thị + 6 skill
  tham chiếu + pre-commit hook cập nhật theo; battery 8/8 tại vị trí mới.
- Thêm README (bản đồ + quy trình vận hành/nâng cấp + bài học field), CHANGELOG, ROADMAP.

## v0.3 — 2026-07-13 · U2: vòng phản hồi + Rhino + dashboard (commit 06ef1c5)

- **Giai đoạn 4 có chỗ chứa**: `qtcn-actuals.schema.json` + `record_actuals.py` —
  giờ công/vật tư/NDT thật → `calibration.json` (hệ số giờ công, suất hàn m/h theo
  tư thế, hao hụt, khuyết tật).
- **Rhino**: `rhino_check.py` (HU-01…04, không cần cài Rhino) + `*.material-map.json`;
  fixture `golden/rhino/` vào battery.
- `pipeline_dashboard.py` (1 bảng + blocker); iLogic thêm D2-05 (occurrence trôi) +
  D3-07 (weld symbol). AP242 đã bật ở export; PMI ngữ nghĩa = việc mở.

## v0.2 — 2026-07-13 · U1: một-lệnh + hàn + harness tầng AI (commit 89e8eaf)

- `run_pipeline.py`: cả chuỗi một lệnh, dừng đúng gate (field-test Tong lap 2 chiều).
- `weld_length.py` v0.2: selftest giải tích chữ T 420,0/420,0 mm; field Tong lap
  phân loại **hàn 577 m (cận trên) / 1.274 cặp interference / 209 cặp trùng hình học**.
- `trace_numbers.py`: số có đơn vị phải truy về seed, khớp đúng thứ nguyên — bắt 3/3
  số bịa cài test; nối `/aigate`. `Drawing_Check_Live.iLogic.vb` (D2-04/D3-03/D1-11).

## v0.1 — 2026-07-02 → 07-13 · Nền móng (commit 0860f34, tag cad-pipeline-v0.1) + U0

- 3 đặc tả WX-QT (EXTRACT-SENSOR bản gốc CEO; DRAWING-SENSOR D-rules + lớp SP BM; CAD-IO).
- `validate_qtcn_seed.py` (S1–S4, G1/G3) + `schemas/qtcn-seed.schema.json` +
  golden 4 case giải tích + fixtures cài lỗi + `run_battery.py` + pre-commit hook.
- Adapter: iLogic ×2, Apprentice (chạy sống Tong lap), FreeCAD, BOM xlsx, merge
  (gate cưỡng chế `require_validated`), DXF 2D. `drawing_check.py` + giao-viec.csv.
- `schemas/materials.json` — một nguồn danh mục vật liệu.

### Lỗi thật harness đã bắt (giá trị tự chứng minh)

| Ngày | Lỗi | Bắt bởi |
|---|---|---|
| 07-02 | freecad_extract nhóm mass_varies lệch instance (794%) | S1-01 trên field data |
| 07-02 | `Part.export` mất nhãn part trong STEP | golden run đầu tiên |
| 07-02 | 33/49 part Generic, 0/49 mass cache (BM-01) | drawing_check D1 |
| 07-13 | 209 cặp hình học trùng chỗ trong STEP (nghi đếm trùng khối lượng) | weld_length v0.2 |
| 07-13 | trace v1 để lọt số bịa (khớp sai thứ nguyên kg↔qty) | test cài số bịa |
