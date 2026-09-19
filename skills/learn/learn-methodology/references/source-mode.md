# Chế độ --source — học bám một cuốn sách hoặc một cụm sách

Không có `--source`, skill dạy **một chủ đề** bằng hiểu biết chung của AI. Có `--source`, skill dạy **cái sách nói**. Hai việc khác nhau, vì sách có thể định nghĩa khác, đếm khác, dùng số khác với "hiểu biết chung", và chỗ khác đó thường chính là phần đáng học.

Luật gốc: **câu nào nói "sách nói X" thì phải có X trong sách, và máy đã kiểm.** Phần AI tự nghĩ (phép so sánh, từ viết tắt, câu hỏi kiểm tra) vẫn được phép, nhưng phải mang nhãn và không được mượn uy tín của sách.

## S1 — Xác định nguồn

`--source` nhận một hoặc nhiều giá trị (lặp cờ cho cụm sách):

| Giá trị | Nhận ra bằng | Kho đối chiếu (`<KHO>`) |
|---|---|---|
| Tệp `.pdf` `.epub` `.md` `.txt` | có đuôi tệp | chính tệp đó |
| Thư mục | là thư mục | thư mục đó — ví dụ `BOOK/_source/` do `/book-to-learn` L2 sinh |
| Notebook NLM | id UUID hoặc alias (`btl-<slug>-goc`, `learn-<slug>`) | dump nguồn ra tệp — xem dưới |
| `.docx` `.pptx` | | chạy `/doc-to-md` trước, rồi dùng tệp `.md` |

**Notebook NLM** — script chỉ đọc được tệp, nên dump nội dung thô (không qua AI) trước khi dạy:

```bash
nlm source list <notebook> -j                         # lấy id + status từng nguồn
nlm source content <source-id> -o "<KHO>/<tên>.md"    # mỗi nguồn một tệp
```

`<KHO>` đặt trong thư mục làm việc tạm (scratchpad), không đặt trong vault. Nguồn nào `status` khác trạng thái sẵn sàng, hoặc tệp dump rỗng/ngắn bất thường, thì loại ra và báo — đừng tin dòng `✓ Added` hay tên nguồn: nguồn có thể mang đúng tên bài mà nội dung là trang chặn bot.

**Có cả tệp lẫn notebook** → đối chiếu bằng **tệp**. NLM là công cụ tìm, tệp là sự thật.

**Báo CEO trước khi dạy** (một khối, rồi chờ xác nhận):

```
NGUỒN: <n> tệp · <số từ> từ · phạm vi: <chương/khái niệm cần học>
<tệp PDF scan không lớp chữ / nguồn bị loại, nếu có>
```

PDF scan không có lớp chữ → dừng, đề nghị OCR. Không dạy "bám sách" trên một cuốn sách máy không đọc được.

## S2 — Lấy nội dung từ sách, không từ trí nhớ

Lấy đoạn sách cho từng khái niệm theo một trong hai đường:

- **Đọc thẳng** tệp (hoặc chương trong `_source/`) — ưu tiên khi phạm vi ≤ vài chương.
- **Hỏi NLM** khi sách dài hoặc cụm nhiều cuốn — để *tìm chỗ*, rồi vẫn phải chép trích dẫn từ **tệp**, không từ câu trả lời NLM. Câu hỏi mẫu: *"Sách nói gì về {khái niệm}? Trích nguyên văn đoạn liên quan, kèm tên nguồn."*

Khi dùng NLM, bốn điều đã trả giá:

1. **Không `chat_configure` với goal tuỳ chỉnh** — persona âm thầm tắt truy hồi nguồn: câu trả lời vẫn dài, trôi chảy, mà `sources_used` = 0.
2. **Mỗi câu hỏi một conversation mới.** Chỉ câu đầu của conversation là chắc có bám nguồn.
3. Câu trả lời có `sources_used` = 0 → bỏ, không dùng làm gì cả.
4. **Trích dẫn đúng không chứng minh đáp án đúng.** NLM có thể đưa đáp án lấy từ chỗ khác kèm một trích dẫn thật. Đối chiếu *nội dung* đáp án trong sách, không chỉ đoạn trích.

## S3 — Viết đầu ra theo quy ước nhãn

Mỗi dòng nội dung thuộc đúng một trong ba loại:

| Loại | Cách viết | Được dùng cho |
|---|---|---|
| **Sách nói** | `«trích nguyên văn»` — [nguồn, vị trí] | định nghĩa, luận điểm, con số, danh sách, thứ tự, điều kiện áp dụng |
| **Diễn giải** | viết thường, ngay sau trích dẫn nó diễn giải | nói lại trích dẫn cho dễ hiểu — không được thêm ý mới |
| **AI tự nghĩ** | `[AI]` ở đầu dòng | phép so sánh, từ viết tắt, câu hỏi kiểm tra, ví dụ Workshop X, liên hệ sang dự án |

Luật cho trích dẫn:

- **Nguyên văn**, ngôn ngữ gốc của sách. Sách tiếng Anh thì trích tiếng Anh; phần Diễn giải viết tiếng Việt.
- **5 từ trở lên** mỗi trích dẫn (ngắn hơn không chứng minh được gì). Lược bằng `[…]`; mỗi đoạn giữa các chỗ lược đều phải có trong sách.
- **Ngắn**: một câu, tối đa hai. Đây là tài liệu học nội bộ, không phải bản chép sách.
- **Mọi con số từ sách phải nằm trong «…»** — số không được đứng trần trong phần Diễn giải. Script chỉ kiểm được những gì nằm trong ngoặc.
- **Vị trí** lấy từ đầu ra của `quote_check.py` (`trang PDF n`, tên tệp chương), **không tự ghi số trang**: agent đọc văn bản trần thì không nhìn thấy số trang, và số trang đoán trông y hệt số trang thật. `trang PDF` là số thứ tự trang trong tệp, có thể lệch số trang in.

**Khi sách không nói về khái niệm cần học:**

```
KHOẢNG TRỐNG: <sách> không nói về <X>. (đã tìm: <các cách viết đã thử>)
```

Không lấp bằng hiểu biết chung. Trước khi ghi khoảng trống, thử ≥ 3 cách viết (từ đồng nghĩa, số ít/nhiều, thuật ngữ gốc tiếng Anh, viết tắt) — lần tìm hụt phần lớn là do tìm sai chữ, không phải do sách thiếu.

## S4 — Cổng máy

```bash
python <KN-Stack>/skills/learn/learn-methodology/scripts/quote_check.py <đầu ra.md> --nguon <KHO> [--nguon <KHO2> ...]
```

- **Mã 0** → mọi trích dẫn có trong sách. Dán dòng `Tổng:` vào cuối đầu ra.
- **Mã 1** → với từng dòng `KHÔNG THẤY`: mở sách, chép lại đúng nguyên văn; không tìm ra thì **xoá cả khẳng định** (không hạ nó thành Diễn giải — nó vẫn là một điều "sách nói" không có trong sách). `QUÁ NGẮN` → nới trích dẫn ra cho đủ câu. Chạy lại tới khi mã 0.
- **Mã 2** → không đo được (nguồn rỗng, không đọc được, PDF scan). Dừng, báo CEO. **Không** giao đầu ra với nhãn "bám sách".

Đầu ra chưa qua mã 0 không được gọi là "bám sách" ở bất cứ đâu.

Script bắt chữ, không bắt nghĩa: một trích dẫn thật đặt cạnh một Diễn giải xuyên tạc nó vẫn qua cổng. Phần đó do người học bắt — lý do mỗi kỹ thuật dưới đây đều bắt người học đọc lại trích dẫn.

## Từng kỹ thuật ở chế độ --source

**FEYNMAN**
- *Ý Cốt Lõi*: 1–3 trích dẫn là định nghĩa/luận điểm của sách, mỗi trích dẫn một câu Diễn giải kiểu học sinh lớp 10 hiểu được.
- *Phép so sánh*: `[AI]`. *Chỗ phép so sánh gãy*: phải trỏ vào một trích dẫn cho thấy sách nói khác phép so sánh ở đâu.
- *Câu hỏi kiểm tra*: `[AI]`, nhưng **đáp án của mỗi câu là một trích dẫn** trong sách. Câu nào sách không trả lời được thì bỏ — đó là câu hỏi về hiểu biết chung, không về sách.

**CHUNKING**
- Cụm đi theo **cấu trúc của sách** (chương, mục), không theo sơ đồ phụ thuộc AI tự dựng.
- Quan hệ phụ thuộc: cạnh nào sách tự nói ("xem chương 2", "dựa trên…") thì kèm trích dẫn; cạnh AI suy ra thì `[AI]`.
- Ghi riêng chỗ **thứ tự phụ thuộc khác thứ tự trình bày** của sách — người đọc theo thứ tự trang sẽ vấp ở đó.
- Bài kiểm tra mỗi cụm: trả lời được bằng một trích dẫn.

**MNEMONIC**
- *Cần Nhớ*: danh sách/trình tự **chép từ sách**, trong «…». **Số mục và thứ tự** phải khớp sách — thêm, bớt hay đảo một mục là mnemonic dạy sai sách.
- Từ viết tắt, câu gợi nhớ: `[AI]`.

**ARCHITECTURE**
- Pha học trỏ vào chương/trang của sách; tài liệu mỗi pha là phần của sách, không phải tài liệu ngoài.
- Tài liệu ngoài sách: `[AI]` và ghi rõ "ngoài sách".
- Mốc có bằng chứng: bằng chứng là việc làm được trên dự án thật, không phải "đọc xong chương".

## Cụm sách (nhiều --source)

- Mỗi trích dẫn ghi rõ của cuốn nào (vị trí script trả về đã có tên tệp).
- **Thêm mục bắt buộc `## Chỗ các nguồn khác nhau`**: cùng một khái niệm mà hai cuốn định nghĩa khác, đếm khác, dùng số khác, hoặc khuyên ngược nhau → đặt hai trích dẫn cạnh nhau, **không gộp thành một giọng**. Không có chỗ nào khác nhau thì ghi `Không thấy mâu thuẫn trong phạm vi <…>` — đừng bỏ mục.
- NLM hỏi trên notebook nhiều nguồn có xu hướng trộn các tác giả thành một câu trả lời. Hỏi riêng từng cuốn (*"Theo {tên nguồn}, …"*) khi cần so.

## Cuối đầu ra

```
NGUỒN: <danh sách tệp/notebook>
quote_check: Tổng: <k>/<n> thấy · 0 không thấy · 0 quá ngắn
KHOẢNG TRỐNG: <danh sách, hoặc "không có">
[AI]: <số dòng> dòng do AI tự nghĩ — kiểm lại trước khi dùng vào thiết kế
```
