---
name: helix-p4-drawing
description: "Block A of Phase 4 pipeline — CEO specifies critical GD&T/surface finish/weld specs/connector pinouts/PCB layout (Core, non-delegable), AI completes 3D model manufacturing features + generates 2D production drawings per ISO 128 / TCVN, exploded views, PCB Gerber checklist, drawing index. P&B 9.2-9.3. Can run standalone. Triggers on: 'Phase 4 drawing', 'manufacturing drawings', 'GD&T', 'final CAD'."
---

# Block A: Drawing — Final CAD + Production Drawings

> **P&B:** Chapter 9 § 9.2-9.3 | **Pipeline:** helix-detail-finalize → Block BA
> **Input:** B0 detail-determining list + frozen requirements | **Output:** `Manufacturing_Drawings/` + `BA_Drawing_Index.md`
> **Standards:** ISO 128 (technical drawings) + TCVN 7283 + ASME Y14.5 (GD&T)

## Operational Envelope

| DO | DON'T |
|----|----|
| AI completes manufacturing features (fillets/chamfers/drafts) | AI decides critical dimensions (= CEO Core) |
| Generate 2D drawings per ISO 128/TCVN | Generate BOM (= BB) |
| Exploded views for assembly reference | Inspection criteria (= BC) |
| PCB Gerber preparation checklist | Workshop master review (= BE, CEO Core) |
| Drawing index + revision control | Vendor selection (= BB, CEO Core) |

**Multi-Agent Mode:** Optional — parallel agents per subsystem (mech/elec/PCB) when ≥3 subsystems.
**CEO Checkpoint:** Approve critical GD&T spec table + drawing first-pass review.

## Workflow

### Step A.1: CEO Critical Spec Table (CORE — Non-Delegable)

**AI presents template, CEO fills.** AI does NOT propose values for critical specs — manufacturing experience required.

```
CRITICAL SPECS — {{project}}
Date: {{today}}
CEO/Workshop Master: __________________

GD&T ON CRITICAL DIMENSIONS:
| Component | Datum | Dim | Tolerance | Form | Position | Notes |
|----|----|----|----|----|----|----|

SURFACE FINISH (functional surfaces only):
| Component | Surface | Ra (μm) | Method | Inspection |
|----|----|----|----|----|

WELDS (defense quality):
| Joint | Process | Filler | Size | NDT level | Standard |
|----|----|----|----|----|----|

CONNECTOR PINOUTS:
| Connector | Pin | Signal | Voltage | Spec | Reference |
|----|----|----|----|----|----|

PCB LAYOUT APPROVAL:
| Layer | Trace width | Spacing | Via | Stackup | Approver |
|----|----|----|----|----|----|
```

### Step A.2: AI Completes 3D Model

> **3D source:** the parametric model comes from `helix-cad-bridge` (code-CAD `.py` → STEP, git source of truth from Phase 3). Manufacturing features below are added by editing those parameters/script and re-exporting STEP — not by redrawing. Keeps drawing ↔ model single-sourced and rev-tracked.

From CEO spec + frozen layout:

```
3D MODEL COMPLETION — {{project}}
For each mechanical part:
  □ Manufacturing features added (fillets, chamfers, drafts)
  □ Material assigned (matches BOM)
  □ Mass properties calculated
  □ Interference check vs assembly
  □ Section views for internal features
```

### Step A.3: 2D Production Drawings (ISO 128 / TCVN)

For each manufactured part:

```
DRAWING — {{part_id}} Rev v1.0
□ Title block (project, part name, material, scale, drawn by, date, rev)
□ Views: front + top + side + isometric (minimum)
□ Section views for internal features
□ All dimensions with tolerances
□ GD&T per CEO spec table
□ Surface finish symbols on functional surfaces
□ Weld symbols per AWS A2.4 / TCVN
□ Notes (material, heat treatment, finish, inspection)
□ Drawing number, revision, sheet count
□ TCVN/ISO 128 format compliance
```

For each PCB:
```
□ Schematic exported (sch)
□ Layout final (pcb)
□ Gerber files (top, bottom, drill, soldermask, silkscreen)
□ Pick & Place file
□ Stackup specification
□ DFM check report
```

### Step A.4: Exploded Views + Assembly Reference

```
□ Top-level exploded view (whole product)
□ Subassembly exploded views
□ Part labels matching BOM Part Number
□ Assembly sequence callouts (links to BD assembly instructions)
```

### Step A.5: Drawing Index + Revision Control

`BA_Drawing_Index.md`:

| Drawing No | Part Name | Rev | Date | Format | File | Status |
|----|----|----|----|----|----|----|
| {{prefix}}-M-001 | [name] | v1.0 | {{today}} | DXF+PDF | path | DRAFT |

Revision rules:
- Pre-fabrication: v1.0 DRAFT
- After workshop master review (BE): v1.0 RELEASED
- Production changes: v1.1, v1.2 — never overwrite v1.0

## Output

Save to `1_Projects/{{project}}/Phase4-Detail/{{variant}}/`:
- `Manufacturing_Drawings/` (DXF + PDF per part)
- `Schematics/` (PCB schematics)
- `Gerber/` (PCB production files)
- `BA_Drawing_Index.md` (complete index with rev tracking)

## CEO Checkpoint

```
═══ BLOCK BA DRAWING COMPLETE ═══
Drawings: {{N}} mech + {{N}} elec + {{N}} PCB
Critical specs: GD&T {{N}} + Surface {{N}} + Weld {{N}} + Conn {{N}} + PCB {{N}}
Standard: ISO 128 / TCVN 7283 / AWS A2.4

CEO:
(1) ✅ Approve → tiếp tục Block BB (Final BOM)
(2) 🔄 Revise critical specs (CORE adjustment)
(3) ⏸️ Dừng — review drawings physically before BOM
```

## COD

- 3D model completion (defined geometry): Offload (O1)
- 2D drawing generation from 3D: Offload (O1)
- Exploded views + indexing: Offload (O1)
- PCB Gerber prep: Offload (O1) — AI runs DFM, CEO approves stackup
- **GD&T on critical dimensions: Core (C)** — manufacturing experience
- **Surface finish on functional surfaces: Core (C)**
- **Weld NDT level: Core (C)** — defense quality judgment
- **Connector pinout final: Core (C)** — interface contract
- **PCB layout approval: Core (C)** — EMC/thermal judgment
