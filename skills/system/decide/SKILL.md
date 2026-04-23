Structured decision support for complex trade-offs and design choices.

Usage: /decide [decision_description] OR provide details interactively.

1. If $ARGUMENTS provided, use as decision description; otherwise ask:
   - What decision needs to be made?
   - What project/area does this belong to?
   - What is the deadline for this decision?
   - What constraints apply?

2. Execute the structured decision process:

```
# DECISION RECORD — {{decision_title}}
**Date:** {{today}}  |  **Project:** {{project}}  |  **Decision By:** CEO

---

## 1. DECISION STATEMENT
{{One sentence: What exactly must be decided?}}

## 2. CONTEXT
{{Why is this decision needed now? What triggered it?}}

## 3. OPTIONS

| # | Option | Pros | Cons | Cost | Risk | Reversibility |
|---|--------|------|------|------|------|---------------|
| A | | | | | | High/Med/Low |
| B | | | | | | High/Med/Low |
| C | Do nothing | | | | | |

## 4. EVALUATION CRITERIA
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| {{criterion 1}} | % | 0-4 | 0-4 | 0-4 |
| {{criterion 2}} | % | | | |
| **Weighted Total** | 100% | | | |

## 5. SECOND-ORDER EFFECTS
- If we choose A, what does that enable or block?
- If we choose B, what does that enable or block?
- What decision does this force NEXT?

## 6. REVERSIBILITY CHECK
- Can this be undone if wrong? At what cost?
- Is this a one-way door (irreversible) or two-way door (easily reversed)?
- One-way doors deserve more analysis. Two-way doors: decide fast.

## 7. RECOMMENDATION
**Option {{X}}** because: {{rationale in 1-2 sentences}}

## 8. DECISION LOG ENTRY
| Field | Value |
|-------|-------|
| Decision | |
| Chosen option | |
| Rationale | |
| Date decided | |
| Decided by | CEO |
| Review date | {{30 days from now}} |
```

3. Present analysis to user. WAIT for CEO to decide.
4. After decision, save to:
   `1_Projects/{{project}}/Phase{{N}}-*/{{PROJECT_NAME}}_Decision_{{NNN}}_v1.0.md`
   Or if organizational: `2_Areas/{{area}}/Decision_{{NNN}}_v1.0.md`

RULES:
- Always include "Do nothing" as an option — it's often underrated
- Always assess reversibility — two-way doors should be decided fast
- COD: This is Core (CEO decides) with Offload (AI structures the analysis)
- Never auto-decide — present and WAIT
- Link to Galaxy: "Phan doan khong the uy thac cho AI"
