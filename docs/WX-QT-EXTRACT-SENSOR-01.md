# WX-QT-EXTRACT-SENSOR-01 — ĐẶC TẢ KỸ THUẬT BỘ SENSOR KIỂM SOÁT CHẤT LƯỢNG TRÍCH XUẤT DỮ LIỆU TỪ BẢN VẼ CAD

> Áp dụng khung Harness Engineering (Guides – Sensors – Gates)
> Mã tài liệu: WX-QT-EXTRACT-SENSOR-01 | Phiên bản: 1.0 | Trạng thái: Dự thảo
> Ngày ban hành: ……/2026
> Hiện thực tham chiếu trong KN-Stack: `scripts/extract/validate_qtcn_seed.py` (xem Phụ lục A)

## 1. MỤC ĐÍCH, PHẠM VI VÀ NGUYÊN TẮC

### 1.1. Mục đích

Tài liệu này đặc tả bộ quy tắc kiểm soát chất lượng (sensor) áp dụng cho khâu trích
xuất dữ liệu tự động từ bản vẽ/mô hình CAD (SolidWorks, Inventor, Rhino) phục vụ xây
dựng quy trình công nghệ, định mức kinh tế kỹ thuật, dự toán, kế hoạch chất lượng và
hồ sơ kiểm tra nghiệm thu. Mục tiêu là bảo đảm mọi số liệu đưa vào các đầu ra nói trên
đều được **kiểm chứng bằng máy trước, kiểm mẫu bằng người sau, và truy vết được về
nguồn gốc**.

### 1.2. Phạm vi

Áp dụng cho toàn bộ dữ liệu do script trích xuất (extractor) sinh ra từ file CAD đã
qua kiểm soát chất lượng bản vẽ đầu vào (tham chiếu quy trình kiểm soát bản vẽ đầu vào
của Workshop X). Không áp dụng cho dữ liệu nhập tay.

### 1.3. Nguyên tắc thiết kế (theo khung Harness Engineering)

- **Guides**: thiết kế schema, đơn vị, danh mục khóa cứng để dữ liệu sai không thể tồn
  tại về mặt cấu trúc.
- **Sensors**: bốn lớp kiểm tra tự động, xếp từ rẻ đến đắt, ưu tiên các bất biến vật lý
  không cần đáp án ngoài.
- **Gates**: ba điểm chặn — gate tự động, gate kiểm mẫu con người, gate golden set khi
  thay đổi phiên bản script.

Dữ liệu chỉ được đóng dấu **"validated"** và đi tiếp vào pipeline 5 đầu ra khi vượt qua
toàn bộ gate bắt buộc.

## 2. GUIDES — YÊU CẦU CẤU TRÚC DỮ LIỆU ĐẦU RA

### 2.1. Schema JSON chuẩn (bắt buộc)

Mọi file dữ liệu trích xuất phải tuân thủ schema khai báo bằng JSON Schema
(draft 2020-12). Các yêu cầu tối thiểu:

- **Tên trường mang đơn vị tường minh**: `mass_kg`, `volume_m3`, `surface_area_m2`,
  `weld_length_mm`, `bbox_x_mm`, `bbox_y_mm`, `bbox_z_mm`.
- Trường số khai báo kiểu number, giá trị tối thiểu > 0 đối với khối lượng, thể tích,
  diện tích.
- Trường vật liệu (`material_grade`) là **enum lấy từ danh mục vật liệu được duyệt**
  của Workshop X (5083, 5086, 6061-T6, 6082-T6…); giá trị ngoài danh mục làm file
  không hợp lệ.
- Trường bắt buộc về truy vết: `part_code`, `revision`, `source_file_hash` (SHA-256
  của file CAD nguồn), `extractor_version`, `extract_timestamp` (ISO 8601),
  `operator_id`.
- Không cho phép trường tự do (`additionalProperties: false`) ở cấp gốc — muốn thêm
  trường phải nâng phiên bản schema.

### 2.2. Yêu cầu đối với script trích xuất

- Chỉ sử dụng **API đọc (read-only)**; nghiêm cấm mọi lời gọi API ghi/sửa mô hình.
- Script được quản lý phiên bản (Git), mỗi bản phát hành gắn tag; `extractor_version`
  trong JSON phải khớp tag.
- Script phải **deterministic**: cùng file nguồn, cùng phiên bản script, hai lần chạy
  phải cho kết quả trùng khớp tuyệt đối (trừ timestamp).

## 3. SENSORS — BỐN LỚP KIỂM TRA TỰ ĐỘNG

Mỗi rule có mã hiệu, mức cảnh báo (**FAIL** chặn tuyệt đối / **WARNING** yêu cầu người
xem / **INFO** ghi log), công thức và ngưỡng dung sai. Ngưỡng ghi trong tài liệu này là
giá trị khởi điểm; được hiệu chỉnh theo dữ liệu thực tế sau mỗi quý và ghi vào phụ lục
ngưỡng.

### 3.1. Lớp 1 — Bất biến vật lý (chạy 100% file, chi phí thấp nhất)

| Mã | Rule | Công thức / Điều kiện | Ngưỡng | Mức |
|---|---|---|---|---|
| S1-01 | Khối lượng khớp thể tích × khối lượng riêng | `\|mass_kg − volume_m3 × ρ(material)\| / mass_kg` | ≤ 2% | FAIL |
| S1-02 | Khối lượng riêng tra theo mác vật liệu | ρ lấy từ bảng danh mục (5083: 2660; 6061: 2700 kg/m³…) | — | — |
| S1-03 | Kích thước bao chi tiết nằm trong bao assembly | `bbox(part) ⊆ bbox(assembly) + 1 mm` | ≤ 1 mm vượt | FAIL |
| S1-04 | Tổng khối lượng chi tiết ≈ khối lượng assembly | `\|Σ mass(parts) − mass(asm)\| / mass(asm)` | ≤ 3% | FAIL |
| S1-05 | Diện tích bề mặt ≥ cận dưới hình học | `surface_area_m2 ≥ (36π·V²)^{1/3}` — mặt cầu là bề mặt nhỏ nhất cho thể tích cho trước ⁽*⁾ | vi phạm | FAIL |
| S1-06 | Thể tích ≤ thể tích hình bao | `volume_m3 ≤ bbox_x × bbox_y × bbox_z` | vi phạm | FAIL |
| S1-07 | Giá trị số hữu hạn, dương | không NaN/Inf/âm ở mass, volume, area, chiều dài hàn; qty ≥ 1 | vi phạm | FAIL |
| S1-08 | Đơn vị nhất quán | so mass tính lại từ volume: nếu lệch đúng hệ số 10/1000/10⁶ (±5%) → nghi nhầm đơn vị, báo đích danh hệ số | phát hiện | FAIL |

⁽*⁾ *Hiệu chỉnh so với dự thảo gốc*: công thức gốc "2(ab+bc+ca) của khối tương đương
thể tích" không phải cận dưới đúng (hình cầu có diện tích **nhỏ hơn** hình hộp cùng thể
tích → rule sẽ FAIL oan chi tiết tròn/trơn). Cận dưới đúng cho mọi solid là **bất đẳng
thức đẳng chu**: `A ≥ (36π·V²)^{1/3}`. Hiện thực dùng công thức này (nhân 0,99 chống
sai số tính diện tích lưới).

### 3.2. Lớp 2 — Kiểm tra chéo hai đường độc lập (chi tiết trọng yếu)

Áp dụng cho chi tiết được đánh dấu **trọng yếu**: giá trị vật tư lớn nhất trong dự
toán, chi tiết chịu lực chính, chi tiết thuộc cụm có yêu cầu nghiệm thu cấp cao.

| Mã | Rule | Đường 1 | Đường 2 | Ngưỡng lệch | Mức |
|---|---|---|---|---|---|
| S2-01 | Khối lượng | COM API `GetMassProperties` / BOM Inventor | Đọc STEP bằng thư viện độc lập (OpenCascade/FreeCAD) | ≤ 0,5% ⁽**⁾ | FAIL |
| S2-02 | Thể tích | COM API | OpenCascade/FreeCAD từ STEP | ≤ 0,5% | FAIL |
| S2-03 | Kích thước bao | COM API | OpenCascade/FreeCAD từ STEP | ≤ 0,2 mm | FAIL |
| S2-04 | Số thực thể hàn (weld bead/đường hàn) | Duyệt cây weldment | Đếm từ bản vẽ 2D/bảng weld table | = 0 lệch | WARNING |

⁽**⁾ Ngưỡng 0,5% áp dụng khi hai đường cùng đo **một hình học** (COM vs OCC trên cùng
model). Khi đường 2 phải **giả định khối lượng riêng** (STEP mất nhãn vật liệu,
`density_assumed = true`), hiện thực tự nới lên ngưỡng WARNING 10% và ghi rõ lý do
trong báo cáo — lệch lúc này đo sai số của ρ giả định, không phải lỗi trích.

### 3.3. Lớp 3 — Sanity check theo dữ liệu lịch sử

| Mã | Rule | Điều kiện | Ngưỡng khởi điểm | Mức |
|---|---|---|---|---|
| S3-01 | Khối lượng lệch bất thường so với chi tiết cùng nhóm | so với median nhóm chi tiết cùng loại (theo `part_code` prefix / tên chuẩn hóa) | > ±30% | WARNING |
| S3-02 | Suất hàn bất thường | `weld_length_mm / mass_kg` so với dải lịch sử nhóm kết cấu hàn | ngoài dải P5–P95 | WARNING |
| S3-03 | Tỷ lệ diện tích/khối lượng bất thường (chi tiết tấm) | `surface_area_m2 / mass_kg` so với dải tương ứng chiều dày tấm khai báo | ngoài dải | WARNING |

Ghi chú: lớp 3 chỉ có hiệu lực sau khi tích lũy tối thiểu **20 chi tiết cùng nhóm**;
trước đó các rule ở trạng thái INFO.

### 3.4. Lớp 4 — Kiểm tra tính lặp lại và diff giữa revision

| Mã | Rule | Điều kiện | Mức |
|---|---|---|---|
| S4-01 | Determinism | Chạy lại cùng file + cùng `extractor_version`: mọi trường số trùng tuyệt đối | FAIL |
| S4-02 | Diff khớp phạm vi thay đổi | Revision mới: trường thay đổi phải thuộc nhóm liên quan đến mô tả thay đổi trong ECN/ghi chú revision | WARNING |
| S4-03 | Số thực thể trích được so với cây feature | Số body/weld/hole trích được so với số đếm trực tiếp trong FeatureManager / số dòng BOM nguồn | = 0 lệch, khác → WARNING |

Rule **S4-03 là tuyến phòng thủ chính chống lỗi thiếu sót** (bỏ sót đường hàn, bỏ sót
lỗ khoan) — loại lỗi mà bất biến vật lý lớp 1 không phát hiện được.

## 4. GATES — ĐIỂM CHẶN VÀ THẨM QUYỀN

### 4.1. Gate G1 — Chặn tự động

- Bất kỳ rule mức FAIL nào vi phạm → file JSON **không được cấp trạng thái
  `validated`**; pipeline 5 đầu ra từ chối nhận.
- Kết quả kiểm được ghi thành `validation_report.json` đính kèm file dữ liệu, liệt kê
  từng rule PASS/FAIL/WARNING kèm giá trị đo.

### 4.2. Gate G2 — Kiểm mẫu con người

- Mỗi lô trích xuất: kỹ sư kiểm tra **đo tay tối thiểu 3–5 giá trị** trên bản vẽ, đối
  chiếu JSON.
- Ưu tiên chọn mẫu: (1) mọi chi tiết có WARNING; (2) chi tiết có giá trị vật tư lớn
  nhất trong dự toán; (3) một mẫu ngẫu nhiên.
- Kết quả kiểm mẫu ghi vào biểu mẫu **WX-QT-EXTRACT-F02**, người kiểm ký xác nhận.
  Lệch vượt dung sai → **cả lô quay lại điều tra nguyên nhân**.

### 4.3. Gate G3 — Golden set (bắt buộc khi thay đổi script)

- Duy trì bộ **10–20 file CAD mẫu có đáp án chuẩn** đã đo tay và phê duyệt (golden
  set), lưu kèm hash và bảng đáp án.
- Mọi phiên bản extractor mới phải chạy toàn bộ golden set và **khớp đáp án 100%**
  (trong dung sai từng rule) trước khi được gắn tag phát hành.
- Golden set phải bao gồm chủ đích các **ca hình học khó**: weldment nhiều đoạn, chi
  tiết đối xứng, pattern lỗ, tấm cong đôi, assembly có chi tiết lặp — để lỗi thiếu sót
  lộ ra tại gate này.
- Golden set được **bổ sung mỗi khi phát hiện một lỗi lọt lưới trong sản xuất**: file
  gây lỗi được đưa vào bộ mẫu vĩnh viễn (quy tắc *"lỗi nào đã xảy ra một lần thì không
  được xảy ra lần hai"*).

## 5. CẤU TRÚC GOLDEN SET

| Nhóm mẫu | Số lượng tối thiểu | Mục tiêu kiểm chứng |
|---|---|---|
| Tấm nhôm phẳng có lỗ/pattern | 3 | Khối lượng, diện tích, đếm lỗ, nhầm đơn vị |
| Kết cấu hàn (weldment) nhiều đoạn | 4 | Tổng chiều dài hàn, đếm đường hàn, lỗi thiếu sót |
| Chi tiết cong đôi (trích từ hull) | 3 | Thể tích/diện tích mặt cong, chất lượng STEP hai đường |
| Chi tiết gia công có dung sai/GD&T | 3 | Trích dimension, dung sai, khớp checklist QC |
| Assembly nhỏ (5–15 chi tiết, có chi tiết lặp) | 3 | Tổng khối lượng, BOM, đếm số lượng chi tiết lặp |
| Ca đã từng gây lỗi (bổ sung dần) | không giới hạn | Regression — chống tái diễn |

Mỗi mẫu lưu: file CAD gốc + hash, bảng đáp án chuẩn (đo tay, **hai người xác nhận**),
ngày lập, người phê duyệt. Golden set lưu trong vùng nội bộ, quản lý cấu hình như tài
liệu kiểm soát.

Cấu trúc thư mục (nhánh theo NGUỒN — lỗi adapter là lỗi theo từng nguồn; script
SolidWorks đúng không chứng minh script Inventor đúng):

```
golden/
  inventor/ | step/ | dxf/ | solidworks/ | rhino/
    <case>/
      source/               ← file CAD gốc (hoặc pointer nếu file mật/quá lớn) + hash
      expected-seed.json    ← đáp án đo tay, hai người xác nhận
      notes.md              ← ai đo, ngày, chỗ oái oăm của ca này
```

## 6. TRÁCH NHIỆM VÀ BIỂU MẪU

| Vai trò | Trách nhiệm |
|---|---|
| Người viết/duy trì script | Tuân thủ schema, chạy golden set trước phát hành, ghi changelog |
| Kỹ sư kiểm tra (QC) | Thực hiện gate G2, ký biểu mẫu kiểm mẫu, đề xuất bổ sung golden set |
| Kỹ sư trưởng | Phê duyệt ngưỡng dung sai, phê duyệt đáp án golden set, xử lý lô FAIL |
| Quản trị hệ thống | Quản lý phiên bản script, lưu trữ validation_report, phân vùng dữ liệu mật |

Biểu mẫu kèm theo: **WX-QT-EXTRACT-F01** (báo cáo thẩm định tự động — chính là
`validation_report.json` in ra), **WX-QT-EXTRACT-F02** (biên bản kiểm mẫu con người),
**WX-QT-EXTRACT-F03** (biên bản phê duyệt phát hành phiên bản extractor).

## 7. HIỆU CHỈNH VÀ CẢI TIẾN

- Ngưỡng dung sai được rà soát **hằng quý** dựa trên thống kê tỷ lệ WARNING/FAIL giả
  (false positive) và lỗi lọt lưới.
- Mỗi lỗi lọt lưới phát hiện ở sản xuất phải có phân tích nguyên nhân: thiếu rule,
  ngưỡng sai, hay lỗi ngoài phạm vi — và cập nhật tương ứng vào tài liệu này.
- Khi đưa AI tham gia khâu xử lý dữ liệu (giai đoạn 3 của pipeline), **toàn bộ sensor
  và gate trong tài liệu này áp dụng nguyên vẹn cho đầu ra của AI**.

---

## PHỤ LỤC A — Ánh xạ vào KN-Stack (hiện thực)

### A.1. Ma trận adapter (một schema — nhiều adapter — một bộ sensor)

| Nguồn | Adapter | Trạng thái |
|---|---|---|
| Inventor BOM export (.xlsx/.csv) | `scripts/extract/bom_xlsx_to_seed.py` | field-verified — **nguồn VÀNG** (Mass/QTY/Material Inventor tự tính) |
| Inventor trong app (iLogic) | `scripts/inventor/Export_QTCN_Package.iLogic.vb`, `scripts/extract/inventor_batch_export.iLogic.vb` | viết theo API chuẩn, chưa chạy thật |
| Inventor headless (Apprentice) | `scripts/extract/inventor_apprentice_extract.py` | **skeleton 0.1.0 — chưa qua G3, chưa được dùng sản xuất** |
| STEP/IGES/FCStd | `scripts/extract/freecad_extract.py` | field-verified (BM-01, 279 solid) |
| DXF/DWG 2D | `scripts/extract/parse_mech_drawing.py` | field-verified (VTI, BM-01) |
| Gộp 2 nguồn | `scripts/extract/merge_qtcn_seeds.py` | field-verified |
| SolidWorks COM / Rhino | chưa có | Rhino cần phụ lục quy ước layer + UserText trước (không có vật liệu/BOM native) |

**Bẫy đơn vị Inventor**: API trả theo đơn vị database (length **cm**, volume cm³;
`MassProperties.Mass` trả **kg**) — không phải mm như hiển thị. Adapter quy đổi tường
minh; S1-08 kiểm chéo; golden set nhánh Inventor kiểm chứng quy đổi.

### A.2. Ánh xạ trường schema mục 2.1 → `qtcn-seed/v1`

| Trường trong đặc tả | Trường qtcn-seed/v1 | Quy đổi |
|---|---|---|
| `mass_kg` (part) | `bom[].specs.est_mass_kg` / `total_mass_kg` | — |
| `volume_m3` | `bom[].specs.volume_cm3` | ×10⁻⁶ |
| `surface_area_m2` | `bom[].specs.area_cm2` | ×10⁻⁴ |
| `bbox_x/y/z_mm` | `bom[].specs.bbox_mm.{x,y,z}` | — |
| `material_grade` | `bom[].material` | khớp mờ với danh mục duyệt |
| ρ(material) | `bom[].specs.density_g_cm3` | g/cm³ = ×1000 kg/m³ |
| mass(assembly) | `product.total_mass_kg` | — |
| bbox(assembly) | `product.principal_particulars.envelope_mm` | — |
| `part_code`, `revision` | `bom[].drawing_no`, `product.code` | — |
| `source_file_hash`, `extractor_version`, `extract_timestamp`, `operator_id` | `source.sha256`, `engine`/`*_version`, `source.extracted_at`, `source.operator` | seed cũ chưa có hash/operator → validator báo INFO, adapter mới bắt buộc ghi |

### A.3. Validator — contract cho pipeline

`python scripts/extract/validate_qtcn_seed.py --seed <seed.json> [...]` — chạy
**kiểm cấu trúc theo `schemas/qtcn-seed.schema.json`** (JSON Schema 2020-12,
`additionalProperties: false` cấp gốc — thi hành mục 2.1) rồi S1 + S4-03;
`--cross a.json b.json` chạy S2; `--history history.jsonl` chạy S3;
`--determinism a.json b.json` chạy S4-01; `--diff old.json new.json` chạy S4-02;
`--golden <dir>` chạy Gate G3. Xuất `*.validation.json` (= biểu mẫu F01).

**`--release` (phát hành lô)**: BẮT BUỘC có `--cross` — vì trên seed đơn, S1-01/S1-04
là rule "tự chấm mình" khi cùng một script tính cả hai vế; bất biến chỉ có sức mạnh
thật giữa hai đường độc lập (BOM Inventor × STEP FreeCAD). Thiếu trường truy vết
(sha256/extracted_at/operator) khi release → WARNING thay vì INFO.

**Self-check 1-click cho người trích**: kéo-thả seed JSON vào
`scripts/extract/self_check.bat`.

**Pipeline MỘT LỆNH**: `python scripts/extract/run_pipeline.py --dir <_QTCN_export/<asm>>
[--release]` — tự chạy BOM→seed, STEP→seed, Gate G1 từng seed, kiểm chéo S2, merge,
validate seed cuối; dừng ngay tại gate đầu tiên chặn và báo cách sửa.

**Harness tầng 3 (đầu ra AI — §7)**: `python scripts/extract/trace_numbers.py --doc
<tài-liệu.md> --seed <seed.json>` — mọi số CÓ ĐƠN VỊ trong tài liệu AI sinh phải truy
được về seed (khớp đúng thứ nguyên: kg chỉ khớp trường mass, mm chỉ khớp trường _mm…),
số mồ côi → exit 2 chặn phát hành. Đã nối vào check TRACEABILITY của skill /aigate.

**Chiều dài hàn v0.2**: `FC_FILE=<asm.step> freecadcmd scripts/extract/weld_length.py`
— phân loại từng cặp solid chạm nhau: weld (giao tuyến = ứng viên chân mối hàn, cận
trên) / interference (thể tích giao >1 mm³ = D2-04) / trùng hình học (STEP xuất đúp —
nghi đếm trùng khối lượng). Chưa qua G3 — số hàn chưa dùng cho hồ sơ chính thức.

### A.4. Golden set v0 (đã vận hành)

`golden/step/` có 3 case **giải tích** (đáp án tính tay chính xác tuyệt đối):
plate-4holes / box-tube / cylinder — sinh bằng `golden/make_golden_v0.py`
(freecadcmd), G3 PASS 3/3 ngày 2026-07-02. Ghi nhận: ngay lần chạy đầu, golden set
bắt được lỗi thật — `Part.export` làm mất nhãn chi tiết trong STEP → generator
chuyển sang `Import.export`. Nhánh `inventor/` khởi động khi chạy iLogic trên
assembly thật (3–5 file, 2 người đo tay ký).

| Exit code | Nghĩa |
|---|---|
| 0 | PASS toàn bộ — seed được đóng dấu validated |
| 1 | Có WARNING, không FAIL — đi tiếp, kèm danh sách kiểm mẫu G2 |
| 2 | Có FAIL — Gate G1 chặn, seed không validated |
| 3 | Lỗi sử dụng / thiếu file |
