---
name: fluency-4d-preflight
description: Cổng kiểm trước khi giao một việc lớn cho AI — ép qua cổng Delegation (việc này Core hay Offload, chạy chế độ nào, giữ lại phần nào) và cổng Description (tiêu chí xong, quy trình, vai AI), chặn nếu Core mà định giao trọn, rồi trả về phiếu giao việc đã viết lại. Triggers on "4d preflight", "preflight", "trước khi giao việc", "chuẩn bị giao task", "kiểm trước khi giao", "giao việc này cho AI thế nào".
---

# /fluency-4d-preflight — Cổng trước khi giao việc

**COD:** Core (CEO quyết C/O/D) · Offload (AI viết lại phiếu giao việc)

Đọc: `../_shared/references/rubric-core.md`, `../_shared/references/profile-workshop-x.md`.
Thí nghiệm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\experiments.md`

**Đọc không được thì DỪNG.** Nếu một trong hai file tham chiếu trên không mở được, KHÔNG chạy cổng.
In thẳng file nào thiếu và dừng lại — cổng chạy thiếu profile sẽ trông vẫn đủ bước nhưng đã mất
toàn bộ tín hiệu ngành.

**Không ghi gì vào sổ điểm.** Đây là cổng, không phải phép đo.

## Bước 0 — Nhắc thí nghiệm đang mở

Đọc `experiments.md`, tìm dòng trạng thái `OPEN`. In lại đúng một dòng câu nếu–thì đó để CEO giữ trong đầu suốt phiên sắp tới. Không có dòng `OPEN` → nói "chưa có thí nghiệm nào đang chạy" rồi đi tiếp.

## Cổng 1 — Delegation

Hỏi và chốt, không đoán hộ:

1. **Việc này là Core / Offload / Default?** (COD). Core = phán đoán thiết kế, quyết định gate, chọn phương án, nhập dữ liệu vật lý thật.
2. **Chế độ nào?** `automation` (AI thực thi tác vụ cụ thể) · `augmentation` (cùng nghĩ cùng làm) · `agency` (AI chạy độc lập, CEO định hình tri thức và hành vi).
3. **Giữ lại phần nào cho mình?** Nêu đích danh phần không giao.
4. **Công cụ và model đã đúng tầng chưa?** Tra xem KN-Stack đã có skill sẵn cho việc này chưa — đừng làm tay một việc đã có skill. Model hạng nặng cho kiến trúc, gate review, thiết kế hệ thống; hạng nhẹ cho đọc file, soạn tài liệu, chạy test. Việc cần công cụ ngoài (CAD, ERP, NotebookLM) mà phiên này không có công cụ đó → nói ra trước, đừng giao.

**Nếu CEO phân loại là Core mà vẫn định giao trọn cho AI → chặn.** Nói rõ vì sao đó là Core, đề xuất tách: phần phán đoán giữ lại, phần chuẩn bị dữ liệu giao đi. Chỉ đi tiếp khi CEO hoặc đổi phân loại, hoặc đồng ý tách.

## Cổng 2 — Description

Ba câu, thiếu câu nào thì hỏi:

1. **Sản phẩm** — đầu ra là gì, định dạng nào, ai đọc, tiêu chí "xong" đo được là gì?
2. **Quy trình** — theo khung nào (3-Gate, VDI 2225, ODI, Pahl-Beitz phase nào), hay để AI tự chọn cách?
3. **Vai** — AI phản biện hay thừa hành, gọn hay chi tiết, được phép hỏi lại bao nhiêu?

## Đầu ra — phiếu giao việc

```
## Phiếu giao việc
- Phân loại: <C/O/D> · Chế độ: <mode>
- Giữ lại: <phần CEO tự làm>
- Công cụ/skill: <skill KN-Stack dùng lại hoặc "làm tay vì …">
- Thí nghiệm đang chạy: <câu nếu–thì hoặc "chưa có">

### Prompt đã viết lại
<đoạn văn giao việc hoàn chỉnh, dán được ngay, đủ sản phẩm + quy trình + vai>
```
