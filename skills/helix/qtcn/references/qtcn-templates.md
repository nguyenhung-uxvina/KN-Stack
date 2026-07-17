# QTCN — Mẫu đầu ra (Output Templates)

Ba dạng đầu ra. Dùng `<…>` là chỗ điền. Mọi mã VT phải khớp BOM.

---

## A. BẢN CHI TIẾT — `QTCN-<sp>-chi-tiet.md`

````markdown
# CHI TIẾT CÁC NGUYÊN CÔNG <LOẠI QUY TRÌNH> THIẾT BỊ <TÊN SẢN PHẨM>

Tài liệu mô tả chi tiết từng bước thao tác, thông số kỹ thuật, vật tư và thiết bị cho toàn bộ <N> nguyên công theo Sơ đồ dòng công nghệ tối ưu.

---

## NGUYÊN CÔNG <k>: <TÊN NGUYÊN CÔNG> (<mã VT liên quan>)

### I. Yêu cầu kỹ thuật
1. <Bước thao tác, kèm thông số định lượng: dung sai, lực siết, phương pháp đo>
   - <chi tiết phụ / quy tắc lắp ghép>
2. **<QUY TẮC CỐT LÕI in đậm khi có — vd: gá lỏng, chưa siết chặt>**

### II. Thông số định mức và phân công
*   **Bậc thợ:** <vd 4/7>
*   **Định mức thời gian:** <vd 30 phút>
*   **Nơi thực hiện:** <vd Bãi lắp dựng ngoài trời>

### III. Danh mục nguyên, vật liệu và thiết bị
*   **Nguyên, vật liệu:**
    1. <Tên gọi> (<mã VT>): <SL>
*   **Thiết bị, trang bị công nghệ:**
    1. <Tên dụng cụ/đồ gá> (<thông số>): <SL>

---
<lặp lại cho từng nguyên công>
````

---

## B. BẢN TỔNG HỢP TỐI ƯU — `QTCN-<sp>-tong-hop.md`

````markdown
# QUY TRÌNH CÔNG NGHỆ <LOẠI> THIẾT BỊ <TÊN SẢN PHẨM> (BẢN TỐI ƯU HÓA)

## I. QUY ĐỊNH CHUNG VỀ KỸ THUẬT VÀ AN TOÀN

### 1. Quy định chung về kỹ thuật
1. Người tham gia phải được đào tạo đúng chuyên môn, nắm vững các bước công nghệ.
2. Tuân thủ chặt chẽ yêu cầu kỹ thuật trong bản vẽ thiết kế và hướng dẫn công nghệ.
3. Chấp hành chế độ trách nhiệm, số lượng người tại vị trí làm việc và bàn giao ca.
4. Toàn bộ liên kết bu lông ngoài trời dùng đầy đủ đệm phẳng + đệm vênh chống tự nới lỏng do rung động sóng nước.
5. Mối nối điện ngoài trời bọc kín bằng băng keo tự co chống nước đạt IP67.
<điều chỉnh theo môi trường khai thác thực tế>

### 2. Quy định chung về an toàn
1. Thực hiện đúng quy định an toàn lao động tại vị trí làm việc.
2. Kiểm tra thiết bị nâng hạ, dụng cụ cầm tay, BHLĐ trước khi lắp ráp.
3. Trang bị BHLĐ (mũ, găng chống cắt, giày, dây đai an toàn) đầy đủ theo quy định.
4. Khi sự cố mất an toàn: ngắt nguồn điện, di chuyển sản phẩm đến nơi an toàn, xử lý theo phương án khẩn cấp.

---

## II. BẢNG TỔNG HỢP TIẾN TRÌNH CÔNG NGHỆ TỐI ƯU (OPTIMIZED FLOW)

| STT | Tên nguyên công | Thiết bị, trang bị công nghệ chủ chốt | Bậc thợ | Định mức (phút) |
| :--- | :--- | :--- | :---: | :---: |
| 1 | <…> | <…> | 4/7 | <…> |
| … | | | | |

---

## III. NỘI DUNG CHI TIẾT CÁC NGUYÊN CÔNG (TỪ <a> ĐẾN <N>)

### NGUYÊN CÔNG <k>: <tên> (<VT>)
*   **Yêu cầu kỹ thuật:**
    1. <cô đọng các bước + thông số chính>
*   **An toàn:** <điểm an toàn đặc thù của nguyên công>
<lặp lại>
````

> Quy ước: NC1 (kiểm tra đầu vào) và NC cuối (kiểm tra tổng thể + bàn giao) thường mô tả ở bản chi tiết; bản tổng hợp tập trung NC 2 → N-1 lắp ráp/hiệu chỉnh. Tổng định mức = Σ thời gian các NC.

---

## C. BIỂU MẪU QTCN CHÍNH THỨC (form xưởng — mỗi nguyên công 1 phiếu)

Khi cần văn bản ký đóng dấu, dựng bảng theo khối tiêu đề chuẩn (xuất DOCX qua `convert_md_to_docx` rồi định dạng bảng, hoặc tạo bảng trực tiếp):

```
┌─────────────────────────────────────────────────────────────────────┐
│ Đơn vị: <…>        │ Tên chi tiết: <Tên SP>     │ Ký hiệu tài liệu:   │ Số tờ:
│ Xưởng: <…>         │ Ký hiệu chi tiết: <…>      │ Ký hiệu SP: <…>     │ Tờ số:
├──────────────────────────────────┬────────────────────────────────────┤
│ NGUYÊN CÔNG <k>: <tên>           │ Bậc thợ │ ĐM │ TL hỏng │ CN kiểm │ KCS kiểm │
├──────────────────────────────────┴────────────────────────────────────┤
│ YÊU CẦU KỸ THUẬT VÀ AN TOÀN                                            │
│  I. YÊU CẦU KỸ THUẬT:  <các bước…>                                      │
├──────────────────────┬──────────────────────────────────────────────────┤
│ Nguyên, vật liệu     │ Thiết bị, trang bị CN                            │
│ Tên gọi│Ký hiệu│S.lg │ Tên gọi│Ký hiệu│S.lg                            │
│  …                   │  …                                               │
├──────────────────────┴──────────────────────────────────────────────────┤
│ Xưởng trưởng │ An toàn │ Kiểm tra │ Công nghệ      <ô ký + Họ tên + ngày>│
├──────────────────────────────────────────────────────────────────────┤
│ S.đ│S.lg│Nội dung sửa đổi│Họ tên│Chữ ký│Ngày│Chịu trách nhiệm│…  (dòng sửa đổi)│
└──────────────────────────────────────────────────────────────────────┘
```

Các trường khối tiêu đề: Đơn vị, Xưởng, Tên chi tiết = tên SP, Ký hiệu tài liệu, Ký hiệu SP, Số tờ / Tờ số. Mỗi nguyên công là một tờ. Đây chính là cấu trúc form trong file QTCN gốc của Workshop X (vd Bia BM-01) — giữ nguyên để tương thích lưu trữ & ký duyệt.

---

## D. KHỐI MINH HỌA CAD trong mỗi nguyên công (khi `--cad`)

Chèn **mục IV** vào cuối mỗi nguyên công ở bản chi tiết. Skill đặc tả hình, họa viên vẽ trong CAD rồi thay `[ẢNH: …]` bằng hình thật. Chọn loại hình theo engineering-rules §9.

````markdown
### IV. Minh họa / Bản vẽ đề xuất
- **Mã hình:** H-<mã NC>          <!-- vd H-B3; nhiều hình → H-B7a, H-B7b -->
- **Loại hình:** <hình chiếu bằng | hình cắt trích + exploded | sơ đồ siết chữ X | detail cóc cáp | sơ đồ rigging | sơ đồ đấu nối DC | hình mớn nước…>
- **Thể hiện:** <nội dung chính — chi tiết VT nào, mối ghép nào, cụm nào>
- **Callout bắt buộc:** <lực siết / dung sai / quy cách ren×dài / thứ tự bộ đệm / hướng / khoảng cách> (số khớp mục I. YCKT)
- **Nguồn:** <mã bản vẽ trích, vd 19.BM-01.02.00 | "dựng mới">
- **Chỗ chèn:** [ẢNH: chèn hình CAD H-<mã NC> tại đây]
````

Ví dụ (NC B3 — lắp dầm ngang, môi trường biển):
````markdown
### IV. Minh họa / Bản vẽ đề xuất
- **Mã hình:** H-B3
- **Loại hình:** Hình cắt trích phóng to mối bích + exploded bộ đệm
- **Thể hiện:** Liên kết dầm ngang (VT2/3/4) – tai phao (VT1); xếp lớp bu lông M12×40
- **Callout bắt buộc:** M12×40; 2 đệm phẳng + 1 đệm vênh sát đai ốc; "GÁ LỎNG — chưa siết"; hướng biển tên ra ngoài
- **Nguồn:** 19.BM-01.02.00 / 03.00 / 04.00
- **Chỗ chèn:** [ẢNH: chèn hình CAD H-B3 tại đây]
````

---

## E. BẢN JSON KIỂM TRA QUY TRÌNH — `QTCN-<sp>.json` (khi `--json`)

Nguồn máy đọc để **đối soát/kiểm tra quy trình về sau** (verify / inspection / audit). Mọi con số khớp bản Markdown. `checkpoints[]` là phần cốt lõi (tiêu chí nghiệm thu định lượng); `cad_illustration` điền khi có `--cad`.

### Schema (rút gọn)
```json
{
  "product": { "code": "19.BM-01.00.00", "name": "...", "type": "...",
               "principal_particulars": { "Lpmax_mm": "3060 ± 20", "...": "..." } },
  "scope": "full | B",                       // "B" khi chạy --B (chỉ B+C)
  "cad_included": true,                        // true khi chạy --cad
  "standards": ["TCVN 1765:1975", "JIS G4303", "..."],
  "general_specs": { "torque": { "M12_8.8": "45-55 Nm", "M10_5.6": "25-30 Nm" },
                     "ip_rating": "IP67", "battery_voltage": "12-12.8 V",
                     "default_tolerance": "±IT14/2" },
  "bom": [ { "vt": "VT2", "drawing_no": "19.BM-01.02.00", "name": "Dầm liên kết ngang đầu phao",
             "qty": "01", "material": "Thép hợp kim EH32" } ],
  "operations": [
    {
      "id": "B3", "seq": 3, "phase": "B",
      "name": "Lắp đặt các dầm liên kết ngang (VT2, VT3, VT4) với phao bia — gá lỏng",
      "vt_refs": ["VT1","VT2","VT3","VT4"],
      "tech_requirements": [
        { "step": 1, "text": "Định vị dầm ngang theo sơ đồ; biển tên N-01/N-03 quay ra ngoài" },
        { "step": 2, "text": "Xỏ bu lông M12×40 từ trên xuống, đủ 2 đệm phẳng + 1 đệm vênh" }
      ],
      "core_rule": "TUYỆT ĐỐI CHƯA SIẾT CHẶT ở nguyên công này (gá lỏng)",
      "labor": { "grade": "4/7", "time_min": 40, "location": "Bãi lắp dựng ngoài trời" },
      "materials": [ { "name": "Bu lông M12×40 (≥5.6)", "vt": null, "qty": 48 },
                     { "name": "Vòng đệm vênh M12", "qty": 48 } ],
      "equipment": [ { "name": "Chốt côn rà lỗ", "spec": "Ø10÷Ø12", "qty": 2 } ],
      "checkpoints": [
        { "param": "sai lệch tâm lỗ bích", "nominal": "0", "tol": "±1", "unit": "mm", "method": "thước cặp/cuộn" },
        { "param": "trạng thái siết", "nominal": "gá lỏng (chưa siết lực)", "method": "kiểm tra bằng tay/quan sát" }
      ],
      "cad_illustration": {
        "required": true, "figure_id": "H-B3",
        "view_type": "hình cắt trích + exploded bộ đệm",
        "shows": "liên kết dầm ngang VT2/3/4 – tai phao VT1",
        "callouts": ["M12×40","2 đệm phẳng + 1 đệm vênh","GÁ LỎNG — chưa siết","hướng biển tên ra ngoài"],
        "source_drawing": "19.BM-01.02.00 / 03.00 / 04.00"
      }
    }
  ],
  "process_summary": [ { "seq": 3, "id": "B3", "name": "...", "grade": "4/7", "time_min": 40 } ],
  "safety": ["làm việc trên cao: dây đai an toàn", "nâng hạ: không đứng dưới vật treo", "..."]
}
```

### Quy ước
- `checkpoints[].param/nominal/tol/unit/method` **rút trực tiếp** từ mục I. YCKT — mỗi thông số định lượng (lực siết, dung sai, khoảng cách, điện áp, độ thẳng đứng, Δ đường chéo) thành 1 checkpoint để verify/inspection so khớp khi kiểm tra thực tế.
- `cad_illustration` bỏ trống (`{"required": false}`) nếu không chạy `--cad`.
- `scope="B"` ⇒ mảng `operations` chỉ chứa `phase` B và C; `phase="A"` bị loại.
- `id` ổn định (B3, C1…) để tham chiếu chéo giữa MD, JSON và file hình `figures/H-B3`.
