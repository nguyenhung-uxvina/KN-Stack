---
name: fluency-4d-review
description: Mổ xẻ phiên làm việc vừa xong theo khung AI Fluency 4D — chấm 12 ô năng lực bằng bằng chứng trích dẫn từ chính phiên, nghiệm thu thí nghiệm hành vi đang mở, kê thí nghiệm mới, ghi một dòng vào sổ điểm. Triggers on "4d review", "mổ xẻ phiên", "chấm phiên", "review fluency", "phiên vừa rồi thế nào", "đánh giá cách tôi làm việc với AI", "chấm 4D".
---

# /fluency-4d-review — Mổ xẻ phiên theo khung 4D

**COD:** Offload (AI chấm + ghi sổ) · Core (CEO nhận thí nghiệm và thực thi)

Đọc trước khi chấm:
- `../_shared/references/rubric-core.md` — 12 ô, thang điểm, ba chốt chống nịnh
- `../_shared/references/profile-workshop-x.md` — tín hiệu và cờ đỏ cho từng ô
- `../_shared/references/ledger-schema.md` — schema dòng sổ
- `../_shared/references/experiment-protocol.md` — luật WIP=1 và streak

Sổ điểm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`

## Ba chốt bắt buộc

1. **Không bằng chứng, không điểm.** Mọi ô ≠ 3 phải kèm trích dẫn nguyên văn từ phiên này. Không trích dẫn được → chấm `null` (n/a). Cấm suy đoán.
2. **Bắt buộc tìm điểm đau.** Báo cáo phải nêu ít nhất một ô ≤ 1, hoặc nói thẳng "không tìm thấy ô nào dưới 2" kèm lý do.
3. **Chấm trước, khen sau.** In bảng điểm và trích dẫn xong mới được viết phần ghi nhận điểm mạnh.

`null` là "phiên không tạo cơ hội quan sát" — **khác** `0` là "có cơ hội mà bỏ qua, hậu quả thấy được".

## Sáu bước

**Bước 1 — Trích bằng chứng.** Đọc lại phiên hội thoại đang trong ngữ cảnh (không đi tìm file log). Trích nguyên văn các đoạn liên quan tới từng ô.

**Bước 2 — Chấm 12 ô.** Theo `rubric-core.md`, soi tín hiệu trong `profile-workshop-x.md`. Ghi chế độ phiên: automation / augmentation / agency. Thứ tự: `del.problem`, `del.platform`, `del.task`, `des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`, `dil.creation`, `dil.transparency`, `dil.deployment`.

**Bước 3 — Nghiệm thu thí nghiệm đang mở TRƯỚC.** Đọc `experiments.md`. Nếu có dòng `OPEN`: phiên này giữ được hay đứt? Giữ → streak +1 (đủ 3 → `PASSED`, ghi ngày đóng). Đứt → streak về 0, cột `đứt` +1 (đủ 3 → `FAILED`). Làm xong bước này rồi mới đi tiếp.

**Bước 4 — Chọn ô yếu nhất.** Điểm thấp nhất. Hòa → ô xuất hiện làm `weakest` nhiều lần nhất trong `sessions.jsonl` 30 ngày gần nhất. Vẫn hòa → thứ tự ưu tiên `dil` > `dis` > `des` > `del`.

**Bước 5 — Kê hoặc giữ thí nghiệm.** **WIP = 1.** Còn dòng `OPEN` sau Bước 3 → giữ nguyên, KHÔNG kê mới, kể cả khi Bước 4 tìm được ô yếu nặng hơn; chỉ nói một dòng rằng ô đó đang xếp hàng. Không còn dòng `OPEN` → kê đúng một thí nghiệm dạng nếu–thì ("Khi …, tôi …"), nhắm ô ở Bước 4. Nếu thí nghiệm vừa `FAILED` → kê cái NHỎ HƠN cho cùng ô, cấm chép lại câu cũ.

**Bước 6 — Ghi sổ.** Append đúng một dòng vào `sessions.jsonl` theo `ledger-schema.md`; cập nhật `experiments.md`. Trích dẫn bằng chứng KHÔNG được đưa vào `sessions.jsonl` — nó chỉ nằm trong báo cáo in ra màn hình.

## Ngoại lệ cờ đỏ

Bất kỳ ô `dil.*` nào chấm `0` — rò rỉ dữ liệu MẬT, dán giá nhà cung cấp, commit thẳng `main` — thì **không** đi vào vòng thí nghiệm. Đặt cảnh báo **CỜ ĐỎ** lên đầu báo cáo, nêu việc phải xử ngay trong phiên. Vòng thí nghiệm dành cho thói quen dài hạn, không dành cho sự cố cần xử lý ngay.

## Khuôn báo cáo

```
## Mổ xẻ phiên <id> — <dự án> — chế độ <mode>

[CỜ ĐỎ nếu có, đặt trên cùng]

### Điểm
| Ô | Điểm | Bằng chứng |
|---|---|---|
| del.problem | 2 | "…trích nguyên văn…" |
… đủ 12 dòng …

### Điểm đau
<ô ≤ 1 và vì sao> HOẶC "không tìm thấy ô nào dưới 2 vì …"

### Thí nghiệm
<nghiệm thu cái đang mở> → <kê mới HOẶC giữ nguyên vì WIP=1>

### Ghi nhận
<điểm mạnh — chỉ viết sau khi điểm đã chốt>

### Đã ghi sổ
<dòng JSONL vừa append>
```
