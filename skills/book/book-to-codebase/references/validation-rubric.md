# Validation Rubric — book-to-codebase R8

> Used by `/btc-validate` (Block R8). Four validation layers: V1 static → V2 semantic → V3 DAG → V4 e2e.
> V1-V3 always run. V4 only with `--deep-scaffold` or CEO explicit request.

---

## V1 — Static Validation (always runs)

Checks structure and completeness without semantic judgment. Fast — no NLM queries.

### V1.1: Frontmatter completeness
For each SKILL.md in `library/skills/`:
- [ ] `name` field present and matches filename
- [ ] `description` field present, ≤100 chars, no emojis
- [ ] Description is actionable (contains a verb: "applies", "decides", "generates", "guards", etc.)

### V1.2: Required sections present
For each SKILL.md, check that required sections exist per template:
- [ ] All concept_kind templates: heading structure matches template (at least 70% of required sections)
- [ ] No `{{double braces}}` remaining (unfilled template fields)
- [ ] Integration section present (even if minimal)

### V1.3: Null discipline
- [ ] No invented values: fields that were null in R2-Extraction-Manifest should use `[unspecified — ...]` fallback, not fabricated content
- [ ] R5 Section C defaults are correctly applied (compare R5-Ambiguity-Ledger.md vs SKILL.md content)

### V1.4: Naming conventions
- [ ] All skill names: kebab-case, domain-prefixed per R4 taxonomy
- [ ] No name collisions within library
- [ ] Cat A overlap skills: reference wrapper format correct (not duplicate content)

### V1.5: Infrastructure files
- [ ] `library/setup.sh` exists and is executable
- [ ] `library/CLAUDE.md` exists
- [ ] `library/ARCHITECTURE.md` exists
- [ ] `library/ARCHITECTURE.md` references all domains from R4-Architecture.md

**V1 Pass threshold:** 0 V1.1 failures, 0 unfilled template fields, ≤5 minor V1.2-V1.4 issues

---

## V2 — Semantic Validation (always runs, 1 NLM query per domain)

Checks whether the extracted skills accurately represent the book's intent.
Uses the book's NLM notebook (from R1 ingest).

### V2 Query Template (per domain)
```
This skill library was extracted from the book in this notebook.
The following skills were generated for the domain "{{domain_name}}":

{{list skill names and 1-sentence descriptions}}

For each skill:
1. Is this skill accurately grounded in the book? (yes / partially / no)
2. If partially or no: what does the book actually say about this topic?
3. Are there any important concepts from this domain in the book that are MISSING from this skill list?

Be specific. Quote chapter and section if possible.
```

### V2 Scoring per skill
- **Green:** "yes" — accurately grounded
- **Yellow:** "partially" — needs adjustment
- **Red:** "no" — misrepresents or fabricates content

### V2 Pass threshold
- Green ≥ 80% of skills
- No Red skills (all must be fixed or removed before R9)
- Yellow skills: CEO decides keep/fix/drop at R8 checkpoint

---

## V3 — DAG Validation (always runs)

Checks the skill dependency graph from R4-Architecture.md for consistency.

### V3.1: Edge resolution
- [ ] Every `depends_on` edge resolves to an existing skill in the library
- [ ] Every `guards` edge points to an existing skill
- [ ] Every `informs` edge is documented in both the source and target skill's Integration section

### V3.2: Cycle detection
- [ ] No cycles except declared `compounding_loop` skills
- [ ] For each cycle detected: confirm it maps to a `compounding_loop` skill; if not, flag as unintended cycle

### V3.3: Orphan detection
- [ ] Every skill is reachable from at least one entry point (called-by or scheduled-by)
- [ ] Skills with no callers: flag as "standalone" in R6-Skill-Registry.md; not a failure but requires annotation

### V3.4: DAG matches R4 Architecture
- [ ] Skills added or removed during R5/R6 are reflected in R4-Architecture.md DAG
- [ ] No skills in `library/skills/` that are missing from `R6-Skill-Registry.md`

**V3 Pass threshold:** 0 unresolved edges, 0 unintended cycles

---

## V4 — End-to-End Validation (--deep-scaffold or CEO request only)

Functional test: can Claude actually invoke and follow each skill?
Cost: 1 short Claude conversation per skill (haiku-level is sufficient).

### V4 Method
For each skill in the library, invoke it with a minimal synthetic input:
```
/{{skill-name}} <<minimal test input>>
```
Evaluate:
- [ ] Skill invoked without error
- [ ] Output structure matches template (expected sections present)
- [ ] No hallucinated content (no invented book quotes or false citations)
- [ ] Integration edges work: if skill calls another skill, that invocation succeeds

### V4 Sampling strategy
- Run ALL skills if skill count ≤ 15
- If skill count > 15: run all Wave 1 skills + 50% random sample of Wave 2-3 + all Wave 4 skills
- Always run all skills with V2 Red or Yellow rating

**V4 Pass threshold:** 0 invocation errors, ≤10% output structure failures (fixable in situ)

---

## R8 Validation Report Format

`R8-Validation-Report.md`:

```
## V1 Static Results
  Pass: {{N}} / {{total}} skills
  Failures: {{list}}
  Infrastructure: {{PASS | FAIL — what's missing}}

## V2 Semantic Results
  Green: {{N}} ({{%}})
  Yellow: {{N}} ({{%}}) — requires CEO decision
  Red: {{N}} ({{%}}) — must fix before R9
  Missing concepts flagged by NLM: {{list}}

## V3 DAG Results
  Unresolved edges: {{N}}
  Unintended cycles: {{N}}
  Orphan skills: {{N}}
  Overall: {{PASS | FAIL}}

## V4 E2E Results (if run)
  Tested: {{N}} / {{total}} skills
  Invocation errors: {{N}}
  Structure failures: {{N}}
  Overall: {{PASS | FAIL}}

## Remediation Required Before R9
{{numbered list of items that must be fixed}}

## CEO Waiver Options
V4 can be waived by CEO. Yellow skills can be deferred to post-R9 cleanup.
```
