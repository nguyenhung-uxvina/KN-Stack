# WX-QT-DRAWING-SENSOR-01 — ĐẶC TẢ KỸ THUẬT SCRIPT THẨM ĐỊNH BẢN VẼ/MÔ HÌNH CAD ĐẦU VÀO

> Harness tầng 1 (bản vẽ đầu vào) — đứng TRƯỚC tầng trích xuất (WX-QT-EXTRACT-SENSOR-01).
> Áp dụng khung Guides – Sensors – Gates. Tác nhân cần kiểm soát: kỹ sư thiết kế,
> đối tác gửi bản vẽ, và sau này là AI sinh bản vẽ — cùng sensors, cùng gates, chỉ khác nguồn.
> Mã tài liệu: WX-QT-DRAWING-SENSOR-01 | Phiên bản: 1.0 | Trạng thái: Dự thảo | 2026-07
> Mã rule dùng tiền tố **D** (Drawing) — phân biệt với **S** (tầng trích xuất).

## 1. MỤC ĐÍCH, PHẠM VI, NGUYÊN TẮC

- **Mục đích**: mọi bản vẽ/mô hình chỉ được cấp trạng thái **"Released"** (và từ đó mới
  vào pipeline trích xuất → 5 đầu ra) sau khi qua thẩm định máy + ký duyệt người.
- **Phạm vi**: file CAD 3D (Inventor .ipt/.iam, SolidWorks, Rhino .3dm, STEP) và bản
  vẽ 2D (.idw/.dwg/.dxf) do nội bộ vẽ hoặc đối tác gửi.
- **Nguyên tắc**: sensor khách quan, chạy máy, chạy rẻ (kỹ sư tự self-check trước khi
  nộp); FAIL chặn tuyệt đối; mỗi lỗi lọt lưới trong sản xuất → thêm rule/case mới.
- **Bằng chứng thực địa làm nền** (Tong lap.iam BM-01, 2026-07-02): 49/49 part
  Material="Generic", 0/49 mass cache, 11 part skeleton/khung KT lọt vào BOM, BOM view
  Parts Only bị Disabled — toàn bộ đều thuộc lớp lỗi mà tầng này phải chặn TRƯỚC khi
  file đến tay tầng trích xuất.

## 2. KIẾN TRÚC SCRIPT THẨM ĐỊNH

```
drawing_check (script thẩm định — read-only tuyệt đối)
├── Lớp D1  Metadata/iProperties      — Apprentice/rhino3dm, KHÔNG cần mở CAD (rẻ nhất, chạy 100%)
├── Lớp D2  Hình học 3D               — Apprentice một phần; interference cần Inventor/SW API
├── Lớp D3  Bản vẽ 2D                 — ezdxf (parse_mech_drawing) + Inventor API cho .idw
├── Lớp D4  Checklist THEO LOẠI chi tiết — WA/WS/MC/SM/HU/AS (bảng mục 6)
├── Lớp D5  Phân loại mật             — iProperty Classification + vị trí thư mục
└── Xuất drawing_report.json  (PASS/WARNING/FAIL từng rule, = biểu mẫu WX-QT-DRAWING-F01)
```

Loại chi tiết đọc từ iProperty bắt buộc **`WX_PartType`** ∈ {WA, WS, MC, SM, **CP**,
HU, AS, STD} (CP = composite; STD = chi tiết mua tiêu chuẩn/gỗ đệm, chỉ chạy D1/D5 +
ghi chú riêng). Thiếu `WX_PartType` → FAIL D1-10 (không phân loại được thì không chọn
được checklist — buộc khai từ template).

Ngoài checklist theo LOẠI CHI TIẾT (D4), sản phẩm thuộc một **lớp sản phẩm** đã có hồ
sơ (Phụ lục B: lớp BM — bia mục tiêu nổi) phải chạy thêm bộ rule cấp sản phẩm của lớp đó.

## 3. LỚP D1 — METADATA / iPROPERTIES (chạy được NGAY hôm nay bằng Apprentice)

| Mã | Rule | Điều kiện | Mức |
|---|---|---|---|
| D1-01 | Mã chi tiết đúng quy ước | Part Number khớp regex `<DựÁn>.<Cụm>.<ChiTiết>[.<Rev>]` (vd `BM01.02.05.A`); khớp tên file | FAIL |
| D1-02 | Vật liệu đã gán và thuộc danh mục duyệt | Material ∉ {rỗng, Generic, Default, Material}; thuộc danh mục khóa cứng (5083, 5086, 6061-T6, 6082-T6, EH32, CT3, SS400, SUS304…) | FAIL ⚑ |
| D1-03 | Revision có | iProperty Revision Number ≠ rỗng; khớp khung tên bản vẽ | FAIL |
| D1-04 | Người thiết kế có | Designer/Engineer ≠ rỗng | WARNING |
| D1-05 | Tên gọi (Description) có | Description ≠ rỗng, tiếng Việt có dấu | WARNING |
| D1-06 | Mass cache hợp lệ | Physical properties đã Update+Save (mass ≠ rỗng/0) VÀ mass ≈ V×ρ(material) ±2% — mass tính trên Generic sẽ lộ ngay tại đây | FAIL ⚑ |
| D1-07 | Đơn vị tài liệu | Document units = mm (và kg) | FAIL |
| D1-08 | Quy cách phôi | Stock Number có với thép hình/tấm (L40×40×4, tấm 5mm…) | WARNING |
| D1-09 | Part phi-chế-tạo đúng vai | Skeleton/khung KT/mẫu/khuôn: BOM Structure = Reference hoặc Phantom (không lọt vào BOM) | FAIL ⚑ |
| D1-10 | Phân loại chi tiết | iProperty `WX_PartType` có và hợp lệ | FAIL |
| D1-11 | BOM view sẵn sàng (assembly) | Parts Only view Enabled trong tài liệu .iam | WARNING ⚑ |

⚑ = rule có bằng chứng thực địa ngày 2026-07-02 (chính là các lỗi đã dính).

## 4. LỚP D2 — HÌNH HỌC 3D

| Mã | Rule | Điều kiện | Mức |
|---|---|---|---|
| D2-01 | Solid kín | Part có ≥1 solid body kín (watertight); chỉ có surface hở → FAIL; >1 body không khai chủ đích (multi-body weldment phải ghi chú) → WARNING | FAIL |
| D2-02 | Không lỗi topology | Check quality (SW Check / Inventor / OCC BRepCheck): mặt tự cắt, sliver | WARNING |
| D2-03 | Kích thước bao hợp lý | Chiều lớn nhất ≤ ngưỡng theo loại (part đơn ≤ 13.000 mm; vượt → nghi lỗi đơn vị ×10, đối chiếu D1-07) | FAIL |
| D2-04 | Interference assembly | Kiểm tra va chạm: thể tích giao > 100 mm³ giữa 2 part không phải mối ren/ép → FAIL; 1–100 mm³ → WARNING (fit hàn) | FAIL/WARNING |
| D2-05 | Ràng buộc lắp đầy đủ | Không occurrence "trôi" (chưa ground/fully constrained) | WARNING |
| D2-06 | Không link gãy | Mọi referenced document resolve được (file con không thiếu) | FAIL |
| D2-07 | Hệ tọa độ đúng quy ước | Sản phẩm nổi: X dọc thân (gốc FP/AP), Y ngang, Z đứng từ baseline; origin không lệch tùy tiện | WARNING |
| D2-08 | Cây feature sạch | Không feature lỗi/suppressed sót (feature đỏ trong tree) | WARNING |

## 5. LỚP D3 — BẢN VẼ 2D

| Mã | Rule | Điều kiện | Mức |
|---|---|---|---|
| D3-01 | Khung tên đầy đủ | Mã, tên, vật liệu, tỷ lệ, khổ giấy, người vẽ/kiểm/duyệt, ngày | FAIL |
| D3-02 | Vật liệu 2D = 3D | Chuỗi vật liệu trên khung tên khớp Material của model (bỏ dấu, chuẩn hóa) | FAIL |
| D3-03 | Không dimension dangling | Số dimension mất tham chiếu (Inventor tô nâu / SW dangling) = 0 — dấu hiệu bản vẽ chưa cập nhật theo model | FAIL |
| D3-04 | Đủ kích thước theo loại | Tối thiểu: 3 kích thước bao + vị trí mọi lỗ/cắt + kích thước theo checklist D4 của loại chi tiết | WARNING |
| D3-05 | Dung sai chung khai báo | Khung tên có dung sai chung (ISO 2768-mK / TCVN 2244) — bắt buộc với MC | FAIL (MC) / WARNING (khác) |
| D3-06 | Chữ không mojibake | Text decode được (DWG legacy font TCVN3: chạy bảng decode trước khi kết luận; không đọc nổi → FAIL trả lại) | WARNING |
| D3-07 | Ký hiệu hàn hiện diện | Weldment (WA/WS): số weld symbol > 0 và có kích thước chân mối hàn | FAIL |
| D3-08 | Revision 2D = 3D | Revision bản vẽ khớp revision model; bảng revision có dòng mô tả thay đổi | FAIL |

## 6. LỚP D4 — CHECKLIST THEO LOẠI CHI TIẾT WORKSHOP X

### WA — Kết cấu hàn NHÔM (xuồng 4–10 m, 5083/5086/6061)

| Mã | Rule | Mức |
|---|---|---|
| WA-01 | Mác nhôm thuộc danh mục hàn kết cấu (5083-H116/H321, 5086, 6061-T6); 6xxx ở vùng hàn chịu lực chính → WARNING (giảm bền vùng HAZ ~40%) | FAIL |
| WA-02 | WPS tham chiếu khai trong iProperty `WX_WPS_Ref` (vd WPS-AL-01 TIG / WPS-AL-02 MIG theo AWS D1.2/ISO 15614-2) | FAIL |
| WA-03 | **Filler khai và TƯƠNG THÍCH**: 5083/5086 → ER5356/ER5183; **CẤM ER4043 với mác 5xxx** (nứt nóng + giảm bền — lỗi kinh điển đã ghi trong giáo trình hàn Bậc 0–5); 6061 → 4043 hoặc 5356 tùy yêu cầu anod hóa | FAIL |
| WA-04 | Chiều dày nhỏ nhất tại mối hàn kết cấu ≥ 3 mm với MIG (< 3 mm phải chỉ định TIG + bậc thợ ≥ 3) | WARNING |
| WA-05 | Ký hiệu hàn đủ: loại mối (giáp/góc), chân mối hàn a, chiều dài–bước với hàn ngắt quãng | FAIL |
| WA-06 | Khe hở lắp ghép hàn trong model 0,5–2 mm (đo gap mặt đối mặt tại mối hàn) | WARNING |
| WA-07 | Trình tự hàn/đối xứng ghi chú với kết cấu dài > 2 m (chống biến dạng nhiệt) | WARNING |
| WA-08 | Xử lý bề mặt khai (anod hóa/sơn epoxy hệ biển); vùng tiếp xúc thép — cách ly galvanic ghi chú | WARNING |

### WS — Kết cấu hàn THÉP (BM-01, pontoon, giá đỡ)

| Mã | Rule | Mức |
|---|---|---|
| WS-01 | Mác thép thuộc danh mục (EH32, CT3, SS400, Q235…); môi trường biển mà dùng thép thường không phủ → WARNING | FAIL |
| WS-02 | WPS/vật liệu hàn tương thích nhóm thép (que 7016/7018 hay dây theo WPS-ST-xx) | FAIL |
| WS-03 | Yêu cầu NDT khai trên bản vẽ (VT 100%; PT/UT % cho mối chịu lực chính theo ISO 3834-2) | WARNING |
| WS-04 | Sơn phủ/mạ kẽm khai đầy đủ hệ (số lớp, chiều dày μm) cho môi trường biển | WARNING |
| WS-05 | Thép hình dùng quy cách tồn kho chuẩn (L40×40×4, L30×30×3, hộp 30×60×1,8…) — quy cách lạ phải ghi chú nguồn | WARNING |

### MC — Chi tiết GIA CÔNG (trục, bích, chi tiết lắp RCWS/LARS)

| Mã | Rule | Mức |
|---|---|---|
| MC-01 | Kích thước lắp ghép có dung sai fit (H7/g6, H7/k6…) cho mọi lỗ–trục lắp | FAIL |
| MC-02 | Nhám bề mặt Ra khai cho mặt làm việc/mặt lắp | WARNING |
| MC-03 | GD&T (vuông góc/đồng tâm/phẳng) cho mặt chuẩn khi chuỗi lắp yêu cầu | WARNING |
| MC-04 | Manufacturability: góc trong có R ≥ bán kính dao chuẩn; lỗ sâu ≤ 5×D; rãnh hẹp hơn dao chuẩn → cảnh báo | WARNING |
| MC-05 | Ren tiêu chuẩn (M-series/UNC khai rõ), chiều sâu ren + lỗ mồi đúng bảng | FAIL |
| MC-06 | Vát mép/phá cạnh ghi chú chung nếu không ghi riêng | INFO |

### SM — Chi tiết TẤM / cắt CNC (mã, bích, nẹp tấm)

| Mã | Rule | Mức |
|---|---|---|
| SM-01 | Chiều dày = tấm tiêu chuẩn tồn kho (3/4/5/6/8/10/12 mm); phi tiêu chuẩn phải ghi chú nguồn phôi | FAIL |
| SM-02 | Chi tiết CÓ UỐN phải mô hình dạng Sheet Metal (unfold được) — solid thường có bend thì không xuất flat pattern DXF được (bằng chứng: DXF=0 trên Tong lap vì part mô hình dạng thường) | FAIL |
| SM-03 | Bán kính uốn ≥ min theo mác+chiều dày (nhôm 5083: R ≥ 2–3t; thép: R ≥ 1–1,5t) | FAIL |
| SM-04 | Lỗ cách mép ≥ 2t; lỗ cách đường uốn ≥ 2t + R | WARNING |
| SM-05 | Chi tiết cắt CNC: biên dạng kín trong bản vẽ/DXF, không hở polyline | FAIL |

### CP — Chi tiết COMPOSITE (thân phao, vỏ bọc — gia công ngoài/đắp khuôn)

| Mã | Rule | Mức |
|---|---|---|
| CP-01 | Vật liệu khai theo hệ lớp: loại nhựa (polyester/vinylester/epoxy) + loại sợi (mat/roving) + số lớp hoặc chiều dày thành (mm) — trong iProperties/UserText, KHÔNG chấp nhận "Generic"/"Composite" trần | FAIL |
| CP-02 | **Khối lượng riêng THIẾT KẾ khai tường minh** (`WX_Density_gcm3`, vd 1,60–1,80) — composite không có ρ chuẩn đơn trị; thiếu nó thì tầng trích xuất không kiểm được mass = V×ρ (bằng chứng: Thân phao BM-01 lệch 25 kg ↔ 42,5 kg giữa Generic 1,0 và composite đoán 1,7) | FAIL |
| CP-03 | BOM Structure = Purchased/gia công ngoài + tham chiếu bản vẽ biên dạng khuôn; khuôn (nếu vẽ) = Reference, không vào BOM sản phẩm | FAIL |
| CP-04 | Ruột phao: khai lõi (rỗng/xốp PU/foam kín) — phao rỗng phải có ghi chú thử kín; xốp nổi khai khối lượng riêng xốp (an toàn còn nổi khi thủng vỏ) | WARNING |
| CP-05 | Liên kết với kim loại: bulông xuyên composite phải có ống lót/đệm bản rộng (chống dập vỡ cục bộ), KHÔNG hàn/khoan tự do vào vỏ composite ngoài vị trí thiết kế | FAIL |
| CP-06 | Dung sai chế tạo khuôn/lắp lỏng hơn kim loại: kích thước lắp với khung thép phải có khe bù ±3–5 mm hoặc lỗ ô-van | WARNING |

### HU — Vỏ / HULL (Rhino, mặt cong đôi)

| Mã | Rule | Mức |
|---|---|---|
| HU-01 | Thân vỏ là solid/polysurface KÍN: `Join` + naked edges = 0 (`ShowEdges`) | FAIL |
| HU-02 | Đơn vị mm + model absolute tolerance ≤ 0,01 mm trước khi export STEP | FAIL |
| HU-03 | Layer theo quy ước (VO_NGOAI / BOONG / MOONPOOL / DUONG_KC…) | WARNING |
| HU-04 | UserText bắt buộc trên surface chính: `material`, `plate_mm` (Rhino không có vật liệu native — đây là quy ước thay thế, bắt buộc) | FAIL |
| HU-05 | Hệ tọa độ hàng hải: X dọc (gốc FP/AP thống nhất), Y ngang, Z từ baseline | FAIL |
| HU-06 | Export đúng chuẩn trao đổi: STEP AP214, chỉ vùng cần cho outfitting (theo WX-QT-CAD-IO-01) | WARNING |

### AS — ASSEMBLY (cụm lắp)

| Mã | Rule | Mức |
|---|---|---|
| AS-01 | Interference = 0 (trừ khai báo ren/ép/hàn) — chi tiết hóa của D2-04 ở mức nghiệm thu cụm | FAIL |
| AS-02 | BOM structure đúng vai: chi tiết mua = Purchased; skeleton/mẫu = Reference; cụm hàn không tách rời = Inseparable | FAIL |
| AS-03 | Mọi part con đã Released (không lắp bản FAIL/đang WIP vào cụm Released) | FAIL |
| AS-04 | Mass toàn cây đã update (không part nào mass cache rỗng) | WARNING |
| AS-05 | Cấu trúc cụm khớp cây mã hồ sơ (Dự án→Cụm→Chi tiết) | WARNING |

## 7. LỚP D5 — PHÂN LOẠI MẬT (Gate 3 bảo mật)

| Mã | Rule | Mức |
|---|---|---|
| SEC-01 | iProperty `WX_Classification` có, ∈ {THUONG, NOIBO, MAT} | FAIL |
| SEC-02 | Part thuộc cụm nhạy cảm (mã cụm RCWS/AIRPAD/LARS trong Part Number) bắt buộc `MAT` | FAIL |
| SEC-03 | File `MAT` phải nằm trong cây thư mục vùng air-gap quy định; xuất hiện ngoài vùng → báo động, không chỉ FAIL | FAIL |
| SEC-04 | File `MAT` không đi qua pipeline cloud — chỉ model local (LocalAI) như phân vùng đã dựng | FAIL |

## 8. GATES

- **Gate 1 (tự động)**: bất kỳ FAIL nào → không cấp trạng thái "Released", không vào
  pipeline trích xuất. Kết quả ghi `drawing_report.json` (= WX-QT-DRAWING-F01).
- **Gate 2 (người có thẩm quyền)**: kỹ sư trưởng duyệt những gì máy không đánh giá
  được — ý đồ thiết kế, tính chế tạo được, phù hợp WPS hiện có. **Chỉ xem bản đã PASS
  Gate 1** → thời gian duyệt dồn vào cái máy không làm được. Ký WX-QT-DRAWING-F02.
- **Gate 3 (phân loại)**: bản vẽ `MAT` → nhánh air-gap; quyết định trước khi file đi
  bất kỳ đâu.

## 9. LỘ TRÌNH TRIỂN KHAI (theo 2 lưu ý "không tự bắn vào chân")

**Khởi điểm — chỉ bật (đúng nguyên tắc gate mỏng):**
1. **Guides trước**: template .ipt/.iam có sẵn iProperties bắt buộc (`WX_PartType`,
   `WX_Classification`, `WX_WPS_Ref`, Material từ thư viện) + quy ước mã + thư viện
   vật liệu khóa cứng. Giải quyết ~70% lỗi không tốn công kiểm.
2. **Sensor D1 (toàn bộ) + D2-01/03/06 + D3-03**: chạy được NGAY bằng hạ tầng hiện có —
   D1 chính là mở rộng `inventor_apprentice_extract.py` (đã đọc được toàn bộ iProperties
   trên Tong lap.iam hôm nay); self-check 1-click kiểu `self_check.bat`.
3. **1 gate người** cho trạng thái Released.

**Thêm dần khi có bằng chứng lỗi lọt**: D2-04 interference (cần Inventor API sống),
D3-04/07 (đếm dimension/weld symbol qua ezdxf + iLogic), D4 đầy đủ theo loại.
Sửa đổi lặt vặt (WIP chưa Released) KHÔNG qua gate — chỉ chặn tại điểm Released.

**Sensor phải rẻ**: kỹ sư tự chạy self-check trước khi nộp — báo cáo là công cụ giúp
họ nộp một lần đạt, không phải công cụ bắt lỗi. FAIL ở self-check không lưu vết;
FAIL ở gate chính thức mới ghi hồ sơ.

## 10. TRÁCH NHIỆM, BIỂU MẪU, HIỆU CHỈNH

| Vai trò | Trách nhiệm |
|---|---|
| Kỹ sư thiết kế | Dùng template, tự self-check trước khi nộp |
| Người viết/duy trì script | D-rules theo tài liệu này; golden set bản vẽ mẫu (bản vẽ đúng chuẩn + bản vẽ cài lỗi chủ đích) trước phát hành |
| Kỹ sư trưởng | Gate 2; phê duyệt ngưỡng; xử lý FAIL tranh chấp |
| Quản trị hệ thống | Phân vùng MAT; lưu drawing_report; version script |

Biểu mẫu: **WX-QT-DRAWING-F01** (báo cáo thẩm định máy), **F02** (phiếu ký duyệt
Released), **F03** (đăng ký template/thư viện vật liệu).

Hiệu chỉnh: rà ngưỡng hằng quý theo tỷ lệ FAIL giả; mỗi lỗi lọt → thêm rule hoặc thêm
bản-vẽ-cài-lỗi vào golden set bản vẽ. **Khi AI bắt đầu sinh bản vẽ: toàn bộ D-rules áp
nguyên vẹn cho đầu ra AI — cùng sensors, cùng gates, chỉ khác nguồn.**

---

## PHỤ LỤC B — HỒ SƠ LỚP SẢN PHẨM "BM" — BIA MỤC TIÊU NỔI (mẫu chuẩn: Tong lap.iam / BM-01)

### B.1. Nhận dạng lớp sản phẩm

Kết cấu nổi làm việc trên biển, không người: **khung dầm thép hàn + phao composite +
gỗ đệm**, chịu kéo dắt/neo, chịu va sóng, và **bị bắn chủ đích** (bia). Vật liệu hỗn
hợp thép–composite–gỗ trong một sản phẩm → rủi ro đặc thù: ăn mòn galvanic, tính nổi,
liên kết dị vật liệu, phần tiêu hao phải thay được.

### B.2. Rule cấp sản phẩm (BM-xx) — chạy THÊM sau D1–D5

| Mã | Rule | Điều kiện / cách kiểm | Mức |
|---|---|---|---|
| BM-01 | Phân loại đủ, đúng bảng B.3 | 100% part có `WX_PartType` khớp bảng phân rã của lớp (thân phao = CP, không được để WS/STD) | FAIL |
| BM-02 | **Cân bằng tính nổi** | Lực nổi phao (Σ **V_chiếm_nước** × 1,025 t/m³) ≥ tổng khối lượng × hệ số dự trữ **≥ 1,5**. ⚠ V_chiếm_nước = thể tích choán nước của VỎ NGOÀI kín, KHÔNG phải thể tích vật liệu trong seed (Thân phao BM-01: vật liệu chỉ 25 L nhưng bao hình 850×3060×305 ≈ 793 L — lệch 32×). Yêu cầu một trong hai: (a) khai iProperty `WX_Displacement_m3` trên part phao, hoặc (b) mô hình kèm solid "vỏ ngoài kín" lớp Reference để trích V choán nước; kiểm nhanh cận trên bằng bbox × Cb (~0,8) | FAIL |
| BM-03 | Điểm cẩu/kéo/neo khai tải | Móc cẩu: WLL ≥ tổng khối lượng × 2 (cẩu nghiêng 2 điểm); móc kéo/neo: lực thiết kế khai trên bản vẽ (theo sức cản kéo dắt + sóng); mối hàn móc thuộc nhóm kiểm NDT WS-03 | FAIL |
| BM-04 | Cách ly galvanic thép–composite–inox | Vị trí bulông inox xuyên thép trần vùng ướt phải có đệm cách ly/sơn phủ kín; ghi chú cách ly trên bản vẽ lắp | WARNING |
| BM-05 | Chống ăn mòn hệ biển | Toàn khung thép: hệ sơn epoxy biển khai đủ (số lớp, μm); ngâm dài ngày → anode hy sinh khai vị trí + khối lượng | FAIL |
| BM-06 | Hộp kín phải kín hoặc thoát nước | Dầm hộp/cột rỗng: HOẶC ghi chú hàn kín + thử kín, HOẶC có lỗ thoát nước Ø≥10 ở điểm thấp — nước đọng trong hộp kín là ổ ăn mòn + tăng khối lượng | WARNING |
| BM-07 | Phao bắt vào khung bằng liên kết tháo được | Bulông inox + đệm theo CP-05; CẤM hàn/khoan hiện trường vào vỏ composite | FAIL |
| BM-08 | Gỗ đệm (hõm gỗ) xử lý | Gỗ ngâm tẩm chống mục khai trên bản vẽ; không kẹp trực tiếp gỗ ướt vào thép trần (lót cách ẩm) | WARNING |
| BM-09 | **Phần tiêu hao thay được** | Chi tiết hứng đạn (cột bia, cánh hứng đạn, khung lưới) liên kết bằng BÍCH BULÔNG với khung nổi, không hàn chết — bia trúng đạn phải thay nhanh tại bến; bản vẽ cụm phải tách "phần nổi tái sử dụng" / "phần tiêu hao" | FAIL |
| BM-10 | Giới hạn vận chuyển/hạ thủy | Tổng khối lượng + kích thước bao ≤ giới hạn xe/cẩu/triền đã khai trong charter dự án; vượt → phải chia module | WARNING |

### B.3. Bảng phân rã chuẩn — áp vào 21 nhóm thật của Tong lap.iam

(21 nhóm từ qtcn-seed STEP + 49 part Apprentice, 2026-07-02. Cột "vật liệu đề xuất"
lấy theo bản vẽ 2D BM-01 và suy đoán pipeline — **bên thiết kế xác nhận rồi gán vào
CAD**, đây chính là phiếu giao việc đóng 49 lỗi D1-02.)

| Nhóm part (thực tế) | WX_PartType | Vật liệu đề xuất | Ghi chú rule |
|---|---|---|---|
| 1-Than phao (×2) | **CP** | Composite sợi thủy tinh, khai ρ thiết kế (CP-02) | BM-02/07, CP-01…06 |
| ISO L40x40x4 (×38), ISO L30x30x3 | WS | Thép góc (CT3/SS400 — theo BV 2D) | WS-05 quy cách tồn kho |
| JIS 100 x 50 x 5 | WS | Thép U (theo BV 2D) | WS-05 |
| Cot bia | WS | Thép ống/hộp | **BM-09: liên kết bích bulông** |
| Nep doc / Nep doc ngan / Nep ngang (×44) | SM | Tấm thép (dày theo BV 2D) | SM-01 |
| Bich chan cot, Bich dam doc/ngang (mặt trên/dưới), Bich dau dam | SM | Tấm thép 8–15 mm | MC-01 nếu có lỗ lắp bulông chuẩn |
| Ma bich dam doc, Ma canh hung dan 1–3, Ma chan cot, Ma tai phao | SM | Tấm thép | SM-04 lỗ cách mép |
| Tai phao (×12) | SM | Tấm thép | BM-07 (điểm bắt phao) |
| Moc cau, Moc buoc neo, Moc tang do | WS | Thép tròn/tấm | **BM-03: khai WLL/lực thiết kế** |
| Thanh do canh hung dan, KT/Mau/Skeleton (11 part) | — | — | **D1-09: BOM Structure = Reference** (khung xương/mẫu, không chế tạo) |
| Hom go (nếu có trong revision sau) | STD | Gỗ ngâm tẩm | BM-08 |

### B.4. Trạng thái hiện tại của mẫu chuẩn (baseline đo ngày 2026-07-02)

Tong lap.iam đối chiếu với đặc tả này: **FAIL D1-02 (49/49), D1-06 (49/49), D1-09
(11 part), D1-10 (100% chưa có WX_PartType), D1-11 (BOM view Disabled)** — chưa kiểm
được D2-04, D3, BM-02/03. File này dùng làm **case số 0 của golden set bản vẽ**: bản
"trước khi sửa" giữ nguyên làm mẫu FAIL; bản sau khi bên thiết kế gán xong theo B.3
trở thành mẫu PASS chuẩn của lớp BM.

---

## PHỤ LỤC A — Khả năng hiện thực hóa bằng hạ tầng KN-Stack hiện có

| Nhóm rule | Công cụ | Trạng thái |
|---|---|---|
| D1-01…D1-11 | Mở rộng `inventor_apprentice_extract.py` (đã đọc iProperties sống trên Tong lap.iam) | làm được NGAY, không cần mở Inventor |
| D2-01/03 | FreeCAD headless (`freecad_extract.py` đã có solid check + bbox) | làm được NGAY qua STEP |
| D2-04/05, D3-03/07, D1-11 enable | Inventor API sống (iLogic rule external — hạ tầng đã chạy) | cần viết rule, ~P1 |
| D3-01/02/04/06, SM-05 | `parse_mech_drawing.py` (ezdxf, TCVN3 decode đã có) | mở rộng từ script hiện có |
| HU-01…HU-06 | rhino3dm (đọc .3dm không cần Rhino) | adapter mới, viết khi có hull Rhino thật |
| SEC-01…04 | Script quét thư mục + iProperty | làm được NGAY |
