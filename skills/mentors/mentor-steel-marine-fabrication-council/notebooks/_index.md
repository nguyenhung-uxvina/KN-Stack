---
mentor: steel-marine-fabrication-council
updated: 2026-06-14
---

| Facet | NLM UUID | URL | Sources | Scope | Last refresh | Primary? |
|-------|----------|-----|:-------:|-------|:------------:|:--------:|
| primary | 0d4d0c47-1bfa-45a0-8abd-c50b4eaa9d3b | https://notebooklm.google.com/notebook/0d4d0c47-1bfa-45a0-8abd-c50b4eaa9d3b | 29 | Steel marine fabrication: structural connections (Eurocode 3-1-8) + slip-critical bolts, welding (SMAW/E7018/S355/A36 + AWS D1.1 code/WPS), marine coating (galvanizing/ZRC + offshore TSA/NORSOK M-501/ISO 12944-9), tropical corrosion, fatigue (DNV RP-C203 + EN 1993-1-9), NDT inspection | 2026-06-14 | ✓ |

## Added 2026-06-14 via Exa Channel 0 (12; this `_index.md` is the source registry — no separate seed-sources.md)

### Offshore coatings / thermally-sprayed aluminium (TSA)
- IOGP S-715 — Supplementary spec to NORSOK M-501 (coating/painting offshore; CX/Im4, TSA per AWS C2.23/ISO 2063) `ab8a4bd6` *(replaces a dead Sherwin-Williams NORSOK link)*
- npj Materials Degradation — Metallic coatings in offshore wind (TSA/TSZ/TSZA, ISO 2063 thicknesses) `88243a9f`
- MDPI Coatings — Sacrificial Thermally Sprayed Aluminium Coatings for Marine Environments: A Review `dfb0ef7a`
- MDPI Materials — Evaluation of Protective Coatings for High-Corrosivity (CX) Offshore Applications (TSA vs carbide vs epoxy) `a2e24a98`
- ISO 12944-9:2018 — protective paint systems for offshore (CX / Im4) `08b3e35d`

### Welding — AWS D1.1 (was claimed authority, previously unsourced)
- AWS D1.1/D1.1M:2020 Structural Welding Code — Steel (code PDF) `0a8e7707`
- Welding Answers — writing AWS D1.1 prequalified WPS (Table 5.3 base metals / 5.1 limits) `5e965612`
- Welding Answers — reason behind D1.1 minimum fillet weld sizes (heat input / HIC) `3eed1025`
- Oliphant — "AWS D1.1: do you know what it really says" (CVN, thin-to-thick plate, prequalified caveats) `988346a8`

### Fatigue (pontoon/marine-critical, previously unsourced)
- DNVGL-RP-C203 — Fatigue design of offshore steel structures (S-N, hot-spot, **seawater + CP**) `ee0293f0` ⭐
- EN 1993-1-9:2005 — Eurocode 3 fatigue (⚠ explicitly EXCLUDES seawater corrosion → use DNV RP-C203 for marine) `ee440b08`

### Connections
- SCI GN-2-06 — preloaded bolts in slip-resistant connections (Eurocode Cat. B/C) `92dc7597`

> Hygiene 2026-06-14: 13 approved; 2 landed as stubs and were deleted (Sherwin-Williams NORSOK 404 → replaced with IOGP S-715; IIW hot-spot guide behind auth.gr login wall → DEFERRED, hot-spot already covered by DNV RP-C203). Notebook 17→29, all on-topic.
> Deferred: IIW "Structural Hot-Spot Stress Approach to Fatigue" Designer's Guide — find open mirror at next refresh.
