---
name: tana-nho
description: THỊNH bước Nhớ — persist knowledge bằng cách sync Tana state với CLAUDE.md, phát hiện drift, và đề xuất updates cụ thể. Memory chỉ bền vững khi được kiểm tra và corrected định kỳ. Requires mcp__tana-local.
---

# Tana Nho — Persist & Sync Memory

Bước **N (Nhớ)** trong THỊNH workflow. Mục tiêu: CLAUDE.md luôn phản ánh reality — không phải snapshot từ 3 tháng trước. Tana = source of truth cho current state; CLAUDE.md = working memory cho AI.

## When to Use

- CEO nói "nhớ bước", "sync claude", "kiểm tra drift"
- Cuối tuần trong tana-weekly Step N
- Sau khi project status thay đổi lớn (G1→G2, product launch, team change)
- Khi AI đưa ra gợi ý dựa trên outdated context ("nhưng project đó đã xong rồi mà")

## Triết lý

> CLAUDE.md drift = AI mang bản đồ cũ vào địa hình mới.

Nhớ không phải ghi thêm — là kiểm tra xem cái đã ghi còn đúng không. Sai thì sửa, đúng thì giữ.

## Workflow

### Step 1: Lấy current state từ Tana

```
list_workspaces → workspaceId
```

Query 4 dimensions:

**Projects:**
```
search_nodes(query="active project") → active_projects
search_nodes(query="completed project") → completed_projects
```

**Areas:**
```
search_nodes(query="area active") → active_areas
```

**Galaxy count:**
```
search_nodes(query="permanent-note") → galaxy_nodes
```

**Products/Teams:**
```
search_nodes(query="product") → products
search_nodes(query="team member") → team
```

### Step 2: Đọc CLAUDE.md

```
Read D:\Workshop_X\.claude\CLAUDE.md
```

*(Skill này đọc file trực tiếp, không qua Tana MCP)*

Extract current state claims:
- Product list + descriptions
- Project list + statuses
- Team composition
- Galaxy note count
- Any "current" or "active" statements

### Step 3: Compare — Tana vs CLAUDE.md

Tạo diff table:

```
## Drift Detection — {{today}}

### Projects
| Project | Tana status | CLAUDE.md | Drift? |
|---------|------------|-----------|--------|
| VN-TGT-F | active | active | ✅ |
| BB-01 | G1 pilot | G1 pilot | ✅ |
| <new project> | active | NOT LISTED | 🔴 missing |
| <old project> | completed | still listed | 🟡 stale |

### Areas
| Area | Tana | CLAUDE.md | Drift? |
|------|------|-----------|--------|
| ...  | ...  | ...       | ...    |

### Galaxy Count
Tana: N notes
CLAUDE.md: M notes
Drift: <±N> → <needs update / in sync>

### Products
| Product | CLAUDE.md description | Matches reality? |
|---------|-----------------------|-----------------|
| V-SMASH | AI FCS nội địa hóa... | ✅ |
| TDR | ... | ✅ |
```

### Step 4: Flag critical drifts

**Critical (update ngay):**
- Project trong CLAUDE.md nhưng đã completed → AI đang prioritize sai
- Project active không có trong CLAUDE.md → AI không biết context
- Product description sai → AI có thể đề xuất sai direction

**Non-critical (update lần sau):**
- Galaxy count lệch ±3
- Minor phrasing differences

### Step 5: Đề xuất edits cụ thể

Với mỗi drift, đề xuất edit cụ thể — không vague:

```
## Đề xuất updates cho CLAUDE.md

### 1. Add missing project [CRITICAL]
Thêm vào Projects section:
  "- VN-XUONG-UUV: Phase 0 Pre-study, active"

### 2. Remove stale project
Xóa hoặc archive:
  "- WX-KPIPE-001: completed 2026-03"

### 3. Update Galaxy count
Đổi "5_Galaxy: N notes" → "5_Galaxy: M notes"

### 4. <other edit>
```

### Step 6: CEO approve + apply

Hỏi CEO từng edit:
```
Apply update #1? [y / n / edit]
Apply update #2? [y / n / edit]
...
```

**Sau khi CEO approve → nhắc CEO tự edit** (CLAUDE.md là file nhạy cảm, AI không tự sửa):

```
✅ Approved updates: N items

Để apply:
1. Mở D:\Workshop_X\.claude\CLAUDE.md
2. Apply các edits sau:
   [list edits rõ ràng với before/after]

Hoặc: paste danh sách edits vào chat và tôi sẽ apply qua Edit tool.
```

### Step 7: Log sync

Sau khi apply:

```
import_tana_paste(parentNodeId=todayNodeId):
%%tana%%
- CLAUDE.md Sync #nho-log
  - Date:: {{today}}
  - Drifts found:: N
  - Critical fixes:: N
  - Galaxy count synced:: <yes/no>
  - Next sync due:: {{today+7}}
```

## Drift Severity Matrix

| Type | Example | Severity | Action |
|------|---------|----------|--------|
| Missing active project | New project not in CLAUDE.md | 🔴 Critical | Fix now |
| Stale completed project | Done project still "active" | 🔴 Critical | Fix now |
| Wrong product description | V-SMASH mô tả sai | 🔴 Critical | Fix now |
| Galaxy count off | ±5 notes | 🟡 Medium | Fix this week |
| Minor phrasing | "3 chuyên gia" vs "4 chuyên gia" | 🟡 Medium | Fix this week |
| Stylistic difference | Format inconsistency | 🟢 Low | Fix monthly |

## Nhớ vs Memory Tool

| | tana-nho | Claude Memory files |
|--|---------|---------------------|
| Scope | CLAUDE.md (AI working memory) | Long-term user/project facts |
| Trigger | THỊNH weekly | When user explicitly asks |
| Source of truth | Tana workspace | Conversation + user input |
| Frequency | Weekly | As needed |

Hai hệ thống complement nhau — không thay thế nhau.

## Edge Cases

**Tana không reflect thực tế:**
→ Tana cũng có thể outdated nếu CEO không update nodes
→ Hỏi: "Node này trong Tana còn đúng không?" trước khi dùng để update CLAUDE.md

**CLAUDE.md có thông tin không có trong Tana:**
→ Có thể CLAUDE.md có context quan trọng chưa được transfer vào Tana
→ Flag để CEO xem xét có nên tạo Tana node không

## COD Classification

- Scan Tana + đọc CLAUDE.md: **Offload (O)**
- So sánh + flag drifts: **Offload (O)**
- Quyết định edit nào apply: **Core (C)**
- Apply edits vào CLAUDE.md: **Offload (O)** sau CEO approve

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId |
| `search_nodes` | Query projects, areas, galaxy, products |
| `read_node` | Đọc specific nodes khi cần detail |
| `get_or_create_calendar_node` | Log sync vào daily note |
| `import_tana_paste` | Tạo sync log node |
