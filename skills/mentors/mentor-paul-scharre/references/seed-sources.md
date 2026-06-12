---
name: paul-scharre-seed-sources
type: source registry
notebook_id: 73ce4511-0924-4e4c-be8b-fafc8ede3e3c
last_updated: 2026-05-22
---

# Seed Sources — mentor-paul-scharre

Total ingested: 19 sources (T1×14, T2×3, T3×2)

## Tier 1 — Direct Primary (own writings, speeches, testimony)

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T1-01 | CNAS "Robotics on the Battlefield Part II: The Coming Swarm" (PDF, 2014) | https://s3.us-east-1.amazonaws.com/files.cnas.org/documents/CNAS_TheComingSwarm_Scharre.pdf | fb1fd253 | Swarm warfare doctrine, cost-exchange math, uninhabited arsenal ships |
| T1-02 | CNAS "Autonomous Weapons and Human Control" (2015) | https://www.cnas.org/publications/reports/autonomous-weapons-and-human-control | 633a6c1e | Human-machine teaming policy, control thresholds |
| T1-03 | CNAS "AI and International Stability: Risks and Confidence-Building Measures" (2021) | https://www.cnas.org/publications/reports/ai-and-international-stability-risks-and-confidence-building-measures | 51b628be | Escalation risk, flash wars, CBMs, off-limits geographic areas |
| T1-04 | Congressional Testimony — SASC | https://www.cnas.org/publications/congressional-testimony/paul-scharre-testimony-before-sasc1 | d235eac7 | Senate testimony on autonomous weapons |
| T1-05 | Congressional Testimony — HASC | https://www.cnas.org/publications/congressional-testimony/paul-scharre-testimony-before-hasc | 770b534c | House testimony on LAWS principles |
| T1-06 | Remarks to UN GGE on LAWS | https://www.cnas.org/publications/congressional-testimony/remarks-by-paul-scharre-to-the-united-nations-group-of-governmental-experts-on-lethal-autonomous-weapon-systems-1 | e2a9a4d9 | "What role do we want humans to have in lethal decision-making?" |
| T1-07 | Foreign Affairs "Killer Apps: The Real Dangers of an AI Arms Race" (2019) | https://www.foreignaffairs.com/articles/2019-04-16/killer-apps | 0e63431e | Three risk categories, machine brittleness, arms race framing |
| T1-08 | Foreign Affairs "The Perilous Coming Age of AI Warfare" (2024) | https://www.foreignaffairs.com/ukraine/perilous-coming-age-ai-warfare | ed0df766 | Ukraine/AI intersection, 5 practical governance steps, antipersonnel ban |
| T1-09 | Foreign Affairs "America Can Win the AI Race" | https://www.foreignaffairs.com/united-states/ai-america-can-win-race | 4660c75f | US AI competitiveness strategy |
| T1-10 | 80,000 Hours Podcast — Paul Scharre on AI Warfare & Autonomous Weapons (2025) | https://80000hours.org/podcast/episodes/paul-scharre-ai-warfare-autonomous-weapons/ | 39a0c010 | Most current views: AGI timelines revised, adoption competition, flash war, bio risk |
| T1-11 | Future of Life Institute — LAWS Podcast (2020) | https://futureoflife.org/podcast/on-lethal-autonomous-weapons-with-paul-scharre/ | 433cccdf | LAWS benefits, risks, regulation, arms control analogies |
| T1-12 | Carnegie Council — Army of None Book Talk (2018) | https://www.carnegiecouncil.org/media/series/39/20180501-army-of-none-autonomous-weapons-future-of-war-paul-scharre | 9e0c00d8 | Key frameworks from primary book; human judgment examples |
| T1-13 | War on the Rocks — "Unleash the Swarm: The Future of Warfare" (2015) | https://warontherocks.com/2015/03/unleash-the-swarm-the-future-of-warfare/ | 5aca253a | Swarm tactics doctrine, operational advantages |
| T1-14 | War on the Rocks — "AI At War" (2023) | https://warontherocks.com/2023/04/ai-at-war/ | 87342e8d | Four Battlegrounds themes; AI as intelligence function not just lethality |

## Tier 2 — Authoritative Secondary

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T2-01 | CFR Podcast — "Killer Robots and Autonomous Weapons with Paul Scharre" (2018) | https://www.cfr.org/podcasts/killer-robots-and-autonomous-weapons-paul-scharre | 5e790432 | Policy framing, arms control, flash war analogy |
| T2-02 | Carnegie Council — "AI Warfare: Arms Control & Deterrence" (2024) | https://www.carnegiecouncil.org/media/series/aiei/ai-warfare-arms-control-deterrence-paul-scharre | 111bacae | Most recent 2024 views: chip governance, institutional muscle memory |
| T2-03 | Paul Scharre personal site — Analysis archive | https://www.paulscharre.com/analysis | b7e067fa | Curated commentary |

## Tier 3 — Other

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T3-01 | Just Security — "Autonomy, Killer Robots, Human Control Part I" | https://www.justsecurity.org/12708/autonomy-killer-robots-human-control-force-part/ | 94082a83 | Legal analysis of autonomy and human control (Cloudflare challenge page — may have limited content) |
| T3-02 | Lawfare — "Blame the Pentagon, Not AI, for Preventable Targeting Mistakes" | https://www.lawfaremedia.org/article/blame-the-pentagon--not-ai--for-preventable-targeting-mistakes | ebe8589d | Accountability framework |

**Failed ingests:**
- TIME 100 AI profile (https://time.com/collections/time100-ai/6307703/paul-scharre/) — JavaScript-rendered, dropped by NLM

## Refresh Strategy

**Primary new content to watch:**
- Paul Scharre's CNAS publications (new reports, testimony)
- Foreign Affairs new essays
- New podcast appearances (80,000 Hours, War on the Rocks podcast)
- CNAS National Security Conference presentations
- Congressional testimony on AI/autonomous weapons

**Refresh trigger:** New CNAS report on autonomous weapons, new book, Congressional testimony, or new Foreign Affairs essay.

**Split trigger:** If source count exceeds 45 → consider topical split:
- `primary-doctrine` — LAWS/autonomy (Army of None era, 2014-2022)
- `primary-political-economy` — Four Battlegrounds/AI competition era (2023+)
