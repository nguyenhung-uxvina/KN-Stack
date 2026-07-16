# Golden Set — Gate G3 (WX-QT-EXTRACT-SENSOR-01 mục 4.3, 5)

Bộ file CAD mẫu **đã biết đáp án đúng**. Mọi phiên bản extractor mới phải chạy qua
toàn bộ golden set và khớp đáp án 100% (trong dung sai) **trước khi được dùng** —
regression test chuyển từ "tin script" sang "chứng minh script đúng".

## Cấu trúc

```
golden/
  make_golden_v0.py        ← sinh 3 case giải tích (chạy bằng freecadcmd)
  step/                    ← nhánh theo NGUỒN (inventor/, dxf/… thêm sau)
    <case>/
      source/*.step        ← file CAD nguồn
      expected-seed.json   ← ĐÁP ÁN — tính tay/đo tay, KHÔNG copy từ máy
      actual-seed.json     ← output extractor (sinh lại mỗi lần chạy G3)
      notes.md             ← phép tính/người đo, ngày, chỗ oái oăm của ca
```

## Chạy G3

```bash
# 1. Sinh lại actual từ extractor phiên bản đang xét (mỗi case):
FC_FILE=<case>/source/<x>.step FC_OUT=<case> FC_NAME=actual-seed \
  "C:/Program Files/FreeCAD 1.1/bin/freecadcmd.exe" cad-pipeline/scripts/extract/freecad_extract.py
# 2. So với đáp án:
python cad-pipeline/scripts/extract/validate_qtcn_seed.py --golden cad-pipeline/golden/step
# exit 0 = 100% khớp -> ĐƯỢC phát hành | exit 2 = CẤM phát hành
```

## Hiện trạng v0 (2026-07-02) — 3 case giải tích

| Case | Hình học | Bắt lỗi gì |
|---|---|---|
| plate-4holes | tấm 1000×500×10, 4 lỗ Ø50 | khối lượng, diện tích, trừ lỗ, nhầm đơn vị |
| box-tube | hộp 60×40×3, L=1000 | thành mỏng, mặt trong có vào diện tích không |
| cylinder | trụ Ø100×200 | mặt cong; ca thử rule đẳng chu S1-05 |

Đáp án v0 là **giải tích** (tính tay chính xác tuyệt đối — mạnh hơn đo tay).
Ngay lần chạy đầu, golden set đã bắt được 1 lỗi thật: `Part.export` làm MẤT nhãn
chi tiết trong STEP (name thành "Open CASCADE STEP translator") → generator chuyển
sang `Import.export`. Đúng vai trò của G3.

## Việc phải làm tiếp (theo mục 5 đặc tả)

- Nhánh `inventor/`: 3–5 file .ipt/.iam THẬT, đo tay 2 người ký (khởi động khi chạy
  iLogic lần đầu trên assembly thật).
- Case weldment nhiều đoạn + tấm cong đôi + assembly có chi tiết lặp.
- Mỗi lỗi lọt lưới trong sản xuất → thêm case vĩnh viễn (lỗi một lần, không lần hai).
