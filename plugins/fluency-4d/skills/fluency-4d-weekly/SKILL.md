---
name: fluency-4d-weekly
description: Tổng hợp sổ điểm AI Fluency 4D theo tuần — trung bình từng ô trong cửa sổ 7 ngày, so với tuần trước, phát hiện ô yếu dai dẳng, báo tình trạng thí nghiệm, chốt một D ưu tiên cho tuần tới. Triggers on "4d weekly", "tổng hợp tuần 4d", "xu hướng fluency", "tuần này tôi tiến bộ chưa", "báo cáo tuần 4d", "fluency weekly".
---

# /fluency-4d-weekly — Tổng hợp tuần

**COD:** Offload (AI tổng hợp) · Core (CEO chốt D ưu tiên)

Đọc: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\sessions.jsonl` và `experiments.md`.
Ghi: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\weekly/<năm>-W<số tuần ISO>.md`

## Năm bước

**Bước 1 — Lấy cửa sổ.** Đọc `sessions.jsonl`, lọc bản ghi trong 7 ngày gần nhất. Lấy thêm cửa sổ 7 ngày liền trước để so sánh.

**Bước 2 — Chốt dữ liệu mỏng.** Cửa sổ hiện tại có dưới 3 phiên → in thẳng "**dữ liệu mỏng, không kết luận xu hướng**", liệt kê các phiên đã có rồi DỪNG. Không vẽ xu hướng, không chốt D ưu tiên, không đoán. Đây là chốt cứng.

**Bước 3 — Trung bình từng ô.** Với mỗi ô trong 12 ô, tính trung bình các điểm, **bỏ qua `null`** (n/a không phải 0, kéo trung bình xuống là sai). Ghi kèm số lần được chấm — trung bình từ 1 mẫu phải nói rõ là 1 mẫu. So với cửa sổ trước: ↑ / ↓ / =.

**Bước 4 — Ô yếu dai dẳng.** Ô nào trung bình ≤ 1.5 trong ≥ 2 tuần liên tiếp → đánh dấu dai dẳng. Đọc `experiments.md`, báo tình trạng streak của thí nghiệm đang chạy và các thí nghiệm đã đóng trong tuần.

**Bước 5 — Chốt 1 D ưu tiên.** Đúng một D (không phải một ô) cho tuần tới, kèm lý do bằng số. Ghi file `weekly/<năm>-W<tuần>.md`.

## Khuôn báo cáo

```
# Tuần <năm>-W<tuần> — AI Fluency 4D
Số phiên: <n> · Chế độ hay dùng: <mode>

## Trung bình từng ô
| Ô | TB tuần này (n mẫu) | Tuần trước | Xu hướng |
|---|---|---|---|
… đủ 12 dòng, ô không có mẫu ghi "—" …

## Ô yếu dai dẳng
<danh sách, kèm số tuần liên tiếp>

## Thí nghiệm
<ID đang chạy · streak x/3 · đứt y/3> · <đã PASSED/FAILED trong tuần>

## 1 D ưu tiên tuần tới
<Delegation | Description | Discernment | Diligence> — vì <lý do bằng số>
```
