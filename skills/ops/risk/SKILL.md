---
name: risk
description: >-
  Generate the Workshop X Risk Radar — early warning system that scans all
  project Status.md files and area dashboards for critical risks, Shifting the
  Burden patterns, physical validation gaps, and supply chain exposures. Use
  weekly or when dP/dt = 0 is flagged. Triggers on: "risk", "risk radar", "rủi
  ro", "early warning", "radar rủi ro", "supply chain risk", "physical gap".
---

Generate the Workshop X Risk Radar — early warning system for organizational and project risks.

Usage: /risk OR /risk [project_name]

1. Read all project Status.md files:
   - Glob `1_Projects/*/Status.md`
   - Extract: blocking constraints, flags, deadlines, dP/dt
2. Read Area dashboards if available:
   - Glob `2_Areas/*/_Area_Dashboard.md`
3. Check CLAUDE.md for survival metrics

4. Compile the Risk Radar:

```
# RISK RADAR — Workshop X
**Date:** {{today}}  |  **Horizon:** 30-day / 90-day

---

## CRITICAL RISKS (action within 7 days)

| # | Risk | Project/Area | Impact | Probability | Trigger Date | Action Required |
|---|------|-------------|--------|-------------|--------------|-----------------|

---

## WARNING RISKS (action within 30 days)

| # | Risk | Project/Area | Impact | Probability | Trigger Date | Action Required |
|---|------|-------------|--------|-------------|--------------|-----------------|

---

## WATCH LIST (monitor, no action yet)

| # | Risk | Project/Area | Next Check |
|---|------|-------------|------------|

---

## SYSTEMIC RISK PATTERNS

### Shifting the Burden Check
- Is any problem being "solved" by AI/delegation that should be solved by CEO judgment?
- Evidence: {{specific examples or "none detected"}}

### Complexity Ceiling Check
- Total active projects: {{count}}
- Solo CEO capacity: 25h/week
- Hours/project/week (estimated): {{25 / count}}
- WARNING threshold: < 4h/project/week → spreading too thin

### Physical Validation Gap
- Projects with dP/dt = 0: {{count}}/{{total}}
- Months since last physical prototype: {{estimate}}
- R3 (AI Dependency Spiral) risk level: {{LOW/MED/HIGH}}

### Supply Chain Risks
- Long-lead items ordered: {{list or "none pending"}}
- Single-source dependencies: {{list or "none identified"}}

---

## RISK TREND (vs last check)
| Category | Last | Now | Trend |
|----------|------|-----|-------|
| Critical risks | ? | {{n}} | ↑↓→ |
| Warning risks | ? | {{n}} | ↑↓→ |
| dP/dt across portfolio | ? | {{n}} | ↑↓→ |
```

5. If $ARGUMENTS contains a project name, expand that project's risks with full detail.
6. Present to user. Do NOT save unless asked.

RULES:
- Risk Radar is READ-ONLY — reports, never modifies
- Always check for Shifting the Burden archetype (Galaxy note)
- Flag dP/dt = 0 as CRITICAL if it persists > 2 weeks
- Supply chain lead times are risks — flag items not yet ordered
- COD: Offload (AI scans, CEO validates and acts)
- Cross-reference with Galaxy: Physical-World Interface, AI Dependency Spiral
