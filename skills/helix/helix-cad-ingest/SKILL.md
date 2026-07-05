---
name: helix-cad-ingest
description: "Inbound CAD bridge — reads an existing PDF + DXF drawing pair the CEO exported from any CAD app, parses them 100% LOCAL (ezdxf + PyMuPDF/pdfplumber, OCR fallback), and extracts a structured engineering record: dimensions, tolerances, GD&T flags, layers, blocks/attributes, BOM rows, title-block metadata, and general notes — for reuse in design (requirements/RE) and in building fabrication processes. Mirror of helix-cad-bridge (which generates CAD); this one reads CAD. Defense-safe: no geometry leaves the machine, no cloud OCR for MẬT. Triggers on: 'cad ingest', 'read dxf', 'read drawing', 'parse dxf', 'extract from pdf drawing', 'đọc bản vẽ', 'bóc tách bản vẽ', 'lấy thông tin từ cad', 'pdf dxf', 'extract dimensions', 'trích xuất kích thước', 'title block', 'BOM từ bản vẽ'."
---

# helix-cad-ingest: Inbound CAD Reader (Local, Defense-Safe)

> **Role:** Cross-phase bridge — the **inbound mirror** of [[helix-cad-bridge]]. Bridge *writes* code→CAD→STEP/PNG. This skill *reads* an existing **PDF + DXF pair** → structured engineering record.
> **Backend:** `ezdxf` (DXF geometry/semantics) + `PyMuPDF` (PDF text + vector + OCR) + `pdfplumber` (PDF tables) — all LOCAL, offline.
> **Interface out:** `cad_extract.json` (machine) + `cad_extract.md` (CEO-readable) — feeds requirements/RE and fabrication process build.
> **Why a pair, not one file:** DXF carries machine-truth geometry (exact coordinates, named entities) but no rendered layout; PDF carries the human-truth drawing (title block, notes, dimension overrides, sheet layout) but is hard to measure. Reading **both and reconciling** gives the most complete, verifiable record.

## Operational Envelope
> Source: [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]] + [[Operational Envelope Law]]

| DO | DON'T |
|----|----|
| Parse entities/text the files **actually contain** | Invent a dimension, tolerance, or note not present in the files |
| Report each value with its **source** (DXF entity handle / PDF page+bbox) | Merge PDF and DXF silently when they disagree — flag the conflict |
| Run all parsing LOCAL; OCR via local Tesseract only | Send any drawing to a cloud OCR / cloud "AI vision" for MẬT/HẠN-CHẾ |
| Flag low-confidence reads (OCR, garbled fonts, exploded text) | Claim extraction is "complete" — only CEO certifies critical dims |
| Emit machine JSON + CEO-readable MD with a confidence column | Treat a scanned/raster PDF as authoritative geometry |

**CEO Checkpoint:** CEO confirms file classification (Step 1) + certifies the critical-dimension table against the source drawing (Step 6). Both Core.

## Extraction Confidence Gate (MANDATORY)
The same [[LLM Spatial Blindness]] that stops the bridge from *inventing* geometry stops this skill from *mis-reading* it. Rules:
1. Every extracted value carries a **source pointer** and a **confidence**: `HIGH` (native DXF entity / native PDF text), `MED` (PDF↔DXF reconciled or layout-inferred), `LOW` (OCR, garbled `/ToUnicode`, exploded-to-lines text).
2. A dimension that exists **only** in a raster/OCR layer is `LOW` and **must** be CEO-confirmed before any downstream use.
3. AI **cannot self-certify** critical dimensions, tolerances, or GD&T. The DXF geometry and the CEO are the proof — not the extract reading well.
4. Missing value → AI writes `[MISSING — not in files]`, never a guess. If DXF and PDF conflict → `[CONFLICT: dxf=… pdf=…]`.

---

## EXPORT REQUIREMENTS — How CEO Must Export the Pair
> **Read this first. Configure your CAD export to these settings so the ingest gets maximum information.** Garbage export → garbage extract; this is the single biggest lever.

### DXF (the machine-truth file)
| Setting | Required | Why |
|----|----|----|
| **Version** | DXF **R2013 or R2018** (ASCII) | Preserves semantic entities (MTEXT, LWPOLYLINE, DIMENSION, HATCH, MLEADER). R12 explodes MTEXT→lines and flattens splines = semantics lost. UTF-8 native since R2007. |
| **Format** | **ASCII DXF**, not Binary, not DWG | ezdxf reads both but ASCII is inspectable/diffable in git. (DWG needs the ODA converter first.) |
| **Text** | Keep as **TEXT / MTEXT entities** — do NOT "explode text to geometry/polylines" | Exploded text = unreadable lines; you lose every label, dim value, and note. |
| **Dimensions** | Keep as **associative DIMENSION entities** — do NOT explode | Keeps measured value, tolerance, and override text as data, not as scattered lines. |
| **Blocks** | Keep **INSERT (block refs) + ATTRIB** intact — do NOT explode blocks | Title block, BOM table, weld/surface symbols ride as block attributes = clean key/value extraction. |
| **Layers** | Export **all layers, named, ON/thawed**; keep the layer scheme | Layer name is free classification (DIM / TEXT / CENTERLINE / HIDDEN / part outline). |
| **Units** | Set drawing **units = mm** and `$INSUNITS`; 1 unit = 1 mm, scale 1:1 in modelspace | Removes scale ambiguity. Note paperspace viewport scale separately. |
| **Geometry** | Prefer **LWPOLYLINE** over exploded segments; export model geometry, not just the plotted view | Connected polylines reconstruct closed profiles for area/length/nesting. |
| **Scope** | Export **modelspace** (true-scale geometry). Optionally a paperspace layout too, but label which is which. | Modelspace = real coordinates; paperspace = sheet layout at plot scale. |

### PDF (the human-truth / annotation file)
| Setting | Required | Why |
|----|----|----|
| **Type** | **Vector PDF** (print/plot to PDF or PDF/A) — NOT a scan/photo, NOT "print as image" | Vector PDF keeps a selectable text layer + vector linework → fast, exact extraction. Raster/scan forces OCR (LOW confidence). |
| **Text layer** | Ensure **searchable/selectable text** (fonts embedded with `/ToUnicode`) | If you can't select text in a viewer, the ingest can't either → OCR fallback only. Embed standard fonts (avoid exotic SHX that lose Unicode mapping). |
| **Resolution** | If a scan is unavoidable: **≥ 300 DPI**, deskewed, high contrast, grayscale/B&W | OCR accuracy collapses below 300 DPI / on skew. |
| **Content** | Include the **title block, revision table, BOM/parts list, and general notes** on the sheet | These are the fields the extract harvests for metadata + BOM. |
| **One drawing = one pair** | Same part/sheet set in **both** files, same revision | Reconciliation needs the PDF and DXF to describe the same thing at the same rev. |

> **Quick CEO checklist before export:** R2013+ ASCII DXF · text & dims & blocks NOT exploded · units mm 1:1 · layers kept · vector PDF with selectable text · title block + BOM + notes on sheet · same revision both files.

---

## Backend Setup (one-time, offline)
```
pip install ezdxf pymupdf pdfplumber          # core parsers, all local
# OCR fallback (only for scanned PDFs): Tesseract is compiled into PyMuPDF's MuPDF;
# install Tesseract language data (tessdata) locally — e.g. eng + vie. No network at runtime.
```
Library roles: **ezdxf** → DXF entities/layers/blocks/dimensions (`ezdxf.recover` for flawed files). **PyMuPDF** → PDF `get_text("dict"/"rawdict")` for positioned text+fonts, `get_drawings()` for vector linework, `get_textpage_ocr()` for scanned fallback. **pdfplumber** → table extraction (BOM / revision tables).

### Reading native DWG (source-of-truth) — ODA File Converter
DWG is the designer's native file; DXF is an export. To read DWG **directly** (defeats export drift), `ingest.py` routes `.dwg` through ezdxf's `odafc` add-on → **ODA File Converter** (free, runs LOCAL — no cloud, MẬT-safe). One-time install:
- Download **"ODA File Converter"** from opendesign.com (free account) — it is NOT on winget/choco/pip.
- Install to the default path `C:\Program Files\ODA\ODAFileConverter\` — ezdxf auto-detects it (`odafc.is_installed()`); no config needed.
- Verify: `python -c "from ezdxf.addons import odafc; print(odafc.is_installed())"` → `True`.
- Until installed, `.dwg` ingest fails fast with `[ODA-NOT-INSTALLED]` + instructions; `.dxf` always works without ODA. odafc converts DWG→DXF in a temp dir then loads — same downstream extraction.

**Bundled runners** (in this skill folder — run with `PYTHONUTF8=1`):
1. **`ingest.py`** — Steps 2/4/5 for **DXF or DWG**: `python ingest.py <file.dxf|.dwg|folder> --out <dir> --classification MẬT [--prefer dwg|dxf]` → emits `<filename>.cad_extract.json` + `.md` per part. `.dwg` is read via ODA (see above); a folder with both `<stem>.dwg` + `.dxf` ingests one per stem honoring `--prefer` (default `dwg` = native source). Keys output by **filename** (reliable), records `code_in_dxf` separately at LOW confidence (title-block codes can be stale/copy-pasted), keeps full `raw_text` so nothing is dropped, flags break-view dim overrides into `conflicts[]`. Extend `MATERIALS` for new alloys.
2. **`aggregate.py`** — `python aggregate.py <extract_dir>` → rolls all per-part JSON into `MASTER_BOM.md` + `MASTER_BOM.csv` (ERP import) + `CRITICAL_DIMS.md`, with material/process rollups and a data-quality section listing stale-code / no-code parts.
3. **`authoritative_bom.py`** — when the project's PDF parts-list/BOM page is available (the source of truth), embed the corrected master here → emits `PARTS_MASTER.md/.csv` + `FAB_ROUTING.md` (routing grouped by station). Use this to override stale title-block codes and fill material/qty/thickness the per-file heuristics miss.
4. **`dwg_dxf_diff.py`** — export-drift verifier: `python dwg_dxf_diff.py --extract <extract_dir> --dwg "<dwg_folder>" [--dwg ...] [--out report.md]`. Ingests native DWG (needs ODA) and content-diffs the union of GT codes, dim values, materials, and text tokens against the DXF-derived extract — robust to DWG-per-sheet vs DXF-per-part organisation. Verdict = part-code set identical + all DWG dims present in DXF. (DXF side needs no ODA.)

> Pipeline: `ingest.py` (read each DXF/DWG) → `aggregate.py` (roll up, surface QA flags) → reconcile against PDF BOM via `authoritative_bom.py` (correct codes) → hand `PARTS_MASTER`/`FAB_ROUTING` to `forge-fabrication`. Optional: `dwg_dxf_diff.py` to confirm DXF exports match the native DWG.

---

## Workflow

### Step 1: Resolve Classification + Intake the Pair (Router — CORE confirm)
Read the project's geometry classification (set in helix-p1-validate sacred constraints; default **MẬT** if unset for any defense product).

| Label | Runtime rule | OCR rule |
|----|----|----|
| **MẬT** (UUV, FCS, torpedo target) | Offline only — assert no network egress | Local Tesseract **only**; no cloud OCR/vision ever |
| **HẠN CHẾ** (pontoon, bia tập) | Local; cloud only on private/internal infra | Local Tesseract only |
| **THƯỜNG** (R&D, demo) | Free | Local preferred; cloud OCR allowed but unnecessary |

Intake check: confirm both files present, same part/rev, DXF readable (`ezdxf.readfile`, fall back to `ezdxf.recover.readfile`), PDF has a text layer (else mark `OCR-REQUIRED`). Flag `[CLASSIFICATION-VIOLATION]` and STOP if any parser would touch the network for MẬT.

### Step 2: DXF Structured Extraction (Offload)
Iterate `modelspace()` (and named paperspace layouts, labeled). Harvest:
```
□ Layers        → name, color, on/off  (layer = free semantic tag)
□ TEXT/MTEXT    → .plain_text(), insert point, layer  (labels, notes, callouts)
□ DIMENSION     → measurement, dim text/override, tolerance, dim style
□ INSERT+ATTRIB → block name + attrib key/value  (title block, BOM rows, weld/surface symbols)
□ Geometry      → LWPOLYLINE/LINE/ARC/CIRCLE: lengths, closed-profile areas, bounding box
□ Header        → $INSUNITS (units), $EXTMIN/$EXTMAX (model extents)
```
Honor OCS/UCS when reading insert points (don't report raw OCS coords as world coords). Record each value with its **entity handle** as the source pointer.

### Step 3: PDF Cross-Read (Offload)
On the vector PDF: `get_text("dict")` for positioned text (title block, notes, dim labels with bbox), `get_drawings()` for vector linework, pdfplumber `find_tables()` for BOM / revision tables. If `OCR-REQUIRED` (raster) → `get_textpage_ocr()` and mark every value `LOW`. Detect garbled text (runs of `0xFFFD`) → flag font/`ToUnicode` loss, mark `LOW`.

### Step 4: Reconcile PDF ↔ DXF (Offload → confidence assignment)
For each candidate value, set confidence per the gate:
- Present & matching in both → `HIGH`.
- DXF-only (geometry) or PDF-only (note/title-block field) → `MED`, source named.
- OCR/garbled origin → `LOW`.
- Disagree → emit `[CONFLICT: dxf=… pdf=…]`, do not pick a winner (DXF = geometry truth, PDF = annotation/override truth; CEO resolves).

### Step 5: Build the Structured Extract (Offload — BOTH files mandatory)
Always emit **both**: `cad_extract.json` (machine — for `forge-fabrication`, `erp-bom`, CNC, diffing) AND `cad_extract.md` (CEO-readable). JSON is not optional.

**`cad_extract.json` — fixed schema** (every measured row carries `source` + `confidence`):
```jsonc
{
  "meta":   { "part_id","name","assembly","product","material","mass_kg","scale",
              "org","date","classification","dxf_version","units",
              "source_files": {"dxf","pdf"}, "ingested","tool":"helix-cad-ingest",
              "provenance": { "part_id":"title-block","code_in_dxf":"title-block",
                              "name":"title-block","material":"title-block","scale":"title-block" } },
  "dimensions":    [ {"param","value","unit","tolerance","method","source","confidence","note"} ],
  "tolerances":    [ {"rule","value","method","source","confidence"} ],
  "gdt":           [ {"symbol","value","datum","source","confidence"} ],
  "holes":         [ {"dia","count","pattern","positions":[[x,y]],"method","source","confidence","note"} ],
  "surface_finish":{ "value","method","source","confidence" },
  "layers":        [ {"name","color","entity_count"} ],
  "blocks":        [ {"name","count","attribs":{}} ],
  "bom":           [ {"item","code","name","qty","material","thickness_mm"} ],   // assemblies only
  "process_notes": [ "..." ],
  "conflicts":     [ {"type","detail"} ],
  "missing":       [ "..." ]
}
```
> Rules: `confidence` ∈ {HIGH,MED,LOW}; never omit it. A break-view / dim-override goes in BOTH the dimension row (`note`) and `conflicts[]` (`type":"BREAK-VIEW"`). Unparsed/uncertain reads go in `missing[]`, never dropped silently.

**Collection-method provenance (`method`) — taxonomy B.** Every value records HOW it was obtained;
`confidence` DERIVES from it (a computed measurement outranks human-typed text — title-block codes
are copy-paste-prone). Enum → default confidence:

| `method` | nguồn | conf mặc định |
|---|---|---|
| `geometry-counted` | đếm entity hình học (CIRCLE) | HIGH |
| `dim-measured` | `DIMENSION.get_measurement()` | HIGH |
| `dim-override` | trị số draftsman gõ đè trên dim | MED |
| `schedule-table` | dòng BOM / parts-list | MED |
| `title-block` | chữ khung tên (mã/vật liệu/tỷ lệ) | MED (mã: LOW qua `code_confidence`) |
| `ocr` | raster→Tesseract (chưa wire ở reader DXF-only) | LOW |
| `human-certified` | CEO/kỹ sư chứng thực → bump đỉnh (đặt downstream) | HIGH |

Giá trị giả định (dung sai mặc định IT14/2) mang `method: null` + `confidence: LOW` — fail-safe cho
mọi `min_method` gate của [[helix-cad-validate]] tới khi được parse/chứng thực.

**`cad_extract.md`** — CEO-readable mirror: title-block table · critical-dimension table (Param | Value | Tol | Source | Confidence) · BOM table · process notes · CONFLICTS/MISSING section.

### Step 6: CEO Certifies Critical Dimensions (CORE — Confidence Gate)
```
═══ EXTRACT VERIFY — {{part_id}} rev {{rev}} ═══
Critical dims match source drawing?   [ ] yes  [ ] no
LOW-confidence values reviewed:       [ ] all confirmed / corrected
Conflicts resolved (dxf vs pdf):      [ ] done
Title block + BOM correct:            [ ] yes
```
CEO `no` → correct the flagged rows (or re-export per Export Requirements) and re-run. AI never self-certifies dimensions.

### Step 7: Handoff to Design / Process (Offload)
Route the certified extract to the consumer:
- **Design / RE** → seed requirements (`helix-p1-requirements`) or a reverse-engineering teardown (`reverse-engineering`) with real measured geometry.
- **Process build** → feed BOM + part geometry + tolerances into `forge-fabrication` to draft the manufacturing process (cut lists, weld maps, machining ops, inspection dims).
- **Inspection** → critical-dim + GD&T table seeds `helix-p4-inspection`.
- Commit `cad_extract.json/.md` + source pointers to the project; register in the ICD as an **ingested** geometry record (rev-locked to the source pair).

## Gotchas
- **Exploded text/dims** in the DXF = the #1 cause of empty extracts. If labels come back as line soup → re-export per Export Requirements (don't explode).
- **Scanned/raster PDF** has no text layer → everything is `LOW` (OCR). Push for a vector PDF re-plot.
- **Garbled glyphs** (custom SHX font, missing `/ToUnicode`) → text extracts as gibberish; OCR is the only fallback.
- **OCS/UCS & paperspace scale**: raw entity coords may be in an OCS, and paperspace geometry is at plot scale — never report those as true-mm world dimensions without transform.
- **Dimension override text**: the displayed value can differ from the measured geometry (designer typed an override). Report both; flag mismatch as a `CONFLICT`.
- **Rev mismatch**: PDF and DXF from different revisions = silent wrong data. Step 1 enforces same-rev pairing.
- **Stale title-block part codes** (field-confirmed): a detail sheet's title-block code can be a leftover copied from a sibling sheet (e.g. group-4 sheets carrying group-1 `GT.00.01.xx` codes). The code lives in BOTH the DXF and the PDF title block, so cross-reading them does NOT catch it — only the **assembly BOM page** (parts list) holds the correct code. Therefore: key every output by **filename** (reliable), record `code_in_dxf` separately at **LOW** confidence, and flag a mismatch in `missing[]`. Never auto-"fix" the code — surface it for the design office.
- **Holes drawn as arc-pairs**: some CAD exports draw a circle as 2+ ARC segments, not a CIRCLE entity. `CIRCLE` count alone under-reports holes; reconcile ARC count and mark hole totals `MED` until confirmed against the PDF.
- **Cross-sheet conflict (detail vs nesting)**: the same part can disagree between its detail sheet and the laser **nesting/sắp-hình sheet** (material and/or qty) — e.g. SS400/SL01 on the detail vs Nhôm 5083/SL02 on the nesting. The **nesting sheet is the authoritative cut-list** for material×thickness×qty; emit the disagreement as a `CONFLICT`, do not silently pick one.
- **Assembly (tổng-lắp) drawings mix parts**: a `*-tong lap` / assembly DXF aggregates many parts' geometry — its dims/holes are assembly-level, NOT a single fabricable part. Exclude assembly files from any cut-list; use them only for the BOM tree.
- **Windows console encoding**: when running the bundled scripts, set `PYTHONUTF8=1`/`PYTHONIOENCODING=utf-8` or Vietnamese prints crash on cp1252. File output is always written UTF-8.
- **DWG via ODA → `\U+XXXX` escapes** (field-confirmed): SHX/Vietnamese text read from a converted DWG comes through as AutoCAD unicode escapes (e.g. `\U+0110\U+1ED3NG` for "ĐỒNG"), unlike a clean DXF export. Decode `\U\+([0-9A-Fa-f]{4})`→`chr()` before matching codes/materials/text (`dwg_dxf_diff.decode_acad`), else material/token comparisons under-count.
- **Drift check is directional**: native DWG is a *superset* (it holds BOM/assembly sheets the per-part DXF folder lacks), so "DWG-only" content is expected, NOT drift. Real export drift = content present in the DXF but ABSENT from the DWG (DXF-only). A few DXF-only dim values are usually override-text/leader dims (the DWG carries them as text, not associative DIMENSION) — verify, don't alarm.

## Integration Map (who consumes this ingest)
| Consumer | Uses the extract for |
|----|----|
| helix-p1-requirements | Seed requirements from a real measured part (RE / customer-supplied drawing) |
| reverse-engineering | Geometry + BOM teardown of a competitor/legacy drawing |
| forge-fabrication | BOM + tolerances + geometry → draft fabrication process / cut & weld plan. For defense products, F0 turns the aggregated extract into a TCVN **Quy trình công nghệ** doc (see forge-fabrication `references/quy-trinh-cong-nghe-template.md`) → DOCX. |
| erp-bom | `MASTER_BOM.csv` from `aggregate.py` imports directly as the ERPNext BOM |
| helix-p4-inspection | Critical-dim + GD&T table → inspection plan |
| helix-cad-bridge | Re-parameterize an ingested profile into editable code-CAD (round-trip) |

**Authoritative-override source:** when the project ships an **assembly BOM page / parts list** (PDF), treat it as the **source of truth** for code, name, qty, material, thickness — it overrides stale detail-sheet title blocks and the weak per-file heuristics. `authoritative_bom.py` encodes such a corrected master and emits `PARTS_MASTER` + `FAB_ROUTING` (routing grouped by station: laser nesting by material×thickness, turning, purchase, weld assemblies).

## Output
Save to `1_Projects/{{project}}/.../cad/ingested/`:
- `{{part_id}}_rev{{rev}}.cad_extract.json` (machine record, source-pointed)
- `{{part_id}}_rev{{rev}}.cad_extract.md` (CEO-readable, confidence column)
- copy/reference of the source `.pdf` + `.dxf` pair (rev-locked)

## CEO Checkpoint
```
═══ helix-cad-ingest COMPLETE ═══
Pair: {{part_id}}.dxf + .pdf   rev {{rev}}   Classification: {{label}}
DXF parsed: ✅ ({{n}} entities, {{l}} layers)   PDF: {{vector|OCR}} 
Extracted: {{d}} dims · {{t}} tolerances · {{b}} BOM rows · {{notes}} notes
Confidence: HIGH {{h}} · MED {{m}} · LOW {{lo}}   Conflicts: {{c}}   Missing: {{x}}
Egress guard (MẬT): [PASS — no network]

CEO:
(1) ✅ Certify critical dims → handoff to {{consumer}}
(2) 🔄 Correct flagged rows (Core) → re-emit
(3) ⏸️ Re-export pair per Export Requirements (text/dims/blocks not exploded, vector PDF)
```

## COD
- DXF/PDF parsing, table/geometry harvest, reconcile, emit JSON/MD: Offload (O)
- **Classification label: Core (C)** — defense data control
- **Critical-dimension / tolerance / GD&T certification: Core (C)** — [[LLM Spatial Blindness]] confidence gate, non-delegable
- Egress + OCR-locality guard (MẬT): Default (D) — automated assertion
