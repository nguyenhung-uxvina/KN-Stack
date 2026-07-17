# Product Dossier — Khối pipeline & Data Spine (reference)

Chi tiết thực thi từng pha, schema `product-spine.json`, và cách mỗi khối P4 tiêu thụ spine. Đọc cùng SKILL.md.

---

## §Spine — Schema `product-spine.json`

Nguồn sự thật duy nhất. Hợp nhất từ per-sheet JSON (mech-drawing-extract) + trang bảng kê.

```json
{
  "product": {
    "code": "19.BM-01.00.00",
    "name": "Bia bắn súng bộ binh BM-01",
    "type": "...",
    "principal_particulars": { "Lpmax_mm": "3060 ± 20", "...": "..." }
  },
  "source_dir": "D:\\...\\Bia BM-2025-PDF-DXF",
  "extracted_at": "YYYY-MM-DD",
  "units": "mm",
  "sheets": [ { "sheet": "Trang-3", "drawing_no": "19.BM-01.00.00", "role": "assembly|bom|detail",
               "json": "extracted/trang-3.json" } ],
  "bom": [
    { "vt": "VT2", "drawing_no": "19.BM-01.02.00", "name": "Dầm liên kết ngang đầu phao",
      "qty": "01", "material": "Thép hợp kim EH32",
      "specs": { "sections": ["L40×40×4"], "plate_mm": null, "key_dims": ["..."],
                 "est_mass_kg": null, "surface_area_m2": null } }
  ],
  "consumables": [ { "name": "Bu lông M12×40", "qty_total": 64, "note": "B3:48+B4:12+B7:4" } ],
  "relationships": [ { "a": "VT2", "b": "VT1", "joint": "bu lông M12×40", "count": 48 } ],
  "flags": { "pdf_scanned": true, "tcvn3": true, "mojibake_pdf": true }
}
```

**Quy tắc lập spine:**
- `bom[].vt` là khóa xuyên suốt; nếu bản vẽ chưa có VT, gán VT1..VTn theo thứ tự bảng kê và ghi lại mapping.
- `specs.est_mass_kg`: ước lượng khi có đủ hình học — `mass = ρ×V` (thép 7,85; nhôm 2,66; composite ~1,7; gỗ thông ~0,5 g/cm³). Đánh dấu là **ước lượng** (Low confidence) trừ khi title block ghi khối lượng.
- `sections`/`plate_mm`: rút từ tên vật liệu BOM (vd "thép hộp 30×60×1,8", "thép tấm 15 mm", "L40×40×4") và từ dims DXF.
- `consumables`: bu lông/đai ốc/đệm/cáp/lạt… gộp toàn sản phẩm (đối soát với QTCN sau).
- Giữ `flags` để tài liệu sau biết độ tin dữ liệu (PDF scan ⇒ nhiều mục cần đọc tay/`[CẦN …]`).

---

## §P0 — Preflight
1. Quét thư mục: nhóm theo phần mở rộng; ghép `Trang-N.pdf`↔`Trang-N.dxf`; đánh dấu `.dwg` (sẽ auto-convert qua ODA trong parser).
2. Nếu 1 DWG gói cả sản phẩm nhiều tờ → dùng kỹ thuật tách sheet-frame của mech-drawing-extract (INSERT khung in) trước khi parse.
3. Đoán tên/mã sản phẩm từ tiêu đề bản lắp hoặc tên thư mục; **xác nhận CEO**.

## §P1 — Extract (chọn engine theo loại file)
- **2D (PDF/DXF/DWG-2D):** `parse_mech_drawing.py` — chữ/dims/dung sai/TCVN3. Ưu tiên DXF cho hình học; PDF cho title block (nếu không scan/mojibake).
- **3D (STEP/IGES/FCStd/DWG-3D):** [D:/WX-Pipeline/scripts/extract/freecad_extract.py](../../../../D:/WX-Pipeline/scripts/extract/freecad_extract.py) qua `freecadcmd` — **khối lượng thật** (V×ρ) + bao hình + BOM lắp ráp, xuất thẳng `qtcn-seed.json` (`est_mass_kg` thật, hết `[CẦN BÓC TÁCH]`). Có thể **gộp** seed 3D (khối lượng) với seed 2D (VT/mã bản vẽ/dung sai/vật tư mua) khi có cả hai.
- Đọc **trang bản lắp / bảng kê** đầu tiên → dựng `bom[]` (Kí hiệu/Tên gọi/Số lượng/Vật liệu). Đây là index của cả sản phẩm.
- Ghi cờ chất lượng (`pdf_scanned`, `tcvn3`, `mojibake_pdf`) vào spine.

## §P2 — Spine
- **Codified:** chạy cầu nối [D:/WX-Pipeline/scripts/extract/extract_to_qtcn_seed.py](../../../../D:/WX-Pipeline/scripts/extract/extract_to_qtcn_seed.py) `--extracted <extracted/>` → **`qtcn-seed.json`** (product + BOM có VT gán sẵn + section/plate/tolerances/key-dims mỗi chi tiết + vật tư mua + flags). Đây là **lõi của spine** — biến đổi tất định, không nhập tay.
- Map mỗi DXF ↔ dòng BOM theo **mã bản vẽ** (cầu nối đã tin mã trong MTEXT hơn tên file).
- (nếu cần) bổ sung `relationships` (mối ghép) và `est_mass` vào spine — phần này skill suy luận, không có trong seed.
- Kết xuất `product-spine.json` (= `qtcn-seed.json` + relationships + est_mass). Rà nhanh: tổng SL, vật liệu, mục thiếu. **`qtcn-seed.json` chính là đầu vào `--seed` cho khối 1 (QTCN).**

---

## §Menu — Khối P4 (cách tiêu thụ spine)

### Khối 1 — QTCN (`qtcn`)
- Gọi skill `qtcn` với **`--seed qtcn-seed.json`** (nền tảng từ P2) — BOM+VT+specs nạp sẵn, không nhập tay; + spine.relationships.
- Hỏi CEO: **phạm vi** (mặc định full A+B+C; hoặc `--B` lắp ráp+thử/bàn giao). Luôn bật **`--cad --json`** để có checkpoint + minh họa nuôi các khối sau.
- Xuất `QTCN-<sp>-*.md` (+ `.json`). **`QTCN.json` là đầu vào bắt buộc cho khối 2, 3, 6.**

### Khối 2 — ĐMKTKT (`dmktkt`) — xem dmktkt-template.md
- **Định mức lao động** = từ `QTCN.json.operations[].labor.time_min` × bậc thợ → giờ công/nguyên công → tổng giờ công.
- **Định mức vật tư** = từ `spine.bom` (khối lượng thép/composite/gỗ = est_mass + hao hụt) + `spine.consumables` (bu lông, cáp, sơn, que hàn, LED, ắc quy…) + định mức tiêu hao (que hàn/kg mối, sơn/m²…).
- **Đơn giá & giá thành** = định mức × đơn giá (CEO nhập; thiếu → `[CẦN ĐƠN GIÁ]`). Ra bảng giá thành 1 sản phẩm (± theo sản lượng).

### Khối 3 — Sổ tay QLCL (`qms`) — xem qms-template.md
- **Quality Plan** = mỗi `QTCN.json.operations[].checkpoints[]` → 1 dòng control plan: nguyên công | đặc tính KT | tiêu chuẩn/dung sai | phương pháp KT | dụng cụ | tần suất | hồ sơ | người KT.
- Cộng chính sách chất lượng, sơ đồ quá trình (từ QTCN flow), kiểm soát NDT/nghiệm thu, biểu mẫu, xử lý sản phẩm KPH, truy xuất theo VT/mã bản vẽ.

### Khối 4 — BOM (`bom`)
- `spine.bom` → bảng BOM chuẩn (MIL-STD flag, local-content ≥60%, rủi ro chuỗi cung nếu chạy `bom`/`lcc`).

### Khối 5 — LCC / đơn giá (`lcc` / `forge-cost`)
- Dùng ĐMKTKT (khối 2) + `spine.bom` → giá thành đơn vị + LCC 5 năm + đối chiếu nhập ngoại (≤70%).

### Khối 6 — Phiếu kiểm tra – nghiệm thu (`verify` / `helix-p4-inspection`)
- `QTCN.json.checkpoints[]` (định lượng) → phiếu kiểm tra: đặc tính | tiêu chuẩn | phương pháp | dụng cụ | kết quả | đạt/không.

### Khối 7 — Datasheet chi tiết (`mech-drawing-extract`)
- Mỗi per-sheet JSON → datasheet MD (title block, bảng dims, GD&T, cờ tin cậy).

### Cờ DOCX
- `convert_md_to_docx` cho mỗi MD đã chọn → bản in/ký. QTCN có thể dựng thêm form xưởng (qtcn-templates §C).

---

## §P5 — INDEX.md (mục lục hồ sơ)

```markdown
# HỒ SƠ SẢN PHẨM — <Tên SP> (<mã>)
> Nguồn: <thư mục> | Lập: <ngày> | Spine: product-spine.json

## Tài liệu đã xuất
| # | Tài liệu | File | Trạng thái |
|---|----------|------|-----------|
| 1 | Quy trình công nghệ | QTCN-...md/.json | ✅ |
| 2 | Định mức KT-KT | DMKTKT-...md | ⚠️ [CẦN ĐƠN GIÁ] |
| 3 | Sổ tay QLCL | SO-TAY-QLCL-...md | ✅ |
| … | | | |

## Số liệu chốt
- Số chi tiết: <n> | Tổng giờ công: <…> | Số checkpoint: <…> | Giá thành/SP: <… hoặc [CẦN ĐƠN GIÁ]>

## Mục còn chờ CEO
- <đơn giá, dung sai chốt, tiêu chuẩn nghiệm thu…>
```

Mọi tài liệu liên kết tương đối trong `HO-SO-SAN-PHAM\`. Spine + QTCN.json luôn kèm để đối soát/kiểm tra về sau.
