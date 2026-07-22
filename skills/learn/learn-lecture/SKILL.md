---
name: learn-lecture
description: >-
  Turn a NotebookLM notebook into a synchronized lecture series — per lesson: slide
  deck + Vietnamese audio that announces "Phần N" in lockstep with the slides. Scans
  all sources, proposes a curriculum in 3 modes (compact/full/extend), CEO picks
  lessons one by one; auto-selects sources per lesson, creates slides, extracts REAL
  slide content, generates audio from it, verifies sync, downloads both to the vault,
  and resumes across sessions via Curriculum.md. Triggers on: "learn lecture",
  "lecture from notebook", "lecture series", "synced slide audio", "tạo bài giảng",
  "bài giảng từ notebook", "tạo bộ bài giảng", "giáo trình từ notebook", "slide audio
  đồng bộ", "bài giảng đồng bộ".
---

Biến một NotebookLM notebook thành bộ bài giảng đồng bộ slide + audio tiếng Việt.

Usage: `/learn-lecture <notebook-name-or-alias>` — flags: `--mode compact|full|extend`, `--resume`, `--lesson <N>`

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
→ Phase 3 LESSON LOOP (per bài, 8 bước) → Phase 4 WRAP
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

### Phase 3 — LESSON LOOP (8 bước / bài)

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
3.4 EXTRACT   download_artifact(slide_deck→PDF) về vault → Read PDF → đọc nội dung
              slide THẬT (tiêu đề + bullet từng slide) = ground truth cho audio
3.5 VERIFY-S  So slide thật vs dàn ý duyệt: đủ N? tiêu đề khớp? PASS → 3.7
3.6 REPAIR    lệch → tối đa 1 vòng studio_revise (hoặc tạo lại) → quay lại 3.4;
              vẫn lệch → CEO quyết: chấp nhận có ghi chú / bỏ bài (⚠ skipped)
3.7 AUDIO     sinh prompt audio TỪ nội dung slide THẬT — không dùng lại dàn ý gốc:
              N đoạn khớp 1-1, mỗi đoạn mở bằng "Phần N — <tiêu đề slide thật>".
              Tự kiểm prompt đủ N callout khớp tiêu đề TRƯỚC khi gửi.
              studio_create(audio) — LUÔN language=vi (bắt buộc, rule /nlm; chỉ đổi
              khi CEO yêu cầu rõ tiếng Anh) → poll completion qua CLI nền
3.8 SAVE      tải slide PDF (download_artifact) + audio (CLI `nlm download audio
              --id <aid> -o` — MCP download_artifact AUDIO hay fail) → <vault-root>\
              Bai-NN-<slug>\ + outline.md (dàn ý duyệt + slide content trích + Sync
              Report) + cập nhật Curriculum.md → hỏi "Tạo bài tiếp theo? (bài N+1)"
```

**Nguyên tắc đồng bộ (bất biến):**
1. Slide trước — audio sau — audio sinh từ slide THẬT. NLM có tự gộp slide thì
   audio vẫn khớp bộ slide thực tế.
2. VERIFY chạy TRƯỚC khi tạo audio — không đốt 10–20 phút audio cho bộ slide hỏng.

**Fallback 3.4:** API không trả được text slide → fallback dùng dàn ý duyệt ở 3.2
làm nguồn audio prompt; Sync Report ghi rõ "đồng bộ mức dàn ý, chưa đối chiếu
slide thật".

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
  (chạy ổn; file ~20–25MB/15 phút). Slide_deck qua MCP `download_artifact` thì OK.
- **studio_create prompt:** đặt full prompt vào `focus_prompt`; set `language="vi"`,
  `source_ids=[...]`, `confirm=true`, `slide_format="detailed_deck"`.
- **CLI env:** `export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"`
  + `PYTHONIOENCODING=utf-8 NO_COLOR=1`. CLI JSON KHÔNG expose url (chỉ id/type/status).

## RULES

- KHÔNG tự thêm nguồn vào notebook (việc của `/nlm add` / deep-research).
- KHÔNG transcribe audio để kiểm chứng sâu (đồng bộ theo xây dựng là đủ).
- KHÔNG tạo video/infographic/quiz — chỉ slide + audio.
- KHÔNG tự sản xuất bài khi CEO chưa chọn — mỗi vòng lặp có gate Core.
- COD: SCAN + sản xuất = Offload · chọn mode, duyệt giáo trình, chọn bài, xử lệch = Core.
