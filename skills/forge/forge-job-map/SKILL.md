---
name: forge-job-map
description: Map customer jobs-to-be-done, generate desired outcome statements, and run opportunity analysis for a product. This skill should be used when the user asks about "customer needs", "job map", "desired outcomes", "ODI", "JTBD", "khách hàng cần gì", "outcome mapping", "opportunity landscape", or wants to understand what customers hire a product to do. Stage 0 of FORGE — feeds into forge-scout, forge-shift, and helix-task-clarify.
---

# Forge Job Map — Customer Job-to-be-Done Mapping

Map the customer's job-to-be-done, generate 50-100 desired outcome statements, score Importance × Satisfaction, and run the Opportunity Algorithm. Output: Job Map (8 steps), Outcome Landscape, and Strategy Recommendation. Defense-adapted for Vietnam military context.

## When to Use

- Before forge-scout (demand-side input for ACH opportunity discovery)
- When entering a new market or customer segment
- When product has user complaints or low adoption despite meeting specs
- Annual/bi-annual per product (customer jobs shift slowly)
- When user asks "khách hàng cần gì?", "why don't they use our product?", "job map"

## Workflow

### Step 1: Define the Job-to-be-Done (Core — CEO + Customer)

The job is NOT the product. The job is what the CUSTOMER is trying to accomplish.

```
JOB STATEMENT FORMAT:
  [Action verb] + [object of action] + [contextual clarifier]

EXAMPLES:
  ✅ "Phát hiện và theo dõi mục tiêu di chuyển trong khu vực tác chiến"
  ✅ "Huấn luyện xạ thủ đạt chuẩn bắn chính xác trong mọi điều kiện"
  ✅ "Đánh giá kết quả bắn đạn thật trên bia mục tiêu"

  ❌ "Dùng V-SMASH" (product, not job)
  ❌ "Mua hệ thống giám sát" (purchase, not job)
  ❌ "Nâng cấp công nghệ" (means, not end)
```

**Defense context:** Interview OPERATORS (lính, sĩ quan vận hành), NOT procurement officers. Buyer ≠ user. Specs reflect buyer's language; jobs reflect user's reality.

**Output:** Job statement + related jobs + emotional/social jobs

### Step 2: Build 8-Step Job Map (Core → Offload)

Walk through HOW the customer does the job today. Use the universal 8-step structure:

```
JOB MAP — {{product}} / {{customer segment}}
Date: {{today}}

┌─────────────────────────────────────────────────────────────┐
│ Step 1: DEFINE — Xác định cần làm gì                       │
│   What triggers the job? How do they decide to start?       │
│   "Nhận lệnh giám sát khu vực X trong Y giờ"               │
├─────────────────────────────────────────────────────────────┤
│ Step 2: LOCATE — Tìm input cần thiết                       │
│   What inputs, materials, information do they gather?       │
│   "Tìm thiết bị trong kho, kiểm tra pin, phụ kiện"         │
├─────────────────────────────────────────────────────────────┤
│ Step 3: PREPARE — Chuẩn bị                                 │
│   How do they set up for execution?                        │
│   "Vận chuyển đến vị trí, lắp đặt, canh chỉnh"            │
├─────────────────────────────────────────────────────────────┤
│ Step 4: CONFIRM — Xác nhận sẵn sàng                        │
│   How do they verify everything is ready?                  │
│   "Test chức năng, kết nối mạng, calibrate"                │
├─────────────────────────────────────────────────────────────┤
│ Step 5: EXECUTE — Thực hiện                                │
│   The core execution of the job                            │
│   "Giám sát mục tiêu, theo dõi cảnh báo"                  │
├─────────────────────────────────────────────────────────────┤
│ Step 6: MONITOR — Theo dõi kết quả                         │
│   How do they track progress during execution?             │
│   "Kiểm tra chất lượng hình ảnh, pin, kết nối"            │
├─────────────────────────────────────────────────────────────┤
│ Step 7: MODIFY — Điều chỉnh nếu cần                       │
│   What changes do they make during the job?                │
│   "Điều chỉnh vùng giám sát, ngưỡng cảnh báo"            │
├─────────────────────────────────────────────────────────────┤
│ Step 8: CONCLUDE — Kết thúc                                │
│   How do they finish and clean up?                         │
│   "Thu hồi, bảo dưỡng, báo cáo kết quả"                  │
└─────────────────────────────────────────────────────────────┘
```

**👤 CEO conducts** workshop/interview with 6-12 users to fill this map.
**🤖 AI structures** the raw notes into the 8-step format.

### Step 3: Generate Desired Outcome Statements (Offload → Core review)

For EACH step in the job map, generate outcome statements:

```
OUTCOME STATEMENT FORMAT:
  [Minimize/Maximize] + [metric] + [context]

EXAMPLES (per job step):
  Step 3 PREPARE:
    "Minimize the time it takes to set up the system at a new position"
    "Minimize the number of people needed for installation"
    "Minimize the weight of equipment to carry to position"

  Step 5 EXECUTE:
    "Minimize the false alarm rate in rain conditions"
    "Minimize the time from target appearance to detection alert"
    "Maximize the detection range in low-light conditions"

  Step 8 CONCLUDE:
    "Minimize the time to pack and transport after mission"
    "Minimize maintenance required between deployments"
```

**Target: 50-100 outcomes per product.** For defense (smaller user base): 30-50 acceptable.

🤖 AI generates draft outcomes from job map + product knowledge.
👤 CEO validates: "Would an operator actually say this? Is this measurable?"

**MANDATORY:** Deduplicate, categorize by job map step, format consistently.

### Step 4: Survey — Importance × Satisfaction (Core — CEO conducts)

For each outcome, ask users:

```
SURVEY FORMAT:
  "Outcome: Minimize the time it takes to set up at a new position"

  Importance (1-5): How important is this to you?
    1 = Not important at all
    5 = Extremely important

  Satisfaction (1-5): How satisfied are you with current solution?
    1 = Not satisfied at all
    5 = Extremely satisfied
```

**Defense adaptation:**
- ODI suggests 180+ respondents. Defense reality: 15-30 users.
- Use structured interviews instead of mass surveys
- 3-5 deep interviews can substitute for 30 surveys if users are domain experts
- Classified outcomes: focus on unclassified operational outcomes (setup, maintenance, training) — these are often the MOST underserved

**Output:** Importance × Satisfaction score per outcome

### Step 5: Run Opportunity Algorithm (Offload — deterministic)

```
OPPORTUNITY SCORE = Importance + max(Importance - Satisfaction, 0)

Scale: 0-10
  ≥ 8.0: HIGHLY UNDERSERVED → ★ top innovation target
  6.0-7.9: UNDERSERVED → innovation opportunity
  4.0-5.9: SERVED → maintain, don't over-invest
  ≤ 3.9: OVERSERVED → cost reduction candidate (ACH!)

OPPORTUNITY LANDSCAPE — {{product}}
Date: {{today}}

UNDERSERVED (top 15 — invest here):
| Rank | Outcome | Job Step | Imp | Sat | Opp Score |
|------|---------|----------|-----|-----|-----------|
| 1 | {{outcome}} | {{step}} | 4.8 | 1.9 | 9.6 |
| 2 | ... | | | | |

OVERSERVED (bottom 15 — reduce cost here):
| Rank | Outcome | Job Step | Imp | Sat | Opp Score |
|------|---------|----------|-----|-----|-----------|
| 1 | {{outcome}} | {{step}} | 2.1 | 4.5 | 2.1 |
```

### Step 6: Strategic Implications (Offload → Core decision)

```
STRATEGY RECOMMENDATION — {{product}}

Based on opportunity landscape:

1. INNOVATION TARGETS (underserved outcomes):
   {{list top 5 outcomes + which sub-functions address them}}

2. ACH CANDIDATES (overserved → reduce cost with AI):
   {{list overserved outcomes where ACH can maintain quality at lower cost}}

3. STRATEGY TYPE:
   [ ] Differentiated — target underserved outcomes (charge premium)
   [ ] Dominant — serve ALL outcomes comprehensively
   [ ] Discrete — simplify overserved features, lower cost
   [ ] Disruptive — new approach gets MORE of the job done

4. OUTCOME × ACH CROSS-REFERENCE:
   {{underserved outcome}} → ACH can address? YES/NO
   If YES → ★ HIGH PRIORITY for forge-scout

5. OUTCOME × REQUIREMENTS BRIDGE:
   {{underserved outcome}} → design requirement for helix-task-clarify
   "Minimize setup time" → "R-XX: Field setup < 8 min by 1 person [D]"

CEO: chọn strategy type và confirm innovation targets.
```

### Step 7: Save and Route

Save to `1_Projects/{{project}}/Phase0-Init/`:
- `Job_Map.md` — 8-step job map
- `Desired_Outcomes.md` — full outcome list with scores
- `Opportunity_Landscape.md` — ranked outcomes + strategy

Route outputs:
```
forge-job-map FEEDS:
├── forge-scout → underserved outcomes as ACH opportunity filter (Step 0)
├── forge-shift → "O" in SHIFTO (outcome-aligned?)
├── forge-validate → customer-defined outcome metrics for validation
├── forge-trust → evidence framed in outcome language
├── forge-cost → overserved outcomes = cost reduction candidates
├── helix-task-clarify → outcome-derived requirements
└── bridge-knowledge-base → Layer 2: customer job data per product
```

## MANDATORY Output Sections

Every /forge-job-map run MUST contain ALL of these:

```
1. JOB STATEMENT — verb + object + context (1-2 sentences)
2. JOB MAP — 8-step table with Vietnamese examples
3. DESIRED OUTCOMES — ≥30 outcome statements, categorized by job step
4. OPPORTUNITY SCORES — Importance × Satisfaction with Opportunity Algorithm
5. UNDERSERVED TOP 15 — ranked table
6. OVERSERVED BOTTOM 15 — ranked table
7. STRATEGY RECOMMENDATION — type + innovation targets + ACH candidates
8. CEO SELECTION — "CEO: chọn strategy type và confirm targets"
```

## HOQ Design Parameter Weights — HELIX Phase 2 Export (Mayda & Borklu 2014)

After generating outcomes and opportunity scores, construct a formal House of Quality (HOQ) to derive weighted design parameters for HELIX Phase 2 VDI 2225 evaluation.

### HOQ Construction Process (Weiss & Hari 2015 — Modified)

**Practical limits:** Keep HOQ to ≤15 outcomes (rows) × ≤12 design parameters (columns). Larger matrices are impractical — select the most important/controversial items.

**Step H1: Map outcomes → design parameters (DPs)**
- Group related outcomes into design parameters
- Example: O-26 (recoil fidelity) + O-27 (traverse feel) → DP: "Haptic Fidelity"
- Target: 6-12 design parameters

**Step H2: Build HOQ matrix with correlation grades**
For each outcome × design parameter intersection, assign correlation:
- **A = 9** — Strong: this DP directly determines outcome satisfaction
- **B = 5** — Moderate: this DP significantly contributes
- **C = 3** — Weak: this DP has minor influence
- **D = 1** — Possible: indirect or conditional influence
- Blank — no correlation

```
HOQ MATRIX — {{project_id}}

                        Design Parameters
                    DP1    DP2    DP3    DP4    ...
Outcomes   Imp
O-{{N}}    {{W}}   A/B/C/D  ...
O-{{M}}    {{W}}   ...
...

W_TP(j) = Σ (W_Gi × F_ij)     ← Absolute importance per DP
R_j = W_TP(j) / Σ W_TP × 100  ← Relative importance (%)
Norm = R_j / 100               ← Normalized weight (0-1) for VDI 2225
```

**Step H3: Calculate design parameter weights**
- Absolute importance: W_TP(j) = Σ [Outcome_importance × Correlation_grade]
- Relative importance: R_j = W_TP(j) / Σ W_TP(j) × 100
- Normalized (0-1): Used directly as VDI 2225 criterion weights
- Rank by R_j — top 3 = highest priority design challenges

**Step H4: Build correlation roof — contradiction detection**
For each pair of DPs, assess interaction:
- **(+)** Positive: improving DP-A also improves DP-B → synergy
- **(-)** Negative: improving DP-A WORSENS DP-B → **CONTRADICTION** → feeds TRIZ Step 0.5
- **(0)** No correlation

**Step H5: Identify "Other characteristics" (Weiss 2015)**
Add a column for characteristics that matter but aren't in the top 12. This prevents losing important factors that don't fit the matrix size.

**Output tables (MANDATORY when project proceeds to HELIX Phase 2):**

```
DESIGN PARAMETER WEIGHTS — {{project_id}}

| DP# | Design Parameter | Source Outcomes | W_TP | R_j (%) | Weight (0-1) | Priority |
|-----|-----------------|----------------|------|---------|-------------|----------|
| DP1 | {{parameter}} | O-{{N}}, O-{{M}} | {{sum}} | {{%}} | {{norm}} | {{H/M/L}} |

Total: Σ weights = 1.00

CORRELATION ROOF (Contradiction Detection):
|     | DP1 | DP2 | DP3 | DP4 | ... |
|-----|-----|-----|-----|-----|-----|
| DP1 | —   |     |     |     |     |
| DP2 | +/0/- | — |     |     |     |
| DP3 | +/0/- | +/0/- | — |   |     |

CONTRADICTIONS DETECTED:
| # | DP-A | DP-B | Nature | → TRIZ Contradiction |
|---|------|------|--------|---------------------|
| K1 | {{DP}} | {{DP}} | {{explanation}} | {{TRIZ param pair}} |

OTHER CHARACTERISTICS (not in matrix):
| Characteristic | Relevant Outcomes | Note |
|---------------|------------------|------|
| {{char}} | O-{{N}} | {{why excluded / monitor in Phase 3}} |
```

Save to: `1_Projects/{{project}}/Phase2-Concept/HOQ_Design_Parameters_v1.0.md`
Contradictions (marked -) feed into `/helix-concept-generate` Step 0.5 TRIZ analysis.
Weights feed into `/helix-concept-generate` Step 3.5 ODI import.

---

## Gotchas (from ODI/JTBD literature + defense context)

1. **Buyer ≠ User** — Procurement officer writes specs. Operator lives the job. Always interview operators, not buyers. Specs and jobs diverge significantly in defense. (Source: ODI Impact Assessment)
2. **"Minimize" outcomes only** — Ulwick's format is ALWAYS "minimize time/effort/likelihood." Never "maximize quality" (vague). If you write "maximize," convert: "maximize accuracy" → "minimize error rate." (Source: Ulwick, What Customers Want)
3. **Small sample ≠ invalid** — Defense may have 15 users, not 180. Use expert-weighted interviews. 3 deep interviews with experienced operators > 30 surveys with recruits. (Source: defense adaptation)
4. **Overserved = ACH gold mine** — Most teams only look at underserved. Overserved outcomes = features customers don't value highly but cost a lot. Replace with cheaper AI solution = margin improvement without losing customer. (Source: ACH × JTBD compound insight)
5. **Step 5 bias** — Workshop X instinctively focuses on EXECUTE (Step 5). But biggest opportunities often in PREPARE (Step 3) and CONCLUDE (Step 8). Always map ALL 8 steps. (Source: E2E Workflow blueprint)

## Rules

- Job definition is **Core** — CEO/product lead MUST talk to actual users
- AI generates draft outcomes but CEO validates ("Would operator say this?")
- Opportunity Algorithm is deterministic — AI calculates, no judgment needed
- Strategy selection is **Core** — CEO decides differentiated/dominant/discrete/disruptive
- Re-run annually or when major market shift (new competitor, new requirement, new customer segment)
- Link to Galaxy: [[Solution Bias Removal — Performance Budget Thay Vendor Name]] — outcomes are solution-neutral by design
- Link to Galaxy: [[Phán đoán không thể uỷ thác cho AI]] — job definition requires human judgment
- **Investment Type column** in opportunity table: tag each opportunity `S` (Structural — hardware/architecture) or `SW` (Software — algorithm/UX) to guide resource allocation
- **HITL Safety Rule:** HITL-mandatory / safety-critical outcomes never classified OVERSERVED unless satisfaction ≥9 — never reduce safety requirements based on opportunity score
- **Evidence tagging on outcomes:** `[FIELD-VALIDATED]` > `[EXPERT-ESTIMATE]` > `[ASSUMPTION]` — explicitly flag assumptions, prioritize field-validated outcomes in strategy decisions
- **VN procurement context (when segmenting):** include procurement authority + operational role analysis, not just geography — defense buyers cluster by MoD procurement authority, not region

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Job statement definition | **C** | CEO + customer conversation |
| Job map workshop | **C** | CEO conducts with users |
| Outcome statement generation | O | AI drafts from job map |
| Outcome validation | **C** | CEO checks: "Would operator say this?" |
| Survey design | O | Standard format |
| Survey execution | **C** | CEO/team conducts interviews |
| Opportunity Algorithm | O | Deterministic calculation |
| Strategy recommendation | O | AI proposes from landscape |
| Strategy selection | **C** | CEO decides |
| Routing to downstream skills | O | Automated feeds |
