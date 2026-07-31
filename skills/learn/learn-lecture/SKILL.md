---
name: learn-lecture
description: >-
  Turn a NotebookLM notebook into a synchronized lecture series — per lesson: slide
  deck + Vietnamese audio that announces "Phần N" in lockstep with the slides. Scans
  all sources, proposes a curriculum in 3 modes (compact/full/extend), CEO picks
  lessons one by one; auto-selects sources per lesson, creates slides AND a slide-script
  file in the same step (the single sync contract — no re-reading the slide PDF),
  generates audio from the FULL source content (not
  the compressed slide bullets) chunked to match the slides, downloads both to the vault,
  detects the spoken "Phần N" timestamps ONCE right after the audio lands and saves them
  to a marks file, then builds a synchronized MP4 video from that file (no re-transcribing),
  and resumes across sessions via Curriculum.md.
  Triggers on: "learn lecture", "lecture from notebook", "lecture series", "synced
  slide audio", "tạo bài giảng", "bài giảng từ notebook", "tạo bộ bài giảng", "giáo
  trình từ notebook", "slide audio đồng bộ", "bài giảng đồng bộ", "video bài giảng",
  "lecture video".
---

Biến một NotebookLM notebook thành bộ bài giảng đồng bộ slide + audio tiếng Việt
+ video MP4 tự chuyển slide theo giọng đọc.

Usage: `/learn-lecture <notebook-name-or-alias>` — flags: `--mode compact|full|extend`, `--resume`, `--lesson <N>`, `--no-video`

Engine: MCP `notebooklm-mcp` — `notebook_list`, `notebook_get`, `source_describe`,
`source_get_content` (fetch text thô/nguồn — dùng cho OUTLINE), `notebook_query`
(chỉ khi cần tổng hợp AI; timeout trên notebook lớn), `studio_create`/`studio_status`,
`download_artifact`. Fallback CLI `nlm` (PATH: Python313/Scripts) khi MCP lỗi —
xem "Gotchas thực chiến".

Auth: phiên NLM ~20 phút. Lỗi auth → báo CEO chạy `nlm login` ở terminal khác →
retry, tối đa 2 lần → vẫn fail thì DỪNG có trạng thái (Curriculum.md đã lưu, resume được).

Vault root: `D:\Workshop_X\2_Areas\CEO-Self\Learning-Architecture\<notebook-slug>\`
(LUÔN ổ `D:\` — không dùng path `E:\` cũ).

---

## PIPELINE — 5 phase

```
Phase 0 INTAKE → Phase 1 SCAN → Phase 2 CURRICULUM (CEO gate)
→ Phase 3 LESSON LOOP (per bài, 9 bước) → Phase 4 WRAP
```

**Resume:** nếu Curriculum.md đã tồn tại cho notebook này → bỏ qua Phase 1-2, vào
thẳng LESSON LOOP với các bài ⬜ pending. `--resume` là alias tường minh; `--lesson N`
nhảy thẳng bài N.

### Phase 0 — INTAKE

1. Resolve notebook: khớp tên/alias qua `notebook_list` (fuzzy). Mơ hồ → đề xuất
   ứng viên gần nhất, CEO xác nhận.
2. Check auth (một lệnh list bất kỳ). Fail → quy trình `nlm login` ở trên.

### Phase 1 — SCAN

1. `notebook_get` → lấy toàn bộ title + source_id của các nguồn trong notebook.
2. Claude gom cụm chủ đề từ TITLE (chỉ `source_describe` khi title mơ hồ —
   KHÔNG query từng nguồn, tốn phiên). Nếu title theo mã có tiền tố `NN.` (VD
   `01.10-...md`) → gom theo prefix `NN.` = 1 khóa.
3. **Notebook đa khóa (thư viện):** nếu thấy nhiều cụm prefix `NN.` khác nhau
   (VD 284 nguồn = ~19 khóa), ĐÂY KHÔNG PHẢI 1 khóa — LÀM TỪNG KHÓA MỘT: liệt kê
   bản đồ khóa (mã · tên · số bài) → CEO chọn 1 khóa → chỉ khóa đó vào Phase 2.
   Slug vault = `<Tên-khóa>` (không phải tên notebook).
4. Notebook >45 nguồn hoặc 1 cụm quá lớn → cảnh báo, đề xuất thu hẹp phạm vi
   (chọn 1 khóa) hoặc extend mode.

### Phase 2 — CURRICULUM

1. Nếu KHÔNG có --mode: hiển thị tóm tắt cụm chủ đề + ước tính số bài của cả 3
   chế độ (VD: compact ≈ 4 bài · full ≈ 9 · extend ≈ 12) → CEO chọn.

| | compact | full | extend |
|---|---|---|---|
| Gom | nhiều cụm → ít bài tổng quan | mỗi cụm = 1 bài đầy đủ | full + deep-dive cụm trọng yếu |
| Slide/bài (N) | ~8 | ~12 | 12–20 |
| Audio/bài | 8–10 phút | 13–16 phút | 15–25 phút |

**N KHÔNG cố định — tự đánh giá theo độ dày nội dung.** Các con số trên chỉ là điểm
xuất phát. Ở 3.2, sau khi đọc nguồn thật, tăng N nếu nội dung dài và phức tạp; quy tắc:
**mỗi slide đúng MỘT khái niệm**. Dấu hiệu phải tăng N: một phần dàn ý phải gộp ≥3 chủ đề
lớn (VD "systems theory + Value Analysis + VDI 2221 + mục tiêu sách"), hoặc một mục sách
dày đặc tên riêng/tiêu chí (VD phần lịch sử ~20 nhân vật → tách 2 slide). Tham chiếu:
26 trang sách dày ≈ 20 slide.

**Trần thời lượng — biết trước để khỏi kỳ vọng sai:** NLM giới hạn tổng độ dài audio
(đo được ~18 phút với `audio_length="long"`) rồi CHIA ĐỀU cho các phần. Nên tăng N làm
mỗi phần MỊN hơn, KHÔNG làm tổng nội dung NHIỀU hơn. Hệ quả 2 chiều: N quá thấp → phần
dày bị nén (32 giây cho 1 phần trong live-run); N quá cao (>25) → mọi phần đều bị băm
vụn. Muốn giảng sâu hơn nữa thì TÁCH THÀNH 2 BÀI, đừng tăng N vô hạn.

2. Đề xuất giáo trình chi tiết: mỗi bài = số thứ tự · tên · 1 câu mô tả · nguồn dự
   kiến (title + source_id) · ước tính slide/phút.
3. CEO duyệt/sửa (gộp, tách, đổi thứ tự, loại bài) TRƯỚC khi ghi Curriculum.md —
   đây là gate **Core** (COD). Sản xuất ở Phase 1/3 = Offload.
4. Ghi state file `Curriculum.md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
notebook: <tên notebook>
notebook_id: <uuid>
mode: full
status: active          # active | completed
tags: [#type/sop, #status/active, #topic/learning]
---
| # | Bài | Nguồn (id rút gọn) | Slide | Trạng thái | Ngày | Thư mục |
|---|-----|--------------------|-------|------------|------|---------|
| 1 | ... | 0c2942, 0b0e28     | 12    | ✅ done    | ...  | Bai-01-... |
| 2 | ... | ...                | 12    | ⬜ pending  |      |         |
```

Bài lỗi bỏ qua → ⚠ skipped kèm lý do. Tất cả ✅ → `status: completed`.

### Phase 3 — LESSON LOOP (9 bước / bài)

```
3.1 PICK      CEO chọn bài (mặc định: bài pending đầu tiên)
3.2 OUTLINE   source_get_content cho từng source_id của bài (CHỈ với source_ids
              của bài đó) — fetch text thô, TỨC THÌ, không dùng notebook_query
              (timeout trên notebook lớn). Ghép nội dung → trích dàn ý đầy đủ theo
              thứ tự (mục tiêu, đề mục, khái niệm, ví dụ, thao tác, ghi nhớ; giữ
              nguyên số liệu/tên riêng) → chưng cất thành DÀN Ý ĐÁNH SỐ N phần.
              CHỌN N Ở ĐÂY, sau khi đã đọc nguồn thật — không dùng N mặc định của mode.
              Mỗi slide đúng MỘT khái niệm; phần nào phải gộp ≥3 chủ đề lớn → tách ra.
              Xem "N KHÔNG cố định" ở Phase 2.
3.3 SLIDES    (a) studio_create(slide_deck, source_ids, language=vi) với prompt template
              SLIDE (references/) — nhúng dàn ý N phần, ràng buộc "ĐÚNG N slide riêng
              biệt, không gộp, CHỈ dùng nguồn đã chọn". Poll completion QUA CLI nền
              (không gọi studio_status MCP lặp — nó dump TẤT CẢ artifact, tốn context)
              (b) NGAY LẬP TỨC ghi `slide-script.md` vào thư mục bài (không đợi PDF) —
              chính là N tiêu đề + bullet đã gửi trong prompt. ĐÂY LÀ HỢP ĐỒNG ĐỒNG BỘ
              DUY NHẤT cho audio (3.7), video (3.9) và outline (3.8). Định dạng bắt
              buộc: xem "slide-script.md" bên dưới.
3.4 EXTRACT   download_artifact(slide_deck→PDF) về vault. KHÔNG đọc PDF để lấy tiêu đề —
              tiêu đề đã có trong slide-script.md. Chỉ lấy SỐ TRANG bằng pymupdf:
              `python -c "import fitz;print(fitz.open(r'<pdf>').page_count)"` (rẻ,
              không render, không tốn context). LƯU Ý: slide chỉ là khung — nội dung
              audio KHÔNG lấy từ bullet slide (bullet đã nén), mà lấy từ dàn ý-nguồn
              ở 3.2 (đầy đủ)
3.5 VERIFY-S  page_count == N trong slide-script.md? PASS → 3.7. Đây là toàn bộ phép
              kiểm bắt buộc: prompt đã ghim tiêu đề nên khớp số trang là đủ để đồng bộ.
              (Chỉ soi tiêu đề thật khi 3.6 kích hoạt — xem Fallback 3.5.)
3.6 REPAIR    lệch số trang → tối đa 1 vòng studio_revise (hoặc tạo lại) → quay lại 3.4.
              Nếu tạo lại vẫn lệch → soi tiêu đề THẬT (Fallback 3.5) rồi SỬA
              slide-script.md cho khớp slide thật (script luôn phải phản ánh slide
              thật trước khi sang 3.7) → hoặc CEO quyết: chấp nhận có ghi chú / bỏ bài
              (⚠ skipped)
3.7 AUDIO     ĐỌC `slide-script.md` để lấy N + tiêu đề (KHÔNG mở lại PDF). Sinh prompt
              audio với nội dung LẤY TRỰC TIẾP & ĐẦY ĐỦ TỪ NGUỒN (dàn ý-nguồn 3.2 /
              source_get_content — chi tiết, ví dụ, số liệu, thao tác, sâu hơn bullet
              slide), MAP lên khung script: N đoạn = N slide, mỗi đoạn mở
              "Phần N — <tiêu đề trong slide-script.md>" rồi giảng đầy đủ nội dung
              nguồn của phần đó.
              Tự kiểm: mỗi đoạn khai triển từ nguồn (không chỉ đọc lại bullet) + N
              callout khớp ĐÚNG CHUỖI tiêu đề trong slide-script.md TRƯỚC khi gửi.
              studio_create(audio) — LUÔN language=vi (bắt buộc, rule /nlm; chỉ đổi
              khi CEO yêu cầu rõ tiếng Anh) → poll completion qua CLI nền
3.8 SAVE      tải slide PDF (download_artifact) + audio (CLI `nlm download audio
    +MARKS    --id <aid> -o` — MCP download_artifact AUDIO hay fail) → <vault-root>\
              Bai-NN-<slug>\ + slide-script.md (đã ghi ở 3.3) + outline.md (dàn ý-nguồn
              + Sync Report; KHÔNG chép lại tiêu đề — trỏ sang slide-script.md).
              NGAY khi audio có bytes, DÒ MỐC MỘT LẦN và ghi ra file (cùng script nền
              với vòng retry download, nối tiếp):
              `python D:\KN-Stack\scripts\lecture_video.py --audio <audio.mp3>
              --slides <N> --detect-only` → sinh `<audio>.marks.json` (mốc giây của
              "Phần 1..N") + `<audio>.transcript.txt` (bản ghi có mốc — MIỄN PHÍ vì
              whisper đã chạy; dùng để đặt mốc theo NỘI DUNG khi audio không xướng
              "Phần N"). N lấy từ slide-script.md — KHÔNG cần PDF ở bước này.
              Đây là mốc chuẩn dùng cho MỌI lần dựng video sau này. In ra số mốc
              tìm được / thiếu → ghi vào Sync Report NGAY (biết sớm hỏng đồng bộ,
              trước khi tốn công dựng video).
              ⚠️ **KIỂM MỐC KHỚP NỘI DUNG — BẮT BUỘC, KHÔNG BỎ:** in transcript tại
              từng mốc vừa dò và đối chiếu với tiêu đề trong `slide-script.md`.
              `found == N` KHÔNG đủ: đã gặp ca audio tự bịa cấu trúc phần của riêng
              nó, xướng "phần 6" rồi giảng nội dung phần 10 → mốc đủ số nhưng video
              lệch slide toàn bộ nửa sau (lỗi im lặng, chỉ lộ khi xem hết video).
              Mốc sai nội dung → xử như hỏng: sinh lại audio, KHÔNG vá.
3.9 VIDEO     (bỏ qua nếu --no-video) dựng MP4 đồng bộ từ PDF+audio+marks đã có:
              `python D:\KN-Stack\scripts\lecture_video.py --pdf <slides.pdf>
              --audio <audio.mp3> --out <Bai-NN-video.mp4>` — ĐỌC `<audio>.marks.json`
              (KHÔNG transcribe lại; chỉ dò mới nếu file thiếu/lệch audio_bytes, hoặc
              khi ép `--redetect`) → tách slide→PNG, slide N hiện đúng mốc "Phần N"
              (mốc sót → nội suy, ghi WARNING), ffmpeg ghép h264+AAC cắt đúng độ dài
              audio, sinh syncmap.md (dòng "Nguồn mốc" ghi rõ lấy từ marks file hay
              dò mới). PDF chỉ dùng làm NGUỒN ẢNH; tên/nhãn các phần đối chiếu
              `slide-script.md`, không đọc lại tiêu đề từ PDF. Có marks file →
              bước này chỉ còn ffmpeg (giây–chục giây), chạy foreground được.
              Ghi kết quả vào Sync Report + cập nhật Curriculum.md → hỏi "Tạo bài
              tiếp theo? (bài N+1)". Video fail → ⚠ ghi chú, KHÔNG chặn bài
              (slide+audio+marks đã đủ, dựng lại bất cứ lúc nào không tốn whisper)
3.9b VERIFY-V ĐỌC syncmap vừa sinh và kiểm 2 điều — 10 giây, bắt được lỗi lệch
              toàn cục mà mắt thường chỉ thấy khi xem hết video:
              (a) **slide 1 PHẢI bắt đầu 0:00**. Khác 0 = cả dải slide chạy SỚM
                  đúng bằng offset đó (xem "Bẫy --timings" ở Gotchas).
              (b) mốc slide cuối < độ dài audio, và các mốc tăng dần.
              Sai (a) hoặc (b) → dựng lại, KHÔNG giao video cho người học.
```

### slide-script.md — hợp đồng đồng bộ

Ghi ở 3.3(b), NGAY sau khi gửi `studio_create(slide_deck)`, vào
`<vault-root>\Bai-NN-<slug>\slide-script.md`. Mọi bước sau ĐỌC file này, KHÔNG mở PDF.

```markdown
---
lesson: N
title: <tên bài>
slides: <N>
scope: <số mục + tiêu đề tiếng Anh gốc + khoảng trang>
source_ids: [<...>]
slide_artifact_id: <uuid>
verified_pages: <điền ở 3.5: số trang PDF thật>
---
| # | Tiêu đề slide (dùng làm callout "Phần N — …") | Bullet chính |
|---|---|---|
| 1 | <tiêu đề 1> | <3–5 ý ngắn đã gửi trong prompt> |
| … | … | … |
```

Quy tắc: **tiêu đề trong bảng này là chuỗi phải xướng nguyên văn ở đầu mỗi đoạn audio.**
Sửa file → phải sửa cả audio; đừng sửa sau khi audio đã sinh.

### `<audio>.marks.json` — hợp đồng MỐC THỜI GIAN

Sinh ở 3.8 bằng `lecture_video.py --detect-only`, nằm cạnh file audio. slide-script.md
giữ **tên** các phần; marks.json giữ **mốc giây** các phần. Dò MỘT LẦN, dùng mãi.

```json
{ "version": 1, "audio": "Bai-01-audio.mp3", "audio_bytes": 17342114,
  "audio_duration": 913.4, "lang": "vi", "model": "small", "n_slides": 12,
  "found": [1,2,3], "missing": [4],
  "marks": { "1": 0.0, "2": 61.3, "3": 154.9 } }
```

- **Ai đọc:** 3.9 VIDEO. Có file khớp audio → bỏ hẳn whisper. Transcribe ~15 phút audio
  ≈ 3–5 phút CPU, nên chỉ trả giá 1 lần ở 3.8 (`run_in_background`); mọi lần dựng lại
  video (đổi độ phân giải, sửa slide, lỗi ffmpeg) là ffmpeg thuần.
- **Chống lệch:** script so `audio_bytes` với file audio thật. Lệch → tự dò lại + ghi
  WARNING (không im lặng dùng mốc của audio cũ). Ép dò lại: `--redetect`.
- **Sửa tay được:** whisper sót mốc nào thì điền vào `marks` (số giây hoặc `"mm:ss"`)
  thay vì phải truyền `--timings` cho cả N slide. Đây là cách vá RẺ NHẤT khi lệch đồng bộ.
- **Audio không xướng "Phần N"** (định dạng podcast 2 giọng — xem finding #8) → `found`
  chỉ có `1`. Biết ngay ở 3.8, và `<audio>.transcript.txt` ĐÃ có sẵn: đọc transcript,
  tìm câu mở đầu từng chủ đề, điền mốc vào `marks`. KHÔNG cần script dump transcript
  riêng, KHÔNG transcribe lần hai.

**Nguyên tắc đồng bộ (bất biến):**
0. **Dải slide phải phủ đúng audio: slide 1 bắt đầu 0:00, tổng thời lượng = độ dài audio.**
   Ảnh luôn phát từ t=0, nên MỌI mốc chỉ có nghĩa khi slide 1 neo ở 0. Mốc nội dung của
   slide 1 (chỗ audio hết mở đầu) KHÔNG phải điểm bắt đầu của slide 1 — phần mở đầu
   thuộc về slide 1. Điền mốc đó vào ô đầu tiên = đẩy TOÀN BỘ slide chạy sớm bằng
   đúng offset ấy. Script nay tự ép về 0 + WARNING, và chặn build nếu tổng thời lượng
   lệch audio > 1s; vẫn phải tự kiểm ở 3.9b vì đây là lỗi im lặng, xem video mới thấy.
1. **Nội dung audio = từ NGUỒN (đầy đủ); slide-script = KHUNG đồng bộ.** Audio giảng chi
   tiết theo source_get_content (ví dụ/số liệu/thao tác); script chỉ cung cấp SỐ PHẦN
   N + TIÊU ĐỀ để xướng "Phần N" cho người nghe lật đúng. Slide là bullet nén — audio
   PHẢI giàu hơn slide, KHÔNG chỉ đọc lại bullet.
2. Slide trước — VERIFY trước — audio sau: VERIFY khóa số slide (page_count == N)
   TRƯỚC khi tạo audio — không đốt 10–20 phút audio cho khung hỏng.
3. **Một nguồn sự thật:** sau 3.3(b), `slide-script.md` là nơi DUY NHẤT chứa tiêu đề.
   KHÔNG trích lại tiêu đề từ PDF, KHÔNG chép tiêu đề sang outline.md — chỉ trỏ tới.

**Fallback 3.5 (chỉ khi 3.6 kích hoạt):** cần soi tiêu đề slide THẬT nhưng PDF của NLM
KHÔNG có text layer (mỗi trang là ảnh) → `get_text()` trả rỗng, và `Read` file PDF hỏng
nếu máy chưa có poppler/pdftoppm. Cách chạy được: render bằng pymupdf rồi ghép contact
sheet để đọc bằng thị giác —
`fitz.open(pdf)[i].get_pixmap(matrix=fitz.Matrix(1.6,1.6))` → PIL thumbnail 760px →
ghép lưới 2×3 (6 slide/sheet) → Read từng sheet. Sau đó SỬA slide-script.md cho khớp
slide thật. Đây là đường tốn context — chỉ dùng khi số trang lệch.

### Phase 4 — WRAP

Khi CEO dừng: tóm tắt tiến độ (x/y bài ✅), nhắc `/learn-lecture <notebook>` để
resume, gợi ý `/session-exit` nếu hết phiên làm việc.

---

## Prompt templates

Xem `references/prompt-templates.md` — 2 template SLIDE và AUDIO với placeholder
`{{N}}`, `{{TÊN_BÀI}}`, `{{DÀN_Ý}}`, `{{SLIDE_CONTENT}}`. Đã kiểm chứng bằng lần
chạy tay 2026-07-22 (bài 1.10 Claude 101, 12 phần).

## Error handling

| Tình huống | Xử lý |
|---|---|
| Auth hết phiên | `nlm login` → retry tối đa 2 → dừng có trạng thái |
| Không thấy notebook | fuzzy match → CEO xác nhận |
| studio_create fail/timeout | **KIỂM `nlm studio status <nb>` TRƯỚC** — timeout MCP thường vẫn tạo xong artifact (xem Gotchas). Chỉ khi status không có artifact mới → retry 1 lần → ghi ⚠ Curriculum.md, hỏi CEO bỏ bài/dừng |
| Slide lệch sau repair | CEO quyết — không lặp vô hạn |
| Notebook >45 nguồn | cảnh báo ở SCAN + đề xuất chọn 1 khóa |
| Video fail (whisper/ffmpeg) | ⚠ ghi Sync Report, giữ slide+audio+marks, KHÔNG chặn bài |
| Whisper sót mốc "Phần N" | 3.8 in ra `missing` NGAY → điền tay vào `marks` (giây hoặc "mm:ss"); không sửa thì 3.9 nội suy giữa 2 mốc kề + WARNING, syncmap ghi "nội suy" |
| Audio sinh lại (bài làm lại) | `audio_bytes` lệch → script tự dò lại + WARNING (không dùng nhầm mốc audio cũ). Ép: `--redetect` |
| Audio không xướng "Phần N" | 3.8 báo `found: [1]` → đọc `<audio>.transcript.txt` (đã sinh sẵn). **Transcript ĐÚNG THỨ TỰ** → điền `marks` tay theo nội dung (rẻ, tất định). **Transcript ĐẢO thứ tự hoặc MẤT phần** → SINH LẠI, vá sẽ ra video đúng mốc nhưng sai slide |
| Audio ra podcast 2 giọng | Bình thường, ~2/3 số lần. Sinh lại; ngân sách ~3 lượt/bài. Đừng sửa prompt/format/length để "trị" — đã loại hết bằng thực nghiệm (xem gotcha "xổ số ~1/3") |
| Mốc đủ số nhưng lệch nội dung | Audio tự bịa cấu trúc phần riêng → mốc GIẢ. Xử như hỏng: sinh lại, KHÔNG vá |

## Gotchas thực chiến (live-run 2026-07-22, notebook 284 nguồn)

- **BẪY `--timings`: giá trị đầu tiên phải là 0, nếu không CẢ DẢI SLIDE CHẠY SỚM
  (bug thật 2026-07-28, 5 video khoá cowork-persona-sinhvien lệch 74–111 giây).**
  Triệu chứng CEO thấy: "slide chuyển sớm hơn lời", lệch đều từ đầu tới cuối video —
  không phải lệch vài giây ở một mốc. Nguyên nhân: khi đọc transcript để đặt mốc nội
  dung, ta ghi cả mốc của slide 1 (chỗ hết phần mở đầu, ví dụ 1:28) rồi truyền vào
  `--timings` làm giá trị đầu; nhưng ảnh luôn phát từ t=0 nên slide 1 bị rút ngắn đúng
  88s và mọi slide sau dồn lên sớm 88s. Marks-file KHÔNG dính (luôn ép slide 1 = 0).
  Đã vá trong `lecture_video.py`: `explicit_timings()` ép về 0 + WARNING, chặn mốc lùi,
  và main() từ chối build nếu slide 1 ≠ 0 hoặc tổng thời lượng lệch audio > 1s.
  Test hồi quy: `scripts/` (case A1 88s → 0). **Vẫn phải làm 3.9b VERIFY-V** vì lỗi cùng
  loại (nhầm nghĩa mốc) có thể tái xuất ở đường khác.

- **🎲 BƯỚC AUDIO LÀ XỔ SỐ ~1/3 — ĐỪNG ĐI TÌM "NGUYÊN NHÂN" (live-run 2026-07-29→31,
  21 lần sinh + 4 thí nghiệm có đối chứng).** `studio_create(audio)` đôi khi trả đúng một
  giọng giảng bài xướng "Phần N", đôi khi trả **podcast 2 giọng** ("Chào mừng đến với phiên
  đào sâu hôm nay…") không xướng mốc nào, ĐẢO thứ tự các phần, hoặc CẮT hẳn vài phần cuối.
  Tỉ lệ ăn đo được **~30–40%**, và **KHÔNG có tham số nào điều khiển được**. Đã thử và LOẠI
  bằng thực nghiệm — đừng thử lại:
  | Giả thuyết | Phản chứng |
  |---|---|
  | Siết prompt (cấm podcast, ép câu đầu, cấm tự đánh số) | Bài dùng ĐÚNG prompt vừa thắng ở bài trước → vẫn hỏng |
  | Giảm số phần / giảm tải mỗi bài | Bài 6 phần, 6,5K ký tự → vẫn hỏng (trong khi bài 13 phần có lần ăn) |
  | `audio_format="brief"` | Giữ cấu trúc hoàn hảo (6/6 mốc) NHƯNG chỉ ra 2 phút kiểu điện tín — không dùng làm bài giảng được |
  | `audio_format="critique"` | Hỏng y như deep_dive |
  | `audio_length="default"` | Ăn ở bài 6 phần, TRƯỢT ở bài 13 phần |
  **Cách làm đúng:** coi đây là bước chập chờn có ngân sách **~3 lượt sinh/bài**; 3.8 là cổng
  kiểm (biết hỏng TRƯỚC khi tốn công dựng video); `found < N` mà transcript đi ĐÚNG THỨ TỰ
  thì vá mốc tay (rẻ, tất định); transcript ĐẢO thứ tự hoặc MẤT phần thì phải sinh lại, vá
  sẽ ra video "đúng mốc nhưng sai slide". Giữ bản hỏng thành `_vN-podcast-*` để đối chiếu.

- **⚠️ `found == N` CHƯA ĐỦ để kết luận đồng bộ — phải soi MỐC KHỚP NỘI DUNG.** Live-run
  2026-07-30: một bản audio báo `found` 6/12 nghe rất khá, nhưng soi transcript thì là **MỐC
  GIẢ** — audio tự bịa cấu trúc 6 phần của riêng nó, xướng "chuyển sang phần 6" rồi giảng
  nội dung phần 10 trong slide-script. Dựng theo mốc đó ra video lệch slide toàn bộ nửa sau,
  và đây là lỗi IM LẶNG (chỉ lộ khi xem hết video). **Bắt buộc ở 3.8:** in transcript tại
  từng mốc và đối chiếu với tiêu đề trong `slide-script.md` trước khi sang 3.9.

- **OUTLINE:** `notebook_query` timeout 120s / "Connection closed" trên notebook lớn
  → LUÔN dùng `source_get_content` (raw, tức thì) cho OUTLINE. notebook_query chỉ khi
  thật sự cần tổng hợp AI đa nguồn.
- **Polling:** `studio_status` (MCP) trả VỀ TẤT CẢ artifact mỗi lần (~15K token/lần) —
  KHÔNG poll lặp bằng MCP. Poll bằng CLI nền: `nlm studio status <nb>` → parse field
  `status=="completed"` cho `artifact_id` cần, chạy `run_in_background`. Slide ~3–7
  phút, audio ~7–8 phút. (Nếu buộc phải hỏi 1 lần bằng MCP thì truyền `artifact_id=`
  — có lọc, chỉ trả 1 artifact, rẻ.)
- **Trạng thái `unknown` KHÔNG có nghĩa là hỏng (live-run 2026-07-25):** trong lúc đang
  sinh, cả CLI lẫn MCP đều báo `status: "unknown"` chứ không phải `in_progress`, và
  `summary.in_progress` vẫn đếm 0 — dễ kết luận nhầm là xong hoặc lỗi. Tín hiệu đáng
  tin duy nhất: `status=="completed"`, hoặc download thành công (file có bytes).
- **`studio_create` (MCP) có thể TREO rất lâu rồi trả timeout DÙ ĐÃ TẠO XONG artifact
  (live-run 2026-07-31):** gọi `studio_create(audio)` bị treo ~38 phút → harness abort với
  "sent no response or progress"; nhưng `nlm studio status <nb>` cho thấy audio đã
  `completed`. TUYỆT ĐỐI KHÔNG kick lại (đốt quota audio + sinh artifact trùng). Xử:
  liệt kê `studio status` lấy artifact_id mới nhất đúng type → download bình thường.
  Cùng họ với bẫy `unknown`: chỉ `completed`/file-có-bytes mới là tín hiệu thật.
- **`source_get_content` có thể vượt giới hạn token của tool** — nguồn PDF ~100 trang
  trả ~220K ký tự, tool ghi ra file thay vì trả nội dung. Cách xử: python đọc file JSON
  (`{content, title, char_count}`), tìm offset của chương cần bằng `re.finditer` trên
  tiêu đề mục (chú ý tiêu đề xuất hiện nhiều lần: lần đầu ở MỤC LỤC, lần sau mới là
  thân chương — lấy lần xuất hiện của thân chương), cắt slice rồi mới Read. Với sách
  chia nhiều part, LUÔN phải làm bước cắt này.
- **Download AUDIO:** MCP `download_artifact(audio)` hay trả "Download failed" →
  fallback CLI `nlm download audio <nb> --id <aid> --no-progress -o <path.m4a>`
  (chạy ổn; file ~17–40MB tùy độ dài). Slide_deck qua MCP `download_artifact` thì OK.
- **Audio propagation delay (finding #7, live-run 2026-07-23):** sau khi audio
  `status=="completed"`, URL download có thể CHƯA live ~1–3 phút → cả CLI lẫn MCP
  download trả "Download failed" dù đã completed (KHÔNG phải auth, KHÔNG phải fail
  thật). Xử: retry download mỗi 30s, tối đa ~6 phút. Pattern gọn nhất = 1 script nền
  làm cả 2 phase: poll `status==completed` → rồi retry-download tới khi thấy
  "Downloaded" (ghi bytes ra file). Tránh gọi download foreground rồi kết luận fail sớm.
- **studio_create prompt:** đặt full prompt vào `focus_prompt`; set `language="vi"`,
  `source_ids=[...]`, `confirm=true`, `slide_format="detailed_deck"`. Audio:
  `audio_format="deep_dive"` (các format khác đã thử và loại — xem gotcha "xổ số ~1/3"),
  `audio_length="long"` cho bài ≥10 phần, `"default"` cho bài ≤8 phần. **LƯU Ý: hai giá trị
  length này KHÔNG quyết định thành bại** — chỉ là chọn độ dài mong muốn, đừng kỳ vọng đổi
  length sẽ sửa được lỗi podcast (đã kiểm chứng: `default` ăn ở bài 6 phần, trượt ở bài
  13 phần).
- **Ghim phạm vi khi nguồn là chunk nhiều chương:** nguồn thường là 1 file ~100 trang
  chứa vài chương. Trong `focus_prompt` phải có 1 khối "PHẠM VI BẮT BUỘC" nêu số mục +
  tiêu đề tiếng Anh gốc + khoảng trang + câu "BỎ QUA HOÀN TOÀN mọi nội dung khác trong
  file: bỏ qua lời tựa, mục lục, Chương X, Chương Y". Live-run 2026-07-25: có khối này
  thì NLM sinh đúng 12/12 slide, đúng tiêu đề, không rò chương khác.
- **Slide PDF của NLM KHÔNG có text layer** — mỗi trang là ảnh, `pymupdf.get_text()`
  trả rỗng. Đây là lý do 3.4 chỉ lấy `page_count`, còn tiêu đề lấy từ `slide-script.md`.
- **Download slide_deck có thể fail vài lần trước khi sẵn sàng** — giống audio, dùng
  vòng retry (`nlm download slide-deck <nb> --id <aid> -o <path>`), coi "file có bytes"
  là tín hiệu hoàn tất. Live-run: thành công ở lần thử thứ 4.
- **CLI env:** `export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"`
  + `PYTHONIOENCODING=utf-8 NO_COLOR=1`. CLI JSON KHÔNG expose url (chỉ id/type/status).
- **Audio fail "Could not create audio" = NGHI AUTH HẾT HẠN TRƯỚC TIÊN.** Session NLM
  ~20 phút; giữa phiên dài auth hết hạn. BẪY: MCP `server_info` trả `auth_status:
  configured` (CACHE CŨ, SAI) — KHÔNG tin nó. Kiểm auth THẬT bằng CLI
  `nlm source content <sid>` → nếu "Authentication expired" → báo CEO chạy `nlm login`
  (interactive, Claude không tự chạy được) → sau đó `refresh_auth` hoặc retry.
  CHỈ khi auth OK mà audio vẫn fail mới nghĩ tới quota audio/ngày. Xử khi kẹt: lưu
  slide + Sync Report ghi audio ⚠ deferred + prompt audio 12 phần trong outline.md →
  retry đầu phiên resume sau `nlm login`. KHÔNG lặp retry mù.
- **NLM tự cân đối độ dài đoạn audio (live-run 2026-07-25):** dù prompt liệt kê chi tiết
  từng phần, NLM vẫn nén phần nội dung dày và giãn phần mỏng — đo được qua syncmap:
  phần dày nhất chỉ 1:33 còn một phần khác tụt xuống 0:32 trong khi các phần đều ~1:33.
  KHÔNG sửa được bằng cách viết prompt dài hơn cho phần đó. Cách xử ĐÚNG: ở 3.2, tách
  phần quá dày thành 2 slide riêng ngay trong dàn ý (mỗi slide 1 khái niệm), đừng trông
  đợi audio tự giãn.
- **MỐC dò 1 lần, dùng mãi (v1.4):** whisper là phần đắt nhất của 3.9 (~3–5 phút CPU
  cho audio 15 phút) và trước đây phải chạy lại mỗi lần dựng video. Nay dò ở 3.8
  (`--detect-only`) ghi `<audio>.marks.json`; 3.9 đọc file → dựng lại video chỉ tốn
  ffmpeg. Lợi kép: biết `missing` mốc NGAY sau khi có audio (trước khi dựng), và vá
  lệch đồng bộ bằng cách sửa 1 dòng JSON thay vì truyền `--timings` cho cả N slide.
- **VIDEO (live-run 2026-07-22, Bài 1 AI Fluency 12/12 mốc):** ffmpeg KHÔNG có trên
  PATH → dùng binary bundle của `imageio_ffmpeg.get_ffmpeg_exe()` (pip: imageio-ffmpeg,
  pymupdf, faster-whisper — cài sẵn Python312). Whisper `info.duration` có thể NGẮN hơn
  mp3 thật (VAD) → script tự parse Duration từ `ffmpeg -i` và cắt `-t` đúng độ dài
  (không có -t: concat demuxer thừa ~40s slide cuối câm). Windows console cp1252 →
  script tự wrap stdout UTF-8. Chi tiết: `references/video-build.md`.

## RULES

- KHÔNG tự thêm nguồn vào notebook (việc của `/nlm add` / deep-research).
- KHÔNG transcribe audio để kiểm chứng NỘI DUNG (đồng bộ theo xây dựng là đủ) —
  transcribe CHỈ để lấy word-timestamps mốc "Phần N", và CHỈ MỘT LẦN ở 3.8
  (`--detect-only` → `<audio>.marks.json`). Bước 3.9 và mọi lần dựng lại video ĐỌC
  file mốc đó, KHÔNG transcribe lại.
- KHÔNG tạo video bằng NLM studio (video artifact NLM không đồng bộ với slide deck);
  video bài giảng dựng CỤC BỘ ở 3.9 từ chính slide+audio đã verify. KHÔNG tạo
  infographic/quiz.
- KHÔNG tự sản xuất bài khi CEO chưa chọn — mỗi vòng lặp có gate Core.
- COD: SCAN + sản xuất = Offload · chọn mode, duyệt giáo trình, chọn bài, xử lệch = Core.
