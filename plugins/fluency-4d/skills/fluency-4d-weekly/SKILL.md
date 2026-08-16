---
name: fluency-4d-weekly
description: Tổng hợp sổ điểm AI Fluency 4D theo tuần và chạy một vòng cải tiến DMIR — trung bình từng ô trong cửa sổ 7 ngày, phát hiện ô đang tụt bằng ngưỡng số, chốt ô RÀNG BUỘC (ô thượng nguồn, thường khác ô thấp nhất), chép bản đồ ô-kéo-ô, kê một ứng viên thí nghiệm nhắm ràng buộc, nghiệm thu vòng trước bằng số. Triggers on "4d weekly", "tổng hợp tuần 4d", "xu hướng fluency", "tuần này tôi tiến bộ chưa", "báo cáo tuần 4d", "fluency weekly", "ràng buộc tuần này".
---

# /fluency-4d-weekly — Tổng hợp tuần, một vòng DMIR

**COD:** Offload (AI tổng hợp) · Core (CEO chốt D ưu tiên và viết câu thí nghiệm)

Đọc: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\sessions.jsonl` và `experiments.md`.
Đọc thêm: `../fluency-4d-shared/references/improvement-playbook.md` — menu cách cải tiến
cho từng ô, và `../fluency-4d-shared/references/active-profile.md` — tên profile đang bật; mở đúng
file profile đó để lấy trường `Cách cải tiến tại chỗ` riêng của tổ chức. KHÔNG đoán tên profile.
Đọc thêm: `../fluency-4d-shared/references/experiment-protocol.md` — Bảng 1 (DMIR đọc gì ghi gì),
Bảng 2 (bản đồ ô kéo ô, 18 cạnh), Bảng 3 (tầng đòn bẩy + luật leo tầng), và Luật bước R.
Ghi: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\weekly/<năm>-W<số tuần ISO>.md`

**Đọc không được thì DỪNG.** Thiếu `improvement-playbook.md` thì KHÔNG in bảng gợi ý —
in thẳng tên file thiếu rồi bỏ trống mục đó. Tự nghĩ cách cải tiến thay cho menu là
vi phạm chốt chặn ở Bước 7, không phải ứng biến cho tiện. Thiếu `experiment-protocol.md`
thì KHÔNG chạy Bước 5, 6, 9 — in tên file thiếu, chạy phần còn lại như bản chưa có DMIR.

## Ba việc AI KHÔNG được làm

1. **Không tự chế cách cải tiến.** Mọi dòng trong bảng gợi ý phải chép từ
   `improvement-playbook.md`. Ô nào playbook chưa có thì ghi "playbook chưa có mục này",
   không điền bù bằng chữ tự nghĩ.
2. **Không tự viết câu nếu–thì.** Bước 8 chỉ liệt kê ứng viên kèm số; câu cam kết do CEO viết.
   Lý do là chốt chặn: coach tự kê thí nghiệm cho chính hành vi mà nó vừa chấm thì nó
   đang chấm bài của chính mình, và sẽ nghiêng về ô dễ ghi streak.
3. **Không tự dựng bản đồ nhân quả.** Mọi cạnh ô-kéo-ô phải chép từ Bảng 2 của
   `experiment-protocol.md`. Cấm suy tương quan giữa các ô từ `sessions.jsonl` — vài chục
   điểm nguyên trong một tuần không đủ cho bất kỳ tương quan nào, và một bản đồ dựng lúc
   chạy sẽ luôn dựng thành cái biện minh cho ô vừa chọn.

## Mười bước

Bốn bước mới mang nhãn DMIR: **Bước 5 = D**, **Bước 6 = M**, **Bước 8 = I**, **Bước 9 = R**.
Sáu bước còn lại là phần tính toán vốn có, giữ nguyên.

**Bước 1 — Lấy cửa sổ.** Đọc `sessions.jsonl`, lọc bản ghi trong 7 ngày gần nhất. Lấy thêm cửa sổ 7 ngày liền trước để so sánh.

**Bước 2 — Chốt dữ liệu mỏng.** Cửa sổ hiện tại có dưới 3 phiên → in thẳng "**dữ liệu mỏng, không kết luận xu hướng**", liệt kê các phiên đã có rồi DỪNG. Không vẽ xu hướng, không in bảng gợi ý, không chốt D ưu tiên, không đoán. Đây là chốt cứng. Bước R cũng không chạy: nghiệm thu một vòng bằng dữ liệu mỏng hơn chính vòng đó là nghiệm thu giả.

**Bước 3 — Trung bình từng ô.** Với mỗi ô trong 12 ô, tính trung bình các điểm, **bỏ qua `null`** (n/a không phải 0, kéo trung bình xuống là sai). Ghi kèm số lần được chấm — trung bình từ 1 mẫu phải nói rõ là 1 mẫu. So với cửa sổ trước: ↑ / ↓ / =.

**Bước 4 — Xác định ô đang tụt.** Định nghĩa bằng số, không bằng cảm tính. Một ô gọi là **đang tụt** khi có **≥ 2 mẫu** trong cửa sổ hiện tại VÀ thoả ít nhất một trong ba:

- **(a) Tụt theo xu hướng:** trung bình tuần này ≤ trung bình tuần trước − 0.5
- **(b) Thấp dai dẳng:** trung bình ≤ 1.5 ở cả tuần này lẫn tuần trước
- **(c) Thấp tuyệt đối:** trung bình ≤ 1.5 với ≥ 3 mẫu ngay trong cửa sổ hiện tại, không cần cửa sổ trước

Tiêu chí (c) có mặt vì (a) và (b) đều đòi cửa sổ trước, mà tuần ĐẦU TIÊN không bao giờ có: thiếu (c) thì báo cáo tuần đầu luôn rỗng kể cả khi có ô ở 0.50 — vô dụng đúng lúc cần nhất. Ngưỡng mẫu của (c) cao hơn (3 thay vì 2) vì nó không có cửa sổ trước để đối chứng.

Ô có dưới 2 mẫu → ghi "chưa đủ mẫu", KHÔNG đưa vào bảng gợi ý và KHÔNG làm ứng viên thí nghiệm. Một mẫu không phải xu hướng.

Ô nào trung bình ≤ 1.5 trong ≥ 2 tuần liên tiếp → đánh dấu dai dẳng (đây là tập con của (b), in kèm số tuần đã kéo dài). Đọc `experiments.md`, báo tình trạng streak của thí nghiệm đang chạy và các thí nghiệm đã đóng trong tuần.

Các ô đang tụt ở bước này hợp thành **nhóm ứng viên** cho Bước 5.

**Bước 5 (D) — Chốt đúng một ô ràng buộc.** Ràng buộc là ô mà cải thiện nó kéo theo ô khác — **không phải** ô điểm thấp nhất. Hai ô này thường khác nhau, và luật dưới đây quyết định bằng số chứ không bằng cảm nhận.

- **Nhóm ứng viên rỗng** → in thẳng "**chưa đủ dữ liệu để chốt ràng buộc**", bỏ Bước 6, 7, 8, đi thẳng Bước 9. Cấm chọn đại một ô cho có.
- **Ràng buộc** = ô trong nhóm ứng viên mà **không ô ứng viên nào khác nằm thượng nguồn của nó** theo Bảng 2 của `experiment-protocol.md`, tính cả bắc cầu.
- **Còn nhiều ô như vậy** → thâm hụt lớn hơn (trung bình thấp hơn) thắng → nhiều mẫu hơn → thứ tự chính tắc `del.problem`, `del.platform`, `del.task`, `des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`, `dil.creation`, `dil.transparency`, `dil.deployment`.
- **Ô thượng nguồn NGOÀI nhóm ứng viên mà trung bình < 2.0** → in một dòng cảnh báo, **KHÔNG** tự động thành ràng buộc. Cửa "đang tụt và ≥ 2 mẫu" ở Bước 4 là thứ giữ báo cáo khỏi nói bừa; cho một ô chưa qua cửa đó lên làm ràng buộc là phá cửa từ phía sau.

Báo cáo **bắt buộc in cả hai**: ô thấp nhất tuyệt đối và ô ràng buộc, kèm một câu vì sao chúng khác nhau — hoặc nói thẳng là chúng trùng nhau. In mỗi ô thấp nhất là quay về luật cũ.

**Bước 6 (M) — Chép bản đồ, không vẽ bản đồ.** Từ Bảng 2 của `experiment-protocol.md`, chép nguyên văn:

- **Tối đa 4 cạnh ra** của ô ràng buộc (các ô nó kéo), kèm cột "Vì sao" nguyên văn.
- **Mọi ô thượng nguồn** của ô ràng buộc, kèm trung bình tuần này — đây là bằng chứng không còn gì hỏng ở phía trên nó.
- **Tầng đòn bẩy** của ô ràng buộc lấy từ Bảng 3 (L3 Mục tiêu / L5 Luật / L6 Dòng thông tin).

Ô ràng buộc là một trong bốn ô cuối nhánh (`dis.performance`, `dil.creation`, `dil.transparency`, `dil.deployment`) → ghi "không có cạnh ra, cố ý" và chỉ in phần thượng nguồn.

Cấm ba thứ ở bước này: vẽ cạnh không có trong Bảng 2; gọi bảng là "mô hình"; ước lượng tương quan giữa các ô từ sổ.

**Bước 7 — Bảng gợi ý cải tiến, gom theo 4 D.** Với mỗi ô đang tụt ở Bước 4, chép dòng tương ứng từ `improvement-playbook.md`, chồng thêm trường `Cách cải tiến tại chỗ` của profile đang bật nếu ô đó có. In thành **bốn bảng con** theo D: Delegation, Description, Discernment, Diligence.

- Chỉ in ô **đang tụt**. Ô không tụt thì không in — bảng đủ 12 dòng mỗi tuần là bảng vô dụng.
- D nào không có ô nào tụt → ghi một dòng "không có ô nào tụt", bỏ bảng con đó.
- Mỗi dòng phải kèm **căn cứ bằng số** trích từ sổ: trung bình tuần này, tuần trước, số mẫu.
- Đánh dấu **◀ RÀNG BUỘC** vào đúng dòng của ô ràng buộc ở Bước 5.
- **Chỉ được chọn dòng có sẵn trong playbook.** Không tự chế cách cải tiến mới.

**Bước 8 (I) — Đúng một ứng viên thí nghiệm, nhắm ràng buộc, để trống câu cam kết.** Ứng viên thứ nhất **phải là ô ràng buộc** ở Bước 5, không phải ô tụt sâu nhất. In tối đa 3 ứng viên, ô ràng buộc đứng đầu, phần còn lại xếp theo mức tụt giảm dần. Mỗi ứng viên kèm: mã ô, trung bình tuần này/tuần trước, số mẫu, số tuần đã tụt liên tiếp, và **trích dẫn dòng sổ** làm căn cứ.

- **WIP = 1 vẫn thắng ràng buộc.** Còn dòng `OPEN` trong `experiments.md` → nói rõ WIP = 1, các ứng viên này đang xếp hàng, KHÔNG kê mới. Ràng buộc không có quyền phá luật này.
- **Cờ lệch ô.** Dòng `OPEN` nhắm ô khác ô ràng buộc → in đúng dòng này: `LỆCH Ô: thí nghiệm đang chạy nhắm <ô cũ>, ràng buộc tuần này là <ô mới> — đóng sớm để chuyển hay chạy nốt, CEO chốt.` AI không tự đóng, không tự chuyển.
- **Luật leo tầng.** Ô ràng buộc đã có ≥ 1 thí nghiệm `FAILED` nhắm đúng nó trong `experiments.md` → in cảnh báo kèm tầng của ô lấy từ Bảng 3, và nêu ràng buộc: câu nếu–thì lần này phải đổi mục tiêu / luật / dòng thông tin, không được là tham số L12 kiểu "làm kỹ hơn". Vẫn không viết hộ câu.

Sau danh sách, in **ô trống để CEO tự viết** câu nếu–thì. Cấm điền hộ, cấm gợi ý mẫu câu.

**Bước 9 (R) — Nghiệm thu vòng trước bằng số.** Theo "Luật bước R" trong `experiment-protocol.md`. Đọc báo cáo weekly của tuần liền trước.

- **Không có file weekly tuần trước** → in `vòng trước: không có`, bỏ qua phần còn lại của bước này. Cấm dựng lại hồi cứu từ trí nhớ.
- **R1 — ô ràng buộc tuần trước có nhúc nhích không.** Trung bình tuần này trừ tuần trước: ≥ +0.5 → `ĐỠ`; trong khoảng ±0.5 → `ĐỨNG YÊN`; ≤ −0.5 → `TỆ ĐI`. In cả ba con số, không in mỗi kết luận.
- **R2 — cạnh đặt cược có đúng không.** Đây là giả định bị chất vấn: tuần trước chọn ô đó vì tin nó kéo ô hạ nguồn. Ô thượng nguồn `ĐỠ` mà **không ô hạ nguồn nào đỡ ≥ +0.3** → đánh dấu cạnh `NGHI VẤN`. Cùng một cạnh nghi vấn **3 tuần liên tiếp** → in đề nghị CEO xoá cạnh khỏi Bảng 2. AI không tự xoá Bảng 2.
- **R3 — kết quả ghi vào đâu.** Chỉ ghi vào `weekly/<năm>-W<tuần>.md`, hai mục `R — Nghiệm thu vòng trước` và `Cạnh nghi vấn`. Weekly KHÔNG sửa `experiments.md` — đóng thí nghiệm là việc của `fluency-4d-review`.

**Bước 10 — Chốt 1 D ưu tiên.** Đúng một D (không phải một ô) cho tuần tới, kèm lý do bằng số. Mặc định là D chứa ô ràng buộc; chọn D khác thì phải nói vì sao. Ghi file `weekly/<năm>-W<tuần>.md`.

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

## D — Ràng buộc tuần này
Ô thấp nhất tuyệt đối: <mã ô> <TB>
Ràng buộc:              <mã ô> <TB> — <vì sao hai ô khác nhau, hoặc "trùng nhau">
Bị loại vì có ô thượng nguồn trong nhóm: <mã ô ← mã ô thượng nguồn>, …
Cảnh báo thượng nguồn ngoài nhóm ứng viên, TB < 2.0: <mã ô> <TB> — chưa đủ điều kiện làm ràng buộc
— hoặc "chưa đủ dữ liệu để chốt ràng buộc"

## M — Bản đồ (chép từ Bảng 2)
Tầng đòn bẩy của ô ràng buộc: <L3 Mục tiêu | L5 Luật | L6 Dòng thông tin>
Thượng nguồn của nó: <mã ô> <TB> · … (hoặc "không có ô thượng nguồn")
| Cạnh | Kéo ô | Vì sao (nguyên văn Bảng 2) |
|---|---|---|
… tối đa 4 cạnh ra; ô cuối nhánh ghi "không có cạnh ra, cố ý" …

## Gợi ý cải tiến (từ improvement-playbook.md)

### Delegation
| Ô | Căn cứ (TB nay / trước / n mẫu) | Cách cải tiến | Dấu hiệu đã ăn | Bẫy thường gặp |
|---|---|---|---|---|
… chỉ các ô đang tụt; ô ràng buộc đánh dấu ◀ RÀNG BUỘC; không có thì ghi "không có ô nào tụt" …

### Description
### Discernment
### Diligence
… ba bảng con cùng khuôn …

## Thí nghiệm
<ID đang chạy · streak x/3 · đứt y/3> · <đã PASSED/FAILED trong tuần>
<LỆCH Ô: … nếu ô mục tiêu khác ô ràng buộc>
<LEO TẦNG: … nếu ô ràng buộc đã từng FAILED>

## I — Ứng viên thí nghiệm tuần tới
1. <mã ô ràng buộc> ◀ RÀNG BUỘC — TB <x> (tuần trước <y>, <n> mẫu, tụt <k> tuần liên tiếp)
   căn cứ: <trích dòng sổ>
2. …

Câu nếu–thì (CEO tự viết):
> Khi ………………………………, tôi ……………………………… .

## R — Nghiệm thu vòng trước
Ràng buộc tuần trước: <mã ô> — TB <tuần trước> → <tuần này> = <hiệu số> → ĐỠ / ĐỨNG YÊN / TỆ ĐI
Ô hạ nguồn: <mã ô> <hiệu số> · …
— hoặc "vòng trước: không có"

## Cạnh nghi vấn
<cạnh #n: ô → ô · NGHI VẤN tuần thứ <k>/3>  — hoặc "không có"

## 1 D ưu tiên tuần tới
<Delegation | Description | Discernment | Diligence> — vì <lý do bằng số>
```
