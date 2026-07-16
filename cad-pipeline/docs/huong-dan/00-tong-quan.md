# HD-00 — TỔNG QUAN: AI ĐỌC GÌ, LÀM GÌ, KHI NÀO

> Bộ hướng dẫn vận hành CAD Pipeline Workshop X. Kiến trúc/lý do thiết kế xem
> [README](../../README.md); đặc tả rule xem `docs/WX-QT-*.md`. Bộ này chỉ trả lời:
> **"tôi ở vai trò X, hôm nay phải làm gì, gõ lệnh gì, kết quả đọc thế nào".**

## 1. Dòng chảy một sản phẩm (nhìn 30 giây)

```
BÊN THIẾT KẾ                KS CÔNG NGHỆ                    KS + QC / CEO
────────────                ────────────                    ─────────────
Chuẩn bị model (HD-01)      Chạy trích xuất (HD-02)         Gate G2/G3 (HD-04)
  iProperties + vật liệu      run_pipeline.py 1 lệnh          đo tay 3–5 giá trị
  chạy Export_QTCN_Package    sửa theo gate báo → chạy lại    golden set
       │                           │                              │
       ▼                           ▼                              ▼
Kiểm bản vẽ (HD-03)         seed VALIDATED ──► Sinh 5 đầu ra + kiểm AI (HD-05)
  drawing_check / live rule                      /qtcn → trace_numbers → trình duyệt
                                                       │
XƯỞNG / THỐNG KÊ ◄─────────────────────────────────────┘
Ghi số thật (HD-06): record_actuals → calibration.json → định mức lần sau chính xác hơn
```

## 2. Bảng vai trò — đọc tài liệu nào

| Vai trò | Việc | Đọc |
|---|---|---|
| Bên thiết kế (Inventor/Rhino) | Chuẩn bị model đạt chuẩn + export gói QTCN + xử lý `giao-viec.csv` | [HD-01](01-thiet-ke-chuan-bi-cad.md) |
| KS công nghệ | Chạy pipeline, đọc gate, quyết chạy lại hay chuyển việc về thiết kế | [HD-02](02-chay-trich-xuat.md), [HD-03](03-kiem-tra-ban-ve.md) |
| KS + QC | Gate G2 đo tay, nuôi golden set | [HD-04](04-gate-golden.md) |
| Người lập QTCN/định mức (+ AI) | Sinh 5 đầu ra, kiểm số AI trước khi trình | [HD-05](05-sinh-5-dau-ra-kiem-ai.md) |
| Thống kê xưởng | Ghi giờ công/vật tư/NDT thật | [HD-06](06-ghi-actuals-hieu-chinh.md) |
| CEO | Nhìn toàn cục 15 giây: `pipeline_dashboard.py --root <_QTCN_export>` | HD-02 §5 |
| Bất kỳ ai gặp lỗi | Tra bảng sự cố trước khi hỏi | [HD-07](07-xu-ly-su-co.md) |

## 3. Quy ước chung (áp dụng mọi script)

- **Exit code**: `0` ĐẠT · `1` ĐẠT-có-WARNING (được đi tiếp, phải đọc danh sách) ·
  `2` FAIL (gate chặn — không đi tiếp) · `3` lỗi môi trường/thiếu đầu vào ·
  `4` merge từ chối seed chưa validate.
- **File sinh ra** (`*.validation.json`, `*.freecad.json`, `*.rhino-check.json`,
  `*.material-map.json`) nằm cạnh file nguồn, KHÔNG commit vào git (đã gitignore).
- **FAIL không bao giờ được ghi đè bằng tay** — chỉ 2 đường: sửa nguồn rồi chạy lại,
  hoặc `--force` có chủ đích (ghi vào biên bản, cấm dùng cho phát hành).
- **File MẬT** (RCWS/AIRPAD/LARS…): chỉ xử lý trong vùng nội bộ, model local —
  tuyệt đối không đưa qua pipeline cloud. Phân loại đánh ở `WX_Classification`.
- Mọi script **read-only với file CAD gốc** — không có đường ghi ngược.

## 4. Môi trường (cài MỘT lần / máy)

| Cần | Kiểm tra |
|---|---|
| Python 3.10+ với `jsonschema`, `openpyxl`, `rhino3dm`, `pywin32` | `pip install jsonschema openpyxl rhino3dm pywin32` |
| FreeCAD 1.1 (`freecadcmd.exe`) | mặc định `C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe`; khác thì đặt env `FREECADCMD` |
| Inventor (cho export + live-check) hoặc chỉ Apprentice (cho drawing_check) | máy hiện tại có Inventor 2018 |
| 2 rule iLogic add làm **External Rule** | trỏ `D:\KN-Stack\cad-pipeline\scripts\inventor\*.vb` (HD-01 §4, HD-03 §3) |

Tự kiểm môi trường + toàn bộ harness: `python cad-pipeline/scripts/extract/run_battery.py`
— phải ĐẠT 8/8 trước khi tin bất kỳ số nào máy này sinh ra.
