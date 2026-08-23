---
name: codebase-to-book
description: "Orchestrator biến codebase bất kỳ thành sách kỹ thuật publication-quality (tương đương O'Reilly). Multi-agent pipeline commanding 9 block-skills (explore → position → outline → write → review → revise → audit → notebook → ceo-insight). Phase 1 và 4 fan-out parallel Task subagents. Phase 8 tạo NotebookLM + ingest full book. Phase 9 query NLM với 5 insight lenses (HELIX/FORGE/Galaxy/ACH/IP) để sinh CEO insights cho Workshop X. Flags: --deep (chain /research per chapter), --quick, --no-nlm, --from/--only, --audience, --parts, --lang, --insight-lens. Triggers on: 'codebase to book', 'phân tích codebase thành sách', 'technical book from code', 'book from source', 'xây sách kỹ thuật', 'ctb'."
---

# Codebase-to-Book — Mega-Skill Orchestrator (9-Phase Multi-Agent Pipeline)

> **Role:** Chỉ huy trưởng (Commander) — điều phối 9 block-skills tuần tự, CEO checkpoint sau mỗi block
> **Architecture:** Modular pipeline — mỗi block = 1 skill độc lập, có thể chạy standalone
> **Source:** Prompt gốc "Turn Any Codebase Into a Technical Book" (see `references/source-prompt.md`)
> **Case study:** "Claude Code from Source" — 36 agents × 7 phases × 6 giờ → 18 chương / 6,271 dòng / ~400 trang
> **Extension cho Workshop X:** Thêm P8 (NotebookLM build) + P9 (CEO insight lenses) — biến sách thành tài sản chiến lược, không chỉ deliverable

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                        codebase-to-book (ORCHESTRATOR — 9 blocks)                       │
│                                                                                          │
│  Flags: --deep | --quick | --no-nlm | --from X | --only X                               │
│         --audience leader|engineer|both | --parts N | --lang vi|en | --insight-lens     │
│                                                                                          │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ P1  │▶│ P2  │▶│ P3  │▶│ P4  │▶│ P5  │▶│ P6  │▶│ P7  │▶│ P8  │▶│ P9  │              │
│  │EXPL │ │POSI │ │OUT- │ │WRITE│ │REVI │ │REVI │ │AUD- │ │NOTE-│ │CEO- │              │
│  │ORE  │ │TION │ │LINE │ │     │ │EW   │ │SE   │ │IT   │ │BOOK │ │INSI │              │
│  │∥    │ │C    │ │C    │ │∥    │ │∥    │ │     │ │C    │ │NLM  │ │GHT  │              │
│  │N×   │ │     │ │     │ │N×   │ │2-3× │ │     │ │     │ │MCP  │ │C    │              │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘              │
│     │CEO    │CORE   │CORE   │CEO    │CEO    │CEO    │CORE   │CEO    │CORE             │
└─────────────────────────────────────────────────────────────────────────────────────────┘

Legend: ∥ = parallel Task subagents | C = CEO Core (non-delegable) | CEO = checkpoint after

Data Bus: 3_Resources/Books/<codebase-slug>/   (trong vault Workshop_X)
          hoặc <path>/book-output/              (nếu codebase ngoài vault)
State:    <output_dir>/_pipeline_state.md
```

## Sub-Skills (9 Block-Skills)

| Block | Skill Name | Parallel? | Purpose | CEO Checkpoint |
|-------|-----------|-----------|---------|----------------|
| **P1** | `/book-explore` | **YES** (N agents) | Read codebase exhaustively per subsystem, produce raw research notes | Review coverage + gaps |
| **P2** | `/book-position` | NO | Define audience (dual-reader), thesis, "why a book" | **CEO Core — approve thesis** |
| **P3** | `/book-outline` | NO | 5-7 parts + 15-20 chapters with ordering rationale | **CEO Core — approve TOC** |
| **P4** | `/book-write` | **YES** (N agents) | Write each chapter from scratch using P1 notes | Review draft quality |
| **P5** | `/book-review` | **YES** (2-3 agents) | Editorial review — flow, cuts, missing content, consistency | Review feedback severity |
| **P6** | `/book-revise` | NO | Apply feedback in one pass — split/merge, cut, add | Approve revised chapters |
| **P7** | `/book-audit` | NO | Source code audit — verbatim → pseudocode, IP check | **CEO Core — IP sign-off** |
| **P8** | `/book-notebook` | NO (but MCP parallel ingest) | Create NotebookLM notebook, chunk book by chapter, ingest all sources | Verify NLM URL + test query |
| **P9** | `/book-ceo-insight` | NO | Query NLM với 5 insight lenses (HELIX/FORGE/Galaxy/ACH/IP) | **CEO Core — select actionable** |

## How to Use

### Full Pipeline (default — Vietnamese output, dual audience, NLM build + insights)
```
/codebase-to-book <path>
```

### With deep research (slower, higher quality, uses /research --deep per subsystem + per chapter)
```
/codebase-to-book <path> --deep
```

### Quick mode (skip P5/P6 — review + revise)
```
/codebase-to-book <path> --quick
```

### Book only, no NLM (skip P8/P9)
```
/codebase-to-book <path> --no-nlm
```

### Resume / Single Block
```
/codebase-to-book <path> --from P4
/book-write <codebase-slug>
```

### English output, engineer-only audience
```
/codebase-to-book <path> --lang en --audience engineer
```

### Custom insight lenses
```
/codebase-to-book <path> --insight-lens helix,galaxy
```

## Orchestrator Workflow

### Step 1: Parse Arguments

```
PATH: {{first argument — codebase path, absolute or relative}}

FLAGS:
  --deep                  → P1 và P4 invoke /research --deep per subsystem/chapter
  --quick                 → Skip P5/P6 (review + revise)
  --no-nlm                → Skip P8/P9 (NotebookLM + insights)
  --from X                → Resume từ block X (P1-P9)
  --only X                → Run single block X only
  --audience leader|engineer|both  → default 'both' (dual-reader)
  --parts N               → Target parts count (default 5-7)
  --lang vi|en            → Output language (default 'vi')
  --insight-lens helix,forge,galaxy,ach,ip  → P9 lens override (default all 5)
```

### Step 1.5: Resolve Output Directory

```
Codebase slug = basename(path) lowercase + kebab-case
  e.g., /d:/KN-Stack → "kn-stack"
  e.g., /e:/Workshop_X/1_Projects/VN-XUONG-UUV → "vn-xuong-uuv"

If path is within D:\Workshop_X vault:
  Output = D:\Workshop_X\3_Resources\Books\<slug>\
Else if path has parent with .git:
  Output = <path>/book-output/<slug>/
Else:
  Output = <cwd>/book-output/<slug>/
```

### Step 1.6: Input Validation & CEO Context Enrichment

**MANDATORY before any block execution.**

#### 1.6a: Verify Codebase Accessible

```
CODEBASE CHECK — {{path}}
  □ Path exists?
  □ Is a directory? (skill không phân tích single file)
  □ Contains source files? (scan *.py, *.ts, *.rs, *.go, *.c, *.cpp, *.md, etc.)
  □ Size estimate (file count, LOC) — warn if >100k files hoặc <50 files
  □ Git repo? (optional — affects metadata gathering)

RESULT: [GO / NO-GO — what's missing?]
```

#### 1.6b: NLM Auth Pre-Check (if --no-nlm not set)

```
NLM AUTH — Verifying notebooklm-mcp session...
  → Call mcp__notebooklm-mcp__refresh_auth
  → If fail: HALT with instruction
     "Run `nlm login` trong terminal của anh, rồi /codebase-to-book ... --from P1"
  → If ok: proceed
```

#### 1.6c: Present Scope to CEO

```
═══ CODEBASE-TO-BOOK — SCOPE PREVIEW ═══

Codebase: {{path}}
Output: {{output_dir}}
Slug: {{slug}}

Files: {{N}} source files, ~{{M}} LOC (rough estimate)
Main languages: {{lang1 ({{pct1}}%), lang2 ({{pct2}}%), ...}}

Pipeline: {{mode}} ({{9 phases | 7 phases --quick | 7 phases --no-nlm}})
Audience: {{leader | engineer | both}}
Language: {{vi | en}}
Deep research: {{YES | NO}}

Estimated deliverables:
  - {{N}} exploration reports (P1)
  - 1 positioning doc (P2)
  - 1 outline with ~15-18 chapters (P3)
  - {{N}} chapter drafts (P4)
  - 1 compiled book.md (P7)
  - 1 NotebookLM notebook (P8) — if NLM mode
  - 1 CEO insights doc (P9) — if NLM mode

Estimated cost: {{rough estimate based on chapter count × deep flag}}
Estimated time: {{hours}} with CEO checkpoints

CEO:
(1) ▶️ Confirm và chạy P1
(2) ⚙️ Adjust flags (specify what)
(3) ⏸️ Cancel
═══════════════════════════════════════════════════
```

Wait for CEO response before proceeding.

### Step 2: Initialize Pipeline State

Create/update `{{output_dir}}/_pipeline_state.md`:

```markdown
---
codebase_path: {{path}}
codebase_slug: {{slug}}
pipeline: codebase-to-book v1.0
started: {{today}}
updated: {{today}}
mode: {{standard | quick | no-nlm}}
flags:
  deep: {{true|false}}
  audience: {{leader|engineer|both}}
  lang: {{vi|en}}
  parts: {{N}}
  insight_lens: [{{list}}]
---

# Book Pipeline State — {{slug}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|-------------|
| P1 | book-explore | PENDING | - | - | - |
| P2 | book-position | PENDING | - | - | - |
| P3 | book-outline | PENDING | - | - | - |
| P4 | book-write | PENDING | - | - | - |
| P5 | book-review | PENDING | - | - | - |
| P6 | book-revise | PENDING | - | - | - |
| P7 | book-audit | PENDING | - | - | - |
| P8 | book-notebook | PENDING | - | - | - |
| P9 | book-ceo-insight | PENDING | - | - | - |

## Block Ledger
> **Purpose:** Sole communication channel between blocks. Each block reads this section for context, then appends its summary. Enables crash recovery and context-free resume.

[Each block appends one entry below when complete — see Ledger Write Protocol]

## CEO Decisions
[populated at each checkpoint]

## Adjustments Log
[populated when CEO modifies outputs]
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ CRITICAL RULE: Execute EXACTLY ONE block per turn. After completing a block, STOP and WAIT for CEO response. DO NOT proceed to the next block until CEO explicitly approves. This is the #1 rule.**

**Architecture: Initializer + Incremental + Ledger** (copied từ helix-task-clarify)
- P1 (Exploration) = **Initializer** — populates ledger với codebase subsystem map + raw notes
- P2-P9 = **Incremental Agents** — mỗi block đọc ledger, làm việc, ghi lại
- `_pipeline_state.md` = **State Ledger** — SOLE communication channel giữa blocks

#### Ledger Read Protocol (BEFORE each block)

Read `_pipeline_state.md` → "Block Ledger" section. Reconstruct context từ previous block summaries, CEO decisions, open questions. Critical cho `--from` resume và new sessions.

#### Ledger Write Protocol (AFTER each block)

Append to "Block Ledger" section:
```
### {{Block ID}} — {{block name}} ({{date}})
**Key findings:** [2-3 bullet points — essential outputs]
**Decisions for downstream:** [what next block needs to know]
**Open questions:** [unresolved items for CEO or next block]
**CEO checkpoint result:** [approve / revise / pause + CEO's words]
```

#### For each block:

1. **Ledger Read:** Read `_pipeline_state.md` để reconstruct context
2. **Announce:** "Đang chạy Block {{X}}: {{name}}..."
3. **Execute block:** Invoke `/book-{{phase}}` hoặc run inline logic
4. **Ledger Write:** Append block summary
5. **Update state:** Mark block COMPLETE trong progress table
6. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK P{{X}} COMPLETE ═══
   Deliverables: [files created]
   Key findings: [1-3 bullets]
   
   CEO:
   (1) ✅ Approve → tiếp tục Block P{{X+1}}
   (2) 🔄 Chạy lại Block P{{X}} với điều chỉnh: [mô tả]
   (3) ⏸️ Dừng pipeline
   (4) ⏭️ Skip Block P{{X+1}}
   ```
7. **⛔ WAIT for CEO message.** Không generate content tiếp cho đến khi CEO phản hồi.
8. **On CEO response:**
   - (1) → Execute next block (ONE block only, then STOP)
   - (2) → Re-run current block với adjustments, then STOP
   - (3) → Save state và halt
   - (4) → Skip next block, STOP và present block sau đó

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
CODEBASE-TO-BOOK PIPELINE COMPLETE — {{slug}}
═══════════════════════════════════════════════════
Book: {{output_dir}}/book.md ({{line_count}} lines / ~{{page_estimate}} pages)
Chapters: {{N}} across {{M}} parts
Diagrams: {{N}} Mermaid
Audit: {{N}} verbatim matches replaced với pseudocode

NotebookLM: {{nlm_url}} ({{source_count}} sources ingested)
CEO Insights: {{output_dir}}/Phase9-CEO-Insights.md
  - HELIX applicability: {{N}} insights
  - FORGE transfers: {{N}} insights
  - Galaxy candidates: {{N}} proposed notes
  - ACH transfers: {{N}} opportunities
  - IP exposure: {{N}} SAFE / {{N}} REVIEW / {{N}} SENSITIVE

Suggested follow-up:
  - /research-to-skill <skill> → apply HELIX/FORGE insights
  - /galaxy-note → create proposed atomic notes
  - /convert_md_to_docx book.md → publish-ready DOCX
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files trong `{{output_dir}}/`:

> ⛔ **Bảng này được THI HÀNH bằng `scripts/databus_check.py`, không phải bằng thiện chí.**
> Chạy nó trước mỗi checkpoint; mã thoát != 0 thì cấm trình checkpoint. Hiện vật nhỏ hơn 400 byte bị
> tính là **không có** — chặn kiểu "tạo file cho có".

| File / Folder | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_pipeline_state.md` | Orchestrator | All blocks | Progress, ledger, CEO decisions |
| `Phase1-Exploration/{{subsystem}}_Exploration.md` | P1 (N subagents) | P2, P3, P4 | Raw research notes per subsystem |
| `Phase1-Exploration/P1_Synthesis.md` | P1 (orchestrator merge) | P2, P3 | Consolidated findings + coverage map |
| `Phase2-Positioning.md` | P2 | P3, P4, P5 | Audience, thesis, "why a book", glossary |
| `Phase3-Outline.md` | P3 | P4, P5, P7 | Parts + chapters + chapter specs (2-3 bullets each) |
| `Phase4-Chapters/Ch{{NN}}_{{slug}}_Draft.md` | P4 (N subagents) | P5, P6 | Chapter drafts |
| `Phase5-Reviews/Review_Ch{{N}}-{{M}}.md` | P5 (2-3 subagents) | Orchestrator | Per-review-agent feedback |
| `Phase5-Review.md` | P5 (orchestrator merge) | P6 | Consolidated, prioritized feedback |
| `Phase6-Revised/Ch{{NN}}_{{slug}}_v2.md` | P6 | P7 | Revised chapters |
| `Phase6-Revise.md` | P6 (nếu sửa TẠI CHỖ) | P7, CEO | **Bắt buộc khi không sinh `Phase6-Revised/`** — danh sách thay đổi đo bằng máy + phạm vi đối chiếu được đến đâu |
| `Phase7-Audit-Log.md` | P7 | P8 | Verbatim matches replaced + IP ratings + research sources |
| `Phase7-<DoiNgoai>/` | P7 (nếu sách có nhãn `[NỘI BỘ]`) | P8 | Bản đối ngoại **sinh bằng máy**, kèm phép đếm rò rỉ = 0 |
| `book.md` | P7 (compile) | P8 | Final compiled book — CEO signed |
| `Phase8-Notebook-Manifest.md` | P8 | P9, CEO | NLM notebook ID + URL + source list. **Phải ghi rõ tải bản NÀO** (đối ngoại, không bao giờ bản nội bộ) + kết quả tiền kiểm rò rỉ |
| `Phase9-CEO-Insights.md` | P9 | CEO | 5-lens insights + action items |

## `--deep` Integration with `/research`

Khi `--deep` flag active:

### P1 enrichment
Mỗi subsystem exploration subagent, sau base analysis, invoke:
```
/research --deep "<subsystem name> — architecture and design patterns in <codebase type>"
```
Kết quả feed vào `<subsystem>_Exploration.md` section `## Deep Research Findings` (NLM notebook URL, source tiers, Critical Lens findings).

### P4 enrichment
Mỗi chapter writing subagent, sau reading P1 notes, invoke:
```
/research --deep "<chapter topic> — design rationale and patterns"
```
Citations + source tiers đính kèm cuối chapter dưới section `## Sources`.

### Source tracking
`Phase7-Audit-Log.md` bổ sung section `## Research Sources` liệt kê tất cả NLM notebooks + tier classification để P8 có context.

## P8 NotebookLM Integration

Block `book-notebook` dùng notebooklm-mcp tools:

| Step | Tool | Purpose |
|------|------|---------|
| 8.1 | `mcp__notebooklm-mcp__refresh_auth` | Pre-check session valid |
| 8.2 | `mcp__notebooklm-mcp__notebook_create` | Create notebook "Book: {{slug}} — {{thesis}}" |
| 8.3 | Bash chunk `book.md` by chapter | Split on `^## Chapter` or `^# Chapter` |
| 8.4 | `mcp__notebooklm-mcp__source_add(source_type=text)` ×N parallel | Upload each chapter as source |
| 8.5 | `mcp__notebooklm-mcp__source_add` for meta files | Upload Phase3-Outline.md + Phase7-Audit-Log.md |
| 8.6 | `mcp__notebooklm-mcp__notebook_describe` | Verify ingest — log count |

**Rationale chunk theo chapter:** NLM performs tốt hơn với sources ≤50KB. Sách 400 trang tổng thể vượt limit — chunk cho phép retrieve precision khi query.

Output: `Phase8-Notebook-Manifest.md` với notebook_id + URL + source table.

## P9 CEO Insight Lenses

Block `book-ceo-insight` query NLM với 5 lenses mặc định (override bằng `--insight-lens`):

| Lens | Output Section | Purpose |
|------|---------------|---------|
| `helix` | `## HELIX Applicability` | Patterns applicable to Pahl-Beitz HELIX pipeline (Phase 0-4) |
| `forge` | `## FORGE Transfers` | Product strategy frameworks → FORGE skills upgrade |
| `galaxy` | `## Galaxy Candidates` | 5-10 atomic concepts → proposed permanent notes |
| `ach` | `## ACH Transfer Opportunities` | AI-Compensates-Hardware patterns → BB-01, V-SMASH, etc. |
| `ip` | `## IP Exposure Map` | Per-chapter SAFE/REVIEW/SENSITIVE rating |

**Optional NLM studio artifacts** (CEO choose trong checkpoint):
- `studio_create(artifact_type="briefing_doc")` → executive summary (Situation-Complication-Resolution)
- `studio_create(artifact_type="audio")` → audio deep-dive tiếng Việt
- `studio_create(artifact_type="mind_map")` → visual insights map

Xem `references/phase-prompts.md` cho exact query templates.

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After completing each block, STOP và WAIT cho CEO response. NEVER execute 2+ blocks trong 1 turn. NEVER combine blocks without CEO explicitly requesting. #1 rule.
- **CEO checkpoint sau EVERY block** — không auto-continue without explicit CEO approval ("tiếp tục", "approve", "ok", v.v.)
- **Orchestrator NEVER does block work itself** — always delegate sang sub-skill
- **Pipeline state file is source of truth** — always read before any action
- **Each block-skill is independently runnable** — CEO có thể `/book-write <slug>` alone
- **Data bus contract is sacred** — block outputs dùng exact filenames trong Data Bus table
- **⛔ CỔNG DATA BUS — không có hiện vật thì KHÔNG được báo xong.** Trước mỗi CEO checkpoint, chạy:
  ```bash
  python skills/book/codebase-to-book/scripts/databus_check.py <output_dir> --phase P5
  ```
  **Mã thoát != 0 ⇒ CẤM trình checkpoint.** Làm ra hiện vật trước.
  Áp cho **mọi** pha, và đặc biệt cho **P5 · P6 · P8** — ba pha dễ bị làm "tại chỗ" rồi báo xong.

  > 🔴 **Vì sao có luật này.** Bảng Data Bus đã đặc tả `Phase5-Review.md`, `Phase6-Revised/`,
  > `Phase8-Notebook-Manifest.md` **từ đầu**. Lần chạy thật `pahl-beitz-tap2` (18 chương, 186k từ,
  > 2026-08-23) vẫn báo *"P5 ✅ · P6 ✅ · P8 ✅"* mà **không có file nào trong ba**: rà soát và hiệu
  > chỉnh được làm **tại chỗ** trên Phase4, phát hiện chỉ ghi vào `_pipeline_state.md`. CEO hỏi
  > *"không thấy thư mục Phase6?"* mới lộ.
  >
  > **Đặc tả tồn tại ≠ đặc tả được thi hành.** Cổng này biến đặc tả thành một lệnh.

- **Hiệu chỉnh tại chỗ thì PHẢI để lại danh sách thay đổi.** Nếu P6 sửa thẳng trên bản P4 thay vì
  sinh `Phase6-Revised/`, thì bắt buộc có `Phase6-Revise.md` chứa **diff đo bằng máy** so với ảnh
  chụp trước hiệu chỉnh. Không có ảnh chụp ⇒ nói thẳng là **không đối chiếu được**, đừng bỏ trống.

- **⛔ Sao lưu theo mốc phải có TÊN KHÁC NHAU — kèm GIỜ, không chỉ ngày.**
  ```bash
  cp -r <nguon>/. "<dich>_$(date +%Y-%m-%d_%H%M)/"
  ```
  `cp -r` vào **cùng một đích** không phải sao lưu — nó là **đồng bộ**, và đồng bộ thì huỷ trạng thái
  cũ. Cùng lần chạy trên, tám mốc công việc bị ghi đè thành một; bản sao lưu mang tên `_2026-08-21`
  thật ra giữ trạng thái ngày 22, mtime còn **muộn hơn bản gốc**. Một bản sao lưu mang nhãn sai
  **tệ hơn không có sao lưu** — không có thì biết mình không có điểm quay lui; có nhãn sai thì **tin**
  là có, và chỉ phát hiện khi cần dùng.

- **Pseudocode rule from P4 onwards** — NEVER verbatim source code trong chapters. P7 audit catches nhưng prevention tốt hơn detection.
- **P2 thesis và P3 outline là CEO Core** — AI proposes, CEO approves. Nếu CEO reject thesis → re-run P2 with feedback.
- **P7 IP sign-off là CEO Core** — AI flags potential issues nhưng CEO ra quyết định SAFE/REVIEW/SENSITIVE final.
- **P9 insights là CEO Core** — AI sinh insights từ NLM query, CEO mark actionable và trigger follow-up skills.
- **NLM auth failure = HALT** — Không bypass, instruct CEO chạy `nlm login` trong terminal.
- **Language discipline** — `--lang vi` → all narrative tiếng Việt, technical terms English (queue, dispatcher...). `--lang en` → all English.
- **If CEO says "chạy hết" hoặc "skip checkpoints"** — STILL stop sau each block nhưng checkpoint minimal (1-line summary + "tiếp tục?")

## Integration

```
codebase-to-book (ORCHESTRATOR) COMMANDS:
  → /book-explore      (Block P1)
  → /book-position     (Block P2)
  → /book-outline      (Block P3)
  → /book-write        (Block P4)
  → /book-review       (Block P5)
  → /book-revise       (Block P6)
  → /book-audit        (Block P7)
  → /book-notebook     (Block P8)
  → /book-ceo-insight  (Block P9)

codebase-to-book READS FROM:
  - <path>/**/* — all source files of target codebase
  - <path>/README.md, CLAUDE.md, CONTRIBUTING.md — for context
  - <path>/.git — commit log, tags (nếu git repo)
  
codebase-to-book INVOKES (when --deep):
  - /research --deep <topic> — per subsystem in P1, per chapter in P4
  
codebase-to-book INVOKES (P8/P9 via MCP):
  - mcp__notebooklm-mcp__refresh_auth
  - mcp__notebooklm-mcp__notebook_create
  - mcp__notebooklm-mcp__source_add
  - mcp__notebooklm-mcp__notebook_describe
  - mcp__notebooklm-mcp__notebook_query
  - mcp__notebooklm-mcp__studio_create (optional)

codebase-to-book WRITES TO:
  - <output_dir>/ — all deliverables per Data Bus
  - NotebookLM account — 1 new notebook per book
  
codebase-to-book FOLLOW-UP (CEO-triggered):
  - /research-to-skill → apply HELIX/FORGE insights to upgrade skills
  - /galaxy-note → create Galaxy candidates as permanent notes
  - /helix-design-journal → log decisions influenced by book insights
  - /convert_md_to_docx book.md → publication-ready DOCX
  - /pipeline → NotebookLM cross-notebook queries across multiple books

SHARED REFERENCES (in codebase-to-book/references/):
  - source-prompt.md → original 7-phase prompt
  - book-voice-and-style.md → tone, code rules, Apply This format
  - chapter-template.md → chapter structure template
  - diagram-types.md → Mermaid patterns
  - phase-prompts.md → Task subagent + NLM query templates
```

## Workshop X Applicability

Skill này không chỉ cho software codebases. "Codebase" rộng nghĩa:

**Ứng viên software (thật):**
- `d:\KN-Stack\` — chính repo agentic system này (143 skills, hooks, evals)
- BB-01 LOMAH acoustic simulator
- VN-12.7MM-SIM recoil simulator
- ERPNext customizations

**Ứng viên conceptual (value-dense hơn):**
- **HELIX Pipeline** (34 skills Pahl-Beitz) → sách methodology thiết kế defense
- **ACH Stack** (8-layer AI-for-defense) → reference manual
- **IPARAG Vault** → knowledge-management playbook
- **FORGE Portfolio** → product strategy book
- **Galaxy Zettelkasten** (160 notes) → "Design Judgment Notes"
- **Decision logs** (20+ projects) → case study compendium

**Insight methodology (7-phase mirror HELIX/FORGE/BRIDGE):**
- P1 parallel exploration ↔ HELIX Phase 1 requirements gathering
- P2 thesis (CEO Core) ↔ FORGE portfolio positioning (CEO gate)
- P3 structure ↔ HELIX BD function structure
- P5 multi-role review ↔ HELIX Gate 1-4 + BRIDGE 3-reviewer
- **P7 source audit (verbatim → pseudocode) ↔ Defense IP export control** — layer chưa có trong HELIX/FORGE
- P8 NLM ingest ↔ knowledge permanence (sách thành knowledge base queryable)
- P9 CEO insight lenses ↔ compound learning — book insights loop back to upgrade skills

## COD Classification

- Pipeline orchestration: Offload (O1)
- Block execution: Offload (O2) — mỗi block có own COD
- CEO checkpoints: **Core (C)**
- P2 thesis approval: **Core (C)** — non-delegable
- P3 outline approval: **Core (C)** — non-delegable
- P7 IP sign-off: **Core (C)** — non-delegable
- P9 insight actionability: **Core (C)** — non-delegable
