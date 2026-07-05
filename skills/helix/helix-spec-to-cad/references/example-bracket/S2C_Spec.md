# Part Spec — DEMO-BRACKET / l-bracket (GOLDEN EXAMPLE)

**Part:** l-bracket · **Rev:** A · **Status:** APPROVED (zero marker)
**Classification:** THƯỜNG · **Input:** "L-bracket nhôm gắn hộp điều khiển lên vách, 4 lỗ bulông M6"

## 1. Purpose & Mounting Context
Là cụm gá hộp điều khiển, part này phải đỡ hộp 1.5 kg lên vách thẳng đứng để cố định thiết bị demo.
1. **Given** bracket bắt 2 bulông M6 vào vách, **When** treo hộp 1.5 kg lên cánh ngang, **Then** không biến dạng nhìn thấy, bulông không chạm mép lỗ.

## 2. Envelope & Datums
| Item | Giá trị | Đơn vị | Nguồn |
|---|---|---|---|
| Envelope L×W×H | 100×80×60 | mm | CEO |
| Datum A | mặt đứng (bắt vách) | — | sketch #1 |
| Datum B | mặt ngang (đỡ hộp) | — | sketch #1 |
| Datum C | cạnh trái | — | sketch #1 |

## 3. Interfaces
| IF | Đối tượng | Kiểu | Kích thước then chốt | Fastener |
|---|---|---|---|---|
| IF-01 | vách | 2× lỗ suốt | Ø6.6, tâm cách 60 mm, cách mép trên 15 mm | M6 |
| IF-02 | hộp điều khiển | 2× lỗ suốt | Ø6.6, tâm cách 60 mm, cách mép ngoài 20 mm | M6 |

## 4. Functional Requirements
| ID | Yêu cầu | Giá trị | Đơn vị | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| FR-001 | Cánh đứng L×H | 100×60 | mm | CEO | trên Datum A |
| FR-002 | Cánh ngang L×W | 100×80 | mm | CEO | trên Datum B |
| FR-003 | Độ dày tấm | 6 | mm | Điều V kho tấm | |
| FR-004 | Lỗ IF-01: 2× Ø6.6, tâm cách 60, mép trên 15 | Ø6.6 | mm | IF-01 | clearance M6 |
| FR-005 | Lỗ IF-02: 2× Ø6.6, tâm cách 60, mép ngoài 20 | Ø6.6 | mm | IF-02 | clearance M6 |
| FR-006 | Fillet góc trong L | R6 | mm | DFM Điều VII | giảm tập trung ứng suất |

## 5. Material & Finish — Al 6061-T6 (whitelist ✅), anodize trong.
## 6. Mass Budget — mass_kg.max = 0.25 kg (t=6 toàn khối ≈ 0.217 kg thực đo — budget 0.20 ban đầu bị chính pipeline bắt vượt, CEO nâng lên 0.25 trong clarify loop).
## 7. Tolerances — chung ISO 2768-m; tâm lỗ ±0.2 mm.
## 8. DFM — min wall 3 ✅ (t=6); hole-to-edge ≥ 1.5×Ø6.6=9.9 → 15/20 ✅; cắt laser + chấn.

## 9. `[NEEDS CLARIFICATION]` — 0/3 (đã giải trong clarify loop)
> Lịch sử: NC-1 "lỗ clearance hay ren?" → CEO chọn A: clearance Ø6.6 (đề xuất).

## 10. Success Criteria
| ID | Tiêu chí | Cách đo |
|---|---|---|
| SC-001 | BBox ≤ 100×80×60 mm | mass-props report |
| SC-002 | Mass ≤ 0.25 kg | mass-props report |
| SC-003 | validate.py exit 0 (hash-OK) | helix-s2c-validate |
| SC-004 | CEO render check ✔ | Spatial Blindness gate |

## 11. Assumptions — tải tĩnh 1.5 kg, không rung động; trong nhà, không cần chống mặn.
