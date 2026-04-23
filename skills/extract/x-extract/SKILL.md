---
name: x-extract
description: Extract key information from X (Twitter) posts, threads, and articles. Scrape post content, replies, engagement metrics, then extract actionable insights for Workshop X vault. Triggers on "x post", "twitter", "tweet", "x thread", "bài trên x", "trích xuất x", or when user provides an x.com or twitter.com URL.
---

# X Extract — Trích Xuất Thông Tin từ X (Twitter)

Scrape X posts/threads/articles → extract content + engagement → route insights to vault.

## When to Use

- Khi CEO gửi link X post/thread/article cần trích xuất
- Khi phát hiện post chứa kiến thức kỹ thuật, market intel, industry insight
- Đã dùng trong session này cho @leopardracer (Skills), @MitcheIl (agents), @shannholmberg (moats)

## Input

User provides one or more X URLs. Accepted formats:
- `https://x.com/USERNAME/status/XXXXXXXXXX`
- `https://twitter.com/USERNAME/status/XXXXXXXXXX`
- Article links: `https://x.com/USERNAME/article/XXXXXXXXXX`

## Workflow

### Step 1: Fetch Post Content

Use `mcp__hyperbrowser__scrape_webpage` with `outputFormat: ["markdown"]`.

Extract:
- **Author** — tên + handle (@username)
- **Date** — ngày đăng
- **Content** — full text (thread = tất cả các tweets)
- **Engagement** — views, likes, retweets, replies, bookmarks
- **Media** — images, videos (describe if present)
- **Article** — nếu là X Article, extract full body text
- **Language** — Vietnamese/English/mixed

### Step 2: Content Analysis

Phân loại:

| Category | Route To |
|----------|----------|
| **Technical/Engineering** | Project docs hoặc KB Layer 2 |
| **AI/Tools** | CEO-Self hoặc AI-Infrastructure |
| **Market Intel/Defense** | FORGE competitive intel |
| **Business/Strategy** | BRIDGE area |
| **Methodology/Learning** | Resources hoặc Learning |
| **Other** | CEO quyết định |

### Step 3: Extract Key Information

```markdown
## X Post Extract
**URL:** [link]
**Author:** [name] (@handle)
**Date:** YYYY-MM-DD
**Engagement:** [views] views, [likes] likes, [retweets] RT
**Category:** [category]
**Type:** [Post / Thread / Article]

### Tóm Tắt (3-5 câu)
[Nội dung chính]

### Thông Tin Quan Trọng
- [Key point 1]
- [Key point 2]

### Áp Dụng Cho Workshop X
- [Relevance cụ thể]

### Galaxy Candidate?
- [ ] Pass 3-question gate?
- Suggested title: [nếu có]
```

### Step 4: CEO Review & Route

Present extract → CEO decides routing:
- Save to project / KB / Galaxy / Archive / Discard

## Batch Mode

Multiple URLs → process all → combined report → CEO reviews at once.

## Tips

- X articles (long-form) thường chứa nhiều content hơn tweets
- Thread posts: scrape lấy toàn bộ thread, không chỉ tweet đầu
- High engagement (>100K views) = strong market signal
- Quote tweets chứa context bổ sung — extract nếu relevant

## Integration Points

- Feeds into: `bridge-knowledge-base`, Galaxy, `/research` (Tier 4 social)
- Companion to: `/fb-extract`, `/yt-extract`, `/chat-extract`

## COD Classification

- Scraping + extraction: **Offload** (AI)
- Content evaluation + routing: **Core** (CEO judgment)
