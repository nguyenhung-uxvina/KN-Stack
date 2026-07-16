# CAD PIPELINE — Workshop X

> **Một nguồn dữ liệu gốc (CAD) → 5 đầu ra** (quy trình công nghệ · định mức KTKT ·
> dự toán · kế hoạch chất lượng · biên bản nghiệm thu) — có harness 3 tầng kiểm soát.
> Nguyên tắc: không nhập tay lại số liệu ở bất kỳ khâu nào; mọi tầng chỉ tin đầu vào
> đã qua tầng trước (defense in depth).
>
> Phiên bản hiện hành: xem [CHANGELOG.md](CHANGELOG.md) · Việc mở: [ROADMAP.md](ROADMAP.md)
> · **Hướng dẫn thực hiện theo vai trò: [docs/huong-dan/](docs/huong-dan/00-tong-quan.md)**

## 1. Kiến trúc 3 tầng

```
TẦNG 1 — BẢN VẼ ĐẦU VÀO          TẦNG 2 — TRÍCH XUẤT                TẦNG 3 — AI SINH 5 ĐẦU RA
(WX-QT-DRAWING-SENSOR-01)        (WX-QT-EXTRACT-SENSOR-01)          (§7 của EXTRACT spec)
─────────────────────────        ──────────────────────────         ─────────────────────────
Inventor ──┬─ drawing_check.py   adapter → qtcn-seed/v1 JSON        skill qtcn/product-dossier
Rhino ─────┼─ rhino_check.py       ├ bom_xlsx_to_seed (BOM=vàng)      │
2D DWG ────┘  Drawing_Check_Live   ├ freecad_extract  (STEP)          ▼
   │            (iLogic sống)      ├ parse_mech_drawing (DXF 2D)    trace_numbers.py
   ▼                               ├ inventor_apprentice (headless)  (số nào cũng phải
Gate 1: FAIL → không Released      └ merge_qtcn_seeds                 truy về seed)
không vào tầng 2                 validate_qtcn_seed.py                 │
                                 (S1 vật lý·S2 chéo·S3 sử·S4 diff)     ▼
                                 Gate G1/G2/G3 → seed validated     Gate: số mồ côi=FAIL
                                        │
                        vòng phản hồi:  ▼  GIAI ĐOẠN 4
                        record_actuals.py → calibration.json → định mức lần sau
```

Chạy cả tầng 2 bằng MỘT lệnh: `python cad-pipeline/scripts/extract/run_pipeline.py
--dir <_QTCN_export/<asm>> [--release]`. Nhìn toàn cục: `pipeline_dashboard.py --root <dir>`.

## 2. Cấu trúc thư mục

```
cad-pipeline/
├── README.md / CHANGELOG.md / ROADMAP.md   ← bạn đang ở đây
├── WX_Pipeline.bat   ← bấm đúp để mở phần mềm điều khiển (GUI)
├── app/         wx_pipeline_gui.py — GUI Tkinter gom mọi bước thành nút bấm (lớp vỏ,
│                gọi lại script scripts/extract/; xem app/README.md)
├── docs/        3 đặc tả: EXTRACT-SENSOR (S-rules, bản gốc CEO) ·
│                DRAWING-SENSOR (D-rules + loại chi tiết + lớp SP BM) · CAD-IO (STEP/read-only)
│   └── huong-dan/   HD-00…07 — SOP theo vai trò (thiết kế · KS · QC · xưởng · CEO):
│                    lệnh gõ gì, kết quả đọc thế nào, bảng tra sự cố
├── schemas/     qtcn-seed.schema.json (giao diện chung) · materials.json (MỘT nguồn
│                danh mục vật liệu — sửa Ở ĐÂY, không sửa trong code) · qtcn-actuals.schema.json
├── scripts/
│   ├── extract/   toàn bộ adapter + sensor + tiện ích (bảng mục 3)
│   ├── inventor/  2 rule iLogic (export gói QTCN · live-check) — add làm External Rule
│   └── hooks/     pre-commit (Gate G3 theo commit — cài: xem đầu file)
└── golden/      bộ đáp án chuẩn: fixtures/ (seed cài lỗi) · step/ (4 case giải tích)
                 · rhino/ (2 fixture .3dm) — quy tắc: lỗi lọt lưới 1 lần → thêm case vĩnh viễn
```

Liên quan nhưng nằm ngoài (thuộc domain khác): `scripts/helix/qtcn_to_json.py` (QTCN→JSON,
tầng 5-đầu-ra), `scripts/mcp/` (FreeCAD MCP — công cụ xem tương tác, không phải đường
sản xuất), `scripts/_codify_ledger.md` (sổ codify chung toàn repo — mọi thay đổi pipeline
đều có dòng ở đó).

## 3. Thành phần & trạng thái chứng minh

| File (scripts/extract/) | Vai trò | Trạng thái |
|---|---|---|
| run_pipeline.py | MỘT LỆNH cả chuỗi, dừng đúng gate | field-tested (Tong lap, 2 chiều) |
| validate_qtcn_seed.py | Sensor S1–S4 + Gate G1/G3 + schema check | field-tested; bắt 3 bug thật |
| drawing_check.py | Tầng bản vẽ D1+SEC (Apprentice) + giao-viec.csv | field-tested (49 part) |
| rhino_check.py | Tầng bản vẽ HU-rules (.3dm) + material-map | fixture-tested (trong battery) |
| bom_xlsx_to_seed.py | BOM Inventor → seed (nguồn VÀNG mass/QTY) | field-verified |
| freecad_extract.py | STEP → seed (hình học thật) | field-verified (279 solid) |
| parse_mech_drawing.py / parse_document.py | DXF/PDF/DOCX 2D → JSON | field-verified (VTI, BM-01, X-UUV) |
| inventor_apprentice_extract.py | .ipt/.iam headless (iProperties) | chạy sống; nhánh mass chờ G3 |
| merge_qtcn_seeds.py | Gộp 2 nguồn (gate cưỡng chế require_validated) | field-verified |
| weld_length.py | Chiều dài hàn v0.2 + interference + trùng hình học | selftest ĐẠT; số hàn CHƯA qua G3 |
| trace_numbers.py | Tầng 3: số AI sinh phải truy về seed | test bắt 3/3 số bịa |
| record_actuals.py | Giai đoạn 4: actuals → calibration.json | test số kiểm tay khớp |
| run_battery.py | Battery hồi quy (gọi bởi pre-commit) | 8/8 |
| pipeline_dashboard.py | 1 bảng trạng thái + blocker list | field-tested |
| self_check.bat | Kéo-thả seed tự kiểm (G1 sơ bộ) | tested |

## 4. Quy trình vận hành chuẩn (mỗi sản phẩm)

> Bản chi tiết từng bước theo vai trò: [docs/huong-dan/00-tong-quan.md](docs/huong-dan/00-tong-quan.md)

1. **Inventor**: mở .iam → chạy External Rule `Export_QTCN_Package` → `_QTCN_export/<asm>/`
2. `python cad-pipeline/scripts/extract/run_pipeline.py --dir <thư mục đó>` — sửa theo gate báo
   (thường: `giao-viec.csv` → bên thiết kế gán vật liệu/iProperties → chạy lại)
3. Phát hành lô: thêm `--release` (bắt buộc kiểm chéo 2 nguồn)
4. Seed validated → skill `/qtcn` hoặc `/product-dossier` sinh 5 đầu ra →
   `trace_numbers.py` kiểm số trước khi trình duyệt (`/aigate` check 1)
5. Sản xuất xong nguyên công → `record_actuals.py --add-file …` ; định kỳ `--report`
6. CEO: `pipeline_dashboard.py --root <_QTCN_export>` — 15 giây

## 5. Quy trình NÂNG CẤP pipeline (bắt buộc theo thứ tự)

1. Sửa code/schema/golden → `python cad-pipeline/scripts/extract/run_battery.py --regen`
   phải ĐẠT TOÀN BỘ (pre-commit hook tự chạy khi commit — bỏ qua có chủ đích: `--no-verify`)
2. Lỗi lọt lưới phát hiện ở sản xuất → viết case golden TRƯỚC, vá sau (case ở lại vĩnh viễn)
3. Đổi hành vi extractor → nâng `EXTRACTOR_VERSION`/`VERSION` trong file + dòng mới
   trong `scripts/_codify_ledger.md` + mục trong [CHANGELOG.md](CHANGELOG.md)
4. Phát hành: tag `cad-pipeline-vX.Y` — `extractor_version` trong seed truy về tag này
5. Đổi danh mục vật liệu: sửa `schemas/materials.json` (một chỗ duy nhất);
   đổi giao diện seed: nâng version trong `schemas/qtcn-seed.schema.json` (root khóa cứng)

## 6. Bài học field đã trả giá (đọc trước khi sửa code)

- Đơn vị database Inventor là **cm** (mass kg); ProgID Apprentice thật = `Inventor.ApprenticeServer`
- iLogic: KHÔNG `Imports System.IO` (đụng `Inventor.Path/File`), KHÔNG Sub lồng trong Main,
  tra BOM view theo **ViewType enum** chứ không theo tên
- freecadcmd **nuốt stdout khi có args** sau tên script → mọi tham số qua env var;
  `Part.export` làm MẤT nhãn part trong STEP → dùng `Import.export`
- Nhóm `mass_varies`: est/volume/bbox phải cùng MỘT instance (bug 794% do lệch instance)
- rhino3dm KHÔNG tính mass properties — hình học Rhino đi đường STEP AP214
- Số bịa của AI hay trùng ngẫu nhiên giá trị thật → trace phải khớp ĐÚNG THỨ NGUYÊN
