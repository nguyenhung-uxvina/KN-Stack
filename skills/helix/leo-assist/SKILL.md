---
name: leo-assist
description: "Phase × Mode Leo AI (getleo.ai) prompt suite. Two axes: 7 lifecycle PHASES (P0 Pre-Study · P1 Requirements · P2 Concept · P3 Embodiment · P4 Detail · QC · Installation) crossed with 6 strength-based MODES (A Part-Search & Reuse · B Engineering Q&A · C Calculation/Sizing · D DFM/Standards-Inspect · E Documentation/BOM · F Material-Selection). Built on deep research of Leo's REAL strengths — citation-backed calc, 120M+ vendor/PLM part-search, DFM inspect, docs, material — NOT production CAD geometry (Leo only outputs mesh; pivoted to part-search; 60-80% 'new' parts are duplicates). Each task → the right mode template (references/leo-mode-templates.md) or phase template, forcing quantified load + real interface dims + mandatory source-citation + search-before-generate, with a router meta-prompt. Classification-gated: THƯỜNG/COTS/generic → Leo cloud OK; MẬT/HẠN-CHẾ geometry/PLM → STOP+abstract, production geometry → helix-cad-bridge (local). Geometry-concept subtasks → leo-prompt (lowest-priority concept-only mode). Triggers on: 'leo assist', 'leo skill', 'leo cho thiết kế', 'prompt leo theo phase', 'leo mode', 'leo part search', 'leo P1 P2 P3 P4', 'leo QC', 'leo lắp đặt', 'leo tìm part', 'leo tính toán', 'leo tiêu chuẩn', 'leo DFM inspect', 'leo chọn vật liệu', 'bộ prompt leo', 'leo router'."
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

## 6 MODE theo thế mạnh (A–F) — trục "LOẠI việc"
> Đây là **lõi** — Leo mạnh ở 6 loại tác vụ. Template điền-sẵn: [references/leo-mode-templates.md](references/leo-mode-templates.md).

| Mode | Tác vụ | Dùng khi |
|----|----|----|
| **A** Part Search & Reuse ⭐ | tìm part COTS/PDM trước khi vẽ (60–80% part mới là trùng lặp) | cần 1 chi tiết |
| **B** Engineering Q&A | tra tiêu chuẩn/fit/quy tắc, có cite | hỏi kỹ thuật |
| **C** Calculation / Sizing | tính hiện công thức+logic+nguồn | thay bảng tính |
| **D** DFM / Standards Inspect | soi vi phạm DFM/quy phạm, mỗi flag có cite | review thiết kế (THƯỜNG) |
| **E** Documentation / BOM | E1 9-point summary · E2 datasheet/BOM-text · E3 gắp mfg-data có sẵn | đặc tả thiết kế + tài liệu nhanh (KHÔNG: quy trình CN/QMS/nghiệm thu → forge-fabrication/helix-p4-inspection/erp-quality) |
| **F** Material Selection | so vật liệu có cite + trade-off | chọn vật liệu |

## Giao diện Leo hiện hành (xác nhận 2026-07-05, screenshot CEO)
> app.getleo.ai giờ là **MỘT khung chat thống nhất** ("Hi, I'm Leo, your engineering copilot") với **4 nhóm intent gợi ý: Calculate · Develop · Part search · Learn** — KHÔNG còn tab/pillar riêng (Ideation không còn trên màn hình vào; 9-point summary vẫn gọi được qua chat). Dán prompt nào cũng vào cùng một ô — dòng `[MODE]` đầu template chính là tín hiệu route cho Leo.

| Nhóm UI Leo | Mode leo-assist tương ứng | Ghi chú |
|----|----|----|
| **Calculate** | **C** (calc/sizing) · **F** (so vật liệu định lượng) | ✨ Calculate giờ **vẽ được plot** ("Calculate and plot…") — Mode C có thể yêu cầu đồ thị (phân bố ứng suất, Mach…) |
| **Develop** | **D** (DFM/standards inspect) · B dạng how-to/best-practice | Ví dụ chính hãng của Develop là câu hỏi DFM FDM — khớp 1-1 Mode D |
| **Part search** | **A** · **E3** (gắp mfg-data) | Thế mạnh số 1, không đổi |
| **Learn** | **B** (lý thuyết/tiêu chuẩn) | Q&A có cite |
| *(qua chat, không có tile)* | **E1/E2** (9-point summary, datasheet) · concept mesh ([[leo-prompt]]) | Tutorial "Generate a Product Summary" vẫn tồn tại |

**2 kênh mới chưa khai thác (THƯỜNG only):**
- **Leo in CAD (desktop app .exe)** — "Leo in CAD (Installed Version)" chạy cạnh CAD; tiện cho part-search trong lúc vẽ. ⛔ MẬT: KHÔNG cài trên máy chứa bản vẽ khí tài (app index thư mục/PLM).
- **Build Complete Assemblies** (homepage flagship mới) + **CAD-to-CAD search** (upload STEP tìm part tương đồng) + sketch-upload — chỉ dùng cho hình học THƯỜNG; classification gate như cũ, upload hình học MẬT vẫn TUYỆT ĐỐI cấm.

## Step 1: Route theo Phase × Mode
Phase = *khi nào* · Mode = *loại việc*. Chọn phase → các mode trội → điền template mode (mode-templates) hoặc template phase ([references/leo-phase-templates.md](references/leo-phase-templates.md)). **Sinh hình học** → [[leo-prompt]] (mesh concept, mode "concept-only" ưu tiên thấp nhất).

| Phase | Mode trội | Skill nội bộ tiêu thụ |
|----|----|----|
| **P0** Pre-Study | B (tiêu chuẩn/tương đương) · A (COTS) | forge-pre-study · odi · forge-cost |
| **P1** Requirements | B (tiêu chuẩn) · C (giá trị mục tiêu) · A (interface COTS) | helix-p1-requirements · helix-p1-validate |
| **P2** Concept | A (part nguyên lý) · F (vật liệu) · B | helix-concept-generate (+leo-prompt concept) |
| **P3** Embodiment ⭐ | **A (part-search COTS)** · C (sizing) · F · D | helix-p3-layout/-dfx/-bom |
| **P4** Detail | D (GD&T/ISO inspect) · B (fit) · E (BOM verify) | helix-p4-drawing/-inspection |
| **QC** | B (tiêu chí nghiệm thu) · D (inspect) · C (đo) | helix-p4-inspection · erp-quality |
| **Lắp đặt** | B (mô-men/tiêu chuẩn) · C (preload) · E (quy trình) | forge-fabrication · helix-p4-handoff |

> **Router nhanh:** dán "Router meta-prompt" (cuối mode-templates) + 1 dòng tác vụ → tự chọn mode + điền template.

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

## Programmatic path — [[leo-bridge]] (MCP)
Vòng thủ công ở trên nay có bản khép kín qua MCP server local `mcp/leo-bridge` (6 tools: classify → prompt_build → send → ingest → route → ledger; gate MẬT hard-block 2 lần; propose-only). Dùng [[leo-bridge]] khi muốn ledger + verify checklist + route tự động; leo-assist vẫn là source of truth cho template + doctrine.

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
