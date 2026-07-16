# HD-05 — SINH 5 ĐẦU RA VÀ KIỂM SỐ AI (TẦNG 3)

> Đầu vào: `qtcn-seed-final.json` VALIDATED (HD-02). Đầu ra: QTCN · định mức KTKT ·
> dự toán · kế hoạch chất lượng (QCP) · biên bản nghiệm thu.
> Nguyên tắc sắt: **AI được SOẠN, không được BỊA — mọi số kèm đơn vị phải truy về seed.**

## 1. Sinh bản nháp bằng skill

- Một sản phẩm, một đầu ra: skill `/qtcn` (đưa đường dẫn seed final).
- Cả bộ hồ sơ từ thư mục tài liệu: skill `/product-dossier` (orchestrator — CEO chọn
  xuất QTCN / định mức / sổ tay QLCL…; qtcn.json là xương sống).
- AI chỉ được lấy số từ seed + hằng số kỹ thuật khai báo; thiếu số → ghi
  "『THIẾU — cần đo/bổ sung』" chứ không ước lượng thầm.

## 2. Kiểm máy TRƯỚC khi người duyệt đọc (bắt buộc)

```bash
python cad-pipeline/scripts/extract/trace_numbers.py --doc "<ban-nhap.md>" \
    --seed qtcn-seed-final.json [--seed <seed-khác.json>] [--report <path>]
```

- Truy mọi **số CÓ ĐƠN VỊ** (kg, mm, m, %, giờ, cái…) về: một trường seed, biến đổi
  đơn vị (×/÷1000), tích với số lượng, hoặc hằng số khai báo. Khớp **đúng thứ nguyên**
  (kg chỉ khớp trường mass, "cái" chỉ khớp qty — trùng ngẫu nhiên khác trường vẫn là mồ côi).
- Số trần không đơn vị (mã hiệu, mục lục) bỏ qua có chủ đích. Hiểu định dạng số VN
  ("1.020.575,22"; chấm nhập nhằng thử cả 2 cách đọc).
- **Exit 2 = có số mồ côi → tài liệu KHÔNG trình duyệt.** Sửa nguồn số (hoặc bổ sung
  hằng số CHÍNH ĐÁNG vào `--constants`) rồi chạy lại. Cấm "sửa cho khớp" bằng cách
  đổi số trong tài liệu cho trùng seed — phải tìm ra số đó từ đâu ra.

`--constants` là file JSON list các hằng số kỹ thuật được phép (ví dụ
`[1.025, 1.5, 2.66]` — mật độ nước biển, hệ số an toàn, ρ nhôm). Mặc định đã có bộ
mật độ vật liệu + 1.025 + 1.5; chỉ thêm khi tài liệu dùng hằng số mới, và hằng số đó
phải xuất hiện trong tài liệu dưới dạng công thức khai báo, không phải số trơ.

## 3. Vòng duyệt người

1. `trace_numbers` exit 0 → đính `<doc>.trace.json` (nếu chạy `--report`) vào hồ sơ trình.
2. Người duyệt đi qua checklist `/aigate` (check 1 = trace máy đã chạy) — đọc NỘI DUNG
   công nghệ (trình tự nguyên công, WPS, tiêu chuẩn nghiệm thu), không phải dò số —
   dò số là việc máy đã làm.
3. Ký → phát hành. Số hiệu seed + `extractor_version` + verdict ghi ngay chân tài liệu
   để 2 năm sau còn truy được nguồn.

## 4. Định mức: dùng hệ số THẬT khi đã có

Sau vài sản phẩm có ghi actuals (HD-06), `calibration.json` chứa hệ số giờ công/suất hàn/
hao hụt thật. Khi lập định mức mới: đưa `calibration.json` cho AI kèm seed — hệ số thật
THAY hệ số ước tính (và ghi rõ trong tài liệu là dùng hệ số hiệu chỉnh từ n record).
