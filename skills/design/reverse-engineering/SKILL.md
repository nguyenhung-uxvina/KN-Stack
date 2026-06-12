---
name: reverse-engineering
description: Systematic reverse engineering pipeline v3.0 for defense products — from comparative MCDA evaluation through physical RE to production-ready redesign. Integrates VDI 2221, VDI 2206 V-Model, Pahl-Beitz methodology, OSINT gathering, and Vietnam defense context (ITAR-free, QPAN compliance) via a 3D-A-R-D cycle. Use for competitive product analysis, domestic redesign of imported defense systems, or cross-family technology RE. Triggers on: "reverse engineer", "RE product", "copy design", "analyze competitor", "domestic redesign", "dao nguoc ky thuat", "noi dia hoa", "đảo ngược kỹ thuật", "nội địa hóa sản phẩm quốc phòng".
---

Systematic reverse engineering pipeline v3.0 for defense products — from comparative evaluation through physical RE to production-ready redesign. Now includes FIELD mode (internal product intelligence from 1,064 deployed units) and TECHNOLOGY mode (cross-family technology domain RE). Integrates VDI 2221 (mechanical), VDI 2206 V-Model (mechatronic), Pahl-Beitz methodology, OSINT intelligence gathering, comparative MCDA evaluation, and partnership strategy with Vietnam defense context (ITAR-free, QPAN compliance). The "super skill" combining /nlm + /helix-* + /research + domain RE expertise into one compound workflow.

Usage: /reverse-engineering <product_or_artifact> [--mode full|mech|mecha|compare|field|technology|audit|capture|partner] [--notebook <alias>] [--project <project-id>] [--stage N] [--candidates "Product1,Product2,Product3"]

PATH setup (required for NLM commands):
```bash
export PATH="$PATH:/c/Users/ADMIN/AppData/Roaming/Python/Python313/Scripts"
export PYTHONIOENCODING=utf-8
export NO_COLOR=1
```

---

## FRAMEWORK: 3D-A-R-D Cycle

→ See `references/re-framework.md` for complete framework, VDI 2206 Inverted V-Model, and domain decomposition templates.

```
3D (Deconstruct → Decode → Document) — Tiếp cận artifact gốc
 A (Abstract) — Trừu tượng hóa → design intent + functional requirements
 R (Reconstruct) — P&B forward redesign với domestic constraints
 D (Deploy) — V&V + production transfer
```

**Key insight:** RE bắt đầu từ physical artifact, phải reconstruct intent TRƯỚC KHI redesign. Workflow nhạy cảm với: IP concerns, incomplete info, material/process mystery, domestic manufacturability.

---

## MODES

| Mode | Stages | Use When |
|------|--------|----------|
| **COMPARE** | C0→C1→C2→C3→C4 | PRE-RE: evaluate multiple candidates before committing (anti-anchoring) |
| **FULL** | 0→1→2→3→3P→4→5 | Complete RE project (new product) |
| **MECH** | 0→1→2→3→3P→4→5 | Purely mechanical product (no electronics/software) |
| **MECHA** | 0→1M→2M→3→3P→4M→5 | Mechatronic product (VDI 2206 V-Model) |
| **FIELD** | F1→F2→F3→F4→F5→F6 | Internal RE of own deployed products (1,064 units field intelligence) |
| **TECHNOLOGY** | T1→T2→T3→T4→T5→T6 | Cross-family technology domain RE (signature, autonomy, etc.) |
| **PARTNER** | 3P only | Partnership/acquisition strategy for selected product |
| **AUDIT** | 4 only | Adversarial review of existing RE work |
| **CAPTURE** | 5 only | Knowledge capture from completed RE project |

Default: **MECHA** (most WX products are mechatronic).

**Recommended sequence for new product category:** COMPARE first → select winner → then FULL/MECH/MECHA on selected product.

**Highest-ROI mode:** FIELD — zero additional hardware cost, maximum learning from 1,064 deployed units. Run FIELD before external RE.

---

## PIPELINE FLOW (6 Stages)

```
[FIELD] INTERNAL PRODUCT FIELD INTELLIGENCE (for own deployed products — highest ROI)
    ├── F1: Field Failure Pattern Analysis
    ├── F2: Customer Usage Pattern Discovery
    ├── F3: Competitor Displacement Analysis
    ├── F4: Next-Gen Driver Identification
    ├── F5: ACH Overlay Mapping
    └── F6: Cross-Product Learning + Galaxy Extraction
     ↓ Field Intelligence Report → MAINT-KIT pricing, next-gen roadmap

[TECHNOLOGY] CROSS-FAMILY TECHNOLOGY DOMAIN RE (signature, autonomy, etc.)
    ├── T1: Domain Definition + WX Application Scope
    ├── T2: OSINT Survey (academic, patents, commercial)
    ├── T3: Technology Decomposition (principles, approaches, trade-offs)
    ├── T4: WX Application Mapping (product priority)
    ├── T5: Capability Gap Analysis (build/buy/partner)
    └── T6: Technology Roadmap + Partnership Strategy
     ↓ Technology Capability Roadmap → cross-family enabler

[COMPARE] PRE-RE Comparative Evaluation (optional, recommended for new product categories)
    ├── C0: WX Reality Filter (team capacity, capital, phase alignment, ACH, compound test)
    ├── C1: OSINT Parity Gathering (equal depth across candidates)
    ├── C2: Design Philosophy + Technical Comparison
    ├── C3: Geopolitical + Cost + Delivery Risk
    └── C4: MCDA Selection + CEO Decision
     ↓ CEO selects product for RE
[0] IP & LEGAL GATE (go/no-go)
     ↓ CEO decides
[1] DECONSTRUCT — Physical Analysis
    ├── 1A: Artifact Deconstruction (geometry, material, process)
    ├── 1B: Material & Process Detective
    ├── 1C: Tolerance & Performance Reverse
    └── [MECHA] 1M: Domain Decomposition (Mech/Elec/Sw/Ctrl)
     ↓ CEO approves RE Deconstruction Report
[2] DECODE — Requirements Reconstruction
    ├── 2A: Design Intent Decoder (inverse P&B Task Clarification)
    ├── 2B: Functional Abstraction Engine (artifact → function structure)
    └── [MECHA] 2M: Cross-Domain Function Allocator + Control Law Reverser
     ↓ CEO approves Reconstructed Requirements
[3] RECONSTRUCT — P&B Forward Redesign
    ├── 3A: Modified Task Clarification (VN constraints)
    ├── 3B: Conceptual Alternatives (morphological matrix, IP-free)
    ├── 3C: VDI 2225 Concept Selection (defense RE weights)
    └── 3D: Divergence Map (what kept/modified/added/removed)
     ↓ CEO selects concept
[3P] PARTNERSHIP — Acquisition & Adaptation Strategy
    ├── 3P-A: Acquisition Structure Options (buy/assemble/co-dev/license)
    ├── 3P-B: Technology Transfer Priority Matrix (Tier 1-4)
    ├── 3P-C: Vietnam Adaptation Roadmap (environment/sovereignty/manufacturing)
    ├── 3P-D: Negotiation Framework (supplier motivations, VN leverage, contract architecture)
    └── 3P-E: Decision Gate Structure (6 gates over program lifecycle)
     ↓ CEO approves partnership strategy
[4] DEPLOY — Validation & Audit
    ├── 4A: V&V Strategy (component → subsystem → system → field)
    ├── 4B: Adversarial RE Audit (8 challenge dimensions)
    └── [MECHA] 4M: Integration Challenge Predictor + V-Model V&V
     ↓ CEO go/no-go for production
[5] KNOWLEDGE CAPTURE — Compound Learning
    ├── 5A: RE Technical Dossier
    ├── 5B: Design Pattern Library + Heuristics Database
    ├── 5C: Galaxy candidates (Three Laws extraction)
    └── 5D: Supplier Capability Map update
```

**RULE: Execute 1 stage, STOP, wait CEO approval. Never auto-continue to next stage.**

---

## MODE: FIELD — Internal Product Field Intelligence (v1.0)

**When:** RE own deployed products to extract maximum learning. Highest-ROI RE mode — zero additional hardware cost, 1,064 units of field data.

**Key insight:** Most RE skills focus on external products. FIELD mode reverses this — RE your OWN shipped products to understand what customers actually value, what fails in field, and what compounds into next-gen.

```
/reverse-engineering "VN-MGM" --mode field
/reverse-engineering "Towed Target 30mm" --mode field
/reverse-engineering "TARGET-DRONE" --mode field
```

**Applicable products (WX deployed fleet):**
| Product | Units | Priority | MAINT-KIT Potential |
|---------|-------|----------|-------------------|
| Towed Target (30mm+12.7mm) | 550 | HIGH — UTT-Towed foundation | $165K/yr @ $300/unit |
| VN-MGM | 300 | HIGH — cash cow intelligence | $90K/yr @ $300/unit |
| TARGET-DRONE | 200 | MEDIUM — ATT evolution | $60K/yr @ $300/unit |
| Naval Sim (Vega Prime) | 8 sys | LOW — TMS software intel | Software support contracts |
| BB-01 LOMAH | 3 | HIGH — signature tech compound | Strategic, not volume |
| VN-AST-MSL-001 | 2 bộ | HIGH — STT-B foundation | Strategic, not volume |

### F1: FIELD FAILURE PATTERN ANALYSIS

**COD: Core** (CEO interprets failure data) with **Offload** (AI compiles patterns)

```
FIELD FAILURE ANALYSIS — {{product}} ({{N}} units deployed)
Date: {{today}}

DEPLOYMENT TIMELINE:
| Year | Units Deployed | Cumulative | Operating Environment |
|------|---------------|------------|---------------------|

FAILURE MODE CATALOG:
| FM-ID | Failure Mode | Frequency | Severity | Detection | Environment | Root Cause | Fix Status |
|-------|-------------|-----------|----------|-----------|-------------|------------|------------|

MTBF ANALYSIS:
- Theoretical MTBF (design): {{hours}}
- Observed MTBF (field): {{hours}}
- Gap: {{%}} — root cause: {{explanation}}

ENVIRONMENTAL FACTORS:
| Factor | Design Spec | Actual Field Condition | Gap | Impact |
|--------|-----------|----------------------|-----|--------|
| Temperature | | VN tropical: 25-45°C, >80% humidity | | |
| Salt spray | | Coastal deployment | | |
| Shock/vibration | | Naval platform / rough terrain | | |
| UV exposure | | Tropical sun | | |

SEASONAL PATTERNS:
- Monsoon season failures: {{pattern}}
- Dry season failures: {{pattern}}
- Training cycle correlation: {{pattern}}

TOP 5 WARRANTY/REPAIR ISSUES:
1. {{issue}} — frequency: {{N/year}} — cost/fix: {{$}}
2-5. ...
```

**STOP. CEO reviews failure patterns. Proceed only after CEO validates.**

### F2: CUSTOMER USAGE PATTERN DISCOVERY

**COD: Core** (CEO has customer relationships)

```
CUSTOMER USAGE ANALYSIS — {{product}}

DESIGNED-FOR vs ACTUAL USAGE:
| Feature/Capability | Designed For | Actually Used For | Surprise Factor |
|-------------------|-------------|-------------------|----------------|

DEPLOYMENT SCENARIOS (observed):
| Scenario | Frequency | Was This Designed? | Customer Workaround |
|----------|-----------|-------------------|-------------------|

FEATURE UTILIZATION:
| Feature | Usage Rate | Customer Value Rating | Enhancement Request |
|---------|-----------|---------------------|-------------------|

CUSTOMER SEGMENTS (who actually buys and why):
| Segment | Units | Use Case | Price Sensitivity | Satisfaction |
|---------|-------|----------|------------------|-------------|

MAINTENANCE PATTERNS:
- Customer-performed maintenance: {{what, quality}}
- WX-required maintenance: {{what, frequency}}
- Unauthorized modifications observed: {{list — these reveal unmet needs}}

TRAINING EFFECTIVENESS (if applicable):
- How customers measure training value
- Reported training improvements
- Feature requests for better training outcomes
```

**STOP. CEO adds customer intelligence (Core — only CEO has these relationships).**

### F3: COMPETITOR DISPLACEMENT ANALYSIS

**COD: Offload** (AI researches) → **Core** (CEO validates from customer intel)

```
COMPETITOR DISPLACEMENT — {{product}}

WHAT DID WX REPLACE?
| Customer | Previous Solution | Why Switched to WX | Key Decision Factors |
|----------|-----------------|-------------------|---------------------|

CURRENT COMPETITIVE LANDSCAPE:
| Competitor | Product | Price vs WX | Capability vs WX | Threat Level |
|-----------|---------|------------|-----------------|-------------|

CUSTOMER WILLINGNESS-TO-PAY:
- Current WX price: ${{X}}
- Customer perceived value: ${{Y}}
- Competitor price: ${{Z}}
- Price elasticity estimate: {{elastic/inelastic}}
- Premium features customer would pay more for: {{list}}

WIN/LOSS ANALYSIS:
| Opportunity | Won/Lost | Against | Reason | Lesson |
|------------|----------|---------|--------|--------|

SWITCHING BARRIERS (WX advantage):
- Technical lock-in: {{specifics}}
- Relationship capital: {{specifics}}
- Integration complexity: {{specifics}}
- Cost of switching: {{estimate}}
```

### F4: NEXT-GEN DRIVER IDENTIFICATION

**COD: Core** (strategic product decisions)

```
NEXT-GEN DRIVERS — {{product}}

CUSTOMER-PULL DRIVERS (from F2 usage patterns):
| Driver | Source | Priority | Feasibility | Revenue Impact |
|--------|--------|----------|-------------|---------------|

TECHNOLOGY-PUSH DRIVERS (from WX capability):
| Driver | Technology Source | Priority | Investment | Timeline |
|--------|-----------------|----------|------------|---------|

COMPETITIVE-PRESSURE DRIVERS (from F3):
| Driver | Competitor Move | Response Urgency | WX Advantage |
|--------|----------------|-----------------|-------------|

REGULATORY/MARKET DRIVERS:
| Driver | Trigger | Timeline | Impact |
|--------|---------|---------|--------|

NEXT-GEN PRODUCT DEFINITION:
- {{product}}-v2 Requirements (top 10):
  1. {{req}} — source: {{F1/F2/F3/regulatory}}
  ...
- Estimated development cost: ${{range}}
- Estimated timeline: {{months}}
- Revenue projection: ${{range}}
- Resource requirements from 26-person team: {{N}} FTE × {{months}}
```

### F5: ACH OVERLAY MAPPING

**COD: Offload** (AI identifies opportunities) → **Core** (CEO validates ACH fit)

```
ACH OVERLAY — {{product}}

CURRENT PRODUCT: Pure hardware, no AI component.

ACH OPPORTUNITIES IDENTIFIED:
| Opportunity | Sub-function | AI Technology | Hardware Replaced/Augmented | Cost Impact | Value Impact |
|------------|-------------|---------------|---------------------------|-------------|-------------|
| O1 | {{function}} | {{ML type}} | {{component}} | {{save/add $}} | {{customer value}} |

MAINT-KIT ACH INTEGRATION:
- Predictive maintenance AI from field data: {{feasibility}}
- Diagnostic AI in MAINT-KIT: {{feasibility}}
- Usage analytics for customer insights: {{feasibility}}
- Data source: {{what sensors/data already exist}}

FIELD DATA AVAILABLE FOR AI TRAINING:
| Data Type | Volume | Quality | Accessibility | AI Application |
|-----------|--------|---------|---------------|----------------|

ACH PRIORITY RANKING (for this product):
| Priority | ACH Application | Expected ROI | Compound Potential | Recommended Phase |
|----------|----------------|-------------|-------------------|------------------|

→ Feed HIGH-priority items to /forge-shift for full SHIFT assessment
```

### F6: CROSS-PRODUCT LEARNING + GALAXY EXTRACTION

**COD: Offload** (AI compiles) → **Core** (CEO validates Galaxy candidates)

```
CROSS-PRODUCT LEARNING — {{product}}

PATTERNS TRANSFERABLE TO OTHER PRODUCTS:
| Pattern | Source Product | Applicable To | Transfer Effort | Value |
|---------|--------------|---------------|----------------|-------|

TECHNOLOGY REUSE OPPORTUNITIES:
| Technology/Component | Used In | Reusable For | Adaptation Needed |
|---------------------|---------|-------------|-----------------|

MAINT-KIT PORTFOLIO SIZING:
| Product | Installed Base | MAINT-KIT Price | Annual Revenue | NRE Required |
|---------|---------------|----------------|---------------|-------------|
| Total | 1,064 units | avg $300/yr | **$320K/yr** | near-zero |

GALAXY CANDIDATES (Three Laws extraction):
1. {{Law name}} — {{1 sentence}} — passes 3-question gate? Y/N
2. ...

FIELD INTELLIGENCE SUMMARY:
- Key finding 1: {{actionable insight}}
- Key finding 2: {{actionable insight}}
- Key finding 3: {{actionable insight}}

CEO ACTIONS FROM FIELD INTELLIGENCE:
| # | Action | Product | Priority | Timeline | Owner |
|---|--------|---------|----------|---------|-------|
```

**Output:**

```
=== FIELD MODE COMPLETE — {{product}} ===

Units analyzed: {{N}} deployed
Field failures catalogued: {{N}} modes
Customer usage patterns: {{N}} discovered
Competitor insights: {{N}} displacement events
Next-gen drivers: {{N}} identified
ACH opportunities: {{N}} ({{HIGH}} high priority)
MAINT-KIT revenue potential: ${{X}}/year
Galaxy candidates: {{N}}

DELIVERABLES:
1. Field Intelligence Report → 1_Projects/{{project}}/Ref/FIELD_INTEL_{{product}}_{{date}}.md
2. MAINT-KIT Business Case (if applicable)
3. Next-Gen Product Brief (draft)
4. ACH opportunities → feed to /forge-shift

HIGHEST-VALUE NEXT STEP: {{recommendation}}

CEO: approve report and route actions?
```

**STOP. Wait CEO approval.**

---

## MODE: TECHNOLOGY — Cross-Family Technology Domain RE (v1.0)

**When:** RE a technology domain (not a product) that enables multiple product families. Examples: signature generation, autonomous behavior, sensor fusion.

**Key insight:** Standard RE = 1 product → 1 redesign. TECHNOLOGY mode = 1 technology domain → enables N products. Higher leverage, longer timeline.

```
/reverse-engineering "Acoustic Signature Generation" --mode technology
/reverse-engineering "Autonomous Surface Behavior" --mode technology
/reverse-engineering "RCS Augmentation" --mode technology
```

**WX Priority Technology Domains:**
| Domain | Enables | Phase | Priority |
|--------|---------|-------|----------|
| Acoustic Signature Generation | UTT-Towed, future UUV | Phase 1 | HIGH |
| RCS Augmentation | Towed targets, STT-B, ATT | Phase 1-2 | HIGH |
| Magnetic Signature | UTT-Towed (mine warfare) | Phase 1 | MEDIUM |
| Infrared Signature | ATT, STT-B | Phase 2 | MEDIUM |
| AI Signature Synthesis | All families (ACH differentiator) | Phase 1+ | HIGH |
| Autonomous Surface Behavior | STT-B, VN-USV | Phase 2 | MEDIUM |

### T1: DOMAIN DEFINITION + WX APPLICATION SCOPE

**COD: Core** (CEO defines scope) with **Offload** (AI drafts)

```
TECHNOLOGY DOMAIN DEFINITION — {{domain}}

DOMAIN BOUNDARY:
- What this technology does: {{precise definition}}
- What's included: {{scope in}}
- What's excluded: {{scope out}}
- Why this matters for WX: {{strategic rationale}}

WX PRODUCT APPLICATION MAP:
| Product | Application | Priority | Timeline | Revenue Impact |
|---------|------------|----------|---------|---------------|

EXISTING WX CAPABILITY:
| Capability | Current Level (1-5) | Source | Gap to Target |
|-----------|-------------------|--------|-------------|
(1=awareness, 2=basic understanding, 3=can design, 4=can build, 5=can optimize)

TECHNOLOGY READINESS LEVEL:
- Global state of art: TRL {{N}}
- WX current: TRL {{N}}
- Target: TRL {{N}} by {{date}}
```

**STOP. CEO confirms domain scope.**

### T2: OSINT SURVEY (Academic, Patents, Commercial)

**COD: Offload** (AI searches) → **Core** (CEO selects sources)

```
TECHNOLOGY OSINT SURVEY — {{domain}}

ACADEMIC SOURCES:
| # | Source | Type | Institution | Relevance | Tier |
|---|--------|------|------------|-----------|------|
| 1 | NPS thesis on {{topic}} | Thesis | Naval Postgraduate School | Direct | A |
| 2 | IEEE paper on {{topic}} | Journal | {{university}} | High | A |
(Search: IEEE, NPS thesis database, Google Scholar, ResearchGate, arXiv)

PATENT LANDSCAPE:
| # | Patent | Holder | Filed | Status | Relevance | Freedom to Operate |
|---|--------|--------|-------|--------|-----------|-------------------|
(Search: Google Patents, Espacenet, USPTO, EPO)

COMMERCIAL PRODUCTS (study marketing + specs):
| # | Product | Manufacturer | Price Range | Key Specs | WX Relevance |
|---|---------|-------------|------------|-----------|-------------|

MILITARY APPLICATIONS (public):
| # | System | Country | Application | Published Info |
|---|--------|---------|------------|---------------|

DUAL-USE TECHNOLOGY (commercial → defense):
| # | Commercial Application | Technology | Defense Translation |
|---|----------------------|-----------|-------------------|

NLM NOTEBOOK SETUP:
→ Create notebook "TECH: {{domain}}"
→ CEO selects sources for ingestion
→ Source Quality Gate (same protocol as FULL mode NLM-1 through NLM-4)
```

**STOP. CEO selects sources for NLM ingestion.**

### T3: TECHNOLOGY DECOMPOSITION

**COD: Offload** (AI analyzes) → **Core** (CEO validates)

```
TECHNOLOGY DECOMPOSITION — {{domain}}

KEY PRINCIPLES:
| Principle | Description | Maturity | WX Feasibility |
|-----------|-------------|----------|---------------|

APPROACHES COMPARISON:
| Approach | Pros | Cons | Cost | Complexity | Best For |
|----------|------|------|------|-----------|---------|

PERFORMANCE PARAMETERS:
| Parameter | State-of-Art | Good-Enough for WX | WX Current | Gap |
|-----------|------------|-------------------|-----------|-----|

TRADE-OFFS:
| Trade-off | Option A | Option B | WX Preferred | Rationale |
|-----------|----------|----------|-------------|-----------|

COMMON PITFALLS (from literature):
| Pitfall | How Others Failed | WX Mitigation |
|---------|------------------|-------------|
```

### T4: WX APPLICATION MAPPING

**COD: Core** (product decisions)

```
WX APPLICATION MAPPING — {{domain}}

PER-PRODUCT APPLICATION:
| Product | Sub-function | Technology Approach | Priority | Development Effort |
|---------|-------------|-------------------|----------|-------------------|

CROSS-PRODUCT SYNERGY:
| Synergy | Products | Shared Component | Reuse % | IRONMESH Module? |
|---------|----------|-----------------|---------|-----------------|

COMPOUND LEARNING OPPORTUNITIES:
| Data Source | Product | AI Training Application | Volume | Quality |
|-----------|---------|----------------------|--------|---------|

ACH INTEGRATION STRATEGY:
- Commodity hardware: {{what to buy, not build}}
- WX AI value-add: {{what makes WX unique}}
- Compound moat: {{how learning widens advantage over time}}
```

### T5: CAPABILITY GAP ANALYSIS

**COD: Core** (build/buy/partner decisions)

```
CAPABILITY GAP — {{domain}}

BUILD vs BUY vs PARTNER:
| Capability | Build | Buy | Partner | Recommended | Rationale |
|-----------|-------|-----|---------|-------------|-----------|

TEAM CAPABILITY ASSESSMENT:
| Skill Needed | Available in WX? | Gap | Closing Strategy |
|-------------|-----------------|-----|-----------------|

EQUIPMENT/INFRASTRUCTURE NEEDS:
| Item | Have? | Cost | Lead Time | Priority |
|------|-------|------|-----------|----------|

ACADEMIC PARTNERSHIP OPPORTUNITIES:
| Institution | Expertise | Collaboration Model | Cost | Timeline |
|------------|-----------|-------------------|------|---------|
(Priority: VN universities first → ASEAN → international)
```

### T6: TECHNOLOGY ROADMAP + PARTNERSHIP STRATEGY

**COD: Core** (strategic decisions)

```
TECHNOLOGY ROADMAP — {{domain}}

PHASE 1 ({{year range}}): Foundation
- Deliverables: {{list}}
- Resources: {{N}} FTE + ${{budget}}
- Milestone: {{specific technical milestone}}

PHASE 2 ({{year range}}): Expansion
- Deliverables: {{list}}
- Resources: {{N}} FTE + ${{budget}}
- Milestone: {{specific technical milestone}}

PHASE 3 ({{year range}}): Maturity
- Deliverables: {{list}}
- Resources: {{N}} FTE + ${{budget}}
- Milestone: {{specific technical milestone}}

PARTNERSHIP STRATEGY:
| Partner Type | Candidate | Value | Cost | Priority |
|-------------|-----------|-------|------|----------|
| Academic (VN) | {{name}} | {{value}} | ${{X}}/yr | HIGH |
| Academic (intl) | {{name}} | {{value}} | ${{X}}/yr | MEDIUM |
| Commercial | {{name}} | {{value}} | ${{X}}/yr | case-by-case |

IP STRATEGY:
- Trade secrets: {{what to protect internally}}
- Academic publication: {{what to publish for reputation}}
- Patents: {{defensive only, if any}}

TOTAL INVESTMENT:
- Phase 1: ${{range}}
- Team: {{N}} FTE (from existing 26-person team + {{N}} new hires)
- Timeline to first product application: {{months}}
- Expected ROI: {{range}}

GALAXY CANDIDATES:
1. {{Law name}} — {{description}}
2. ...
```

**Output:**

```
=== TECHNOLOGY MODE COMPLETE — {{domain}} ===

OSINT sources surveyed: {{N}} ({{academic}}/{{patent}}/{{commercial}})
Key principles identified: {{N}}
Approaches compared: {{N}}
WX products enabled: {{N}}
Capability gaps: {{N}} ({{build}}/{{buy}}/{{partner}})
Investment required: ${{range}} over {{years}}

DELIVERABLES:
1. Technology Capability Roadmap → 1_Projects/{{project}}/Ref/TECH_{{domain}}_{{date}}.md
2. Partnership recommendations
3. NLM notebook: TECH-{{alias}}
4. Galaxy candidates: {{N}}

RECOMMENDED NEXT STEPS:
1. {{action}} — {{owner}} — {{timeline}}
2. ...

CEO: approve roadmap and authorize Phase 1 investment?
```

**STOP. Wait CEO approval.**

---

## MODE: COMPARE — Pre-RE Comparative Evaluation (v2.0)

**When:** Before committing to RE a specific product. Evaluates 2-5 candidates side-by-side to counter anchoring bias and ensure best selection.

**Anti-anchoring principle:** Deep-diving one product first creates confirmation bias. COMPARE mode enforces EQUAL evaluation depth across all candidates before commitment.

```
/reverse-engineering "TRV Program" --mode compare --candidates "Simsek-K,Abhyas,Mirach-40"
```

### C0: WX REALITY FILTER

**COD: Core** — CEO validates reality check before investing COMPARE effort.

Before ANY comparative evaluation, filter candidates through WX reality constraints:

```
=== WX REALITY FILTER — {{product category}} ===

FILTER CRITERIA (ALL must pass):

☐ TEAM CAPACITY: Can WX (26 người, growing to 30-35) handle this?
  - FTE required for RE + development: {{N}}
  - >10 FTE dedicated = AUTO-DEFER
  - Assessment: PASS / FAIL / CONDITIONAL

☐ CAPITAL DISCIPLINE: Within Phase 1 $8-15M total budget?
  - Estimated total investment: ${{range}}
  - >$2M single line item = requires deep justification
  - Assessment: PASS / FAIL / CONDITIONAL

☐ PHASE ALIGNMENT: Serves G1 (2027: $5M + UTT-Towed) or G2 (2029: $8M + STT-B + export)?
  - Gate served: G{{N}}
  - Timeline fit: PASS / FAIL
  - Assessment: PASS / FAIL

☐ ACH OVERLAY: Has clear AI-Compensates-Hardware angle?
  - ACH sub-functions identified: {{list}}
  - Commodity + AI = premium? YES / NO / UNCLEAR
  - Assessment: PASS / FAIL

☐ COMPOUND TEST: Builds on existing competence?
  - Compounds: towed targets (550) / target drones (200) / naval sims (8) / BB-01 (3) / VN-AST (2) / VN-MGM (300)
  - Specific foundation: {{which existing product/skill}}
  - Assessment: PASS / FAIL

☐ ASEAN EXPORT: Has exportable ITAR-free version?
  - Export potential: HIGH / MEDIUM / LOW / NONE
  - ITAR-free path: YES / NO / PARTIAL
  - Assessment: PASS / FAIL / N/A

VERDICT:
- Criteria passed: {{N}}/6
- FAIL ≥3 = AUTO-DEFER with documented reason
- Decision: PROCEED TO C1 / DEFER / KILL

⚠️ ANALYST TRAP CHECK: "Is this RE work or just interesting analysis?"
  - Does this directly enable a product WX can ship within 3 years?
  - YES → proceed | NO → defer to Phase 2+ or Area monitoring
```

**STOP. CEO approves Reality Filter before any COMPARE work.**

### C1: OSINT PARITY GATHERING

**COD: Offload** (AI gathers) → **Core** (CEO validates parity)

For EACH candidate, gather EQUAL depth across 10 layers:

| Layer | What to Collect |
|-------|----------------|
| 1. Manufacturer info | Brochures, datasheets, expo presentations, annual reports |
| 2. Government statements | Defense ministry announcements, parliamentary answers, CAG reports |
| 3. Technical publications | Academic papers, university research, conference papers |
| 4. Trade press | Janes, Flight Global, Defense News, regional publications |
| 5. Export customers | Known acquisitions, evaluations, competitive wins/losses |
| 6. Specifications | Cross-referenced spec table with confidence per cell |
| 7. Operational history | Flight tests, demos, incidents, deployments |
| 8. Development timeline | Program start → first flight → production → IOC → export |
| 9. Competitive intelligence | What competitors say about each other |
| 10. Independent analysis | SIPRI, IISS, RAND, academic comparative studies |

**Specification Confidence Matrix (identical for all candidates):**
| Parameter | Candidate A | Source | Confidence | Candidate B | Source | Confidence | ... |

**Parity Check (CEO gate):**
- Same categories collected for all?
- Similar depth per candidate?
- Gaps identified equally?
- If one candidate has 90% coverage and another 40% → spend more time on the weaker one BEFORE proceeding

**NLM setup:** Create one NLM notebook per candidate (CEO selects sources per notebook, Source Quality Gate per notebook).

**Output:** Three-Way OSINT Dossier with equal-depth documentation.

**STOP. CEO approves parity before proceeding.**

### C2: DESIGN PHILOSOPHY + TECHNICAL COMPARISON

**COD: Core** (CEO validates scoring) with **Offload** (AI drafts analysis)

**Step C2a — Design Philosophy Analysis (per candidate):**

For each candidate, analyze:
- Historical context (country's defense industry evolution)
- Strategic design drivers (multi-theater, operator skill, supply chain autonomy, export economics)
- Engineering culture traits (strengths, common approaches)
- Cost-performance trade-off philosophy
- Product family strategy
- Indigenous technology use

**Output:** Design philosophy comparative matrix:
| Dimension | Candidate A | Candidate B | Candidate C |
| Heritage depth | | | |
| Performance ambition | | | |
| Technology maturity | | | |
| Cost positioning | | | |
| Customization flexibility | | | |
| Export openness | | | |
| TT willingness | | | |
| Support sustainability | | | |

**Step C2b — Technical Head-to-Head:**

Evaluate ALL candidates against **Vietnam's specific requirements** (not general excellence):

7 dimensions with VN-specific weighting:
1. **Flight Performance** (15%) — speed, ceiling, endurance, range, sea-skimming
2. **Signature Replication** (20%) — RCS augmentation, IR, emissions, kinematic profile, threat library
3. **Propulsion** (10%) — engine maturity, domestic production rights, fuel compatibility
4. **Avionics** (10%) — flight control, navigation, datalink, encryption sovereignty
5. **Launch/Recovery** (5%) — method, complexity, reusability, naval compatibility
6. **Mission Capability** (10%) — autonomous mission, waypoint nav, multi-drone, mission planning SW
7. **Lifecycle Support + TT Openness** (30%) — manufacturer stability, spare parts, technical data access, upgrade path, training

**Sensitivity analysis:** Re-run scoring with 3-4 different weight scenarios (tech-first, TT-first, risk-averse, cost-first). Show how winner changes.

**STOP. CEO reviews technical comparison before proceeding.**

### C3: GEOPOLITICAL + COST + DELIVERY RISK

**COD: Core** (strategic decisions)

**Step C3a — Geopolitical Risk Assessment:**
- Bilateral relations quality (VN ↔ each supplier country)
- Strategic alignment (shared concerns, non-alignment compatibility)
- Export control friction (ITAR/Wassenaar/EU/national)
- Third-country complication risks
- Long-term stability (20-year outlook)
- Customer priority (how important is VN to this supplier?)
- Broader partnership potential (beyond this product)

**Step C3b — Total Cost of Ownership (20-year):**
| Cost Category | Candidate A | Candidate B | Candidate C |
| Acquisition (visible) | | | |
| Acquisition (hidden: test equip, tools, facilities) | | | |
| Technology Transfer | | | |
| Operating (per flight × flights/year × 20 years) | | | |
| Infrastructure | | | |
| Personnel (training + salaries) | | | |
| Upgrades + obsolescence | | | |
| Risk premium (delivery/currency/political) | | | |
| **TOTAL TCO** | | | |

Value-per-dollar: (Technical score + Industrial score) / TCO

**Step C3c — Delivery Risk Assessment:**
| Risk Dimension | Candidate A | Candidate B | Candidate C |
| Program maturity | | | |
| Production capacity | | | |
| Supply chain | | | |
| Contract execution track record | | | |
| Technical risk | | | |
| Customization risk | | | |
| External factors | | | |

On-time delivery probability per candidate.

**STOP. CEO reviews full picture before MCDA.**

### C4: MULTI-CRITERIA DECISION + CEO SELECTION

**COD: Core** — CEO makes final selection (non-delegable)

**Step C4a — MCDA Aggregate Scoring:**

| Category | Weight | Candidate A | Candidate B | Candidate C |
|----------|--------|------------|------------|------------|
| Technical Capability | 30% | | | |
| Industrial Partnership | 25% | | | |
| Geopolitical Fit | 15% | | | |
| Cost Effectiveness | 15% | | | |
| Delivery Reliability | 15% | | | |
| **WEIGHTED TOTAL** | | | | |

**Step C4b — Sensitivity across 5+ scenarios:**
- Baseline → winner?
- Tech-first (50% tech) → winner?
- Industrial-first (40% industrial) → winner?
- Risk-averse (30% delivery) → winner?
- Cost-first (30% cost) → winner?
- Strategic-first (30% geopolitical) → winner?

**Robustness:** How many scenarios does each candidate win?

**Step C4c — Strategic options:**
- Single supplier lock-in
- Phased approach (supplier A for quick capability, supplier B for long-term partnership)
- Hybrid (buy from A, co-develop with B)

**Step C4d — Negotiation Leverage Analysis:**
Per supplier: motivations, pressure points, what they'll concede, what they'll resist, Vietnam's leverage, cultural considerations.

**Output:**

```
=== COMPARE MODE COMPLETE — {{product category}} ===

Candidates evaluated: {{N}} (equal depth)
MCDA winner (baseline): {{name}} (score: {{X}}/10)
Robust winner ({{N}}/{{total}} scenarios): {{name}}
Strategic recommendation: {{single/phased/hybrid}}

CEO DECISION REQUIRED:
1. Select product for RE pipeline (FULL/MECH/MECHA mode)
2. Select partnership strategy (direct purchase / assembly / co-dev / license)
3. Approve negotiation approach

Save to: 1_Projects/{{project}}/Ref/COMPARE_{{category}}_{{date}}.md
```

**STOP. CEO selects. Then proceed to FULL/MECH/MECHA mode on selected product.**

---

## PIPELINE INFRASTRUCTURE (aligned with HELIX mega-skill architecture)

### Pipeline State File

Create at project start, update after each stage:

```
File: 1_Projects/{{project}}/RE/{{product}}/_pipeline_state.md

---
project: {{project}}
product: {{product}}
pipeline: reverse-engineering v3.0
mode: [full|mech|mecha|field|technology|compare]
started: {{date}}
updated: {{date}}
---

## Stage Progress
| Stage | Name | Status | Started | Completed | CEO Approved |
|-------|------|--------|---------|-----------|-------------|
| 0 | IP & Legal Gate | PENDING | - | - | - |
| 1 | DECONSTRUCT | PENDING | - | - | - |
| 2 | DECODE | PENDING | - | - | - |
| 3 | RECONSTRUCT | PENDING | - | - | - |
| 3P | PARTNERSHIP | PENDING | - | - | - |
| 4 | DEPLOY | PENDING | - | - | - |
| 5 | KNOWLEDGE CAPTURE | PENDING | - | - | - |

## Deliverables
[populated per stage — tracks file paths]

## CEO Decisions
[populated at each checkpoint]

## Requirements Delta Log
[populated when Stage 3 modifies Stage 2 requirements — VDI 2221:2019 co-evolution]
```

### Data Bus Contract (exact output filenames per stage)

| Stage | Output File | Content | Read By |
|-------|-----------|---------|---------|
| 0 | `RE_{{product}}_S0_Legal_Gate.md` | IP risk matrix, go/no-go | S1, all |
| 1A | `RE_{{product}}_S1A_Deconstruction.md` | 4-layer physical analysis | S2 |
| 1B | `RE_{{product}}_S1B_Material_Process.md` | Material + VN gap | S2, S3 |
| 1C | `RE_{{product}}_S1C_Tolerance_Perf.md` | Tolerance hierarchy | S2, S3 |
| 1M | `RE_{{product}}_S1M_Domain_Decomp.md` | 4-domain decomposition | S2M |
| 2A | `RE_{{product}}_S2A_Requirements.md` | Reconstructed req list (17 P&B categories, D/W) | S2B, S3 |
| 2A-TVDT | `RE_{{product}}_S2A_TVDT.md` | Target Values Decision Table | S3 |
| 2B | `RE_{{product}}_S2B_Function_Structure.md` | 6-flow function structure | S3 |
| 2B-SF | `RE_{{product}}_S2B_Solution_Det_SF.md` | Solution-determining sub-function | S3 |
| 2B-DT | `RE_{{product}}_S2B_Design_Type.md` | RE complexity (Green/Amber/Red) | S3 |
| 2M | `RE_{{product}}_S2M_Cross_Domain.md` | Cross-domain analysis | S3 |
| 3A | `RE_{{product}}_S3A_Modified_Req.md` | VN-adapted requirements | S3B |
| 3B | `RE_{{product}}_S3B_Morpho_Matrix.md` | IP-free alternatives | S3C |
| 3C | `RE_{{product}}_S3C_VDI2225.md` | Concept evaluation | S3D |
| 3D | `RE_{{product}}_S3D_Divergence_Map.md` | Kept/modified/added/removed | S4 |
| 3-DELTA | `RE_{{product}}_Requirements_Delta_Log.md` | Stage 2↔3 req co-evolution | S2, S3, S4 |
| 4A | `RE_{{product}}_S4A_VV_Strategy.md` | V&V plan | S5 |
| 4B | `RE_{{product}}_S4B_Audit.md` | 8-challenge audit | S5 |
| 5 | `RE_{{product}}_Dossier.md` | Complete RE dossier | Archive |

**Contract Rule:** Each stage MUST validate its input files exist before running. If missing → report which stage needs to run first.

### Input Validation Protocol (before each stage)

```
BEFORE running Stage {{N}}:
1. Read _pipeline_state.md → determine current state
2. Check input files exist:
   - Required: {{list from data bus}}
   - Optional: {{list}}
3. If required input MISSING → "Stage {{M}} chưa hoàn thành. Chạy Stage {{M}} trước."
4. If optional input MISSING → warn CEO but proceed
5. Load context from input files
6. Execute stage
```

### RE Complexity Classification (like HELIX design type)

Determined in Stage 2B, cascades to Stage 3:

| RE Complexity | Criterion | Stage 3 Depth | Time Budget |
|--------------|----------|---------------|-------------|
| **GREEN** (Variant-level) | Known product class, WX has similar, minor adaptation | Minimal redesign | 30-40% |
| **AMBER** (Adaptive-level) | Known class, significant subsystems novel for WX | Deep on novel SFs only | 60-70% |
| **RED** (Original-level) | New product class, WX has no precedent | Deep everywhere | 100% |

**Quick mode calibration:** For AMBER, Stage 3 must specify per-SF depth:
- Novel SFs (no WX experience) → DEEP search (all methods in morpho matrix)
- Known SFs (WX has prior art) → SHALLOW search (catalogue + WX pattern library only)

---

## STAGE 0: IP & LEGAL GATE

**COD: Core** — CEO must make go/no-go decision.

Before ANY RE work, assess legal landscape:

### 0A — IP Landscape
- Patents relevant (search Google Patents, Espacenet)
- Trade secret indicators (proprietary formulations, undocumented processes)
- Patent expiration status + jurisdictional coverage
- Design patents vs utility patents implications

### 0B — Export Control
- ITAR categories (USML Category I-XXI)
- EAR classifications (ECCN) for dual-use
- Wassenaar Arrangement controls
- Country of origin + sanctions considerations

### 0C — Vietnam Legal Framework
- Luat Cong nghiep Quoc phong 2024
- Law 32/2021/QH15 procurement
- IP Law Vietnam 2022 amendments
- Technology transfer agreement requirements

### 0D — RE Legality Assessment
- Clean-room vs contaminated RE
- Documentation of independent development
- Third-party source chain of custody
- Publication/distribution restrictions

### 0E — Safer Path Recommendations
- Low-risk focus areas (non-patented mechanical interfaces)
- Design-around strategies
- Documentation practices for independent creation
- Collaboration alternatives (licensing, JV)

**Output:**

```
=== RE LEGAL GATE — {{product}} ===

IP RISK MATRIX:
| Risk Category | Likelihood | Impact | Rating |
|--------------|-----------|--------|--------|

RECOMMENDATION: GO / CONDITIONAL GO / NO-GO
CONDITIONS (if conditional):
- {{condition 1}}
- {{condition 2}}

CEO DECISION: ___
```

**STOP. Wait CEO go/no-go.**

---

## STAGE 1: DECONSTRUCT — Physical Analysis

**COD: Offload** (AI drafts analysis) → **Core** (CEO validates inferences)

### 1A — Artifact Deconstruction

4-layer systematic analysis:

**Layer 1 — Geometric & Dimensional:**
- Overall envelope (LxWxH, mass, CG)
- Critical dimensions + tolerance stack-up inference
- GD&T features observed (datum structure, tolerance zones)
- Surface finish requirements (Ra estimation)
- Non-obvious features (cooling channels, stress relief, manufacturing witness marks)

**Layer 2 — Material & Process Inference:**
- Material candidates per component (with confidence %)
- Manufacturing process evidence (casting/machining/welding marks)
- Surface treatment (anodizing, phosphating, plating, painting)
- Joining methods (threaded, welded, bonded, riveted, press-fit)

**Layer 3 — Functional Decomposition:**
- Component inventory + suspected function
- Power/signal flow paths
- Kinematic chains + DOF analysis
- Interface points (mechanical, electrical, fluid, thermal)

**Layer 4 — Hidden Design Intent:**
- Why this geometry? (not just what)
- Safety factors implied (over-sized bearings → reliability critical)
- Manufacturing era signals (technology available at design time)
- Operational environment clues (sealing, corrosion protection, shock mounts)

**Output: RE Deconstruction Report** with confidence (High/Medium/Low) per inference + Unknown Items List.

### 1B — Material & Process Detective

```
TABLE A — Material Identification:
| Component | Visual Evidence | Material Candidates | Most Likely | Confidence % | Verification Method |

TABLE B — Manufacturing Process:
| Feature | Process Evidence | Process Candidates | VN Alternative | Cost/Quality Trade-off |

TABLE C — Surface Treatment:
| Surface | Treatment Evidence | Spec Estimate | VN-Available Alternative |

TABLE D — Heat Treatment:
| Component | Evidence | Likely HT Process | VN Alternative |

TABLE E — Vietnam Manufacturing Capability Gap:
| Component | Original Spec | VN Alternative | Performance Impact | Cost Impact | Priority |
  ✅ Available in VN | ⚠️ Limited | ❌ Not available | 🔄 Substitute exists
```

Flag **strategic bottlenecks** for technology sovereignty.

### 1C — Tolerance & Performance Reverser

**Tolerance hierarchy:**
- Tier 1 (Functional Critical): ±0.01-0.05mm — directly affects function
- Tier 2 (Interface Critical): ±0.02-0.1mm — mating surfaces
- Tier 3 (Assembly Critical): ±0.1-0.3mm — clearances
- Tier 4 (Cosmetic): ±0.5mm+ — non-functional

**Analysis deliverables:**
- Datum structure reverse (primary → secondary → tertiary)
- GD&T inference per critical feature
- Fits & clearances (ISO 286)
- Critical performance parameters (loads, stresses, safety factors, fatigue life)
- Manufacturing capability requirements (CNC grade, measurement equipment)

### 1M — Domain Decomposition (MECHA mode only)

→ See `references/re-framework.md` Section "VDI 2206 Inverted V-Model"

Tach integrated artifact thanh 4 domain views:

**Domain 1 — Mechanical:** structural, kinematic, thermal, sealing, vibration/shock
**Domain 2 — Electronic:** power, signal conditioning, processing, sensors, actuators, interconnects, PCB analysis
**Domain 3 — Software:** bootloader, RTOS/OS, drivers, middleware, application, control algorithms, safety/monitoring
**Domain 4 — Control:** control loops (inner/middle/outer/supervisory), state machines, safety logic

**Critical output — Cross-Domain Mapping Matrix:**
| Function | Mech Role | Elec Role | Sw Role | Ctrl Role | Integration Concerns |

**System Boundary & Black Box:**
- Context diagram (external entities + interfaces)
- Interface inventory (mech/elec/digital/analog/RF/pneumatic/optical)
- Behavioral modes (Off/Standby/Init/Normal/Emergency/Maintenance/Shutdown)
- Stimulus-response mapping (foundation for V&V)

**NLM integration (if sources available):**

#### NLM-1: Create Notebook
```bash
nlm notebook create "RE: {{product}}"
nlm alias set re-{{short}} {{uuid}}
```

#### NLM-2: Present Sources to CEO (Core — do not skip)

Collect all available sources (technical manuals, patents, photos, CAD files, similar product docs) and present to CEO for selection:

```markdown
## RE Sources — {{product}}

| # | Title | Type | Source | Relevance |
|---|-------|------|--------|-----------|
| 1 | {{manual}} | PDF/URL | {{origin}} | Direct — original product doc |
| 2 | {{patent}} | Patent | patents.google.com | IP landscape |
| 3 | {{similar product datasheet}} | URL | {{oem}} | Comparable product |
| ...

CEO: Chon sources nao de add vao NLM notebook? (Core — CEO quyet dinh)
```

**STOP. Wait CEO source selection.**

#### NLM-3: Add Selected Sources + Source Dedup

```bash
# For each CEO-selected source:
nlm source add re-{{short}} --url "{{url}}"
# OR for local files:
nlm source add re-{{short}} --file "{{local_pdf}}"
```

Source dedup check before each add:
```bash
nlm source list re-{{short}} 2>&1
# URL match → skip: "Already in notebook"
```

#### NLM-4: SOURCE QUALITY GATE (Core — do not skip)

After ALL `source add` calls, verify ingestion:

```bash
nlm source list re-{{short}}
# Compare ingested count vs selected count
```

```markdown
=== SOURCE QUALITY GATE — RE: {{product}} ===

INGESTION REPORT:
| # | Title | Type | Status | Reason |
|---|-------|------|:------:|--------|
| 1 | {{source}} | PDF | ✅ OK | |
| 2 | {{source}} | URL | ❌ FAILED | Paywall / 403 / JS-rendered |

Ingested: {{N}} / {{total selected}}
Failed: {{M}} sources
```

**For each failed source — try 3 recovery methods:**

```
RECOVERY 1: Alt URL → WebSearch "{{title}} filetype:pdf OR preprint"
  → If found → nlm source add re-{{short}} --url "{{alt_url}}"

RECOVERY 2: WebFetch → text injection
  → WebFetch original URL → nlm source add re-{{short}} --text "{{content}}" --title "{{title}}"

RECOVERY 3: YouTube substitute
  → Search "{{title}} explained" on YouTube → nlm source add re-{{short}} --url "{{yt_url}}"

IF ALL FAIL: Log as "✗ UNRECOVERABLE" → add to gap list
```

**Present to CEO:**

```markdown
=== SOURCE QUALITY GATE — RE: {{product}} ===

✅ Ingested: {{N}} sources
🔄 Recovered: {{R}} via alt channel
❌ Failed: {{F}} unrecoverable

FAILED SOURCES (if any):
| # | Source | Why Failed | Impact on RE |
|---|--------|-----------|-------------|

CEO OPTIONS:
(1) ✅ Proceed — sources sufficient for RE analysis
(2) 📎 CEO adds source manually (provide URL/PDF path)
(3) 🔍 Search deeper for alternatives
(4) ⏸️ Pause — CEO will find source offline

CEO: xac nhan du nguon? Chi khi approve moi tien hanh analysis.
```

**STOP. Do NOT run NLM queries or generate reports until CEO confirms source quality.**

**Output:**

```
=== STAGE 1 COMPLETE — {{product}} DECONSTRUCTION ===

Components catalogued: {{N}}
Materials identified: {{N}} ({{avg_confidence}}% avg confidence)
Critical dimensions: {{N}} Tier 1 features
[MECHA] Domains mapped: Mech({{N}}) / Elec({{N}}) / Sw({{N}}) / Ctrl({{N}})
Unknown items requiring physical inspection: {{N}}
Strategic bottlenecks (VN capability gap): {{N}}

TOP 5 UNKNOWNS (need physical test/inspection):
1. {{item}} — {{why unknown}}
...

CEO: approve deconstruction report to proceed to Stage 2?
```

**STOP. Wait CEO approval.**

---

## STAGE 2: DECODE — Requirements Reconstruction

**COD: Offload** (AI reconstructs requirements) → **Core** (CEO validates D/W classification)

### 2A — Design Intent Decoder (Inverse P&B Task Clarification — HELIX-aligned v2.0)

Reconstruct the Requirements List using **17 Pahl-Beitz requirement categories** (aligned with /helix-p1-requirements). This ensures RE-reconstructed requirements are directly comparable to forward-design requirements and can feed into HELIX pipeline if product transitions to forward development.

**Step 2A-1: Requirements Reconstruction (17 P&B Categories)**

For EACH category, infer requirements from the physical artifact:

```
RECONSTRUCTED REQUIREMENTS LIST — {{product}}
Date: {{today}}  |  Confidence: H=High, M=Medium, L=Low

| Cat# | P&B Category | ID | Requirement | D/W | Evidence in Artifact | Confidence | Source |
|------|-------------|-----|-------------|-----|---------------------|-----------|--------|
| 1 | Geometry | R-001 | {{dimension/shape req}} | D/W | {{physical evidence}} | H/M/L | S1A |
| 2 | Kinematics | R-00x | {{motion/DOF req}} | | | | |
| 3 | Forces | R-00x | {{load/stress req}} | | | | |
| 4 | Energy | R-00x | {{power/efficiency req}} | | | | |
| 5 | Material | R-00x | {{material property req}} | | | | |
| 6 | Signals | R-00x | {{I/O, sensor, control req}} | | | | |
| 7 | Safety | R-00x | {{safety/protection req}} | | | | |
| 8 | Ergonomics | R-00x | {{human factors req}} | | | | |
| 9 | Production | R-00x | {{manufacturing req}} | | | | |
| 10 | Quality | R-00x | {{inspection/tolerance req}} | | | | |
| 11 | Assembly | R-00x | {{assembly/integration req}} | | | | |
| 12 | Transport | R-00x | {{packaging/shipping req}} | | | | |
| 13 | Operation | R-00x | {{use/deployment req}} | | | | |
| 14 | Maintenance | R-00x | {{MRO/serviceability req}} | | | | |
| 15 | Recycling | R-00x | {{disposal/end-of-life req}} | | | | |
| 16 | Cost | R-00x | {{cost target/budget req}} | | | | |
| 17 | Schedule | R-00x | {{timeline/delivery req}} | | | | |

Target: 40-80 requirements (matching HELIX Phase 1 output density)
```

**Step 2A-2: D/W Classification (Core — CEO validates)**

**COD: Core** — D/W classification is NON-DELEGABLE (same as HELIX /helix-p1-validate).

AI proposes D/W based on artifact evidence:
- **D (Demand)**: Feature is structurally critical, safety-related, or functionally essential → evidence: over-designed, redundant, safety-wired
- **W (Wish)**: Feature is nice-to-have, cost-driven, or convenience → evidence: cheaper material, simpler solution would work

```
CEO D/W VALIDATION — {{product}}

| ID | Requirement | AI Proposed D/W | CEO Override | Rationale |
|----|------------|----------------|-------------|-----------|

⚠️ CEO: kiểm tra kỹ D/W classification. Sai D/W ở đây = sai concept selection ở Stage 3.
```

**Step 2A-3: TVDT Generation (Target Values Decision Table)**

Generate TVDT for top 10-15 requirements (aligned with HELIX /helix-p1-abstract output):

```
TARGET VALUES DECISION TABLE — {{product}} (Reconstructed from RE)

| Rank | Req ID | Parameter | Unit | Original Value (inferred) | VN Target | Tolerance | Trade-off Notes | Weight % |
|------|--------|-----------|------|-------------------------|-----------|-----------|----------------|----------|
| 1 | R-{{X}} | {{param}} | {{unit}} | {{from artifact}} | {{VN-adapted}} | ±{{range}} | {{what changes}} | {{%}} |

Notes:
- "Original Value" = best estimate from artifact analysis (with confidence H/M/L)
- "VN Target" = realistic target given VN manufacturing + supply chain
- Trade-offs documented for CEO decision in Stage 3
- TVDT feeds directly into VDI 2225 evaluation criteria (Stage 3C)
```

**Step 2A-4: RED FLAGS**

```
RED FLAGS:
- Over-designed features → reliability/safety critical (keep as D)
- Under-designed features → cost-driven compromise or known limitation (may upgrade for VN)
- Unusual choices → patent avoidance or specific operational requirement (investigate)
- Missing categories → artifact may not address (transport, recycling often absent in defense)
- Categories with 0 requirements → either truly N/A or RE missed evidence (flag for CEO)
```

**Requirements Confidence Matrix:** High (must keep in redesign) vs Low (re-evaluate in Stage 3)

**Output:** Save to `RE_{{product}}_S2A_Requirements.md` + `RE_{{product}}_S2A_TVDT.md`

### 2B — Functional Abstraction Engine (6-flow + Solution-Determining SF — HELIX-aligned v2.0)

VDI 2221 inverse: artifact → function structure. Now uses **6-flow** (aligned with /helix-p1-structure and /helix-6flow-mapper) and identifies **solution-determining sub-function** (aligned with /helix-p2-frame).

**Step 1:** Black Box — **6-flow** (E-M-S + Data-Compute-Trust)

```
REVERSE BLACK BOX — {{product}}

Classical 3-flow (from artifact):
  E-IN: {{energy inputs}} → E-OUT: {{energy outputs + losses}}
  M-IN: {{material inputs}} → M-OUT: {{material outputs + waste}}
  S-IN: {{signal inputs}} → S-OUT: {{signal outputs}}

Extended 3-flow (reconstructed from behavior):
  D-IN: {{data inputs}} → D-OUT: {{data outputs, logs, telemetry}}
  C-IN: {{computation triggers}} → C-OUT: {{decisions, control outputs}}
  T-IN: {{trust inputs: auth, safety, integrity}} → T-OUT: {{trust assurances: encryption, heartbeat, fallback}}

System boundary: {{context diagram}}
Operational states: {{Off/Standby/Init/Normal/Emergency/Maintenance/Shutdown}}
```

**Step 2:** White Box decomposition — verb-noun sub-functions + quantified I/O per 6-flow
**Step 3:** Function structure diagram — hierarchy + 6-flow connections
**Step 4:** Solution-neutral reformulation — **CRITICAL FOR IP-FREE RE**
  - BAD: "Convert 24VDC to motion using BLDC + planetary gearbox"
  - GOOD: "Convert electrical energy to rotational motion with specified torque/speed"
  - This enables IP-free alternative exploration in Stage 3
  - **Test:** Can the function statement be satisfied by ≥3 different physical principles?

**Step 5:** Function-Component Matrix (extended)
```
| Sub-Function | Original Component | 6-Flow | Criticality | VN Alternatives | ACH Candidate? |
|-------------|-------------------|--------|-------------|----------------|---------------|
| SF-001 {{verb-noun}} | {{component}} | E/M/S/D/C/T | H/M/L | {{list}} | Y/N |
```

**Step 6:** Hidden functions detection — safety, reliability, manufacturing, legacy, diagnostic functions

**Step 6.5: Domain-Perspective Function Allocation** (Multi-Perspective v2.0)

> **Trigger:** RE Complexity AMBER/RED (from Step 8 preview or prior knowledge). Skip for GREEN.
> **Source:** Multi-Agent Selectivity Law — domain debate only for coupled products.

Run `/helix-domain-debate` with question: "How should the functions from Steps 2-6 be allocated across Mech/Elec/AI-SW domains? What functions does YOUR domain claim, and what allocation choices by the competitor surprise you?"

```
DOMAIN-PERSPECTIVE ALLOCATION — RE {{product}}

From JSON side-car (```json:domain-debate-sidecar):
  → perspectives[].preferred_approach → domain-claimed functions
  → contradictions[] → allocation disagreements (= integration complexity)
  → synthesis.recommendation → proposed WX allocation

ALLOCATION COMPARISON:
| SF | Competitor Allocation | MECH Claims | ELEC Claims | AI_SW Claims | Conflict? |
|----|----------------------|-------------|-------------|-------------|-----------|
| SF-001 | Mech 80%, Elec 20% | {{agree/claim more}} | {{agree/claim more}} | {{not involved}} | Y/N |

INSIGHTS FOR STEP 7:
- SFs where domains disagree on allocation → HIGH coupling → likely solution-determining
- SFs where competitor allocated differently than WX would → redesign opportunity
- SFs with 3-domain claims → integration-intensive → architect carefully
```

**Rules:**
- 15 minutes max — allocation debate, not deep analysis (2M does that for MECHA)
- Output appends to `RE_{{product}}_S2B_Function_Structure.md`
- Allocation conflicts feed directly into Step 7 (solution-determining SF)
- If 2M (MECHA mode) is active, Step 6.5 replaces 2M-1 (Cross-Domain Function Allocator) with multi-perspective version

**Step 7: Solution-Determining Sub-Function Identification** (NEW — aligned with /helix-p2-frame)

```
SOLUTION-DETERMINING SF ANALYSIS — {{product}}

Candidate SFs for solution-determining role:
| SF | Why Solution-Determining? | If Changed, What Cascades? | WX Capability |
|-----|--------------------------|---------------------------|-------------|
| SF-{{X}} | {{rationale}} | {{cascade list}} | H/M/L |

SELECTED SOLUTION-DETERMINING SF: SF-{{X}} — {{name}}
  Rationale: {{why this SF drives the architecture}}
  Stage 3 implication: redesign effort concentrates HERE
  Other SFs: adapt around this SF's solution choice

⚠️ P&B principle: "Giải pháp cho SF quyết định → cascade toàn bộ thiết kế"
   (Galaxy: Solution-Determining SF Law)
```

**Step 8: RE Complexity Classification** (NEW — like HELIX design type)

```
RE COMPLEXITY CLASSIFICATION — {{product}}

Per-SF assessment:
| SF | WX Prior Art | Complexity | Depth in Stage 3 |
|----|-------------|-----------|-----------------|
| SF-001 | Yes (from {{product}}) | GREEN | SHALLOW (catalogue) |
| SF-002 | Partial | AMBER | MODERATE |
| SF-003 | No precedent | RED | DEEP (all methods) |

OVERALL RE COMPLEXITY: GREEN / AMBER / RED
  - GREEN SFs: {{N}} ({{%}}) → reuse WX pattern library
  - AMBER SFs: {{N}} ({{%}}) → selective external learning
  - RED SFs: {{N}} ({{%}}) → full morphological search required

Stage 3 TIME BUDGET calibration:
  GREEN: 30-40% time budget (most WX knowledge reusable)
  AMBER: 60-70% time budget (novel subsystems only deep)
  RED: 100% time budget (new product class, deep everywhere)
```

**Output:** Save to `RE_{{product}}_S2B_Function_Structure.md` + `RE_{{product}}_S2B_Solution_Det_SF.md` + `RE_{{product}}_S2B_Design_Type.md`

### 2M — Cross-Domain Analysis (MECHA mode only)

**2M-1: Cross-Domain Function Allocator** (Multi-Perspective v2.0)

If Step 6.5 ran (AMBER/RED): use its domain debate results as input. Extend with driver analysis and alternative exploration below.
If Step 6.5 skipped (GREEN): run the single-agent table below.

| Function | Mech % | Elec % | Sw % | Ctrl % | Rationale | Domain Debate? |

Allocation driver analysis:
- Technology drivers (era of design, cost/perf at that time)
- Physical drivers (weight, power, thermal, vibration)
- Strategic drivers (export control, supplier availability)
- Operational drivers (maintenance philosophy, repair capability)

Alternative allocation exploration (informed by Step 6.5 domain claims if available):
| Strategy | Distribution | Advantages | Disadvantages | Vietnam Fit |
- Software-centric / Electronics-centric / Mechanical-centric / Distributed

**2M-2: Control Law Reverser**

System identification approach:
- Step response → time constants, damping, overshoot
- Frequency sweep → Bode plot, bandwidth, resonances
- PRBS → MIMO system identification
- Black box model fitting (1st/2nd order, delay, state-space)
- PID parameter extraction (Kp, Ki, Kd, filter, anti-windup)
- State machine reverse (states, transitions, timing)
- Safety/protection logic (over-current, link loss, geofencing, flight termination)

Control architecture documentation:
- Inner loops (1-10 kHz) → middle (100-500 Hz) → outer (10-100 Hz) → supervisory
- Sample rates, latency budgets, saturation limits, sensor bandwidth

**2M-3: Firmware & Software Archaeology**

Multi-layer approach (safest → deepest):
- L1: External observation (boot time, response latency, failure modes) — always legal
- L2: Interface analysis (protocol reverse, data format, command mapping)
- L3: Memory analysis (if JTAG accessible and legal)
- L4: Binary analysis (behavior understanding only, NOT code reproduction)

Software architecture hypothesis:
1. Bare Metal (fast boot, deterministic, simple)
2. RTOS (FreeRTOS, ThreadX, VxWorks — concurrent, preemptive)
3. Linux/Embedded Linux (longer boot, network stack)
4. Hybrid (Linux + RTOS on separate cores)

Algorithm inventory:
| Category | Likely Implementation | Evidence | Reconstruction Feasibility |
(Sensor fusion, navigation, control, signal processing, encryption, image processing)

Redevelopment strategy:
- Option A: Full independent development (clean IP, slow)
- Option B: Open-source adaptation (ArduPilot/PX4, ROS, NuttX/Zephyr)
- Option C: COTS commercial (licensed, supported)
- Option D: Hybrid (most common in practice)

**NLM deep query (if notebook active):**
```bash
nlm notebook query re-{{short}} "From the technical documentation: (1) What are the inferred functional requirements? (2) What design intent is hidden behind the observed features? (3) What performance parameters can be reverse-calculated? (4) What are the likely failure modes based on design choices? (5) What standards compliance is evidenced? (6) What material/process selections suggest about the operational environment?"
```

**NLM contradiction query (if notebook has ≥3 sources from different OEMs/origins):**
```bash
nlm notebook query re-{{short}} "Compare sources from different manufacturers/origins
and identify contradictions relevant to reverse engineering:
(1) Where do specs from different OEMs contradict each other for similar components?
    (These contradictions reveal design trade-off decisions — critical for RE.)
(2) What assumptions do all sources share but never test?
    (Shared blind spots = risk for VN adaptation.)
(3) Where do sources disagree on methodology (testing, qualification, manufacturing)?
    (Methodology gaps = validation risk for Workshop X.)
For each finding: state positions, name sources, explain WHY they differ,
rate impact on VN redesign: HIGH / MEDIUM / LOW."
```
This query is especially valuable when RE compares competing products (COMPARE mode) or when multiple OEM datasheets describe similar subsystems differently — contradictions reveal hidden design trade-offs that pure spec-reading misses.

**Output:**

```
=== STAGE 2 COMPLETE — {{product}} REQUIREMENTS RECONSTRUCTED ===

Requirements reconstructed: {{N}} across 17 P&B categories ({{D_count}} Demand, {{W_count}} Wish)
  - Categories with reqs: {{N}}/17
  - Categories empty: {{list}} — investigate or confirm N/A
High confidence: {{N}} | Medium: {{N}} | Low: {{N}}
TVDT generated: top {{N}} parameters with VN targets

Sub-functions (6-flow): {{N}} total
  - E-M-S flows: {{N}} | D-C-T flows: {{N}}
Solution-determining SF: SF-{{X}} — {{name}}
RE Complexity: GREEN / AMBER / RED ({{N}}% GREEN, {{N}}% AMBER, {{N}}% RED)

[MECHA] Cross-domain: Mech({{N}}) / Elec({{N}}) / Sw({{N}}) / Ctrl({{N}})
[MECHA] Control loops: {{N}} | State machine states: {{N}}
[MECHA] SW architecture hypothesis: {{type}}

Solution-neutral functions ready for morphological matrix: {{N}}

DELIVERABLES PRODUCED:
1. RE_{{product}}_S2A_Requirements.md — 17-category req list with D/W
2. RE_{{product}}_S2A_TVDT.md — Target Values Decision Table
3. RE_{{product}}_S2B_Function_Structure.md — 6-flow structure
4. RE_{{product}}_S2B_Solution_Det_SF.md — Solution-determining SF
5. RE_{{product}}_S2B_Design_Type.md — RE complexity classification
[MECHA] 6. RE_{{product}}_S2M_Cross_Domain.md — 4-domain decomposition

CEO ACTIONS REQUIRED (Core — non-delegable):
1. ✅ Validate D/W classification — sai D/W = sai concept selection
2. ✅ Confirm TVDT target values — VN targets realistic?
3. ✅ Approve solution-determining SF selection
4. ✅ Validate RE complexity classification
5. 🔍 Flag any requirements from operational knowledge not captured
6. ⚠️ Note: Requirements Delta Log will track Stage 2↔3 co-evolution

CEO: approve Stage 2 outputs to proceed to Stage 3?
```

**STOP. Wait CEO approval.**

---

## REQUIREMENTS DELTA LOG — Stage 2↔3 Co-evolution (VDI 2221:2019)

**Principle:** Requirements reconstructed in Stage 2 will evolve when Stage 3 redesign reveals VN constraints. This is NORMAL in systematic design (VDI 2221:2019 "Yellow Strand"). Track all changes to prevent silent requirement drift.

```
REQUIREMENTS DELTA LOG — RE: {{product}}

| Delta-ID | Req-ID | Change Type | Stage 2 Value | Stage 3 Modified | Reason | CEO Approved | Propagate? |
|----------|--------|------------|---------------|-----------------|--------|-------------|-----------|
| D-001 | R-{{X}} | VALUE CHANGE | {{original}} | {{new}} | VN material limitation | YES/NO/PENDING | S2A req list |
| D-002 | R-{{X}} | NEW REQ | — | {{new req}} | VN regulatory (QPAN) | | S2A req list |
| D-003 | R-{{X}} | REMOVED | {{original}} | — | Not feasible in VN | | S2A req list |
| D-004 | R-{{X}} | D→W | Demand | Wish | Cost-driven relaxation | | S2A D/W table |

RULES:
- First delta → CREATE this log immediately (do not wait until Stage 3 complete)
- Every delta requires CEO APPROVE/REJECT (Core — non-delegable)
- ACCEPT → propagate to S2A_Requirements.md (creates version v1.1, v1.2, etc.)
- REJECT → document rationale, may require design rework in Stage 3
- DEFER → flag as [TBD], track in Stage 4 validation

⚠️ FLAG at Stage 3 CEO checkpoint:
"Requirements backflow: {{N}} requirements modified since Stage 2"
```

Save to: `RE_{{product}}_Requirements_Delta_Log.md`

---

## STAGE 3: RECONSTRUCT — P&B Forward Redesign

**COD: Core** (design decisions) with **Offload** (alternative generation)

**Input validation:** Read `RE_{{product}}_S2A_Requirements.md` + `RE_{{product}}_S2A_TVDT.md` + `RE_{{product}}_S2B_Function_Structure.md` + `RE_{{product}}_S2B_Solution_Det_SF.md` + `RE_{{product}}_S2B_Design_Type.md`. If any missing → report which Stage 2 sub-step to run first.

**RE Complexity calibration:** Read `S2B_Design_Type.md` → calibrate Stage 3 depth:
- GREEN SFs → SHALLOW search (WX pattern library + catalogue only)
- AMBER SFs → MODERATE search (catalogue + limited external)
- RED SFs → DEEP search (all morphological methods, /wp integration)

### 3A — Modified Task Clarification

Updated Requirements List with VN modifications:
| ID | Requirement | Original | Modified for VN | Rationale |

Modification drivers:
- Vietnam operational environment (tropical, coastal, seismic)
- Vietnam manufacturing capability constraints
- ITAR-free component sourcing
- Domestic MRO capability requirements
- Cost optimization for domestic budget
- Standardization with existing VN military inventory

### 3B — Conceptual Alternatives

Morphological matrix with IP-free alternatives:
| Function | Original Solution | Alt 1 (VN-optimized) | Alt 2 (Cost-optimized) | Alt 3 (Capability-extended) |

Criteria for alternatives:
- Patent/IP-free implementations
- Domestic supply chain solutions
- Performance equivalent or better
- Manufacturing capability fit

### 3C — VDI 2225 Concept Selection (Defense RE Weights)

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Technical performance | 35% | Function fulfillment, reliability, margins |
| Manufacturability | 25% | VN capability, tooling, workforce skills |
| Sovereignty | 20% | ITAR-free, domestic %, supply chain resilience |
| Cost | 10% | Unit cost, lifecycle cost, tooling investment |
| Time-to-deploy | 10% | Development time, qualification time |

Generate weighted scoring matrix + sensitivity analysis.

### 3D — Divergence Map

| Category | Features | Rationale |
|----------|----------|-----------|
| **Kept** from original | {{list}} | Why retained |
| **Modified** | {{list}} | How + why changed |
| **Added** | {{list}} | What + why new |
| **Removed** | {{list}} | What + why dropped |

Critical for: IP defense, configuration management, backward compatibility.

**Output:**

```
=== STAGE 3 COMPLETE — {{product}} REDESIGN CONCEPT ===

Concept variants generated: {{N}}
VDI 2225 winner: Concept {{X}} (score: {{S}}/4.0)
Sensitivity: {{robust/sensitive to criterion Y}}
Domestic content: {{X}}%
IP-free components: {{X}}/{{total}}
Key divergences from original: {{N}}

CEO DECISION REQUIRED (Core — non-delegable):
Select concept for embodiment → connects to /helix-embody-realize

CEO: select concept to proceed to Stage 4?
```

**STOP. Wait CEO concept selection.**

---

## STAGE 3P: PARTNERSHIP — Acquisition & Adaptation Strategy (v2.0)

**COD: Core** — Strategic partnership decisions are non-delegable.

Can run standalone (`--mode partner`) or as part of FULL/MECH/MECHA pipeline after Stage 3.

### 3P-A: Acquisition Structure Options

Evaluate 4 acquisition models for the selected product:

| Option | Description | Timeline | VN Content | Cost |
|--------|------------|----------|-----------|------|
| **1. Direct Purchase** | Buy off-the-shelf | 1-2 yr | 0% | Lowest upfront |
| **2. Assembly License** | Import components, assemble in VN | 3-5 yr | 30-60% | Moderate |
| **3. Co-Development** | Joint development of VN variant | 5-7 yr | 60-80% | Higher |
| **4. Technology Transfer** | Full license to produce in VN | 7-10 yr | 80-95% | Highest upfront, lowest long-term |

**Recommendation framework:** Option 1→2 (near-term capability), progressing to 3→4 (long-term sovereignty).

### 3P-B: Technology Transfer Priority Matrix

| Tier | What to Transfer | Strategic Value |
|------|-----------------|----------------|
| **1 MUST** | Flight control SW (source code), mission planning, control laws, test procedures, maintenance | Operational sovereignty |
| **2 SHOULD** | Airframe design methodology, composite manufacturing, electronic integration, QC procedures | Capability building |
| **3 NICE** | Propulsion technology, advanced materials, specialized sensors | Deep independence |
| **4 UNLIKELY** | Proprietary algorithms, classified signature data, latest-gen advances | Accept gap |

### 3P-C: Vietnam Adaptation Roadmap

**Environmental adaptations:**
- Tropical humidity protection (conformal coating, hermetic sealing, desiccants)
- Salt spray resistance (5000-series aluminum, cathodic protection, marine coatings)
- UV-resistant materials
- High-temperature reliability focus (relax cold-weather specs)

**Sovereignty adaptations:**
- GNSS receiver: BeiDou/GLONASS/GPS multi-constellation (reduce Western dependency)
- Datalink: Vietnamese indigenous or trusted-source encryption
- Flight control: domestic processor, Vietnamese-developed software
- Software: full rewrite from requirements (IP-safe, ArduPilot/PX4 base possible)

**Manufacturing capability roadmap:**
| Year | Capability Level | VN Content | Investment |
|------|-----------------|-----------|------------|
| 1-2 | Field support + maintenance | 10% | $5-10M |
| 3-4 | Assembly + sub-system integration | 30-50% | $20-30M |
| 5-7 | Component manufacturing + test | 60-80% | $30-50M |
| 8-10 | Full production + VN variant development | 80-95% | $10-20M |

**Workshop X role:** Support → Assembly → Partial production → Full production → Export

### 3P-D: Negotiation Framework

**Supplier motivation analysis:**
- What does supplier WANT from VN deal? (market entry, reference customer, revenue, strategic alignment)
- What pressure points? (export targets, domestic competition, currency, political)
- What will they concede? (pricing, TT, customization, training, support)
- What will they resist? (source code, unlimited export rights, future maintenance revenue loss)

**Vietnam leverage:**
- Multiple qualified suppliers available
- Large ASEAN market gateway
- Strategic geographic position
- Government-backed procurement with long-term commitment potential

**Negotiation tactics awareness:**
- "Bait and switch" → lock key terms early
- "Sole source" claims → maintain visible alternatives
- "Future generation" promises → contract for current capability only
- "Package deal" pressure → require itemized pricing
- "Limited time" → calm, patient approach

**Contract architecture (phased):**
- Phase 1: Initial procurement (specific units, price, delivery, warranty)
- Phase 2: Technology transfer (optional, success-gated, milestone payments)
- Phase 3: Production partnership (optional, shared IP, VN production)
- Phase 4: Strategic partnership (optional, R&D, export, next-gen)

### 3P-E: Decision Gate Structure

| Gate | Decision | Criteria | Timeline |
|------|----------|---------|----------|
| G1 Technical | Which suppliers technically acceptable? | Meet minimum VN requirements | Month 1-6 |
| G2 Strategic | Which align with VN long-term strategy? | Geopolitical + industrial fit | Month 3-6 |
| G3 Competitive | Best value proposition? | RFP evaluation + BAFO | Month 6-15 |
| G4 Negotiation | Acceptable terms secured? | Contract validation | Month 12-18 |
| G5 Implementation | Performing as expected? | First deliveries + IOC | Year 2-3 |
| G6 Expansion | Should partnership expand? | TT success + broader opportunity | Year 5-7 |

**Output:**

```
=== STAGE 3P COMPLETE — {{product}} PARTNERSHIP STRATEGY ===

Recommended acquisition model: Option {{N}} → progressing to Option {{M}}
TT priority: Tier 1 ({{N}} items), Tier 2 ({{N}} items)
VN adaptation areas: {{N}} environmental, {{N}} sovereignty, {{N}} manufacturing
Workshop X investment required: ${{range}} over {{N}} years
Negotiation approach: {{summary}}
Decision gates: 6 gates over {{N}} years

CEO DECISION (Core): Approve partnership strategy to proceed to Stage 4?
Save to: 1_Projects/{{project}}/Ref/PARTNERSHIP_{{product}}_{{date}}.md
```

**STOP. Wait CEO approval.**

---

## STAGE 4: DEPLOY — Validation & Audit

**COD: Core** (go/no-go) with **Offload** (test plan generation, audit execution)

### 4A — V&V Strategy

4-level test hierarchy:

**Level 1 — Component Testing:**
| Component | Original Spec | Redesign Spec | Test Method | Acceptance Criteria | MIL-STD Ref |

**Level 2 — Subsystem Testing:**
- Load (static, dynamic, fatigue)
- Environmental (MIL-STD-810G: temp, humidity, vibration, shock, salt fog)
- EMC (MIL-STD-461G) if electronic
- Reliability (MTBF verification)

**Level 3 — System Integration:**
- End-to-end function verification
- Interface compatibility with existing systems
- Side-by-side comparison with original (if available)

**Level 4 — Field Validation:**
- Trial unit deployment
- User feedback protocol
- MTBF/MTTR verification in field

**Defense Acceptance Testing (Vietnam):**
1. Thu nghiem xuat xuong (factory acceptance)
2. Thu nghiem nghiem thu cap Bo (ministry acceptance)
3. Thu nghiem chien dau / su dung (operational trials)

### 4B — Adversarial RE Audit (8 Challenges)

Red team audit — find flaws BEFORE field discovers them:

| # | Challenge | Focus |
|---|-----------|-------|
| 1 | Requirements Completeness | Missing/implicit/environmental/interface/lifecycle reqs |
| 2 | Function Structure | Redundant/missing functions, edge cases, failure modes |
| 3 | Design Decisions | Evidence, alternatives, biases (anchoring, availability, sunk cost, confirmation) |
| 4 | Manufacturability | VN workforce capability, training, tooling, yield, supplier failure |
| 5 | Operational | Field usability, maintenance complexity, logistics tail, equipment compatibility |
| 6 | Adversary | Vulnerability points, countermeasures, degradation in contested environment |
| 7 | Regulatory | MIL-STD coverage, STANAG compliance, VN regulatory, export control |
| 8 | Strategic | Technology sovereignty contribution, opportunity cost, obsolescence timeline |

**Severity levels:**
- CRITICAL: Must fix before production (show-stopper)
- HIGH: Must fix before field deployment
- MEDIUM: Should fix, manage risk
- LOW: Future improvement

### 4M — Integration Challenges (MECHA mode only)

7-category integration risk analysis:
1. Timing & latency risks (sensor→processor→actuator chain)
2. Resource contention (CPU, memory, bus, power, thermal budgets)
3. EMC risks (motor drives, switching PSU, RF, ground loops — MIL-STD-461G)
4. Thermal risks (hotspots, cooling path disruption, cycling fatigue)
5. Mechanical tolerance stack-up (optical alignment, PCB mounting, antenna position)
6. Software-hardware coupling (ADC resolution, motor parameters, sensor noise assumptions)
7. Control stability (new dynamics → retune PID/Kalman/notch filters)

Integration test strategy (bottom-up):
1. Component qualification → 2. Domain integration → 3. Two-domain → 4. Three-domain → 5. Full system → 6. Environmental → 7. Mission

V-Model right-side V&V:
- Unit/component verification (bench, HIL, SIL)
- Domain integration (CMM, functional, EMC pre-compliance, code coverage)
- Cross-domain integration (vibration survival, register access, algorithm verification)
- System-level verification (analysis, inspection, demonstration, test per IEEE 1012)
- System validation (side-by-side, benchmarking, user acceptance)
- Environmental qualification (MIL-STD-810G: 501-520)
- EMC qualification (MIL-STD-461G: CE/CS/RE/RS)
- Reliability testing (HALT, HASS, life cycle, duty cycle)

**Vietnam test facility considerations:**
- Vien Cong nghe va Chien luoc Bien (naval)
- Vien Ky thuat Khong quan (aerial)
- Vien KHCN Quan su (general defense)
- Gap analysis: domestic vs abroad testing capability

**Output:**

```
=== STAGE 4 COMPLETE — {{product}} VALIDATION & AUDIT ===

V&V PLAN:
- Component tests: {{N}} | Subsystem tests: {{N}} | System tests: {{N}}
- Environmental tests: {{MIL-STD-810G methods}}
- [MECHA] EMC tests: {{MIL-STD-461G requirements}}
- Estimated V&V duration: {{N}} weeks
- Estimated V&V cost: {{range}}

AUDIT FINDINGS:
| Severity | Count |
|----------|-------|
| CRITICAL | {{N}} |
| HIGH     | {{N}} |
| MEDIUM   | {{N}} |
| LOW      | {{N}} |

GO/NO-GO: {{recommendation}}
Top blockers: {{list}}
Overall readiness: {{score}}/10

CEO DECISION (Core): Go / Conditional Go / No-Go for production?
```

**STOP. Wait CEO decision.**

---

## STAGE 5: KNOWLEDGE CAPTURE — Compound Learning

**COD: Offload** (AI compiles) → **Core** (CEO validates Galaxy candidates)

### 5A — RE Technical Dossier

Structured document:
1. Executive Summary (1 page)
2. Original Product Analysis
3. Requirements Reconstruction
4. Function Structure Analysis
5. Material & Process Analysis
6. Tolerance & Performance Analysis
7. IP & Legal Analysis
8. Redesign Rationale
9. Validation Results
10. Lessons Learned

Save to: `1_Projects/{{project}}/Ref/RE_DOSSIER_{{product}}_{{date}}.md`

### 5B — Design Pattern Library + Heuristics

**Reusable patterns:**
| Pattern Name | Context | Problem | Solution | Consequences | Source Product |

Defense patterns to capture:
- Shock mounting (naval)
- Tropical humidity sealing
- Desert thermal management
- EMI shielding
- Corrosion protection (coastal)

**Heuristics database:**
| Heuristic | Domain | Evidence | Confidence | Constraints |

Save to: `3_Resources/Technical-References/RE-Patterns/{{product}}_patterns.md`

### 5C — Galaxy Candidates

Apply Three Laws extraction to RE learnings:

```
## Ba Quy Luat — RE: {{product}}

### Quy Luat 1: {{Ten}} Law
{{...}}

### Quy Luat 2: {{Ten}} Law
{{...}}

### Quy Luat 3: {{Ten}} Law
{{...}}
```

Galaxy quality gate (3-question check):
1. Thay doi cach thiet ke?
2. Thay doi quyet dinh chien luoc?
3. Canh bao tranh trap nao?

**PROPOSE Galaxy notes — do NOT create without CEO approval.**

### 5D — Supplier Capability Map Update

Vietnam ecosystem documentation:
| Capability | Suppliers | Capacity | Quality Level | Strategic Rating |

Update: `2_Areas/FORGE/Product-Portfolio/VN_Supplier_Capability.md`

### 5E — Capability Building Map

| RE Project | Capabilities Gained | Sovereignty Contribution | Next Logical RE Target |

**Output:**

```
=== STAGE 5 COMPLETE — {{product}} KNOWLEDGE CAPTURED ===

RE Dossier: {{path}}
Design patterns extracted: {{N}}
Heuristics captured: {{N}}
Galaxy candidates: {{N}} (pending CEO review)
Three Laws: {{names}}
Supplier map updates: {{N}} entries
Capability sovereignty delta: +{{N}}% domestic content gained

COMPOUND ENGINEERING VALUE:
- Patterns reusable for: {{product list}}
- Heuristics applicable to: {{domain list}}
- Next recommended RE target: {{product}}

SESSION COMPLETE.
```

---

## RE MATURITY ASSESSMENT (use for gate checks)

8-dimension scoring (use with `--stage check`):

| Dimension | Weight | Score (1-10) |
|-----------|--------|-------------|
| Understanding Depth (L1-L5) | 20% | |
| Documentation Completeness | 10% | |
| Model Fidelity (F1-F5) | 10% | |
| Verification Coverage | 20% | |
| Risk Assessment | 15% | |
| Production Readiness | 10% | |
| Sovereignty Score | 10% | |
| Lifecycle Readiness | 5% | |

**Understanding levels:**
- L1 Surface: know what it does
- L2 Structural: know what's inside
- L3 Functional: know how it works
- L4 Causal: know WHY it's designed this way
- L5 Generative: could design equivalent from scratch

**Target: L4-L5 before production commit.**

**Go threshold:** >80 total, no dimension <70
**Conditional:** 70-80 with mitigation plan
**No-go:** <70 → more RE work needed

**Red team questions (final gate):**
1. "If original developer walked in, would they recognize this as equivalent?"
2. "If asked to design from scratch tomorrow, could I?"
3. "What's my biggest remaining uncertainty?"
4. "If this fails in field, WHERE will it fail?"
5. "Am I fooling myself about any aspect?"

---

## NLM INTEGRATION

### Notebook naming convention
```bash
nlm notebook create "RE: {{product_name}}"
nlm alias set re-{{short}} {{uuid}}
```

### Standard NLM queries per stage

**Stage 1 (Deconstruct):**
```
"From the technical documentation, identify: (1) All material specifications mentioned, (2) Manufacturing processes described or implied, (3) Critical dimensions and tolerances, (4) Environmental operating conditions, (5) Any design rationale or justification statements."
```

**Stage 2 (Decode):**
```
"Reconstruct the design requirements: (1) What functional requirements does this product satisfy? (2) What performance parameters are specified or implied? (3) What constraints (environmental, interface, regulatory) are documented? (4) What failure modes are addressed by the design? (5) What standards compliance is claimed or implied? (6) What is the intended operational lifecycle?"
```

**Stage 3 (Reconstruct):**
```
"For redesign planning: (1) What are alternative solutions for each critical function? (2) What are the known weaknesses or limitations? (3) What improvements have been suggested in literature? (4) What are the manufacturing alternatives available? (5) What modern components could replace legacy parts?"
```

**Stage 4 (Deploy):**
```
"For validation: (1) What test methods are specified in referenced standards? (2) What acceptance criteria are documented? (3) What qualification testing is required? (4) What field performance data is available? (5) What known failure modes must be tested for?"
```

---

## NLM KNOWLEDGE BASE SETUP (auto-generate reports + quiz + persona)

When NLM notebook is created for an RE project, auto-generate a complete knowledge base of reports that CEO can reference later in NLM chat. Run this ONCE after Stage 1 source ingestion is confirmed (Step 4G passed).

### Step KB-1: Verify Notebook Ready

KB Setup runs AFTER Stage 1 NLM integration is complete (NLM-1 through NLM-4 passed). Do NOT re-add sources — they were already ingested and quality-gated in Stage 1.

```bash
# Verify notebook exists and has sources
nlm source list re-{{short}}
# Should show all CEO-approved sources from Stage 1 NLM-4
```

If notebook does not exist yet (CEO skipped NLM in Stage 1):
→ Run full NLM-1 through NLM-4 protocol from Stage 1 (CEO source selection → add → quality gate → CEO confirm)

### Step KB-2: Set Chat Persona (auto-configured via MCP)

Use `mcp__notebooklm-mcp__chat_configure` to set persona automatically — no manual paste needed. Select persona based on RE mode:

```
# For MECH mode:
chat_configure(
  notebook_id={{uuid}},
  goal="custom",
  response_length="longer",
  custom_prompt="PERSONA — RE MECHANICAL LEAD FOR WORKSHOP X

You are a Senior Reverse Engineering Lead at Workshop X, a Vietnam defense manufacturer with 1,064+ hardware units shipped. You specialize in deconstructing foreign military products for domestic localization. Your expertise covers:
- Material science (metals, polymers, composites — Vietnam manufacturing capability)
- Manufacturing process inference (casting, machining, welding, heat treatment)
- Tolerance analysis and GD&T reverse engineering
- Pahl-Beitz systematic design (VDI 2221) applied to redesign
- MIL-STD compliance (810G environmental, 461G EMC, 1521 reviews)
- Vietnam defense regulations (Luat Cong nghiep Quoc phong 2024)
- ITAR-free component sourcing and supply chain sovereignty

RULES:
- Always cite specific sources from uploaded documents
- Flag confidence level (High/Medium/Low) for every inference
- Always include Vietnam Manufacturing Capability assessment for materials/processes
- When discussing redesign, always propose ITAR-free alternatives
- Flag potential IP/patent concerns proactively
- Use metric units exclusively
- When unsure, say Low confidence — needs physical verification
- Always consider tropical maritime environment (humidity, salt fog, temperature)"
)

# For MECHA mode:
chat_configure(
  notebook_id={{uuid}},
  goal="custom",
  response_length="longer",
  custom_prompt="PERSONA — RE MECHATRONIC SYSTEMS ENGINEER FOR WORKSHOP X

You are a Systems Engineer specializing in mechatronic product reverse engineering using VDI 2206 V-Model methodology at Workshop X (1,064+ units shipped). Your expertise spans 4 domains: Mechanical (structures, kinematics), Electronic (PCB, sensors, actuators), Software (embedded firmware, RTOS, algorithms), and Control (PID, Kalman, state machines). You reverse-engineer foreign products for sovereign localization in Vietnam.

RULES:
- Always decompose analysis into 4 domains (Mech/Elec/Sw/Ctrl)
- Flag cross-domain dependencies and integration risks
- For control systems: specify sample rates, latency budgets, stability margins
- For software: recommend open-source alternatives (ArduPilot, PX4, FreeRTOS, Zephyr)
- For electronics: identify component part numbers when visible, suggest ITAR-free substitutes
- Always cite confidence levels and flag items needing physical testing
- Use VDI 2206 V-Model terminology consistently
- Always consider Vietnam manufacturing context (tropical, domestic sourcing, conscript maintenance)"
)
```

### Step KB-3: Generate Reports (batch — run all queries sequentially)

**CEO gate:** "Tạo bộ reports RE trong NLM? Mất ~10-15 phút, 10-20 queries." — CEO approves before running.

After CEO approval, run these queries and save each as an NLM note:

#### Reports cho MECH mode (10 reports):

```bash
# Report 1: Artifact Deconstruction
nlm notebook query re-{{short}} "Act as RE Lead. Perform 4-layer artifact deconstruction from all uploaded sources: Layer 1 (Geometric & Dimensional): envelope, critical dimensions, GD&T, surface finish, non-obvious features. Layer 2 (Material & Process): material candidates with confidence %, manufacturing evidence, surface treatment, joining methods. Layer 3 (Functional Decomposition): component inventory, power/signal flow, kinematic chains, interfaces. Layer 4 (Hidden Design Intent): why this geometry, implied safety factors, manufacturing era, environment clues. Output as structured tables with confidence levels (H/M/L)."

# Report 2: Design Intent Decoder
nlm notebook query re-{{short}} "Perform inverse Pahl-Beitz Task Clarification. From all sources, reconstruct 3 requirements tables: Table A Functional Requirements (satisfied by artifact): ID, Requirement, D/W, Evidence, Confidence. Table B Performance Requirements (inferred): ID, Parameter, Estimated Value, Inference Method, Verification Needed. Table C Constraints (environment/interface/regulatory): ID, Type, Description, Evidence, Impact. Flag: over-designed features (reliability critical), under-designed (cost compromise), unusual choices (patent avoidance?). End with Requirements Confidence Matrix."

# Report 3: IP & Legal Navigator
nlm notebook query re-{{short}} "Act as IP/Legal advisor for RE in Vietnam context. Analyze: (A) IP Landscape — relevant patents, trade secrets, patent expiration. (B) Export Control — ITAR categories, EAR/ECCN, Wassenaar. (C) Vietnam Legal — Luat CNQP 2024, Law 32/2021, IP Law 2022. (D) RE Legality — clean-room vs contaminated, documentation requirements. (E) Safer Path — low-risk areas, design-around strategies. Output: RE Risk Assessment Matrix with go/no-go recommendation per component."

# Report 4: Functional Abstraction Engine
nlm notebook query re-{{short}} "Convert physical artifact to abstract function structure per VDI 2221: Step 1 Black Box (3 flows: Energy, Material, Signal). Step 2 White Box decomposition (verb-noun sub-functions). Step 3 Function structure diagram (hierarchy + connections). Step 4 CRITICAL — Solution-neutral reformulation (separate function from specific implementation to enable IP-free redesign). Step 5 Function-Component Matrix. Step 6 Hidden functions detection (safety, reliability, manufacturing, legacy). Output complete function structure ready for conceptual redesign."

# Report 5: Material & Process Detective
nlm notebook query re-{{short}} "Act as Material Scientist + Manufacturing Engineer. From all sources, create: Table A Material Identification (component, visual evidence, candidates, most likely, confidence %, verification method). Table B Manufacturing Process (feature, evidence, candidates, VN alternative, cost/quality trade-off). Table C Surface Treatment. Table D Heat Treatment. Table E CRITICAL — Vietnam Manufacturing Capability Gap: classify each as Available-in-VN / Limited / Not-available / Substitute-exists. Flag strategic bottlenecks for technology sovereignty."

# Report 6: Tolerance & Performance Reverser
nlm notebook query re-{{short}} "Perform Inverse Tolerance Analysis: (A) Tolerance Hierarchy — classify dimensions as Tier 1 Functional (±0.01-0.05mm), Tier 2 Interface (±0.02-0.1mm), Tier 3 Assembly (±0.1-0.3mm), Tier 4 Cosmetic (±0.5mm+). (B) Datum Structure Reverse (primary/secondary/tertiary). (C) GD&T Inference per critical feature. (D) Fits & Clearances (ISO 286). (E) Critical Performance Parameters (loads, stresses, safety factors, fatigue life). (F) Manufacturing Capability Requirements (CNC grade, measurement equipment). Flag Quality Gate critical dimensions."

# Report 7: Redesign Strategist
nlm notebook query re-{{short}} "Act as Chief Design Engineer transitioning RE to P&B redesign. Create: (I) Modified Requirements List for Vietnam: Original vs Modified with rationale (tropical environment, VN manufacturing, ITAR-free, domestic MRO, cost, standardization). (II) Morphological Matrix with IP-free alternatives per critical function. (III) VDI 2225 evaluation with defense RE weights (Technical 35%, Manufacturability 25%, Sovereignty 20%, Cost 10%, Time 10%). (IV) Design Decisions Log. (V) Divergence Map (features kept/modified/added/removed with rationale)."

# Report 8: Validation & Testing Strategy
nlm notebook query re-{{short}} "Act as Test & Evaluation Lead. Design validation strategy proving redesign performs >= original. Level 1 Component (dimensional, material, surface, NDT). Level 2 Subsystem (load, MIL-STD-810G environmental, 461G EMC, reliability). Level 3 System Integration (end-to-end, interface compatibility, side-by-side). Level 4 Field (trial deployment, user feedback, MTBF/MTTR). Include Vietnam defense acceptance: thu nghiem xuat xuong, nghiem thu cap Bo, chien dau/su dung. Output: Test Plan Matrix with resource estimates and go/no-go gates."

# Report 9: Knowledge Capture Architecture
nlm notebook query re-{{short}} "Design knowledge management system for this RE project. Create: (1) RE Technical Dossier structure. (2) Design Pattern Library — reusable patterns (shock mounting naval, tropical sealing, desert thermal, EMI shielding). (3) Heuristics Database (rules of thumb from observed design). (4) Failure Mode Catalog. (5) Vietnam Supplier Capability Map. (6) Lessons Learned Register. (7) Compound Engineering workflow for future RE projects. (8) Strategic Capability Building Map: RE Project → Capabilities Gained → Sovereignty Contribution → Next RE Target."

# Report 10: Adversarial Audit
nlm notebook query re-{{short}} "Act as Red Team Auditor. Aggressively challenge RE output across 8 dimensions: (1) Requirements Completeness — missing/implicit/environmental/interface/lifecycle. (2) Function Structure — redundant/missing functions, edge cases. (3) Design Decisions — evidence, alternatives, biases (anchoring, availability, sunk cost, confirmation). (4) Manufacturability — VN workforce, training, tooling, yield, supplier failure. (5) Operational — field usability, maintenance, logistics. (6) Adversary — vulnerabilities, countermeasures. (7) Regulatory — MIL-STD, STANAG, VN regulatory. (8) Strategic — sovereignty contribution, opportunity cost, obsolescence. Output: Findings table with severity (Critical/High/Medium/Low) + Go/No-Go score."
```

#### Additional Reports cho MECHA mode (10 more):

```bash
# M-Report 1: System Boundary & Black Box
nlm notebook query re-{{short}} "Act as Systems Engineer. Perform Level 0 RE: (1) System Context Diagram — all external entities (users, target, environment, power, external systems, maintenance). (2) Interface Inventory — type, protocol, direction, signals, connector, criticality. (3) Behavioral Modes (Off/Standby/Init/Normal/Emergency/Maintenance/Shutdown). (4) Stimulus-Response Mapping. (5) Emergent Behavior Hypothesis. Output: Black Box Specification — external behavior only, solution-neutral."

# M-Report 2: Domain Decomposition
nlm notebook query re-{{short}} "Perform 4-domain decomposition: Domain 1 Mechanical (structural, kinematic, thermal, sealing, vibration). Domain 2 Electronic (power, signal conditioning, processing, sensors, actuators, PCB analysis). Domain 3 Software (bootloader, RTOS, drivers, middleware, application, control algorithms, safety). Domain 4 Control (inner/middle/outer/supervisory loops, state machines, safety logic). CRITICAL: Cross-Domain Mapping Matrix — Function vs Mech/Elec/Sw/Ctrl roles with integration concerns. Hidden dependencies: thermal→elec, vibration→sensors, EMI→sw, power→all."

# M-Report 3: Requirements from Testing (V-Model Right Side)
nlm notebook query re-{{short}} "Perform behavior-driven requirements reconstruction via Reverse V-Model: Level 1 Component Testing (test each component, infer spec). Level 2 Subsystem (control subsystem step response, navigation accuracy, comm range). Level 3 System (end-to-end mission scenarios). Level 4 Environmental (temperature, vibration, EMI, power variation). Level 5 Performance Envelope (min/max/nominal per parameter). Output: Reconstructed Requirements Specification with traceability from requirement → evidence → test → inferred spec."

# M-Report 4: Cross-Domain Function Allocator
nlm notebook query re-{{short}} "Analyze function-domain allocation: (A) Current allocation per function (Mech%/Elec%/Sw%/Ctrl%). (B) Allocation drivers (technology era, physical constraints, strategic, operational). (C) Alternative allocations: software-centric, electronics-centric, mechanical-centric, distributed — with pros/cons/Vietnam fit. (D) Domain-specific RE priority (difficulty vs redesign freedom). (E) Interface contracts between domains. Output: Architecture Decision Record per major allocation choice."

# M-Report 5: Control Law Reverser
nlm notebook query re-{{short}} "Reconstruct control system: (1) System identification tests (step response, frequency sweep, PRBS). (2) Black box model fitting (1st/2nd order, delay, state-space). (3) Controller structure identification (PID vs advanced). (4) Parameter extraction (Kp, Ki, Kd, filters, anti-windup). (5) State machine reverse (states, transitions, timing). (6) Safety/protection logic (over-current, link loss, geofencing, flight termination). (7) Control architecture (inner/middle/outer loop rates, latency budgets). (8) Parameter sensitivity analysis. Output: Control System Model Document with simulation model spec."

# M-Report 6: Firmware & Software Archaeology
nlm notebook query re-{{short}} "Perform software RE (behavior-based, legal): Layer 1 External observation (boot time, latency, failure modes → OS type, scheduler). Layer 2 Interface analysis (protocols, data formats, command mapping). Layer 3 Architecture hypothesis (Bare Metal / RTOS / Linux / Hybrid). Algorithm inventory: sensor fusion, navigation, control, signal processing, encryption. Software requirements reconstruction per IEEE 830. Redevelopment strategy: Full independent / Open-source (ArduPilot, PX4, FreeRTOS) / COTS / Hybrid. Output: Software Architecture Document with redevelopment recommendation."

# M-Report 7: Integration Challenge Predictor
nlm notebook query re-{{short}} "Predict re-integration issues across 7 categories: (1) Timing & latency risks (sensor→processor→actuator chain). (2) Resource contention (CPU, memory, bus, power, thermal). (3) EMC risks (MIL-STD-461G: CE/CS/RE/RS). (4) Thermal risks (hotspots, cooling disruption). (5) Mechanical tolerance stack-up (optical/PCB/antenna alignment). (6) Software-hardware coupling (ADC resolution, motor params in SW). (7) Control stability (new dynamics → retune). Design bottom-up integration test sequence. List early warning indicators. Output: Integration Risk Register."

# M-Report 8: V&V Strategy (VDI 2206)
nlm notebook query re-{{short}} "Design V&V strategy per VDI 2206 right-side V-model: Level 1 Unit/component (bench, HIL, SIL). Level 2 Domain integration (CMM, functional, EMC pre-compliance, code coverage). Level 3 Cross-domain (vibration survival, register access, algorithm verification). Level 4 System (IEEE 1012: analysis, inspection, demonstration, test). Level 5 Validation (side-by-side, benchmarking, user acceptance). Environmental (MIL-STD-810G: methods 501-520). EMC (MIL-STD-461G). Reliability (HALT, HASS, life cycle). Safety (FMEA/FMECA). Software V&V (MISRA-C, coverage, traceability). Vietnam test facilities assessment. Output: V&V Strategy Document."

# M-Report 9: MBRE Digital Thread
nlm notebook query re-{{short}} "Design Model-Based RE implementation: Layer 1 Requirements Model (SysML). Layer 2 System Architecture (BDD, IBD). Layer 3 Behavioral (State Machine, Activity, Sequence). Layer 4 Physics (Modelica/Simulink). Layer 5 Control (executable algorithms). Layer 6 Software Architecture (UML). Digital thread connectivity. Model validation against original. HIL/SIL/PIL testing infrastructure. Tool recommendations for Vietnam (open-source: Papyrus, OpenModelica, Scilab vs commercial: Simulink, dSPACE). Output: MBRE Implementation Plan."

# M-Report 10: Maturity Assessment
nlm notebook query re-{{short}} "Assess RE maturity across 8 dimensions: (1) Understanding Depth L1-L5 (Surface→Generative) 20%. (2) Documentation Completeness 10%. (3) Model Fidelity F1-F5 10%. (4) Verification Coverage 20%. (5) Risk Assessment 15%. (6) Production Readiness 10%. (7) Sovereignty Score (domestic %) 10%. (8) Lifecycle Readiness 5%. Scoring: >80 Go, 70-80 Conditional, <70 No-go. Red team questions: Would original developer recognize this? Could I design from scratch? Biggest uncertainty? Where will it fail? Am I fooling myself? Output: Maturity Assessment Report with gap analysis."
```

### Step KB-4: Generate Quiz & Study Materials

```bash
# Quiz for RE knowledge validation
nlm notebook query re-{{short}} "Create expert-level RE assessment: PART A (10 MCQ): material identification from visual evidence, tolerance inference, manufacturing process detection, failure mode prediction. PART B (5 scenarios): (1) identify material from corrosion pattern + color + weight, (2) infer manufacturing process from tool marks, (3) reverse GD&T from mating surfaces, (4) determine control loop type from step response data, (5) assess VN manufacturability of a component. Each answer with: correct answer, why others wrong, common RE mistakes, confidence level required. Bloom's taxonomy: mostly Analyze and Evaluate level."

# Flashcards for quick reference
nlm notebook query re-{{short}} "Create 30 flashcard pairs (Q/A) covering: (10) Material identification visual cues, (5) Manufacturing process evidence signatures, (5) Tolerance tier classification rules, (5) VDI 2225 defense RE evaluation criteria, (5) Vietnam manufacturing capability quick-check. Format: | Q | A | Difficulty |"
```

### Step KB-5: Generate Studio Artifacts (persistent learning materials in NLM UI)

After NLM conversation queries (KB-3 + KB-4) are complete, generate persistent Studio artifacts. These are accessible via NLM notebook UI even after conversation context expires — CEO's long-term RE reference library.

**CEO gate:** "Tạo bộ Studio artifacts (quiz, flashcards, reports, audio) trong NLM? ~5 phút."
**Trigger:** Auto-suggest after KB-4 completes. CEO can skip if only needs conversation reports.

Use `mcp__notebooklm-mcp__studio_create` MCP tool for ALL artifacts. Do NOT use `nlm audio create` CLI (not supported).

**CRITICAL — Prompt Quality Rule:**
- NEVER use generic focus_prompts → NLM auto-generates shallow, generic content
- Every artifact MUST include WX-specific context: product name, RE mode, VN manufacturing capability
- Quiz: material ID scenarios + tolerance inference + VN manufacturability assessment
- Flashcards: Easy/Medium/Hard tiers + visual cues + process signatures + design rules
- Reports: RE-specific structure (3D-A-R-D phases) with VN sovereignty assessment
- Audio: focus on hidden design intent, IP risks, and VN manufacturing gaps

**6 artifacts to generate (parallel where possible):**

```
# Artifact 1: Quiz (hard, RE-specific scenarios)
studio_create(notebook_id={{uuid}}, artifact_type="quiz", question_count=10, difficulty="hard",
  focus_prompt="RE assessment for {{product}} — Vietnam defense context.
  PART A (10 MCQ): (1) material identification from visual/physical evidence,
  (2) manufacturing process detection from tool marks/surface finish,
  (3) tolerance inference from mating surfaces, (4) failure mode prediction
  from design choices, (5) VN manufacturability assessment.
  Each answer: why correct, why others wrong, confidence level required, Bloom's level.
  PART B (5 RE scenarios): (1) identify material from corrosion + color + weight,
  (2) infer process from tool marks, (3) reverse GD&T from assembly,
  (4) assess IP risk for specific component, (5) determine VN domestic alternative.",
  confirm=True)

# Artifact 2: Flashcards (Easy/Medium/Hard, RE knowledge)
studio_create(notebook_id={{uuid}}, artifact_type="flashcards", difficulty="medium",
  focus_prompt="20 flashcard pairs for RE of {{product}}:
  EASY (7): material visual identification cues, basic manufacturing process signatures,
  standard tolerance tiers (Tier 1-4).
  MEDIUM (7): VDI 2225 defense RE evaluation criteria, function-component mapping,
  surface treatment identification, joining method evidence.
  HARD (6): hidden design intent inference, IP/patent risk indicators,
  Vietnam manufacturing capability gaps, ITAR-free substitution rules,
  cross-domain integration risks (for MECHA mode).
  All focused on {{product}} specifics.",
  confirm=True)

# Artifact 3: Briefing Doc (RE executive summary)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Briefing Doc",
  focus_prompt="WORKSHOP X CEO RE BRIEFING — {{product}}
  Structure: (1) ARTIFACT OVERVIEW: what we're looking at, origin, condition.
  (2) KEY FINDINGS: top 5 design intent discoveries with confidence levels.
  (3) IP & LEGAL: go/no-go assessment, patent landscape, ITAR status.
  (4) VN CAPABILITY GAP: what we can make vs what we can't (with alternatives).
  (5) REDESIGN STRATEGY: keep/modify/replace decisions with rationale.
  (6) SOVEREIGNTY SCORE: % domestic content achievable, critical foreign dependencies.
  (7) NEXT ACTIONS: physical tests needed, supplier contacts, timeline.
  Cite specific sources with confidence H/M/L.",
  confirm=True)

# Artifact 4: Study Guide (RE methodology mastery)
studio_create(notebook_id={{uuid}}, artifact_type="report", report_format="Study Guide",
  focus_prompt="WORKSHOP X RE STUDY GUIDE — {{product}}
  Ordered learning path for engineering team:
  Step 1 3D PHASE: how to deconstruct this specific artifact (tools, sequence, evidence).
  Step 2 ABSTRACTION: reconstructing design intent and requirements from physical evidence.
  Step 3 MATERIALS & PROCESS: identification techniques for materials found in {{product}}.
  Step 4 FUNCTION STRUCTURE: 6-flow decomposition applied to this product.
  Step 5 REDESIGN: P&B forward design with VN constraints and ITAR-free alternatives.
  Step 6 V&V: validation strategy proving redesign >= original.
  For each step: key techniques, common mistakes, VN-specific considerations, exercises.",
  confirm=True)

# Artifact 5: Audio Deep Dive (RE findings)
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="deep_dive",
  language="vi",
  focus_prompt="Focus on key RE findings for {{product}}: hidden design intent discoveries,
  material/process mysteries solved, IP landscape assessment, Vietnam manufacturing
  capability gaps, and redesign strategy with domestic sovereignty implications.",
  confirm=True)

# Artifact 6: Audio Critique (RE assumptions challenge)
studio_create(notebook_id={{uuid}}, artifact_type="audio", audio_format="critique",
  language="vi",
  focus_prompt="Critically evaluate the RE analysis of {{product}}: What assumptions are
  we making about materials that need physical verification? Where could our function
  structure be wrong? What IP risks are we underestimating? What VN manufacturing
  capabilities are we overestimating? What would go wrong if we proceed to redesign
  with current confidence levels?",
  confirm=True)
```

**Verify all 6 complete:**
```
studio_status(notebook_id={{uuid}})
```

### Step KB-6: Save Report Index to Vault

Save index file to project:

```markdown
# NLM Knowledge Base — RE: {{product}}
Notebook: re-{{short}}
Created: {{today}}
Reports: {{10 or 20}} (MECH: 10, MECHA: 20)

## Report Index
| # | Report | Query Type | Use When |
|---|--------|-----------|----------|
| 1 | Artifact Deconstruction | Stage 1 | Starting physical analysis |
| 2 | Design Intent Decoder | Stage 2 | Reconstructing requirements |
| 3 | IP & Legal Navigator | Stage 0 | Go/no-go decision |
| 4 | Functional Abstraction | Stage 2 | Building function structure |
| 5 | Material & Process | Stage 1 | VN capability gap analysis |
| 6 | Tolerance & Performance | Stage 1 | Critical dimensions |
| 7 | Redesign Strategist | Stage 3 | P&B forward design |
| 8 | Validation Strategy | Stage 4 | Test planning |
| 9 | Knowledge Capture | Stage 5 | Compound learning |
| 10 | Adversarial Audit | Stage 4 | Red team review |
[MECHA] 11-20: System Boundary, Domain Decomposition, V-Model Requirements, Cross-Domain Allocator, Control Law, Firmware Archaeology, Integration Risks, V&V Strategy, MBRE Digital Thread, Maturity Assessment

## Studio Artifacts (persistent in NLM UI)
| # | Title | Type | Status |
|---|-------|------|:------:|
| 1 | {{title}} | Quiz (MCQ + RE Scenarios) | ✅/⏳ |
| 2 | {{title}} | Flashcards (Easy/Med/Hard) | ✅/⏳ |
| 3 | {{title}} | Briefing Doc (RE Summary) | ✅/⏳ |
| 4 | {{title}} | Study Guide (RE Methodology) | ✅/⏳ |
| 5 | {{title}} | Audio Deep Dive | ✅/⏳ |
| 6 | {{title}} | Audio Critique | ✅/⏳ |

## Chat Persona
Persona text pasted into NLM Settings: YES/NO
Mode: MECH / MECHA

## How to Use in NLM Chat
After reports are generated, CEO can chat in NLM with questions like:
- "So sanh vat lieu component X voi alternative VN"
- "Tolerance nao la critical nhat cho function Y?"
- "Rui ro IP cao nhat o dau?"
- "VN co the san xuat component nao bang noi luc?"
NLM chat will use both uploaded sources AND generated reports to answer.
```

Save to: `1_Projects/{{project}}/Ref/NLM_KB_RE_{{product}}_{{date}}.md`

---

## INTEGRATION WITH EXISTING SKILLS

| Stage/Mode | Related Skills | How Connected |
|------------|---------------|---------------|
| FIELD | /forge-shift, /forge-scout, /bd-pulse | ACH opportunities, customer intel |
| FIELD | /forge-flywheel, /data-capture | Field data → AI training pipeline |
| FIELD | /forge-portfolio | MAINT-KIT revenue, product health |
| TECHNOLOGY | /research, /nlm | OSINT survey, NLM knowledge base |
| TECHNOLOGY | /forge-library | Technology → model library |
| COMPARE C0 | /forge-pre-study | Reality filter alignment |
| 0 | — | Standalone legal gate |
| 1 | /bom, /helix-p3-bom | Component inventory → BOM draft |
| 2 | /helix-task-clarify, /6flow | Requirements + function structure |
| 3 | /helix-concept-generate, /reverse-mc | Morpho matrix + concept selection |
| 4 | /validate, /verify, /helix-quality-gate | V&V plan + gate review |
| 5 | /galaxy-note, /learning, /teach | Knowledge capture + Galaxy |

**Handoff to HELIX pipeline (seamless transition):**

RE outputs are now HELIX-compatible, enabling direct handoff:

```
RE Stage 2A → HELIX Phase 1 equivalent:
  RE_{{product}}_S2A_Requirements.md    ≈  Requirements_List_v1.0.md (17 P&B categories, D/W)
  RE_{{product}}_S2A_TVDT.md            ≈  TVDT.md (Target Values Decision Table)

RE Stage 2B → HELIX Phase 1 BD equivalent:
  RE_{{product}}_S2B_Function_Structure.md  ≈  Function_Structure.md (6-flow)
  RE_{{product}}_S2B_Solution_Det_SF.md     ≈  Phase 2 BA Problem_Frame.md input
  RE_{{product}}_S2B_Design_Type.md         ≈  Design_Type.md (O/A/V → GREEN/AMBER/RED)

RE Stage 3 → HELIX Phase 2 equivalent:
  RE_{{product}}_S3B_Morpho_Matrix.md       ≈  Morphological_Matrix.md
  RE_{{product}}_S3C_VDI2225.md             ≈  VDI_2225_Evaluation.md
  RE_{{product}}_S3D_Divergence_Map.md      → unique to RE (no HELIX equivalent)

Requirements_Delta_Log.md                    ≈  Requirements_Delta_Log.md (identical mechanism)
```

After Stage 3 concept selection, product enters normal HELIX flow:
- Stage 3 output → /helix-embody-realize (Phase 3) — reads RE morpho matrix + VDI 2225
- Stage 4 output → /helix-detail-finalize (Phase 4)
- Requirements Delta Log → continues into HELIX phases (same VDI 2221:2019 mechanism)

---

## RULES

1. **One stage per turn** — execute stage, STOP, wait CEO approval
2. **CEO gates are Core** — go/no-go decisions, D/W classification, concept selection, SOURCE SELECTION
3. **Source Quality Gate (NLM-4) mandatory** — after source ingestion: verify count, recover failures (alt URL → WebFetch→text → YouTube), present gap report, STOP until CEO confirms "du nguon". CEO can add manually. NEVER run NLM queries without CEO source approval. Same protocol as /research Step 4G.
4. **Confidence levels mandatory** — every inference must have H/M/L confidence
4. **VN capability gap flagged** — every material/process must show VN availability
5. **IP awareness continuous** — flag potential IP issues throughout, not just Stage 0
6. **Solution-neutral abstraction** — Stage 2B Step 4 is the most critical step for IP-free redesign
7. **Physical validation anchor** — analyst trap guard: if RE produces only documents without physical test plan, flag
8. **NLM for volume, Claude for depth** — use NLM when sources > 5000 words or multiple docs
9. **Galaxy = distilled only** — RE findings go to Dossier, only Three Laws go to Galaxy candidates
10. **Clean-room documentation** — maintain evidence of independent development throughout

---

## TYPICAL TIMELINES

**Field Intelligence (FIELD mode):**
- F1-F2: 1-2 weeks (data collection + analysis)
- F3-F4: 1 week (competitive + next-gen)
- F5-F6: 0.5-1 week (ACH overlay + cross-product)
- Total: 2.5-4 weeks per product line
- **Recommended:** Run FIELD on all 6 product lines = 15-24 weeks total (can parallelize)

**Technology Domain RE (TECHNOLOGY mode):**
- T1: 1-2 days (domain definition)
- T2: 2-4 weeks (OSINT survey)
- T3-T4: 1-2 weeks (decomposition + mapping)
- T5-T6: 1-2 weeks (gap analysis + roadmap)
- Total: 4-8 weeks per technology domain

**Comparative Evaluation (COMPARE mode):**
- C0: 0.5 day (reality filter)
- C1: 2-4 weeks | C2: 1-2 weeks | C3: 1-2 weeks | C4: 1 week
- Total: 4-9 weeks

**Mechanical RE (MECH mode):**
- Stage 0: 1 day | Stage 1: 2-4 weeks | Stage 2: 1-2 weeks | Stage 3: 2-4 weeks | Stage 4: 4-8 weeks | Stage 5: 1 week
- Total: 10-19 weeks

**Mechatronic RE (MECHA mode):**
- Stage 0: 1 day | Stage 1: 3-6 weeks | Stage 2: 3-4 weeks | Stage 3: 4-6 weeks | Stage 4: 8-13 weeks | Stage 5: 1-2 weeks
- Total: 19-31 weeks (~5-8 months)

**Audit only (AUDIT mode):** 1-2 weeks
**Knowledge capture only (CAPTURE mode):** 2-3 days
