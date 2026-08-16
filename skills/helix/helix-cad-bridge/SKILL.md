---
name: helix-cad-bridge
description: "Cross-phase CAD bridge — AI writes parametric code-CAD (build123d/CadQuery/OpenSCAD) from CEO's explicit dimensions + sketch, executes 100% LOCAL, exports STEP + render PNG for CEO verification. Classification router blocks external/cloud calls for MẬT geometry. Serves P2 concept, P3 layout/dfx/bom, P4 drawing, and forge-fabrication handoff. Defense-safe: no geometry leaves the machine. Triggers on: 'cad bridge', 'code-cad', 'build123d', 'cadquery', 'parametric model', 'generate geometry', 'text-to-cad', 'sinh hình học', 'dựng model', 'xuất STEP', 'mech agent'."
---

# helix-cad-bridge: Code-CAD Bridge (Local, Defense-Safe)

> **Role:** Cross-phase bridge — NOT a P-phase block. Called by P2/P3/P4 blocks + forge-fabrication.
> **Backend:** code-CAD only (build123d primary · CadQuery alt · OpenSCAD for simple) — runs LOCAL, offline.
> **Interface:** STEP (geometry handoff) + PNG (CEO verification) + the `.py` script itself (git source of truth).
> **Why code-CAD, not SaaS/MCP:** Leo/Zoo/Fusion/Onshape push geometry to their cloud — disqualified for MẬT defense work. Code-CAD forces explicit parametric dimensions (defeats [[LLM Spatial Blindness]]) and version-controls in git.

## Operational Envelope
> Source: [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]] + [[Operational Envelope Law]]

| DO | DON'T |
|----|----|
| Write parametric code from CEO's **explicit numeric** dimensions | Invent spatial arrangement / placement from vague description |
| Execute script LOCAL, export STEP + render PNG | Call any cloud CAD API (Leo/Zoo/Fusion) for MẬT/HẠN-CHẾ geometry |
| Compute mass properties, bounding box, volume from model | Decide critical dimensions / GD&T (= CEO Core, see helix-p4-drawing) |
| Parameterize so CEO tweaks one variable → regenerate | Claim the geometry is "correct" — only CEO verifies the render |
| Commit `.py` + STEP to project, register in ICD | Overwrite a released STEP without rev bump |

**Multi-Agent Mode:** Optional — one agent per part when ≥3 independent parts.
**CEO Checkpoint:** CEO owns spatial intent (Step 2) + verifies rendered geometry (Step 5). Both Core.

## Spatial Blindness Gate (MANDATORY)
LLMs fail 3D spatial cognition (Cambridge: 100% geometry failure on right-angle precision). Code-CAD mitigates but does NOT remove this. Rules:
1. AI writes code ONLY from CEO's **explicit numbers** (a dimensions table or annotated sketch). No number → AI asks, never guesses.
2. Any spatial relation (coaxial, flush, offset, between, mirrored…) must trace to a CEO value or sketch callout. AI writes `# per CEO sketch: bore coaxial with shaft, Ø12` — not its own inference.
3. **AI cannot see its own output.** After execution, CEO MUST inspect the PNG/STEP against intent. The render is the proof, not the code reading well.

## Backend Setup (one-time, offline)
```
# Python env (local, no network at runtime)
pip install build123d cadquery ocp-vscode   # build123d pulls OCP (OpenCASCADE)
# OpenSCAD: install binary separately for simple/CSG parts
```
Backend pick: **build123d** for parametric B-Rep + clean STEP (default) · **OpenSCAD** for simple CSG · **CadQuery** if CEO prefers its fluent API.

## Workflow

### Step 1: Resolve Classification + Backend (Router)
Read the project's geometry classification (set in helix-p1-validate sacred constraints; default **MẬT** if unset for any defense product).

| Label | Runtime rule | Allowed backend |
|----|----|----|
| **MẬT** (UUV, FCS, torpedo target) | Offline only — assert no network egress, no telemetry | code-CAD local **only** |
| **HẠN CHẾ** (pontoon, bia tập) | Local; cloud only on private/internal infra | code-CAD local |
| **THƯỜNG** (R&D, demo) | Free | code-CAD local (cloud allowed but unnecessary) |

> Since backend is code-CAD-local for all labels, the router's job is a **guard**: for MẬT it asserts the script imports no networked lib and writes only to the project folder. Flag `[CLASSIFICATION-VIOLATION]` and STOP if violated.

### Step 2: CEO Parametric Intent (CORE — Non-Delegable)
AI presents template, CEO fills. AI does NOT propose geometry values.
```
PARAMETRIC INTENT — {{project}} / {{part_id}}
Date: {{today}}    Classification: [MẬT/HẠN-CHẾ/THƯỜNG]
Source sketch: [reference / attach]

DIMENSIONS (CEO numbers only):
| Param | Symbol | Value | Unit | Note |
|----|----|----|----|----|

SPATIAL RELATIONS (trace each to sketch):
| Relation | Entities | Source |
|----|----|----|
(e.g., "coaxial" | bore ↔ shaft | sketch callout #3)

MATERIAL / EXPORT: [material] · units mm · export STEP + PNG
```

### Step 3: AI Writes Code-CAD Script (Offload)
- One parameterized script per part; CEO's dimensions become named variables at top.
- Comment every spatial op with its CEO source.
- No magic numbers — every value references the dimensions table.
- Save to `Phase{{N}}-.../cad/{{part_id}}.py`.

### Step 4: Execute Local → Export
```
□ Run script offline → {{part_id}}.step
□ Render isometric + 3 ortho views → {{part_id}}.png
□ Report: bounding box, volume, mass (with material density), CoG
□ Sanity asserts (e.g., wall thickness ≥ spec, no zero-volume bodies)
```

### Step 5: CEO Verifies Rendered Geometry (CORE — Spatial Blindness Gate)
```
═══ GEOMETRY VERIFY — {{part_id}} ═══
PNG matches intent?           [ ] yes  [ ] no
Bounding box vs envelope:     {{LxWxH}} vs {{limit}}
Mass vs P51 estimate:         {{kg}} vs {{target}}
Critical dims spot-check:     [ ] pass
```
CEO `no` → revise params/script, regenerate. AI never self-approves.

### Step 6: Commit + Register
- Commit `{{part_id}}.py` + `.step` + `.png` (script is source of truth).
- Register STEP in ICD (helix-p3-integrate freezes ICD v3 — geometry interface = STEP).
- Each backend handoff (P2→P3→P4→fab) = a versioned STEP, never a binary blob outside git.

## Integration Map (who calls this bridge)
| Caller | Uses bridge for |
|----|----|
| helix-p2-develop | Concept geometry to score VDI 2225 on real shapes |
| helix-p3-layout | Parametric layout of main function carriers (CEO sketch → code) |
| helix-p3-dfx | Mass props / interference inputs |
| helix-p3-bom | Extract part list + volumes from model |
| helix-p4-drawing | 3D source for 2D drawing generation (ISO 128/TCVN) |
| forge-fabrication | STEP handoff F0→F5, closing R&D→production loop |
| helix-s2c-implement | Spec-to-CAD BD: spec-driven part generation — Parametric Intent pre-filled from approved S2C spec/plan |

## Output
Save to `1_Projects/{{project}}/Phase{{N}}-.../cad/`:
- `{{part_id}}.py` (parametric source — git tracked)
- `{{part_id}}.step` (B-Rep interface)
- `{{part_id}}.png` (verification render)
- `cad_manifest.md` (part_id ↔ classification ↔ params ↔ rev)

## CEO Checkpoint
```
═══ helix-cad-bridge COMPLETE ═══
Part: {{part_id}}   Classification: {{label}}   Backend: build123d
STEP exported: ✅   Render verified by CEO: [ ]
Mass: {{kg}} (vs P51 {{target}})   BBox: {{LxWxH}}
Egress guard (MẬT): [PASS — no network lib]

CEO:
(1) ✅ Approve geometry → handoff to {{next block}}
(2) 🔄 Revise params (Core) → regenerate
(3) ⏸️ Dừng — physical mock-up / CAD review first
```

## COD
- Writing parametric code from CEO numbers: Offload (O1)
- Execution, STEP/PNG export, mass props: Offload (O2)
- **Spatial intent + dimensions: Core (C)** — design judgment, non-delegable
- **Geometry verification against render: Core (C)** — [[LLM Spatial Blindness]] gate
- **Classification label: Core (C)** — defense data control
- Egress guard enforcement: Default (D) — automated assertion
