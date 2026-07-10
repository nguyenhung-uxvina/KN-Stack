---
name: topic-notebook
description: "Persistent topic NotebookLM lifecycle — register/build/query/refresh reference notebooks for recurring workflow topics (standards, VDI methodology, harness doctrine, per-project). Neutral citation-first persona (NOT mentor persona-purity). Unified registry at vault 3_Resources/Topic-Notebooks. Primary T1 LOOKUP executor for /helix-research. Triggers on: 'topic notebook', 'reference notebook', 'notebook chủ đề', 'sổ tay tra cứu', 'đăng ký notebook', 'tra chuẩn MIL-STD', 'query topic notebook', 'notebook thường trực'."
---

# Topic Notebook — Persistent Reference Notebooks

> Harness class: `guide` (knowledge feedforward) + `sensor-inferential` (query answers are propose-only, citation-required).
> Distinct from mentor notebooks (person, persona-purity) and research-sprint notebooks (one-off).

## Operational Envelope

| CAN | CANNOT |
|-----|--------|
| Register existing NLM notebooks into the unified registry | Create Galaxy notes (propose-only, per AI Permissions) |
| Build a new topic notebook AFTER CEO approves seed-sources | Add sources CEO has not approved (source selection = Core) |
| Query registered notebooks, citation-first | Answer from model memory when sources are insufficient |
| Propose refresh candidates | Change a shared mentor notebook's persona |

## Modes

| Mode | Usage |
|------|-------|
| `--register <alias> <nlm-id>` | Register an EXISTING notebook |
| `--add <topic>` | Build a new topic notebook (seed-sources → CEO gate → create → ingest → persona) |
| `--query <alias> "<question>"` | Citation-first lookup |
| `--refresh <alias>` | Propose + ingest new sources (CEO approves) |
| `--list` | Registry table |
| `--health` | Staleness + capacity audit |

## Registry

Single source of truth: `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (append/update per entry; never delete entries — mark `status: retired`). Schema: see `references/registry-schema.md`.

## Workflows

### --register <alias> <nlm-id>
1. `mcp__notebooklm-mcp__notebook_describe` the ID — confirm it exists, capture source count.
2. Ask CEO for 1-line scope if not given.
3. Append entry to registry (schema fields). If the notebook is shared with a mentor (e.g. `harness` ↔ mentor-harness-engineering-council), set `persona: mentor-mode (shared)` and DO NOT reconfigure chat persona.
4. `nlm alias set <alias> <nlm-id>` (best-effort; skip with a note if nlm CLI unavailable).

### --add <topic>
1. Draft seed-sources table, tier-classified S/A/B/C per `research/references/source-tiers.md`. TCVN rows: NEVER fabricate numbers — leave `CEO to supply`.
2. **CEO GATE (Core):** present table; CEO approves/edits source list. STOP until approved.
3. `notebook_create` → `source_add` each approved source (retry: alt-URL → WebFetch-to-text → flag failed).
4. `chat_configure` with `references/reference-persona.md` content.
5. Register (as --register) + report ingest count vs approved count (fail-safe: list every source that failed).

### --query <alias> "<question>"
1. Resolve alias in registry → NLM ID. Unknown alias → show `--list`, stop.
2. `mcp__notebooklm-mcp__notebook_query`. Answer format:
   - Direct answer, each claim with `[source]` citation
   - `Confidence: HIGH/MEDIUM/LOW`
   - **NOT FOUND:** parts of the question the sources do not answer (mandatory when applicable — never fill from model memory)
3. If NOT FOUND is non-empty, propose: `--refresh` with candidate sources, or escalate to `/helix-research` T2.

### --refresh <alias>
1. Propose new source candidates (reuse `/research` Step 1 discovery or CEO-provided URLs), tier-classified.
2. CEO approves (Core) → `source_add` → update registry (`source_count`, `last_refresh`).

### --health
For each registry entry flag: `last_refresh` > 90 days → STALE; `source_count` > 45 → propose facet split per `mentor-board/references/facet-split-strategies.md`; describe-call failure → BROKEN.

## COD
- Register / query / health: **Offload** (auto-OK, report back)
- Seed-source selection, refresh approval, scope definition: **Core (CEO)**
- Notebook naming cleanup: Default (skip unless asked)

## Integration
- `/helix-research` — uses `--query` as Tier-1 LOOKUP executor
- `/helix-project-init` Step 3b — pins aliases into project charter
- `/research` — a finished research-sprint notebook may be promoted via `--register`
- `/nlm` — low-level CLI/MCP plumbing; this skill adds registry + lifecycle + protocol

## Rules
1. Citation-first: every claim carries a source reference. No citation → say NOT FOUND.
2. Registry is append/update only — retired notebooks stay listed with `status: retired`.
3. Shared-with-mentor notebooks: never touch persona (mentor purity).
4. >45 sources → facet split proposal, never silent overflow (NLM cap ~50).
