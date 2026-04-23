---
name: helix-p1-structure
description: "Block D of Phase 1 pipeline — generate 6-flow function structure (E-M-S + Data-Compute-Trust), decompose into sub-functions, assess design type (Original/Adaptive/Variant). P&B 6.3. Can run standalone. Triggers on: 'function structure', 'sub-functions', 'design type', 'cau truc chuc nang', '6-flow'."
---

# Block D: Function Structure — 6-Flow Decomposition + Design Type

> **P&B:** 6.3 (Function Structures) | **VDI 2221:2019:** Functional Architecture (solution-neutral) | **Pipeline:** helix-task-clarify → Block BD
> **Input:** `BC_Essential_Problem.md`, `BB_Requirements_List_v1.md` | **Output:** `BD_Function_Structure.md`, `BD_Design_Type.md`
> **Galaxy:** [[Solution-Determining Subfunction]], [[Variation vs Simplification]]

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Generate 6-flow function structure (E-M-S + Data-Compute-Trust) | Search working principles (= Phase 2 BB) |
| Decompose overall function into sub-functions | Evaluate or rank solutions (= Phase 2 BC) |
| Identify solution-determining sub-function | Create physical layout (= Phase 3 BA) |
| Assess design type (Original/Adaptive/Variant) | Skip 6-flow — use only E-M-S 3-flow |
| Verify all SFs appear as potential morpho rows | Embed solutions in function names |

**Multi-Agent Mode:** NO — function decomposition is a structured logical task, single agent sufficient. Multi-perspective analysis starts in Phase 2 BA (solution-determining SF scoring).
**CEO Checkpoint:** Validate function structure completeness and solution-determining SF identification.

## Standalone Usage
```
/helix-p1-structure VN-XUONG-UUV
```

## Input Requirements
- `BC_Essential_Problem.md` — CEO-approved EP
- `BB_Requirements_List_v1.md` — validated requirements (domain tags)
- `B0_Preflight_Report.md` — multi-domain status

## Workflow

### Step D1: Overall Function Black-Box (P&B 6.3.1)

State the overall function as an E/M/S transformation BEFORE decomposing:

```
OVERALL FUNCTION — {{project_id}}

Energy INPUT:   [power sources, kinetic energy, thermal, ...]
Material INPUT: [raw materials, consumables, ammunition, ...]
Signal INPUT:   [commands, sensor data, user input, ...]

       ┌────────────────────────┐
       │   OVERALL FUNCTION     │
       │   (verb + noun)        │
       │   = Essential Problem  │
       └────────────────────────┘

Energy OUTPUT:   [mechanical action, heat, electrical, ...]
Material OUTPUT: [product, waste, debris, ...]
Signal OUTPUT:   [actuation commands, display, data logs, ...]

SYSTEM BOUNDARY: [what's inside vs outside]
```

**Solution-neutral test:** Can ≥3 different internal structures achieve this overall function?
If NO → statement is too specific, re-abstract before proceeding to decomposition.

> **VDI 2221:2019 Terminology:** What P&B calls "function structure" is termed **"functional architecture"** (Funktionale Architektur) in VDI 2221:2019 — defined as a "solution-neutral description of purely functional relationships using a set of interconnected functions and sub-functions." This aligns with the RFLP framework: **R**equirements (Phase 1 BA-BB) → **F**unctional (this block BD) → **L**ogical (Phase 2 concepts) → **P**hysical (Phase 3 embodiment). The function structure is the F layer — it bridges what the product must do (R) with how it might do it (L).

### Step D2: 6-Flow Decomposition

```
6-FLOW FUNCTION STRUCTURE — {{project_id}}
Date: {{today}}

ENERGY FLOWS (E):
  Input:     [power source, kinetic, thermal, ...]
  Transform: [convert, transmit, regulate, dissipate, ...]
  Output:    [mechanical action, heat, electrical, ...]

MATERIAL FLOWS (M):
  Input:     [raw materials, consumables, ammunition, ...]
  Transform: [shape, move, store, separate, ...]
  Output:    [product, waste, debris, ...]

SIGNAL FLOWS (S):
  Input:     [sensor data, commands, user input, ...]
  Transform: [process, filter, decide, display, ...]
  Output:    [actuation, display, logging, ...]

DATA FLOWS (D) — Workshop X extension:
  Input:     [raw sensor data, measurements, ...]
  Transform: [aggregate, clean, format, ...]
  Output:    [structured data, telemetry, ...]

COMPUTATION FLOWS (C) — Workshop X extension:
  Input:     [data, model parameters, ...]
  Transform: [infer, classify, predict, ...]
  Output:    [decisions, alerts, recommendations, ...]

TRUST FLOWS (T) — Workshop X extension:
  Input:     [calibration data, validation evidence, ...]
  Transform: [verify, certify, audit, ...]
  Output:    [confidence level, compliance status, ...]

NOTE: D/C/T flows only for products with AI/software. Pure mechanical = E+M+S only.
```

### Step D3: Sub-Function Decomposition

```
SUB-FUNCTION TABLE — {{project_id}}

| SF-ID | Sub-Function (verb+noun) | Primary Flow | Domain | Requirements Traced | Notes |
|-------|-------------------------|-------------|--------|-------------------|-------|
| SF-01 | [verb + noun] | [E/M/S/D/C/T] | [Co/Dien/AI] | [R-xxx, R-xxx] | |
| SF-02 | [verb + noun] | | | | |
| ... | | | | | |

DECOMPOSITION RULES (P&B 6.3.2-6.3.3):
  □ Main flows decomposed first, auxiliary flows second
  □ Solution-neutral language (verbs from P&B library)
  □ Generally-valid functions where possible (catalogue access)
  □ Task-specific functions where no standard equivalent
  □ Each SF traces to ≥1 requirement
  □ All E-M-S (and D-C-T if applicable) flows accounted for
  □ No premature solution bias in SF names
```

**Function Verb Library:** Convert, Transform, Transmit, Store, Separate, Connect, Channel, Rectify, Amplify, Reduce, Sense, Display, Process, Control, Regulate, Vary, Guide, Distribute, Retain, Hold, Buffer, Detect, Measure, Monitor, Capture.

### Step D4: Design Type Assessment

> **Galaxy:** [[Variation vs Simplification]]

```
DESIGN TYPE ASSESSMENT — {{project_id}}

| Criterion | Assessment | Score (1-5) |
|----------|-----------|-------------|
| Problem novelty | [entirely new / partially new / known] | |
| Precedent products | [none / partial / full precedent exists] | |
| Function structure novelty | [all SFs new / some new / all known] | |
| Solution principles known | [unknown / some known / all known] | |
| Manufacturing familiarity | [unfamiliar / partially / WX experienced] | |

TOTAL SCORE: __ / 25
  20-25: VARIANT — minimal decomposition, document what exists
  12-19: ADAPTIVE — deep on novel SFs, shallow on known
   5-11: ORIGINAL — deep decomposition everywhere

DESIGN TYPE: [Original / Adaptive / Variant]
IMPLICATION FOR PHASE 2: [decomposition depth strategy]
```

### Step D5: Solution-Determining SF Identification (Preview)

Early identification for Phase 2 planning:

```
SOLUTION-DETERMINING SF CANDIDATES — {{project_id}}

Which SF, when its working principle is chosen, cascades through entire design?

| SF-ID | Sub-Function | Cascade Potential | Novelty | Candidate? |
|-------|-------------|------------------|---------|-----------|

PRELIMINARY: SF-{{XX}} — "{{name}}" appears solution-determining.
(Confirmed in Phase 2, Block BA)
```

### ICDM Extension (if --icdm active)
- Innovation flow (7th flow) in function structure
- Innovation potential mapping per SF

## Output

Save to `1_Projects/{{project}}/Phase1-Task/`:
- `BD_Function_Structure.md` — 6-flow decomposition with SF table
- `BD_Design_Type.md` — Original/Adaptive/Variant assessment

## CEO Checkpoint

```
═══ BLOCK BD FUNCTION STRUCTURE COMPLETE ═══
Sub-functions: {{N}} identified across {{M}} flows
Domains: Co({{n}}) / Dien({{n}}) / AI({{n}})
Design Type: [Original / Adaptive / Variant]
Solution-determining SF (preliminary): SF-{{XX}}

CEO:
(1) ✅ Approve → tiếp tục Block BE (Compile & Sync)
(2) 🔄 Adjust SF decomposition
(3) 🔄 Change design type classification
(4) ⏸️ Dừng — cần review function structure deeper
```

## COD
- 6-flow decomposition: Offload (O2) — AI drafts from EP + requirements
- SF identification: Offload (O2) — AI proposes
- **Function structure validation: Core (C) — CEO confirms SFs correct**
- **Design type decision: Core (C) — CEO classifies**
- Solution-determining SF: Offload (O2) preview / **Core (C)** confirmed in Phase 2
