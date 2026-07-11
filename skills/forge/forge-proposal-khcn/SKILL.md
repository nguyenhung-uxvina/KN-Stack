---
name: forge-proposal-khcn
description: "Soạn Phiếu đề xuất nhiệm vụ Khoa học và Công nghệ (KHCN) đúng quy định cho hệ thống quốc phòng Việt Nam — hỗ trợ 4 cấp: Nhà nước (BQP), Bộ Quốc phòng, Tổng cục CNQP, và cơ sở (Quân chủng/Viện). Output là form hoàn chỉnh sẵn sàng nộp. Use when a military unit or Workshop X needs to submit an R&D project proposal for annual review. Triggers on: \"đề xuất KHCN\", \"phiếu đề xuất nhiệm vụ\", \"đề tài quốc phòng\", \"nộp hồ sơ BQP\", \"KHCN proposal\", \"defense R&D proposal\", \"science technology proposal Vietnam\", \"de xuat de tai nghien cuu\"."
---

# forge-proposal-khcn

Soạn **Phiếu đề xuất nhiệm vụ Khoa học và Công nghệ** đúng quy định cho hệ thống quốc phòng Việt Nam. Hỗ trợ 4 cấp: Nhà nước (qua BQP), Bộ Quốc phòng, Tổng cục CNQP, và cơ sở (Quân chủng/Viện/Bệnh viện). Output: form hoàn chỉnh sẵn sàng nộp.

---

## Khi nào dùng

- Đơn vị quân sự / WX cần đề xuất đề tài/dự án R&D lên cấp trên
- Hỗ trợ khách hàng Hải quân / Lục quân / Viện KT điền phiếu đề xuất
- Chuẩn bị hồ sơ cho chu kỳ xét duyệt hàng năm
- Kiểm tra phiếu đề xuất hiện có so với đúng mẫu quy định

---

## Chọn Cấp (Mode Selection)

Hỏi CEO/người dùng chọn một trong 4 chế độ:

```
1 = Cấp Nhà nước     → BQP trình lên Bộ KH&CN / Hội đồng KHCN Quốc gia
2 = Cấp Bộ QP        → Nộp Cục Khoa học Quân sự (Bộ QP)         [TT 180/2019]
3 = Cấp Tổng cục CNQP → Nộp Phòng/Vụ KHCN Tổng cục CNQP
4 = Cấp cơ sở        → Nộp Hội đồng KH Viện/Quân chủng/Quân đoàn
```

Nếu không rõ cấp: hỏi "Đề tài nộp lên đâu? (Bộ QP / CNQP / Viện / Quân chủng)"

---

## Loại Nhiệm Vụ

Trong mỗi cấp, xác định loại:

| Ký hiệu | Loại | Khi dùng |
|---------|------|----------|
| **ĐT** | Đề tài KH&CN | Nghiên cứu ứng dụng, làm chủ công nghệ |
| **DA** | Dự án sản xuất thử nghiệm | Có sản phẩm mẫu, thử nghiệm quy trình |
| **ĐA** | Đề án khoa học | Quy hoạch, chiến lược, hệ thống lớn |

---

## Workflow

### Bước 1 — Thu thập thông tin dự án

Hỏi người dùng (dạng interview, không hỏi tất cả cùng lúc):

```
1. Tên đề tài/dự án là gì? (ngắn gọn, súc tích)
2. Đơn vị đề xuất là ai? (Viện, Xưởng, Phòng KT...)
3. Vấn đề thực tế cần giải quyết là gì?
4. Mục tiêu cụ thể cần đạt: (chỉ tiêu đo được)
5. Sản phẩm cuối là gì? (mẫu thử, tài liệu KT, phần mềm, thiết bị...)
6. Thời gian dự kiến: (X tháng)
7. Kinh phí dự kiến: (triệu VNĐ)
8. Ai chủ nhiệm đề tài? (họ tên, học hàm học vị)
```

Sau khi có đủ thông tin → tiến hành điền form theo cấp được chọn.

---

## Form Cấp 2: Bộ Quốc phòng

**Căn cứ:** Thông tư 180/2019/TT-BQP (hiệu lực 20/01/2020)
**Nộp:** Cục Khoa học Quân sự — trước ngày 01/01 hàng năm
**Phân loại:** Đề xuất Ứng dụng (M-ĐX-UD) hoặc Đề xuất Nghiên cứu (M-ĐXNC)

> **ĐX-UD** = đơn vị sẽ trực tiếp ứng dụng kết quả  
> **ĐX-NC** = đơn vị nghiên cứu, đơn vị khác ứng dụng

### Nội dung tối thiểu bắt buộc (Điều 16 TT180):

```
TÊN NHIỆM VỤ: [ngắn gọn, bắt đầu "Nghiên cứu..." / "Thiết kế..." / "Phát triển..."]

MỤC TIÊU:
  - [Mục tiêu 1 — đo được, có chỉ số cụ thể]
  - [Mục tiêu 2]
  - [...]

YÊU CẦU ĐỐI VỚI KẾT QUẢ:
  Sản phẩm dạng I: [Bài báo / Bằng sáng chế / Không]
  Sản phẩm dạng II: [Quy trình / Tài liệu KT / Báo cáo / Thiết kế]
  Sản phẩm dạng III: [Mẫu thử / Thiết bị / Phần mềm + chỉ tiêu KT]

  Chỉ tiêu chiến-kỹ thuật cần đạt:
  | Chỉ tiêu | Giá trị yêu cầu | Ghi chú |
  |----------|----------------|---------|
  | [...]    | [...]          | [...]   |
```

**Checklist tự kiểm trước nộp:**
- [ ] Không trùng nhiệm vụ đang triển khai (tra cứu Cơ sở dữ liệu KHQS)
- [ ] Tính cấp thiết: giải quyết vấn đề quân sự cụ thể
- [ ] Tính mới: có điểm khác biệt so với giải pháp hiện tại
- [ ] Chỉ tiêu KT định lượng (không dùng "tốt hơn", "cải thiện")
- [ ] Đơn vị ứng dụng có cam kết (với ĐX-UD)

---

## Form Cấp 3: Tổng cục CNQP

**Căn cứ:** Quy định nội bộ CNQP (theo khung TT180/2019 + yêu cầu bổ sung công nghiệp QP)
**Nộp:** Phòng/Vụ KHCN Tổng cục CNQP
**Đặc thù:** Yêu cầu cao hơn về tính ứng dụng sản xuất, chuyển giao công nghệ

### Nội dung đề xuất cấp CNQP:

```
TÊN NHIỆM VỤ: [...]

MỤC TIÊU: [...]

YÊU CẦU ĐỐI VỚI KẾT QUẢ: [...]

BỔ SUNG BẮT BUỘC CHO CNQP:
  Liên kết với cơ sở CNQP: [Nhà máy / Tổng công ty nào sẽ tiếp nhận?]
  Khả năng nội địa hóa: [% linh kiện nội địa dự kiến]
  Năng lực sản xuất sau nghiên cứu: [Số lượng/năm nếu thành công]
  Tiêu chuẩn áp dụng: [MIL-STD / TCVN / tiêu chuẩn QP...]
```

---

## Form Cấp 4: Cơ sở (Viện / Quân chủng / Quân đoàn)

**Căn cứ:** Quy định của từng đơn vị (chuẩn thực tế từ Viện KTHQ 2025)
**Mẫu:** 13 mục — đây là chuẩn phổ biến nhất ở cấp Viện/Quân chủng

---

### TIÊU ĐỀ PHIẾU

```
[TÊN ĐƠN VỊ CHỦ QUẢN]          CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
[ĐƠN VỊ ĐỀ XUẤT]               Độc lập – Tự do – Hạnh phúc

                    [Địa danh], ngày ... tháng ... năm ...

              PHIẾU ĐỀ XUẤT
   NHIỆM VỤ KHOA HỌC VÀ CÔNG NGHỆ CẤP [VIỆN/QUÂN CHỦNG/...]
```

---

### MỤC 1 — Tên đề tài

Công thức: `[Động từ hành động], [đối tượng], [mục đích/ngữ cảnh]`

Ví dụ tốt:
- "Nghiên cứu, thiết kế, chế tạo UAV VTOL phục vụ trinh sát hải quân"
- "Phát triển phần mềm điều khiển hỏa lực tích hợp cho tàu tuần tra"

Tránh:
- Tên mơ hồ: "Nghiên cứu về UAV" (thiếu mục đích)
- Tên quá dài: quá 2 dòng

---

### MỤC 2 — Xuất xứ hình thành

```
- Căn cứ vào [kết quả nghiên cứu trước / chỉ thị / nhu cầu đơn vị] từ [năm] đến nay;
- Căn cứ vào nhu cầu [hoàn thiện / làm chủ / phát triển] [lĩnh vực] của [đơn vị];
- [Thêm căn cứ pháp lý nếu có: Quyết định, Thông tư liên quan]
```

---

### MỤC 3 — Lý do đề xuất

**3.1 Tình hình nghiên cứu và ứng dụng trên thế giới**

```
Trên thế giới, [tên lĩnh vực/công nghệ] đang [xu hướng chính]:
- [Quốc gia/tổ chức 1]: [giải pháp, hiệu quả đạt được]
- [Quốc gia/tổ chức 2]: [giải pháp]
- [...]

Nhận xét: Các hệ thống này có [ưu điểm] nhưng [hạn chế khi áp dụng cho VN].
→ Tạo khoảng trống công nghệ và nhu cầu cấp bách phát triển giải pháp nội địa.
```

**3.2 Thực trạng nghiên cứu trong nước**

```
Trong nước, [hiện trạng]: [mô tả tình trạng thiếu hụt/bất cập].

Các giải pháp hiện tại không đáp ứng vì:
- [Lý do 1]
- [Lý do 2]
- [...]

Nhu cầu thực tế tại [đơn vị ứng dụng]: [mô tả cụ thể yêu cầu chiến đấu/vận hành].
```

---

### MỤC 4 — Mục tiêu

```
- Mục tiêu tổng quát:
  + Làm chủ công nghệ [X], thiết kế, chế tạo và thử nghiệm [sản phẩm] có khả năng:
  + [Chức năng 1]
  + [Chức năng 2]

- Mục tiêu cụ thể:
  + [Chỉ tiêu 1: có số đo — ví dụ "Tầm bay ≥ 60 km"]
  + [Chỉ tiêu 2: có số đo]
  + [Sản phẩm cuối: "Nguyên mẫu hoàn chỉnh + thử nghiệm tại [địa điểm]"]
```

---

### MỤC 5 — Nội dung KHCN chủ yếu

Tổ chức theo 4–5 phần nhỏ:

```
5.1 Nghiên cứu cơ sở khoa học – công nghệ
    - [Phân tích lý thuyết, mô hình hóa, khảo sát tài liệu]

5.2 Thiết kế [hệ thống / phần cứng / phần mềm]
    - [Các hạng mục thiết kế chính]

5.3 Chế tạo mẫu / Phát triển phần mềm
    - [Nội dung chế tạo hoặc lập trình]

5.4 Tích hợp và thử nghiệm
    - [Phương pháp thử nghiệm, địa điểm, điều kiện]

5.5 Tổng hợp kết quả và hoàn thiện hồ sơ công nghệ
```

---

### MỤC 6 — Yêu cầu đối với kết quả

```
* Sản phẩm dạng I: [Bài báo khoa học / Không]

* Sản phẩm dạng II:
  - Báo cáo chuyên đề nghiên cứu
  - Hồ sơ thiết kế: Bộ chỉ tiêu tính năng chiến-kỹ thuật, Điều kiện kỹ thuật,
    Bản vẽ sản phẩm, Thuyết minh kỹ thuật và hướng dẫn sử dụng
  - Báo cáo tổng kết đề tài

* Sản phẩm dạng III: [Mẫu / Thiết bị / Phần mềm]
  - [Chỉ tiêu chiến-kỹ thuật 1: Giá trị]
  - [Chỉ tiêu 2: Giá trị]
  - [Điều kiện môi trường: nhiệt độ, độ ẩm, chống nước, chịu rung...]
  - [Kích thước, khối lượng]
  - [Nguồn điện / năng lượng]
  - [Thử nghiệm: địa điểm, đơn vị nhận xét nghiệm]
```

**Lưu ý sản phẩm dạng III:**
- PHẢI có chỉ tiêu định lượng (không chấp nhận "đạt yêu cầu")
- Với UAV/vũ khí: bắt buộc có chỉ tiêu môi trường biển (muối, ẩm, gió cấp)
- Với phần mềm: thời gian đáp ứng, độ chính xác, tỷ lệ lỗi cho phép

---

**Dạng IV — Đăng ký bảo hộ quyền sở hữu công nghiệp, quyền đối với giống cây trồng**

| TT | Tên sản phẩm | Yêu cầu khoa học cần đạt | Ghi chú |
|----|--------------|--------------------------|---------|
| 1 | [Sáng chế / Giải pháp hữu ích / Kiểu dáng công nghiệp / Nhãn hiệu] | [Tính mới, tính sáng tạo, khả năng áp dụng công nghiệp] | |
| 2 | | | |

> Với WX / CNQP: điền nếu đề tài tạo ra giải pháp kỹ thuật có thể nộp đơn sáng chế hoặc giải pháp hữu ích. Nếu không có → ghi "Không".

---

### MỤC 7 — Yêu cầu về thời gian

```
Dự kiến [X] tháng (từ tháng [MM/YYYY] – [MM/YYYY])
```

Thực tế theo cấp:
- Cấp cơ sở: 6–12 tháng
- Cấp CNQP: 12–24 tháng
- Cấp BQP: 24–36 tháng

---

### MỤC 8 — Năng lực tổ chức của cơ quan, đơn vị

```
[Tên đơn vị] có kinh nghiệm trong [lĩnh vực], gồm:
- Đã thực hiện đề tài/dự án tương tự: [liệt kê nếu có]
- Trang thiết bị phòng thí nghiệm: [liệt kê]
- Nhân lực: [Số KS/ThS/TS chuyên ngành]

Hoặc: "Không" (nếu đơn vị không có năng lực và cần phối hợp bên ngoài)
```

---

### MỤC 9 — Kinh phí dự kiến

```
[X.XXX.XXX đồng]
Bằng chữ: [...]

Phân kỳ (nếu nhiều năm):
  Năm 1: [...]
  Năm 2: [...]
```

**Tham chiếu ngưỡng thực tế:**
- Đề tài cơ sở đơn giản: 15–50 triệu VNĐ
- Đề tài cơ sở có chế tạo mẫu: 100–500 triệu VNĐ
- Cấp CNQP/BQP: 500 triệu – vài tỷ VNĐ

---

### MỤC 10 — Phương án huy động các nguồn lực

```
Kinh phí thực hiện đề tài từ các nguồn:
- Ngân sách nhà nước cấp [cấp]: [X triệu đồng] — để [nội dung]
- Nguồn tự huy động / tài trợ: [X triệu đồng] — để [nội dung]
- Nguồn phối hợp từ [đối tác]: [X triệu đồng]
```

---

### MỤC 11 — Dự kiến hiệu quả của nhiệm vụ KH&CN

```
- Hiệu quả quốc phòng – an ninh:
  + [Tác động cụ thể đến năng lực chiến đấu / vận hành]
  + [Giảm phụ thuộc nhập khẩu / nội địa hóa]

- Hiệu quả khoa học – công nghệ:
  + [Làm chủ công nghệ gì]
  + [Hình thành năng lực gì]
  + [Tạo nền tảng phát triển gì tiếp theo]

- Hiệu quả kinh tế (nếu có):
  + [So sánh chi phí với giải pháp nhập ngoại]
```

---

### MỤC 12 — Đề xuất cá nhân, đơn vị thực hiện

```
[Họ tên, học hàm học vị Chủ nhiệm] – [Đơn vị] chủ nhiệm đề tài
phối hợp với [Phòng/Ban/Đơn vị phối hợp]
```

---

### MỤC 13 — Phương án sử dụng kết quả

```
Sản phẩm đề tài được [trang bị / chuyển giao / triển khai] cho
[đơn vị sử dụng] phục vụ [mục đích cụ thể].

[Nếu có]: Hướng tiếp tục phát triển: [mô tả bước kế tiếp]
```

---

### CHỮ KÝ CUỐI PHIẾU

```
                                    ĐƠN VỊ CHỦ TRÌ
                           (Ký tên, đóng dấu / Ghi rõ họ tên chức vụ)
```

---

## Form Cấp 1: Nhà nước (qua BQP)

**Căn cứ:** Thông tư 06/2023/TT-BKHCN + quy trình nội bộ BQP
**Kênh:** Đơn vị QP → BQP (Cục KHQS) → Bộ KH&CN → Hội đồng xét duyệt QG
**Hồ sơ gồm:**
1. Công văn đề nghị (từ BQP)
2. Phiếu đề xuất nhiệm vụ (theo mẫu Bộ KH&CN — Mẫu B1/B2-ĐXĐH)
3. Bảng tổng hợp danh mục (kèm theo)
4. Tài liệu chứng minh tính cấp thiết quốc gia

**Khác biệt với cấp BQP:**
- Phải chứng minh tầm vóc quốc gia (không chỉ quốc phòng)
- Ngưỡng kinh phí lớn hơn nhiều
- Thời gian xét duyệt: 6–12 tháng
- Yêu cầu có đơn vị ứng dụng cam kết từ đầu

### Mục 22 — Sản phẩm KH&CN chính và yêu cầu chất lượng cần đạt

> Mục bắt buộc theo mẫu Bộ KH&CN. Phải điền đủ tất cả dạng có liên quan — là căn cứ nghiệm thu.

**Dạng I — Công bố khoa học** (Bài báo; Sách chuyên khảo và các sản phẩm khác)

| Số TT | Tên sản phẩm | Yêu cầu khoa học cần đạt | Dự kiến nơi công bố (Tạp chí, NXB) | Ghi chú |
|-------|--------------|--------------------------|-------------------------------------|---------|
| 1 | | | | |
| 2 | | | | |

---

**Dạng II — Tài liệu kỹ thuật và sản phẩm phi vật thể** (Nguyên lý ứng dụng; Phương pháp; Tiêu chuẩn; Quy phạm; Phần mềm máy tính; Bản vẽ thiết kế; Quy trình công nghệ; Sơ đồ, bản đồ; Số liệu, Cơ sở dữ liệu; Báo cáo phân tích/khoa học; Chuyên đề; Tài liệu dự báo (phương pháp, quy trình, mô hình, ...); Đề án, quy hoạch; Luận chứng kinh tế-kỹ thuật; Báo cáo nghiên cứu khả thi và các sản phẩm khác)

| TT | Tên sản phẩm | Yêu cầu khoa học cần đạt | Ghi chú |
|----|--------------|--------------------------|---------|
| 1 | | | |
| 2 | | | |

---

**Dạng III — Mẫu / Thiết bị / Sản phẩm vật thể** (Mẫu model/maket; Sản phẩm là hàng hoá có thể tiêu thụ trên thị trường; Vật liệu; Thiết bị, máy móc; Dây chuyền công nghệ; Giống cây trồng; Giống vật nuôi và các loại khác)

| Số TT | Tên sản phẩm cụ thể và chỉ tiêu chất lượng chủ yếu | Đơn vị đo | Mức chất lượng cần đạt | Mẫu tương tự trong nước (tiêu chuẩn mới nhất) | Mẫu tương tự thế giới | Dự kiến số lượng / quy mô sản phẩm tạo ra |
|-------|-----------------------------------------------------|-----------|------------------------|----------------------------------------------|----------------------|------------------------------------------|
| 1 | [Tên sản phẩm] | | | | | |
| | — [Chỉ tiêu 1] | | | | | |
| | — [Chỉ tiêu 2] | | | | | |
| 2 | | | | | | |

**Hướng dẫn điền Dạng III:**
- Cột **"Cần đạt"**: cam kết định lượng — là căn cứ nghiệm thu, không được để trống
- Cột **"Mẫu tương tự trong nước"**: SP VN tốt nhất hiện có cùng loại (nếu chưa có → "Chưa có")
- Cột **"Mẫu tương tự thế giới"**: SP nước ngoài làm chuẩn so sánh
- Cột **"Số lượng/quy mô"**: số lượng mẫu hoặc quy mô triển khai dự kiến

---

**Dạng IV — Đăng ký bảo hộ quyền sở hữu công nghiệp, quyền đối với giống cây trồng**

| TT | Tên sản phẩm | Yêu cầu khoa học cần đạt | Ghi chú |
|----|--------------|--------------------------|---------|
| 1 | [Sáng chế / Giải pháp hữu ích / Kiểu dáng công nghiệp / Nhãn hiệu] | [Tính mới, tính sáng tạo, khả năng áp dụng công nghiệp] | |
| 2 | | | |

> Với WX / CNQP: điền nếu đề tài tạo ra giải pháp kỹ thuật có thể nộp đơn sáng chế. Nếu không có → ghi "Không".

---

## Gotchas

| Lỗi phổ biến | Cách tránh |
|-------------|-----------|
| Mục tiêu không đo được | Luôn có ít nhất 1 chỉ số định lượng: tốc độ, tầm, trọng lượng, độ chính xác... |
| Sản phẩm dạng III không có chỉ tiêu KT | Điền đầy đủ bảng chỉ tiêu chiến-kỹ thuật |
| Nộp nhầm cấp | Kiểm tra: đề tài > 500 triệu → CNQP/BQP; < 100 triệu → cơ sở |
| Trùng với đề tài đang chạy | Tra cứu cơ sở dữ liệu KHQS trước khi nộp |
| Thời gian quá ngắn cho phạm vi | Đề tài có chế tạo mẫu: tối thiểu 12 tháng |
| Thiếu đơn vị ứng dụng cam kết | BQP bắt buộc có cam kết từ đơn vị nhận kết quả |
| Kinh phí không có phân kỳ | Đề tài > 12 tháng: phải phân kỳ theo năm |

---

## Sơ đồ trong hồ sơ (wx-diagram — AUTO)

Hồ sơ KHCN cần sơ đồ trình được. Khi soạn phiếu đề xuất/thuyết minh, xuất qua `/wx-diagram`:
- `/wx-diagram function-structure {{project}}` — sơ đồ chức năng tổng thể.
- `/wx-diagram swimlane {{project}}` — quy trình thực hiện nhiệm vụ (theo giai đoạn).
Format PDF khi mẫu biểu yêu cầu. CẤM aiicons.py (CDN) với nội dung MẬT/HẠN-CHẾ — xem rule bảo mật trong wx-diagram.

---

## Quy trình sau khi nộp phiếu đề xuất

```
CẤP CƠ SỞ:
  Nộp phòng KHCN đơn vị → Hội đồng KH cơ sở xét duyệt (30 ngày)
  → Phê duyệt → Ký hợp đồng thực hiện

CẤP CNQP:
  Nộp Vụ/Phòng KHCN Tổng cục → Tổng hợp danh mục → Hội đồng tư vấn (30 ngày)
  → Trình Tổng cục trưởng phê duyệt → Tuyển chọn/giao trực tiếp

CẤP BỘ QP (Thông tư 180/2019):
  Nộp trước 01/01 → Cục KHQS tham mưu → Lấy ý kiến đơn vị ứng dụng
  → Hội đồng tư vấn 30 ngày → Thủ trưởng BQP phê duyệt → Giao/tuyển chọn

CẤP NHÀ NƯỚC (qua BQP):
  BQP tổng hợp → Nộp Bộ KH&CN → Hội đồng xét duyệt quốc gia
  → Phê duyệt chương trình → Tuyển chọn đơn vị thực hiện
```

---

## Căn cứ pháp lý

| Cấp | Văn bản | Hiệu lực |
|-----|---------|----------|
| Nhà nước | Thông tư 06/2023/TT-BKHCN | 09/07/2023 |
| Nhà nước (cấp tỉnh/cơ sở dân sự) | Thông tư 09/2024/TT-BKHCN | 10/02/2025 |
| Bộ Quốc phòng | Thông tư 180/2019/TT-BQP | 20/01/2020 |
| Đăng ký thông tin KH&CN trong BQP | Thông tư 169/2017/TT-BQP | 17/07/2017 |
| CNQP | Quy định nội bộ Tổng cục CNQP | Theo ban hành |

---

## COD Classification

| Công việc | COD | Ghi chú |
|-----------|-----|---------|
| Chọn cấp nộp phiếu | **Core** | CEO/người dùng quyết định |
| Thu thập thông tin dự án | **Core** | Nội dung kỹ thuật từ người dùng |
| Soạn thảo nội dung | Offload | AI điền dựa trên thông tin đã có |
| Kiểm tra checklist | Offload | AI tự kiểm |
| Xác nhận chỉ tiêu KT | **Core** | Phải do kỹ sư chuyên môn xác nhận |
| Ký phiếu và nộp | **Core** | Người có thẩm quyền ký |

---

## Rules

- **KHÔNG tự điền chỉ tiêu chiến-kỹ thuật** nếu chưa được người dùng cung cấp — hỏi rõ
- **LUÔN hỏi cấp nộp trước** khi bắt đầu soạn
- **KHÔNG dùng ngôn ngữ mơ hồ** trong mục tiêu và yêu cầu kết quả: không "cải thiện", "tốt hơn", "phù hợp"
- **Dạng III PHẢI có bảng chỉ tiêu** — đây là căn cứ nghiệm thu
- Với WX context: nhớ Workshop X là công ty CNQP tư nhân → nêu rõ vai trò (đơn vị đề xuất hay đơn vị thực hiện)
