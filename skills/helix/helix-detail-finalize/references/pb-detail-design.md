# Pahl-Beitz Detail Design — Phase 4 Reference

Source: P&B Ch7.6-7.8 (Evaluation, Examples, Detail Design)

## 5-Step Detail Design Process (P&B Fig 7.164)

```
[1] Finalize definitive layout
    → Final dimensions, tolerances, surface finishes
    → Material grades confirmed (not just "steel" → "AISI 4140 QT HRC 28-32")

[2] Integrate into overall layout drawings
    → Assembly drawings with all components
    → Interference/clearance checks complete
    → Exploded views for complex assemblies

[3] Complete production documents
    → Individual part drawings with GD&T
    → Final BOM with part numbers, suppliers, costs
    → Assembly instructions (step-by-step)
    → Inspection checklist per part

[4] Check all documents
    → Standards compliance (ISO 128, TCVN, MIL-STD)
    → Dimension chains verified
    → Tolerance stack-up analysis
    → Drawing cross-references consistent

[5] Documentation and decision
    → Complete production package released
    → Gate 4 review
    → Workshop master sign-off
```

## Drawing Standards

### GD&T Symbols (ISO 1101 / ASME Y14.5)

| Symbol | Meaning | When to Apply |
|--------|---------|---------------|
| ⊕ | Position | Hole patterns, mounting points |
| ⊖ | Concentricity | Rotating parts, shafts |
| ∥ | Parallelism | Mating surfaces |
| ⊥ | Perpendicularity | Reference surfaces |
| ⌒ | Profile | Complex curves, fairings |
| ○ | Circularity | Bores, cylinders |
| ◎ | Total runout | Assembled rotating parts |

### Tolerance Grades (ISO 286)

| Fit Type | Application | Ví dụ |
|----------|-------------|-------|
| H7/g6 | Sliding fit | Piston in bore |
| H7/k6 | Transition fit | Bearing housing |
| H7/p6 | Press fit | Shaft coupling |
| H11/c11 | Clearance fit | Cover on housing |

### Surface Finish (Ra values)

| Ra (μm) | Surface | Application |
|----------|---------|-------------|
| 0.4 | Ground/polished | Bearing surfaces, seals |
| 0.8 | Fine machined | Precision fits |
| 1.6 | Machined | General mating surfaces |
| 3.2 | Rough machined | Non-critical surfaces |
| 6.3 | As-cut | Structural, no contact |
| 12.5 | As-welded | Weldments (cleaned) |

## BOM Structure

### Level Format
```
Level 0: Complete Product Assembly
├── Level 1: Major Sub-assemblies
│   ├── Level 2: Sub-sub-assemblies
│   │   └── Level 3: Individual Parts
│   └── Level 2: Purchased Items
└── Level 1: Consumables/Wear Parts
```

### BOM Entry Fields
```
Part # | Description | Material | Qty | Source | Unit Cost | Lead Time | Drawing #
```

**Source codes:**
- M = Make (workshop fabrication)
- B = Buy (off-the-shelf)
- S = Subcontract (outsource fabrication)
- A = Assembly (combine M/B/S parts)

## Inspection Checklist Template

| # | Feature | Nominal | Tolerance | Method | Instrument | Accept/Reject |
|---|---------|---------|-----------|--------|------------|---------------|
| 1 | OD shaft | 25.000 | ±0.013 (h6) | Measure | Micrometer | |
| 2 | Bore | 25.021 | +0.021/0 (H7) | Measure | Bore gauge | |
| 3 | Surface Ra | 0.8 | max | Compare | Surface comp. | |
| 4 | Hardness | HRC 30 | ±2 | Test | Rockwell | |

## Assembly Instruction Format

```
Step [N]: [Action verb] [component] [to/into/onto] [target]
         Tool: [required tool]
         Torque: [if fastener, specify Nm]
         Note: [special instruction if any]
         Check: [verification after step]
```

### Example:
```
Step 3: Insert bearing (P/N BB-01-023) into housing bore (P/N BB-01-001)
        Tool: Bearing press, arbor #3
        Note: Cool bearing to -20°C before insertion (shrink fit)
        Check: Bearing seated flush ±0.1mm with housing face
```

## Workshop X Production Standards

- Drawing format: A3 landscape preferred, A4 for simple parts
- Language: English for dimensions/notes, Vietnamese for assembly instructions
- File format: DXF/PDF for workshop, native CAD for archive
- Revision control: Rev A, B, C... (never Rev 1, 2, 3)
- Critical dimensions: **BOXED** on drawing (ISO convention)
