# S1 Prompt Templates — Phase 1 Task Clarification

Source: `3_Resources/SOPs/S1_prompt_library.md` v5.2

## Applicable P-Templates

| P# | Name | When to Use in Phase 1 |
|----|------|----------------------|
| P01 | Structured Defense Task Delegation | Master template cho mọi delegation task trong Phase 1 |
| P02 | Defense AI QC Review Gate | Chạy trên requirements list trước khi present cho CEO |
| P03 | Engineering Document Generation | Generate requirements document, P12 spec |
| P04 | TCVN Compliance Check | Verify requirements reference correct TCVN standards |
| P05 | Physics Plausibility Check | Validate physics-based requirements (forces, speeds, ranges) |
| P06 | Context Window Scoping | Khi requirements list > 100 items, scope sub-tasks |

## P02 QC Check (MANDATORY on AI-generated requirements)

Run 5-check sequence before presenting requirements to CEO:

```
CHECK 1 — COHERENCE: Do requirements form a consistent set? No contradictions?
CHECK 2 — STANDARDS: Are referenced standards (MIL-STD, TCVN) correct and current?
CHECK 3 — ENVIRONMENT: Are Vietnam conditions accounted for? (25-55°C, 40-100% humidity, salt air)
CHECK 4 — SAFETY: Any requirements involving engagement/weapon parameters? → flag for human review
CHECK 5 — CONFIDENCE: Are AI-generated values justified? Flag high precision + low confidence
```

## Schema v3.0 Fields for Phase 1 Tasks

When delegating Phase 1 sub-tasks to AI:
```
TASK: [specific verb + object]
CONTEXT: Product={{name}}, Phase=1, Standards=[list]
CONSTRAINTS:
  hard_limits: [requirement count ≥ 50, D/W classification = human only]
  reject_conditions: [solution-specific requirements, vendor names in specs]
  prohibited_actions: [classify D/W/PD, hallucinate TCVN numbers]
TOOLS_ALLOWED: [Read, Grep, Glob, WebSearch]
HITL_CHECKPOINT: {requirements_complete: true, abstraction_step5: "IMMEDIATE"}
SAFETY_OVERRIDE: "Any weapon/engagement parameter → CEO review before proceeding"
```
