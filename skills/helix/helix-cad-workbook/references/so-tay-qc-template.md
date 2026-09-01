# Template — SỔ TAY QUẢN LÝ CHẤT LƯỢNG DỰ ÁN {{PROJECT}}

> Điền từ {PROJECT}_FAB-DB.xlsx (sheet QC_DIMS + PARTS + CHECKLIST). QUY TẮC: mỗi dòng kế hoạch
> kiểm PHẢI truy về 1 dòng QC_DIMS — không bịa phép kiểm. Xuất DOCX: /convert_md_to_docx.

## 0. Bìa + kiểm soát tài liệu
| Trường | Giá trị |
|---|---|
| Tài liệu | STCL-{{PROJECT}}-{{REV}} |
| Dự án / Sản phẩm | {{PROJECT}} — {{PRODUCT_NAME}} |
| Soạn / Kiểm tra / Phê duyệt | {{AUTHOR}} / {{REVIEWER}} / {{APPROVER}} (ký, ngày) |
| Phân loại | {{CLASSIFICATION}} |
| Nguồn dữ liệu | {{PROJECT}}_FAB-DB.xlsx (master data v{{MASTER_VERSION}}, sinh {{GENERATED_AT}}) |

Bảng sửa đổi: | Rev | Ngày | Nội dung | Người duyệt |

## 1. Chính sách & trách nhiệm QC
- Quản đốc phân xưởng: kiểm trong-nguyên-công (tự kiểm 100% kích thước tới hạn).
- QC xưởng: gate CKCX / DT / DC / VL / Final; lập biên bản; quyền dừng chuyền.
- Kỹ sư định danh: duyệt NCR, ký xuất xưởng. PASS validator ≠ an toàn — chữ ký người thật là gate cuối.

## 2. Kế hoạch kiểm per-part (từ sheet QC_DIMS)
| Part | Đặc tính kiểm | Danh nghĩa | Dung sai | Dụng cụ đo | Tần suất | Tiêu chí chấp nhận |
|---|---|---|---|---|---|---|
| {{PART_ID}} | {{FEATURE}} | {{VALUE}} | {{TOLERANCE}} | {{GAUGE}} | 100% tới hạn / AQL còn lại | trong dung sai |

Part có CHECKLIST cột SO_TAY_QC ≠ "ĐỦ": liệt kê + biện pháp bổ sung dữ liệu TRƯỚC khi sản xuất.

## 3. Gate QC
| Gate | Nội dung | Hồ sơ |
|---|---|---|
| CKCX | Cơ khí chính xác — kích thước tới hạn sau gia công | Phiếu đo từng part |
| DT | Điện/điện tử (nếu có) | Biên bản test |
| DC | Dung sai cụm — lắp thử | Biên bản lắp |
| VL | Vật liệu — CO/CQ, đối chiếu MATERIALS master | CO/CQ |
| Final | Nghiệm thu xuất xưởng | Biên bản + ảnh |

## 4. Biểu mẫu
- Phiếu đo kích thước (part_id / đặc tính / thực đo / KL đạt-không / người đo / ngày)
- Biên bản NCR (mô tả / nguyên nhân / xử lý: sửa-loại-nhân nhượng / người duyệt = kỹ sư định danh)
- Biên bản nghiệm thu Final

## 5. Ma trận truy xuất
| Part | Bản vẽ (rev) | Dòng QC_DIMS | Phiếu đo | Biên bản gate | NCR (nếu có) |
|---|---|---|---|---|---|

Lưu hồ sơ ≥ 5 năm. Dụng cụ đo có tem hiệu chuẩn còn hạn (sổ hiệu chuẩn riêng).
