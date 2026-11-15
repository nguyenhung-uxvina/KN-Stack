---
name: helix-p2-firmup
description: "Block BC2 of Phase 2 pipeline — CRUMPLE-S method-guided firming up of principle solutions. Diagnoses information gaps per concept, recommends methods (Calculations, Rough sketches, Unit experiments, Models, PC simulation, Literature, External research), generates task briefs with COD assignment. Can run standalone. Triggers on: 'firming up', 'firm up', 'CRUMPLE', 'cụ thể hóa', 'method selection', 'gap diagnosis'."
---

# Block BC2: Firming Up Principle Solutions — CRUMPLE-S Method-Guided

> **P&B:** 6.5.1 | **Pipeline:** helix-concept-generate → Block BC → delegates here from C2
> **Input:** `BB_Concept_Variants.md`, `BB_Morphological_Matrix.md` | **Output:** `BC_Firming_Up.md`
> **Galaxy:** [[Physical-World Interface]], [[Reliability Trumps Precision]]
> **Reference:** `helix-concept-generate/references/pb-conceptual-design.md` (P&B 6.5.1)
> **Learning ref:** `3_Resources/Books & Articles/Engineering Design/Ch6_Conceptual_Design/6.5.1 Firming_Up_MetaLearning_Analysis.md`

## Standalone Usage
```
/helix-p2-firmup {{project_id}}
```

## Input Requirements
- `BB_Concept_Variants.md` — surviving concept definitions (post-Pugh or all if ≤3)
- `BB_Morphological_Matrix.md` — WP details per sub-function
- `Requirements_List_v1.md` — requirements driving evaluation criteria
- Optional: `BC_Pugh_Screening.md` — if Pugh already run, use survivors only

## Core Principle

> **"Firming up ≠ detail design. Just enough to COMPARE."**
> — P&B 6.5.1: ~30% of final detail. Purpose = enable VDI 2225 scoring.

> **"Start with the CHEAPEST method that can answer the MOST IMPORTANT question."**
> — Escalation rule: Research → Calculate → Sketch → Simulate → Physical test

> **"Calculating and representation add up to 60% of total time spent on conceptual design."**
> — P&B 6.5.3: Firming up IS the heavy lift of Phase 2. Not a quick step.

> **"Verbal estimates (high/average/low) are preferable when data is uncertain. Numerical values introduce a false sense of certainty."**
> — P&B 6.5.2 Step 3: Use qualitative when quantitative is unreliable.

## Terminology
- **Property:** Observable attribute of a concept (e.g., weight, cost, reliability)
- **Gap:** Unknown value of a property. Severity: **U** = UNKNOWN (no data), **R** = ROUGH (guess only), **E** = ESTIMATED (adequate for VDI 2225)
- **Method:** CRUMPLE-S firming technique to reduce a gap
- **Criterion:** Property used in VDI 2225 scoring (subset of all properties)

---

## Workflow

### Step F0: Gap Diagnosis — What Do We NOT Know?

Read `BB_Concept_Variants.md`. For each surviving concept, assess property categories per P&B's 3 groups + WX extensions:

```
GAP DIAGNOSIS — {{project_id}}
Date: {{today}}
Concepts assessed: {{list concept names}}

PROPERTY CATEGORIES (P&B 3 groups + WX extensions):

GROUP 1 — Working Principle Characteristics (P&B 6.5.1):
  T1. Performance (key metric)
  T2. Reliability (MTBF estimate)
  T3. Fault susceptibility (failure modes)

GROUP 2 — Embodiment Characteristics (P&B 6.5.1):
  E1. Size (LxWxH envelope)
  E2. Weight estimate
  E3. Service life projection

GROUP 3 — Task-Specific Constraints (P&B 2.1.7):
  S1. Safety (MIL-STD, operational safety)
  S2. Ergonomics (human-machine interface)
  S3. Production/assembly feasibility
  M1. Unit cost (±30%) — qualitative OK if numbers unreliable
  M2. Development cost estimate

WX Extensions:
  V1. VN manufacturability (local capability)
  V2. VN supply chain (component availability)
  A1. ACH compensation potential (only if forge-shift = GO)

GAP MATRIX:
| Property | Concept A | Concept B | Concept C | Gap Type |
|----------|-----------|-----------|-----------|----------|
| T1       | [U/R/E]  | [U/R/E]  | [U/R/E]  | [type]   |
| T2       | [U/R/E]  | [U/R/E]  | [U/R/E]  | [type]   |
| ...      |          |          |          |          |

Gap severity: U = UNKNOWN (no data), R = ROUGH (guess only), E = ESTIMATED (adequate)
Gap type: force/spatial/dynamic/material/human/safety/cost/benchmark/environmental/ACH

SUMMARY:
- Total gaps (U + R): {{count}} across {{N}} concepts
- Critical gaps (U on high-weight criteria): {{list}}
- Gaps shared across ALL concepts: {{list}} → single investigation serves all
```

**Rule:** If a property is ESTIMATED for all concepts → skip it (no firming needed).
**Rule:** If a gap is shared across all concepts → investigate ONCE, apply to all.
**Rule (Selective Detailing — P&B 6.5.3):** Do NOT firm up all properties equally. Focus on properties that are ESSENTIAL for evaluation and concept selection. High detail only for: novel WPs, critical interfaces, safety elements. Lower detail for: standard COTS, well-understood components.
**Rule (Priority):** Cross-reference gap matrix with VDI 2225 criteria weights. High-weight criteria with UNKNOWN gaps = priority 1. Low-weight criteria with ROUGH gaps = can defer.

---

### Step F1: CRUMPLE-S Method Selection Matrix

For each gap from F0, recommend the appropriate firming method(s).

**CRUMPLE-S = 7 Methods for Firming Up (P&B 6.5.1):**

| Letter | Method | Vietnamese | Cost | Time | Best For |
|--------|--------|------------|------|------|----------|
| **C** | Calculations (rough, simplified) | Tính toán sơ bộ | $ | hours | Force, energy, stress, thermal, sizing |
| **R** | Rough sketches/scale drawings | Phác thảo tỷ lệ | $ | hours | Spatial arrangement, interfaces, fit |
| **U** | Unit experiments (preliminary tests) | Thử nghiệm sơ bộ | $$$ | days-weeks | Dynamic behavior, safety, human factors |
| **M** | Models (physical construction) | Mô hình vật lý | $$$ | days-weeks | Complex geometry, assembly verification |
| **P** | PC simulation (analogue/digital) | Mô phỏng máy tính | $$ | hours-days | Multi-physics, optimization, sensitivity |
| **L** | Literature & patent search | Tìm kiếm tài liệu | $ | hours | Benchmarks, existing solutions, prior art |
| **E** | External research (market) | Nghiên cứu thị trường | $ | hours-days | Component availability, cost data, suppliers |

**DECISION MATRIX — Which method for which gap type:**

```
METHOD SELECTION — {{project_id}}

| # | Gap | Gap Type | Primary | Fallback | Rationale |
|---|-----|----------|---------|----------|-----------|
```

Apply these rules:

| Gap Type | Primary Method | Fallback | Rationale |
|----------|---------------|----------|-----------|
| Force/stress/energy/thermal | **C** Calculation | **P** Simulation | Physics-first = cheapest verification |
| Spatial arrangement/interfaces | **R** Rough sketch | **M** Physical model | Visualize before committing to build |
| Dynamic/transient behavior | **P** PC simulation | **U** Unit experiment | Too complex for hand calc, too early for hardware |
| Material/component selection | **L** Literature + **E** Market | — | Don't reinvent — build on existing knowledge |
| Human factors/ergonomics | **U** Unit experiment | **M** Physical model | MUST test with real humans |
| Safety-critical properties | **U** Experiment MANDATORY | + **C** Calculation | Physical verification non-negotiable for defense |
| Cost estimation | **E** Market research | **L** Literature | Supplier quotes > engineering assumptions |
| Existing solution benchmarks | **L** Literature FIRST | **E** Market | Prior art reduces reinvention |
| Environmental tolerance | **P** Simulation | **U** Experiment | MIL-STD-810 methods define test approach |
| ACH/AI performance | **P** Simulation (data) | **U** Field experiment | Data-dependent — need representative dataset |
| Weight estimation | **C** Calculation | **R** Sketch (measure) | Sum of parts from BOM draft |
| Service life/fatigue | **C** Calculation | **L** Literature | S-N curves + duty cycle |

**ESCALATION RULE (Golden Path — cheap to expensive):**
```
L/E (research, $0-$) → C (calculate, $) → R (sketch, $) → P (simulate, $$) → U/M (physical, $$$)
Time:    hours          hours              hours           hours-days         days-weeks
```

**When to escalate:** If primary method yields uncertainty too high for VDI 2225 scoring (cannot distinguish 0 vs 4), escalate to fallback.

**SAFETY OVERRIDE:** For properties marked safety-critical in requirements → U/M is MANDATORY regardless of cost. Paper analysis alone is NEVER sufficient for defense safety properties.
- **U** (Unit Experiment) preferred: single-parameter gap (e.g., "Does sensor detect round at 2m?")
- **M** (Physical Model) preferred: multi-parameter assembly gap (e.g., "Can operator load magazine <5s?")
- **Both** required: safety-critical SF with 2+ dependent unknowns

**ESCALATION HALT RULE:** If 2 escalations yield uncertainty still > ±50% → flag as REMAINING UNKNOWN in F4. Do NOT pursue 3+ escalations — cost/benefit inverts. Accept the uncertainty and note it for VDI 2225 Step 7.

**ACH RULE:** If forge-shift = NO → skip A1 row entirely. If forge-shift = GO but A1 has high uncertainty → primary method = P (simulation with representative dataset).

---

### Step F2: Task Brief Generation

For each gap × recommended method, generate a specific task brief. Group by method type for batch efficiency.

```
═══ FIRMING-UP TASK BRIEFS — {{project_id}} ═══
Date: {{today}}
Total tasks: {{count}}

────────────────────────────────────────
GROUP L: LITERATURE & PATENT SEARCH
────────────────────────────────────────

TASK L-001: {{descriptive name}}
  Question:   {{What specific question does this answer?}}
  Concepts:   {{Which concepts benefit — often ALL}}
  Search scope: {{databases, keywords, patent classes}}
  Expected output: {{e.g., "Benchmark table: 5+ existing products with specs"}}
  Accuracy target: Comparative data (sufficient for VDI 2225 0-4 scoring)
  Time estimate: {{hours}}
  COD: [ ] Core  [ ] Offload  [ ] Skip

TASK L-002: ...

────────────────────────────────────────
GROUP E: EXTERNAL/MARKET RESEARCH
────────────────────────────────────────

TASK E-001: {{descriptive name}}
  Question:   {{e.g., "What servomotors are available in VN for ≤$500?"}}
  Concepts:   {{which concepts}}
  Search scope: {{suppliers, catalogs, contacts}}
  Expected output: {{e.g., "Supplier shortlist with specs + lead time + price"}}
  Accuracy target: ±20% on cost, confirmed availability
  Time estimate: {{hours}}
  COD: [ ] Core  [ ] Offload  [ ] Skip

**RESEARCH HOOK (L/E execution):** When CEO marks an L or E task **Offload**, do NOT
"compile options" from model memory. Convert the task brief into a Research Brief and call
`/helix-research`:
- `question` = task Question · `type` = prior-art (L) / market (E) · `phase` = P2
- `source_block` = helix-p2-firmup · `risk_if_wrong` = HIGH if the gap feeds a safety-critical
  or high-weight VDI 2225 criterion, else MEDIUM
- `known_sources` = charter-pinned topic-notebook aliases
The dispatcher proposes T1/T2/T3 (CEO approves T2/T3). Feed the Response's cited findings
back into the gap matrix; anything under **NOT FOUND** stays an open gap for F4 — never
fill it with uncited estimates.

────────────────────────────────────────
GROUP C: ROUGH CALCULATIONS
────────────────────────────────────────

TASK C-001: {{descriptive name}}
  Question:   {{e.g., "What launch force is needed for 25kg UAV at 20m/s?"}}
  Concepts:   {{which concepts}}
  Method:     {{formula/approach, e.g., "KE = ½mv², F = KE/d"}}
  Assumptions: {{list simplifying assumptions to state}}
  Expected output: {{e.g., "Force value ± range, comparison across concepts"}}
  Accuracy target: ±30% (order-of-magnitude sufficient)
  Time estimate: {{hours}}
  COD: [ ] Core  [ ] Offload  [ ] Skip

────────────────────────────────────────
GROUP R: ROUGH SKETCHES / SCALE DRAWINGS
────────────────────────────────────────

TASK R-001: {{descriptive name}}
  Question:   {{e.g., "Does the sensor array fit within the 1m² frame?"}}
  Concepts:   {{which concepts}}
  What to draw: {{specific arrangement, key dimensions to show}}
  Scale:      {{approximate, e.g., "1:10 on A3"}}
  Expected output: {{e.g., "Arrangement drawing showing component positions + envelope"}}
  Accuracy target: Spatial feasibility (fit/no-fit)
  Time estimate: {{hours}}
  COD: [ ] Core  [ ] Offload  [ ] Skip

────────────────────────────────────────
GROUP P: PC SIMULATION
────────────────────────────────────────

TASK P-001: {{descriptive name}}
  Question:   {{e.g., "What is the acoustic propagation pattern at 50m range?"}}
  Concepts:   {{which concepts}}
  Tool:       {{software — MATLAB, Python, ANSYS, etc.}}
  Model scope: {{what to model, boundary conditions}}
  Expected output: {{e.g., "Sensitivity curve, parameter sweep results"}}
  Accuracy target: Trend + order of magnitude (not final design values)
  Time estimate: {{hours}}
  COD: [ ] Core  [ ] Offload  [ ] Skip

────────────────────────────────────────
GROUP U: UNIT EXPERIMENTS (PRELIMINARY TESTS)
────────────────────────────────────────

TASK U-001: {{descriptive name}}
  Question:   {{e.g., "Does the piezo sensor detect 7.62mm at 2m distance?"}}
  Concepts:   {{which concepts}}
  Test setup: {{equipment, materials, location}}
  Procedure:  {{step-by-step — keep simple, ≤5 steps}}
  Expected output: {{e.g., "Signal amplitude vs distance curve"}}
  Accuracy target: Go/no-go + approximate performance range
  Time estimate: {{hours/days}}
  Resources:  {{materials, equipment, safety requirements}}
  COD: [ ] Core  [ ] Offload  [ ] Skip
  ⚠️ PHYSICAL — cannot delegate to AI

────────────────────────────────────────
GROUP M: PHYSICAL MODELS
────────────────────────────────────────

TASK M-001: {{descriptive name}}
  Question:   {{e.g., "Can operator load magazine in <5s with this arrangement?"}}
  Concepts:   {{which concepts}}
  Model type: {{foam mockup / 3D print / cardboard / scale model}}
  What to build: {{specific features to replicate}}
  Expected output: {{e.g., "Ergonomic assessment, assembly sequence verification"}}
  Accuracy target: Spatial + human factors validation
  Time estimate: {{hours/days}}
  Resources:  {{materials, tools, workshop access}}
  COD: [ ] Core  [ ] Offload  [ ] Skip
  ⚠️ PHYSICAL — cannot delegate to AI
```

**Batching rule:**
- L tasks → combine into 1 literature review session (CEO or AI)
- E tasks → combine into 1 market research session
- C tasks → combine into 1 calculation session (sequence matters: do shared-across-concepts first)
- R tasks → combine into 1 sketching session
- P tasks → may need separate sessions (different tools)
- U/M tasks → each standalone (physical setup overhead)

---

### Step F3: COD Assignment — CEO Checkpoint

Present the complete task list. CEO marks each task:

```
═══ COD ASSIGNMENT — {{project_id}} ═══

SUGGESTED COD (CEO overrides freely):

ALWAYS CORE (CEO must do):
- U/M tasks (physical experiments, models) — cannot delegate to AI
- Safety-critical assessments — CEO judgment required
- Design sketches requiring spatial intuition — Core skill development

TYPICAL OFFLOAD (AI can do):
- L tasks (literature/patent search) — AI excels at retrieval
- E tasks (market research/web search) — AI can compile options
- C tasks (rough calculations) — AI can draft, CEO validates
- P tasks (simulation setup) — AI can write scripts, CEO runs/validates

SKIP CANDIDATES:
- Properties where ALL concepts score similarly → won't affect VDI 2225 ranking
- Properties with low weight in evaluation criteria

CEO DECISION TABLE:
| Task ID | Description | Suggested COD | CEO Decision | Notes |
|---------|-------------|---------------|--------------|-------|
| L-001   |             | O             | [ C / O / D ] |      |
| E-001   |             | O             | [ C / O / D ] |      |
| C-001   |             | O             | [ C / O / D ] |      |
| R-001   |             | C             | [ C / O / D ] |      |
| P-001   |             | O             | [ C / O / D ] |      |
| U-001   |             | C (mandatory) | [ C / — / — ] |      |

SUMMARY:
- Core tasks: {{N}} (CEO does — estimated {{X}} hours)
- Offload tasks: {{M}} (AI does — estimated {{Y}} hours)
- Skipped: {{K}}

CEO:
(1) ✅ Approve COD assignments → AI starts Offload tasks
(2) ✏️ Modify assignments → reassign specific tasks
(3) ⏸️ Pause — need to schedule physical tests first
```

**STOP HERE. Wait for CEO approval before proceeding to F4.**
**Do NOT proceed to F4 (Results Compilation) until CEO approves COD assignments.**
**Do NOT auto-execute Offload tasks without explicit CEO go-ahead.**

---

### Step F4: Results Compilation

After Core tasks completed by CEO and Offload tasks completed by AI:

1. **Collect all results** into unified property table:

```
FIRMING-UP RESULTS — {{project_id}}
Date: {{today}}
Iteration: {{1st / 2nd / 3rd}}

| Property | Concept A | Concept B | Concept C | Method Used | Confidence |
|----------|-----------|-----------|-----------|-------------|------------|
| T1. Performance | {{value or HIGH/AVG/LOW}} | {{value or H/A/L}} | {{value or H/A/L}} | {{C/L/P/...}} | {{H/M/L}} |
| T2. Reliability  | {{value}} | {{value}} | {{value}} | {{method}} | {{H/M/L}} |
| T3. Faults       | {{value}} | {{value}} | {{value}} | {{method}} | {{H/M/L}} |
| E1. Size         | {{LxWxH}} | {{LxWxH}} | {{LxWxH}} | {{R/C}} | {{H/M/L}} |
| E2. Weight       | {{kg}}    | {{kg}}    | {{kg}}    | {{C/R}} | {{H/M/L}} |
| E3. Service life | {{hrs}}   | {{hrs}}   | {{hrs}}   | {{C/L}} | {{H/M/L}} |
| M1. Unit cost    | {{$±30%}} | {{$±30%}} | {{$±30%}} | {{E/L}} | {{H/M/L}} |
| M2. Dev cost     | {{$±30%}} | {{$±30%}} | {{$±30%}} | {{E}} | {{H/M/L}} |
| V1. Mfg-ability  | {{1-4}}   | {{1-4}}   | {{1-4}}   | {{E/L}} | {{H/M/L}} |
| V2. Supply chain | {{1-4}}   | {{1-4}}   | {{1-4}}   | {{E}} | {{H/M/L}} |
| A1. ACH ready    | {{1-4}}   | {{1-4}}   | {{1-4}}   | {{P}} | {{H/M/L}} |

Confidence: H = High (multiple methods agree), M = Medium (single method, reasonable),
            L = Low (rough estimate, high uncertainty — flag for VDI 2225 Step 7)

VALUE FORMAT (P&B 6.5.2 Step 3):
- Use NUMBERS when data is reliable (e.g., "35 kg", "$2,500 ±30%")
- Use VERBAL ESTIMATES when data is uncertain: HIGH / AVERAGE / LOW
  P&B warns: "Numerical values are dangerous because they introduce a false sense of certainty"
- Economic properties: qualitative OK if costs can't be figured ("high / moderate / low")
```

2. **Remaining gaps check:**
```
REMAINING UNKNOWNS:
| Property | Concept(s) | Why unresolved | Impact on VDI 2225 |
|----------|-----------|----------------|-------------------|
| {{prop}} | {{concept}} | {{reason}} | {{can/cannot score}} |

ITERATION NEEDED? {{YES/NO}}
If YES: Return to F0 with updated gap matrix (2nd iteration)
P&B allows 2-3 selection-firming cycles for complex systems.

ITERATION DECISION RULES:
- ITERATE (2nd pass) IF: ≥3 gaps still UNKNOWN on high-weight criteria
- ITERATE (3rd pass) IF: 2nd iteration resolved <50% of unknowns AND concepts still indifferentiable
- STOP IF: VDI 2225 readiness = READY, OR cost/schedule prevents further investigation
- MAX: 3 iterations. After 3rd, accept remaining unknowns and note in VDI 2225 Step 7.
```

3. **VDI 2225 readiness assessment:**
```
VDI 2225 READINESS CHECK:
- [ ] All high-weight criteria can be scored (0-4) for all concepts
- [ ] Cost estimates available (±30% sufficient)
- [ ] No safety-critical property is UNKNOWN
- [ ] Concepts are differentiable (not all identical scores)

VERDICT: {{READY / NEEDS MORE FIRMING / NEEDS PHYSICAL TEST}}
```

Save to `1_Projects/{{project}}/Phase2-Concept/BC_Firming_Up.md`

---

## CEO Checkpoint (End of Skill)

```
═══ BLOCK BC2 FIRMING UP COMPLETE ═══
Gaps diagnosed: {{total}} across {{N}} concepts
Tasks generated: {{count}} (L:{{n}} E:{{n}} C:{{n}} R:{{n}} P:{{n}} U:{{n}} M:{{n}})
Tasks completed: Core {{N}} + Offload {{M}} + Skipped {{K}}
Gaps resolved: {{X}}/{{Y}} ({{%}})
Remaining unknowns: {{list or "none"}}
VDI 2225 readiness: {{READY / NEEDS MORE FIRMING / NEEDS PHYSICAL TEST}}

NEW IDEAS LOG (P&B 6.5.3: "a completely new idea for a working principle
might emerge while making a rough layout"):
{{list any new WP ideas discovered during firming → route to BB_Morphological_Matrix}}

CEO:
(1) ✅ Approve → return to /helix-p2-develop Step C3 (ODI weights)
(2) 🔄 2nd firming iteration — resolve remaining gaps
(3) ⏸️ Pause — need physical test results before continuing
(4) 🔍 Review specific task results in detail
(5) 💡 New WP discovered → return to /helix-p2-search to update morphological matrix
```

---

## COD Classification (this skill overall)

| Activity | COD | Rationale |
|----------|-----|-----------|
| Gap diagnosis (F0) | **O** (Offload) | AI reads variants, flags unknowns |
| Method selection (F1) | **O** (Offload) | AI applies decision matrix, CEO validates |
| Task brief generation (F2) | **O** (Offload) | AI drafts, CEO reviews |
| COD assignment (F3) | **C** (Core) | CEO decides what to do vs delegate |
| Literature/market research | **O** (Offload) | AI excels at retrieval |
| Rough calculations | **O** (Offload) | AI drafts, CEO validates assumptions |
| Rough sketches | **C** (Core) | Spatial intuition = CEO skill development |
| Experiments/models | **C** (Core) | Physical work = non-delegable |
| Results compilation (F4) | **O** (Offload) | AI compiles, CEO checks |

---

## Error Patterns to Detect (from P&B 6.5.1 meta-learning analysis)

| Error | Detection | Correction |
|-------|-----------|------------|
| **Over-firming** | Detail exceeds ~30% of final design | Strip back: "just enough to score 0-4" |
| **Under-firming** | Cannot distinguish concepts in VDI 2225 | Add targeted firming on differentiating properties |
| **Premature optimization** | Firming focuses on 1 concept only | Parallel development — all survivors get equal effort |
| **Method mismatch** | Expensive test for simple question | Check escalation rule: did we skip cheaper methods? |
| **Ignoring economics** | Only technical properties firmed | Add cost/market tasks (E/L methods) |
| **Missing VN context** | Environmental/supply chain ignored | Add V1/V2 assessment (standard for WX products) |
| **Safety skip** | Safety-critical property estimated by calculation only | MANDATORY physical test (U/M) — no exceptions |
