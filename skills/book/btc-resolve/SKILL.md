---
name: btc-resolve
description: "Block R5 of book-to-codebase: ambiguity ledger — auto-resolve, ≤30 CEO questions, sane defaults for remainder. Outputs R5-Ambiguity-Ledger.md. Optional R5.5 KN-Stack overlap scan."
---

# BTC-Resolve — Block R5

> **Pipeline:** book-to-codebase Block R5
> **Purpose:** Clear all ambiguities before R6 generates SKILL.md files. Auto-resolve what the rules allow; surface ≤30 questions to CEO; defer the rest with sane defaults.
> **CEO:** Up to 30 questions — answer all or skip (defaults applied to skipped)
> **Standalone:** `/btc-resolve <book_output_dir> [--deep-scaffold]`

## Prerequisites
- R2-Extraction-Manifest.md (all null fields and ambiguities)
- R4-Architecture.md (skill-to-domain mapping, DAG edges)
- R3-Charter.md (placement, naming conventions)

## Steps

### 1. Build Ambiguity Inventory
Scan R2-Extraction-Manifest.md for:
- All null fields (inputs, outputs, stopping_conditions)
- Low-confidence R2.1 derivations
- concept_kind ambiguities
- Naming conflicts (proposed names vs existing KN-Stack names)
- Contradictory specs (same concept, different chapters)
- DAG edge unknowns from R4

Total ambiguity count: {{N}}

### 2. Apply Auto-Resolution Rules
Run through AR-1 through AR-7 from `../book-to-codebase/references/ambiguity-decision-tree.md`.
Write each resolved item to Section A of ledger.

### 3. Prioritize CEO Questions
Sort remaining ambiguities by impact (H/M/L).
Take top 30 → Section B.
Move overflow → Section C with sane defaults.

### 4. Present CEO Questions

Present all Section B questions at once (numbered Q1-Q30 max).
Use question format from `../book-to-codebase/references/ambiguity-decision-tree.md → CEO Question Templates`.

```
═══ R5: AMBIGUITY LEDGER — {{N}} ITEMS TO RESOLVE ═══

Auto-resolved (Section A): {{N}} items
Questions for you (Section B): {{N}} questions (max 30)
Deferred with defaults (Section C): {{N}} items

--- QUESTIONS ---
{{numbered Q1-QN list}}

You can answer all, some, or none.
Unanswered questions will use the default shown in each question.

After your answers: R5 is complete → R6 begins scaffolding.
═══════════════════════════════════════════════════════
```

### 5. Record CEO Answers
For each question with a CEO answer: write answer to Section B.
For each skipped question: apply sane default from `../book-to-codebase/references/ambiguity-decision-tree.md → Sane Defaults`, write to Section C.

### 6. R5.5 KN-Stack Overlap Scan (--deep-scaffold only)
If `--deep-scaffold` flag: run overlap scan per `../book-to-codebase/references/domain-mapping-heuristics.md → Part 3`.
Write `R5.5-Delta-Report.md` with Cat A/B/C/D classification.
Present delta summary before proceeding to R6.

### 7. Finalize Ledger
Write `R5-Ambiguity-Ledger.md` with all three sections populated.

## Output
- `R5-Ambiguity-Ledger.md` (Section A: auto, B: CEO, C: defaults)
- `R5.5-Delta-Report.md` (if --deep-scaffold)

## CEO Checkpoint
```
═══ R5 COMPLETE: BTC-Resolve ═══
Auto-resolved: {{N}}
CEO questions answered: {{N}} / {{N_asked}}
Deferred with defaults: {{N}}
{{If --deep-scaffold: "Delta report: {{A}} overlap | {{B}} partial | {{C}} new | {{D}} gaps"}}

R6 will scaffold {{total_skills}} SKILL.md files across {{N}} domains.

CEO:
(1) ✅ Approve → R6 (btc-scaffold)
(2) 🔄 Revise any answer: Q{{N}} should be [new answer]
(3) ⏸️ Pause
```
