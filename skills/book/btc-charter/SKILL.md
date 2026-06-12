---
name: btc-charter
description: "Block R3 of book-to-codebase: library identity — name, tagline, HELIX-FORGE placement (A/B/C/D), deployment path. CEO Core. Outputs R3-Charter.md."
---

# BTC-Charter — Block R3

> **Pipeline:** book-to-codebase Block R3
> **Purpose:** Define the library's identity — what it is called, where it lives, and how it fits in Workshop X's skill ecosystem. HELIX-FORGE placement (A/B/C/D) is a non-delegable CEO Core decision.
> **CEO Core:** YES — placement decision cannot be approved by AI alone
> **Standalone:** `/btc-charter <book_output_dir>`

## Prerequisites
- R2-Extraction-Manifest.md exists (spec counts + concept_kind distribution)
- If `--suggest` was run: R3.0-Archetypes.md exists (CEO selected archetype)
- If `--from-pipeline`: Phase2-Positioning.md available as charter seed

## Steps

### 1. Read Context
Read:
- R2-Extraction-Manifest.md (summary stats: total specs, concept_kind distribution)
- R3.0-Archetypes.md (if exists — use CEO's selected archetype as seed)
- Phase2-Positioning.md (if `--from-pipeline` — use thesis as library purpose)

### 2. Apply HELIX-FORGE Classification Heuristics
Run through decision flowchart from `../book-to-codebase/references/domain-mapping-heuristics.md → Part 1`.

Produce placement recommendation:
```
Recommended placement: Type {{A/B/C/D}}
Rationale: [2-4 sentences — why this placement based on spec distribution + book structure]
Alternative: Type {{X}} — would apply if [condition]
```

### 3. Draft Charter

Present to CEO for approval:
```
═══ LIBRARY CHARTER PROPOSAL ═══

Library name: {{proposed name}}
Tagline: {{1-line — what the library does}}
Placement: Type {{A/B/C/D}} — {{placement label}}
Deployment path: {{d:\KN-Stack\skills\{{domain}}\ | standalone repo}}
Skill count estimate: {{N}} skills across {{M}} domains
Domain prefix: {{prefix-}} (for Type B) | (n/a for Type A/C/D)

Placement rationale:
{{2-4 sentences from step 2}}

If you prefer different placement:
  Type A: would require reducing scope to ≤3 pipeline-fitting skills
  Type B: would require a single domain prefix covering all skills
  Type C: standalone repo — recommended for compound learning >15 skills
  Type D: no skills — Galaxy notes only

CEO:
(1) ✅ Approve charter as proposed → R4 (btc-architect)
(2) ✏️ Modify: [name / placement / deployment path]
(3) 🔄 Re-run with different archetype
(4) ⏸️ Pause
═════════════════════════════════
```

### 4. Write R3-Charter.md (after CEO approval)

```markdown
# Library Charter — {{slug}}
Approved: {{date}}

name: {{library_name}}
tagline: {{tagline}}
placement: {{A|B|C|D}}
deployment_path: {{path}}
domain_prefix: {{prefix or n/a}}
skill_count_estimate: {{N}}

## Placement Rationale
{{approved rationale}}

## Placement Decision Log
{{CEO's exact words from approval message}}
```

## Output
- `R3-Charter.md`

## Notes
- If CEO requests re-run with different archetype: update R3.0-Archetypes.md with new selection, re-run this block
- Charter is read by R4 (domain taxonomy must align with placement), R6 (skill naming uses domain_prefix), R7 (deployment path in setup.sh)
