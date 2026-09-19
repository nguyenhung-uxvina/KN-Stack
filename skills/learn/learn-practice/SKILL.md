---
name: learn-practice
description: Targeted drills, interleaving study schedules, and 90-minute focus sessions for engineering learning — produces a practice plan as text, does not create calendar events or recurring agents (that is /schedule) and does not run the DMIR learning cycle (that is /cycle). With --source <file|folder|notebook> the drill topics, worked examples and answer keys come from a specific book, every book claim a verbatim «quote» checked by learn-methodology's quote_check.py. Triggers on "practice plan", "practice drills", "drill", "luyện tập", "bài luyện", "interleave", "interleaving", "lịch học xen kẽ", "study schedule", "lịch ôn", "focus session", "pomodoro", "luyện theo sách".
argument-hint: "<chủ đề hoặc yêu cầu> [--source <tệp|thư mục|notebook> ...]"
---

# /learn-practice — Engineering Practice & Learning System

**COD:** Offload (AI generates plan) | Core (learner executes + reflects)
**Galaxy links:** [[Training Scars]] · [[Muscle Memory Law]]

---

## --source — Practising What a Book Teaches

Without `--source`, drills use general knowledge and the fixed topic list below. With `--source`, drill **what the book teaches**. Practising the wrong version of a method is worse than not practising ([[Training Scars]]).

`--source` takes the same values as `/learn-methodology --source`: a file, a folder (e.g. `BOOK/_source/`), or an NLM notebook id/alias. **First load the Skill `learn-methodology:references:source-mode`.** Steps S1 (resolve and dump the source), S2 (NLM traps), S3 (label rules: `«quote»` / paraphrase / `[AI]`) and S4 (the gate) apply unchanged. This section says only what differs for practice:

1. **Topics come from the book.** Each drill topic is a framework or procedure the book names, introduced by a `«quote»` that defines it. The fixed *Defense Engineering Drill Topics* list below is not used. Inside a `/book-to-learn` cycle, the topics are exactly `framework_ung_vien` in `LEARN/_pipeline_state.md`. Add no others.
2. **Week 1–2 worked examples are the book's own**, quoted with location. **Recompute every one before using it as an answer key.** A book's worked example can contradict its own text. Measured on the CFMA paper (Hari & Weiss): the prose gives the bulb-failure severity as 8, while Table 1 shows 10; and a row shows SFD 40 where S × F × D = 4. An inconsistent example goes into a `## Chỗ nguồn tự mâu thuẫn` section and is **not** an answer key.
3. **Week 3–4 varied problems are `[AI]`**, and each answer key names the book rule that decides it as a `«quote»`. If the book's rules cannot decide the answer, drop the problem. It tests general knowledge, not the book.
4. **Week 5+ gate review:** the checklist is the book's own criteria or steps, quoted. The learner defends against those, not against AI-invented criteria.
5. **Interleaving:** Topics A/B/C are book frameworks. Where a real Workshop X task exists, a real-work block counts as a topic, so book blocks alternate with applying them.
6. **Book has no worked example for a topic** → `KHOẢNG TRỐNG`, and an `[AI]` example whose answer the learner checks against the quoted rule.
7. **Gate:** write the plan to a file (`LEARN/learn/lp-plan-<topic>.md` inside a `/book-to-learn` cycle, otherwise the scratchpad), then run
   `python <KN-Stack>/skills/learn/learn-methodology/scripts/quote_check.py <plan.md> --nguon <source>`.
   Exit codes are handled as in source-mode S4. A plan that has not exited 0 is not "book-grounded".

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
- Requirements writing: quantified vs. wished requirements, ODI outcome statements ([Direction] + [Metric] + [Object of control] + [Context clarifier], see `/odi`)
- VDI 2225 evaluation matrix: weighted criteria, variant scoring
- FEM/simulation setup: boundary conditions, mesh sensitivity
- Gate Review: G1/G2/G3 checklist execution

---

## MODE 2 — Interleaving Schedule

*Use when:* "Plan my study schedule for [topics] over [N] weeks"

### Rules
1. Never schedule the same single topic in consecutive sessions — including across days (Mon PM → Wed AM counts as consecutive). A mixed session (A+B, 3-topic) may sit next to one of its own topics: it is already interleaved.
2. Minimum 2 topics interleaved per week (3 is optimal)
3. Morning blocks = new/hard material | Afternoon blocks = review/practice. One exception: Week 1 Mon PM introduces Topic B, because A is the only thing learned so far and drilling it would break rule 1.
4. Every 4th week = integration week (no new material, connect everything)

**Before outputting a schedule, walk it session by session and check rule 1 on every adjacent pair.** An earlier version of this template broke rule 1 in Week 1 (A→A, B→B) and nobody noticed, because a template reads as correct at a glance.

### Schedule Template (4-week unit, repeat as needed)

```
Week 1 — Introduction (sequence A · B · C · A · B · C)
  Mon AM: Topic A (new)       Mon PM: Topic B (new, light intro)
  Wed AM: Topic C (new)       Wed PM: Topic A (drill)
  Fri AM: Topic B (deepen)    Fri PM: Topic C (drill)

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
