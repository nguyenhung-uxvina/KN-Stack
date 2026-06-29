---
name: bom
description: Generate a structured Bill of Materials from an embodiment/detail design layout, with MIL-STD flags, local-content accounting (>=60% by value), and supply-chain risk identification. Triggers on "bom", "bill of materials", "danh sach vat tu", "BOM generation", or when finalizing components for a Vietnamese defense program.
---

Generate a structured Bill of Materials from an embodiment design layout.

Usage: /bom [project_name] OR provide design details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - What subsystem or assembly are you building the BOM for?
   - Do you have a layout/embodiment design document to reference?
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - Phase 3 embodiment documents
3. Execute BOM generation:
   - List all components in hierarchical BOM structure (assembly -> subassembly -> part)
   - For each item: Part Number | Description | Qty | Unit | Material/Spec | Make/Buy | Local % | Unit Cost (VND) | Source
   - Flag: MIL-STD compliance requirements per item
   - Flag: items requiring import (local content impact)
   - Calculate: total local content % by value
   - Check: local content target >=60% by value
   - Identify: critical supply chain risks (single-source items, long lead times)
4. Save output to:
   `1_Projects/{{project}}/Phase4-Detail/{{PROJECT_NAME}}_BOM_v1.0.md`

LOCAL CONTENT RULE: Must achieve >=60% by value for Vietnamese defense programs. Flag any shortfall.
NAMING RULE: Always prefix filename with project name (e.g. VN-RANGE-001_BOM_v1.0.md).
