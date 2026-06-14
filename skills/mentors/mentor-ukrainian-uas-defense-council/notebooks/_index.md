---
name: ukrainian-uas-defense-council-notebooks
type: facet-index
mentor: ukrainian-uas-defense-council
last_updated: 2026-06-14
---

# Notebooks Index — mentor-ukrainian-uas-defense-council

| Facet | NLM URL | Notebook ID | Sources | Scope | Primary? | Last refresh |
|-------|---------|-------------|:-------:|-------|:--------:|:------------:|
| primary | https://notebooklm.google.com/notebook/dcc34486-21b4-473d-b3ff-9bdce223c494 | dcc34486-21b4-473d-b3ff-9bdce223c494 | 45 | Fedorov + Brave1 cluster + KSE Institute (incl. Mar-2026 market report) + TRADOC + CSIS/CSET + Ukraine EW + Sky Fortress + I-SEE + Aero Azimuth SIGINT + DefTech 2025; (+4 Exa 2026-06-14) autonomous Shahed interception (Brave1/MaXon 95%), interceptor scaling (Brave1 CEO), AI mid-range deep-strike | ✓ | 2026-06-14 |

## Facet scope notes

**primary:** Single facet covering all 4 domains:
- AI cameras with edge processing (Farsight Vision FSV, Ukrspecsystems USG-231/232 AI modes, Brave1 Dataroom, Jetson Orin edge inference, fog/low-light AI)
- UAVs — attack, reconnaissance, interceptors (Brave1 ecosystem, Fedorov Army of Drones, KSE reports, DefTech 2025 systems warfare, fiber-optic FPV defeat)
- UTM / airspace deconfliction (UTM paradox doctrine, fratricide prevention, Delta COP, Ukraine as European drone wall architect)
- Counter-UAV detection and interception (Bukovel-AD EW, Pokrova spoofing, Zvook/Sky Fortress acoustic 14K sensors, I-SEE passive AI, Kvertus Aero Azimuth SIGINT/receiver ID, Sting interceptors, passive sensor fusion)

## Cross-facet query

Default: all queries go to `primary` facet (only 1 facet exists).

**Current: 45 sources — ✓ no split (trigger raised 45→50 on 2026-06-14, CEO decision).** Rationale: this council is *entirely* 2022-2026 and tightly cross-temporal (e.g. Bukovel-AD 2022 → Brave1 95%-automated interception 2026 are one thread), and most sources are undated web articles spanning the whole war — a `2022-2024 / 2025-2026` partition would cut linked threads and add little. Keep whole; if it ever exceeds 50, the documented split below is the fallback:
- `primary-2022-2024` — early war period, EW adaptation, first AI deployments
- `primary-2025-2026` — autonomous systems maturity, Brave1 Dataroom, remote C2 interceptors, autonomous interception, AI mid-range deep-strike
NLM caveat: sources can't be moved between notebooks — a split would mean a 2nd notebook + re-ingest of the 2025-2026 set. Use `cross_notebook_query` before resorting to a split.

### Added 2026-06-14 via Exa Channel 0 (4; freshest 2026-H1)
- KSE Institute "Ukrainian Defense Technology Market" Mar 2026 `441f5568`
- UNITED24 — Brave1/MaXon 95%-automated autonomous Shahed interception (Jun 2026) `d7e6ab34`
- TWZ — Inside Ukraine's interceptor-drone innovations (Brave1 CEO; 2,000/day) `e545a6c2`
- TWZ — AI-enabled mid-range deep-strike vs Russian logistics (Jun 2026) `57ed0c3a`
> Deleted 1 junk Cloudflare stub (`43c5440b`). Notebook 42→45 (clean). Deferred (held for post-split): AI gun-turret vs fiber-optic, counter-drone lasers/DEW, HORNET VISION Ctrl 500km, Euromaidan/BBC AI middle-strike.

## NLM alias

`nlm alias: mentor-ukrainian-uas-defense-council → dcc34486-21b4-473d-b3ff-9bdce223c494`
