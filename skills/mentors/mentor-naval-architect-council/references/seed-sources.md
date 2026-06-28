# Seed Sources — mentor-naval-architect-council

Curated source list ingested during ADD pipeline (2026-05-28). **Updated 2026-06-14** (`--update use exa`): live notebook = **42 sources** (the original 18 below + an un-logged prior expansion of ~13 mooring/scantlings/floating-wind sources + 11 added via Exa 2026-06-14; 1 junk stub deleted). See `notebooks/_index.md` for the full current source list with IDs.

## Source Registry (original ADD-pipeline 18)

| NLM ID | Title | Tier | Method | Notes |
|--------|-------|------|--------|-------|
| `3a78d65a` | Taylor "The Speed and Power of Ships" (Archive.org 1910/1933) | T1 | URL ✓ | Primary — TSS charts, resistance/propulsion methodology |
| `9c5d9e92` | Taylor "Resistance of Ships and Screw Propulsion" (1893, text compilation) | T1 | TRY2 text | Primary — foundational resistance theory |
| `7934fd1d` | PNA Vol I — Stability and Strength (Lewis ed., SNAME 1967/1988, text compilation) | T1 | TRY2 text | Primary — stability, structural design, HAZ |
| `2e00748b` | PNA Vol II — Resistance, Propulsion and Vibration (Lewis ed., SNAME 1988, text compilation) | T1 | TRY2 text | Primary — ITTC friction, Holtrop-Mennen, EHP-DHP chain |
| `7f271f3c` | PNA Vol III — Motions in Waves and Controllability (Lewis ed., SNAME 1989, text compilation) | T1 | TRY2 text | Primary — seakeeping, roll resonance, maneuvering |
| `698550f7` | Gertler, "A Reanalysis of the Original Test Data for the Taylor Standard Series" DTMB Report 806 (1954, text compilation) | T2 | TRY2 text | Authoritative — TSS Gertler charts, valid bounds |
| `63ea8202` | Tupper, "Introduction to Naval Architecture" 4th ed. (Archive.org) | T2 | URL ✓ | Authoritative — accessible modern synthesis |
| `fd55858a` | MIT OpenCourseWare 2.20 — Marine Hydrodynamics (Lectures + Notes) | T2 | URL ✓ | Authoritative — modern teaching materials |
| `9592efec` | Molland, Turnock, Hudson — "Ship Resistance and Propulsion" (Cambridge University Press 2017, text compilation) | T2 | TRY2 text | Authoritative — modern resistance/propulsion including small craft |
| `3531eb75` | David W. Taylor — Wikipedia (biographical + career) | T3 | URL ✓ | Background — career arc, program history |
| `2e9cfde8` | Tunaley — "The Taylor Standard Series" (london-research-and-development.com PDF) | T3 | URL ✓ | Accessible TSS explanation + charts |
| `ebc60556` | PNA Ship Resistance excerpts (rexresearch1.com compilation) | T3 | URL ✓ | Reference excerpts |
| `38f5f8bd` | Shallow Water River Craft Hydrodynamics (text compilation: Schlichting correction, Barras squat, critical speed, transcritical regime) | T3 | TRY2 text | VSN-1500 specific — shallow water methods |
| `4f5622cb` | NAS Biographical Memoir — David Watson Taylor (text compilation) | T3 | TRY2 text | Background — Taylor's contributions in historical context |

| `141a2303` | Li & Ellingsen 2016 — "Ship waves on uniform shear current at finite depth: wave resistance and critical velocity" — J. Fluid Mechanics (arXiv:1604.06608) | T2 | URL ✓ | Shear current lateral wave resistance (10-20% of Rt); upstream resistance peaks at lower Fn; critical for VSN-1500 EHP |
| `edd5ebfc` | TC 5-210 Ch.4 "Improved Float Bridge (Ribbon)" — US Army Training Circular (ugliboats.com PDF) | T2 | TRY3 URL ✓ | Military float bridge operational doctrine: current limits, load classification, self-propelled raft propulsion |
| `7e6fe9a8` | MDPI JMSE 2025 — "CFD-Based Estimation of Ship Waves in Shallow Waters" Vol 13 No 10 | T3 | URL ✓ | Transcritical bounds: 0.84≤Fnh≤1.15; wave height surge formula; swamping risk from own transverse wash |
| `f85f0899` | arXiv:1702.06275 — "Time-frequency analysis of ship wave patterns in shallow water" — Pethiyagoda et al. 2017 | T3 | URL ✓ | Physical experiment confirmation: high-aspect-ratio hull interference; 8-hull phà wave interference unpredictable from theory |

**Tier summary:** T1×5, T2×6, T3×7 = 18 total

## Deleted Bad Sources (TRY1 failures → replaced by TRY2)

| Original NLM ID | Original URL | Failure reason | Replacement |
|-----------------|-------------|---------------|-------------|
| `684204e3` | archive.org/details/resistanceofship00tayl | Internet Archive "Error" — wrong identifier | `9c5d9e92` (text compilation) |
| `6bab1b45` | NAS PDF Cloudflare-blocked | "Just a moment..." Cloudflare block | `4f5622cb` (text compilation) |
| `f8a35673` | Academia.edu PNA Vol I | "Just a moment..." Cloudflare/paywall | `7934fd1d` (text compilation) |

## Refresh Search Channels (for future --refresh)

Priority channels to check since last_refresh:
1. **SNAME Transactions** — peer-reviewed, T1-T2 potential
2. **Journal of Ship Research** (SNAME) — resistance/propulsion research, T2
3. **International Journal of Offshore and Polar Engineering (IJOPE)** — shallow water, T2-T3
4. **RINA Proceedings (Royal Institution of Naval Architects)** — design guidance, T2
5. **NSWCDD/DTMB declassified reports** — successors to Taylor's basin, T2
6. **MIT OpenCourseWare** — 2.20 updates, T2
7. **USNI Naval Engineers Journal** — military small craft, T2-T3

**Recommended next refresh:** 2026-08-28 (quarterly cadence, same as Rickover)
