---
name: forge-shift
description: ACH (AI-Compensates-Hardware) Go/No-Go assessment using the SHIFT checklist. This skill should be used when the user asks to "evaluate ACH", "run SHIFT assessment", "should this product use AI instead of hardware?", "go/no-go ACH", "ACH assessment", or "co nen dung AI thay hardware?". The most critical FORGE decision skill.
---

# Forge SHIFT — ACH Go/No-Go Assessment

Evaluate whether a specific product sub-function should apply the ACH design principle (replace expensive/imported hardware with AI + commodity sensors). Output a SHIFT scorecard with GO / CONDITIONAL GO / NO-GO recommendation for CEO decision.

## When to Use

- Before committing to ACH for any product sub-function
- When forge-scout identifies a high-potential ACH opportunity
- When revisiting an existing ACH decision after new evidence
- During Phase 1 Task Clarification when AI vs hardware trade-off arises

## Workflow

### Step 1: Gather Context

Read project artifacts:
- `1_Projects/{{project}}/Status.md` — current phase and constraints
- `1_Projects/{{project}}/_Project_Brief.md` — requirements and customer context
- Any ODI report, Phase 0/1 artifacts, or morphological matrix
- forge-scout output if available (ACH Opportunity Matrix)

If no project specified, ask:
1. What product or sub-function is being evaluated?
2. What is the current non-ACH baseline?
3. Who is the target customer?

### Step 2: Run SHIFT Checklist

For the target sub-function, evaluate each SHIFT dimension:

```
SHIFT SCORECARD — {{product}} / {{sub-function}}
Date: {{today}}

S — SUBSTITUTABLE?
  Physics test: "Is the information present in cheap sensor data?"
  Evidence: [search papers, patents, existing implementations]
  Score: PASS / MARGINAL / FAIL
  Notes:

H — HYBRID POSSIBLE?
  "Can AI + commodity sensor replace expensive specialized sensor?"
  Candidate hybrid architectures:
  Score: PASS / MARGINAL / FAIL
  Notes:

I — IMPROVEMENT TRAJECTORY?
  dA/dt (AI capability growth rate for this task):
  dH/dt (hardware improvement rate):
  Crossover estimate: "AI surpasses hardware by 20XX"
  Score: PASS (dA/dt >> dH/dt) / MARGINAL / FAIL

F — FALLBACK FEASIBLE?
  Level 0: No fallback         → FAIL (unacceptable for defense)
  Level 1: Manual override     → MARGINAL
  Level 2: Graceful degradation → PASS
  Level 3: Redundant path      → STRONG PASS
  Required fallback level:
  Score: PASS / MARGINAL / FAIL
  → If MARGINAL or PASS: trigger forge-fallback for architecture design

T — TRAINING DATA?
  Available datasets:
  Synthetic generation feasible?
  Field collection plan:
  Score: PASS (rich) / MARGINAL (moderate) / FAIL (scarce)

O — OUTCOME-ALIGNED? ★ (requires forge-job-map data)
  Which customer desired outcomes does this ACH address?
  Outcome IDs: [list from forge-job-map Opportunity Landscape]
  Opportunity scores of addressed outcomes:
  Number of top-15 underserved outcomes addressed: __/15
  Assessment:
    ✅ HIGH: addresses top-5 underserved outcome (opp score ≥ 8.0)
    ⚠️ MEDIUM: addresses top-15 underserved (opp score 6.0-7.9)
    ❌ LOW: no underserved outcome addressed → question value
    🔴 RED FLAG: addresses OVERSERVED outcome → gold-plating risk
  Score: ✅ / ⚠️ / ❌
  Notes:
  If no forge-job-map data exists: Score: N/A — "Run /forge-job-map first for outcome data"
```

### Step 3: ACH Economics Quick-Check

Link to forge-cost for full analysis. Generate summary:

| Category | Hardware Alternative | ACH Solution | Delta |
|----------|---------------------|-------------|-------|
| Unit cost (defense-grade) | | | |
| Import/supply chain risk | | | |
| Capability premium | | | |
| Reuse multiplier (N products) | | | |
| Local content impact | | | |

### Step 4: Generate Decision Package

```
SHIFT ASSESSMENT SUMMARY — {{product}} / {{sub-function}}

SCORECARD:
  S: [PASS/MARGINAL/FAIL]
  H: [PASS/MARGINAL/FAIL]
  I: [PASS/MARGINAL/FAIL]
  F: [PASS/MARGINAL/FAIL]
  T: [PASS/MARGINAL/FAIL]
  O: [✅/⚠️/❌/N/A] — Outcome alignment (from forge-job-map)

OUTCOME SUMMARY (if O data available):
  Outcomes addressed: {{N}} of top-15 underserved
  Combined opportunity score: {{sum}}/{{max}}
  If ACH succeeds → moves {{N}} outcomes from underserved to served

ECONOMICS: [favorable / neutral / unfavorable at WX volumes]
CAPABILITY PREMIUM: [description of features impossible with hardware]
REUSE VALUE: [model serves N products from forge-scout synergy]

RISK: "If AI fails in this product, consequence = ___"
  - Lose contract → recoverable → acceptable
  - Lose MoD trust → catastrophic → need Level 2+ fallback
  - Safety incident → unacceptable → NO-GO unless Level 3

RECOMMENDATION: GO / CONDITIONAL GO / NO-GO
CONDITIONS (if conditional):
```

### Step 5: CEO Decision (Core — Non-Delegable)

Present the decision package. WAIT for CEO to:
- Review SHIFT scorecard
- Factor in: customer relationship, political context, team capacity
- Apply gut check: "If AI fails here, what happens?"
- Declare: **GO / NO-GO / GO with conditions**

Record decision in project Status.md.

## HELIX Integration

```
forge-shift READS FROM HELIX:
  - Function structure → WHERE AI replaces hardware
  - Requirements → accuracy/reliability thresholds
  - Concept evaluation → existing ACH in concept?

forge-shift WRITES TO HELIX:
  - "ACH APPROVED for sub-function X" → new requirement
  - "Fallback Level N required" → new constraint
  - "Model WX-XXX-NNN applicable" → concept option
  - "Training data plan needed" → project task
```

## Gotchas (from production use)

1. **T=MARGINAL is acceptable IF lab demonstrator gate exists** — VN-USV-SS-001 got ACH GO with T=MARGINAL because $140 lab demonstrator generates first training data BEFORE Phase 2 lock. Without physical gate → T=MARGINAL should be NO-GO. (Source: Session 52)
2. **Level 2 fallback can be INHERENT in design** — NC (normally-closed) ballast valve = auto-surface on fault = Level 2 fallback without extra engineering. Look for physics-based fallbacks, not just software fallbacks. (Source: VN-USV-SS-001 SHIFT)
3. **Don't confuse consumer pricing with defense pricing** — "$300 vs $10K" is unit cost. Add MIL-STD qualification, lifecycle, spares → real delta may be 60%, not 97%. Use forge-cost for accurate comparison. (Source: ACH Economics Trap)
4. **ACH Boundary Rule is HARD** — AI works on INFORMATION (scoring, coaching, navigation). AI does NOT work on PHYSICAL FORCES (recoil, structural loads, buoyancy). If sub-function is physical → NO-GO for ACH, no exceptions. (Source: [[ACH Boundary Rule]])
5. **"Technological infanticide" risk** — Position ACH as "complement" not "replacement" to customer. Military customers fear AI replacing their equipment/roles. (Source: [[Technological Infanticide]])

## Rules

- Never auto-approve ACH — always present for CEO decision
- Any SHIFT dimension = FAIL → overall recommendation must be NO-GO or CONDITIONAL
- Fallback Level 0 = automatic NO-GO for defense products
- If TRL < 4 for AI/ML component, flag as HIGH risk
- Goldilocks Disclosure applies: assessment may contain proprietary strategy
- Link to Galaxy: [[Phan doan khong the uy thac cho AI]] — this IS a judgment call

## COD Classification

- SHIFT checklist population: Offload (O2) — AI runs checklist
- Economics calculation: Offload (O1) — AI computes
- GO/NO-GO decision: **Core (C)** — CEO decides, accountable
- Risk acceptance: **Core (C)** — defense context requires human judgment
