---
name: leo-assist
description: "Phase-aware Leo AI (getleo.ai) prompt/template generator across the design lifecycle (P0 Pre-Study, P1 Requirements, P2 Concept, P3 Embodiment, P4 Detail) + QC + Installation. Built on deep research of Leo's REAL strengths — citation-backed calculations, 120M+ vendor/PLM part-search, DFMA reasoning, documentation — NOT production CAD geometry (Leo only outputs mesh; it pivoted to part-search). Routes each task to a phase template that plays to those strengths, forces quantified load case + real interface dims + source-citation + search-before-generate, and gates on classification: THƯỜNG/COTS/generic-knowledge → Leo cloud OK; MẬT/HẠN-CHẾ geometry/PLM → STOP (never upload), route to helix-cad-bridge (local). Geometry-generation subtasks → delegate to leo-prompt. Triggers on: 'leo assist', 'leo skill', 'leo cho thiết kế', 'prompt leo theo phase', 'leo P1 P2 P3 P4', 'leo QC', 'leo lắp đặt', 'getleo theo giai đoạn', 'leo tìm part', 'leo tính toán', 'leo tiêu chuẩn', 'bộ prompt leo'."
---

# leo-assist — Phase-Aware Leo AI Prompt Suite (research-grounded)

> **Role:** Sinh prompt/template cho **getleo.ai** đúng **thế mạnh đã kiểm chứng** của Leo, theo từng giai đoạn thiết kế (P0–P4) + QC + Lắp đặt. NOT a CAD generator; it writes the *prompt* that makes Leo deliver value where it actually can.
> **Nền tảng:** research getleo.ai (`3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_getleo-ai_2026-06-26.md`). Leo = **Large Mechanical Model**: mạnh ở *tính toán có cite · tìm part 120M vendor+PLM · DFMA · tài liệu*; **KHÔNG sinh CAD tham số production** (chỉ mesh — đã pivot sang part-search).
> **Mirror:** geometry production cho MẬT → [[helix-cad-bridge]] (local). Geometry concept prompt → [[leo-prompt]].

## Leo dùng ĐÚNG việc (research-verified) — bộ lọc thế mạnh
| ✅ Giao Leo (mạnh) | ❌ KHÔNG giao Leo (yếu/cấm) |
|----|----|
| Tính toán kỹ thuật **có trích nguồn** (sức bền, vật liệu, công thức) | Sinh CAD tham số production (Leo chỉ ra **mesh** — vô dụng gia công) |
| **Tìm part tiêu chuẩn/COTS** (120M vendor + PLM): bạc đạn, ray HGH, fastener | Quyết định dung sai/GD&T tới hạn (= CEO + CAD) |
| Tra **tiêu chuẩn** (ISO/ASME/MIL/datasheet) có cite | Thẩm định **hình học** bản vẽ (chỉ thẩm định *quy phạm*) |
| DFMA trade-off, chọn vật liệu, gợi ý part thay thế | Bất kỳ hình học/PLM/context **MẬT** lên cloud |
| Sinh concept (mesh) + tài liệu/spec/BOM-text (THƯỜNG) | "Vẽ" máy production từ text |

## Step 0: Classification Gate (FIRST — non-negotiable)
| Label | Quy tắc dùng Leo |
|----|----|
| **THƯỜNG** (đồ cá nhân, jig/gá nội bộ, R&D không nhạy cảm) | ✅ Full — concept + calc + search + docs. |
| **MẬT / HẠN-CHẾ** (UUV, FCS, khí tài) | ⚠️ **Chỉ kiến thức generic/COTS:** tra công thức/tiêu chuẩn công khai, tìm part chuẩn (bạc đạn, ray) bằng mô tả **không kèm context khí tài**. **TUYỆT ĐỐI KHÔNG upload bản vẽ/PLM/hình học MẬT.** Hình học production → [[helix-cad-bridge]] local. |

> Nguyên tắc vàng cho MẬT: prompt Leo phải **trừu tượng hóa** — hỏi "bạc lót trục Ø40h7 chịu X N, vật liệu?" KHÔNG hỏi "bạc cho UUV GIÁ TRƯỢT".

## Step 1: Route theo Phase + loại nhiệm vụ
Đọc phase (P0–P4/QC/Install) + loại việc → chọn template trong [references/leo-phase-templates.md](references/leo-phase-templates.md). Nếu việc là **sinh hình học** → chuyển [[leo-prompt]] (và nhắc Leo chỉ ra mesh concept).

| Phase | Leo hỗ trợ (đúng thế mạnh) | Skill nội bộ tiêu thụ kết quả |
|----|----|----|
| **P0** Pre-Study | tra tiêu chuẩn/sản phẩm tương đương, khả thi sơ bộ + COTS, ước cost generic | forge-pre-study · odi · forge-cost |
| **P1** Requirements | liệt kê tiêu chuẩn áp dụng + **giá trị mục tiêu** có cite, tra interface COTS, điều kiện môi trường | helix-p1-requirements · helix-p1-validate |
| **P2** Concept | tìm **nguyên lý/part** hiện thực, chọn vật liệu, DFMA trade-off, concept mesh (THƯỜNG) | helix-concept-generate |
| **P3** Embodiment ⭐ | **part-search COTS** (bạc đạn/ray/fastener), **tính sức bền/sizing** có cite, vật liệu, DFMA review, BOM standard-part | helix-p3-layout/-dfx/-bom |
| **P4** Detail | **kiểm quy phạm** (GD&T/ASME/ISO), tra dung sai/ren/fit, verify vendor-part BOM | helix-p4-drawing/-inspection |
| **QC** | tiêu chí nghiệm thu + phương pháp kiểm (VT/PT/UT/NDT) theo tiêu chuẩn, tính đo | helix-p4-inspection · erp-quality |
| **Lắp đặt** | trình tự lắp, **mô-men siết/preload** có cite, fit/căn chỉnh, checklist ATLĐ | forge-fabrication · helix-p4-handoff |

## Step 2: Emit prompt (cấu trúc bắt buộc — 5 nguyên tắc Leo)
Mọi prompt Leo phải có (đây là điểm Leo > ChatGPT, **phải ép dùng**):
1. **Load case định lượng** (lực/khối lượng, hướng, tĩnh/động) + **FoS mục tiêu**.
2. **Kích thước interface/mating thật** (Ø, ren, chốt) — không để "tiêu chuẩn" mơ hồ.
3. **Process chế tạo + thông số** (FDM/tiện/laser…) khi liên quan hình học.
4. **Bắt buộc trích nguồn** mọi số liệu kỹ thuật & nhân trắc.
5. **Search-before-generate:** bảo Leo tìm part tiêu chuẩn TRƯỚC; chỉ thiết kế mới khi không có.
+ Dòng **Phân loại** + danh sách **GIẢ ĐỊNH** cuối prompt để CEO kiểm.

## Step 3: Handoff
Output = prompt Leo dán thẳng + nêu **skill nội bộ tiêu thụ** kết quả Leo (vd part Leo tìm → forge-fabrication "mua ngoài"; calc Leo → helix-p3-dfx verify). **Số liệu Leo trả về luôn CEO/CAD verify** trước khi vào bản vẽ/BOM MẬT.

## Vòng kết hợp (Leo ⨉ bộ skill nội bộ)
```
Leo (THƯỜNG/generic): tìm part chuẩn · tính có cite · tra tiêu chuẩn · concept/docs
        ↓ (CEO verify số liệu)
Bộ skill nội bộ (MẬT, local): helix-cad-bridge (dựng hình) · helix-cad-ingest (đọc bản vẽ)
        · helix-cad-nest (cắt phôi) · helix-cad-to-fab (quy trình) · forge-fabrication (sản xuất)
leo-prompt = sinh prompt hình học (mesh concept) · leo-assist = sinh prompt theo phase
```

## Gotchas
- **Mesh ≠ production:** kết quả hình học Leo chỉ để ideation/visual. Đừng đưa mesh vào gia công — dựng lại tham số bằng helix-cad-bridge.
- **Part Leo tìm = đã validated** (có revision/drawing) — đây mới là giá trị thật (60-80% part vẽ mới là trùng lặp). Ưu tiên dùng.
- **MẬT abstraction:** trừu tượng hóa mọi prompt MẬT; không bao giờ tên khí tài/upload PLM.
- **Cite-check:** Leo trích nguồn nhưng vẫn phải mở nguồn xác minh cho quyết định chịu lực/an toàn.

## COD
- Sinh prompt theo phase (cấu trúc, template): Offload (O)
- **Classification + abstraction MẬT: Core (C)** — defense egress control
- **Load case / interface dims: Core (C)** — CEO cấp số thật ([[LLM Spatial Blindness]])
- **Verify số liệu Leo trước khi vào bản vẽ/BOM: Core (C)** — Leo "gần đúng", người chốt
