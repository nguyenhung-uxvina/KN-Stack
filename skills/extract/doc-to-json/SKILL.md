---
name: doc-to-json
description: Convert a document (PDF, Markdown, Word .docx, Excel .xlsx) into a structured, fidelity-preserving JSON file — giữ nguyên thông tin. Produces one unified JSON document model with reading order, headings, paragraphs, lists, tables, code, Word run formatting, and Excel cell grids (values + formulas + merged ranges) intact. Triggers on "convert document to json", "doc to json", "document to json", "pdf to json", "word to json", "excel to json", "md to json", "chuyển tài liệu sang json", "convert sang json", "giữ nguyên thông tin", "parse document", "extract document", or when pointing at a .pdf/.md/.docx/.xlsx file to be structured.
---

# Doc → JSON — Document to Structured JSON (fidelity-preserving)

Turn any **PDF, Markdown, Word (.docx), or Excel (.xlsx)** file into a single **`<name>.json`** that preserves the document's information — reading order, structure, tables, formatting, and metadata — so nothing is lost in the conversion.

The deterministic parsing (PDF text+tables, DOCX ordered body walk, XLSX cell grid, Markdown block parse) is **codified in Python** at [parse_document.py](../../../cad-pipeline/scripts/extract/parse_document.py). This skill orchestrates that script, sanity-checks fidelity, and (optionally) curates a human view. **Never hand-transcribe content the script already recovered — read the JSON.**

This is the **general document** converter. For **engineering drawings** (title block, dimensions, GD&T from PDF/DXF/DWG) use [mech-drawing-extract](../mech-drawing-extract/SKILL.md) instead — that one knows CAD; this one preserves prose/tables/sheets.

## When to Use

- CEO/engineer drops a report, spec, memo, contract, or spreadsheet and wants it as machine-readable JSON.
- Feeding documents into downstream skills (`bridge-knowledge-base`, `bridge-signal-extract`, `chat-extract`, Galaxy) that want structured input, not raw files.
- Archiving documents into the vault as a recoverable, diff-able, grep-able JSON record.
- Migrating mixed-format docs (PDF + Word + Excel) into **one consistent schema**.

## Input

```bash
python cad-pipeline/scripts/extract/parse_document.py --in <file> [--out <dir>] [--name <slug>] [--text]
```

- `--in` — the source file. Format is auto-detected by extension: `.pdf`, `.md`/`.markdown`, `.docx`, `.xlsx`.
- `--out` — output directory (default cwd). Pass the project's folder, e.g. `1_Projects/<project>/extracted/`.
- `--name` — output slug (default: kebab-cased filename). Produces `<name>.json`.
- `--text` — also write `<name>.txt`, a plain full-text dump (handy for quick grep / diff; not the deliverable).

**Legacy formats:** `.doc` and `.xls` are **not** supported — the script exits 2 and tells you to **Save As** the modern format (`.docx` / `.xlsx`) first. (Binary `.doc`/`.xls` have no reliable open parser; converting in Office is the faithful path.)

**Dependencies** (install once if the script reports them missing, exit 3):
```bash
pip install pdfplumber       # PDF
pip install python-docx      # Word .docx
pip install openpyxl         # Excel .xlsx
# Markdown needs nothing — pure-Python parser.
```
Each dependency is needed only for its own format; a missing one fails only that format.

## Workflow

### Step 1 — Identify the file & intended name

Confirm the path and a sensible output slug (kebab-case). If converting a set, decide the output folder once and reuse it.

### Step 2 — Run the parser (codified, COD: Offload)

```bash
python cad-pipeline/scripts/extract/parse_document.py --in report.pdf --out extracted/ --name q2-report
```

The script writes `<name>.json` and prints a one-line summary (block counts, or sheet/cell/formula counts for Excel) plus a warning count.

### Step 3 — Read the JSON & verify fidelity (COD: Core)

Read `<name>.json`. It is a **unified envelope**:

| Field | Meaning |
|-------|---------|
| `source` | path, filename, format, byte size, **sha256** (traceability / tamper check) |
| `metadata` | document properties — title/author/created/modified; Markdown frontmatter; Office core props |
| `blocks` | **reading-order stream** for PDF/MD/DOCX (see block types below) |
| `sheets` | spreadsheet grids for XLSX (see sheet shape below) |
| `pages` | per-page geometry + char/table counts (PDF only) |
| `pdf_quality` | scanned / mojibake / encoding flags (PDF only) |
| `text` | full plain-text dump for quick grep |
| `stats` | block/type counts, or sheet/cell/formula totals |
| `warnings` | anything the parser could not faithfully map — **always read these** |

**Block types** (`blocks[]`): `heading` (`level` 0–6), `paragraph` (PDF/MD carry `page`/`text`; DOCX may carry `runs` with bold/italic/underline and a `style`), `list` (`ordered`, `items[].level` for nesting), `list_item` (DOCX list-styled paragraphs), `table` (`header`, `rows`, `n_rows`, `n_cols`, and — for DOCX — `merged_cells`; see Word notes), `code` (`lang`, `text`), `blockquote`, `rule`, `pagebreak` (PDF page boundary).

**Sheet shape** (`sheets[]`): `name`, `dimensions`, `n_rows`, `n_cols`, `state` (visible/hidden), `merged_cells` (range strings), `grid` (2-D values), and `cells` (every non-empty cell with `ref`, `row`, `col`, `type`, `value`, and — for formula cells — `formula` plus the cached `value`, and `number_format` when non-default).

**Fidelity check (do this every time):**
- Skim `warnings`. A non-empty list means information may have been dropped or is unreliable — surface it, don't bury it.
- Cross-check `stats` against the source: does the block/sheet/cell count look complete? A 40-page PDF yielding 3 blocks means the text layer is thin (likely scanned).
- Spot-check one table and one heading against the original to confirm structure survived.

### Step 4 — Report & route

Summarize: format, block/sheet counts, tables found, any warnings/open items. Then route the JSON to whatever needs it (`bridge-knowledge-base`, `bridge-signal-extract`, Galaxy, or a downstream analysis). Only write a curated `.md` view if the user asks — the JSON is the deliverable.

## Format-Specific Notes & Traps

**PDF**
- `pdfplumber` recovers text + tables from PDFs that have a **text layer**. **Scanned / image-only PDFs** have none — the parser sets `pdf_quality.scanned_no_text_layer` and warns. OCR is out of scope: read the PDF visually with the Read tool (it renders pages as images).
- **Legacy-font mojibake** (TCVN3/VNI Vietnamese PDFs) yields garbled text — `pdf_quality.encoding_warning` flags a high replacement-char ratio. Don't trust that text; read visually. (For CAD drawings with this problem, `mech-drawing-extract` decodes TCVN3 from the DXF — but that is drawing-specific.)
- Table detection is heuristic; verify any table that feeds a decision against the source page.

**Markdown**
- YAML frontmatter (`--- … ---`) is split into `metadata.frontmatter_raw` + a **naive flat** `metadata.frontmatter` (no external YAML dep — nested/list values are kept as raw strings; the raw block is always preserved for lossless recovery).
- Inline markup inside paragraphs (`**bold**`, links) is kept **as literal Markdown text** in `text` — structure (headings/lists/tables/code) is parsed; inline styling is preserved verbatim, not tokenized.

**Word (.docx)**
- The body is walked in **XML document order**, so paragraphs and tables stay correctly interleaved (reading order preserved).
- Heading level comes from the paragraph **style** (`Heading 1` → level 1; `Title` → level 0). Run-level **bold/italic/underline** is captured under `runs` when any run is styled.
- **Merged table cells** are handled at the XML level (`gridSpan` + `vMerge`): the full column geometry is kept, but a merged cell's text appears **only at its anchor** (top-left) position — spanned positions are blank — and every span is listed in the table's `merged_cells` as `R{r0}C{c0}:R{r1}C{c1}` (0-based), the same model as XLSX `merged_cells`. This is what keeps heavily-merged forms (e.g. a QTCN operation sheet) from coming out as wide grids of repeated text. (Word concatenates the originals' text into the surviving cell, so an anchor may hold newline-joined fragments.)
- Footnotes, headers/footers, comments, embedded images, and **nested tables inside a cell** are **not** extracted — if the source relies on them, note it as an open item.

**Excel (.xlsx)**
- Loaded **twice**: once with formulas (`data_only=False`) and once with Excel's **cached values** (`data_only=True`). Formula cells get both `formula` and the cached `value`; the `grid` shows the cached value where available.
- **Caveat:** if the workbook was generated programmatically and **never opened/saved in Excel**, there are no cached values — formula cells show `value: null` and the `grid` falls back to the formula string. Open + save in Excel once to populate cached values, or just rely on the `formula` field.
- Merged ranges, hidden-sheet state, and non-default number formats are preserved. Charts/pivot tables/macros are not.

## Output Contract

| File | Producer | Content |
|------|----------|---------|
| `<name>.json` | Python script | Unified document model: source+sha256, metadata, reading-order blocks (or sheet grids), pages/quality (PDF), full text, stats, warnings |
| `<name>.txt` | Script (`--text`, optional) | Plain full-text dump — for grep/diff, not the deliverable |
| `<name>.md` | This skill (only if asked) | Curated human view of the JSON |

## What the Script Recovers vs What You Interpret

| Recovered deterministically (trust it) | Interpreted by skill (judge it) |
|----------------------------------------|----------------------------------|
| Reading order, headings/levels, paragraphs, lists, tables | Whether a `warning` means real information loss |
| DOCX run formatting, styles, table merge spans; XLSX values + formulas + merged ranges | Whether a thin-text PDF needs visual reading / OCR |
| Document metadata, sha256, page geometry, full text | Whether table heuristics captured a table correctly |
| PDF scanned / mojibake / encoding flags | Where to route the JSON downstream |

## COD Classification

- Parsing PDF/MD/DOCX/XLSX → JSON: **Offload** (codified Python).
- Verifying fidelity, judging warnings, deciding visual-read vs trust: **Core** (human judgment).
- Writing the JSON file: **Default** (automate).
- Routing downstream: **Core** (CEO/engineer decides).

## Limitations

- **Scanned PDFs** and **mojibake PDFs** have no usable text layer — the parser flags both; read visually (no OCR).
- **Legacy `.doc` / `.xls`** are rejected — Save As `.docx` / `.xlsx` first.
- **DOCX**: footnotes, headers/footers, comments, tracked changes, embedded images, and nested in-cell tables are not extracted. Table merge spans are recorded (`merged_cells`) but cell-level styling (shading, borders) is not.
- **XLSX**: charts, pivot tables, and macros are out of scope; formula cells need Excel-cached values for a populated `value`.
- **Markdown**: inline markup is preserved as literal text, not tokenized; frontmatter parsing is flat (raw block always kept).
- The script reports what the bytes contain; it does **not** validate the document's correctness — that is the reviewer's job.
