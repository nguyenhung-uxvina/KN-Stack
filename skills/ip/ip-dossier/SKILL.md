---
name: ip-dossier
description: "Block B4 của ip-invent — lập hồ sơ. Xuất bộ đơn nộp Cục SHTT (tờ khai theo Phụ lục I HIỆN HÀNH, bản mô tả 9 mục, yêu cầu bảo hộ, hình vẽ, bản tóm tắt ≤150 từ), trang khả năng/thực tế ứng dụng CNQP-AN, hồ sơ chứng cứ ĐÃ ĐƯỢC ÁP DỤNG khi đích là QĐ 12/2025 nhánh trong LLVT, bản ghi xuất xứ đóng góp người/AI theo Điều 10a, và gói câu hỏi giao đại diện sở hữu công nghiệp. Có cổng kiểm soát an ninh Điều 14 (sáng chế thuộc danh mục bí mật nhà nước QP-AN chỉ được nộp ở nước ngoài nếu BQP/BCA cho phép) và bước bắt buộc xác minh chuỗi sửa đổi tới ngày hôm nay trước khi xuất quy cách. Triggers on: 'ip-dossier', 'lập hồ sơ sáng chế', 'bộ đơn sáng chế', 'tờ khai đăng ký sáng chế', 'bản mô tả sáng chế', 'bản tóm tắt sáng chế', 'nộp đơn Cục SHTT', 'giao đại diện SHTT', 'chứng cứ đã được áp dụng', 'nộp đơn ra nước ngoài'."
---

# ip-dossier — B4: lập hồ sơ

> Đọc khung claim đã chọn (B3) + routing (B2) + thước đo (B0) từ ledger.
> **Đầu ra là BẢN NHÁP KỸ THUẬT để giao đại diện sở hữu công nghiệp — KHÔNG phải bản nộp cuối.**

## ⛔ BƯỚC 0 BẮT BUỘC — xác minh chuỗi sửa đổi (không được bỏ)

Trước khi xuất **bất kỳ** quy cách, biểu mẫu, thời hạn hay mức phí:

```
1. Tra chuỗi sửa đổi Luật SHTT tới hôm nay
   Đã biết tới 2026-08-06: Luật 50/2005 sđ bởi 36/2009, 42/2019, 07/2022,
   93/2025/QH15, 131/2025/QH15
2. Tra chuỗi sửa đổi nghị định
   Đã biết: NĐ 65/2023 → NĐ 15/2026 (14/01) → NĐ 33/2026 (21/01) → NĐ 100/2026 (31/3, hiệu lực 01/4/2026)
3. Kiểm có nghị định/thông tư mới hơn chưa
4. IN dòng: "Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>"
```

> 🔴 **Vì sao bước này là bắt buộc, không phải cẩn thận thừa.** NĐ 100/2026 đã **bãi bỏ Điều 16–28,
> 30–32, 43–47, 108** của NĐ 65/2023 — đúng cụm quy định **hồ sơ đơn, bản mô tả, quy cách yêu cầu bảo
> hộ, thẩm định hình thức, công bố đơn, thẩm định nội dung** — và **thay toàn bộ Phụ lục I và II**
> (bãi bỏ Phụ lục III–VII). Nhiều trang hướng dẫn, **kể cả ipvietnam.gov.vn**, còn dẫn neo cũ.
> Trong một phiên dựng skill này, dữ kiện "tờ khai mẫu nào" đã bị lật **ba lần**:
> TT 23/2023 Phụ lục A mẫu 01-SC → Phụ lục I NĐ 65/2023 mẫu số 01 → **Phụ lục I NĐ 100/2026**.
> **Không có dòng ngày kiểm ⇒ đầu ra không dùng được.**

## Bộ hồ sơ đơn — thành phần

> ⚠️ Cấu trúc dưới đây theo hướng dẫn Cục SHTT (dẫn neo **đã bị thay**). **Phải đối chiếu Phụ lục I
> hiện hành** ở Bước 0 rồi mới dùng. Nếu chưa có Phụ lục I hiện hành → xuất bản nháp và **ghi rõ
> "quy cách chờ đối chiếu Phụ lục I hiện hành — đại diện SHTT chốt"**, đừng giả vờ đủ.

| # | Tài liệu | Yêu cầu |
|---|---|---|
| 1 | **Tờ khai** | theo mẫu tờ khai đăng ký sáng chế tại **Phụ lục I hiện hành** |
| 2 | **Bản mô tả** | gồm **Phần mô tả** + **Yêu cầu bảo hộ** + **Hình vẽ (nếu có)** |
| 3 | **Yêu cầu bảo hộ** | tách riêng sau phần mô tả; ngắn gọn, rõ ràng, **phù hợp với phần mô tả và hình vẽ**; **làm rõ những dấu hiệu mới** |
| 4 | **Hình vẽ, sơ đồ** | tách thành trang riêng |
| 5 | **Bản tóm tắt** | **≤ 150 từ**, trang riêng; hình vẽ/công thức đặc trưng chỉ trong nửa trang A4; **không bắt buộc nộp lúc nộp đơn**, bổ sung sau được |
| 6 | **Chứng từ nộp phí, lệ phí** | |
| + | Giấy uỷ quyền | nếu nộp qua tổ chức đại diện SHCN |
| + | Tài liệu chứng minh quyền đăng ký | nếu thụ hưởng từ người khác |
| + | Tài liệu chứng minh quyền ưu tiên | nếu có yêu cầu hưởng quyền ưu tiên |
| + | **Yêu cầu công bố sớm** | ⚠️ nếu muốn thẩm định nhanh (Điều 14a.c) — **phải nộp TẠI THỜI ĐIỂM nộp đơn** |

### Phần mô tả — 9 mục theo thứ tự

1. Tên sáng chế/GPHI
2. Lĩnh vực sử dụng
3. **Tình trạng kỹ thuật** của lĩnh vực sử dụng ← đưa prior art từ B2/B3 vào đây
4. Mục đích
5. **Bản chất kỹ thuật** ← đặc trưng phân biệt từ khung claim B3
6. Mô tả vắn tắt các hình vẽ kèm theo
7. **Mô tả chi tiết các phương án thực hiện**
8. **Ví dụ thực hiện**
9. Những lợi ích (hiệu quả) có thể đạt được

### Yêu cầu hình thức (đối chiếu lại ở Bước 0)
Tiếng Việt · trình bày dọc · **A4** · lề **20 mm** bốn phía · **Times New Roman ≥ cỡ 13** · số trang
bằng chữ số Ả-rập · ≥02 trang thì **đóng dấu giáp lai** · mực khó phai, **không tẩy xoá** (sửa lỗi
chính tả phải có chữ ký xác nhận tại chỗ sửa) · thuật ngữ thống nhất, phổ thông · ký hiệu/đơn vị đo
theo **tiêu chuẩn Việt Nam**.

> **Mỗi đơn chỉ được yêu cầu MỘT văn bằng bảo hộ**, và loại văn bằng phải phù hợp đối tượng nêu trong
> đơn → **nộp kép = hai bộ đơn riêng**; tách để về trần Điều 14a.d = **các đơn riêng ngay từ đầu**.

## ⛔ CỔNG ĐIỀU 14 — kiểm soát an ninh khi nộp ra nước ngoài

Chạy cổng này **bất cứ khi nào** có ý định nộp PCT / nước ngoài:

```
Giải pháp có thuộc DANH MỤC BÍ MẬT NHÀ NƯỚC trong lĩnh vực kỹ thuật
có tác động đến quốc phòng, an ninh?
  ├─ CÓ / CHƯA RÕ  →  ⛔ DỪNG. Chỉ được nộp ở nước ngoài NẾU ĐÃ ĐƯỢC
  │                    BỘ QUỐC PHÒNG HOẶC BỘ CÔNG AN CHO PHÉP.
  │                    Hồ sơ đề nghị (nộp trực tiếp/bưu chính tới cơ quan
  │                    có thẩm quyền BQP/BCA):
  │                      · Tờ khai đề nghị cho phép đăng ký sáng chế ra nước
  │                        ngoài — Mẫu số 25 Phụ lục I
  │                      · Bản mô tả sáng chế dự định đăng ký ở nước ngoài
  │                      · Văn bản xác định sáng chế thuộc bí mật nhà nước
  │                      · Uỷ quyền (nếu qua đại diện)
  │                    Đơn hợp lệ → được cấp Giấy tiếp nhận đơn
  └─ KHÔNG (có căn cứ)  →  nộp nước ngoài theo thủ tục thường
```

> 🔴 Điều kiện áp dụng: sáng chế **được tạo ra tại Việt Nam** và thuộc quyền đăng ký của **công dân
> Việt Nam thường trú tại Việt Nam** hoặc **tổ chức được thành lập theo pháp luật Việt Nam** — đúng
> hồ sơ của Workshop X.
> **Nộp ra nước ngoài mà chưa xin phép là vi phạm.** Kế hoạch kiểu *"đã lộ trong nước thì chỉ còn PCT"*
> **không hợp lệ** cho sản phẩm quốc phòng nếu chưa qua cổng này.
> **Ai xác định "thuộc danh mục bí mật nhà nước": cơ quan có thẩm quyền — KHÔNG phải skill này, KHÔNG
> phải CEO tự tuyên.** Chưa có văn bản xác định ⇒ coi như CHƯA RÕ ⇒ dừng.

## Hồ sơ chứng cứ ĐÃ ĐƯỢC ÁP DỤNG (khi đích là QĐ 12/2025, nhánh trong LLVT)

Chỉ lập khi thước đo B0 nói điều kiện kèm là **"đã được áp dụng"**. Đây là **tài liệu riêng**, không
nằm trong bộ đơn Cục SHTT — nó phục vụ hồ sơ chức danh.

| Loại chứng cứ | Gợi ý |
|---|---|
| Chế tạo | biên bản/hồ sơ chế tạo, ảnh có mốc thời gian, hồ sơ QC |
| Thử nghiệm | biên bản thử nghiệm, kết quả đo, báo cáo nghiệm thu kỹ thuật |
| Triển khai/sử dụng | biên bản bàn giao, xác nhận của đơn vị sử dụng, hợp đồng |
| Gắn với văn bằng | đối chiếu **từng dấu hiệu trong yêu cầu bảo hộ** ↔ sản phẩm đã áp dụng |

> Dòng cuối là dòng quan trọng nhất: phải chứng minh **cái đã áp dụng chính là cái được bảo hộ**, không
> phải một biến thể khác. Lập bảng đối chiếu dấu hiệu ↔ sản phẩm thật.

## Bản ghi xuất xứ đóng góp người/AI (Điều 10a)

Lấy từ B1, đưa thành tài liệu chính thức:

```markdown
### Xuất xứ đóng góp — <ứng viên>
Đóng góp đáng kể của con người:
- <ai> đề xuất <gì> ngày <ngày> — dẫn: <_meta/decisions.md | design journal | biên bản>
- Phán đoán chọn <A thay vì B> là của <ai> ngày <ngày> — dẫn: <…>
AI hỗ trợ (không phải tác giả):
- <tra prior art / dựng bảng so sánh / soạn nháp văn bản>
Kết luận tư cách tác giả: <tên> là tác giả / tác giả chính.
```

> Vì sao cần: Điều 10a — quyền chỉ được xác lập nếu **con người có đóng góp đáng kể**, và người đó mới
> **được coi là tác giả**. Cả QĐ 431 Điều 5.6 (tác giả **chính**) và QĐ 12/2025 Điều 3.2.b (tác giả)
> neo vào tư cách tác giả. Thiếu bản ghi này ⇒ rủi ro **có bằng mà không dùng được cho chức danh**.

## Trang "Khả năng / thực tế ứng dụng CNQP-AN"

Hai phần, viết riêng:
- **Quân sự:** giải pháp phục vụ nhiệm vụ gì, thay thế/cải thiện gì so với hiện trạng
- **Dân sự (lưỡng dụng):** ứng dụng ngoài quốc phòng — hợp với định hướng *"phát triển CNQP-AN theo
  hướng lưỡng dụng"* của Luật 38/2024

Dùng đúng bộ động từ của Luật 38/2024 khi mô tả: *nghiên cứu, thiết kế, chế tạo, sản xuất, sửa chữa,
cải hoán, cải tiến, hiện đại hoá, tăng hạn sử dụng* vũ khí trang bị kỹ thuật / vật tư kỹ thuật /
phương tiện kỹ thuật nghiệp vụ.

## Gói câu hỏi giao đại diện SHTT

Bắt buộc có — đây là chỗ skill tự khai báo giới hạn thay vì giả vờ đủ:

```markdown
### Câu hỏi cho đại diện sở hữu công nghiệp
Quy cách:
- [ ] Mẫu tờ khai hiện hành trong Phụ lục I <văn bản mới nhất> — số mẫu nào?
- [ ] Quy cách bản mô tả/yêu cầu bảo hộ sau khi Điều 16–28 NĐ 65/2023 bị bãi bỏ — thông tư nào của Bộ KH&CN thay thế?
- [ ] Mức phí hiện hành: thẩm định hình thức/nội dung, công bố, tra cứu, cấp văn bằng, duy trì, **phí thẩm định nội dung nhanh**
Chiến lược:
- [ ] Tra cứu novelty chính thức + FTO (pre-search của chúng tôi chỉ để chọn cái đáng đổ tiền)
- [ ] Khung claim đề xuất có sống được không; câu chữ nào cần sửa
- [ ] Xác nhận số điểm độc lập ≤02 để đủ Điều 14a.d; nên tách thành mấy đơn
- [ ] Routing sáng chế / GPHI / nộp kép có đúng không
- [ ] **Đường sáng chế MẬT**: thủ tục hiện hành? và **văn bằng mật có chứng minh được trong hồ sơ chức danh không**?
- [ ] Nếu có ý định nộp nước ngoài: trình tự xin phép BQP/BCA theo Điều 14
Thời hạn:
- [ ] Thời hạn thẩm định nội dung nhanh theo khoản 2a Điều 119 là bao lâu, so với thường?
- [ ] Thời hạn hiệu lực: sáng chế / GPHI (đối chiếu Điều 93 bản hợp nhất mới nhất)
```

## Checklist trước nộp

```
□ Chuỗi sửa đổi đã kiểm, có in ngày
□ Tờ khai theo mẫu Phụ lục I HIỆN HÀNH
□ Bản mô tả đủ 9 mục, đúng thứ tự
□ Yêu cầu bảo hộ tách riêng, làm rõ dấu hiệu mới, phù hợp mô tả + hình vẽ
□ Đếm lại: <n> điểm độc lập / <m> tổng điểm — đúng khung B3 CEO đã chọn
□ Nếu đi thẩm định nhanh: yêu cầu công bố sớm ĐÃ kèm trong hồ sơ nộp (không bổ sung sau)
□ Nếu tách đơn: đã tách NGAY từ đầu, không phải đơn tách
□ Bản tóm tắt ≤150 từ (hoặc ghi rõ sẽ bổ sung sau)
□ Hình vẽ trang riêng, đủ số hiệu tham chiếu trong mô tả
□ Hình thức: A4, lề 20mm, Times New Roman ≥13, giáp lai, không tẩy xoá
□ Mỗi đơn chỉ yêu cầu MỘT văn bằng
□ Bản ghi xuất xứ đóng góp người/AI (Điều 10a)
□ Trang khả năng/thực tế ứng dụng CNQP-AN
□ Hồ sơ chứng cứ áp dụng (nếu đích 12/2025 trong LLVT) + bảng đối chiếu dấu hiệu ↔ sản phẩm
□ Cổng Điều 14 đã chạy nếu có ý định nộp nước ngoài
□ Gói câu hỏi cho đại diện SHTT
□ Phân loại MẬT; chưa khóa priority date thì CẤM công khai
```

## Output

Ghi vào `1_Projects/<project>/IP/`:
- `Don_<ip-type>_<candidate>_<ngày>.md` — bộ đơn nháp
- `Chung_cu_ap_dung_<candidate>.md` — nếu cần
- `Xuat_xu_dong_gop_<candidate>.md` — Điều 10a
- `Handoff_dai_dien_SHTT_<ngày>.md` — gói câu hỏi + checklist
- cập nhật ledger `_pipeline_state.md` → `CLOSED — handed to IP agent <ngày>`
- ghi ngày mục tiêu **khóa priority date** vào Gate Register để QP-02-07 chặn P3 nếu chưa khóa

## Gotchas

- **Không xuất quy cách mà chưa chạy Bước 0.** Đây là lỗi đã xảy ra ba lần trong một phiên.
- **Yêu cầu công bố sớm phải nộp LÚC nộp đơn** — không bổ sung sau, mất quyền thẩm định nhanh.
- **Đơn tách mất quyền thẩm định nhanh** → tách từ đầu.
- **Bản tóm tắt ≤150 từ** và có thể bổ sung sau — đừng để nó chặn ngày nộp.
- **"Khả năng áp dụng công nghiệp" ≠ "đã được áp dụng"** — hai tài liệu khác nhau, đừng dùng lẫn.
- **Chưa có văn bản xác định bí mật nhà nước ⇒ coi như CHƯA RÕ** ⇒ không nộp nước ngoài.
- Hồ sơ chứng cứ áp dụng phải chứng minh **cái đã áp dụng chính là cái được bảo hộ**.

## COD

| Việc | COD |
|------|-----|
| Soạn bộ đơn nháp, checklist, gói câu hỏi | Offload |
| Tra chuỗi sửa đổi (Bước 0) | Offload |
| **Duyệt hồ sơ + ký giao đại diện SHTT** | **Core** |
| **Quyết có nộp nước ngoài hay không** | **Core** (sau cổng Điều 14) |
| Xác định thuộc bí mật nhà nước | **Ngoài AI** — cơ quan có thẩm quyền |
| Bản nộp cuối, câu chữ pháp lý | **Ngoài AI** — đại diện SHTT |

## Rules

- **Bước 0 bắt buộc**, in ngày kiểm chuỗi sửa đổi.
- **Tự khai báo giới hạn** — chỗ nào chưa đối chiếu được quy cách hiện hành thì ghi rõ, không giả vờ đủ.
- **Cổng Điều 14 chặn** mọi ý định nộp nước ngoài.
- Bản ghi Điều 10a là **tài liệu bắt buộc**, không phải phụ lục tuỳ chọn.
- Đầu ra là **bản nháp kỹ thuật giao đại diện SHTT**, không phải bản nộp — nói câu này trong mọi đầu ra.
- Phân loại **MẬT**; không đẩy nội dung ra tool ngoài.
