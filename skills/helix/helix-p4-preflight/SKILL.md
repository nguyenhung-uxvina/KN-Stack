---
name: helix-p4-preflight
description: "Block 0 of Phase 4 pipeline — verify Phase 3 complete + Gate 3 passed, lock requirements freeze (VDI 2221:2019 mandate), identify detail-determining components (critical dims/surfaces/welds/electrical), assess P03/P04 readiness, detect ACH lifecycle need. P&B 9.1. Can run standalone. Triggers on: 'Phase 4 preflight', 'detail design inputs', 'requirements freeze'."
---

# Block 0: Pre-Flight — Phase 3 Verification + Requirements Freeze

> **P&B:** Chapter 9 (Detail Design § 9.1) | **Pipeline:** helix-detail-finalize → Block B0
> **Input:** Phase 3 deliverables + Gate 3 result | **Output:** `B0_Preflight_Report.md`
> **VDI 2221:2019 Blatt 1:** Requirements MUST be frozen before detail design — no further changes without formal change request.

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|----|----|
| Verify Phase 3 complete + Gate 3 passed | Specify critical GD&T (= BA, CEO Core) |
| Freeze requirements list (VDI 2221:2019) | Generate drawings (= BA) |
| Identify detail-determining components | Compile final BOM (= BB) |
| P03/P04 readiness check | Inspection plan (= BC) |
| ACH detection (for BE lifecycle gen) | Workshop master review (= BE, CEO Core) |

**Multi-Agent Mode:** NO — verification + classification, single agent sufficient.
**CEO Checkpoint:** Confirm requirements frozen + detail-determining component list before BA.

## Workflow

### Step 0.1: Verify Phase 3 Complete

```
□ B0_Preflight_Report.md (Phase 3) exists
□ BA_Layout.md — preliminary layout CEO-approved
□ BB_DfX_Review.md — all FAIL items resolved
□ BC_Integration.md — ICD v3 frozen
□ BD_BOM_Draft.md — draft BOM exists
□ BE_Phase3_Compile.md — Phase 3 deliverables compiled
□ Gate 3 PASSED (date: ______)
```

If any FAIL → STOP, return to `helix-embody-realize` (P3).

### Step 0.2: Requirements Freeze Check (VDI 2221:2019 Blatt 1)

```
REQUIREMENTS FREEZE — {{project}}
Date: {{today}}

□ Requirements_Delta_Log.md reviewed — all deltas CEO-approved? [list pending]
□ Requirements_List version v{{X}} (should be ≥ v1.1 if deltas occurred)
□ No [TBD] in D-requirements? [list TBDs]
□ All [P4]-tagged requirements have values? [list missing]
□ Test methods defined for ALL D-requirements? [count]

STATUS: [FROZEN / PENDING — {{N}} items to resolve]
```

**If PENDING → BLOCK P4 pipeline. CEO must resolve before BA.**

### Step 0.3: Identify Detail-Determining Components (P&B § 9.1)

```
DETAIL-DETERMINING COMPONENTS — {{project}}

CRITICAL DIMENSIONS (GD&T mandatory — datum/tolerance stack):
> If a `cad_extract.json` geometry-of-record exists for the part, pre-fill this table from its critical-dim rows (via [[helix-cad-ingest]]) for CEO confirmation, rather than listing them from scratch.
| Component | Why critical | Datum surface | Tolerance class |
|----|----|----|----|

CRITICAL SURFACES (functional finish):
| Component | Function | Finish spec | Inspection method |
|----|----|----|----|

CRITICAL WELDS (defense-grade):
| Joint | Process | Filler | NDT level (AWS/TCVN) |
|----|----|----|----|

CRITICAL ELECTRICAL (PCB + harness):
| Item | Spec | Pinout reference | Layout approval |
|----|----|----|----|
```

These items will require **CEO Core specification in BA** — AI cannot determine.

### Step 0.4: P03 / P04 Readiness Check

```
P03 DOC QUALITY readiness (target before BC):
  □ Quantification rate ≥80% in Phase 3 docs?
  □ Parameter citation 100% traceable?
  □ Safety tags [SAFETY-CRITICAL] applied?
  □ No vague terms (adequate/sufficient/good)?

P04 TCVN COMPLIANCE readiness (target before BE):
  □ Primary TCVN standard identified + cited?
  □ Compliance matrix structure ready?
  □ Top procurement-blocking gaps known?
  □ Safety-critical sections flagged?

Score: P03 __/4   P04 __/4  → flag gaps for BC/BE.
```

### Step 0.5: ACH Detection

```
Read FORGE/ACH_Assessment_v*.md or forge-shift output:
  ACH Status: [YES → BE generates Operational_Update_Lifecycle.md]
              [NO → BE skips ACH lifecycle block]
```

### Step 0.6: Variant Subfolder Resolution

If variant specified → `Phase4-Detail/<variant>/` + file prefix `{{PROJECT}}_{{VARIANT}}_`.

## Output

Save to `1_Projects/{{project}}/Phase4-Detail/{{variant}}/B0_Preflight_Report.md`.

Append summary to `_pipeline_state.md` Block Ledger.

## CEO Checkpoint

```
═══ BLOCK B0 PRE-FLIGHT COMPLETE ═══
Phase 3 + Gate 3: {{PASS / FAIL items}}
Requirements: [FROZEN / PENDING — N items]
Detail-determining: {{N}} dims + {{N}} surfaces + {{N}} welds + {{N}} electrical
P03/P04 readiness: {{score}}/8
ACH lifecycle: [YES / NO]

CEO:
(1) ✅ Approve → tiếp tục Block BA (Drawing)
(2) 🔄 Resolve pending requirements first
(3) ⏸️ Dừng — Phase 3 incomplete, return to helix-embody-realize
```

## COD

- Phase 3 verification: Offload (O1)
- Requirements freeze audit: Offload (O2) — AI lists, CEO approves freeze
- Detail-determining identification: Offload (O2) — AI proposes from drawings, CEO confirms
- cad_extract critical-dim pre-fill: Offload (O1) — CEO confirms geometry-of-record rows
- ACH detection: Offload (O1)
- **Requirements freeze decision: Core (C)** — CEO accountable for "no more changes"
