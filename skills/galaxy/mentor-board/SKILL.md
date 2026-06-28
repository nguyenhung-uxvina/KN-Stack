---
name: mentor-board
description: "Hội đồng cố vấn AI — orchestrator điều phối 7 mentor skills riêng biệt (Musk, Munger, Marks, Dalio, Huang, Naval, Grove) đã 'nhân bản tư duy' từ talks/books/writings của họ qua NotebookLM. Default entry point: `/mentor-board \"<problem>\"` → INTAKE smart router (clarifying questions → propose mentor list + mode → CEO confirm → route). 4 consultation modes: CONSULT (single, 5-frame DMIR report), PANEL (multi parallel + synthesis), DEBATE (3-round argument: position→rebuttal→convergence), DECIDE (option scoring matrix). DMIR cycle applied to mọi consult (Diagnose→Model→Intervene→Reflect); `--retro <consult-id>` closes R-step + updates mentor's reliability_log. Multi-notebook per mentor (facet split nếu >45 sources). Board management: --add (~2h pipeline tạo new mentor skill), --remove (archive), --rename, --suggest (AI propose new mentors based on consult patterns), --list, --check-new --all, --sync --all. Manual refresh per mentor. Triggers on: 'mentor board', 'hội đồng cố vấn', 'vĩ nhân', 'cố vấn elon', 'cố vấn munger', 'consult advisor', 'mentor advice', 'tư vấn vĩ nhân', 'naval', 'munger', 'mentor debate', 'mentor decide', 'mentor panel'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# mentor-board — Hội Đồng Cố Vấn AI (DMIR-driven Multi-Mentor Orchestrator)

> **Role:** Orchestrator điều phối các mentor-* skills riêng biệt. Mỗi mentor = 1 skill độc lập với own NotebookLM. mentor-board = sync layer + multi-mentor modes.
> **Why exist:** CEO Workshop X cần truy cập tư duy của các vĩ nhân doanh nhân (Musk, Munger, Marks, Dalio, Huang, Naval, Grove) như một hội đồng cố vấn. Mỗi consultation áp DMIR cycle, mỗi advice là compounding learning asset (prediction tracked → reliability log).
> **Pattern precedent:** helix-task-clarify orchestrator + helix-p1-* blocks; codebase-to-book + book-* blocks.
> **DMIR canonical (Workshop X):** D-Diagnose → M-Model → I-Intervene → R-Reflect (from `/cycle` + `/reflect`).

## Quick Start

```
/mentor-board "<problem>"          # default smart router — recommended for most CEO use
/mentor-board --help               # full usage guide
/mentor-board                      # registry view (no problem)
```

CEO **không cần memorize flags** — gõ vấn đề tự nhiên, AI sẽ clarify + propose mentors + propose mode + CEO confirm trước khi run.

## Mode Inventory

```
# Help + Registry
--help                            # full cheat sheet (reads references/help-content.md)
--help <mode>                     # drilldown cho 1 mode
(no args, no problem)             # registry view
--list                            # detailed table với reliability stats
--suggest                         # AI proposes new mentors (≥5 consults required)

# Roster Management
--add <leader>                    # CREATE new mentor-<leader> skill (~2h, 5 gates)
--remove <leader>                 # archive (not delete)
--rename <old> <new>

# Bulk Maintenance
--check-new --all
--sync --all                      # batch refresh all mentors

# ENTRY (default smart router)
"<problem>"                       # INTAKE flow: clarify → propose → confirm → route
                                  # OR routes directly if CEO already specified --mode

# Multi-mentor consultation modes
--consult                         # interactive picker (no problem yet)
--consult <leaders> "<problem>"   # explicit single/multi
--panel <leaders|preset> "<problem>"   # parallel 5-frame + synthesis
--debate <leaders|preset> "<problem>"  # 3-round argument
--decide <leaders|preset> "<problem>" --options "A; B; C"   # option matrix

# DMIR closure
--retro <consult-id>              # close R-step on any past consult
```

**Presets** (for multi-mentor modes): `capital` (Munger+Marks+Dalio) · `scaling` (Musk+Huang+Grove) · `ai-strategy` (Huang+Musk+Naval) · `manufacturing` (Musk+Grove) · `founder-wisdom` (Naval+Grove+Munger) · `people` (Grove+Dalio+Munger) · `all` (7 mentors)

See `references/preset-clusters.md` cho chi tiết logic.

## Architecture

```
skills/
├── mentors/                          # PER-MENTOR domain (each callable directly)
│   ├── mentor-musk/SKILL.md
│   ├── mentor-munger/SKILL.md
│   └── ... (7 total, generated via --add)
└── galaxy/mentor-board/              # THIS — orchestrator
    ├── SKILL.md
    └── references/
        ├── help-content.md            # --help canonical content
        ├── intake-protocol.md         # smart router logic
        ├── dmir-template.md           # 5-frame consult template
        ├── debate-protocol.md         # 3-round argument
        ├── decide-matrix.md           # option scoring matrix
        ├── preset-clusters.md         # preset definitions
        ├── retro-template.md          # DMIR R-step
        ├── facet-split-strategies.md  # multi-notebook split logic
        └── mentor-skill-template.md   # --add generates new mentor-X SKILL.md from this
```

**Vault outputs:**
- `D:/Workshop_X/3_Resources/Mentor-Board/_registry.md` — append-only ledger
- `D:/Workshop_X/3_Resources/Mentor-Board/<leader>/` — profile + reliability_log + refreshes
- `D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/<YYYYMMDD>-<leader|mode>-<slug>.md` — per-consult output

## Workflow Router

```
Parse $ARGUMENTS:

IF --help (with or without <mode>) → run HELP pipeline (read references/help-content.md, render)
ELIF --list → render registry detailed view
ELIF --suggest → run SUGGEST pipeline
ELIF --add <leader> → run ADD pipeline (~2h, NLM-heavy)
ELIF --remove <leader> → run REMOVE pipeline
ELIF --rename <old> <new> → run RENAME pipeline
ELIF --check-new (--all or single) → run CHECK-NEW pipeline
ELIF --sync --all → run SYNC pipeline
ELIF --retro <consult-id> → run RETRO pipeline (DMIR R-step)
ELIF --consult <leaders> "<problem>" → run CONSULT/PANEL routing
ELIF --panel <list|preset> "<problem>" → run PANEL pipeline
ELIF --debate <list|preset> "<problem>" → run DEBATE pipeline
ELIF --decide <list|preset> "<problem>" --options "..." → run DECIDE pipeline
ELIF --consult (no leader) → run INTERACTIVE PICKER → route
ELIF "<problem>" (no mode flag) → run INTAKE smart router → route
ELSE (no args) → render registry simple view
```

## Pipelines

### HELP (instant, no NLM)

1. Read `references/help-content.md`
2. If `--help <mode>` → extract mode-specific section, render
3. Else → render full cheat sheet
4. Never error, never touch NLM

### INTAKE (Smart Router — DEFAULT entry, ~5-10 min)

**Trigger:** `/mentor-board "<problem>"` (no mode flag).

1. **I1** Parse problem. If empty → ask "CEO có vấn đề cần tư vấn không?"
2. **I2** Read `references/intake-protocol.md` for clarifying questions. Present 6-question prompt to CEO. **C** — minimum: questions 1 (decision), 3 (options state), 6 (domain hint).
3. **I3** AI proposes mentor list with rationale:
   - Read `_registry.md` for available mentors + reliability_log per mentor
   - Match CEO's domain hint → recommend ★★★ / ★★ / ★ rated mentors
   - Flag MISSING-FROM-BOARD if ideal mentor not yet added → suggest `--add <name>` first
4. **I4** AI proposes mode (CONSULT/PANEL/DEBATE/DECIDE) using heuristics from `intake-protocol.md`:
   - 1 mentor + clear single framework → CONSULT
   - Multi mentors, exploring → PANEL
   - Multi mentors with detected tension → DEBATE
   - Has concrete options A/B/C → DECIDE
5. **I5** CEO confirms or adjusts — **C**:
   ```
   (1) ✅ Đồng ý → proceed
   (2) ➕ Thêm mentor: <name>
   (3) ➖ Bỏ mentor: <name>
   (4) 🔄 Đổi mode: <new>
   (5) 📝 Refine problem → loop I2
   (6) ⏸️ Cancel
   ```
6. **I6** Route to confirmed pipeline. Save CEO's intake answers as `intake_context:` frontmatter trong final output (provides D-Diagnose context to mentors).

### CONSULT — single mentor (via per-mentor skill, ~10 min)

When orchestrator invokes single-mentor CONSULT:

1. Delegate to `/mentor-<leader> "<problem>"` (the per-mentor skill handles its own NLM)
2. Per-mentor skill runs C1-C6 (see mentor-skill-template.md for details)
3. Output saved by per-mentor skill to `Mentor-Consultations/`
4. Increment per-mentor `consult_count` in registry

### PANEL — parallel 5-frame + synthesis (~15-20 min)

1. Parse leaders (explicit list or preset from `preset-clusters.md`)
2. CEO context enrichment (skip if from INTAKE) — **C**
3. **Parallel queries:** spawn 1 Task subagent per leader. Each agent reads `mentor-<leader>` profile + runs 5-frame DMIR query (see `dmir-template.md`) against that leader's NLM. Outputs staged to `<run_dir>/<leader>_frame.md`.
4. **Merge:** compose comparison matrix:
   - Per-frame summary table (Diagnosis/Model/Reject/Adapt/Action × leaders)
   - Full frame-by-frame expandable sections
   - **Frame 6 SYNTHESIS** (the value-add — see template in `dmir-template.md`):
     - Where they AGREE (consensus)
     - Where they DIFFER (productive tension)
     - CEO Decision Lens (high-confidence actions / trade-offs / watch-outs)
     - 3 Action Steps (CEO Core synthesis)
5. Write to `Mentor-Consultations/<YYYYMMDD>-panel-<slug>.md`
6. Update each leader's `consult_count` + add `panel_count` field

### DEBATE — 3-round argument (~30 min, the tranh luận mode)

See `references/debate-protocol.md` for full Round 1-3 prompts.

1. Parse leaders (≥2) + problem
2. CEO context enrichment — **C**
3. **Round 1 (Position):** parallel Task subagents per leader, each runs 5-frame DMIR on problem. Stage to `<run_dir>/round1_<leader>.md`.
4. **Round 2 (Rebuttal):** parallel agents. Each agent receives OTHER leaders' Round 1 outputs (NOT other notebooks — only outputs). Query template (from `debate-protocol.md`): "Read contrary views. Which do you most strongly disagree with? Rebut with citation from YOUR notebook." Stage to `round2_<leader>.md`.
5. **Round 3 (Convergence):** parallel agents read all Round 2 rebuttals. Query: "Do you UPDATE view? Where converge, where stay firm and why?" Stage to `round3_<leader>.md`.
6. **Synthesis (CEO Core):** merge 3 rounds into transcript identifying:
   - Productive tensions (with leader-by-leader trajectory across rounds)
   - What all agreed on
   - **What CEO Must Decide** (unresolved core)
   - DMIR closure section (D-M-I, R empty for `--retro`)
7. Write to `Mentor-Consultations/<YYYYMMDD>-debate-<slug>.md`
8. Update each leader's `debate_count`

### DECIDE — option scoring matrix (~20 min)

See `references/decide-matrix.md` for matrix template + scoring rubric.

1. Parse leaders + problem + `--options "A; B; C"` (≥2, ≤5 options)
2. CEO confirms framing — **C**
3. **Per mentor × per option:** parallel Task subagents. Each agent for (leader, option) runs query from `decide-matrix.md`: score 1-10 + rationale + risk + reverse-condition.
4. **Aggregate matrix:**
   - Rows: mentors; Columns: options; Cells: score + risk flag
   - Reliability weights applied (from each mentor's reliability_log for this problem class)
   - Weighted average per option
   - Strong reject flags (score ≤ 3)
   - Consensus risk identification
   - Reverse conditions table
5. **DMIR closure:**
   - D: decision framed
   - M: scoring models surfaced
   - I: CEO final pick — **C**
   - R: empty for `--retro`
6. Write to `Mentor-Consultations/<YYYYMMDD>-decide-<slug>.md`
7. Update each mentor's `decide_count` + log per-option predictions to their reliability_log for future tracking

### ADD — create new mentor-X skill (~2h, 5 CEO gates)

1. **A1** Resolve leader (canonical slug, e.g., "naval-ravikant" not "Naval"). Check not duplicate in registry.
2. **A2** Discover sources via multi-channel (reuse `/research` Step 1 + Step 4G logic — **Exa Channel 0 when available**, see `../research/references/exa-discovery.md`; WebSearch fallback otherwise). Tier classify T1/T2/T3 (see facet-split-strategies.md cho T criteria).
3. **A3** CEO reviews discovery, selects sources — **C**
4. **A3.5** **Facet split detection** — **C** if N > 45:
   - Read `references/facet-split-strategies.md` for strategy options (temporal/topical/hybrid)
   - CEO picks strategy
   - Assign sources to facets
5. **A4** For each facet (1 or N):
   - `mcp__notebooklm-mcp__notebook_create(title="mentor-<leader>" or "mentor-<leader>-<facet>")`
   - Ingest sources via `source_add` with TRY1→TRY2→TRY3 recovery (reuse `/research` Step 4G)
   - `nlm alias set mentor-<leader>[-<facet>] <uuid>`
   - Set persona via `chat_configure(goal="custom", custom_prompt=<from persona-prompts template>)`
6. **A5** 8-query foundational extraction (parallel if multi-facet):
   - Q1. Top 5-10 core decision principles
   - Q2. Recurring frameworks/mental models
   - Q3. What they REJECT as failure modes
   - Q4. Specific advice on entrepreneurship/leadership/scaling
   - Q5. Risk vs opportunity framing
   - Q6. People/team/culture philosophy
   - Q7. What they've changed mind about
   - Q8. VN/emerging-market analog (if any)
7. **A6** Studio artifacts on PRIMARY facet:
   - `studio_create(artifact_type="briefing_doc")` — one-pager
   - `studio_create(artifact_type="audio")` — Audio Deep Dive VN
   - `studio_create(artifact_type="quiz")` — 5Q understanding test
   - `studio_create(artifact_type="flashcards")` — decision rules
   - Poll `studio_status` until complete
8. **A7** Generate new skill file:
   - Read `references/mentor-skill-template.md`
   - Substitute: leader name, bio, specialties, frameworks, decision rules, NLM URLs per facet, persona prompt path
   - Write to `d:/KN-Stack/skills/mentors/mentor-<leader>/SKILL.md`
   - Also create `mentor-<leader>/references/persona.md` (from template + CEO-approved persona)
   - Also create `mentor-<leader>/references/seed-sources.md` (the curated source list)
   - Also create `mentor-<leader>/notebooks/_index.md` (facet registry)
9. **A8** Run `bash d:/KN-Stack/setup.sh --install "D:/Workshop_X"` to deploy junction
10. **A9** Append to `_registry.md`:
    ```markdown
    | <leader> | <NLM URL primary> | <facet_count> | <total_sources> | <today> | ACTIVE | 0 | 0 | 0 |
    ```
    Fields: leader, primary_nlm_url, facets, total_sources, last_refresh, status, consult_count, debate_count, decide_count
    CEO approve close — **C**
11. **A10** Initialize per-mentor profile:
    - `<leader>/profile.md` — bio + 8Q frameworks + decision rules
    - `<leader>/reliability_log.md` — empty header table
    - `<leader>/refreshes/` — empty folder

### REMOVE — archive (~1 min)

1. CEO confirm archive (NOT delete) — **C**
2. Move `D:/Workshop_X/3_Resources/Mentor-Board/<leader>/` → `Mentor-Board/_archived/<leader>-<YYYYMMDD>/`
3. Rename NLM notebook(s): `mcp__notebooklm-mcp__notebook_rename` with `[ARCHIVED]` prefix
4. Move skill folder: `d:/KN-Stack/skills/mentors/mentor-<leader>/` → `d:/KN-Stack/skills/mentors/_archived/`
5. Remove junction: `rm "C:/Users/Admin/.claude/commands/mentor-<leader>"`
6. Update registry: status=ARCHIVED, archived_date=today
7. Historical consultations stay valid (queryable)

### RENAME (~1 min)

1. Rename vault folder
2. Rename NLM via `notebook_rename`
3. Rename skill folder + re-run `setup.sh --install` to recreate junction
4. Update registry with both names (old as alias for past consults)

### REFRESH (per mentor, ~30 min) — Delegated

CEO calls `/mentor-<leader> --refresh` (per-mentor skill handles its own refresh).

If `/mentor-board --sync --all` → orchestrator iterates registry, invokes each `/mentor-<leader> --refresh` sequentially (NOT parallel — avoid NLM rate limit).

### CHECK-NEW — Delegated

CEO calls `/mentor-<leader> --check-new` (per-mentor skill).

If `/mentor-board --check-new --all` → orchestrator iterates registry, runs check-new for each. Output: bulk table "Leader | New sources | Recommend refresh? Y/N".

### RETRO — DMIR R-step closure (~5-10 min, the compound learning step)

See `references/retro-template.md` for R-section format.

1. Read `<consult-id>.md` from `Mentor-Consultations/`
2. Identify which mentor(s) made predictions in this consult
3. **CEO inputs (mandatory honesty)** — **C**:
   - What action did you take? (concrete)
   - What outcome happened? (factual)
   - Did mentor's prediction match outcome? HIT / MISS / PARTIAL
   - What was learned about their framework's applicability to WX context?
4. Update Frame 6 R-section in original consult file (APPEND, not overwrite — preserves history if same consult revisited)
5. Update mentor's `<leader>/reliability_log.md`:
   - Row: consult_id, date, problem_class, predicted, actual, hit/miss/partial, notes
6. Pattern detection: if mentor has 5+ misses in same problem_class → output warning:
   ```
   ⚠️ <leader> has 5+ misses in <class> consultations.
   Recommendations:
   (1) Revise persona prompt → reduce overconfidence
   (2) Downgrade weight in --decide matrix for this class
   (3) Add complementary mentor to board to balance
   ```
   CEO decides action — **C**.

### SUGGEST — AI proposes new mentors (~5 min)

1. Scan `Mentor-Consultations/*.md` from last 30 days
2. If < 5 consults → output "Insufficient data, run more consultations first."
3. Extract problem classes from consults + reliability_log misses
4. Identify gaps: classes with low coverage OR low aggregate reliability
5. Propose 3-5 new mentor candidates với:
   - Name + primary works (T1 sources)
   - Specific gap they'd fill
   - Estimated source pool size + setup effort
6. CEO accepts → `/mentor-board --add <suggested>` flow — **C**

## Reused Patterns

- **NLM source-add + TRY1/2/3 recovery:** from `/research` Step 4G
- **Tier S/A/B/C classification:** from `/research` + `source-tiers.md` (adapted to T1/T2/T3 for personas)
- **6Q→8Q extraction framework:** from `/skill-from-research`
- **chat_configure persona setup:** from `/research`, `/reverse-engineering`
- **First-principles STRIP/INVERT/REBUILD:** from `/research-to-skill` (used in Frame 4 adaptation)
- **Studio artifacts (Briefing/Audio/Quiz/Flashcards):** from `/research`, `/learning`
- **Parallel Task subagent orchestration:** from `/codebase-to-book` P1/P4/P5
- **Multi-skill orchestrator pattern:** from `helix-task-clarify` + `helix-p1-*`
- **NLM auth detect-pause:** from `/research` Step 3.5
- **Append-only registry:** from skill-to-public's `_published_registry.md`, codify's `_codify_ledger.md`
- **DMIR cycle:** from `/cycle`, `/reflect`

## Rules

- **Tier 1 source mandatory** — mỗi mentor PHẢI có ≥3 T1 sources (own writings/talks). Violation = abort ADD.
- **Persona purity strict (default)** — `chat_configure` instructs NLM "answer in <leader>'s voice using ONLY their writings; cite source per claim; refuse if no source supports." CEO can `--persona-purity standard` if too restrictive.
- **DMIR mandatory structure** — every consult output has 5 frames mapped to D-M-I-R + Frame 6 R-section (filled via `--retro` after action).
- **Reliability tracking is the compound asset** — each mentor's hits/misses logged via `--retro`. After 5 misses same class → warning + CEO action.
- **VN/WX adaptation Frame 4 cannot skip** — original US/global advice always adapted to Workshop X defense context.
- **No advisor source merging** — 1 mentor = own notebook(s). Cross-mentor wisdom only emerges in PANEL/DEBATE/DECIDE synthesis layer (orchestrator).
- **Multi-facet per-mentor decision** — A3.5 triggers only if >45 sources. CEO picks split strategy.
- **Cross-facet query default** — `/mentor-X "<problem>"` queries ALL facets in parallel + synthesizes with citation tags. Use `--facet <name>` to narrow.
- **INTAKE smart router is front door** — `/mentor-board "<problem>"` (no flags) routes through I1-I6. Direct flags bypass for power users.
- **`--help` always works** — never errors, no NLM, instant. Reads `references/help-content.md`.
- **DEBATE Round 2 sees outputs only** — agents see other mentors' Round 1 OUTPUTS, never other notebooks (no source contamination).
- **DECIDE option count 2-5** — fewer = not real decision, more = decision fatigue.
- **Archive, never delete** — REMOVE = archive + `[ARCHIVED]` prefix. Historical consults remain valid.
- **CEO Core gates non-delegable:** A3 source selection, A9 close approve, all C1/Db1/Dc1 problem framing, Dc4 final decision, all Re2 retros.
- **Reliability log feeds DECIDE weights** — mentor low accuracy on class X → reduced weight in DECIDE matrix for that class. Show "low confidence" if <5 retros tracked.

## Integration

```
mentor-board COMMANDS (delegates to per-mentor skills):
  → /mentor-<leader> "<problem>"       (single CONSULT, per-mentor skill handles NLM)
  → /mentor-<leader> --refresh          (per-mentor refresh)
  → /mentor-<leader> --check-new        (per-mentor scan)

mentor-board ORCHESTRATES (parallel Task subagents):
  PANEL: N agents × 1 query/agent = N parallel
  DEBATE: N agents × 3 rounds = 3N sequential rounds, each round N parallel
  DECIDE: N agents × M options = N*M parallel queries
  ADD A5: N facet agents × 8 queries = up to 8N parallel

mentor-board READS:
  - _registry.md → advisor list + reliability + counts
  - <leader>/profile.md → frameworks + decision rules (used in synthesis)
  - <leader>/reliability_log.md → weighting for DECIDE
  - Mentor-Consultations/ → SUGGEST pattern analysis, RETRO lookup

mentor-board WRITES:
  - _registry.md → append-only
  - Mentor-Consultations/<YYYYMMDD>-<mode>-<slug>.md → per-consult outputs
  - <leader>/reliability_log.md → via RETRO closure
  - skills/mentors/mentor-<leader>/ → generates via ADD A7

mentor-board MCP CALLS (via per-mentor skills + own):
  - mcp__notebooklm-mcp__notebook_create  (ADD A4)
  - mcp__notebooklm-mcp__source_add        (ADD A4)
  - mcp__notebooklm-mcp__chat_configure   (ADD A4 — persona)
  - mcp__notebooklm-mcp__notebook_query   (CONSULT, PANEL, DEBATE, DECIDE)
  - mcp__notebooklm-mcp__studio_create    (ADD A6)
  - mcp__notebooklm-mcp__studio_status     (ADD A6)
  - mcp__notebooklm-mcp__notebook_rename   (REMOVE, RENAME)
  - mcp__notebooklm-mcp__refresh_auth      (pre-checks)

mentor-board FOLLOW-UP (CEO-triggered):
  - /skill-to-public → turn favorite consult into public post (Naval-style leverage)
  - /galaxy-note → extract pattern from consult to Galaxy permanent note
  - /helix-design-journal → log decisions influenced by mentors
```

## COD Classification

- Mode routing: Offload (O1) — deterministic flag parsing
- HELP rendering: Offload (O1)
- INTAKE clarifying question generation: Offload (O2)
- **INTAKE problem framing (CEO answers): Core (C)** — quality of consult depends on this
- INTAKE mentor proposal: Offload (O2) — AI proposes, CEO confirms
- **INTAKE mentor selection close: Core (C)**
- PANEL/DEBATE/DECIDE parallel agent dispatch: Offload (O1)
- Synthesis (Frame 6) drafting: Offload (O2)
- **DEBATE "What CEO Must Decide" judgment: Core (C)** — non-delegable
- **DECIDE final pick: Core (C)** — non-delegable
- **RETRO honesty (hit/miss/partial): Core (C)** — non-delegable, no sycophancy
- **ADD A3 source selection: Core (C)**
- **ADD A3.5 facet split strategy: Core (C)** if triggered
- **ADD A9 close approve: Core (C)**
- REMOVE confirm: **Core (C)** (preserving historical record)
- SUGGEST cold-start gate: Offload (O1) — auto "insufficient data"

## Why This Compounds (Naval + Workshop X Lens)

Every consultation → markdown file → Frame 6 R-section eventually filled → mentor reliability_log updated → next DECIDE weights informed by past accuracy.

Over 1 year of weekly consultations:
- 50+ markdown advice assets (replayable, searchable)
- 7 mentors × ~10-15 retros each = empirical accuracy distribution
- INTAKE clarifying questions train CEO to frame problems sharply
- DEBATE surface productive tensions that single consults can't reveal
- DECIDE creates audit trail for capital allocation decisions

**This is Munger's "lattice of mental models" turned into a queryable system.** Not just stored — actively consulted, predictions tracked, reliability proven empirically.
