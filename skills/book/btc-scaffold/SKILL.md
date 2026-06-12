---
name: btc-scaffold
description: "Block R6 of book-to-codebase: parallel SKILL.md generation in 4 confidence waves. CEO reviews Wave 4 sample before batch approval. Outputs library/skills/**/*.md."
---

# BTC-Scaffold — Block R6

> **Pipeline:** book-to-codebase Block R6
> **Purpose:** Generate all SKILL.md files using resolved specs. Fan-out parallel subagents per domain or per skill (for large libraries). 4 confidence waves — CEO reviews Wave 4 sample.
> **Parallel:** YES — N subagents (one per domain or per skill batch)
> **Standalone:** `/btc-scaffold <book_output_dir> [--deep-scaffold]`

## Prerequisites
- R4-Architecture.md (skill list, domain map, DAG)
- R5-Ambiguity-Ledger.md (all resolved fields and defaults)
- R5.5-Delta-Report.md (if --deep-scaffold — Cat A skills → reference wrapper only)
- R3-Charter.md (domain_prefix, deployment_path)

## Steps

### 1. Prepare Skill Queue
From R4-Architecture.md: build ordered skill list with assigned concept_kind and domain.
Apply R5 Section A+B+C resolutions: fill in all fields.
Apply R5.5 Cat A skills: mark as "reference wrapper" (no content generation — just pointer to existing KN-Stack skill).

### 2. Assign Confidence Waves
- **Wave 1:** Skills from Apply This specs with all fields populated (high confidence)
- **Wave 2:** Skills from Q1-Q6 prose specs with all fields populated
- **Wave 3:** Skills from R2.1 derivations with medium+ confidence
- **Wave 4:** Skills using R5 Section C sane defaults (CEO review required)

### 3. Fan-Out Generation (Waves 1-3 first)
Fan-out subagents to generate SKILL.md for each skill:
- Each subagent: reads spec from manifest + R5 resolutions + template from `../book-to-codebase/references/skill-md-template.md`
- Selects template matching concept_kind
- Fills all fields; uses `[unspecified — ...]` fallback for remaining nulls
- Writes to: `library/skills/{{domain}}/{{skill}}/SKILL.md`

If `--deep-scaffold`: each subagent additionally invokes `/research --deep "{{skill_topic}}"` and appends findings to SKILL.md `## Notes` section.

### 4. CEO Sample Review (before Wave 4)
After Waves 1-3 complete, present sample:
```
═══ R6: WAVES 1-3 COMPLETE — WAVE 4 SAMPLE REVIEW ═══
Generated: {{N}} skills (Waves 1-3) in {{N}} domains

Sample (5 skills — one per concept_kind):
  [show each skill's name + description + first 10 lines]

Wave 4 skills pending ({{N}} skills using sane defaults):
  {{list skill names + which field used default}}

CEO:
(1) ✅ Approve sample + proceed with Wave 4
(2) ✏️ Adjust template for [skill]: [change]
(3) ⏸️ Pause before Wave 4
```

### 5. Generate Wave 4
After CEO approval: generate Wave 4 skills.
Mark each Wave 4 skill in `R6-Skill-Registry.md` with `wave: 4 (sane-default)` flag for R8 V2 attention.

### 6. Write Skill Registry
`R6-Skill-Registry.md`:
```
# Skill Registry — {{slug}}
Generated: {{date}}

| # | Skill | Domain | concept_kind | Wave | File path | Source spec |
|---|-------|--------|-------------|------|-----------|-------------|
...

Total: {{N}} skills across {{M}} domains
Wave 1: {{N}} | Wave 2: {{N}} | Wave 3: {{N}} | Wave 4: {{N}}
Reference wrappers (Cat A overlap): {{N}}
```

## Output
- `library/skills/{{domain}}/{{skill}}/SKILL.md` (all skills)
- `R6-Skill-Registry.md`

## CEO Checkpoint (final)
```
═══ R6 COMPLETE: BTC-Scaffold ═══
Skills generated: {{N}} (Wave 1: {{N}}, W2: {{N}}, W3: {{N}}, W4: {{N}})
Reference wrappers: {{N}} (Cat A overlaps → no content)
Output: {{btc_output_dir}}/library/skills/

CEO:
(1) ✅ Approve → R7 (btc-wire)
(2) 🔄 Regenerate skill [name] with [adjustment]
(3) ⏸️ Pause
```
