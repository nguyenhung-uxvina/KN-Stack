---
name: tana-ich
description: THỊNH bước Ích — xử lý Galaxy candidates trong Tana Inbox, tìm connections, và chuẩn bị handoff cho /galaxy-note. Đảm bảo mỗi concept mới có ≥2 wikilinks trước khi atomize vào Obsidian. Requires mcp__tana-local.
---

# Tana Ich — Connect Galaxy Candidates

Bước **I (Ích)** trong THỊNH workflow. Mục tiêu: không có Galaxy note nào được tạo ra mà không có ít nhất 2 connections — ích lợi chỉ đến khi nodes kết nối với nhau.

## When to Use

- Sau khi tana-thu đã capture items có `PARA-dest:: 5_Galaxy`
- CEO nói "tìm kết nối cho note này", "ích bước", "connect galaxy"
- Trước khi chạy /galaxy-note để đảm bảo context đầy đủ
- Khi có batch Galaxy candidates cần xử lý

## Workflow

### Step 1: Lấy Galaxy candidates từ Inbox

```
list_workspaces → workspaceId
search_nodes(query="PARA-dest:: 5_Galaxy") → candidates
```

Nếu không có kết quả, thử:
```
search_nodes(query="galaxy-candidate") → candidates
```

Hiển thị danh sách:
```
## Galaxy Candidates cần xử lý: N items

1. "<Title>" — <Date>
2. "<Title>" — <Date>
...

Xử lý lần lượt từng item.
```

Nếu Inbox không có candidates → báo: "Không có Galaxy candidates. Dùng /tana-thu để capture insight mới."

### Step 2: Xử lý từng candidate

Với mỗi candidate:

#### 2a. Đọc nội dung
```
read_node(nodeId) → content
```

#### 2b. Extract atomic concept

Đặt câu hỏi kiểm tra atomicity:
- Concept có thể diễn đạt trong 1–3 câu không?
- Nếu có "và" nối 2 ý độc lập → gợi ý tách 2 notes

Kiểm tra Galaxy-worthy (≥1 phải đúng):
1. Có thay đổi cách thiết kế sản phẩm không?
2. Có thay đổi quyết định chiến lược không?
3. Có cảnh báo về trap cụ thể không?

Nếu không pass → gợi ý route sang `3_Resources/` thay vì Galaxy.

#### 2c. Tìm connections trong Tana

Search các nodes liên quan:
```
search_nodes(query="<keyword từ concept>") → related_nodes
search_nodes(query="<keyword 2>") → more_related
```

Từ kết quả, đề xuất 2–3 connections:

```
Concept: "<atomic statement>"

Connections đề xuất:
→ [[<Note/Node A>]] — <lý do liên kết>
→ [[<Note/Node B>]] — <lý do liên kết>
→ [[<Note/Node C>]] — (cross-cluster, nếu tìm được)

Galaxy cluster gợi ý: <A–H> — <lý do>
```

#### 2d. Present handoff cho /galaxy-note

Output structured prompt sẵn sàng paste vào /galaxy-note:

```
---GALAXY-NOTE HANDOFF---
Title gợi ý: <Vietnamese title with diacritics>
Source: Tana Inbox — <Date>
Atomic concept: <1-3 câu>
Cluster: <A–H>
Links:
  - [[<Note A>]] — <annotation>
  - [[<Note B>]] — <annotation>
Tags: <#acq / #sys / #pahl / #defense / #product / #ceo / #meta / #three-laws / #warning>
---END HANDOFF---

→ Chạy /galaxy-note với handoff này để tạo permanent note trong Obsidian.
```

#### 2e. Hỏi CEO

```
Tạo Galaxy note này? [y / n / edit / later]
```

- `y` → output handoff, CEO paste vào /galaxy-note
- `n` → route sang Resources hoặc trash
- `edit` → CEO chỉnh concept/links trước
- `later` → giữ nguyên trong Inbox với tag `#galaxy-pending`

### Step 3: Update Tana node

Sau khi CEO quyết định:

**Nếu `y`:** Update node với thông tin đã chuẩn bị:
```
set_field_content(nodeId, "Status", "→ /galaxy-note pending")
set_field_content(nodeId, "Connections-draft", "[[A]], [[B]]")
```

**Nếu `n`:** Update destination:
```
set_field_content(nodeId, "PARA-dest", "3_Resources/")
```

**Nếu `later`:** Giữ nguyên — CEO tự xử lý sau.

### Step 4: Summary

```
## Tana Ich — Summary

Đã xử lý: N candidates
→ Ready for /galaxy-note: N
→ Routed to Resources: N
→ Deferred: N

Next: Chạy /galaxy-note với từng handoff để hoàn thành bước Hóa + Ích.
```

## Quality Gates

| Check | Yêu cầu |
|-------|---------|
| Atomic | 1 concept per note — split nếu có "và" |
| Galaxy-worthy | Pass ≥1 trong 3 câu hỏi |
| Connections | ≥2 links đề xuất trước khi handoff |
| Cross-cluster | ≥1 link từ cluster khác |
| No auto-create | CEO approve trước khi handoff sang /galaxy-note |

## Relationship với /galaxy-note

`tana-ich` = **preparation layer** (Tana)
`/galaxy-note` = **creation layer** (Obsidian)

Flow: `tana-thu` → `tana-ich` → `/galaxy-note` → `5_Galaxy/<file>.md`

## COD Classification

- Step 1–2 (scan + extract): **Offload (O)**
- Quyết định Galaxy-worthy: **Core (C)**
- Approve connections: **Core (C)**
- Update Tana fields: **Offload (O)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId |
| `search_nodes` | Tìm candidates + related nodes |
| `read_node` | Đọc content candidate |
| `set_field_content` | Update status sau CEO decide |
