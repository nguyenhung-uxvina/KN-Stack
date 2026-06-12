---
name: gate3
description: Conducts the formal Phase 3 Gate Review scoring Requirements Traceability, Interface Completeness, Layout Feasibility, BOM Completeness, Local Content (≥60%), DfX Review, Power/Thermal Budget, and Risk Update (weighted, target ≥3.0/4.0) before authorizing Phase 4. Any subsystem with TRL <5 and no prototype test plan is an automatic FAIL. Triggers on: "gate 3", "G3", "phase 3 gate", "embodiment gate", "xét duyệt cổng 3", "nghiệm thu thiết kế hiện thân".
---
Conduct the formal Phase 3 Gate Review before proceeding to Phase 4 Detail Design.

Usage: /gate3 [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Provide references to Phase 3 artifacts (system architecture, ICD, layout, BOM, DfX, power budget)
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - All Phase 3 documents in `1_Projects/{{project}}/Phase3-Embodiment/`
   - Phase 1 requirements list (for traceability check)
3. Execute the gate review workflow:
   - Score 8 criteria independently (0-4 each):
     A. Requirements Traceability (15%) -- every D-requirement maps to >=1 subsystem?
     B. Interface Completeness (15%) -- all subsystem interfaces documented in ICD? No TBDs in critical interfaces?
     C. Layout Feasibility (15%) -- spatial arrangement fits envelope? Assembly sequence defined?
     D. BOM Completeness (10%) -- all components listed? Cost rollup vs budget?
     E. Local Content (10%) -- >=60% by value? Import items flagged?
     F. DfX Review (10%) -- DfM, DfA, DfT, DfMaint all assessed? No category scored <=1?
     G. Power/Thermal Budget (10%) -- >=20% margin? Thermal dissipation manageable?
     H. Risk Update (15%) -- Phase 2 risks updated? Manufacturing + supply chain risks added? Physical prototype plan defined?
   - Calculate weighted total
   - Target: >=3.0/4.0
   - Present gate decision: PASS / CONDITIONAL PASS / FAIL
   - WAIT for explicit user response
4. Save output to:
   `1_Projects/{{project}}/Phase3-Embodiment/{{PROJECT_NAME}}_Phase3_Gate_Review_v1.0.md`

CRITICAL: This is a NEVER-AUTOMATE decision. Present scores and WAIT.
BLOCKER: Any subsystem with TRL <5 and no prototype test plan -> FAIL.
BLOCKER: Cost overrun >20% of target with no mitigation plan -> CONDITIONAL at best.
BLOCKER: Local content <50% -> FAIL for Vietnamese defense programs.
FLAG: Physical prototype not yet built -> note as risk. dP/dt = 0 is a warning.
