Drive a weekly design sprint for a specific project — the operational heartbeat between CEO Dashboard reviews.

Usage: /sprint [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - Which active project? List projects from `1_Projects/*/Status.md`

2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md` — tier, phase, blockers, deadlines, dP/dt
   - `1_Projects/{{project}}/_Project_Brief.md` — requirements, scope
   - Phase folder contents (e.g., `Phase3-Embodiment/*.md`) — deliverables status
   - Any ICD tracker if Phase 3+

3. Determine sprint context from Status.md:
   - **Current phase** → drives which deliverables are expected
   - **Physical gate date** → compute days remaining
   - **Blocking constraints** → surface immediately
   - **Key decisions pending** → these ARE the sprint's focus
   - **dP/dt** → physical iteration velocity

4. Generate the Weekly Sprint Driver:

```
# SPRINT DRIVER — {{project}}
**Week of:** {{today}} | **Phase:** {{current_phase}} | **Tier:** {{tier}}

---

## GATE COUNTDOWN
- Physical gate: {{date}} ({{N}} days remaining)
- Phase completion: {{estimate or TBD}}
- ALERT: {{if <7 days, flag RED; if <14 days, flag YELLOW}}

---

## THIS WEEK'S FOCUS (max 3 items)

### 1. {{highest priority item from blocking constraints or pending decisions}}
- **Type:** C (Core — CEO decides) / O (Offload — AI executes)
- **What's needed to resolve:** {{specific information, data, test, analysis}}
- **Deliverable by Friday:** {{concrete output}}
- **Blocked by:** {{dependency or "None"}}

### 2. {{second priority}}
- **Type:** C / O
- **What's needed:** {{...}}
- **Deliverable by Friday:** {{...}}

### 3. {{third priority}}
- **Type:** C / O
- **What's needed:** {{...}}
- **Deliverable by Friday:** {{...}}

---

## DECISIONS NEEDED THIS WEEK

| # | Decision | Info Available | Info Missing | Owner | Deadline | Impact |
|---|----------|---------------|-------------|-------|----------|--------|
| D1 | {{from Key Decisions Pending}} | {{what we know}} | {{what we need}} | CEO / AI | {{date}} | {{what's blocked until decided}} |

---

## HUMAN-AI HANDOFF PLAN

| Task | Mode | AI Does | CEO Does | Due |
|------|------|---------|----------|-----|
| {{task}} | C/O/CO/OC | {{AI action or "—"}} | {{CEO action or "—"}} | {{day}} |

Modes: C = Core (CEO only), O = Offload (AI only), CO = CEO then AI, OC = AI then CEO validates

---

## PHASE DELIVERABLES TRACKER

| # | Deliverable | Status | Notes |
|---|------------|--------|-------|
{{list all expected deliverables for current phase, mark done/in-progress/not-started}}

---

## INTEGRATION & DEBT CHECK
- Open TBDs in ICD: {{count or "N/A if Phase 1-2"}}
- Interface changes this week: {{list or "none"}}
- Cross-project impact: {{if interface change affects other projects, flag here}}

---

## dP/dt PULSE
- Physical iterations this month: {{count}}
- Physical work this week: {{planned activity or "NONE — flag if 3+ weeks without"}}
- Next hands-on milestone: {{what and when}}

{{if dP/dt = 0 for current month AND >14 days into month:}}
> ANALYST TRAP WARNING: No physical iteration this month. Vault is exceeding the lab.
> Recommended: Schedule physical work within 7 days or reassess project tier.

---

## LAST WEEK REVIEW (skip on first sprint)
- Decisions made: {{count}} / {{count planned}}
- Items completed: {{list}}
- Carried over: {{items not completed — why?}}
- Velocity trend: {{improving / stable / declining}}
```

5. After presenting the sprint:
   - Ask CEO: "Does this sprint focus look right? Any items to swap or reprioritize?"
   - If CEO approves, offer to update Status.md with sprint plan
   - If CEO adjusts, regenerate the affected sections

6. Sprint close (when called with "close" or "review"):
   - Read previous sprint output (from Status.md or conversation)
   - Score: decisions made vs planned, items completed vs planned
   - Update dP/dt in Status.md
   - Carry over incomplete items to next sprint
   - Flag any recurring blockers (same blocker 2+ weeks = systemic issue)

RULES:
- MAX 3 focus items per week — CEO is solo engineer with 25h/week across 3-4 projects
- Every focus item must have a concrete Friday deliverable — no vague "continue working on X"
- Decisions are the primary output — the sprint succeeds when decisions are MADE, not when docs are written
- Always classify tasks as C/O/CO/OC — this enforces the COD system
- Physical work trumps document work — if dP/dt = 0, prioritize hands-on tasks
- Never auto-update Status.md — always propose changes and wait for CEO approval
- Link to Galaxy notes when relevant (Physical-World Interface, Analyst Trap, Musk Sequence)
- If project has no physical gate date set, flag it — Tier 1/2 projects MUST have physical gates
- Sprint driver is Offload (O) — AI generates, CEO validates and adjusts priorities
- Keep output to ONE SCREEN — CEO has 10 minutes for sprint planning, not 30
