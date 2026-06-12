---
type: cross-corpus-analysis
created: 2026-05-09
scope: KN-Stack — all 257 files (165 SKILL.md + 29 reference docs + meta + rules + evals)
date_range: 2026-02-14 → 2026-04-27
analysis_lens: recurring themes + contradictions/tensions
---

# KN-Stack — Patterns & Tensions Report

A pass over the entire KN-Stack repository looking for (a) themes that recur across many files and (b) places where stated principles diverge from actual practice. The repo is ~371,000 words of markdown across 165 SKILL.md files, 13 domains, and 10 weeks of development history.

The intent is to surface things that are useful to know but easy to miss when you live inside the codebase day to day.

---

## Inventory snapshot (corrected)

The two existing inventory statements are out of date. Actual counts as of 2026-04-27:

| Source                 | Skills | Domains | Notes                                       |
|------------------------|-------:|--------:|---------------------------------------------|
| `CHANGELOG.md` v1.0.0  |   143  |     12  | Last touched 2026-04-23 — stale by 22 days  |
| `CLAUDE.md`            |   153  |     13  | Last touched 2026-04-24 — stale by 15 days  |
| **Repository today**   | **165** | **13** | book domain doubled (10 → 22) since v1.0.0 |

Per-domain breakdown today: helix 34, **book 22** (was 10), design 19, system 16, ops 15, forge 13, bridge 10, galaxy 9, guard 7, erp 6, extract 6, session 5, learn 3.

The mismatch isn't just cosmetic — `CLAUDE.md` is presented as a source of truth ("Source of truth for skills, hooks, rules, evals"), and other docs may be referencing those numbers.

---

## Recurring themes

### Theme 1 — "Pipeline with explicit CEO checkpoints" is the dominant structural template

The newer skills are not freeform documents; they are nearly identical templates wrapping a discrete pipeline block. Same shape:

- A frontmatter description naming the parent pipeline and block ID (e.g., "Block R8 of book-to-codebase")
- A `Prerequisites` section listing files the block expects to find
- Numbered `Steps` (typically 4–6)
- An `Output` list of files the block produces
- A closing `CEO Checkpoint` rendering a 3- or 4-option menu

Examples:

- `book/btc-validate/SKILL.md` ends with `(1) ✅ Approve  (2) 🔧 Fix Red skills  (3) 🗑️ Remove Red skill  (4) ⏸️ Pause`
- `book/btc-scaffold/SKILL.md` uses the same 3-option menu plus an extra mid-block "Wave 4 sample review" gate
- `book/btc-handoff/SKILL.md`, `book/btc-resolve/SKILL.md`, and `book/btc-wire/SKILL.md` all close with structurally identical `═══` banners

The principle behind it sits in `ETHOS.md`: "**One Block Per Turn.** All pipeline skills: execute 1 block, STOP, wait for CEO approval. Never auto-continue through a multi-block pipeline without explicit human checkpoint."

This is the single most important convention in the repo and could probably stand to be hoisted into its own template doc that future skills can `@include` mentally rather than redrafting.

### Theme 2 — "Physical > Analytical" is enforced, not just stated

Across the repo this isn't a slogan — it's wired into automated watchdogs and demotion rules:

- `ETHOS.md`: "Prototype iterations per month must always be positive. Analysis without physical validation is the Analyst Trap."
- `guard/analyst-trap` and `guard/ratio-check` both run a 7-day git scan and trigger an alert when `analytical files > physical files × 3` (37 files mention "Analyst Trap"; 35 mention `dP/dt`).
- `rules/projects.md`: "Nếu project không có physical gate trong 30 ngày → cảnh báo: 'Project này đang chuyển sang Area mode'" — i.e., projects without an upcoming physical milestone get auto-demoted out of Project status.
- `ETHOS.md` also requires `dJ/dt > dD/dt` ("judgment improvement must outpace decision drag") — appears in 13 files.

This is one of the strongest signals in the corpus: the system is built to actively resist its own drift toward analysis-without-action.

### Theme 3 — Compound Law (BRIDGE × FORGE × HELIX) is the universal frame

The three-way multiplicative model appears in 23 files and structures all three architecture documents. Quotes:

- `docs/BRIDGE_Architecture.md`: "Nếu BRIDGE yếu → FORGE quyết định mù → HELIX thực hiện sai → waste."
- `docs/FORGE_Architecture.md`: "FORGE = WHAT products to build, WHICH ACH to apply … HELIX = HOW to execute each product's design process."
- `ETHOS.md` opens with: "Weakness in any dimension depresses all others."

It also appears as a working assumption in many skill descriptions ("Block 0 of Phase 1 pipeline …") — the framing is fully internalized.

### Theme 4 — Pahl-Beitz / VDI 2221 is the methodological backbone of HELIX (and bleeds into FORGE)

66 files mention Pahl-Beitz. The phase numbering Phase 0 → Phase 4 is reused across HELIX block IDs (`helix-p1-preflight`, `helix-p2-firmup`), gate IDs (`Gate 0` … `Gate 4`), and as orienting language in non-HELIX skills (`forge-validate` Step 0 says "HELIX Gate 4 passed").

Phase counts in markdown text: Phase 0 = 35 files, Phase 1 = 80, Phase 2 = 92, Phase 3 = 74, Phase 4 = 35. This is one of the few concepts that has truly common currency across domains.

### Theme 5 — ACH (AI-Compensates-Hardware) is the strategic spine

187 files reference ACH — by far the most-cited concept in the repo. ETHOS defines it: "use commodity hardware + AI compensation to achieve performance that would otherwise require expensive precision hardware."

It shows up not just as a label but as a decision criterion (`forge-validate` requires an "ACH thesis"; `helix-p1-preflight` reads `ACH_Assessment_v*.md` and `ACH_Opportunity_Scan_v*.md`; gates can be passed only if "ACH go/no-go" is decided).

### Theme 6 — Bilingual operation (VN ↔ EN) is intentional but uneven

39 of 165 SKILL.md files have bilingual triggers in their description block; 126 are EN-only; 0 are VN-only. The three architecture docs (`docs/BRIDGE_Architecture.md`, `docs/FORGE_Architecture.md`, `docs/HELIX_Architecture.md`) are written almost entirely in Vietnamese. The most recent skills (`book/*`, `notebook-to-book`) tend to be EN-with-VN-aliases. Older skills are inconsistent.

There's no rule about coverage. Newer additions look more English-leaning; the original substrate is Vietnamese.

---

## Tensions and contradictions

### Tension 1 — 65 skills (39%) lack a `description:` field; 73 (44%) lack a `name:` field

Only 71 of 165 SKILL.md files have YAML frontmatter at all. The other 94 are flat markdown that cannot be auto-triggered by Claude (the description block is what the agent matches against). This is a silent reliability hole.

Per-domain breakdown of missing-frontmatter skills:

| Domain   | Missing description | Of total |
|----------|--------------------:|---------:|
| design   | 17                  | of 19    |
| system   | 16                  | of 16    |
| ops      | 15                  | of 15    |
| guard    | 6                   | of 7     |
| galaxy   | 6                   | of 9     |
| session  | 5                   | of 5     |
| extract  | 1                   | of 6     |
| **Other 6 domains** | 0      |          |

The newer pipeline domains (`book`, `bridge`, `erp`, `forge`, `helix`, `learn`) are clean. The older substrate (`design`, `system`, `ops`, `session`, `guard`, `galaxy`) was never migrated.

### Tension 2 — Naming convention from `CLAUDE.md` is ignored across whole domains

`CLAUDE.md` says: "Domain prefix: `bridge-`, `forge-`, `helix-`, `erp-`, `book-`, etc." Reality:

- **system** — 16 of 16 skills are unprefixed (`gate0`, `gate1`, `cld`, `decide`, `clarify`, …).
- **ops** — 15 of 15 unprefixed (`portfolio`, `sprint`, `weekly-3`, …).
- **design** — 19 of 19 unprefixed (`bom`, `odi`, `validate`, `verify`, …).
- **session** — 4 of 5 unprefixed (`catchup`, `checkpoint`, `journal`, `reflect`).
- **galaxy** — 6 of 9 unprefixed (`research`, `learning`, `analyze`, `pipeline`, …).

The rule applies to roughly half the repo but is treated as universal in `CLAUDE.md`. Either the rule needs to be amended ("prefix required for newer pipeline domains; legacy domains exempt") or those ~60 skills need to be renamed and their dependents updated.

### Tension 3 — Multiple skills compete for the same name

Same short name appears in multiple domains:

| Short name  | Skills sharing it                                                      |
|-------------|-----------------------------------------------------------------------|
| validate    | `design/validate`, `forge/forge-validate`, `book/btc-validate`, `helix/helix-p1-validate` |
| fallback    | `design/fallback`, `forge/forge-fallback`                              |
| portfolio   | `design/portfolio`, `forge/forge-portfolio`                            |
| shift       | `design/shift`, `forge/forge-shift`                                    |
| flywheel    | `bridge/bridge-flywheel`, `forge/forge-flywheel`                       |
| bom         | `design/bom`, `erp/erp-bom`                                            |

These are not all duplicates — `forge-validate` (lab/field/monitoring infra for ACH products), `btc-validate` (book pipeline output validation), and `design/validate` (generic plan generator) are genuinely different tools. But because `design/validate` has no frontmatter and the others do, the agent will trigger `forge-validate` or `btc-validate` for ambiguous prompts and silently skip `design/validate`. The original may already be unreachable.

`helix-p1-validate` is a particularly misleading name — it's actually requirements classification (Demand/Wish), not validation in the testing sense.

### Tension 4 — "AI assists, never decides" vs auto-resolution and sane defaults

`ETHOS.md` is absolute: "**Judgment is Non-Delegable.** Design decisions, inbox triage, permanent note creation = Core (COD-C). AI assists, never decides."

But the pipelines have several places where the AI does decide:

- `book/btc-resolve/SKILL.md` Step 2: "Apply Auto-Resolution Rules AR-1 through AR-7" — and Step 5: "For each skipped question: apply sane default … write to Section C." When the CEO doesn't answer, the AI decides.
- `book/btc-scaffold/SKILL.md` Wave 4: skills generated using sane defaults proceed without per-skill CEO sign-off (only one bulk approval at the wave gate).
- `progress.md` records a real-world consequence: P7 (write-time IP audit) found `15 SAFE / 0 issues`, P9 (read-time IP audit on the same book content) found `7 SAFE / 5 REVIEW / 3 SENSITIVE`. Two AI judgments on the same artifact contradicted each other and the conflict had to be flagged to the CEO for resolution.

The practice (delegate low-stakes / aggregate high-stakes) is reasonable. The tension is that ETHOS doesn't acknowledge a hierarchy. A better framing: "Judgment is non-delegable for class X decisions; AI may decide class Y under sane-default rules logged in Section C." Right now the gap between principle and practice is implicit and a future contributor will have to reverse-engineer it.

### Tension 5 — Same concept, different names

The "don't act outside your defined boundary" idea has at least three names:

- "Iron Law" — appears in 1 file (`forge-validate`): "IRON LAW: No validation plan is designed for an unready product."
- "Operational Envelope" / "envelope law" — appears in 28 files (cited as `[[Operational Envelope Law]]` source: Multi-Agent Research 2026-04-22).
- "Guard Rail" / "guard rail" — appears in 6 files; instantiated as the `guard/` skill domain.

All three express the same underlying logic (define DO/DON'T, halt if outside). They aren't cross-referenced; the Iron Law citation in `forge-validate` doesn't acknowledge that the same idea is called something else 28 files away. Pick one name, retire the others (or formally distinguish their scopes).

### Tension 6 — Pahl-Beitz "Phase N" vs HELIX "Gate N" terminology drift

Both are used heavily and they correspond, but different files prefer different framing:

- "Phase 0–4" appears 316 times across 92 files (peak).
- "Gate 0–4" appears 85 times across 21 files (peak).
- The `system/` domain has skill names `gate0`, `gate1`, `gate2`, `gate3` (lowercased, no prefix) — competing with the prose-level "Gate 0" / "Gate 1".

Are gates a thing inside phases, or are they synonymous with phase boundaries? `helix-p1-preflight` references "Gate 0 PASS" as a Phase 0 completion criterion, suggesting gate ⊂ phase, but the relationship isn't documented anywhere central.

### Tension 7 — `CHANGELOG.md` has been frozen for 16 days of heavy development

CHANGELOG stops at v1.0.0 (2026-04-23). Since then `progress.md` records:

- The full `book-to-codebase` pipeline R1–R9 (12+ new skills)
- The `notebook-to-book` skill (NLM-first variant)
- `helix-p1-preflight` expansion to read FORGE outputs
- `forge-validate` THESIS mode + Iron Law guard rails
- TradingAgents BTC pipeline R1–R4 (paused at R5)
- A pending feature branch `feature/evals-static-mode`

None of this is in CHANGELOG. The "Unreleased" pattern would help here, or per-week dated entries.

### Tension 8 — `progress.md` carries two unresolved blockers

Both are explicitly logged but easy to miss because the file gets overwritten every session:

- **CEO P9 approval pending** for the Finding Alphas book pipeline — `Phase9-CEO-Insights.md` has 16 action items, 5 HIGH priority, no decision.
- **P7 vs P9 IP rating conflict** — three chapters (Ch05, Ch08, Ch12) are flagged SENSITIVE by P9 NLM but SAFE by P7 write-time check. Decision required before external sharing.

These should arguably live somewhere more durable than the rolling session checkpoint (e.g., `_pipeline_state.md` or a project-level `Backlog.md`), since `progress.md` will be replaced the next time `/checkpoint` runs.

---

## Quick wins (if you want a punch list)

1. **Update `CLAUDE.md` and `CHANGELOG.md` skill counts** (165 / 22 in book domain). Add a "last-verified" date so future drift is visible.
2. **Add YAML frontmatter to the 65 skills that lack `description:`.** Without it the agent can't auto-trigger them. The `design/`, `system/`, and `ops/` domains are the bulk of this.
3. **Resolve the `validate` collision** — either rename `design/validate` → `design-validate` (and make it discoverable) or formally retire it in favour of `forge-validate` / `btc-validate`. Document which is canonical when.
4. **Pick one name for the boundary rule** (Iron Law / Operational Envelope / Guard Rail). The 6-file `guard/` domain suggests "Guard Rail" already won by adoption.
5. **Hoist "One Block Per Turn" + the CEO checkpoint template** into a single `docs/PIPELINE_BLOCK_TEMPLATE.md` so new pipeline skills can reference one source.
6. **Add a "Decisions AI may make on its own" section to `ETHOS.md`** — even a 3-line addendum acknowledging the auto-resolve / sane-defaults pattern would close the principle-vs-practice gap.
7. **Move unresolved P9 / IP-conflict items** out of `progress.md` and into `Backlog.md` or `_pipeline_state.md` so they survive the next session checkpoint.

---

## Method

Inventory and frequency counts via `find` + `grep` over `D:\KN-Stack`, excluding `.git`. Sampled the 8 most recently modified SKILL.md files and the 3 architecture docs in full; spot-checked guard, ops, session, system, and rules for breadth. Term-frequency scans on conceptual vocabulary ("Compound Law", "Pahl-Beitz", "ACH", "dP/dt", "Iron Law", etc.) used to estimate concept reach across the corpus. Naming-convention and frontmatter audits done programmatically over all 165 SKILL.md files.

Limits: I read ~12 files in full; most of the rest were inspected via grep+head. Specific quotes in this report are verified; broader claims about a domain's character (e.g., "design/ has many small stubs") are pattern-level and merit a deeper read before acting on them.
