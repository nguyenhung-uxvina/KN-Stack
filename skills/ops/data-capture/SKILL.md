Design minimal data capture pipeline per product. Stop data from evaporating.

Usage: /data-capture [product-name]

---

## Process

### Step 1: Select product

If argument given, use that product.
If not, list deployed products and ask CEO to pick one.

### Step 2: Read existing spec

Read `1_Projects/[project]/data-capture-spec.md` if exists.
If exists, show current spec and ask for updates.
If not exists, go to Step 3.

### Step 3: Data audit — 5 questions

Ask CEO sequentially:

1. **"Mỗi lần sử dụng/exercise, sản phẩm này tạo ra data gì?"**
   - Scoring data (hit/miss, accuracy, timing)
   - Sensor readings (piezo signals, GPS, IMU)
   - Session metadata (date, unit, operator, conditions)
   - Performance metrics (system uptime, error rate)

2. **"Data hiện đang lưu ở đâu?"**
   - (A) Mất — không lưu (evaporating)
   - (B) SD card / USB — manual extraction
   - (C) Local storage on device — stays on device
   - (D) Cloud / server — centralized
   - (E) Paper log — manual recording

3. **"Format data hiện tại?"**
   - Raw binary / hex
   - CSV / text log
   - Custom protocol
   - Không biết — cần reverse-engineer

4. **"Ai extract data sau mỗi exercise?"**
   - Không ai — data stays on device until overwritten
   - Operator (quân nhân) — nhưng không consistent
   - Workshop X technician — khi bảo trì
   - Automatic upload — (nếu có connectivity)

5. **"Nếu có 1 báo cáo tự động sau mỗi exercise, khách hàng cần gì nhất?"**
   - Kết quả chấm điểm (pass/fail, accuracy %)
   - So sánh với lần trước (improvement trend)
   - So sánh giữa các đơn vị (benchmarking)
   - Đề xuất huấn luyện (AI recommendation)

### Step 4: Design minimal pipeline

Based on answers, create the simplest possible pipeline:

```
LEVEL 1 (Minimum — stop evaporation):
  [data source] → [storage medium] → [extraction method] → [file format]
  Example: Piezo ADC → SD card CSV → monthly USB extract → Excel

LEVEL 2 (Useful — enable reporting):
  Level 1 + [analysis script] → [report template] → [delivery method]
  Example: CSV → Python script → PDF report → email to unit commander

LEVEL 3 (Valuable — enable analytics):
  Level 2 + [database] → [dashboard] → [trend analysis] → [recommendations]
  Example: CSV → SQLite → Grafana dashboard → quarterly performance review
```

Recommend starting at Level 1. Don't over-engineer.

### Step 5: Create spec

Write to `1_Projects/[project]/data-capture-spec.md`:

```markdown
# Data Capture Spec — [Product Name]

> Minimal pipeline to stop data evaporation.
> Created by /data-capture. Review quarterly.

---

## Data Generated Per Exercise
| Data Type | Source | Rate | Current Storage | Status |
|-----------|--------|------|----------------|--------|
| [type] | [sensor/system] | [per exercise] | [where/lost] | 🔴/🟡/🟢 |

## Current State
- Storage: [answer from Q2]
- Format: [answer from Q3]
- Extraction: [answer from Q4]
- Customer need: [answer from Q5]

## Designed Pipeline (Level [1/2/3])

### Data Flow
[source] → [storage] → [extraction] → [format] → [analysis] → [output]

### Implementation
| Step | What | How | Who | Deadline |
|------|------|-----|-----|----------|
| 1 | [first step] | [method] | [owner] | [date] |
| 2 | | | | |

### Hardware/Software Needed
- [list]

### Cost Estimate
- [amount]

## Revenue Unlock
- Current: [hardware only price]
- With data pipeline: [+ service/analytics price]
- Delta: [additional revenue per unit per year]
```

### Step 6: Output

```
## Data Capture — [product] — [today]

### Current: [data status — evaporating/partial/captured]

### Designed Pipeline: Level [N]
[source] → [storage] → [extraction] → [output]

### Implementation: [N] steps, first step by [date]

### Revenue Unlock: +[X] VND/unit/year (analytics on top of hardware)

### H Layer Impact
Products with data pipeline: [N/total]
```
