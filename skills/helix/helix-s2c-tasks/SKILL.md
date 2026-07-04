---
name: helix-s2c-tasks
description: "Block BC of Spec-to-CAD pipeline — decomposes the approved parametric plan into a dependency-ordered feature-tree task list using cad-tasks-template: [ID] [P?] [FR-ref] format, phases Setup → Foundational (serial) → Detail features ([P] parallelizable when no shared edge/face) → Late ops (fillets last) → Export & self-check. Triggers on: 's2c tasks', 'feature tree tasks', 'danh sách thao tác dựng hình', 'task list CAD', 'phân rã plan'."
---

# helix-s2c-tasks — Block BC: Feature-Tree Task List

> **Role:** Block BC của [[helix-spec-to-cad]] — phase SDD `tasks`.
> **Template:** `helix-spec-to-cad/references/cad-tasks-template.md`
> **In:** `{{prefix}}S2C_Plan.md` (APPROVED, Constitution Check PASS).
> **Out:** `{{prefix}}S2C_Tasks.md` — thứ tự dựng hình mà BD (implement) sẽ theo đúng.

## Workflow

### 1. Ledger Read
Đọc `_pipeline_state.md`. Xác nhận BB APPROVED (Constitution Check PASS). Chưa → STOP.

### 2. Decompose feature-tree → tasks (Offload)
Từ feature-tree outline của plan, sinh task list theo template, format `[ID] [P?] [FR-ref]`:

- **Phase S — Setup:** T001 khai parameter block (toàn bộ số từ Parameter Table).
- **Phase F — Foundational (SERIAL):** sketch profile trên datum → extrude base solid
  (+ assert bbox ≤ envelope). Mỗi op tiêu thụ solid của op trước — không song song.
- **Phase D — Detail features:** hole patterns, slots, pockets. Gắn `[P]` CHỈ khi hai
  feature không chung edge/face/vertex trên base đã đóng băng.
- **Phase L — Late ops:** fillets + chamfers — LUÔN sau toàn bộ Phase D (đổi thứ tự làm
  hỏng edge selection).
- **Phase E — Export & self-check:** export STEP + render PNG (iso + 3 ortho), mass-props
  report + sanity asserts (wall ≥ min DFM, no zero-volume).

Mỗi task ghi FR-ref/SC-ref; mỗi kích thước trace về param của Parameter Table.

### 3. Dependencies section
Ghi rõ: S → F → D → L → E; T-fillet phụ thuộc toàn bộ Phase D; `[P]` tasks độc lập.

### 4. Ledger Write + checkpoint (CEO Core — BLOCKING)
```
═══ BLOCK BC COMPLETE — {{prefix}}S2C_Tasks.md ═══
Tasks: {{n}} ({{n}} [P]) · Phases: S/F/D/L/E · 100% FR-traced
CEO: (1) ✅ Approve → BD implement  (2) 🔄 Sửa tasks  (3) ⏸️ Dừng
```

## Rules
- Fillet/chamfer luôn Phase L — sau mọi hole/pocket.
- `[P]` chỉ khi không chung edge/face — nghi ngờ thì bỏ `[P]` (serial an toàn hơn).
- Một part một run — multi-part = loop pipeline, không merge.
- Task không chứa số rời — chỉ tham chiếu param symbol.

## COD
- Phân rã plan → tasks: Offload (O)
- **Duyệt task list: Core (C)**
