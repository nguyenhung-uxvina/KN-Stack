# Nạp Nguồn — Dựng Kho Ngữ Liệu Đối Chiếu Được

> Đọc ở P0/P1. Mọi phép đo về sau đứng trên kho này; kho sai thì con số đẹp cũng vô nghĩa.

## Nguyên tắc đầu tiên

**Có tệp gốc trong tay thì đừng đi vòng qua NotebookLM.** Đã đo: kiểm qua `nlm notebook query` chỉ
đối chiếu được 19 mệnh đề, và gặp ca `sources_used: 1` nhưng `cited_text` kéo về Lời nói đầu trong
khi phần trả lời vẫn viết *"câu nguyên văn ở Chương 6 là…"* rồi in câu ấy trong ngoặc kép.
`sources_used > 0` **không phải bằng chứng**. Đọc PDF thẳng thì có luôn cả 629 trang.

## Lệnh

```bash
python skills/book/book-to-book/scripts/source_ingest.py "<tệp>" \
  -o "<output_dir>" --label "<nhãn ngắn>" --offset auto
```

Sinh trong `<output_dir>/_source/`:

| tệp | dùng để làm gì |
|---|---|
| `<nhãn>.corpus.txt` | kho chuẩn hoá, nối liền một chuỗi — nền của mọi phép so |
| `<nhãn>.pagemap.json` | `[[vị trí ký tự, trang in], …]` — để trích dẫn trả được số trang |
| `<nhãn>.meta.json` | `words` (mẫu số của mọi tỷ lệ), `sha256`, số neo trang |

Chạy lại cho **từng** nguồn phụ, mỗi nguồn một nhãn.

## Theo định dạng

| Định dạng | Cách làm |
|---|---|
| `.pdf` có lớp text | Chạy thẳng. Đây là ca tốt nhất: có cả text lẫn số trang in |
| `.epub` | Chạy thẳng. Script đọc theo thứ tự spine của OPF. **Không có số trang in** — trích dẫn sẽ neo theo chương, nói rõ điều này với CEO |
| `.md` / `.txt` | Chạy thẳng |
| `.docx` `.pptx` `.xls` | `/doc-to-md` trước → nạp bản `.md` |
| PDF **scan** (ảnh) | Script dừng ở mã 2 khi đọc được <200 từ. OCR trước — xem `/doc-to-md` luật 6 (cổng phân loại trước khi bật OCR đám mây). **Sách quốc phòng/nội bộ không đẩy lên OCR đám mây** |
| PDF có DRM | Không mở được thì không có kho. Nói thẳng với CEO là **không đo được tỷ lệ nguyên bản**, đừng chạy tiếp rồi báo 0% |

## Số trang in — vì sao phải dò running header

Số trang PDF ≠ số trang in, và **độ lệch không đều**: đo trên Pahl & Beitz, lệch +17 ở đầu sách rồi
+12 ở phần sau. Không có công thức; phải nội suy từ mốc gần nhất.

- `--offset auto` (mặc định): dò số ở dòng đầu/dòng cuối mỗi trang, chỉ nhận neo **tiến đều** so với
  neo trước (chặn số trong bảng biểu), rồi nội suy cho trang không có header.
- `--offset N`: dùng khi đã **kiểm tay 3–4 mốc** và thấy lệch đều. Nhanh và chắc hơn auto.
- Trang mở chương thường không có running header → luôn là trang nội suy. Đừng tra bảng bằng phép
  tìm khớp chính xác: nó trả khớp nhầm từ phần đầu sách (đã báo sai một lần vì lỗi này).

Script in tỷ lệ neo dò được. **Dưới 30% thì cảnh báo** — lúc đó số trang là *suy ra*, không phải
*đọc được*; kiểm tay vài mốc trước khi để trích dẫn mang số trang ra ngoài.

## Bốn nguồn âm tính giả — sửa hết mới đọc được kết quả

Hàm `norm()` xử cả bốn. Ghi lại đây vì mỗi lần ai đó viết một script đối chiếu mới là một lần
chúng quay về.

1. **Ngắt từ bằng gạch nối + xuống dòng** (`de-\nsign`). Phải gỡ gạch nối **trước** khi gộp khoảng
   trắng. Gỡ gạch mà để xuống dòng thành dấu cách → `de sign` → trượt. Một mình lỗi này sinh 3 ca
   "không tìm thấy" hoàn toàn giả.
2. **Câu vắt qua chỗ ngắt trang.** Dò theo *từng trang* thì trượt. Vì thế kho được **nối liền** và
   running header bị gỡ — không gỡ thì số trang chèn vào giữa câu.
3. **Chú thích hình chèn vào giữa câu.** Ca nặng nhất đã gặp: `…fulfils exactly one` │
   `Figure 9.33. Product architecture` │ *(sang trang)* `subfunction.` — vắt trang **và** bị chú
   thích cắt. Cách chữa: dò theo cửa sổ đầu câu (60% số từ) khi khớp nguyên chuỗi trượt.
4. **Ligature `ﬁ ﬂ`**, nháy cong, gạch ngang unicode, non-breaking space, ký hiệu hạ chỉ, dấu nhấn
   Markdown, và **dấu lược `…`** trong trích dẫn. Dấu lược phải cắt trích thành mảnh rồi kiểm từng
   mảnh — không xử thì báo "18 câu sai" trong khi 16/18 là thật.

Đo trên P&B 629 trang: **43 ca trượt lượt đầu → 36 là giả** (ngắt trang/dấu lược), 4 do regex cắt
ngang bảng, 3 soi tay thì đều CÓ. Không sửa bốn nguồn trên thì báo cáo "7% sai" trong khi thật là 0%.

**Điểm thứ năm, riêng của kho tiếng Việt:** chuẩn hoá kiểu cũ `re.sub(r"[^a-z0-9]+", " ", s)` nghiền
nát chữ có dấu và cho âm tính giả im lặng. `norm()` ở đây giữ dải Unicode tiếng Việt. Cùng họ với
chuyện `grep` mặc định không khớp tiếng Việt có dấu: Galaxy ra 0/246 kết quả, đặt `LC_ALL=C.UTF-8`
thì ra 8 — và kết quả rỗng đọc y hệt "không có gì".

## Vì sao cần nguồn thứ hai (`--source2`)

Kho **một cuốn** báo NOT-FOUND cho mọi trích hợp lệ mà tác giả dẫn lại từ sách khác → dương tính giả
hàng loạt, và thường rơi đúng vào chương nặng lý thuyết nhất. Cross dẫn Pahl & Beitz ở Ch.10; không
nạp P&B thì cổng kêu oan cả chương.

Nạp nguồn phụ khi: sách gốc trích nhiều từ một tác phẩm nền · đang viết sách so sánh hai tác giả ·
hoặc lượt đo đầu cho một cụm NOT-FOUND tụ vào một chương — đó gần như luôn là dấu hiệu thiếu nguồn,
không phải dấu hiệu bịa.

## Kiểm kho trước khi tin

Ba phép rẻ, làm ngay sau khi nạp:

1. **Số từ có hợp lý không?** Sách 220 trang ra 60k từ là bình thường; ra 5k từ nghĩa là nửa cuốn
   không có lớp text.
2. **Lấy một câu bất kỳ ở giữa sách, tìm trong kho.** Không thấy → chuẩn hoá đang hỏng, không phải
   sách hỏng.
3. **Lấy một câu tự bịa, tìm trong kho.** Thấy → phép tìm đang quá lỏng. Luôn thử **hai chiều**;
   một mẫu thật phải đỗ, một mẫu bịa phải trượt.

Phép thứ ba là phép hay bị bỏ qua nhất và là phép bắt được nhiều bug nhất.

## Đếm là phép kiểm rẻ nhất và sắc nhất

Nếu sách phái sinh (hoặc chính sách gốc) tự khai một con số — "từ X xuất hiện 0 lần trong 566
trang", "dẫn mã [x.y] 277 lần" — thì **kiểm số trước, kiểm chữ sau**. Một lần xuất hiện là cả sợi
lập luận sụp.

Nhưng: **con số tự khai chỉ kiểm lại được khi quy ước đếm cũng được khai.** Một tập khai "277 lần";
đếm bằng regex đơn ra 214, tách ngoặc gộp ra 371, đếm cặp ngoặc ra 278 — khớp. Tập đó đếm cặp ngoặc
mà không nói. Suýt báo sai "khai khống 63 lần". **Đòi quy ước đếm trước khi kết luận sai số.**
