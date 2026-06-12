---
name: book-position
description: "Block P2 của codebase-to-book pipeline — define dual-reader audience, extract core thesis (the ONE big insight), và articulate 'why a book' vs 'read the source'. CEO Core decision. Sinh Phase2-Positioning.md + glossary. Can run standalone. Triggers on: 'book positioning', 'thesis', 'audience', 'core insight', 'why a book', 'P2 book'."
---

# Block P2: Positioning — Audience, Thesis, and Book Value

> **Pipeline:** codebase-to-book → Block P2
> **Input:** `Phase1-Exploration/P1_Synthesis.md` + CEO intent
> **Output:** `Phase2-Positioning.md`
> **Nature:** **CEO Core** — thesis is non-delegable. AI proposes, CEO decides.

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Propose dual-reader audience split | Write chapter content (= P4) |
| Propose thesis options (3-5 alternatives) | Decide final thesis — CEO chooses |
| Articulate "why a book" value proposition | Make outline (= P3) |
| Extract glossary of recurring terms | Propose revisions to source code |
| Flag audience conflicts (e.g., leader vs engineer needs) | Over-scope: "every reader imaginable" |

**Multi-Agent Mode:** NO — single synthesis task, CEO-facing.
**CEO Checkpoint:** BLOCKING — thesis decision. No auto-approve.

## Standalone Usage
```
/book-position <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — context từ P1
- `Phase1-Exploration/P1_Synthesis.md` — cross-cutting patterns, surprising decisions
- `Phase1-Exploration/<subsystem>_Exploration.md` × N — specific details
- CEO intent (via checkpoint conversation) — what CEO wants sách này accomplish

## Workflow

### Step P2.1: Read P1 Synthesis Deeply

Load `P1_Synthesis.md` + 2-3 exploration files với highest "surprising decisions" density. Identify:

- Recurring design philosophy (what does this codebase believe?)
- The one big architectural bet
- Patterns that would transfer well to other systems
- Patterns that only work because of this specific context

### Step P2.2: Propose Audience

Dual-reader model (default):

```markdown
## Audience

### Primary Reader A: Technical Leader
- **Who:** Engineering managers, staff/principal engineers, architects
- **What they want:** Architecture, design rationale, transferable lessons
- **Reading style:** Skim code blocks, linger on diagrams và "why" passages, skip deep dives
- **Not want:** Tutorial walkthroughs, implementation minutiae, every edge case

### Primary Reader B: Senior Engineer
- **Who:** Individual contributors deeply curious about this specific system
- **What they want:** Implementation-level understanding, edge cases, performance nuance
- **Reading style:** Read everything including deep dives, examine pseudocode carefully, look for patterns to steal
- **Not want:** High-level overviews without depth

### Who this book is NOT for
- Users of the system (they need a user manual, not this book)
- Beginners learning programming (too much context assumed)
- People deciding whether to adopt the system (they need evaluation criteria, not architecture)
```

### Step P2.3: Propose Thesis Options

Present 3-5 alternative thesis statements. Each:
- 1-2 sentences
- Architectural bet + consequence
- Concrete enough để every chapter reference

Example (from "Claude Code from Source" case study):
> **Thesis A:** "Claude Code is an agent harness pretending to be a CLI. Every technical decision — from the React-based TUI to the tool dispatch layer — serves the goal of making an LLM feel like a first-class terminal citizen."

> **Thesis B:** "The system's hot path is a single message-passing loop. Everything else — MCP servers, plugins, permission prompts — is latency-tolerant infrastructure that decorates that loop without ever blocking it."

> **Thesis C:** "Claude Code's moat isn't the model — it's the harness's ability to recover from bad tool calls, prompt edits, and agent failures without user intervention."

Present format:

```
═══ THESIS OPTIONS — {{slug}} ═══

CEO, I have read P1 exploration deeply. Here are 3-5 thesis candidates. Each is defensible; each shapes the book differently.

Option A: "<thesis A>"
  - Implication for TOC: chapters organize around <X>
  - Core tension the book builds toward: <Y>
  - Who's the ideal reader? <audience bias>
  - Weakness: <what this thesis under-sells>

Option B: "<thesis B>"
  - ...

Option C: "<thesis C>"
  - ...

[Option D, E if applicable]

CEO:
(1) Choose A / B / C / D / E
(2) Hybrid: combine elements from <X> + <Y>
(3) Reject all — my thesis is: <CEO writes>
(4) Not enough data — re-run P1 for subsystem <Z>
═══════════════════════════════════════════════════
```

### Step P2.4: Articulate "Why a Book"

Four value dimensions (every book must justify all four):

```markdown
## Why a Book (Not "Read the Source")

### 1. Narrative
The source has no narrative. Files live alphabetically, not in the order a mind builds understanding. This book orders concepts so each chapter unlocks the next.

### 2. Cross-Cutting Patterns
Patterns like <X> and <Y> are scattered across <N> files in the source — visible only to readers who've internalized the whole thing. The book surfaces these patterns in dedicated chapters.

### 3. Design Rationale
Code records WHAT was built, not WHY or WHAT WAS REJECTED. The book reconstructs rationale from commit history, comment archaeology, and inference — none of which is in the code itself.

### 4. Transferable Lessons
The Apply This sections at each chapter's end extract reusable patterns. Readers leave with 5 × N = {{5×chapter_count}} concrete patterns they can steal for their own systems.
```

### Step P2.5: Extract Glossary

Scan P1 exploration for terms used across multiple subsystems với specific meaning in this codebase:

```markdown
## Glossary

> Terms with codebase-specific meaning. Subsequent chapters use these consistently. Writers in P4 must not introduce synonyms.

| Term | Definition | First appearance |
|------|-----------|------------------|
| <Term A> | <1-line definition — what it means HERE, not generally> | Chapter <N> |
| <Term B> | ... | ... |
```

### Step P2.6: Flag Positioning Risks

```markdown
## Positioning Risks

### Risk: Audience split too wide
If leaders and engineers want fundamentally different books, dual-reader model fails. Mitigation: <approach>.

### Risk: Thesis too narrow
If thesis only covers <X>% of the codebase, other chapters feel disconnected. Mitigation: <approach>.

### Risk: Reader assumed knowledge
If book assumes knowledge of <technology Y>, that limits audience. Acknowledge upfront in preface.

### Risk: IP exposure
Defense codebases: thesis mentioning specific algorithms may telegraph sensitive IP. Flag for P7 audit.
```

### Step P2.7: Write Phase2-Positioning.md

Final document structure:

```markdown
# Phase 2 Positioning — {{slug}}
Date: {{today}}
Author: codebase-to-book pipeline
CEO-approved thesis: <quote>

## Audience
[Dual-reader detail per P2.2]

## Core Thesis
> <CEO-approved thesis statement>

### Thesis commentary
<1-2 paragraphs expanding the thesis — the chain of reasoning from exploration to this claim>

### Thesis anchors
Every chapter will connect back to thesis via one of these anchors:
1. <Anchor 1 — e.g., "The architectural bet">
2. <Anchor 2 — e.g., "The consequence in daily use">
3. <Anchor 3 — e.g., "What the codebase chose NOT to do">

## Why a Book
[Four dimensions per P2.4]

## Glossary
[Per P2.5]

## Positioning Risks
[Per P2.6 — flags for downstream]

## Decisions Locked in This Block
- Thesis: <quote>
- Audience: <leader | engineer | both>
- Language: <vi | en>
- Target length: <N> chapters across <M> parts (to be detailed in P3)
```

### Step P2.8: Update Pipeline State + Ledger

```markdown
### P2 — Positioning (<date>)
**Key findings:**
- Thesis: "<quoted>"
- Audience: dual-reader (leader + engineer)
- Target: ~{{N}} chapters — decided in P3

**Decisions for downstream:**
- P3 must organize chapters around thesis anchors
- P4 must reference thesis explicitly at each chapter opening
- Glossary terms lock terminology — P4 subagents must enforce

**Open questions:** [none unless CEO flagged]

**CEO checkpoint result:** [approve / revise + CEO words]
```

## Output

Save to `{{output_dir}}/Phase2-Positioning.md`.
Update: `{{output_dir}}/_pipeline_state.md` Block Ledger.

## CEO Checkpoint (BLOCKING — thesis is Core)

```
═══ BLOCK P2 POSITIONING COMPLETE ═══
Thesis: "<CEO-approved statement>"
Audience: dual-reader (leader + engineer)
Glossary: {{N}} terms locked
Language: {{vi | en}}

Deliverables:
  - {{output_dir}}/Phase2-Positioning.md

CEO:
(1) ✅ Approve → tiếp tục Block P3 (Outline)
(2) 🔄 Revise thesis: [specify]
(3) 🔄 Revise audience: [specify]
(4) ⏸️ Dừng — need to explore more before deciding
═══════════════════════════════════════════════════
```

## COD Classification

- Audience proposal: Offload (O2) — AI drafts, CEO confirms
- Thesis proposal: Offload (O2) — AI proposes options
- **Thesis selection: Core (C)** — non-delegable
- "Why a book" articulation: Offload (O2)
- Glossary extraction: Offload (O2)
- Risk flagging: Offload (O2) — AI identifies, CEO decides mitigation

## Rules

- **Thesis is CEO Core — never auto-select** — Always present 3-5 options, never "the thesis is..."
- **Every chapter must reference thesis** — enforced in P4 via chapter opening requirement
- **Glossary locks terminology** — P4 subagents get glossary in their prompts, deviations flagged in P5 review
- **If CEO rejects all thesis options** — don't loop. Ask: "What's the ONE thing about this system you wish more people understood?" Use answer as thesis raw material.
- **Dual-reader is default** — if CEO wants single-reader, that's fine. Don't default to hybrid if CEO explicitly chose one.
- **Language decision locked here** — all downstream blocks inherit. Mixing within a book creates editorial nightmare.
