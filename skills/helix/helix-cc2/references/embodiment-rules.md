# Chỉ mục quy tắc hiện thân → câu hỏi kiểm hình thể

> Reference dùng chung của bộ `helix-cc2`, dùng ở C2 (mỗi phương án hình thể phải có lý do từ quy tắc) và ở CA
> (đọc ngược «vì sao hình học này»). Nguồn: TK = *Thiết kế hiện thân*, Ch04–Ch16. Lời văn là diễn ý; cột
> *Tham số bị khoá* là tham số hình thể mà quy tắc ấy buộc người thiết kế quyết.

Cách đọc chung: mỗi nguyên tắc là một giả thuyết đã có người kiểm, kèm điều kiện để nó đúng; nguyên tắc chỉ là chiến
lược để chọn, không phải luật (TK Ch06 §06.1). Quy tắc cơ bản *rõ ràng, đơn giản, an toàn* đứng trên nguyên tắc và
luôn đúng (TK Ch04 §04.1). Câu soát xét đổi từ «đã áp nguyên tắc nào chưa» sang «tác dụng gốc ở đây là gì, phần bổ sung
giao cho chi tiết nào» (TK Ch06 §06.1).

| Quy tắc | Câu hỏi kiểm hình thể | Tham số bị khoá | Nguồn |
|---|---|---|---|
| Rõ ràng — một đường truyền lực, một chức năng | Có LSS nào mang hai chức năng có độ lớn độc lập không? | Số và bố trí LSS trên đường lực | TK Ch04 §04.2 |
| Rõ ràng — không lắp ghép kép | Có phần tử «thêm cho chắc» tranh tải theo dung sai, hay mỗi mối ghép đúng một kiểu khớp? | Số mặt định vị, kiểu khớp của từng mối ghép | TK Ch04 §04.3 |
| Rõ ràng khi tính — ghi tải cả lúc không làm việc | Điều kiện tải đã gồm trạng thái nằm chờ, vận chuyển, khoang kín bị bịt? | Danh sách trạng thái tải, chiều tải | TK Ch04 §04.4 |
| Đơn giản — hình học tính được | So sánh «đơn giản hơn» đã ghi pha (chế tạo, lắp, dùng)? Có đối xứng khi không có lý do lệch? | Dạng hình học cơ bản, trục đối xứng | TK Ch04 §04.7 |
| An toàn — biện pháp trực tiếp trước, bảo vệ sau | Nguy cơ đã được bỏ bằng hình thể trước khi thêm cơ cấu bảo vệ? Có chỗ nào chỉ dẫn là biện pháp duy nhất? | Khe, mép, điểm kẹp giữa phần chuyển động | TK Ch05 §05.7 |
| An toàn — hỏng an toàn | Năng lượng đưa hệ về trạng thái an toàn có nằm sẵn trong hệ (lò xo, trọng lực)? | Vị trí và chiều của phần tử tích năng | TK Ch05 §05.4 |
| An toàn — cơ cấu bảo vệ kiểm được | Cơ cấu bảo vệ có kiểm được mà không cần nguy hiểm thật, có cấm tự khởi động lại? | Điểm thử, đường tiếp cận kiểm tra | TK Ch05 §05.9 |
| Ổn định vật nổi là tính chất hình thể | Bố trí đã khoá ổn định trước khi có số chưa (cái gì đặt cao, cái gì đặt thấp)? | Thứ tự bố trí khối lượng, chiều cao trọng tâm | TK Ch05b §05b.4 |
| Dòng lực khép kín, ngắn, trực tiếp | Chuỗi WFP–LSS có quay về qua một Connector có tên? Bao nhiêu LSS giữa chỗ nhận tải và chỗ trả tải? | Chiều dài đường lực, số LSS | TK Ch06 §06.2 |
| Tránh đổi hướng gấp và đổi tiết diện đột ngột | LSS nào đổi hướng hay đổi tiết diện gấp trên đường lực? | Bán kính chuyển tiếp, quy luật đổi tiết diện | TK Ch06 §06.4 |
| Biến dạng khớp nhau | Ở mỗi mối ghép trên đường lực, biến dạng hai bên cùng chiều, ngược chiều hay chưa biết? | Độ cứng vững tương đối hai phía mối ghép | TK Ch06 §06.6 |
| Cân bằng lực tại chỗ sinh ra | Mọi lực đi kèm (dọc trục, mô-men lật) đã được khép ngay tại nguồn, hay để đi qua ổ và khung? | Bố trí đối xứng, phần tử bù | TK Ch06 §06.7 |
| Phân chia nhiệm vụ | Mỗi vật mang gánh bao nhiêu chức năng; các chức năng có cản trở nhau? Nhiều phần tử chia tải dựa vào điều kiện chia đều nào? | Ranh giới chức năng giữa các chi tiết | TK Ch06 §06.8 |
| Tự tăng lực | Tác dụng hỗ trợ cùng chiều, bằng không hay ngược chiều với tác dụng gốc, ở *mỗi* chiều tải? | Hình học đặt lực hỗ trợ (góc nêm, cánh tay đòn) | TK Ch07 §07.1 |
| Ổn định / lưỡng ổn | Lực làm việc đẩy hay kéo phần tử có thể nghiêng? Cần nhảy dứt khoát thì đã so độ dốc hai đặc tính, biết khoảng trễ? | Chiều dài dẫn hướng, điểm đặt lực, đặc tính lò xo | TK Ch07 §07.3 |
| Thiết kế ít lỗi — bất biến, bù, chống lắp sai | Kích thước dung sai chặt nào bỏ được, làm bất biến được, chỉnh sau lắp được? Người không thiết kế có lắp sai được không? | Mặt chuẩn định vị, hình dạng chống lắp ngược | TK Ch07 §07.4 |
| Giãn nở — một điểm cố định | Cụm có đúng một điểm cố định, dẫn hướng còn lại nằm trên tia đối xứng biến dạng thật? | Vị trí điểm cố định, hướng dẫn trượt | TK Ch08 §08.1 |
| Giãn nở tương đối hai vật liệu | Chênh hệ số giãn nở giữa hai vật liệu ghép đã tính theo kích thước thật? | Khe bù, dạng lỗ (tròn hay rãnh) | TK Ch08 §08.2 |
| Rão và chùng ứng suất | Mối ghép căng đã tính mất lực căng do rão và lún, hay giả định lực siết giữ nguyên mãi? Số mặt tiếp xúc đã tối thiểu? | Số mặt tiếp xúc, độ nhám mặt tì | TK Ch08 §08.3 |
| Ăn mòn tiếp xúc | Có cặp kim loại khác điện thế chạm nhau trong môi trường ẩm? | Lớp cách điện, cặp vật liệu | TK Ch09 §09.4 |
| Ăn mòn khe và hình dạng | Có khe hẹp, khe gốc mối hàn không thông khí; hình dạng có đọng nước? | Kiểu mối hàn, khe ghép, lỗ thoát | TK Ch09 §09.7 |
| Ăn mòn do cọ xát | Có chuyển động tương đối nhỏ dưới áp lực giữa hai mặt ghép? Đã thử loại bỏ hẳn chuyển động (treo đàn hồi) trước khi đổi sang vật liệu cứng hơn? | Độ cứng vững mối ghép, kiểu khớp | TK Ch09 §09.5 |
| Mài mòn — sơ cấp trước, thứ cấp sau | Chuyển động trượt có chuyển được sang ma sát lưu chất hay khớp đàn hồi? Mặt dễ mòn có được tách thành chi tiết rẻ, dễ thay, có dấu báo mòn? | Kiểu khớp, chi tiết hao mòn tách riêng | TK Ch09 §09.9 |
| Kết cấu tấm — dòng lực và độ cứng vững | Lực vào tấm theo diện hay theo điểm? Đã thử gân, gập mép, đóng tiết diện trước khi tăng bề dày? | Gân, mép gập, bề dày tấm | TK Ch10 §10.2 |
| Kết cấu tấm — gộp chi tiết | Có thể thay một mối hàn bằng một đường gập, gộp bớt chi tiết rời? | Số chi tiết, đường gập | TK Ch10 §10.3 |
| Composite — đưa tải vào | Điểm tải cao có phụ kiện kim loại phân tải ra toàn tiết diện, hay đưa lực vào một điểm trên lớp vật liệu? | Phụ kiện đưa tải, diện tích phân tải | TK Ch11 §11.5 |
| Composite — hướng sợi và tiếp xúc kim loại | Hướng sợi gán theo loại phần tử chưa? Chỗ chạm nhôm/thép có lớp cách điện trên bản vẽ lắp đầu tiên? | Hướng sợi, lớp cách điện | TK Ch11 §11.4 |
| Chế tạo — hình thể quyết định công nghệ | Chi tiết thuộc nhóm công nghệ nào; xưởng có máy cho nhóm đó? | Dạng phôi, nhóm công nghệ | TK Ch12 §12.1 |
| Chế tạo — bố cục theo sản lượng | Phân tách, liền khối, hỗn hợp hay khuôn-mẫu đã chọn theo sản lượng và số biến thể thật, không theo thói quen dự án trước? | Số chi tiết, cách chia cụm lắp | TK Ch12 §12.4 |
| Hàn — ba tiêu chí | Vật liệu hàn được, hình thể hợp ứng suất thật, thi công được qua chuẩn bị–hàn–hoàn thiện — đã kiểm cả ba, hay mới một hai? | Vật liệu, kiểu mối hàn, đường tiếp cận mỏ hàn | TK Ch13 §13.1 |
| Hàn — tránh mối hàn tập trung, giao nhau | Có nhiều mối hàn chồng hay giao nhau ở một nút khung, nơi ứng suất dư cộng dồn? | Vị trí và khoảng cách các mối hàn | TK Ch13 §13.2 |
| Dán | Hình học mối dán đẩy tải vào tâm hay để một mép chịu bóc? | Diện tích dán, dạng mối | TK Ch13 §13.3 |
| Dung sai — chặt đến mức cần, rộng đến mức có thể | Dung sai từng chi tiết có chặt hơn mức cần? Chuỗi dài nhất đã có mặt chỉnh để bẻ gãy? | Dung sai, mặt chỉnh | TK Ch14 §14.6 |
| Lắp ráp — giao diện sống qua lắp | Vít chỉnh, điểm đo còn tiếp cận được sau khi ghép, đã kiểm bằng mẫu lắp thật? | Đường tiếp cận dụng cụ | TK Ch14 §14.7 |
| Sản xuất bồi đắp — bốn bước theo thứ tự | Đã đi Đặt chi tiết → Định kích thước → Làm sạch → Chống đỡ, đúng thứ tự? Mặt nào cần dư cỡ, đặc điểm nào ra hụt cỡ? | Hướng in, dư cỡ, chống đỡ | TK Ch15 §15.4 |
| Tối ưu tô-pô là giả thuyết | Kết quả tối ưu đã diễn giải lại theo khả năng chế tạo thật, và có phép kiểm vật lý khác mô phỏng? | Hình học sau diễn giải | TK Ch15 §15.7 |
| Con người — định lực theo người yếu, định bền theo người khoẻ | Bộ điều khiển định cỡ lực theo nhóm yếu và bền theo nhóm khoẻ riêng biệt? | Lực thao tác, độ bền tay nắm | TK Ch16 §16.2 |
| Con người — hướng điều khiển | Hướng tác động của cần/nút khớp hướng hiệu ứng mong đợi; đời sau có đảo hướng một điều khiển an toàn-tới-hạn? | Hướng, vị trí bộ điều khiển | TK Ch16 §16.4 |

Luật dùng ở C2: mỗi phương án hình thể ghi ít nhất một dòng của bảng làm lý do, kèm nhãn `phỏng đoán` cho tới khi có
phép thử; khi hai dòng kéo ngược nhau, ghi cả hai và để C3/C4 quyết bằng tham số nhạy nhất (TK Ch06 §06.1).
