# Design Spec — Exa-Powered Source Discovery for NLM Pipelines

- **Date:** 2026-06-13
- **Author:** CEO + Claude (brainstorming session)
- **Branch:** `feature/research-exa-discovery`
- **Status:** Approved design — pending implementation plan
- **Origin:** `/research` run on Weekend Build video "Claude AI + Exa.ai" → RESEARCH_exa-claude-research-agents_2026-06-13.md

## Problem

Every KN-Stack skill that discovers external sources for NotebookLM uses **keyword search only**: `WebSearch` (academic/authority/defense queries) and `yt-dlp` (YouTube keyword match). Zero skills use semantic search. The `/research` run on Exa.ai established (★★★ HIGH, vendor-confirmed) that Exa's neural-embedding search:
- Finds conceptually-related sources keyword search misses (incl. Google Maps reviews, social/forum content).
- Returns clean structured results (categories: company / news / people / research paper / financial report) that feed LLMs directly.
- Supports domain filtering (`includeDomains`) and date filtering (`startPublishedDate`) — directly replicating our authority-domain and recency channels.
- Has a "highlights" feature that cuts token cost.

Upgrading source discovery to prefer Exa (when available) raises the *quality of every notebook* that research / mentor / learning pipelines build.

## Goals

1. Make Exa the **preferred** discovery engine across NLM source-discovery skills, **without breaking** the existing WebSearch/yt-dlp pipelines.
2. Encode the Exa protocol **once** (single source of truth) so downstream skills inherit it.
3. Degrade gracefully: skills work identically to today when Exa is not installed, quota-exhausted (429), or disabled via `--no-exa`.

## Non-Goals

- Installing/configuring the Exa Connector (CEO does this in Claude Desktop).
- Replacing yt-dlp for video discovery (Exa is weaker on video; yt-dlp stays).
- Replacing the patent channel (Channel 4 unchanged; Exa `research paper` category *supplements*, not replaces).
- Live end-to-end testing of the Exa path (Exa MCP is not connected in the authoring session; verification happens post-install).

## Decisions (locked with CEO 2026-06-13)

| Decision | Choice |
|----------|--------|
| Replace vs augment | **Augment + fallback** — Exa is an added "Channel 0", WebSearch/yt-dlp remain as fallback |
| Scope | **Hub-first** — upgrade `/research` + references (propagates to inheritors), thin notes elsewhere |
| Activation | **Auto when Exa available**, `--no-exa` escape; auto-fallback when absent/429 |
| Encoding | **Option A** — one shared reference doc `research/references/exa-discovery.md` |
| Process rigor | Full superpowers (spec → plan → execute) |

## Architecture

### Shared protocol (single source of truth)

```
research/references/exa-discovery.md   ← NEW canonical "Exa Discovery Protocol"
        ▲ referenced by
        ├── research/SKILL.md (Step 1, Channel 0)
        ├── mentor-board/SKILL.md (Stage A2 pointer)
        ├── learning/SKILL.md (Step 1 pointer)
        ├── yt-search/SKILL.md (thin note)
        └── yt-learn/SKILL.md (thin note)
research/references/source-tiers.md    ← gains "Exa result tiering" subsection
```

Skills that delegate to `/research` (research-to-skill, skill-from-research) inherit with **no edit needed**.

### Exa Discovery Protocol — contents of `exa-discovery.md`

1. **Capability detection**
   - Exa present if an Exa search tool is available to the agent: Exa MCP tool (`web_search_advanced_exa`, or `mcp__exa__*`) OR the native Exa Claude Connector.
   - Rule: `IF exa_search_tool_available AND NOT --no-exa → Exa path; ELSE → WebSearch/yt-dlp fallback (current behavior).`

2. **Query mapping** (Exa replaces keyword Channels 1 & 3 when active)
   - Categories: `company` (competitor/market), `news` (recent events), `people` (experts/mentors), `research paper` (academic → Tier S), `financial report` (Tier S).
   - `type`: `auto` default, `deep` for high-stakes / `--deep`.
   - `includeDomains`: replicate authority-domain channel — pull domain lists straight from `source-tiers.md` (e.g. academic `["ieee.org","arxiv.org","mdpi.com"]`; defense `["dtic.mil","nato.int"]`).
   - `startPublishedDate` / `endPublishedDate`: recency control (esp. for `--update` mode).
   - Request highlights/structured contents to minimize downstream tokens.
   - Result budget: mirror current caps (≈15 web-equivalent), dedup by URL before merge.

3. **Tier mapping for Exa results**
   - `category: research paper` or `financial report` → **S**.
   - Result whose domain ∈ authority list (source-tiers.md) → **A**.
   - Else → apply existing URL heuristic from source-tiers.md.
   - (Exa returns a relevance score — record it but do not let it override tier.)

4. **Fallback ladder + free-tier guard**
   - Exa active → Channel 0 runs first. WebSearch Channels 1/3 become *supplementary* (catch index-lag / niche); skip if Exa already yields S+A ≥ 3. Channel 2 (yt-dlp) and Channel 4 (patents) always run.
   - Exa absent / `--no-exa` → current pipeline unchanged, log `"Exa unavailable — WebSearch fallback"`.
   - Exa **429 / quota exhausted** (free tier = 1000 req/mo, hard stop, no graceful degrade per research finding) → fall back to WebSearch mid-run, warn CEO once.

### `/research` Step 1 change

Insert **Channel 0 — Exa Semantic Discovery** above Channel 1; update the PIPELINE FLOW ascii diagram; add `--no-exa` to the Usage line; bump header v4.0 → **v4.1**.

### Downstream edits

- `mentor-board/SKILL.md` Stage A2 + `learning/SKILL.md` Step 1: one-line pointer — "Source discovery uses the Exa Discovery Protocol (`research/references/exa-discovery.md`) when Exa is available; WebSearch fallback otherwise."
- `yt-search/SKILL.md` + `yt-learn/SKILL.md`: thin note — optional Exa semantic video discovery (`includeDomains:["youtube.com"]`) as a pre-step before/alongside yt-dlp keyword search; yt-dlp remains the fallback.

## Error Handling

| Condition | Behavior |
|-----------|----------|
| No Exa tool present | Silent fallback to WebSearch/yt-dlp; log once |
| `--no-exa` flag | Force fallback |
| Exa 429 / quota | Fall back mid-run + warn CEO |
| Exa returns 0 results | Run WebSearch channels as supplement (don't fail) |
| Exa result URL fails NLM ingest | Existing Step 4G recovery ladder (alt URL → WebFetch→text → YT substitute) — unchanged |

## Testing / Verification

- **Static (now):** each edited SKILL.md keeps valid frontmatter (`name:` = dir, `description:` with triggers); `bash setup.sh --status` skill count unchanged (no skills added/removed); junctions still resolve.
- **Behavioral (now, no Exa):** confirm `/research` instructions still describe a complete WebSearch+yt-dlp run when Exa absent (fallback path intact). This is the only path testable in-session.
- **Live (post-install, CEO):** after Exa Connector added, run `/research` on a VN-market topic and confirm Channel 0 fires and tiers map correctly. Deferred — documented as a follow-up, not a blocker.

## Files Touched

| # | File | Change | Risk |
|---|------|--------|:----:|
| 1 | `skills/galaxy/research/references/exa-discovery.md` | NEW protocol doc | low |
| 2 | `skills/galaxy/research/SKILL.md` | Channel 0 + diagram + `--no-exa` + v4.1 | med |
| 3 | `skills/galaxy/research/references/source-tiers.md` | Exa tiering subsection | low |
| 4 | `skills/galaxy/mentor-board/SKILL.md` | Stage A2 one-line pointer | low |
| 5 | `skills/galaxy/learning/SKILL.md` | Step 1 one-line pointer | low |
| 6 | `skills/extract/yt-search/SKILL.md` | thin Exa note | low |
| 7 | `skills/extract/yt-learn/SKILL.md` | thin Exa note | low |
| 8 | `CHANGELOG.md` | entry for the upgrade | low |

> Note: Explore agent reported `mentor-board` and `learning` under `skills/galaxy/`. Implementation plan must verify exact paths (`bash setup.sh --status` / Glob) before editing — mentor-board may live at `skills/galaxy/mentor-board/`.

## Open Risks

1. **Exa tool name uncertainty** — the exact callable name once the Connector is installed (`web_search_advanced_exa` vs `mcp__exa__...`) isn't observable now. Mitigation: protocol detects "any Exa search tool" by capability, not a hardcoded name; give both known forms as examples.
2. **Path drift** — Explore agent's line numbers are a snapshot; re-grep at edit time.
3. **No live test** — accepted; fallback design makes it safe.
