# Tìm chuẩn đối sánh theo chức năng (bước F4, khối BF)

Tệp này quy định cách tìm và ghi `<P>BF_Benchmark.md`. Mục đích: có ít nhất vài lời giải đã có người làm cho từng chức năng, mỗi lời giải được dịch sang chuỗi C&C², để đặt cạnh phương án của mình trong bảng chấm (cột `HC-<id>-<n>`). Chuẩn đối sánh là nguồn cảm hứng và thước so sánh, không phải lệnh sao chép.

## Truy vấn theo CHỨC NĂNG, không theo tên sản phẩm

Truy vấn bằng động từ chức năng và điều kiện (ví dụ `nhận xung va chạm đầu đạn trên bia nổi`, `giữ thân nổi thẳng đứng khi bị bắn`, `nối mô-đun tháo được kín nước`), cộng từ đồng nghĩa kỹ thuật, không bằng tên hãng hay tên sản phẩm. Tên sản phẩm chỉ xuất hiện ở kết quả. Lý do: tên sản phẩm chỉ cho ra thứ đã biết; truy vấn theo chức năng mới lộ ra lời giải cùng chức năng ở lĩnh vực khác (KL-R120: từ khoá kỹ thuật cộng từ đồng nghĩa, rồi thu hẹp bằng mã phân loại).

## Ba tầng nguồn, đi theo thứ tự

| Tầng | Nguồn | Cách làm | Nguồn trích |
|---|---|---|---|
| 1 | Hồ sơ dự án: RE, FTO, bản PDF sáng chế đã có trong thư mục dự án và vault | Đọc trước; ghi đường dẫn tương đối trong `Nguồn:` (ví dụ `RE/<Tên>/x.md`) | [ngoài sách] |
| 2 | Web qua Exa: `mcp__exa__web_search_exa` để tìm, `mcp__exa__web_fetch_exa` để đọc trang đã biết URL | Tìm theo chức năng; chỉ ghi nguồn đã mở đọc, ghi URL đầy đủ và ngày truy cập | [ngoài sách] |
| 3 | Sáng chế qua Exa trên Google Patents / Espacenet | Ưu tiên công bố trong 5 năm gần nhất; ĐỌC HÌNH VẼ, không chỉ đọc tóm tắt hay mô tả (KL-R121: đọc yêu cầu bảo hộ, không đọc ví dụ minh hoạ); ghi số sáng chế như `US 9,097,498 B2`, `CN116753779A` | [KL9 Ch16 §24.3.7] |

Cách đọc sáng chế ở tầng 3 theo sách KL9 Ch16 (mã dòng trong `kl9-gestaltung`): KL-R119 (tra cứu TRƯỚC khi chốt hình thể) [KL9 Ch16 §24.3.7], KL-R120 (từ khoá + từ đồng nghĩa + phân loại IPC, giới hạn thời gian) [KL9 Ch16 §24.3.7], KL-R121 (đọc claims) [KL9 Ch16 §24.3.7], KL-R122 và KL-R123 (né tránh thiết kế và bốn lối ra) [KL9 Ch16 §24.3.2.1], KL-R124 (độc quyền không phải quyền sử dụng) [KL9 Ch16 §24.2], KL-R125 (nguyên tắc lãnh thổ) [KL9 Ch16 §24.3.1]. Sáng chế chỉ có tóm tắt mà không mở được hình vẽ thì ghi nhãn `giả định` và nói rõ chưa đọc hình.

## Giới hạn và loại bỏ

- Tối đa 8 chuẩn đối sánh (HC) cho mỗi chức năng; nhiều hơn thì lint báo `TOO_MANY_BENCH`. Chọn theo độ sát chức năng và độ đọc được nguồn, không theo độ nổi tiếng.
- Dừng khi lời giải mới chỉ lặp lại một chuỗi C&C² đã có. Thiếu nguồn cho một chức năng thì ghi mục trống kèm lý do, không bịa.
- Không đưa nguồn chưa mở đọc. Không dán nguyên văn dài từ nguồn; viết lại bằng lời mình.

## Dịch mỗi giải pháp sang chuỗi C&C²

Mỗi HC phải kèm `Chuỗi C&C²:` viết bằng WFP (cặp bề mặt làm việc), LSS (cấu trúc dẫn-đỡ) và Connector (môi trường/phần tử nối ngoài cặp): ví dụ `WFP1 → LSS1 → Connector → WFP2`. Thiếu chuỗi thì `BENCH_NO_CHAIN`. Dựng chuỗi theo `tkht-rules § C&C² 7 bước dựng mô hình` và đọc sáng chế bằng bảng WFP/LSS/Connector của `reverse-engineering:references:cc2-lens`.

## Nhãn tri thức

Mỗi HC có `Nhãn:` thuộc đúng một trong ba giá trị: `tri thức` (đã kiểm: mở nguồn gốc, đọc hình, hoặc có đo), `phỏng đoán` (suy từ nguồn, chưa kiểm), `giả định` (lấy tạm, chưa có nguồn xác nhận). Giá trị khác thì `BAD_LABEL`. Mặc định cho sáng chế chưa kiểm bằng thử nghiệm là `phỏng đoán`.

## Cờ FTO

Khi một HC là sáng chế còn hiệu lực hoặc chuỗi C&C² của HC khớp đặc điểm trong yêu cầu bảo hộ, ghi thêm dòng `Cờ FTO:` nêu số sáng chế, lãnh thổ nghi ngờ và việc cần làm, rồi chuyển cho `ip-*` (ví dụ `ip-screen`) và quy trình FTO QP-02-06. BF KHÔNG phán định có vi phạm hay không, không kết luận sáng chế đã hết hiệu lực; cờ chỉ có nghĩa «cần người có thẩm quyền rà». Cờ FTO không chặn việc đưa HC vào bảng chấm làm chuẩn so sánh.

## Khuôn hồ sơ một giải pháp

Mỗi chức năng một mục `## F-<id> — <tên chức năng>`; mỗi giải pháp một mục `### HC-<F-id>-<n> — <tên>` với các trường dưới đây (lint đọc đúng các nhãn này):

```
# Chuẩn đối sánh

## F-<id> — <tên chức năng>

### HC-<id>-1 — <tên giải pháp>
- Nguồn: <URL đầy đủ | số sáng chế như US 9,097,498 B2 | đường dẫn tương đối RE/…>
- Truy cập: <YYYY-MM-DD>
- Nhãn: <tri thức | phỏng đoán | giả định>
- Chuỗi C&C²: <WFP1 → LSS1 → Connector → WFP2>
- Cờ FTO: <tuỳ chọn: số sáng chế; lãnh thổ; chuyển ip-* / QP-02-06>
```

Quy tắc trường: `Nguồn:` phải là URL, số sáng chế (US/EP/CN/WO/JP/KR/DE) hoặc đường dẫn có dấu `/` (thiếu thì `BENCH_NO_SOURCE`); `Truy cập:` đúng dạng `YYYY-MM-DD` (thiếu hoặc sai dạng thì `BENCH_NO_DATE`); số HC mỗi chức năng không quá 8. Mã `HC-<F-id>-<n>` dùng đúng làm tiêu đề cột `HC-…` trong bảng chấm (`scoring`).
