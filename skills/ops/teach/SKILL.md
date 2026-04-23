Compound CEO judgment over time by extracting, cataloging, and replaying decision patterns from past project decisions.

This is NOT a decision-maker — it's a decision TEACHER that helps the CEO see their own patterns, biases, and growth areas. It enforces dJ/dt > dD/dt (judgment grows faster than delegation).

Usage: /teach [mode] where mode = record | review | pattern | challenge

---

## MODE 1: RECORD (capture a decision just made)

If $ARGUMENTS = "record" or no arguments:

1. Ask:
   - What decision was made? (one sentence)
   - What project / context?
   - What alternatives were considered?
   - What information did you use?
   - What information was MISSING but you decided anyway?
   - What's your confidence level? (HIGH / MEDIUM / LOW)
   - When will you know if this was right? (validation trigger)

2. Generate the decision record:

```
# DECISION RECORD — DR-{{YYYY-MM-DD}}-{{seq}}
**Date:** {{today}} | **Project:** {{project}} | **Phase:** {{phase}}

## Decision
{{one sentence}}

## Context
{{what prompted this decision}}

## Alternatives Considered
| # | Option | Pros | Cons | Why Rejected |
|---|--------|------|------|-------------|
| A | {{chosen}} | | | **SELECTED** |
| B | | | | |
| C | | | | |

## Information Used
- {{list of data points, analyses, test results that informed the decision}}

## Information Gap
- {{what was unknown or uncertain at decision time}}
- {{assumptions made to bridge the gap}}

## Decision Type
- **COD:** C (Core — CEO judgment) / O (Offload — AI recommended)
- **Reversibility:** Easy / Hard / Irreversible
- **Time pressure:** High / Medium / Low
- **Analogous to:** {{link to similar past decision if exists}}

## Confidence & Validation
- **Confidence:** HIGH / MEDIUM / LOW
- **Validation trigger:** {{event that will prove/disprove this decision}}
- **Expected validation date:** {{when}}
- **Outcome:** {{fill in later: CORRECT / WRONG / PARTIALLY RIGHT / TBD}}
```

3. Save to `1_Projects/{{project}}/decisions/DR-{{date}}-{{seq}}.md`
   (Create decisions/ folder if it doesn't exist)

---

## MODE 2: REVIEW (revisit past decisions for learning)

If $ARGUMENTS = "review":

1. Scan `1_Projects/*/decisions/DR-*.md` for all recorded decisions
2. Filter for decisions where validation date has passed but Outcome = TBD
3. For each, ask CEO:
   - Was this decision CORRECT / WRONG / PARTIALLY RIGHT?
   - What would you do differently now?
   - What did you learn?

4. Generate review summary:

```
# DECISION REVIEW — {{today}}

## Decisions Validated This Session
| DR# | Decision | Confidence | Outcome | Lesson |
|-----|----------|-----------|---------|--------|
| DR-{{date}} | {{summary}} | {{H/M/L}} | {{C/W/P}} | {{one line}} |

## Calibration Check
- Decisions marked HIGH confidence: {{N}} → {{%}} actually correct
- Decisions marked LOW confidence: {{N}} → {{%}} actually correct
- **Calibration gap:** {{overconfident / underconfident / well-calibrated}}

## Pattern Detected
{{any recurring pattern: always choosing cheapest option? always delaying irreversible decisions? always overconfident on timeline estimates?}}
```

---

## MODE 3: PATTERN (analyze decision history for meta-patterns)

If $ARGUMENTS = "pattern":

1. Read all `1_Projects/*/decisions/DR-*.md`
2. Analyze across dimensions:

```
# DECISION PATTERN ANALYSIS — {{today}}

## Decision Volume
- Total decisions recorded: {{N}}
- By project: {{breakdown}}
- By phase: {{Phase 1 / 2 / 3 / 4}}
- Decisions/week average: {{N}}

## Confidence Calibration
| Stated Confidence | Actually Correct | Calibration |
|------------------|-----------------|-------------|
| HIGH | {{%}} | Over/Under/Good |
| MEDIUM | {{%}} | Over/Under/Good |
| LOW | {{%}} | Over/Under/Good |

## Decision Speed
- Average time from "question raised" to "decision made": {{days}}
- Fastest domain: {{Mech / Elec / SW}}
- Slowest domain: {{which and why}}

## Reversibility Pattern
- % of decisions that were Easy to reverse: {{%}}
- % Hard: {{%}}
- % Irreversible: {{%}}
- Do you tend to avoid irreversible decisions? {{Y/N — and is that good or bad?}}

## Information Gap Pattern
- Most common missing info type: {{supplier data / test results / customer feedback / cost data}}
- Do you decide WITH the gap or WAIT? {{tendency}}
- When you decided with gaps, were you more/less often correct?

## Core vs Offload Pattern
- % Core decisions: {{%}} (target: CEO handles truly novel/judgment-heavy decisions)
- % Offload decisions: {{%}} (target: routine decisions delegated to AI)
- Are you spending Core time on truly Core decisions? {{Y/N}}

## Recurring Traps
{{identify any of these patterns:}}
- Analysis paralysis: decisions taking >2 weeks without new information
- Premature commitment: deciding before key data is available
- Anchoring: always choosing the first option considered
- Sunk cost: continuing because of past investment, not future value
- Availability bias: overweighting recent experiences

## Growth Areas
1. {{specific area where judgment could improve}}
2. {{specific area}}
3. {{specific area}}

## Galaxy Connection
{{link to relevant Galaxy notes: "Phan doan khong the uy thac cho AI", "Skin in the Game", etc.}}
```

---

## MODE 4: CHALLENGE (pre-mortem on an upcoming decision)

If $ARGUMENTS = "challenge":

1. Ask: What decision are you about to make?
2. Run a structured pre-mortem:

```
# DECISION CHALLENGE — {{decision_summary}}
**Date:** {{today}} | **Project:** {{project}}

## The Decision
{{what CEO is about to decide}}

## Pre-Mortem: "It's 6 months later and this was WRONG. Why?"
1. {{scenario 1 — what could go wrong}}
2. {{scenario 2}}
3. {{scenario 3}}

## Devil's Advocate
- What would someone who DISAGREES with this decision say?
- {{strongest counter-argument}}

## Analogous Decisions
{{search decision records for similar past decisions}}
- DR-{{ref}}: Similar situation, outcome was {{X}} — lesson: {{Y}}

## Information You're Missing
- {{what you don't know that could change this decision}}
- Can you get this information before deciding? {{Y/N, effort}}
- If NO: what's your confidence given the gap?

## Reversibility Check
- If wrong, can you reverse within: {{hours / days / weeks / never}}
- Cost of reversal: {{$, time, reputation}}
- Cost of DELAY (not deciding now): {{$, time, opportunity cost}}

## Recommendation
- **Decide now** if: cost of delay > cost of potential reversal
- **Wait** if: key information arriving within {{N}} days AND cost of delay is low
- **Prototype first** if: you can test the decision cheaply before committing
```

RULES:
- This skill is fundamentally CORE — it develops CEO judgment, not replaces it
- AI facilitates the reflection process but NEVER tells CEO what to decide
- Decision records are permanent — never delete, even wrong ones (they're learning material)
- Review mode should be run at least monthly (integrate with /reflect)
- Pattern analysis requires minimum 10 recorded decisions to be meaningful
- Challenge mode is most valuable for irreversible or high-cost decisions
- Always link back to Galaxy notes about judgment, especially "Phan doan khong the uy thac cho AI"
- dJ/dt metric: track whether CEO's calibration improves over time (HIGH confidence accuracy trending up)
- If CEO is delegating decisions that should be Core, flag it — this is the R3 AI Dependency Spiral
- COD: The skill itself is Offload (AI structures the reflection), but the CONTENT is Core (CEO's judgment)
