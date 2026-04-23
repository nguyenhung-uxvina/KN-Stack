# BRIDGE SKILL ARCHITECTURE v2
## Bộ Skill Đầy Đủ Theo Giai Đoạn Vận Hành — Phối Hợp Người-AI × FORGE × HELIX

**Ngày:** 01/03/2026
**Bối cảnh:** BRIDGE = tầng ngoài cùng trong Compound Law (BRIDGE × FORGE × HELIX). Hiện tại 40% (12/30 = FRAGILE). BRIDGE quản lý TỔ CHỨC VẬN HÀNH — nền tảng mà FORGE (product strategy) và HELIX (design execution) đứng lên trên.
**Mục tiêu:** Thiết kế bộ skill phản ánh vòng đời vận hành — từ knowledge → readiness → signals → automation → judgment → evolution — với ranh giới người-AI rõ ràng và điểm tích hợp với FORGE + HELIX.

---

## I. BRIDGE TRONG BỘ BA: TẦNG NỀN TẢNG

### Tại Sao BRIDGE Phải Ổn Định Trước

```
BRIDGE × FORGE × HELIX:

BRIDGE (Operations) = ORGANIZATIONAL INFRASTRUCTURE
  "Tri thức có được capture không? Tín hiệu có bị mất không?
   Process có automate không? Judgment có được hỗ trợ không?
   Hệ thống có tự cải thiện không?"
       │
       ├── Nếu BRIDGE yếu → FORGE decisions dựa trên thông tin thiếu
       ├── Nếu BRIDGE yếu → HELIX execution không có context
       └── Nếu BRIDGE yếu → Compound Law multiplier bị kéo xuống
       │
       ▼
FORGE (Product Strategy) = PRODUCT INTELLIGENCE
  "ACH opportunity nào? Validate thế nào? Reuse gì? Moat đâu?"
       │
       ▼
HELIX (Design Execution) = PROJECT EXECUTION
  "Requirements? Function structure? Embodiment? Detail?"

★ BRIDGE cung cấp TRI THỨC + TÍN HIỆU + TỰ ĐỘNG HÓA cho cả FORGE và HELIX.
  Không có BRIDGE → FORGE quyết định mù → HELIX thực hiện sai → waste.
```

### Vấn Đề Hiện Tại: BRIDGE Skills Không Tồn Tại

```
HIỆN TẠI — BRIDGE không có skill nào:
┌───────────────────────────────────────────────────┐
│ BRIDGE (operations)                               │
│ ❌ Không có KB system → tri thức trong đầu người   │
│ ❌ Không có signal extraction → data mất mỗi ngày  │
│ ❌ Không có deployment gates → launch không kiểm soát│
│ ❌ Không measure flywheel → không biết đang improve? │
│ ⚠️ Một số automation skills rời rạc (quality-gate,  │
│    cad-doc-gen) nhưng không trong framework         │
└───────────────────────────────────────────────────┘

FORGE + HELIX đã có skill architecture (vừa thiết kế).
BRIDGE = lỗ hổng cuối cùng. Document này lấp lỗ hổng đó.
```

### Thiết Kế Mới: BRIDGE Skills Theo B-R-I-D-G-E Flow

```
BRIDGE OPERATIONS FLOW:

Stage B         Stage R          Stage I          Stage D          Stage G         Stage E
BUILD           READY            INTERPRET        DO               GUIDE           EVOLVE
KNOWLEDGE       INTERNALLY       SIGNALS          DETERMINISTIC    JUDGMENT        SYSTEM
┌──────────┐   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ bridge-  │──▶│ bridge-  │───▶│ bridge-  │───▶│ bridge-  │───▶│ bridge-  │───▶│ bridge-  │
│ knowledge│   │ deploy-  │    │ signal-  │    │ automate │    │ judgment │    │ flywheel │
│ -base    │   │ gate     │    │ extract  │    │          │    │          │    │          │
└──────────┘   └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
      │              │               │               │               │              │
      ▼              ▼               ▼               ▼               ▼              ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        BRIDGE CROSS-STAGE SKILLS                                       │
│  bridge-risk-radar  │  bridge-cross-learn  │  bridge-dashboard  │  bridge-talent-map  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## II. HUMAN-AI COLLABORATION MODEL CHO BRIDGE

BRIDGE skills vận hành ở tầng TỔ CHỨC → mix giữa infrastructure tasks (AI-heavy) và organizational decisions (human-heavy).

| Ký hiệu | Vai trò | Ví dụ BRIDGE |
|:--------:|---------|--------------|
| 🤖 | **AI Generates** | Index KB, extract signals from meetings, track metrics |
| 👤 | **Human Generates** | Customer insights, field observations, tacit knowledge |
| 🤖→👤 | **AI Draft → Human Decides** | KB gap report → CEO prioritize which gaps to fill |
| 👤→🤖 | **Human Specifies → AI Executes** | "Transcribe & extract from this design review" |

**Nguyên tắc phân công BRIDGE:**

```
AI LÀM TỐT:                              NGƯỜI PHẢI LÀM:
──────────────                             ──────────────────
✓ Index, organize, search knowledge base   ✗ Capture TACIT knowledge (experience, intuition)
✓ Transcribe & extract from meetings       ✗ Validate extracted insights (AI misinterprets context)
✓ Track deployment readiness checklists    ✗ Decide GO/NO-GO for deployment
✓ Automate document generation             ✗ Design the PROCESS to automate (judgment)
✓ Calculate metrics, detect trends         ✗ Interpret metrics in organizational context
✓ Alert on anomalies                       ✗ Decide how to respond to anomalies
✓ Generate dashboards                      ✗ Decide what to CHANGE based on dashboards
✓ Cross-reference across products          ✗ Decide which cross-product lesson is applicable
✓ Draft training materials from KB         ✗ Teach, mentor, transfer judgment (human-to-human)
✓ Monitor flywheel metrics                 ✗ Steer flywheel direction (what to optimize next)
```

---

## III. BỘ SKILL ĐẦY ĐỦ: 10 SKILLS

### Tổng Quan

| # | Skill Name | Stage | Mục đích | Vai trò chính |
|:-:|-----------|:-----:|----------|:-------------:|
| 1 | `bridge-knowledge-base` | B | Capture, organize, serve tri thức tổ chức | 👤→🤖 (capture) + 🤖 (serve) |
| 2 | `bridge-deploy-gate` | R | Kiểm soát deployment sequence (Phase 0→1→2) | 🤖→👤 |
| 3 | `bridge-signal-extract` | I | Trích xuất insight từ mọi interaction | 👤→🤖 |
| 4 | `bridge-automate` | D | Tự động hóa quy trình lặp lại | 🤖→👤 |
| 5 | `bridge-judgment` | G | Hỗ trợ ra quyết định có chất lượng | 🤖→👤 |
| 6 | `bridge-flywheel` | E | Đo và tăng tốc R1-WX insight cycle | 🤖 (measure) + 👤 (steer) |
| 7 | `bridge-risk-radar` | Cross | Phát hiện rủi ro tổ chức sớm | 🤖→👤 |
| 8 | `bridge-cross-learn` | Cross | Cross-product learning sessions | 🤖→👤 |
| 9 | `bridge-dashboard` | Cross | Unified CEO view (7 metrics, 15 min/week) | 🤖 |
| 10 | `bridge-talent-map` | Cross | Knowledge risk & talent pipeline | 🤖→👤 |

---

## IV. CHI TIẾT TỪNG SKILL

---

### SKILL 1: `bridge-knowledge-base` — Hệ Thống Tri Thức

**Stage:** B (nền tảng — mọi thứ khác đứng trên đây)
**Trigger:** "knowledge base", "KB", "tri thức", "document", "lưu lại", "tôi cần tìm thông tin về..."

**KB Architecture — 3 Layers:**

```
LAYER 1: STANDARDS & METHODS (thay đổi chậm, formal)
├── Design methodology templates (P&B phases, HELIX protocols)
├── Standards library (MIL-STD, TCVN, STANAG references)
├── Product templates (requirements checklist, DfX rules)
├── FORGE templates (SHIFT checklist, fallback template, cost model)
└── Update: quarterly or when standards change

LAYER 2: PRODUCT KNOWLEDGE (thay đổi mỗi project, semi-formal)
├── Per-product: requirements, function structures, ICDs, test results
├── Design decisions log (from helix-design-journal)
├── Validation evidence (from forge-validate)
├── Model library catalog (from forge-library)
└── Update: per-project, synced with HELIX phases

LAYER 3: TACIT & INSIGHTS (thay đổi liên tục, captured from work)
├── Design review extracts (from bridge-signal-extract)
├── Field feedback digests (structured from anecdotal)
├── Cross-product lessons (from bridge-cross-learn)
├── CEO decision rationale (from bridge-judgment)
└── Update: weekly, continuous capture
```

**Workflow:**

```
CAPTURE FLOW:
  │
  ├── 👤 Engineer creates/updates design artifact
  │   └── 🤖 Auto-index into KB Layer 2 (metadata, tags, links)
  │
  ├── 👤→🤖 Tacit knowledge capture session (monthly per senior)
  │   ├── "Anh/chị, nếu anh/chị nghỉ ngày mai, 5 điều quan trọng nhất team cần biết?"
  │   ├── AI records, structures, indexes into KB Layer 3
  │   └── 👤 Expert validates: "Đúng, nhưng thêm điều kiện X"
  │
  ├── 🤖 Auto-extract from HELIX & FORGE
  │   ├── helix-design-journal entries → KB Layer 2+3
  │   ├── helix-sync-protocol summaries → KB Layer 3
  │   ├── forge-validate results → KB Layer 2
  │   └── forge-library catalog → KB Layer 2
  │
  └── 🤖 Auto-extract from bridge-signal-extract → KB Layer 3

SERVE FLOW:
  │
  ├── 🤖 Search: "Tìm tất cả test results cho sensor mounting bracket"
  │   └── Returns: structured results from Layer 2 + related Layer 3 insights
  │
  ├── 🤖 Context injection: khi engineer bắt đầu HELIX task
  │   └── "Dự án tương tự XYZ gặp vấn đề thermal ở Phase 3 — xem thêm KB#1234"
  │
  └── 🤖 Gap detection: "Sản phẩm MTB-20 có 0 entries Layer 2 — KB gap ★★★"
```

**FORGE + HELIX Integration:**
```
bridge-knowledge-base FEEDS INTO:
├── FORGE: forge-scout reads KB to find ACH opportunities in existing products
├── FORGE: forge-shift reads KB for prior similar assessments
├── FORGE: forge-cost reads KB for historical cost data
├── HELIX: helix-task-clarify reads KB for similar product requirements
├── HELIX: helix-concept-generate reads KB for prior solution principles
├── HELIX: helix-embody-realize reads KB for known manufacturing constraints
└── HELIX: helix-6flow-mapper reads KB for similar function structures

bridge-knowledge-base RECEIVES FROM:
├── FORGE: forge-validate results, forge-library entries
├── HELIX: helix-design-journal, helix-sync summaries, helix-quality-gate results
└── BRIDGE: bridge-signal-extract outputs, bridge-cross-learn sessions
```

**Metrics:**
- KB Coverage: % products with Layer 2 documentation (current: ~20%, target 6M: 70%)
- KB Currency: % entries updated within last 3 months (target: >80%)
- KB Utilization: queries/week (indicates team actually using it)
- KB Single-Person Risk: % knowledge held by only 1 person (target: <20%)

---

### SKILL 2: `bridge-deploy-gate` — Kiểm Soát Deployment

**Stage:** R (Readiness — prevent premature deployment)
**Trigger:** "deploy", "triển khai", "go live", "phase gate", "ready?", "có nên deploy chưa?"

**The 4-Phase Deployment Protocol:**

```
Phase 0: INTERNAL PROOF OF CONCEPT
─────────────────────────────────
🤖 Checklist:
├── [ ] AI model trained on available data
├── [ ] Basic accuracy demonstrated (internal benchmark)
├── [ ] Known limitations documented
├── [ ] No safety-critical failure modes identified
👤 Decision: "Proof exists that approach COULD work"
→ Gate: Evidence-based, low threshold

Phase 1: INTERNAL VALIDATION
────────────────────────────
🤖 Checklist:
├── [ ] forge-validate Stage 1 (lab) passed
├── [ ] forge-fallback architecture designed and coded
├── [ ] DfX review completed (from HELIX)
├── [ ] Performance Envelope v1 documented
├── [ ] Integration Debt < threshold (from HELIX)
👤 Decision: "System works under controlled conditions with fallback"
→ Gate: Higher threshold, internal evidence sufficient

Phase 2: CONTROLLED EXTERNAL
────────────────────────────
🤖 Checklist:
├── [ ] forge-validate Stage 2 (field simulation) passed
├── [ ] Fallback tested under realistic conditions
├── [ ] Customer briefed on capabilities AND limitations
├── [ ] Continuous monitoring active (forge-flywheel)
├── [ ] Operator training completed
👤 Decision: "System ready for limited external use"
→ Gate: Customer trust evidence required

Phase 3: FULL DEPLOYMENT
────────────────────────
🤖 Checklist:
├── [ ] forge-validate Stage 3 (operational field test) passed
├── [ ] 90+ day operational history without critical failures
├── [ ] Customer satisfaction confirmed
├── [ ] Revalidation schedule established
├── [ ] Model entered into forge-library
👤 Decision: "System is production-ready"
→ Gate: Highest threshold, customer evidence required
```

**Critical Rule:**
```
★ V-SMASH YOLO WAS DEPLOYED AT PHASE 2 WITHOUT PHASE 0-1 EVIDENCE.
  This worked because of CEO's personal judgment and small-scale deployment.
  
  FROM NOW ON: Phase sequence is NON-NEGOTIABLE.
  Phase 0-1 evidence BEFORE Phase 2 deployment.
  CEO can ACCELERATE phases but cannot SKIP them.
  
  bridge-deploy-gate tracks compliance:
  "Product X at Phase Y — all prior phase evidence present? YES/NO"
```

**FORGE + HELIX Integration:**
```
bridge-deploy-gate READS FROM:
├── FORGE: forge-validate results (which stage passed?)
├── FORGE: forge-fallback (fallback designed and tested?)
├── FORGE: forge-trust (customer briefed?)
├── HELIX: helix-quality-gate (design phase gates passed?)
├── HELIX: helix-integration-debt (all interfaces resolved?)
└── HELIX: helix-detail-finalize (manufacturing package complete?)

bridge-deploy-gate WRITES TO:
├── BRIDGE: bridge-dashboard (deployment status per product)
├── FORGE: forge-portfolio (deployment maturity feeds portfolio view)
└── BRIDGE: bridge-risk-radar (deployment without evidence = RED flag)
```

---

### SKILL 3: `bridge-signal-extract` — Trích Xuất Tín Hiệu

**Stage:** I (Interpret — turn interactions into data)
**Trigger:** "extract", "trích xuất", "transcribe", "log meeting", "capture insights", "design review", "test report"

**4 Signal Sources:**

```
SOURCE 1: Design Reviews (highest signal density)
──────────────────────────────────────────────────
👤→🤖 Protocol:
  BEFORE: AI prepares agenda from project status (HELIX data)
  DURING: AI records (transcript or notes)
  AFTER (within 24h):
    🤖 Extract:
    ├── Decisions made (what, why, alternatives rejected)
    ├── Assumptions stated (verified/unverified)
    ├── Interface changes (→ helix-integration-debt)
    ├── Action items (owner, deadline)
    └── Risk flags ("I'm worried about X" = signal)
    
    👤 Review: 5 min validation, correct misinterpretations
    🤖 Route: → KB Layer 3, helix-design-journal, ICD updates

VALUE: ~10 decisions/review × 4 reviews/week = 40 decisions CAPTURED
       (currently: 0 captured → 100% loss rate)

SOURCE 2: Test Events (second highest signal)
─────────────────────────────────────────────
👤→🤖 Protocol:
  BEFORE: AI generates test protocol from forge-validate plan
  DURING: Data logged (sensors + observations + photos)
  AFTER (within 48h):
    🤖 Extract:
    ├── Pass/fail per criterion (auto-scored where possible)
    ├── Anomaly analysis (unexpected behavior = HIGHEST signal)
    ├── Pattern matching ("similar to anomaly in Product B?")
    ├── Root cause hypotheses (ranked by likelihood)
    └── Recommended follow-up
    
    👤 Validate: engineer reviews AI analysis
    🤖 Route: → KB Layer 2, forge-validate evidence, HELIX design-journal

SOURCE 3: Customer/Field Interactions
──────────────────────────────────────
👤→🤖 Protocol:
  AFTER each customer interaction:
    👤 Input: structured form (product, issue, conditions, workaround)
    🤖 Extract:
    ├── Classify: design/manufacturing/user/environment issue
    ├── Traceability: connect to design decisions
    ├── Cross-product check: "same issue elsewhere?"
    ├── Priority score: safety × frequency × fix difficulty
    └── Recommended action: design change / training / process fix
    
    🤖 Route: → KB Layer 3, forge-flywheel (R1-WX input), CEO monthly digest

SOURCE 4: Cross-Domain Sync Meetings (from HELIX)
──────────────────────────────────────────────────
👤→🤖 Protocol:
  AFTER each helix-sync-protocol:
    🤖 Auto-extract: (already done by helix-sync-protocol)
    🤖 Additional BRIDGE-level extraction:
    ├── Cross-product patterns: "issue Y in Product A similar to Product B?"
    ├── Organizational bottlenecks: "blocked by same supplier 3rd time"
    ├── Talent gaps: "nobody on team knows EMC simulation"
    └── Process improvements: "sync format should include X next time"
    
    🤖 Route: → KB Layer 3, bridge-risk-radar, bridge-talent-map
```

---

### SKILL 4: `bridge-automate` — Tự Động Hóa Quy Trình

**Stage:** D (Do deterministic work — free human capacity for judgment)
**Trigger:** "automate", "tự động hóa", "repetitive", "template", "giải phóng thời gian"

**Workflow:**

```
Step 1: 🤖→👤 Identify automation candidates
  │     ├── Scan current processes: which are deterministic (same input → same output)?
  │     ├── Score each: frequency × time/instance × error risk
  │     ├── Rank by: freed_hours_per_week / implementation_effort
  │     └── Present top 5 candidates to CEO
  │
Step 2: 👤 Select & prioritize
  │     ├── "This one first — frees most judgment time"
  │     ├── "Skip that one — too fragile, context-dependent"
  │     └── ★ Rule: automate PROCESS, never automate JUDGMENT
  │
Step 3: 🤖 Implement automation
  │     ├── Connect to existing skills (cad-doc-gen, quality-gate-reporter)
  │     ├── Create new automation scripts as needed
  │     ├── Build templates for repetitive documents
  │     └── Test: AI-generated output vs. previous human output (quality check)
  │
Step 4: 👤 Validate & monitor
  │     ├── Review first 10 automated outputs (catch errors early)
  │     ├── Set quality threshold: "if AI output below X → flag for human"
  │     └── ★ Track FREED TIME: where does it go?
  │
Step 5: 🤖→👤 Freed Time Allocation (CEO mandate)
  │     ├── 40% → Judgment work (design decisions, trade-offs, reviews)
  │     ├── 25% → Integration work (cross-domain coordination)
  │     ├── 20% → Learning (skill development, methodology practice)
  │     └── 15% → Innovation (explore new approaches, ACH opportunities)
  │
  │     ★ "KHÔNG giảm người. Tăng tốc flywheel."
  │       If freed time goes to MORE paperwork → automation failed
  │       CEO tracks weekly: "Freed time went where this week?"
```

**Existing Skills as Automation Tools:**
```
Already available (invoke from bridge-automate):
├── quality-gate-reporter → Automate quality reporting
├── cad-documentation-generator → Automate drawing docs, BOM, inspection
├── cad-review-automation → Automate DfX checks
└── design-iteration-assistant → Automate design improvement proposals

To create:
├── Meeting report generator (from bridge-signal-extract output)
├── Weekly status report compiler (from HELIX + FORGE metrics)
├── Standards compliance checker (against KB Layer 1)
└── Cost estimation tool (from forge-cost templates)
```

**FORGE + HELIX Integration:**
```
bridge-automate CONNECTS TO:
├── FORGE: forge-cost templates → automate cost estimation per product
├── FORGE: forge-portfolio report → automate weekly portfolio summary
├── HELIX: helix-quality-gate → automate phase gate checklist compilation
├── HELIX: helix-integration-debt → automate ICD consistency checking
└── HELIX: all documentation outputs → automate formatting, numbering, indexing

bridge-automate WRITES TO:
├── bridge-dashboard: "Freed hours this week: X → allocated to: Y"
└── bridge-flywheel: "automation coverage: X% of deterministic processes"
```

---

### SKILL 5: `bridge-judgment` — Hỗ Trợ Ra Quyết Định

**Stage:** G (Guide — support human judgment quality, never replace it)
**Trigger:** "quyết định", "decision", "trade-off", "nên chọn gì?", "guide", "recommendation"

**Workflow:**

```
Step 1: 🤖 Structure the decision
  │     ├── Identify decision type:
  │     │   ├── Technical: "material A hay B?" → DfX data, cost, experience
  │     │   ├── Strategic: "invest vào V-SMASH hay LOMAH?" → portfolio, capacity, customer
  │     │   ├── Resource: "hire AI engineer hay buy tool?" → talent map, budget, timeline
  │     │   └── Risk: "deploy Phase 2 now or wait?" → evidence, trust, consequence
  │     │
  │     ├── Gather relevant context from:
  │     │   ├── KB (similar decisions made before? outcomes?)
  │     │   ├── FORGE portfolio (strategic alignment?)
  │     │   ├── HELIX project data (technical constraints?)
  │     │   └── External (market, competitor, regulation?)
  │     │
  │     └── Present as decision package:
  │         ├── Options (2-4 clear alternatives)
  │         ├── Criteria (what matters for this decision)
  │         ├── Evidence for each option
  │         ├── Risk assessment per option
  │         ├── ★ What we DON'T know (uncertainty disclosure)
  │         └── ★ Reversibility: "can we undo this if wrong?"
  │
Step 2: 👤 DECIDE (non-delegable)
  │     ├── Review decision package
  │     ├── Factor in: experience, intuition, relationships, politics
  │     ├── ★ "What does my gut say? Does data confirm or contradict?"
  │     └── DECISION: chosen option + rationale
  │
Step 3: 🤖 Document decision
  │     ├── Log: decision, rationale, alternatives considered, evidence used
  │     ├── Route: → KB Layer 3 (institutional memory)
  │     ├── Route: → helix-design-journal (if project-specific)
  │     └── Track: create review trigger ("revisit this in 3 months")
  │
Step 4: 🤖 Decision quality monitoring (over time)
  │     ├── Tag outcomes: "decision X from 6 months ago → outcome was Y"
  │     ├── Pattern detection: "CEO consistently overestimates timeline by 30%"
  │     └── Feedback: "decisions with more data had 2x better outcomes"
```

**★ CRITICAL PRINCIPLE:**
```
bridge-judgment NEVER says: "You should do X"
bridge-judgment ALWAYS says: "Here are options, evidence, risks, unknowns.
                              You decide."

AI improves INFORMATION QUALITY feeding into human judgment.
AI does NOT replace human judgment.

The moment CEO delegates judgment to AI → 
  Judgment stock atrophies → 
  Shifting the Burden archetype activates →
  System degrades.
```

---

### SKILL 6: `bridge-flywheel` — R1-WX Insight Cycle

**Stage:** E (Evolve — the system improves itself)
**Trigger:** "flywheel", "R1-WX", "cycle time", "evolution", "improve system", "cải thiện"

**The R1-WX Flywheel:**

```
  DEPLOY product ──▶ FIELD DATA collected (bridge-signal-extract)
         ↑                        │
         │                        ▼
  BETTER DESIGN     INSIGHTS extracted (bridge-knowledge-base)
  (HELIX cycle)              │
         ↑                        ▼
         │               DESIGN CHANGES proposed (forge-flywheel)
         │                        │
         └────────────────────────┘
         
CURRENT CYCLE TIME: 12-24 months (estimate)
TARGET: 4-6 months
METRIC: R1-WX Speed = (Insights Acted On / Insights Generated) × (1 / Avg Days to Action)
```

**Workflow:**

```
Step 1: 🤖 Measure flywheel components
  │     ├── GENERATE: How many insights extracted this month?
  │     │   Source: bridge-signal-extract output count
  │     │
  │     ├── DELIVER: How many insights reached the right person?
  │     │   Source: KB utilization + decision log
  │     │
  │     ├── ACT: How many insights became design changes?
  │     │   Source: helix-design-journal entries linked to insights
  │     │
  │     ├── VALIDATE: How many design changes validated in field?
  │     │   Source: forge-validate results on updated products
  │     │
  │     └── COMPOUND: How many improvements transferred across products?
  │         Source: forge-library transfers + bridge-cross-learn sessions
  │
Step 2: 🤖 Identify bottleneck
  │     ├── "100 insights generated but only 10 reached team → DELIVERY bottleneck"
  │     ├── "10 insights reached team but 0 became design changes → ACTION bottleneck"
  │     ├── "5 changes made but none validated → VALIDATION bottleneck"
  │     └── Prescribe: focus intervention on the BOTTLENECK stage
  │
Step 3: 👤 Steer flywheel
  │     ├── "Bottleneck is at ACTION — why aren't insights becoming changes?"
  │     │   ├── Capacity: team too busy with current projects
  │     │   ├── Priority: insights not important enough
  │     │   └── Process: no mechanism to convert insight → design task
  │     ├── CEO intervention: address root cause of bottleneck
  │     └── ★ "R1-WX cycle time đang ở X tháng. Target là Y. Trend?"
  │
Step 4: 🤖 Track compression
  │     ├── Monthly: R1-WX Speed metric
  │     ├── Quarterly: cycle time trend (compressing or expanding?)
  │     └── Annual: comparison to industry benchmarks
```

**FORGE + HELIX Integration:**
```
bridge-flywheel ORCHESTRATES:
├── bridge-signal-extract → GENERATE insights
├── bridge-knowledge-base → DELIVER insights to right people
├── HELIX skills → ACT on insights (design changes)
├── forge-validate → VALIDATE changes work
└── forge-library + bridge-cross-learn → COMPOUND across products

bridge-flywheel IS THE COMPOUND LAW IN ACTION:
├── BRIDGE health → more insights generated & delivered
├── FORGE maturity → insights become validated products faster
├── HELIX rigor → design changes are higher quality
└── ALL THREE improving → flywheel accelerates exponentially
```

---

### SKILL 7: `bridge-risk-radar` — Phát Hiện Rủi Ro Tổ Chức

**Stage:** Cross-stage
**Trigger:** "rủi ro", "risk", "warning", "vấn đề tiềm ẩn", "what could go wrong?"

**Workflow:**

```
🤖 Continuous monitoring — scan all data sources for risk signals:

ORGANIZATIONAL RISKS:
├── Key-person dependency: "Engineer X is sole owner of 3 products"
│   Source: bridge-talent-map
├── Knowledge loss risk: "Senior engineer retiring in 6 months, KB capture at 20%"
│   Source: bridge-knowledge-base gap analysis
├── Capacity overload: "25h/week split across 6 products = 4h each"
│   Source: HELIX project data
└── Skill gaps: "No one on team knows EMC simulation"
    Source: bridge-signal-extract pattern detection

PRODUCT RISKS:
├── Deployment without evidence: "Product Y at Phase 2 but Phase 0 incomplete"
│   Source: bridge-deploy-gate
├── Integration Debt accumulating: "3 products with rising ICD debt"
│   Source: helix-integration-debt
├── Fallback missing: "LOMAH-AD at Fallback Level 0"
│   Source: forge-fallback
└── Validation gap: "Model WX-DET-001 not revalidated in 6+ months"
    Source: forge-validate schedule

STRATEGIC RISKS:
├── Compound stalling: "0 model transfers in 90 days → R5 dormant"
│   Source: forge-library
├── Trust decay: "Customer Z no contact in 60+ days"
│   Source: forge-trust tracker
├── Analyst Trap: "CEO spending 80% time on analysis, 0% on prototypes"
│   Source: bridge-judgment decision log analysis
└── Shifting the Burden: "Solving symptoms not root causes 3+ times"
    Source: bridge-flywheel bottleneck patterns

OUTPUT:
├── 🔴 RED alerts: immediate action required (safety, deployment, key-person)
├── 🟡 YELLOW warnings: trending toward problem (debt, capacity, trust)
├── 🟢 GREEN: monitored, under control
└── CEO receives: weekly risk digest (3 min review)
```

---

### SKILL 8: `bridge-cross-learn` — Cross-Product Learning

**Stage:** Cross-stage (monthly sessions)
**Trigger:** "cross-product", "lessons learned", "transfer", "học từ dự án khác", "cross-learn"

**Monthly Session Protocol (60 min):**

```
PREPARATION (🤖, 30 min before):
├── Collect top 3 lessons from each active project (from helix-design-journal)
├── Pattern match: "Lesson X in Product A ≈ issue Y in Product B?"
├── Prepare cross-product insight brief
└── Identify: "Products B, C could benefit from Product A's solution"

SESSION (👤 leads, 🤖 records):
├── 15 min: Each project lead presents top lessons (3 min each)
├── 15 min: CEO + AI facilitate cross-pollination
│   ├── "Product A solved thermal issue — Product C has similar config?"
│   ├── "Manufacturing trick in MTB-20 → applicable to BB-01?"
│   └── "AI training approach in V-SMASH → transfer to LOMAH?"
├── 15 min: Action items
│   ├── Specific transfers: "Person X will apply Lesson Y to Product Z"
│   ├── Deadlines
│   └── Expected outcome
└── 15 min: Meta-review
    ├── "What patterns keep recurring? Root cause?"
    ├── "What should we formalize into KB Layer 1 (standard)?"
    └── "bridge-flywheel: are we actually acting on cross-learn insights?"

POST-SESSION (🤖):
├── Session summary → KB Layer 3
├── Action items tracked
├── Transfer success tracked (forge-library + bridge-flywheel)
└── Pattern database updated
```

**★ This is R5 (Tacit Knowledge Extraction) — currently DORMANT at Workshop X.**
**Single highest-leverage organizational practice Workshop X could implement.**

---

### SKILL 9: `bridge-dashboard` — CEO Dashboard

**Stage:** Cross-stage (CEO's primary BRIDGE view)
**Trigger:** "dashboard", "metrics", "7 con số", "how are we doing?", "weekly review"

**The 7 Metrics (15 min/week):**

```
┌──────────────────────────────────────────────────────────────┐
│          BRIDGE CEO DASHBOARD — Thứ Hai 15 Phút              │
│          ──────────────────────────────────────               │
│                                                               │
│  1. KB Coverage:        __% products documented               │
│     (Layer 1: __% | Layer 2: __% | Layer 3: __%)             │
│     Trend: ↑/↓/=  Alert if: <40% Layer 2                    │
│                                                               │
│  2. Signal Capture:     __% interactions extracted            │
│     (Design reviews: __% | Tests: __% | Field: __%)          │
│     Trend: ↑/↓/=  Alert if: <50% design reviews             │
│                                                               │
│  3. Phase Compliance:   __% products follow R-gates           │
│     (Phase 0: __ | 1: __ | 2: __ | 3: __)                   │
│     Trend: ↑/↓/=  Alert if: ANY product skipped phase       │
│                                                               │
│  4. Time Freed:         __ hrs/week automated                 │
│     Allocation: Judgment __% | Integration __% |             │
│                 Learning __% | Innovation __%                │
│     Alert if: >50% freed time goes to MORE paperwork         │
│                                                               │
│  5. Decision Quality:   __/__ decisions documented this week  │
│     With rationale: __% | With evidence: __%                 │
│     Alert if: <30% documented (judgment stock atrophying)    │
│                                                               │
│  6. R1-WX Speed:        Current: __ months | Target: __      │
│     Bottleneck: GENERATE/DELIVER/ACT/VALIDATE/COMPOUND       │
│     Trend: ↑/↓/=  Alert if: stagnant 2+ months              │
│                                                               │
│  7. Risk Radar:         🔴 __ RED | 🟡 __ YELLOW | 🟢 __    │
│     Top risk: ________________________________                │
│     Action: ________________________________                  │
│                                                               │
│  ═══════════════════════════════════════════                  │
│  COMPOUND LAW: BRIDGE __% × FORGE __% × HELIX __% = __%     │
│  Trend: ↑/↓/=   Target 3M: __% | Target 6M: __%            │
│  ═══════════════════════════════════════════                  │
│                                                               │
│  THIS WEEK'S BOTTLENECK:  B / R / I / D / G / E              │
│  ONE INTERVENTION: _______________________________            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

### SKILL 10: `bridge-talent-map` — Knowledge Risk & Talent Pipeline

**Stage:** Cross-stage
**Trigger:** "talent", "nhân sự", "key person", "ai biết cái gì?", "skill gap", "risk nếu người X nghỉ"

**Workflow:**

```
Step 1: 🤖→👤 Map current talent
  │     ├── Per person: skills, products involved, knowledge unique to them
  │     ├── Risk score: "If Person X leaves tomorrow, impact = ?"
  │     │   ├── 🔴 Catastrophic: sole owner of critical knowledge, no documentation
  │     │   ├── 🟡 High: primary owner but some KB capture done
  │     │   ├── 🟢 Manageable: knowledge distributed, KB documented
  │     └── Gap analysis: "No one knows EMC simulation → gap for all products"
  │
Step 2: 👤 Prioritize mitigation
  │     ├── Immediate: KB capture sessions for 🔴 risks
  │     ├── Medium-term: cross-training plan (person A teaches person B)
  │     └── Long-term: hiring plan for structural gaps
  │
Step 3: 🤖→👤 Monitor & update quarterly
  │     ├── Talent map updated
  │     ├── Risk scores re-assessed
  │     ├── KB capture progress tracked
  │     └── Hiring/training pipeline status
```

**★ BINDING CONSTRAINT: AI Talent (1-2 engineers).**
```
bridge-talent-map makes this VISIBLE:
"Mọi FORGE skills (validate, library, flywheel) capped by 1-2 AI engineers.
 Mọi HELIX AI-domain work capped.
 Compound Law numerator limited.
 
 CEO #1 talent action: Grow AI team to 3-4 within 12 months.
 Everything else is secondary."
```

---

## V. BRIDGE × FORGE × HELIX: COMPLETE TRI-FRAMEWORK INTEGRATION

```
╔══════════════════════════════════════════════════════════════════════╗
║              COMPLETE SKILL ARCHITECTURE: 30 SKILLS                 ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  BRIDGE (10 skills) — ORGANIZATIONAL INFRASTRUCTURE                  ║
║  ┌────────────────────────────────────────────────────────────────┐  ║
║  │ B: knowledge-base   R: deploy-gate   I: signal-extract        │  ║
║  │ D: automate         G: judgment      E: flywheel              │  ║
║  │ Cross: risk-radar, cross-learn, dashboard, talent-map         │  ║
║  └─────────────────────────┬──────────────────────────────────────┘  ║
║                             │                                        ║
║    BRIDGE provides:         │  BRIDGE receives:                      ║
║    ├ KB for all decisions   │  ├ FORGE: validate results, library    ║
║    ├ Signal data            │  ├ HELIX: design journals, sync summ.  ║
║    ├ Deployment gates       │  └ Both: metrics for dashboard         ║
║    ├ Automation infra       │                                        ║
║    ├ Judgment support       │                                        ║
║    └ Flywheel measurement   │                                        ║
║                             ▼                                        ║
║  FORGE (10 skills) — PRODUCT STRATEGY                                ║
║  ┌────────────────────────────────────────────────────────────────┐  ║
║  │ 0: scout   1: shift, fallback   2: validate, trust            │  ║
║  │ 3: library, flywheel   Cross: portfolio, cost, evolve         │  ║
║  └─────────────────────────┬──────────────────────────────────────┘  ║
║                             │                                        ║
║    FORGE provides:          │  FORGE receives:                       ║
║    ├ ACH decisions          │  ├ BRIDGE: KB, signals, deployment OK  ║
║    ├ Fallback specs         │  ├ HELIX: design artifacts, gate pass  ║
║    ├ Validation evidence    │  └ BRIDGE: freed capacity for analysis ║
║    ├ Model library          │                                        ║
║    └ Cost models            │                                        ║
║                             ▼                                        ║
║  HELIX (10 skills) — DESIGN EXECUTION                                ║
║  ┌────────────────────────────────────────────────────────────────┐  ║
║  │ 0: project-init   1: task-clarify   2: concept-generate       │  ║
║  │ 3: embody-realize   4: detail-finalize                        │  ║
║  │ Cross: sync-protocol, integration-debt, quality-gate,         │  ║
║  │        6flow-mapper, design-journal                           │  ║
║  └────────────────────────────────────────────────────────────────┘  ║
║                                                                      ║
║    HELIX provides:          HELIX receives:                          ║
║    ├ Design artifacts       ├ BRIDGE: KB context, signal data        ║
║    ├ Phase gate evidence    ├ FORGE: ACH decisions, fallback specs   ║
║    ├ Integration status     ├ FORGE: model library (solution options)║
║    └ Design decisions       └ BRIDGE: automation tools               ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  EXISTING SKILLS (execution layer — called by HELIX):                ║
║  ├ cad-visualization-freecad (CAD modeling)                          ║
║  ├ cad-review-automation (DfX checking)                              ║
║  ├ cad-documentation-generator (drawing generation)                  ║
║  ├ design-iteration-assistant (design improvement)                   ║
║  ├ quality-gate-reporter (manufacturing QC)                          ║
║  ├ pahl-beitz-mastery (learning/mentoring)                           ║
║  ├ requirements-abstraction-mentor (Phase 1 support)                 ║
║  └ engineering-concept-evaluation-assistant (Phase 2 support)        ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Data Flow Summary: What Flows Where

```
BRIDGE → FORGE:
├── KB context → forge-scout (what do we know about opportunities?)
├── KB context → forge-shift (prior similar assessments?)
├── Signal data → forge-flywheel (field data feeds model improvement)
├── Deploy gates → forge-portfolio (deployment status per product)
├── Freed capacity → forge activities (more time for strategic work)
└── Decision log → forge-evolve (strategic pattern detection)

BRIDGE → HELIX:
├── KB Layer 1 → helix-task-clarify (standards, templates)
├── KB Layer 2 → helix-concept-generate (prior solutions)
├── KB Layer 3 → all phases (lessons learned, field insights)
├── Signal data → helix-design-journal (meeting extracts)
├── Automation → all phases (doc gen, DfX checks, formatting)
└── Deploy gates → helix-quality-gate (linked phase evidence)

FORGE → BRIDGE:
├── Validate results → KB Layer 2 (evidence archive)
├── Library entries → KB Layer 2 (model catalog)
├── Trust metrics → dashboard (customer relationship health)
├── Portfolio status → dashboard + risk-radar
└── Flywheel data → bridge-flywheel (R1-WX metrics)

FORGE → HELIX:
├── ACH decisions → requirements (new constraints)
├── Fallback specs → ICD entries + requirements
├── Model availability → concept options
├── Cost data → evaluation criteria
└── Portfolio priority → resource allocation

HELIX → BRIDGE:
├── Design journals → KB Layer 2+3
├── Sync summaries → KB Layer 3
├── Quality gate results → deploy-gate evidence
├── Integration debt status → dashboard + risk-radar
└── Design decisions → decision log

HELIX → FORGE:
├── Phase status → portfolio dashboard
├── Gate pass → validation trigger (forge-validate ready)
├── Detail design → validation input (what to test)
├── Validated model → library entry trigger
└── ICD status → fallback verification
```

---

## VI. IMPLEMENTATION PRIORITY — BRIDGE

### Giai Đoạn 1 (Tuần 1-2): Foundation

```
Priority 1: bridge-knowledge-base    (EVERYTHING stands on this)
Priority 2: bridge-signal-extract    (stop losing 40 decisions/week)
Priority 3: bridge-dashboard         (CEO needs visibility NOW)
```

**Rationale:** KB + Signal Extraction addresses the TWO biggest bottlenecks (B=2/5, I=1/5). Dashboard gives CEO immediate operational awareness. Three skills alone: BRIDGE 12/30 → ~18/30.

### Giai Đoạn 2 (Tuần 3-4): Control & Intelligence

```
Priority 4: bridge-deploy-gate       (prevent uncontrolled deployment)
Priority 5: bridge-risk-radar        (early warning system)
Priority 6: bridge-talent-map        (make AI talent constraint visible)
```

### Giai Đoạn 3 (Tuần 5-6): Acceleration

```
Priority 7: bridge-automate          (free capacity for judgment)
Priority 8: bridge-judgment          (improve decision quality)
Priority 9: bridge-cross-learn       (activate R5)
Priority 10: bridge-flywheel         (measure and compress R1-WX)
```

---

## VII. COMPLETE IMPLEMENTATION ROADMAP: 30 SKILLS IN 6 WEEKS

```
WEEK 1-2: FOUNDATIONS (9 skills — 3 per framework)
═══════════════════════════════════════════════════
  BRIDGE:                FORGE:                HELIX:
  ├ knowledge-base       ├ shift               ├ project-init
  ├ signal-extract       ├ portfolio           ├ sync-protocol
  └ dashboard            └ fallback            └ integration-debt

  ★ Impact: BRIDGE 40→55%, FORGE 31→42%, HELIX 29→42%
  ★ Compound: 3.6% → ~10%
  ★ CEO gets: visibility + decision infrastructure + integration tracking

WEEK 3-4: STRUCTURE (9 skills)
══════════════════════════════
  BRIDGE:                FORGE:                HELIX:
  ├ deploy-gate          ├ validate            ├ task-clarify
  ├ risk-radar           ├ cost                ├ 6flow-mapper
  └ talent-map           └ trust               └ concept-generate

  ★ Impact: BRIDGE 55→65%, FORGE 42→55%, HELIX 42→52%
  ★ Compound: ~10% → ~19%
  ★ CEO gets: risk awareness + validation infrastructure + Phase 1-2 execution

WEEK 5-6: ACCELERATION (12 skills)
═══════════════════════════════════
  BRIDGE:                FORGE:                HELIX:
  ├ automate             ├ scout               ├ embody-realize
  ├ judgment             ├ library             ├ quality-gate
  ├ cross-learn          ├ flywheel            ├ detail-finalize
  └ flywheel             └ evolve              └ design-journal

  ★ Impact: BRIDGE 65→70%, FORGE 55→64%, HELIX 52→63%
  ★ Compound: ~19% → ~28%
  ★ CEO gets: compound engine + full design execution + evolution system
```

---

## VIII. 9 OPERATING LAWS (Nhắc Lại — Unified Across All 3 Frameworks)

```
BRIDGE LAWS:
  1. Knowledge Trước, Mọi Thứ Sau
     (KB là substrate — mọi decision/action/automation đứng trên nó)
  2. Compress Flywheel, Không Phải Headcount
     (R1-WX cycle time = competitive advantage, AI tăng tốc flywheel, không giảm người)
  3. Judgment Là Sản Phẩm, Process Là Phương Tiện
     (Workshop X bán judgment cho khách hàng, không phải paperwork)

FORGE LAWS:
  4. The Substrate Law — You cannot forge what you cannot fuel
     (Talent + Data TRƯỚC design technique)
  5. The Envelope Law — Average performance is a lie
     (Defense tests at extremes → build Performance Envelopes)
  6. The Identity Law — ACH as checklist = 20%, as identity = 100%
     ("Defense AI company that ships hardware" = target identity)

HELIX LAWS:
  7. The Topology Law — Match development topology to product topology
     (Triple Helix concurrent, not sequential pipeline)
  8. The Abstraction Ascent Law — Human value migrates upward
     (Invest in judgment skills, not tool proficiency)
  9. The Six-Flow Law — You cannot integrate what you cannot express
     (6-flow design language for 2026 products)

META-LAW (across all 3):
  THE COMPOUND LAW:
  Workshop X Value = BRIDGE health × FORGE maturity × HELIX rigor
  If ANY = 0 → TOTAL = 0
  If ALL grow 20% → TOTAL grows 73% (1.2³ = 1.73)
  Weakest framework = system bottleneck
  CEO invests across all 3, concentrated on bottleneck
```

---

## IX. CEO MASTER PROTOCOL: UNIFIED BRIDGE × FORGE × HELIX

### Daily (2 phút)

```
Sáng:
"Hôm nay tôi đang:
 BUILD knowledge (BRIDGE-B) / SCOUT opportunities (FORGE-0) /
 DESIGN product (HELIX-2/3) / VALIDATE results (FORGE-2) /
 LEARN cross-product (BRIDGE-cross) ?"

Nếu "FIX problems" 3+ ngày liên tiếp → Shifting the Burden
Nếu "ANALYZE" 3+ ngày liên tiếp → Analyst Trap
Tốt nhất: "BUILD + DESIGN" (compound)
```

### Weekly (30 phút — Thứ Hai)

```
bridge-dashboard: 7 metrics (15 min)
├── KB Coverage trend
├── Signal Capture rate
├── Phase Compliance
├── Time Freed allocation
├── Decision Quality
├── R1-WX Speed + bottleneck
└── Risk Radar top items

Quick FORGE check (10 min)
├── forge-portfolio alerts
├── Pending forge-shift decisions
└── forge-flywheel data rate

Quick HELIX check (5 min)
├── helix-integration-debt trend
├── Blocked domains?
└── Next phase transition approaching?
```

### Monthly (90 phút)

```
BRIDGE (20 min): bridge-dashboard deep review + bridge-cross-learn session prep
FORGE (20 min): forge-portfolio full review + forge-validate Stage progress
HELIX (40 min): helix-sync-protocol + helix-quality-gate review
UNIFIED (10 min): Compound Law recalculation + next month focus
```

### Quarterly (3 giờ)

```
1. Full BRIDGE + FORGE + HELIX Score reassessment (45 min)
2. Compound Law: recalculate, trend analysis (15 min)
3. forge-evolve: moat assessment + identity score (30 min)
4. bridge-talent-map: full review + hiring decisions (30 min)
5. Resource reallocation decision for next quarter (30 min)
6. Strategy validation: "Are we building the right things?" (30 min)
```

---

*BRIDGE Skill Architecture completes the BRIDGE × FORGE × HELIX triad.*

*30 total skills: BRIDGE (10) + FORGE (10) + HELIX (10), built on existing execution skills (8+).*

*Three-tier hierarchy: BRIDGE (organizational infrastructure) → FORGE (product strategy) → HELIX (design execution) → existing skills (specific task execution).*

*Implementation: 6 weeks, 9 skills per 2-week sprint, prioritized by impact on Compound Law.*

*Next steps: (1) Implement actual SKILL.md files starting with Week 1-2 foundations, (2) Create Unified Dashboard React app, (3) First bridge-cross-learn session to activate R5.*
