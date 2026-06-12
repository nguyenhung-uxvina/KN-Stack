# Source Prompt — "Turn Any Codebase Into a Technical Book"

> **Source:** Anh THỊNH cung cấp 2026-04-24 từ tài liệu `analyze-codebase-to-book.md`.
> **Case study gốc:** 36 agents × 7 phases × 6 giờ → "Claude Code from Source" 18 chương / 6,271 dòng / ~400 trang. Sanitized từ source maps leaked qua npm.
> **Mục đích lưu tại đây:** traceability — để downstream skill hoặc người đọc biết nguyên văn prompt gốc để so sánh với implementation.

---

## Prompt gốc

```
I want you to analyze the source code at [path] and produce a comprehensive
technical book about its architecture, patterns, and internals.

The book should read like a professional technical publication — the kind of
book a senior engineer would buy to deeply understand a system. Not documentation.
Not a tutorial. A book that teaches how the system works, why each decision was
made, and what patterns the reader can steal for their own projects.
```

## Phase 1: Exploration

Launch parallel agents (one per major subsystem) to read every file in the codebase exhaustively. Each agent should document:

- Architecture and module boundaries
- Key abstractions (types, interfaces, core classes)
- Data flow (how information moves through the system)
- Design patterns (what patterns are used and why)
- Integration points (how this module connects to others)
- Surprising decisions (anything non-obvious or clever)

Produce a raw analysis document per subsystem. These are research notes, not the final book.

## Phase 2: Audience and Positioning

Before structuring the book, define:

**Primary audience** — Dual-reader model:
- Technical leaders (architecture + rationale; can skip code blocks and deep-dive sections)
- Senior engineers (implementation-level understanding; read everything)

**Core thesis** — The ONE big insight. Every chapter connects back. Usually:
> "Here is the architectural bet this system makes, and here is how every subsystem serves that bet."

**What makes it worth a book** — Not just: "read the source." The book's value:
- Narrative (the source has no narrative)
- Cross-cutting patterns (scattered across files in the source)
- Design rationale (not in the code at all)
- Transferable lessons (require synthesis the source can't provide)

## Phase 3: Structure

Organize the book as if the reader were building the system from scratch. Each chapter solves ONE clear problem that the next chapter depends on. The reader should never encounter a concept that requires a later chapter to understand.

**Parts** — Group chapters into 5-7 thematic parts. Each part has a one-line epigraph.

**Chapter ordering principles:**
- Foundations first (startup, state, communication with external services)
- Core loop next (the main execution cycle — usually the most important chapter)
- Capabilities built on the core (tools, plugins, extensions)
- Advanced patterns (multi-agent, orchestration, coordination)
- Supporting infrastructure (UI, networking, persistence)
- Performance and optimization last (you can't optimize what you don't understand)
- Epilogue: synthesis, transferable lessons, forward look

**Chapter sizing** — 300-800 lines per chapter. Over 800 = split. Under 200 = merge.

Present full outline with part names, chapter titles, 2-3 bullets per chapter. Get approval BEFORE writing.

## Phase 4: Writing

Write each chapter FROM SCRATCH using Phase 1 analysis as research notes. Do NOT restructure the analysis — rewrite as narrative prose.

### Chapter Template

1. **Opening** (2-3 paragraphs)
   - What problem does this layer/subsystem solve?
   - Why does it exist? What would break without it?
   - How does it connect to what the reader already knows? (explicit backward reference)
   - What will the reader understand by the end?

2. **Body**
   - Mix of prose, diagrams, code snippets, tables
   - Prose for narrative and rationale ("why")
   - Diagrams for architecture, data flow, state machines
   - Code for key patterns (pseudocode only — see rules)
   - Tables for reference material

3. **Deep Dive sections** (optional, inline)
   - Callout sections that leaders can skip
   - "How does this actually work at the byte level"
   - Readable independently without losing narrative

4. **Apply This** (closing)
   - Exactly 5 transferable patterns
   - Each: name → what problem it solves → how to adapt it → pitfall to watch for
   - Vary format slightly between chapters

### Voice and Tone

- **Expert peer** — Senior engineer doing deep technical review for a colleague
- **Direct and opinionated** — "This is clever because..." / "This is the wrong abstraction for..."
- **No filler** — Every sentence teaches or sets up the next thing that teaches
- **Show trade-offs** — Explain what was NOT built and why

### Code Blocks

- **Pseudocode only** — Never reproduce exact source code. Show PATTERN, not implementation.
- **3-5 blocks per chapter max**, each 5-15 lines
- **Different variable names** — Generic, not exact identifiers
- **Label as illustrative** — `// Pseudocode — illustrates the pattern`
- **Context before and after** — One sentence before (WHAT), one paragraph after (WHY)

### Diagrams

- **Mermaid format** — ```mermaid fenced code blocks
- **Every architectural concept gets a diagram**
- Types: `graph TD` / `graph LR` / `sequenceDiagram` / `stateDiagram-v2` / `flowchart TD` / `gantt`
- **2-4 diagrams per chapter**

### Cross-References

- Explicit backward reference at chapter start
- Forward references: "Chapter N covers this in depth"
- Each concept has ONE canonical home — other chapters reference, not re-explain

### Consistency

- No repeated rhetorical phrases across chapters
- Standardized "Apply This" format (5 patterns)
- No exact file counts or version numbers (go stale)
- Consistent terminology

## Phase 5: Editorial Review

Launch 2-3 review agents, each covering a section. Evaluate:

1. **Opening quality** — Does it hook? Connect to previous chapter?
2. **Flow** — Sections that drag, repeat, or list facts without building insight
3. **Content cuts** — Reference-manual content that doesn't serve narrative, long code blocks
4. **Missing content** — Gaps where reader would be confused, missing transitions
5. **Diagrams needed** — Specific places where diagram replaces wall of text
6. **Cross-chapter consistency** — Voice, formatting, terminology, contradictions
7. **Specific fixes** — 5-10 sentences/paragraphs to rewrite, with reasons

Compile all feedback into single prioritized action plan.

## Phase 6: Revision

Apply all review feedback in one pass:

- **Structural** — Split/merge chapters, fix broken references, add missing closing
- **Deduplication** — Each concept explained once
- **Content cuts** — Remove enumeration (keep patterns), trim bloated sections
- **Content additions** — Worked examples, real hook examples, diagrams at identified locations
- **Consistency** — Standardize Apply This, fix repeated phrases, verify cross-references

## Phase 7: Source Code Audit

Before publication, audit every code block against the original source:

- **REPLACE** verbatim/near-verbatim copies with pseudocode using different variable names
- **ANNOTATE** type signatures with "// Illustrative"
- **VERIFY** no proprietary prompt text, internal constants, or exact implementations remain

The book teaches patterns and architecture. It should NOT enable reconstruction of the exact source code.

---

## How It Was Used (reference numbers)

- 36 AI agents across 7 phases
- ~6 hours total production time
- **Phase 1:** 6 exploration agents × 1,884 source files read
- **Phase 2-3:** 7 parts, 18 chapters
- **Phase 4:** 15 writing agents → 10,320 lines draft
- **Phase 5:** 3 review agents → 900 lines feedback
- **Phase 6:** 3 revision agents → cut 38% (-3,934 lines), added 25+ Mermaid diagrams
- **Phase 7:** 1 audit agent found 35 exact copies + 1 sanitization agent replaced all with pseudocode
- **Final:** 6,271 lines / ~400 pages equivalent
