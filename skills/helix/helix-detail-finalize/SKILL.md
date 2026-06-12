---
name: helix-detail-finalize
description: "Orchestrator for Pahl-Beitz Phase 4 Detail Design — multi-agent pipeline commanding 6 block-skills (preflight → drawing → bom → inspection → assembly → handoff). Each block is an independent skill that can be run, inspected, and upgraded separately. Produces manufacturing-ready package + bridges to forge-fabrication F0. Flags: --from <block>, --only <block>, --variant <name>, --no-tech-spec, --ach. Triggers on: 'detail design', 'manufacturing drawings', 'production ready', 'hoan thien che tao', 'Phase 4', 'finalize design', 'workshop fabrication handoff'."
---

# Helix Detail Finalize — Phase 4 Orchestrator (Multi-Agent Pipeline)

> **Role:** Chỉ huy trưởng (Commander) — điều phối 6 block-skills tuần tự, đóng vòng R&D → production
> **Architecture:** Modular pipeline — đối xứng với P1 (helix-task-clarify), P2 (helix-concept-generate), P3 (helix-embody-realize)
> **P&B Reference:** Chapter 9 (Detail Design § 9.1-9.7)
> **VDI 2221:2019:** Blatt 1 — requirements MUST be frozen before detail design begins
> **AI-Orchestration:** S1 (Schema v3.0) · S2 (Multi-Agent) · S3 (P02 QC) · S5 (Audit Trail)
> **Closes:** the R&D → production gap. Feeds `forge-fabrication F0`.

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                  helix-detail-finalize (ORCHESTRATOR — 6 blocks)                 │
│                                                                                   │
│  Flags: --from <B0/BA/BB/BC/BD/BE>  --only <X>  --variant <name>                │
│         --no-tech-spec  --ach (force ACH lifecycle)                             │
│                                                                                   │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐                     │
│  │ B0   │─▶│ BA   │─▶│ BB   │─▶│ BC   │─▶│ BD   │─▶│ BE   │                     │
│  │PRE-  │  │DRAW- │  │FINAL │  │INSP- │  │ASSEM-│  │HAND- │                     │
│  │FLT   │  │ING   │  │BOM   │  │ECTION│  │BLY   │  │OFF   │                     │
│  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘                     │
│     │CEO     │CORE     │CORE     │CEO      │CEO      │CORE                      │
│     ▼        ▼         ▼         ▼         ▼         ▼                          │
│  [verify]  [GD&T]   [vendor]  [FAT]     [DfX     [workshop                     │
│   freeze    drawings  cost     trace-    final +   master                       │
│   reqs      ISO128    long-    ability   routing]  review]                      │
│                       lead                                                       │
└──────────────────────────────────────────────────────────────────────────────────┘

Legend: CORE = CEO non-delegable | CEO = checkpoint after block

Data Bus: 1_Projects/{{project}}/Phase4-Detail/{{variant}}/
State:    {{output_path}}/_pipeline_state.md
Next:     /helix-quality-gate ... --gate 4  +  /forge-fabrication ...
```

## Sub-Skills (6 Block-Skills)

| Block | Skill | P&B § | Purpose | CEO Gate |
|----|----|----|----|----|
| **B0** | `/helix-p4-preflight` | 9.1 | Verify P3 + Gate 3, **requirements freeze (VDI 2221:2019)**, identify detail-determining components, P03/P04 readiness, ACH detection | Approve freeze + detail-determining list |
| **BA** | `/helix-p4-drawing` | 9.2-9.3 | **CEO specifies critical GD&T/surface/weld/connector/PCB (CORE)**, AI completes 3D + 2D drawings per ISO 128/TCVN, Gerber prep, drawing index | **CORE — critical spec table** |
| **BB** | `/helix-p4-bom` | 9.4 | Final BOM (mech/elec/fasteners/COTS), **Vietnam vendor selection ≥60% local**, long-lead order-by, cost rollup vs P3, single-source flags, MIL/TCVN trace | **CORE — vendor selection critical/SS** |
| **BC** | `/helix-p4-inspection` | 9.5 | Incoming + in-process + FAT plans, Req-ID ↔ Test-ID matrix, serialization, P03 + P04 gates, 5-yr retention | Approve FAT criteria + serial scheme |
| **BD** | `/helix-p4-assembly` | 9.6 | Final DfX verification, tools/consumables, step-by-step sequence with critical sign-off, time/unit, **routing alignment with erp-master** | Approve critical sign-off + time |
| **BE** | `/helix-p4-handoff` | 9.7 | **Workshop master review "gia cong duoc?" (CORE)**, ACH Operational Lifecycle (if applicable), customer Tech Spec, compile package, **handoff to forge-fabrication F0** | **CORE — workshop verdict** |

## How to Use

### Full Pipeline (default)
```
/helix-detail-finalize VN-XUONG-UUV
```
Runs B0 → BE sequentially. Pauses after each block for CEO inspection.

### With variant
```
/helix-detail-finalize VN-MGM V5-MOTORIZED
```
Output → `Phase4-Detail/V5-MOTORIZED/` + file prefix `VN_MGM_V5_`.

### Resume from block
```
/helix-detail-finalize VN-XUONG-UUV --from BC
```

### Single block (re-run after adjustment)
```
/helix-p4-bom VN-XUONG-UUV
```

### Skip customer tech spec
```
/helix-detail-finalize VN-XUONG-UUV --no-tech-spec
```

### Force ACH lifecycle (override B0 detection)
```
/helix-detail-finalize BB-01 --ach
```

## Orchestrator Workflow

### Step 1: Parse Arguments

```
PROJECT: {{first arg}}
VARIANT: {{second arg or empty}}
FLAGS:
  --from X        → Resume from B0/BA/BB/BC/BD/BE
  --only X        → Run single block
  --variant N     → Variant subfolder + file prefix
  --no-tech-spec  → BE skips customer-facing Tech Spec
  --ach           → Force ACH lifecycle in BE (override B0)
```

### Step 1.5: Resolve Output Path + Variant Convention

```
If variant given:
  output_path = 1_Projects/{{project}}/Phase4-Detail/{{variant}}/
  prefix      = {{PROJECT}}_{{VARIANT_SHORT}}_
Else:
  output_path = 1_Projects/{{project}}/Phase4-Detail/
  prefix      = {{PROJECT}}_
```

Matches P1-P3 variant convention exactly.

### Step 1.6: Input Validation

**MANDATORY before any block.** Verify Phase 3 outputs exist:

```
═══ INPUT VALIDATION — {{project}} {{variant}} — Phase 4 ═══

REQUIRED (Phase 3 — helix-embody-realize):
  □ {{prefix}}BA_Layout.md
  □ {{prefix}}BB_DfX_Review.md
  □ {{prefix}}BC_Integration.md (ICD v3 frozen)
  □ {{prefix}}BD_BOM_Draft.md
  □ {{prefix}}BE_Phase3_Compile.md
  □ Gate 3 PASSED

REQUIRED (Phase 1):
  □ {{prefix}}Requirements_List_v*.md (frozen)
  □ {{prefix}}Requirements_Delta_Log.md (if exists)

RECOMMENDED:
  □ FORGE/ACH_Assessment_v*.md (for BE ACH lifecycle)
  □ FORGE/Cost_Envelope_v*.md (for BB variance check)

CEO:
(1) ▶️ Proceed with current inputs
(2) 🔄 Run prerequisite: /helix-embody-realize / /helix-quality-gate --gate 3
(3) 📝 Manual input
═══════════════════════════════════════════════════
```

### Step 2: Initialize Pipeline State

`{{output_path}}/_pipeline_state.md`:

```markdown
---
project: {{project}}
variant: {{variant or "default"}}
pipeline: helix-detail-finalize v2.0
started: {{today}}
updated: {{today}}
ach_lifecycle: [TBD — set by B0]
---

# Phase 4 Pipeline State — {{project}} {{variant}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|----|----|----|----|----|----|
| B0 | helix-p4-preflight | PENDING | - | - | - |
| BA | helix-p4-drawing | PENDING | - | - | - |
| BB | helix-p4-bom | PENDING | - | - | - |
| BC | helix-p4-inspection | PENDING | - | - | - |
| BD | helix-p4-assembly | PENDING | - | - | - |
| BE | helix-p4-handoff | PENDING | - | - | - |

## Block Ledger
> SOLE communication channel between blocks.

[populated by each block]

## CEO Decisions
[populated at each checkpoint]

## Requirements Delta Log (Phase 4)
> If any block discovers a need to change Phase 1/2/3 reqs → STOP, escalate as architectural concern. Phase 4 = freeze.
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ #1 RULE: Execute EXACTLY ONE block per turn. STOP and WAIT for CEO response after each.**

#### Ledger Read Protocol (BEFORE each block)
Read `_pipeline_state.md` → Block Ledger. Reconstruct context. Critical for `--from` resume.

#### Ledger Write Protocol (AFTER each block)
Append:
```
### {{Block ID}} — {{block name}} ({{date}})
**Key outputs:** [2-3 bullets — files + counts]
**Decisions for downstream:** [what next block needs]
**Open questions:** [unresolved]
**CEO checkpoint result:** [approve / revise / pause + words]
```

#### Per-Block Execution

For each block (respecting --from / --only):

1. **Ledger Read** — context reconstruct
2. **Announce:** "Đang chạy Block {{X}}: {{name}}..."
3. **Pre-conditions check** — verify predecessor files exist
4. **Execute block** — invoke `/helix-p4-{{name}}` (orchestrator never does block work itself)
5. **Post-conditions check** — verify expected outputs created
6. **Ledger Write** — append summary
7. **Update state** — mark COMPLETE
8. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK {{X}} COMPLETE ═══
   Deliverables: [files]
   Key findings: [bullets]
   
   CEO:
   (1) ✅ Approve → tiếp tục Block {{next}}
   (2) 🔄 Chạy lại Block {{X}} với điều chỉnh
   (3) ⏸️ Dừng pipeline
   (4) ⏭️ Skip Block {{next}}
   ```
9. **⛔ WAIT for CEO message.**

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
PHASE 4 PIPELINE COMPLETE — {{project}} {{variant}}
═══════════════════════════════════════════════════
Manufacturing package: {{N}} files in Phase4-Detail/{{variant}}/
Workshop verdict: GIA CONG DUOC
Local content: {{%}} (target ≥60%)
Unit cost: {{VND}} (variance vs P3: ±{{%}})
FAT coverage: {{N}}/{{N}} D-requirements
Critical sign-off steps: {{N}}
ACH lifecycle: [READY / N/A]

Next:
  - /helix-quality-gate {{project}} --gate 4   (formal gate review)
  - /forge-fabrication --product {{project}} --qty N --helix-handoff {{path}}
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files in `{{output_path}}/` with `{{prefix}}` prefix:

| File Pattern | Written By | Read By | Content |
|----|----|----|----|
| `_pipeline_state.md` | Orchestrator | All blocks | Progress, ledger, CEO decisions |
| `B0_Preflight_Report.md` | B0 | BA, BE | P3 verification + reqs freeze + detail-determining + ACH flag |
| `Manufacturing_Drawings/` (dir) | BA | BB, BC, BD | DXF + PDF per part |
| `Schematics/`, `Gerber/` (dirs) | BA | BD, fabrication | PCB production files |
| `BA_Drawing_Index.md` | BA | BB | Drawing list + revisions |
| `BOM_Final.md` + `BOM_Final.csv` | BB | BC, BD, BE, **forge-fabrication F0** | Hierarchical BOM + vendor + cost |
| `Inspection_Checklist.md` | BC | BD, BE, **forge-fabrication F3/F4** | Incoming + in-process + FAT |
| `Test_Procedures.md` | BC | BE | FAT procedure book |
| `Req_Test_Traceability.md` | BC | BE, Gate 4 | Req-ID ↔ Test-ID matrix |
| `Serialization_Scheme.md` | BC | BE, fabrication | Serial format + retention |
| `Calibration_Register.md` | BC | BE | Equipment cal references |
| `Assembly_Instructions.md` | BD | BE, **forge-fabrication F3** | Step sequence + critical sign-off |
| `DfX_Final_Verification.md` | BD | BE | Final DfX result |
| `Tools_Consumables.md` | BD | BE | Required for production |
| `First_Article_Plan.md` | BD | BE, fabrication | FA build plan |
| `Workshop_Review.md` | BE | Gate 4 | Workshop verdict |
| `Operational_Update_Lifecycle.md` | BE (ACH only) | bridge-deploy-gate | ACH lifecycle |
| `Tech_Spec_v1.0.md` | BE | customer | TCVN-format spec |
| `Handoff_to_Fabrication.md` | BE | **forge-fabrication F0** | Production readiness summary |

Update `_routing.md` (planned hours from BD) — feeds `erp-master` Operations.

## Integration

```
helix-detail-finalize (ORCHESTRATOR) COMMANDS:
  → /helix-p4-preflight    (B0)
  → /helix-p4-drawing      (BA)
  → /helix-p4-bom          (BB)
  → /helix-p4-inspection   (BC)
  → /helix-p4-assembly     (BD)
  → /helix-p4-handoff      (BE)

helix-detail-finalize READS FROM:
  - helix-embody-realize → P3 deliverables (layout, DfX, ICD v3, BOM draft)
  - helix-task-clarify → frozen requirements + test methods
  - forge-cost → cost envelope (variance check)
  - forge-shift → ACH assessment (BE lifecycle decision)
  - forge-library → standard component specs

helix-detail-finalize WRITES TO:
  - 1_Projects/{{project}}/Phase4-Detail/{{variant}}/ → all deliverables
  - 1_Projects/{{project}}/_routing.md → planned hours (BD output)
  - helix-quality-gate → Gate 4 readiness
  - **forge-fabrication → F0 handoff package (closes R&D → production loop)**
  - bridge-deploy-gate → manufacturing package signed off
  - bridge-risk-radar → manufacturing risks identified
  - forge-library → new component drawings cataloged

helix-detail-finalize FOLLOW-UP (CEO-triggered):
  - /helix-quality-gate {{project}} --gate 4 → formal Gate 4 review
  - /forge-fabrication --product {{project}} ... → production run
  - /bridge-deploy-gate → deployment readiness check
  - /helix-design-journal → log final decisions

SHARED REFERENCES (in helix-detail-finalize/references/):
  - pb-detail-design.md → P&B Ch9 complete methodology
  - prompt-templates.md → S1 prompt templates for Phase 4
```

## Why This Mega-Skill Exists (Symmetry + Loop Closure)

Before: `helix-detail-finalize` was a **single skill** while P1/P2/P3 each had 6-block pipelines. This asymmetry meant the most expensive phase (detail design — entering production) had the **least granular CEO control**.

After: P4 mirrors P1-P3. Each block has independent checkpoint, can be re-run, can be inspected. Critical CORE decisions (GD&T, vendor selection, workshop review) are isolated into their own blocks instead of buried in step list.

**The bigger closure:** `BE → Handoff_to_Fabrication.md → forge-fabrication F0`. Previously there was a black hole between "design freeze" and "part on shop floor". Now it's a documented bridge that auto-generates the production trigger.

```
HELIX P1 → P2 → P3 → P4 (this) → forge-fabrication F0→F5 → field → forge-flywheel
```

Compounding asset, not one-shot transaction.

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After each block, STOP. NEVER chain. #1 rule.
- **B0 requirements freeze is mandatory** — VDI 2221:2019 Blatt 1. PENDING reqs block pipeline.
- **BA critical specs are CEO Core** — GD&T, surface, weld NDT, connector pinout, PCB approval. AI cannot determine.
- **BB vendor selection for critical/single-source = CORE** — relationship + supply chain commitment.
- **BC P03 + P04 gates must PASS before BE** — fail = revise docs.
- **BD DfX FAIL = loop back to BA** — never proceed with failed DfX.
- **BE workshop verdict is CORE — non-delegable** — "gia cong duoc?" must be physically judged.
- **Phase 4 requirements ARE FROZEN** — any block discovering a needed req change → STOP, escalate as architectural concern, not a routine delta.
- **Handoff_to_Fabrication.md is the production trigger** — generated by BE, consumed by forge-fabrication F0.
- **`_routing.md` planned hours come from BD** — forge-fabrication F3 will update actuals back. This is the compounding asset.
- **Each block-skill is independently runnable** — CEO can `/helix-p4-bom` alone after BB adjustment.
- **Orchestrator NEVER does block work** — always delegates.
- **Data Bus contract is sacred** — exact filenames + prefix convention.
- **If CEO says "chạy hết" or "skip checkpoints"** — STILL stop after each block, minimal checkpoint (1-line + "tiếp tục?").

## COD Classification

- Pipeline orchestration: Offload (O1)
- Block execution: Offload (O2) — each block has own COD
- B0 reqs freeze decision: **Core (C)** — accountability for "no more changes"
- BA critical specs: **Core (C)** — manufacturing experience
- BB vendor selection (critical/SS): **Core (C)** — supply chain trust
- BC FAT acceptance thresholds: **Core (C)** — quality bar
- BD critical sign-off step selection: **Core (C)** — safety judgment
- BE workshop master review: **Core (C)** — physical feasibility (non-delegable)
- BE Tech Spec accuracy sign-off: **Core (C)** — customer-facing claims
- Phase 4 completion sign-off: **Core (C)** — CEO accountable
