# eval_harness — PASS
- validator: validate.py  · k=3  · 2026-07-17T13:37:30.131426+00:00
- regression: 10/10 (pass_rate 1.0) — MUST be 1.0
- capability: 0/0 (pass_rate None) — hill to climb

| Case | Tier | Expect | Got | k-repro | Hit | Origin |
|---|---|---|---|:-:|:-:|---|
| MR-PASS-massprops | regression | PASS | PASS | ✓ | ✓ | Δ-C mass_reconciliation (Fairley Sanity-Check, CEO 2026-07-17) |
| MR-FAIL-drift | regression | FAIL | FAIL | ✓ | ✓ | Δ-C mass_reconciliation |
| MR-PASS-bom-compute | regression | PASS | PASS | ✓ | ✓ | Δ-C mass_reconciliation |
| MR-FAIL-partial-bom | regression | FAIL | FAIL | ✓ | ✓ | Δ-C mass_reconciliation |
| MR-FAIL-failsafe | regression | FAIL | FAIL | ✓ | ✓ | Δ-C mass_reconciliation |
| DFA-PASS-clean | regression | PASS | PASS | ✓ | ✓ | DFA wire-in 2026-07-17 |
| DFA-FAIL-gating | regression | FAIL | FAIL | ✓ | ✓ | DFA wire-in 2026-07-17 |
| DFA-WARN-advisory | regression | PASS | PASS | ✓ | ✓ | DFA wire-in 2026-07-17 |
| DFA-FAILSAFE-gating | regression | FAIL | FAIL | ✓ | ✓ | DFA wire-in 2026-07-17 |
| DFA-FAILSAFE-advisory | regression | PASS | PASS | ✓ | ✓ | DFA wire-in 2026-07-17 |