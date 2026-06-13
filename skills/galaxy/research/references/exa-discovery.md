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
