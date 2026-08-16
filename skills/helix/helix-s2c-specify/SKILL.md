---
name: helix-s2c-specify
description: "Block BA of Spec-to-CAD pipeline — writes the part spec from CEO's description using cad-spec-template (FR-001… numeric-only requirements, envelope, datums, interfaces, material, mass budget, tolerances, DFM, SC-001… success criteria). Missing numbers become [NEEDS CLARIFICATION] markers (max 3, option tables with recommended default) — AI never invents a dimension. Includes the clarify loop: block only completes when CEO resolves all markers (zero-marker spec). Triggers on: 's2c specify', 'spec part', 'viết spec chi tiết', 'đặc tả part', 'part spec', 'clarify spec'."
---

# helix-s2c-specify — Block BA: Part Spec + Clarify Loop

> **Role:** Block BA của [[helix-spec-to-cad]] — gộp 2 phase SDD `specify` + `clarify`
> (clarify loop chính là CEO checkpoint của block này).
> **Template:** `helix-spec-to-cad/references/cad-spec-template.md`
> **In:** mô tả part của CEO + constitution (từ B0) + ICD/requirements nếu trong HELIX project.
> **Out:** `{{prefix}}S2C_Spec.md` — APPROVED chỉ khi **zero `[NEEDS CLARIFICATION]` marker**.

## Workflow

### 1. Ledger Read
Đọc `_pipeline_state.md` → Block Ledger: constitution đã duyệt (B0), classification label,
design_rules.json path, part_id/rev. Nếu B0 chưa APPROVED → STOP, yêu cầu chạy B0 trước.

### 2. Gather sources (Offload)
- Mô tả gốc của CEO (`$ARGUMENTS` / CEO context trong ledger)
- ICD + Requirements_List nếu part thuộc HELIX project (envelope, interfaces có sẵn)
- Constitution Điều V–VII (whitelist vật liệu, DFM, budget) — spec không được mâu thuẫn

### 3. Fill spec template (Offload)
Copy `cad-spec-template.md` → `{{prefix}}S2C_Spec.md`, điền đủ 11 section.

**Nguyên tắc thép (Điều IV — Spatial Blindness):**
- Mọi FR phải có **số + đơn vị + nguồn**. AI KHÔNG bao giờ bịa kích thước.
- Số thiếu → `[NEEDS CLARIFICATION: câu hỏi cụ thể]` — **TỐI ĐA 3 marker**.
  Nếu cần hơn 3: spec chưa đủ chín, STOP và đề nghị CEO cấp sketch/dimensions table trước.
- Mỗi marker = 1 **option table** (option A đề xuất + lý do, option B/C thay thế, ưu/nhược).
- Quan hệ không gian (coaxial/flush/offset/mirrored) phải trace về sketch callout hoặc giá trị CEO.

### 4. Clarify loop (CEO Core — BLOCKING)
```
═══ BLOCK BA — SPEC DRAFT: {{part_id}} ═══
FR: {{n}} yêu cầu ({{n}} có số đầy đủ) · SC: {{n}} tiêu chí
[NEEDS CLARIFICATION]: {{n}}/3

NC-1: {{câu hỏi}} → option table [A đề xuất / B / C]
...

CEO: chọn option cho từng NC (hoặc cấp giá trị khác)
```
CEO trả lời → ghi số vào FR, XÓA marker. Lặp đến khi **zero marker**.

### 5. Ledger Write + checkpoint
Append Block Ledger: key findings (FR count, material, mass budget, criticals), decisions cho BB
(param nào nhạy), open questions. Trình CEO duyệt spec cuối:
```
═══ BLOCK BA COMPLETE — {{prefix}}S2C_Spec.md ═══
Markers: 0/3 ✅ · FR: {{n}} (100% có số+đơn vị) · SC: {{n}}
CEO: (1) ✅ Approve → BB plan  (2) 🔄 Sửa spec  (3) ⏸️ Dừng
```

## Rules
- **AI never invents a dimension** — no number → marker, không đoán. Marker > 3 → STOP.
- Spec APPROVED = zero marker. Không mang marker sang BB.
- Spec không được mâu thuẫn constitution (vật liệu ngoài whitelist → NC hoặc amendment).
- Classification label READ-only.

## COD
- Điền template từ nguồn có sẵn: Offload (O)
- **Giải marker / cấp kích thước: Core (C)** — non-delegable
- **Duyệt spec cuối: Core (C)**
