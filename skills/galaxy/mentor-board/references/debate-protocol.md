# DEBATE Protocol — 3-Round Argument

3-round argument across multiple mentors. Each round = N parallel Task subagents (one per mentor).

## Round 1 — Position (~10 min)

Each mentor receives same problem + intake_context. Runs standard 5-frame DMIR consult (see `dmir-template.md`).

Output to `<run_dir>/round1_<leader>.md`.

**Key:** mentors do NOT see each other in Round 1. Pure independent position.

## Round 2 — Rebuttal (~10 min)

Each mentor now receives:
- Their own Round 1 output
- ALL OTHER mentors' Round 1 outputs (markdown text)
- Same problem + intake_context

Query template:

```
Context: You previously took position <Round 1 summary>.

Other mentors took these positions:
─────────────────────────────────────
<Leader B>'s position (Round 1):
<Round 1 output of Leader B>

<Leader C>'s position (Round 1):
<Round 1 output of Leader C>
─────────────────────────────────────

Now: which of the OTHER mentors' views do you MOST STRONGLY DISAGREE with?
Pick ONE (cannot punt or compromise).

Provide your rebuttal in this structure:

═══════════════════════════════════════════════════════════════════════════════
ROUND 2 REBUTTAL
═══════════════════════════════════════════════════════════════════════════════

## Target: <Leader X>'s position on <specific claim>

## Their claim (paraphrased)
<what Leader X argued in Round 1>

## My rebuttal
<your counter-argument, drawing on YOUR notebook>

## Source citation (mandatory)
<book/talk citation supporting your rebuttal>

## What Leader X is missing
<the gap in their framework that your framework catches>

## What would they need to concede
<the specific point Leader X would have to give up for your rebuttal to land>

═══════════════════════════════════════════════════════════════════════════════
```

**Refuse-to-generate guards:**
- If output is "I broadly agree with all" → re-prompt: "Force pick ONE to rebut. Even small disagreement counts."
- If rebuttal has no source citation → re-prompt: "Cite from YOUR notebook."
- If rebuttal is generic ("they're too short-term") → re-prompt: "Specific claim + specific counter."

Output to `<run_dir>/round2_<leader>.md`.

## Round 3 — Convergence (~10 min)

Each mentor receives:
- Their own Round 1 + Round 2
- ALL OTHER mentors' Round 2 rebuttals
- Same problem

Query template:

```
After reading rebuttals from other mentors, do you UPDATE your position?

Provide your final position in this structure:

═══════════════════════════════════════════════════════════════════════════════
ROUND 3 CONVERGENCE
═══════════════════════════════════════════════════════════════════════════════

## What I CHANGE from my Round 1 position
<list — be specific, or write "Nothing — see firm reasons below">

## Why I changed (citing the rebuttal)
<which rebuttal moved you, and why>

## What I HOLD FIRM on
<list — positions you refuse to update>

## Why I hold firm
<explain — what would actually move you that wasn't presented>

## Updated 3-action recommendation (Frame 5 revised)
- Week-1: <revised action> — success: <metric>
- Week 2-4: <revised action> — success: <metric>
- Quarter: <revised action> — success: <metric>

═══════════════════════════════════════════════════════════════════════════════
```

**Quality bar:** if mentor refuses to engage with rebuttals ("I stand by everything"), re-prompt asking them to address at least 1 specific rebuttal point.

Output to `<run_dir>/round3_<leader>.md`.

## Synthesis (CEO Core, ~5-10 min)

AI reads all 3N round files and composes:

```markdown
# DEBATE — <problem>
Date: <today>  Mentors: <list>  Consult ID: <id>

## intake_context
<from INTAKE if used, else direct context>

## Round-by-Round Trajectory

### <Leader A>
- Round 1: <position summary>
- Round 2: rebutted <Leader X> on <topic>
- Round 3: changed <X>, held firm on <Y>

### <Leader B>
- (same structure)

### <Leader C>
- (same structure)

## Productive Tensions Identified

### Tension 1: <topic, e.g., "Growth velocity vs capital preservation">
- <Leader A>'s position: <view> [from Round 1, evolved/firm in Round 3]
- <Leader B>'s position: <contrary view> [from Round 1, evolved/firm]
- **Underlying disagreement (root cause):**
  <e.g., "Different risk tolerance — A operates with conviction-bet model, B operates with margin-of-safety model.">
- **What rebuttal was strongest:**
  <which side made the move-the-needle argument>
- **What's unresolved:**
  <the assumption neither side could disprove>

### Tension 2: <next topic>
(same structure)

## What All Agreed On
| Consensus point | Cited by | Combined source pool |
|----------------|----------|---------------------|
| <point> | <all 3 leaders> | <sources> |

## What CEO Must Decide (the unresolved core)
**This is the value of DEBATE — surface what mentors can't resolve, so CEO can.**

| Decision point | Pro-A side | Pro-B side | What CEO's choice depends on |
|---------------|------------|------------|------------------------------|
| <unresolved Q> | <case> | <case> | <CEO's risk tolerance / time horizon / WX constraint> |

## DMIR Closure

**D (Diagnose):** Refined problem (post-debate): <updated framing>

**M (Model):** Competing models surfaced:
- <Model 1 from Leader A>
- <Model 2 from Leader B>
- <Model 3 from Leader C if different>

**I (Intervene):** Fork-specific actions:
- If CEO commits to <Model 1>: actions = <list>
- If CEO commits to <Model 2>: actions = <list>
- If CEO commits to hybrid: actions = <list>

**R (Reflect):** [Empty — fill via /mentor-board --retro <consult-id>]
```

## Notes for Implementation

- **NLM session expiry:** 3 rounds × N mentors = 3N total queries. If session ~20min and full debate ~30min, may hit expiry. Mitigation: refresh auth between rounds 1-2 and 2-3.
- **Round file naming:** `round{N}_<leader>.md` for traceability. Keep in `<run_dir>/` after synthesis.
- **Parallel safety:** each round agents are independent — no shared state. Round outputs read by next round agents.
- **Source contamination prevention:** agents NEVER receive other mentors' notebook URLs. Only their Round N outputs (markdown text).

## Common Failure Modes

1. **All agree (no debate)** — re-prompt Round 2 with "Even small disagreements count. Pick the position most distant from yours."
2. **Personal attacks instead of position attacks** — re-prompt: "Engage the ARGUMENT, not the person. Cite their claim, counter the claim."
3. **Round 3 = Round 1 verbatim** (no update) — Add explicit prompt: "List ≥1 thing you CHANGED, even if minor."
4. **Synthesis is just summary** — re-prompt: "Identify ROOT CAUSE of disagreement (risk tolerance? time horizon? capital intensity?). Why couldn't either side disprove the other?"
