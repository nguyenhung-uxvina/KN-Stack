---
name: btc-handoff
description: "Block R9 of book-to-codebase: DMIR retrospective, Galaxy candidates, usage commitment, and pipeline completion. CEO Core. Outputs R9-DMIR.md."
---

# BTC-Handoff — Block R9

> **Pipeline:** book-to-codebase Block R9
> **Purpose:** Close the pipeline with a structured retrospective (DMIR), surface Galaxy permanent note candidates, and secure CEO commitment to an activation cadence for the new skill library.
> **CEO Core:** YES — activation commitment is non-delegable
> **Standalone:** `/btc-handoff <book_output_dir>`

## Prerequisites
- R8-Validation-Report.md (all V2 Red resolved)
- R6-Skill-Registry.md (final skill list)
- R3-Charter.md (library identity)
- R4-Architecture.md (domain map)
- R2-Extraction-Manifest.md (for DMIR Reflect — Cat D gaps)

## Steps

### 1. Read Full Pipeline Ledger
Read `_btc_state.md` → Block Ledger. Reconstruct full pipeline history for DMIR.

### 2. Collect DMIR Prompts
Present 4 DMIR questions (from `book-to-codebase/SKILL.md → DMIR Meta-Layer`):

```
═══ R9: DMIR RETROSPECTIVE ═══
(These are optional — skip any you prefer. Logged as incomplete if skipped.)

D — DIAGNOSE: What problem did this skill library solve that KN-Stack couldn't before?

M — MODEL: What mental model does this library encode?

I — INTERVENE: What will be different in the next real project that uses these skills?
    (Name a specific project + cadence: "I will use {{skill}} when doing {{X}} at {{frequency}}")

R — REFLECT: What did the extraction process reveal about the book itself?
    (Gaps, quality, Apply This density vs expectation)

Respond to any or all. I'll record your answers.
═══════════════════════════════
```

### 3. Surface Galaxy Candidates
From the extraction manifest, identify 3-7 concepts that are:
- Highly abstract (not operational enough for a skill, but intellectually dense)
- Cross-domain (applies beyond this library's domain)
- Have 2+ connections to existing KN-Stack domains

Present as proposed Galaxy permanent notes:
```
GALAXY CANDIDATES ({{N}} proposed):
  - "{{concept name}}" — from Ch{{N}}: {{1-sentence description}}
    Suggested links: [[{{existing galaxy note}}]], [[{{existing galaxy note}}]]
  ...
→ Run /galaxy-note to create these (CEO Core — manual creation only)
```

### 4. Identify Post-R9 Cleanup
From R8 V2 Yellow skills and R5.5 Cat D gaps:
```
POST-R9 CLEANUP (non-blocking — track in backlog):
  Yellow skills needing refinement: {{N}}
  Book gaps (Cat D — signal for next edition): {{N}}
  Section C deferred ambiguities: {{N}}
```

### 5. Write R9-DMIR.md

```markdown
# DMIR Retrospective — {{slug}}
Completed: {{date}}
Pipeline run: R1-R9 ({{N}} CEO checkpoints)

## D — Diagnose
{{CEO answer or "(incomplete)"}}

## M — Model
{{CEO answer or "(incomplete)"}}

## I — Intervene
{{CEO answer or "(incomplete)"}}
Activation commitment: {{specific use case + frequency, or "(not specified)"}}

## R — Reflect
{{CEO answer or "(incomplete)"}}

## Galaxy Candidates
{{list}}

## Post-R9 Cleanup
{{Yellow skills, Cat D gaps, Section C deferrals}}

## Pipeline Summary
Library: {{name}} | {{N}} skills | {{N}} domains | Placement: Type {{A/B/C/D}}
Validation: V1 {{pass/fail}} | V2 {{N}}G/{{N}}Y/{{N}}R | V3 {{pass/fail}} | V4 {{pass/not run}}
Deploy: bash {{library/setup.sh}} --install <vault_path>
```

### 6. Final Completion Message

```
═══════════════════════════════════════════════
BOOK-TO-CODEBASE PIPELINE COMPLETE — {{slug}}
═══════════════════════════════════════════════
Library: {{library_name}} (Type {{placement}})
Skills: {{N}} across {{M}} domains
Location: {{btc_output_dir}}/library/

Deploy:
  bash {{btc_output_dir}}/library/setup.sh --install <vault_path>

Galaxy candidates: {{N}} proposed
  → /galaxy-note to create

Post-R9 cleanup: {{N}} items
  → tracked in R9-DMIR.md

Suggested follow-up:
  /galaxy-note → create R9 Galaxy candidates
  /research-to-skill <skill> → deepen any skill with research
  /helix-design-journal → log DMIR findings
  /codebase-to-book {{btc_output_dir}}/library/ → meta-loop: book the skill library
═══════════════════════════════════════════════
```

## Output
- `R9-DMIR.md`
