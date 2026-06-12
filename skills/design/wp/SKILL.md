---
name: wp
description: Searches for working principles for each sub-function in a product's Pahl-Beitz function structure, drawing from physical effects catalogs, solution catalogs, patents, competitor analysis, biomimicry, and TRIZ. Each principle is rated on TRL, local content, and ACH potential; flags any sub-function with fewer than 3 viable principles. Use at Phase 2 concept development to build the morphological matrix. Triggers on: "working principles", "function structure principles", "morphological matrix", "physical effects", "nguyen ly lam viec", "nguyen ly hoat dong", "nguyên lý làm việc", "ma trận hình thái".
---

Search for working principles for each sub-function of a product's function structure.

Usage: /wp [project_name] OR provide function structure interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Do you have the function structure from P17? (paste or reference file path)
   - What domain: training / maritime / engagement / surveillance / logistics?
   - Any existing technologies to consider? (Workshop X assets, etc.)
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - Phase 1 function structure document
3. Execute working principles search:
   - For each sub-function: find 3-5 working principles from >=3 different source types:
     1. Physical effects catalogs
     2. Solution catalogs / design handbooks
     3. Literature / patents
     4. Competitor analysis
     5. Biomimicry / cross-domain analogies
     6. Brainstorming / TRIZ
   - For each principle: Physical Effect | Source Type | TRL | Advantages | Disadvantages | Local Content | ACH Potential
   - Flag any sub-function with <3 viable principles -> search needs widening
   - Flag any principle requiring 100% import components
   - Solution-neutral check: each principle describes a physical effect, NOT a specific product
4. Save output to:
   `1_Projects/{{project}}/Phase2-Concept/{{PROJECT_NAME}}_Working_Principles_v1.0.md`

HITL RULE: Present principles table -> get confirmation before building morphological matrix (P18).
QUALITY CHECK: >=3 different source types used. If <3, flag low-confidence search.
