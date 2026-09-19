---
name: learn-track
description: Tracks engineering learning in three modes — journal reflection prompts (learner writes), a competency progress grid with evidence per level, and a behavioral rubric generator with observable 1/3/5 anchors. For design decision records use /journal or /helix-design-journal, for design-review rubrics use /helix-design-review. Triggers on "track learning", "learning journal", "nhật ký học", "self-assess", "learning rubric", "rubric học tập", "learning progress", "tiến độ học", "đánh giá tiến độ học".
---

# Learn-Track — Consolidated Learning Skill

**COD:** Journal writing = Core (learner owns reflection) | Rubric + tracker grid + measured evidence = Offload (AI) | Scoring own level = Core (learner, from the numbers)

**Galaxy links:** [[Output Loop]] · [[dD dt Lớn Hơn dV dt]]

---

## Auto-Detect Mode

| Trigger phrase | Mode activated |
|---|---|
| "journal my learning", "nhật ký học" | → **Journal** |
| "how am I progressing?", "đánh giá tiến độ" | → **Progress Tracker** |
| "create rubric for X", "self-assess" | → **Rubric Generator** |
| "track + assess + journal" | → **Combined flow** (Rubric → Tracker → Journal) |

If ambiguous, ask: "Journal reflection, progress check, or rubric generation?"

---

## Mode 1: Journal (Core — learner writes)

Generate **5-7 reflection prompts** tied to the content's key dynamics. At least one prompt must surface a feedback loop.

**Prompt structure:**
1. What was the key mechanism/principle I encountered today?
2. Where did my mental model break down or get updated?
3. *[Feedback loop prompt]* What loop is driving improvement here — what reinforces it, what balances it?
4. What would I do differently if I repeated this task?
5. What physical evidence (test result, prototype, calculation) confirmed or challenged my understanding?
6. What is the next smallest action to deepen this?
7. *(Optional)* What Galaxy note does this connect to?

**Defense engineering example:**
> Learning Pahl-Beitz Phase 2 (Conceptual Design)?
> - Loop prompt: "What reinforcing loop makes early concept errors compound — and how does the morphological matrix break that loop?"
> - Physical evidence: "Did any concept score change after you calculated actual mass or force budget?"

---

## Mode 2: Progress Tracker (Offload grid + evidence — Core level)

Output a **competency grid** for the stated topic. **The AI never assigns Current Level.** It builds the grid and fills Evidence with measurements. The learner scores the level while looking at the numbers. An AI's impression of "level 3" is the same fluency illusion `/learn-teach` exists to catch: neither the AI nor the learner can see it without a cold measurement.

### Step 1 — Look for the measurement first

If a `/learn-teach` workspace exists for this topic (`RETRIEVAL.md` in the current folder, or `LEARN/learn/RETRIEVAL.md` inside a `/book-to-learn` cycle), run:

```bash
python <KN-Stack>/skills/learn/learn-track/scripts/retrieval_stats.py <workspace or RETRIEVAL.md>
```

- **Exit 0:** use its numbers as Evidence: recall rate, the "chắc mà sai" (confident-but-wrong) items, overdue items, and the per-lesson table. Map each dimension to the lessons (`Bài`) that measure it.
- **Exit 1:** some ledger rows are unreadable and are listed. Fix the ledger, then re-run. Do not build the grid on partial numbers.
- **Exit 2:** no ledger found. Evidence then comes only from artifacts (test results, `Run_Log.md`, reviewed designs). Write `chưa có phép đo` where none exist, never an estimate.

### Step 2 — Grid

```
Topic: [X]
Date: [YYYY-MM-DD]
Measurement: [retrieval_stats line "Đã hồi tưởng … nhớ đúng …", or "chưa có phép đo"]

| Dimension | Lessons (Bài) | Evidence (measured) | Current Level (learner) | Target | Gap |
|---|---|---|---|---|---|
| [dim 1] | 01, 02 | nhớ đúng 4/6 · chắc mà sai 1 (#2) | ← learner fills | 3 | |
| [dim 2] | — | chưa có phép đo | ← learner fills | 4 | |
```

Levels: 1=Novice · 2=Developing · 3=Competent · 4=Proficient · 5=Expert

**Rules the AI enforces after the learner fills the levels:**
- A dimension whose lessons contain a **"chắc mà sai"** item and whose self-score is ≥ 3 gets flagged: *"You scored this Competent, but #N is a confident miss — the one error you cannot self-detect."* The learner may keep the score, but the flag stays in the grid.
- Recall measures **memory, not doing**. The *Physical/practical validation* dimension never takes RETRIEVAL numbers as evidence. It needs a test result, a prototype, or a reviewed deliverable.
- `retrieval_stats` reports a snapshot of the **latest** recall per item (the ledger keeps no history). To show progress over time, compare two dated trackers. Do not infer a trend from one run.

**Dimensions to include** (pick 4-6 relevant):
- Conceptual understanding
- Tool/method execution speed
- Error detection (can you catch your own mistakes?)
- Transfer (can you apply to a new problem?)
- Teaching ability (can you explain to a peer?)
- Physical/practical validation (have you tested it?)

**Defense engineering example (P&B mastery). Levels below were scored by the learner, not the AI:**
| Dimension | Current | Target | Gap |
|---|---|---|---|
| Task clarification (Step 1-2) | 2 | 4 | -2 |
| Function structure (Step 3) | 1 | 3 | -2 |
| VDI 2225 scoring | 1 | 3 | -2 |
| Running a Gate Review | 1 | 4 | -3 |

---

## Mode 3: Rubric Generator (Offload — AI generates)

Generate a **6-10 dimension rubric** with behavioral indicators at 3 anchor points.

**Format per dimension:**
```
### [Dimension Name]
- **1 — Novice:** [specific observable behavior]
- **3 — Competent:** [specific observable behavior]
- **5 — Expert:** [specific observable behavior]
```

Rules:
- Behavioral indicators must be observable, not vague ("can explain" not "understands")
- At least one dimension must address physical/empirical validation
- At least one dimension must address error/failure handling

**Defense engineering example — Design Review Readiness:**

### Requirements Completeness
- 1: Requirements exist but many are qualitative or untestable
- 3: ≥ 80% requirements quantified with test method defined
- 5: 100% quantified, linked to functions, with rationale for each threshold

### Gate Decision Quality
- 1: Can only say pass/fail; cannot articulate what evidence drove the decision
- 3: States pass/fail with supporting evidence and open issues list
- 5: Predicts failure modes before review; proposes conditional pass criteria

### Physical Evidence Integration
- 1: Relies solely on analysis; no prototype or test data cited
- 3: At least one physical test result cited per critical requirement
- 5: dP/dt tracked; test results directly updated design parameters

---

## Combined Flow

When user wants full cycle:
1. **Generate rubric** for topic X (Offload)
2. **Run progress tracker** against that rubric (Offload: grid + measured Evidence via `retrieval_stats.py`. Core: the learner scores every Current Level. The AI does not pre-fill levels.)
3. **Run journal** with prompts derived from the largest gaps in tracker (Core — learner writes). If `retrieval_stats` listed "chắc mà sai" items, one prompt must name one of them: *"You were sure about #N and missed it. What did you think the answer was, and why did it feel certain?"*

Output sequence: Rubric → Tracker table → Journal prompts (do not write journal for the learner).
