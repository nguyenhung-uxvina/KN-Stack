---
description: "Generate Excalidraw diagrams for HELIX pipeline outputs. Creates .excalidraw.md files viewable in Obsidian. Supports 12 diagram types across Phase 1-3 blocks. Triggers on 'draw', 'diagram', 'excalidraw', 'vẽ sơ đồ', 'biểu đồ', 'chart', 'visual', or when a block-skill output would benefit from a visual representation."
allowed-tools: ["Read", "Write", "Glob", "Grep", "Bash", "Agent"]
---

# helix-draw — Excalidraw Diagram Generator for HELIX Pipeline

> **Purpose:** Generate `.excalidraw.md` files from structured data produced by HELIX pipeline blocks.
> **Output:** Obsidian-compatible Excalidraw files with `excalidraw-plugin: parsed` frontmatter.
> **Integration:** Called by block-skills via reference, or standalone via `/helix-draw <type> <project>`.

## Usage

```
/helix-draw <diagram-type> <project> [--source <file>] [--title <title>]
```

**Examples:**
```
/helix-draw morpho VN-CUAV-SIM-001
/helix-draw s-diagram VN-CUAV-SIM-001 --source VDI_2225_Evaluation.md
/helix-draw radar VN-CUAV-SIM-001 --title "TESE 8-Trend Analysis"
/helix-draw function-tree VN-CUAV-SIM-001
```

## Supported Diagram Types (12)

| Type | Keyword | Phase | Block(s) | Description |
|------|---------|:-----:|----------|-------------|
| `morpho` | morphological matrix | 2 | BB | Rows=SFs, cols=WPs, concept paths as colored lines. DSO scores in cells. |
| `s-diagram` | S-diagram, Rt-Re | 2,3 | BC, BE | Scatter plot: X=technical quality, Y=cost (or economic rating). Value line diagonal. Data points = concepts/products. |
| `function-tree` | function structure, 6-flow | 1 | BD | 7 L1 blocks with L2 sub-functions. 6-flow arrows (E/M/S/D/C/T). System boundary. |
| `radar` | radar chart, spider | 1,2,3 | Multiple | N-axis radar/spider chart. Use for: TESE trends, design novelty, DfX scores, PLAUSIBLE checks, concept comparison. |
| `pipeline` | pipeline flow | 1,2,3 | Orchestrator | B0→BA→BB→BC→BD→BE progress blocks with status colors (green/orange/gray). |
| `block-diagram` | system architecture | 1,3 | BD, BA | SS1-SS5 blocks with interface arrows. Domain colors (MECH/ELEC/SW). Labels on interfaces. |
| `matrix` | coupling, compatibility, FR×DP | 2 | BB, BC | N×N color-coded grid. Green=OK, Yellow=partial, Red=conflict. Use for: compatibility, AD coupling, interface. |
| `tree` | product line, decision | 2 | BB | Hierarchical tree: common platform → variants. Or decision tree with branches. |
| `bar-chart` | bar chart, Pareto, waterfall | 1,2,3 | Multiple | Vertical/horizontal bars. Use for: requirements coverage, BOM cost breakdown, DQM comparison, DSO ranking. |
| `dashboard` | scorecard, traffic light | 1,2,3 | BE | Multi-metric dashboard with traffic lights (green/yellow/red). Use for: QC gate, DfX audit, preflight check. |
| `trade-study` | trade study, comparison | 2 | BB, BC | Side-by-side WP comparison cards with criteria scores. Use for: recoil trade, display trade, etc. |
| `stakeholder-map` | stakeholder, power-interest | 1 | B0 | 2×2 influence-interest grid with stakeholder positions. |

## Excalidraw File Format

Output files MUST use this structure:

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
aliases: [<Descriptive Alias>]
---

# Excalidraw Data

## Text Elements
<searchable text content repeated here for Obsidian search>

## Drawing
\```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [...],
  "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" },
  "files": {}
}
\```

%%
## Drawing
%%
```

## Element Construction Rules

### General
- `roughness: 0` for all elements (clean, not sketchy)
- Use `roundness: {"type": 3}` for rounded rectangles
- Unique `id` per element (descriptive string, e.g., `"f1-box"`, `"dot-lite"`)
- `seed` and `versionNonce` = any unique integer per element

### Color Palette (Workshop X standard)

| Role | strokeColor | backgroundColor | Use |
|------|-----------|----------------|-----|
| **LITE / Primary** | `#1971c2` | `#d0ebff` | LITE variant, SS1, primary data |
| **FIXED / Secondary** | `#2f9e44` | `#ebfbee` | FIXED variant, SS3, positive |
| **FULL / Accent** | `#e8590c` | `#fff4e6` | FULL variant, SS2, warning |
| **CORTEX / Tertiary** | `#7048e8` | `#f3f0ff` | CORTEX variant, SS4, systems |
| **Risk / Alert** | `#e03131` | `#fff5f5` | Value lines, risks, failures |
| **Neutral / Muted** | `#868e96` | `#f1f3f5` | Grayed out, pending, disabled |
| **Control / Process** | `#862e9c` | `#f8f0fc` | Control flow, instructor, session |
| **Platform / Cyan** | `#0c8599` | `#e3fafc` | MWI, swap, modularity |
| **Text** | `#1e1e1e` | — | Primary text |
| **Subtle text** | `#495057` | — | Sub-labels, descriptions |
| **Grid / Guide** | `#868e96` | — | Grid lines, tick marks (opacity 30) |

### Text Sizing

| Level | fontSize | Use |
|-------|:--------:|-----|
| Title | 20-24 | Diagram title |
| Subtitle | 13-14 | Subtitle, date, source |
| Label | 14-16 | Box titles, axis labels |
| Body | 11-12 | Content text, descriptions |
| Tick | 11-13 | Axis ticks, small annotations |
| Note | 9-11 | Footnotes, interface labels |

### Coordinate System
- Top-left origin (0,0)
- Typical canvas: 800-900px wide, 500-700px tall
- Chart area margins: left 120px (axis labels), right 50px, top 60px (title), bottom 50px (axis)
- Standard box: 150-200px wide, 80-130px tall
- Arrow gap between boxes: 30-50px

## How Block-Skills Reference This Skill

Each block-skill that produces visual output should include in its output step:

```markdown
### Visual Output
Generate Excalidraw diagram: `/helix-draw <type> {{project}} --source <output-file> --title "<title>"`
Embed in deliverable: `![[{{prefix}}<DiagramName>.excalidraw]]`
```

## Diagram Type Specifications

### `morpho` — Morphological Matrix
- **Data source:** `*_Morphological_Matrix.md` or `*_Morpho_SS*.md`
- **Structure:** Rows = sub-functions (left column), Columns = working principles per SF
- **Cell content:** WP name, DSO score, cost
- **Concept paths:** Colored lines connecting selected WPs across rows (1 color per concept variant)
- **Markers:** ★ for selected WP, ⚠️ for solution-determining SF, [NEW] for TRIZ-derived
- **WTP filter:** Essential SFs = bold border, Beneficial = normal, Luxurious = dashed

### `s-diagram` — Technical Quality vs Cost
- **Data source:** `*_VDI_2225_Evaluation.md` or `*_ICDM_CSR_Evaluation.md`
- **X-axis:** BOM Cost or Re (economic rating), labeled with tick marks
- **Y-axis:** DQM% or Rt (technical rating), labeled with tick marks
- **Value line:** Dashed red line at threshold (e.g., DQM=85%)
- **Viable zone:** Light green fill above value line
- **Data points:** Colored circles (per WX color palette) with labels
- **Grid:** Dotted gray lines at major ticks

### `function-tree` — 6-Flow Function Structure
- **Data source:** `*_Function_Structure_6Flow*.md`
- **L1 blocks:** Colored rectangles per function (F1-F7), each with L2 sub-functions listed inside
- **Arrows:** Flow connections between blocks (colored by flow type if needed)
- **System boundary:** Dashed rectangle around all blocks
- **Legend:** Flow types (E/M/S/D/C/T), latency chain, solution-determining markers

### `radar` — Radar/Spider Chart
- **Data source:** Varies (TESE, DfX, design type, concept comparison)
- **Axes:** N labeled axes radiating from center (N = number of criteria)
- **Scale:** Center = min, outer = max (labeled)
- **Data series:** Colored polygons (1 per concept/entity compared)
- **Legend:** Color → entity mapping

### `pipeline` — Pipeline Progress Flow
- **Data source:** `_pipeline_state.md`
- **Blocks:** 6 rectangles (B0→BA→BB→BC→BD→BE) with arrows between
- **Colors:** Green = complete, Orange = in progress, Gray = pending
- **Labels:** Block name + skill name + status + description
- **Progress bar:** Text showing N/6 complete + percentage

### `block-diagram` — System Architecture
- **Data source:** `SA_System_Architecture.md` or concept descriptions
- **Blocks:** SS1-SS5 (or domain grouping) as colored rectangles
- **Interfaces:** Arrows between blocks with protocol labels (USB, UDP, HDMI, LAN)
- **Domain colors:** MECH=blue, ELEC=orange, SW=purple (or per subsystem)
- **Info text:** Key specs per block, total cost, latency chain

### `matrix` — N×N Grid (Coupling, Compatibility, FR×DP)
- **Data source:** Coupling analysis, compatibility matrix, AD analysis
- **Structure:** Row headers = items A, Column headers = items B
- **Cells:** Color-coded (Green=OK, Yellow=partial, Red=conflict)
- **Diagonal:** Highlighted if applicable (AD independence)
- **Legend:** Color → meaning

### `tree` — Hierarchical Tree
- **Data source:** Product line architecture, decision trees
- **Root node:** Common platform / decision question
- **Branches:** Lines connecting to child nodes
- **Leaf nodes:** Variant boxes with key specs
- **Annotations:** Commonality %, costs, DQM

### `bar-chart` — Vertical/Horizontal Bars
- **Data source:** Requirements count, BOM breakdown, DQM comparison
- **Bars:** Colored per category/variant
- **Labels:** Category/item names on one axis, values on other
- **Reference line:** Target or threshold (dashed)
- **Variants:** Stacked bars, grouped bars, Pareto (with cumulative line)

### `dashboard` — Multi-Metric Scorecard
- **Data source:** QC gate results, preflight checks
- **Layout:** Grid of status indicators
- **Indicators:** Traffic lights (●) or filled rectangles, colored green/yellow/red
- **Labels:** Metric name + value + status

### `trade-study` — Side-by-Side Comparison Cards
- **Data source:** Trade study matrix from BB/BC
- **Cards:** One rectangle per WP candidate, side by side
- **Content:** WP name, criteria scores (★ rating), key specs, DSO score, recommendation
- **Highlight:** Recommended WP with thicker border or different background

### `stakeholder-map` — Power-Interest Grid
- **Data source:** Stakeholder register from B0
- **Quadrants:** 2×2 grid (High/Low Interest × High/Low Power)
- **Labels:** Quadrant strategies (Manage Closely, Keep Satisfied, Keep Informed, Monitor)
- **Data points:** Stakeholder names positioned in appropriate quadrant

## Naming Convention

Output file: `{{prefix}}<DiagramType>_<Subject>.excalidraw.md`

Examples:
- `VN_CUAV_SIM_001_Morpho_Matrix.excalidraw.md`
- `VN_CUAV_SIM_001_S_Diagram.excalidraw.md`
- `VN_CUAV_SIM_001_Function_Tree.excalidraw.md`
- `VN_CUAV_SIM_001_TESE_Radar.excalidraw.md`

## Embedding in Deliverables

After generating a diagram, embed it in the corresponding markdown deliverable:

```markdown
![[VN_CUAV_SIM_001_S_Diagram.excalidraw|800]]
```

Width parameter (e.g., `|800`) controls display size in Obsidian.

## 73 Visual Outputs Mapped to Diagram Types

### Phase 1 — helix-task-clarify (22 visuals)

| Block | Output | Diagram Type |
|-------|--------|:------------:|
| B0 | Stakeholder Register | `stakeholder-map` |
| B0 | Standards Compliance | `matrix` |
| B0 | Contextual Factors | `radar` |
| BA | Requirements Coverage | `bar-chart` |
| BA | Life Stage Scenarios | `pipeline` (swim-lane) |
| BA | Requirements Distribution | `bar-chart` |
| BB | D/W Classification | `bar-chart` |
| BB | Gap Analysis | `dashboard` |
| BB | IFR + Sacred Constraints | `tree` |
| BB | Failure Mode / SPOF | `matrix` |
| BB | Solution Ideas Log | `matrix` |
| BC | 5-Step Abstraction | `pipeline` (funnel) |
| BC | TVDT Benchmark Comparison | `radar` |
| BD | System Black-Box | `block-diagram` |
| BD | 6-Flow Function Structure | `function-tree` |
| BD | Sub-Function Decomposition | `tree` |
| BD | Design Type Assessment | `radar` |
| BD | Solution-Determining SFs | `bar-chart` (bubble) |
| BE | Cross-Domain Interface | `matrix` |
| BE | P02 QC Gate | `dashboard` |
| BE | Gate 1 Readiness | `dashboard` |
| BE | Mechatronic Routing | `tree` (decision) |

### Phase 2 — helix-concept-generate (25 visuals)

| Block | Output | Diagram Type |
|-------|--------|:------------:|
| B0 | Input Verification | `dashboard` |
| B0 | Abstraction Quality | `dashboard` |
| B0 | Function Structure 11-Guideline | `radar` |
| BA | Solution-Determining SF Ranking | `bar-chart` |
| BA | TRIZ Contradictions | `matrix` |
| BA | TESE 8-Trend Analysis | `radar` |
| BB | WP Search Coverage | `matrix` |
| BB | DSO Pre-Ranking | `bar-chart` |
| BB | Morphological Matrix | `morpho` |
| BB | Service/CPS Row | `morpho` (extension) |
| BB | Compatibility Matrix | `matrix` |
| BB | Concept Variants Overview | `tree` |
| BC | Pugh Screening | `matrix` |
| BC | FR×DP Coupling | `matrix` |
| BC | Firming-Up Gap Diagnosis | `matrix` (heatmap) |
| BC | CRUMPLE-S Method Selection | `tree` (decision) |
| BC | Firming-Up Results Comparison | `radar` |
| BC | VDI 2225 Evaluation | `bar-chart` (value profile) |
| BC | **S-Diagram (Rt-Re)** | `s-diagram` |
| BD | Cross-Domain Coupling | `matrix` |
| BD | Assumption Register | `matrix` |
| BD | 3-Scenario Spread | `bar-chart` (box-whisker) |
| BD | CFMA SFD Pareto | `bar-chart` (Pareto) |
| BD | Sensitivity Tornado | `bar-chart` (tornado) |
| BE | CEO Decision Dashboard | `dashboard` |

### Phase 3 — helix-embody-realize (23 visuals)

| Block | Output | Diagram Type |
|-------|--------|:------------:|
| B0 | Embodiment Constraints | `tree` |
| B0 | Spatial Constraints | `block-diagram` |
| BA | Preliminary Layout | `block-diagram` |
| BA | Weight Estimate | `bar-chart` (stacked) |
| BA | Stability Check (maritime) | `bar-chart` |
| BB | Basic Rules Audit (3) | `radar` |
| BB | 5 Design Principles | `radar` |
| BB | DfX Review (7 categories) | `dashboard` |
| BB | PLAUSIBLE 9-Check | `radar` |
| BC | Interface Verification | `block-diagram` |
| BC | Thermal Check | `block-diagram` |
| BC | EMC Assessment | `block-diagram` |
| BC | Shadow Assumptions | `matrix` |
| BC | ICD v3 Diagram | `block-diagram` |
| BD | BOM Cost Breakdown | `bar-chart` (Pareto) |
| BD | Local Content | `bar-chart` (pie) |
| BD | Long-Lead Procurement | `bar-chart` (Gantt-like) |
| BD | Cost Drivers Pareto | `bar-chart` (Pareto) |
| BE | Embodiment Rt Scoring | `radar` |
| BE | Re Economic Rating | `bar-chart` |
| BE | **S-Diagram (Rt vs Re)** | `s-diagram` |
| BE | Weak Spot Value Profile | `bar-chart` |
| BE | P02 QC Gate Phase 3 | `dashboard` |

### Cross-Cutting (3 visuals)

| Output | Diagram Type |
|--------|:------------:|
| Pipeline Progress | `pipeline` |
| Requirements Delta Log | `bar-chart` (waterfall) |
| ICD Version Progression | `block-diagram` |

## COD Classification
- Diagram generation: **Offload (O)** — mechanical Excalidraw JSON generation
- Diagram type/content selection: **Core (C)** — CEO decides what to visualize
- Diagram editing in Obsidian: **Core (C)** — CEO adjusts visuals manually
