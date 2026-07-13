# Golden case: box-tube (giải tích)

Hộp chữ nhật thành mỏng 60×40 mm, dày 3 mm, dài 1000 mm (lòng 54×34 xuyên suốt).
Vật liệu quy ước: Thép EH32, ρ = 7,85 g/cm³.

**Mục tiêu kiểm chứng**: chi tiết thành mỏng (thể tích nhỏ so bao hình — dễ lộ lỗi
V ≤ bbox nếu extractor đọc nhầm), mặt TRONG có được tính vào diện tích không.

**Đáp án tính tay:**
- V = (60·40 − 54·34)·1000 = (2400 − 1836)·1000 = 564.000 mm³ = **564,00 cm³**
- m = 564.000 × 7,85 / 10⁶ = **4,427 kg**
- A = 2·(60+40)·1000 [ngoài] + 2·(54+34)·1000 [trong] + 2·564 [2 vành đầu]
    = 200.000 + 176.000 + 1.128 = 377.128 mm² = **3771,28 cm²**
- bbox = 60 × 40 × 1000 mm

Nguồn sinh: `golden/make_golden_v0.py`. Lập: 2026-07-02 · Xác nhận: giải tích 2 đường.
