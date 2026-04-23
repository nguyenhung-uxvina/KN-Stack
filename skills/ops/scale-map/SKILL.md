Track horizontal expansion: Product × Military Unit matrix. Force 1 outreach per week.

Usage: /scale-map

---

## Process

### Step 1: Read expansion map

Read `_meta/scale-map.md`. If not exists, go to Step 2 (first run).

If exists, show current matrix and pipeline status.

### Step 2: First run — build product × unit matrix

Ask CEO:

1. **"Sản phẩm nào đang deployed? Ở đơn vị nào?"**
   Build matrix with known deployments.

2. **"Sản phẩm nào có thể bán cho nhiều đơn vị hơn?"**
   Identify replicable products (low customization, proven, standardized).

3. **"Đơn vị nào là target tiếp theo cho mỗi sản phẩm?"**
   CEO identifies 3-5 target units per replicable product.

Create `_meta/scale-map.md`:

```markdown
# Scale Map — Workshop X Horizontal Expansion

> Product × Military Unit matrix. Track from UNTOUCHED → OUTREACH → PROPOSAL → ORDER → DEPLOYED.
> Updated by /scale-map. Goal: expand deployed products to more units.

---

## Expansion Matrix

### [Product 1]
| Military Unit | Branch | Status | Contact | Last Touch | Next Action |
|--------------|--------|--------|---------|-----------|-------------|
| [unit A] | [Army/Navy/AF/Border] | DEPLOYED | [name] | [date] | Maintenance |
| [unit B] | | UNTOUCHED | — | — | Identify contact |
| [unit C] | | OUTREACH | [name] | [date] | Send proposal |

### [Product 2]
...

---

## Pipeline Summary
| Stage | Count |
|-------|:-----:|
| DEPLOYED | [N] |
| ORDER | [N] |
| PROPOSAL | [N] |
| OUTREACH | [N] |
| UNTOUCHED | [N] |

## History
- [date] Created scale map.
```

### Step 3: Weekly update

For each product:
1. Show current matrix
2. Ask: "Có update nào? (outreach, proposal sent, response received, order?)"
3. Update status changes

### Step 4: Force outreach

After update, scan for UNTOUCHED targets:
- List top 3 highest-potential untouched targets
- Ask CEO: **"Chọn 1 target để outreach tuần này."**
- Log commitment: who, when, how (call/visit/email)

If CEO says "không" → "⚠️ Zero expansion outreach this week. Pipeline drying up."

### Step 5: Pipeline metrics

Calculate:
- **Expansion rate:** New OUTREACH/week
- **Conversion rate:** PROPOSAL → ORDER (if enough data)
- **Coverage:** DEPLOYED / (DEPLOYED + UNTOUCHED) per product
- **TAM estimate:** Total addressable units × unit price

### Step 6: Output

```
## Scale Map — [today]

### Pipeline
| Product | Deployed | Order | Proposal | Outreach | Untouched |
|---------|:--------:|:-----:|:--------:|:--------:|:---------:|
| [name] | [N] | [N] | [N] | [N] | [N] |

### This Week's Outreach Commitment
🎯 [target unit] — [product] — [action] by [date]

### Top Untouched Targets
1. [unit] — [product] — [why high potential]
2. [unit] — [product] — [why]
3. [unit] — [product] — [why]

### Coverage: [X]% of known TAM
```
