# HD-02 — KS CÔNG NGHỆ: CHẠY TRÍCH XUẤT (MỘT LỆNH)

> Đầu vào: thư mục `_QTCN_export\<asm>\` bên thiết kế bàn giao (HD-01 §3).
> Đầu ra: `qtcn-seed-final.json` VALIDATED — nguồn số duy nhất cho 5 đầu ra (HD-05).

## 1. Lệnh chuẩn

```bash
python cad-pipeline/scripts/extract/run_pipeline.py --dir "D:\...\_QTCN_export\Tong lap"
```

Tùy chọn:

| Cờ | Khi nào dùng |
|---|---|
| `--release` | **Phát hành lô** — bắt buộc kiểm chéo 2 nguồn (S2); thiếu 1 nguồn = chặn. Mọi bộ số đi vào định mức/dự toán chính thức PHẢI chạy cờ này. |
| `--seed2d <seed.json>` | Có bản vẽ 2D đã trích (DXF qua `parse_mech_drawing.py`) — ghép dung sai/drawing_no vào seed cuối |
| `--name <slug>` | Đặt tên sản phẩm khác tên thư mục |
| `--force` | Đi tiếp qua gate FAIL — CHỈ để chẩn đoán, ghi biên bản, cấm dùng số cho phát hành |

Pipeline tự chạy chuỗi: tìm STEP + BOM → `qtcn-seed-bom.json` + `qtcn-seed-step.json`
→ Gate G1 từng seed → kiểm chéo S2 → merge → validate seed cuối → tóm tắt.
**Dừng ngay tại gate đầu tiên chặn** và in rõ: gate nào, vì sao, sửa ở đâu.

## 2. Đọc kết quả

- Exit `0`: xong. Vẫn phải đọc **danh sách WARNING** cuối output — đó là các mục
  Gate G2 con người xác nhận (HD-04 §2).
- Exit `2`: gate chặn. Đọc dòng `FAIL` trong output hoặc mở
  `<seed>.validation.json` (form F01: từng rule S1–S4, PASS/WARNING/FAIL + giá trị đo).
  Hai hướng xử lý:
  - Lỗi thuộc **model** (vật liệu Generic, PN rỗng, mass lệch V×ρ…) → chạy
    `drawing_check.py --ticket` (HD-03 §2) → gửi `giao-viec.csv` về bên thiết kế.
  - Lỗi thuộc **extractor** (số 2 nguồn lệch nhau vô lý, xem HD-07) → báo người giữ
    pipeline, KHÔNG tự nới ngưỡng.
- Exit `3`: thiếu đầu vào (không có STEP/BOM trong `--dir`) hoặc thiếu freecadcmd
  (đặt env `FREECADCMD` nếu FreeCAD cài chỗ khác).

## 3. Chạy lẻ từng bước (khi cần chẩn đoán)

```bash
# BOM → seed (nguồn vàng QTY/Material/Mass)
python cad-pipeline/scripts/extract/bom_xlsx_to_seed.py --bom "<asm>_BOM.csv" \
    --assembly-code BM-01 --product-name "Bia mục tiêu BM-01"

# STEP → seed (hình học thật; freecadcmd nhận tham số qua ENV — xem HD-07)
set FC_FILE=<asm>.step& set FC_OUT=<dir>& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" cad-pipeline/scripts/extract/freecad_extract.py

# Kiểm 1 seed bất kỳ (hoặc kéo-thả seed vào cad-pipeline/scripts/extract/self_check.bat)
python cad-pipeline/scripts/extract/validate_qtcn_seed.py --seed <seed.json>

# Kiểm chéo 2 nguồn độc lập (S2)
python cad-pipeline/scripts/extract/validate_qtcn_seed.py --cross qtcn-seed-bom.json qtcn-seed-step.json

# Gộp 2 seed (tự TỪ CHỐI seed chưa validate / FAIL / cũ hơn seed — exit 4)
python cad-pipeline/scripts/extract/merge_qtcn_seeds.py --seed2d <a.json> --seed3d <b.json> --out qtcn-seed-final.json
```

## 4. Chiều dài hàn (phục vụ định mức giờ công hàn)

```bash
set FC_FILE=<asm>.step& set FC_OUT=<dir>& "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" cad-pipeline/scripts/extract/weld_length.py
```

Ra `weld-report.json` — 3 nhóm: `weld` (cận trên chiều dài hàn — kỹ sư rà cột
`welded?`, sửa `false` cho mối bulông), `interference` (= lỗi D2-04, chuyển thiết kế),
`duplicates` (hình học trùng chỗ — nghi đếm trùng khối lượng, chuyển thiết kế).
**Số hàn chưa qua hiệu chuẩn G3 — chưa được vào định mức chính thức** (ROADMAP mục 1).

## 5. Nhìn toàn cục (CEO / trưởng nhóm)

```bash
python cad-pipeline/scripts/extract/pipeline_dashboard.py --root "D:\...\_QTCN_export"
```

Ra `dashboard.md`: 1 bảng trạng thái mọi sản phẩm (bản vẽ/trích xuất/chéo/AI/hàn/giao việc)
+ danh sách blocker kèm ai phải làm gì.
