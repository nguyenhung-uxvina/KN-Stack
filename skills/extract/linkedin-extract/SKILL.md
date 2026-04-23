---
name: linkedin-extract
description: Extract key information from LinkedIn posts and articles. Scrape content, engagement, author profile context, then extract actionable insights for Workshop X vault. Triggers on "linkedin", "linkedin post", "linkedin article", "bài linkedin", "trích xuất linkedin", or when user provides a linkedin.com URL.
---

# LinkedIn Extract — Trích Xuất Thông Tin từ LinkedIn

Scrape LinkedIn posts/articles → extract professional content → route insights to vault.

## When to Use

- Khi CEO gửi link LinkedIn post/article cần trích xuất
- Khi phát hiện post chứa industry insight, defense procurement info, partnership signals
- LinkedIn đặc biệt giá trị cho: defense industry contacts, procurement announcements, partnership signals

## Input

User provides one or more LinkedIn URLs. Accepted formats:
- `https://www.linkedin.com/posts/USERNAME_XXXXXXXXXX/`
- `https://www.linkedin.com/pulse/TITLE-AUTHOR/`
- `https://www.linkedin.com/feed/update/urn:li:activity:XXXXXXXXXX/`

## Workflow

### Step 1: Fetch Post Content

Use `mcp__hyperbrowser__scrape_webpage` with `outputFormat: ["markdown"]`.

⚠️ **LinkedIn thường block scraping** (login wall). Fallback options:
1. Try scrape → nếu thành công, extract content
2. Nếu bị block → ask CEO copy-paste nội dung post
3. CEO có thể screenshot → đọc image bằng Read tool

Extract:
- **Author** — tên, title, company
- **Date** — ngày đăng
- **Content** — full text
- **Engagement** — likes, comments, reposts
- **Hashtags** — nếu có
- **Media** — images, documents, carousels
- **Language** — Vietnamese/English/mixed

### Step 2: Content Analysis

LinkedIn-specific categories:

| Category | Why LinkedIn Valuable | Route To |
|----------|----------------------|----------|
| **Defense Procurement** | Announcements, contract awards | FORGE market intel |
| **Industry Insight** | Expert opinions, trend analysis | KB Layer 3 hoặc Galaxy |
| **Partnership Signal** | Company relationships, JV announcements | BRIDGE Viettel/ecosystem |
| **Technical** | Engineering deep-dives, case studies | KB Layer 2 |
| **Hiring/Talent** | Competitor hiring = capability signal | bridge-talent-map |
| **Event/Conference** | Defense expos, trade shows | bd-pulse |
| **AI/Technology** | New tools, platforms, capabilities | CEO-Self hoặc FORGE tech roadmap |

### Step 3: Extract Key Information

```markdown
## LinkedIn Post Extract
**URL:** [link]
**Author:** [name], [title] at [company]
**Date:** YYYY-MM-DD
**Engagement:** [likes] likes, [comments] comments
**Category:** [category]
**Type:** [Post / Article / Document]

### Tóm Tắt (3-5 câu)
[Nội dung chính]

### Thông Tin Quan Trọng
- [Key point 1]
- [Key point 2]

### Author Context
- [Người này là ai? Có authority trong domain không?]
- [Company nào? Competitor/partner/customer?]

### Áp Dụng Cho Workshop X
- [Relevance cụ thể]

### Action Items (nếu có)
- [ ] Follow up with author?
- [ ] Log in bd-pulse?
- [ ] Forward to team?

### Galaxy Candidate?
- [ ] Pass 3-question gate?
- Suggested title: [nếu có]
```

### Step 4: CEO Review & Route

Present extract → CEO decides routing.

## LinkedIn-Specific Value

LinkedIn khác các platform khác vì:
1. **Author authority** — title + company = credibility signal
2. **Network proximity** — "2nd connection" = reachable
3. **Procurement signals** — defense companies post contract wins
4. **Hiring = capability** — đối thủ tuyển AI engineer = đang build AI product
5. **Partnership** — JV/MOU announcements = market structure change

## Batch Mode

Multiple URLs → process all → combined report → CEO reviews at once.

## Integration Points

- Feeds into: `bridge-knowledge-base` (KB Layer 2/3)
- Feeds into: `bd-pulse` (touchpoint nếu author là contact)
- Feeds into: `bridge-talent-map` (hiring signals)
- Feeds into: FORGE competitive intel
- Feeds into: Galaxy (via `/galaxy-gate`)
- Companion to: `/x-extract`, `/fb-extract`, `/yt-extract`

## COD Classification

- Scraping + extraction: **Offload** (AI)
- Content evaluation + routing: **Core** (CEO judgment)
- Follow-up actions (contact author, log bd-pulse): **Core** (CEO relationship)
