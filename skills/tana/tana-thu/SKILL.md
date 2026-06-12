---
name: tana-thu
description: THỊNH bước Thu — capture ý tưởng/insight/task mới vào Tana Inbox với đủ "why" context và COD classification. Dùng khi CEO muốn capture nhanh không mất ý tưởng. Requires mcp__tana-local.
---

# Tana Thu — Capture to Inbox

Bước **T (Thu)** trong THỊNH workflow. Mục tiêu: mọi item mới đều vào Inbox với đủ context để xử lý sau — không phải ghi cho có, mà ghi có *tại sao*.

## When to Use

- CEO nói "capture cái này", "ghi lại", "thu vào inbox", "nhớ cái này"
- Sau meeting, sau physical test, sau đọc tài liệu, khi có insight bất chợt
- Khi kết thúc một task và muốn log kết quả/quyết định

## Workflow

### Step 1: Lấy workspace context

```
list_workspaces → lấy workspaceId
```

Inbox ID: `{workspaceId}_CAPTURE_INBOX`

### Step 2: Hỏi CEO 3 câu — tuần tự, chấp nhận câu trả lời ngắn

**Câu 1:** "Capture cái gì?" → Title của item

**Câu 2:** "Tại sao capture lúc này?"
→ Why context là bắt buộc. Nếu CEO không có why, nhắc nhở:
> "Không có 'why' thì Inbox = graveyard. Dù ngắn cũng được — tại sao cái này quan trọng?"

**Câu 3:** "COD: Core / Offload / Default?"
→ Gợi ý nếu CEO chưa rõ:

| Label | Nghĩa | Ví dụ |
|-------|-------|-------|
| **C** | Cần phán đoán CEO | Quyết định thiết kế, inbox triage |
| **O** | AI xử lý được | Draft note, search, format |
| **D** | Skip / automate | Notification, cleanup |

### Step 3: Đề xuất PARA destination

Phân tích title + why, gợi ý destination:

| Nếu item là... | Gợi ý destination |
|----------------|-------------------|
| Task có deadline | `1_Projects/<project-name>` |
| Ongoing responsibility | `2_Areas/<area>` |
| Tài liệu tham khảo | `3_Resources/` |
| Insight cần atomize | `5_Galaxy` (→ chạy /tana-hoa sau) |
| Chưa rõ | Giữ ở Inbox |

**KHÔNG tự move** — chỉ đề xuất.

### Step 4: Import vào Tana Inbox

Dùng `import_tana_paste` với cú pháp Tana Paste:

**Nếu là note/insight:**
```
%%tana%%
- <Title> #inbox
  - Why:: <why context>
  - COD:: <C / O / D>
  - PARA-dest:: <destination gợi ý>
  - Date:: <YYYY-MM-DD>
```

**Nếu là task:**
```
%%tana%%
- [ ] <Title> #inbox
  - Why:: <why context>
  - COD:: <C / O / D>
  - PARA-dest:: <destination gợi ý>
  - Date:: <YYYY-MM-DD>
```

**Nếu là Galaxy candidate:**
```
%%tana%%
- <Title> #inbox #galaxy-candidate
  - Why:: <why context>
  - COD:: C
  - PARA-dest:: 5_Galaxy
  - Concept-draft:: <1-sentence atomic concept>
  - Date:: <YYYY-MM-DD>
```

### Step 5: Confirm

Output ngắn gọn:

```
✅ Captured: "<Title>"
   Inbox → gợi ý: <PARA-dest>
   COD: <class>
   
Thêm item nào không?
```

## Quality Gates

Trước khi import, kiểm tra:

| Check | Yêu cầu |
|-------|---------|
| Why present | Bắt buộc — không có why thì dừng lại hỏi |
| COD assigned | Một trong C / O / D |
| Title clear | Đủ để hiểu sau 1 tuần không có context |
| No auto-move | Chỉ gợi ý PARA-dest, không tự chuyển |

## COD Classification

- Skill này: **Offload (O)** — AI format + import, CEO cung cấp content
- Quyết định PARA destination: **Core (C)**
- Quyết định có Galaxy-worthy không: **Core (C)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId → Inbox ID |
| `import_tana_paste` | Tạo node trong Inbox |
| `get_or_create_calendar_node` | Nếu CEO muốn capture vào daily note thay vì Inbox |
