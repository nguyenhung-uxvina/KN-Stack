# Facet Split Strategies — Multi-Notebook Per Mentor

When mentor's source pool exceeds NLM 50-source limit (practical cap: 45 with 5-slot refresh headroom), split into facets.

Triggered at ADD A3.5 step.

## Tier Classification (T1/T2/T3) — Source Quality

Before facet split, sources are tier-classified:

| Tier | Type | Example for Munger |
|------|------|---------------------|
| **T1 Direct** | Leader's own writings/talks/posts | Berkshire annual meetings (verbatim), Poor Charlie's Almanack, DJCO meetings, USC commencement |
| **T2 Authoritative** | Biographies + academic case studies + official corporate docs by leader | Berkshire shareholder letters (Munger co-authored), Damn Right (Janet Lowe biography), academic papers analyzing Munger's investment style |
| **T3 Other** | Third-party analysis, op-eds, fan summaries | Investor newsletter analyses of Munger's portfolio, podcast interviews ABOUT Munger (not BY) |

**Rule:** T1 mandatory ≥3, T2 supplements, T3 fills gaps (max 30% of total).

## Split Strategy Options

Present these 3 strategies to CEO at A3.5:

### Strategy A — Temporal Split

**Best for:** mentors with long career + evolving thinking (Munger 60+ years, Buffett, Marks across cycles).

**Pattern:**
```
mentor-<leader>-early    pre-2000 (foundational era)
mentor-<leader>-middle   2000-2015 (mature framework)
mentor-<leader>-recent   2015+ (current views)
```

**Pros:** evolution tracking (Frame 1 can show "earlier view vs current view"), refresh-by-era simple.

**Cons:** problems may need cross-era synthesis (handled by per-mentor skill's cross-facet query).

**Example for Munger:**
- `munger-early`: 1995-2000 Berkshire meetings + USC speech
- `munger-middle`: 2001-2015 Berkshire + DJCO meetings + Poor Charlie's
- `munger-recent`: 2016-2023 Berkshire + DJCO + interviews

### Strategy B — Topical Split

**Best for:** mentors with multi-modal content (books vs talks vs corporate docs) where each modality has distinct character.

**Pattern:**
```
mentor-<leader>-books        published books only
mentor-<leader>-talks        speeches, interviews, podcasts
mentor-<leader>-corporate    earnings, shareholder letters, official docs
mentor-<leader>-social       X/Twitter, blog posts, casual writings
```

**Pros:** query precision (CEO can ask "what's Musk's view from X archive only?"), book-mode is highest-density wisdom.

**Cons:** themes split across modalities; cross-facet synthesis needed for full picture.

**Example for Musk:**
- `musk-books`: Walter Isaacson biography (authorized, primary)
- `musk-talks`: SpaceX/Tesla YouTube + Everyday Astronaut interviews + GTC appearances
- `musk-corporate`: Tesla earnings calls 2018-2024 + SpaceX press conferences
- `musk-social`: X (Twitter) archive (his own posts)

### Strategy C — Hybrid (CEO-defined)

**Best for:** mentors with unique structure (e.g., Naval has "books + tweets" but tweets ARE his book; Howard Marks has memos as primary).

**Pattern:** CEO defines facet boundaries based on what makes sense for that specific mentor.

**Example for Naval:**
- `naval-essays`: naval.al + Almanack
- `naval-tweets`: pre-2024 Twitter archive (his most distilled thinking)
- `naval-podcasts`: Joe Rogan #1309 + Tim Ferriss + Knowledge Project

**Example for Howard Marks:**
- `marks-memos`: oaktreecapital.com memos (his PRIMARY content)
- `marks-books`: Most Important Thing + Mastering Market Cycles
- `marks-interviews`: Bloomberg + podcast appearances

## Split Decision Heuristic

```
IF leader has 50+ years of speeches/writings AND evolution is meaningful:
  → Strategy A (Temporal)

ELIF leader has clear modality differences (books are dense, talks are casual):
  → Strategy B (Topical)

ELIF leader has unique structure that doesn't fit A or B:
  → Strategy C (Hybrid — CEO defines)
```

## Per-Facet Persona Prompt

Same persona prompt across facets (it's the same person). However, optional facet-specific addendum:

```
[Standard persona prompt from references/persona.md]

[Facet-specific addendum if needed]
You are answering from your <facet name> writings/talks.
If asked about content outside this scope, say:
  "That's outside this facet — see other facets for [topic]."

Cite sources within this facet only.
```

## Cross-Facet Query in CONSULT

When CEO calls `/mentor-<leader> "<problem>"`:

1. Per-mentor skill reads `notebooks/_index.md`
2. If single facet → standard 5-frame query
3. If multi-facet (default cross-facet):
   - Spawn parallel Task subagent per facet
   - Each runs 5-frame on its facet
   - Synthesize cross-facet:
     - Per-frame: combine with `[facet_name]` citation tags
     - Detect contradictions across facets → flag as evolution
     - Output unified 5-frame with per-facet citation transparency

## --facet Targeting

CEO can narrow:

```bash
/mentor-munger --facet brk-meetings "Position sizing concentration"
  → queries only brk-meetings notebook (faster, narrower, less cost)

/mentor-musk --facet auto "How to scale production?"
  → AI picks most-relevant facet based on problem
  → Decision matrix: if problem mentions "first-principles" → talks facet
                     if problem mentions "factory layout" → books facet (Isaacson)
                     if problem mentions "Q3 results" → corporate facet
```

`--facet auto` heuristic in per-mentor skill should prefer most-cited facet for that problem class (track usage stats in `notebooks/_index.md`).

## Refresh Scoping

```bash
/mentor-munger --refresh --facet brk-meetings
  → only scan + ingest new BRK meetings content

/mentor-munger --refresh  (no facet flag)
  → refresh all facets sequentially (or parallel if rate limit allows)
```

## notebooks/_index.md Schema

```markdown
---
mentor: <leader>
total_sources: <sum across facets>
facet_count: <N>
last_refresh: <max(facet last_refresh)>
split_strategy: <temporal | topical | hybrid>
---

# Notebooks Index — <leader>

## Facets

| Facet | NLM URL | Source count | Scope | Last refresh | Primary? |
|-------|---------|:------------:|-------|--------------|:--------:|
| <facet 1> | <url> | <N> | <description> | <date> | ✓ (Studio artifacts here) |
| <facet 2> | <url> | <N> | <description> | <date> | |

## Facet Routing Stats (auto-tracked)

Last 30 days:
- <facet 1>: <N> queries (most-used facets bubble up here for --facet auto)
- <facet 2>: <N> queries
```

## Refacet (v2 future)

If mentor evolves significantly post-split (e.g., Naval starts new era of content post-2024), CEO may want to:
- Add new facet (`naval-post-2024`)
- Split existing facet
- Merge two underused facets

This is `--refacet` mode (NOT in MVP). For now: CEO manually edits `notebooks/_index.md` + runs ADD-style flow for new facets.
