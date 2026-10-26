# C&C² lõi — từ vựng, bảy bước, giới hạn, phạm vi, nhãn

> Reference dùng chung của bộ `helix-cc2`. Nguồn: hai quyển nội bộ — **CC** = *Mô hình C&C² và giả thuyết kết cấu*,
> **TK** = *Thiết kế hiện thân*. Mỗi quy tắc ghi một trích nguồn dạng `(CC ChNN §NN.x)`. Lời văn là diễn ý; câu
> trong «…» là nguyên văn sách và được `scripts/cc2_ref_check.py` kiểm.

## Từ vựng

| Chữ | Nghĩa dùng trong bộ skill | Nguồn |
|---|---|---|
| **WFP** — cặp bề mặt làm việc | Hai bề mặt (rắn, hoặc mặt phân cách của chất lỏng, khí, trường) tiếp xúc và trao đổi năng lượng, vật chất hay thông tin. Chức năng sinh ra ở *cặp*, không ở một chi tiết | (CC Ch02 §02.3) |
| **LSS** — cấu trúc dẫn-đỡ | Thể tích nối đúng hai WFP và dẫn dòng giữa chúng. Một chức năng có thể có nhiều LSS; mỗi LSS chỉ có hai đầu | (CC Ch05 §05.3) |
| **Connector (C)** | Phần môi trường nằm ngoài vùng thiết kế nhưng có ảnh hưởng, đại diện bằng một mặt làm việc kèm mô hình của nó. Mỗi Connector là một lời hứa «phần này không liên quan», và lời hứa ấy có thể sai | (CC Ch04 §04.3) |
| **Mặt biên (BF)** | Bề mặt không làm việc ở trạng thái đang xét. Nhiều mặt *trông như* tiếp xúc chỉ là mặt biên; qua nhiều chu kỳ, mặt biên có thể thành mặt làm việc | (CC Ch04 §04.4) |
| **Trạng thái** | Khoảng thời gian mô hình không đổi; trạng thái mới bắt đầu khi số hay thuộc tính phần tử đổi. Nguyên văn: «một trạng thái là khoảng thời gian trong đó mô hình C&C² không đổi» | (CC Ch02 §02.3) |
| **Trạng thái logic** | Nhánh hành vi do một kích hoạt (thao tác, điều kiện ban đầu, tải lúc hệ không chạy) chọn, không do đồng hồ. Hỏi: hệ bắt đầu chu trình từ bao nhiêu điều kiện ban đầu khác nhau? | (CC Ch05 §05.1) |
| **Mô hình chuỗi** | Nhiều mô hình C&C² của các trạng thái, sắp theo thời gian và/hoặc theo logic | (CC Ch02 §02.8) |
| **Tác dụng** | Thứ sinh ra ở WFP/LSS/Connector (ví dụ ma sát). Tác dụng *không phải* tham số hình thể; tham số là cái ghi được lên bản vẽ | (CC Ch02 §02.3) |

Luật bộ tối thiểu: «một chức năng cần ít nhất hai cặp bề mặt làm việc nối bằng một cấu trúc dẫn-đỡ, mỗi cặp nối ra môi trường bằng một Connector» (CC Ch02 §02.4).

Quy ước đặt tên trên phiếu: chữ cái cho hệ, số nối chấm cho hệ con, `//` cho WFP, `~` cho LSS, `(S1)` cho trạng thái;
nhánh logic ghi ở đầu phiếu, không nhét vào tên phần tử (CC Ch05 §05.4).

## Bảy bước dựng mô hình

Bảy bước là *danh mục việc phải xong*, không phải thứ tự bắt buộc; thường lặp giữa (b) và (c) (CC Ch02 §02.6).

1. **(a) Ghi mục đích** dưới dạng câu hỏi về MỘT hiện tượng ở MỘT hệ, hỏi *đặc điểm nào*, không hỏi *sửa thế nào*. Mục đích viết thành lời giải là đã nhảy qua phân tích (CC Ch02 §02.6).
2. **(b) Định biên** trong không gian và thời gian. Biên có thể bắt đầu hẹp rồi nới, hoặc rộng rồi thu; đổi biên thì định lại Connector (CC Ch02 §02.7).
3. **(c) Chọn ảnh hệ lúc đang làm chức năng** — bản phác, mặt cắt CAD, ảnh mẫu thử; hình thể phải có mặt trong ảnh (CC Ch02 §02.6).
4. **(d) Lần dòng** năng lượng, vật chất, thông tin qua các phần tử để lộ phần tử chưa biết (CC Ch02 §02.6).
5. **(e) Gắn WFP, LSS, Connector lên ảnh hệ** theo ba giả thuyết nền; mỗi hình vừa một trang A4, không vừa thì vẽ thô hơn (CC Ch02 §02.7).
6. **(f) Tìm tham số hình thể liên quan đến chức năng** và viết quan hệ của chúng với chức năng: «pha này chỉ xong khi đã làm rõ một quan hệ giữa tham số hình thể liên quan đến chức năng và chính chức năng» (CC Ch02 §02.6).
7. **(g) Kiểm mô hình.** Mọi quan hệ vừa vẽ đều là phỏng đoán: «những quan hệ hình thể – chức năng đã nhận ra và vẽ vào mô hình lúc đầu đều chưa được kiểm chứng» (CC Ch02 §02.6).

Sau (g), tổng hợp dùng đúng danh sách tham số mà (f) đã tìm, rồi quay lại phân tích hình thể vừa tổng hợp (CC Ch04 §04.1).

## Giới hạn dùng và bằng chứng

- **Bằng chứng hiệu quả C&C² yếu, đọc như kỷ luật tư duy chứ không như phương pháp đã chứng minh.** Sách tự kết: dạy phân tích C&C² như một kỷ luật tư duy có lý do vật lý, «không như phương pháp đã được chứng minh hiệu quả» (CC Ch04 §04.12).
- Bậc bằng chứng cao nhất là II trên thang năm bậc, gần như toàn bộ do cùng một trục nghiên cứu tự đo, phần lớn trên sinh viên; chưa có nghiên cứu đối chứng độc lập, chưa có lần làm lại giữ nguyên điều kiện (CC Ch11 §11.9).
- Ở mức chi tiết, người mới bị ép dùng trọn quy trình có kết quả kém hơn làm theo trực giác; không giao người mới dựng mô hình mức chi tiết khi không có người kèm (CC Ch11 §11.3).
- Không chạy kỹ thuật nào nếu chưa viết được câu hỏi mà kỹ thuật ấy trả lời; đã chạy thì chạy đúng điều kiện của nó (CC Ch04 §04.11).
- Mô hình phải vẽ tay được; cần phần mềm mới vẽ nổi là đã vượt câu hỏi (CC Ch05 §05.5).
- Không chọn C&C² khi câu hỏi đã định lượng và mô hình tính đã đúng, hoặc khi chức năng nằm chủ yếu ở điện, phần mềm (CC Ch02 §02.12).
- Mỗi phiên của bộ skill mở bằng một dòng nhắc giới hạn này; mọi gợi ý ra đời dưới dạng giả thuyết có nhãn *(quy ước bộ skill)*.

## Phạm vi cứng

Chỉ dựng C&C² cho **chức năng quyết định giải pháp** cộng **tối đa 3 chức năng tới hạn** khác. Không mô hình hoá cả
sản phẩm. Con số 3 là quy ước của bộ skill; sách chỉ nói C&C² dùng khi gặp khó lớn hoặc cần tranh luận nhóm, tập
trung vào cái cốt yếu, và bảng kỹ thuật không phải danh sách tích ô (CC Ch04 §04.11). Thứ tự: chức năng tới hạn
trước, để nó được hiện thực và kiểm sớm hơn (CC Ch08 §08.7).

Mỗi chức năng con đi qua sàng ba ô, ghi một dòng lý do:

| Ô sàng | Khi nào | Nguồn |
|---|---|---|
| `dựng C&C²` | Câu hỏi là *đặc điểm hình thể nào quyết định hiện tượng*; hệ đổi trạng thái; hiện tượng không có trong mô hình tính; nhiều người phải cùng cãi trên một hình | (CC Ch02 §02.12) |
| `chỉ bảng tham số` | Quan hệ đã chuẩn hoá thành bảng hay công thức (ví dụ cặp bánh răng, lò xo trụ), chỉ cần chọn giá trị và dải | (CC Ch05 §05.5) |
| `không áp dụng` | Chức năng nằm chủ yếu ở mạch điện tử hay phần mềm; ghi `C&C²: không áp dụng, vì …` (xem `multidomain.md`) | (CC Ch02 §02.12) |

## Hai loại nhãn

Hai loại câu, hai bộ nhãn; không trộn.

**(a) Quan hệ nhân quả hình thể → chức năng** (mọi câu «do X nên Y»):

| Nhãn | Khi nào | Nguồn |
|---|---|---|
| `tri thức` | Quan hệ nhân quả đã chứng minh, kèm bằng chứng cụ thể (biên bản thử, hiện vật, phép tính có người ký). Một tương quan quan sát được chưa phải tri thức | (CC Ch06 §06.1) |
| `phỏng đoán` | Câu về cơ chế, có hướng nhân quả, có lý do, chưa kiểm, có thể sai | (CC Ch06 §06.1) |
| `giả định` | Điều được coi là đúng mà không hỏi lại, thường nằm ngầm (tải theo sổ tay, người lắp siết đúng lực) | (CC Ch06 §06.1) |

Mô hình bao giờ cũng chứa phần chưa kiểm: «ngoài những tri thức ấy, mô hình luôn chứa cả phỏng đoán và giả định về quan hệ hình thể – chức năng» (CC Ch06 §06.1).

**(b) Thuộc tính của một cặp hay một trạng thái** (khe hở, xử lý nhiệt, trình tự lắp, trạng thái mòn):

| Nhãn | Khi nào | Nguồn |
|---|---|---|
| `đo được` | Có phép đo, ghi cách đo | (CC Ch02 §02.9) |
| `suy ra (từ …)` | Suy từ một nguồn hay phép tính có tên; ghi nguồn trong ngoặc | (CC Ch02 §02.9) |
| `chưa biết` | Không suy ra được. Đây không phải lỗi; sách đã báo trước có thứ không suy ra được trên vật hoàn chỉnh | (CC Ch02 §02.9) |

Một hồ sơ ghi đủ chi tiết mà không đánh dấu *phỏng đoán* nguy hiểm hơn hồ sơ thiếu, vì nó trông như tri thức (CC Ch05 §05.3).
