Weekly accountability: 3 commitments Monday, 3 scores Friday. Cross-layer P-CHIẾN LƯỢC enforcement.

Usage: /weekly-3 [monday|friday]
- monday: commit 3 deliverables for the week
- friday: score completion and reflect
- no argument: auto-detect day of week

---

## Process

### Detect mode

If no argument given:
- Monday-Wednesday → Monday mode
- Thursday-Sunday → Friday mode

If argument given: use that mode.

---

## Monday Mode: Commit

### Step 1: Review last week

Read `_meta/weekly-3.md`. Find the most recent Monday entry.

If exists, show last week's commitments and ask CEO to score each:
- ✅ DONE
- ⚠️ PARTIAL (explain)
- ❌ MISSED (explain)

Calculate score: X/3. Track streak in file.

### Step 2: New commitments

Ask CEO for 3 deliverables this week. Enforce rules:

**Rule 1:** ≥1 MUST be physical (P layer)
- Valid: order material, conduct test, send document to partner, visit workshop
- Invalid: write analysis, create framework, build skill, update vault

**Rule 2:** ≥1 MUST be external (Ế or I₂ layer)
- Valid: call Viettel, meet customer, post job listing, interview candidate, send proposal
- Invalid: internal vault work, Galaxy notes, design documents

**Rule 3:** 1 free choice (any CHIẾN LƯỢC layer)

If CEO's commitments don't meet rules → push back: "Cần ít nhất 1 physical và 1 external. Thử lại."

### Step 3: Log

Append to `_meta/weekly-3.md`:

```
## Week of [Monday date]

### Commitments
1. [P] [physical action] — deadline: [date]
2. [Ế/I₂] [external action] — deadline: [date]
3. [layer] [free choice] — deadline: [date]

### Score (filled Friday)
- [ ] 1:
- [ ] 2:
- [ ] 3:
Total: /3
```

If file doesn't exist, create with header:
```
# Weekly 3 — Accountability Log
> 3 commitments every Monday. Score every Friday.
> Rule: ≥1 physical, ≥1 external, 1 free.
> Target: 3/3 every week. Streak tracked.
```

### Step 4: Output

```
## Weekly 3 — [Monday date]

### Last Week Score
[X/3] | Streak: [consecutive 3/3 weeks]
[details per item]

### This Week Commitments
1. 🔨 [physical] — by [date]
2. 🤝 [external] — by [date]
3. [icon] [free] — by [date]

Next check: Friday [date]
```

---

## Friday Mode: Score

### Step 1: Read this week's commitments

Read `_meta/weekly-3.md`, find current week's entry.

### Step 2: Score each

For each commitment, ask CEO:
- "1. [action] — DONE, PARTIAL, hoặc MISSED?"
- Record answer and brief note

### Step 3: Update log

Update the week's entry with scores:
```
### Score
- [x] 1: ✅ DONE — [note]
- [ ] 2: ❌ MISSED — [reason]
- [x] 3: ⚠️ PARTIAL — [note]
Total: 1.5/3
```

(PARTIAL counts as 0.5)

### Step 4: Streak tracking

If 3/3 → increment streak counter
If <3/3 → reset streak to 0

### Step 5: Pattern detection

After 3+ weeks of data, analyze:
- Which layer commitments get MISSED most? → that's the avoidance pattern
- Which get DONE most? → that's the comfort zone (possibly Analyst Trap)
- If physical always MISSED → "🔴 Physical avoidance pattern detected. B1b active."
- If external always MISSED → "🔴 Relationship avoidance. Ế layer decaying."

### Step 6: Output

```
## Weekly 3 — Friday [date]

### This Week Score: [X/3]

1. [status icon] [action] — [note]
2. [status icon] [action] — [note]
3. [status icon] [action] — [note]

### Streak: [N] consecutive 3/3 weeks
### Pattern: [insight if 3+ weeks data]

### CHIẾN LƯỢC Layer Health (from weekly-3 data)
P: [% physical commitments completed]
Ế: [% external commitments completed]
Other: [% free commitments completed]
```
