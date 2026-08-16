---
name: helix-s2c-plan
description: "Block BB of Spec-to-CAD pipeline — turns the approved zero-marker spec into a parametric plan using cad-plan-template: parameter table (name/symbol/value/unit/driven-by-FR, zero magic numbers), backend pick (build123d), feature-tree outline, and the Constitution Check GATE (all 8 articles must PASS; accepted violations go to Complexity Tracking with CEO justification). Triggers on: 's2c plan', 'parametric plan', 'kế hoạch tham số', 'constitution check', 'lập plan CAD'."
---

# helix-s2c-plan — Block BB: Parametric Plan + Constitution Check Gate

> **Role:** Block BB của [[helix-spec-to-cad]] — phase SDD `plan`.
> **Template:** `helix-spec-to-cad/references/cad-plan-template.md`
> **In:** `{{prefix}}S2C_Spec.md` (APPROVED, zero marker) + constitution.
> **Out:** `{{prefix}}S2C_Plan.md` — APPROVED chỉ khi **Constitution Check toàn PASS**
> (hoặc violation có justification được CEO chấp nhận trong Complexity Tracking).

## Workflow

### 1. Ledger Read
Đọc `_pipeline_state.md`. Xác nhận BA APPROVED (spec zero marker). Chưa → STOP.

### 2. Parameter table (Offload)
Từ spec, lập bảng tham số: mỗi kích thước = 1 param có symbol (`base_l`, `t`, `hole_d`…),
value, unit, **driven-by FR-ref**. Zero magic number — số nào không trace được về FR/spec
→ quay lại BA, KHÔNG tự chế.

### 3. Backend + feature-tree outline (Offload)
- Backend: **build123d** mặc định (theo [[helix-cad-bridge]]); OpenSCAD cho CSG đơn giản.
- Feature-tree: sketch → extrude → holes/pockets → fillets/chamfers (LUÔN CUỐI) → export.
- Risks: liệt kê quan hệ không gian cần CEO sketch callout (mục 6 template).

### 4. Constitution Check GATE (bảng 8 điều)
Chấm từng điều I–VIII: PASS / VIOLATION. VIOLATION → ghi vào **Complexity Tracking**
với justification; CEO chấp nhận hoặc gate ĐÓNG (sửa spec/plan rồi chấm lại).
Không được xóa/bỏ qua điều nào để gate xanh.

### 5. Ledger Write + checkpoint (CEO Core — BLOCKING)
```
═══ BLOCK BB COMPLETE — {{prefix}}S2C_Plan.md ═══
Params: {{n}} (100% driven-by-FR) · Backend: build123d
Constitution Check: {{8-n}}/8 PASS · Violations accepted: {{n}} (Complexity Tracking)
CEO: (1) ✅ Approve → BC tasks  (2) 🔄 Sửa plan  (3) ⏸️ Dừng
```

## Rules
- **Constitution Check PASS là điều kiện tiên quyết** — gate đóng thì không sang BC.
- Zero magic number — mọi param driven-by-FR.
- Fillet/chamfer luôn cuối feature-tree (edge selection ổn định).
- Plan không đổi số của spec — cần đổi → re-run BA.

## COD
- Lập param table + feature-tree: Offload (O)
- **Chấp nhận violation (Complexity Tracking): Core (C)**
- **Duyệt plan: Core (C)**
