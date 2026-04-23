---
name: helix-sync-protocol
description: Cross-domain sync protocol for Workshop X concurrent engineering. Two modes — monthly full sync (CEO-led 40min meeting) and weekly micro-sync (AI-driven 10min health pulse). Triggers on "sync", "monthly review", "domain sync", "helix sync", "micro-sync", "weekly check", "domain check", "quick domain check". Consumes domain-debate JSON side-cars from pipeline work.
---

# Helix Sync Protocol — Cross-Domain Monthly Integration Review

Run the 3-part monthly sync that keeps concurrent engineering domains aligned. BEFORE (AI prepares) + DURING (Human leads 40 min) + AFTER (AI documents). Without this, integration debt compounds silently.

## Modes

| Mode | Trigger | Duration | Who Leads | Frequency |
|------|---------|----------|-----------|-----------|
| `--monthly` (default) | "sync", "monthly review" | 40 min meeting + AI prep/doc | CEO | Monthly |
| `--weekly` | "micro-sync", "weekly check", "domain check" | 10 min AI check, CEO reviews | AI (escalate to CEO) | Weekly mid-sprint |

## When to Use

**Monthly (default):**
- Monthly sync meeting (scheduled or overdue)
- Before a quality gate review (pre-gate alignment)
- When integration debt trend shows 2+ consecutive increases
- When any domain reports >1 month behind schedule
- User asks "are our domains aligned?" or "sync prep"

**Weekly micro-sync (`--weekly`):**
- Mid-sprint alignment check between monthly syncs
- After any domain debate run that week (consumes JSON side-car)
- After a block completion in any HELIX pipeline (BB, BC, BD)
- User asks "quick domain check" or "micro-sync"

---

## Weekly Micro-Sync Protocol (`--weekly`)

> **10-minute AI-driven check.** NOT a meeting — a written health pulse.
> **COD:** Offload (O2). CEO reviews output, acts only if RED flags.
> **Source:** DSM-Based Task Sequencing (Insight #8) — lightweight coupling checks between full syncs prevent integration debt accumulation.

### W1: Automated Scan (AI runs, no CEO input needed)

```
MICRO-SYNC — {{Date}} (Week {{N}} of sprint)
Project(s): {{active Tier 1/2 projects}}

1. DOMAIN DEBATE DIGEST
   Scan for any ```json:domain-debate-sidecar emitted this week.
   Per debate found:
   | Date | Calling Block | Project | Contradictions | Unresolved |
   |------|-------------|---------|----------------|------------|
   
   If 0 debates this week → "No cross-domain analysis performed"

2. INTERFACE DELTA
   Compare ICD status vs last weekly/monthly sync:
   | Interface | Last Status | Current | Changed? | Freeze Due? |
   |-----------|------------|---------|----------|-------------|
   
   Flag: any interface that SHOULD be frozen but isn't

3. ASSUMPTION EXPIRY CHECK
   Scan BD_Assumption_Register.md for verification deadlines this week:
   | AS-ID | Assumption | Deadline | Status | Overdue? |
   |-------|-----------|----------|--------|---------|
   
   Flag: any assumption past deadline with Status ≠ VERIFIED

4. BLOCK PROGRESS vs PLAN
   | Project | Block Last Week | Block This Week | On Track? |
   |---------|----------------|----------------|-----------|
   
   Flag: any block taking >2x expected duration

5. dP/dt PULSE
   Physical actions this week: {{list or "NONE"}}
   If NONE → ⚠️ "Zero physical activity this week"
```

### W2: Traffic Light Summary

```
MICRO-SYNC VERDICT — {{Date}}

🟢 GREEN (no action): All interfaces stable, no expired assumptions, blocks on track
🟡 YELLOW (CEO awareness): {{specific item}} — review at convenience
🔴 RED (CEO action needed): {{specific item}} — resolve before next block

Overall: 🟢 / 🟡 / 🔴

If 🔴: Tag specific action + deadline
If 🟢: "No escalation. Continue sprint."
```

### W3: Save + Route

- Save to `2_Areas/HELIX — Design Execution/Sync-Log/Micro-Sync_{{YYYY-MM-DD}}.md`
- If RED: present to CEO immediately (interrupt current work)
- If YELLOW: present at next CEO checkpoint
- If GREEN: append to sync log silently (CEO reviews at monthly sync)

### Weekly Micro-Sync Rules

1. **Never call a meeting for micro-sync** — it's a written artifact, not a discussion
2. **10-minute hard cap** — if scan takes longer, scope is too broad
3. **Consume domain debate JSON** — the whole point is to harvest cross-domain signals from normal pipeline work
4. **Escalate, don't resolve** — AI flags, CEO decides. No AI recommendations for RED items.
5. **Skip if no HELIX activity this week** — don't generate empty reports

---

## Monthly Sync Protocol (default)

## Workflow

### Part 1: BEFORE — AI Prepares Sync Brief (Offload)

#### Step 1: Collect and Build Sync Brief

Scan vault for each active Tier 1/2 project:
- `1_Projects/{{project}}/Status.md` — phase, blockers, decisions
- ICD registry (helix-integration-debt) — interface status
- Design journal entries since last sync
- Quality gate results if any

Structure sync brief using E1 Weekly Review pattern (from Pattern Library):

```
SYNC BRIEF STRUCTURE (6 sections — adapted from E1):
  1. PROGRESS: What each domain accomplished since last sync (bullet points)
  2. CONSTRAINT CHECK: Is 25h/week CEO capacity being used on highest-leverage cross-domain work?
  3. INTEGRATION STATUS: ICD frozen %, debt trend, unverified assumptions count
  4. DOMAIN ALLOCATION: Hours spent per domain this period — balanced or skewed?
  5. NEXT PERIOD PRIORITIES: Top 3 integration actions ranked by blocking impact
  6. RISK FLAGS: Anything threatening phase gate timeline or physical milestone?
```

Generate pre-meeting document:

```
============================================
   SYNC BRIEF — {{Date}}
   Period: {{last-sync-date}} to {{today}}
============================================

--- Domain Status ---
| Domain | Project | Phase | On Track? | Key Change Since Last Sync |
|--------|---------|-------|-----------|---------------------------|
| Mechanical | VN-AST-MSL-001 | Phase 3 | | |
| Electrical | VN-AST-MSL-001 | Phase 3 | | |
| AI/SW | VN-AST-MSL-001 | Phase 2 | | |
| Mechanical | BB-01 LOMAH | Phase 1 | | |
| Electrical | BB-01 LOMAH | Phase 1 | | |

--- ICD Status Summary ---
| Interface | Status | Owner | Last Updated | Overdue? |
|-----------|--------|-------|-------------|----------|
| IF-001 Mechanical-Electrical | | | | |
| IF-002 Electrical-AI | | | | |
| IF-003 Mechanical-AI | | | | |
| IF-004 System-Environment | | | | |

--- Integration Debt Summary ---
Total open items: __
Trend since last sync: [up/down/stable]
Critical items (severity HIGH):
  1.
  2.

--- Unverified Assumptions ---
| ID | Assumption | Domain | Verification Deadline | Status |
|----|-----------|--------|----------------------|--------|
| | | | | |

--- Risk Flags ---
| Risk | Severity | Affected Domains | Recommended Action |
|------|----------|-----------------|-------------------|
| | | | |
============================================
```

Present sync brief to CEO 24h before meeting. Flag any domain >1 month behind.

### Part 2: DURING — Human Leads 40-Minute Meeting (Core)

CEO runs the meeting. AI does NOT lead — only records.

**Meeting structure:** 15 min domain reports (3x5 min: Mech, Elec, AI — each covers progress, interface concerns, needs from other domains) + 15 min integration discussion (ICD changes, expired assumptions, debt trend, cross-domain conflicts, **interface freeze decisions**) + 10 min next period planning (top 3 deliverables per domain, integration milestones, dP/dt targets).

**Interface Freeze Protocol** — enforce freeze order at each sync:
```
FREEZE ORDER (progressive, cannot skip):
  1. DATA FORMAT    — Digital interface specs (bus protocol, packet format, sample rate)
  2. PHYSICAL       — Mounting holes, envelopes, clearances, connectors
  3. ELECTRICAL     — Pin assignments, voltage levels, power budget, grounding
  4. THERMAL        — Heat dissipation allocation, airflow paths, max junction temp

WHY THIS ORDER:
  - Data format changes late = firmware rewrite + retest (weeks)
  - Physical changes late = re-machining (days-weeks)
  - Electrical changes late = PCB respin ($$$, weeks)
  - Thermal changes late = redesign enclosure (worst case)
  Early items are cheaper to change now but catastrophic if changed later.

AT EACH SYNC, CHECK:
  □ Which interfaces are due for freeze this period?
  □ Are all parties ready to freeze? (prerequisites met)
  □ Any request to UNFREEZE a previously frozen interface? → CEO approval + debt item
```

**CEO responsibilities:** Ensure sync HAPPENS (no postpone >1 week). Ask about integration debt trend and unverified assumptions. Escalate if domain >1 month behind. Resolve cross-domain conflicts. **Approve or defer interface freezes per freeze protocol.**

### Part 3: AFTER — AI Documents Results (Offload)

#### Step 4: Generate Sync Summary

```
============================================
   SYNC SUMMARY — {{Date}}
   Attendees: {{names}}
   Duration: {{minutes}} min
============================================

--- Domain Status (Updated) ---
| Domain | Project | Phase | Status | Next Milestone | Date |
|--------|---------|-------|--------|---------------|------|
| | | | | | |

--- Decisions Made ---
| # | Decision | Rationale | Owner | Impact on ICD? |
|---|----------|-----------|-------|----------------|
| 1 | | | | |
| 2 | | | | |

--- ICD Changes ---
| Interface | Change | Old Spec | New Spec | Effective Date |
|-----------|--------|---------|---------|----------------|
| | | | | |

--- Action Items ---
| # | Item | Owner | Deadline | Priority |
|---|------|-------|----------|----------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

--- Integration Debt Update ---
Items resolved this period: __
Items added this period: __
Net change: __
Trend: [improving/stable/degrading]

--- Next Sync ---
Date: {{next-sync-date}}
Focus: {{anticipated-focus}}
============================================
```

#### Step 5: Update Downstream

Update ICD registry (helix-integration-debt), log decisions (helix-design-journal), update Status.md files, feed summary to BRIDGE KB Layer 3.

## Integration

```
helix-sync-protocol READS FROM:
  - helix-integration-debt → ICD status, debt summary
  - helix-design-journal → decisions since last sync
  - helix-quality-gate → recent gate results
  - 1_Projects/*/Status.md → project status

helix-sync-protocol WRITES TO:
  - helix-integration-debt → ICD changes from sync
  - helix-design-journal → sync decisions logged
  - bridge-knowledge-base → Layer 3 sync summary
  - 1_Projects/*/Status.md → updated milestones
```

## Rules

- Sync MUST happen monthly minimum — if skipped, flag RED on next dashboard
- AI prepares and documents but NEVER leads the meeting
- All ICD changes from sync must be recorded within 24h
- Unverified assumptions past deadline = automatic risk flag
- Domain >1 month behind = CEO escalation required
- Reference: [[Phán đoán không thể uỷ thác cho AI]] — conflict resolution is Core

## COD Classification

- Sync brief preparation: Offload (O1) — AI gathers and formats
- Meeting agenda distribution: Offload (O1) — automated
- Meeting leadership: **Core (C)** — CEO leads, resolves conflicts
- Conflict resolution: **Core (C)** — human judgment required
- Summary documentation: Offload (O1) — AI transcribes and formats
- ICD updates post-sync: Offload (O2) — AI updates, CEO validates
- Action item tracking: Offload (O1) — AI tracks deadlines
