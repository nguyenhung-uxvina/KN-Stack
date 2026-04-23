---
name: helix-detail-finalize
description: Run Pahl-Beitz Phase 4 Detail Design to produce manufacturing-ready package with drawings, final BOM, inspection checklist, and assembly instructions. This skill should be used when the user asks for "detail design", "manufacturing drawings", "production ready", "hoan thien che tao", "Phase 4", or needs to finalize a design for workshop fabrication.
---

# Helix Detail Finalize — Phase 4 Pahl-Beitz Detail Design

> **VDI 2221:2019:** Blatt 1 — requirements freeze before detail design

Produce the complete manufacturing package: final CAD with GD&T, manufacturing drawings, final BOM, inspection checklist, and assembly instructions. Workshop master review gate included.

## When to Use

- After Phase 3 Embodiment Design is complete and Gate 3 passed
- User asks "detail design", "manufacturing drawings", "production ready"
- When preparing handoff to workshop for fabrication
- Final phase before physical prototype build

## Workflow

### Step 1: Gather Inputs

Read Phase 3 deliverables:
- `1_Projects/{{project}}/Phase3-Embodiment/DfX_Review.md` — all items resolved
- `1_Projects/{{project}}/Phase3-Embodiment/BOM_Draft.md` — draft BOM
- `1_Projects/{{project}}/Phase3-Embodiment/ICD_v3.md` — frozen interfaces
- `1_Projects/{{project}}/Phase3-Embodiment/Design_Decisions.md` — trade-offs
- `1_Projects/{{project}}/Phase1-Task/Requirements_List_v1.md` — for traceability

Verify prerequisites:
- All DfX FAIL items resolved? [YES/NO]
- ICD v3 frozen? [YES/NO]
- BOM draft complete? [YES/NO]
- If any NO → return to helix-embody-realize

### Step 1b: Requirements Freeze Confirmation (VDI 2221:2019)

> **VDI 2221:2019:** Requirements co-evolve with the solution through Phase 2 and Phase 3. By Phase 4, the requirements list MUST be frozen — no further changes without formal change request.

```
REQUIREMENTS FREEZE CHECK — {{project}}
Date: {{today}}

□ Requirements_Delta_Log.md exists? [YES / NO]
  If YES: All deltas CEO-approved? [YES / NO — list pending]
□ Requirements_List version: v{{X}} (should be ≥ v1.1 if deltas exist)
□ No [TBD] values remaining in D-requirements? [PASS / FAIL — list TBDs]
□ All [P4]-tagged requirements have values now? [PASS / FAIL]

STATUS: [REQUIREMENTS FROZEN / PENDING — {{N}} items to resolve]
```

If PENDING → CEO must resolve before detail design proceeds.

> **P&B Reference + VDI 2221:2019 Blatt 1**

### Step 2: Human Specifies Critical Dimensions (Core)

User provides:
- GD&T on critical dimensions (datum surfaces, tolerances)
- Surface finish requirements on functional surfaces
- Weld specifications (type, size, inspection level)
- Cable/connector pinout definitions
- PCB final layout approval

AI cannot determine which dimensions are critical — this requires manufacturing experience.

### Step 3: AI Completes CAD Package

From human specs, AI generates:
- 3D model completion (manufacturing features: fillets, chamfers, draft angles)
- 2D manufacturing drawings (per ISO 128 / TCVN drawing standards)
- Exploded views for assembly reference
- PCB Gerber files preparation checklist

### Step 4: Final DfX Verification

Re-run DfX checks on final geometry:

```
FINAL DfX VERIFICATION — {{project_id}}
Date: {{today}}
CAD revision: [rev]

| Category | Items Checked | PASS | WARN | FAIL |
|----------|-------------|------|------|------|
| DfM | [n] | [n] | [n] | [n] |
| DfA | [n] | [n] | [n] | [n] |
| DfR | [n] | [n] | [n] | [n] |
| DfT | [n] | [n] | [n] | [n] |
| DfU | [n] | [n] | [n] | [n] |

GATE: [PASS — proceed / FAIL — iterate]
Any remaining WARN items: [list with accepted risk rationale]
```

### Step 5: Compile Final BOM

```
FINAL BOM — {{project_id}}
Date: {{today}}
Revision: v1.0 (production)

MECHANICAL:
| Item | Part No. | Description | Material | Qty | Dims (mm) | Process | Vendor | Cost (VND) | Lead (d) |
|------|----------|-------------|----------|-----|-----------|---------|--------|-----------|----------|
| M-01 | [PN] | [desc] | [mat] | [n] | [LxWxH] | [CNC/weld/bend] | [VN vendor] | [cost] | [days] |
| M-02 | ... | ... | ... | ... | ... | ... | ... | ... | ... |

ELECTRICAL:
| Item | Part No. | Description | Package | Qty | Vendor | Cost (VND) | Lead (d) |
|------|----------|-------------|---------|-----|--------|-----------|----------|
| E-01 | [PN] | [desc] | [pkg] | [n] | [vendor] | [cost] | [days] |
| E-02 | ... | ... | ... | ... | ... | ... | ... |

FASTENERS & HARDWARE:
| Item | Spec | Qty | Cost (VND) |
|------|------|-----|-----------|
| F-01 | M5x16 SS304 | [n] | [cost] |
| ... | ... | ... | ... |

PURCHASED ITEMS (COTS):
| Item | Description | Supplier | Qty | Cost (VND) | Lead (d) |
|------|-------------|----------|-----|-----------|----------|
| P-01 | [desc] | [supplier] | [n] | [cost] | [days] |
| ... | ... | ... | ... | ... | ... |

COST SUMMARY:
| Category | Cost (VND) | % Total |
|----------|-----------|---------|
| Mechanical | [sum] | [%] |
| Electrical | [sum] | [%] |
| Fasteners | [sum] | [%] |
| COTS | [sum] | [%] |
| Assembly labor (est.) | [sum] | [%] |
| TOTAL | [sum] | 100% |

LONG-LEAD PROCUREMENT (order immediately):
| Item | Lead Time | Order By | Status |
|------|-----------|---------|--------|
| [item] | [days] | [date] | [ordered/pending] |
```

### Step 6: Generate Inspection Checklist

```
INSPECTION CHECKLIST — {{project_id}}
Date: {{today}}

INCOMING MATERIAL INSPECTION:
| Check | Method | Accept Criteria | Freq |
|-------|--------|----------------|------|
| Material cert (Al 5083) | Certificate review | Match spec | 100% |
| Dimensional check (CNC parts) | Caliper/CMM | Per drawing +/- | 100% |
| PCB visual | Microscope | IPC-A-610 Class 2 | 100% |
| Connector continuity | Multimeter | < 0.5 ohm | 100% |

IN-PROCESS INSPECTION:
| Stage | Check | Method | Accept | Record |
|-------|-------|--------|--------|--------|
| After welding | Weld visual + dims | Visual + caliper | AWS D1.2 | Photo |
| After assembly | Torque check | Torque wrench | Per spec | Checklist |
| After wiring | Continuity + isolation | Multimeter | Per ICD | Test report |
| After firmware | Functional test | Test procedure | Per req | Log |

FINAL ACCEPTANCE TEST (FAT):
| Test | Requirement | Method | Duration | Accept |
|------|------------|--------|----------|--------|
| [test 1] | R-xxx | [method] | [time] | [criteria] |
| [test 2] | R-xxx | [method] | [time] | [criteria] |
| ... | ... | ... | ... | ... |

TRACEABILITY:
  Each unit gets serial number: {{project_id}}-[YYYY]-[NNN]
  Test records retained for: [5 years minimum for defense]
```

### Step 6b: P03 Document Quality Gate + P04 TCVN Compliance (from S1 Prompt Library)

Before compiling final package, verify all documents meet P03 and P04 standards:

```
P03 ENGINEERING DOCUMENT QUALITY — {{project_id}}

□ Quantification rate: ≥80% of specs have measurable acceptance criteria?
□ Parameter citation: 100% of technical parameters traceable to source?
□ Safety tagging: All life-safety requirements tagged [SAFETY-CRITICAL]?
□ No forbidden vague terms: "adequate", "sufficient", "good", "robust" → replaced with numbers?
□ YAML frontmatter: project, phase, type, version, created, status — all present?
□ [UNKNOWN] marked: Any unverified value flagged [UNKNOWN: requires verification from {{source}}]?

P03 SCORE: __/6 checks passed
```

```
P04 TCVN COMPLIANCE — {{project_id}}

□ Primary standard identified and cited (TCVN_XXXX:YYYY)?
□ Compliance matrix: section-by-section Compliant / Gap / Unknown?
□ Top 3 procurement-blocking gaps explicitly highlighted?
□ No fabricated TCVN clause numbers (use [TCVN-UNKNOWN] if uncertain)?
□ Safety-critical sections with GAP/CONFLICT flagged as [SAFETY-GAP]?

P04 SCORE: __/5 checks passed
IF any P03 or P04 FAIL → revise documents before Phase 4 compilation
```

### Step 7: Assembly Instructions Outline

```
ASSEMBLY INSTRUCTIONS — {{project_id}}
Date: {{today}}

REQUIRED TOOLS:
  [list specific tools: torque wrench ranges, crimping tools, etc.]

REQUIRED CONSUMABLES:
  [thread locker, thermal paste, conformal coat, etc.]

ASSEMBLY SEQUENCE:
| Step | Action | Parts Used | Torque/Spec | Photo Ref | Time (min) |
|------|--------|-----------|-------------|-----------|-----------|
| 1 | [action] | M-01, F-01 | [spec] | [ref] | [est] |
| 2 | [action] | E-01, M-02 | [spec] | [ref] | [est] |
| ... | ... | ... | ... | ... | ... |

CRITICAL STEPS (require sign-off):
  Step [N]: [description] — Inspector sign-off required
  Step [N]: [description] — Functional test before proceeding

ESTIMATED TOTAL ASSEMBLY TIME: [hours] per unit
```

### Step 8: Workshop Master Review (Core)

Present manufacturing package to workshop master (or user acting as workshop master):

```
WORKSHOP REVIEW — {{project_id}}
Date: {{today}}
Reviewer: [name]

MANUFACTURING FEASIBILITY:
| Item | Workshop Can Make? | Notes |
|------|-------------------|-------|
| [part 1] | [YES/OUTSOURCE/MODIFY] | |
| [part 2] | [YES/OUTSOURCE/MODIFY] | |
| ... | ... | ... |

WORKSHOP VERDICT: "gia cong duoc" / "can sua" / "khong lam duoc"
  [YES — proceed to fabrication]
  [MODIFY — list changes needed, iterate]
  [NO — fundamental redesign needed, return to Phase 3]

SIGN-OFF: _________________ Date: _________
```

### Step 9: Operational Update Lifecycle Document (ACH products only)

For products flagged as ACH in FORGE portfolio, generate:

```
OPERATIONAL UPDATE LIFECYCLE — {{project_id}}
Date: {{today}}
ACH Status: [YES — from forge-shift]

1. MODEL UPDATE PROCEDURE:
   a. Trigger: [scheduled quarterly / performance regression detected / new training data available]
   b. Retraining pipeline: [data source → labeling → training → validation → staging → deploy]
   c. Validation criteria: [minimum accuracy on test set, no regression on edge cases]
   d. Deployment method: [OTA / USB field update / depot-level update]
   e. Rollback trigger: [performance below threshold for N consecutive samples]
   f. Rollback procedure: [automatic / manual — steps to revert to previous model]

2. FIELD DATA COLLECTION:
   a. What data is collected: [sensor readings, inference results, ground truth when available]
   b. Storage: [onboard buffer size, offload method, offload frequency]
   c. Privacy/security: [data classification, encryption, handling procedures]

3. MONITORING:
   a. Health telemetry: [CPU temp, inference time, error rate, uptime]
   b. Performance drift detection: [moving average of key metrics, alert threshold]
   c. Alerting: [who gets notified, how, escalation path]

4. VERSION TRACKING:
   a. Model version format: [project-vMAJOR.MINOR.PATCH]
   b. Registry: [where deployed model versions are tracked per unit serial number]
   c. Compatibility matrix: [which model versions work with which firmware/hardware versions]

5. DEPENDENCY MANAGEMENT:
   a. AI framework: [version, update policy]
   b. OS: [version, security patch policy]
   c. Hardware drivers: [version, compatibility notes]
```

### Step 10: Compile Phase 4 Deliverables

Save to `1_Projects/{{project}}/Phase4-Detail/`:
- `Manufacturing_Drawings/` — drawing files (DXF/PDF per ISO 128/TCVN)
- `BOM_Final.md` — hierarchical BOM (assembly → subassembly → part):
  - Per item: Part Number | Description | Qty | Material/Spec | Make/Buy | Local% | Unit Cost (VND) | Source | MIL-STD req
  - Local content target: ≥60% by value for Vietnamese defense programs
  - Flag single-source items and long-lead items (>4 weeks)
- `Manufacturing_Plan.md` — process sequence per custom part, tooling/fixture requirements, quality inspection points, estimated time per unit
- `Inspection_Checklist.md`
- `Assembly_Instructions.md`
- `Test_Procedures.md` — unit-level + integration + system acceptance tests, mapped to requirements
- `Workshop_Review.md`
- `DfX_Final_Verification.md`
- `Documentation_Package.md` — drawing list, wiring diagrams, SW version, user manual outline, maintenance manual outline
- `Operational_Update_Lifecycle.md` — ACH products only (from Step 9)

Update `Status.md` → Phase 4 complete, ready for Gate 4 review and fabrication.

## Integration

```
helix-detail-finalize READS FROM:
  - helix-embody-realize → frozen layout, ICD v3, draft BOM
  - helix-task-clarify → requirements for traceability + test methods
  - forge-cost → budget validation against final BOM
  - forge-library → standard component specs for drawings

helix-detail-finalize WRITES TO:
  - bridge-deploy-gate → manufacturing package for Gate 4 review
  - bridge-risk-radar → manufacturing risks identified
  - forge-library → new component drawings cataloged
  - bridge-dashboard → project status update (Phase 4 complete)
```

### Step 10b: Customer-Facing Technical Specification (from Pattern Library B1)

For products approaching deployment, generate a customer-facing tech spec separate from internal manufacturing package:

```
TECHNICAL SPECIFICATION — {{product_id}}
Version: v1.0 DRAFT
Date: {{today}}
Audience: Vietnamese military procurement officers + technical evaluators
Standard: TCVN format where applicable

STRUCTURE:
1. OVERVIEW (1 page max)
   - Product description, operational concept, key differentiators
   - Photo/render of product in operational context

2. TECHNICAL SPECIFICATIONS (tables)
   - Performance specs with test methods (from requirements list)
   - Environmental specs: MIL-STD-810H Method 501-507 (tropical)
   - EMC specs: MIL-STD-461G (if applicable)
   - Power specs: voltage, consumption, battery life

3. INTERFACE SPECIFICATIONS
   - Physical: dimensions, weight, mounting (from ICD v3)
   - Electrical: connectors, pinout (from ICD v3)
   - Data: protocols, formats, update methods

4. ENVIRONMENTAL SPECIFICATIONS
   - Operating temperature: {{range}} (Vietnam tropical)
   - Storage temperature: {{range}}
   - Humidity: 40-100% RH (non-condensing)
   - Salt fog: per MIL-STD-810H Method 509
   - IP rating: {{IPxx}}

5. COMPLIANCE MATRIX
   | Standard | Clause | Compliant | Gap | Evidence |
   |----------|--------|:---------:|:---:|----------|
   | TCVN_XXXX | §X.Y | ✓/✗/TBD | | |
   | MIL-STD-810H | Method 501 | ✓/✗/TBD | | |

6. LOGISTICS
   - Packaging, transport, storage requirements
   - Maintenance schedule, MTBF, MTTR
   - Spare parts list (from BOM critical items)
   - Training requirements
```

**CONSTRAINTS (from Pattern Library B1):**
- Do NOT invent specifications — use only data from Phase 4 deliverables
- Do NOT claim MIL-STD compliance without verification note
- Do NOT include pricing or commercial information
- Do NOT reference competitor products by name
- Tone: factual, precise, professional — no marketing language
- Every spec value must be traceable to a test method
- Mark unverified values as [TBD — requires {{test_type}}]

**Save to:** `1_Projects/{{project}}/Phase4-Detail/Tech_Spec_v1.0.md`

## Rules

- AI NEVER determines which dimensions are critical — that requires workshop experience
- Workshop master review ("gia cong duoc?") is MANDATORY before fabrication
- Final BOM must include Vietnam-sourced vendors where possible
- Inspection checklist must trace back to requirements (Req-ID linkage)
- Serial number scheme must be defined before first unit
- All test records retained minimum 5 years for defense products
- Long-lead items must be flagged with order-by dates
- Link to Galaxy: [[Phan doan khong the uy thac cho AI]] — manufacturing feasibility is judgment
- Link to Galaxy: [[Musk Sequence]] — serial development, get one right before scaling

## COD Classification

- CAD completion from specs: Offload (O1) — AI executes defined geometry
- Drawing generation: Offload (O1) — automated from 3D model
- BOM compilation: Offload (O1) — AI extracts from design
- Inspection checklist generation: Offload (O2) — AI drafts from requirements
- Assembly instructions outline: Offload (O2) — AI drafts sequence
- GD&T on critical dimensions: **Core (C)** — manufacturing experience required
- Workshop master review: **Core (C)** — physical feasibility judgment
- Final sign-off for fabrication: **Core (C)** — CEO accountable
- Vendor selection for critical parts: **Core (C)** — relationship and trust based
