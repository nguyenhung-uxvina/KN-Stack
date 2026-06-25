---
name: helix-cad-to-fab
description: "One-command drawing-folder → fabrication bundle. Codifies the proven read-from-drawings workflow (DWG/DXF + PDF → cad_extract → MASTER_BOM → PDF parts-list → nest → TCVN Quy trình công nghệ → DOCX) so any drawing group runs the SAME pipeline without redoing it by hand. Bundled cad_fab_pipeline.py runs the deterministic ~80% (ingest → aggregate → PDF parts-list extract → report); AI+CEO finalize the judgment tail (decode Vietnamese names, reconcile codes, resolve conflicts, fill the process doc). Chains helix-cad-ingest → helix-cad-nest → forge-fabrication F0. Defense-safe: 100% LOCAL, reads Geometry Classification. Triggers on: 'cad to fab', 'drawing to process', 'bản vẽ sang quy trình', 'chạy pipeline bản vẽ', 'quy trình công nghệ từ folder', 'fab bundle', 'cụm bản vẽ khác', 'áp dụng pipeline', 'cad fab pipeline', 'đọc folder bản vẽ ra quy trình'."
---

# helix-cad-to-fab — Drawing Folder → Fabrication Bundle (Local, Defense-Safe)

> **Role:** Thin pipeline driver codifying the proven manual workflow (field-validated on GIÁ TRƯỢT UUV / Khung cơ sở). Chains [[helix-cad-ingest]] → [[helix-cad-nest]] → [[forge-fabrication]] F0.
> **Why:** Doing the full ingest→fab flow by hand for every drawing group is slow and error-prone. This runs the **deterministic plumbing once, identically**, then AI+CEO only do the judgment that can't be automated.
> **Split (honest):** the script does ~80% mechanical extraction; the LLM-spatial-blindness/Vietnamese-decode/conflict-resolution/process-authoring ~20% stays with AI+CEO.

## The Pipeline

```
folder (DWG/DXF + PDF, MẬT)
   │  python cad_fab_pipeline.py "<folder>" --classification MẬT
   ▼  ───────── DETERMINISTIC (script) ─────────
 [1] ingest      DWG via ODA → cad_extract.json/.md per sheet   (helix-cad-ingest/ingest.py)
 [2] aggregate   → MASTER_BOM.md/.csv + CRITICAL_DIMS.md         (helix-cad-ingest/aggregate.py)
 [3] pdf         PDF text dump + parts-list rows (VL×dày×SL)     → PDF_PARTSLIST.csv + PDF_RAW.txt
 [4] report      → PIPELINE_REPORT.md (counts · materials · next-steps)
   │  ───────── JUDGMENT (AI + CEO) ─────────
 [5] decode      garbled Vietnamese names in PDF_PARTSLIST.csv  (font /ToUnicode loss)
 [6] reconcile   PDF parts-list (authoritative) ↔ MASTER_BOM (DWG): lock code+SL, flag conflicts
 [7] nest        parts.csv → helix-cad-nest/nest_estimate.py    → NEST_PLAN + CUT_LIST
 [8] QTCN        forge-fabrication F0 + 11-section TCVN template → QUY_TRINH_CONG_NGHE.md
 [9] docx        python md_to_docx.py QUY_TRINH_CONG_NGHE.md    → DOCX trình ký
 [10] CEO        chốt §11 flags + classification → ký phát hành
```

## How to Use

```
# Step 1 — run the deterministic pipeline on any drawing folder
PYTHONUTF8=1 python cad_fab_pipeline.py "D:/.../3 - Ban ve gia phu" \
    --classification MẬT --out "D:/.../3 - Ban ve gia phu/ingested"

# → ingested/: cad_extract×N · MASTER_BOM.* · CRITICAL_DIMS.md · PDF_PARTSLIST.csv · PDF_RAW.txt · PIPELINE_REPORT.md

# Step 2 — AI+CEO finalize (read PIPELINE_REPORT.md §⏭️): decode parts-list, reconcile,
#          nest, author Quy trình công nghệ, emit DOCX, CEO sign-off.
```

## Bundled Runners
- **`cad_fab_pipeline.py`** — the driver. `<folder> --classification MẬT [--out DIR] [--prefer dwg|dxf]`. Locates `ingest.py`/`aggregate.py` in the sibling `helix-cad-ingest/` skill. Auto-finds the PDF, dumps `PDF_RAW.txt`, and extracts parts-list rows (any line carrying material + thickness + `SL n`) to `PDF_PARTSLIST.csv` — the raw_name stays garbled for AI to decode (numbers/material/SL are reliable). Emits `PIPELINE_REPORT.md` with the AI/CEO next-steps.
- **`md_to_docx.py`** — reusable Markdown→DOCX for the process doc (`<in.md> [out.docx]`; Times New Roman, GFM tables, falls back to `*_v2.docx` if the file is open in Word).

## What stays manual (and why)
- **Decode the PDF parts-list names** — Vietnamese SHX fonts lose `/ToUnicode`; names extract garbled. The LLM decodes (skeleton + numbers are intact); material/thickness/SL are auto-parsed.
- **Reconcile codes** — title-block codes are stale (copy-paste gotcha); only the PDF parts-list page is authoritative. AI cross-reads, CEO certifies.
- **Conflicts** (C45 turned-vs-sheet, oversize plate, material/qty disagreements) — surfaced, never auto-resolved.
- **Quy trình công nghệ specifics** (operation sheets, cut/bend/turn regimes, WPS) + **classification + §11 sign-off** — Core (CEO).

## Output (per folder)
```
<folder>/ingested/
  *.cad_extract.json/.md        # per sheet (helix-cad-ingest)
  MASTER_BOM.md/.csv  CRITICAL_DIMS.md
  PDF_PARTSLIST.csv  PDF_RAW.txt
  PIPELINE_REPORT.md            # counts + flags + AI/CEO next-steps
  nest/   NEST_PLAN.md  CUT_LIST.csv          # step 7
  fab/<run_id>/  QUY_TRINH_CONG_NGHE.md/.docx  F0_Handoff_Gate.md   # steps 8-9
```

## Gotchas
- **MẬT egress** — all local (ODA + ezdxf + PyMuPDF offline). No cloud OCR/nesting. Confirm the Geometry Classification before running.
- **`authoritative_bom.py` is product-specific** — it embeds a corrected master per product (e.g. all GIÁ TRƯỢT groups 1/3/4). For a NEW product, the per-folder `MASTER_BOM.csv` + the PDF parts-list are the source; encode a fresh master if the product isn't yet in `authoritative_bom.py`.
- **PDF parts-list page** — the authoritative SL/material/thickness live on the assembly nomenclature page (often the biggest sheet). The script grabs every `SL n` row across all pages; AI picks the real parts-list.
- **Windows UTF-8** — run with `PYTHONUTF8=1`.

## COD
- Pipeline plumbing (ingest/aggregate/pdf/report): Offload (O)
- Decode + reconcile + conflict flagging: Offload→**CEO certify (C)**
- Classification + critical-dim/process sign-off: **Core (C)**
