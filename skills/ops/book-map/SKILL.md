---
name: book-map
description: >-
  Dựng một trang HTML "bản đồ sách" offline từ thư mục sách đã qua pipeline
  codebase-to-book / notebook-to-book / book-to-book. Mỗi chương một thẻ: số
  từ thật so với số từ đặt ra, số sơ đồ, số chương khác cần đọc trước, và dòng
  rủi ro của dàn ý. Kèm đồ thị tham chiếu chéo dựng bằng SVG tính sẵn, không
  JavaScript và không gọi mạng. Trả lời câu "ba chương nào cần đọc lại" mà
  không phải mở cả 85–300k từ. Chạy được hồi tố cho sách đã dựng xong.
  Triggers on: "bản đồ sách", "book map", "map sách", "đọc lại sách nào",
  "chương nào cần đọc lại", "tổng quan cuốn sách", "sách thành trang web",
  "book to html", "book overview page", "render book as webpage", "xem nhanh
  cuốn sách".
---

Dựng bản đồ một cuốn sách đã viết xong thành một tệp HTML đọc từ đĩa.

Cách gọi: `/book-map <đường-dẫn-thư-mục-sách>`

## Chạy

Toàn bộ logic nằm ở `scripts/md_to_html.py` — gọi thẳng, đừng dựng lại bằng tay:

```bash
python D:/KN-Stack/scripts/md_to_html.py "<thư-mục-sách>" [-o out.html] [--verify]
```

Thư mục sách là thư mục **chứa `book.md`**, ví dụ
`D:/Workshop_X/3_Resources/Books/usv-thiet-ke-he-thong` — KHÔNG phải đường dẫn
tới `book.md` trực tiếp.

| Cờ | Dùng khi |
|---|---|
| `-o <path>` | Đặt nơi ra. Bỏ trống thì `<thư-mục>/<slug>-map.html` |
| `--verify` | Chạy lại cổng nghiệm thu trên tệp đã dựng, không dựng lại |

Nếu không có đường dẫn trong `$ARGUMENTS`, hỏi người dùng cần dựng cuốn nào.

## Ba tầng dữ liệu — tầng 2 thiếu thì in `chưa đo`, KHÔNG bịa

1. **Xương, bắt buộc** — đọc từ `book.md`: danh sách chương, tên chương, số từ,
   số sơ đồ, đồ thị tham chiếu chéo, nhãn phạm vi. Thiếu thì dừng, không sinh trang.
2. **Làm giàu, suy thoái êm** — từ `Phase3-Outline.md`: số từ đặt ra, dòng `Rủi ro:`,
   số hình, neo. Khuôn dàn ý **không nhất quán** giữa các cuốn (22/32 có heading
   `###`; ngay trong một cuốn chỉ 13/28 chương dùng bullet), nên thiếu là chuyện
   thường — in `chưa đo`, đừng suy luận.
3. **Sinh mới** — ô tóm tắt 3–5 dòng. Hiện in `chưa tóm tắt`; xem spec §1.2.

## An ninh — ràng buộc cứng

Trang dựng **offline tuyệt đối**: không CDN, không `<script>`, không gọi bất kỳ
dịch vụ web nào — kể cả cho sơ đồ tham chiếu chéo, dựng sẵn bằng SVG tĩnh trong
Python, không qua thư viện JS nào. Không được sửa cho khác đi. Một thẻ
`src="https://…"` không chỉ phá tính offline — nó đẩy tên cuốn sách ra DNS của
người khác. Cổng `--verify` chặn việc này (`goi mang`, `the script`); đây là
ràng buộc kiến trúc, không phải tuỳ chọn.

**Không publish trang này lên dịch vụ ngoài / không gửi ra khỏi máy.** Phần lớn
sách trong kho xếp ⛔ NỘI BỘ. Đổi định dạng (markdown → HTML) không phải một
quyết định phát hành mới; phạm vi chốt ở pipeline gốc đi theo tệp.

## Đọc bảng nghiệm thu

Script in một bảng 10 phép đo cuối lượt chạy (cả khi dựng mới và khi `--verify`).
Dòng nào CHẶN thì script trả mã lỗi và in "CÒ ĐỘNG CHẶN — không giao tệp này":

- **`ty le phu`** — tổng số từ trong các chương chia cho `wc -w` của cả
  `book.md`. Dưới **70% là CHẶN**: nghĩa là parser mất chương, không phải sách
  ngắn. 70–85% là cảnh báo. Đây là cảm biến **duy nhất** bắt đủ 5/5 ca lỗi parse
  đã đo được — hai cảm biến chỉ so các chương với nhau bỏ sót 4/5, và một cuốn
  (`pahl-beitz-tap2`) nằm ở **40% phủ** mà hai cảm biến đó vẫn báo "sạch".
- **`goi mang`** · **`the script`** · **`chu thich html`** — phải bằng 0,
  CHẶN nếu khác 0.
- **`nhan pham vi`** — phải ≥ 1, CHẶN nếu = 0. Không khai được phạm vi ở đâu
  thì trang tự in `⛔ PHẠM VI CHƯA KHAI — coi như NỘI BỘ`; đừng gỡ nhãn đó đi.
- **`so the vs so chuong`** — số thẻ `.card` trên trang so với số chương parse
  được. CHẶN nếu lệch.
- **`tieu de lac trong than chuong`** — điều kiện CẤU TRÚC, không phải ngưỡng
  thống kê: CHẶN nếu khác 0. Hàng này thay cho một tỉ lệ (chương cuối / trung
  vị) đã thử và KHÔNG tách được: lỗi EOF-overrun thật đo được **1.49× trung
  vị**, nằm GIỮA hai chương cuối dài thật đo được **1.48×** và **1.61×** — không
  ngưỡng nào trên tỉ lệ đó tách được cả ba ca. Cảm biến cấu trúc không có vùng
  xám, không cần ngưỡng.
- **`so do the vs nguon`** · **`chuong cuoi / trung vi`** — chỉ cảnh báo
  (`canh-bao`), không chặn. `chuong cuoi / trung vi` (ngưỡng 1.8×) chỉ còn bắt
  hình dạng dàn bài lỏng; vai trò bắt EOF-overrun đã chuyển hẳn cho dòng
  `tieu de lac trong than chuong` ở trên.
- **`so chuong trung`** khác 0 ⇒ sách có hai chương cùng số. Cảnh báo, không
  chặn — nói con số cho CEO, đừng tự chọn giữ chương nào.

## Sửa ở đâu

Bản đồ là **hiện vật dựng ra**. Vá thẳng vào `*-map.html` thì lần dựng sau xoá
sạch. Mọi sửa phải vào `book.md` hoặc vào `scripts/md_to_html.py`.

Chân trang in sha256 của `book.md`. Lệch sha ⇒ bản đồ đã cũ, dựng lại.
