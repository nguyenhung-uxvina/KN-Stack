---
name: ip-claim
description: "Block B3 của ip-invent — đề xuất phương án khung yêu cầu bảo hộ. Sinh 2-3 khung claim khác trục (rộng / hẹp / đổi trục), mỗi khung kèm bảng phân biệt với prior art gần nhất, kịch bản lùi claim khi thẩm định viên phản đối, ĐẾM điểm độc lập đối chiếu trần thẩm định nội dung nhanh (≤10 điểm yêu cầu bảo hộ, ≤02 điểm độc lập — Điều 14a), và chi phí theo số điểm độc lập. Cảnh báo bẫy: muốn về trần thì phải tách NGAY từ đầu vì đơn tách mất quyền thẩm định nhanh. Đóng khung lại giải pháp phần mềm thành hệ thống/quy trình kỹ thuật để tránh Điều 59. Triggers on: 'ip-claim', 'khung claim', 'yêu cầu bảo hộ', 'viết claim sáng chế', 'điểm độc lập', 'claim độc lập phụ thuộc', 'phân biệt prior art', 'thu hẹp claim', 'phương án bảo hộ'."
---

# ip-claim — B3: đề xuất phương án claim

> Đọc kết luận B2 (routing, prior art gần nhất, mâu thuẫn hai trục, bảng Điều 14a) từ ledger.
> **Block này đề xuất PHƯƠNG ÁN, không viết bản nộp cuối.** Bản nộp là việc của đại diện SHTT.

## Nguyên tắc: claim là nơi đánh đổi, không phải nơi tối đa hoá

Bốn thứ kéo nhau, không thể tối đa cùng lúc:

| Kéo | Muốn rộng thì | Muốn nhanh/rẻ thì |
|---|---|---|
| **Phạm vi bảo hộ** | nhiều điểm độc lập, câu chữ rộng | ít điểm, câu chữ hẹp |
| **Độ sống sót thẩm định** | hẹp, nhiều dấu hiệu phân biệt | — |
| **Tốc độ cấp bằng** | — | **≤02 điểm độc lập** (Điều 14a.d) |
| **Chi phí** | — | ít điểm độc lập (phí tính theo điểm) |

→ Việc của B3: **bày đánh đổi bằng số**, không khuyên "claim càng rộng càng tốt".

## Ràng buộc mang số — Điều 14a.d

**Trần để đủ điều kiện thẩm định nội dung nhanh: ≤10 điểm yêu cầu bảo hộ, trong đó ≤02 điểm độc lập.**

```
Với mỗi khung claim, ĐẾM và đối chiếu:
  số điểm độc lập  = ?   → ≤2 ?
  tổng số điểm     = ?   → ≤10 ?
  → vượt trần ⇒ MẤT quyền thẩm định nhanh ⇒ đi thẩm định thường (chậm hơn nhiều)
```

> 🔴 **Bẫy đơn tách.** Điều 14a.đ loại **đơn tách và đơn chuyển đổi**. Nên nếu muốn về ≤02 điểm độc lập
> thì phải **tách thành các đơn riêng NGAY TỪ ĐẦU**, không nộp một đơn nhiều điểm độc lập rồi tách sau —
> tách sau là mất luôn quyền thẩm định nhanh cho cả các đơn con.
> Quyết định này **không lùi được**, phải chốt trước khi nộp.

**Chi phí theo điểm độc lập** (TT 263/2016/TT-BTC sđ TT 31/2020 — xác nhận lại mức hiện hành):
- Phí thẩm định hình thức: tính **theo mỗi điểm yêu cầu bảo hộ độc lập**
- Đơn sáng chế có **trên 01 điểm độc lập**: từ điểm độc lập **thứ hai** trở đi phải nộp thêm **theo mỗi
  điểm**
→ Số điểm độc lập là **biến chi phí trực tiếp**. Nêu con số, đừng nói "chi phí tăng".

## Sinh 2-3 khung khác TRỤC (không phải 3 biến thể của một ý)

| Khung | Cách đóng | Dùng khi |
|---|---|---|
| **Rộng** | claim tổ hợp chức năng ở mức khái quát nhất còn phân biệt được | novelty rất sạch, chấp nhận rủi ro bị phản đối |
| **Hẹp** | thêm dấu hiệu định lượng/cấu hình cụ thể làm đặc trưng phân biệt | prior art dày, cần sống sót chắc |
| **Đổi trục** | claim ở **chỗ khác** — mục đích sử dụng, quy trình thay vì thiết bị, hoặc chính chỗ prior art "giải sai bài" | khi điểm mới thật nằm ở **đổi bài**, không ở chi tiết kỹ thuật |

> **Khung "đổi trục" thường là khung mạnh nhất** khi B2 báo *prior art giải sai bài*. Ví dụ dạng: mọi
> tài liệu trước đều **bù trừ/triệt tiêu** một hiện tượng, còn giải pháp của ta **chủ động tạo ra** nó
> cho một mục đích khác — thì đặc trưng phân biệt là **chiều tác động + mục đích**, và phải chọn câu
> chữ tránh đúng từ khoá của prior art.

## Bảng phân biệt prior art — bắt buộc cho từng khung

```markdown
| Prior art | Nội dung nó dạy | Khung này phân biệt bằng gì | Mạnh/yếu |
|---|---|---|---|
| <số đơn/bằng> | | | |
```

Yêu cầu: mỗi prior art loại (C)/(D) từ B2 **phải có một dòng**. Không được bỏ trống prior art gần nhất.
Nêu rõ **từ khoá cần TRÁNH** trong câu chữ claim (vì đã bị prior art phủ).

## Kịch bản lùi claim

Với khung được khuyến nghị, viết trước đường lùi:

```
Nếu thẩm định viên phản đối <dấu hiệu X> vì <prior art Y>:
  → lùi về: <thêm dấu hiệu phân biệt Z / chuyển X xuống điểm phụ thuộc>
  → phạm vi còn lại: <mô tả>
  → có còn đủ giá trị bảo hộ / đủ cho chức danh không? CÓ / KHÔNG
Nếu lùi hết mà vẫn bị phản đối:
  → chuyển routing sang GPHI? / rút đơn? → nêu rõ
```

> Không có đường lùi = đơn dễ chết trắng. Đây là chỗ B3 tạo giá trị nhiều nhất.

## Đóng khung tránh Điều 59 (nếu B1/B2 đánh cờ)

Giải pháp nặng thuật toán/phần mềm: **không claim chương trình máy tính hay thuật toán trần** (Điều 59).
Đóng lại thành:
- **Hệ thống/thiết bị**: đặc trưng bởi dấu hiệu **kết cấu** — cảm biến, cơ cấu, luồng tín hiệu vật lý,
  quan hệ hình học/lực
- **Quy trình kỹ thuật**: đặc trưng bởi **trình tự, điều kiện, thành phần tham gia, biện pháp, phương
  tiện** thực hiện (khớp định nghĩa giải pháp kỹ thuật của Cục SHTT)

Cách nhận biết đã đóng khung đúng: bỏ hết phần "tính toán" ra thì claim **vẫn còn một cấu hình vật lý
xác định**. Nếu bỏ ra chỉ còn công thức → chưa đủ, còn rơi Điều 59.

## Ma trận điểm — xuất bảng

| Tiêu chí | Trọng số | Khung Rộng | Khung Hẹp | Khung Đổi trục |
|---|---|---|---|---|
| Phạm vi bảo hộ | | | | |
| Độ sống sót thẩm định | | | | |
| Sức phân biệt vs prior art gần nhất | | | | |
| **Số điểm độc lập** (≤2?) | | | | |
| **Tổng điểm YCBH** (≤10?) | | | | |
| Chi phí (theo điểm độc lập) | | | | |
| Đủ Điều 14a để đi nhanh? | | | | |
| Đủ cho thước đo chức danh (B0)? | | | | |

→ Khuyến nghị **một** khung + nêu rõ **cái gì bị đánh đổi** khi chọn nó.

## Output — ledger

```markdown
## B3 — ip-claim  (Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản>)

### Khung 1 — Rộng
Điểm độc lập 1 (thiết bị/quy trình): <nội dung>
Điểm phụ thuộc: <danh sách>
Đếm: <n> điểm độc lập / <m> tổng điểm → Điều 14a.d: ĐẠT / VƯỢT TRẦN
Bảng phân biệt prior art: <bảng>
Từ khoá phải tránh: <…>

### Khung 2 — Hẹp
<như trên>

### Khung 3 — Đổi trục
<như trên>

### Ma trận điểm
<bảng>

### ⭐ KHUYẾN NGHỊ
Khung: <n> — vì <lý do>
Đánh đổi phải chấp nhận: <nói thẳng>
Nếu muốn đi thẩm định nhanh: phải tách thành <k> đơn riêng NGAY TỪ ĐẦU
  → đơn 1: <claim gì> · đơn 2: <claim gì>
Chi phí dự kiến theo điểm độc lập: <số>

### Kịch bản lùi
<đường lùi từng bước>

### Câu hỏi cho đại diện SHTT
- [ ] <những chỗ cần phán đoán pháp lý chuyên môn>

⏸️ CEO: chọn khung claim.
```

## Gotchas

- **Đếm điểm độc lập, đừng ước.** Trần 2 điểm là cứng; một claim phương pháp phụ thêm là đủ vượt.
- **Tách phải tách từ đầu** — đơn tách mất quyền thẩm định nhanh (Điều 14a.đ). Không lùi được.
- **Mỗi đơn chỉ một văn bằng** → nộp kép là hai đơn, và loại văn bằng phải phù hợp đối tượng.
- **Claim rộng không phải luôn tốt.** Với mục tiêu chức danh, thứ cần là **bằng ĐƯỢC CẤP** — claim hẹp
  mà cấp được thắng claim rộng bị treo.
- **Đừng dùng từ khoá của prior art** trong đặc trưng phân biệt; đó là cách nhanh nhất bị đọc là trùng.
- Nếu tất cả khung đều không phân biệt được với prior art (D) → **báo lại B2**, có thể phải loại ứng
  viên hoặc chuyển GPHI, đừng cố viết cho có.

## COD

| Việc | COD |
|------|-----|
| Sinh khung, dựng bảng phân biệt, đếm điểm, tính chi phí | Offload |
| **Chọn khung claim** | **Core** — quyết định phạm vi bảo hộ của xưởng |
| **Quyết đánh đổi phạm vi ↔ tốc độ cấp bằng** | **Core** |
| Câu chữ pháp lý bản nộp cuối | **Ngoài AI** — đại diện SHTT |

## Rules

- Sinh **khác trục**, không phải 3 biến thể một ý.
- **Mọi prior art (C)/(D) từ B2 phải có dòng trong bảng phân biệt.**
- **Luôn đếm và đối chiếu trần ≤10/≤02**; nêu rõ hệ quả nếu vượt.
- **Luôn viết kịch bản lùi.**
- Chi phí nêu **bằng số theo điểm độc lập**, không nói chung.
- Đây là **bản nháp kỹ thuật**, không phải bản nộp — nói câu này trong mọi đầu ra.
