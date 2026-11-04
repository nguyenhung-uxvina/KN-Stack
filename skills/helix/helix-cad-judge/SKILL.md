---
name: helix-cad-judge
description: "Giám khảo Ý ĐỒ cho mô hình CAD do AI dựng, theo kiểu CADCodeVerify — kỹ sư KÝ trước một bộ câu hỏi Có/Không (judge_questions[] nằm trong geometry_contract.json, khoá bằng --approved-hash), một agent MỚI (không phải agent đã dựng) đọc spec + model.py + 7 hình render rồi trả lời từng câu Có / Không / Không rõ kèm lập luận + chứng cứ (view, dòng code), và judge_score.py TẤT ĐỊNH tính verdict pass / comment-only / block / needs_human: câu thiếu chứng cứ bị hạ thành Không rõ, Không rõ chuyển người, phát hiện ngoài câu đã ký không đổi verdict. Bắt lỗi đo đạc bỏ lọt: lỗ vuông thay lỗ tròn, lồi↔lõm, vát sai cạnh, rãnh sai hướng, ảnh gương. LỚP PHỤ: chỉ chạy khi helix-cad-gates verdict PASS với cùng hợp đồng, không lật FAIL thành PASS, không sửa mô hình, không phải chữ ký. Triggers on: 'cad judge', 'intent judge', 'giám khảo ý đồ', 'kiểm ý đồ thiết kế', 'mô hình có đúng ý không', 'so mô hình với spec', 'review render', 'design intent check', 'câu hỏi kiểm', 'verification questions', 'CADCodeVerify'."
allowed-tools: ["Read", "Bash", "Task", "Write"]
---

# helix-cad-judge: Giám khảo ý đồ (lớp phụ sau cổng tất định)

> **Role:** Ứng dụng 9 của [[helix-cad-agents]]. Đứng SAU [[helix-cad-gates]] PASS, TRƯỚC cổng CEO xem render.
> **Nguồn:** CADCodeVerify (arXiv 2410.05340) — câu hỏi Có/Không từ spec, trả lời bằng hình render, "Không rõ"
> khi thiếu thông tin · cadgate (judge đọc code + render bắt `.rect(10,10)` thay lỗ Ø10) · Chen & Cheng 2026 P-C-C
> (LLM không là thẩm quyền).

## Why v2 (2026-11-05)
v1 giao cho agent một prompt mở và để **chính agent viết verdict**. CADCodeVerify đo giám khảo kiểu này:
câu trả lời đúng **64,6 % / 68,2 %**, "Không rõ" **26,6 %** (Bảng 9). Ba hệ quả, mỗi cái thành một cơ chế:
1. Agent tự chọn thứ để kiểm ⇒ chọn được thứ dễ. → **Câu hỏi do kỹ sư ký**, nằm trong hợp đồng có hash.
2. "Không rõ" là kết quả bình thường, không phải lỗi. → **Không rõ ⇒ `needs_human`**, không bao giờ thành pass.
3. LLM khẳng định không bằng chứng. → **`judge_score.py` hạ câu thiếu lập luận/chứng cứ thành Không rõ** và tự
   tính verdict; agent chỉ ghi câu trả lời.

## Luật cứng (cơ chế — chỗ thực thi ghi trong ngoặc)
1. Cổng hình học phải `verdict == "PASS"` **với cùng hợp đồng** (`judge_score.py` từ chối, exit 3, khi verdict ≠ PASS —
   kể cả `DRAFT-PASS` — hoặc khi `contract_sha256` của báo cáo cổng ≠ hash hợp đồng ≠ `--approved-hash`).
2. Hợp đồng phải có `judge_questions[]` 1–12 câu, mỗi câu có `id`, `q`, `spec_line`, `severity` (`judge_score.py`
   từ chối khi thiếu). Luật soạn: `references/question-rules.md`.
3. **Agent giám khảo ≠ agent dựng** — luôn `Task(general-purpose)` MỚI, không truyền lịch sử của agent dựng (orchestrator).
4. Đầu vào CỐ ĐỊNH 4 tệp: `spec.md` · `model.py` · `model_views.png` · `geometry_contract.json` (để đọc câu hỏi).
   Không đọc bản vẽ gốc (judge kiểm mô hình ↔ spec; spec ↔ bản vẽ là việc kỹ sư khi duyệt spec).
5. Agent chỉ ghi `judge_answers.json`. **Verdict do `judge_score.py` ghi** vào `judge_verdict.json/.md`.
6. Verdict `block` / `needs_human` **không** tự gửi sửa: orchestrator đưa CEO; CEO quyết.
7. Phân loại MẬT ⇒ **không chạy judge** (agent là Claude cloud) — chỉ cổng tất định + CEO.

## Workflow
### Step 1: Soạn câu hỏi (O nháp → **C** ký) — một lần mỗi chi tiết, cùng lúc lập geometry_contract
Agent nháp (KHÁC agent dựng) đọc `spec.md` + `references/question-rules.md`, đề xuất `judge_questions[]`.
Kỹ sư sửa, gán `severity`, ký hợp đồng ⇒ sha256 ghi vào `_pipeline_state.md` (cùng hash với [[helix-cad-gates]]).

### Step 2: Điều kiện (O)
`cad_gates_report.json` verdict `PASS` (chạy `--mode release`) · phân loại ≠ MẬT · có `model_views.png`.

### Step 3: Gọi agent giám khảo (O) — prompt dán nguyên văn, thay `<DIR>`
```
Bạn là kỹ sư kiểm tra thiết kế. Chỉ được đọc đúng 4 tệp: <DIR>/spec.md, <DIR>/model.py, <DIR>/model_views.png,
<DIR>/geometry_contract.json. Không đọc tệp nào khác, không sửa tệp nào.
Trong geometry_contract.json có mảng judge_questions — kỹ sư đã ký. Trả lời TỪNG câu, không thêm, không bớt,
không sửa câu hỏi. Ảnh model_views.png gồm 7 hình của CÙNG một vật: Front, Back, Left, Right, Top, Bottom, Iso.
Mỗi câu trả lời là một trong ba: "yes", "no", "unclear". Trả "unclear" khi không nhìn rõ hoặc không đủ thông tin —
đừng đoán. Mỗi câu phải có "reasoning" và chứng cứ: "view" (tên hình ở trên) và/hoặc "code_line" (số dòng trong
model.py). Thiếu chứng cứ thì câu đó bị tính là "unclear".
Không đánh giá kích thước bằng số (cổng tất định đã đo). Không đề xuất chỉnh kích thước cho khớp khối lượng.
Nếu thấy sai khác KHÔNG nằm trong câu hỏi nào, ghi vào extra_findings.
Ghi <DIR>/judge_answers.json:
{"answers":[{"id":"Q1","answer":"yes|no|unclear","view":"Front","code_line":12,"reasoning":"..."}],
 "extra_findings":[{"what":"...","view":"Iso","code_line":20,"evidence":"..."}]}
Trả lời ≤ 5 dòng tóm tắt.
```

### Step 4: Chấm tất định (O)
```bash
python judge_score.py --contract geometry_contract.json --gates cad_gates_report.json \
                      --answers judge_answers.json --model model.py --approved-hash <sha256> --out judge_verdict
```
Exit 0 `pass`/`comment-only` · 2 `block` · 5 `needs_human` · 3 từ chối (điều kiện sai) / lỗi IO.

### Step 5: Trình CEO (**C**)
Đưa `judge_verdict.md`: bảng câu hỏi · trả lời · chứng cứ · câu bị hạ. CEO chọn:
(1) Approve · (2) Re-run khối dựng kèm các câu ❌ · (3) Kỹ sư xem tay các câu ❓ · (4) Stop · (5) Skip judge (ghi lý do).

## Gotchas
- Judge **vẫn có thể sai** khi có chứng cứ: chứng cứ chỉ chứng minh agent đã nhìn, không chứng minh nhìn đúng.
- **Đã đo 2026-11-05** (`evals/cad-judge-bench/RESULTS-2026-11-05.md`): 10 ca lỗi cấy, 76/76 câu đúng, 10/10
  verdict, bắt cả 4 lỗi lọt cổng tất định. NHƯNG 80/80 câu dẫn `code_line` — đó là số đo **đọc mã code-CAD sạch**,
  không phải nhìn hình. Mô hình KHÔNG có mã (Fusion MCP, STEP ngoài) ⇒ judge chỉ còn render ⇒ **chưa đo, đừng tin**.
- Cách ly agent là lời nhắc: 1/10 agent đo thử đã chạy python dù prompt cấm.
- Render là ảnh tô bóng đơn giản; chi tiết < 1 mm có thể không thấy — câu về chi tiết nhỏ nên được trả lời bằng `code_line`.
- Đổi câu hỏi = đổi hợp đồng ⇒ hash đổi ⇒ phải chạy lại cổng hình học (đúng ý: cổng và judge dùng chung một hợp đồng).
- `extra_findings` không chặn được gì: muốn chặn thứ gì thì phải có câu hỏi đã ký cho nó.

## Output
`judge_answers.json` (agent) · `judge_verdict.json` + `.md` (`judge_score.py`) — cạnh `model.step`.

## COD
| Task | COD |
|---|---|
| Nháp câu hỏi | O |
| Sửa + ký câu hỏi, gán severity | **C** |
| Gọi judge, chạy judge_score.py | O |
| Quyết khi `block` / xem tay câu `needs_human` | **C** |

## Tests
`python -m pytest scripts/test_helix_cad_judge.py -v` — không cần build123d (chỉ JSON).
