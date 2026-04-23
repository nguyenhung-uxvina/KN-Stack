---
name: yt-extract
description: Extract key information from YouTube Shorts and short videos. Fetch transcript/captions, metadata, comments, then extract actionable insights for Workshop X vault. Triggers on "youtube short", "yt short", "youtube video ngắn", "trích xuất youtube", or when user provides a youtube.com/shorts or youtu.be URL.
---

# YT Extract — Trích Xuất Thông Tin từ YouTube Short Video

Fetch YouTube Shorts/short videos → extract transcript + metadata → route insights to vault.

## When to Use

- Khi CEO gửi link YouTube Shorts cần trích xuất thông tin
- Khi phát hiện video chứa kiến thức kỹ thuật, market intel, hoặc competitor info
- Khác với `/yt-search` (tìm kiếm video) — skill này **extract nội dung** từ link đã có

## Input

User provides one or more YouTube URLs. Accepted formats:
- `https://youtube.com/shorts/XXXXXXXXXXX`
- `https://www.youtube.com/watch?v=XXXXXXXXXXX`
- `https://youtu.be/XXXXXXXXXXX`

## Workflow

### Step 1: Fetch Video Data

Use `mcp__hyperbrowser__scrape_webpage` to scrape video page with `outputFormat: ["markdown"]`.

Extract:
- **Title** — tiêu đề video
- **Channel** — tên kênh
- **Date** — ngày đăng
- **Views** — lượt xem
- **Duration** — thời lượng
- **Description** — mô tả video
- **Tags/Hashtags** — nếu có
- **Language** — Vietnamese/English/mixed

### Step 2: Get Transcript

Try transcript extraction in order:
1. Scrape page → tìm transcript/captions trong markdown output
2. Nếu không có → notify CEO: "Video không có phụ đề — cần tóm tắt thủ công"

Transcript là nguồn giá trị nhất — ưu tiên extract.

### Step 3: Content Analysis

Phân loại nội dung:

| Category | Description | Route To |
|----------|-------------|----------|
| **Technical** | Chế tạo, CNC, hàn, vật liệu, quy trình | Project docs hoặc KB Layer 2 |
| **Market Intel** | Đối thủ, sản phẩm mới, xu hướng | FORGE competitive intel |
| **Training** | Kỹ năng, best practices, tutorial | Resources hoặc Learning |
| **Defense/Military** | Quốc phòng, vũ khí, huấn luyện | Project-specific hoặc Galaxy |
| **Business/AI** | Quản lý, AI tools, productivity | BRIDGE hoặc CEO-Self |
| **Other** | Không phân loại được | CEO quyết định |

### Step 4: Extract Key Information

```markdown
## YT Video Extract
**URL:** [link]
**Title:** [tiêu đề]
**Channel:** [tên kênh]
**Date:** YYYY-MM-DD
**Duration:** [thời lượng]
**Views:** [lượt xem]
**Category:** [Technical/Market/Training/Defense/Business/Other]

### Tóm Tắt (3-5 câu)
[Nội dung chính]

### Transcript Highlights
- [Đoạn quan trọng 1 — timestamp nếu có]
- [Đoạn quan trọng 2]

### Thông Tin Quan Trọng
- [Fact/số liệu/insight cụ thể]
- [...]

### Áp Dụng Cho Workshop X
- [Relevance cụ thể cho WX products/projects/strategy]
- [Hoặc: "Không trực tiếp applicable — lưu tham khảo"]

### Galaxy Candidate?
- [ ] Có insight đủ atomic + thay đổi design/strategy/cảnh báo trap?
- Suggested title: [nếu có]
```

### Step 5: CEO Review & Route

| Decision | Action |
|----------|--------|
| Save to project | Append to project reference folder |
| Save to KB | Add to `3_Resources/` appropriate subfolder |
| Feed to NLM | Add as source to relevant NLM notebook |
| Galaxy candidate | Run `/galaxy-gate` → create note if passes |
| Archive | URL + summary in `_meta/learnings.md` |
| Discard | No action |

## Batch Mode

Multiple URLs → process all → combined report → CEO reviews at once.

## vs /yt-search

| | `/yt-search` | `/yt-extract` |
|---|-------------|---------------|
| Input | Topic/keyword | Specific URL |
| Purpose | Discovery — find videos | Extraction — mine content |
| Output | List of videos + metadata | Deep extract from 1 video |
| When | "Tìm video về X" | "Trích xuất video này" |

## Integration Points

- Feeds into: `bridge-knowledge-base` (KB Layer 2/3)
- Feeds into: Galaxy (via `/galaxy-gate`)
- Feeds into: NLM notebooks (as source)
- Feeds into: `/research` (as Tier 3 YouTube source)
- Companion to: `/yt-search` (search first, extract best results)

## COD Classification

- Scraping + transcript extraction: **Offload** (AI)
- Content evaluation + routing: **Core** (CEO judgment)
- Watching video without captions: **Core** (CEO — AI can't watch)
