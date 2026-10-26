# Phiếu giả thuyết kết cấu 9 mục + kế hoạch thử trên bàn thử

> Reference dùng chung của bộ `helix-cc2`, dùng ở C4 (phiếu + kế hoạch thử), C6 (phiếu mở khi bàn giao) và CA
> (phiếu sinh từ phân tích). Nguồn: CC = *Mô hình C&C² và giả thuyết kết cấu*. Phiếu được
> `scripts/cc2_sheet_lint.py --kind hypo` chặn; khuôn dưới đây khớp đúng định dạng parser ấy.

## Vì sao có phiếu

- Giả thuyết là phỏng đoán được làm cho kiểm được: «như vậy giả thuyết mô tả một phỏng đoán kiểm được về quan hệ giữa hình thể và chức năng» (CC Ch06 §06.6).
- Chỉ cần viết tường minh phỏng đoán là đã lộ chỗ hổng trong hiểu biết; câu khung là *Nếu* [tham số hình thể] — *Thì* [chức năng đo được] — *Vì* [cơ chế] (CC Ch06 §06.6).
- Mục 1–6 theo khuôn sáu mục của nguồn; mục 7–9 là phần ghép của sách (dự đoán viết trước; độ tin / tầm ảnh hưởng; loại lặp nếu bị bác) (CC Ch06 §06.6).
- Giả thuyết bị bác vẫn sinh tri thức làm tăng hiểu biết về hệ, nên phiếu bị bác không bị xoá (CC Ch06 §06.6).

## Khuôn phiếu

Mỗi phiếu là một khối `text`; dòng đầu là tiêu đề, mỗi mục một dòng bắt đầu bằng số mục. Mục 5 phải có
`ngày thử: YYYY-MM-DD`; mục 7 phải có `người ký <tên> — ngày YYYY-MM-DD`, ngày ký **trước** ngày thử.

```text
PHIẾU GIẢ THUYẾT — GT-{{nnn}}
1 Tiêu đề: {{số thứ tự + tên tham số hình thể}} — phần tử {{WFP/LSS/C, mã trạng thái}}
2 NẾU: {{tham số hình thể GHI ĐƯỢC LÊN BẢN VẼ}} = {{giá trị}} | Đối chứng: {{mẫu đối chứng, chỉ khác đúng tham số này}}
3 THÌ: {{đại lượng chức năng đo được}} {{hơn/kém}} đối chứng, ngưỡng {{…}}
4 VÌ: {{một cơ chế vật lý duy nhất}}
5 KIỂM: {{bàn thử, số mẫu, điều kiện biên, khoảng tin cậy chọn TRƯỚC, người đọc kết quả}}; ngày thử: {{YYYY-MM-DD}}
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: {{số hoặc hiện tượng kỳ vọng}}; người ký {{tên}} — ngày {{YYYY-MM-DD}}
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: {{thấp/trung/cao}} ({{lý do}}) / {{thấp/trung/cao}} ({{lý do}})
9 NẾU BỊ BÁC: {{lặp trong pha | lặp xuyên cổng → mở lại quyết định cổng nào}}; điểm đầu tư gần nhất {{…}}
```

## Điều kiện hợp lệ

- **NẾU là tham số, không phải tác dụng.** Không đặt ma sát, mòn, độ kín, «tín hiệu» ở mục 2; phải viết tham số đứng sau tác dụng ấy (lớp phủ, độ nhám, góc, khe) (CC Ch06 §06.6).
- **Đổi đúng một biến.** Mục 2 chỉ một tham số đổi so với đối chứng; đổi hai thứ cùng lúc thì phiếu giải được vấn đề mà không sinh tri thức (CC Ch06 §06.7).
- **Có đối chứng.** Không có đối chứng thì chỉ có một con số, không có một so sánh; mục 3 là thay đổi *so với* đối chứng (CC Ch06 §06.6).
- **VÌ phải viết được, và chỉ một cơ chế.** Không viết được VÌ nghĩa là chưa có mô hình: quay về phân tích, không lên bàn thử (CC Ch06 §06.6). Hai cơ chế thì tách thành hai phiếu (CC Ch13 §13.7).
- **Dự đoán viết trước, có chữ ký và ngày trước ngày thử**: «không lập giả thuyết trước thì rất dễ đọc ra quan hệ từ những kết quả vô nghĩa» (CC Ch06 §06.2).
- **Ghi trước quan sát nào sẽ khác đi nếu giả thuyết sai**, và người đọc kết quả không phải người lập phiếu khi làm được — người lập hay đọc bằng chứng phản bác thành xác nhận (CC Ch06 §06.6).
- **Không ngoại suy** ra ngoài dải đã kiểm (CC Ch06 §06.6).
- Phiếu gắn vào đúng một phần tử của mô hình C&C²; khó gắn là dấu hiệu chỗ ấy phải làm mịn mô hình (CC Ch09 §09.5).

## Khuôn kế hoạch thử trên bàn thử

Gọi đúng tên câu hỏi trước khi chọn phép thử: thử thăm dò (hướng này có hiểu được không), thực nghiệm (tham số nào
ảnh hưởng — đây là chỗ phiếu chạy), kiểm chứng (khớp đặc tả, có/không), xác nhận (đáp ứng người dùng) (CC Ch08 §08.2).
Kế hoạch có dòng «đổi tham số X giữa các mẫu» thì không thể là kiểm chứng (CC Ch08 §08.2).

| Mục kế hoạch | Ghi gì | Nguồn |
|---|---|---|
| Đại lượng mục tiêu | Đại lượng chức năng đo được, đo ở giao diện có sẵn nếu chỗ trong không đặt được cảm biến; ghi ca thử cụ thể | (CC Ch10 §10.1) |
| Bàn thử | Dựng từ giả thuyết, không dựng trước: «các bệ thử này được dựng từ những giả thuyết về quan hệ hình thể – chức năng nằm bên dưới chúng, và có phương tiện đo chức năng» | (CC Ch10 §10.2) |
| Mẫu | Prototype chuyên dụng cho đúng một quan hệ là đủ; tìm trước một vật mà tham số cần hỏi tự nó biến thiên (phân tán tự nhiên của hàng có sẵn) | (CC Ch08 §08.1) |
| Đối chứng | Chế tạo cùng cách, cùng vật liệu, chỉ khác tham số đang kiểm; đo đối chứng ở đầu và cuối loạt để bắt trôi | (CC Ch10 §10.3) |
| Đổi một biến | «điều quyết định cho thực nghiệm là các vít đem thử chỉ khác nhau ở đúng tham số hình thể đang kiểm»; đo mọi tham số nghi để chắc các tham số kia gần như nhau | (CC Ch08 §08.1) |
| Phân nhóm | Phân nhóm theo **tham số** trước, viết dự đoán, rồi mới đo kết quả; nhóm theo kết quả rồi nhìn tham số dễ dính tương quan giả | (CC Ch08 §08.1) |
| Dải | Dải tham số và dải điều kiện biên ghi trước; kết luận chỉ đúng trong dải ấy | (CC Ch06 §06.6) |
| Lặp và khối | Đủ lần lặp để thấy độ phân tán; khối hoá theo lô, người, ngày | (CC Ch13 §13.7) |
| Người đọc kết quả | Người đọc kết quả ≠ người lập phiếu; ghi tên cả hai | (CC Ch06 §06.6) |
| Thẻ thử | Mỗi lần thử một thẻ: số chuỗi, tham số cố ý đổi (hoặc «không»), đại lượng đo, kết quả, quyết định | (CC Ch09 §09.2) |

## Định tuyến độ tin × tầm ảnh hưởng

Độ tin là lòng tin chủ quan; tầm ảnh hưởng là việc phỏng đoán bị bác sẽ có nghĩa gì cho thiết kế. Hai trục độc lập,
không cộng thành một số. Sách cho điều kiện và ba đường: «chỉ khi tầm ảnh hưởng thấp và/hoặc độ tin cao thì mới có thể hợp lý khi thiết kế trên những phỏng đoán chưa kiểm» (CC Ch06 §06.2).

Ma trận dưới là cách bộ skill sắp ba đường của sách vào hai trục *(quy ước bộ skill, sách không lập ma trận này)*. Hàng tầm ảnh hưởng cao mặc định đi đường 3 ở cả hai ô, vì khi tầm ảnh hưởng tối đa, độ tin cao không phải lý do bỏ kiểm — độ tin là chủ quan (CC Ch06 §06.2).

| | Độ tin cao | Độ tin thấp |
|---|---|---|
| **Tầm ảnh hưởng thấp** | Đường 1–2: dùng phỏng đoán, ghi nhãn | Đường 2: lý giải nhóm, có một người được giao vai phản biện |
| **Tầm ảnh hưởng cao** | **Đường 3 (mặc định): phiếu 9 mục + phép thử**; chỉ hạ xuống đường 2 khi CEO ký lý do trên phiếu | **Đường 3: phiếu 9 mục + phép thử trên bàn thử** |

- Ba đường lấy từ sách; đường 1 (phỏng đoán chưa nghĩ lại) gần như không nên, vì sai rồi thì không học được gì (CC Ch06 §06.2).
- Phỏng đoán chạm an toàn con người mặc định đi đường 3, bất kể độ tin (CC Ch06 §06.2).
- Phiếu nào nếu bị bác sẽ mở lại một quyết định cổng thì lên trước trong thứ tự kiểm, bất kể trục kia (CC Ch09 §09.6).
- Thứ tự kiểm khi cải tiến: chỗ đổi hình thể hay đổi nguyên lý trước, rồi phần mang sang đã chỉnh, rồi phần mang sang nguyên mà Connector đã đổi (CC Ch09 §09.6).

## Phiếu mẫu đã điền

Cơ cấu công khai: nắp gài (snap-fit) của một hộp nhựa đậy tay. Người ký, ngày và số là minh hoạ, không phải hồ sơ
dự án.

```text
PHIẾU GIẢ THUYẾT — GT-001
1 Tiêu đề: 001 góc mặt rút của móc gài — phần tử A:móc//gờ (S3 tháo)
2 NẾU: góc mặt rút của móc gài α = 45° | Đối chứng: α = 30°, cùng vật liệu, cùng khuôn in, chỉ khác góc
3 THÌ: lực tháo nắp bằng tay lớn hơn đối chứng, vượt ngưỡng ghi ở mục 7
4 VÌ: mặt rút dốc hơn làm thành phần lực đẩy cần móc ra ngoài nhỏ đi, nên cần móc phải uốn nhiều hơn mới nhả
5 KIỂM: mười nắp mỗi biến thể trên gá kéo thẳng, đo lực tháo bằng lực kế, cùng nhiệt độ phòng, đối chứng đo đầu và cuối loạt; người đọc kết quả Kỹ thuật viên B; ngày thử: 2026-11-20
6 KẾT QUẢ + khuyến nghị: chưa có — điền sau ngày thử, kèm dải đã kiểm
7 DỰ ĐOÁN VIẾT TRƯỚC: lực tháo trung bình của biến thể 45° lớn hơn đối chứng ít nhất 20%; người ký Kỹ sư A — ngày 2026-10-20
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: trung (cơ chế mặt nghiêng quen, chưa đo trên vật liệu này) / thấp (sửa khuôn in rẻ, đảo lại được)
9 NẾU BỊ BÁC: lặp trong pha — đổi chiều dài cần móc ở phiếu GT-002; không mở lại quyết định cổng nào; điểm đầu tư gần nhất là ngày đặt khuôn ép
```
