---
name: tana-hoa
description: THỊNH bước Hóa — atomize raw Inbox captures thành structured items sẵn sàng route. Tách complex items, chuẩn hóa format, phân loại PARA, flag Galaxy candidates. Khác tana-ich (connect links) — Hóa là transform raw → structured. Requires mcp__tana-local.
---

# Tana Hoa — Atomize Inbox Items

Bước **H (Hóa)** trong THỊNH workflow. Raw capture từ tana-thu thường là lumpy — nhiều ideas trong 1 node, thiếu structure, chưa actionable. Hóa = biến raw thành atomic, structured, routable.

## When to Use

- CEO nói "hóa bước", "atomize inbox", "xử lý inbox"
- Sau khi Inbox có nhiều items chưa được structured
- Khi item trong Inbox quá phức tạp hoặc quá vague để route
- Được gọi từ tana-weekly Step H

## Phân biệt Hóa vs Ích

| | Hóa | Ích |
|--|-----|-----|
| Input | Raw Inbox items | Galaxy candidates đã structured |
| Output | Structured, routable items | Items với ≥2 wikilinks sẵn sàng cho /galaxy-note |
| Tập trung | Transform format + atomize | Build connections |
| Khi nào | Sau tana-thu | Sau tana-hoa (cho Galaxy items) |

## Workflow

### Step 1: Scan Inbox items cần atomize

```
list_workspaces → workspaceId
search_nodes(query="inbox") → inbox_items
```

Filter items chưa được xử lý (không có `Status:: processed` hoặc PARA-dest đã xác nhận):

```
read_node(nodeId) → kiểm tra completeness
```

Danh sách items cần Hóa:
```
## Inbox cần atomize: N items

1. "<Title>" — captured <Date>
2. "<Title>" — captured <Date>
...
```

### Step 2: Atomize từng item

Với mỗi item, đọc content:
```
read_node(nodeId) → title, why, content
```

#### 2a. Kiểm tra atomicity

**Test 1 — Single concept test:**
> "Có thể diễn đạt item này trong 1 câu không?"

Nếu không → item cần tách.

**Test 2 — "và" test:**
> Title hoặc why có chứa "và" nối 2 independent ideas?

Nếu có → split thành 2 items.

**Test 3 — Action clarity:**
> Nếu là task: có verb + object cụ thể không? "Nghiên cứu" quá vague. "Đọc datasheet DS18B20 và extract pinout" là đủ.

#### 2b. Nếu cần tách

Present cho CEO:
```
Item: "<Title>"
→ Phát hiện 2 concepts độc lập:

  A: "<Concept A>"
  B: "<Concept B>"

Tách thành 2 items? [y / n / edit]
```

Nếu CEO approve → tạo 2 nodes mới, trash node cũ:
```
import_tana_paste(parentNodeId=inbox_id):
%%tana%%
- <Concept A title>
  - Why:: <why A>
  - COD:: <class>
  - PARA-dest:: <dest A>
  - Date:: <today>
- <Concept B title>
  - Why:: <why B>
  - COD:: <class>
  - PARA-dest:: <dest B>
  - Date:: <today>
```

Sau đó: `trash_node(original_nodeId)`

#### 2c. Nếu item vague — clarify

```
Item: "<vague title>"
Why: <empty hoặc vague>

Item này chưa đủ để route. Cần clarify:
- "Cụ thể cần làm gì với thông tin này?"
- "Done trông như thế nào?"

CEO: <clarification>
```

Update node với clarification:
```
set_field_content(nodeId, "Why", "<clarified why>")
edit_node(nodeId, "<clearer title>")
```

#### 2d. Chuẩn hóa fields

Kiểm tra và fill missing fields:

| Field | Required? | Default nếu thiếu |
|-------|-----------|-------------------|
| Why | Bắt buộc | Hỏi CEO nếu trống |
| COD | Bắt buộc | Gợi ý dựa vào content |
| PARA-dest | Bắt buộc | Gợi ý, CEO confirm |
| Date | Auto | Ngày hôm nay |

#### 2e. Flag Galaxy candidates

Kiểm tra item có Galaxy potential:
- Có thay đổi cách thiết kế không?
- Có thay đổi chiến lược không?
- Có cảnh báo trap không?

Nếu YES → mark:
```
set_field_content(nodeId, "PARA-dest", "5_Galaxy")
```

Và thêm tag flag trong title hoặc field để tana-ich xử lý sau.

### Step 3: Confirm routes với CEO

Sau khi xử lý hết batch, present summary để CEO confirm:

```
## Atomize Complete — N items

Sẵn sàng route:
1. "<Title A>" → 1_Projects/VN-TGT-F [COD: O]
2. "<Title B>" → 5_Galaxy [COD: C] ⭐ Galaxy candidate
3. "<Title C>" → 2_Areas/HELIX [COD: O]
4. "<Title D>" → TRASH (vague, no why)

Confirm routes? [y / edit specific items]
```

**KHÔNG auto-move** — CEO confirm batch trước.

> **Lưu ý kiến trúc:** Tana = capture layer. "Move" trong Tana nghĩa là cập nhật `PARA-dest` field làm routing label — không di chuyển node vật lý trong Tana. Filing thực sự xảy ra trong Obsidian (`D:\Workshop_X\`) khi CEO xử lý batch cuối tuần. Không tạo IPARAG folder structure trong Tana vì sẽ duplicate và tạo maintenance overhead.

### Step 4: Update status

Sau CEO confirm:
```
set_field_content(nodeId, "Status", "hoa-complete")
```

### Step 5: Handoff

Output handoffs cho bước tiếp theo:

```
## Hóa → Handoffs

→ /tana-ich: N Galaxy candidates sẵn sàng connect
→ /tana-project: N items route sang 1_Projects/
→ /tana-weekly: N items xử lý xong trong Step H
```

## Edge Cases

**Item là link/URL:**
→ Route `3_Resources/` với type `clipping`
→ COD: O (AI có thể summarize)

**Item là quyết định đã được đưa ra:**
→ Route `1_Projects/<project>/decisions/`
→ COD: C (CEO cần verify accuracy)

**Item là complaint / frustration:**
→ Hỏi: "Đây có phải là problem muốn solve không, hay chỉ vent?"
→ Nếu problem → restructure thành "How might we...?"
→ Nếu vent → trash

**Item duplicate với existing node:**
```
search_nodes(query="<title keywords>") → check duplicates
```
Nếu tìm được duplicate → merge hoặc trash.

## COD Classification

- Scan + atomicity check: **Offload (O)**
- Quyết định có tách hay không: **Core (C)**
- Chuẩn hóa fields (auto-fill): **Offload (O)**
- Confirm route: **Core (C)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId → Inbox |
| `search_nodes` | Scan inbox + check duplicates |
| `read_node` | Đọc content từng item |
| `edit_node` | Clarify vague title |
| `set_field_content` | Fill missing fields, update status |
| `import_tana_paste` | Tạo split items mới |
| `trash_node` | Xóa item sau split hoặc confirm trash |
