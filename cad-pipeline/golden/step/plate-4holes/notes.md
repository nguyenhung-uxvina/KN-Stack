# Golden case: plate-4holes (giải tích)

Tấm thép 1000×500×10 mm, 4 lỗ Ø50 xuyên tại (200,150) (200,350) (800,150) (800,350).
Vật liệu quy ước: Thép EH32, ρ = 7,85 g/cm³ (STEP không mang nhãn — extractor rơi
về default EH32, chủ đích).

**Mục tiêu kiểm chứng** (mục 5 đặc tả): khối lượng, diện tích, TRỪ LỖ đúng, nhầm đơn vị.

**Đáp án tính tay** (không đo từ máy — đây là điểm mấu chốt của case giải tích):
- V = 1000·500·10 − 4·π·25²·10 = 5.000.000 − 78.539,816 = 4.921.460,18 mm³ = **4921,46 cm³**
- m = 4.921.460,18 × 7,85 / 10⁶ = **38,633 kg**
- A = 2·(500.000 − 4·π·625) + 2·(1000+500)·10 + 4·π·50·10
    = 984.292,04 + 30.000 + 6.283,19 = 1.020.575,22 mm² = **10205,75 cm²**
- bbox = 1000 × 500 × 10 mm

Nguồn sinh: `golden/make_golden_v0.py` (FreeCAD 1.1.1, Import.export STEP AP214).
Lập: 2026-07-02 · Xác nhận: đáp án giải tích (2 đường: tay + FreeCAD shape.Volume
khớp tuyệt đối lúc sinh). Khi thêm case từ file THẬT: bắt buộc 2 người đo tay ký.
