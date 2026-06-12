---
name: helix-p4-bom
description: "Block B of Phase 4 pipeline — final production BOM (mechanical/electrical/fasteners/COTS), Vietnam vendor selection ≥60% local content target, long-lead item flagging + order-by dates, cost rollup vs Phase 3 budget, single-source risk flags, MIL-STD/TCVN traceability, supplier sign-offs. P&B 9.4. Triggers on: 'Phase 4 BOM', 'final BOM', 'production BOM', 'vendor selection'."
---

# Block B: Final BOM — Production-Ready Bill of Materials

> **P&B:** Chapter 9 § 9.4 | **Pipeline:** helix-detail-finalize → Block BB
> **Input:** P3 BOM Draft + BA drawings (Part Numbers locked) | **Output:** `BOM_Final.md` + supplier annex

## Operational Envelope

| DO | DON'T |
|----|----|
| Compile hierarchical BOM (assy → sub → part) | Critical dim/tolerance specs (= BA, CEO Core) |
| Vendor selection with Vietnam-source priority | Inspection criteria (= BC) |
| Long-lead order-by date calculation | Assembly sequence (= BD) |
| Cost rollup vs Phase 3 envelope | Workshop master review (= BE, CEO Core) |
| Single-source risk flag | Customer pricing (defense — CEO only) |

**Multi-Agent Mode:** NO — single source of truth required.
**CEO Checkpoint:** Approve vendor selection for critical/single-source/long-lead items.

## Workflow

### Step B.1: Compile Hierarchical BOM

Structure: assembly → subassembly → part. Each item must have a Part Number from BA Drawing Index.

```
FINAL BOM — {{project}} Rev v1.0
Date: {{today}}

LEVEL 0: {{product}} (1 unit)
├── LEVEL 1: Main Assembly A
│   ├── LEVEL 2: Subassembly A.1
│   │   ├── M-001 [part] qty=N
│   │   └── ...
│   └── LEVEL 2: Subassembly A.2
└── LEVEL 1: Main Assembly B
```

### Step B.2: BOM Tables (4 sections)

**MECHANICAL:**
| Item | Part No. | Description | Material | Qty | Dims (mm) | Process | Make/Buy | Vendor | Cost (VND) | Lead (d) | MIL/TCVN |
|----|----|----|----|----|----|----|----|----|----|----|----|

**ELECTRICAL:**
| Item | Part No. | Description | Package | Qty | Vendor | Cost (VND) | Lead (d) | RoHS | MIL/TCVN |
|----|----|----|----|----|----|----|----|----|----|

**FASTENERS & HARDWARE:**
| Item | Spec | Standard | Qty | Cost (VND) | Vendor |
|----|----|----|----|----|----|

**PURCHASED (COTS):**
| Item | Description | Supplier | Qty | Cost (VND) | Lead (d) | Single source? |
|----|----|----|----|----|----|----|

### Step B.3: Vietnam Local Content Target ≥60%

```
LOCAL CONTENT ANALYSIS:
| Category | Total VND | VN-source VND | % Local |
|----|----|----|----|
| Mechanical | | | |
| Electrical | | | |
| Fasteners | | | |
| COTS | | | |
| TOTAL | | | __% |

TARGET: ≥60% by value for Vietnamese defense programs
STATUS: [PASS / GAP — list imported items eligible for VN substitution]
```

### Step B.4: Cost Rollup vs Phase 3 Budget

```
COST RECONCILIATION:
| Category | P3 Estimate | P4 Final | Variance | Reason |
|----|----|----|----|----|
| Mechanical | | | ±% | |
| Electrical | | | ±% | |
| Fasteners | | | ±% | |
| COTS | | | ±% | |
| Assembly labor (est) | | | ±% | |
| **TOTAL unit cost** | | | **±%** | |

Variance threshold: ±10% — over → flag for CEO before proceeding.
```

### Step B.5: Long-Lead Procurement Schedule

```
LONG-LEAD ITEMS (lead > 4 weeks):
| Item | Lead (d) | Order By | Vendor | Critical Path? | Status |
|----|----|----|----|----|----|

ORDER-BY date calculation:
  Order By = TARGET_PRODUCTION_START - lead_days - safety_buffer(7d)

If Order By < TODAY → ⚠️ already late, schedule risk
```

### Step B.6: Single-Source Risk Flag

```
SINGLE-SOURCE RISK:
| Item | Vendor | Risk Level | Mitigation |
|----|----|----|----|
| | | HIGH/MED | qualify 2nd source / strategic stock / redesign |

HIGH risk items require CEO acknowledgment before BE handoff.
```

### Step B.7: MIL-STD / TCVN Requirements Traceability

For each item, map to applicable standards:
- MIL-STD-810H (environmental)
- MIL-STD-461G (EMC)
- TCVN_XXXX:YYYY (Vietnamese standards)
- AWS D1.2 / TCVN (welding)
- RoHS / REACH (electronics)

### Step B.8: Supplier Sign-Off Pack

For each Tier-1 (critical) vendor:
- Spec sheet sent + acknowledged
- Sample/test piece if applicable
- Quality agreement signed
- Payment terms confirmed

Append to `BOM_Final.md` under `## Supplier Sign-Off Status`.

## Output

`1_Projects/{{project}}/Phase4-Detail/{{variant}}/BOM_Final.md` — single source of truth.

Also export: `BOM_Final.csv` for ERPNext sync (rows match `erp-bom create` schema).

## CEO Checkpoint

```
═══ BLOCK BB FINAL BOM COMPLETE ═══
Items: {{N}} mech + {{N}} elec + {{N}} fasteners + {{N}} COTS
Unit cost: {{VND}} (variance vs P3: {{±%}})
Local content: {{%}} (target ≥60%)
Long-lead: {{N}} items, earliest order-by: {{date}}
Single-source HIGH risk: {{N}} items

CEO:
(1) ✅ Approve → tiếp tục Block BC (Inspection)
(2) 🔄 Revise vendor selection: [item list]
(3) ⏸️ Cost variance > 10% — review before proceeding
```

## COD

- BOM table compilation from drawings: Offload (O1)
- Cost rollup math: Offload (O1)
- Long-lead schedule calculation: Offload (O1)
- MIL/TCVN traceability tagging: Offload (O2)
- **Vendor selection for critical parts: Core (C)** — relationship + trust based
- **Single-source risk acceptance: Core (C)** — supply chain commitment
- **VN local content trade-off decisions: Core (C)** — strategic
