---
name: brendan-schulman-notebooks-index
type: facet-registry
mentor: brendan-schulman
last_updated: 2026-06-14
---

# Notebooks Index — mentor-brendan-schulman

| Facet | NLM URL | Notebook ID | Sources | Scope | Last refresh | Status |
|-------|---------|-------------|:-------:|-------|:------------:|:------:|
| primary | https://notebooklm.google.com/notebook/329abb9e-554a-4f8e-a519-7a7174cf73d3 | 329abb9e-554a-4f8e-a519-7a7174cf73d3 | 19 | DJI drone-policy era (ViewPoints 2020-22, Senate testimony 2017, Smithsonian Pirker profile) + **NTSB Huerta v. Pirker full ruling** + Boston Dynamics robotics-policy era (Responsible Robotics Act, weaponization-ban testimony, AI-robot ethics) + China-drone-ban landscape (NDAA FY25 §1709 / Countering CCP Drones Act, DJI response, 2026 Senate small-drone industrial-base hearing) + Sinica China-drones podcast + RDQ v FAA | 2026-06-14 (Exa rebuild) | ACTIVE — rebuilt |

## Query Configuration

**Default:** Query `primary` facet.
**Conversation IDs (last session):** `192920c8-faa7-44a1-b96b-196548b5d5a9`
**Note:** New CONSULT should use `mcp__notebooklm-mcp__notebook_query` without `conversation_id` to start a fresh thread.

## Reconciled 2026-06-14 (registry-drift audit)

count corrected 10→21 to match live notebook (sources added by prior refresh/agent but never logged).

Sources in live notebook NOT previously represented in registry (11 new):

| Source Title | Source ID |
|---|---|
| 404 Page - Page not found - DJI United States (dead link 1) | 5a776b0d-5a60-4004-be6a-cf0f9fb4fccb |
| 404 Page - Page not found - DJI United States (dead link 2) | 7caf24a4-2366-41c4-9adc-bcfb605bfeed |
| 404 Page - Page not found - DJI United States (dead link 3) | 9a68b88c-73e6-47bc-8d79-a6b48bb318a8 |
| 404 Page - Page not found - DJI United States (dead link 4) | bc5f3a65-6d55-48ae-8685-27373a41347c |
| 404 Page - Page not found - DJI United States (dead link 5) | c2639352-3d6d-4586-82f9-ab238890250c |
| ERROR: The request could not be satisfied (dead link) | 70a69789-1046-4566-9fb1-a47de80bd80f |
| Just a moment... (Cloudflare gate — source 1) | 2afc8ead-fb6c-44f4-8170-16cecdb10cee |
| Just a moment... (Cloudflare gate — source 2) | 4d0f0e2c-c19a-4708-af0a-9654015fdc05 |
| Just a moment... (Cloudflare gate — source 3) | 5d11e2e3-b17c-4a24-9fb8-f0916ee78575 |
| Page Not Found (dead link) | 59f6ecff-eba6-4fd9-8b79-0171a1c5fd7c |
| Page not found - U.S. Senate Committee on Commerce, Science, & Transportation | 1208374e-cb75-4d3b-bf62-a6e611e603bb |

Note: 10 of these 11 entries are dead-link/access-blocked stubs (DJI 404s, Cloudflare gates, generic error pages) — they were ingested by the prior agent but returned no substantive content. The Senate Commerce Committee page (1208374e) may have been a secondary testimony page linked from the primary testimony source already in the registry.

## Junk purge 2026-06-14

Purged 11 junk dead-link/blocked stubs from NLM (count 21→10): 5× DJI 404, 1× "ERROR: request could not be satisfied", 3× Cloudflare "Just a moment…", 1× "Page Not Found", 1× Senate-Commerce 404.

**WARNING — notebook now needs a real source rebuild.** ~Half the total sources in this notebook were dead links. With only 10 real sources, advisor quality is severely degraded. Priority action: run `--refresh` to find and ingest live Schulman content (DJI Newsroom archives, Covington & Burling publications, YouTube testimony recordings, podcast appearances).

Kept-but-flagged: none — all ambiguous stubs were deleted.

## ✅ Rebuild 2026-06-14 (`update use exa` — Exa Channel 0) — REBUILD DONE, count 10 → 19

Discovery: Exa MCP `web_search_exa` (Channel 0), 4 semantic queries. CEO source-selection gate → chose Tier 1 + Tier 2. The above WARNING is now RESOLVED.

**Persona corrected:** Schulman is NOT at Covington & Burling — he has been **VP of Policy & Government Relations at Boston Dynamics since Sept 2021**, pivoted from drone law to robotics policy (Responsible Robotics Act). `references/persona.md` updated accordingly.

**9 new sources added** (10 selected; AI-Business robot-ethics piece DROPPED as thin/video-only):

| Tier | Source | NLM id |
|------|--------|--------|
| T1 | NTSB *Huerta v. Pirker* full decision (2014, the landmark ruling itself — notebook previously had only the Smithsonian narrative) | fd839441 |
| T1 | Sinica/The China Project podcast (2020) — "Grounding China's drones," Schulman on China-drone security + US regulation | 8530a7b4 |
| T1 | WCVB (2023) — Schulman testimony to MA Joint Judiciary on the weaponized-robot/drone ban bill (S2483/H4103) | a3d618a2 |
| T1 | TechHQ (2024) — Schulman on the Responsible Robotics Act (warrants, anti-weaponization, ACLU partnership, MA/CA/NY) | e3e048ba |
| T1 | DroneXL (2022) — RDQ v. FAA lawsuit & Remote ID with Schulman (last major drone-era legal commentary) | 42a47fd2 |
| T1 | DroneDJ (2021) — Schulman DJI→Boston Dynamics farewell statement + career (text; raw-URL async dup deleted) | bc885855 |
| T2 | DRONELIFE (2024) — Countering CCP Drones Act in NDAA FY25 §1709 (FCC Covered List mechanism) | 76e37e11 |
| T2 | DJI official NDAA response (2024) — technical-audit + right-of-reply argument | 07341415 |
| T2 | Senate Armed Services hearing (Mar 2026) — American small-drone industrial base (Drone Dominance, §1709 implemented, China-component sourcing) | ba8933ee |

Dropped: AI Business "robot ethics" (2024) — thin 1-min video page, no substantive text (Cloudflare stub `129c5508` deleted).
Hygiene: deleted 1 async raw-URL dup of the DroneDJ source (`92022477`). Final = **19 clean sources**, no stubs.
