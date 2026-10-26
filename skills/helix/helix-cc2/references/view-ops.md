# Phép biến đổi góc nhìn và phương tiện quan sát

> Reference dùng chung của bộ `helix-cc2`. Sáu phép dùng được trên mọi chuỗi C&C² (`--op <phép>`). Mỗi phép ghi
> *khi nào* (câu hỏi kích hoạt), *làm gì với mô hình*, *dấu hiệu dùng sai*. Mỗi lần dùng sinh một phiên bản chuỗi mới
> (`A.1`, `A.2`…), không ghi đè. Nguồn: CC = *Mô hình C&C² và giả thuyết kết cấu*.

Zoom, shift, state, view không chạm mẫu; chúng đổi mức chi tiết, biên, thời gian và hướng nhìn của mô hình (CC Ch04 §04.3). Chỉ observe tác động lên mẫu.
Bảng kỹ thuật là *một lựa chọn*, không phải danh mục phải chạy hết (CC Ch04 §04.2).

Bốn câu hỏi dẫn đường dùng như danh sách kiểm, không như thứ tự bắt buộc: nghi một tham số mà không thấy vì mức chi
tiết → zoom-in; nghi một tương tác → shift hoặc zoom-out; trạng thái hệ có đổi → state; vẫn chưa rõ → view
(CC Ch04 §04.3).

### zoom-in

- Khi nào: nghi một tham số hình thể liên quan chức năng nhưng mức chi tiết hiện tại không cho thấy nó; một WFP thô có thể đang chứa nhiều điểm tựa (CC Ch04 §04.3).
- Làm gì với mô hình: tách một phần tử thành nhiều phần tử nhỏ trong một khung con có **mục đích riêng**; mô hình thô vẫn còn hiệu lực ở mức của nó (CC Ch04 §04.3).
- Dấu hiệu dùng sai: phóng to mà không ghi câu hỏi mới cho khung con; hoặc phóng mọi chỗ cùng lúc thay vì chỉ ở chỗ thực hiện chức năng — chi tiết cao ở «răng lược», thô ở «sống lược» (CC Ch02 §02.7).

### zoom-out

- Khi nào: nghi một tương tác với hệ con xung quanh hay với môi trường; mô hình đã ngập thông tin (CC Ch04 §04.2).
- Làm gì với mô hình: nâng mức xem, gộp phần tử, nới biên để thấy tương tác; mô hình chi tiết vẫn hiệu lực (CC Ch04 §04.3).
- Dấu hiệu dùng sai: gộp LSS song song mà không giữ vòng phóng to ở vùng tới hạn — khi ấy mô hình, nói chặt, là không đúng (CC Ch05 §05.3).

### shift

- Khi nào: hệ con nghi vấn khó quan sát; hoặc có một tác dụng mà mô hình hiện tại không giải thích được (CC Ch04 §04.3).
- Làm gì với mô hình: dời trọng tâm dọc lưới làm việc — tách một Connector thành WFP và LSS để mở biên, hoặc gộp ngược thành Connector mới; hai bước là dời nghi vấn rồi mở biên. Ví dụ sách: «Shift dời trọng tâm từ WFP1 sang WFP2, và biên không gian được mở» (CC Ch04 §04.3).
- Dấu hiệu dùng sai: không ai ký cho mở biên sang dụng cụ, đồ gá, quy trình lắp, nên cuộc tìm dừng ở chi tiết dễ đổ lỗi nhất (CC Ch04 §04.3); hoặc tháo phần ngoài biên để «mở» làm mất chính trạng thái lắp cần xem (CC Ch04 §04.2).

### state

- Khi nào: quá trình quá nhanh hoặc quá chậm để thấy; một trạng thái kéo dài bất thường; hệ có nhánh logic (CC Ch05 §05.1).
- Làm gì với mô hình: cắt chuỗi trạng thái theo bộ phần tử (thêm/bớt WFP, LSS), phân tích từng trạng thái rồi gộp quan sát; ghi tiêu chí cắt khi thuộc tính đổi dần (CC Ch05 §05.1).
- Dấu hiệu dùng sai: chỉ nhìn trạng thái cuối nên bỏ lỡ một tham số đã «in dấu» ở trạng thái trước rồi biến mất (CC Ch04 §04.3); hoặc dựng chuỗi khi câu hỏi chỉ ở một trạng thái (CC Ch05 §05.5).

Luật kèm: «trạng thái dài bất thường là tín hiệu có một chuỗi khác, ở chỗ khác, đang can thiệp» (CC Ch05 §05.1).

### view

- Khi nào: hành vi vẫn chưa rõ sau các phép khác; hoặc góc nhìn thường lệ che đúng chỗ đáng nhìn — «nhìn hệ từ hướng không gian hay chỗ đứng khác giúp vượt rào cản quan sát và tìm nguyên nhân của hành vi chưa biết» (CC Ch04 §04.3).
- Làm gì với mô hình: tạo một ảnh hệ mới (bước c) từ chỗ đứng khác; vẽ dòng trước, phần tử sau — góc nhìn mới thường làm lộ một WFP chưa ai vẽ (CC Ch04 §04.3).
- Dấu hiệu dùng sai: camera hay đèn làm đổi chính dòng đang quan sát; hoặc thấy một dòng lạ một lần rồi coi là quy luật (CC Ch04 §04.2).

### observe

- Khi nào: bốn phép trên chưa đủ, cần một phương pháp tác động lên mẫu để tách WFP thật khỏi mặt biên (CC Ch04 §04.4).
- Làm gì với mô hình: chọn phương tiện phá rào cản — đọc vết mòn và chỗ hỏng, bột rà màu, chụp xuyên vật liệu, mẫu phóng tỉ lệ, dựng lại bằng vật liệu thay thế, mặt cắt ở trạng thái làm chức năng, quang ứng suất; ghi điều kiện chạy (mẫu nào, trạng thái nào, ai làm) lên phiếu (CC Ch04 §04.4).
- Dấu hiệu dùng sai: cắt mẫu hỏng duy nhất cho một câu hỏi chưa ai viết; rà màu quá dày hay chỉ xoay tay rồi dùng vết sai để *loại* một WFP thật (CC Ch04 §04.11).

Cách đọc vết: «vết mòn là dấu hiệu của cặp bề mặt làm việc; chỗ bị ép và chỗ hỏng là dấu hiệu của cấu trúc dẫn-đỡ» (CC Ch04 §04.4).

## Rào cản quan sát

Rào cản là thuộc tính của **hệ** (cái gì che); lớp lỗi là thuộc tính của **người quan sát và kỹ thuật** (mình có thể
sai ở đâu). Phá được rào cản vẫn có thể đưa vào lỗi *quan sát sai* hay *diễn giải sai* (CC Ch04 §04.2).

| Rào cản | Dấu hiệu nhận ra | Phép / phương tiện phá | Lỗi dễ đưa vào | Nguồn |
|---|---|---|---|---|
| quá nhanh | Quá trình vài mili giây; WFP chỉ tồn tại trong một trạng thái ngắn | `state` + camera tốc độ cao; dừng hệ ở nhiều thời điểm rồi cắt mặt | Một lần quay được coi là quy luật | (CC Ch04 §04.3) |
| quá chậm | Lỏng dần, chai dần, mòn tích dần qua nhiều chu kỳ; mỗi lần nhìn gần như lần trước | `state` theo vòng đời + `observe` (vết mòn so mẫu chưa dùng); ảnh định kỳ cùng góc, cùng mốc | Đổi do mùa, do lắp lại bị đọc thành đổi do mòn | (CC Ch04 §04.2) |
| bị che | WFP nằm khuất trong cụm lắp | `observe`: rà màu, chụp xuyên, mặt cắt ở trạng thái làm chức năng; `shift` sang hệ con láng giềng | Lớp màu đổi khe; cắt sau khi tháo | (CC Ch04 §04.4) |
| quá nhỏ / quá lớn | Chi tiết ngoài tầm tay và mắt người | `zoom-in`; `observe`: mẫu phóng hay thu tỉ lệ dựng từ số đo thật — chỉ trả lời câu hỏi hình học | Kết luận hình học bị kéo sang vật liệu, ma sát | (CC Ch04 §04.4) |
| sai góc nhìn | Bộ phận bị nghi «làm tốt» mà kết quả vẫn kém | `view`: camera trong khoang, đổi hướng quay | Camera chắn dòng vật liệu | (CC Ch04 §04.3) |
| ngoài biên | Nguyên cớ nằm ở phần chưa đưa vào mô hình (dụng cụ, đồ gá, nguồn, người lắp) | `shift`, `zoom-out`, mở Connector | Nguyên nhân ở dụng cụ bị gán cho sản phẩm | (CC Ch04 §04.3) |

Cuối mỗi khối C1, C2, CA, skill in **«Phép nên làm tiếp»**: 1–3 dòng `phép · phần tử · câu hỏi kích hoạt` lấy từ
các dòng `Khi nào:` ở trên. Mỗi phép một câu hỏi; không có câu hỏi thì không đề xuất phép (CC Ch04 §04.11).
