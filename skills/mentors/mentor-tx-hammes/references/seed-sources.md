---
name: tx-hammes-seed-sources
type: source registry
notebook_id: 18dc8984-7646-49a4-bd41-cd527e4b97dd
last_updated: 2026-05-22
---

# Seed Sources — mentor-tx-hammes

Total ingested: 17 sources (T1×13, T2×4)

## Tier 1 — Direct Primary (own writings, speeches)

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T1-01 | NDU Strategic Forum SF-278 "Offshore Control: A Proposed Strategy for an Unlikely Conflict" (PDF, 2012) | https://ndupress.ndu.edu/Portals/68/Documents/stratforum/SF-278.pdf | 076fb376 | Core Offshore Control doctrine — concentric rings, blockade mechanics, theory of victory, escalation management |
| T1-02 | War on the Rocks "Hammes: Strategy and AirSea Battle" (2013) | https://warontherocks.com/2013/07/hammes-strategy-and-airseabattle/ | 4378ae11 | AirSea Battle critique, Offshore Control origin story, OSD-P request, deterrence via blockade |
| T1-03 | War on the Rocks "The Future of Warfare: Small, Many, Smart vs. Few & Exquisite?" (2014) | https://warontherocks.com/2014/07/the-future-of-warfare-small-many-smart-vs-few-exquisite/ | 8bfe3842 | Cost-curve inversion thesis, F-35/carrier trap, battleship→carrier aviation historical analogy |
| T1-04 | NDU JFQ-81 "Cheap Technology Will Challenge U.S. Tactical Dominance" (PDF, 2016) | https://ndupress.ndu.edu/Portals/68/Documents/jfq/jfq-81/jfq-81_76-85_Hammes.pdf | 42a591aa | Technology convergence thesis, interwar battleship failure analogy, UUV/drone economics |
| T1-05 | War on the Rocks "The Democratization of Airpower: The Insurgent and the Drone" (2016) | https://warontherocks.com/2016/10/the-democratization-of-airpower-the-insurgent-and-the-drone/ | 380ae091 | Non-state actor drone threat, "bring the detonator" concept, cheap drones vs. exquisite bases |
| T1-06 | NDU Strategic Forum SF-214 "Insurgency: Modern Warfare Evolves into a Fourth Generation" (2005) | https://digitalcommons.ndu.edu/strategic-forums/14/ | 60ca3e20 | 4GW foundational framework — political will as target, all-domain warfare, non-state parity |
| T1-07 | NDU Strategic Forum SF-307 "Baltics Left of Bang: Comprehensive Defense in the Baltic States" (PDF, 2020) | https://ndupress.ndu.edu/Portals/68/Documents/stratforum/SF-307.pdf | 7ffb85d4 | Comprehensive defense doctrine, coalition sea denial, NATO small-nation deterrence |
| T1-08 | Atlantic Council "An Affordable Defense of Asia" (2020) | https://www.atlanticcouncil.org/in-depth-research-reports/report/an-affordable-defense-of-asia/ | 6305659e | First island chain leverage, geographic + technological advantage, affordable deterrence architecture |
| T1-09 | NDU JFQ-103 "The Tactical Defense Becomes Dominant Again" (PDF, 2021) | https://ndupress.ndu.edu/Portals/68/Documents/jfq/jfq-103/jfq-103_10-17_Hammes.pdf | 991c92cf | Tactical defense dominance thesis, pervasive surveillance kill zone, 15km → 40km drone kill zone, cross-domain attacks |
| T1-10 | War on the Rocks "Airpower and Interdiction: Overcoming Defender Advantages" (2022) | https://warontherocks.com/2022/09/airpower-and-interdiction-overcoming-defender-advantages/ | a0582048 | Post-Ukraine airpower analysis, defender advantage, interdiction under defense dominance |
| T1-11 | NDU CSR "Rising Dominance of the Tactical Defense" (2024) | https://digitalcommons.ndu.edu/csr-articles/1/ | 7ee74e94 | Extended tactical defense dominance analysis, Ukraine evidence, 2024 update |
| T1-12 | NDU CSR "The Arctic is a Strategic Distraction" (2024) | https://digitalcommons.ndu.edu/csr-articles/25/ | 9e8d4e00 | Indo-Pacific priority over Arctic, resource allocation critique |
| T1-13 | Stimson Center "We Can't Buy Our Way Out: It's Time to Think Differently" (2025) | https://www.stimson.org/2025/we-cant-buy-our-way-out-drones-portable-missiles/ | bad61b53 | Comprehensive platform vulnerability analysis, containerization thesis, mass-producible munitions, DIB capacity gap, F-35 lifecycle cost analysis |

## Tier 2 — Authoritative Secondary

| # | Title | URL | Source ID | Coverage |
|---|-------|-----|-----------|---------|
| T2-01 | Atlantic Council Q&A "Small, smart, many and cheaper: Competitive adaptation in modern warfare" (2024) | https://www.atlanticcouncil.org/content-series/ac-turkey-defense-journal/qa-with-t-x-hammes/ | 30be0416 | Ukrainian drone adaptation, iron triangle critique, DoD Task Force 59, containerized launches from trucks |
| T2-02 | NDU CSR "China's exploitation of overseas ports and bases" (2025) | https://digitalcommons.ndu.edu/csr-articles/17/ | 02fd9a3d | PLA overseas port network, maritime chokepoints, A2/AD node implications |
| T2-03 | NDU CSR "Rising Dominance of the Tactical Defense" (Hellenic HNDC version, 2024) | https://digitalcommons.ndu.edu/csr-articles/1/ | 7ee74e94 | (see T1-11 — same article, different repository entry) |
| T2-04 | NDU Strategic Forum SF-307 "Baltics Left of Bang" — multi-author coalition work (2020) | https://ndupress.ndu.edu/Portals/68/Documents/stratforum/SF-307.pdf | 7ffb85d4 | (see T1-07 — co-authored) |

## Failed ingests

- PRISM Vol.4 No.2 "Offshore Control" (PDF, 2013) — https://ndupress.ndu.edu/Portals/68/Documents/prism/prism_4-2/prism_47-60_hammes.pdf — 404 on NDU server
- WotR "Offshore Control Is the Answer" (2013) — https://warontherocks.com/2013/12/offshore-control-is-the-answer/ — page not found
- USNI Proceedings "Warship Weapons for Merchant Ship Platforms" (Feb 2025) — paywall/processing failure

## Refresh Strategy

**Primary new content to watch:**
- New NDU Strategic Forum or JFQ articles by Hammes
- New Atlantic Council / Stimson Center publications
- War on the Rocks articles (Hammes publishes regularly)
- Congressional testimony on defense acquisition / drones
- New book (if announced — next after Sling and the Stone)

**Refresh trigger:** New NDU/Stimson/AtCo report, new WotR article, or Congressional testimony on defense acquisition reform.

**Split trigger:** If source count exceeds 45 → consider topical split:
- `primary-strategy` — Offshore Control, 4GW doctrine (2005-2020 era)
- `primary-technology` — Small-many-smart, containerization, tactical defense dominance (2014-2025 era)
