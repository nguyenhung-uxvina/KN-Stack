---
name: book-explore
description: "Block P1 của codebase-to-book pipeline — phân tích codebase theo từng subsystem bằng N parallel Task subagents, mỗi agent đọc exhaustively 1 subsystem và sinh raw research notes. Supports --deep để chain /research per subsystem. Can run standalone. Triggers on: 'explore codebase', 'phân tích subsystem', 'book exploration', 'raw analysis', 'P1 book'."
---

# Block P1: Exploration — Parallel Subsystem Analysis

> **Pipeline:** codebase-to-book → Block P1
> **Input:** Codebase path + CEO scope confirmation
> **Output:** `Phase1-Exploration/<subsystem>_Exploration.md` × N + `P1_Synthesis.md`
> **Reference:** `codebase-to-book/references/phase-prompts.md` (P1 subagent prompt template)

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Map codebase into subsystems | Propose book structure (= P3) |
| Spawn N parallel Task subagents | Write narrative prose (= P4) |
| Read every file in each subsystem exhaustively | Evaluate "book-worthiness" (= P2) |
| Produce raw research notes per subsystem | Sanitize code / replace verbatim (= P7) |
| Flag coverage gaps + contradictions | Select what's in/out of scope — CEO does that |
| Invoke `/research --deep` per subsystem (if flag set) | Skip surprising-decisions section (high value) |

**Multi-Agent Mode:** YES — parallel Task subagents (1 per subsystem, typically 4-10 agents).
**CEO Checkpoint:** Review subsystem map BEFORE fan-out (avoid wasted agent runs). Then review coverage after merge.

## Standalone Usage
```
/book-explore <codebase-slug>
```

Trước khi chạy, cần có:
- `_pipeline_state.md` trong `<output_dir>/` (hoặc skill tự tạo minimal state nếu chạy standalone)
- Codebase path accessible (absolute path preferred)

## Input Requirements

- `<path>` — absolute path to codebase
- `<output_dir>` — from orchestrator hoặc derived từ slug
- `_pipeline_state.md` (nếu có) — để ledger read
- `--deep` flag (optional) — enables `/research --deep` enrichment per subsystem

## Workflow

### Step P1.1: Codebase Preflight (sequential, orchestrator-side)

Trước khi fan-out, phân tích codebase structure để xác định subsystem boundaries:

```bash
# Pseudocode — codebase scan
codebase_scan(path):
  # Language detection
  file_counts = glob("**/*.{py,ts,tsx,js,jsx,rs,go,c,cpp,java,rb,php,sh,md}")
  languages = top_3_by_count(file_counts)
  
  # Top-level structure
  top_dirs = ls("<path>/*", type="dir")
  # Filter obvious non-subsystems: node_modules, .git, dist, build, target
  excluded = {"node_modules", ".git", "dist", "build", "target", "__pycache__", ".venv", "vendor"}
  candidate_subsystems = [d for d in top_dirs if basename(d) not in excluded]
  
  # Look for known structural markers
  markers = {
    "src/": "conventional source root",
    "lib/": "library code",
    "core/": "core logic",
    "packages/": "monorepo — multiple packages",
    "services/": "microservices",
    "apps/": "multi-app repo",
    "skills/": "agentic system (KN-Stack pattern)",
  }
  
  # LOC per candidate
  loc_per_subsystem = wc_lines(candidate_subsystem)
  
  # Heuristic: subsystem valid nếu LOC ≥ 500 HOẶC có > 10 source files
  valid_subsystems = [s for s in candidates if s.loc >= 500 or s.file_count >= 10]
  
  return {
    "languages": languages,
    "total_loc": sum(loc_per_subsystem.values()),
    "subsystems": valid_subsystems,
    "excluded": excluded_dirs,
    "special_dirs": detect_markers(top_dirs),
  }
```

### Step P1.2: Present Subsystem Map to CEO (Checkpoint BEFORE fan-out)

```
═══ P1 SUBSYSTEM MAP — {{slug}} ═══

Codebase: {{path}}
Total: {{N}} files, ~{{M}} LOC
Main languages: {{lang1}} ({{pct1}}%), {{lang2}} ({{pct2}}%), ...

Proposed subsystems (N = {{count}}):
  1. <name-1> — <LOC>, <file-count> files — <1-line purpose guess>
  2. <name-2> — ...
  ...

Excluded từ analysis:
  - node_modules/ (dependencies)
  - .git/ (version control metadata)
  - dist/, build/ (generated)
  ...

Special files read globally:
  - README.md, CLAUDE.md, CONTRIBUTING.md (project context)
  - package.json / Cargo.toml / pyproject.toml (dependency tree)
  - .github/workflows/ (CI patterns)

CEO:
(1) ✅ Approve — fan-out {{N}} agents
(2) 📝 Adjust subsystem boundaries (specify changes)
(3) ➕ Add/remove subsystem(s)
(4) ⏸️ Dừng — cần review manual trước
═══════════════════════════════════════════════════
```

**Wait for CEO response.** Adjusting subsystems BEFORE fan-out tiết kiệm nhiều cost hơn fix sau.

### Step P1.3: Fan-Out Parallel Exploration Agents

Sau khi CEO approve subsystem map, spawn N Task subagents **trong single message** (multiple tool calls):

```python
# Pseudocode — orchestrator fan-out
output_dir_p1 = f"{output_dir}/Phase1-Exploration"
mkdir(output_dir_p1)

# Single message with N Task tool calls (parallel execution)
for s in approved_subsystems:
    Task(
        description=f"Explore {s.name}",
        subagent_type="Explore" if s.loc < 5000 else "general-purpose",
        prompt=render_p1_prompt(
            subsystem_name=s.name,
            boundary=s.boundary,  # list of paths/globs
            codebase_path=path,
            output_file=f"{output_dir_p1}/{s.slug}_Exploration.md",
            deep=args.deep,
        )
    )
```

**Subagent prompt template:** See `codebase-to-book/references/phase-prompts.md` § "Phase 1 — Exploration Subagent Prompt".

**Subagent output schema** (enforced via prompt):
```markdown
# Exploration — <subsystem>
Date: <date> | Agent: <id> | Codebase: <path>

## Architecture and Module Boundaries
## Key Abstractions
## Data Flow
## Design Patterns
## Integration Points
## Surprising Decisions
## Open Questions

[If --deep:]
## Deep Research Findings
### NLM Notebook
### Cross-Source Synthesis
### Critical Lens Queries
### Relevant External Patterns
```

### Step P1.4: Merge + Synthesize

Sau khi tất cả subagents return, orchestrator merge outputs:

```python
# Pseudocode
exploration_files = glob(f"{output_dir_p1}/*_Exploration.md")

synthesis = {
    "subsystems_explored": len(exploration_files),
    "files_read_total": sum(extract_files_read(f) for f in exploration_files),
    "coverage_map": build_coverage_map(exploration_files),
    "cross_cutting_patterns": find_shared_patterns(exploration_files),
    "open_questions_all": aggregate_open_questions(exploration_files),
    "contradictions": detect_contradictions(exploration_files),
}

write(f"{output_dir_p1}/P1_Synthesis.md", render_synthesis(synthesis))
```

### Step P1.5: P1 Synthesis Document

Format:

```markdown
# P1 Synthesis — {{slug}}
Date: {{today}}
Subsystems explored: {{N}}

## Coverage Map
| Subsystem | Files Read | LOC Est | Agent | Output File | Status |
|-----------|-----------|---------|-------|-------------|--------|
| ... |

## Cross-Cutting Patterns
> Patterns that appear across multiple subsystems — candidates for dedicated chapters trong book.
- Pattern 1: appears in {{A, B, C}} — <1-line summary>
- Pattern 2: ...

## Cross-Subsystem Data Flows
> Data that crosses subsystem boundaries — candidates cho architectural diagrams.
- Flow 1: <subsystem A> → <subsystem B> — carries <type>, via <mechanism>
- Flow 2: ...

## Surprising Decisions Catalog
> Aggregated từ each subsystem's "Surprising Decisions" section.
- [X-ref: subsystem Y] <decision> — why non-obvious

## Open Questions (aggregated)
> Questions flagged bởi subagents — some for CEO, some for P2 research agents to resolve.
- Q1 (from subsystem A): ...
- Q2 (from subsystem B): ...

## Contradictions Detected
> Subsystem reports that seem to conflict — need CEO disambiguation or deeper study.
- Subsystem A says X, subsystem B implies not-X — resolve via <approach>

## Coverage Gaps
> Subsystems đã explored nhưng có areas chưa cover kỹ — flag cho P4 writer subagents.
- Subsystem A section <X> shallow — deep dive needed if chapter covers this
```

### Step P1.6: Update Pipeline State + Ledger

```markdown
### P1 — Exploration (<date>)
**Key findings:** 
- {{N}} subsystems explored, {{M}} files read, {{L}} LOC
- {{K}} cross-cutting patterns identified as chapter candidates
- {{J}} open questions flagged for CEO / downstream

**Decisions for downstream:**
- P2 should use <thesis hint> based on recurring theme
- P3 should consider chapter breakdown matching subsystem boundaries, plus 2-3 cross-cutting chapters

**Open questions:**
- {{Q1}}
- {{Q2}}

**CEO checkpoint result:** [pending]
```

## Output

Save to `{{output_dir}}/Phase1-Exploration/`:
- `<subsystem>_Exploration.md` × N (1 per agent)
- `P1_Synthesis.md` (merged)

Update: `{{output_dir}}/_pipeline_state.md` Block Ledger.

## CEO Checkpoint (after merge)

```
═══ BLOCK P1 EXPLORATION COMPLETE ═══
Subsystems explored: {{N}}
Files read: {{M}} total
Cross-cutting patterns: {{K}} identified
Open questions: {{J}} flagged
Deep research: {{enabled | disabled}} — {{X}} NLM notebooks created

Deliverables:
  - {{output_dir}}/Phase1-Exploration/ ({{N+1}} files)

Key findings:
  - {{bullet 1}}
  - {{bullet 2}}
  - {{bullet 3}}

CEO:
(1) ✅ Approve → tiếp tục Block P2 (Positioning)
(2) 🔄 Re-run agent for specific subsystem: [specify]
(3) ➕ Add missing subsystem that was excluded: [specify]
(4) ⏸️ Dừng — cần CEO read exploration outputs trước
═══════════════════════════════════════════════════
```

## COD Classification

- Subsystem mapping: Offload (O2) — AI scans, CEO confirms boundaries
- Subsystem approval: **Core (C)** — CEO decides what's in/out of scope
- Fan-out exploration: Offload (O2) — parallel agents
- Synthesis merge: Offload (O2)
- Deep research invocation: Offload (O2) with CEO gates inside /research
- Coverage gap decisions: Offload (O2) — AI flags, P4 agents handle

## Rules

- **Fan-out ONLY after CEO approves subsystem map** — avoid wasted agent runs
- **Subagent output schema enforced via prompt** — deviations flagged in merge
- **Read-exhaustively discipline** — subagents must not skip files to "save time"; book quality depends on P1 depth
- **Surprising Decisions section is gold** — flag agents that return empty surprise section (likely shallow exploration)
- **If subagent returns <100 lines for a significant subsystem** — re-run with stricter prompt
- **--deep enrichment AFTER base exploration** — never start with /research (grounds in codebase first)
