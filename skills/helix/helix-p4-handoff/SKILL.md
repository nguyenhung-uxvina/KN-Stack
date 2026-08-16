---
name: helix-p4-handoff
description: "Block E of Phase 4 pipeline — workshop master review (CORE 'gia cong duoc?'), ACH Operational Update Lifecycle (if applicable), customer-facing TCVN technical specification, compile Phase 4 deliverables, generate handoff package for forge-fabrication F0, update Status.md → ready for Gate 4. P&B 9.7. Triggers on: 'Phase 4 handoff', 'workshop review', 'manufacturing package', 'gia cong duoc'."
---

# Block E: Handoff — Workshop Review + Manufacturing Package + forge-fabrication Bridge

> **P&B:** Chapter 9 § 9.7 | **Pipeline:** helix-detail-finalize → Block BE
> **Input:** BA drawings + BB BOM + BC inspection + BD assembly | **Output:** Compiled manufacturing package + `Handoff_to_Fabrication.md`
> **Critical:** Closes R&D → production. Feeds `forge-fabrication F0`.

## Operational Envelope

| DO | DON'T |
|----|----|
| Workshop master review ("gia cong duoc?") | Change drawings/BOM/inspection (loop back) |
| ACH lifecycle (if applicable from B0) | Order materials (= forge-fabrication F1) |
| Customer-facing TCVN tech spec | Release WO (= forge-fabrication F2, CORE) |
| Compile manufacturing package | Field warranty terms (BRIDGE) |
| Handoff package for forge-fabrication F0 | Customer pricing (commercial — separate) |
| Status.md update + Gate 4 readiness | |

**Multi-Agent Mode:** NO.
**CEO Checkpoint:** Workshop verdict (gia cong duoc / can sua / khong lam duoc) + final Phase 4 sign-off.

## Workflow

### Step E.1: Workshop Master Review (CORE — non-delegable)

```
WORKSHOP REVIEW — {{project}}
Date: {{today}}
Reviewer: [workshop master / lead technician name]

MANUFACTURING FEASIBILITY:
| Item | Workshop Can Make? | Notes |
|----|----|----|
| [part 1] | YES / OUTSOURCE / MODIFY | |
| [part 2] | YES / OUTSOURCE / MODIFY | |
| ... | | |

PX READINESS:
| PX | Tools available? | Consumables stocked? | Operator trained? | Ready? |
|----|----|----|----|----|
| CKCX | | | | |
| DT | | | | |
| DC | | | | |
| VL | | | | |

WORKSHOP VERDICT:
  □ "GIA CONG DUOC" — proceed to fabrication ✅
  □ "CAN SUA" — list changes needed, iterate (loop back to BA/BB/BD)
  □ "KHONG LAM DUOC" — fundamental redesign, return to Phase 3

SIGN-OFF: _________________ Date: _________
```

**This step is non-delegable.** AI presents drawings/BOM/instructions, workshop master judges.

### Step E.2: ACH Operational Update Lifecycle (if ACH = YES from B0)

For ACH products (AI-Compensates-Hardware), generate:

```
OPERATIONAL UPDATE LIFECYCLE — {{project}}
Date: {{today}}

1. MODEL UPDATE PROCEDURE:
   - Trigger: [quarterly / regression-detected / new training data]
   - Pipeline: data → label → train → validate → stage → deploy
   - Validation: [min accuracy + no regression on edge cases]
   - Deploy method: [OTA / USB field / depot]
   - Rollback trigger + procedure: [threshold + steps]

2. FIELD DATA COLLECTION:
   - Data: [sensor + inference + ground truth when available]
   - Storage: [onboard buffer + offload + frequency]
   - Privacy: [classification + encryption]

3. MONITORING:
   - Health telemetry: [CPU temp / inf time / error rate / uptime]
   - Drift detection: [moving avg + alert threshold]
   - Alerting: [who / how / escalation]

4. VERSION TRACKING:
   - Model: [project-vMAJOR.MINOR.PATCH]
   - Registry: [where versions tracked per serial]
   - Compatibility matrix: [model/firmware/hardware versions]

5. DEPENDENCY MANAGEMENT:
   - AI framework version + update policy
   - OS version + security patch policy
   - Hardware drivers
```

Save as `Operational_Update_Lifecycle.md`.

### Step E.3: Customer-Facing Technical Specification (TCVN format)

Separate from internal package — for customer/procurement evaluators.

```
TECHNICAL SPECIFICATION — {{product}}
Version: v1.0 DRAFT
Audience: VN military procurement + technical evaluators
Standard: TCVN format

STRUCTURE:
1. OVERVIEW (1 page)
2. TECHNICAL SPECIFICATIONS
   - Performance (from Req with test methods)
   - Environmental: MIL-STD-810H Method 501-507 (tropical)
   - EMC: MIL-STD-461G (if applicable)
   - Power: voltage / consumption / battery
3. INTERFACE SPECIFICATIONS
   - Physical (from ICD v3)
   - Electrical connectors (from ICD v3)
   - Data protocols
4. ENVIRONMENTAL SPECS
   - Op temp / Storage / Humidity / Salt fog / IP rating
5. COMPLIANCE MATRIX
   | Standard | Clause | Compliant | Gap | Evidence |
6. LOGISTICS
   - Packaging / transport / storage
   - Maintenance / MTBF / MTTR
   - Spare parts / Training
```

**Constraints (Pattern Library B1):**
- NEVER invent specs — only Phase 4 data
- NEVER claim MIL-STD without verification note
- NEVER include pricing
- NEVER reference competitors by name
- Factual tone, no marketing
- All values traceable to test method
- Unverified → `[TBD — requires {{test_type}}]`

Save as `Tech_Spec_v1.0.md` (separate publish track from internal package).

### Step E.4: Compile Manufacturing Package

`1_Projects/{{project}}/Phase4-Detail/{{variant}}/` final structure:

```
Phase4-Detail/{{variant}}/
├── _pipeline_state.md
├── B0_Preflight_Report.md
├── BA_Drawing_Index.md
├── Geometry/                 (STEP/ + code-CAD .py source — from [[helix-cad-bridge]], rev-locked geometry-of-record; THE geometry master)
│   └── cad_extract.json      (for any human-drawn/imported parts, via [[helix-cad-ingest]])
├── Manufacturing_Drawings/   (DXF + PDF — derived 2D views, NOT the master)
├── Schematics/               (PCB sch)
├── Gerber/                   (PCB production files)
├── BOM_Final.md
├── BOM_Final.csv             (for ERPNext sync)
├── Inspection_Checklist.md
├── Test_Procedures.md
├── Req_Test_Traceability.md
├── Serialization_Scheme.md
├── Calibration_Register.md
├── Assembly_Instructions.md
├── DfX_Final_Verification.md
├── Tools_Consumables.md
├── First_Article_Plan.md
├── Workshop_Review.md
├── Operational_Update_Lifecycle.md  (ACH only)
├── Tech_Spec_v1.0.md         (customer-facing)
└── Handoff_to_Fabrication.md  (← bridge to forge-fabrication)
```

### Step E.5: Handoff Package for forge-fabrication F0 (KEY INTEGRATION)

Generate `Handoff_to_Fabrication.md`:

```markdown
# Manufacturing Handoff — {{project}} {{variant}}
Date: {{today}}  Version: v1.0  Workshop verdict: GIA CONG DUOC

## Production Readiness
- BOM_Final.md → ready for `/erp-bom create {{product}}` (CSV exported)
- Drawings v1.0 RELEASED — drawing index attached
- Routing → `_routing.md` aligned with erp-master Operations
- Inspection plan → maps to erp-quality gates (CKCX/DT/DC/VL/Final)
- Serialization scheme → {{PROJECT}}-YYYY-NNN

## Files for forge-fabrication F0 verification
| File | Used by F0 check |
|----|----|
| Geometry/ (STEP/ + code-CAD .py source) | geometry master from [[helix-cad-bridge]] (rev-locked geometry-of-record) — fabrication receives the 3D master, not just 2D |
| Geometry/cad_extract.json | for any human-drawn/imported parts, via [[helix-cad-ingest]] |
| BOM_Final.md | erp-bom check {{product}} |
| _routing.md | erp-master audit (Routing check) |
| Workshop_Review.md | F0 handoff gate |
| Manufacturing_Drawings/ (DXF+PDF) | derived 2D views for shop floor (NOT the geometry master) |

## Pre-Run Reminders for CEO
- Long-lead items already ordered? {{Y/N — list pending}}
- Single-source HIGH risk items mitigated? {{Y/N}}
- VN local content {{%}} achieved (target ≥60%)
- First Article plan reviewed?
- Contract reference / customer for F5 invoice?

## Publication diagrams (wx-diagram — AUTO)

Trước khi đóng gói handoff, xuất bản vẽ sơ đồ qua `/wx-diagram` (engine draw.io, xem bảng quyết định trong skill đó):

1. `/wx-diagram block-diagram {{project}}` — assembly/block diagram cho fab bundle.
2. Lưu vào `1_Projects/{{project}}/Phase4-Detail/diagrams/`, liệt kê 2 file (.drawio + .drawio.png) vào mục Files của handoff.

Nếu draw.io CLI chưa cài → wx-diagram tự degrade (chỉ sinh .drawio XML) — vẫn đính kèm, KHÔNG chặn handoff.

## Next Command
```
/forge-fabrication --product {{product}} --qty {{N}} --helix-handoff {{this_path}}
```
```

### Step E.6: Status.md Update + Gate 4 Readiness

```
Update 1_Projects/{{project}}/Status.md:
  □ Phase 4 Detail Design: COMPLETE  ({{today}})
  □ Workshop verdict: GIA CONG DUOC
  □ Ready for Gate 4 review: YES
  □ Ready for forge-fabrication F0: YES
  □ ACH lifecycle: [READY / N/A]

Next gates:
  - /helix-quality-gate {{project}} --gate 4 (formal gate review)
  - /forge-fabrication --product {{product}} ... (production)
```

## Output

All files listed in Step E.4 above. Key new file: `Handoff_to_Fabrication.md` (the bridge to manufacturing).

## CEO Checkpoint

```
═══ BLOCK BE HANDOFF COMPLETE ═══
Workshop verdict: GIA CONG DUOC / CAN SUA / KHONG LAM DUOC
Manufacturing package: {{N}} files in Phase4-Detail/{{variant}}/
ACH lifecycle: [READY / N/A]
Tech Spec v1.0 DRAFT: ready
Handoff to forge-fabrication: READY

CEO:
(1) ✅ Approve → Phase 4 COMPLETE. Trigger /helix-quality-gate {{project}} --gate 4
(2) 🔄 Workshop CAN SUA — list changes, loop back
(3) ⏸️ KHONG LAM DUOC — return to helix-embody-realize
```

## COD

- ACH lifecycle drafting from FORGE inputs: Offload (O2)
- Tech Spec compilation from Phase 4 data: Offload (O2)
- Package compilation + Status update: Offload (O1)
- Handoff_to_Fabrication.md generation: Offload (O1) — mechanical from prior blocks
- **Workshop master review verdict: Core (C)** — physical feasibility, non-delegable
- **Tech Spec accuracy sign-off: Core (C)** — claims to customers
- **Phase 4 completion sign-off: Core (C)** — CEO accountable
