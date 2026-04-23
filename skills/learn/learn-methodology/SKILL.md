---
name: learn-methodology
description: Master any engineering concept using auto-detected learning technique. Triggers on "learn concept", "explain", "giải thích", "feynman", "chunking", "mnemonic", "learning path", "how to learn", "học concept"
---

# /learn-methodology — Unified Learning Skill

**COD:** Offload (AI generates technique output) | Core (learner validates understanding)
**Galaxy links:** [[Muscle Memory Law]] · [[dJ dt lớn hơn dD dt]]

---

## Auto-Detection Logic

Read user input and select technique:

| Trigger words | Technique |
|--------------|-----------|
| "explain simply", "giải thích đơn giản", "feynman", "ELI5" | → **FEYNMAN** |
| "break down", "chunk", "phân tách", "step by step" | → **CHUNKING** |
| "help me remember", "mnemonic", "nhớ", "acronym" | → **MNEMONIC** |
| "learning path", "how to learn", "lộ trình", "learning architecture" | → **ARCHITECTURE** |
| Ambiguous / "comprehensive" / "full" | → Ask user, or run FEYNMAN → CHUNKING sequence |

---

## TECHNIQUE 1: FEYNMAN — 60-Second Explanation

**When:** User wants to understand a concept quickly and test comprehension.

**Output format:**

```
## Feynman: [Concept Name]

### Core Idea (plain language, no jargon)
[1-3 sentences a 15-year-old could follow]

### Analogy
[Concrete comparison to everyday object or experience]
Defense example: "Charge amplifier = like a bucket (capacitor) catching rain (charge) —
the water level (voltage) tells you how hard it rained (force), not the rain rate."

### Where It Breaks Down
[1 sentence: where the analogy fails — builds accurate mental model]

### Diagnostic Questions (answer these to confirm understanding)
1. [Question testing recall]
2. [Question testing application]
3. [Question testing edge case]

### If you couldn't answer Q2 or Q3 → re-read [specific section/concept]
```

---

## TECHNIQUE 2: CHUNKING — Dependency Hierarchy

**When:** User needs to learn a large/complex topic systematically.

**Output format:**

```
## Chunking Map: [Topic]

### Prerequisite Check
Before starting, you need: [list 2-4 foundational concepts]
Missing any? → Learn those first (run /learn-methodology on each)

### Chunk Structure (4-8 chunks, 5-9 concepts each)

**Chunk 1 — [Foundation layer name]** (learn first)
- Concept A
- Concept B
- Concept C
→ Mastery test: [1-sentence test]

**Chunk 2 — [Next layer]** (needs Chunk 1)
- Concept D (depends on A)
- Concept E
→ Mastery test: [1-sentence test]

[Continue to Chunk N...]

### Dependency Graph (text form)
A → D → G
B → D
C → E → H
E → F

### Suggested Session Schedule
- Session 1: Chunk 1 (≈45 min)
- Session 2: Chunk 2 (≈45 min)
- [...]
- Capstone: Apply to [real project task at Workshop X]
```

---

## TECHNIQUE 3: MNEMONIC — Memory Aid

**When:** User needs to retain a list, sequence, formula, or set of rules.

**Output format:**

```
## Mnemonic: [Concept/List Name]

### What to Remember
[The original list/sequence/rule being encoded]

### Acronym / Keyword Chain
[Meaningful acronym where each letter = key term]
Example for Pahl-Beitz phases: **T-C-E-D**
T = Task Clarification
C = Conceptual Design
E = Embodiment Design
D = Detail Design
→ "The CEO Executes Details"

### Retrieval Cue
[How to trigger recall: a question, image, or physical gesture]
"When starting any design: ask 'The CEO Executes Details?' → expands to 4 phases"

### Spaced Repetition Schedule
- Day 0: Create mnemonic
- Day 1: Recall without notes (< 30 sec)
- Day 3: Recall + explain each term
- Day 7: Apply to a real task
- Day 21: Spot-check

### Defense Engineering Example
[Show mnemonic applied to VN defense context: BB-01, VN-AST, VDI 2225, MIL-STD, etc.]
```

---

## TECHNIQUE 4: ARCHITECTURE — Full Learning Pathway

**When:** User wants to build deep competence in a domain over weeks/months.

**Output format:**

```
## Learning Architecture: [Domain]

### Outcome Definition
After completing this path, you will be able to:
- [Skill 1 — measurable]
- [Skill 2 — measurable]
- [Skill 3 — apply in Workshop X context]

### Prerequisite Chain
[Domain] requires:
└── [Prereq A] requires:
    └── [Prereq A1]
└── [Prereq B] (can learn in parallel with A)

### Phase Structure

**Phase 1 — Foundations** (Week 1-2)
Resources: [book chapter / paper / hands-on task]
Output: [what you build/produce to prove phase complete]
Gate: [1-sentence mastery test]

**Phase 2 — Core Skills** (Week 3-5)
Resources: [...]
Output: [prototype / analysis / design document]
Gate: [...]

**Phase 3 — Integration** (Week 6-8)
Apply to: [specific Workshop X project — BB-01 / VN-AST / etc.]
Output: [real deliverable]
Gate: [peer review or physical test result]

### Milestones & Metrics
| Week | Milestone | Evidence |
|------|-----------|---------- |
| 2    | [...]     | [...]     |
| 5    | [...]     | [...]     |
| 8    | [...]     | [...]     |

### Analyst Trap Warning
⚠️ If > 60% of time is reading/analysis with no physical output → trigger [[Muscle Memory Law]]:
Skills compound only through doing. Schedule a build/test task every 2 weeks minimum.
```

---

## Combining Techniques

For comprehensive onboarding to a new engineering domain, run in sequence:

1. **ARCHITECTURE** — get the map (30 min)
2. **CHUNKING** — break Phase 1 into learnable pieces (20 min)
3. **FEYNMAN** — validate each chunk after study (10 min/concept)
4. **MNEMONIC** — lock in key rules before applying (10 min)

Total setup time: ~70 min → saves weeks of inefficient study.

---

## Usage Examples

```
/learn-methodology Explain the charge amplifier circuit simply
→ FEYNMAN output for piezo signal chain (BB-01 context)

/learn-methodology Break down VDI 2225 evaluation method
→ CHUNKING output: 4 chunks, dependency graph, session schedule

/learn-methodology Help me remember the 7 Pahl-Beitz sub-steps of conceptual design
→ MNEMONIC output: acronym + spaced repetition schedule

/learn-methodology Design a learning path for marine structural analysis
→ ARCHITECTURE output: 8-week path, milestones, Workshop X integration

/learn-methodology Explain AND help me remember mooring chain catenary math
→ FEYNMAN → MNEMONIC sequence
```
