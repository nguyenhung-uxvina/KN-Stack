---
name: brendan-schulman-seed-sources
type: source registry
notebook_id: 329abb9e-554a-4f8e-a519-7a7174cf73d3
last_updated: 2026-06-14
---

# Seed Sources — mentor-brendan-schulman

Total: 19 sources (10 DJI-era survivors + 9 added 2026-06-14 via Exa). See "Rebuild 2026-06-14" section at the bottom for the new sources. The 10 DJI-era sources below are the survivors after the 2026-06-14 junk purge (11 dead-link/Cloudflare stubs removed).

## Tier 1 — Direct Primary (own writings, testimony, case coverage)

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T1-01 | "Setting the Record Straight on DJI Drone Data Security" (DJI ViewPoints, Jan 6, 2020) | https://www.dji.com/newsroom/news/setting-the-record-straight-on-dji-drone-data-security | 1dc193f5 | DJI Local Data Mode, data isolation architecture, AES-256 encryption, government security assessments, NDAA Section 848 |
| T1-02 | "How I Know DJI Doesn't Have Your Drone Data" (DJI ViewPoints, May 16, 2020) | https://www.dji.com/newsroom/news/how-i-know-dji-doesnt-have-your-drone-data | e0e66864 | Technical explanation of data flow architecture, Local Data Mode implementation, flight data storage, no cloud transmission during flight |
| T1-03 | "We Strongly Support Drone Remote ID. But Not Like This." (DJI ViewPoints, Jan 14, 2020) | https://www.dji.com/newsroom/news/we-strongly-support-drone-remote-id-but-not-like-this | d57899e6 | Broadcast Remote ID advocacy, network Remote ID critique, subscription fee analysis (20% cost-of-flight tax), privacy concerns |
| T1-04 | "FAA Remote ID: What it Means for You and Your DJI Drone" (DJI ViewPoints, Apr 19, 2021) | https://www.dji.com/newsroom/news/faa-remote-id-what-it-means-for-you-and-your-dji-drone | c6d4d2a5 | Final FAA Remote ID rule analysis, broadcast Remote ID implementation, compliance timeline, practical implications for drone operators |
| T1-05 | "You Already Knew Drones Are Safe. Here's More Proof, By The Numbers." (DJI ViewPoints, Nov 20, 2020) | https://www.dji.com/newsroom/news/you-already-knew-drones-are-safe-heres-more-proof-by-the-numbers | aa12acfe | 87.8M US drone flights 2019 / 10.3M flight hours / zero fatalities — proportionate regulation foundation data |
| T1-06 | "Why Did DJI Create a 249-Gram Drone?" (DJI ViewPoints, May 10, 2022) | https://www.dji.com/newsroom/news/why-did-dji-create-a-249-gram-drone | 4aafb6af | Sub-250g weight threshold rationale, global regulatory alignment (FAA/EASA/CASA/Transport Canada), DJI Mini design engineering |
| T1-07 | "Raising Standards: An Update On DJI's 'Elevating Safety' Drone Safety Plan" (DJI ViewPoints, Jul 14, 2021) | https://www.dji.com/newsroom/news/raising-standards-an-update-on-djis-elevating-safety-drone-safety-plan | f66b25d6 | DJI safety plan components: geofencing, ADS-B, remote ID, registration, education programs — industry self-regulation model |
| T1-08 | Smithsonian Magazine "Brendan Schulman v. the FAA" (Huerta v. Pirker narrative) | https://www.smithsonianmag.com/air-space-magazine/brendan-schulman-v-faa-180975337/ | 0d275f69 | Huerta v. Pirker (2014) case narrative, NTSB ALJ ruling, FAA appeal, legal precedent for drone-specific frameworks, Schulman career origin story |
| T1-09 | U.S. Senate Commerce Committee testimony (2017) | https://www.commerce.senate.gov/2017/5/drone-innovation-and-safety | 092fa6de | Congressional testimony: proportionate regulation advocacy, Remote ID position, data security framework, competitive regulation risk (foreign manufacturers), commercial drone industry development |

## Tier 2 — Reference

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T2-01 | DJI ViewPoints author page — Brendan Schulman | https://www.dji.com/newsroom/author/brendan-schulman | 89cf9dd8 | Full article index for Schulman's DJI publications; used as discovery/completeness check |

## Failed Ingests

*(None recorded for this notebook)*

## Refresh Strategy

**Important note (corrected 2026-06-14):** Schulman left DJI in Sept 2021 (not 2022) and is **VP of Policy & Government Relations at Boston Dynamics** — NOT Covington & Burling (prior note was wrong). He has pivoted to robotics policy (Responsible Robotics Act) while retaining drone-law expertise.

**Primary new content to watch:**
- Boston Dynamics robotics-policy output by Schulman (Responsible Robotics Act in new states, weaponization-ban advocacy, UN/Geneva AI-for-Good)
- Congressional / state-legislature testimony (Schulman is periodically called as expert witness)
- Commentary on the China-drone-ban arc (NDAA §1709, Countering CCP Drones Act, FCC Covered List, Section 848/899/1043)
- EU drone & AI/robotics regulation commentary (EASA, EU AI Act)
- @robotpolicy / @dronelaws posts

**Refresh trigger:** New Schulman testimony, significant NDAA drone/robotics provision, Responsible Robotics Act movement in a new state, or a new China-drone-ban development.

**Split trigger:** Unlikely to exceed 45 sources given scope; no split planned.

---

## Rebuild 2026-06-14 (Exa Channel 0 semantic discovery) — +9 → 19 total

CEO source-selection gate → Tier 1 + Tier 2. Discovery: Exa `web_search_exa`, 4 queries. AI-Business robot-ethics piece dropped as thin/video-only; 1 async raw-URL dup deleted.

### Tier 1 — Schulman's own voice + the landmark ruling
| Title | URL | Source ID | Coverage |
|-------|-----|-----------|----------|
| NTSB *Huerta v. Pirker* full decision (Order EA-5730, Nov 18 2014) | https://www.ntsb.gov/legal/alj/OnODocuments/Aviation/5730.pdf | fd839441 | The actual landmark ruling: UAS are "aircraft" under 14 CFR §1.1 / 49 USC §40102; §91.13(a) careless/reckless applies; ALJ reversed & remanded. Schulman's defining case. |
| "Grounding China's Drones" — Sinica/The China Project podcast (May 2020) | https://thechinaproject.com/podcast/grounding-chinas-drones-leading-drone-maker-djis-brendan-schulman-on-u-s-regulatory-challenges/ | 8530a7b4 | Schulman first-person on US Country-of-Origin scrutiny of DJI, draft executive order, DOI program, no signs of CCP influence in 5 yrs, COVID drone use |
| Boston Dynamics + MassRobotics testimony to ban arming robots (WCVB, Nov 2023) | https://www.wcvb.com/article/massachusetts-armed-robots-legislation-terminator-robocop/45919791 | a3d618a2 | Schulman MA Joint Judiciary testimony on S2483/H4103 — covers robotic devices AND drone aircraft; DoD/LE/AG-waiver carve-outs; ACLU partnership |
| Boston Dynamics' push for the Responsible Robotics Act (TechHQ, Oct 2024) | https://techhq.com/news/boston-dynamics-push-for-the-responsible-robotics-act/ | e3e048ba | In-depth Schulman interview: warrants for robot entry; anti-weaponization; MA→CA (Weber)→NY; UN Geneva AI-for-Good; "manufacturers can't police customer use" |
| RDQ v. FAA lawsuit & Remote ID with Schulman (DroneXL/PiXL show, Aug 2022) | https://dronexl.co/2022/08/03/rdq-faa-lawsuit-remote-id-brendan-schulman/ | 42a47fd2 | RaceDayQuads (Tyler Brennan) v. FAA over Remote ID — Schulman's last major drone-era legal commentary |
| Schulman DJI→Boston Dynamics farewell + career (DroneDJ, Sep 2021) [text] | https://dronedj.com/2021/09/10/breaking-brendan-schulman-leaving-dji/ | bc885855 | His farewell statement: "end of a mission" on Remote ID/ops frameworks; politicization as threat to innovation; 730+ rescues; @robotpolicy launch; full CV |

### Tier 2 — China-drone-ban landscape (WX-critical context)
| Title | URL | Source ID | Coverage |
|-------|-----|-----------|----------|
| Countering CCP Drones Act in NDAA FY2025 §1709 (DRONELIFE, Dec 2024) | https://dronelife.com/2024/12/08/fy-2025-ndaa-conference-text-what-happened-with-the-countering-ccp-drones-act/ | 76e37e11 | §1709: national-security agency must assess DJI/Autel within 1 yr; FCC Covered List in 30 days; auto-add if no study; bandwidth ban mechanism |
| DJI official NDAA response (DRONELIFE, Dec 2024) | https://dronelife.com/2024/12/09/dji-responds-calls-for-fair-assessment-in-ndaa-drone-legislation/ | 07341415 | DJI's due-process argument: technical/evidence-based audit + right-of-reply, not automatic origin-based listing — the Schulman doctrine |
| Senate Armed Services hearing — American small-drone industrial base (Mar 3 2026) | https://www.armed-services.senate.gov/download/full-transcript_03-03-2026 | ba8933ee | §1709 implemented by FCC; "Drone Dominance" program; JIATF-401 counter-UAS; China-component onshoring; per-unit cost gap below $2k |

**Dropped:** AI Business "Schulman on AI-enabled robot ethics" (2024) — thin 1-min video page, no substantive text.
