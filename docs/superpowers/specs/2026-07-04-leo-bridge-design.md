# Design Spec — `leo-bridge`: MCP server + skill wrapper kết nối getleo.ai

> Date: 2026-07-04 · Status: approved by CEO (design review) · Branch: `feature/helix-leo-bridge`
> Nguồn nghiên cứu: mentor-getleo-ai (NLM 2848c37a) + `RESEARCH_getleo-ai_2026-06-26.md` + web check getleo.ai/api

## 1. Bối cảnh & mục tiêu

Leo AI (getleo.ai) là Large Mechanical Model mạnh ở: part-search 120M+ vendor parts, tính toán có cite (96% accuracy), standards Q&A, DFM, material selection. Leo KHÔNG sinh CAD tham số production (chỉ mesh).

Hiện trạng KN-Stack: `leo-assist` + `leo-prompt` chỉ sinh prompt để CEO dán tay — vòng lặp hở (kết quả Leo không quay về hệ thống có kiểm soát).

**Mục tiêu:** khép kín vòng prompt → Leo → kết quả → verify → route vào skill nội bộ, với gate bảo mật MẬT cứng, qua một MCP server local.

**Hiện trạng kết nối Leo (đã xác minh 2026-07-04):**
- Leo có trang API chính thức (getleo.ai/api) nhưng business-only, phải request access (hello@getleo.ai), không có docs/pricing công khai, không có MCP chính thức.
- Browser automation = rủi ro cao (Cloudflare, khóa account) — KHÔNG dùng.
- Quyết định: **semi-auto clipboard bridge ngay bây giờ, transport tách riêng để cắm API sau** (hybrid-ready). CEO có account thường, sẽ gửi form xin API access.

## 2. Quyết định thiết kế đã chốt (CEO, 2026-07-04)

| Quyết định | Lựa chọn |
|---|---|
| Kênh kết nối | Semi-auto clipboard bridge, hybrid-ready (API transport stub) |
| Năng lực khai thác | Full 6 modes A–F của leo-assist (part search, Q&A, calc, DFM, docs, material) |
| Hình thức | MCP server (Python + FastMCP, stdio, local) + skill wrapper mỏng |
| Gate MẬT | Hard block + auto-abstract, KHÔNG có override gửi nguyên bản |
| Return path | Clipboard 2 chiều (send copy prompt, ingest đọc kết quả từ clipboard) |
| Output | Propose-only — `ingest` đề xuất đích, `route` chỉ ghi khi CEO ra lệnh |
| API request | Soạn draft email xin API access (deliverable của dự án) |

## 3. Kiến trúc

```
CEO/Claude (bất kỳ skill HELIX/FORGE nào)
   │
   ▼
[MCP: leo-bridge]  (Python + FastMCP, stdio, 100% local)
   ├── leo_classify      Gate MẬT — Computational Sensor, hard-block + auto-abstract
   ├── leo_prompt_build  Sinh prompt Mode A–F từ template leo-assist (ép 5 nguyên tắc)
   ├── leo_send          Gate lần 2 → copy clipboard → ghi ledger (exchange ID)
   ├── leo_ingest        Đọc clipboard kết quả → parse structured → checklist cite-verify
   ├── leo_route         Sau khi CEO duyệt: ghi vào đích đã đề xuất
   └── leo_ledger        Traceability: list/status mọi exchange
   │
   ▼ Transport layer (transports/)
   ├── ClipboardTransport  — bây giờ (pyperclip / PowerShell fallback)
   └── ApiTransport        — stub, cắm API key khi Leo cấp
```

Vòng chuẩn: skill nội bộ cần Leo → `classify` → `prompt_build` → `send` → CEO dán vào app.getleo.ai → copy kết quả → `ingest` → CEO verify cite → `route` vào skill tiêu thụ.

## 4. Đặc tả từng tool

### 4.1 `leo_classify(task_text) → {verdict, hits, abstracted_prompt?}`
- Deterministic denylist (KHÔNG dựa LLM): `denylist.yaml` gồm (a) tên khí tài/mã dự án portfolio (VN-*, V-SMASH, Verdict, Bastion, Sentinel, Scout, Nexus, Axis, UUV, GIÁ TRƯỢT, BB-01, THANH TRI, TLS…), (b) từ khóa defense VN+EN (khí tài, ngư lôi, torpedo, radar target, FCS, fire control, BQP…), (c) pattern mã bản vẽ/PBS nội bộ.
- Verdict `MAT` → trả về lý do (hits) + bản prompt **trừu tượng hóa** (thay tên khí tài bằng mô tả chức năng generic + thông số) để CEO duyệt.
- Verdict `THUONG` → pass.
- CEO bổ sung denylist được; file nằm cạnh server, có comment hướng dẫn.

### 4.2 `leo_prompt_build(mode, phase?, params) → {prompt, assumptions[]}`
- Mode A–F đọc template từ `skills/helix/leo-assist/references/leo-mode-templates.md` (single source of truth — KHÔNG copy template vào server; parse tại runtime).
- Ép 5 nguyên tắc leo-assist: (1) load case định lượng + FoS, (2) kích thước interface thật, (3) process chế tạo, (4) bắt buộc cite, (5) search-before-generate. Thiếu param bắt buộc → trả lỗi liệt kê thiếu gì, không sinh prompt mơ hồ.
- Kèm dòng Phân loại + danh sách GIẢ ĐỊNH cuối prompt.

### 4.3 `leo_send(prompt, mode, exchange_note?) → {exchange_id, instructions}`
- **Chạy lại gate** trên prompt cuối (defense-in-depth — chặn prompt viết tay lách classify). MẬT → từ chối, trỏ về `leo_classify`.
- Copy prompt vào clipboard, tạo `exchange_id` (`LEO-YYYYMMDD-NNN`), append ledger (JSONL: id, timestamp, mode, classification, prompt, status=SENT).
- Trả hướng dẫn: "Dán vào app.getleo.ai → copy toàn bộ kết quả → gọi leo_ingest".

### 4.4 `leo_ingest(exchange_id?) → {parsed, verify_checklist, proposed_routes}`
- Đọc clipboard; nếu rỗng hoặc không giống kết quả Leo (heuristic độ dài + cấu trúc) → lỗi rõ ràng, không đoán.
- Parse theo mode của exchange:
  - **A:** part rows {name, vendor, part_number, specs, source_cite} → đề xuất đích `parts_master` CSV / BOM mua ngoài (forge-fabrication).
  - **B/C:** {công thức, inputs, kết quả, sources[]} → mỗi số liệu 1 dòng checklist "đã mở nguồn xác minh?" — mặc định `UNVERIFIED`.
  - **D/F:** flags/bảng so sánh có cite.
- Kết quả không có cite → flag đỏ "Leo không cite — không dùng cho quyết định chịu lực".
- Cập nhật ledger status=INGESTED, lưu raw + parsed.
- **Propose-only:** chỉ đề xuất đích, không ghi.

### 4.5 `leo_route(exchange_id, target, confirm) → {written}`
- Chỉ chạy khi CEO ra lệnh rõ (confirm=true từ hội thoại).
- Từ chối ghi số liệu còn `UNVERIFIED` vào BOM/bản vẽ; đích journal/ghi chú thì cho phép kèm nhãn UNVERIFIED.
- Targets v1: append `parts_master` CSV (đường dẫn do CEO cấp), design journal file, calc-sheet markdown. Ledger status=ROUTED.

### 4.6 `leo_ledger(action, filter?) → …`
- `list` / `show <id>` / `pending` (SENT chưa ingest, INGESTED chưa verify). Ledger = JSONL tại `mcp/leo-bridge/ledger/` (gitignored).

## 5. Skill wrapper + tích hợp

- `skills/helix/leo-bridge/SKILL.md`: orchestrate vòng khép kín; route Phase×Mode theo bảng leo-assist; nhắc verify checklist; naming/frontmatter chuẩn KN-Stack.
- Cập nhật `leo-assist` SKILL.md: thêm mục "Programmatic path" trỏ sang leo-bridge (leo-assist vẫn là source of truth cho template + doctrine).
- Đăng ký `.mcp.json` (project scope): stdio, `python mcp/leo-bridge/server.py`.

## 6. Deliverables

| # | Deliverable | Vị trí |
|---|---|---|
| 1 | MCP server | `mcp/leo-bridge/` (server.py, gate.py, denylist.yaml, transports/, parsers/, ledger/) |
| 2 | Skill wrapper | `skills/helix/leo-bridge/SKILL.md` + cập nhật leo-assist |
| 3 | Đăng ký MCP | `.mcp.json` |
| 4 | Email xin API | `mcp/leo-bridge/docs/api-access-request-draft.md` — tiếng Anh, danh nghĩa công ty kỹ thuật VN, use-case "internal engineering workflow integration", KHÔNG nhắc defense |
| 5 | Tests | pytest: gate (denylist cases VN+EN), parsers, ledger, prompt_build validation; clipboard mocked |
| 6 | Eval | `evals/leo-bridge.json` (static mode) |
| 7 | Housekeeping | VERSION bump + CHANGELOG entry |

## 7. Error handling & ràng buộc

- Clipboard rỗng / nội dung không hợp lệ → lỗi tường minh, hướng dẫn thao tác lại.
- Template leo-assist đổi format → parser template phải fail loudly (không sinh prompt sai).
- Không network call nào từ server (100% local) — transport API chỉ kích hoạt khi có key trong env.
- Python 3.10+, deps: fastmcp (mcp SDK), pyperclip, pyyaml. Windows-first (PowerShell clipboard fallback).
- Git: branch `feature/helix-leo-bridge`, commit format `[HELIX] …`, không đụng main.

## 8. Ngoài phạm vi (v1)

- Browser automation app.getleo.ai — loại bỏ (rủi ro ToS/Cloudflare).
- ApiTransport hoạt động thật — chỉ stub interface; implement khi Leo cấp access.
- Auto-verify cite (mở URL nguồn tự động) — v2; v1 checklist thủ công có cấu trúc.
- Upload file CAD/hình học lên Leo — cấm theo doctrine MẬT; ngoài phạm vi vĩnh viễn cho khí tài.
