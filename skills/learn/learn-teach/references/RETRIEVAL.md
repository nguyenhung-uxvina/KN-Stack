# Đường Quay Lại — Giao Thức Hồi Tưởng & Hiệu Chỉnh

Không có file này, workspace chỉ ghi ra mà không bao giờ quay lại: bài học được viết, đọc một lần, rồi nằm im. Mọi đòn bẩy mạnh nhất của khoa học học tập — giãn cách, hồi tưởng có nỗ lực, phát hiện ảo giác thành thạo — đều **đòi hỏi quay lại**. Không có đường quay lại thì việc nêu chúng trong phần Triết Lý chỉ là trang trí.

## Mâu Thuẫn Phải Sửa

Quiz và câu tự luận nằm ở **cuối chính bài học vừa dạy**. Đó là khoảnh khắc độ trôi chảy cao nhất: nội dung còn nguyên trong bộ nhớ làm việc, ngữ cảnh còn mở, câu trả lời còn nằm cách vài dòng phía trên.

**Kiểm tra ngay sau khi dạy đo độ trôi chảy, không đo độ bền lưu trữ.** Nó vẫn có giá trị — buộc xử lý sâu ngay lúc học — nhưng **không bao giờ được coi là bằng chứng đã học**. Bằng chứng duy nhất là hồi tưởng nguội, muộn, không mở lại bài.

Quy tắc: quiz cuối bài là *công cụ dạy*. Hồi tưởng ở phiên sau là *phép đo*. Đừng lẫn hai thứ.

## `RETRIEVAL.md` — Sổ Hồi Tưởng

Một file ở gốc workspace. **Đây là nguồn sự thật duy nhất** về việc gì đã được nhớ, gì đến hạn, hiệu chỉnh của người học ra sao.

```md
# Sổ Hồi Tưởng — {Chủ Đề}

**Cập nhật:** {YYYY-MM-DD} · **Hiệu chỉnh tổng:** {ví dụ: quá tự tin 3/11 lượt}

| # | Mục | Bài | Đoán | Thực | Bậc | Đến hạn | Ghi chú |
|---|-----|-----|------|------|-----|---------|---------|
| 1 | Cowork nạp skill từ đâu, và vì sao không phải ~/.claude | 01 | C | ✓ | 3 | 2026-08-21 | |
| 2 | Auto khác Skip ở cơ chế nào | 01 | C | ✗ | 1 | 2026-08-15 | **ảo giác** — chắc mà sai, dạy lại bằng ví dụ khác |
| 3 | Vì sao outcome-first thay task-first | 01 | T | ✓ | 2 | 2026-08-17 | dưới tự tin |

**Đã bỏ qua:** {ngày} — bỏ 3 mục đến hạn để học bài mới
```

- **Mục** — một câu hỏi hồi tưởng, không phải một chủ đề. Viết ở dạng hỏi để dùng lại được nguyên văn.
- **Đoán** — người học tự đoán **trước khi trả lời**: `C` chắc · `V` vừa · `T` thấp.
- **Thực** — `✓` nhớ đúng · `✗` không nhớ hoặc sai.
- **Bậc** — nấc trong thang giãn cách.
- **Đến hạn** — ngày tuyệt đối. Không ghi "3 ngày nữa".

### Mục nào đáng đưa vào sổ

3–6 mục cho mỗi bài học. Tiêu chí: **mục phải chịu lực**. Nếu quên nó thì phần còn lại của bài sụp — đó là mục đáng đưa vào. Một định nghĩa từ vựng đơn lẻ thì không.

Ưu tiên câu hỏi dạng *vì sao* và *khác nhau ở cơ chế nào* hơn dạng *là gì*. Câu "là gì" kiểm tra nhận ra; câu "vì sao" buộc tạo lại lời giải thích từ đầu.

## Thang Giãn Cách

Bậc 1 → 2 → 3 → 4 → 5 tương ứng **1 · 3 · 7 · 16 · 35 ngày**.

- Nhớ đúng → lên một bậc.
- Không nhớ → **lùi hai bậc** (thấp nhất là bậc 1), không đặt về 0.

Lý do lùi hai bậc chứ không xoá sạch: một mục đã lên bậc 4 rồi trượt vẫn khác hẳn một mục chưa từng nhớ được. Đặt về 0 sẽ đốt lượt ôn vào thứ gần như đã thuộc, đúng cái lãng phí mà giãn cách sinh ra để tránh.

Thang này là điểm khởi đầu hợp lý, không phải hằng số thiêng. Nếu người học liên tục nhớ đúng ở mọi bậc, giãn thưa hơn — mục tiêu là hồi tưởng **có nỗ lực**, và nhớ quá dễ nghĩa là ôn quá sớm.

## Cổng Mở Phiên

**Mọi phiên `/learn-teach` bắt đầu bằng hồi tưởng các mục đến hạn, trước khi dạy bất cứ thứ gì mới.**

1. Đọc `RETRIEVAL.md`, lọc mục có `Đến hạn` ≤ hôm nay.
2. Nếu có mục đến hạn — **hỏi nguội**. Không mở lại bài học, không tóm tắt trước, không gợi ý. Chỉ đưa câu hỏi.
3. Với mỗi mục, **bắt đoán trước**: *"Trước khi trả lời — bạn nghĩ mình còn nhớ chắc, vừa, hay thấp?"* Ghi lại, rồi mới nghe câu trả lời.
4. Chấm, cập nhật `Đoán`/`Thực`/`Bậc`/`Đến hạn`.
5. **Rồi mới** dạy bài mới, và chọn dạy gì dựa trên kết quả vừa đo.

Nếu người học muốn bỏ qua để học bài mới ngay: cho phép, nhưng **ghi vào dòng "Đã bỏ qua"**. Bỏ qua một lần là bình thường; bỏ qua ba lần liên tiếp là tín hiệu — hoặc mục viết dở, hoặc mission đã đổi, hoặc workspace đang bị dùng như nơi tiêu thụ nội dung chứ không phải nơi học. Nêu thẳng điều đó với người học.

### Xen kẽ khi có nhiều mục đến hạn

Khi quá 3 mục đến hạn, **chọn trải rộng qua nhiều bài học nhất có thể**, đừng dồn hết mục của bài mới nhất. Trộn chủ đề trong một lượt ôn là nguồn của phần lớn lợi ích từ xen kẽ.

Cần lịch học nhiều tuần thì gọi `/learn-practice` thay vì tự dựng — nó đã có luật xen kẽ (không lặp cùng chủ đề hai buổi liền, tối thiểu 2 chủ đề mỗi tuần) và khối tập trung. Đừng chép lại luật đó vào đây.

## Hiệu Chỉnh — Đoán Trước Rồi Thử

Khoảng lệch giữa **đoán** và **thực** chính là ảo giác thành thạo, đo được bằng số. Đây là tín hiệu tốt nhất để chọn dạy gì tiếp theo — tốt hơn nhiều so với việc hỏi người học thấy phần nào khó.

| Đoán | Thực | Nghĩa là | Làm gì |
|---|---|---|---|
| Chắc | ✗ | **Ảo giác thành thạo** — nguy hiểm nhất | Ưu tiên cao nhất. Dạy lại bằng **cách biểu diễn khác** (ví dụ số mới, hình mới, góc nhìn mới), tuyệt đối không lặp lại đúng lời cũ |
| Thấp | ✓ | Dưới tự tin | Đừng dạy lại. Cho gặp thêm vài lần để dựng lòng tin; dạy lại chỉ làm mất thời gian |
| Chắc | ✓ | Hiệu chỉnh tốt | Lên bậc, giãn thưa |
| Thấp | ✗ | Biết mình chưa biết | Dạy lại bình thường — không phải ảo giác, chỉ là chưa học xong |

Ô **Chắc + ✗** là lý do tồn tại của cả giao thức này. Người học không thể tự phát hiện nó, vì cảm giác chắc chắn chính là thứ đang lừa họ. Chỉ một phép đo nguội, muộn mới lộ ra.

Ghi tình trạng hiệu chỉnh tổng vào đầu sổ (ví dụ *"quá tự tin 3/11 lượt"*) và nói cho người học biết. Bản thân việc thấy con số đó đã cải thiện hiệu chỉnh.

## Trang Ôn Tập HTML — Thuần Dẫn Xuất

Sinh `review/index.html` **từ** `RETRIEVAL.md` để người học tự ôn khi không mở agent.

**Ràng buộc chống lệch trạng thái, không được vi phạm:**

- Sổ là nguồn sự thật. Trang HTML **chỉ đọc**, sinh lại từ sổ, **không bao giờ sửa tay**.
- Trang **không ghi trạng thái có thẩm quyền**. Nếu dùng `localStorage` cho tiện thao tác trong một lượt, phải in rõ trên mặt trang: *"kết quả tự ôn ở đây KHÔNG được ghi vào sổ — nói lại với agent nếu muốn cập nhật"*.
- In ngày sinh trang. Trang cũ hơn sổ là chuyện bình thường và phải nhìn thấy được.
- Trang giấu đáp án sau nút bấm, và **giấu luôn cả mức đoán** cho tới khi người học chọn — giữ nguyên kỷ luật đoán-trước-rồi-thử.

Sinh lại trang mỗi lần sổ đổi. Nếu sinh lại không được thì thà không có trang còn hơn có trang nói dối.

## Nhịp Phiên — Tập Trung và Khuếch Tán

Não củng cố ở chế độ khuếch tán, tức lúc **không** tập trung vào tài liệu. Nhồi hai bài học vào một phiên thì bài thứ hai được học tệ hơn hẳn, và cả hai đều không có thời gian lắng.

- **Mặc định một bài học mỗi phiên.** Dạy xong thì dừng, kể cả khi người học còn hào hứng — nhất là khi còn hào hứng.
- Nói thẳng ra: *"Dừng ở đây. Việc học phần này còn tiếp diễn sau khi bạn đóng máy."* Đây không phải câu xã giao mà là một phần của phương pháp.
- Đừng xếp sẵn bài kế trong cùng phiên trừ khi người học yêu cầu. Nếu họ yêu cầu, nói rõ đánh đổi rồi làm theo ý họ.
- Giá trị của phiên sau đến từ cổng hồi tưởng ở đầu phiên. Nhồi hết trong một phiên là tự tay cắt mất cái đó.

## Ảo Giác Thành Thạo — Skill Không Được Tự Sinh Ra Chúng

Những thứ tạo cảm giác hiểu mà không tạo trí nhớ. Skill này phải tránh sản xuất chúng:

| Ảo giác | Vì sao dối | Thay bằng |
|---|---|---|
| Đọc lại | Trôi chảy do quen mặt chữ, không phải do nhớ | Hồi tưởng nguội, không mở bài |
| Tô đậm / gạch chân | Cảm giác đã xử lý, thực ra chỉ đánh dấu | Tự viết lại ý bằng lời mình |
| Trắc nghiệm đơn thuần | Kiểm tra **nhận ra**, không kiểm tra **tạo ra** | Kèm câu tự luận và hồi tưởng tự do |
| Xem lời giải mẫu trước khi thử | Đọc lời giải hay tạo cảm giác "tôi cũng nghĩ vậy" | Bắt viết trước, mở đáp án sau |
| Bản tóm tắt cuối bài | Nhắc lại ≠ nhớ lại | Bắt người học tự tóm tắt, rồi mới so |

Hệ quả cụ thể: **không viết mục "Tóm tắt bài học" vào bài học.** Nếu muốn có, hãy đặt một ô nhập trống bảo người học tự tóm tắt trước, rồi mới hiện bản của bạn để đối chiếu.

## Einstellung — Mẫu Cũ Chặn Mẫu Mới

Kiến thức có sẵn không chỉ giúp; nó còn **chặn**. Một trực giác đã thành thục ở lĩnh vực gần sẽ tự động kích hoạt và bịt mất lối nghĩ đúng. Người học càng giỏi lĩnh vực gần thì bẫy càng mạnh — đây là bẫy dành riêng cho người có kinh nghiệm, không phải cho người mới.

Vì vậy: **mỗi bài học phải gọi tên trực giác cũ sẽ dẫn sai, ngay từ đầu bài.**

- Đọc `MISSION.md` và `learning-records/` để biết người học mang sẵn chuyên môn gì.
- Với mỗi khái niệm mới, tự hỏi: *nếu người này áp thẳng mẫu quen của họ vào đây, họ sẽ sai ở đâu?*
- Viết chỗ sai đó ra **trước** khi dạy cách đúng. Đặt câu hỏi hồi tưởng riêng cho nó — trực giác cũ sẽ quay lại, nên nó cần được kiểm nhiều lần hơn kiến thức thường.

Với người học đã thạo một lĩnh vực gần, phần này thường là phần giá trị nhất của cả bài học. Chỗ khó của họ không phải thiếu thông tin, mà là **gỡ một mẫu đang chạy tự động**.
