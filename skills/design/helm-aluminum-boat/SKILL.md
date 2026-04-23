---
name: helm-aluminum-boat
description: Quy trình chế tạo và thử nghiệm xuồng nhôm cỡ nhỏ (4-10m). Bao gồm trình tự chế tạo, quy trình hàn nhôm 5083, NDT kiểm tra mối hàn (VT/PT/RT/UT step-by-step), thử nghiệm tại bến và thử biển. Triggers on "chế tạo xuồng nhôm", "aluminum boat manufacturing", "quy trình hàn nhôm", "thử nghiệm xuồng", "boat testing", "đăng kiểm xuồng", "welding procedure nhôm", "aluminum hull fabrication", "xuồng nhôm", "NDT nhôm", "kiểm tra mối hàn", "dye penetrant aluminum", "ultrasonic weld test", "AWS D1.2".
---

# HELM Aluminum Boat — Quy Trình Chế Tạo & Thử Nghiệm Xuồng Nhôm Cỡ Nhỏ

Hướng dẫn step-by-step từ tôn nhôm thô → xuồng hoàn thiện → thử biển đạt đăng kiểm. Freedom level: LOW (sai quy trình = hỏng sản phẩm / mất an toàn).

## When to Use

- Lập quy trình chế tạo xuồng nhôm mới (VN-XUONG-UUV, AST-MSL-001)
- Review/audit quy trình hàn nhôm tại xưởng
- Chuẩn bị hồ sơ đăng kiểm phương tiện thủy
- Lập checklist thử nghiệm tại bến và thử biển
- Training thợ hàn mới về aluminum marine welding
- Lập quy trình NDT kiểm tra mối hàn nhôm (VT/PT/RT/UT)
- Chuẩn bị biên bản NDT cho đăng kiểm

## 5 Quy Tắc Bất Di Bất Dịch

1. **KHÔNG BAO GIỜ dùng ER4043 cho vỏ 5xxx** — Silicon + Magnesium = Magnesium Silicide (giòn) → nứt vỡ SCC trên biển. Chỉ dùng ER5183 hoặc ER5356.
2. **Tẩy dầu TRƯỚC KHI chải** — Chải tôn dính dầu = ép hydrocarbon vào bề mặt nhôm → rỗ khí nghiêm trọng khi hàn. Quy trình: acetone → chải inox → hàn.
3. **Nhiệt độ liên pass < 150°C** — Giữ 5083 ở 65-200°C quá lâu → sensitization (Mg cluster) → mất khả năng chống ăn mòn biển + yếu HAZ.
4. **Bàn chải inox CHUYÊN DỤNG cho nhôm** — Chải đã dùng cho thép = nhiễm sắt → ăn mòn galvanic → gỉ sét trên vỏ nhôm. Đánh dấu màu, để riêng.
5. **PHẢI có khung gia cường** — "Frameless" = tăng dày tôn cực lớn, nặng, đắt, không thực tế. Mọi xuồng nhôm phải có framing (stringer, web frame, vách ngăn).

## Quy Trình Chế Tạo (8 Bước)

### Bước 1: Thiết Kế & Triển Khai (Design & Lofting)

- CAD lofting → nest parts tối ưu vật liệu
- Xuất file cắt CNC/plasma
- Xác nhận vật liệu: 5083-H116 (hull), 6061-T6 (extrusions nếu cần)
- **Decision:** Frames-first hay Plate-first?
  - Frames-first → hull phức tạp, nhiều compound curve
  - Plate-first → hull developable (single-curve), fairness tốt hơn, thợ ít kinh nghiệm

### Bước 2: Xử Lý Vật Liệu (Material Prep)

- Rửa kiềm (alkaline clean) loại bỏ oxide film
- Passivation chromate tăng chống ăn mòn
- Kiểm tra chứng chỉ vật liệu (mill cert): đúng grade, temper, thickness
- Lưu kho: kê cao, tránh ẩm, không chồng lên thép

### Bước 3: Cắt & Chuẩn Bị Mép (Cutting & Edge Prep)

- Cắt plasma (tôn) — tránh biến dạng nhiệt
- Cắt CNC saw (profile/extrusion)
- Mép hàn tôn > 4-5mm: V-groove 60°, land 1.5mm (chống thủng gốc)
- Mép hàn tôn ≤ 4mm: mép vuông (square butt), gap 1-2mm
- Vệ sinh mép: acetone → chải inox chuyên dụng → hàn trong 4h

### Bước 4: Lắp Ráp Khung (Frame Assembly)

- Uốn T-extrusion → hàn vào floor CNC-cut trên bàn phẳng
- Dung sai khung: < 1mm
- Đặt khung lên keel bar (cách sàn ~300mm)
- Kỹ thuật "egg-crate": notch-to-notch interlocking cho alignment nhanh
- Kiểm tra: vuông góc, thẳng hàng, khoảng cách đều

### Bước 5: Bọc Tôn Vỏ (Hull Plating)

- Uốn nguội (cold forming/wheeling) cho compound curves
- Hot bending: KHÔNG quá 200°C (5xxx-series)
- Bắt đầu từ vùng phẳng → tiến đối xứng 2 bên
- Tack weld mỗi 150mm, kéo tôn dưới tension để tạo hình
- **Decision:** MIG hay TIG?
  - MIG (Pulse GMAW) → seam dài, tôn dày ≥ 3mm, năng suất cao
  - TIG (GTAW) → tôn mỏng < 3mm, chi tiết phức tạp, root pass

### Bước 6: Hàn Vỏ (Welding Sequence)

**Setup thiết bị MIG:**
- Liner: Teflon hoặc Carbon-Teflon (KHÔNG dùng liner thép)
- Drive rolls: U-Groove only (KHÔNG V-Groove — đè dẹp dây nhôm)
- Contact tip: loại dành cho nhôm (ký hiệu "A"), oversized

**Kỹ thuật hàn:**
- Góc đẩy (push/forehand) 10-15° — gas bảo vệ làm sạch oxide trước hồ quang
- Back-stepping: hàn từng đoạn 300mm, lùi về — giảm biến dạng
- Crater fill: ramp down dòng 2-3 giây cuối — tránh nứt hố
- Nhiệt độ liên pass: < 150°C (thử bằng tay găng — nóng = dừng)
- Seam ngoài: gouge + flush weld cho full thickness

**Filler wire:**
- ER5183: mối hàn mạnh hơn, ductile hơn → ưu tiên cho hull
- ER5356: dễ hàn hơn, ok cho kết cấu phụ
- TUYỆT ĐỐI KHÔNG dùng ER4043

### Bước 7: Xử Lý Bề Mặt (Surface Treatment)

- Bên trong: etch + sơn epoxy high-build (bilge)
- Bên ngoài:
  1. Phun cát (sandblast)
  2. Sơn lót epoxy chống ăn mòn (ngay sau phun cát — < 4h)
  3. Bả fairing: epoxy/glass epispheres (low density)
  4. Tie-coat + sơn chống hà (antifouling)
- **VN tropical note:** ẩm độ cao → sơn lót trong 2h sau phun cát, không để qua đêm

### Bước 8: Lắp Đặt & Hoàn Thiện (Fitting Out)

- Vách ngăn, cabin, hệ thống ống
- Hệ thống điện, đèn hàng hải
- Động cơ + hệ truyền động
- Hệ thống lái
- Trang thiết bị an toàn (theo QCVN 72)

## Kiểm Tra Chất Lượng (QC Checklist)

### NDT Decision Tree — Chọn Phương Pháp

```
Mối hàn cần kiểm tra
  ├─ Tôn ≤ 8mm → RT (radiographic) cho khuyết tật ngầm
  ├─ Tôn > 8mm → UT (ultrasonic) cho khuyết tật ngầm
  ├─ Mọi mối hàn → VT (visual) 100%
  ├─ Critical joints (chine, keel, transom, vách kín) → PT (dye penetrant)
  └─ T-joints, cruciform, fillet → UT only (RT không thể chụp)
```

**IF** đăng kiểm VR/QCVN 72 → VT 100% + PT critical + RT/UT theo yêu cầu giám sát viên
**IF** xuồng < 10m nội địa → VT 100% + PT critical là đủ (RT/UT khi có yêu cầu hợp đồng)

### VT — Visual Testing (100% mối hàn)

Kiểm tra ngay sau hàn, trước khi xử lý bề mặt:

| Tiêu chí | Giới hạn chấp nhận | Hành động nếu FAIL |
|----------|--------------------|--------------------|
| Nứt (crack) | **KHÔNG chấp nhận** — bất kỳ kích thước nào | Mài bỏ + hàn lại |
| Undercut | < 0.5mm depth (AS/NZS 1665 marine) | Hàn bù nếu > 0.5mm |
| Rỗ khí bề mặt | Không cụm, đơn lẻ < 1.5mm | Mài + hàn lại nếu cụm |
| Wetting/toe angle | Đều, góc < 90° | Chỉnh kỹ thuật hàn |
| Chiều cao excess | ≤ 3mm (butt), ≤ 1.5mm convexity (fillet) | Mài flush |
| Lack of fusion (cold lap) | **KHÔNG chấp nhận** | Gouge + hàn lại |

### PT — Dye Penetrant Testing (7 bước)

**Áp dụng cho:** mối hàn critical — chine, keel line, transom, vách kín nước, gusset chịu lực.
**Tiêu chuẩn:** ASTM E165 / ISO 23277 / AWS D1.2.

**Bước 1 — Làm sạch bề mặt**
- Lau acetone bằng vải không xơ (lint-free) → loại dầu mỡ
- Chải inox chuyên dụng (KHÔNG dùng chải đã chạm thép)
- Làm sạch ≥ 25mm mỗi bên mối hàn
- Để khô hoàn toàn ở nhiệt độ phòng

**Bước 2 — Bôi penetrant (chất thẩm thấu)**
- Xịt aerosol đỏ (Type 2 visible) phủ kín toàn bộ mối hàn
- Nhiệt độ bề mặt: 5°C – 52°C (ASTM E165)
- **VN tropical:** xưởng nóng > 40°C → xịt lúc sáng sớm hoặc chiều muộn

**Bước 3 — Dwell time (ngâm thấm)**
- **20 phút** (tiêu chuẩn cho aluminum weld cracks)
- Nứt nhỏ/micro-crack: tăng lên 30 phút
- KHÔNG để penetrant khô trên bề mặt (xịt bổ sung nếu bay hơi nhanh)

**Bước 4 — Lau sạch thừa**
- Lau bằng vải lint-free + dung môi remover
- **KHÔNG BAO GIỜ xịt remover trực tiếp lên bề mặt** → rửa trôi penetrant trong vết nứt
- Lau cho đến khi nền sạch, chỉ còn dấu penetrant trong khuyết tật

**Bước 5 — Bôi developer (chất hiện)**
- Xịt developer trắng (non-aqueous wet) lớp mỏng đều
- Giữ khoảng cách xịt 200-300mm
- **Chờ ≥ 10 phút** để developer hút penetrant lên bề mặt (bleed-out)

**Bước 6 — Kiểm tra (đọc kết quả)**
- Ánh sáng trắng đủ sáng cho Type 2 (visible red dye)
- Fluorescent (Type 1): phòng tối, UV-A 365nm ≥ 1000 µW/cm², ánh sáng trắng ≤ 2 fc
- Ghi nhận: vị trí, hình dạng (tuyến tính/tròn), kích thước mỗi indication
- **Nứt = REJECT** bất kỳ kích thước nào

**Bước 7 — Làm sạch sau kiểm tra**
- Lau sạch developer + penetrant còn lại bằng dung môi
- **⚠️ CRITICAL cho nhôm:** Nếu sẽ hàn sửa → phải tẩy sạch 100% penetrant dầu gốc (oil-based) khỏi vùng hàn. Penetrant còn lại → rỗ khí nghiêm trọng khi hàn

### RT — Radiographic Testing (tôn ≤ 8mm, butt joints)

**Khi nào:** đăng kiểm yêu cầu, hoặc mối butt chịu lực chính tôn < 8mm.
**Yêu cầu:** truy cập 2 mặt, ASNT Level II operator, ISO 10675 acceptance.

| Khuyết tật | Chấp nhận | Reject |
|-----------|----------|--------|
| Rỗ khí đơn lẻ | ≤ 2mm hoặc ≤ T/4 (nhỏ hơn) | Cụm rỗ khí, aligned porosity |
| LOF (Lack of Fusion) | **KHÔNG chấp nhận** | Mọi kích thước |
| Incomplete penetration | **KHÔNG chấp nhận** | Mọi kích thước |
| Slag/oxide inclusion | ≤ T/3, max 6mm | Dài hơn giới hạn |

### UT — Ultrasonic Testing (tôn > 8mm)

**Khi nào:** tôn dày > 8mm, T-joints, cruciform joints (nơi RT không thể chụp).
**Tiêu chuẩn:** ASME Sec V Article 4 & 5 / AWS D1.2 / ISO 11666.

**Setup thiết bị:**
- Máy: Pulse-echo A-Scan, tần số 1-5 MHz (thường dùng 4 MHz)
- Đầu dò angle beam: 70° cho 12.5mm, 60°/70° cho 12.5-25.4mm, 45°/60° cho > 25.4mm
- Couplant: glycerin hoặc SAE No.20 motor oil — **DÙNG CÙNG LOẠI cho calibration và scan**

**Calibration:**
- Dùng block V1 & V2 (cùng loại vật liệu với chi tiết kiểm tra)
- Lập DAC curve (Distance Amplitude Correction) ở 40-80% full screen height
- Kiểm tra lại calibration: nếu DAC shift > 2 dB → recalibrate + kiểm tra lại từ lần cal cuối

**Quy trình scan:**
1. Straight beam trước → scan HAZ + base metal → phát hiện reflector nền
2. Angle beam → vuông góc trục hàn, từ 2 hướng → phát hiện nứt dọc
3. Angle beam → song song trục hàn → phát hiện nứt ngang
4. Tốc độ scan: ≤ 150 mm/s, overlap ≥ 10% transducer width
5. Gain: ≥ 2× primary reference level

**Đánh giá & chấp nhận:**
- Indication > 20% DAC → điều tra chi tiết (hình dạng, vị trí, kích thước)
- Sizing: half-value method (6 dB drop)
- **Cracks, LOF, incomplete penetration → REJECT bất kỳ kích thước**
- Linear imperfection khác: reject nếu vượt T/4 (T ≤ 19mm), T/3 (19-57mm), 19mm (T > 57mm)

### Quy Tắc Mở Rộng Kiểm Tra (Escalation Rules)

| Tỷ lệ lỗi | Hành động |
|-----------|----------|
| < 10% checkpoints lỗi | Tiếp tục chế tạo bình thường |
| ≥ 10% checkpoints lỗi (LR, NK) | Mở rộng kiểm tra + điều tra nguyên nhân gốc |
| ≥ 20% checkpoints lỗi (KR) | Tăng gấp đôi phạm vi kiểm tra (→ 40% checkpoints) |
| DNV: 1 lỗi cần sửa | Kiểm thêm 2 đoạn cùng chiều dài |
| Lỗi lặp lại hệ thống | Dừng hàn → review WPS → khắc phục → hàn lại |

### Mẫu Biên Bản NDT (NDT Report Template)

```markdown
## BIÊN BẢN KIỂM TRA NDT — [Tên Xuồng / Mã Dự Án]

**Ngày:** YYYY-MM-DD
**Người kiểm tra:** [Tên, chứng chỉ ASNT Level]
**Phương pháp:** VT / PT / RT / UT (chọn)
**Tiêu chuẩn áp dụng:** AWS D1.2 / QCVN 72 / ISO [số]

### Thông Tin Mối Hàn
| # | Vị trí | Loại mối hàn | Chiều dày (mm) | Filler wire |
|---|--------|-------------|---------------|------------|
| 1 | Keel seam Fr.3-Fr.5 | Butt | 5 | ER5183 |

### Kết Quả Kiểm Tra
| # | Vị trí | Indication | Kích thước | Đánh giá | PASS/FAIL |
|---|--------|------------|-----------|----------|-----------|
| 1 | Keel seam Fr.4 | Linear | 8mm | Incomplete fusion | FAIL |

### Tỷ Lệ Lỗi
- Tổng checkpoints: ___
- Checkpoints lỗi: ___ ( __%)
- Escalation required? YES / NO

### Hành Động Khắc Phục
| # | Lỗi | Hành động | Deadline | Người thực hiện |
|---|-----|-----------|---------|----------------|
| 1 | LOF Fr.4 | Gouge + re-weld + re-inspect | ___ | ___ |

### Kết Luận
- [ ] PASS — Mối hàn đạt tiêu chuẩn
- [ ] FAIL — Cần sửa chữa và kiểm tra lại
- [ ] CONDITIONAL — Đạt với điều kiện [ghi rõ]

**Chữ ký kiểm tra viên:** _______________
**Chữ ký giám sát (QC/đăng kiểm):** _______________
```

### 3 NDT Gotchas Cho Nhôm

| # | Gotcha | Tại sao nguy hiểm | Phòng ngừa |
|---|--------|-------------------|------------|
| 1 | PT oil-based residue trước hàn sửa | Penetrant dầu gốc → rỗ khí nghiêm trọng khi hàn lại | Tẩy sạch 100% penetrant bằng acetone + chải TRƯỚC KHI hàn sửa |
| 2 | UT trên nhôm grain thô | Hạt nhôm không đồng nhất → standing waves + velocity changes → false reading | Dùng tần số thấp hơn (2 MHz), tăng gain, double-check bằng RT nếu nghi ngờ |
| 3 | RT trên T-joint/fillet | RT không chụp được T-joint — chỉ chụp butt joint có truy cập 2 mặt | Dùng UT hoặc PAUT cho T-joints, fillet welds, cruciform joints |

### Kiểm tra kín nước

- Hose test: phun nước áp lực lên mối hàn → quan sát rò rỉ bên trong
- Chalk test: bôi phấn bên trong, dầu bên ngoài → phấn đổi màu = rò
- Pressure test (nếu có khoang kín): 0.2 bar, giữ 15 phút, không sụt áp

### Kiểm tra kích thước

- Chiều dài tổng: ± 5mm
- Chiều rộng: ± 3mm
- Frame spacing: ± 2mm
- Đường nước thiết kế: ± 10mm
- Đối xứng trái-phải: ± 3mm

## Thử Nghiệm Tại Bến (Dock Trial)

1. **Hạ thủy** — quan sát mớn nước, nghiêng, chúi
2. **Kiểm tra rò rỉ** — 24h neo tại bến, kiểm tra bilge
3. **Khởi động động cơ** — idle, kiểm tra cooling, exhaust, vibration
4. **Hệ thống lái** — full lock port/starboard, response time
5. **Hệ thống điện** — đèn, bơm, radio, navigation lights
6. **Thiết bị an toàn** — phao, bình chữa cháy, pháo sáng

## Thử Biển (Sea Trial)

### Điều kiện thử

- Sóng ≤ SS3, gió ≤ 15 knots (điều kiện tốt)
- Vùng nước đủ sâu (≥ 3× draft)
- Thông báo đăng kiểm 7 ngày trước

### Nội dung thử (10 bài)

| # | Bài thử | Tiêu chí đạt |
|---|---------|-------------|
| 1 | Tốc độ tối đa | Đạt ≥ 90% tốc độ thiết kế |
| 2 | Tiêu hao nhiên liệu | ≤ 110% thiết kế tại tốc độ hành trình |
| 3 | Quay trở (turning circle) | Bán kính ≤ 3× LOA |
| 4 | Dừng khẩn cấp (crash stop) | Quãng đường dừng ≤ 4× LOA |
| 5 | Chạy lùi | Ổn định, lái được |
| 6 | Endurance (1h @ cruise) | Nhiệt độ động cơ ổn định, không rò rỉ |
| 7 | Dao động (vibration) | Không rung bất thường ở hull/engine mount |
| 8 | Ổn định tĩnh (nếu yêu cầu) | GM theo tính toán ± 10% |
| 9 | Hệ thống điện tải | Tất cả thiết bị chạy đồng thời |
| 10 | Thông tin liên lạc | Radio, GPS hoạt động |

### Biên bản thử biển

Ghi nhận: ngày, thời tiết, sóng gió, người tham gia, kết quả từng bài, bất thường, kết luận PASS/FAIL, chữ ký đăng kiểm viên (nếu có).

## 7 Failure Modes Thường Gặp

| # | Lỗi | Nguyên nhân | Phát hiện | Phòng ngừa |
|---|-----|-------------|-----------|------------|
| 1 | Rỗ khí (Porosity) | Không tẩy dầu trước chải, tốc độ quá cao | VT: mối hàn như sâu bướm; RT: lỗ rỗ | Acetone → chải → hàn. Amperage đủ |
| 2 | Nứt SCC | Dùng ER4043, hoặc sensitization | Nứt vỏ khi vận hành biển | ER5183/5356 only. Interpass < 150°C |
| 3 | Nứt hố (Crater crack) | Ngắt hồ quang đột ngột | Nứt hình sao cuối mối hàn | Crater fill 2-3 giây |
| 4 | Gỉ sét galvanic | Chải/đá mài nhiễm thép | Đốm gỉ trên bề mặt nhôm | Dụng cụ chuyên dụng, đánh dấu màu |
| 5 | Biến dạng vỏ (Hungry horse) | Hàn liên tục dài, nhiệt cao | Tôn gợn sóng giữa khung | Back-stepping 300mm, tack 150mm |
| 6 | Bám đen (Black smut) | Voltage quá cao, arc dài | Bụi đen dọc mối hàn | Giảm voltage, đúng arc length |
| 7 | Thủng gốc (Melt-through) | Nhôm yếu ở nhiệt cao, chảy lỏng | Pool rơi qua mặt sau | Backing plate + land 1.5mm |

## Tiêu Chuẩn Áp Dụng

| Tiêu chuẩn | Nội dung |
|------------|---------|
| AWS D3.7 | Guide for Aluminum Hull Welding |
| AWS D1.2 | Structural Welding Code — Aluminum |
| QCVN 72 | Quy phạm phân cấp phương tiện thủy nội địa (VN) |
| QCVN 42 | Trang bị an toàn tàu biển (VN) |
| ISO 10675 | NDT of welds — Acceptance levels for RT |
| ISO 23277 | NDT of welds — Penetrant testing |
| 5083-H116 | Marine grade aluminum plate (ASTM B928) |

## VN Tropical Considerations

- **Ẩm độ cao** → sơn lót < 2h sau phun cát (không chờ qua đêm)
- **Nhiệt độ cao** → nhôm nguội chậm hơn ở xưởng nóng, giám sát interpass temperature chặt hơn
- **Nước biển VN** → salinity cao, cần antifouling + anodes kẽm đúng chuẩn
- **Đăng kiểm VN** → Cục Đăng kiểm Việt Nam (VR) theo QCVN 72, không theo Lloyd's/ABS

## NLM Reference

- Notebook: `skill-alboat` (16 sources) — query cho deeper domain context
- Key sources:
  - "Welding 5083 Marine Grade Aluminum" (materialwelding.com) — welding procedures
  - "Frames First or Plating First?" (Kasten Marine) — construction approach
  - "Aluminum For Boats" (Kasten Marine) — material selection
  - "Round-bilge aluminium shell construction" (Nordkyn Design) — frame fabrication
  - "NDT Examination Methods for Ships" (TWI) — NDE inspection regimes, classification society rules
  - "Dye Penetration Test" (whatispiping.com) — PT step-by-step procedure, ASTM E165
  - "AWS D1.2 Essential Guide" (megmeet-welding.com) — AWS D1.2 scope, WPS requirements
  - "Ultrasonic Testing Procedure" (inspection-for-industry.com) — UT equipment, calibration, scanning
  - "ASTM E165 Standard Practice" (labsinus.com) — PT acceptance criteria, fluorescent vs visible
- Conversation ID: 338ab720-b833-44a4-ba8a-a099c497078c

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| Lập quy trình chế tạo | Offload | AI draft, CEO review |
| Quyết định frames-first/plate-first | **Core** | CEO judgment based on hull design |
| Giám sát hàn | **Core** | Thợ hàn + supervisor tại xưởng |
| Kiểm tra mối hàn (VT/PT) | **Core** | QC inspector tại xưởng |
| Lập biên bản thử biển | Offload | AI template, CEO fills data |
| Quyết định PASS/FAIL | **Core** | CEO + đăng kiểm viên |
