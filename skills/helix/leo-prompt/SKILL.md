---
name: leo-prompt
description: "Generate a standardized, buildable text-to-CAD prompt (getleo.ai / Leo / Zoo / any text→CAD) from a part idea. Forces the 3 things text-to-CAD AIs need but users omit: an explicit parametric DIMENSIONS table, a build-order feature sequence, and a datum/orientation — defeating the same LLM spatial blindness that helix-cad-bridge guards. Classification-gated: THƯỜNG/personal → cloud Leo OK; MẬT/HẠN-CHẾ defense geometry → STOP and route to helix-cad-bridge (local, no cloud egress). Output = ready-to-paste CPTRF+CAD prompt with acceptance checks + FDM print constraints + variants. Triggers on: 'leo prompt', 'getleo', 'getleo.ai', 'text to cad prompt', 'text2cad', 'prompt cad', 'prompt getleo', 'tạo prompt cad', 'prompt in 3d', 'prompt chi tiết 3d', 'prompt thiết kế', 'làm prompt cad chuẩn', 'cad prompt builder'."
---

# leo-prompt — Text-to-CAD Prompt Generator (classification-aware)

> **Role:** Turn a rough part idea into a **buildable** text-to-CAD prompt for getleo.ai (or Leo/Zoo/any text→CAD). NOT a CAD generator itself — it writes the *prompt* that makes the cloud tool produce correct geometry on the first try.
> **Why:** A good design brief (CPTRF) still fails text-to-CAD because the AI is **spatially blind** ([[LLM Spatial Blindness]]): it needs explicit numbers, build order, and a datum — not adjectives like "gọn nhẹ". This skill forces those in.
> **Mirror:** for cloud-disqualified (MẬT) geometry, this skill refuses Leo and routes to [[helix-cad-bridge]] (local code-CAD).

## Step 0: Classification Gate (FIRST — non-negotiable)
Ask / infer the part's classification:
| Label | Rule |
|----|----|
| **THƯỜNG** (cá nhân, đồ tập, demo, R&D không nhạy cảm) | ✅ getleo.ai (cloud) OK — proceed. |
| **HẠN CHẾ / MẬT** (UUV, FCS, khí tài, chi tiết quốc phòng) | ⛔ STOP. Cloud text-to-CAD đẩy hình học lên server = vi phạm egress. → route to **[[helix-cad-bridge]]** (build123d local). Do NOT emit a Leo prompt. |

> Default for any defense product = MẬT → bridge. Only emit a Leo prompt when the user confirms THƯỜNG/personal.

## Step 1: Intake (gather — NEVER invent numbers)
Collect, asking for any missing critical value (spatial blindness = don't guess dimensions):
```
□ Chức năng (1 câu) + người dùng/bối cảnh
□ Gắn vào / giao diện: vật thể nó lắp vào + KÍCH THƯỚC giao diện thực tế (vd Ø tay cầm)
□ Kích thước chính CEO biết (dài/rộng/cao, Ø, góc, bề dày)
□ Vật liệu + công nghệ (FDM PETG/Nylon + TPU grip; in nhanh; support tối thiểu)
□ Ràng buộc bbox / khối lượng mục tiêu
□ Biến thể mong muốn (basic / padded / adjustable …)
```
If a critical dimension is unknown → ask, or mark `[CEO điền]` in the prompt (never fabricate).

## Step 2: Emit the Prompt (fixed structure — the value-add)
Produce a ready-to-paste prompt with these blocks. The **bold** blocks are what users omit and Leo needs most.

```
# C — CONTEXT
Mục đích: <…>. Người dùng/bối cảnh: <…>. Phân loại: THƯỜNG (cloud OK).
Gắn vào / giao diện: <vật thể + kích thước giao diện thực>.

# P — PERSONA
Bạn là kỹ sư thiết kế <lĩnh vực>, ưu tiên <ergonomics / printability / tương thích>. Style: liệt kê trước, diễn giải sau.

# T — TASK (1 thân chính, mô tả theo TRÌNH TỰ DỰNG)
Base feature: <khối/biên dạng gốc + số>. Op2: <extrude/cut/revolve + số>. Op3: <…>.
Bo/vát: <R… ở cạnh nào>. Pattern/đối xứng: <mặt phẳng, số lượng>.

# DIMENSIONS (tham số — Leo dùng trực tiếp)   ★ KHỐI QUAN TRỌNG NHẤT
| Tham số | Ký hiệu | Giá trị | Đơn vị | Ghi chú |
|---|---|---|---|---|
| … | L | … | mm | |
SPATIAL/DATUM: gốc = <…>; mặt đối xứng = <…>; +Z = <hướng in>.

# R — RULES / CONSTRAINTS
FDM, support tối thiểu, in nhanh. Thành ≥ <t> mm (≥3×nozzle). Bo cạnh tiếp xúc da R≥2.
Vật liệu thân <PETG/Nylon>; grip <TPU>. KHÔNG: overhang>45°, thành mỏng, chi tiết <0.8mm.

# ACCEPTANCE (đo được — Leo phải đạt)
Bounding box ≤ <LxWxH>. Khối lượng ≤ <g>. Không thành < <t>. Tự đứng khi in (đáy phẳng).

# F — FORMAT
Output markdown. Sections: Concepts, Dimensions, Print Setup, Assembly, Safety, Variants.
Bảng in: Nozzle|Layer|Infill|Support|Time|Material. Ngôn ngữ: vi. Biến thể: <basic/padded/adjustable>.
```

## Step 3: Quality self-check before handing over
- [ ] Mọi tham số trong DIMENSIONS có **số thật** (không có "gọn/nhẹ" thay cho mm); chỗ chưa biết = `[CEO điền]`.
- [ ] TASK mô tả **theo trình tự dựng** (base→op→fillet→pattern), không phải mô tả tĩnh.
- [ ] Có **DATUM** (gốc + mặt đối xứng + hướng in) — Leo mới đặt đúng.
- [ ] Có **ACCEPTANCE đo được** + **negative constraints (KHÔNG…)**.
- [ ] Có dòng **Phân loại** (chặn nhầm đồ MẬT lên cloud).

## What makes this "chuẩn hơn" than a plain CPTRF brief
| Plain brief | + leo-prompt |
|----|----|
| "gọn nhẹ, ôm tay cầm" | **DIMENSIONS table** số thật (D_grip, t, θ) |
| Mô tả tĩnh hình dáng | **Build-order** feature sequence |
| Không gốc tọa độ | **DATUM** (origin/đối xứng/hướng in) |
| "đẹp, an toàn" | **ACCEPTANCE** đo được + bbox/khối lượng |
| — | **Phân loại gate** (THƯỜNG→Leo / MẬT→helix-cad-bridge) |

## Output
- The ready-to-paste prompt (markdown) for getleo.ai.
- If MẬT: a one-line refusal + `→ /helix-cad-bridge` handoff (no prompt emitted).

## Integration
- **[[helix-cad-bridge]]** — the local fallback for MẬT geometry (this skill routes there instead of Leo).
- **[[helix-cad-ingest]]** — after Leo exports STEP/STL, ingest it back to lock a measured record if it enters a real project.
- **[[LLM Spatial Blindness]]** — the law this skill operationalizes for cloud text-to-CAD.

## COD
- Prompt drafting (structure, build-order, format): Offload (O)
- **Classification call (THƯỜNG vs MẬT): Core (C)** — defense egress control, non-delegable
- **Dimensions: Core (C)** — CEO supplies real numbers; AI never invents geometry ([[LLM Spatial Blindness]])
