---
name: erp-production
description: "ERPNext Production management — Work Order, Job Card, Stock Entry (Manufacture). Encodes ERP Dependency Chain for production flow. Triggers on: 'erp production', 'erp work order', 'erp wo', 'erp job card', 'lệnh sản xuất erp', 'tạo wo erp', 'job card'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-production — ERPNext Production Management

> **HOK Layer:** Knowledge (procedural knowledge for Work Order → Job Card → Stock Entry)
> **MCP Tools used:** `@casys/mcp-erpnext` — Work Order, Job Card, Stock Entry (Manufacture)
> **Galaxy anchor:** [[ERP Dependency Chain — Thứ Tự Bắt Buộc Không Thể Đảo]], [[Stock Entry Truth — Không Có Chứng Từ Số Thì Không Tồn Tại]]
> **COD:** Offload (AI creates WO draft) / **Core** (CEO releases WO = production commitment)

## Usage

```
/erp-production                → Production dashboard from ERPNext
/erp-production wo add         → Create Work Order (BOM + Routing must exist)
/erp-production wo WO-ID       → View WO detail + Job Card status
/erp-production jobcard        → List active Job Cards per PX
/erp-production complete WO-ID → Complete WO → auto Stock Entry (Manufacture)
```

## Procedural Knowledge

### Work Order Creation Pre-flight (MANDATORY)
Before creating ANY Work Order:
1. **BOM exists?** → check via `/erp-bom check PRODUCT` — if no BOM, STOP
2. **Routing exists?** → check `_routing.md` — if no routing, STOP  
3. **Material available?** → run Material Availability Check from `/ops` intelligence
4. Show material impact to CEO: "Nếu tạo WO → [items affected]"
5. **CEO confirms** → create WO (status: Draft)
6. **CEO releases** → WO status: Not Started → material reserved

### Job Card Flow per PX
```
Work Order (released)
  → Job Card WS-CKCX (Draft → Open → Complete)
  → Job Card WS-DT   (Draft → Open → Complete)
  → Job Card WS-DC   (Draft → Open → Complete)
  → Job Card WS-VL   (Draft → Open → Complete)
  → All Job Cards Complete → Stock Entry (Manufacture) → WO Completed
```

Each Job Card:
- Assigned to 1 Workstation (PX)
- Has planned hours (from Routing)
- Logs actual hours (from Daily Log)
- Completion triggers next PX in sequence

### Stock Entry (Manufacture) — Production Completion
When all Job Cards for a WO are complete:
1. Auto-generate Stock Entry type "Manufacture"
2. **Consume:** raw materials per BOM (deduct from WH-NVL)
3. **Produce:** finished goods (add to WH-FG)
4. Stock Ledger updated automatically
5. **This is the Stock Entry Truth** — no Stock Entry = product doesn't exist in system

### WO Release = Core Decision
WO release commits materials + PX capacity. This is a **production commitment** that:
- Reserves materials (blocks other WOs from using same stock)
- Allocates PX capacity (affects heatmap)
- Sets customer expectation (target_date)

**AI recommends, CEO releases.**

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Create WO | `create_manufacturing_work_order` | BOM + Routing exist, material check |
| Get WO | `get_manufacturing_work_orders` | — |
| Create Job Card | Auto from WO + Routing | WO must be released |
| Complete Job Card | Update via API | Actual hours logged |
| Stock Entry | `create_inventory_stock_entry` | All Job Cards complete |

## Guardrails
- NEVER create WO without existing BOM + Routing
- NEVER release WO without CEO approval — production commitment
- NEVER skip material availability check
- NEVER manually create Stock Entry for manufacture — must flow from WO completion
