---
name: lcc
description: Generate a detailed unit cost breakdown and Life Cycle Cost estimate across production volumes, with import-equivalent target check (<=70%), 5-year LCC horizon, and local-content value confirmation. Triggers on "lcc", "life cycle cost", "unit cost", "cost breakdown", "gia thanh", "chi phi vong doi".
---

Generate a detailed unit cost breakdown and Life Cycle Cost estimate.

Usage: /lcc [project_name] OR provide BOM/design details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for?
   - Do you have a BOM? (reference file path or paste key items)
   - What is the target unit cost vs import equivalent?
   - What production volume are you planning (unit/year)?
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - BOM and Phase 3/4 documents
3. Execute cost analysis:
   UNIT COST:
   - Materials + purchased components (from BOM)
   - Manufacturing labor (VN labor rates)
   - Overhead (facility, tooling amortization)
   - Total unit cost at 3 volumes: 10 / 50 / 200 units/year
   COST TARGET CHECK:
   - Compare to import equivalent price
   - Target: unit cost <=70% of import equivalent
   - Flag if over target -> identify top-3 cost drivers
   LIFE CYCLE COST (LCC):
   - Acquisition + Training + Operations + Maintenance + Disposal
   - LCC over 5-year horizon
   - Cost per engagement (for weapon systems)
   LOCAL CONTENT VALUE:
   - % by value sourced locally -> confirm >=60% target
4. Save output to:
   `1_Projects/{{project}}/Phase4-Detail/{{PROJECT_NAME}}_Cost_Analysis_v1.0.md`

COST RULE: Must achieve <=70% of import equivalent. Escalate if target not achievable -- do not hide overruns.
