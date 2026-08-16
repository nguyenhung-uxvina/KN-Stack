---
name: gate1
description: Conducts the formal Phase 1 Gate Review scoring Requirements Completeness, Quantification Level, D/W Classification, Stakeholder Coverage, Standards Mapping, Function Structure, and Conflict Check (weighted, target ≥3.0/4.0) before authorizing Phase 2. Flags every unquantified D-requirement as a HIGH gap. Triggers on: "gate 1", "G1", "phase 1 gate", "requirements gate", "xét duyệt cổng 1", "nghiệm thu giai đoạn 1".
---
Conduct the formal Phase 1 Gate Review before proceeding to Phase 2 Conceptual Design.

Usage: /gate1 [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Provide references to Phase 1 artifacts (charter, requirements, stakeholders, function structure)
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - All Phase 1 documents in `1_Projects/{{project}}/Phase1-Task/`
3. Execute the gate review workflow:
   - Score 7 criteria independently (0-4 each):
     A. Requirements Completeness (20%) -- all categories covered? (Geometry, Kinematics, Forces, Energy, Material, Signals, Safety, Ergonomics, Production, Quality, Assembly, Transport, Operation, Maintenance, Cost, Schedule)
     B. Quantification Level (20%) -- target >=80% of requirements have measurable values
     C. Demand vs Wish Classification (10%) -- every requirement marked D or W?
     D. Stakeholder Coverage (10%) -- operator, maintainer, procurer, trainer, regulatory all addressed?
     E. Standards Mapping (10%) -- applicable MIL-STD, TCVN, STANAG identified and mapped to requirements?
     F. Function Structure (15%) -- overall function defined solution-neutral? Sub-functions decomposed to L2 minimum?
     G. Conflict Check (15%) -- requirements internally consistent? No contradictions between D-requirements?
   - Calculate weighted total
   - Target: >=3.0/4.0
   - Flag specific gaps:
     - List each unquantified D-requirement as HIGH gap
     - List each requirement conflict as finding (HIGH/MEDIUM/LOW)
     - List missing stakeholder perspectives
   - Present gate decision: PASS / CONDITIONAL PASS / FAIL
   - WAIT for explicit user response
4. Save output to:
   `1_Projects/{{project}}/Phase1-Task/{{PROJECT_NAME}}_Phase1_Gate_Review_v1.0.md`

CRITICAL: This is a NEVER-AUTOMATE decision. Present scores and WAIT.
BLOCKER: Quantification <60% -> FAIL regardless of other scores.
BLOCKER: Any unresolved D-requirement conflict -> CONDITIONAL at best.
FLAG: Missing stakeholder interviews -> note as risk, don't auto-reject.

After the gate decision is recorded, render a one-page publication gate pack via `/wx-diagram gate-pack {{project}}` (draw.io engine; degrades to .drawio XML if CLI missing) and attach it next to the gate review file.
