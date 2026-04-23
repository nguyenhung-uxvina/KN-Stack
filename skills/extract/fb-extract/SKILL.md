---
name: fb-extract
description: Extract key information from Facebook short videos (Reels, Watch). Scrape video page for captions, comments, metadata, then extract actionable insights for Workshop X vault. Triggers on "facebook video", "fb video", "fb reel", "facebook reel", "video facebook", "trích xuất video", or when user provides a facebook.com/reel or fb.watch URL.
---

# FB Extract — Trích Xuất Thông Tin từ Facebook Video

Scrape Facebook short videos (Reels/Watch) → extract metadata + content → route insights to vault.

## When to Use

- Khi CEO gửi link Facebook Reel/video cần trích xuất thông tin
- Khi có danh sách links trong Inbox cần batch process
- Khi phát hiện video chứa kiến thức kỹ thuật, market intel, hoặc competitor info

## Input

User provides one or more Facebook video URLs. Accepted formats:
- `https://www.facebook.com/reel/XXXXXXXXXX`
- `https://fb.watch/XXXXXXX`
- `https://www.facebook.com/watch/?v=XXXXXXXXXX`
- `https://www.facebook.com/USERNAME/videos/XXXXXXXXXX`

If user says "links trong inbox" → scan `0_Inbox/` for files containing facebook.com URLs.

## Workflow

### Step 1: Fetch Video Page

Use `mcp__hyperbrowser__scrape_webpage` to scrape each URL with `outputFormat: ["markdown"]`.

Extract:
- **Title/Description** — caption text từ người đăng
- **Author** — tên page/người đăng
- **Date** — ngày đăng
- **Engagement** — likes, comments, shares (nếu có)
- **Comments** — top comments (chứa phản hồi thực tế)
- **Language** — Vietnamese/English/mixed
- **Duration** — nếu có

If scraping fails (login wall, private video):
- Notify CEO: "Video này cần đăng nhập / riêng tư — không scrape được"
- Suggest: CEO copy-paste caption + context thủ công

### Step 2: Content Analysis

Phân loại nội dung video:

| Category | Description | Route To |
|----------|-------------|----------|
| **Technical** | Kỹ thuật chế tạo, vật liệu, quy trình | Project docs hoặc KB Layer 2 |
| **Market Intel** | Đối thủ, sản phẩm mới, xu hướng thị trường | FORGE competitive intel |
| **Training** | Kỹ năng, phương pháp, best practices | Resources hoặc Learning |
| **Defense/Military** | Quốc phòng, vũ khí, huấn luyện quân sự | Project-specific hoặc Galaxy |
| **Business** | Quản lý, chiến lược, tổ chức | BRIDGE area |
| **Other** | Không phân loại được | CEO quyết định |

### Step 3: Extract Key Information

Cho mỗi video, tạo structured extract:

```markdown
## FB Video Extract
**URL:** [link]
**Author:** [tên]
**Date:** YYYY-MM-DD
**Category:** [Technical/Market/Training/Defense/Business/Other]
**Language:** [VN/EN/mixed]

### Tóm Tắt (3-5 câu)
[Nội dung chính của video]

### Thông Tin Quan Trọng
- [Bullet point 1 — fact/số liệu/insight cụ thể]
- [Bullet point 2]
- [...]

### Áp Dụng Cho Workshop X
- [Relevance cụ thể cho WX products/projects/strategy]
- [Hoặc: "Không trực tiếp applicable — lưu tham khảo"]

### Top Comments (nếu có giá trị)
- [Comment 1 — bổ sung thông tin hoặc phản biện]
- [Comment 2]

### Galaxy Candidate?
- [ ] Có insight đủ atomic + thay đổi design/strategy/cảnh báo trap?
- Suggested title: [nếu có]
```

### Step 4: CEO Review

Present extract(s) for validation:
- Confirm category + routing
- Decide: archive / save to project / Galaxy candidate
- For Galaxy candidates → route qua `/galaxy-gate`

### Step 5: Route & Save

| Decision | Action |
|----------|--------|
| Save to project | Append to project's reference folder |
| Save to KB | Add to `3_Resources/` appropriate subfolder |
| Galaxy candidate | Run `/galaxy-gate` → create note if passes |
| Archive | Note URL + summary in `_meta/learnings.md` |
| Discard | No action |

## Batch Mode

If multiple URLs provided:
1. Process all in sequence
2. Generate combined report
3. CEO reviews all at once
4. Batch route

## Limitations

- Facebook thường block scraping → fallback to CEO manual input
- Video audio/transcript KHÔNG extract được (không có subtitle API)
- Chỉ extract text content (caption, comments, metadata)
- Nếu video quan trọng → suggest CEO tóm tắt nội dung bằng voice note → route qua tana-iparag-bridge

## Integration Points

- Feeds into: `bridge-knowledge-base` (KB Layer 2/3)
- Feeds into: `bridge-signal-extract` (nếu video chứa market/competitor signals)
- Feeds into: Galaxy (via `/galaxy-gate`)
- Feeds into: `/research` (as supplementary source, Tier 4 social media)

## COD Classification

- Scraping + extraction: **Offload** (AI)
- Content evaluation + routing: **Core** (CEO judgment)
- Watching video + summarizing audio content: **Core** (CEO — AI can't watch)
