---
name: btc-extract
description: "Block R2 of book-to-codebase: parallel NLM extraction per chapter — Apply This pre-pass + 6 standard queries + R2.1 derivation. Outputs R2-Extraction-Manifest.md."
---

# BTC-Extract — Block R2

> **Pipeline:** book-to-codebase Block R2
> **Purpose:** Extract all operational patterns from the book via NLM queries. Apply This specs = extraction spine. 6 standard queries per chapter. R2.1 derivation for null fields.
> **Parallel:** YES — N subagents (one per chapter or one per chapter-batch)
> **Standalone:** `/btc-extract <book_output_dir> [--deep-extract]`

## Prerequisites
- R1-Chapter-Index.md exists
- NLM notebook with book chapters ingested (created in R1 or pre-existing from P8)

## Steps

### 1. Read R1 Context
Read `R1-Chapter-Index.md` to get:
- Chapter list + file paths
- Apply This quick-count (sets expectation)
- NLM notebook ID (if stored by R1)

### 2. R2.0 Apply This Pre-Pass (1 fan-out call, all chapters)
Execute NLM query from `../book-to-codebase/references/extraction-templates.md → R2.0`.
Write result to: `R2-raw/R2.0_apply_this_master.md`

### 3. Parallel Chapter Extraction
Fan-out N subagents (one per chapter or batched for small books ≤5 chapters):

Each subagent:
1. Reads chapter file from canonical phase
2. Executes Q1-Q6 NLM queries (from `../book-to-codebase/references/extraction-templates.md → R2 Standard`)
3. If `--deep-extract`: executes Q7-Q9 additionally
4. Executes R2.1 derivation query for null fields
5. Writes `R2-raw/Ch{{NN}}_extraction.md`

### 4. Merge to Extraction Manifest
After all subagents complete, orchestrate merge:
- Deduplicate (Apply This vs prose specs — same concept → keep Apply This as primary)
- Count by concept_kind
- Collect all remaining nulls for R5

Write `R2-Extraction-Manifest.md` per merge structure in `../book-to-codebase/references/extraction-templates.md → R2 Merge`.

## Output
- `R2-raw/R2.0_apply_this_master.md`
- `R2-raw/Ch{{NN}}_extraction.md` (one per chapter)
- `R2-Extraction-Manifest.md` (merged, deduplicated)

## CEO Checkpoint
```
═══ R2 COMPLETE: BTC-Extract ═══
Total specs extracted: {{N}}
  Apply This: {{N}} ({{%}})
  Prose-derived: {{N}} ({{%}})
  Derivations: {{N}} ({{%}})
Null fields remaining: {{N}} (→ R5 ambiguity ledger)
Chapters with no Apply This: {{list or "none"}}

CEO:
(1) ✅ Approve → continue R3 (btc-charter)
(2) 🔍 Review extraction sample (show first 5 specs)
(3) 🔄 Re-run specific chapter extraction
(4) ⏸️ Pause
```
