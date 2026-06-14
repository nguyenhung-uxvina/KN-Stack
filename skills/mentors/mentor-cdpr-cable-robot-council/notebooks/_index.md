# Notebook Index — mentor-cdpr-cable-robot-council

> Facet registry. Single facet at current size (34 sources). Split trigger: >45 sources.

| Facet | NLM ID | NLM URL | Sources | Last refresh | Primary? |
|-------|--------|---------|:-------:|:------------:|:--------:|
| primary | a2f76979-5dd5-4ac5-a8b7-b56ffdf336f0 | https://notebooklm.google.com/notebook/a2f76979-5dd5-4ac5-a8b7-b56ffdf336f0 | 34 | 2026-06-14 | ✓ |

> 2026-06-14 `--update use exa`: +10 (recover gated panorama via HAL + FWTP/marine cluster: ReaTHM, marine L&R, wave-comp FK, offshore-crane + theory: Merlet workspace/IK-NN, monodromy FK, 2025 review, camera-robot sagging). Deduped Wiley/Hindawi double + 2 thin Springer landings. See `references/seed-sources.md`.
> 2026-06-14 deep-dive Hawwa marine: +1 (academia "Dynamic Analysis of a Floating Cable-driven Platform", 3fa93b4f — figure-caption-level). 2 MMT-2018 ScienceDirect papers (workspace + cable-layout) gated, queued. → 22 sources.
> 2026-06-14 Exa-fallback NLM deep-research (Exa not wired): imported 7 of 56 found → ~29 entries (~6 RG blocked 1020). Useful loaded: Diao&Ma force-closure (≥7 cables, VERIFIED), tanh tension distribution, backstepping LMPC. 6-3-3 layout numbers are synthesis-level (RG primary blocked). Synthesis artifact → project Research_Floating_CDPR_Marine_2026-06-14.md.
> 2026-06-14 Horoub–Hawwa deep-dive (Exa, claude): net +4 → **33 sources**. KEY FIX: the parallel RG imports of the core Horoub papers had landed as Cloudflare **Error-1020 block stubs** (no readable content) — including the CEO-requested AEJ-2023 FPMR "cables' pattern" paper. Replaced them with abstract-level TEXT sources:
>  • Horoub et al. 2023 AEJ — 6-DOF FPMR, **6-6 vs new 6-3-3 cable-bundle**: now LOADED as OPEN-ACCESS FULL TEXT by the parallel pass (`cf38b94c`, DOI 10.1016/j.aej.2022.08.043 — VERIFIED 6-3-3 gains: −39.7% draft, −68.2% tension at X=Y=10, r=5m d=50m H=1m). My interim abstract-text was deleted as redundant. ⚠ raw-pii dup `5faeb1c0` of the same paper present — flag for parallel curator.
>  • Horoub/Hassan/Hawwa 2018 MMT-120 — 3-3 Gough-Stewart, harmonic waves, no-slack workspace + min submerged depth `0672eef5` (replaced blocked stub 75c0395b)
>  • Horoub/Hawwa 2018 MMT-129 — 4 layouts (3-3/6-6/6-3/3-6), layout decides stiffness/tension, mass = structural + added hydrodynamic `3710af57` (replaced thin SD stub b3ce8ad2)
>  • Horoub 2020 IEEE-Access — TLP-as-manipulator, mooring pretension/stiffness tuning `5d5b2db3` (text; IEEE ielx7 PDF blocked)
>  Plus open-access adjacent: Uminho deep-sea CPM 6/8/10-cable optimization `b7203d78` (10-cable +20% workspace/−15% post-failure tension); LIRMM CableCon-2023 Robotic Seabed Cleaning Platform `a7a0feb2` (8-winch floating marine CDPR prototype); TU Dresden 4-cable floating desedimentation `0e69f2cf` (sag→FK ambiguity).
>  Hygiene: deleted blocked/dup stubs (a8f008db, b3ce8ad2, 75c0395b, d691dc6c, 81f38715, IEEE ielx7). Kept academia Hawwa-dyn `3fa93b4f` (loaded). ⚠ `f3a09f67` (Horoub 2019 Springer "A Floating CDR Manipulator in a Marine Environment") is still a blocked RG stub — re-attempt as text/file next pass.

## Scope
CDPR theory + kinematics (Pott, sagging IK, workspace) + control/marine (tension distribution AC, input-shaping, boat/vessel motion simulator).

## Split plan (when >45 sources)
- `cdpr-theory-kinematics` — Pott book, sagging/catenary IK, workspace/stiffness analysis
- `cdpr-control-marine` — tension distribution, input-shaping, LMI/tensegrity, vessel motion simulators

## Pending ingest (gated seed sources) — status 2026-06-14
- ✅ MPE 2022 overview — resolved (Hindawi OA full text; Wiley dup deleted)
- ✅ Panorama of sagging cables — resolved (HAL open full text; thin Springer chapter deleted)
- ⚠ Heavy-duty parallel ship motion sim platform (Springer 978-981-95-2101-2_10) — still thin; no open mirror found yet
- ⚠ 6-DOF vessel motion simulator MBD+LBM (Ocean Eng.) — still thin; no open mirror found yet
Re-attempt the 2 remaining at next `--refresh` (author preprint / arXiv).
