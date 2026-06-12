# mentor-skill-template.md

This is the template used by `/mentor-board --add <leader>` at step A7 to generate the new `skills/mentors/mentor-<leader>/SKILL.md`.

Placeholders `{{...}}` are substituted by the ADD pipeline with values from A5 (8-query extraction) and A4 (NLM URLs per facet).

---

## Template Content (copy verbatim to new mentor SKILL.md, then substitute)

```markdown
---
name: mentor-{{LEADER_SLUG}}
description: "Cố vấn AI nhân bản tư duy của {{LEADER_FULL_NAME}} — {{LEADER_BIO_ONELINE}}. Specialties: {{SPECIALTIES_CSV}}. Built from {{TOTAL_SOURCES}} sources (T1 direct: {{T1_COUNT}}, T2 authoritative: {{T2_COUNT}}, T3 other: {{T3_COUNT}}) across {{FACET_COUNT}} NotebookLM notebook(s). Default mode: 5-frame DMIR CONSULT cross-facet (Diagnose → Model → Intervene → Reflect). Flags: --help, --facet <name>|auto, --facets, --refresh, --check-new, --history, --reliability. Triggers on: 'mentor {{LEADER_SLUG}}', 'cố vấn {{LEADER_VN_NAME}}', '{{LEADER_SLUG}} advice', '{{LEADER_SLUG}} thinks', '{{ALIAS_KEYWORDS}}', 'consult {{LEADER_SLUG}}'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# mentor-{{LEADER_SLUG}} — {{LEADER_FULL_NAME}} Advisor

> **Role:** Single-mentor advisor skill. Direct callable: `/mentor-{{LEADER_SLUG}} "<problem>"`. Also dispatched by `/mentor-board` for PANEL/DEBATE/DECIDE/PRESET modes.
> **Parent orchestrator:** `mentor-board` (galaxy/) handles multi-mentor synthesis.
> **DMIR canonical:** Diagnose → Model → Intervene → Reflect — see `galaxy/mentor-board/references/dmir-template.md`.

## Bio (from 8Q A5 extraction)

{{LEADER_FULL_NAME}} — {{LEADER_BIO_PARA}}

**Era of content:** {{ERA_RANGE}}
**Primary works (Tier 1):** {{T1_WORKS_LIST}}
**Specialties:** {{SPECIALTIES_CSV}}

## Frameworks & Mental Models (Q1, Q2 of 8Q extraction)

{{FRAMEWORKS_LIST_NUMBERED}}

Each framework appears in `chat_configure` persona prompt and influences which facet is selected via `--facet auto`.

## Decision Rules (Q1, Q4 of 8Q extraction)

{{DECISION_RULES_BULLET_LIST}}

These rules appear in 5-frame DMIR Frame 2 (Model) output when CEO queries this mentor.

## What They REJECT (Q3 of 8Q extraction)

{{REJECTIONS_BULLET_LIST}}

These appear in Frame 3 (Rejection) — the contrarian layer that pushes back against CEO's default approach.

## Notebooks (Multi-Facet Support)

See `notebooks/_index.md` for current facet registry.

{{FACET_COUNT}} facet(s):

{{FACETS_TABLE}}

**Cross-facet query (default):** when CEO calls `/mentor-{{LEADER_SLUG}} "<problem>"`, all facets queried in parallel, output synthesizes with `[facet_name]` citation tags.

**Facet targeting:** `/mentor-{{LEADER_SLUG}} --facet <name> "<problem>"` narrows to single facet.

**Auto routing:** `/mentor-{{LEADER_SLUG}} --facet auto "<problem>"` — AI picks most-relevant facet based on problem keywords + past query stats.

## Modes

```
/mentor-{{LEADER_SLUG}}                          # Show profile + last_refresh + reliability stats
/mentor-{{LEADER_SLUG}} --help                   # Cheat sheet
/mentor-{{LEADER_SLUG}} "<problem>"              # CONSULT (5-frame DMIR, cross-facet)
/mentor-{{LEADER_SLUG}} --facet <name> "<problem>"   # CONSULT scoped to 1 facet
/mentor-{{LEADER_SLUG}} --facet auto "<problem>"     # CONSULT — AI picks best facet
/mentor-{{LEADER_SLUG}} --facets                 # List facets + source counts + last_refresh
/mentor-{{LEADER_SLUG}} --refresh                # Refresh all facets
/mentor-{{LEADER_SLUG}} --refresh --facet <name> # Refresh single facet
/mentor-{{LEADER_SLUG}} --check-new              # Scan new content (no ingest)
/mentor-{{LEADER_SLUG}} --history                # Past 10 consultations
/mentor-{{LEADER_SLUG}} --reliability            # Hits/misses per problem class
```

## CONSULT Workflow

For full pipeline detail, see `galaxy/mentor-board/references/dmir-template.md`.

1. **C1** Parse problem. If invoked directly (not via INTAKE), ask optional context — **C** (skip if INTAKE-routed with intake_context).
2. **C2** Read `references/persona.md`, `notebooks/_index.md`, and `D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/reliability_log.md`.
3. **C3** NLM auth pre-check via `mcp__notebooklm-mcp__refresh_auth`. If fail → prompt CEO `nlm login`.
4. **C4** Configure persona via `mcp__notebooklm-mcp__chat_configure(notebook_id=<primary_facet>, goal="custom", custom_prompt=<from persona.md>)`. Repeat per facet if multi.
5. **C5** Execute 5-frame DMIR query (template from dmir-template.md):
   - Single facet: 5 queries × 1 facet
   - Multi facet: 5 queries × N facets parallel, then synthesize per-frame
6. **C6** Compose output markdown with frontmatter:
   ```yaml
   ---
   consult_id: <YYYYMMDD-HHMM-slug>
   mentor: {{LEADER_SLUG}}
   mode: CONSULT
   problem: "<problem>"
   facets_queried: [<list>]
   intake_context: <from INTAKE if applicable>
   prediction_at: <today + planned action date for --retro tracking>
   ---
   ```
7. **C7** Frame 6 R-section initialized empty with `consult_id` for `/mentor-board --retro <consult-id>` later.
8. **C8** Write to `D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/<YYYYMMDD>-{{LEADER_SLUG}}-<slug>.md`.
9. **C9** Append entry to mentor's history (in `D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/profile.md`).
10. **C10** Provide NLM URL(s) for optional follow-up free-chat.

## REFRESH Workflow

1. **R1** Read `notebooks/_index.md` for facet list + last_refresh per facet.
2. **R2** For each facet (or specified `--facet`): multi-channel search since last_refresh date.
3. **R3** Tier-classify findings (T1/T2/T3). Present to CEO — **C**.
4. **R4** Dedup against existing facet sources (`nlm source list <facet>`). Ingest approved with TRY1→2→3 recovery.
5. **R5** Delta query per refreshed facet: "Điều gì MỚI? Contradicting? Evolution?"
6. **R6** Update profile.md "Evolution" section (append, not overwrite). Bump facet's last_refresh in `notebooks/_index.md`.
7. **R7** Log to `D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/refreshes/<YYYY-MM>.md` (per-facet new sources + delta findings).

## CHECK-NEW Workflow (lightweight, no NLM writes)

1. Read last_refresh from `notebooks/_index.md`.
2. Multi-channel search for new content since that date.
3. Output table:
   ```
   New content available since <last_refresh>:
   | Facet | New T1 | New T2 | New T3 | Recommend refresh? |
   |-------|:------:|:------:|:------:|:------------------:|
   | <facet 1> | 2 | 1 | 0 | YES (T1 detected) |
   | <facet 2> | 0 | 0 | 3 | NO (only T3) |
   ```

## HISTORY Mode

Read `D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/*-{{LEADER_SLUG}}-*.md` (last 10), display table:
| Date | Consult ID | Problem | Mode | R-step status |

## RELIABILITY Mode

Render `D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/reliability_log.md` directly. Show:
- Per-class stats (N, hits, misses, partials, % with confidence flag)
- Recent retros (last 10)
- Patterns detected (5+ misses same class → warning)

## FACETS Mode

List all facets with metadata:
```
{{LEADER_FULL_NAME}} facets:

| Facet | NLM URL | Sources | Scope | Last refresh |
|-------|---------|:-------:|-------|--------------|
| <facet 1> | <url> | <N> | <description> | <date> |
| <facet 2> | <url> | <N> | <description> | <date> |

Cross-facet query default. Use `--facet <name>` to narrow.
Use `--facet auto` for AI routing.
```

## --facet auto Heuristic

When CEO uses `--facet auto`, AI picks facet by:
1. Keyword matching: problem contains terms strongly associated with facet scope
2. Past query stats: which facet most-cited for similar problem class
3. Recency preference: if problem is current/operational → recent facet; if foundational/strategic → primary or temporal-early facet
4. Default fallback: PRIMARY facet (the one marked ✓ in `notebooks/_index.md`)

## Integration

```
mentor-{{LEADER_SLUG}} READS:
  - references/persona.md → chat_configure prompt
  - references/seed-sources.md → source registry
  - notebooks/_index.md → facet list + NLM URLs
  - D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/profile.md → grounding
  - D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/reliability_log.md → confidence display

mentor-{{LEADER_SLUG}} WRITES:
  - D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/<file>.md → consults
  - D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/profile.md → history append
  - D:/Workshop_X/3_Resources/Mentor-Board/{{LEADER_SLUG}}/refreshes/<YYYY-MM>.md → refresh logs

mentor-{{LEADER_SLUG}} CALLED BY:
  - /mentor-{{LEADER_SLUG}} (direct CEO call)
  - /mentor-board (orchestrator dispatch in CONSULT/PANEL/DEBATE/DECIDE modes via Task subagent)

mentor-{{LEADER_SLUG}} MCP CALLS:
  - mcp__notebooklm-mcp__refresh_auth
  - mcp__notebooklm-mcp__chat_configure (per facet)
  - mcp__notebooklm-mcp__notebook_query (5 frames × N facets)
  - mcp__notebooklm-mcp__source_add (REFRESH only)
  - mcp__notebooklm-mcp__source_list (CHECK-NEW + dedup)
```

## Rules

- **Persona purity strict** — `chat_configure` instructs NLM to answer ONLY using sources from this mentor's notebook(s). Cite per claim. If no source → "[UNCERTAIN]".
- **DMIR 5-frame mandatory** — no skipping Frame 3 (Rejection) or Frame 4 (Adaptation). These are the contrarian and VN-adapt layers that prevent generic advice.
- **Cross-facet default** — multi-facet mentors query ALL facets by default. Use `--facet` to narrow only when CEO is confident.
- **Reliability is empirical** — accuracy comes from `--retro` history, not declaration. Show "low confidence (n=<N>)" when reliability log thin.
- **Append-only history** — never overwrite consult outputs or profile history.

## COD Classification

- Mode routing: Offload (O1)
- NLM query execution: Offload (O1)
- 5-frame synthesis: Offload (O2)
- Frame 4 (VN adaptation): Offload (O2) — AI draws on persona, CEO validates accuracy
- **Persona prompt edit (`references/persona.md`): Core (C)** — affects all future consults
- **Source selection at REFRESH R3: Core (C)** — quality determines downstream consult quality
- **--retro inputs: Core (C)** — honest hit/miss tracking is non-delegable
```

## Template Substitution Variables (filled by ADD A7)

| Placeholder | Source | Example for Naval Ravikant |
|---|---|---|
| `{{LEADER_SLUG}}` | A1 — canonical slug | `naval-ravikant` |
| `{{LEADER_FULL_NAME}}` | A1 — display name | `Naval Ravikant` |
| `{{LEADER_VN_NAME}}` | A1 — VN nickname if any | `Naval` |
| `{{LEADER_BIO_ONELINE}}` | A5 Q1 — distillation | "Co-founder AngelList, specific knowledge + leverage theorist" |
| `{{LEADER_BIO_PARA}}` | A5 Q1 — 3-5 sentences | (longer bio para) |
| `{{ERA_RANGE}}` | A2 metadata | "2007-2024 (active investor + writer era)" |
| `{{TOTAL_SOURCES}}` | A4 sum | `28` |
| `{{T1_COUNT}}`, `{{T2_COUNT}}`, `{{T3_COUNT}}` | A3 selection | 18, 7, 3 |
| `{{T1_WORKS_LIST}}` | A3 — bulleted | "naval.al essays · Almanack · Joe Rogan #1309 · Tim Ferriss appearances" |
| `{{FACET_COUNT}}` | A3.5 | `1` (no split) or `3` (multi-facet) |
| `{{SPECIALTIES_CSV}}` | A5 Q1+Q4 | "specific knowledge, leverage, judgment, founder mode, internet wealth" |
| `{{ALIAS_KEYWORDS}}` | A5 — common triggers | "naval, ravikant, specific knowledge, angellist" |
| `{{FRAMEWORKS_LIST_NUMBERED}}` | A5 Q1+Q2 — markdown numbered list | (numbered framework list) |
| `{{DECISION_RULES_BULLET_LIST}}` | A5 Q1+Q4 — bullets | (rules) |
| `{{REJECTIONS_BULLET_LIST}}` | A5 Q3 — bullets | (rejections) |
| `{{FACETS_TABLE}}` | A3.5 — markdown table | (facet table per notebooks/_index.md) |

## Validation After A7 Substitution

Before A8 (deploy junction), AI checks:
- No remaining `{{...}}` placeholders in generated SKILL.md (use grep)
- Frontmatter description ≥100 chars and includes triggers
- All TOC links resolve
- `references/persona.md` exists and is filled (separate file generated alongside)
- `notebooks/_index.md` exists with at least 1 facet
- Skill folder structure matches expected pattern

If any check fails → halt ADD pipeline, surface to CEO for fix.
