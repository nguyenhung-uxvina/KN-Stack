# CLAUDE.md — KN-Stack Developer Guide

> Agentic system for IPARAG vaults. Source of truth for skills, hooks, rules, evals.
> Version: 1.2.0

## Structure

```
KN-Stack/
├── skills/           ← 249 skills organized by domain (15 domains)
│   ├── bridge/       (10) — Operations skills
│   ├── forge/        (15) — Product strategy skills (+ forge-fabrication mega-skill: 6-block manufacturing pipeline F0-F5
│   │                       — closes R&D → production loop via Handoff_to_Fabrication.md from helix-detail-finalize;
│   │                       + forge-proposal-khcn for KHCN proposal drafting)
│   ├── helix/        (55) — Design execution pipeline (Pahl-Beitz phases — P1/P2/P3/P4 all 6-block mega-skill pipelines; CAD chain: helix-cad-bridge code→CAD, helix-cad-ingest CAD→info, helix-cad-validate design-rule Computational Sensor+Gate, helix-cad-roundtrip orchestrates across P1-P4 with human-draw import, helix-cad-nest geometry→cut-plan/nesting, helix-cad-to-fab drawing-folder→fab bundle; Spec-to-CAD: helix-spec-to-cad SDD orchestrator + 6 helix-s2c-* blocks — spec-kit methodology as disciplined Flow-B front-end)
│   ├── galaxy/       (12) — Knowledge management (+ skill-to-public, codify, mentor-board — Naval outbound + code + mentor leverage)
│   ├── mentors/      (58, dynamic) — Per-mentor advisor skills (add more via /mentor-board --add <leader>); orchestrator at galaxy/mentor-board/
│   ├── book/         (23) — Book pipelines: codebase-to-book (9-phase, book-* blocks), book-to-codebase (btc-* blocks), book-to-skill, notebook-to-book
│   ├── erp/          (6)  — ERPNext integration
│   ├── extract/      (7)  — Content extraction (social, chat, yt-extract/yt-learn/yt-search)
│   ├── learn/        (3)  — Learning methodology
│   ├── guard/        (7)  — Guard rails (analyst-trap, ratio-check)
│   ├── design/       (8)  — Specialized tools only (odi, opt, wp, verify, reverse-engineering, reverse-mc, sdmodel, helm-aluminum-boat) — 11 overlapping skills merged into helix/forge on 2026-05-11
│   ├── ops/          (15) — CEO operations (portfolio, sprint, weekly-3)
│   ├── session/      (5)  — Session management (catchup, checkpoint)
│   ├── system/       (16) — System design tools (gate0-3, decide, cld)
│   └── tana/         (9)  — Tana integration (THỊNH workflow capture: tana-thu/hoa/ich/nho/hanh, tana-session, tana-weekly)
├── scripts/          ← Python scripts codified from skills (Naval code leverage)
│   └── _codify_ledger.md  (append-only registry of markdown→Python conversions)
├── hooks/            ← 3 hook scripts (SessionStart, UserPromptSubmit, Stop)
├── rules/            ← 4 vault rules (projects, galaxy, areas-helix, resources)
├── evals/            ← Eval framework (specs + runner; static-mode for orchestrator skills)
└── docs/             ← Skill architecture docs (BRIDGE, FORGE, HELIX) + SYSTEM_OVERVIEW.md (current-state map)
```

> Skill counts above are maintained manually — verify with `bash setup.sh --status` (or `find skills -name SKILL.md | wc -l`) before citing them.

## Adding/Editing Skills

1. All skills use directory format: `skills/<domain>/<skillname>/SKILL.md`
2. If skill has references: `skills/<domain>/<skillname>/references/<ref>.md`
3. Edit the SKILL.md directly — no template compilation needed
4. After editing, junctions make changes immediately effective in `~/.claude/commands/`
5. Every SKILL.md MUST start with YAML frontmatter: `name:` (= directory name) and `description:` (what it does + "Triggers on: …" phrases, English + Vietnamese). The description drives AI skill routing — no generic filler.

## Naming Conventions

- Domain prefix: `bridge-`, `forge-`, `helix-`, `erp-`, `book-`, `tana-`, `mentor-`, etc.
- HELIX pipeline blocks: `helix-p{phase}-{block}` (e.g., `helix-p1-preflight`)
- Book pipeline blocks: `book-{phase}` (e.g., `book-explore`, `book-write`) — orchestrator is `codebase-to-book`; reverse pipeline blocks are `btc-{step}` — orchestrator is `book-to-codebase`
- Mentor skills: `mentor-<kebab-name>` (e.g., `mentor-palmer-luckey`) — created via `/mentor-board --add`
- Guard rails: descriptive name without prefix (e.g., `analyst-trap`, `ratio-check`)
- Skill file: always `SKILL.md` (uppercase)

## Deployment

```bash
# Install: create junctions from ~/.claude/commands/ to KN-Stack
bash setup.sh --install /path/to/vault

# Update: re-copy hooks and rules to vault
bash setup.sh --update /path/to/vault

# Verify: check all junctions resolve correctly
bash setup.sh --verify

# Status: skill counts by domain + deployment summary
bash setup.sh --status

# Unlink: remove all junctions (restore from backup)
bash setup.sh --unlink
```

## Evals

```bash
# Run a single eval
bash evals/run-eval.sh analyst-trap

# Run with auto-improve
bash evals/run-eval.sh helix-task-clarify --improve
```

- Spec format: `evals/<skill-name>.json` with `mode: "runtime"` (pipes test_input to `claude -p`) or `mode: "static"` (audits SKILL.md directly — use for orchestrator/multi-block pipeline skills that can't produce full deliverables in one shot).
- When adding a significant skill (orchestrator, mega-skill, gate), add an eval spec alongside it.

## Git Conventions

- Feature branches: `feature/<domain>-<description>`
- Commit format: `[DOMAIN] Brief description` (e.g., `[HELIX] Add helix-p2-firmup block skill`)
- Tag releases: `v1.0.0`, `v1.1.0`, etc.
- Bump `VERSION` and add a `CHANGELOG.md` entry whenever skills are added/removed or domains change.
