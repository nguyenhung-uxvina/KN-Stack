# HD-06 — GHI SỐ LIỆU THẬT TỪ XƯỞNG (GIAI ĐOẠN 4 — VÒNG PHẢN HỒI)

> Người thực hiện: thống kê xưởng / tổ trưởng, cuối mỗi nguyên công hoặc cuối ngày.
> Vì sao: định mức lần đầu là ƯỚC TÍNH. Ghi số thật đều tay → sau 3–5 sản phẩm,
> định mức chuyển sang dữ liệu thật của chính Workshop X — đấu thầu sát giá hơn.

## 1. File sổ ghi

Mỗi sản phẩm một file `actuals.jsonl` đặt cạnh hồ sơ sản phẩm (append-only — chỉ thêm
dòng, không sửa dòng cũ; ghi sai thì thêm dòng đính chính mới). Mỗi record được kiểm
schema (`schemas/qtcn-actuals.schema.json`) TRƯỚC khi ghi — sai là từ chối (exit 2),
không làm bẩn sổ.

## 2. Ghi một record

Tiện nhất: điền form/Excel xuất ra file JSON rồi:

```bash
python cad-pipeline/scripts/extract/record_actuals.py --file actuals.jsonl --add-file record.json
```

(Ghi nhanh inline: `--add '{...}'` cùng nội dung.)

**3 loại record** — trường chung: `schema` ("qtcn-actuals/v1"), `product_code`,
`nguyen_cong`, `date` (YYYY-MM-DD), `recorded_by`, `type`:

```json
{"schema":"qtcn-actuals/v1","product_code":"BM-01","nguyen_cong":"NC05-HAN",
 "date":"2026-07-20","recorded_by":"Hùng","type":"labor",
 "labor":{"est_hours":12,"actual_hours":15.5,"weld_length_m":38.4,"position":"PB","grade":"3/7"}}
```

```json
{"schema":"qtcn-actuals/v1","product_code":"BM-01","nguyen_cong":"NC02-CAT",
 "date":"2026-07-21","recorded_by":"Lan","type":"material",
 "material":{"item":"Nhôm 5083 t5","net_kg":120.4,"issued_kg":138.0,"scrap_kg":9.2}}
```

```json
{"schema":"qtcn-actuals/v1","product_code":"BM-01","nguyen_cong":"NC05-HAN",
 "date":"2026-07-25","recorded_by":"QC-Minh","type":"ndt",
 "ndt":{"method":"VT","checked":142,"defects":3}}
```

Ghi chú thực địa: `est_hours` lấy từ định mức đã duyệt; `position` là tư thế hàn
(PA/PB/PF…); `net_kg` = khối lượng CAD thuần, `issued_kg` = xuất kho thật.

## 3. Báo cáo hiệu chỉnh (định kỳ / cuối sản phẩm)

```bash
python cad-pipeline/scripts/extract/record_actuals.py --file actuals.jsonl --report --out calibration.json
```

In + ghi `calibration.json`:

- **Hệ số giờ công** = Σthật/Σđịnh mức, tách theo `nguyên công | bậc thợ | tư thế`
  (đúng đơn vị mà định mức dùng)
- **Suất hàn thật** m/giờ theo tư thế (đối chiếu được với `weld-report.json`)
- **Hệ số hao hụt vật tư** = Σxuất kho/ΣCAD thuần + lượng thu hồi đầu mẩu
- **Tỷ lệ khuyết tật NDT** theo phương pháp (đầu vào cho QCP sản phẩm sau)

`calibration.json` là ĐẦU VÀO cho lần lập định mức kế tiếp (HD-05 §4). Hệ số chỉ đáng
tin khi `n` đủ lớn — dưới 3 record cùng nhóm thì vẫn dùng ước tính, ghi chú rõ.
