---
name: ip-criteria
description: "Block B0 của ip-invent — CHẶN. Dựng thước đo 'cái gì được tính' TRƯỚC khi rà ứng viên sáng chế. Kiểm điều kiện đăng ký (ai được nộp hồ sơ chức danh), lập bảng đối chiếu QĐ 431/QĐ-BQP (CSDL chuyên gia KH&CN BQP — 1 trong 6 đường, chỉ cần 01 văn bằng, 05 năm) ↔ QĐ 12/2025/QĐ-TTg (chức danh Chuyên gia CNQP-AN — 1 trong 2 nhóm, 02 văn bằng đã cấp VÀ đã được áp dụng nếu trong LLVT, 07 năm), chấm tất cả các đường theo chi phí × thời gian × độ chắc rồi khuyến nghị đường ngắn nhất — kể cả khi đường đó KHÔNG phải patent (bài ISI, sách chuyên khảo, giải thưởng VIFOTEC/Hội thi sáng tạo). Triggers on: 'ip-criteria', 'tiêu chí chức danh', 'thước đo chức danh', 'chuyên gia CNQP tiêu chí', 'CSDL chuyên gia BQP', 'QĐ 431', 'QĐ 12/2025', 'đường nào nhanh nhất đạt chức danh', 'cái gì được tính cho chức danh'."
---

# ip-criteria — B0: thước đo "cái gì được tính"

## ⛔ BƯỚC 0′ — đọc workspace TRƯỚC MỌI VIỆC KHÁC

Đọc `../ip-shared/references/active-workspace.md` → lấy tên file profile → đọc profile đó.
**Đọc không được thì DỪNG**, báo *"không đọc được tầng trỏ workspace"*, **không đoán, không chạy
tiếp bằng giá trị mặc định**. Một báo cáo trông đầy đủ mà chạy không có workspace là lỗi tệ hơn
không chạy gì.

Nếu profile khai `surface: cloud` → chạy cổng phân loại trong
`../ip-shared/references/co-mat-gate.md` **trước khi đụng nội dung ứng viên bất kỳ**.

In ở đầu mọi báo cáo:

```
Bề mặt: <surface> · Cổng phân loại: <trạng thái> · Căn cứ: <…>
```

Trường workspace nào bằng `none` → chạy **chế độ giảm** và **in dòng khai báo** (ví dụ
`1b chạy KHÔNG có TRIZ`). Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ.

> **Đây là block CHẶN.** Không có nó, B2 chấm trục "giá trị chức danh" bằng cảm giác.
> **Lý do tồn tại (ca thật):** tiền đề *"cần ≥2 bằng sáng chế, đó là đường găng"* đã dẫn sai cả một
> cụm quyết định của Workshop X suốt 53 ngày — chọn cặp ứng viên thuần theo novelty, bỏ qua việc
> QĐ 431 chỉ cần **01** văn bằng và QĐ 12/2025 có **đường nhiệm vụ KH&CN** thay thế.
> **Rà soát khả thi mà không biết cái gì được tính thì rà vô nghĩa.**

## When to use

- Trước khi bắt đầu bất kỳ việc IP nhắm mục tiêu chức danh
- Khi luật/quyết định tiêu chí đổi, hoặc nghi tiêu chí đang dùng đã lạc hậu
- Khi xét chức danh cho **người khác** trong xưởng (thước đo tái dùng được)
- Khi cần trả lời "đổ tiền vào patent có phải đường nhanh nhất không?"

## Bước 0 — Điều kiện đăng ký (làm TRƯỚC tiêu chí)

Trả lời trước khi bàn tiêu chí, vì nếu không thuộc diện thì tiêu chí vô nghĩa:

| Câu | Nguồn kiểm |
|---|---|
| Cá nhân/tổ chức có thuộc **diện áp dụng** không? | QĐ 12/2025 **Điều 1.2**: *"tổ chức, cá nhân thuộc các cơ sở công nghiệp quốc phòng do Bộ Quốc phòng quản lý, cơ sở công nghiệp an ninh do Bộ Công an quản lý; **cá nhân ngoài lực lượng vũ trang tham gia phục vụ** công nghiệp quốc phòng, an ninh"* · QĐ 431 **Điều 2**: cơ quan, đơn vị, **doanh nghiệp quân đội** + cá nhân liên quan đến quản lý/khai thác/**đăng ký tham gia** |
| Thuộc nhánh **TRONG** hay **NGOÀI** LLVT? | Quyết định thành lập/công nhận **cơ sở CNQP**; quyết định bổ nhiệm **ngạch** (kỹ sư cao cấp = hạng I chức danh sĩ quan CM-KT-NV, TT 222/2017/TT-BQP sđ TT 58/2022/TT-BQP) |
| Cần **đơn vị bảo trợ** không? | Nếu không thuộc diện trực tiếp |

> ⚠️ **Nhánh TRONG vs NGOÀI LLVT đổi hẳn yêu cầu** — không phải chi tiết hành chính:
> · **trong LLVT:** văn bằng phải *"được cấp văn bằng bảo hộ **VÀ ĐÃ ĐƯỢC ÁP DỤNG**"* trong CNQP-AN
> · **ngoài LLVT:** văn bằng *"được cấp văn bằng bảo hộ **CÓ KHẢ NĂNG ỨNG DỤNG**"* cho CNQP-AN
> Nhánh ngoài **dễ hơn**. Đoán sai nhánh = sai cả chiến lược ứng viên. **Đòi chứng cứ, đừng suy diễn.**

## Bảng đối chiếu hai văn bản (khung bắt buộc xuất)

| | **QĐ 431/QĐ-BQP** (12/02/2020) | **QĐ 12/2025/QĐ-TTg** (26/4/2025, hiệu lực 01/7/2025) |
|---|---|---|
| Đích | Vào **CSDL chuyên gia KH&CN của BQP** | **Chức danh** Chuyên gia CNQP-AN — BQP/BCA công nhận **CÓ THỜI HẠN** |
| Trình độ | TS/TSKH **HOẶC** ngạch cao cấp (GS, PGS, GVCC, NCVCC, **Kỹ sư cao cấp**, BSCC, DSCC); HOẶC ĐH + đạt Khoản 2 hoặc 6 Điều 5 | **Thạc sĩ trở lên** chuyên ngành KHKT&CN + **thành thạo ≥1 ngoại ngữ thông dụng** |
| Kinh nghiệm | ≥ **05** năm nghiên cứu liên tục | ≥ **07** năm liên tục (bộ động từ theo Luật 38/2024) |
| Kết quả KHCN | **1 trong 6** (Điều 5) — nhánh văn bằng chỉ cần **01** | **1 trong 2** (Điều 3.2) — nhánh văn bằng cần **02** |
| Năng lực khác | — | Điều 3.1.c — xây dựng tài liệu thiết kế/công nghệ, quy định thử nghiệm–nghiệm thu, tiêu chuẩn sản phẩm **và trực tiếp triển khai** |
| Phẩm chất | Điều 6.1 — **05 năm** không bị kỷ luật từ khiển trách; Điều 6.2 — không vi phạm hành vi bị cấm | Điều 3.1.d — không vi phạm hành vi bị cấm theo **Luật CNQP-AN-ĐVCN 38/2024**; **tiêu chuẩn chính trị** theo quy định BQP/BCA |

> 🔴 **Viện dẫn lỗi phải sửa khi lập hồ sơ:** QĐ 431 Điều 6.2 dẫn **Điều 8 Luật KH&CN 29/2013** — luật
> đó **hết hiệu lực 01/10/2025**, thay bởi **Luật Khoa học, Công nghệ và Đổi mới sáng tạo 93/2025/QH15**,
> nơi hành vi bị cấm nằm ở **Điều 14** (05 hành vi, không phải 04). Quy chiếu sang luật mới.

## Chấm các đường — bảng bắt buộc xuất

### QĐ 431 Điều 5 — 6 đường, đạt 01 là đủ (trong 05 năm liên tục tính đến ngày nộp)

| # | Đường | Yêu cầu | Chi phí × thời gian | Trạng thái |
|---|---|---|---|---|
| 5.1 | Nhiệm vụ KH&CN | chủ trì ≥01 đề tài cấp QG/Bộ (hoặc tương đương) **đã nghiệm thu** | | |
| 5.2 | Bài báo | tác giả chính ≥01 bài **ISI/Scopus**; HOẶC ≥05 bài trong nước có điểm **HĐGS Nhà nước** | | |
| 5.3 | Đào tạo | hướng dẫn chính 01 NCS TS; HOẶC 01 BSCK II; HOẶC 05 thạc sĩ | | |
| 5.4 | Sách | **chủ biên ≥01 sách chuyên khảo** | | |
| 5.5 | Chương trình | thành viên **Ban chủ nhiệm** chương trình KH&CN cấp QG/BQP | | |
| 5.6 | SHTT & giải thưởng | tác giả chính ≥**01** văn bằng bảo hộ; **HOẶC** ≥01 giải thưởng (HCM, Nhà nước, Tạ Quang Bửu, Trần Đại Nghĩa, **Giải nhất VIFOTEC**, **Giải nhất Hội thi Sáng tạo KT toàn quốc**) | | |

### QĐ 12/2025 Điều 3.2 — 2 nhóm, đạt 01 là đủ (trong 07 năm liên tục)

**Nhóm a — nhiệm vụ KH&CN. Trong LLVT có BA bậc, đừng chỉ nhìn bậc cao nhất:**

| Bậc | Yêu cầu (trong LLVT) |
|---|---|
| a1 | chủ trì **01 nhiệm vụ cấp bộ** |
| **a2** | chủ trì **01 nhiệm vụ cấp đầu mối trực thuộc bộ** về VKTBKT **có ý nghĩa chiến lược** / phương tiện KT nghiệp vụ **đặc biệt** ← **bậc thấp hơn a1, vẫn chỉ 01** |
| a3 | chủ trì **03 nhiệm vụ cấp đầu mối trực thuộc bộ**, **kết quả tạo ra sản phẩm được đưa vào trang bị** |

*(Ngoài LLVT: 01 nhiệm vụ cấp bộ HOẶC 03 nhiệm vụ cấp đầu mối trực thuộc bộ, nghiên cứu công nghệ chiến lược/nền/lõi/mới/lưỡng dụng **có khả năng ứng dụng** cho CNQP-AN.)*

**Nhóm b — văn bằng:** tác giả ≥**02** bằng sáng chế/GPHI, trong LLVT phải **được cấp VÀ đã được áp dụng**.

### Quy tắc chấm

Mỗi đường cho **3 số** + 1 kết luận:
- **Chi phí** (tiền + giờ CEO là Core, không uỷ thác được)
- **Thời gian tới đích** (tính từ hôm nay, tính cả thời gian chờ cấp/nghiệm thu/xét giải)
- **Độ chắc** (tự chủ được hay phụ thuộc bên ngoài duyệt/giao/xét — đường phụ thuộc bổ nhiệm hoặc
  cơ cấu giải thưởng hẹp thì hạ độ chắc, dù chi phí thấp)

**Bắt buộc kiểm mốc thời gian:** thành tích ngoài cửa sổ 05 năm (431) / 07 năm (12/2025) **không tính**.
Kiểm theo **ngày**, không theo cảm giác "gần đây".

## Nghĩa vụ nói thẳng

> Nếu chấm ra **đường ngắn nhất KHÔNG phải patent** → **nói thẳng ngay trong báo cáo B0**, đặt ở đầu,
> không giấu dưới bảng. Rồi nêu rõ: pipeline `ip-invent` **vẫn có giá trị** nhưng đổi vai — từ
> *"đường găng chức danh"* thành *"bảo hộ sản phẩm"*. Để CEO quyết dồn lực.
>
> Ba lý do patent vẫn đáng làm dù không phải đường nhanh nhất: (i) phục vụ **cả hai** đích; (ii) bảo hộ
> sản phẩm có giá trị độc lập với chức danh; (iii) nhánh trong LLVT đòi "đã được áp dụng" nên thời gian
> thẩm định (18–30 tháng) là đúng khoảng để chế tạo–triển khai–lập chứng cứ → **nộp muộn thì lùi cả mốc**.

## Output — ghi vào ledger

```markdown
## B0 — ip-criteria  (Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản>)

### Điều kiện đăng ký
Diện áp dụng: ĐỦ / CẦN BẢO TRỢ / KHÔNG THUỘC — căn cứ: <chứng cứ>
Nhánh: TRONG LLVT / NGOÀI LLVT — căn cứ: <chứng cứ, không suy diễn>

### Trạng thái tiêu chí
| Văn bản | Trình độ | Kinh nghiệm | Năng lực | Kết quả KHCN | Phẩm chất |
|---|---|---|---|---|---|

### Chấm đường (chi phí × thời gian × độ chắc)
<bảng đầy đủ, mọi đường, kể cả đường không phải patent>

### ⭐ KHUYẾN NGHỊ
Đường ngắn nhất: <tên>  — vì <lý do có số>
Đường patent xếp thứ: <n>  — chênh <bao lâu>
Vai của ip-invent theo kết quả này: đường găng chức danh / bảo hộ sản phẩm

### Thước đo cho B2 (trục "giá trị chức danh")
- Số văn bằng cần: <01 cho 431 / 02 cho 12-2025>
- Điều kiện kèm: <có khả năng ứng dụng | ĐÃ ĐƯỢC ÁP DỤNG>
- Vai tác giả cần: <tác giả | tác giả chính>
- Cửa sổ thời gian: <05 năm | 07 năm> tính đến <ngày dự kiến nộp hồ sơ>

### Khoản chưa xác minh (không được im lặng bỏ qua)
- [ ] <liệt kê>

⏸️ CEO: xác nhận bảng tiêu chí + chọn đường.
```

## Gotchas

- **Hai văn bản, hai đích — đừng gộp.** 431 là vào CSDL chuyên gia; 12/2025 là chức danh được công
  nhận có thời hạn. Tiêu chí, số văn bằng, số năm đều khác.
- **"Sáng kiến không đếm" chỉ đúng một nửa.** Sáng kiến không phải văn bằng bảo hộ → không đếm ở
  nhánh một Điều 5.6. **Nhưng** nó là **nguyên liệu đi thi**, và **Giải nhất VIFOTEC / Hội thi Sáng tạo
  KT toàn quốc ĐẾM** ở nhánh hai. Đừng viết "sáng kiến vô dụng cho chức danh".
- **Cơ cấu giải thưởng rất hẹp** (Hội thi lần 17: ~6 Giải nhất toàn quốc; chu kỳ **2 năm**; lần 18 hạn
  31/8/2025 đã đóng) → độ chắc thấp, nộp song song chứ không làm đường găng.
- **Ngồi hội đồng nghiệm thu ≠ chủ trì nhiệm vụ.** Hai vai khác nhau; chỉ "chủ trì" mới đếm.
- **QĐ 431 không có bản công khai** (văn bản nội bộ BQP) → đọc từ bản CEO giữ, **local**, không upload.
- **Kỹ sư cao cấp đã thỏa trình độ 431** mà không cần tiến sĩ — đừng mặc định phải có học vị TS.

## COD

| Việc | COD |
|------|-----|
| Tra nguyên văn, dựng bảng đối chiếu, chấm 3 số | Offload |
| **Xác nhận diện áp dụng + nhánh LLVT** | **Core** (đòi chứng cứ) |
| **Chọn đường dồn lực** | **Core** |
| Kết luận "đã đủ tiêu chí" | **Ngoài AI** — cơ quan xét quyết định |

## Rules

- **Không suy diễn nhánh LLVT** — đòi chứng cứ văn bản.
- **Chấm tất cả các đường**, không chỉ đường văn bằng. Bỏ sót đường rẻ hơn = lỗi của block này.
- **In ngày kiểm chuỗi sửa đổi**; tiêu chí lấy từ nguyên văn, không từ trang tổng hợp.
- **Liệt kê minh bạch khoản chưa xác minh** — im lặng bỏ qua đọc thành "đã đủ".
- Không kết luận thay cơ quan xét chức danh.
