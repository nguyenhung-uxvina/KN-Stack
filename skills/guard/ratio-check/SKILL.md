Weekly analytical:physical ratio check for Workshop X vault. Recommended every Sunday/Monday.

Quantifies whether vault growth serves engineering or drifts toward pure analysis.

Usage: /ratio-check

---

## Process

### Step 1: Scan 7-day activity (dual-source)

Run these commands to get ALL changed files:

```bash
# Committed changes (7-day window)
git log --since="7 days ago" --name-only --diff-filter=ACMR --format="" | sort -u
# Uncommitted changes
git status --porcelain | sed 's/^...//' | sort -u
```

Merge and deduplicate both lists.

### Step 2: Classify files

**Analytical:**
- `5_Galaxy/` notes (except those tagged `#product` or `#pahl`)
- `3_Resources/` framework content, analysis documents
- Any pure-analysis doc outside project folders

**Physical:**
- `1_Projects/*/` test results, prototype docs, BOM, drawings
- `Status.md` updates with physical milestone data
- Galaxy notes tagged `#product` or `#pahl` with design content

**Neutral (exclude):**
- Config files, `_meta/`, `.claude/`, `CLAUDE.md`, `docs/`, `progress.md`

### Step 3: Calculate ratio

- analytical_count / physical_count
- If physical_count = 0 → ratio = ∞ (🔴 alert)

### Step 4: Trend comparison

Read `_meta/system-health.md` for last `/ratio-check` entry (look for "## Ratio Check" sections).
- If previous entry exists → compare ratios: improving (↑) / stable (→) / worsening (↓)
- If no previous entry → "First measurement (no trend data)"

### Step 5: Alert logic

| Condition | Alert |
|-----------|-------|
| Physical = 0 | 🔴 Zero physical activity this week |
| Ratio > 3:1 | ⚠️ Vault growing analytical faster than physical |
| Ratio trending worse vs last week | ⚠️ Trend worsening |
| Ratio ≤ 1:1 | ✅ Healthy balance |

### Step 6: Output and persist

Output format:
```
## Ratio Check — {{today}}
Analytical: [X] files | Physical: [Y] files | Ratio: [X:Y]
Trend vs last week: [↑ improving / → stable / ↓ worsening]
Status: [🔴/⚠️/✅] [verdict]
```

Append this block to `_meta/system-health.md` under a new section.
