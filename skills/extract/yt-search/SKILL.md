---
name: yt-search
description: Search YouTube for videos on a topic, present results, then optionally feed selected videos into NotebookLM for deep extraction. Triggers on "tìm video", "yt-search", "youtube search", "tìm youtube về", or when user asks to find YouTube videos on a topic.
---

# YT Search — Tìm Kiếm YouTube + Feed vào NotebookLM

Tìm video trên YouTube → chọn video tốt → tạo NLM notebook → query insights → route to vault.

**PATH:** `yt-dlp` tại `C:/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts/yt-dlp.exe`
Luôn prefix bash: `export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"`

## When to Use

- Khi CEO muốn tìm video về một chủ đề cụ thể
- Khi cần market intel, competitor intel, hoặc technical references từ YouTube
- Khác với `/yt-extract-short` (extract 1 URL đã có) — skill này **tìm kiếm** trước

## Input

```
/yt-search <topic> [--count N] [--lang vi|en|any]
```

- `topic`: từ khóa tìm kiếm (tiếng Việt hoặc tiếng Anh)
- `--count N`: số kết quả (default: 8)
- `--lang`: ưu tiên ngôn ngữ (default: any)

---

## Workflow

### Step 1: Search YouTube via yt-dlp

```bash
export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"
yt-dlp "ytsearch8:<topic>" \
  --flat-playlist \
  --print "%(id)s | %(title)s | %(duration_string)s | %(view_count)s | %(upload_date)s | %(channel)s" \
  --no-download 2>/dev/null
```

Adjust count: `ytsearch5:`, `ytsearch10:`, etc. theo `--count`.

Nếu `yt-dlp` không tìm được → báo CEO, dừng.

### Step 2: Present Results Table

Hiển thị kết quả dạng bảng có thể scan nhanh:

```
## Kết Quả Tìm Kiếm: "<topic>"

| # | Title | Channel | Duration | Views | Date | URL |
|---|-------|---------|----------|-------|------|-----|
| 1 | ...   | ...     | mm:ss    | ...   | YYYY-MM-DD | youtube.com/watch?v=ID |
| 2 | ...   |
...

**Chọn video để extract sâu hơn (VD: "1,3,5" hoặc "tất cả" hoặc "bỏ qua"):**
```

**DỪNG — chờ CEO chọn video.**

### Step 3: Extract Selected Videos via NLM

Với mỗi video CEO chọn:

**3a. Tạo 1 NLM notebook chứa tất cả video được chọn:**
```
mcp__notebooklm-mcp__notebook_create(
  title="YT Search — <topic> — <YYYY-MM-DD>"
)
```

**3b. Add các video được chọn làm sources (bulk):**
```
mcp__notebooklm-mcp__source_add(
  notebook_id=...,
  source_type="url",
  urls=["https://youtube.com/watch?v=ID1", "https://youtube.com/watch?v=ID2", ...],
  wait=True,
  wait_timeout=180
)
```

Nếu source thất bại (video private/không có caption) → bỏ qua video đó, báo CEO, tiếp tục với video còn lại.

**3c. Confirm sources đã processed:**
```
mcp__notebooklm-mcp__notebook_get(notebook_id=...)
```

Báo CEO: "✅ [N] video đã add vào NLM. Đang query..."

### Step 4: Query NLM Notebook

Chạy 4 queries:

**Q1 — Overview (toàn bộ sources):**
> "Summarize the key themes and insights across all videos in this notebook. What are the main topics covered?"

**Q2 — Top insights:**
> "What are the 5 most valuable facts, techniques, or insights mentioned across these videos? Be specific with numbers and names."

**Q3 — Differences between videos:**
> "Compare the approaches or perspectives across different videos. What does each video uniquely contribute?"

**Q4 — Workshop X relevance:**
> "This content is for a Vietnamese defense technology company (Workshop X) building: military simulators, AI-powered defense systems, underwater vehicles, and target drones. Which insights from these videos are most directly applicable, and how?"

### Step 5: Present Search Report

```markdown
## YT Search Report: "<topic>"
**Date:** YYYY-MM-DD
**Videos found:** [N total] | **Selected:** [N selected]
**NLM Notebook:** [notebook_id] — "[title]"

### Videos Được Chọn
1. [Title] — [Channel] — [Duration] — [URL]
2. ...

### Themes & Overview (Q1)
[Từ NLM]

### Top Insights (Q2)
- [Insight 1 — cụ thể]
- [Insight 2]
- ...

### So Sánh Các Video (Q3)
- Video 1: [unique contribution]
- Video 2: [unique contribution]

### Áp Dụng Cho Workshop X (Q4)
- [Applicable insight 1]
- [Hoặc: "Không trực tiếp applicable"]

### Galaxy Candidates?
- [ ] Có insight đủ atomic cho Galaxy note?
- Suggested titles: [nếu có]

### NLM Notebook
✅ Created: "[title]" (ID: [id])
💡 Notebook persistent — CEO có thể query thêm sau
```

**DỪNG — chờ CEO quyết định routing.**

### Step 6: CEO Review & Route

| Decision | Action |
|----------|--------|
| Giữ NLM notebook | Không làm gì |
| Xóa NLM notebook | `mcp__notebooklm-mcp__notebook_delete(notebook_id=...)` |
| Save report to vault | Ghi vào `0_Inbox/YT_Search_<topic>_<date>.md` |
| Save to KB | Add vào `3_Resources/` subfolder phù hợp |
| Galaxy candidate | Run `/galaxy-gate` → tạo note nếu pass |
| Deep-dive 1 video | Chạy `/yt-extract-short` với URL cụ thể |
| Discard | Xóa notebook, không lưu |

---

## Quick Mode (không cần NLM)

Nếu CEO chỉ muốn danh sách video (không extract):
- Sau Step 2 → nếu CEO nói "chỉ list" hoặc "không cần extract" → dừng tại Step 2
- Không tạo NLM notebook

---

## Content Classification

| Category | Keywords | Route To |
|----------|----------|----------|
| **Technical** | Chế tạo, hardware, CNC, vật liệu | Project docs / KB Layer 2 |
| **Market Intel** | Competitor, product launch, pricing | FORGE competitive intel |
| **Training** | Tutorial, how-to, best practices | Resources / Learning |
| **Defense/Military** | Quốc phòng, vũ khí, simulation | Project-specific / Galaxy |
| **Business/AI** | AI tools, Claude API, SaaS, orchestration | BRIDGE / CEO-Self |
| **Other** | — | CEO quyết định |

---

## Error Handling

| Lỗi | Xử lý |
|-----|-------|
| yt-dlp không tìm được | Thử lại với từ khóa ngắn hơn / tiếng Anh |
| Tất cả videos private/no caption | Báo CEO: "NLM không extract được — thử /yt-extract-short từng URL" |
| NLM timeout | Retry 1 lần sau 30s |
| < 3 kết quả tìm được | Báo CEO, gợi ý từ khóa thay thế |

---

## vs /yt-extract-short

| | `/yt-search` | `/yt-extract-short` |
|---|-------------|---------------------|
| Input | Topic/keyword | Specific URL |
| Purpose | Discovery — tìm video | Extraction — mine 1 URL |
| NLM | Tạo notebook multi-source | Add vào NLM hiện có hoặc mới |
| When | "Tìm video về X" | "Trích xuất video này" |
| Flow | search → select → NLM | URL → NLM → extract |

## COD Classification

- yt-dlp search + NLM notebook creation + queries: **Offload** (AI)
- Video selection sau khi xem list: **Core** (CEO judgment)
- Routing decision: **Core** (CEO judgment)
- Galaxy note creation: **Core** (CEO phải approve)
