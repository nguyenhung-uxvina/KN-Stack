---
name: ach-recurse
description: >-
  Track each Workshop X product's ACH (AI-Compound Hardware) recursion layer
  from L0 (hardware only) through L4 (platform integration), estimates revenue
  unlock per layer transition, and forces 1 layer-up commitment per quarter. Use
  quarterly to compound product value without new hardware development. Triggers
  on: "ach-recurse", "ACH layer", "product layer", "recursion", "layer
  transition", "analytics subscription", "data pipeline product", "compound
  hardware".
---

Track ACH recursion layers per product. Force 1 layer transition commitment per quarter.

Usage: /ach-recurse

---

## Process

### Step 1: Read recursion tracker

Read `_meta/ach-recursion.md`. If not exists, go to Step 2 (first run).

If exists, show current layer status per product.

### Step 2: First run — map current layers

For each deployed product, classify its ACH layer:

```
Layer 0: Hardware only (no AI/automation)
Layer 1: Hardware + auto-scoring/automation (AI replaces manual labor)
Layer 2: Layer 1 + data analytics (AI generates insights from data)
Layer 3: Layer 2 + training recommendations (AI advises human decisions)
Layer 4: Layer 3 + platform integration (SCOREBOARD/AICC ecosystem)
```

Ask CEO to confirm layer per product.

Create `_meta/ach-recursion.md`:

```markdown
# ACH Recursion Tracker — Workshop X

> Track each product's ACH layer. Each layer up = higher price, margin, moat.
> Law 2: Apply ACH to your own ACH products.
> Updated by /ach-recurse.

---

## Product Layers

### BB-01 (Bia bắn thông minh)
- **Current layer:** 1 — Hardware + auto-scoring
- **Next layer:** 2 — Training analytics (shot pattern analysis, unit performance reports)
- **Blocker:** Data pipeline not built (H layer = 2.5)
- **Investment:** Data capture spec + report template + storage
- **Revenue impact:** Recurring analytics subscription on top of hardware sale
- **Timeline:** TBD

### [Product 2]
...

---

## Layer Summary
| Product | L0 | L1 | L2 | L3 | L4 | Revenue/Layer |
|---------|:--:|:--:|:--:|:--:|:--:|:-------------:|
| BB-01 | ✅ | ✅ | ⬜ | ⬜ | ⬜ | Hardware + Scoring |
| [next] | | | | | | |

## Revenue Model (ACH Recursion)
```
L0: One-time hardware sale ($X)
L1: Hardware + service contract ($X + recurring)
L2: L1 + analytics subscription ($X + $Y/month)
L3: L2 + AI advisory retainer ($X + $Y + $Z/month)
L4: Platform fee (% of training budget)
```

## History
- [date] Created recursion tracker.
```

### Step 3: Quarterly review

For each product at Layer N:
1. **"Ready to move to Layer N+1?"**
2. If yes → define: what's needed (tech, data, packaging), timeline, investment
3. If no → what's blocking?
4. CEO commits 1 product to level up this quarter

### Step 4: Revenue projection

For products moving to next layer, estimate:
- Current revenue per unit (at current layer)
- Projected revenue per unit (at next layer)
- Delta = revenue unlock per layer transition
- Priority = highest delta × easiest transition

### Step 5: Force commitment

Ask: **"Sản phẩm nào sẽ lên layer tiếp theo quarter này?"**

Log commitment with:
- Product name
- Current → target layer
- Key deliverable (e.g., "data capture spec for BB-01")
- Deadline
- Owner (CEO or delegate)

### Step 6: Output

```
## ACH Recursion — [today]

### Layer Status
| Product | Current | Next | Blocker | Commitment |
|---------|:-------:|:----:|---------|------------|
| [name] | L[N] | L[N+1] | [what] | [action by date] |

### Quarterly Commitment
🎯 [product] → Layer [N+1] by [date]
   Deliverable: [what]

### Revenue Unlock Estimate
Moving [product] from L[N] → L[N+1] = +[X] VND/unit/month

### Portfolio ACH Depth
Average layer: [X.X] / 4.0
Products at L0: [N] | L1: [N] | L2: [N] | L3: [N] | L4: [N]
```
