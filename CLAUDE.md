# CLAUDE.md — KN-Stack Developer Guide

> Agentic system for IPARAG vaults. Source of truth for skills, hooks, rules, evals.
> Version: 1.0.0

## Structure

```
KN-Stack/
├── skills/           ← 182 skills organized by domain (14 domains)
│   ├── bridge/       (10) — Operations skills
│   ├── forge/        (14) — Product strategy skills (+ forge-fabrication mega-skill: 6-block manufacturing pipeline F0-F5)
│   │                       — closes R&D → production loop via Handoff_to_Fabrication.md from helix-detail-finalize
│   ├── helix/        (42) — Design execution pipeline (Pahl-Beitz phases — P1/P2/P3/P4 all now 6-block mega-skill pipelines)
│   │                       + product-dossier: orchestrator từ thư mục PDF/DXF/DWG → CEO chọn xuất QTCN / ĐMKTKT / Sổ tay QLCL… (data-spine pipeline; qtcn.json là xương sống)
│   ├── galaxy/       (11) — Knowledge management (+ skill-to-public, codify, mentor-board — Naval outbound + code + mentor leverage)
│   ├── mentors/      (13) — Per-mentor advisor skills (13 mentors live; add more via /mentor-board --add <leader>); orchestrator at galaxy/mentor-board/
│   ├── erp/          (6)  — ERPNext integration
│   ├── extract/      (9)  — Content extraction (social, chat, CAD: mech-drawing-extract "cad-to-json", doc-to-json, yt-learn)
│   ├── learn/        (3)  — Learning methodology
│   ├── guard/        (7)  — Guard rails (analyst-trap, ratio-check)
│   ├── design/       (9)  — Specialized tools only (opt, wp, verify, reverse-engineering, reverse-mc, sdmodel, helm-aluminum-boat) — 12 overlapping skills merged into helix/forge on 2026-05-11
│   ├── ops/          (15) — CEO operations (portfolio, sprint, weekly-3)
│   ├── session/      (5)  — Session management (catchup, checkpoint)
│   ├── system/       (16) — System design tools (gate0-3, decide, cld)
│   └── book/         (22) — Codebase-to-book + book-to-codebase pipelines (btc-* blocks)
├── scripts/          ← Python scripts codified from skills (Naval code leverage)
│   └── _codify_ledger.md  (append-only registry of markdown→Python conversions)
├── leo-ai/           ← Claude Code plugin: getleo.ai toolkit (4 skills + MCP leo-bridge 6 tools, gate MẬT denylist)
│                       CANONICAL copy (build.sh is legacy); installed via junction ~/.claude/skills/leo-ai → repo
│  (CAD pipeline:     TÁCH RA REPO ĐỘC LẬP D:\WX-Pipeline từ 2026-07-17 — CAD → 5 đầu ra,
│                      harness 3 tầng, kiến trúc core/contract/shell. Đọc D:\WX-Pipeline\README.md
│                      + docs\ARCHITECTURE.md trước khi sửa; tag vX.Y.Z; các skill qtcn/
│                      product-dossier/aigate/doc-to-json/mech-drawing-extract trỏ sang đó)
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
