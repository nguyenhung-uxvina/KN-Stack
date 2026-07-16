# HD-01 — BÊN THIẾT KẾ: CHUẨN BỊ MODEL + EXPORT GÓI QTCN

> Người thực hiện: kỹ sư thiết kế (Inventor hoặc Rhino).
> Mục tiêu: model đạt chuẩn để pipeline trích số TỰ ĐỘNG — model chuẩn 1 lần,
> mọi đầu ra (QTCN/định mức/dự toán/QCP/nghiệm thu) hưởng mãi.
> Rule chi tiết + checklist theo loại chi tiết: `docs/WX-QT-DRAWING-SENSOR-01.md`.

## 1. Checklist model TRƯỚC khi export (Inventor)

Mỗi part chế tạo (không phải mua sẵn):

- [ ] **Part Number** không rỗng, theo quy ước mã của sản phẩm
- [ ] **Vật liệu gán từ thư viện** — KHÔNG để `Generic`. Chuỗi tên phải khớp danh mục
      `cad-pipeline/schemas/materials.json` (ví dụ `Nhôm 5083`, `CT3`, `SUS304`…).
      Cần thêm vật liệu mới → báo KS công nghệ sửa `materials.json` (một chỗ duy nhất),
      KHÔNG tự chế tên.
- [ ] **iProperties bắt buộc** (Custom): `WX_PartType` (WA/WS/MC/SM/CP/HU/AS/STD),
      `WX_Classification` (THUONG/NOIBO/MAT), `WX_WPS_Ref` (nếu có hàn)
- [ ] Part **skeleton / khung KT / mẫu dựng hình**: đặt BOM Structure = **Reference**
      (Inventor sẽ loại khỏi BOM — không đếm vào khối lượng)
- [ ] Assembly: bật **BOM view Parts Only** (Tools → Bill of Materials → tab Parts Only
      → Enable), rồi **Update mass** + Save

> Vì sao nghiêm: mass Inventor tính bằng V×ρ của vật liệu Đà GÁN. Part `Generic`
> (ρ=1,0) cho mass sai hoàn toàn — pipeline sẽ chặn ở gate, việc quay lại đúng bàn này.

## 2. Xử lý `giao-viec.csv` (khi pipeline trả việc về)

KS công nghệ chạy kiểm sẽ gửi file `giao-viec.csv` — mỗi dòng một part chưa đạt kèm
lý do (thiếu vật liệu / thiếu iProperty / PN rỗng). Cách làm:

1. Mở CSV (Excel đọc được, UTF-8 có BOM), lọc theo cột lý do.
2. Sửa từng part theo checklist §1. Với sản phẩm BM: bảng gán vật liệu theo nhóm
   có sẵn ở `docs/WX-QT-DRAWING-SENSOR-01.md` Phụ lục B mục B.3.
3. Update mass + Save toàn bộ → báo lại KS chạy vòng kiểm mới.

## 3. Export gói QTCN (1 nút)

1. Mở file lắp **.iam** trong Inventor.
2. Manage → iLogic → **External Rules → Add** →
   `D:\KN-Stack\cad-pipeline\scripts\inventor\Export_QTCN_Package.iLogic.vb` (add 1 lần,
   về sau chỉ Run — luôn là bản mới nhất).
3. Run → đọc hộp thoại tổng kết. Kết quả vào `_QTCN_export\<tên asm>\`:
   `<asm>_BOM.csv` (nguồn VÀNG mass/QTY) · `<asm>.step` (AP242, hình học) ·
   `dxf\` (flat-pattern tôn) · `pdf\` (bản vẽ trùng tên).
4. Bàn giao cả thư mục cho KS công nghệ (nội bộ — không gửi kênh ngoài nếu có phần MẬT).

**Nếu dán rule bằng tay** (không dùng External Rule): xóa SẠCH nội dung rule cũ trước
khi dán (Ctrl+A → Delete). Dán nối vào code cũ sẽ báo `All other Sub's must be after
Sub Main()`.

## 4. Đường Rhino (vỏ nhôm, HU)

Rhino không có BOM/iProperties — chuẩn thay thế:

- Layer đặt tên theo tiền tố quy ước (`HULL_`, `FRAME_`, `PLATE_`…); mỗi object là solid kín.
- Gắn **UserText** trên object: `material` (khớp materials.json) và `plate_mm` (chiều dày).
- Kiểm trước khi bàn giao: `python cad-pipeline/scripts/extract/rhino_check.py --file <file.3dm>`
  (HD-03 §4) — sinh kèm `<file>.material-map.json` dùng cho bước sau.
- Xuất hình học: **STEP AP214** (File → Export Selected), KHÔNG dùng IGES —
  quy trình 5 bước ở `docs/WX-QT-CAD-IO-01.md`. Mass sẽ do FreeCAD tính từ STEP
  (rhino3dm không tính được mass).
