---
name: mech-drawing-extract
description: Extract detailed mechanical part information from engineering drawings supplied as PDF, DXF and/or DWG, then save a structured JSON dataset plus a curated Markdown datasheet. Pulls title block, dimensions, tolerances, GD&T, ISO fits, threads, surface finish, material, layers, and entity inventory. Triggers on "đọc bản vẽ", "trích xuất bản vẽ", "bản vẽ cơ khí", "extract drawing", "read dxf", "read dwg", "cad to json", "parse pdf drawing", "chi tiết cơ khí", "mechanical drawing", "dxf", "dwg", "title block", or when pointing at a .pdf/.dxf/.dwg engineering drawing.
---

# Mech Drawing Extract — Engineering Drawing → JSON + MD

Turn a mechanical part drawing (PDF and/or DXF) into two artifacts:
1. **`<name>.json`** — complete machine-recoverable dataset (source of truth, feeds tools/BOM/RE).
2. **`<name>.md`** — curated human datasheet (title block, dimension table, GD&T, confidence flags).

The deterministic parsing (DXF entity walk, PDF word/table extraction, regex spec mining) is **codified in Python** at [parse_mech_drawing.py](../../../D:/WX-Pipeline/scripts/extract/parse_mech_drawing.py). This skill orchestrates that script, then interprets its JSON into a clean datasheet. **Never hand-transcribe geometry the script already recovered** — read the JSON.

## When to Use

- CEO/engineer drops a part drawing (`.pdf`, `.dxf`, or both for the same part) and wants structured specs.
- Building input for `/bom`, `/verify`, `/reverse-engineering`, or `helix-detail-finalize`.
- Cataloguing legacy drawings into the vault as machine-readable records.

## Input

User provides one or more:
- `--dxf <path>` — DXF export (best for geometry, dimensions, layers — structured CAD data).
- `--dwg <path>` — native DWG. Converted to DXF in memory via the **ODA File Converter** and then walked by the identical DXF code path (output lands under `dxf` with `converted_from_dwg: true`). Requires the free converter installed (see Dependencies). Pass `--dwg` **or** `--dxf`, not both — if you already have a DXF export, prefer it (no conversion step).
- `--pdf <path>` — PDF drawing (best for title block, notes, GD&T frames, tables).

When a DXF/DWG **and** a PDF exist for the **same part**, always pass both: the CAD file gives reliable dimensions/extents, the PDF gives the title block and annotations. They cross-validate.

## Workflow

### Step 1 — Locate files & confirm part identity

Confirm the file paths and the intended part/drawing name. If the name is unclear, derive a kebab-case `--name` from the title block or filename and confirm with the user.

### Step 2 — Run the parser (codified, COD: Offload)

```bash
python D:/WX-Pipeline/scripts/extract/parse_mech_drawing.py \
  --dxf <part.dxf> --pdf <part.pdf> \
  --out <output_dir> --name <part-name>

# DWG source (auto-converted to DXF via ODA File Converter):
python D:/WX-Pipeline/scripts/extract/parse_mech_drawing.py \
  --dwg <part.dwg> --out <output_dir> --name <part-name>
```

- Provide at least one of `--dxf`, `--dwg`, or `--pdf`. `--dxf` and `--dwg` are mutually exclusive (both are the geometry source).
- Output dir defaults to cwd; pass the project's drawings folder (e.g. `1_Projects/<project>/Drawings/extracted/`).
- The script writes `<name>.json` and prints a one-line spec summary.

**Dependencies** (install once if the script reports them missing):
```bash
pip install ezdxf pdfplumber
```
- `ezdxf` — DXF/DWG geometry. `pdfplumber` — PDF only. Each is needed only for its format.
- **DWG also needs the free ODA File Converter** (ezdxf cannot read DWG natively). The script exits with code 3 and install instructions if it's missing:
  ```bash
  winget install --id ODA.ODAFileConverter   # or download from opendesign.com
  ```
  No-converter fallback: open the DWG in your CAD app, **Save As → DXF**, then pass `--dxf`.

The parser self-reports PDF text health: check `pdf.scanned_no_text_layer`, `pdf.encoding_warning`, and `pdf.text_quality_note` (also printed to stdout with a ⚠️). If either flag is true the extracted PDF text is unreliable — **read the PDF visually with the Read tool** (it renders pages as images) and use the DXF for geometry. Don't trust garbled/empty PDF text.

### Step 3 — Read the JSON & interpret

Read `<name>.json`. Map the machine output into a curated datasheet. Key sections to interpret:

- **`title_block_candidates`** (DXF + PDF) and **`pdf.tables`** — assemble the real title block: drawing no., part name, material, scale, revision, general tolerance, finish, drawn/checked/approved, weight, units. Cross-check DXF vs PDF; flag conflicts.
- **`dxf.units` / `dxf.extents`** — drawing units and overall size; sanity-check against title-block dimensions.
- **`specs_merged`** — deduplicated, cross-source:
  - `tolerances` — nominal + bilateral/symmetric tolerance (incl. those mined from DXF dimension override text, e.g. `4250±3`).
  - `diameter_fits` — **toleranced bores/shafts** like `Ø25H7`, `Ø40m6` (highest-value machining spec; uppercase letter = hole fit, lowercase = shaft fit).
  - `diameters`, `radii`, `iso_fits` (standalone grades), `threads` (M…), `chamfers` (C…), `surface_finish_ra` (Ra/Rz/Rt/Rq), `gdt_frames_detected`.
- **`dxf.dimensions`** — actual measured dimension values from DXF DIMENSION entities **plus** cleaned override `text` (the override carries the real tolerance; the geometric `measurement` may differ if the model isn't 1:1 — prefer the override, then confirm vs PDF).
- **`dxf.block_attributes` / `dxf.block_definition_text`** — title-block fields and surface-finish symbols often live inside blocks, not modelspace; the parser harvests both.
- **`dxf.layers` / `dxf.entity_counts`** — drawing structure; also a **completeness check**: compare `CIRCLE` count to the holes visible on the PDF — a big gap means the DXF geometry is incomplete (flag it, take hole positions from the PDF).
- **`pdf.pages[].lines`** — notes, general tolerances, heat treatment, special instructions.

**Confidence discipline:** the script reports what the bytes contain; assigning meaning is your job. Mark each interpreted field **High / Medium / Low** confidence. GD&T frames are detected by symbol count only — if `gdt_frames_detected > 0` but you can't reconstruct the frame (datum + tolerance + feature), say so rather than inventing values.

**⚠️ Title-block bare-number trap (esp. Vietnamese drawings).** Title blocks place adjacent unlabelled numbers in the `Khối lượng | Tỷ lệ` (Mass | Scale) cells — these arrive as free MTEXT like `25` and `1 : 10`. Do **not** map a bare number to thickness/length: a lone `25` next to a scale is almost always **mass in kg**, and the real **thickness is a dimensioned value** on the part (e.g. the `6` on a side view). Sanity-check with mass = volume × density (Al ≈ 2.66, steel ≈ 7.85 g/cm³). When DXF and PDF disagree, **the PDF title block wins** for metadata.

**⚠️ Mojibake PDFs.** Legacy Vietnamese CAD exports (TCVN3/VNI fonts) yield a garbled PDF text layer (e.g. `TǌM Cũ SȆ` for `TẤM CƠ SỞ`) — `pdfplumber` will return nonsense. Detect this (non-UTF text, replacement chars) and fall back to **reading the PDF visually** with the Read tool; treat the **DXF as the reliable automated source** and the PDF as a visual cross-check.

**✅ TCVN3 DXF text is auto-decoded.** Legacy DXF/DWG files store Vietnamese in the TCVN3 (ABC/.VnTime) charset, so ezdxf yields mojibake like `Khung xe thÐp hép` for `Khung xe thép hộp`. The parser now decodes this to clean Unicode automatically (`decode_tcvn3`), and — crucially — only touches strings carrying an unambiguous TCVN3 marker char, so a drawing that **mixes** TCVN3 (old BOM rows) with already-correct Unicode (newer title blocks) is handled correctly, leaving the clean strings intact. Check `dxf.tcvn3` (`{detected, decoded_count}`); when `detected` is true, `dxf.raw_text` holds the **decoded** text and `dxf.raw_text_original` preserves the raw mojibake for traceability. Note: the diameter symbol `Ø` is deliberately **not** remapped (its byte collides with TCVN3 `ỉ`), so `Ø100` stays intact; a genuine `ỉ` in a name is the rare cost — verify such words against the PDF.

### Step 4 — Write the curated MD datasheet

Write `<name>.md` next to the JSON, in this shape:

```markdown
# <Part Name> — Drawing Datasheet
> Source: <pdf>, <dxf> | Extracted: <date> | Drawing No: <no> | Rev: <rev>

## Title Block
| Field | Value | Confidence | Source |
|-------|-------|-----------|--------|
| Drawing No | | | DXF/PDF |
| Part Name | | | |
| Material | | | |
| General Tolerance | | | |
| Scale | | | |
| Surface Finish | | | |
| Units | | | DXF |
| Weight/Mass | | | |
| Drawn / Checked / Approved | | | |

## Overall Geometry
- Envelope (from DXF extents): W × H <units>
- Entity inventory: <n> entities across <m> layers

## Dimensions & Tolerances
| # | Nominal | Tolerance | Type | Confidence | Notes |
|---|---------|-----------|------|-----------|-------|

## Features
- Threads: <list>
- Diameters / Bores: <list>  (with ISO fits, e.g. Ø25 H7)
- Radii / Fillets: <list>

## GD&T
| Feature | Symbol | Tolerance | Datum | Confidence |
(If frames detected but unreadable, state: "N frames detected — not machine-reconstructable, verify against PDF.")

## Notes & Special Instructions
- <heat treatment, coating, general notes from PDF lines>

## Manufacturing Flags (for /bom, /verify, RE)
- <tightest tolerance, critical fits, non-standard threads, material availability concerns>

## Open / Unverified Items
- <conflicts between DXF and PDF, low-confidence reads, missing fields>
```

### Step 5 — Report & route

Summarize to the user: # dimensions, # tolerances, tightest tolerance, material, and any conflicts/open items. Offer downstream routing:
- `/bom` — if the part is one of several in an assembly.
- **`qtcn` (quy trình công nghệ)** — for a multi-part package, run the bridge [D:/WX-Pipeline/scripts/extract/extract_to_qtcn_seed.py](../../../D:/WX-Pipeline/scripts/extract/extract_to_qtcn_seed.py) `--extracted <dir>` to turn **BOM.json + per-sheet JSON** into `qtcn-seed.json` (product + VT-assigned BOM + section/plate/tolerances per part + purchased items). That seed is the **foundation** for `qtcn` (`--seed qtcn-seed.json`) and for the `product-dossier` pipeline — so the QTCN is built from the extracted JSON, not re-typed.
- `/verify` — generate the inspection/verification plan from the dimension table.
- `/reverse-engineering` — if this is RE input.
- `helix-detail-finalize` — if part of an active design's detail package.

## Multi-Part / Assembly Packages

Real drawing PDFs are often a **whole package**: a top assembly + a BOM table + many detail pages (e.g. `GT.00.00.00` assembly → `GT.00.01.00` sub-assembly → details `GT.00.01.01…10`). DXF exports usually come **one file per detail**. Handle this as a set, not a single part:

1. **Read the BOM page(s) first** — the parts list (Kí hiệu / Tên gọi / Số lượng / Vật liệu) is the index: drawing-no, name, qty, material per part. Capture it as `BOM.md` + `BOM.json`.
2. **Match DXF files to BOM rows** by drawing number (the DXF MTEXT usually carries the `GT.xx.xx.xx` code — trust that over the filename, which may be the assembly name).
3. **One datasheet per detail** — run the parser per DXF (or read each PDF detail page visually if no DXF), producing `<drawing-no>.json` + `<drawing-no>.md`.
4. **Roll up** — a package `README.md` linking the BOM and every part datasheet, plus a fits/material summary across parts (feeds `/bom`, `/verify`).

Quantities and material-per-part come from the **BOM**, not the detail title block — cross-check them.

**⚠️ Stock-length BOM lines (profiles/tube/bar).** A Vietnamese fabrication BOM line like `Khung xe thép hộp 80×40×4×6000` encodes the **stock length** as the trailing dimension (here 6000 = a 6 m bar), so its `Slg` (Số lượng) counts **how many bars**, not "1 assembly". Don't default such a line to qty 1 — read the Slg cell (e.g. `06` ⇒ 6 × 6 m = 36 m of section). Same family as the bare-number trap: a number's role depends on the column it sits in.

## Output Contract

| File | Producer | Content |
|------|----------|---------|
| `<name>.json` | Python script | Full machine dataset (title-block candidates, dimensions, layers, entities, block attributes/definitions, merged specs, PDF text-quality flags, TCVN3 decode flag + raw/decoded text, DWG-conversion flag, raw text) |
| `<name>.md` | This skill | Curated, confidence-flagged engineering datasheet |
| `<name>.raw.md` | Script (`--md`, optional) | Plain dump — starting point only, not the deliverable |
| `BOM.json` / `BOM.md` | This skill | Parts list for multi-part packages (drawing-no, name, qty, material) |
| `qtcn-seed.json` (optional) | `extract_to_qtcn_seed.py` | QTCN foundation from BOM.json + per-sheet JSON: product + VT-assigned BOM + section/plate/tolerances/key-dims per part + purchased items. Feeds `qtcn --seed` / `product-dossier` |

## What the Script Recovers vs What You Interpret

| Recovered deterministically (trust it) | Interpreted by skill (flag confidence) |
|----------------------------------------|----------------------------------------|
| DXF dimension measurements + override text, extents, units | Which dimensions are functionally critical |
| Layer list, entity counts, block attributes/definitions | Title-block field meaning (label→value mapping; mass vs thickness) |
| All text/MTEXT strings, PDF lines/tables | GD&T frame reconstruction (datum/tol/feature) |
| Regex-mined tolerances, bore-fits, threads, chamfers, Ra/Rz | Material substitution / manufacturing flags |
| PDF text-quality flags (mojibake / scanned) | Whether to trust PDF text or read it visually |

## COD Classification

- Parsing PDF/DXF → JSON: **Offload** (codified Python).
- Interpreting title block, GD&T, criticality, conflicts: **Core** (engineering judgment).
- Writing JSON file: **Default** (automate).
- Routing to BOM/verify/RE: **Core** (CEO/engineer decides).

## Limitations

- **Raster (scanned) PDFs** and **mojibake PDFs** (legacy VN fonts) have no usable text layer — the parser flags both; read visually or rely on the DXF.
- **TCVN3 DXF text** is auto-decoded to Unicode, but decoding is marker-gated and best-effort: a short word whose only diacritic is an ambiguous Latin-1 letter (e.g. `Cãc`) may be left raw rather than risk corrupting clean text, and `Ø` is never remapped. Spot-check decoded names against the drawing; `raw_text_original` holds the pre-decode text.
- **GD&T** is detected by symbol presence, not parsed into structured frames — verify against the drawing.
- **DXF geometry may be incomplete** vs the PDF (e.g. fewer holes) — use the `CIRCLE` count vs PDF as a completeness check.
- **DWG** is read by converting to DXF via the external ODA File Converter — if it is not installed the script reports it (exit 3); convert manually (Save As DXF) as a fallback. Conversion is faithful but adds a step; prefer a native DXF export when one exists.
- **3D models** (STEP/IGES/FCStd/3D-DWG): use the **FreeCAD 3D engine** [D:/WX-Pipeline/scripts/extract/freecad_extract.py](../../../D:/WX-Pipeline/scripts/extract/freecad_extract.py) (headless via `freecadcmd`) — computes **real mass** (V×ρ), bounding box, surface area, dedups the assembly container, groups instances → BOM qty, and emits the **same `qtcn-seed.json`** contract (so `qtcn --seed` / `product-dossier` are unchanged; `est_mass_kg` is real, not `[CẦN BÓC TÁCH]`). Verified on FreeCAD 1.1.1. Run with env vars (freecadcmd otherwise swallows `--file`): `FC_FILE=<part.step> FC_OUT=<dir> FC_NAME=<slug> freecadcmd freecad_extract.py`. Requires FreeCAD; DWG still needs ODA. **Engine split:** 2D (PDF/DXF text/dims/TCVN3) → `parse_mech_drawing.py`; 3D solids (mass/assembly) → `freecad_extract.py`.
- The script reports; it does not validate engineering correctness — that is the reviewer's job.

## Field-Tested Learnings (changelog)

Improvements driven by real extractions; each is now in the parser/skill above.
- **TCVN3 legacy-font auto-decode (XE XUỒNG / X-UUV/01-02-00, 2026-06):** DXF/DWG text in the TCVN3 (ABC/.VnTime) charset arrives as cp1252 mojibake (`Khung xe thÐp hép`). Added `decode_tcvn3` using the canonical TCVN3→Unicode table (validated char-for-char against the VTI drawings) → clean `Khung xe thép hộp`, `Bulong đai ốc`, `Mã gia cường`, `Xuồng triển khai và thu hồi UUV`. **Marker-gated**: only strings carrying a non-Vietnamese TCVN3 marker char are decoded, so a drawing mixing TCVN3 (old BOM) with Unicode (new title block) keeps the clean strings intact (`VIỆN KỸ THUẬT HẢI QUÂN`, `Nguyễn V.Hùng` untouched). `Ø` is excluded from the map (byte collides with `ỉ`) so `Ø100` survives. JSON gains `dxf.tcvn3 {detected, decoded_count}` and `dxf.raw_text_original`. A non-TCVN3 DXF is detected as such and passes through unchanged.
- **DWG support + AutoCAD %% codes (XE XUỒNG / X-UUV/01-02-00, Viện KT Hải quân, 2026-06):**
  - Added `--dwg` input. ezdxf cannot read DWG natively, so DWG is converted to DXF in memory via the ezdxf `odafc` addon (free ODA File Converter) and walked by the same `_walk_dxf_doc` path as a native DXF — identical JSON contract, stamped `converted_from_dwg`. Graceful exit 3 with winget/Save-As-DXF fallback when the converter is absent; auto-detects the **versioned** install folder (`ODAFileConverter <ver>`) that winget/MSI create, which ezdxf's default path misses.
  - **DTEXT `%%` control codes** are now decoded (`clean_dtext`): `%%c→Ø`, `%%d→°`, `%%p→±`, `%%%→%`, and underline/overline/strike toggles (`%%u/%%o/%%k`) stripped. Fixes a false-positive where `%%U1`…`%%U9` balloon numbers were mined as ISO fit grades `U1…U9`. (`plain_mtext()` already handled MTEXT; DTEXT needed this.)
  - **cp1252-safe stdout** — the end-of-run PDF-quality summary used a ⚠️ emoji that crashed (exit 1) on a legacy Windows console even though the JSON wrote fine; now plain ASCII `[!]`.
  - **TL-scale trap:** a detail drawn at TL 2:1 reports DXF `measurement` = 2× the labelled text — prefer the dimension **text** over the geometric measurement for scaled details (same rule as a non-1:1 model).
- **GT.00.01.01 (TẤM CƠ SỞ, Viện KT Hải quân, 2026-06):** title-block `25` was mass (kg), not thickness — added the bare-number trap caution + mass=ρ×V sanity check. PDF text was TCVN3 mojibake — added `mojibake_ratio`/`encoding_warning` detection. Tolerances lived in DXF dimension override text (`4250±3`) and surface finish (`Rz20`) inside a block definition — both now harvested. Toleranced bores (`Ø25H7`/`Ø40m6`), chamfers (`C1`, not `C45`), and shaft fits added to the spec miner.
