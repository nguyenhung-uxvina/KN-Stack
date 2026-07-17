# Định mức Kinh tế – Kỹ thuật (ĐMKTKT) — Rules & Template

Sinh tài liệu **Định mức kinh tế – kỹ thuật** cho một sản phẩm từ **Data Spine** + **QTCN.json**. Ba trụ: **định mức vật tư**, **định mức lao động**, **định mức máy/thiết bị** → quy ra **đơn giá & giá thành**.

> Nguyên tắc: định mức = *lượng hao phí cho 1 đơn vị sản phẩm*. Số **kỹ thuật** (khối lượng, giờ công) rút tự động từ spine/QTCN; số **kinh tế** (đơn giá) do CEO/phòng kế hoạch chốt — thiếu thì để `[CẦN ĐƠN GIÁ]`, **không bịa**.

---

## 1. Định mức vật tư (material norms)

### 1.1 Vật tư chính (kết cấu) — từ `spine.bom`
Mỗi chi tiết: khối lượng tịnh (est_mass_kg) + **hao hụt** theo dạng gia công.

| Dạng vật tư | Cách tính lượng | Hao hụt định hướng |
|-------------|-----------------|--------------------|
| Thép tấm (EH32, tấm 15mm) | m = ρ·(diện tích×dày), ρ=7,85 | cắt CNC 3–8% (nesting) |
| Thép hình L/hộp (L40×40×4, 30×60×1,8) | m = khối lượng mét dài × tổng dài | cắt 2–5% |
| Composite (thân phao, khuôn) | vải+nhựa theo số lớp×diện tích | 10–15% |
| Gỗ (hõm gỗ) | thể tích phôi | 10–20% |

### 1.2 Vật tư phụ / tiêu hao — từ `spine.consumables` + định mức tiêu hao
- Bu lông/đai ốc/đệm/cáp/ma ní/tăng đơ/LED/ắc quy: lấy **số lượng** từ consumables (đối soát QTCN).
- Que hàn/dây hàn: ~ (chiều dài mối × tiết diện) hoặc định mức kg/kg kết cấu (định hướng 1–3%).
- Sơn: chống gỉ + phủ ghi = diện tích bề mặt × định mức (m²/lít) × số lớp.
- Khí bảo vệ, đá mài, hóa chất NDT (PT), băng keo, mỡ… theo định mức tiêu hao.

**Bảng ĐM vật tư (mẫu):**
| TT | Vật tư | Mã VT/BV | Quy cách | ĐVT | Định mức/SP | Hao hụt | Đơn giá | Thành tiền |
|----|--------|----------|----------|-----|-------------|---------|---------|-----------|
| 1 | Thép hợp kim EH32 (dầm ngang) | VT2/19.BM-01.02.00 | tấm | kg | `<est>` | 5% | `[CẦN ĐƠN GIÁ]` | |
| 2 | Bu lông M12×40 | — | ≥8.8 | cái | 64 | — | | |
| … | | | | | | | | **Σ vật tư** |

## 2. Định mức lao động (labor norms) — từ `QTCN.json.operations[]`
- Mỗi nguyên công: `time_min` → **giờ công = time_min/60**, gắn **bậc thợ** (`labor.grade`).
- Nhóm theo bậc thợ để áp đơn giá giờ công theo bậc.

**Bảng ĐM lao động (mẫu):**
| TT | Nguyên công | Mã NC | Bậc thợ | Giờ công | Đơn giá giờ (đ/h) | Thành tiền |
|----|-------------|-------|:------:|:--------:|:-----------------:|-----------|
| 1 | Lắp dầm ngang | B3 | 4/7 | 0,67 | `[CẦN ĐƠN GIÁ]` | |
| … | | | | | | |
| | **Tổng** | | | `<Σ giờ công>` | | **Σ nhân công** |

> Tổng giờ công = Σ `time_min`/60 toàn bộ nguyên công (khớp `QTCN.json.total_time_min`).

## 3. Định mức máy / thiết bị (machine-hour) — từ `equipment[]`
- Thiết bị chính có ca máy (cắt CNC, cần cẩu, máy hàn, xe nâng): ước **giờ máy** theo nguyên công dùng nó.
- Dụng cụ cầm tay/BHLĐ: tính vào chi phí chung, không lập ca máy riêng.

**Bảng ĐM máy (mẫu):** TT | Thiết bị | Nguyên công dùng | Giờ máy | Đơn giá ca/giờ | Thành tiền.

## 4. Tổng hợp giá thành 1 sản phẩm
| Khoản mục | Thành tiền | Ghi chú |
|-----------|-----------|---------|
| A. Vật tư chính | | §1.1 |
| B. Vật tư phụ/tiêu hao | | §1.2 |
| C. Nhân công | | §2 |
| D. Máy/thiết bị | | §3 |
| E. Chi phí chung (%·(A..D)) | | định hướng 10–20% |
| **Giá thành sản xuất = A+B+C+D+E** | | |
| Lãi định mức / thuế (nếu lập giá bán) | | CEO chốt |

- Có thể lập **theo sản lượng** (1 / 10 / 50 SP): vật tư ~ tuyến tính; nhân công giảm nhờ đường cong học tập; khấu hao đồ gá/khuôn phân bổ theo lô. Nối `lcc` để ra LCC 5 năm & đối chiếu nhập ngoại (≤70%).

## 5. Đầu ra
- `DMKTKT-<sp>.md` — 3 bảng định mức + bảng tổng hợp giá thành, mọi số truy về spine/QTCN, ô đơn giá `[CẦN ĐƠN GIÁ]` nếu chưa có.
- `DMKTKT-<sp>.json` — máy đọc: `{ product, material_norms[], labor_norms[], machine_norms[], cost_summary }`, để đối soát & tính lại khi có đơn giá.

## 6. Chống sai
- **Không bịa đơn giá/hao hụt**: chưa có → placeholder + liệt kê ở "Mục cần CEO".
- Khối lượng est_mass là **ước lượng** trừ khi title block ghi — đánh dấu Low confidence, ưu tiên số cân thực khi có.
- Số lượng bu lông/vật tư phụ phải **khớp QTCN** (vd M12 = 64) — lệch thì sửa ở spine trước.
