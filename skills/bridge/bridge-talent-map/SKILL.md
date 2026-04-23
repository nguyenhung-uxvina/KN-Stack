---
name: bridge-talent-map
description: Map knowledge distribution, key-person risks, and skill gaps across Workshop X. This skill should be used when the user asks about talent, key person risk, skill gaps, who knows what, or workforce planning. Triggers on talent, nhan su, key person, skill gap, ai biet cai gi, risk neu nguoi X nghi.
---

# Bridge Talent Map — Knowledge Risk and Talent Pipeline

Map who knows what, identify key-person risks, detect skill gaps, and plan mitigation. Makes the binding constraint (AI talent: 1-2 engineers) visible and actionable.

## When to Use

- Quarterly talent review
- When a team member departure is announced or anticipated
- When a skill gap blocks a project
- When planning hiring or cross-training
- When bridge-risk-radar flags key-person dependency

## Workflow

### Step 1: Map Current Talent

For each team member, document:

```
## Talent Map — [Name]

**Products involved:** [list]
**Unique knowledge:** [what only this person knows]
**KB capture status:** [% documented in bridge-knowledge-base]

**Risk Score:**
- RED (Catastrophic): Sole owner of critical knowledge, no documentation
- YELLOW (High): Primary owner, some KB capture done
- GREEN (Manageable): Knowledge distributed, KB documented
```

Build the map from:
- Project Status.md files (who works on what)
- bridge-knowledge-base coverage (what is documented)
- bridge-signal-extract patterns (who is mentioned as sole expert)

### Step 2: Identify Gaps

Scan across all products and capabilities:
- "No one knows EMC simulation — gap for all products"
- "Only 1 person understands LARS control system"
- "AI/ML capability capped at 1-2 engineers"

Classify each gap:
- **Critical:** Blocks active Tier 1/2 projects
- **Important:** Limits future capability
- **Nice-to-have:** Would improve efficiency

### Step 3: Prioritize Mitigation

Present mitigation options to CEO for decision:

| Timeframe | Action | Example |
|-----------|--------|---------|
| Immediate | KB capture sessions for RED risks | "Record 5 things team needs to know" |
| Medium-term | Cross-training plan | Person A teaches Person B |
| Long-term | Hiring plan for structural gaps | Grow AI team to 3-4 in 12 months |

### Step 4: Monitor Quarterly

- Update talent map with changes
- Re-assess risk scores
- Track KB capture progress
- Report hiring/training pipeline status

## Binding Constraint Visibility

```
All FORGE skills (validate, library, flywheel) capped by 1-2 AI engineers.
All HELIX AI-domain work capped.
Compound Law numerator limited.

CEO #1 talent action: Grow AI team to 3-4 within 12 months.
Everything else is secondary.
```

## Integration Points

- Feeds into: bridge-risk-radar (key-person risks), bridge-dashboard (capacity view)
- Receives from: bridge-knowledge-base (KB coverage per person), HELIX project data (who works on what)

## Metrics

- Key-person risk count: number of RED-rated individuals (target: 0)
- Knowledge distribution: % knowledge documented in KB (target: >80%)
- Skill gap count: identified gaps without mitigation plan (target: 0)
- KB capture rate: % planned capture sessions completed (target: 100%)

## COD Classification

- Talent mapping: Offload (O2) — AI maps from project data, human validates
- Risk scoring: Offload (O2) — AI scores, CEO validates
- Mitigation prioritization: Core (C) — CEO decides hiring/training
- KB capture execution: Core (C) — human-to-human knowledge transfer
