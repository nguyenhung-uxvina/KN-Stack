# Assay — AI Design-Review Gate: kiến trúc tham chiếu 5 bước

> Bản đồ doctrine cho hệ kiểm tra thiết kế cơ khí **air-gapped** của xưởng CNQP. "Assay" là tên
> thương mại (CEO chốt 2026-07-05) cho lớp **đảm bảo kỹ thuật (assurance)** — tách khỏi họ kill-chain.
> Luận điểm lõi: **AI làm Sensor tất định (soi-và-chặn), KHÔNG làm Generator/Actor (vẽ khí tài).**
> Neo doctrine: [[mentor-harness-engineering-council]] · [[Sensor-Not-Generator Law]].
>
> Tài liệu này mô tả kiến trúc MỤC TIÊU và ánh xạ nó vào cặp skill hiện có. Nó KHÔNG kèm cấu hình
> triển khai hạ tầng server (Docker/vLLM/Qwen/`.helix/rules.yaml`) — phần đó HOÃN tới khi có trigger
> triển khai LAN biệt lập thật (xem bảng "Hoãn" cuối trang).

## Sơ đồ 5 bước

```
  ĐẦU VÀO: bản vẽ 2D (PDF+DXF) + mô hình 3D (STEP / CAD-as-code)
                          │
                          v
  ┌──────────────────────────────────────────────────────────┐
  │ BƯỚC 1 — TRÍCH XUẤT HÌNH HỌC TẤT ĐỊNH  [Computational]   │
  │ B-Rep AAG (OpenCASCADE) · mesh metrics · tool-collision   │
  │ + DFM lỗ tất định (nay: min_hole_dia, spacing, depth:dia) │
  └──────────────────────────────────────────────────────────┘
              │                          │
              v                          v
  ┌───────────────────────┐  ┌───────────────────────────────┐
  │ BƯỚC 2 — KAN DFM      │  │ BƯỚC 3 — VLM 2D-3D ALIGNMENT   │
  │ [Inferential/propose] │  │ [Inferential/propose]          │
  └───────────────────────┘  └───────────────────────────────┘
              └────────────┬─────────────┘
                           v
  ┌──────────────────────────────────────────────────────────┐
  │ BƯỚC 4 — LLM JUDGE + ReCAD hint  [Inferential/propose]    │
  │ ghép chéo → helix-receipt.json + gợi ý (KHÔNG ghi đè gốc) │
  └──────────────────────────────────────────────────────────┘
                           │
                           v
  ┌──────────────────────────────────────────────────────────┐
  │ BƯỚC 5 — CỔNG PHÊ DUYỆT QUÂN SỰ (HITL)  [Shared]         │
  │ kỹ sư định danh soi cờ đỏ · provenance audit · ký số      │
  └──────────────────────────────────────────────────────────┘
                           │
                           v
                    XUẤT XƯỞNG CHẾ TẠO
```

## Ánh xạ bước → tier → skill

| Bước spec | Loại | Skill | Trạng thái |
|----|----|----|----|
| **1** Trích xuất hình học tất định (STEP→AAG, mesh, va-chạm-dụng-cụ) | **Computational** | `helix-cad-validate` (`validate.py`) | DFM lỗ tất định ĐÃ chạy trên `cad_extract` 2D; engine STEP/AAG/GPU nặng = HOÃN |
| **2** KAN DFM (tabular + SHAP) | **Inferential — propose-only** | [[helix-design-review]] | mục tiêu; nay thay bằng LUẬT DFM tất định ở Bước 1 |
| **3** VLM 2D-3D alignment (Qwen2-VL, GD&T, correspondence) | **Inferential — propose-only** | [[helix-design-review]] | mục tiêu |
| **4** LLM-judge + ReCAD hint (propose-only, không ghi đè gốc) | **Inferential — propose-only** | [[helix-design-review]] | rubric-judge đã có; ReCAD hint = mục tiêu |
| **5** Military HITL + provenance sign | **Shared HITL** | `helix-cad-validate` Step 6 + khối `provenance` | ĐÃ có: engineer sign-off block + receipt provenance |

**Ranh giới bất di dịch:** hard-gate (exit 0/2) CHỈ phụ thuộc luật **tất định** ở Bước 1. Mọi kết quả
Inferential (Bước 2-4) là **đề xuất, không chặn** — kỹ sư định đoạt. Đây là điều giữ danh tính
"Computational-only, auditable" của Assay và tránh "AI tự phán an toàn" (Inferential thay Computational).

## Receipt & Provenance (helix-receipt)

`cad_validate_report.json` CHÍNH LÀ "biên bản kiểm tra kỹ thuật số" (helix-receipt) của Bước 5, mang khối
`provenance`: `linter_sha256` (mã-luật nào đã chấm) + `contract_sha256` (luật nào) + `tool_version` +
`python_version` + `validated_at`. Cổng HITL truy ngược đúng phiên bản công cụ + contract đã tạo verdict —
mọi thay đổi thiết kế truy vết được về kỹ sư chịu trách nhiệm.

## Improvement Engine (sai một lần, chặn mãi)

Finding Inferential (helix-design-review) lặp lại + được kỹ sư xác nhận → **nâng thành luật Computational**
trong `design_rules.json` (do kỹ sư định danh, bump `contract_version` + re-hash). Vòng khép: cái đọc-ngữ-cảnh
hôm nay → cái mã-hóa-được ngày mai.

## Hoãn (next tier — chỉ dựng khi có trigger)

Không dựng sớm. CHỈ triển khai khi gặp trigger thật (xem bảng "When to add the next tier" trong SKILL.md):
- **Engine geometry nặng** (OpenCASCADE B-Rep AAG, `manifold-3d` mesh, GPU BVH tool-collision) — khi có
  STEP thật + hạ tầng LAN biệt lập. Cần: kích hoạt `hole_depth_ratio` + check độ-kín-nước/độ-dày-thành 3D.
- **Stack server Inferential** (vLLM/Ollama + Qwen2-VL/LLaVA cho VLM & LLM-judge, KAN + SHAP cho DFM) — khi
  luật DFM tất định không đủ tinh. Chạy LOCAL cho MẬT/HẠN-CHẾ, không egress.
- **`.helix/rules.yaml` linter config + eval pass^k** — khi contract phình / lo phá thiết kế cũ; seed
  regression corpus ở `examples/`.

Blueprint cấu hình hạ tầng (image Docker, lệnh vLLM, tên model, định dạng `.helix/rules.yaml`) sẽ viết
thành reference doc riêng khi bước vào triển khai — HOÃN có chủ đích (QĐ CEO 2026-07-09).
