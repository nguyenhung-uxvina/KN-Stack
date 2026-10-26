---
name: helix-cc2-form
description: "Khối C2 của bộ helix-cc2 — từ chuỗi C&C² CEO đã chọn ở Cổng CEO 2 sinh 2–3 phương án hình thể (A-1, A-2…) cho mỗi chuỗi; mỗi phương án có mô tả hình học bằng lời, phác Mermaid hoặc ASCII, bảng «Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn» lấy từ quy tắc hiện thân (embodiment-rules) và khối «Phép nên làm tiếp». Hình thể là giả thuyết: lý do mang nhãn phỏng đoán cho tới khi có phép thử; không chọn phương án thay CEO. Triggers on: 'form variants', 'embodiment variants', 'C&C2 form', 'geometry from chain', 'phương án hình thể', 'hình thể từ chuỗi', 'quy tắc hiện thân', 'helix-cc2-form'."
---

# helix-cc2-form — Khối C2: 2–3 phương án hình thể mỗi chuỗi

> **Vai:** sau Cổng CEO 2, trước C3. Biến chuỗi đã chọn thành vài hình thể cụ thể kèm lý do; không xếp hạng, không chọn.
> **Đầu vào:** `{{prefix}}CC2_C1_Chains.md` (chuỗi đã chọn ghi ở bảng **Cổng CEO** của `_pipeline_state.md`, cột «Chuỗi chọn») |
> **Đầu ra:** `{{prefix}}CC2_C2_Forms.md` | **Đọc bởi:** C3, C6
> **Nguồn dùng chung:** `helix-cc2:references:embodiment-rules` (bảng quy tắc), `helix-cc2:references:cc2-core`
> (§Hai loại nhãn), `helix-cc2:references:view-ops` (§Rào cản quan sát).

## Đầu vào

- Bắt buộc: `{{prefix}}CC2_C1_Chains.md` và chuỗi chọn trong `_pipeline_state.md` (vd. `B.1`). Thiếu tệp nào → liệt kê tệp
  thiếu và dừng; không tự chọn chuỗi, không dựng giả C1.
- Chế độ dự án: chạy theo từng `F-id`; đọc và ghi trong `<nơi ghi>/<F-id>/` (C0 nằm ở gốc `<nơi ghi>/`).
- Chuỗi chọn có phiên bản `--op` (`B.1`, `B.2`…): dùng đúng phiên bản CEO chỉ định.

## Luật cứng

1. **2–3 phương án mỗi chuỗi** *(quy ước bộ skill)*, đặt `A-1`, `A-2`, `A-3` (chuỗi `B` thì `B-1`…). Khác nhau ở **hình học
   hay vật liệu** của WFP và LSS đã nêu trong chuỗi — không đổi chuỗi (đổi chuỗi là việc của C1) và không chỉ đổi một con số
   (việc của C3). Mỗi phương án ghi một dòng `Khác phương án <X> ở:` nêu tham số hình thể nào khác.
2. **Mỗi phương án có lý do từ quy tắc hiện thân:** bảng `| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |`, mỗi dòng lấy
   *nguyên văn tên quy tắc* ở cột «Quy tắc» của `helix-cc2:references:embodiment-rules`, **ít nhất một dòng**. Không bịa quy
   tắc ngoài bảng; thiếu quy tắc hợp thì ghi `Quy tắc: chưa có trong embodiment-rules` và nhãn `giả định`.
3. **Cột «Kết quả»** trả lời câu hỏi kiểm của quy tắc bằng lời (đạt / chưa đạt / chưa biết + vì sao), không số bịa. Cột
   **«Nhãn»** là `tri thức` / `phỏng đoán` / `giả định` (`helix-cc2:references:cc2-core` §Hai loại nhãn). Lý do hình thể
   mặc định là `phỏng đoán` cho tới khi có phép thử; `tri thức` chỉ khi nguồn công khai kiểm được và ghi nguồn.
4. **Hai quy tắc kéo ngược nhau** → ghi cả hai dòng, không dàn xếp; C3/C4 quyết bằng tham số nhạy nhất.
5. **Phác hình vẽ tay lại được:** Mermaid `flowchart LR` hoặc ASCII, bám các phần tử WFP/LSS/Connector của chuỗi (giữ tên
   phần tử trong C1). Mô tả bằng lời gồm: hình học từng WFP, LSS, vật liệu nếu đã định, Connector biên.
6. **Không có số bịa.** Chưa có số thì không ghi số. Không xếp hạng và không chấm điểm phương án.
7. Hình thể đi vào điện tử / phần mềm: ghi chỗ C&C² hết dùng được (`helix-cc2:references:multidomain` §Chỗ phải dừng).

## Bước

1. Đọc chuỗi chọn; liệt kê phần tử WFP/LSS/Connector và mặt biên.
2. Nghĩ 2–3 cách hiện thân khác nhau thật (luật 1). Với mỗi cách, mô tả hình học và phác hình.
3. Với từng phương án: duyệt bảng quy tắc, chọn các dòng hợp, điền câu hỏi kiểm, kết quả và nhãn (luật 2–3).
4. Viết 1–3 dòng `## Phép nên làm tiếp` theo rào cản quan sát (`helix-cc2:references:view-ops` §Rào cản quan sát).
5. Cập nhật `_pipeline_state.md` (cột C2). **Không có Cổng CEO riêng ở C2** (Cổng CEO của orchestrator chỉ có 3 cổng:
   sàng, chọn chuỗi, ký dự đoán) — CEO xem lại phương án khi duyệt C3; muốn loại phương án nào thì nói ở đó.

## Khuôn đầu ra: `{{prefix}}CC2_C2_Forms.md`

````markdown
---
updated: YYYY-MM-DD
f_id: {{F-id hoặc —}}
chuỗi chọn: {{vd. A}}
---
# CC2 C2 — Phương án hình thể cho chuỗi {{X}}: {{chức năng}}

> Hình thể là giả thuyết. Lý do dưới đây là `phỏng đoán` cho tới khi có phép thử.

### Phương án {{X}}-1 — {{tên ngắn}}

{{mô tả hình học bằng lời: WFP, LSS, vật liệu, Connector biên}}

```mermaid
flowchart LR
  C1([Connector]) --> W1[WFP1: {{hình học}}]
  W1 --> L1[LSS: {{hình học}}]
  L1 --> W2[WFP2: {{hình học}}]
```

- Khác phương án {{Y}} ở: {{tham số hình thể}}

| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |
|---|---|---|---|
| {{tên quy tắc nguyên văn}} | {{câu hỏi}} | {{đạt / chưa đạt / chưa biết, vì sao}} | {{nhãn}} |

### Phương án {{X}}-2 — …

## Phép nên làm tiếp
- {{phép}} · {{phần tử}} · {{câu hỏi kích hoạt}}
````

## Ví dụ ngắn (cơ cấu công khai: nắp gài bằng móc đàn hồi; giả định, không số)

Chuỗi `A` đã chọn: tay người → WFP móc//gờ → LSS cần đàn hồi → WFP móc//gờ (gài giữ) → Connector khung thân.

### Phương án A-1 — cần móc ngàm một đầu

Cần đàn hồi nhô từ thành nắp, đầu cần có móc chạm gờ ở thân; một bộ cần và gờ. Khác phương án A-2 ở: số cần (1), kiểu khớp
(gài một phía).

```mermaid
flowchart LR
  H([Tay người]) --> W1[WFP mặt vào của móc]
  W1 --> L1[LSS cần đàn hồi]
  L1 --> W2[WFP móc // gờ giữ]
  W2 --> K([Connector khung thân])
```

| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |
|---|---|---|---|
| Đơn giản — hình học tính được | So sánh «đơn giản hơn» đã ghi pha (chế tạo, lắp, dùng)? Có đối xứng khi không có lý do lệch? | Cần là dầm một đầu, tính được; không đối xứng, một phía chịu lực | phỏng đoán |
| An toàn — hỏng an toàn | Năng lượng đưa hệ về trạng thái an toàn có nằm sẵn trong hệ (lò xo, trọng lực)? | Cần đàn hồi tự đưa nắp về trạng thái gài; chưa biết sau nhiều lần mở | phỏng đoán |

### Phương án A-2 — hai cần đối xứng

Hai cần đàn hồi đặt đối xứng hai bên, mỗi cần một móc và một gờ. Khác phương án A-1 ở: số cần (2), bố trí đối xứng.

| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |
|---|---|---|---|
| Thiết kế ít lỗi — bất biến, bù, chống lắp sai | Kích thước dung sai chặt nào bỏ được, làm bất biến được, chỉnh sau lắp được? Người không thiết kế có lắp sai được không? | Hai gờ phải khớp cùng lúc nên dung sai chặt hơn; chưa biết cách bù | giả định |
| Đơn giản — hình học tính được | So sánh «đơn giản hơn» đã ghi pha (chế tạo, lắp, dùng)? Có đối xứng khi không có lý do lệch? | Đối xứng, lực gài chia hai bên; chia đều chưa kiểm | phỏng đoán |

## Phép nên làm tiếp
- `zoom-in` · A-2:cần đàn hồi · mỗi cần có chịu cùng tải khi dung sai khác nhau không?

## Chạy riêng

```
/helix-cc2-form [--out <thư mục>]
```

Đầu vào tối thiểu: `{{prefix}}CC2_C1_Chains.md` và chuỗi chọn trong `_pipeline_state.md` ở nơi ghi (chạy `/helix-cc2-chain`
trước nếu chưa có). Chế độ dự án: truyền `--out <nơi ghi>/<F-id>` hoặc để C2 đọc `current_f`.

## COD

| Việc | Lớp | Ai |
|---|---|---|
| Sinh phương án, phác hình, bảng quy tắc, «Phép nên làm tiếp» | **O** Offload | AI |
| Giữ hay loại phương án, quyết hình thể đi tiếp sang C3 | **C** Core | CEO / kỹ sư |
| Cập nhật `_pipeline_state.md` | **D** Default | tự động |
