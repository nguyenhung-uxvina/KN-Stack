# Nước đi tổng hợp trên một chuỗi C&C²

> Reference dùng chung của bộ `helix-cc2`, dùng ở C1 (sinh ≥3 chuỗi khác nhau thật) và C2 (chuỗi → hình thể).
> Nguồn: CC = *Mô hình C&C² và giả thuyết kết cấu*; TK = *Thiết kế hiện thân*. Ví dụ đều là cơ cấu công khai,
> không thuộc sản phẩm nào của Xưởng. Ô ví dụ ghi *(ví dụ sách)* khi cơ cấu lấy từ sách, *(ví dụ minh hoạ)* khi
> là cơ cấu phổ thông người viết reference chọn để minh hoạ nguyên tắc ở cột Nguồn.

## Gốc của các nước đi

- Mọi cách định hình thể quy về ba phép: **thêm**, **bỏ** WFP hoặc LSS, hoặc **đổi** đặc điểm của chúng (CC Ch08 §08.7).
- Bản gốc năm 2005 tách «đổi» thành hai: đổi tính chất WFP và đổi tính chất LSS; bộ skill giữ bốn ô ấy và thêm các nước đi theo biên, trạng thái, miền (CC Ch08 §08.7).
- Ba phép dùng được ở mọi mức tỉ lệ — vi cấu trúc, hình học ren, cả cụm — vì mô hình có tính phân hình (CC Ch02 §02.4).
- Tổng hợp cặp, không tổng hợp mặt: «khi lập bản vẽ chi tiết đúng yêu cầu chế tạo, người ta dễ mất tầm nhìn vào các tương tác» (CC Ch08 §08.7).
- WFP và LSS trước, mặt biên và kết cấu dư sau; chức năng tới hạn trước (CC Ch08 §08.7).
- Định *tính chất* của WFP mới (truyền lực hay thông tin gì, chuyển động tương đối, hướng lực so với mặt) trước khi vẽ hình dạng, và đánh dấu trước *mặt nào cấm* (CC Ch08 §08.7).
- Mỗi nước đi sinh một hình thể mới, tức một giả thuyết mới; nó lại phải qua phiếu và phép thử (CC Ch08 §08.7).
- Mỗi nguyên tắc hiện thân chỉ *gợi ra* một thay đổi ứng viên; nguyên tắc là chiến lược để chọn, đúng trong điều kiện nhất định (TK Ch06 §06.1).
- Ba chuỗi trong C1 phải khác nhau ở cách sắp WFP/LSS/Connector, không chỉ khác kích thước; đổi một con số là việc của C3, không phải một chuỗi mới (CC Ch08 §08.7).

## Các nước đi

| Nước đi | Làm gì trên chuỗi | Ví dụ cơ cấu công khai | Câu hỏi bắt buộc | Nguồn |
|---|---|---|---|---|
| **Thêm WFP** | Biến một mặt biên hay kết cấu dư thành mặt làm việc; thêm một cặp mới cho chức năng mới | Trục khuấy cần nâng hạ khi đang chạy: tiếp xúc trượt chỉ đẩy, không kéo, nên chiều lên và chiều xuống cần hai WFP riêng — ra một dạng ổ trượt kiểu càng sang số *(ví dụ sách)* | Cặp mới truyền gì, theo chiều nào; chiều ngược lại do cặp nào gánh? | (CC Ch08 §08.7) |
| **Bớt WFP** | Bỏ một cặp thừa hay cặp gây hại; thường chỉ thấy khi biết cặp ấy xuất hiện ở trạng thái nào | Khớp tự do con lăn kẹp: đổi góc một mặt để mặt thứ ba không còn cọ ở trạng thái chạy *(ví dụ sách)* | Bỏ cặp này thì chức năng của nó chuyển sang đâu, hay chấp nhận mất? | (CC Ch05 §05.2) |
| **Tách WFP / tách vai** | Giao mỗi chức năng con cho một vật mang riêng; một cặp đang làm hai việc thành hai cặp | Mối ghép ren: một mặt giữ lực kẹp, một chi tiết khác (chốt định vị) giữ vị trí — mỗi chi tiết một chức năng *(ví dụ minh hoạ)* | Hai chức năng cũ có hạn chế, cản trở nhau không; số chi tiết tăng có bù được không? | (TK Ch06 §06.8) |
| **Gộp WFP / gộp chi tiết** | Gộp nhiều chi tiết thành một khối liền; bỏ lớp trung gian | Nắp gài (snap-fit) thay vít: liên kết hình học được bỏ, thay bằng một LSS đàn hồi trên chính nắp *(ví dụ sách, heuristic 2005 ở CC Ch08 §08.7)* | Phần tử bị bỏ đang gánh gì (cách điện, cản nhiệt, giảm rung); chức năng ấy có chỗ mới trên phiếu chưa? | (CC Ch15 §15.2) |
| **Đổi LSS** | Đổi thể tích, chiều dài, độ cứng vững của dẫn-đỡ; rút ngắn đường lực | Kẹp lò xo (spring clip): chiều dài và tiết diện cần đàn hồi quyết lực kẹp; bập bênh: chiều dài LSS là cánh tay đòn *(kẹp lò xo: minh hoạ; bập bênh: ví dụ sách)* | Rút ngắn có làm tăng tải trên WFP nào? Dòng lực có còn khép kín? | (CC Ch13 §13.2) |
| **Đổi tính chất WFP** | Đổi hướng (WSPO), diện tích (WSPA), vật liệu, lớp phủ của cặp | Ổ trượt: đổi vật liệu bạc hay độ nhám trục; nêm hãm: đổi góc nêm để đổi lực pháp tuyến *(ổ trượt: minh hoạ; nêm hãm: ví dụ sách, CC Ch13 §13.2)* | Đổi này có kéo theo mục tiêu mới ở Connector và một tác dụng phụ mới không? | (CC Ch08 §08.7) |
| **Dời Connector** | Mở biên (Connector → WFP + LSS) hoặc thu biên (WFP + LSS → Connector mới); dời chỗ hệ chạm môi trường | Bản lề cửa: dời điểm bắt từ khung gỗ sang một tấm đế kim loại riêng, để tải vào khung theo diện *(ví dụ minh hoạ)* | Connector mới hứa «phần ngoài không liên quan» — lời hứa ấy kiểm bằng gì? | (CC Ch04 §04.3) |
| **Đổi trạng thái** | Thêm, bỏ, đổi thứ tự trạng thái; thêm một nhánh logic có chủ ý (cữ chặn, khoá) | Chốt lò xo hai trạng thái (lưỡng ổn) thay một kẹp ma sát: nhảy dứt khoát giữa *mở* và *đóng*, không dừng nửa vời *(ví dụ minh hoạ; lưỡng ổn ở TK Ch07 §07.3)* | Hệ bắt đầu chu trình từ bao nhiêu điều kiện ban đầu; nhánh nào chạm an toàn người? | (CC Ch05 §05.1) |
| **Đổi miền** | Đổi nguyên lý ở một WFP: cơ → quang, cơ → điện; WFP thành chỗ chuyển đổi năng lượng | Rào sáng chung: thay một công tắc tiếp xúc cơ bằng rào sáng xuyên tia, phản xạ ngược, hay bóng đổ lên mảng thu — mức nguyên lý, không số *(ví dụ minh hoạ)* | Chỗ đổi miền là WFP nào; phía sau nó C&C² còn dùng được không (xem `multidomain.md`)? | (CC Ch15 §15.1) |

## Luật dùng

- Mỗi lần **bỏ** hay **gộp**, ghi một dòng: chức năng của phần tử bị bỏ chuyển sang đâu, hay được chấp nhận mất (CC Ch15 §15.2).
- Khi hai nguyên tắc kéo ngược nhau (tách vai làm dài đường dung sai; thêm chỗ chỉnh làm thêm tham số), quyết bằng sai lệch tới hạn của chính sản phẩm, không bằng cộng điểm (CC Ch14 §14.4).
- Khi cải tiến thế hệ sau, giữ một chuỗi «hình thể hiện có, sửa tối thiểu»; chỉ đổi những tham số cần cho chức năng mới hay đã đổi (CC Ch09 §09.6).
- Mô hình loại trừ hình thể sai rất tốt (*mặt này cấm*); chọn trong các hình thể còn lại vẫn là việc của kinh nghiệm và phép thử, nên C2 trả 2–3 phương án, không trả một đáp án (CC Ch08 §08.7).
- Đổi tính chất (góc, chiều dày, vật liệu) cần ít nhất biết chiều và thứ tự ảnh hưởng; chỉ thêm hay bỏ WFP thì mô hình định tính là đủ (CC Ch13 §13.1).
