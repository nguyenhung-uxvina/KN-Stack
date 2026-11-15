# HARNESS_STANDARD — Guides–Sensors–Gates cho KN-Stack

> v1.0 · 2026-07-11 · Áp dụng cho MỌI skill mới; skill cũ refactor dần theo trigger.
> Nguồn doctrine: KHUNG HARNESS ENGINEERING v1.0 (VN-SIM-TECH) + mentor-harness-engineering-council.

## 1. Vocabulary bắt buộc
- **Guide** (feedforward): hướng dẫn nạp trước — SKILL.md, template, contract, AGENTS.md.
- **Sensor** (feedback): chấm sau khi có output. **Computational** = script tất định (regex/schema/exit-code, chạy máy được); **Inferential** = LLM chấm theo rubric (propose-only).
- **Gate** (cưỡng chế): chặn hành động rủi ro bằng CƠ CHẾ — exit-code, hash-lock, hook chặn. "Cơ chế không phải prompt."
- **Improvement Engine**: mỗi lỗi lặp lại được xác nhận → nâng thành luật Computational (fix-it-once).
- **Fail-safe**: thiếu dữ liệu cho check tới hạn → FAIL/NOT FOUND, không bao giờ silent skip.

## 2. Khai báo class (skill mới BẮT BUỘC)
Frontmatter hoặc dòng đầu body: `Harness class: guide | sensor-computational | sensor-inferential | gate`.
**Quy tắc nhãn:** cấm chữ "Gate/BLOCK/halt" nếu không có cơ chế cưỡng chế thật. Checklist LLM = "review (Inferential, propose-only)". Vi phạm nhãn = defect, sửa như bug.

## 3. Eval bắt buộc
Orchestrator / mega-skill / gate mới → PHẢI có `evals/<skill>.json` cùng PR. Mode `static` + `checks` cho skill không chạy 1-shot; check nào regex-hóa được thì regex (Computational), phần còn lại prose assert (LLM-judge).

## 4. Improvement Engine loop
Mẫu chuẩn: `helix-design-review` (Inferential finding) → kỹ sư xác nhận lặp lại → luật mới trong `design_rules.json` (bump version + re-hash) → `helix-cad-validate` hấp thu. Mọi cặp Sensor-Inferential/Gate-Computational mới theo đúng vòng này.

## 5. Phân loại hiện trạng (audit 2026-07-11)
| Thành phần | Nhãn tự xưng | Class thật | Ghi chú |
|---|---|---|---|
| helix-cad-validate (validate.py) | Gate | **gate** (exit 2, hash-lock, provenance) | Mẫu mực duy nhất |
| helix-design-review | propose-only | sensor-inferential | Đúng nhãn |
| aigate (FORGE-F 7-check) | "Gate/BLOCK" | sensor-inferential | Nhãn quá — không cưỡng chế |
| qc (Defense QC 10-check) | "Gate/halt" | sensor-inferential | Check-02 HITL "halt" chỉ là chữ |
| helix-quality-gate | Gate 1-4 | sensor-inferential + HITL Core | A-items chưa script-hóa |
| hooks (3 bash) | — | sensor-computational (soft) | Đo lường, không chặn |
| run-eval.sh + evals/*.json | — | sensor-computational (nông) | regex keyword-level |

## 6. Roadmap Gates còn thiếu (dựng theo TRIGGER, không dựng trước)
| Gate | Pha | Trigger dựng |
|---|---|---|
| Script-hóa helix-quality-gate P02 A-items | Thiết kế | HARNESS_STANDARD áp 1 quý + gate dùng ≥5 lần/quý |
| AI-QC hàn/NDT false-negative sensor | Chế tạo | forge-fabrication chạy sản phẩm hàn nhôm đầu tiên qua F3 |
| Eval coupon (thử nghiệm vật lý) | Thử nghiệm | Bench test campaign đầu tiên có ≥2 vòng lặp |
| CI gate cấm auto-merge mã AI vào firmware tới hạn | Lập trình | Repo firmware đầu tiên có CI |
| Earned-autonomy gate (cấp quyền theo năng lực đã chứng minh) | Toàn hệ | ≥3 gate Computational vận hành ổn định 1 quý |
| Deep-research harness nội bộ | Research | T3 executor fail lặp ≥3 lần trên cùng loại brief |
