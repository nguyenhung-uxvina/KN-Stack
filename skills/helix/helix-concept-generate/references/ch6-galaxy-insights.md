# Galaxy Permanent Notes — Phase 2 Conceptual Design Insights

These Galaxy notes contain distilled insights applicable during Phase 2.
Reference these notes at the indicated steps for deeper context.

---

## Core Phase 2 Notes

### [[Solution-Determining Subfunction — Không Phải Mọi Function Đều Bằng Nhau]]
**Apply at:** Step A1 (Solution-Determining SF Identification)
**Insight:** In any function structure, ONE subfunction determines the rest. Choose its WP → entire downstream design cascades. Solve it FIRST, decompose DEEP there, SHALLOW elsewhere.
**Example:** VN-12.7MM-SIM "Generate recoil force impulse" → choose pneumatic → cascades compressor, valve timing, cylinder, DfM, O-ring supply.
**Cluster:** G (Pahl-Beitz Technical)

### [[Two-Stage Evaluation Law — Pugh Nhanh Rồi VDI Sâu]]
**Apply at:** Step C1 (Pugh Screening)
**Insight:** Use Pugh matrix (4-6 criteria, +/S/-) to eliminate 50% fast, then VDI 2225 deep on survivors only. For solo CEO, each hour evaluating = hour not prototyping.
**Cluster:** G (Pahl-Beitz Technical)

### [[VDI 2225 — Sensitivity Analysis Kiểm Tra Robustness]]
**Apply at:** Step D5 (Sensitivity Analysis)
**Insight:** VDI score alone meaningless. Vary weights ±20-30% and check ranking stability. Winners with <5% lead need re-evaluation. Weights BEFORE scoring — choosing after = confirmation bias.
**Cluster:** G (Pahl-Beitz Technical)

### [[DSO Pre-Ranking — Performance × Risk Trước Khi Tổ Hợp]]
**Apply at:** Step B2 (DSO Pre-Ranking)
**Insight:** Score each WP individually (Performance 1-4 × Risk 1-4) before combining. Reduces 1,024 combinations to ~10-15 viable. DSO ≥12 strong, 6-11 viable, ≤5 avoid.
**Cluster:** G (Pahl-Beitz Technical)

### [[Interface Ownership — Đẩy Function Qua Biên Giới Hệ Thống]]
**Apply at:** Step B1 (Working Principles Search)
**Insight:** Before designing a function, ask "Who OWNS this?" Pushing it across interface boundary can collapse complexity more than any optimization. VN-XUONG-UUV: cable drum inside UUV → 9→1 subfunctions. But needs ICD to ensure other party handles it.
**Cluster:** G (Pahl-Beitz Technical)

### [[TRIZ × Pahl-Beitz — Contradiction Finder Nâng Innovation Level Từ 1-2 Lên 2-4]]
**Apply at:** Steps A2, B3, C5 (TRIZ throughout)
**Insight:** Pure P&B morphological matrix → Level 1-2 solutions. TRIZ-enhanced → Level 2-4 = real competitive differentiation. Use HOQ roof to detect contradictions → 40 Principles → tag solutions by level.
**Cluster:** G (Pahl-Beitz Technical)

### [[TESE Stalled Trend — Xu Hướng Tắc Nghẽn = Hướng Đổi Mới]]
**Apply at:** Step A3 (TESE Check)
**Insight:** Score product against 8 Altshuller evolution trends (1-5). Stalled trends (<3) = highest-leverage innovation direction. Defense ceilings: Macro→Micro ≤3, Dynamicity limited by VN manufacturing.
**Cluster:** G (Pahl-Beitz Technical)

---

## Supporting Notes

### [[Variation vs Simplification — Hai Triết Lý Phân Tích Chức Năng]]
**Apply at:** Block 0 (Design Type Detection)
**Insight:** P&B = decompose for VARIATION (explore widest solution space). Ulrich-Eppinger = decompose for SIMPLIFICATION (manageable teams). P&B for Original design, U-E for Adaptive. Knowing which = critical judgment.

### [[VDI 2221 Evolution — Khi Tiêu Chuẩn Thừa Nhận Waterfall Là Ảo Tưởng]]
**Apply at:** Throughout (iteration mindset)
**Insight:** New VDI 2221 officially rejects waterfall. Feedback loops EXPECTED. P&B is adaptive framework to CONFIGURE, not recipe to FOLLOW. Iterate freely with small loops.

### [[Phán đoán không thể uỷ thác cho AI]]
**Apply at:** Steps B6, E3 (Human creativity, CEO selection)
**Insight:** Hub note (12+ links). Core judgment decisions — concept selection, novel WP creation, design direction — cannot be delegated to AI. AI generates options; human decides.
**Cluster:** C (Judgment & Agency)

### [[Physical-World Interface]]
**Apply at:** Steps C2, D4 (Firming up, CFMA)
**Insight:** Hub note (10+ links). All concepts must eventually interface with physical reality. Firming up with F3-F4 methods (experiments, models) grounds abstract concepts.
**Cluster:** C (Judgment & Agency)

### [[6-Fold Symmetry — Omnidirectional Stability]]
**Apply at:** Step B1 (Working Principles — marine products)
**Insight:** For seagoing platforms, 6-fold symmetry optimal for omnidirectional wave stability. Avoids weak axes of 4-pontoon designs. Symmetry of structure must match symmetry of loads (P&B 7.3.1).
**Cluster:** H (Physical Design)

### [[Flexibility Là Output, Không Phải Input]]
**Apply at:** Throughout (methodology mindset)
**Insight:** P&B's strict 4 phases don't LIMIT creativity — they CHANNEL it. Phase 2 = creative phase. Framework RIGID → flexibility in execution AUTOMATIC. "Be flexible" is bad advice; "be flexible ABOUT instruments within rigid framework" is good.

---

## Quick Lookup: Galaxy Note → Skill Step

| Galaxy Note | Skill Step |
|------------|-----------|
| Solution-Determining SF | A1 |
| TRIZ × Pahl-Beitz | A2, B3, C5 |
| TESE Stalled Trend | A3 |
| Interface Ownership | B1 |
| DSO Pre-Ranking | B2 |
| Variation vs Simplification | Block 0 |
| Two-Stage Evaluation Law | C1 |
| VDI 2225 Sensitivity | D5 |
| Phán đoán không thể uỷ thác | B6, E3 |
| Physical-World Interface | C2, D4 |
| VDI 2221 Evolution | Throughout |
| Flexibility Là Output | Throughout |
