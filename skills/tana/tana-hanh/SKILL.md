---
name: tana-hanh
description: THỊNH bước Hành — harvest Galaxy insights từ Tana, map tới decisions đang pending, brief CEO với top 3 insights có actionable implication cho tuần tới. Knowledge chỉ có giá trị khi được dùng. Requires mcp__tana-local.
---

# Tana Hanh — Harvest Insights for Action

Bước **H (Hành)** trong THỊNH workflow — bước cuối và quan trọng nhất. Galaxy không phải archive, đó là decision engine. Hành = kéo insights ra và dùng chúng ngay hôm nay.

## When to Use

- CEO nói "hành bước", "harvest insights", "galaxy nói gì về X"
- Trước khi đưa ra quyết định lớn (design choice, strategy pivot, gate review)
- Cuối tuần trong tana-weekly Step H
- Khi stuck trên một vấn đề — Galaxy có thể đã có answer

## Triết lý

> "Build Galaxy để dùng, không phải để có."

Nếu CEO không chạy Hành thường xuyên → Galaxy = graveyard đẹp. Hành đo lường xem đầu tư vào Ích có sinh lợi không.

## Workflow

### Step 1: Xác định context hiện tại

Hỏi CEO (hoặc detect tự động từ Tana):

**Option A — CEO chỉ định:**
> "Tôi đang cần insights về: <topic/decision>"

**Option B — Auto-detect từ Tana:**
```
search_nodes(query="active project") → active_projects
search_nodes(query="session-log", limit=3) → recent_work
```

Từ đó extract: đang làm gì, đang stuck ở đâu, quyết định nào đang pending.

### Step 2: Query Galaxy nodes

```
list_workspaces → workspaceId
search_nodes(query="permanent-note") → all_galaxy_nodes
```

Với active context, search thêm:
```
search_nodes(query="<keyword từ context 1>") → relevant_1
search_nodes(query="<keyword từ context 2>") → relevant_2
search_nodes(query="<project name>") → project_specific
```

Priority tags — search thêm:
```
search_nodes(query="#warning") → trap_alerts
search_nodes(query="#three-laws") → distilled_laws
search_nodes(query="#ceo") → leadership_insights
```

### Step 3: Read + filter relevant nodes

Với mỗi node tìm được:
```
read_node(nodeId) → content
```

Score relevance (0–3):
- +1 nếu liên quan trực tiếp tới active project
- +1 nếu có tag `#warning` hoặc `#three-laws` (high-leverage)
- +1 nếu được tạo trong 30 ngày (fresh)

Lấy top 5 nodes score cao nhất.

### Step 4: Map insights → actions

Với mỗi top node, tạo mapping:

```
Insight: [[<Note title>]]
Core concept: <1-2 câu>
Relevant to: <project / decision>
Implication: <nếu áp dụng insight này thì...>
Action: <hành động cụ thể có thể làm tuần này>
```

**Action phải SMART:**
- Specific: "test X" không phải "nghiên cứu X"
- Tana-trackable: có thể tạo task node
- Time-bound: "trong 3 ngày" không phải "sớm"

### Step 5: Brief CEO — Top 3

```
## Galaxy Harvest — {{today}}
Context: <active projects + pending decisions>

---

### #1 — [[<Note A>]]
Insight: <2-3 câu>
Apply to: <project/decision>
Action this week: <cụ thể>

### #2 — [[<Note B>]]
Insight: <2-3 câu>
Apply to: <project/decision>  
Action this week: <cụ thể>

### #3 — [[<Note C>]]
Insight: <2-3 câu>
Apply to: <project/decision>
Action this week: <cụ thể>

---
⚠️ Trap alerts (nếu có):
[[<Warning note>]] — <trap đang relevant>
```

### Step 6: Tạo action tasks trong Tana (nếu CEO approve)

Với mỗi action CEO approve:
```
import_tana_paste(parentNodeId=todayNodeId):
%%tana%%
- [ ] <action> #inbox
  - Why:: Galaxy insight: [[<Note>]]
  - COD:: C
  - PARA-dest:: 1_Projects/<project>
  - Due:: <date>
```

### Step 7: Log harvest

```
import_tana_paste(parentNodeId=todayNodeId):
%%tana%%
- Galaxy Harvest #harvest-log
  - Date:: {{today}}
  - Context:: <active focus>
  - Insights surfaced:: N
  - Actions created:: N
  - Top insight:: [[<Note A>]]
```

## Harvest Quality Metrics

Theo dõi theo thời gian:

| Metric | Healthy | Warning |
|--------|---------|---------|
| Insights surfaced per session | 3–5 | <2 hoặc >8 |
| Actions created / insights | >50% | <30% |
| Insights reused (cited >1 lần) | >20% | <5% |
| Days since last harvest | ≤7 | >14 |

**Nếu "insights surfaced < 2"** → Galaxy quá nhỏ hoặc quá disconnected.
Chạy /tana-ich để tăng connectivity.

**Nếu "actions created < 30%"** → Insights không actionable.
Galaxy notes quá abstract — cần rewrite với "Tại sao điều này quan trọng?" section rõ hơn.

## Harvest Modes

| Mode | Khi nào | Cách gọi |
|------|---------|---------|
| **Full** | Weekly review | `/tana-hanh` |
| **Focused** | Trước gate review | `/tana-hanh gate2` |
| **Quick** | Đầu ngày làm việc | `/tana-hanh quick` — chỉ top 1 insight |
| **Trap scan** | Khi cảm thấy stuck | `/tana-hanh traps` — chỉ #warning nodes |

## Relationship với THỊNH

```
Thu → Hóa → Ích → Nhớ → Hành
                         ↑
                    Đây là nơi ROI của Galaxy được realize.
                    4 bước trước chỉ là chuẩn bị.
```

Nếu Hành chưa được chạy trong >14 ngày → cảnh báo trong tana-weekly:

```
⚠️ Last Harvest: N ngày trước.
Galaxy đang build nhưng không được dùng.
ROI = 0 cho đến khi chạy /tana-hanh.
```

## COD Classification

- Scan + score + map: **Offload (O)**
- Quyết định action có worth pursuing: **Core (C)**
- Tạo task nodes sau approve: **Offload (O)**
- Interpret insight trong context cụ thể: **Core (C)**

## Tana MCP Tools Used

| Tool | Khi nào |
|------|---------|
| `list_workspaces` | Lấy workspaceId |
| `search_nodes` | Query Galaxy nodes theo keyword + tag |
| `read_node` | Đọc full content nodes để score |
| `get_or_create_calendar_node` | Log harvest + tạo action tasks |
| `import_tana_paste` | Tạo action tasks + harvest log |
