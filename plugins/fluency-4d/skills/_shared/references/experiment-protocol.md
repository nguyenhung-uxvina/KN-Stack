# Giao thức thí nghiệm hành vi

## Luật

1. **WIP = 1.** Chỉ một thí nghiệm `OPEN` tại một thời điểm. Phát hiện 5 điểm yếu vẫn chỉ kê 1. Ràng buộc cứng, không phải gợi ý.
2. **Dạng nếu–thì.** Câu phải bắt đầu bằng "Khi " và chứa " tôi ", mô tả hành vi quan sát được. Cấm viết kiểu "chú ý Description hơn".
3. **Cách đo.** Mỗi phiên sau ghi `exp_held: true/false` vào sổ.
4. **Nghiệm thu.** Giữ 3 phiên liên tiếp → `PASSED`, đóng, mở thí nghiệm mới.
5. **Đứt.** Streak về 0, số lần đứt +1. Đứt lần thứ 3 → `FAILED`.
6. **Sau `FAILED`.** Kê thí nghiệm NHỎ HƠN nhắm cùng ô. Cấm chép lại nguyên văn câu cũ.

## Bảng `experiments.md`

| ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng |
|---|---|---|---|---|---|---|---|
| `EXP-001` | `des.product` | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi. | 3 | 0 | PASSED | 2026-08-01 | 2026-08-05 |
| `EXP-002` | `dis.product` | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng. | 1 | 0 | OPEN | 2026-08-06 |  |

## Ví dụ tốt và xấu

| Xấu | Tốt |
|---|---|
| Chú ý Description hơn | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi |
| Kiểm chứng kỹ hơn | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng |
| Delegation tốt hơn | Khi mở phiên, tôi nói rõ task này là Core hay Offload trước câu hỏi đầu tiên |
