# learn-lecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `/learn-lecture` skill — NotebookLM notebook → CEO-approved curriculum → per-lesson synchronized slide deck + Vietnamese audio, with resume via Curriculum.md.

**Architecture:** Single markdown skill (Approach A from spec) at `skills/learn/learn-lecture/SKILL.md` with a 5-phase pipeline and an 8-step per-lesson loop; prompt templates live in `references/prompt-templates.md`. Validated by a static-mode eval (regex assertions against SKILL.md), per KN-Stack convention for orchestrator skills.

**Tech Stack:** KN-Stack markdown skill + MCP `notebooklm-mcp` tools (referenced by name inside SKILL.md, no code) + `evals/run-eval.sh` static runner.

**Spec:** `docs/superpowers/specs/2026-07-22-learn-lecture-design.md` (approved 2026-07-22). Branch: `feature/learn-lecture`.

## Global Constraints

- Skill frontmatter MUST have `name: learn-lecture` (= directory name) and `description:` with "Triggers on:" phrases in English + Vietnamese (CLAUDE.md rule).
- Audio ALWAYS `language=vi` unless CEO explicitly asks for English (inherited rule from `/nlm` v2.2).
- Slide-first, audio-from-REAL-slide-content; verify slides BEFORE creating audio; repair max 1 round.
- Vault output root: `D:\Workshop_X\2_Areas\CEO-Self\Learning-Architecture\<notebook-slug>\` (D:\ not E:\ — stale-path gotcha).
- CEO gates (Core): mode choice (when no `--mode`), curriculum approval, lesson pick each loop, repair-failure disposition.
- Commit format `[LEARN] ...`; do NOT bump VERSION in this branch (stacked PRs already claim 1.6–1.8) — CHANGELOG `[Unreleased]` entry only.
- Eval file `evals/learn-lecture.json`, `"mode": "static"`, format identical to `evals/fable-gpt.json`.

---

### Task 1: Static eval spec (the failing test)

**Files:**
- Create: `evals/learn-lecture.json`

**Interfaces:**
- Produces: 12 assertion regexes that Task 2's SKILL.md must satisfy. Task 2 authors MUST read this file's regexes verbatim.

- [ ] **Step 1: Write the eval spec**

```json
{
  "skill": "learn-lecture",
  "version": "1.0",
  "description": "Binary assertions for learn-lecture — NotebookLM notebook → synced slide+audio lecture series (scan → curriculum → per-lesson produce/verify loop)",
  "mode": "static",
  "test_input": "tạo bộ bài giảng từ notebook Claude Course 2026, chế độ full",
  "total_required": 12,
  "passing_score": 11,
  "assertions": [
    {
      "id": "LL-FRONTMATTER",
      "name": "frontmatter_name_and_bilingual_triggers",
      "check": "frontmatter có name: learn-lecture + description chứa Triggers on với cụm EN và VI",
      "regex": "name: learn-lecture[\\s\\S]*Triggers on[\\s\\S]*(tạo bài giảng|bài giảng từ notebook)",
      "required": true
    },
    {
      "id": "LL-PHASES",
      "name": "five_phase_pipeline",
      "check": "đủ 5 phase INTAKE / SCAN / CURRICULUM / LESSON LOOP / WRAP",
      "regex": "INTAKE[\\s\\S]*SCAN[\\s\\S]*CURRICULUM[\\s\\S]*LESSON LOOP[\\s\\S]*WRAP",
      "required": true
    },
    {
      "id": "LL-MODE-GATE",
      "name": "mode_chosen_after_scan_when_flag_absent",
      "check": "không có --mode → sau SCAN hiển thị ước tính cả 3 chế độ rồi CEO chọn",
      "regex": "(không|KHÔNG) có --mode[\\s\\S]*(3 chế độ|cả 3|compact.*full.*extend)[\\s\\S]*CEO chọn",
      "required": true
    },
    {
      "id": "LL-CORE-GATE",
      "name": "curriculum_core_gate",
      "check": "Phase 2: CEO duyệt/sửa giáo trình trước khi ghi Curriculum.md — gate Core",
      "regex": "CEO (duyệt|phê duyệt)[\\s\\S]*Curriculum\\.md[\\s\\S]*(Core|CORE)",
      "required": true
    },
    {
      "id": "LL-SOURCE-SCOPE",
      "name": "per_lesson_source_ids_only",
      "check": "outline query và slide của mỗi bài CHỈ dùng source_ids của bài đó",
      "regex": "(CHỈ|chỉ) (dùng|với) source_ids",
      "required": true
    },
    {
      "id": "LL-SLIDE-FIRST",
      "name": "audio_from_real_slide_content",
      "check": "slide tạo trước; audio prompt sinh TỪ nội dung slide THẬT (không dùng lại dàn ý gốc)",
      "regex": "slide (THẬT|thật)[\\s\\S]*(không dùng (lại )?dàn ý gốc|ground truth)",
      "required": true
    },
    {
      "id": "LL-VERIFY-BEFORE-AUDIO",
      "name": "verify_slides_before_audio",
      "check": "VERIFY slide chạy TRƯỚC khi tạo audio — không đốt thời gian audio cho slide hỏng",
      "regex": "(VERIFY|verify)[\\s\\S]{0,200}(TRƯỚC|trước) khi tạo audio",
      "required": true
    },
    {
      "id": "LL-AUDIO-VI",
      "name": "audio_always_vietnamese",
      "check": "audio LUÔN language=vi trừ khi CEO yêu cầu rõ tiếng Anh (rule /nlm)",
      "regex": "language=vi[\\s\\S]*(LUÔN|luôn|bắt buộc)|LUÔN[\\s\\S]{0,80}language=vi",
      "required": true
    },
    {
      "id": "LL-REPAIR-ONCE",
      "name": "repair_max_one_round_then_ceo",
      "check": "repair slide tối đa 1 vòng (studio_revise/tạo lại) → vẫn lệch thì CEO quyết chấp nhận/bỏ bài",
      "regex": "(tối đa|TỐI ĐA) 1 vòng[\\s\\S]*CEO quyết",
      "required": true
    },
    {
      "id": "LL-RESUME",
      "name": "resume_via_curriculum_md",
      "check": "Curriculum.md đã tồn tại → bỏ qua Phase 1-2, vào thẳng LESSON LOOP với bài pending",
      "regex": "Curriculum\\.md (đã )?tồn tại[\\s\\S]*(bỏ qua|skip) Phase 1",
      "required": true
    },
    {
      "id": "LL-FALLBACK",
      "name": "extract_fallback_outline_sync_note",
      "check": "không đọc được nội dung slide → fallback dàn ý duyệt + Sync Report ghi 'đồng bộ mức dàn ý'",
      "regex": "fallback[\\s\\S]*dàn ý[\\s\\S]*đồng bộ mức dàn ý",
      "required": true
    },
    {
      "id": "LL-AUTH-RETRY",
      "name": "auth_fail_nlm_login_retry_two",
      "check": "auth NLM hết phiên → báo CEO chạy nlm login, retry tối đa 2 lần, dừng có trạng thái",
      "regex": "nlm login[\\s\\S]*(tối đa|TỐI ĐA) 2",
      "required": true
    }
  ]
}
```

- [ ] **Step 2: Run eval to verify it fails (SKILL.md not yet written)**

Run: `bash evals/run-eval.sh learn-lecture`
Expected: FAIL — skill file `skills/learn/learn-lecture/SKILL.md` not found (or 0/12 assertions).

- [ ] **Step 3: Commit**

```bash
git add evals/learn-lecture.json
git commit -m "[LEARN] Add learn-lecture static eval spec (12 assertions, red)"
```

---

### Task 2: SKILL.md (make the eval pass)

**Files:**
- Create: `skills/learn/learn-lecture/SKILL.md`

**Interfaces:**
- Consumes: assertion regexes from `evals/learn-lecture.json` (Task 1) — phrasing below already satisfies them; do not paraphrase the quoted key sentences.
- Produces: section `## Prompt templates` referencing `references/prompt-templates.md` (Task 3 creates it) with placeholder tokens `{{N}}`, `{{DÀN_Ý}}`, `{{SLIDE_CONTENT}}`, `{{TÊN_BÀI}}`.

- [ ] **Step 1: Write SKILL.md with the following full content**

````markdown
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

Engine: MCP `notebooklm-mcp` — `notebook_list`, `source_list`, `source_describe`,
`notebook_query` (với `source_ids`), `studio_create`/`studio_status`/`studio_revise`,
`download_artifact`/`export_artifact`.

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

1. `source_list` → lấy toàn bộ title + source_id.
2. Claude gom cụm chủ đề từ TITLE (chỉ `source_describe` khi title mơ hồ —
   KHÔNG query từng nguồn, tốn phiên).
3. Notebook >45 nguồn hoặc 1 cụm quá lớn → cảnh báo, đề xuất extend mode hoặc
   thu hẹp phạm vi.

### Phase 2 — CURRICULUM

1. Nếu KHÔNG có `--mode`: hiển thị tóm tắt cụm chủ đề + ước tính số bài của cả 3
   chế độ (VD: compact ≈ 4 bài · full ≈ 9 · extend ≈ 12) → CEO chọn mode.

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
3.2 OUTLINE   notebook_query CHỈ với source_ids của bài đó → trích dàn ý đầy đủ
              theo thứ tự (mục tiêu, đề mục, khái niệm, ví dụ, thao tác, ghi nhớ;
              giữ nguyên số liệu/tên riêng) → chưng cất thành DÀN Ý ĐÁNH SỐ N phần
3.3 SLIDES    studio_create(slides) với prompt template SLIDE (references/) —
              nhúng dàn ý N phần, ràng buộc "ĐÚNG N slide riêng biệt, không gộp,
              CHỈ dùng nguồn đã chọn" → poll studio_status
3.4 EXTRACT   download/export artifact → đọc nội dung slide THẬT (tiêu đề + bullet
              từng slide) = ground truth cho audio
3.5 VERIFY-S  So slide thật vs dàn ý duyệt: đủ N? tiêu đề khớp? PASS → 3.7
3.6 REPAIR    lệch → tối đa 1 vòng studio_revise (hoặc tạo lại) → quay lại 3.4;
              vẫn lệch → CEO quyết: chấp nhận có ghi chú / bỏ bài (⚠ skipped)
3.7 AUDIO     sinh prompt audio TỪ nội dung slide THẬT — không dùng lại dàn ý gốc:
              N đoạn khớp 1-1, mỗi đoạn mở bằng "Phần N — <tiêu đề slide thật>".
              Tự kiểm prompt đủ N callout khớp tiêu đề TRƯỚC khi gửi.
              studio_create(audio) — LUÔN language=vi (bắt buộc, rule /nlm; chỉ đổi
              khi CEO yêu cầu rõ tiếng Anh) → poll studio_status
3.8 SAVE      tải PPTX + MP3 → <vault-root>\Bai-NN-<slug>\ + outline.md (dàn ý
              duyệt + slide content trích + Sync Report) + cập nhật Curriculum.md
              → hỏi "Tạo bài tiếp theo? (bài N+1)"
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
| Notebook >45 nguồn | cảnh báo ở SCAN |

## RULES

- KHÔNG tự thêm nguồn vào notebook (việc của `/nlm add` / deep-research).
- KHÔNG transcribe audio để kiểm chứng sâu (đồng bộ theo xây dựng là đủ).
- KHÔNG tạo video/infographic/quiz — chỉ slide + audio.
- KHÔNG tự sản xuất bài khi CEO chưa chọn — mỗi vòng lặp có gate Core.
- COD: SCAN + sản xuất = Offload · chọn mode, duyệt giáo trình, chọn bài, xử lệch = Core.
````

- [ ] **Step 2: Run eval to verify it passes**

Run: `bash evals/run-eval.sh learn-lecture`
Expected: PASS ≥11/12 (target 12/12). If an assertion fails, fix SKILL.md phrasing to match the regex (do NOT loosen the regex to pass).

- [ ] **Step 3: Commit**

```bash
git add skills/learn/learn-lecture/SKILL.md
git commit -m "[LEARN] Add learn-lecture skill — notebook → synced slide+audio lecture series (eval green)"
```

---

### Task 3: Prompt templates reference

**Files:**
- Create: `skills/learn/learn-lecture/references/prompt-templates.md`

**Interfaces:**
- Consumes: placeholder names promised by Task 2 (`{{N}}`, `{{TÊN_BÀI}}`, `{{DÀN_Ý}}`, `{{SLIDE_CONTENT}}`).

- [ ] **Step 1: Write the file with both templates (proven in the 2026-07-22 manual run)**

````markdown
# learn-lecture — Prompt Templates

Placeholder: `{{N}}` = số phần · `{{TÊN_BÀI}}` = tên bài · `{{DÀN_Ý}}` = dàn ý đánh
số N phần (mỗi dòng: `N. <Tiêu đề> — <ý chính, số liệu giữ nguyên>`) ·
`{{SLIDE_CONTENT}}` = nội dung slide THẬT trích ở bước 3.4 (mỗi slide: tiêu đề +
bullet). Nguồn: đã tick sẵn đúng source_ids của bài trước khi gửi prompt.

## TEMPLATE 1 — SLIDE (studio_create, artifact_type=slides)

```
Tạo một slide deck bài giảng tiếng Việt cho "{{TÊN_BÀI}}". Giữ nguyên thuật ngữ
tiếng Anh. CHỈ dùng thông tin trong nguồn đã chọn, KHÔNG thêm kiến thức ngoài,
KHÔNG bịa số liệu.

Bắt buộc đủ {{N}} slide RIÊNG BIỆT, không gộp, ĐÚNG thứ tự và tiêu đề dưới đây;
mỗi slide 1 ý chính + 3–5 gạch đầu dòng NGẮN (không đoạn văn dài):

{{DÀN_Ý}}

Phong cách: sạch, ít chữ, mỗi slide một khái niệm; ưu tiên bảng/mũi tên cho slide
so sánh và sơ đồ. Ngôn ngữ: tiếng Việt.
```

## TEMPLATE 2 — AUDIO (studio_create, artifact_type=audio, language=vi BẮT BUỘC)

```
Tạo một bài giảng audio tiếng Việt cho "{{TÊN_BÀI}}". Giữ nguyên thuật ngữ tiếng
Anh. CHỈ dùng thông tin trong nguồn đã chọn, KHÔNG thêm kiến thức ngoài, KHÔNG bịa
số liệu.

QUAN TRỌNG — audio này phải ĐỒNG BỘ với một slide deck {{N}} slide. Chia lời giảng
thành ĐÚNG {{N}} đoạn, ĐÚNG thứ tự dưới đây. Ở đầu mỗi đoạn, XƯỚNG RÕ số và tên
phần (ví dụ: "Phần 4 — <tiêu đề>") để người nghe lật đúng slide. Mỗi đoạn chỉ diễn
giảng nội dung của slide tương ứng, không lan man sang phần khác.

Nội dung {{N}} phần (khớp 1-1 với slide thật):
{{SLIDE_CONTENT}}

Giọng: người dẫn giảng bài rõ ràng, mạch lạc, sư phạm. Ngôn ngữ: tiếng Việt.
```

## Checklist tự kiểm trước khi gửi TEMPLATE 2

- [ ] Số đoạn == số slide thật (không phải N kế hoạch, nếu đã chấp-nhận-có-ghi-chú)
- [ ] Tiêu đề từng đoạn == tiêu đề slide thật, đúng thứ tự
- [ ] `language=vi` đã set
````

- [ ] **Step 2: Re-run eval (references must not break anything)**

Run: `bash evals/run-eval.sh learn-lecture`
Expected: PASS (same score as Task 2 — eval only reads SKILL.md).

- [ ] **Step 3: Commit**

```bash
git add skills/learn/learn-lecture/references/prompt-templates.md
git commit -m "[LEARN] learn-lecture: add slide/audio prompt templates (proven 2026-07-22 manual run)"
```

---

### Task 4: CHANGELOG + deployment check

**Files:**
- Modify: `CHANGELOG.md` (top, inside `## [Unreleased]` → `### Added`)

**Interfaces:**
- Consumes: nothing new. VERSION bump deliberately deferred to merge (stacked-PR practice — 1.6–1.8 claimed by other branches).

- [ ] **Step 1: Add CHANGELOG entry under `## [Unreleased]` / `### Added`**

```markdown
- NEW skill `learn/learn-lecture` — NotebookLM notebook → bộ bài giảng đồng bộ slide + audio tiếng Việt. Pipeline 5 phase (INTAKE → SCAN → CURRICULUM CEO-gate → LESSON LOOP 8 bước → WRAP); 3 chế độ giáo trình compact/full/extend (không `--mode` → CEO chọn sau SCAN); đồng bộ theo xây dựng: slide tạo trước → đọc nội dung slide THẬT → audio sinh từ đó, xướng "Phần N" khi chuyển slide; VERIFY slide chạy trước khi tạo audio, repair tối đa 1 vòng; resume qua Curriculum.md state file; output PPTX+MP3+outline.md về `2_Areas/CEO-Self/Learning-Architecture/<notebook>/`. Tự động hóa quy trình chạy tay 2026-07-22 (bài 1.10 Claude 101). Adds 1 skill.
- `evals/learn-lecture.json` (static, 12 assertions: bilingual triggers, 5-phase, mode-gate-after-scan, curriculum Core gate, per-lesson source_ids scope, audio-from-real-slides, verify-before-audio, language=vi, repair-once, resume, extract-fallback, auth-retry-2).
```

- [ ] **Step 2: Verify deployment via junction**

Run: `bash setup.sh --status`
Expected: learn domain count tăng 3 → 4; no junction errors. (Junctions expose the new directory immediately — no install step needed; if `--status` shows otherwise, run `bash setup.sh --verify` and report.)

- [ ] **Step 3: Final full-eval run**

Run: `bash evals/run-eval.sh learn-lecture`
Expected: PASS 12/12 (≥11 acceptable per spec `passing_score`).

- [ ] **Step 4: Commit**

```bash
git add CHANGELOG.md
git commit -m "[LEARN] CHANGELOG: learn-lecture entry under Unreleased (VERSION bump deferred to merge)"
```

---

## Self-review notes

- Spec coverage: §2 identity→Task 2 frontmatter/usage; §3 phases→Task 2 pipeline; §4 modes+Curriculum→Task 2 Phase 2; §5 loop+sync→Task 2 Phase 3 + Task 3 templates; §6 errors→Task 2 table; §7 eval→Task 1 + Task 4; §8 YAGNI→Task 2 RULES. No gaps.
- Placeholders: `{{...}}` tokens in templates are the deliverable's own placeholder syntax, not plan placeholders.
- Consistency: assertion regexes in Task 1 were written against the exact SKILL.md phrasing in Task 2 (checked line-by-line: "CHỈ với source_ids", "slide THẬT", "không dùng lại dàn ý gốc", "TRƯỚC khi tạo audio", "LUÔN language=vi", "tối đa 1 vòng…CEO quyết", "Curriculum.md đã tồn tại…bỏ qua Phase 1", "đồng bộ mức dàn ý", "nlm login…tối đa 2").
