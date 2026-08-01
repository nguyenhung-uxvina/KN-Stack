# Lớp hiệu chỉnh — Workshop X

> File này KHÔNG định nghĩa lại thang điểm. Thang điểm nằm ở `rubric-core.md`.
> Ở đây chỉ có: tín hiệu cần soi, cờ đỏ, ví dụ ngành — cho từng ô trong 12 ô.
> Muốn phát cho người khác: chép file này thành `profile-<tên>.md`, giữ nguyên
> khung `## <mã ô>` + ba trường, rồi đổi dòng trỏ trong ba SKILL.md.

## del.problem

**Tín hiệu:** Task đã được phân loại COD (Core / Offload / Default) trước khi giao chưa? Mục tiêu và tiêu chí "xong" đã rõ trước khi mở phiên chưa?

**Cờ đỏ:** Việc thuộc Core (phán đoán thiết kế, quyết định gate, chọn phương án) mà đem giao trọn — chấm thấp bất kể kết quả tốt. Tỷ trọng thời gian Core vượt trần 60%.

**Ví dụ ngành:** "Chọn concept mặt bia nào" là Core. "Lập ma trận hình thái cho 4 concept" là Offload.

## del.platform

**Tín hiệu:** Chọn đúng tầng model cho loại việc — hạng nặng cho kiến trúc, gate review, thiết kế hệ thống; hạng nhẹ cho đọc file, soạn tài liệu, chạy test. Có tra xem KN-Stack đã có skill cho việc này chưa.

**Cờ đỏ:** Làm tay một việc đã có skill sẵn. Dùng model đắt cho việc đọc file. Giao việc cần công cụ ngoài (CAD, ERP) cho phiên không có công cụ đó.

**Ví dụ ngành:** Cần soi bản vẽ trước khi cấp phát xưởng — đã có `helix-cad-validate`, đừng dựng lại quy trình kiểm bằng tay.

## del.task

**Tín hiệu:** Việc được chia theo phase Pahl-Beitz hoặc theo khối giao được, mỗi khối có đầu vào–đầu ra rõ. Phần phán đoán thiết kế được giữ lại đích danh.

**Cờ đỏ:** Quăng cả cục "làm giúp anh cái này". Giao một lần cả bốn phase. Không nói phần nào tự làm.

**Ví dụ ngành:** Phase 2 concept: giao sinh ma trận hình thái và chấm sơ bộ, giữ lại quyết định chốt concept.

## des.product

**Tín hiệu:** Nói rõ đầu ra là gì, định dạng nào, ai đọc, và tiêu chí "xong" đo được. Mọi đại lượng vật lý dùng hệ mét.

**Cờ đỏ:** "Cứ làm đi rồi tính." Không nêu người đọc. Xuất hiện inch, pound, psi mà không quy đổi.

**Ví dụ ngành:** "Báo cáo 2 trang cho hội đồng nghiệm thu, có bảng so sánh 2 vật liệu, kết luận 1 dòng, xong = trả lời được câu hỏi chọn cái nào và vì sao."

## des.process

**Tín hiệu:** Chỉ định khung làm việc sẵn có — 3-Gate, VDI 2225, ODI, phase Pahl-Beitz, ACH — thay vì để AI tự chế quy trình.

**Cờ đỏ:** Bài toán chọn phương án mà không nhắc VDI 2225. Bài toán nhu cầu người dùng mà không nhắc ODI. AI tự bịa ra một khung lạ và không bị chặn.

**Ví dụ ngành:** "Chấm 4 concept theo VDI 2225, trọng số lấy từ danh mục yêu cầu Phase 1."

## des.performance

**Tín hiệu:** Nói rõ muốn AI phản biện hay thừa hành, gọn hay chi tiết, được phép hỏi lại đến đâu.

**Cờ đỏ:** Không bao giờ yêu cầu phản biện, rồi ngạc nhiên vì AI gật theo mọi thứ. Nhận một chuỗi đồng ý liên tiếp mà không thấy lạ.

**Ví dụ ngành:** "Đóng vai hội đồng nghiệm thu khó tính, tìm chỗ hồ sơ này sẽ bị bắt bẻ."

## dis.product

**Tín hiệu:** Có kiểm số trước khi dùng — chạy ratio-check, đòi bằng chứng vật lý (kết quả test, ảnh, số đo), hỏi nguồn cho mọi con số then chốt.

**Cờ đỏ:** Nhận một con số kỹ thuật rồi đưa thẳng vào hồ sơ mà không hỏi nguồn. Chấp nhận "khoảng", "ước tính" cho tham số đi vào quyết định.

**Ví dụ ngành:** AI đưa giới hạn chảy 245 MPa cho SS400 — hỏi tiêu chuẩn nào, bản nào, dày bao nhiêu, trước khi dùng để tính.

## dis.process

**Tín hiệu:** Soi cách AI đi tới kết luận — nguồn có phân tier S/A/B/C không, có kiểm chéo ít nhất hai nguồn độc lập cho khẳng định quan trọng không.

**Cờ đỏ:** Kết luận dựa trên một nguồn duy nhất. Trích dẫn không kiểm được. Suy luận nhảy bước mà không bị hỏi.

**Ví dụ ngành:** Kết luận về sản phẩm đối thủ chỉ dựa trên một trang marketing — chưa đủ tier để đưa vào hồ sơ cạnh tranh.

## dis.performance

**Tín hiệu:** Bắt được lúc AI trôi sang analyst-trap — đẻ thêm phân tích, khung, tài liệu thay vì đẩy tới dữ liệu vật lý — và kéo lại.

**Cờ đỏ:** Phiên kết thúc với thêm ba tài liệu phân tích và không có hành động vật lý nào. AI đề xuất "nghiên cứu thêm" và được chấp nhận không phản biện.

**Ví dụ ngành:** Đang bí ở khâu chọn vật liệu, AI đề xuất lập thêm ma trận đánh giá — câu hỏi đúng là "chỗ này cần thêm phân tích hay cần một mẫu thử?"

## dil.creation

**Tín hiệu:** Không đưa dữ liệu MẬT, không đưa giá nhà cung cấp, không đưa thông tin định danh đối tác vào prompt. Cân nhắc phiên này chạy ở đâu, ai đọc được.

**Cờ đỏ:** Dán bảng báo giá có tên nhà cung cấp. Dán nội dung có dấu mật. Đưa thông số khí tài nhạy cảm vào dịch vụ ngoài. Bất kỳ cái nào cũng là điểm 0 và bật cờ đỏ.

**Ví dụ ngành:** Cần so sánh chi phí thì dùng "nhà cung cấp A / B" với giá tương đối, không dùng tên và giá thật.

## dil.transparency

**Tín hiệu:** Tài liệu giao ra ngoài — BQP, hội đồng, đối tác — có ghi rõ phần nào AI tham gia và người ký đã kiểm.

**Cờ đỏ:** Nộp hồ sơ do AI soạn phần lớn mà không ghi nhận gì. Để người đọc mặc định đó là công sức thủ công.

**Ví dụ ngành:** Thuyết minh đề tài KHCN: nêu rõ phần tổng hợp tài liệu có AI hỗ trợ, phần số liệu thử nghiệm là đo thật.

## dil.deployment

**Tín hiệu:** Chạy test trước khi mở PR, không commit thẳng main, tự đọc lại và đứng tên chịu trách nhiệm cho thứ đem dùng.

**Cờ đỏ:** Commit thẳng main. Mở PR chưa chạy test. Ký vào tài liệu chưa đọc hết. Đem kết quả AI đi họp mà chưa tự kiểm.

**Ví dụ ngành:** Bản vẽ chế tạo do AI sinh phải qua helix-cad-validate và mắt người trước khi xuống xưởng cắt.
