# C&C² cho cơ – điện – quang – phần mềm nhúng: chỗ dùng được, chỗ phải dừng

> Reference dùng chung của bộ `helix-cc2`, dùng ở C0 (sàng chức năng con), C1 (chuỗi đi qua nhiều miền) và C6
> (ghi chỗ C&C² không dùng được trong bàn giao). Nguồn: CC = *Mô hình C&C² và giả thuyết kết cấu*. Ví dụ quang chỉ ở
> mức nguyên lý chung, không số.

## Chỗ mô hình còn dùng được

- **Định nghĩa đã cho phép mọi miền.** WFP sinh được từ bề mặt rắn hoặc mặt giao của chất lỏng, khí, trường; LSS là thể tích vật rắn, chất lưu hoặc không gian có trường xuyên qua. Cái thiếu là cách làm, không phải định nghĩa (CC Ch15 §15.1).
- **Mặt phân cách chất lưu là WFP thật.** Ổ trượt thuỷ động: màng dầu là LSS, hai mặt dầu–trục và dầu–bạc là hai WFP; cùng một phần chất lỏng có lúc là mặt làm việc, có lúc là LSS (CC Ch02 §02.3).
- **Năng lượng và thông tin là hai kênh.** Tách truyền công suất *thực hiện* chức năng khỏi truyền dữ liệu chỉ *quy định* chức năng; trên phiếu hai thứ ấy không vẽ cùng một kiểu đường (CC Ch15 §15.1).
- **WFP là chỗ đổi miền.** Khoanh riêng mọi WFP mà ở đó năng lượng đổi miền (điện → cơ, cơ → nhiệt, quang → điện); đó thường là chỗ có hiện tượng chưa ai trong nhóm hiểu trọn (CC Ch15 §15.1).
- **Connector nguồn.** Đánh dấu chỗ năng lượng đi vào hệ; người đọc tự suy hướng ở các LSS, không gắn mũi tên lên mọi LSS (CC Ch15 §15.1).
- **Trường xuyên qua khe.** Với từ thông, LSS gồm mọi thể tích liên tục mà trường đi qua, kể cả khe khí; mỗi chỗ chuyển vật liệu là một WFP; khối khí làm nhiều việc thì chia thành thể tích kiểm soát (CC Ch15 §15.2).
- **Bỏ một phần tử thì hỏi chức năng của nó đi đâu.** Bỏ một lớp cách điện, một tấm đệm, một vỏ trong: chức năng cũ phải có chỗ mới trên phiếu hoặc một dòng «chấp nhận mất» (CC Ch15 §15.2).
- **Phần mềm là Connector có tên và trạng thái**, nối vào mô hình qua kênh thông tin, không vẽ thành LSS: đổi phần mềm không đổi hình thể của cặp mặt nhưng đổi trạng thái mà cặp mặt phải chịu. Đây là đề xuất của sách, chưa có ca kiểm (CC Ch15 §15.1).
- **Mặt bắt là chỗ nhiều dòng gặp nhau.** Mặt bắt của một vỏ kín chứa mạch điện tử đỡ tải, dẫn hay cản nhiệt, có khi nối đất: một WFP mang nhiều giả thuyết; vẽ nó một lần cho mỗi miền rồi chồng lên, mỗi miền một màu (CC Ch15 §15.6).

### Ví dụ quang → điện ở mức nguyên lý (đề xuất của bộ skill)

Sách ghi rằng phần đa miền *chưa* được thử ở miền quang (CC Ch15 §15.1). Vì vậy cách đọc dưới đây là `giả định` làm
việc, không phải tri thức của sách. Một rào sáng chung đọc thành chuỗi: Connector nguồn (nguồn sáng) → WFP mặt phát /
không khí → LSS là khoảng không khí có chùm tia đi qua → WFP không khí / mặt thu → Connector (mạch đọc). Vật che là
một phần tử *xuất hiện ở một trạng thái*: nó thêm hai WFP (mặt vật / chùm tia) và cắt LSS. Ba cách sắp khác nhau
thật, đúng loại khác biệt mà C1 cần:

| Cách sắp | Chuỗi khác ở đâu | Chỗ đổi miền |
|---|---|---|
| Rào sáng xuyên tia | Phát và thu ở hai phía; vật che cắt LSS giữa hai bên | WFP không khí / mặt thu |
| Rào sáng phản xạ ngược | Phát và thu cùng phía; thêm một WFP ở mặt phản xạ, LSS đi hai lượt | WFP không khí / mặt thu, cùng phía với nguồn |
| Bóng đổ lên mảng thu | Một nguồn, nhiều mặt thu; vật che đổi *phần* LSS nào bị cắt, nên trạng thái mang cả vị trí | Nhiều WFP không khí / phần tử thu |

Phía sau mặt thu, chuỗi đi vào mạch điện tử: C&C² dừng ở đó (xem dưới).

## Chỗ phải dừng

- **Không chọn C&C² khi chức năng nằm chủ yếu ở điện, phần mềm**, hoặc khi câu hỏi đã định lượng và mô hình tính đã đúng (CC Ch02 §02.12).
- **Mã nguồn.** Chưa nguồn nào trên máy dựng một mô hình C&C² mà phần tử là đoạn mã; thuật toán, logic điều khiển, xử lý tín hiệu nằm ngoài mô hình (CC Ch15 §15.6).
- **Mạch điện tử bên trong.** Khi miền điện từ là lõi chức năng, chưa có quy ước chuẩn cho chuyển đổi năng lượng giữa miền và cho thể tích có trường xuyên qua mà không có bề mặt rõ (CC Ch15 §15.2).
- **Lực sinh trong thể tích.** Lực từ không đi từ mặt sang mặt mà sinh trong một thể tích; vẽ nó xuất phát ở WFP chỉ là cách gọn, không phải lúc nào cũng được (CC Ch15 §15.2).
- **Mô hình học máy không thay mô hình định tính.** Mô hình thống kê dự báo trong vùng đã đo, không nói cặp mặt nào gây hiện tượng và im lặng ngoài vùng dữ liệu; phiếu C&C² đi trước, mô hình thống kê đi sau (CC Ch15 §15.5).
- **Bằng chứng đa miền rất mỏng**: một ca stator, một nhóm tác giả, mô hình định tính, không đối chứng (CC Ch15 §15.2).

Ở chỗ dừng, chuỗi không bị xoá: phần tử cuối còn trong miền vật lý trở thành một **Connector có tên** (ví dụ «mạch
đọc mặt thu, trạng thái 2»), và yêu cầu của nó đi sang tài liệu của ngành tương ứng (CC Ch15 §15.6).

## Câu khuôn

Mỗi chức năng con bị sàng ra ô `không áp dụng` (xem `cc2-core.md`), hoặc mỗi đoạn chuỗi bị cắt, ghi đúng một dòng:

```text
C&C²: không áp dụng, vì <chức năng nằm ở miền nào> — <lý do theo một dòng ở mục Chỗ phải dừng>; chuyển sang <tài liệu / skill của ngành đó>
```

Ví dụ:

- `C&C²: không áp dụng, vì chức năng «lọc nhiễu số» nằm ở phần mềm — chưa có mô hình C&C² cho mã nguồn; chuyển sang đặc tả phần mềm` (CC Ch15 §15.6).
- `C&C²: không áp dụng, vì chức năng «khuếch đại tín hiệu mặt thu» nằm trong mạch điện tử — miền điện chưa có quy ước chuẩn; chuyển sang thiết kế mạch` (CC Ch15 §15.2).
- `C&C²: không áp dụng, vì quan hệ «lực lò xo theo độ nén» đã có công thức — câu hỏi đã định lượng; dùng bảng tham số` (CC Ch02 §02.12).
