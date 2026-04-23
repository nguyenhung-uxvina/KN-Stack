# HELIX SKILL ARCHITECTURE v2
## Bộ Skill Đầy Đủ Theo Giai Đoạn — Phối Hợp Người-AI Cho Workshop X

**Ngày:** 01/03/2026
**Bối cảnh:** HELIX = chiều thứ 3 trong Compound Law (BRIDGE × FORGE × HELIX). Hiện tại 29% effectiveness → system bottleneck.
**Mục tiêu:** Thiết kế bộ skill phản ánh workflow thực tế theo giai đoạn Pahl-Beitz adapted cho Triple Helix (Cơ-Điện-AI), với ranh giới rõ ràng giữa việc AI làm và việc người phải làm.

---

## I. TẠI SAO CẦN REDESIGN BỘ SKILL HELIX

### Vấn Đề Hiện Tại

Bộ skill hiện tại có 2 lỗi cấu trúc:

**Lỗi 1: Skill theo CHỨC NĂNG thay vì theo GIAI ĐOẠN**

```
HIỆN TẠI (function-based):
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ pahl-beitz-  │ cad-review-  │ cad-viz-     │ design-      │
│ mastery      │ automation   │ freecad      │ iteration    │
│ (learning)   │ (DfX check)  │ (CAD model)  │ (improve)    │
└──────────────┴──────────────┴──────────────┴──────────────┘
          ↑ Không biết mình đang ở Phase nào
          ↑ Không biết ai (người/AI) làm bước nào
          ↑ Không có sync protocol giữa 3 domain
```

**Lỗi 2: Thiếu Human-AI Handoff Protocol**

Mỗi skill giả định toàn bộ do AI làm hoặc toàn bộ do người làm. Thực tế: mỗi bước trong design process cần MỘT PHÂN CÔNG CỤ THỂ — ai tạo draft, ai review, ai quyết định, ai execute.

### Thiết Kế Mới: Phase-Based + Role-Based

```
THIẾT KẾ MỚI (phase-based):

Phase 0          Phase 1           Phase 2            Phase 3           Phase 4
PROJECT SETUP    TASK CLARIFY      CONCEPTUAL         EMBODIMENT        DETAIL DESIGN
                                   DESIGN             DESIGN            
┌──────────┐    ┌──────────┐     ┌──────────┐      ┌──────────┐     ┌──────────┐
│ helix-   │───▶│ helix-   │────▶│ helix-   │─────▶│ helix-   │────▶│ helix-   │
│ project- │    │ task-    │     │ concept- │      │ embody-  │     │ detail-  │
│ init     │    │ clarify  │     │ generate │      │ realize  │     │ finalize │
└──────────┘    └──────────┘     └──────────┘      └──────────┘     └──────────┘
                     │                │                  │                │
                     ▼                ▼                  ▼                ▼
              ┌──────────────────────────────────────────────────────────────┐
              │              CROSS-PHASE SKILLS (always available)           │
              │  helix-sync-protocol  │  helix-integration-debt  │  helix-  │
              │  (monthly sync)       │  (ICD tracking)          │  quality │
              │                       │                          │  gate    │
              └──────────────────────────────────────────────────────────────┘
```

---

## II. HUMAN-AI COLLABORATION MODEL: PHIÊN HỢP TÁC

Mỗi bước thiết kế có 4 vai trò khả thi:

| Ký hiệu | Vai trò | Nghĩa |
|:--------:|---------|-------|
| 🤖 | **AI Generates** | AI tạo draft/output đầu tiên |
| 👤 | **Human Generates** | Người tạo nội dung gốc (AI không thể) |
| 🤖→👤 | **AI Draft → Human Decides** | AI đề xuất, người phê duyệt/sửa |
| 👤→🤖 | **Human Specifies → AI Executes** | Người ra spec, AI thực hiện |

**Nguyên tắc phân công:**

```
AI LÀM TỐT (delegate):              NGƯỜI PHẢI LÀM (non-delegable):
─────────────────────────             ──────────────────────────────
✓ Tra cứu tiêu chuẩn                ✗ Xác định nhu cầu khách hàng thực
✓ Generate checklist từ template      ✗ Quyết định trade-off chiến lược
✓ Tạo function structure draft        ✗ Đánh giá dựa trên kinh nghiệm thực địa
✓ Chạy DfX check                     ✗ Phê duyệt ICD changes
✓ Tạo CAD geometry từ spec           ✗ Validate mô phỏng vs. thực tế
✓ Generate documentation              ✗ Quyết định go/no-go
✓ Track Integration Debt              ✗ Giải quyết xung đột giữa domains
✓ So sánh phương án theo tiêu chí    ✗ Chọn phương án khi tiêu chí conflict
✓ Draft requirements từ similar prods ✗ Requirements mới chưa có precedent
✓ Tính toán, mô phỏng                ✗ Validation vật lý (bắn thử, đo đạc)
```

---

## III. BỘ SKILL ĐẦY ĐỦ: 10 SKILLS

### Tổng Quan

| # | Skill Name | Phase | Mục đích | Vai trò chính |
|:-:|-----------|:-----:|----------|:-------------:|
| 1 | `helix-project-init` | 0 | Khởi tạo dự án Triple Helix | 🤖→👤 |
| 2 | `helix-task-clarify` | 1 | Làm rõ yêu cầu & abstraction | 🤖→👤 |
| 3 | `helix-concept-generate` | 2 | Tạo & đánh giá phương án | 🤖→👤 |
| 4 | `helix-embody-realize` | 3 | Thiết kế chi tiết hình dáng + layout | 👤→🤖 |
| 5 | `helix-detail-finalize` | 4 | Hoàn thiện bản vẽ chế tạo | 👤→🤖 |
| 6 | `helix-sync-protocol` | Cross | Monthly sync giữa 3 domains | 🤖→👤 |
| 7 | `helix-integration-debt` | Cross | Track & manage ICD | 🤖 (track) + 👤 (resolve) |
| 8 | `helix-quality-gate` | Cross | Phase gate review | 🤖→👤 |
| 9 | `helix-6flow-mapper` | 1-2 | Function structure 6-flow | 🤖→👤 |
| 10 | `helix-design-journal` | Cross | Design decision log | 👤→🤖 (format) |

---

## IV. CHI TIẾT TỪNG SKILL

---

### SKILL 1: `helix-project-init` — Khởi Tạo Dự Án

**Phase:** 0 (trước khi bắt đầu thiết kế)
**Trigger:** "khởi tạo dự án", "init project", "bắt đầu thiết kế [tên sản phẩm]", "new HELIX project"

**Workflow:**

```
Input: Tên sản phẩm + mô tả sơ bộ
  │
  ▼
Step 1: 🤖 Generate project template
  │     ├── Project ID, tên, mô tả
  │     ├── Domain map: Cơ khí / Điện tử / AI-SW
  │     ├── Clock speed estimate cho mỗi domain
  │     ├── Suggested sync point schedule (monthly)
  │     └── Initial ICD skeleton
  │
  ▼
Step 2: 👤 Review & adjust
  │     ├── Xác nhận scope: sản phẩm mới / cải tiến / variant?
  │     ├── Xác nhận domains involved (có thể chỉ 2/3)
  │     ├── Assign domain leads (hoặc flag nếu 1 người kiêm nhiều)
  │     └── Set milestone dates: first sync, prototype target, delivery
  │
  ▼
Step 3: 🤖 Generate project charter document
  │     ├── 1-page project brief (Obsidian template)
  │     ├── Triple Helix timeline (ASCII hoặc Mermaid)
  │     ├── ICD v0 (empty template, sections per interface)
  │     └── Sync calendar (12 months, monthly)
  │
  ▼
Output: Project charter + ICD v0 + sync calendar
```

**AI Generates:**
- Project template từ database sản phẩm tương tự (FORGE model library)
- Clock speed estimate dựa trên product complexity class
- Standard ICD template cho loại sản phẩm (sensor/weapon/vehicle/C4ISR)

**Human Must:**
- Xác nhận scope và constraints thực tế
- Assign resources (ai làm domain nào)
- Set realistic milestones dựa trên capacity thực (25h/week)

**Integration:**
- Feeds into: `helix-task-clarify`, `helix-sync-protocol`, `helix-integration-debt`
- Reads from: FORGE product portfolio (nếu sản phẩm nằm trong portfolio đã có)
- Updates: BRIDGE KB Layer 1 (project registered)

**Output Files:**
```
[PROJECT_ID]/
├── PROJECT_CHARTER.md        (1-page brief)
├── TRIPLE_HELIX_TIMELINE.md  (phase map per domain)
├── ICD_v0.md                 (interface control doc skeleton)
├── SYNC_CALENDAR.md          (12-month sync schedule)
└── DECISION_LOG.md           (empty, first entry = "project initiated")
```

---

### SKILL 2: `helix-task-clarify` — Làm Rõ Yêu Cầu

**Phase:** 1 (Task Clarification — Pahl-Beitz Phase 1)
**Trigger:** "làm rõ yêu cầu", "task clarification", "requirements list", "abstract requirements", "xác định vấn đề cốt lõi"

**Workflow:**

```
Input: Project charter + stakeholder inputs + standards
  │
  ▼
Step 1: 🤖 Draft requirements list
  │     ├── Scrape relevant standards (MIL-STD, TCVN, STANAG)
  │     ├── Pull requirements from similar products (FORGE library)
  │     ├── Generate 50-80 requirement candidates
  │     ├── Classify: D (demand) / W (wish) + priority
  │     └── Flag gaps: "missing thermal?" "missing EMC?" "missing lifecycle?"
  │
  ▼
Step 2: 👤 Review & validate
  │     ├── Thêm requirements từ khách hàng thực (cuộc họp, field trips)
  │     ├── Phân loại lại D/W dựa trên kinh nghiệm thực chiến
  │     ├── Xóa requirements không phù hợp bối cảnh VN
  │     └── Xác nhận: "Đây có đúng là vấn đề cần giải chưa?"
  │
  ▼
Step 3: 🤖 Abstraction (5-step P&B process)
  │     ├── Bước 1: Bỏ nguyện vọng cá nhân
  │     ├── Bước 2: Bỏ yêu cầu không liên quan hệ thống tổng
  │     ├── Bước 3: Chuyển định lượng → định tính
  │     ├── Bước 4: Khái quát hóa
  │     └── Bước 5: Phát biểu vấn đề trung lập với giải pháp
  │
  ▼
Step 4: 👤 Validate essential problem statement
  │     ├── "Nếu giải đúng vấn đề này, mọi thứ khác follow?"
  │     ├── Check: vấn đề có đủ rộng cho nhiều giải pháp?
  │     └── CEO gut-check: "Khách hàng có đồng ý đây là vấn đề?"
  │
  ▼
Step 5: 🤖→👤 Generate 6-flow function structure (link to helix-6flow-mapper)
  │
  ▼
Output: Requirements list v1 + Essential problem statement + Function structure draft
```

**Cross-Domain Protocol:**
```
             CƠ KHÍ                 ĐIỆN TỬ                AI/SW
             ──────                 ───────                ─────
Phase 1:     Requirements           Requirements           Requirements
             cơ-nhiệt-bền          EMC-power-thermal      accuracy-latency-data

SYNC S1:  ──────────── ALIGN REQUIREMENTS ────────────────────
          "Có conflict giữa kích thước cơ khí và PCB layout?"
          "AI cần data từ sensor nào? Sensor đó trong spec điện tử chưa?"
          "Thermal budget phân bổ thế nào giữa 3 domain?"
```

**AI Generates:**
- Requirements draft từ standard databases
- Abstraction steps (template-driven)
- Gap analysis ("8/10 similar products có requirement X, bạn chưa có")
- Cross-reference matrix: requirement ↔ standard ↔ test method

**Human Must:**
- Requirements từ khách hàng thực (field interviews, operational context)
- D/W classification dựa trên hiểu biết chiến lược
- Essential problem validation ("đây có phải vấn đề thật không?")
- Cross-domain trade-off decisions khi requirements conflict

**Integration:**
- Uses: `requirements-abstraction-mentor` (existing skill, subsume partially)
- Feeds: `helix-concept-generate`, `helix-6flow-mapper`
- Updates: ICD v1 (interface requirements identified)

---

### SKILL 3: `helix-concept-generate` — Tạo & Đánh Giá Phương Án

**Phase:** 2 (Conceptual Design — Pahl-Beitz Phase 2)
**Trigger:** "tạo phương án", "conceptual design", "morphological matrix", "đánh giá phương án", "VDI 2225", "concept generation"

**Workflow:**

```
Input: Function structure + requirements list + essential problem
  │
  ▼
Step 1: 🤖 Generate solution space
  │     ├── Morphological matrix (sub-functions × solution principles)
  │     ├── Auto-populate từ FORGE model library (existing solutions)
  │     ├── Suggest novel principles từ patent databases / papers
  │     └── Flag ACH opportunities: "sub-function X = candidate cho AI replacement"
  │
  ▼
Step 2: 👤 Creative input
  │     ├── Thêm solution principles từ kinh nghiệm (không có trong database)
  │     ├── Sketch concepts bằng tay hoặc verbal description
  │     ├── Identify "dark horse" concepts (counterintuitive combinations)
  │     └── Decide: bao nhiêu phương án evaluate? (recommend 3-5)
  │
  ▼
Step 3: 🤖 Evaluate concepts
  │     ├── VDI 2225 evaluation matrix
  │     ├── Auto-score criteria có thể tính (weight, cost estimate, part count)
  │     ├── Generate sensitivity analysis (thay đổi weight → ranking đổi không?)
  │     └── ★ COUPLING ANALYSIS: mỗi phương án couple Cơ-Điện-AI thế nào?
  │         ├── Coupling Score: 0 (independent) → 10 (tightly coupled)
  │         ├── Interface count per concept
  │         └── "Concept B có 3 interfaces, Concept C có 7 → B dễ integrate hơn"
  │
  ▼
Step 4: 👤 Select concept
  │     ├── Review VDI 2225 results + coupling analysis
  │     ├── Gut-check: "Nếu manufacturing fail, concept nào có fallback tốt nhất?"
  │     ├── Strategic alignment: concept nào build model library tốt nhất?
  │     └── ★ GO/NO-GO DECISION: Concept chọn → Phase 3
  │
  ▼
Output: Chosen concept + evaluation report + coupling analysis + decision rationale
```

**Cross-Domain Protocol:**
```
             CƠ KHÍ                 ĐIỆN TỬ                AI/SW
             ──────                 ───────                ─────
Phase 2:     Cơ cấu concept        Circuit topology       Algorithm approach
             3-5 layouts            2-3 architectures      2-3 pipelines

SYNC S3:  ──────────── CONCEPT COMPATIBILITY CHECK ──────────
          "Concept cơ khí B có chỗ cho PCB architecture 2 không?"
          "AI pipeline 1 cần GPU → thermal impact lên cơ khí?"
          "Nếu chọn Concept C, điện tử cần thay architecture không?"
          
          ★ OUTPUT: Concept COMBINATION matrix (Cơ × Điện × AI)
            Ví dụ: Cơ-B + Điện-2 + AI-1 = compatible, coupling = 4
                    Cơ-C + Điện-1 + AI-3 = incompatible (thermal conflict)
```

**AI Generates:**
- Morphological matrix draft with existing solution principles
- VDI 2225 evaluation with auto-scorable criteria
- Coupling analysis giữa domain combinations
- Sensitivity analysis (which criteria changes flip the ranking?)

**Human Must:**
- Novel solution principles từ domain expertise
- Creative concept sketches (AI can't imagine hardware yet)
- Evaluate intangibles: manufacturability cảm tính, operational experience
- Final concept selection (trade-off judgment)

**Integration:**
- Uses: `engineering-concept-evaluation-assistant` (existing, enhance with coupling)
- Uses: `helix-6flow-mapper` (function structure input)
- Feeds: `helix-embody-realize`, ICD v2 (interfaces specified per chosen concept)

---

### SKILL 4: `helix-embody-realize` — Thiết Kế Hình Dáng

**Phase:** 3 (Embodiment Design — Pahl-Beitz Phase 3)
**Trigger:** "embodiment design", "thiết kế hình dáng", "layout", "preliminary design", "DfX check", "embody"

**Workflow:**

```
Input: Chosen concept + ICD v2 + requirements
  │
  ▼
Step 1: 👤 Preliminary layout sketching
  │     ├── Hand sketches hoặc rough CAD (kỹ sư cơ khí)
  │     ├── Schematic draft (kỹ sư điện tử)
  │     ├── Software architecture doc (kỹ sư AI)
  │     └── Mỗi domain CỤ THỂ HÓA concept thành hình dáng sơ bộ
  │
  ▼
Step 2: 🤖 DfX Review tự động
  │     ├── Invoke cad-review-automation
  │     ├── DfM: wall thickness, radii, tolerance feasibility
  │     ├── DfA: assembly sequence, fastener count
  │     ├── DfR: failure modes, redundancy
  │     ├── DfT: test access points, sensor placement
  │     └── ★ DfU (Design for Update): AI model swap paths, firmware ports
  │
  ▼
Step 3: 🤖→👤 Integration check
  │     ├── Compare layout vs. ICD: "PCB outline fit vào vỏ chưa?"
  │     ├── Thermal simulation estimate: "GPU 15W + motor 5W → cần heatsink?"
  │     ├── Cable routing feasibility
  │     ├── Connector compatibility check
  │     └── ★ Update ICD v3 (dimensions, connectors, thermal boundaries)
  │
  ▼
Step 4: 👤 Design decisions
  │     ├── Resolve DfX issues (tradeoff: thicker wall → heavier → ok?)
  │     ├── Resolve integration conflicts
  │     ├── Material selection decisions
  │     └── ★ CRITICAL: Approve ICD v3 freeze for affected interfaces
  │
  ▼
Step 5: 👤→🤖 Detailed CAD modeling
  │     ├── Invoke cad-visualization-freecad (người spec → AI model)
  │     ├── Generate part drawings
  │     ├── Assembly model
  │     └── Manufacturing drawings draft
  │
  ▼
Step 6: 🤖 Documentation
  │     ├── Invoke cad-documentation-generator
  │     ├── Drawing list
  │     ├── BOM draft
  │     └── Inspection checklist draft
  │
  ▼
Output: Preliminary CAD + DfX report + ICD v3 + BOM draft
```

**Cross-Domain Protocol:**
```
SYNC S5 (CRITICAL — First Hardware Available for AI):
──────────────────────────────────────────────────────
"First mechanical prototype ready → AI team can START physical testing"
"Before this sync: AI only tested on simulation/synthetic data"
"After this sync: Real sensor noise, real vibration, real thermal"

CEO CHECK:
├── "AI team đang test trên data thật hay vẫn synthetic?"
├── "Hardware prototype có đúng timeline không?"
└── "Nếu hardware delay → AI team bị block → track as Integration Debt"
```

**AI Does:**
- DfX automated review
- CAD modeling từ human specs
- Integration compatibility checks (ICD vs. actual dimensions)
- Documentation generation
- BOM extraction

**Human Must:**
- Initial layout creation (spatial arrangement is judgment)
- Resolve DfX trade-offs (lighter vs. stronger vs. cheaper)
- Integration conflict resolution (which domain adapts?)
- ICD freeze approval (irreversible decisions)
- Material and manufacturing process selection

---

### SKILL 5: `helix-detail-finalize` — Hoàn Thiện Chế Tạo

**Phase:** 4 (Detail Design — Pahl-Beitz Phase 4)
**Trigger:** "detail design", "hoàn thiện bản vẽ", "chế tạo", "manufacturing drawings", "production ready"

**Workflow:**

```
Input: Approved embodiment design + ICD v3 + BOM
  │
  ▼
Step 1: 👤→🤖 Final CAD completion
  │     ├── Complete all manufacturing features (chamfers, fillets, threads)
  │     ├── Add GD&T annotations
  │     ├── Generate production drawing set
  │     └── Export manufacturing files (STEP, DXF, G-code if applicable)
  │
  ▼
Step 2: 🤖 Final DfX check + documentation
  │     ├── Full DfX re-check on final geometry
  │     ├── Complete BOM with part numbers, vendors, costs
  │     ├── Inspection checklist finalized
  │     ├── Assembly instructions generated
  │     └── Test procedure draft
  │
  ▼
Step 3: 👤 Manufacturing review
  │     ├── Review with workshop master/machinists
  │     ├── Discuss tolerances, surface finish requirements
  │     ├── Confirm material availability
  │     └── ★ SIGN-OFF: "Bản vẽ này gia công được"
  │
  ▼
Step 4: 🤖→👤 Quality gate (link to helix-quality-gate)
  │     ├── Phase 4 gate checklist
  │     ├── All DfX passed?
  │     ├── All ICD interfaces resolved?
  │     ├── Integration Debt = 0 for this phase?
  │     └── ★ GO/NO-GO: Release for manufacturing
  │
  ▼
Output: Manufacturing drawing package + BOM + inspection checklist + test procedures
```

**Human Must:**
- Manufacturing feasibility confirmation (experience-based)
- GD&T decisions on critical dimensions (judgment)
- Final sign-off (accountability)

**AI Does:**
- CAD completion from human-approved layouts
- Drawing generation and formatting
- BOM compilation
- Inspection checklist from standards
- Cross-check: BOM vs. drawing vs. ICD consistency

---

### SKILL 6: `helix-sync-protocol` — Đồng Bộ Giữa 3 Domain

**Phase:** Cross-phase (monthly, throughout project)
**Trigger:** "sync", "đồng bộ domain", "monthly review", "integration sync", "helix sync"

**Workflow:**

```
BEFORE SYNC (🤖 prepares):
├── Collect status from each domain lead (or from project files)
├── Generate sync brief:
│   ├── Phase per domain: "Cơ khí: Embodiment 60%, Điện: Concept 90%, AI: Sprint 8/18"
│   ├── ICD status: "12 interfaces defined, 3 open, 2 changed since last sync"
│   ├── Integration Debt summary: "5 items, 2 critical"
│   ├── Assumptions list: "7 unverified assumptions, 3 overdue"
│   └── Risk flags: "AI blocked waiting for PCB pinout → 2 weeks delay risk"
│
DURING SYNC (👤 leads, 🤖 records):
├── 15 min: Each domain reports (3×5 min)
│   ├── What was done since last sync
│   ├── What's blocked
│   └── What assumption needs verification
├── 15 min: Integration discussion
│   ├── Review ICD changes
│   ├── Resolve blocking conflicts
│   └── Update assumptions (verified/invalidated/new)
├── 10 min: Next period planning
│   ├── Who delivers what by next sync
│   └── Which interfaces freeze next
│
AFTER SYNC (🤖 documents):
├── Sync summary → BRIDGE KB Layer 3
├── ICD updated → helix-integration-debt
├── Decision log entries → helix-design-journal
├── Action items with owners and deadlines
└── Updated Triple Helix timeline
```

**CEO Role in Sync:**
```
CEO DOESN'T:                          CEO DOES:
─────────────                         ─────────
✗ Solve technical problems            ✓ Ensure sync HAPPENS monthly
✗ Decide interface specifications     ✓ Ask: "Integration Debt trending up or down?"
✗ Choose between domain solutions     ✓ Ask: "How many unverified assumptions?"
✗ Assign technical tasks              ✓ Escalate if any domain is > 1 month behind
                                      ✓ Ask: "AI team testing on real data yet?"
```

---

### SKILL 7: `helix-integration-debt` — Quản Lý Interface Control

**Phase:** Cross-phase (continuous)
**Trigger:** "ICD", "integration debt", "interface", "nợ tích hợp", "interface control"

**Structure:**

```
ICD Document Structure:
├── Interface Registry
│   ├── IF-001: Cơ khí ↔ Điện tử (mounting, connectors, thermal)
│   ├── IF-002: Điện tử ↔ AI/SW (data bus, signal format, latency)
│   ├── IF-003: Cơ khí ↔ AI/SW (sensor mounting, actuator interface)
│   └── IF-004: System ↔ Environment (IP rating, temperature, vibration)
│
├── Per Interface:
│   ├── Status: 🔴 Undefined / 🟡 Draft / 🟢 Agreed / 🔵 Frozen
│   ├── Owner: Who resolves if conflict
│   ├── Spec: What exactly crosses this interface
│   ├── Assumptions: What we assumed (with verification deadline)
│   └── History: Changes log with date + reason
│
├── Integration Debt Tracker
│   ├── Item, severity, owner, deadline
│   ├── Trend: ↑ increasing / ↓ decreasing / = stable
│   └── ★ Alert if debt items > 10 or trend ↑ for 2+ syncs
│
└── Metrics:
    ├── Total interfaces: N
    ├── Frozen: X% (target: 80% by Phase 3 end)
    ├── Open debt items: Y (target: 0 by Phase 4)
    └── Average time to resolve: Z days
```

**AI Does:**
- Track all interface statuses
- Flag inconsistencies ("ICD says connector A, but CAD shows connector B")
- Generate debt trend charts
- Alert when debt threshold exceeded

**Human Must:**
- Resolve conflicts between domains
- Decide interface specifications
- Approve interface freeze (irreversible)
- Verify assumptions (requires physical testing or supplier confirmation)

---

### SKILL 8: `helix-quality-gate` — Phase Gate Review

**Phase:** Cross-phase (at end of each P&B phase)
**Trigger:** "quality gate", "phase gate", "gate review", "ready for next phase?", "kiểm tra gate"

**Gate Checklists:**

```
GATE 1: Task Clarification → Conceptual Design
─────────────────────────────────────────────────
🤖 Auto-check:
├── [ ] Requirements list complete (≥ 40 items)
├── [ ] All D requirements have test method specified
├── [ ] Standards referenced and available
├── [ ] 6-flow function structure exists
├── [ ] Cross-domain requirements aligned (from Sync S1)
👤 Human judgment:
├── [ ] Essential problem statement validated with customer
├── [ ] CEO confirms: "Đây là sản phẩm đúng cho thị trường này"
├── [ ] Domain leads confirm: "Yêu cầu feasible trong capacity hiện tại"

GATE 2: Conceptual Design → Embodiment Design
──────────────────────────────────────────────
🤖 Auto-check:
├── [ ] ≥ 3 concepts evaluated
├── [ ] VDI 2225 scoring complete with sensitivity analysis
├── [ ] Coupling analysis for cross-domain combinations
├── [ ] Morphological matrix documented
├── [ ] Concept combination compatibility verified
👤 Human judgment:
├── [ ] Chosen concept has clear ACH advantage (FORGE alignment)
├── [ ] Manufacturing feasibility confirmed (workshop capacity)
├── [ ] CEO confirms: "Risk level acceptable for this product"

GATE 3: Embodiment Design → Detail Design
──────────────────────────────────────────
🤖 Auto-check:
├── [ ] DfX review: 0 critical issues remaining
├── [ ] ICD: ≥ 80% interfaces frozen
├── [ ] Integration Debt: trend ↓
├── [ ] CAD model complete for all domains
├── [ ] BOM draft with cost estimate
👤 Human judgment:
├── [ ] Workshop master confirms: "Gia công được"
├── [ ] Test plan realistic with available equipment
├── [ ] CEO confirms: "Budget approved for prototype"

GATE 4: Detail Design → Manufacturing
──────────────────────────────────────
🤖 Auto-check:
├── [ ] All manufacturing drawings complete
├── [ ] BOM final with part numbers
├── [ ] Inspection checklist complete
├── [ ] Assembly instructions complete
├── [ ] Integration Debt = 0
├── [ ] All ICD interfaces frozen
👤 Human judgment:
├── [ ] All materials procured or orderable
├── [ ] Workshop schedule confirmed
├── [ ] Test equipment available
├── [ ] CEO FINAL GO: "Chế tạo"
```

**AI Does:**
- Run automated checklist against project files
- Score completion percentage
- Identify gaps and blockers
- Generate gate review report

**Human Must:**
- Judgment calls that require domain expertise
- GO/NO-GO decisions
- Risk acceptance
- Resource commitment

---

### SKILL 9: `helix-6flow-mapper` — Function Structure 6-Flow

**Phase:** 1-2 (used in Task Clarification and Conceptual Design)
**Trigger:** "function structure", "6-flow", "cấu trúc chức năng", "flows", "energy material signal data computation trust"

**The 6 Flows:**

```
TRUYỀN THỐNG (3-flow):              EXTENDED (6-flow cho sản phẩm 2026):
─────────────────────                ──────────────────────────────────────
1. Energy (E)                        1. Energy (E) — Năng lượng
2. Material (M)                      2. Material (M) — Vật chất
3. Signal (S)                        3. Signal (S) — Tín hiệu (analog)
                                     4. Data (D) — Dữ liệu (digital, AI)
                                     5. Computation (C) — Xử lý (AI inference)
                                     6. Trust (T) — Tin cậy (human oversight)
```

**Why 6 flows matter for Workshop X:**

```
Ví dụ: V-SMASH System

3-FLOW FUNCTION STRUCTURE (thiếu):
[Detect target] ──Signal──▶ [Process] ──Signal──▶ [Display] ──Signal──▶ [Fire command]

6-FLOW FUNCTION STRUCTURE (đầy đủ):
[Detect target]  ──Signal──▶ [Digitize]  ──Data──▶   [AI Classify] ──Computation──▶
    │                            │                        │
    └──Energy──                  └──Data──                └──Trust──▶ [Human Confirm]
                                                                          │
                                                          Trust──▶ [Fire Authorize]
                                                                          │
                                                          Signal──▶ [Fire Command]

★ Trust flow FORCES the design to include human oversight
★ Computation flow REVEALS where AI inference happens (= ACH opportunity)
★ Data flow SEPARATES from Signal flow (different reliability requirements)
```

**Workflow:**

```
Step 1: 🤖 Generate 6-flow draft from requirements + product description
Step 2: 👤 Review, add missing functions, correct flow types
Step 3: 🤖 Render clean diagram (Mermaid or ASCII)
Step 4: 👤 Validate: "Mỗi function box — ai implement? Cơ/Điện/AI?"
Step 5: 🤖→👤 Map functions to domains → reveals INTERFACE points → feeds ICD
```

---

### SKILL 10: `helix-design-journal` — Nhật Ký Thiết Kế

**Phase:** Cross-phase (every design session)
**Trigger:** "design journal", "nhật ký thiết kế", "log decision", "ghi lại", "end of session"

**Template Per Entry:**

```markdown
## [DATE] — Design Session Log

**Project:** [ID]
**Phase:** [1-4]
**Domain:** [Cơ/Điện/AI/Cross]
**Duration:** [hours]
**Người thực hiện:** [name]

### Quyết Định Hôm Nay
1. [Decision] — Lý do: [why] — Alternatives rejected: [what, why not]

### Interface Impact
- ICD changes: [none / IF-XXX updated]
- Assumptions added/verified: [list]

### Integration Debt
- New items: [list]
- Resolved items: [list]

### Blocked / Cần Hỗ Trợ
- [What's blocked, from whom]

### CEO Notes (nếu CEO review)
- [Quick observation]

### AI-Assisted Work This Session
- [What AI generated, what human modified]
```

**AI Does:**
- Generate template pre-filled from project context
- Auto-link to ICD entries when interfaces mentioned
- Summarize weekly/monthly for sync prep
- Extract patterns: "70% of decisions in Phase 3 involve thermal trade-offs"

**Human Must:**
- Record actual decisions and rationale
- Document what was rejected and why (institutional memory)
- Flag integration concerns honestly

---

## V. SKILL DEPENDENCY MAP

```
                          PROJECT LIFECYCLE
    ═══════════════════════════════════════════════════════
    Phase 0         Phase 1          Phase 2          Phase 3          Phase 4
    
    helix-         helix-           helix-           helix-           helix-
    project-  ───▶ task-     ──────▶concept-  ──────▶embody-   ──────▶detail-
    init           clarify          generate         realize          finalize
      │              │                │                │                │
      │              ▼                │                │                │
      │          helix-              │                │                │
      │          6flow-  ────────────┘                │                │
      │          mapper                               │                │
      │                                               │                │
      └──────────────────────────────────────────────────────────────────
                           │                │                │
                     ┌─────┴─────┐    ┌─────┴─────┐   ┌─────┴─────┐
                     │ helix-    │    │ helix-    │   │ helix-    │
                     │ sync-    │    │ integr-  │   │ quality- │
                     │ protocol │    │ debt     │   │ gate     │
                     └───────────┘    └───────────┘   └───────────┘
                                          │
                                    ┌─────┴─────┐
                                    │ helix-    │
                                    │ design-  │
                                    │ journal  │
                                    └───────────┘

    EXTERNAL INTEGRATIONS:
    ──────────────────────
    ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
    │ EXISTING SKILLS │     │ BRIDGE          │     │ FORGE           │
    │ ───────────────│     │ ──────          │     │ ─────           │
    │ cad-viz-freecad│◄────│ KB Layer 1-3    │     │ Model Library   │
    │ cad-review-auto│     │ Signal Extract  │     │ Product Portfolio│
    │ cad-doc-gen    │     │ Decision Guide  │     │ ACH Checklist   │
    │ quality-gate   │     └─────────────────┘     └─────────────────┘
    │ pahl-beitz-mas │
    │ req-abstract   │
    └─────────────────┘
```

---

## VI. RELATIONSHIP TO EXISTING SKILLS

| Existing Skill | Relationship to HELIX | Action |
|---------------|----------------------|--------|
| `pahl-beitz-mastery` | Overlap: Phase 1-4 methodology → **Subsume into HELIX phase skills** | Keep for learning; HELIX skills for execution |
| `requirements-abstraction-mentor` | Subset of `helix-task-clarify` Step 3 | Call from within helix-task-clarify |
| `cad-review-automation` | Tool used BY `helix-embody-realize` Step 2 | Keep as-is, invoke from HELIX |
| `cad-visualization-freecad` | Tool used BY `helix-embody-realize` Step 5 | Keep as-is, invoke from HELIX |
| `cad-documentation-generator` | Tool used BY `helix-detail-finalize` Step 2 | Keep as-is, invoke from HELIX |
| `design-iteration-assistant` | Operates within Phase 3-4 iteration loops | Keep as-is, invoke from HELIX |
| `quality-gate-reporter` | Manufacturing gate → `helix-quality-gate` expands to all phases | Enhance or replace |
| `engineering-concept-evaluation-assistant` | Subset of `helix-concept-generate` Step 3 | Call from within helix-concept-generate |

**Principle:** HELIX skills are **orchestrators** that call existing skills as tools. Existing skills remain as specialized executors.

---

## VII. IMPLEMENTATION PRIORITY

### Giai Đoạn 1 (Tuần 1-2): 3 Core Skills

```
Priority 1: helix-project-init        (enables everything else)
Priority 2: helix-sync-protocol       (the #1 missing capability)
Priority 3: helix-integration-debt     (tracks the hidden killer)
```

**Rationale:** Sync protocol và Integration Debt tracking là 2 thứ Workshop X CHƯA BAO GIỜ CÓ. Project init chuẩn hóa how projects start. Ba skill này alone sẽ improve HELIX Score from 29% → ~45%.

### Giai Đoạn 2 (Tuần 3-4): Phase 1-2 Skills

```
Priority 4: helix-task-clarify         (Phase 1 — most mature methodology)
Priority 5: helix-6flow-mapper         (6-flow is Workshop X's unique advantage)
Priority 6: helix-concept-generate     (Phase 2 — includes coupling analysis)
```

### Giai Đoạn 3 (Tuần 5-6): Phase 3-4 + Support

```
Priority 7: helix-embody-realize       (Phase 3 — orchestrates existing CAD skills)
Priority 8: helix-quality-gate         (all phase gates formalized)
Priority 9: helix-detail-finalize      (Phase 4 — manufacturing package)
Priority 10: helix-design-journal      (continuous, lowest urgency)
```

---

## VIII. HELIX SCORE v2: METRICS THAT REFLECT THE NEW SKILL SET

| Dimension | Metric | Current | Target 3M | Target 6M | Measured How |
|-----------|--------|:-------:|:---------:|:---------:|-------------|
| **T** — Methodology | % projects using Triple Helix | 0% | 50% | 100% | helix-project-init records |
| **H** — Harmonize | Integration Debt trend | Unknown | Measured | ↓ monthly | helix-integration-debt |
| **I** — Identify | % designs using 6-flow | 0% | 30% | 80% | helix-6flow-mapper usage |
| **Ế** — Evaluate | % concepts with coupling analysis | 0% | 50% | 100% | helix-concept-generate |
| **T** — Transpose | Average DfX critical issues at Phase 4 | Unknown | < 5 | < 2 | helix-quality-gate |
| **K** — Keep Updatable | % products with DfU score | 0% | 2 products | 5 products | helix-embody-realize |
| **Ế** — Evolve | Sync points held on schedule | 0% | 80% | 100% | helix-sync-protocol |

**HELIX Composite Score = sum of dimension scores (each 1-5) / 35**

**Bands:**
- 0-10/35 (< 29%): **THÔ** — No systematic method → hiện tại
- 11-18/35 (31-51%): **ĐANG CHUYỂN ĐỔI** — Some practices adopted
- 19-25/35 (54-71%): **HOẠT ĐỘNG** — Triple Helix running, debt managed
- 26-35/35 (74-100%): **TINH LUYỆN** — Design method creates competitive advantage

---

## IX. COMPOUND LAW IMPACT PROJECTION

```
HIỆN TẠI:
  BRIDGE: 12/30 = 40%
  FORGE:  7.8/25 = 31%
  HELIX:  ~10/35 = 29%
  COMPOUND: 0.40 × 0.31 × 0.29 = 0.036 = 3.6%  ← hầu như zero value

SAU 3 THÁNG (với HELIX skill set):
  BRIDGE: 15/30 = 50%   (+25%)
  FORGE:  10/25 = 40%   (+29%)
  HELIX:  16/35 = 46%   (+59%)  ← biggest improvement
  COMPOUND: 0.50 × 0.40 × 0.46 = 0.092 = 9.2%  ← 2.6× improvement

SAU 6 THÁNG:
  BRIDGE: 18/30 = 60%
  FORGE:  14/25 = 56%
  HELIX:  22/35 = 63%
  COMPOUND: 0.60 × 0.56 × 0.63 = 0.212 = 21.2%  ← 5.9× improvement

★ HELIX cải thiện nhiều nhất → compound value tăng mạnh nhất
  (Vì HELIX là bottleneck, mỗi % improvement ở đây có hiệu ứng
   lớn hơn cùng % improvement ở BRIDGE hoặc FORGE)
```

---

## X. CEO DAILY/WEEKLY/MONTHLY PROTOCOL VỚI BỘ SKILL MỚI

### Daily (30 giây)

```
Sáng: "Hôm nay team đang ở phase nào? AI đang test trên data thật chưa?"
```

### Weekly (15 phút)

```
1. Review helix-design-journal entries tuần qua (5 min)
2. Check helix-integration-debt dashboard (3 min)
3. Identify: domain nào đang behind? Blocked bởi gì? (5 min)
4. One action: unblock or escalate (2 min)
```

### Monthly (60 phút = sync meeting)

```
1. helix-sync-protocol full execution (40 min)
2. helix-quality-gate check if approaching phase transition (10 min)
3. HELIX Score update (10 min)
```

### Quarterly (2 giờ)

```
1. Full HELIX Score reassessment
2. Review Compound Law: BRIDGE × FORGE × HELIX
3. Decide: nơi nào invest next quarter?
4. Skill improvement: nên thêm/sửa skill nào?
```

---

*Architecture designed for: Workshop X defense engineering, Triple Helix concurrent development (Mechanical × Electronics × AI/Software), Pahl-Beitz systematic methodology adapted for AI-integrated products, 25h/week CEO engineering capacity constraint.*

*Integrates with: BRIDGE (operations), FORGE (product strategy), existing CAD/documentation/review skills.*

*Next step: Implement Priority 1-3 skills (helix-project-init, helix-sync-protocol, helix-integration-debt) as actual SKILL.md files.*
