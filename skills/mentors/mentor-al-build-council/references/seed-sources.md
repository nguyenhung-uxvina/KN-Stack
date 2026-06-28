# Seed Sources — mentor-al-build-council

## T1 Sources (Primary — council's own authoritative publications)

| # | Title | Type | NLM Source ID | Notes |
|---|-------|------|--------------|-------|
| T1-01 | AWS D1.2:2021 – Structural Welding Code for Aluminum: Key Principles | Text (derived) | 0a5329ac-0af7-45e5-a985-80fa7f32073e | Core welding standard |
| T1-02 | Al 5083-H32 Material Properties and HAZ Behavior under TIG Welding | Text (derived) | 57a375ba-f52f-4c4d-a1b3-631a5b52027f | Material science foundation |
| T1-03 | Windenburg-Trilling Buckling Formula – External Pressure Thin Cylinders (DTMB 886) | Text (derived) | e3aa06e5-dcf8-4567-b09a-ec224db90105 | 1934 foundational paper |
| T1-04 | TIG Welding Process for Thin Aluminum (3-4mm): Parameters and Technique | Text (derived) | 903225a8-130b-4cee-a04d-f9da7f0a77ba | Process engineering |
| T1-05 | Aluminum Rolling Process and Cylinder Fabrication for Pressure Vessels | Text (derived) | 10fd4c35-e971-4d41-b506-4332bd5da885 | Fabrication sequence |
| T1-06 | Aluminum Torpedo Hull Fabrication: International Practice Survey | Text (derived) | 98eea9cc-ca2c-4f63-a0ec-8e2771f6bc54 | International practice |
| T1-07 | Al-Build Council: Decision Principles and Fabrication Checklist for Torpedo Hulls | Text (derived) | 94a39fc1-4faa-4bb7-9881-d20fe627dd63 | Council synthesis |

## T2 Sources (Authoritative secondary)

| # | Title | Type | NLM Source ID | Notes |
|---|-------|------|--------------|-------|
| T2-01 | Distortion Control and Sequence B Fabrication for Ring-Stiffened Cylinders | Text (derived) | c88bb508-7b18-4081-893a-feb695357f55 | Distortion management |
| T2-02 | DNV / BV Naval Aluminum Rules and Hydrostatic Test Procedures | Text (derived) | 127529b9-02d3-4fac-aa55-97882b42f9b4 | Classification rules |
| T2-03 | Filler Metal Selection for Underwater Aluminum Structures (ER5356 vs ER4043) | Text (derived) | 0642a2f6-1fd4-48fa-9951-67d46c727ee7 | Materials selection |

## T3 Sources (Supporting)

| # | Title | Type | NLM Source ID | Notes |
|---|-------|------|--------------|-------|
| T3-01 | Hobart Brothers – Filler Metal Selection Guide for Aluminum | URL | 262ff006-c8fa-4dbf-a73b-a31095b86214 | Partial content (URL) |

## Added 2026-06-14 — Exa Channel 0 semantic discovery (10, full-text)

Total now: 27 sources (17 original + 10). Notebook a0e354c4. Discovery engine: Exa MCP. CEO selected "full-text only" (dropped 2 paywalled ScienceDirect abstracts).

### Buckling / external pressure
| # | Title | Type | NLM Source ID | Notes |
|---|-------|------|--------------|-------|
| X-B1 | DTIC ADA592293 — Submarine pressure-hull structural integrity (PRHDEF / BS5500; interframe + overall buckling, out-of-circularity) | URL (PDF, .mil) | e4f5ee0b-f76b-4c45-9caa-bb2c456e3af0 | **A-tier** authoritative; modern complement to 1934 Windenburg-Trilling text |
| X-B2 | MDPI JMSE — Buckling Analysis of AUV Pressure Vessel with Sliding Stiffeners (2020) | URL (open) | 3a07f5b1-f108-4da8-8880-ef1b4296c758 | Aluminum AUV; welded-stiffener residual-stress tradeoff |
| X-B5 | MDPI JMSE — Failure of Corrugated Aluminum Pressure Shells under External Pressure (2024) | URL (open) | 9690d1be-0665-45ff-81f0-438d1a2fee2a | Hydrostatic test + Abaqus/Riks w/ measured imperfections |
| X-B6 | ISEC — Buckling Behavior of Ring-Stiffened Aluminum Cylinders (FE 3–17 stiffeners) | URL (PDF) | fe29af81-3000-439c-a5d5-8fe24ca6f61e | Optimum stiffener count/spacing |

### Welding / HAZ / qualification
| # | Title | Type | NLM Source ID | Notes |
|---|-------|------|--------------|-------|
| X-W1 | IRClass — Guidelines on WPS Qualification Tests of Aluminium Alloys for Hull Construction (Sep 2022) | URL (PDF) | 7302d0f4-e24a-4345-ae69-5aaf47d7e235 | **A-tier** real WPS qual procedure; alloy Groups A/B/C; min tensile by grade |
| X-W2 | ESAB — The HAZ in Aluminum Welds (as-welded vs base tensile tables; 5083-H116 46→43 ksi) | **Text** (WebFetch) | 91d4d221-297a-4643-a01e-e865127a4fe9 | URL ingest blocked by Cloudflare → ingested as text |
| X-W3 | Nature Sci. Reports — Filler effects (ER4043 vs ER5356) on GTAW Al 5083/6082 joints (2023) | URL (open) | d80ff9fd-544a-4465-8dbf-3d6deb7a2ac4 | **A-tier** peer-reviewed; backs ER5356 preference |
| X-W4 | Lloyd's Register — Specific requirements for welded aluminium (GTAW/GMAW/FSW; no heat distortion-correction) | URL | c3d01776-3bc8-4738-9fdd-b277ec904143 | Classification welding rule + property tables |
| X-W5 | ESAB Aluminum Technical Guide | URL (PDF) | cd523589-b78f-4d68-84f8-e389b2fefb8b | Comprehensive metallurgy primer |
| X-W6 | BlueScope — Aluminium 5383 Data Sheet (5083 upgrade) | URL | 9655fb17-d8fc-45bf-b160-b22d26938f68 | 5383 properties/corrosion/bend radii |

## Failed / recovered ingests (2026-06-14)
- ESAB HAZ URL → blocked by Cloudflare ("Attention Required!"); recovered via WebFetch → text source `91d4d221`. Blocked junk entry `6c4604ec` deleted.

## Refresh Priority

Already added 2026-06-14: classification WPS qualification (IRClass), HAZ metallurgy (ESAB), filler science (Nature), modern buckling (DTIC/MDPI/ISEC). Still open:
- Lincoln Electric GTAW Aluminum Best Practices (URL)
- NAVSEA welding specifications (public portions)
- ScienceDirect full-text (paywalled) — aluminum implosion tests + Merchant-Rankine ultimate-strength formulation (abstracts deferred 2026-06-14; ingest if full-text access obtained)
