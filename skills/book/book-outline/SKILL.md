---
name: book-outline
description: "Block P3 của codebase-to-book pipeline — tạo TOC với 5-7 parts và 15-20 chapters theo chapter ordering principles (foundations → core loop → capabilities → advanced → infrastructure → performance → epilogue). Mỗi chapter có 2-3 bullet specs. CEO Core decision — outline approval trước khi P4 writers fan-out. Can run standalone. Triggers on: 'book outline', 'TOC', 'table of contents', 'chapter structure', 'parts', 'P3 book'."
---

# Block P3: Outline — Parts, Chapters, and Ordering

> **Pipeline:** codebase-to-book → Block P3
> **Input:** `Phase2-Positioning.md` + `P1_Synthesis.md`
> **Output:** `Phase3-Outline.md`
> **Nature:** **CEO Core** — outline approval non-delegable

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Propose 5-7 parts grouping related chapters | Write chapter content (= P4) |
| Propose 15-20 chapter list với ordering rationale | Skip chapters that don't fit thesis — flag instead |
| Write 2-3 bullet spec per chapter | Deep-dive specific implementations (= P4 subagent job) |
| Propose chapter ordering following 7 principles | Reorder in "alphabetical" or "by subsystem" mode |
| Flag chapters that risk being too big (split) or too small (merge) | Finalize chapter count — CEO decides |
| Assign Apply This format variants (A/B/C rotation) | Assign subagent authors (that's P4 orchestrator job) |

**Multi-Agent Mode:** NO — single synthesis + CEO negotiation.
**CEO Checkpoint:** BLOCKING — outline must be CEO-approved before P4 fan-out (avoid wasted writing).

## Standalone Usage
```
/book-outline <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger
- `Phase2-Positioning.md` — thesis + audience + glossary
- `Phase1-Exploration/P1_Synthesis.md` — cross-cutting patterns, coverage
- `--parts <N>` flag (optional, default 5-7)

## Workflow

### Step P3.1: Load Thesis + Cross-Cutting Patterns

Re-read `Phase2-Positioning.md` thesis + anchors. Re-read `P1_Synthesis.md` cross-cutting patterns + cross-subsystem flows.

### Step P3.2: Chapter Ordering Principles (per source prompt)

Target ordering:

1. **Foundations first** — startup, state, communication with external services
2. **Core loop next** — the main execution cycle (usually most important chapter)
3. **Capabilities built on core** — tools, plugins, extensions
4. **Advanced patterns** — multi-agent, orchestration, coordination
5. **Supporting infrastructure** — UI, networking, persistence
6. **Performance and optimization last** — "you can't optimize what you don't understand"
7. **Epilogue** — synthesis, transferable lessons, forward look

Not every book has every category. Skip gracefully; don't force chapters to fill quota.

### Step P3.3: Propose Parts (5-7)

Default part breakdown:

```markdown
# Part I: Foundations
> <epigraph — 1 line framing this part>
Chapters: <list>

# Part II: The Core Loop
> <epigraph>
Chapters: <list>

# Part III: Capabilities
> ...

# Part IV: Advanced Patterns
> ...

# Part V: Infrastructure
> ...

# Part VI: Performance (optional — if enough material)
> ...

# Part VII: Synthesis
> ...
```

Each part has a **one-line epigraph** — readers pause here. Good epigraphs:
- Surface the tension the part resolves
- Connect to thesis
- Hint at what reader will understand

Example:
> **Part II: The Core Loop** — "Everything in this system is an elaboration on one 30-line function. Nothing runs without touching it, and nothing touches it without passing through the same three guards."

### Step P3.4: Chapter List with Specs

Per chapter spec:

```markdown
## Chapter <NN>: <Title>

**Part:** <N>
**Length target:** <300-800 lines>
**Thesis anchor:** <which of the 3 thesis anchors this chapter reinforces>
**Apply This format:** Variant A | B | C (rotate across book)
**Backward reference:** Chapter <N-1> ended at <topic>; this chapter picks up from <bridge>
**Forward references:** Chapter <M> expands on <topic>; Chapter <K> covers <topic>

**What this chapter teaches** (2-3 bullets):
- <Concrete outcome 1 — reader will understand X>
- <Concrete outcome 2 — reader will be able to describe Y>
- <Concrete outcome 3 — optional, if chapter warrants>

**Source research:**
- Primary: `Phase1-Exploration/<subsystem>_Exploration.md` sections <...>
- Cross-cutting: patterns <X, Y> from P1_Synthesis
- Deep research: invoke `/research --deep "<topic>"` if `--deep` flag — focus area <...>

**Diagrams planned (2-4):**
1. <Diagram 1 — type + what it shows>
2. <Diagram 2 — ...>

**Pseudocode blocks planned (3-5):**
1. <Pattern 1 — what it illustrates>
2. <Pattern 2 — ...>

**Risks:**
- <If something might be too long → split candidate>
- <If relies on later chapter's concept → reorder candidate>
- <IP sensitivity → flag for P7>
```

### Step P3.5: Chapter Size Check

Scan specs for size issues:

```
CHAPTER SIZE AUDIT

✅ Target: 300-800 lines per chapter

OVER (split candidates):
  - Ch <N> <Title> — projected {{X}} lines (>800). Split suggestions:
    - Ch <Na>: <topic A>
    - Ch <Nb>: <topic B>

UNDER (merge candidates):
  - Ch <M> <Title> — projected {{Y}} lines (<200). Merge options:
    - Merge into Ch <M-1> as section
    - Merge with Ch <M+1>
```

### Step P3.6: Chapter Ordering Audit

Scan for ordering violations:

```
ORDERING AUDIT

✅ Rule: Reader should never encounter concept requiring later chapter to understand.

VIOLATIONS DETECTED:
  - Ch <N> mentions <concept X>, but Ch <M> (M > N) introduces X properly
    → Fix option 1: Move concept intro to Ch <N>, reference forward in Ch <M>
    → Fix option 2: Reorder — move Ch <M> before Ch <N>
    → Fix option 3: Brief aside in Ch <N> with "Chapter M covers this in depth"
```

### Step P3.7: Apply This Format Rotation

Assign format variant per chapter to avoid monotony:

```
APPLY THIS FORMAT ROTATION

| Chapter | Format Variant | Rationale |
|---------|---------------|-----------|
| Ch 01 | A (inline header) | Foundation — tight prose style |
| Ch 02 | A | Continuity với Ch 01 |
| Ch 03 | B (bold keywords) | Pattern-heavy chapter — structured lookup better |
| Ch 04 | B | ... |
| Ch 05 | C (quote style) | Rationale chapter — narrative fits |
| Ch 06 | A | Back to inline |
| Ch 07 | C | ... |
| ...   | ...           | ... |

Rule: No 3+ consecutive chapters same variant.
```

Xem `../codebase-to-book/references/chapter-template.md` § "Varying format giữa các chapter" cho 3 variants.

### Step P3.8: Write Phase3-Outline.md

Final doc structure:

```markdown
# Phase 3 Outline — {{slug}}
Date: {{today}}
CEO-approved: <timestamp>

## Summary
- Parts: {{N}}
- Chapters: {{M}}
- Target book length: {{range}} lines total
- Apply This rotation: <distribution>

## Part I: <Title>
> <epigraph>

### Chapter 01: <Title>
[full spec per P3.4]

### Chapter 02: <Title>
[...]

## Part II: <Title>
> <epigraph>

...

## Ordering Rationale
[Why this order — connecting to 7 ordering principles]

## Risks Flagged for Downstream
- Chapter XX length risk → monitor in P4
- Ordering concern YY → re-evaluate after P5 review
- IP sensitivity ZZ → flag for P7

## Glossary Alignment
All chapters use glossary terms from Phase2-Positioning.md. Subagents get glossary in their prompts.
```

### Step P3.9: Update Pipeline State + Ledger

```markdown
### P3 — Outline (<date>)
**Key findings:**
- {{N}} parts × {{M}} chapters ({{range}} total lines projected)
- Chapter size audit: {{X}} splits suggested, {{Y}} merges suggested
- Ordering audit: {{Z}} violations detected → fixed

**Decisions for downstream:**
- P4 fan-out = {{M}} subagents, one per chapter
- Each chapter spec feeds directly to Task prompt (see phase-prompts.md)
- Apply This variant per chapter locked

**Open questions:** [if any]

**CEO checkpoint result:** [approve / revise + notes]
```

## Output

Save to `{{output_dir}}/Phase3-Outline.md`.
Update: `{{output_dir}}/_pipeline_state.md` Block Ledger.

## CEO Checkpoint (BLOCKING — outline is Core)

```
═══ BLOCK P3 OUTLINE COMPLETE ═══
Parts: {{N}}
Chapters: {{M}}
Projected length: {{range}} lines / ~{{pages}} pages equivalent
Thesis anchors balanced: [A: {{n}}, B: {{n}}, C: {{n}}]
Apply This rotation: A={{n}}, B={{n}}, C={{n}}

Deliverables:
  - {{output_dir}}/Phase3-Outline.md

CEO:
(1) ✅ Approve → tiếp tục Block P4 (Writing)
(2) 🔄 Adjust chapter list: [add/remove/rename/reorder]
(3) 🔄 Resize: split Ch <X> / merge Ch <Y> và Ch <Z>
(4) 🔄 Change part structure: [specify]
(5) ⏸️ Dừng — cần đọc outline kỹ trước
═══════════════════════════════════════════════════
```

## COD Classification

- Parts proposal: Offload (O2) — AI drafts
- Chapter list proposal: Offload (O2)
- Chapter specs: Offload (O2)
- Ordering audit: Offload (O2)
- **Outline approval: Core (C)** — non-delegable
- Apply This rotation: Offload (O2) — AI assigns, CEO can override

## Rules

- **Present BEFORE writing** — per source prompt: "Get approval before writing"
- **Outline is contract** — P4 writers MUST follow chapter specs. Deviations flagged in P5.
- **Every chapter references thesis** — via one of 3 anchors. Enforced at chapter opening in P4.
- **Chapter sizing 300-800 lines** — over = split, under = merge. Audit mandatory.
- **Reader never encounters future concept** — ordering audit mandatory.
- **Don't force 7-principle ordering** — if a category doesn't fit, skip. Better 5 strong parts than 7 forced.
- **Epigraph per part** — 1 line, frames the part, connects to thesis.
- **Apply This variant rotation** — no 3+ consecutive same variant.
- **If CEO rejects outline entirely** — ask: "Which chapters do you trust? Which don't fit?" Rebuild from trusted subset.
