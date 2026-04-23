# Rules for 5_Galaxy/ folder

Galaxy là Zettelkasten — HOÀN TOÀN PHẲNG, KHÔNG subfolder.

## Before creating a Galaxy note
Verify 3-question quality gate:
1. Note trả lời ≥1 câu: (a) Thay đổi cách thiết kế? (b) Thay đổi quyết định chiến lược? (c) Cảnh báo tránh trap nào?
2. Note có ≥ 2 [[wikilinks]] tới notes khác trong Galaxy?
3. Note đã đủ atomic? (1 concept duy nhất, nếu > 300 words → có thể chưa atomic)

Nếu không pass → chưa đủ distilled, đừng tạo note.

## When creating a note
- File name: Tiếng Việt có dấu, descriptive (ví dụ: `Recoil Fidelity Threshold — 70% Lực Đủ Cho Training Transfer.md`)
- Viết bằng lời người dùng, KHÔNG copy-paste từ source
- Xác định note thuộc cluster nào (A-I) → link đến hub note của cluster + ≥1 cross-cluster link

## Frontmatter
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: permanent-note
tags: [#type/permanent-note, #topic/..., cluster-tag]
links: [[Note 1]], [[Note 2]]
---
```

## Galaxy tags
`#acq` (ACH) · `#sys` (systems) · `#pahl` (Pahl-Beitz) · `#defense` (VN defense) · `#product` (technical) · `#ceo` (leadership) · `#meta` (learning) · `#three-laws` (distilled laws) · `#warning` (traps)

## Content structure
1. **Ý Tưởng Cốt Lõi** — 1-3 câu tóm concept
2. **Giải Thích Chi Tiết** — mở rộng với ví dụ
3. **Tại Sao Điều Này Quan Trọng?** — relevance cho Workshop X
4. **Liên Kết** — wikilinks có annotation
5. **Nguồn Gốc** — citation + ngày gặp

## Hub notes (ưu tiên link đến)
- `Phán đoán không thể uỷ thác cho AI` (12+ links)
- `Physical-World Interface` (10+ links)
- `Shifting the Burden Archetype` (8+ links)
- `Nguyên Tắc Atomic Note` (8 links)

## KHÔNG BAO GIỜ
- Tạo subfolder trong Galaxy
- Chuyển Galaxy note sang Archives
- Gộp nhiều concepts vào 1 note
- Tạo note chỉ vì có analysis mới — phải distill trước
