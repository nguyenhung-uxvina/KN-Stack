---
name: helix-cad-roundtrip
description: "Cross-phase CAD orchestrator — sequences the two mirror bridges (helix-cad-bridge OUT: code→STEP, helix-cad-ingest IN: drawing→record) across HELIX Phase 1-2-3-4, closing the geometry round-trip from RE intake to verified production handoff. NOT a P-phase block; a thin commander that routes 3 flows (--ingest-first P1 RE seed · --forward P2→P3→P4→fab synthesis · --verify P4 export-drift loop). Shares the classification label, LLM Spatial Blindness gate, and ICD rev-lock with both bridges. Defense-safe: no geometry leaves the machine. Triggers on: 'cad roundtrip', 'cad round-trip', 'cad pipeline', 'code to cad to drawing', 'geometry loop', 'ingest then bridge', 'bridge then verify', 'vòng tròn CAD', 'pipeline CAD', 'khép vòng hình học', 'đọc rồi dựng lại', 'verify bản vẽ vs model', 'roundtrip hình học'."
---

# helix-cad-roundtrip — Cross-Phase CAD Orchestrator (Local, Defense-Safe)

> **Role:** Chỉ huy mỏng (thin commander) — KHÔNG phải block của P1–P4. Điều phối **hai bridge gương** đã có sẵn theo đúng thứ tự lifecycle.
> **Commands:** [[helix-cad-bridge]] (OUTBOUND: số liệu CEO → code-CAD → STEP + PNG) · [[helix-cad-ingest]] (INBOUND: PDF + DXF/DWG → `cad_extract.json` + `.md`) · `helix-cad-ingest/dwg_dxf_diff.py` (export-drift verifier).
> **Why an orchestrator, not a new bridge:** Hai bridge đã hoàn chỉnh và độc lập. Giá trị bị thiếu là **trình tự gọi + handoff contract** giữa chúng qua bốn phase — đặc biệt là **vòng khép** (model → bản vẽ → đọc lại → xác minh không drift) mà chưa skill nào sở hữu. Skill này tài liệu hóa và thực thi trình tự đó; nó KHÔNG tự parse/dựng hình — luôn ủy quyền cho bridge.

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
        ┌──────────────────── VÒNG KHÉP (round-trip) ────────────────────┐
        ▼                                                                 │
  [Bản vẽ vào: RE / khách cấp / legacy]                      [Bản vẽ phát hành PDF+DXF từ P4]
        │ FLOW A: --ingest-first                                          ▲ FLOW C: --verify
┌───────┼─────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────────┼──────────────┐
│ P1 Clarify      │ │ P2 Concept   │ │ P3 Embodiment│ │ P4 Detail        │              │
├─────────────────┤ ├──────────────┤ ├──────────────┤ ├─────────────────────────────────┤
│ INGEST          │ │ BRIDGE       │ │ BRIDGE  ★★   │ │ BRIDGE → p4-drawing (STEP→2D)   │
│ → p1-requirements│ │ → p2-develop │ │ → p3-layout  │ │ INGEST → p4-inspection (crit/GD&T)│
│ (label SET ở    │ │ (VDI2225 trên│ │ → p3-dfx     │ │ INGEST đọc lại bản vẽ phát hành ─┘│
│  p1-validate)   │ │  hình thật)  │ │ → p3-bom     │ │   + dwg_dxf_diff.py = QA loop    │
│                 │ │ INGEST(opt): │ │ → p3-integrate│ │                                 │
│                 │ │  baseline    │ │   ICD v3=STEP│ │ ── FLOW B: --forward ──────────▶│
│                 │ │              │ │ INGEST:round │ │  forge-fabrication              │
│                 │ │              │ │  -trip legacy│ │  BRIDGE: STEP F0→F5             │
│                 │ │              │ │              │ │  INGEST: extract → TCVN QTCN    │
└─────────────────┘ └──────────────┘ └──────────────┘ └─────────────────────────────────┘
```

## Three Flows (modes)

| Flow | Flag | When | Sequence |
|----|----|----|----|
| **A — Ingest-first** | `--ingest-first` | P1 RE / khách cấp bản vẽ / tái dùng legacy | ingest cặp PDF+DXF/DWG → `cad_extract.json` → seed `helix-p1-requirements` (hoặc `reverse-engineering`) |
| **B — Forward** | `--forward` | P2→P3→P4→fab (luồng thiết kế xuôi) | bridge từ số liệu CEO → STEP qua từng block (p2-develop → p3-layout/dfx/bom/integrate → p4-drawing → forge-fabrication F0) |
| **C — Verify (loop)** | `--verify` | Sau P4: bản vẽ phát hành đã xuất | bridge-STEP/bản vẽ → ingest đọc lại bản vẽ phát hành → `dwg_dxf_diff.py` so khớp → xác nhận **no export-drift** |

> Round-trip riêng (P3 legacy reuse): `--ingest-first` rồi `--forward` trên cùng part = đọc chi tiết cũ → tham số hóa lại thành code-CAD chỉnh sửa được (đúng dòng "Re-parameterize an ingested profile" trong Integration Map của ingest).

## How to Use

```
# P1 — bóc tách bản vẽ RE/khách cấp để seed requirements
/helix-cad-roundtrip VN-XUONG-UUV --ingest-first --pair gia-truot.pdf gia-truot.dxf

# P2→P4 — dựng hình xuôi từ số liệu CEO
/helix-cad-roundtrip VN-XUONG-UUV --forward --part nose-cone

# Sau P4 — khép vòng: đọc lại bản vẽ phát hành, kiểm drift vs model
/helix-cad-roundtrip VN-XUONG-UUV --verify --part nose-cone

# Không flag → smart router hỏi đang ở đâu trong lifecycle, đề xuất flow
/helix-cad-roundtrip VN-XUONG-UUV
```

## Orchestrator Workflow

### Step 1: Resolve Classification + Flow (Router — CORE confirm)
1. **Read the project's classification label** from `helix-p1-validate` sacred constraints (default **MẬT** if unset for any defense product). The orchestrator does NOT set it — it only reads and propagates. Flag `[CLASSIFICATION-VIOLATION]` and STOP if any downstream bridge would touch the network for MẬT.
2. **Determine flow:** explicit flag (`--ingest-first`/`--forward`/`--verify`) wins. No flag → ask the CEO where in the lifecycle this part is and propose a flow:
   ```
   ═══ CAD ROUNDTRIP — {{project}} ═══
   Classification (from p1-validate): {{label}}
   Phần này đang ở đâu?
   (A) Có bản vẽ vào (RE/khách cấp/legacy) → --ingest-first
   (B) Thiết kế xuôi từ số liệu CEO       → --forward
   (C) Đã có bản vẽ phát hành, cần kiểm   → --verify
   ```
3. **Confirm part/rev scope.** A flow operates on one part (or one assembly) at one rev. Multi-part → loop the flow per part, never merge.

### Step 2: Execute the Flow — DELEGATE, never do bridge work inline
The orchestrator NEVER parses a DXF or writes code-CAD itself. It calls the bridge skill and relays the handoff. One bridge call → STOP at that bridge's own CEO checkpoint.

- **Flow A (`--ingest-first`):** invoke `helix-cad-ingest` on the pair → it emits `cad_extract.json` + `.md` and runs its **Step 6 critical-dim certification (CEO Core)**. On CEO certify → route the extract to `helix-p1-requirements` (seed measured requirements) or `reverse-engineering` (teardown). Register the extract in the ICD as an **ingested** record (rev-locked to the source pair).
- **Flow B (`--forward`):** invoke `helix-cad-bridge` with the consuming block as context (p2-develop / p3-layout / p3-dfx / p3-bom / p4-drawing / forge-fabrication F0). Bridge runs its **Step 2 parametric intent (CEO Core)** + **Step 5 render verification (CEO Core)**. On CEO approve → hand the versioned **STEP** to the next block. `helix-p3-integrate` freezes ICD v3 with STEP as the geometry interface.
- **Flow C (`--verify`):** after P4 exports the released drawing (PDF+DXF), invoke `helix-cad-ingest` to read the **released drawing** back, then run `dwg_dxf_diff.py` (export-drift verifier) comparing the released DXF against the native source. Surface the verdict; **drift is directional** — content in DXF but ABSENT from the source DWG = real drift; DWG-only content (BOM/assembly sheets) is expected, not drift (see ingest Gotchas).

### Step 3: Handoff Contract (the only data the orchestrator threads)
| Flow | In | Bridge | Out (handoff) | Consumer |
|----|----|----|----|----|
| A | PDF + DXF/DWG pair | helix-cad-ingest | `cad_extract.json` | helix-p1-requirements · reverse-engineering · forge-fabrication (BOM) · helix-p4-inspection (crit/GD&T) |
| B | CEO dims + sketch | helix-cad-bridge | `{{part}}.step` (+ `.py` git source) | helix-p3-integrate (ICD v3) · helix-p4-drawing · forge-fabrication F0→F5 |
| C | released PDF + DXF | helix-cad-ingest + `dwg_dxf_diff.py` | drift verdict + `cad_extract.json` | CEO sign-off · helix-p4-inspection |

> **STEP in ↔ cad_extract.json out are mirror interfaces.** A round-trip part flows out as STEP (Flow B) and, once drawn and released, comes back in as cad_extract.json (Flow A/C) — same part, rev-bumped. The orchestrator never converts between them itself; the bridges own that.

### Step 4: Completion
```
═══ CAD ROUNDTRIP COMPLETE — {{project}} / {{part}} rev {{rev}} ═══
Flow run: {{A ingest-first | B forward | C verify}}
Classification: {{label}}   Egress guard (MẬT): [PASS — no network]
Handoff emitted: {{cad_extract.json | STEP | drift verdict}}
ICD registered: {{ingested record | STEP v{{n}} | verified-no-drift}}

CEO:
(1) ✅ Approve handoff → route to {{consumer}}
(2) 🔄 Re-run flow with corrections (Core)
(3) ⏸️ Dừng — physical/CAD review trước
(4) ↻ Chạy flow kế tiếp ({{A→B round-trip | B→C verify loop}})
```

## Integration Map
| Phase | Block that triggers a flow | Flow | Bridge it commands |
|----|----|----|----|
| P1 | helix-p1-requirements / reverse-engineering | A | helix-cad-ingest |
| P2 | helix-p2-develop | B (+ A optional baseline) | helix-cad-bridge (+ helix-cad-ingest) |
| P3 | helix-p3-layout / -dfx / -bom / -integrate | B (+ A round-trip legacy) | helix-cad-bridge (+ helix-cad-ingest) |
| P4 | helix-p4-drawing | B | helix-cad-bridge |
| P4 | helix-p4-inspection | A / C | helix-cad-ingest |
| fab | forge-fabrication | B (STEP) / A (extract→TCVN QTCN) | both |

## Rules
- **⛔ Orchestrator NEVER does bridge work itself** — never parses a DXF, never writes code-CAD. Always delegates to `helix-cad-bridge` / `helix-cad-ingest`. This is the #1 rule.
- **One flow per turn, STOP at the bridge's own CEO checkpoint** — never chain Flow A→B→C without explicit CEO approval between them.
- **Classification label is READ, not set** — propagated from `helix-p1-validate`; orchestrator only enforces the egress guard, never reclassifies.
- **Critical dims / spatial intent stay Core** — ingest's Step 6 certification and bridge's Step 2/5 verification are non-delegable; the orchestrator never self-certifies geometry.
- **Mirror interfaces are sacred** — STEP (out) and cad_extract.json (in); the orchestrator threads only these, never converts between them.
- **Drift check is directional** — DXF-only content = real export drift; DWG-only (BOM/assembly sheets) = expected superset, not drift.
- **One part, one rev per flow** — multi-part = loop, never merge (assembly files mix parts; exclude from cut-lists).
- **Rev-lock every handoff** — a part that went out as STEP and returns as a drawing MUST be rev-bumped; same-rev mismatch = silent wrong data.

## COD Classification
- Flow orchestration + handoff threading: Offload (O1)
- Bridge execution (parse / dvng / diff): Offload (O2) — each bridge has its own COD
- **Classification label propagation + egress guard:** Default (D) — automated assertion (label decision itself is Core, owned upstream)
- **Spatial intent / dimensions (bridge Step 2):** Core (C) — non-delegable
- **Geometry render verification (bridge Step 5):** Core (C) — [[LLM Spatial Blindness]] gate
- **Critical-dim / GD&T certification (ingest Step 6):** Core (C) — [[LLM Spatial Blindness]] gate
- **Drift verdict sign-off (Flow C):** Core (C) — release gate
