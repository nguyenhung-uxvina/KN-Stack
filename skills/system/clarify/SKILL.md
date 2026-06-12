---
name: clarify
description: Runs Pahl-Beitz Phase 1 Task Clarification, producing a Project Charter, Requirements List v1.0 (Demands vs Wishes, ≥80% quantified), Stakeholder Analysis, and preliminary Function Structure. Use at project start after Gate 0 is passed. Triggers on: "phase 1", "task clarification", "requirements list", "project charter", "làm rõ nhiệm vụ", "danh sách yêu cầu", "giai đoạn 1".
---
Run Phase 1 Task Clarification for a project following Pahl-Beitz systematic design.

Usage: /clarify [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project? (project code or name)
   - Do you have Phase 0 artifacts? (_Project_Brief.md, ODI report, Gate 0 review)

2. Read existing project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - `1_Projects/{{project}}/_Project_Brief.md`
   - Any Phase 0 documents in the project folder
   - Check if Phase 0 Gate was passed (required before Phase 1)

3. Phase 1 Task Clarification produces these documents (in order):

   **Doc 001: Project Charter**
   - Objective, scope, stakeholders, constraints, timeline
   - Reference: Pahl-Beitz Chapter 5

   **Doc 002: Requirements List v1.0**
   - Structured requirements: Demands (D) vs Wishes (W)
   - Categories: Geometry, Kinematics, Forces, Energy, Material, Signals, Safety, Ergonomics, Production, Quality, Assembly, Transport, Operation, Maintenance, Cost, Schedule
   - Each requirement: ID | Category | D/W | Description | Quantification | Source | Verification Method
   - Target: ≥80% quantified (measurable values, not vague statements)
   - Flag any requirement without quantification as HIGH gap

   **Doc 003: Stakeholder Analysis**
   - Identify all stakeholders (operator, maintainer, procurer, trainer, regulatory)
   - For each: needs, influence, engagement strategy

   **Doc 004: Competitive Analysis**
   - Existing solutions, their strengths/weaknesses
   - Workshop X differentiation

   **Doc 005: Standards & Compliance Matrix**
   - Applicable MIL-STD, TCVN, STANAG standards
   - Map each standard to affected requirements

   **Doc 006: Abstraction & Function Structure (preliminary)**
   - Overall function statement (solution-neutral)
   - Main function → sub-functions decomposition (L1/L2)
   - Input/output flows: Material, Energy, Signal

4. For each document:
   - Draft the document
   - Present to user for review (HITL checkpoint)
   - Wait for approval before proceeding to next
   - Save to `1_Projects/{{project}}/Phase1-Task/{{NNN}}_{{DocName}}_v1.0.md`

5. After all documents created, update Status.md:
   - Mark Phase 1 checkbox
   - Note any open items or flags

6. Suggest next step: Phase 1 Gate Audit (manual review of quantification and conflicts)

RULES:
- Phase 0 Gate MUST be passed before Phase 1 — check Status.md
- Requirements must be QUANTIFIED — "high accuracy" is not acceptable, "accuracy ≤ 1 MOA" is
- Solution-neutral language — describe WHAT, not HOW
- Each document gets its own HITL checkpoint — do not batch
- COD: Offload (AI drafts, CEO reviews and decides on requirements)
- If stakeholder interviews are needed, FLAG them — do not fabricate stakeholder input
- Number documents sequentially: 001, 002, 003...
- Always check for existing Phase 1 documents before creating duplicates
