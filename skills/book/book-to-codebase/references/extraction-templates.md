# Extraction Templates — book-to-codebase R2

> Used by `/btc-extract` (Block R2). All queries are NLM notebook queries against the ingested book.
> Assumes the book's NLM notebook was already created by `codebase-to-book` P8.
> If no NLM notebook exists: R1 creates one from the canonical chapters before R2 begins.

## R2.0 — Apply This Pre-Pass (1 fan-out call, all chapters)

**Purpose:** Identify all "Apply This" spec blocks across the book in one query. These are the extraction spine — highest confidence because the book author explicitly encoded them as transferable patterns.

**NLM Query (single call, broad):**
```
List every "Apply This" section, box, callout, or checklist in this book.
For each one, return:
  - Chapter number and title
  - The section heading or label
  - The full text of the Apply This block (verbatim if short, paraphrased if long)
  - The concept_kind: one of [decision_rule, architectural_principle, mechanism, discipline_contract, compounding_loop, anti_pattern_guard]

Format as a numbered list. If a chapter has no Apply This section, say "Chapter N: none".
```

**Expected output:** `R2-raw/R2.0_apply_this_master.md`
Contains: one entry per Apply This spec with chapter attribution, verbatim text, and concept_kind tag.

---

## R2 Standard — 6 NLM Queries Per Chapter

Run for EACH chapter (N chapters × 6 queries). Output goes to `R2-raw/Ch{{NN}}_extraction.md`.

### Q1 — Decision Rules
```
In Chapter {{N}} ("{{title}}"), what decisions does the author instruct the reader to make?
List each decision rule as:
  - Trigger: [when to apply this rule]
  - Action: [what to do]
  - Rationale: [why — if stated]

Focus on explicit "when X, do Y" patterns. Do not infer. If none stated clearly, say "none found."
```

### Q2 — Mechanisms and Processes
```
In Chapter {{N}} ("{{title}}"), what mechanisms, processes, or workflows does the author describe?
For each:
  - Name: [the mechanism name or label]
  - Steps: [ordered sequence if present]
  - Inputs: [what it consumes — if stated]
  - Outputs: [what it produces — if stated]
  - Stopping condition: [when it terminates — if stated]

If inputs/outputs/stopping condition are not stated, return null for those fields.
```

### Q3 — Architectural Principles
```
In Chapter {{N}} ("{{title}}"), what architectural or design principles does the author state or demonstrate?
For each principle:
  - Statement: [the principle in one sentence]
  - Evidence: [how the author supports it — example, case, argument]
  - Scope: [where this principle applies — system level, component level, process level, etc.]
```

### Q4 — Anti-Patterns and Failure Modes
```
In Chapter {{N}} ("{{title}}"), what anti-patterns, failure modes, traps, or warnings does the author describe?
For each:
  - Name or label: [if given]
  - Symptom: [how to recognize it]
  - Cause: [why it happens]
  - Remedy: [what to do instead — if stated]
```

### Q5 — Compounding Loops and Feedback Cycles
```
In Chapter {{N}} ("{{title}}"), does the author describe any feedback loops, compounding effects, or virtuous/vicious cycles?
For each:
  - Name: [if given]
  - Trigger: [what starts the loop]
  - Reinforcing mechanism: [what amplifies it]
  - Break condition: [what can interrupt it — if stated]
  - Direction: [virtuous / vicious / context-dependent]
```

### Q6 — Discipline Contracts and Commitments
```
In Chapter {{N}} ("{{title}}"), what ongoing disciplines, habits, rituals, or non-negotiable commitments does the author prescribe?
For each discipline:
  - Name: [if given]
  - Frequency / cadence: [daily, weekly, per-project, etc.]
  - Inputs required: [what you need to do it]
  - Non-compliance consequence: [what breaks if you skip it — if stated]
```

---

## R2-deep — 3 Extra Queries Per Chapter (--deep-extract only)

Additional depth queries. Run AFTER R2 standard 6 queries, same chapter context.
Cost: ~3× extra NLM calls per chapter. For a 17-chapter book: +51 calls total.

### Q7 — Analogical Reasoning
```
In Chapter {{N}} ("{{title}}"), does the author draw analogies to other fields, domains, or systems?
For each analogy:
  - Source domain: [what field the analogy comes from]
  - Target concept: [what in this book it illuminates]
  - The analogy: [how they map]
  - Limits: [where the analogy breaks — if stated]
```

### Q8 — Failure Mode Depth
```
In Chapter {{N}} ("{{title}}"), go deeper on failure modes: what second-order failures does the author describe — failures that arise from applying the book's own advice incorrectly?
For each second-order failure:
  - Misapplication: [what incorrect application triggers it]
  - Symptom: [how to recognize the resulting failure]
  - Correction: [how to apply the advice correctly]
```

### Q9 — Cross-Domain Pattern Matching
```
In Chapter {{N}} ("{{title}}"), what patterns or concepts appear that also exist in [systems engineering / software architecture / military operations / economic theory]?
For each cross-domain match:
  - Concept in book: [as named by the author]
  - Analogous concept in other field: [name + field]
  - Mapping quality: [strong / partial / metaphorical]
  - Implication for skill design: [what this suggests about how to implement the skill]
```

---

## R2.1 — Derivation Query (Null-Discipline)

**Purpose:** For all concepts identified in Q1-Q6 that returned null for `inputs`, `outputs`, or `stopping_conditions` — attempt one final derivation pass using book context.

**Run once per chapter, AFTER all 6 standard queries are merged.**

```
For the following concepts from Chapter {{N}}, the inputs / outputs / stopping conditions were not explicitly stated.
Based only on the surrounding context in this chapter, what can be inferred for each?

Concepts with nulls:
{{list from Q1-Q6 merge where field = null}}

For each:
  - Concept name:
  - Inferred inputs: [or null if cannot determine]
  - Inferred outputs: [or null if cannot determine]
  - Inferred stopping condition: [or null if cannot determine]
  - Confidence: [high / medium / low]
  - Evidence: [which sentence or paragraph supports the inference]

IMPORTANT: If you cannot determine a value with medium or high confidence, return null.
Do not invent values that are not supported by the text.
```

**Output:** Appended to `R2-raw/Ch{{NN}}_extraction.md` as section `## R2.1 Derivations`
Nulls at this stage surface to `R5-Ambiguity-Ledger.md` as Section C (deferred with sane defaults).

---

## R2 Merge — Extraction Manifest Assembly

After all per-chapter queries complete, `/btc-extract` merges into `R2-Extraction-Manifest.md`:

```
MERGE STRUCTURE:
  ## Apply This Specs (from R2.0)
    — highest confidence; sorted by concept_kind
  ## Per-Chapter Prose Specs (from Q1-Q6)
    — medium confidence; one section per chapter
  ## Derivations (from R2.1)
    — low-medium confidence; flagged for R5 review
  ## Null-Field Inventory
    — all remaining nulls; surfaced at R5

DEDUPLICATION RULE:
  If an Apply This spec and a Q1-Q6 prose spec describe the same concept:
    → keep Apply This as primary, mark prose as "confirmed by Q{{n}}"
    → do not create two separate skills

SUMMARY STATS (for R3 context):
  Total specs: {{N}}
    Apply This: {{N}} ({{%}})
    Prose-derived: {{N}} ({{%}})
    Derivations: {{N}} ({{%}})
  Concept kinds:
    decision_rule: {{N}}
    architectural_principle: {{N}}
    mechanism: {{N}}
    discipline_contract: {{N}}
    compounding_loop: {{N}}
    anti_pattern_guard: {{N}}
  Chapters with no Apply This: {{list}}
```
