Plan a D-M-I-R learning cycle for a specific topic, project, or skill.

Usage: /cycle [topic] OR provide details interactively.

1. If $ARGUMENTS provided, use as topic; otherwise ask:
   - What topic or skill are you planning a learning cycle for?
   - What is your current understanding level? (novice / intermediate / advanced)
   - What triggered this learning need? (project requirement, failure, curiosity)
   - How much time can you allocate? (hours/week)

2. Generate the DMIR cycle plan:

```
# D-M-I-R CYCLE PLAN — {{topic}}
**Date:** {{today}}  |  **Duration:** {{weeks}}  |  **Hours/week:** {{hours}}

---

## CYCLE OBJECTIVE
**By the end of this cycle, I will be able to:**
{{specific, measurable capability — not "understand X" but "apply X to Y and get Z result"}}

---

## D — DIAGNOSE (Week 1)
**Goal:** Understand current state honestly. What do I know? What don't I know? What do I think I know but might be wrong about?

| Activity | Time | Output |
|----------|------|--------|
| Self-assessment: write what I currently know | 1h | Knowledge map (honest) |
| Identify gaps: what can't I do that I need to? | 30m | Gap list |
| Find sources: who/what can teach me? | 30m | Resource list |
| Test current skill: attempt a real task | 1-2h | Baseline performance |

**Diagnostic questions:**
- Where am I on the Dreyfus scale? (Novice → Advanced Beginner → Competent → Proficient → Expert)
- What's my biggest misconception likely to be?
- What's the difference between knowing about X and being able to DO X?

---

## M — MODEL (Week 2)
**Goal:** Build a mental model of how the system/skill works. Understand the structure, not just the surface.

| Activity | Time | Output |
|----------|------|--------|
| Study core framework/theory | 2-3h | Framework summary |
| Build causal model (/cld if systems topic) | 1h | CLD or concept map |
| Identify key principles (max 5) | 30m | Principles list |
| Find analogies to things I already know | 30m | Analogy map |

**Modeling questions:**
- What are the 3-5 core principles?
- What's the causal structure? (what causes what?)
- What are the common failure modes?
- What does mastery look like? (reference examples)

---

## I — INTERVENE (Weeks 3-4)
**Goal:** Apply the model to real work. Deliberately practice. Make mistakes in safe environments.

| Activity | Time | Output |
|----------|------|--------|
| Apply to current project | 2-3h/wk | Work product |
| Deliberate practice on weak areas | 1h/wk | Practice log |
| Get feedback (from results, peers, or AI review) | 30m/wk | Feedback notes |
| Adjust model based on practice | 30m/wk | Updated model |

**Intervention rules:**
- Practice must involve REAL stakes (not toy problems)
- Feedback loop must be <24h (fast feedback = fast learning)
- Track errors: what went wrong and WHY (not just what)
- One skill focus per cycle — no multitasking learning

---

## R — REFLECT (End of cycle)
**Goal:** Extract permanent insights. Update Galaxy. Plan next cycle.

| Activity | Time | Output |
|----------|------|--------|
| Run /reflect on the cycle | 30m | DMIR reflection |
| Extract Galaxy-worthy insights | 30m | 1-3 permanent notes |
| Update skill self-assessment | 15m | New Dreyfus level |
| Plan next cycle (if needed) | 15m | Next cycle brief |

**Reflection questions:**
- What surprised me?
- What was harder/easier than expected?
- What would I tell past-me at the start of this cycle?
- Has my mental model changed? How?
- What's the ONE insight worth preserving? (-> Galaxy note)

---

## SUCCESS CRITERIA
- [ ] Can I DO the thing, not just describe it?
- [ ] Have I applied it to real work (not just exercises)?
- [ ] Have I extracted >=1 Galaxy note from this cycle?
- [ ] Do I know what I still DON'T know? (conscious incompetence > unconscious incompetence)

---

## ANTI-PATTERNS TO AVOID
- [ ] Tutorial hell: consuming content without practicing
- [ ] Premature teaching: explaining before understanding
- [ ] Skipping Diagnose: assuming you know your starting point
- [ ] Skipping Reflect: learning without extracting = forgetting
```

3. Present plan to user. Adjust based on time constraints and priorities.

RULES:
- One DMIR cycle = one topic. No multitasking.
- Minimum cycle length: 2 weeks. Maximum: 6 weeks. Longer = scope too big, split it.
- Real work > exercises. Always tie learning to a current project if possible.
- Galaxy output is mandatory — a cycle without a permanent note is incomplete.
- COD: Core (CEO learns) with Offload (AI structures the plan)
- Cross-reference: dJ/dt > dD/dt — judgment must grow faster than delegation
