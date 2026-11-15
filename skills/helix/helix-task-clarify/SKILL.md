---
name: helix-task-clarify
description: "Orchestrator for Pahl-Beitz Phase 1 Task Clarification — multi-agent pipeline commanding 6 block-skills (preflight → requirements → validate → abstract → structure → compile). Each block is an independent skill. Supports --icdm flag for ICDM extensions. Aligned with P&B Ch5 (5.1–5.4) + Ch6.1–6.3 + AI-Orchestration S1-S5. Triggers on: 'task clarification', 'requirements', 'lam ro yeu cau', 'Phase 1', 'req', 'yeu cau'."
---

# Helix Task Clarify — Phase 1 Orchestrator (Multi-Agent Pipeline)

> **Role:** Chỉ huy trưởng (Commander) — điều phối 6 block-skills tuần tự
> **Architecture:** Modular pipeline — mỗi block = 1 skill độc lập
> **P&B Reference:** Ch5 (5.1–5.4) Task Clarification + Ch6.1–6.3 (Abstraction, Function Structure)
> **VDI 2221:2019:** Blatt 1 (generic model) + Blatt 2 (context-specific adaptation)
> **VDI 2206:2021:** System-level integration — mechatronic products route to `/helix-system-arch` after Gate 1
> **AI-Orchestration:** S1 (Schema v3.0) · S2 (Multi-Agent) · S3 (P02 QC) · S5 (Audit Trail)

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  helix-task-clarify (ORCHESTRATOR)               │
│                                                                  │
│  Flags: --icdm | --quick | --from <block> | --only <block>      │
│                                                                  │
│  ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐
│  │ B0   │──▶│ BA   │──▶│ BB   │──▶│ BC   │──▶│ BD   │──▶│ BE   │
│  │PRE-  │   │REQUI-│   │VALI- │   │ABSTR-│   │STRU- │   │COMP- │
│  │FLIGHT│   │REMEN │   │DATE  │   │ACT   │   │CTURE │   │ILE   │
│  └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘   └──┬───┘
│     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO     │ ✓CEO
└─────────────────────────────────────────────────────────────────┘

Data Bus: 1_Projects/{{project}}/Phase1-Task/
State:    1_Projects/{{project}}/Phase1-Task/_pipeline_state.md
```

## VDI 2221:2019 Alignment

This pipeline implements VDI 2221:2019 (Blatt 1 + Blatt 2) principles:

- **Contextual Tailoring (Blatt 2):** Pipeline mode (standard/quick/icdm) + contextual factors in B0 preflight adapt the generic process to WX defense context. Use `--quick` for Variant/Adaptive, full pipeline for Original. B0 assesses external factors (legislation, market, customer type) and internal factors (company capability, product novelty, batch size, team composition) per VDI 2221 Blatt 2.
- **Co-evolution of Problem and Solution:** Requirements are living — VDI 2221:2019 explicitly states that requirements co-evolve alongside the design solution. Requirements tagged `[CONCEPT]`/`[EMBODY]`/`[LATE]` may be updated in Phase 2/3 via `Requirements_Delta_Log.md`. CEO approves all changes.
- **Method Ecosystem:** P&B systematic design + TRIZ + VDI 2225 + ICDM + Axiomatic Design coexist as complementary methods in a self-sustaining ecosystem (not isolated "method zoo"). Each method activates where it adds unique value.
- **Continuous Assurance (Eigenschaftsabsicherung):** CEO checkpoints after each block = VDI 2221:2019 checkpoints. Formal gates (Gate 1-4) = phase transitions. PLAUSIBLE + P02 = assurance layer combining verification + validation.
- **Functional Architecture:** VDI 2221:2019 defines function structure as "functional architecture" — solution-neutral description of purely functional relationships. Aligns with RFLP framework (Requirements → Functional → Logical → Physical).

**VDI 2206 Three Strands Mapping:**
- **Orange strand** (core activities) = pipeline blocks B0→BA→BB→BC→BD→BE
- **Yellow strand** (continuous RE) = `Requirements_Delta_Log.md` backflow mechanism
- **Blue strand** (modeling mandate) = future enhancement (model inventory system TBD)
- **RFLP position:** Phase 1 = **R** (Requirements) + **F** (Functional architecture in BD)

**System-Arch Routing:** After Gate 1, if product is mechatronic (≥2 domains), route to `/helix-system-arch` BEFORE Phase 2. Pipeline completion (BE) should recommend this routing.

**NLM References:**
- `Research: VDI 2221 Systematic Design (1986→2019)` (27 sources, notebook `f6e2b21f`)
- `Research: VDI 2206 V-Model Mechatronic CPS` (16 sources, notebook `3856a428`)

## Sub-Skills (6 Block-Skills)

| Block | Skill Name | P&B Section | Purpose | CEO Checkpoint |
|-------|-----------|-------------|---------|----------------|
| **B0** | `/helix-p1-preflight` | 5.1 | Verify Phase 0 done, gather context, stakeholder map, standards scan | Confirm scope & stakeholders |
| **BA** | `/helix-p1-requirements` | 5.2 | Generate 50-80 requirements from standards + similar products + context | Review draft, add field knowledge |
| **BB** | `/helix-p1-validate` | 5.2-5.3 | Human D/W classification (D/W+/W/W-), gap analysis, failure-derived reqs, solution-idea isolation → Solution_Ideas_Log | **Classify D/W** (Core) |
| **BC** | `/helix-p1-abstract` | 6.1-6.2, 5.3 | 5-step abstraction, essential problem, TVDT (Target Values) | **Approve essential problem** |
| **BD** | `/helix-p1-structure` | 6.3 | 6-flow function structure, SF decomposition, design type assessment | Validate function structure |
| **BE** | `/helix-p1-compile` | 5.4 | Cross-domain sync S1, P02 QC gate, department objection check, compile 8 deliverables | Approve for Gate 1 |

## How to Use

### Full Pipeline (default)
```
/helix-task-clarify VN-XUONG-UUV
```

### ICDM-Enhanced Pipeline
```
/helix-task-clarify VN-XUONG-UUV --icdm
```

### Quick Mode (simple products or retroactive documentation)
```
/helix-task-clarify VN-MGM-V1 --quick
```
Abbreviated: B0 (quick) → BA (from archive) → BB (confirm D/W) → BC (skip TVDT) → BD (shallow) → BE.

### Resume / Single Block
```
/helix-task-clarify VN-XUONG-UUV --from BC
/helix-p1-requirements VN-XUONG-UUV
```

## Orchestrator Workflow

### Step 1: Parse Arguments

```
PROJECT: {{first argument — project folder name, e.g. VN-MGM}}
VARIANT: {{second argument — variant name, e.g. V5-MOTORIZED}}
         If no variant specified → use project-level root folder
FLAGS:
  --icdm    → ICDM framework extensions
  --quick   → Abbreviated for simple/retroactive products
  --from X  → Resume from block X
  --only X  → Run single block X only
```

#### Variant Subfolder Convention

When a variant is specified, ALL outputs go into a variant subfolder under the phase folder, and ALL output filenames are prefixed with the project+variant identifier. This follows the same pattern as Phase0-Plan.

```
EXAMPLE: /helix-task-clarify VN-MGM V5-MOTORIZED

Output path: 1_Projects/VN-MGM/Phase1-Task/V5-MOTORIZED/
File prefix: VN_MGM_V5_

Files created:
  Phase1-Task/V5-MOTORIZED/_pipeline_state.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_B0_Preflight_Report.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Requirements_List_v1.0.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Abstraction.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Essential_Problem.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_TVDT.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Function_Structure.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Design_Type.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_P02_QC_Gate.md
  Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Deliverables_Index.md

EXAMPLE: /helix-task-clarify VN-MGM (no variant — project level)

Output path: 1_Projects/VN-MGM/Phase1-Task/
File prefix: VN_MGM_
(files at root of Phase1-Task/, same as before)
```

**Rules:**
- Variant subfolder name = EXACT variant ID (e.g. `V5-MOTORIZED`, `N12-RETROFIT-KIT`)
- File prefix = `{{PROJECT}}_{{VARIANT_SHORT}}_` with underscores (e.g. `VN_MGM_V5_`)
- Portfolio-level files (shared across variants) stay at Phase root
- Pipeline state file always inside the variant subfolder
- Reference pattern: see `Phase0-Plan/` in any multi-variant project

### Step 1.5: Input Validation & CEO Context Enrichment

**MANDATORY before any block execution.** Read and verify all expected input files. Present a checklist to CEO showing what's available and what's missing.

#### 1.5a: Scan Input Files

Check for these inputs (read each file that exists to load context):

```
REQUIRED INPUTS (Phase 0):
  □ Product_Planning_v*.md    → scope, stakeholders, cost targets
  □ Product_Proposal_v*.md    → IFR, sacred constraints, TRIZ resources
  □ Portfolio_Planning_v*.md  → variant strategy, synergy map (if multi-variant)

RECOMMENDED INPUTS (FORGE — Phase 0-Forge):
  □ Job_Map_v*.md             → 8-step JTBD (from /forge-job-map)
  □ Desired_Outcomes_v*.md    → ODI outcomes with I×S scores
  □ Opportunity_Landscape_v*.md → ranked underserved/overserved
  □ HOQ_Design_Parameters_v*.md → weighted DPs for VDI 2225
  □ ACH_Assessment_v*.md      → SHIFT scorecard (from /forge-shift)
  □ Cost_Envelope_v*.md       → cost targets + LCC (from /forge-cost)
  □ ACH_Opportunity_Scan_v*.md → ACH opportunities (from /forge-scout)

OPTIONAL INPUTS:
  □ helix-project-init charter → project charter, ICD v0
  □ Archive/deep-dive docs    → previous phase data for retroactive products
  □ 3_Resources/Technical-References/ → MIL-STD, STANAG applicable
```

Glob for each file pattern in `Phase0-Plan/`, `Phase0-Plan/{{variant}}/`, `Phase0-Forge/ (or FORGE/)`, and project root.

#### 1.5b: Present Input Checklist to CEO

```
═══ INPUT VALIDATION — {{project}} {{variant}} ═══

✅ FOUND (will be loaded as context):
  - Product_Planning_v1.0.md (Phase0-Plan/)
  - ...

⚠️ MISSING (recommended but not blocking):
  - Job_Map_v*.md — /forge-job-map chưa chạy
  - ACH_Assessment_v*.md — /forge-shift chưa chạy

❌ MISSING (required — may block pipeline quality):
  - Product_Proposal_v*.md — /plan chưa tạo proposal

CEO:
(1) ▶️ Tiếp tục với inputs hiện có
(2) 🔄 Quay lại chạy skill bổ sung:
    → /plan {{project}} (tạo Product Proposal)
    → /forge-job-map {{project}} (tạo Job Map + ODI)
    → /forge-shift {{project}} (tạo ACH Assessment)
    → /forge-cost {{project}} (tạo Cost Envelope)
    → /forge-scout {{project}} (tạo ACH Scan)
(3) 📝 Bổ sung thông tin thủ công (CEO cung cấp context)
═══════════════════════════════════════════════════
```

Wait for CEO response before proceeding.

#### 1.5c: CEO Context Enrichment

After input validation, ALWAYS ask:

```
📋 CEO: Có thông tin bổ sung nào giúp Phase 1 sát thực tế hơn không?
Ví dụ:
  - Feedback từ khách hàng / người dùng gần đây?
  - Thay đổi yêu cầu hoặc ưu tiên mới?
  - Kết quả test / prototype gần đây?
  - Thông tin đối thủ cạnh tranh mới?
  - Ràng buộc ngân sách / timeline cập nhật?
  - File hoặc tài liệu nào cần đọc thêm?

(Nhập thông tin hoặc "skip" để tiếp tục)
```

If CEO provides additional context → append to pipeline state as `## CEO Context Input` section.

### Step 2: Initialize Pipeline State

Determine output path based on variant:
- With variant: `1_Projects/{{project}}/Phase1-Task/{{variant}}/`
- Without variant: `1_Projects/{{project}}/Phase1-Task/`

Check/create `{{output_path}}/_pipeline_state.md`:

```markdown
---
project: {{project}}
pipeline: helix-task-clarify v3.2
started: {{today}}
updated: {{today}}
mode: [standard | icdm | quick]
---

# Phase 1 Pipeline State — {{project}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|-------------|
| B0 | helix-p1-preflight | PENDING | - | - | - |
| BA | helix-p1-requirements | PENDING | - | - | - |
| BB | helix-p1-validate | PENDING | - | - | - |
| BC | helix-p1-abstract | PENDING | - | - | - |
| BD | helix-p1-structure | PENDING | - | - | - |
| BE | helix-p1-compile | PENDING | - | - | - |

## Block Ledger
> **Purpose:** Sole communication channel between blocks. Each block reads this section for context, then appends its summary. Enables crash recovery and context-free resume.

[Each block appends one entry below when complete — see Ledger Write Protocol]

## CEO Decisions
[populated at each checkpoint]

## Adjustments Log
[populated when CEO modifies outputs]
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

For each block:
1. **Ledger Read:** Read `_pipeline_state.md` to reconstruct context
2. **Announce:** "Đang chạy Block {{X}}: {{name}}..."
3. **Execute block:** Create output file(s) for this block ONLY
4. **Ledger Write:** Append block summary to "Block Ledger" section
5. **Update state:** Mark block COMPLETE in pipeline state
6. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK {{X}} COMPLETE ═══
   Deliverables: [files created]
   Key findings: [1-3 bullets]
   
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
   - (3) → Save state and halt completely
   - (4) → Skip next block, STOP and present the block after that

**Why this matters:** Each block produces deliverables that CEO must inspect. CEO may have corrections, additional context, or want to modify outputs BEFORE they cascade into downstream blocks. Auto-continuing creates compounding errors that are expensive to fix later.

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
PHASE 1 PIPELINE COMPLETE — {{project}}
═══════════════════════════════════════════════════
Requirements: {{N}} ({{D}}D / {{W}}W), {{pct}}% quantified
Essential Problem: "{{EP statement}}"
Function Structure: {{N}} sub-functions
Categories: {{N}}/17 P&B categories covered

Next: /helix-quality-gate {{project}} --gate 1
      /helix-concept-generate {{project}}
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files are placed in `{{output_path}}/` (variant subfolder if variant specified, phase root otherwise).
When variant is specified, all filenames are prefixed with `{{prefix}}` (e.g. `VN_MGM_V5_`).

| File Pattern | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_pipeline_state.md` | Orchestrator | All | Progress, CEO decisions |
| `{{prefix}}B0_Preflight_Report.md` | B0 | BA, BB | Context, stakeholders, standards, scope |
| `{{prefix}}Requirements_Draft.md` | BA | BB, BC | AI-generated 50-80 requirements (unclassified) |
| `{{prefix}}Requirements_List_v1.0.md` | BB | BC, BD, BE | CEO-validated requirements with D/W + gaps |
| `{{prefix}}Failure_Derived_Reqs.md` | BB | BC | FMEA-derived requirements + SPOF check |
| `{{prefix}}Abstraction.md` | BC | BD | 5-step abstraction results |
| `{{prefix}}Essential_Problem.md` | BC | BD, BE, Phase 2 | CEO-approved essential problem |
| `{{prefix}}TVDT.md` | BC | BD, Phase 2 | Target Values Decision Table |
| `{{prefix}}Function_Structure.md` | BD | BE, Phase 2 | 6-flow decomposition with SF table |
| `{{prefix}}Design_Type.md` | BD | Phase 2 | Original/Adaptive/Variant assessment |
| `{{prefix}}Cross_Domain_Sync_S1.md` | BE | Phase 2 | Interface checks, ICD v1 |
| `{{prefix}}P02_QC_Gate.md` | BE | Gate 1 | QC gate results |
| `{{prefix}}Deliverables_Index.md` | BE | Gate 1 | Complete list of Phase 1 outputs |

**Example (with variant):** `Phase1-Task/V5-MOTORIZED/VN_MGM_V5_Requirements_List_v1.0.md`
**Example (no variant):** `Phase1-Task/VN_MGM_Requirements_List_v1.0.md`

## ICDM Extensions (--icdm flag)

> **Source:** Hari & Weiss, ICDM Steps 1-2-5 + EQFD (Enriched QFD), Technion.
> **NLM notebooks:** `icdm`, `eqfd` (19 sources).
> **Maps to:** ICDM Steps 1 (Customer Needs), 2 (EQFD → Product Definition), 5 (Concept Evaluation Criteria).

When `--icdm` is active, each block receives **specific EQFD/ICDM methodological extensions:**

### B0 ICDM: Customer & Innovation Context

- **WTP (Willingness to Pay) assessment:** Classify product scope into 3 WTP categories:
  - **Essential:** Basic needs — primary reasons customer pays. MUST be met.
  - **Beneficial:** Secondary needs — customer pays small additional amount.
  - **Luxurious:** Nice-to-have — customer will NOT pay extra.
- **Innovation type classification:** Technology novelty (1-5) × Market novelty (1-5) × Business model novelty (1-5) → Overall innovation level.
- **Creativity readiness:** Cross-functional input, external benchmarking, TRIZ resources, design space explored.

### BA ICDM: EQFD Process (Enriched Quality Function Deployment)

Replace standard requirements generation with EQFD process:

1. **Limit customer needs:** Filter VOC to **15-20 most critical system-level needs** (not 50+ raw requirements).
2. **Filter product characteristics:** Identify **20-25 most important/difficult/controversial** engineering parameters.
3. **"Other" placeholder:** Single column for minor parameters not in top 20-25.
4. **Streamline benchmarking:** Identify **single best competitor** per need (not exhaustive grid).
5. **Skip correlation roof:** Only discuss correlations that affect target value decisions.
6. **Populate TVDT:** For each parameter: relative weight, trade-offs, reference product, Target Value, implications.
7. **Generate action plan:** Immediate actions for completing specifications.

**Key difference from standard BA:** Standard BA generates 50-80 requirements in P&B categories. EQFD BA generates a focused 15-20 needs → 20-25 characteristics → TVDT. The full requirements list is still produced but EQFD outputs DRIVE the evaluation criteria.

### BB ICDM: WTP Classification + CSR Definition

- **WTP tag per requirement:** Every requirement gets tagged Essential / Beneficial / Luxurious.
- **CSR functions (Customer Satisfaction Rating):** For each top characteristic from EQFD, define a satisfaction function:
  - Achieving Target Value = **100% satisfaction**.
  - Below target = decreasing % (linear, exponential, or step-based — CEO decides curve shape).
  - Above target = **capped at 100%** (no credit for over-engineering).
- **Group A/B criteria split:**
  - **Group A:** Smallest set of criteria covering ≥70% of total satisfaction weight → used for Pugh SCREENING in Phase 2.
  - **Group B:** Extended set covering ≥95% → used for FINAL concept selection in Phase 2.

**Additional outputs:** CSR function tables in `{{prefix}}CSR_Functions.md`, Group A/B split in requirements list.

### BC ICDM: Solution-Free Verification

- **ICDM Step 3 check:** Verify essential problem is truly "solution-free" — no brand names, no specific technologies, no geometry constraints in the problem statement.
- **Functional abstraction:** Problems described as abstract functions, not implementations.
- Standard P&B 5-step abstraction is retained. ICDM adds explicit solution-free verification gate.

### BD ICDM: Platform & Innovation Flows

- **Innovation flow (7th flow):** Add to 6-flow function structure:
  - I-IN: Customer feedback, field data, competitor intelligence
  - I-PROCESS: Data analysis, model improvement, knowledge capture
  - I-OUT: Product updates, platform upgrades, new variant generation
- **Platform commonality check:** For each SF, flag if shared with other portfolio variants.

### BE ICDM: Concept Evaluation Criteria Deliverable (ICDM Step 5)

- **Compile ICDM Step 5 output:** Formal deliverable listing:
  - Group A criteria (for Phase 2 Pugh screening)
  - Group B criteria (for Phase 2 final evaluation)
  - CSR functions per criterion
  - DQM (Design Quality Measurement) framework ready for Phase 2

> **Provenance note — do not re-add "IRL".** This block previously scored an "IRL (Innovation
> Readiness Level) 1-5". Verified 2026-08-15 against the full ICDM corpus (Hari & Weiss 1996-2015,
> 15 sources): **no ICDM source mentions IRL.** It belongs to the KTH Innovation Readiness Level
> model — an unrelated framework, six dimensions over nine levels. Removed as a misattribution.
> Readiness in ICDM is carried by RTA (Knowledge Gap → development cycles → TTM) in Phase 2 BD,
> not by a scale set here in Phase 1.

**Additional outputs:** `{{prefix}}ICDM_Evaluation_Criteria.md`, `{{prefix}}CSR_Functions.md`

## Future Extension Points

```
--icdm      → ICDM framework overlay
--mil-std   → Auto-import MIL-STD requirements template
--retroactive → Optimized for documenting existing products
--agile     → Sprint-compatible requirements breakdown
```

## Integration

```
helix-task-clarify (ORCHESTRATOR) COMMANDS:
  → /helix-p1-preflight     (Block 0)
  → /helix-p1-requirements  (Block A)
  → /helix-p1-validate      (Block B)
  → /helix-p1-abstract      (Block C)
  → /helix-p1-structure     (Block D)
  → /helix-p1-compile       (Block E)

helix-task-clarify READS FROM:
  - helix-project-init → charter, ICD v0
  - /plan outputs (if available):
      Product_Proposal_v*.md → IFR, sacred constraints, TRIZ resources
      Product_Planning_v*.md → scope, stakeholders, cost targets, timeline
      Portfolio_Planning_v*.md → variant strategy, shared platform, synergy map
  - Phase0-Forge/ (or FORGE/) outputs (if available):
      forge-job-map → ODI_Outcomes_v*.md, Job_Map_v*.md, HOQ_Design_Parameters_v*.md
      forge-cost → Cost_Envelope_v*.md, LCC_Estimate_v*.md
      forge-shift → ACH_Assessment_v*.md
      forge-scout → ACH_Opportunity_Scan_v*.md
  - forge-library → similar product requirements (vault-wide)
  - 3_Resources/Technical-References/ → MIL-STD, STANAG, TCVN

helix-task-clarify WRITES TO:
  - 1_Projects/{{project}}/Phase1-Task/ → all deliverables
  - helix-concept-generate → requirements + function structure + essential problem
  - helix-quality-gate → Gate 1 readiness
  - ICD v1 → requirements allocated to domains
  - bridge-risk-radar → requirements risks
  - helix-design-journal → session log

helix-task-clarify VISUAL OUTPUTS (via /helix-draw):
  - B0: Stakeholder Map → /helix-draw stakeholder-map
  - B0: Contextual Factors → /helix-draw radar
  - BA: Requirements Coverage → /helix-draw bar-chart
  - BB: D/W Classification → /helix-draw bar-chart
  - BB: SPOF Risk Matrix → /helix-draw matrix
  - BC: TVDT Benchmark Comparison → /helix-draw radar
  - BD: System Black-Box → /helix-draw block-diagram
  - BD: 6-Flow Function Structure → /helix-draw function-tree
  - BD: Design Type Assessment → /helix-draw radar
  - BE: P02 QC Gate → /helix-draw dashboard
  - BE: Gate 1 Readiness → /helix-draw dashboard

SHARED REFERENCES (in helix-task-clarify/references/):
  - pb-task-clarification.md → P&B Ch5 methodology
  - prompt-templates.md → S1 templates for Phase 1
```

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After completing each block, STOP generating content and WAIT for CEO response. NEVER execute 2+ blocks in a single turn. NEVER combine blocks (e.g., "BA+BB") without CEO explicitly requesting it. This is the #1 rule.
- **CEO checkpoint after EVERY block** — no auto-continue without explicit CEO approval ("tiếp tục", "approve", "ok", etc.)
- **Orchestrator NEVER does block work itself** — always delegates to sub-skills
- **Pipeline state file is source of truth** — always read before any action
- **Each block-skill is independently runnable** — CEO can run `/helix-p1-validate` alone
- **Data bus contract is sacred** — block outputs use exact filenames in Data Bus table
- **Orchestrator tracks but doesn't modify** block outputs — modifications happen by re-running the block
- **D/W classification is ALWAYS Core** — AI never classifies D vs W, AI proposes, CEO confirms
- **Essential problem approval is ALWAYS Core** — AI proposes, CEO decides
- **Minimum 50 requirements** for defense products
- **Requirements are "Binding Yet Provisional"** (P&B 5.3.1) — once listed, they are commitments for current phase, BUT must be updated as knowledge grows. Tag each requirement: [CONCEPT] / [STRUCTURE] / [EMBODY] / [LATE] to indicate when it must be resolved. [LATE]-tagged requirements may use [TBD] placeholder values.
- **Solution ideas ≠ requirements** — if a solution idea emerges during BA/BB, record it in Solution_Ideas_Log section (separate from requirements), re-express the requirement as performance specification. Solution ideas feed Phase 2 working principle search.
- **If CEO says "chạy hết" or "skip checkpoints"** — STILL stop after each block but keep checkpoint minimal (1-line summary + "tiếp tục?")

## COD Classification

- Pipeline orchestration: Offload (O1)
- Block execution: Offload (O2) — each block has own COD
- CEO checkpoints: **Core (C)**
- D/W classification: **Core (C)** — non-delegable
- Essential problem approval: **Core (C)** — non-delegable
- Standards selection: **Core (C)** — CEO provides, AI fills template
