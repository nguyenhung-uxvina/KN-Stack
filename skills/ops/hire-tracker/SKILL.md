Track hiring pipeline from "cần gì" → "đăng tuyển" → "phỏng vấn" → "onboard". Breaks I₂ = 0 bottleneck.

Usage: /hire-tracker

---

## Process

### Step 1: Read pipeline

Read `_meta/hiring-pipeline.md`. If not exists, go to Step 2 (first run).

If exists, show current state:

```
## Hiring Pipeline — [date]

| Role | Stage | Since | Next Action | Deadline |
|------|-------|-------|-------------|----------|
| [role] | [stage] | [date] | [action] | [date] |
```

Stages: DEFINE → POST → SCREEN → INTERVIEW → OFFER → ONBOARD → ACTIVE

For each role, ask: "Có update gì cho [role]?"
- If stage changed → update
- If no change > 14 days → flag: "⚠️ [role] stuck at [stage] for [N] days"

### Step 2: First run — define first hire

If `_meta/hiring-pipeline.md` doesn't exist, guide CEO through 5 questions:

1. **"Nếu có 1 người thêm, người đó làm gì?"**
   - Suggest based on vault: product line owner? production assistant? BD support?
   - CEO answers freely

2. **"Full-time hay part-time?"**
   - Part-time/contract = lower risk, faster to start
   - Full-time = higher commitment, higher impact

3. **"Mức lương/chi phí dự kiến?"**
   - Don't judge — just record

4. **"Đăng ở đâu?"**
   - Vietnam options: TopCV, VietnamWorks, LinkedIn, university network, word of mouth
   - Defense sector: military academy alumni network, SOE contacts

5. **"Khi nào bắt đầu tuyển?"**
   - If "chưa biết" → set reminder for 2 weeks: "Review hiring decision"
   - If date given → log as POST deadline

Create `_meta/hiring-pipeline.md`:

```markdown
# Hiring Pipeline — Workshop X

> Track from DEFINE → POST → SCREEN → INTERVIEW → OFFER → ONBOARD → ACTIVE
> Updated by /hire-tracker

---

## Roles

### [Role Name]
- **Stage:** DEFINE
- **Type:** [full-time/part-time/contract]
- **Budget:** [amount]
- **Channel:** [where to post]
- **Defined:** [today's date]
- **Target start:** [date or TBD]
- **Next action:** [specific action]
- **Next deadline:** [date]

---

## History
- [today] Created pipeline. First role: [role name].
```

### Step 3: Add new role (if requested)

If CEO says "thêm role mới" → run through the 5 questions again, append to pipeline.

### Step 4: Nudge check

Calculate days since last stage change for each role.

- < 7 days: normal
- 7-14 days: "💡 [role] — consider moving to next stage"
- > 14 days: "⚠️ [role] stuck at [stage] for [N] days. Blocker?"
- > 30 days: "🔴 [role] stalled. Decide: advance, pivot, or drop?"

### Step 5: I₂ score update

Count active roles in pipeline:
- 0 roles defined → I₂ = 0/5
- 1+ roles defined → I₂ = 1/5
- 1+ roles posted → I₂ = 2/5
- 1+ candidates screening → I₂ = 2.5/5
- 1+ interviews conducted → I₂ = 3/5
- 1+ offers made → I₂ = 3.5/5
- 1+ people onboarded → I₂ = 4/5
- Team delivering independently → I₂ = 5/5

### Step 6: Output

```
## Hire Tracker — [today]

### Pipeline
| Role | Stage | Days in Stage | Next Action |
|------|-------|:------------:|-------------|
| [role] | [stage] | [N] | [action by date] |

### I₂ Score: [X/5] ([reason])

### Alerts
[nudges from Step 4]

### Quick Stats
- Roles defined: [N]
- Roles posted: [N]
- Active candidates: [N]
- Days since pipeline created: [N]
```
