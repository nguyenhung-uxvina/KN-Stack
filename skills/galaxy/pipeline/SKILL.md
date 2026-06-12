---
name: pipeline
description: "Manages the full signal-to-knowledge pipeline for the IPARAG vault — from raw capture through routing, storage, retrieval, and harvest. The BRIDGE-level orchestrator covering Inbox status, project decisions, Galaxy note growth, and resource staleness. Use to check pipeline health or trigger ingest/audit/harvest operations. Triggers on: \"pipeline status\", \"knowledge pipeline\", \"pipeline audit\", \"vault health\", \"kiem tra pipeline\", \"trang thai he thong\", \"kiểm tra kho tri thức\", \"luồng tri thức\"."
---

Manage the full signal-to-knowledge pipeline — from raw capture through routing, storage, retrieval, and harvest. The BRIDGE-level orchestrator for knowledge flow.

Unlike /signal (extracts signals from a single source), /pipeline manages the SYSTEM: what's flowing, what's stuck, what's being used, and what's rotting.

Usage: /pipeline [mode] where mode = status | ingest | audit | harvest

---

## MODE 1: STATUS (pipeline health dashboard)

If $ARGUMENTS = "status" or no arguments:

1. Scan the vault:
   - `0_Inbox/` — count items, age of oldest
   - `1_Projects/*/decisions/` — recent decision records (from /teach)
   - `5_Galaxy/` — count notes, recent additions, link density
   - Recent /signal outputs (if saved)
   - `3_Resources/` — check for stale items (>3 months untouched)

2. Generate:

```
# KNOWLEDGE PIPELINE STATUS — {{today}}

---

## FLOW METRICS

| Stage | Count | Health | Action |
|-------|-------|--------|--------|
| Inbox (raw capture) | {{N items}} | {{GREEN if 0-5, YELLOW if 6-15, RED if >15}} | {{process or OK}} |
| Signals extracted (this week) | {{N}} | {{GREEN if >3, YELLOW if 1-2, RED if 0}} | |
| Signals routed (this week) | {{N}} | {{GREEN if = extracted, RED if gap}} | |
| Galaxy notes created (this week) | {{N}} | {{GREEN if >3, RED if 0}} | |
| Decisions recorded (this week) | {{N}} | {{from /teach records}} | |
| Galaxy notes USED in decisions | {{N}} | {{harvest effectiveness}} | |

## PIPELINE BOTTLENECK
{{Which stage has the biggest gap between input and output?}}
- Capture → Extract: {{flow rate}}
- Extract → Route: {{flow rate}}
- Route → Store (Galaxy/Project): {{flow rate}}
- Store → Retrieve → Use: {{flow rate — hardest to measure}}

**Binding constraint:** {{which stage is the bottleneck and why}}

---

## INBOX STATUS
- Items: {{N}}
- Oldest item: {{age in days}}
- Inbox Zero achieved this week? {{Y/N}}

## GALAXY HEALTH
- Total notes: {{N}} / 50 target (6-week)
- Notes added this week: {{N}}
- Average link density: {{N}} (target: >=3)
- Physical:Framework ratio: {{%}} (target: >20%)
- Orphan notes (0-1 links): {{list}}
- Stale notes (>30 days no update): {{list}}

## NLM PIPELINE HEALTH
- Active notebooks: {{N}} (list aliases from MEMORY.md: kpipe, ast, rcs, lomah, 127sim, ach, mcp-agent)
- Total sources: {{estimate from known notebooks}}
- Stale notebooks (>30d no query): {{list}}
- Near capacity (>45 sources): {{list}}
- Auth: {{run `nlm notebook list` with NO_COLOR=1 — ✓ if returns data, ✗ if auth error}}

## GALAXY LINK HEALTH
- Avg link density: {{scan frontmatter `links:` field of all Galaxy notes, count per note, average}}
- Notes below minimum (< 2 links): {{list}}
- Cross-cluster ratio: {{% of links going to different cluster than source}}
- Last /galaxy-links scan: {{check progress.md or galaxy-state.md for date}}
- Recommendation: {{run scan if >30d since last, or if notes < 2 links exist}}

## RESOURCE DECAY CHECK
- Resources untouched >3 months: {{list top 5}}
- Action: Archive or delete per CLAUDE.md rule

## DECISION KNOWLEDGE LOOP
- Decisions recorded (all time): {{N}}
- Decisions with Outcome filled: {{N}} / {{total}}
- Overdue reviews (validation date passed, outcome = TBD): {{list}}
```

---

## MODE 2: INGEST (batch process multiple sources)

If $ARGUMENTS = "ingest":

1. Ask: What sources do you want to process? Options:
   a) All items in 0_Inbox/
   b) A specific document or meeting notes
   c) Recent session outputs (design reviews, analyses)

2. For each source, run /signal extraction logic inline:
   - Extract signals (FACT / INSIGHT / QUESTION / WARNING)
   - Propose routing (Project / Galaxy / Area / Archive / Delete)
   - Group by destination

3. Present batch routing plan:

```
# BATCH INGEST — {{today}}
**Sources processed:** {{N}}

## ROUTING PLAN

### → Projects
| Source | Signal | Project | Update Target |
|--------|--------|---------|---------------|

### → Galaxy (new permanent notes)
| Source | Signal | Proposed Title | Cluster | Hub Link |
|--------|--------|---------------|---------|----------|

### → Areas (dashboard updates)
| Source | Signal | Area | What to update |
|--------|--------|------|----------------|

### → Archive (processed, no further action)
| Source | Reason |
|--------|--------|

### → Delete (noise, no value)
| Source | Reason |
|--------|--------|

### → NLM Notebooks (source ingestion)
{{For each source routed to a project with an associated NLM notebook alias, suggest adding as NLM source}}
| Source | Notebook Alias | Reason |
|--------|---------------|--------|
| {{URL or file}} | {{alias from: kpipe, ast, rcs, lomah, 127sim, ach, mcp-agent}} | Relevant to {{project}} research |

{{Only show this section if routed sources match a project with known NLM notebook. Use alias mapping from MEMORY.md.}}

## CEO REVIEW NEEDED
{{list items where routing is ambiguous — these are Core decisions}}
```

4. Wait for CEO approval before executing any moves.

---

## MODE 3: AUDIT (quarterly knowledge quality review)

If $ARGUMENTS = "audit":

1. Deep scan of Galaxy:
   - Read all files in `5_Galaxy/`
   - Check each note against quality criteria from CLAUDE.md

2. Generate:

```
# GALAXY QUALITY AUDIT — {{today}}

## QUANTITATIVE METRICS
- Total notes: {{N}}
- Average link density: {{avg}} (target: >=3)
- Notes below 2 links: {{list — these violate CLAUDE.md rule}}
- Physical:Framework ratio: {{%}} (target: >20%)
- Cluster distribution: {{count per cluster A-H}}
- Cluster gaps: {{clusters with <3 notes}}

## QUALITATIVE CHECKS (spot-check 5 random notes)
| Note | Atomic? | Own Words? | Answers >=1 Question? | Links Valid? | Score |
|------|---------|-----------|----------------------|-------------|-------|
{{sample 5 notes, check quality}}

Questions each note must answer at least 1:
1. Changes how I design?
2. Changes a strategic decision?
3. Warns about a trap?

## LINK NETWORK ANALYSIS (enhanced — runs /galaxy-links scan logic)
- Hub notes (>5 incoming): {{list}}
- Bridge notes (connect 2+ clusters): {{list}}
- Isolated notes (1 cluster only, low links): {{list — candidates for cross-linking}}
- Missing links found: {{N}} (from /galaxy-links scan — run inline if audit, skip if just status)
- Cluster bridge gaps: {{table from galaxy-links scan}}
- Orphan risk notes (≤1 cross-cluster link): {{list}}
- **Action:** Run `/galaxy-links scan` for full link suggestions if gaps found

## LEARNING REFRESH CHECK
- Past /learning outputs: {{N}} (search `3_Resources/Deep-Content-Analyzer-Outputs/LEARN_*.md`)
- Outputs > 90 days old: {{list with last refresh date}}
- Never refreshed: {{list — files without "## Refresh" section}}
- Recently refreshed (valid): {{list with next refresh date}}
- **Recommendation:** Run `/learning --mode refresh` on {{oldest unrefreshed or most stale}}

## DECAY DETECTION
- Notes not updated in >90 days: {{list}}
- Are they still valid? (flag for CEO review)

## GROWTH TRAJECTORY
- Notes created per month: {{trend}}
- On track for 50-note target? {{Y/N, ETA}}
- Recommended focus: {{which cluster needs growth}}

## RECOMMENDATIONS
1. {{highest-impact improvement}}
2. {{second}}
3. {{third}}
```

---

## MODE 4: HARVEST (find Galaxy knowledge relevant to current work)

If $ARGUMENTS = "harvest" or $ARGUMENTS = "harvest [topic]":

1. If topic provided, search Galaxy for relevant notes
   If no topic, read active project Status.md files to identify current decisions/blockers

2. For each active decision or blocker:
   - Search Galaxy notes for relevant insights
   - Search decision records for analogous past decisions
   - Surface connections the CEO might not see

3. Generate:

```
# KNOWLEDGE HARVEST — {{today}}

## CURRENT WORK CONTEXT
{{from Status.md: active decisions, blockers, open questions}}

## RELEVANT GALAXY INSIGHTS

### For: {{decision/blocker 1}}
- [[Galaxy Note A]] — {{why it's relevant}}
- [[Galaxy Note B]] — {{connection}}
- **Synthesis:** {{how these notes inform this decision}}

### For: {{decision/blocker 2}}
- {{similar}}

## ANALOGOUS PAST DECISIONS
| Current Question | Past Decision (DR#) | Outcome | Lesson |
|-----------------|---------------------|---------|--------|
{{from /teach decision records}}

## MISSING KNOWLEDGE
{{topics where no Galaxy note exists but CEO needs insight}}
- {{topic}} — consider creating a note after this decision
- {{topic}} — search 3_Resources/ for existing material

## SERENDIPITY (unexpected connections)
{{any cross-cluster links that surprised the analysis}}
- [[Note X]] + [[Note Y]] → {{novel insight the CEO might find useful}}

## NLM CROSS-PRODUCT INSIGHTS
{{For active project blockers, check if 2+ NLM notebooks are relevant}}
{{Known aliases: kpipe, ast, rcs, lomah, 127sim, ach, mcp-agent}}

| Blocker/Question | Relevant Notebooks | Suggested Command |
|-----------------|-------------------|-------------------|
| {{blocker}} | {{alias1}}, {{alias2}} | `/nlm cross-query {{alias1}} {{alias2}} "{{question}}"` |

{{Suggest only — don't auto-run. Cross-query is token-heavy.}}
{{Only show this section if 2+ notebooks are relevant to the same blocker.}}
```

RULES:
- Pipeline is BRIDGE-level — it manages the system, not individual signals (/signal does that)
- Inbox Zero is a weekly target — /pipeline status should flag when inbox is growing
- Galaxy growth without USAGE is the Vault = Graveyard pattern — harvest mode prevents this
- Resources >3 months untouched must be archived per CLAUDE.md
- Decision records from /teach feed the harvest — this closes the judgment learning loop
- Never move files without CEO approval — always present the routing plan first
- Audit mode should run quarterly (integrate with /sync monthly review)
- Harvest is the most valuable mode — it turns stored knowledge into active decisions
- COD: Pipeline management is Offload, routing decisions are Core, Galaxy writing is Core
- Link to Galaxy: Vault = Graveyard, Analyst Trap, Activation Threshold, Serendipity
