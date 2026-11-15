---
name: helix-p1-preflight
description: "Block 0 of Phase 1 pipeline — verify Phase 0 complete, gather project context, build stakeholder register, scan applicable standards, confirm scope boundaries. P&B 5.1. Can run standalone. Triggers on: 'Phase 1 preflight', 'stakeholder analysis', 'gather context', 'task source'."
---

# Block 0: Pre-Flight — Context Gathering & Scope Confirmation

> **P&B:** 5.1 (Importance of Task Clarification) | **Pipeline:** helix-task-clarify → Block B0
> **Input:** Phase 0 deliverables | **Output:** `B0_Preflight_Report.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Verify Phase 0 inputs exist and are complete | Generate requirements (= BA) |
| Build stakeholder register from project docs | Classify D/W (= BB, CEO Core) |
| Scan applicable standards (MIL-STD, TCVN) | Abstract the problem (= BC) |
| Confirm scope boundaries with CEO | Create function structure (= BD) |
| Assess VDI 2221 contextual factors | Make design decisions |

**Multi-Agent Mode:** NO — simple validation, single agent sufficient.
**CEO Checkpoint:** Confirm scope, stakeholders, and standards before BA starts.

## Standalone Usage
```
/helix-p1-preflight VN-XUONG-UUV
```

## Input Requirements
- `Status.md` — current phase, tier, blocking constraints
- `_Project_Brief.md` — charter, scope
- `ICD_v0.md` — domain boundaries (if multi-domain)
- `/plan` outputs in `Phase0-Plan/` (if available):
  - `Product_Proposal_v*.md` → IFR statement, sacred constraints, TRIZ available resources, design paradigm
  - `Product_Planning_v*.md` → scope definition, stakeholder map, cost targets, development timeline, NRE budget
  - `Portfolio_Planning_v*.md` → variant strategy, shared platform modules, cross-product synergy, revenue targets
- FORGE outputs in `Phase0-Forge/ (or FORGE/)` (if available):
  - `ODI_Outcomes_v*.md` → customer desired outcomes, opportunity scores → drive VDI 2225 weights in Phase 2
  - `Job_Map_v*.md` → customer job steps → inform requirement categories
  - `HOQ_Design_Parameters_v*.md` → design parameters + correlation roof → feed TRIZ in Phase 2
  - `Cost_Envelope_v*.md` → unit cost target, NRE budget, volume assumptions
  - `LCC_Estimate_v*.md` → lifecycle cost breakdown → informs CAT 15 (Costs) requirements
  - `ACH_Assessment_v*.md` → ACH go/no-go → constrains solution space for AI/SW requirements
  - `ACH_Opportunity_Scan_v*.md` → ACH potential per sub-function → informs PD requirements

## Workflow

### Step 0.1: Verify Phase 0 Complete

```
PHASE 0 VERIFICATION — {{project_id}}
Date: {{today}}

□ Status.md exists and shows Phase 0 COMPLETE or Gate 0 PASS
□ _Project_Brief.md exists with scope defined
□ Product Planning document exists (from /helix-project-init or /plan)
□ ICD v0 exists (or N/A for single-domain)

/PLAN OUTPUTS CHECK (Phase0-Plan/ folder):
□ Product_Proposal_v*.md — [FOUND / NOT FOUND]
    If found: extract IFR, sacred constraints, TRIZ resources, design paradigm
□ Product_Planning_v*.md — [FOUND / NOT FOUND]
    If found: extract stakeholders, cost targets, timeline, NRE, scope decisions
□ Portfolio_Planning_v*.md — [FOUND / NOT FOUND]
    If found: extract variant strategy, shared modules, synergy map, revenue targets
    NOTE: Portfolio context is CRITICAL for variant-aware requirements
          (e.g., VN-MGM V1 requirements must consider V5 inheritance path)

/FORGE OUTPUTS CHECK (Phase0-Forge/ (or FORGE/) folder):
□ ODI_Outcomes_v*.md — [FOUND / NOT FOUND]
    If found: extract opportunity scores → will drive VDI 2225 weights in Phase 2
□ Job_Map_v*.md — [FOUND / NOT FOUND]
    If found: extract job steps → inform requirement categories
□ HOQ_Design_Parameters_v*.md — [FOUND / NOT FOUND]
    If found: extract design parameters + correlation roof → feed TRIZ in Phase 2
□ Cost_Envelope_v*.md — [FOUND / NOT FOUND]
    If found: extract unit cost target, NRE budget → constraint for CAT 15 requirements
□ LCC_Estimate_v*.md — [FOUND / NOT FOUND]
    If found: extract lifecycle costs → inform maintenance + disposal requirements
□ ACH_Assessment_v*.md — [FOUND / NOT FOUND]
    If found: extract ACH go/no-go → constrains AI/SW solution space
□ ACH_Opportunity_Scan_v*.md — [FOUND / NOT FOUND]
    If found: ACH potential per sub-function → informs PD requirements

STATUS: [GO / NO-GO — what's missing?]
```

### Step 0.2: Identify Task Source Type (P&B 5.1)

| Source Type | Check | Implications |
|------------|-------|-------------|
| Development Order | From product planning / MoD? | Formal, contractual, MIL-STD heavy |
| Definite Customer Order | Specific contract? | Clear specs, focus compliance |
| Internal Request | From sales/test/assembly? | Problem-driven, failure analysis first |
| Market Analysis | Identified opportunity? | No specific customer — needs ODI |
| Problem Report | Field failures? | Root cause before requirements |
| Regulatory Change | New standards? | Compliance-driven redesign |

**Task source: {{type}}**

Extract from task: Product statements + Deadline statements + Cost targets.

### Step 0.3: Stakeholder Register (P&B 5.1 + Defense Context)

```
STAKEHOLDER REGISTER — {{project_id}}
Date: {{today}}

| # | Role | Stakeholder | Buyer/User? | Interest Domain | Access? | Priority |
|---|------|-----------|------------|----------------|---------|----------|
| S1 | Operator | [who operates?] | USER | Ease of use, reliability | [Y/N] | HIGH |
| S2 | Commander/Decision-Maker | [who decides?] | DECISION | Availability, capability | [Y/N] | HIGH |
| S3 | Procurement | [who buys?] | BUYER ≠ USER | Cost, local content, delivery | [Y/N] | HIGH |
| S4 | Maintainer | [who maintains?] | USER | Simple maintenance, spare parts | [Y/N] | MED |
| S5 | Safety Officer | [who approves?] | AUTHORITY | No structural failure | [Y/N] | HIGH |
| S6 | Production (WX) | [internal] | INTERNAL | CNC feasible, local supply | Y | MED |
| S7 | Logistics | [transport] | INTERNAL | Weight, dimensions, packaging | Y | LOW |
| S8 | Trainer | [who trains?] | USER | Training time, simplicity | [Y/N] | MED |

CONFLICTS IDENTIFIED:
| S-A | S-B | Conflict | Resolution | Status |
|-----|-----|---------|-----------|--------|

⚠ BLOCKING: If ≥2 HIGH stakeholders have Access=N → add to Status.md blockers immediately.
```

### Step 0.4: Standards Scan

```
APPLICABLE STANDARDS — {{project_id}}

| Standard | Scope | Requirements Impact | CEO Confirmed? |
|----------|-------|-------------------|---------------|
| MIL-STD-810H | Environmental (temp, humidity, vibration, salt fog) | CAT 13 (Operation) | [Y/N] |
| MIL-STD-882E | System safety | CAT 7 (Safety) | [Y/N] |
| MIL-STD-461G | EMI/EMC | CAT 6 (Signals) | [Y/N] |
| STANAG {{N}} | Interoperability | [varies] | [Y/N] |
| TCVN {{N}} | Vietnamese national | [varies] | [Y/N] |
| [product-specific] | [scope] | [impact] | [Y/N] |

NOTE: AI lists candidates. CEO CONFIRMS which standards apply. AI NEVER fabricates TCVN numbers.
```

**RESEARCH HOOK (standards):** Before presenting candidates to CEO, query the `std`
topic notebook if registered (`/topic-notebook --query std "applicable standards for
<product class>"`) — cited hits pre-fill the table, and CEO only supplies the gaps.
If `std` is not yet built or returns NOT FOUND, offer a T2 brief via `/helix-research`
(`type: standards`, `risk_if_wrong: HIGH` — defense citations must be tier S/A).
CEO confirmation of applicability remains Core; this hook only reduces the blank-page load.

### Step 0.5: Scope Boundaries

```
SCOPE — {{project_id}}

INCLUDED: [what this product IS]
EXCLUDED: [what this product is NOT]
INTERFACES: [what it connects to — defines ICD boundaries]
OPERATIONAL ENVELOPE: [where/when/how it operates]

THREE QUESTIONS (P&B 5.1):
  Q1 — What objectives must the solution satisfy?
  Q2 — What properties MUST it have?
  Q3 — What properties must it NOT have?
```

### Step 0.6: Contextual Factors Assessment (VDI 2221 Blatt 2)

> **VDI 2221:2019 Blatt 2** requires adapting the generic design process to company-specific context. This step assesses contextual factors that influence pipeline mode and depth.

```
CONTEXTUAL FACTORS — {{project_id}}
Date: {{today}}

EXTERNAL FACTORS:
  □ Legislation/standards: [MIL-STD heavy / TCVN / mixed / minimal]
  □ Market type: [defense procurement / commercial / dual-use]
  □ Customer type: [MoD / military unit / OEM / end-user]
  □ Competition intensity: [monopoly / oligopoly / competitive]
  □ Time-to-market pressure: [urgent / normal / relaxed]

INTERNAL FACTORS:
  □ Company capability: [full in-house / partial outsource / heavy outsource]
  □ Product novelty: [Original / Adaptive / Variant] — from Design Type
  □ Batch size: [prototype / small series / mass production]
  □ Team composition: [solo CEO / small team / multi-disciplinary]
  □ Manufacturing tools: [CNC + manual / advanced / basic workshop]
  □ Prior product experience: [none / partial / extensive ({{similar products}})]

PIPELINE MODE RECOMMENDATION:
  Based on contextual factors:
  □ --quick recommended? [YES if Variant + extensive experience + small team]
  □ --icdm recommended? [YES if customer-driven + commercial + Original]
  □ Standard mode: [default for defense + Adaptive/Original]

NOTE: This assessment informs pipeline depth but CEO decides final mode.
```

### Step 0.6b: Question Protocol + Stopping Conditions (gstack Ch07 Office-Hours)

> Pattern source: gstack Station Zero — "surface ambiguity before implementation, with defined stopping conditions."

Before B0 is approved, surface all open questions systematically. Unanswered questions at this stage become blocking surprises in Phase 2 or 3.

**Question sweep — 5 domains:**

```
QUESTION PROTOCOL — {{project_id}}
Date: {{today}}

1. SCOPE questions
   □ Is the product boundary clear enough that two engineers would agree on what's in/out?
   □ Are there adjacent systems that might "absorb" scope if not explicitly excluded?
   □ Open: {{list or NONE}}

2. STAKEHOLDER questions
   □ Is there a decision-maker we haven't spoken to whose veto could block this product?
   □ Are any HIGH-priority stakeholders currently inaccessible? (→ see Step 0.3 blocking flag)
   □ Open: {{list or NONE}}

3. REQUIREMENTS questions (to be answered by BA, not CEO here)
   □ Are any 17 P&B categories clearly impossible to populate given current info?
   □ Is there a hard constraint the requirements list MUST reflect but hasn't been stated?
   □ Open: {{list or NONE}}

4. CONSTRAINTS questions
   □ Are there external constraints (budget ceiling, HELIX Gate 0 verdicts, ACH go/no-go) that
     would make this product infeasible before requirements are written?
   □ Open: {{list or NONE}}

5. DEPENDENCIES questions
   □ Does this task depend on outputs from another parallel project not yet complete?
   □ Are shared platform modules locked or still in flux?
   □ Open: {{list or NONE}}
```

**Stopping conditions — B0 is DONE ENOUGH to proceed to BA when:**

| Condition | Check |
|-----------|-------|
| SC-1 | All 5 question domains addressed (answers or explicit "NONE") |
| SC-2 | No HIGH-priority stakeholder has Access=N (or blocker logged in Status.md) |
| SC-3 | Scope boundaries defined with at least one explicit EXCLUDED item |
| SC-4 | No fatal feasibility blocker identified (budget, ACH no-go, standard violation) |
| SC-5 | CEO can state the "definition of done" for Phase 1 in one sentence |

**HALT condition:** If SC-4 fails → do NOT proceed to BA. Update Status.md with blocker and return to the blocking upstream deliverable (forge-shift, helix-project-init, etc.) before re-running B0.

**CEO time target:** 20 min for familiar project, 45 min for new product domain.

**COD:** Core (C) for SC-4 and SC-5 — only CEO knows if a constraint is fatal.

### Step 0.7: Model Inventory Check (VDI 2206 Blue Strand)

> **VDI 2206:2021 Blue Strand:** All engineering tasks should be supported by models. Establish baseline.

```
MODEL INVENTORY — {{project_id}} Phase 1
Date: {{today}}

EXISTING MODELS:
  □ CAD models from similar products? [YES: list / NO]
  □ Simulation models (FEM, CFD, thermal)? [YES: list / NO]
  □ Mathematical/analytical models? [YES: list / NO]

MODELS NEEDED FOR PHASE 2:
  □ Concept sketch capability (hand/CAD)?
  □ Rough calculation tools (spreadsheet/MATLAB)?
  □ Reference models from forge-library?

NOTE: Phase 1 = requirements + function structure. Models mainly needed from Phase 2.
```

### ICDM Extension (if --icdm active)
- Innovation context analysis
- Creativity readiness assessment
- Collaboration maturity check

## Output

Save to `1_Projects/{{project}}/Phase1-Task/B0_Preflight_Report.md`

## CEO Checkpoint

```
═══ BLOCK B0 PRE-FLIGHT COMPLETE ═══
Task Source: {{type}}
Stakeholders: {{N}} identified, {{M}} HIGH priority, {{K}} accessible
Standards: {{N}} applicable
Scope: [confirmed / needs clarification]

Stopping Conditions (Step 0.6b):
  SC-1 All 5 question domains addressed:  [✅ / ❌ — list open]
  SC-2 No unblocked HIGH-priority stake:  [✅ / ❌ — {{who}}]
  SC-3 Scope has ≥1 explicit EXCLUDED:    [✅ / ❌]
  SC-4 No fatal feasibility blocker:       [✅ / ❌ — {{what}}]
  SC-5 Phase 1 "done" in one sentence:    "{{sentence}}"

CEO:
(1) ✅ All SC pass → tiếp tục Block BA (Requirements Generation)
(2) 🔄 Bổ sung stakeholders hoặc standards
(3) ⏸️ Dừng — SC-4 blocker: cần resolve {{issue}} trước
(4) ❓ Re-run question protocol — thêm domain {{X}} chưa đủ
```

## COD
- Context gathering: Offload (O1) — AI reads project files
- Standards scan: Offload (O2) — AI lists candidates
- Standards confirmation: **Core (C)** — CEO confirms which apply
- Stakeholder identification: Offload (O2) / **Core (C)** for military contacts
- Scope boundaries: **Core (C)** — CEO defines
