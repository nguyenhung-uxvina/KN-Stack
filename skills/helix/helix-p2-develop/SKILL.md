---
name: helix-p2-develop
description: "Block C of Phase 2 pipeline — Pugh screening (Stage A), firming up principle solutions (7 methods), VDI 2225 full evaluation (8-step), TRIZ solution improvement, weak spot analysis. Can run standalone. Triggers on: 'Pugh', 'firming up', 'VDI 2225', 'concept evaluation', 'evaluate concepts', 'weak spot'."
---

# Block C: Concept Development — Pugh + Firming Up + VDI 2225

> **P&B:** 6.5 | **Pipeline:** helix-concept-generate → Block BC
> **Input:** `BB_Morphological_Matrix.md`, `BB_Concept_Variants.md` | **Output:** `BC_*.md` files
> **Galaxy:** [[Two-Stage Evaluation Law]], [[VDI 2225 — Sensitivity Analysis]]
> **Reference:** `helix-concept-generate/references/pb-conceptual-design.md`, `triz-sufield-76solutions.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Pugh screening (Stage A eliminate) | Add new WPs not in morpho matrix (= BB) |
| Firm up principle solutions (7 methods) | Select final concept (= BE, CEO Core) |
| VDI 2225 full evaluation (8-step) | Change evaluation weights mid-process |
| TRIZ solution improvement on weak spots | Skip Pugh and go straight to VDI 2225 |
| Estimate CSR per criterion with domain lens | Override CEO's D/W classification |

**Multi-Agent Mode:** LIGHT — domain-specific criterion estimation for DQM accuracy
**CEO Checkpoint:** Block boundary (output: BC_VDI_2225_Evaluation.md). CEO reviews ranking + weak spots.

## Standalone Usage
```
/helix-p2-develop VN-XUONG-UUV
```

## Input Requirements
- `BB_Concept_Variants.md` — concept definitions
- `BB_Morphological_Matrix.md` — WP details for scoring
- `Requirements_List_v1.md` — criteria source
- Optional: ODI/HOQ for VDI weights

## Workflow

### Step C1: Two-Stage Screening — Pugh Matrix (Stage A)

> **Galaxy:** [[Two-Stage Evaluation Law — Pugh Nhanh Rồi VDI Sâu]]

```
PUGH SCREENING — {{project_id}}
Datum: Concept {{X}} (most understood)

| Criterion | Weight | Concept A vs Datum | Concept B | Concept C | ... |
|-----------|--------|-------------------|-----------|-----------|-----|
| [top 4-6] | [H/M/L] | [+/S/-] | [+/S/-] | [+/S/-] | |
| NET Score | | [net] | [net] | [net] | |

ELIMINATE: Concepts with negative NET score
SURVIVORS → proceed to Firming Up + VDI 2225
```

**Skip condition:** If only 3 concepts → skip Pugh, proceed directly to C1.5.

### Step C1.5: AD Coupling Check — Filter Before Score (v3.1)

> **Galaxy:** [[Filter Before Score — AD Lọc Coupling Trước Khi VDI 2225 Chấm Điểm]]
> **Source:** Axiomatic Design Independence Axiom (Suh, 1990) + WX Session 56 validation
> **Time:** 30 minutes in Excel. **COD:** Offload (AI drafts matrix, CEO validates)

For each surviving concept (post-Pugh), build a quick FR×DP coupling matrix:

```
AD COUPLING CHECK — {{project_id}}
Date: {{today}}
Concepts: {{list post-Pugh survivors}}

STEP 1: List top 5-8 FRs (from Requirements List, high-weight criteria)
| FR# | Functional Requirement | Source |
|-----|----------------------|--------|
| FR1 | {{e.g., Traverse speed ≥90°/s}} | C1 |
| FR2 | {{e.g., Manual fallback ≤1s}} | C8 |
| ... | | |

STEP 2: For each concept, list its key DPs
| DP# | Design Parameter | Concept |
|-----|-----------------|---------|
| DP1 | {{e.g., BLDC motor 200W}} | A, B, C |
| DP2 | {{e.g., Ball screw actuator}} | C only |
| ... | | |

STEP 3: Fill coupling matrix (X = DP affects FR, blank = no effect)

CONCEPT {{X}}:
| | DP1 | DP2 | DP3 | DP4 | DP5 |
|-----|:---:|:---:|:---:|:---:|:---:|
| FR1 | X | | | | |
| FR2 | | X | | | |
| FR3 | | | X | | |
| FR4 | | X | X | | |  ← DP2 affects FR2 AND FR4 = coupling!
| FR5 | | | | | X |

VERDICT:
- Diagonal (all X on diagonal only) → UNCOUPLED ✅ → proceed
- Triangular (X below diagonal) → DECOUPLED ⚠️ → document tuning sequence
- Full (X scattered) → COUPLED ❌ → flag for CEO: redesign or eliminate

COUPLING SUMMARY:
| Concept | Matrix Shape | Coupled FRs | Action |
|---------|:-----------:|-------------|--------|
| A | Decoupled ⚠️ | FR2×FR4 via DP2 | Document sequence |
| B | Uncoupled ✅ | None | Proceed |
| C | Coupled ❌ | FR1×FR3 via DP1 | ELIMINATE or redesign |
```

**Rules:**
- Coupled concepts → flag to CEO BEFORE investing firming-up effort
- CEO decides: eliminate now, or carry with known coupling risk to VDI 2225
- If ALL concepts are coupled → return to BB (morphological matrix) for new WPs
- Decoupled concepts: document the tuning sequence in BC_Firming_Up.md (critical for manufacturing)
- **30 minutes max** — this is a quick filter, not deep analysis. The BD_Coupling_Analysis (Block BD) does the deep version later.

**Skip condition:** Variant/Adaptive designs with ≤2 concepts → skip (coupling already known from V1 baseline).

### Step C2: Firming Up Principle Solutions (P&B 6.5.1)

> **DELEGATES to `/helix-p2-firmup {{project_id}}`** — standalone block skill with CRUMPLE-S method-guided gap diagnosis, method selection matrix, task brief generation, and COD assignment.

Run: `/helix-p2-firmup {{project_id}}`

This block skill will:
1. **F0** — Diagnose information gaps per concept (11 property categories: TEM + VN + ACH)
2. **F1** — Recommend CRUMPLE-S methods per gap using decision matrix (cheap→expensive escalation)
3. **F2** — Generate concrete task briefs grouped by method type
4. **F3** — CEO marks each task as Core/Offload/Skip
5. **F4** — Compile results into `BC_Firming_Up.md`

**Wait for BC2 completion before proceeding to C3.**

<details>
<summary>Quick mode fallback (--quick): flat table without method guidance</summary>

```
FIRMING UP — {{project_id}} (QUICK MODE)

7 METHODS: F1=Rough calcs, F2=Principle sketches, F3=Experiments,
           F4=Physical models, F5=Simulation, F6=Literature, F7=Market research

| Property | Concept A | Concept B | Concept C | Method |
|----------|-----------|-----------|-----------|--------|
| Performance (key metric) | | | | |
| Reliability (MTBF est.) | | | | |
| Fault susceptibility | | | | |
| Approx size (LxWxH) | | | | |
| Weight estimate | | | | |
| Cost estimate (±30%) | | | | |
| Service life | | | | |
| VN manufacturability | | | | |
| ACH readiness | | | | |

DETAIL LEVEL: HIGH for novel/critical, LOW for standard COTS
Rule: Firming up ≠ detail design. Just enough to COMPARE.
```
</details>

### Step C3: Import ODI-Derived Weights

1. Check for HOQ/ODI output
2. If found: Use as VDI 2225 weights (priority 1)
3. If not: CEO assigns weights 1-4 (log in design journal)

**Rule:** ODI weights > subjective weights. CEO may override with justification.

### Step C3.5: Domain-Informed Criterion Assessment (Multi-Perspective DQM)

> **Trigger:** Design complexity AMBER/RED (from B0 preflight) AND ≥3 criteria span multiple domains
> **Skip:** GREEN complexity, Variant/Adaptive with ≤2 concepts, or all criteria single-domain
> **Source:** Multi-Agent Selectivity Law — only add domain perspectives where coupling exists
> **COD:** Offload (AI runs domain debate), Core (CEO reviews trade-offs)

Before scoring in VDI 2225 Step 4, run domain debate on cross-domain criteria to get calibrated bounds.

```
DOMAIN-INFORMED DQM — {{project_id}}
Date: {{today}}

STEP 1: Identify cross-domain criteria (criteria that 2+ domains can assess differently)
| Cr-ID | Criterion | Primary Domain | Secondary Domain(s) | Why Cross-Domain? |
|-------|-----------|---------------|---------------------|-------------------|
| {{e.g., C-05}} | {{Recoil fidelity ≥25N}} | MECH | ELEC (actuator), AI_SW (feedback loop) | Force generation + control + sensing |

STEP 2: Run /helix-domain-debate for each cluster of related cross-domain criteria
  → Design question: "Score bounds for criteria C-05, C-08, C-12 across concepts A/B/C"
  → Context: concept descriptions, firming-up data from C2

STEP 3: Extract from JSON side-car (```json:domain-debate-sidecar)
  → perspectives[].constraints → domain-specific feasibility bounds
  → synthesis.trade_offs → evidence for weight adjustment
  → contradictions[] → flag as uncertainty (?) in VDI 2225 Step 4

APPLY TO VDI 2225:
  (a) SCORE BOUNDS: If MECH says criterion C-05 can achieve 3/4 but ELEC says only 2/4 due to
      actuator limits → score = 2/4 with note "limited by ELEC: {{constraint}}"
  (b) WEIGHT ADJUST: If domain debate reveals a trade-off that changes relative importance →
      CEO reviews weight adjustment (Core decision)
  (c) UNCERTAINTY: If contradiction severity = CRITICAL → mark criterion with ? in Step 4
      (triggers sensitivity analysis in Step 7)
```

**Rules:**
- Cap at 8-10 cross-domain criteria per debate call — group related criteria
- Domain debate for DQM uses the `constraints` field (not `wp_candidates` or `coupling_scores`)
- Single-domain criteria score normally (no debate needed)
- Domain debate output appends to `BC_VDI_2225_Evaluation.md` (not separate file)
- **15-20 minutes max** — this is criterion calibration, not deep coupling analysis (BD does that)

### Step C4: VDI 2225 Full Evaluation (8-Step)

```
VDI 2225 EVALUATION — {{project_id}}
Date: {{today}}

STEP 1 — IDENTIFY CRITERIA (15-30, independent, from requirements):
| Cr-ID | Criterion | Category | Source | Consumer/Producer |

STEP 2 — WEIGHT CRITERIA:
| Cr-ID | Weight | Source (ODI/D-W/Expert) | Justification |

STEP 3 — DEFINE SCALES (what 0 and 4 mean per criterion)

STEP 4 — SCORE (0-4, tendency signs ↑↓, uncertainty ?):
  If C3.5 ran: apply domain-debate bounds (score ≤ min(domain bounds), ? if CRITICAL contradiction)
| Criterion | Weight | Concept A | Concept B | Concept C | Domain Bound? |

STEP 5 — CALCULATE:
  x_t = Σ(w×s) / (4×Σw)   |  x_e = Σ(w×s) / (4×Σw)
  Threshold: ≥ 0.6 | RANKING: ___

STEP 6 — Rt-Re DIAGRAM: [above diagonal = good value]

STEP 7 — UNCERTAINTIES: [for ? scores, what range? does it change ranking?]

STEP 8 — WEAK SPOTS:
  ⚠ Score ≤ 1 → WEAK SPOT
  ⚠ 2+ below average → RELATIVE WEAK
  ⚠ High ? on high-weight → RISK SPOT
  
VALUE PROFILE: [bar chart visualization]
GOLDEN RULE: "Balanced 75% > Unbalanced 85%"
```

### Step C5: TRIZ Solution Improvement

**Trigger:** ANY VDI criterion < 2/4
**Reference:** `helix-concept-generate/references/triz-sufield-76solutions.md`

1. Identify weak areas from Step C4
2. Su-Field model each weakness (S1, S2, F, model type)
3. Look up standard solution (Class 1-5)
4. Propose improvement → re-evaluate
5. Innovation level assessment

**Skip:** If ALL criteria ≥ 2/4 → skip.

### ICDM Extension (if --icdm active)

- Add sustainability criteria to VDI 2225
- Add circularity score per concept
- Add innovation maturity assessment
- ICDM multi-criteria supplement output
- **DQM Multi-Perspective (v2.0):** When ICDM is active, Step C3.5 is MANDATORY (not optional) because CSR-weighted evaluation accuracy depends on domain-specific constraint knowledge. The domain debate informs:
  - CSR criterion bounds (from `perspectives[].constraints`)
  - Group A vs Group B weight validation (from `synthesis.trade_offs`)
  - Cross-domain failure risk per criterion (from `contradictions[]`)

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/`:
- `BC_Pugh_Screening.md` — elimination results (if run)
- `BC_Firming_Up.md` — property estimates per concept
- `BC_VDI_2225_Evaluation.md` — full 8-step evaluation

### Requirements Backflow Check (VDI 2221:2019 Co-evolution)

After VDI 2225 evaluation and weak spot analysis, check if any findings require updating Phase 1 requirements:

```
REQUIREMENTS BACKFLOW — Block BC
Date: {{today}}

□ Any requirement value proven infeasible by firming up calculations?
□ Any new requirement discovered during concept development?
□ Any requirement conflict revealed by VDI 2225 evaluation?
□ Any requirement obsoleted by selected working principles?

If YES to any:
  → Log in {{prefix}}Requirements_Delta_Log.md:
    | Delta-ID | Req-ID | Change Type | Old Value | New Value | Reason | CEO Approved |
    |----------|--------|-------------|-----------|-----------|--------|-------------|
  → Flag at CEO checkpoint below
```

## CEO Checkpoint

```
═══ BLOCK BC CONCEPT DEVELOPMENT COMPLETE ═══
Survivors after Pugh: {{N}} concepts
Domain-Informed DQM: {{ran/skipped}} ({{N}} cross-domain criteria debated, {{N}} contradictions)
VDI 2225 Ranking: {{Concept X}} ({{x_t}}) > {{Concept Y}} ({{x_t}}) > ...
Weak Spots: {{count}} found ({{N}} domain-bounded)
TRIZ Improvements: {{count}} applied
Requirements backflow: {{N}} changes logged (see Requirements_Delta_Log.md)

CEO:
(1) ✅ Approve → tiếp tục Block BD (Risk & Integration)
(2) 🔍 Xem chi tiết weak spots trước khi tiếp
(3) 🔄 Chạy lại — điều chỉnh weights hoặc criteria
(4) ⏸️ Dừng — cần firming up thêm (thí nghiệm)
```

## COD
- Pugh screening: Offload (O1)
- Firming up calculations: Offload (O2)
- Firming up experiments: **Core (C)** — physical lab work
- VDI 2225 computation: Offload (O1)
- Weak spot identification: Offload (O2)
- Weight decisions: **Core (C)** — CEO assigns/validates
- TRIZ improvement acceptance: **Core (C)**
