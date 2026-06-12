---
name: btc-ingest
description: "Block R1 of book-to-codebase: NLM auth check, chapter index build, Apply This quick-count, and --from-pipeline artifact reuse. Outputs R1-Chapter-Index.md."
---

# BTC-Ingest — Block R1

> **Pipeline:** book-to-codebase Block R1
> **Purpose:** Initialize the BTC pipeline — verify book artifacts, build chapter index, detect Apply This density, reuse codebase-to-book artifacts if `--from-pipeline`.
> **Standalone:** `/btc-ingest <book_output_dir> [--from-pipeline]`

## Steps

### 1. NLM Auth Check
```
→ mcp__notebooklm-mcp__refresh_auth
If fail: HALT — "Run `nlm login` in terminal, then /btc-ingest ... --from R1"
If ok: proceed
```

### 2. Detect Canonical Phase
```
Check: Phase6-Revised/ (preferred) → Phase4-Chapters/ (fallback)
Warn if Phase4-only: "P4 chapters may have known issues — consider running book-revise first"
Count chapters: scan for Ch*.md files
```

### 3. Apply This Quick-Count
Scan all chapter files for regex: `/Apply This|apply this|## Apply/i`
Report: N chapters with Apply This, N without.
Do NOT extract content here — that's R2's job.

### 4. --from-pipeline Fast Path
If `--from-pipeline` flag:
```
Check each artifact exists:
  □ Phase2-Positioning.md
  □ Phase3-Outline.md
  □ Phase1-Exploration/P1_Synthesis.md
  □ Phase7-Audit-Log.md (optional — for IP context)

For each found: record path in R1-Chapter-Index.md → Fast-Path Artifacts section
For each missing: log as "absent — R3/R4 will need full CEO Core session"
```

### 5. Build Chapter Index

Write `{{btc_output_dir}}/R1-Chapter-Index.md`:

```
# Chapter Index — {{slug}}
Generated: {{date}}
Canonical phase: {{Phase6-Revised | Phase4-Chapters}}
Total chapters: {{N}}

## Chapter List
| # | File | Title (from H1) | Apply This? | Word count (estimate) |
|---|------|-----------------|-------------|----------------------|
| 01 | Ch01_... | ... | YES/NO | ~N |
...

## Apply This Summary
  Chapters with Apply This: {{N}} / {{total}}
  Quick-count estimate: ~{{N}} Apply This specs (may be undercounted — R2 will extract all)

## Fast-Path Artifacts (--from-pipeline)
  Phase2-Positioning.md: {{FOUND / ABSENT}}
  Phase3-Outline.md: {{FOUND / ABSENT}}
  P1_Synthesis.md: {{FOUND / ABSENT}}
  Phase7-Audit-Log.md: {{FOUND / ABSENT}}
```

### 6. Create/Update BTC Output Dir
```
mkdir -p {{btc_output_dir}}
mkdir -p {{btc_output_dir}}/R2-raw
mkdir -p {{btc_output_dir}}/library
```

## Output
- `R1-Chapter-Index.md` — chapter manifest + quick-count + fast-path status
- `_btc_state.md` — initialized (if not already exists)

## CEO Checkpoint
```
═══ R1 COMPLETE: BTC-Ingest ═══
Chapters: {{N}} ({{canonical_phase}})
Apply This quick-count: ~{{N}} specs across {{N}} chapters
Fast-path: {{N}}/4 artifacts found

CEO:
(1) ✅ Approve → continue R2 (btc-extract)
(2) ⚙️ Adjust (e.g., force Phase4, different output dir)
(3) ⏸️ Pause
```
