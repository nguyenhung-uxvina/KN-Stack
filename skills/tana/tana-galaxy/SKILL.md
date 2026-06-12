---
name: tana-galaxy
description: Galaxy health audit qua Tana — scan toàn bộ permanent notes/galaxy-candidate nodes, báo cáo orphan density, đề xuất connections còn thiếu. Dùng monthly hoặc khi Galaxy có dấu hiệu stagnation. Requires mcp__tana-local.
---

# Tana Galaxy — Galaxy Link Audit

Audit định kỳ để Galaxy không biến thành graveyard. Mục tiêu: mọi permanent note phải có ≥2 wikilinks — nodes cô lập không compound.

## When to Use

- Monthly audit (cuối tháng)
- CEO nói "galaxy audit", "kiểm tra galaxy", "orphan notes"
- Khi Galaxy tăng nhanh nhưng insights không surface trong decisions
- Trước /tana-weekly để có bức tranh toàn cảnh

## Workflow

### Step 1: Scan Galaxy nodes trong Tana

```
list_workspaces → workspaceId
search_nodes(query="permanent-note") → permanent_notes
search_nodes(query="galaxy-candidate") → pending_candidates
search_nodes(query="galaxy-pending") → deferred_items
```

Tổng hợp:

```
## Galaxy Audit — {{today}}

Permanent notes (processed): N
Galaxy candidates (pending): N
Deferred items: N
Total in pipeline: N
```

### Step 2: Orphan scan

Với mỗi permanent note node, đọc content:
```
read_node(nodeId) → content
```

Kiểm tra số wikilinks trong content (pattern: `[[...]]`).

Phân loại:
- **Healthy**: ≥3 links
- **Minimal**: 2 links (đạt yêu cầu, nhưng fragile)
- **Orphan**: 0–1 links (cần attention ngay)

Output bảng:

```
## Link Density Report

| Status | Count | % |
|--------|-------|---|
| Healthy (≥3 links) | N | N% |
| Minimal (2 links)  | N | N% |
| Orphan (<2 links)  | N | N% |

Orphan notes:
1. "<Title>" — N links hiện tại
2. "<Title>" — N links hiện tại
...
```

### Step 3: Connection suggestions cho orphans

Xử lý từng orphan node. Với mỗi orphan:

#### 3a. Đọc concept
```
read_node(nodeId) → content
```

Extract core concept (1 câu).

#### 3b. Tìm candidates để link

```
search_nodes(query="<keyword từ concept>") → potential_links
search_nodes(query="<keyword 2>") → more_candidates
```

Lọc kết quả: loại bỏ self-reference, tìm nodes thực sự liên quan.

#### 3c. Đề xuất

```
Orphan: "<Title>"
Concept: <1 câu>

Đề xuất thêm links:
→ [[<Node A>]] — <lý do>
→ [[<Node B>]] — <lý do> (cross-cluster)

Add? [y / n / edit]
```

**Không tự edit** — CEO approve, rồi tự update trong Obsidian hoặc qua /galaxy-note.

### Step 4: Pending candidates audit

Review danh sách `#galaxy-pending` và `#galaxy-candidate`:

```
search_nodes(query="galaxy-pending") → pending
```

Với mỗi item đã deferred quá 14 ngày:

```
⚠️ Deferred quá lâu: "<Title>" (N ngày)
Quyết định: [process now / route to Resources / trash]
```

### Step 5: Stagnation check

Tính toán:

**Throughput metric:**
```
New permanent notes this month: N
Galaxy candidates captured this month: N
Conversion rate: N%
```

Nếu conversion rate < 50% → cảnh báo:
```
⚠️ Galaxy Stagnation: N% candidates convert thành permanent notes.
Nguyên nhân thường gặp:
- Capture quá nhiều, atomize quá ít → giảm tana-thu, tăng tana-ich
- Candidates quá phức tạp → cần tách atomic hơn
- /galaxy-note chưa được chạy sau tana-ich
```

### Step 6: Galaxy Health Report

```
## Galaxy Health Report — {{today}}

### Link Density
Healthy: N (N%) ✅
Minimal: N (N%) ⚠️
Orphan:  N (N%) 🔴

### Pipeline
Candidates pending: N
Deferred >14 days: N
Throughput (30d): N%

### Actions Required
- [ ] Fix N orphan notes (see suggestions above)
- [ ] Process N deferred candidates
- [ ] <other actions>

### Trend
<improving / stable / declining — based on comparison với last audit>
```

## Frequency

| Cadence | Trigger |
|---------|---------|
| Monthly | /tana-galaxy scheduled cuối tháng |
| Ad-hoc | Sau khi có batch capture lớn (>5 items) |
| Pre-gate | Trước G1/G2/G3 review để surface relevant insights |

## COD Classification

- Scan + report: **Offload (O)**
- Quyết định fix orphan / route candidate: **Core (C)**
- Update links trong Obsidian: **Core (C)** — không thể delegate qua Tana MCP

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId |
| `search_nodes` | Scan permanent notes, candidates, pending |
| `read_node` | Đọc content từng node để count links |
| `get_children` | Nếu notes có children cần kiểm tra |
