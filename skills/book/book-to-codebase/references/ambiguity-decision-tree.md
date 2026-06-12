# Ambiguity Decision Tree — book-to-codebase R5

> Used by `/btc-resolve` (Block R5). Governs how ambiguities in the extraction manifest are handled.
> Goal: resolve as many as possible automatically; surface ≤30 questions to CEO; defer the rest with sane defaults.

---

## R5 Ledger Structure

`R5-Ambiguity-Ledger.md` has three sections:

```
## Section A — Auto-Resolved
Items resolved without CEO input (rules below).

## Section B — CEO Questions (max 30)
Items requiring CEO judgment. Presented as numbered questions.

## Section C — Deferred (sane defaults applied)
Items too complex or low-priority to resolve now. Default applied; flagged for R9 DMIR.
```

---

## Auto-Resolution Rules (Section A)

Apply these in order. If a rule fires, add to Section A and do NOT ask CEO.

### AR-1: Null inputs/outputs with high-confidence inference
**Condition:** R2.1 derivation returned a value with confidence = "high"
**Action:** Use the derived value; note source evidence in ledger
**Example:** "Inputs: [the current state artifact]" inferred from "this step takes the previous output"

### AR-2: Concept_kind ambiguity between decision_rule and anti_pattern_guard
**Condition:** A spec looks like both (it states a condition AND warns against doing the opposite)
**Action:** Classify as decision_rule; add the warning as its "Common misapplication" field
**Rationale:** Decision rule is the primary operational content; guard is secondary

### AR-3: Duplicate spec (same concept, two chapters)
**Condition:** Two specs from different chapters describe the same concept with ≥80% overlap
**Action:** Keep the spec from the chapter with higher Apply This confidence; mark the other as "confirmed by Ch{{N}}"
**Do not ask CEO** unless the two versions contradict each other

### AR-4: Mechanism with no stopping condition
**Condition:** R2.1 returned null for stopping_condition; concept_kind = mechanism
**Action:** Apply default stopping condition: "stop when output artifact is stable and reviewed"
**Flag in ledger** but do not escalate to CEO

### AR-5: Glossary term naming conflict
**Condition:** A proposed skill name conflicts with an existing KN-Stack skill name (different concept)
**Action:** Append book slug as suffix: `{{skill-name}}-{{book-slug}}` (e.g., `review-gstack`)
**Flag in ledger** for CEO awareness; do not block

### AR-6: domain_prefix absent from R4 for a skill
**Condition:** A spec has a clear concept_kind but no domain was assigned in R4 taxonomy
**Action:** Assign to domain "general" temporarily; flag for CEO in Section B

### AR-7: concept_kind = compounding_loop with no break condition
**Condition:** Loop spec has break_condition = null after R2.1
**Action:** Apply default: "break condition not specified; monitor for inversion symptoms"
**Do not escalate** — this is a known acceptable null in loop specs

---

## CEO Question Templates (Section B)

Present as numbered questions. Cap at 30. If overflow: move lowest-priority to Section C.

**Priority order for Section B escalation:**
1. Placement conflicts (R3-related ambiguities that arrived late)
2. Naming conflicts that AR-5 couldn't resolve
3. Contradictory specs (same concept, different instructions in different chapters)
4. Null fields that are critical for R6 scaffolding (inputs to a core mechanism)
5. Domain taxonomy edge cases (should concept X go in domain A or domain B?)

### Question format:
```
Q{{N}}: [CATEGORY: naming | null-field | contradiction | taxonomy | other]
  Context: [1-2 sentences describing the ambiguity]
  Option A: [first resolution]
  Option B: [second resolution]
  Default if you skip: [what R6 will use if CEO does not answer]
  Impact: [what changes downstream if the answer is A vs B]
```

### CEO answer format (for ledger):
```
Q{{N}} → CEO answer: [A / B / other]
  Recorded: {{date}}
  Applied in: R6 Wave {{N}}
```

---

## Sane Defaults (Section C)

When a question cannot be resolved by AR rules AND CEO capacity is exceeded (>30 questions):

| Ambiguity Type | Sane Default |
|---|---|
| Null inputs | "[requires context — see book Ch{{N}}]" |
| Null outputs | "[produces structured output — form TBD]" |
| Null stopping_condition | "stop when output is stable and reviewed" |
| concept_kind unclear | classify as `mechanism` (most general) |
| Domain assignment unclear | assign to `general` domain |
| Contradictory specs | use the Apply This version; note contradiction |
| Skill name collision | append `-v2` suffix |
| Integration edges unknown | leave Integration section blank; note "DAG TBD" |

**All Section C items are surfaced in R9 DMIR — Reflect section** as "deferred ambiguities requiring book revision or CEO decision."

---

## Overflow Protocol

If total items for Section B exceed 30:
1. Sort all Section B candidates by impact score (H/M/L)
2. Take top 30 by impact
3. Move remainder to Section C with sane defaults
4. Summarize overflow in ledger: "{{N}} questions deferred to Section C — see R9 DMIR"

Impact scoring:
- H: null critical field in mechanism or decision_rule (blocks R6 scaffolding)
- M: naming conflict or taxonomy edge case (degrades quality but doesn't block)
- L: missing rationale, weak evidence, non-critical metadata
