---
name: forge-scout
description: Systematic ACH opportunity discovery across the product portfolio. This skill should be used when the user asks to "find ACH opportunities", "scout ACH", "scan portfolio for AI", "which product should use AI?", "ACH potential", "tim co hoi ACH", or "san pham nao dung AI thay hardware?". Stage 0 of the FORGE lifecycle.
---

# Forge Scout — ACH Opportunity Discovery

Systematically scan the product portfolio to identify sub-functions where AI can replace expensive or imported hardware (ACH principle). Output: ACH Opportunity Matrix, cross-product Synergy Graph, and CEO-prioritized shortlist for forge-shift assessment.

## When to Use

- Quarterly strategic review (systematic portfolio scan)
- When a new product enters the portfolio
- When new AI capability becomes available (model or hardware)
- When supply chain disruption makes hardware ACH more attractive

## Workflow

### Step 0: Import Customer Outcome Data (if available)

Check for forge-job-map outputs:
- Glob `1_Projects/*/Phase0-Init/Opportunity_Landscape.md`
- If found: import underserved outcomes (top 15) and overserved outcomes (bottom 15)

```
OUTCOME-FIRST FILTER — {{product}}

UNDERSERVED outcomes (from forge-job-map):
| Rank | Outcome | Opp Score | ACH addressable? |
|------|---------|-----------|:-----------------:|
| 1 | {{outcome}} | {{score}} | YES/NO/MAYBE |

OVERSERVED outcomes → ACH cost reduction candidates:
| Rank | Outcome | Opp Score | Current cost driver |
|------|---------|-----------|-------------------|
| 1 | {{outcome}} | {{score}} | {{expensive hardware}} |

If no forge-job-map data exists:
→ Flag: "⚠️ No customer outcome data. Scout is technology-push only. Run /forge-job-map first for demand-side input."
→ Proceed with Step 1 (technology scan) but note limitation.
```

### Step 1: Portfolio Scan

Read all project data:
- Glob `1_Projects/*/Status.md` and `_Project_Brief.md`
- Function structures if available (from HELIX 6-flow)
- Morphological matrices if available (from Phase 2)
- forge-library → existing models that could be reused
- **forge-job-map outputs** (if available from Step 0)

For each product, list all sub-functions and classify ACH potential:

```
ACH OPPORTUNITY MATRIX — Workshop X Portfolio
Date: {{today}}

| Product | Sub-function | Current Solution | ACH Potential | Rationale |
|---------|-------------|-----------------|:-------------:|-----------|
| {{name}} | {{SF}} | {{hardware}} | HIGH/MED/LOW | |

Classification guide:
- HIGH: Sensor-based or computation-based function, commodity data available
- MEDIUM: Safety-critical but AI feasible with fallback
- LOW: Mechanical-only function, no information advantage from AI
```

### Step 2: Cross-Product Synergy Map

Identify sub-functions that are similar across products:

```
SYNERGY GRAPH

{{product A}} / {{SF-1}}  ≈  {{product B}} / {{SF-3}}
  → Same model type could serve both
  → Reuse Multiplier: 1 model → {{N}} products

Cross-product model opportunities:
| Model Type | Products Served | Reuse Multiplier |
|-----------|----------------|:----------------:|
| Detection (visual) | | |
| Classification | | |
| Tracking | | |
| Prediction | | |
```

### Step 2b: Competitive Reverse-Engineering (from DMIR×ODI Framework)

For each HIGH-potential product, identify and analyze key competitors/benchmarks:

```
COMPETITIVE REVERSE-ENGINEERING — {{product}}

For each competitor/benchmark product:
1. Create REF_{{competitor}}_ReverseEng.md in project References/
2. Extract structured data:

| Dimension | Competitor Data | WX Comparison |
|-----------|----------------|---------------|
| Architecture | [hull type, propulsion, control] | [same/different] |
| Key specs | [size, weight, speed, endurance] | [better/worse/same] |
| Pricing | [unit price if public] | [target vs actual] |
| Supply chain | [imported/local, lead time] | [advantage/risk] |
| Strengths | [what they do well] | [learn from] |
| Weaknesses | [where they fail] | [WX opportunity] |
| ACH potential | [uses AI? how?] | [WX can do better?] |

3. Map competitor functions → WX function structure (when Phase 1 available)
4. Flag: "What competitor does well that WX should LEARN"
5. Flag: "What WX can do BETTER (ACH advantage, local content, cost)"

RULE: ≥2 competitors/benchmarks per product before Phase 1
      If 0 competitors found → "greenfield market" — higher risk, higher reward
```

Output feeds:
- `helix-task-clarify` → requirements benchmarking (competitor specs as W-requirements)
- `helix-concept-generate` → concept alternatives inspired by competitor architectures
- `forge-shift` → ACH comparison vs competitor hardware approach

### Step 3: Preliminary SHIFT Quick-Pass

For each HIGH-potential opportunity, run a 30-second SHIFT pre-screen:

| Opportunity | S? | H? | I? | F? | T? | Quick Verdict |
|-------------|----|----|----|----|----|----|
| | Y/N/? | Y/N/? | Y/N/? | Y/N/? | Y/N/? | Proceed to forge-shift / Skip |

### Step 4: CEO Strategic Filter (Core)

Present ACH Opportunity Matrix + Synergy Graph to CEO.

CEO filters by factors AI cannot assess:
- Customer urgency and willingness to pay
- Funding availability and timing
- Team capacity (solo engineer, 25h/week)
- Political context and relationship dynamics
- "Opportunity X looks good on paper but customer isn't ready"
- "Opportunity Y is small but unlocks 3 downstream products"

Output: **Top 3-5 opportunities** → push to forge-shift for full assessment.

## HELIX Integration

```
forge-scout READS FROM HELIX:
  - 6-flow function structures → sub-functions to evaluate
  - Task clarification → requirements related to AI capability
  - Project charters → what products are in scope

forge-scout WRITES TO HELIX:
  - "ACH opportunity identified for SF-X" → tag in task clarification
  - "Reuse potential: model from Product A → Product B" → cross-project note
```

## Rules

- Scan ALL products, not just the ones CEO is thinking about (avoid confirmation bias)
- HIGH potential does not mean GO — that's forge-shift's job
- Cross-product synergies are where compound value lives — always map them
- Existing forge-library models are "easy ACH" — check library first
- Capacity constraint is REAL — recommend 2-3 opportunities, not 10

## COD Classification

- Portfolio scan: Offload (O1) — AI reads vault data
- Synergy mapping: Offload (O2) — AI identifies similarities
- SHIFT quick-pass: Offload (O2) — AI pre-screens
- Strategic prioritization: **Core (C)** — CEO selects based on judgment
