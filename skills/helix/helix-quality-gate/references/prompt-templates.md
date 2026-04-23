# S1 Prompt Templates — Gate Reviews

Source: `3_Resources/SOPs/S1_prompt_library.md` v5.2

## Applicable P-Templates

| P# | Name | When to Use |
|----|------|-------------|
| P02 | Defense AI QC Review Gate | Content quality check on all AI-generated gate artifacts |
| P04 | TCVN Compliance Check | Standards compliance at every gate |
| P05 | Physics Plausibility Check | Gate 2+ physics validation |
| P55 | Shadow Assumption Extraction | Gate 2+ cross-domain assumption check |
| P56 | Gate Review Execution | Master gate template: auto-check + P02 + human judgment |

## P56 Gate Review Flow

```
Step 1: Auto-checks (A-items) → file existence, completeness
Step 2: P02 Content Quality (5 checks) → AI output integrity
Step 3: PLAUSIBLE 9-check → AI output physics/logic validation
Step 4: S-items → Cross-domain sync verification
Step 5: H-items → Human judgment (CEO decides PASS/FAIL)
Step 6: Score → /4.0 → PASS/CONDITIONAL/REVISE/FAIL
```

## Compliance Tracking (S5 Integration)

Per-gate standards verification:

| Gate | Standards to Verify |
|------|-------------------|
| Gate 1 | Requirements reference correct MIL-STD/TCVN/STANAG |
| Gate 2 | Concept evaluation uses correct VDI 2225 methodology |
| Gate 3 | DfX checks against applicable manufacturing standards |
| Gate 4 | Drawing standards ISO 128, GD&T ISO 1101, material specs |

## Schema v3.0 for Gate Reviews

```
TASK: [gate N review for {{product}}]
CONTEXT: Product={{name}}, Gate={{N}}, Phase={{current}}→Phase={{next}}
CONSTRAINTS:
  hard_limits: [H-item FAIL = max CONDITIONAL, score < 2.5 + critical blocker = FAIL]
  reject_conditions: [auto-passing gate, skipping H-items]
  prohibited_actions: [delete gate results, approve without CEO input]
HITL_CHECKPOINT: {h_items: "IMMEDIATE", go_nogo: "IMMEDIATE"}
SAFETY_OVERRIDE: "PLAUSIBLE L-check (Lethality) REJECT → gate blocked"
```
