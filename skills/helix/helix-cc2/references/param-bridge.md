# Cầu nối tham số hình thể ↔ thông số chức năng (khối C3)

> Reference dùng chung của bộ `helix-cc2`, dùng ở C3 (bảng tham số) và C4 (chọn tham số nhạy nhất để viết phiếu).
> Nguồn: CC = *Mô hình C&C² và giả thuyết kết cấu*. Bảng C3 được `scripts/cc2_sheet_lint.py --kind params` chặn khi
> ô Nhãn hay ô Nguồn số trống.

## Tham số, không phải tác dụng

- Ba loại tính chất phải tách: tính chất **chức năng** (thời gian, tỉ lệ hỏng — cái khách đo), tính chất **tác dụng** (lực, mô-men qua một WFP), tính chất **hình thể** (hình học, vật liệu của mặt và LSS — cái người vẽ đặt) (CC Ch04 §04.5).
- Cột *Tham số hình thể* chỉ chứa thứ ghi được lên bản vẽ: góc, chiều dài, khe hở, độ nhám, lớp phủ, vật liệu. Ma sát, độ kín, «tín hiệu mạnh hơn» là tác dụng; nguyên văn: «vì ma sát là một tác dụng sinh ra từ các tham số hình thể ở cặp bề mặt làm việc» (CC Ch06 §06.6).
- Phép thử ba giây: viết được giá trị của ô ấy lên bản vẽ không? Không được thì đó là tác dụng, phải tìm tham số đứng sau nó (CC Ch06 §06.6).
- Một mối ghép ma sát luôn kèm một dòng `giả định` cho hệ số ma sát và tham số đứng sau nó (cặp vật liệu, lớp phủ, độ nhám) (CC Ch13 §13.2).

## WSPO / WSPA

- C&C² chỉ ra tương tác phải xảy ra ở *đâu* nhưng chỉ dẫn ít về hình học của nó nên thiết kế ra sao — «khoảng trống tổng hợp». Hai thuộc tính vectơ của WFP lấp một phần: **WSPO** (hướng, theo pháp tuyến) và **WSPA** (diện tích chiếu lên ba mặt phẳng toạ độ) (CC Ch13 §13.2).
- Hai nước đi định lượng: đổi hướng/diện tích WFP (đổi góc truyền lực, đổi áp lực bề mặt = lực chia diện tích) và đổi thể tích, diện tích, chiều dài LSS (cánh tay đòn, mô-men uốn, độ cứng vững) (CC Ch13 §13.2).
- Phép đo tối thiểu: với WFP đang nghi, vẽ pháp tuyến và ghi diện tích chiếu; với LSS đang nghi, ghi chiều dài làm cánh tay đòn. Hai dòng ấy đủ viết vế *Thì* bằng chiều và dấu (CC Ch13 §13.2).
- Giới hạn tự nêu của nguồn: độ nhám, cặp vật liệu, lớp phủ, bôi trơn, độ cứng, hành vi theo nhiệt nằm ngoài phạm vi WSPO/WSPA; chưa có kiểm định thực nghiệm trên kỹ sư thật (CC Ch13 §13.2).

## Độ nhạy và thứ hạng

- Một biến điều khiển *được lượng hoá* cần bốn thông tin: **dấu** (tăng thì chức năng tốt lên hay xấu đi), **thứ hạng** trong các tham số nghi, **trạng thái** mà dấu và thứ hạng ấy đúng, **công sức đổi** trên sản phẩm. Thiếu ô thứ tư thì đội đổi cái dễ đổi, không phải cái đáng đổi (CC Ch13 §13.6).
- Con số chuyên gia ghi trong ma trận ảnh hưởng chỉ xếp thứ tự giả thuyết, không phản ánh độ mạnh thật (CC Ch13 §13.6).
- Một ngưỡng tham số lượng hoá đúng chỉ là điều kiện *cần* cho chức năng con của nó, không *đủ* cho chức năng tổng (CC Ch13 §13.1).
- Sau khi đánh nhãn, xếp hạng xem quan hệ nào đang gánh quyết định lớn nhất (CC Ch06 §06.1). Phần xếp hạng theo cái gánh quyết định là của sách; phần chọn NHẠY là của bộ skill. Tiêu chí NHẠY *(quy ước bộ skill)*: (1) ứng viên là tham số có Nhãn không phải `tri thức`, vì quan hệ `tri thức` đã được chứng minh và không cần phiếu giả thuyết; (2) trong các ứng viên, tối đa 3 tham số có hạng tốt nhất (hạng 1 là tốt nhất) là `NHẠY`; (3) nếu có hơn 3 ứng viên thì phần còn lại giữ hạng và không `NHẠY`; (4) ngoại lệ: tham số mà giá trị sai làm mất an toàn được thêm `NHẠY` ngoài trần 3 và phải ghi lý do «an toàn». Đó là các tham số đi tiếp sang phiếu C4.
- Dưới sai lệch: cùng một thay đổi đặc điểm có thể tốt dưới sai lệch này mà vô ích dưới sai lệch khác; ghi sai lệch tới hạn (dung sai, mòn, nhiệt) cạnh mỗi tham số nhạy (CC Ch14 §14.3).
- Ba loại nhiễu gắn với phần tử: nhiễu ngoài (nhiệt độ) ở Connector, nhiễu trong (mòn) ở WFP đổi theo thời gian, nhiễu giữa các sản phẩm ở dung sai và độ phân tán của LSS (CC Ch14 §14.2).
- Mỗi dung sai trên bản vẽ là một giả thuyết rằng WFP đã chế tạo đủ gần WFP đã thiết kế để chức năng không đổi (CC Ch04 §04.7).

## Dải đã kiểm

- Không ngoại suy ra ngoài dải đã kiểm: kết quả một giả thuyết thường không đúng ra ngoài quan hệ đã thử — không được giả định «cứng hơn nữa sẽ tốt hơn nữa» (CC Ch06 §06.6).
- Mỗi con số mang theo trạng thái, dải hiệu lực và khối thử (lô, người, ngày) (CC Ch13 §13.7).
- Đại lượng mục tiêu thiết kế là một mệnh đề có điều kiện: với ca thử này, trên bệ này, so với đối chứng này, giá trị này của tham số này làm mục tiêu kia tốt hơn (CC Ch10 §10.3).
- Không biết tải tuyệt đối vẫn so tương đối được: hai phương án dưới cùng tải giả định và cùng biên cho «hơn / bằng / kém»; phép so không trả lời «đủ bền» (CC Ch13 §13.1).

Thang lượng hoá (leo từng nấc, chỉ khi quyết định cần) (CC Ch13 §13.7):

| Nấc | Trả lời được | Đầu ra trong bảng C3 |
|---|---|---|
| 0 — định tính | WFP, LSS, Connector nào tham gia, ở trạng thái nào | Cột *Phần tử* và *Tham số hình thể*; *Ước lượng* = `—` |
| 1 — có hướng | Đổi theo chiều nào thì chức năng tốt lên | *Chiều ảnh hưởng* có dấu và mã trạng thái |
| 2 — có thứ hạng | Trong vài tham số, cái nào đổi trước | Thứ hạng trong *Chiều ảnh hưởng* |
| 3 — so tương đối | Phương án mới hơn / bằng / kém đối chứng cùng biên | *Ước lượng* dạng so sánh; nấc mặc định |
| 4 — tuyệt đối | Đủ bền, đủ cứng, với bao nhiêu dư | Chỉ khi chạm biên an toàn hay chứng nhận |

Trước khi lượng hoá, ghi ba ô: một đại lượng chức năng đo được, một tham số hình thể nghi ngờ, một phương án đối chứng; ba ô trống thì chưa đến lúc lượng hoá (CC Ch13 §13.1).

## Khuôn bảng C3

Mỗi dòng một tham số gắn với đúng một phần tử (WFP, LSS hay Connector) kèm mã trạng thái (CC Ch13 §13.7). Ô *Nhãn*
là một trong `tri thức` / `phỏng đoán` / `giả định`; ô *Nguồn số* bắt đầu bằng `đo được` / `suy ra (từ …)` /
`chưa biết` (xem `cc2-core.md`). Nhãn `tri thức` không đi với `chưa biết` *(quy ước bộ skill)*.

NHẠY = ô "Chiều ảnh hưởng" bắt đầu bằng `NHẠY` (quy ước bộ skill); C4 lấy đúng các dòng này.

| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |
|---|---|---|---|---|---|---|---|
| {{A:WFP1 (S2)}} | {{góc, chiều dài, khe…}} | {{đại lượng đo được}} | {{↑/↓, thứ hạng}} | {{giá trị hoặc —}} | {{min–max}} | {{tri thức/phỏng đoán/giả định}} | {{đo được / suy ra (từ …) / chưa biết}} |

Ví dụ điền (nắp gài công khai, không số thật):

| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng | Ước lượng | Khoảng chọn | Nhãn | Nguồn số |
|---|---|---|---|---|---|---|---|
| A:móc//gờ (S2 gài) | góc mặt vào của móc | lực đóng nắp bằng tay | góc tăng → lực đóng tăng; hạng 2 | — | chọn sau phép so | phỏng đoán | chưa biết |
| A:móc//gờ (S3 tháo) | góc mặt rút của móc | lực tháo nắp | góc tăng → lực tháo tăng; hạng 1 | so tương đối với góc hiện dùng | quanh góc hiện dùng | phỏng đoán | suy ra (từ phân tích lực trên mặt nghiêng) |
| A:cần móc (LSS) | chiều dài cần đàn hồi | lực đóng, biến dạng còn lại sau nhiều lần mở | dài hơn → lực đóng giảm; hạng 3 | — | giới hạn bởi không gian nắp | giả định | chưa biết |
