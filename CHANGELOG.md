# Changelog

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
