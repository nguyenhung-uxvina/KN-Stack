# Notebooks Index — mentor-military-combat-engineer-council

Facet registry for this mentor. Updated each ADD or REFRESH.

## Facet Registry

| Facet | NLM URL | Notebook ID | Source count | Scope | Last refresh | Primary? |
|-------|---------|-------------|:------------:|-------|:------------:|:--------:|
| primary | https://notebooklm.google.com/notebook/2cb1a634-90e6-4ce6-acb5-d747d45165b2 | `2cb1a634-90e6-4ce6-acb5-d747d45165b2` | 45 | All doctrine: US FMs (FM 90-13, FM 3-34, FM 3-90.12, TC 5-210, ATP 3-90.5) + Soviet doctrine (FM 100-2-1, PU-48 TRY2) + WWII/Korea historical lessons + tropical riverine adaptation + Ukraine LSCO lessons + Siverskyi Donets 2022 + IRB MLC 120; (+4 Exa 2026-06-14) Military Review 2026 doctrine-reconsideration (M18 DSB, anti-drone crossing TTPs), Oskil EW-umbrella-vs-fiber-optic, France Syfrall MLC85/100, conditions-not-clock wet-gap | 2026-06-14 | ✓ |

**Total facets:** 1  
**Split trigger:** > 50 sources → temporal split (pre-2000 foundational doctrine / post-2000 LSCO + modern systems)  
**Current status:** ✓ No split — 45 sources, headroom to 50. (2026-06-14 CEO decision: trigger raised 45→50 instead of fragmenting. Rationale: this is a cross-temporal synthesis council — the 2025-26 drone-age sources only have meaning *next to* the foundational FMs, so a pre/post-2000 split degrades query quality; re-ingesting ~20 globalsecurity/bits.de/dtic/cgsc/history.army.mil PDFs would also re-create the blocked-stub problem cleaned this session. Use `cross_notebook_query` if a genuine 2nd facet ever emerges.)

## ADD Pipeline History

| Date | Action | Sources added | Notes |
|------|--------|:-------------:|-------|
| 2026-05-28 | Initial ADD | 33 | Full ingestion: 12 T1 + 11 T2 + 7 T3 + 3 TRY2 text compilations. No facet split needed. 8-query extraction completed. Studio artifacts created. |
| 2026-05-28 | REFRESH | +7 (→40) | R2 search found 8 new + 1 retry. Ingested 6 URL + 1 TRY2 text. Skipped 1 (Mick Ryan paywall T3). AUSA URL still blocked (TRY2 f6bda25d remains). Delta: Siverskyi Donets case study, IRB MLC 120 approval, MRBC shortfall analysis, UAS threat doctrine, upstream infrastructure risk, GCTC. |
| 2026-06-14 | `--update use exa` + hygiene | +4 / −7 dup-stub (→45) | ⚠ Found notebook DRIFTED to 47 (registry said 40; unlogged URL bulk-adds incl. **6 duplicate pairs**: FM 3-34.343, FM 5-100, FM 90-13 TOC, globalsecurity FM 3-34/FM 3-90-12/FM 5-277). Deleted the 6 dup copies + 1 async Yahoo stub. Added 4 fresh 2026 sources: Military Review "Reconsider River-Crossing Doctrine" (`1c18a12b` — M18 DSB, kedge-anchors not BEBs, EM-signature cut, floating ped bridges), Oskil EW-umbrella-vs-fiber-optic (`6c7f39e3`, text), France Syfrall heavy floating bridge MLC85C/100R (`a3c40657`), Military Review "Condition Checks: Wet-Gap" conditions-not-clock (`3760f0e3`). Now AT split trigger. |

## Studio Artifacts (primary facet)

| Artifact | Status | Created |
|----------|--------|---------|
| Briefing Doc | Created | 2026-05-28 |
| Audio Deep Dive | Created | 2026-05-28 |
| Quiz (5Q) | Created | 2026-05-28 |
| Flashcards (decision rules) | Created | 2026-05-28 |

## Query Config

- **Persona configured:** `chat_configure(goal="custom", custom_prompt=<from references/persona.md>)`
- **Last configure date:** 2026-05-28
- **Persona version:** 1.0
