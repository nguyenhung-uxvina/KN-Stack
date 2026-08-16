---
name: helix-s2c-implement
description: "Block BD of Spec-to-CAD pipeline — DELEGATES geometry generation to helix-cad-bridge: pre-fills the bridge's Parametric Intent (Step 2) from the approved spec/plan/tasks (CEO confirms — stays Core), bridge writes the build123d script following the task order, executes 100% LOCAL, exports STEP + PNG + mass-props. The block never writes CAD code itself. Ends at the Spatial Blindness gate: CEO inspects the render PNG. Triggers on: 's2c implement', 'sinh CAD từ spec', 'generate part from spec', 'dựng hình theo tasks', 'implement CAD'."
---

# helix-s2c-implement — Block BD: Implement via helix-cad-bridge

> **Role:** Block BD của [[helix-spec-to-cad]] — phase SDD `implement`. **Thin delegator** —
> block này KHÔNG tự viết code-CAD; toàn bộ việc sinh hình giao cho [[helix-cad-bridge]].
> **In:** `{{prefix}}S2C_Spec.md` + `{{prefix}}S2C_Plan.md` + `{{prefix}}S2C_Tasks.md` (đều APPROVED).
> **Out:** `cad/{{part_id}}.py` + `.step` + `.png` + mass-props JSON (do bridge tạo).

## Workflow

### 1. Ledger Read
Đọc `_pipeline_state.md`. Xác nhận BC APPROVED. Đọc classification label — MẬT/HẠN-CHẾ
→ assert offline (egress guard của bridge).

### 2. Pre-fill Parametric Intent (Offload → CEO Core confirm)
Ưu thế của Spec-to-CAD: bridge Step 2 (Parametric Intent) không phải điền tay từ đầu —
block này **pre-fill từ artifacts đã duyệt**:
- DIMENSIONS table ← Parameter Table của Plan (đã 100% driven-by-FR)
- SPATIAL RELATIONS ← spec section 2–3 (datums, interfaces) + Risks của Plan
- MATERIAL/EXPORT ← spec section 5 + Technical Context của Plan

CEO xác nhận Intent (vẫn Core — bridge rule: AI không đề xuất giá trị hình học; ở đây mọi
giá trị đều là số CEO đã duyệt ở BA/BB, block chỉ CHUYỂN, không chế).

### 3. Delegate to helix-cad-bridge (Offload)
Gọi [[helix-cad-bridge]] với Intent đã confirm. Yêu cầu bridge:
- Viết script theo ĐÚNG thứ tự `{{prefix}}S2C_Tasks.md` (S→F→D→L→E; fillet cuối).
- Mỗi task = 1 đoạn code có comment `# T00x [FR-ref]` — truy vết task↔code.
- Chạy LOCAL → export `{{part_id}}.step` + `.png` (iso + 3 ortho) + mass-props JSON
  (`{"mass_kg": …, "bbox": …}`) vào `cad/`.
- Sanity asserts của Phase E (bbox ≤ envelope, wall ≥ min DFM) nằm TRONG script.

### 4. Spatial Blindness gate (CEO Core — BLOCKING)
Bridge Step 5 nguyên trạng: **AI không tự chứng nhận hình học — render là bằng chứng.**
```
═══ BLOCK BD COMPLETE — GEOMETRY VERIFY {{part_id}} ═══
PNG khớp intent?        [ ] yes [ ] no
BBox vs envelope:       {{LxWxH}} vs {{limit}} (SC-001)
Mass vs budget:         {{kg}} vs {{max}} (SC-002)
Tasks traced in code:   {{n}}/{{n}} có comment T-ref
CEO: (1) ✅ Approve render → BE validate  (2) 🔄 Sửa param → regenerate  (3) ⏸️ Dừng
```

### 5. Ledger Write
Append: script path, STEP/PNG path, mass-props, kết quả render check, param nào CEO chỉnh.

## Rules
- **⛔ Block NEVER writes CAD code itself** — luôn delegate helix-cad-bridge. #1 rule.
- Mọi giá trị trong Intent phải đã tồn tại trong spec/plan APPROVED — số mới xuất hiện
  ở bước này = vi phạm, quay lại BA.
- **AI never self-certifies geometry** — CEO kiểm PNG, không có ngoại lệ.
- Classification label READ-only; MẬT → bridge egress guard bắt buộc PASS.
- FAIL loop từ BE quay về block này: sửa param → regenerate → CEO kiểm render lại.

## COD
- Pre-fill Intent + delegate + thread handoff: Offload (O)
- **Confirm Parametric Intent: Core (C)** — bridge Step 2, non-delegable
- **Render verification: Core (C)** — Spatial Blindness gate, bridge Step 5
