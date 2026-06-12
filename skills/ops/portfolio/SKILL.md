---
name: portfolio
description: >-
  Generate the Workshop X Product Portfolio dashboard — compiles all active
  projects from Status.md files into a prioritized matrix with Tier health
  checks, dependency map, and resource allocation view. Use when reviewing
  portfolio priorities, checking for missing Tier 1 projects, or resolving
  sequencing conflicts. Triggers on: "portfolio", "danh mục sản phẩm", "project
  matrix", "tier health", "portfolio review", "xem portfolio".
---

Generate the Workshop X Product Portfolio dashboard with prioritization.

Usage: /portfolio OR /portfolio [filter]

1. Read all project Status.md files:
   - Glob `1_Projects/*/Status.md` in the current vault
   - Also check for `_Project_Brief.md` in each project folder
2. Read archived projects for historical context:
   - Glob `4_Archives/Projects/*/` to count archived projects
3. Compile portfolio view:

```
# PRODUCT PORTFOLIO — Workshop X
**Date:** {{today}}

---

## PORTFOLIO MATRIX

| # | Product | Code | Tier | Phase | Gate Score | Physical Gate | ACH? | Local% | Est. Cost | Revenue Model |
|---|---------|------|------|-------|------------|---------------|------|--------|-----------|---------------|
| 1 | | | T1/T2/T3 | 0-4 | /4.0 | date or N/A | Y/N | % | $ | |

---

## DEPENDENCY MAP

```
{{Draw ASCII dependency graph showing which products depend on others}}
{{e.g., I-01 Standard → I-02 CTR (DG-1: I-01 Phase 3)}}
```

---

## TIER HEALTH CHECK

### Tier 1 (Prototype) — Must have ≥1 project with physical gate ≤30d
- [ ] At least 1 active Tier 1 project? {{YES/NO}}
- [ ] Physical gate within 30 days? {{YES/NO}}
- **Action needed:** {{if no, recommend promoting a project or defining a gate}}

### Tier 2 (Product Dev) — Pahl-Beitz tracked
- Projects in Phase 3+: {{count}}
- Projects blocked: {{count + reasons}}

### Tier 3 (Strategic) — Time-bounded knowledge deliverables
- Projects with clear "done" criteria: {{count}}/{{total}}

---

## RESOURCE ALLOCATION (Solo CEO)
| Domain | This Week Hours | % of 25h | Target |
|--------|-----------------|----------|--------|
| Tier 1 Physical | | | ≥40% |
| Tier 2 Design | | | ≤30% |
| Tier 3 Strategic | | | ≤15% |
| Operations | | | ≤15% |

---

## PORTFOLIO DECISIONS NEEDED
1. {{Any project needing tier change?}}
2. {{Any project needing archival?}}
3. {{Any project missing Status.md?}}
4. {{Sequencing conflicts?}}
```

4. If $ARGUMENTS contains a filter (e.g., "tier1", "blocked", "ACH"), show only matching projects with expanded detail.
5. Present portfolio to user. Do NOT save to file unless asked.

RULES:
- Use data from Status.md and _Project_Brief.md, not assumptions
- Flag any project missing Status.md — it needs one
- Flag any Tier 2 project without Pahl-Beitz phase tracking
- Flag portfolios with 0 Tier 1 projects — violates CLAUDE.md rule
- Always show dependency map — sequencing errors are expensive
- COD: This is an Offload task (AI compiles, CEO decides)
