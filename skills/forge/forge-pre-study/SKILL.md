---
name: forge-pre-study
description: Lightweight 30-minute product opportunity screening before committing to full ODI/JTBD analysis. Use when a new product idea, customer request, or market signal needs quick GO/PARK/KILL decision. Triggers on "new product idea", "pre-study", "should we pursue", "co nen lam", "danh gia co hoi", "san pham moi", "opportunity screening", "nên làm không", "prestudy".
---

# FORGE Pre-Study — Stage -1 Product Opportunity Screening

30-minute max screening to decide whether Workshop X should invest effort in full `/forge-job-map` analysis (2-4 hours). Answers: "Should WX pursue this product opportunity?"

## When to Use

- CEO receives a customer inquiry or market signal about a new product
- `bd-pulse` logs a touchpoint mentioning a potential new product need
- `bridge-signal-extract` captures a signal that looks like a product opportunity
- CEO has an idea for a new product and wants quick sanity check
- BEFORE creating a new project folder or running `/forge-job-map`

## When NOT to Use

- Product already has a project folder → use `/forge-job-map` or check Status.md
- Evaluating an EXISTING product for ACH → use `/forge-shift`
- Deep competitive analysis needed → use `/reverse-mc`

## Workflow

### Step 1: Capture the Signal

Document the raw opportunity in 1-2 sentences:

```
PRE-STUDY SIGNAL — {{date}}

Source: {{bd-pulse / customer conversation / competitor observation / CEO idea / market research}}
Signal: "{{raw description of the opportunity}}"
```

### Step 2: Run PRESTUDY Checklist (7 Questions, 30 Minutes Max)

For each question, spend MAX 4 minutes. Gut feeling + 1-minute search is sufficient. This is a FILTER, not an analysis.

```
PRESTUDY SCREENING — {{product_idea}}
Date: {{today}}
Time started: {{HH:MM}}

P — PEOPLE (Ai cần?)
  Target user: {{role — e.g., "gunner", "instructor", "maintenance crew"}}
  Unit type: {{military unit — e.g., "infantry battalion", "naval vessel", "training center"}}
  Estimated count: {{number of potential units × users per unit}}
  Confidence: {{HIGH/MED/LOW — do we actually know or guessing?}}
  → {{assessment}}

R — REVENUE (Bao nhiêu tiền?)
  Unit price estimate: ${{price}} (±50% OK — order of magnitude)
  TAM (Total Addressable Market): {{units}} × ${{price}} = ${{TAM}}/year
  Recurring revenue potential: {{consumables / maintenance / software updates / training}}
  → {{assessment}}
  KILL if: TAM < $100K/year (not worth WX effort as solo CEO)

E — EXISTING (Ai đang bán?)
  Known competitors: {{name1 ($price1), name2 ($price2)}} — 1 minute search max
  Market gap (gut feel): {{what they don't do / price gap / capability gap}}
  → {{assessment}}
  WARNING if: Dominant incumbent, no visible gap

S — SKILL FIT (WX làm được?)
  Cơ khí (Mechanical): {{YES/PARTIAL/NO}} — {{brief why}}
  Điện tử (Electronics): {{YES/PARTIAL/NO}} — {{brief why}}
  AI/Software: {{YES/PARTIAL/NO}} — {{brief why}}
  Triple Helix score: {{0-3}}/3
  → {{assessment}}
  KILL if: 0/3 domains (completely outside WX capability)
  WARNING if: 1/3 domains (heavy dependency on partners)

T — TIMING (Khi nào cần?)
  Budget cycle: {{when does customer procure? — e.g., "Q4 2026", "unknown"}}
  Procurement window: {{open / closing / closed / unknown}}
  Urgency signal: {{customer said "urgent" / routine inquiry / strategic planning}}
  → {{assessment}}
  PARK if: Window closed, next cycle > 12 months

U — UNIQUE (WX khác gì?)
  Differentiation hypothesis (1 sentence): "WX is the only one that {{differentiator}}"
  ACH advantage applicable?: {{YES — AI compensates hardware / NO — pure hardware}}
  Price positioning: {{10× cheaper / comparable / premium}}
  → {{assessment}}
  WARNING if: "Same as competitor but cheaper" = weak moat, price war risk

D — DECISION INPUTS (ACH potential?)
  ACH candidate: {{YES / NO / MAYBE}}
  If YES: Which physical limitation could AI compensate? {{brief}}
  IRONMESH reuse: {{which existing modules/models transfer? — e.g., "scoring from VN-12.7MM-SIM"}}
  Estimated development time: {{3-6 months / 6-12 months / 12+ months}}
  → {{assessment}}

Time finished: {{HH:MM}} (must be ≤ 30 min from start)
```

### Step 3: Yield — CEO Decision

Based on PRESTUDY answers, present recommendation:

```
Y — YIELD (GO / PARK / KILL)

SCORING:
  P (People):   {{GREEN/YELLOW/RED}}
  R (Revenue):  {{GREEN/YELLOW/RED}}
  E (Existing): {{GREEN/YELLOW/RED}}
  S (Skill):    {{GREEN/YELLOW/RED}}
  T (Timing):   {{GREEN/YELLOW/RED}}
  U (Unique):   {{GREEN/YELLOW/RED}}
  D (Decision): {{GREEN/YELLOW/RED}}

  GREEN count: {{N}}/7
  RED count:   {{N}}/7

DECISION RULES:
  ≥ 5 GREEN, 0 RED → Recommend GO
  ≥ 3 GREEN, ≤ 1 RED → Recommend GO with caveats
  2+ RED → Recommend PARK or KILL
  Any KILL criteria triggered → Recommend KILL

AI RECOMMENDATION: {{GO / PARK / KILL}} — {{1 sentence rationale}}

CEO: GO / PARK / KILL?
```

**IMPORTANT:** AI recommends, CEO DECIDES. This is a Core (C) judgment.

### Step 4: Route Output

**If GO:**
1. Save screening card to `0_Inbox/PRESTUDY_{{product_id}}_{{date}}.md`
2. Suggest: "Run `/helix-project-init {{product_name}}` to create project folder"
3. Suggest: "Run `/forge-job-map {{product_name}}` for full ODI analysis"
4. Log decision in `_meta/decisions.md`

**If PARK:**
1. Save screening card to `4_Archives/Pre-Study/PRESTUDY_{{product_id}}_{{date}}.md`
2. Log: reason for parking, revisit date, trigger condition
3. Add to `_meta/system-health.md` parked opportunities list

**If KILL:**
1. Save screening card to `4_Archives/Pre-Study/PRESTUDY_{{product_id}}_{{date}}.md`
2. Log: kill reason (which PRESTUDY criteria failed)
3. No further action

## MANDATORY Output Sections

```
1. SIGNAL — raw opportunity description + source
2. PRESTUDY CHECKLIST — all 7 answers (P-R-E-S-T-U-D)
3. YIELD — scoring + decision rules + recommendation
4. CEO DECISION — GO / PARK / KILL (CEO selects)
5. ROUTING — where to save + next action
```

## Integration

```
forge-pre-study READS FROM:
  - bridge-signal-extract → raw signals
  - bd-pulse → customer touchpoints
  - bridge-knowledge-base → existing product knowledge (avoid duplicates)
  - forge-portfolio → current product portfolio (capacity check)

forge-pre-study WRITES TO:
  - helix-project-init → if GO, triggers project creation
  - forge-job-map → if GO, next step in FORGE pipeline
  - _meta/decisions.md → decision log
  - 4_Archives/Pre-Study/ → if PARK or KILL
```

## Pipeline Position

```
BRIDGE signals → CEO triage → forge-pre-study (Stage -1, 30 min)
                                    ↓ GO
                              forge-job-map (Stage 0, 2-4h)
                              reverse-mc (Stage 0.5)
                              forge-scout (Stage 0)
                              forge-shift (Stage 1)
                                    ↓
                              helix-project-init (Phase 0)
```

## Rules

- **30 MINUTES MAX** — if you're spending more, you're doing analysis, not screening. Stop and decide with what you have.
- **NO deep research** — gut feeling + 1-minute web search per question. Save deep research for `/forge-job-map`.
- **AI recommends, CEO decides** — always end with "CEO: GO / PARK / KILL?"
- **Never skip KILL criteria** — if TAM < $100K or 0/3 Triple Helix → flag immediately.
- **Log everything** — even KILL decisions are valuable data (patterns of what WX rejects).

## Gotchas

1. **"Interesting" ≠ "Viable"** — Many signals are intellectually interesting but fail R (revenue) or S (skill fit). Pre-study catches this before wasting 4h on ODI.
2. **Sunk cost of asking** — Once you run `/forge-job-map`, there's psychological pressure to continue. Pre-study is the last cheap exit.
3. **PARK ≠ KILL** — Parking means "not now, but conditions may change." Always log the trigger condition for revisiting.
4. **Portfolio capacity** — As solo CEO, WX can handle ~3 Tier 1+2 projects. If at capacity, even a GREEN pre-study should PARK until a slot opens. Check `forge-portfolio` for current load.

## COD Classification

- PRESTUDY checklist execution: Offload (O2) — AI fills template, does quick searches
- GO/PARK/KILL decision: **Core (C)** — CEO judgment, accountable
- Routing and filing: Offload (O1) — deterministic
