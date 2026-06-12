---
name: physical-sprint
description: >-
  Force 1 physical action commitment per session before any analytical work
  begins — reads Tier 1 project open items, presents only physical actions
  (material orders, tests, calls, document submissions), logs the CEO's
  commitment, and tracks previous commitments for DONE/MISSED outcomes. Triggers
  Analyst Trap after 3 consecutive sessions with no physical commitment. Triggers
  on: "physical-sprint", "physical action", "force physical", "hành động thực
  tế", "không có gì physical", "break analyst trap", "commit physical".
---

Force 1 physical action per session. Not analysis — hardware, test, or document sent.

Breaks the Infrastructure Trap (B1b) by requiring a physical commitment before any analytical work.

Usage: /physical-sprint

---

## Process

### Step 1: Read Tier 1 project status

Read Status.md for all Tier 1 projects in 1_Projects/. Extract ONLY:
- Open physical items (OI items, tests, material orders, documents to send)
- Next physical gate date
- dP/dt this month

### Step 2: List available physical actions

Present a numbered list of ONLY physical actions. Exclude:
- Analysis, frameworks, design documents
- Galaxy notes, skills, infrastructure
- Anything that lives purely in the vault

Examples of valid physical actions:
- Order material (HDPE sheets, aluminum, fasteners)
- Schedule/conduct weld test, fit check, or prototype assembly
- Send ICD/document to partner or customer
- Make phone call to supplier or partner
- Visit workshop/lab for measurement or inspection
- Submit procurement paperwork

### Step 3: CEO commits

Ask: **"Chọn 1 action và commit thời gian cụ thể."**

Format: "[Action] — trước [ngày/giờ cụ thể]"

### Step 4: Log commitment

Append to `_meta/physical-sprint-log.md`:

```
## [today's date]
- **Committed:** [action] — deadline: [date/time]
- **Project:** [project name]
- **Status:** PENDING
```

If the file doesn't exist, create it with header:
```
# Physical Sprint Log
> 1 physical action per session. Track commitments and completion.
```

### Step 5: Check previous commitments

Read `_meta/physical-sprint-log.md` for any PENDING items.

For each PENDING item:
- Ask CEO: "Đã hoàn thành [action] chưa?"
- If yes → update status to DONE, record completion date
- If no → update status to MISSED, ask why, carry forward or drop

### Step 6: Output

```
## Physical Sprint — [today]

### Previous Commitments
[list with DONE/MISSED status]

### Available Physical Actions
1. [action] — [project] — deadline [gate date]
2. [action] — [project] — deadline [gate date]
...

### Today's Commitment
✅ [CEO's chosen action] — deadline: [date/time]

### dP/dt Status
[current month iterations] | Streak: [consecutive sessions with physical action]
```

### Rules
- If CEO says "không có gì physical" → output: "🔴 Analyst Trap active. Có chắc không có 1 email, 1 phone call, 1 material order?"
- If 3+ consecutive sessions with no physical commitment → trigger full /analyst-trap
- NEVER suggest analytical work as a substitute for physical action
