---
name: btc-suggest
description: "Standalone pre-pipeline: ingest book + propose 3 architecture archetypes (α minimal / β standard / γ anchor-based). CEO selects before committing to full book-to-codebase run. No pipeline commitment."
---

# BTC-Suggest — Standalone Archetype Proposals (R3.0)

> **Pipeline:** book-to-codebase Block R3.0 (optional — activated by `--suggest` flag or standalone)
> **Purpose:** Before committing to the full BTC pipeline, present 3 architecture archetypes based on a quick R1 ingest + extraction density analysis. CEO selects archetype (or opts out). No downstream commitment.
> **Standalone:** `/btc-suggest <book_output_dir>`
> **In pipeline:** activated by `--suggest` flag; runs before R3

## What This Is Not
- Not a full R2 extraction (no per-chapter NLM queries)
- Not a placement decision (that's CEO Core in R3)
- Not a commitment to run the full pipeline

## Steps

### 1. Quick Ingest (abbreviated R1)
- Detect canonical phase, count chapters
- Scan for Apply This density (regex quick-count)
- Check `--from-pipeline` artifacts availability
- Check if NLM notebook already exists for this book

### 2. Sample Extraction (3 chapters max)
Run R2.0 Apply This pre-pass against first + middle + last chapter (3 NLM queries total).
Goal: estimate total Apply This spec count and concept_kind distribution without full R2.

### 3. Propose 3 Archetypes

**Archetype α — Minimal**
- Scope: 1-5 skills, no domain taxonomy, no setup.sh
- Format: flat SKILL.md files, delivered as a single folder
- Best when: Apply This count ≤ 5, OR all specs are `architectural_principle` / `decision_rule`
- Placement: Type A (pipeline enhancement) or Type D (Galaxy notes only)
- Estimated skill count: {{N}} (from sample × chapter scaling)
- Estimated cost: low (R6 only, no infrastructure)

**Archetype β — Standard**
- Scope: 5-15 skills across 1-3 domains, with setup.sh and CLAUDE.md
- Format: domain-prefixed skills + junction installer
- Best when: Apply This count 6-20, concept_kinds diverse, single cohesive domain
- Placement: Type B (new named domain in KN-Stack)
- Estimated skill count: {{N}}
- Estimated cost: medium

**Archetype γ — Anchor-Based**
- Scope: 10-30 skills organized around anchor concepts from book
- Format: anchor-organized taxonomy + full infrastructure (Type C standalone repo)
- Best when: book has explicit process model (phases, stations, gates), OR Apply This count > 20, OR compound cross-domain learning
- Placement: Type C (standalone repo with own setup.sh)
- Recommended when `--from-pipeline` (book structure already validated)
- Estimated skill count: {{N}}
- Estimated cost: high

### 4. Present to CEO

```
═══ BTC-SUGGEST — ARCHETYPE PROPOSALS ═══
Book: {{slug}} ({{N}} chapters, ~{{M}} Apply This specs estimated)
Source: {{canonical phase}}
Fast-path: {{N}}/4 artifacts available

ARCHETYPE α — Minimal
  Skills: ~{{N}} | Placement: {{A|D}} | Cost: low
  Best for: {{reason based on extraction density}}

ARCHETYPE β — Standard
  Skills: ~{{N}} | Placement: B | Cost: medium
  Best for: {{reason}}

ARCHETYPE γ — Anchor-Based
  Skills: ~{{N}} | Placement: C | Cost: high
  Best for: {{reason}}
  {{★ Recommended | Not recommended for this book because: ...}}

CEO:
(1) Select α → save as R3.0 seed; continue with /book-to-codebase --from-pipeline
(2) Select β → save as R3.0 seed; continue with /book-to-codebase --from-pipeline
(3) Select γ → save as R3.0 seed; continue with /book-to-codebase --from-pipeline
(4) None of the above → proceed to R3 blank-slate
(5) Stop here — no pipeline commitment
═══════════════════════════════════════════
```

### 5. Write R3.0-Archetypes.md (regardless of CEO choice)

```markdown
# Archetype Proposals — {{slug}}
Generated: {{date}}
Book: {{N}} chapters, ~{{M}} Apply This (estimated from 3-chapter sample)

## Archetype α — Minimal
[proposal details]

## Archetype β — Standard
[proposal details]

## Archetype γ — Anchor-Based
[proposal details]

## CEO Selection
{{α | β | γ | blank-slate | stopped — recorded from checkpoint}}
Recorded: {{date}}
```

## Output
- `R3.0-Archetypes.md`

## Integration
```
btc-suggest READS FROM:
  - Canonical chapter files (3 samples)
  - R1-Chapter-Index.md (if exists from prior R1 run)

btc-suggest WRITES TO:
  - {{btc_output_dir}}/R3.0-Archetypes.md

btc-suggest FEEDS INTO (if pipeline continues):
  - btc-charter (R3) — uses CEO selection as charter seed
```
