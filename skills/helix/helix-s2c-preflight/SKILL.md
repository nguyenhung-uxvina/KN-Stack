---
name: helix-s2c-preflight
description: "Block B0 (Initializer) of Spec-to-CAD pipeline — resolves/creates the CAD Constitution from cad-constitution-template, reads the geometry classification label (or CEO sets it ONCE here in standalone mode — the only place, flagged Core), runs the Geometry Source Gate (non-AI-parametrizable part → EXIT and route to /helix-cad-roundtrip --design-import Flow D), and compiles the constitution's Machine-Checkable Extract into the project's design_rules.json draft for engineer approval + sha256. Triggers on: 's2c preflight', 'cad constitution', 'hiến pháp CAD', 'khởi tạo spec-to-cad', 'geometry source gate'."
---

# helix-s2c-preflight — Block B0: Constitution + Gates (Initializer)

> **Role:** Block B0 của [[helix-spec-to-cad]] — phase SDD `constitution` + Initializer của
> pipeline (validate inputs, populate ledger).
> **Template:** `helix-spec-to-cad/references/cad-constitution-template.md`
> **Out:** `{{prefix}}S2C_Constitution.md` + `design_rules.json` (draft → kỹ sư duyệt + sha256)
> + `_pipeline_state.md` khởi tạo.

## Workflow

### 1. Resolve project context + classification
- **Trong HELIX project:** ĐỌC classification label từ `helix-p1-validate` sacred constraints
  (default **MẬT** nếu chưa đặt cho sản phẩm quốc phòng). Label là READ, không đặt lại.
- **Standalone part (không có P1):** CEO đặt label MỘT LẦN tại đây — **case duy nhất**
  pipeline này đặt label, flag **Core**. Ghi vào constitution, downstream chỉ đọc.

### 2. Geometry Source Gate (CEO Core — có thể EXIT)
Cùng gate với [[helix-cad-roundtrip]]:
```
═══ GEOMETRY SOURCE GATE — {{part_id}} ═══
Part này AI có dựng tham số được không?
(B) ✅ Tham số rõ, CEO cấp đủ số → TIẾP TỤC pipeline Spec-to-CAD (Flow B có kỷ luật)
(D) 🧑 Phức tạp/hữu cơ/cần phán đoán hình → EXIT → /helix-cad-roundtrip --design-import
```
**Mặc định an toàn: không chắc → chọn D.** Spec-to-CAD CHỈ sở hữu part Flow-B-eligible;
ép code-CAD lên hình phức tạp vi phạm [[LLM Spatial Blindness]]. Chọn D → pipeline dừng
tại đây, route sang roundtrip Flow D (AI ra Design Brief, người vẽ ngoài).

### 3. Resolve/create Constitution (Offload → CEO Core approve)
- Đã có `{{prefix}}S2C_Constitution.md` hoặc constitution project-level? → dùng, kiểm version.
- Chưa có → copy template, điền Điều V–VII với chuẩn Workshop X thực (vật liệu kho, DFM xưởng,
  budget từ spec/P51). CEO duyệt từng điều — đây là văn bản bất khả thương lượng.

### 4. Compile Machine-Checkable Extract → design_rules.json (Offload → Engineer Core)
- Copy JSON block trong constitution → `design_rules.json` cạnh artifacts.
- **Kỹ sư định danh** điền số thật (KHÔNG placeholder), duyệt, rồi tính sha256:
  `python -c "import hashlib;print(hashlib.sha256(open('design_rules.json','rb').read()).hexdigest())"`
- Hash lưu NGOÀI tầm ghi của agent (kỹ sư giữ) — BE dùng `--approved-hash` chống tự-sửa-rào.

### 5. Initialize `_pipeline_state.md` + checkpoint (CEO Core — BLOCKING)
Khởi tạo ledger theo format orchestrator (Block Progress 6 block + Block Ledger + CEO Decisions).
```
═══ BLOCK B0 COMPLETE — {{part_id}} ═══
Constitution: v{{x.y.z}} APPROVED · Classification: {{label}} ({{read|set-standalone}})
Geometry Source Gate: (B) Flow-B eligible ✅ · design_rules.json: engineer-approved, sha256 recorded
CEO: (1) ✅ Approve → BA specify  (2) 🔄 Sửa constitution  (3) ⏸️ Dừng
```

## Rules
- **Classification label is READ, not set** — ngoại lệ duy nhất: standalone bootstrap, Core.
- **Gate nghiêng về D khi không chắc** — Spec-to-CAD không nhận part ngoài envelope Flow B.
- Constitution + design_rules chỉ kỹ sư/CEO sửa; agent read-only; mọi sửa = version bump + re-hash.
- MẬT → assert offline ngay từ B0; vi phạm → `[CLASSIFICATION-VIOLATION]` + STOP.

## COD
- Copy template, compile Extract, khởi tạo ledger: Offload (O)
- **Classification (standalone) + Geometry Source Gate: Core (C)** — non-delegable
- **Duyệt constitution + design_rules + hash custody: Core (C)** — CEO/kỹ sư định danh
- Egress guard assertion: Default (D)
