---
name: helix-cad-nest
description: "Geometry→manufacturing-instruction bridge — turns the flat-profile geometry-of-record (DXF flat patterns from cad_extract, or unfolded sheet-metal from STEP) into a fabrication-ready cut plan: parts grouped by material×thickness, per-sheet cut-list, sheet-count + material-yield estimate, and a hand-off of the true-shape nest geometry to a LOCAL nesting tool. Honest about LLM spatial blindness: AI does the COMPUTABLE part (grouping, area sums, sheet-count, cut-list, material norms) and hands true geometric nesting to a local tool/human, never fakes a nest layout. Closes the design→production loop helix-cad-bridge/ingest opened. Feeds forge-fabrication F0/F1. Defense-safe: reads Geometry Classification, all LOCAL. Triggers on: 'cad nest', 'nesting', 'sắp hình', 'cut list', 'cut plan', 'laser nesting', 'plasma cut', 'khai triển tấm', 'flat pattern', 'material yield', 'định mức vật tư', 'sheet utilization', 'phôi cắt', 'CNC cut file', 'tận dụng vật liệu'."
---

# helix-cad-nest — Geometry → Cut Plan Bridge (Local, Defense-Safe)

> **Role:** Cross-phase bridge — the **production-prep mirror** that closes the loop [[helix-cad-bridge]] (code→STEP) and [[helix-cad-ingest]] (drawing→record) opened. It converts the **geometry-of-record** into a fabrication-ready **cut plan** and hands the actual nest geometry to a local CNC/nesting tool.
> **Backend:** `ezdxf` (read flat-profile DXF: closed LWPOLYLINE areas + bounding boxes) — LOCAL, offline. Optional local **Deepnest/SVGnest** (offline) or the shop CAM for true-shape nesting.
> **Interface in:** flat-pattern DXF (from `cad_extract.json` per part, or unfolded from a sheet-metal STEP) + material×thickness per part. **Interface out:** `NEST_PLAN.md` + `CUT_LIST.csv` (+ optional `nest_*.dxf` per sheet from the local tool).
> **Why this exists:** [[helix-cad-bridge]] makes geometry; [[helix-cad-ingest]] reads it; nothing turned geometry into machine instructions. Nesting/cut-files lived only as prose for the shop floor. This bridge produces the computable cut plan and routes true-shape nest layout to where it belongs.

## The Spatial-Blindness Honest Line (MANDATORY)
> Source: [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]]

True-shape part nesting is a **geometric packing** problem — exactly what an LLM is blind to. This skill therefore **splits the work honestly**:

| AI DOES (computable, deterministic) | AI HANDS OFF (geometric, to local tool/human) |
|----|----|
| Group parts by **material × thickness** (the cut-list axis) | True-shape nest layout (where each part sits on the sheet) |
| Sum part **areas** + read **bounding boxes** from the DXF | The actual `nest_*.dxf` with parts placed + common-line cuts |
| Estimate **sheet count + utilization%** via bounding-box bin-packing (a *lower-bound* yield, clearly labelled an estimate) | Final yield optimization (true-shape can beat the bbox estimate) |
| Emit **per-sheet cut-list**, qty, material norm, scrap% | — |
| Flag conflicts vs the design BOM / nesting sheet | — |

**AI never draws a fake nest layout.** The placement geometry comes from a LOCAL nesting tool (Deepnest/SVGnest offline, or the shop CAM) or the human nester. AI's bounding-box estimate is a **planning lower bound**, never the production nest.

## Operational Envelope
| DO | DON'T |
|----|----|
| Read areas/bboxes the DXF **actually contains**; group by real material×thickness | Invent a placement, a yield %, or a part the geometry doesn't show |
| Label the bbox sheet-count as an **estimate** (true-shape does better) | Present the bbox bin-pack as the final production nest |
| Run all parsing LOCAL; nest geometry via local tool only | Send profiles to a cloud nesting service for MẬT/HẠN-CHẾ |
| Reconcile against the **nesting/sắp-hình sheet** (authoritative cut-list) | Silently override the shop's nesting sheet |

## Classification Router (Step 0 — reads, never sets)
Read **Geometry Classification** (MẬT / HẠN-CHẾ / THƯỜNG) from `helix-p1-validate` sacred constraints (carried in `003_IFR_Sacred_Constraints_v1.0.md`), same label the rest of the CAD trio reads. Default **MẬT** for any defense product. MẬT/HẠN-CHẾ → nesting geometry stays on a LOCAL tool only; no cloud nesting service ever. Flag `[CLASSIFICATION-VIOLATION]` and STOP if any step would egress.

## Backend Setup (one-time, offline)
```
pip install ezdxf            # read flat-profile DXF (areas, bounding boxes)
# Optional true-shape nesting, LOCAL only:
#   Deepnest (deepnest.io) — offline desktop, or SVGnest (browser, run locally)
#   or the shop's existing CAM/laser nesting software
```

**Bundled runner** (in this skill folder — run with `PYTHONUTF8=1`):
- **`nest_estimate.py`** — `python nest_estimate.py <parts.csv|parts.json|dxf_dir> --sheet 1500x3000 --kerf 0.2 --gap 5 --out <dir>`. Reads per-part `{code, material, thickness_mm, area_mm2, bbox_w, bbox_h, qty}` (from a CSV/JSON, or harvested from flat DXF via ezdxf), groups by material×thickness, runs a **shelf/first-fit bounding-box bin-pack** per sheet size → emits `NEST_PLAN.md` (per group: parts, qty, total part-area, sheets needed, est. utilization%, scrap%) + `CUT_LIST.csv` (per-sheet rows for ERP/shop). Utilization is explicitly tagged `ESTIMATE (bbox lower-bound)`.

## Workflow

### Step 1: Resolve the Flat-Profile Geometry-of-Record (intake)
Cut plans are for **sheet/plate parts**. For each fabricable part, get its flat profile:
- **From `helix-cad-ingest`:** the part's `cad_extract.json` already carries closed LWPOLYLINE areas + bbox + material + thickness — use directly.
- **From `helix-cad-bridge`:** a sheet-metal STEP must be **unfolded to a flat pattern** first (in the CAD/CAM, exported as flat DXF) — AI cannot unfold (3D geometry). Note `[UNFOLD-REQUIRED]` for parts supplied only as folded STEP.
- Exclude non-sheet parts (turned, purchased, machined-from-block) — route those to their own forge-fabrication stations, not the nest.

### Step 2: Group by Material × Thickness (CORE axis)
The cut-list axis is **material × thickness × sheet-size**. Build groups; each group nests independently (you cannot mix 5083-3mm with SS400-6mm on one sheet). Pull material+thickness from the geometry-of-record; flag any part missing thickness as `[MISSING — thickness]` (CEO supplies).

### Step 3: Area + Bounding-Box Harvest (Offload)
Per part: closed-profile **area** (for material norm / scrap%), **bbox W×H** (for the bin-pack), **qty** (from BOM). All read from the DXF — never estimated.

### Step 4: Sheet-Count + Utilization ESTIMATE (Offload — clearly a lower bound)
Run `nest_estimate.py` (bounding-box shelf bin-pack) per group on the stock sheet size, honoring **kerf** + **part gap**. Output per group: sheets needed, Σpart-area, sheet-area, **utilization% = Σpart-area / (sheets × sheet-area)** tagged `ESTIMATE`. State plainly: *true-shape nesting on a local tool will need the same or FEWER sheets* — this is a planning lower bound for material ordering, not the production nest.

### Step 5: Hand Off True-Shape Nest to LOCAL Tool (Spatial-Blindness boundary)
Export the grouped flat profiles for the LOCAL nester (Deepnest/SVGnest/shop CAM). The human/tool produces the real `nest_*.dxf` (placed parts + common-line cuts + lead-ins). **AI does not place parts.** When the nest DXF comes back, it can be re-read by [[helix-cad-ingest]] to confirm part count + material against this plan (round-trip check).

### Step 6: Emit Cut Plan + Reconcile (Offload → CEO confirm)
Emit `NEST_PLAN.md` (CEO-readable) + `CUT_LIST.csv` (ERP/shop import). **Reconcile** against:
- the design **BOM** (every BOM sheet-part appears in a nest group; no orphans),
- the **nesting/sắp-hình sheet** if one exists — it is the **authoritative cut-list** for material×thickness×qty; emit any disagreement as a `CONFLICT` (per [[helix-cad-ingest]] cross-sheet gotcha), do not silently pick one.

### Step 7: CEO Confirms → Handoff (CORE)
```
═══ CUT PLAN VERIFY — {{project}} ═══
Material×thickness groups:     {{N}}
Sheets (estimate, bbox):       {{S}}   Utilization est: {{U}}%
True-shape nest produced by:   [ ] local tool  [ ] shop CAM  [ ] pending
BOM reconciled (no orphans):   [ ] yes
Nesting-sheet conflicts:       {{c}} (resolved? [ ])
```
CEO confirm → hand `CUT_LIST.csv` + sheet-count to **forge-fabrication F1** (material allocation + laser nesting station) and the **material order** (Σ sheets per material×thickness + scrap%).

## Output
Save to `1_Projects/{{project}}/.../cad/nest/`:
- `NEST_PLAN.md` (CEO-readable: groups, sheet-count estimate, utilization, scrap%, conflicts)
- `CUT_LIST.csv` (per-sheet cut-list for ERP/shop import)
- optional `nest_*.dxf` (true-shape layout from the LOCAL tool — referenced, rev-locked)

## Integration Map
| Consumer | Uses the cut plan for |
|----|----|
| forge-fabrication F0/F1 | Material norm + laser/plasma nesting station routing; `CUT_LIST.csv` feeds the F1 material/BOM allocation |
| erp-stock / erp-bom | Sheet-count × material×thickness → purchase requisition + material norm |
| helix-cad-ingest | Re-read the returned `nest_*.dxf` to confirm part count/material (round-trip check) |
| helix-p4-inspection | Cut-list ↔ BOM reconciliation feeds incoming/first-article check |

**Source-of-truth note:** when a project ships a **nesting/sắp-hình sheet** (PDF), it is the **authoritative cut-list** for material×thickness×qty and overrides this skill's estimate — emit disagreements as `CONFLICT`, never auto-resolve.

## Gotchas
- **Bbox estimate ≠ production nest** — the bounding-box bin-pack is a material-ordering lower bound; true-shape nesting (common-line, part-in-hole) does better. Never quote the estimate as the final yield.
- **Folded STEP can't be nested** — sheet-metal must be unfolded to a flat pattern in CAD first (AI can't unfold 3D). Flag `[UNFOLD-REQUIRED]`.
- **Mixed material/thickness on one sheet is invalid** — groups never mix; a part with missing thickness blocks its group.
- **Grain/rolling direction** (for anisotropic plate, formed parts) — if the drawing specifies grain direction, the human nester must honor it; AI's area/bbox math ignores orientation constraints — flag if the geometry-of-record notes a grain callout.
- **Kerf + gap matter** — a too-small gap fuses parts on the laser; carry the shop's kerf/gap into the estimate, don't assume zero.
- **Windows console encoding** — run bundled script with `PYTHONUTF8=1` or Vietnamese prints crash on cp1252.

## CEO Checkpoint
```
═══ helix-cad-nest COMPLETE ═══
Project: {{project}}   Classification: {{label}}
Groups (material×thickness): {{N}}   Parts: {{p}}   Sheet-parts only: ✅
Sheets needed (ESTIMATE, bbox): {{S}}   Utilization est: {{U}}%   Scrap est: {{sc}}%
True-shape nest: {{local tool | shop CAM | PENDING}}
BOM orphans: {{o}}   Nesting-sheet conflicts: {{c}}
Egress guard (MẬT): [PASS — no cloud nesting]

CEO:
(1) ✅ Confirm cut plan → handoff to forge-fabrication F1 + material order
(2) 🔄 Re-group / re-estimate (different sheet size, kerf, gap)
(3) ⏸️ Resolve nesting-sheet CONFLICT first
```

## COD
- DXF area/bbox harvest, material×thickness grouping, sheet-count estimate, cut-list emit: Offload (O)
- **Classification label read + egress guard: Default (D)** — automated assertion
- **True-shape nest layout: handed to LOCAL tool/human** — [[LLM Spatial Blindness]] boundary, AI never places parts
- **Nesting-sheet CONFLICT resolution + final cut-plan confirm: Core (C)** — material-cost commitment, non-delegable
