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
- forge-validate → Performance Envelope, validation results, Learning Loop Architecture (Step 1.5 entries)
- forge-fallback → fallback architecture (reassurance material)
- forge-cost → transparent cost-benefit analysis
- HELIX Phase 3 design journal → architectural compliance choices (provider lock-in audit, telemetry-by-default audit, on-device vs cloud inference)
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
| Architecture compliance (air-gapped / provider-agnostic / on-device) | Audited/Pending | Strong/Weak |

## CUSTOMER-FACING MATERIALS
1. Performance Envelope summary (non-proprietary version)
   - Where AI works well: {{conditions}}
   - Where AI degrades: {{conditions}}
   - Where fallback activates: {{conditions}}
2. Fallback explanation (reassurance)
   - "If AI fails, system does THIS automatically"
3. Cost-benefit for customer (total ownership perspective)
4. Case study / field results (if available)

## ARCHITECTURE COMPLIANCE EVIDENCE

For defense customers in compliance-gated environments (tactical isolation, air-gapped networks, no-cloud requirements). Each architectural choice is concrete, auditable evidence — not a marketing claim.

| Compliance dimension | Concrete architectural choice | Audit method | Status |
|---------------------|-------------------------------|--------------|--------|
| Air-gapped operation | All inference on-device; no network calls in decision path | Network capture during 1h field run | Audited / Pending |
| Provider-agnostic | No vendor-specific SDK in production binary (no OpenAI/Anthropic/Cohere SDKs); local model weights only | Binary scan + dependency audit | Audited / Pending |
| Lexical memory (no embeddings) | Retrieval uses BM25 / keyword (not embedding model) — no version-migration risk on provider deprecation | `grep -i embedding` on memory layer; verify zero embedding service calls | Audited / Pending |
| No telemetry-by-default | Field unit ships with telemetry OFF; opt-in only with operator consent | Default-config audit + first-run network capture | Audited / Pending |
| No embedded credentials | Binary contains no API keys, no provider tokens, no callback URLs | `strings` scan + entropy check | Audited / Pending |
| Reproducible model artifact | Model weights + config bundled in single signed artifact; no runtime download | Build artifact inventory | Audited / Pending |

**Pattern source:** TradingAgents (arXiv:2412.20138) Ch 9 — BM25, Not Embeddings. The framework explicitly rejects vector embeddings to preserve provider-agnosticism + offline capability. Same architectural discipline produces compliance evidence for defense buyers: each rejected dependency is one less compliance question to answer at procurement gate.

**Goldilocks Disclosure for architecture:**
- SHARE: which compliance dimensions are met (audit results above)
- SHARE: that retrieval is lexical/local (not how the model is trained)
- DO NOT SHARE: training data sources, model architecture details, internal calibration coefficients
- DO NOT SHARE: which competitor architectures have which weaknesses (sounds like marketing; defense buyers prefer audit-evidence over comparisons)

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
- Architecture compliance is auditable evidence, not a claim — every dimension must have a concrete audit method, not just a checkbox
- Each rejected dependency (no cloud, no provider SDK, no embedding service) is one less compliance question to answer at procurement gate

## COD Classification

- Evidence package compilation: Offload (O2) — AI assembles from forge-validate/fallback/cost
- Engagement tracking: Offload (O1) — AI maintains log
- Customer meetings and demos: **Core (C)** — CEO only
- Trust trajectory assessment: **Core (C)** — requires human relationship judgment
