# Parametric Plan — {{project}} / {{part_id}}

> **Vai trò:** Kế hoạch dựng hình tham số từ Spec đã duyệt (mượn plan-template + Constitution
> Check gate của GitHub spec-kit). Plan chỉ được duyệt khi **Constitution Check toàn PASS**
> (hoặc vi phạm có justification trong Complexity Tracking được CEO chấp nhận).

**Part:** {{part_id}} · **Rev:** {{rev}} · **Spec:** `{{prefix}}S2C_Spec.md` (APPROVED, zero marker)

---

## 1. Technical Context

| Item | Giá trị |
|---|---|
| Backend | build123d (mặc định — theo helix-cad-bridge) |
| Units | mm, 1:1 |
| Export | STEP AP214 + PNG (isometric + 3 ortho) + mass-props JSON |
| Runtime | 100% LOCAL, offline (Điều II) |
| Classification | {{label}} (READ-ONLY) |

## 2. Constitution Check (GATE — phải PASS trước khi sang tasks)

| Điều | Nội dung | PASS/VIOLATION | Ghi chú |
|---|---|---|---|
| I | Metric-only, mm 1:1 | | |
| II | Local/air-gapped, không SaaS CAD | | |
| III | Label đọc từ constitution, egress guard | | |
| IV | Không số bịa — mọi param trace về FR/sketch | | |
| V | Vật liệu thuộc whitelist | | |
| VI | Mass budget + safety factor khai trong design_rules | | |
| VII | DFM: min wall / hole-to-edge / fillet đạt | | |
| VIII | Kế hoạch exit qua validate PASS + render check + KS ký | | |

## 3. Parameter Table (data model — mọi số trace về FR)

> Nguyên tắc: KHÔNG magic number. Mỗi param một dòng, driven-by rõ ràng.

| Param | Symbol | Value | Unit | Driven by |
|---|---|---|---|---|
| {{chiều dài đế}} | `base_l` | {{n}} | mm | FR-001 |
| {{độ dày}} | `t` | {{n}} | mm | FR-002 / Điều V kho tấm |

## 4. Feature-Tree Outline

```
1. Sketch profile trên Datum A          ← FR-001
2. Extrude → base solid                 ← FR-002
3. Hole pattern(s)                      ← IF-01 / FR-003
4. Fillets / chamfers (LUÔN CUỐI)       ← FR-005 / Điều VII
5. Export STEP + PNG + mass-props
```

## 5. Complexity Tracking

> Chỉ có nội dung khi Constitution Check có VIOLATION được CEO chấp nhận.

| Vi phạm | Điều | Justification | CEO chấp nhận? |
|---|---|---|---|

## 6. Risks (spatial)

| Risk | Quan hệ không gian cần CEO sketch callout | Mitigation |
|---|---|---|
| {{ví dụ: lỗ đồng trục với trục lắp}} | {{callout #}} | trace trong code comment, CEO kiểm PNG |
