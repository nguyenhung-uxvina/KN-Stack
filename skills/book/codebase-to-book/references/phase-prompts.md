# Phase Prompts — Task Subagent + NLM Query Templates

> Reference cho các prompt dùng khi:
> - **P1/P4:** Orchestrator spawn N parallel Task subagents (exploration + writing)
> - **P5:** Spawn 2-3 review subagents
> - **P9:** Query NotebookLM với 5 insight lenses

---

## Phase 1 — Exploration Subagent Prompt

### Template (P1 subagent — 1 agent per subsystem)

```
You are an exploration agent analyzing one subsystem of a codebase to produce raw research notes for a technical book.

SUBSYSTEM: <subsystem name>
BOUNDARY: <what's in scope — specific directories/files/modules>
CODEBASE PATH: <absolute path>
OUTPUT FILE: <path>/Phase1-Exploration/<subsystem>_Exploration.md

Your job is to read every file in the subsystem exhaustively and produce a structured analysis document. These are RESEARCH NOTES, not the final book. The writing team will rewrite them later.

Document the following sections (in this exact order):

## Architecture and Module Boundaries
- What are the main modules/files in this subsystem?
- How do they relate to each other?
- Where does this subsystem end and another begin?

## Key Abstractions
- Types, interfaces, core classes
- Purpose of each — why it exists
- Public vs internal — what's exported

## Data Flow
- How does information move through this subsystem?
- Entry points → transformations → exit points
- Shape of data at each stage

## Design Patterns
- What patterns are used? (e.g., observer, strategy, state machine, pipeline)
- Why were they chosen?
- Where do they break down?

## Integration Points
- How does this subsystem connect to others?
- What does it depend on? What depends on it?
- Contracts at boundaries (interfaces, protocols, formats)

## Surprising Decisions
- Anything non-obvious or clever?
- Code that does MORE than it looks like it does?
- Code that does LESS than it looks like it does?
- Workarounds, historical artifacts, "here be dragons" comments

## Open Questions
- What did you find but couldn't figure out?
- What would need a human expert to explain?
- What might be a bug vs intentional?

WRITING STYLE:
- Technical, direct, no marketing language
- Cite file paths and line numbers when referencing code
- Quote small snippets (≤ 3 lines) only when needed; prefer paraphrase
- Do NOT attempt to write "book-quality" prose — this is research notes

READ EVERY FILE in the subsystem. Don't skip. The book quality depends on exhaustive exploration at this phase.

When done, save output to OUTPUT FILE and return a 3-line summary: (1) files read count, (2) most important finding, (3) most surprising discovery.
```

### Parallel spawn pattern (orchestrator)

```python
# Pseudocode — orchestrator spawns N agents in single message
subsystems = preflight_output["subsystem_list"]  # e.g., 6-15 subsystems

# Single message with multiple Task tool calls
for s in subsystems:
    Task(
        description=f"Explore {s.name}",
        subagent_type="Explore",  # or "general-purpose" for heavier work
        prompt=P1_SUBAGENT_PROMPT.format(
            subsystem=s.name,
            boundary=s.boundary,
            codebase_path=args.path,
            output_path=f"{state.output_dir}/Phase1-Exploration/{s.slug}_Exploration.md",
        )
    )
# Parallel execution — all N agents run concurrently
```

---

## Phase 1 — Deep Research Variant (`--deep`)

Khi `--deep` active, sau khi base exploration xong, subagent invoke `/research --deep`:

```
You have completed base exploration of <subsystem>. Now enrich with deep research.

Invoke: /research --deep "<subsystem name> architecture and design patterns in <codebase type> systems"

Wait for completion. Then:
1. Read the research output file (3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_*.md)
2. Append to <subsystem>_Exploration.md a new section:

## Deep Research Findings

### NLM Notebook
- URL: <nlm notebook URL>
- Source tier distribution: <S/A/B/C counts>

### Cross-Source Synthesis
<3-5 insights from NLM notebook that corroborate or challenge your base exploration>

### Critical Lens Queries
<CL-1 contradictions, CL-2 assumption killers, CL-3 methodology gaps from research pipeline>

### Relevant External Patterns
<Patterns from other codebases/papers that inform this subsystem — with citations>
```

---

## Phase 4 — Writing Subagent Prompt

### Template (P4 subagent — 1 agent per chapter)

```
You are a writing agent producing ONE chapter of a publication-quality technical book.

CHAPTER: <NN> — <Title>
CHAPTER SPEC: <2-3 bullets from Phase3-Outline.md>
TARGET LENGTH: 300-800 lines
OUTPUT FILE: <path>/Phase4-Chapters/Ch<NN>_<slug>_Draft.md

CONTEXT TO READ BEFORE WRITING:
- <path>/Phase1-Exploration/<relevant>_Exploration.md (research notes for this chapter)
- <path>/Phase2-Positioning.md (audience, thesis, "why a book")
- <path>/Phase3-Outline.md (full TOC — for cross-references)
- <path>/_pipeline_state.md Block Ledger (decisions from upstream)
- References:
  - book-voice-and-style.md (tone, code rules, Apply This format)
  - chapter-template.md (exact chapter structure)
  - diagram-types.md (when to use what Mermaid type)

WRITING RULES (non-negotiable):
1. Voice: expert peer, direct, opinionated. No filler. No marketing.
2. Opening: 2-3 paragraphs (Problem → Connection to previous chapter → Promise)
3. Body: 3-5 sections, each with prose + diagram OR pseudocode OR table
4. Diagrams: 2-4 Mermaid per chapter
5. Pseudocode: 3-5 blocks, 5-15 lines each, DIFFERENT variable names from source, comment "// Pseudocode — illustrates the <pattern>"
6. Apply This: exactly 5 patterns with Name + Problem + Adaptation + Pitfall
7. Cross-references: backward to previous chapter (mandatory), forward to later chapters (optional)
8. Language: <vi | en> per --lang flag

ANTI-PATTERNS (will be flagged in P5 review):
- Verbatim source code or exact variable names
- Filler sentences ("in this chapter we will...")
- Marketing language ("elegant", "robust", "seamless")
- Concepts from later chapters that haven't been introduced
- Exact version/file counts that go stale
- Repeated rhetorical phrases

When done, save to OUTPUT FILE. Return 3-line summary: (1) line count, (2) diagram count, (3) pseudocode block count + any rule violations you're uncertain about.
```

### Parallel spawn pattern

```python
# Orchestrator — single message, N Task calls
chapters = outline["chapters"]  # e.g., 15-18 chapters

for ch in chapters:
    Task(
        description=f"Write Ch{ch.num}: {ch.title}",
        subagent_type="general-purpose",  # writing needs more context than Explore
        prompt=P4_SUBAGENT_PROMPT.format(
            chapter_num=ch.num,
            chapter_title=ch.title,
            chapter_spec=ch.spec,
            output_path=f"{state.output_dir}/Phase4-Chapters/Ch{ch.num:02d}_{ch.slug}_Draft.md",
            lang=args.lang,
        )
    )
```

---

## Phase 5 — Review Subagent Prompt

### Template (P5 — 2-3 agents, each covers a section of book)

```
You are an editorial review agent auditing a section of a technical book manuscript.

ASSIGNMENT: Chapters <N> through <M>
CHAPTER FILES: <list of Ch<NN>_<slug>_Draft.md files>
OUTPUT FILE: <path>/Phase5-Reviews/Review_Ch<N>-<M>.md

Your job is to identify concrete problems and propose specific fixes. Not "this could be better" — actionable changes with rationale.

AUDIT FRAMEWORK (evaluate each chapter):

## 1. Opening Quality
- Does it hook in the first paragraph?
- Does it connect to the previous chapter explicitly?
- Does the Promise state concrete outcomes?
- Problems: list specific sentences to rewrite

## 2. Flow
- Sections that drag, repeat earlier content, or list facts without building insight?
- Problems: flag paragraphs to cut or restructure

## 3. Content Cuts
- Reference-manual content that doesn't serve narrative?
- Code blocks too long (>20 lines)?
- Bullet lists that could be prose or tables?
- Problems: flag with "CUT: <what>, reason: <why>"

## 4. Missing Content
- Gaps where the reader would be confused?
- Missing transitions between sections?
- Problems: flag with "ADD: <what>, location: <where>"

## 5. Diagrams Needed
- Specific places where a wall of text could become a diagram?
- Describe each proposed diagram in detail (type + what to show)

## 6. Cross-Chapter Consistency
- Voice drift across chapters?
- Contradictions (Ch 5 says X, Ch 9 says not-X)?
- Terminology inconsistencies?
- Problems: list each

## 7. Specific Fixes
- 5-10 concrete sentences/paragraphs to rewrite
- For each: quote the original, suggest the replacement, give the reason

OUTPUT FORMAT:
Each problem tagged with [SEVERITY] = CRITICAL | MAJOR | MINOR
Each problem has (Chapter, line range, proposed fix, rationale)

Sort by severity within each chapter. CRITICAL issues first.
```

### Merge pattern (orchestrator compiles P5 outputs)

Orchestrator reads 2-3 review files → produces consolidated `Phase5-Review.md` sorted by severity, deduplicating overlapping issues.

---

## Phase 9 — NotebookLM Insight Query Templates

### Lens 1: HELIX Applicability

```
Query to NotebookLM:

"Trong cuốn sách này, những pattern hoặc decision nào có thể áp dụng vào Pahl-Beitz HELIX design pipeline của Workshop X? HELIX có 4 phases:

- Phase 0: Product Planning (charter, scope, initial stakeholder map)
- Phase 1: Task Clarification (requirements, abstraction, function structure)
- Phase 2: Conceptual Design (morphological matrix, concept variants, selection)
- Phase 3: Embodiment Design (layout, DfX, ICD v2, BOM)
- Phase 4: Detail Design (drawings, final BOM, inspection, assembly)

Liệt kê insights theo phase. Mỗi insight structure:
- Pattern/decision name từ sách (citation chapter)
- HELIX phase áp dụng được
- Cách map cụ thể (1-2 câu)
- Skill hiện có cần upgrade (nếu biết — ví dụ: /helix-p1-requirements, /helix-p2-search)

Nếu insight không fit HELIX thì ghi 'N/A — no HELIX parallel'."
```

### Lens 2: FORGE Transfers

```
"FORGE là hệ thống product strategy của Workshop X, gồm:
- forge-portfolio: dashboard portfolio sản phẩm
- forge-shift: ACH (AI-Compensates-Hardware) go/no-go assessment
- forge-scout: scan ACH opportunities
- forge-cost: cost envelope + LCC
- forge-trust: customer trust evidence
- forge-validate: validation infrastructure
- forge-library: AI model library (cross-product transfer)
- forge-job-map: ODI + JTBD
- forge-evolve: competitive moat
- forge-market-intel: competitor monitoring

Những framework product strategy hoặc portfolio positioning nào trong sách có thể transfer vào FORGE? Mỗi transfer:
- What (framework name từ sách + chapter citation)
- How (cách áp dụng cụ thể 1-2 câu)
- Which FORGE skill to upgrade

Prioritize insights có ROI cao (applicable ngay vs theoretical-only)."
```

### Lens 3: Galaxy Candidates

```
"Galaxy là hệ thống Zettelkasten của Workshop X — atomic permanent notes với ≥2 wikilinks mỗi note. Hiện có ~160 notes.

Identify 5-10 atomic concepts trong sách xứng đáng thành Galaxy permanent notes. Mỗi concept:
- Proposed note title (ngắn gọn, describes concept)
- Atomic level check (1 concept? hay cần split thành nhiều note?)
- 1-2 wikilinks đến Galaxy notes hiện có (nếu biết — nếu không ghi '[needs connection research]')
- Tag đề xuất (chọn từ #type/permanent-note + #sys / #pahl / #ceo / #meta / #defense)
- 1-câu tóm tắt insight

Loại trừ concepts đã quá phổ biến (e.g., 'separation of concerns'). Chỉ recommend concepts non-obvious hoặc có wording đặc biệt tốt trong sách."
```

### Lens 4: ACH Transfer Opportunities

```
"ACH (AI-Compensates-Hardware) là thesis của Workshop X: dùng AI để bù cho giới hạn hardware (sensor cheap, compute edge, mechanical tolerance loose...) — giữ chất lượng end-product.

Workshop X products applying ACH:
- BB-01 LOMAH (piezo sensor + AI detection)
- V-SMASH (low-cost sensor + classification)
- MTB-20 (mechanical simplification + AI correction)
- TDR (edge AI)
- VN-XUONG-UUV (future — sonar + AI)

Identify pattern trong sách relevant đến ACH — những nơi sách cho thấy cách AI compensate cho hardware limit / sensor noise / compute constraint / mechanical tolerance. Mỗi pattern:
- Pattern từ sách (chapter citation)
- ACH mapping (hardware limit nào AI đang compensate?)
- Product applicable (BB-01 / V-SMASH / MTB-20 / TDR / UUV / multiple)
- ACH readiness (can deploy now / needs research / speculative)"
```

### Lens 5: IP Exposure Map

```
"Workshop X sản xuất defense products cho Vietnamese military. IP protection concerns:
- Export control (MIL-STD, STANAG coupling)
- Trade secret (specific algorithms, calibration, test data)
- Publishable (methodology, process discipline, generic patterns)

Rate mỗi chapter trong sách:
- SAFE — Có thể public (methodology, systems thinking, generic patterns)
- REVIEW — Cần CEO đọc trước khi chia sẻ external (có specific architecture details nhưng không phải IP core)
- SENSITIVE — Không nên public, chỉ dùng internal training (exact algorithms, sensor calibration, performance data)

Cho mỗi chapter:
- Chapter number + title
- Rating (SAFE / REVIEW / SENSITIVE)
- Rationale (1-2 câu — cái gì trong chapter drive rating này)
- Redaction suggestion nếu REVIEW/SENSITIVE (cái gì cụ thể cần mask)"
```

### Output aggregation (orchestrator)

Sau khi 5 queries xong, orchestrator compile vào `Phase9-CEO-Insights.md`:

```python
# Pseudocode
results = {}
for lens in ["helix", "forge", "galaxy", "ach", "ip"]:
    response = mcp__notebooklm_mcp__notebook_query(
        notebook_id=state.notebook_id,
        query=LENS_PROMPTS[lens],
    )
    results[lens] = response

# Compile structured output
render_ceo_insights_md(
    book_title=state.book_title,
    notebook_id=state.notebook_id,
    sections=results,
    output=f"{state.output_dir}/Phase9-CEO-Insights.md",
)
```

---

## Notes on prompt design

**Why these prompts are long:** Task subagents don't see the orchestrator's conversation. They need complete context in the prompt — goal, constraints, output format, file paths, references to consult, anti-patterns to avoid. A terse prompt = shallow generic output.

**Why NLM queries are specific to WX:** Generic query like "what are key insights from this book?" returns textbook answers. Lens queries grounded in Workshop X's actual systems (HELIX, FORGE, ACH, Galaxy, IP) surface insights the CEO can actually act on.

**Language of prompts:** Prompts to Task subagents có thể bilingual (English instruction + Vietnamese content rules). Prompts to NLM dùng tiếng Việt vì NLM handles Vietnamese tốt và output sẽ merge với rest of Phase9-CEO-Insights.md (tiếng Việt).
