---
name: helix-p4-assembly
description: "Block D of Phase 4 pipeline — final DfX verification on production geometry, tools + consumables list, step-by-step assembly sequence with torque specs + critical sign-off steps, time estimation per unit, PX workstation routing alignment with erp-master routing. P&B 9.6. Triggers on: 'Phase 4 assembly', 'assembly instructions', 'work instructions', 'final DfX'."
---

# Block D: Assembly — Work Instructions + Final DfX

> **P&B:** Chapter 9 § 9.6 | **Pipeline:** helix-detail-finalize → Block BD
> **Input:** BA drawings + BB BOM + BC inspection gates | **Output:** `Assembly_Instructions.md` + `DfX_Final_Verification.md` + `_routing.md` update

## Operational Envelope

| DO | DON'T |
|----|----|
| Final DfX verification on production geometry | Critical dim/tolerance (= BA, CEO Core) |
| Tools + consumables list | Vendor selection (= BB, CEO Core) |
| Step-by-step assembly sequence | Inspection acceptance criteria (= BC) |
| Time estimate per unit per PX | Workshop master sign-off (= BE, CEO Core) |
| Routing alignment with erp-master | Customer training materials (BE/BRIDGE) |

**Multi-Agent Mode:** Optional — parallel per PX (CKCX/DT/DC/VL) when complex.
**CEO Checkpoint:** Approve critical sign-off steps + time estimates.

## Workflow

### Step D.1: Final DfX Verification (re-run on production geometry)

```
FINAL DfX — {{project}} Rev: BA drawings v1.0
Date: {{today}}

| Category | Items Checked | PASS | WARN | FAIL |
|----|----|----|----|----|
| DfM (manufacturability) | | | | |
| DfA (assembly) | | | | |
| DfR (reliability) | | | | |
| DfT (test) | | | | |
| DfU (use) | | | | |

GATE: [PASS — proceed / FAIL — iterate back to BA]
Remaining WARN items: [list with accepted risk + mitigation]
```

Any FAIL → loop back to BA. WARN allowed with documented rationale.

### Step D.2: Tools + Consumables List

```
REQUIRED TOOLS:
| Tool | Spec | Range | Calibrated? | PX |
|----|----|----|----|----|
| Torque wrench | 5-25 Nm | | Yes (cert ref BC) | CKCX |
| Crimper | AWG 22-12 | | No | DC |
| ESD wrist strap | 1 MΩ | | Yes (monthly) | DT |
| ...

REQUIRED CONSUMABLES:
| Consumable | Spec | Vendor | Qty/unit | Shelf life |
|----|----|----|----|----|
| Thread locker | Loctite 243 | | drops | 2 yr |
| Thermal paste | TIM-X | | g | 1 yr |
| Conformal coat | spec | | mL | 1 yr |
```

### Step D.3: Step-by-Step Assembly Sequence

Each step: action, parts, spec, photo ref, time, PX.

```
ASSEMBLY SEQUENCE — {{project}}
Total estimated time: {{H}} hours/unit

| Step | PX | Action | Parts Used | Torque/Spec | Photo Ref | Time (min) | Critical? |
|----|----|----|----|----|----|----|----|
| 1 | CKCX | [action] | M-001, F-001 | 5 Nm | DWG-001 | 10 | |
| 2 | DT | [action] | E-001, E-002 | 3.5V check | SCH-002 | 15 | ⚠️ sign-off |
| 3 | DC | [action] | M-010, E-005 | continuity | DWG-010 | 8 | |
| 4 | VL | [action] | finishing | Ra 1.6 | DWG-020 | 12 | |
| 5 | FINAL | [action] | full unit | FAT | TST-001 | 30 | ⚠️ sign-off |
```

### Step D.4: Critical Sign-Off Steps

```
CRITICAL STEPS (require inspector + log entry):
Step {{N}}: [description]
  Inspector: QĐ {{PX}} or QC
  Verification method: [exact check]
  Record: signature + photo + measurement value
  Block status: cannot proceed to next step until signed

Common critical steps:
  □ Torque on safety-critical fasteners
  □ Polarity check before power-on
  □ Functional test before sealing
  □ FAT before serialization
```

### Step D.5: Routing Alignment (feeds erp-master routing)

The assembly sequence MUST match `_routing.md` operations and workstation assignments.

```
ROUTING ALIGNMENT CHECK:
| Routing Op | PX | Plan hrs | Assembly Step(s) | Match? |
|----|----|----|----|----|
| OP-010 CNC | CKCX | 4.0 | Steps 1-3 | ✅ |
| OP-020 Weld | CKCX | 2.5 | Step 4 | ✅ |
| OP-030 PCB | DT | 6.0 | Steps 5-8 | ✅ |
| ...
```

Update `_routing.md` planned hours from this block's time estimates. (forge-fabrication F3 will later update actuals back.)

### Step D.6: Time Estimation per Unit

```
TIME PER PX (planned, from steps):
| PX | Planned hrs | Critical path? |
|----|----|----|
| CKCX | | |
| DT | | |
| DC | | |
| VL | | |
| **Total** | | |

Compare with forge-fabrication F1 capacity check → flag if any PX bottleneck.
```

### Step D.7: First Article Build Plan

```
FIRST ARTICLE (FA) PLAN — unit serial {{PROJECT}}-{{YYYY}}-001
□ Built by lead technician + supervised
□ All time logs captured (compare to estimate)
□ All NCRs documented for routing refinement
□ FA review meeting before lot release
```

## Output

`1_Projects/{{project}}/Phase4-Detail/{{variant}}/`:
- `Assembly_Instructions.md` — full sequence
- `DfX_Final_Verification.md`
- `Tools_Consumables.md`
- `First_Article_Plan.md`
- Update: `_routing.md` planned hours

## CEO Checkpoint

```
═══ BLOCK BD ASSEMBLY COMPLETE ═══
DfX final: PASS/WARN/FAIL counts
Steps: {{N}} total, {{N}} critical sign-off
Time/unit: {{H}}h ({{H}} CKCX + {{H}} DT + {{H}} DC + {{H}} VL)
Routing aligned with erp-master: {{Y/N}}

CEO:
(1) ✅ Approve → tiếp tục Block BE (Handoff)
(2) 🔄 Adjust critical sign-off steps / time estimates
(3) ⏸️ DfX FAIL — return to BA for design fix
```

## COD

- Final DfX checklist run: Offload (O2)
- Tools/consumables list: Offload (O1)
- Step sequence drafting: Offload (O2)
- Time estimate from operations: Offload (O1)
- Routing alignment check: Offload (O1)
- **Critical sign-off step selection: Core (C)** — safety judgment
- **DfX FAIL acceptance: Core (C)** — risk decision
