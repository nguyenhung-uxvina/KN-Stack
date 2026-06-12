---
name: analyst-trap
description: >-
  Quantitative Analyst Trap detector — scans 7-day vault activity, classifies
  files as analytical vs physical-validation, reads dP/dt from system-health.md,
  checks for upcoming physical gates, and alerts when vault growth is outpacing
  physical engineering (ratio > 3:1 or dP/dt = 0). Run weekly or whenever
  dP/dt = 0 is flagged by sprint or session-exit. Triggers on: "analyst-trap",
  "analyst trap", "dP/dt = 0", "no physical progress", "vault vs lab", "bẫy
  phân tích", "too much analysis", "physical velocity zero".
---

Quantitative Analyst Trap detector for Workshop X vault. Run weekly or when dP/dt = 0 is flagged.

Detects whether vault activity is serving engineering (physical deliverables) or drifting into pure analysis.

Usage: /analyst-trap

---

## Process

### Step 1: Collect 7-day vault activity (dual-source)

Run these commands to get ALL changed files (committed + uncommitted):

```bash
# Committed changes (7-day window)
git log --since="7 days ago" --name-only --diff-filter=ACMR --format="" | sort -u
# Uncommitted changes (staged + unstaged + untracked)
git status --porcelain | sed 's/^...//' | sort -u
```

Merge both lists (deduplicated). Then classify each file:

**Analytical files:**
- `5_Galaxy/` notes with `#sys`, `#meta`, or `#three-laws` tags
- `3_Resources/` framework or analysis content
- Any document that is purely analytical (no test data, no physical measurements)

**Physical validation files:**
- `1_Projects/` files containing test results, measurements, prototype data
- `Status.md` updates with physical milestone data
- BOM updates, manufacturing drawings, CAD-related files
- Galaxy notes tagged `#product` or `#pahl` with physical design content

**Neutral (exclude from ratio):**
- `CLAUDE.md`, `_meta/`, `.claude/`, `docs/`, config files, `progress.md`

### Step 2: Read dP/dt

Read `_meta/system-health.md`. Look for the current month's section.
- Extract dP/dt value (prototype iterations this month)
- If no entry for current month → flag as "dP/dt UNKNOWN"

### Step 3: Scan physical gates

Read each `1_Projects/*/Status.md`. Extract "next gate" or "next physical gate" date.
- Count projects with gate date within 30 days from today

### Step 4: Apply alert logic

| Condition | Alert |
|-----------|-------|
| Analytical > Physical × 3 | ⚠️ ANALYST TRAP ACTIVE |
| dP/dt = 0 this month | 🔴 ZERO PHYSICAL VELOCITY |
| Zero projects with gate < 30 days | 🔴 NO UPCOMING GATES |
| All conditions OK | ✅ Vault serving engineering |

### Step 5: Generate report

Output format:

```
## Analyst Trap Check — {{today}}

📊 7-day activity: [X] analytical files | [Y] physical validation files
📈 dP/dt tháng [M]/[YYYY]: [N] iterations
🚪 Projects with gate < 30 days: [list or "none"]

Status: [🔴/⚠️/✅] [verdict]

💡 Recommendation: [specific action to restore balance]
```

### Step 6: Persist

Append the report to `_meta/system-health.md` under a new dated section.
