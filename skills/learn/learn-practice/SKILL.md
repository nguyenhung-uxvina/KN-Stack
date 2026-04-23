---
name: learn-practice
description: Targeted drills, interleaving study schedules, and focus sessions for engineering learning. Triggers on "practice", "drill", "luyện tập", "schedule", "interleave", "focus session", "pomodoro", "study plan", "practice plan".
---

# /learn-practice — Engineering Practice & Learning System

**COD:** Offload (AI generates plan) | Core (learner executes + reflects)
**Galaxy links:** [[Training Scars]] · [[Muscle Memory Law]]

---

## Mode Detection

| Input contains… | Mode activated |
|----------------|----------------|
| "practice X", "drill", "luyện tập" | **Targeted Drills** |
| "study schedule", "study plan", "interleave", "plan my" | **Interleaving Schedule** |
| "focus", "pomodoro", "focus session", "time block" | **Focus Session** |
| "full plan", "everything", "combined" | **All three modes** |

---

## MODE 1 — Targeted Drills

*Use when:* "I need to practice [topic]"

### Drill Progression

**Week 1–2 (Foundation)**
- Purpose: Build vocabulary and basic pattern recognition
- Duration: 20–30 min/session
- Instructions: Work through canonical examples with solution visible; pause at each step and predict next action before reading
- Scoring: Count steps you predicted correctly / total steps (target ≥ 50%)

**Week 3–4 (Application)**
- Purpose: Transfer to slightly varied problems
- Duration: 30–45 min/session
- Instructions: Solve from scratch, check after completion; time yourself
- Scoring: Correct solution + time under target = pass (target: ≥ 70% correct)

**Week 5+ (Integration)**
- Purpose: Reproduce under realistic conditions (design review pressure, time constraints)
- Duration: 45–60 min/session
- Instructions: Simulate a Gate Review — no notes, defend decisions aloud or in writing
- Scoring: Could you defend it to a skeptical engineer? Yes/No

### Defense Engineering Drill Topics
- Pahl-Beitz phases: Task Clarification → Conceptual → Embodiment → Detail
- Requirements writing: quantified vs. wished requirements, DMIR/ODI format
- VDI 2225 evaluation matrix: weighted criteria, variant scoring
- FEM/simulation setup: boundary conditions, mesh sensitivity
- Gate Review: G1/G2/G3 checklist execution

---

## MODE 2 — Interleaving Schedule

*Use when:* "Plan my study schedule for [topics] over [N] weeks"

### Rules
1. Never schedule the same topic in consecutive sessions
2. Minimum 2 topics interleaved per week (3 is optimal)
3. Morning blocks = new/hard material | Afternoon blocks = review/practice
4. Every 4th week = integration week (no new material, connect everything)

### Schedule Template (4-week unit, repeat as needed)

```
Week 1 — Introduction + Separation
  Mon AM: Topic A (new)       Mon PM: Topic A (drill)
  Wed AM: Topic B (new)       Wed PM: Topic B (drill)
  Fri AM: Topic C (new)       Fri PM: Mixed A+B drill

Week 2 — Deepening
  Mon AM: Topic B (extend)    Mon PM: Topic A (varied drill)
  Wed AM: Topic C (extend)    Wed PM: Topic B (varied drill)
  Fri AM: Topic A (extend)    Fri PM: Mixed B+C drill

Week 3 — Application
  Mon AM: Topic C (apply)     Mon PM: Topic A+C connection
  Wed AM: Topic A (apply)     Wed PM: Topic B+C connection
  Fri AM: Topic B (apply)     Fri PM: Mixed 3-topic drill

Week 4 — Integration (no new content)
  Mon: Review weakest topic from Weeks 1-3
  Wed: Simulate Gate Review using all 3 topics
  Fri: Write 1 Galaxy note from what changed in your thinking
```

Scale to 8–16 weeks by repeating the 4-week unit with increased difficulty.

---

## MODE 3 — Focus Session (90-min Block)

*Use when:* "Help me focus on [task]"

### Optimal 90-min Block Design

```
0:00 – 0:05   Orient (5 min)
  → State the single deliverable for this session (1 sentence)
  → Open only files needed; close everything else

0:05 – 0:45   Deep Work Block 1 (40 min)
  → No interruptions; work on hardest sub-task first
  → If stuck >5 min: write the obstacle, move to next sub-task

0:45 – 0:50   Break (5 min)
  → Stand, move; no screens

0:50 – 1:20   Deep Work Block 2 (30 min)
  → Resolve obstacles noted in Block 1
  → Or switch to review/verification if main task complete

1:20 – 1:30   Consolidation (10 min)
  → Write 3 bullets: what was done / what remains / what surprised you
  → Update Status.md if design work; append to _meta/decisions.md if decision made
```

### For Design Work Specifically
- Block 1 → generation (morphological matrix, sketching, sizing)
- Block 2 → evaluation (VDI 2225, FEM check, coupling analysis)
- Consolidation → log design decision with rationale

### Nesting Focus Sessions in a Week
- Max 3 deep sessions/day (90 min each = 4.5 hr deep work)
- Alternate domain per session where possible (avoid [[Training Scars]] from massed practice)
- Log energy level (1–5) at session end; reschedule high-stakes work to your peak window

---

## COMBINED PLAN

When asked for a full practice plan, output all three sections in order:
1. Drill map for the topic(s) with week-by-week progression
2. Interleaving schedule for the planning horizon
3. Recommended focus session structure per session type

---

## Output Format

Always end any plan with:

```
NEXT ACTION (Core — CEO executes):
□ [Specific first step to do today]
□ [Reflection checkpoint: when + what question to ask]

ANALYST TRAP CHECK:
Is this plan generating physical validation data or more analysis?
If answer is "analysis only" → add at least 1 physical drill (prototype, test, hands-on).
```
