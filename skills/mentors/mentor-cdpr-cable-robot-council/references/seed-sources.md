# Seed Sources — mentor-cdpr-cable-robot-council

> Curated 2026-06-14. Build: 8 + 4 gated. `--update use exa` 2026-06-14: +10 (recover gated #2 via open mirror + FWTP/marine cluster + theory). **Live notebook: 21 clean sources** (after deduping a Wiley/Hindawi double + 2 thin Springer landings).
> Notebook: a2f76979-5dd5-4ac5-a8b7-b56ffdf336f0

## Ingested (8)

### Tier 1 — Canonical / direct
| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| 1 | Pott, A. — *Cable-Driven Parallel Robots: Theory and Application* (Springer STAR 120, 2018) | link.springer.com/book/10.1007/978-3-319-76138-1 | 1334e655 | Canonical textbook |
| 2 | A Review on Cable-Driven Parallel Robots (Chinese J. Mech. Eng., 2018) | link.springer.com/article/10.1186/s10033-018-0267-9 | 7f57a848 | Comprehensive survey |
| 3 | Jang & Bewley — Tension Optimization of the 6-DOF Cable-Driven Boat Motion Simulator (RSAE 2021, ACM) | dl.acm.org/doi/fullHtml/10.1145/3475851.3475854 | 1371828b | ⭐ Direct FWTP analog (8-cable, LMI, tensegrity) |

### Tier 2 — Authoritative supporting
| # | Source | URL | NLM source_id | Topic |
|---|--------|-----|---------------|-------|
| 4 | Stiffness-based Analytic-Centre Method for CDPR (arXiv 2505.07348) | arxiv.org/pdf/2505.07348 | fdf01dc4 | AC tension distribution + active stiffness |
| 5 | Input-Shaping for Feed-Forward Control of CDPR (arXiv 2010.11676) | arxiv.org/pdf/2010.11676 | 73881402 | ZVD/ZVD-ZVD vibration suppression |
| 6 | Empirical Quasi-Static & Inverse Kinematics of CDPM incl. Sagging (MDPI Appl. Sci. 10(15):5318) | mdpi.com/2076-3417/10/15/5318 | 5a6e863c | Irvine sagging hybrid IK, ΔL=TL/EA |
| 7 | Inverse Kinematics & Workspace Analysis of a Cable-Driven (Colostate, MMT 2014) | engr.colostate.edu/.../2014-MMT.pdf | ee64cd7b | IK + workspace |
| 8 | Design of a 6-DoF Cable-Driven Parallel Robot Experimental Platform (SciOpen 2025) | sciopen.com/article/10.16791/j.cnki.sjg.2025.06.024 | 65c4329d | 8-cable 6-DOF PVT control, force sensors |

## Added 2026-06-14 — Exa Channel 0 semantic discovery (10; CEO-approved full set)

### Recovered gated source via open mirror
| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| G1 | A Panorama of Methods for Dealing with Sagging Cables in CDPR (Tissot/Merlet, ARK 2022) | inria.hal.science/hal-03610293v1/document | 9feccd4e | ✅ Open full text — supersedes gated #2 (thin Springer chapter deleted) |

### Marine / FWTP application (council's core purpose)
| # | Source | URL | NLM source_id | Topic |
|---|--------|-----|---------------|-------|
| M1 | Optimal Actuator Placement for Real-Time Hybrid Model Testing using CDPR (MDPI JMSE 9(2):191) | mdpi.com/2077-1312/9/2/191 | 4e45030a | ⭐ ReaTHM ocean-structure testing; force allocation, winch placement |
| M2 | An Underactuated CDPR for Marine Automated Launch & Recovery Operations (2025) | academia.edu/121823122 | 02b55f1f | ⭐ Vessel-mounted CDPR deploy/recover craft through sea surface; winch sizing, 10 kN |
| M3 | Real-time FK of suspended 6-DOF wave-compensation CDPM (Lv, Tao, Hu — Adv. Mech. Eng. 2017) | journals.sagepub.com/doi/10.1177/1687814017706264 | 134a948d | **text** (SAGE stub deleted); tetrahedron+LM real-time FK tolerant of slack cables; 8-cable + encoders/laser/IMU |
| M4 | Offshore crane payload positioning, parallel cable-driven anti-swing (PP-PCDM) | yadda.icm.edu.pl/baztech/...4_PMRes_Ren_29_45.pdf | 8696c099 | Ship-mounted anti-swing tension control |

### Theory / kinematics deepening (sagging + workspace + tension)
| # | Source | URL | NLM source_id | Topic |
|---|--------|-----|---------------|-------|
| T1 | Workspace cross-sections of CDPR with 6 sagging cables (Merlet) | inria.hal.science/hal-01643456/document | 8abf4eee | Irvine sagging workspace border |
| T2 | IK of CDPR with >6 sagging cables, Part 2: neural networks (Merlet) | inria.hal.science/hal-04609264v1/document | 645ecfdd | Redundant-cable IK optimization |
| T3 | Monodromy numerical-continuation FK of CDPR with sagging cables (Baskar, MMT 2024) | par.nsf.gov/servlets/purl/10562611 | e03ce17d | All-solutions FK, 8-cable spatial CDPR |
| T4 | A Review of CDPR — AI-driven control (J. Vib. Eng. Tech. 2025) | link.springer.com/article/10.1007/s42417-025-02121-z | 119c8624 | **text** (thin Springer URL deleted); 2025 state-of-the-art citation map |
| T5 | Large-span high-speed camera-robot CDPR — catenary sagging + tension distribution + anti-wind (MDPI Machines 10(7):565) | mdpi.com/2075-1702/10/7/565 | 1703558b | Sagging + anti-wind tension optimization |

## Gated — status after 2026-06-14 `--update`
| Source | Status |
|--------|--------|
| Overview of CDPR: Workspace, Tension Distribution, Cable Sagging (MPE 2022/2199748) | ✅ RESOLVED — Hindawi open-access full text retained (`56364bc1`); Wiley duplicate (`c2f4f494`) deleted |
| A Panorama of Methods for Dealing with Sagging Cables (Springer 978-3-031-08140-8_14) | ✅ RESOLVED — replaced by HAL open full text G1 (`9feccd4e`); thin Springer chapter (`1744f796`) deleted |
| Design & Optimization of a Heavy-Duty Parallel Ship Motion Simulation Platform (Springer 978-981-95-2101-2_10) | ⚠ STILL THIN — landed as gated Springer page (`6ff9fe51`); no open mirror found. Re-attempt next refresh (author preprint) |
| 6-DOF vessel motion simulator MBD+LBM (Ocean Eng. S0029801825013010) | ⚠ STILL THIN — landed as ScienceDirect abstract (`1be80c93`); no open mirror found. Re-attempt (arXiv/author copy) |

## Added 2026-06-14 — deep-dive: Horoub–Hawwa marine floating CDPR (KFUPM)

| # | Source | URL | NLM source_id | Note |
|---|--------|-----|---------------|------|
| H1 | Hawwa — *Dynamic Analysis of a Floating Cable-driven Platform for Marine Applications* | academia.edu/53616609 | 3fa93b4f | ⭐ 6-cable 3-3 Stewart-Gough, seabed-moored, motors-on-platform, buoyancy↔pretension↔draft, Finnegan(2011) wave forces. Figure-caption-level content (full 8-pg PDF gated) |

### Gated — queued (closest FWTP prior art; for SHTT brief)
| Source | Status |
|--------|--------|
| Horoub, Hassan, Hawwa (2018) *Workspace analysis of a Gough-Stewart type cable marine platform subjected to harmonic water waves*, Mech. Mach. Theory 120:314–325 (S0094114X1630708X) | ScienceDirect gated; foundational full-equation paper — re-attempt ResearchGate/author copy |
| Horoub, Hassan (2018) *Influence of cables layout on the dynamic workspace of a six-DOF parallel marine manipulator*, Mech. Mach. Theory (S0094114X18302982) | ScienceDirect gated; directly addresses cable-layout → 4-vs-8 question; re-attempt |
| Horoub, Hassan, Hawwa (2019) *A Floating Cable-Driven Robotic Manipulator in a Marine Environment*, Springer (978-3-030-20131-9_286) | Springer chapter gated |

## Added 2026-06-14 — Exa-fallback NLM deep-research (56 found, 7 imported)

> Exa not wired this session → used NotebookLM `deep` web research (protocol-sanctioned fallback). RG imports mostly blocked (Error 1020) — useful loaded marked ✅.

| Source | URL | NLM source_id | Status |
|--------|-----|---------------|--------|
| ✅ Diao & Ma — Force-closure analysis of 6-DOF cable manipulators with seven+ cables (Robotica) | cambridge.org/.../7CA7A5062C... | e71ce76d | LOADED — VERIFIED ≥7-cable rule |
| Real-Time Tension Distribution (tanh-bounded), MDPI Appl.Sci. 13/1/10 | mdpi.com/2076-3417/13/1/10 | f9ad25cd | loaded |
| Robust Adaptive Backstepping + improved LMPC, underwater CDPM, MDPI JMSE 11/6/1173 | mdpi.com/2077-1312/11/6/1173 | ba2874f5 | loaded |
| Hawwa Dynamic Analysis (RG mirror) | researchgate.net/publication/269629692 | 81f38715 | BLOCKED 1020 (academia copy 3fa93b4f already loaded) |
| Horoub Workspace MMT 2018 (RG) | researchgate.net/publication/320276018 | 75c0395b | BLOCKED 1020 |
| Horoub "A Floating CDR Manipulator in a Marine Environment" (RG) | researchgate.net/publication/333766806 | f3a09f67 | BLOCKED 1020 |
| Horoub "Study effect of changing cables' pattern (6-3-3) on 6-DOF FPMR workspace" (RG) | researchgate.net/publication/363305374 | d691dc6c | BLOCKED 1020 — superseded by OA primary below |
| ✅ Horoub et al. (6-3-3 paper, OPEN ACCESS primary) — *Alexandria Eng. J.* 64:847–858 (2023), CC BY, DOI 10.1016/j.aej.2022.08.043 | sciencedirect.com/science/article/pii/S1110016822005750 | cf38b94c | LOADED full text — VERIFIED 6-3-3 numbers (−39.7% draft, −68.2% tension at X=10,Y=10; r=5m, d=50m, H=1m). Found via KFUPM repo → DOI → AEJ OA |

Deep-research synthesis (equations + 6-3-3 numbers, UNVERIFIED vs primary) saved to: `D:/Workshop_X/1_Projects/VN-FWTP-001…/Research_Floating_CDPR_Marine_2026-06-14.md`. To verify: acquire Horoub MMT-2018 PDFs outside RG and add as `file`/`text`.

## Tier criteria
- T1: canonical textbook, comprehensive survey, or direct application analog (boat/vessel cable motion sim).
- T2: peer-reviewed method paper on a specific sub-problem (tension distribution, IK sagging, input-shaping, workspace).
- T3: adjacent/secondary (none retained this build).
