---
name: research
description: End-to-end research pipeline v4.0 with multi-channel source discovery (Web + YouTube + Authority + Patents), source tier classification (S/A/B/C), cross-validation, and structured NLM extraction. The super-skill combining WebSearch + /yt-search + /nlm into one workflow with CEO approval gates. Use when starting a new research sprint on any technical, defense, or market topic. Triggers on: "research topic", "find sources on", "nghien cuu chu de", "tim tai lieu", "nghiên cứu chuyên sâu", "tìm nguồn tham khảo", "patent search", "literature review".
---

End-to-end research pipeline v4.1 with multi-channel source discovery (Exa + Web + YouTube + Authority + Patents), source tier classification (S/A/B/C), analysis routing by quality, cross-validation, and structured NLM extraction templates. The "super skill" combining WebSearch + /yt-search + /nlm + Deep Content Analyzer into one workflow. v4.0 adds 3 extraction modes for deep NLM analysis. v4.1 adds Channel 0 — Exa semantic discovery (preferred when the Exa MCP/Connector is available; WebSearch fallback otherwise). See references/exa-discovery.md.

Usage: /research <topic> [--notebook <alias>] [--output report|audio|mindmap|quiz] [--count N] [--deep] [--patents] [--update] [--extract miner|cross-std|structure] [--no-exa]

PATH setup (required for all commands):
```bash
export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"
export PYTHONIOENCODING=utf-8
export NO_COLOR=1
```

---

## PIPELINE FLOW (9 Steps)

```
[1] MULTI-CHANNEL SEARCH (parallel)
    ├── Channel 0: Exa semantic discovery (when available — see exa-discovery.md)
    ├── Channel 1: WebSearch academic/OEM/standards (Exa fallback / supplement)
    ├── Channel 2: YouTube (yt-dlp)
    ├── Channel 3: Known authority domains (→ Exa includeDomains when Exa active)
    └── Channel 4: Patent search (engineering topics or --patents)
     ↓
[2] MERGE + TIER CLASSIFY (S/A/B/C)
    Deduplicate → Tag tier → Sort S-first
    Priority check: S+A ≥ 3? → "đủ nguồn pro"
     ↓
[3] PRESENT TO CEO (Core — không skip)
    Table grouped by tier, S first → A → B → C
    Patent-specific table with metadata (Patent #, Assignee, Filed, Status)
    CEO selects sources + confirms analysis depth
     ↓
[3.5] NLM AUTH PRE-CHECK
    Verify NLM session before committing to pipeline
    If expired → prompt CEO to login → retry → fallback to Quick Mode
     ↓
[4] NLM NOTEBOOK SETUP
    Create/reuse notebook → Add ALL selected sources via nlm source add
    Source dedup: skip if URL already in notebook
    Source limit: warn if notebook approaching 50 sources
    NLM can ingest URLs that WebFetch cannot (PDFs, paywalls, YouTube)
     ↓
[4G] SOURCE QUALITY GATE (v3.1 — Core, do not skip)
    Verify ingested vs selected → Recover failed sources (alt URL, WebFetch, YT)
    Present gap report → CEO adds manual sources OR approves
    STOP until CEO confirms "đủ nguồn + chất lượng"
     ↓
[5] ANALYSIS ROUTING (by tier)
    S/A → Deep Path (NLM deep query + optional DCA v2)
    B   → Standard Path (NLM standard query)
    C   → Quick Path (NLM 3-bullet)
    ALL → NLM cross-source synthesis query (mandatory)
     ↓
[6] CROSS-VALIDATE
    Compare S/A findings vs B/C claims
    Score each insight: ★★★ / ★★ / ★
     ↓
[7] SAVE TO VAULT
    → 3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_<slug>_<date>.md
    Enhanced format: source tier + confidence per insight
     ↓
[8] FLAG GALAXY CANDIDATES (THỊNH H — Hóa)
    Only ★★★/★★ qualify for Galaxy promotion
    ★ insights → "needs verification" backlog
     ↓
[9] SOURCE QUALITY REPORT
    Summary of S/A/B/C distribution + gap flags + patent landscape
```

---

## SOURCE TIER SYSTEM

→ See `references/source-tiers.md` for full tier table, detection heuristics, authority domain queries, patent metadata extraction, and confidence scoring.

Quick reference: **S** (Standards/Primary) → **A** (Authority/OEM) → **B** (Professional) → **C** (Community)

---

## STEP 1: MULTI-CHANNEL SEARCH

Run search channels in parallel. **First, detect Exa availability** (see `references/exa-discovery.md` §1). When Exa is available and `--no-exa` is not set, Channel 0 is the preferred discovery engine and Channels 1 & 3 become supplementary; otherwise the pipeline runs exactly as the 4-channel WebSearch/yt-dlp flow below.

### Channel 0 — Exa Semantic Discovery (when available)

Neural-embedding search via the Exa MCP/Connector. Replaces keyword Channels 1 & 3 when active. Map topic → Exa categories + `includeDomains` (from source-tiers.md) per `references/exa-discovery.md` §2; tier results per §3. On Exa 429/quota or zero results → fall back to WebSearch (§4). Channels 2 (yt-dlp) and 4 (patents) always run.

### Channel 1 — Web Search

Use WebSearch tool with 3 queries per topic:

```
Q1 (Academic/Standards):
    "<topic> site:ieee.org OR site:arxiv.org OR site:researchgate.net"

Q2 (OEM/Industry):
    "<topic> application note OR whitepaper OR datasheet filetype:pdf"

Q3 (Defense/Standards):
    "<topic> MIL-STD OR STANAG OR standard OR specification"
```

Take top 5 results per query → max 15 web sources.

### Channel 2 — YouTube (existing)

```bash
yt-dlp "ytsearch{{count}}:{{topic}}" --flat-playlist --print "%(id)s | %(title)s | %(duration_string)s | %(view_count)s views | %(upload_date)s | %(channel)s" --no-download
```

Default count: 5. Include channel name for tier classification.

### Channel 3 — Known Authority Domains

Use WebSearch with domain-specific queries. See `references/source-tiers.md` for full query templates per topic domain (Electronics, Defense, Engineering, Vietnam Standards).

Select relevant domains based on topic. Take top 3-5 per domain.

### Channel 4 — Patent Search (v3.0)

**Activation:** Runs when topic is product/technology/engineering (default for Workshop X), OR when `--patents` flag is used. Skip for non-technical research topics.

See `references/source-tiers.md` for patent query templates and metadata extraction fields.

Take top 5 results per query → max 15 patent sources. All patents → **Tier S**.

---

## STEP 2: MERGE + TIER CLASSIFY

1. Collect all results from 4 channels
2. Deduplicate by URL
3. Apply tier detection heuristics to each source
4. Sort: S first → A → B → C
5. Priority check:

```
IF tier_S_count + tier_A_count >= 3:
    flag "✓ Đủ nguồn pro — Tier C sources optional"
ELSE:
    warn "⚠ Thiếu nguồn pro — cần refine search terms?"
    suggest alternative search queries
```

---

## STEP 3: PRESENT TO CEO (Core — do not skip)

Present results as grouped table:

```markdown
## Search Results: "{{topic}}"
Channels: Web ✓ | YouTube ✓ | Authority ✓ | Patents ✓/—
Pro sources (S+A): {{count}} | Total: {{total}}

### Tier S — Standards/Primary
| # | Title | Source | Type |
|---|-------|--------|------|
| 1 | {{title}} | ieee.org | Paper |

### Tier S — Patents
| # | Patent # | Title | Assignee | Filed | Status |
|---|----------|-------|----------|-------|--------|
| 2 | US10,234,567 | {{title}} | {{assignee}} | 2019 | Active |

### Tier A — Authority/OEM
| # | Title | Source | Type |
|---|-------|--------|------|
| 3 | {{title}} | ti.com | App Note |

### Tier B — Professional
| # | Title | Source | Type | Views |
|---|-------|--------|------|-------|
| 4 | {{title}} | YouTube | Video | 150K |

### Tier C — Community
| # | Title | Source | Type | Views |
|---|-------|--------|------|-------|
| 5 | {{title}} | YouTube | Tutorial | 5K |

CEO: Chọn sources nào để analyze? (gợi ý: ưu tiên S/A)
```

Wait for CEO selection. Never auto-select.

---

## STEP 3.5: NLM AUTH PRE-CHECK (v3.0)

Before committing to NLM-based pipeline, verify auth:

```bash
nlm notebook list --quiet 2>&1
```

Decision logic:
```
IF exit_code != 0 OR output contains "auth" OR "login" OR "expired" OR "401":
  → Log: "⚠ NLM session hết hạn."
  → Prompt CEO: "Chạy `nlm login` ở terminal riêng, rồi nói 'done'"
  → Wait for CEO response
  → Retry `nlm notebook list --quiet`
  → IF still fail → switch to Quick Mode (Claude-only analysis)
ELSE:
  → Log: "✓ NLM auth valid"
  → Proceed to Step 4
```

---

## STEP 4: NLM NOTEBOOK SETUP

**NLM is the primary analysis engine.** All selected sources MUST be added to NLM before analysis begins. NLM (Google NotebookLM) can ingest URLs that WebFetch cannot — including PDFs, paywalled articles, and YouTube videos.

### 4a. Create or Reuse Notebook

```bash
# If --notebook specified and exists:
nlm notebook query {{notebook}} "list sources"  # verify notebook alive

# If --notebook specified but new topic area, create dedicated notebook:
nlm notebook create "Research: {{topic}}"
nlm alias set {{short-alias}} {{new-uuid}}

# If no --notebook specified, ask CEO:
# "Dùng notebook nào? Existing: [list aliases] hoặc tạo mới?"
```

### 4b. Source Limit Check (v3.0)

Before bulk add, check current source count:
```bash
nlm source list {{notebook}} 2>&1 | wc -l
```
If current_count + new_sources > 45 (NLM limit ~50):
→ Warn CEO: "Notebook gần đầy ({{count}}/50). Tạo notebook phụ cho patent sources?"
→ CEO decides: add to existing or create sub-notebook

### 4c. Source Dedup Check (v3.0)

Before adding each source, check if already in notebook:
```bash
nlm source list {{notebook}} 2>&1
```
- URL match (substring) → skip, log "⚠ Already in notebook: {{title}}"
- Fuzzy title match (first 50 chars) → auto-skip with log in /research context (sources already CEO-selected in Step 3)

### 4d. Add ALL Selected Sources to NLM

For EACH selected source, try ingestion in priority order:

```
FOR each selected source URL:

  TRY 1 (preferred): nlm source add {{notebook}} --url "{{url}}"
    → NLM fetches directly (handles PDFs, YouTube, most web pages)
    → Works for: ieee.org, mdpi.com, researchgate.net, YouTube,
      ti.com, dtic.mil, most .gov sites, patents.google.com
    → Log: "✓ NLM ingested: {{title}}"

  IF TRY 1 fails:
  TRY 2: WebFetch content → nlm source add {{notebook}} --text "{{content}}"
    → Fetch via WebFetch, then inject as text source
    → Log: "⚠ NLM URL failed, injected as text: {{title}}"

  IF TRY 2 fails:
  TRY 3: WebSearch for alternative URL of same content → TRY 1 again
    → Search: "{{title}} {{author}}" to find mirror/preprint
    → Log: "⚠ Trying alternative URL: {{alt_url}}"

  IF ALL fail:
  FALLBACK: Log as "✗ Cannot ingest: {{title}} — Claude-only analysis"
    → Use WebSearch extracts for Claude inline analysis
    → Flag in Source Quality Report as "NLM gap"
```

**Important:** Run all `nlm source add` commands BEFORE any queries. NLM needs time to index sources.

### 4e. NLM Auth Detect-Pause (v3.0)

If ANY `nlm` command during Steps 4-5 returns auth error:

```
1. Log current pipeline state:
   - Sources added so far: [list]
   - Sources pending: [list]
   - Current step: [step #]
2. Prompt CEO: "⚠ NLM session expired. Chạy `nlm login`, rồi nói 'done'"
3. On CEO confirm → retry the failed command
4. Max retries: 2
5. If still fail after 2 retries → log "✗ NLM unavailable"
   → Switch remaining analysis to Auto-fallback Quick Mode (Claude-only)
   → Flag in Source Quality Report: "NLM unavailable — Claude-only analysis for {{N}} sources"
```

### 4f. Verify Sources Added + Source Quality Gate (v3.1)

After ALL `source add` calls complete, run verification:

```bash
nlm source list {{notebook}}
```

**1. Compare ingested vs selected:**

```
SOURCE INGESTION REPORT:
| # | Title | Tier | Status | Reason |
|---|-------|:----:|:------:|--------|
| 1 | {{title}} | S | ✅ OK | |
| 2 | {{title}} | A | ❌ FAILED | Paywall / 403 / timeout / JS-rendered |
| ...

Ingested: {{N}} / {{total selected}}
Failed: {{M}} sources (list below)
```

**2. For EACH failed source — try alternative recovery (AI Offload):**

```
FOR each failed source:

  RECOVERY 1: Search for alternative URL of same content
    → WebSearch: "{{title}} {{author}} filetype:pdf"
    → WebSearch: "{{title}} preprint OR mirror OR researchgate"
    → If found → nlm source add --url "{{alt_url}}"
    → Log: "🔄 Recovered via alt URL: {{alt_url}}"

  RECOVERY 2: Fetch content via WebFetch → inject as text
    → Try WebFetch on original URL (may work where NLM failed)
    → If content retrieved → nlm source add --text "{{content}}" --title "{{title}}"
    → Log: "🔄 Recovered via WebFetch→text injection"

  RECOVERY 3: Search for YouTube explanation of same content
    → If source is a paper/standard: search "{{title}} explained" on YouTube
    → If found relevant video → nlm source add --url "{{yt_url}}"
    → Log: "🔄 Substituted with YouTube explanation: {{yt_url}}"

  IF ALL RECOVERY FAILS:
    → Log: "✗ UNRECOVERABLE: {{title}} (Tier {{X}})"
    → Add to gap list for CEO manual action
```

**3. Present SOURCE QUALITY GATE to CEO (Core — do not skip):**

```markdown
═══ SOURCE QUALITY GATE — {{notebook}} ═══

INGESTION SUMMARY:
  ✅ Successfully ingested: {{N}} sources
  🔄 Recovered via alt channel: {{R}} sources
  ❌ Failed (unrecoverable): {{F}} sources

FAILED SOURCES (CEO action needed):
| # | Title | Tier | Why Failed | Impact |
|---|-------|:----:|-----------|--------|
| {{n}} | {{title}} | {{tier}} | {{paywall/403/JS}} | {{HIGH if S/A, LOW if C}} |

CEO OPTIONS:
(1) ✅ Proceed — current sources sufficient for research quality
(2) 📎 CEO adds sources manually:
    - "Tôi có PDF/link cho source {{X}} — add vào notebook"
    - AI sẽ chạy: nlm source add --url "{{ceo_url}}" hoặc --file "{{path}}"
    - Hoặc CEO tự add qua NLM web UI: {{notebook_url}}
(3) 🔍 Search deeper — AI tìm thêm alt sources cho các failed items
(4) ⏸️ Pause — CEO tự tìm nguồn offline rồi quay lại

QUALITY CHECK:
  Pro sources (S+A) in notebook: {{count}} / {{total S+A selected}}
  Pro ratio after ingestion: {{%}}
  ⚠️ If pro ratio < 50% after failures → WARN: research quality may be degraded

CEO: xác nhận notebook đủ nguồn + chất lượng? Chỉ khi CEO approve mới tiến hành query.
```

**STOP HERE. Do NOT proceed to Step 5 until CEO confirms source quality.**

**CEO confirmation triggers:**
- "(1)" or "proceed" or "đủ" → proceed to Step 5
- "(2)" + URL/file → add source, re-verify, re-present gate
- "(3)" → run additional search for failed sources
- "(4)" → pause pipeline, save state for resume

---

## STEP 5: ANALYSIS ROUTING

Route analysis depth by tier of selected sources.
**ALL analysis goes through NLM first** — NLM uses Gemini (FREE tokens). Claude analysis is supplementary.

### Deep Path (Tier S/A sources)

```
1. NLM deep query — 6-question framework (FREE — Gemini tokens):
   nlm notebook query {{notebook}} "Analyze all sources focusing on
   Tier S/A (standards and authority) content:
   (1) Core 3-5 principles?
   (2) System archetypes present?
   (3) Failure modes and warnings?
   (4) What must be true for claims to hold?
   (5) Ignored dimensions?
   (6) Rate-of-change dynamics?
   Cite specific sources for each finding."

2. NLM topic-specific query (tailored to research question):
   nlm notebook query {{notebook}} "{{specific OI-04 style question
   relevant to the design decision being researched}}"

3. If --deep flag: apply Deep Content Analyzer v2 on NLM output
   → First-Principles Debate
   → Three Laws extraction
   → Missing Dimensions checklist
   → ARCHITECT framework (if substantial enough)

4. Tag all insights with source tier + citation
```

### Standard Path (Tier B sources)

```
1. Sources already in NLM notebook (added in Step 4)
2. NLM standard query:
   nlm notebook query {{notebook}} "Extract from professional sources:
   (1) key insights, (2) actionable techniques,
   (3) warnings/pitfalls,
   (4) connections to existing knowledge"
3. Flag any claims that contradict Tier S/A findings
```

### Quick Path (Tier C sources)

```
1. Sources already in NLM notebook (added in Step 4)
2. NLM quick query:
   nlm notebook query {{notebook}} "Summarize community sources
   in 3 bullets each. Flag any claim that contradicts
   higher-tier (standards/authority) sources."
3. Only use Tier C for:
   - Gap filling (topics S/A sources don't cover)
   - Practical how-to (tutorials, demos)
   - Vietnamese-specific context
```

### Cross-Source Synthesis (MANDATORY — run after all paths)

```bash
nlm notebook query {{notebook}} "Synthesize ALL sources together:
(1) What do all sources agree on? (high confidence findings)
(2) Where do sources contradict each other? (flag for CEO)
(3) What questions remain unanswered? (coverage gaps)
(4) What is the single most important finding for: {{design question}}?
Distinguish between findings from standards vs community sources."
```

This synthesis query is the primary value of NLM — cross-referencing multiple sources simultaneously using FREE Gemini tokens instead of expensive Claude tokens.

### Critical Lens Queries (MANDATORY — run after cross-source synthesis)

3 additional NLM queries that catch blind spots the synthesis query misses. All FREE (Gemini tokens).

```bash
# CL-1: Contradiction Finder — systematic source-vs-source conflict detection
nlm notebook query {{notebook}} "Identify every point where two or more sources
directly contradict each other. For each contradiction:
- State both positions clearly
- Name the sources
- Explain WHY they likely disagree (methodology difference? dataset difference?
  era/vintage difference? different application context? different assumptions?)
- Rate severity: CRITICAL (changes design decision) / MODERATE (affects confidence)
  / MINOR (definitional or contextual)
Format as a table sorted by severity."
```

```bash
# CL-2: Assumption Killer — shared untested assumptions across ALL sources
nlm notebook query {{notebook}} "List every assumption that the MAJORITY of these
sources share but never explicitly test or justify. For each assumption:
- State it clearly
- Name 1-2 sources that rely on it most heavily
- Explain what would happen to the field's conclusions if this assumption
  turned out to be wrong
- Rate relevance to Vietnam defense manufacturing context: HIGH / MEDIUM / LOW
Focus especially on assumptions about: operating environment, manufacturing
capability, material availability, user skill level, maintenance infrastructure."
```

```bash
# CL-3: Methodology Audit — compare HOW sources reached their conclusions
nlm notebook query {{notebook}} "Compare the research methodologies used across
all sources. Group by: experiments, simulations, field tests, analytical models,
surveys, case studies, expert opinion. Then flag:
- Which methodology dominates this field and why?
- Which methodology is underused or absent?
- Which source's methodology is weakest and why?
- For Workshop X (defense hardware, Vietnam context): which methodology gap
  is most dangerous for design decisions?"
```

**Integration with Cross-Validate (Step 6):**
- CL-1 contradictions with severity CRITICAL → force CEO review before confidence scoring
- CL-2 assumptions → add as caveat to any ★★★ insight that depends on an untested assumption
- CL-3 methodology gaps → downgrade confidence if insight comes from weak/absent methodology

---

## STEP 6: CROSS-VALIDATE

After all paths complete, cross-validate insights:

```
CONFIDENCE SCORING PER INSIGHT:

★★★ HIGH: Confirmed by ≥1 Tier S/A source
★★  MED:  From Tier B only, no contradiction with S/A
★   LOW:  From Tier C only, OR contradicted by S/A source

CONTRADICTION HANDLING:
- If Tier C insight contradicts Tier S/A → flag as ★ LOW + note conflict
- If Tier B insight contradicts Tier S/A → flag for CEO review
- If Tier S contradicts Tier A → flag as research gap, both may be valid
```

---

## STEP 7: SAVE TO VAULT

Save the analysis output to: `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_{{topic_slug}}_{{date}}.md`

Enhanced frontmatter:

```yaml
---
created: {{today}}
source: research-pipeline-v3
notebook: {{notebook-alias}}
topic: "{{topic}}"
type: nlm-output
status: active
tags: [#type/nlm-output, #status/active]
source_quality:
  tier_s: {{count}}
  tier_a: {{count}}
  tier_b: {{count}}
  tier_c: {{count}}
  pro_ratio: "{{(S+A)/(total)}}%"
sources_analyzed:
  - title: "{{title}}"
    tier: S
    url: "{{url}}"
  - title: "{{title}}"
    tier: B
    url: "{{url}}"
---
```

### Insight Format (inside file)

```markdown
## Analysis

### Insight 1: {{insight title}}
- **Source tier:** {{S/A/B/C}} ({{source name}})
- **Confidence:** ★★★ HIGH
- **Cross-validated by:** {{other source if applicable}}
- **Citation:** {{author, title, year, URL}}
- **Galaxy candidate:** YES/NO/NEEDS VERIFICATION

### Insight 2: {{insight title}}
- **Source tier:** C ({{YouTube channel}})
- **Confidence:** ★ LOW — needs Tier A verification
- **Contradicts:** {{note if contradicts S/A source}}
- **Galaxy candidate:** NOT YET — cần pro source confirm
```

---

## STEP 8: FLAG GALAXY CANDIDATES

Scan insights for Galaxy promotion candidates:

```markdown
## Galaxy Candidates (THỊNH H — Hóa)

### ★★★/★★ — Ready for Promotion
1. "{{insight}}" → proposed title: {{Galaxy note title}}
   - Cluster: {{A-I}}
   - Links to: [[existing note 1]], [[existing note 2]]
   - Source: {{Tier S/A citation}}
   - Confidence: ★★★

### ★ — Needs Verification Before Galaxy
1. "{{insight}}" → potential title: {{title}}
   - Missing: {{what Tier S/A source would confirm this?}}
   - Search suggestion: "{{query to find pro source}}"

CEO: which ★★★/★★ candidates to promote to Galaxy? (Core decision)
CEO: any ★ insights worth pursuing with targeted search? (Core decision)
```

---

## STEP 9: SOURCE QUALITY REPORT

End every /research run with a quality summary:

```markdown
## Source Quality Report

| Metric | Value |
|--------|-------|
| Total sources found | {{N}} |
| Tier S (Standards) | {{N}} |
| Tier S (Patents) | {{N}} |
| Tier A (Authority) | {{N}} |
| Tier B (Professional) | {{N}} |
| Tier C (Community) | {{N}} |
| Pro ratio (S+A/total) | {{N}}% |
| Insights extracted | {{N}} |
| ★★★ HIGH confidence | {{N}} |
| ★★ MED confidence | {{N}} |
| ★ LOW confidence | {{N}} |
| Galaxy candidates | {{N}} ready, {{N}} needs verification |

### Patent Landscape (v3.0)
- Patents found: {{N}}
- Active patents potentially relevant: {{N}}
- ⚠ Freedom-to-operate concern: {{YES/NO}}
  - {{Patent # — why it might be relevant}}
- CEO: review flagged patents for FTO risk (Core decision)

### Coverage Gaps
- {{topic aspect}} — no Tier S/A source found
  → Suggested search: "{{specific query}}"
- {{topic aspect}} — only Tier C coverage
  → Suggested source: {{specific OEM/standard to check}}

### NLM Status
- NLM notebook: {{alias}} ({{source_count}} sources)
- NLM gaps: {{N}} sources failed ingestion → Claude-only
- Auto-fallback triggered: YES/NO

### Recommendation for Next Research
{{What to search next to fill gaps}}
```

---

## UPDATE MODE (v3.1)

Incremental research — add new sources to existing notebook, re-analyze with combined knowledge.

```
/research <topic> --update --notebook <existing-alias>
```

**When to use:** Topic was researched before, new papers/products/standards published since, CEO wants deeper coverage without losing existing analysis.

### Update Pipeline

```
[U1] LOAD EXISTING NOTEBOOK
     Read notebook source list → identify what's already there
     Read previous output: RESEARCH_{{slug}}_{{original_date}}.md
     ↓
[U2] INCREMENTAL SEARCH (same 4 channels as Step 1)
     Add time filter: "after:{{last_research_date}}" where possible
     Dedup against existing notebook sources (by URL + fuzzy title)
     ↓
[U3] PRESENT NEW SOURCES TO CEO (Core)
     Table showing: NEW sources found (not in notebook)
     Mark: which are genuinely new vs duplicates of existing
     CEO selects which new sources to add
     ↓
[U4] ADD NEW SOURCES + SOURCE QUALITY GATE
     Add selected new sources to EXISTING notebook (do NOT create new)
     Run Step 4G quality gate on NEW sources only
     CEO confirms "đủ nguồn mới"
     ↓
[U5] DELTA ANALYSIS (NLM queries on combined notebook)
     Query 1: "What NEW insights emerge from the recently added sources
              that were NOT present in the original analysis? Compare with
              previously known findings."
     Query 2: "Do any new sources CONTRADICT findings from the original
              sources? Flag conflicts."
     Query 3: "What coverage gaps from the original research are now filled
              by the new sources?"
     ↓
[U6] SAVE UPDATE OUTPUT
     File: RESEARCH_{{slug}}_update_{{today}}.md
     Format: Same as original + DELTA section
     Original file: UNTOUCHED (preserved as historical record)
     ↓
[U7] GALAXY CANDIDATES (new insights only)
```

### Update Output Format

```yaml
---
created: {{today}}
source: research-pipeline-v3.1-update
notebook: {{same notebook alias}}
topic: "{{topic}}"
type: nlm-output-update
status: active
update_of: "RESEARCH_{{slug}}_{{original_date}}.md"
original_date: {{original_date}}
tags: [#type/nlm-output, #status/active]
source_quality:
  existing_sources: {{N}}
  new_sources_added: {{M}}
  total_after_update: {{N+M}}
---

# {{topic}} — Research Update ({{today}})

## Previous Research
- Original: `RESEARCH_{{slug}}_{{original_date}}.md`
- Sources at time: {{N}}
- Key findings: {{brief summary of original 3-5 insights}}

## New Sources Added (this update)
| # | Title | Tier | Type | Why new |
|---|-------|:----:|------|---------|
| 1 | {{title}} | {{tier}} | {{type}} | Published after {{original_date}} / missed in original |

## Delta Analysis

### New Insights (not in original)
1. **{{insight}}** — Source: {{new source}} — Confidence: ★★★/★★/★
   - Changes original finding #X? YES/NO

### Contradictions with Original
1. **{{conflict}}** — Original said: {{X}} — New source says: {{Y}}
   - Resolution: {{CEO judgment needed / new source supersedes / both valid in context}}

### Coverage Gaps Filled
| Gap (from original) | Now filled by | Confidence |
|---------------------|--------------|:----------:|
| {{gap}} | {{new source}} | ★★★ |

### Remaining Gaps (still open)
| Gap | Still missing |
|-----|--------------|

## Updated Galaxy Candidates (new insights only)
...

## Source Quality Report (update)
| Metric | Original | After Update |
|--------|:--------:|:------------:|
| Total sources | {{N}} | {{N+M}} |
| Tier S+A | {{x}} | {{x+y}} |
| Pro ratio | {{%}} | {{%}} |
```

### Update Rules
- **NEVER modify the original output file** — it's a historical record
- **NEVER remove existing sources from notebook** — only add new ones
- **Dedup is critical** — same URL or fuzzy title match = skip (do not re-add)
- **Time-scoped search when possible** — reduces noise from already-known sources
- **Delta focus** — NLM queries specifically ask "what's NEW" vs "what was already known"
- If `--notebook` not specified → search for most recent `RESEARCH_{{topic_slug}}_*.md` in vault, extract notebook alias from frontmatter

---

## QUICK MODE

Two variants:

### User-chosen Quick Mode
For fast research without NLM (when NLM not needed or quick scan):

```bash
yt-dlp "ytsearch5:{{topic}}" --flat-playlist --print "%(id)s | %(title)s | %(duration_string)s | %(view_count)s views" --no-download
```

Then use Claude Code's own analysis + WebSearch for pro sources.
Tier classification still applies in quick mode.

### Auto-fallback Quick Mode (v3.0)
Triggered automatically when NLM auth fails mid-pipeline after 2 retry attempts.
Same Claude-only analysis approach, but logs: "⚠ Auto-fallback: NLM unavailable, using Claude-only analysis"
Flagged in Source Quality Report under "NLM Status" section.

---

## NOTEBOOK MANAGEMENT

→ See `references/notebooks.md` for full alias registry, management commands, and source limit rules.

---

## EXTRACTION TEMPLATES (v4.0)

3 structured NLM extraction modes for Step 5 analysis. Use with `--extract <mode>` to replace or augment the default analysis queries. These produce structured, paste-ready output tables.

### `--extract miner` — Data Mining Mode

Replaces default Step 5 queries with structured data extraction. Produces 5 tables of quantitative data and heuristics from all ingested sources.

```bash
nlm notebook query {{notebook}} "Extract ALL quantitative data and heuristics into 5 structured tables:

TABLE 1 — Design Rules & Heuristics:
| Rule/Heuristic | Phase/Context | Numerical Value | Source | Confidence |

TABLE 2 — Evaluation Criteria:
| Criterion | Weight Range | Scoring Scale | Application Domain | Source |

TABLE 3 — Checklist Items:
| Checklist Topic | Phase | Items Count | Key Questions | Source |

TABLE 4 — Formulas & Calculations:
| Formula Name | Equation | Variables | Units | Application | Source |

TABLE 5 — Design-for-X Guidelines:
| DfX Category | Specific Guidelines | Quantitative Limits | Trade-offs | Source |

Include hidden numbers embedded in text (e.g. '80% of cost locked at conceptual phase'). Format for direct paste into markdown."
```

**When to use:** Building reference sheets, populating HELIX templates (requirements list, VDI 2225 scorecard, DfX checklists), extracting actionable parameters from textbooks/standards.

**Output:** Appended to standard research output as `## Extracted Data Tables` section.

### `--extract cross-std` — Cross-Standard Synthesis Mode

Produces mapping matrices across multiple standards/methodologies. Essential for defense products needing multi-standard compliance.

```bash
nlm notebook query {{notebook}} "Synthesize content across standards and methodologies. Create:

TABLE A — Phase Mapping Matrix:
| P&B Phase | VDI 2221 Step | VDI 2206 V-model Stage | Relevant MIL-STD | STANAG | Vietnam TCVN/TCQS |

TABLE B — Key Intersections:
| Domain | Standard A | Standard B | Where They Connect | Gap/Conflict |

Examples to look for:
- Requirements List ↔ MIL-STD-961 (Defense Specifications)
- Function Structure ↔ SysML block diagrams (MBSE)
- VDI 2225 evaluation ↔ DoD Architecture Framework decision analysis
- Embodiment Design ↔ MIL-HDBK-5 (metallic materials) / MIL-HDBK-17 (composites)
- Detail Design ↔ ASME Y14.5 (GD&T) / ISO 1101
- Design Review ↔ MIL-STD-1521 (Technical Reviews and Audits)

TABLE C — Vietnam Context Gaps:
| Standard/Practice | VN Has Equivalent? | VN-Specific Adaptation Needed | Impact on Workshop X |

Conclude with: Recommended integrated design process framework for Workshop X."
```

**When to use:** Before starting HELIX pipeline for new product (understand which standards apply), compliance mapping for defense contracts, building integrated process from multiple methodology sources.

**Output:** Appended as `## Cross-Standard Mapping` section.

### `--extract structure` — Content Structure Navigation Mode

Produces reading paths and concept hierarchies for dense technical material. Optimizes learning time allocation.

```bash
nlm notebook query {{notebook}} "Analyze the structure of all content and produce:

LEVEL 1 — One-line summary per major section/chapter

LEVEL 2 — Key concepts hierarchy:
| Concept | Category | Dependencies |
Categories: Foundational (must read first), Advanced (skip on first read), Reference (lookup when needed)

LEVEL 3 — Topic-based navigation for Workshop X focus areas:
| Focus Area | Most Important Sections | Page/Section References |
Focus areas: requirements engineering, function structure, concept evaluation (VDI 2225), embodiment principles, DfM for Vietnam capability, reverse engineering methodology, mechatronic system design (VDI 2206)

LEVEL 4 — Reading paths:
| Path | Hours | What It Covers | Best For |
- Fast track (~40h): only what's needed for current project
- Comprehensive (~120h): master entire methodology
- Specialist: deep in 1 phase only

Show dependencies between sections as ordered list."
```

**When to use:** Starting a `/learning --mode practice` cycle (need to know what to study first), onboarding to a new textbook/standard, CEO time optimization for reading dense material.

**Output:** Appended as `## Content Structure Map` section.

### Extraction Template Integration

| Extract Mode | Step 5 Impact | Output Location |
|-------------|---------------|-----------------|
| `miner` | Replaces default analysis queries for all tiers | `## Extracted Data Tables` |
| `cross-std` | Adds after cross-source synthesis query | `## Cross-Standard Mapping` |
| `structure` | Runs as pre-analysis (before tier routing) | `## Content Structure Map` |

Multiple extraction modes can be combined: `--extract miner --extract cross-std`

Extraction templates work with both default and `--update` modes. In update mode, extraction focuses on NEW sources only.

### NLM Knowledge Base Setup (auto-generate reports + quiz + persona)

When a research notebook is created with `--extract` mode, auto-generate persistent reports and set up chat persona for later CEO reference.

**Step RKB-1: Set Chat Persona** (auto-configured via MCP)

Use `mcp__notebooklm-mcp__chat_configure` to set persona automatically — no manual paste needed.

```
chat_configure(
  notebook_id={{uuid}},
  goal="custom",
  response_length="longer",
  custom_prompt="PERSONA — RESEARCH ANALYST FOR WORKSHOP X

You are a senior research analyst at Workshop X, a Vietnam defense manufacturer with 1,064+ hardware units shipped. Your role is to help the CEO extract actionable engineering knowledge from uploaded sources. You specialize in:
- Source tier assessment (S=Standards/Primary, A=Authority/OEM, B=Professional, C=Community)
- Cross-standard mapping (VDI 2221, VDI 2206, MIL-STD, STANAG, TCVN)
- Quantitative data extraction (heuristics, formulas, thresholds, design rules)
- Vietnam defense manufacturing context (ITAR-free, domestic capability, tropical maritime)

RULES:
- Always cite specific sources with confidence levels (HIGH/MED/LOW)
- Flag contradictions between sources explicitly
- When extracting numbers, include units and applicable context/constraints
- Distinguish between established engineering data (S/A tier) and community opinions (C tier)
- Format output as structured tables when extracting data
- Flag items relevant for Galaxy permanent notes (atomic insights that change design thinking)
- Always consider tropical maritime degradation when discussing sensor/hardware performance
- Design recommendations must account for conscript-level operator skill"
)
```

**Step RKB-2: Generate Extraction Reports** (after Step 4G source quality gate passed)

```bash
# Report 1: Data Mining (5 tables)
nlm notebook query {{notebook}} "Extract ALL quantitative data into 5 tables: TABLE 1 Design Rules & Heuristics (Rule, Phase, Value, Source). TABLE 2 Evaluation Criteria (Criterion, Weight, Scale, Domain). TABLE 3 Checklist Items (Topic, Phase, Count, Questions). TABLE 4 Formulas (Name, Equation, Variables, Units). TABLE 5 DfX Guidelines (Category, Guidelines, Limits, Trade-offs). Include hidden numbers in text."

# Report 2: Cross-Standard Synthesis
nlm notebook query {{notebook}} "Create mapping matrices: TABLE A Phase Mapping (P&B Phase vs VDI 2221 vs VDI 2206 vs MIL-STD vs STANAG vs TCVN). TABLE B Key Intersections (Requirements↔MIL-STD-961, Function Structure↔SysML, VDI 2225↔DoD AF, Embodiment↔MIL-HDBK-5/17, Detail↔ASME Y14.5, Review↔MIL-STD-1521). TABLE C Vietnam Gaps (standard, VN equivalent exists?, adaptation needed, WX impact)."

# Report 3: Content Structure Navigation
nlm notebook query {{notebook}} "Map content structure: Level 1 one-line summary per section. Level 2 concept hierarchy (foundational/advanced/reference). Level 3 topic navigation for WX focus areas (requirements, function structure, VDI 2225, embodiment, DfM Vietnam, RE, mechatronic VDI 2206). Level 4 reading paths: fast track 40h, comprehensive 120h, specialist per phase."

# Report 4: Failure Mode Analysis
nlm notebook query {{notebook}} "Extract design failure modes per phase: Task Clarification (requirements creep, missing stakeholders, untestable requirements), Conceptual (anchoring, incomplete function structure, biased evaluation), Embodiment (over-engineering, premature optimization, skipping DfX, tolerance stack-up), Detail (drawing errors, BOM inconsistency). Per failure: symptom, root cause, prevention, detection stage, recovery, defense example. Rank top 10 by RPN for Vietnam defense context."

# Report 5: Quiz + Flashcards
nlm notebook query {{notebook}} "Create assessment materials: PART A (10 MCQ): test understanding of core concepts, distinguish easily confused terms, edge cases. PART B (5 application scenarios): real Vietnam defense engineering situations requiring this knowledge. Each answer with: explanation, why others wrong, pitfalls, source reference, Bloom's level. PART C: 20 flashcard pairs (Question | Answer | Difficulty) covering key data points, formulas, and rules of thumb."
```

**Step RKB-3: Generate Studio Artifacts** (persistent learning materials in NLM UI)

After NLM conversation queries (RKB-2) are complete, generate persistent Studio artifacts. These are accessible via NLM notebook UI even after conversation context expires — CEO's long-term reference library.

**CEO gate:** "Tạo bộ Studio artifacts (quiz, flashcards, reports, audio) trong NLM? ~5 phút."
**Trigger:** Auto-suggest after RKB-2 completes. CEO can skip if only needs conversation reports.

Use `mcp__notebooklm-mcp__studio_create` MCP tool for ALL artifacts. Do NOT use `nlm audio create` CLI (not supported).

**CRITICAL — Prompt Quality Rule:**
- NEVER use generic focus_prompts → NLM auto-generates shallow, generic content
- Every artifact MUST include WX-specific context: product names, VN defense, tropical maritime, competitors
- Quiz: VN scenarios + Bloom's taxonomy + source references
- Flashcards: Easy/Medium/Hard tiers + key numbers + doctrine + design rules
- Reports: Situation-Complication-Resolution structure with WX product implications
- Audio: focus on contradictions, warnings, and WX-specific design decisions

**6 artifacts to generate (parallel where possible):**

```
# Artifact 1: Quiz (hard, WX scenarios)
studio_create(notebook_id={{uuid}}, artifact_type="quiz", question_count=10, difficulty="hard",
  focus_prompt="PART A (10 MCQ): test {{topic}} concepts for Vietnam defense manufacturer CEO.
  Include: (1) easily confused terms from this domain, (2) edge cases from contradictions
  found in cross-source analysis, (3) Vietnam-specific context (tropical maritime, conscript
  operators, ASEAN export advantage). Each answer: why correct, why others wrong, source
  reference, Bloom's taxonomy level.
  PART B (5 application scenarios): real Vietnam defense engineering situations at Workshop X
  applying {{topic}} knowledge. Reference specific WX products where relevant.",
  confirm=True)

# Artifact 2: Flashcards (Easy/Medium/Hard, 20 cards)
studio_create(notebook_id={{uuid}}, artifact_type="flashcards", difficulty="medium",
  focus_prompt="20 flashcard pairs organized by difficulty:
  EASY (7): key definitions, acronyms, market numbers from sources.
  MEDIUM (7): doctrine references, competitor products/specs, architecture components.
  HARD (6): contradictions between sources, hidden assumptions, design rules,
  VN-specific adaptations needed.
  All data points must be directly actionable for Workshop X product decisions.",
  confirm=True)

# Artifact 3: Briefing Doc (SCR format, WX-specific)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Briefing Doc",
  focus_prompt="WORKSHOP X CEO EXECUTIVE BRIEFING — {{topic}}
  Structure: (1) SITUATION: market/technology landscape with specific numbers from sources.
  (2) COMPLICATION: gaps, contradictions, risks specific to Workshop X Vietnam.
  (3) WX ADVANTAGE: how existing portfolio ({{list relevant products}}) addresses gaps.
  (4) KEY DECISIONS: specific go/no-go questions for CEO with evidence.
  (5) COMPETITIVE LANDSCAPE: who does what, what no one does (product gap).
  (6) RISK WARNINGS: from Critical Lens analysis (CL-1 contradictions, CL-2 assumptions).
  Cite specific sources with tier levels (S/A/B/C).",
  confirm=True)

# Artifact 4: Study Guide (ordered learning path)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Study Guide",
  focus_prompt="WORKSHOP X ENGINEERING TEAM STUDY GUIDE — {{topic}}
  Structure as ordered 6-step learning path (dependencies matter):
  Step 1 FOUNDATION: why this topic matters for WX (regulatory, market, threat).
  Step 2 FRAMEWORK: standards, doctrine, methodology references.
  Step 3 ARCHITECTURE: how systems/products work (subsystems, interfaces).
  Step 4 TECHNICAL DEPTH: specs, physics, sensor performance, formulas.
  Step 5 METHODOLOGY: how to apply knowledge (design process, evaluation criteria).
  Step 6 VIETNAM CONTEXT: tropical maritime, conscript operators, domestic sourcing, ASEAN export.
  For each step: key sources to read, data points to memorize, WX design decisions, test questions.",
  confirm=True)

# Artifact 5: Audio Deep Dive
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="deep_dive",
  language="vi",
  focus_prompt="Focus on key findings for Workshop X Vietnam: {{top 3-5 findings from
  cross-source synthesis, with specific WX product implications}}. Cover competitive
  landscape and critical design warnings for Vietnam context.",
  confirm=True)

# Artifact 6: Audio Critique (judgment development)
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="critique",
  language="vi",
  focus_prompt="Critically evaluate contradictions found in this research: {{list top 3
  contradictions from CL-1}}. Challenge hidden assumptions: {{list top 3 from CL-2 with
  VN relevance HIGH}}. What could go wrong for a Vietnam manufacturer? What methodology
  gaps are most dangerous for design decisions?",
  confirm=True)
```

**Verify all 6 complete:**
```
studio_status(notebook_id={{uuid}})
# All 6 should show status: completed
# Audio artifacts may take 3-5 minutes
```

**Step RKB-4: Save KB Index**

Save to: `3_Resources/Deep-Content-Analyzer-Outputs/NLM_KB_RESEARCH_{{topic}}_{{date}}.md`

```markdown
# NLM Knowledge Base — Research: {{topic}}
Notebook: {{alias}}
Created: {{today}}
NLM conversation reports: 5 (Data Mining, Cross-Standard, Structure, Failures, Quiz)

## Studio Artifacts (persistent in NLM UI)
| # | Title | Type | Status |
|---|-------|------|:------:|
| 1 | {{title}} | Quiz (MCQ + Scenarios) | ✅/⏳ |
| 2 | {{title}} | Flashcards (Easy/Med/Hard) | ✅/⏳ |
| 3 | {{title}} | Briefing Doc (SCR format) | ✅/⏳ |
| 4 | {{title}} | Study Guide (6-step path) | ✅/⏳ |
| 5 | {{title}} | Audio Deep Dive | ✅/⏳ |
| 6 | {{title}} | Audio Critique | ✅/⏳ |

## Chat Persona
Persona pasted: YES/NO

## How to Use in NLM Chat
- "Cho toi formula cho X" → pulls from Data Mining report
- "Standard nao ap dung cho phase Y?" → pulls from Cross-Standard report
- "Doc gi truoc khi bat dau phase Z?" → pulls from Structure report
- "Sai lam thuong gap khi lam X?" → pulls from Failure Mode report
- "Test kien thuc cua toi ve Y" → pulls from Quiz report + Studio Quiz
```

---

## RULES

- **MANDATORY:** ALWAYS present source table and ask "CEO: chọn sources nào để analyze?" — NEVER auto-select sources. Step 3 is Core, not Offload. Output MUST contain "CEO" + "chọn" or "select" in source selection step.
- **MANDATORY:** After source ingestion (Step 4), ALWAYS run Source Quality Gate (Step 4G). Verify ingested count vs selected count. For failed sources: try alt URL → WebFetch→text → YouTube substitute. Present gap report to CEO. NEVER proceed to Step 5 queries without CEO confirming "đủ nguồn". CEO may add sources manually via NLM web UI or provide local PDF/link. This is Core, not Offload.
- NEVER download full video files — metadata and NLM ingestion only
- NLM auth: pre-check before Step 4 + detect-pause mid-pipeline + max 2 retries + auto-fallback
- Session lifetime ~20 min — pre-check catches most expirations
- NLM analysis is FREE (Gemini tokens) — prefer NLM over Claude for heavy analysis
- **MANDATORY: Save output** to `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_{{slug}}_{{date}}.md` — EVERY run must produce a saved file. Never skip Step 7.
- **MANDATORY: Flag Galaxy candidates** — EVERY run must end with Step 8 listing ★★★/★★ insights as Galaxy candidates with proposed note titles. Never skip Step 8.
- Galaxy extraction is Core — AI proposes, CEO decides
- **Only ★★★/★★ insights qualify for Galaxy promotion** — ★ needs verification first
- **Pro sources first** — always search S/A channels before presenting C sources
- **Cross-validate** — never present Tier C insight as fact without S/A confirmation
- **--deep flag** activates Deep Content Analyzer v2 for Tier S/A sources
- **--patents flag** forces Channel 4 patent search even for non-technical topics
- **Source dedup** — check before adding to NLM, auto-skip duplicates with log
- **Source limit** — warn at 45+ sources in notebook, suggest sub-notebook
- Link to Galaxy: [[Analyst Trap]] (extract insights, don't just collect), [[Vault = Graveyard]] (use what you save), [[Reliability Trumps Precision]] (pro sources > many sources)

## Gotchas (from production use)

1. **NLM notebook hits 50-source cap faster than expected** — 4-channel search (15 web + 5 YouTube + 10 authority + 15 patents) = 45 sources BEFORE dedup. Always dedup + let CEO prune BEFORE adding to NLM. Session 52 needed prune scripts for 6 notebooks. (Source: Session 50 prune, Session 52 research pipelines)
2. **Espacenet and IEEE = WebFetch blind spots** — Espacenet is JS-rendered (always fails). IEEE often paywalled. For these, rely on NLM URL ingestion (TRY 1) — NLM handles both. If NLM also fails, use search snippet only. Do NOT waste retries on known-failing domains. (Source: Session 52 patent search)
3. **Pro ratio is misleading when patents inflate Tier S count** — 10 patents + 2 papers = 80% "pro ratio" but actual analytical depth is shallow. Report patent count SEPARATELY from paper/standard count. "12 Tier S (10 patents, 2 papers)" is honest; "80% pro" is not. (Source: HDPE hull research)
4. **NLM auth expires mid-pipeline ~20 min** — The detect-pause protocol works, but the REAL gotcha is running Steps 4-5 sequentially on 20+ sources. Batch source adds (all in Step 4) BEFORE any queries (Step 5). Interleaving add→query→add→query doubles auth exposure window. (Source: Session 52, 3 pipelines)
5. **Skipping source verification = garbage-in-garbage-out** — Session 56 lost 3/21 sources (2 ScienceDirect paywall + 1 core.ac.uk 502) and proceeded to NLM queries without notifying CEO. NLM then analyzed only 19/21 sources but reported confidence as if all 21 were present. The Source Quality Gate (Step 4G) now STOPS the pipeline for CEO verification. Recovery options (alt URL, WebFetch→text, YouTube substitute) catch 50-70% of failures. CEO can also manually add PDFs they have locally. NEVER proceed to Step 5 without CEO confirming "đủ nguồn". (Source: Session 56 VDI 2221 research)
6. **YouTube view count ≠ credibility** — A 500K-view "tutorial" by non-engineer is still Tier C. Check channel credentials (description, about page) before promoting to Tier B. "Professional" means the creator has verifiable domain expertise, not just production quality. (Source: semi-sub USV research, multiple Tier C misclassifications)

## COD CLASSIFICATION

| Task | COD | Notes |
|------|-----|-------|
| Multi-channel search (4 channels) | O | Mechanical, parallel |
| Tier classification | O | Heuristic-based |
| Source selection | **C** | CEO judgment — informed by tier |
| Patent FTO review | **C** | CEO reviews flagged patents |
| NLM auth management | O | Auto pre-check + detect-pause |
| Deep analysis (S/A) | O | NLM + Deep Content Analyzer |
| Standard analysis (B) | O | NLM query |
| Cross-validation | O | AI compares, CEO validates |
| Confidence scoring | O | AI proposes ★★★/★★/★ |
| Galaxy promotion | **C** | CEO decides — only ★★★/★★ |
| Source quality report | O | Feedback for next search |
