---
name: forge-market-intel
description: Continuous market intelligence for Workshop X — competitor monitoring, ASEAN export strategy, and partnership evaluation. Three sub-modes for defense market awareness. This skill should be used when the user asks about "competitor watch", "doi thu canh tranh", "ASEAN export", "xuat khau ASEAN", "partnership evaluation", "danh gia doi tac", "market intelligence", "tinh bao thi truong", "competitive monitoring", or "theo doi doi thu". Grounded in WX reality (26 people, $3-6M revenue, 3-5 year competitive window).
---

# Forge Market Intel — Continuous Market Intelligence

Three-mode market intelligence system for Workshop X. Grounded in 26-person team reality, $3-6M revenue, and 3-5 year competitive window to ~2030.

Usage: `/forge-market-intel [--competitor | --export | --partner]`

Default: `--competitor` (most frequent use)

## When to Use

- Monthly: `--competitor` quick scan (15 min)
- Quarterly: `--competitor` deep review (1 hour)
- When evaluating new markets: `--export`
- When partnership opportunity arises: `--partner`
- Before exhibitions/trade shows: `--competitor` + `--export`
- When bd-pulse detects competitor mention: `--competitor` focused

---

## MODE 1: --competitor — Continuous Competitor Monitoring

**COD: Offload** (AI monitors) → **Core** (CEO validates signals and decides responses)

### Step 1: Competitor Watch List

```
COMPETITOR WATCH LIST — Workshop X
Date: {{today}}  |  Review: Monthly / Quarterly / Annual

=== TIER 1 — DIRECT THREATS ===

| # | Competitor | Country | Products | WX Overlap | Threat Level | Last Signal |
|---|-----------|---------|----------|-----------|-------------|------------|
| 1 | HII (Huntington Ingalls) | USA | UTT-Vehicle, LARS | UTT family | LOW (ITAR blocks VN) | |
| 2 | Kongsberg | Norway | K-TAG UTT, sonar | UTT-Towed | HIGH | |
| 3 | Meggitt | Canada/UK | Hammerhead, Rapier | STT-B, surface targets | MEDIUM | |

=== TIER 2 — MEDIUM THREATS ===

| # | Competitor | Country | Products | WX Overlap | Threat Level | Last Signal |
|---|-----------|---------|----------|-----------|-------------|------------|
| 4 | ECA Group | France | Mine warfare training | UTT-Mine | MEDIUM | |
| 5 | Atlas Elektronik | Germany | Mine warfare tech | Signature tech | LOW-MEDIUM | |
| 6 | Korean Shipyards | Korea | MSM-class | Different scale | LOW | |
| 7 | Chinese suppliers | China | Price segment | Indirect (ASEAN) | LOW (political barrier) | |

=== TIER 3 — EMERGING THREATS ===

| # | Competitor | Country | Products | WX Overlap | Threat Level | Last Signal |
|---|-----------|---------|----------|-----------|-------------|------------|
| 8 | Turkish ecosystem (TAI/Baykar) | Turkey | Simsek, UAV portfolio | ATT family | MEDIUM | |
| 9 | Indian industry (DRDO) | India | Abhyas, growing export | ATT, export | LOW-MEDIUM | |
| 10 | Israeli systems (Elbit/IAI) | Israel | Training systems | TMS, sims | LOW (via 3rd party) | |
```

### Step 2: Intelligence Collection

```
INTELLIGENCE SOURCES — Monthly Scan

PUBLIC SOURCES (weekly — AI Offload):
☐ Jane's Defence Weekly — new product announcements
☐ Flight Global — aerial target systems
☐ Defense News — ASEAN defense deals
☐ Aviation Week — technology developments
☐ Regional: ASEAN Defence, Nhan Dan Quan Doi

EVENT MONITORING (quarterly — track calendar):
| Event | Location | Date | WX Attend? | Competitors Expected |
|-------|----------|------|-----------|---------------------|
| IDEX | UAE | Feb | No | Kongsberg, ECA |
| IDEF | Turkey | May | TBD | TAI, Baykar |
| DefExpo | India | Feb | TBD | DRDO, BEL |
| Eurosatory | France | Jun | No | ECA, Atlas |
| DSEI | UK | Sep | No | Meggitt, QinetiQ |
| LIMA | Malaysia | Dec | YES | All ASEAN competitors |
| BRIDEX | Brunei | TBD | TBD | Regional |
| Vietnam DSE | Vietnam | Dec | YES (home) | All interested in VN |

PATENT MONITORING (quarterly — AI Offload):
☐ Key competitors' new patent filings (Google Patents, Espacenet)
☐ Signature generation patents
☐ Training system patents
☐ Target system patents

CUSTOMER INTELLIGENCE (ongoing — Core, CEO only):
- VN Navy contacts: who else is proposing?
- Trade attache networks
- Supplier relationship intel
```

### Step 3: Threat Assessment

```
MONTHLY THREAT ASSESSMENT — {{month}} {{year}}

NEW SIGNALS DETECTED:
| # | Signal | Source | Competitor | Threat To | Urgency |
|---|--------|--------|-----------|----------|---------|

SIGNAL INTERPRETATION:
| Signal | What It Means | WX Response Required? | Timeline |
|--------|-------------|---------------------|---------|

=== SPECIFIC WATCH ITEMS ===

SIGNAL 1 — UTT COMPETITION:
- Kongsberg K-TAG enters ASEAN? {{status}}
- ECA Group UTT-Mine ASEAN deal? {{status}}
- Chinese UTT emergence? {{status}}
→ Response if triggered: Accelerate UTT-Towed launch

SIGNAL 2 — ATT COMPETITION:
- Turkish Simsek to other ASEAN? {{status}}
- Chinese target drone exports? {{status}}
- Indian Abhyas exports? {{status}}
→ Response if triggered: Differentiate TARGET-DRONE via ACH features

SIGNAL 3 — STT COMPETITION:
- Meggitt surface target ASEAN? {{status}}
- Korean autonomous boat targets? {{status}}
- Commercial USV military adaptations? {{status}}
→ Response if triggered: Accelerate STT-B development

SIGNAL 4 — SOFTWARE COMPETITION:
- Major training SW company ASEAN entry? {{status}}
- Local competitor emergence? {{status}}
- Open-source alternative maturation? {{status}}
→ Response if triggered: TMS platform moat deepening

OVERALL THREAT LEVEL: GREEN / YELLOW / RED
COMPARED TO LAST MONTH: IMPROVED / STABLE / DEGRADED
```

### Step 4: Response Playbook (pre-defined)

```
RESPONSE PLAYBOOK

THREAT: Competitor enters VN market
→ Leverage existing VN Navy relationship
→ Emphasize: ITAR-free, local support, ASEAN solidarity
→ Pricing strategy: maintain 40-60% cost advantage

THREAT: Technology leap by competitor
→ ACH differentiation (AI adaptation faster than hardware replacement)
→ Academic acceleration partnership
→ Feature parity timeline assessment

THREAT: Price pressure
→ Value-based pricing (training effectiveness, not hardware specs)
→ Customer support + ecosystem as differentiator
→ Cost reduction via ACH + continuous improvement
```

Save to: `2_Areas/FORGE/Market-Intelligence/COMPETITOR_WATCH_{{date}}.md`

**STOP. CEO reviews signals and decides responses.**

---

## MODE 2: --export — ASEAN Export Market Intelligence

**COD: Core** (strategic market entry decisions)

### Step 1: Country Analysis

```
ASEAN EXPORT OPPORTUNITY MATRIX — Workshop X
Date: {{today}}

| # | Country | Defense Budget | Naval Focus | Threat Similarity | WX Products Fit | Entry Barrier | Timeline | Priority |
|---|---------|--------------|-----------|------------------|----------------|-------------|---------|----------|
| 1 | Indonesia | Large, growing | HIGH (archipelago) | Similar to VN | UTT/ATT/STT/TMS | Bureaucratic, local content | 2029-2031 | HIGH |
| 2 | Philippines | Growing (SCS) | HIGH | Similar to VN | All families | Political, US alliance | 2030+ | MEDIUM |
| 3 | Malaysia | Moderate | MEDIUM | Moderate | ATT/TMS/naval | Own defense industry | 2030-2031 | MEDIUM |
| 4 | Thailand | Substantial | MEDIUM | Different | Broad | Internal politics | 2030+ | LOW-MEDIUM |
| 5 | Singapore | High per capita | HIGH (quality) | Different | Niche only | Sophisticated buyer | Opportunistic | LOW |

DETAILED ANALYSIS PER COUNTRY:

### {{Country}}

DEFENSE PROFILE:
- Budget: ${{X}}/year
- Modernization status: {{description}}
- Key suppliers: {{list}}
- Procurement process: {{description}}

TRAINING MARKET:
- Current training systems: {{list}}
- Training gaps identified: {{list}}
- Budget per training category: {{estimate}}

WX OPPORTUNITY:
- Products applicable: {{list with priority}}
- Estimated TAM: ${{range}}/year
- Competitive landscape: {{who else is selling}}
- WX advantages: {{list}}

ENTRY BARRIERS:
- Regulatory: {{specific requirements}}
- Local content: {{requirement %}}
- Political: {{considerations}}
- Competition: {{established players}}

RECOMMENDED APPROACH:
- Entry strategy: Product-led / Partnership-led / Exhibition-led / Government-led
- First product to offer: {{product}}
- Timeline: {{exploration → engagement → first contract}}
- Investment required: ${{range}}
```

### Step 2: Entry Strategy

```
ASEAN EXPORT STRATEGY — Workshop X

ENTRY FRAMEWORK:
1. Exhibition presence starting 2028 (LIMA, DSA, regional)
2. Product demonstrations 2029
3. First customer engagement 2030
4. First contracts 2031
5. Production deliveries 2032+

RESOURCE REQUIREMENTS:
- BD director hired: 2028 (${{salary}})
- Travel budget: $50-100K/year
- Exhibition budget: $100-200K/year
- Per-country localization: $100-200K
- Certification/compliance: $50-100K per market

REVENUE TRAJECTORY:
| Year | Phase | Revenue Est. |
|------|-------|-------------|
| 2028 | Exploration | $0 |
| 2029 | Small pilots | ~$100K |
| 2030 | First contracts | $200-500K |
| 2031 | Established | $500K-1M |
| 2032 | Multi-country | $1-2M |
| 2035 | Mature | $3-6M |
| 2036 | Target | $5-10M ASEAN export |
```

Save to: `2_Areas/FORGE/Market-Intelligence/ASEAN_EXPORT_{{date}}.md`

**STOP. CEO reviews and prioritizes markets.**

---

## MODE 3: --partner — Partnership Opportunity Filter

**COD: Core** — strategic partnership decisions are non-delegable.

### Step 1: 5-Criteria Filter

```
PARTNERSHIP EVALUATION — {{partner name}}
Date: {{today}}

=== 5-CRITERIA FILTER (ALL must pass) ===

☐ CRITERION 1 — PHASE 1 PRODUCTIVE:
  Does this help 2026-2028 cash cow compound + UTT-Towed launch?
  Evidence: {{specific deliverable or capability}}
  PASS / FAIL / CONDITIONAL

☐ CRITERION 2 — MANAGEABLE SCALE:
  Can 26-person team actually manage this relationship?
  FTE commitment required: {{estimate}}
  CEO time required: {{hours/month}}
  PASS / FAIL / CONDITIONAL (>2 FTE = FAIL)

☐ CRITERION 3 — CLEAR VALUE:
  Specific deliverable, not vague "strategic cooperation"?
  Deliverable: {{specific, measurable output}}
  Timeline: {{when delivered}}
  PASS / FAIL / CONDITIONAL

☐ CRITERION 4 — RISK-PROPORTIONATE:
  What's the failure mode? Acceptable given WX size?
  Worst case: {{scenario}}
  Cost of failure: ${{range}}
  Recovery plan: {{description}}
  PASS / FAIL / CONDITIONAL

☐ CRITERION 5 — CULTURAL FIT:
  Partner workable with WX style?
  Decision speed: {{fast/slow vs WX}}
  Communication: {{language, timezone, formality}}
  Track record with similar-sized partners: {{evidence}}
  PASS / FAIL / CONDITIONAL

VERDICT:
  Criteria passed: {{N}}/5
  ALL PASS = PROCEED to detailed evaluation
  ANY FAIL = DECLINE (with documented reason)
  CONDITIONAL = CEO judgment call (document rationale)
```

### Step 2: Partnership Portfolio

```
PARTNERSHIP PORTFOLIO — Workshop X
Date: {{today}}

=== TIER 1: STRATEGIC (2-3 max) ===
| # | Partner | Type | Value | FTE | Status | Health |
|---|---------|------|-------|-----|--------|--------|
| 1 | VN Navy | Customer | Survival | Significant | Ongoing | {{G/Y/R}} |
| 2 | {{TRV partner}} | Technology | ATT capability | 1-2 | {{status}} | {{G/Y/R}} |
| 3 | India framework | Strategic | Long-term | 0.5 | Building | {{G/Y/R}} |

=== TIER 2: TACTICAL (4-6 max) ===
| 4 | {{VN university}} | Academic | Talent pipeline | 0.1 | {{status}} | |
| 5 | {{intl university}} | Academic | Research | 0.1 | {{status}} | |
| 6-8 | Component suppliers | Supply | Components | 0.1 ea | Active | |

=== TIER 3: OPPORTUNISTIC (monitor only) ===
| 9+ | Potential future partners | Watch | Variable | 0 | Monitoring | |

TOTAL FTE COMMITMENT: {{sum}} / 26 team = {{%}}
⚠️ If > 2 FTE on partnerships → overhead too high for current scale

=== AVOID LIST (for now) ===
- Large Western defense primes (scale mismatch, ITAR)
- Complex multilateral programs (overhead)
- Speculative research partnerships (unclear ROI)
- Any partnership requiring > 2 FTE commitment
```

### Step 3: New Partnership Decision Framework

```
QUICK FILTER FOR NEW PARTNERSHIP REQUESTS:

1. Phase 1 urgency? NO → defer to Phase 2+
2. Compounds existing capability? NO → decline
3. 26-person team has capacity? NO → decline
4. Clear ROI within 18 months? NO → investigate or decline
5. Cultural fit? NO → decline

Only "YES" to all 5 → proceed to detailed 5-criteria evaluation above.
```

Save to: `2_Areas/FORGE/Market-Intelligence/PARTNER_EVAL_{{partner}}_{{date}}.md`

**STOP. CEO decides on partnership action.**

---

## Integration

```
forge-market-intel READS FROM:
  - bd-pulse → relationship health, customer signals
  - forge-portfolio → product status, FORGE scores
  - forge-evolve → moat assessment, identity trajectory
  - reverse-engineering FIELD → customer displacement data
  - reverse-engineering COMPARE → competitor product analysis

forge-market-intel WRITES TO:
  - bridge-risk-radar → competitive threat signals
  - forge-portfolio → market context for prioritization
  - forge-pre-study → competitor data for PRESTUDY E-EXISTING
  - reverse-engineering COMPARE → candidates for evaluation
  - forge-evolve → moat inputs (competitor activity)
```

## Rhythms

| Activity | Frequency | Mode | Duration | Owner |
|----------|-----------|------|----------|-------|
| Signal scan | Weekly | --competitor | 15 min | AI (Offload) |
| Threat assessment | Monthly | --competitor | 30 min | CEO reviews |
| Deep competitive review | Quarterly | --competitor | 1 hour | CEO + AI |
| Export strategy review | Semi-annually | --export | 1 hour | CEO |
| Partnership portfolio review | Quarterly | --partner | 30 min | CEO |

## Rules

- Competitor monitoring is Offload — AI scans, CEO validates signals
- Strategic responses are Core — CEO decides, not AI
- No classified info in competitor analysis — OSINT only
- Export decisions are Phase 3 (2030+) — monitor now, don't execute
- Partnership filter must be ruthless — 26 people cannot support many partnerships
- Always ask: "What does this intelligence change about what we ship?"

## COD Classification

- Intelligence collection: Offload (O1) — AI gathers
- Signal interpretation: Offload (O2) — AI proposes significance
- Strategic response: **Core (C)** — CEO decides
- Market entry decisions: **Core (C)** — CEO judgment
- Partnership evaluation: **Core (C)** — non-delegable
