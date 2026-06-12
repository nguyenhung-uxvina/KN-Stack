---
name: missy-cummings-seed-sources
type: source registry
notebook_id: f03036c0-348f-4b8b-8dd3-ae0d4867d5dd
last_updated: 2026-05-23
---

# Seed Sources — mentor-missy-cummings

Total ingested: 11 sources (T1×10, T2×1)

## Tier 1 — Direct Primary (interviews, testimony, research)

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T1-01 | Carnegie Council "The Promise & Peril of AI & Human Systems Engineering" (Oct 2021) | https://www.carnegiecouncil.org/media/article/the-promise-peril-of-ai-human-systems-engineering | 3c0ca0ec | RICHEST SOURCE: vigilance decrement (physiological), Guardian AI concept, mode confusion (Air France 447), neuromuscular lag (~0.5s), safe-mode defaults, static vs. dynamic targets, conscript operator design requirements |
| T1-02 | McKinsey "From fighter pilot to robotics pioneer: Missy Cummings on the promises and perils of AI" (Sep 2021) | https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/from-fighter-pilot-to-robotics-pioneer | 8a565883 | Career narrative, F/A-18 combat experience informing autonomy research, human-autonomy interaction philosophy, AI hype critique, timeline realism |
| T1-03 | GovInfo "The Future of Unmanned Aviation" — Senate testimony (Jan 15, 2014) | https://www.govinfo.gov/content/pkg/CHRG-113shrg89867/html/CHRG-113shrg89867.htm | de62054f | Congressional testimony: drone safety standards, autonomous systems in national airspace, human factors in UAS operations, certification requirements |
| T1-04 | Union of Concerned Scientists "When Will Autonomous Vehicles be Safe Enough?" interview | https://www.ucsusa.org/resources/when-will-autonomous-vehicles-be-safe-enough | 0805a440 | Autonomous vehicle safety thresholds, statistical comparison to human drivers, regulatory certification challenge, "safe enough" definition, timeline critique |
| T1-05 | GMU MARC "Missy Cummings — Mason Autonomy and Robotics Center" profile | https://autonomy.gmu.edu/people/missy-cummings/ | eef54edf | Current research focus, lab overview, recent publications list, institutional context |
| T1-06 | "Prohibiting Generative AI in any Form of Weapon Control" — NeurIPS 2025 Position Paper | https://openreview.net/forum?id=uEY7kQsiZz | 070ba107 | SRKE framework (Skills-Rules-Knowledge-Expertise), hallucination stats (28.6-79%), GPT-4 planning success ~12%, moratorium argument, 30yr drones vs 6yr GenAI timeline, danger zone matrix |
| T1-07 | "Lethal Autonomous Weapons: Meaningful Human Control or Meaningful Human Certification?" — IEEE Technology and Society Magazine Vol.38 No.4 (2019) | https://technologyandsociety.org/lethal-autonomous-weapons-meaningful-human-control-or-meaningful-human-certification/ | 6f384839 | Meaningful human certification reframe, Operation Provide Comfort 1994 case study (26 killed, 130 errors), Chinese Embassy Belgrade 1999, obligation reversal thesis, manufacturer indemnification ban argument |
| T1-08 | "Missy Cummings shows risks of unfettered AI in Voices of Discovery lecture" — Elon University (Nov 18, 2024) | https://www.elon.edu/u/news/2024/11/18/missy-cummings-shows-risks-of-unfettered-ai-in-voices-of-discovery-lecture/ | d8584a52 | GenAI psychopath characterization, non-deterministic vs deterministic AI distinction, danger zone (nondeterministic + safety-critical), medical AI misdiagnosis risk |
| T1-09 | "Podcast: Artificial Intelligence is Artificial and Not Intelligent" — George Mason University (Jan 2023) | https://www.gmu.edu/news/2023-01/podcast-missy-cummings-artificial-intelligence-artificial-and-not-intelligent | 9f446762 | Spider/shoot-shoot cue story (near-miss on commanding officer), Asiana Airlines SFO crash (automation skill degradation), video-game complacency effect, NHTSA Tesla Autopilot investigation context |
| T1-10 | "Ethics 2014 — Mary Cummings: The Human Role in Autonomous Weapon Design and Deployment" — YouTube lecture (2014) | https://www.youtube.com/watch?v=iswXRql8m0Q | cc0066b6 | Human-on-the-loop vs human-in-the-loop definitions, brain drain from defense to commercial (Google/Boston Dynamics), foundational supervisory control framework, early autonomous systems taxonomy |

## Tier 2 — Authoritative Secondary (collaborative/policy)

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T2-01 | RAND "Autonomous Vehicle Technology: A Guide for Policymakers" | https://www.rand.org/pubs/research_reports/RR443-2.html | 4b98084c | Policy framework for autonomous systems deployment, safety certification challenges, regulatory design principles — Cummings cited contributor |

## Failed Ingests

*(None recorded for this notebook)*

## Refresh Strategy

**Primary new content to watch:**
- New Carnegie Council / Brookings / RAND publications by Cummings
- Congressional testimony on AI weapons governance (Cummings testifies regularly)
- GMU MARC research publications on human-autonomy interaction
- FAA safety advisor follow-on publications
- Academic journal papers (Cummings publishes in human factors, IEEE journals)

**Refresh trigger:** New Congressional testimony on AI/autonomous weapons, or major new academic publication on human-autonomy interaction.

**Split trigger:** If source count exceeds 45 → consider topical split:
- `civil-autonomy` — autonomous vehicles, civilian aviation, FAA context
- `military-autonomy` — AI weapons governance, military human-machine teaming, FCS design

**Note on source depth:** Current 6-source base is lean. High-priority additions on next refresh:
- Cummings' peer-reviewed publications on human supervisory control
- Additional Congressional testimonies (multiple on record 2014-2024)
- Brookings Institution pieces on autonomous weapons policy
- IEEE Transactions on Human-Machine Systems articles
