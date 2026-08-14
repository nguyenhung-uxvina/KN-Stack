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

## S0 — Pha Nguồn Cấp

Chạy **sau** khi `MISSION.md` chốt, **trước** khi viết bài học đầu tiên. Không có ngoại lệ "bài đầu dễ, viết tạm rồi bổ sung nguồn sau" — bài học viết từ trí nhớ model sẽ không bao giờ được kiểm lại.

1. **Rút truy vấn từ mission.** Mỗi gạch đầu dòng trong "Thành Công Trông Như Thế Nào" là một vùng kiến thức cần phủ. 3–6 truy vấn. Nếu không rút được truy vấn nào cụ thể, mission còn quá mơ hồ — quay lại phỏng vấn người dùng.

2. **Gọi `/research <vùng kiến thức>`** cho từng vùng lõi. Chạy theo vùng, đừng gộp cả chủ đề vào một cú — kết quả sẽ nông và lệch. `/research` trả về nguồn đã phân hạng S/A/B/C từ 5 kênh (Exa ngữ nghĩa, Web, YouTube, authority domain, patent) và tự dựng notebook NLM.

3. **Gán trục E cho từng nguồn.** `/research` không làm việc này — nó không biết mục đích là dạy học. Đây là việc riêng của learn-teach. Với nguồn chưa đọc, mở xem thật rồi chấm; đừng đoán E từ tên miền.

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

Khi nền nguồn đổi đáng kể, ghi một learning record: nó thay đổi những gì dạy được tiếp theo, đúng tiêu chí "hệ quả" của [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md).
