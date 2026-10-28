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
   số hình, neo. Khuôn dàn ý **không nhất quán** giữa các cuốn — đo lại 2026-10-05
   trên 34 cuốn (số cũ "22/32" đã bị **rút lại**): **26/34** có heading `### `;
   bullet `- ` có mặt ở **488/521** chương (94%), và `usv-thiet-ke-he-thong` là
   cuốn LỆCH duy nhất chỉ dùng ở 13/28 — nên thiếu là chuyện thường, in `chưa đo`,
   đừng suy luận.
3. **Sinh mới** — ô tóm tắt 3–5 dòng. Nếu sách có `_book_map_digest.md`, in dòng
   digest (đã qua cổng neo — xem Tầng 3 dưới). Nếu không (32/34 cuốn hiện tại),
   in bullet của dàn ý — nhưng gắn nhãn tiếng Việt rõ "Từ dàn ý — CHƯA qua cổng
   neo" và một class CSS riêng (`summary-unanchored`) để không ai nhầm nó với một
   tóm tắt đã kiểm. Không còn dàn ý thì mới in `chưa tóm tắt`. Xem spec §1.2 và
   mục "Đọc bảng nghiệm thu" dưới.

## Tầng 3 — ô tóm tắt, việc của agent chứ không phải của script

Script **không sinh** tóm tắt. Khi người dùng gọi `/book-map` và sách chưa có
`_book_map_digest.md`, agent viết 3–5 dòng mỗi chương vào tệp đó. Mỗi mục hai
dòng: dòng đầu `## Ch.NN LNNN`, dòng sau là câu tóm tắt. `Ch.NN` là số chương;
`LNNN` là **số dòng trong `book.md`** nơi câu ấy có gốc.

Cách lấy nguyên liệu — đã đo lại trên toàn kho ngày 2026-10-05, khác với giả
định ban đầu: bullet của `Phase3-Outline.md` **có mặt ở hầu hết chương** (488/521
chương trên 34 cuốn, 94%) — không phải trường hợp hiếm. `usv-thiet-ke-he-thong`
(13/28) là cuốn LỆCH, không phải điển hình. Nhưng bullet đó dài 120–150 ký tự,
gộp nhiều mệnh đề và số trang trích dẫn — ví dụ *"Biên hệ thống không phải sự
thật về con tàu mà là **một lựa chọn**; đổi biên thì hàm phụ thành hàm chính và
ngược lại (tr.33)."* — nên nó là **tư liệu nguồn tốt**, không phải tóm tắt một-ý-
một-dòng đã xong việc. Vì vậy, khi viết digest:

- Chương **có** bullet dàn ý: đọc bullet, **chắt lại** thành 1 dòng ≤25 từ, một
  ý, rồi tự đi tìm số dòng gốc trong `book.md` khớp với ý đó.
- Chương **không có** bullet (hoặc bullet không đủ cho một ý rõ): đọc thẳng
  thân chương, chọn câu/đoạn mang quyết định hoặc hệ quả, rồi ghi số dòng của
  chính câu/đoạn đó.

Cả hai đường đều **đọc rồi viết lại bằng lời agent**, không copy-paste bullet
nguyên văn — một bullet 140 ký tự dán thẳng vào thường vi phạm trần 25 từ và
"một dòng một ý" ngay lập tức.

Ràng buộc viết — gọi là **STE 80%**, *không* gọi là ASD-STE100 (Dictionary của
chuẩn đó là tiếng Anh và có bản quyền ASD):

- Một dòng một ý. Tối đa **25 từ**.
- Thể chủ động. Chủ ngữ là vật hoặc người làm việc.
- Mỗi dòng kết bằng **một đại lượng, một quyết định, hoặc một hệ quả** — không
  kết bằng chủ đề.
- Một khái niệm **một tên** xuyên toàn bản đồ. Không luân phiên từ đồng nghĩa.
- Thuật ngữ kỹ thuật giữ nguyên tiếng Anh.

Cổng `tom tat vi pham STE` (`ste_lint`) chỉ **đo được BA trong năm** ràng buộc
trên — không phải cả năm:

- Dài hơn 25 từ.
- Hơn một câu trên một dòng.
- Thể bị động **có nêu chủ thể**: mẫu `được … bởi` / `bị … bởi`.

Nó **không** bắt được thể bị động không nêu chủ thể (`Biên được vẽ.` lọt qua
sạch), và không có cảm biến nào cho "một khái niệm một tên" hay "giữ thuật
ngữ gốc" — hai điều đó agent phải tự giữ khi viết, không có máy kiểm. Một
dòng có thể vụng theo cách không máy nào ở đây bắt được. Đừng đọc tên hàng
này rộng hơn cái nó đo.

**Cổng `neo tom tat sai` CHẶN.** Không neo được câu vào một dòng có thật trong
chương thì câu đó là bịa — bỏ nó đi, **đừng đổi số dòng cho lọt cổng**. Đây đúng
là lý do cổng tồn tại: ô tóm tắt là **bề mặt bịa đặt duy nhất** của cả tính
năng (mọi ô khác đều là số đo từ `book.md`), nên nó là ô duy nhất cần một cổng
kiểm chuyên biệt. Sửa một anchor sai bằng cách đổi `LNNN` cho tới khi cổng im
lặng là tự tay vô hiệu hoá chính cổng đó — nó biến "cổng kiểm được neo có thật"
thành "cổng kiểm được số nào đó nằm trong khoảng cho phép", hai thứ khác nhau
hoàn toàn.

Cổng `tom tat vi pham STE` chỉ **cảnh báo**, không chặn — một câu vụng (dài,
bị động có nêu chủ thể, hoặc hai ý một dòng) là vấn đề văn phong, không phải
bịa đặt; đừng lẫn hai cổng này vào nhau. Mất neo là mất sự thật, lỗi văn
phong không mất gì ngoài độ gọn.

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

Script in một bảng 12 phép đo cuối lượt chạy (cả khi dựng mới và khi `--verify`).
Dòng nào CHẶN thì script trả mã lỗi và in "CO DONG CHAN — khong giao tep nay."
(đúng chữ script in ra, không dấu):

- **`ty le phu`** — tổng số từ trong các chương chia cho `wc -w` của cả
  `book.md`. Dưới **70% là CHẶN**: nghĩa là parser mất chương, không phải sách
  ngắn. 70–85% là cảnh báo. **Sửa 2026-10-06 (F3):** câu "cảm biến duy nhất bắt
  đủ 5/5" ở bản trước chỉ đúng cho một phép **so sánh trước/sau** (phủ tụt ở cả
  5 cuốn khi lỗi khối mã được mô phỏng) — nó **sai** cho cổng `--verify` đã giao,
  vì cổng đó dùng một **ngưỡng tuyệt đối trên một lượt chạy**. Đo lại 5 cuốn đó
  với ngưỡng đã chọn: `tau-nhom-han-quoc-phong` 38,9% CHẶN, `pahl-beitz-tap2`
  40,1% CHẶN, `ai-at-war` 76,6% cảnh báo, `cross-design-methods` 94,0% ok (im
  lặng), `kien-truc-tu-hanh-hang-hai` 93,7% ok (im lặng) — chỉ 2/5 bị chặn, 2/5
  im lặng hoàn toàn. Hàng này bắt ca **nặng** (39–40%), cảnh báo ca **vừa**
  (77%), nhưng **không** bắt được ca **nhẹ** (94%) — và không ngưỡng tuyệt đối
  nào có thể, vì một mất 4% nằm dưới mọi sàn mà không đồng thời chặn nhầm sách
  hợp lệ gần nhất (76,1%). Hàng cấu trúc `tieu de lac trong than chuong` dưới
  đây mới bắt đúng cả năm ca này — giữa hai hàng: hàng này bắt mất NẶNG, hàng
  cấu trúc bắt lỗi CẤU TRÚC chính xác, không hàng nào một mình bắt được mất NHẸ.
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
- **`neo tom tat sai`** — CHẶN nếu khác 0, nhưng **chỉ đọc `_book_map_digest.md`**
  (không đọc bullet dàn ý). Mỗi dòng digest (tầng 3, xem mục trên) phải neo vào
  một số dòng nằm trong đúng chương nó khai. Đây là cổng của **bề mặt bịa đặt
  duy nhất** trong cả tính năng — không neo được là câu đó bịa, bỏ câu đó, đừng
  đổi số dòng. Bullet dàn ý không có số dòng gốc để neo, nên **không thể và
  không được** tính vào hàng này — thiếu neo ở đó không phải bịa đặt, chỉ là
  chưa kiểm (xem `tom tat vi pham STE` dưới).
- **`tom tat vi pham STE`** — chỉ cảnh báo, không chặn. **Sửa 2026-10-06 (F1):**
  trước đây hàng này chỉ đọc `_book_map_digest.md` — vì KHÔNG cuốn nào trong kho
  có tệp đó (0/34), hàng này luôn báo "sạch" trên đúng cái ô tóm tắt mà
  32/34 cuốn đang hiện ra (bullet dàn ý, chưa ai lint qua: ~1.402 dòng render,
  281 dòng trong số đó vượt trần 25 từ). Giờ hàng này đọc trực tiếp các dòng
  tóm tắt **đã render trên trang** — cả `summary-anchored` (digest) VÀ
  `summary-unanchored` (bullet) — và lint cả hai như nhau, đếm số dòng vi phạm
  MỘT TRONG BA điều máy đo được (dài hơn 25 từ, bị động có nêu chủ thể, hoặc hai
  ý một dòng) — xem "Tầng 3" ở trên để biết hai ràng buộc STE còn lại mà hàng
  này KHÔNG đo. Vụng văn không phải bịa đặt; đừng lẫn hàng này
  với `neo tom tat sai`.

## Sửa ở đâu

Bản đồ là **hiện vật dựng ra**. Vá thẳng vào `*-map.html` thì lần dựng sau xoá
sạch. Mọi sửa phải vào `book.md` hoặc vào `scripts/md_to_html.py`.

Chân trang in sha256 của `book.md`. Lệch sha ⇒ bản đồ đã cũ, dựng lại.
