---
name: gate2
description: Conducts the formal Phase 2 Gate Review scoring Concept Diversity, Evaluation Rigor (VDI 2225), Selected Concept Quality (Rt ≥0.70), Function Coverage, Feasibility, and Documentation (weighted, target ≥3.5/4.0) before authorizing Phase 3. Requires explicit CEO approval — never auto-proceeds. Triggers on: "gate 2", "G2", "phase 2 gate", "concept gate", "xét duyệt cổng 2", "nghiệm thu khái niệm".
---
Conduct the formal Phase 2 Gate Review before proceeding to Phase 3 Embodiment Design.

Usage: /gate2 [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Provide references to Phase 2 artifacts:
     - Problem Abstraction (P16)
     - Function Structure (P17)
     - Working Principles Search (P52, if done)
     - Morphological Matrix (P18)
     - Concept Sketch Review (P19)
     - Selection Chart (P20)
     - VDI 2225 Evaluation (P21)
     - Reuse Analysis (P50, if done)
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - All Phase 2 documents in `1_Projects/{{project}}/Phase2-Concept/`
3. Execute the gate review workflow:
   - Score 6 criteria independently (0-4 each):
     A. Concept Diversity (15%) -- >=3 different concepts evaluated?
     B. Evaluation Rigor (25%) -- VDI 2225 criteria independent, weights justified, sensitivity done?
     C. Selected Concept Quality (25%) -- Rt >=0.70, no unresolved weak spots?
     D. Function Coverage (15%) -- all sub-functions have working principle assigned?
     E. Feasibility Check (15%) -- local content >=40% achievable, cost in range?
     F. Documentation (5%) -- rationale documented, fallback concept identified?
   - Calculate weighted total: (0.15*A + 0.25*B + 0.25*C + 0.15*D + 0.15*E + 0.05*F)
   - Target: >=3.5/4.0
   - Present gate decision: A (Approve) / B (Revise) / C (Pause) / D (Cancel)
   - WAIT for explicit user response
4. Save output to:
   `1_Projects/{{project}}/Phase2-Concept/{{PROJECT_NAME}}_Phase2_Gate_Review_v1.0.md`

CRITICAL: This is a NEVER-AUTOMATE decision. Present scores and WAIT. Do NOT auto-proceed to Phase 3.
BLOCKER: Any criterion scoring 0 -> REVISE regardless of total.
BLOCKER: Unresolved safety/reliability weak spot -> cannot APPROVE.
