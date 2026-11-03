---
created: 2026-10-03
updated: 2026-10-04
type: spec
status: da-duyet
tags: [#type/sop, #status/active, #topic/ai-tools]
---

# Spec — `/book-map`: bậc HTML tương tác cho sách đã dựng

> Trạng thái: **CEO ĐÃ DUYỆT 2026-10-04**. Chưa viết mã thật. Mọi con số trong tệp này đo
> ngày 2026-10-03 trên 32 cuốn có `book.md` tại `D:\Workshop_X\3_Resources\Books\`.
> Hiện vật thực nghiệm (`scratchpad/probe_book_map.py` + 6 trang HTML) là **bản thợ,
> bỏ đi** — không phải mã nguồn của skill.

## 1. Vì sao có spec này

Yêu cầu khởi đầu: áp chuẩn **ASD-STE100** (Simplified Technical English) vào ba
pipeline sách — `/codebase-to-book`, `/notebook-to-book`, `/book-to-book` — kèm
thang leo của Karpathy: văn rõ → sơ đồ → HTML tương tác → video.

Mục đích thật, CEO đã chốt: **CEO tự đọc lại sách của chính mình cho nhanh hiểu.**
Một người đọc, sách nội bộ, trên máy CEO.

### 1.1 Những gì BỊ LOẠI khỏi spec, và vì sao

| Bị loại | Lý do |
|---|---|
| **STE100 làm chuẩn văn toàn sách** | STE100 là chuẩn của **tiếng Anh** — lõi của nó là Dictionary từ-được-phép, không dịch sang tiếng Việt được. Sách mặc định `--lang vi`. Áp lên tiếng Việt = tự phát minh một chuẩn không có cơ quan bảo chứng. |
| **Nhãn tuân thủ "ASD-STE100"** | Dictionary có bản quyền ASD, không được phát hành lại ⇒ không nhúng được vào repo. In nhãn tuân thủ khi chỉ cài vài quy tắc đo được là **tuyên bố sai**. |
| **Viết lại văn sách theo STE** | Đụng trực diện `book-voice-and-style.md` (bắt buộc "direct và opinionated", "show the trade-offs") — STE thì cấm ẩn dụ, cấm từ đồng nghĩa, một câu một lệnh. Và một cổng đếm 20 từ/câu sẽ làm người viết **bẻ câu cho lọt cổng** thay vì viết cho đúng. |
| **Bậc video** | NLM `studio_create(video)` đẩy nội dung lên hạ tầng Google; Manim + ElevenLabs là một việc dựng thật. Tách spec riêng nếu còn muốn. |
| **Publish lên claude.ai** | Sách xếp ⛔ NỘI BỘ. Hiện vật **ở lại trên máy**. Đường publish để sau, như một lựa chọn hỏi từng lần qua cổng phạm vi. |

### 1.2 Chỗ STE100 THỰC SỰ vào hệ thống

**Ô tóm tắt 3–5 dòng trên mỗi thẻ chương** của bản đồ sách. Văn này **sinh mới**,
ngắn, một ý một câu. Không đụng văn sách ⇒ không có chuyện bẻ câu cho lọt cổng, và
không xung đột với `book-voice-and-style.md`.

Ràng buộc cho ô tóm tắt (gọi là **"STE 80%"**, không gọi là ASD-STE100):

- Một câu một ý. Tối đa **25 từ/câu**.
- Thể chủ động. Chủ ngữ là vật hoặc người làm việc, không phải "việc… được…".
- Mỗi câu kết bằng **một đại lượng, một quyết định, hoặc một hệ quả** — không kết bằng chủ đề.
- Không ẩn dụ, không từ đồng nghĩa luân phiên: một khái niệm **một tên** xuyên toàn bản đồ.
- Thuật ngữ kỹ thuật giữ nguyên tiếng Anh như `book-voice-and-style.md` đã quy định.

> Đây là **hạng mục công việc chính** của bậc A, không phải trang trí. Lý do ở §3.3:
> tóm tắt **không thu hoạch được** từ dàn ý.

## 2. Bối cảnh đo được

Mọi quyết định kiến trúc dưới đây dựa trên số đo, không dựa trên phỏng đoán.

### 2.1 Ba pipeline hội tụ về một chokepoint — nhưng spec này KHÔNG sửa nó

`book-write`, `book-review`, `book-revise` đều nạp
`skills/book/codebase-to-book/references/book-voice-and-style.md`. Sửa tệp đó đổi
hành vi cả 3 pipeline cùng lúc. **Spec này không sửa nó.** Bán kính ảnh hưởng co
lại còn: 2 tệp mới + 3 chỗ chèn pha tuỳ chọn.

### 2.2 Khuôn hiện vật KHÔNG nhất quán giữa các cuốn

| Dữ liệu | Có ở | Hệ quả thiết kế |
|---|---|---|
| tiêu đề chương trong `book.md` | **32/32** sau đường lùi (27 dùng H1, 5 dùng H2) | **xương chịu lực** |
| số từ · số sơ đồ · tham chiếu chéo | 32/32 (dẫn xuất từ `book.md`) | **xương chịu lực** |
| nhãn phạm vi trong **thân** `book.md` | **26** trong 28 cuốn không có tệp sidecar | **nguồn nhãn chính** |
| `_scope_decision.md` | **4/32** | nguồn phụ, KHÔNG phải nguồn chính |
| không khai phạm vi ở đâu | 2/32 | phải tự in nhãn bảo toàn |
| `### Ch.NN` trong `Phase3-Outline.md` | 22/32 | lớp làm giàu, suy thoái êm |
| mục `- ` dùng làm tóm tắt | **13/28 chương** ngay ở cuốn mẫu | **không dùng được** |
| dòng `Rủi ro:` + 🔴 | **3/32 cuốn** | thưởng, không phải tính năng |
| bảng xếp mức IP trong thân sách | **3/32 cuốn** | thưởng; P7 bản mới đã sinh ⇒ tự phủ dần |
| `inside-the-box` | **0 sơ đồ**, 2 cạnh phụ thuộc | trang phải **ẩn** mục, không in khung trống |

Dấu phân cách tiêu đề chương có **ba dạng**: `—`, `:`, `·`. Số chương có khi không
đệm 0 (`Chương 1`). Có cuốn dùng lẫn hai dấu trong cùng một sách (`finding-alphas`).

**Đo lại 2026-10-05 trên 34 cuốn (kho lớn hơn lúc viết bảng trên) — bốn dòng sau đã
bị RÚT LẠI, đừng trích số cũ:**

| Dòng cũ | Số cũ (2026-10-03, 32 cuốn) | Số đúng (2026-10-05, 34 cuốn) |
|---|---|---|
| tiêu đề chương | 27 H1 + 5 H2 | **29 H1 + 5 H2** |
| nhãn phạm vi trong thân | 26/28 (không sidecar) | **23 khai trong thân · 0 chỉ dựa sidecar · 11 không khai** |
| `_scope_decision.md` | 4/32 | **5/34**, cả 5 đều đã khai trong thân (không còn là nguồn duy nhất của cuốn nào) |
| CRLF | không có trong bảng, đo ở nơi khác là 4/32 | **3/34** |
| `### Ch.NN` trong `Phase3-Outline.md` | 22/32 | **26/34** |
| mục `- ` dùng làm tóm tắt | 13/28 chương (coi là điển hình) | **488/521 chương trên toàn kho (94%)** — `usv-thiet-ke-he-thong` (13/28) là cuốn LỆCH DUY NHẤT, không phải điển hình |

### 2.3 Ba lỗi parser đã tìm ra và vá trên bản thợ

Mỗi lỗi đi kèm phép đo chứng minh nó tồn tại và đã đóng.

| # | Lỗi | Bằng chứng | Luật đúng |
|---|---|---|---|
| L1 | Chương cuối chạy đến hết tệp ⇒ hút phụ lục + mục lục | `tu-khong-den-mot` Ch.19 **22.915 → 15.565** (trung vị 15.323); `ghi-de-quy-trach-nhiem` Ch.08 **6.267 → 3.653** | chương dừng ở tiêu đề kế tiếp, không dừng ở EOF |
| L2 | Luật dừng không được cố định theo mức heading | `principles-ba-tai-san` dùng **H2 cho cả chương lẫn tiểu mục** ⇒ bản vá L1 làm nó tụt còn **326 từ/chương** | `depth==1`: dừng ở H1 kế tiếp. `depth>1`: chỉ dừng ở tiêu đề **nông hơn**, hoặc ở chương kế tiếp |
| L3 | `#` trong khối mã bị đọc thành tiêu đề | `tau-nhom-han-quoc-phong` có `# 80% công việc…` trong sơ đồ ASCII | phải dựng **mặt nạ khối mã** (``` và ~~~) trước khi dò tiêu đề |

**L3 vỡ 5 cuốn, không phải 1:**

| Sách | Trước vá | Sau vá | Mất |
|---|---|---|---|
| `pahl-beitz-tap2` | 74.951 | **186.707** | **60%** |
| `tau-nhom-han-quoc-phong` | 37.005 | 93.386 | 61% |
| `ai-at-war` | 86.361 | 105.172 | 18% |
| `cross-design-methods` | 149.704 | 156.055 | 4% |
| `kien-truc-tu-hanh-hang-hai` | 79.476 | 84.823 | 6% |

Sau cả ba bản vá: **32/32 cuốn parse được, tỷ lệ phủ 76–100%**, không cuốn nào còn
dấu hiệu hỏng.

### 2.4 Bài học cảm biến — phần quan trọng nhất của mục 2

Ba bộ dò được dựng. Chỉ một bộ bắt được L3:

| Bộ dò | Bắt được L3 ở |
|---|---|
| trung vị từ/chương quá nhỏ (< 1.500) | **1/5 cuốn** |
| chương cuối phình > 1,5× trung vị | **0/5 cuốn** |
| **tỷ lệ phủ = Σ từ trong chương ÷ `wc -w` cả tệp** | **5/5 cuốn** |

`pahl-beitz-tap2` nằm ở **40% phủ** mà hai bộ đầu vẫn báo "sạch". Lý do: cả hai chỉ
so các chương **với nhau** — khi lỗi cắt vụn mọi chương đều đặn thì nội bộ trông
nhất quán. Bộ thứ ba so với **một tổng độc lập** nên miễn nhiễm.

⇒ **Bất biến BI-5 ở §5.** Cảm biến phải so với một tổng tính ngoài đường ống.

Ghi nhận một chỗ chủ quan: ngưỡng chương-cuối-phình được nới **1,5× → 1,8× sau khi
thấy dữ liệu**, vì `finding-alphas` ở 1,61× là chương kết dài thật. Đó là ngưỡng đặt
theo cảm giác, không theo phép đo. Nó là **cảnh báo**, không phải cổng chặn.

## 3. Kiến trúc

### 3.1 Hiện vật và chỗ đứng

| Thứ | Đường dẫn | Ghi chú |
|---|---|---|
| Bộ sinh | `scripts/md_to_html.py` | `import` lại từ `md_to_epub.py`: `strip_frontmatter`, `find_mermaid_blocks`, `count_html_comments`, `derive_title` cho bậc A; thêm `find_mmdc`, `render_diagrams` **chỉ khi làm bậc B**. **Không sửa một dòng** của `md_to_epub.py` — nó có `scripts/test_md_to_epub.py` đang xanh |
| Skill | `skills/ops/book-map/SKILL.md` | soi khuôn `skills/ops/md-to-epub/` |
| Test | `scripts/test_md_to_html.py` | bắt buộc, xem §7 |
| Chèn pha | **P7.6** ngay sau P7.5 trong `codebase-to-book`, `notebook-to-book`, `book-to-book` | ~15 dòng/tệp, đúng khuôn cổng CEO của P7.5/P8.5 |

Gọi được **hai đường**: trong pipeline như một pha tuỳ chọn, hoặc đứng riêng
`/book-map <đường-dẫn-thư-mục-sách>` cho **32 cuốn đã dựng xong**.

> Giá trị hồi tố này là lý do chính để làm bậc A: nó áp ngay cho 32 cuốn cũ, không
> chỉ cho lần chạy sau.

### 3.2 Công cụ — đã kiểm là có trên máy, không cần cài

`pandoc` ✅ · `mmdc` ✅ · `node`/`npm` ✅ ·
`mermaid.min.js` **có sẵn offline** tại
`%APPDATA%\npm\node_modules\@mermaid-js\mermaid-cli\node_modules\mermaid\dist\mermaid.min.js`
(3,5 MB). Nghĩa là sơ đồ sống pan/zoom làm được mà **không gọi CDN**.

### 3.3 Ba tầng dữ liệu

**Tầng 1 — xương, bắt buộc, dẫn xuất 100% từ `book.md`.** Thiếu tầng này thì dừng,
không sinh trang.

- danh sách chương + tên chương (lấy từ chính dòng tiêu đề)
- số từ mỗi chương — **`LC_ALL=C.UTF-8`**, không chế độ byte (chế độ byte thổi phồng
  +2,9% trên cuốn mẫu: 264.885 so với 257.450)
- số sơ đồ mermaid mỗi chương
- đồ thị tham chiếu chéo giữa các chương
- nhãn phạm vi phát hành, đọc từ **thân sách** (§4)

**Tầng 2 — làm giàu, suy thoái êm.** Thiếu thì in `chưa đo`, **không bịa, không suy
luận**.

- số từ đặt ra cho mỗi chương (từ `Phase3-Outline.md`) ⇒ tính độ lệch
- dòng `Rủi ro:` + cờ 🔴
- số hình đặt ra
- neo N1/N2/N3
- mức IP từng chương, **chỉ khi** thân sách có bảng `Xếp mức IP theo chương` ở dạng
  đọc được bằng máy

**Tầng 3 — sinh mới.** Ô tóm tắt STE 80% (§1.2). Đây là phần việc của agent, không
phải của parser.

### 3.4 Vì sao mức IP từng chương KHÔNG được dò bằng từ khoá

`Phase7-Audit-Log.md` của `usv-thiet-ke-he-thong` xếp mức trong **văn xuôi**, và hai
agent **không đồng ý nhau**: IP-B xếp Ch.07·09·10·12·13 là SAFE, IP-A xếp cả năm là
SENSITIVE; bản hợp nhất ra 28/28 SENSITIVE mà chính log gọi là **"thoái hoá"**.

Dán badge "SAFE/REVIEW" bằng cách dò từ khoá sẽ lặp lại đúng lớp lỗi đã trả giá:
**đặt tên cột theo thứ mình muốn nó đo**. Có tiền lệ đắt: 5 chương xếp SAFE bằng từ
khoá thực ra là REVIEW và đã bị nạp lên dịch vụ ngoài.

⇒ Mức IP chỉ in khi có **bảng đọc được bằng máy** trong thân sách (3/32 cuốn hiện
nay). Còn lại in `mức IP: chưa đo`. Số cuốn có bảng sẽ tự tăng vì P7 bản mới đã sinh
nó — không cần làm gì thêm.

## 4. Nhãn phạm vi phát hành

Thứ tự đọc, dừng ở nguồn đầu tiên tìm thấy:

1. tiêu đề `# ⛔ Phạm vi lưu hành` hoặc `# BẢN NỘI BỘ …` trong **thân `book.md`**
   → phủ 26 trong 28 cuốn không có tệp sidecar (đo 2026-10-03, 32 cuốn; đo lại
   2026-10-05 trên 34 cuốn ra **23 khai trong thân**, xem bảng rút lại ở §2.2)
2. `_scope_decision.md`, trường `**phạm vi phát hành: …**` → 4/32 (đo lại
   2026-10-05: **5/34**, cả 5 đều cũng đã khai trong thân — thân sách vẫn luôn
   thắng, thứ tự đọc không đổi)
3. **không tìm thấy** → in `⛔ PHẠM VI CHƯA KHAI — coi như NỘI BỘ`

Mục 3 là bắt buộc. Lý do: đã có tiền lệ đo được — bản EPUB đầu tiên của
`10x-easier-than-2x` mang `distribution: ⛔ NỘI BỘ` ở frontmatter và **0/70 tệp trong
zip** chứa chữ ấy, vì `md_to_epub.py` bóc frontmatter trước khi giao pandoc. Một tệp
vài trăm KB không dấu hiệu thì ai chuyển tiếp cũng được.

**Nhãn phải nằm trong thân trang HTML**, không nằm trong `<meta>` hay chú thích.

## 5. Bất biến

Năm thứ này là **bất biến**, không phải chi tiết cài đặt. Vi phạm bất kỳ cái nào thì
bản sinh ra không được coi là hợp lệ.

| | Bất biến | Bắt nguồn từ |
|---|---|---|
| **BI-1** | Dò tiêu đề phải đi qua **mặt nạ khối mã**. `#` trong ``` hoặc ~~~ không phải tiêu đề. | L3 — vỡ 5 cuốn |
| **BI-2** | Chương dừng ở tiêu đề kế tiếp theo luật phụ thuộc độ sâu (§2.3 L2), **không** dừng ở EOF. | L1 + L2 |
| **BI-3** | Trang không được gọi **bất kỳ** tài nguyên mạng nào. Offline tuyệt đối — kế thừa ràng buộc kiến trúc của `md-to-epub`. | ràng buộc đã có |
| **BI-4** | Nhãn phạm vi nằm **trong thân trang**, và khi không khai được thì in nhãn bảo toàn. | lỗi 0/70 tệp zip |
| **BI-5** | Mọi cảm biến nghiệm thu phải so với **một tổng tính ngoài đường ống**, không so các phần với nhau. | §2.4 — `pahl-beitz-tap2` ở 40% phủ mà 2/3 bộ dò báo sạch |

## 6. Bậc A — bản đồ sách, một tệp

Một tệp HTML cho cả cuốn. Mở bằng trình duyệt từ đĩa.

**Nội dung, theo thứ tự trên trang:**

1. **Đầu trang** — nhãn phạm vi · tên sách · N chương · tổng từ · tổng sơ đồ · mức
   nguyên bản · ước thời gian đọc lại
2. **Đồ thị tham chiếu chéo** — SVG tính sẵn trong Python, **không JS**. Cung nối
   chương, đốm to = bị nhiều chương trỏ tới, kèm một dòng chữ nêu 5 chương bị trỏ
   nhiều nhất. **Ẩn cả mục nếu số cạnh < 5** (`inside-the-box` chỉ có 2).
3. **Bảng "đọc lại trước"** — chỉ hiện khi tầng 2 có dòng `Rủi ro:` (3/32 cuốn).
4. **Thẻ chương**, nhóm theo phần. Mỗi thẻ: số chương · neo · tên · **tóm tắt STE 3–5
   dòng** · số từ thật / số từ đặt kèm % lệch · số sơ đồ thật / đặt · số chương khác
   cần đọc trước · mức IP · dòng `Rủi ro` nếu có.

**Giá trị không dự tính được, đã quan sát:** ô "% lệch" làm hiện ra chuyện cuốn
`usv-thiet-ke-he-thong` **vượt dàn ý +36%** (đặt 188.830 / thật 256.809). Không cuốn
nào đang đo cái lệch này. Phụ thu: dàn ý cuốn đó **tự mâu thuẫn** — frontmatter ghi
`target_words: 170000` nhưng tổng đặc tả từng chương ra 188.830, lệch 11% trong cùng
một tệp.

## 7. Cổng nghiệm thu

Chạy sau khi dựng. **Lệnh bắt buộc, không phải lời nhắc.**

```bash
# CỔNG CHẶN — khác ngưỡng thì không giao tệp
python scripts/md_to_html.py --verify <out.html>
```

Bảng `--verify` phải in:

| Phép đo | Ngưỡng | Bắt lỗi gì |
|---|---|---|
| tỷ lệ phủ: Σ từ trong chương ÷ `wc -w` cả `book.md` | **≥ 70% chặn · < 85% cảnh báo** | L1/L2/L3 và mọi lỗi cắt chương NẶNG — chặn ca 39–40%, cảnh báo ca 77%, im lặng trước ca 94% (xem ghi chú F3 dưới bảng) |
| `src="http` / `href="http` trong trang | **= 0** | gọi CDN ⇒ mất offline, và rò tên sách ra DNS |
| `<script` | **= 0** ở bậc A | bậc A không cần JS |
| `<!--` | **= 0** | chú thích nội bộ đường ống lọt vào bản xuất |
| nhãn phạm vi trong thân trang | **≥ 1** | BI-4 |
| số thẻ chương == số chương parse được | **lệch 0** | mất chương lúc kết xuất |
| số sơ đồ ĐẾM ĐƯỢC trên thẻ vs trong `book.md` | **lệch 0** | đếm sai, không phải dựng sai — **bậc A chỉ đếm sơ đồ, không dựng** |

**Hai mức, cố ý.** Ngưỡng **chặn đặt 70%** — đủ thấp để không chặn ca hợp lệ đã biết
(`nha-luoi-chong-uav` ở **76,1%** vì có phần sau sách lớn thật). Mức **85% chỉ cảnh
báo**. Không được nâng 85% thành cổng chặn trước khi R-2 đóng — làm thế là chặn ca
hợp lệ bằng một ngưỡng đặt theo cảm giác.

**Sửa 2026-10-06 (F3) — câu "vẫn bắt mọi ca L3 đã đo" ở trên và câu "cảm biến duy
nhất bắt đủ 5/5" trong bảng trên đều bị rút lại.** Cả hai đúng cho một phép **so
sánh trước/sau** (phủ tụt ở cả 5 cuốn khi lỗi khối mã được mô phỏng — xem §2.4), nhưng
**sai** cho cổng `--verify` đã giao: cổng đó dùng một **ngưỡng tuyệt đối trên một lượt
chạy**, không so trước/sau. Đo lại 5 cuốn L3 đó với ngưỡng đã chọn (70% chặn · 85%
cảnh báo):

| Sách | Phủ | Trạng thái |
|---|---|---|
| `tau-nhom-han-quoc-phong` | 38,9% | CHẶN |
| `pahl-beitz-tap2` | 40,1% | CHẶN |
| `ai-at-war` | 76,6% | cảnh báo |
| `cross-design-methods` | 94,0% | ok, im lặng |
| `kien-truc-tu-hanh-hang-hai` | 93,7% | ok, im lặng |

Chỉ **2/5** bị chặn, **2/5** im lặng hoàn toàn. Hàng tỷ lệ phủ bắt ca **nặng** (39–40%)
và cảnh báo ca **vừa** (77%); nó **không** bắt được ca **nhẹ** (94%) — và không ngưỡng
tuyệt đối nào có thể bắt, vì một mất 4% nằm dưới mọi sàn mà không đồng thời chặn nhầm
sách hợp lệ gần nhất (`nha-luoi-chong-uav`, 76,1%). Hàng cấu trúc `tieu de lac trong
than chuong` (§7 bảng trên) mới là cảm biến bắt đúng **cả năm** ca này — giữa hai
hàng: hàng tỷ lệ phủ bắt mất NẶNG, hàng cấu trúc bắt lỗi CẤU TRÚC chính xác, nhưng
không hàng nào một mình bắt được mất NHẸ.

### 7.1 Đối chứng âm — bắt buộc, trong `test_md_to_html.py`

Cảm biến phải **sai đúng đơn vị của chính nó**. Mỗi đối chứng dưới đây phải làm cổng
**bật đỏ**; nếu nó vẫn xanh thì cổng không đo gì cả.

| Đối chứng âm | Cổng phải chặn ở |
|---|---|
| tiêm `<script src="https://cdn.jsdelivr.net/npm/x">` vào trang | phép đo CDN ≠ 0 (**đã chạy thật trên bản thợ: ra 1** ✅) |
| tắt mặt nạ khối mã rồi dựng `tau-nhom-han-quoc-phong` | tỷ lệ phủ tụt về ~39% |
| cho chương cuối chạy đến EOF rồi dựng `tu-khong-den-mot` | chương cuối 1,50× trung vị (22.915 ÷ 15.323) |
| cố định luật dừng ở `depth` rồi dựng `principles-ba-tai-san` | trung vị tụt về ~326 từ |
| bỏ nhãn phạm vi | phép đo nhãn = 0 |

⚠️ **Đối chứng âm không được là chính khuyết tật sắp bị sửa.** Bốn đối chứng trên
dựng bằng cách **tắt một bản vá** trong test, chứ không phải bằng cách để nguyên lỗi
trong mã sản xuất. Để nguyên lỗi thì sửa xong là đối chứng tự huỷ.

## 8. Bậc B — trang chương sâu, chỉ khi bấm

Dựng **theo yêu cầu từ bản đồ**, không áp đều.

- `mermaid.min.js` copy **một lần** vào `_assets/` cạnh các trang; trang trỏ đường dẫn
  tương đối. **Không nhúng inline** — 3,5 MB × N trang là không chấp nhận được.
- Bậc B là trang duy nhất được có `<script>`; cổng `<script> = 0` chỉ áp cho bậc A.
- Nội dung: sơ đồ sống pan/zoom · bảng xếp được · "Để áp dụng" thành danh sách tích.

**Hoãn khỏi v1:** "bước qua từng trạng thái" của sơ đồ. Nó cần sinh N biến thể mermaid
hoặc tiêm lớp đánh dấu vào mermaid sống — một việc dựng thật, không phải một tham số.

## 9. Rủi ro còn mở

| | Rủi ro | Xử lý |
|---|---|---|
| **R-1** | Tóm tắt STE là văn **agent sinh**, không đo được bằng máy như các trường khác. Đây là bề mặt bịa đặt. | Tóm tắt phải **neo vào thân chương**: mỗi dòng tóm tắt kèm số dòng trong `book.md` để kiểm được. Không neo được ⇒ in `chưa tóm tắt`. **Sửa 2026-10-06 (F1):** ô tóm tắt còn có một nguồn KHÁC không phải agent sinh — bullet của `Phase3-Outline.md` (tầng 2, suy thoái êm), hiện khi chưa có digest (32/34 cuốn). Bullet đó không mang số dòng gốc nên không có gì để neo — đây KHÔNG phải bịa đặt, chỉ là chưa qua cổng kiểm, nên trang phải dán nhãn riêng (`summary-unanchored`) và cổng `tom tat vi pham STE` phải lint cả hai nguồn như nhau; chỉ `neo tom tat sai` là tiếp tục CHẶN và chỉ áp cho digest. |
| **R-2** | **Đóng một phần 2026-10-06 (F3).** Đo lại trên 34 cuốn: phủ thấp nhất **76,1%**, hai cuốn nằm trong dải cảnh báo (**76,1%** và **83,9%**), trung vị **97,7%**. Ba ca lỗi khối mã đo được chạy **39–40%** (xem §7 ghi chú F3) — khoảng 40–76% vẫn rộng và không có điểm đo nào trong đó, nên **mọi ngưỡng chặn giữa 40% và 76% đều được dữ liệu ủng hộ ngang nhau**; 70% chỉ là điểm giữa đã chọn, không phải điểm tối ưu đo được. | 85% **phải giữ là cảnh báo** — nâng thành cổng chặn sẽ chặn nhầm hai cuốn hợp lệ đang nằm trong dải cảnh báo (76,1%, 83,9%). Trong lúc chờ thêm dữ liệu để thu hẹp khoảng 40–76%, **cảnh báo không được chặn** — người đọc bảng quyết định. |
| **R-3** | Ngưỡng chương-cuối-phình 1,8× đặt theo cảm giác (§2.4). | Giữ là **cảnh báo**, không nâng thành cổng chặn cho đến khi có phân bố. |
| **R-4** | Bản đồ là **hiện vật dựng ra**. Vá thẳng vào nó thì lần sinh sau xoá sạch. | Mọi sửa phải vào `book.md` hoặc vào bộ sinh, không vào `out.html`. Ghi câu này vào SKILL.md. |
| **R-5** | Bậc A đọc tên chương từ thân sách. Nếu sách đổi tiêu đề, bản đồ cũ im lặng lạc hậu. | In **ngày dựng + sha256 của `book.md`** vào chân trang. Lệch sha ⇒ bản đồ cũ. |

## 10. Việc KHÔNG làm

Ghi rõ để lần sau không ai mở lại:

- Không sửa `book-voice-and-style.md`.
- Không sửa `md_to_epub.py` (có test đang xanh).
- Không sửa `VERSION` và `CHANGELOG.md` — văn changelog đặt trong phần mô tả PR, dưới
  tiêu đề `## CHANGELOG`; người hợp nhánh mới chọn số phiên bản.
- Không dò mức IP bằng từ khoá (§3.4).
- Không gọi bất kỳ dịch vụ web nào, kể cả để dựng sơ đồ.
- Không publish hiện vật lên claude.ai trong v1.

## 11. Nghiệm thu spec này

Spec coi là xong khi:

1. `/book-map` chạy được trên **32/32 cuốn**, tỷ lệ phủ in ra cho từng cuốn.
2. `scripts/test_md_to_html.py` xanh, **gồm cả 5 đối chứng âm ở §7.1**.
3. Năm bất biến §5 mỗi cái có một phép đo trong `--verify`.
4. Ba orchestrator có pha P7.6, và pha đó **không chặn** pha sau khi CEO bỏ qua.
5. `/book-map` gọi được đứng riêng, không cần chạy pipeline.
