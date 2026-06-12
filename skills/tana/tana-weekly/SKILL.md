---
name: tana-weekly
description: Orchestrator THỊNH weekly review — Inbox Zero + connect Galaxy notes + harvest insights. Chạy cuối tuần hoặc khi Inbox tích lũy. Pipeline 5 bước: Thu-Hóa-Ích-Nhớ-Hành. Requires mcp__tana-local.
---

# Tana Weekly — THỊNH Review Orchestrator

Weekly ritual đảm bảo Inbox về zero, Galaxy tiếp tục compound, và CEO có insights sẵn cho tuần tới. Tổng thời gian mục tiêu: **30–45 phút**.

## When to Use

- Cuối tuần (thường Chủ Nhật tối hoặc Thứ Hai sáng)
- CEO nói "weekly review", "tana weekly", "inbox zero"
- Khi Inbox > 10 items tích lũy
- Trước gate review (G1/G2/G3) để có context đầy đủ

## Pipeline

```
T → scan Inbox items
H → atomize + route each item  
I → find orphan Galaxy notes → suggest links
N → check CLAUDE.md drift vs Tana state
H → harvest top insights → brief CEO cho tuần tới
```

---

## Step T — Thu: Scan Inbox (5 phút)

```
list_workspaces → workspaceId
search_nodes(tag="#inbox") → inbox_items
```

Output danh sách inbox:

```
## Inbox hiện tại: N items

| # | Title | Date | COD | PARA-dest |
|---|-------|------|-----|-----------|
| 1 | ...   | ...  | ... | ...       |
...

Hành động: xử lý từng item theo thứ tự (oldest first).
```

Nếu Inbox = 0: chuyển thẳng sang Step I.

---

## Step H — Hóa: Atomize + Route (15 phút)

Xử lý từng inbox item. Với mỗi item:

### H.1: Đọc nội dung

```
read_node(nodeId) → content
```

### H.2: Phân loại và đề xuất action

| Loại item | Đề xuất action |
|-----------|---------------|
| Task rõ deadline | → `1_Projects/<project>` |
| Task không deadline | → `2_Areas/<area>` |
| Tài liệu tham khảo | → `3_Resources/` |
| `#galaxy-candidate` hoặc insight sâu | → atomize thành Galaxy note (chạy /galaxy-note) |
| Không rõ | → giữ Inbox, hỏi CEO |
| Outdated / done | → trash |

### H.2a: Nếu là Galaxy candidate

Kiểm tra 3 câu hỏi Galaxy-worthy:
1. Có thay đổi cách thiết kế sản phẩm không?
2. Có thay đổi quyết định chiến lược không?
3. Có cảnh báo về trap cụ thể không?

Nếu YES ≥1 → present atomic concept draft, đề xuất chạy `/galaxy-note`.
Nếu NO → route sang Resources hoặc trash.

### H.3: Present cho CEO từng item

```
Item #N: "<Title>"
Nội dung: <summary ngắn>
Đề xuất: <action>
Confirm? [y/n/edit/trash]
```

**KHÔNG tự move** — chờ CEO confirm từng item.

### H.4: Update status sau khi CEO confirm

Nếu CEO confirm route → `set_field_content(nodeId, "PARA-dest", confirmed_dest)`
Nếu CEO trash → `trash_node(nodeId)`
Nếu là task đã done → `check_node(nodeId)`

---

## Step I — Ích: Connect Galaxy Notes (10 phút)

### I.1: Tìm orphan notes

```
search_nodes(tag="#type/permanent-note") → all_galaxy_notes
```

Với mỗi note, đọc và kiểm tra số wikilinks trong `links:` frontmatter.

Filter: notes có < 2 wikilinks → **orphan candidates**.

### I.2: Đề xuất connections

Với mỗi orphan:
1. Đọc core concept
2. Search notes khác có overlap topic
3. Đề xuất 1–2 wikilinks mới với annotation

```
Orphan note: "<Title>"
Concept: <1-sentence>

Đề xuất link:
→ [[<Note A>]] — <lý do liên kết>
→ [[<Note B>]] — <lý do liên kết>

Add these links? [y/n/edit]
```

### I.3: Update nếu CEO approve

CEO approve → chạy `/galaxy-note` hoặc user tự edit trong Obsidian.
Không tự edit Galaxy notes qua Tana MCP.

---

## Step N — Nhớ: CLAUDE.md Drift Check (5 phút)

So sánh Tana state với CLAUDE.md:

### N.1: Project count check

```
search_nodes(tag="#type/project", field="status=active") → active_projects
```

So với danh sách projects trong CLAUDE.md. Flag nếu:
- Project trong Tana không có trong CLAUDE.md → có thể thiếu
- Project trong CLAUDE.md nhưng không còn active trong Tana → outdated

### N.2: Galaxy count check

```
search_nodes(tag="#type/permanent-note") → count
```

So với số trong CLAUDE.md (`5_Galaxy: N notes`). Nếu lệch → gợi ý update.

### N.3: Active areas check

```
search_nodes(tag="#type/area", field="status=active") → active_areas
```

Flag bất kỳ area nào xuất hiện trong Tana nhưng không có trong CLAUDE.md 2_Areas.

Output:

```
## CLAUDE.md Drift Check

Projects: Tana=N, CLAUDE.md=M → <match / cần update>
Galaxy: Tana=N, CLAUDE.md=M → <match / cần update>
Areas: <list differences>

Đề xuất update: <specific edits nếu có>
```

---

## Step H — Hành: Harvest Insights (5 phút)

### H.1: Lấy recent Galaxy notes

```
search_nodes(tag="#type/permanent-note", sort=created_desc, limit=10) → recent_notes
```

### H.2: Filter theo relevance

Đọc content, filter notes liên quan tới:
- Projects đang active (từ Step N)
- Decisions đang pending (từ Tana search)
- Tags: `#warning`, `#three-laws`, `#ceo`

### H.3: Brief CEO

```
## Galaxy Insights cho tuần tới

Top 3 insights relevant tới work hiện tại:

1. [[<Note A>]]
   Insight: <1-2 sentences>
   Apply to: <project/decision>

2. [[<Note B>]]
   Insight: <1-2 sentences>
   Apply to: <project/decision>

3. [[<Note C>]]
   Insight: <1-2 sentences>
   Apply to: <project/decision>
```

---

## Final Output

```
## THỊNH Weekly Review — {{today}}

### Thu
✅ Inbox processed: N items → N routed, N trashed, N deferred

### Hóa
✅ Galaxy candidates: N → reviewed
✅ Tasks routed: N items

### Ích
✅ Orphan notes fixed: N
⚠️ Still orphan: N (need attention)

### Nhớ
✅ CLAUDE.md drift: <none / list updates>

### Hành
💡 Top insight này tuần: "<Note title>"

---
Inbox Zero: <✅ YES / ⚠️ N items remain>
Time: ~{{elapsed}} min
Next review: {{next_sunday}}
```

## Quality Gates

| Gate | Yêu cầu |
|------|---------|
| Inbox Zero | Mọi item phải có decision (route/trash/defer) |
| No auto-move | CEO confirm từng item trước khi route |
| Galaxy connections | Mọi orphan note phải được addressed |
| CLAUDE.md sync | Số Galaxy notes và projects phải khớp |

## Partial Run

Nếu không có đủ thời gian, chạy partial:
- Chỉ Step T + H: `/tana-weekly inbox` 
- Chỉ Step I: `/tana-weekly galaxy`
- Chỉ Step H (Hành): `/tana-weekly harvest`

## COD Classification

- Step T (scan): **Offload (O)** — AI đọc và list
- Step H (route decision): **Core (C)** — CEO decide từng item
- Step I (suggest links): **Offload (O)** — AI đề xuất, CEO approve
- Step N (drift check): **Offload (O)** — AI compare, CEO confirm update
- Step H (harvest): **Offload (O)** — AI surface, CEO interpret

## Tana MCP Tools Used

| Tool | Step | Khi nào |
|------|------|---------|
| `list_workspaces` | T | Lấy workspaceId |
| `search_nodes` | T, I, N, H | Tìm inbox, galaxy, projects |
| `read_node` | H, I | Đọc content từng item |
| `set_field_content` | H | Update PARA-dest sau confirm |
| `check_node` | H | Mark done task |
| `trash_node` | H | Xóa item đã xử lý |
| `import_tana_paste` | H | Tạo Galaxy note mới nếu cần |
