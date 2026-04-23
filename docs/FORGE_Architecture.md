# FORGE SKILL ARCHITECTURE v2
## Bộ Skill Đầy Đủ Theo Giai Đoạn Sản Phẩm — Phối Hợp Người-AI × HELIX Integration

**Ngày:** 01/03/2026
**Bối cảnh:** FORGE = chiều thứ 2 trong Compound Law (BRIDGE × FORGE × HELIX). Hiện tại 31% (7.8/25 = RAW ORE). FORGE quản lý PORTFOLIO & PRODUCT STRATEGY; HELIX quản lý EXECUTION mỗi dự án bên trong.
**Mục tiêu:** Thiết kế bộ skill phản ánh vòng đời sản phẩm ACH — từ cơ hội → portfolio → validation → reuse → moat — với ranh giới người-AI rõ ràng và điểm tích hợp chính xác với HELIX.

---

## I. FORGE vs. HELIX: HAI TẦNG CỦA CÙNG HỆ THỐNG

### Vấn Đề Hiện Tại

FORGE (product strategy) và HELIX (design execution) hiện tại KHÔNG NÓI CHUYỆN VỚI NHAU:

```
HIỆN TẠI:
┌───────────────────────────────────────────────────┐
│ FORGE (product strategy)                          │
│ CEO biết: "V-SMASH cần ACH cho detection"         │
│ CEO KHÔNG biết: "Team đang ở Phase 2 hay 3?"      │
│                 "ICD có cập nhật với ACH decision?" │
│                 "Model library có entry mới chưa?"  │
└───────────────────────────────────────────────────┘
        ↑ GAP: không có handoff protocol ↑
┌───────────────────────────────────────────────────┐
│ HELIX (design execution)                          │
│ Team biết: "Đang làm embodiment design V-SMASH"    │
│ Team KHÔNG biết: "ACH opportunity nào đã approve?"  │
│                  "Fallback requirement ở đâu?"      │
│                  "Model có reuse potential không?"   │
└───────────────────────────────────────────────────┘
```

### Thiết Kế Mới: FORGE Wraps HELIX

```
FORGE PRODUCT LIFECYCLE (CEO-level):

Stage 0        Stage 1         Stage 2         Stage 3         Stage 4
OPPORTUNITY    ACH DESIGN      VALIDATION      REUSE &         MOAT &
DISCOVERY      DECISIONS       & TRUST         COMPOUND        EVOLUTION
┌──────────┐  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ forge-   │─▶│ forge-   │──▶│ forge-   │──▶│ forge-   │──▶│ forge-   │
│ scout    │  │ shift    │   │ validate │   │ library  │   │ evolve   │
└──────────┘  └──────────┘   └──────────┘   └──────────┘   └──────────┘
                   │              │                │
                   ▼              ▼                ▼
              ┌──────────────────────────────────────────┐
              │    HELIX DESIGN EXECUTION               │
              │    (Phase 0→1→2→3→4 per project)        │
              │    helix-project-init → task-clarify → …│
              └──────────────────────────────────────────┘
                   │              │                │
                   ▼              ▼                ▼
              ┌──────────────────────────────────────────┐
              │    FORGE CROSS-STAGE SKILLS              │
              │  forge-portfolio │ forge-cost │ forge-   │
              │  -dashboard      │ -reality   │ flywheel │
              └──────────────────────────────────────────┘

KEY DIFFERENCE:
  FORGE = "WHAT products to build, WHICH ACH to apply, HOW to compound"
  HELIX = "HOW to execute each product's design process"
  
  FORGE operates at PORTFOLIO + PRODUCT level (CEO + product lead)
  HELIX operates at PROJECT + TASK level (engineering team)
```

### Cùng Sản Phẩm, Hai Lenses

```
V-SMASH qua lens FORGE:                V-SMASH qua lens HELIX:
─────────────────────                   ─────────────────────
"ACH opportunity ở đâu?"               "Requirements list xong chưa?"
"Model nào reuse được?"                 "Function structure dùng 6-flow?"
"Fallback Level mấy?"                  "ICD giữa camera-board-algorithm?"
"Cost so với hardware alternative?"     "DfX check embodiment passed?"
"Customer trust evidence?"              "Monthly sync S5 đã chạy?"
"Data pipeline active?"                 "Integration Debt trend?"
```

---

## II. HUMAN-AI COLLABORATION MODEL CHO FORGE

FORGE decisions mang tính CHIẾN LƯỢC hơn HELIX → vai trò người NẶNG hơn.

| Ký hiệu | Vai trò | Ví dụ FORGE |
|:--------:|---------|-------------|
| 🤖 | **AI Generates** | Scrape market data, calculate cost models, track portfolio metrics |
| 👤 | **Human Generates** | Customer insights, strategic vision, trust relationships |
| 🤖→👤 | **AI Draft → Human Decides** | SHIFT assessment → CEO approve/reject ACH |
| 👤→🤖 | **Human Specifies → AI Executes** | "Track V-SMASH model performance" → AI dashboard |

**Nguyên tắc phân công FORGE:**

```
AI LÀM TỐT:                              NGƯỜI PHẢI LÀM:
──────────────                             ──────────────────
✓ Run SHIFT checklist (template)           ✗ Quyết định GO/NO-GO ACH
✓ Calculate ACH economics                  ✗ Customer trust building (relationship)
✓ Track model library inventory            ✗ Strategic portfolio prioritization
✓ Monitor model performance drift          ✗ Decide when to HALT a product
✓ Generate cost comparison reports         ✗ Identify NEW ACH opportunities (insight)
✓ Cross-reference product synergies        ✗ Negotiate with defense customers
✓ Draft validation test plans              ✗ Accept risk on defense deployment
✓ Alert: model degradation detected        ✗ Decide: retrain, fallback, or recall?
✓ Track competitive landscape              ✗ Set organizational identity direction
✓ Generate local content reports           ✗ Government/military relationship mgmt
```

---

## III. BỘ SKILL ĐẦY ĐỦ: 10 SKILLS

### Tổng Quan

| # | Skill Name | Stage | Mục đích | Vai trò chính |
|:-:|-----------|:-----:|----------|:-------------:|
| 1 | `forge-scout` | 0 | Phát hiện cơ hội ACH trong portfolio | 🤖→👤 |
| 2 | `forge-shift` | 1 | Đánh giá ACH Go/No-Go | 🤖→👤 |
| 3 | `forge-fallback` | 1 | Thiết kế fallback architecture | 🤖→👤 |
| 4 | `forge-validate` | 2 | Validation infrastructure & test | 👤→🤖 |
| 5 | `forge-trust` | 2 | Customer trust evidence building | 👤 (lead) + 🤖 (track) |
| 6 | `forge-library` | 3 | Model library management & reuse | 🤖→👤 |
| 7 | `forge-flywheel` | 3-4 | Data flywheel & compound tracking | 🤖 (track) + 👤 (steer) |
| 8 | `forge-portfolio` | Cross | Portfolio dashboard & prioritization | 🤖→👤 |
| 9 | `forge-cost` | Cross | Edge-realistic defense cost analysis | 🤖→👤 |
| 10 | `forge-evolve` | 4 | Competitive moat & identity evolution | 👤 (lead) + 🤖 (support) |

---

## IV. CHI TIẾT TỪNG SKILL

---

### SKILL 1: `forge-scout` — Phát Hiện Cơ Hội ACH

**Stage:** 0 (trước khi có ACH decision)
**Trigger:** "tìm cơ hội ACH", "scout ACH", "sản phẩm nào dùng AI thay hardware?", "ACH opportunities", "scan portfolio"

**Workflow:**

```
Input: Product portfolio + existing morphological matrices (nếu có)
  │
  ▼
Step 1: 🤖 Portfolio scan
  │     ├── List tất cả sản phẩm + sub-functions
  │     ├── Cho mỗi sub-function, check: "hardware có thể thay bằng AI?"
  │     │   ├── Sensor-based functions → HIGH potential
  │     │   ├── Computation-based functions → HIGH potential
  │     │   ├── Mechanical-only functions → LOW potential
  │     │   └── Safety-critical functions → MEDIUM (needs fallback)
  │     ├── Score: ACH Potential Matrix (Product × Sub-function)
  │     └── Highlight: "5 highest-potential ACH opportunities"
  │
  ▼
Step 2: 🤖 Cross-product synergy map
  │     ├── "Sub-function A trong V-SMASH ≈ sub-function B trong LOMAH"
  │     ├── "Cùng model type có thể serve 3 products"
  │     ├── Generate: Synergy Graph (which products share AI needs)
  │     └── Score: Reuse Multiplier (1 model → N products)
  │
  ▼
Step 3: 👤 Strategic filter
  │     ├── CEO xem ACH Potential Matrix + Synergy Graph
  │     ├── Filter by: customer urgency, funding available, team capacity
  │     ├── "Opportunity X tốt trên giấy nhưng customer chưa sẵn sàng"
  │     ├── "Opportunity Y nhỏ nhưng unlock 3 downstream products"
  │     └── Select: Top 3-5 opportunities → push to forge-shift
  │
  ▼
Output: ACH Opportunity Matrix + Synergy Graph + CEO-prioritized shortlist
```

**HELIX Integration:**
```
forge-scout READS FROM HELIX:
├── helix-6flow-mapper: "Function structure nào đã có?" → scout dùng functions đó
├── helix-task-clarify: "Requirements nào liên quan đến AI capability?"
└── helix-project-init: "Products nào đã có project charter?"

forge-scout WRITES TO HELIX:
├── "ACH opportunity identified for sub-function X" → tags in helix-task-clarify
└── "Reuse potential: model from Product A applicable to Product B" → cross-project note
```

**AI Generates:**
- Portfolio scan from product database
- Synergy graph from sub-function similarity analysis
- Preliminary scoring based on SHIFT criteria (quick-pass)
- Comparison with FORGE model library ("model này đã có → easy ACH")

**Human Must:**
- Strategic prioritization (market timing, customer relationship, funding)
- Identify opportunities AI can't see (field observations, customer hints, geopolitical shifts)
- Capacity allocation decision ("team chỉ có 25h/week — chọn 2, không phải 5")

---

### SKILL 2: `forge-shift` — Đánh Giá ACH Go/No-Go

**Stage:** 1 (decision point — most critical FORGE skill)
**Trigger:** "đánh giá ACH", "SHIFT", "go no-go", "có nên dùng AI thay hardware?", "ACH assessment"

**Workflow:**

```
Input: Specific sub-function + product context from forge-scout
  │
  ▼
Step 1: 🤖 Run SHIFT Checklist
  │     ├── S — SUBSTITUTABLE?
  │     │   ├── Physics test: "Information present trong cheap data?"
  │     │   ├── Evidence: search papers, patents, existing implementations
  │     │   └── Score: ✅ Yes / ⚠️ Maybe / ❌ No
  │     │
  │     ├── H — HYBRID POSSIBLE?
  │     │   ├── "AI + cheap sensor vs. expensive specialized sensor?"
  │     │   ├── List candidate hybrid architectures
  │     │   └── Score: ✅/⚠️/❌
  │     │
  │     ├── I — IMPROVEMENT TRAJECTORY?
  │     │   ├── dA/dt: AI capability growth rate for this task
  │     │   ├── dH/dt: hardware improvement rate
  │     │   ├── Crossover estimate: "AI surpasses hardware by 20XX"
  │     │   └── Score: ✅ dA/dt >> dH/dt / ⚠️ comparable / ❌ hardware faster
  │     │
  │     ├── F — FALLBACK FEASIBLE?
  │     │   ├── Level 0: No fallback → ❌ STOP cho defense
  │     │   ├── Level 1: Manual override available → ⚠️ acceptable
  │     │   ├── Level 2: Graceful degradation → ✅ good
  │     │   ├── Level 3: Redundant path → ✅✅ excellent
  │     │   └── Score + flag: "Fallback architecture cần design" → forge-fallback
  │     │
  │     └── T — TRAINING DATA?
  │         ├── Available: existing datasets, field data
  │         ├── Creatable: synthetic generation feasible?
  │         ├── Collectable: field collection plan?
  │         └── Score: ✅ rich / ⚠️ moderate / ❌ scarce
  │
  ▼
Step 2: 🤖 ACH Economics Quick-Check (link to forge-cost for full analysis)
  │     ├── Hardware alternative cost (defense-realistic, not consumer)
  │     ├── ACH solution cost (compute + sensor + development + validation)
  │     ├── Breakeven volume estimate
  │     ├── ★ Capability premium: "ACH enables feature X impossible with hardware"
  │     └── ★ Reuse value: "Model serves N products" (from forge-scout synergy)
  │
  ▼
Step 3: 🤖→👤 Decision Package
  │     ├── SHIFT scorecard: S/H/I/F/T each ✅/⚠️/❌
  │     ├── Economics summary: cost/capability/reuse
  │     ├── Risk assessment: "what fails if this fails?"
  │     ├── Recommendation: GO / CONDITIONAL GO / NO-GO
  │     └── Conditions (if conditional): "needs fallback design first" etc.
  │
  ▼
Step 4: 👤 CEO Decision
  │     ├── Review SHIFT scorecard
  │     ├── Factor in: customer relationship, political context, team morale
  │     ├── ★ GUT CHECK: "Nếu AI fail ở sản phẩm này, hậu quả gì?"
  │     │   ├── "Lose a contract" → recoverable → acceptable risk
  │     │   ├── "Lose trust with MoD" → catastrophic → need Level 2+ fallback
  │     │   └── "Safety incident" → unacceptable → NO-GO unless Level 3 fallback
  │     └── DECISION: GO / NO-GO / GO with conditions
  │
  ▼
Output: SHIFT Assessment Report + CEO Decision + Conditions (if any)
```

**HELIX Integration:**
```
forge-shift READS FROM HELIX:
├── helix-6flow-mapper: function structure → identifies WHERE AI replaces hardware
├── helix-task-clarify: requirements → "requirement X demands >95% accuracy"
└── helix-concept-generate: "concept already includes ACH?" → validate or update

forge-shift WRITES TO HELIX:
├── "ACH APPROVED for sub-function X" → becomes REQUIREMENT in helix-task-clarify
├── "Fallback Level 2 required" → becomes CONSTRAINT in helix-task-clarify
├── "Model WX-DET-001 applicable" → informs helix-concept-generate solution space
└── "Training data plan needed" → becomes task in helix-project-init
```

**AI Generates:**
- SHIFT checklist auto-populated from product context + prior assessments
- Economics quick-check from cost database
- Risk assessment from template + product class
- Evidence search (papers, patents, competitive products using similar AI)

**Human Must:**
- GO/NO-GO decision (accountability — person who signs off)
- Risk acceptance calibration (defense context: stakes, politics, relationships)
- Strategic sequencing ("even if GO technically, timing wrong for this customer")

---

### SKILL 3: `forge-fallback` — Thiết Kế Kiến Trúc Dự Phòng

**Stage:** 1 (after SHIFT → GO, before HELIX Phase 2)
**Trigger:** "thiết kế fallback", "fallback architecture", "degradation mode", "AI fail thì sao?", "backup plan"

**Workflow:**

```
Input: SHIFT Assessment (approved) + fallback level requirement
  │
  ▼
Step 1: 🤖 Generate fallback architecture options
  │     ├── Level 1: Manual Override
  │     │   └── "Operator có thể bypass AI và điều khiển manual"
  │     │       Requirements: switch, manual interface, training
  │     │
  │     ├── Level 2: Graceful Degradation
  │     │   └── "AI fail → system degrades to simpler mode"
  │     │       Ví dụ: AI object detection fail → system fallback to motion detection
  │     │       Requirements: degradation logic, threshold definitions
  │     │
  │     ├── Level 3: Redundant Path
  │     │   └── "Dual system: AI primary + traditional secondary"
  │     │       Ví dụ: AI tracker + mechanical backup tracker
  │     │       Requirements: voting logic, switchover criteria
  │     │
  │     └── For each level: estimate cost, weight, complexity impact
  │
  ▼
Step 2: 👤 Select fallback level + architecture
  │     ├── Balance: cost vs. safety vs. customer expectation
  │     ├── Defense context: higher stakes → higher level
  │     ├── ★ "Fallback phải THỰC SỰ HOẠT ĐỘNG, không chỉ trên giấy"
  │     └── DECISION: Level + specific architecture
  │
  ▼
Step 3: 🤖→👤 Generate fallback specification
  │     ├── Fallback trigger conditions (when does system switch?)
  │     ├── Degradation behavior (what does system DO in fallback?)
  │     ├── Recovery path (how does system return to AI mode?)
  │     ├── Test plan: how to VERIFY fallback actually works
  │     └── ★ Integration requirements → feed into HELIX ICD
  │
  ▼
Output: Fallback Architecture Spec → HELIX ICD input + test requirements
```

**HELIX Integration:**
```
forge-fallback WRITES TO HELIX:
├── Fallback spec → helix-task-clarify (new requirements)
├── Fallback interface → helix-integration-debt (ICD entry: IF-AI-FALLBACK)
├── Fallback trigger logic → helix-6flow-mapper (Trust flow path)
├── Fallback test plan → helix-quality-gate (Gate 3 checklist addition)
└── Weight/cost/complexity impact → helix-concept-generate (evaluation criteria)

★ CRITICAL: Fallback design CHANGES the product architecture.
  forge-fallback MUST trigger helix-sync-protocol if design is in Phase 2+
  "New fallback requirement → ICD change → all domains affected"
```

---

### SKILL 4: `forge-validate` — Validation Infrastructure

**Stage:** 2 (after design decisions, before/during production)
**Trigger:** "validation", "test AI", "prove it works", "performance envelope", "defense test"

**Workflow:**

```
Input: ACH design (from HELIX Phase 3-4) + SHIFT assessment + fallback spec
  │
  ▼
Step 1: 🤖 Generate validation plan
  │     ├── Stage 1: Lab Validation
  │     │   ├── Controlled environment tests
  │     │   ├── Known inputs → expected outputs
  │     │   ├── Edge case matrix (worst case scenarios)
  │     │   └── Baseline comparison: AI vs. hardware alternative
  │     │
  │     ├── Stage 2: Field Simulation
  │     │   ├── Realistic conditions but controlled setup
  │     │   ├── Environmental variables: weather, lighting, vibration
  │     │   ├── Adversarial testing (deception, jamming, countermeasures)
  │     │   └── Fallback trigger testing
  │     │
  │     ├── Stage 3: Operational Field Test
  │     │   ├── Real environment, real operators
  │     │   ├── Extended duration (burn-in, drift detection)
  │     │   ├── User feedback collection
  │     │   └── Comparison with operational requirements
  │     │
  │     └── Stage 4: Continuous Monitoring (post-deployment)
  │         ├── Telemetry pipeline active
  │         ├── Performance drift detection
  │         ├── Automatic alert if performance drops below threshold
  │         └── Quarterly revalidation schedule
  │
  ▼
Step 2: 👤 Execute validation (PHYSICAL — AI cannot do this)
  │     ├── Set up test environment
  │     ├── Run tests, collect data
  │     ├── Observe behaviors AI metrics miss (operator confusion, ergonomic issues)
  │     └── Document anomalies and edge cases
  │
  ▼
Step 3: 🤖 Analyze validation results
  │     ├── Statistical analysis: confidence intervals, failure rates
  │     ├── Performance Envelope generation
  │     │   ├── "Works well: conditions A, B, C"
  │     │   ├── "Works but degraded: conditions D, E"
  │     │   └── "FAILS: conditions F, G → fallback activates"
  │     ├── Compare vs. requirements: PASS/FAIL per requirement
  │     └── Generate: Validation Report (defense-grade documentation)
  │
  ▼
Step 4: 👤 Accept/reject validation results
  │     ├── "Performance Envelope acceptable for customer?"
  │     ├── "Edge cases covered?"
  │     ├── "Fallback tested and working?"
  │     └── DECISION: VALIDATED / NEEDS MORE TESTING / REJECT
  │
  ▼
Output: Validation Report + Performance Envelope + Continuous Monitoring Setup
```

**HELIX Integration:**
```
forge-validate READS FROM HELIX:
├── helix-detail-finalize: manufacturing drawings → what EXACTLY is being tested
├── helix-quality-gate: Gate 4 passed? → prerequisite for Stage 1 validation
├── helix-integration-debt: all interfaces resolved? → validation covers interfaces
└── helix-design-journal: known issues → test plan covers them

forge-validate WRITES TO HELIX:
├── Validation results → helix-design-journal (evidence log)
├── "Performance Envelope" → helix-task-clarify for NEXT product revision
├── Anomalies found → helix-integration-debt (if interface-related)
└── "Stage 4 telemetry needs" → helix-embody-realize Phase 3 (DfU requirement)

★ CRITICAL SYNC POINT:
  HELIX Sync S5 ("First hardware available for AI testing")
  = forge-validate Stage 1 START trigger
  
  Before S5: AI team can only run simulation validation
  After S5: forge-validate Stage 1-2 becomes possible
  CEO must ensure S5 happens on time → if delayed, AI validation delayed → product delayed
```

---

### SKILL 5: `forge-trust` — Customer Trust Evidence

**Stage:** 2-3 (parallel with validation, feeds into market)
**Trigger:** "customer trust", "demo", "evidence", "chứng minh cho khách", "defense customer"

**Workflow:**

```
Input: Validation results (from forge-validate) + customer context
  │
  ▼
Step 1: 🤖 Generate trust evidence package
  │     ├── Performance Envelope summary (customer-facing version)
  │     ├── Comparison: ACH vs. hardware alternative (transparent)
  │     ├── Fallback architecture explanation (reassurance)
  │     ├── Continuous monitoring dashboard (real-time evidence)
  │     └── Case study: successful field deployment (if available)
  │
  ▼
Step 2: 👤 Customer engagement (NON-DELEGABLE)
  │     ├── Present evidence to customer (face-to-face preferred)
  │     ├── LISTEN: what concerns does customer have?
  │     ├── Demonstrate live system (hands-on experience)
  │     ├── Invite customer to witness validation testing
  │     └── ★ "Trust builds linearly, collapses exponentially"
  │         → Every interaction either builds or erodes
  │
  ▼
Step 3: 🤖 Track trust metrics
  │     ├── Customer engagement log (meetings, demos, questions)
  │     ├── Concern tracking: "customer worried about X" → addressed? resolved?
  │     ├── Trust trajectory: trending up/down/flat
  │     └── Alert: "Customer Z hasn't seen update in 60 days" → trust decay risk
  │
  ▼
Output: Trust Evidence Package + Customer Engagement Log + Trust Metrics
```

**Human Must:**
- ALL customer-facing interactions (trust is human-to-human)
- Understanding unspoken concerns (political, career-risk, organizational)
- Relationship management across customer organization (not just technical PoC)
- Deciding WHEN to show what (premature demo of unstable system destroys trust)

**AI Does:**
- Package evidence into professional, clear documentation
- Track engagement timeline and flag gaps
- Generate comparison materials
- Monitor public/industry signals about competitors

---

### SKILL 6: `forge-library` — Model Library & Reuse

**Stage:** 3 (after validation, enables compound)
**Trigger:** "model library", "reuse model", "transfer learning", "thư viện mô hình", "cross-product model"

**Workflow:**

```
Input: Validated model from a product + model metadata
  │
  ▼
Step 1: 🤖 Catalog model into library
  │     ├── Model ID: WX-[TYPE]-[NUMBER] (e.g., WX-DET-001)
  │     ├── Type: Detection / Classification / Tracking / Prediction / Control
  │     ├── Input spec: sensor type, resolution, format
  │     ├── Output spec: data format, latency, accuracy
  │     ├── Performance Envelope: where it works / doesn't
  │     ├── Training data description
  │     ├── Validation evidence reference
  │     ├── Source product: which product created this model
  │     └── Reuse potential: which other products could use it
  │
  ▼
Step 2: 🤖 Cross-product matching
  │     ├── Scan portfolio: "Product Y has sub-function similar to this model"
  │     ├── Estimate transfer effort: fine-tune vs. retrain vs. direct use
  │     ├── Score: Transfer Readiness (1-5)
  │     └── Alert CEO: "WX-DET-001 potentially applicable to LOMAH-AD, OVERWATCH"
  │
  ▼
Step 3: 👤 Transfer decision
  │     ├── "Worth the effort to transfer?" (team capacity, timeline)
  │     ├── "Product Y ready to receive?" (HELIX Phase check)
  │     ├── "Customer for Product Y would accept transferred model?"
  │     └── DECISION: Transfer approved / defer / not applicable
  │
  ▼
Step 4: 👤→🤖 Execute transfer (if approved)
  │     ├── Fine-tuning plan (data, compute, timeline)
  │     ├── Validation plan for new context
  │     ├── Integration spec for receiving product's HELIX ICD
  │     └── Track: time saved, cost saved, performance delta
  │
  ▼
Output: Model Library entry + Cross-product match report + Transfer plan
```

**HELIX Integration:**
```
forge-library READS FROM HELIX:
├── helix-6flow-mapper: function structure → "which functions need AI models?"
├── helix-concept-generate: "concept evaluation should include library models as options"
├── helix-integration-debt: "model interface spec matches ICD?"
└── helix-quality-gate: "validation passed?" → prerequisite for library entry

forge-library WRITES TO HELIX:
├── "Model WX-DET-001 available" → helix-concept-generate solution space expanded
├── "Model requires input X, output Y" → helix-integration-debt ICD spec
├── "Model transfer to Product B" → helix-project-init for Product B
└── "Performance Envelope of model" → helix-task-clarify requirements calibration

★ R5 ACTIVATION:
  forge-library is the mechanism that activates R5 (Model Reuse Compound)
  Every library entry = potential multiplier across portfolio
  CEO tracks: library size, transfer count, time-saved-per-transfer
```

---

### SKILL 7: `forge-flywheel` — Data Flywheel & Compound Tracking

**Stage:** 3-4 (continuous, accelerating)
**Trigger:** "data flywheel", "compound", "R1 flywheel", "training data", "field data pipeline"

**Workflow:**

```
THE FORGE FLYWHEEL (R1-F):

  DEPLOY product with AI ──▶ Field data collected via telemetry
         ↑                              │
         │                              ▼
  Better model retrained ◀── Data improves training set
         │                              │
         │                              ▼
  Model updated ◀──────── New model validated
         │
         ▼
  Product performance improves ──▶ Customer trust increases
         │                              │
         ▼                              ▼
  More products deployed ◀──── More contracts won
```

```
Step 1: 🤖 Monitor flywheel health
  │     ├── Data collection rate: GB/month from deployed products
  │     ├── Data quality: % usable for retraining
  │     ├── Model update frequency: versions/quarter
  │     ├── Performance improvement: accuracy delta per retraining
  │     ├── Flywheel speed: (insights acted on / generated) × (1 / days to action)
  │     └── Alert: "Flywheel stalling — data collection rate dropped 40%"
  │
Step 2: 👤 Steer flywheel
  │     ├── Prioritize: which data is most valuable to collect?
  │     ├── Decide: retrain now or wait for more data?
  │     ├── Allocate: team capacity for flywheel vs. new products
  │     └── Strategic: "Should we deploy more units to generate more data?"
  │
Step 3: 🤖 Compound tracking
  │     ├── Portfolio Compound Score: sum of cross-product synergies
  │     ├── Library Growth Rate: new models/quarter
  │     ├── Transfer Success Rate: % successful cross-product transfers
  │     ├── Cost Reduction Trend: ACH savings over time
  │     └── Capability Growth: new features enabled by retraining
```

---

### SKILL 8: `forge-portfolio` — Portfolio Dashboard

**Stage:** Cross-stage (CEO's primary FORGE view)
**Trigger:** "portfolio", "dashboard", "FORGE score", "all products", "product status"

**Dashboard Structure:**

```
┌──────────────────────────────────────────────────────────────────┐
│        FORGE PORTFOLIO DASHBOARD — CEO VIEW                      │
│        ────────────────────────────────────                      │
│                                                                   │
│  PORTFOLIO FORGE SCORES:                                          │
│  ┌─────────────┬───┬───┬───┬───┬───┬───────┬────────┐           │
│  │ Product     │ F │ O │ R │ G │ E │ Score │ Stage  │           │
│  ├─────────────┼───┼───┼───┼───┼───┼───────┼────────┤           │
│  │ V-SMASH     │ 2 │ 3 │ 2 │ 3 │ 3 │ 13/25 │ HEATING│           │
│  │ LOMAH-AD    │ 0 │ 1 │ 1 │ 1 │ 2 │  5/25 │ RAW ORE│           │
│  │ BB-01       │ 1 │ 1 │ 0 │ 1 │ 2 │  5/25 │ RAW ORE│           │
│  │ MTB-20      │ 2 │ 2 │ 1 │ 2 │ 3 │ 10/25 │ HEATING│           │
│  │ TDR         │ 1 │ 0 │ 0 │ 0 │ 1 │  2/25 │ RAW ORE│           │
│  │ SCOREBOARD  │ 3 │ 2 │ 1 │ 2 │ 3 │ 11/25 │ HEATING│           │
│  └─────────────┴───┴───┴───┴───┴───┴───────┴────────┘           │
│  Portfolio Average: 7.7/25 = RAW ORE                              │
│                                                                   │
│  MODEL LIBRARY:                                                   │
│  Total models: 3 (1 production, 2 experimental)                   │
│  Transfers this quarter: 0 → TARGET: 1                           │
│  Library utilization: 33% (1/3 products using library models)    │
│                                                                   │
│  FLYWHEEL HEALTH:                                                │
│  Data collection: ___ GB/month (target: ___)                     │
│  Model updates this quarter: ___ (target: 1)                    │
│  Flywheel speed: ___ (baseline)                                  │
│                                                                   │
│  ACH PIPELINE:                                                    │
│  Stage 0 (Scouting): ___ opportunities identified                │
│  Stage 1 (SHIFT assessed): ___ GO / ___ NO-GO / ___ pending    │
│  Stage 2 (Validating): ___ products in validation                │
│  Stage 3 (Library): ___ models cataloged                        │
│                                                                   │
│  ALERTS:                                                          │
│  🔴 LOMAH-AD: Fallback Level 0 — HALT deployment               │
│  🟡 Library: 0 transfers in 90 days — R5 dormant               │
│  🟡 TDR: SHIFT assessment overdue                               │
│                                                                   │
│  BINDING CONSTRAINT: AI Talent (2 engineers)                     │
│  Impact: Caps model development to ~2 products/quarter           │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**HELIX Integration:**
```
forge-portfolio READS FROM HELIX:
├── helix-quality-gate: product phase → "V-SMASH at HELIX Phase 3"
├── helix-integration-debt: "Product X has 5 open integration items"
├── helix-sync-protocol: "Last sync date, next sync date"
└── helix-project-init: "New project started for Product Y"

forge-portfolio WRITES TO HELIX:
├── "FORGE priority: V-SMASH > LOMAH > BB-01" → helix resource allocation
├── "HALT LOMAH-AD deployment" → helix-quality-gate override
└── "New ACH opportunity in MTB-20" → triggers helix-task-clarify review
```

---

### SKILL 9: `forge-cost` — Edge-Realistic Defense Cost Analysis

**Stage:** Cross-stage (used during SHIFT, validation, portfolio review)
**Trigger:** "chi phí ACH", "cost analysis", "breakeven", "defense cost", "so sánh giá"

**Workflow:**

```
Input: ACH solution spec + hardware alternative spec
  │
  ▼
Step 1: 🤖 Generate cost comparison
  │     ├── HARDWARE ALTERNATIVE:
  │     │   ├── Unit cost (defense-grade, NOT consumer pricing)
  │     │   ├── Import cost (customs, export license, shipping to VN)
  │     │   ├── Integration cost (adapt to Workshop X product)
  │     │   ├── Lifecycle cost (maintenance, calibration, spares)
  │     │   └── Supply chain risk cost (sanctions, embargo probability)
  │     │
  │     ├── ACH SOLUTION:
  │     │   ├── Compute hardware (defense-rated board)
  │     │   ├── Sensor cost (commodity camera, mic, IMU)
  │     │   ├── Development cost (model dev, amortized over production volume)
  │     │   ├── Validation cost (testing infrastructure)
  │     │   ├── Deployment cost (integration, firmware, field update)
  │     │   ├── Continuous monitoring cost (telemetry, retraining)
  │     │   └── Reuse credit: "Dev cost shared across N products"
  │     │
  │     ├── COMPARISON:
  │     │   ├── Breakeven volume: at what quantity is ACH cheaper?
  │     │   ├── ★ At Workshop X volumes (<100 units): net cost delta
  │     │   ├── ★ Capability premium: features impossible with hardware
  │     │   ├── ★ Local content impact: % domestic sourcing change
  │     │   └── ★ Strategic value: independence from foreign suppliers
  │     │
  │     └── SENSITIVITY: What changes the math?
  │         ├── "If production volume doubles → breakeven shifts from 50 to 25"
  │         ├── "If talent cost increases 30% → still viable?"
  │         └── "If export controls tighten → ACH value increases dramatically"
  │
  ▼
Step 2: 👤 Interpret & decide
  │     ├── "Economics alone don't justify at our volumes — but..."
  │     ├── "...capability premium is decisive for this customer"
  │     ├── "...local content value outweighs cost difference"
  │     ├── "...supply chain independence is strategic necessity"
  │     └── DECISION: economically justified? / strategically justified?
  │
  ▼
Output: Cost Analysis Report → feeds forge-shift and forge-portfolio
```

**Key Insight (from past analysis):**
```
⚠️ ACH ECONOMICS WARNING:

Consumer costing:  ACH saves $500/unit ← MISLEADING
Defense costing:   Breakeven ~30-100 units ← REALISTIC
Workshop X volume: <10 prototypes ← ACH may be NET COST INCREASE

BUT: Giá trị thực nằm ở:
1. Capability Premium (tính năng mới không thể làm bằng hardware)
2. Reuse Compound (model serve multiple products)
3. Local Content (giảm phụ thuộc nhập khẩu)
4. Supply Chain Independence (không bị export control)

→ CEO đừng justify ACH bằng unit cost savings
→ Justify bằng STRATEGIC VALUE + COMPOUND POTENTIAL
```

---

### SKILL 10: `forge-evolve` — Competitive Moat & Identity Evolution

**Stage:** 4 (long-term, continuous)
**Trigger:** "competitive moat", "identity", "defense AI company", "long-term strategy", "evolve portfolio"

**Workflow:**

```
Input: Portfolio dashboard + model library + market intelligence
  │
  ▼
Step 1: 🤖 Moat assessment
  │     ├── Data Moat: "How much field data do we have that competitors don't?"
  │     ├── Model Library Moat: "How many validated models? Transfer count?"
  │     ├── Validation Moat: "How much defense-grade evidence?"
  │     ├── Trust Moat: "How many repeat customers? Contract renewals?"
  │     ├── Talent Moat: "How hard to replicate our team?"
  │     └── Compound Moat: "How many cross-product synergies active?"
  │
  ▼
Step 2: 👤 Identity check
  │     ├── "When I introduce Workshop X, do I say:"
  │     │   ├── ❌ "xưởng cơ khí quốc phòng" → OLD identity
  │     │   ├── ⚠️ "xưởng cơ khí dùng AI" → TRANSITIONING
  │     │   └── ✅ "defense AI company that ships hardware" → TARGET identity
  │     ├── "Does our team BELIEVE we're an AI company?"
  │     ├── "Do our customers PERCEIVE us as AI-capable?"
  │     └── IDENTITY SCORE: 1 (old) → 5 (fully transformed)
  │
  ▼
Step 3: 🤖→👤 Evolution roadmap
  │     ├── Next 12 months: what products move portfolio toward target identity?
  │     ├── Talent plan: what hires/training to strengthen moat?
  │     ├── Visibility plan: publications, demos, conferences
  │     └── Compound targets: library growth, transfer targets, flywheel speed
  │
  ▼
Output: Moat Assessment + Identity Score + Evolution Roadmap (annual)
```

---

## V. FORGE × HELIX INTEGRATION MAP

```
╔════════════════════════════════════════════════════════════════════╗
║           FORGE × HELIX: COMPLETE INTEGRATION PROTOCOL            ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  FORGE Stage 0 (Scout)                                             ║
║  ├── READS: HELIX 6-flow functions, project charters              ║
║  └── WRITES: ACH opportunity tags → HELIX task-clarify            ║
║                                                                    ║
║  FORGE Stage 1 (SHIFT + Fallback)                                  ║
║  ├── READS: HELIX requirements, function structures, concepts     ║
║  └── WRITES: ACH approval → HELIX requirements (new constraints)  ║
║              Fallback spec → HELIX ICD entry                       ║
║              Model availability → HELIX concept options            ║
║                                                                    ║
║  ★ SYNC TRIGGER: forge-shift GO decision →                        ║
║    helix-sync-protocol MUST run within 2 weeks                     ║
║    (new ACH requirement affects all 3 domains)                     ║
║                                                                    ║
║  FORGE Stage 2 (Validate + Trust)                                  ║
║  ├── READS: HELIX Gate 4 (manufacturing ready), detailed design   ║
║  ├── TRIGGER: HELIX Sync S5 = forge-validate Stage 1 START        ║
║  └── WRITES: validation results → HELIX design journal            ║
║              performance envelope → HELIX next-version requirements║
║                                                                    ║
║  FORGE Stage 3 (Library + Flywheel)                                ║
║  ├── READS: HELIX gate results (validation passed? → library OK)  ║
║  └── WRITES: library models → HELIX concept-generate options      ║
║              model interfaces → HELIX ICD templates                ║
║              transfer plans → new HELIX project-init               ║
║                                                                    ║
║  FORGE Stage 4 (Evolve)                                            ║
║  ├── READS: all HELIX metrics (methodology adoption, debt trends) ║
║  └── WRITES: portfolio direction → HELIX resource priorities      ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  CROSS-CUTTING PROTOCOLS:                                          ║
║                                                                    ║
║  CEO Monthly Review:                                               ║
║  ├── forge-portfolio dashboard (15 min)                           ║
║  ├── HELIX sync protocol (40 min)                                  ║
║  └── Cross-check: "FORGE priorities aligned with HELIX execution?"║
║                                                                    ║
║  Quarterly Strategic Review:                                       ║
║  ├── forge-evolve moat assessment                                  ║
║  ├── HELIX Score reassessment                                      ║
║  ├── Compound Law recalculation (BRIDGE × FORGE × HELIX)          ║
║  └── Decision: resource reallocation for next quarter              ║
║                                                                    ║
╠════════════════════════════════════════════════════════════════════╣
║  ANTI-PATTERN DETECTION:                                           ║
║                                                                    ║
║  🔴 forge-shift says GO but HELIX has no project-init             ║
║     → Decision made but not executed. Track as "Strategy-Execution ║
║       Gap." CEO action: create HELIX project within 1 week.       ║
║                                                                    ║
║  🔴 HELIX building product but no forge-shift assessment          ║
║     → Executing without strategic decision. Track as "Accidental   ║
║       ACH." CEO action: run forge-shift retroactively.            ║
║                                                                    ║
║  🔴 forge-library has model but HELIX not using it                ║
║     → Compound opportunity missed. Track as "R5 Dormant."         ║
║       CEO action: review in next sync.                            ║
║                                                                    ║
║  🔴 HELIX sync reveals ICD change but forge-fallback not updated  ║
║     → Fallback may be invalidated. CRITICAL. CEO action: halt     ║
║       until fallback re-verified.                                  ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

---

## VI. RELATIONSHIP TO EXISTING SKILLS

| Existing Skill | FORGE Relationship | Action |
|---------------|-------------------|--------|
| `pahl-beitz-mastery` | FORGE wraps P&B at portfolio level; P&B executes within HELIX | Keep for learning; FORGE for strategy |
| `engineering-concept-evaluation-assistant` | Used BY `forge-shift` for VDI 2225 with ACH criteria | Enhance to include ACH column |
| `cad-review-automation` | Used BY HELIX under FORGE product standards | Keep; add forge-fallback checks |
| `cad-visualization-freecad` | Execution tool within HELIX, informed by FORGE specs | Keep as-is |
| `dmir-defense-systems-mentor` | Analytical framework; FORGE is operational application | D-M-I-R diagnoses; FORGE executes |
| `quality-gate-reporter` | Manufacturing QC; forge-validate extends to AI validation | Enhance or integrate |
| `compound-engineering` | Meta-system for learning extraction; FORGE uses for flywheel | Complementary, different scope |

**Principle:** FORGE skills operate at PORTFOLIO/PRODUCT STRATEGY level. They CALL HELIX skills for execution. HELIX skills CALL existing CAD/documentation skills for specific tasks. Three-tier hierarchy:

```
FORGE (what to build, which ACH) 
  └── HELIX (how to design each product)
        └── Existing skills (CAD, docs, review — specific task execution)
```

---

## VII. IMPLEMENTATION PRIORITY

### Giai Đoạn 1 (Tuần 1-2): Decision Infrastructure

```
Priority 1: forge-shift         (THE critical decision skill — GO/NO-GO ACH)
Priority 2: forge-portfolio     (CEO needs visibility NOW)
Priority 3: forge-fallback      (every ACH needs this, currently 0% coverage)
```

**Rationale:** forge-shift + forge-fallback ngay lập tức address LOMAH-AD crisis (Fallback Level 0). forge-portfolio cho CEO visibility across tất cả products. Ba skill này alone đưa FORGE từ 31% → ~45%.

### Giai Đoạn 2 (Tuần 3-4): Validation & Economics

```
Priority 4: forge-validate      (prove products work — builds trust stock)
Priority 5: forge-cost          (stop using consumer pricing for defense)
Priority 6: forge-trust         (customer relationships = defense differentiator)
```

### Giai Đoạn 3 (Tuần 5-6): Compound & Moat

```
Priority 7: forge-scout         (systematic opportunity discovery)
Priority 8: forge-library       (R5 activation — compound begins)
Priority 9: forge-flywheel      (continuous improvement engine)
Priority 10: forge-evolve       (long-term identity transformation)
```

---

## VIII. FORGE SCORE v2: METRICS CHO BỘ SKILL MỚI

| Dimension | Metric | Current | Target 3M | Target 6M | Measured By |
|-----------|--------|:-------:|:---------:|:---------:|-------------|
| **F** — Fallback | % ACH products with Level 1+ fallback | ~20% | 80% | 100% | forge-fallback |
| **O** — Validate | % products with Performance Envelope | ~10% | 40% | 70% | forge-validate |
| **R** — Reuse | Model library size + transfer count | 1 model, 0 transfers | 3 models, 1 transfer | 5 models, 3 transfers | forge-library |
| **G** — Ground truth | Products with active data pipeline | ~1 | 2 | 4 | forge-flywheel |
| **E** — Edge-cost | % products with defense-realistic costing | ~20% | 80% | 100% | forge-cost |

**FORGE Composite Score = sum of dimension scores (each 1-5) / 25**

**Bands:**
- 0-7/25 (< 28%): **RAW ORE** — No systematic product strategy → gần hiện tại
- 8-13/25 (32-52%): **HEATING** — Some ACH discipline, validation starting
- 14-19/25 (56-76%): **FORGING** — Library active, flywheel turning, moat building
- 20-25/25 (80-100%): **TEMPERED** — Defense AI company identity achieved

---

## IX. COMPOUND LAW IMPACT VỚI FORGE + HELIX SKILLS

```
HIỆN TẠI:
  BRIDGE: 12/30 = 40%
  FORGE:  7.8/25 = 31%  ← no systematic product strategy
  HELIX:  ~10/35 = 29%  ← no systematic design execution
  COMPOUND: 0.40 × 0.31 × 0.29 = 0.036 = 3.6%

SAU 3 THÁNG (FORGE + HELIX skill sets deployed):
  BRIDGE: 15/30 = 50%   (+25%)
  FORGE:  12/25 = 48%   (+55%)  ← SHIFT decisions + fallback + portfolio view
  HELIX:  16/35 = 46%   (+59%)  ← sync + ICD + 6-flow
  COMPOUND: 0.50 × 0.48 × 0.46 = 0.110 = 11.0%  ← 3.1× improvement

SAU 6 THÁNG:
  BRIDGE: 18/30 = 60%
  FORGE:  16/25 = 64%   (+106%) ← validation + library + flywheel starting
  HELIX:  22/35 = 63%   (+117%)
  COMPOUND: 0.60 × 0.64 × 0.63 = 0.242 = 24.2%  ← 6.7× improvement

★ FORGE + HELIX together improve faster than either alone
  Because: FORGE decisions (what ACH) feed HELIX execution (how to design)
  And: HELIX validation results feed FORGE library (compound)
  → CROSS-FRAMEWORK REINFORCEMENT (virtuous cycle)
```

---

## X. CEO PROTOCOL: FORGE + HELIX COMBINED

### Daily (1 phút)

```
"Hôm nay team đang SCOUT (cơ hội mới), DECIDE (SHIFT), DESIGN (HELIX),
 VALIDATE (prove), hay COMPOUND (library/flywheel)?"

Nếu không biết → ngày bị firefighting
Nếu 3 ngày liên tiếp DECIDE mà không DESIGN → Analyst Trap
Nếu 3 ngày liên tiếp DESIGN mà không VALIDATE → shipping unproven product
```

### Weekly (20 phút)

```
FORGE (10 min):
├── forge-portfolio quick check: any alerts?
├── forge-shift: pending decisions to make?
└── forge-flywheel: data collection on track?

HELIX (10 min):
├── helix-integration-debt: trend up or down?
├── helix-design-journal: review entries
└── Any domain blocked? Need unblocking?
```

### Monthly (90 phút)

```
FORGE (30 min):
├── forge-portfolio full review
├── forge-validate: any products ready for Stage 2+?
├── forge-library: any new models to catalog?
└── forge-trust: customer engagement gaps?

HELIX (40 min):
├── helix-sync-protocol: full sync meeting
├── helix-quality-gate: any phase transitions?
└── HELIX Score update

CROSS-CHECK (20 min):
├── "FORGE decisions aligned with HELIX execution?"
├── "Anti-patterns detected?" (see Section V)
├── "Compound Law recalculation"
└── "Next month priority: FORGE-heavy or HELIX-heavy?"
```

### Quarterly (3 giờ)

```
1. forge-evolve: moat assessment + identity score (60 min)
2. Full FORGE + HELIX Score reassessment (30 min)
3. Compound Law: BRIDGE × FORGE × HELIX (30 min)
4. Resource reallocation: nơi nào invest next quarter? (30 min)
5. Strategic direction: portfolio evolution (30 min)
```

---

## XI. THREE LAWS CỦA FORGE (Nhắc Lại + Cập Nhật)

### Law 1: The Substrate Law
**"You cannot forge what you cannot fuel."**
Talent + Data TRƯỚC design technique. FORGE skills giúp CEO THẤY substrate gaps rõ hơn, nhưng không GIẢI QUYẾT chúng. Hire AI engineers = prerequisite cho mọi FORGE skill hoạt động hiệu quả.

### Law 2: The Envelope Law
**"Average performance is a lie. Defense tests at extremes."**
forge-validate builds Performance Envelopes. Mỗi ACH product phải có envelope — transparent, shared với customer. Khi CEO nghe "accuracy 95%," hỏi: "At what conditions? Where does it fail?"

### Law 3: The Identity Law
**"ACH as checklist = tactic (20% value). ACH as organizational identity = transformation (100% value)."**
forge-evolve tracks identity transformation. Khi Workshop X's FORGE Score reaches FORGING (56%+) VÀ CEO tự nhiên nói "defense AI company" thay vì "xưởng cơ khí" → Identity Law activated.

---

*Architecture designed for: Workshop X defense product portfolio, ACH (AI-Compensates-Hardware) design principle, defense-grade validation, compound model library, phối hợp với HELIX design execution skills.*

*Integrates with: BRIDGE (operations), HELIX (design execution), existing CAD/documentation/review skills.*

*Next step: Implement Priority 1-3 skills (forge-shift, forge-portfolio, forge-fallback) as actual SKILL.md files. Cross-implement HELIX Priority 1-3 simultaneously for maximum compound effect.*
