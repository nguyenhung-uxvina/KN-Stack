# Template — QUY TRÌNH CÔNG NGHỆ (TCVN / defense process document)

> **Mục đích:** Khi F0 cần xuất một *quy trình công nghệ chế tạo* phát hành cho xưởng CNQP (không phải gói ERPNext), dùng cấu trúc 11 mục dưới đây thay cho bản routing rút gọn. Soạn Markdown → `convert_md_to_docx` → DOCX trình ký.
> **Khi nào dùng:** sản phẩm quốc phòng / khách Viện–Nhà máy QP cần tài liệu công nghệ trình duyệt + nghiệm thu; hoặc CEO yêu cầu "xuất quy trình chế tạo / quy trình công nghệ cho xưởng".
> **Nguồn dữ liệu:** PARTS_MASTER + FAB_ROUTING (từ helix-cad-ingest) + ghi chú chung trên bản vẽ.
> **Defense rule:** nếu MẬT → có dòng kiểm soát tài liệu mật + ô số bản in; KHÔNG nhúng dữ liệu nhạy cảm ngoài mức cần thiết.

## Cấu trúc bắt buộc (11 mục)

1. **Trang bìa + kiểm soát tài liệu** — mã SP, đơn vị TK, phân loại (MẬT/…), SL, tài liệu nguồn, mã run, ngày. Dòng MẬT + ô "Số kiểm soát bản in / Bản số / Tổng số trang". **Bảng phê duyệt**: Soạn thảo · Kiểm tra (KCS/Phòng KT) · Phê duyệt (Thủ trưởng) — Họ tên / Chức vụ / Chữ ký–Ngày.
2. **Bảng theo dõi sửa đổi (Revision History)** — Lần sửa | Ngày | Nội dung thay đổi | Người lập | Người duyệt. Lần 00 = ban hành đầu.
3. **§1 Phạm vi áp dụng** — quy định gì, cho sản phẩm/cụm nào, ràng buộc "mọi sai khác phải được Viện + cơ quan công nghệ duyệt bằng văn bản".
4. **§2 Tài liệu viện dẫn** — bảng tiêu chuẩn (xem danh mục mặc định bên dưới); để trống số TQS cho Viện điền.
5. **§3 Yêu cầu kỹ thuật chung** — laser+chấn; dung sai không ghi = IT14/2 (TCVN 2244/2245); dung sai HD-VT (TCVN 5906); làm cùn cạnh; Rz20; mối hàn ngấu đều/không nứt/không rỗ (ký hiệu TCVN 1691, quá trình TCVN 8524, chuẩn bị mối nối TCVN 12425); **vật liệu phải có CO/CQ**, thay thế phải được duyệt; mác tương đương.
6. **§4 Cấu trúc sản phẩm (BOM tổng)** — bảng cụm: mã | tên | khối lượng | ghi chú.
7. **§5 Quy trình công nghệ chế tạo chi tiết**
   - 5.1 **Trạm Laser+Chấn** — nhóm theo *vật liệu × bề dày* (sắp hình/nesting), bảng SL|chi tiết|mã|kích thước.
   - 5.2 **Trạm Tiện/Phay** — bảng SL|chi tiết|mã|vật liệu|kích thước chính.
   - 5.3 **Mua ngoài / cắt phôi**.
   - 5.4 **Phiếu công nghệ nguyên công (điển hình)** — xem mẫu phiếu bên dưới; lập ≥1 phiếu/nhóm công nghệ (tấm, trục đặc, chi tiết rỗng, cụm hàn), còn lại "lập tương tự theo PARTS_MASTER".
8. **§6 Trình tự lắp ráp & hàn** — Bước 1 cụm con → Bước 2 cụm trung → Bước 3 tổng lắp.
9. **§7 Định mức vật tư** — bảng theo nhóm vật liệu + **% hao hụt công nghệ** (đề xuất: tấm laser +8%, phôi tiện +15%, định hình/cắt +5%, Teflon/cao su +10%, vật tư hàn theo định mức). Ghi rõ "Viện/bộ phận định mức xác nhận trước khi cấp phôi".
10. **§8 QC & nghiệm thu** — bảng cổng (Gate-Cắt/Tiện/Hàn/Lắp) + nội dung kiểm; kích thước critical; VT 100% mối hàn, PT/UT mối chịu lực; sai vượt dung sai → **NCR** do Viện quyết.
11. **§9 ATLĐ** · **§10 Bao gói–ghi nhãn–bảo quản–bàn giao** · **§11 Cảnh báo chất lượng dữ liệu** (các blocker/xung đột phát hiện khi đọc CAD — đánh 🔴🟠🟡, nêu để Viện xử lý, KHÔNG tự sửa bản vẽ gốc).

## Danh mục tài liệu viện dẫn mặc định (điền/bớt theo SP)
| Số hiệu | Nội dung |
|---|---|
| TCVN 2244:1999 (ISO 286-1) | Hệ thống ISO dung sai & lắp ghép — cơ sở |
| TCVN 2245:1999 (ISO 286-2) | Cấp dung sai & sai lệch giới hạn lỗ/trục |
| TCVN 5906:1995 | Dung sai hình dạng & vị trí — ký hiệu trên bản vẽ |
| TCVN 1691:1975 | Mối hàn hồ quang tay — ký hiệu & biểu diễn |
| TCVN 8524 (ISO 4063) | Danh mục quá trình hàn & số hiệu tham chiếu |
| TCVN 12425-1/-2 (ISO 9692) | Chuẩn bị mối nối hàn |
| JIS G3101 | Thép kết cấu cán nóng SS400 |
| TCVN 1766 / JIS S45C | Thép cacbon kết cấu — C45 |
| EN AW-5083 / ASTM B209 | Hợp kim nhôm 5083 — tấm/lá |
| ASTM A240 / TCVN 6571 | Thép không gỉ tấm — INOX 304 |
| TQS …… | TQS về tài liệu công nghệ & nghiệm thu SP QP (Viện điền) |
| Bộ bản vẽ <mã>.xx.xx | Bản vẽ thiết kế (PDF + DXF) |

## Mẫu PHIẾU CÔNG NGHỆ NGUYÊN CÔNG (lập 1 phiếu/chi tiết hoặc cụm)
Header: *Chi tiết/Cụm · Mã · Vật liệu · Phôi · SL.*
Bảng nguyên công:

| NC | Nội dung nguyên công | Thiết bị / Đồ gá | Dụng cụ cắt – dụng cụ đo | Chế độ công nghệ | Bậc thợ |
|---|---|---|---|---|---|

- Bậc thợ ghi `x/7` = yêu cầu tối thiểu. Nguyên công cuối luôn là **kiểm tra → cổng Gate-… (KCS)**.
- 4 phiếu điển hình tối thiểu: (1) tấm laser+chấn, (2) trục đặc tiện, (3) chi tiết rỗng khoan-khoét-doa, (4) cụm hàn (chuẩn bị→hàn đính→hàn hoàn thiện→nắn/làm sạch→VT).

### Ví dụ — phiếu tấm laser+chấn
NC10 Cắt laser CNC theo DXF khai triển (máy laser; thước cặp; chế độ theo bề dày) 3/7 ·
NC20 Làm sạch ba via, cùn cạnh (bàn nguội/mài tay) 3/7 ·
NC30 Chấn gấp theo gân khai triển (máy chấn CNC; dao V; dưỡng góc) 4/7 ·
NC40 Kiểm tra khai triển/góc/lỗ (bàn KCS; thước, dưỡng) → Gate-Cắt.

### Ví dụ — phiếu trục tiện (vd Ø30h7)
NC10 cắt phôi/khỏa mặt/khoan tâm 2 đầu 3/7 · NC20 tiện thô (t=1,5–2mm) 4/7 ·
NC30 tiện tinh + vát mép, đạt Rz20 5/7 · NC40 kiểm Ø h7/L/đồng tâm/nhám (panme, đồng hồ so 0,05) → Gate-Tiện.

## Quy tắc
- Mục §11 (cảnh báo dữ liệu) là **bắt buộc** khi nguồn là bản vẽ đọc bằng helix-cad-ingest — liệt kê stale-code/conflict/missing đã phát hiện; KHÔNG tự "đoán sửa" bản vẽ gốc.
- Footer ghi rõ "Lập tự động từ bản vẽ qua quy trình đọc CAD (helix-cad-ingest → forge-fabrication F0). Cần CEO/Viện rà soát mục cảnh báo trước khi phát hành xưởng."
- Tài liệu MẬT: chế độ tài liệu mật ở bìa + §10.
