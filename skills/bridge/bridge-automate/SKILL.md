---
name: bridge-automate
description: Identify and implement process automation to free human capacity for judgment work. This skill should be used when the user wants to automate repetitive tasks, find automation candidates, track freed time, or reduce manual work. Triggers on automate, tu dong hoa, repetitive, template, giai phong thoi gian.
---

# Bridge Automate — Process Automation for Freed Judgment Time

Identify deterministic processes, automate them, and track where freed time goes. Rule: automate PROCESS, never automate JUDGMENT.

## When to Use

- When looking for automation opportunities
- When a repetitive process is consuming too much time
- When tracking freed hours and their allocation
- When reviewing automation coverage across workflows
- When bridge-dashboard metric #4 (Time Freed) needs updating

## Workflow

### Step 1: Identify Automation Candidates

Scan current processes for deterministic tasks (same input produces same output):

| Candidate | Frequency | Time/Instance | Error Risk | Score |
|-----------|-----------|---------------|------------|-------|
| [process] | [/week] | [hours] | [H/M/L] | freq x time / effort |

Score = freed_hours_per_week / implementation_effort

Present top 5 candidates to CEO.

### Step 2: Select and Prioritize

CEO selects which candidates to automate:
- "This one first — frees most judgment time"
- "Skip that one — too fragile, context-dependent"

Rule: If the task requires interpretation, intuition, or contextual judgment, it is NOT an automation candidate.

### Step 3: Implement Automation

Connect to existing automation tools:
- quality-gate-reporter — automate quality reporting
- cad-documentation-generator — automate drawing docs, BOM, inspection
- cad-review-automation — automate DfX checks
- design-iteration-assistant — automate design improvement proposals

Create new automation as needed:
- Meeting report generator (from bridge-signal-extract output)
- Weekly status report compiler (from HELIX + FORGE metrics)
- Standards compliance checker (against KB Layer 1)
- Cost estimation tool (from forge-cost templates)

### Step 4: Validate and Monitor

- Review first 10 automated outputs against previous human outputs
- Set quality threshold: "if AI output below X, flag for human review"
- Track error rate over time

### Step 5: Track Freed Time Allocation

CEO mandate for freed time distribution:

| Allocation | Target % | Purpose |
|-----------|----------|---------|
| Judgment work | 40% | Design decisions, trade-offs, reviews |
| Integration work | 25% | Cross-domain coordination |
| Learning | 20% | Skill development, methodology practice |
| Innovation | 15% | New approaches, ACH opportunities |

If freed time goes to MORE paperwork, automation has failed. CEO tracks weekly: "Freed time went where this week?"

## Integration Points

- Connects to: FORGE cost templates, FORGE portfolio report, HELIX quality-gate, HELIX integration-debt, all documentation outputs
- Writes to: bridge-dashboard (freed hours metric #4), bridge-flywheel (automation coverage %)

### Step 5b: Delegation Anti-Pattern Audit (from Pattern Library Phần 5)

Monthly scan of recent sessions for delegation mistakes. Feeds improvement loop back into delegation templates.

```
DELEGATION ANTI-PATTERN AUDIT — {{month}}

SCAN: Review last 4 weeks of session history for patterns:

AP-1 "HANDLE IT" DELEGATION (no context, no constraints)
  Instances found: __
  Examples: [list specific cases]
  Fix: Add context block to delegation (Pattern Library DCTRS: D+C)

AP-2 DELEGATING AMBIGUOUS WORK (HW debug, architecture to AI)
  Instances found: __
  Examples: [list cases where AI gave generic answer]
  Fix: DO YOURSELF. Use AI only for sub-questions (Pattern Library flowchart)

AP-3 TRUSTING AI ON VN MILITARY CONTEXT
  Instances found: __
  Examples: [cases where AI hallucinated TCVN/doctrine]
  Fix: CEO provides data, AI fills template (Pattern Library B1 rule)

AP-4 SKIPPING REVIEW ON "SIMPLE" OUTPUT
  Instances found: __
  Examples: [cases where unreviewed output had error]
  Fix: EVERY output gets minimum 2-min scan (Pattern Library rule)

AP-5 USING AI TO AVOID DECISIONS
  Instances found: __
  Examples: [cases where AI was asked to choose, not structure]
  Fix: Use bridge-judgment to STRUCTURE, CEO DECIDES (Pattern Library E1)

TOTAL ANTI-PATTERNS: __/5 types active
TREND vs LAST MONTH: ↑ / ↓ / =

TOP 1 ACTION: [specific improvement for next month]
```

## Metrics

- Automation coverage: % deterministic processes automated (target: 70%)
- Freed hours per week: hours saved by automation
- Quality score: % automated outputs meeting threshold (target: >95%)
- Freed time allocation: % going to judgment vs paperwork (target: >40% judgment)
- Anti-pattern count: total instances/month (target: decreasing trend)

## COD Classification

- Candidate identification: Offload (O2) — AI identifies, CEO selects
- Implementation: Offload (O1) — AI builds automation
- Quality validation: Core (C) — human validates first 10 outputs
- Time allocation decision: Core (C) — CEO decides where freed time goes
