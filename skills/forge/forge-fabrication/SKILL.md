---
name: forge-fabrication
description: "Manufacturing orchestrator mega-skill — đóng vòng từ design freeze (HELIX P3/P4 handoff) đến giao hàng + invoice. 6-block deterministic pipeline (preflight → material → release → execute → acceptance → invoice) commanding 6 existing erp-* skills as blocks. Cross-product capacity arbitration cho BB-01/V-SMASH/MTB-20/TDR. Traceability per Work Order (BOM allocation, Job Card lineage, QC stamps, NCR linkage, defense milestone billing). Flags: --product, --qty, --customer, --contract, --from, --only, --dry-run. Triggers on: 'forge fabrication', 'sản xuất', 'fab pipeline', 'manufacturing pipeline', 'đưa vào sản xuất', 'release to production', 'fab BB-01', 'chế tạo lô', 'chạy WO', 'production run', 'mfg orchestrator'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# forge-fabrication — Manufacturing Mega-Skill Orchestrator

> **Role:** Chỉ huy trưởng (Commander) — điều phối 6 erp-* skills tuần tự để đóng vòng R&D → sản xuất → giao hàng
> **Architecture:** Modular pipeline — reuse 6 existing erp-* block skills, KHÔNG duplicate
> **Why this skill exists:** HELIX P1-P3 đã có full pipeline cho R&D, nhưng từ "design freeze" → "part trên xưởng" là black hole. CEO phải gọi `/erp-master`, `/erp-bom`, `/erp-stock`, `/erp-production`, `/erp-quality`, `/erp-finance` thủ công cho từng lô. Mega-skill này đóng vòng + thêm cross-product capacity arbitration mà single skill không thấy được.
> **Musk principle:** "Manufacturing IS the product." Production engineering không phải downstream, là tài sản chiến lược.
> **Naval principle:** Mỗi WO sinh artifact deterministic (BOM allocation JSON, Job Card lineage, QC stamps) — compound assets cho future code-leverage và field data flywheel.

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                    forge-fabrication (ORCHESTRATOR — 6 blocks)                       │
│                                                                                       │
│  Flags: --product <BB-01|V-SMASH|MTB-20|TDR> --qty N --customer <name>              │
│         --contract <ref> --from F0-F5 --only Fx --dry-run                           │
│                                                                                       │
│  ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐                          │
│  │ F0  │──▶│ F1  │──▶│ F2  │──▶│ F3  │──▶│ F4  │──▶│ F5  │                          │
│  │PRE- │   │MAT- │   │RE-  │   │EXEC │   │ACC- │   │INV- │                          │
│  │FLT  │   │ERIAL│   │LEASE│   │UTE  │   │EPT  │   │OICE │                          │
│  └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘                          │
│     │CEO     │CEO      │CORE     │CEO      │CORE     │CORE                          │
│     ▼        ▼         ▼         ▼         ▼         ▼                              │
│  [audit] [reorder] [release]  [job   [accept]  [bill]                              │
│   master  stock     WO        cards] gate     defense                              │
│   +BOM    +PO       prod      +QC    +stock   milestone                            │
└──────────────────────────────────────────────────────────────────────────────────────┘

Legend: CORE = CEO non-delegable (production commitment, acceptance, billing)
        CEO  = checkpoint after block

Data Bus: 2_Areas/WX-OPS/Fabrication-Runs/<product>-<run_id>/
State:    <run_dir>/_pipeline_state.md
Run ID:   <product>-<YYYYMMDD>-<seq> (e.g., BB-01-20260511-001)
```

## Sub-Skills (6 Block — Reuse Existing erp-*)

| Block | Reused Skill(s) | Purpose | CEO Gate |
|-------|----------------|---------|----------|
| **F0** | `/erp-master audit` + `/erp-bom check` | Verify HELIX handoff, master data ≥90%, BOM exists + complete, routing exists | Approve handoff gate |
| **F1** | `/erp-stock` (availability + reorder) | Material Availability Check (MAC) — calculate `max_builds`, flag BLOCKING items, draft PO if shortage | Approve PO if needed |
| **F2** | `/erp-production wo add` | Draft Work Order, show material impact + capacity impact, **CEO releases** = production commitment | **CORE — release WO** |
| **F3** | `/erp-production` (job cards) + `/erp-quality` (inline gates) | Job Card lifecycle WS-CKCX → WS-DT → WS-DC → WS-VL with inline QC gates after each PX | Review gate pass rate |
| **F4** | `/erp-quality` Gate-Final + `/erp-production complete` | Final acceptance, Stock Entry (Manufacture), WH-FG update | **CORE — final acceptance** |
| **F5** | `/erp-finance invoice sales` + payment tracking | Defense milestone invoice (30/40/30), payment entry, P&L impact | **CORE — invoice approval** |

**Reuse rationale:** 6 erp-* skills already encode the procedural knowledge. forge-fabrication adds the **glue** missing from single-skill calls:
1. Cross-block state ledger (no context loss between blocks)
2. Cross-product capacity arbitration (when 2 products compete for same PX)
3. HELIX P3/P4 handoff gate (closes design → production)
4. Traceability artifact (one folder per run, full lineage)
5. Defense milestone billing scheduler

## How to Use

### Full Pipeline (default)
```
/forge-fabrication --product BB-01 --qty 4 --customer "Cục KH-CN BQP" --contract "HĐ-2026-014"
```

### Dry run (plan only, no ERPNext writes)
```
/forge-fabrication --product V-SMASH --qty 2 --dry-run
```
Outputs: capacity impact, material impact, NCR risk forecast — without committing.

### Resume from block
```
/forge-fabrication --from F3 --run BB-01-20260511-001
```

### Single block (inspection / re-run)
```
/forge-fabrication --only F1 --run BB-01-20260511-001
```

### Cross-product check (before committing)
```
/forge-fabrication --product MTB-20 --qty 6 --check-conflicts
```
Lists active WOs and shows PX/material conflicts before F0.

## Orchestrator Workflow

### Step 1: Parse Arguments

```
FLAGS:
  --product P     → BB-01 | V-SMASH | MTB-20 | TDR (required unless --from)
  --qty N         → batch size (required for new run)
  --customer C    → customer name (required for F5; can defer)
  --contract R    → contract reference (required for F5; can defer)
  --from Fx       → resume from block F0-F5
  --only Fx       → run single block
  --run ID        → run identifier (auto-generated if new)
  --dry-run       → no ERPNext writes
  --check-conflicts → F0 sub-mode: capacity + material conflict report only
```

### Step 1.5: Resolve Run Directory

```
If --run given:
  run_id = <given>
  run_dir = 2_Areas/WX-OPS/Fabrication-Runs/<run_id>/
  Read existing _pipeline_state.md

Else (new run):
  run_id = <product>-<YYYYMMDD>-<seq>
    where seq = next sequential number for this product+date
  run_dir = 2_Areas/WX-OPS/Fabrication-Runs/<run_id>/
  mkdir -p run_dir
```

### Step 1.6: Cross-Product Pre-Check (NEW — value-add over single erp-* calls)

**MANDATORY before F0.** Lists active production state:

```
═══ CROSS-PRODUCT CAPACITY SCAN ═══
Active WOs:
  - WO-2026-019  BB-01    qty=2  PX-CKCX (24h alloc) PX-DT (8h)   target 2026-05-18
  - WO-2026-021  V-SMASH  qty=1  PX-CKCX (8h)        PX-DC (16h)  target 2026-05-15

This run: <product> qty=<N> → estimated PX load
  - PX-CKCX:  +Xh  (current util: Y% → would become Z%)
  - PX-DT:    +Xh
  - PX-DC:    +Xh
  - PX-VL:    +Xh

⚠️ Conflicts detected: [list of overloads or blocking]
✅ Or: No conflicts — proceed safely.

Critical material conflicts (shared BOM items across active WOs):
  - ALU-6061-10: total demand 40m, on-hand 28m → shortage 12m, lead time 14d
  - ENCODER-600P: demand 4, on-hand 2 → shortage 2, lead time 30d

CEO:
(1) ▶️ Confirm — proceed to F0
(2) ⏸️ Reduce qty / change target date
(3) ❌ Cancel run
═══════════════════════════════════════
```

If `--check-conflicts` flag → STOP here, output report only.

### Step 2: Initialize Pipeline State

Create `<run_dir>/_pipeline_state.md`:

```markdown
---
run_id: <product>-<YYYYMMDD>-<seq>
product: <product>
qty: <N>
customer: <customer or "TBD">
contract: <contract or "TBD">
pipeline: forge-fabrication v1.0
started: <today>
updated: <today>
mode: [standard | dry-run]
helix_handoff: <P3 handoff package path if from HELIX, else "manual">
---

# Fabrication Run — <run_id>

## Block Progress
| Block | Skill(s) Called | Status | Started | Completed | CEO Approved |
|-------|----------------|--------|---------|-----------|-------------|
| F0 | erp-master + erp-bom | PENDING | - | - | - |
| F1 | erp-stock | PENDING | - | - | - |
| F2 | erp-production (wo) | PENDING | - | - | - |
| F3 | erp-production (jc) + erp-quality | PENDING | - | - | - |
| F4 | erp-quality + erp-production | PENDING | - | - | - |
| F5 | erp-finance | PENDING | - | - | - |

## Block Ledger
> SOLE communication channel between blocks. Each block reads, then appends summary.

[populated by each block]

## CEO Decisions
[populated at each checkpoint]

## Traceability Manifest
[populated as run progresses — see Data Bus]
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ #1 RULE: Execute EXACTLY ONE block per turn. STOP and WAIT for CEO response after each.**

#### Ledger Read Protocol (BEFORE each block)
Read `_pipeline_state.md` → "Block Ledger" section. Reconstruct context from prior blocks. Critical for `--from` resume.

#### Ledger Write Protocol (AFTER each block)
Append:
```
### F<X> — <block name> (<date>)
**Skills called:** [/erp-* commands with arguments]
**Key results:** [2-3 bullets — counts, IDs, gate results]
**Artifacts created:** [files in run_dir]
**Decisions for downstream:** [what next block needs]
**Open issues:** [unresolved — flagged for CEO or next block]
**CEO checkpoint result:** [approve / revise / pause + CEO's words]
```

#### Per-Block Execution

For each block:

1. **Ledger Read** — reconstruct context
2. **Announce:** "Đang chạy Block F<X>: <name>..."
3. **Pre-conditions check** — verify required inputs exist (next section)
4. **Invoke erp-* skill(s)** — translate pipeline state → trigger commands
5. **Post-conditions check** — verify expected outputs created in ERPNext
6. **Artifact capture** — copy/link key outputs into `<run_dir>/`
7. **Ledger Write** — append summary
8. **Update state** — mark COMPLETE
9. **STOP — CEO Checkpoint (BLOCKING):**
   ```
   ═══ BLOCK F<X> COMPLETE — <run_id> ═══
   Skills invoked: [list]
   Artifacts: [files]
   Key results: [bullets]
   ⚠️ Issues: [if any]

   CEO:
   (1) ✅ Approve → tiếp tục Block F<X+1>
   (2) 🔄 Chạy lại Block F<X> với điều chỉnh: [mô tả]
   (3) ⏸️ Dừng pipeline
   (4) ⏭️ Skip Block F<X+1>
   ```
10. **⛔ WAIT** for CEO message.

### Block-Level Logic

#### F0 — Preflight (HELIX Handoff Gate)

**Pre-conditions:**
- HELIX P3 handoff package exists (path passed via --helix-handoff, or scan 1_Projects/<product>/Phase3-Embody/)
- Master data quality score ≥90% (from `/erp-master audit`)
- BOM exists and complete (from `/erp-bom check <product>`)
- Routing exists in `_routing.md`

**Invoke:**
```
/erp-master audit
/erp-bom check <product>
```

**Pass criteria:** Both return GREEN. If RED → STOP, instruct CEO which gap to close first.

**Artifact:** `<run_dir>/F0_Handoff_Gate.md` (audit results + handoff package summary)

#### F1 — Material Availability

**Invoke:**
```
/erp-stock                        → balance check
/erp-stock reorder                → reorder suggestions if shortage
```

**Logic:**
- For each BOM item: `required = qty_per_unit × <qty>`
- Compare with `qty_on_hand` minus reservations for active WOs
- Classify each item: OK | LOW (below reorder, can proceed) | BLOCKING (insufficient for this run)
- If BLOCKING items exist → draft PO via `/erp-finance po` (CEO approves before F2)

**Artifact:** `<run_dir>/F1_Material_Plan.md` (BOM allocation table with status per line)

#### F2 — Work Order Release (CORE)

**Pre-conditions:** F0 + F1 green.

**Invoke:**
```
/erp-production wo add            → draft (Status: Draft)
[CEO approval required]
/erp-production wo release <ID>   → release (Status: Not Started, materials reserved)
```

**Capacity arbitration:** Before release, check active WOs on same PX. If overload → recommend target_date adjustment.

**Artifact:** `<run_dir>/F2_Work_Order.md` (WO ID + Job Card plan + capacity allocation + reservation list)

**⛔ This is the production commitment point.** No materials reserved before this.

#### F3 — Shop Floor Execution

**Job Card flow per Routing:**
```
WS-CKCX (Job Card) → Gate-CKCX (QC inspection) →
WS-DT   (Job Card) → Gate-DT   (QC) →
WS-DC   (Job Card) → Gate-DC   (QC) →
WS-VL   (Job Card) → Gate-VL   (QC)
```

**Invoke per PX:**
```
/erp-production jobcard          → status per WS
/erp-quality inspect <WO-ID>     → log gate result (PASS/FAIL → NCR auto)
```

**NCR loop:** If any gate FAIL → `/erp-quality ncr` open, rework hours logged, gate re-inspected. F3 does NOT exit until all gates PASS.

**Artifact:** `<run_dir>/F3_Shopfloor_Log.md` (job card timeline + QC stamps + NCR list if any)

**CEO checkpoint cadence:** Standard = end of F3. CEO can request inline checkpoints per PX via `--checkpoint-per-px` flag.

#### F4 — Final Acceptance + Stock Entry (CORE)

**Pre-conditions:** All F3 gates PASS, all Job Cards Complete.

**Invoke:**
```
/erp-quality inspect <WO-ID> --gate Final   → CEO/PGĐ physical inspection
/erp-production complete <WO-ID>            → triggers Stock Entry (Manufacture)
                                              → consume materials from WH-NVL
                                              → produce qty into WH-FG
```

**⛔ Final acceptance is CEO Core** — AI logs, CEO judges PASS.

**Artifact:** `<run_dir>/F4_Acceptance_Report.md` (final QC + stock entry refs + WH-FG state)

#### F5 — Invoice + Payment (CORE)

**Pre-conditions:** F4 PASS, contract reference + customer set.

**Defense milestone billing schedule:**
- Contract signed → 30% advance (may have been billed before run)
- This run delivery → 40% progress invoice
- Final acceptance + warranty start → 30% completion invoice

**Invoke:**
```
/erp-finance invoice sales       → create Sales Invoice (linked to WO, contract)
[CEO approves invoice]
/erp-finance payment             → record payment when received
```

**Artifact:** `<run_dir>/F5_Invoice_Package.md` (invoice ID, milestone, expected payment date, contract status)

### Step 4: Pipeline Completion

```
═══════════════════════════════════════════════════
FABRICATION RUN COMPLETE — <run_id>
═══════════════════════════════════════════════════
Product: <product> × <qty>
Customer: <customer> (contract <contract>)

Timeline:
  F0 → F5 elapsed: <hours/days>
  Routing planned: <hours>  Actual: <hours>  Variance: <±%>

Quality:
  FPY: <%>  NCRs opened: <N>  NCRs closed: <N>
  Gate-Final result: PASS

Financial:
  COGS: <VND> (from BOM × actual)
  Invoice issued: <ID> (<milestone>, <amount> VND)
  Margin estimate: <%>

Traceability artifacts in <run_dir>/:
  F0_Handoff_Gate.md
  F1_Material_Plan.md
  F2_Work_Order.md
  F3_Shopfloor_Log.md
  F4_Acceptance_Report.md
  F5_Invoice_Package.md
  _pipeline_state.md  (full ledger)

Compound learning hooks:
  - /forge-flywheel <product> → log field data collection start (warranty period begin)
  - /forge-library audit → check if this run validates a model from library
  - /helix-design-journal → record any production-discovered issues for next P3
  - /bridge-cross-learn → suggest if patterns transfer to other products
═══════════════════════════════════════════════════
```

## Data Bus — Shared File Contract

All files in `2_Areas/WX-OPS/Fabrication-Runs/<run_id>/`:

| File | Written By | Read By | Content |
|------|-----------|---------|---------|
| `_pipeline_state.md` | Orchestrator | All blocks | Progress, ledger, CEO decisions, traceability manifest |
| `F0_Handoff_Gate.md` | F0 | F1, F2 | HELIX handoff verification, master/BOM audit results |
| `F1_Material_Plan.md` | F1 | F2 | BOM allocation table, PO drafts if shortage |
| `F2_Work_Order.md` | F2 | F3 | WO ID, Job Card plan, capacity allocation, reservation list |
| `F3_Shopfloor_Log.md` | F3 | F4 | Job card timeline per PX, QC stamps, NCR list |
| `F4_Acceptance_Report.md` | F4 | F5, flywheel | Final QC, Stock Entry refs, WH-FG state |
| `F5_Invoice_Package.md` | F5 | finance | Invoice ID + milestone + payment status |

**Contract rule:** Each block reads its predecessors' files. If a predecessor file is missing → STOP, instruct CEO to run that block first.

## Cross-Product Capacity Logic (UNIQUE VALUE-ADD)

Beyond single erp-* calls, the orchestrator maintains a **global capacity view**:

1. **Scan all active WOs** across all products before F0
2. **Compute PX utilization** per workstation (current + this run's load)
3. **Detect material conflicts** — shared BOM items between active WOs
4. **Suggest sequencing** — if conflict, propose target date shift or qty reduction
5. **CEO authoritative** — recommendations only; CEO can override

This is the gap that single-skill calls cannot fill: each erp-* skill sees only its own document type. The orchestrator sees the **product portfolio in motion**.

## HELIX → FORGE Handoff Integration

When invoked with `--helix-handoff <path>`:

1. Read HELIX P3 handoff package (BOM_Draft, Routing_v3, ICD_v3, embodiment evaluation)
2. Verify BOM_Draft matches `BOM Master` sheet for the product
3. Verify Routing_v3 matches `_routing.md`
4. If mismatch → flag for CEO before F0

If no handoff path given → scan `1_Projects/<product>/Phase3-Embody/` for latest package. If none found → assume manual run (CEO acknowledges).

This closes the R&D → production gap that previously required manual bridging.

## Compound Learning Hooks (NAVAL LEVERAGE)

Each completed run automatically:

1. **Updates `forge-flywheel`:** Field deployment starts → data collection begins → model retraining accumulator
2. **Updates `forge-library`:** If product uses a library model, log production validation as evidence
3. **Updates `bridge-knowledge-base`:** Run summary becomes searchable case study
4. **Updates routing actuals:** Job Card actual hours feed back to update planned hours in `_routing.md` (improving F0 capacity estimates over time)

These hooks turn each run from a one-shot operation into a **compounding asset** — Naval's "code/media that work while you sleep."

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — After each block, STOP and WAIT for CEO. NEVER chain blocks. NEVER auto-continue. #1 rule.
- **F2 WO release = CORE** — production commitment, materials reserved, capacity allocated. AI drafts, CEO releases.
- **F4 Final acceptance = CORE** — physical inspection, CEO/PGĐ judges. AI cannot replace.
- **F5 Invoice = CORE** — defense contract legal compliance, VAT, TT200. KTT validates.
- **Cross-product scan MANDATORY before F0** — never start a run blind to portfolio state.
- **`--dry-run` writes ZERO to ERPNext** — only generates plan files for CEO review.
- **HELIX handoff verification mandatory if path given** — mismatch = STOP, not warning.
- **Job Card actuals MUST flow back to routing** — F3 close = update `_routing.md` planned hours per operation. This is the compounding asset.
- **NCR ≠ blocker for downstream gates** — F3 gate FAIL → rework loop. F4 cannot start until all F3 gates PASS.
- **Defense milestone billing schedule is sacred** — 30/40/30. Never bill out of sequence without CEO + KTT sign-off.
- **Orchestrator NEVER calls ERPNext MCP directly** — always delegates via `/erp-*` block skills. Keeps separation of concerns.
- **Run folder is the traceability source of truth** — all artifacts in one place per WO. NEVER scatter.

## Integration

```
forge-fabrication (ORCHESTRATOR) COMMANDS:
  → /erp-master audit              (F0)
  → /erp-bom check <product>       (F0)
  → /erp-stock                     (F1)
  → /erp-stock reorder             (F1)
  → /erp-production wo add         (F2)
  → /erp-production wo release     (F2)
  → /erp-production jobcard        (F3)
  → /erp-quality inspect           (F3, F4)
  → /erp-quality ncr               (F3)
  → /erp-production complete       (F4)
  → /erp-finance invoice sales     (F5)
  → /erp-finance payment           (F5)
  → /erp-finance po                (F1 — if shortage)

forge-fabrication READS FROM:
  - 1_Projects/<product>/Phase3-Embody/ → HELIX handoff package
  - 1_Projects/<product>/_routing.md   → routing per product/variant
  - WX-OPS.xlsx (BOM Master, Stock Ledger, Customers, Suppliers) → master data
  - ERPNext → live state via MCP (through erp-* skills)

forge-fabrication WRITES TO:
  - 2_Areas/WX-OPS/Fabrication-Runs/<run_id>/ → all run artifacts
  - ERPNext → WO, Job Card, Stock Entry, QC Inspection, NCR, Sales Invoice, Payment
  - 1_Projects/<product>/_routing.md → planned hours updated from actuals (after F3)

forge-fabrication TRIGGERS (CEO-prompted after F5):
  - /forge-flywheel <product> → start field data collection window
  - /forge-library audit → log model validation evidence
  - /bridge-knowledge-base → ingest run summary
  - /helix-design-journal → capture any production-discovered design issues

forge-fabrication COMPLEMENTS:
  - helix-task-clarify, helix-concept-generate, helix-embody-realize (P1-P3)
  - helix-detail-finalize (P4) — feeds handoff into F0
  - forge-portfolio → run state appears in dashboard
  - bridge-deploy-gate → final deploy readiness uses F4 acceptance
```

## COD Classification

- Pipeline orchestration: **Offload (O1)** — mechanical sequencing
- F0 audit / F1 material check: **Offload (O2)** — AI analyzes, CEO approves
- F2 WO **release**: **Core (C)** — production commitment, non-delegable
- F3 job card progress logging: **Offload (O2)** — AI logs from shop floor inputs
- F3 NCR root cause: **Core (C)** — must be observed on floor
- F4 final acceptance: **Core (C)** — physical inspection, non-delegable
- F5 invoice approval: **Core (C)** — legal + financial commitment
- Cross-product capacity arbitration: **Offload (O2)** — AI recommends, CEO authorizes

## Why This Closes the Loop

Before forge-fabrication:
```
HELIX P1 → P2 → P3 → P4 → [GAP] → manual erp-* calls → field
```

After forge-fabrication:
```
HELIX P1 → P2 → P3 → P4 → forge-fabrication F0→F5 → field data → forge-flywheel → loop
```

Each run is now a **node in a compounding graph**, not a standalone transaction.
