---
name: tana-session
description: Session exit capture — ghi key decisions, learnings, và physical progress của session vào Tana daily note. Chạy sau /session-exit hoặc standalone khi kết thúc làm việc. Requires mcp__tana-local.
---

# Tana Session — Session Exit Capture

Đóng session bằng cách log 3 thứ vào Tana daily note: **quyết định**, **learning**, **physical progress**. Tana là long-term memory; Claude memory là short-term. Skill này đảm bảo không mất gì sau session.

## When to Use

- Cuối mỗi session làm việc (sau /session-exit hoặc thay thế)
- Khi CEO nói "kết thúc hôm nay", "wrap up", "tana session"
- Khi đạt milestone hoặc gate (G1/G2/G3) và muốn log

## Workflow

### Step 1: Lấy daily note

```
list_workspaces → workspaceId
get_or_create_calendar_node(workspaceId, date=today) → dailyNodeId
```

### Step 2: Hỏi CEO 3 câu reflective

**Câu 1 — Physical Progress:**
> "Hôm nay có gì di chuyển product tới physical milestone?"

Gợi ý nếu không rõ:
- Có đo/test/lắp ráp gì không?
- Có file CAD/BOM/drawing nào được approve không?
- Có supplier confirm gì không?

→ Nếu "không có gì" → ghi nhận, tăng zero-counter trong output.

**Câu 2 — Key Decisions:**
> "Quyết định nào được đưa ra hôm nay? (kể cả quyết định không làm gì)"

→ Ghi ít nhất 1 quyết định. Không có quyết định = session chưa complete.

**Câu 3 — Learning:**
> "Learning nào đáng giữ lại? (format: [topic] — [insight] → [action])"

→ Gợi ý nếu CEO stuck: "Có gì surprised không? Có assumption nào sai không?"

### Step 3: Import vào Tana daily note

Dùng `import_tana_paste` với nodeId = dailyNodeId:

```
%%tana%%
- Session Log #session-log
  - Physical Progress:: <câu trả lời hoặc "None — streak: N">
  - Key Decisions::
    - <quyết định 1>
    - <quyết định 2 nếu có>
  - Learnings::
    - <topic> — <insight> → <action>
  - Projects Active:: <list project IDs đang active>
  - Next Physical Action:: <hành động vật lý tiếp theo cụ thể>
```

### Step 4: Kiểm tra analyst trap

Đếm số session gần đây có Physical Progress = "None":

```
search_nodes(query="Physical Progress:: None", tag="session-log") → count recent zeros
```

Nếu ≥ 3 sessions liên tiếp không có physical progress:

```
🔴 ANALYST TRAP ALERT — 3+ sessions không có physical progress!
Recommend: /analyst-trap để diagnostic đầy đủ.
Next action: schedule ít nhất 1 physical task trong 48h.
```

### Step 5: Kiểm tra Galaxy candidates

Scan learnings vừa nhập:
- Nếu learning nào answers ≥1 Galaxy question (thay đổi thiết kế / thay đổi chiến lược / cảnh báo trap) → gợi ý:

```
💡 Learning này có thể là Galaxy candidate:
"<learning text>"
→ Chạy /tana-hoa để atomize thành permanent note?
```

### Step 6: Output wrap-up

```
## Session Captured — {{today}}

### Physical Progress
<câu trả lời hoặc "None — consecutive zeros: N/3">

### Decisions Logged
- <list>

### Learnings Logged  
- <list>

### Next Physical Action
<hành động cụ thể>

✅ Saved to Tana daily note
<Galaxy candidates nếu có>
```

## Quality Gates

| Check | Yêu cầu |
|-------|---------|
| Physical status | Bắt buộc — "None" là hợp lệ nhưng phải ghi rõ |
| ≥1 decision | Session không có quyết định → hỏi lại |
| ≥1 learning | Nếu thực sự không có → ghi "N/A — exploratory session" |
| Next physical action | Cụ thể, có thể làm được ngay |

## Relationship với /session-exit

Skill này **thay thế hoặc bổ sung** cho `/session-exit`:

| `/session-exit` | `/tana-session` |
|----------------|----------------|
| Update progress.md + CLAUDE.md | Capture vào Tana daily note |
| Local file-based | Tana workspace (long-term) |
| Check CLAUDE.md drift | Detect Galaxy candidates |

Nếu dùng cả hai: chạy `/session-exit` trước, `/tana-session` sau.

## COD Classification

- Skill này: **Offload (O)** — AI format + import
- Nội dung decisions/learnings: **Core (C)** — CEO cung cấp
- Quyết định có Galaxy-worthy không: **Core (C)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId |
| `get_or_create_calendar_node` | Tạo/lấy daily note của hôm nay |
| `import_tana_paste` | Ghi session log vào daily note |
| `search_nodes` | Kiểm tra analyst trap streak |
