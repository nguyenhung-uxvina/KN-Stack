Interact with Google NotebookLM via nlm-cli v2.0. Query notebooks, add sources, generate reports/audio/quizzes, cross-query multiple notebooks, check health, and save outputs to the IPARAG vault.

Usage: /nlm [mode] where mode = query | add | generate | list | cross-query | health | persona | deep-research

IMPORTANT: nlm sessions last ~20 minutes. If any command fails with auth error, tell the user to run `nlm login` in a separate terminal.

PATH: nlm.exe is at C:/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts/nlm.exe
Always prefix commands with: `export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"`
Always set: `PYTHONIOENCODING=utf-8`
Always set: `NO_COLOR=1` (prevents Unicode crash on Windows cp1252)

---

## MODE 1: QUERY (ask a notebook)

If $ARGUMENTS starts with "query" or contains a question:

1. Identify the target notebook:
   - Check aliases: `nlm alias list`
   - If no alias, list notebooks: `nlm notebook list --quiet`
   - Ask user which notebook to query if ambiguous

2. Run the query:
   ```bash
   nlm notebook query <notebook-id-or-alias> "<question>"
   ```

3. Present the response, then ask:
   - Save to vault? (which folder: project, or 3_Resources)
   - Extract Galaxy candidates? (run THỊNH H step)
   - Follow-up question? (use `--conversation-id` from response)

---

## MODE 2: ADD (add sources to a notebook)

If $ARGUMENTS starts with "add":

1. Identify source type and target notebook

2. **Source dedup check (v2.0):**
   ```bash
   nlm source list <notebook> 2>&1
   ```
   - URL match (substring of new URL found in existing sources) → skip, log "⚠ Already in notebook: <title>"
   - Title match (first 50 chars match) → warn "⚠ Similar source exists: <existing>. Add anyway? (y/n)"
   - No match → proceed

3. Add the source:
   - URL: `nlm source add <notebook> --url "<url>"`
   - Text: `nlm source add <notebook> --text "<content>" --title "<title>"`
   - YouTube: `nlm source add <notebook> --url "https://youtube.com/watch?v=..."`

4. Verify: `nlm source list <notebook>`

---

## MODE 3: GENERATE (create deliverables)

If $ARGUMENTS starts with "generate" or specifies a deliverable type:

Supported types:
- `report` — Briefing Doc, Study Guide, Blog Post, or custom prompt
- `audio` — Podcast (deep_dive, brief, critique, debate, quiz)
- `quiz` — Questions with difficulty 1-5
- `flashcards` — Easy/medium/hard
- `mindmap` — Visual concept map (extractable as JSON)
- `slides` — Presenter or detailed format (downloadable as PPTX)
- `infographic` — Landscape/portrait/square
- `data-table` — Tabular data (exportable as CSV)

1. Ask user: which notebook + which deliverable type
2. Run generation:
   ```bash
   nlm <type> create <notebook> --confirm
   ```
3. Poll for completion:
   ```bash
   nlm studio status <notebook>
   ```
4. When complete, present output and ask:
   - Save to vault? (propose path based on content)
   - Extract insights for Galaxy?

### Vault Routing for Artifacts (v2.1)

| Artifact | Save Location | Format | Use Case |
|----------|--------------|--------|----------|
| `audio` | `2_Areas/CEO-Self/Learning-Architecture/` | MP3/MP4 link | THỊNH learning — commute listening |
| `quiz` | Project folder or `3_Resources/` | Markdown | Self-test after research |
| `flashcards` | Project folder | Markdown | Spaced repetition |
| `mindmap` | Project folder | JSON → can feed into `/cld` | Visual concept mapping |
| `slides` | Project folder | PPTX | Viettel/HD128 presentations |
| `report` | `3_Resources/Deep-Content-Analyzer-Outputs/` | Markdown | Research output |
| `data-table` | Project folder | CSV | Feed into VDI 2225 / analysis |

### Audio Overview for THỊNH Learning (v2.1)

Generate Audio Overview in different modes for CEO learning:

```bash
# Standard deep-dive podcast
nlm audio create <notebook> --format deep_dive --confirm

# Brief overview (shorter)
nlm audio create <notebook> --format brief --confirm

# Critique mode — critical analysis
nlm audio create <notebook> --format critique --confirm

# Debate mode — hosts argue opposing viewpoints
nlm audio create <notebook> --format debate --confirm

# Focused on specific topic
nlm audio create <notebook> --format deep_dive --focus "sensor failure modes" --confirm

# Vietnamese language
nlm audio create <notebook> --format deep_dive --language vi --confirm
```

After generation:
1. Link/embed in Obsidian note: `![[audio-overview-<notebook>-<date>.mp3]]`
2. Add to CEO learning log in `_meta/learnings.md`
3. Listen → capture new insights → route back through THỊNH (Thu → Hóa)

---

## MODE 4: LIST (show notebooks and sources)

If $ARGUMENTS = "list":

```bash
nlm notebook list
```

For a specific notebook's sources:
```bash
nlm source list <notebook>
```

---

## MODE 5: CROSS-QUERY (v2.0 — query across multiple notebooks)

If $ARGUMENTS starts with "cross-query":

**Syntax:**
```
/nlm cross-query <nb1> <nb2> [nb3] "question"
/nlm cross-query <nb1> <nb2> --compare "topic"
```

**Max notebooks:** 3 per cross-query (beyond 3 = slow + noisy).

### Sequential mode (default — no --compare flag)

```
1. FOR each notebook in argument list:
     result[notebook] = nlm notebook query <notebook> "<question>"

2. MERGE results (Claude — cross-notebook reasoning):
   - Deduplicate identical findings
   - Tag each finding with source notebook alias
   - Group into:
     a) "Agreed" — found in 2+ notebooks (high confidence)
     b) "Unique to <notebook>" — found in 1 notebook only

3. OUTPUT format:
   ## Cross-Query: "<question>"
   Notebooks: <nb1>, <nb2> [, nb3]

   ### Agreed Findings (high compound value)
   1. Finding — sources: <nb1>, <nb2>

   ### Unique to `<nb1>`
   1. Finding

   ### Unique to `<nb2>`
   1. Finding

   ### Galaxy Candidates (cross-product insights)
   - "<insight>" — ★★★ compound (found across products)

4. ASK CEO:
   - Save to vault?
   - Promote any Galaxy candidates? (Core)
   - Follow-up cross-query?
```

### Compare mode (--compare flag)

```
1. Query each notebook with structured prompt:
   nlm notebook query <nb> "<topic>:
     (1) key principles, (2) techniques used,
     (3) constraints encountered, (4) failure modes"

   IF NLM returns no relevant findings for a notebook on the queried topic:
   → Report "No coverage in `<notebook>` for this topic"
   → Skip comparison for that notebook, suggest more targeted question

2. CLAUDE COMPARE (cross-notebook reasoning — NLM cannot do this):
   Build comparison table:

   | Dimension | <nb1> | <nb2> |
   |-----------|-------|-------|
   | Key principle | ... | ... |
   | Technique | ... | ... |
   | Constraint | ... | ... |
   | Failure mode | ... | ... |

   Then analyze:
   a) Contradictions: A says X, B says Y — which is context-dependent?
   b) Synergies: Shared patterns across different domains
   c) Transfer opportunities: Technique from A applicable to B's problem?
   d) Galaxy candidates: Cross-product insights with compound value

3. OUTPUT format:
   ## Compare: <nb1> vs <nb2> on "<topic>"

   ### Comparison Table
   | Dimension | <nb1> | <nb2> |
   ...

   ### Contradictions
   - <nb1>: X — <nb2>: Y — Reason: context-dependent / one is wrong

   ### Synergies
   - Both use: ...

   ### Transfer Opportunities
   - <nb1> technique → applicable to <nb2> problem?

   ### Galaxy Candidates (cross-product — high compound)
   - "<insight>" — proposed title, cluster, links

4. ASK CEO: same as sequential
```

**COD:** Query execution = O, Merge/Compare analysis = O, Galaxy promotion = **C**

**NLM auth:** Apply detect-pause wrapper to all nlm commands (same as /research v3.0): auth error → prompt CEO → retry → max 2 → fallback.

---

## MODE 6: HEALTH (v2.0 — notebook health dashboard)

If $ARGUMENTS = "health":

**Auth handling:** HEALTH mode itself serves as an auth check. If `nlm notebook list` fails → report "Auth: ✗ Expired — run `nlm login`" and stop (diagnostic, not a pipeline — no retry loop).

**Implementation:**
```
1. Run: nlm notebook list --quiet
   → Parse notebook names and IDs
   → If auth error → report "Auth: ✗ Expired — run `nlm login`" and STOP

2. FOR each notebook:
   Run: nlm source list <notebook> --quiet
   → Count sources

3. Check last query date:
   → Grep vault files: find latest RESEARCH_* or NLM_* file referencing each notebook alias
   → Check in: 3_Resources/Deep-Content-Analyzer-Outputs/ and 1_Projects/
   → Extract date from filename or frontmatter

4. OUTPUT:
   ## NLM Notebook Health Dashboard

   | Alias | Sources | Last Used | Age | Status |
   |-------|---------|-----------|-----|--------|
   | kpipe | — | — | — | — |
   | ast | — | — | — | — |
   | rcs | — | — | — | — |
   | lomah | — | — | — | — |
   | 127sim | — | — | — | — |
   | ach | — | — | — | — |
   | mcp-agent | — | — | — | — |

   Total: {{N}} notebooks, {{N}} sources
   Stale (>30d no use): {{N}}
   Near capacity (>45 sources): {{N}}
   Auth: ✓ Valid

   ### Recommendations
   - {{notebook}} not used in 30+ days — archive or query?
   - {{notebook}} has >45 sources — consider splitting
   - {{notebook}} has only {{N}} sources — add more?
```

**Stale threshold:** 30 days no query → flag as stale.

---

## VAULT INTEGRATION

When saving NLM output to the vault:
- Research outputs → `3_Resources/Deep-Content-Analyzer-Outputs/`
- Project-specific analysis → `1_Projects/<project>/`
- Galaxy candidates → flag for CEO review (Core decision per COD)

File naming: `NLM_<notebook-alias>_<type>_<date>.md`

Add frontmatter:
```yaml
---
created: {{today}}
source: NotebookLM
notebook: {{notebook-name}}
type: nlm-output
status: active
tags: [#type/nlm-output, #status/active]
---
```

---

## MODE 7: CUSTOM-INSTRUCTIONS (v2.1 — set notebook persona)

If $ARGUMENTS starts with "persona" or "instructions":

Configure up to 10,000 characters of custom instructions for a notebook.
This forces NLM to behave as a domain-specific expert.

**Use cases:**
- Defense engineering: "You are a defense systems engineer. Always cite MIL-STD numbers. Flag any claim not backed by uploaded sources."
- Pahl-Beitz: "You are a Pahl-Beitz systematic design expert reviewing Phase 2 concepts. Apply VDI 2225 criteria."
- Competitive analysis: "You are a competitive intelligence analyst. Compare features quantitatively. Flag unverified claims."

**Implementation:**
Set via NLM web UI: Open notebook → Settings → Custom Instructions → paste text.
(CLI does not support custom instructions yet — manual step, one-time per notebook.)

---

## MODE 8: DEEP-RESEARCH (v2.1 — NLM auto-research)

If $ARGUMENTS starts with "deep-research":

NLM Deep Research mode auto-browses hundreds of websites and produces a comprehensive cited report, imported as a new source.

```bash
nlm research start <notebook> "<topic>" 2>&1
# Wait for completion
nlm research status <notebook> 2>&1
# Import discovered sources
nlm research import <notebook> 2>&1
```

**When to use:** Before /research pipeline — let NLM find sources first (free), then CEO curates for /research analysis.

---

## ALIASES

Active aliases (21 — run `nlm alias list` for current):
- `kpipe` → Siêu quy trình nghiên cứu
- `ast` → AST-MSL-001 Design Questions
- `rcs` → Trihedral Corner Reflector RCS
- `lomah` → Piezo LOMAH Signal Conditioning
- `127sim` → 12.7mm Simulator Recoil Fidelity
- `127sim-comp` → 12.7mm Competitor Analysis
- `ach` → ACH Defense Training Cases
- `mcp-agent` → MCP Agent Development
- `hdpe-hull` → HDPE Torpedo Hull Research
- `hdpe-mooring` → HDPE Mooring Research
- `stability` → Stability Analysis
- `ssusv` → Semi-sub USV Research
- `pb-textbook` → Pahl-Beitz Textbook
- `pb-mastery` → Pahl-Beitz Mastery
- `pb-mechai` → Pahl-Beitz Mechanical AI
- `pb-defense-ai` → Pahl-Beitz Defense AI
- `triz` → TRIZ Innovation Methods
- `recoil-re` → Recoil Research
- `nemotron-vn` → Nemotron Vietnamese
- `trolydoanhnghiep` → Trợ Lý Doanh Nghiệp
- `nlm-agent` → NLM + Claude Agent Pipeline Research

To create new: `nlm alias set <name> <uuid>`
To list: `nlm alias list`

---

## RULES

- NEVER use `nlm chat start` — it opens an interactive REPL. Use `nlm notebook query` instead.
- Always use `--confirm` flag for generation/delete commands
- Ask user before ANY delete operation
- Session lifetime is ~20 min — if auth fails, prompt user to run `nlm login`
- NLM processing is FREE (Gemini tokens) — offload heavy analysis here
- COD: Query/generate = Offload, Galaxy extraction from results = Core
- **Cross-query max 3 notebooks** — beyond 3 is slow and noisy
- **Source dedup** — always check before add, log skipped duplicates
- **Source limit** — warn at 45+ sources per notebook (NLM limit ~50)
- **Empty results** — report "No coverage" rather than forcing comparison on irrelevant notebooks
- Link to Galaxy: Analyst Trap (don't just generate, extract insights), Vault = Graveyard (use outputs)
