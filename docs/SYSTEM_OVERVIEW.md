# KN-Stack System Overview

> Current-state map of the agentic system.
> Skill counts are deliberately absent from this file — they change on every merge and every
> hard-coded number here went stale. Run `bash setup.sh --status` for the real figures.

## What this system is

KN-Stack is the source of truth for the Claude Code skills that run Workshop X as an AI-First
company: product strategy (FORGE), design execution (HELIX, Pahl-Beitz), manufacturing
(forge-fabrication → ERPNext), operations (BRIDGE, ops), knowledge management (galaxy,
IPARAG/Zettelkasten), and an AI mentor board.

Deployment: NTFS junctions from `~/.claude/commands/<skill>` → `D:\KN-Stack\skills\<domain>\<skill>`
(`setup.sh --install/--verify/--status`). The working tree IS the runtime: switching branch,
stashing or resetting in `D:\KN-Stack` changes what every session loads.

## The closed loop (R&D → production → knowledge)

```
FORGE (what to build)
  forge-pre-study → forge-job-map (ODI) → forge-scout/shift → forge-validate → forge-portfolio
        │
        ▼
HELIX (how to build — Pahl-Beitz P1→P4; each phase skill is an orchestrator that delegates to blocks)
  helix-task-clarify    = p1-preflight → requirements → validate → abstract → structure → compile
  helix-concept-generate= p2-preflight → frame → search → develop → risk → select
  helix-embody-realize  = p3-preflight → form (BF) → layout → integrate → dfx → bom → compile
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
  mentor-board (orchestrator) → mentors/* skills (CONSULT/PANEL/DEBATE/DECIDE, DMIR + retro)
  codify (markdown → Python, ledger at scripts/_codify_ledger.md)
```

Quality gates: `helix-quality-gate` is the gate every HELIX phase skill and block points to
(Gates 1–4). `gate0` (system/) is the only Phase-0 gate. `gate1`–`gate3` (system/) are older
standalone scorecards that no HELIX skill calls and whose thresholds differ — see Known debt.
Guard rails (guard/) watch CEO failure modes: `analyst-trap`, `physical-sprint`.

## Domains

| Domain | Role | Key entry points |
|---|---|---|
| helix | Pahl-Beitz design execution, CAD chain, C&C² | helix-task-clarify, -concept-generate, -embody-realize, -detail-finalize, helix-project-init, helix-quality-gate |
| mentors | Per-mentor AI advisors (NotebookLM-grounded) | via galaxy/mentor-board |
| book | Codebase↔book↔skill pipelines | codebase-to-book (book-*), book-to-codebase (btc-*), book-to-skill, notebook-to-book, book-to-book |
| system | Decision and systems-thinking tools, legacy gates | gate0, decide, cycle, constraint, cld, archetype, leverage |
| forge | Product strategy + manufacturing | forge-pre-study, forge-job-map, forge-shift, forge-fabrication |
| ops | CEO operations | portfolio, risk, sprint, weekly-3, nlm |
| galaxy | Zettelkasten + mentor board + codify | galaxy-note, mentor-board, research, codify |
| bridge | Operations layer | bridge-judgment, bridge-knowledge-base, bridge-signal-extract |
| tana | THỊNH workflow capture (needs the Tana MCP server) | tana-thu/hoa/ich/nho/hanh, tana-session, tana-weekly |
| design | Specialized engineering tools | reverse-engineering, odi, sdmodel, helm-aluminum-boat |
| guard | CEO guard rails | analyst-trap, aigate, qc |
| extract | Content extraction | yt-learn, yt-search, chat-extract |
| erp | ERPNext integration (needs the ERPNext MCP server) | erp-master/bom/production/quality/stock/finance |
| session | Session lifecycle | catchup, checkpoint, session-exit |
| learn | Learning methodology | learn-methodology/practice/teach/track |

## Infrastructure

- **rules/** (4): vault rules for 1_Projects, 5_Galaxy, 2_Areas/HELIX, 3_Resources; copied to the vault by `setup.sh --update`.
- **evals/** (specs + runner): runtime mode pipes test_input to `claude -p`; **static mode** audits SKILL.md directly (use for orchestrators).
- **scripts/**: codified Python (Naval code leverage); registry at `_codify_ledger.md`.
- **plugins/**, **mcp/**: self-contained plugins and local MCP servers.

## Standards

1. Every SKILL.md starts with frontmatter: `name:` (= dir name) + `description:` with "Triggers on: …" (EN + VN).
2. References resolve relative to the skill dir; cross-skill refs use `../<skill>/references/<file>.md` (see book domain).
3. Runtime state (`_meta/`, `progress.md`) and vault artifacts (`.obsidian/`, `book/`, xls/xlsx/docx) are gitignored — never commit them.
4. New orchestrator/mega-skill ⇒ add a static-mode eval spec.
5. A skill that names a tool, file or sibling skill must name one that exists. The 2026-11-15 audit removed 16 skills, most of them for pointing at things that were never there.

## Known debt (measured 2026-11-15, not yet resolved)

- **Threshold drift across layers.** Requirement count is ">= 40" in helix-quality-gate Gate 1 but "50-80" in helix-task-clarify and helix-p1-requirements. Quantification is ">=80%" (FAIL below 60%) in system/gate1. One concept, several numbers; none cites a source.
- **Two folder names for one phase.** Skills write both `Phase3-Embody/` and `Phase3-Embodiment/`, and the vault holds both. Fixing it needs a naming decision plus a vault rename.
- **Two ODI scales.** forge-job-map scores opportunity with cut-offs at 8.0 / 6.0 / 4.0; design/odi uses Ulwick's > 15 / 12–15 / 10–12. Vault artifacts exist in both.
- **system/gate1–gate3 vs helix-quality-gate.** Same gates, different checks and pass marks; only helix-quality-gate is wired into the pipeline.
- **Phase orchestrators restate their blocks.** The four phase skills repeat each block's output contract in a "Data Bus" table that has drifted from the blocks (file names, variant prefixes). The blocks are what runs; the tables are the copy.
- **Naming:** legacy helix skills don't follow `helix-p{n}-{block}`; `btc-*` is accepted as the book-to-codebase block namespace.
- **Overlap clusters still open:** research-to-skill ↔ skill-from-research; learn-* ↔ galaxy/learning; ops/portfolio ↔ forge-portfolio; session/journal ↔ helix-design-journal ↔ ops/teach.
