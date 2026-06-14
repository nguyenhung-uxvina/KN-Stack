# Seed Sources — mentor-nswc-hull-council

Initial source list ingested 2026-06-09 (20). **Updated 2026-06-14** (`--update use exa`): +7 → **27 sources** (class-society rules + Kendrick-via-Ross + general-instability/imperfection-sensitivity). Full current list with IDs in `notebooks/_index.md`.

## T1 — Primary Institutional Publications (Open Access)

| # | Title | Source | URL | NLM Source ID |
|---|-------|---------|-----|---------------|
| 1 | Windenburg & Trilling (1934) — "Collapse by Instability of Thin Cylindrical Shells" | DTMB / APM | https://cybra.lodz.pl/Content/6287/APM_56_20.pdf | 528db19f-5e36-4743-b5c8-4eb061f71785 |
| 2 | NASA SP-8007 (1968) — Buckling of Thin-Walled Circular Cylinders | NASA NTRS | https://ntrs.nasa.gov/api/citations/19690013955/downloads/19690013955.pdf | c406930c-9a9a-4a05-95cb-848972ad00cc |
| 3 | NASA SP-8007 Rev 2 (2020) | NASA NTRS | https://ntrs.nasa.gov/api/citations/20205011530/downloads/20205011530%20Rev%202FINALa%201-2023.pdf | 5a440b76-4e00-4ea7-8ee3-5497bea75475 |
| 4 | DTIC AD0729021 — Design Considerations for Aluminum Hull Structures | DTIC | https://apps.dtic.mil/sti/tr/pdf/AD0729021.pdf | 58a669d0-ba5b-4609-a3d6-cb3fb2970ea1 |
| 5 | DTIC ADA405710 — Failure of Ring-Stiffened Cylinders (NAVSEA) | DTIC | https://apps.dtic.mil/sti/tr/pdf/ADA405710.pdf | ef09c1f8-0dc7-44f2-a90c-e8af19a511a1 |
| 6 | DTIC ADA058231 — Optimal Design of Ring Stiffened Cylindrical Shells | DTIC | https://apps.dtic.mil/sti/tr/pdf/ADA058231.pdf | 0dd89817-f5c3-4725-8cc2-10a238c910b3 |
| 7 | DTIC ADA480819 — Design and Analysis of Orthotropic Ring-Stiffened Cylindrical Shells | DTIC | https://apps.dtic.mil/sti/pdfs/ADA480819.pdf | 8dc2f996-dcdc-4223-9800-c8318a11d5d1 |
| 8 | DTIC ADA475270 — Cylinder Collapse Tests (external T-section rings) | DTIC | https://apps.dtic.mil/sti/tr/pdf/ADA475270.pdf | 1a9c57f9-e960-4376-b1f5-ce004841ac92 |
| 9 | DTIC ADA592293 — PRHDEF Stress and Stability of Ring Stiffened Cylinders | DTIC | https://apps.dtic.mil/sti/tr/pdf/ADA592293.pdf | d1f24ccd-6231-4acd-b7f1-e51d3deb4a9f |
| 10 | DTIC ADA607750 — Preliminary Design of an AUV | DTIC | https://apps.dtic.mil/sti/tr/pdf/ADA607750.pdf | 04e810ac-9c1e-4bee-8423-34c8821f440b |
| 11 | MDPI — Pressure Hull Design Methods for UUV (2019) | MDPI Open | https://www.mdpi.com/2077-1312/7/11/382 | 39980bf8-9688-4c97-a22f-8ff9fd58ea62 |
| 12 | MDPI — Initial Scantling Formulas for Submarine Deep Frames (2026) | MDPI Open | https://www.mdpi.com/2077-1312/14/4/386 | 17f5ffea-557c-42d6-8f23-f0a5ec824d1d |

## T2 — Standards and Reference Materials

| # | Title | Source | URL | NLM Source ID |
|---|-------|---------|-----|---------------|
| 13 | MIL-HDBK-5H — Metallic Materials for Aerospace Structures | DoD/MMPDS | https://aluminium-guide.com/wp-content/uploads/2019/04/MIL-HDBK-5H-Design-with-Metals.pdf | 943fe444-659f-4a5e-b827-74a4cbb71117 |
| 14 | NAVSEA General Specification for Hyperbaric Equipment | NAVSEA | https://www.navsea.navy.mil/Portals/103/Documents/SUPSALV/Diving/General%20Specifications%20Hyperbaric%20Equip.pdf | 72ac4aad-4a1c-4978-8b65-62b3a19e7097 |

## T3 — Text Sources (Council-Synthesized)

| # | Title | NLM Source ID |
|---|-------|---------------|
| 15 | NSWC Carderock / DTMB — Institutional Profile & Design Authority | cc0303ac-bb9e-4a90-8629-1af0243b2486 |
| 16 | Ring-Stiffened Cylinder Design — Complete Quantitative Guide | 2f0df71c-007f-48df-80d9-f339caafe720 |
| 17 | AUV and Torpedo Pressure Hull Design — International Practice Survey | 80f1d858-8224-4eee-bd91-a82b2cce6ea9 |
| 18 | MIL-SPEC Safety Factor Framework for Naval Pressure Hulls | 959195fd-1337-4b32-ade3-d82bc03a17c4 |
| 19 | Hydrostatic Test Protocol — Navy Procedure for Pressure Hull Certification | 88b90ed5-1bd0-4893-a818-e0260feccb73 |
| 20 | NSWC Hull Council — Decision Principles, Frameworks, and WX Application Guide | f03bd605-6824-4776-9113-9019dc97c936 |

## Next Refresh Priority — status after 2026-06-14 `--update`

1. NAVSEA DDS 100-4 — ring-stiffened cylinder DDS — ⚠ STILL OPEN (no accessible public version found)
2. Kendrick (1953) buckling under external pressure, ring frames — ✅ ADDRESSED via Ross/Andriosopoulos/Little (Kendrick Pt.1/3 + plastic-knockdown design charts, `c11f4391`) + NACA explicit formulas (`1c86ed54`). Kendrick ORIGINAL still gated (OSTI has no digital full text).
3. ABS Guide for Underwater Vehicles/Systems/Hyperbaric — ✅ DONE — ABS Underwater Rules 2025 (`757dcec6`)
4. DNV submersible structural design — ✅ DONE — DNVGL-RU-UWT text (Pt.3 + Pt.5 Ch.7, `a77c3bd2`) + DNV technology-qualification (`f0065c7b`)
5. NUWC Newport torpedo-hull structural certification — ⚠ STILL OPEN (not surfaced via Exa/DTIC)

### Also added 2026-06-14 (beyond the original priority list)
- USCG/ABS Pressure-Hull Requirements for Passenger Submersibles (2024) — approved pressure-hull materials + cert chain, post-Titan (`045ed4b8`)
- Buckling & sensitivity estimates for ring-stiffened cylinders — SIFM vs GIFM, imperfection sensitivity (`b659c101`)

### Remaining for next refresh
- NAVSEA DDS 100-4 (try alternate hosts / FOIA-released versions)
- NUWC Newport torpedo-hull certification reports (DTIC deep search)
- Kendrick 1953 original full text (WorldCat / UK NCRE archive)
