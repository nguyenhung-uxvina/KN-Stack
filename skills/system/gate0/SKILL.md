Conduct the formal Phase 0 Gate Review before proceeding to Phase 1 Task Clarification.

Usage: /gate0 [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project is this for? (VN-XXX-XXX code or product name)
   - Provide references to Phase 0 artifacts:
     - Situation Analysis (P09)
     - Idea Generation (P10)
     - Product Proposal (P11)
     - ODI Report (P28, if completed)
2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - `1_Projects/{{project}}/_Project_Brief.md`
   - Any Phase 0 documents in the project folder
3. Execute the gate review workflow:
   - Score 5 criteria independently (0-4 each):
     A. Strategic Fit (25%) -- Workshop X alignment, competitive advantage, R2 loop contribution?
     B. Customer Insight (25%) -- target segment identified, unmet needs documented?
     C. Scope Clarity (20%) -- primary function defined, top 3 targets quantified, cost target set?
     D. Feasibility (20%) -- TRL >=4, local content >=40% achievable, timeline realistic?
     E. Risk Awareness (10%) -- risks identified, kill condition defined?
   - Calculate weighted total: (0.25*A + 0.25*B + 0.20*C + 0.20*D + 0.10*E)
   - Target: >=3.0/4.0
   - Present gate decision: A (Approve) / B (Revise) / C (Pause) / D (Cancel)
   - WAIT for explicit user response
4. Save output to:
   `1_Projects/{{project}}/Phase1-Task/{{PROJECT_NAME}}_Phase0_Gate_Review_v1.0.md`

CRITICAL: This is a NEVER-AUTOMATE decision. Present scores and WAIT. Do NOT auto-proceed to Phase 1.
BLOCKER: Any criterion scoring 0 -> REVISE regardless of total.
BLOCKER: Controlled technology (ITAR/EAR/dual-use) without clearance -> must PAUSE.
NOTE: ODI not done is acceptable -- flag as risk but don't auto-reject.
