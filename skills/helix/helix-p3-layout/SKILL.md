---
name: helix-p3-layout
description: "Block A of Phase 3 pipeline — CEO creates preliminary layout (Core, non-delegable), maritime auto-invoke P50 stability + P51 weight estimate, main function carrier development. P&B 7.1 Steps 2-6. Can run standalone. Triggers on: 'preliminary layout', 'create layout', 'P50 stability', 'P51 weight', 'main function carriers'."
---

# Block A: Layout — Preliminary Design (CEO Core + Maritime Checks)

> **P&B:** 7.1 (Steps 2-6) | **Pipeline:** helix-embody-realize → Block BA
> **Input:** `B0_Preflight_Report.md` + Phase 2 concept | **Output:** `BA_Preliminary_Layout.md` + maritime files

## Operational Envelope
> Source: [[Operational Envelope Law]] + [[LLM Spatial Blindness]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Document CEO's layout decisions | Generate spatial arrangement or layout |
| Check dimensional constraints vs requirements | Suggest component placement |
| Run maritime P50 stability + P51 weight | Override CEO's spatial judgment |
| Flag conflicts between layout and requirements | Skip CEO layout — go straight to DfX |
| Validate material compatibility | Assume LLM can "see" 3D relationships |

**Multi-Agent Mode:** NO — CEO Core. LLM fundamentally lacks 3D spatial cognition (100% geometry failure in research). AI documents and validates constraints, NEVER generates layout.
**CEO Checkpoint:** CEO IS the block. AI assists with constraint checking only.
**LLM Spatial Blindness Gate:** Any AI output containing spatial terms = LOW CONFIDENCE, must be verified on physical sketch/CAD.
- **Trigger words:** above, below, left, right, adjacent, next to, perpendicular, parallel, behind, opposite, between, centered, aligned, offset, flush, coaxial, concentric
- LLMs systematically misinterpret descriptive spatial terms (Cambridge: 100% geometry failure on right-angle precision)
- If AI generates text with ≥2 trigger words in same paragraph → auto-flag `[SPATIAL — CEO VERIFY]`

## Workflow

### Step A1: CEO Creates Preliminary Layout (Core — NON-DELEGABLE)

> **Rule:** AI NEVER generates the initial layout. This is design judgment. See [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]].

CEO provides:
- Hand sketches or CAD rough layout
- Key dimensional decisions (envelope, mounting points)
- Material candidates for primary structure
- Component placement rationale
- Assembly concept (how it goes together)

AI documents what CEO provides:
```
PRELIMINARY LAYOUT — {{project}}
Date: {{today}}
Source: CEO sketch/CAD [reference]

Main Function Carriers:
| MFC-ID | Function | Component(s) | Material | Key Dimensions |
|--------|----------|-------------|----------|----------------|

Layout Decisions:
| Decision | Rationale | Alternative Considered |
|----------|----------|----------------------|

SPATIAL ALLOCATION: [CEO INPUT ONLY — AI documents, does NOT generate]
[CEO describes arrangement of main function carriers in envelope]
[AI transcribes verbatim. Any spatial description here MUST come from CEO sketch/CAD, not AI inference.]
```

### Step A2: Develop Main Function Carriers (P&B 7.1 Steps 3-5)

> **Spatial Guard:** AI assists with material, dimensions, manufacturing — NOT spatial form. Any form description (shape, geometry, orientation) must reference CEO's sketch/CAD. AI outputs "per CEO sketch: ..." not "component should be..."

For each main function carrier:
- Preliminary form design (shapes, interfaces) — **reference CEO sketch**
- Key dimensions from requirements
- Material selection rationale
- Manufacturing method assumption

### Step A3: Auxiliary Function Solutions (P&B 7.1 Step 7)

> **Spatial Guard:** Cable routing, thermal paths, and component retention are inherently spatial. AI lists options and constraints — CEO decides routing and placement. AI outputs "Options: X, Y, Z — CEO selects and sketches routing."

Identify and solve auxiliary functions:
- Sealing, cooling, retention, support, cable routing — **CEO sketches spatial paths**
- Fastener standardization
- Adjustment mechanisms

### Step A4: Maritime Auto-Invoke (if --maritime or product is vessel/USV/buoy)

**P51 Weight Estimate:**
```
WEIGHT ESTIMATE — {{project}}
| Subsystem | Item | Material | Qty | Unit Wt | Total | Confidence |
|-----------|------|----------|-----|---------|-------|-----------|
| Structure | | | | | | [L1-L5] |
| Propulsion | | | | | | |
| Electrical | | | | | | |
| Payload | | | | | | |
| Outfit | | | | | | |
| SUBTOTAL | | | | | | |
| Margin (10-15%) | | | | | | |
| TOTAL | | | | | | |
```

**P50 Stability Check:**
```
STABILITY CHECK — {{project}}
| Condition | Displacement | GM | Trim | Freeboard | Status |
|-----------|-------------|----|----|-----------|--------|
| Lightship | | | | | |
| Half-load | | | | | |
| Full-load | | | | | |
| Worst-case | | | | | |

GM minimum: ≥ 0.5m ALL conditions
Trim freeboard minimum: ≥ 0.3m
```

**Gate:** GM < 0.5m → STOP [STABILITY-FAIL]. Weight > SWL → [OVERWEIGHT-RISK].

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BA_Preliminary_Layout.md`
- `BA_Weight_Estimate.md` (maritime only)
- `BA_Stability_Check.md` (maritime only)

## CEO Checkpoint
```
═══ BLOCK BA LAYOUT COMPLETE ═══
Main function carriers: {{N}} defined
Auxiliary functions: {{N}} solved
Maritime: [P50/P51 PASS / N/A]
Key layout decisions: {{N}} documented

CEO:
(1) ✅ Approve layout → tiếp tục Block BB (DfX Review)
(2) 🔄 Revise layout
(3) ⏸️ Dừng — need CAD iteration
```

## COD
- **Layout creation: Core (C)** — non-delegable, CEO judgment
- Layout documentation: Offload (O1) — AI records
- P50/P51 calculations: Offload (O2) — AI computes
- **Layout approval: Core (C)**
