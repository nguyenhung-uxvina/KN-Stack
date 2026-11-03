---
name: helix-cad-batch
description: "Tự động hoá CAD hàng loạt, tất định, cục bộ — (1) quét HỌ BIẾN THỂ từ một model.py tham số (hợp đồng PARAMS/build của helix-cad-gates) theo bảng CSV: mỗi biến thể dựng lại trong tiến trình con cách ly, xuất STEP (+STL), qua cổng F1 B-Rep kín + F2 hộp bao kỳ vọng, gom summary.csv/.md; (2) đổi tên layer DXF hàng loạt theo bảng ánh xạ (không bao giờ ghi đè tệp gốc). Dùng cho họ chi tiết cùng dạng khác kích thước (chốt, bạc, tai bắt), chuẩn hoá bản vẽ nhà cung cấp về layer xưởng. Triggers on: 'cad batch', 'batch variants', 'họ chi tiết', 'quét biến thể', 'parameter sweep', 'param sweep', 'xuất STEP hàng loạt', 'export STL hàng loạt', 'đổi tên layer', 'rename layers', 'chuẩn hoá layer DXF', 'tự động hoá CAD'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-cad-batch: Họ biến thể + chuẩn hoá DXF

> **Role:** Khối Offload cho ứng dụng 4 của [[helix-cad-agents]]. Không LLM sinh hình học ở đây — chỉ chạy
> lại một `model.py` ĐÃ qua [[helix-cad-gates]] với bộ tham số khác.
> **Backend:** `batch_sweep.py` (dùng `cad_runner.py` + `geom_gates.py` của helix-cad-gates), `dxf_layers.py` (ezdxf).

## Operational Envelope
| DO | DON'T |
|---|---|
| Quét biến thể từ mô hình gốc đã qua cổng đầy đủ (F1–F4) + CEO duyệt | Quét từ mô hình chưa qua F4 (gãy khi đổi kích thước) |
| Ghi bbox kỳ vọng mỗi biến thể vào CSV khi biết | Coi "dựng được" là "đúng" |
| Ghi ra thư mục mới; đổi layer sang tệp mới | Ghi đè STEP đã phát hành / DXF gốc |
| Biến thể đi sản xuất: chạy lại `geom_gates.py` đủ hợp đồng + điểm dò | Phát hành biến thể chỉ với F1/F2 của batch |

## Workflow
### Step 1: Kiểm điều kiện (Offload)
`model.py` phải theo hợp đồng PARAMS/build và đã PASS `geom_gates.py --model` (F4 PASS).
### Step 2: Lập bảng biến thể (CORE — CEO/kỹ sư chọn dải kích thước)
```csv
variant_id,L_SHAFT,D_SHAFT,bbox_x,bbox_y,bbox_z
GT-0301-A,186,28,194,40,40
GT-0301-B,226,28,234,40,40
```
Cột trùng tên PARAMS ghi đè; `bbox_x/y/z` tuỳ chọn. Cột lạ ⇒ dừng (bắt lỗi gõ sai tên tham số).
### Step 3: Chạy (Offload)
```bash
python batch_sweep.py --model model.py --variants variants.csv --out variants_out --stl
```
Exit 0 tất cả PASS · 2 có biến thể FAIL · 3 lỗi đầu vào.
### Step 4: Đổi tên layer DXF (Offload)
```bash
python dxf_layers.py --in-dir dxf/ --map layer_map.csv --out-dir dxf_std/ --dry-run   # xem trước
python dxf_layers.py --in-dir dxf/ --map layer_map.csv --out-dir dxf_std/
```
`layer_map.csv`: `old,new`. Tên mới trùng layer đã có ⇒ exit 2, không đổi.

## Gotchas
- Batch chỉ chạy F1 + F2 (không điểm dò, không F3): đủ để lọc biến thể gãy, **không** đủ để phát hành.
- Sweep dùng `cad_runner` ⇒ mỗi biến thể là một tiến trình Python mới (~2–5 s); 100 biến thể ≈ vài phút.
- Trải phẳng tấm (flat pattern) từ STEP **chưa có** — dùng [[helix-cad-nest]] với DXF đã trải.

## Output
`variants_out/<variant_id>/model.step` (+`.stl`, `gates.json`) · `summary.csv` · `summary.md`.

## COD
| Task | COD |
|---|---|
| Chọn dải biến thể, bảng layer chuẩn | **C** |
| Chạy sweep, đổi layer | O |
| Phát hành biến thể | **C** (sau cổng đầy đủ) |

## Tests
`python -m pytest scripts/test_helix_cad_batch.py -v`
