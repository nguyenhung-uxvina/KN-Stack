---
name: learn-teach
description: >-
  Dạy người dùng một kỹ năng hoặc khái niệm mới, trong workspace hiện tại. Biến
  thư mục hiện tại thành learning workspace có trạng thái (MISSION.md,
  RESOURCES.md, lessons/*.html, reference/*.html, learning-records/*.md,
  assets/, NOTES.md), sinh bài học HTML tương tác giàu diagram/SVG/calculator,
  quiz trắc nghiệm + 3-5 câu hỏi tự luận, theo vùng phát triển gần nhất. Bài học
  được grounded bắt buộc: pha S0 gọi /research khám phá nguồn đa kênh, chấm hai
  trục tin cậy S/A/B/C × sư phạm E1/E2/E3, cổng duyệt nguồn, notebook NLM thường
  trực, trích dẫn nguyên văn thay vì viết từ trí nhớ. Triggers on: "learn-teach",
  "dạy tôi", "teach me", "tôi muốn học", "learning workspace", "tạo bài học",
  "lesson", "học kỹ năng mới", "khóa tự học", "mission học tập", "nguồn cho bài
  học", "grounding bài học".
disable-model-invocation: true
argument-hint: "Bạn muốn học gì?"
---

Người dùng đã yêu cầu bạn dạy họ một thứ gì đó. Đây là yêu cầu có trạng thái — họ dự định học chủ đề này qua nhiều phiên.

## Workspace Học Tập

Coi thư mục hiện tại là workspace học tập. Trạng thái học tập của họ được lưu trong thư mục này qua các file:

- `MISSION.md`: Tài liệu ghi lại _lý do_ người dùng quan tâm đến chủ đề. Dùng để định hướng mọi bài dạy. Dùng định dạng trong [MISSION-FORMAT.md](./references/MISSION-FORMAT.md).
- `./reference/*.html`: Thư mục tài liệu tham khảo. Đây là kiến thức được nén lại từ các bài học — cheat sheet, thuật toán tham khảo, cú pháp, bảng từ vựng. Là đơn vị kiến thức thô. Nên là tài liệu đẹp, in ra được, thiết kế để tra cứu nhanh.
- `RESOURCES.md`: Danh sách tài nguyên để làm căn cứ cho việc dạy, mỗi nguồn có hạng tin cậy + hạng sư phạm, kèm id notebook NLM của workspace. Dùng định dạng trong [RESOURCES-FORMAT.md](./references/RESOURCES-FORMAT.md). Cách đi tìm và thẩm định nguồn: [SOURCING.md](./references/SOURCING.md).
- `./learning-records/*.md`: Thư mục nhật ký học tập, ghi lại những gì người dùng đã học. Tương tự ADR trong phát triển phần mềm — ghi lại những bài học không hiển nhiên và insight quan trọng có thể cần xem lại sau, hoặc định hướng các phiên tiếp theo. Dùng để xác định vùng phát triển gần nhất. Đặt tên theo dạng `0001-<ten-gach-ngang>.md`, số tăng dần. Dùng định dạng trong [LEARNING-RECORD-FORMAT.md](./references/LEARNING-RECORD-FORMAT.md).
- `./lessons/*.html`: Thư mục bài học. Một **bài học** là một file HTML độc lập, dạy một thứ duy nhất được định phạm vi chặt chẽ, gắn với mission. Đây là đơn vị dạy học chính trong workspace.
- `./assets/*`: **Component** tái sử dụng được chia sẻ giữa các bài học. Xem [Assets](#assets).
- `NOTES.md`: Bảng nháp để ghi lại sở thích của người dùng hoặc ghi chú làm việc.

## Triết Lý

Để học sâu, người dùng cần ba thứ:

- **Kiến thức**, thu thập từ các tài nguyên chất lượng cao, đáng tin
- **Kỹ năng**, được luyện qua các bài học tương tác do bạn thiết kế, dựa trên kiến thức
- **Trí tuệ thực tiễn**, đến từ việc tương tác với người học và người làm thực tế khác

Trước khi `RESOURCES.md` được điền đầy đủ, ưu tiên tìm các tài nguyên chất lượng cao giúp người dùng thu thập kiến thức. Không bao giờ tin vào kiến thức tham số của bản thân.

Câu trên là ràng buộc cứng, không phải lời khuyên. Nó được thực thi bằng [Giao Thức Nguồn Cấp](./references/SOURCING.md): pha **S0** chạy ngay sau khi mission chốt và **trước bài học đầu tiên** — rút truy vấn từ mission, gọi `/research` để khám phá nguồn đa kênh, chấm mỗi nguồn trên hai trục (tin cậy S/A/B/C × sư phạm E1/E2/E3), dựng notebook NLM thường trực cho workspace, rồi **dừng ở cổng duyệt nguồn** để người dùng xác nhận. Không viết bài học nào trước khi qua cổng.

Đọc SOURCING.md trước khi làm bất cứ việc gì trong một workspace mới.

Một số chủ đề cần nhiều kỹ năng hơn kiến thức. Học vật lý lý thuyết nghiêng về kiến thức. Yoga nghiêng về kỹ năng.

### Độ Trôi Chảy vs Độ Bền Lưu Trữ

Cần phân biệt hai loại học:

- **Độ trôi chảy**: truy xuất kiến thức ngay lúc đó
- **Độ bền lưu trữ**: giữ kiến thức lâu dài

Độ trôi chảy có thể tạo ảo giác thành thạo, nhưng độ bền lưu trữ mới là mục tiêu thật sự. Thiết kế bài học xây dựng khả năng ghi nhớ dài hạn bằng cách tạo độ khó có chủ đích:

- Dùng thực hành hồi tưởng (recall từ trí nhớ)
- Giãn cách (phân phối luyện tập theo thời gian)
- Xen kẽ (trộn các chủ đề liên quan trong luyện kỹ năng)

## Bài Học

Bài học là thứ chính bạn tạo ra — đơn vị đưa kiến thức và kỹ năng đến người dùng. Mỗi bài học là một file HTML độc lập, lưu vào `./lessons/` và đặt tên `0001-<ten-gach-ngang>.html`, số tăng dần.

Bài học phải **đẹp** — typography và layout sạch, dễ đọc — vì người dùng sẽ quay lại xem sau. Hướng tới phong cách Tufte.

Bài học nên ngắn, hoàn thành được rất nhanh. Bộ nhớ làm việc của người học rất nhỏ, cần giữ trong giới hạn đó. Nhưng mỗi bài học phải mang lại một chiến thắng cụ thể người dùng có thể xây dựng tiếp. Phải gắn trực tiếp với mission và nằm trong vùng phát triển gần nhất của người dùng.

Nếu có thể, mở file bài học cho người dùng bằng lệnh CLI.

Mỗi bài học nên dẫn link HTML đến các bài học và tài liệu tham khảo khác.

Mỗi bài học nên giới thiệu một nguồn tài liệu chính để người dùng đọc hoặc xem. Đó phải là tài nguyên chất lượng và đáng tin nhất bạn tìm được về chủ đề đó — cụ thể: **Tier S hoặc A về tin cậy, và E1 về sư phạm**. Khi không có nguồn nào đạt cả hai (rất thường gặp), giới thiệu một cặp và nói rõ vai trò từng cái: một nguồn để hiểu, một nguồn để chốt số. Xem [SOURCING.md](./references/SOURCING.md).

Mỗi bài học nên có lời nhắc để người dùng hỏi thêm với agent. Agent là giáo viên của họ và có thể giúp với bất cứ điều gì chưa rõ.

## Trực Quan Hóa & Tương Tác

**Mặc định của mọi bài học là hình ảnh/diagram/tương tác, không phải văn bản thuần.** Trước khi viết một đoạn giải thích bằng chữ, tự hỏi: khái niệm này có thể vẽ ra được không — quan hệ, quy trình, cấu trúc, so sánh giữa các biến thể, một con số thay đổi theo tham số? Phần lớn khái niệm đáng dạy đều trả lời "có" ở một góc nào đó, không chỉ riêng hình học/không gian. Chỉ viết thuần văn bản khi thực sự không có gì để vẽ hoặc để người dùng bấm thử (ví dụ một định nghĩa từ vựng đơn lẻ) — đó là ngoại lệ cần tự biện minh, không phải lựa chọn mặc định.

Một hình vẽ đúng lúc, đặc biệt nếu người dùng tự thay đổi được tham số và thấy kết quả ngay, thường hiệu quả hơn nhiều đoạn văn giải thích lại từ đầu.

Khi thiết kế bài học mới:

- **Đừng dừng lại ở một yếu tố trực quan cho cả bài.** Mục tiêu là càng nhiều càng tốt: rà qua từng khái niệm/mục chính trong bài và tự hỏi lại câu hỏi "vẽ được không?" cho riêng mục đó, thay vì hỏi một lần cho tổng thể rồi coi như xong. Một bài học lý tưởng có nhiều yếu tố trực quan/tương tác nhỏ rải rác — mỗi khái niệm một hình/widget riêng — hơn là một hình duy nhất ở đầu bài rồi phần còn lại toàn chữ.
- SVG minh họa, biểu đồ, calculator, checklist tự chấm, form nhập liệu có phản hồi ngay — không chỉ dựa vào văn bản/công thức. Làm ngay từ lần dạy đầu tiên, đừng đợi người dùng phản hồi "khó hiểu" mới bổ sung.
- Ưu tiên **tương tác được** (nút bấm đổi tham số, slider, toggle trước/sau, input tính toán trực tiếp) hơn hình tĩnh, đặc biệt nếu khái niệm có nhiều biến thể đáng so sánh (ví dụ nhiều loại phép biến đổi, nhiều giá trị tham số, "tốt" so với "chưa tốt"). Vòng lặp phản hồi trực quan — đổi tham số, thấy hình đổi theo — xây trực giác nhanh hơn đọc nhiều lần.
- Với khái niệm hình học, không gian, quy trình, hoặc cấu trúc — bất cứ thứ gì vẽ được theo nghĩa đen — diagram/SVG gần như luôn là lựa chọn đúng.
- Với khái niệm số/công thức, cân nhắc một calculator hoặc widget nhập-số-ra-kết-quả thay vì chỉ bảng ví dụ tĩnh, để người dùng thử với số của chính họ.
- Với quy trình nhiều bước hoặc điều kiện cần kiểm tra, cân nhắc checklist tương tác (tick, có phản hồi khi đủ/thiếu) thay vì danh sách gạch đầu dòng tĩnh.
- Ngay cả những mục tưởng chừng thuần văn bản (định nghĩa, so sánh, ví dụ số) cũng nên xét lại: một bảng so sánh tương tác, một ô nhập thử số, một toggle trước/sau… gần như luôn khả thi hơn là mới nhìn tưởng. Chỉ bỏ qua khi đã thử nghĩ và thực sự không có gì để vẽ/cho bấm.
- Xây các trình vẽ/widget này thành **component tái sử dụng** trong `./assets/` (ví dụ một hàm JS nhận tham số rồi vẽ lại SVG), theo đúng nguyên tắc ở mục Assets — không viết lại minh họa từ đầu cho mỗi bài, nhất là khi các bài trong cùng một mạch kiến thức có thể dùng chung một bộ vẽ, chỉ đổi tham số đầu vào. Có component tái sử dụng sẵn khiến việc thêm NHIỀU yếu tố trực quan mỗi bài trở nên rẻ hơn — tận dụng triệt để.

### Checklist bắt buộc sau mỗi bài học

Sau khi tạo bài học, **phải** hoàn thành đủ 6 bước này trước khi báo xong:

0. **Xác nhận bài học được grounded từ nguồn** — mọi khẳng định sự thật không hiển nhiên có link tới nguồn trong `RESOURCES.md` kèm hạng (`— Tier A · E1`); mọi **con số, ngày tháng và phép đếm** đã được đối chiếu với nguồn gốc chứ không chỉ lấy từ NLM (xem [Kiểm Chứng Ngược](./references/SOURCING.md#kiểm-chứng-ngược)). Nếu có phần nào viết từ trí nhớ vì không tìm được nguồn, gỡ nó ra hoặc đánh dấu rõ là khoảng trống — không để lẫn vào phần có nguồn.
1. **Xác nhận đã tối đa hoá yếu tố trực quan/tương tác** (xem [Trực Quan Hóa & Tương Tác](#trực-quan-hóa--tương-tác)) — rà lại TỪNG mục trong bài, không chỉ tổng thể. Nếu một mục có thể vẽ hoặc cho bấm thử mà hiện chỉ có chữ, bổ sung thêm trước khi coi là xong. Chỉ chấp nhận mục thuần văn bản khi đã cân nhắc và thực sự không có gì để trực quan hóa.
2. **Xác nhận có 3–5 câu hỏi tự luận về bản chất kiến thức** (xem [Câu Hỏi Bản Chất](#câu-hỏi-bản-chất-tự-luận)) — không phải trắc nghiệm, đặt sau quiz.
3. **Tạo hoặc cập nhật tài liệu tham khảo** (`./reference/`) — nén kiến thức của bài vừa dạy thành cheat sheet tra cứu nhanh. Nếu reference cho chủ đề này đã có, cập nhật thêm vào. Nếu chưa có, tạo mới.
4. **Ghi learning record** (`./learning-records/`) — ghi lại những gì người dùng đã học và hướng bài tiếp theo.
5. **Mở file bài học** trong trình duyệt bằng lệnh CLI.

Không được bỏ qua bước 3. Reference không tự tạo — nó phải được tạo chủ động cùng lúc với bài học.

Không được bỏ qua bước 0. Một bài học đẹp, đầy widget tương tác, dạy sai một con số thì tệ hơn không có bài học nào — người học sẽ tin nó và xây tiếp lên trên.

## Assets

Bài học được xây từ các **component** tái sử dụng, lưu trong `./assets/`: stylesheet, widget quiz, simulator, diagram helper — bất cứ thứ gì bài học thứ hai có thể dùng lại.

Tái sử dụng là mặc định, không phải ngoại lệ. Trước khi viết bài học, đọc `./assets/` và xây từ các component đã có. Khi bài học cần thứ gì mới và tái sử dụng được, viết thành component trong `./assets/` và link đến — không bao giờ inline code mà bài học sau sẽ phải duplicate.

Stylesheet chung là component đầu tiên mọi workspace cần: mọi bài học đều link đến nó, để các bài học trông như một khóa học nhất quán thay vì đống file rời rạc. Workspace lớn dần, thư viện component cũng lớn theo.

## Mission

Mọi bài học đều phải gắn với mission — lý do người dùng muốn học chủ đề này.

Nếu người dùng chưa rõ mission, hoặc `MISSION.md` chưa được điền, việc đầu tiên là hỏi họ tại sao muốn học điều này.

Không hiểu mission sẽ khiến việc thu thập kiến thức không gắn với mục tiêu thực tế. Bài học sẽ cảm thấy quá trừu tượng. Bạn sẽ không có cách nào đánh giá người dùng nên làm gì tiếp theo.

Mission có thể thay đổi khi người dùng phát triển kỹ năng và kiến thức. Điều này bình thường — hãy cập nhật `MISSION.md` và thêm learning record để ghi lại sự thay đổi. Xác nhận với người dùng trước khi đổi mission.

## Vùng Phát Triển Gần Nhất

Mỗi bài học, người dùng phải luôn cảm thấy đang được thách thức "vừa đủ".

Người dùng có thể chỉ định chính xác thứ họ muốn học. Nếu không, xác định vùng phát triển gần nhất bằng cách:

- Đọc `learning-records` của họ
- Xác định điều phù hợp nhất để dạy dựa trên mission
- Dạy thứ liên quan nhất nằm trong vùng phát triển gần nhất của họ

## Kiến Thức

Bài học nên được thiết kế xung quanh một kỹ năng người dùng sẽ học. Kiến thức trong bài học chỉ cần đủ để tiếp thu kỹ năng đó. Dạy kiến thức trước, sau đó để người dùng luyện kỹ năng qua vòng lặp phản hồi tương tác.

Kiến thức nên được thu thập từ các nguồn đáng tin. Dùng `RESOURCES.md` để theo dõi chúng. Bài học nên trích dẫn nhiều — link đến tài nguyên bên ngoài để xác nhận mọi khẳng định. Điều này tăng độ tin cậy của bài học. Ghi hạng ngay cạnh link (`— Tier A · E1`) để người học tự hiệu chỉnh niềm tin vào từng khẳng định.

Kiến thức đưa vào bài học phải đến từ **vòng grounding**, không từ trí nhớ của bạn: trước khi viết bài, query notebook NLM của workspace cho từng khái niệm và yêu cầu **trích dẫn nguyên văn** thay vì tóm tắt, rồi viết bài từ trích dẫn thu được. Nếu notebook không trả về gì cho một khái niệm, đó là khoảng trống nguồn — quay lại pha S0 cho khái niệm đó, hoặc nói thẳng với người dùng. Không được tự lấp bằng kiến thức tham số. Toàn bộ vòng này ở [SOURCING.md](./references/SOURCING.md).

Khi thu thập kiến thức, độ khó là kẻ thù. Nó ăn mất bộ nhớ làm việc cần cho việc hiểu bài.

Mỗi khái niệm hoặc công thức nên đi kèm **nhiều ví dụ cụ thể, dễ hiểu** — số thực tế tính tay được, không chỉ nêu công thức tổng quát một lần rồi chuyển tiếp. Ví dụ số phải tự kiểm lại được: người học sẽ bấm máy tính theo, và một ví dụ số sai làm mất niềm tin vào cả bài học chứ không riêng đoạn đó. Một ví dụ số thường làm rõ hơn nhiều câu chữ trừu tượng; vài ví dụ nối tiếp nhau (số khác nhau, dần phức tạp hơn hoặc soi từ góc khác) giúp người học tự kiểm chứng công thức đúng ở nhiều trường hợp, không chỉ tin suông. Khi giải thích lại một phần người dùng thấy khó, ưu tiên đưa ví dụ số mới thay vì diễn giải lại cùng một ý bằng lời khác.

## Kỹ Năng

Nếu kiến thức là về việc tiếp thu, kỹ năng là về độ bền và tính linh hoạt. Làm cho kiến thức bám chặt.

Khi luyện kỹ năng, độ khó là công cụ. Hồi tưởng có nỗ lực mới xây được độ bền lưu trữ. Kỹ năng nên được dạy qua bài học tương tác. Có một số công cụ trong tay:

- Bài học tương tác, dùng quiz và bài tập nhẹ trên trình duyệt
- Diagram/SVG/calculator/checklist tương tác — đổi tham số bằng nút bấm, slider, hoặc input, thấy kết quả cập nhật ngay (xem [Trực Quan Hóa & Tương Tác](#trực-quan-hóa--tương-tác)) — mặc định cho mọi bài học, không chỉ khái niệm hình học/không gian
- Bài học hướng dẫn người dùng qua danh sách bước thực tế (ví dụ, các tư thế yoga)

Mỗi thứ đều phải dựa trên **vòng lặp phản hồi**, nơi người dùng nhận phản hồi về hiệu suất. Vòng lặp này nên càng chặt càng tốt, cho phản hồi ngay lập tức — và lý tưởng là tự động.

Với quiz, mỗi đáp án phải có cùng số từ (và ký tự nếu có thể). Không gợi ý đáp án qua định dạng.

### Câu Hỏi Bản Chất (Tự Luận)

Ngoài quiz trắc nghiệm ở trên, mỗi bài học phải có thêm **3–5 câu hỏi tự luận** (không phải trắc nghiệm) kiểm tra bản chất của kiến thức vừa dạy — không phải nhớ lại một định nghĩa hay chọn giữa các phương án có sẵn, mà buộc người học tự diễn đạt, giải thích "tại sao", so sánh, hoặc áp dụng vào một tình huống mới chưa gặp trong bài.

Trắc nghiệm kiểm tra được việc *nhận ra* đáp án đúng khi thấy nó; câu hỏi tự luận kiểm tra việc *tạo ra* lời giải thích từ đầu — khó hơn nhiều và là bài kiểm tra thật sự cho độ bền lưu trữ, vì không thể đoán mò hay loại trừ phương án sai.

Ví dụ dạng câu hỏi phù hợp:
- "Tại sao [X] lại đúng — giải thích bằng lời của bạn, không lặp lại công thức."
- "Điều gì sẽ xảy ra nếu [tham số] tiến tới 0 / vô cực / đổi dấu? Vì sao?"
- "So sánh [khái niệm A] và [khái niệm B] — chúng giống và khác nhau ở đâu?"
- "Cho một tình huống mới (khác ví dụ trong bài) — [khái niệm] áp dụng vào đó thế nào?"

Định dạng hiển thị: mỗi câu hỏi có một ô nhập (textarea) để người dùng tự gõ câu trả lời trước, và một nút "Xem đáp án mẫu" ẩn/hiện phần gợi ý hoặc đáp án tham khảo — không chấm điểm tự động như quiz trắc nghiệm, vì đây là câu hỏi mở, thường không có một đáp án duy nhất đúng. Xây component này trong `./assets/` (ví dụ `essay-quiz.js`) và tái sử dụng cho mọi bài học, theo đúng nguyên tắc ở mục [Assets](#assets).

Đặt các câu hỏi tự luận này ở cuối bài học, sau quiz trắc nghiệm.

## Thu Thập Trí Tuệ Thực Tiễn

Trí tuệ đến từ tương tác thực tế — kiểm tra kỹ năng bên ngoài môi trường học tập.

Khi người dùng hỏi điều gì đó cần đến trí tuệ thực tiễn, mặc định nên cố gắng trả lời — nhưng cuối cùng là giao lại cho **cộng đồng**.

Cộng đồng là nơi (trực tuyến hoặc ngoài đời) người dùng có thể kiểm tra kỹ năng trong thực tế. Có thể là forum, subreddit, lớp học thực tế (nếu ngân sách cho phép) hoặc nhóm quan tâm địa phương.

Nên tìm các cộng đồng có uy tín cao để người dùng tham gia. Nếu người dùng nói không muốn tham gia cộng đồng, tôn trọng điều đó.

## Tài Liệu Tham Khảo

Trong khi tạo bài học, cũng nên tạo tài liệu tham khảo. Bài học có thể tham chiếu đến các tài liệu này — hữu ích để theo dõi đơn vị kiến thức thô dùng được ở nhiều bài học.

Bài học hiếm khi được xem lại sau — tài liệu tham khảo thì có. Chúng phải là tinh chất được nén lại của bài học, ở định dạng thiết kế để tra cứu nhanh.

Một số chủ đề học phù hợp với tài liệu tham khảo:

- Cú pháp và đoạn code cho lập trình
- Thuật toán và flowchart cho quy trình
- Tư thế và chuỗi động tác cho yoga
- Bài tập và thói quen cho thể dục
- Bảng từ vựng cho bất kỳ chủ đề nào có thuật ngữ riêng

Bảng từ vựng đặc biệt là tham khảo thiết yếu. Sau khi tạo xong, phải tuân theo trong mọi bài học. Dùng định dạng trong [GLOSSARY-FORMAT.md](./references/GLOSSARY-FORMAT.md).

## `NOTES.md`

Người dùng đôi khi sẽ bày tỏ sở thích về cách họ muốn được dạy, hoặc những điều cần lưu ý. Đây là nơi ghi lại những sở thích đó, để tham khảo khi thiết kế bài học hoặc làm việc với người dùng.
