---
name: book-to-book
description: "Orchestrator biến MỘT CUỐN SÁCH CÓ SẴN (PDF/EPUB/DOCX/MD) thành sách phái sinh tiếng Việt để CEO tham khảo và học tập NỘI BỘ — không phát hành ra ngoài. Nâng cấp của notebook-to-book: đọc thẳng tệp gốc thay vì hỏi NotebookLM, nên mọi trích dẫn đối chiếu được và tỷ lệ nguyên bản ĐO ĐƯỢC bằng máy. Tuỳ chọn trung tâm: --fidelity F1 lược thuật | F2 diễn giải ứng dụng | F3 trung thành theo chương | F4 sát nguyên bản. Pipeline 10 pha: P0 cổng nguyên bản+phạm vi → P1 nạp nguồn → P2 định vị → P3 dàn ý → P4 viết → P5 rà soát → P6 hiệu chỉnh → P7 cổng nguyên bản đo bằng máy → P7.5 EPUB → P8 NLM (khoá theo mức) → P9 insight CEO. Triggers on: 'book to book', 'sách thành sách', 'biến sách thành sách', 'derive book', 'sách phái sinh', 'tóm tắt cuốn sách thành sách', 'dịch sách nội bộ', 'b2b book', 'đọc sách này rồi viết lại cho tôi'."
---

# Book-to-Book — Sách Gốc → Sách Phái Sinh Nội Bộ (10 pha)

> **Vai trò:** Chỉ huy trưởng — đường ống 10 pha, mở bằng một cổng và đóng bằng một phép đo
> **Cha:** Bản nâng cấp của `notebook-to-book`; P2–P6, P9 dùng lại nguyên các block `book-*`
> **Nguồn:** Một (hoặc vài) tệp sách: `.pdf` `.epub` `.md` `.txt` — **tệp thật, không phải notebook**
> **Đích:** Sách tiếng Việt cho CEO đọc và học **nội bộ**. Không phát hành ra ngoài. Không thương mại.

## Khác `notebook-to-book` ở đâu

Một câu: **cuốn này đọc sách, cuốn kia đọc bản tóm tắt của một chatbot về sách.**

| | notebook-to-book | book-to-book |
|---|---|---|
| Nguồn P1 | Truy vấn NotebookLM | Đọc thẳng tệp gốc → kho ngữ liệu chuẩn hoá |
| Trích dẫn | Không đối chiếu được (đo thật: **18/378 trích sai chữ hoặc bịa**) | Đối chiếu từng câu với kho gốc, trả **số trang in** |
| Tỷ lệ nguyên bản | Biết ở cuối, sau khi viết xong (Cross: **16,07%**) | **Khai ở P0, đo bằng máy ở P7**, vượt trần thì chặn |
| Phạm vi phát hành | *Giả định* của đường ống, treo đến hết dự án | **Quyết định có chữ ký ở P0**, máy kiểm |
| Mức nguyên bản | Không có khái niệm — ra bao nhiêu biết bấy nhiêu | `--fidelity F1..F4`, mỗi mức một trần và một cách viết |
| NLM | Bắt buộc, là nguồn | Tuỳ chọn, chỉ là **ống kính phụ**, không bao giờ là nguồn trích |
| Dấu bản | Không | Mọi tệp mang dấu `BẢN NỘI BỘ`, máy kiểm |

> ✅ **Cổng đã đối chứng trên cuốn thật.** Chạy lại `fidelity_audit.py` trên chính
> `cross-design-methods` (18 chương, 151.633 từ, hai nguồn Cross + P&B): ra **9.581 từ nguyên văn ·
> bao phủ 15,98%** so với **9.606 từ · 16,07%** đo tay bằng một đường công cụ khác. Lệch 0,09 điểm
> phần trăm. Con số này không phải ước lượng của model.
>
> 🔴 **Vì sao đảo thứ tự.** Lần chạy Cross 5e (2026-09-07) ra 18 chương/159k từ rồi mới đo được
> trích nguyên văn **9.606 từ = 16,07% toàn bộ sách gốc** — đủ dùng nội bộ, không đứng được nếu
> phát hành. Con số ấy quyết định cuốn sách **dùng được ở đâu**, mà nó chỉ xuất hiện khi mọi chữ
> đã viết xong. Ở đây nó được khai trước và đo suốt.

## Bốn mức nguyên bản

`--fidelity` là tuỳ chọn trung tâm của skill này. Nó quyết định **cách viết ở P4** và **trần ở P7**.

| Mức | Tên | Là cái gì | Dàn ý | Trần bao phủ¹ | Trần mật độ² | Độ dài / sách gốc |
|:--:|---|---|---|:--:|:--:|:--:|
| **F1** | Lược thuật | Bản rút gọn để CEO đọc trong 1–2 giờ; lập luận của mình, sách là nguyên liệu | Tự do hoàn toàn | 2% | 3% | 10–20% |
| **F2** | Diễn giải ứng dụng | Chuyển hoá vào bối cảnh Xưởng X: mỗi ý gốc đi kèm "vậy ở ta thì sao" | Tự do, bám luận đề riêng | 8% | 10% | 50–150% |
| **F3** | Trung thành theo chương | Bám sát trình tự lập luận của tác giả, giữ ví dụ gốc, thêm chú giải | Ánh xạ 1-1 với mục lục gốc | 20% | 25% | 60–120% |
| **F4** | Sát nguyên bản | Bản dịch/diễn đạt sát từng đoạn. **Là bản sao dịch của tác phẩm** | Y nguyên gốc | — (mù, xem dưới) | — | 90–110% |

¹ **bao phủ** = từ nguyên văn ÷ **từ sách gốc** → *tôi tái tạo bao nhiêu phần của người ta* (câu hỏi bản quyền).
² **mật độ** = từ nguyên văn ÷ **từ sách mình** → *bao nhiêu phần sách này không phải của tôi* (câu hỏi đóng góp).

**Hiệu chỉnh trên số thật, không phải ước lượng:** cuốn Cross đo được bao phủ 16,07% · mật độ 6,0%
→ nó là **F3 xét bao phủ nhưng F2 xét mật độ**. Hai thước đo lệch nhau như vậy là bình thường:
sách phái sinh càng dài thì mật độ càng loãng trong khi bao phủ vẫn tăng. **Bao phủ là thước ràng
buộc cho sách dài, mật độ cho sách ngắn.** Trần trong bảng đặt để cả hai cùng phải đạt.

### 🔴 F4 và vùng mù của phép đo

Ở F4 cảm biến **không đo được gì có nghĩa**: bản dịch tiếng Việt tái tạo ~100% tác phẩm gốc theo
thiết kế, nhưng nó không khớp chuỗi với bản gốc tiếng Anh, nên máy trả số thấp — và **số thấp ấy là
MÙ, không phải sạch**. Hệ quả thực hành:

- F4 được cai trị bằng **khai báo + khoá phát tán**, không bằng con số. Khai báo P0 bắt buộc mang
  dòng `khoá phát tán: máy CEO + vault, KHÔNG TẢI LÊN dịch vụ ngoài` — máy kiểm dòng này.
- **P8 mặc định TẮT ở F3/F4.** Nạp sách lên NotebookLM là gửi bản dịch cho bên thứ ba; ở mức tái tạo
  phần lớn tác phẩm thì đó là một hành vi phát tán, không phải một bước kỹ thuật.
- Chọn F4 khi và chỉ khi mục đích là **đọc hiểu chính xác lời tác giả**. Nếu mục đích là *dùng được*
  thì F2 cho giá trị cao hơn với rủi ro thấp hơn nhiều.

Chi tiết từng mức đổi cách làm ở từng pha ra sao: `references/fidelity-levels.md`.

## Dùng

```bash
# Mặc định: F2, tiếng Việt, dual audience
/book-to-book "D:\Workshop_X\3_Resources\Books & Articles\cuon-sach.pdf"

# Lược thuật nhanh để quyết có nên đọc cả cuốn không
/book-to-book "<đường dẫn>" --fidelity F1 --quick

# Trung thành theo chương, có sách nền thứ hai để khỏi báo dương tính giả
/book-to-book "<đường dẫn>" --fidelity F3 --source2 "<sách nền>.pdf"

# Sát nguyên bản, khoá trên máy
/book-to-book "<đường dẫn>" --fidelity F4 --no-nlm

# Chạy tiếp từ một pha
/book-to-book "<đường dẫn>" --from P4
```

### Cờ

```
--fidelity F1|F2|F3|F4   mức nguyên bản (mặc định F2) — quyết định cách viết + trần đo
--source2 <path>         nguồn thứ hai; lặp được. Sách nền mà tác giả trích lại
--offset auto|N          trang in = trang pdf − N; 'auto' dò running header (mặc định)
--min-run N              số từ liên tiếp tính là nguyên văn ở P7 (mặc định 10)
--nlm-lens               thêm NLM làm ống kính phụ ở P1 (KHÔNG phải nguồn trích)
--slug <tên>             ghi đè slug thư mục
--lang vi|en             mặc định vi
--audience leader|engineer|both   mặc định both
--deep / --quick         thêm/bớt độ sâu ở P1 và P4 · --quick bỏ P5/P6
--no-nlm                 bỏ P8/P9
--from Px / --only Px    chạy tiếp / chạy đúng một pha
```

**Không có cờ `--scope`.** Skill này chỉ sinh bản nội bộ. Muốn phát hành ra ngoài thì đó là một
quyết định khác, đo lại ở trần khác, người quyết là CEO — không phải một cờ dòng lệnh.

## Kiến trúc

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                    book-to-book (ĐIỀU PHỐI — 10 pha)                               │
│                                                                                     │
│ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌─────┐ ┌────┐ ┌────┐    │
│ │ P0 │▶│ P1 │▶│ P2 │▶│ P3 │▶│ P4 │▶│ P5 │▶│ P6 │▶│ P7 │▶│P7.5 │▶│ P8 │▶│ P9 │    │
│ │CỔNG│ │NẠP │ │ĐỊNH│ │DÀN │ │VIẾT│ │RÀ  │ │HIỆU│ │CỔNG│ │EPUB │ │NLM │ │CEO │    │
│ │MỨC+│ │NGUỒN│ │VỊ  │ │Ý   │ │ N× │ │SOÁT│ │CHỈNH│ │ĐO  │ │tuỳ  │ │khoá│ │INS │    │
│ │PHẠM│ │+đọc│ │    │ │    │ │    │ │2-3×│ │    │ │MÁY │ │chọn │ │mức │ │IGHT│    │
│ │ VI │ │    │ │    │ │    │ │    │ │    │ │    │ │🔒  │ │     │ │    │ │    │    │
│ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └─┬──┘ └──┬──┘ └─┬──┘ └─┬──┘    │
│   CORE   O      CORE   CORE   O      O      O      CORE    CORE   CORE  CORE      │
└────────────────────────────────────────────────────────────────────────────────────┘

Data Bus: D:\Workshop_X\3_Resources\Books\<slug>\   (trong vault)
          hoặc <cwd>/book-output/<slug>/            (ngoài vault)
Sổ:       <output_dir>/_pipeline_state.md
Khai báo: <output_dir>/_scope_decision.md      ← P0 sinh, P7 đọc, không có thì không đo được
```

---

## P0 — Cổng Mức Nguyên Bản & Phạm Vi (CHẶN, CEO Core)

Pha này tồn tại vì một lỗi cụ thể: lần chạy trước kết thúc với phạm vi phát hành **vẫn treo**, vì
không bước nào *bắt* phải chốt. "Nội bộ" là giả định mặc định của đường ống chứ chưa ai quyết.

### P0.1 — Nạp nguồn thử và trình số thật

Trước khi hỏi CEO bất cứ điều gì, chạy:

```bash
python skills/book/book-to-book/scripts/source_ingest.py "<tệp gốc>" \
  -o "<output_dir>" --label "<nhãn>" --offset auto
```

Script in ra **số từ của sách gốc** — mẫu số của mọi tỷ lệ về sau — và tỷ lệ trang dò được running
header. Mã thoát 2 (bản scan, DRM, tệp rỗng) ⇒ **dừng**, chuyển `/doc-to-md` hoặc OCR rồi quay lại.
Không có kho ngữ liệu thì không có phép đo, và pipeline chạy tiếp sẽ báo 0% — mà 0% ở đó đọc y hệt
"sạch".

### P0.2 — Trình CEO

```
═══ P0 — CỔNG MỨC NGUYÊN BẢN & PHẠM VI ═══

Nguồn      : {{tên tệp}} · {{N}} trang · {{W}} từ đọc được
             neo trang in: {{k}}/{{N}} trang ({{pct}}%)
Nguồn phụ  : {{danh sách --source2 | không có}}
Slug       : {{slug}}          Data Bus: {{output_dir}}

MỤC ĐÍCH ĐÃ CỐ ĐỊNH CỦA SKILL NÀY:
  CEO tham khảo và học tập nội bộ · KHÔNG phát hành ra ngoài · KHÔNG thương mại

Chọn mức nguyên bản:
  (F1) Lược thuật          — trần bao phủ 2%  · sách ~{{W*0.15}} từ · đọc 1-2 giờ
  (F2) Diễn giải ứng dụng  — trần bao phủ 8%  · sách ~{{W*1.0}} từ  · [mặc định]
  (F3) Trung thành theo chương — trần 20%     · sách ~{{W*0.9}} từ  · P8 tắt mặc định
  (F4) Sát nguyên bản      — KHÔNG đo được    · sách ~{{W}} từ      · khoá trên máy

Hệ quả đi kèm mức đang chọn:
  - P4 viết theo lối: {{xem references/fidelity-levels.md}}
  - P7 sẽ CHẶN nếu vượt trần — không có đường vòng
  - {{nếu F3/F4}} P8 NotebookLM TẮT; bật là một quyết định phát tán riêng

CEO:
(1) ▶️ Chốt mức {{F?}} và ký — sinh _scope_decision.md, sang P1
(2) ⚙️ Đổi mức
(3) ⏸️ Dừng
═══════════════════════════════════════════════════
```

### P0.3 — Sinh `_scope_decision.md`

Chỉ sinh **sau khi CEO chọn**. Khuôn (máy đọc các dòng in đậm; gõ có dấu hay không đều được):

```markdown
---
type: scope-decision
book: <slug>
---

# Quyết định phạm vi — <tên sách phái sinh>

**mức nguyên bản: F2**
**phạm vi phát hành: NỘI BỘ** — CEO tham khảo và học tập, không phát hành ra ngoài
**khoá phát tán: máy CEO + vault, KHÔNG TẢI LÊN dịch vụ ngoài**   ← bắt buộc với F3/F4
**CEO ký ngày: YYYY-MM-DD**

## Nguồn
| nhãn | tệp | trang | từ | sha256 |
|---|---|---:|---:|---|

## Vì sao mức này
<2-4 câu: mục đích đọc là gì, vì sao mức cao hơn/thấp hơn không phục vụ mục đích đó>

## Hệ quả đã chấp nhận
- <ví dụ: P8 tắt, cuốn này không lên NotebookLM>
- <ví dụ: mọi tệp mang dấu BẢN NỘI BỘ>
```

> **Đổi mức giữa chừng được, nhưng phải viết lại vì sao.** `fidelity_audit.py` so lời khai với cờ
> đang chạy; hai bên lệch nhau thì nó dừng ở mã 2 chứ không lặng lẽ chạy theo cờ.

---

## P1 — Nạp Nguồn + Thăm Dò (thay `book-explore`)

### P1.1 — Kho ngữ liệu là sự thật nền

`source_ingest.py` đã chạy ở P0 sinh ra `_source/<nhãn>.corpus.txt` + `.pagemap.json` + `.meta.json`.
Chạy lại cho từng `--source2`. **Mỗi nguồn một nhãn.**

> Vì sao cần nguồn thứ hai: kho một cuốn báo NOT-FOUND cho **mọi** trích hợp lệ mà tác giả dẫn lại
> từ sách khác — dương tính giả hàng loạt. Cuốn Cross dẫn Pahl & Beitz ở Ch.10; không nạp P&B thì
> cổng kêu oan toàn bộ chương đó.

### P1.2 — Đọc cấu trúc, đề xuất cụm chủ đề

Đọc mục lục + phần mở/kết từ **chính tệp gốc** (không hỏi NLM). Rút ra:
- Mục lục gốc → `Phase1-Exploration/_source_toc.md` (bắt buộc ở F3/F4, là bản đồ ánh xạ chương)
- 5–10 cụm chủ đề, mỗi cụm độc lập đọc được
- Luận điểm bao trùm của tác giả, người đọc lý tưởng

Trình CEO **trước khi fan-out** (giống P1.2 của `notebook-to-book`).

### P1.3 — Fan-out đọc sâu

Mỗi cụm một agent đọc phần tương ứng trong kho ngữ liệu → `Phase1-Exploration/<cụm>_Exploration.md`,
schema y hệt `book-explore` để P2+ không cần biết nguồn là tệp hay notebook.

**Luật trích dẫn, áp từ P1 và không nới ở pha nào sau:**

- Chỉ được đóng ngoặc kép quanh chuỗi **chép từ kho ngữ liệu**, kèm số trang in.
- Không nhớ, không diễn đạt lại rồi đóng ngoặc. Đo thật: bỏ luật này thì 18/378 trích sai; áp luật
  thì 0/446 ở P4 và 0/389 ở P6.
- Câu tiếng Việt khẳng định *"tác giả cho rằng X"* mà không có trích neo hoặc số trang cũng là một
  khẳng định về nguồn — P7 liệt kê hết ra cho người đọc soi.

### P1.4 — `--nlm-lens` (tuỳ chọn)

NLM ở đây là **ống kính phụ, không bao giờ là nguồn trích**: chỉ dùng để hỏi câu tổng hợp ("chủ đề
xuyên suốt là gì") khi đã có tệp gốc mà vẫn muốn một góc nhìn thứ hai.
Không bao giờ lấy chuỗi từ NLM đưa vào ngoặc kép. Lý do: `sources_used > 0`
**không phải bằng chứng** — đã gặp ca `cited_text` kéo về Lời nói đầu trong khi phần trả lời viết
*"câu nguyên văn ở Chương 6 là…"* rồi in câu ấy trong ngoặc kép.

---

## P2–P6 — Giống `codebase-to-book`, có điều chỉnh theo mức

Gọi đúng các block: `/book-position` (P2) · `/book-outline` (P3) · `/book-write` (P4) ·
`/book-review` (P5) · `/book-revise` (P6). Ba chỗ khác:

**P3 — dàn ý phải mang bảng ánh xạ nguồn** (bắt buộc F3/F4, khuyến nghị F1/F2):

| Chương phái sinh | Chương gốc | Trang in | Ghi chú lệch |
|---|---|---|---|

Bảng này là thứ duy nhất về sau trả lời được câu *"có phải mình chép cấu trúc không"* — mà không
phép so chuỗi nào bắt được chuyện đó.

**P4 — ngân sách trích cho từng chương.** Chia trần toàn sách cho số chương rồi phát cho agent viết
dưới dạng **số từ cụ thể**, không phải lời khuyên "trích ít thôi". Ở Cross, 4 chương gánh 38,5%
tổng lượng trích trong khi 14 chương còn lại chia phần còn lại — không có ngân sách thì lượng trích
dồn cục chứ không trải đều.

**P4 — liều lượng của chính chỉ thị.** Một câu trích đặt vào bản chỉ dẫn làm cơ chế chặn đã thành
phản xạ dán, lặp 16/18 chương. Chỉ thị nào cũng có liều; đặt xong thì P5 phải soi xem nó có bị dán
máy móc không.

**P6 — sửa tại chỗ thì phải để lại danh sách thay đổi** (`Phase6-Revise.md`, diff đo bằng máy).

---

## P7 — Cổng Nguyên Bản (CHẶN, đo bằng máy, CEO Core)

Đây là pha có sức nặng nhất của skill này. Chạy **hai** thứ, theo thứ tự:

```bash
# 1. Cổng Data Bus — có hiện vật thì mới được báo xong
python skills/book/codebase-to-book/scripts/databus_check.py "<output_dir>" --phase P6

# 2. Cổng nguyên bản — đo thật, ghi Phase7-Fidelity-Report.md, ra phán quyết
python skills/book/book-to-book/scripts/fidelity_audit.py "<output_dir>" \
  --level F2 --min-run 10 --nguon "Cross,Nigel Cross,Pahl & Beitz"
```

Mã thoát:

| mã | nghĩa | được làm gì |
|:--:|---|---|
| 0 | ĐẠT | trình CEO checkpoint P7 |
| 1 | KHÔNG ĐẠT — vượt trần / trích bịa / thiếu dấu nội bộ | **CẤM** trình checkpoint; sửa rồi chạy lại |
| 2 | KHÔNG ĐO ĐƯỢC — thiếu khai báo / thiếu kho / không thấy bản thảo | **CẤM**; mã 2 **không phải "sạch"** |

Sau đó chạy `/book-audit` (nhãn IP SAFE/REVIEW/SENSITIVE theo chương, quét nhãn mật, hợp `book.md`).
Hai cổng soi hai trục **độc lập nhau**: ở Cross, hai chương an toàn nhất về nhãn mật lại là hai
chương trích nhiều nhất.

### Vượt trần thì làm gì

Theo thứ tự rẻ → đắt:
1. **Cắt trích dài.** Ở Cross, cắt 33 trích ≥40 từ hạ ~1.400 từ → 16,07% xuống ~13,7%. Không trích
   nào quá dài (dài nhất 59 từ) — vấn đề luôn là **tổng lượng**, không phải một câu cá biệt.
2. **Đổi trích thành diễn giải + số trang.** Giữ được sức nặng học thuật, bỏ được lượng.
3. **Đóng ngoặc cho đoạn đang chép trần.** Không hạ được số, nhưng biến một đoạn đạo văn im lặng
   thành một trích dẫn có nguồn — đây là việc phải làm dù có vượt trần hay không.
4. **Khai lại mức ở P0** kèm lý do. Hợp lệ, nhưng là quyết định của CEO chứ không phải cách chữa
   mặc định — nếu lần nào cũng nới trần thì trần không còn là trần.

### Checkpoint P7

Dán **nguyên văn** khối phán quyết của script vào checkpoint, kèm hai con số bao phủ/mật độ và mục
"CỔNG NÀY KHÔNG NHÌN THẤY GÌ". CEO ký IP trên số thật, không trên lời tóm tắt.

---

## P7.5 — EPUB (tuỳ chọn, CEO quyết, không chặn P8)

Điều kiện vào: `fidelity_audit.py --verify` trả 0 — nghĩa là báo cáo P7 **còn đúng với bản thảo hiện
tại**, không phải một báo cáo cũ từ trước lần sửa gần nhất.

```bash
python skills/book/book-to-book/scripts/fidelity_audit.py "<output_dir>" --level F2 --verify
python D:/KN-Stack/scripts/md_to_epub.py "<output_dir>/book.md" \
  -o "<output_dir>/<slug>.epub" --split-level 1 --lang vi
```

- `--split-level 1` bắt buộc: `book.md` dùng H1 cho cả phần lẫn chương.
- Đọc bảng nghiệm thu: `tham chieu gay` = 0 · `mermaid sot` = 0 · `chu thich an` khác 0 thì **nói
  con số đó cho CEO trước khi tệp rời máy** — EPUB là zip chứa HTML, mọi `<!-- … -->` đi thẳng vào
  bản xuất và ai giải nén cũng đọc được.
- **Dấu `BẢN NỘI BỘ` phải có trong siêu dữ liệu EPUB, không chỉ trong thân sách.** Đổi định dạng
  không phải một quyết định phát hành mới; phạm vi chốt ở P0 đi theo tệp.

---

## P7.6 — Bản đồ sách HTML (**tuỳ chọn, CEO quyết, không chặn pha sau**)

Ngay sau khi CEO ký duyệt IP ở P7 (và dù có chạy P7.5 EPUB hay không), **hỏi
CEO một câu** trước khi sang P8:

```
═══ P7.6 — BẢN ĐỒ SÁCH (tuỳ chọn) ═══
`book.md` đã hợp: {{N}} chương · {{W}} từ · {{M}} sơ đồ
Phạm vi đã chốt: {{scope}}  — trang HTML Ở LẠI TRÊN MÁY, không publish

CEO:
(1) ▶️ Dựng bản đồ — /book-map, một tệp HTML, offline tuyệt đối
(2) ⏭️ Bỏ qua      — sang pha sau
══════════════════════════════════════
```

Nếu chọn (1):

```bash
python D:/KN-Stack/scripts/md_to_html.py "<output_dir>"
```

- **Đọc bảng nghiệm thu trước khi báo xong.** `ty le phu` dưới **70% là CHẶN** —
  nghĩa là parser mất chương, không phải sách ngắn. `goi mang` · `the script` ·
  `chu thich html` phải bằng 0. `nhan pham vi` phải ≥ 1.
- **Không publish trang này.** Phạm vi đã chốt đi theo tệp; đổi định dạng không
  phải một quyết định phát hành mới.
- **Không chặn pha sau.** CEO bỏ qua thì ghi "P7.6 bỏ qua" vào ledger rồi đi tiếp.
  Chạy sau lúc nào cũng được bằng `/book-map <output_dir>`.

---

## P8 — NotebookLM (KHOÁ THEO MỨC)

| Mức | P8 | Vì sao |
|:--:|---|---|
| F1, F2 | Bật (mặc định) | Sách phần lớn là lời của mình; nạp lên là nạp tài sản của mình |
| F3 | **Tắt mặc định** — bật phải có dòng đồng ý riêng của CEO trong `_scope_decision.md` | Tái tạo phần lớn lập luận gốc |
| F4 | **Tắt.** Không có đường bật bằng cờ | Nạp bản dịch toàn cuốn lên dịch vụ bên thứ ba là phát tán |

Khi bật: chạy `/book-notebook` như thường, **notebook MỚI**, không bao giờ ghi vào notebook nguồn.
Manifest phải ghi rõ đã tải **bản nào** và kết quả tiền kiểm rò rỉ.

Bẫy NLM đã trả giá, đọc trước khi chạy P8:
- `nlm source add` **nói dối cả hai chiều** — báo lỗi mà vẫn tạo vỏ rỗng, và in `✓ Added` kèm đúng
  tên bài mà vẫn hỏng. Cảm biến đúng là `status` trong `source list -j` (2 = tốt, 3 = hỏng).
- Trần **300 nguồn/notebook** là cứng và im lặng.

---

## P9 — Insight CEO

`/book-ceo-insight` với 5 lăng kính (HELIX · FORGE · Galaxy · ACH · IP). Thêm một lăng kính riêng
của skill này:

**Lăng kính "cái gì chuyển được, cái gì không"** — với sách nước ngoài, phần chuyển thẳng sang Xưởng
X thường nhỏ hơn cảm giác khi đọc. Buộc phân loại từng bài học thành: *áp được ngay* · *áp được sau
khi sửa điều kiện* · *không áp được vì khác nền công nghiệp*. Nhóm thứ ba là nhóm hay bị bỏ quên và
là nhóm sinh ra quyết định sai đắt nhất.

---

## Data Bus

| Tệp | Ai ghi | Nội dung |
|---|---|---|
| `_scope_decision.md` | **P0** | Mức nguyên bản + phạm vi + chữ ký. P7 không đọc được thì không đo |
| `_source/<nhãn>.corpus.txt` | P0/P1 | Kho ngữ liệu chuẩn hoá — sự thật nền |
| `_source/<nhãn>.pagemap.json` | P0/P1 | Ánh xạ vị trí → trang in |
| `_source/<nhãn>.meta.json` | P0/P1 | Số từ gốc, sha256, số neo trang |
| `Phase1-Exploration/_source_toc.md` | P1 | Mục lục gốc (bắt buộc F3/F4) |
| `Phase1-Exploration/<cụm>_Exploration.md` | P1 | Thăm dò từng cụm |
| `Phase2-Positioning.md` … `Phase6-Revised/` | P2–P6 | Như `codebase-to-book` |
| `Phase7-Fidelity-Report.md` | **P7 script** | Số đo + phán quyết + khối ấn băm. Chỉ script ghi |
| `Phase7-Audit-Log.md` | P7 `/book-audit` | Nhãn IP theo chương |
| `book.md` | P7 | Bản hợp nhất, mang dấu nội bộ |
| `_pipeline_state.md` | mọi pha | Sổ + bảng tiến độ |

## Luật

- **⛔ MỘT PHA MỘT LƯỢT — DỪNG VÀ CHỜ.** Không bao giờ chạy 2+ pha trong một lượt.
- **⛔ KHÔNG CÓ `_scope_decision.md` THÌ KHÔNG VIẾT CHỮ NÀO.** P0 là cổng chặn, không phải thủ tục.
- **⛔ CỔNG DATA BUS — không có hiện vật thì không được báo xong.** `databus_check.py`, mã thoát
  khác 0 ⇒ **CẤM** trình checkpoint. Áp cho mọi pha, đặc biệt **P5 · P6 · P8** — ba pha dễ bị làm
  tại chỗ rồi báo xong.
- **⛔ CỔNG NGUYÊN BẢN — model không được tự chấm tỷ lệ.** `fidelity_audit.py` là nơi **duy nhất**
  ra phán quyết. Một con số do model tự ước lượng là một con số bịa có thiện chí.
- **Mã thoát 2 không phải "sạch".** Thiếu kho ngữ liệu / không thấy bản thảo / thiếu khai báo đều
  trả 0 vi phạm nếu cổng viết cẩu thả — và 0 ở đó đọc y hệt như đã kiểm xong.
- **Trích dẫn chỉ lấy từ kho ngữ liệu.** Không trích từ trí nhớ, không trích từ NLM.
- **Mọi tệp giao ra mang dấu `BẢN NỘI BỘ`** — kể cả siêu dữ liệu EPUB. Máy kiểm ở P7.
- **`--verify` trước P7.5/P8.** Sửa xong rồi mới đo mới có nghĩa; báo cáo cũ mang dấu ✅ tệ hơn
  không có báo cáo.
- **Sao lưu theo mốc phải có TÊN KHÁC NHAU, kèm giờ:**
  `cp -r <nguồn>/. "<đích>_$(date +%Y-%m-%d_%H%M)/"`. `cp -r` vào cùng một đích là **đồng bộ**, không
  phải sao lưu — nó huỷ trạng thái cũ.
- **Đóng băng thư mục là quy ước, không phải quyền hệ thống.** Không gì *ngăn* một agent pha trước
  ghi đè; chỉ ảnh chụp sha256 *phát hiện ra*. Trước khi dời bản đang dùng, kiểm còn agent nào sống.
- **Sửa bằng script nghịch đảo được thì hỏng vẫn cứu được; sửa bằng tay thì không.**
- **Đọc `references/fidelity-levels.md` TRƯỚC P4** — cách viết khác nhau hẳn giữa các mức.

## Phân loại COD

- Nạp nguồn, dựng kho ngữ liệu: Offload (O)
- **Chọn mức nguyên bản + ký phạm vi (P0): Core (C)** — không uỷ thác được, đây là quyết định pháp lý
- Bản đồ cụm chủ đề: Offload (O), CEO duyệt
- Luận đề P2 · dàn ý P3: **Core (C)**
- Viết, rà soát, hiệu chỉnh (P4–P6): Offload (O)
- **Ký IP sau khi đọc số đo P7: Core (C)**
- Quyết có xuất EPUB (P7.5) và có bật P8 hay không: **Core (C)**; thao tác chuyển định dạng: Offload
- Chọn insight hành động được (P9): **Core (C)**

## Tích hợp

```
book-to-book GỌI SCRIPT:
  - skills/book/book-to-book/scripts/source_ingest.py      (P0/P1)
  - skills/book/book-to-book/scripts/fidelity_audit.py     (P7, và --verify trước P7.5/P8)
  - skills/book/codebase-to-book/scripts/databus_check.py  (mọi pha)
  - scripts/md_to_epub.py                                  (P7.5)

book-to-book UỶ NHIỆM:
  - /book-position (P2) · /book-outline (P3) · /book-write (P4)
  - /book-review (P5) · /book-revise (P6) · /book-audit (P7 — nhãn IP)
  - /book-notebook (P8, khoá theo mức) · /book-ceo-insight (P9)
  - /doc-to-md — khi nguồn là .docx/.pptx/.xls hoặc bản scan cần OCR

book-to-book ĐỌC:
  - tệp sách gốc (sự thật nền) · --source2 (sách nền tác giả dẫn lại)

TIẾP THEO (CEO kích hoạt):
  - /galaxy-note   — chuyển bài học thành permanent note
  - /book-to-skill — nếu cuốn sách nên thành một skill chạy được
  - /mentor-board --add — nếu tác giả đáng thành một mentor thường trực
```

## Kiểm cổng

```bash
python scripts/test_book_to_book.py     # 35 phép thử, đột biến hai chiều
```

Mỗi phép thử đi theo cặp: một mẫu **thật phải đỗ**, một mẫu **bịa phải trượt**. Bốn nhánh trích dẫn
(thật · bịa · lược thật · nửa thật nửa bịa) từng bắt được bug ghép nhầm hai trích dẫn liền nhau.
Sửa script mà không chạy lại bộ này thì coi như chưa sửa.
