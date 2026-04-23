---
name: helix-project-init
description: Initialize a new HELIX project with charter, Triple Helix timeline, ICD v0 skeleton, and sync calendar. This skill should be used when the user asks to "init project", "new HELIX project", "start new product", "khoi tao du an moi", or needs to set up a fresh Pahl-Beitz design project from Phase 0.
---

# Helix Project Init — Phase 0 Setup

Bootstrap a new Workshop X product project with all Phase 0 artifacts: project charter, Triple Helix timeline (mechanical/electrical/AI domains), ICD v0 skeleton, and cross-domain sync calendar.

## When to Use

- Starting a new product development project
- User says "init project", "new HELIX project", "tao du an moi"
- After FORGE portfolio decision greenlights a new product
- When a product idea graduates from forge-scout to active development

## Workflow

### Step 1: Gather Inputs

Ask the user for:
1. **Product name** and short description (1-2 sentences)
2. **Target customer** (e.g., Viettel, MoD, export)
3. **Tier classification**: Tier 1 (Prototype), Tier 2 (Product Dev), Tier 3 (Strategic)
4. **Similar existing products** in FORGE library (AI suggests from portfolio)

Read from vault:
- `1_Projects/` — scan for naming convention and existing project IDs
- forge-portfolio output — check portfolio fit and resource conflicts
- forge-library — find similar product models for template reuse

### Step 1b: Portfolio Resource Conflict Gate (from DMIR×ODI Framework)

Before committing to a new project, check CEO capacity:

```
PORTFOLIO CONFLICT CHECK — {{today}}

Active projects by tier:
  Tier 1 (Prototype): __ projects (target: ≤2)
  Tier 2 (Product Dev): __ projects (target: ≤3)
  Tier 3 (Strategic): __ projects
  TOTAL active: __ (target: ≤7)

CEO hours estimate:
  Current committed: ~__ h/week across active projects
  Available for new project: ~__ h/week (minimum 5h needed)

VERDICT:
  ✓ CLEAR — capacity available, proceed
  ⚠ TIGHT — capacity marginal, CEO decides accept risk or defer
  ✗ OVERLOADED — ≥7 active projects OR <5h available → recommend DEFER or ARCHIVE-FIRST
```

IF OVERLOADED → present to CEO: "Archive or defer 1 project before adding?"
CEO decides: PROCEED / DEFER / ARCHIVE-FIRST (Core decision)

### Step 1c: Stakeholder Discovery Checklist (from DMIR Diagnosis)

Structure initial stakeholder identification — don't just ask "target customer":

```
STAKEHOLDER MAP — {{project_id}}

| # | Stakeholder | Role | Access | Priority | ODI Relevance |
|---|------------|------|:------:|:--------:|:-------------:|
| 1 | End operator (e.g., NCO, soldier) | Daily user | [have/need] | HIGH | Job executor |
| 2 | Procurement officer | Purchase decision | [have/need] | HIGH | Budget gate |
| 3 | Unit commander | Doctrine approval | [have/need] | MED | Requirements source |
| 4 | Maintenance team | Sustain operations | [have/need] | MED | Consumption chain |
| 5 | Training instructor | Integrates product | [have/need] | MED | Related job |
| 6 | Workshop/manufacturer | Builds product | [have/need] | LOW | Supply constraint |

ACCESS GAPS:
  If "Access = need" for ≥2 HIGH stakeholders:
    → Add to Status.md BLOCKING CONSTRAINTS
    → Flag: "Cannot validate ODI outcomes without stakeholder access"
    → Mitigation: proxy data from similar products, competitor user reviews

NOTE: Stakeholder list feeds /odi (Step 1: Define job executor)
```

### Step 2: Generate Project ID

Follow Workshop X naming convention:
```
VN-[CATEGORY]-[SEQ]    e.g., VN-AST-MSL-001, VN-12.7MM-SIM, BB-01
```

Verify no collision with existing project IDs in `1_Projects/`.

### Step 3: Generate Project Charter

```
PROJECT CHARTER — {{project_id}}
Date: {{today}}
Author: Workshop X CEO
Status: Phase 0 — Initialized

PRODUCT: {{product_name}}
DESCRIPTION: {{description}}
TIER: {{tier}} | TARGET CUSTOMER: {{customer}}

DOMAINS INVOLVED:
| Domain | Lead | Clock Speed | Notes |
|--------|------|-------------|-------|
| Co (Mechanical) | [TBD] | [weeks/sprint] | |
| Dien (Electrical) | [TBD] | [weeks/sprint] | |
| AI/Software | [TBD] | [weeks/sprint] | |

MILESTONES:
| Gate | Target Date | Deliverable | Status |
|------|------------|-------------|--------|
| G0 | {{today}} | Charter + ICD v0 | DONE |
| G1 | [+4-6 weeks] | Task Clarification complete | PENDING |
| G2 | [+8-12 weeks] | Conceptual Design selected | PENDING |
| G3 | [+16-20 weeks] | Embodiment Design frozen | PENDING |
| G4 | [+24-30 weeks] | Detail Design + manufacturing pkg | PENDING |

PHYSICAL GATE (Tier 1 MUST have within 30 days):
  Date: [TBD]
  Deliverable: [first prototype / test coupon / proof-of-concept]

SIMILAR PRODUCTS (from FORGE library):
- {{similar_1}} — reuse potential: [high/medium/low]
- {{similar_2}} — reuse potential: [high/medium/low]

ACH APPLICABILITY: [YES — run forge-shift / NO / TBD]

SUCCESS CRITERIA (must be specific + measurable):
1. [criterion 1]
2. [criterion 2]
3. [criterion 3]

## ODI INPUT (from DMIR×ODI Framework bridge)
ODI Report: [link to Phase 0 ODI report, or "NOT YET — run /odi"]
Top opportunities (score ≥10):
| # | Outcome Statement | Opp Score | → Requirement Category |
|---|-------------------|:---------:|----------------------|
| 1 | [DIM format] | [score] | → R-xxx |

VDI 2225 weight recommendation (from ODI opportunity scores):
| Criterion | ODI-Derived Weight (0-4) | Rationale |
|-----------|:------------------------:|-----------|
| [criterion matching top opportunity] | [weight] | Opp score [X] → weight [Y] |

Mapping rule:
  Opp score ≥15 → VDI weight 4 (extreme opportunity = must-have criterion)
  Opp score 12-15 → VDI weight 3 (high opportunity)
  Opp score 10-12 → VDI weight 2 (moderate)
  Opp score <10 → VDI weight 1 (low priority)

⚠ IF no ODI report exists:
  Flag: "Requirements will be engineer-assumption-based (17% success rate per Ulwick)"
  Recommend: Run /odi before /helix-task-clarify
  CEO decides: PROCEED WITHOUT ODI (accept risk) / RUN ODI FIRST

## BUSINESS CASE SUMMARY (P11 — Product Proposal)
| Dimension | Value | Confidence |
|-----------|-------|:----------:|
| Target market size | [units/year] | [L3-L5] |
| Unit price target | [range VND] | [L4-L5] |
| Development cost estimate | [$] | [L4-L5] |
| Break-even volume | [units] | [L5] |
| Time to first revenue | [months] | [L5] |
| Strategic value | [ACH compound / portfolio synergy / customer relationship] | CEO judgment |

⚠ IF ALL economic fields are [L5] AND strategic value not compelling:
  Flag: "No business case evidence — may be passion project, not product"
  CEO decides: PROCEED (strategic bet) / RESEARCH-FIRST / DEFER
```

### Step 4: Generate ICD v0 Skeleton

Interface Control Document version 0 — domains and interfaces identified, details TBD.

```
ICD v0 — {{project_id}}
Date: {{today}}
Status: SKELETON — details populated during Phase 1

DOMAIN BOUNDARIES:
  Co (Mechanical): [enclosure, mounting, thermal, structural]
  Dien (Electrical): [PCB, sensors, power, cabling]
  AI/Software: [firmware, ML models, data pipeline, UI]

INTERFACE REGISTER:
| IF-ID | From | To | Type | Description | Status |
|-------|------|----|------|-------------|--------|
| IF-001 | Co | Dien | Physical | Sensor mounting / PCB enclosure | TBD |
| IF-002 | Dien | AI | Data | Sensor signal → ADC → processor | TBD |
| IF-003 | Co | AI | Thermal | Heat dissipation for compute | TBD |
| IF-004 | Dien | Co | Power | Battery / PSU mounting | TBD |
| IF-005 | AI | Dien | Control | Actuator commands | TBD |

CONSTRAINTS INHERITED FROM FORGE:
- [from forge-shift: ACH constraints if applicable]
- [from forge-cost: budget envelope]
- [from forge-portfolio: resource sharing with other products]

ICD EVOLUTION PLAN:
  v0 (Phase 0): Skeleton — this document
  v1 (Phase 1): Requirements allocated to domains
  v2 (Phase 2): Concept-specific interfaces defined
  v3 (Phase 3): Frozen for embodiment — change control active
```

### Step 5: Generate Sync Calendar

```
CROSS-DOMAIN SYNC CALENDAR — {{project_id}}

SYNC POINTS (from Pahl-Beitz + Triple Helix):
| Sync | Phase | Purpose | Participants |
|------|-------|---------|-------------|
| S0 | 0→1 | Charter review, domain leads assigned | All |
| S1 | 1 | Requirements cross-check across domains | All |
| S2 | 1→2 | Essential problem agreement | All |
| S3 | 2 | Concept compatibility check (coupling) | All |
| S4 | 2→3 | Concept selection + ICD v2 freeze plan | All |
| S5 | 3 | First hardware available for AI testing | Co + AI |
| S6 | 3→4 | Embodiment freeze + ICD v3 sign-off | All |
| S7 | 4 | Manufacturing review with workshop | Co + Dien |

CADENCE: [weekly / bi-weekly] standups, 30 min max
ASYNC UPDATES: Status.md updated by each domain lead weekly
```

### Step 6: Create Vault Structure

Create the following files in `1_Projects/{{project_id}}/`:
- `_Project_Brief.md` — from charter above
- `Status.md` — initialized at Phase 0
- `ICD_v0.md` — from ICD skeleton above

Present all artifacts to user for review before creating files.

## Integration

```
helix-project-init READS FROM:
  - forge-portfolio → portfolio fit, resource conflicts
  - forge-library → similar product templates
  - forge-scout → ACH opportunity assessment
  - 1_Projects/ → existing project IDs (collision check)

helix-project-init WRITES TO:
  - helix-task-clarify → charter + ICD v0 as inputs for Phase 1
  - helix-sync-protocol → sync calendar as baseline
  - bridge-dashboard → new project appears in dashboard
  - bridge-risk-radar → initial risk register entry
```

## Rules

- Always present charter to user for review BEFORE creating files
- Tier 1 projects MUST have a physical gate within 30 days — enforce this
- Never skip domain identification — even single-domain projects must document why
- ICD v0 is a skeleton — do NOT fill in detailed specs at Phase 0
- Project ID must follow Workshop X naming convention
- If no similar product exists in FORGE library, flag as "greenfield" risk

## COD Classification

- Template generation from similar products: Offload (O1) — AI generates
- Project ID assignment: Offload (O1) — AI checks collisions
- Scope definition + milestone dates: **Core (C)** — CEO decides
- Domain lead assignment: **Core (C)** — CEO decides
- Tier classification: **Core (C)** — CEO decides based on strategic priority
- ICD v0 skeleton: Offload (O2) — AI drafts, CEO validates interfaces
