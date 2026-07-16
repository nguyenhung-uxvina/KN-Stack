# ROADMAP — CAD Pipeline

> Cập nhật khi đóng/mở việc. Nguyên tắc thêm việc: có bằng chứng lỗi lọt hoặc nhu cầu
> sản phẩm thật — không dựng gate/tính năng phòng xa (bài học "đừng dựng gate quá dày").

## ĐANG CHẶN — việc phía CON NGƯỜI (không phải code)

| # | Việc | Ai | Mở khóa cái gì |
|---|---|---|---|
| 1 | Xử lý `giao-viec.csv` BM-01: gán vật liệu 33 part theo bảng B.3 (DRAWING-SENSOR Phụ lục B), đặt 11 part skeleton/KT = Reference, bật Parts Only view, Update mass + Save | Bên thiết kế | BOM thành nguồn vàng thật; `--release` chạy được; golden nhánh `inventor/` |
| 2 | Rà 209 cặp trùng hình học (danh sách `duplicates` trong weld-report.json) — xoá đúp hoặc xác nhận chủ đích | Bên thiết kế | Tin được tổng khối lượng 408 kg |
| 3 | Chạy `Drawing_Check_Live.iLogic.vb` lần đầu (External Rule) trên .iam + .idw thật | CEO/KS | Kích hoạt D2-04/05, D3-03/07; sửa các [VER] theo version Inventor |
| 4 | Đo tay 3–5 giá trị đối chiếu seed (Gate G2) + 2 người ký → khởi tạo golden `inventor/` | KS + QC | Adapter Apprentice nhánh mass được dùng sản xuất |

## KẾ TIẾP (theo thứ tự giá trị)

1. **Hiệu chuẩn weld_length qua G3**: 1 cụm hàn thật đo tay chiều dài mối hàn → hệ số
   quy đổi chu-vi→m-hàn theo loại mối → số hàn được phép vào định mức.
2. **Golden nhánh `dxf/`**: 1–2 case bản vẽ 2D chuẩn (đường X-UUV đang chạy) — đóng
   nốt nguồn chưa có regression.
3. **S3 history vận hành**: bật `--history/--update-history` trong run_pipeline sau
   mỗi lô PASS (tự nuôi sensor lịch sử; đủ hiệu lực sau ~20 chi tiết/nhóm).
4. **S4-02 vào quy trình revision**: khi BM-01/X-UUV có revision mới → `--diff` cũ/mới
   bắt buộc trong run_pipeline, người duyệt đối chiếu ECN.
5. **PMI/AP242 ngữ nghĩa**: cần 1 file Inventor có MBD annotations để thử đọc GD&T
   thẳng từ STEP (giảm phụ thuộc parse DXF 2D — khâu mong manh nhất).
6. **SEC scanner** (D5): quét cây thư mục đối chiếu `WX_Classification` với vùng lưu
   (file MẬT ngoài vùng air-gap → báo động) — viết khi cụm RCWS/AIRPAD vào pipeline.
7. **Trace DOCX**: `trace_numbers.py` đọc .docx qua `parse_document.py` (hiện .md/.txt).
8. **Định mức tự động hoá tiếp**: nối `calibration.json` vào skill `/qtcn` — hệ số
   thật tự thay hệ số ước tính khi có ≥ N record.

## KHÔNG LÀM (đã cân nhắc và bỏ)

- MCP sống hai chiều với CAD (rủi ro ghi ngược + không chạy được air-gap — WX-QT-CAD-IO-01 §II)
- Tính diện tích/thể tích bằng rhino3dm (không có API — đi đường STEP)
- Gate dày cho sửa đổi WIP (kỹ sư sẽ lách — chỉ chặn tại điểm Released)
