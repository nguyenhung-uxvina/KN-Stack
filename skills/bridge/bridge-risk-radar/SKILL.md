---
name: bridge-risk-radar
description: Early warning system for organizational, product, and strategic risks at Workshop X. This skill should be used when the user asks about risks, warnings, potential problems, or what could go wrong. Scans vault data to classify risks as RED/YELLOW/GREEN. Triggers on risk, warning, rui ro, van de tiem an, what could go wrong.
---

# Bridge Risk Radar — Early Warning System

Scan all vault data sources to detect organizational, product, and strategic risks before they become incidents. Output a RED/YELLOW/GREEN risk register with top risk and recommended action.

## When to Use

- Weekly risk review (feeds bridge-dashboard metric #7)
- Before major decisions (risk context check)
- When asked "what could go wrong?" or "rui ro gi?"
- After project status changes or gate reviews
- When capacity or resource concerns arise

## Workflow

### Step 1: Scan Data Sources

Read all available vault data:
- `1_Projects/*/Status.md` — project health, blocking constraints, dP/dt
- `2_Areas/` dashboards — area health indicators
- Galaxy notes — systemic pattern warnings
- Recent gate reviews — evidence gaps
- KB coverage — knowledge distribution

### Step 2: Classify Risks

**Organizational Risks:**

| Risk Type | Signal | Source |
|-----------|--------|--------|
| Key-person dependency | Engineer X sole owner of N products | bridge-talent-map |
| Knowledge loss | Senior engineer leaving, KB capture incomplete | bridge-knowledge-base gap |
| Capacity overload | Hours/week split across too many products | HELIX project data |
| Skill gaps | No one knows critical capability | bridge-signal-extract patterns |

**Product Risks:**

| Risk Type | Signal | Source |
|-----------|--------|--------|
| Deployment without evidence | Product at Phase N but Phase N-1 incomplete | bridge-deploy-gate |
| Integration debt rising | Multiple products with unresolved ICDs | helix-integration-debt |
| Fallback missing | Product at Fallback Level 0 | forge-fallback |
| Validation gap | Model not revalidated in 6+ months | forge-validate schedule |

**Strategic Risks:**

| Risk Type | Signal | Source |
|-----------|--------|--------|
| Compound stalling | 0 model transfers in 90 days | forge-library |
| Trust decay | Customer no contact in 60+ days | forge-trust tracker |
| Analyst Trap | CEO 80%+ time on analysis, 0% prototypes | bridge-judgment log |
| Shifting the Burden | Solving symptoms not root causes 3+ times | bridge-flywheel patterns |

### Step 3: Score Severity

For each identified risk, score as:
- **RED** — Immediate action required (safety, deployment, key-person loss)
- **YELLOW** — Trending toward problem (debt, capacity, trust erosion)
- **GREEN** — Monitored, under control

Scoring formula: Impact x Likelihood x Urgency

### Step 4: Generate Risk Register

```
## Risk Radar — [Date]

### RED Alerts (N)
| # | Risk | Category | Impact | Action Required |
|---|------|----------|--------|-----------------|

### YELLOW Warnings (N)
| # | Risk | Category | Trend | Mitigation |
|---|------|----------|-------|------------|

### GREEN Monitored (N)
| # | Risk | Category | Last Checked |
|---|------|----------|-------------|

TOP RISK: [description]
RECOMMENDED ACTION: [specific, actionable, completable this week]
```

### Step 5: Route Output

- Feed RED/YELLOW/GREEN counts to bridge-dashboard metric #7
- Flag any new RED risks for immediate CEO attention
- Track risk resolution over time

## Integration Points

- Receives from: bridge-talent-map, bridge-knowledge-base, bridge-deploy-gate, HELIX project data, FORGE validate/fallback/trust
- Feeds into: bridge-dashboard (metric #7), CEO weekly digest

## Metrics

- Risk detection lead time: days before risk becomes incident (longer is better)
- Risk resolution rate: % RED risks resolved within 2 weeks (target: >80%)
- False positive rate: % flagged risks that were non-issues (target: <20%)

## COD Classification

- Data scanning: Offload (O1) — AI scans vault
- Risk classification: Offload (O2) — AI classifies, CEO validates
- Severity scoring: Offload (O2) — AI proposes, CEO confirms
- Response decision: Core (C) — CEO decides action
