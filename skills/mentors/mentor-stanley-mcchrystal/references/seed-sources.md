---
name: mcchrystal-seed-sources
type: source-registry
mentor: stanley-mcchrystal
notebook_id: 718dec71-a19e-4a7e-9e62-d645d8e39969
created: 2026-05-23
total_sources: 16
---

# Seed Sources — mentor-stanley-mcchrystal

## Ingested Sources (16 total)

| # | Tier | Source ID | Title | Year | URL | Signal |
|---|------|-----------|-------|------|-----|--------|
| T1-01 | T1 | `d5188aac` | Tim Ferriss #535 — "Mastering Risk: A User's Guide" | Oct 2021 | https://tim.blog/2021/10/04/general-stanley-mcchrystal-transcript/ | ★★★ richest single source (~15k word transcript) |
| T1-02 | T1 | `bb667a64` | DVIDS Leadership List — Team of Teams Ep 03 | Jun 2020 | https://www.dvidshub.net/news/372348/transcript-leadership-list-podcast-stanley-mcchrystal-team-teams-episode-03 | ★★★ verbatim transcript, widest framework coverage |
| T1-03 | T1 | `0b02e912` | TED Talk — "Listen, Learn, Then Lead" | (classic) | https://www.youtube.com/watch?v=FmpIMt95ndU | ★★★ iconic framework talk |
| T1-04 | T1 | `f9a27f22` | Knowledge Project #132 — "Masterclass on Leadership" | Mar 2022 | https://www.youtube.com/watch?v=-qVVcDi3s9c | ★★★ |
| T1-05 | T1 | `44c25711` | On Character — McChrystal Group interview | May 2025 | https://www.mcchrystalgroup.com/insights/detail/2025/05/30/on-character--a-conversation-with-general-stan-mcchrystal | ★★★ newest book launch |
| T1-06 | T1 | `a77a7c39` | CBS Face the Nation — On Character transcript | May 2025 | https://www.cbsnews.com/news/stanley-mcchrystal-retired-general-face-the-nation-transcript-05-18-2025/ | ★★ |
| T1-07 | T1 | `bf27acff` | From the Green Notebook Ep 147 — On Character | May 2025 | https://fromthegreennotebook.com/2025/05/23/ep-147-on-character-with-general-stanley-mcchrystal/ | ★★ |
| T1-08 | T1 | `0b451b20` | Staffbase "Aspire to Inspire" — trust + transformation | Oct 2024 | https://staffbase.com/podcasts/aspire-to-inspire/2024/e14-navigating-leadership-challenges-general-mcchrystal-on-trust-teams-and-transformation | ★★★ Ranger Effect + say-do gap best coverage |
| T1-09 | T1 | `639fde38` | LEADERS Magazine — McChrystal Group | Oct 2025 | https://www.leadersmag.com/issues/2025.4_Oct/PUR/LEADERS_McChrystal_McChrystal_Group.html | ★★ Ukraine + keyboard talent quote |
| T1-10 | T2 | `d8a1d718` | Small Wars Journal — On Character review | Oct 2025 | https://smallwarsjournal.com/2025/10/21/on-character-choices-that-define-a-life/ | ★★ Character = Convictions × Discipline formula |
| T1-11 | T1 | `3e4cd735` | Learning Leader #633 — On Character | 2025 | https://learningleader.com/generalstanleymcchrystal/ | ★★★ Ranger Effect + white water rafting quote |
| T1-12 | T1 | `b6543bf5` | Learning Leader #439 — Risk & the Unknown | Oct 2021 | https://learningleader.com/stanmcchrystal439/ | ★★★ Risk immune system + piranha quote |
| T1-13 | T1 | `47806456` | Vanderbilt Lecture — On Character (with Gen. Nakasone) | Sep 2025 | https://www.vanderbilt.edu/national-security/2025/09/18/stanley-mcchrystal-brings-on-character-to-vanderbilt-lecture-series/ | ★★ |
| B1 | T1 | `ceb4693c` | Team of Teams (Army Infantry Magazine full text) | 2015 | https://www.benning.army.mil/infantry/magazine/issues/2015/Jul-Sept/pdfs/Book1-Team%20of%20Teams_TEXT.pdf | ★★★ book full text |
| B2 | T1 | `79b16646` | My Share of the Task (Internet Archive) | 2013 | https://archive.org/details/myshareoftaskmem0000mcch | ★★ memoir |
| B3 | T1 | `b51c687b` | On Character (Google Books preview) | 2025 | https://books.google.com/books/about/On_Character.html?id=mAMrEQAAQBAJ | ★★ Character formula |

## Failed Ingests (TRY2 recoveries)

| # | Original URL | Failure | Recovery |
|---|-------------|---------|---------|
| FC-01 | https://www.fastcompany.com/91447502/stanley-mcchrystal-says-leaders-must-have-good-character-and-strong-convictions | Redirected to Palantir article | TRY2: `91333979` also redirected → replaced with Learning Leader #439 + Vanderbilt |
| EX-01 | https://www.mcchrystalgroup.com/insights/playbooks/detail/... | 404 (playbook behind form) | Dropped — Team of Teams covered by B1 (Army PDF full text) |

## Source Quality Notes

- **Richest sources:** T1-01 (Tim Ferriss #535 — 15k word transcript, Risk book launch), T1-02 (DVIDS — 13.5k word Team of Teams verbatim), T1-08 (Staffbase — Ranger Effect + say-do gap best coverage), T1-11 (Learning Leader #633 — richest On Character + Ranger Effect), T1-12 (Learning Leader #439 — Risk immune system + piranha)
- **Three-book coverage:** Team of Teams (B1 + T1-02 + T1-04 + T1-03); Risk (T1-01 + T1-12); On Character (T1-05 + T1-06 + T1-07 + T1-10 + T1-11 + T1-13 + B3); Memoir (B2)
- **Conversation ID from A5 extraction:** `eeb4e258-9190-4ab4-ac5b-cbb1ae0c2032` — do NOT reuse for new CONSULTs

## Refresh Strategy

- Check for new McChrystal Group insights articles quarterly
- Monitor for new podcast appearances (Learning Leader, Tim Ferriss, Knowledge Project)
- **Split trigger:** >45 sources → `mcchrystal-teams` (Team of Teams/JSOC arc) + `mcchrystal-character` (Risk/On Character arc)
