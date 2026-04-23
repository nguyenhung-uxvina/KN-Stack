---
name: learn-track
description: Triggers on "track learning", "journal", "nhật ký học", "self-assess", "rubric", "how am I doing", "learning progress", "đánh giá tiến độ học". Consolidates journal, progress tracker, and rubric generator into one skill.
---

# Learn-Track — Consolidated Learning Skill

**COD:** Journal writing = Core (learner owns reflection) | Rubric/tracker generation = Offload (AI)

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

## Mode 2: Progress Tracker (Offload — AI generates)

Output a **competency grid** for the stated topic.

**Format:**
```
Topic: [X]
Date: [YYYY-MM-DD]

| Dimension | Current Level | Target | Gap | Evidence |
|---|---|---|---|---|
| [dim 1]   | 1 Novice      | 3      | -2  | [what proves current level] |
| [dim 2]   | 2 Developing  | 4      | -2  | ... |
| ...       |               |        |     |     |
```

Levels: 1=Novice · 2=Developing · 3=Competent · 4=Proficient · 5=Expert

**Dimensions to include** (pick 4-6 relevant):
- Conceptual understanding
- Tool/method execution speed
- Error detection (can you catch your own mistakes?)
- Transfer (can you apply to a new problem?)
- Teaching ability (can you explain to a peer?)
- Physical/practical validation (have you tested it?)

**Defense engineering example (P&B mastery):**
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
2. **Run progress tracker** against that rubric (Offload — AI fills draft, learner corrects)
3. **Run journal** with prompts derived from the largest gaps in tracker (Core — learner writes)

Output sequence: Rubric → Tracker table → Journal prompts (do not write journal for the learner).
