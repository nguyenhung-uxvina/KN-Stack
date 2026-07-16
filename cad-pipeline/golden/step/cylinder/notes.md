# Golden case: cylinder (giải tích)

Trụ đặc Ø100 × 200 mm. Vật liệu quy ước: Thép EH32, ρ = 7,85 g/cm³.

**Mục tiêu kiểm chứng**: mặt cong (không phải hình hộp), đồng thời là ca thử cho
rule đẳng chu S1-05 — trụ có A/V thấp, sẽ FAIL oan nếu ai đó "sửa lại" S1-05 về
công thức hình hộp của bản dự thảo gốc (xem chú thích (*) trong đặc tả).

**Đáp án tính tay:**
- V = π·50²·200 = 1.570.796,33 mm³ = **1570,80 cm³**
- m = 1.570.796,33 × 7,85 / 10⁶ = **12,331 kg**
- A = 2·π·50² + 2·π·50·200 = 15.707,96 + 62.831,85 = 78.539,82 mm² = **785,40 cm²**
- bbox = 100 × 100 × 200 mm

Nguồn sinh: `golden/make_golden_v0.py`. Lập: 2026-07-02 · Xác nhận: giải tích 2 đường.
