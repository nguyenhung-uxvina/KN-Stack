---
name: reverse-mc
description: Build a Reverse Morphological Chart from existing competitor products to map the design space, identify uncontested gaps, and validate design decisions. Based on Hülagü & Timur (2024). Use when analyzing competitors, benchmarking products, finding market gaps, or preparing Phase 2 Conceptual Design input. Triggers on "reverse morphological", "competitor analysis MC", "design space mapping", "competitive morphological chart", "phân tích đối thủ MC", "bản đồ thiết kế", "gap analysis products", "analyze existing designs".
allowed_tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, Agent, TodoWrite
---

# Reverse Morphological Chart — Competitive Design Space Analysis

> **Method:** Hülagü, R. & Timur, Ş. (2024). "Using Morphological Chart for Analysing Existing Designs." *Archives of Design Research*, 37(1), 27-41.
> **Origin:** Zwicky, F. (1967). Morphological approach. Extended by Pahl & Beitz (2007) Ch. 6.
> **Innovation:** MC thông thường SINH ý tưởng (forward). Reverse MC PHÂN TÍCH sản phẩm hiện có (backward) → phát hiện design space gaps → inform new product design.

## When To Use

| Context | Framework | Position in Pipeline |
|---------|-----------|---------------------|
| **Competitive analysis cho sản phẩm mới** | FORGE Stage 0 | Sau `/forge-job-map`, trước `/forge-shift` |
| **Input cho Phase 2 Conceptual Design** | HELIX Phase 2 | Trước `/helix-concept-generate` (morphological matrix) |
| **Benchmarking sản phẩm existing** | Standalone | Bất kỳ lúc nào cần hiểu landscape |
| **Validate design decisions** | HELIX Phase 2-3 | Sau khi chọn concept, kiểm tra uniqueness |

## Usage

```
/reverse-mc <product-category> [--project <project-id>] [--ref-folder <path>] [--depth quick|standard|deep]
```

**Arguments:**
- `<product-category>`: Loại sản phẩm cần phân tích (e.g., "12.7mm gunnery simulator", "naval USV", "LOMAH system")
- `--project`: Project ID để link output (e.g., VN-12.7MM-SIM)
- `--ref-folder`: Thư mục chứa REF files đã có (skip Step 1 nếu có)
- `--depth`: quick (≤5 products, inline), standard (5-10), deep (10-20, full REF files)

---

## PIPELINE — 7 Steps

```
[1] COLLECT — Thu thập sản phẩm hiện có
     ↓
[2] DECOMPOSE — Xác định sub-functions từ tất cả sản phẩm
     ↓
[3] MAP — Đặt mỗi sản phẩm vào ma trận (solutions per sub-function)
     ↓
[4] ANALYZE — Frequency analysis, gap detection, cluster identification
     ↓
[5] POSITION — Đặt sản phẩm Workshop X vào ma trận, đánh giá uniqueness
     ↓
[6] RECOMMEND — Design decisions từ gap analysis
     ↓
[7] SAVE — Lưu MC + gap analysis vào project Ref/
```

---

## STEP 1: COLLECT EXISTING PRODUCTS

### If --ref-folder provided:
Read existing REF files → extract product data → skip to Step 2.

### If no REF files:
Run `/research <product-category>` to find competitors, OR ask CEO for known competitors.

**Minimum products:** 5 (quick mode), 10 (standard), 15+ (deep)

**For each product, collect:**
- Company, product name, country
- Key technical specifications
- Differentiating features
- Price range (if available)
- Patent/IP status

**Output:** Product list table for CEO confirmation.

```markdown
## Products Collected: {{N}}

| # | Company | Product | Country | Source |
|---|---------|---------|---------|--------|
| 1 | {{company}} | {{product}} | {{country}} | {{REF file or URL}} |
| ... | | | | |

CEO: Danh sách đủ chưa? Thêm/bớt sản phẩm nào?
```

**CEO gate:** Confirm product list before proceeding.

---

## STEP 2: DECOMPOSE INTO SUB-FUNCTIONS

### Method (Hülagü & Timur 2024, reversed):

**Forward MC (Pahl-Beitz):** Function structure → sub-functions → brainstorm solutions → matrix
**Reverse MC:** Analyze ALL products → extract ALL sub-functions they address → compile master list

### Process:

1. For EACH product, list every design dimension / feature / specification
2. Normalize terminology across products (same sub-function, different names)
3. Merge into master sub-function list
4. Filter: keep sub-functions where ≥2 products have DIFFERENT solutions (variation = interesting)
5. Target: 8-20 sub-functions (< 8 = too shallow, > 20 = unmanageable)

### Sub-function naming convention:
```
SF{{N}}: {{Verb}} + {{Object}} — {{one-line description}}
Example: SF1: Generate Recoil — Phương pháp tạo giật cho vũ khí mô phỏng
```

### Sub-function categories (guide, not mandatory):
- **Energy domain:** Power source, actuation, force generation
- **Material domain:** Structure, materials, form factor
- **Signal domain:** Sensing, display, data processing, AI
- **User domain:** Ergonomics, training mode, crew configuration
- **Business domain:** Deployment, maintenance, cost structure

**Output:**

```markdown
## Sub-Functions Identified: {{N}}

| SF# | Sub-Function | Mô tả | # Solutions Found |
|-----|-------------|--------|-------------------|
| SF1 | {{name}} | {{description}} | {{N}} |
| ... | | | |

CEO: Sub-functions đủ chưa? Thiếu dimension nào?
```

**CEO gate:** Confirm sub-function list. CEO may add domain-specific sub-functions AI missed.

---

## STEP 3: MAP PRODUCTS TO MATRIX

### For each sub-function, list ALL solutions found across ALL products:

```markdown
### SF{{N}}: {{Sub-Function Name}}

| Solution | Mô tả | Products Using | Count |
|----------|--------|----------------|-------|
| S{{N}}.1 | {{description}} | REF-01, REF-04 | 2 |
| S{{N}}.2 | {{description}} | REF-03, REF-07, REF-14 | 3 |
| S{{N}}.3 | {{description}} | — (none) | 0 |
| ... | | | |
```

### Rules:
- Every product MUST have exactly 1 solution per sub-function (or "N/A" if not applicable)
- If a product has a NOVEL solution not seen in others → add new solution row
- Solutions should be MUTUALLY EXCLUSIVE within a sub-function
- Order solutions by frequency (most common first)

### Full Product × Sub-Function Matrix:

Create a master table: rows = products, columns = sub-functions, cells = solution codes.

```markdown
| Product | SF1 | SF2 | SF3 | ... | SF{{N}} |
|---------|-----|-----|-----|-----|---------|
| REF-01  | S1.1 | S2.3 | S3.2 | ... | S{{N}}.1 |
| REF-02  | S1.4 | S2.1 | S3.5 | ... | S{{N}}.2 |
| ... | | | | | |
| **WX Product** | **S1.?** | **S2.?** | **S3.?** | ... | **S{{N}}.?** |
```

---

## STEP 4: ANALYZE — Gap Detection & Frequency Analysis

### 4.1 Frequency Analysis (per sub-function)

For each sub-function, count how many products use each solution:

```
SF1 {{name}} — Distribution:
S1.1 {{solution}}: ████ (4/15) — COMMON
S1.2 {{solution}}: ██ (2/15)
S1.3 {{solution}}: █ (1/15) — RARE
S1.4 {{solution}}: ZERO — GAP
```

### 4.2 Gap Detection

Three types of gaps:

| Gap Type | Definition | Significance |
|----------|-----------|-------------|
| **Solution Gap** | Sub-function has NO solution from any product | New solution opportunity |
| **Combination Gap** | Solution exists but NEVER combined with another specific solution | Novel combination |
| **Market Gap** | Sub-function solution exists but no one serves a specific market | Market entry opportunity |

### 4.3 Cluster Analysis

Identify groups of products that share similar solution patterns:

```
Cluster A (Premium): REF-01, REF-03, REF-10 — electric recoil + projection + 6-DOF
Cluster B (Budget): REF-06, REF-07 — pneumatic + basic visual + individual
Cluster C (Kit/Addon): REF-05, REF-14 — drop-in + no visual + tetherless
```

### 4.4 Design Space Size

Calculate total theoretical combinations:
```
Design Space = ∏(solutions per sub-function)
             = SF1_solutions × SF2_solutions × ... × SFN_solutions
             = {{number}}

Products explored: {{N}} ({{percentage}}% of design space)
```

### 4.5 Patent/FTO Overlay

For each sub-function, mark solutions with patent risk:
```
SF1: S1.1 Electric motor — 🔴 ACME patent US10001338
SF1: S1.3 Pneumatic — ✅ SAFE (prior art)
```

**Output:**

```markdown
## ANALYSIS RESULTS

### Uncontested Spaces (Solution Gaps)
| SF# | Solution | Competitors | Opportunity |
|-----|----------|------------|-------------|
| {{SF}} | {{solution}} | **0/{{N}}** | {{description}} |

### Crowded Spaces (> 50% products)
| SF# | Solution | # Products | Risk |
|-----|----------|-----------|------|
| {{SF}} | {{solution}} | {{N}} | High competition |

### Novel Combinations (never combined)
| SF-A Solution | SF-B Solution | Products with both | Opportunity |
|-------------|-------------|-------------------|-------------|
| {{S_A}} | {{S_B}} | **0** | {{description}} |

### Design Space
- Total theoretical combinations: {{N}}
- Products analyzed: {{N}} ({{%}} explored)
- Cluster count: {{N}}

### FTO Summary
- SAFE solutions: {{N}}/{{total}}
- PATENT RISK solutions: {{N}}/{{total}} (avoid)
```

---

## STEP 5: POSITION WORKSHOP X PRODUCT

Map the Workshop X product (existing or proposed) into the matrix:

```markdown
## Workshop X Product: {{name}}

### Solution Selection
| SF# | Sub-Function | WX Solution | Gap? | Unique? | FTO |
|-----|-------------|------------|------|---------|-----|
| SF1 | {{name}} | {{solution}} | {{Y/N}} | {{Y/N}} | {{SAFE/RISK}} |
| ... | | | | | |

### Uniqueness Score
- Sub-functions with UNIQUE solution: {{N}}/{{total}} ({{%}})
- Combination match with any competitor: {{YES/NO}}
- Closest competitor: {{name}} ({{N}}/{{total}} SF match)

### Position Assessment
{{One paragraph: where does WX product sit in the design space?
Is it in uncontested space? Crowded space? Novel combination?}}
```

**CEO gate:** CEO reviews positioning. May adjust solutions for uncontested positioning.

---

## STEP 6: RECOMMEND DESIGN DECISIONS

Based on gap analysis, recommend:

```markdown
## RECOMMENDATIONS

### Validated Decisions (gap confirms uniqueness)
| # | Decision | MC Evidence |
|---|---------|-------------|
| 1 | {{decision}} | SF{{N}}: 0/{{total}} competitors use this → uncontested |

### New Opportunities (gaps to explore)
| # | Opportunity | Gap Type | Action |
|---|-----------|---------|--------|
| 1 | {{opportunity}} | Solution Gap | {{what to do}} |
| 2 | {{opportunity}} | Combination Gap | {{what to do}} |

### Warnings (crowded spaces to differentiate)
| # | Warning | Crowded SF | Differentiation Strategy |
|---|---------|----------|------------------------|
| 1 | {{warning}} | SF{{N}} | {{how to stand out}} |

### Input for HELIX Phase 2
{{If using for concept generation:}}
- Use these {{N}} gaps as starting points for morphological matrix
- Avoid solutions in crowded spaces unless differentiation clear
- FTO-safe solutions: {{list}}

### Input for FORGE Stage 0
{{If using for competitive positioning:}}
- Uncontested spaces validate product-market fit
- {{N}} competitors in adjacent space — monitor
- Price positioning: below {{cheapest}} but above {{bottom}}
```

---

## STEP 7: SAVE OUTPUT

Save to: `1_Projects/{{project-id}}/Ref/MORPHOLOGICAL_CHART_Competitive_Analysis_{{date}}.md`

**Frontmatter:**
```yaml
---
created: {{today}}
type: morphological-chart-analysis
method: "Reverse Morphological Chart (Hülagü & Timur 2024)"
product: "{{product-name}}"
products_analyzed: {{N}}
sub_functions: {{N}}
design_space_size: {{N}}
uncontested_gaps: {{N}}
uniqueness_score: "{{N}}/{{total}} ({{%}})"
status: active
---
```

---

## INTEGRATION WITH EXISTING SKILLS

### FORGE Pipeline Position
```
/forge-job-map → /forge-scout → /reverse-mc → /forge-shift → /forge-validate
                                     ↑
                        Competitive landscape input
                        "Where is NO ONE competing?"
```

### HELIX Pipeline Position
```
/helix-task-clarify → /reverse-mc → /helix-concept-generate → /helix-embody-realize
                          ↑                    ↑
                  Competitor MC         Forward MC (concept generation)
                  (what exists)         (what to create IN THE GAPS)
```

### Key Relationship: Reverse MC → Forward MC
- **Reverse MC** answers: "What design space is already explored?"
- **Forward MC** (Pahl-Beitz) answers: "What solutions should we generate?"
- **Connection:** Reverse MC gaps = Forward MC focus areas
- **Rule:** Never generate concepts in crowded spaces without clear differentiation

---

## RULES

- **MANDATORY:** Step 2 CEO gate — CEO must confirm sub-function list. AI may miss domain-specific dimensions.
- **MANDATORY:** Step 5 CEO gate — CEO must review positioning before recommendations.
- **Minimum products:** 5 (quick), 10 (standard), 15+ (deep). Below 5 = insufficient design space mapping.
- **Sub-function count:** Target 8-20. Below 8 = too shallow. Above 20 = split into sub-charts.
- **Mutually exclusive solutions:** Each product has exactly 1 solution per sub-function. No overlaps.
- **Frequency analysis is NON-NEGOTIABLE.** Every Step 4 must include distribution bars.
- **FTO overlay is NON-NEGOTIABLE** for engineering products. Skip only for non-patentable domains.
- **Design space size calculation** — always compute and report. Puts human perspective on exploration.
- **"0/N competitors" = uncontested** — this is the PRIMARY output. If no gaps found, design space is saturated.
- **Reverse MC ≠ feature comparison.** Feature comparison = "who has what." Reverse MC = "what design space exists and where is nobody."
- **COD:** Step 1-4 = Offload (O). Step 5-6 = Core (C — CEO positioning decisions). Step 7 = Offload (O).
- **Link to Galaxy:** [[Variation vs Simplification]], [[Solution-Determining Subfunction]], [[Analyst Trap]]

## REFERENCES

- Hülagü, R. & Timur, Ş. (2024). Using Morphological Chart for Analysing Existing Designs. *Archives of Design Research*, 37(1), 27-41.
- Zwicky, F. (1967). The Morphological Approach to Discovery, Invention, Research and Construction.
- Pahl, G. & Beitz, W. (2007). Engineering Design: A Systematic Approach. Springer. Ch. 6.
- Börekçi, N. A. (2018). Design Divergence Using the Morphological Chart.
- Tiwari, S. et al. (2007). Genetic algorithm based procedure for extracting optimal solutions from a morphological chart.
- Jones, J. C. (1992). Design Methods.
