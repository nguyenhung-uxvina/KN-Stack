---
name: helix-cad-agents
description: "Orchestrator mỏng cho bộ agent Claude × CAD — menu 10 ứng dụng, mỗi ứng dụng định tuyến sang khối/flow đã có, không tự làm việc của khối: (1) spec → CAD → STEP [helix-spec-to-cad / helix-cad-bridge + helix-cad-gates] · (2) bóc kích thước/vật liệu/BOM từ DXF có nhãn nguồn D/G/T [helix-cad-ingest] · (4) họ biến thể + đổi layer [helix-cad-batch] · (5) cổng hình học tất định F1–F4 [helix-cad-gates] · (9) giám khảo ý đồ [helix-cad-judge] · (10) dựng 3D từ 2D CÓ KIỂM NGƯỢC — bản vẽ là gốc, 4 agent (lập sổ hình chiếu, dựng cách ly với vòng crosscheck bên trong, chẩn đoán, lập phiếu đề xuất sửa 2D) + cổng tất định crosscheck/mutate/audit_claims --profile reconstruct [helix-cad-crosscheck] · đợt 2: (3) dựng NHÁP từ bản vẽ, (6) hàn/lắp ráp nhiều tờ, (7) GD&T, (8) rà trước phát hành. Router phân loại MẬT chặn mọi agent LLM; ledger _pipeline_state.md; MỘT khối mỗi lượt, dừng chờ CEO. Bài học phép đo GIÁ TRƯỢT 2026-11-02 mã hoá thành luật: điểm dò bắt buộc, khối lượng không phải mục tiêu, khai phương pháp chiếu, agent dựng cách ly, giám khảo khác agent dựng. Triggers on: 'cad agents', 'bộ agent CAD', 'claude cad', 'claude với CAD', 'ứng dụng CAD', 'CAD pipeline', 'agent CAD', 'tự động CAD', 'dựng CAD bằng AI', 'AI CAD workflow', 'dựng 3D từ 2D', 'tạo 3D từ bản vẽ', '3D từ 2D có kiểm', 'đề xuất sửa bản vẽ'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Task"]
---

# helix-cad-agents: Bộ định tuyến 10 ứng dụng Claude × CAD

> **Role:** Thin commander. **NEVER does block work itself** — chỉ phân loại, chọn ứng dụng, gọi khối,
> ghi ledger, dừng chờ CEO. Khối thật: [[helix-cad-ingest]] · [[helix-spec-to-cad]] / [[helix-cad-bridge]] ·
> [[helix-cad-gates]] · [[helix-cad-batch]] · [[helix-cad-judge]] · [[helix-cad-roundtrip]] · [[helix-cad-validate]] ·
> [[helix-cad-crosscheck]].
> **Nguồn:** `/research --deep "CAD claude"` 2026-11-02 (`3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_claude-cad-helix-p3p4_2026-11-02.md`)
> + phép đo 5 bản vẽ GIÁ TRƯỢT cùng ngày.

## Ranh giới đã đo (đọc trước khi chọn ứng dụng)
| Khâu | Claude | Bằng chứng |
|---|---|---|
| Spec chữ → CAD | ✅ tin được | spec người viết 1,000 (Reshef/onShape-cad); RealCADBench chạy được 89% |
| Chép kích thước từ PDF/DXF vector | ✅ có điều kiện | LevelPlane F1 0,962 (PDF gốc, tiếng Anh) |
| Đọc bản vẽ chi tiết đơn sạch → 3D | ⚠️ NHÁP | GIÁ TRƯỢT P1–P3 qua cổng; benchmark CAD-CUA chỉ 15% |
| Bản vẽ hàn / lắp ráp | ⚠️ NHÁP + soi kỹ | GIÁ TRƯỢT P4 sai Ø trục (chỉ điểm dò bắt), P5 thiếu 1,5 mm |
| Bố trí không gian, quyết định đạt/không về số | ❌ | [[LLM Spatial Blindness]] · P-C-C: LLM không là thẩm quyền |

## Luật cứng (cơ chế — mỗi luật có chỗ thực thi)
1. **Phân loại trước tiên** (router = [[helix-cad-bridge]] Step 1). **MẬT ⇒ không gọi Task/agent LLM nào**;
   chỉ chạy script cục bộ (ingest, gates, batch, render) + người. Ghi phân loại + người duyệt vào ledger.
2. **Một khối mỗi lượt**, Ledger Read → làm → Ledger Write → **STOP chờ CEO** (mẫu [[helix-spec-to-cad]]).
3. **Mọi STEP do AI dựng phải qua `geom_gates.py`** với `geometry_contract.json` **đã ký + `--approved-hash`**
   trước khi tới judge/CEO. Hợp đồng thiếu `probes[]` cho feature quan trọng ⇒ không ký (đếm feature đã cho qua nhầm).
   Cơ chế: `--mode release` (mặc định) tự FAIL khi thiếu `probes[]` / `--model` / `param_probes[]` / `--approved-hash`
   (trừ `waivers` trong hợp đồng đã ký); `--mode draft` chỉ cho `DRAFT-PASS`, không mở judge/CEO.
4. **Khối lượng khung tên là INFO.** Prompt mọi agent dựng có câu: *"Không được chỉnh kích thước để khớp khối lượng."*
5. **Spec khai `projection_method` + `axis_convention`**; mọi giá trị mang nhãn D/G/T/?; mọi `?` kỹ sư xác nhận.
6. **Agent dựng cách ly**: chỉ được đọc thư mục đầu vào của mình (prompt liệt kê đúng tệp); giám khảo là agent
   KHÁC agent dựng ([[helix-cad-judge]]).
7. **Ảnh bản vẽ cho agent** phải qua `helix-cad-ingest/render_dxf.py` (sửa font TCVN, AIGDT n→Ø).
8. **Mô hình AI dựng từ bản vẽ = DRAFT**, không bao giờ là geometry-of-record khi chưa có chữ ký kỹ sư.
9. **Spec phải sạch trước khi khởi chạy agent dựng**: `helix-cad-validate/audit_claims.py spec --spec spec.md` exit 0.
   Quyết định CEO được VIẾT LẠI thành câu khẳng định trong chính spec (agent cách ly chỉ đọc spec, không đọc
   `_pipeline_state.md`). Đo 2026-11-05: quyết định "không dựng X" chỉ ghi ở sổ ⇒ agent dựng X ⇒ trượt cổng.
10. **Trình CEO bằng bản ghi claim** (`audit_claims.py collect … --profile full`), không bằng tóm tắt tự viết;
    mọi báo cáo khác qua `check-report` (mỗi dòng phát hiện phải trích claim_id có thật).

## Menu ứng dụng
| # | Ứng dụng | Đợt | Chuỗi khối (mỗi mũi tên = một lượt, dừng chờ CEO) |
|---|---|---|---|
| 1 | Spec → CAD → STEP | 1 | `/helix-spec-to-cad` (B0→BE) — BD dựng theo hợp đồng PARAMS/build, BE gọi `helix-cad-gates` sau `validate.py` |
| 2 | Bóc kích thước/vật liệu/BOM | 1 | `helix-cad-ingest/ingest.py --measure-geometry [--config]` → `aggregate.py` → (`authoritative_bom.py`) → CEO chứng thực kích thước tới hạn |
| 4 | Họ biến thể / đổi layer | 1 | điều kiện: mô hình gốc PASS F1–F4 → `helix-cad-batch/batch_sweep.py` → CEO chọn biến thể → cổng đầy đủ cho biến thể phát hành |
| 5 | Cổng hình học | 1 | kỹ sư ký `geometry_contract.json` → `geom_gates.py` → `render_views.py` → CEO xem render + ký |
| 9 | Giám khảo ý đồ | 1 | kỹ sư ký `judge_questions[]` trong hợp đồng → điều kiện: cổng PASS cùng hash, không MẬT → `/helix-cad-judge` (agent mới ghi `judge_answers.json`) → `judge_score.py` tính verdict → CEO quyết khi `block` / xem tay khi `needs_human` |
| 10 | Dựng 3D từ 2D có kiểm ngược | 1 | `references/crosscheck-agents.md`: A1 agent lập `views.json` → kỹ sư duyệt phương nhìn/tỉ lệ → A2 agent dựng cách ly (vòng `crosscheck.py` bên trong: sửa mô hình khi `model`, KHÔNG theo hình bị nghi khi `drawing`) → A3 script `geom_gates` + `crosscheck` + `mutate` + `audit_claims --profile reconstruct` → A4 agent chẩn đoán (khác A2) → A5 agent lập phiếu đề xuất sửa 2D (nếu có) → CEO quyết từng mục → người sửa DXF → lại A3. Mô hình vẫn là NHÁP tới khi kỹ sư ký |
| 3 | Dựng NHÁP từ bản vẽ | 2 | `render_dxf.py` → agent cách ly dựng + `inferred_spec.json` → kỹ sư duyệt spec → cổng 5 → judge 9 |
| 6 | Hàn / lắp ráp nhiều tờ | 2 | như 3, thêm danh sách thành viên + tờ con (`authoritative_bom.py` WELD-ASSY) |
| 7 | GD&T | 2 | `ingest.py` giải mã khung dung sai AIGDT → `gdt[]` (chỉ chép) → kỹ sư đối chiếu từng khung |
| 8 | Rà trước phát hành | 2 | quy tắc số trong `validate.py`; LLM chỉ giải thích; trạng thái NEEDS_EVIDENCE / NEEDS_HUMAN_RELEASE / ABSTAINED |

Ứng dụng 10 thay đường thủ công của 3 cho chi tiết đơn: cùng giao thức cách ly, thêm kiểm ngược về bản vẽ.

**Đợt 2 chưa bật.** Chọn 3/6/7/8 ⇒ trả lời: *"Đợt 2 chờ kết quả nhánh (a) phép đo GIÁ TRƯỢT (spec đã duyệt → so 2 nhánh).
Hiện có thể chạy thủ công theo `references/reconstruct-brief.md` (giao thức cách ly của phép đo), kết quả là NHÁP."*
— không tự làm khi CEO chưa chọn chạy thủ công.

## Orchestrator Workflow
### Step 1: Router (CORE confirm)
Hỏi/đọc: dự án, chi tiết, **phân loại** (MẬT / HẠN-CHẾ / KHÔNG-NHẠY-CẢM — người duyệt), ứng dụng #. Ghi ledger.
### Step 2: Khởi tạo `_pipeline_state.md` (trong thư mục chi tiết)
```markdown
# CAD Agents — {{project}} / {{part_id}}
Phân loại: {{class}} (duyệt: {{ai}}, {{ngày}}) · Ứng dụng: {{#}} · Đợt: {{1|2}}
## Block Progress
| Lượt | Khối | Trạng thái | Sản phẩm | CEO |
## Block Ledger
## Contract
geometry_contract.json sha256: {{chưa ký}} · ký bởi: {{}}
## CEO Decisions
```
### Step 3: Chạy MỘT khối, rồi STOP
```
═══ {{khối}} XONG ═══
Sản phẩm: [tệp] · Cổng: {{PASS/FAIL + số FAIL}} · Phát hiện: [1–3 dòng]
CEO: (1) ✅ Approve → {{khối kế}}  (2) 🔄 Chạy lại (kèm fix_hint)  (3) ⏸️ Dừng  (4) ⏭️ Skip (ghi lý do)
```
⛔ Chờ CEO trả lời. FAIL ở cổng ⇒ đề xuất (2) với `fix_hint` từ báo cáo; một vòng sửa = một lượt.
### Step 4: Hoàn tất
Tóm tắt: STEP + `cad_gates_report` (PASS, hash khớp) + render + judge (nếu có) + **ô ký kỹ sư còn trống** —
PASS ≠ chữ ký.

## Data Bus
| Tệp | Ghi bởi | Đọc bởi |
|---|---|---|
| `_pipeline_state.md` | orchestrator + khối | tất cả |
| `<part>.cad_extract.json` (+`geometry.views`) | ingest | người lập spec / contract |
| `spec.md` (nhãn D/G/T/?) + `geometry_contract.json` | người (AI nháp) | gates, judge, khối dựng |
| `model.py` (PARAMS/build) + `model.step` | bridge / s2c BD / batch | gates, judge |
| `cad_gates_report.json/.md` + `model_views.png` | gates | judge, CEO |
| `judge_answers.json` | judge (agent) | `judge_score.py` |
| `judge_verdict.json/.md` | `judge_score.py` (tất định) | CEO |
| `views.json` (sổ hình chiếu) | A1 agent → kỹ sư duyệt | crosscheck, mutate, A2 |
| `xc.json/.md` + PNG chồng nét · `mut.json` | `crosscheck.py` / `mutate.py` (tất định) | audit_claims, A4, A5 |
| `chan_doan.md` · `de_xuat_sua_ban_ve.md` | A4 / A5 (agent khác A2) | CEO |

## COD
| Task | COD |
|---|---|
| Phân loại, chọn ứng dụng, ký spec/contract, xem render, quyết khi judge block | **C** |
| Duyệt sổ hình chiếu; quyết từng mục đề xuất sửa bản vẽ (ứng dụng 10) | **C** |
| Bóc DXF, dựng theo spec, chạy cổng, render, batch, judge | O |
| Thông báo, định dạng ledger | D |

## Gotchas
- `geom_gates` F4 FAIL "không theo hợp đồng PARAMS/build" ≠ "số cứng": brief cũ không yêu cầu hợp đồng.
- `ingest --measure-geometry` gộp hai hình chiếu đặt sát nhau (< 15 mm) — kiểm số view trước khi dùng.
- Agent dựng tự chấm độ tin cậy (0,6–0,92 ở GIÁ TRƯỢT) **không** thay cổng.
