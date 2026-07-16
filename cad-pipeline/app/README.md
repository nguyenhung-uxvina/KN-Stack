# app/ — Phần mềm điều khiển tổng thể pipeline

`wx_pipeline_gui.py` — giao diện desktop (Tkinter) gom mọi bước pipeline thành nút bấm.

## Chạy

- Bấm đúp `cad-pipeline\WX_Pipeline.bat`, **hoặc**
- `python cad-pipeline/app/wx_pipeline_gui.py`

Chỉ cần Python có Tkinter (bản chuẩn Windows đã kèm). FreeCAD/Inventor chỉ cần cho
các nút tương ứng — thiếu thì nút đó báo lỗi rõ, không làm sập app.

## Thiết kế

Đây là **lớp vỏ**, không phải lõi. Mỗi nút chỉ dựng lệnh rồi gọi lại đúng script
trong `../scripts/extract/` qua `subprocess`, in output ra khung console và tô màu
theo exit code (xanh=ĐẠT · cam=WARNING · đỏ=FAIL/lỗi). Sửa hành vi trích xuất/kiểm
tra → sửa script trong `scripts/extract/`, KHÔNG sửa GUI. GUI không giữ số liệu,
không ghi ngược file CAD, không mở cổng mạng.

Các tab theo vai trò (ánh xạ `docs/huong-dan/`):

| Tab | Nút chính | Script gọi | HD |
|---|---|---|---|
| Thiết kế | Kiểm bản vẽ / Rhino; chép đường dẫn External Rule | drawing_check · rhino_check | 01, 03 |
| KS công nghệ | Trích xuất 1 lệnh (--release/--force); kiểm 1 seed; kiểm chéo; chiều dài hàn | run_pipeline · validate_qtcn_seed · weld_length | 02 |
| QC / Gate | Golden G3; battery 8/8; kiểm môi trường | validate --golden · run_battery | 04 |
| Đầu ra AI | Kiểm số tài liệu AI | trace_numbers | 05 |
| Xưởng | Ghi actuals; báo cáo hiệu chỉnh | record_actuals | 06 |
| CEO | Dashboard + mở dashboard.md | pipeline_dashboard | 02 §5 |

Gặp lỗi: xem `../docs/huong-dan/07-xu-ly-su-co.md`.
