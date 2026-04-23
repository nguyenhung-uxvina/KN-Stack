---
name: bridge-judgment
description: Structure complex decisions with options, evidence, risks, and unknowns to support CEO judgment quality. This skill should be used when the user faces a trade-off, needs to choose between alternatives, or asks for a recommendation. NEVER recommends — only structures. Triggers on decision, trade-off, quyet dinh, nen chon gi, guide, recommendation.
---

# Bridge Judgment — Decision Support (Never Decision Replacement)

Structure decisions with options, evidence, risks, and unknowns. Present the decision package to the CEO. NEVER say "You should do X." ALWAYS say "Here are options, evidence, risks, unknowns. You decide."

## When to Use

- When facing a technical trade-off (material A vs B)
- When making a strategic choice (invest in product X vs Y)
- When allocating resources (hire vs buy)
- When assessing risk (deploy now vs wait)
- When bridge-dashboard metric #5 (Decision Quality) needs improvement

## Critical Principle

AI improves INFORMATION QUALITY feeding into human judgment. AI does NOT replace human judgment.

The moment CEO delegates judgment to AI:
- Judgment stock atrophies
- Shifting the Burden archetype activates
- System degrades

This skill exists to STRENGTHEN judgment, not substitute for it.

## Workflow

### Step 1: Structure the Decision

Identify decision type:

| Type | Example | Key Data Sources |
|------|---------|-----------------|
| Technical | "Material A or B?" | DfX data, cost, field experience |
| Strategic | "Invest in V-SMASH or LOMAH?" | Portfolio, capacity, customer demand |
| Resource | "Hire AI engineer or buy tool?" | Talent map, budget, timeline |
| Risk | "Deploy Phase 2 now or wait?" | Evidence level, trust, consequences |

### Step 2: Gather Context

Pull relevant information from:
- bridge-knowledge-base: similar decisions made before, their outcomes
- FORGE portfolio: strategic alignment
- HELIX project data: technical constraints
- External: market, competitor, regulation (if available)

### Step 3: Present Decision Package

```
## Decision Package — [Title]
**Date:** YYYY-MM-DD
**Type:** Technical / Strategic / Resource / Risk
**Reversibility:** High / Medium / Low

### Options
| Option | Description | Evidence For | Evidence Against |
|--------|------------|-------------|-----------------|
| A | ... | ... | ... |
| B | ... | ... | ... |
| C | ... | ... | ... |

### Criteria
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|

### What We Don't Know
- [uncertainty 1]
- [uncertainty 2]

### Risk Assessment
| Option | Risk | Likelihood | Impact | Mitigation |
|--------|------|-----------|--------|------------|

### Reversibility
Can we undo this if wrong? How costly is reversal?
```

### Step 4: CEO Decides

CEO reviews package, factors in experience, intuition, relationships, and context that AI cannot capture. Records:
- Chosen option
- Rationale
- What tipped the decision

### Step 5: Document and Track

- Log decision with rationale to KB Layer 3
- Route to helix-design-journal if project-specific
- Set review trigger: "revisit this decision in N months"

### Step 6: Monitor Decision Quality Over Time

- Tag outcomes: "decision X from N months ago, outcome was Y"
- Detect patterns: "CEO consistently overestimates timeline by 30%"
- Feedback loop: "decisions with more data had 2x better outcomes"

## Integration Points

- Reads from: bridge-knowledge-base (prior decisions), FORGE portfolio (strategic context), HELIX project data (technical constraints)
- Writes to: KB Layer 3 (decision log), helix-design-journal (project decisions), bridge-dashboard (decision quality metric #5)

## Metrics

- Decision documentation rate: % decisions with rationale logged (target: >80%)
- Decision review rate: % decisions revisited at scheduled time (target: >50%)
- Outcome tracking: % decisions with outcome tagged (target: >30%)

## COD Classification

- Decision structuring: Offload (O2) — AI structures, CEO reviews framing
- Context gathering: Offload (O1) — AI pulls from KB, FORGE, HELIX
- The decision itself: Core (C) — CEO decides, always
- Documentation: Offload (O1) — AI logs after CEO decides
- Pattern analysis: Offload (O2) — AI detects patterns, CEO interprets
