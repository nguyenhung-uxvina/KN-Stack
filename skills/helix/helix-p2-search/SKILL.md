---
name: helix-p2-search
description: "Block B of Phase 2 pipeline — search working principles (7 methods), DSO pre-ranking, build morphological matrix, verify compatibility (8 types), combine into ≥3 concept variants, human creative input. Can run standalone. Triggers on: 'working principles', 'morphological matrix', 'solution search', 'WP search', 'DSO ranking', 'compatibility'."
---

# Block B: Solution Search — Working Principles + Morphological Matrix

> **P&B:** 6.4 | **Pipeline:** helix-concept-generate → Block BB
> **Input:** `BA_Problem_Frame.md` + Phase 1 Function Structure | **Output:** `BB_Morphological_Matrix.md`, `BB_Concept_Variants.md`
> **Galaxy:** [[DSO Pre-Ranking]], [[Interface Ownership]], [[TRIZ × Pahl-Beitz]]
> **Reference:** `helix-concept-generate/references/pb-conceptual-design.md`, `triz-40-principles.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Search WPs using 7 methods per sub-function | Evaluate/rank concepts (= BC) |
| DSO pre-ranking per sub-function | Eliminate WPs without DSO scoring |
| Build morphological matrix | Select final concept (= BE, CEO Core) |
| Verify compatibility (8 types) | Skip compatibility check |
| Combine into ≥3 concept variants | Limit to 1 concept variant |
| Request CEO creative input | Generate layout/spatial arrangement |

**Multi-Agent Mode:** YES — SBCE parallel WP exploration (highest value block for multi-agent)
- 3 domain agents (Mech/Elec/AI-SW) each explore WPs for their sub-functions independently
- Merge into unified morphological matrix at intersection
- Expect: more cross-domain hybrid WPs but shallower individual detail
- Use for RED/AMBER complexity designs. GREEN complexity = single agent sufficient.

**CEO Checkpoint:** Block boundary (output: BB_Morphological_Matrix.md + BB_Concept_Variants.md). CEO reviews variants + adds creative combinations.

## Standalone Usage
```
/helix-p2-search VN-XUONG-UUV
```

## Input Requirements
- `BA_Problem_Frame.md` — solution-determining SF, decomposition strategy, essential problems
- `Function_Structure.md` — sub-functions list
- forge-library — existing WPs for reuse (marked L)
- forge-shift — ACH go/no-go

## Workflow

### Step B1: Working Principles Search (7 Methods + Multi-Perspective)

**Multi-Agent Selectivity check:** For solution-determining SFs (from BA) with AMBER/RED complexity → activate SBCE-style multi-perspective search via `/helix-domain-debate`. For GREEN SFs → single-agent search (standard).

**For AMBER/RED SFs — SBCE Multi-Perspective Search:**

Run `/helix-domain-debate` with question: "Search working principles for SF-{{X}} from YOUR domain's perspective. What solutions does YOUR domain offer that other domains might not consider?"

Each domain explores INDEPENDENTLY, then merge:

```
SBCE MULTI-PERSPECTIVE WP SEARCH — {{project_id}} / SF-{{X}} {{name}}
Date: {{today}}

═══ MECHANICAL PERSPECTIVE WPs ═══
(Focus: materials, geometry, mechanisms, manufacturing, physical effects)
| WP-ID | Principle | Method | Source | TRL | Perspective |
|-------|-----------|--------|--------|-----|-------------|
| WP-M01 | {{mech solution}} | M3/M5 | {{source}} | {{TRL}} | MECH |

═══ ELECTRICAL PERSPECTIVE WPs ═══
(Focus: power electronics, sensors, signal processing, EMC, actuators)
| WP-ID | Principle | Method | Source | TRL | Perspective |
|-------|-----------|--------|--------|-----|-------------|
| WP-E01 | {{elec solution}} | M1/M6 | {{source}} | {{TRL}} | ELEC |

═══ AI/SW PERSPECTIVE WPs ═══
(Focus: algorithms, AI models, sensor fusion, control logic, data-driven approaches)
| WP-ID | Principle | Method | Source | TRL | Perspective |
|-------|-----------|--------|--------|-----|-------------|
| WP-S01 | {{sw solution}} | M7/M1 | {{source}} | {{TRL}} | AI/SW |

═══ CROSS-DOMAIN HYBRID WPs (intersection discoveries) ═══
| WP-ID | Principle | Domains Combined | How Hybrid Works | Perspective |
|-------|-----------|-----------------|-----------------|-------------|
| WP-H01 | {{hybrid approach}} | Mech+Elec / Mech+AI / Elec+AI | {{integration}} | [HYB] |

MERGE INTO UNIFIED TABLE:
```

**Then merge all WPs into standard morpho matrix format below.**

**For GREEN SFs — Standard Single-Agent Search:**

For each SF (depth per BA strategy), search using ≥3 of 7 methods:

```
WORKING PRINCIPLES SEARCH — {{project_id}}
Date: {{today}}

7 METHODS: M1=Literature, M2=Natural systems, M3=Known products, M4=Analogies,
           M5=Physical effects, M6=Classification schemes, M7=TRIZ principles

| SF-ID | Sub-Function | Method | WP-ID | Principle | Physical Effect | Source | TRL | Local % | ACH? | Perspective | Adv | Disadv |
|-------|-------------|--------|-------|-----------|----------------|--------|-----|---------|------|------------|-----|--------|

NEW COLUMN: "Perspective" = MECH / ELEC / AI-SW / HYB / SINGLE (for GREEN SFs)
```

INTERFACE OWNERSHIP CHECK: Before each SF, ask "Can this function be pushed across system boundary?"

FLAGS:
  ⚠ SF with < 3 WPs → widen search
  ⚠ 100% import WP → local content risk
  ⚠ Solution-determining SF must have ≥5 WPs from ≥4 methods
```

Source marking: (L)=Library, (S)=Standards, (A)=ACH, (H)=Human, (T)=TRIZ

### Step B2: DSO Pre-Ranking

```
DSO PRE-RANKING — {{project_id}}
Combinatorial explosion: {{N}} SFs × avg {{M}} WPs = {{M^N}} theoretical

| SF-ID | WP-ID | Principle | Performance (1-4) | Risk (1-4) | DSO (P×R) | Rank |
|-------|-------|-----------|-------------------|-----------|-----------|------|

Thresholds: ≥12 Strong, 6-11 Viable, ≤5 Weak
Rearranged: Best WPs on LEFT → left-path = strongest baseline
```

### Step B3: Morphological Matrix (TRIZ-Enhanced)

```
MORPHOLOGICAL MATRIX — {{project_id}}
Date: {{today}} | Design Type: {{type}} | Status: DRAFT

| SF-ID | Sub-Function | SP-1 | Src | Lvl | DSO | SP-2 | Src | Lvl | DSO | SP-3 | Src | Lvl | DSO | SP-ACH | Src | Lvl | DSO |
|-------|-------------|------|-----|-----|-----|------|-----|-----|-----|------|-----|-----|-----|--------|-----|-----|-----|

ACH COLUMN: MANDATORY for every SF. If no AI solution → "N/A — physical only"

ESSENTIAL PROBLEM SATISFACTION:
| SP | Satisfies | Count |
```

### Step B3b: CPS/Services Row (VDI 2221:2019 Scope Extension)

> **VDI 2221:2019** explicitly expands scope to CPS and services. Modern products consist of mechanics, electronics, software, AND services.

For products with field deployment or ongoing customer relationship:
```
SERVICE/CPS MORPHOLOGICAL ROW — {{project_id}}

| SF-ID | Sub-Function | SP-1 | SP-2 | SP-3 |
|-------|-------------|------|------|------|
| SF-SVC | Service delivery model | On-site support | Remote monitoring | Self-service + manual |
| SF-UPD | Update mechanism | Manual firmware | OTA update | No updates (frozen) |
| SF-DATA | Field data collection | None | Manual download | Continuous telemetry |

NOTE: Skip for pure mechanical products without electronics.
      MANDATORY for ACH products (data flywheel depends on SF-DATA).
      Already included in --icdm mode (BB ICDM extension). This makes it standard.
```

### Step B4: Compatibility Verification (8 Types)

```
COMPATIBILITY MATRIX — {{project_id}}

8 TYPES: Energy, Geometric, Material, Signal, Temporal, Environmental, Manufacturing, Supply chain

| WP-A | WP-B | Compatible? | Issue | Remediation |
```

### Step B5: Concept Combination (≥3 Variants)

```
CONCEPT VARIANTS — {{project_id}}

Concept A (Conservative): [left-path from DSO] — Profile: {{description}}
Concept B (Balanced): — Profile: {{description}}
Concept C (Ambitious/ACH): — Profile: {{description}}

VARIANT COUNT: {{N}} (MINIMUM 3)
```

### Step B6: Human Creative Input (Core)

Present matrix to CEO. CEO adds:
- Novel (H) principles from experience
- Sketch-based concepts
- Cross-domain insights

**Rule:** Pure AI matrix = incomplete. (H) principles MUST be present after this step.

### ICDM Extension (if --icdm active)

- Add service design WPs as additional row
- Add business model WPs as additional row
- Extended solution space beyond technical domain

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/`:
- `BB_Morphological_Matrix.md` — full matrix with DSO, compatibility, sources
- `BB_Concept_Variants.md` — concept A/B/C definitions with profiles

## CEO Checkpoint

```
═══ BLOCK BB SOLUTION SEARCH COMPLETE ═══
Working Principles: {{N}} found across {{M}} sub-functions
Concept Variants: {{count}} defined
Human (H) principles: [present / MISSING — needs CEO input]

CEO:
(1) ✅ Approve → tiếp tục Block BC (Concept Development)
(2) ➕ Thêm working principles (H) trước khi tiếp
(3) 🔄 Chạy lại — mở rộng search cho SF-{{XX}}
(4) ⏸️ Dừng — kiểm tra matrix
```

## COD
- WP search: Offload (O2)
- DSO ranking: Offload (O2)
- Matrix generation: Offload (O2)
- Novel (H) principles: **Core (C)** — human creativity
- Compatibility judgment: Offload (O2) / Core for edge cases
