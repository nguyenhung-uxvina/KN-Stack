---
name: book-audit
description: "Block P7 của codebase-to-book pipeline — audit final book cho verbatim source code, replace với pseudocode khác variable names. Scan cho proprietary prompt text, internal constants, exact function implementations. Rate per-chapter IP exposure (SAFE/REVIEW/SENSITIVE). Compile final book.md. CEO Core — IP sign-off non-delegable. Can run standalone. Triggers on: 'book audit', 'source audit', 'IP check', 'sanitize', 'pseudocode replace', 'P7 book', 'compile book'."
---

# Block P7: Source Code Audit + Book Compilation

> **Pipeline:** codebase-to-book → Block P7
> **Input:** `Phase6-Revised/Ch*_v2.md` + original codebase path
> **Output:** `Phase7-Audit-Log.md` + `book.md` (final compiled book)
> **Nature:** **CEO Core** — IP sign-off non-delegable

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Compare each code block in book against source | Rewrite content (= P6, done) |
| Replace verbatim matches với pseudocode, different variable names | Delete code blocks entirely (removes teaching value) |
| Scan for proprietary prompt text, internal constants | Audit non-code content (already done in P5) |
| Annotate type signatures với `// Illustrative` | Change book structure |
| Rate per-chapter IP exposure (SAFE/REVIEW/SENSITIVE) | Make publication decision — CEO does that |
| Compile chapters into single `book.md` với frontmatter + TOC | Auto-publish or distribute |
| Catalog research sources (NLM notebooks if --deep) | Edit source code |

**Multi-Agent Mode:** NO — audit requires consistent cross-chapter view.
**CEO Checkpoint:** BLOCKING — IP rating + final sign-off before P8.

## Standalone Usage
```
/book-audit <codebase-slug>
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P6 complete
- `Phase6-Revised/Ch*_v2.md` × N — chapters to audit
- Original codebase path — for verbatim comparison
- `Phase3-Outline.md` — for TOC compilation
- `Phase2-Positioning.md` — for frontmatter (thesis, audience)

## Workflow

### Step P7.1: Extract Code Blocks from All Chapters

```python
# Pseudocode — extract code blocks
code_blocks = []
for chapter_file in glob(f"{output_dir}/Phase6-Revised/Ch*_v2.md"):
    content = read(chapter_file)
    for block in extract_code_blocks(content):
        code_blocks.append({
            "chapter": extract_chapter_num(chapter_file),
            "block_id": generate_block_id(),
            "lang": block.language,
            "content": block.content,
            "location": block.line_number,
            "comment_label": block.first_line_comment,  # should contain "Pseudocode" marker
        })
```

### Step P7.2: Verbatim Match Detection

For each code block, scan source codebase for similarity:

```python
# Pseudocode — verbatim detection
source_files = glob(f"{codebase_path}/**/*.{py,ts,js,rs,go,c,cpp,java,rb}")

for block in code_blocks:
    matches = []
    for src_file in source_files:
        if is_language_match(block.lang, src_file):
            similarity = detect_similarity(block.content, read(src_file))
            # Heuristic: ≥70% token overlap on sliding window of 5+ lines
            if similarity.score >= 0.7:
                matches.append({
                    "source_file": src_file,
                    "source_lines": similarity.location,
                    "score": similarity.score,
                    "exact_tokens": similarity.shared_tokens,
                })
    
    block["verbatim_matches"] = matches
    block["needs_replacement"] = len(matches) > 0
```

Detection heuristics:
- **Token-level similarity** — same variable names, same function signatures
- **Structural similarity** — same line-by-line logic even if vars renamed slightly
- **Constant matching** — magic numbers, regex patterns, string constants from source
- **Comment matching** — docstrings or inline comments copied from source

### Step P7.3: Replace Verbatim with Pseudocode

For each flagged block, produce replacement:

```python
# Pseudocode — replacement rules
def sanitize_block(block):
    new_block = block.content
    
    # Rule 1: Rename identifiers
    new_block = rename_identifiers(new_block, use_generic_names=True)
    # "config_manager" → "configRegistry" or similar
    
    # Rule 2: Remove proprietary strings
    new_block = strip_exact_strings(new_block, source_strings)
    # Replace with placeholder: "<system prompt text>"
    
    # Rule 3: Generalize constants
    new_block = generalize_constants(new_block)
    # 42 stays (generic); specific magic values replaced with named constant
    
    # Rule 4: Simplify multi-line patterns
    if line_count(new_block) > 15:
        new_block = extract_pattern_core(new_block, target_lines=10)
    
    # Rule 5: Add "Pseudocode" label
    new_block = prepend_comment(new_block, "// Pseudocode — illustrates the pattern")
    
    # Rule 6: Different language if original exact
    # Optional: if Python source, show in TypeScript to emphasize pattern not implementation
    
    return new_block
```

### Step P7.4: Proprietary Content Scan

Beyond code blocks, scan prose for:

- **Exact prompt text** copied from source (if codebase is AI/agent system)
- **Internal constants** (API endpoints, bucket names, internal IDs)
- **Exact error messages** from source
- **Specific performance numbers** tied to one deployment

Flag for CEO review. Don't auto-replace prose (too risky).

### Step P7.5: Per-Chapter IP Exposure Rating

Rate each chapter:

- **SAFE** — Methodology, patterns, rationale. Can publish externally (open source, blog, training material).
- **REVIEW** — Specific architecture details not IP-core, but CEO should read before external sharing. Internal training yes, external gated.
- **SENSITIVE** — Exact algorithms, sensor calibration, performance data, IP core. Internal training only, never external.

For Workshop X defense context:

```
IP EXPOSURE RATING FRAMEWORK

SAFE indicators:
  ✅ Generic design patterns (observer, state machine)
  ✅ Cross-industry methodologies (CI/CD, RESTful design)
  ✅ High-level architecture diagrams without implementation specifics
  ✅ Rationale about trade-offs
  ✅ Apply This patterns transferable to other systems

REVIEW indicators:
  ⚠️ Specific module boundaries revealing product architecture
  ⚠️ Integration patterns with named internal systems
  ⚠️ Data schemas
  ⚠️ Non-core algorithms tailored to product

SENSITIVE indicators:
  🔴 Specific sensor calibration values / tolerances
  🔴 Exact AI model architectures + hyperparameters
  🔴 Defense-specific thresholds (detection accuracy, FAR/FNR)
  🔴 MIL-STD / STANAG specific test results
  🔴 Performance numbers tied to deployed units
  🔴 Counter-measures or jamming resistance details
```

### Step P7.6: Research Sources Catalog (if --deep was used)

Compile NLM notebooks consulted:

```markdown
## Research Sources (--deep mode)

### NLM Notebooks Created
| Notebook | Topic | Tier Distribution | Chapters Cited |
|----------|-------|------------------|----------------|
| <notebook_id_1> | <topic> | S:2, A:5, B:3 | Ch 3, Ch 7 |
| <notebook_id_2> | ... | ... | Ch 10 |

### External Citations
| Citation | Source Tier | Chapter |
|----------|-------------|---------|
| [Paper title by Author, Year] | S | Ch 3 |
| ... |
```

### Step P7.7: Compile book.md

After sanitization, compile final book:

```python
# Pseudocode — book compilation
book_content = []

# Frontmatter
book_content.append(render_frontmatter(
    title=thesis_title,
    subtitle=thesis_subtitle,
    date=today,
    audience=positioning.audience,
    thesis=positioning.thesis,
    language=args.lang,
))

# Preface (auto-generated from positioning)
book_content.append(render_preface(positioning))

# Table of Contents (auto-generated from outline)
book_content.append(render_toc(outline))

# Parts + chapters
for part in outline.parts:
    book_content.append(f"# Part {part.num}: {part.title}")
    book_content.append(f"> {part.epigraph}")
    for ch in part.chapters:
        ch_content = read(f"{output_dir}/Phase6-Revised/Ch{ch.num:02d}_{ch.slug}_v2.md")
        book_content.append(ch_content)

# Epilogue (if applicable)
# Already part of last chapter per outline

# Appendix: Apply This Catalog (aggregated all 5×N patterns)
book_content.append(render_apply_this_catalog(all_chapters))

# Appendix: Glossary
book_content.append(render_glossary(positioning.glossary))

# Appendix: Research Sources (if --deep)
if args.deep:
    book_content.append(render_research_sources(audit.sources))

write(f"{output_dir}/book.md", "\n\n".join(book_content))
```

### Step P7.8: Write Phase7-Audit-Log.md

```markdown
# Phase 7 Audit Log — {{slug}}
Date: {{today}}
Chapters audited: {{N}}
Code blocks audited: {{total_blocks}}

## Verbatim Match Summary
| Match Type | Count | Disposition |
|-----------|-------|-------------|
| Exact copies (score ≥ 0.9) | {{N}} | All replaced with pseudocode |
| Near-copies (0.7-0.9) | {{M}} | All replaced |
| Paraphrased (< 0.7) | {{K}} | Annotated as "// Illustrative" |

## Replacements Applied
| Chapter | Block ID | Source File | Similarity | Replacement Strategy |
|---------|----------|-------------|-----------|---------------------|
| Ch 3 | B3.1 | src/dispatcher/core.py:45-78 | 0.85 | Renamed identifiers, trimmed to 12 lines |
| Ch 3 | B3.2 | src/dispatcher/queue.py:12-30 | 0.72 | Language swap (Py → TS pseudo), generalized constants |
| ... |

## Proprietary Content Flags
| Chapter | Line Range | Type | CEO Decision |
|---------|-----------|------|--------------|
| Ch 5 | 234-240 | Exact error message | Replaced with generic |
| Ch 8 | 102 | Specific performance number | Changed to "roughly X" |
| ... |

## Per-Chapter IP Exposure Rating

### Overall distribution
- SAFE: {{N}} chapters
- REVIEW: {{M}} chapters
- SENSITIVE: {{K}} chapters

### Per-Chapter
| Chapter | Rating | Rationale | Redaction if non-SAFE |
|---------|--------|-----------|----------------------|
| Ch 1 | SAFE | Generic startup patterns | - |
| Ch 2 | REVIEW | Specific event queue architecture | Don't share external without CEO OK |
| Ch 7 | SENSITIVE | Sensor fusion algorithm details | Internal only — redact sections X, Y |
| ... |

## Research Sources (if --deep)
[Per P7.6]

## Compilation Output
- Final book.md: {{output_dir}}/book.md
- Total lines: {{N}}
- Word count estimate: {{M}}
- Page equivalent (~250 words/page): ~{{pages}} pages
```

### Step P7.9: Update Pipeline State + Ledger

```markdown
### P7 — Audit + Compile (<date>)
**Key findings:**
- Code blocks audited: {{N}}
- Verbatim matches replaced: {{M}} ({{pct}}% of blocks)
- IP ratings: {{safe}} SAFE / {{review}} REVIEW / {{sensitive}} SENSITIVE
- book.md compiled: {{N_lines}} lines / ~{{pages}} pages

**Decisions for downstream:**
- P8 NotebookLM ingest: chunk by chapter (N chunks ready)
- CEO external sharing gate: chapters rated REVIEW/SENSITIVE stay internal
- Research sources cataloged for P9 context

**Open questions:**
- CEO must confirm IP ratings: [any chapters CEO wants to change]

**CEO checkpoint result:** [pending]
```

## Output

Save to `{{output_dir}}/`:
- `Phase7-Audit-Log.md`
- `book.md` (final compiled book)

Update: `{{output_dir}}/_pipeline_state.md`.

## CEO Checkpoint (BLOCKING — IP sign-off is Core)

```
═══ BLOCK P7 AUDIT + COMPILE COMPLETE ═══
Code blocks audited: {{total}}
Verbatim matches: {{found}} → all replaced với pseudocode
Proprietary content flags: {{N}} → CEO-reviewed

IP Exposure:
  🟢 SAFE: {{n}} chapters — publishable external
  🟡 REVIEW: {{n}} chapters — CEO gate required
  🔴 SENSITIVE: {{n}} chapters — internal only

Compiled book: {{output_dir}}/book.md
  Lines: {{N}}
  Chapters: {{M}}
  Page equivalent: ~{{P}} pages

Deliverables:
  - {{output_dir}}/Phase7-Audit-Log.md
  - {{output_dir}}/book.md

CEO IP sign-off:
(1) ✅ Approve IP ratings → tiếp tục Block P8 (NotebookLM)
(2) 🔄 Re-rate chapter [X] from [Y] to [Z] — reason: [specify]
(3) 🔄 Additional sanitization for chapter [X]: [specify]
(4) ⏸️ Dừng — CEO cần read book.md end-to-end trước publishing
(5) 🏁 Final (skip P8/P9 — CEO chọn không build NLM)
═══════════════════════════════════════════════════
```

## COD Classification

- Code block extraction: Offload (O2)
- Verbatim detection: Offload (O2)
- Sanitization replacement: Offload (O2)
- Proprietary content flagging: Offload (O2) — AI detects, CEO confirms
- IP rating proposal: Offload (O2) — AI drafts, CEO confirms
- **IP sign-off: Core (C)** — non-delegable
- Book compilation: Offload (O2)
- Research sources catalog: Offload (O2)

## Rules

- **Verbatim replacement is NON-NEGOTIABLE** — no exceptions. Even "short" code blocks matching source get replaced.
- **Teaching value preserved** — don't delete code blocks. Replace with pseudocode. Reader still learns pattern.
- **Different language sometimes clearer** — if source is Python, showing pattern in TS/pseudo-Python emphasizes "this is the pattern, not the code"
- **Proprietary strings auto-flagged, CEO confirms replacement** — some strings may be legitimately educational
- **IP rating is CEO-driven, AI advises** — defense context means CEO knows sensitivity better than AI
- **SENSITIVE chapters compiled but marked** — they're IN book.md with clear "INTERNAL ONLY" frontmatter flag. Distribution wrapper decides what to share.
- **Research sources catalog immutable** — NLM notebook IDs cited in book. P8 ingests book and links back.
- **If --deep was used** — notebooks from P1 + P4 research carry forward as supporting sources in P8 (option)
- **book.md is final format** — P8 ingests it, P9 queries it, CEO shares (gated by ratings). No further editing expected.
