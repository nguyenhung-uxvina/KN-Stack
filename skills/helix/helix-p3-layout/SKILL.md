---
name: helix-p3-layout
description: "Block A of Phase 3 pipeline — CEO creates preliminary layout (Core, non-delegable), maritime auto-invoke P50 stability + P51 weight estimate, main function carrier development. P&B 7.1 Steps 2-6. Can run standalone. Triggers on: 'preliminary layout', 'create layout', 'P50 stability', 'P51 weight', 'main function carriers'."
---

# Block A: Layout — Preliminary Design (CEO Core + Maritime Checks)

> **P&B:** 7.1 (Steps 2-6) | **Pipeline:** helix-embody-realize → Block BA
> **Input:** `B0_Preflight_Report.md` + Phase 2 concept | **Output:** `BA_Preliminary_Layout.md` + maritime files

## Operational Envelope
> Source: [[Operational Envelope Law]] + [[LLM Spatial Blindness]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Document CEO's layout decisions | Generate spatial arrangement or layout |
| Check dimensional constraints vs requirements | Suggest component placement |
| Run maritime P50 stability + P51 weight | Override CEO's spatial judgment |
| Flag conflicts between layout and requirements | Skip CEO layout — go straight to DfX |
| Validate material compatibility | Assume LLM can "see" 3D relationships |

**Multi-Agent Mode:** NO — CEO Core. LLM fundamentally lacks 3D spatial cognition (100% geometry failure in research). AI documents and validates constraints, NEVER generates layout.
**CEO Checkpoint:** CEO IS the block. AI assists with constraint checking only.
**LLM Spatial Blindness Gate:** Any AI output containing spatial terms = LOW CONFIDENCE, must be verified on physical sketch/CAD.
- **Trigger words:** above, below, left, right, adjacent, next to, perpendicular, parallel, behind, opposite, between, centered, aligned, offset, flush, coaxial, concentric
- LLMs systematically misinterpret descriptive spatial terms (Cambridge: 100% geometry failure on right-angle precision)
- If AI generates text with ≥2 trigger words in same paragraph → auto-flag `[SPATIAL — CEO VERIFY]`

## Workflow

### Step A1: CEO Creates Preliminary Layout (Core — NON-DELEGABLE)

> **Rule:** AI NEVER generates the initial layout. This is design judgment. See [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]].

CEO provides:
- Hand sketches or CAD rough layout
- Key dimensional decisions (envelope, mounting points)
- Material candidates for primary structure
- Component placement rationale
- Assembly concept (how it goes together)

AI documents what CEO provides:
```
PRELIMINARY LAYOUT — {{project}}
Date: {{today}}
Source: CEO sketch/CAD [reference]

Main Function Carriers:
| MFC-ID | Function | Component(s) | Material | Key Dimensions |
|--------|----------|-------------|----------|----------------|

Layout Decisions:
| Decision | Rationale | Alternative Considered |
|----------|----------|----------------------|

SPATIAL ALLOCATION: [CEO INPUT ONLY — AI documents, does NOT generate]
[CEO describes arrangement of main function carriers in envelope]
[AI transcribes verbatim. Any spatial description here MUST come from CEO sketch/CAD, not AI inference.]
```

### Step A2: Develop Main Function Carriers (P&B 7.1 Steps 3-5)

> **Spatial Guard:** AI assists with material, dimensions, manufacturing — NOT spatial form. Any form description (shape, geometry, orientation) must reference CEO's sketch/CAD. AI outputs "per CEO sketch: ..." not "component should be..."

For each main function carrier:
- Preliminary form design (shapes, interfaces) — **reference CEO sketch**
- Key dimensions from requirements
- Material selection rationale
- Manufacturing method assumption

> **CAD generation:** To turn CEO's dimensioned sketch into parametric geometry, invoke `helix-cad-bridge` — AI writes code-CAD from CEO's **explicit numbers only** (not spatial inference), exports STEP + render for CEO verification. This is the sanctioned escape from the Spatial Blindness gate: code with explicit params, never AI-invented arrangement. Output STEP feeds Block BB (DfX) + Phase 4.
>
> **Per-part Geometry Source Gate (B vs D):** Decide the geometry path per part. For organic/complex parts the AI cannot parametrize (castings, hulls, ergonomic shells), do NOT force code-CAD — route via [[helix-cad-roundtrip]] --design-import (Flow D): AI writes a Design Brief from the layout envelope + interfaces, a human designer draws it externally, [[helix-cad-ingest]] imports + reconciles it. Either way the part's STEP or cad_extract.json registers as its **geometry-of-record** in ICD v3 ([[helix-p3-integrate]] Step C3a).

### Step A3: Auxiliary Function Solutions (P&B 7.1 Step 7)

> **Spatial Guard:** Cable routing, thermal paths, and component retention are inherently spatial. AI lists options and constraints — CEO decides routing and placement. AI outputs "Options: X, Y, Z — CEO selects and sketches routing."

Identify and solve auxiliary functions:
- Sealing, cooling, retention, support, cable routing — **CEO sketches spatial paths**
- Fastener standardization
- Adjustment mechanisms

### Step A4: Maritime Auto-Invoke (if --maritime or product is vessel/USV/buoy)

**P51 Weight Estimate:**
```
WEIGHT ESTIMATE — {{project}}
| Subsystem | Item | Material | Qty | Unit Wt | Total | Confidence |
|-----------|------|----------|-----|---------|-------|-----------|
| Structure | | | | | | [L1-L5] |
| Propulsion | | | | | | |
| Electrical | | | | | | |
| Payload | | | | | | |
| Outfit | | | | | | |
| SUBTOTAL | | | | | | |
| Margin (10-15%) | | | | | | |
| TOTAL | | | | | | |
```

**P50 Stability Check:**
```
STABILITY CHECK — {{project}}
| Condition | Displacement | GM | Trim | Freeboard | Status |
|-----------|-------------|----|----|-----------|--------|
| Lightship | | | | | |
| Half-load | | | | | |
| Full-load | | | | | |
| Worst-case | | | | | |

GM minimum: ≥ 0.5m ALL conditions
Trim freeboard minimum: ≥ 0.3m
```

**Gate:** GM < 0.5m → STOP [STABILITY-FAIL]. Weight > SWL → [OVERWEIGHT-RISK].

## Khi có CC2_Handoff.md

Nếu `Phase3-Embodiment/` hoặc `Phase3-Embody/` (hoặc thư mục biến thể bên dưới) có `{{prefix}}CC2_Handoff.md` từ `/helix-cc2`:
- Layout lấy khoảng tham số hình thể từ mục `## Tham số hình thể và khoảng chọn` của Handoff; tham số nhạy và phiếu giả thuyết đang mở ghi kèm trong `BA_Preliminary_Layout.md`.
- Muốn đổi một khoảng thì mở hoặc sửa phiếu giả thuyết tương ứng (qua `/helix-cc2`), không tự chọn lại khoảng trong layout.
- Handoff là đối chiếu mức mô tả. Khi đã có hình học (`cad_extract.json` từ `helix-cad-bridge` hoặc `helix-cad-ingest`), chạy vòng lặp P3 bằng `--crosscheck` của CA (không dùng `/helix-cc2 --analyze`): dựng một `<thư mục trích>` mới gồm bản trích C0, bản trích C2 + C3 của phương án đi tiếp `<X-n>` và `cad_extract.json`, rồi trong tác tử con mới chạy `/helix-cc2-analyze --crosscheck <thư mục trích> <X-n> <n>` (`<n>` = số GT lớn nhất ở mục Phiếu giả thuyết đang mở của Handoff cộng 1). Kết quả nằm trong `<thư mục trích>`; CEO quyết từng chỗ lệch.

## Khi có BF_Form_Selection.md (block BF)

Nếu có `{{prefix}}BF_Form_Selection.md` (từ `/helix-p3-form`, đã qua Cổng CEO 2):
- Đây là **nguồn khoảng tham số** hình thể của layout: mỗi `## F-<id>` có hình thể đã chọn, `Khoảng tham số:` và `Kế hoạch thử:`. Layout phải nằm trong các khoảng này và ghi lại trong `BA_Preliminary_Layout.md`.
- Muốn đổi một khoảng → quay lại BF (`/helix-p3-form --function <F-id>`), không tự chọn lại khoảng trong layout.
- Mục «Khi có CC2_Handoff.md» ở trên giữ nguyên hiệu lực (BF sinh `CC2_Handoff.md` nếu chưa có thì Handoff đó cũng áp dụng).
- Không có `BF_Form_Selection.md` mà orchestrator không ghi `--skip-form` → nhắc CEO chạy BF trước.
- Trước khi dùng, chạy lint chính thức `python -X utf8 D:/KN-Stack/scripts/p3_form_lint.py <thư mục P3 hoặc biến thể> --prefix {{prefix}} [--quick]` (không `--draft`; thêm `--quick` khi orchestrator chạy với `--quick`, như lint cuối của BF): exit ≠ 0 (còn `Chọn: (chờ CEO)`, thiếu `Lý do CEO:`/dòng `Cổng CEO 2 — ngày …`) → BA từ chối Selection, dừng và trả về BF.

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BA_Preliminary_Layout.md`
- `BA_Weight_Estimate.md` (maritime only)
- `BA_Stability_Check.md` (maritime only)

## CEO Checkpoint
```
═══ BLOCK BA LAYOUT COMPLETE ═══
Main function carriers: {{N}} defined
Auxiliary functions: {{N}} solved
Maritime: [P50/P51 PASS / N/A]
Key layout decisions: {{N}} documented

CEO:
(1) ✅ Approve layout → tiếp tục Block BB (DfX Review)
(2) 🔄 Revise layout
(3) ⏸️ Dừng — need CAD iteration
```

## COD
- **Layout creation: Core (C)** — non-delegable, CEO judgment
- Layout documentation: Offload (O1) — AI records
- Geometry Source Gate (B parametric vs D design-import) per part: **Core (C)** — CEO judges parametrizability
- Design Brief for Flow D parts ([[helix-cad-roundtrip]] --design-import): Offload (O2) — human designer draws, [[helix-cad-ingest]] reconciles
- P50/P51 calculations: Offload (O2) — AI computes
- **Layout approval: Core (C)**
