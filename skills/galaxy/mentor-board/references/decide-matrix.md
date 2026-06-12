# DECIDE Matrix — Option Scoring Protocol

Per-mentor × per-option scoring → weighted decision matrix.

## When to Use DECIDE

CEO has CONCRETE options (A, B, C) and needs structured comparison.

NOT for:
- Exploration (use PANEL)
- Unresolved tension (use DEBATE)
- Single-option stress-test (use CONSULT)

## Inputs

- Problem statement
- Options: 2-5 (fewer = not real decision, more = decision fatigue)
- Mentors: explicit list or preset
- (Optional) Reliability weights per mentor per problem class (auto-applied if logged)

## Per-Mentor × Per-Option Query Template

For each (mentor, option) pair, parallel Task subagent runs:

```
Context: You are <FULL NAME>. Answer using ONLY your writings/talks from notebook.

CEO problem: <problem>
CEO is considering OPTION <X>: "<option text>"

Provide your assessment of THIS OPTION (not comparison with others):

═══════════════════════════════════════════════════════════════════════════════
ASSESSMENT — OPTION <X>
═══════════════════════════════════════════════════════════════════════════════

## Score (1-10)
<integer> — where:
  10 = strongly recommend (matches your framework perfectly)
  7-9 = recommend
  4-6 = neutral / depends on conditions
  1-3 = strongly reject (violates your framework)

## Rationale (1-2 sentences)
<why this score, citing your framework>

## Source citation
<book/talk supporting your assessment>

## Top risk you see in this option
<one specific risk>

## Reverse condition
<what would need to be true for you to reverse the score by 3+ points>

═══════════════════════════════════════════════════════════════════════════════
```

## Aggregation — Decision Matrix

After all (mentor × option) queries complete, compose:

```markdown
# DECISION MATRIX — <problem>
Date: <today>  Consult ID: <id>

## Options
- A: <text>
- B: <text>
- C: <text>

## Mentor Scores

| Mentor | Reliability weight | A | B | C | Top risk per option |
|--------|-------------------|:-:|:-:|:-:|---------------------|
| Musk   | 0.9 (capital class) | 8 (timing) | 4 (slow) | 2 (no growth) | A: execution / B: pace / C: opp cost |
| Munger | 1.0 (capital class) | 5 (over-paying) | 7 (steady) | 8 (margin of safety) | A: hidden risk |
| Marks  | 1.0 (capital class) | 4 (cycle blind) | 5 (timing) | 9 (cycle-aware) | A: top-of-cycle risk |

### Score sources
| Mentor | Option | Score | Reverse condition |
|--------|--------|:-----:|-------------------|
| Musk   | A | 8 | "If team < 5 engineers, drop to 4" |
| Munger | A | 5 | "If you can buy at 50% discount to fair value, raise to 8" |
| Marks  | A | 4 | "If macro turns risk-off, drop to 1" |
| ... (continue for all cells)

## Weighted Averages

Formula: weighted_avg(option) = Σ(score × reliability_weight) / Σ(reliability_weight)

| Option | Weighted avg | Raw avg | Variance |
|--------|:-----------:|:------:|:--------:|
| A | 5.7 | 5.7 | 4.0 (high — disagreement) |
| B | 5.3 | 5.3 | 2.3 (medium) |
| C | 6.3 | 6.3 | 13.0 (very high — strong split) |

**High variance = mentors disagree strongly. Worth understanding before deciding.**

## Strong Reject Flags (score ≤ 3)

- **Musk vetoes C (score 2):** "Bank reserves = giving up future growth" [Cite: Twitter 2023]
- **Marks gives A only 4:** "If we're top-of-cycle, optionality > deployment" [Memo: Sea Change 2022]

When ≥1 mentor strongly rejects, CEO must understand the rejection mechanism before proceeding.

## Consensus Identification

| Pattern | Detected? |
|---------|-----------|
| All ≥7 on any option | None (no strong consensus) |
| All ≤3 on any option | None (no strong reject) |
| Majority within ±2 on top option | No (high variance) |
| **All flag same risk** | YES — timing risk flagged by all 3 |

## Reverse Conditions Table

If CEO can VERIFY any reverse condition → re-score:

| Condition | Affects | New likely scores |
|-----------|---------|-------------------|
| "Team grows to 5+ engineers" | Musk on A | A: 8→4 (downgrade) |
| "Can buy at 50% discount" | Munger on A | A: 5→8 (upgrade) |
| "Macro turns risk-off" | Marks on A | A: 4→1 (downgrade) |

## DMIR Closure

**D (Diagnose):** Decision framed as 3 options.

**M (Model):** 3 scoring models surfaced (Musk growth-velocity, Munger margin-of-safety, Marks cycle-awareness).

**I (Intervene):** [CEO Core — final pick]

CEO must commit:
- (1) Pick highest weighted-avg → C (6.3)
- (2) Pick most-aligned with WX constraints → <CEO judgment>
- (3) Defer until reverse condition tested → <which condition>
- (4) Reframe options → restart DECIDE

CEO selection: <to be filled>

**R (Reflect):** [Empty — fill via /mentor-board --retro <consult-id> after outcome]
```

## Reliability Weighting (Per Problem Class)

Each mentor's `reliability_log.md` tracks:
- Per problem class (capital, scaling, manufacturing, etc.)
- Hits / Misses / Partials
- Reliability % = hits / total

Weight formula:
```
reliability_weight = 0.5 + (reliability_pct × 0.5)
  → Range: 0.5 (0% reliability) to 1.0 (100% reliability)
  → Minimum 0.5 to avoid zero-weighting based on small N

Confidence threshold:
  - N ≥ 5 retros for class → apply weight
  - N < 5 → use weight = 1.0 + flag "low confidence (n=<N>)"
```

## Cold-Start Handling

When reliability_log empty (no retros yet):
- All weights = 1.0
- Output table includes "⚠️ Cold start — reliability weights not yet calibrated. Decision based on raw scores."
- Encourage CEO to run `--retro` after outcomes to build calibration data.

## Validation Rules

- Options ≥ 2 and ≤ 5 — refuse otherwise
- Mentors ≥ 1 (single-mentor DECIDE possible, just gives 1 column)
- Problem statement length ≥ 30 chars (too short = poorly framed)
- If all mentors give same score for all options → re-prompt: "Force differentiation. Each mentor should have at least 2-point spread across options if their framework discriminates."
