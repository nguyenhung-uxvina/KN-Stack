---
name: tana-cod
description: COD classification engine cho Tana Inbox — scan items thiếu COD label, guide CEO classify từng item C/O/D, batch update. Có thể chạy standalone hoặc được gọi từ tana-weekly. Requires mcp__tana-local.
---

# Tana COD — Classification Engine

Đảm bảo mọi item trong Inbox đều có COD label trước khi xử lý. Không có COD = không biết ai làm = item đóng băng trong Inbox mãi.

## When to Use

- CEO nói "classify inbox", "cod triage", "ai làm cái này"
- Khi Inbox tích lũy nhiều items không rõ owner
- Được gọi tự động từ `/tana-weekly` Step H
- Weekly habit trước khi bắt đầu ngày làm việc

## COD Framework

| Layer | Label | Định nghĩa | Dấu hiệu nhận biết |
|-------|-------|-----------|-------------------|
| **C** | Core | Cần phán đoán chiến lược của CEO | "Có nên...", "Chọn giữa...", design decisions, gate approvals |
| **O** | Offload | AI xử lý được dưới supervision | Draft, search, format, calculate, compile |
| **D** | Default | Skip hoặc automate hoàn toàn | Notifications, reminders, administrative cleanup |

**Constraint:** Tổng C < 60% để tránh Opus Trap.

## Workflow

### Step 1: Scan Inbox — items thiếu COD

```
list_workspaces → workspaceId
search_nodes(query="inbox") → all_inbox_items
```

Filter items không có `COD::` field trong content:
```
read_node(nodeId) → check if "COD::" present
```

Hoặc scan nhanh:
```
search_nodes(query="COD:: C") → has_cod_c
search_nodes(query="COD:: O") → has_cod_o
search_nodes(query="COD:: D") → has_cod_d
```

Output:

```
## Inbox COD Scan

Đã có COD: N items (C: N, O: N, D: N)
Thiếu COD:  N items → cần classify

Bắt đầu classify?
```

### Step 2: Classify từng item

Với mỗi item thiếu COD:

```
read_node(nodeId) → title, why, para-dest
```

Present cho CEO:

```
Item: "<Title>"
Why: <why context>
PARA-dest: <destination>

Gợi ý: <C / O / D> — <lý do ngắn>

COD? [C / O / D / skip]
```

**Logic gợi ý tự động:**

| Điều kiện | Gợi ý COD |
|-----------|----------|
| Title có "quyết định", "chọn", "approve", "thiết kế" | **C** |
| Title có "nghiên cứu", "tìm", "draft", "tổng hợp", "format" | **O** |
| PARA-dest = `5_Galaxy` | **C** (Galaxy = CEO judgment) |
| PARA-dest = `1_Projects/` + action verb | **O** |
| Item không rõ tại sao quan trọng | **D** (hoặc hỏi lại why) |
| Notification / FYI / reminder | **D** |

CEO có thể override gợi ý bất kỳ lúc nào.

### Step 3: Batch update

Sau khi CEO classify xong tất cả, update Tana:

Với mỗi item đã classify:
```
set_field_content(nodeId, "COD", "<C/O/D>")
```

### Step 4: COD Distribution Report

```
## COD Classification Complete — {{today}}

Đã classify: N items

Distribution:
  C (Core):    N items (N%) <bar>
  O (Offload): N items (N%) <bar>
  D (Default): N items (N%) <bar>

```

**Nếu C > 60%:**
```
⚠️ Opus Trap Alert: C = N% (>60%)
CEO đang giữ quá nhiều. Xem xét lại:
- Có item nào C thực ra có thể O không?
- Có item D nào cần delete thay vì giữ?
Recommend: /analyst-trap để diagnostic đầy đủ.
```

**Nếu D > 30%:**
```
💡 D = N% — nhiều items không cần làm.
Recommend: trash ngay thay vì để chờ.
```

### Step 5: Priority queue cho C items

Sau classification, list C items theo thứ tự xử lý:

```
## C Items — Priority Queue

High (có deadline / blocking):
  1. "<Title>" — <why>

Normal:
  2. "<Title>" — <why>
  3. "<Title>" — <why>

Low (no urgency):
  4. "<Title>" — <why>

→ Tackle item #1 trước. Còn lại → schedule hoặc route sang /sprint.
```

## Partial Run

- Chỉ scan không classify: `/tana-cod scan`
- Chỉ classify C items: `/tana-cod core-only`
- Chỉ report distribution: `/tana-cod report`

## Integration với tana-weekly

`tana-weekly` gọi `tana-cod` tự động trong Step H (Hóa) sau khi route items. Flow:

```
tana-weekly Step H:
  → route item (PARA-dest)
  → tana-cod: assign COD cho item đó
  → tiếp tục item tiếp theo
```

Hoặc: chạy `tana-cod` standalone trước `tana-weekly` để clean Inbox trước.

## COD Classification

- Skill này: **Offload (O)** — AI scan + gợi ý
- Quyết định từng item C/O/D: **Core (C)**
- Batch update Tana fields: **Offload (O)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId → Inbox ID |
| `search_nodes` | Scan inbox, filter by COD presence |
| `read_node` | Đọc title + why + para-dest của từng item |
| `set_field_content` | Update COD field sau CEO classify |
