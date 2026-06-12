---
name: book-to-codebase
description: "Orchestrator biến sách kỹ thuật publication-quality thành agentic skill library deployable. Reverse pipeline of codebase-to-book: NLM ingest → extract operational patterns → charter library identity → architect domain taxonomy → resolve ambiguity → scaffold SKILL.md files → wire infrastructure → validate → handoff. 9 block-skills (btc-ingest → btc-extract → btc-charter → btc-architect → btc-resolve → btc-scaffold → btc-wire → btc-validate → btc-handoff). Apply This specs = extraction spine. HELIX-FORGE classification (A/B/C/D). DMIR meta-layer. Flags: --from-pipeline (reuse codebase-to-book artifacts), --deep-extract, --deep-scaffold, --suggest (R3.0 archetype proposals), --lang, --from, --only. Triggers on: 'book to codebase', 'extract skills from book', 'sách thành skill library', 'turn book into skills', 'btc', 'reverse pipeline'."
---

# Book-to-Codebase — Mega-Skill Orchestrator (9-Phase Reverse Pipeline)

> **Role:** Chỉ huy trưởng (Commander) — điều phối 9 block-skills tuần tự, CEO checkpoint sau mỗi block
> **Architecture:** Modular pipeline — mỗi block = 1 skill độc lập, có thể chạy standalone
> **Inverse of:** `codebase-to-book` — reverses the direction: artifact (book) → operational system (skill library)
> **Extraction spine:** Apply This specs from book — ~72 high-confidence specs vs ~15 prose-extracted
> **Case study (gstack):** P6 canonical, 17 chapters, 17-term glossary, 8 cross-cutting patterns → ~72 Apply This specs → Type C skill library

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                        book-to-codebase (ORCHESTRATOR — 9 blocks)                        │
│                                                                                           │
│  Flags: --from-pipeline | --deep-extract | --deep-scaffold | --suggest                   │
│         --lang vi|en | --from Rn | --only Rn                                              │
│                                                                                           │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐               │
│  │ R1  │▶│ R2  │▶│ R3  │▶│ R4  │▶│ R5  │▶│ R6  │▶│ R7  │▶│ R8  │▶│ R9  │               │
│  │ING- │ │EXT- │ │CHA- │ │ARC- │ │RES- │ │SCA- │ │WIRE │ │VAL- │ │HAND-│               │
│  │EST  │ │RACT │ │RTER │ │HITE │ │OLVE │ │FFOLD│ │     │ │IDATE│ │OFF  │               │
│  │NLM  │ │∥    │ │C    │ │C    │ │CEO  │ │∥    │ │     │ │     │ │C    │               │
│  │     │ │N×   │ │     │ │     │ │30Q  │ │4wav │ │     │ │4V   │ │DMIR │               │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘               │
│     │CEO    │CEO    │CORE   │CORE   │CEO    │CEO    │CEO    │CEO    │CORE              │
└──────────────────────────────────────────────────────────────────────────────────────────┘

Legend: ∥ = parallel Task subagents | C = CEO Core (non-delegable) | CEO = checkpoint after
        4wav = 4 confidence waves | 4V = V1 static + V2 semantic + V3 DAG + V4 e2e

Data Bus: <book_output_dir>/btc-output/              (alongside existing book output)
State:    <book_output_dir>/btc-output/_btc_state.md
```

## Sub-Skills (9 Block-Skills)

| Block | Skill Name | Parallel? | Purpose | CEO Checkpoint |
|-------|-----------|-----------|---------|----------------|
| **R1** | `/btc-ingest` | NO | NLM auth + chapter index + artifact reuse from `--from-pipeline` | Review chapter index + Apply This count |
| **R2** | `/btc-extract` | **YES** (N per chapter) | Apply This pre-pass (R2.0) + 6 NLM queries/chapter + R2.1 derivation | Review extraction quality; accept/reject specs |
| **R3** | `/btc-charter` | NO | Library identity: name, tagline, placement (A/B/C/D), CEO Core | **CEO Core — approve charter + placement** |
| **R3.0** | `/btc-suggest` *(--suggest only)* | NO | Pre-R3: 3 architecture archetype proposals; CEO selects one | **CEO Core — select archetype before R3** |
| **R4** | `/btc-architect` | NO | Domain taxonomy + skill DAG; CEO Core | **CEO Core — approve taxonomy** |
| **R5** | `/btc-resolve` | NO | Ambiguity ledger: auto-resolve / 30-Q CEO / deferred-default | Review open items; answer up to 30 questions |
| **R5.5** | *(--deep-scaffold)* | NO | KN-Stack overlap pre-scan; delta report Cat A/B/C/D | Review delta — Cat D warns of gaps |
| **R6** | `/btc-scaffold` | **YES** (N per skill) | Parallel SKILL.md gen; 4 confidence waves; glossary lock | Review samples (Wave 4); approve batch |
| **R7** | `/btc-wire` | NO | setup.sh, CLAUDE.md, ARCHITECTURE.md, ICD stubs, hooks | Review infrastructure; approve deploy |
| **R8** | `/btc-validate` | NO | V1 static + V2 semantic + V3 DAG + V4 e2e (`--deep`) | Review validation report; green-light or remediate |
| **R9** | `/btc-handoff` | NO | DMIR retrospective + Galaxy candidates + usage commitment | **CEO Core — commit to activation cadence** |

## How to Use

### Full pipeline (default — English output, fresh book)
```
/book-to-codebase <book_output_dir>
```

### Reuse codebase-to-book artifacts (60% work already done)
```
/book-to-codebase <book_output_dir> --from-pipeline
```

### With archetype suggestions before charter
```
/book-to-codebase <book_output_dir> --suggest
```

### Deep extraction (3 extra NLM queries per chapter — cost-intensive)
```
/book-to-codebase <book_output_dir> --deep-extract
```

### Deep scaffold (KN-Stack overlap scan + /research per skill)
```
/book-to-codebase <book_output_dir> --deep-scaffold
```

### Resume / Single Block
```
/book-to-codebase <book_output_dir> --from R4
/btc-architect <book-slug>
```

### Vietnamese output
```
/book-to-codebase <book_output_dir> --lang vi
```

### Suggest archetypes only (standalone — no pipeline commitment)
```
/btc-suggest <book_output_dir>
```

## Orchestrator Workflow

### Step 1: Parse Arguments

```
BOOK_OUTPUT_DIR: {{first argument — path to book-output directory}}

FLAGS:
  --from-pipeline        → R1 reuses Phase2-Positioning.md, Phase3-Outline.md,
                           P1_Synthesis.md from codebase-to-book output
                           R3 checkpoint becomes "approve" not "fill-in" (~60% less work)
  --deep-extract         → R2 adds 3 deep NLM queries per chapter (R2-deep)
                           Scales as: chapters × 3 extra calls (~15× base R2 cost)
  --deep-scaffold        → R5.5 KN-Stack overlap pre-scan runs before R6
                           R6 adds /research --deep per skill (~5-10× base R6 cost)
  --suggest              → R3.0 btc-suggest runs BEFORE R3; CEO selects archetype
                           Adds ~1 turn; prevents R3 rework from wrong archetype
  --lang vi|en           → Output language (default 'en' — SKILL.md is code)
  --from Rn              → Resume from block Rn (R1-R9)
  --only Rn              → Run single block Rn only
```

### Step 1.5: Resolve Book Output Directory

```
Book slug = basename(book_output_dir) lowercase + kebab-case
  e.g., D:\gstack\book-output\gstack → "gstack"
  e.g., D:\Workshop_X\3_Resources\Books\kn-stack → "kn-stack"

BTC output dir = <book_output_dir>/btc-output/
  e.g., D:\gstack\book-output\gstack\btc-output\

Detect canonical phase:
  Prefer Phase6-Revised/ chapters (canonical)
  Fall back to Phase4-Chapters/ if Phase6 absent
  Warn if P4-only (known-issue risk)
```

### Step 1.6: Input Validation & CEO Context Enrichment

**MANDATORY before any block execution.**

#### 1.6a: Verify Book Output Accessible

```
BOOK OUTPUT CHECK — {{book_output_dir}}
  □ Path exists?
  □ Contains Phase* directories?
  □ Phase2-Positioning.md exists? (for --from-pipeline)
  □ Phase3-Outline.md exists? (for --from-pipeline)
  □ Phase6-Revised/ or Phase4-Chapters/ contains chapter files?
  □ Chapter count: {{N}} chapters detected
  □ Apply This sections found in any chapter? (quick scan — not exhaustive)

RESULT: [GO / NO-GO — what's missing?]
```

#### 1.6b: NLM Auth Pre-Check

```
NLM AUTH — Verifying notebooklm-mcp session...
  → Call mcp__notebooklm-mcp__refresh_auth
  → If fail: HALT with instruction
     "Run `nlm login` in terminal, then /book-to-codebase ... --from R1"
  → If ok: proceed
```

#### 1.6c: Present Scope to CEO

```
═══ BOOK-TO-CODEBASE — SCOPE PREVIEW ═══

Book output: {{book_output_dir}}
Slug: {{slug}}
BTC output: {{btc_output_dir}}

Chapters detected: {{N}} ({{canonical_phase}})
Apply This sections found: {{count_quick_scan}} (pre-scan estimate)
Glossary terms: {{N}} terms in Phase2-Positioning.md

Pipeline: {{9 blocks | --from Rn: starting at Rn}}
Language: {{en | vi}}
--from-pipeline: {{YES (reusing Phase2+Phase3+P1_Synthesis) | NO (fresh extraction)}}
--suggest: {{YES (R3.0 archetype proposals first) | NO}}
--deep-extract: {{YES (~{{N×3}} extra NLM queries) | NO}}
--deep-scaffold: {{YES (KN-Stack overlap scan + /research per skill) | NO}}

Estimated deliverables:
  - 1 extraction manifest (R2) with ~{{apply_this_estimate}} Apply This specs
  - 1 library charter (R3): name, tagline, placement (A/B/C/D)
  - 1 domain taxonomy + skill DAG (R4): {{domain_count_estimate}} domains
  - 1 resolved skill list (R5): {{skill_count_estimate}} skills
  - {{skill_count_estimate}} SKILL.md files (R6)
  - 1 infrastructure bundle (R7): setup.sh + CLAUDE.md + ARCHITECTURE.md
  - 1 validation report (R8)
  - 1 DMIR retrospective + Galaxy candidates (R9)

Estimated cost: {{rough estimate based on chapter count × flags}}
Estimated time: {{hours}} with CEO checkpoints

CEO:
(1) ▶️ Confirm và chạy R1
(2) ⚙️ Adjust flags (specify what)
(3) ⏸️ Cancel
═══════════════════════════════════════════════════
```

Wait for CEO response before proceeding.

### Step 2: Initialize Pipeline State

Create/update `{{btc_output_dir}}/_btc_state.md`:

```markdown
---
book_slug: {{slug}}
book_output_dir: {{book_output_dir}}
btc_output_dir: {{btc_output_dir}}
pipeline: book-to-codebase v1.0
started: {{today}}
updated: {{today}}
flags:
  from_pipeline: {{true|false}}
  deep_extract: {{true|false}}
  deep_scaffold: {{true|false}}
  suggest: {{true|false}}
  lang: {{en|vi}}
---

# BTC Pipeline State — {{slug}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|-------------|
| R1 | btc-ingest | PENDING | - | - | - |
| R2 | btc-extract | PENDING | - | - | - |
| R3.0 | btc-suggest (if --suggest) | SKIPPED | - | - | - |
| R3 | btc-charter | PENDING | - | - | - |
| R4 | btc-architect | PENDING | - | - | - |
| R5 | btc-resolve | PENDING | - | - | - |
| R5.5 | overlap-scan (if --deep-scaffold) | SKIPPED | - | - | - |
| R6 | btc-scaffold | PENDING | - | - | - |
| R7 | btc-wire | PENDING | - | - | - |
| R8 | btc-validate | PENDING | - | - | - |
| R9 | btc-handoff | PENDING | - | - | - |

## Block Ledger
> **Purpose:** Sole communication channel between blocks. Each block reads this section for context, then appends its summary. Enables crash recovery and context-free resume.

[Each block appends one entry below when complete — see Ledger Write Protocol]

## CEO Decisions
[populated at each checkpoint]

## Adjustments Log
[populated when CEO modifies outputs]
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ CRITICAL RULE: Execute EXACTLY ONE block per turn. After completing a block, STOP and WAIT for CEO response. DO NOT proceed to the next block until CEO explicitly approves. This is the #1 rule.**

**Architecture: Initializer + Incremental + Ledger**
- R1 (Ingest) = **Initializer** — populates ledger with chapter index + Apply This count + fast-path artifacts
- R2-R9 = **Incremental Agents** — each block reads ledger, works, appends
- `_btc_state.md` = **State Ledger** — SOLE communication channel between blocks

#### Ledger Read Protocol (BEFORE each block)

Read `_btc_state.md` → "Block Ledger" section. Reconstruct context from previous block summaries, CEO decisions, open questions. Critical for `--from` resume and new sessions.

#### Ledger Write Protocol (AFTER each block)

Append to "Block Ledger" section:
```
### {{Block ID}} — {{block name}} ({{date}})
**Key findings:** [2-3 bullet points — essential outputs]
**Decisions for downstream:** [what next block needs to know]
**Open questions:** [unresolved items for CEO or next block]
**CEO checkpoint result:** [approve / revise / pause + CEO's words]
```

#### For each block:

1. **Ledger Read:** Read `_btc_state.md` to reconstruct context
2. **Announce:** "Running Block {{X}}: {{name}}..."
3. **Execute block:** Invoke `/btc-{{phase}}` or run inline logic
4. **Ledger Write:** Append block summary
5. **Update state:** Mark block COMPLETE in progress table
6. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK R{{X}} COMPLETE ═══
   Deliverables: [files created]
   Key findings: [1-3 bullets]

   CEO:
   (1) ✅ Approve → continue Block R{{X+1}}
   (2) 🔄 Re-run Block R{{X}} with adjustments: [describe]
   (3) ⏸️ Pause pipeline
   (4) ⏭️ Skip Block R{{X+1}}
   ```
7. **⛔ WAIT for CEO message.** Do not generate content until CEO responds.
8. **On CEO response:**
   - (1) → Execute next block (ONE block only, then STOP)
   - (2) → Re-run current block with adjustments, then STOP
   - (3) → Save state and halt
   - (4) → Skip next block, STOP and present the one after

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
BOOK-TO-CODEBASE PIPELINE COMPLETE — {{slug}}
═══════════════════════════════════════════════════
Library: {{library_name}} ({{placement_classification}})
Skills: {{N}} SKILL.md files across {{M}} domains
Domains: {{domain_list}}
Taxonomy: {{taxonomy_label}}

Infrastructure: {{btc_output_dir}}/library/
  setup.sh — junction install / update / verify / unlink
  CLAUDE.md — developer guide
  ARCHITECTURE.md — domain map + DAG
  hooks/ — {{N}} hooks (if wired)

Validation: {{validation_summary}} (V1/V2/V3/V4 results)

DMIR Retrospective: {{btc_output_dir}}/R9-DMIR.md
Galaxy Candidates: {{N}} proposed permanent notes
Usage Commitment: {{activation_cadence}}

Suggested follow-up:
  - /galaxy-note → create R9 Galaxy candidates
  - /research-to-skill <skill> → deepen any skill with external research
  - /helix-design-journal → log DMIR findings as design decisions
  - bash setup.sh --install <vault_path> → deploy to target vault
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files in `{{btc_output_dir}}/`:

| File / Folder | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_btc_state.md` | Orchestrator | All blocks | Progress, ledger, CEO decisions |
| `R1-Chapter-Index.md` | R1 | R2, R3, R4 | Chapter list + Apply This count + fast-path artifacts list |
| `R2-Extraction-Manifest.md` | R2 (merge) | R3, R4, R5, R6 | All extracted specs: Apply This + prose + R2.1 derivations |
| `R2-raw/Ch{{NN}}_extraction.md` | R2 (N subagents) | R2 merge | Per-chapter raw extraction output |
| `R3-Charter.md` | R3 | R4, R5, R6, R7, R9 | Library name, tagline, HELIX-FORGE placement (A/B/C/D), deployment path |
| `R3.0-Archetypes.md` | R3.0 (if --suggest) | R3 | 3 archetype proposals + CEO selection |
| `R4-Architecture.md` | R4 | R5, R6, R7, R8 | Domain taxonomy + skill DAG + domain→spec mapping |
| `R5-Ambiguity-Ledger.md` | R5 | R6 | Resolved/deferred ambiguities; 30-Q CEO answers; sane defaults |
| `R5.5-Delta-Report.md` | R5.5 (if --deep-scaffold) | R6 | KN-Stack overlap Cat A/B/C/D; delta skills to create |
| `R6-Skill-Registry.md` | R6 (merge) | R7, R8, R9 | All generated skill paths + concept_kind + confidence wave |
| `library/skills/{{domain}}/{{skill}}/SKILL.md` | R6 (N subagents) | R8 | Generated skill files |
| `R7-Infrastructure-Bundle.md` | R7 | R8, CEO | Manifest of all wired files: setup.sh, CLAUDE.md, etc. |
| `library/setup.sh` | R7 | CEO | Deploy / update / verify / unlink junctions |
| `library/CLAUDE.md` | R7 | CEO | Developer guide (mirrors KN-Stack CLAUDE.md pattern) |
| `library/ARCHITECTURE.md` | R7 | CEO | Domain map + DAG + placement rationale |
| `R8-Validation-Report.md` | R8 | R9, CEO | V1-V4 results; pass/fail per skill; remediation list |
| `R9-DMIR.md` | R9 | CEO | DMIR retrospective + Galaxy candidates + activation commitment |

## `--from-pipeline` Fast Path

When `--from-pipeline` flag is active, R1 reuses existing `codebase-to-book` artifacts:

```
FAST-PATH REUSE MAP
  Phase2-Positioning.md    → R3 charter seed (library identity ≈ book thesis)
  Phase3-Outline.md        → R4 architecture seed (domain ≈ part structure)
  Phase1-Exploration/P1_Synthesis.md  → R2 context enrichment (subsystem map)
  Phase7-Audit-Log.md      → R5 ambiguity context (IP + source citations)

FAST-PATH EFFECT ON EACH BLOCK:
  R1: reads 4 artifacts, flags reuse in Chapter Index
  R2: uses P1_Synthesis as background context for NLM queries
  R3: presents pre-filled charter from Phase2 + asks CEO to confirm/adjust
      → checkpoint becomes "approve" not "fill-in" (~60% less CEO time)
  R4: presents pre-structured taxonomy from Phase3 parts → CEO refines
  R5: uses Audit-Log IP context to pre-resolve source attribution questions

Without --from-pipeline: R3 and R4 are blank-slate CEO Core sessions.
```

## HELIX-FORGE Classification System

R3 (`btc-charter`) assigns a placement decision for the new skill library. Classification determines the deployment path and integration depth.

```
PLACEMENT DECISION MATRIX

  A — Forward Pipeline Enhancement
      └── New block-skill for existing HELIX or FORGE pipeline
      └── Example: a new helix-p2-* or forge-* skill
      └── Deploy to: d:\KN-Stack\skills\helix\ or skills\forge\

  B — Domain-Specific Skill (new domain, named prefix)
      └── Standalone domain not in current KN-Stack taxonomy
      └── Example: a "logistics-*" or "acoustic-*" domain
      └── Deploy to: d:\KN-Stack\skills\{{new_domain}}\

  C — Compound Tool (cross-domain peer library)
      └── Encodes compound learning across multiple existing domains
      └── Example: gstack → station+gate pipeline (HELIX pattern) + compound cluster
      └── Deploy to: standalone repo with own setup.sh + junction to ~/.claude/commands/

  D — Galaxy Note Only
      └── Concept too abstract or too domain-specific to be operational
      └── No SKILL.md; one or more Galaxy permanent notes instead
      └── Route to: /galaxy-note (R9 surfacess candidates)

Verdict rationale is documented in R3-Charter.md + R9-DMIR.md.
```

## DMIR Meta-Layer

R9 (`btc-handoff`) applies the DMIR framework (from `cycle` skill) as a retrospective lens over the full pipeline run.

```
DMIR QUESTIONS (enrichment — not blocking; pipeline completes without answers)

  D — DIAGNOSE
      "What problem did this skill library solve that KN-Stack couldn't before?"
      Log: what was missing in the pre-BTC state

  M — MODEL
      "What mental model does this library encode?"
      Log: the key abstraction or framework crystallized into skills

  I — INTERVENE
      "What will be different in the next real project that uses these skills?"
      Log: first concrete activation use case + cadence commitment

  R — REFLECT
      "What did the extraction process reveal about the book itself?"
      Log: gaps surfaced (Cat D delta), quality issues, Apply This density

DMIR output goes to: R9-DMIR.md
If CEO skips DMIR questions: log as "(incomplete)" — no re-prompt.
```

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After completing each block, STOP and WAIT for CEO response. NEVER execute 2+ blocks in one turn. NEVER combine blocks without CEO explicitly requesting. #1 rule.
- **CEO checkpoint after EVERY block** — no auto-continue without explicit CEO approval ("continue", "approve", "ok", v.v.)
- **Orchestrator NEVER does block work itself** — always delegate to sub-skill
- **Pipeline state file is source of truth** — always read before any action
- **Each block-skill is independently runnable** — CEO can `/btc-architect gstack` alone
- **Data bus contract is sacred** — block outputs use exact filenames in Data Bus table
- **Apply This is extraction spine** — specs from Apply This sections take priority over prose-inferred specs; never invent specs not in the book
- **Null discipline in R2.1** — if book doesn't specify stopping_conditions, output_artifact, or input_artifact for a concept: return `null`, surface at R5; never invent values
- **R3 placement is CEO Core** — AI proposes A/B/C/D with rationale; CEO decides; no placement without explicit CEO approval
- **R4 taxonomy is CEO Core** — AI proposes domain names + DAG; CEO approves; affects all downstream R6 file paths
- **R5 cap at 30 CEO questions** — excess questions → Section C (deferred with sane defaults); prevent CEO fatigue
- **R6 confidence waves** — Wave 1 (high-confidence Apply This specs), Wave 2 (prose-derived), Wave 3 (R2.1 derivations), Wave 4 (gap-fills from R5 defaults); CEO reviews Wave 4 sample before batch approval
- **R8 validation is non-negotiable** — V1 static check runs even if CEO says "skip"; CEO can waive V4 e2e only
- **--deep-extract vs --deep-scaffold are independent cost profiles** — R2-deep scales with chapters; R6-deep scales with skill count; present cost estimate before each if not flagged upfront
- **Language discipline** — `--lang en` (default): all SKILL.md in English (code consumed by Claude). `--lang vi`: narrative in Vietnamese, technical terms English
- **Cat D delta = forward pipeline feedback** — skills with no Apply This coverage surfaced at R5.5 are signals for the next book iteration, not pipeline failures
- **NLM auth failure = HALT** — do not bypass; instruct CEO to run `nlm login` in terminal
- **If CEO says "run all" or "skip checkpoints"** — STILL stop after each block but checkpoint minimal (1-line summary + "continue?")

## Integration

```
book-to-codebase (ORCHESTRATOR) COMMANDS:
  → /btc-ingest       (Block R1)
  → /btc-extract      (Block R2)
  → /btc-suggest      (Block R3.0 — standalone or --suggest)
  → /btc-charter      (Block R3)
  → /btc-architect    (Block R4)
  → /btc-resolve      (Block R5)
  → /btc-scaffold     (Block R6)
  → /btc-wire         (Block R7)
  → /btc-validate     (Block R8)
  → /btc-handoff      (Block R9)

book-to-codebase READS FROM:
  - <book_output_dir>/Phase6-Revised/ or Phase4-Chapters/ — canonical chapters
  - <book_output_dir>/Phase2-Positioning.md — (--from-pipeline)
  - <book_output_dir>/Phase3-Outline.md — (--from-pipeline)
  - <book_output_dir>/Phase1-Exploration/P1_Synthesis.md — (--from-pipeline)
  - <book_output_dir>/Phase7-Audit-Log.md — (--from-pipeline: IP context)
  - <book_output_dir>/_pipeline_state.md — (--from-pipeline: prior run metadata)

book-to-codebase INVOKES (R1/R2 via MCP):
  - mcp__notebooklm-mcp__refresh_auth
  - mcp__notebooklm-mcp__notebook_query (R2 extraction queries)
  - mcp__notebooklm-mcp__notebook_query_start / notebook_query_status (async)

book-to-codebase INVOKES (when --deep-scaffold):
  - /research --deep <skill-topic> — per skill in R6

book-to-codebase WRITES TO:
  - <book_output_dir>/btc-output/ — all BTC deliverables per Data Bus
  - <book_output_dir>/btc-output/library/ — generated skill library

book-to-codebase FOLLOW-UP (CEO-triggered):
  - /galaxy-note → create R9 Galaxy candidates as permanent notes
  - /research-to-skill <skill> → deepen any skill with external research
  - /helix-design-journal → log DMIR findings as design decisions
  - bash library/setup.sh --install <vault_path> → deploy to target vault
  - /codebase-to-book <library/> → meta-loop: book the new skill library

REFERENCES (in book-to-codebase/references/):
  - extraction-templates.md → Apply This pre-pass + 6 standard + 3 deep NLM queries + R2.1
  - skill-md-template.md → 6 SKILL.md stubs by concept_kind
  - domain-mapping-heuristics.md → A/B/C/D placement + taxonomy rules
  - ambiguity-decision-tree.md → R5 auto-resolve logic + sane defaults
  - validation-rubric.md → V1-V4 criteria + pass/fail thresholds
```

## `--suggest` Standalone Mode (`/btc-suggest`)

`/btc-suggest <book_output_dir>` runs R1 + R3.0 only — no pipeline commitment.

```
OUTPUT: R3.0-Archetypes.md with 3 architecture proposals:

  Archetype α — Minimal (SKILL.md-only, no setup.sh, no domain prefix)
    → Best when: book encodes 1-3 dense decision rules; placement Type A or D
    → Skill count estimate: {{N}}

  Archetype β — Standard (domain-prefixed, setup.sh, CLAUDE.md)
    → Best when: book encodes 5-15 cohesive skills in 2-3 domains
    → Skill count estimate: {{N}}

  Archetype γ — Anchor-Based (taxonomy preserves book structure; station+gate)
    → Best when: book has explicit process model (pipeline, phases, stations)
    → Recommended when: book was generated by codebase-to-book (--from-pipeline)
    → Skill count estimate: {{N}}

CEO selects archetype → becomes R3 charter seed if pipeline continues.
CEO can stop after /btc-suggest without running full pipeline.
```

## COD Classification

- Pipeline orchestration: Offload (O1)
- Block execution: Offload (O2) — each block has own COD
- R3 placement decision: **Core (C)** — non-delegable
- R4 taxonomy approval: **Core (C)** — non-delegable
- R5 ambiguity answers: **Core (C)** — up to 30 questions max
- R6 Wave 4 sample review: **Core (C)** — before batch approval
- R8 V4 e2e waiver (if CEO skips): **Core (C)**
- R9 DMIR + usage commitment: **Core (C)** — non-delegable
- DMIR retrospective questions: **Core (C)**
