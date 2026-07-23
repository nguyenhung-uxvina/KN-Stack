---
name: learn-lecture
description: >-
  Turn a NotebookLM notebook into a synchronized lecture series — per lesson: slide
  deck + Vietnamese audio that announces "Phần N" in lockstep with the slides. Scans
  all sources, proposes a curriculum in 3 modes (compact/full/extend), CEO picks
  lessons one by one; auto-selects sources per lesson, creates slides, extracts REAL
  slide titles as a sync skeleton, generates audio from the FULL source content (not
  the compressed slide bullets) chunked to match the slides, downloads both to the vault,
  then builds a synchronized MP4 video (slides auto-advance at each spoken "Phần N"
  via whisper word-timestamps), and resumes across sessions via Curriculum.md.
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
| Slide/bài (N) | ~8 | ~12 | 12; bài mở rộng ~15 |
| Audio/bài | 8–10 phút | 13–16 phút | 15–25 phút |

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
              nguyên số liệu/tên riêng) → chưng cất thành DÀN Ý ĐÁNH SỐ N phần
3.3 SLIDES    studio_create(slide_deck, source_ids, language=vi) với prompt template
              SLIDE (references/) — nhúng dàn ý N phần, ràng buộc "ĐÚNG N slide riêng
              biệt, không gộp, CHỈ dùng nguồn đã chọn". Poll completion QUA CLI nền
              (không gọi studio_status MCP lặp — nó dump TẤT CẢ artifact, tốn context)
3.4 EXTRACT   download_artifact(slide_deck→PDF) về vault → Read PDF → đọc tiêu đề +
              THỨ TỰ slide THẬT = KHUNG ĐỒNG BỘ cho audio (số phần N + tiêu đề từng
              phần). LƯU Ý: slide chỉ là khung — nội dung audio KHÔNG lấy từ bullet
              slide (bullet đã nén), mà lấy từ dàn ý-nguồn ở 3.2 (đầy đủ)
3.5 VERIFY-S  So slide thật vs dàn ý duyệt: đủ N? tiêu đề khớp? PASS → 3.7
3.6 REPAIR    lệch → tối đa 1 vòng studio_revise (hoặc tạo lại) → quay lại 3.4;
              vẫn lệch → CEO quyết: chấp nhận có ghi chú / bỏ bài (⚠ skipped)
3.7 AUDIO     sinh prompt audio với nội dung LẤY TRỰC TIẾP & ĐẦY ĐỦ TỪ NGUỒN (dàn ý-
              nguồn 3.2 / source_get_content — chi tiết, ví dụ, số liệu, thao tác, sâu
              hơn bullet slide), MAP lên KHUNG slide thật: N đoạn = N slide thật, mỗi
              đoạn mở "Phần N — <tiêu đề slide THẬT>" rồi giảng đầy đủ nội dung nguồn
              của phần đó. Nếu slide thật gộp/khác N kế hoạch → gom lại các phần dàn ý
              cho khớp SỐ & TIÊU ĐỀ slide thật (đồng bộ ưu tiên khung slide thật).
              Tự kiểm: mỗi đoạn khai triển từ nguồn (không chỉ đọc lại bullet) + N
              callout khớp tiêu đề slide thật TRƯỚC khi gửi.
              studio_create(audio) — LUÔN language=vi (bắt buộc, rule /nlm; chỉ đổi
              khi CEO yêu cầu rõ tiếng Anh) → poll completion qua CLI nền
3.8 SAVE      tải slide PDF (download_artifact) + audio (CLI `nlm download audio
              --id <aid> -o` — MCP download_artifact AUDIO hay fail) → <vault-root>\
              Bai-NN-<slug>\ + outline.md (dàn ý duyệt + slide content trích + Sync
              Report)
3.9 VIDEO     (bỏ qua nếu --no-video) dựng MP4 đồng bộ từ PDF+audio đã tải:
              `python D:\KN-Stack\scripts\lecture_video.py --pdf <slides.pdf>
              --audio <audio.mp3> --out <Bai-NN-video.mp4>` — tách slide→PNG,
              faster-whisper (word timestamps, vi) dò mốc giọng đọc xướng "Phần N"
              → slide N hiện đúng mốc đó (mốc sót → nội suy, ghi WARNING), ffmpeg
              ghép h264+AAC cắt đúng độ dài audio, sinh syncmap.md. Transcribe
              ~15 phút audio ≈ 3–5 phút CPU → chạy run_in_background. Ghi kết quả
              vào Sync Report + cập nhật Curriculum.md → hỏi "Tạo bài tiếp theo?
              (bài N+1)". Video fail → ⚠ ghi chú, KHÔNG chặn bài (slide+audio đã đủ)
```

**Nguyên tắc đồng bộ (bất biến):**
1. **Nội dung audio = từ NGUỒN (đầy đủ); slide = KHUNG đồng bộ.** Audio giảng chi
   tiết theo source_get_content (ví dụ/số liệu/thao tác); slide chỉ cung cấp SỐ PHẦN
   N + TIÊU ĐỀ để xướng "Phần N" cho người nghe lật đúng. Slide là bullet nén — audio
   PHẢI giàu hơn slide, KHÔNG chỉ đọc lại bullet. NLM có tự gộp slide thì gom lại các
   phần dàn ý-nguồn cho khớp SỐ & TIÊU ĐỀ slide thật.
2. Slide trước — VERIFY trước — audio sau: VERIFY khóa KHUNG slide thật (N + tiêu đề)
   TRƯỚC khi tạo audio — không đốt 10–20 phút audio cho khung hỏng.

**Fallback 3.4:** không đọc được PDF slide (không lấy được tiêu đề thật) → dùng dàn ý
duyệt ở 3.2 vừa làm nội dung audio vừa làm khung đồng bộ; Sync Report ghi rõ "đồng bộ
theo dàn ý kế hoạch, chưa đối chiếu tiêu đề slide thật". (Nội dung audio KHÔNG bị ảnh
hưởng — luôn từ nguồn; chỉ khung tiêu đề là mức kế hoạch.)

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
| studio_create fail/timeout | retry 1 lần → ghi ⚠ Curriculum.md, hỏi CEO bỏ bài/dừng |
| Slide lệch sau repair | CEO quyết — không lặp vô hạn |
| Notebook >45 nguồn | cảnh báo ở SCAN + đề xuất chọn 1 khóa |
| Video fail (whisper/ffmpeg) | ⚠ ghi Sync Report, giữ slide+audio, KHÔNG chặn bài |
| Whisper sót mốc "Phần N" | script tự nội suy giữa 2 mốc kề + WARNING; syncmap ghi "nội suy" |

## Gotchas thực chiến (live-run 2026-07-22, notebook 284 nguồn)

- **OUTLINE:** `notebook_query` timeout 120s / "Connection closed" trên notebook lớn
  → LUÔN dùng `source_get_content` (raw, tức thì) cho OUTLINE. notebook_query chỉ khi
  thật sự cần tổng hợp AI đa nguồn.
- **Polling:** `studio_status` (MCP) trả VỀ TẤT CẢ artifact mỗi lần (~15K token/lần) —
  KHÔNG poll lặp bằng MCP. Poll bằng CLI nền: `nlm studio status <nb>` → parse field
  `status=="completed"` cho `artifact_id` cần, chạy `run_in_background`. Slide ~3–5
  phút, audio ~7–8 phút.
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
  `source_ids=[...]`, `confirm=true`, `slide_format="detailed_deck"`.
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
- **VIDEO (live-run 2026-07-22, Bài 1 AI Fluency 12/12 mốc):** ffmpeg KHÔNG có trên
  PATH → dùng binary bundle của `imageio_ffmpeg.get_ffmpeg_exe()` (pip: imageio-ffmpeg,
  pymupdf, faster-whisper — cài sẵn Python312). Whisper `info.duration` có thể NGẮN hơn
  mp3 thật (VAD) → script tự parse Duration từ `ffmpeg -i` và cắt `-t` đúng độ dài
  (không có -t: concat demuxer thừa ~40s slide cuối câm). Windows console cp1252 →
  script tự wrap stdout UTF-8. Chi tiết: `references/video-build.md`.

## RULES

- KHÔNG tự thêm nguồn vào notebook (việc của `/nlm add` / deep-research).
- KHÔNG transcribe audio để kiểm chứng NỘI DUNG (đồng bộ theo xây dựng là đủ) —
  transcribe CHỈ để lấy word-timestamps cho bước 3.9 VIDEO.
- KHÔNG tạo video bằng NLM studio (video artifact NLM không đồng bộ với slide deck);
  video bài giảng dựng CỤC BỘ ở 3.9 từ chính slide+audio đã verify. KHÔNG tạo
  infographic/quiz.
- KHÔNG tự sản xuất bài khi CEO chưa chọn — mỗi vòng lặp có gate Core.
- COD: SCAN + sản xuất = Offload · chọn mode, duyệt giáo trình, chọn bài, xử lệch = Core.
