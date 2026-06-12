# Notebooks Index — mentor-military-combat-engineer-council

Facet registry for this mentor. Updated each ADD or REFRESH.

## Facet Registry

| Facet | NLM URL | Notebook ID | Source count | Scope | Last refresh | Primary? |
|-------|---------|-------------|:------------:|-------|:------------:|:--------:|
| primary | https://notebooklm.google.com/notebook/2cb1a634-90e6-4ce6-acb5-d747d45165b2 | `2cb1a634-90e6-4ce6-acb5-d747d45165b2` | 40 | All doctrine: US FMs (FM 90-13, FM 3-34, FM 3-90.12, TC 5-210, ATP 3-90.5) + Soviet doctrine (FM 100-2-1, PU-48 TRY2) + WWII/Korea historical lessons + tropical riverine adaptation + Ukraine LSCO lessons + Siverskyi Donets 2022 failure analysis + IRB MLC 120 update + MRBC shortfall analysis | 2026-05-28 | ✓ |

**Total facets:** 1  
**Split trigger:** > 45 sources → consider temporal split (pre-2000 foundational doctrine / post-2000 LSCO + modern systems)  
**Current status:** No split required (33 sources, well under threshold)

## ADD Pipeline History

| Date | Action | Sources added | Notes |
|------|--------|:-------------:|-------|
| 2026-05-28 | Initial ADD | 33 | Full ingestion: 12 T1 + 11 T2 + 7 T3 + 3 TRY2 text compilations. No facet split needed. 8-query extraction completed. Studio artifacts created. |
| 2026-05-28 | REFRESH | +7 (→40) | R2 search found 8 new + 1 retry. Ingested 6 URL + 1 TRY2 text. Skipped 1 (Mick Ryan paywall T3). AUSA URL still blocked (TRY2 f6bda25d remains). Delta: Siverskyi Donets case study, IRB MLC 120 approval, MRBC shortfall analysis, UAS threat doctrine, upstream infrastructure risk, GCTC. |

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
