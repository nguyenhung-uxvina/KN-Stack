# Source Tier System — Research Pipeline v3.0

## Tier Classification

| Tier | Loại | Ví dụ | Trust Level |
|------|------|-------|-------------|
| **S** | Standards/Primary | MIL-STD, IEEE, STANAG, TCVN, patents, peer-reviewed papers, theses | Citable facts |
| **A** | Authority/OEM | TI/AD app notes, OEM whitepapers, datasheets, DTIC, NATO STO reports, manufacturer guides | High confidence |
| **B** | Professional | Engineering blogs, conference talks, curated YouTube (credentials + >50K views) | Good reference |
| **C** | Community | General YouTube, forums, Reddit, blog posts, tutorials without credentials | Cross-check only |

## Tier Detection Heuristics

```
URL contains ieee.org, doi.org, mil-std, stanag, .gov/publications,
  arxiv.org, tcvn.gov.vn, patents, patents.google.com,
  worldwide.espacenet.com, lens.org → S

URL contains ti.com, analog.com, dtic.mil, nato.int,
  researchgate.net, springer.com, sciencedirect.com,
  mdpi.com, mouser.com/applications, digikey.com/articles → A

YouTube channel: verified + >100K subs + author has
  engineering/academic credentials in description → B

Everything else → C
```

## Authority Domain Queries by Topic

**ELECTRONICS:**
```
"<topic> site:ti.com OR site:analog.com"
"<topic> site:mouser.com OR site:digikey.com"
```

**DEFENSE/TRAINING:**
```
"<topic> site:dtic.mil"
"<topic> site:nato.int OR site:sto.nato.int"
```

**ENGINEERING:**
```
"<topic> site:researchgate.net OR site:mdpi.com"
"<topic> site:sciencedirect.com OR site:springer.com"
```

**VIETNAM STANDARDS:**
```
"<topic> site:tcvn.gov.vn OR TCVN"
```

## Patent Search Queries

```
Q1: "<topic> site:patents.google.com"
Q2: "<topic> site:worldwide.espacenet.com"
Q3: "<topic> patent OR utility model site:lens.org"
```

### Patent Metadata Extraction

| Field | Extraction Method |
|-------|-------------------|
| Patent # | URL parse (e.g., `US10234567` from Google Patents URL) |
| Title | HTML title or first heading |
| Assignee | Body text parse — look for "Assignee:", "Applicant:", or meta tag |
| Filing date | Body text parse — "Filed:", "Filing date:" |
| Status | Heuristic: "Active", "Expired", "Application" from page text |

**Fallback:** If WebFetch fails on a patent URL (common for Espacenet — JS-rendered pages), extract from search snippet only. Log as "partial metadata".

**Tier classification:** All patents → **Tier S** (primary source).

## Confidence Scoring

```
★★★ HIGH: Confirmed by ≥1 Tier S/A source
★★  MED:  From Tier B only, no contradiction with S/A
★   LOW:  From Tier C only, OR contradicted by S/A source
```

### Contradiction Handling
- Tier C contradicts S/A → flag as ★ LOW + note conflict
- Tier B contradicts S/A → flag for CEO review
- Tier S contradicts Tier A → flag as research gap, both may be valid

## Exa Result Tiering (v4.1)

When sources come from Exa Channel 0 (see `exa-discovery.md`), assign tier in this order:

1. Exa `category: "research paper"` or `"financial report"` → **S** (primary).
2. Result domain ∈ any Authority Domain list above (ti.com, dtic.mil, ieee.org, …) → **A**.
3. Otherwise → apply the URL heuristic table above (S/A/B/C).

Exa returns a relevance score per result — use it for sort order only, never to override tier. Exa `includeDomains` maps directly onto the "Authority Domain Queries" lists above: pass the same domains to Exa instead of running `site:` WebSearch queries.
