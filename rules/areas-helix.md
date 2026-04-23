# Rules for 2_Areas/HELIX — Design Execution/

HELIX là current binding constraint (~29% theo Blueprint).
Mọi cải thiện ở đây = high-leverage.

## Physical-Validation-Log
File: `2_Areas/HELIX — Design Execution/Physical-Validation/Monthly-Log.md`

Format:
```
## Tháng [X] [Year]
- Prototype iterations: [số]
- Products có physical test: [danh sách]
- Products zero physical activity: [danh sách — cảnh báo đỏ nếu > 2]
- dP/dt vs tháng trước: ↑ / ↓ / =
```

Rules:
- Cập nhật ngay khi có test result mới
- Nếu "zero activity" list > 2 products → flag trong `_meta/system-health.md`
- Nếu dP/dt = 0 trong tháng hiện tại → cảnh báo CEO ngay lập tức

## Analyst Trap Guard
⚠️ Trước khi tạo thêm analysis/framework content trong HELIX:
Hỏi: "Hành động này tạo ra physical validation data, hay thêm analytical content?"
Nếu chỉ analytical → cảnh báo CEO và đề xuất physical alternative.

## Design-Review-Log
- Record mọi design review với: date, product, phase, findings, actions
- Link đến `_meta/decisions.md` cho significant decisions

## Khi làm việc trong HELIX
- Ưu tiên tasks liên quan đến physical prototype/test
- AI Orchestration tasks = Offload (COD)
- Design decisions = Core (CEO judgment)
- Physical-Validation tracking = Core (CEO must input real data)
