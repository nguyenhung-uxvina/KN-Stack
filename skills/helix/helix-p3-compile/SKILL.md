---
name: helix-p3-compile
description: "Block E of Phase 3 pipeline — embodiment evaluation (Rt/Re + S-diagram), weak spot elimination, P02 QC gate, compile deliverables, update Status.md for Gate 3. P&B 7.6-7.7. Can run standalone. Triggers on: 'embodiment evaluation', 'Phase 3 complete', 'Gate 3 ready', 'compile Phase 3', 'weak spot elimination', 'Rt Re'."
---

# Block E: Compile — Evaluation + Weak Spots + QC Gate + Deliverables

> **P&B:** 7.6 (Evaluation) + 7.7 (Example) | **Pipeline:** helix-embody-realize → Block BE
> **Input:** All B0-BD outputs | **Output:** `BE_*.md` files
> **AI-Orchestration:** S3 (P02 QC Gate mandatory)

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Calculate Rt (technical) + Re (economic) scores | Make design decisions or modify layout |
| Plot S-diagram (Rt vs Re) | Skip P02 QC gate for "quick" products |
| Identify weak spots via value profile chart | Approve Gate 3 (= CEO Core) |
| Execute P02 QC gate (mandatory) | Start Phase 4 without Gate 3 pass |
| Flag return-to-concept if D=0 or >=3 D=1 | Override return-to-concept recommendation |

**Multi-Agent Mode:** NO — evaluation and compilation are mechanical, single agent sufficient.
**CEO Checkpoint:** Gate 3 readiness = Core. CEO decides proceed to Phase 4, loop back to Phase 2, or revise embodiment.

## Workflow

### Step E1: Embodiment Evaluation (P&B 7.6 — Rt/Re)

```
EMBODIMENT EVALUATION — {{project}}
Date: {{today}}

TECHNICAL RATING (Rt):
| # | Criterion | Source | Weight | Score (0-4) | Weighted |
|---|----------|--------|--------|-------------|---------|
| 1 | Function fulfillment | DfX Review | | | |
| 2 | Working principle effectiveness | DfX Review | | | |
| 3 | Layout quality (Clarity/Simplicity) | Basic Rules Audit | | | |
| 4 | Safety compliance | Basic Rules + DfX | | | |
| 5 | Ergonomics | DfX Review | | | |
| 6 | Production feasibility | DfM results | | | |
| 7 | Assembly feasibility | DfA results | | | |
| 8 | Reliability (MTBF) | DfR results | | | |
| 9 | Maintainability | DfMa results | | | |
| 10 | Integration quality | Integration Check | | | |
| Rt = Σweighted / (4 × Σweights) | | | | {{Rt}} |

ECONOMIC RATING (Re):
  BOM cost: {{amount}}
  Assembly labor: {{amount}}
  Total unit cost: {{amount}}
  Budget (Co = 0.7 × admissible): {{amount}}
  Re = Co / Total = {{Re}}

  Alternative (qualitative if cost data unavailable):
  | Factor | Score (0-4) |
  | Material cost intensity | |
  | Manufacturing complexity | |
  | Maintenance burden | |
  Re_qual = Σ / (4 × 3) = {{Re}}

S-DIAGRAM:
  Rt = {{value}}, Re = {{value}}
  Position: [upper-right / on diagonal / above / below]
  Overall R (geometric mean): √(Rt × Re) = {{R}}

GO/NO-GO:
  Rt ≥ 0.80, Re ≥ 0.70, no critical weak spots → GO
  Rt 0.70-0.80, Re ≥ 0.60 → GO with monitoring
  Rt < 0.70 OR Re < 0.60 → CONDITIONAL — fix weak spots
  Rt < 0.60 OR multiple critical → NO-GO — return to concept
```

### Step E2: Weak Spot Identification & Elimination (P&B 7.6)

```
WEAK SPOT ANALYSIS — {{project}}

| Criterion | Score | Weak? | Strategy | Status |
|----------|-------|-------|---------|--------|
| [any ≤1] | | CRITICAL | Major redesign or return to concept | |
| [any = 2 when avg ≥3] | | WEAK | Targeted improvement | |

RETURN-TO-CONCEPT TRIGGERS:
  □ Multiple demand criteria score 0-1?
  □ Weak spots fundamental to working principle?
  □ Improvement attempts consistently fail?
  □ Economic viability compromised beyond recovery?
```

### Step EX: Requirements Delta Summary for Gate 3 (VDI 2221:2019)

Compile all requirement changes from Phase 2 and Phase 3:

```
CUMULATIVE REQUIREMENTS DELTA — Gate 3 Review
Source: Requirements_Delta_Log.md (Phase 2 + Phase 3)

Phase 2 deltas: {{N}} (from BC concept development + BD risk + BE selection)
Phase 3 deltas: {{N}} (from BC integration + BD BOM/cost)
Total: {{N}} changes to Requirements_List since v1.0

Requirements_List version: v{{X}} (incorporating all CEO-approved deltas)
Pending unapproved deltas: {{N}} — must resolve before Gate 3

CEO: Review cumulative delta impact on original scope.
```

> **VDI 2221:2019:** Requirements co-evolve with the solution. By Gate 3, the requirements list should reflect all knowledge gained during conceptual and embodiment design. Any delta not yet CEO-approved is a Gate 3 blocker.

### Step E3: P02 QC Gate (MANDATORY — S3)

```
P02 QC GATE — Phase 3 Output

CHECK 1 — COHERENCE: Layout physically buildable? DfX checks consistent?  [PASS/FAIL]
CHECK 2 — STANDARDS: Materials/processes meet referenced standards?       [PASS/FAIL]
CHECK 3 — ENVIRONMENT: VN tropical conditions in DfR/corrosion/thermal?  [PASS/FAIL]
CHECK 4 — SAFETY: All H-severity DfX FAILs resolved? PLAUSIBLE L-check? [PASS/FAIL]
CHECK 5 — CONFIDENCE: BOM costs justified? Sourcing verified?            [PASS/FAIL]

OVERALL: [PASS / REVIEW / REJECT]
```

### Step E4: Compile Deliverables

```
PHASE 3 DELIVERABLES — {{project}}

□ BA_Preliminary_Layout.md (CEO-approved layout)
□ BB_DfX_Review.md (all categories OK/WARN/FAIL)
□ BB_PLAUSIBLE_Check.md (9-check results)
□ BB_Basic_Rules_Audit.md (Clarity/Simplicity/Safety)
□ BC_Integration_Check.md (cross-domain verified)
□ BC_ICD_v3.md (FROZEN interfaces)
□ BD_BOM_Draft.md (preliminary cost)
□ BD_Long_Lead_Items.md (procurement schedule)
□ BE_Embodiment_Evaluation.md (Rt/Re + S-diagram)
□ BE_P02_QC_Gate.md (5-check results)
□ BE_Deliverables_Index.md (this file)
```

### Step E5: Update Status.md + Design Journal

Update `Status.md` → Phase 3 complete, ready for Gate 3.
Log session via `/helix-design-journal`.

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BE_Embodiment_Evaluation.md`
- `BE_P02_QC_Gate.md`
- `BE_Deliverables_Index.md`

## CEO Checkpoint (FINAL)
```
═══ BLOCK BE COMPILE COMPLETE — PHASE 3 DONE ═══
Rt = {{value}}, Re = {{value}}, R = {{value}}
S-diagram: [position]
Weak spots: {{N}} found, {{M}} resolved
DfX: {{N}} OK, {{M}} WARN, {{K}} FAIL (all H resolved: [Y/N])
P02 QC: {{PASS/FAIL}}
BOM cost: {{amount}} vs target {{amount}}

PHASE 3 PIPELINE COMPLETE.
Next: /helix-quality-gate {{project}} --gate 3
      /helix-detail-finalize {{project}}
```

## COD
- Evaluation scoring: Offload (O2)
- Weak spot identification: Offload (O2)
- P02 QC gate: Offload (O1)
- Deliverable compilation: Offload (O1)
- **Go/No-Go decision: Core (C)** — CEO judgment
- **Weak spot acceptance/resolution: Core (C)**
