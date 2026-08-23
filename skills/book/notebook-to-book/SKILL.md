---
name: notebook-to-book
description: "Orchestrator biến NotebookLM notebook thành sách kỹ thuật publication-quality. Adapter của codebase-to-book: P1 thay bằng NLM multi-query topic extraction thay vì file exploration. Pipeline 9-phase: P1 NLM-explore → P2 position → P3 outline → P4 write → P5 review → P6 revise → P7 audit → P8 notebook (new NLM) → P9 CEO insight. Flags: --notebook <name>, --codebase <path> (supplementary), --deep, --quick, --no-nlm, --from/--only, --lang vi|en. Triggers on: 'notebook to book', 'notebooklm thành sách', 'chuyển notebook thành sách', 'nlm to book', 'ntb'."
---

# Notebook-to-Book — Orchestrator (9-Phase, NLM-First)

> **Role:** Chỉ huy trưởng — pipeline 9-phase với P1 adapter NLM thay vì file exploration
> **Parent:** Adapter của `codebase-to-book` — P2-P9 giống hệt; P1 và P7 được điều chỉnh
> **Source:** NotebookLM notebook (đã tồn tại) → book publication-quality
> **Case study:** "Tìm Kiếm Alpha: Chiến Lược Kinh Doanh Định Lượng" — NLM notebook → sách trading quantitative

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                     notebook-to-book (ORCHESTRATOR — 9 phases)                          │
│                                                                                          │
│  Flags: --notebook <name> | --codebase <path> | --deep | --quick | --no-nlm             │
│         --from X | --only X | --lang vi|en | --audience leader|engineer|both            │
│                                                                                          │
│  ┌──────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐            │
│  │ P1   │▶│ P2  │▶│ P3  │▶│ P4  │▶│ P5  │▶│ P6  │▶│ P7  │▶│ P8  │▶│ P9  │            │
│  │NLM-  │ │POSI │ │OUT- │ │WRITE│ │REVI │ │REVI │ │AUD- │ │NOTE-│ │CEO- │            │
│  │EXPLO │ │TION │ │LINE │ │     │ │EW   │ │SE   │ │IT*  │ │BOOK │ │INSI │            │
│  │RE    │ │C    │ │C    │ │∥    │ │∥    │ │     │ │C    │ │NLM  │ │GHT  │            │
│  │∥NLM  │ │     │ │     │ │N×   │ │2-3× │ │     │ │     │ │MCP  │ │C    │            │
│  │query │ │     │ │     │ │     │ │     │ │     │ │     │ │     │ │     │            │
│  └──┬───┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘            │
│     │CEO     │CORE   │CORE   │CEO    │CEO    │CEO    │CORE   │CEO    │CORE           │
└─────────────────────────────────────────────────────────────────────────────────────────┘

* P7 audit mode = source attribution (không phải verbatim code) trừ khi --codebase có mặt

Data Bus: D:\Workshop_X\3_Resources\Books\<slug>\   (trong vault)
          hoặc <cwd>/book-output/<slug>/             (ngoài vault)
State:    <output_dir>/_pipeline_state.md
```

## Differences vs `codebase-to-book`

| Phase | codebase-to-book | notebook-to-book |
|-------|-----------------|-----------------|
| P1 | File exploration (Glob/Read per subsystem) | NLM multi-query topic extraction |
| P1 input | File path | NLM notebook name/ID |
| P4 code examples | Verbatim from codebase | Reference `--codebase` path (optional) |
| P7 audit | Verbatim → pseudocode + IP rating | Source attribution + IP rating (no verbatim code by default) |
| P8 | New NLM notebook from compiled book | Same — new NLM notebook (separate from source) |
| Slug | basename(path) | notebook name → kebab-case |

## How to Use

### Full pipeline (Vietnamese, dual audience, NLM + insights)
```
/notebook-to-book --notebook "Tìm Kiếm Alpha: Chiến Lược Kinh Doanh Định Lượng"
```

### With supplementary codebase (code examples trong chapters)
```
/notebook-to-book --notebook "Tìm Kiếm Alpha" --codebase D:\TradingAgents
```

### Deep extraction (extra NLM queries per topic)
```
/notebook-to-book --notebook "Tìm Kiếm Alpha" --deep
```

### Resume from specific block
```
/notebook-to-book --notebook "Tìm Kiếm Alpha" --from P4
```

### Quick (skip review + revise)
```
/notebook-to-book --notebook "Tìm Kiếm Alpha" --quick
```

### Book only, no NLM rebuild
```
/notebook-to-book --notebook "Tìm Kiếm Alpha" --no-nlm
```

---

## Orchestrator Workflow

### Step 1: Parse Arguments

```
FLAGS:
  --notebook <name>       → NLM notebook name (fuzzy match) or exact UUID
  --codebase <path>       → Supplementary codebase for code examples (P4)
                            e.g., D:\TradingAgents
  --deep                  → P1: 3 extra queries per topic cluster
                            P4: /research --deep per chapter
  --quick                 → Skip P5/P6
  --no-nlm                → Skip P8/P9
  --from X                → Resume từ phase X (P1-P9)
  --only X                → Run single phase X only
  --audience leader|engineer|both  → default 'both'
  --lang vi|en            → default 'vi'
  --insight-lens          → P9 lens override (default: helix,forge,galaxy,ach,ip)
```

### Step 1.5: Resolve Notebook + Output Directory

```
NOTEBOOK RESOLUTION:
  1. Call mcp__notebooklm-mcp__notebook_list
  2. Fuzzy match --notebook value against notebook titles
  3. If multiple matches → present list to CEO, ask to confirm
  4. If no match → HALT: "Notebook không tìm thấy. Kiểm tra tên."
  5. Call mcp__notebooklm-mcp__notebook_get(notebook_id) → source count, metadata

SLUG DERIVATION:
  notebook_name → lowercase → replace spaces/colons/special_chars → kebab-case
  e.g., "Tìm Kiếm Alpha: Chiến Lược Kinh Doanh Định Lượng"
       → "tim-kiem-alpha-chien-luoc-kinh-doanh-dinh-luong"
  (normalize Vietnamese diacritics: ì→i, ế→e, etc.)
  Short slug preferred: "tim-kiem-alpha"

OUTPUT DIR:
  If pwd within D:\Workshop_X vault OR target is D:\Workshop_X:
    Output = D:\Workshop_X\3_Resources\Books\<slug>\
  Else:
    Output = <cwd>/book-output/<slug>/
```

### Step 1.6: Input Validation & CEO Context Enrichment

#### 1.6a: NLM Auth Pre-Check

```
NLM AUTH — Verifying notebooklm-mcp session...
  → Call mcp__notebooklm-mcp__refresh_auth
  → If fail: HALT
    "Run `nlm login` trong terminal, rồi /notebook-to-book ... --from P1"
  → If ok: proceed
```

#### 1.6b: Codebase Pre-Check (if --codebase set)

```
CODEBASE CHECK — {{codebase_path}}
  □ Path exists?
  □ Contains source files?
  □ Size estimate — warn if >100k files
RESULT: [GO / NO-GO]
```

#### 1.6c: Present Scope to CEO

```
═══ NOTEBOOK-TO-BOOK — SCOPE PREVIEW ═══

Source notebook: "{{notebook_title}}"
  Notebook ID: {{uuid}}
  Sources: {{N}} sources in NLM
  Last updated: {{date}}

Slug: {{slug}}
Output dir: {{output_dir}}

Supplementary codebase: {{path | NONE}}
Pipeline: {{9 phases | --quick: 7 | --no-nlm: 7}}
Audience: {{leader | engineer | both}}
Language: {{vi | en}}
Deep extraction: {{YES — 3 extra NLM queries per topic | NO}}

Estimated deliverables:
  - {{N_topics}} topic exploration files (P1)
  - 1 positioning doc (P2)
  - 1 outline ~15-18 chapters (P3)
  - {{N_ch}} chapter drafts (P4)
  - 1 compiled book.md (P7)
  - 1 NotebookLM notebook (P8) — if NLM mode
  - 1 CEO insights doc (P9) — if NLM mode

Estimated cost: {{rough estimate based on topic count × deep flag}}

CEO:
(1) ▶️ Confirm — chạy P1
(2) ⚙️ Adjust flags
(3) ⏸️ Cancel
═══════════════════════════════════════════════════
```

Wait for CEO response before proceeding.

---

## P1 — NLM Topic Extraction (NLM Adapter for book-explore)

> This replaces `book-explore`. All other blocks use exact same logic as `codebase-to-book`.

### P1.1: Discovery Query

Run 1 initial NLM query to map notebook structure:

```
Query: "Hãy liệt kê đầy đủ: (1) các chương và phần chính trong tài liệu này,
        (2) 5-10 chủ đề lớn được đề cập, (3) các framework hoặc mô hình tư duy
        cốt lõi, (4) loại nội dung có mặt (lý thuyết / thực hành / case study /
        dữ liệu / code). Không cần giải thích chi tiết — chỉ cần bản đồ cấu trúc."
```

From response → derive **Topic Cluster Map** (= subsystem map equivalent):
- Each cluster = 1 major theme or section of the notebook
- Aim for 5-10 clusters (matches P3 chapter granularity)
- Each cluster should be independently queryable

### P1.2: Present Topic Cluster Map to CEO (Checkpoint BEFORE fan-out)

```
═══ P1 TOPIC CLUSTER MAP — {{slug}} ═══

Notebook: "{{title}}" ({{N}} NLM sources)

Proposed topic clusters ({{count}}):
  1. <cluster-name-1> — <1-line scope>
  2. <cluster-name-2> — ...
  ...

Cross-cutting themes detected: {{list}}
Content types found: {{theory|practice|case_study|data|code}}

Supplementary codebase: {{path — will be used for code examples in P4 | NONE}}

CEO:
(1) ✅ Approve — fan-out {{N}} NLM extraction queries
(2) 📝 Merge clusters (specify)
(3) ➕ Add missing cluster (specify)
(4) ⏸️ Dừng
═══════════════════════════════════════════════════
```

**Wait for CEO approval before fan-out.**

### P1.3: Fan-Out NLM Extraction Queries

Sau khi CEO approve topic map, spawn N parallel NLM queries **trong single message**:

```python
# Pseudocode — orchestrator fan-out
for cluster in approved_clusters:
    # Base queries (always)
    query_1 = f"""
        Về chủ đề "{cluster.name}":
        (1) Các luận điểm chính và kết luận
        (2) Frameworks, mô hình, hoặc phương pháp được trình bày
        (3) Ví dụ cụ thể, case study, dữ liệu, hoặc bằng chứng
        (4) Bài học thực hành và khuyến nghị hành động
        (5) Điểm bất ngờ hoặc counterintuitive insights
    """
    query_2 = f"""
        Về "{cluster.name}": Các quyết định thiết kế / lý do / trade-offs
        được thảo luận? Tại sao tác giả chọn cách tiếp cận này thay vì
        alternatives? Limitations nào được thừa nhận?
    """
    # --deep extra queries (if flag set)
    if deep:
        query_3 = f"Về '{cluster.name}': Chi tiết methodology, công thức, hoặc quy trình step-by-step?"
        query_4 = f"Về '{cluster.name}': Góc nhìn phê bình, rủi ro, edge cases, và điều kiện thất bại?"
        query_5 = f"Về '{cluster.name}': Ứng dụng thực tế và ví dụ từ thực tiễn?"
    
    # Save to Phase1-Exploration/<cluster_slug>_Exploration.md
    write(f"{output_dir}/Phase1-Exploration/{cluster.slug}_Exploration.md",
          render_nlm_exploration(cluster, query_responses))
```

**Output schema per cluster** (saves to `Phase1-Exploration/<cluster>_Exploration.md`):

```markdown
# NLM Exploration — <cluster>
Date: <date> | Source: NotebookLM "<notebook_title>"

## Core Arguments and Conclusions
## Frameworks and Mental Models
## Examples, Case Studies, Data
## Actionable Insights
## Design Decisions and Trade-offs
## Surprising / Counterintuitive Points
## Open Questions

[If --deep:]
## Methodology Detail
## Critical Lens (risks, edge cases, failure conditions)
## Real-World Applications
```

### P1.4: Cross-Cutting Query + Synthesis

Sau khi per-cluster queries complete, run 1 synthesis query:

```
Query: "Nhìn toàn bộ tài liệu: (1) Các chủ đề xuyên suốt nào kết nối các phần lại
        với nhau? (2) Luận điểm overarching của tác giả là gì? (3) Cấu trúc tư duy
        nền tảng (mental model, worldview)? (4) Độc giả lý tưởng của tài liệu này
        là ai và họ sẽ thay đổi gì sau khi đọc?"
```

Merge → `Phase1-Exploration/P1_Synthesis.md` (same schema as `book-explore`):

```markdown
# P1 Synthesis — {{slug}}
Date: {{today}} | Source: NLM "{{title}}"

## Coverage Map
| Cluster | Queries Run | Output File | Status |
|---------|------------|-------------|--------|

## Cross-Cutting Themes
## Overarching Argument Structure
## Ideal Reader Profile (→ seeds P2 audience)
## Surprising Decisions Catalog
## Open Questions (aggregated)
## Coverage Gaps (topics mentioned but shallow in NLM responses)
```

### P1.5: CEO Checkpoint After P1

```
═══ BLOCK P1 NLM EXTRACTION COMPLETE ═══
Notebook queried: "{{title}}"
Topic clusters extracted: {{N}}
Total NLM queries: {{N_base + N_deep}}
Cross-cutting themes: {{K}} identified

Deliverables:
  - {{output_dir}}/Phase1-Exploration/ ({{N+1}} files)

Key findings:
  - {{bullet 1 — dominant theme}}
  - {{bullet 2 — main framework detected}}
  - {{bullet 3 — ideal reader + use case}}

CEO:
(1) ✅ Approve → Block P2 (Positioning)
(2) 🔄 Re-query specific cluster: [specify]
(3) ➕ Add topic cluster not covered: [specify]
(4) ⏸️ Dừng — đọc exploration outputs trước
═══════════════════════════════════════════════════
```

---

## P2-P9: Same as `codebase-to-book`

> **Delegation rule:** For P2-P9, invoke the corresponding `book-*` sub-skills exactly as documented in `codebase-to-book`. The P1 output format is compatible — P2 reads `P1_Synthesis.md`, P3 reads thesis, P4 reads exploration files.

### P4 Enrichment: Supplementary Codebase (if --codebase set)

When `--codebase <path>` is provided:
- P4 writing subagents receive `codebase_path` as context
- Subagents may read relevant files for code examples
- Prompt addition: "Tham khảo codebase tại `{{codebase_path}}` để thêm code examples minh họa vào chapters. Dùng pseudocode cho verbatim sections (P7 sẽ audit)."

### P7 Audit Adapter: Source Attribution Mode

By default (no `--codebase`):
- Skip verbatim-code check (no source code in book)
- Focus audit on:
  1. **Claim attribution** — lý thuyết/frameworks có được ghi nguồn?
  2. **Data attribution** — số liệu/statistics có cite nguồn gốc không?
  3. **IP rating per chapter** — SAFE / REVIEW / SENSITIVE (same scale)
  4. **Originality check** — tỷ lệ nội dung gốc vs tổng hợp từ nguồn

When `--codebase` is provided:
- Run full P7 verbatim check on code snippets (same as `codebase-to-book`)

---

## Pipeline State Schema

```markdown
---
source_notebook: "{{notebook_title}}"
notebook_id: {{uuid}}
source_type: notebooklm
codebase_path: {{path | null}}
slug: {{slug}}
pipeline: notebook-to-book v1.0
started: {{today}}
updated: {{today}}
mode: {{standard | quick | no-nlm}}
flags:
  deep: {{true|false}}
  audience: {{leader|engineer|both}}
  lang: {{vi|en}}
  insight_lens: [helix, forge, galaxy, ach, ip]
---
```

Progress table and Block Ledger: same schema as `codebase-to-book/_pipeline_state.md`.

---

## Data Bus — Shared File Contract

Same contract as `codebase-to-book`. P1 differences:

| File | Written By | Content |
|------|-----------|---------|
| `Phase1-Exploration/<cluster>_Exploration.md` | P1 NLM queries | Per-cluster extraction (replaces per-subsystem file) |
| `Phase1-Exploration/P1_Synthesis.md` | P1 merge | Same schema — downstream blocks read unchanged |
| `Phase1-Exploration/_nlm_query_log.md` | P1 | NLM query texts + response timestamps (for reproducibility) |

All other files (Phase2-Phase9): identical to `codebase-to-book` Data Bus.

---

## NLM Query Templates

### Discovery (P1.1)
```
"Hãy liệt kê đầy đủ: (1) các chương và phần chính trong tài liệu,
(2) 5-10 chủ đề lớn, (3) frameworks hoặc mô hình tư duy cốt lõi,
(4) loại nội dung có mặt (lý thuyết / thực hành / case study / dữ liệu / code).
Chỉ cần bản đồ cấu trúc — không cần giải thích chi tiết."
```

### Per-Cluster Base (P1.3 — query_1)
```
"Về chủ đề '[CLUSTER]':
(1) Các luận điểm chính và kết luận
(2) Frameworks, mô hình, hoặc phương pháp được trình bày
(3) Ví dụ cụ thể, case study, dữ liệu, bằng chứng
(4) Bài học thực hành và khuyến nghị hành động
(5) Điểm bất ngờ hoặc counterintuitive insights"
```

### Per-Cluster Design Decisions (P1.3 — query_2)
```
"Về '[CLUSTER]': Các quyết định thiết kế / lý do / trade-offs được thảo luận?
Tại sao tác giả chọn cách tiếp cận này thay vì alternatives?
Limitations nào được thừa nhận?"
```

### Cross-Cutting Synthesis (P1.4)
```
"Nhìn toàn bộ tài liệu:
(1) Các chủ đề xuyên suốt kết nối các phần lại?
(2) Luận điểm overarching của tác giả?
(3) Cấu trúc tư duy nền tảng (mental model, worldview)?
(4) Độc giả lý tưởng và họ sẽ thay đổi gì sau khi đọc?"
```

### Deep Extra Queries (--deep, P1.3 — queries 3-5)
```
Q3: "Về '[CLUSTER]': Chi tiết methodology, công thức, hoặc quy trình step-by-step?"
Q4: "Về '[CLUSTER]': Góc nhìn phê bình — rủi ro, edge cases, điều kiện thất bại?"
Q5: "Về '[CLUSTER]': Ứng dụng thực tế và ví dụ từ thực tiễn ngoài tài liệu?"
```

---

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — #1 rule. Không bao giờ chạy 2+ blocks trong 1 turn.
- **⛔ CỔNG DATA BUS — không có hiện vật thì KHÔNG được báo xong.** Trước mỗi CEO checkpoint, chạy:
  ```bash
  python skills/book/codebase-to-book/scripts/databus_check.py <output_dir> --phase P5
  ```
  **Mã thoát != 0 ⇒ CẤM trình checkpoint.** Làm ra hiện vật trước.
  Áp cho **mọi** pha, và đặc biệt cho **P5 · P6 · P8** — ba pha dễ bị làm "tại chỗ" rồi báo xong.

  > 🔴 **Vì sao có luật này.** Bảng Data Bus đã đặc tả `Phase5-Review.md`, `Phase6-Revised/`,
  > `Phase8-Notebook-Manifest.md` **từ đầu**. Lần chạy thật `pahl-beitz-tap2` (18 chương, 186k từ,
  > 2026-08-23) vẫn báo *"P5 ✅ · P6 ✅ · P8 ✅"* mà **không có file nào trong ba**: rà soát và hiệu
  > chỉnh được làm **tại chỗ** trên Phase4, phát hiện chỉ ghi vào `_pipeline_state.md`. CEO hỏi
  > *"không thấy thư mục Phase6?"* mới lộ.
  >
  > **Đặc tả tồn tại ≠ đặc tả được thi hành.** Cổng này biến đặc tả thành một lệnh.

- **Hiệu chỉnh tại chỗ thì PHẢI để lại danh sách thay đổi.** Nếu P6 sửa thẳng trên bản P4 thay vì
  sinh `Phase6-Revised/`, thì bắt buộc có `Phase6-Revise.md` chứa **diff đo bằng máy** so với ảnh
  chụp trước hiệu chỉnh. Không có ảnh chụp ⇒ nói thẳng là **không đối chiếu được**, đừng bỏ trống.

- **⛔ Sao lưu theo mốc phải có TÊN KHÁC NHAU — kèm GIỜ, không chỉ ngày.**
  ```bash
  cp -r <nguon>/. "<dich>_$(date +%Y-%m-%d_%H%M)/"
  ```
  `cp -r` vào **cùng một đích** không phải sao lưu — nó là **đồng bộ**, và đồng bộ thì huỷ trạng thái
  cũ. Cùng lần chạy trên, tám mốc công việc bị ghi đè thành một; bản sao lưu mang tên `_2026-08-21`
  thật ra giữ trạng thái ngày 22, mtime còn **muộn hơn bản gốc**. Một bản sao lưu mang nhãn sai
  **tệ hơn không có sao lưu** — không có thì biết mình không có điểm quay lui; có nhãn sai thì **tin**
  là có, và chỉ phát hiện khi cần dùng.

- **NLM auth failure = HALT** — Không bypass; instruct CEO `nlm login`.
- **Notebook not found = HALT** — Không guess notebook ID; present list và ask CEO.
- **Topic map CEO approval BEFORE fan-out** — tránh wasted NLM queries.
- **P1 output schema must be compatible với book-explore schema** — P2+ blocks không biết nguồn là NLM hay file.
- **P8 tạo notebook MỚI** — separate from source notebook; không overwrite source.
- **Source notebook is READ-ONLY** — chỉ query, không add/delete sources.
- **--deep escalation**: Base = 2 queries/cluster. Deep = 5 queries/cluster. Present cost before fan-out.
- **P7 default = attribution mode** — không check verbatim code trừ khi --codebase có mặt.
- **Language discipline** — `--lang vi` (default): Vietnamese narrative, English technical terms.
- **CEO checkpoints**: Không auto-continue. Minimal checkpoint nếu CEO nói "chạy hết" (1-line + "tiếp?").

---

## COD Classification

- NLM auth + notebook discovery: Offload (O2)
- Topic cluster mapping: Offload (O2) — AI proposes, CEO approves (P1.2 checkpoint)
- Topic cluster approval: **Core (C)** — affects P3 chapter granularity
- NLM fan-out queries: Offload (O2) — parallel, non-blocking
- P1 synthesis merge: Offload (O2)
- P2 thesis approval: **Core (C)** — non-delegable
- P3 outline approval: **Core (C)** — non-delegable
- P7 IP sign-off: **Core (C)** — non-delegable
- P9 insight actionability: **Core (C)** — non-delegable
- DMIR retrospective: Offload (O2) — optional enrichment

---

## Integration

```
notebook-to-book INVOKES (P1 via MCP):
  - mcp__notebooklm-mcp__refresh_auth
  - mcp__notebooklm-mcp__notebook_list
  - mcp__notebooklm-mcp__notebook_get
  - mcp__notebooklm-mcp__notebook_query (×N per cluster)

notebook-to-book DELEGATES P2-P9 TO:
  - /book-position    (P2)
  - /book-outline     (P3)
  - /book-write       (P4) [+ --codebase path if set]
  - /book-review      (P5)
  - /book-revise      (P6)
  - /book-audit       (P7) [attribution mode by default]
  - /book-notebook    (P8)
  - /book-ceo-insight (P9)

notebook-to-book READS:
  - NLM notebook (via MCP) — source of truth
  - --codebase <path> (optional) — code examples for P4

notebook-to-book WRITES TO:
  - <output_dir>/Phase1-Exploration/ — NLM extraction results
  - <output_dir>/_pipeline_state.md — pipeline state + ledger
  - <output_dir>/Phase2-Phase9/ — same as codebase-to-book
  - NotebookLM account — 1 new notebook (P8, separate from source)

FOLLOW-UP (CEO-triggered):
  - /research-to-skill → apply P9 HELIX/FORGE insights
  - /galaxy-note → create P9 Galaxy candidates
  - /convert_md_to_docx book.md → publication-ready DOCX
  - /codebase-to-book --from-pipeline → if book inspires a codebase
  - /book-to-codebase → if book should become a skill library
```
