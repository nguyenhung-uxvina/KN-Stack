---
description: "ERPNext Master Data management — Item, Workstation, Operation, Routing. The foundation layer per ERP Dependency Chain. Gate rule: master data quality ≥90% before any Work Orders. Triggers on: 'erp master', 'erp item', 'item master', 'workstation', 'operation', 'routing', 'master data', 'dữ liệu gốc', 'tạo item', 'create item'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-master — ERPNext Master Data Management

> **HOK Layer:** Knowledge (procedural knowledge for Item/Workstation/Operation/Routing)
> **MCP Tools used:** `@casys/mcp-erpnext` — Item CRUD, Workstation, Operation, Routing
> **Galaxy anchor:** [[ERP Dependency Chain — Thứ Tự Bắt Buộc Không Thể Đảo]], [[Master Data Gravity — 80 Phần Trăm Effort ERP Nằm Ở Dữ Liệu Gốc]]
> **COD:** Offload (AI drafts) / Core (CEO validates naming + classification)

## Why This Skill Exists

Master Data Gravity Law: 80% ERP effort = master data quality. Item → Workstation → Operation → Routing is a **linear dependency chain that cannot be reordered**. This skill encodes the procedural knowledge to prevent the #1 ERPNext failure mode: creating Work Orders before master data is ready.

## Usage

```
/erp-master                    → Dashboard: master data completeness check
/erp-master item add           → Create new Item with WX naming convention
/erp-master item check CODE    → Validate item exists + completeness
/erp-master workstation        → List 4 PX workstations + capacity
/erp-master operation          → List operations per product line
/erp-master routing PRODUCT    → Show routing for a product variant
/erp-master audit              → Full master data quality audit (target ≥90%)
```

## Procedural Knowledge

### Item Naming Convention (MANDATORY)
Format: `[MATERIAL]-[SPEC]` or `[TYPE]-[SPEC]`
- Metals: `ALU-6061-10`, `STEEL-60x40`, `STEEL-PIPE-114`
- Electronics: `ESP32-WROOM`, `ENCODER-600P`, `BTS7960`
- Fasteners: `BOLT-M10x30`
- COTS: `PROJ-BENQ`, `RTX4090`
- Machined: `TRUNNION-PIN-25`, `SPADE-GRIP`

**Before creating any Item:**
1. Check if item already exists in `Stock Ledger` sheet of WX-OPS.xlsx
2. Verify item_code follows naming convention
3. Confirm UOM is metric (m, mm, kg, cái, bộ, tấm)
4. Assign to correct Item Group (Metals/Electronics/Fasteners/COTS/Bearings/Mechanical/Machined/Consumables)
5. Set default warehouse: `WH-NVL`

### 4 Workstations (fixed — maps to 4 PX)
| ERPNext Workstation | Workshop X PX | Capacity | Skills |
|---|---|---|---|
| WS-CKCX | PX Cơ Khí Chính Xác | 4 workers × 8h = 32h/day | CNC, Welding, Assembly |
| WS-DT | PX Điện Tử | 4 workers × 8h = 32h/day | PCB, Soldering, Testing |
| WS-DC | PX Điện Cơ | 4 workers × 8h = 32h/day | Wiring, Integration |
| WS-VL | PX Vật Liệu | 4 workers × 8h = 32h/day | Surface Treatment, Packaging |

### Operation → Routing Chain
Operations are product-specific steps assigned to workstations.
Routing = ordered sequence of operations for a product variant.

**Before creating Routing:**
1. All Operations must exist
2. Each Operation must reference a valid Workstation
3. Time estimates must come from `_routing.md` or actual production data — NEVER guess

### Master Data Quality Audit
When `/erp-master audit` is called:
1. Read all items from `Stock Ledger` sheet → check naming convention compliance
2. Check: every BOM item_code exists in Stock Ledger
3. Check: every product in `Work Orders` has a routing in `_routing.md`
4. Calculate: `quality_score = (compliant_items / total_items) × 100`
5. **Gate: quality_score ≥ 90% required before ERPNext Work Order creation**

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Create Item | `create_manufacturing_item` | Naming convention + UOM + no duplicate |
| List Items | `get_manufacturing_items` | — |
| Create Workstation | `create_workstation` | Fixed 4 only — rarely needed |
| Create Operation | `create_operation` | Workstation must exist |
| Create Routing | `create_routing` | All operations must exist |

## Guardrails
- NEVER create Items with generic names ("part1", "material A")
- NEVER skip UOM validation — must be metric
- NEVER create duplicate items — always search first
- Master data changes = CEO approval required (naming affects entire chain)
