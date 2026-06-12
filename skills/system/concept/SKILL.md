---
name: concept
description: Runs Pahl-Beitz Phase 2 Conceptual Design, producing a refined Function Structure, Working Principles Search, Morphological Matrix, and VDI 2225 concept evaluation to select the winning concept variant. Use after Phase 1 Gate is passed and requirements are locked. Triggers on: "phase 2", "conceptual design", "morphological matrix", "working principles", "thiết kế khái niệm", "ma trận hình thái", "giai đoạn 2".
---
Run Phase 2 Conceptual Design for a project following Pahl-Beitz systematic design.

Usage: /concept [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project? (project code or name)
   - Is Phase 1 Task Clarification complete? (requirements list, function structure)

2. Read existing project artifacts:
   - `1_Projects/{{project}}/Status.md` — verify Phase 1 done
   - Phase 1 documents (requirements, function structure, stakeholder analysis)
   - Any existing Phase 2 documents (avoid duplicates)

3. Phase 2 Conceptual Design produces these documents (in order):

   **Doc: Function Structure v2.0** (refine from Phase 1 preliminary)
   - Decompose to L1 → L2 → L3 sub-functions
   - 6-flow analysis: Direct flows (D-C-T: Drive, Control, Transmit) + Enabling flows (E-M-S: Energy, Material, Signal)
   - Latency/timing budget if applicable
   - Traceability: each sub-function → parent requirement(s)

   **Doc: Working Principles Search** (or use /wp output if already done)
   - For each key sub-function: 3-5 working principles
   - Each principle: Physical Effect | TRL | Cost | Local Content | Advantages | Disadvantages
   - ≥3 different source types (catalogs, patents, competitors, cross-domain)

   **Doc: Morphological Matrix**
   - Rows: key sub-functions (typically 10-15)
   - Columns: working principles for each (3-5 per row)
   - Combine into 2-4 concept variants
   - Each variant: describe the combination rationale

   **Doc: Concept Evaluation (VDI 2225)**
   - Define 8-12 evaluation criteria from requirements (weighted)
   - Score each variant 0-4 on each criterion
   - Calculate weighted technical value (Σ wi × si / 4)
   - Sensitivity analysis: test top-3 criteria weight changes (±20%)
   - Risk register: top 5 risks per concept
   - Present ranking with recommendation

   **Doc: Phase 2 Gate Review**
   - 8 gate criteria (all must PASS):
     1. Requirements coverage (every D-requirement addressed)
     2. Function completeness (no orphan sub-functions)
     3. ≥2 viable concepts evaluated
     4. VDI 2225 evaluation completed with sensitivity
     5. Cost estimate within target (±15%)
     6. Local content target achievable
     7. TRL assessment realistic
     8. Risk register with mitigations
   - Gate decision: PASS / CONDITIONAL / FAIL

4. For each document:
   - Draft and present to user (HITL checkpoint)
   - Wait for approval before proceeding
   - Save to `1_Projects/{{project}}/Phase2-Concept/{{NNN}}_{{DocName}}_v{{X}}.0.md`

5. After gate review, update Status.md with results.

6. Suggest next step: /embody (Phase 3) if gate passed, or remediation if conditional/fail.

RULES:
- Phase 1 MUST be complete before Phase 2 — check Status.md
- ≥2 concept variants required — never evaluate a single concept alone
- VDI 2225 scores must include sensitivity analysis — single-point scores are fragile
- Solution-neutral sub-functions, solution-specific working principles
- COD: Offload (AI generates, CEO decides on concept selection)
- Do NOT auto-select winning concept — present scores and WAIT for CEO decision
- If /wp was already run, reuse those results instead of regenerating
- Number documents continuing from Phase 1 sequence
