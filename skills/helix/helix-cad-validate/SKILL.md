---
name: helix-cad-validate
description: "Design-phase Computational Sensor + Gate — chấm cad_extract.json (từ helix-cad-ingest) + mass-props (từ helix-cad-bridge) theo một design_rules.json contract có phiên bản, trả PASS/FAIL TẤT ĐỊNH (CPU, stdlib-only, air-gapped), và CHẶN handoff sang forge-fabrication / chặn freeze ICD nếu fail. Đây là 'harness vật lý' pha Thiết kế: cơ-chế-không-phải-prompt, fail-safe (thiếu/LOW-confidence cho rule tới hạn → FAIL), contract read-only-với-agent (kiểm hash đã-duyệt chống tự-sửa-rào). PASS = đạt chuẩn TỐI THIỂU, KHÔNG thay chữ ký kỹ sư định danh. BƯỚC 1 của lộ trình validator (mentor-harness-engineering-council DEBATE 2026-06-25); thêm middleware/eval/inferential KHI có trigger. Triggers on: 'cad validate', 'design rule check', 'kiểm tra thiết kế', 'validator thiết kế', 'design gate', 'cổng thiết kế', 'design_rules', 'chấm bản vẽ theo luật', 'computational sensor', 'gate tất định', 'check cad_extract', 'kiểm tra ràng buộc thiết kế'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-cad-validate: Design-Rule Validator (Computational Sensor + Gate)

> **Role:** Cross-phase **Computational Sensor + Gate** for the DESIGN phase. Sits AFTER geometry
> exists ([[helix-cad-bridge]] code-CAD or [[helix-cad-ingest]] extract) and BEFORE
> [[forge-fabrication]] handoff / ICD freeze ([[helix-p3-integrate]]).
> **Backend:** pure-stdlib Python (`validate.py` v2.0) — runs LOCAL, offline, air-gapped. No LLM, no network.
> **Interface in:** `cad_extract.json` (+ optional mass-props json) + `design_rules.json` contract.
> **Interface out:** `cad_validate_report.json` = **receipt tất định (provenance-signed)** + `.md` (CEO/engineer readable) + exit code.
> **Lineage:** BƯỚC 1 of the validator roadmap from the harness-engineering DEBATE (2026-06-25); see
> `D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/20260625-debate-vsn1500-validator-architecture.md`.
> **Sản phẩm:** Computational spine của **"Assay"** AI Design-Review Gate. Phần Inferential (KAN DFM /
> VLM 2D-3D / LLM-judge) là PROPOSE-ONLY, thuộc [[helix-design-review]] — xem `references/assay-architecture.md`.

## Why this exists (the harness gap it closes)
helix-cad-bridge + helix-cad-ingest already PRODUCE structured JSON. What was missing is the
**deterministic yardstick + gate**: nothing checked the design against engineering constraints and
blocked bad output structurally. Per KHUNG HARNESS ENGINEERING v1.0 §5.2 (pha THIẾT KẾ), the design
phase needs GUIDES (ràng buộc cứng) → **SENSORS (validator tất định mỗi phương án)** → GATES
(kỹ sư định danh ký). This skill is that Computational Sensor + Gate. [[mentor-harness-engineering-council]]

## Operational Envelope
| DO | DON'T |
|----|----|
| Chấm Pass/Fail TẤT ĐỊNH theo luật khai trong contract | Để LLM "tự phán an toàn" (Inferential thay Computational) |
| Fail-safe: thiếu / LOW-confidence cho rule critical → FAIL | Silent SKIP một rule `required` khi thiếu dữ liệu |
| Giữ contract READ-ONLY với agent; kiểm `--approved-hash` | Cho agent sửa `design_rules.json` để gate xanh |
| Chạy mỗi iteration thiết kế (rẻ, nhanh, CPU) | Coi PASS = an toàn xuất xưởng (chỉ là chuẩn tối thiểu) |
| Chạy offline cho MẬT/HẠN-CHẾ | Gọi cloud / thêm lib mạng |

## The contract = GUIDE + yardstick
`design_rules.json` is versioned, **edited only by a kỹ sư định danh**, and is BOTH a Guide (nạp vào
AGENTS.md/context TRƯỚC khi agent vẽ) and the SENSOR's yardstick. Schema + rule keys:
`references/design_rules.schema.md`. Pilot for VSN-1500: `references/design_rules.vsn1500.example.json`.

Rule keys (mỗi cái tùy chọn): `materials` · `plate_thickness_mm` · `mass_kg` · `safety_factor`
· `tolerance_mm` · `mandatory_components` · `weld_standard` · `load_class` · `conflicts_block`
· `bom_master` · `confidence_gate` · `mass_reconciliation` · **DFM tất định:** `min_hole_dia_mm` ·
`hole_spacing_mm` · `hole_depth_ratio` (opt-in, cần depth 3D). Severity `critical`/`major` — **mọi FAIL đóng gate**.

**`mass_reconciliation` (Sanity-Check vật lý — Δ-C)**: đối chiếu khối lượng **bottom-up** (Σ tôn+outfit
từ `mass_props.bottom_up_kg`, hoặc tính từ BOM có `area_m2`+`thickness_mm`+vật liệu) ↔ **lightship estimate**
(`reference_kg`, kỹ sư khai) trong dung sai % (`scope:"assembly"` ±5% / `"part"` ±3%, CEO chốt 2026-07-17).
Lệch = dấu hiệu sai-trích-xuất/thiếu-part/vật-liệu-sai — neo bằng vật lý, không "đo theo tỷ lệ thước".
Gate **không bịa** diện tích: BOM thiếu dữ liệu → `require_complete` cho FAIL (fail-safe).

## Bản đồ kiến trúc 5-bước (Assay)
Spec 5-bước ánh xạ vào cặp validator — **hard-gate CHỈ tất định; KAN/VLM/LLM-judge là đề xuất, KHÔNG chặn**
(nguyên tắc [[Sensor-Not-Generator Law]]: AI làm Sensor, không làm Actor). Chi tiết: `references/assay-architecture.md`.

| Bước spec | Loại | Nơi thực thi |
|----|----|----|
| 1 Trích xuất hình học tất định (STEP/AAG/mesh/tool-collision) | Computational | **skill này** — nay + DFM lỗ tất định; engine STEP/GPU nặng = server air-gapped (HOÃN) |
| 2 KAN DFM · 3 VLM 2D-3D · 4 LLM-judge | **Inferential (propose-only)** | → [[helix-design-review]] (BƯỚC 2) |
| 5 Military HITL + provenance sign | Shared HITL | kỹ sư định danh ký (Step 6) + khối `provenance` trong receipt |

## Backend
```
# stdlib only — nothing to install. Windows: prefix PYTHONUTF8=1.
python validate.py --extract <part.cad_extract.json> --rules <design_rules.json> \
                   [--mass-props <mp.json>] [--out <basename>] [--approved-hash <sha256>] [--quiet]
# exit 0 = PASS (gate OPEN, pending engineer sign-off) · 2 = FAIL (gate CLOSED) · 3 = IO error
```

## Workflow

### Step 1: Resolve contract + classification (CORE)
Locate the project's `design_rules.json` (per-project, e.g. `1_Projects/VSN-1500/.../design_rules.json`).
If none exists → copy the schema (`references/design_rules.schema.md`) + nearest example, and have the
**kỹ sư định danh** fill real limits (số liệu RE/tính toán, KHÔNG để placeholder). Read Geometry
Classification (helix-p1-validate); for MẬT/HẠN-CHẾ assert offline.

### Step 2: Gather inputs (Offload)
- `cad_extract.json` từ [[helix-cad-ingest]] (đã qua confidence-gate certify), và/hoặc
- mass-props json từ [[helix-cad-bridge]] (`{"mass_kg":…, "safety_factor":…}`) nếu có.

### Step 3: Compute approved-hash once (CORE — chống tự-sửa-rào)
Kỹ sư duyệt contract → ghi lại sha256:
```
python -c "import hashlib;print(hashlib.sha256(open('design_rules.json','rb').read()).hexdigest())"
```
Lưu hash này NGOÀI tầm ghi của agent (vd biến CI / file kỹ sư giữ). Mọi lần chạy gate dùng
`--approved-hash <sha256>`; nếu contract bị sửa → `contract_integrity` FAIL.

### Step 4: Run the sensor (Offload — chạy mỗi iteration)
`python validate.py --extract … --rules … --approved-hash …`. Đọc `cad_validate_report.md`:
mỗi FAIL kèm observed/expected/fix-hint máy-đọc-được → bơm lại cho agent tự sửa (sensor feedback).

### Step 5: Gate (deterministic)
- **exit 0 / PASS** → gate OPEN: cho phép handoff [[forge-fabrication]] / freeze ICD —
  **nhưng vẫn chờ chữ ký kỹ sư định danh** (Step 6).
- **exit 2 / FAIL** → gate CLOSED: CẤM handoff/freeze. Agent sửa thiết kế, chạy lại. Lỗi tái diễn
  loại mới → thêm 1 luật vào contract (Improvement Engine — qua kỹ sư).

### Step 6: Engineer-of-record sign-off (CORE — không AI)
PASS của validator = ĐẠT CHUẨN TỐI THIỂU. Kết luận kết cấu/mỏi/FEA và phê duyệt cuối do **kỹ sư
định danh ký** (block ký trong `.md`). Cấm tuyệt đối auto-merge AI vào luồng sản xuất.

## When to add the next tier (DEBATE trigger-based — KHÔNG theo lịch)
Giữ BƯỚC 1 tối thiểu. CHỈ thêm khi gặp trigger thật:
| Trigger | Thêm | Loại |
|----|----|----|
| Agent doom-loop (sửa 1 lỗi > N lần) | LoopDetection middleware | Computational |
| `design_rules.json` phình > ~10k token, agent bỏ sót luật | compaction / sub-agent RAG tra ISO | kiến trúc |
| Cần chấm phi-cấu-trúc (thủy động khoang phao) | LLM-as-judge có rubric → ✅ [[helix-design-review]] (BƯỚC 2, propose-only) | **Inferential** |
| Sửa contract → lo phá thiết kế cũ | eval harness Capability/Regression, **pass^k** (seed ở `examples/`) | Computational |
| Có STEP thật + cần AAG/mesh/tool-collision | engine geometry nặng (OpenCASCADE B-Rep, GPU BVH) — server air-gapped | kiến trúc |
| Luật DFM tất định không đủ tinh (bề mặt/fillet phức tạp) | KAN DFM + SHAP → helix-design-review (propose-only) | **Inferential** |

## Integration Map
| Producer | → | helix-cad-validate | → | Consumer |
|----|----|----|----|----|
| helix-cad-ingest (`cad_extract.json`) | → | **SENSOR+GATE** | → | forge-fabrication (chỉ khi PASS + ký) |
| helix-cad-bridge (mass-props) | → | | → | helix-p3-integrate (ICD freeze chỉ khi PASS) |
| design_rules.json (kỹ sư định danh) | → | (yardstick, read-only) | | helix-p4-inspection (kế thừa luật→plan đo) |
| helix-s2c-validate (Spec-to-CAD BE — contract compiled từ CAD Constitution ở s2c-preflight) | → | (delegator) | → | Spec-to-CAD close-out |

## Gotchas
- **BOM thickness = MED confidence** (BOM rows không mang confidence field). Đặt `plate_thickness_mm.min_confidence: "MED"` nếu chấp nhận nguồn BOM/nesting; để `"HIGH"` thì buộc có dimension đã-certify.
- **Placeholder limits**: ví dụ VSN-1500 là PILOT — số min/max PHẢI do kỹ sư hiệu chỉnh theo tính toán thật trước khi dùng làm gate sản xuất.
- **Windows UTF-8**: chạy với `PYTHONUTF8=1` để tránh cp1252 crash khi report tiếng Việt (file luôn ghi UTF-8).
- **Fail-safe nhiểu nhầm là "khó tính"**: thiếu dữ liệu cho rule `required` → FAIL là CHỦ Ý (an toàn khí tài), không phải bug. Cấp dữ liệu hoặc hạ `required:false` có chủ đích.
- **Mandatory components dò bằng text** (tên BOM/notes). Dùng list synonym (vd `["junction plate","tấm liên kết"]`) để bắt cả tiếng Việt/Anh.
- **`mass_reconciliation` là check cấp CỤM, không phải cấp part**: đối chiếu tổng bottom-up ↔ lightship chỉ có nghĩa khi extract mang **toàn bộ** part (aggregate) hoặc có `mass_props.bottom_up_kg` đã cộng đủ. Chạy trên 1 part lẻ với `require_complete:true` sẽ FAIL đúng (tổng thiếu) — đó là fail-safe, không phải bug. Muốn dùng: trỏ vào extract tổng-hợp hoặc cấp bottom-up đã tính từ `helix-cad-bridge`.
- **`reference_kg` placeholder**: ví dụ VSN-1500 để `required:false` + số lightship PLACEHOLDER — kỹ sư định danh PHẢI thay bằng ước tính naval-architect thật trước khi bật gate sản xuất (giống `plate_thickness_mm` pilot).

## Output
Per-part vào `1_Projects/{{project}}/.../cad/validated/`:
- `{{part_id}}.cad_validate_report.json` (gate signal + **receipt tất định**, machine) — mang khối
  `provenance` `{tool_version, linter_sha256, contract_sha256, python_version, validated_at}` = dấu
  vết truy nguyên cho cổng HITL (Bước 5): kỹ sư ký biết CHÍNH XÁC phiên bản linter + contract nào đã chấm.
- `{{part_id}}.cad_validate_report.md` (engineer-readable + sign-off block + dòng provenance)

## CEO/Engineer Checkpoint
```
═══ helix-cad-validate ═══
Part: {{part_id}}   Contract: {{product}} rev{{rev}} v{{ver}}   Hash-OK: {{y/n}}
Verdict: {{PASS|FAIL}}   ({{n_fail}}/{{n_checks}})   Gate: {{OPEN|CLOSED}}
FAIL → sửa thiết kế / re-ingest, chạy lại.   PASS → kỹ sư định danh ký cổng cuối.
```

## COD
- Run validator, parse report, feed fixes to agent: Offload (O)
- **design_rules.json authoring/edit: Core (C)** — kỹ sư định danh, non-delegable
- **approved-hash custody: Core (C)** — chống agent tự-sửa-rào
- **Engineer-of-record final sign-off: Core (C)** — PASS ≠ an toàn, không AI
- Offline/egress guard (MẬT): Default (D) — stdlib-only, no network
