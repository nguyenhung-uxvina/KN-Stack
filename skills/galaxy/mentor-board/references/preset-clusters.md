# Preset Clusters — Pre-defined Mentor Groupings

For multi-mentor modes (PANEL/DEBATE/DECIDE), CEO can use preset name instead of explicit comma-separated list.

## Available Presets

| Preset | Mentors | Best for | Rationale |
|---|---|---|---|
| `capital` | Munger + Marks + Dalio | Capital allocation, valuation, position sizing, bubble detection | 3 framework-distinct capital thinkers: Munger (lattice + concentration), Marks (cycles + margin), Dalio (machine + balance) |
| `scaling` | Musk + Huang + Grove | Operational scaling, vertical integration, manufacturing leverage | 3 scale operators across hardware (Musk), platforms (Huang), management process (Grove) |
| `ai-strategy` | Huang + Musk + Naval + Dario | AI/compute strategy, chip positioning, model strategy, safety | Huang (compute infrastructure), Musk (AI safety + applied), Naval (philosophical implications + leverage), Dario (RSP/safety framework + Constitutional AI) |
| `manufacturing` | Musk + Grove + Ford | Production engineering, assembly line, factory design, cost reduction | Musk (1st-principles factory), Grove (OKR + manufacturing-as-process), Ford (mass production + price-led costing) |
| `founder-wisdom` | Naval + Grove + Munger + Jobs | Specific knowledge, judgment, mental models, life decisions | Naval (specific knowledge + leverage), Grove (paranoid survival), Munger (multidisciplinary wisdom), Jobs (product vision + focus) |
| `product-vision` | Jobs + Musk + Huang | Product design, customer experience, category creation, hardware excellence | Jobs (customer-backwards + design), Musk (first-principles hardware), Huang (platform + ecosystem) |
| `people` | Grove + Dalio + Munger | Hiring, culture, principles, performance management | Grove (1:1s, OKRs), Dalio (radical transparency + believability), Munger (incentives + character) |
| `systems` | Brooks + Grove + Dalio | Systems design, complexity, operational rigor | Brooks (complexity + architecture), Grove (process + measurement), Dalio (machine thinking) |
| `value-investing` | Shiller + Marks + Munger + Kiyosaki + Li Ka-shing + Zell | Value investing: valuation discipline, bubble detection, cash flow, cycle | Academic (Shiller) + practitioner (Marks) + framework (Munger) + mindset (Kiyosaki) + Asian EM (Li Ka-shing) + contrarian (Zell) |
| `real-estate` | Li Ka-shing + Zell + Yardney + Linneman + Sternlicht + Horn | Core real estate: strategy, underwriting, emerging markets, development | Asian EM (Li Ka-shing) + contrarian (Zell) + growth (Yardney) + academic (Linneman) + hospitality/luxury (Sternlicht) + EM dev (Horn) |
| `real-estate-vn` | Li Ka-shing + Shiller + Linneman + Horn + Terwilliger + Zell | Vietnam real estate decisions: EM context, bubble detection, underwriting | Emerging market lens (Li Ka-shing + Horn + Terwilliger) + bubble (Shiller) + underwriting discipline (Linneman) + contrarian timing (Zell) |
| `re-development` | Ross + Sternlicht + Roth + Sitt + Terwilliger + Horn | Large-scale RE development decisions | Mixed-use (Ross) + hospitality/brand (Sternlicht) + urban repositioning (Roth) + retail/street (Sitt) + affordable (Terwilliger) + EM (Horn) |
| `wx-management` | Ngô Minh Tuấn + Phan Văn Trường + Alan Phan + Giản Tư Trung + Ben Horowitz + David Marquet | Workshop X team management: cơ chế khoán, đàm phán quốc phòng, leadership culture | VN tư duy (Ngô/Phan/Alan/Giản) + global startup hard things (Horowitz) + military-tech leadership (Marquet) |
| `vn-leadership` | Ngô Minh Tuấn + Giản Tư Trung + Alan Phan | Vietnamese management culture, team incentives, contrarian strategy | 3 tư duy lãnh đạo Việt Nam: khoán (Ngô) + nhân cách (Giản) + ngược (Alan) |
| `defense-startup` | Ben Horowitz + David Marquet + Palmer Luckey + Chris Brose | Building and leading a defense technology startup | Wartime CEO (Horowitz) + Intent-Based Leadership (Marquet) + hardware defense (Luckey) + acquisition reform (Brose) |
| `b2g-procurement` | Phan Văn Trường + Chris Brose + Palmer Luckey + Robert Work | Vietnam B2G + US defense procurement + reform strategy | VN negotiation (Phan) + acquisition reform (Brose + Work) + defense hardware founder (Luckey) |
| `al-build` | al-build-council | Aluminum fabrication for underwater weapons: Ø400mm hull, t=3mm, 19 rings, 50m depth, TIG welding, Sequence B | Single specialist council — AWS D1.2 + Alcoa Marine + NSWC Carderock + Windenburg-Trilling buckling |
| `nswc-hull` | nswc-hull-council | External pressure structural certification: ring-stiffened cylinder design, ovalization knockdown, hydrostatic test protocols, MIL-SPEC depth rating | Single specialist council — DTMB + NAVSEA Submarine Structural Integrity + NASA SP-8007 + ABS Underwater Vehicles |
| `hull-cert` | al-build-council + nswc-hull-council | Complete hull certification path: fabrication (al-build) + structural certification (nswc-hull) for TN-03-02-000 Ø400mm torpedo hull | 2-council focused pair — fabrication HOW (al-build) + structural WHY + test protocol (nswc-hull) |
| `torpedo-fabrication` | al-build-council + nswc-hull-council + naval-architect-council + hyman-rickover + military-combat-engineer-council | Full combat torpedo hull fabrication: structural + process + quality + dynamic loads | Materials/process (al-build) + external pressure theory (nswc-hull) + general structural standards (naval-arch) + quality accountability (Rickover) + dynamic shock (combat-eng) |
| `all` | All 51 mentors | Maximum diversity (long output, ~51× cost) | When complete coverage matters more than focus |

## Preset Selection Logic in INTAKE

When INTAKE proposes mode + mentors:

```
domain (from CEO answer Q6) → preset mapping

capital                    → preset 'capital'
scaling                    → preset 'scaling'
manufacturing              → preset 'manufacturing'
product-design             → preset 'product-vision'
ai-strategy                → preset 'ai-strategy'
people                     → preset 'people'
founder-wisdom             → preset 'founder-wisdom'
systems / complexity       → preset 'systems'
real-estate (general)      → preset 'real-estate'
real-estate (VN/EM focus)  → preset 'real-estate-vn'
real-estate (development)  → preset 're-development'
value-investing            → preset 'value-investing'
team management (VN)       → preset 'vn-leadership'
workshop-x management      → preset 'wx-management'
defense startup ops        → preset 'defense-startup'
defense procurement B2G    → preset 'b2g-procurement'
other (or 2+ domains)      → CEO selects explicit list OR preset 'all'
```

## Override Mechanics

CEO can ALWAYS override preset with explicit list:

```bash
# Use preset
/mentor-board --debate capital "VC funding decision"

# Override: same mode, different mentors
/mentor-board --debate musk,marks,naval "VC funding decision"
  → custom 3-mentor combo, regardless of preset name

# Hybrid: preset + addition
/mentor-board --debate capital+naval "VC funding decision"
  → Munger + Marks + Dalio + Naval (preset + 1 extra)

# Preset exclusion
/mentor-board --debate capital-dalio "VC funding decision"
  → Munger + Marks (preset minus 1)
```

## Adding New Presets

When CEO builds frequent custom combinations, document as new preset:

1. Add row to table above
2. CEO can then use `--panel <new-preset>` etc.

Common candidates if board grows:
- `risk` — Marks + Taleb (if added) + Dalio
- `compounding` — Buffett (if added) + Munger + Naval
- `competition` — Thiel (if added) + Bezos (if added) + Musk
- `vietnam-defense` — Phan Văn Trường + Ngô Minh Tuấn + Alan Phan (added 2026-06-06 — see `wx-management` preset)

## Preset Cost Estimate

| Preset | Mentor count | Approximate query count for: |
|--------|:------------:|------------------------------|
| | | PANEL | DEBATE (3 rounds) | DECIDE (3 options) |
| `capital` | 3 | 3 | 9 | 9 |
| `scaling` | 3 | 3 | 9 | 9 |
| `ai-strategy` | 3 | 3 | 9 | 9 |
| `manufacturing` | 2 | 2 | 6 | 6 |
| `founder-wisdom` | 3 | 3 | 9 | 9 |
| `people` | 3 | 3 | 9 | 9 |
| `systems` | 3 | 3 | 9 | 9 |
| `product-vision` | 3 | 3 | 9 | 9 |
| `value-investing` | 6 | 6 | 18 | 18 |
| `real-estate` | 6 | 6 | 18 | 18 |
| `real-estate-vn` | 6 | 6 | 18 | 18 |
| `re-development` | 6 | 6 | 18 | 18 |
| `wx-management` | 6 | 6 | 18 | 18 |
| `vn-leadership` | 3 | 3 | 9 | 9 |
| `defense-startup` | 4 | 4 | 12 | 12 |
| `b2g-procurement` | 4 | 4 | 12 | 12 |
| `nswc-hull` | 1 | 1 | 3 | 3 |
| `hull-cert` | 2 | 2 | 6 | 6 |
| `all` | 51 | 51 | 153 | 153 (per 3-option) |

NLM rate-limit consideration: `--debate all` = 153 parallel queries — DO NOT USE. Use targeted presets instead. Mentor-board should chunk if N > 10.
