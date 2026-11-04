# judge_questions — luật soạn câu hỏi kiểm ý đồ

Nguồn: CADCodeVerify (Alrashedy et al., arXiv 2410.05340) — Fig. 11 (sinh câu hỏi), Fig. 13 (trả lời), Bảng 9
(độ đúng câu trả lời 64,6 % / 68,2 %; "Unclear" 26,6 % / 19,3 %). Bài báo để chính mô hình tự sinh câu hỏi mỗi
lượt; ở Xưởng câu hỏi được **soạn một lần, kỹ sư sửa + ký**, nằm trong `geometry_contract.json` ⇒ khoá bằng
`--approved-hash` cùng hợp đồng hình học. Lý do: agent tự đặt câu hỏi thì tự chọn được câu dễ.

## Ai làm gì
| Việc | COD |
|---|---|
| Nháp câu hỏi từ `spec.md` theo luật dưới (agent, KHÁC agent dựng) | O |
| Sửa, xoá, thêm, gán `severity`, ký hợp đồng | **C** (kỹ sư) |

## Khuôn
```json
"judge_questions": [
  {"id": "Q1", "q": "Lỗ ở đầu +X có tiết diện TRÒN (không vuông, không lục giác)?",
   "spec_line": "Lỗ thông Ø10 cách đầu +X 30 mm", "severity": "block"},
  {"id": "Q2", "q": "Vát cạnh nằm ở mép NGOÀI của mặt +Z (không ở mép lỗ)?",
   "spec_line": "Vát 1×45° các cạnh ngoài mặt trên", "severity": "comment"}
]
```

## Luật (mỗi câu)
1. **Có/Không, viết sao cho "Không" ⇒ phải sửa mô hình.** (CADCodeVerify Fig. 11.)
2. **Chỉ nhắc thứ có trong spec** — mỗi câu có `spec_line` trích nguyên dòng. Không bịa feature để hỏi.
3. **Hỏi thứ cổng tất định KHÔNG đo được**: loại tiết diện (tròn/vuông), lồi ↔ lõm (+boss / −pocket), thông ↔ kín
   đáy, có/không có feature, cạnh nào được vát/bo, hướng rãnh/côn, đối xứng, gương. **Không hỏi số đo** (Ø, dài,
   hộp bao) — đó là việc của `geom_gates.py`; prompt phản hồi của CADCodeVerify cũng cấm góp ý kích thước.
4. **Hướng phải theo trục** trong `axis_convention` ("đầu +X", "mặt +Z"). Cấm "trái/phải/trên/dưới" trơn —
   CADCodeVerify cấm vì tương đối; ở đây có quy ước trục nên dùng trục thay vì cấm hẳn.
5. **Một ý mỗi câu.** "Lỗ tròn và thông?" ⇒ tách 2 câu.
6. **3–12 câu / chi tiết**; mỗi feature quan trọng ≥ 1 câu. Không đủ ý thì ít câu — đừng độn (Fig. 11: "Do not
   make up questions").
7. `severity: block` khi trả lời "Không" làm chi tiết sai chức năng / lắp ghép; còn lại `comment`.

## Judge trả lời thế nào (luật judge_score.py áp bằng máy)
- Mỗi câu: `yes | no | unclear` + `reasoning` + chứng cứ (`view` ∈ Front/Back/Left/Right/Top/Bottom/Iso
  và/hoặc `code_line` có thật trong `model.py`).
- Thiếu lập luận hoặc thiếu chứng cứ ⇒ **hạ thành `unclear`**. Câu không được trả lời / trả lời trùng ⇒ `unclear`.
- `unclear` bất kỳ ⇒ verdict `needs_human` — kỹ sư tự xem render cho câu đó.
- Phát hiện ngoài các câu đã ký ⇒ `extra_findings[]`, CEO xem, **không** đổi verdict.
