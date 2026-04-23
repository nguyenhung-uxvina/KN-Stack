---
name: forge-flywheel
description: Monitor and accelerate the ACH data flywheel — field data collection, model retraining, and compound tracking across the portfolio. This skill should be used when the user asks about "data flywheel", "compound tracking", "field data pipeline", "model retraining", "R1 flywheel", "du lieu thuc dia", or "vong quay du lieu". Stage 3-4 continuous improvement engine.
---

# Forge Flywheel — Data Flywheel & Compound Tracking

Monitor and steer the ACH data flywheel: deployed products generate field data → data improves models → better models improve products → more sales → more deployments. Track compound metrics across the portfolio. This is the engine that makes ACH investment compound over time.

## When to Use

- Monthly flywheel health check (part of FORGE protocol)
- When model performance drift is detected
- When deciding whether to retrain a model
- Quarterly compound assessment (feeds forge-evolve)

## The Flywheel

```
DEPLOY product with AI ──> Field data collected via telemetry
       ^                              |
       |                              v
Better model retrained <── Data improves training set
       |                              |
       |                              v
Model updated <──────── New model validated (forge-validate)
       |
       v
Product performance improves ──> Customer trust increases
       |                              |
       v                              v
More products deployed <──── More contracts won
```

## Workflow

### Step 1: Monitor Flywheel Health

```
FLYWHEEL HEALTH REPORT — Workshop X
Date: {{today}}

## DATA COLLECTION
| Product | Deployed Units | Data Rate | Quality | Pipeline Status |
|---------|:-------------:|-----------|---------|----------------|
| | | GB/month | % usable | Active/Stalled/None |

Total data collection: __ GB/month
Data quality (usable for retraining): __%

## MODEL UPDATE CYCLE
| Model ID | Last Retrained | Performance Delta | Next Scheduled |
|----------|:-------------:|:-----------------:|:--------------:|
| | {{date}} | +/- % | {{date}} |

Model updates this quarter: __ (target: 1)

## FLYWHEEL SPEED
Formula: (insights acted on / insights generated) x (1 / avg days to action)

| Metric | Value | Trend |
|--------|-------|-------|
| Insights generated (from field data) | | |
| Insights acted on (model updates, design changes) | | |
| Average days from insight to action | | |
| Flywheel speed | | UP/FLAT/DOWN |

## COMPOUND METRICS
| Metric | Current | 3M Ago | Trend |
|--------|---------|--------|-------|
| Portfolio Compound Score | | | |
| Library size (forge-library) | | | |
| Total transfers | | | |
| Transfer success rate | | | |
| Cost reduction from reuse | | | |
| New capabilities from retraining | | | |

## ALERTS
- [RED] Flywheel stalled: data collection dropped >50%
- [YELLOW] No model updates in 90 days
- [YELLOW] Data quality below 50% usable
- [GREEN] Flywheel accelerating
```

### Step 2: CEO Steering (Core)

CEO makes strategic flywheel decisions:
- Prioritize: which data is most valuable to collect?
- Decide: retrain now or wait for more data?
- Allocate: team capacity for flywheel vs new products
- Strategic: "Deploy more units to generate more data?"

### Step 3: Identify Flywheel Blockers

Common blockers and interventions:

| Blocker | Signal | Intervention |
|---------|--------|-------------|
| No telemetry designed in | Data rate = 0 | Retrofit telemetry (costly) or wait for next revision |
| Data quality too low | < 50% usable | Improve data pipeline, add filtering |
| No retraining capacity | Model stale > 6 months | Allocate compute + engineer time |
| Customer won't share data | Political/legal block | Negotiate data agreement (Core) |
| Model improvement plateaued | Delta < 1% per retrain | Shift to new model architecture or new data source |

### Step 4: Compound Projection

Estimate future compound value:
- If flywheel continues at current speed: {{projection}}
- If flywheel stalls: {{cost of lost compound}}
- Investment needed to accelerate: {{resources}}

## HELIX Integration

```
forge-flywheel READS FROM HELIX:
  - Deployed product specs → what telemetry is available
  - Design journal → known data quality issues
  - Integration debt → data pipeline interfaces

forge-flywheel WRITES TO:
  - forge-portfolio → compound metrics for dashboard
  - forge-library → model update triggers
  - forge-evolve → flywheel speed as moat metric
  - bridge-dashboard → flywheel health metric
```

## Rules

- Telemetry must be designed INTO products (DfU) — retrofit is 10x more expensive
- Field data is the moat — treat data pipeline as critical infrastructure
- Flywheel speed matters more than absolute metrics — acceleration = compounding
- 0 model updates in 90 days = flywheel dormant → RED alert
- Customer data agreements are Core — CEO negotiates, not AI

## COD Classification

- Flywheel health monitoring: Offload (O1) — AI tracks metrics
- Data quality analysis: Offload (O2) — AI identifies issues
- Retrain decision: **Core (C)** — CEO allocates resources
- Customer data negotiation: **Core (C)** — relationship-dependent
- Compound projection: Offload (O2) — AI models, CEO validates
