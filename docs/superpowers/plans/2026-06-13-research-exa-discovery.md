# Exa-Powered Source Discovery — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Exa semantic search the preferred source-discovery engine ("Channel 0") across KN-Stack's NLM pipelines, encoded once in a shared reference doc, with safe WebSearch/yt-dlp fallback when Exa is absent.

**Architecture:** One canonical protocol doc (`research/references/exa-discovery.md`) defines capability-detection → query-mapping → tier-mapping → fallback. `/research` Step 1 gains a Channel 0 that points to it; skills that delegate to `/research` inherit automatically; mentor-board, learning, yt-search, yt-learn get one-line pointers. Augment + fallback; auto-when-available; `--no-exa` escape.

**Tech Stack:** Markdown skill files (KN-Stack `skills/<domain>/<skill>/SKILL.md`), deployed via junctions. No code/runtime — "tests" are static checks (frontmatter validity, `setup.sh --status` skill count unchanged, junctions resolve, fallback path still complete).

**Spec:** `docs/superpowers/specs/2026-06-13-research-exa-discovery-design.md`
**Branch:** `feature/research-exa-discovery` (already created)

---

## File Structure

| File | Responsibility | Action |
|------|----------------|--------|
| `skills/galaxy/research/references/exa-discovery.md` | Canonical Exa Discovery Protocol (single source of truth) | CREATE |
| `skills/galaxy/research/SKILL.md` | Add Channel 0 to Step 1, flow diagram, `--no-exa`, v4.1 | MODIFY |
| `skills/galaxy/research/references/source-tiers.md` | Exa result tiering rules | MODIFY |
| `skills/galaxy/mentor-board/SKILL.md` | A2 discovery pointer | MODIFY |
| `skills/galaxy/learning/SKILL.md` | Step 1 intake pointer | MODIFY |
| `skills/extract/yt-search/SKILL.md` | Optional Exa video discovery note | MODIFY |
| `skills/extract/yt-learn/SKILL.md` | Cross-ref to discovery skills | MODIFY |
| `CHANGELOG.md` | Release entry | MODIFY |

---

## Task 1: Create the Exa Discovery Protocol reference doc

**Files:**
- Create: `skills/galaxy/research/references/exa-discovery.md`

- [ ] **Step 1: Create the file with this exact content**

````markdown
# Exa Discovery Protocol — Semantic Source Discovery for NLM Pipelines

> Shared protocol. Referenced by /research (Channel 0), mentor-board (A2), learning (Step 1), yt-search, yt-learn.
> Exa = neural-embedding web search ("đôi mắt của Claude"). PREFERRED discovery engine WHEN AVAILABLE; WebSearch/yt-dlp remain the fallback. Discovery only — does not change NLM ingestion (Step 4G) or the CEO source-selection gate (Step 3).

## 1. Capability Detection (run before any discovery)

Exa is "available" if EITHER holds:
- An Exa MCP search tool is callable — name is one of `web_search_advanced_exa`, `mcp__exa__web_search_advanced_exa`, or any tool whose name contains both `exa` and `search`.
- The native Exa Claude Connector is active (its search tool appears in the tool list).

Decision:
```
IF exa_search_tool_available AND NOT flag --no-exa:
    → EXA PATH (Channel 0, §2)
ELSE:
    → FALLBACK: existing WebSearch + yt-dlp channels. Log once:
      "ℹ Exa unavailable — WebSearch/yt-dlp fallback"
```
Never fail when Exa is absent. The fallback IS the original pipeline.

## 2. Query Mapping (Exa replaces keyword Channels 1 & 3 when active)

| Intent | Exa params |
|--------|-----------|
| Competitor / market scan | `category:"company"`, `numResults:15` |
| Recent events / news | `category:"news"`, `startPublishedDate:<ISO>` |
| Experts / people / mentors | `category:"people"` |
| Academic (→ Tier S) | `category:"research paper"` |
| Financial filings (→ Tier S) | `category:"financial report"`, `includeDomains:["sec.gov", …]` |
| Authority-domain (→ Tier A) | `type:"auto"`, `includeDomains:[…from source-tiers.md]` |

Rules:
- `type`: `"auto"` default; `"deep"` for high-stakes or when `--deep` is set.
- `includeDomains`: pull domain lists straight from `source-tiers.md` "Authority Domain Queries" (academic `["ieee.org","arxiv.org","mdpi.com","researchgate.net"]`; defense `["dtic.mil","nato.int","sto.nato.int"]`; VN `["tcvn.gov.vn"]`). This replicates Channel 3 semantically.
- Request highlights / structured `contents` to minimize downstream token cost.
- Keep total Exa results ≤ 15 (mirror Channel-1 cap). Dedup by URL before merge.

## 3. Tier Mapping for Exa Results

Apply in order:
1. Exa `category:"research paper"` or `"financial report"` → **S**.
2. Result domain ∈ any Authority Domain list in source-tiers.md → **A**.
3. Otherwise → apply the URL heuristic table in source-tiers.md (S/A/B/C).

Record Exa's relevance score for sort order only — it never overrides tier.

## 4. Fallback Ladder & Free-Tier Guard

- Exa active → Channel 0 runs FIRST. Then:
  - Channel 0 yields S+A ≥ 3 → WebSearch Channels 1/3 OPTIONAL (run only to fill a gap).
  - Else → run WebSearch Channels 1/3 as supplement (Exa index can lag niche / JS-heavy content).
- Channel 2 (yt-dlp) and Channel 4 (patents) ALWAYS run — Exa is weak on video; patents have a dedicated channel. Exa `research paper` supplements, never replaces, patents.
- **Free-tier 429 guard:** Exa free tier ≈ 1000 req/month with a HARD stop (429, no graceful degrade). On 429 / quota error:
  ```
  → Stop Exa calls; fall back to WebSearch for remaining queries
  → Warn CEO once: "⚠ Exa quota hết (429) — chuyển sang WebSearch"
  ```
- Exa returns 0 results → run WebSearch channels; never fail the pipeline.

## 5. Integration with Source Quality Gate (Step 4G)

Exa changes DISCOVERY only. After sources are selected and added to NLM, the existing Step 4G ingestion-recovery ladder (alt URL → WebFetch→text → YouTube substitute) is UNCHANGED.

## 6. CEO-Facing Notes

- The Step 3 source-selection gate is unchanged: AI presents the tiered table, CEO selects. Exa only changes HOW candidates are found.
- When Exa is used, note it in the Source Quality Report: "Discovery: Exa Channel 0 (semantic) + [fallback channels run]".
````

- [ ] **Step 2: Verify the file exists and is well-formed**

Run: `cd "D:/KN-Stack" && wc -l skills/galaxy/research/references/exa-discovery.md && head -3 skills/galaxy/research/references/exa-discovery.md`
Expected: ~55 lines; first line `# Exa Discovery Protocol — Semantic Source Discovery for NLM Pipelines`

- [ ] **Step 3: Commit**

```bash
cd "D:/KN-Stack" && git add skills/galaxy/research/references/exa-discovery.md && git commit -m "[RESEARCH] Add Exa Discovery Protocol reference doc" -m "Shared single-source-of-truth: capability detection, query mapping, tier mapping, fallback ladder + free-tier 429 guard." -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 2: Add Channel 0 to /research

**Files:**
- Modify: `skills/galaxy/research/SKILL.md`

- [ ] **Step 1: Add `--no-exa` to the Usage line**

Replace:
```
Usage: /research <topic> [--notebook <alias>] [--output report|audio|mindmap|quiz] [--count N] [--deep] [--patents] [--update] [--extract miner|cross-std|structure]
```
With:
```
Usage: /research <topic> [--notebook <alias>] [--output report|audio|mindmap|quiz] [--count N] [--deep] [--patents] [--update] [--extract miner|cross-std|structure] [--no-exa]
```

- [ ] **Step 2: Bump version note in the intro prose (line ~6)**

Replace:
```
End-to-end research pipeline v4.0 with multi-channel source discovery (Web + YouTube + Authority + Patents), source tier classification (S/A/B/C), analysis routing by quality, cross-validation, and structured NLM extraction templates. The "super skill" combining WebSearch + /yt-search + /nlm + Deep Content Analyzer into one workflow. v4.0 adds 3 extraction modes for deep NLM analysis.
```
With:
```
End-to-end research pipeline v4.1 with multi-channel source discovery (Exa + Web + YouTube + Authority + Patents), source tier classification (S/A/B/C), analysis routing by quality, cross-validation, and structured NLM extraction templates. The "super skill" combining WebSearch + /yt-search + /nlm + Deep Content Analyzer into one workflow. v4.0 adds 3 extraction modes for deep NLM analysis. v4.1 adds Channel 0 — Exa semantic discovery (preferred when the Exa MCP/Connector is available; WebSearch fallback otherwise). See references/exa-discovery.md.
```

- [ ] **Step 3: Add Channel 0 to the PIPELINE FLOW diagram**

Replace:
```
[1] MULTI-CHANNEL SEARCH (parallel)
    ├── Channel 1: WebSearch academic/OEM/standards
    ├── Channel 2: YouTube (yt-dlp)
    ├── Channel 3: Known authority domains
    └── Channel 4: Patent search (engineering topics or --patents)
```
With:
```
[1] MULTI-CHANNEL SEARCH (parallel)
    ├── Channel 0: Exa semantic discovery (when available — see exa-discovery.md)
    ├── Channel 1: WebSearch academic/OEM/standards (Exa fallback / supplement)
    ├── Channel 2: YouTube (yt-dlp)
    ├── Channel 3: Known authority domains (→ Exa includeDomains when Exa active)
    └── Channel 4: Patent search (engineering topics or --patents)
```

- [ ] **Step 4: Insert Channel 0 subsection + detection note in Step 1**

Replace:
```
## STEP 1: MULTI-CHANNEL SEARCH

Run 4 search channels in parallel:

### Channel 1 — Web Search
```
With:
```
## STEP 1: MULTI-CHANNEL SEARCH

Run search channels in parallel. **First, detect Exa availability** (see `references/exa-discovery.md` §1). When Exa is available and `--no-exa` is not set, Channel 0 is the preferred discovery engine and Channels 1 & 3 become supplementary; otherwise the pipeline runs exactly as the 4-channel WebSearch/yt-dlp flow below.

### Channel 0 — Exa Semantic Discovery (when available)

Neural-embedding search via the Exa MCP/Connector. Replaces keyword Channels 1 & 3 when active. Map topic → Exa categories + `includeDomains` (from source-tiers.md) per `references/exa-discovery.md` §2; tier results per §3. On Exa 429/quota or zero results → fall back to WebSearch (§4). Channels 2 (yt-dlp) and 4 (patents) always run.

### Channel 1 — Web Search
```

- [ ] **Step 5: Verify frontmatter intact + Channel 0 present + reference resolves**

Run:
```bash
cd "D:/KN-Stack" && head -4 skills/galaxy/research/SKILL.md && grep -n "Channel 0" skills/galaxy/research/SKILL.md && grep -n "no-exa" skills/galaxy/research/SKILL.md && test -f skills/galaxy/research/references/exa-discovery.md && echo "REF OK"
```
Expected: frontmatter `name: research` present; ≥2 "Channel 0" hits; ≥2 "no-exa" hits; "REF OK".

- [ ] **Step 6: Commit**

```bash
cd "D:/KN-Stack" && git add skills/galaxy/research/SKILL.md && git commit -m "[RESEARCH] v4.1: add Channel 0 Exa semantic discovery to Step 1" -m "Augment+fallback; --no-exa escape; flow diagram + usage updated." -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 3: Add Exa tiering rules to source-tiers.md

**Files:**
- Modify: `skills/galaxy/research/references/source-tiers.md` (append at end, after the "Contradiction Handling" block)

- [ ] **Step 1: Append this section to the end of the file**

```markdown

## Exa Result Tiering (v4.1)

When sources come from Exa Channel 0 (see `exa-discovery.md`), assign tier in this order:

1. Exa `category: "research paper"` or `"financial report"` → **S** (primary).
2. Result domain ∈ any Authority Domain list above (ti.com, dtic.mil, ieee.org, …) → **A**.
3. Otherwise → apply the URL heuristic table above (S/A/B/C).

Exa returns a relevance score per result — use it for sort order only, never to override tier. Exa `includeDomains` maps directly onto the "Authority Domain Queries" lists above: pass the same domains to Exa instead of running `site:` WebSearch queries.
```

- [ ] **Step 2: Verify**

Run: `cd "D:/KN-Stack" && grep -n "Exa Result Tiering" skills/galaxy/research/references/source-tiers.md`
Expected: one hit.

- [ ] **Step 3: Commit**

```bash
cd "D:/KN-Stack" && git add skills/galaxy/research/references/source-tiers.md && git commit -m "[RESEARCH] source-tiers: Exa result tiering rules" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 4: Add inherited-discovery pointers to mentor-board & learning

**Files:**
- Modify: `skills/galaxy/mentor-board/SKILL.md` (A2 line)
- Modify: `skills/galaxy/learning/SKILL.md` (Step 1 intake table)

- [ ] **Step 1: mentor-board A2 — add Exa pointer**

Replace:
```
2. **A2** Discover sources via multi-channel (reuse `/research` Step 4 logic). Tier classify T1/T2/T3 (see facet-split-strategies.md cho T criteria).
```
With:
```
2. **A2** Discover sources via multi-channel (reuse `/research` Step 1 + Step 4G logic — **Exa Channel 0 when available**, see `../research/references/exa-discovery.md`; WebSearch fallback otherwise). Tier classify T1/T2/T3 (see facet-split-strategies.md cho T criteria).
```

- [ ] **Step 2: learning Step 1 — add Exa note to the "Raw topic" intake row**

Replace:
```
| Raw topic (no source) | Search → gather | /research pipeline |
```
With:
```
| Raw topic (no source) | Search → gather (Exa Channel 0 when available) | /research pipeline — see `../research/references/exa-discovery.md` |
```

- [ ] **Step 3: Verify both pointers + relative paths resolve**

Run:
```bash
cd "D:/KN-Stack" && grep -n "exa-discovery" skills/galaxy/mentor-board/SKILL.md skills/galaxy/learning/SKILL.md && test -f skills/galaxy/research/references/exa-discovery.md && echo "TARGET OK"
```
Expected: one hit in each file; "TARGET OK" (relative `../research/references/exa-discovery.md` from `skills/galaxy/<skill>/` resolves to the real file).

- [ ] **Step 4: Commit**

```bash
cd "D:/KN-Stack" && git add skills/galaxy/mentor-board/SKILL.md skills/galaxy/learning/SKILL.md && git commit -m "[GALAXY] mentor-board + learning: point discovery to Exa protocol" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 5: Add Exa notes to yt-search & yt-learn

**Files:**
- Modify: `skills/extract/yt-search/SKILL.md` (Step 1)
- Modify: `skills/extract/yt-learn/SKILL.md` (Input section)

- [ ] **Step 1: yt-search — add optional Exa video-discovery note after the count-adjust line**

Replace:
```
Adjust count: `ytsearch5:`, `ytsearch10:`, etc. theo `--count`.

Nếu `yt-dlp` không tìm được → báo CEO, dừng.
```
With:
```
Adjust count: `ytsearch5:`, `ytsearch10:`, etc. theo `--count`.

> **Exa option (when available):** for *concept-based* video discovery (not just keyword match), run Exa with `includeDomains:["youtube.com"]` first (see `../../galaxy/research/references/exa-discovery.md`), then merge with yt-dlp results and dedup by video ID. yt-dlp remains the fallback.

Nếu `yt-dlp` không tìm được → báo CEO, dừng.
```

- [ ] **Step 2: yt-learn — add cross-ref note after the Input URL formats**

Replace:
```
- `https://youtube.com/shorts/XXXXXXXXXXX`

## Workflow
```
With:
```
- `https://youtube.com/shorts/XXXXXXXXXXX`

> To *find* a video worth learning from (semantic discovery), use `/yt-search` or `/research` Channel 0 (Exa) first — see `../../galaxy/research/references/exa-discovery.md`. `/yt-learn` itself assumes the URL is already chosen.

## Workflow
```

- [ ] **Step 3: Verify both notes + relative paths**

Run:
```bash
cd "D:/KN-Stack" && grep -n "exa-discovery" skills/extract/yt-search/SKILL.md skills/extract/yt-learn/SKILL.md && test -f skills/galaxy/research/references/exa-discovery.md && echo "PATH OK"
```
Expected: one hit in each; "PATH OK" (relative `../../galaxy/research/references/exa-discovery.md` from `skills/extract/<skill>/` resolves to the real file).

- [ ] **Step 4: Commit**

```bash
cd "D:/KN-Stack" && git add skills/extract/yt-search/SKILL.md skills/extract/yt-learn/SKILL.md && git commit -m "[EXTRACT] yt-search + yt-learn: Exa discovery cross-refs" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Task 6: CHANGELOG entry + final whole-repo verification

**Files:**
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Read the current top of CHANGELOG to match its format**

Run: `cd "D:/KN-Stack" && head -20 CHANGELOG.md`
Expected: see the existing latest-version heading style (e.g. `## [1.1.0] - YYYY-MM-DD`).

- [ ] **Step 2: Insert this entry directly under the top title, ABOVE the most recent version block** (adapt heading punctuation to match existing style)

```markdown
## [Unreleased] - 2026-06-13
### Added
- **Exa semantic source discovery ("Channel 0")** across NLM discovery pipelines, encoded once in `skills/galaxy/research/references/exa-discovery.md`. Augment + fallback: Exa preferred when the Exa MCP/Connector is available; WebSearch/yt-dlp fallback otherwise; `--no-exa` escape; free-tier 429 guard. Touched: `/research` (→ v4.1), `source-tiers.md`, `mentor-board` (A2), `learning` (Step 1), `yt-search`, `yt-learn`.
```

- [ ] **Step 3: Verify skill count unchanged (no skills added/removed — only a reference doc + edits)**

Run: `cd "D:/KN-Stack" && find skills -name SKILL.md | wc -l`
Expected: same count as before this plan (230). A reference doc is not a SKILL.md, so the count must NOT change.

- [ ] **Step 4: Verify fallback path is still complete (the only in-session-testable behavior)**

Run: `cd "D:/KN-Stack" && grep -n "Channel 1 — Web Search" skills/galaxy/research/SKILL.md && grep -n "yt-dlp" skills/galaxy/research/SKILL.md | head -1`
Expected: Channel 1 + yt-dlp still present — confirms that with Exa absent, the original 4-channel pipeline is intact.

- [ ] **Step 5: Verify junctions still resolve (deployment integrity)**

Run: `cd "D:/KN-Stack" && bash setup.sh --verify 2>&1 | tail -5`
Expected: junctions resolve OK (no broken-link errors). If `setup.sh --verify` is unavailable, run `bash setup.sh --status 2>&1 | tail -10` and confirm domain counts unchanged.

- [ ] **Step 6: Commit**

```bash
cd "D:/KN-Stack" && git add CHANGELOG.md && git commit -m "[META] CHANGELOG: Exa Channel 0 source-discovery upgrade" -m "Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
```

---

## Done criteria
- `exa-discovery.md` exists and is referenced by 5 skills (research, mentor-board, learning, yt-search, yt-learn).
- `/research` describes Channel 0 + detection + fallback; `--no-exa` documented; v4.1.
- All relative reference paths resolve to the real file.
- Skill count unchanged (230); fallback (WebSearch/yt-dlp) path intact; junctions verify.
- 6 commits on `feature/research-exa-discovery`.
- **Deferred (post-install, not a blocker):** live `/research` run with Exa Connector to confirm Channel 0 fires and tiers map correctly.
