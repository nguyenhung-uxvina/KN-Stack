---
name: helix-p1-requirements
description: "Block A of Phase 1 pipeline — generate 50-80 requirements from 17 P&B categories, standards, similar products, and operational context. AI drafts, CEO validates. P&B 5.2. Can run standalone. Triggers on: 'generate requirements', 'requirements draft', 'req list', 'danh sach yeu cau'."
---

# Block A: Requirements Generation — AI Draft from 16 Categories

> **P&B:** 5.2 (Setting Up a Requirements List) | **Pipeline:** helix-task-clarify → Block BA
> **Input:** `B0_Preflight_Report.md` | **Output:** `BA_Requirements_Draft.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Generate 50-80 requirements from 17 P&B categories | Classify D/W (= BB, CEO Core) |
| Pull requirements from standards + similar products | Abstract problem or find essential problem (= BC) |
| Tag each req with resolution phase [CONCEPT/EMBODY/LATE] | Decompose into sub-functions (= BD) |
| Flag solution ideas → Solution_Ideas_Log (separate) | Evaluate or rank requirements |
| Mark all D/W as [TBD] for CEO in BB | Skip categories — all 17 must appear |

**Multi-Agent Mode:** NO — standard generation task, single agent with reference access.
**CEO Checkpoint:** Review draft count, category coverage, and obvious gaps before D/W classification in BB.

## Standalone Usage
```
/helix-p1-requirements VN-XUONG-UUV
```

## Input Requirements
- `B0_Preflight_Report.md` — stakeholders, standards, scope, task source
- forge-library — similar product requirements
- 3_Resources/Technical-References/ — MIL-STD templates

## Workflow

### Step A1: Apply 17-Category Checklist (P&B Table 5.1 / Figure 5.3)

Generate requirements SYSTEMATICALLY — every category MUST be addressed:

| # | Category | Minimum Items | Focus Areas |
|---|----------|--------------|-------------|
| 1 | Geometry | 3-6 | Dimensions, clearances, footprint, mounting |
| 2 | Kinematics | 2-5 | Motion types, speeds, accelerations, ranges |
| 3 | Forces | 3-7 | Loads, magnitudes, frequencies, safety factors |
| 4 | Energy | 2-4 | Power I/O, efficiency, thermal, consumption |
| 5 | Material | 3-5 | Properties, standards, availability, prohibited |
| 6 | Signals | 2-5 | I/O, displays, controls, data formats, comms |
| 7 | Safety | 4-8 | Fail-safe, hazards, MIL-STD-882E, pinch points |
| 8 | Ergonomics | 3-6 | Human-machine, anthropometry (VN), operation |
| 9 | Production | 3-5 | Workshop capability, tolerances, local content |
| 10 | Quality Control | 2-4 | Inspection, testing, measurability |
| 11 | Assembly | 2-4 | Installation, commissioning, special tools |
| 12 | Transport | 2-4 | Weight, dimensions, packaging, shock rating |
| 13 | Operation | 3-6 | Environment (MIL-STD-810H), modes, sea state |
| 14 | Maintenance | 3-6 | MTBF, 3-level maintenance, intervals, spares |
| 15 | Costs | 3-5 | Unit cost, LCC, NRE, local content %, margin |
| 16 | Schedules | 2-3 | Milestones, lead time, surge capability |
| 17 | Recycling/Disposal | 2-3 | Safe disposal, hazmat, battery handling, material recovery |

**Target: 50-80 requirements total** (fewer = incomplete for defense).

### Step A1b: "Obviously Necessary" Items Check (P&B 5.2)

Before proceeding, prompt for requirements so basic they might be skipped:

```
□ No injury to operator during normal use
□ No injury to bystanders during operation
□ Operable in local climate (VN: tropical, salt air, monsoon)
□ Corrosion resistance for deployment environment
□ Can be manufactured with available workshop capability
□ Can be transported to operational site
□ Complies with applicable safety regulations
□ Can be stored without degradation for expected shelf life
□ Spare parts obtainable within acceptable lead time
```

### Step A1c: Implicit Requirements Discovery (P&B 5.2)

Ask: **"What would customer reject the design for if absent, even though never stated?"**

Scan 6 areas:
1. Safety: What failure modes could injure someone?
2. Environment: What VN conditions are assumed? (humidity, salt, heat)
3. Maintainability: What would make field repair impossible?
4. Usability: What would frustrate a typical VN military operator?
5. Logistics: What would prevent deployment to remote sites?
6. Training: What would require unreasonable training time?

Mark implicit requirements with Source = "Implicit — [discovery area]"

### Step A2: Scenario Method — Life Stage Requirements (P&B 5.2)

For each life stage, ask "What might happen?" → derive requirements:

| Life Stage | Scenario | Requirement Derived |
|-----------|---------|-------------------|
| Production | Component shortage | Alt. supplier identified |
| Transport | Dropped / rough handling | MIL-STD-810H 516.8 shock |
| Installation | Hostile environment | Install time ≤ {{N}} min |
| Operation (normal) | Daily use patterns | Operating temp, humidity |
| Operation (extreme) | Worst-case environment | Salt fog, monsoon, sea state |
| Maintenance L1 | Operator-level | No special tools, ≤15 min |
| Maintenance L2 | Field tech | Standard tools, ≤2 hours |
| Maintenance L3 | Depot/WX | Full overhaul, ≤8 hours |
| Disposal/EOL | End of service | Safe disposal, material recovery |

### Step A3: Import from Similar Products (FORGE Library)

Check forge-library for requirements from similar WX products:
- BB-01 (if acoustic/detection), VN-AST (if marine), VN-CUAV-SIM (if sim), etc.
- Mark reused requirements as `[REUSE: {{source_product}}]`

### Step A4: Three-Step Refinement (P&B 5.2)

For any vague requirement, apply 3-step refinement:
```
Step 1 (Vague):     "Easy maintenance"
Step 2 (Developed): 1. Long interval  2. Easy access  3. Easy to learn
Step 3 (Quantified): 1.1 ≥1000h  1.2 Grease every 3mo  2.1 Hand-open covers
```

**Forbidden terms:** adequate, sufficient, robust, good, high-quality → replace with NUMBERS.

### Step A4b: Partial Requirements Lists (P&B 5.3.2)

Prompt CEO: which stakeholder perspectives have contributed partial requirements?

| Department/Perspective | Focus Area | Partial List? |
|----------------------|-----------|--------------|
| Operations/Users | Ease of use, reliability, training | [Y/N/NA] |
| Procurement | Cost, local content, delivery | [Y/N/NA] |
| Production (WX) | Manufacturability, tolerances, supply | [Y/N/NA] |
| Safety/QC | Fail-safe, hazards, compliance | [Y/N/NA] |
| Maintenance | Intervals, access, spares | [Y/N/NA] |
| Logistics | Transport, packaging, storage | [Y/N/NA] |

For WX solo-CEO: walk through each perspective systematically to avoid blind spots.

### Step A5: Solution-Neutral Check (P&B 5.4)

Scan ALL requirements for solution bias:

| Solution-Specific (WRONG) | Solution-Neutral (CORRECT) |
|--------------------------|--------------------------|
| "Use NVIDIA Jetson" | "Inference ≤30ms, power ≤25W" |
| "Use LoRa 433MHz" | "Range ≥500m, bandwidth ≥1 kbps" |
| "Make from aluminum" | "Yield ≥275 MPa, density ≤2.8 g/cm³" |

**Rule:** Requirements specify WHAT and HOW WELL — never HOW.

### Step A6: Compile Draft

```
REQUIREMENTS LIST — {{project_id}} — DRAFT v0.1
Date: {{today}}
Source: AI-generated from 16 categories + standards + similar products
Status: DRAFT — requires human D/W classification in Block BB

| Req-ID | Category | Requirement | Value | Unit | D/W | Domain | Verify | Standard | Source |
|--------|----------|-------------|-------|------|-----|--------|--------|----------|--------|
| R-001 | Geometry | [requirement] | [value] | [unit] | [TBD] | [Co/Dien/AI] | [I/M/T/A] | [ref] | [source] |
| R-002 | ... | | | | [TBD] | | | | |

D/W COLUMN: All marked [TBD] — CEO classifies in Block BB

IMPLICIT REQUIREMENTS (P&B 5.2 — often missed):
| Req-ID | Requirement | Why implicit | Category |
|--------|-------------|-------------|----------|
| R-0xx | No injury to operator | Safety — assumed but must be stated | Safety |
| R-0xx | Operable in rain | VN tropical — assumed | Operation |

PD REQUIREMENTS (for AI/sensor products):
| Req-ID | Metric | Target@CI | Degradation Bound | Test Sample |
|--------|--------|----------|-------------------|-------------|
```

### Step A7: Requirements Lifecycle Note (VDI 2221:2019)

> **VDI 2221:2019 Co-evolution Principle:** Requirements are NOT static. They co-evolve alongside the design solution. The requirements list is a "living document" — it will be updated in Phase 2 and Phase 3 when concept development and embodiment reveal new needs, changed values, or obsolete requirements.

**Phase Resolution Tags:** Each requirement should indicate when it must be fully resolved:
- `[P1]` — Must be fully specified by end of Phase 1 (task clarification)
- `[P2]` — Can use [TBD] placeholder; resolved during conceptual design
- `[P3]` — Can use [TBD] placeholder; resolved during embodiment (e.g., exact dimensions)
- `[P4]` — Resolved during detail design (e.g., GD&T tolerances)

Requirements tagged `[P2]`/`[P3]`/`[P4]` are "Binding Yet Provisional" (P&B 5.3.1) — they exist as commitments but their exact values may change. Changes are tracked in `Requirements_Delta_Log.md` created in Phase 2/3.

### ICDM Extension (if --icdm active)
- Innovation KPI requirements (novel feature count, patent potential)
- Collaboration metric requirements (stakeholder engagement frequency)
- TRIZ resource inventory (available resources in system environment)

## Output

Save to `1_Projects/{{project}}/Phase1-Task/BA_Requirements_Draft.md`

## CEO Checkpoint

```
═══ BLOCK BA REQUIREMENTS GENERATION COMPLETE ═══
Total requirements: {{N}} across {{M}}/17 categories
From standards: {{N}} | From similar products: {{N}} | New: {{N}}
Implicit found: {{N}} | Solution-biased removed: {{N}}
D/W status: ALL [TBD] — CEO classifies in Block BB

CEO:
(1) ✅ Approve draft → tiếp tục Block BB (Validate & Classify)
(2) ➕ Bổ sung requirements từ field experience
(3) 🔄 Chạy lại — thiếu category {{X}}
(4) ⏸️ Dừng — cần stakeholder input trước
```

## COD
- 16-category systematic generation: Offload (O1)
- Standards-based requirements: Offload (O1) — AI templates
- Similar product import: Offload (O1) — AI cross-references
- Solution-neutral check: Offload (O2) — AI flags bias
- D/W classification: **FORBIDDEN for AI** — always [TBD]
- Field/operator knowledge: **Core (C)** — CEO adds in BB
