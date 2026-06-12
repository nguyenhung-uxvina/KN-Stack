---
name: aigate
description: >-
  Validate any AI-generated deliverable before it enters a production workflow
  — 7-check FORGE-F gate covering traceability, internal consistency,
  completeness, hallucination, actionability, COD boundary, and downstream
  impact. Issues PROCEED / REVISE / BLOCK decision. Distinct from /qc which
  handles defense-domain safety; aigate handles structural quality of any AI
  output. Triggers on: "aigate", "AI gate", "validate deliverable", "kiểm tra
  deliverable", "FORGE-F gate", "check AI output", "hallucination check",
  "deliverable gate".
---

Validate AI-generated deliverables before they enter production workflows — the FORGE-F deployment gate.

Unlike /qc (defense domain checks), /aigate validates structural quality, consistency, and fitness-for-use of ANY AI output: designs, analyses, documents, code, recommendations.

Usage: /aigate [deliverable_type] OR provide details interactively.

1. Collect inputs:
   - If $ARGUMENTS provided, use as deliverable type; otherwise ask:
     a) What AI output are you validating? (design doc / analysis / code / recommendation / BOM / requirements / other)
     b) What project does it belong to? (read from Status.md)
     c) What will this output be USED for? (decision-making / prototype build / gate review / customer delivery / internal reference)
   - Ask user to provide or point to the content

2. Read the deliverable and relevant project context:
   - `1_Projects/{{project}}/Status.md` — current phase, constraints
   - The AI-generated deliverable itself
   - Upstream artifacts it should be consistent with (requirements, architecture, etc.)

3. Run the 7-check FORGE-F Validation Gate:

```
# AI VALIDATION GATE — FORGE-F
**Date:** {{today}} | **Project:** {{project}} | **Deliverable:** {{type}}
**Intended use:** {{what this output will be used for}}

---

## GATE CHECKS

### 1. TRACEABILITY (Does it connect to upstream artifacts?)
- [ ] References correct requirements doc version?
- [ ] Traces to correct phase deliverables?
- [ ] No orphan claims (assertions without source)?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 2. INTERNAL CONSISTENCY (Does it contradict itself?)
- [ ] Numbers used consistently throughout?
- [ ] Units correct and consistent (metric only)?
- [ ] No contradictory statements between sections?
- [ ] Calculations spot-checked (pick 2-3, verify)?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 3. COMPLETENESS (Does it cover what it claims to cover?)
- [ ] All sections populated (no TBD placeholders passed as done)?
- [ ] Scope matches what was requested?
- [ ] Edge cases addressed (or explicitly deferred)?
- [ ] Missing items flagged as known gaps?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 4. HALLUCINATION CHECK (Are facts verifiable?)
- [ ] Component part numbers exist? (spot-check 2-3)
- [ ] Standards referenced correctly? (MIL-STD, TCVN numbers)
- [ ] Supplier names and capabilities accurate?
- [ ] Performance claims physically plausible?
- [ ] No "confident but wrong" patterns detected?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 5. ACTIONABILITY (Can someone ACT on this output?)
- [ ] Clear next steps or decisions identified?
- [ ] Owner/responsibility assigned where needed?
- [ ] Deadlines or priorities stated?
- [ ] Sufficient detail for the intended audience?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 6. COD BOUNDARY (Does it stay in Offload territory?)
- [ ] No design DECISIONS made (only options presented)?
- [ ] Judgment calls flagged for CEO review?
- [ ] Does not auto-commit to irreversible choices?
- [ ] Acknowledges uncertainty where it exists?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

### 7. DOWNSTREAM IMPACT (What breaks if this is wrong?)
- [ ] Blast radius identified (what depends on this output)?
- [ ] Reversibility assessed (can we undo if wrong)?
- [ ] Cost of error estimated (time, money, safety)?
- [ ] Appropriate confidence level stated?
- **Status:** PASS / FLAG / FAIL
- **Evidence:** {{specific findings}}

---

## GATE DECISION

| Check | Status |
|-------|--------|
| 1. Traceability | |
| 2. Internal Consistency | |
| 3. Completeness | |
| 4. Hallucination | |
| 5. Actionability | |
| 6. COD Boundary | |
| 7. Downstream Impact | |

### Decision: {{PROCEED / REVISE / BLOCK}}

- **PROCEED:** All PASS or minor FLAGs only. Safe to use.
- **REVISE:** 1+ FLAGs need attention. List specific fixes, re-run gate after.
- **BLOCK:** 1+ FAILs. Do NOT use this output. List what must change.

---

## REQUIRED FIXES (if REVISE or BLOCK)
| # | Check | Issue | Required Fix | Priority |
|---|-------|-------|-------------|----------|
{{specific issues and how to fix them}}

---

## CONFIDENCE ASSESSMENT
- **AI confidence in this output:** {{HIGH / MEDIUM / LOW}}
- **Verification method:** {{how CEO can independently verify key claims}}
- **Recommended human review depth:**
  - HIGH confidence: Skim check (5 min)
  - MEDIUM confidence: Focused review on flagged sections (15 min)
  - LOW confidence: Full independent verification required (30+ min)
```

4. Present gate result. If REVISE or BLOCK:
   - Offer to fix the issues and re-run the gate
   - Track fix iterations (max 2 — if still failing after 2 fixes, escalate to CEO manual review)

RULES:
- This gate runs BEFORE the deliverable is used for decisions, not after
- Check 4 (Hallucination) is the most critical for AI outputs — always spot-check specific facts
- Check 6 (COD Boundary) prevents AI from making decisions that belong to CEO (Core tasks)
- Never pass a deliverable with FAIL in checks 4 or 6 — these are hard blocks
- If the deliverable is for a gate review (/gate1, /gate2, /gate3), apply STRICTER standards
- /qc is for defense-domain safety checks; /aigate is for structural quality of any AI output
- Both /qc and /aigate can run on the same deliverable — they check different things
- COD: This skill is itself Offload — AI validates AI, but CEO makes final accept/reject
- Track gate pass rate over time — if >30% of outputs need REVISE, the upstream prompts need improvement
- Max 2 re-run iterations per deliverable — avoid infinite revision loops
