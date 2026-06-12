---
name: forge-validate
description: Design and track validation infrastructure for ACH products — lab, field, and continuous monitoring. Now includes THESIS mode for portfolio-wide ACH thesis validation. This skill should be used when the user asks to "validate AI product", "test AI performance", "prove it works", "performance envelope", "defense validation", "validation plan for ACH", "chung minh AI hoat dong", "ACH thesis validation", "validate thesis", or "quarterly ACH scorecard". Builds the evidence that defense customers require.
---

# Forge Validate — ACH Validation Infrastructure

Design a staged validation plan for ACH products: Lab → Field Simulation → Operational Test → Continuous Monitoring. Output: validation plan with Performance Envelope, pass/fail criteria, and monitoring setup. Builds the trust evidence that defense customers demand.

## When to Use

- After HELIX Phase 3-4 produces testable hardware (Sync S5 trigger)
- When forge-portfolio flags missing Performance Envelope
- Before customer demonstrations (forge-trust needs evidence)
- When model performance drift is suspected

## Validation Stages

| Stage | Environment | Purpose | Prerequisite |
|-------|------------|---------|-------------|
| 1 — Lab | Controlled | Baseline vs. requirements | HELIX Gate 4 passed |
| 2 — Field Sim | Realistic but controlled | Environmental robustness | Stage 1 PASS |
| 3 — Operational | Real environment, real operators | User acceptance | Stage 2 PASS |
| 4 — Continuous | Deployed products | Drift detection | Stage 3 PASS + telemetry |

## Workflow

### Step 0: Guard Rail Pre-Check — Iron Law (gstack Ch08)

> Pattern source: gstack Guard Rail + Iron Law — "no build starts without an approved plan that passes defined criteria." Adapted here: no validation plan is designed for a product that hasn't cleared minimum readiness criteria.

**Run before any other step. HALT immediately if any guard fails.**

```
GUARD RAIL CHECK — {{product}} / {{sub-function}}
Date: {{today}}

G1 — Quantitative requirements exist?
  □ HELIX requirements list includes at least 3 measurable pass/fail criteria for this sub-function
  □ Criteria are in number + unit form (not "adequate" or "robust")
  Status: [PASS / FAIL — return to helix-p1-requirements to define criteria first]

G2 — Fallback defined?
  □ forge-fallback spec exists OR product-level fallback behavior is documented
  □ Fallback has its own pass/fail criteria (not "AI fails → human takes over" without definition)
  Status: [PASS / FAIL — run forge-fallback before forge-validate]

G3 — HELIX Gate 4 passed (or equivalent testable state)?
  □ Hardware exists in sufficient form that Stage 1 lab test is physically possible
  □ Status.md shows Gate 4 PASS or "Stage 1 pre-gate approved"
  Status: [PASS / FAIL — validation plan is premature; re-trigger at Sync S5]

G4 — Learning Loop Architecture feasibility?
  □ Ground-truth signal (Step 1.5 GT1) is identifiable — not AI-judging-AI
  □ GT1 latency is acceptable for development cadence (GT2 reasonable)
  Status: [PASS / FAIL — GT1 not identifiable: flag as architectural blocker for CEO]

GUARD RAIL RESULT:
  All 4 PASS  → Proceed to Step 1
  Any FAIL    → HALT. Record failed guard(s) in Status.md.
                Return to: {{upstream skill}} to resolve before re-running forge-validate.

IRON LAW: No validation plan is designed for an unready product.
          Cost of a premature plan = wasted CEO time + misleading evidence.
```

**COD:** Offload (O1) — AI reads project files and checks. CEO confirms GT1 (G4) is realistic.

### Step 1: Gather Context

Read:
- forge-shift SHIFT assessment → what was promised
- forge-fallback spec → fallback must be tested too
- HELIX requirements list → quantitative pass/fail criteria
- HELIX design journal → known issues to cover in test plan

### Step 1.5: Define Outcome-Linked Learning Loop Architecture

**Purpose:** Before designing the test plan, define the architectural separation between *decision flow* (what deployed AI does in the field, real-time) and *learning flow* (how field outcomes update the model, offline). Without this up front, Stage 4 silently degrades into "model judges itself" — endogenous noise loops that look like learning but aren't.

**Pattern source:** TradingAgents (arXiv:2412.20138) Ch 7-8 — outcome-linked offline learning. P&L is the ground-truth signal; reflection happens offline after trades settle; memory is read-only during decision, write-only during reflection. Defense / sensor-noisy contexts: same shape (mission-result feedback, calibration accuracy, hit-rate).

**Mandatory: define 4 entries before Stage 1 begins.**

| Entry | Question | Example (BB-01 LOMAH) |
|-------|----------|----------------------|
| **GT1 — Ground truth signal** | What externally-determined truth arrives late from the field? Must NOT come from the AI itself. | Operator-confirmed shot-call accuracy from range exercises (instrument-measured, T+days) |
| **GT2 — Arrival latency** | How long after a decision does ground truth arrive? Drives offline batch cadence. | 1-7 days per range exercise; quarterly aggregate |
| **GT3 — Read/write boundary** | Where in the runtime is AI ALLOWED to read memory? FORBIDDEN to write? Where is the offline writer? | Edge inference: read-only on model weights + lookup table. Offline retraining (after each exercise): write-only into next model version. No in-loop self-update. |
| **GT4 — Cold-start behavior** | First N deployments: ground-truth backlog is empty. What does AI output? Must be sensible without field-derived memory. | Default to Stage 1 lab calibration table; no field-derived adjustments until 3+ exercises completed. |

**Failure modes this prevents:**
- **In-loop self-judgment** — model evaluates its own output during decision (LLM-as-judge in real time, confidence-as-truth) → endogenous noise → false improvement signal → silent drift.
- **Premature first-week optimization** — Stage 4 updates model from Day 1 telemetry without waiting for ground truth → overfits to deployment artifacts (sensor seating, operator novelty) → degrades.
- **Ground truth that is model-judging-model** — "field performance" measured by another AI rather than human operators / physical instruments → loop is self-amplifying noise, not learning.
- **Indefinite-pending outcomes blocking the loop** — if ground truth never arrives (mission cancelled, exercise postponed), learning freezes. Define timeout + default behavior.

**Output:** "Learning Loop Architecture" sub-section in Validation Plan (added in Step 2). Becomes checked precondition for Stage 4 sign-off.

**Skip condition:** ACH product where field outcomes are immediate + objective (e.g., automated weight-on-target measurement, instant scoring instrument). Pattern still helps but mandatory 4-entry structure can be lighter.

**Time:** 30-60 min CEO-led, AI drafts.

**COD:** **Core** — only CEO knows what ground-truth signal is realistic for the specific defense customer's operational tempo.

### Step 2: Generate Validation Plan

```
VALIDATION PLAN — {{product}} / {{ACH sub-function}}
Date: {{today}}  |  Project: {{project}}

## VALIDATION OBJECTIVES
1. Prove ACH meets requirements from SHIFT assessment
2. Define Performance Envelope (where AI works / degrades / fails)
3. Verify fallback activation and recovery
4. Collect baseline data for continuous monitoring

## REQUIREMENTS TRACEABILITY
| Req ID | Requirement | Stage | Method | Pass Criteria |
|--------|-------------|-------|--------|---------------|
| | | 1/2/3 | I/A/D/T | quantitative |

Methods: I=Inspection, A=Analysis, D=Demonstration, T=Test

## STAGE 1: LAB VALIDATION
Test matrix:
| Test # | Name | Input | Expected Output | Pass/Fail | Duration |
|--------|------|-------|----------------|-----------|----------|

Edge case matrix:
| Condition | Expected Behavior | Fallback Triggers? |
|-----------|-------------------|-------------------|

Baseline comparison: AI vs. hardware alternative (same test conditions)

## STAGE 2: FIELD SIMULATION
Environmental variables to test:
| Variable | Range | Method |
|----------|-------|--------|
| Weather | | |
| Lighting | | |
| Vibration | | |

Adversarial testing (if applicable):
- Deception scenarios
- Jamming / countermeasures
- Degraded input quality

Fallback trigger testing: verify each FM-N from forge-fallback

## STAGE 3: OPERATIONAL FIELD TEST
- Duration: {{extended burn-in period}}
- Operators: {{real users, not developers}}
- User feedback collection method
- Comparison with operational requirements

## STAGE 4: CONTINUOUS MONITORING
- Telemetry pipeline: what data to collect
- Performance metrics tracked automatically
- Drift detection thresholds
- Alert conditions: "performance drops below X → notify CEO"
- Quarterly revalidation schedule
- **Outcome-linked learning gate (from Step 1.5):**
  - Model updates ONLY after ground truth (GT1) arrives — no in-loop self-update
  - Telemetry runs READ-ONLY on field data; writes only after ground-truth batch
  - Cold-start behavior (GT4) active until N exercises completed
  - Ground-truth timeout: if GT1 not received within {{GT2 × 2}}, escalate (do not silently fall through to model-judging-model)

## LEARNING LOOP ARCHITECTURE (from Step 1.5 — mandatory before Stage 4 sign-off)
| Entry | Definition |
|-------|-----------|
| GT1 — Ground truth signal | {{from Step 1.5}} |
| GT2 — Arrival latency | {{days/exercises}} |
| GT3 — Read/write boundary | {{description}} |
| GT4 — Cold-start behavior | {{description}} |

## PERFORMANCE ENVELOPE (output of validation)
| Condition | Performance | Category |
|-----------|------------|----------|
| {{condition A}} | {{metric}} | WORKS WELL |
| {{condition D}} | {{metric}} | DEGRADED |
| {{condition F}} | {{metric}} | FAILS → fallback |

## TEST INFRASTRUCTURE
| Item | Available? | Source | Lead Time | Cost |
|------|-----------|--------|-----------|------|

## GO/NO-GO CRITERIA
| # | Criterion | Threshold | Rationale |
|---|----------|-----------|-----------|

## SCHEDULE
| Phase | Activity | Duration | Dependencies |
|-------|----------|----------|-------------|
```

### Step 3: Execute and Analyze

- Stage 1-3 execution is PHYSICAL — Core task, AI cannot do this
- AI analyzes results: confidence intervals, failure rates, envelope generation
- AI generates defense-grade Validation Report

### Step 4: CEO Accept/Reject (Core)

CEO reviews:
- Performance Envelope acceptable for customer?
- Edge cases covered?
- Fallback tested and working?
- Decision: VALIDATED / NEEDS MORE TESTING / REJECT

## Critical Sync Point

```
HELIX Sync S5 ("First hardware available for AI testing")
= forge-validate Stage 1 START trigger

Before S5: only simulation validation possible
After S5: Stage 1-2 becomes possible
CEO must ensure S5 happens on time
```

## HELIX Integration

```
forge-validate READS FROM HELIX:
  - Detail design → what exactly is being tested
  - Gate 4 → prerequisite for Stage 1
  - Integration debt → validation covers interfaces
  - Design journal → known issues

forge-validate WRITES TO HELIX:
  - Validation results → design journal (evidence log)
  - Performance Envelope → next-version requirements
  - Anomalies → integration debt (if interface-related)
  - Telemetry needs → Phase 3 DfU requirement
```

## Rules

- Every ACH product needs a Performance Envelope — no exceptions
- "Average accuracy 95%" is insufficient — specify conditions
- Physical tests always preferred over analysis alone
- Fallback must be tested as part of validation — not separately
- Stage 4 telemetry must be designed INTO the product (DfU)
- Define Learning Loop Architecture (Step 1.5) BEFORE Stage 1 — Stage 4 read/write boundary must be designed-in, not bolted-on
- Ground truth must come from OUTSIDE the AI (operator, instrument, physical outcome) — no in-loop self-judgment, no model-judging-model

---

## MODE: THESIS — Portfolio-Wide ACH Thesis Validation (v1.0)

**When:** Validate the ACH thesis (AI-Compensates-Hardware) across the entire portfolio, not just per-product. Strategy doc notes 133 Galaxy notes but 0 validated models — critical risk.

**Usage:** `/forge-validate --thesis`

**Key difference from per-product mode:** Per-product validates one ACH sub-function. THESIS mode validates the strategic thesis that ACH works as a business model across WX's portfolio.

### ACH Thesis Precision Statement

```
THESIS: Commodity hardware + WX AI software = premium defense product performance
  at 40-60% lower cost than pure hardware alternatives,
  with compound learning from field deployment creating widening competitive moat.

SPECIFIC CLAIMS TO VALIDATE:
1. Hardware cost reduction: 30-50% for similar performance
2. Performance delivered: 80-95% of premium alternatives
3. Development speed: 2-3x faster than pure hardware path
4. Learning compound: measurable improvement per deployed unit
5. Pricing power: premium pricing despite commodity hardware
```

### 5 Validation Applications (1 per quarter minimum)

```
ACH THESIS VALIDATION MATRIX — Workshop X
Date: {{today}}  |  Quarter: Q{{N}} {{year}}

APPLICATION 1 — ATT Flight Control:
  Thesis: commodity flight controller + AI = realistic threat behavior
  Hardware: COTS autopilot (${{X}} vs MIL-grade ${{Y}})
  AI component: behavior model (RL-based threat simulation)
  Validation method: simulation comparison → prototype flight test
  Metric: behavior realism score (expert evaluation 1-10)
  Status: NOT STARTED / IN PROGRESS / VALIDATED / FAILED
  Evidence: {{description or link}}

APPLICATION 2 — UTT Signature Generation:
  Thesis: commodity transducers + AI signal synthesis = premium signatures
  Hardware: COTS acoustic/magnetic (${{X}} vs MIL-grade ${{Y}})
  AI component: signature synthesis trained on BB-01 field measurements
  Validation method: BB-01 measurement of generated vs reference signatures
  Metric: signature fidelity (correlation coefficient ≥ 0.85)
  Status: NOT STARTED / IN PROGRESS / VALIDATED / FAILED
  Evidence: {{description or link}}

APPLICATION 3 — STT-B Autonomous Behavior:
  Thesis: commodity autonomy compute + AI behavior = realistic threat simulation
  Hardware: COTS marine computer (${{X}} vs custom ${{Y}})
  AI component: tactical behavior model (FAC approach patterns)
  Validation method: sim-first → modified boat prototype → customer evaluation
  Metric: operator cannot distinguish AI vs scripted (blind test)
  Status: NOT STARTED / IN PROGRESS / VALIDATED / FAILED
  Evidence: {{description or link}}

APPLICATION 4 — MAINT-KIT Predictive Maintenance:
  Thesis: simple sensors + AI diagnostics = premium maintenance service
  Hardware: basic accelerometer/temp sensors ($50/unit)
  AI component: failure prediction from field vibration + thermal data
  Validation method: instrument 10 VN-MGM units → predict vs actual failures
  Metric: prediction accuracy ≥ 70%, false positive rate ≤ 20%
  Status: NOT STARTED / IN PROGRESS / VALIDATED / FAILED
  Evidence: {{description or link}}

APPLICATION 5 — TMS Curriculum Personalization:
  Thesis: standard sim + AI analytics = personalized training value
  Hardware: existing VN-CUAV-SIM (no change)
  AI component: performance analytics → adaptive scenario generation
  Validation method: A/B test (standard vs AI-enhanced training)
  Metric: training effectiveness improvement ≥ 15% (time to competency)
  Status: NOT STARTED / IN PROGRESS / VALIDATED / FAILED
  Evidence: {{description or link}}
```

### Quarterly ACH Scorecard

```
ACH SCORECARD — Q{{N}} {{year}}

| # | Application | Validated? | Evidence | Hardware Cost % | Performance % | Compound? |
|---|------------|-----------|----------|----------------|--------------|----------|
| 1 | ATT Flight Control | | | /100 vs benchmark | /100 vs premium | Y/N |
| 2 | UTT Signature | | | /100 vs benchmark | /100 vs premium | Y/N |
| 3 | STT-B Behavior | | | /100 vs benchmark | /100 vs premium | Y/N |
| 4 | MAINT-KIT | | | /100 vs benchmark | /100 vs premium | Y/N |
| 5 | TMS Curriculum | | | /100 vs benchmark | /100 vs premium | Y/N |

Validated this quarter: __/1 target
Cumulative validated: __/5
Thesis confidence: LOW (<2) / MEDIUM (2-3) / HIGH (4-5)

⚠️ COMMITMENT: 1 model validation per quarter (from strategy doc)
```

### ACH Risk Analysis

```
ACH THESIS RISK REGISTER

| Risk | Likelihood | Impact | Mitigation | Status |
|------|-----------|--------|-----------|--------|
| A — Insufficient data | M | H | Partnerships for data, synthetic augmentation | |
| B — Commoditization | M | M | Proprietary data moat, compound learning | |
| C — Customer skepticism | H | H | Demonstrations, evidence, case studies | |
| D — Talent limitation | H | M | Academic partnerships, remote, training pipeline | |
| E — Integration complexity | M | M | Phased approach, strong testing | |

THESIS FAILURE MODES:
- If hardware cost reduction < 20% → ACH = cost increase, need strategic value justification
- If performance < 70% of premium → customer rejection risk
- If no compound learning after 2 quarters → moat claim invalid
- If all 5 applications fail → thesis fundamentally wrong → strategy pivot required

PROTECTION STRATEGY:
- Trade secrets preferred over patents (enforcement cost > benefit)
- Continuous learning widens gap over time
- Publish general principles (reputation) but keep implementations secret
- Academic partnerships for talent pipeline + credibility
```

### Step 5: CEO Review (Core — non-delegable)

CEO validates:
- Which application to validate THIS quarter?
- Resources allocated (embedded in product development)?
- Evidence bar acceptable?
- Decision: CONTINUE / PIVOT / ESCALATE

Save to: `2_Areas/FORGE/ACH-Design-Principle/ACH_Thesis_Scorecard_{{date}}.md`

→ Feed to forge-evolve (moat assessment) and forge-portfolio (FORGE SCORE dimension O)

---

## COD Classification

- Validation plan design: Offload (O2) — AI designs plan
- Test execution: **Core (C)** — physical, non-delegable
- Results analysis: Offload (O1) — AI processes data
- Accept/reject decision: **Core (C)** — CEO accountable
- Thesis-level validation: **Core (C)** — strategic, CEO judges evidence bar
