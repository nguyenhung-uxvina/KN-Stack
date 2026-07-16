# HD-04 — GATE G1/G2/G3 VÀ GOLDEN SET

> Gate là chỗ QUYỀN LỰC của harness: số chưa qua gate = số chưa tồn tại.
> Đặc tả gốc (mã rule chính thức của CEO): `docs/WX-QT-EXTRACT-SENSOR-01.md`.

## 1. Ba gate — ai, làm gì

| Gate | Bản chất | Ai | Khi nào |
|---|---|---|---|
| **G1** máy | Sensor S1–S4 tự chấm seed; FAIL → seed không validated (exit 2) | tự động trong `run_pipeline.py` | mọi lần trích |
| **G2** người | Lấy mẫu **3–5 giá trị** trong seed, đối chiếu nguồn độc lập (đo tay/bản vẽ), 2 người ký | KS + QC | trước phát hành lô đầu của mỗi sản phẩm/adapter |
| **G3** hồi quy | Chạy lại toàn bộ golden set — phải khớp đáp án 100% | tự động (pre-commit hook + battery) | mọi lần sửa code/schema/golden |

## 2. Gate G2 — quy trình đo tay (bắt buộc trước lô đầu)

1. Mở `<seed>.validation.json` → mục WARNING là danh sách G2 máy đề nghị người xem;
   chọn 3–5 giá trị ưu tiên: mass nhóm nặng nhất, QTY nhóm nhiều nhất, 1 bbox, 1 vật liệu.
2. Đối chiếu với nguồn ĐỘC LẬP với đường trích: đo tay trên vật thật / đọc trực tiếp
   trên bản vẽ ký duyệt / cân.
3. Hai người (KS + QC) ký xác nhận vào biên bản (form F02 trong đặc tả EXTRACT §Gate).
4. Bộ giá trị đã ký = **đáp án khởi tạo golden nhánh mới** (§3) — một lần đo, dùng mãi.

## 3. Golden set — luật "lỗi một lần, không lần hai"

Vị trí: `cad-pipeline/golden/` — `fixtures/` (seed cài lỗi phải bị bắt) ·
`step/` (4 case giải tích: khối lượng tính tay bằng công thức) · `rhino/` (2 fixture .3dm).

- **Bug lọt lưới phát hiện ở sản xuất** → viết golden case tái hiện bug TRƯỚC khi vá,
  case ở lại vĩnh viễn (ví dụ có sẵn: `step/frame-varies` — bug lệch instance 794%).
- Chạy tay khi cần: `python cad-pipeline/scripts/extract/validate_qtcn_seed.py --golden cad-pipeline/golden/step`
- Thêm case hình học mới: sửa `golden/make_golden_v0.py` (nhớ dùng `Import.export`,
  KHÔNG `Part.export` — mất nhãn part), chạy battery `--regen` để sinh đáp án, tính tay
  kiểm chứng con số trước khi commit.

## 4. Battery + pre-commit (G3 tự động theo commit)

```bash
python cad-pipeline/scripts/extract/run_battery.py            # kiểm 8 hạng mục
python cad-pipeline/scripts/extract/run_battery.py --regen    # kèm regen golden STEP (cần freecadcmd)
```

Pre-commit hook (cài theo hướng dẫn đầu file `cad-pipeline/scripts/hooks/pre-commit`)
tự chạy battery khi commit chạm `cad-pipeline/(scripts|schemas|golden)`. Battery đỏ =
không commit được; bỏ qua chỉ khi có chủ đích: `git commit --no-verify` (ghi rõ lý do
trong message).

## 5. Kiểm nhanh 1 seed (không cần nhớ lệnh)

Kéo-thả file seed vào `cad-pipeline/scripts/extract/self_check.bat` — chạy G1 sơ bộ,
in verdict ngay trên console.

## 6. Chính sách phát hành

Một bộ số chỉ được vào định mức/dự toán/hồ sơ nghiệm thu khi ĐỦ:
G1 PASS (`--release`, tức có kiểm chéo 2 nguồn) **+** G2 đã ký (lô đầu) **+**
G3 xanh tại commit tương ứng (tag `cad-pipeline-vX.Y` ghi trong `extractor_version` của seed).
Thiếu bất kỳ mảnh nào → số chỉ dùng tham khảo nội bộ, đóng dấu NHÁP.
