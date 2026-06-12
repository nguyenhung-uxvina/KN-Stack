---
name: ops
description: "WX-OPS — Workshop X AI-First Operations System. Manage production, inventory, finance, HR, CRM, and QC with AI intelligence layer (capacity planning, material forecasting, delay prediction, reorder alerts, NCR pattern detection). XLSX workbook (ERPNext-compatible). Triggers on: 'ops', 'production', 'sản xuất', 'work order', 'lệnh sản xuất', 'inventory', 'tồn kho', 'kho', 'stock', 'finance', 'tài chính', 'invoice', 'hóa đơn', 'cashflow', 'dòng tiền', 'HR', 'nhân sự', 'employee', 'CRM', 'khách hàng', 'customer', 'deal', 'pipeline', 'briefing', 'capacity', 'overload', 'thiếu vật tư', 'delay', 'QC', 'quality', 'chất lượng', 'NCR', 'inspection', 'kiểm tra'."
allowed-tools: ["Read", "Write", "Edit", "Glob", "Grep", "Bash", "Agent"]
---

# WX-OPS — Workshop X AI-First Operations System

> **Architecture:** XLSX workbook (ERPNext-compatible) + Claude Code skills + AI Intelligence Layer
> **Location:** `2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx`
> **Users:** CEO (primary), QĐ (production input), KTT/NV TC (finance input)
> **Migration:** Export sheets → CSV → ERPNext Data Import. Or direct via `@casys/mcp-erpnext` MCP server.
> **AI-First:** System THINKS, not just STORES — capacity planning, material forecasting, delay prediction
> **Team access:** QĐ/KTT/NV mở WX-OPS.xlsx bằng Excel — quen thuộc, không cần training

## Usage

```
/ops                          → AI BRIEFING: full morning briefing with intelligence
/ops production               → Work orders + delay predictions + capacity heatmap
/ops production add           → Create WO + auto material availability check
/ops production update WO-ID  → Update WO status + cascade effects
/ops production log           → Log daily production activity
/ops inventory                → Stock levels + reorder alerts cross-referenced with WOs
/ops inventory check ITEM     → Check specific item stock + WO demand forecast
/ops inventory po             → Create purchase order
/ops finance                  → Monthly P&L, cash flow summary
/ops finance invoice          → Log new invoice
/ops finance cashflow         → Log cash in/out
/ops qc                       → QC dashboard: pass rate, NCR patterns, FPY trend
/ops qc log                   → Log gate inspection result (pass/fail + NCR if fail)
/ops qc ncr                   → View open NCRs, pattern analysis
/ops hr                       → Employee list, skill matrix
/ops crm                      → Customer pipeline, deals
/ops crm add                  → Add customer/deal
```

## Data Location

**Primary data file:** `2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx` (1 workbook, 11 sheets)

```
WX-OPS.xlsx
  ├── Sheet: Work Orders        ← All work orders (ERPNext: Work Order)
  ├── Sheet: BOM Master         ← BOM per product/variant (material requirements)
  ├── Sheet: Daily Log          ← Daily production activity log (actual vs planned)
  ├── Sheet: QC Log             ← Gate inspection results + NCR tracking
  ├── Sheet: Stock Ledger       ← Current stock levels (ERPNext: Stock Ledger)
  ├── Sheet: Suppliers          ← Supplier database (ERPNext: Supplier)
  ├── Sheet: Purchase Orders    ← Purchase orders (ERPNext: Purchase Order)
  ├── Sheet: Invoices           ← Sales + Purchase invoices
  ├── Sheet: Cashflow           ← Cash in/out log
  ├── Sheet: Employees          ← 26 employees (ERPNext: Employee)
  ├── Sheet: Customers          ← Customer database (ERPNext: Customer)
  └── Sheet: Deals              ← Deal pipeline (ERPNext: Opportunity)

Supporting files (same folder):
  ├── Production/_routing.md    ← Production routing per product (Markdown — lookup table)
  ├── Finance/_monthly_pnl.md   ← Generated monthly P&L (Markdown — auto-generated)
  └── _WX_OPS_Dashboard.md     ← Master dashboard
```

### XLSX I/O Protocol

**Read sheet** (dùng python + openpyxl):
```bash
python -c "
import openpyxl, json
wb = openpyxl.load_workbook('2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx')
ws = wb['Sheet Name']
headers = [c.value for c in ws[1]]
rows = []
for row in ws.iter_rows(min_row=2, values_only=True):
    if any(v is not None for v in row):
        rows.append(dict(zip(headers, row)))
print(json.dumps(rows, default=str, ensure_ascii=False, indent=2))
"
```

**Append row** to a sheet:
```bash
python -c "
import openpyxl
from datetime import datetime
wb = openpyxl.load_workbook('2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx')
ws = wb['Sheet Name']
ws.append([value1, value2, ...])
wb.save('2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx')
"
```

**Update cell** in a sheet:
```bash
python -c "
import openpyxl
wb = openpyxl.load_workbook('2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx')
ws = wb['Sheet Name']
# Find row by key column (e.g., wo_id in column A)
for row in ws.iter_rows(min_row=2):
    if row[0].value == 'WO-2026-004':
        row[N].value = 'new_value'
        break
wb.save('2_Areas/BRIDGE — Operations/WX-OPS/WX-OPS.xlsx')
"
```

**Sheet name ↔ old CSV mapping:**

| Sheet Name | Old CSV File | ERPNext DocType |
|---|---|---|
| Work Orders | _work_orders.csv | Work Order |
| BOM Master | _bom_master.csv | BOM |
| Daily Log | _daily_log.csv | Job Card |
| QC Log | _qc_log.csv | Quality Inspection |
| Stock Ledger | _stock_ledger.csv | Stock Ledger Entry |
| Suppliers | _suppliers.csv | Supplier |
| Purchase Orders | _purchase_orders.csv | Purchase Order |
| Invoices | _invoices.csv | Sales/Purchase Invoice |
| Cashflow | _cashflow.csv | Payment Entry |
| Employees | _employees.csv | Employee |
| Customers | _customers.csv | Customer |
| Deals | _deals.csv | Opportunity |

**Concurrent access guard:** WX-OPS.xlsx may be open in Excel by team members. If `openpyxl` fails with PermissionError → warn CEO: "File đang mở bởi người khác. Đóng Excel rồi thử lại." NEVER force-write over a locked file.

---

## AI INTELLIGENCE LAYER

### When `/ops` is called (no args) → Generate AI Morning Briefing

Read ALL data files, then produce a consolidated briefing:

```
═══════════════════════════════════════════════════
  WX-OPS AI BRIEFING — [date]
═══════════════════════════════════════════════════

📊 PRODUCTION STATUS
  Active WOs: [N] | Completed this month: [N] | Overdue: [N]
  [Table: wo_id | product | status | target_date | risk]

🏭 PX CAPACITY HEATMAP
  WS-CKCX: [█████░░░░░] 50% (WO-001 + WO-004)
  WS-DT:   [███░░░░░░░] 30% (WO-002)
  WS-DC:   [░░░░░░░░░░]  0%
  WS-VL:   [░░░░░░░░░░]  0%
  ⚠️ [Flag if any PX > 80%]

📦 MATERIAL ALERTS
  🔴 BLOCKING: [items that block active WOs]
  🟡 LOW: [items below reorder level but not blocking]
  ✅ OK: [N] items adequate

⏰ DELAY PREDICTIONS
  [WOs at risk of missing target_date, with reason]

📋 TODAY'S PRIORITIES
  1. [Highest priority action based on analysis]
  2. [Second priority]
  3. [Third priority]
═══════════════════════════════════════════════════
```

### Intelligence Algorithm: Material Availability Check

When viewing WOs or creating new WO, ALWAYS run this check:

1. Read sheet `BOM Master` → get materials needed per product/variant
2. For EACH active/queued WO in sheet `Work Orders`:
   - Calculate: `demand = wo_qty × bom_qty_per_unit`
   - Sum total demand across ALL active WOs per item_code
3. Read sheet `Stock Ledger` → get qty_on_hand per item_code
4. Compare: `surplus = qty_on_hand - total_demand_all_WOs`
5. Output per item:
   - `✅ ĐỦ` if surplus > 0
   - `⚠️ VỪA` if surplus = 0
   - `❌ THIẾU [N]` if surplus < 0 → flag which WOs affected

**When creating new WO (`/ops production add`):**
- Run material check BEFORE confirming
- Show: "Nếu tạo WO này, material status sẽ thay đổi:"
- CEO quyết định: proceed (accept shortage) hoặc cancel

### Intelligence Algorithm: PX Capacity Heatmap

1. Read sheet `Work Orders` → filter status = "In Process" or "Queued"
2. For each WO, determine current PX from `current_px` column
3. Read `_routing.md` → get est. time per PX per product
4. Calculate per PX:
   - `load_hours = Σ (remaining_units × hours_per_step)`
   - `capacity = 4 workers × 8 hours = 32 hours/day`
   - `utilization = load_hours / capacity`
5. Display as bar chart:
   - 🟢 < 50% | 🟡 50-80% | 🔴 > 80%
6. If PX > 100% → flag bottleneck, suggest: reschedule lower-priority WO or overtime

### Intelligence Algorithm: Delay Prediction

For each active WO:
1. Calculate `planned_end = start_date + lead_time` (from routing)
2. Check PX queue: if current PX has multiple WOs → add queue delay
3. Check material: if ❌ THIẾU → add procurement lead time (~7 days domestic)
4. `predicted_end = planned_end + queue_delay + material_delay`
5. Compare vs `target_date`:
   - ✅ On track: predicted_end ≤ target_date
   - ⚠️ At risk: predicted_end within 3 days of target_date
   - 🔴 Late: predicted_end > target_date → flag with reason + suggested action

### Intelligence Algorithm: Reorder Alert System

When running `/ops` or `/ops inventory`:
1. Read sheet `Stock Ledger` → find items where `qty_on_hand ≤ reorder_level`
2. Cross-reference with BOM demand from active WOs:
   - `production_demand = Σ(active_wo_qty × bom_qty_per_unit)` per item
   - `net_available = qty_on_hand - production_demand`
3. Classify alerts:
   - 🔴 BLOCKING: `net_available < 0` AND item needed by active WO with target < 30 days
   - 🟡 LOW: `qty_on_hand ≤ reorder_level` but not blocking production
   - 🟢 ADEQUATE: `qty_on_hand > reorder_level`
4. For 🔴 items: show supplier from sheet `Suppliers` + suggested PO quantity
5. Write alerts to `Inventory/_reorder_alerts.md` (overwrite each run)

### Intelligence Algorithm: Daily Log Analytics

When `/ops production log` is called:
1. Prompt CEO: date, wo_id, px, activity, hours, output_qty, notes
2. Append row to sheet `Daily Log`
3. After logging, show quick analytics:
   - This WO: actual hours logged vs routing estimate
   - This PX: total hours today across all WOs
   - Trend: if > 3 data points for same product, show avg hours vs planned

### Intelligence Algorithm: QC & NCR Pattern Detection

When `/ops qc` is called:
1. Read sheet `QC Log` → calculate per product/variant:
   - **FPY (First Pass Yield)** = PASS count / total inspections
   - **Gate pass rate** per PX gate (Gate-CKCX, Gate-DT, Gate-DC, Gate-VL)
2. **NCR Pattern Analysis** (after ≥ 10 NCR records):
   - Group NCRs by `ncr_category` (Dimensional, Electrical, Assembly, Material, Cosmetic)
   - Group by product + gate → find hotspots
   - "80% NCR từ 3 tháng qua liên quan đến [category X] tại [Gate Y]"
   - Suggest corrective action or design standard update
3. **Rework cost tracking:**
   - Sum `rework_hours` per product → estimate rework cost
   - Flag products with rework > 10% of routing time
4. Include QC summary in `/ops` AI briefing:
   ```
   🔍 QC STATUS
     FPY this month: [X]% | NCRs open: [N] | Top NCR category: [X]
     ⚠️ [Pattern alert if detected]
   ```

When `/ops qc log` is called:
1. Prompt: date, wo_id, gate (Gate-CKCX/DT/DC/VL/Final), result (PASS/FAIL)
2. If FAIL → prompt: ncr_category, ncr_description, root_cause, corrective_action
3. Auto-generate NCR ID: `NCR-YYYY-NNN`
4. Append to sheet `QC Log`
5. Show: "This product FPY so far: [X]% ([N] pass / [M] total)"

### Compound Learning (when data accumulates)

After ≥ 5 completed WOs for same product:
- Calculate actual avg lead time vs routing estimate
- If actual > planned by > 20% → suggest updating routing
- Flag: "TOWED-TARGET actual lead time = 9.2 days vs planned 7.5 days. Suggest update routing?"

---

## Module Specifications

### PRODUCTION (`/ops production`)

**Read** sheet `Work Orders`, sheet `BOM Master`, sheet `Stock Ledger`, sheet `Daily Log` and present:

1. **Dashboard view (ALWAYS includes intelligence):**
   - Total active WOs, by status (Queued/In Process/Completed)
   - **PX Capacity Heatmap** (run Intelligence Algorithm above)
   - **Delay Predictions** for each active WO (run Intelligence Algorithm above)
   - Critical/overdue WOs (target_date < today and not completed)

2. **Add work order** (`/ops production add`):
   - Prompt: product, variant, quantity, priority, customer, target date
   - Auto-generate WO-ID: `WO-YYYY-NNN` (next sequential)
   - Look up routing from `_routing.md` → pre-fill PX status columns
   - **MANDATORY: Run Material Availability Check BEFORE confirming**
   - Show material impact: "Nếu tạo WO này → [items affected]"
   - CEO confirms → append row to sheet `Work Orders`

3. **Update status** (`/ops production update WO-2026-004`):
   - Read current row
   - CEO/QĐ specifies: which PX completed / which PX starting
   - Update status columns
   - If all 4 PX + QC completed → status = "Completed", set completed_date
   - **After update: show cascade effects** (next PX load change, material release)

4. **Log daily activity** (`/ops production log`):
   - Prompt: date (default today), wo_id, px, activity, hours, output_qty, notes
   - Append to sheet `Daily Log`
   - Show quick analytics: actual vs planned hours for this WO

### INVENTORY (`/ops inventory`)

**Read** sheet `Stock Ledger`, sheet `BOM Master`, sheet `Work Orders` and present:

1. **Dashboard view (ALWAYS includes intelligence):**
   - **Reorder Alerts** (run Reorder Alert Intelligence Algorithm)
     - 🔴 BLOCKING: items that block active WOs
     - 🟡 LOW: below reorder but not blocking
     - ✅ OK: adequate stock
   - Total inventory value (Σ qty × unit_cost)
   - Items with zero stock
   - **Production demand forecast**: total material needed by all active WOs

2. **Check item** (`/ops inventory check ESP32`):
   - Search by item_code or item_name (fuzzy match)
   - Show: qty, reorder level, supplier, last price
   - **NEW: Show which active WOs need this item + total demand**

3. **Stock adjustment:**
   - Receive: add qty (material received from supplier)
   - Issue: subtract qty (material issued to PX for work order)
   - Transfer: move between warehouses (WH-NVL → WIP-CKCX)
   - Update sheet `Stock Ledger` qty_on_hand and last_updated
   - **After adjustment: re-check if any reorder alert status changed**

4. **Purchase order** (`/ops inventory po`):
   - Items below reorder → suggest PO
   - **Priority-ranked by production impact** (blocking WOs first)
   - Create PO entry in sheet `Purchase Orders`
   - Show supplier + lead time from sheet `Suppliers`

### FINANCE (`/ops finance`)

**Read** sheet `Invoices` + sheet `Cashflow` and present:

1. **Dashboard:**
   - Revenue this month (sum Sales invoices)
   - Expenses this month (sum Purchase invoices)
   - Cash balance (running total from cashflow)
   - Outstanding receivables (invoices unpaid)
   - Outstanding payables (invoices unpaid)

2. **Log invoice** (`/ops finance invoice`):
   - Type: Sales or Purchase
   - Customer/Supplier, product, qty, price
   - Append to sheet `Invoices`

3. **Log cash** (`/ops finance cashflow`):
   - In or Out, category, amount, reference
   - Append to sheet `Cashflow`

4. **Monthly P&L** (`/ops finance pnl`):
   - Read invoices for current month
   - Calculate: Revenue - COGS - Operating expenses
   - Generate `_monthly_pnl.md`

### HR (`/ops hr`)

**Read** sheet `Employees`:
- Employee list with department, PX, skills
- Headcount per PX
- Skill matrix (who can do what)

### QC (`/ops qc`)

**Read** sheet `QC Log` and present:

1. **Dashboard view (ALWAYS includes intelligence):**
   - **FPY (First Pass Yield)** per product line — PASS / total inspections
   - Gate pass rate per PX gate
   - Open NCRs (result=FAIL, no corrective_action logged)
   - **NCR Pattern Analysis** (run QC Intelligence Algorithm above)
   - Rework hours this month vs total production hours

2. **Log inspection** (`/ops qc log`):
   - Prompt: date, wo_id, gate, result (PASS/FAIL)
   - If FAIL: ncr_category (Dimensional/Electrical/Assembly/Material/Cosmetic), description, root_cause, corrective_action, rework_hours
   - Auto-generate NCR-ID: `NCR-YYYY-NNN`
   - Append to sheet `QC Log`
   - Show FPY impact: "Product FPY: was X%, now Y%"

3. **NCR review** (`/ops qc ncr`):
   - List open NCRs (no corrective_action)
   - Pattern detection if ≥ 10 records
   - Suggest: "Consider design standard update for [category] at [gate]"

### CRM (`/ops crm`)

**Read** sheet `Customers` + sheet `Deals`:
- Customer list with products, relationship status
- Deal pipeline: active opportunities
- Integration with existing `bd-pulse` skill

## ERPNext Migration Rules

**Every XLSX column maps to an ERPNext field.** Naming convention:
- `wo_id` → ERPNext `name` (Work Order)
- `item_code` → ERPNext `item_code` (Item)
- `customer_id` → ERPNext `name` (Customer)
- `supplier_id` → ERPNext `name` (Supplier)

When migrating:
1. Export sheet from WX-OPS.xlsx → CSV (openpyxl or Excel "Save As")
2. ERPNext > Data Import > upload CSV per sheet
3. Link fields (customer_id, supplier_id) resolve automatically by name match
4. Or use `@casys/mcp-erpnext` MCP server to sync directly via API (Phase 1+)

## Integration with IPARAG

| Direction | Data | How |
|:---------:|------|-----|
| HELIX Phase 4 → Production | BOM → work order + material list | `/helix-detail-finalize` outputs BOM → append to `BOM Master` sheet |
| Production → Status.md | Unit counts, completion dates | `/ops production` → update project Status.md |
| Inventory → FORGE Cost | Actual material costs | `/ops inventory` costs → `/forge-cost` validation |
| CRM → bd-pulse | Customer touchpoints | Shared data in `Customers` sheet |
| Finance → bridge-dashboard | Revenue, margin | `/ops finance` → dashboard metrics |

## STRUCTURED GUARDRAILS (Research-validated — Springer 2025)

**MANDATORY for all AI outputs in /ops:**

1. **NEVER infer values not in XLSX** — always cite source sheet + row. If data missing → say "KHÔNG CÓ DATA" instead of guessing.
2. **NEVER generate BOM/routing/cost from general knowledge** — only from sheet `BOM Master`, `_routing.md`, sheet `Stock Ledger`.
3. **All calculations must be traceable**: show formula + input values. E.g., "demand = 5 units × 2 tấm/unit = 10 tấm (from BOM Master row 3)."
4. **Flag data gaps explicitly**: "⚠️ DATA GAP: BOM cho TARGET-DRONE không có STEEL-60x40 — có thể thiếu item."
5. **AI recommend, human decide** — mọi action (tạo WO, PO, update status) phải CEO confirm. KHÔNG auto-execute.

**Why:** Generic LLMs hallucinate manufacturing parameters khi input vague (J. Intelligent Manufacturing, 2025). XLSX = structured template = guardrail tự nhiên. Giữ guardrail = giữ data integrity.

## COMPOUND LEARNING METRICS

Khi `/ops` hoặc `/ops production` chạy, tự động tính và hiển thị (nếu có đủ data):

```
📈 COMPOUND METRICS (auto-calculated)
  Lead Time Accuracy:
    TOWED-TARGET: planned 7.5d, actual avg [X]d ([N] WOs completed) — deviation [Y]%
    VN-MGM: planned 11d, actual avg [X]d ([N] WOs completed)
  FPY Trend:
    This month: [X]% | Last month: [Y]% | Δ: [+/-Z]%
  PX Efficiency:
    WS-CKCX: avg [X]h/unit actual vs [Y]h/unit planned — [over/under] by [Z]%
  Routing Update Suggestions:
    [If deviation > 20% for ≥ 5 completed WOs → suggest update]
```

Sources: `WX-OPS.xlsx` sheets — `Work Orders` (completed WOs), `Daily Log` (actual hours), `QC Log` (FPY), `_routing.md` (planned).

## COD Classification

- Data entry (log invoice, update WO status): **Offload (O)** — AI assists
- Data review (dashboard, alerts): **Offload (O)** — AI generates
- QC gate decisions (pass/fail): **Core (C)** — CEO/QĐ judgment
- Financial decisions (approve PO >50M): **Core (C)** — CEO judgment
- Production priorities: **Core (C)** — CEO/PGĐ judgment
- Customer relationship decisions: **Core (C)** — CEO judgment
