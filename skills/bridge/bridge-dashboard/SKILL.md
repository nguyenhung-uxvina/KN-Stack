---
name: bridge-dashboard
description: Generate the unified CEO Weekly Dashboard for Workshop X with 7 key metrics across BRIDGE, FORGE, and HELIX. This skill should be used when the user asks for dashboard, metrics, weekly review, how are we doing, or wants a 15-minute operational overview. Replaces the previous dash command with full BRIDGE integration.
---

# Bridge Dashboard — CEO Weekly Operational View

Generate the 7-metric CEO Dashboard in 15 minutes. The single view that tells the CEO if Workshop X is improving or degrading.

## When to Use

- Monday morning weekly review
- Before strategic decisions (context check)
- When user asks "how are we doing?"
- Monthly/quarterly trend reviews

## The 7 Metrics

### Metric 1: KB Coverage
- What: Percentage of active products with Layer 2 documentation
- Source: Scan 1_Projects/ for each active product, check artifact completeness
- Alert: RED if any Tier 1 product has no L2 docs

### Metric 2: Signal Capture
- What: Percentage of interactions with signal extraction done
- Source: Count signal reports vs. known meetings/reviews
- Alert: RED if design review capture rate falls below 50%

### Metric 3: Phase Compliance
- What: Percentage of products following deployment gate sequence
- Source: Check each product Status.md for phase evidence
- Alert: RED if ANY product deployed without prior phase evidence

### Metric 4: Time Freed
- What: Hours per week freed by automation
- Source: Track automated vs. manual task completion
- Alert: YELLOW if freed time goes to more paperwork instead of judgment work

### Metric 5: Decision Quality
- What: Ratio of documented decisions (with rationale) vs. undocumented
- Source: Count design journal entries, gate review decisions
- Alert: YELLOW if documentation rate falls below 30%

### Metric 6: R1-WX Speed
- What: Insight-to-action cycle time in months
- Source: Track from signal extraction to design change implementation
- Alert: RED if stagnant for 2+ months

### Metric 7: Risk Radar Summary
- What: Count of RED, YELLOW, GREEN risks
- Source: bridge-risk-radar output
- Alert: RED count displayed prominently with top risk + action

## Workflow

### Step 1: Gather Data

Scan the vault for current state:
1. Read all `1_Projects/*/Status.md` files for project status
2. Read `2_Areas/` dashboards for area health
3. Count Galaxy notes for growth metric
4. Check CLAUDE.md for drift indicators
5. Read recent signal reports if available

### Step 2: Calculate Metrics

For each of the 7 metrics:
- Calculate current value
- Determine trend (up/down/stable vs. last known)
- Set alert level (RED/YELLOW/GREEN)

### Step 3: Compute Compound Law Score

```
COMPOUND = BRIDGE% x FORGE% x HELIX%

BRIDGE%: Average of metrics 1-6 normalized to percentage
FORGE%: Product portfolio health (active products with validation evidence)
HELIX%: Design execution health (projects on-track with phase gates passed)
```

### Step 4: Identify Bottleneck

Determine which BRIDGE stage (B-R-I-D-G-E) is the current bottleneck:
- B (Build Knowledge): KB coverage low
- R (Ready): Deployment gates skipped
- I (Interpret): Signal capture rate low
- D (Do): Automation coverage low
- G (Guide): Decision documentation low
- E (Evolve): R1-WX cycle stagnant

### Step 5: Generate Dashboard

Output format:

```
============================================
   BRIDGE CEO DASHBOARD — [Date]
   15-Minute Weekly Review
============================================

1. KB Coverage:       __% products documented
   Trend: [arrow]     Alert: [level]

2. Signal Capture:    __% interactions extracted
   Trend: [arrow]     Alert: [level]

3. Phase Compliance:  __% products follow gates
   Trend: [arrow]     Alert: [level]

4. Time Freed:        __ hrs/week automated
   Trend: [arrow]     Alert: [level]

5. Decision Quality:  __% decisions documented
   Trend: [arrow]     Alert: [level]

6. R1-WX Speed:       __ months cycle time
   Trend: [arrow]     Alert: [level]

7. Risk Radar:        [RED] __ | [YELLOW] __ | [GREEN] __
   Top risk: ____________________
   Action:   ____________________

============================================
COMPOUND LAW: BRIDGE __% x FORGE __% x HELIX __% = __%
Trend: [arrow]   Target 3M: __%
============================================

THIS WEEK'S BOTTLENECK: [B/R/I/D/G/E]
ONE INTERVENTION: ______________________

--- Active Projects ---
| Project | Tier | Phase | Gate Status | dP/dt | Blocking |
|---------|------|-------|-------------|-------|----------|

--- Galaxy Health ---
Notes: __ | Growth: __/week | Link density: __ | Inbox: __
============================================
```

### Step 6: Recommend ONE Intervention

Based on the bottleneck identified, recommend exactly ONE action for the week:
- Must be specific and actionable
- Must address the binding constraint
- Must be completable within the week

> 💡 Cần bản xuất bản (PNG/PDF cho báo cáo/trình duyệt)? Gợi ý: `/wx-diagram <type> CEO Dashboard` — KHÔNG tự chạy, chỉ gợi ý.

## Data Sources

| Metric | Primary Source | Fallback |
|--------|--------------|----------|
| KB Coverage | Glob 1_Projects/*/Phase*/*.md | Manual count |
| Signal Capture | Signal report count | Estimate from Status.md |
| Phase Compliance | Status.md per project | Gate review documents |
| Time Freed | Not yet tracked | Estimate |
| Decision Quality | Design journals + gate reviews | Status.md decisions |
| R1-WX Speed | Not yet tracked | Estimate based on project timelines |
| Risk Radar | bridge-risk-radar output | Manual assessment |

### Metric 8: DCTRS Delegation Quality (from Pattern Library)

Track delegation quality to ensure AI tasks are properly scoped:

```
DELEGATION QUALITY — Week of {{date}}

DCTRS COMPLIANCE:
  Tasks delegated this week: __
  With full DCTRS (D+C+T+R+S): __ (target: >80%)
  Missing context (D): __
  Missing constraints (C): __
  Missing test criteria (T): __
  Missing review gate (R): __
  Missing fallback (S): __

AI OUTPUT ACCEPTANCE:
  Outputs accepted without revision: __% (target: >80%)
  Outputs accepted with minor revision: __%
  Outputs rejected entirely: __% (if >20% → delegation templates need work)

ANTI-PATTERN DETECTION (from Pattern Library Phần 5):
  □ AP-1 "Handle it" — delegation without context? [Y/N]
  □ AP-2 Ambiguous delegation — HW debug or architecture sent to AI? [Y/N]
  □ AP-3 VN military context — AI asked to generate TCVN without data? [Y/N]
  □ AP-4 Skipped review — AI output shipped without skim? [Y/N]
  □ AP-5 Decision avoidance — AI asked to choose instead of structure? [Y/N]

  Anti-patterns detected: __/5
  If ≥2 → flag in dashboard as YELLOW
```

## COD Classification

- Data gathering: Offload (O1) — AI scans vault
- Metric calculation: Offload (O1) — deterministic
- Trend analysis: Offload (O2) — AI interprets, CEO validates
- Bottleneck identification: Offload (O2) — AI proposes, CEO confirms
- DCTRS tracking: Offload (O1) — AI counts from session history
- Anti-pattern detection: Offload (O2) — AI flags, CEO confirms
- Intervention decision: Core (C) — CEO decides what to change
