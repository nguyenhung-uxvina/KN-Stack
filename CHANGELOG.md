# Changelog

## [Unreleased] - 2026-06-13
### Added
- **Exa semantic source discovery ("Channel 0")** across NLM discovery pipelines, encoded once in `skills/galaxy/research/references/exa-discovery.md`. Augment + fallback: Exa preferred when the Exa MCP/Connector is available; WebSearch/yt-dlp fallback otherwise; `--no-exa` escape; free-tier 429 guard. Touched: `/research` (→ v4.1), `source-tiers.md`, `mentor-board` (A2), `learning` (Step 1), `yt-search`, `yt-learn`.

## v1.1.0 — 2026-06-12

System grows 143 → 230 skills (15 domains). Full-system audit + hygiene pass.

### Added
- **book/** domain expanded to 23 skills: `book-to-codebase` reverse pipeline (orchestrator + 10 `btc-*` blocks), `book-to-skill`, `notebook-to-book` (NotebookLM-driven P1 adapter)
- **mentors/** domain scaled 26 → 54 mentor advisor skills (councils: torpedo-asw, naval-hydraulics, steel-marine-fabrication, nswc-hull, al-build, ukrainian-uas-defense; individuals: chris-brose, palmer-luckey, stanley-mcchrystal, peter-thiel, hyman-rickover, danny-gold, …)
- **tana/** domain (9 skills): THỊNH workflow capture — `tana-thu/hoa/ich/nho/hanh`, `tana-cod`, `tana-galaxy`, `tana-session`, `tana-weekly`
- **helix/** P4 pipeline blocks: `helix-p4-preflight/-drawing/-bom/-assembly/-inspection/-handoff` (P1–P4 now all 6-block mega-skill pipelines)
- **forge/**: `forge-fabrication` mega-skill (F0–F5 manufacturing pipeline, closes R&D → production loop), `forge-proposal-khcn`
- **galaxy/**: `mentor-board` orchestrator, `codify` (markdown → Python leverage), `skill-to-public`
- **extract/**: `yt-learn` (deep 9-query learning pipeline)
- **scripts/** directory with `_codify_ledger.md` (append-only markdown→Python registry)
- Evals: static-mode for orchestrator skills (`helix-task-clarify`, `helix-concept-generate`, `helix-embody-realize`); runner path fix
- `setup.sh`: `shopt -s nullglob` guard for empty domain globs

### Changed
- **design/** consolidated: 11 overlapping skills (6flow, arch, bom, fallback, icd, lcc, opp, outcomes, seg, shift, validate) merged into helix/forge (2026-05-11); 8 specialized tools remain
- `helix-detail-finalize` refactored (+614 lines, emits Handoff_to_Fabrication.md)
- `forge-validate` + `forge-trust` upgraded with TradingAgents patterns
- `design/odi` expanded to full ODI methodology (426 lines)

### Fixed (v1.1.0 hygiene pass, 2026-06-12)
- 71 SKILL.md files missing YAML frontmatter (name + description with trigger phrases) — frontmatter is now mandatory per CLAUDE.md
- CLAUDE.md drift: counts corrected 165 → 230 skills, 14 → 15 domains (tana was undocumented; mentors 26 → 54; book 10 → 23)
- Removed malformed `D:Workshop_X/` directory at repo root (U+F03A path-encoding artifact from an old hook deploy)
- `.gitignore` extended: `_meta/`, `progress.md`, `.obsidian/`, `book/`, `*.xlsx`, `*.docx` (runtime/vault artifacts out of source control)
- Dangling `references/` paths in book-domain block skills
- `yt-extract-short` orphan in `~/.claude/commands/` (real dir with no KN-Stack source) brought under source control + junction

## v1.0.0 — 2026-04-23

Initial extraction of agentic system from Workshop X IPARAG vault.

- 143 skills organized into 12 domains: bridge (10), forge (13), helix (34), galaxy (9), erp (6), extract (6), learn (3), guard (7), design (19), ops (15), session (5), system (16)
- 72 flat .md skills converted to directory format (skillname/SKILL.md)
- 3 hook scripts (SessionStart, UserPromptSubmit, Stop)
- 4 vault rules (projects, galaxy, areas-helix, resources)
- 6 eval specs + runner
- 3 skill architecture docs (BRIDGE, FORGE, HELIX)
- setup.sh with --install, --update, --verify, --unlink, --status modes
- CLAUDE.md split: agentic rules → global CLAUDE.md, vault state stays in vault
- ETHOS.md with Workshop X core philosophy
- Junction-based deployment via PowerShell (Windows compatible, no admin required)
