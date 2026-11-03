# Bốn Mức Nguyên Bản — Mỗi Mức Là Một Cách Viết Khác, Không Phải Một Con Số Khác

> Đọc trước P3 và P4. Trần ở P7 chỉ là hệ quả; thứ thật sự khác nhau giữa các mức là **agent viết
> được phép làm gì với lời của tác giả**.

## Chọn mức bằng mục đích đọc, không bằng độ dài mong muốn

| Hỏi mình câu này | Thì chọn |
|---|---|
| "Cuốn này có đáng đọc cả không? Cho tôi cái sườn để quyết." | **F1** |
| "Ý này áp vào Xưởng X thì thành cái gì?" | **F2** |
| "Tôi cần theo đúng mạch lập luận của ông ấy, nhưng bằng tiếng Việt và có chú giải." | **F3** |
| "Tôi cần biết chính xác ông ấy viết gì, từng đoạn." | **F4** |

Cái bẫy hay gặp: chọn F3/F4 vì *cảm giác* trung thành thì an toàn hơn. Ngược lại — **mức càng cao,
tác phẩm phái sinh càng gần bản sao, rủi ro càng lớn và giá trị dùng được càng nhỏ.** F2 gần như
luôn là mức cho tỷ lệ giá trị/rủi ro cao nhất. Chọn F4 chỉ khi mục đích đúng là *đọc hiểu lời tác
giả*, và khi đó cuốn sách ở lại trên máy.

## Bảng đối chiếu theo pha

| | **F1 Lược thuật** | **F2 Diễn giải ứng dụng** | **F3 Trung thành theo chương** | **F4 Sát nguyên bản** |
|---|---|---|---|---|
| **P2 luận đề** | Luận đề **của mình**, sách là bằng chứng | Luận đề của mình, đặt cạnh luận đề của tác giả | Luận đề **của tác giả**, phát biểu lại cho rõ | Không có luận đề riêng |
| **P3 dàn ý** | Tự do; gộp/tách thoải mái | Tự do; bảng ánh xạ nguồn khuyến nghị | **Ánh xạ 1-1** với mục lục gốc, bắt buộc | Y nguyên mục lục gốc |
| **P4 lời văn** | Hoàn toàn lời mình | Lời mình + trích neo ngắn ở chỗ then chốt | Diễn đạt lại từng đoạn + trích khi câu gốc không thay được | Dịch sát, giữ cấu trúc câu |
| **P4 ví dụ** | Bỏ ví dụ gốc, thay bằng ví dụ Xưởng X | Giữ 1 ví dụ gốc + thêm 1 ví dụ Xưởng X | Giữ ví dụ gốc, chú giải thêm | Giữ nguyên |
| **P4 "Apply This"** | Bắt buộc, là phần chính | Bắt buộc | Tuỳ chọn, tách khối riêng có nhãn | **Không** — chèn ý mình vào bản dịch là xuyên tạc |
| **Trần bao phủ** | 2% | 8% | 20% | mù |
| **Trần mật độ** | 3% | 10% | 25% | mù |
| **P8 NotebookLM** | bật | bật | tắt mặc định | tắt, không bật được bằng cờ |

## Ngân sách trích cho từng chương — phát bằng SỐ TỪ

Đừng bảo agent viết "trích ít thôi". Tính ra số rồi phát:

```
ngân sách toàn sách (từ) = từ_sách_gốc × trần_bao_phủ
ngân sách một chương      = ngân sách toàn sách ÷ số chương × hệ số chương
```

`hệ số chương` mặc định 1,0; nâng lên 1,5 cho 2–3 chương mà lời tác giả là thứ không thay được
(định nghĩa, phát biểu nguyên tắc), và hạ xuống 0,5 cho các chương ứng dụng.

**Ví dụ thật (Cross 5e):** sách gốc 59.792 từ, 18 chương, khai F2 → ngân sách 59.792 × 8% = 4.783 từ
→ ~266 từ/chương. Cuốn đã chạy dùng **9.606 từ**, gấp đôi. Và lượng ấy **dồn cục**: 4 chương gánh
38,5% tổng lượng (Ch.08 mật độ 12,0% · Ch.05 11,2% · Ch.15 10,3% · Ch.03 10,2%). Không phát ngân
sách thì lượng trích không trải đều — nó tụ vào những chương agent thấy khó diễn đạt lại nhất.

**Quy tắc phụ:** không trích nào quá **40 từ**. Ở Cross, trích dài nhất chỉ 59 từ mà tổng vẫn vượt —
vấn đề luôn là tổng lượng. Nhưng cắt 33 trích ≥40 từ hạ được ~1.400 từ (16,07% → ~13,7%), nên trần
độ dài vẫn là cần gạt rẻ nhất khi cần hạ gấp.

## Câu chỉ thị phát cho agent viết (P4), theo mức

**F1:**
> Viết bằng lời của bạn. Không mở ngoặc kép quanh câu nào của tác giả trừ khi cả chương không có
> cách nào khác — ngân sách trích của chương này là **{{N}} từ**. Mỗi ý gốc phải đi kèm một câu trả
> lời cho *"vậy CEO làm gì với nó"*. Nếu một đoạn không trả lời được câu đó, cắt đoạn ấy.

**F2:**
> Ngân sách trích: **{{N}} từ**, chỉ dùng cho câu mà diễn đạt lại sẽ làm mất nghĩa. Mỗi trích phải
> kèm số trang in. Sau mỗi ý gốc, viết một đoạn *"ở Xưởng X"* nối vào sản phẩm hoặc quy trình cụ
> thể — không nối được thì nói thẳng là không nối được, đừng bịa ra liên hệ.

**F3:**
> Bám trình tự lập luận của chương gốc {{ch}} (trang {{a}}–{{b}}). Diễn đạt lại từng đoạn bằng tiếng
> Việt; giữ ví dụ gốc. Ngân sách trích **{{N}} từ**. Mọi bổ sung của người viết phải nằm trong khối
> `> **Chú giải của người biên soạn:**` — người đọc phải phân biệt được đâu là tác giả, đâu là ta.

**F4:**
> Dịch sát đoạn {{a}}–{{b}}. Giữ cấu trúc câu và thuật ngữ; chú thích thuật ngữ ở cước chú, không
> sửa trong thân. **Không thêm ví dụ, không thêm liên hệ, không thêm mục "Apply This".** Chỗ nào bản
> gốc tối nghĩa thì giữ nguyên độ tối nghĩa và ghi chú, đừng "sửa giúp" tác giả.

## Hai thước đo, và vì sao phải có cả hai

- **bao phủ** = từ nguyên văn ÷ **từ sách gốc**. Trả lời: *tôi tái tạo bao nhiêu phần tác phẩm của
  người ta.* Đây là câu hỏi bản quyền. Sách phái sinh càng dài thì số này càng tăng.
- **mật độ** = từ nguyên văn ÷ **từ sách mình**. Trả lời: *bao nhiêu phần cuốn này không phải của
  tôi.* Đây là câu hỏi đóng góp. Sách càng dài thì số này càng loãng.

Cross đo được **bao phủ 16,07% · mật độ 6,0%** — một cuốn có thể *trông* rất gốc (94% là đóng góp
riêng) mà vẫn tái tạo 1/6 tác phẩm nguồn. Chỉ nhìn mật độ thì yên tâm sai. Cổng bắt cả hai cùng đạt.

## Dạng phơi lộ mà không thước nào bắt được

Ở Cross, phơi lộ nguy hiểm nhất **không phải trích dẫn**: cổng G1–G4 của Xưởng xuất hiện ở 13/18
chương, HELIX ở 11/18, một chương có 26 chỗ định vị danh mục sản phẩm trên ma trận đẩy/kéo — trong
khi **0 lần** chạm nhãn mật (V-SMASH / Verdict / Bastion / Sentinel / Kairos / hoả lực).

Nghĩa là: quét tên sản phẩm sạch trơn mà cuốn sách vẫn để lộ **cách Xưởng vận hành**. Hai trục hoàn
toàn độc lập — ở Cross, hai chương *an toàn nhất về nhãn mật* lại là hai chương *trích nhiều nhất*.

Với mức F1/F2 (nhiều liên hệ Xưởng X) thì trục quy trình là trục đáng lo hơn trục trích dẫn. Đó là
lý do `/book-audit` vẫn phải chạy cạnh `fidelity_audit.py`, không thay thế được nhau.

## Đổi mức giữa chừng

Được, và đôi khi là việc đúng. Nhưng:

1. Sửa `_scope_decision.md`, **viết vì sao đổi**, ký lại ngày.
2. Chạy lại `fidelity_audit.py --level <mức mới>`. Cổng so lời khai với cờ; lệch nhau thì nó dừng ở
   mã 2 chứ không chạy theo cờ.
3. Nếu nâng mức chỉ vì đang vượt trần — dừng lại một nhịp. Lần nào vượt cũng nới thì trần không còn
   là trần, và cái mất là chính thứ P0 sinh ra để bảo vệ.
