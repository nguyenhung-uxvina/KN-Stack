---
name: c-uas-council-seed-sources
type: source registry
notebook_id: 107cde20-217d-4429-9f81-91ed979637e1
last_updated: 2026-05-22
---

# Seed Sources — mentor-c-uas-counter-drone-technology-council

Total ingested: 10 sources (T1×7, T2×3)

## Tier 1 — Authoritative Primary (official doctrine, cleared lists, primary reports)

| # | Title | URL | Source ID | Coverage | Pillar |
|---|-------|-----|-----------|---------|--------|
| T1-01 | DIU "Blue UAS Cleared Drone List" (2023) | https://www.diu.mil/blue-uas-cleared-list | 99b9be62 | DoD-approved commercial UAS/C-UAS platforms, supply chain clearance, data security verified | Technology |
| T1-02 | Army ATP 3-01.81 "Counter-Unmanned Aircraft System Techniques" (Aug 2023) | https://armypubs.army.mil/epubs/DR_pubs/DR_a/ARN36290-ATP_3-01.81-000-WEB-1.pdf | c1ca5f81 | Employment doctrine, kill chain procedures, unit-level C-UAS integration, EW deconfliction, engagement windows | Doctrine |
| T1-03 | CNAS "Countering the Swarm: Lessons from the Red Sea" (Sep 2025) | https://www.cnas.org/publications/reports/countering-the-swarm | 831decef | Red Sea Houthi campaign analysis, cost-exchange table, Fabian strategy documentation, stockpile depletion data, 9-20 second engagement window ← RICHEST SOURCE |
| T1-04 | CSIS "Countering Small Uncrewed Aerial Systems: A Framework for Analysis" (PDF, Nov 2023) | https://csis-website-prod.s3.amazonaws.com/s3fs-public/2023-11/231114_Harrison_Countering_UAS.pdf | d330ec39 | Analytical framework: detection/tracking/ID/defeat layers, cost-exchange analysis, procurement recommendations | Research |
| T1-05 | DoD C-UAS Fact Sheet (Dec 2024) | https://www.defense.gov/News/Releases/Release/Article/3998763/ | 1f7a9bc2 | Current DoD C-UAS systems inventory, program status, fielded capabilities, service integration | Technology |
| T1-06 | DoD "Counter-Small Unmanned Aircraft Systems Strategy" (Jan 2021) | https://media.defense.gov/2021/Jan/07/2002563945/-1/-1/1/DEPARTMENT-OF-DEFENSE-COUNTER-SMALL-UNMANNED-AIRCRAFT-SYSTEMS-STRATEGY.PDF | 2e8afc52 | Joint strategy framework, threat characterization (Group 1-5), layered defense concept, acquisition strategy | Doctrine |
| T1-07 | RUSI "Protecting the Force from Uncrewed Aerial Systems" (Oct 2024) | https://rusi.org/explore-our-research/publications/special-resources/protecting-force-uncrewed-aerial-systems | 8a8c787f | Ukraine/Middle East operational lessons, passive sensor priority, EW fratricide analysis, drone-on-drone intercept data | Research |

## Tier 2 — High-Quality Secondary (congressional, analytical)

| # | Title | URL | Source ID | Coverage | Pillar |
|---|-------|-----|-----------|---------|--------|
| T2-01 | GAO-22-105705 "Counter-Drone Technologies: Actions Needed to Strengthen DoD's Efforts" (2022) | https://www.gao.gov/assets/gao-22-105705.pdf | edd38621 | DoD C-UAS program gaps, acquisition fragmentation, interoperability failures, procurement reform recommendations | Research |
| T2-02 | RAND RR3023 "Small Unmanned Aerial System Adversary Capabilities" | https://www.rand.org/pubs/research_reports/RR3023.html | 95066a22 | Adversary UAS threat characterization, commercial drone military adaptation, COTS drone proliferation | Research |
| T2-03 | CRS R48477 "Counter-Unmanned Aircraft Systems" (Mar 2025) | https://crsreports.congress.gov/product/pdf/R/R48477 | 06d0588a | Congressional research service overview: current capabilities, funding gaps, legislative actions, FY25 priorities | Research |

## Failed Ingests

*(None recorded for this notebook)*

## Refresh Strategy

**Primary new content to watch:**
- New CNAS C-UAS / drone warfare reports
- Army ATP updates (ATP 3-01.81 revision cycle)
- DoD C-UAS annual fact sheets / program updates
- Red Sea / Ukraine operational lessons learned reports
- CRS updates to R48477 (published annually)
- New DIU Blue UAS list additions

**Refresh trigger:** New CNAS/CSIS/RUSI operational lessons report, updated Army doctrine, or new DoD C-UAS program announcements.

**Split trigger:** If source count exceeds 45 → consider topical split:
- `doctrine` — Army ATP 3-01.81, DoD Strategy, employment procedures
- `technology` — Blue UAS list, DoD Fact Sheets, system specifications
- `research` — CNAS, CSIS, RAND, RUSI, GAO, CRS analysis
