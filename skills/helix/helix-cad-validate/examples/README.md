# examples/ — regression-corpus seed (v2.0 DFM)

Golden fixtures for the deterministic DFM checks. Seed for the `pass^k` eval/regression tier in the
roadmap (SKILL.md "When to add the next tier"). Run against the hermetic `design_rules.example.json`
(self-contained — no external parts_master CSV needed).

```bash
# Windows: prefix PYTHONUTF8=1
python ../validate.py --extract pass_case.cad_extract.json --rules design_rules.example.json --out /tmp/pass
#   => exit 0 · verdict PASS  (Ø8 hole, spacing 30mm, depth:dia 3.0×  — all DFM PASS)

python ../validate.py --extract fail_case.cad_extract.json --rules design_rules.example.json --out /tmp/fail
#   => exit 2 · verdict FAIL  (Ø3 < 6mm min · spacing 8 < 20mm · depth:dia 10× > 6×  — three DFM FAILs)
```

Expected verdicts:

| Fixture | min_hole_dia_mm | hole_spacing_mm | hole_depth_ratio | Verdict | Exit |
|---|---|---|---|---|---|
| `pass_case` | Ø8 ≥ 6 ✅ | 30 ≥ 20 ✅ | 3.0× ≤ 6 ✅ | **PASS** | 0 |
| `fail_case` | Ø3 < 6 ❌ | 8 < 20 ❌ | 10× > 6 ❌ | **FAIL** | 2 |

Both also carry a `provenance` block in the JSON output (linter + contract sha256). When adding a new
rule to `validate.py`, add a fixture here that exercises it (one PASS, one FAIL) before shipping.
