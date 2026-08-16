# Giao thức thí nghiệm hành vi

## Luật

1. **WIP = 1.** Chỉ một thí nghiệm `OPEN` tại một thời điểm. Phát hiện 5 điểm yếu vẫn chỉ kê 1. Ràng buộc cứng, không phải gợi ý.
2. **Dạng nếu–thì.** Câu phải bắt đầu bằng "Khi " và chứa " tôi ", mô tả hành vi quan sát được. Cấm viết kiểu "chú ý Description hơn".
3. **Cách đo.** Phiên MỞ thí nghiệm ghi `"exp_active": null, "exp_held": null` — thí nghiệm chỉ được tính từ phiên KẾ TIẾP trở đi. Từ phiên kế tiếp, mỗi phiên ghi `exp_active` = ID thí nghiệm và `exp_held: true/false`.

   Luật này áp cho **phiên tự kê thí nghiệm**, vì không thể "giữ" một cam kết chưa tồn tại
   lúc phiên đó diễn ra. Thí nghiệm mở **ngoài phiên** — CEO chốt ở bước weekly sau khi cờ
   `LỆCH Ô` bật — thì cam kết đã có trước, nên phiên được chấm kế tiếp **tính ngay**, không
   bỏ trống một nhịp. Ghi nhầm ở đây làm streak chậm mất một phiên mà không ai thấy.
4. **Nghiệm thu.** Giữ 3 phiên liên tiếp → `PASSED`, đóng, mở thí nghiệm mới.
5. **Đứt.** Streak về 0, số lần đứt +1. Đứt lần thứ 3 → `FAILED`.
6. **Sau `FAILED`.** Kê thí nghiệm NHỎ HƠN nhắm cùng ô. Cấm chép lại nguyên văn câu cũ.
7. **`SUPERSEDED` — đóng sớm.** Chỉ CEO quyết, thường khi weekly in cờ `LỆCH Ô`: thí nghiệm
   đang chạy nhắm một ô, ràng buộc tuần đã đổi sang ô khác. Ghi trạng thái `SUPERSEDED` kèm
   ngày đóng, **giữ nguyên `streak` và `đứt` tại thời điểm đóng** — đó là dữ liệu, không phải
   điểm số. `SUPERSEDED` chỉ hợp lệ khi `streak < 3` VÀ `đứt < 3`; đủ một trong hai thì nó đã
   là `PASSED`/`FAILED` rồi, dán `SUPERSEDED` lên là xoá mất một kết quả thật.
   Luật 6 **không** áp cho `SUPERSEDED` — thí nghiệm sau nhắm ô ràng buộc mới, không phải
   bản nhỏ hơn của ô cũ. AI **không** tự đặt `SUPERSEDED`: weekly chỉ in cờ và dừng ở đó.

   Trạng thái này tồn tại vì thiếu nó thì một thí nghiệm bị bỏ giữa chừng chỉ có hai đường
   ghi sổ, cả hai đều nói dối: `PASSED` khi chưa giữ đủ 3 phiên, hoặc `FAILED` khi chưa đứt
   3 lần. Sổ chỉ append — ghi sai một lần là sai vĩnh viễn.

## Bảng `experiments.md`

| ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng |
|---|---|---|---|---|---|---|---|
| `EXP-001` | `des.product` | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi. | 3 | 0 | PASSED | 2026-08-01 | 2026-08-05 |
| `EXP-002` | `dis.product` | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng. | 1 | 0 | OPEN | 2026-08-06 |  |

Cột **`ô mục tiêu`** là nơi duy nhất ghi ô mà thí nghiệm nhắm tới. Nó **khác** trường `weakest`
trong `sessions.jsonl`: `weakest` là ô thấp nhất tuyệt đối của phiên (kể cả ô `dil.*` đang bị cờ đỏ),
còn ô mục tiêu thí nghiệm phải LOẠI mọi ô `dil.*` chấm `0` — cờ đỏ xử ngay trong phiên, không đi
vào vòng thí nghiệm.

## Ví dụ tốt và xấu

| Xấu | Tốt |
|---|---|
| Chú ý Description hơn | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi |
| Kiểm chứng kỹ hơn | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng |
| Delegation tốt hơn | Khi mở phiên, tôi nói rõ task này là Core hay Offload trước câu hỏi đầu tiên |

---

# Phần chỉ weekly dùng — vòng cải tiến DMIR

> `fluency-4d-review` KHÔNG đọc phần này. Review dừng ở luật WIP=1 và streak phía trên.
>
> Ba bảng dưới đây là **hằng số**. `fluency-4d-weekly` **chọn dòng** từ chúng, không sinh
> dòng mới lúc chạy — cùng kỷ luật với `improvement-playbook.md`. Lý do y hệt: một coach
> được phép tự dựng bản đồ nhân quả ngay lúc chạy sẽ dựng đúng cái bản đồ biện minh cho ô
> nó vừa chọn. Bảng viết trước, người dùng duyệt trước — đó là chỗ chặn.
>
> Chỉ CEO sửa được ba bảng này. AI đề nghị sửa thì in đề nghị, không tự sửa.

## Bảng 1 — DMIR đọc ô nào, ghi ra cái gì

Bảng này tồn tại để DMIR không bị dán vào như nhãn. Mỗi giai đoạn bị buộc phải chỉ ra
nguồn đọc và sản phẩm ghi ra; giai đoạn nào không chỉ được thì giai đoạn đó là giấy.

| Giai đoạn | Đọc gì | Chỉ được ghi ra gì | Cấm |
|---|---|---|---|
| **D — Chuẩn đoán** | Nhóm ứng viên (các ô đang tụt) + Bảng 2 | Đúng **một** ô ràng buộc, kèm ô thấp nhất tuyệt đối và một câu vì sao hai ô đó khác nhau | Chốt ràng buộc khi nhóm ứng viên rỗng |
| **M — Bản đồ** | Bảng 2 + Bảng 3 | Các cạnh có ô ràng buộc ở một đầu, **chép nguyên văn**; trung bình của mọi ô thượng nguồn; tầng đòn bẩy của ô ràng buộc | Vẽ cạnh không có trong Bảng 2; gọi bảng là "mô hình"; ước lượng tương quan giữa các ô từ sổ |
| **I — Can thiệp** | `improvement-playbook.md` + profile đang bật + `experiments.md` | Đúng **một** ứng viên thí nghiệm nhắm ô ràng buộc; cờ lệch ô nếu thí nghiệm đang chạy nhắm ô khác | Mở thí nghiệm mới khi còn dòng `OPEN`; viết hộ câu nếu–thì |
| **R — Nghiệm thu** | Báo cáo weekly tuần trước + `sessions.jsonl` + `experiments.md` | Phán quyết bằng số cho hai câu hỏi ở mục "Luật bước R"; danh sách cạnh nghi vấn | Văn phản tỉnh; thách thức paradigm; hồi cứu bịa ra khi không có tuần trước |

**Đã cố ý cắt, đừng khôi phục.** Bản gốc DMIR còn có: mô hình System Dynamics (stock–flow,
mô phỏng, sensitivity analysis) ở M; menu 8 system archetype và vẽ CLD ở D; bước 2–4 của
Five Focusing Steps (exploit / subordinate / elevate) ở I; thách thức paradigm L1–L2 ở R;
và 8 tầng đòn bẩy còn lại của Meadows. Tất cả đã bị cắt vì sổ điểm này là dữ liệu thưa —
điểm nguyên 0–3, vài phiên một tuần, một người. Không có tồn, không có dòng, không có độ
trễ nào ước lượng được, không có tác nhân thứ hai. Bê chúng vào thì mỗi tuần sinh ra một
câu chuyện mới rồi gọi là phân tích. Muốn khôi phục phần nào thì phải chỉ ra trước dữ liệu
nào nuôi nó.

## Bảng 2 — Bản đồ ô kéo ô (18 cạnh)

Mỗi cạnh là **khẳng định cấu trúc rút từ câu hỏi chấm trong `rubric-core.md`**, KHÔNG phải
tương quan rút từ sổ. Đọc: "ô trái hỏng thì ô phải không thể tốt". Đồ thị không có chu trình.

| # | Ô thượng nguồn | Kéo ô | Vì sao |
|:-:|---|---|---|
| 1 | `del.problem` | `del.task` | Chưa hiểu bản chất việc thì không cắt được khối để chia người/AI |
| 2 | `del.problem` | `des.product` | Không có "xong nghĩa là gì" thì không có tiêu chí xong để mô tả |
| 3 | `del.problem` | `des.performance` | Chưa phân loại Core/Offload thì không biết cần AI phản biện hay thừa hành |
| 4 | `del.platform` | `del.task` | Không biết công cụ làm được gì thì chia theo "thế mạnh mỗi bên" là đoán |
| 5 | `del.platform` | `des.process` | Không biết đã có khung/skill sẵn nào thì đành để AI tự chế quy trình |
| 6 | `del.platform` | `dis.process` | Không biết công cụ **không** làm được gì thì không biết chỗ nào nó đang bịa |
| 7 | `del.platform` | `dil.creation` | Chọn sai công cụ/kênh thì dữ liệu đi vào chỗ lẽ ra không được đi vào |
| 8 | `del.task` | `des.product` | Giao trọn gói thì mô tả cũng trọn gói — không có đầu ra từng khối để tả |
| 9 | `del.task` | `dis.product` | Không giữ lại khối nào thì không còn thước độc lập để chấm đầu ra |
| 10 | `des.product` | `dis.product` | Không nêu tiêu chí đầu ra thì "đúng trọng tâm" là đúng trọng tâm nào? |
| 11 | `des.product` | `dil.deployment` | Không nêu người đọc thì không biết phải kiểm tới mức nào trước khi ký |
| 12 | `des.process` | `dis.process` | Không chỉ định quy trình thì không có chuẩn để đối chiếu khi soi đường đi |
| 13 | `des.performance` | `dis.performance` | Không nêu muốn AI hành xử ra sao thì không có kỳ vọng để đánh giá hành xử |
| 14 | `des.performance` | `dis.process` | Không giao vai phản biện thì AI không tự bày chỗ yếu — soi thành dò lại từ đầu |
| 15 | `dis.product` | `dil.deployment` | Chưa chấm chất lượng đầu ra thì đứng tên là đứng tên mù |
| 16 | `dis.product` | `dil.transparency` | Không biết phần nào AI làm và phần nào đã kiểm thì dòng ghi nhận ra chung chung |
| 17 | `dis.process` | `dil.deployment` | Không soi đường đi thì cổng kiểm chỉ canh hình thức |
| 18 | `dis.process` | `dil.transparency` | Không biết AI đi qua bước nào thì không chỉ được người đọc cần kiểm kỹ chỗ nào |

**Bốn ô cuối nhánh, cố ý không có cạnh ra:** `dis.performance`, `dil.creation`,
`dil.transparency`, `dil.deployment`. Ghi rõ ở đây để lần bảo trì sau không bịa cạnh cho đủ
đối xứng. `dis.performance` canh việc phiên có trôi thành đẻ tài liệu hay không — tức canh
tính hữu dụng của cả phiên, không canh điểm của ô nào khác.

## Bảng 3 — Tầng đòn bẩy Meadows theo ô

Bốn tầng, đúng bốn. Tám tầng còn lại của Meadows không có ô nào tương ứng ở quy mô một
người một sổ, nên không đưa vào.

| Ô | Tầng | Đổi cái gì |
|---|---|---|
| `del.problem`, `del.task` | **L3 Mục tiêu** | Phiên này rốt cuộc để làm gì, phần nào tôi không giao |
| `del.platform`, `des.product`, `des.process`, `des.performance` | **L5 Luật** | Luật thường trực về định tuyến việc và về cách giao |
| `dis.product`, `dis.process`, `dis.performance` | **L6 Dòng thông tin** | Chất lượng phản hồi tôi tự tạo ra cho mình |
| `dil.creation`, `dil.transparency`, `dil.deployment` | **L5 Luật** | Cổng thường trực trước khi thứ gì đó rời khỏi tay mình |
| *(không ô nào)* | **L12 Tham số** | "Làm kỹ hơn", "kiểm thêm một lần" — chỗ câu nếu–thì hay rơi vào |

Thứ tự tầng ở bảng này **không trùng** thứ tự thượng nguồn ở Bảng 2 (`dis.*` ở L6 thấp hơn
`dil.*` ở L5 nhưng lại nằm thượng nguồn của `dil.*`). Đó là lý do tầng đòn bẩy KHÔNG được
dùng để chọn ô ràng buộc — chọn ô là việc của Bảng 2. Tầng đòn bẩy có đúng một việc:

**Luật leo tầng.** Ô ràng buộc đã có ≥ 1 thí nghiệm `FAILED` nhắm đúng nó trong
`experiments.md` → in cảnh báo kèm tầng của ô, và nêu ràng buộc: câu nếu–thì lần này phải
đổi mục tiêu / luật / dòng thông tin của ô đó, **không được là tham số L12** ("làm kỹ hơn",
"kiểm thêm một lần"). Vòng trước đã thử ở tầng thấp và trượt rồi. AI vẫn KHÔNG viết hộ câu —
chỉ in ràng buộc về tầng.

## Luật bước R — nghiệm thu vòng trước

Bước R nghiệm thu **vòng weekly trước**, khác với việc đóng thí nghiệm. Đóng thí nghiệm là
việc của `fluency-4d-review` theo luật 4 và 5 phía trên; weekly chỉ đọc và báo, **không sửa
`experiments.md`**.

**R1 — Ô ràng buộc tuần trước có nhúc nhích không.** Lấy trung bình ô đó tuần này trừ tuần
trước: ≥ **+0.5** → `ĐỠ`; trong khoảng **±0.5** → `ĐỨNG YÊN`; ≤ **−0.5** → `TỆ ĐI`. In cả ba
con số, không in mỗi kết luận.

**R2 — Cạnh đặt cược có đúng không.** Đây là giả định bị chất vấn: tuần trước chọn ô đó làm
ràng buộc **vì tin rằng nó kéo các ô hạ nguồn**. Lấy các ô hạ nguồn trực tiếp của nó theo
Bảng 2. Ô thượng nguồn `ĐỠ` mà **không ô hạ nguồn nào đỡ ≥ +0.3** → đánh dấu cạnh đó
`NGHI VẤN` và ghi vào mục "Cạnh nghi vấn" của báo cáo tuần. Cùng một cạnh `NGHI VẤN`
**3 tuần liên tiếp** → in đề nghị CEO xoá cạnh khỏi Bảng 2. AI không tự xoá.

**R3 — Không có tuần trước.** Chưa có file weekly của tuần liền trước → in
`vòng trước: không có` rồi bỏ qua R1 và R2. Cấm dựng lại hồi cứu từ trí nhớ.

**R4 — Kết quả ghi vào đâu.** Toàn bộ đầu ra bước R nằm trong `weekly/<năm>-W<tuần>.md`, ở
hai mục `R — Nghiệm thu vòng trước` và `Cạnh nghi vấn`. `experiments.md` chỉ review ghi.
Bảng 2 và Bảng 3 chỉ CEO sửa.
