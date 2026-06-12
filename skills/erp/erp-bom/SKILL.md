---
name: erp-bom
description: "ERPNext BOM (Bill of Materials) management — create, compare, version control. Encodes BOM Immutability Law. Triggers on: 'erp bom', 'bom erp', 'tạo bom', 'create bom', 'bom version', 'bom compare', 'amendment'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-bom — ERPNext BOM Management

> **HOK Layer:** Knowledge (procedural knowledge for BOM CRUD + versioning)
> **MCP Tools used:** `@casys/mcp-erpnext` — BOM CRUD, BOM comparison
> **Galaxy anchor:** [[ERP Dependency Chain — Thứ Tự Bắt Buộc Không Thể Đảo]]
> **COD:** Offload (AI drafts BOM from WX-OPS.xlsx) / Core (CEO approves final BOM)

## Why This Skill Exists

BOM Immutability Law: a submitted BOM cannot be edited — only amended (new version). This skill encodes the knowledge to prevent cascading errors from incorrect BOMs, which would affect every downstream Work Order.

## Usage

```
/erp-bom                       → List all BOMs per product/variant
/erp-bom create PRODUCT        → Create BOM from WX-OPS.xlsx BOM Master sheet
/erp-bom compare V1 V2         → Compare two BOM versions
/erp-bom check PRODUCT         → Validate BOM completeness (all items exist?)
/erp-bom sync                  → Sync WX-OPS.xlsx BOM Master ↔ ERPNext
```

## Procedural Knowledge

### BOM Creation Sequence (MANDATORY)
1. **Pre-flight:** ALL items in BOM must exist in Item master (run `/erp-master item check` first)
2. Read `BOM Master` sheet from WX-OPS.xlsx → filter by product + variant
3. For each row: verify item_code exists, qty_per_unit > 0, UOM matches Item master
4. **Flag missing items** before creating BOM — NEVER create BOM with missing items
5. Present BOM to CEO for approval
6. Create BOM in ERPNext via MCP → set as default BOM for the Item

### BOM Amendment Workflow
ERPNext BOMs are **immutable once submitted**. To change:
1. Amend existing BOM → creates new version (BOM-PRODUCT-002)
2. Compare old vs new → show diff to CEO
3. CEO approves → new BOM becomes default
4. Old BOM stays for historical reference — NEVER delete

### BOM ↔ WX-OPS.xlsx Sync
- **Source of truth during Phase 0:** WX-OPS.xlsx `BOM Master` sheet
- **Source of truth after ERPNext live:** ERPNext BOM
- **Sync direction:** XLSX → ERPNext (Phase 0-1), ERPNext → XLSX (Phase 2+)
- When syncing: flag any discrepancies for CEO review

### Cross-check with Stock
When creating or reviewing BOM:
1. For each BOM item: check `Stock Ledger` sheet → qty_on_hand
2. Calculate: can this BOM be fulfilled N times? `max_builds = min(qty_on_hand / qty_per_unit)`
3. Report: "BOM cho TOWED-TARGET 30mm: có thể build 4 units trước khi hết ALU-6061-10"

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Create BOM | `create_manufacturing_bom` | All items exist in Item master |
| Get BOM | `get_manufacturing_bom` | — |
| List BOMs | `get_manufacturing_items` (filter) | — |
| Amend BOM | Amend workflow via API | CEO approval required |

## Guardrails
- NEVER create BOM with items that don't exist in Item master
- NEVER delete a submitted BOM — amend only
- NEVER generate BOM quantities from general knowledge — only from WX-OPS.xlsx data
- BOM approval = Core (CEO judgment) — AI drafts only
