---
name: forge-portfolio
description: FORGE Product Portfolio dashboard with ACH pipeline, model library status, and FORGE SCORE per product. Two modes — default dashboard and --learn (quarterly cross-product pattern extraction from completed Phase 2s). Triggers on "portfolio dashboard", "FORGE score", "all products status", "product portfolio", "portfolio review", "san pham tong quan", "forge dashboard", "portfolio learn", "cross-product patterns", "what have we learned across products". CEO's primary FORGE-level view.
---

# Forge Portfolio — Product Portfolio Dashboard

Generate the FORGE Portfolio Dashboard showing all products with FORGE SCORE, ACH pipeline status, model library health, and flywheel metrics. This is the CEO's primary strategic product view.

## When to Use

- Weekly portfolio quick-check (10 min in CEO weekly protocol)
- Monthly full portfolio review (30 min)
- Before resource allocation decisions
- When asked "how is the portfolio doing?"

## Workflow

### Step 1: Gather Data

Read all project data:
- Glob `1_Projects/*/Status.md` — phase, tier, blocking constraints, dP/dt
- Glob `1_Projects/*/_Project_Brief.md` — requirements, cost targets
- `4_Archives/Projects/` — count archived projects
- Area dashboards for FORGE metrics if populated

### Step 2: Generate FORGE SCORE Per Product

For each active product, score 5 FORGE dimensions (1-5 each):

| Dimension | What It Measures | Score Guide |
|-----------|-----------------|-------------|
| **F** — Fallback | ACH fallback architecture designed? | 0=none, 1=concept, 3=designed, 5=tested |
| **O** — Validate | Performance Envelope documented? | 0=none, 1=plan, 3=lab tested, 5=field validated |
| **R** — Reuse | Model in library, transfers done? | 0=no model, 1=experimental, 3=cataloged, 5=transferred |
| **G** — Ground truth | Active data pipeline from field? | 0=none, 1=planned, 3=collecting, 5=retraining |
| **E** — Edge-cost | Defense-realistic costing done? | 0=none, 1=consumer pricing, 3=defense costed, 5=LCC done |

**Bands:** 0-7 RAW ORE / 8-13 HEATING / 14-19 FORGING / 20-25 TEMPERED

### Step 3: Generate Dashboard

```
# FORGE PORTFOLIO DASHBOARD — Workshop X
Date: {{today}}

## PORTFOLIO MATRIX

| # | Product | Tier | Phase | F | O | R | G | E | Score | Band | I-Lvl | Moat? |
|---|---------|------|-------|---|---|---|---|---|-------|------|-------|-------|
| 1 | {{name}} | T1/T2/T3 | 0-4 | /5 | /5 | /5 | /5 | /5 | /25 | | {{avg}} | {{Y/N}} |

Portfolio Average: __/25 = {{band}}

## INNOVATION LEVEL TRACKER (Altshuller — from TRIZ dry runs)

| Product | Phase | Avg I-Level | Peak Level | Key TRIZ Principle | Moat Assessment |
|---------|-------|------------|------------|-------------------|-----------------|
| {{name}} | {{phase}} | {{1.0-5.0}} | L{{1-5}} | #{{N}} {{name}} | {{commodity/differentiated/unique}} |

**I-Level Guide:**
- Avg < 1.5 → WARNING: commodity concept, no competitive differentiation
- Avg 1.5-2.0 → ADEQUATE: some contradictions resolved
- Avg 2.0-3.0 → STRONG: multiple contradictions resolved, clear moat
- Avg > 3.0 → EXCEPTIONAL: new system principle

**Rule:** If product at Phase 2+ has I-Level = 0 (not assessed) → flag "TRIZ not applied — run /helix-concept-generate Step 0.5"

## ACH PIPELINE

| Stage | Count | Products |
|-------|-------|----------|
| 0 — Scouting | | |
| 1 — SHIFT assessed (GO) | | |
| 1 — SHIFT assessed (NO-GO) | | |
| 2 — Validating | | |
| 3 — Library (model cataloged) | | |
| 4 — Evolving (moat building) | | |

## MODEL LIBRARY STATUS

Total models: __ (__ production, __ experimental)
Transfers this quarter: __ (target: 1)
Library utilization: __% (products using library models / total)

## FLYWHEEL HEALTH

Data collection: __ GB/month
Model updates this quarter: __
Flywheel speed: (insights acted on / generated) x (1 / days to action)

## TIER HEALTH CHECK

### Tier 1 (Prototype) — Must have >=1 with physical gate <=30d
- Active Tier 1 projects: __
- Physical gate within 30 days: YES/NO
- dP/dt this month: __

### Tier 2 (Product Dev) — Pahl-Beitz tracked
- Projects in Phase 3+: __
- Projects blocked: __ (reasons)

### Tier 3 (Strategic) — Time-bounded
- Projects with clear "done" criteria: __/__

## DEPENDENCY MAP

{{ASCII graph showing product dependencies}}

## RESOURCE ALLOCATION (Solo CEO, ~25h/week)

| Domain | Target % | Actual | Status |
|--------|----------|--------|--------|
| Tier 1 Physical | >=40% | | |
| Tier 2 Design | <=30% | | |
| Tier 3 Strategic | <=15% | | |
| Operations | <=15% | | |

## CEO TIME BUDGET (from Pattern Library E1 + Phần 4)

| Category | Target h/wk | Actual | Delta | Notes |
|----------|:-----------:|:------:|:-----:|-------|
| AMBIGUOUS work (design decisions, HW debug, integration, strategy) | ≥20h | | | High-value: $500/h equivalent |
| ROUTINE work (AI-delegated: docs, boilerplate, formatting) | ≤2h | | | Low-value: $50/h equivalent — should be delegated |
| AI oversight (reviewing AI outputs) | ~3h | | | Keep quality high without over-reviewing |

VALUE MULTIPLIER:
  Current: routine __h × $50 + ambiguous __h × $500 = $__/week
  Optimal: 2h × $50 + 23h × $500 = $11,600/week

⚠ If ROUTINE > 3h → delegation patterns not being used — review Pattern Library
⚠ If AMBIGUOUS < 18h → time leaking to routine work

## RE INVESTMENT PORTFOLIO (from prompt-pattern analysis)

Bounded RE allocation — 11% of 26-person team. Prevents Analyst Trap.

| Cat | Activity | FTE | Budget/yr | Priority | Phase |
|-----|----------|-----|----------|----------|-------|
| A-Mandatory | Own product field intel (→ /reverse-engineering --mode field) | 0.5 | $0 | MAX | Now |
| A-Mandatory | VN Navy understanding (→ /bd-pulse) | 0.5 | $10K | MAX | Now |
| B-High | Signature tech (→ /reverse-engineering --mode technology) | 1.0 | $100K | HIGH | Phase 1 |
| B-High | TMS architecture learning (embedded) | 0.25 | $20K | HIGH | Phase 1 |
| B-High | Competitor monitoring (→ /forge-market-intel --competitor) | 0.25 | $30K | HIGH | Ongoing |
| C-Medium | ACH thesis validation (→ /forge-validate --thesis) | 0.25 | $20K | MED-HIGH | Ongoing |
| C-Medium | TRV partnership eval (→ /reverse-engineering --mode compare) | varies | $50K | HIGH but defer | Phase 1 success |
| D-Low | ASEAN market intel (→ /forge-market-intel --export) | 0.1 | $10K | LOW-MED | Monitor |
| E-Avoid | Complex platform RE, products WX can't build | 0 | $0 | AVOID | — |

**Total dedicated RE: ~2.85 FTE (11% of team) | ~$240K/yr | $720K over 3 years**

⚠️ ANALYST TRAP GUARD: If RE FTE > 3.0 or budget > $300K/yr → flag "Strategy work displacing production"
⚠️ Always ask: "What does this RE change about what we ship?"

## ALERTS

[RED] {{critical issues — fallback Level 0, deployment without evidence}}
[YELLOW] {{trending problems — 0 transfers in 90d, stale costing}}

## DECISIONS NEEDED

1. {{tier changes}}
2. {{archival candidates}}
3. {{sequencing conflicts}}
4. {{ACH decisions pending}}
5. {{RE investment rebalancing needed?}}
```

### Step 4: Present and Route

- Present dashboard to CEO
- Feed FORGE scores to bridge-dashboard if requested
- Flag anti-patterns from architecture doc:
  - forge-shift GO but no HELIX project-init → Strategy-Execution Gap
  - HELIX building but no forge-shift → Accidental ACH
  - forge-library has model but HELIX not using → R5 Dormant

---

## Portfolio Learner Mode (`--learn`)

> **Trigger:** "portfolio learn", "cross-product patterns", "what have we learned across products", "portfolio knowledge"
> **Frequency:** Quarterly (or after any product completes Phase 2/3)
> **Source:** Multi-agent research Insight #2 (SBCE-Agent Mapping) — cross-product pattern library = reusable design knowledge
> **COD:** Offload (AI extracts), Core (CEO validates which patterns to promote to Galaxy)

### L1: Scan Completed Phase 2+ Products

Glob for Phase 2 artifacts across all projects:
- `1_Projects/*/Phase2-Concept/BB_Morphological_Matrix.md` — WP choices
- `1_Projects/*/Phase2-Concept/BC_VDI_2225_Evaluation.md` — scoring, weak spots
- `1_Projects/*/Phase2-Concept/BD_CFMA.md` — failure modes
- `1_Projects/*/Phase2-Concept/BD_Coupling_Analysis.md` — coupling patterns
- `1_Projects/*/RE/RE_*_S5_Knowledge_Capture.md` — laws from RE

```
PORTFOLIO LEARNER SCAN — {{Date}}
Products scanned: {{list of products with Phase 2+ complete}}
Artifacts found: {{count}}
```

### L2: Extract 5 Pattern Categories

```
═══ CATEGORY 1: RECURRING WORKING PRINCIPLES ═══
WPs that appear in 2+ product morphological matrices:

| Working Principle | Products Using It | Sub-Function | Performance | Reuse Confidence |
|------------------|-------------------|-------------|-------------|-----------------|
| {{e.g., BLDC + planetary}} | VN-MGM, VN-AST, TARGET-DRONE | SF-xx (Convert E→M) | {{rating}} | H/M/L |

→ HIGH reuse confidence = add to BB search library for future products

═══ CATEGORY 2: COMMON WEAK SPOTS ═══
VDI 2225 criteria scored ≤1 across multiple products:

| Weak Spot Pattern | Products Affected | Root Cause | Resolved How? | Transferable Fix? |
|------------------|-------------------|-----------|---------------|------------------|
| {{e.g., salt spray resistance}} | VN-AST, BB-01, VN-USV | VN maritime environment | {{solution}} | Y/N |

→ Transferable fixes = pre-load in BC firming-up for new maritime products

═══ CATEGORY 3: CROSS-PRODUCT FAILURE MODES ═══
CFMA failure modes recurring across 2+ products:

| Failure Mode | Products | Severity Range | Common Cause | Portfolio Mitigation |
|-------------|----------|---------------|-------------|---------------------|
| {{e.g., connector corrosion}} | VN-AST, BB-01 | S=6-8 | Salt + vibration | {{standard solution}} |

→ Recurring FMs = pre-seed in BD CFMA for all new products (prevent rediscovery)

═══ CATEGORY 4: COUPLING ARCHETYPES ═══
Cross-domain coupling patterns that repeat:

| Coupling Pattern | Products | Domains | Typical Score | Design Strategy |
|-----------------|----------|---------|--------------|----------------|
| {{e.g., motor thermal × ESC derating}} | VN-MGM, TARGET-DRONE | Mech×Elec | 7-8/10 | {{architecture choice}} |

→ Known coupling patterns = pre-load in BD coupling analysis

═══ CATEGORY 5: SOLUTION-DETERMINING SF PATTERNS ═══
Which types of SFs tend to be solution-determining across products:

| SF Type | Products Where Solution-Determining | Why | Implication for New Products |
|---------|-------------------------------------|-----|---------------------------|
| {{e.g., AI feedback loop}} | VN-CUAV-SIM, VN-AICC | Software complexity cascade | Prioritize SW architecture early |
```

### L3: Generate Transfer Recommendations

```
TRANSFER MATRIX — What to pre-load in future projects

| Pattern | Source Product(s) | Target Use | Inject Into | Priority |
|---------|------------------|-----------|-------------|----------|
| {{WP}} | {{source}} | BB search library | helix-p2-search | H/M/L |
| {{weak spot fix}} | {{source}} | BC firming-up | helix-p2-firmup | H/M/L |
| {{FM}} | {{source}} | BD CFMA pre-seed | helix-p2-risk | H/M/L |
| {{coupling}} | {{source}} | BD coupling prior | helix-p2-risk D1 | H/M/L |
| {{Galaxy candidate}} | {{source}} | 5_Galaxy/ | /galaxy-note | H/M/L |

CEO DECISION: Which transfers to activate? (Core — judgment on relevance)
```

### L4: Save + Route

- Save to `2_Areas/FORGE — Product Strategy/Product-Portfolio/Portfolio_Learner_{{YYYY-Q}}.md`
- Galaxy candidates (patterns distilled to laws) -> flag for `/galaxy-note`
- Transfer recommendations -> CEO approves -> inject into skill reference files
- Update this dashboard's "MODEL LIBRARY STATUS" with pattern count

### Portfolio Learner Rules

1. **Only scan completed Phase 2+** — in-progress products have unstable patterns
2. **2+ products minimum** — single-product patterns are not portfolio patterns
3. **CEO validates transfers** — AI proposes, CEO approves which to pre-load
4. **Galaxy gate applies** — only promote to Galaxy if pattern passes 3-question gate
5. **Quarterly cadence** — not more frequent (patterns need time to stabilize)
6. **Track pattern age** — if a pattern was transferred but never used in 2 quarters, retire it

---

## HELIX Integration

```
forge-portfolio READS FROM HELIX:
  - Product phase → current Pahl-Beitz stage
  - Integration debt → open ICD items per product
  - Sync protocol → last/next sync dates

forge-portfolio WRITES TO HELIX:
  - Priority ordering → resource allocation guidance
  - HALT flags → quality gate override
  - New ACH opportunity → triggers task clarification review
```

## Rules

- Use data from Status.md and _Project_Brief.md — do not assume
- Flag any project missing Status.md
- Flag portfolios with 0 Tier 1 projects (violates CLAUDE.md)
- Always show dependency map — sequencing errors are expensive
- FORGE SCORE is AI-proposed, CEO-validated
- Do NOT save to file unless asked

## COD Classification

- Data compilation: Offload (O1) — AI gathers from vault
- FORGE scoring: Offload (O2) — AI proposes, CEO validates
- Portfolio prioritization: **Core (C)** — CEO decides resource allocation
- Tier change decisions: **Core (C)** — CEO judgment
