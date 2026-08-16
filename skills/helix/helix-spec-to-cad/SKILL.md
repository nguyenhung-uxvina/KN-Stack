---
name: helix-spec-to-cad
description: "Spec-to-CAD orchestrator — Spec-Driven Development (SDD, borrowed from GitHub spec-kit methodology, NOT a fork) applied to AI-assisted mechanical CAD: constitution → specify → clarify → plan → tasks → implement → validate, commanding 6 block-skills (helix-s2c-preflight/specify/plan/tasks/implement/validate). Lightweight PART-level path — a disciplined front-end to Flow B of helix-cad-roundtrip: spec with [NEEDS CLARIFICATION] markers (max 3), Constitution Check gate, feature-tree tasks, then DELEGATES geometry to helix-cad-bridge (build123d → STEP+PNG, 100% local) and gating to helix-cad-validate (design_rules.json, deterministic, --approved-hash). Preserves Spatial Blindness gate + Geometry Source Gate (complex parts exit to Flow D human-CAD). Triggers on: 'spec to cad', 'spec-to-cad', 'spec-driven cad', 'sdd cad', 'thiết kế theo spec', 'từ spec ra STEP', 'đặc tả ra CAD', 'spec kit cad', 'thiết kế CAD có AI', 'part từ đặc tả'."
---

# helix-spec-to-cad — Spec-to-CAD Orchestrator (SDD × HELIX CAD chain)

> **Role:** Chỉ huy mỏng (thin commander) — KHÔNG phải block P1–P4. Điều phối 6 block-skills
> tuần tự theo phương pháp **Spec-Driven Development** (mượn methodology từ GitHub spec-kit,
> bản địa hóa cho CAD cơ khí — KHÔNG fork code spec-kit).
> **Vị trí:** con đường **PART-level nhẹ** — front-end kỷ luật cho **Flow B** của
> [[helix-cad-roundtrip]]. Pipeline P1–P4 vẫn là con đường PRODUCT-level; hai bên không
> xung đột: STEP output đăng ký vào **cùng slot ICD geometry-of-record**.
> **Backend:** [[helix-cad-bridge]] (build123d → STEP+PNG) + [[helix-cad-validate]]
> (design_rules.json sensor+gate) — 100% LOCAL, air-gapped, defense-safe.

## Tại sao SDD cho CAD?
spec-kit chứng minh: spec là source-of-truth khả thi hành, không phải giấy vứt đi. Áp cho CAD:
- **Constitution** = luật thiết kế bất khả thương lượng → compile thành `design_rules.json`
  (yardstick của validator) — spec-kit constitution gặp KHUNG HARNESS §5.2 Guides–Sensors–Gates.
- **`[NEEDS CLARIFICATION]` markers** = chống [[LLM Spatial Blindness]] có cấu trúc: AI không
  bịa kích thước, số thiếu thành câu hỏi option-table cho CEO (max 3).
- **Constitution Check gate** ở plan = chặn vi phạm TRƯỚC khi sinh hình, không phải sau.
- **Feature-tree tasks** `[ID] [P?] [FR-ref]` = thứ tự dựng hình truy vết được về requirement.

## Pipeline Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                helix-spec-to-cad (ORCHESTRATOR)                     │
│  Flags: --part <id> | --variant <name> | --from <block> | --only   │
│                                                                     │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐       │
│  │ B0   │─▶│ BA   │─▶│ BB   │─▶│ BC   │─▶│ BD   │─▶│ BE   │       │
│  │PRE-  │  │SPEC- │  │PLAN  │  │TASKS │  │IMPLE-│  │VALI- │       │
│  │FLIGHT│  │IFY   │  │      │  │      │  │MENT  │  │DATE  │       │
│  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘       │
│     │✓CEO     │✓CEO     │✓CEO     │✓CEO     │✓CEO     │✓CEO       │
│  constitution  spec+     param+    feature   bridge:   validate.py │
│  + geometry    clarify   Constit.  tree      STEP+PNG  gate 0/2    │
│  source gate   loop      Check     [P] ops   render ✓  ←─loop─┐    │
│     │                                          └───FAIL fix-hints──┘│
│     └─(D) EXIT → /helix-cad-roundtrip --design-import (human-CAD)  │
└────────────────────────────────────────────────────────────────────┘
SDD chain:  constitution → specify → clarify → plan → tasks → implement → validate
State:      {{output_path}}/_pipeline_state.md
```

## Sub-Skills (6 Block-Skills)

| Block | Skill | SDD phase | Purpose | CEO Checkpoint |
|-------|-------|-----------|---------|----------------|
| **B0** | `/helix-s2c-preflight` | constitution | Constitution + classification + **Geometry Source Gate** + compile `design_rules.json` | Duyệt constitution; kỹ sư duyệt rules + sha256 |
| **BA** | `/helix-s2c-specify` | specify + clarify | Part spec FR-001… toàn số; `[NEEDS CLARIFICATION]` max 3, option tables | **Giải markers** (Core) → zero-marker |
| **BB** | `/helix-s2c-plan` | plan | Parameter table + feature-tree + **Constitution Check gate** + Complexity Tracking | Duyệt plan; gate PASS bắt buộc |
| **BC** | `/helix-s2c-tasks` | tasks | Feature-tree ops `[ID] [P?] [FR-ref]`, fillet cuối | Duyệt task list |
| **BD** | `/helix-s2c-implement` | implement | **Delegate [[helix-cad-bridge]]** → `.py`+STEP+PNG+mass-props | **Render check** (Spatial Blindness gate) |
| **BE** | `/helix-s2c-validate` | validate | **Delegate [[helix-cad-validate]]** → exit 0/2, fix-hints loop về BD | Close pipeline; kỹ sư ký ngoài AI |

## How to Use

```
# Full pipeline — part trong HELIX project
/helix-spec-to-cad VN-XUONG-UUV --part mounting-bracket

# Standalone part (không có P1–P4)
/helix-spec-to-cad DEMO-BRACKET --part l-bracket

# Resume / single block
/helix-spec-to-cad VN-XUONG-UUV --part mounting-bracket --from BC
/helix-s2c-plan VN-XUONG-UUV --part mounting-bracket
```

## Orchestrator Workflow

### Step 1: Parse Arguments + Route
```
PROJECT: {{first argument}}    PART: --part <id> (bắt buộc — one part per run)
VARIANT: --variant <name> (optional)
FLAGS: --from X | --only X
```
- **Trong HELIX project:** output theo Data Bus P-phase hiện hành —
  `1_Projects/{{project}}/Phase{N}-…/{{variant}}/`, prefix `{{PROJECT}}_{{VARIANT_SHORT}}_`.
- **Standalone:** `1_Projects/{{project}}/SpecToCAD/{{part_id}}/`, prefix `{{PROJECT}}_`.

### Step 2: Initialize Pipeline State
Check/create `{{output_path}}/_pipeline_state.md` (B0 là Initializer sẽ populate):

```markdown
---
project: {{project}}
part: {{part_id}}
pipeline: helix-spec-to-cad v1.0
started: {{today}}
mode: [helix-project | standalone]
---
# Spec-to-CAD Pipeline State — {{project}} / {{part_id}}

## Block Progress
| Block | Skill | Status | Started | Completed | CEO Approved |
|-------|-------|--------|---------|-----------|--------------|
| B0 | helix-s2c-preflight | PENDING | - | - | - |
| BA | helix-s2c-specify   | PENDING | - | - | - |
| BB | helix-s2c-plan      | PENDING | - | - | - |
| BC | helix-s2c-tasks     | PENDING | - | - | - |
| BD | helix-s2c-implement | PENDING | - | - | - |
| BE | helix-s2c-validate  | PENDING | - | - | - |

## Block Ledger
> Sole communication channel between blocks. Ledger-Read trước, Ledger-Write sau mỗi block.

## CEO Decisions

## Adjustments Log
```

### Step 3: Execute Blocks Sequentially — ONE AT A TIME

**⛔ CRITICAL RULE: Execute EXACTLY ONE block per turn. Sau mỗi block, STOP and WAIT for CEO.
DO NOT proceed, DO NOT combine blocks, DO NOT auto-continue.**

Mỗi block: (1) **Ledger Read** `_pipeline_state.md` → reconstruct context; (2) Announce
"Đang chạy Block {{X}}"; (3) Execute block (delegate cho sub-skill); (4) **Ledger Write**
(key findings / decisions for downstream / open questions / CEO checkpoint result);
(5) Update Block Progress; (6) **STOP — CEO Checkpoint (BLOCKING)**:
```
═══ BLOCK {{X}} COMPLETE ═══
Deliverables: [files] · Key findings: [1-3 bullets]
CEO: (1) ✅ Approve → Block {{next}}  (2) 🔄 Chạy lại với điều chỉnh
     (3) ⏸️ Dừng pipeline  (4) ⏭️ Skip block kế (nếu hợp lệ)
```
(7) **⛔ WAIT for CEO message** — không sinh thêm nội dung đến khi CEO trả lời.

**FAIL loop (BE→BD):** validate exit 2 → orchestrator thread fix-hints về BD (một vòng =
một turn, vẫn STOP tại render check của BD rồi mới chạy lại BE).

### Step 4: Pipeline Completion
```
═══ SPEC-TO-CAD COMPLETE — {{project}} / {{part_id}} rev {{rev}} ═══
Spec: {{n}} FR (zero marker) · Plan: Constitution Check {{8}}/8 PASS
Tasks: {{n}} ops ({{n}} [P]) · Geometry: {{part}}.step + .py + .png
Validate: PASS (hash-OK) · SC scorecard: 4/4 ✅
ICD: geometry-of-record registered rev {{n}} (cùng slot Flow B roundtrip)
Còn NGOÀI AI: kỹ sư định danh ký sign-off trong validate report

Next: /helix-p3-integrate (ICD freeze) · /helix-p4-drawing (2D) · /forge-fabrication (F0)
```

## Data Bus — Shared File Contract (sacred)

| File | Written by | Read by |
|---|---|---|
| `_pipeline_state.md` | Orchestrator + blocks | All |
| `{{prefix}}S2C_Constitution.md` + `design_rules.json` | B0 | BB (gate), BE (sensor) |
| `{{prefix}}S2C_Spec.md` | BA | BB, BC, BD |
| `{{prefix}}S2C_Plan.md` | BB | BC, BD |
| `{{prefix}}S2C_Tasks.md` | BC | BD |
| `cad/{{part_id}}.py` + `.step` + `.png` + massprops JSON | BD (via helix-cad-bridge) | BE |
| `cad/validated/{{part_id}}.cad_validate_report.{json,md}` | BE (via helix-cad-validate) | ICD, forge-fabrication |

## Integration Map

```
helix-spec-to-cad (ORCHESTRATOR) COMMANDS:
  → /helix-s2c-preflight · /helix-s2c-specify · /helix-s2c-plan
  → /helix-s2c-tasks · /helix-s2c-implement · /helix-s2c-validate
BD DELEGATES TO: helix-cad-bridge (build123d → STEP + PNG + mass-props)
BE DELEGATES TO: helix-cad-validate (validate.py, design_rules.json, --approved-hash)
B0 EXITS TO:     helix-cad-roundtrip --design-import (Flow D, part phức tạp — người vẽ ngoài)

READS FROM:  ICD + Requirements_List (nếu trong HELIX project) · constitution templates
WRITES TO:   ICD geometry-of-record (cùng slot Flow B) · helix-p3-integrate · helix-p4-drawing
             · forge-fabrication F0
TEMPLATES:   references/cad-constitution-template.md · cad-spec-template.md
             · cad-plan-template.md · cad-tasks-template.md
EXAMPLE:     references/example-bracket/ (golden run: L-bracket 100×80×6 Al 6061)
```

## Rules

- **⛔ ONE BLOCK PER TURN — STOP AND WAIT** — không chạy 2+ block một lượt, không auto-continue. #1 rule.
- **Orchestrator NEVER does block work itself** — không viết spec, không viết code-CAD,
  không parse gì; luôn delegate sub-skills; BD/BE delegate tiếp bridge/validate.
- **Pipeline state file is source of truth** — Ledger-Read trước mọi action.
- **Data bus contract is sacred** — đúng filename trong bảng.
- **AI never invents a dimension** — số thiếu = `[NEEDS CLARIFICATION]` (max 3), không đoán.
- **AI never self-certifies geometry** — render PNG là bằng chứng, CEO kiểm (Spatial Blindness
  gate, Core, non-delegable).
- **Geometry Source Gate nghiêng về D khi không chắc** — part phức tạp EXIT sang roundtrip
  Flow D (người vẽ ngoài); Spec-to-CAD chỉ sở hữu part Flow-B-eligible.
- **Classification label is READ, not set** — từ helix-p1-validate; ngoại lệ duy nhất:
  standalone bootstrap ở B0 (Core). MẬT → egress guard, vi phạm = `[CLASSIFICATION-VIOLATION]` + STOP.
- **Contract read-only-với-agent** — design_rules.json chỉ kỹ sư sửa; BE luôn chạy
  `--approved-hash`; FAIL không được "sửa luật cho gate xanh".
- **PASS ≠ chữ ký** — validate PASS là chuẩn tối thiểu; kỹ sư định danh ký cổng cuối, không AI.
- **One part, one rev per run** — multi-part = loop pipeline, không merge.

## COD Classification

- Pipeline orchestration + handoff threading: Offload (O1)
- Block execution: Offload (O2) — mỗi block có COD riêng
- CEO checkpoints (mọi block): **Core (C)**
- Geometry Source Gate (B vs D): **Core (C)** — non-delegable
- Giải `[NEEDS CLARIFICATION]` / cấp kích thước: **Core (C)**
- Render verification (Spatial Blindness): **Core (C)**
- design_rules.json authoring + approved-hash custody: **Core (C)** — kỹ sư định danh
- Egress guard: Default (D) — automated assertion
