---
name: unlimited-ocr
description: OCR tài liệu scan / PDF ảnh / ảnh chụp sang Markdown theo từng trang bằng mô hình baidu/Unlimited-OCR (VLM 3B kế thừa DeepSeek-OCR — đọc đúng thứ tự cột, bảng, công thức). Ba đường chạy — Space Hugging Face (máy không có GPU NVIDIA, gửi ảnh ra ngoài, quota ZeroGPU rất hẹp), máy chủ SGLang trên máy có CUDA, hoặc `--backend windows` (Windows.Media.Ocr cục bộ, không quota, không gửi gì ra ngoài, chữ thuần không giữ bảng — dùng để làm nốt khi Space hết quota hoặc cho tài liệu không được gửi đi). Có resume theo trang và cảm biến đối chứng với lớp chữ sẵn có của PDF. Triggers on "unlimited ocr", "unlimited-ocr", "OCR sách scan", "OCR pdf", "scan sang markdown", "đọc trang scan", "nhận dạng chữ trang ảnh", "pdf ảnh sang chữ", "ocr bằng VLM", "OCR cục bộ", "windows ocr", "hết quota OCR", "lớp chữ PDF hỏng", or when doc-to-md exits code 3 (page needs OCR).
---

# Unlimited-OCR — Trang Scan → Markdown

Mô hình [baidu/Unlimited-OCR](https://github.com/baidu/Unlimited-OCR) (Baidu, MIT, arXiv 2606.23050). Repo gốc clone ở `D:\GitHub\Unlimited-OCR`. Skill này bọc nó bằng một script chạy được trên máy CEO, thêm resume và cảm biến đối chứng.

## Khi Nào Dùng

- PDF scan không có lớp chữ, hoặc lớp chữ sai thứ tự (mục lục 2 cột, bảng)
- `/doc-to-md` thoát mã `3` (trang cần OCR)
- Cần bảng/công thức giữ cấu trúc mà lớp chữ OCR cũ của Internet Archive làm vỡ
- **Không dùng** khi PDF đã có lớp chữ tốt và chỉ cần văn xuôi — `fitz`/`/doc-to-md` nhanh hơn, miễn phí, không gửi gì ra ngoài. Đo trước: `page.get_text()` từng trang.

## Ràng Buộc Phần Cứng (đã đo 2026-10-19)

Máy CEO: Intel Iris Xe, **không có GPU NVIDIA**, RAM 16 GB, ổ C: còn ~5 GB.
- Code model (`modeling_unlimitedocr.py`) gọi `.cuda()` và `torch.autocast("cuda")` cứng ở mọi nhánh suy luận ⇒ **không chạy cục bộ được** nếu không vá; vá sang CPU thì bf16 trên i7 laptop là nhiều phút/trang. Model 6,7 GB — đừng để cache HF rơi vào ổ C:.
- SGLang trong repo dùng `--attention-backend fa3` (FlashAttention 3 ⇒ GPU Hopper). Trên GPU khác đổi backend attention.

## Lệnh

```bash
S=skills/extract/unlimited-ocr/scripts/unlimited_ocr.py
python -I $S book.pdf --out D:/tmp/ocr_book --pages 1-20     # thử trước vài trang
python -I $S book.pdf --out D:/tmp/ocr_book                  # cả cuốn; chạy lại = làm tiếp
python -I $S scans/ --out D:/tmp/ocr_scans                   # thư mục ảnh
python -I $S book.pdf --out D:/tmp/ocr_book --backend server --server http://<máy-GPU>:10000
python -I $S book.pdf --out D:/tmp/ocr_book --backend windows # cục bộ; làm nốt trang Space bỏ dở
```

Cần: `pip install gradio_client pymupdf requests`. Đầu ra trong `--out`:
`pages/page_NNNN.md` (thô, 1 trang/tệp) · `<tên>.md` (ghép, bỏ dấu `<|det|>`, neo `<!-- page N -->`) · `_report.json` · `_img/` (ảnh trang đã render, tái dùng khi chạy lại).

Mã thoát: `0` xong · `1` có trang lỗi · `4` **hết quota Space** — trang đã xong được giữ, chạy lại đúng lệnh cũ để làm tiếp, **hoặc** chạy lại cùng lệnh thêm `--backend windows` để làm nốt ngay trên máy (chỉ OCR các trang còn thiếu).

## Luật

**1. 🔴 CỔNG PHÂN LOẠI — trước khi chạy `--backend space` (mặc định).** Mỗi trang được tải lên Space công khai của Baidu trên Hugging Face. Tài liệu MẬT / HẠN CHẾ / dự toán quốc phòng / hồ sơ đề tài BQP / bản vẽ Xưởng: **DỪNG, hỏi CEO**. Sách kỹ thuật nước ngoài đã xuất bản, tài liệu công khai → chạy được. Đường vòng: `--backend server` trên máy GPU trong mạng nội bộ.

**2. Quota ZeroGPU quyết định tất cả.** Đo 2026-10-19, không đăng nhập: **2 trang** thì hết (`90s requested vs. 0s left` — mỗi lệnh xin giữ 90 s GPU dù chỉ dùng ~10–40 s). Đặt `HF_TOKEN` (tài khoản free) để nới; tài khoản PRO nới nhiều hơn. Sách >10 trang qua Space = nhiều ngày ⇒ chọn `--pages` có chủ đích (trang hình/bảng/lớp chữ hỏng), đừng OCR cả cuốn khi lớp chữ đã tốt. Cả cuốn ⇒ máy GPU (`--backend server`) hoặc Baidu Cloud OCR.

**3. Giữ `--concurrency 1` với Space.** Song song chỉ đốt quota nhanh hơn, không nhanh hơn thực tế. Với `server` mới tăng (repo gốc mặc định 8).

**4. Đọc cảm biến đối chứng đúng cách.** Với PDF có lớp chữ, mỗi trang có hai số so với lớp chữ:
   | `layer_order_ratio` | `layer_word_recall` | Nghĩa |
   |---|---|---|
   | cao | cao | khớp |
   | **thấp** | **cao** | khác THỨ TỰ — thường chính lớp chữ cũ sai (trang 4 Pollard: mục lục 2 cột, ratio 0,546 / recall 1,0; OCR đúng, lớp chữ xen kẽ) |
   | thấp | thấp | OCR mất/đọc sai chữ ⇒ mở ảnh `_img/page_NNNN.png` kiểm |
   | `null` | `null` | lớp chữ < 20 từ — không có thước, phải mở ảnh |
   Đã chạy đối chứng: dương (lớp chữ vs chính nó) 1,0/1,0; âm (OCR trang 4 vs lớp chữ trang 10) 0,02/0,077. **Recall ≠ đúng chính tả**: chỉ đo từ của lớp chữ có mặt; lớp chữ cũng là OCR nên có lỗi riêng.

**5. `fffd` > 0 = ký tự hỏng thật trong tệp** (đếm `U+FFFD` trên tệp UTF-8, không phải lỗi hiển thị terminal). Lần thử đầu in ra `593�C` qua console — chưa phân định được là console hay model; tin số `fffd` trong `_report.json`, không tin mắt đọc stdout.

**6. Space trả chữ thuần, `server` trả có dấu `<|det|>loại [bbox]<|/det|>`.** Tệp `pages/` giữ thô (có bbox — dùng được để cắt hình); tệp ghép đã bỏ dấu theo hàm `remove_det` của README gốc. Khối `image` bị bỏ khỏi tệp ghép — **hình không được mô tả**, chỉ chữ trong hình (nếu có) được đọc.

**6b. `--backend windows` — Windows.Media.Ocr, KHÔNG phải mô hình Unlimited-OCR** (đo 2026-11-01, bài ICED 01 9 trang có lớp chữ rác):
   - Chạy qua `scripts/winocr.ps1` (PowerShell 5.1, một tiến trình/trang, ~0,8 s/trang). Cục bộ hoàn toàn ⇒ **không cần cổng phân loại của luật 1**, dùng được cho tài liệu không được gửi ra ngoài.
   - Chữ: khớp chuỗi từ **0,990–0,996** với Unlimited-OCR (tr. 1–3); trên PDF có lớp chữ tốt: order 0,91–0,96 / recall 0,99+.
   - 🔴 **Không giữ bảng:** đọc theo dòng, bỏ cả cột (bài thử mất nguyên cột trọng số Wi) ⇒ bảng phải chép tay từ `_img/page_NNNN.png`, kiểm tổng dòng/cột, gắn nhãn chép tay. Hình: nhãn trục rơi thành dòng rời — xoá hoặc chép lại.
   - Lỗi lặp: chữ số **«1» đọc thành «l»** (`[l — 5]`, `figure l.`). Script KHÔNG tự sửa (sửa mù dễ sai ở chỗ chữ «l» thật) — rà `\bl\b` bằng tay sau khi chạy.
   - Ngôn ngữ = gói ngôn ngữ OCR đã cài trong Windows; máy CEO hiện **chỉ có `en-US`** ⇒ tài liệu tiếng Việt phải cài gói OCR `vi-VN` trước. `--lang` sai ⇒ báo rõ ngôn ngữ đang có, mã thoát 1.
   - Script `.ps1` phải **thuần ASCII**: PowerShell 5.1 đọc tệp không BOM theo ANSI, một dấu «—» trong chuỗi làm vỡ cú pháp (lỗi «Missing ')'», đã gặp).
   - Cảm biến luật 4 với **lớp chữ rác** (font không ToUnicode): order/recall đều thấp (0,05/0,23) **dù OCR đúng** — vì thước đo hỏng, không phải OCR hỏng. Nhận ra bằng cách xem `page.get_text()`: không có từ tiếng Anh nào.

**7. Đầu ra OCR là nguồn thô, không phải bằng chứng.** Đưa vào `/book-to-book` hay `/notebook-to-book` thì vẫn qua cổng kiểm trích của pipeline đó; số liệu kỹ thuật (độ dày tấm, ứng suất, nhiệt độ) đối chiếu ảnh trang trước khi dùng cho thiết kế.

**8. Đầu ra vào scratchpad hoặc `D:/tmp/`**, không ghi thẳng vào vault. Muốn lưu vào `3_Resources/` thì hỏi CEO (luật resources: chỉ tạo nếu dùng trong 30 ngày).

## Ghi Chú Kỹ Thuật

- `--mode gundam` (mặc định, base 1024 + crop 640, hợp trang chữ dày) · `base` (1024, không crop; bắt buộc cho đa trang).
- `--dpi 200` mặc định (upstream 300). 200 DPI đã đủ cho sách 509×690 pt; tăng lên nếu chữ nhỏ.
- Đa trang trong một lệnh (`infer_multi`, "long-horizon") **không** có trên Space — Space chỉ có `/run_ocr` (1 ảnh) và `/explode_pdf`. Muốn dùng phải chạy `server`/transformers.
- Dựng máy chủ trên máy CUDA: làm theo `D:\GitHub\Unlimited-OCR\README.md` mục SGLang (wheel trong `wheel/`), rồi trỏ `--server`.

## COD

- Chọn trang cần OCR, quyết gửi tài liệu ra ngoài = **Core** (CEO)
- Chạy script, đọc `_report.json`, khoanh trang nghi ngờ = **Offload** (AI)
- Chạy lại khi hết quota = **Default** (tự động hoá được bằng `/loop`, hoặc làm nốt ngay bằng `--backend windows`)
