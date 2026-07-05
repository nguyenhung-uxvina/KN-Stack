---
name: helix-design-review
description: "Design-phase Inferential Sensor (LLM-as-Judge có rubric) — BƯỚC 2 của lộ trình validator, bổ trợ [[helix-cad-validate]] (Computational). Chấm những gì LUẬT KHÔNG mã hóa nổi: design-intent smells (đặt tên lệch, BOM-vs-mô-hình lệch, revision mồ côi, code title-block cũ dán nhầm), yếu tố phi cấu trúc cần phán đoán (thủy động khoang phao, khả lắp, DFM ngoài luật cứng), mâu thuẫn chéo tài liệu (note vẽ vs dim vs ICD vs requirements). TUYỆT ĐỐI propose-only: KHÔNG bao giờ là gate cứng, KHÔNG sửa geometry-of-record, KHÔNG lật gate Computational — chỉ xuất findings có severity+confidence+rationale cho KỸ SƯ ĐỊNH DANH định đoạt (accept/reject/defer). Classification-gated: MẬT/HẠN-CHẾ → model LOCAL air-gapped (GPU), không egress cloud. Improvement Engine: finding lặp lại được xác nhận → kỹ sư NÂNG thành luật Computational trong design_rules.json (fix-it-once). Chạy SAU cad-validate PASS, TRƯỚC chữ ký kỹ sư / freeze ICD. Triggers on: 'design review', 'inferential review', 'review thiết kế', 'chấm thiết kế mềm', 'design-intent smell', 'LLM as judge thiết kế', 'rà soát thiết kế', 'con mắt thứ hai', 'review phi cấu trúc', 'second pair of eyes', 'kiểm tra ngữ nghĩa thiết kế', 'rubric review'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# helix-design-review: Inferential Design Reviewer (LLM-as-Judge có Rubric)

> **Role:** Cross-phase **Inferential SENSOR — PROPOSE ONLY** cho pha THIẾT KẾ (P3/P4). Cặp đôi với
> [[helix-cad-validate]]: cái kia là Computational (luật tất định, gate CỨNG); cái này là Inferential
> (phán đoán LLM, KHÔNG BAO GIỜ gate). Chạy SAU `helix-cad-validate` **PASS** và TRƯỚC chữ ký kỹ sư
> định danh / freeze ICD ([[helix-p3-integrate]]) / handoff ([[helix-p4-handoff]]).
> **Backend:** một model suy luận chạy một RUBRIC có phiên bản. MẬT/HẠN-CHẾ → model LOCAL (GPU air-gapped).
> **Interface in:** `cad_extract.json` (+ ICD, requirements, drawing notes) + `review_rubric.md` (Guide).
> **Interface out:** `design_review_findings.json` (+ `.md`) — danh sách finding cho kỹ sư định đoạt.
> **Lineage:** BƯỚC 2 lộ trình validator (harness-engineering DEBATE 2026-06-25, line 43: "chấm yếu tố
> phi cấu trúc → LLM-as-judge có rubric → Inferential (GPU)"); trigger đã tới. [[mentor-harness-engineering-council]]

## Vì sao tồn tại (khe hở helix-cad-validate không lấp được)
`helix-cad-validate` chặn được cái MÃ HÓA ĐƯỢC thành luật nhị phân (vật liệu whitelist, dày ≥ X, có junction
plate). Nó KHÔNG chấm được cái cần đọc-ngữ-cảnh-và-phán-đoán: note vẽ có mâu thuẫn dim không? BOM có khớp
mô hình không? tên chi tiết có nhất quán không? khoang phao này có smell thủy động không? Đó là việc của
Inferential. Theo [[Sensor-Not-Generator Law — AI Review Thắng AI Generate Vì Bất Đối Xứng Mesh]]: đây vẫn
là **AI làm Sensor (soi), không làm Actor (vẽ)** — chỉ khác là sensor mềm, nên KHÔNG được quyền chặn cứng.

## Operational Envelope
| DO | DON'T |
|----|----|
| Xuất finding: dimension · severity · **confidence** · rationale · evidence · disposition | Chặn cứng handoff/freeze (đó là việc của Computational gate) |
| Chấm theo RUBRIC có phiên bản (Guide), không "cảm tính tự do" | LLM-as-judge kiểu vibes, không rubric |
| Ghi rõ LOW-confidence là KHÔNG chắc chắn | Trình LOW-confidence như sự thật |
| MẬT/HẠN-CHẾ → model LOCAL air-gapped | Gọi cloud LLM cho geometry MẬT (egress) |
| Đề xuất NÂNG finding lặp lại → luật Computational | Tự sửa `design_rules.json` / geometry-of-record |
| Cap số vòng (chống doom-loop) | Rà mù vô hạn một finding |

## Guide = review_rubric.md
Rubric có phiên bản, **do kỹ sư định danh sở hữu**, nạp vào context TRƯỚC khi review. Nó định nghĩa các
chiều chấm + thang severity + thang confidence — biến "review" từ cảm tính thành có kỷ luật. Template:
`references/review-rubric.template.md`. Chiều chấm gợi ý (mỗi dự án tùy biến):
`intent_naming` · `bom_model_consistency` · `revision_lineage` · `cross_doc_conflict` · `nonstructural_judgment`
(thủy động/khả lắp/ergonomics) · `dfm_soft` · `completeness` (thiếu GD&T nơi chức năng cần).

## Findings schema (`design_review_findings.json`)
```json
{
  "meta": {"part_id":"…","product":"…","classification":"…","rubric_version":"…","model":"local|cloud","run_ts":"…"},
  "findings": [
    {"dimension":"cross_doc_conflict","severity":"concern","confidence":"MED",
     "finding":"Note ghi 'thép' nhưng meta.material=5083 — mâu thuẫn.",
     "evidence":"process_notes[2] vs meta.material","suggested_disposition":"engineer_review",
     "promote_candidate":true}
  ],
  "summary": {"advisory":N,"concern":N,"blocker_candidate":N}
}
```
Severity: `advisory` (nên xem) · `concern` (nên sửa) · `blocker_candidate` (NÊN thành luật cứng — nhưng
KHÔNG tự chặn; đề xuất kỹ sư nâng vào contract). Disposition do KỸ SƯ điền: accept / reject / defer.

## Workflow

### Step 1: Tiền đề (CORE)
Xác nhận `helix-cad-validate` đã **PASS** (Computational gate MỞ). Nếu Computational còn FAIL → dừng, sửa
cái cứng trước; Inferential không chạy trên thiết kế còn vi phạm luật. Đọc Geometry Classification
([[helix-p1-validate]]): MẬT/HẠN-CHẾ → chọn model LOCAL, assert offline.

### Step 2: Nạp Guide + input (Offload)
Rubric dự án (`review_rubric.md`) + `cad_extract.json` + ICD + requirements + drawing notes. Thiếu rubric →
copy `references/review-rubric.template.md`, kỹ sư điền chiều chấm thật.

### Step 3: Chấm theo rubric (Offload — Inferential)
Với MỖI chiều rubric: model đọc bằng chứng, xuất finding có **confidence bắt buộc**. Quy tắc:
- Không đủ bằng chứng → confidence LOW, KHÔNG bịa.
- Mỗi finding PHẢI trỏ evidence (field/dòng cụ thể), không phán chung chung.
- Không phát hiện gì cho một chiều → ghi rõ "clean", đừng bịa finding cho đủ.

### Step 4: Kỹ sư định đoạt (CORE — không AI)
Kỹ sư đọc `design_review_findings.md`, điền disposition từng finding (accept/reject/defer). **Đây là điểm
quyết**: Inferential đề xuất, con người quyết. PASS Computational + kỹ sư ký = đủ điều kiện freeze/handoff.

### Step 5: Improvement Engine (CORE — fix-it-once)
Finding `promote_candidate:true` được kỹ sư xác nhận đúng & lặp lại → kỹ sư **nâng thành luật Computational**
trong `design_rules.json` (qua [[helix-cad-validate]]), ký lại hash. Theo thời gian, gate tất định HẤP THU
dần cái mà LLM cứ bắt được → giảm phụ thuộc phán đoán mềm. Đây là vòng "sai một lần, chặn mãi".

## Anti-patterns (đừng phạm)
- **Để Inferential chặn cứng.** Nó KHÔNG phải gate. Chặn cứng chỉ có helix-cad-validate.
- **Chạy cloud cho MẬT.** Egress geometry mật ra model ngoài = vi phạm chủ quyền. Local hoặc trừu tượng hóa.
- **Trình LOW-confidence như chắc chắn.** Mất niềm tin kỹ sư = skill chết.
- **Tự sửa contract/geometry.** Chỉ đề xuất; kỹ sư nâng luật, kỹ sư sửa thiết kế.
- **Doom-loop.** Cap vòng review; lặp cùng finding > N → đẩy lên kỹ sư, đừng rà mù.

## Ranh giới với helix-cad-validate
| | helix-cad-validate | helix-design-review |
|---|---|---|
| Loại | Computational | Inferential |
| Backend | stdlib CPU, air-gapped | model suy luận (local cho MẬT) |
| Quyền | **Gate CỨNG** (block freeze/handoff) | **Propose-only** (không block) |
| Chấm | luật nhị phân mã hóa được | phán đoán ngữ cảnh không mã hóa được |
| Chữ ký | PASS ≠ an toàn, chờ kỹ sư ký | finding chờ kỹ sư định đoạt |
| Vòng cải tiến | nơi luật được nâng vào | nơi phát hiện luật cần nâng |
