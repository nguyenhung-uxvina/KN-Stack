---
name: btc-architect
description: "Block R4 of book-to-codebase: domain taxonomy + skill DAG from extraction manifest. CEO Core. Outputs R4-Architecture.md with domain map, skill list, dependency edges."
---

# BTC-Architect — Block R4

> **Pipeline:** book-to-codebase Block R4
> **Purpose:** Translate extraction manifest into a structured skill library architecture — domain names, taxonomy style, skill-to-domain assignment, and dependency DAG.
> **CEO Core:** YES — taxonomy determines all downstream file paths and cannot be changed after R6
> **Standalone:** `/btc-architect <book_output_dir>`

## Prerequisites
- R2-Extraction-Manifest.md (all specs with concept_kinds)
- R3-Charter.md (placement A/B/C/D, domain_prefix if B)

## Steps

### 1. Read Charter Constraints
From R3-Charter.md:
- Placement type → constrains taxonomy style (see domain-mapping-heuristics.md Part 2)
- domain_prefix (Type B only) → all skills get this prefix
- deployment_path → affects directory structure

### 2. Select Taxonomy Style
Apply heuristics from `../book-to-codebase/references/domain-mapping-heuristics.md → Part 2`:
- Type A → Style β (phase-prefixed, matching existing helix-p* naming)
- Type B → Style α or β (CEO decides)
- Type C → Style γ (anchor-based — recommended)
- Type D → no taxonomy (Galaxy notes route)

### 3. Propose Domain Map
Group specs from R2-Extraction-Manifest.md into domains.
Present draft:
```
Proposed domains ({{style_label}} taxonomy):
  Domain 1: {{name}} — {{N}} skills — {{concept_kinds present}}
  Domain 2: {{name}} — {{N}} skills — {{concept_kinds present}}
  ...
  Total: {{N}} domains, {{total_skills}} skills
```

Apply naming rules from domain-mapping-heuristics.md (max 8 domains, kebab-case, from book vocabulary).

### 4. Draft Skill List per Domain

For each domain, list proposed skills:
```
Domain: {{domain-name}}
  {{skill-name}} ({{concept_kind}}) — {{1-line purpose from extraction spec}}
  ...
```

### 5. Sketch DAG Edges

Apply DAG construction heuristics from domain-mapping-heuristics.md Part 2:
- Mechanisms: explicit edges from inputs/outputs
- Decision rules: edges from context they consume
- Compounding loops: downstream position in sequence
- Anti-pattern guards: parallel guard edges

Output: list of `A → B (depends_on | informs | guards)` edges.

### 6. CEO Presentation & Approval

```
═══ R4: ARCHITECTURE PROPOSAL ═══
Taxonomy: {{style α/β/γ}} | Placement: Type {{A/B/C/D}}

DOMAIN MAP ({{N}} domains, {{N}} skills):
{{domain table}}

SKILL DAG (key edges):
{{top 10 edges — most connected nodes first}}

Full list: {{btc_output_dir}}/R4-Architecture.md (draft)

CEO:
(1) ✅ Approve → R5 (btc-resolve)
(2) ✏️ Rename domains: [specify]
(3) ✏️ Move skill X to domain Y
(4) ✏️ Merge/split domains: [specify]
(5) ⏸️ Pause
═══════════════════════════════
```

### 7. Write R4-Architecture.md (after CEO approval)

Includes: placement, taxonomy style, domain descriptions, full skill list per domain, DAG edge list, deployment directory structure.

## Output
- `R4-Architecture.md`

## Notes
- R4 is the last CEO Core before R6 creates files — changes after R4 require re-running R6
- DAG is validated in R8 V3; unresolved edges will block V3 pass
