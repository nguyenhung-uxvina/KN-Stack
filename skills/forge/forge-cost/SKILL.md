---
name: forge-cost
description: Edge-realistic defense cost analysis comparing ACH vs hardware alternatives. This skill should be used when the user asks about "ACH cost", "chi phi ACH", "cost analysis", "breakeven volume", "defense costing", "so sanh gia AI vs hardware", or "is ACH worth it financially?". Prevents consumer-pricing mistakes in defense context.
---

# Forge Cost — Edge-Realistic Defense Cost Analysis

Generate a defense-realistic cost comparison between ACH (AI + commodity sensors) and hardware alternatives. Prevents the common trap of using consumer pricing for defense products. Includes strategic value dimensions beyond unit economics.

## When to Use

- During forge-shift (SHIFT Step 2: Economics Quick-Check)
- Monthly portfolio review (are cost assumptions still valid?)
- Before customer pricing discussions
- When evaluating make-vs-buy decisions for ACH components

## Critical Warning

```
ACH ECONOMICS TRAP:
Consumer costing:  "ACH saves $500/unit"     ← MISLEADING
Defense costing:   "Breakeven ~30-100 units"  ← REALISTIC
Workshop X volume: "<10 prototypes"           ← ACH may be NET COST INCREASE

Justify ACH by STRATEGIC VALUE + COMPOUND POTENTIAL,
NOT by unit cost savings at Workshop X volumes.
```

## Workflow

### Step 1: Gather Data

Read:
- `1_Projects/{{project}}/Status.md` — cost targets
- `1_Projects/{{project}}/_Project_Brief.md` — requirements, volume estimates
- BOM if available (Phase 3 embodiment)
- forge-shift assessment — what alternatives were compared

### Step 2: Generate Cost Comparison

```
COST ANALYSIS — {{product}} / {{sub-function}}
Date: {{today}}  |  Project: {{project}}

## HARDWARE ALTERNATIVE
| Cost Element | Amount | Notes |
|-------------|--------|-------|
| Unit cost (defense-grade, NOT consumer) | | MIL-spec pricing |
| Import cost (customs, export license, shipping to VN) | | |
| Integration cost (adapt to WX product) | | NRE |
| Lifecycle cost (maintenance, calibration, spares/10yr) | | |
| Supply chain risk cost (sanctions, embargo probability) | | qualitative |
| **TOTAL hardware (unit + lifecycle)** | | |

## ACH SOLUTION
| Cost Element | Amount | Notes |
|-------------|--------|-------|
| Compute hardware (defense-rated board) | | CM4/Jetson/etc |
| Sensor cost (commodity camera, mic, IMU) | | COTS |
| Development cost (model dev, NRE) | | amortized over N units |
| Validation cost (testing infrastructure) | | from forge-validate |
| Deployment cost (integration, firmware, field update) | | per unit |
| Continuous monitoring cost (telemetry, retraining/yr) | | annual |
| Reuse credit: dev cost shared across N products | | from forge-scout |
| Component reuse credit: shared HW ÷ N products | | from forge-library Step 6 |
| **TOTAL ACH (unit + lifecycle)** | | |

## COMPARISON
| Metric | Hardware | ACH | Delta |
|--------|----------|-----|-------|
| Unit cost | | | |
| 10-year lifecycle | | | |
| Breakeven volume | N/A | {{units}} | |
| At WX volumes (<10) | | | {{+/-}} |

## STRATEGIC VALUE (beyond unit economics)
| Dimension | Value | Score (1-5) |
|-----------|-------|:-----------:|
| Capability premium (features impossible w/ hardware) | | |
| Reuse compound (model serves N products) | | |
| Local content (% domestic sourcing change) | | |
| Supply chain independence (no export control risk) | | |
| Data flywheel (field data improves product over time) | | |

## SENSITIVITY ANALYSIS
| If... | Then... |
|-------|---------|
| Production volume doubles | Breakeven shifts from __ to __ |
| Talent cost +30% | Still viable? Y/N |
| Export controls tighten | ACH value increases by __ |
| Model reused in 3 products | Dev cost/unit drops by __% |

## VERDICT
- Economically justified at WX volumes? YES / NO / MARGINAL
- Strategically justified? YES / NO
- Overall recommendation:
```

### Step 3: CEO Interpretation (Core)

CEO factors in what numbers cannot capture:
- "Economics alone don't justify — but capability premium is decisive"
- "Local content value outweighs cost difference for this customer"
- "Supply chain independence is strategic necessity"

### Step 4: Feed Results

- To forge-shift: economics input for SHIFT assessment
- To forge-portfolio: cost reality check per product
- To customer materials: transparent cost-benefit (via forge-trust)

## Rules

- NEVER use consumer pricing for defense cost analysis
- Always include import costs, MIL-spec markup, and lifecycle
- Supply chain risk is a REAL cost — quantify or qualify it
- Reuse credit is valid ONLY if forge-library has the model cataloged
- Breakeven volume must be compared to REALISTIC WX production volume
- No supplier pricing in prompts (CLAUDE.md rule) — use ranges

## COD Classification

- Cost data compilation: Offload (O1) — AI gathers from BOM/market
- Cost comparison generation: Offload (O2) — AI calculates
- Strategic value assessment: **Core (C)** — CEO judgment
- Pricing decisions: **Core (C)** — CEO accountable
