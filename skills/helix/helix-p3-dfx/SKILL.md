---
name: helix-p3-dfx
description: "Block B of Phase 3 pipeline — full DfX review (DfM/DfA/DfR/DfT/DfW/DfU), 3 basic rules audit (Clarity/Simplicity/Safety), 5 design principles check, PLAUSIBLE 9-check. P&B 7.3-7.5. Can run standalone. Triggers on: 'DfX review', 'design for manufacturing', 'PLAUSIBLE', 'clarity simplicity safety', 'design principles'."
---

# Block B: DfX Review — Design Rules + Principles + PLAUSIBLE

> **P&B:** 7.3 (Basic Rules) + 7.4 (Principles) + 7.5 (DfX Guidelines) | **Pipeline:** helix-embody-realize → Block BB
> **Input:** `BA_Preliminary_Layout.md` + Phase 1 requirements | **Output:** `BB_DfX_Review.md`, `BB_PLAUSIBLE_Check.md`, `BB_Basic_Rules_Audit.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], [[LLM Spatial Blindness]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Audit 3 basic rules (Clarity/Simplicity/Safety) | Modify layout directly (= flag issues for BA revision) |
| Check 5 design principles | Freeze ICDs (= BC) |
| Run full DfX review (16 categories) | Generate BOM (= BD) |
| Execute PLAUSIBLE 9-check | Override CEO's layout decisions |
| Flag FAIL items with severity + remediation | Propose spatial rearrangements (LLM Spatial Blindness) |

**Multi-Agent Mode:** NO — DfX is a structured checklist review, single agent sufficient. Spatial suggestions are explicitly out of scope per [[LLM Spatial Blindness]].
**CEO Checkpoint:** Resolve all FAIL severity H items. DfX WARN items documented for tracking.

## Workflow

> **Geometry-derived inputs (not hand-estimated):** Mass properties, bounding box, and interference inputs come from the layout's **geometry-of-record** (STEP via [[helix-cad-bridge]], or cad_extract.json via [[helix-cad-ingest]]) — not hand-estimated. Use the bridge's computed mass/CoG/volume for force-flow (B2), DfR mass/MTBF, and PLAUSIBLE Physics/Integration/Boundary (B4) checks.

### Step B1: 3 Basic Rules Audit (P&B 7.3)

```
BASIC RULES AUDIT — {{project}}

CLARITY (Rõ ràng) — P&B 7.3.1:
□ Every function clearly assignable to a component?
□ Force flow traceable through structure? (no ambiguous load paths)
□ No double fits? (one locating surface per direction)
□ Thermal expansion path defined?
□ Assembly sequence unambiguous?
□ Service life predictable from design?
Score: [0-4] Evidence: ___

SIMPLICITY (Đơn giản) — P&B 7.3.2:
□ Minimum component count for function?
□ Standard parts used where possible?
□ Simple shapes (reduce machining complexity)?
□ Fastener types standardized?
□ Part count vs previous iteration: [count]
Score: [0-4] Evidence: ___

SAFETY (An toàn) — P&B 7.3.3:
□ Direct safety: hazards prevented by design? (Safe-Life / Fail-Safe)
□ Indirect safety: protective systems where direct insufficient?
□ Redundancy type identified for critical functions? (Active/Passive/Principle)
□ Stored energy principle applied where possible?
□ MIL-STD-882E system safety addressed?
□ Bi-stability for ON/OFF states (no ambiguous intermediate)?
Score: [0-4] Evidence: ___
```

### Step B2: 5 Design Principles Check (P&B 7.4)

```
DESIGN PRINCIPLES — {{project}}

FORCE TRANSMISSION (7.4.1) — ĐỒNG-NGẮN-CÙNG-CÂN:
□ Uniform strength — no over/under-stressed sections?
□ Direct/short force path — minimum bending?
□ Matched deformations — compatible stiffness at joints?
□ Balanced forces — internal forces cancel where possible?
Score: [0-4]

DIVISION OF TASKS (7.4.2):
□ One function per component (where practical)?
□ Adjustable separated from fixed?
□ AI-updateable separated from hardware-fixed (DfU)?
Score: [0-4]

SELF-HELP (7.4.3) — TĂNG-CÂN-BẢO:
□ Self-reinforcing: normal forces amplify function?
□ Self-balancing: opposing forces cancel?
□ Self-protecting: overload triggers protection?
Score: [0-4]

STABILITY (7.4.4):
□ Stable equilibrium for normal states?
□ Bi-stable for switching functions?
□ No neutral equilibrium (unpredictable)?
Score: [0-4]

FAULT-FREE DESIGN (7.4.5):
□ Error prevention: physically impossible to assemble wrong?
□ Error tolerance: wide margins absorb variation?
□ Error compensation: auto-calibration where needed?
Score: [0-4]
```

### Step B3: DfX Review (P&B 7.5 — 7 categories)

```
DfX REVIEW — {{project}}
Date: {{today}}

DfM — Design for Manufacture (VN workshop):
| ID | Check | Severity | Status | Notes |
| DfM-01 | Standard sheet sizes available? | | | |
| DfM-02 | Welding access for manual TIG? | | | |
| DfM-03 | CNC tolerances within capability? | | | |
| DfM-04 | Local material sourcing? | | | |
| DfM-05 | Batch size feasible? | | | |

DfA — Design for Assembly (P&B 7.5.9):
| DfA-01 | Assembly sequence defined + unambiguous? | | | |
| DfA-02 | Fastener standardization? | | | |
| DfA-03 | Base-part-up assembly possible? | | | |
| DfA-04 | Sub-assemblies for parallel preassembly? | | | |
| DfA-05 | Cable/connector access without full disassembly? | | | |

DfR — Design for Reliability:
| DfR-01 | IP rating achievable? | | | |
| DfR-02 | MIL-STD-810H vibration/shock? | | | |
| DfR-03 | Corrosion protection (marine/tropical)? | | | |
| DfR-04 | MTBF estimate reasonable? | | | |

DfT — Design for Test:
| DfT-01 | Test points accessible? | | | |
| DfT-02 | Functional test without full assembly? | | | |
| DfT-03 | Field diagnostic capability (BIT)? | | | |

DfW — Design for Waste Reuse (TRIZ #22):
| DfW-01 | Exhaust/gas reusable? | | | |
| DfW-02 | Waste heat reusable? | | | |
| DfW-03 | Vibration byproduct useful? | | | |
| DfW-04 | Data byproduct captured? | | | |

DfU — Design for Update (WX unique — AI/firmware):
| DfU-01 | Firmware update port accessible? | | | |
| DfU-02 | AI model swap without hardware change? | | | |
| DfU-03 | Compute module replaceable path? | | | |
| DfU-04 | Sensor upgrade without enclosure redesign? | | | |
| DfU-05 | OTA update capability? | | | |
| DfU-06 | Model rollback mechanism? | | | |
| DfU-07 | Computational headroom ≥30%? | | | |
| DfU-08 | Data collection port? | | | |
| DfU-09 | Monitoring endpoint? | | | |
| DfU-10 | AI dependency stack documented? | | | |

DfU NOTE: For purely mechanical products → "DfU: N/A — no AI/firmware"

DfMa — Design for Maintenance (P&B 7.5.10):
| DfMa-01 | L1 maintenance no special tools, ≤15 min? | | | |
| DfMa-02 | Wear parts accessible without full disassembly? | | | |
| DfMa-03 | 3-level maintenance philosophy defined? | | | |
| DfMa-04 | Built-in diagnostics for field troubleshooting? | | | |

SUMMARY: OK={{N}} | WARN={{N}} | FAIL={{N}}
Critical FAILs (severity H): [list — must resolve before Phase 4]
```

### Step B4: PLAUSIBLE 9-Check (S1 P47)

```
PLAUSIBLE — {{project}}

P — Physics: Layout obeys physical laws? (thermal, structural, fluid)   [PASS/FLAG/FAIL]
L — Logic: Assembly sequence holds? No impossible ordering?              [PASS/FLAG/FAIL]
A — Assumptions: ALL hidden assumptions listed? (material, tolerance)    [PASS/FLAG/FAIL]
U — Units: All dimensions consistent? (mm throughout)                    [PASS/FLAG/FAIL]
S — Scale: Works at 0.5x and 2x production volume?                     [PASS/FLAG/FAIL]
I — Integration: Compatible with ICD v2? Interfaces achievable?         [PASS/FLAG/FAIL]
B — Boundary: What at max load + max temp + max vibration?             [PASS/FLAG/FAIL]
L — Lethality: If layout WRONG, could someone get hurt?                [PASS/FLAG/FAIL]
E — Endurance: Works in 2 years? (corrosion, fatigue, UV, tropical)    [PASS/FLAG/FAIL]

⚠ L-check (Lethality) FAIL → STOP [SAFETY-CRITICAL-DEFECT]
```

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BB_DfX_Review.md` — full DfX results
- `BB_PLAUSIBLE_Check.md` — 9-check results
- `BB_Basic_Rules_Audit.md` — Clarity/Simplicity/Safety scores

## CEO Checkpoint
```
═══ BLOCK BB DfX REVIEW COMPLETE ═══
Basic Rules: Clarity {{score}}/4, Simplicity {{score}}/4, Safety {{score}}/4
Design Principles: {{avg}}/4 across 5 principles
DfX: OK={{N}} | WARN={{N}} | FAIL={{N}}
PLAUSIBLE: {{N}}/9 PASS, {{N}} FLAG, {{N}} FAIL
Critical items: {{list}}

CEO:
(1) ✅ Approve → tiếp tục Block BC (Integration)
(2) 🔧 Resolve FAIL items, re-run DfX
(3) 🔄 Revise layout (back to Block BA)
(4) ⏸️ Dừng — needs design iteration
```

## COD
- Mass/CoG/interference inputs from geometry-of-record ([[helix-cad-bridge]]/[[helix-cad-ingest]]): Offload (O2) — read from model, not estimated
- DfX checklist execution: Offload (O2) — AI runs systematically
- PLAUSIBLE check: Offload (O2) — AI assesses
- Basic rules audit: Offload (O2) — AI evaluates against criteria
- **FAIL resolution decisions: Core (C)** — CEO judges trade-offs
- **Lethality FAIL response: Core (C)** — immediate CEO attention
