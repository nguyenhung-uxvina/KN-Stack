---
name: robert-work-notebooks-index
type: facet-registry
mentor: robert-work
last_updated: 2026-06-14
---

# Notebooks Index — mentor-robert-work

| Facet | NLM URL | Notebook ID | Sources | Scope | Last refresh | Status |
|-------|---------|-------------|:-------:|-------|:------------:|:------:|
| primary | https://notebooklm.google.com/notebook/7cd03ea2-513d-4089-9f28-614899f13133 | 7cd03ea2-513d-4089-9f28-614899f13133 | 17 | CNAS 20YY + Pentagon speeches (2015-2016) + JFQ-84 + WotR (2019-2021) + CNAS Autonomous Weapons + Data Principles + Breaking Defense + Nextgov/FCW | 2026-05-22 (reconcile + purge 2026-06-14; ambiguous-review purge 2026-06-14) | ACTIVE — clean |

## Query Configuration

**Default:** Query `primary` facet.
**Conversation IDs (last session):** `d5d6e360-579e-44df-8572-acaaf5f01bee`
**Note:** New CONSULT should use `mcp__notebooklm-mcp__notebook_query` without `conversation_id` to start a fresh thread, OR use the last `conversation_id` to continue the context thread.

## Reconciled 2026-06-14 (registry-drift audit)

count corrected 13→28 to match live notebook (sources added by prior refresh/agent but never logged).

Sources in live notebook NOT previously represented in registry (15 new):

| Source Title | Source ID |
|---|---|
| CNAS (generic — article 1) | 450f3655-e1ca-4807-909d-bab628882dd2 |
| CNAS (generic — article 2) | 7c659f53-e0fe-442a-8e44-6652cfa743ea |
| CNAS (generic — article 3) | 870b5431-c23d-4d01-9fa9-f3d29d1df3bc |
| CNAS (generic — article 4) | a1557f03-856b-4475-8792-7a37f01b6de7 |
| The (War)Games We Play | 7c14ab0f-38cd-4662-a570-27567fa5b8f4 |
| https://breakingdefense.com/2015/08/this-is-the-brain-of-the-third-offset-strategy-robert-work/ | a375d1ae-a22a-4cb8-9f5f-693510e261e3 |
| Presidential Advisers Recommend Countering Cyberattacks, Shootings with Big Data - Nextgov/FCW | 4c4f0134-18e9-4190-a615-7e5a98943bb4 |
| 404 Error (dead link — source 1) | f5ad48fb-0fc9-4f82-b66d-31d27a4ec3c8 |
| 404 Not Found (dead link — source 2) | 984c2028-0579-416b-9bc7-4fe0bc058dc2 |
| PAGE NOT AVAILABLE (Error 404) \| RAND | 621b08d1-7265-4069-a163-b07b7713f73d |
| Page Not Found \| CSIS | e89d6814-991c-45e7-adf4-da30cb0509d1 |
| Page not found - Atlantic Council | a4e133c4-3044-43c3-a881-7e2505f468be |
| Page not found - War on the Rocks (dead link 1) | 20ea40a2-eb27-4aa9-b754-a0cbeb6cc99d |
| Page not found - War on the Rocks (dead link 2) | b18efa8f-e571-4993-8e04-11321aa1bba5 |
| Steering in the Right Direction in the Military-Technical Revolution | e6c10cf7-339a-4523-9a50-cdb4eb4d444d |

Note: Several entries (4× "CNAS", 7× dead-link stubs) have no descriptive titles in NLM — they are URL-ingested pages that returned 404 or generic landing pages at crawl time. Content value is limited; they are retained as ingested by the prior agent.

## Junk purge 2026-06-14

Purged 7 dead-link 404 stubs from NLM (count 28→21): RAND 404, CSIS 404, Atlantic-Council 404, War-on-the-Rocks×2 404, 2× generic 404.

## Ambiguous-review purge 2026-06-14 (count 21→17)

The 4 bare-titled "CNAS" sources (450f3655, 7c659f53, 870b5431, a1557f03) were inspected via `source_get_content` — all four are identical CNAS **"404 Page not found"** pages (site nav chrome only, zero article content). Deleted. Notebook now clean at 17 real sources.
