---
name: helix-cad-roundtrip
description: "Cross-phase CAD orchestrator — sequences the two mirror bridges (helix-cad-bridge OUT: code→STEP, helix-cad-ingest IN: drawing→record) across HELIX Phase 1-2-3-4, closing the geometry round-trip from RE intake to verified production handoff. Honest about LLM spatial blindness: parts the AI can't auto-generate are drawn EXTERNALLY by a human designer and IMPORTED back (Flow D Design-import), so every part gets a traceable geometry-of-record whether AI-parametric or human-CAD. NOT a P-phase block; a thin commander routing 4 flows (--ingest-first P1 RE seed · --forward AI-parametric synthesis · --design-import human-draws-externally→import→reconcile · --verify P4 export-drift loop) with a per-part Geometry Source Gate. Shares the classification label, LLM Spatial Blindness gate, and ICD rev-lock with both bridges. Defense-safe: no geometry leaves the machine. Triggers on: 'cad roundtrip', 'cad round-trip', 'cad pipeline', 'geometry loop', 'design import', 'import drawing into workflow', 'người thiết kế vẽ ngoài', 'nhập bản vẽ vào quy trình', 'designer draws', 'drawing request', 'design brief cad', 'vòng tròn CAD', 'pipeline CAD', 'khép vòng hình học', 'verify bản vẽ vs model', 'nguồn hình học'."
---

# helix-cad-roundtrip — Cross-Phase CAD Orchestrator (Local, Defense-Safe)

> **Role:** Chỉ huy mỏng (thin commander) — KHÔNG phải block của P1–P4. Điều phối **hai bridge gương** + **nhánh người-vẽ-ngoài** theo đúng thứ tự lifecycle.
> **Commands:** [[helix-cad-bridge]] (OUTBOUND: số liệu CEO → code-CAD → STEP + PNG) · [[helix-cad-ingest]] (INBOUND: PDF + DXF/DWG → `cad_extract.json` + `.md`) · `helix-cad-ingest/dwg_dxf_diff.py` (export-drift verifier).
> **Why an orchestrator, not a new bridge:** Hai bridge đã hoàn chỉnh và độc lập. Giá trị bị thiếu là **trình tự gọi + handoff contract** giữa chúng qua bốn phase — gồm cả **vòng khép** (model → bản vẽ → đọc lại → xác minh không drift) và **nhánh người thiết kế vẽ ngoài** mà chưa skill nào sở hữu.

## Sự thật nền tảng: AI KHÔNG tự sinh được mọi hình học
> Source: [[LLM Spatial Blindness — AI Không Có Mắt 3D Chỉ Có Miệng Code]]

`helix-cad-bridge` chỉ viết được code-CAD cho **chi tiết tham số hóa rõ ràng** (CEO cấp đủ số). Với phần lớn chi tiết phức tạp/hữu cơ/đòi hỏi phán đoán hình học ở **P2/P3/P4**, AI **không** dựng được — **người thiết kế phải vẽ trong app CAD thật** (SolidWorks/Inventor/…), export ra cặp PDF + DXF/DWG, rồi **import ngược** vào workflow. Đây không phải thiếu sót — đây là **phân công đúng**: con người vẽ hình (nơi AI mù không gian), AI viết brief + đọc-đối chiếu + giữ truy vết. Vì thế mỗi part đều có **geometry-of-record** dù nguồn là AI-parametric (Flow B) hay Human-CAD (Flow D).

## The Mirror Pair (cùng cột sống, ngược chiều)

| | helix-cad-bridge | helix-cad-ingest |
|----|----|----|
| Hướng | **OUTBOUND** — tổng hợp xuôi (ý tưởng → hình học) | **INBOUND** — phân tích ngược (hình học → spec) |
| Vào | Số liệu CEO + sketch | Cặp PDF + DXF/DWG có sẵn |
| Ra | `{{part}}.py` + `.step` + `.png` | `{{part}}.cad_extract.json` + `.md` |
| Interface | **STEP** (B-Rep handoff) | **cad_extract.json** (record handoff) |

**Cột sống dùng chung (orchestrator bảo toàn cả ba):**
1. **Classification label** — đặt một lần ở `helix-p1-validate` sacred constraints; CẢ HAI bridge đọc nó để bật egress guard (MẬT = offline-only, no cloud OCR). Orchestrator KHÔNG đặt lại label; nó truyền label xuống mọi bridge call.
2. **[[LLM Spatial Blindness]] gate** — bridge không bịa hình học, ingest không bịa số đọc; render/extract là bằng chứng, không phải code/đọc "trông đúng".
3. **ICD rev-lock** — mọi handoff (STEP hoặc cad_extract) đăng ký vào ICD, khóa theo rev. `helix-p3-integrate` đóng băng ICD v3 với STEP = giao diện hình học.

## Pipeline Architecture

```
        ┌──────────────────────── VÒNG KHÉP (round-trip) ────────────────────────┐
        ▼                                                                         │
  [Bản vẽ vào: RE / khách cấp / legacy]                          [Bản vẽ phát hành PDF+DXF từ P4]
        │ FLOW A: --ingest-first                                                  ▲ FLOW C: --verify
┌───────┼─────────┐ ┌──────────────────────────────────────────────┐ ┌───────────┼──────────────┐
│ P1 Clarify      │ │ P2 Concept · P3 Embodiment · P4 Detail        │ │ P4 Detail │              │
├─────────────────┤ ├──────────────────────────────────────────────┤ ├──────────────────────────┤
│ INGEST          │ │  ┌─ Geometry Source Gate (mỗi part, CEO Core)─┐│ │ BRIDGE → p4-drawing      │
│ → p1-requirements│ │  │ part tham số đơn giản → FLOW B            ││ │   (STEP→2D ISO/TCVN)     │
│ (label SET ở    │ │  │ part phức tạp/judgment → FLOW D           ││ │ INGEST → p4-inspection   │
│  p1-validate)   │ │  └──────────────────────────────────────────┘│ │ INGEST đọc lại bản vẽ ───┘│
│                 │ │   FLOW B (AI-parametric)   FLOW D (Human-CAD) │ │   + dwg_dxf_diff.py = QA  │
│                 │ │   BRIDGE: số CEO→code      AI ra Design Brief │ │                          │
│                 │ │     →STEP                    ↓ (hand-out)     │ │                          │
│                 │ │   → p2-develop             [Người vẽ NGOÀI    │ │ forge-fabrication:       │
│                 │ │   → p3-layout/dfx/bom        trong app CAD]   │ │  BRIDGE STEP F0→F5       │
│                 │ │   → p3-integrate (ICD v3)    ↓ export PDF+DXF │ │  INGEST extract→TCVN QTCN │
│                 │ │                            INGEST: import     │ │                          │
│                 │ │   ┌── cả B và D đổ về ────  → reconcile vs    │ │                          │
│                 │ │   cùng consumer ──────────   Brief           │ │                          │
└─────────────────┘ └──────────────────────────────────────────────┘ └──────────────────────────┘
```

## Four Flows (modes)

| Flow | Flag | When | Sequence |
|----|----|----|----|
| **A — Ingest-first** | `--ingest-first` | P1 RE / khách cấp bản vẽ / tái dùng legacy | ingest cặp PDF+DXF/DWG → `cad_extract.json` → seed `helix-p1-requirements` (hoặc `reverse-engineering`) |
| **B — Forward (AI-parametric)** | `--forward` | P2→P3→P4: part tham số hóa được | bridge từ số liệu CEO → STEP qua từng block (p2-develop → p3-layout/dfx/bom/integrate → p4-drawing → fab) |
| **D — Design-import (Human-CAD)** | `--design-import` | P2→P3→P4: part AI **không** dựng được → người vẽ ngoài | AI ra **Design Brief** → [người thiết kế vẽ trong app CAD, async] → export → **import** qua `helix-cad-ingest` → **reconcile vs Brief** → geometry-of-record |
| **C — Verify (loop)** | `--verify` | Sau P4: bản vẽ phát hành đã xuất | bridge-STEP/bản vẽ → ingest đọc lại bản vẽ phát hành → `dwg_dxf_diff.py` so khớp → xác nhận **no export-drift** |

> **B và D là hai mặt của cùng một bước "forward"** — cùng tạo hình học cho thiết kế, khác ở *ai vẽ*. Cả hai đổ vào cùng consumer (p3-integrate ICD, p3-bom, p4-drawing). **Geometry Source Gate** ở Step 1 định tuyến từng part vào B hoặc D.
> Round-trip riêng (P3 legacy reuse): `--ingest-first` rồi `--forward` trên cùng part = đọc chi tiết cũ → tham số hóa lại thành code-CAD chỉnh sửa được.

## How to Use

```
# P1 — bóc tách bản vẽ RE/khách cấp để seed requirements
/helix-cad-roundtrip VN-XUONG-UUV --ingest-first --pair gia-truot.pdf gia-truot.dxf

# P2→P4 — part tham số: AI dựng hình xuôi từ số liệu CEO
/helix-cad-roundtrip VN-XUONG-UUV --forward --part nose-cone

# P2→P4 — part phức tạp: AI ra brief → người vẽ ngoài → import ngược
/helix-cad-roundtrip VN-XUONG-UUV --design-import --part hull-casting

# Sau P4 — khép vòng: đọc lại bản vẽ phát hành, kiểm drift vs model
/helix-cad-roundtrip VN-XUONG-UUV --verify --part nose-cone

# Không flag → smart router hỏi đang ở đâu + nguồn hình học, đề xuất flow
/helix-cad-roundtrip VN-XUONG-UUV
```

## Orchestrator Workflow

### Step 1: Resolve Classification + Flow + Geometry Source (Router — CORE confirm)
1. **Read the project's classification label** from `helix-p1-validate` sacred constraints (default **MẬT** if unset for any defense product). Orchestrator only reads & propagates — never re-sets. Flag `[CLASSIFICATION-VIOLATION]` and STOP if any downstream bridge would touch the network for MẬT.
2. **Determine flow:** explicit flag wins. No flag → ask where in the lifecycle this part is:
   ```
   ═══ CAD ROUNDTRIP — {{project}} ═══
   Classification (from p1-validate): {{label}}
   Phần này đang ở đâu?
   (A) Có bản vẽ vào (RE/khách cấp/legacy)        → --ingest-first
   (B/D) Cần TẠO hình học cho thiết kế (P2/P3/P4)  → Geometry Source Gate ↓
   (C) Đã có bản vẽ phát hành, cần kiểm drift     → --verify
   ```
3. **Geometry Source Gate (CEO Core — chỉ cho B/D):** với mỗi part cần tạo hình, CEO quyết nguồn:
   ```
   ═══ GEOMETRY SOURCE GATE — {{part}} ═══
   Part này AI có dựng tham số được không?
   (B) ✅ Tham số rõ, CEO cấp đủ số  → --forward  (helix-cad-bridge viết code-CAD)
   (D) 🧑 Phức tạp/hữu cơ/cần phán đoán hình → --design-import (người thiết kế vẽ ngoài)
   ```
   *Mặc định an toàn:* nếu CEO không chắc, chọn **D** — AI mù không gian, ép code-CAD lên hình phức tạp là sai. Một assembly có thể trộn: vài part đi B, vài part đi D.
4. **Confirm part/rev scope.** Một flow xử lý một part (hoặc một assembly) tại một rev. Multi-part → loop flow theo part, không merge.

### Step 2: Execute the Flow — DELEGATE, never do bridge work inline
Orchestrator NEVER tự parse DXF hay viết code-CAD. Nó gọi bridge và relay handoff. Một bridge call → STOP tại CEO checkpoint của chính bridge đó.

- **Flow A (`--ingest-first`):** gọi `helix-cad-ingest` trên cặp file → emit `cad_extract.json` + `.md`, chạy **Step 6 critical-dim certification (CEO Core)**. CEO certify → route extract vào `helix-p1-requirements`/`reverse-engineering`. Đăng ký ICD record (rev-locked).

- **Flow B (`--forward`, AI-parametric):** gọi `helix-cad-bridge` với block tiêu thụ làm context (p2-develop / p3-layout / p3-dfx / p3-bom / p4-drawing / fab F0). Bridge chạy **Step 2 parametric intent (CEO Core)** + **Step 5 render verification (CEO Core)**. CEO approve → hand **STEP** sang block kế. `helix-p3-integrate` đóng băng ICD v3 với STEP.

- **Flow D (`--design-import`, Human-CAD) — nhánh người vẽ ngoài, 5 bước:**
  - **D1 — AI ra Design Brief (Offload).** Kéo từ ICD + requirements: envelope/bounding-box limit, interface points (mating face, hole pattern, datum) part phải tôn trọng, material, critical dims/tolerances, classification, và **trỏ người thiết kế vào "Export Requirements" của `helix-cad-ingest`** (R2013+ ASCII DXF, vector PDF, KHÔNG explode text/dim/block, units mm 1:1). Emit `Design_Brief_{{part}}.md`. Đây là bản hand-out — AI **không** vẽ hình, chỉ ra spec.
  - **D2 — [EXTERNAL, async] người thiết kế vẽ** trong app CAD thật theo Brief, rồi export cặp PDF+DXF/DWG. (Ngoài workflow; CEO/quản đốc giao việc.)
  - **D3 — Import (Offload).** Khi designer nộp file → gọi `helix-cad-ingest` đọc cặp → `cad_extract.json` + `.md` với confidence + source pointer.
  - **D4 — Reconcile vs Brief (Offload → CEO Core certify).** Đối chiếu extract với Design Brief: bounding-box ≤ envelope? interface (hole pattern/mating dims/datum) khớp? critical dims có mặt & trong dung sai? material/qty đúng? **Sai lệch → ghi `[CONFLICT: brief=… drawing=…]`, không tự "sửa".** Đây là điểm AI mạnh (đọc-so), bù cho điểm AI yếu (vẽ).
  - **D5 — CEO certify (Core).** CEO duyệt extract + giải quyết CONFLICT → đăng ký làm **geometry-of-record** của part trong ICD (rev-locked tới cặp file người vẽ), feed downstream y như STEP của Flow B.

- **Flow C (`--verify`):** sau P4 xuất bản vẽ phát hành (PDF+DXF), gọi `helix-cad-ingest` đọc **lại** bản vẽ phát hành, chạy `dwg_dxf_diff.py` so DXF phát hành với nguồn. **Drift directional** — nội dung có trong DXF nhưng VẮNG ở nguồn = drift thật; DWG-only (BOM/assembly sheet) = superset mong đợi, không phải drift.

### Step 3: Handoff Contract (dữ liệu duy nhất orchestrator luồn qua)
| Flow | In | Bridge | Out (handoff) | Consumer |
|----|----|----|----|----|
| A | PDF + DXF/DWG pair | helix-cad-ingest | `cad_extract.json` | helix-p1-requirements · reverse-engineering · forge-fabrication (BOM) · helix-p4-inspection |
| B | CEO dims + sketch | helix-cad-bridge | `{{part}}.step` (+ `.py` git source) | helix-p3-integrate (ICD v3) · helix-p4-drawing · forge-fabrication F0→F5 |
| D | Design Brief → [human draws] → PDF+DXF | helix-cad-ingest | `cad_extract.json` + reconcile verdict | helix-p3-integrate (ICD v3, geometry-of-record) · helix-p3-bom · helix-p4-drawing · forge-fabrication |
| C | released PDF + DXF | helix-cad-ingest + `dwg_dxf_diff.py` | drift verdict + `cad_extract.json` | CEO sign-off · helix-p4-inspection |

> **STEP (B) ↔ cad_extract.json (A/D/C) là interface gương.** Dù part sinh ra từ AI-parametric (STEP) hay Human-CAD (cad_extract), nó đăng ký vào **cùng một slot ICD** như geometry-of-record của part đó. Orchestrator không tự chuyển đổi giữa hai dạng; bridge sở hữu việc đó. Một part Flow-D về sau có thể được tham số hóa lại thành code-CAD qua Flow B nếu cần (round-trip).

### Step 4: Completion
```
═══ CAD ROUNDTRIP COMPLETE — {{project}} / {{part}} rev {{rev}} ═══
Flow run: {{A ingest-first | B forward | D design-import | C verify}}
Geometry source: {{AI-parametric (STEP) | Human-CAD (imported)}}
Classification: {{label}}   Egress guard (MẬT): [PASS — no network]
Handoff emitted: {{cad_extract.json | STEP | reconcile verdict | drift verdict}}
ICD registered: {{geometry-of-record rev {{n}} | verified-no-drift}}

CEO:
(1) ✅ Approve handoff → route to {{consumer}}
(2) 🔄 Re-run flow with corrections (Core)  / D: gửi lại Brief cho người vẽ
(3) ⏸️ Dừng — physical/CAD review trước
(4) ↻ Chạy flow kế tiếp ({{Gate part khác | B→C verify loop}})
```

## Integration Map
| Phase | Block that triggers a flow | Flow | Bridge it commands |
|----|----|----|----|
| P1 | helix-p1-requirements / reverse-engineering | A | helix-cad-ingest |
| P2 | helix-p2-develop | B or **D** (qua Gate) | helix-cad-bridge / helix-cad-ingest |
| P3 | helix-p3-layout / -dfx / -bom / -integrate | B or **D** (qua Gate) | helix-cad-bridge / helix-cad-ingest |
| P4 | helix-p4-drawing | B (STEP→2D) | helix-cad-bridge |
| P4 | helix-p4-inspection | A / C | helix-cad-ingest |
| fab | forge-fabrication | B (STEP) / A/D (extract→TCVN QTCN) | both |

## Rules
- **⛔ Orchestrator NEVER does bridge work itself** — never parses a DXF, never writes code-CAD. Always delegates. #1 rule.
- **AI never draws complex geometry** — nếu part không tham số hóa được, Gate → Flow D (người vẽ ngoài). Ép code-CAD lên hình phức tạp vi phạm [[LLM Spatial Blindness]]; mặc định Gate nghiêng về D khi CEO không chắc.
- **Flow D: AI ra Brief + reconcile, KHÔNG vẽ** — D1 là spec, không phải hình; D4 là đọc-so, điểm mạnh của AI bù điểm yếu vẽ.
- **One flow per turn, STOP at the bridge's own CEO checkpoint** — không chain Gate→B/D→C không có CEO approve giữa các bước.
- **Classification label is READ, not set** — propagated from `helix-p1-validate`; orchestrator chỉ enforce egress guard.
- **Critical dims / spatial intent / reconcile stay Core** — bridge Step 2/5, ingest Step 6, và D4/D5 reconcile certify đều non-delegable; orchestrator không self-certify hình học.
- **Mirror interfaces are sacred** — STEP (out) và cad_extract.json (in) cùng đăng ký một slot ICD geometry-of-record; không tự convert giữa hai.
- **Drift check is directional** — DXF-only = drift thật; DWG-only superset = expected.
- **One part, one rev per flow** — multi-part = loop, không merge (assembly file trộn part; loại khỏi cut-list).
- **Rev-lock every handoff** — part ra STEP rồi quay về bản vẽ PHẢI rev-bump; same-rev mismatch = silent wrong data.

## COD Classification
- Flow orchestration + handoff threading: Offload (O1)
- Bridge execution (parse / dựng / diff): Offload (O2) — each bridge has its own COD
- **Design Brief generation (D1):** Offload (O) — kéo spec từ ICD/requirements; CEO duyệt brief trước khi giao
- **Classification label propagation + egress guard:** Default (D) — automated assertion (label decision itself is Core, owned upstream)
- **Geometry Source Gate (B vs D per part):** Core (C) — non-delegable design judgment
- **Spatial intent / dimensions (bridge Step 2):** Core (C) — non-delegable
- **Geometry render verification (bridge Step 5):** Core (C) — [[LLM Spatial Blindness]] gate
- **Reconcile imported drawing vs Brief (D4) + certify (D5):** Core (C) — release gate
- **Critical-dim / GD&T certification (ingest Step 6):** Core (C) — [[LLM Spatial Blindness]] gate
- **Drift verdict sign-off (Flow C):** Core (C) — release gate
