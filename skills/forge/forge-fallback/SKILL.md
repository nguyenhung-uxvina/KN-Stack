---
name: forge-fallback
description: Design fallback architecture for ACH products with defense-grade degradation levels. This skill should be used when the user asks to "design fallback", "fallback architecture", "what if AI fails?", "degradation mode", "backup plan for AI", "fallback level", or "AI fail thi sao?". Required for every ACH GO decision.
---

# Forge Fallback — ACH Fallback Architecture Design

Design a defense-grade fallback architecture for products using ACH (AI-Compensates-Hardware). Every ACH product MUST have a fallback before deployment. Output: fallback specification with trigger conditions, degradation behavior, recovery path, and test plan.

## When to Use

- After forge-shift returns GO or CONDITIONAL GO
- When forge-portfolio flags Fallback Level 0 (RED alert)
- Before HELIX Phase 2 Conceptual Design (fallback shapes the concept)
- When revisiting fallback after ICD changes

## Fallback Levels (Defense Standard)

| Level | Name | Description | Defense Acceptability |
|-------|------|-------------|---------------------|
| 0 | None | No fallback exists | UNACCEPTABLE — halt deployment |
| 1 | Manual Override | Operator bypasses AI, controls manually | Acceptable for non-critical |
| 2 | Graceful Degradation | AI fails → system degrades to simpler mode | Good for most applications |
| 3 | Redundant Path | Dual system: AI primary + traditional secondary | Required for safety-critical |

## Workflow

### Step 1: Gather Context

Read:
- forge-shift assessment → approved ACH sub-function + required fallback level
- `1_Projects/{{project}}/Status.md` — current phase
- Risk register (Phase 2/3) if available
- Concept evaluation — runner-up concepts are natural fallback candidates

### Step 2: Generate Fallback Architecture Options

For each applicable level, specify:

```
FALLBACK ARCHITECTURE — {{product}} / {{sub-function}}
Date: {{today}}

## PRIMARY APPROACH (Plan A)
| Aspect | Description |
|--------|-------------|
| Design | {{ACH approach: AI + commodity sensor}} |
| TRL | {{current TRL}} |
| Key risk | {{what could go wrong}} |
| Failure consequence | Safety / Mission-critical / Financial / Schedule |

## FAILURE MODE ANALYSIS
| # | Failure Mode | Prob | Severity | Detection | Trigger |
|---|-------------|------|----------|-----------|---------|
| FM-1 | Model accuracy drops below threshold | | | | |
| FM-2 | Sensor hardware failure | | | | |
| FM-3 | Inference latency exceeds limit | | | | |
| FM-4 | Environmental conditions outside training envelope | | | | |

## FALLBACK OPTIONS

### Level 1: Manual Override
- What: Operator bypasses AI, controls manually
- Switch mechanism: {{physical switch / software toggle}}
- Operator training required: {{hours}}
- Performance in manual mode: {{% of full capability}}
- Cost to implement: {{additional cost}}

### Level 2: Graceful Degradation
- What: AI fails → system falls back to simpler algorithm
- Example: AI object detection → motion detection fallback
- Degradation logic: {{threshold definitions}}
- Performance in degraded mode: {{what you lose}}
- Cost to implement: {{additional cost}}

### Level 3: Redundant Path
- What: Dual system — AI primary + traditional secondary
- Secondary system: {{specific hardware/approach}}
- Voting logic: {{how system decides which path to trust}}
- Switchover criteria: {{measurable conditions}}
- Cost to implement: {{significant — dual system}}

## FALLBACK DECISION MATRIX
| Criterion | Wt | L1 Manual | L2 Degrade | L3 Redundant |
|-----------|---:|-----------|-----------|-------------|
| Implementation speed | 25% | | | |
| Cost | 20% | | | |
| Performance retained | 25% | | | |
| Risk of fallback failing | 15% | | | |
| Local content impact | 15% | | | |

RECOMMENDED: Level __ — {{rationale}}

## ACTIVATION PROTOCOL
1. Trigger: {{specific measurable condition}}
2. Decision maker: CEO (Core)
3. Switch time: {{seconds/minutes to activate}}
4. Recovery path: {{how to return to AI mode after fix}}
5. Test plan: {{how to verify fallback works}}

## INTEGRATION REQUIREMENTS → HELIX ICD
- New interface: IF-AI-FALLBACK between {{subsystems}}
- Weight/cost/complexity impact on embodiment
- Test requirements for Gate 3 checklist
```

### Step 3: CEO Decision (Core)

Present options. CEO selects:
- Fallback level
- Specific architecture
- Budget allocation for fallback implementation

### Step 4: Feed to HELIX

After CEO approval, fallback spec becomes:
- New requirements in task clarification
- ICD entry for integration (IF-AI-FALLBACK)
- Trust flow path in function structure
- Gate 3 checklist addition for testing
- Weight/cost impact on concept evaluation

## Critical Rule

```
FALLBACK CHANGES THE PRODUCT ARCHITECTURE.
If product is in HELIX Phase 2+:
  forge-fallback MUST trigger helix-sync-protocol
  "New fallback requirement → ICD change → all domains affected"
```

## Rules

- Fallback Level 0 = automatic RED alert in forge-portfolio
- Fallback triggers must be MEASURABLE — "if it doesn't work" is not a trigger
- Always include recovery path — how to return to AI mode
- Runner-up concepts from Phase 2 are natural fallback candidates
- Test plan for fallback is as important as the fallback itself
- Point of no return: identify date after which switching is too expensive

## COD Classification

- Fallback option generation: Offload (O2) — AI generates options
- Failure mode analysis: Offload (O2) — AI analyzes, CEO validates
- Fallback level selection: **Core (C)** — CEO decides
- Risk acceptance for defense deployment: **Core (C)** — CEO accountable
