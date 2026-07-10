---
name: leo-bridge
description: "Vòng khép kín bán tự động Workshop X ↔ getleo.ai qua MCP server local (mcp/leo-bridge). 6 tools: leo_classify (gate MẬT hard-block + redaction) → leo_prompt_build (template leo-assist mode A–F, ép 5 nguyên tắc) → leo_send (gate lần 2 + clipboard + ledger) → CEO dán vào app.getleo.ai → leo_ingest (parse + verify checklist UNVERIFIED) → leo_route (propose-only, chặn UNVERIFIED vào parts_master) + leo_ledger (traceability). Transport hybrid-ready: clipboard bây giờ, API stub chờ getleo.ai cấp access. Triggers on: 'leo bridge', 'gửi leo', 'hỏi leo', 'kết nối leo', 'leo mcp', 'ask leo', 'send to leo', 'leo exchange', 'leo ledger', 'ingest leo', 'kết quả leo', 'đem kết quả leo về'."
---

# leo-bridge — Vòng khép kín Leo AI (MCP)

> **Role:** Orchestrate 6 MCP tools của server `leo-bridge` thành vòng khép kín. Doctrine + template = [[leo-assist]] (source of truth); skill này là CÁCH THI HÀNH programmatic.
> **Prereq:** MCP server `leo-bridge` trong `.mcp.json`. Cài dependency: `pip install -r mcp/leo-bridge/requirements.txt`. Kiểm tra: tool `leo_ledger` gọi được.

## Vòng chuẩn (mọi tác vụ Leo)

```
1. leo_classify(task)        → MAT? → CEO trừu tượng hóa (dùng redacted làm gợi ý) → classify lại
2. leo_prompt_build(mode, params, assumptions)   ← mode theo bảng Phase×Mode của leo-assist
3. leo_send(prompt, mode)    → exchange_id; prompt đã trong clipboard
4. [CEO] dán vào app.getleo.ai → copy TOÀN BỘ kết quả
5. leo_ingest(exchange_id)   → parsed + verify_checklist (mọi số = UNVERIFIED) + proposed_routes
6. [CEO] mở nguồn cite, xác minh từng mục checklist
7. leo_route(exchange_id, target_type, target_path, confirm=true, verified_items=[...])
```

## Chọn mode + tham số
- Mode A–F + phase: theo [[leo-assist]] (bảng Phase×Mode). Tham số bắt buộc từng mode: tool tự báo nếu thiếu — cấp giá trị ĐỊNH LƯỢNG (tải + đơn vị, kích thước interface thật).
- Sinh hình học concept (mesh) → [[leo-prompt]], KHÔNG qua bridge (Leo không sinh CAD production).

## UI Leo hiện hành (2026-07)
- app.getleo.ai = **1 khung chat thống nhất**, 4 nhóm intent gợi ý: **Calculate · Develop · Part search · Learn** (xem bảng map Mode→nhóm trong [[leo-assist]]). `leo_send` tự kèm gợi ý nhóm trong instructions; dòng `[MODE]` đầu prompt là tín hiệu route cho Leo.
- Mode C có thể yêu cầu Leo **vẽ plot** (Calculate hỗ trợ "Calculate and plot…").
- Kênh ngoài bridge (THƯỜNG only, thao tác tay): desktop app "Leo in CAD" (⛔ KHÔNG cài trên máy chứa bản vẽ MẬT), CAD-to-CAD part search, sketch-upload — classification gate như cũ.

## Targets của leo_route
| target_type | Đích | Ràng buộc |
|---|---|---|
| `parts_master_csv` | STAGING CSV (CEO merge tay vào parts_master thật) | CHẶN nếu còn mục UNVERIFIED |
| `calc_md` | Calc sheet markdown | UNVERIFIED được, gắn nhãn |
| `journal_md` | Design journal | UNVERIFIED được, gắn nhãn |

Skill tiêu thụ tiếp: part rows → [[forge-fabrication]] (BOM mua ngoài) · calc → [[helix-p3-dfx]] verify · spec text → [[helix-p1-requirements]].

## Gotchas
- **Gate chạy 2 lần** (classify + send) — prompt viết tay không qua build vẫn bị chặn nếu MẬT. Không có override.
- **BLOCKED ≠ lỗi:** dùng `redacted_suggestion` làm khung, thay [REDACTED] bằng mô tả chức năng generic.
- **Clipboard rỗng / kết quả <80 ký tự** → ingest từ chối; copy lại toàn bộ kết quả Leo.
- **Ledger** = `mcp/leo-bridge/ledger/ledger.jsonl` (gitignored). `leo_ledger("pending")` xem exchange dở dang.
- **Ingest lại = mất dấu VERIFIED:** gọi leo_ingest lần 2 sinh checklist mới toàn UNVERIFIED — phải verify lại từ đầu (fail-safe chủ ý).

## COD
- Vòng tools (build/send/ingest/route): Offload (O)
- **Trừu tượng hóa prompt MẬT: Core (C)** — CEO quyết định ngữ nghĩa
- **Verify cite từng mục checklist: Core (C)** — số Leo là điểm khởi đầu, người chốt
- **confirm=true cho leo_route: Core (C)** — propose-only doctrine
