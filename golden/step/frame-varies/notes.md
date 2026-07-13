# Golden case: frame-varies (giải tích — regression từ lỗi thật)

Hai thanh 40×40 mm CÙNG tên gốc "ThanhGoc" (hậu tố instance `001` kiểu STEP/Inventor),
KHÁC chiều dài: L=500 và L=1000 — mô phỏng thanh Frame Generator cùng profile.

**Nguồn gốc case**: bug bắt bởi sensor S1-01 trên `Tong lap.iam` THẬT (BM-01,
2026-07-02): nhóm mass_varies lấy `est_mass_kg` từ instance NHẸ NHẤT nhưng
`volume/bbox` từ instance ĐẦU TIÊN → "ISO L40x40x4: mass=0,133 kg vs V×ρ=1,189 kg
(794%)". Quy tắc mục 4.3: lỗi đã xảy ra một lần → vào golden set vĩnh viễn.

**Mục tiêu kiểm chứng**: gộp instance khác khối lượng — est/volume/bbox phải thuộc
CÙNG MỘT instance (thanh ngắn), total = Σ thật, unit_mass_range đúng.

**Đáp án tính tay** (Thép EH32, ρ = 7,85 g/cm³):
- Thanh ngắn: V = 40·40·500 = 800.000 mm³ = **800 cm³**; m = **6,280 kg**;
  A = 2·40·40 + 4·40·500 = 83.200 mm² = **832,00 cm²**; bbox 40×40×500
- Thanh dài:  V = 1600 cm³; m = **12,560 kg**
- Nhóm: qty = 2, mass_varies = true, est = 6,280 (min), range [6,280; 12,560],
  **total = 18,840 kg**, volume/area/bbox = của thanh ngắn

Nguồn sinh: `golden/make_golden_v0.py`. Lập: 2026-07-02 · Xác nhận: giải tích 2 đường.
