---
name: helix-p3-bom
description: "Block D of Phase 3 pipeline — generate draft BOM (mechanical/electrical/fasteners/COTS), long-lead item identification, cost estimate, VN sourcing verification. P&B 7.1 Step 14. Can run standalone. Triggers on: 'BOM', 'bill of materials', 'parts list', 'cost estimate', 'sourcing', 'long lead'."
---

# Block D: BOM — Draft Bill of Materials + Cost + Sourcing

> **P&B:** 7.1 (Step 14) | **Pipeline:** helix-embody-realize → Block BD
> **Input:** `BA_Preliminary_Layout.md`, `BC_ICD_v3.md` | **Output:** `BD_BOM_Draft.md`, `BD_Long_Lead_Items.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Generate draft BOM (mech/elec/fasteners/COTS) | Change design to reduce cost (= flag to CEO) |
| Identify long-lead items for early procurement | Evaluate embodiment quality (= BE) |
| Estimate cost per subsystem | Approve sourcing decisions (= CEO Core) |
| Verify VN sourcing availability | Skip cost estimate for "simple" products |
| Flag items exceeding cost envelope | Substitute components without CEO approval |

**Multi-Agent Mode:** NO — BOM generation is a structured listing task, single agent with sourcing database access.
**CEO Checkpoint:** Review BOM feasibility, long-lead items, and cost vs target. CEO decides sourcing strategy.

## Workflow

### Step D1: Draft BOM by Category

```
DRAFT BOM — {{project}}
Date: {{today}}
Status: PRELIMINARY — costs are estimates (±30%)

MECHANICAL:
| # | Part | Material | Qty | Process | VN Vendor | Est. Cost | Lead Time |
|---|------|----------|-----|---------|-----------|----------|-----------|

ELECTRICAL:
| # | Component | Spec | Qty | Source | VN Available? | Est. Cost | Lead Time |

FASTENERS:
| # | Type | Size | Grade | Qty | Standard | Est. Cost |

COTS (Commercial Off-The-Shelf):
| # | Item | Model/Spec | Qty | Vendor | Est. Cost | Lead Time | Alt. Source |

SOFTWARE/COMPUTE (if applicable):
| # | Item | Spec | Qty | Source | Est. Cost | Lead Time |

SUBTOTALS:
  Mechanical: ___
  Electrical: ___
  Fasteners: ___
  COTS: ___
  Software: ___
  TOTAL BOM: ___
  Assembly labor (est.): ___
  TOTAL UNIT COST: ___
  
Cost target (from requirements): ___
Status: [WITHIN / OVER by ___% / UNDER by ___%]
```

> **Extract from geometry-of-record, don't transcribe:** Where a geometry-of-record exists, extract the part list + per-part volumes/mass directly from the model via [[helix-cad-bridge]] (or read the cad_extract.json BOM rows from [[helix-cad-ingest]]) instead of transcribing from the layout .md. Reconcile against the ICD v3 geometry-of-record registry ([[helix-p3-integrate]] Step C3a) so every BOM line has a matching geometry row (no orphans).

### Step D2: VN Sourcing Verification

```
SOURCING CHECK — {{project}}

LOCAL CONTENT:
  VN-sourced items: {{N}} ({{pct}}% by value)
  Import items: {{N}} ({{pct}}% by value)
  Target (from requirements): ≥{{pct}}%
  Status: [PASS / GAP of {{pct}}%]

SINGLE-SOURCE RISKS:
| Item | Current Source | Alternative? | Risk if Unavailable |
|------|--------------|-------------|-------------------|
```

### Step D3: Long-Lead Items

```
LONG-LEAD ITEMS (>4 weeks) — {{project}}

| # | Item | Lead Time | Order By Date | Budget Impact | Status |
|---|------|-----------|--------------|--------------|--------|

EARLY PROCUREMENT RECOMMENDATION:
  Items to order NOW: [list]
  Items to order after Gate 3: [list]
  Items to defer to Phase 4: [list]
```

### Step D4: Cost Sensitivity

```
COST SENSITIVITY — {{project}}

Top 5 cost drivers:
| # | Item | Cost | % of Total | Reduction Option | Saving |
|---|------|------|-----------|-----------------|--------|

If cost > target: [list value engineering options]
```

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BD_BOM_Draft.md`
- `BD_Long_Lead_Items.md`

## CEO Checkpoint
```
═══ BLOCK BD BOM COMPLETE ═══
Total BOM cost: {{amount}} (target: {{target}})
Cost status: [WITHIN / OVER {{pct}}%]
Local content: {{pct}}% (target: {{pct}}%)
Long-lead items: {{N}} (earliest order-by: {{date}})
Single-source risks: {{N}}

CEO:
(1) ✅ Approve → tiếp tục Block BE (Compile)
(2) 💰 Value engineering needed — identify cuts
(3) 🔄 Revise BOM after layout changes
(4) ⏸️ Dừng — need supplier quotes
```

## COD
- BOM compilation: Offload (O1) — AI from geometry-of-record ([[helix-cad-bridge]]/[[helix-cad-ingest]]) where it exists, else layout
- BOM↔geometry-of-record reconciliation (no orphan lines): Offload (O2) — AI cross-checks ICD v3 registry
- Cost estimation: Offload (O2) — AI estimates from catalogs
- **Cost target decision: Core (C)** — CEO accepts or demands VE
- Sourcing check: Offload (O2)
- **Procurement timing: Core (C)** — CEO decides when to order
