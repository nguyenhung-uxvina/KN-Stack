---
name: helix-s2c-validate
description: "Block BE of Spec-to-CAD pipeline — DELEGATES deterministic gating to helix-cad-validate: runs validate.py with the project's design_rules.json (compiled from the CAD constitution at preflight) using --approved-hash anti-tamper; exit 0 = gate OPEN, exit 2 = machine-readable fix-hints loop back to BD implement. Registers the STEP as ICD geometry-of-record when inside a HELIX project. Acceptance = validate PASS + CEO render check; engineer-of-record sign-off stays outside AI. Triggers on: 's2c validate', 'validate part', 'chấm part theo luật', 'gate spec-to-cad', 'kiểm tra part cuối'."
---

# helix-s2c-validate — Block BE: Deterministic Gate via helix-cad-validate

> **Role:** Block BE của [[helix-spec-to-cad]] — phase SDD `validate` (analyze+gate).
> **Thin delegator** — sensor thật là `validate.py` của [[helix-cad-validate]] (stdlib,
> CPU, air-gapped, no LLM). Block này chỉ chuẩn bị input, chạy sensor, đọc verdict.
> **In:** mass-props JSON (từ BD) + `design_rules.json` (compile ở B0, sha256 kỹ sư giữ).
> **Out:** `cad/validated/{{part_id}}.cad_validate_report.{json,md}` + gate verdict.

## Workflow

### 1. Ledger Read
Đọc `_pipeline_state.md`. Xác nhận BD APPROVED (CEO đã kiểm render). Lấy path mass-props,
design_rules.json, approved-hash (kỹ sư cấp — KHÔNG lấy từ ledger nếu kỹ sư giữ ngoài).

### 2. Run the sensor (Offload — deterministic)
```
PYTHONUTF8=1 python skills/helix/helix-cad-validate/validate.py \
  --extract {{part_id}}.cad_extract.json  # nếu có (part từng qua ingest) \
  --mass-props cad/{{part_id}}.massprops.json \
  --rules design_rules.json --approved-hash {{sha256}} \
  --out cad/validated/{{part_id}}
```
- Part thuần Flow-B (chưa có cad_extract): chấm bằng mass-props + rules áp được
  (mass_kg, safety_factor, materials, contract_integrity). Rule `required:true` thiếu
  dữ liệu → FAIL fail-safe — ĐÚNG THIẾT KẾ, cấp dữ liệu hoặc kỹ sư hạ required có chủ đích.

### 3. Gate verdict (deterministic)
- **exit 0 — PASS, gate OPEN:** đủ điều kiện SC-003. Sang bước 4.
- **exit 2 — FAIL, gate CLOSED:** đọc fix-hints máy-đọc-được trong report → **loop về BD**
  (sửa param → regenerate → CEO render check → chạy lại BE). KHÔNG sửa design_rules.json
  để gate xanh — contract read-only-với-agent, hash sẽ bắt.

### 4. Register + completion (CEO Core — BLOCKING)
- Trong HELIX project: đăng ký STEP vào **ICD geometry-of-record** (cùng slot Flow B của
  [[helix-cad-roundtrip]], rev-locked) — helix-p3-integrate/p4/forge-fabrication tiêu thụ.
- Standalone: ghi `cad_manifest.md` (part_id ↔ classification ↔ params ↔ rev).
```
═══ BLOCK BE COMPLETE — SPEC-TO-CAD DONE: {{part_id}} ═══
Verdict: {{PASS|FAIL}} ({{n_fail}}/{{n_checks}}) · Hash-OK: {{y/n}} · Gate: {{OPEN|CLOSED}}
SC scorecard: SC-001 bbox ✅ · SC-002 mass ✅ · SC-003 validate ✅ · SC-004 render ✅
Còn lại NGOÀI AI: kỹ sư định danh ký sign-off block trong report .md
CEO: (1) ✅ Close pipeline → handoff {{ICD/fab}}  (2) 🔄 Loop BD  (3) ⏸️ Dừng
```

## Rules
- **⛔ Block NEVER judges pass/fail itself** — verdict là exit code của validate.py.
  Không LLM "tự phán an toàn" thay Computational sensor.
- **Contract read-only-với-agent** — mọi run dùng `--approved-hash`; sửa contract = kỹ sư.
- FAIL → loop BD, không "giải thích cho qua".
- **PASS = chuẩn TỐI THIỂU** — chữ ký kỹ sư định danh là cổng cuối, không AI, không auto-merge.
- Acceptance đầy đủ = SC-003 (validate PASS) **VÀ** SC-004 (CEO render check từ BD).

## COD
- Chạy sensor, đọc report, thread fix-hints về BD: Offload (O)
- **approved-hash custody: Core (C)** — kỹ sư giữ, chống tự-sửa-rào
- **Engineer-of-record sign-off: Core (C)** — ngoài AI
- Egress guard (stdlib, offline): Default (D)
