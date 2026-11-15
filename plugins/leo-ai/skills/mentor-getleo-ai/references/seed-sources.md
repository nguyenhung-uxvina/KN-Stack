# Seed Sources — mentor-getleo-ai

NotebookLM notebook: **Research: Leo AI (getleo.ai) — LMM + tích hợp Workshop X**
ID: `2848c37a-e029-4bec-a2db-cdb5b56a3f8b` · 11 sources · created 2026-06-26.

Tier scheme: T1 = official getleo.ai material · T2 = authoritative trade press / independent review · T3 = SEO/blog explainer.

## Cited sources (confirmed in extraction)

| # | source_id | Description | Tier |
|---|-----------|-------------|:----:|
| 1 | 3446a3c0-429b-4850-85cd-021d7307518f | getleo.ai — "Best Text-to-CAD Tools 2026 / Find Parts Before You Generate" (geometry-aware search) | T1 |
| 2 | 233bc62f-c5a6-4986-b0a1-2fb2d1b65660 | Michelle Ben-David — text-to-CAD teardown (mesh vs parametric; Zoo.dev; bottom line) | T1 |
| 3 | a7208c50-4236-492c-98e6-38a3316a2a3e | appvizer — Leo AI overview/review (benefits, pricing, 55k engineers) | T2 |
| 4 | 137273a4-b73c-45f4-ad96-afc7525fe3c0 | getleo.ai homepage — "Unlock Legacy Knowledge", enterprise security | T1 |
| 5 | 16a49d14-e201-4f5a-be0b-fbed3a71ca8c | getleo.ai — first patent announcement (US 18/907,937, auto CAD assembly) | T1 |
| 6 | 10e2a9e3-ac9f-4e2e-9090-47ff23fd504a | machinedesign.com — Farid interview (LMM, BREP, 96% vs 46%, SOC2, embedding vectors) | T2 |
| 7 | 6ce17639-2db7-4a95-af9b-f51d1bc52dea | getleo.ai — "How We Do It" + Leadership (Farid, Moravia, Unit 81) | T1 |
| 8 | ee328650-3db2-4dc0-ac1f-8e1799fddb67 | "GetLeo AI Pro Builder Guide" — prompting bad-vs-good, draft/render, 9-point summary | T3 |

## Not-yet-cited in extraction (in notebook, 3 remaining)
The notebook holds 11 sources total; the 8 above carried the cited content across the 3 extraction queries. The remaining ~3 are supporting/duplicate-topic articles — confirm via `nlm source list 2848c37a-…` at next REFRESH and tier them.

## Key facts harvested (with anchor sources)
- LMM, parts-as-tokens, BREP understanding [6,7]; 96% vs GPT 46%, >1M sources, 120M vendor parts [6,16a].
- Part reuse: 60–80% of new parts are duplicates; Leo +32% reuse, −34% mistakes, ~5–12h/week saved [1,3].
- PDM/PLM: SolidWorks PDM, Autodesk Vault, PTC Windchill, Siemens Teamcenter, Arena; text/CAD-to-CAD search [1].
- Limits: text-to-CAD = MESH (STL/OBJ), not editable/tolerance-able/machinable [1,2]; human final validation mandatory [8].
- Security: SOC2 + GDPR, zero training on data, embedding-vector index (no file move, not reverse-engineerable), **cloud-based**; on-prem/air-gap [UNCERTAIN — not in sources].
- Founders: Maor Farid (CEO), Moti Moravia (CTO) — Technion / Unit 81 / Israeli MOD [7].
