---
name: helix-p2-preflight
description: "Block 0 of Phase 2 pipeline — verify Phase 1 inputs, check abstraction quality (5-step), validate function structure (11 P&B guidelines), classify design type (Original/Adaptive/Variant). Can run standalone or as part of /helix-concept-generate pipeline. Triggers on: 'preflight', 'Phase 2 input check', 'verify Phase 1', 'design type'."
---

# Block 0: Pre-Flight — Input Verification & Quality Gate

> **P&B:** 6.1–6.3.3 | **Pipeline:** helix-concept-generate → Block B0
> **Input:** Phase 1 deliverables | **Output:** `B0_Preflight_Report.md`
> **Galaxy:** [[Variation vs Simplification]], [[VDI 2221 Evolution]]

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Verify all Phase 1 deliverables exist | Change scope or requirements |
| Check abstraction quality (5-step) | Re-do Phase 1 work |
| Validate function structure (11 guidelines) | Propose new sub-functions |
| Classify design type (O/A/V) | Skip classification even if "obvious" |
| Flag missing inputs clearly | Proceed with missing inputs |

**Multi-Agent Mode:** NO — simple validation, single agent sufficient
**CEO Checkpoint:** Block boundary only (output: B0_Preflight_Report.md)

## Standalone Usage
```
/helix-p2-preflight VN-XUONG-UUV
```

## Input Requirements
Read from `1_Projects/{{project}}/Phase1-Task/`:
- `Requirements_List_v1.md` — D/W requirements
- `Function_Structure.md` — sub-functions
- `Essential_Problem.md` — core problem
- ICD v1 — domain allocations

## Workflow

### Step 0.1: Verify Phase 1 Deliverables Exist

```
PRE-FLIGHT CHECKLIST — {{project_id}}
Date: {{today}}

□ Requirements_List_v1.md exists — D/W classification complete
□ Function_Structure.md exists — sub-functions identified  
□ Essential_Problem.md exists — CEO-approved
□ ICD v1 exists — domain allocations defined
□ Gate 1 PASSED (date: ______)

VDI 2206 SYSTEM ARCHITECTURE CHECK (mechatronic products only):
□ Product mechatronic classification: [YES/NO/SKIP]
□ If YES: System-Arch/ folder exists with:
  □ SA_System_Architecture.md — block diagram + domain allocation
  □ SA_Domain_Budgets.md — weight/power/cost per domain
  □ SA_VV_Plan.md — verification matrix
  □ ICD v1 updated with interface contracts
□ If NO/SKIP: Single-domain confirmed, reason documented

MISSING ITEMS: [list or "NONE"]
STATUS: [GO / NO-GO — specify what's missing]
```

**REJECT IF:** Function structure unavailable OR requirements not D/W classified OR essential problem not CEO-approved. For mechatronic products: ALSO REJECT IF system architecture not completed — suggest running `/helix-system-arch {{project}}` first. Report which deliverable is missing.

### Step 0.2: Abstraction Quality Check (P&B 6.2 — 5-Step)

Verify essential problem passes all 5 steps:

| Step | Check | Pass? |
|------|-------|-------|
| 1. Eliminate personal preferences | No brand names, no specific suppliers | □ |
| 2. Omit non-functional requirements | Problem focused on WHAT, not HOW | □ |
| 3. Transform quantitative → qualitative | Core function in general terms | □ |
| 4. Generalize results | Not locked to one solution class | □ |
| 5. Formulate solution-neutral | ≥3 different solutions could satisfy | □ |

**Solution-Neutral Test:** List 3 fundamentally different solution approaches. If only 1 → problem is solution-biased → return to Phase 1.

### Step 0.3: Function Structure Quality Check (P&B 6.3.3 — 11 Guidelines)

| # | Guideline | Check |
|---|-----------|-------|
| 1 | Depends on problem interpretation — documented? | □ |
| 2 | Detail matches task novelty + experience | □ |
| 3 | Completeness appropriate for design type | □ |
| 4 | Enables solution search WITHOUT premature bias | □ |
| 5 | Representation form justified | □ |
| 6 | Physical structure alignment (modular) | □ |
| 7 | Can be VARIED during Phase 2 (not frozen) | □ |
| 8 | Subfunctions & relationships clear | □ |
| 9 | Task-specific functions where needed | □ |
| 10 | Generally-valid functions where possible | □ |
| 11 | Each subfunction equally important | □ |

**3-Flow Verification:** Every SF accounts for Energy, Material, Signal.
**6-Flow Extension:** Also Data, Computation, Trust (for AI/software products).

**If ≥3 guidelines FAIL:** Return to Phase 1.

### Step 0.4: Design Type Classification

> **Galaxy:** [[Variation vs Simplification]]

| Type | Criterion | Decomposition | Time Budget |
|------|----------|--------------|-------------|
| **Original** | New problem, no precedent | Deep everywhere | 100% |
| **Adaptive** | Known problem, novel subsystem | Deep on novel SFs only | 60-70% |
| **Variant** | Known product, parameter change | Minimal | 30-40% |

**CEO DECIDES** design type. This cascades through ALL subsequent blocks.

### Step 0.4b: Contextual Factors Check (VDI 2221 Blatt 2)

Verify contextual factors from Phase 1 B0 are still valid. If project context has changed (new customer requirements, budget change, timeline shift), update:

```
CONTEXTUAL FACTORS UPDATE — {{project_id}} Phase 2
Date: {{today}}

Changes since Phase 1:
  □ Customer requirements changed? [YES: describe / NO]
  □ Budget/timeline changed? [YES: describe / NO]
  □ Team composition changed? [YES: describe / NO]
  □ Manufacturing constraints changed? [YES: describe / NO]

If any YES → recommend pipeline mode adjustment to CEO.
If all NO → confirm Phase 1 contextual factors still valid.
```

> **VDI 2221:2019:** Design process is "not a purely sequential, predictable or repeatable process." Context evolves — check it at each phase boundary.

### Step 0.4c: Model Readiness Check (VDI 2206 Blue Strand)

> **VDI 2206:2021 Blue Strand:** Concept evaluation requires models. Verify what's available.

```
MODEL READINESS — {{project_id}} Phase 2
Date: {{today}}

AVAILABLE:
  □ Calculation tools for firming up (CRUMPLE-S)?
  □ CAD for rough sketches (hand drawings acceptable)?
  □ Simulation for critical physics?
  □ Reference data from similar WX products?
  □ SA_Model_Inventory.md (from /helix-system-arch)? [YES / NO / N/A]

MISSING (may limit evaluation quality):
  [list tools/models needed but unavailable]
```

### Step 0.5: ICDM Extension (if --icdm active)

Check pipeline state for ICDM flag. If active:
- Overlay ICDM innovation requirements onto checklist
- Add collaboration gate criteria
- Generate ICDM compliance matrix

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/B0_Preflight_Report.md`:

```markdown
# B0 Pre-Flight Report — {{project}}
Date: {{today}}

## Deliverable Verification: [GO / NO-GO]
[checklist results]

## Abstraction Quality: [PASS / FAIL — {{N}}/5 steps]
[5-step results + solution-neutral test]

## Function Structure Quality: [PASS / FAIL — {{N}}/11 guidelines]
[11 guidelines results + flow verification]

## Design Type: [Original / Adaptive / Variant]
CEO Decision: _______________
Rationale: _______________

## Recommendations for Block BA
[specific guidance based on design type and findings]
```

## CEO Checkpoint

```
═══ BLOCK B0 PRE-FLIGHT COMPLETE ═══
Design Type: [Original / Adaptive / Variant]
Input Quality: [GO / NO-GO]
Guidelines: {{N}}/11 pass

CEO: 
(1) ✅ Approve → tiếp tục Block BA (Problem Framing)
(2) 🔄 Chạy lại với điều chỉnh
(3) ⏸️ Dừng — cần fix Phase 1 trước
```

## COD
- Checklist verification: Offload (O1)
- Design type decision: **Core (C)** — CEO judgment
- Abstraction re-formulation: **Core (C)** — if needed
