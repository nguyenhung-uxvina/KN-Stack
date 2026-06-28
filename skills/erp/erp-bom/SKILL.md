---
name: erp-bom
description: "ERPNext BOM (Bill of Materials) management — create, compare, version control. Encodes BOM Immutability Law. Triggers on: 'erp bom', 'bom erp', 'tạo bom', 'create bom', 'bom version', 'bom compare', 'amendment'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-bom — ERPNext BOM Management

> **HOK Layer:** Knowledge (procedural knowledge for BOM CRUD + versioning)
> **MCP Tools used:** `@casys/mcp-erpnext` — BOM CRUD, BOM comparison
> **Galaxy anchor:** [[ERP Dependency Chain — Thứ Tự Bắt Buộc Không Thể Đảo]]
> **COD:** Offload (AI drafts BOM from WX-OPS.xlsx, or maps [[helix-cad-ingest]] MASTER_BOM.csv → diff via `import-cad`) / Core (CEO accepts diff + approves final BOM)

## Why This Skill Exists

BOM Immutability Law: a submitted BOM cannot be edited — only amended (new version). This skill encodes the knowledge to prevent cascading errors from incorrect BOMs, which would affect every downstream Work Order.

## Usage

```
/erp-bom                       → List all BOMs per product/variant
/erp-bom create PRODUCT        → Create BOM from WX-OPS.xlsx BOM Master sheet
/erp-bom compare V1 V2         → Compare two BOM versions
/erp-bom check PRODUCT         → Validate BOM completeness (all items exist?)
/erp-bom sync                  → Sync WX-OPS.xlsx BOM Master ↔ ERPNext
/erp-bom import-cad CSV        → Import [[helix-cad-ingest]] MASTER_BOM.csv as a feeder → DIFF vs BOM Master → CEO accepts → write
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

### Import-CAD Feeder Path (`/erp-bom import-cad <MASTER_BOM.csv>`)
Alternate IMPORT path that lets a [[helix-cad-ingest]] aggregate seed BOM Master — WITHOUT bypassing the guardrail. The CSV is an **import feeder only**; `BOM Master` stays the source of truth AFTER the CEO accepts the diff.
1. Read `MASTER_BOM.csv` produced by [[helix-cad-ingest]] `aggregate.py`.
2. **Column mapping** (ingest → BOM Master): `item`→item_name, `code`→item_code, `name`→description, `qty`→qty_per_unit, `material`→material, `thickness`→thickness/spec. Flag any unmapped or blank-code rows.
3. **Build a DIFF** against the existing `BOM Master` sheet (added lines / changed qty or material / removed lines / unchanged). NEVER write yet.
4. **Present the DIFF to the CEO** (Core decision — same approval bar as `create`). 
5. On CEO accept → merge accepted lines into `BOM Master`; on reject → discard, no change.
6. After acceptance, the normal `create`/`sync` flow runs against the now-updated `BOM Master`.
This closes the [[helix-cad-ingest]] → ERPNext BOM loop (read-from-drawings BOM → reviewed → BOM Master) while keeping the immutability + source-of-truth rules intact.

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
- NEVER generate BOM quantities from general knowledge — only from WX-OPS.xlsx data OR a [[helix-cad-ingest]] `MASTER_BOM.csv` feeder via `import-cad` (CEO-reviewed diff before any write)
- `import-cad` is a FEEDER, not a new source of truth — `BOM Master` remains authoritative AFTER the CEO accepts the diff; NEVER write CSV rows directly to ERPNext without the diff-accept step
- BOM approval = Core (CEO judgment) — AI drafts only
