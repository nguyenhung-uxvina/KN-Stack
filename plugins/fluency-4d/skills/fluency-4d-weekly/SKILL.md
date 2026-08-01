---
name: fluency-4d-weekly
description: Tổng hợp sổ điểm AI Fluency 4D theo tuần — trung bình từng ô trong cửa sổ 7 ngày, so với tuần trước, phát hiện ô đang tụt bằng ngưỡng số, in bảng gợi ý cải tiến gom theo 4 D lấy từ playbook, kê ứng viên thí nghiệm kèm bằng chứng số, chốt một D ưu tiên cho tuần tới. Triggers on "4d weekly", "tổng hợp tuần 4d", "xu hướng fluency", "tuần này tôi tiến bộ chưa", "báo cáo tuần 4d", "fluency weekly".
---

# /fluency-4d-weekly — Tổng hợp tuần

**COD:** Offload (AI tổng hợp) · Core (CEO chốt D ưu tiên và viết câu thí nghiệm)

Đọc: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\sessions.jsonl` và `experiments.md`.
Đọc thêm: `../fluency-4d-shared/references/improvement-playbook.md` — menu cách cải tiến
cho từng ô, và `../fluency-4d-shared/references/active-profile.md` — tên profile đang bật; mở đúng
file profile đó để lấy trường `Cách cải tiến tại chỗ` riêng của tổ chức. KHÔNG đoán tên profile.
Ghi: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\weekly/<năm>-W<số tuần ISO>.md`

**Đọc không được thì DỪNG.** Thiếu `improvement-playbook.md` thì KHÔNG in bảng gợi ý —
in thẳng tên file thiếu rồi bỏ trống mục đó. Tự nghĩ cách cải tiến thay cho menu là
vi phạm chốt chặn ở Bước 5, không phải ứng biến cho tiện.

## Hai việc AI KHÔNG được làm

1. **Không tự chế cách cải tiến.** Mọi dòng trong bảng gợi ý phải chép từ
   `improvement-playbook.md`. Ô nào playbook chưa có thì ghi "playbook chưa có mục này",
   không điền bù bằng chữ tự nghĩ.
2. **Không tự viết câu nếu–thì.** Bước 6 chỉ liệt kê ứng viên kèm số; câu cam kết do CEO viết.
   Lý do là chốt chặn: coach tự kê thí nghiệm cho chính hành vi mà nó vừa chấm thì nó
   đang chấm bài của chính mình, và sẽ nghiêng về ô dễ ghi streak.

## Bảy bước

**Bước 1 — Lấy cửa sổ.** Đọc `sessions.jsonl`, lọc bản ghi trong 7 ngày gần nhất. Lấy thêm cửa sổ 7 ngày liền trước để so sánh.

**Bước 2 — Chốt dữ liệu mỏng.** Cửa sổ hiện tại có dưới 3 phiên → in thẳng "**dữ liệu mỏng, không kết luận xu hướng**", liệt kê các phiên đã có rồi DỪNG. Không vẽ xu hướng, không in bảng gợi ý, không chốt D ưu tiên, không đoán. Đây là chốt cứng.

**Bước 3 — Trung bình từng ô.** Với mỗi ô trong 12 ô, tính trung bình các điểm, **bỏ qua `null`** (n/a không phải 0, kéo trung bình xuống là sai). Ghi kèm số lần được chấm — trung bình từ 1 mẫu phải nói rõ là 1 mẫu. So với cửa sổ trước: ↑ / ↓ / =.

**Bước 4 — Xác định ô đang tụt.** Định nghĩa bằng số, không bằng cảm tính. Một ô gọi là **đang tụt** khi có **≥ 2 mẫu** trong cửa sổ hiện tại VÀ thoả ít nhất một trong hai:

- **(a) Tụt theo xu hướng:** trung bình tuần này ≤ trung bình tuần trước − 0.5
- **(b) Thấp dai dẳng:** trung bình ≤ 1.5 ở cả tuần này lẫn tuần trước

Ô có dưới 2 mẫu → ghi "chưa đủ mẫu", KHÔNG đưa vào bảng gợi ý và KHÔNG làm ứng viên thí nghiệm. Một mẫu không phải xu hướng.

Ô nào trung bình ≤ 1.5 trong ≥ 2 tuần liên tiếp → đánh dấu dai dẳng (đây là tập con của (b), in kèm số tuần đã kéo dài). Đọc `experiments.md`, báo tình trạng streak của thí nghiệm đang chạy và các thí nghiệm đã đóng trong tuần.

**Bước 5 — Bảng gợi ý cải tiến, gom theo 4 D.** Với mỗi ô đang tụt ở Bước 4, chép dòng tương ứng từ `improvement-playbook.md`, chồng thêm trường `Cách cải tiến tại chỗ` của profile đang bật nếu ô đó có. In thành **bốn bảng con** theo D: Delegation, Description, Discernment, Diligence.

- Chỉ in ô **đang tụt**. Ô không tụt thì không in — bảng đủ 12 dòng mỗi tuần là bảng vô dụng.
- D nào không có ô nào tụt → ghi một dòng "không có ô nào tụt", bỏ bảng con đó.
- Mỗi dòng phải kèm **căn cứ bằng số** trích từ sổ: trung bình tuần này, tuần trước, số mẫu.
- **Chỉ được chọn dòng có sẵn trong playbook.** Không tự chế cách cải tiến mới.

**Bước 6 — Ứng viên thí nghiệm, để trống câu cam kết.** Xếp các ô đang tụt theo mức tụt giảm dần, in tối đa 3 ứng viên. Mỗi ứng viên kèm: mã ô, trung bình tuần này/tuần trước, số mẫu, số tuần đã tụt liên tiếp, và **trích dẫn dòng sổ** làm căn cứ.

Còn dòng `OPEN` trong `experiments.md` → nói rõ WIP = 1, các ứng viên này đang xếp hàng, không kê mới.

Sau danh sách, in **ô trống để CEO tự viết** câu nếu–thì. Cấm điền hộ, cấm gợi ý mẫu câu.

**Bước 7 — Chốt 1 D ưu tiên.** Đúng một D (không phải một ô) cho tuần tới, kèm lý do bằng số. Ghi file `weekly/<năm>-W<tuần>.md`.

## Khuôn báo cáo

```
# Tuần <năm>-W<tuần> — AI Fluency 4D
Số phiên: <n> · Chế độ hay dùng: <mode>

## Trung bình từng ô
| Ô | TB tuần này (n mẫu) | Tuần trước | Xu hướng |
|---|---|---|---|
… đủ 12 dòng, ô không có mẫu ghi "—" …

## Ô đang tụt
<mã ô · tiêu chí (a) hay (b) · số liệu>  — hoặc "không có ô nào đạt ngưỡng tụt"
<ô dưới 2 mẫu liệt kê riêng, ghi "chưa đủ mẫu">

## Gợi ý cải tiến (từ improvement-playbook.md)

### Delegation
| Ô | Căn cứ (TB nay / trước / n mẫu) | Cách cải tiến | Dấu hiệu đã ăn | Bẫy thường gặp |
|---|---|---|---|---|
… chỉ các ô đang tụt; không có thì ghi "không có ô nào tụt" …

### Description
### Discernment
### Diligence
… ba bảng con cùng khuôn …

## Thí nghiệm
<ID đang chạy · streak x/3 · đứt y/3> · <đã PASSED/FAILED trong tuần>

## Ứng viên thí nghiệm tuần tới
1. <mã ô> — TB <x> (tuần trước <y>, <n> mẫu, tụt <k> tuần liên tiếp)
   căn cứ: <trích dòng sổ>
2. …

Câu nếu–thì (CEO tự viết):
> Khi ………………………………, tôi ……………………………… .

## 1 D ưu tiên tuần tới
<Delegation | Description | Discernment | Diligence> — vì <lý do bằng số>
```
