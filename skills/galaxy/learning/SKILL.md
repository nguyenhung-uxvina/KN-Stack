End-to-end meta-learning pipeline v2.0: source intake → deep analysis → DMIR cycle → Galaxy extraction → judgment compounding. The "super skill" combining /analyze + /cycle + /teach + /reflect + /nlm into one learning workflow. Also generates standalone self-study practice documents with step-by-step lessons, exercises, and evaluation rubrics. v2.0 adds 10 NLM Mastery Archetypes for specialized deep extraction.

Usage: /learning <topic_or_source> [--mode full|quick|review|practice|refresh|update] [--notebook <alias>] [--project <project-id>] [--weeks N] [--level novice|intermediate|advanced] [--nlm-archetype feynman|briefing|skeptic|miner|study|roadmap|structure|cross-std|failures|socratic]

PATH setup (required for NLM commands):
```bash
export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"
export PYTHONIOENCODING=utf-8
export NO_COLOR=1
```

---

## PIPELINE FLOW

```
[1] Source Intake (file, URL, transcript, or topic)
     ↓
[1G] Source Quality Gate (if NLM path: verify ingestion, recover fails, CEO approve)
     ↓
[2] Deep Analysis (/analyze framework OR NLM deep dive)
     ↓
[3] Three Laws Extraction (distill to 3 irreducible principles)
     ↓
[4] DMIR Cycle Plan (/cycle — if skill-building needed)
     ↓
[5] Galaxy Harvest (THỊNH H — atomic notes from analysis)
     ↓
[6] Decision Bridge (/teach — connect learning to active project decisions)
     ↓
[7] Reflection Capture (update skill stack + judgment calibration)
```

---

## MODE: FULL (default — all 7 steps)

### STEP 1: SOURCE INTAKE

Identify what the CEO wants to learn from:

| Source Type | Action | Tool |
|------------|--------|------|
| File in vault | Read directly | Read tool |
| URL / article | Fetch or add to NLM | WebFetch / nlm source add |
| YouTube video(s) | Run /yt-search first | yt-dlp |
| Book chapter (PDF) | Read + extract | Read tool (PDF mode) |
| Raw topic (no source) | Search → gather | /research pipeline |
| Voice transcript | Process via MCP | tana-iparag-bridge |
| Past analysis output | Read from 3_Resources/ | Read tool |

**CEO gate:** Confirm source and learning objective before proceeding.

Ask:
- Nguồn gì? (file path, URL, topic)
- Mục tiêu học? (hiểu concept / xây skill / ra quyết định / viết Galaxy note)
- Dự án liên quan? (để bridge learning → action)
- Thời gian? (quick 30min / deep 2h / cycle nhiều tuần)

### STEP 2: DEEP ANALYSIS

**Option A: Claude inline** (source < 5,000 words, quick analysis)
Run /analyze logic inline — 5 phases:
1. Content extraction (thesis, variables, gaps)
2. Systems Thinking (stocks, flows, loops, archetypes, leverage)
3. Meta-Learning (Feynman, chunking, mnemonic, rubric, drills)
4. First-Principles Debate (3-7 debate points, current vs fundamental)
5. ARCHITECT framework (reduction, layers, Three Laws)

**Option B: NLM-powered** (source > 5,000 words OR multiple sources)
```bash
# Create or reuse notebook
nlm notebook create "Learning: {{topic}}"
nlm alias set learn-{{short}} {{uuid}}

# Add ALL sources FIRST (batch before any queries)
nlm source add learn-{{short}} --url "{{url1}}"
nlm source add learn-{{short}} --url "{{url2}}"
# ... add all sources
```

**Option C: Hybrid** (best for substantial content)
- NLM processes raw sources (free tokens, handles volume)
- Claude applies /analyze frameworks to NLM output (structured thinking)
- Result: NLM breadth × Claude depth

### Step 1G: SOURCE QUALITY GATE (for Option B/C — v3.1)

After ALL `source add` calls, verify ingestion before querying:

```bash
nlm source list learn-{{short}}
# Compare ingested count vs intended count
```

**1. Check for failed sources:**

```
SOURCE INGESTION REPORT — Learning: {{topic}}
| # | Title/URL | Status | Reason |
|---|-----------|:------:|--------|
| 1 | {{source}} | ✅ OK | |
| 2 | {{source}} | ❌ FAILED | Paywall / 403 / JS-rendered |

Ingested: {{N}} / {{total}}
Failed: {{M}} sources
```

**2. For each failed source — try recovery:**

```
RECOVERY 1: Alt URL → WebSearch "{{title}} filetype:pdf OR preprint"
  → If found → nlm source add --url "{{alt_url}}"

RECOVERY 2: WebFetch → text injection
  → WebFetch original URL → nlm source add --text "{{content}}" --title "{{title}}"

RECOVERY 3: YouTube substitute
  → Search "{{title}} explained" on YouTube → nlm source add --url "{{yt_url}}"

IF ALL FAIL: Log as "✗ UNRECOVERABLE" → add to gap list
```

**3. Present to CEO:**

```
═══ SOURCE QUALITY GATE — Learning: {{topic}} ═══

✅ Ingested: {{N}} sources
🔄 Recovered: {{R}} via alt channel
❌ Failed: {{F}} unrecoverable

FAILED SOURCES (if any):
| # | Source | Why Failed | Impact on Learning |
|---|--------|-----------|-------------------|

CEO OPTIONS:
(1) ✅ Proceed — sources sufficient for learning objective
(2) 📎 CEO adds source manually (provide URL/PDF path)
(3) 🔍 Search deeper for alternatives
(4) ⏸️ Pause — CEO will find source offline

CEO: xác nhận đủ nguồn? Chỉ khi approve mới tiến hành deep query.
```

**STOP. Do NOT run NLM queries until CEO confirms source quality.**

**Skip condition:** If Option A (Claude inline, single source < 5000 words) → skip this gate entirely. Gate only applies to NLM-powered paths (B/C) with multiple sources.

### Deep Query (after CEO approves sources)

```bash
nlm notebook query learn-{{short}} "Analyze this content: (1) What are the 3-5 core principles? (2) What system archetypes are present? (3) What are the common failure modes? (4) What must be true for the author's claims to hold? (5) What dimensions does the author ignore? (6) What are the rate-of-change dynamics?"
```

Save analysis to: `3_Resources/Deep-Content-Analyzer-Outputs/LEARN_{{topic}}_{{date}}.md`

### STEP 3: THREE LAWS EXTRACTION

Distill the analysis to exactly 3 irreducible laws:

```
## Ba Quy Luật — {{topic}}

### Quy Luật 1: {{Tên}} Law
{{Một câu — đủ nhớ, đủ sâu để sinh ra toàn bộ framework}}
- Tại sao đây là quy luật: {{2-3 câu}}
- Phản trực giác: {{điều ngạc nhiên}}

### Quy Luật 2: {{Tên}} Law
{{...}}

### Quy Luật 3: {{Tên}} Law
{{...}}

**Kiểm tra chất lượng:**
- [ ] Mỗi law có thể nhớ sau 1 tuần không đọc lại?
- [ ] 3 laws có thể sinh lại 80% framework?
- [ ] Ít nhất 1 law phản trực giác?
```

**CEO gate:** CEO xác nhận Three Laws trước khi tiếp.

### STEP 4: DMIR CYCLE PLAN (nếu cần xây skill)

Chỉ chạy nếu mục tiêu là skill-building (không chỉ hiểu concept).

Generate using /cycle logic:

```
## D-M-I-R CYCLE — {{topic}}
**Objective:** Sau cycle này, tôi sẽ có thể {{hành động cụ thể, đo được}}
**Duration:** {{2-6 tuần}} | **Hours/week:** {{N}}
**Project anchor:** {{dự án đang chạy — học phải gắn vào việc thật}}

### D — Diagnose
- Dreyfus level hiện tại: {{Novice → Expert}}
- Gaps: {{cụ thể}}
- Baseline test: {{task thử để đo hiện tại}}

### M — Model
- Core framework: {{from Step 2}}
- Three Laws: {{from Step 3}}
- Mental model: {{CLD hoặc concept map}}

### I — Intervene
- Week {{N}}: Apply {{principle}} vào {{project task}}
- Deliberate practice: {{drill cụ thể}}
- Feedback loop: {{từ đâu, bao lâu}}

### R — Reflect
- Galaxy output target: {{N}} notes
- Skill reassessment: {{Dreyfus re-evaluation}}
- Next cycle: {{Y/N, topic}}
```

### STEP 5: GALAXY HARVEST

Scan analysis + Three Laws cho atomic insights → propose Galaxy candidates:

```
## Galaxy Candidates (THỊNH H — Hóa)

1. "{{insight}}" → proposed title: {{Vietnamese title with dấu}}
   - Cluster: {{A-H}}
   - Hub link: [[{{relevant hub note}}]]
   - Cross-cluster link: [[{{note from different cluster}}]]
   - Answers: {{(1) thay đổi cách thiết kế? / (2) chiến lược? / (3) cảnh báo trap?}}

2. ...

CEO: Candidates nào promote lên Galaxy? (Core decision — KHÔNG tự ý tạo)
```

**Quality gate cho Galaxy candidate:**
- Atomic? (1 concept duy nhất)
- Bằng lời mình? (không copy-paste từ source)
- ≥ 2 wikilinks khả thi?
- Trả lời ≥ 1 trong 3 câu hỏi Galaxy?
- Tiếng Việt có dấu?

### STEP 6: DECISION BRIDGE

Connect learning → active project decisions using /teach logic:

```
## Decision Bridge — {{topic}} × {{project}}

### Quyết định hiện tại bị ảnh hưởng
| Project | Open Question / Decision | Learning Insight | How It Changes the Decision |
|---------|------------------------|-----------------|---------------------------|
| {{project}} | {{question}} | {{Three Law or insight}} | {{cụ thể}} |

### Analogous Past Decisions
{{search DR-* records for similar patterns}}

### New Decision to Record?
Nếu learning dẫn đến quyết định mới → chạy /teach record
```

**CEO gate:** CEO quyết định learning có thay đổi project decision không.

### STEP 7: REFLECTION CAPTURE

```
## Learning Reflection — {{topic}}

### Đã học gì?
- Trước: {{mental model cũ}}
- Sau: {{mental model mới — thay đổi gì?}}
- Surprise: {{điều bất ngờ nhất}}

### Skill Stack Update
- CEO skill affected: {{S1-S5, B-EI/CP/AL/NS}}
- Dreyfus before → after: {{level change}}
- dJ/dt impact: {{judgment tăng ở đâu?}}

### Compound Effect
- Learning này compounds với: {{past learning, Galaxy note, project outcome}}
- Predicted value in 6 months: {{how this compounds}}

### Save To
- Analysis → `3_Resources/Deep-Content-Analyzer-Outputs/`
- DMIR plan → `2_Areas/CEO-Self/Learning-Architecture/`
- Galaxy notes → `5_Galaxy/` (CEO creates after approval)
- Decision record → `1_Projects/{{project}}/decisions/` (via /teach)
```

---

## MODE: QUICK (Steps 1→1G→2→3→5 only — skip DMIR, bridge, reflection)

For when CEO encounters content and wants fast insight extraction without full cycle.

```
/learning "topic or source" --mode quick
```

Flow: Source → Analysis (Option A inline) → Three Laws → Galaxy candidates.
~30 minutes. No DMIR plan, no decision bridge.

---

## MODE: REVIEW (Steps 6→7 only — review past learning)

For weekly/monthly reflection on accumulated learning.

```
/learning --mode review
```

1. Read recent `3_Resources/Deep-Content-Analyzer-Outputs/LEARN_*.md`
2. Read recent Galaxy notes created from learning
3. Read recent decision records from /teach
4. Generate:

```
# LEARNING REVIEW — {{today}}

## Learning Volume
- Analyses this month: {{N}}
- Galaxy notes from learning: {{N}}
- DMIR cycles active: {{N}}
- Three Laws extracted: {{N sets}}

## Compound Check
| Three Laws Set | Source | Used in Decision? | Galaxy Note? | Still Valid? |
|---------------|--------|-------------------|-------------|-------------|
| {{set 1}} | {{source}} | {{Y/N + DR#}} | {{Y/N}} | {{Y/N}} |

## dJ/dt Assessment
- Which judgments improved this month?
- Which learning actually changed a decision? (compound proof)
- Which learning was "interesting but unused"? (Analyst Trap warning)

## Dreyfus Movement
| Skill | Start | Now | Evidence |
|-------|-------|-----|----------|
| {{skill}} | {{level}} | {{level}} | {{what can I do now that I couldn't?}} |

## Next Learning Priority
Based on active projects and skill gaps:
1. {{topic — why — which project}}
2. {{topic}}
```

---

## MODE: PRACTICE (generate self-study & practice document)

Tạo tài liệu tự học step-by-step cho một chủ đề hoặc kỹ năng, bao gồm bài giảng, bài tập, rubric đánh giá, và lịch thực hành. Output là một "mini course" hoàn chỉnh CEO có thể follow từ tuần 1 đến tuần N.

```
/learning <topic> --mode practice [--weeks N] [--level novice|intermediate|advanced] [--project <id>]
```

### PHASE 1: SCOPE DEFINITION

Xác định phạm vi trước khi tạo document:

```
## Scope — {{topic}}
- **Mục tiêu kỹ năng:** Sau khóa tự học, tôi sẽ có thể {{hành động đo được}}
- **Dreyfus hiện tại:** {{Novice / Advanced Beginner / Competent / Proficient / Expert}}
- **Dreyfus mục tiêu:** {{target level}}
- **Thời lượng:** {{N}} tuần × {{M}} giờ/tuần = {{total}} giờ
- **Dự án anchor:** {{project — mỗi bài tập gắn vào dự án thật}}
- **Đánh giá bằng gì:** {{output cụ thể chứng minh skill — không phải quiz}}
```

**CEO gate:** Xác nhận scope trước khi generate document.

### PHASE 2: KNOWLEDGE MAP

Dùng /analyze logic hoặc NLM để xây knowledge map:

1. **Core concepts** — 5-9 concepts chính (chunk size tối ưu cho bộ nhớ)
2. **Dependency tree** — concept nào phải hiểu trước concept nào
3. **Common failure modes** — sai ở đâu khi tự học topic này
4. **Three Laws** — 3 quy luật nền tảng (from Step 3 of full mode)
5. **Skill breakdown** — decompose thành sub-skills đo được

```
## Knowledge Map — {{topic}}

### Dependency Tree
{{concept_1}} (foundation)
  ├── {{concept_2}} (requires 1)
  │   └── {{concept_4}} (requires 2)
  ├── {{concept_3}} (requires 1)
  │   └── {{concept_5}} (requires 2+3)
  └── {{concept_6}} (independent)

### Sub-Skills (đo được)
| # | Sub-Skill | Observable Behavior | Current | Target |
|---|-----------|-------------------|---------|--------|
| 1 | {{sub-skill}} | {{khi nào biết mình đã có skill này}} | {{Y/N}} | {{Y/N}} |
| 2 | ... | ... | | |
```

### PHASE 3: COURSE DOCUMENT GENERATION

Generate tài liệu hoàn chỉnh theo cấu trúc:

```markdown
---
created: {{today}}
type: practice-guide
topic: "{{topic}}"
level: {{novice|intermediate|advanced}}
duration_weeks: {{N}}
hours_per_week: {{M}}
project_anchor: {{project-id}}
tags: [#type/practice-guide, #status/active]
---

# Tài Liệu Tự Học: {{Topic}} — {{Level}}

> Mục tiêu: {{observable skill outcome}}
> Thời lượng: {{N}} tuần × {{M}} giờ/tuần
> Dự án thực hành: {{project name}}

---

## Tổng Quan Khóa Học

### Ba Quy Luật Nền Tảng
1. **{{Law 1}}** — {{1 câu}}
2. **{{Law 2}}** — {{1 câu}}
3. **{{Law 3}}** — {{1 câu}}

### Cấu Trúc Mỗi Tuần
- **Học** (30%): Đọc / xem / nghe — input
- **Làm** (50%): Bài tập thực hành gắn vào dự án — deliberate practice
- **Đánh giá** (20%): Tự chấm rubric + ghi reflection

### Dreyfus Progression Map
| Tuần | Target Level | Evidence of Progress |
|------|-------------|---------------------|
| 1-2  | {{level}} | {{observable behavior}} |
| 3-4  | {{level}} | {{observable behavior}} |
| ...  | {{level}} | {{observable behavior}} |

---

## Tuần {{N}}: {{Tên Chủ Đề}}

### Mục Tiêu Tuần
- [ ] Hiểu: {{concept — Feynman test: giải thích được trong 60 giây}}
- [ ] Làm được: {{skill — chứng minh bằng output}}
- [ ] Nhận ra: {{failure mode — biết khi nào mình sai}}

### Phần Học ({{M × 0.3}} giờ)

**Tài liệu bắt buộc:**
1. {{source 1}} — đọc/xem {{phần cụ thể}} ({{time}})
2. {{source 2}} — focus vào {{section}} ({{time}})

**Ghi chú hướng dẫn:**
- Khi đọc, trả lời: {{câu hỏi diagnostic}}
- Tìm: {{pattern cụ thể liên quan đến Three Laws}}
- Cảnh báo: {{misconception phổ biến ở level này}}

**Mnemonic:** {{nhớ bằng cách nào — acronym, analogy, hình ảnh}}

### Phần Thực Hành ({{M × 0.5}} giờ)

**Bài Tập {{N}}.1: {{Tên}}** ({{difficulty: Easy/Medium/Hard}})
- **Mô tả:** {{task cụ thể}}
- **Dự án:** Áp dụng vào {{project task cụ thể}}
- **Input:** {{những gì cần chuẩn bị}}
- **Output mong đợi:** {{deliverable cụ thể, đo được}}
- **Thời gian:** {{phút/giờ}}
- **Tiêu chí đạt:**
  - [ ] {{criterion 1 — binary, không subjective}}
  - [ ] {{criterion 2}}
  - [ ] {{criterion 3}}
- **Nếu bí:** {{hint — không phải đáp án, mà là câu hỏi gợi ý}}
- **Extension (nếu xong sớm):** {{challenge thêm}}

**Bài Tập {{N}}.2: {{Tên}}** ({{difficulty}})
- {{...tương tự...}}

**Bài Tập Tích Hợp {{N}}.3: {{Tên}}** (Hard — kết hợp nhiều sub-skills)
- **Mô tả:** {{task đòi hỏi synthesis}}
- **Mục đích:** Kiểm tra CEO có thể kết hợp các sub-skills đã học
- {{...}}

### Phần Đánh Giá ({{M × 0.2}} giờ)

**Rubric Tự Đánh Giá — Tuần {{N}}:**

| Dimension | 1 (Chưa đạt) | 3 (Đạt) | 5 (Xuất sắc) |
|-----------|-------------|---------|-------------|
| {{dim 1}} | {{observable behavior}} | {{observable behavior}} | {{observable behavior}} |
| {{dim 2}} | {{...}} | {{...}} | {{...}} |
| {{dim 3}} | {{...}} | {{...}} | {{...}} |

**Scoring:**
- Trung bình < 2: Lặp lại tuần này trước khi qua tuần sau
- Trung bình 2-3: Đạt — qua tuần sau, nhưng ghi lại gaps
- Trung bình > 3: Xem xét skip ahead hoặc tăng difficulty

**Reflection Questions (ghi vào journal):**
1. Điều gì dễ hơn/khó hơn mong đợi? Tại sao?
2. Mental model nào thay đổi so với trước tuần này?
3. Nếu phải dạy ai đó concept này trong 2 phút, tôi sẽ nói gì?
4. Concept này liên quan gì đến {{Three Law N}}?

**Galaxy Candidate Check:**
- Có insight nào đủ atomic để thành Galaxy note? {{Y/N}}
- Nếu có: {{proposed title}} → ghi vào backlog

---

## Tuần {{N+1}}: {{Tên Chủ Đề Tiếp}}
{{...cấu trúc tương tự...}}

---

## Đánh Giá Cuối Khóa

### Capstone Exercise
**Tên:** {{bài tập tổng hợp cuối khóa}}
**Mô tả:** {{task lớn đòi hỏi tất cả sub-skills — gắn vào dự án thật}}
**Thời gian:** {{N}} giờ
**Output:** {{deliverable cụ thể — portfolio piece}}
**Tiêu chí đạt:**
- [ ] {{...}}

### Final Rubric — Full Skill Assessment

| Sub-Skill | Dreyfus Before | Dreyfus After | Evidence |
|-----------|---------------|---------------|----------|
| {{sub-skill 1}} | {{level}} | {{level}} | {{what I can do now}} |
| {{...}} | | | |

### Compound Value Assessment
- Kỹ năng này compounds với kỹ năng nào đã có?
- Dự án nào benefit trực tiếp?
- Galaxy notes đã tạo trong quá trình: {{list}}
- Judgment thay đổi gì? (dJ/dt)

### Next Cycle
- Tiếp tục DMIR cycle? {{Y/N}}
- Nếu có: {{topic + objective}}
- Nếu không: Chuyển sang skill mới — {{recommendation}}
```

Save to: `2_Areas/CEO-Self/Learning-Architecture/PRACTICE_{{topic_slug}}_{{date}}.md`

### PHASE 4: SUPPORTING MATERIALS (optional, CEO request)

Nếu CEO yêu cầu, generate thêm:

| Material | Mục đích | Format |
|----------|----------|--------|
| **Flashcards** | Spaced repetition cho core concepts | Markdown table: Q/A pairs |
| **Cheat Sheet** | Quick reference 1 trang | Condensed markdown |
| **Interleaving Schedule** | Lịch xen kẽ topics tối ưu memory | Weekly calendar |
| **Accountability Template** | Check-in hàng tuần | Markdown checklist |
| **NLM Audio** | Podcast-style deep dive | `nlm audio create <notebook>` |

---

## MODE: REFRESH (re-validate past learning output)

Re-validate a past `/learning` output — check if Three Laws still hold, find newer sources, update Galaxy candidates. Lightweight: 1-3 WebSearches max, not a full `/research` re-run.

```
/learning <topic_or_file> --mode refresh [--notebook <alias>]
```

Where `<topic_or_file>` can be:
- A topic string (searches for matching `LEARN_*.md` in `3_Resources/Deep-Content-Analyzer-Outputs/`)
- A file path to a specific past learning output

### STEP 1: LOCATE PAST OUTPUT

- If file path → read directly
- If topic → search `3_Resources/Deep-Content-Analyzer-Outputs/LEARN_*` for match (Glob + Grep)
- If multiple matches → present list, CEO picks
- Extract: Three Laws, Galaxy candidates (promoted? unused?), source list, date
- **Fallback:** If file has no Three Laws section (older format or created via `/analyze`), offer to run quick Three Laws extraction first before refresh

### STEP 2: STALENESS CHECK

```markdown
## Refresh Check — {{topic}}
Original date: {{date}} ({{N}} days ago)

### Three Laws Validity
| # | Law | Still Valid? | Evidence |
|---|-----|-------------|----------|
| 1 | {{law}} | ✓/⚠/✗ | {{why — new info, project experience, or Galaxy note contradicts?}} |
| 2 | {{law}} | ✓/⚠/✗ | {{...}} |
| 3 | {{law}} | ✓/⚠/✗ | {{...}} |

### Source Freshness
- Original sources: {{N}}
- Sources > 1 year old: {{N}}
- Field has evolved since analysis? {{Y/N — check via quick WebSearch}}

### Galaxy Status
- Candidates proposed: {{N}}
- Promoted to Galaxy: {{N}} (which?)
- Still in backlog: {{N}} (still worth promoting?)
- Used in decisions: {{N}} (which DR-*?)
```

Cross-check Three Laws against:
1. Current Galaxy notes (any new note that contradicts or refines a Law?)
2. Active project experience (did applying the Law work? fail?)
3. Quick WebSearch for newer sources on each Law's domain

### STEP 3: TARGETED UPDATE (if staleness found)

- If any Law marked ⚠/✗ → run quick WebSearch for newer sources on that specific law
- If `--notebook` provided → query NLM for updated perspective
- If field evolved → propose revised Three Laws (CEO validates — Core)
- If Galaxy candidates still in backlog → re-evaluate: still worth promoting?

### STEP 4: OUTPUT

**Append** refresh section to original file (never overwrite original analysis):

```yaml
---
refreshed: {{today}}
refresh_result: valid | partial-update | major-revision
---
```

```markdown
## Refresh — {{today}}

### Changes
- Law {{N}} revised: {{old}} → {{new}} (reason: {{...}})
- New source found: {{citation}}
- Galaxy candidate "X" promoted / dropped (reason)

### Next Refresh
- Recommended: {{date}} ({{N}} months from now)
- Trigger: {{what would invalidate these laws}}
```

**If all 3 Laws still valid + no new sources → output:**
```
✓ Still valid, next refresh {{date+3months}}
```
Don't force changes when none are needed.

### REFRESH RULES
- **Append-only** — never overwrite original analysis (it's a record)
- **Lightweight** — 1-3 WebSearches max, not a full /research re-run
- **CEO validates** any Law revision (Core per COD)
- **Staleness threshold:** Analysis > 90 days old = recommend refresh
- Link to Galaxy: [[Temporal Lifecycle — Khi Permanent Note Lỗi Thời]], [[Vault = Graveyard nếu không có Harvest]]

---

## MODE: UPDATE (add new sources to existing notebook, re-analyze)

Incremental learning — add new sources to an existing NLM notebook, run delta analysis, produce update output without touching the original file.

```
/learning <topic> --mode update --notebook <existing-alias>
```

**When to use:** CEO learned a topic before (has `LEARN_*.md` + NLM notebook), now has new sources (new article, new book chapter, new video, CEO's own experience notes) or wants to deepen coverage.

### Pipeline

```
[U1] LOAD EXISTING STATE
     → Read LEARN_{{topic}}_{{original_date}}.md (Three Laws, Galaxy candidates)
     → nlm source list {{notebook}} → current source inventory
     → Identify: coverage gaps from original, unused Galaxy candidates

[U2] NEW SOURCE INTAKE (CEO provides or AI searches)
     CEO provides: "Thêm file {{path}}", "Thêm URL {{url}}", "Tìm thêm về {{sub-topic}}"
     AI searches: WebSearch / YouTube for newer sources (time-filtered)
     Dedup: skip if URL/title already in notebook

[U3] ADD + QUALITY GATE (Step 1G applies)
     → Add new sources to EXISTING notebook
     → Verify ingestion → recover failures → CEO confirms

[U4] DELTA ANALYSIS (NLM on combined old + new)
     Query 1: "Considering ALL sources including the newly added ones:
              What NEW insights emerge that were not in the original analysis?
              How do they change or refine the original Three Laws?"
     Query 2: "Do new sources contradict any original findings? Flag conflicts."
     Query 3: "What coverage gaps from the original are now filled?"

[U5] THREE LAWS RE-EVALUATION
     Compare original 3 Laws vs new evidence:
     | Law | Original | Still valid? | Refined version (if changed) |
     CEO decides: keep / refine / replace each Law

[U6] SAVE UPDATE OUTPUT
     File: LEARN_{{topic}}_update_{{today}}.md
     Original file: UNTOUCHED
     Format:
       - Link to original: LEARN_{{topic}}_{{original_date}}.md
       - New sources added: {{list}}
       - Delta insights: {{new findings, contradictions, gaps filled}}
       - Three Laws: updated if needed (CEO approved)
       - New Galaxy candidates: from new insights only

[U7] GALAXY HARVEST (new insights only)
```

### Update Rules
- **NEVER modify the original LEARN_*.md file** — it's a historical record of that learning session
- **NEVER remove sources from existing notebook** — only add new ones
- **Three Laws may evolve** — but CEO must explicitly approve any changes (Core)
- Output filename: `LEARN_{{topic}}_update_{{today}}.md` — clearly marked as update
- Multiple updates accumulate: `_update_2026-04-12.md`, `_update_2026-05-15.md`, etc.
- If no `--notebook` specified → search frontmatter of most recent `LEARN_{{topic}}_*.md` for notebook alias

### Difference: UPDATE vs REFRESH

| Aspect | REFRESH | UPDATE |
|--------|---------|--------|
| New sources | Quick WebSearch only (1-3) | Full source intake + NLM ingestion |
| NLM notebook | Optional query | Required — adds new sources |
| Output | Appends to original file | New separate file `_update_{{date}}` |
| Three Laws | Validity check only | May refine/replace (CEO Core) |
| Depth | Lightweight (30 min) | Deep (1-2 hours, like full mode) |
| When | Monthly check | New book/paper/source available |

---

## WHEN TO USE WHICH MODE

| Situation | Mode | Time | Output |
|-----------|------|------|--------|
| Đọc bài viết hay, muốn extract value | `quick` | 30 min | Three Laws + Galaxy candidates |
| Cần xây skill mới cho dự án | `full` | 2h + cycle | DMIR plan + Galaxy + decision bridge |
| NLM notebook đầy, cần synthesize | `full --notebook X` | 1-2h | Cross-source analysis |
| Cuối tuần, review learning tích lũy | `review` | 30 min | Compound check + dJ/dt |
| Voice transcript từ Tana | `quick` (auto-route) | 20 min | Three Laws + triage |
| Cần tài liệu tự học có bài tập, rubric | `practice` | 1-2h | Practice guide + exercises |
| Có nguồn mới cho topic đã học | `update --notebook X` | 1-2h | Delta analysis + updated Three Laws |
| Kiểm tra Three Laws còn đúng không | `refresh` | 30 min | Validity check + staleness report |
| Onboard kỹ năng mới cho dự án Tier 1 | `practice --project X` | 1-2h | Project-anchored course |
| Kiểm tra analysis cũ còn đúng không | `refresh` | 15-30 min | Staleness report + updates |
| Quarterly audit tất cả past learning | `refresh` (batch) | 30-60 min | Batch validity check |

---

## INTEGRATION WITH EXISTING SKILLS

```
/learning = Super Skill (orchestrator)
    ├── /analyze  → Phase 2 (deep analysis engine) + Practice Phase 2 (knowledge map)
    ├── /cycle    → Phase 4 (DMIR cycle planning)
    ├── /teach    → Phase 6 (decision recording + patterns)
    ├── /reflect  → Phase 7 (weekly reflection)
    ├── /nlm      → Phase 2 Option B (NLM-powered analysis)
    ├── /research → Phase 1 (source gathering if topic, not file)
    ├── /galaxy-note → Phase 5 (note creation after CEO approval)
    ├── Refresh mode → re-validate past analyses (staleness check, Three Laws validity)
    └── Practice mode → standalone self-study document generator
        ├── Scope definition + Dreyfus targeting
        ├── Knowledge map + dependency tree
        ├── Week-by-week lessons + exercises (project-anchored)
        ├── Rubric tự đánh giá (observable behaviors, not subjective)
        ├── Capstone exercise + final assessment
        └── Supporting materials (flashcards, cheat sheet, interleaving schedule)
```

Relationship to /research:
- `/research` = **knowledge acquisition** (find sources → analyze → save)
- `/learning` = **knowledge transformation** (analyze → distill → apply → compound)
- `/research` feeds `/learning` — research output becomes learning input

---

## OUTPUT FILE FORMAT

```yaml
---
created: {{today}}
source: learning-pipeline
topic: "{{topic}}"
mode: full|quick|review|refresh
type: learning-output
status: inbox
tags: [#type/learning-output, #status/inbox]
project: {{project-id or null}}
three_laws:
  - "{{Law 1 name}}"
  - "{{Law 2 name}}"
  - "{{Law 3 name}}"
galaxy_candidates: {{N}}
dmir_cycle: {{Y/N}}
---
```

File path: `3_Resources/Deep-Content-Analyzer-Outputs/LEARN_{{topic_slug}}_{{date}}.md`

---

## NLM MASTERY ARCHETYPES (v2.0)

11 specialized NLM query templates for deep extraction. Use with `--nlm-archetype <name>` on any mode that uses NLM (full, quick, update). Each archetype sets a NLM persona + structured query optimized for a specific learning objective.

**When to use:** After sources are ingested into NLM notebook (Step 1G passed), replace or augment the default Step 2 NLM query with an archetype-specific query. Multiple archetypes can be chained in sequence on the same notebook.

**Recommended learning journey:**
- Week 1-2 (Foundation): `feynman` + `structure` → build mental model
- Week 3-4 (Deep dive): `miner` + `cross-std` → internalize parameters
- Week 5-6 (Critical thinking): `skeptic` + `failures` + `contradict` → develop judgment
- Week 7-8 (Application): `study` + `socratic` → test mastery
- Ongoing: `briefing` + `roadmap` → implementation planning

### 1. FEYNMAN — Explain like I'm a new engineer

```bash
nlm notebook query {{notebook}} "Read all sources and explain the core concepts as if I'm a newly graduated engineer who has never encountered this methodology. For each concept: (1) Explain in plain language avoiding jargon, (2) Use analogies from everyday Vietnamese life (motorbike design, rice cooker, construction), (3) Explain WHY behind each step not just HOW, (4) Give 1 typical junior engineer mistake, (5) Connect to defense product context (UAV, naval gun mount, LOMAH, target drone). End with a concept map showing how all concepts interconnect."
```

**Best for:** First contact with new methodology/domain. Foundation building.

### 2. BRIEFING — Executive summary for technical leadership

```bash
nlm notebook query {{notebook}} "Act as Chief Engineer reporting to CEO of Workshop X. Create a 1-2 page executive briefing: (1) 5 core principles applicable to current projects, (2) 3 methodology risks when skipping systematic approach (jumping to solutions, anchoring bias, inadequate requirements), (3) Strategic recommendations for Vietnam defense enterprise considering current engineer capability and ITAR-free constraints, (4) ROI estimation: how much design error reduction and rework savings, (5) Quick wins deployable in 30/60/90 days. Be concise with specific numbers."
```

**Best for:** Before making strategic decisions. CEO judgment calibration.

### 3. SKEPTIC — Critical review for defense context

```bash
nlm notebook query {{notebook}} "Read with professional skepticism from a Vietnam defense engineer perspective. Analyze: (1) Limitations when applied to products requiring MIL-STD/STANAG compliance, (2) Does it account for reverse engineering from foreign products (common VN context)? (3) How does it handle classified requirements and compartmentalized information? (4) Is it suitable for modern mechatronic/cyber-physical systems or needs VDI 2206 supplement? (5) Identify the 5 biggest weaknesses for QPAN Vietnam application with page references and proposed adaptations."
```

**Best for:** Before adopting a new methodology. Bias detection. Gap analysis.

### 4. MINER — Extract all quantitative data and heuristics

```bash
nlm notebook query {{notebook}} "Extract ALL quantitative data and heuristics from sources into structured tables: TABLE 1 Design Rules & Heuristics (Rule, Phase, Context, Numerical Value, Source); TABLE 2 Evaluation Criteria (Criterion, Weight Range, Scoring Scale, Domain); TABLE 3 Checklist Items (Topic, Phase, Count, Key Questions); TABLE 4 Formulas & Calculations (Name, Equation, Variables, Units, Application); TABLE 5 Design-for-X Guidelines (DfX Category, Guidelines, Quantitative Limits, Trade-offs). Include hidden numbers in text (e.g. '80% of cost locked at conceptual phase'). Format for direct paste into markdown tables."
```

**Best for:** Building reference sheets. Populating design templates. Data-driven analysis.

### 5. STUDY — Mastery-level assessment material

```bash
nlm notebook query {{notebook}} "Create expert-level study materials: PART A (10 hard MCQ): distinguish easily confused concepts, edge cases, when to use which method. PART B (5 case studies): (1) target drone ITAR-free design, (2) reverse engineering fire control system, (3) UAV gimbal for Vietnam sea conditions, (4) naval gun mount 30mm with domestic manufacturing, (5) LOMAH acoustic sensor for range. PART C (5 essay questions): compare approaches, critique a sample deliverable, design for a specific product. Each answer with: detailed explanation, why other options wrong, common pitfalls, source page reference, Bloom's taxonomy level."
```

**Best for:** Self-assessment. Identifying knowledge gaps. Dreyfus level verification.

### 6. ROADMAP — Implementation plan for Workshop X

```bash
nlm notebook query {{notebook}} "Based on sources, create implementation roadmap for Workshop X (~26 people, defense manufacturing): Phase 1 Foundation (0-3 months): training program, template creation (requirements list, function structure, morphological matrix, VDI 2225 scorecard, DfX checklists), pilot selection criteria. Phase 2 Pilot (3-9 months): 2-3 pilot projects (1 mechanical, 1 mechatronic, 1 reverse engineering), KPIs (design iterations, defect rate, time-to-prototype), mentorship. Phase 3 Scale (9-18 months): PLM/CAD integration, cross-functional involvement. Phase 4 Excellence (18+ months): internal certification, continuous improvement. Per phase: responsible roles, deliverables, dependencies, risks (resistance to change, quick-fix culture), budget estimate, success metrics."
```

**Best for:** Converting learning into organizational action. Implementation planning.

### 7. STRUCTURE — Navigation map for dense material

```bash
nlm notebook query {{notebook}} "Analyze the structure of this content: Level 1 — one-line summary per major section/chapter. Level 2 — key concepts hierarchy: which are foundational (must read first), which are advanced (skip first read), which are reference (lookup when needed). Level 3 — topic-based navigation: for each Workshop X focus area (requirements engineering, function structure, concept evaluation VDI 2225, embodiment principles, DfM for Vietnam capability, reverse engineering, mechatronic VDI 2206), list the most important pages/sections. Level 4 — reading paths: fast track (40h), comprehensive (120h), specialist (deep in 1 phase). Create ASCII dependency diagram between sections."
```

**Best for:** Orientation in large textbooks/standards. Learning path optimization.

### 8. CROSS-STD — Cross-standard synthesis

```bash
nlm notebook query {{notebook}} "Synthesize content with related standards for defense engineers. Create mapping matrix: P&B Phase | VDI 2221 Step | VDI 2206 V-model Stage | Relevant MIL-STD | STANAG | Vietnam TCVN/TCQS. Identify key intersections: Requirements↔MIL-STD-961, Function Structure↔SysML, VDI 2225↔DoD Architecture Framework, Embodiment↔MIL-HDBK-5/17, Detail Design↔ASME Y14.5/ISO 1101, Design Review↔MIL-STD-1521. Flag gaps for Vietnam: standards VN lacks, standards needing localization, handling customer spec vs commercial best practice. Conclude with recommended integrated framework for Workshop X."
```

**Best for:** Standards integration. Compliance mapping. Building unified process.

### 9. FAILURES — Design failure mode analysis from methodology

```bash
nlm notebook query {{notebook}} "Extract and analyze design failure modes per phase: Task Clarification failures (requirements creep, missing stakeholders, untestable/conflicting requirements), Conceptual Design failures (anchoring to first solution, incomplete function structure, biased VDI 2225, insufficient alternatives), Embodiment failures (over-engineering, premature optimization, skipping DfX, tolerance stack-up), Detail Design failures (drawing errors, BOM inconsistency, missing manufacturing notes). Per failure: symptom, root cause (5-Why/Ishikawa), prevention, detection stage, recovery at minimal cost, defense product example. Rank top 10 by RPN (Severity x Occurrence x Detection) for Vietnam defense manufacturing context."
```

**Best for:** Developing engineering judgment. Failure prevention. Quality gate design.

### 10. SOCRATIC — Self-assessment through questioning

```bash
nlm notebook query {{notebook}} "Act as Socratic coach. Instead of explaining, generate questions that force deep thinking: Level 1 Comprehension — ask me to define core concepts in my own words, distinguish easily confused terms. Level 2 Application — give specific defense engineering scenarios, ask how to apply. Level 3 Critical — ask when methodology FAILS, what are trade-offs of deviation. Level 4 Synthesis — ask to connect concepts across sections, design hybrid approaches for uncovered situations. Level 5 Teaching (Feynman) — ask me to explain to a junior engineer, then evaluate my explanation gaps. Provide competency assessment across 4 VDI 2221 phases (Clarify/Conceptualize/Embody/Detail) with 1-5 scale and next-step recommendations."
```

**Best for:** Deep mastery verification. Identifying hidden gaps. Dreyfus progression.

### 11. CONTRADICT — Contradiction finder + assumption killer + intellectual lineage

```bash
nlm notebook query {{notebook}} "Perform 3 critical analyses across all sources:

PART A — CONTRADICTION MAP:
Identify every point where two or more sources directly contradict each other.
For each contradiction:
| Sources | Position A | Position B | Why They Disagree | Severity |
Severity: CRITICAL (changes what I should learn/apply) / MODERATE (affects confidence) / MINOR (definitional)
Explain WHY they disagree: methodology? dataset? era? assumptions? context?

PART B — ASSUMPTION KILLER:
List every assumption the MAJORITY of sources share but never explicitly test.
For each:
| Assumption | Sources Relying On It | What Breaks If Wrong | VN Defense Relevance |
Focus on assumptions about: operating environment, manufacturing capability,
material availability, user skill level, maintenance infrastructure.

PART C — CITATION CHAIN (intellectual lineage):
Pick the 3 most-cited concepts across these sources. For each:
- Who introduced it first?
- Who challenged it?
- Who refined it?
- What is the current consensus (if any)?
Show the intellectual lineage as a timeline.

Conclude with: Which contradictions and assumptions should the CEO investigate
BEFORE applying this knowledge to defense product design?"
```

**Best for:** Before trusting a body of knowledge. Catching shared blind spots. Understanding field maturity. Use AFTER `feynman` or `structure` (need foundation first to appreciate contradictions).

### Archetype Chaining

For maximum learning depth, chain archetypes in sequence:

```
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype structure
# → Understand content structure first
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype feynman
# → Build intuitive understanding
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype miner
# → Extract quantitative data
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype skeptic
# → Challenge assumptions
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype contradict
# → Find contradictions + shared blind spots
/learning "P&B Systematic Design" --notebook pb-textbook --nlm-archetype socratic
# → Test mastery
```

Each run produces a separate `LEARN_*` file. The `review` mode then synthesizes across all runs.

### NLM Knowledge Base Setup (auto-generate reports + quiz + persona)

When a learning notebook is created (or an archetype is used for the first time), auto-generate a persistent knowledge base of reports in NLM. CEO can return to the notebook later and chat with full context.

**Trigger:** First time `--nlm-archetype` is used on a notebook, OR when CEO runs `/learning <topic> --mode full --notebook <alias>` with new notebook.

**Step LKB-1: Set Chat Persona** (auto-configured via MCP)

Use `mcp__notebooklm-mcp__chat_configure` to set persona automatically — no manual paste needed.

```
chat_configure(
  notebook_id={{uuid}},
  goal="custom",
  response_length="longer",
  custom_prompt="PERSONA — ENGINEERING MASTERY COACH FOR WORKSHOP X

You are a Pahl-Beitz systematic design coach for a Vietnam defense CEO learning engineering methodology. Workshop X has shipped 1,064+ hardware units across 8 product lines. Your role:
- Explain concepts using Vietnamese analogies (xe may, noi com dien, cong trinh)
- Always connect theory to defense products (UAV, naval gun mount, LOMAH sensor, target drone, USV, naval simulator)
- Flag WHY behind each step, not just HOW
- Point out common junior engineer mistakes
- When testing knowledge, use Socratic questioning before giving answers
- Cite specific sources from uploaded documents with page references
- Assess learner at Dreyfus levels (Novice→Advanced Beginner→Competent→Proficient→Expert)
- Use metric units exclusively
- Respond in Vietnamese when asked, English for technical terms
- Always consider Vietnam manufacturing context (tropical, domestic sourcing, ITAR-free)"
)
```

**Step LKB-2: Generate Archetype Reports** (batch — CEO approves first)

```
CEO gate: "Tao bo reports learning trong NLM? Chon archetypes nao?"
Options: ALL (10 reports) / FOUNDATION (feynman+structure+miner) / MASTERY (skeptic+failures+socratic) / CUSTOM (CEO picks)
```

Run selected archetype queries (from NLM MASTERY ARCHETYPES section above) and save each as NLM note.

**Step LKB-3: Generate Quiz & Study Materials** (NLM conversation queries)

```bash
# Mastery quiz (auto-generated from all sources)
nlm notebook query learn-{{short}} "Create expert-level assessment: PART A (10 hard MCQ): distinguish easily confused concepts, edge cases in methodology, when to use which approach. PART B (5 case studies): each a real Vietnam defense scenario requiring methodology application. PART C (3 essay questions): compare approaches, critique a sample deliverable, design for specific product. Each answer: detailed explanation, why others wrong, common pitfalls, source reference, Bloom's taxonomy level (target: Analyze/Evaluate/Create)."

# Spaced repetition flashcards
nlm notebook query learn-{{short}} "Create 30 flashcard pairs covering core concepts: (10) definitions and distinctions, (10) application rules and heuristics with numerical values, (10) failure modes and warnings. Format: | # | Question | Answer | Difficulty (Easy/Medium/Hard) |"
```

**Step LKB-4: Generate Studio Artifacts** (persistent learning materials in NLM UI)

After NLM conversation queries (LKB-2 + LKB-3) are complete, generate persistent Studio artifacts. These are accessible via NLM notebook UI even after conversation context expires — CEO's long-term learning library.

**CEO gate:** "Tạo bộ Studio artifacts (quiz, flashcards, reports, audio) trong NLM? ~5 phút."
**Trigger:** Auto-suggest after LKB-3 completes. CEO can skip if only needs conversation reports.

Use `mcp__notebooklm-mcp__studio_create` MCP tool for ALL artifacts. Do NOT use `nlm audio create` CLI (not supported).

**CRITICAL — Prompt Quality Rule:**
- NEVER use generic focus_prompts → NLM auto-generates shallow, generic content
- Every artifact MUST include WX-specific context: product names, VN defense, learning level, active project
- Quiz: VN defense scenarios + Bloom's taxonomy + Dreyfus level assessment
- Flashcards: Easy/Medium/Hard tiers + key formulas + heuristics + failure modes
- Reports: ordered learning path structure with WX product application
- Audio: focus on core principles, common mistakes, and WX-specific application

**6 artifacts to generate (parallel where possible):**

```
# Artifact 1: Quiz (hard, WX application scenarios)
studio_create(notebook_id={{uuid}}, artifact_type="quiz", question_count=10, difficulty="hard",
  focus_prompt="PART A (10 MCQ): test {{topic}} mastery for Vietnam defense CEO at
  {{level}} level. Include: (1) easily confused concepts in this domain, (2) edge cases
  where methodology breaks down, (3) Vietnam defense application scenarios using WX products
  ({{list relevant products}}). Each answer: why correct, why others wrong, source reference,
  Bloom's taxonomy level (target Analyze/Evaluate/Create).
  PART B (5 case studies): real Workshop X engineering situations requiring {{topic}}
  application. Include specific product contexts and design decisions.",
  confirm=True)

# Artifact 2: Flashcards (Easy/Medium/Hard)
studio_create(notebook_id={{uuid}}, artifact_type="flashcards", difficulty="medium",
  focus_prompt="20 flashcard pairs for {{topic}} organized by difficulty:
  EASY (7): core definitions, key distinctions, fundamental principles.
  MEDIUM (7): application rules, heuristics with numerical values, method selection criteria.
  HARD (6): failure modes and warnings, edge cases, VN-specific adaptations,
  contradictions between sources.
  Focus on knowledge directly applicable to Workshop X engineering decisions.",
  confirm=True)

# Artifact 3: Briefing Doc (learning summary for CEO)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Briefing Doc",
  focus_prompt="WORKSHOP X CEO LEARNING BRIEFING — {{topic}}
  Structure: (1) CORE PRINCIPLES: 3-5 irreducible laws/rules (Three Laws extraction).
  (2) COMMON FAILURE MODES: what goes wrong when applying this methodology.
  (3) WX APPLICATION: how each principle applies to active WX projects ({{products}}).
  (4) DECISION FRAMEWORK: when to use what approach (decision tree).
  (5) DREYFUS ASSESSMENT: current CEO level + specific actions to advance.
  (6) PRACTICE PLAN: what to do this week to compound learning.
  Cite specific sources. Connect to existing Galaxy notes where relevant.",
  confirm=True)

# Artifact 4: Study Guide (ordered mastery path)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Study Guide",
  focus_prompt="WORKSHOP X MASTERY STUDY GUIDE — {{topic}}
  Structure as ordered learning path with dependencies:
  Step 1 FOUNDATION: core concepts, vocabulary, mental models (must master first).
  Step 2 PRINCIPLES: key rules, heuristics, formulas with numerical values.
  Step 3 METHOD: step-by-step application process with checkpoints.
  Step 4 FAILURE MODES: what breaks, why, how to detect early.
  Step 5 APPLICATION: map to WX products and active projects.
  Step 6 MASTERY: advanced topics, edge cases, cross-domain connections.
  For each step: estimated time, key sources, exercises, self-assessment criteria.",
  confirm=True)

# Artifact 5: Audio Deep Dive (commute learning)
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="deep_dive",
  language="vi",
  focus_prompt="Focus on mastering {{topic}} for a Vietnam defense CEO. Cover:
  {{top 3-5 core principles}}, common mistakes engineers make, how this applies
  to Workshop X products ({{list products}}), and what to practice this week.",
  confirm=True)

# Artifact 6: Audio Critique (judgment development)
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="critique",
  language="vi",
  focus_prompt="Critically evaluate {{topic}}: Where does the methodology break down?
  What assumptions are untested? What contradictions exist between sources?
  What would a skeptic say? How does Vietnam's manufacturing context challenge
  standard Western approaches? What are the hidden failure modes?",
  confirm=True)
```

**Verify all 6 complete:**
```
studio_status(notebook_id={{uuid}})
```

**Step LKB-5: Save KB Index**

Save to: `2_Areas/CEO-Self/Learning-Architecture/NLM_KB_LEARN_{{topic}}_{{date}}.md`

```markdown
# NLM Knowledge Base — Learning: {{topic}}
Notebook: learn-{{short}}
Created: {{today}}
Archetypes generated: {{list}}

## Studio Artifacts (persistent in NLM UI)
| # | Title | Type | Status |
|---|-------|------|:------:|
| 1 | {{title}} | Quiz (MCQ + Case Studies) | ✅/⏳ |
| 2 | {{title}} | Flashcards (Easy/Med/Hard) | ✅/⏳ |
| 3 | {{title}} | Briefing Doc (CEO summary) | ✅/⏳ |
| 4 | {{title}} | Study Guide (mastery path) | ✅/⏳ |
| 5 | {{title}} | Audio Deep Dive | ✅/⏳ |
| 6 | {{title}} | Audio Critique | ✅/⏳ |

## Chat Persona
Persona pasted: YES/NO

## How to Use in NLM Chat
- "Giai thich concept X nhu cho nguoi moi" (Feynman mode)
- "Diem yeu nao khi ap dung cho defense VN?" (Skeptic mode)
- "Cho toi 3 bai tap ve topic Y" (Study mode)
- "Hoi toi cau hoi de kiem tra hieu biet" (Socratic mode)
NLM will use sources + generated reports for deep, contextual answers.
```

### Archetype + Mode Integration

| Mode | Archetype Usage |
|------|----------------|
| `full` | Archetype replaces default NLM query in Step 2 |
| `quick` | Archetype replaces default inline analysis |
| `update` | Archetype applied to delta analysis (U4) |
| `practice` | `study` archetype auto-invoked for Phase 2 knowledge map |
| `review` | N/A (no new NLM queries) |
| `refresh` | `skeptic` archetype can augment staleness check |

---

## RULES

- Three Laws extraction is NON-NEGOTIABLE — every /learning run must produce exactly 3 laws
- Galaxy candidates are PROPOSED, not created — CEO decides (Core per COD)
- DMIR cycle must anchor to an active project — learning without application = Analyst Trap
- Review mode: check "used in decision?" column — learning that never changes decisions is waste
- NLM for volume (>5000 words, multiple sources), Claude for depth (frameworks, debate)
- **Source Quality Gate (Step 1G):** When using NLM path (Option B/C), ALWAYS verify source ingestion after adding. Try 3 recovery methods for failed sources (alt URL, WebFetch→text, YouTube). Present ingestion report to CEO. NEVER run NLM queries until CEO confirms "đủ nguồn". CEO can add sources manually via NLM web UI or provide local PDF. Skip gate for Option A (single source, Claude inline).
- All Vietnamese text MUST have dấu — no exceptions
- Decision Bridge (Step 6) is what makes this different from just reading — connect learning to ACTION
- dJ/dt tracking: every /learning run should increase judgment, not just knowledge
- If 3 consecutive learning sessions produce no Galaxy notes → something is wrong with source quality or extraction
- COD: Pipeline orchestration = O, Source selection = C, Three Laws validation = C, Galaxy promotion = C, Decision = C
- Link to Galaxy: Phán đoán không thể uỷ thác cho AI, dJ/dt > dD/dt, Analyst Trap, Vault = Graveyard, Training Scars

### Practice Mode Rules (additional)
- Mỗi bài tập PHẢI gắn vào dự án thật — bài tập "toy" vi phạm Training Scars principle
- Rubric dùng observable behaviors, KHÔNG dùng subjective (tốt/chưa tốt) — phải binary check
- Scoring < 2 trung bình → lặp lại tuần đó, KHÔNG skip — mastery before moving on
- Mỗi tuần có Galaxy Candidate Check — practice tạo insight tốt hơn passive reading
- Capstone exercise là proof of skill — nếu không hoàn thành được, khóa học chưa xong
- Document lưu tại `2_Areas/CEO-Self/Learning-Architecture/` — không phải 0_Inbox
- Practice mode có thể chạy độc lập HOẶC sau full/quick mode (dùng Three Laws từ analysis trước)
- Supporting materials (flashcards, cheat sheet) chỉ tạo khi CEO yêu cầu — tránh over-engineering
- Dependency tree quyết định thứ tự tuần — KHÔNG dạy concept phụ thuộc trước concept nền tảng
- Interleaving: sau 2 tuần cùng topic, xen 1 tuần review hoặc topic khác để chống forgetting curve
