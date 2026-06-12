---
name: book-notebook
description: "Block P8 của codebase-to-book pipeline — tạo NotebookLM notebook cho sách vừa compile, chunk book.md theo chapter, ingest từng chunk làm source riêng để NLM retrieve chính xác. Upload thêm meta-sources (outline + audit log). Verify ingest count. CEO test query trước khi sang P9. Dùng mcp__notebooklm-mcp MCP tools. Can run standalone. Triggers on: 'nlm book', 'notebooklm build', 'ingest book', 'tạo notebook sách', 'P8 book'."
---

# Block P8: NotebookLM Build + Full-Book Ingest

> **Pipeline:** codebase-to-book → Block P8
> **Input:** `book.md` (final, CEO-signed từ P7) + `Phase7-Audit-Log.md`
> **Output:** `Phase8-Notebook-Manifest.md` (notebook ID + URL + source log)
> **MCP:** `mcp__notebooklm-mcp__*` tools

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Verify NLM auth valid before operations | Attempt ingest if `nlm login` expired — HALT instead |
| Create notebook titled "Book: <slug> — <thesis>" | Overwrite existing notebook without CEO confirmation |
| Chunk book.md by chapter (respects NLM source size limits) | Upload whole book as single source (exceeds limits) |
| Upload each chapter as separate source (parallel MCP calls) | Skip chapters because "too small" — all chunks go in |
| Upload meta-sources (Outline, Audit Log) | Run analysis queries (= P9) |
| Verify source count matches expected | Create studio artifacts (= P9 optional) |

**Multi-Agent Mode:** NO — but MCP source_add calls run parallel (multiple tool calls in single message).
**CEO Checkpoint:** CEO opens notebook URL, tests 1-2 queries, confirms before P9.

## Standalone Usage
```
/book-notebook <codebase-slug>
```

Pre-conditions:
- `book.md` exists in output dir (P7 complete)
- `nlm login` valid session (if expired, skill HALT with instruction)

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P7 complete + CEO IP sign-off
- `book.md` — compiled book
- `Phase7-Audit-Log.md` — for metadata + research sources context
- `Phase3-Outline.md` — for metadata + TOC

## Workflow

### Step P8.1: Pre-Flight NLM Auth

```
NLM AUTH PRE-CHECK
  → Call mcp__notebooklm-mcp__refresh_auth
  
  If success:
    → Proceed to P8.2
  If failure:
    → HALT với message:
       "⚠️  NotebookLM auth expired. Anh chạy trong terminal:
           nlm login
        Xong rồi: /codebase-to-book <slug> --from P8"
```

### Step P8.2: Check for Existing Notebook

```python
# Pseudocode — avoid accidental overwrite
notebooks = mcp__notebooklm-mcp__notebook_list()

existing = find_by_title_prefix(notebooks, f"Book: {slug}")
if existing:
    # CEO checkpoint
    present_to_ceo(f"""
    ⚠️  Notebook đã tồn tại: {existing.title}
    URL: {existing.url}
    Sources: {existing.source_count}
    
    CEO:
    (1) ➕ Tạo notebook mới (song song) 
    (2) 🔄 Overwrite — xóa notebook cũ và tạo lại
    (3) ⏭️ Skip P8 — dùng notebook cũ cho P9
    (4) ⏸️ Dừng
    """)
    wait_for_ceo_response()
```

### Step P8.3: Create Notebook

```python
# Pseudocode
thesis_short = extract_thesis_first_sentence(positioning.thesis)[:60]
notebook_title = f"Book: {slug} — {thesis_short}"

notebook = mcp__notebooklm-mcp__notebook_create(
    title=notebook_title,
)

notebook_id = notebook.id
notebook_url = notebook.url
```

### Step P8.4: Chunk book.md by Chapter

```bash
# Bash — split book.md on chapter headings
# NLM performs best với sources ≤ ~50KB (~10k words)

# Detect chapter markers — usually "^## Chapter" or "^# Chapter"
awk '
  /^# Chapter [0-9]+:/ || /^## Chapter [0-9]+:/ {
    if (out) close(out)
    n = $0
    gsub(/[^a-zA-Z0-9]+/, "-", n)
    out = sprintf("chunks/chapter-%02d-%s.md", ++count, substr(n, 1, 40))
  }
  { if (out) print > out }
' book.md
```

Alternative (if book uses different chapter heading style): use Python/TS script with regex.

```python
# Pseudocode — chunk script
import re

content = read("book.md")
chunks = re.split(r'^#+ Chapter (\d+)', content, flags=re.MULTILINE)
# chunks[0] = frontmatter + preface + TOC + Part I intro
# chunks[1] = chapter 1 num, chunks[2] = chapter 1 content, etc.

output = []
# First chunk: preface + frontmatter
output.append({
    "title": "Preface + TOC + Part Intros",
    "content": chunks[0],
})

for i in range(1, len(chunks), 2):
    ch_num = chunks[i]
    ch_content = f"# Chapter {ch_num}" + chunks[i+1]
    title = extract_first_heading(ch_content)
    output.append({
        "title": f"Ch{ch_num.zfill(2)} — {title}",
        "content": ch_content,
    })

write_chunks_to_disk(output, f"{output_dir}/chunks/")
```

### Step P8.5: Ingest Chapter Chunks (Parallel)

Upload each chunk as separate NLM source. Single message with multiple `source_add` calls:

```python
# Pseudocode — parallel ingest
ingest_results = []
for chunk in chunks:
    # Each tool call in single orchestrator message
    result = mcp__notebooklm-mcp__source_add(
        notebook_id=notebook_id,
        source_type="text",
        text=chunk.content,
        # Some MCP implementations support title/metadata:
        # title=chunk.title,
    )
    ingest_results.append({
        "chunk_title": chunk.title,
        "source_id": result.source_id if result.success else None,
        "size_bytes": len(chunk.content),
        "status": "ok" if result.success else f"failed: {result.error}",
    })
```

### Step P8.6: Ingest Meta-Sources

Upload supporting documents làm meta-sources:

```python
# Meta-source 1: Book outline (for retrieval of chapter structure)
mcp__notebooklm-mcp__source_add(
    notebook_id=notebook_id,
    source_type="text",
    text=read(f"{output_dir}/Phase3-Outline.md"),
)

# Meta-source 2: Audit log (research sources + IP ratings context)
mcp__notebooklm-mcp__source_add(
    notebook_id=notebook_id,
    source_type="text",
    text=read(f"{output_dir}/Phase7-Audit-Log.md"),
)

# Meta-source 3: Positioning (thesis + audience + glossary — grounds NLM queries)
mcp__notebooklm-mcp__source_add(
    notebook_id=notebook_id,
    source_type="text",
    text=read(f"{output_dir}/Phase2-Positioning.md"),
)
```

### Step P8.7: Verify Ingest

```python
# Pseudocode
describe = mcp__notebooklm-mcp__notebook_describe(notebook_id=notebook_id)

expected_count = len(chunks) + 3  # chapters + 3 meta-sources
actual_count = describe.source_count

if actual_count != expected_count:
    flag_for_ceo(
        f"⚠️  Ingest mismatch: expected {expected_count}, got {actual_count}. "
        f"Check Phase8-Notebook-Manifest.md for per-source status."
    )
```

### Step P8.8: Write Phase8-Notebook-Manifest.md

```markdown
---
notebook_id: {{nlm-uuid}}
notebook_url: https://notebooklm.google.com/notebook/{{uuid}}
notebook_title: {{title}}
created: {{date}}
source_count: {{N}}
book_slug: {{slug}}
---

# NotebookLM Manifest — {{slug}}

## Notebook
- **Title:** {{notebook_title}}
- **ID:** `{{notebook_id}}`
- **URL:** {{notebook_url}}
- **Created:** {{date}}
- **Source count:** {{N}} ({{chapter_chunks}} chapter chunks + {{meta_count}} meta-sources)

## Sources Ingested

### Chapter Chunks
| # | Title | Size | Source ID | Status |
|---|-------|------|-----------|--------|
| 1 | Preface + TOC + Part Intros | {{KB}} | `{{source_id}}` | ✅ |
| 2 | Ch01 — {{title}} | {{KB}} | `{{source_id}}` | ✅ |
| 3 | Ch02 — {{title}} | {{KB}} | `{{source_id}}` | ✅ |
| ... |

### Meta-Sources
| # | Title | Purpose | Status |
|---|-------|---------|--------|
| N+1 | Phase3-Outline.md | Book structure retrieval | ✅ |
| N+2 | Phase7-Audit-Log.md | Research sources + IP context | ✅ |
| N+3 | Phase2-Positioning.md | Thesis + glossary grounding | ✅ |

## Ingest Log
[Raw output from MCP tool calls — for debugging if re-run needed]

## CEO Verification Instructions
Trước khi P9 chạy, anh mở notebook URL và test 2 câu hỏi:

1. **Query structure:** "Liệt kê các parts và chapters trong sách này"
   - Expected: NLM retrieves từ Phase3-Outline.md meta-source, trả lời đầy đủ

2. **Query content:** "Chapter 3 dạy những gì?" (thay 3 bằng chapter phù hợp)
   - Expected: NLM retrieves từ chapter chunk, tóm tắt key patterns + Apply This

Nếu 2 queries OK → approve P9.
Nếu failure → P8 re-run hoặc re-chunking.
```

### Step P8.9: Update Pipeline State + Ledger

```markdown
### P8 — NotebookLM Build (<date>)
**Key findings:**
- Notebook created: {{notebook_id}}
- URL: {{notebook_url}}
- Sources ingested: {{N}} ({{chapters}} chapters + {{meta}} meta-sources)
- Ingest failures: {{X}} (if any — details in manifest)

**Decisions for downstream:**
- P9 will query notebook_id {{id}} với 5 insight lenses
- Optional studio artifacts postponed to P9 checkpoint

**Open questions:**
- CEO verification pending — test queries

**CEO checkpoint result:** [pending — awaiting NLM URL test]
```

## Output

Save to `{{output_dir}}/`:
- `Phase8-Notebook-Manifest.md`
- `chunks/` subfolder với chapter chunks (preserve for re-ingest if needed)

Update: `{{output_dir}}/_pipeline_state.md`.

## CEO Checkpoint (BLOCKING — test query verification)

```
═══ BLOCK P8 NOTEBOOKLM BUILD COMPLETE ═══

NotebookLM URL: {{notebook_url}}

Sources ingested: {{N}}
  - Chapter chunks: {{N_chapters}}
  - Meta-sources: {{N_meta}}
Failures: {{N_fail}} (details in Phase8-Notebook-Manifest.md)

Next step requires CEO verification:

👉 Anh mở URL và test 2 câu hỏi:
   1. "Liệt kê parts và chapters trong sách"
   2. "Chapter {{X}} dạy gì?"

Nếu NLM trả lời chính xác với citations từ sources → approve.
Nếu NLM không retrieve được → có issue với ingest, cần re-run.

Deliverables:
  - {{output_dir}}/Phase8-Notebook-Manifest.md
  - {{output_dir}}/chunks/ ({{N_chapters}} files)

CEO:
(1) ✅ Test OK → tiếp tục Block P9 (CEO Insight)
(2) 🔄 Re-run P8 — ingest issue: [specify]
(3) 🔄 Change chunking strategy: [finer/coarser]
(4) ⏸️ Dừng — skip P9 (no NLM insights needed)
═══════════════════════════════════════════════════
```

## COD Classification

- Auth pre-check: Offload (O2)
- Existing notebook detection: Offload (O2) — CEO if conflict
- Notebook creation: Offload (O2)
- Chunking: Offload (O2)
- MCP source_add (parallel): Offload (O2)
- Ingest verification: Offload (O2)
- **CEO test query verification: Core (C)** — human confirms NLM works before P9

## Rules

- **Never auto-overwrite existing notebook** — CEO gate mandatory
- **Chunk by chapter, not arbitrary size** — retains semantic boundaries for NLM retrieval
- **Meta-sources always uploaded** — Outline + Audit Log + Positioning make NLM queries more accurate
- **NLM auth failure = HALT** — instruct CEO run `nlm login`, don't bypass
- **Preserve chunks on disk** — if NLM ingest fails partially, re-run without re-chunking
- **Single message parallel source_add** — not sequential (slower + hits rate limits)
- **If ingest mismatch (expected vs actual count)** — flag for CEO, show per-source status, don't proceed silent
- **Chunk size target 30-50KB** — small enough for NLM retrieval precision, large enough to preserve chapter coherence
- **Notebook title format: "Book: {{slug}} — {{thesis_short}}"** — discoverable in NLM UI alongside other notebooks
- **Don't delete book.md or chunks after ingest** — anh có thể cần re-ingest later
