# Spec: `/ebook-to-md` + `/ebook-lecture` — PDF ebook → MD theo chương → NotebookLM → bài giảng

> Date: 2026-07-25 · Status: approved-design · Domain: extract/ + learn/
> Nguồn gốc: CEO yêu cầu nối khâu còn thiếu ở đầu chuỗi học tập — hiện đã có
> `/nlm` (CLI), `/book-notebook` (chunk sách đã có sẵn dạng MD), `/learn-lecture`
> (notebook → slide+audio+video), nhưng chưa có đường từ **file PDF ebook** vào.

## 1. Mục đích

CEO đưa một file PDF ebook → nhận về bộ file Markdown tách theo chương (chương dài
tự tách tiếp theo đoạn), nạp vào một NotebookLM notebook, rồi bàn giao cho
`/learn-lecture` sản xuất bài giảng.

Khâu PDF→MD tách thành skill độc lập vì còn dùng được cho mọi PDF cần số hóa
(tài liệu kỹ thuật, catalogue nhà cung cấp, tiêu chuẩn MIL-STD), không riêng ebook.

## 2. Quyết định thiết kế đã chốt (CEO, 2026-07-25)

| # | Quyết định | Lý do CEO chọn | Đánh đổi đã được nêu |
|---|---|---|---|
| 1 | Engine trích xuất **luôn là PP-StructureV3**, không hybrid theo text-layer | Chất lượng layout: bảng, công thức, thứ tự đọc đa cột ra Markdown chuẩn | Máy không GPU: đo thực tế 44 s/trang cho OCR thuần, StructureV3 nặng hơn → ebook 300 trang ≈ 4–6 h |
| 2 | Ranh giới chương lấy từ **bookmark PDF**, CEO duyệt trước khi OCR | Biết chính xác bản đồ chương TRƯỚC khi đốt 2–4 h máy | Ebook không có bookmark phải suy từ trang mục lục |
| 3 | Đóng gói **1 orchestrator + 1 block** | Khâu PDF→MD tái sử dụng được | Nhiều file hơn phương án gộp 1 skill |
| 4 | **Bật HPI** (`paddleocr install_hpi_deps cpu`) + chạy nền | Rút 2–5× thời gian mỗi cuốn | Thêm một bước setup, thêm dependency ONNX Runtime/OpenVINO |
| 5 | OCR **theo từng trang** (per-page cache) | Job 2–4 h đứt giữa chừng chỉ mất 1 trang | Bảng/đoạn tràn qua 2 trang mất ngữ cảnh → ghi cảnh báo QC, không tự xử lý |

## 3. Định danh & giao diện

### `/ebook-to-md` (block)
- Vị trí: `skills/extract/ebook-to-md/SKILL.md`
- Gọi: `/ebook-to-md <đường-dẫn-pdf>`
- Flags:
  - `--pages <a-b>` — chỉ xử lý khoảng trang này (test nhanh / OCR bổ sung)
  - `--resume` — tường minh cho hành vi resume mặc định
  - `--chunk-kb <N>` — ngưỡng tách chương thành đoạn, mặc định 50
  - `--no-images` — bỏ trích ảnh, chỉ lấy text
- Engine: venv `D:\GitHub\PaddleOCR\.venv` + `PADDLE_PDX_CACHE_HOME=D:\tmp\paddlex_cache`
  (xem §9 — môi trường đã dựng sẵn ngày 2026-07-25)

### `/ebook-lecture` (orchestrator)
- Vị trí: `skills/learn/ebook-lecture/SKILL.md`
- Gọi: `/ebook-lecture <đường-dẫn-pdf | book-slug>`
- Flags: `--from <bước>` (`md` | `ingest` | `handoff`), `--notebook <tên>` (ingest vào
  notebook có sẵn thay vì tạo mới)
- Engine: MCP `notebooklm-mcp`, fallback CLI `nlm` — kế thừa nguyên rule auth của
  `/nlm` và `/learn-lecture` (phiên ~20 phút, hết hạn → CEO chạy `nlm login`)

### Trigger (description frontmatter)
EN + VI: "ebook to markdown", "pdf to md", "pdf sang markdown", "số hóa ebook",
"chuyển pdf thành chương", "ebook lecture", "bài giảng từ ebook", "pdf thành bài giảng".

## 4. Bố cục vault

```
D:\Workshop_X\3_Resources\Books & Articles\<book-slug>\
  ChapterMap.md          state file — bản đồ chương CEO duyệt; là hợp đồng cho E3
  pages\page-0001.md     cache OCR từng trang (checkpoint resume)
  chapters\01-<slug>.md  DELIVERABLE — 1 file/chương
  chapters\03.2-<slug>.md  đoạn, khi chương 3 vượt ngưỡng chunk
  images\                ảnh PP-StructureV3 trích ra, MD tham chiếu đường dẫn tương đối
  ocr.log                tiến độ + ETA của job nền
  Ingest-Manifest.md     notebook id/url + source_id từng chương
```

Đặt ở `3_Resources` theo IPARAG (sách = thứ mình DÙNG, không phải project có deadline).
Bài giảng vẫn ra `2_Areas\CEO-Self\Learning-Architecture\<slug>\` do `/learn-lecture`
quản — hai skill không giẫm chân nhau.

Ổ đĩa: **luôn `D:\Workshop_X`**. `E:\Workshop_X` là bản cũ (Learning-Architecture ở E:
chỉ còn 1 file, ở D: đã có đủ output Claude-101) — cùng rule với `/learn-lecture`.

## 5. Luồng `/ebook-to-md` — 5 bước

```
E0 PREFLIGHT → E1 MAP → [CEO GATE] → E2 OCR (nền) → E3 ASSEMBLE → E4 VERIFY
```

### E0 PREFLIGHT
1. File PDF tồn tại và đọc được (`pypdfium2.PdfDocument`) → lấy số trang.
2. Kiểm venv PaddleOCR + `PADDLE_PDX_CACHE_HOME`. Thiếu → HALT kèm lệnh dựng lại (§9).
3. Kiểm HPI: thử tạo pipeline với `use_hpip=True`; chưa cài → nhắc CEO chạy
   `paddleocr install_hpi_deps cpu`, cho phép tiếp tục không HPI nếu CEO chọn.
4. Slug hóa tên sách (bỏ dấu, kebab-case) → tạo cây thư mục §4.
5. `ChapterMap.md` đã tồn tại → chế độ resume, nhảy thẳng E2 với các trang còn thiếu.

### E1 MAP
1. `PdfDocument.get_toc()` → cây bookmark (level, title, page index). **API đã verify
   chạy được trên venv hiện tại.**
2. Chọn cấp làm "chương": mặc định **level 0**. Nhưng nếu level 0 có <3 mục mà level 1
   có ≥3 mục (ebook chia Phần → Chương) thì dùng **level 1**, level 0 ghi vào ChapterMap
   làm cột "Phần". Các level sâu hơn giữ lại làm gợi ý tách đoạn ở E3. Chọn sai cấp
   không nguy hiểm vì CEO GATE duyệt trước khi OCR.
3. Trang kết thúc của chương N = trang bắt đầu chương N+1 trừ 1; chương cuối = hết sách.
4. Không có bookmark → OCR riêng 3–8 trang đầu, Claude đọc trang mục lục suy ra map.
   Vẫn không được → CEO nhập map thủ công, hoặc coi cả cuốn = 1 chương.
5. Ghi `ChapterMap.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: sop
status: active
tags: [#type/sop, #status/active, #topic/learning]
source_pdf: <đường dẫn tuyệt đối>
total_pages: <N>
engine: PP-StructureV3
---
| # | Chương | Trang | Số trang | File | Trạng thái |
|---|--------|-------|----------|------|------------|
| 1 | Mở đầu | 1-14  | 14       | 01-mo-dau.md | ⬜ |
| 2 | ...    | 15-38 | 24       | 02-....md    | ⬜ |
```

Trạng thái: ⬜ pending · 🔄 ocr · ✅ done · ⚠ warning (kèm lý do).

### CEO GATE (Core — chặn)
Trình bản đồ chương + ước tính thời gian OCR (số trang × tốc độ đo được) → CEO duyệt,
gộp, tách, đổi tên, hoặc loại chương không cần. **Chỉ sau khi duyệt mới chạy E2.**
Đây là điểm chặn quan trọng nhất: sai map mà đã OCR xong nghĩa là mất 2–4 h.

### E2 OCR (chạy nền)
Script `scripts/ebook_ocr.py`, gọi qua `run_in_background`:
- Với mỗi trang trong phạm vi cần xử lý: nếu `pages/page-NNNN.md` đã tồn tại → skip.
- Gọi PP-StructureV3 cho trang đó → ghi Markdown + ảnh vào `images/`.
- Ghi 1 dòng tiến độ vào `ocr.log`: trang / tổng, thời gian trang, ETA còn lại.
- Ghi confidence trung bình của trang vào cùng dòng log (E4 dùng lại).
- Ctrl-C / mất điện → chạy lại lệnh cũ, tự bỏ qua trang đã xong.

### E3 ASSEMBLE
1. Ghép `pages/page-NNNN.md` theo khoảng trang trong ChapterMap → `chapters/NN-<slug>.md`.
2. Frontmatter mỗi file chương:
   ```yaml
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   type: article
   status: active
   tags: [#type/article, #status/active, #topic/learning]
   book: <tên sách>
   chapter: <N>
   pages: <a-b>
   ```
3. Dọn artifact OCR: số trang chạy đứng riêng dòng, header/footer lặp lại ≥3 trang,
   gạch nối cuối dòng nối từ bị cắt.
4. Chương vượt `--chunk-kb` (mặc định 50KB) → tách thành `NN.M-<slug>.md`. Đây vừa là
   "đoạn" CEO yêu cầu, vừa là ngưỡng NLM retrieve chính xác. Thứ tự ưu tiên điểm cắt:
   (a) heading cấp 2 trong Markdown; (b) không có heading cấp 2 → bookmark level sâu hơn
   từ E1; (c) không có cả hai → cắt theo ranh giới trang gần nhất sao cho mỗi đoạn
   ≤ ngưỡng, tiêu đề đặt là `<Tên chương> (phần M)`. Ghi các file con trở lại ChapterMap.
5. Cập nhật trạng thái ChapterMap → ✅.

### E4 VERIFY
Bảng QC gửi CEO: mỗi chương gồm số trang, số ký tự, confidence OCR trung bình, số ảnh.
Cảnh báo (⚠, không im lặng bỏ qua):
- Chương rỗng hoặc <500 ký tự → nghi map sai hoặc trang scan hỏng
- Confidence trung bình <0.85 → nghi chất lượng scan kém
- Trang có bảng bị cắt ở ranh giới trang (phát hiện bằng dòng bảng Markdown chưa đóng)

## 6. Luồng `/ebook-lecture` — orchestrator

```
L0 MD       gọi /ebook-to-md (skip nếu chapters/ đã đủ theo ChapterMap)
L1 AUTH     refresh_auth → fail thì HALT, báo CEO chạy `nlm login`
L2 CREATE   check trùng title trước → notebook_create "Book: <tên sách>"
            trùng → CEO chọn: tạo mới song song / dùng lại / dừng (KHÔNG tự đè)
L3 INGEST   source_add từng file chương — SONG SONG trong 1 message
            + 1 meta-source = ChapterMap.md (để NLM trả lời được câu hỏi cấu trúc sách)
L4 VERIFY   notebook_describe → so số source vs số file; lệch thì báo per-source
            ghi Ingest-Manifest.md
L5 TEST     CEO mở URL, test 2 query: "liệt kê các chương", "chương N nói gì"  ← Core gate
L6 HANDOFF  in lệnh `/learn-lecture "<tên notebook>"` để CEO chạy
```

**Không tự chain sang `/learn-lecture`** — skill đó có gate riêng cho CEO chọn mode
(compact/full/extend) và duyệt giáo trình; tự chạy sẽ vượt quyền.

## 7. Xử lý lỗi

| Tình huống | Xử lý |
|---|---|
| PDF hỏng / có mật khẩu | HALT ở E0, báo rõ, không tạo thư mục rác |
| Không bookmark, không đọc được mục lục | CEO nhập map thủ công, hoặc cả cuốn = 1 chương |
| HPI chưa cài | Cảnh báo + cho phép chạy không HPI (chậm hơn), không HALT |
| OCR chết giữa chừng | `ocr.log` giữ tiến độ; chạy lại tự skip trang đã xong |
| Trang OCR ra rỗng | E4 cảnh báo ⚠, ghi vào ChapterMap, không im lặng |
| Bảng tràn 2 trang | E4 cảnh báo, CEO tự sửa file chương — không tự động ghép |
| NLM auth hết hạn giữa ingest | HALT, giữ nguyên `chapters/`, resume bằng `--from ingest` |
| Notebook trùng title | CEO quyết, không tự đè (cùng rule `/book-notebook`) |
| Chương >50KB | Tự tách theo heading cấp 2, ghi rõ trong ChapterMap |

## 8. COD

- E1 MAP (đọc bookmark), E2 OCR, E3 ASSEMBLE, L3 INGEST = **Offload**
- Duyệt bản đồ chương (CEO GATE), đọc QC report E4, test query L5 = **Core**
- Ghi log, dọn artifact OCR = **Default**

## 9. Môi trường (đã dựng 2026-07-25)

Khâu OCR chạy trên venv riêng của repo PaddleOCR, không dùng Python hệ thống:

```
venv:   d:\GitHub\PaddleOCR\.venv        (Python 3.12.10)
paddle: paddlepaddle 3.2.0 CPU  ·  paddlex 3.7.2  ·  paddleocr 3.8.0.dev11 (editable)
env:    PADDLE_PDX_CACHE_HOME=D:\tmp\paddlex_cache
```

Máy không có GPU NVIDIA; ổ C: còn ~25 GB nên model cache và pip cache đều để trên D:.
Số đo cơ sở: OCR thuần PP-OCRv6_medium = 43.7 s/trang A4 (4 trang, 89 dòng,
confidence trung bình 0.994).

## 10. Kiểm thử

1. **Smoke** — `sample_pdf.pdf` trong repo PaddleOCR (4 trang, ~3 phút): chạy hết
   E0→E4, kiểm cây thư mục, frontmatter, và nhánh "không có bookmark" (file này
   `get_toc()` trả 0 entry — đúng ca cần test).
2. **Có bookmark** — một PDF có outline thật, kiểm map chương khớp bookmark.
3. **Resume** — giết job giữa chừng, chạy lại, xác nhận chỉ OCR các trang còn thiếu.
4. **Ngưỡng chunk** — chương giả >50KB, xác nhận tách thành `NN.M-*.md` và ChapterMap
   được cập nhật.
5. **End-to-end** — 1 ebook thật CEO chọn, chạy tới notebook + test query, rồi bàn giao
   `/learn-lecture`.

## 11. Ngoài phạm vi (YAGNI)

- Không hỗ trợ EPUB/MOBI — chỉ PDF.
- Không dịch nội dung sách (đã có `/nlm` + PP-DocTranslation nếu cần).
- Không tự tạo Galaxy note từ nội dung sách (đó là `/galaxy-note`, R3 risk — chỉ làm khi CEO yêu cầu).
- Không tự chạy `/learn-lecture`.
- Không hybrid engine theo text-layer — CEO đã chốt luôn dùng PP-StructureV3 (§2.1).
