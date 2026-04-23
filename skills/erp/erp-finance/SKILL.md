---
description: "ERPNext Finance management — Purchase Order, Sales Invoice, Payment Entry. TT200 chart of accounts for Vietnam. Defense contract milestone billing. Triggers on: 'erp finance', 'erp invoice', 'erp po', 'purchase order erp', 'sales invoice erp', 'payment erp', 'hóa đơn erp', 'thanh toán erp', 'TT200'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# erp-finance — ERPNext Finance Management

> **HOK Layer:** Knowledge (procedural knowledge for PO, Invoice, Payment)
> **MCP Tools used:** `@casys/mcp-erpnext` — Purchase Order, Sales Invoice, Payment Entry
> **COD:** **Core** (CEO approves PO > 50M VND, all invoices) / Offload (AI drafts)

## Usage

```
/erp-finance                   → Finance dashboard: receivables, payables, cashflow
/erp-finance po                → Create Purchase Order (from reorder suggestion)
/erp-finance invoice sales     → Create Sales Invoice linked to WO/customer
/erp-finance invoice purchase  → Log Purchase Invoice from supplier
/erp-finance payment           → Record payment in/out
/erp-finance pnl               → Monthly P&L report
```

## Procedural Knowledge

### TT200 Chart of Accounts (Vietnam)
ERPNext must use Thông tư 200 chart of accounts:
- 152: Nguyên vật liệu (raw materials) — maps to WH-NVL stock value
- 154: Chi phí SXKD dở dang (WIP) — maps to WIP-[PX] warehouses
- 155: Thành phẩm (finished goods) — maps to WH-FG
- 331: Phải trả người bán (AP) — supplier payables
- 131: Phải thu khách hàng (AR) — customer receivables
- 511: Doanh thu (revenue) — sales invoices
- 632: Giá vốn hàng bán (COGS) — linked to BOM cost

### Purchase Order Flow
```
Reorder alert (/erp-stock or /ops)
  → PO drafted (AI) → CEO approves
  → PO sent to supplier
  → Goods received → Stock Entry (Receipt) via /erp-stock
  → Purchase Invoice received → matched to PO
  → Payment made → Payment Entry
```

**PO approval rules:**
- PO < 10M VND: PGĐ can approve
- PO ≥ 10M VND: CEO approval required
- PO ≥ 50M VND: CEO approval + written justification

### Sales Invoice — Defense Contract Billing
Defense contracts use **milestone billing**:
1. Contract signed → 30% advance (hóa đơn tạm ứng)
2. Prototype delivery → 40% progress (hóa đơn tạm tính)
3. Final acceptance → 30% completion (hóa đơn quyết toán)

Each invoice links to:
- Customer (from `Customers` sheet)
- Work Order(s) (which products delivered)
- Contract reference (hợp đồng số)

### Payment Entry
Record cash in/out with:
- Type: Receive (from customer) or Pay (to supplier)
- Reference: Invoice or PO number
- Payment method: Transfer / COD / Cash
- Auto-update Cashflow sheet in WX-OPS.xlsx

### Monthly P&L Generation
1. Revenue: sum Sales Invoices for month
2. COGS: sum BOM costs × units completed (from Stock Entry Manufacture)
3. Operating expenses: sum Purchase Invoices (non-material)
4. Gross margin: Revenue - COGS
5. Net: Gross margin - Operating expenses
6. Compare vs previous month + YTD

## ERPNext MCP Tool Mapping

| Action | MCP Tool | Pre-check |
|---|---|---|
| Create PO | `create_buying_purchase_order` | Supplier exists, items exist |
| Create Sales Invoice | `create_selling_sales_invoice` | Customer exists, WO reference |
| Get Invoices | `get_selling_sales_invoices` / `get_buying_purchase_invoices` | — |
| Payment Entry | `create_accounts_payment_entry` | Invoice must exist |
| P&L Report | `get_accounts_profit_loss` | Date range |

## Guardrails
- NEVER approve PO without CEO confirmation (≥10M VND)
- NEVER create Sales Invoice without matching WO/delivery
- NEVER guess unit prices — only from WX-OPS.xlsx or contract
- Defense contract invoices = Core (legal compliance, VAT, hợp đồng reference)
- KTT (Kế toán trưởng) validates TT200 compliance — AI cannot replace
