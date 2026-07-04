# Parametric Plan — DEMO-BRACKET / l-bracket (GOLDEN EXAMPLE)

**Part:** l-bracket · **Rev:** A · **Spec:** S2C_Spec.md (APPROVED, zero marker)

## 1. Technical Context
| Item | Giá trị |
|---|---|
| Backend | build123d |
| Units | mm, 1:1 |
| Export | STEP AP214 + PNG (iso + 3 ortho) + mass-props JSON |
| Runtime | 100% LOCAL, offline |
| Classification | THƯỜNG (READ-ONLY) |

## 2. Constitution Check (GATE)
| Điều | Nội dung | PASS/VIOLATION | Ghi chú |
|---|---|---|---|
| I | Metric-only | PASS | mm toàn bộ |
| II | Local/air-gapped | PASS | build123d local |
| III | Label + egress guard | PASS | THƯỜNG |
| IV | Không số bịa | PASS | 100% param driven-by-FR |
| V | Vật liệu whitelist | PASS | Al 6061-T6, tấm 6 mm kho |
| VI | Mass budget | PASS | thực đo 0.217 kg < 0.25 |
| VII | DFM | PASS | wall 6≥3; edge 15/20 ≥ 9.9; R6 ≥ R3 |
| VIII | Exit qua validate+render+KS | PASS | kế hoạch BE |

## 3. Parameter Table
| Param | Symbol | Value | Unit | Driven by |
|---|---|---|---|---|
| Chiều dài | `L` | 100 | mm | FR-001/002 |
| Rộng cánh ngang | `W` | 80 | mm | FR-002 |
| Cao cánh đứng | `H` | 60 | mm | FR-001 |
| Độ dày | `t` | 6 | mm | FR-003 |
| Đường kính lỗ | `hole_d` | 6.6 | mm | FR-004/005 |
| Khoảng tâm lỗ | `hole_cc` | 60 | mm | IF-01/02 |
| Lỗ vách cách mép trên | `edge_wall` | 15 | mm | FR-004 |
| Lỗ hộp cách mép ngoài | `edge_shelf` | 20 | mm | FR-005 |
| Fillet góc trong | `fillet_r` | 6 | mm | FR-006 |
| Khối lượng riêng Al 6061 | `rho` | 2.70e-6 | kg/mm³ | Điều V |

## 4. Feature-Tree Outline
```
1. Sketch L-profile (100×60 đứng + 100×80 ngang, t=6) trên Datum A   ← FR-001/002/003
2. Extrude L=100 → base solid                                        ← FR-001
3. Hole pattern IF-01: 2× Ø6.6 cánh đứng                             ← FR-004
4. Hole pattern IF-02: 2× Ø6.6 cánh ngang                            ← FR-005
5. Fillet R6 góc trong L (CUỐI)                                      ← FR-006
6. Export STEP + PNG + mass-props
```

## 5. Complexity Tracking — (trống, zero violation)

## 6. Risks (spatial)
| Risk | Callout | Mitigation |
|---|---|---|
| Hai hole pattern trên hai mặt vuông góc — dễ nhầm mặt | sketch #1 | comment `# per CEO sketch #1` từng pattern; CEO kiểm PNG 3 ortho |
