# HD-03 — KIỂM TRA BẢN VẼ/MODEL (TẦNG 1)

> Chạy TRƯỚC tầng trích xuất: model FAIL tầng này thì không Released, không vào tầng 2.
> Rule đầy đủ: `docs/WX-QT-DRAWING-SENSOR-01.md` (D1 metadata · D2 hình học ·
> D3 bản vẽ 2D · D4 theo loại chi tiết · D5/SEC phân loại mật).

## 1. Kiểm nhanh không cần mở Inventor (Apprentice)

```bash
python cad-pipeline/scripts/extract/drawing_check.py --file "<file .ipt|.iam>"
```

- Kiểm lớp **D1** (Part Number, vật liệu ≠ Generic, iProperties WX_*, mass cache)
  + **SEC** (WX_Classification hợp lệ). Console gom theo rule; chi tiết từng part trong
  `drawing_report.json`.
- Tùy chọn: `--pn-regex "<regex>"` áp quy ước mã PN của sản phẩm;
  `--materials <json>` nếu dùng danh mục khác mặc định.

## 2. Xuất phiếu giao việc cho bên thiết kế

```bash
python cad-pipeline/scripts/extract/drawing_check.py --file "<asm.iam>" --ticket
```

Ra `giao-viec.csv` — mỗi dòng 1 part chưa đạt + lý do. Gửi nguyên file cho bên thiết kế
(cách xử lý phía họ: HD-01 §2). Chạy lại sau khi họ sửa để chốt vòng.

## 3. Kiểm cần Inventor SỐNG (interference, BOM view, dim dangling)

Các rule Apprentice không với tới: D2-04 (giao nhau chi tiết), D2-05 (occurrence trôi
ràng buộc), D1-11 (Parts Only đã Enable?), D3-03 (dimension mất tham chiếu),
D3-07 (ký hiệu hàn trên .idw).

1. Add 1 lần: Manage → iLogic → **External Rules → Add** →
   `D:\KN-Stack\cad-pipeline\scripts\inventor\Drawing_Check_Live.iLogic.vb`
2. Mở **.iam** → Run rule → kiểm D2-04/D2-05/D1-11.
   Mở **.idw/.dwg** → Run rule → kiểm D3-03/D3-07.
3. Kết quả: hộp thoại + `drawing_live_report.json` cạnh file tài liệu. Read-only —
   rule không sửa/không lưu gì.

> Lưu ý lần chạy đầu: AnalyzeInterference trên assembly lớn có thể chậm (chạy giờ nghỉ);
> vài thuộc tính dimension khác nhau theo version Inventor — gặp lỗi biên dịch báo
> người giữ pipeline kèm ảnh chụp (các điểm [VER] đã đánh dấu sẵn trong rule).

## 4. Model Rhino (.3dm)

```bash
python cad-pipeline/scripts/extract/rhino_check.py --file "<hull.3dm>"
```

Kiểm HU-01…04: solid kín, đơn vị/tolerance document, layer đúng tiền tố, UserText
`material`/`plate_mm`. Ra `<file>.rhino-check.json` + `<file>.material-map.json`
(bảng object→vật liệu — đầu vào cho bước gán ρ sau khi qua STEP).
Giới hạn thật: rhino3dm KHÔNG tính được mass — khối lượng đi đường STEP (HD-01 §4).

## 5. Bản vẽ 2D rời (DXF/PDF)

```bash
python cad-pipeline/scripts/extract/parse_mech_drawing.py --dxf "<bản vẽ.dxf>" --out <dir>
```

Ra JSON kích thước/dung sai/khung tên — validate như mọi seed rồi đưa vào
`run_pipeline.py --seed2d` (HD-02 §1). PDF scan/mojibake: ưu tiên DXF gốc;
chữ font TCVN3 cũ decode được bằng bảng map (hỏi người giữ pipeline), không đoán mắt.
