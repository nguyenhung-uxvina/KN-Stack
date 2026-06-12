---
name: opt
description: Conducts a Pahl-Beitz design optimization review for Workshop X products to improve weight, cost, part count, and local content percentage. Analyzes 5 optimization categories and quantifies trade-offs for each opportunity, with mandatory HITL approval before implementation. Use at Phase 3 embodiment or when DfX scores flag weaknesses. Triggers on: "optimize design", "weight reduction", "cost optimization", "reduce part count", "local content", "toi uu thiet ke", "giam trong luong", "tối ưu thiết kế", "giảm chi phí sản xuất".
---

Conduct a design optimization review to improve weight, cost, part count, and performance.

Usage: /opt [project_name] OR provide design details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Do you have the current embodiment layout?
   - DfX results from P25? (which categories scored <=3?)
   - Current estimates: weight, cost, part count, local content %?
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - Phase 3 embodiment documents
3. Execute optimization review:
   - Analyze 5 optimization categories:
     1. Weight -- material substitution, topology, consolidation
     2. Cost -- material downgrade (where margin allows), process change, standard parts
     3. Part Count -- multi-function parts, integral features, consolidation
     4. Performance -- address DfX weak spots (scores <=3)
     5. Local Content -- find local alternatives for import items
   - Identify >=5 optimization opportunities, ranked by impact
   - For each: quantify improvement AND state trade-off (no free lunches)
   - Present before/after summary table
   - HITL: user decides which optimizations to implement
4. Save output to:
   `1_Projects/{{project}}/Phase3-Embodiment/{{PROJECT_NAME}}_Optimization_Review_v1.0.md`

SAFETY RULE: Any optimization reducing safety margin -> flag [SAFETY-TRADE-OFF]. Do not implement without explicit approval.
LOCAL CONTENT: Optimizations must not decrease local content below 60%.
