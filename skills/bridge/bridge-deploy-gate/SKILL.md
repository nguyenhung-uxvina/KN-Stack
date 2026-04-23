---
name: bridge-deploy-gate
description: Deployment readiness gate for Workshop X products. This skill should be used when the user asks about deployment, go-live readiness, phase gates, or whether a product is ready to deploy. Enforces a 4-phase sequential protocol where no phase can be skipped. Triggers on deploy, go live, phase gate, ready, trien khai, co nen deploy chua.
---

# Bridge Deploy Gate — Deployment Readiness Control

Prevent premature deployment by enforcing a 4-phase sequential gate protocol. CEO can accelerate phases but cannot skip them.

## When to Use

- Before deploying any product or system to external users
- When asked "is this ready to deploy?" or "co nen deploy chua?"
- At any phase gate review for product maturity
- When transitioning from internal validation to external exposure

## Workflow

### Step 1: Identify Current Phase

Determine which deployment phase the product is at (0-3). Check Status.md and bridge-dashboard for existing records. If no prior record, product starts at Phase 0.

### Step 2: Verify Prior Phase Evidence

For the requested phase, confirm ALL evidence from prior phases is present. No phase may be skipped.

**Phase 0 — Internal Proof of Concept**

| # | Criterion | Evidence Source |
|---|-----------|----------------|
| 1 | AI model trained on available data | Lab results |
| 2 | Basic accuracy demonstrated (internal benchmark) | Test report |
| 3 | Known limitations documented | Design journal |
| 4 | No safety-critical failure modes identified | FMEA / risk register |

Human Decision: "Proof exists that approach COULD work"

**Phase 1 — Internal Validation**

| # | Criterion | Evidence Source |
|---|-----------|----------------|
| 1 | forge-validate Stage 1 (lab) passed | Validation report |
| 2 | forge-fallback architecture designed and coded | Fallback spec |
| 3 | DfX review completed | HELIX DfX output |
| 4 | Performance Envelope v1 documented | Test data |
| 5 | Integration Debt < threshold | HELIX ICD tracker |

Human Decision: "System works under controlled conditions with fallback"

**Phase 2 — Controlled External**

| # | Criterion | Evidence Source |
|---|-----------|----------------|
| 1 | forge-validate Stage 2 (field simulation) passed | Field test report |
| 2 | Fallback tested under realistic conditions | Test evidence |
| 3 | Customer briefed on capabilities AND limitations | Meeting record |
| 4 | Continuous monitoring active | forge-flywheel config |
| 5 | Operator training completed | Training log |

Human Decision: "System ready for limited external use"

**Phase 3 — Full Deployment**

| # | Criterion | Evidence Source |
|---|-----------|----------------|
| 1 | forge-validate Stage 3 (operational field test) passed | Ops report |
| 2 | 90+ day operational history without critical failures | Ops log |
| 3 | Customer satisfaction confirmed | Feedback record |
| 4 | Revalidation schedule established | Schedule doc |
| 5 | Model entered into forge-library | Library entry |

Human Decision: "System is production-ready"

### Step 3: Gap Analysis

For each checklist item in the target phase:
1. Mark as PASS (evidence present), FAIL (evidence missing), or PARTIAL (incomplete)
2. For FAIL/PARTIAL items, specify what is needed and estimated effort
3. Flag any attempt to skip a phase as a violation

### Step 4: Render Verdict

- All prior phases PASS + current phase PASS: recommend GO
- Any item FAIL: recommend NO-GO with specific gaps
- Items PARTIAL: recommend CONDITIONAL with remediation plan

Present verdict to CEO for final GO/NO-GO decision.

### Step 2b: Governance Documentation Gate (from Pattern Library B2)

Before ANY Phase 2+ transition, verify governance documentation exists. These are CUSTOMER-FACING documents — they must exist before external exposure.

```
GOVERNANCE DOCUMENTATION GATE — {{product}}

5 REQUIRED DOCUMENTS (from Pattern Library B2):

DOC 1: SYSTEM LIMITATIONS
  Content: AI CAN do (with confidence levels) | AI CANNOT do | Human MUST do | Operator certification requirements
  Status: EXISTS / DRAFT / MISSING
  Owner: CEO + AI draft
  Template: DCTRS — D: list capabilities, C: no marketing language, T: NCO-level readability, R: HITL mandatory, S: mark [TBD] not guess

DOC 2: ACCOUNTABILITY CHAIN
  Content: Who is responsible at each decision point | Escalation path | Override authority levels | Post-incident review requirements
  Status: EXISTS / DRAFT / MISSING
  Owner: CEO
  Rule: "AI is TOOL. Human ALWAYS accountable for decisions."

DOC 3: AUDIT TRAIL SPECIFICATION
  Content: What gets logged (ALL AI decisions + ALL human overrides) | Log format (timestamped, tamper-evident) | Retention period (≥5 years for defense) | Access control
  Status: EXISTS / DRAFT / MISSING
  Owner: CEO + AI draft

DOC 4: OPERATOR OVERRIDE PROTOCOL
  Content: How to override AI decisions | Authority levels (operator → supervisor → commander) | When override is MANDATORY | Post-override documentation requirements
  Status: EXISTS / DRAFT / MISSING
  Owner: CEO
  Safety hierarchy: SAFETY > COMPLIANCE > ACCURACY > SPEED — always

DOC 5: INCIDENT RESPONSE PROTOCOL
  Content: If AI makes wrong decision, what happens? | Reporting chain | Investigation procedure | Corrective action | Return-to-service criteria
  Status: EXISTS / DRAFT / MISSING
  Owner: CEO

GOVERNANCE GATE VERDICT:
  Phase 0-1: DOC 1 required (minimum)
  Phase 2:   DOC 1-4 required (controlled external)
  Phase 3:   ALL 5 required (full deployment)

  Missing docs at target phase → NO-GO until drafted
  Draft docs → CONDITIONAL GO (must finalize within 30 days)
  All docs exist → governance gate PASS
```

**DCTRS applied to governance docs:**
- **D (Delegate):** AI drafts docs from product brief + design artifacts
- **C (Constrain):** No marketing language. No unreferenced reliability claims. NCO readability.
- **T (Test):** Every claim verifiable through audit trail. Every responsibility has named role.
- **R (Review):** MANDATORY CEO + military liaison review (Pattern Library B2 rule)
- **S (Specify):** If unsure about military procedure → mark [VERIFY WITH MILITARY], never guess

**Prohibited in governance docs:**
- Do NOT claim AI is "safe" — claim it operates within defined bounds
- Do NOT promise reliability percentages without test data
- Do NOT reference internal Workshop X processes (customer-facing)
- Do NOT use jargon NCO wouldn't understand

## Integration Points

- Reads from: forge-validate (stage results), forge-fallback (architecture status), forge-trust (customer briefing), helix-quality-gate (design phase gates), helix-integration-debt (debt level), helix-detail-finalize (manufacturing package)
- Writes to: bridge-dashboard (deployment status per product), forge-portfolio (deployment maturity), bridge-risk-radar (deployment without evidence = RED flag, missing governance docs = YELLOW flag)

## Metrics

- Phase compliance: % products with all prior phase evidence present (target: 100%)
- Skip detection: count of phases skipped across all products (target: 0)
- Gate cycle time: days from gate request to GO/NO-GO decision

## COD Classification

- Checklist compilation: Offload (O1) — AI assembles evidence
- Evidence gathering: Offload (O1) — AI collects artifacts
- Gap identification: Offload (O2) — AI flags, CEO reviews
- GO/NO-GO decision: Core (C) — CEO decides, no delegation
