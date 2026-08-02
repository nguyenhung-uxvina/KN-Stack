# Lớp hiệu chỉnh — Quản đốc phân xưởng

> **Dùng được.** Toàn bộ 12 trường Cờ đỏ do CEO chốt ngày 2026-08-02 — cờ đỏ là tuyên bố
> hành vi nào không chấp nhận được trong xưởng, AI không viết hộ trường này.
>
> Ba trường còn lại — `Tín hiệu`, `Ví dụ ngành`, `Cách cải tiến tại chỗ` — vẫn là bản AI
> soạn, chưa qua tay quản đốc thật. Sửa được bất cứ lúc nào mà không phải hỏi ai.
>
> Bật profile này: đổi tên file trong khối mã của `active-profile.md`.
>
> Thang điểm nằm ở `rubric-core.md`, KHÔNG định nghĩa lại ở đây.

## Vai này khác CEO ở chỗ nào

Quản đốc không quyết kiến trúc sản phẩm và không chốt gate. Việc hằng ngày là **biến bản vẽ
và yêu cầu thành thao tác ở xưởng**: đọc bản vẽ, ra quy trình công nghệ, phân công, ghi hồ sơ
kiểm tra, xử lý sự cố ca. Nên trọng tâm chấm dịch chuyển: nhẹ về `del.problem` (đầu bài phần
lớn đến từ trên xuống), nặng về `dis.product` (số sai xuống xưởng là cắt hỏng phôi thật) và
`dil.deployment` (thứ ký vào hồ sơ là thứ chịu trách nhiệm trước hội đồng).

---

## del.problem

**Tín hiệu:** Trước khi hỏi AI, đã đọc hết bản vẽ và phiếu công nghệ được giao chưa; đã biết chi tiết này thuộc cụm nào, lắp với cái gì. Hỏi AI để hiểu nhanh hơn thì được, hỏi AI thay cho việc đọc thì không.

**Cờ đỏ:** Ra quyết định có hệ quả xuống xưởng chỉ dựa vào câu trả lời AI, chưa đối chiếu hồ sơ gốc.

**Ví dụ ngành:** "Chi tiết này dung sai bao nhiêu" là câu tra được. "Nên gá thế nào cho khỏi vênh" là câu cần hiểu cụm lắp trước khi hỏi.

**Cách cải tiến tại chỗ:** Nói một câu về mục đích của chi tiết trước khi hỏi AI về nó. Nói không được là chưa đọc đủ.

## del.platform

**Tín hiệu:** Biết việc nào AI trả lời được ngay, việc nào phải tra tiêu chuẩn hoặc hỏi thiết kế. Không hỏi AI những thứ chỉ có trong hồ sơ nội bộ mà AI không thấy.

**Cờ đỏ:** Lấy thông số thiết bị xưởng từ AI rồi dùng như số thật, không tra lý lịch máy.

**Ví dụ ngành:** Hỏi AI thông số máy trong xưởng thì nó đoán; thông số đó nằm ở lý lịch máy, phải tra.

**Cách cải tiến tại chỗ:** Trước khi hỏi, tự trả lời: dữ liệu để trả lời câu này nằm ở đâu — trong sách vở chung hay trong hồ sơ xưởng mình?

## del.task

**Tín hiệu:** Giao AI phần soạn thảo và tra cứu, giữ lại phần quyết định thao tác và phân công người. Nói rõ phần nào tự làm.

**Cờ đỏ:** Để AI chốt chế độ gia công hoặc thứ tự nguyên công, kể cả dưới dạng bản nháp.

**Ví dụ ngành:** Để AI soạn khung phiếu công nghệ thì được; chọn chế độ cắt và thứ tự nguyên công là việc của quản đốc.

**Cách cải tiến tại chỗ:** Mỗi lần dùng AI cho việc xưởng, nói ra một câu phần nào mình tự quyết. Không nói được là chưa chia việc.

## des.product

**Tín hiệu:** Nói rõ đầu ra cần gì: phiếu cho ai đọc, thợ bậc mấy, in ra hay xem trên máy, dài bao nhiêu. Mọi kích thước và chế độ ghi hệ mét.

**Cờ đỏ:** Ban hành tài liệu xuống xưởng thiếu thông số hoặc dung sai bắt buộc, để thợ tự đoán.

**Ví dụ ngành:** "Viết hướng dẫn thao tác cho thợ hàn bậc 3, một trang, có bảng thông số hàn, đọc xong là làm được không cần hỏi lại."

**Cách cải tiến tại chỗ:** Nêu đích danh người sẽ đọc và bậc thợ ngay trong câu giao việc. Tài liệu xưởng sai người đọc là tài liệu vô dụng.

## des.process

**Tín hiệu:** Chỉ định theo quy trình và biểu mẫu sẵn có của xưởng thay vì để AI tự bịa ra một trình tự lạ.

**Cờ đỏ:** Để AI tự chế khung cho bất kỳ tài liệu nào đi vào hồ sơ chất lượng sản phẩm.

**Ví dụ ngành:** "Soạn theo đúng khung phiếu công nghệ đang dùng, không thêm bớt mục."

**Cách cải tiến tại chỗ:** Dán mẫu biểu đang dùng vào prompt thay vì mô tả bằng lời. Mẫu thật chặn được việc AI tự chế khung.

## des.performance

**Tín hiệu:** Có yêu cầu AI chỉ ra chỗ dễ sai, chỗ nguy hiểm, thay vì chỉ viết cho trôi.

**Cờ đỏ:** Ban hành tài liệu thao tác do AI soạn mà không có mục cảnh báo chỗ dễ sai và chỗ nguy hiểm.

**Ví dụ ngành:** "Viết xong thì chỉ ra ba chỗ thợ mới hay làm sai trong quy trình này."

**Cách cải tiến tại chỗ:** Thêm một câu cố định vào cuối mọi prompt soạn quy trình: chỗ nào dễ làm sai, chỗ nào nguy hiểm.

## dis.product

**Tín hiệu:** Mọi con số đi xuống xưởng — chế độ cắt, thông số hàn, dung sai, lực siết — đều đối chiếu tiêu chuẩn hoặc sổ tay trước khi ban hành. Không dùng số AI đưa mà chưa đối chiếu.

**Cờ đỏ:** Số chạm tới an toàn hoặc khả năng chịu lực đi xuống xưởng khi chưa có người đối chiếu và ký.

**Ví dụ ngành:** AI đưa dòng hàn cho tôn 6 mm — đối chiếu sổ tay hàn và máy đang có trước khi ghi vào phiếu.

**Cách cải tiến tại chỗ:** Số nào chưa đối chiếu thì ghi rõ "chưa đối chiếu" ngay trong bản nháp, đừng để lẫn với số đã kiểm.

## dis.process

**Tín hiệu:** Hỏi AI dựa vào đâu mà ra con số đó — tiêu chuẩn nào, vật liệu nào, chiều dày nào — trước khi tin.

**Cờ đỏ:** Dùng một thông số mà không biết nó ứng với vật liệu, chiều dày, thiết bị nào.

**Ví dụ ngành:** Cùng một mác thép mà khác chiều dày thì chế độ khác nhau; câu trả lời không nói chiều dày là câu chưa dùng được.

**Cách cải tiến tại chỗ:** Hỏi lại đúng một câu "căn cứ vào đâu" cho mỗi thông số then chốt, trước khi đưa vào phiếu.

## dis.performance

**Tín hiệu:** Nhận ra lúc AI đang viết dài ra thay vì giải quyết; kéo về câu hỏi thao tác cụ thể.

**Cờ đỏ:** Thiết bị đang dừng mà hỏi AI quá hai vòng vẫn chưa ra được thao tác kiểm tra nào.

**Ví dụ ngành:** Máy đang lỗi mà ngồi hỏi AI phân tích nguyên nhân vòng vo — câu đúng là hỏi cách kiểm tra từng bước, rồi ra máy kiểm.

**Cách cải tiến tại chỗ:** Đặt mốc: hỏi AI quá hai vòng mà chưa ra thao tác kiểm tra được thì dừng, ra hiện trường.

## dil.creation

**Tín hiệu:** Không đưa bản vẽ có dấu, thông số sản phẩm quốc phòng, tên và giá nhà cung cấp vào công cụ ngoài. Cần hỏi thì mô tả bằng hình học và vật liệu chung.

**Cờ đỏ:** Đưa ra công cụ ngoài bất kỳ thứ nào sau đây: bản vẽ còn khung tên hoặc dấu · thông số sản phẩm quốc phòng · tên và giá nhà cung cấp.

**Ví dụ ngành:** Hỏi cách gá một chi tiết thì mô tả "tấm thép 8 mm, 300×200, bốn lỗ M12", không dán bản vẽ có khung tên.

**Cách cải tiến tại chỗ:** Trước khi dán bất cứ thứ gì, nhìn khung tên và dấu trên tài liệu. Có dấu thì không dán.

## dil.transparency

**Tín hiệu:** Tài liệu xuống xưởng hoặc vào hồ sơ có ghi phần nào AI soạn, và ai đã kiểm.

**Cờ đỏ:** Tài liệu đi vào hồ sơ chất lượng hoặc ra khỏi xưởng mà không ghi phần nào AI soạn, ai đã kiểm.

**Ví dụ ngành:** Phiếu công nghệ AI soạn khung, quản đốc chốt thông số — ghi rõ như vậy vào ô ghi chú.

**Cách cải tiến tại chỗ:** Thêm một dòng cố định ở cuối tài liệu do AI hỗ trợ: phần nào soạn máy, ai kiểm, ngày nào.

## dil.deployment

**Tín hiệu:** Không ban hành tài liệu chưa đọc hết. Thứ đã ký là thứ chịu trách nhiệm, kể cả phần AI soạn.

**Cờ đỏ:** Ký và ban hành tài liệu do AI soạn mà chưa đọc hết từng dòng thông số.

**Ví dụ ngành:** Phiếu công nghệ do AI soạn phải đọc lại từng dòng thông số trước khi ký và phát cho tổ.

**Cách cải tiến tại chỗ:** Đọc to phần thông số trước khi ký. Đọc to bắt được lỗi mà đọc lướt bỏ qua.
