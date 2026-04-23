---
name: helix-p3-preflight
description: "Block 0 of Phase 3 pipeline — verify Phase 2 complete + Gate 2 passed, identify embodiment-determining requirements (size/arrangement/material), map spatial constraints, confirm layout strategy. P&B 7.1 Step 1-2. Can run standalone. Triggers on: 'Phase 3 preflight', 'embodiment inputs', 'spatial constraints'."
---

# Block 0: Pre-Flight — Phase 2 Verification + Embodiment Constraints

> **P&B:** 7.1 (Steps 1-2) | **Pipeline:** helix-embody-realize → Block B0
> **Input:** Phase 2 deliverables | **Output:** `B0_Preflight_Report.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Verify Phase 2 complete + Gate 2 passed | Create preliminary layout (= BA, CEO Core) |
| Identify embodiment-determining requirements | Run DfX review (= BB) |
| Map spatial constraints from requirements | Freeze ICDs (= BC) |
| Confirm layout strategy with CEO | Generate BOM (= BD) |
| Check if SA_System_Architecture exists (mechatronic) | Start embodiment without concept selection |

**Multi-Agent Mode:** NO — simple verification, single agent sufficient.
**CEO Checkpoint:** Confirm layout strategy and embodiment-determining requirements before BA starts.

## Workflow

### Step 0.1: Verify Phase 2 Complete
```
□ BE_Concept_Selection.md exists — CEO chose concept
□ BE_Handoff_Package.md exists — weak spots tracker, traceability
□ BC_VDI_2225_Evaluation.md exists — scores recorded
□ BB_Morphological_Matrix.md exists — selected path highlighted
□ ICD v2 exists — concept-specific interfaces
□ Gate 2 PASSED (date: ______)
```

### Step 0.2: Identify Embodiment-Determining Requirements (P&B 7.1 Step 1)

Three categories that CONSTRAIN the layout:

```
EMBODIMENT-DETERMINING REQUIREMENTS — {{project}}

SIZE-DETERMINING (control envelope):
| Req-ID | Requirement | Value | Implication |
|--------|-------------|-------|-------------|
| [from Phase 1] | [req] | [value] | [constrains overall size] |

ARRANGEMENT-DETERMINING (control topology):
| Req-ID | Requirement | Value | Implication |
| [from Phase 1] | [flow direction, position, interfaces] | | |

MATERIAL-DETERMINING (control material selection):
| Req-ID | Requirement | Value | Implication |
| [from Phase 1] | [corrosion, service life, standards] | | |
```

### Step 0.3: Spatial Constraints

```
SPATIAL CONSTRAINTS — {{project}}
Installation envelope: [L×W×H max]
Interface positions: [deck bolts, connectors, cable routing]
Clearance requirements: [recoil path, operator access, maintenance]
Environmental zones: [wet/dry, hot/cold, EMC sensitive]
```

### Step 0.4: Layout Strategy

Based on design type (from Phase 2) and constraints:
- Original: full layout exploration needed
- Adaptive: modify existing layout for new subsystems
- Variant: parametric changes to proven layout

### Step 0.X: Contextual Factors Check (VDI 2221 Blatt 2)

Verify Phase 1 contextual factors are still valid for Phase 3. Embodiment design is the most resource-intensive phase — wrong pipeline mode here is expensive.

```
CONTEXTUAL FACTORS UPDATE — {{project_id}} Phase 3
Date: {{today}}

Changes since Phase 2:
  □ Supplier availability changed? [YES: describe / NO]
  □ Manufacturing capability updated? [YES: describe / NO]
  □ Budget revised? [YES: describe / NO]
  □ Timeline shifted? [YES: describe / NO]
  □ Integration complexity changed? [YES: more domains / NO]

If any YES → recommend mode adjustment (e.g., --quick → standard, or vice versa).
```

> **VDI 2221:2019 Blatt 2:** Context-specific adaptation is not a one-time activity — it must be revisited as the project evolves.

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/B0_Preflight_Report.md`

## CEO Checkpoint
```
═══ BLOCK B0 PRE-FLIGHT COMPLETE ═══
Embodiment-determining: {{N}} size + {{N}} arrangement + {{N}} material
Spatial envelope: {{L×W×H}}
Layout strategy: [Original/Adaptive/Variant approach]

CEO:
(1) ✅ Approve → tiếp tục Block BA (Layout Creation)
(2) 🔄 Adjust constraints
(3) ⏸️ Dừng — Phase 2 deliverables incomplete
```

## COD
- Input verification: Offload (O1)
- Constraint identification: Offload (O2)
- **Layout strategy decision: Core (C)**
