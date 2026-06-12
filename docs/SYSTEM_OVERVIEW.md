# KN-Stack System Overview — v1.1.0 (2026-06-12)

> Current-state map of the agentic system. This is the **freshest** architecture doc.
> The per-pillar deep-dives (BRIDGE/FORGE/HELIX_Architecture.md) date from v1.0.0 (2026-04-23)
> and predate: helix P4 pipeline, forge-fabrication, book domain, mentors scale-out (26→54), tana domain.
> Trust this file for topology; trust the deep-dives only for per-pillar design rationale.

## What this system is

KN-Stack is the source of truth for **230 Claude Code skills** (15 domains) that run Workshop X
as an AI-First company: product strategy (FORGE), design execution (HELIX, Pahl-Beitz),
manufacturing (forge-fabrication → ERPNext), operations (BRIDGE, ops), knowledge management
(galaxy, IPARAG/Zettelkasten), and a 54-mentor AI advisory board.

Deployment: NTFS junctions from `~/.claude/commands/<skill>` → `D:\KN-Stack\skills\<domain>\<skill>` (`setup.sh --install/--verify/--status`).

## The closed loop (R&D → production → knowledge)

```
FORGE (what to build)
  forge-pre-study → forge-job-map (ODI) → forge-scout/shift → forge-validate → forge-portfolio
        │
        ▼
HELIX (how to build — Pahl-Beitz P1→P4, each a 6-block mega-skill pipeline)
  helix-task-clarify    = p1-preflight → requirements → validate → abstract → structure → compile
  helix-concept-generate= p2-preflight → frame → search → develop → risk → select
  helix-embody-realize  = p3-preflight → layout → integrate → dfx → bom → compile
  helix-detail-finalize = p4-preflight → drawing → bom → assembly → inspection → handoff
        │  emits Handoff_to_Fabrication.md
        ▼
FABRICATION (forge-fabrication, F0–F5)
  preflight → material → release → execute → acceptance → invoice
  (commands erp-stock / erp-production / erp-quality / erp-finance as blocks)
        │
        ▼
KNOWLEDGE (galaxy)
  galaxy-note (permanent notes) ← session-exit / tana-* (THỊNH capture)
  mentor-board (orchestrator) → 54 mentors/* skills (CONSULT/PANEL/DEBATE/DECIDE, DMIR + retro)
  codify (markdown → Python, ledger at scripts/_codify_ledger.md)
```

Quality gates: `gate0`–`gate3` (system/) enforce the 3-Gate Quality System between phases;
`helix-quality-gate` runs the in-pipeline review. Guard rails (guard/) watch CEO failure
modes: `analyst-trap`, `ratio-check` (MAKE:THINK), `physical-sprint`.

## Domains (230 skills)

| Domain | n | Role | Key entry points |
|---|---|---|---|
| helix | 40 | Pahl-Beitz design execution | helix-task-clarify, -concept-generate, -embody-realize, -detail-finalize, helix-project-init |
| mentors | 54 | Per-mentor AI advisors (NotebookLM-grounded) | via galaxy/mentor-board |
| book | 23 | Codebase↔book↔skill pipelines | codebase-to-book (book-*), book-to-codebase (btc-*), book-to-skill, notebook-to-book |
| system | 16 | Design/decision tools | gate0-3, decide, cld, archetype, leverage |
| forge | 15 | Product strategy + manufacturing | forge-pre-study, forge-job-map, forge-fabrication |
| ops | 15 | CEO operations | portfolio, sprint, weekly-3, hire-tracker, nlm |
| galaxy | 12 | Zettelkasten + mentor board + codify | galaxy-note, mentor-board, research, codify |
| bridge | 10 | Operations layer | bridge-dashboard, bridge-flywheel, bridge-knowledge-base |
| tana | 9 | THỊNH workflow capture (Tana MCP) | tana-thu/hoa/ich/nho/hanh, tana-session, tana-weekly |
| design | 8 | Specialized engineering tools | reverse-engineering, odi, sdmodel, helm-aluminum-boat |
| guard | 7 | CEO guard rails | analyst-trap, ratio-check, aigate |
| extract | 7 | Content extraction | yt-extract/yt-learn/yt-search, x/fb/linkedin/chat-extract |
| erp | 6 | ERPNext integration | erp-master/bom/production/quality/stock/finance |
| session | 5 | Session lifecycle | catchup, checkpoint, session-exit |
| learn | 3 | Learning methodology | learn-methodology/practice/track |

## Infrastructure

- **hooks/** (3): `session-briefing.sh` (SessionStart — vault health briefing), `track-skill-usage.sh` (UserPromptSubmit — MAKE/CHECK/THINK CSV), `check-learnings.sh` (Stop — daily learning reminder). All paths git-relative; deployed to the vault by `setup.sh --update`.
- **rules/** (4): vault rules for 1_Projects, 5_Galaxy, 2_Areas/HELIX, 3_Resources.
- **evals/** (9 specs + runner): runtime mode pipes test_input to `claude -p`; **static mode** audits SKILL.md directly (use for orchestrators). Covered: analyst-trap, research, helix-task-clarify, helix-concept-generate, helix-embody-realize, helix-quality-gate, forge-fabrication, mentor-board, codebase-to-book.
- **scripts/**: codified Python (Naval code leverage); registry at `_codify_ledger.md`.

## Standards (enforced 2026-06-12)

1. Every SKILL.md starts with frontmatter: `name:` (= dir name) + `description:` with "Triggers on: …" (EN + VN). 230/230 compliant.
2. References resolve relative to the skill dir; cross-skill refs use `../<skill>/references/<file>.md` (see book domain).
3. Runtime state (`_meta/`, `progress.md`) and vault artifacts (`.obsidian/`, `book/`, xlsx/docx) are gitignored — never commit them.
4. New orchestrator/mega-skill ⇒ add a static-mode eval spec.
5. Counts drift — verify with `setup.sh --status` before citing.

## Known debt (deliberate, not forgotten)

- Naming: 15 legacy helix skills don't follow `helix-p{n}-{block}` (they predate the pipeline convention; renaming would break muscle memory + junctions — revisit at v2.0).
- `btc-*` block prefix vs `book-` convention: accepted as the book-to-codebase block namespace.
- BRIDGE/FORGE/HELIX deep-dive docs are v1.0.0-era (see banner above).
- Eval coverage 9/230 — by design only orchestrators/gates get specs; blocks are exercised through their orchestrator.
- Overlap clusters to watch: research ↔ research-to-skill ↔ skill-from-research; learn-* ↔ galaxy/learning; docs/TNKCT_* project artifacts should migrate to the vault.
