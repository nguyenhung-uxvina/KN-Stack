# Giao Thức Nguồn Cấp

Một bài học chỉ tốt bằng nguồn nuôi nó. Chỉ thị "tìm tài nguyên chất lượng cao" tự nó không kiểm chứng được — không có cách nào biết đã làm hay chưa. File này biến nó thành quy trình có cổng, có bằng chứng, có tiêu chí trượt.

Nguyên tắc gốc không đổi: **không bao giờ tin vào kiến thức tham số của bản thân.** Mọi thứ dưới đây tồn tại để thực thi câu đó.

## Hai Trục Đánh Giá Nguồn

Một nguồn dùng cho dạy học phải được chấm trên **hai** trục độc lập. Chấm thiếu một trục là lỗi phổ biến nhất.

### Trục 1 — Độ Tin Cậy (S / A / B / C)

Dùng nguyên hệ phân hạng của pipeline nghiên cứu. **Không chép lại vào đây** — bản gốc là nguồn chân lý duy nhất, chép ra là bảo đảm hai bản sẽ trôi khỏi nhau.

Đọc bằng Skill tool: **`research:references:source-tiers`**. Dùng đường này, không dùng đường dẫn tương đối.

> Đường dẫn tương đối vượt ra ngoài thư mục skill **không đáng tin** ở đây. Skill được triển khai bằng junction, và `..` cho kết quả khác nhau tuỳ độ sâu: một cấp thì dereference sang đích thật trong repo, hai cấp thì quay về `~/.claude/commands/` nơi các skill nằm phẳng (`research/`, không phải `galaxy/research/`). Không tồn tại chuỗi `../` nào đúng ở cả hai bối cảnh. Nếu cần chỉ chỗ cho người đọc, ghi đường dẫn từ gốc repo — `skills/galaxy/research/references/source-tiers.md` — như một chỉ dẫn, đừng biến nó thành link tương đối.

Tóm tắt để nhớ: **S** chuẩn/sơ cấp (MIL-STD, IEEE, TCVN, patent, paper bình duyệt) · **A** thẩm quyền/OEM (app note, whitepaper, datasheet, DTIC) · **B** chuyên nghiệp (blog kỹ thuật, talk hội nghị, YouTube có credential) · **C** cộng đồng (forum, Reddit, tutorial vô danh — chỉ để đối chiếu chéo).

> **Với chủ đề công cụ và sản phẩm, Tier S không tồn tại — đừng đi săn.** Không có chuẩn hay công trình bình duyệt nào về một phần mềm ra mắt năm ngoái. Ở những chủ đề này **nhà sản xuất chính là nguồn gốc**, nên tài liệu chính hãng (docs, changelog, trang hỗ trợ) đóng vai trò của S: nó vừa là thẩm quyền cao nhất, vừa là thứ duy nhất định nghĩa được sự thật. Luật "mỗi vùng ≥1 nguồn S/A" khi đó thoả bằng A, và thế là đủ. Nhận ra sớm điều này để khỏi đốt một vòng tìm kiếm vô vọng.

### Trục 2 — Giá Trị Sư Phạm (E1 / E2 / E3)

Trục này không có trong pipeline nghiên cứu vì nghiên cứu không cần nó. Dạy học thì cần.

| Hạng | Nghĩa | Dấu hiệu | Dùng để |
|---|---|---|---|
| **E1** | **Giảng được** | Xây từ nền lên, có ví dụ số làm tay được, có hình, lường trước chỗ người mới vấp | Lấy **xương sống** của bài học |
| **E2** | **Tra được** | Đúng và đầy đủ nhưng khô — chuẩn, spec, datasheet, paper | **Chốt** sự thật, số, ngưỡng, định nghĩa |
| **E3** | **Mồi được** | Không đủ dạy, nhưng nêu vấn đề, cho trực giác, cho bối cảnh thực tế | **Mở** bài, cho ví dụ đời thật, cho lý do quan tâm |

### Bẫy Của Việc Chỉ Nhìn Trục 1

**Tier cao không có nghĩa dạy tốt.** Một MIL-STD là Tier S — chính xác tuyệt đối, và là thảm hoạ khi dạy người mới. Một cuốn giáo trình hay có thể chỉ là Tier B mà lại là thứ duy nhất thật sự dạy được khái niệm đó.

Đây chính là lý do phải có trục E. Nếu bê nguyên hệ tier nghiên cứu sang dạy học rồi luôn ưu tiên tier cao nhất, bài học sẽ chính xác và không ai học nổi.

Công thức: **xương từ E1, sự thật từ S/A, ví dụ đời từ E3.**

Hệ quả cần chấp nhận: một nguồn `B · E1` có thể là nguồn quan trọng nhất của cả workspace. Được phép — miễn là mọi con số lấy từ nó đều được một nguồn S/A chốt lại (xem [Kiểm Chứng Ngược](#kiểm-chứng-ngược)).

## Độ Tươi — Thứ Hai Trục Không Bắt Được

Hai trục trên chấm **nguồn**. Chúng không nói gì về việc nguồn đó còn đúng hay không. Một bài viết có thể được chấm `A · E1` hoàn toàn chính xác vào lúc chấm, và đang nói sai sự thật ngay lúc bạn dạy.

Chỗ cắt đúng không phải "nguồn cũ / nguồn mới", mà là **loại sự thật**:

| Loại | Ví dụ | Trôi theo thời gian? |
|---|---|---|
| **Sự thật bền** | Khái niệm, nguyên lý, vì sao thứ này tồn tại, nó giải quyết vấn đề gì, đánh đổi thiết kế | Gần như không |
| **Sự thật dễ trôi** | Ai dùng được, gói/giá, nền tảng hỗ trợ, giới hạn số, tên nút, các bước thao tác, tính năng có/không | Rất nhanh |

Cùng một nguồn có thể **vừa quý vừa độc**: một bài ra mắt sản phẩm là nguồn tốt để hiểu *vì sao* thứ đó được tạo ra (bền), và là nguồn tệ để nói *ai dùng được nó* (trôi). Loại bỏ cả nguồn là phí; tin cả nguồn là nguy.

**Luật:**

1. **Sự thật dễ trôi chỉ được lấy từ nguồn sống của chính nhà sản xuất** — tài liệu chính thức, changelog, trang hỗ trợ. Không lấy từ báo chí, video, hay blog, bất kể tier và hạng E cao đến đâu.
2. **Ở S0, xác định "trọng tài độ tươi"** của chủ đề: một nguồn sống duy nhất phân xử câu hỏi *"hiện tại đúng là gì"*. Với sản phẩm phần mềm thường là changelog hoặc trang docs. Ghi nó vào `RESOURCES.md`. Khi hai nguồn đá nhau về sự thật dễ trôi, trọng tài thắng, không cần tranh luận.
3. **Ghi ngày kiểm** cho mọi nguồn có mang sự thật dễ trôi. Nguồn không có ngày kiểm thì không được trích số, ngày tháng, hay các bước thao tác.
4. **Chủ đề càng mới thì càng nguy.** Với thứ ra mắt trong vòng 12 tháng, mặc định giả định mọi nguồn không phải của nhà sản xuất đều đã lạc hậu về sự thật dễ trôi — kiểm trước khi dùng, đừng kiểm sau khi người học phát hiện.

Dấu hiệu bạn vừa dính bẫy này: nguồn nói "hiện đang là bản xem trước / chỉ dành cho gói cao nhất / sắp có trên nền tảng X". Mọi câu có thì hiện tại về tình trạng sản phẩm đều là sự thật dễ trôi.

## S0 — Pha Nguồn Cấp

Chạy **sau** khi `MISSION.md` chốt, **trước** khi viết bài học đầu tiên. Không có ngoại lệ "bài đầu dễ, viết tạm rồi bổ sung nguồn sau" — bài học viết từ trí nhớ model sẽ không bao giờ được kiểm lại.

### Khi mission chưa được xác nhận

Đừng chặn cứng chờ người dùng trả lời. Nếu bạn có đủ bối cảnh để đoán mission một cách có căn cứ:

- Soạn `MISSION.md` **bản tạm**, mở đầu bằng một khối cảnh báo ghi rõ đây là suy đoán, dựa trên gì, và rằng nó phải được xác nhận trước bài học đầu tiên.
- Chạy tiếp S0 bình thường trên mission tạm đó.
- **Đưa mission ra duyệt cùng lúc với bảng nguồn ở bước 5** — người dùng chỉ phải dừng lại một lần, và họ sửa mission dễ hơn nhiều khi đã thấy nó kéo theo bộ nguồn nào.
- Sau khi được xác nhận, thay khối cảnh báo bằng dòng ghi ngày xác nhận.

Chỉ chặn cứng khi bạn không có bối cảnh nào để đoán — lúc đó một câu hỏi thẳng rẻ hơn một vòng S0 sai hướng.

### Các bước

1. **Rút truy vấn từ mission.** Mỗi gạch đầu dòng trong "Thành Công Trông Như Thế Nào" là một vùng kiến thức cần phủ. 3–6 truy vấn. Nếu không rút được truy vấn nào cụ thể, mission còn quá mơ hồ — quay lại phỏng vấn người dùng.

2. **Gọi `/research <vùng kiến thức>`** cho từng vùng lõi. Chạy theo vùng, đừng gộp cả chủ đề vào một cú — kết quả sẽ nông và lệch. `/research` trả về nguồn đã phân hạng S/A/B/C từ 5 kênh (Exa ngữ nghĩa, Web, YouTube, authority domain, patent) và tự dựng notebook NLM.

3. **Gán trục E cho từng nguồn.** `/research` không làm việc này — nó không biết mục đích là dạy học. Đây là việc riêng của learn-teach. Với nguồn chưa đọc, mở xem thật rồi chấm; đừng đoán E từ tên miền.

3b. **Chỉ ra trọng tài độ tươi.** Trong đống nguồn vừa tìm, nguồn sống nào của chính nhà sản xuất sẽ phân xử câu hỏi "hiện tại đúng là gì"? Mở nó ra đọc ngay ở bước này và đối chiếu với những gì các nguồn khác đang khẳng định — mâu thuẫn về sự thật dễ trôi phải được phát hiện **trước** cổng duyệt, không phải giữa lúc soạn bài. Xem [Độ Tươi](#độ-tươi--thứ-hai-trục-không-bắt-được).

4. **Chấm phủ.** Mỗi vùng kiến thức phải có **≥1 nguồn E1** và **≥1 nguồn S hoặc A**. Vùng nào thiếu một trong hai → đó là khoảng trống, ghi ra, đừng lấp bằng kiến thức tham số.

5. **CỔNG DUYỆT NGUỒN — dừng lại.** Trình cho người dùng bảng nguồn nhóm theo vùng kiến thức, mỗi dòng có tier + hạng E + một câu nói nó bao quát gì. Nêu rõ khoảng trống còn lại. Hỏi: đủ chưa, có nguồn nào bạn muốn thêm/bỏ không. **Không viết bài học nào trước khi qua cổng này.** Người dùng thường biết một cuốn sách hay một người thầy mà không công cụ nào tìm ra.

6. **Ghi `RESOURCES.md`** theo định dạng trong [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md), kèm phần `## Khoảng Trống`.

### Khi Hạ Tầng Không Có

Thang giảm cấp, giữ nguyên tinh thần:

| Thiếu | Làm thay |
|---|---|
| Exa | `/research` tự fallback sang WebSearch — không phải làm gì |
| Cả `/research` | WebSearch trực tiếp theo truy vấn authority domain trong `source-tiers.md`, gán tier tay theo heuristic URL |
| NLM | Bỏ notebook, đọc nguồn tại chỗ bằng WebFetch lúc soạn bài. Cổng duyệt nguồn và hai trục **vẫn giữ nguyên** |

Cổng duyệt nguồn không bao giờ được bỏ, kể cả khi mọi công cụ đều hỏng.

## Notebook Thường Trực

Một notebook cho một workspace, tạo ở bước S0. Đây là kho kiến thức bền của workspace — nguồn đã duyệt nằm trong đó, không nằm trong trí nhớ model.

```bash
nlm notebook create "Learn: {Chủ Đề}"
nlm alias set learn-{slug} {notebook-id}

# Nạp nguồn — LƯU Ý hai chỗ dễ sai:
#   • URL phải đi sau cờ -u (hoặc -y cho YouTube); URL trần bị từ chối
#   • KHÔNG trộn -u với -y trong cùng một lệnh → "Please specify only one source type at a time"
nlm source add {notebook-id} -u "https://…" -u "https://…"
nlm source add {notebook-id} -y "https://youtu.be/…" -y "https://youtu.be/…"
```

`nlm` đã có sẵn trên PATH. Ghi notebook id vào `RESOURCES.md` để phiên sau tìm lại được.

Nạp toàn bộ nguồn đã qua cổng. NLM đọc được PDF, trang có paywall và YouTube — những thứ WebFetch thường chịu thua. Trần 300 nguồn/notebook là cứng và **im lặng** khi chạm; workspace học tập hiếm khi tới gần, nhưng đừng đổ cả kết quả research thô vào.

Query phải chạy bất đồng bộ: `notebook_query` chết cứng ở 120s và bỏ qua tham số timeout. Dùng `notebook_query_start` rồi `notebook_query_status`.

## Vòng Grounding Trước Mỗi Bài

Trước khi viết bài học thứ N:

1. Xác định các khái niệm bài này sẽ dạy.
2. Query notebook cho từng khái niệm, và **yêu cầu trích dẫn nguyên văn**, không yêu cầu tóm tắt: *"Giải thích {khái niệm}. Trích nguyên văn đoạn trong nguồn nói điều đó, kèm tên nguồn."*
3. Viết bài từ trích dẫn thu được. Không từ trí nhớ model.
4. Nếu notebook trả rỗng hoặc không trích được gì — **đó là khoảng trống, không phải giấy phép tự viết.** Quay lại S0 cho riêng khái niệm đó, hoặc nói thẳng với người dùng rằng phần này chưa có nguồn.

Bước 4 là chỗ giao thức này sống hay chết. Sức ép để "cứ viết đại phần nhỏ này" luôn có, và luôn phải bị từ chối.

## Kiểm Chứng Ngược

NLM **bịa ngày tháng, bịa số, và đếm sai thực thể** ngay cả khi phần trích dẫn trông tử tế và đúng định dạng. Ba loại dữ kiện sau tuyệt đối không được vào bài học từ NLM mà không đối chiếu:

- **Con số** — hằng số, ngưỡng, kích thước, giá, tỉ lệ
- **Ngày tháng** — năm ban hành, mốc lịch sử, phiên bản
- **Phép đếm** — "có 5 loại…", "gồm 3 giai đoạn…"

Đối chiếu bằng cách mở thẳng nguồn gốc (`source_get_content`, WebFetch, hoặc đọc file). **Không** đối chiếu bằng cách hỏi lại NLM "có chắc không" — mô hình sẽ vui vẻ xác nhận đúng cái nó vừa bịa. Kiểm chứng phải đến từ bên ngoài hệ thống vừa sinh ra khẳng định đó.

### Số trích dẫn của NLM không đáng tin — đoạn trích thì đáng

Các marker `[1] [2] [3]` trong câu trả lời của NLM **lệch so với bảng nguồn kèm theo**: marker trỏ sang một source, còn đoạn trích thực sự lại thuộc source khác. Đoạn trích nguyên văn và tên nguồn NLM ghi trong phần trả lời thì đúng.

Luật: **tin đoạn trích và tên nguồn, không tin con số.** Khi cần biết chính xác một khẳng định đến từ đâu, tìm đoạn trích đó trong bảng `references` theo nội dung, đừng tra theo số.

### Khi hai công cụ kiểm chứng đá nhau

Chuyện này xảy ra thật: bản tóm tắt của máy tìm kiếm và bản đọc thẳng trang cho hai con số khác nhau cho cùng một câu hỏi.

Thứ tự phân xử, từ mạnh xuống yếu:

1. **Đọc thẳng trang gốc** (WebFetch, `source_get_content`) — thắng tất cả
2. **Trọng tài độ tươi** của chủ đề, nếu đây là sự thật dễ trôi
3. Bản tóm tắt do máy tìm kiếm sinh ra — **không bao giờ dùng một mình để chốt một con số**

Nếu sau cả ba vẫn không phân xử được: **đừng dạy con số đó.** Ghi vào `## Khoảng Trống` như một mâu thuẫn chưa giải quyết và dạy phần cấu trúc mà mọi nguồn đều đồng ý. Một bài học thiếu một con số vẫn dùng được; một bài học có con số sai thì không.

Quy tắc này áp cho cả ví dụ số trong bài học: mục "Kiến Thức" đòi nhiều ví dụ số làm tay được, và một ví dụ số sai còn tệ hơn không có ví dụ nào — người học sẽ tự kiểm tra bằng máy tính rồi mất niềm tin vào cả bài.

## Trích Dẫn Trong Bài Học

- **Mọi khẳng định sự thật không hiển nhiên đều link tới nguồn** trong `RESOURCES.md`. Đây là thứ tách một bài học khỏi một bài viết trôi nổi.
- **Ghi hạng ngay cạnh link** để người học tự hiệu chỉnh niềm tin: `[Tên nguồn](url) — Tier A · E1`. Người học cần biết cái nào là chuẩn quốc gia, cái nào là blog hay.
- **Nguồn chính của mỗi bài** (mục "giới thiệu một nguồn tài liệu chính" trong SKILL.md) phải **S hoặc A về tin cậy, VÀ E1 về sư phạm**.
- Nếu không tồn tại nguồn nào vừa S/A vừa E1 — trường hợp rất thường gặp — thì **giới thiệu một cặp** và nói rõ vai trò: *"Đọc {E1} để hiểu, đối chiếu {S/A} để chốt số."* Đừng ép một nguồn gánh cả hai vai.

## Khi Nào Chạy Lại S0

- **Mission đổi** — nguồn cũ có thể không còn phục vụ mục tiêu mới.
- **Vùng phát triển gần nhất đi sang lãnh thổ chưa được phủ** — kiểm phủ trước khi soạn, không phải sau.
- **Hai nguồn mâu thuẫn** — xử theo luật xung đột trong `source-tiers.md` (C chọi S/A → gắn ★ thấp; B chọi S/A → đưa người dùng quyết; S chọi A → khoảng trống nghiên cứu, cả hai có thể đúng).
- **Người dùng hỏi thứ notebook không trả lời được** — đó là tín hiệu phủ thiếu, không phải lúc ứng khẩu.
- **Một nguồn hoá ra sai hoặc nông** — cắt tỉa quyết đoán theo RESOURCES-FORMAT, đừng chôn nó ở cuối danh sách.
- **Sự thật dễ trôi đã quá hạn kiểm** — với chủ đề đang phát triển nhanh, mở trọng tài độ tươi ra đối chiếu trước khi dạy lại bất cứ con số, gói, nền tảng hay thao tác nào. Bài học cũ không tự hỏng có tiếng động.

Khi nền nguồn đổi đáng kể, ghi một learning record: nó thay đổi những gì dạy được tiếp theo, đúng tiêu chí "hệ quả" của [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
