---
name: book-ceo-insight
description: "Block P9 của codebase-to-book pipeline — query NotebookLM (book vừa ingest ở P8) với 5 insight lenses đặc thù Workshop X: HELIX applicability, FORGE transfers, Galaxy candidates, ACH opportunities, IP exposure map. Sinh Phase9-CEO-Insights.md structured với action items + COD classification + suggested follow-up skills. Optional NLM studio artifacts (briefing doc, audio, mind map). CEO Core — chọn insights actionable. Triggers on: 'ceo insight', 'book insight', 'rút insight', 'analyze book', 'HELIX forge galaxy insight', 'P9 book'."
---

# Block P9: CEO Insight Extraction — NLM-Driven 5-Lens Query

> **Pipeline:** codebase-to-book → Block P9 (final block)
> **Input:** `Phase8-Notebook-Manifest.md` (notebook_id từ P8)
> **Output:** `Phase9-CEO-Insights.md` với 5 sections + action items
> **Reference:** `../codebase-to-book/references/phase-prompts.md` § P9 NLM Query Templates

## Operational Envelope

| DO (within envelope) | DON'T (outside envelope) |
|---|---|
| Query NLM với 5 lens templates (HELIX/FORGE/Galaxy/ACH/IP) | Read book.md directly — NLM is the retrieval engine |
| Grounding queries trong Workshop X context (products, skills, domains) | Use generic "key insights" queries — shallow output |
| Extract action items tied to existing KN-Stack skills | Propose creating new skills without CEO discussion |
| Rate action priority (HIGH/MED/LOW) và COD (Core/Offload/Default) | Auto-trigger follow-up skills — CEO decides |
| Optional: create NLM studio artifacts (audio, briefing, mind map) | Make publishing decisions — P7 IP rating governs |

**Multi-Agent Mode:** NO — sequential lens queries to NLM.
**CEO Checkpoint:** Final — CEO selects actionable items, triggers follow-up skills.

## Standalone Usage
```
/book-ceo-insight <codebase-slug>
/book-ceo-insight <codebase-slug> --insight-lens helix,galaxy
```

## Input Requirements

- `_pipeline_state.md` Block Ledger — must show P8 complete + CEO test query approval
- `Phase8-Notebook-Manifest.md` — notebook_id + URL
- `Phase2-Positioning.md` — thesis + glossary (for query grounding)
- `--insight-lens` flag (optional) — subset của 5 lenses. Default: all 5.

## Workflow

### Step P9.1: Load Notebook Context

```python
# Pseudocode
manifest = parse_yaml_frontmatter(read(f"{output_dir}/Phase8-Notebook-Manifest.md"))
notebook_id = manifest["notebook_id"]
notebook_url = manifest["notebook_url"]
book_slug = manifest["book_slug"]

# Verify auth still valid
mcp__notebooklm-mcp__refresh_auth()

# Parse --insight-lens flag
active_lenses = args.insight_lens.split(",") if args.insight_lens else ["helix", "forge", "galaxy", "ach", "ip"]
```

### Step P9.2: Run 5 Lens Queries (Sequential)

Sequential vì mỗi query build on previous context (NLM conversation-style). Query template chi tiết trong `../codebase-to-book/references/phase-prompts.md`.

#### Lens 1: HELIX Applicability

```python
# Pseudocode
if "helix" in active_lenses:
    query = HELIX_LENS_PROMPT  # see phase-prompts.md
    # Long query may need async — use _start + _status pattern
    
    response = mcp__notebooklm-mcp__notebook_query(
        notebook_id=notebook_id,
        query=query,
    )
    
    helix_insights = parse_response_to_structured(response)
    # Structure: list of insights, each with:
    #   - pattern_name
    #   - chapter_citation
    #   - helix_phase (0/1/2/3/4)
    #   - mapping_description
    #   - skill_to_upgrade (optional — e.g., /helix-p1-requirements)
```

#### Lens 2: FORGE Transfers

```python
if "forge" in active_lenses:
    query = FORGE_LENS_PROMPT
    response = mcp__notebooklm-mcp__notebook_query(notebook_id=notebook_id, query=query)
    forge_insights = parse_response_to_structured(response)
    # Structure: list with:
    #   - framework_name, chapter_citation
    #   - how_to_apply (1-2 sentences)
    #   - forge_skill_to_upgrade (e.g., /forge-portfolio, /forge-shift)
```

#### Lens 3: Galaxy Candidates

```python
if "galaxy" in active_lenses:
    query = GALAXY_LENS_PROMPT
    response = mcp__notebooklm-mcp__notebook_query(notebook_id=notebook_id, query=query)
    galaxy_candidates = parse_response_to_structured(response)
    # Structure: list of 5-10 proposed Galaxy notes with:
    #   - proposed_title
    #   - atomic_level_check
    #   - suggested_wikilinks (may be [needs connection research])
    #   - proposed_tag
    #   - one_line_summary
```

#### Lens 4: ACH Transfer Opportunities

```python
if "ach" in active_lenses:
    query = ACH_LENS_PROMPT
    response = mcp__notebooklm-mcp__notebook_query(notebook_id=notebook_id, query=query)
    ach_opportunities = parse_response_to_structured(response)
    # Structure: list with:
    #   - pattern_name, chapter_citation
    #   - ach_mapping (hardware limit being compensated)
    #   - products_applicable (BB-01, V-SMASH, MTB-20, TDR, UUV, or multiple)
    #   - readiness (deploy now / needs research / speculative)
```

#### Lens 5: IP Exposure Map

```python
if "ip" in active_lenses:
    query = IP_LENS_PROMPT
    response = mcp__notebooklm-mcp__notebook_query(notebook_id=notebook_id, query=query)
    ip_ratings = parse_response_to_structured(response)
    # Structure: per-chapter:
    #   - chapter_num, title
    #   - rating (SAFE / REVIEW / SENSITIVE)
    #   - rationale
    #   - redaction_suggestion (if non-SAFE)
    
    # NOTE: P7 already did IP rating from write-time. P9 re-rates from NLM read-time perspective.
    # Cross-validate: flag discrepancies between P7 ratings and P9 NLM ratings.
```

### Step P9.3: Synthesize Action Items

Scan insights across all 5 lenses, extract action items:

```python
# Pseudocode — action extraction
actions = []

# From HELIX insights
for insight in helix_insights:
    if insight.skill_to_upgrade:
        actions.append({
            "action": f"Upgrade {insight.skill_to_upgrade} với pattern '{insight.pattern_name}' từ Ch{insight.chapter_citation}",
            "cod": "Offload",
            "suggested_skill": "/research-to-skill",
            "lens": "helix",
            "priority": estimate_priority(insight),
        })

# From FORGE insights
for insight in forge_insights:
    actions.append({
        "action": f"Transfer '{insight.framework_name}' → {insight.forge_skill_to_upgrade}",
        "cod": "Offload",
        "suggested_skill": "/research-to-skill",
        "lens": "forge",
        "priority": estimate_priority(insight),
    })

# From Galaxy candidates
for candidate in galaxy_candidates:
    actions.append({
        "action": f"Create Galaxy note: '{candidate.proposed_title}'",
        "cod": "Core",  # Galaxy notes are CEO Core per CLAUDE.md
        "suggested_skill": "/galaxy-note",
        "lens": "galaxy",
        "priority": "MED",  # Galaxy always MED unless CEO elevates
    })

# From ACH opportunities
for opp in ach_opportunities:
    if opp.readiness == "deploy now":
        actions.append({
            "action": f"Apply ACH pattern '{opp.pattern_name}' to {opp.products_applicable}",
            "cod": "Core",  # product decisions
            "suggested_skill": "/forge-shift or /helix-design-journal",
            "lens": "ach",
            "priority": "HIGH",
        })

# From IP ratings (if P9 NLM rating conflicts with P7)
ip_conflicts = find_ip_rating_conflicts(p7_audit_log, ip_ratings)
for conflict in ip_conflicts:
    actions.append({
        "action": f"Reconcile IP rating for Ch{conflict.chapter}: P7 said {conflict.p7}, P9 NLM said {conflict.p9}",
        "cod": "Core",
        "suggested_skill": None,  # CEO resolves directly
        "lens": "ip",
        "priority": "HIGH",
    })

# Sort by priority
actions = sorted(actions, key=lambda x: priority_rank(x.priority))
```

### Step P9.4: Optional NLM Studio Artifacts

Present to CEO, offer 3 optional artifacts:

```
═══ P9 Studio Artifacts (Optional) ═══

Nếu muốn NLM sinh thêm artifacts dùng cho consumption khác nhau:

(1) 📄 Briefing Doc — Executive summary dạng Situation/Complication/Resolution
    Use case: Share với stakeholder ngoài team, pitch insight
    Cost: ~30s NLM compute

(2) 🎧 Audio Deep-Dive — Podcast-style tiếng Việt, 2 speakers discuss insights
    Use case: Listen trong commute, passive absorption
    Cost: ~2-5 min NLM compute

(3) 🧠 Mind Map — Visual hierarchy của insights + connections
    Use case: Wall poster, workshop whiteboard reference
    Cost: ~30s NLM compute

CEO: Chọn 0 hoặc nhiều (1,2,3 hoặc all hoặc none)
```

Nếu CEO chọn:

```python
# Pseudocode
if "briefing" in ceo_artifacts:
    mcp__notebooklm-mcp__studio_create(
        notebook_id=notebook_id,
        artifact_type="briefing_doc",
    )
    # Poll studio_status until complete

if "audio" in ceo_artifacts:
    mcp__notebooklm-mcp__studio_create(
        notebook_id=notebook_id,
        artifact_type="audio",
        # Optional: language=vi
    )

if "mind_map" in ceo_artifacts:
    mcp__notebooklm-mcp__studio_create(
        notebook_id=notebook_id,
        artifact_type="mind_map",
    )

# Download artifacts if available
for artifact in created_artifacts:
    mcp__notebooklm-mcp__download_artifact(
        notebook_id=notebook_id,
        artifact_type=artifact.type,
        # Save to output_dir
    )
```

### Step P9.5: Write Phase9-CEO-Insights.md

```markdown
---
created: {{date}}
book: {{slug}}
notebook_id: {{nlm-uuid}}
notebook_url: {{url}}
lenses: [{{list of active}}]
total_insights: {{N}}
action_items: {{M}}
---

# CEO Insights — {{book_title}}

> Source: NotebookLM notebook {{url}}
> Lenses applied: {{list}}
> Generated: {{date}}

## Executive Summary

<3-5 bullet synthesis — top insights CEO should act on, extracted across all 5 lenses>

## HELIX Applicability

> Patterns từ sách có thể áp dụng vào Pahl-Beitz HELIX pipeline (Phase 0-4).

### Phase 0: Product Planning
- **[Ch{{N}}] {{Pattern}}** — {{how to apply}}
  - Skill to upgrade: `{{skill}}`
- ...

### Phase 1: Task Clarification
- **[Ch{{N}}] {{Pattern}}** — ...

### Phase 2: Conceptual Design
...

### Phase 3: Embodiment Design
...

### Phase 4: Detail Design
...

## FORGE Transfers

> Product strategy frameworks → upgrade FORGE skills.

### Portfolio Management
- **[Ch{{N}}] {{Framework}}** — {{how to apply}}
  - FORGE skill: `/forge-portfolio` (upgrade)

### ACH Strategy
...

### Customer Trust
...

### Market Intelligence
...

## Galaxy Candidates

> 5-10 atomic concepts xứng đáng thành permanent notes.

### 1. {{Proposed Title}}
- **Summary:** {{1-line}}
- **Wikilinks:** [[{{existing note}}]], [[{{existing note}}]]
- **Tag:** {{#type/permanent-note + domain tag}}
- **Source:** Ch{{N}} của sách

### 2. {{Proposed Title}}
...

## ACH Transfer Opportunities

> Patterns relevant đến AI-Compensates-Hardware thesis của Workshop X.

### Deploy Now
- **[Ch{{N}}] {{Pattern}}** — compensate {{hardware limit}} via {{AI approach}}
  - Products: {{BB-01, V-SMASH, ...}}
  - Next action: {{specific step}}

### Needs Research
- ...

### Speculative
- ...

## IP Exposure Map

> Per-chapter rating cho external sharing decisions.

### SAFE — Publishable
| Chapter | Title | Rationale |
|---------|-------|-----------|
| Ch 1 | {{title}} | Generic patterns, no WX-specific IP |
| Ch 3 | ... | ... |

### REVIEW — CEO Gate Required
| Chapter | Title | Rationale | Redaction Suggestion |
|---------|-------|-----------|---------------------|
| Ch 5 | {{title}} | Specific architecture visible | Mask section "{{X}}" |

### SENSITIVE — Internal Only
| Chapter | Title | Rationale |
|---------|-------|-----------|
| Ch 7 | {{title}} | Sensor calibration values, defense-specific thresholds |

### P7 vs P9 Rating Conflicts
{{If any: list chapters where P7 audit rating differs from P9 NLM rating, flag for CEO resolution}}

## Recommended Actions

Sorted by priority:

| # | Action | Lens | COD | Priority | Suggested Skill |
|---|--------|------|-----|----------|----------------|
| 1 | {{action}} | {{lens}} | Core/Offload | HIGH | `/research-to-skill <skill>` |
| 2 | ... | | | | |

## Studio Artifacts
{{If CEO created any:}}
- Briefing Doc: {{path or "Generated in NLM UI — {{url}}"}}
- Audio: {{path}}
- Mind Map: {{path}}

## Next Steps

CEO, các skills follow-up đề xuất:

### Priority HIGH (do ngay tuần này)
{{List of HIGH priority actions with skill invocations}}

### Priority MED (2 tuần tới)
{{...}}

### Priority LOW (backlog)
{{...}}

Để chạy một action:
```
/research-to-skill <skill> UPGRADE with "{{pattern name}}"
/galaxy-note "{{proposed title}}"
/helix-design-journal "Applied pattern {{X}} từ book {{slug}}"
```
```

### Step P9.6: Final Pipeline State Update

```markdown
### P9 — CEO Insights (<date>)
**Key findings:**
- {{N}} insights extracted across {{M}} active lenses
- {{K}} action items generated
- {{P}} HIGH priority actions require immediate follow-up
- Studio artifacts: {{list or "none"}}

**Decisions for downstream:**
- CEO selects actionable items — follow-up skills triggered manually
- Pipeline COMPLETE — codebase-to-book finished

**Open questions:**
- IP rating conflicts (P7 vs P9): {{list if any — CEO resolves}}

**CEO checkpoint result:** [pending — final]
```

Mark Block Progress table: all P1-P9 COMPLETE.

## Output

Save to `{{output_dir}}/`:
- `Phase9-CEO-Insights.md`
- Optional: `studio-artifacts/` folder với briefing doc / audio / mind map

Update: `{{output_dir}}/_pipeline_state.md` — mark pipeline COMPLETE.

## CEO Checkpoint (FINAL — Pipeline Completion)

```
═══ BLOCK P9 CEO INSIGHT COMPLETE ═══
═══  CODEBASE-TO-BOOK PIPELINE COMPLETE ═══

Notebook: {{url}}

Insights Generated:
  📐 HELIX Applicability: {{N}} patterns
  🎯 FORGE Transfers: {{N}} frameworks
  🌌 Galaxy Candidates: {{N}} proposed notes
  🤖 ACH Opportunities: {{N}} transfer ideas ({{deploy-now}} ready)
  🔒 IP Exposure: {{safe}} SAFE / {{review}} REVIEW / {{sensitive}} SENSITIVE
  
Action Items: {{total}} total
  🔴 HIGH priority: {{N}}
  🟡 MED priority: {{N}}
  🟢 LOW priority: {{N}}

Studio artifacts: {{list or "none chosen"}}

Final Deliverables:
  - {{output_dir}}/book.md (P7)
  - {{output_dir}}/Phase8-Notebook-Manifest.md (P8)
  - {{output_dir}}/Phase9-CEO-Insights.md (P9)
  - NotebookLM notebook: {{url}}

CEO — Final actions:
(1) ✅ Complete — insights approved, pipeline done
(2) 📋 Select HIGH priority actions để trigger follow-up skills NGAY
(3) 🔄 Re-run specific lens với different angle: [specify]
(4) ➕ Additional studio artifact: [briefing/audio/mind_map]
(5) 📅 /schedule agent cleanup book outputs in 3 months
═══════════════════════════════════════════════════
```

## COD Classification

- Auth pre-check: Offload (O2)
- Lens query execution: Offload (O2) — NLM does heavy lifting
- Response parsing: Offload (O2)
- Action item extraction: Offload (O2)
- Priority rating: Offload (O2)
- **Actionable selection: Core (C)** — CEO decides what to pursue
- Studio artifact creation: Offload (O2) — CEO chooses which artifacts

## Rules

- **NLM is the retrieval engine, not Claude** — queries grounded in WX context make or break insight quality
- **5 lenses are default — override với --insight-lens** — don't skip lenses without CEO intent
- **Lens prompts are specific to WX** — generic prompts → shallow output. See phase-prompts.md for full templates.
- **Citations mandatory** — every insight cites chapter. NLM naturally provides this; enforce by including "với citation chapter" in query.
- **P7 vs P9 IP rating cross-check** — different perspectives may catch different issues. Flag conflicts.
- **Galaxy candidates are Core (C)** — per CLAUDE.md "AI cannot write permanent notes without being asked"
- **Action items tied to existing skills when possible** — reuse, don't proliferate
- **Studio artifacts optional — never default** — artifacts cost NLM compute; CEO picks what's worth generating
- **Pipeline ends at P9** — no P10. Follow-up skills triggered by CEO from action items.
- **If lens query returns <3 insights** — NLM retrieval weak for that lens. Re-query với narrower context hoặc flag as limitation.
