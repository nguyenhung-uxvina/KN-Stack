Evaluate whether a product should apply the ACH (Autonomous Coaching Hardware) design principle.

Usage: /shift [product_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as product name; otherwise ask:
   - What product or system are you evaluating?
   - What is its current function (non-ACH baseline)?
   - Who is the target customer and what job are they hiring for?

2. Read project artifacts if they exist:
   - `1_Projects/{{project}}/Status.md`
   - `1_Projects/{{project}}/_Project_Brief.md`
   - Any ODI report or Phase 0 artifacts

3. Apply the ACH Go/No-Go evaluation:

```
# ACH SHIFT EVALUATION — {{product_name}}
**Date:** {{today}}

---

## 1. ACH PRINCIPLE RECAP
ACH = embedding autonomous coaching intelligence into training hardware.
The shift: from "dumb hardware + human instructor" → "smart hardware that coaches autonomously."

---

## 2. PRECONDITION CHECK (all must be YES to proceed)

| # | Precondition | Answer | Evidence |
|---|-------------|--------|----------|
| 1 | Does the product involve TRAINING or SKILL DEVELOPMENT? | Y/N | |
| 2 | Is there a measurable performance metric to coach toward? | Y/N | |
| 3 | Can sensor data capture trainee performance automatically? | Y/N | |
| 4 | Is the current instructor bottleneck real? (cost, availability, consistency) | Y/N | |
| 5 | Is the customer willing to pay for autonomous capability? | Y/N/? | |

**If any precondition = NO → ACH is NOT applicable. Stop here.**
**If precondition 5 = ? → flag as validation requirement, proceed conditionally.**

---

## 3. ACH VALUE ASSESSMENT

| Dimension | Non-ACH Baseline | With ACH | Delta |
|-----------|-----------------|----------|-------|
| Training throughput (sessions/day) | | | |
| Instructor dependency (hours/session) | | | |
| Consistency of feedback | | | |
| Data collection for improvement | | | |
| Unit cost impact | | | |
| Recurring revenue potential | | | |

---

## 4. ACH READINESS (TRL Assessment)

| Component | Required TRL | Current TRL | Gap | Risk |
|-----------|-------------|-------------|-----|------|
| Sensor subsystem | ≥6 | | | |
| AI/ML model | ≥4 | | | |
| Coaching interface | ≥5 | | | |
| Data pipeline | ≥4 | | | |

---

## 5. COMPETITIVE MOAT ANALYSIS

- Does ACH create switching costs? (data lock-in, model improvement over time)
- Does ACH enable a data flywheel? (more usage → better coaching → more usage)
- Is ACH defensible? (can competitors replicate easily?)
- Does ACH align with Workshop X IRONMESH platform?

---

## 6. GO/NO-GO DECISION

| Criterion | Score (0-4) | Weight |
|-----------|------------|--------|
| Training value-add | | 25% |
| Technical feasibility | | 20% |
| Customer willingness to pay | | 20% |
| Competitive moat | | 15% |
| IRONMESH platform fit | | 10% |
| Revenue model viability | | 10% |

**Weighted Score:** __/4.0
- ≥3.0 → GO: Apply ACH principle
- 2.0-2.9 → CONDITIONAL: Apply ACH as optional upgrade tier
- <2.0 → NO-GO: Keep as conventional hardware

**Recommendation:** {{GO / CONDITIONAL / NO-GO}}
```

4. Present evaluation to user. WAIT for CEO decision — this is a Core strategic call.

RULES:
- ACH is Workshop X's core strategic differentiator — but not every product needs it
- Never auto-approve ACH — it adds cost, complexity, and TRL risk
- If TRL < 4 for AI/ML component, flag as HIGH risk
- Goldilocks Disclosure applies: evaluation details may contain proprietary strategy
- COD: Offload (AI evaluates, CEO decides GO/NO-GO)
- Link to Galaxy: "Phán đoán không thể uỷ thác cho AI" — this IS a judgment call
