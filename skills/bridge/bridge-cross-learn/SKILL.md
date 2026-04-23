---
name: bridge-cross-learn
description: Facilitate monthly cross-product learning sessions to transfer lessons between projects. This skill should be used when the user wants to run a cross-product review, transfer lessons learned, or identify patterns across projects. Activates R5 (Tacit Knowledge Extraction). Triggers on cross-product, lessons learned, transfer, hoc tu du an khac, cross-learn.
---

# Bridge Cross-Learn — Cross-Product Learning Sessions

Run monthly 60-minute sessions to transfer lessons between active projects. This is R5 (Tacit Knowledge Extraction) — the single highest-leverage organizational practice Workshop X could implement.

## When to Use

- Monthly cross-product learning session (scheduled)
- When a breakthrough or failure in one project may apply to others
- When bridge-flywheel shows COMPOUND stage is stalled
- When recurring patterns appear across multiple projects

## Workflow

### Step 1: Prepare (AI, 30 minutes before session)

Collect data from all active projects:

1. Read each `1_Projects/*/Status.md` for recent progress and blockers
2. Scan design journals for top 3 lessons per project
3. Pattern match: "Lesson X in Product A similar to issue Y in Product B?"
4. Prepare cross-product insight brief
5. Identify: "Products B, C could benefit from Product A's solution"

Output:

```
## Cross-Learn Prep Brief — [Date]

### Per-Project Top Lessons
| Project | Lesson 1 | Lesson 2 | Lesson 3 |
|---------|----------|----------|----------|

### Cross-Product Patterns Detected
| Pattern | Products Affected | Potential Transfer |
|---------|-------------------|-------------------|

### Suggested Transfer Actions
| From | To | What | Expected Benefit |
|------|-----|------|-----------------|
```

### Step 2: Run Session (Human leads, AI records — 60 min)

**15 min — Project Presentations:**
Each project lead presents top lessons (3 min each)

**15 min — Cross-Pollination:**
CEO + AI facilitate connections:
- "Product A solved thermal issue — Product C has similar config?"
- "Manufacturing trick in MTB-20 applicable to BB-01?"
- "Validation approach from VN-XUONG transferable to VN-12.7MM?"

**15 min — Action Items:**
- Specific transfers: "Person X will apply Lesson Y to Product Z"
- Deadlines assigned
- Expected outcomes defined

**15 min — Meta-Review:**
- "What patterns keep recurring? Root cause?"
- "What should we formalize into KB Layer 1 (standard)?"
- "Are we actually acting on previous cross-learn insights?"

### Step 3: Post-Session (AI)

1. Generate session summary → route to KB Layer 3
2. Log all action items with owners and deadlines
3. Track transfer success (did the lesson improve the target product?)
4. Update pattern database
5. Feed transfer count to bridge-flywheel COMPOUND metric

## Integration Points

- Receives from: HELIX design journals, project Status.md files, bridge-signal-extract outputs
- Feeds into: bridge-knowledge-base (KB Layer 3), bridge-flywheel (compound metric), forge-library (cross-product transfers)

## Metrics

- Session completion rate: % planned monthly sessions held (target: 100%)
- Transfer count: lessons transferred across products per session (target: >=2)
- Transfer success rate: % transferred lessons that improved target product (target: >50%)
- Pattern formalization: lessons promoted to KB Layer 1 per quarter (target: >=1)

## COD Classification

- Preparation: Offload (O1) — AI collects and pattern-matches
- Session facilitation: Core (C) — human leads, AI supports
- Recording: Offload (O1) — AI records and structures
- Transfer decisions: Core (C) — CEO decides which lessons to transfer
- Meta-review insights: Core (C) — CEO identifies root patterns
