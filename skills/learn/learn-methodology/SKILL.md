---
name: learn-methodology
description: Master any engineering concept using auto-detected learning technique (Feynman, chunking, mnemonic, learning architecture). With --source <file|folder|notebook> it teaches what a specific book or book cluster says instead of general knowledge — every book claim is a verbatim «quote» machine-checked against the source by scripts/quote_check.py. Triggers on "learn concept", "explain", "giải thích", "feynman", "chunking", "mnemonic", "learning path", "how to learn", "học concept", "học theo sách", "bám sách", "learn from this book", "giải thích theo sách"
argument-hint: "<khái niệm hoặc yêu cầu> [--source <tệp|thư mục|notebook> ...]"
---

# /learn-methodology — Unified Learning Skill

**COD:** Offload (AI generates technique output) | Core (learner validates understanding)
**Galaxy links:** [[Muscle Memory Law]] · [[dJ dt lớn hơn dD dt]]

---

## --source — Learning from a Book or Book Cluster

Without `--source`, this skill teaches a **topic** from general knowledge. With `--source`, it teaches **what the book says**. Books define, count, and quantify differently from general knowledge, and that difference is usually the part worth learning.

`--source` accepts a file (`.pdf` `.epub` `.md` `.txt`), a folder (e.g. `BOOK/_source/` from `/book-to-learn` L2), or an NLM notebook id/alias (e.g. `btl-<slug>-goc`). Repeat the flag for a book cluster.

**Before doing anything in this mode, read [references/source-mode.md](references/source-mode.md).** It holds steps S1–S4, the per-technique rules, and the NLM traps. The non-negotiable rules:

1. **Every "the book says" line is a verbatim `«quote»`** in the book's original language, ≥ 5 words, followed by [source, location]. Every number taken from the book sits inside «…».
2. **Anything the AI invents is labelled `[AI]`**: analogies, acronyms, diagnostic questions, Workshop X examples. It is allowed, but it must not borrow the book's authority.
3. **Location comes from the script's output, never typed by hand.** A guessed page number looks identical to a read one.
4. **The book is silent → `KHOẢNG TRỐNG`, never general knowledge.** Try ≥ 3 spellings or synonyms first. Most misses are search misses.
5. **Machine gate:** write the output to a file (`LEARN/learn/lm-<technique>-<concept>.md` inside a `/book-to-learn` cycle, otherwise the scratchpad), then run
   `python <KN-Stack>/skills/learn/learn-methodology/scripts/quote_check.py <output.md> --nguon <source> [--nguon ...]`
   - **Exit 0:** paste its `Tổng:` line at the end of the output.
   - **Exit 1:** fix every `KHÔNG THẤY` / `QUÁ NGẮN` line by re-copying from the book, or delete the claim. Then re-run.
   - **Exit 2:** stop and tell the user. The output may not be called "source-grounded" until the script exits 0.
6. **Book cluster:** add a mandatory `## Chỗ các nguồn khác nhau` section with conflicting quotes side by side, never merged into one voice.

The four techniques below keep their formats; source-mode.md specifies what changes in each.

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

/learn-methodology giải thích đơn giản "morphological matrix" --source "D:/Workshop_X/3_Resources/Books/pahl-beitz/_source"
→ FEYNMAN bám sách: định nghĩa là «trích» + vị trí, phép so sánh gắn [AI], cổng quote_check mã 0

/learn-methodology giúp nhớ các bước thiết kế ý tưởng --source btl-pahl-beitz-goc
→ dump nguồn NLM ra tệp → MNEMONIC: danh sách chép từ sách, đúng số bước và thứ tự

/learn-methodology phân tách "requirements list" --source pahl-beitz.pdf --source cross-design-methods.pdf
→ CHUNKING theo chương từng cuốn + mục bắt buộc "Chỗ các nguồn khác nhau"
```
