# Lớp hiệu chỉnh — Quản đốc phân xưởng

> **NHÁP — chưa dùng được.** Ba trường `Tín hiệu`, `Ví dụ ngành`, `Cách cải tiến tại chỗ`
> là bản soạn sẵn để CEO gạch xoá, viết đè, hoặc bỏ hẳn. Toàn bộ 12 trường `Cờ đỏ` bỏ trống
> có chủ đích: cờ đỏ là tuyên bố hành vi nào không chấp nhận được trong xưởng — đó là chuẩn
> mực của người chịu trách nhiệm, không phải suy đoán của AI.
>
> Còn sót ô `⟨CEO chốt: …⟩` thì `active-profile.md` từ chối bật file này. Đó là cố ý.
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

**Cờ đỏ:** ⟨CEO chốt: quản đốc dùng AI tới mức nào thì thành thay cho việc đọc bản vẽ? Ranh giới này quyết định cả cách chấm ô này⟩

**Ví dụ ngành:** "Chi tiết này dung sai bao nhiêu" là câu tra được. "Nên gá thế nào cho khỏi vênh" là câu cần hiểu cụm lắp trước khi hỏi.

**Cách cải tiến tại chỗ:** Nói một câu về mục đích của chi tiết trước khi hỏi AI về nó. Nói không được là chưa đọc đủ.

## del.platform

**Tín hiệu:** Biết việc nào AI trả lời được ngay, việc nào phải tra tiêu chuẩn hoặc hỏi thiết kế. Không hỏi AI những thứ chỉ có trong hồ sơ nội bộ mà AI không thấy.

**Cờ đỏ:** ⟨CEO chốt: hỏi AI thông số khí tài hoặc nội dung hồ sơ nội bộ — mức nào là nhầm lẫn công cụ, mức nào là vi phạm bảo mật?⟩

**Ví dụ ngành:** Hỏi AI thông số máy trong xưởng thì nó đoán; thông số đó nằm ở lý lịch máy, phải tra.

**Cách cải tiến tại chỗ:** Trước khi hỏi, tự trả lời: dữ liệu để trả lời câu này nằm ở đâu — trong sách vở chung hay trong hồ sơ xưởng mình?

## del.task

**Tín hiệu:** Giao AI phần soạn thảo và tra cứu, giữ lại phần quyết định thao tác và phân công người. Nói rõ phần nào tự làm.

**Cờ đỏ:** ⟨CEO chốt: có phần việc nào của quản đốc tuyệt đối không được để AI soạn dù chỉ là bản nháp?⟩

**Ví dụ ngành:** Để AI soạn khung phiếu công nghệ thì được; chọn chế độ cắt và thứ tự nguyên công là việc của quản đốc.

**Cách cải tiến tại chỗ:** Mỗi lần dùng AI cho việc xưởng, nói ra một câu phần nào mình tự quyết. Không nói được là chưa chia việc.

## des.product

**Tín hiệu:** Nói rõ đầu ra cần gì: phiếu cho ai đọc, thợ bậc mấy, in ra hay xem trên máy, dài bao nhiêu. Mọi kích thước và chế độ ghi hệ mét.

**Cờ đỏ:** ⟨CEO chốt: tài liệu xuống xưởng thiếu thông tin gì thì coi là không đạt, phải trả lại?⟩

**Ví dụ ngành:** "Viết hướng dẫn thao tác cho thợ hàn bậc 3, một trang, có bảng thông số hàn, đọc xong là làm được không cần hỏi lại."

**Cách cải tiến tại chỗ:** Nêu đích danh người sẽ đọc và bậc thợ ngay trong câu giao việc. Tài liệu xưởng sai người đọc là tài liệu vô dụng.

## des.process

**Tín hiệu:** Chỉ định theo quy trình và biểu mẫu sẵn có của xưởng thay vì để AI tự bịa ra một trình tự lạ.

**Cờ đỏ:** ⟨CEO chốt: quy trình nào bắt buộc phải theo đúng biểu mẫu, không được để AI đề xuất trình tự khác?⟩

**Ví dụ ngành:** "Soạn theo đúng khung phiếu công nghệ đang dùng, không thêm bớt mục."

**Cách cải tiến tại chỗ:** Dán mẫu biểu đang dùng vào prompt thay vì mô tả bằng lời. Mẫu thật chặn được việc AI tự chế khung.

## des.performance

**Tín hiệu:** Có yêu cầu AI chỉ ra chỗ dễ sai, chỗ nguy hiểm, thay vì chỉ viết cho trôi.

**Cờ đỏ:** ⟨CEO chốt: với việc có rủi ro an toàn, bắt buộc phải yêu cầu AI nêu cảnh báo hay không? Nếu có thì trường hợp nào⟩

**Ví dụ ngành:** "Viết xong thì chỉ ra ba chỗ thợ mới hay làm sai trong quy trình này."

**Cách cải tiến tại chỗ:** Thêm một câu cố định vào cuối mọi prompt soạn quy trình: chỗ nào dễ làm sai, chỗ nào nguy hiểm.

## dis.product

**Tín hiệu:** Mọi con số đi xuống xưởng — chế độ cắt, thông số hàn, dung sai, lực siết — đều đối chiếu tiêu chuẩn hoặc sổ tay trước khi ban hành. Không dùng số AI đưa mà chưa đối chiếu.

**Cờ đỏ:** ⟨CEO chốt: loại số nào tuyệt đối không được xuống xưởng nếu chưa có người đối chiếu và ký? Đây là ô dễ gây hỏng phôi và tai nạn nhất⟩

**Ví dụ ngành:** AI đưa dòng hàn cho tôn 6 mm — đối chiếu sổ tay hàn và máy đang có trước khi ghi vào phiếu.

**Cách cải tiến tại chỗ:** Số nào chưa đối chiếu thì ghi rõ "chưa đối chiếu" ngay trong bản nháp, đừng để lẫn với số đã kiểm.

## dis.process

**Tín hiệu:** Hỏi AI dựa vào đâu mà ra con số đó — tiêu chuẩn nào, vật liệu nào, chiều dày nào — trước khi tin.

**Cờ đỏ:** ⟨CEO chốt: câu trả lời không nêu được căn cứ thì xử lý thế nào — bỏ hẳn, hay dùng tạm và đánh dấu?⟩

**Ví dụ ngành:** Cùng một mác thép mà khác chiều dày thì chế độ khác nhau; câu trả lời không nói chiều dày là câu chưa dùng được.

**Cách cải tiến tại chỗ:** Hỏi lại đúng một câu "căn cứ vào đâu" cho mỗi thông số then chốt, trước khi đưa vào phiếu.

## dis.performance

**Tín hiệu:** Nhận ra lúc AI đang viết dài ra thay vì giải quyết; kéo về câu hỏi thao tác cụ thể.

**Cờ đỏ:** ⟨CEO chốt: dấu hiệu nào cho thấy quản đốc đang dùng AI để trì hoãn việc xuống xưởng xử lý trực tiếp?⟩

**Ví dụ ngành:** Máy đang lỗi mà ngồi hỏi AI phân tích nguyên nhân vòng vo — câu đúng là hỏi cách kiểm tra từng bước, rồi ra máy kiểm.

**Cách cải tiến tại chỗ:** Đặt mốc: hỏi AI quá hai vòng mà chưa ra thao tác kiểm tra được thì dừng, ra hiện trường.

## dil.creation

**Tín hiệu:** Không đưa bản vẽ có dấu, thông số sản phẩm quốc phòng, tên và giá nhà cung cấp vào công cụ ngoài. Cần hỏi thì mô tả bằng hình học và vật liệu chung.

**Cờ đỏ:** ⟨CEO chốt: danh mục cụ thể những thứ tuyệt đối không được đưa ra ngoài, và mức xử lý khi vi phạm. Đây là trường không được để trống⟩

**Ví dụ ngành:** Hỏi cách gá một chi tiết thì mô tả "tấm thép 8 mm, 300×200, bốn lỗ M12", không dán bản vẽ có khung tên.

**Cách cải tiến tại chỗ:** Trước khi dán bất cứ thứ gì, nhìn khung tên và dấu trên tài liệu. Có dấu thì không dán.

## dil.transparency

**Tín hiệu:** Tài liệu xuống xưởng hoặc vào hồ sơ có ghi phần nào AI soạn, và ai đã kiểm.

**Cờ đỏ:** ⟨CEO chốt: hồ sơ nào bắt buộc phải ghi nhận phần AI tham gia, hồ sơ nào không cần? Ranh giới do CEO định⟩

**Ví dụ ngành:** Phiếu công nghệ AI soạn khung, quản đốc chốt thông số — ghi rõ như vậy vào ô ghi chú.

**Cách cải tiến tại chỗ:** Thêm một dòng cố định ở cuối tài liệu do AI hỗ trợ: phần nào soạn máy, ai kiểm, ngày nào.

## dil.deployment

**Tín hiệu:** Không ban hành tài liệu chưa đọc hết. Thứ đã ký là thứ chịu trách nhiệm, kể cả phần AI soạn.

**Cờ đỏ:** ⟨CEO chốt: ban hành tài liệu do AI soạn mà chưa đọc hết — xử lý thế nào? Mức này định ra toàn bộ sức nặng của ô Diligence⟩

**Ví dụ ngành:** Phiếu công nghệ do AI soạn phải đọc lại từng dòng thông số trước khi ký và phát cho tổ.

**Cách cải tiến tại chỗ:** Đọc to phần thông số trước khi ký. Đọc to bắt được lỗi mà đọc lướt bỏ qua.
