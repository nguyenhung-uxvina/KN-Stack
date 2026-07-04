# Feature-Tree Tasks — {{project}} / {{part_id}}

> **Vai trò:** Danh sách thao tác dựng hình có thứ tự phụ thuộc (mượn tasks-template của
> GitHub spec-kit). Format: `[ID] [P?] [FR-ref]` — `[P]` = parallelizable (feature độc lập,
> không chung edge/face với feature khác trong cùng phase).
> **Plan nguồn:** `{{prefix}}S2C_Plan.md` (APPROVED, Constitution Check PASS)

---

## Phase S — Setup
- [ ] T001 — Khai parameter block từ Parameter Table của Plan (toàn bộ số CEO, zero magic number) `[FR-all]`

## Phase F — Foundational (SERIAL — mỗi op tiêu thụ solid của op trước)
- [ ] T002 — Sketch profile trên Datum A `[FR-001]`
- [ ] T003 — Extrude → base solid; assert bbox ≤ envelope `[FR-001, SC-001]`

## Phase D — Detail features ([P] khi không chung edge/face)
- [ ] T004 [P] — {{hole pattern 1, datum-referenced}} `[FR-003]`
- [ ] T005 [P] — {{hole pattern 2 / slot / pocket}} `[FR-004]`

## Phase L — Late ops (order-sensitive — fillet/chamfer LUÔN sau holes)
- [ ] T006 — Fillets {{R}} + chamfer mép lỗ {{c×45°}} `[FR-005]`

## Phase E — Export & self-check
- [ ] T007 — Export `{{part_id}}.step` + render PNG (iso + 3 ortho) `[SC-001]`
- [ ] T008 — Mass-props report + sanity asserts (wall ≥ min DFM, no zero-volume) `[SC-002]`

---

## Dependencies & Execution Order
- S → F → D → L → E. Trong D, các task `[P]` chạy được song song (feature độc lập trên base đã đóng băng).
- T006 phụ thuộc TOÀN BỘ Phase D (fillet sau cùng — đổi thứ tự làm hỏng edge selection).

## Rules
- Mỗi kích thước trong task trace về 1 param của Parameter Table (không số rời).
- `[P]` CHỈ gắn khi hai feature không chung edge/face/vertex.
- Một part một run — multi-part = loop pipeline theo part, không merge.
- Fillet/chamfer luôn ở Phase L, sau mọi hole/pocket.
