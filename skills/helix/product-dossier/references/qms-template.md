# Sổ tay Quản lý Chất lượng (QLCL / QMS) — Rules & Template

Sinh **Sổ tay Quản lý chất lượng cho một sản phẩm** (product quality manual + Quality Plan) từ **QTCN.json** (checkpoint + YCKT) + **Data Spine**. Trọng tâm là **Quality Plan (Kế hoạch chất lượng)** — bảng điểm kiểm soát rút thẳng từ checkpoint của QTCN.

> Đây là sổ tay chất lượng **cấp sản phẩm/lô sản xuất**, không thay hệ thống QMS cấp công ty (ISO 9001 toàn doanh nghiệp). Nó biến các checkpoint kỹ thuật thành **kế hoạch kiểm soát có thể kiểm tra & lưu hồ sơ**.

---

## Cấu trúc tài liệu `SO-TAY-QLCL-<sp>.md`

### 1. Phạm vi & Chính sách chất lượng
- Sản phẩm áp dụng (mã, tên), phạm vi (chế tạo/lắp ráp/thử nghiệm theo QTCN).
- Chính sách chất lượng ngắn gọn: tuân thủ bản vẽ & tiêu chuẩn, "làm đúng ngay từ đầu", truy xuất nguồn gốc, cải tiến liên tục.
- Tài liệu viện dẫn: bản vẽ 19.xx, QTCN, tiêu chuẩn (TCVN/JIS/AWS…), quy chuẩn nghiệm thu.

### 2. Tổ chức & trách nhiệm chất lượng
- Ma trận RACI gọn: Công nhân (tự kiểm) · Tổ trưởng · KCS · Cán bộ công nghệ · Người ký nghiệm thu.
- Quy định bậc thợ tối thiểu theo nguyên công (từ `QTCN.labor.grade`); công đoạn hàn/NDT cần chứng chỉ.

### 3. Sơ đồ quá trình sản xuất (process map)
- Từ **QTCN flow** (A chế tạo → B lắp ráp/hiệu chỉnh → C thử nghiệm/bàn giao). Đánh dấu **điểm dừng kiểm tra (hold/witness point)**: NDT mối hàn, kín nước, siết lực, thử điện, thử nổi.

### 4. KẾ HOẠCH CHẤT LƯỢNG (Quality Plan / Control Plan) — cốt lõi
Mỗi `QTCN.json.operations[].checkpoints[]` → **một dòng**:

| TT | Nguyên công (mã) | Đặc tính KT kiểm soát | Tiêu chuẩn / dung sai | Phương pháp KT | Dụng cụ | Tần suất | Loại điểm | Hồ sơ ghi | Người KT |
|----|------------------|-----------------------|-----------------------|----------------|---------|----------|-----------|-----------|----------|
| 1 | B1 | Sai lệch tâm lỗ bích | ±1 mm | đo | thước cặp/cuộn | 100% | H | Phiếu KCS-01 | KCS |
| 2 | B5 | Mô-men siết M12 (8.8) | 45–55 Nm | cờ lê lực | cờ lê cân lực | 100% mối | H | BB siết lực | Tổ+KCS |
| 3 | B5 | Δ đường chéo khung | ≤ 5 mm | đo chéo | thước cuộn | mỗi cụm | H | Phiếu KCS-02 | KCS |
| 4 | B13 | Cấp kín nước mối nối | ≥ IP67 | quan sát bọc kín | — | 100% | W | BB điện | KCS |
| 5 | B14/C1 | Điện áp ắc quy | 12–12,8 V | đo | VOM | mỗi SP | W | BB thử điện | KCS |
| 6 | C2 | Chiều chìm phao Tp | ≈ 0,25 m | đo mớn nước | thước mớn | mỗi SP | W | BB thử nổi | Hội đồng |
| … | | | | | | | | | |

- **Ánh xạ trường:** `param`→Đặc tính; `nominal`+`tol`+`unit`→Tiêu chuẩn/dung sai; `method`→Phương pháp; (suy ra Dụng cụ từ method/QTCN equipment).
- **Loại điểm:** H = Hold (dừng chờ duyệt mới đi tiếp), W = Witness (chứng kiến), — = tự kiểm. Gán H cho: NDT, kín nước, siết lực tới hạn, thử nổi; W cho thử điện, mớn nước.
- **Tần suất:** 100% cho đặc tính an toàn/chức năng; lấy mẫu cho đặc tính phụ.

### 5. Kiểm soát hàn & NDT (nếu có kết cấu hàn)
- Tiêu chí mối hàn (chân ≥3mm, ngấu, không nứt/rỗ/ngậm xỉ) từ YCKT bản vẽ.
- Kế hoạch VT 100% + PT các mối chịu lực; biểu mẫu biên bản NDT; xử lý & kiểm lại khi khuyết tật.

### 6. Kiểm soát sản phẩm không phù hợp (KPH) & hành động khắc phục
- Quy trình phát hiện → cách ly/đánh dấu → hội đồng quyết (sửa/loại/nhân nhượng) → khắc phục → phòng ngừa. Sổ theo dõi KPH.

### 7. Truy xuất nguồn gốc & lưu hồ sơ
- Gắn **mã VT / mã bản vẽ / số lô / số sản phẩm** vào mọi phiếu. Danh mục hồ sơ lưu: phiếu KCS, BB NDT, BB siết lực, BB thử điện/thử nổi, BB nghiệm thu-bàn giao. Thời hạn lưu.

### 8. Biểu mẫu kèm theo (phụ lục)
- KCS-01 (kích thước/lỗ bích), KCS-02 (hình học khung/thẳng đứng), BB siết lực, BB NDT (VT/PT), BB thử điện, BB thử nổi/thử neo, BB nghiệm thu-bàn giao, Sổ KPH. Mỗi mẫu có ô: hạng mục | tiêu chuẩn | kết quả đo | đạt/không | người KT | ngày.

---

## Quy tắc sinh
1. **Quality Plan = 1:1 với checkpoints** của QTCN — không thêm/bớt đặc tính kỹ thuật ngoài checkpoint; nếu cần thêm, bổ sung checkpoint ở QTCN trước (giữ một nguồn sự thật).
2. **Con số khớp QTCN** (dung sai, lực siết, IP, điện áp, mớn nước) — lệch = lỗi.
3. Gán **loại điểm H/W** theo mức rủi ro (an toàn/chức năng → H). Ghi rõ điểm dừng để không đi tiếp khi chưa đạt.
4. Chưa có tiêu chuẩn nghiệm thu chính thức cho một đặc tính → đánh dấu `[CẦN TIÊU CHUẨN]`, không tự đặt ngưỡng.

## Đầu ra
- `SO-TAY-QLCL-<sp>.md` — 8 mục trên, trọng tâm Quality Plan.
- (tùy chọn) `quality-plan-<sp>.json` — control plan máy đọc `{ op_id, characteristic, standard, method, tool, frequency, point_type, record, inspector }` để nhập phần mềm QC / đối soát khi kiểm tra thực tế.
