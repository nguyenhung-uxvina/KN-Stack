---
name: bridge-flywheel
description: Measure and accelerate the R1-WX insight-to-action cycle across Workshop X. This skill should be used when the user wants to check flywheel health, measure cycle time, identify where insights get stuck, or improve the system evolution rate. Triggers on flywheel, R1-WX, cycle time, evolution, improve system, cai thien.
---

# Bridge Flywheel — R1-WX Insight Cycle Measurement

Measure and compress the insight-to-action cycle. The flywheel is the Compound Law in action: BRIDGE generates insights, FORGE validates them, HELIX implements them, and the cycle repeats faster each time.

## When to Use

- Monthly flywheel review
- When bridge-dashboard metric #6 (R1-WX Speed) needs updating
- When insights seem to get stuck (generated but not acted on)
- When questioning whether the system is actually improving
- Quarterly trend analysis

## The R1-WX Flywheel

```
DEPLOY product --> FIELD DATA collected (bridge-signal-extract)
       ^                        |
       |                        v
BETTER DESIGN     INSIGHTS extracted (bridge-knowledge-base)
(HELIX cycle)              |
       ^                        v
       |               DESIGN CHANGES proposed
       |                        |
       +------------------------+

CURRENT CYCLE TIME: 12-24 months (estimate)
TARGET: 4-6 months
```

## Workflow

### Step 1: Measure Flywheel Components

For each stage, count and track:

| Stage | Question | Source | Count |
|-------|----------|--------|-------|
| GENERATE | How many insights extracted this month? | bridge-signal-extract outputs | |
| DELIVER | How many insights reached the right person? | KB utilization + decision log | |
| ACT | How many insights became design changes? | helix-design-journal entries linked to insights | |
| VALIDATE | How many design changes validated in field? | forge-validate results | |
| COMPOUND | How many improvements transferred across products? | forge-library + bridge-cross-learn | |

### Step 2: Calculate Conversion Rates

```
GENERATE --> DELIVER: __% (insights that reached someone)
DELIVER  --> ACT:     __% (insights that became changes)
ACT      --> VALIDATE:__% (changes that got tested)
VALIDATE --> COMPOUND:__% (validated changes transferred)
```

The lowest conversion rate is the bottleneck.

### Step 3: Identify Bottleneck

| Bottleneck | Symptom | Root Cause Options |
|-----------|---------|-------------------|
| GENERATE | Few insights extracted | Low signal capture rate, few interactions |
| DELIVER | Insights not reaching team | KB not used, routing broken |
| ACT | Insights not becoming changes | Capacity, priority, no conversion process |
| VALIDATE | Changes not tested | No test opportunity, validation backlog |
| COMPOUND | No cross-product transfer | Siloed products, no cross-learn sessions |

### Step 4: Steer Flywheel (CEO decides)

Present bottleneck analysis to CEO:
- "Bottleneck is at ACTION — why aren't insights becoming changes?"
- Root cause options: capacity, priority, or process gap
- CEO decides intervention

### Step 5: Track Compression

- Monthly: R1-WX Speed metric
- Quarterly: cycle time trend (compressing or expanding?)
- Annual: comparison to industry benchmarks

```
R1-WX Speed = (Insights Acted On / Insights Generated) x (1 / Avg Days to Action)
```

Higher is better. Track trend over time.

## Integration Points

- Orchestrates: bridge-signal-extract (GENERATE), bridge-knowledge-base (DELIVER), HELIX skills (ACT), forge-validate (VALIDATE), forge-library + bridge-cross-learn (COMPOUND)
- Feeds into: bridge-dashboard (R1-WX Speed metric #6)
- Receives from: all BRIDGE, FORGE, and HELIX skills

## Metrics

- R1-WX Speed: composite metric (higher = faster cycle)
- Stage conversion rates: % at each GENERATE/DELIVER/ACT/VALIDATE/COMPOUND transition
- Cycle time: months from insight to validated design change (target: 4-6 months)
- Bottleneck stage: which stage is currently constraining

## COD Classification

- Measurement: Offload (O1) — AI counts and calculates
- Bottleneck identification: Offload (O2) — AI identifies, CEO validates
- Steering decisions: Core (C) — CEO decides intervention
- Cycle time tracking: Offload (O1) — deterministic
