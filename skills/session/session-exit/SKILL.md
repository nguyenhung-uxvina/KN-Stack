Session exit protocol for Workshop X. Run at the end of every session to enforce compound learning.

Asks reflective questions, logs learnings, updates progress.md, and tracks physical progress streaks.

Usage: /session-exit

---

## Process

### Step 1: Ask 3 reflective questions

Present these questions to the CEO one at a time. Wait for answers.

1. **"Hôm nay có gì di chuyển product tới physical milestone?"**
   → Record the answer. "Không" is a valid answer.

2. **"Learning nào đã được log?"**
   → Check `_meta/learnings.md` for entries with today's date.
   → If entries exist, show them: "Already logged: [list]"
   → If none, prompt: "Dictate ≥ 1 insight. Format: [topic] — [insight] → [action]"

3. **"CLAUDE.md cần update gì?"**
   → Scan CLAUDE.md for potential drift:
     - Galaxy count still accurate?
     - Project list still current?
     - Any new conventions learned this session?
   → If drift detected → suggest specific edits
   → If no drift → "No drift detected"

### Step 2: Log learnings

If no learnings were logged today:
- Take the CEO's dictated insight from question 2
- Append to `_meta/learnings.md` in format: `[YYYY-MM-DD] [topic] — [insight] → [action taken]`

### Step 3: Update progress.md

Read current `progress.md`. Update:
- **Completed:** Add today's work
- **Current State:** Update project statuses
- **Next Steps:** Update based on what remains
- **updated:** field in frontmatter → today's date

### Step 4: Consecutive-zero tracking

Read `_meta/session-counters.json`.

**If question 1 answer = "không" or indicates no physical progress:**
- Increment `consecutive_zero_physical`
- Update `last_session_date` to today
- If counter ≥ 3 → output:
  ```
  🔴 FULL ANALYST TRAP ALERT — 3+ consecutive sessions with zero physical progress!
  Run /analyst-trap for full diagnostic.
  Recommended: Schedule a physical test or prototype activity this week.
  ```

**If question 1 indicates physical progress:**
- Reset `consecutive_zero_physical` to 0
- Update `last_physical_progress` to today
- Update `last_session_date` to today

Write updated JSON back to `_meta/session-counters.json`.

### Step 5: Output session wrap-up

```
## Session Exit — {{today}}

### Physical Progress Today
[CEO's answer or "None — counter: N/3 before alert"]

### Learnings Logged
- [list of today's entries from _meta/learnings.md, or "⚠️ None — logging now..."]

### CLAUDE.md Drift
[Suggested updates or "No drift detected"]

### Progress File
✅ progress.md updated for /catchup
```
