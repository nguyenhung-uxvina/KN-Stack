---
name: book-write
description: "Block P4 của codebase-to-book pipeline — fan-out N parallel Task subagents (one per chapter) viết từng chương từ scratch sử dụng P1 research notes + P2 thesis + P3 chapter spec. Supports --deep để chain /research per chapter. Enforces chapter template (Opening → Body → Deep Dive → Apply This 5 patterns), voice rules, pseudocode-only code. Can run standalone. Triggers on: 'write chapters', 'viết chương', 'book writing', 'chapter drafts', 'P4 book'."
---

# Block P4: Writing — Parallel Chapter Drafting

> **Pipeline:** codebase-to-book → Block P4
> **Input:** `Phase3-Outline.md` + `Phase2-Positioning.md` + `Phase1-Exploration/` research notes
> **Output:** `Phase4-Chapters/Ch<NN>_<slug>_Draft.md` × N
> **Reference:** `../codebase-to-book/references/phase-prompts.md` (P4 subagent prompt), `chapter-template.md`, `book-voice-and-style.md`

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Fan-out N parallel Task subagents, one per chapter | Write all chapters yourself (sequential = slow + drift) |
| Enforce chapter template structure via prompt | Let subagents invent their own structure |
| Supply each subagent with thesis + glossary + chapter spec | Give subagents full book context (blows prompt) |
| Enforce voice + code rules via prompt | Police style — that's P5's job |
| Invoke `/research --deep` per chapter if `--deep` flag | Start writing without research notes |
| Verify basic quality gates (length, diagrams, pseudocode count) | Do full editorial review (= P5) |

**Multi-Agent Mode:** YES — parallel subagents (typically 12-18 agents, one per chapter).
**CEO Checkpoint:** AFTER all chapters drafted — quick quality scan + approve for P5.

## Standalone Usage
```
/book-write <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P3 approved
- `Phase2-Positioning.md` — thesis + audience + glossary (fed to each subagent)
- `Phase3-Outline.md` — chapter list + specs (one spec per subagent)
- `Phase1-Exploration/` — research notes (subagents read relevant subsystem files)
- `--deep` flag (optional) — subagents invoke `/research --deep` for extra depth

## Workflow

### Step P4.1: Preflight — Verify P3 Approved

Read `_pipeline_state.md` Block Progress table. P3 must show `CEO Approved = YES`. If not, HALT with:
> "Block P3 chưa được CEO approve. Chạy `/book-outline <slug>` trước rồi get approval."

### Step P4.2: Load Chapter Specs

Parse `Phase3-Outline.md` → list of chapter objects:
```
chapters = [
  {
    num: 1,
    title: "Runtime Startup",
    slug: "runtime-startup",
    part: 1,
    spec_bullets: [...],
    thesis_anchor: "A",
    apply_variant: "A",
    backward_ref: "This chapter begins the journey...",
    source_files: ["Phase1-Exploration/startup_Exploration.md"],
    diagrams_planned: [...],
    pseudocode_planned: [...],
    length_target: "400-600 lines",
    deep_research_topic: "Runtime startup patterns in agentic systems",
  },
  ...
]
```

### Step P4.3: Fan-Out Writing Subagents

Spawn N Task subagents **trong single message** (multiple tool calls parallel):

```python
# Pseudocode — orchestrator fan-out
output_dir_p4 = f"{output_dir}/Phase4-Chapters"
mkdir(output_dir_p4)

# Single message with N Task tool calls
for ch in chapters:
    Task(
        description=f"Write Ch{ch.num:02d}: {ch.title}",
        subagent_type="general-purpose",  # writing task needs general capability
        prompt=render_p4_prompt(
            chapter=ch,
            positioning_file=f"{output_dir}/Phase2-Positioning.md",
            outline_file=f"{output_dir}/Phase3-Outline.md",
            research_files=ch.source_files,
            output_file=f"{output_dir_p4}/Ch{ch.num:02d}_{ch.slug}_Draft.md",
            references=[
                "../codebase-to-book/references/book-voice-and-style.md",
                "../codebase-to-book/references/chapter-template.md",
                "../codebase-to-book/references/diagram-types.md",
            ],
            lang=args.lang,
            deep=args.deep,
        )
    )
```

**Subagent prompt template:** See `../codebase-to-book/references/phase-prompts.md` § "Phase 4 — Writing Subagent Prompt".

### Step P4.4: Subagent Responsibilities (enforced via prompt)

Each subagent must:

1. **Read inputs** — positioning, outline (full, for cross-refs), relevant P1 exploration files
2. **Invoke `/research --deep <topic>`** if `--deep` flag set — wait for completion, read research output
3. **Draft chapter** per template:
   - Opening: 2-3 paragraphs (Problem → Connection → Promise)
   - Body: 3-5 sections với prose + diagram(s) + pseudocode(s) + table(s)
   - Deep Dive: 0-2 inline callouts (implementation depth leaders can skip)
   - Apply This: exactly 5 patterns (Name, Problem, Adapt, Pitfall)
4. **Validate before submit:**
   - Length 300-800 lines
   - 2-4 Mermaid diagrams
   - 3-5 pseudocode blocks, 5-15 lines each, "// Pseudocode —" label
   - No verbatim source code
   - 5 Apply This patterns
   - Backward reference to previous chapter at opening
5. **Save to output file.** Return 3-line summary to orchestrator.

### Step P4.5: Collect + Quality Scan

After all subagents return, orchestrator scans each chapter for basic violations:

```python
# Pseudocode — quality scan
for ch_file in glob(f"{output_dir_p4}/*_Draft.md"):
    content = read(ch_file)
    checks = {
        "length_ok": 300 <= count_lines(content) <= 800,
        "diagrams_count": count_mermaid_blocks(content) in range(2, 5),
        "pseudocode_count": count_code_blocks(content) in range(3, 6),
        "pseudocode_labels": all("Pseudocode" in block.first_line for block in code_blocks),
        "apply_this_count": count_apply_this_patterns(content) == 5,
        "opening_has_backward_ref": detect_backward_ref(content[:first_1000_chars]),
        "no_verbatim": not contains_suspiciously_verbatim_code(content),  # heuristic
    }
    
    if not all(checks.values()):
        flag_for_revision(ch_file, failed_checks=checks)
```

### Step P4.6: Handle Quality Failures

Two paths:

**Path A — Auto-retry (for simple failures):**
- Chapter too short (<300 lines) → re-invoke subagent with "chapter was too terse, expand sections X, Y"
- Missing Apply This pattern → re-invoke with "add missing 5th pattern"
- Missing backward reference → re-invoke with "add opening sentence connecting to Ch N-1"

**Path B — Flag for CEO (complex failures):**
- Verbatim source suspected → CEO reviews in checkpoint, decision: fix in P4 OR defer to P7 audit
- Structural issues (3 bullets missing, wrong chapter focus) → CEO reviews outline alignment

### Step P4.7: Update Pipeline State + Ledger

```markdown
### P4 — Writing (<date>)
**Key findings:**
- {{M}} chapter drafts produced
- Total lines drafted: {{total}}
- Quality scan: {{N_pass}} passed, {{N_retry}} auto-retried, {{N_flag}} flagged for CEO
- Deep research: {{X}} NLM notebooks consulted (if --deep)

**Decisions for downstream:**
- P5 review should prioritize flagged chapters: [list]
- Cross-chapter consistency: pending P5 audit
- Diagram quality: pending P5 audit

**Open questions:**
- Chapter <N>: <specific concern>

**CEO checkpoint result:** [pending]
```

## Output

Save to `{{output_dir}}/Phase4-Chapters/`:
- `Ch<NN>_<slug>_Draft.md` × N (N = chapter count from outline)

Update: `{{output_dir}}/_pipeline_state.md` Block Ledger.

## CEO Checkpoint

```
═══ BLOCK P4 WRITING COMPLETE ═══
Chapters drafted: {{M}}/{{N_planned}}
Total lines: {{total_lines}}
Quality scan:
  ✅ Passed: {{N_pass}}
  🔄 Auto-retried: {{N_retry}} (now passing)
  ⚠️  Flagged: {{N_flag}} (details below)

Flagged chapters:
  - Ch {{X}}: {{issue summary}}
  - Ch {{Y}}: {{issue summary}}

Deliverables:
  - {{output_dir}}/Phase4-Chapters/ ({{M}} files)

CEO:
(1) ✅ Approve → tiếp tục Block P5 (Review)
(2) 🔄 Re-write specific chapter: [specify Ch number + reason]
(3) 🔄 Revise outline và re-run P4 for affected chapters (goes back to P3)
(4) ⏸️ Dừng — CEO cần read chapter drafts trước
═══════════════════════════════════════════════════
```

## COD Classification

- Fan-out orchestration: Offload (O1)
- Chapter writing (subagents): Offload (O2)
- Deep research invocation: Offload (O2) with internal CEO gates
- Quality scan: Offload (O2)
- Auto-retry decision: Offload (O2)
- Flag-for-CEO decision: Offload (O2) — AI detects, CEO resolves
- Final chapter approval: **Core (C)** — CEO skims và approve batch

## Rules

- **Outline is contract** — subagents must follow chapter spec từ P3
- **Each subagent = one chapter** — don't batch 2+ chapters per agent (context dilution)
- **Thesis reference mandatory at opening** — enforced in prompt, flagged in quality scan
- **Pseudocode rule enforced early** — P7 catches violations but preventing at P4 saves iteration
- **Backward reference mandatory** — Ch N must connect to Ch N-1 explicitly (except Ch 1)
- **Glossary terms locked** — subagents get glossary, must not introduce synonyms
- **Length discipline** — <300 = too shallow, >800 = too much. Auto-retry for simple over/under.
- **Apply This exactly 5 patterns** — rigorously enforced
- **Apply This variant per chapter** — follow P3 assignment
- **Parallel fan-out in single message** — multiple Task calls together, not sequentially
- **If >30% chapters fail quality scan** — likely outline problem (P3) or exploration gap (P1). Halt và escalate to CEO.
- **--deep calls happen INSIDE subagents** — not orchestrator. Each subagent owns its research chain.
