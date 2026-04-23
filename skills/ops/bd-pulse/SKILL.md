Log defense BD touchpoints. Track relationship health. CRM tối giản cho solo CEO.

Usage: /bd-pulse

---

## Process

### Step 1: Read contact log

Read `2_Areas/BRIDGE — Operations/Defense-Ecosystem-Vietnam/contact-log.md`.

If not exists, create with template (Step 2).

If exists, show dashboard:

```
## BD Pulse — [today]

### Relationship Health
| Contact | Organization | Last Touch | Days Ago | Status |
|---------|-------------|-----------|:--------:|--------|
| [name] | [org] | [date] | [N] | 🟢/🟡/🔴 |

🟢 = < 14 days | 🟡 = 14-30 days | 🔴 = > 30 days (going cold)
```

### Step 2: First run — seed contacts

If file doesn't exist, ask CEO:

1. **"Ai là 3-5 contacts quan trọng nhất trong defense ecosystem?"**
   - Name, organization, role, relationship strength (1-5)

2. **"Lần cuối liên hệ mỗi người là khi nào?"**
   - Date + topic

3. **"Exhibition nào sắp tới?"**
   - VIETSHIP, Vietnam Defence Expo, other

Create `2_Areas/BRIDGE — Operations/Defense-Ecosystem-Vietnam/contact-log.md`:

```markdown
# Defense BD Contact Log — Workshop X

> CRM tối giản. Log mỗi touchpoint. Review weekly via /bd-pulse.

---

## Contacts

### [Name 1]
- **Organization:** [org]
- **Role:** [role]
- **Relationship strength:** [1-5]
- **Notes:** [context]

#### Touchpoints
| Date | Type | Topic | Next Action | Follow-up |
|------|------|-------|-------------|-----------|
| [date] | [call/meeting/email/exhibition] | [topic] | [action] | [date] |

---

### [Name 2]
...

---

## Exhibitions & Events

| Event | Date | Status | Notes |
|-------|------|--------|-------|
| [name] | [date] | [planned/registered/attended] | [notes] |

---

## Pipeline (Deals/Opportunities)

| Opportunity | Contact | Stage | Value | Next Step |
|-------------|---------|-------|-------|-----------|
```

### Step 3: Log new touchpoint

Ask: **"Hôm nay có liên hệ ai không?"**

If yes:
- Who? (match to existing contact or add new)
- Type? (call / meeting / email / exhibition / site visit)
- Topic?
- Next action?
- Follow-up date?

Append to that contact's touchpoint table.

If no: skip to Step 4.

### Step 4: Follow-up check

Scan all contacts for:
- Follow-ups due today or overdue → "📞 Follow-up due: [name] — [topic]"
- Contacts going cold (>30 days) → "🔴 [name] going cold. Last contact: [date]"
- No touchpoints this week → "⚠️ Zero BD activity this week"

### Step 5: Ế score update

Calculate Ế score from activity:
- 0 contacts logged → Ế = 0/5
- Contacts exist but all cold (>30d) → Ế = 1/5
- ≥1 active contact (<14d) → Ế = 2/5
- ≥3 active contacts + follow-up system → Ế = 3/5
- Exhibition attended + reference visits conducted → Ế = 4/5
- Systematic pipeline with tracked win rate → Ế = 5/5

### Step 6: Weekly summary

If today is Monday or Friday:

```
## BD Weekly Summary — Week of [date]

### Activity
- Touchpoints this week: [N]
- New contacts added: [N]
- Follow-ups completed: [N/total due]

### Health
- 🟢 Active (<14d): [N] contacts
- 🟡 Warm (14-30d): [N] contacts
- 🔴 Cold (>30d): [N] contacts

### Ế Score: [X/5]

### Priority Actions
1. [most urgent follow-up]
2. [coldest important contact]
3. [next exhibition or event]
```

### Step 7: Output

```
## BD Pulse — [today]

### Dashboard
[relationship health table]

### Today's Touchpoint
[logged or "None — consider a 5-min check-in call"]

### Follow-ups Due
[list with dates]

### Ế Score: [X/5]

### Next Exhibition: [name] — [date] — [status]
```
