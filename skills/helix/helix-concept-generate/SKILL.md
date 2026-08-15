---
name: helix-concept-generate
description: "Orchestrator for Pahl-Beitz Phase 2 Conceptual Design — multi-agent pipeline commanding 6 block-skills (preflight → frame → search → develop → risk → select). Each block is an independent skill that can be run, inspected, and upgraded separately. Supports --icdm flag for ICDM-enhanced pipeline. Triggers on: 'conceptual design', 'morphological matrix', 'VDI 2225', 'concept generation', 'thiet ke y tuong', 'Phase 2', 'working principles', 'firming up', 'concept evaluation'."
---

# Helix Concept Generate — Phase 2 Orchestrator (Multi-Agent Pipeline)

> **Role:** Chỉ huy trưởng (Commander) — điều phối 6 block-skills tuần tự
> **Architecture:** Modular pipeline — mỗi block = 1 skill độc lập, có thể chạy riêng, kiểm tra, nâng cấp
> **P&B Reference:** Chapter 6 (6.1–6.5.3)
> **VDI 2221:2019:** Blatt 1 (generic model) + Blatt 2 (context-specific adaptation)
> **VDI 2206:2021:** System-level integration — B0 verifies `/helix-system-arch` completed for mechatronic products
> **AI-Orchestration:** S1 (Schema v3.0) · S2 (Multi-Agent) · S3 (P02 QC) · S5 (Audit Trail)

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  helix-concept-generate (ORCHESTRATOR)           │
│                                                                  │
│  Flags: --icdm (ICDM-enhanced) | --quick (Adaptive/Variant)    │
│         --from <block> (resume from block) | --only <block>     │
│                                                                  │
│  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│  │ B0   │──▶│ BA   │──▶│ BB   │──▶│ BC   │──▶│ BD   │──▶│ BE   │
│  │PRE-  │   │FRAME │   │SEARCH│   │DEV   │   │RISK  │   │SELECT│
│  │FLIGHT│   │      │   │      │   │      │   │      │   │      │
│  └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘
│     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO
│     ▼          ▼          ▼          ▼          ▼          ▼
│  [inspect]  [inspect]  [inspect]  [inspect]  [inspect]  [inspect]
└─────────────────────────────────────────────────────────────────┘

Data Bus: 1_Projects/{{project}}/Phase2-Concept/
State:    1_Projects/{{project}}/Phase2-Concept/_pipeline_state.md
```

## VDI 2221:2019 Alignment

This pipeline implements VDI 2221:2019 (Blatt 1 + Blatt 2) principles:

- **Contextual Tailoring (Blatt 2):** Pipeline mode (standard/quick/icdm) + contextual factors in B0 preflight adapt the generic process to WX defense context. B0 classifies design type (Original/Adaptive/Variant) which calibrates decomposition depth per VDI 2221 Blatt 2 context-specific adaptation.
- **Co-evolution of Problem and Solution:** Requirements are living — if concept development (BC) or risk analysis (BD) reveals that a requirement needs updating, the change is logged in `Requirements_Delta_Log.md` and flagged at CEO checkpoint. This implements VDI 2221:2019's explicit acknowledgment that "requirements co-evolve alongside the design solution."
- **Method Ecosystem:** TRIZ + VDI 2225 + P&B + ICDM + AD + CFMA coexist as complementary methods in a self-sustaining ecosystem (not isolated "method zoo"). Each method activates where it adds unique value — TRIZ for contradictions, VDI 2225 for evaluation, AD for coupling, CFMA for failure analysis.
- **Continuous Assurance (Eigenschaftsabsicherung):** CEO checkpoints after each block = VDI 2221:2019 checkpoints. Formal gates (Gate 1-4) = phase transitions. PLAUSIBLE + P02 = assurance layer combining verification + validation throughout the process.

**VDI 2206 Three Strands Mapping:**
- **Orange strand** (core activities) = pipeline blocks B0→BA→BB→BC→BD→BE
- **Yellow strand** (continuous RE) = `Requirements_Delta_Log.md` backflow from BC/BD
- **Blue strand** (modeling mandate) = future enhancement (model inventory system TBD)
- **RFLP position:** Phase 2 = **L** (Logical) — concepts are logical solution structures before physical realization

**System-Arch Prerequisite:** For mechatronic products, B0 preflight verifies `/helix-system-arch` was completed (SA_System_Architecture.md exists). If missing → warn CEO and recommend running it before concept search.

**NLM References:**
- `Research: VDI 2221 Systematic Design (1986→2019)` (27 sources, notebook `f6e2b21f`)
- `Research: VDI 2206 V-Model Mechatronic CPS` (16 sources, notebook `3856a428`)

## Sub-Skills (6 Block-Skills)

| Block | Skill Name | P&B Section | Purpose | CEO Checkpoint |
|-------|-----------|-------------|---------|----------------|
| **B0** | `/helix-p2-preflight` | 6.1-6.3.3 | Verify Phase 1 inputs, abstraction, function structure, design type, **verify all SFs appear as morpho rows (G11)**, **classify constraints as genuine vs fictitious (§6.2)** | Approve design type + constraint classification |
| **BA** | `/helix-p2-frame` | 6.2 + TRIZ + §6.3.3 G7 | Solution-determining SF (cascade×breadth scoring), TRIZ contradictions, TESE trends, **CARS function structure variants (≥2)**, **solution-neutral test (≥3 solution classes)**, **enumerate-first if unclear** | Approve essential problems + **select function structure(s) for BB** |
| **BB** | `/helix-p2-search` | 6.4 | WP search (7 methods incl. **M5 catalogue lookup** + **M7 TRIZ→WP resolution**), **DEMAND hard filter**, DSO ranking, morphological matrix (**WP = [Effect]+[Geometry]+[Material] 3-component cells**, **[HYB] marking for cross-domain WPs**), **8-type compatibility check (Energy, Geometric, Material, Signal, Temporal, Environmental, Manufacturing, Supply chain)**, **recommended column grouping by energy domain** | Add creative WPs (H) |
| **BC** | `/helix-p2-develop` | 6.5 | Pugh screening, **AD coupling check (C1.5, Filter Before Score)**, **firming up (delegates to `/helix-p2-firmup` = Block BC2 with CRUMPLE-S method selection) → MANDATORY `Firming_Up.md` output (9 P&B properties × N concepts: performance, reliability MTBF, fault susceptibility, size L×W×H, weight, cost ±30%, service life, manufacturability, ACH readiness)**, VDI 2225 (8-step incl. **mandatory S-diagram plot via `/helix-draw s-diagram`**), TRIZ improve, **concept geometry for VDI 2225 "real shapes" (P&B §6.5.2 scale layouts) produced via [[helix-cad-bridge]] (Flow B, AI-parametric) or [[helix-cad-roundtrip]] (Flow D, human-draws-externally→import for complex shapes)**, **iteration exit: if concept fails feasibility → Back to BB with reason (CEO approves loop)** | Review coupling + weak spots + S-diagram + **firming-up property table** |
| **BC→BA** | *Backflow Assessment* | VDI 2221:2019 | If BC weak spots affect solution-determining SF → recommend BA revisit. CEO decides: loop back or proceed. See Backflow Rules below. | Approve loop / proceed |
| **BD** | `/helix-p2-risk` | WX ext. | Coupling (multi-perspective via `/helix-domain-debate` for AMBER/RED), assumptions, 3-scenario, CFMA, sensitivity | Acknowledge risks |
| **BE** | `/helix-p2-select` | 6.5.3 | P02 QC gate, CEO concept selection, handoff package (**incl. structured org transition: team/supplier/budget**) | **SELECT CONCEPT** |

## How to Use

### Full Pipeline (default)
```
/helix-concept-generate VN-XUONG-UUV
```
Runs all 6 blocks sequentially. Pauses after each block for CEO inspection.

### ICDM-Enhanced Pipeline
```
/helix-concept-generate VN-XUONG-UUV --icdm
```
Same 6 blocks + ICDM extensions injected into each block (see ICDM Extensions below).

### Quick Mode (Adaptive/Variant designs)
```
/helix-concept-generate VN-MGM-V5 --quick
```
Abbreviated pipeline: B0 (quick) → BA (skip TESE, **but calibrate depth per-SF: deep on NOVEL SFs, shallow on KNOWN**) → BB (shallow search) → BC (skip Pugh) → BD (coupling only) → BE.

### Resume from Block
```
/helix-concept-generate VN-XUONG-UUV --from BC
```
Reads pipeline state, resumes from Block C (Develop). Use when previous session completed BA/BB.

### Run Single Block
```
/helix-p2-search VN-XUONG-UUV
```
Runs only Block BB. Reads inputs from Phase2-Concept/ folder. Useful for inspection, testing, or re-running after adjustments.

## Orchestrator Workflow

When invoked, follow this EXACT sequence:

### Step 1: Parse Arguments

```
PROJECT: {{first argument — project folder name, e.g. VN-MGM}}
VARIANT: {{second argument — variant name, e.g. V5-MOTORIZED}}
         If no variant specified → use project-level root folder
FLAGS:
  --icdm    → Enable ICDM framework extensions (default: OFF)
  --quick   → Abbreviated pipeline for Adaptive/Variant (default: OFF)
  --from X  → Resume from block X (B0/BA/BB/BC/BD/BE)
  --only X  → Run single block X only
```

#### Variant Subfolder Convention

When a variant is specified, ALL outputs go into a variant subfolder under the phase folder, and ALL output filenames are prefixed with the project+variant identifier. This follows the same pattern as Phase0-Plan.

```
EXAMPLE: /helix-concept-generate VN-MGM V5-MOTORIZED

Output path: 1_Projects/VN-MGM/Phase2-Concept/V5-MOTORIZED/
File prefix: VN_MGM_V5_

Files created:
  Phase2-Concept/V5-MOTORIZED/_pipeline_state.md
  Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_B0_Preflight_Report.md
  Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_Problem_Frame.md
  Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_Morphological_Matrix.md
  Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_Concept_Variants.md
  Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_VDI_2225_Evaluation.md
  ... etc

EXAMPLE: /helix-concept-generate VN-XUONG-UUV (no variant — project level)

Output path: 1_Projects/VN-XUONG-UUV/Phase2-Concept/
File prefix: VN_XUONG_UUV_
(files at root of Phase2-Concept/)
```

**Rules:**
- Variant subfolder name = EXACT variant ID (e.g. `V5-MOTORIZED`, `N12-RETROFIT-KIT`)
- File prefix = `{{PROJECT}}_{{VARIANT_SHORT}}_` with underscores (e.g. `VN_MGM_V5_`)
- Portfolio-level files (shared across variants) stay at Phase root
- Pipeline state file always inside the variant subfolder
- Reference pattern: see `Phase0-Plan/` in any multi-variant project

### Step 1.5: Input Validation & CEO Context Enrichment

**MANDATORY before any block execution.** Read and verify all expected input files from Phase 1 and FORGE. Present a checklist to CEO.

#### 1.5a: Scan Input Files

Check for these inputs (read each file that exists to load context):

```
REQUIRED INPUTS (Phase 1 — from helix-task-clarify):
  □ {{prefix}}Requirements_List_v*.md   → validated requirements with D/W
  □ {{prefix}}Essential_Problem.md      → CEO-approved essential problem
  □ {{prefix}}Function_Structure.md     → 6-flow decomposition with SFs
  □ {{prefix}}Design_Type.md            → Original/Adaptive/Variant assessment
  □ {{prefix}}TVDT.md                   → Target Values Decision Table

RECOMMENDED INPUTS (FORGE):
  □ HOQ_Design_Parameters_v*.md         → VDI 2225 criterion weights (from /forge-job-map)
  □ ACH_Assessment_v*.md                → SHIFT scorecard (from /forge-shift)
  □ Cost_Envelope_v*.md                 → cost constraints (from /forge-cost)
  □ Opportunity_Landscape_v*.md         → underserved outcomes (from /forge-job-map)
  □ ACH_Opportunity_Scan_v*.md          → ACH opportunities (from /forge-scout)

OPTIONAL INPUTS:
  □ Product_Proposal_v*.md              → sacred constraints, risk assessment
  □ Archive/deep-dive docs              → competitor analysis, prior art
```

Glob for each in `Phase1-Task/{{variant}}/`, `Phase0-Forge/ (or FORGE/)`, `Phase0-Plan/{{variant}}/`.

#### 1.5b: Present Input Checklist to CEO

```
═══ INPUT VALIDATION — {{project}} {{variant}} — Phase 2 ═══

✅ FOUND (sẽ load làm context):
  - VN_MGM_V5_Requirements_List_v1.0.md ✅
  - ...

⚠️ MISSING (recommended):
  - HOQ_Design_Parameters_v*.md — VDI 2225 weights chưa có
    → Chạy /forge-job-map {{project}} để tạo

❌ MISSING (required — chặn pipeline):
  - Function_Structure.md — Phase 1 chưa hoàn thành
    → Chạy /helix-task-clarify {{project}} {{variant}} để hoàn thành Phase 1

CEO:
(1) ▶️ Tiếp tục với inputs hiện có
(2) 🔄 Quay lại chạy skill/phase trước:
    → /helix-task-clarify {{project}} {{variant}} (hoàn thành Phase 1)
    → /forge-job-map {{project}} (tạo HOQ weights)
    → /forge-shift {{project}} (tạo ACH assessment)
    → /forge-cost {{project}} (tạo cost envelope)
(3) 📝 Bổ sung thông tin thủ công
═══════════════════════════════════════════════════
```

If REQUIRED inputs are missing → **strongly recommend** option (2). Proceeding without required inputs will produce lower-quality output.

#### 1.5c: CEO Context Enrichment

After input validation, ALWAYS ask:

```
📋 CEO: Có thông tin bổ sung nào giúp Phase 2 sát thực tế hơn không?
Ví dụ:
  - Working principles đã biết từ kinh nghiệm / sản phẩm tương tự?
  - Ràng buộc concept cứng (phải dùng / không được dùng giải pháp nào)?
  - Kết quả bench test hoặc prototype gần đây?
  - Thông tin đối thủ / sản phẩm tham khảo mới?
  - Ngân sách / timeline cập nhật ảnh hưởng concept selection?
  - File hoặc tài liệu nào cần đọc thêm?

(Nhập thông tin hoặc "skip" để tiếp tục)
```

If CEO provides context → append to pipeline state as `## CEO Context Input`.

### Step 2: Initialize Pipeline State

Determine output path based on variant:
- With variant: `1_Projects/{{project}}/Phase2-Concept/{{variant}}/`
- Without variant: `1_Projects/{{project}}/Phase2-Concept/`

Check for existing state file: `{{output_path}}/_pipeline_state.md`

If exists → read current progress. If not → create:

```markdown
---
project: {{project}}
pipeline: helix-concept-generate v3.2
started: {{today}}
updated: {{today}}
mode: [standard | icdm | quick]
design_type: [TBD]
---

# Phase 2 Pipeline State — {{project}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|-------------|
| B0 | helix-p2-preflight | PENDING | - | - | - |
| BA | helix-p2-frame | PENDING | - | - | - |
| BB | helix-p2-search | PENDING | - | - | - |
| BC | helix-p2-develop | PENDING | - | - | - |
| BD | helix-p2-risk | PENDING | - | - | - |
| BE | helix-p2-select | PENDING | - | - | - |

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
Read `_pipeline_state.md` → "Block Ledger" section. Reconstruct context from:
- B0 initializer summary (project context, design type, constraints)
- Previous block summaries (key findings, decisions, open questions)
- CEO decisions (approvals, overrides, adjustments)
- This is ESPECIALLY critical for `--from` resume and new sessions where prior conversation context is lost.

#### Ledger Write Protocol (AFTER each block)
Append to "Block Ledger" section in `_pipeline_state.md`:
```
### {{Block ID}} — {{block name}} ({{date}})
**Key findings:** [2-3 bullet points — the essential outputs, not file listings]
**Decisions for downstream:** [what the next block needs to know]
**Open questions:** [unresolved items for CEO or next block]
**CEO checkpoint result:** [approve / revise / pause + CEO's words]
```

For each block (respecting --from / --only flags):

1. **Ledger Read:** Read `_pipeline_state.md` to reconstruct context
2. **Announce:** "Đang chạy Block {{X}}: {{block name}}..."
3. **Execute block:** Create output file(s) for this block ONLY
4. **Ledger Write:** Append block summary to "Block Ledger" section
5. **Update pipeline state:** Mark block COMPLETE in progress table
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

**Why this matters:** Each block produces deliverables that CEO must inspect. Morphological matrix needs CEO creative input. VDI 2225 weights need CEO validation. Concept selection is non-delegable. Auto-continuing creates compounding errors.

### Step 4: Pipeline Completion

After all blocks complete (or BE completes):

```
═══════════════════════════════════════════════════
PHASE 2 PIPELINE COMPLETE — {{project}}
═══════════════════════════════════════════════════
Mode: [standard / icdm / quick]
Blocks completed: {{N}}/6
Selected concept: {{concept name from BE}}

Deliverables in 1_Projects/{{project}}/Phase2-Concept/:
  [list all files]

Next: /helix-quality-gate {{project}} --gate 2
      /helix-embody-realize {{project}}
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All block-skills read/write to `{{output_path}}/` (variant subfolder if specified) using prefixed filenames.
When variant is specified, all filenames are prefixed with `{{prefix}}` (e.g. `VN_MGM_V5_`).

| File Pattern | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_pipeline_state.md` | Orchestrator | All | Pipeline progress, CEO decisions |
| `{{prefix}}B0_Preflight_Report.md` | B0 | BA, BB | Input verification, design type, guidelines check |
| `{{prefix}}Problem_Frame.md` | BA | BB, BC | Solution-determining SF, TRIZ problems, TESE analysis, **CARS function structure variants (≥2)** |
| `{{prefix}}Morphological_Matrix.md` | BB | BC, BD | Full matrix with WPs, DSO scores, compatibility |
| `{{prefix}}Concept_Variants.md` | BB | BC, BD, BE | Concept A/B/C definitions and combination paths |
| `{{prefix}}Pugh_Screening.md` | BC | BC | Pugh elimination results (if >3 concepts) |
| `{{prefix}}Firming_Up.md` | BC | BC, BD | **MANDATORY** 9 P&B properties × N concepts (performance DQM, reliability MTBF, fault susceptibility, size L×W×H, weight ±30%, cost ±30%, service life, manufacturability, ACH readiness) |
| `{{prefix}}VDI_2225_Evaluation.md` | BC | BD, BE | Full 8-step VDI evaluation with scores |
| `Concept_Geometry/` (STEP+PNG) | BC (via [[helix-cad-bridge]] Flow B / [[helix-cad-roundtrip]] Flow D) | BC, BE | VDI 2225 "real shapes" — concept scale layouts for evaluation; not yet geometry-of-record (frozen later at Phase 3 [[helix-p3-integrate]] C3a) |
| `{{prefix}}Coupling_Analysis.md` | BD | BE | Cross-domain coupling per concept |
| `{{prefix}}Assumption_Register.md` | BD | BE | Assumptions + shadow assumptions |
| `{{prefix}}CFMA.md` | BD | BE | Conceptual failure mode analysis |
| `{{prefix}}Sensitivity_Analysis.md` | BD | BE | Ranking stability under weight variation |
| `{{prefix}}P02_QC_Gate.md` | BE | — | QC gate results |
| `{{prefix}}Concept_Selection.md` | BE | Phase 3 | CEO decision + rationale |
| `{{prefix}}Handoff_Package.md` | BE | embody-realize | Weak spots, deliverable list, traceability, **resource/team implications (§6.5.3)** |
| `{{prefix}}Requirements_Delta_Log.md` | Any block | All | **MANDATORY** VDI 2221:2019 co-evolution log. Created at first delta, updated by any block that changes/adds/removes requirements. Each entry: Delta-ID, Req-ID, change type, old/new value, reason, CEO approved, propagation status. |

**Example (with variant):** `Phase2-Concept/V5-MOTORIZED/VN_MGM_V5_Morphological_Matrix.md`
**Example (no variant):** `Phase2-Concept/VN_XUONG_UUV_Morphological_Matrix.md`

**Contract rule:** Each block MUST check that its input files exist before running. If missing → report which block needs to run first.

## ICDM Extensions (--icdm flag)

> **Source:** Hari & Weiss, ICDM (Integrated Customer Driven Conceptual Design Method), Technion.
> **NLM notebooks:** `icdm`, `eqfd`, `cfma`, `icdm-research` (44 sources total).
> **Principle:** ICDM embeds customer-driven tools (EQFD, CFMA, CDTC, RTA, Robustool) into the P&B systematic framework. P&B = structure. ICDM = customer + risk + cost lenses at each step.

When `--icdm` is active, each block receives **specific methodological extensions** (not generic placeholders):

### B0 ICDM: Verify EQFD Inputs

| Check | Required Input | Source | Action if Missing |
|-------|---------------|--------|-------------------|
| EQFD outputs | CSR functions (satisfaction graphs) per top 15-20 needs | Phase 1 BB (helix-task-clarify --icdm) | Cannot run ICDM evaluation without CSR. Fall back to standard VDI 2225. |
| WTP classification | Each requirement tagged: Essential / Beneficial / Luxurious | Phase 1 BA (EQFD process) | Classify now (CEO Core task). |
| Group A/B criteria | Group A (≥70% satisfaction coverage) for screening, Group B (≥95%) for final selection | Phase 1 BE | Split criteria from requirements list. |
| Cost target (CDTC) | Target cost with WTP-derived breakdown | Phase 0 FORGE or Phase 1 | Use Cost_Envelope_v*.md as fallback. |

**Additional output:** `{{prefix}}ICDM_Input_Checklist.md`

### BA ICDM: DSO Pre-Ranking (Direct Synthesis Optimization)

**DSO replaces brute-force morphological combination.** Before synthesizing concept variants in BB:

1. **Score each WP on 2 dimensions:**
   - **Quality (Q, 1-4):** How well does this WP satisfy the sub-function's CSR target? (4 = exceeds target, 1 = barely meets)
   - **Risk (R, 1-4):** How mature/proven is this WP? (4 = COTS proven, 1 = requires new R&D)
   - **DSO Score = Q × R** (range 1-16). ≥12 = Strong. 6-11 = Viable. ≤5 = Weak.

2. **Rearrange morphological matrix:** Sort WPs left-to-right by DSO score (best = leftmost column).
   - **Left-path combination** (all column-1 WPs) = strongest baseline concept.
   - Reduces combinatorial explosion: instead of N^M combinations, evaluate ≤5 structured paths.

3. **CEO checkpoint:** Review DSO scores before BB synthesizes concepts. CEO may override Risk scores based on field knowledge.

**Additional output:** DSO scores embedded in `{{prefix}}Morphological_Matrix.md` (already in standard mode, ICDM makes it mandatory)

### BB ICDM: CSR-Aware WP Search

When `--icdm` is active, BB WP search adds:
- **WTP filter:** WPs for "Luxurious" requirements get lower priority than "Essential" WPs.
- **Service/business model row:** Add 1 morphological row for "service delivery model" (how the product is supported/maintained — not just hardware).
- **Platform commonality check:** For each WP, flag if it's shared with other portfolio variants (IRONMESH reuse score).

**Additional output:** Service model row in morpho matrix + commonality flags

### BC ICDM: CSR-Weighted Evaluation (replaces generic VDI 2225)

**ICDM evaluation uses Customer Satisfaction Rating (CSR) functions instead of generic 0-4 scoring:**

1. **CSR Functions (per criterion):**
   - Each evaluation criterion has a CSR graph/table (from Phase 1 EQFD output).
   - Achieving Target Value = 100% satisfaction. Below = decreasing %. Above = capped at 100% (no credit for over-engineering).
   - CSR can be linear, non-linear (exponential near threshold), or step-based (pass/fail).

2. **Group A Screening (ICDM Step 7):**
   - Use only Group A criteria (≥70% of total customer satisfaction weight).
   - Pugh screening against best concept as datum.
   - Eliminate concepts that fail Group A screening.

3. **Group B Full Evaluation (ICDM Step 8):**
   - Surviving concepts evaluated on Group B criteria (≥95% satisfaction coverage).
   - For each concept × each criterion: estimate performance → look up CSR function → get satisfaction %.
   - **DQM (Design Quality Measurement) = Σ (weight_i × CSR_i)** per concept.
   - DQM is the single number that compares concepts. Higher = better customer satisfaction.

4. **S-Diagram:** Plot DQM (technical quality) vs estimated unit cost. Concepts above the value line = viable.

**Additional output:** `{{prefix}}ICDM_CSR_Evaluation.md` (CSR tables + DQM scores per concept)

### BD ICDM: CFMA + CDTC + RTA (Triple Analysis)

**ICDM Step 8 mandates three concurrent analyses on ALL surviving main concepts:**

#### BD-1: CFMA (Conceptual Failure Mode Analysis)
Unlike traditional FMEA (component-based), CFMA evaluates **function-level failures:**

| Column | Content |
|--------|---------|
| System Function | From function structure (e.g., "Drive azimuth") |
| Potential Failure Mode | Loss/degradation of function (NOT component failure) |
| Failure Cause | What could cause this functional loss? |
| Failure Effect | Impact on customer/operator |
| Severity (S, 1-10) | Impact severity (10 = safety hazard) |
| Frequency (F, 1-10) | Likelihood (10 = new design, no history; 1 = prevented by standard) |
| Detection (D, 1-10) | Ability to detect during DESIGN process (not in field) |
| **SFD = S × F × D** | Priority score (max 1000) |
| Action Items | Design changes or tests to mitigate |
| **Rev SFD** | Recalculated after action items applied |

**Key difference from standard mode:** Standard BD does a simplified "CFMA" that's really just FMEA. ICDM CFMA is strictly function-based, scores SFD, and requires Rev SFD showing improvement.

**Additional output:** `{{prefix}}CFMA.md` (upgraded from generic to true CFMA format)

#### BD-2: CDTC (Conceptual Design To Cost)
Early-stage cost evaluation using Pareto principle:

1. Identify top 20% of cost factors (Pareto) that drive 80% of total cost.
2. For each surviving concept, build a **Cost Model** (materials + labor + overhead per cost factor).
3. Compare concept costs against EQFD-derived target cost (from WTP).
4. Flag concepts that exceed target cost → CEO decides: redesign, relax spec, or eliminate.

**Additional output:** CDTC section in `{{prefix}}ICDM_CSR_Evaluation.md`

#### BD-3: RTA (Risk and Time to Market Analysis)
Knowledge Gap analysis for each surviving concept:

1. **Identify Knowledge Gaps (KGs):** For each concept, what NEW knowledge/technology must WX develop or acquire? (List per concept)
2. **Gap Closing Plans:** For each KG, define: events needed, configurations, contribution to closing gap.
3. **Logic Network:** Arrange gap-closing activities into a dependency network → estimate TTM per concept.
4. **Compare TTM:** Concept with shorter TTM = lower risk. Concept with many KGs = higher risk.

**Additional output:** `{{prefix}}RTA_Knowledge_Gaps.md`

#### BD-4: Robustool (Illegitimate Operation Analysis)
For each surviving concept, evaluate:
- What happens under misuse? (operator error, wrong power, wrong weapon, extreme environment)
- What happens under upgrade? (future camera, FCS, gyro — does the concept architecture support it?)
- What happens under overload? (recoil beyond spec, sustained fire beyond duty cycle)

**Additional output:** Robustool section in `{{prefix}}CFMA.md`

### BE ICDM: DQM-Based Final Selection

**ICDM Step 9 — Final Concept Selection uses quantitative DQM comparison:**

1. **DQM Score Table:**

   | Concept | DQM (%) | CFMA Rev SFD (lower=better) | CDTC Cost vs Target | RTA TTM (weeks) | Robustool Pass? |
   |---------|:-------:|:---------------------------:|:-------------------:|:---------------:|:---------------:|
   | A       | 78%     | 120                         | -5% (under target)  | 12              | ✅               |
   | B       | 72%     | 180                         | +8% (over target)   | 16              | ⚠️               |

2. **CEO selects based on DQM + risk balance** (not just technical score).
3. **Readiness input comes from RTA, not a separate scale.** ICDM already carries concept readiness
   through the Knowledge Gap analysis in BD: KG count and severity → number of development cycles
   needed → TTM and risk index per concept. Read those off `{{prefix}}RTA_Knowledge_Gaps.md`.
   Do not introduce a second readiness score here — it double-counts RTA and disagrees with it.

> **Provenance note — do not re-add "IRL".** Earlier versions of this section scored concepts on an
> "IRL (Innovation Readiness Level), 1-5, based on ICDM criteria". Verified 2026-08-15 against the
> full ICDM corpus (Hari & Weiss 1996-2015, 15 sources): **no ICDM source mentions IRL.** The term
> belongs to the KTH Innovation Readiness Level model — six readiness dimensions scored over nine
> levels — which is an unrelated framework, and the 1-5 scale matched neither. Removed as a
> misattribution. If a readiness scale is genuinely wanted here, add it under its own name and cite
> KTH; do not present it as ICDM.

**Additional output:** `{{prefix}}ICDM_Final_Selection.md` (DQM comparison + CEO rationale)

### ICDM Data Bus Extension

When `--icdm` is active, these additional files are created:

| File Pattern | Written By | Content |
|------|-----------|---------|
| `{{prefix}}ICDM_Input_Checklist.md` | B0 | EQFD inputs, WTP, CSR, Group A/B verification |
| `{{prefix}}ICDM_CSR_Evaluation.md` | BC | CSR functions, DQM scores, CDTC cost models |
| `{{prefix}}RTA_Knowledge_Gaps.md` | BD | Knowledge gaps, gap closing plans, TTM per concept |
| `{{prefix}}ICDM_Final_Selection.md` | BE | DQM comparison table, RTA readiness read-off, CEO rationale |

Each block-skill checks for `--icdm` in pipeline state and loads ICDM methodology from this section.

## Future Extension Points

The modular architecture supports adding new frameworks via flags:

```
--icdm     → ICDM framework overlay (planned)
--axiomatic → Suh Axiomatic Design (independence/information axioms)
--topsys   → TopSys systematic innovation
--dfss     → Design for Six Sigma integration
--agile    → Agile hardware development gates
```

Each flag injects block-level extensions without modifying the core P&B pipeline.

## Integration

```
helix-concept-generate (ORCHESTRATOR) COMMANDS:
  → /helix-p2-preflight  (Block 0)
  → /helix-p2-frame      (Block A)
  → /helix-p2-search     (Block B)
  → /helix-p2-develop    (Block C)
  → /helix-p2-risk       (Block D)
  → /helix-p2-select     (Block E)

helix-concept-generate READS FROM:
  - helix-task-clarify → Phase 1 deliverables
  - forge-job-map → HOQ + ODI weights
  - forge-library → existing solution principles
  - forge-shift → ACH go/no-go
  - forge-cost → cost envelope
  - helix-cad-ingest → cad_extract.json from prior-art / RE drawings (optional, for WP shapes)

helix-concept-generate WRITES TO:
  - 1_Projects/{{project}}/Phase2-Concept/ → all deliverables
  - helix-cad-bridge → BC concept-geometry requests (Flow B parametric → STEP+PNG)
  - helix-cad-roundtrip → BC complex-shape requests (Flow D human-draws-externally→import)
  - helix-embody-realize → handoff package
  - helix-quality-gate → gate 2 readiness
  - forge-library → new solution principles
  - bridge-risk-radar → concept risks
  - helix-design-journal → session log

helix-concept-generate VISUAL OUTPUTS (via /helix-draw):
  - BA: TESE 8-Trend Radar → /helix-draw radar
  - BB: Morphological Matrix → /helix-draw morpho
  - BB: Compatibility Matrix → /helix-draw matrix
  - BB: Concept Variants Tree → /helix-draw tree
  - BC: Pugh Screening Matrix → /helix-draw matrix
  - BC: FR×DP Coupling Matrix → /helix-draw matrix
  - BC: VDI 2225 Value Profile → /helix-draw bar-chart
  - BC: S-Diagram (DQM vs Cost) → /helix-draw s-diagram
  - BD: CFMA SFD Pareto → /helix-draw bar-chart
  - BD: Sensitivity Tornado → /helix-draw bar-chart
  - BE: CEO Decision Dashboard → /helix-draw dashboard

SHARED REFERENCES (in helix-concept-generate/references/):
  - pb-conceptual-design.md — P&B Ch6 complete methodology
  - prompt-templates.md — S1 prompt templates for Phase 2
  - triz-40-principles.md — TRIZ inventive principles + matrix
  - triz-sufield-76solutions.md — Su-field analysis + 76 solutions
  - ch6-galaxy-insights.md — Galaxy notes mapped to blocks
```

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After completing each block, STOP generating content and WAIT for CEO response. NEVER execute 2+ blocks in a single turn. NEVER combine blocks (e.g., "BA+BB") without CEO explicitly requesting it. This is the #1 rule.
- **CEO checkpoint after EVERY block** — no auto-continue without explicit CEO approval ("tiếp tục", "approve", "ok", etc.)
- **Orchestrator NEVER does block work itself** — always delegates to sub-skills
- **Pipeline state file is source of truth** — always read before any action
- **Each block-skill is independently runnable** — CEO can run `/helix-p2-search` alone
- **Data bus contract is sacred** — block outputs use exact filenames above
- **Orchestrator tracks but doesn't modify** block outputs — modifications happen by re-running the block
- **BA (Frame) includes CARS mini-gate (§6.3.3 G9)** — BA outputs ≥2 function structure variants using CARS. CEO checkpoint MUST include: "Select which structure(s) proceed to BB." Document rejection rationale for eliminated structures. This screens architectures BEFORE investing in WP search.
- **BB (Search) requires CEO creative input** — AI proposes WPs, CEO MUST add/remove before proceeding
- **BE (Select) is non-delegable** — CEO selects concept, AI presents options
- **Requirements Backflow (VDI 2221:2019 Co-evolution):** If any block discovers that a Phase 1 requirement needs updating (new req, changed value, removed req), log the change in `{{prefix}}Requirements_Delta_Log.md`. Flag at CEO checkpoint: "⚠️ Requirements backflow: N requirements updated". CEO decides: accept → propagate to Requirements_List; reject → document rationale. This implements VDI 2221:2019's requirement co-evolution principle.
- **If CEO says "chạy hết" or "skip checkpoints"** — STILL stop after each block but keep checkpoint minimal (1-line summary + "tiếp tục?")
- **BB Time-Budget Checkpoint (VDI 2221:2019 §5.6):** At the end of BB, estimate cumulative pipeline effort vs the 25%/60%/15% guideline (search/combine = 25%, firm up/evaluate = 60%, select = 15%). If search phase consumed >40% of estimated total effort → flag inversion to CEO. This prevents over-investing in WP search at the expense of evaluation depth.
- **BB Morpho WP Notation (VDI 2221:2019 Blatt 1):** Every WP cell in the morphological matrix MUST include 3-component annotation: `[Effect] + [Geometry hint] + [Material hint]`. A supplementary notation table is acceptable if inline cells are too crowded. Cross-domain hybrid WPs MUST be tagged `[HYB]`.
- **BB Compatibility 8-Type Check (VDI 2221:2019):** Compatibility matrix MUST explicitly check all 8 types: Energy, Geometric, Material, Signal, **Temporal**, **Environmental**, Manufacturing, Supply chain. Missing types = audit finding.
- **BC Firming_Up.md is MANDATORY (P&B §6.5.2):** BC MUST produce a consolidated `Firming_Up.md` with **9 P&B properties** for each surviving concept: (1) Performance/DQM, (2) Reliability/MTBF, (3) Fault susceptibility, (4) Size L×W×H, (5) Weight ±30%, (6) Cost ±30%, (7) Service life, (8) Manufacturability, (9) ACH readiness. Properties may be estimated at ±30% — but ALL 9 must appear. Missing properties = audit finding.
- **Requirements_Delta_Log.md auto-creation (VDI 2221:2019 Co-evolution):** The FIRST time any block changes, adds, or removes a requirement (including cost limit changes, constraint adjustments, WP removals that affect requirements) → CREATE `Requirements_Delta_Log.md` immediately. Do NOT wait until BD to check for backflow — log deltas as they occur.

- **BC→BA Backflow Assessment (Multi-Agent Collaborative Design research, 2026-04-22):** After BC evaluation (VDI 2225 + weak spot analysis), check if weak spots affect the **solution-determining SF** (identified in BA). If YES → the essential problem may need reframing, not just WP substitution.

  ```
  BC→BA BACKFLOW ASSESSMENT:
  
  Weak spots from VDI 2225:
  | Weak Spot | SF Affected | Is Solution-Determining SF? | Severity |
  |-----------|-----------|---------------------------|---------|
  
  IF weak spot affects solution-determining SF:
    → RECOMMEND: Loop back to BA with refined essential problem
    → Rationale: Solution-determining SF weakness cascades to ALL dependent SFs
    → CEO options:
      (a) Loop to BA — reframe problem, re-run BB+BC with new frame
      (b) Loop to BB only — search additional WPs for weak SF
      (c) Proceed to BD — accept weakness, manage as risk
      (d) Abandon concept — eliminate from evaluation
  
  IF weak spots are all in NON-determining SFs:
    → Proceed to BD (normal flow)
    → Track weak spots in BD assumption register
  ```
  
  **Rule:** Max 1 BC→BA loop per pipeline run (prevent infinite recursion). If second loop needed → escalate to CEO as architectural concern.

## COD Classification

- Pipeline orchestration: Offload (O1) — mechanical sequencing
- Block execution: Offload (O2) — each block has own COD
- CEO checkpoints: **Core (C)** — inspect, approve, adjust
- Concept selection (BE): **Core (C)** — non-delegable
- Framework flag decisions (--icdm): **Core (C)** — CEO chooses methodology
- Concept geometry generation (BC via [[helix-cad-bridge]]/[[helix-cad-roundtrip]]): Offload (O2) — AI-parametric or human-drawn import under CEO review
