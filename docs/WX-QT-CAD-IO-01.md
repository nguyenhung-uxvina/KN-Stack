# WX-QT-CAD-IO-01 — Quy ước trao đổi hình học CAD & kiến trúc trích xuất read-only

> Tài liệu tham chiếu cho Giai đoạn 1–2 của pipeline "1 nguồn dữ liệu gốc → 5 đầu ra".
> Bổ trợ cho WX-QT-EXTRACT-SENSOR-01 (harness tầng trích xuất).
> Phiên bản: 1.0 | Trạng thái: Dự thảo | 2026-07

## PHẦN I — Trao đổi hình học Rhino → SolidWorks (hull → outfitting)

### 1. Quyết định định dạng: STEP, không phải IGES

STEP **AP214** giữ topology dạng solid/BREP liền mạch; IGES là định dạng surface-based
cũ, khi import vào SolidWorks thường sinh hàng trăm patch rời rạc, dễ hở khe (gap) ở
mép cong đôi của vỏ tàu — hình học khó nhất trong bộ. Chỉ dùng IGES nếu phần mềm
downstream bắt buộc (hiếm). AP214 còn giữ được layer/color từ Rhino — hữu ích để tách
lớp vỏ ngoài, biên moonpool, đường tham chiếu kết cấu.

### 2. Bước 1 — Chuẩn hóa trước khi export (quan trọng nhất, hay bị bỏ qua)

- **Đơn vị**: khóa cả hai file cùng **mm** — không để Rhino ở m còn SolidWorks ở mm.
- **Tolerance**: siết Rhino model tolerance xuống ~**0.01 mm** (`Options > Units`)
  trước export — tolerance lỏng là nguyên nhân số 1 khiến SolidWorks không "knit"
  được thành solid kín khi import.
- **Kiểm tra mặt kín**: chạy `Join` + `CheckNewObjects` trong Rhino, xác nhận thân vỏ
  là **1 solid kín** trước khi export — nếu không, SolidWorks nhận về surface rời,
  không dùng làm reference đặc được.
- **Hệ tọa độ chung (bắt buộc với thiết kế tàu)**: thống nhất gốc tọa độ và chiều trục
  trước khi bắt đầu — chuẩn hàng hải: X dọc tàu (gốc tại FP hoặc AP), Y ngang, Z thẳng
  đứng từ baseline. Không chốt trước → mỗi lần import phải canh chỉnh tay → sai số
  tích lũy.

### 3. Bước 2 — Export từ Rhino

`File > Export Selected` → STEP → AP214 → **chỉ export phần hình học cần thiết cho
outfitting** (vùng lắp RCWS, vùng moonpool, mặt boong liên quan) thay vì toàn bộ vỏ —
file SolidWorks nhẹ và dễ quản lý.

### 4. Bước 3 — Import vào SolidWorks

`File > Open` STEP → bật `Tools > Import Diagnostics` ngay sau import để SolidWorks tự
phát hiện và heal mặt hở/lỗi. Nếu còn lỗi: **quay lại Rhino sửa**, không cố sửa trong
SolidWorks (sửa hình học ngoại lai trong SW rất khó).

### 5. Bước 4 — Kiến trúc assembly: top-down, hull là reference cố định

- Đưa STEP hull vào assembly như **component cố định (Fixed)** — chấp nhận là "dumb
  solid", không cố biến thành feature parametric.
- Thiết kế outfitting (mount RCWS, giá đỡ LARS) **in-context**: `Insert > Reference
  Geometry` lấy offset surface, intersection curve từ hull làm chuẩn định vị — không
  sửa trực tiếp hình học hull.
- Hull lớn → dùng **Lightweight/SpeedPak** cho component hull.

### 6. Bước 5 — Quản lý revision (điểm dễ vỡ nhất của quy trình 2 phần mềm)

STEP là hình học "câm" — không có associativity. Khi bên Rhino sửa hull (rất hay xảy
ra ở giai đoạn tối ưu hydrodynamic):

1. Rhino xuất STEP mới, tên có version (`Hull_v03.step`)
2. SolidWorks dùng **`Replace Component`** (không mở file mới rời) để giữ mate/reference
3. Chạy lại `Import Diagnostics`, kiểm tra bằng mắt mount RCWS/LARS còn khớp bề mặt
   không — thay đổi hull có thể làm lệch offset surface đã dùng làm chuẩn
4. **Ghi log thay đổi hình học ảnh hưởng outfitting** — tránh kỹ sư cơ khí không biết
   hull đã đổi

### 7. Bẫy thường gặp

- Xuất cả hull nguyên khối cho mọi chỉnh nhỏ → file nặng, re-import không cần thiết
- Không khóa hệ tọa độ chung từ đầu → align tay, sai số cộng dồn qua nhiều vòng lặp
- Cố sửa hình học import trong SolidWorks thay vì sửa gốc ở Rhino → **2 nguồn sự thật
  lệch nhau**

## PHẦN II — Kiến trúc trích xuất: script một chiều, không kết nối sống

Nếu chỉ cần **đọc dữ liệu** (không sửa, không tạo feature), tách hẳn 2 việc:
**trích xuất** (local, không cần AI) và **phân tích/soạn tài liệu** (AI, dùng dữ liệu
đã trích). Không dùng MCP server cộng đồng có quyền ghi/chạy macro.

### 1. API read-only theo mục đích (SolidWorks)

| Mục đích | API cần dùng | Dữ liệu lấy được |
|---|---|---|
| Định mức KTKT | `GetMassProperties3`, `GetVolume`, `SurfaceArea` | khối lượng, thể tích, diện tích bề mặt (→ định mức vật tư, thời gian sơn/hàn) |
| Quy trình công nghệ | `FeatureManager` traversal | trình tự feature (cắt, uốn, hàn, khoan…) → gợi ý trình tự công nghệ |
| Kiểm tra/QC | `DimXpertManager`, `IDisplayDimension` | kích thước, dung sai (GD&T nếu có DimXpert) → checklist kiểm tra |
| Quản lý/BOM | `GetCustomPropertyNames`/`Value`, BOM table | mã hiệu, revision, vật liệu, cấu trúc lắp ráp |
| Đối chiếu bản vẽ | Export PDF/STEP kèm properties | bản ghi tham chiếu không sửa được |

(Tương đương Inventor: `MassProperties`, `BOM` object, `iProperties`,
`PartComponentDefinition.Features`; headless qua Apprentice Server — xem
WX-QT-EXTRACT-SENSOR-01 Phụ lục A.)

### 2. Vì sao script một chiều thay vì MCP sống

- Script chạy độc lập, **không cần CAD + AI client mở cùng lúc** → chạy hoàn toàn
  trong vùng mật/air-gap, xuất JSON/Excel được kỹ sư rà soát trước khi đưa ra ngoài.
- **Không có đường nào để AI ghi ngược vào file gốc** — loại bỏ rủi ro macro-execution
  của các MCP server cộng đồng (execute VBA, COM ghi).
- Dữ liệu đưa cho Claude/Codex chỉ là **số liệu đã trích** (khối lượng, kích thước,
  BOM…), không phải hình học đầy đủ hay file CAD gốc — giảm mức nhạy cảm khi gửi qua
  model cloud.

### 3. Luồng làm việc

1. Script chạy batch trên thư mục bản vẽ → xuất `qtcn-seed.json` / `.xlsx`
2. Kỹ sư review, **lọc trường không cần đưa ra ngoài** (chi tiết RCWS/LARS/AIRPAD)
3. Seed đã qua validator (Gate G1, WX-QT-EXTRACT-SENSOR-01) + đã lọc → đưa vào Claude
   Code/Claude.ai → dựng quy trình công nghệ, định mức KTKT, checklist QC
