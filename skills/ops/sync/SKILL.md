Run a monthly cross-domain synchronization review across BRIDGE, FORGE, and HELIX.

Usage: /sync OR /sync [focus_area]

1. Read current state:
   - All `1_Projects/*/Status.md`
   - `2_Areas/*/_Area_Dashboard.md` (if they exist)
   - Galaxy note count and recent additions
   - Recent /reflect outputs (if available)

2. Generate the sync review:

```
# MONTHLY SYNC REVIEW — {{month}} {{year}}
**Date:** {{today}}

---

## CROSS-DOMAIN ALIGNMENT CHECK

### BRIDGE → FORGE (Operations feeding Strategy)
- [ ] Customer signals captured this month? {{Y/N — list}}
- [ ] Market intelligence updated? {{Y/N}}
- [ ] Competitor moves detected? {{Y/N}}
- **Gap:** {{what BRIDGE should feed FORGE but isn't}}

### FORGE → HELIX (Strategy guiding Execution)
- [ ] Portfolio priorities clear? {{Y/N}}
- [ ] ACH decisions made for active products? {{Y/N}}
- [ ] Cost targets set and tracked? {{Y/N}}
- **Gap:** {{what FORGE should feed HELIX but isn't}}

### HELIX → BRIDGE (Execution informing Operations)
- [ ] Design reviews conducted? {{Y/N — count}}
- [ ] Physical prototypes built/tested? {{Y/N — dP/dt}}
- [ ] Lessons learned captured? {{Y/N — /reflect count}}
- **Gap:** {{what HELIX should feed BRIDGE but isn't}}

---

## COMPOUND LAW SCORE

| Domain | Last Month | This Month | Delta | Bottleneck |
|--------|-----------|------------|-------|-----------|
| BRIDGE | % | % | | |
| FORGE | % | % | | |
| HELIX | % | % | | |
| **Compound** | % | % | | |

---

## dP/dt PORTFOLIO REVIEW
| Project | Physical iterations this month | Target | Status |
|---------|------------------------------|--------|--------|
| | | >0 | PASS/FAIL |

---

## GALAXY HEALTH
- Notes added this month: {{count}} (target: 12-20/month)
- Link density average: {{avg}} (target: >=3)
- Physical:Framework ratio: {{%}} (target: >20%)
- Stale notes (>3 months no update): {{count}}

---

## TOP 3 CROSS-DOMAIN ACTIONS
1. {{highest-impact action that connects two domains}}
2. {{second}}
3. {{third}}
```

3. Present to user. Do NOT save unless asked.

RULES:
- Monthly cadence — not more frequent (overhead), not less (drift)
- Focus on CONNECTIONS between domains, not within-domain details (/dash handles that)
- dP/dt = 0 for >1 month across all projects = CRITICAL flag
- COD: Offload (AI compiles, CEO validates alignment)
- This feeds /dash with updated Compound Law scores
