# S1 Prompt Templates — Phase 4 Detail Design

Source: `3_Resources/SOPs/S1_prompt_library.md` v5.2

## Applicable P-Templates

| P# | Name | When to Use in Phase 4 |
|----|------|----------------------|
| P01 | Structured Defense Task Delegation | Master template |
| P02 | Defense AI QC Review Gate | Chạy trên manufacturing package trước release |
| P03 | Engineering Document Generation | Drawings specs, assembly instructions, manuals |
| P04 | TCVN Compliance Check | Final standards compliance verification |
| P49 | Governance Document Generation | System limitations, accountability docs |
| P52 | SOP Update from Design Decisions | Batch update SOPs from Phase 3-4 decisions |

## Schema v3.0 for Phase 4

```
TASK: [finalize drawings / generate BOM / create inspection checklist / assembly instructions]
CONTEXT: Product={{name}}, Phase=4, Layout=[frozen from Phase 3]
CONSTRAINTS:
  hard_limits: [GD&T on critical dims, ISO 128/TCVN drawing standards, Rev control A/B/C]
  reject_conditions: [releasing without workshop master review]
  prohibited_actions: [skip tolerance stack-up, omit inspection checklist]
TOOLS_ALLOWED: [Read, Grep, Glob, Write]
HITL_CHECKPOINT: {gdt_critical_dims: "IMMEDIATE", workshop_review: "IMMEDIATE"}
SAFETY_OVERRIDE: "Manufacturing package release = commitment — verify before shipping"
```
