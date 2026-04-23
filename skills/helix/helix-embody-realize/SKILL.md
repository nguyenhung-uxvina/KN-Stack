---
name: helix-embody-realize
description: "Orchestrator for Pahl-Beitz Phase 3 Embodiment Design — multi-agent pipeline commanding 6 block-skills (preflight → layout → dfx → integrate → bom → compile). Transforms selected concept into buildable layout with DfX review, integration check, ICD v3 freeze, and draft BOM. Aligned with P&B Ch7 (7.1–7.8) + AI-Orchestration S1-S5. Triggers on: 'embodiment design', 'layout', 'DfX', 'embody', 'thiet ke tong the', 'Phase 3'."
---

# Helix Embody Realize — Phase 3 Orchestrator (Multi-Agent Pipeline)

> **Role:** Chỉ huy trưởng — điều phối 6 block-skills tuần tự
> **Architecture:** Modular pipeline — mỗi block = 1 skill độc lập
> **P&B Reference:** Ch7 (7.1–7.8) Embodiment Design
> **VDI 2221:2019:** Blatt 1 (generic model) + Blatt 2 (context-specific adaptation)
> **VDI 2206:2021:** System-level integration — BC uses VERIFICATION mode when SA exists; RFLP "P" layer
> **AI-Orchestration:** S1 (Schema v3.0) · S2 (Multi-Agent) · S3 (P02 QC) · S5 (Audit Trail)

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  helix-embody-realize (ORCHESTRATOR)             │
│                                                                  │
│  Flags: --icdm | --quick | --maritime | --from <block>          │
│         --only <block> (run single block)                       │
│                                                                  │
│  ┌──────┐   ┌──────┐   ┌────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│  │ B0   │──▶│ BA   │──▶│BA½│──▶│ BB   │──▶│ BC   │──▶│ BD   │──▶│ BE   │
│  │PRE-  │   │LAY-  │   │ERR│   │DfX   │   │INTE- │   │BOM   │   │COMP- │
│  │FLIGHT│   │OUT   │   │CHK│   │      │   │GRATE │   │      │   │ILE   │
│  └──┬───┘   └──┬───┘   └─┬─┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘
│     │ ✓CEO     │ ✓CEO    │✓CEO    │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO
└─────────────────────────────────────────────────────────────────┘

Data Bus: 1_Projects/{{project}}/Phase3-Embodiment/
State:    1_Projects/{{project}}/Phase3-Embodiment/_pipeline_state.md
```

## VDI 2221:2019 Alignment

This pipeline implements VDI 2221:2019 (Blatt 1 + Blatt 2) principles:

- **Contextual Tailoring (Blatt 2):** Pipeline mode (standard/quick/icdm/maritime) + contextual factors in B0 preflight adapt the process. VDI 2221:2019 redefines "modules" as subsystems distributed by time, organization, or interdisciplinary trades — not just physical assemblies. This affects BOM structure (BD) and integration checks (BC).
- **Co-evolution of Problem and Solution:** Requirements are living — if embodiment reveals that a requirement needs updating (e.g., DfX FAIL forces spec change, integration check reveals new interface requirement), the change is logged in `Requirements_Delta_Log.md`. Phase 3 compile (BE) includes a requirements delta summary for Gate 3 review.
- **Method Ecosystem:** DfX + PLAUSIBLE + P&B basic rules + VDI 2206 integration coexist as complementary methods. Each addresses a different design quality dimension — DfX for lifecycle concerns, PLAUSIBLE for AI output integrity, basic rules for fundamental design quality.
- **Continuous Assurance (Eigenschaftsabsicherung):** CEO checkpoints after each block = VDI 2221:2019 checkpoints. ICD v3 freeze (BC) is a major assurance milestone. PLAUSIBLE + P02 = assurance layer at Gate 3.

**VDI 2206 Three Strands Mapping:**
- **Orange strand** (core activities) = pipeline blocks B0→BA→BA½→BB→BC→BD→BE
- **Yellow strand** (continuous RE) = `Requirements_Delta_Log.md` backflow from BC (integration) and BE (compile delta summary)
- **Blue strand** (modeling mandate) = future enhancement (model inventory system TBD)
- **RFLP position:** Phase 3 = **P** (Physical) — embodiment transforms logical concepts into physical realizations

**NLM References:**
- `Research: VDI 2221 Systematic Design (1986→2019)` (27 sources, notebook `f6e2b21f`)
- `Research: VDI 2206 V-Model Mechatronic CPS` (16 sources, notebook `3856a428`)

## Sub-Skills (6 Block-Skills)

| Block | Skill Name | P&B Section | Purpose | CEO Checkpoint |
|-------|-----------|-------------|---------|----------------|
| **B0** | `/helix-p3-preflight` | 7.1 | Verify Phase 2 done, identify embodiment-determining reqs, spatial constraints | Confirm layout strategy |
| **BA** | `/helix-p3-layout` | 7.1 (Steps 2-6) | CEO creates preliminary layout, maritime P50/P51 auto-invoke | **Approve layout** (Core) |
| **BA→BB** | *(early error-check)* | 7.1 Step 6 | Lightweight error + cost check on layout BEFORE detailed DfX — catch flawed layouts early | CEO: fix layout or proceed |
| **BB** | `/helix-p3-dfx` | 7.3-7.5 | 3 basic rules (PASS/FAIL) → 5 principles rapid audit → DfX review (DfM/DfA/DfR/DfT/DfW/DfU/DfQC + DfCorrosion/DfThermal/DfDurability/DfWear/DfTransport/DfCreep; optional: DfAesthetics/DfRecycling), PLAUSIBLE 9-check | Resolve FAIL items |
| **BC** | `/helix-p3-integrate` | 7.4 | Cross-domain integration, ICD v2→v3, thermal/EMC, shadow assumptions | **Approve ICD v3 freeze** |
| **BD** | `/helix-p3-bom` | 7.1 (Steps 14) | Draft BOM, long-lead items, cost estimate, VN sourcing check | Review BOM feasibility |
| **BE** | `/helix-p3-compile` | 7.6-7.7 | **Prerequisite check** (all variants same concreteness? costs estimable?) → Embodiment eval (Rt/Re + S-diagram), weak spot elimination (value profile chart), P02 QC gate, deliverables. **Return-to-concept trigger:** any D=0 or ≥3 D=1 → flag RECOMMEND RETURN TO PHASE 2 | Approve for Gate 3 |

## How to Use

### Full Pipeline
```
/helix-embody-realize VN-XUONG-UUV
```

### Maritime Mode (auto-invoke P50/P51 in Block BA)
```
/helix-embody-realize VN-USV-SS-001 --maritime
```

### ICDM-Enhanced / Quick / Resume / Single Block
```
/helix-embody-realize VN-XUONG-UUV --icdm
/helix-embody-realize VN-MGM-V5 --quick
/helix-embody-realize VN-XUONG-UUV --from BC
/helix-p3-dfx VN-XUONG-UUV
```

### Quick Mode (--quick) Abbreviated Sequence
B0 (quick) → BA (skip P50/P51 unless maritime) → BA½ (error-check always runs) → BB (DfX core + DfCorrosion if maritime, skip PLAUSIBLE + extended DfX) → BC (ICD update only, skip shadow) → BD (BOM from template) → BE (skip Rt/Re, QC gate only).

## Orchestrator Workflow

### Step 1: Parse Arguments

```
PROJECT: {{first argument — project folder name, e.g. VN-MGM}}
VARIANT: {{second argument — variant name, e.g. V5-MOTORIZED}}
         If no variant specified → use project-level root folder
FLAGS:
  --icdm     → ICDM framework extensions (default: OFF)
  --quick    → Abbreviated pipeline (default: OFF)
  --maritime → Auto-invoke P50/P51 in Block BA (default: auto-detect)
  --from X   → Resume from block X (B0/BA/BB/BC/BD/BE)
  --only X   → Run single block X only
```

#### Variant Subfolder Convention

When a variant is specified, ALL outputs go into a variant subfolder under the phase folder, and ALL output filenames are prefixed with the project+variant identifier. This follows the same pattern as Phase0-Plan.

```
EXAMPLE: /helix-embody-realize VN-MGM V5-MOTORIZED

Output path: 1_Projects/VN-MGM/Phase3-Embody/V5-MOTORIZED/
File prefix: VN_MGM_V5_

Files created:
  Phase3-Embody/V5-MOTORIZED/_pipeline_state.md
  Phase3-Embody/V5-MOTORIZED/VN_MGM_V5_B0_Preflight_Report.md
  Phase3-Embody/V5-MOTORIZED/VN_MGM_V5_Preliminary_Layout.md
  Phase3-Embody/V5-MOTORIZED/VN_MGM_V5_DfX_Review.md
  Phase3-Embody/V5-MOTORIZED/VN_MGM_V5_BOM_Draft.md
  ... etc

EXAMPLE: /helix-embody-realize VN-XUONG-UUV (no variant — project level)

Output path: 1_Projects/VN-XUONG-UUV/Phase3-Embody/
File prefix: VN_XUONG_UUV_
```

**Rules:**
- Variant subfolder name = EXACT variant ID (e.g. `V5-MOTORIZED`, `N12-RETROFIT-KIT`)
- File prefix = `{{PROJECT}}_{{VARIANT_SHORT}}_` with underscores (e.g. `VN_MGM_V5_`)
- Portfolio-level files (shared across variants) stay at Phase root
- Pipeline state file always inside the variant subfolder
- Reference pattern: see `Phase0-Plan/` in any multi-variant project

### Step 1.5: Input Validation & CEO Context Enrichment

**MANDATORY before any block execution.** Read and verify all expected input files from Phase 2, Phase 1, and FORGE. Present checklist to CEO.

#### 1.5a: Scan Input Files

Check for these inputs (read each file that exists to load context):

```
REQUIRED INPUTS (Phase 2 — from helix-concept-generate):
  □ {{prefix}}Concept_Selection.md      → CEO-selected concept + rationale
  □ {{prefix}}Handoff_Package.md        → weak spots, deliverable list, traceability
  □ {{prefix}}VDI_2225_Evaluation.md    → concept scores for reference
  □ {{prefix}}Morphological_Matrix.md   → WP selections per sub-function

REQUIRED INPUTS (Phase 1 — from helix-task-clarify):
  □ {{prefix}}Requirements_List_v*.md   → requirements for DfX checks
  □ {{prefix}}Function_Structure.md     → SF mapping for integration check

RECOMMENDED INPUTS (FORGE):
  □ Cost_Envelope_v*.md                 → cost targets for BOM check (from /forge-cost)
  □ ACH_Assessment_v*.md                → ACH/fallback constraints for DfU (from /forge-shift)
  □ HOQ_Design_Parameters_v*.md         → weighted DPs (from /forge-job-map)

OPTIONAL INPUTS:
  □ Product_Proposal_v*.md              → sacred constraints
  □ Bench test / prototype results      → empirical data for layout
```

Glob for each in `Phase2-Concept/{{variant}}/`, `Phase1-Task/{{variant}}/`, `Phase0-Forge/ (or FORGE/)`, `Phase0-Plan/{{variant}}/`.

#### 1.5b: Present Input Checklist to CEO

```
═══ INPUT VALIDATION — {{project}} {{variant}} — Phase 3 ═══

✅ FOUND (sẽ load làm context):
  - VN_MGM_V5_Concept_Selection.md ✅
  - VN_MGM_V5_Requirements_List_v1.0.md ✅
  - ...

⚠️ MISSING (recommended):
  - Cost_Envelope_v*.md — BOM check sẽ thiếu cost targets
    → Chạy /forge-cost {{project}} để tạo

❌ MISSING (required — chặn pipeline):
  - Concept_Selection.md — Phase 2 chưa hoàn thành
    → Chạy /helix-concept-generate {{project}} {{variant}} để hoàn thành Phase 2
  - Handoff_Package.md — Phase 2 select chưa chạy
    → Chạy /helix-p2-select {{project}} {{variant}}

CEO:
(1) ▶️ Tiếp tục với inputs hiện có
(2) 🔄 Quay lại chạy skill/phase trước:
    → /helix-concept-generate {{project}} {{variant}} (hoàn thành Phase 2)
    → /helix-task-clarify {{project}} {{variant}} (bổ sung Phase 1)
    → /forge-cost {{project}} (tạo cost envelope)
    → /forge-shift {{project}} (tạo ACH assessment)
(3) 📝 Bổ sung thông tin thủ công
═══════════════════════════════════════════════════
```

If REQUIRED inputs are missing → **strongly recommend** option (2). Phase 3 without concept selection = building the wrong thing.

#### 1.5c: CEO Context Enrichment

After input validation, ALWAYS ask:

```
📋 CEO: Có thông tin bổ sung nào giúp Phase 3 sát thực tế hơn không?
Ví dụ:
  - Kết quả bench test / prototype gần đây?
  - Supplier quotes hoặc material availability updates?
  - CNC/manufacturing constraints mới phát hiện?
  - Kết quả DfX từ sản phẩm tương tự (lessons learned)?
  - Thay đổi ICD hoặc integration requirements?
  - Spatial constraints từ platform / installation site?
  - File hoặc tài liệu nào cần đọc thêm?

(Nhập thông tin hoặc "skip" để tiếp tục)
```

If CEO provides context → append to pipeline state as `## CEO Context Input`.

### Step 2: Initialize Pipeline State

Determine output path based on variant:
- With variant: `1_Projects/{{project}}/Phase3-Embody/{{variant}}/`
- Without variant: `1_Projects/{{project}}/Phase3-Embody/`

Check/create `{{output_path}}/_pipeline_state.md`:

```markdown
---
project: {{project}}
pipeline: helix-embody-realize v3.2
started: {{today}}
updated: {{today}}
mode: [standard | icdm | quick]
maritime: [true | false]
---

# Phase 3 Pipeline State — {{project}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|-------------|
| B0 | helix-p3-preflight | PENDING | - | - | - |
| BA | helix-p3-layout | PENDING | - | - | - |
| BB | helix-p3-dfx | PENDING | - | - | - |
| BC | helix-p3-integrate | PENDING | - | - | - |
| BD | helix-p3-bom | PENDING | - | - | - |
| BE | helix-p3-compile | PENDING | - | - | - |

## Block Ledger
> **Purpose:** Sole communication channel between blocks. Each block reads this section for context, then appends its summary. Enables crash recovery and context-free resume.

[Each block appends one entry below when complete — see Ledger Write Protocol]

## CEO Decisions
[populated at each checkpoint]

## Adjustments Log
[populated when CEO modifies block outputs between runs]
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ CRITICAL RULE: Execute EXACTLY ONE block per turn. After completing a block, STOP and WAIT for CEO response. DO NOT proceed to the next block until CEO explicitly approves. DO NOT combine multiple blocks. DO NOT auto-continue.**

**Architecture: Initializer + Incremental + Ledger** (Source: Anthropic Agent Harness, Tier A)
- B0 (Preflight) = **Initializer** — validates inputs, populates ledger with project context
- BA-BE = **Incremental Agents** — each reads ledger, does work, writes back
- `_pipeline_state.md` = **State Ledger** — the SOLE communication channel between blocks

#### Ledger Read Protocol (BEFORE each block)
Read `_pipeline_state.md` → "Block Ledger" section. Reconstruct context from previous block summaries, CEO decisions, and open questions. Critical for `--from` resume and new sessions.

#### Ledger Write Protocol (AFTER each block)
Append to "Block Ledger" section in `_pipeline_state.md`:
```
### {{Block ID}} — {{block name}} ({{date}})
**Key findings:** [2-3 bullet points — essential outputs]
**Decisions for downstream:** [what next block needs to know]
**Open questions:** [unresolved items for CEO or next block]
**CEO checkpoint result:** [approve / revise / pause + CEO's words]
```

For each block (respecting --from / --only flags):

1. **Ledger Read:** Read `_pipeline_state.md` to reconstruct context
2. **Announce:** "Đang chạy Block {{X}}: {{block name}}..."
3. **Execute block:** Create output file(s) for this block ONLY
4. **Ledger Write:** Append block summary to "Block Ledger" section
5. **Update pipeline state:** Mark block COMPLETE
6. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK {{X}} COMPLETE ═══
   Deliverables: [list files created/updated]
   Key findings: [1-3 bullet points]
   
   CEO:
   (1) ✅ Approve → tiếp tục Block {{next}}
   (2) 🔄 Chạy lại Block {{X}} với điều chỉnh: [mô tả]
   (3) ⏸️ Dừng pipeline — kiểm tra kết quả trước
   (4) ⏭️ Skip Block {{next}} (nếu không cần thiết)
   ```
7. **⛔ WAIT for CEO message.** Do NOT generate any further content until CEO responds.
8. **On CEO response:**
   - (1) → Execute next block (ONE block only, then STOP again)
   - (2) → Re-run current block with adjustments, then STOP for approval
   - (3) → Save state and halt. CEO can resume later with `--from`
   - (4) → Skip next block, STOP and present the block after that

**Why this matters:** Layout decisions (BA) affect ALL downstream blocks. DfX findings (BB) may require layout changes. BOM (BD) depends on frozen ICD (BC). Auto-continuing cascades errors through the physical design.

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
PHASE 3 PIPELINE COMPLETE — {{project}}
═══════════════════════════════════════════════════
Mode: [standard / icdm / quick]
Blocks completed: {{N}}/6
Rt = {{value}}, Re = {{value}}, R = {{value}}
BOM cost: {{amount}} vs target {{amount}}
ICD v3: [FROZEN / PENDING]

Deliverables in 1_Projects/{{project}}/Phase3-Embodiment/:
  [list all files]

Next: /helix-quality-gate {{project}} --gate 3
      /helix-detail-finalize {{project}}
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files are placed in `{{output_path}}/` (variant subfolder if variant specified, phase root otherwise).
When variant is specified, all filenames are prefixed with `{{prefix}}` (e.g. `VN_MGM_V5_`).

| File Pattern | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_pipeline_state.md` | Orchestrator | All | Progress, CEO decisions |
| `{{prefix}}B0_Preflight_Report.md` | B0 | BA, BB | Embodiment-determining reqs, spatial constraints |
| `{{prefix}}Preliminary_Layout.md` | BA | BB, BC, BD | Layout description, key dimensions, material candidates |
| `{{prefix}}Weight_Estimate.md` | BA | BD, BE | P51 bottom-up weight (maritime only) |
| `{{prefix}}Stability_Check.md` | BA | BE | P50 GM/trim check (maritime only) |
| `{{prefix}}DfX_Review.md` | BB | BC, BE | 16 DfX (DfM/DfA/DfR/DfT/DfW/DfU/DfQC/DfCorrosion/DfThermal/DfDurability/DfWear/DfTransport/DfCreep + optional DfAesthetics/DfRecycling) + 5 Principles Audit, each OK/WARN/FAIL |
| `{{prefix}}PLAUSIBLE_Check.md` | BB | BE | 9-check PLAUSIBLE results |
| `{{prefix}}Basic_Rules_Audit.md` | BB | BE | Clarity/Simplicity/Safety assessment |
| `{{prefix}}Integration_Check.md` | BC | BD, BE | Interface verification, thermal, EMC |
| `{{prefix}}ICD_v3.md` | BC | Phase 4 | Frozen interfaces (after CEO approval) |
| `{{prefix}}Shadow_Assumptions.md` | BC | BE | Cross-domain assumption validation |
| `{{prefix}}BOM_Draft.md` | BD | BE | Preliminary BOM with costs, sourcing |
| `{{prefix}}Long_Lead_Items.md` | BD | BE | Items requiring early procurement |
| `{{prefix}}Embodiment_Evaluation.md` | BE | Gate 3 | Rt/Re scores, S-diagram, weak spots |
| `{{prefix}}P02_QC_Gate.md` | BE | Gate 3 | QC gate results |
| `{{prefix}}Deliverables_Index.md` | BE | Phase 4 | Complete deliverable list |

**Example (with variant):** `Phase3-Embody/V5-MOTORIZED/VN_MGM_V5_BOM_Draft.md`
**Example (no variant):** `Phase3-Embody/VN_XUONG_UUV_BOM_Draft.md`

## ICDM Extensions (--icdm flag)

> **Source:** Hari & Weiss, ICDM Steps 8-10 + CDTC + RTA, Technion.
> **NLM notebooks:** `icdm`, `icdm-research`, `cfma` (29 sources).
> **Maps to:** ICDM Step 8 (Preliminary Design + Analysis), Step 10 (Project Launch / Gap Closing).

When `--icdm` is active, each block receives **specific ICDM methodological extensions:**

### B0 ICDM: Load Phase 2 ICDM Outputs + Gap Closing Plan

- **Required ICDM inputs from Phase 2:**
  - `ICDM_CSR_Evaluation.md` → DQM scores, CSR functions, CDTC cost model
  - `RTA_Knowledge_Gaps.md` → Knowledge gaps, gap closing plans, TTM estimate
  - `CFMA.md` → Function-level failure analysis with SFD scores + Robustool
  - `ICDM_Final_Selection.md` → CEO selection rationale with DQM comparison
- **Gap Closing Plan activation:** Each Knowledge Gap from RTA becomes a Phase 3 task:
  - KG with high severity → Phase 3 prototype/test MUST address this gap BEFORE detail design.
  - KG with low severity → can resolve during detail design.
- **CDTC cost model refinement:** As embodiment progresses, CDTC Pareto cost factors get refined with actual BOM data.

### BA ICDM: CSR-Guided Layout

- **Layout priorities from CSR:** Use Group A criteria (≥70% satisfaction weight) to guide layout decisions:
  - Higher CSR weight → more design attention in layout.
  - If layout forces a CSR trade-off → document and escalate to CEO.
- **Architecture from ICDM Step 8:** Preliminary design decisions (make/buy, interfaces, manufacturing processes) from Phase 2 BD are now realized in layout.

### BB ICDM: Extended DfX + Robustool Refinement

- **Robustool follow-up:** Phase 2 BD identified illegitimate operation risks. Phase 3 BB must verify that embodiment layout addresses each Robustool finding:
  - Misuse protection designed in?
  - Upgrade path physically possible?
  - Overload tolerance verified by analysis?
- **DfUpgradeability:** Explicit check that ICDM platform requirements (IX-01 to IX-07 from Phase 1) are physically embodied in layout (e.g., expansion ports, mounting points, I/O reserves).

### BC ICDM: CDTC Refinement + CFMA Update

- **CDTC Stage 6:** Compare actual BOM cost against Phase 2 CDTC cost model. Update cost tree with real data.
  - If actual > target: identify Pareto cost factors → propose value engineering.
  - If actual < target: document savings → allocate to future-proofing features.
- **CFMA update:** Phase 2 CFMA was function-level. Phase 3 refines to component-level where embodiment provides sufficient detail. Update SFD → Rev SFD with embodiment data.

### BD ICDM: Cost Model in BOM

- **CDTC cost tree embedded in BOM:** Each BOM line item tagged with CDTC cost factor. Top 20% Pareto items highlighted.
- **WTP verification:** Cross-check BOM cost breakdown against WTP categories:
  - Essential functions → cost must be within WTP Essential budget.
  - Beneficial functions → cost within WTP Beneficial premium.
  - Luxurious functions → cost must be near-zero (customer won't pay).

### BE ICDM: DQM Re-evaluation at Gate 3

- **Re-calculate DQM with embodiment data:** Same CSR functions from Phase 1, but now with actual (not estimated) performance values from Phase 3 analysis/test.
  - DQM should INCREASE from Phase 2 estimate (better data → more accurate → higher confidence).
  - If DQM DECREASES → weak spot identified → CEO decides: fix or accept.
- **RTA TTM update:** Update Knowledge Gap status. Which gaps were closed during Phase 3? Which remain for Phase 4?
- **ICDM Innovation Maturity Level:** Score for Gate 3 readiness.

### ICDM Data Bus Extension (Phase 3)

| File Pattern | Written By | Content |
|------|-----------|---------|
| `{{prefix}}CDTC_Cost_Model_v2.md` | BD | Refined cost tree with actual BOM data |
| `{{prefix}}CFMA_v2.md` | BC | Updated CFMA with component-level data |
| `{{prefix}}RTA_Gap_Status.md` | BE | Knowledge gap closure status |
| `{{prefix}}DQM_Gate3.md` | BE | Re-calculated DQM with embodiment performance |

## Integration

```
helix-embody-realize (ORCHESTRATOR) COMMANDS:
  → /helix-p3-preflight   (Block 0)
  → /helix-p3-layout      (Block A)
  → /helix-p3-dfx         (Block B)
  → /helix-p3-integrate   (Block C)
  → /helix-p3-bom         (Block D)
  → /helix-p3-compile     (Block E)

helix-embody-realize READS FROM:
  - helix-concept-generate → BE_Concept_Selection, BE_Handoff_Package
  - helix-task-clarify → requirements for DfX checks
  - forge-cost → cost envelope
  - forge-shift → ACH/fallback constraints for DfU

helix-embody-realize WRITES TO:
  - 1_Projects/{{project}}/Phase3-Embodiment/ → all deliverables
  - helix-detail-finalize → frozen layout + BOM for Phase 4
  - helix-quality-gate → Gate 3 readiness
  - ICD v3 → frozen interfaces
  - bridge-risk-radar → integration risks
  - forge-library → new components cataloged
  - helix-design-journal → session log

helix-embody-realize VISUAL OUTPUTS (via /helix-draw):
  - BA: Preliminary Layout → /helix-draw block-diagram
  - BA: Weight Estimate (maritime) → /helix-draw bar-chart
  - BB: Basic Rules Audit (3) → /helix-draw radar
  - BB: 5 Design Principles → /helix-draw radar
  - BB: DfX Review (7 categories) → /helix-draw dashboard
  - BB: PLAUSIBLE 9-Check → /helix-draw radar
  - BC: Interface Verification → /helix-draw block-diagram
  - BC: ICD v3 Diagram → /helix-draw block-diagram
  - BD: BOM Cost Breakdown → /helix-draw bar-chart
  - BD: Cost Drivers Pareto → /helix-draw bar-chart
  - BE: S-Diagram (Rt vs Re) → /helix-draw s-diagram
  - BE: Weak Spot Value Profile → /helix-draw bar-chart
  - BE: P02 QC Gate Phase 3 → /helix-draw dashboard

SHARED REFERENCES (in helix-embody-realize/references/):
  - pb-embodiment-design.md → P&B Ch7 methodology reference
  - prompt-templates.md → S1 templates for Phase 3
```

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After completing each block, STOP generating content and WAIT for CEO response. NEVER execute 2+ blocks in a single turn. NEVER combine blocks without CEO explicitly requesting it. This is the #1 rule.
- **CEO checkpoint after EVERY block** — no auto-continue without explicit CEO approval ("tiếp tục", "approve", "ok", etc.)
- **Orchestrator NEVER does block work itself** — always delegates to sub-skills
- **Pipeline state file is source of truth** — always read before any action
- **Each block-skill is independently runnable** — CEO can run `/helix-p3-dfx` alone
- **Data bus contract is sacred** — block outputs use exact filenames in Data Bus table
- **Orchestrator tracks but doesn't modify** block outputs — modifications happen by re-running the block
- **AI NEVER generates initial layout** — that is Core (CEO judgment)
- **ICD v3 freeze requires EXPLICIT CEO approval**
- **Requirements Backflow (VDI 2221:2019 Co-evolution):** If any block discovers that a Phase 1 requirement needs updating (e.g., DfX FAIL forces spec change, integration reveals new interface requirement, BOM shows cost target unachievable), log the change in `{{prefix}}Requirements_Delta_Log.md`. Flag at CEO checkpoint. BE compile includes a requirements delta summary for Gate 3 review. CEO decides: accept → propagate to Requirements_List; reject → document rationale.
- **Any DfX FAIL severity H must be resolved before Phase 4**
- **DfCorrosion FAIL on --maritime products → BLOCKING, cannot proceed to Gate 3**
- **Block BA½ (early error-check):** After BA layout, before BB DfX — quick check: obvious force-path errors? cost-effectiveness concern? disturbing factors? If YES → return to BA with specific fix, don't waste detailed DfX effort on flawed layout (P&B 7.1 Step 6)
- **Block BE prerequisite check:** Before Rt/Re scoring — are all variants at same degree of concreteness? Are manufacturing costs estimable? If NO → flag to CEO before scoring
- **Block BE return-to-concept trigger:** If any demand criterion scores 0, or ≥3 demands score 1 → output "⚠️ RECOMMEND RETURN TO PHASE 2" with failing criteria. CEO decides (Core)
- **PLAUSIBLE L-check (Lethality) FAIL → STOP immediately**
- **If CEO says "chạy hết" or "skip checkpoints"** — STILL stop after each block but keep checkpoint minimal (1-line summary + "tiếp tục?")

## COD Classification

- Pipeline orchestration: Offload (O1)
- Block execution: Offload (O2) — each block has own COD
- CEO checkpoints: **Core (C)** — inspect, approve, adjust
- **Initial layout creation: Core (C)** — non-delegable
- **Design trade-off resolution: Core (C)**
- **ICD v3 freeze: Core (C)** — commitment with consequences
- Framework flag decisions (--icdm, --maritime): **Core (C)** — CEO chooses
