---
name: helix-cad-judge
description: "Giám khảo Ý ĐỒ cho mô hình CAD do AI dựng — một agent MỚI (không phải agent đã dựng) đọc spec đã duyệt + model.py + 6 hình chiếu render (helix-cad-gates/render_views.py) + báo cáo cổng, trả verdict JSON pass / block / comment-only kèm lý do bám chứng cứ. Bắt lỗi mà đo đạc bỏ lọt: đúng kích thước nhưng sai hình dạng/ý đồ (vd lỗ vuông thay lỗ tròn Ø10, vát sai cạnh, rãnh sai hướng). LỚP PHỤ: chỉ chạy SAU KHI helix-cad-gates PASS, không bao giờ lật FAIL thành PASS, không sửa mô hình, không phải chữ ký. Triggers on: 'cad judge', 'intent judge', 'giám khảo ý đồ', 'kiểm ý đồ thiết kế', 'mô hình có đúng ý không', 'so mô hình với spec', 'review render', 'design intent check'."
allowed-tools: ["Read", "Bash", "Task", "Write"]
---

# helix-cad-judge: Giám khảo ý đồ (lớp phụ sau cổng tất định)

> **Role:** Ứng dụng 9 của [[helix-cad-agents]]. Đứng SAU [[helix-cad-gates]] PASS, TRƯỚC cổng CEO xem render.
> **Nguồn ý tưởng:** cadgate (LLM judge đọc code + render + mô tả cùng lúc bắt `.rect(10,10)` thay lỗ Ø10 mà
> metric + DFM để lọt) · Chen & Cheng 2026 P-C-C (LLM chỉ hỗ trợ, không là thẩm quyền về số).

## Luật cứng (cơ chế, không phải lời nhắc)
1. **Không chạy nếu `cad_gates_report.json` có `verdict != "PASS"`.** Orchestrator kiểm trước khi gọi.
   `DRAFT-PASS` (cổng chạy `--mode draft`, hợp đồng chưa đủ) **≠ PASS** ⇒ không chạy judge.
2. **Agent giám khảo ≠ agent dựng.** Luôn `Task(general-purpose)` MỚI, không truyền lịch sử hội thoại của agent dựng.
3. Đầu vào CỐ ĐỊNH, chỉ 4 tệp: `spec.md` (đã duyệt) · `model.py` · `model_views.png` · `cad_gates_report.json`.
   Không đọc bản vẽ gốc (judge kiểm mô hình ↔ spec; spec ↔ bản vẽ là việc của kỹ sư khi duyệt spec).
4. Không sửa tệp nào ngoài `judge_verdict.json`. Không đề xuất chỉnh kích thước để khớp khối lượng.
5. Verdict `block` **không** tự gửi sửa: orchestrator đưa CEO xem; CEO quyết (Re-run khối dựng / bỏ qua có lý do).
6. Phân loại MẬT ⇒ **không chạy judge** (agent là Claude cloud) — chỉ cổng tất định + CEO.

## Prompt giao cho agent giám khảo (dán nguyên văn, thay `<...>`)
```
Bạn là kỹ sư kiểm tra thiết kế. Nhiệm vụ: so mô hình CAD với SPEC đã duyệt và chỉ ra chỗ hình dạng/ý đồ
không khớp. Chỉ được đọc đúng 4 tệp: <DIR>/spec.md, <DIR>/model.py, <DIR>/model_views.png,
<DIR>/cad_gates_report.json. Không đọc tệp nào khác. Cổng tất định đã PASS — đừng kiểm lại kích thước hộp bao;
hãy tìm thứ con số không bắt được: loại feature sai (vuông/tròn, lồi/lõm, thông/không thông), sai cạnh vát,
sai hướng (gương), feature trong spec mà mô hình thiếu hoặc mô hình có mà spec không có, code đặt feature bằng
toạ độ tuyệt đối thay vì theo tham số.
Với MỖI phát hiện: trích dòng spec liên quan, chỉ dòng code (số dòng), và hình chiếu nào cho thấy nó.
Không có bằng chứng thì không kết luận. Không đề xuất chỉnh kích thước cho khớp khối lượng.
Ghi <DIR>/judge_verdict.json:
{"verdict":"pass|block|comment-only","findings":[{"severity":"block|comment","what":"...",
 "spec_line":"...","code_line":N,"view":"Front|Top|...|Iso","evidence":"..."}],"confidence":0-1}
block = có ít nhất 1 sai khác làm chi tiết không đúng chức năng/lắp ghép. Trả lời ≤ 8 dòng tóm tắt.
```

## Workflow
### Step 1: Điều kiện (Offload)
`cad_gates_report.json.verdict == "PASS"` và phân loại ≠ MẬT; có `model_views.png` (`render_views.py`).
### Step 2: Gọi agent giám khảo (Offload)
`Task(subagent_type="general-purpose", prompt=<prompt trên>)` — một agent mới mỗi chi tiết.
### Step 3: Đọc verdict, trình CEO (CORE)
Bảng: verdict · số phát hiện block/comment · trích dẫn. CEO chọn: (1) Approve · (2) Re-run khối dựng với
findings · (3) Stop · (4) Skip judge (ghi lý do vào `_pipeline_state.md`).

## Gotchas
- Judge **có thể sai** (cũng là LLM): finding không kèm `spec_line` + `code_line` ⇒ coi là comment, không block.
- Render là ảnh tô bóng đơn giản; chi tiết < 1 mm có thể không thấy — judge nên đọc code cho chi tiết nhỏ.

## Output
`judge_verdict.json` cạnh `model.step`.

## COD
| Task | COD |
|---|---|
| Gọi judge, gom verdict | O |
| Quyết định khi `block` | **C** |
