---
name: odi
description: "Applies Outcome-Driven Innovation (Ulwick) and Jobs-to-be-Done (JTBD) framework adapted for Vietnam defense acquisition — captures operator outcomes first, quantifies opportunity gaps, then guides feature prioritization. Use at Phase 0 PreStudy or Phase 1 Task Clarification before locking requirements; do NOT use after CDR. Triggers on: \"ODI\", \"outcome driven\", \"jobs to be done\", \"JTBD\", \"customer outcome\", \"opportunity score\", \"operator needs\", \"xac dinh nhu cau nguoi dung\", \"phan tich nhu cau van hanh\", \"xác định nhu cầu thực sự\"."
skill: odi
version: 2.0.0
domain: design
created: 2026-05-22
nlm_notebook: ODI — Outcome-Driven Innovation + JTBD Framework
nlm_id: 5823c0a7-6dd9-4a98-8231-dd90c0a75348
---

# ODI — Outcome-Driven Innovation
## JTBD Framework × WX Defense Adaptation × Israeli Doctrine Lens

> **Core insight (Ulwick):** Customers don't buy products — they *hire* them to get a job done.
> Innovation fails 83% of the time because companies start with ideas, not outcomes.
> ODI flips the sequence: define outcomes first → quantify gaps → *then* ideate.
>
> **WX adaptation (Israeli lens):** In defense acquisition, the Job Executor is the *trắc thủ/operator*,
> not the BQP procurement office. Always capture outcomes from the operator first.

## When to Use

- Phase 0 PreStudy: before locking requirements — identify what job the operator is *really* trying to do
- Phase 1 Task Clarification: before writing FR/NFR — convert vague needs to measurable outcome statements
- Product strategy: deciding which features to build vs. kill based on opportunity scores
- Portfolio review: identifying underserved vs. overserved outcomes across product line
- Before customer interview: structure questions around outcomes, not solutions

**Do NOT use when:**
- Requirements already locked at CDR (Gold rule — SC-03)
- CEO asks for solution validation (ODI uncovers needs, not validates pre-decided solutions)

---

## Workflow (6 Steps)

### Step 1 — Define Job Executor + JTBD

**Purpose:** Identify WHO is trying to get the job done and WHAT the job is.

**WX Defense Rule — Three Customer Types (never conflate):**

| Role | WX Equivalent | What they provide |
|------|--------------|-------------------|
| **Job Executor** | Trắc thủ / operator / soldier | Desired outcomes — PRIMARY |
| **Buyer** | BQP procurement office | Financial metrics — SECONDARY |
| **Support** | Kỹ thuật viên / bảo trì | Consumption chain jobs (install, maintain) |

**Start always with Job Executor.** If you don't have executor access → this is BLOCKING (arrange via BQP).

**How to define the JTBD:**
```
Market = [Group of people] + [Core functional job they're trying to get done]

RIGHT: "Trắc thủ 12.7mm trying to detect and neutralize aerial threats before attack range"
WRONG: "Counter-UAV system users" (product-centric, not job-centric)
WRONG: "BQP defense procurement" (buyer, not executor)
```

**Abstraction level check:**
- Too narrow: "operate the gimbal" (product step, not job)
- Too broad: "defend the nation" (too abstract, unstable)
- CORRECT: "detect, classify, and neutralize approaching UAV/USV threats before they reach engagement range"

**Israeli Doctrine adaptation:** The job must be stated as an *operational need statement* — what the operator needs to *accomplish* in the field, independent of any system or technology. This is the "left of boom" requirement.

**Output:** Job statement in format: `[Group] trying to [core functional job]`

---

### Step 2 — Map the Job (Universal Job Map)

**Purpose:** Deconstruct the job into 8 universal steps to expose ALL points where operator struggles.

**The Universal Job Map (Ulwick):**

| Step | Verb Set | What to ask |
|------|----------|-------------|
| **1. DEFINE** | Plan, select, determine | What must be established before execution? |
| **2. LOCATE** | Gather, access, receive | What inputs/items must be found or acquired? |
| **3. PREPARE** | Set up, organize, examine | What must be configured before taking action? |
| **4. CONFIRM** | Validate, prioritize, decide | What must be verified before committing? |
| **5. EXECUTE** | Perform, transact, administer | What is the core action? |
| **6. MONITOR** | Verify, track, check | What must be watched during execution? |
| **7. MODIFY** | Update, adjust, maintain | What corrections are needed if monitor shows drift? |
| **8. CONCLUDE** | Store, finish, close | What happens after execution to close the cycle? |

**Example — VN-CUAS-001 (Counter-UAV/USV):**
```
Job: Detect, classify, and neutralize approaching threats before attack range

1. DEFINE    — Determine threat alert threshold, ROE boundaries, engagement authority
2. LOCATE    — Detect acoustic/visual/radar signature, obtain bearing + range
3. PREPARE   — Slew camera to bearing, verify field-of-view, ready FCS
4. CONFIRM   — Classify threat (UAV/USV/bird/vessel), verify hostile intent
5. EXECUTE   — Approve firing solution, engage with 12.7mm
6. MONITOR   — Track round impact, assess threat neutralization
7. MODIFY    — Adjust aim if missed, re-engage if threat continues
8. CONCLUDE  — Log engagement, reset system, report to command
```

**Output:** Job map table with 8 rows, each with 3-8 initial outcome ideas.

---

### Step 3 — Capture Outcome Statements (target: 50-150)

**Purpose:** For each job step, capture the measurable metrics operators use to judge success.

**Outcome Statement Formula (Ulwick canonical):**
```
[Direction] + [Metric] + [Object of control] + [Context clarifier]

Direction: Minimize / Maximize / Increase / Decrease / Reduce
Metric:    time / likelihood / frequency / number / amount / percentage / error
Object:    what specifically is being measured
Context:   under what conditions
```

**WRONG vs RIGHT examples:**

| WRONG (solution-contaminated / vague) | RIGHT (outcome statement) |
|---------------------------------------|--------------------------|
| "The system should be faster" | "Minimize time from acoustic alert to camera on-target" |
| "We need better radar" | "Minimize likelihood of false positive classification in sea noise" |
| "Easy to maintain" | "Minimize time required to replace acoustic sensor array in field" |
| "AI should be accurate" | "Minimize percentage of confirmed threats missed per engagement window" |
| "Reliable in tropical conditions" | "Minimize frequency of system failures during 8-hour continuous operation at 45°C" |

**Interview technique (Moesta method for niche defense markets — WX adaptation):**
- Never use a discussion guide — let operator narrate their struggle
- Ask: "Walk me through the last time you tried to [job]. What happened?"
- Listen for: pushes (struggle moments), pulls (what better would look like), anxieties, habits
- Write outcome statements IN REAL TIME — operator validates on screen
- Target: 10-15 good outcomes per interview × 7-12 interviews = 70-150 total

**Security filter (WX rule):** Outcome statements must be:
- Solution-neutral (no system names, technology names)
- Non-classified (measurable without revealing operational intelligence)
- Stable over time (won't change when the system changes)

**Output:** Outcome statement database, organized by job step (Step 3 → outcomes, Step 4 → outcomes, etc.)

---

### Step 4 — Quantify Importance + Satisfaction

**Purpose:** Measure which outcomes are underserved (important but unsatisfied) vs. overserved.

**Standard ODI method (for markets with 180+ accessible respondents):**

For each outcome statement, ask TWO questions on 1-5 scale:
```
Importance: "When [performing job], how important is it to [outcome statement]?"
            1=Not important → 5=Critically important

Satisfaction: "When using your current solution, how satisfied are you with your
               ability to [outcome statement]?"
              1=Not satisfied → 5=Completely satisfied
```

Convert to 10-point scale: % rating 4 or 5 × 10 = Score
Example: 92% rate 4-5 for importance → Importance score = 9.2

**WX Defense Adaptation — Small Sample / Classified Programs:**

When operator access is limited (<30 accessible, or classified program):
```
IF respondents < 30:
  → Use Moesta qualitative method: 7-12 deep switch interviews
  → Causal patterns repeat at 7-8 interviews (Dr. Deming validated)
  → Estimate scores from interview content: HIGH/MED/LOW mapping
  → Do NOT extrapolate to statistical confidence — flag as "qualitative estimate"

IF classified program:
  → Conduct interviews in cleared facility, no written transcripts
  → Map outcomes to qualitative opportunity tiers only
  → Mark all scores as "CE" (Classified Estimate) in output table
```

**Output:** Importance + Satisfaction score table for all 50-150 outcomes.

---

### Step 5 — Calculate Opportunity Scores + Build Opportunity Landscape

**Opportunity Algorithm (Ulwick, 2002):**
```
Opportunity = Importance + max(Importance − Satisfaction, 0)

Why max(…,0): High satisfaction never subtracts from importance.
Range: practical 5-16 typical; theoretical 0-20.
```

**Worked example:**
```
Outcome: "Minimize time from acoustic alert to camera on-target"
  Importance:   9.2 (92% rate 4-5)
  Satisfaction: 3.0 (30% rate 4-5 — current solutions poor)
  Opportunity:  9.2 + (9.2 - 3.0) = 15.4 → EXTREME
```

**Opportunity Score Decision Table:**

| Score | Classification | Action |
|:-----:|---------------|--------|
| > 15 | EXTREME opportunity | Highest priority — accelerate immediately |
| 12–15 | HIGH opportunity | Strong priority — fund |
| 10–12 | MODERATE opportunity | Second-tier — monitor |
| < 10 | LOW / OVERSERVED | Reduce investment; consider cost reduction |

**WX Mission-Critical Override (Israeli doctrine adaptation):**
```
IF outcome relates to operator safety OR mission failure = loss of life:
  → Auto-classify as Tier 0 (MUST address) regardless of opportunity score
  → Examples: "Minimize likelihood of friendly fire engagement"
              "Minimize time to abort engagement after ROE violation detected"
```

**Opportunity Landscape:** Plot all outcomes on scatter: X=Importance, Y=Satisfaction.
- Top-right: Table Stakes (high importance, high satisfaction — maintain, don't invest)
- Top-left: CRITICAL — underserved (high importance, low satisfaction — primary targets)
- Bottom-right: Overserved (low importance, high satisfaction — cost reduction candidates)
- Bottom-left: Non-issues

**Output:** Ranked opportunity table + Opportunity Landscape scatter plot.

---

### Step 6 — Segment + Growth Strategy

**Purpose:** Discover hidden segments with different underserved outcomes. Select growth strategy.

**Segmentation method (outcome-based, NOT demographic):**
```
1. Factor analysis: group 50-150 outcomes into 15-20 factors
2. K-means cluster analysis using OPPORTUNITY SCORES as clustering variable
3. Result: 3-6 segments with distinct patterns of underserved outcomes
4. Profile segments with demographics AFTER clustering (not before)
```

**WX Defense Segmentation — typical patterns:**
- Segment A: High-volume qualification (training throughput, cost per trainee)
- Segment B: Tactical realism (scenario fidelity, transfer of learning)
- Segment C: Export/simplified (maintenance simplicity, local support)

**Growth Strategy Selection:**

| Condition | Strategy |
|-----------|----------|
| High opportunity outcomes in existing market | **Sustaining** — add features to address underserved outcomes |
| Heavily overserved market segment | **Disruption** — enter with simpler, cheaper product |
| Job that customers can't get done at all | **New Market** — create product for underserved job |
| Multiple related jobs, platform opportunity | **Platform** — get entire job done on single architecture |

**Sequencing rule (Israeli: beachhead first):**
Start with the segment that is largest + least technically demanding → establish, then expand upward to premium/special operations segment.

**Output:** Segment map + Growth strategy recommendation + Priority outcome list per segment.

---

## Quality Criteria (Gate Check)

Run before handing outputs to Phase 1 / helix-task-clarify:

```
OUTCOME STATEMENTS (target: 50-150):
  □ Each follows [Direction] + [Metric] + [Object] + [Context] formula
  □ Zero solution-contamination (no technology names, system names)
  □ Each is measurable (engineer can design a test for it)
  □ Each is stable over time (independent of current solutions)
  □ Organized by Universal Job Map step

OPPORTUNITY SCORES:
  □ Importance + Satisfaction scores captured for all outcomes
  □ Algorithm applied correctly: Opp = Imp + max(Imp-Sat, 0)
  □ Mission-critical override applied where relevant
  □ Overserved outcomes identified (candidates for cost reduction)

JOB DEFINITION:
  □ Job executor correctly identified (operator, not buyer)
  □ Job stated at correct abstraction level (stable, not product-tied)
  □ Job map covers all 8 Universal Job Map steps

PROCESS COMPLETE WHEN:
  Can answer with quantitative confidence:
  (1) Who is the job executor?
  (2) What job are they trying to get done?
  (3) What are all 50-150 desired outcomes?
  (4) Which outcomes are underserved and by how much?
  (5) Do segments exist with different unmet needs?
```

---

## Gotchas (Top 5 Failure Modes)

**G1 — Solution-contaminated outcome statements**
> Symptoms: Statement contains a technology, product, or system name.
> Example WRONG: "Minimize time for AI to process acoustic signal"
> Example RIGHT: "Minimize time from threat sound event to bearing confirmation"
> Fix: Strip all solution references. Ask "WHY does that matter?" until you reach the metric.

**G2 — Confusing job vs. outcome**
> "Detect UAV" is the JOB (or a job step). "Minimize time to first detection of UAV at 2km range" is the OUTCOME.
> Fix: Job = what they're trying to accomplish. Outcome = metric for measuring success at each step.

**G3 — Wrong abstraction level for JTBD**
> Too narrow: captures only current product function → misses platform opportunity.
> Too broad: job can't be mapped into 8 concrete steps.
> Fix: Job must be decomposable into 8 Universal Job Map steps AND stable over 10+ years.

**G4 — Segmenting by demographics before outcomes**
> "Army vs Navy" or "tàu chiến vs nhà giàn" are demographic segments → create phantom segments.
> Fix: Run cluster analysis on opportunity scores first. Apply demographics ONLY to profile results.

**G5 — Capturing BQP requirements instead of operator outcomes**
> BQP writes specifications (solutions). Operators have outcomes (jobs to get done).
> Fix: Never substitute procurement documents for operator interviews. Always interview trắc thủ/operator directly.

**G6 — WX-specific: Skipping operator access because "BQP said so"**
> If BQP provides requirements without operator validation → treat as hypotheses, not facts.
> Fix: Outcomes from operators are ALWAYS primary. BQP financials are secondary buyer metrics.

---

## WX Defense Integration — Israeli Doctrine Lens

The Israeli Defense acquisition philosophy maps directly to ODI:

| Israeli Concept | ODI Equivalent |
|----------------|----------------|
| Operational Need Statement (ONS) | Job-to-be-Done definition |
| "What the soldier needs to accomplish" | Desired Outcomes (measurable metrics) |
| Combat-proven requirements | Outcomes validated by operators in field conditions |
| Detection Primacy | Underserved outcomes in LOCATE + CONFIRM job steps |
| Human-on-the-loop ROE | Outcomes in DECIDE step (operator approval flow) |
| "Combat user drives requirements" | Job Executor = trắc thủ, always interviewed first |
| Tech spec (engineering) | Solution — captured AFTER outcomes are locked |

**Key Israeli rule:** If outcomes are captured from procurement without combat-user validation, they are hypotheses. Run operator interviews before committing to any architecture.

---

## NLM Reference

- **Notebook:** ODI — Outcome-Driven Innovation + JTBD Framework
- **ID:** `5823c0a7-6dd9-4a98-8231-dd90c0a75348`
- **URL:** https://notebooklm.google.com/notebook/5823c0a7-6dd9-4a98-8231-dd90c0a75348
- **Sources:** 10 (Ulwick free book, Strategyn whitepaper, 4× YouTube, 2× Marketing Journal, Strategyn process guide, Innosight)
- **Created:** 2026-05-22 via `/research-to-skill`

**Query this notebook for:**
- Specific opportunity algorithm worked examples
- Universal Job Map detailed step definitions
- Case studies (Cordis, Motorola, Bosch, Kroll)
- Outcome statement conversion exercises

---

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Define Job Executor (Step 1) | **Core** | CEO judgment — who is the real customer |
| Write outcome statements (Step 3) | Offload | AI drafts, operator validates |
| Interview structuring | **Core** | CEO facilitates, CANNOT delegate |
| Opportunity score calculation (Step 5) | Offload | Math — AI executes |
| Growth strategy selection (Step 6) | **Core** | CEO decides which segment to pursue |
| Segmentation cluster analysis | Offload | Statistical analysis |

---

## Rules

- **Job Executor is always primary.** Never substitute buyer/procurement requirements for operator outcomes.
- **Outcomes must be solution-neutral.** Any statement containing a technology name is invalid.
- **50-150 outcomes per job** — fewer = incomplete map → missed opportunities guaranteed.
- **Small sample? Use Moesta 7-12 interviews** — qualitative patterns repeat reliably at 7-8. Flag all scores as "qualitative estimate."
- **Mission-critical override is non-negotiable** — operator safety outcomes are Tier 0 regardless of opportunity score.
- **Segment on outcomes, profile with demographics** — never the reverse.
- **No classified data in outcome statements** — measurable without revealing operational intelligence.
- **ODI outputs feed Phase 1** — opportunity landscape + ranked outcomes are direct inputs to `/helix-task-clarify`.
