---
name: book-review
description: "Block P5 của codebase-to-book pipeline — launch 2-3 editorial review subagents, mỗi agent cover một section của sách, evaluate 7 dimensions (opening, flow, cuts, missing content, diagrams, consistency, specific fixes). Consolidate vào Phase5-Review.md prioritized by severity (CRITICAL/MAJOR/MINOR). Can run standalone. Triggers on: 'book review', 'editorial review', 'review chapters', 'feedback', 'audit drafts', 'P5 book'."
---

# Block P5: Editorial Review — Multi-Agent Feedback Consolidation

> **Pipeline:** codebase-to-book → Block P5
> **Input:** `Phase4-Chapters/Ch*_Draft.md` × N
> **Output:** `Phase5-Reviews/Review_Ch<N>-<M>.md` × (2-3) + `Phase5-Review.md` (consolidated)
> **Reference:** `codebase-to-book/references/phase-prompts.md` § Phase 5 Review Subagent Prompt

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Spawn 2-3 review subagents covering book sections | Rewrite chapters (= P6's job) |
| Evaluate 7 dimensions per chapter (opening, flow, cuts, missing, diagrams, consistency, fixes) | "Nitpick everything" — flag concrete actionable issues only |
| Consolidate reviews into prioritized action plan | Let reviews contradict without flagging disagreement |
| Flag cross-chapter consistency issues | Check IP sensitivity (= P7) |
| Sort issues by severity (CRITICAL / MAJOR / MINOR) | Apply fixes (= P6) |

**Multi-Agent Mode:** YES — 2-3 parallel review subagents.
**CEO Checkpoint:** After consolidation — CEO reviews severity distribution + decides scope of P6.

## Standalone Usage
```
/book-review <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P4 complete
- `Phase4-Chapters/Ch*_Draft.md` × N
- `Phase2-Positioning.md` — for consistency checks (glossary, thesis, voice)
- `Phase3-Outline.md` — để reviewers know chapter specs

## Workflow

### Step P5.1: Partition Book into Review Sections

Divide chapters among review agents. Rules:
- 2 agents for books ≤ 10 chapters
- 3 agents for books 11-20 chapters
- Partition roughly even, keeping parts intact when possible

```
REVIEW PARTITION — {{slug}} ({{N_chapters}} chapters)

Review Agent 1: Ch 01–06 (Parts I–II — Foundations + Core Loop)
Review Agent 2: Ch 07–12 (Parts III–IV — Capabilities + Advanced)
Review Agent 3: Ch 13–18 (Parts V–VII — Infrastructure + Performance + Epilogue)
```

### Step P5.2: Fan-Out Review Subagents

Spawn 2-3 subagents in single message:

```python
# Pseudocode
output_dir_p5 = f"{output_dir}/Phase5-Reviews"
mkdir(output_dir_p5)

for partition in review_partitions:
    Task(
        description=f"Review Ch{partition.start}-{partition.end}",
        subagent_type="general-purpose",
        prompt=render_p5_prompt(
            chapter_range=partition,
            chapter_files=partition.files,
            positioning_file=f"{output_dir}/Phase2-Positioning.md",
            outline_file=f"{output_dir}/Phase3-Outline.md",
            output_file=f"{output_dir_p5}/Review_Ch{partition.start}-{partition.end}.md",
            references=["codebase-to-book/references/book-voice-and-style.md"],
        )
    )
```

### Step P5.3: Review Framework (7 Dimensions)

Each reviewer evaluates each chapter trên 7 dimensions:

#### 1. Opening Quality
- Does it hook in first paragraph?
- Explicit backward reference to previous chapter?
- Promise states concrete outcomes (not vague "you'll learn about X")?

#### 2. Flow
- Sections that drag, repeat, or list facts without building insight?
- Pacing appropriate (not too fast for complex concepts, not dwelling on simple ones)?
- Transitions between sections natural?

#### 3. Content Cuts
- Reference-manual content not serving narrative?
- Code blocks >20 lines?
- Bullet lists that should be prose or tables?
- Deep Dives that should be cut or moved inline?

#### 4. Missing Content
- Gaps where reader would be confused?
- Missing transitions between sections?
- Concepts introduced without enough grounding?
- Trade-offs mentioned without explaining the other side?

#### 5. Diagrams Needed
- Walls of text that should be diagrams?
- Specific proposals: "Replace paragraph 3 of section X with sequence diagram showing Y"

#### 6. Cross-Chapter Consistency
- Voice drift (one chapter reads differently from others)?
- Terminology inconsistency (same concept, different names)?
- Contradictions (Ch 5 says X, Ch 9 implies not-X)?
- Repeated rhetorical phrases across chapters?

#### 7. Specific Fixes
- 5-10 concrete sentences/paragraphs to rewrite
- Each: quote original + suggested replacement + reason

### Step P5.4: Severity Ranking

Each issue tagged:

- **CRITICAL** — blocks publication. Must fix before P6 release.
  - Factual errors, contradictions between chapters, thesis disconnect
  - Verbatim source code (should be caught by P4 but sometimes slips — P7 safety net)
  - Missing chapter concepts entirely
- **MAJOR** — quality degrading, should fix.
  - Opening doesn't hook, slow flow, missing key diagram
  - Terminology drift, missing cross-references
- **MINOR** — polish improvements.
  - Single awkward sentence, could-be-cleaner bullet list
  - Style preference issues

### Step P5.5: Consolidation (Orchestrator)

After 2-3 reviewers return, orchestrator merges:

```python
# Pseudocode
all_reviews = [read(f) for f in glob(f"{output_dir_p5}/Review_*.md")]

# Deduplicate: if 2 reviewers flag same issue, merge
deduplicated = dedupe_issues(all_reviews, similarity_threshold=0.7)

# Flag disagreements: if reviewers conflict, surface both
disagreements = find_conflicts(all_reviews)

# Sort by severity then by chapter
sorted_issues = sorted(deduplicated, key=lambda x: (severity_rank(x), x.chapter))

# Group by chapter for P6 ease
grouped = group_by_chapter(sorted_issues)

write_consolidated_review(f"{output_dir}/Phase5-Review.md", grouped, disagreements)
```

### Step P5.6: Consolidated Review Document Format

```markdown
# Phase 5 Consolidated Review — {{slug}}
Date: {{today}}
Reviewers: {{N}} agents
Chapters reviewed: {{M}}

## Severity Distribution
- CRITICAL: {{N}} issues
- MAJOR: {{N}} issues
- MINOR: {{N}} issues
Total: {{N}}

## Prioritized Action Plan (for P6 — Revision)

### CRITICAL Issues

#### Ch <N>: <Issue summary>
- **Dimension:** <opening|flow|cuts|missing|diagrams|consistency|specific>
- **Reviewer:** Agent <X>
- **Quote:** <original text>
- **Problem:** <why it's critical>
- **Fix:** <proposed replacement>
- **Severity reason:** <why CRITICAL, not MAJOR>

[more CRITICAL issues, grouped by chapter]

### MAJOR Issues

[...similar format, grouped by chapter]

### MINOR Issues

[brief list, not full detail — P6 fixes in batch]

## Reviewer Disagreements

### Disagreement 1: Ch <N> — <topic>
- Agent X says: <claim A>
- Agent Y says: <claim B>
- Orchestrator assessment: <which is more likely correct + reasoning>
- Recommendation: <ask CEO OR trust one reviewer based on context>

## Cross-Chapter Issues
(Not tied to specific chapter — book-level concerns)

### 1. Voice drift
- Chapters <X, Y, Z> read differently from rest
- Rewrite guidance: <specific voice anchors to re-apply>

### 2. Terminology inconsistency
- Term "dispatcher" (glossary) sometimes written as "router" or "mediator"
- Affected chapters: <list>

## P6 Scope Recommendation
- Must-fix: CRITICAL + high-impact MAJOR
- Should-fix: remaining MAJOR
- Optional: MINOR batch
```

### Step P5.7: Update Pipeline State + Ledger

```markdown
### P5 — Review (<date>)
**Key findings:**
- CRITICAL: {{N}}, MAJOR: {{N}}, MINOR: {{N}}
- Reviewer disagreements: {{N}}
- Cross-chapter issues: {{N}}

**Decisions for downstream:**
- P6 scope: [CEO-approved — must-fix / should-fix / optional]
- Chapters requiring most work: Ch <X>, Ch <Y>

**Open questions:**
- Disagreement on Ch <N> — CEO input needed if not resolved in checkpoint

**CEO checkpoint result:** [pending]
```

## Output

Save to `{{output_dir}}/`:
- `Phase5-Reviews/Review_Ch<N>-<M>.md` × (2-3)
- `Phase5-Review.md` (consolidated)

Update: `{{output_dir}}/_pipeline_state.md`.

## CEO Checkpoint

```
═══ BLOCK P5 REVIEW COMPLETE ═══
Issues found: {{total}} total
  🔴 CRITICAL: {{N}}
  🟠 MAJOR: {{N}}
  🟡 MINOR: {{N}}

Reviewer disagreements: {{N}}
Cross-chapter issues: {{N}}

Most flagged chapter: Ch {{X}} ({{count}} issues)
Least flagged chapter: Ch {{Y}} ({{count}} issues)

Deliverables:
  - {{output_dir}}/Phase5-Reviews/ ({{N}} review files)
  - {{output_dir}}/Phase5-Review.md (consolidated action plan)

CEO P6 scope decision:
(1) ✅ Fix all CRITICAL + MAJOR (standard)
(2) ✅ Fix all CRITICAL + MAJOR + MINOR (thorough)
(3) ✅ Fix CRITICAL only (quick)
(4) 🔄 Re-run review with different focus: [specify]
(5) ⏸️ Dừng — CEO cần đọc review trước

Reviewer disagreements need CEO input: {{list if any}}
═══════════════════════════════════════════════════
```

## COD Classification

- Partition decision: Offload (O2)
- Review fan-out: Offload (O1)
- Per-chapter evaluation: Offload (O2) — reviewer subagents
- Consolidation + deduplication: Offload (O2)
- Disagreement resolution: Offload (O2) / **Core (C)** for substantive conflicts
- P6 scope decision: **Core (C)** — CEO decides quality budget

## Rules

- **2-3 reviewers, not 1** — different eyes catch different issues. Single reviewer misses ~30% of problems.
- **5-10 specific fixes per reviewer minimum** — vague "improve flow" not acceptable. Concrete quote + replacement.
- **Severity discipline** — CRITICAL reserved for publication blockers. Don't inflate.
- **Flag disagreements, don't hide** — if reviewers conflict, surface both. CEO or P6 agent decides.
- **Cross-chapter consistency is reviewer job** — reviewers read multiple chapters, can detect drift individual chapter writers cannot.
- **Don't rewrite — review** — reviewers produce feedback, not revised chapters. P6 applies the fixes.
- **Consolidated review is P6 contract** — P6 must address every CRITICAL + MAJOR at minimum.
- **If reviewers return <10 issues total** — review was superficial. Re-run with stricter prompt.
