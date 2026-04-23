# S1 Prompt Templates — Phase 3 Embodiment Design

Source: `3_Resources/SOPs/S1_prompt_library.md` v5.2

## Applicable P-Templates

| P# | Name | When to Use in Phase 3 |
|----|------|----------------------|
| P01 | Structured Defense Task Delegation | Master template |
| P02 | Defense AI QC Review Gate | Chạy trên DfX review + BOM draft |
| P03 | Engineering Document Generation | Generate BOM, ICD v3, design specs |
| P05 | Physics Plausibility Check | Structural, thermal, fluid analysis outputs |
| P07 | Sensor Fusion Design Review | IRONMESH products: sensor integration review |
| P50 | Preliminary Stability Check | Maritime products: GM/trim parametric check |
| P51 | Weight Estimate (Bottom-Up) | All products: weight breakdown validation |
| P53 | ICD Template Generation | Cross-domain interface documents |
| P54 | DfX Review Execution | DfM/DfA/DfR/DfT/DfU/DfACH + PLAUSIBLE |
| P55 | Shadow Assumption Extraction | Cross-domain assumption validation |

## Maritime Auto-Invoke (P50 + P51)

For vessel/USV/buoy/floating products, Phase 3 MUST auto-invoke:
1. P51 (Weight Estimate) → bottom-up weight breakdown
2. P50 (Stability Check) → GM ≥ 0.5m, trim < 5% Lwl

## Schema v3.0 for Phase 3

```
TASK: [DfX review / ICD freeze / BOM generation / integration check]
CONTEXT: Product={{name}}, Phase=3, Concept=[selected from Phase 2]
CONSTRAINTS:
  hard_limits: [DfU mandatory, ICD v3 requires human approval, severity H = resolve before Phase 4]
  reject_conditions: [AI generating initial layout, auto-freezing ICD]
  prohibited_actions: [skip PLAUSIBLE, omit DfU for AI/firmware products]
TOOLS_ALLOWED: [Read, Grep, Glob, Write]
HITL_CHECKPOINT: {layout_creation: "IMMEDIATE", icd_freeze: "IMMEDIATE", dfx_fail_H: true}
SAFETY_OVERRIDE: "PLAUSIBLE L-check (Lethality) FAIL → STOP [SAFETY-CRITICAL-DEFECT]"
```
