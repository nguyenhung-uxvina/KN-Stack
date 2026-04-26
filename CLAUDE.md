# CLAUDE.md — KN-Stack Developer Guide

> Agentic system for IPARAG vaults. Source of truth for skills, hooks, rules, evals.
> Version: 1.0.0

## Structure

```
KN-Stack/
├── skills/           ← 153 skills organized by domain (13 domains)
│   ├── bridge/       (10) — Operations skills
│   ├── forge/        (13) — Product strategy skills
│   ├── helix/        (34) — Design execution pipeline (Pahl-Beitz phases)
│   ├── galaxy/       (9)  — Knowledge management
│   ├── erp/          (6)  — ERPNext integration
│   ├── extract/      (6)  — Content extraction (social, chat)
│   ├── learn/        (3)  — Learning methodology
│   ├── guard/        (7)  — Guard rails (analyst-trap, ratio-check)
│   ├── design/       (19) — Generic design tools (bom, validate, odi)
│   ├── ops/          (15) — CEO operations (portfolio, sprint, weekly-3)
│   ├── session/      (5)  — Session management (catchup, checkpoint)
│   ├── system/       (16) — System design tools (gate0-3, decide, cld)
│   └── book/         (10) — Codebase-to-book pipeline (9-phase mega-skill)
├── hooks/            ← 3 hook scripts (SessionStart, UserPromptSubmit, Stop)
├── rules/            ← 4 vault rules (projects, galaxy, areas-helix, resources)
├── evals/            ← Eval framework (6 specs + runner)
└── docs/             ← Skill architecture docs (BRIDGE, FORGE, HELIX)
```

## Adding/Editing Skills

1. All skills use directory format: `skills/<domain>/<skillname>/SKILL.md`
2. If skill has references: `skills/<domain>/<skillname>/references/<ref>.md`
3. Edit the SKILL.md directly — no template compilation needed
4. After editing, junctions make changes immediately effective in `~/.claude/commands/`

## Naming Conventions

- Domain prefix: `bridge-`, `forge-`, `helix-`, `erp-`, `book-`, etc.
- HELIX pipeline blocks: `helix-p{phase}-{block}` (e.g., `helix-p1-preflight`)
- Book pipeline blocks: `book-{phase}` (e.g., `book-explore`, `book-write`) — orchestrator is `codebase-to-book`
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

## Git Conventions

- Feature branches: `feature/<domain>-<description>`
- Commit format: `[DOMAIN] Brief description` (e.g., `[HELIX] Add helix-p2-firmup block skill`)
- Tag releases: `v1.0.0`, `v1.1.0`, etc.
