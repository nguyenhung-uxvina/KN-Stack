---
description: "ERPNext Stock/Inventory management — Stock Entry, Stock Ledger, Warehouse, Material Transfer. Encodes Stock Entry Truth Law. Triggers on: 'erp stock', 'erp inventory', 'erp kho', 'stock entry', 'material transfer', 'nhập kho', 'xuất kho', 'chuyển kho', 'reorder erp'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-stock — ERPNext Stock/Inventory Management

> **HOK Layer:** Knowledge (procedural knowledge for Stock Entry, Warehouse, Reorder)
> **MCP Tools used:** `@casys/mcp-erpnext` — Stock Entry, Stock Ledger, Warehouse
> **Galaxy anchor:** [[Stock Entry Truth — Không Có Chứng Từ Số Thì Không Tồn Tại]]
> **COD:** Offload (AI generates entries) / Core (NV Kho confirms physical count)

## Usage

```
/erp-stock                     → Stock dashboard + reorder alerts
/erp-stock receive PO-ID       → Receive goods from PO → Stock Entry (Receipt)
/erp-stock issue WO-ID         → Issue materials to PX → Stock Entry (Issue)
/erp-stock transfer FROM TO    → Transfer between warehouses
/erp-stock reconcile           → Compare WX-OPS.xlsx vs ERPNext stock
/erp-stock reorder             → Generate reorder suggestions
```

## Procedural Knowledge

### Stock Entry Types (ERPNext)
| Type | When | From → To |
|---|---|---|
| Material Receipt | Goods received from supplier | — → WH-NVL |
| Material Issue | Materials sent to PX for WO | WH-NVL → WIP-[PX] |
| Material Transfer | Move between warehouses | WH-A → WH-B |
| Manufacture | WO completed (auto from erp-production) | WH-NVL → WH-FG |

### Warehouse Structure (maps to WX physical layout)
| ERPNext Warehouse | Physical Location | Purpose |
|---|---|---|
| WH-NVL | Kho nguyên vật liệu | Raw materials + COTS |
| WIP-CKCX | PX Cơ Khí CX | Work-in-progress CK |
| WIP-DT | PX Điện Tử | Work-in-progress ĐT |
| WIP-DC | PX Điện Cơ | Work-in-progress ĐC |
| WIP-VL | PX Vật Liệu | Work-in-progress VL |
| WH-FG | Kho thành phẩm | Finished goods |

### Stock Entry Truth Protocol
**Every physical material movement MUST have a Stock Entry.**
- NV Kho receives goods → Stock Entry (Receipt) + update PO status
- QĐ requests materials → Stock Entry (Issue) referencing WO
- Transfer between PX → Stock Entry (Transfer)
- No Stock Entry = material doesn't exist in system (even if physically present)

### Reorder Logic
1. Read `Stock Ledger` sheet → find items where `qty_on_hand ≤ reorder_level`
2. Cross-reference with active WO demand (BOM × qty)
3. Priority: BLOCKING (needed for active WO) > LOW (below reorder) > OK
4. Suggest PO with supplier from `Suppliers` sheet + lead_time_days
5. CEO approves → create PO via `/erp-finance` or manual

### Reconciliation (WX-OPS.xlsx ↔ ERPNext)
During Phase 0→1 transition:
1. Export ERPNext Stock Ledger via MCP
2. Compare with `Stock Ledger` sheet in WX-OPS.xlsx
3. Flag discrepancies: item exists in one but not other, qty mismatch
4. CEO decides which source is correct
5. Adjust the other source

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Stock Entry (all types) | `create_inventory_stock_entry` | Valid warehouse, item exists |
| Get Stock Balance | `get_inventory_stock_balance` | — |
| Get Stock Ledger | `get_inventory_stock_ledger` | — |

## Guardrails
- NEVER adjust stock without a Stock Entry document
- NEVER guess quantities — always reference PO, WO, or physical count
- Stock accuracy target: ≥95% (current ~60% per Galaxy note)
- NV Kho physical confirmation = Core — AI cannot replace physical count
