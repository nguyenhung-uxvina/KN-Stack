---
name: helix-p1-validate
description: "Block B of Phase 1 pipeline — CEO performs D/W classification (Core, non-delegable), gap analysis, failure-derived requirements, SPOF check, IFR statement, sacred constraints. P&B 5.2-5.3. Can run standalone. Triggers on: 'classify requirements', 'D/W classification', 'validate requirements', 'failure analysis', 'sacred constraints'."
---

# Block B: Validate — D/W Classification + Gap Analysis + Failure Requirements

> **P&B:** 5.2-5.3 | **Pipeline:** helix-task-clarify → Block BB
> **Input:** `BA_Requirements_Draft.md` | **Output:** `BB_Requirements_List_v1.md`, `BB_Failure_Derived_Reqs.md`
> **Galaxy:** [[Phán đoán không thể uỷ thác cho AI]]

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Present requirements for CEO D/W classification | Override or pre-fill CEO's D/W choices |
| Run gap analysis against 17 categories | Abstract the problem (= BC) |
| Generate failure-derived requirements (FMEA) | Decompose into sub-functions (= BD) |
| Check SPOF (Single Point of Failure) | Evaluate concepts or search WPs (= Phase 2) |
| Isolate solution ideas → Solution_Ideas_Log | Skip SPOF check for defense products |

**Multi-Agent Mode:** NO — CEO IS the block for D/W classification. AI assists with FMEA and gap analysis.
**CEO Checkpoint:** D/W classification = Core, non-delegable. CEO classifies every requirement.

## Standalone Usage
```
/helix-p1-validate VN-XUONG-UUV
```

## Input Requirements
- `BA_Requirements_Draft.md` — AI-generated requirements with D/W = [TBD]
- `B0_Preflight_Report.md` — stakeholders for conflict checking

## Workflow

### Step B1: D/W Classification (Core — NON-DELEGABLE)

> **Galaxy:** [[Phán đoán không thể uỷ thác cho AI]]
> **P&B 5.2:** "D/W classification is a JUDGMENT call — only the user knows what customer truly demands."

Present requirements to CEO. CEO marks each:

```
CLASSIFICATION TEST (per requirement):
  "If this requirement is NOT met, is the product DEAD (unusable for its mission)?"
  YES → D (Demand)
  NO  → W (Wish) → then grade:
    W+ (major)  — thiếu = giảm giá trị đáng kể (VDI 2225 weight 3-4)
    W  (medium) — thiếu = giảm sức cạnh tranh (VDI 2225 weight 2)
    W- (minor)  — thiếu = vẫn chấp nhận được (VDI 2225 weight 1)
```

**AI assists by:**
- Highlighting safety requirements → likely D
- Highlighting nice-to-haves → likely W
- Flagging conflicts between requirements
- **AI NEVER decides D vs W**

### Step B2: Gap Analysis

CEO reviews classified list for gaps:

```
GAP ANALYSIS — {{project_id}}

CHECKLIST:
  □ All 17 P&B categories have ≥1 requirement?
  □ All safety-critical functions have a requirement?
  □ Every D-requirement has a quantified value?
  □ Every requirement has a verification method (I/M/T/A)?
  □ Implicit requirements captured? (safety, rain, corrosion)
  □ Lifecycle stages covered? (transport, install, operate, maintain, dispose)
  □ Stakeholder needs all addressed?

GAPS FOUND:
| Gap | Category | Description | Action | Owner |
|-----|----------|------------|--------|-------|
```

### Step B3: IFR Statement + Sacred Constraints (CEO Defines)

```
IFR (Ideal Final Result) — {{project_id}}

"The ideal {{product}} delivers {{core function}} with ZERO {{eliminated resource/limitation}},
using ZERO {{eliminated dependency}}, while maintaining {{key performance}} under
{{operational conditions}}."

GEOMETRY CLASSIFICATION (CEO Core — defense data control):
| Field | Value | Note |
|-------|-------|------|
| Geometry Classification | [MẬT / HẠN-CHẾ / THƯỜNG] | Governs every CAD/geometry tool's egress rule (default MẬT for any defense product) |

  → This is the SINGLE upstream source the CAD trio reads: [[helix-cad-bridge]],
    [[helix-cad-ingest]], [[helix-cad-roundtrip]] all gate their network/cloud-OCR
    behaviour on this label. MẬT = offline-only, no cloud OCR/vision ever.
  → Carried forward verbatim into 003_IFR_Sacred_Constraints_v1.0.md (helix-p1-compile)
    so the geometry tools can read it at any phase.

SACRED CONSTRAINTS (non-negotiable physics/operations/safety):
| # | Constraint | Basis | Type | Status |
|---|-----------|-------|------|--------|
| SC-1 | {{constraint}} | {{physics/ops/safety reason}} | [Physics/Ops/Safety/Regulatory] | [Proven/Assumed] |

AVAILABLE RESOURCES (TRIZ — what's already in the system):
| Resource | Present? | Currently Used For |
|----------|----------|-------------------|
```

### Step B4: Failure-Derived Requirements (P&B 5.4 + MIL-STD-882E)

```
FAILURE MODE SCAN — {{project_id}}

For each core function, ask: "How can this FAIL?"

| Function | Failure Mode | Consequence | Severity | Req Generated | Field Evidence |
|----------|-------------|------------|----------|--------------|----------------|

SPOF CHECK (Single Point of Failure):
| Component | If It Fails | Redundancy? | SPOF? | Mitigated By |
|-----------|------------|------------|-------|-------------|

NEW REQUIREMENTS FROM FAILURE ANALYSIS:
| Req-ID | Derived From | Requirement | D/W |
|--------|-------------|-------------|-----|
```

### Step B5: Requirement Priority Tagging (P&B 5.3)

Tag which requirements must be resolved EARLIEST:

| Priority Type | Definition | Tag |
|--------------|-----------|-----|
| Concept-defining | Determines which concept family | [CONCEPT] |
| Structure-influencing | Determines subsystem division | [STRUCTURE] |
| Embodiment-determining | Determines shape/size/config | [EMBODY] |
| Late-bindable | Can wait until Detail Design | [LATE] |

### Step B5b: Solution-Idea Isolation (P&B 5.4)

Scan requirements for embedded solution ideas. Extract and park them:

```
SOLUTION IDEAS LOG — {{project_id}}
(Ideas captured during requirements work — feed Phase 2 working principle search)

| # | Solution Idea | Triggered By Req | Phase 2 Relevance |
|---|--------------|-----------------|-------------------|
| S1 | [idea] | R-xxx | [high/med/low] |

RULE: If a requirement contains HOW (not just WHAT), split it:
  - Requirement stays as performance spec
  - Solution idea goes to this log
```

### Step B5c: Binding Yet Provisional Tagging (P&B 5.3.1)

Tag each requirement with resolution timing:

```
TIMING TAGS:
  [CONCEPT]    — must know before Phase 2 (determines concept family)
  [STRUCTURE]  — must know before Phase 3 (determines subsystem division)
  [EMBODY]     — must know before Phase 4 (determines shape/size/config)
  [LATE]       — can wait until Detail Design (use [TBD] placeholder)

NOTE: Requirements are BINDING (commitments for current phase) but PROVISIONAL
      (must update as knowledge grows). Mark [LATE] items with planned resolution date.
```

### Step B6: Compile Validated Requirements List

```
REQUIREMENTS LIST — {{project_id}} — v1.0
Date: {{today}}
Status: CEO VALIDATED — D/W classified
Total: {{N}} ({{D}}D / {{W}}W), {{pct}}% quantified, {{cat}}/16 categories

[full table with D/W filled in, gaps closed, failure-derived added]
```

### ICDM Extension (if --icdm active)
- Innovation-oriented gap analysis (missing innovation enablers)
- TRIZ resource inventory integrated into available resources

## Output

Save to `1_Projects/{{project}}/Phase1-Task/`:
- `BB_Requirements_List_v1.md` — validated with D/W + gaps closed
- `BB_Failure_Derived_Reqs.md` — failure analysis + SPOF check

## CEO Checkpoint

```
═══ BLOCK BB VALIDATION COMPLETE ═══
Requirements: {{N}} total ({{D}}D / {{W}}W)
Quantified: {{pct}}%
Categories: {{N}}/17
Sacred Constraints: {{N}} defined
Failure-derived: {{N}} new requirements added
SPOFs: {{N}} identified, {{M}} mitigated

CEO:
(1) ✅ Approve → tiếp tục Block BC (Abstraction)
(2) ➕ Thêm requirements từ field experience
(3) 🔄 Reclassify một số D/W
(4) ⏸️ Dừng — cần stakeholder interview
```

## COD
- Presenting requirements for classification: Offload (O1)
- **D/W classification: Core (C) — NEVER delegated to AI**
- Gap analysis checklist: Offload (O2) — AI flags gaps
- **IFR statement: Core (C) — CEO defines**
- **Sacred constraints: Core (C) — CEO decides**
- **Geometry Classification (MẬT/HẠN-CHẾ/THƯỜNG): Core (C) — defense data control; the upstream label the CAD trio reads**
- Failure mode scan: Offload (O2) — AI drafts, CEO validates severity
- SPOF identification: Offload (O2) — AI flags, CEO validates
