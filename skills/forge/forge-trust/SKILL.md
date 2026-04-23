---
name: forge-trust
description: Build and track customer trust evidence for ACH products in defense markets. This skill should be used when the user asks about "customer trust", "demo preparation", "trust evidence", "defense customer engagement", "chung minh cho khach hang", "customer relationship tracking", or "trust metrics". Trust is the currency of defense sales.
---

# Forge Trust — Customer Trust Evidence Building

Build and track trust evidence packages for defense customers evaluating ACH products. Trust builds linearly but collapses exponentially — every interaction either builds or erodes. Output: trust evidence package, engagement log, and trust trajectory.

## When to Use

- Before customer demonstrations or presentations
- When forge-validate produces results worth sharing
- When bridge-risk-radar flags trust decay (60+ days no contact)
- Monthly trust review as part of FORGE protocol

## Workflow

### Step 1: Gather Evidence

Read:
- forge-validate → Performance Envelope, validation results
- forge-fallback → fallback architecture (reassurance material)
- forge-cost → transparent cost-benefit analysis
- `1_Projects/{{project}}/Status.md` — current readiness

### Step 2: Generate Trust Evidence Package

```
TRUST EVIDENCE PACKAGE — {{product}}
Date: {{today}}  |  Customer: {{customer_name}}

## EVIDENCE SUMMARY
| Evidence Type | Status | Strength |
|--------------|--------|----------|
| Performance Envelope (from forge-validate) | Available/Pending | Strong/Weak |
| Fallback architecture (from forge-fallback) | Designed/Tested | Strong/Weak |
| Cost-benefit analysis (from forge-cost) | Done/Draft | Strong/Weak |
| Live demonstration capability | Ready/Not Ready | Strong/Weak |
| Field deployment data | Available/None | Strong/Weak |
| Comparison vs hardware alternative | Done/Not Done | Strong/Weak |

## CUSTOMER-FACING MATERIALS
1. Performance Envelope summary (non-proprietary version)
   - Where AI works well: {{conditions}}
   - Where AI degrades: {{conditions}}
   - Where fallback activates: {{conditions}}
2. Fallback explanation (reassurance)
   - "If AI fails, system does THIS automatically"
3. Cost-benefit for customer (total ownership perspective)
4. Case study / field results (if available)

## CUSTOMER CONCERN TRACKER
| # | Concern | Source | Status | Response |
|---|---------|--------|--------|----------|
| C-1 | | Meeting/Email/Inferred | Open/Addressed | |

## ENGAGEMENT LOG
| Date | Type | Attendees | Key Takeaway | Follow-up |
|------|------|-----------|-------------|-----------|
| | Meeting/Demo/Email | | | |

## TRUST TRAJECTORY
- Trend: UP / FLAT / DOWN
- Last engagement: {{date}} ({{days ago}})
- Next planned engagement: {{date}}
- Alert: >60 days no contact = trust decay risk
```

### Step 3: Customer Engagement (Core — Non-Delegable)

CEO executes all customer-facing interactions:
- Present evidence face-to-face (preferred)
- LISTEN: capture unspoken concerns (political, career-risk, organizational)
- Demonstrate live system (hands-on experience)
- Invite customer to witness validation testing
- Manage relationship across customer organization (not just technical PoC)

### Step 4: Track Trust Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| Days since last engagement | Calendar | < 60 |
| Concerns open vs resolved | Count | Trending down |
| Customer-initiated contact | Frequency | Increasing |
| Demo/witness requests | Count | > 0 |
| Repeat business / renewals | Revenue | Growing |

### Step 5: Trust Decay Alert

Flag for bridge-risk-radar when:
- No customer contact in 60+ days
- Open concerns not addressed in 30+ days
- Customer tone shift detected (from proactive to passive)
- Competitor mentioned in customer communications

## Key Principle

```
TRUST IN DEFENSE:
- Builds: linearly, through consistent evidence and transparency
- Collapses: exponentially, through one failure or broken promise
- Decides WHEN to show what: premature demo of unstable system DESTROYS trust
- Is HUMAN-TO-HUMAN: AI packages evidence, humans deliver trust
```

## HELIX Integration

```
forge-trust READS FROM HELIX:
  - Product readiness → is it demo-ready?
  - Design journal → any known issues to disclose?
  - Quality gate → has it passed required gates?

forge-trust WRITES TO:
  - bridge-risk-radar → trust decay alerts
  - forge-portfolio → customer engagement status
  - forge-evolve → trust as competitive moat metric
```

## Rules

- ALL customer interactions are Core — never delegate to AI
- Transparency builds trust: share Performance Envelope honestly including failure conditions
- Never demo an unstable system — better to delay than destroy trust
- Track unspoken concerns — political and career risk drive defense decisions
- Goldilocks Disclosure applies — know what to share vs protect

## COD Classification

- Evidence package compilation: Offload (O2) — AI assembles from forge-validate/fallback/cost
- Engagement tracking: Offload (O1) — AI maintains log
- Customer meetings and demos: **Core (C)** — CEO only
- Trust trajectory assessment: **Core (C)** — requires human relationship judgment
