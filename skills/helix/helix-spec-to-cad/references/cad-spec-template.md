# Part Spec — {{project}} / {{part_id}}

> **Vai trò:** Đặc tả part theo SDD (mượn spec-template của GitHub spec-kit, bản địa hóa cơ khí).
> Nguyên tắc thép (Điều IV Constitution): **mọi FR phải có SỐ + ĐƠN VỊ**. Số thiếu = đánh dấu
> `[NEEDS CLARIFICATION: câu hỏi]` — TỐI ĐA 3 marker, mỗi marker trình CEO bằng option table.
> Spec chỉ được duyệt khi **zero marker**.

**Part:** {{part_id}} · **Project:** {{project}} · **Rev:** {{rev}} · **Status:** [DRAFT | CLARIFYING | APPROVED]
**Classification:** {{label}} (READ-ONLY — từ constitution) · **Input:** "{{$ARGUMENTS — mô tả gốc của CEO}}"

---

## 1. Purpose & Mounting Context (user story)

Là {{cụm lắp / assembly}}, part này phải {{chức năng chính}} để {{lý do tồn tại}}.

**Acceptance scenarios (Given/When/Then, per interface):**
1. **Given** {{trạng thái lắp}}, **When** {{tải/thao tác}}, **Then** {{kết quả đo được}}
2. ...

## 2. Envelope & Datums

| Item | Giá trị | Đơn vị | Nguồn |
|---|---|---|---|
| Envelope (L×W×H max) | {{a×b×c}} | mm | {{ICD / CEO}} |
| Datum A | {{mặt/trục}} | — | {{sketch callout}} |
| Datum B | {{...}} | — | |
| Datum C | {{...}} | — | |

## 3. Interfaces (mating)

| IF | Đối tượng giao tiếp | Kiểu (mặt phẳng/lỗ/ren…) | Kích thước then chốt | Fastener |
|---|---|---|---|---|
| IF-01 | {{part đối diện}} | {{...}} | {{Ø, pitch, khoảng cách tâm}} | {{M6×…}} |

## 4. Functional Requirements

> Mỗi FR: số + đơn vị + nguồn. Không số → `[NEEDS CLARIFICATION]`, không đoán.

| ID | Yêu cầu | Giá trị | Đơn vị | Nguồn | Ghi chú |
|---|---|---|---|---|---|
| FR-001 | {{...}} | {{n}} | mm | CEO | |
| FR-002 | {{...}} | {{n}} | kg | budget | |

## 5. Material & Finish

- Vật liệu: {{...}} (phải thuộc whitelist Điều V constitution)
- Xử lý bề mặt: {{anodize/sơn/để trần…}}

## 6. Mass Budget

- `mass_kg.max` = {{n}} kg (khớp Machine-Checkable Extract)

## 7. Tolerances

- Dung sai chung: {{ISO 2768-m / ±0.x mm}}
- Critical dims (dung sai riêng): {{FR-ref → giá trị}}

## 8. DFM Constraints

- Min wall: {{n}} mm · Min hole-to-edge: {{n}} mm · Fillet policy: {{...}}
- Quy trình chế tạo dự kiến: {{cắt laser/phay/chấn…}}

## 9. `[NEEDS CLARIFICATION]` (tối đa 3)

> Mỗi marker = 1 option table, có default đề xuất. CEO chọn → xóa marker, ghi số vào FR.

### NC-1: {{câu hỏi}}
| Option | Giá trị | Ưu | Nhược |
|---|---|---|---|
| A (đề xuất) | {{...}} | {{...}} | {{...}} |
| B | {{...}} | {{...}} | {{...}} |

## 10. Success Criteria (đo được, technology-agnostic)

| ID | Tiêu chí | Cách đo |
|---|---|---|
| SC-001 | Bounding box ≤ envelope | mass-props report từ helix-cad-bridge |
| SC-002 | Mass ≤ {{n}} kg | mass-props report |
| SC-003 | `validate.py` exit 0 (contract approved-hash) | helix-s2c-validate |
| SC-004 | CEO render check ✔ (PNG khớp intent) | Spatial Blindness gate |

## 11. Assumptions

- {{giả định 1 — điều được coi là đúng nếu CEO không nói khác}}
