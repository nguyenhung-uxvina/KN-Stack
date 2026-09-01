---
name: helix-p2-risk
description: "Block D of Phase 2 pipeline — cross-domain coupling analysis (Mech×Elec×AI), assumption register with shadow assumptions, 3-scenario evaluation, CFMA (Conceptual Failure Mode Analysis), sensitivity analysis. Can run standalone. Triggers on: 'coupling analysis', 'assumption register', 'CFMA', 'concept risk', 'sensitivity', '3-scenario'."
---

# Block D: Risk & Integration — Coupling + Assumptions + CFMA + Sensitivity

> **P&B:** Workshop X extensions | **Pipeline:** helix-concept-generate → Block BD
> **Input:** `BC_VDI_2225_Evaluation.md`, `BB_Concept_Variants.md` | **Output:** `BD_*.md` files
> **Galaxy:** [[VDI 2225 — Sensitivity Analysis]], [[Physical-World Interface]]

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Cross-domain coupling analysis (Mech×Elec×AI) | Propose design changes (= BC/BB feedback) |
| Build assumption register + shadow assumptions | Dismiss assumptions without evidence |
| 3-scenario evaluation | Select preferred concept (= BE, CEO Core) |
| CFMA per concept variant | Skip CFMA for "obvious" winner |
| Sensitivity analysis on VDI 2225 ranking | Change VDI 2225 scores (= BC output) |

**Multi-Agent Mode:** YES — 3 domain agents for parallel CFMA + coupling detection (highest-value alongside BB)
- Mech agent: structural, thermal, vibration failure modes + manufacturing coupling
- Elec agent: EMC, power, sensor failure modes + signal integrity coupling
- AI-SW agent: algorithm, latency, data pipeline failure modes + compute coupling
- Merge: cross-domain coupling matrix (where domains conflict/depend)

**CEO Checkpoint:** Block boundary (output: BD_*.md files). CEO reviews CRITICAL coupling + unverified assumptions.

## Standalone Usage
```
/helix-p2-risk VN-XUONG-UUV
```

## Input Requirements
- `BC_VDI_2225_Evaluation.md` — scores, ranking, weak spots
- `BB_Concept_Variants.md` — concept definitions
- `BB_Morphological_Matrix.md` — WP details for coupling analysis
- ICD v1 — domain allocations

## Workflow

### Step D1: Cross-Domain Coupling Analysis (Multi-Perspective v2.0)

**Multi-Agent Selectivity check:** If RE Complexity = GREEN (all SFs have WX prior art) → skip domain debate, use single-agent scoring below. If AMBER/RED → run `/helix-domain-debate` for coupling scoring.

**For AMBER/RED complexity (run domain debate):**

Run `/helix-domain-debate` with question: "Score coupling between domains for each concept. What interactions does YOUR domain see that other domains might miss?"

```
COUPLING ANALYSIS — {{project_id}} (Multi-Perspective)
Date: {{today}}

═══ 3 DOMAIN LENS COUPLING SCORES ═══

MECHANICAL PERSPECTIVE — coupling felt by mechanical domain:
| Concept | Co×Dien (mech sees) | Co×AI (mech sees) | Key Concern |
|---------|--------------------|--------------------|-------------|

ELECTRICAL PERSPECTIVE — coupling felt by electrical domain:
| Concept | Co×Dien (elec sees) | Dien×AI (elec sees) | Key Concern |
|---------|--------------------|--------------------|-------------|

AI/SW PERSPECTIVE — coupling felt by SW domain:
| Concept | Co×AI (sw sees) | Dien×AI (sw sees) | Key Concern |
|---------|-----------------|-------------------|-------------|

═══ CONTRADICTION TABLE (MANDATORY) ═══
| # | Coupling Pair | Mech Score | Elec Score | AI/SW Score | Delta | Resolution |
|---|-------------|-----------|-----------|------------|-------|-----------|
(Contradictions with delta ≥ 3 points → flag for CEO)

═══ CONSOLIDATED COUPLING MATRIX ═══

Score: 0 (independent) to 10 (tightly coupled)
Method: average of 3 domain perspectives, weighted by domain closest to interface

| Concept | Co×Dien | Co×AI | Dien×AI | Co×Dien×AI | Total | Risk |
|---------|---------|-------|---------|------------|-------|------|

THRESHOLDS: <15=LOW, 15-25=MEDIUM, >25=HIGH

COUPLING INSIGHTS FROM DOMAIN DEBATE:
- Hidden coupling #1: {{what one domain saw that others missed}}
- Hidden coupling #2: {{cross-domain interaction not obvious from single perspective}}
```

**For GREEN complexity (single-agent, no debate):**

```
COUPLING ANALYSIS — {{project_id}}
Date: {{today}}

Score: 0 (independent) to 10 (tightly coupled)

| Concept | Co×Dien | Co×AI | Dien×AI | Co×Dien×AI | Total | Risk |
|---------|---------|-------|---------|------------|-------|------|

THRESHOLDS: <15=LOW, 15-25=MEDIUM, >25=HIGH (simplify)
```

For single-domain: State "Coupling: single-domain, no cross-coupling" explicitly.

### Step D2: Assumption Register

```
ASSUMPTION REGISTER — {{project_id}}

EXPLICIT ASSUMPTIONS:
| AS-ID | Assumption | Concept | Domain | Impact if Wrong | Verify How | By |

SHADOW ASSUMPTIONS (cross-domain):
| SA-ID | Domain Making | About Domain | Assumption | Verified? |

NOTE: Unverified SA at concept selection = hidden integration debt → D-xxx at Gate 2.
```

### Step D3: 3-Scenario Evaluation

```
3-SCENARIO — {{project_id}}

| Scenario | Concept A | Concept B | Concept C |
|----------|-----------|-----------|-----------|
| OPTIMISTIC | VDI: __ | VDI: __ | VDI: __ |
| NOMINAL | VDI: __ | VDI: __ | VDI: __ |
| PESSIMISTIC | VDI: __ | VDI: __ | VDI: __ |

SPREAD: Narrow = robust. Pessimistic < 0.6 = "high-risk"
```

### Step D4: CFMA — Conceptual Failure Mode Analysis (Weiss & Hari 2015, Multi-Perspective v2.0)

**Multi-Agent Selectivity check:** Same as D1 — if AMBER/RED complexity, run 3-domain parallel FM identification. If GREEN, single-agent CFMA.

**For AMBER/RED complexity (3-domain parallel CFMA):**

```
CFMA — {{project_id}} — Concept {{X}} (Multi-Perspective)

═══ STEP D4.1: INJECT CROSS-DOMAIN FMs FROM D1 COUPLING ═══

Extract from D1 domain-debate JSON side-car (```json:domain-debate-sidecar):
→ contradictions[] where severity = CRITICAL → mandatory cross-domain failure modes
→ coupling_scores where score ≥ 7 → high-priority interface for FM analysis

PRE-SEEDED CROSS-DOMAIN FMs:
| FM-ID | Source | Contradiction/Coupling | Mandatory? |
|-------|--------|----------------------|------------|
| FM-X01 | D1-CON-1 | {{CRITICAL contradiction from D1}} | YES |
| FM-X02 | D1-coupling | {{Co×Dien score ≥7: interface FM}} | YES |

═══ STEP D4.2: 3-DOMAIN PARALLEL FM IDENTIFICATION ═══

MECHANICAL FMs — failure modes visible from mechanical domain:
| FM-ID | Function | Failure Mode | Effect | S | Cause | F | Source |
|-------|----------|-------------|--------|---|-------|---|--------|
| FM-M01 | {{SF}} | {{mode}} | {{effect}} | {{1-10}} | {{cause}} | {{1-10}} | MECH |

ELECTRICAL FMs — failure modes visible from electrical domain:
| FM-ID | Function | Failure Mode | Effect | S | Cause | F | Source |
|-------|----------|-------------|--------|---|-------|---|--------|
| FM-E01 | {{SF}} | {{mode}} | {{effect}} | {{1-10}} | {{cause}} | {{1-10}} | ELEC |

AI/SW FMs — failure modes visible from software domain:
| FM-ID | Function | Failure Mode | Effect | S | Cause | F | Source |
|-------|----------|-------------|--------|---|-------|---|--------|
| FM-S01 | {{SF}} | {{mode}} | {{effect}} | {{1-10}} | {{cause}} | {{1-10}} | AI_SW |

═══ STEP D4.3: MERGE + DEDUPLICATE + SCORE ═══

Merge rules:
- Same failure mode seen by 2+ domains → keep, mark [2D] or [3D], use HIGHEST severity
- Cross-domain FMs from D4.1 → already scored, verify with domain perspectives
- Unique domain FMs → these are the HIGH-VALUE additions (single domain would miss the others)

UNIFIED CFMA TABLE:
| FM-ID | Function | Failure Mode | Effect | S | Cause | F | Detection | D | SFD | Source | Actions | Rev SFD |
|-------|----------|-------------|--------|---|-------|---|-----------|---|-----|--------|---------|---------|

FM SOURCE SUMMARY:
| Source | Count | Critical (SFD≥80) | Notes |
|--------|-------|--------------------|-------|
| MECH only | {{N}} | {{N}} | FMs visible only to mechanical |
| ELEC only | {{N}} | {{N}} | FMs visible only to electrical |
| AI_SW only | {{N}} | {{N}} | FMs visible only to software |
| CROSS [2D+] | {{N}} | {{N}} | FMs from D1 coupling or seen by 2+ domains |
| TOTAL | {{N}} | {{N}} | Must be 0 critical for concept selection |
```

**For GREEN complexity (single-agent CFMA, no parallel):**

```
CFMA — {{project_id}} — Concept {{X}}

| Function | Failure Mode | Effect | S(1-10) | Cause | F(1-10) | Detection | D(1-10) | SFD | Actions | Rev SFD |

SFD: ≥80=CRITICAL (resolve or reject), 40-79=IMPORTANT (track), <40=OK
```

**Rules (both modes):**
- SFD: >=80=CRITICAL (resolve or reject), 40-79=IMPORTANT (track), <40=OK
- WX DEFENSE: Always check training scar, environmental, integration failure modes
- CRITICAL (SFD>=80) MUST be zero for concept selection
- Multi-perspective CFMA typically finds 30-50% more FMs than single-agent (mostly cross-domain interface failures)
- **Time budget:** 20-30 min for multi-perspective, 10-15 min for single-agent

### Step D5: Sensitivity Analysis

```
SENSITIVITY — {{project_id}}

| Criterion | Weight +1 | Winner | Weight -1 | Winner | Stable? |
|-----------|-----------|--------|-----------|--------|---------|

CONCLUSION: [ROBUST / SENSITIVE to criterion Cx]
If sensitive → weight of Cx is the REAL decision.
```

### ICDM Extension (if --icdm active)

- Add lifecycle risk (sustainability, end-of-life, social impact)
- Add supply chain resilience scoring
- ICDM risk overlay output
- **CFMA Multi-Perspective (v2.0):** When ICDM is active, D4 multi-perspective is MANDATORY (not optional) because CSR-linked failure modes require cross-domain visibility. The domain-parallel CFMA feeds:
  - Pre-seeded FMs from D1 `contradictions[]` (JSON side-car)
  - Domain-specific FM source tracking for traceability to CSR functions
  - FM Source Summary table validates coverage across all 3 domains

**RESEARCH HOOK (knowledge gaps):** For every RTA knowledge gap classified NEW, generate one
Research Brief (`type: knowledge-gap`, `phase: P2`, `source_block: helix-p2-risk`,
`risk_if_wrong` = HIGH when the gap sits on a CRITICAL CFMA path) and list the brief_ids in
the gap-closing plan. Gaps with an unanswered brief stay OPEN in the risk register — a plan
line without evidence does not close a gap.

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/`:
- `BD_Coupling_Analysis.md`
- `BD_Assumption_Register.md`
- `BD_CFMA.md`
- `BD_Sensitivity_Analysis.md`

## CEO Checkpoint

```
═══ BLOCK BD RISK & INTEGRATION COMPLETE ═══
Coupling: [H/M/L per concept] (domain debate: {{ran/skipped}})
Assumptions: {{N}} explicit, {{M}} shadow ({{K}} unverified)
CFMA: {{mode: multi-perspective/single-agent}} — {{total}} FMs ({{MECH-only}}/{{ELEC-only}}/{{AI_SW-only}}/{{CROSS}})
CFMA Critical: {{count}} (must be 0 for selection)
D1→D4 injection: {{N}} cross-domain FMs pre-seeded from coupling contradictions
Sensitivity: [ROBUST / SENSITIVE to {{Cx}}]

CEO:
(1) ✅ Approve → tiếp tục Block BE (Selection)
(2) ⚠️ Resolve CFMA critical items first
(3) 🔄 Re-run with adjusted assumptions
(4) ⏸️ Dừng — cần verify shadow assumptions
```

## COD
- Coupling scoring: Offload (O2) — AI estimates
- Assumption listing: Offload (O2)
- CFMA generation: Offload (O2) — AI drafts
- Severity/frequency judgment: **Core (C)** — CEO + domain expert
- Sensitivity computation: Offload (O1)
- Risk acceptance: **Core (C)** — CEO acknowledges
