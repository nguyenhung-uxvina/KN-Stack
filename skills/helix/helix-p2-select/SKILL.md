---
name: helix-p2-select
description: "Block E of Phase 2 pipeline — P02 QC gate (mandatory S3 compliance), CEO concept selection (non-delegable), embodiment handoff package, design journal entry. Can run standalone. Triggers on: 'concept selection', 'select concept', 'P02 QC gate', 'handoff', 'Phase 2 complete', 'chon concept'."
---

# Block E: Selection & Handoff — QC Gate + CEO Decision + Phase 3 Package

> **P&B:** 6.5.3 | **Pipeline:** helix-concept-generate → Block BE
> **Input:** All BD_*.md + BC_VDI_2225 + BB_Variants | **Output:** `BE_*.md` files
> **Galaxy:** [[Phán đoán không thể uỷ thác cho AI]]
> **AI-Orchestration:** S3 (P02 QC Gate mandatory)

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Run P02 QC gate (mandatory S3 compliance) | Select concept for CEO (non-delegable) |
| Present all evidence (VDI 2225 + CFMA + coupling) | Recommend a specific concept |
| Compile embodiment handoff package | Skip QC gate even if "time pressure" |
| Record design journal entry | Override CEO's concept choice |

**Multi-Agent Mode:** NO — CEO decision, single agent presents data. Agent NEVER recommends.
**CEO Checkpoint:** THIS IS the checkpoint. CEO selects concept. Non-delegable per [[Phán đoán không thể uỷ thác cho AI]].

## Standalone Usage
```
/helix-p2-select VN-XUONG-UUV
```

## Input Requirements
- `BC_VDI_2225_Evaluation.md` — scores, ranking
- `BD_Coupling_Analysis.md` — coupling risks
- `BD_Assumption_Register.md` — unverified items
- `BD_CFMA.md` — failure analysis
- `BD_Sensitivity_Analysis.md` — ranking stability
- `BB_Concept_Variants.md` — concept definitions

## Workflow

### Step E1: P02 QC Gate (MANDATORY — S3 Compliance)

```
P02 QC GATE — Phase 2 Output
Date: {{today}}

CHECK 1 — COHERENCE: Concept combinations physically compatible?     [PASS/FAIL]
  Evidence: BD Compatibility Matrix

CHECK 2 — STANDARDS: WPs based on real standards/papers?              [PASS/FAIL]
  Evidence: BB source citations

CHECK 3 — ENVIRONMENT: Concepts work in VN conditions?                [PASS/FAIL]
  Evidence: MIL-STD-810 compatibility check

CHECK 4 — SAFETY: Safety-critical SF changes flagged?                 [PASS/FAIL]
  Evidence: BD CFMA — zero critical SFDs

CHECK 5 — CONFIDENCE: VDI scores justified? Weights traced?           [PASS/FAIL]
  Evidence: BC weight sources + BD sensitivity

OVERALL: [PASS / REVIEW / REJECT]
```

**Rule:** If ANY check = FAIL → fix before CEO presentation. No exceptions.

### Step E2: Cross-Domain Sync S3

```
CROSS-DOMAIN SYNC S3 — {{project_id}}
Date: {{today}}

| IF-ID | Concept A Compatible? | Concept B Compatible? | Notes |

ICD UPDATE → v2: [changes needed for selected concept]
```

### Step E3: CEO Concept Selection (Core — Non-Delegable)

> **Galaxy:** [[Phán đoán không thể uỷ thác cho AI]]

Present COMPLETE decision package:

```
═══════════════════════════════════════════════════════
CEO CONCEPT SELECTION — {{project_id}}
═══════════════════════════════════════════════════════

1. VDI 2225 RANKING:
   Concept A: x_t = ___, x_e = ___, overall = ___
   Concept B: x_t = ___, x_e = ___, overall = ___
   Concept C: x_t = ___, x_e = ___, overall = ___

2. WEAK SPOTS: [which concepts, which criteria?]

3. COUPLING RISK: [H/M/L per concept]

4. SENSITIVITY: [robust or sensitive to Cx?]

5. CFMA: [critical SFDs? unresolved?]

6. 3-SCENARIO: [most robust under pessimistic?]

7. INNOVATION LEVEL: [avg per concept, problems satisfied]

8. ASSUMPTIONS: [unverified count per concept]

9. P02 QC: [PASS status]

═══════════════════════════════════════════════════════
CEO: Chọn concept nào?
Rationale (CEO viết): ___________________________________
═══════════════════════════════════════════════════════
```

**Rule:** AI NEVER selects concept. AI presents data. CEO decides.

### Step E4: Embodiment Handoff Package

```
PHASE 3 HANDOFF PACKAGE — {{project_id}}
Date: {{today}}

SELECTED CONCEPT: {{name}}

DELIVERABLES CHECKLIST:
  □ BB_Morphological_Matrix.md (selected path highlighted)
  □ BC_VDI_2225_Evaluation.md (complete 8-step)
  □ BC_Firming_Up.md (rough calculations, sketches)
  □ BD_Coupling_Analysis.md (risk mitigation plan)
  □ BD_Assumption_Register.md (verification schedule)
  □ BD_CFMA.md (action items for Phase 3)
  □ BE_Concept_Selection.md (CEO rationale)
  □ ICD v2 (concept-specific interfaces)

WEAK SPOTS TRACKER (carry into Phase 3):
| Spot | VDI Score | Mitigation | Owner | Due |

TRACEABILITY: Every R-xxx → concept feature

NEXT: /helix-quality-gate {{project}} --gate 2
      /helix-embody-realize {{project}}
```

### Step E4b: Requirements Delta Summary (VDI 2221:2019)

If `{{prefix}}Requirements_Delta_Log.md` exists (created by BC or BD), include in handoff package:

```
REQUIREMENTS DELTA SUMMARY — Phase 2
Total changes: {{N}}
  - New requirements added: {{n}}
  - Values changed: {{n}}
  - Requirements removed: {{n}}
  - All CEO-approved: [YES / NO — list pending]

Action for Phase 3: Update Requirements_List to v1.1 incorporating approved deltas.
```

### Step E5: Design Journal Entry

Log session decisions:
- Key design choices
- Concept selection rationale
- Surprises / lessons
- What would change if starting over

### ICDM Extension (if --icdm active)

- IRL (Innovation Readiness Level) score per concept
- ICDM compliance summary
- Innovation pathway recommendation

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/`:
- `BE_P02_QC_Gate.md`
- `BE_Concept_Selection.md`
- `BE_Handoff_Package.md`

Update `Status.md` → Phase 2 complete, ready for Gate 2.

## CEO Checkpoint (FINAL)

```
═══ BLOCK BE SELECTION COMPLETE — PHASE 2 DONE ═══
Selected: {{concept name}}
P02 QC: {{PASS/FAIL}}
Handoff ready: [YES/NO]

PHASE 2 PIPELINE COMPLETE.
Next: /helix-quality-gate {{project}} --gate 2
```

## COD
- P02 QC checks: Offload (O1)
- ICD sync: Offload (O2)
- Concept selection: **Core (C)** — CEO decides, non-delegable
- Decision rationale: **Core (C)** — must reflect real reasoning
- Handoff compilation: Offload (O1)
