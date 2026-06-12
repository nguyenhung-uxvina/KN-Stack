---
name: journal
description: >-
  Record a design decision immediately when it is made — captures context,
  options considered, rationale, trade-offs accepted, reversibility, and a
  review trigger. Saves to the project's Phase folder as a structured Decision
  record. Use any time a design or engineering decision is made during a Helix
  phase. Triggers on: "journal", "record decision", "design decision", "ghi
  quyết định thiết kế", "log decision", "decision journal", "quyết định phase".
---

Record a design decision with context, rationale, and alternatives considered.

Usage: /journal [decision_summary] OR provide details interactively.

1. If $ARGUMENTS provided, use as decision summary; otherwise ask:
   - What design decision was just made?
   - What project does it belong to?
   - What phase? (Phase 1-4)

2. Generate the journal entry:

```
# DESIGN DECISION — {{summary}}
**Date:** {{today}}  |  **Project:** {{project}}  |  **Phase:** {{phase}}
**Decision #:** {{sequential within project}}

---

## CONTEXT
{{What triggered this decision? What problem were we solving?}}

## OPTIONS CONSIDERED
| # | Option | Evaluated? |
|---|--------|-----------|
| A | {{chosen}} | Yes — SELECTED |
| B | {{alternative}} | Yes — rejected because: |
| C | {{alternative}} | No — why not evaluated: |

## DECISION
**Chose:** {{option A}}
**Rationale:** {{1-2 sentences — WHY this option, not just WHAT}}

## TRADE-OFFS ACCEPTED
- {{what we gave up by choosing this option}}
- {{constraint this creates for future decisions}}

## REVERSIBILITY
- [ ] Easily reversible (two-way door)
- [ ] Difficult to reverse (one-way door)
- **Cost to reverse:** {{time/money estimate}}

## DEPENDENCIES
- **This decision enables:** {{what can now proceed}}
- **This decision blocks:** {{what is now constrained}}

## REVIEW TRIGGER
**Revisit this decision if:** {{condition that would invalidate the rationale}}
```

3. Save to:
   `1_Projects/{{project}}/Phase{{N}}-*/{{PROJECT_NAME}}_Decision_{{NNN}}_v1.0.md`

RULES:
- Record decisions WHEN THEY ARE MADE — not after the fact
- "Why not" is as valuable as "why" — document rejected alternatives
- One-way doors deserve more documentation than two-way doors
- COD: Core (CEO decides) with Offload (AI records and structures)
- Keep entries short — 1 page maximum. This is a log, not an essay.
