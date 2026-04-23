Build a System Dynamics stock-and-flow model for deep quantitative analysis.

Usage: /sdmodel [system_description] OR provide details interactively.

1. If $ARGUMENTS provided, use as system description; otherwise ask:
   - What system are you modeling? (product pipeline, org capacity, market dynamics, etc.)
   - What behavior are you trying to explain or predict? (growth, oscillation, collapse, plateau)
   - What time horizon? (weeks, months, quarters, years)
   - What decisions depend on this model?

2. Build the System Dynamics model:

```
# SYSTEM DYNAMICS MODEL — {{system}}
**Date:** {{today}}  |  **Horizon:** {{timeframe}}  |  **Purpose:** {{decision it informs}}

---

## 1. MODEL BOUNDARY
### Endogenous (inside model)
| Variable | Type | Units |
|----------|------|-------|
| | Stock / Flow / Auxiliary | |

### Exogenous (inputs/assumptions)
| Variable | Value | Source | Sensitivity |
|----------|-------|--------|-------------|
| | | | H/M/L |

### Excluded (consciously omitted)
| Variable | Why Excluded |
|----------|-------------|
| | |

---

## 2. STOCKS (Accumulations)
| Stock | Initial Value | Units | Description |
|-------|--------------|-------|-------------|
| S1 | | | |

## 3. FLOWS (Rates of change)
| Flow | Direction | Equation | Units/time |
|------|-----------|----------|-----------|
| F1 | Inflow to S1 | | |
| F2 | Outflow from S1 | | |

## 4. AUXILIARIES (Intermediate calculations)
| Auxiliary | Equation | Depends On |
|-----------|----------|-----------|
| A1 | | |

---

## 5. STOCK-FLOW DIAGRAM (Text)

```
                    F1 (inflow)
                        |
                        v
[Source] -----> [ S1: Stock Name ] -----> [Sink]
                        ^        F2 (outflow)
                        |
                   A1 (auxiliary)
                        |
                   [feedback from S2]
```

---

## 6. FEEDBACK LOOPS
| Loop | Type | Variables | Dominance |
|------|------|-----------|-----------|
| R1 | Reinforcing | S1 -> F1 -> S1 | Dominant early |
| B1 | Balancing | S1 -> F2 -> S1 | Dominant late |

---

## 7. BEHAVIOR OVER TIME (Qualitative)
```
Value
  ^
  |     /-------- (plateau)
  |    /
  |   /
  |  /
  | /
  |/________________> Time
  0    T1    T2    T3
```
**Reference mode:** {{describe the expected behavior pattern}}
**Key transitions:** T1 = {{event}}, T2 = {{event}}

---

## 8. SENSITIVITY ANALYSIS
| Parameter | Base | Low (-20%) | High (+20%) | Impact on Key Output |
|-----------|------|-----------|------------|---------------------|
| | | | | H/M/L |

**Most sensitive parameters:** {{top 3 — these need validation}}

---

## 9. POLICY EXPERIMENTS
| # | Policy | What Changes | Expected Effect | Side Effects |
|---|--------|-------------|-----------------|-------------|
| P1 | Do nothing (baseline) | — | {{trajectory}} | — |
| P2 | {{intervention}} | {{parameter change}} | | |
| P3 | {{intervention}} | {{parameter change}} | | |

---

## 10. MODEL LIMITATIONS
- What does this model NOT capture?
- Where are the weakest assumptions?
- What data would improve confidence?
```

3. Present model to user. Do NOT auto-implement policy recommendations.

RULES:
- Keep models small: 3-5 stocks maximum — complex models are wrong models
- Every stock must have at least one inflow AND one outflow
- Every feedback loop must be named and classified (R or B)
- Sensitivity analysis is mandatory — models without it are false precision
- COD: Offload (AI builds model, CEO validates structure and assumptions)
- Quarterly use: this is heavy analysis, not for weekly sessions
- Reference: Sterman "Business Dynamics", Meadows "Thinking in Systems"
