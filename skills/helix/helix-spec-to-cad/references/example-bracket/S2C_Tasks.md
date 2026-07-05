# Feature-Tree Tasks — DEMO-BRACKET / l-bracket (GOLDEN EXAMPLE)

> Plan nguồn: S2C_Plan.md (APPROVED, Constitution Check 8/8 PASS)

## Phase S — Setup
- [x] T001 — Khai parameter block: `L, W, H, t, hole_d, hole_cc, edge_wall, edge_shelf, fillet_r, rho` `[FR-all]`

## Phase F — Foundational (SERIAL)
- [x] T002 — Sketch L-profile (đứng 100×60, ngang 100×80, t=6) trên Datum A `[FR-001/002/003]`
- [x] T003 — Extrude L=100 → base solid; assert bbox ≤ 100×80×60 `[FR-001, SC-001]`

## Phase D — Detail features
- [x] T004 [P] — Hole IF-01: 2× Ø6.6 cánh đứng, tâm cách 60, mép trên 15 `[FR-004]`
- [x] T005 [P] — Hole IF-02: 2× Ø6.6 cánh ngang, tâm cách 60, mép ngoài 20 `[FR-005]`

## Phase L — Late ops
- [x] T006 — Fillet R6 góc trong L `[FR-006]` (phụ thuộc toàn bộ Phase D)

## Phase E — Export & self-check
- [x] T007 — Export `l-bracket.step` + render PNG iso + 3 ortho `[SC-001]`
- [x] T008 — Mass-props JSON + asserts (mass ≤ 0.25 kg; no zero-volume) `[SC-002]`

## Dependencies
S → F → D → L → E. T004/T005 song song (hai mặt khác nhau, không chung edge). T006 sau D.
