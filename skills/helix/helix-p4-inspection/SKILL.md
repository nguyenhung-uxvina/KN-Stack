---
name: helix-p4-inspection
description: "Block C of Phase 4 pipeline — incoming material + in-process + Final Acceptance Test (FAT) inspection plans, serialization scheme, Req-ID → test method traceability matrix, P03 doc quality + P04 TCVN compliance gates, 5-year retention policy. P&B 9.5. Triggers on: 'Phase 4 inspection', 'inspection plan', 'FAT', 'serialization', 'P03 P04'."
---

# Block C: Inspection — Quality Plan + Traceability

> **P&B:** Chapter 9 § 9.5 | **Pipeline:** helix-detail-finalize → Block BC
> **Input:** BA drawings (acceptance criteria) + BB BOM (incoming items) + frozen requirements (test methods) | **Output:** `Inspection_Checklist.md` + `Test_Procedures.md`

## Operational Envelope

| DO | DON'T |
|----|----|
| Incoming + in-process + FAT plans | Critical dim spec (= BA, CEO Core) |
| Req-ID → test method matrix | Assembly sequence (= BD) |
| Serialization scheme | Workshop master review (= BE, CEO Core) |
| P03/P04 gates | Field warranty terms (BRIDGE) |
| 5-year retention policy | Customer acceptance criteria (BE/customer) |

**Multi-Agent Mode:** NO.
**CEO Checkpoint:** Approve FAT procedures + serialization scheme.

## Workflow

### Step C.1: Incoming Material Inspection

```
INCOMING INSPECTION — {{project}}
| Item | Check | Method | Accept Criteria | Frequency | Inspector |
|----|----|----|----|----|----|
| Al 5083 plate | Material cert | Certificate review | EN 573 / TCVN | 100% lots | QC |
| CNC parts | Dimensional | Caliper / CMM | Per drawing ±tol | 100% | QC |
| PCB | Visual | Microscope | IPC-A-610 Class 2 | 100% | QC |
| Connectors | Continuity | Multimeter | <0.5 Ω | 100% | QC |
| COTS modules | Functional | Power-on test | Per datasheet | Sample/lot | QC |
```

### Step C.2: In-Process Inspection (Gate Map)

Maps to PX workstations (matches `erp-quality` Gate-CKCX/DT/DC/VL/Final):

```
IN-PROCESS GATES:
| Gate | After | Check | Method | Accept | Record |
|----|----|----|----|----|----|
| Gate-CKCX | CNC/Welding | Weld visual + dims | AWS D1.2 / caliper | Class B | Photo + form |
| Gate-DT | PCB assembly | Continuity + isolation | Multimeter + DMM | Per ICD | Test report |
| Gate-DC | Integration | Wiring check + torque | Multimeter + wrench | Per spec | Checklist |
| Gate-VL | Surface treatment | Visual + adhesion | Visual + tape test | Per spec | Photo |
| Gate-Final | All complete | Functional + cosmetic | FAT procedure | Per req | FAT log |
```

### Step C.3: Final Acceptance Test (FAT) Procedures

> **Seed dimensional accept criteria from the geometry-of-record, don't re-transcribe:** When an ingested record exists for the part, seed dimensional acceptance criteria directly from its geometry-of-record `cad_extract.json` critical-dim rows (Param|Value|Tol|Source|Confidence) via [[helix-cad-ingest]] — don't re-transcribe from the BA drawing by hand. Carry the Source pointer + Confidence into the inspection plan; LOW-confidence dims require CEO certification before becoming accept criteria.

For each D-requirement → one test procedure:

```
FAT TEST {{TEST-ID}}: [Test Name]
Requirement: R-{{xxx}} (from frozen Requirements_List)
Acceptance criterion: [measurable, quantitative]
Method: [exact procedure, equipment, environmental conditions]
Duration: [time]
Equipment: [calibrated, with cert reference]
Sample size: [unit / batch]
Pass/fail logic: [explicit]
Record format: [data sheet or log file format]
Inspector competency: [training/cert required]
```

**Traceability matrix:**

| Req-ID | Requirement | Test ID | Method | Equipment | Inspector |
|----|----|----|----|----|----|

100% of D-requirements must map to ≥1 test. Audit at end of BC.

### Step C.4: Serialization Scheme

```
SERIAL NUMBER FORMAT — {{project}}
Pattern: {{PROJECT}}-{{YYYY}}-{{NNN}}
  e.g., BB-01-2026-001 through BB-01-2026-100

ALLOCATION:
  - Pre-production (engineering): 001-009
  - Production lot 1: 010-099
  - Production lot 2+: 100+

ASSIGNMENT POINT: Stamped during Gate-VL (surface treatment), tied to WO ID

RETAINED RECORDS PER UNIT (5 years minimum for defense):
  □ Material certs (for traceable items)
  □ Gate inspection records (CKCX/DT/DC/VL/Final)
  □ FAT log
  □ NCR if any
  □ Calibration cert references
  □ Customer delivery confirmation
```

### Step C.5: P03 Engineering Document Quality Gate

```
P03 GATE — Phase 4 documents
□ Quantification rate ≥80% (specs have measurable criteria)?
□ Parameter citation 100% traceable to source?
□ Safety tagging on life-safety reqs [SAFETY-CRITICAL]?
□ No vague terms (adequate/sufficient/good/robust)?
□ YAML frontmatter complete?
□ [UNKNOWN] flagged with source needed?

P03 SCORE: __/6  → FAIL = revise before BE.
```

### Step C.6: P04 TCVN Compliance Gate

```
P04 GATE — Phase 4 compliance
□ Primary TCVN standard cited (TCVN_XXXX:YYYY)?
□ Compliance matrix section-by-section?
□ Top procurement-blocking gaps highlighted?
□ No fabricated TCVN clauses (use [TCVN-UNKNOWN])?
□ Safety-critical sections with gaps flagged [SAFETY-GAP]?

P04 SCORE: __/5  → FAIL = revise before BE.
```

### Step C.7: Calibration Reference Register

Each test procedure must reference calibrated equipment. List in `Calibration_Register.md`:

| Equipment | Range | Cert No. | Cal Date | Next Due | Used in Test |
|----|----|----|----|----|----|

## Output

`1_Projects/{{project}}/Phase4-Detail/{{variant}}/`:
- `Inspection_Checklist.md` — incoming + in-process matrix
- `Test_Procedures.md` — FAT procedure book
- `Req_Test_Traceability.md` — Req-ID ↔ Test-ID matrix
- `Serialization_Scheme.md`
- `Calibration_Register.md`

## CEO Checkpoint

```
═══ BLOCK BC INSPECTION COMPLETE ═══
Incoming checks: {{N}}  In-process gates: 5 (CKCX/DT/DC/VL/Final)
FAT tests: {{N}} (100% req coverage = {{Y/N}})
Serial scheme: {{PROJECT}}-YYYY-NNN
P03 score: __/6   P04 score: __/5

CEO:
(1) ✅ Approve → tiếp tục Block BD (Assembly)
(2) 🔄 Adjust FAT criteria / serialization
(3) ⏸️ P03/P04 gate failed — revise docs
```

## COD

- cad_extract dimensional accept-criteria seeding: Offload (O1) — LOW-confidence dims need CEO certification
- Incoming + in-process checklist drafting: Offload (O2)
- Req-ID → Test-ID matrix: Offload (O1) — mechanical mapping
- Serialization scheme: Offload (O1)
- P03/P04 gate scoring: Offload (O2)
- **FAT acceptance criteria thresholds: Core (C)** — quality bar judgment
- **Calibration equipment selection: Core (C)** — metrology competency
