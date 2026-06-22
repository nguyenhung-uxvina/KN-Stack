# Changelog

## [Unreleased] - 2026-06-13
### Added
- **`forge-fabrication` — Defense process-document output (Quy trình công nghệ TCVN)**: new reference `references/quy-trinh-cong-nghe-template.md` (11-section TCVN/defense template: doc-control + approval block, standards refs §2, per-process operation sheets / Phiếu công nghệ nguyên công §5.4 with bậc thợ + thiết bị + chế độ cắt, material norms with waste % §7, QC + VT/PT/UT + NCR §8, ATLĐ §9, packaging/handover §10, mandatory data-quality warnings §11). F0 now emits `QUY_TRINH_CONG_NGHE.md` → `/convert_md_to_docx` → DOCX when the handoff source is read-from-drawings (`helix-cad-ingest`) rather than a HELIX P3 package. Distilled from a CEO-upgraded real document (GIÁ TRƯỢT UUV). Eval +1 (FF-PROCESSDOC), 13/13.
- **`helix-cad-ingest`** (helix/) — inbound CAD reader, the mirror of `helix-cad-bridge`: reads an existing PDF + DXF drawing pair (CEO exported from any CAD app), parses 100% LOCAL (ezdxf + PyMuPDF/pdfplumber, local Tesseract OCR fallback), and emits a structured engineering record (dimensions, tolerances, GD&T flags, layers, blocks/ATTRIB, BOM rows, title-block, notes) as `cad_extract.json` + `.md` with per-value source pointers and HIGH/MED/LOW confidence. Includes an **Export Requirements** section telling the CEO how to export the pair for maximum extraction (R2013/R2018 ASCII DXF, text/dims/blocks NOT exploded, units mm 1:1, layers kept; vector PDF with selectable text, ≥300 DPI if scanned). Classification router blocks cloud OCR for MẬT (egress guard). Extraction Confidence Gate operationalizes LLM Spatial Blindness (AI never self-certifies critical dims, never invents missing values). Feeds `helix-p1-requirements`/`reverse-engineering` (design/RE) and `forge-fabrication`/`helix-p4-inspection` (process build). Skill count 231 → 232. **Field-hardened on GIÁ TRƯỢT UUV (41 DXF)**: bundled runnable scripts `ingest.py` (per-part) + `aggregate.py` (MASTER_BOM/CSV + QA rollup) + `authoritative_bom.py` (PDF-BOM override → PARTS_MASTER + FAB_ROUTING by station); new Gotchas for stale copy-pasted title-block codes (filename = reliable key, `code_in_dxf` = LOW, never auto-fix), arc-pair holes, detail-vs-nesting cross-sheet conflicts (nesting = authoritative cut-list), assembly-file mixing, Windows UTF-8. Eval 8/8 → 10/10.
- **`helix-cad-bridge`** (helix/) — cross-phase code-CAD bridge: AI writes parametric build123d/CadQuery/OpenSCAD from CEO's explicit dimensions, executes 100% LOCAL, exports STEP + render for CEO verification. Classification router (MẬT/HẠN-CHẾ/THƯỜNG) with egress guard blocks cloud/network for sensitive geometry — defense-safe alternative to SaaS CAD copilots (Leo/Zoo/Fusion). Operationalizes the LLM Spatial Blindness law (explicit params, CEO verifies render). Wired into `helix-p3-layout` (sketch→geometry), `helix-p4-drawing` (3D source), `forge-fabrication` F0 (STEP handoff gate). Static eval 7/7. POC verified end-to-end (UUV nose cone, STEP+PNG, mass 1.645 kg Al). Skill count 230 → 231.
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
