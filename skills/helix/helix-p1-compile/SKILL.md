---
name: helix-p1-compile
description: "Block E of Phase 1 pipeline — cross-domain sync S1, P02 QC gate (mandatory), compile 8 Phase 1 deliverables, update Status.md for Gate 1 readiness. P&B 5.4. Can run standalone. Triggers on: 'compile Phase 1', 'cross-domain sync', 'Gate 1 ready', 'Phase 1 complete', 'deliverables'."
---

# Block E: Compile — Sync + QC Gate + Deliverables Package

> **P&B:** 5.4 (Practical Application) | **Pipeline:** helix-task-clarify → Block BE
> **Input:** All B0-BD outputs | **Output:** `BE_*.md` files + compiled deliverables
> **AI-Orchestration:** S3 (P02 QC Gate mandatory)

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Run cross-domain sync (S1) | Make design decisions or select concepts |
| Execute P02 QC gate (mandatory) | Modify requirements without delta log |
| Compile 8 Phase 1 deliverables | Skip P02 QC gate for "simple" products |
| Update Status.md for Gate 1 readiness | Start Phase 2 work (concept search) |
| Route mechatronic products to /helix-system-arch | Close the phase without CEO approval |

**Multi-Agent Mode:** NO — compilation and QC are mechanical checks, single agent sufficient.
**CEO Checkpoint:** Approve Gate 1 readiness. CEO decides whether to proceed to Phase 2 or loop back.

## Standalone Usage
```
/helix-p1-compile VN-XUONG-UUV
```

## Input Requirements
- All block outputs: B0 through BD

## Workflow

### Step E1: Cross-Domain Sync S1

```
CROSS-DOMAIN SYNC S1 — {{project_id}}
Date: {{today}}

INTERFACE REQUIREMENTS CHECK:
| IF-ID | Domain A | Domain B | Requirement Conflict? | Resolution | Owner |
|-------|---------|---------|---------------------|-----------|-------|

GAP ANALYSIS:
  Requirements with no domain assigned: [count — must be 0]
  Requirements spanning multiple domains: [count — need ICD entry]
  Interface requirements missing: [list]

ICD v0 → v1 CHANGES:
  [list updates based on requirements allocation]
```

For single-domain (pure mechanical): State "Single-domain — no cross-domain sync needed."

### Step E2: P02 QC Gate (MANDATORY — S3 Compliance)

```
P02 QC GATE — Phase 1 Output
Date: {{today}}

CHECK 1 — COHERENCE: Requirements form consistent set? No contradictions?      [PASS/FAIL]
  Evidence: Gap analysis from BB, cross-domain sync from E1

CHECK 2 — STANDARDS: Referenced standards (MIL-STD, TCVN) correct/current?     [PASS/FAIL]
  Evidence: Standards scan from B0, CEO confirmed

CHECK 3 — ENVIRONMENT: Vietnam conditions accounted for?                        [PASS/FAIL]
  Evidence: CAT 13 requirements (MIL-STD-810H)

CHECK 4 — SAFETY: Weapon/engagement parameters flagged for human review?        [PASS/FAIL]
  Evidence: CAT 7 safety requirements, all D-classified

CHECK 5 — CONFIDENCE: AI-generated values justified? High precision flagged?    [PASS/FAIL]
  Evidence: [TBD]/[ESTIMATE] tags present where uncertain

OVERALL: [PASS / REVIEW / REJECT]
```

**Rule:** If ANY check = FAIL → fix before proceeding to Gate 1.

### Step E2b: Department Objection Check (P&B 5.4 — 4-Step Compilation Step 4)

Before releasing Requirements List as v1.0:

```
STAKEHOLDER OBJECTION CHECK — {{project_id}}

Walk through each stakeholder perspective from B0 Stakeholder Register:
  □ Production (WX): Any requirement impossible to manufacture?
  □ Safety: Any safety gap in requirements?
  □ Operations/Users: Any requirement that makes field use impractical?
  □ Maintenance: Any requirement that makes maintenance impossible?
  □ Logistics: Any requirement that blocks transport/deployment?
  □ Procurement: Any cost target unrealistic?

OBJECTIONS FOUND:
| # | Stakeholder | Requirement | Objection | Resolution | Status |
|---|-----------|------------|----------|-----------|--------|

NOTE: For WX solo-CEO, walk through each perspective systematically.
      For multi-person teams, circulate draft and collect written responses.
```

### Step E3: Requirements List Quality Gate (P&B 5.4)

| Criterion | Weight | Score (0-4) | Evidence |
|----------|--------|------------|---------|
| **Completeness** (30%) | | | All 3 questions answered; ≥50 reqs; ≥70% quantified; all lifecycle stages |
| **Quality** (30%) | | | D/W justified; no contradictions; testable; solution-neutral; refined |
| **Defense-Specific** (20%) | | | MIL-STD cited; safety analysis; security addressed; 3-level maintenance |
| **Process** (20%) | | | Stakeholder cooperation; change control; distribution maintained |

**Thresholds:**
- ≥ 3.5: Approve for Gate 1 → Conceptual Design
- 2.5-3.4: Minor revision, re-review
- < 2.5: Major revision required

### Step E4: Compile Phase 1 Deliverables

Rename and organize all block outputs into standard deliverables:

```
PHASE 1 DELIVERABLES — {{project_id}}

COMPILED FILES (in Phase1-Task/):
  □ 001_Stakeholder_Analysis_v1.0.md ← from B0 (stakeholder register)
  □ 002_Requirements_List_v1.0.md ← from BB (validated D/W list)
  □ 003_IFR_Sacred_Constraints_v1.0.md ← from BB (IFR + SC + resources + Geometry Classification MẬT/HẠN-CHẾ/THƯỜNG — the label the CAD trio reads)
  □ 004_Failure_Analysis_v1.0.md ← from BB (failure-derived + SPOF)
  □ 005_Standards_Compliance_Matrix_v1.0.md ← from B0 + BA (standards mapped)
  □ 006_Essential_Problem_v1.0.md ← from BC (CEO-approved EP)
  □ 007_TVDT_v1.0.md ← from BC (target values, if applicable)
  □ 008_Function_Structure_v1.0.md ← from BD (6-flow + SF table)
  □ Cross_Domain_Sync_S1.md ← from BE (this block)
  □ ICD_v1.md ← updated from v0

PIPELINE ARTIFACTS (retained for audit trail):
  B0_Preflight_Report.md, BA_Requirements_Draft.md, BD_Design_Type.md, BE_P02_QC_Gate.md
```

### Step E4b: Mechatronic Routing (VDI 2206)

After compiling deliverables, classify product for system architecture phase:

```
MECHATRONIC ROUTING — {{project_id}}

Domain count from Function Structure:
  Mechanical sub-functions:  {{count}}
  Electrical sub-functions:  {{count}}
  Software sub-functions:    {{count}}

ROUTING DECISION:
  □ Single-domain (pure mech) → Proceed directly to Phase 2
  □ Multi-domain (mechatronic) → Run /helix-system-arch BEFORE Phase 2
    "⚠️ This product has Mech+Elec+SW. Run /helix-system-arch {{project}}
     to establish cross-domain architecture before concept search."
```

### Step E5: Update Status.md

```
Update 1_Projects/{{project}}/Status.md:
  - Phase 1: COMPLETE
  - Date: {{today}}
  - Requirements: {{N}} ({{D}}D / {{W}}W)
  - Essential Problem: "{{EP}}"
  - Design Type: [Original / Adaptive / Variant]
  - Mechatronic: [YES/NO — if YES, system-arch required before Phase 2]
  - Next: [Gate 1 → /helix-system-arch → Phase 2] OR [Gate 1 → Phase 2]
  - Blocking constraints: [from B0 + BB findings]
```

### Step E6: Design Journal Entry

Log via `/helix-design-journal`:
- Key decisions made during Phase 1
- Surprising requirements discovered
- Stakeholder conflicts resolved
- What would change if starting over

### ICDM Extension (if --icdm active)
- Innovation readiness assessment for Gate 1
- ICDM compliance summary

## Output

Save to `1_Projects/{{project}}/Phase1-Task/`:
- `BE_Cross_Domain_Sync_S1.md`
- `BE_P02_QC_Gate.md`
- `BE_Deliverables_Index.md`
- All compiled 00x_* deliverables (renamed from block outputs)

Update `Status.md` → Phase 1 complete, ready for Gate 1.

## CEO Checkpoint (FINAL)

```
═══ BLOCK BE COMPILE COMPLETE — PHASE 1 DONE ═══
Requirements: {{N}} ({{D}}D / {{W}}W), {{pct}}% quantified
Categories: {{N}}/17
Essential Problem: "{{EP}}"
Function Structure: {{N}} sub-functions
Design Type: {{type}}
P02 QC: {{PASS/FAIL}}
Quality Score: {{score}}/4.0

PHASE 1 PIPELINE COMPLETE.
Deliverables: {{N}} files in Phase1-Task/

Mechatronic: {{YES → run /helix-system-arch first / NO → skip}}

Next:
  /helix-quality-gate {{project}} --gate 1
  {{IF mechatronic}} → /helix-system-arch {{project}} (VDI 2206 system design)
  {{THEN}} → /helix-concept-generate {{project}}
```

## COD
- Cross-domain sync: Offload (O2) — AI checks, CEO resolves conflicts
- P02 QC gate: Offload (O1) — mechanical check
- Quality scoring: Offload (O2) — AI scores, CEO validates
- Deliverable compilation: Offload (O1)
- Status update: Offload (O1)
- **Gate 1 readiness decision: Core (C)** — CEO confirms
