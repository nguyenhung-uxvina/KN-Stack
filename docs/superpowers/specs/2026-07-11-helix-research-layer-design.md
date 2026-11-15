# Design Spec — HELIX Research Layer + Topic Notebooks + Harness Upgrade

> Ngày: 2026-07-11 · Nhánh: `feature/helix-research-layer` · Trạng thái: CEO đã duyệt hướng thiết kế (Hướng 1)
> Phạm vi session: thiết kế đầy đủ 4 track, triển khai phần lõi (Track A + B + D); Track C là đề xuất trong doc này.

## 1. Bối cảnh — 3 phát hiện từ khảo sát

1. **HELIX không có dây nối nghiên cứu.** Pipeline nhận diện đúng các điểm cần nghiên cứu (M1-Literature ở `helix-p2-search`, method L/E ở `helix-p2-firmup`, TESE ở `helix-p2-frame`, standards scan ở `helix-p1-preflight`, ICDM Knowledge Gap ở `helix-p2-risk`) nhưng xử lý bằng trí nhớ model + vault nội bộ + CEO tự làm. Zero tham chiếu tới `/research`, mentor-board, NotebookLM MCP trong toàn bộ 57 skill HELIX — trong khi hạ tầng executor đã tồn tại đủ.
2. **NotebookLM bị dùng như chú thích chết.** ID notebook VDI 2221/2206/ICDM đã ghi trong SKILL.md nhưng không bao giờ được query lúc chạy. Chưa có khái niệm "topic notebook" (notebook thường trực theo chủ đề, khác mentor notebook theo người). 3 registry hiện rời rạc (research alias table · mentor `_registry.md` · book manifest).
3. **Harness engineering mới thẩm thấu 1 cụm.** `helix-cad-validate` (validate.py: exit-code, hash-lock, provenance) là Gate tất định duy nhất. `aigate`/`qc`/`helix-quality-gate` mang danh Gate nhưng là checklist LLM tự chấm. Lỗi cụ thể: `evals/helix-cad-validate.json` đã chuyển sang format `checks` nhưng `run-eval.sh` chỉ đọc `assertions`+regex → eval không chạy được. Ba pha Chế tạo/Thử nghiệm/Firmware chưa có Gate.

## 2. Quyết định CEO (2026-07-11)

| Quyết định | Lựa chọn |
|---|---|
| Phạm vi | Thiết kế đủ 4 track + triển khai lõi (helix-research, topic-notebook, wiring, runner fix, HARNESS_STANDARD) |
| Topic notebook | Cả 4: `std` (ưu tiên, build mới) · `vdi` (đăng ký sẵn có) · `harness` (đăng ký sẵn có) · per-project (nối helix-project-init) |
| Executor mặc định | Router 3 tầng theo độ khó, CEO duyệt theo COD |
| Harness | Vá runner static/checks + HARNESS_STANDARD.md + eval cho skill mới; KHÔNG script-hóa aigate/qc đợt này |
| Kiến trúc | Hướng 1 "Dispatcher mỏng + Registry" — 2 skill mới, HELIX hiện có chỉ nhận Research Hook ngắn |

## 3. Track A — Skill `helix-research` (mới)

**Vị trí:** `skills/helix/helix-research/SKILL.md` (method-skill cross-phase, cùng hạng `helix-domain-debate`).
**Vai trò:** Dispatcher nghiên cứu duy nhất cho toàn pipeline HELIX. Mọi block cần tri thức ngoài đều gửi Research Brief về đây — không block nào tự chọn executor.

### 3.1 Research Brief (input chuẩn hóa)

```yaml
brief_id: RB-<project>-<seq>        # ví dụ RB-VNTGTF-003
question: <câu hỏi nghiên cứu cụ thể>
type: standards | prior-art | working-principle | state-of-the-art | knowledge-gap | market
phase: P0 | P1 | P2 | P3 | P4
source_block: <skill sinh brief, ví dụ helix-p2-firmup>
risk_if_wrong: LOW | MEDIUM | HIGH    # sai thì hậu quả gì — HIGH ép tier nguồn S/A
known_sources: [<alias topic-notebook nếu có>]
deadline: <nếu có>
```

### 3.2 Router 3 tầng

| Tầng | Executor | Điều kiện chọn | COD |
|---|---|---|---|
| **T1 LOOKUP** | `mcp__notebooklm-mcp__notebook_query` vào topic-notebook (theo `known_sources` hoặc match type→alias) hoặc mentor NLM | Câu hỏi tra cứu, nguồn đã có trong notebook đăng ký | Offload — auto-OK, báo lại kết quả |
| **T2 SPRINT** | `/research` v4.1 (multi-channel + source tiers + NLM ingest) | Cần nguồn MỚI có kiểm soát tier; type=prior-art/standards chưa có notebook | Offload — CEO confirm trước khi chạy |
| **T3 DEEP** | `nlm` Mode 8 (NLM Deep Research native, chạy nền, token free) hoặc plugin `deep-research` (fan-out + adversarial verify, nhanh, tốn token) | Vấn đề mở/đa chiều/chưa rõ nguồn; type=knowledge-gap, state-of-the-art | CEO confirm + chọn engine |

Quy tắc router (AI đề xuất tầng + lý do, CEO duyệt trừ T1):
- `risk_if_wrong: HIGH` → kết quả bắt buộc có nguồn tier S/A; T1 chỉ được dùng nếu notebook nguồn là S/A; nếu không → nâng T2.
- T1 trả "nguồn không đủ" → tự đề xuất nâng T2 (không im lặng trả lời từ trí nhớ model).
- SF màu RED / tranh luận đa domain → route sang `mentor-board` PANEL/DEBATE thay vì search (tri thức phán đoán ≠ tri thức tra cứu).

### 3.3 Research Response (output chuẩn hóa)

File `Research_Response_<brief_id>.md` ghi vào thư mục dự án (cạnh `_pipeline_state.md`), gồm:
- Trả lời trực tiếp câu hỏi + **trích dẫn từng claim** (nguồn + tier S/A/B/C)
- `confidence: HIGH/MEDIUM/LOW` + tier tổng hợp
- **"KHÔNG tìm thấy"**: liệt kê phần câu hỏi chưa trả lời được (fail-safe — cấm lấp bằng suy đoán không nguồn)
- Đề xuất bước tiếp (nâng tầng? thêm nguồn vào notebook? hỏi mentor?)
- Tùy chọn: ingest response vào project notebook (nếu có).

Block gọi ghi tóm tắt 1 dòng + link Response vào `_pipeline_state.md` (đúng Block Ledger protocol).

### 3.4 Điểm nối dây — 6 file HELIX hiện có (mỗi file thêm mục "Research Hook" ~10-15 dòng)

| # | File | Hook |
|---|---|---|
| 1 | `skills/helix/helix-p2-firmup/SKILL.md` | Task brief L (Literature/patent) và E (External/market) khi CEO phân Offload → chuyển thành Research Brief, gọi `/helix-research`. Đây là executor thật cho task brief vốn "rỗng". |
| 2 | `skills/helix/helix-p1-preflight/SKILL.md` | Standards scan: query T1 notebook `std` TRƯỚC, trình CEO danh sách chuẩn tìm được + phần thiếu; CEO chỉ bù phần thiếu (giảm Core load). |
| 3 | `skills/helix/helix-p1-requirements/SKILL.md` | A2 (standards) + A3 (similar products): sau forge-library, thêm T1 lookup `std`/project notebook; requirement sinh từ lookup phải mang citation. |
| 4 | `skills/helix/helix-p2-frame/SKILL.md` | TESE stalled-trend: khi trend chấm ≤2/5 hoặc CEO nghi model lỗi thời → Research Brief type=state-of-the-art (T2/T3). |
| 5 | `skills/helix/helix-p2-risk/SKILL.md` | ICDM RTA (BD-3): mỗi knowledge gap NEW → 1 Research Brief type=knowledge-gap, vào gap-closing plan. |
| 6 | `skills/helix/helix-domain-debate/SKILL.md` | SF RED hoặc 3 góc nhìn mô phỏng bất đồng không giải được → escalate option: `mentor-board` PANEL với council chuyên ngành (naval-architect, nswc-hull, torpedo-asw, harness-engineering…). KB tĩnh giữ nguyên làm tầng 0. |

Ngoài ra 2 orchestrator (`helix-task-clarify`, `helix-concept-generate`) thêm 1 câu ở Step 1.5 (Context Enrichment): liệt kê topic-notebook đã pin trong charter và nhắc block có thể gửi Research Brief.

**Ràng buộc:** Hook là *đề xuất route*, không đổi thứ tự block, không thêm block mới vào pipeline 6-block, không phá quy tắc ONE BLOCK PER TURN.

## 4. Track B — Skill `topic-notebook` (mới)

**Vị trí:** `skills/galaxy/topic-notebook/SKILL.md` (+ `references/registry-schema.md`, `references/reference-persona.md`).
**Vai trò:** Vòng đời notebook chủ đề thường trực — khác mentor (persona người, nguồn tĩnh theo tác giả) và khác research-sprint (one-off).

### 4.1 Modes

| Mode | Hành vi |
|---|---|
| `--register <alias> <nlm-id>` | Đăng ký notebook CÓ SẴN vào registry (scope, source count, persona hiện tại, ghi chú chia sẻ với mentor nếu có). |
| `--add <topic>` | Build mới: soạn seed-sources phân tier S/A/B/C (tái dùng `research/references/source-tiers.md`) → **CEO duyệt nguồn (Core)** → `notebook_create` + `source_add` (retry 3 tầng như mentor A4) → `chat_configure` reference-persona → đăng ký registry + `nlm alias set`. |
| `--query <alias> "<q>"` | Lookup protocol nhẹ: citation-first, trả nguyên văn trích dẫn + source id; nói rõ khi nguồn không đủ. (Khác 5-frame DMIR của mentor.) |
| `--refresh <alias>` | Incremental: đề xuất nguồn mới (tái dùng research `--update` + mentor `--check-new`), CEO duyệt, ingest, bump registry. |
| `--list` / `--health` | Bảng registry + cảnh báo stale >90 ngày hoặc >45 sources (đề xuất facet split theo `facet-split-strategies.md`). |

### 4.2 Registry thống nhất

`D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (append-only, state ở vault — protocol ở repo, giống mentor-board). Mỗi entry: alias · NLM ID · URL · scope 1 dòng · source count + tier mix · persona mode · shared-with (mentor nào nếu dùng chung) · created/last-refresh · pinned-projects.

### 4.3 Reference-persona (khác persona-purity của mentor)

"Chuyên gia miền trung lập của Workshop X. Chỉ trả lời từ nguồn trong notebook, mỗi claim kèm trích dẫn nguồn. Khi nguồn không đủ: nói rõ 'nguồn hiện có không trả lời được X', tuyệt đối không suy đoán. Ưu tiên số liệu, điều khoản chuẩn, đơn vị metric."

### 4.4 Seeding đợt này

| Alias | Cách | Ghi chú |
|---|---|---|
| `vdi-2221`, `vdi-2206` | `--register` (ID sẵn: `f6e2b21f`, `3856a428`) | Zero effort; HELIX orchestrator đổi "chú thích chết" thành alias query được |
| `harness` | `--register` (ID `8c7dab78`) | Dùng chung notebook mentor-harness-engineering-council; registry ghi `persona: mentor-mode (shared)` — không đổi persona để giữ purity |
| `std` | `--add` | Tôi soạn DRAFT seed-sources (MIL-STD-810H, MIL-STD-461G, MIL-STD-1472, MIL-STD-882E, STANAG public, TCVN quốc phòng liên quan, ISO 128/2768) → CEO duyệt nguồn → build. Nếu CEO chưa kịp duyệt trong session: dừng ở draft, ghi vào roadmap. |
| per-project | Sửa `helix-project-init` | Thêm step tùy chọn "tạo project notebook + pin alias vào charter"; `known_sources` của Research Brief đọc từ charter. |

## 5. Track C — Đề xuất công cụ tham khảo (không code đợt này)

| Công cụ | Dùng cho | Khuyến nghị | Trigger thêm |
|---|---|---|---|
| Exa semantic search | Channel 0 của `/research` | ĐÃ CÓ — giữ | — |
| ASSIST Quick Search (assist.dla.mil) | Tra MIL-STD chính bản + trạng thái hiệu lực | **Thêm vào seed-sources `std` + ghi vào Research Hook standards** (WebFetch, free) | Ngay đợt này (dạng nguồn, không phải tích hợp) |
| Espacenet + Google Patents | M1-Literature / prior-art / FTO | Ghi thành phương án chuẩn trong T2 cho type=prior-art (WebFetch/WebSearch, free) | Khi có ≥3 brief prior-art/tháng thì cân nhắc API |
| Semantic Scholar API | Literature học thuật có citation graph | Roadmap — chỉ khi T2 chứng minh thiếu học thuật | Trigger: 2 brief liên tiếp fail vì thiếu paper |
| ScrapeCreators (last30days) | Social signal cho type=market | Tùy CEO — phục vụ FORGE nhiều hơn HELIX | Khi forge-pulse cần Reddit/TikTok |
| Deep-research harness nội bộ (fan-out tự host) | Thay plugin ngoài | **HOÃN theo trigger** (đúng doctrine Assay) | 2 executor T3 hiện có fail lặp lại |

## 6. Track D — Harness upgrade

### 6.1 Vá `evals/run-eval.sh` — hỗ trợ `mode: static` + format `checks`

- Spec có `checks[]` (id/desc/assert): check nào có thêm `regex` → chấm tất định trên nội dung SKILL.md (+ file phụ khai trong `files[]`); check chỉ có `assert` chữ → chấm bằng LLM-judge (`claude -p` trả JSON `{id, verdict, reason}` từng check).
- Backward-compatible: spec `assertions[]` cũ chạy như hiện tại. Không sửa `evals/helix-cad-validate.json` (thuộc nhánh Assay đang dở) — chỉ làm runner ĐỌC ĐƯỢC format đó.
- Kết quả: đóng lỗi "eval static không chạy được"; nhánh đích `feature/evals-static-mode` là nơi hợp lý để PR.

### 6.2 `docs/HARNESS_STANDARD.md` — chuẩn Guides–Sensors–Gates toàn workflow

Nội dung:
1. **Vocabulary bắt buộc** (theo KHUNG HARNESS ENGINEERING v1.0): Guides (feedforward) / Sensors (feedback) / Gates (cưỡng chế); Computational vs Inferential; "cơ chế không phải prompt"; Improvement Engine; fail-safe.
2. **Khai báo class trong frontmatter skill mới**: `harness_class: guide | sensor-computational | sensor-inferential | gate`. Quy tắc đặt nhãn: **cấm** dùng chữ "Gate/BLOCK/halt" trong skill nếu không có cơ chế cưỡng chế thật (exit-code, hash-lock, hook chặn) — phải gọi là "checklist/review (Inferential, propose-only)".
3. **Eval bắt buộc** cho orchestrator/mega-skill/gate mới (mode static nếu không chạy 1-shot được).
4. **Improvement Engine loop**: finding Inferential lặp lại + xác nhận → nâng thành luật Computational (mẫu: design-review → design_rules.json).
5. **Bảng phân loại hiện trạng** (từ audit này): validate.py = gate thật; aigate/qc/quality-gate = sensor-inferential mang nhãn sai; hooks = sensor đo lường soft.
6. **Roadmap Gates còn thiếu**: Chế tạo (AI-QC hàn/NDT), Thử nghiệm (eval coupon), Firmware (CI gate cấm auto-merge mã AI vào firmware tới hạn), earned-autonomy gate — mỗi cái kèm trigger dựng.

### 6.3 Eval mới

`evals/helix-research.json` + `evals/topic-notebook.json` — mode static, format `checks` (dogfood chính runner mới): kiểm frontmatter, router 3 tầng đủ, COD rule, fail-safe "không tìm thấy", citation bắt buộc, registry protocol, không vi phạm AI Permissions (propose-only với vault).

## 7. Ràng buộc & không đụng vào

- **Không sửa** các file working-tree của nhánh Assay: `skills/helix/helix-cad-validate/*`, `evals/helix-cad-validate.json`, `skills/mentors/mentor-chris-brose/SKILL.md`, `CHANGELOG.md`/`VERSION` phần đã sửa dở, `evals/fixtures/`, `temp/`.
- Nhánh làm việc: `feature/helix-research-layer` (từ HEAD `feature/leo-ai-plugin`); chỉ stage file thuộc scope này.
- AI Permissions vault giữ nguyên: registry ở vault là append/update theo protocol; Galaxy notes vẫn propose-only.
- HELIX hooks không đổi thứ tự block, không phá ONE BLOCK PER TURN, mọi quyết định Core (chọn nguồn, duyệt T2/T3) vẫn của CEO.
- `VERSION` bump + `CHANGELOG.md` entry khi hoàn thành (theo quy ước repo) — thực hiện lúc commit cuối để tránh giẫm phần Assay đang sửa dở trong 2 file này.

## 8. Definition of Done (phần lõi đợt này)

1. `skills/helix/helix-research/SKILL.md` tồn tại, frontmatter đúng chuẩn, router 3 tầng + Brief/Response schema đầy đủ.
2. `skills/galaxy/topic-notebook/SKILL.md` + 2 references tồn tại; registry khởi tạo tại vault với ≥3 entry (`vdi-2221`, `vdi-2206`, `harness`); draft seed-sources `std` sẵn sàng cho CEO duyệt.
3. 6 file HELIX + 2 orchestrator + `helix-project-init` có Research Hook/pin-notebook (diff mỗi file nhỏ, không đổi cấu trúc block).
4. `run-eval.sh` chạy được spec `mode: static` + `checks` (kiểm bằng eval mới); spec `assertions` cũ vẫn pass.
5. `docs/HARNESS_STANDARD.md` tồn tại với 6 mục ở §6.2.
6. 2 eval mới pass; `bash setup.sh --verify` không vỡ junction.
7. VERSION bump + CHANGELOG entry; PR về `feature/evals-static-mode`.

## 9. Roadmap (hoãn có chủ đích, kèm trigger)

| Hạng mục | Trigger dựng |
|---|---|
| Build notebook `std` (nếu chưa duyệt nguồn kịp) | CEO duyệt draft seed-sources |
| Script-hóa helix-quality-gate P02 / aigate | Sau khi HARNESS_STANDARD áp 1 quý, chọn gate có tần suất dùng cao nhất |
| Gates Chế tạo/Thử nghiệm/Firmware | Theo bảng trigger trong HARNESS_STANDARD §6 |
| Deep-research harness nội bộ | T3 executor hiện có fail lặp lại (≥3 lần) |
| Semantic Scholar API | 2 brief liên tiếp thiếu nguồn học thuật |
| Facet split cho notebook `std` | >45 sources |
