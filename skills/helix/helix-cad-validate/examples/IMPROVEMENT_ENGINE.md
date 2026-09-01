# Improvement Engine — helix-cad-validate regression ledger

> KHUNG v1.0 §4: "Mỗi lỗi → một bản sửa vĩnh viễn." Mỗi bug đã vá PHẢI graduate thành 1 regression
> case trong `corpus.json` để **bất khả lặp lại**. `eval_harness.py` chạy corpus này ở mỗi thay đổi
> `validate.py`/contract; regression tier phải 100% nếu không → thay đổi bị từ chối.

## Quy trình (fix-it-once)
1. Quan sát 1 lỗi (validator chấm sai: false-pos/false-neg, hoặc luật lọt).
2. Vá `validate.py` hoặc thêm/sửa rule trong contract.
3. **Thêm 1 regression case** (extract fixture + expected verdict) khóa đúng hành vi vừa vá.
4. `python eval_harness.py --corpus corpus.json` → regression 100% mới ship.
5. Ghi 1 dòng dưới đây.

## Ledger
| ID | Ngày | Triệu chứng (bug) | Bản vá | Regression case khóa |
|----|------|-------------------|--------|----------------------|
| #M4-001 | 2026-06-27 | Rủi ro: nếu nới `confidence_gate`/`min_confidence`, một độ dày chỉ đọc được ở tầng OCR (LOW) có thể lọt PASS → giá trị an toàn chưa chứng nhận lọt cổng. | Fail-safe đã có trong `validate.py` (LOW < min_confidence → FAIL); NAY khóa bằng eval để không ai regress. | `IE-001-confidence-failsafe` (expect FAIL) |

## Capability → Regression graduation
Khi 1 capability case đạt PASS ổn định qua nhiều checkpoint → đổi `tier` sang `regression` để bảo vệ vĩnh viễn (Anthropic: capability evals "graduate" thành regression suite).
