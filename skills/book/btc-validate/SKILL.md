---
name: btc-validate
description: "Block R8 of book-to-codebase: 4-layer validation — V1 static + V2 semantic (NLM) + V3 DAG + V4 e2e (--deep). Outputs R8-Validation-Report.md. V2 Red skills block R9."
---

# BTC-Validate — Block R8

> **Pipeline:** book-to-codebase Block R8
> **Purpose:** Verify the generated skill library against 4 validation layers before handoff. V2 Red skills must be fixed or removed. V4 is optional (CEO or --deep-scaffold).
> **Standalone:** `/btc-validate <book_output_dir> [--deep-scaffold]`

## Prerequisites
- All R6 SKILL.md files generated
- R7-Infrastructure-Bundle.md (all infra files present)
- R4-Architecture.md (DAG edges for V3)
- Book's NLM notebook accessible (for V2)

## Steps

### 1. V1 — Static Validation
Check all SKILL.md files per criteria in `../book-to-codebase/references/validation-rubric.md → V1`.
Run locally — no NLM queries.
Log failures to `R8-Validation-Report.md → V1 Static Results`.

### 2. V2 — Semantic Validation
Per domain: run NLM query from `../book-to-codebase/references/validation-rubric.md → V2 Query Template`.
Classify each skill as Green / Yellow / Red.
Log results to `R8-Validation-Report.md → V2 Semantic Results`.

**Red skills:** present to CEO with remediation options:
- Fix: re-run btc-scaffold for this skill with NLM correction guidance
- Remove: drop from R6-Skill-Registry.md; document in R9 DMIR as gap
- Keep as-is: CEO accepts known misalignment (unusual)

### 3. V3 — DAG Validation
Check R4-Architecture.md edges against actual generated skill files.
Per criteria in `../book-to-codebase/references/validation-rubric.md → V3`.
Log failures.

### 4. V4 — E2E Validation (--deep-scaffold or CEO request)
Run functional test per criteria in `../book-to-codebase/references/validation-rubric.md → V4`.
Sample strategy: all skills if ≤15; partial sample if >15 (all Wave 4 + all V2 Yellow/Red).

### 5. Write Validation Report
Compile `R8-Validation-Report.md` per format in validation-rubric.md.

### 6. CEO Checkpoint

```
═══ R8 COMPLETE: BTC-Validate ═══
V1 Static: {{PASS | FAIL (N failures)}}
V2 Semantic: {{N}} Green / {{N}} Yellow / {{N}} Red
V3 DAG: {{PASS | FAIL (N unresolved edges / N cycles)}}
{{V4 E2E: {{PASS | FAIL}} | (not run)}}

{{If Red skills exist:
  RED SKILLS (must resolve before R9):
  - {{skill}}: {{NLM finding}}
  Options: [fix / remove / accept]}}

{{If all Green:
  All {{N}} skills validated. Ready for R9 handoff.}}

CEO:
(1) ✅ Approve (accept Yellow as-is; will note in R9)
(2) 🔧 Fix Red skills: [specify which and how]
(3) 🗑️ Remove Red skill [name]
(4) ⏸️ Pause
```

## Output
- `R8-Validation-Report.md`

## Notes
- V1 failures are auto-fixed inline if mechanical (missing section headers, unfilled template braces)
- V2 Yellow skills are noted in R9 DMIR as "post-R9 cleanup candidates"
- V2 Red skills are a hard blocker for R9 unless CEO explicitly accepts
