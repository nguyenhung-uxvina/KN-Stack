---
name: dwg-to-pdf
description: Chuyển file bản vẽ DWG/DXF nhiều tờ (mỗi tờ là một khung in "Khung in A3/A4" đặt trong modelspace — kiểu đóng gói hồ sơ bản vẽ VN) thành bộ tài liệu PDF vector — PDF tổng có bookmark từng tờ + từng tờ riêng + danh mục bản vẽ — KHÔNG cần AutoCAD. Tự giải mã chữ TCVN3 (.VnTime / romant.shx) sang Unicode đủ dấu, in hoa đúng các font chữ hoa TCVN3, đặt tên tờ theo ký hiệu + tên trong khung tên, gắn cờ tờ nghi sai để người rà. Triggers on "dwg sang pdf", "dwg to pdf", "chuyển bản vẽ thành pdf", "xuất pdf bản vẽ", "in bản vẽ ra pdf", "bộ tài liệu pdf", "plot dwg", "publish dwg", "in hàng loạt bản vẽ", "dxf sang pdf", hoặc khi trỏ vào file .dwg/.dxf và yêu cầu PDF.
---

# DWG → bộ PDF

Biến **một file DWG chứa cả bộ bản vẽ** (nhiều khung in đặt cạnh nhau trong modelspace) thành:

| Đầu ra | Nội dung |
|---|---|
| `PDF-<tên file>/<tên file>.pdf` | PDF tổng, mỗi tờ một trang đúng khổ (A3/A4…), bookmark `NN. <ký hiệu> – <tên tờ>` |
| `PDF-<tên file>/Tung-to/NN_<ký hiệu>_<tên>.pdf` | Từng tờ riêng để gửi lẻ |
| `PDF-<tên file>/DANH-MUC-BAN-VE.md` | Bảng danh mục: tờ, ký hiệu, tên, khổ, tỷ lệ khung, cột **Cần rà** |
| `PDF-<tên file>/sheets.json` | Manifest máy đọc (toạ độ khung, chế độ TCVN3, cờ rà soát) |
| `PDF-<tên file>/_preview.png` | Bảng ảnh thu nhỏ mọi trang — dùng để **nhìn kiểm** |

PDF là **vector**: nét đen trên nền trắng, chữ chọn/tìm kiếm được.

Phần tất định nằm trong script [scripts/cad/dwg_to_pdf.py](../../../scripts/cad/dwg_to_pdf.py). Skill này chạy script, **nhìn kiểm** kết quả và báo cáo. Không tự viết lại quy trình render bằng tay.

## Khi nào dùng / không dùng

- **Dùng:** DWG/DXF có các block khung in (tên chứa "khung", "frame", "border", "A3"…) đặt trong modelspace, mỗi khung là một tờ. Đây là cách đóng gói phổ biến ở xưởng VN (bộ QTCN, bản vẽ chế tạo).
- **Không dùng:**
  - Bản vẽ đã dàn trang trong paperspace layout: script sẽ báo, nên in layout bằng DWG TrueView.
  - Cần PDF **giống hệt** AutoCAD (font .shx gốc, bảng plot style .ctb): dùng DWG TrueView 2018 có sẵn trên máy (`C:\Program Files\Autodesk\DWG TrueView 2018 - English`), Plot → `DWG To PDF.pc3`, thao tác tay từng khung.
  - Cần **trích dữ liệu** (kích thước, BOM): dùng `mech-drawing-extract`. Skill này chỉ xuất bản in.

## Phụ thuộc

- Python có `ezdxf` (≥1.1, đã chạy với 1.4.4) và `PyMuPDF` (`fitz`).
- ODA File Converter cho đầu vào `.dwg`: `winget install --id ODA.ODAFileConverter`. Script tự tìm trong `C:\Program Files\ODA\*\`. Nếu thiếu, script thoát với mã 3.
- Font TTF Unicode có đủ dấu tiếng Việt. Mặc định là `arial.ttf`, có thể dùng `times.ttf`.

## Quy trình

### Bước 1 — Dry-run: dò khung, đặt tên, chưa xuất

```bash
python -I D:/KN-Stack/scripts/cad/dwg_to_pdf.py "<file.dwg>" --dry-run
```

Đọc bảng in ra và kiểm tra:
- **Số khung** có khớp số tờ người dùng mong đợi không. Nếu dò thiếu hoặc thừa, chỉ định rõ `--frame-blocks "Khung in A3,Khung in A4"`. Tên block xem ở dòng `Khung: N (...)`.
- **Dòng TCVN3:**
  - `mode=full`: bản vẽ là TCVN3 toàn bộ.
  - `marker`: bản vẽ trộn Unicode và TCVN3.
  - `off`: bản vẽ là Unicode sạch.
  - Nếu chế độ tự nhận sai (chữ ra lỗi), ép bằng `--tcvn3 on` hoặc `--tcvn3 off`.
- **Thứ tự tờ:** script đọc theo hàng từ trên xuống, trong hàng từ trái sang phải, đúng như người vẽ dàn trong modelspace.
- **Tờ có ⚠:** đọc lý do (tên tờ giống ô vật liệu, không đọc được ký hiệu…).

### Bước 2 — Sửa tên tờ (nếu cần)

Heuristic lấy tên tờ là chữ dài nhất trong style chữ hoa, sau khi loại ký hiệu, tên sản phẩm và ô vật liệu. Các tờ bảng kê A4 thường mang tên của bản lắp ráp. Nếu cần sửa, ghi file JSON `{"<số tờ>": "TÊN ĐÚNG"}` rồi truyền vào bằng `--titles file.json`. Tên lấy theo bảng kê của chính bộ bản vẽ, **không tự bịa**. Nếu không chắc thì giữ nguyên và báo người dùng.

### Bước 3 — Xuất

```bash
python -I D:/KN-Stack/scripts/cad/dwg_to_pdf.py "<file.dwg>" [--titles t.json] [--out DIR] [--name "Tên PDF tổng"] [--color]
```

- Mặc định đầu ra nằm **cạnh file nguồn**: `PDF-<tên file>/`. Nếu thư mục đó đã có kết quả cũ thì hỏi trước khi ghi đè, hoặc dùng `--out`.
- Bộ 52 tờ chạy khoảng 2–4 phút. Hãy chạy nền hoặc đặt timeout lớn.
- Mã thoát:
  - `0`: sạch.
  - `2`: xuất xong nhưng có tờ cần rà.
  - `1`: lỗi.
  - `3`: thiếu ODA.

### Bước 4 — Nhìn kiểm (bắt buộc, không bỏ qua)

1. `Read` file `_preview.png`: tìm trang trắng, trang đen, trang thiếu hình, trang bị cắt mép.
2. Render 2–3 trang đại diện ở dpi khoảng 100–150 rồi `Read`: một bản lắp, một bảng kê, một chi tiết. Nếu có ô khung tên thì cắt riêng ô đó ở 150–200 dpi để soi dấu tiếng Việt.
   ```python
   import fitz; d = fitz.open(r"<pdf tổng>"); d[N-1].get_pixmap(dpi=110).save("pN.png")
   d[N-1].get_pixmap(dpi=180, clip=fitz.Rect(x0,y0,x1,y1)).save("crop.png")   # soi khung tên
   ```
3. Kiểm 3 lỗi hay gặp:
   - Chữ dạng `Chó thÝch`, tức TCVN3 chưa giải.
   - Ô vuông `□` thay cho ợ/ỗ, tức một font chưa được thay.
   - Chữ lẽ ra in hoa lại ra chữ thường, tức font chữ hoa chưa được nhận. Thêm font đó bằng `--caps-fonts romanh.shx,<font>.shx`.

### Bước 5 — Báo cáo

Báo ngắn gọn cho người dùng:
- Đường dẫn PDF tổng, thư mục `Tung-to`, số trang.
- Danh sách tờ cần rà kèm lý do.
- **Mâu thuẫn trong bản vẽ gốc** thấy được khi nhìn kiểm, ví dụ: tiêu đề trên hình khác khung tên, ô tên ghi tên vật liệu, ký hiệu trùng. PDF giữ nguyên như DWG. Chỉ báo, không tự sửa nội dung bản vẽ.
- Giới hạn: font .shx được thay bằng TTF nên dáng chữ hơi khác AutoCAD. Đối tượng nằm ngoài mọi khung bị bỏ (số lượng in ở dòng "đối tượng ngoài khung").

## Cơ chế & gotcha (đã trả giá để biết)

1. **Nền đen.** `Frontend.draw_entities()` không tự đặt nền như `draw_layout()`. Phải gọi `fe.set_background(ctx.current_layout_properties.background_color)`, nếu không trang sẽ đen kịt (kể cả khi dùng `BackgroundPolicy.WHITE`).
2. **TCVN3 phải giải toàn cục.** Lối marker-gated của `parse_mech_drawing.py` bỏ sót các chuỗi không có ký tự đánh dấu (`Chó thÝch`, `Sè`, `mãc buéc`). Chế độ `full` giải mọi chuỗi không có ký tự > U+00FF. Script chỉ bật chế độ này khi số chuỗi có marker lớn hơn số chuỗi Unicode thật. Ký tự `Ø` luôn được giữ nguyên (byte trùng với TCVN3 'ỉ').
3. **Font chữ hoa TCVN3.** `romanh.shx` và các họ TTF `.Vn…H` (`.VnArial NarrowH`, `.VnTimeH`) gõ chữ thường nhưng hiển thị chữ hoa. Script in hoa phần chữ, giữ nguyên mã MTEXT (`\P`, `\T0.9;`, `%%c`). Riêng `Vnromadi.shx` (style CKH) chưa rõ có phải font chữ hoa không, đang để chữ thường.
4. **XDATA font.** Text style có thể mang họ font TTF trong XDATA `ACAD`, và giá trị này **đè lên** `.font`. Phải gỡ XDATA, nếu không sẽ ra `□` cho ợ/ỗ.
5. **Mã font inline** `\Fromant|c0;` trong MTEXT: phải xoá, nếu không ezdxf sẽ quay lại dùng font gốc.
6. **Gán đối tượng** theo tâm bbox vào khung nhỏ nhất chứa nó. Khung lồng trong khung khác bị loại. Khổ giấy tính bằng kích thước khung chia tỷ lệ chèn (`xscale`).
7. **Thứ tự hàng:** khung khác khổ thường chỉ thẳng hàng theo mép dưới, nên gom hàng theo độ chồng lấn dọc, không theo mép trên.
8. **ODA kén đường dẫn Unicode.** Script copy file nguồn sang thư mục tạm với tên ASCII trước khi convert.
9. Không đặt tên script tạm là `inspect.py` hay `bisect.py` vì sẽ che module chuẩn và làm `import ezdxf` vỡ.

## Liên quan

- `mech-drawing-extract` (cad-to-json): trích dữ liệu từ chính các bản vẽ này.
- `product-dossier` / `qtcn`: hồ sơ sản phẩm dùng PDF này làm phụ lục bản vẽ.
- WX-Pipeline (`D:\WX-Pipeline`): pipeline CAD → 5 đầu ra. Bảng TCVN3 ở đây được chép từ `parse_mech_drawing.py` để script tự đứng được, không phụ thuộc repo đó.

## Lịch sử

- v1.0.0 (2026-11-02): codify từ phiên xuất bộ bản vẽ BIA BẮN tự động dấu T (52 tờ, 19.BM-01.xx.xx). Kết quả từ script khớp bản làm tay: cùng thứ tự, cùng 52 trang, 12,9 MB, tự gắn cờ tờ 13.00 (ô tên ghi "GANG XÁM").
