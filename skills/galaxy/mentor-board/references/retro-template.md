# DMIR R-Step Retrospective Template

The R-section of every consult is filled via `/mentor-board --retro <consult-id>`.

This is the **compound learning step** — without R, consultations are one-shot advice, not assets.

## Prompt CEO at Re2 (Mandatory Honesty)

```
═══════════════════════════════════════════════════════════════════════════════
DMIR RETROSPECTIVE — Consult <consult-id>
═══════════════════════════════════════════════════════════════════════════════

Original consultation:
  Date: <consult date>
  Mentor(s): <list>
  Problem: <problem statement>
  Predicted action (Frame 5): <Frame 5 actions from original>

CEO inputs (REQUIRED — honesty critical, no sycophancy):

1. **What action did you actually take?**
   Be concrete. Which Frame 5 step, modified or not?
   If you took none → say so.
   If you took a DIFFERENT action than recommended → describe what + why.
   
   [CEO answer]

2. **What outcome happened?**
   Factual, dated. No "good" / "ok" / "fine" — give specifics.
   - Date outcome became clear: <date>
   - What measurable result: <numbers if available>
   - Externalities you didn't control for: <list>
   
   [CEO answer]

3. **Did the mentor's prediction hold?**
   Choose ONE per mentor (no compromise):
   - HIT — prediction matched outcome closely
   - MISS — outcome contradicted prediction
   - PARTIAL — outcome matched on some dimensions, missed on others
   
   [Per-mentor verdict]

4. **What did you learn about this mentor's framework applicability to Workshop X?**
   Examples:
   - "Munger's margin-of-safety works perfectly here — slowed me down from over-paying"
   - "Musk's first-principles approach didn't translate — VN supply chain constraints invalidate the assumption that 'parts can always be sourced cheaper'"
   - "Naval's specific knowledge framing was right but timing was wrong — needed 6 more months of market signal"
   
   [CEO answer]

5. **Would you consult this mentor again for this problem class?**
   - YES, with same weight
   - YES, with downweight (less reliable for this class)
   - NO, framework doesn't apply to WX context for this class
   - PARTIAL — only useful in specific scenarios (specify)
   
   [CEO answer]
═══════════════════════════════════════════════════════════════════════════════
```

## R-Section Format (Appended to Original Consult File)

```markdown
## FRAME 6 — REFLECT (R)

### Retrospective filled on: <YYYY-MM-DD>

### Action taken
<from CEO Q1>

### Outcome
- Date: <from CEO Q2>
- Result: <factual>
- Externalities: <list>

### Per-mentor verdicts
| Mentor | Prediction | Verdict | Learning |
|--------|-----------|:-------:|----------|
| <Leader A> | <Frame 5 prediction summary> | HIT/MISS/PARTIAL | <CEO learning> |
| <Leader B> | (same) | | |

### Framework applicability lessons
<from CEO Q4 — long-form>

### Future consult preference
<from CEO Q5 — per mentor>

### Pattern flags (auto-detected by mentor-board)
<populated by Re5 step if patterns detected, e.g., "5+ misses on capital class for Musk" — see below>
```

## reliability_log.md Update Schema

Each mentor has `D:/Workshop_X/3_Resources/Mentor-Board/<leader>/reliability_log.md`:

```markdown
---
mentor: <leader>
updated: <today>
total_predictions: <N>
total_hits: <H>
total_misses: <M>
total_partials: <P>
overall_reliability: <H / total>
---

# Reliability Log — <leader>

## Per-Class Stats

| Problem class | N | Hits | Misses | Partials | Reliability % | Confidence |
|---------------|:-:|:----:|:------:|:--------:|:------------:|:----------:|
| capital | 8 | 6 | 1 | 1 | 75% | HIGH (N≥5) |
| scaling | 3 | 2 | 0 | 1 | 67% | LOW (N<5) |
| ai-strategy | 0 | - | - | - | - | NO DATA |

## Per-Consult History

| Date | Consult ID | Problem class | Predicted | Actual | Verdict | Notes |
|------|-----------|---------------|-----------|--------|:-------:|-------|
| 2026-05-20 | 20260520-musk-vc | capital | "Take VC, dilute, scale fast" | Took 500M instead, kept control | MISS | Underestimated VN procurement velocity |
| 2026-06-15 | 20260615-musk-fab | scaling | "Vertical integrate by year 1" | Outsourced anodizing, kept assembly | PARTIAL | Right principle, wrong scope |

## Patterns Detected

<populated when >5 consults same class:>

⚠️ <leader> has <N> misses in <class> consultations.
Recommendations:
(1) Revise persona prompt to reduce overconfidence in <class>
(2) Downgrade weight in --decide for <class>
(3) Add complementary mentor (suggested: <name>)

[CEO action taken: <date> <action>]
```

## Re5 Pattern Detection Logic

After updating reliability_log:

```python
for class in mentor.problem_classes:
    if class.misses >= 5 and class.misses / class.total > 0.5:
        flag_pattern(
            mentor=mentor,
            class=class,
            severity="HIGH",
            recommendations=[
                "Revise persona prompt",
                "Downgrade DECIDE weight",
                "Add complementary mentor"
            ]
        )
        prompt_ceo_action()
```

CEO decides — **C** (non-delegable):
- Revise persona → CEO edits `mentor-<leader>/references/persona.md`
- Downgrade weight → automatic in `decide-matrix.md` formula
- Add complementary → `/mentor-board --add <suggested>`
- Accept pattern → log decision but don't act

## Honesty Enforcement

The skill MUST refuse low-quality retros:

- "I took some action, it went well" → re-prompt: "Specific action. Specific outcome with date and numbers."
- "Hard to say if prediction held" → re-prompt: "Pick HIT, MISS, or PARTIAL. If genuinely ambiguous → PARTIAL."
- "Mentor was generally right" → re-prompt: "Per-prediction verdict. Frame 5 had 3 actions — verdict per action."

The whole compounding value depends on honest tracking. Sycophancy = useless reliability data = misleading DECIDE weights downstream.

## Periodic Aggregate Review

Recommended cadence: after every 10 retros across all mentors, CEO runs:

```
/mentor-board --list --verbose
```

→ Shows aggregate reliability table across all mentors + suggests `--suggest` if gaps detected.
