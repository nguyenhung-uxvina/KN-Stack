---
description: "ERPNext Quality management — Quality Inspection, NCR tracking, FPY analysis. Links QC gates to Work Orders for traceability. Triggers on: 'erp quality', 'erp qc', 'quality inspection', 'erp ncr', 'kiểm tra chất lượng erp', 'fpy erp', 'inspection erp'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-quality — ERPNext Quality Management

> **HOK Layer:** Knowledge (procedural knowledge for Quality Inspection + NCR)
> **MCP Tools used:** `@casys/mcp-erpnext` — Quality Inspection, custom NCR doctype
> **COD:** Offload (AI logs inspection) / **Core** (CEO/QĐ judges PASS/FAIL)

## Usage

```
/erp-quality                   → QC dashboard: FPY, open NCRs, gate pass rates
/erp-quality inspect WO-ID     → Log gate inspection (PASS/FAIL)
/erp-quality ncr               → List open NCRs + pattern analysis
/erp-quality fpy PRODUCT       → FPY trend for a product line
```

## Procedural Knowledge

### QC Gate Structure (maps to 4 PX + Final)
| Gate | After PX | Inspector | Criteria |
|---|---|---|---|
| Gate-CKCX | WS-CKCX | QĐ Cơ Khí | Dimensional, surface finish |
| Gate-DT | WS-DT | QĐ Điện Tử | Electrical, functional test |
| Gate-DC | WS-DC | QĐ Điện Cơ | Integration, wiring check |
| Gate-VL | WS-VL | QĐ Vật Liệu | Surface treatment, packaging |
| Gate-Final | All PX done | CEO/PGĐ | Full system acceptance |

### Inspection → Job Card Traceability
Every Quality Inspection in ERPNext links to:
1. **Work Order** (which product)
2. **Job Card** (which PX step)
3. **Inspector** (who judged)
4. **Result** (PASS/FAIL)
5. If FAIL → NCR auto-created with mandatory fields

### NCR Workflow
```
FAIL detected → NCR created (auto-ID: NCR-YYYY-NNN)
  → ncr_category: Dimensional | Electrical | Assembly | Material | Cosmetic
  → root_cause: required
  → corrective_action: required
  → rework_hours: logged
  → NCR closed when corrective action verified
```

### NCR Pattern Detection (≥10 records)
1. Group NCRs by category × gate × product
2. Identify hotspots: "80% NCR tại Gate-CKCX là Dimensional"
3. Suggest: design standard update, fixture calibration, training
4. Feed patterns back to `/ops qc` intelligence algorithm

### FPY Calculation
`FPY = (units passing first inspection) / (total units inspected) × 100`
- Per product line
- Per gate
- Trend: this month vs last month
- Target: ≥ 90% (defense quality standard)

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Create Inspection | Quality Inspection via API | WO + Job Card must exist |
| Get Inspections | Filter by WO/product/date | — |
| NCR (custom doctype) | Create/update via API | Inspection result = FAIL |

## Guardrails
- NEVER auto-set PASS/FAIL — QĐ/CEO physical inspection = Core
- NEVER skip NCR for FAIL results — every FAIL must have root cause
- NEVER generate root causes from general knowledge — must be observed on shop floor
- AI role: log, calculate FPY, detect patterns — NOT judge quality
