---
name: helix-integration-debt
description: Track and manage interface control documents (ICDs) and integration debt across Workshop X products. This skill should be used when the user mentions "ICD", "integration debt", "interface", "nợ tích hợp", "interface status", or needs to track cross-domain dependencies in concurrent engineering. The hidden killer in multi-domain product development.
---

# Helix Integration Debt — ICD Registry and Debt Tracker

Track the interfaces between Mechanical, Electrical, and AI domains. Integration debt is the #1 silent killer in concurrent engineering — this skill makes it visible before it becomes catastrophic.

## When to Use

- Setting up interfaces for a new project (Phase 1-2)
- Checking interface status before a quality gate
- When a design change impacts another domain
- Monthly sync prep (feeds helix-sync-protocol)
- When user asks "what interfaces are undefined?" or "ICD status"
- Alert triggered: debt items >10 or trend increasing 2+ syncs

## Interface Categories

All Workshop X products use 4 standard interface types:

| ID | Interface | Example (BB-01 LOMAH) | Example (VN-AST-MSL-001) |
|----|-----------|----------------------|--------------------------|
| IF-001 | Mechanical-Electrical | Piezo mount ↔ charge amp PCB | Tow frame ↔ power/signal cable |
| IF-002 | Electrical-AI | ADC output ↔ hit detection algo | Sensor data ↔ scoring processor |
| IF-003 | Mechanical-AI | Target panel geometry ↔ hit zone map | Tow body shape ↔ RCS model |
| IF-004 | System-Environment | Operating temp range, IP rating | Sea state limits, tow speed range |

## Workflow

### Step 1: Initialize or Load Registry

For new project: create interface registry from function structure (helix-6flow-mapper output).
Use **P53 ICD Template** (from S1 Prompt Library) for new ICD entries:
- Every parameter gets unique code: A1, A2... (physical), B1, B2... (electrical), C1, C2... (environmental), D1, D2... (operational)
- Bold critical parameters (design-driving items)
- Include bidirectional data: OEM→WX and WX→OEM
- Include documentation request section (drawings, 3D models, manuals)
- Include sign-off block (OEM + Workshop X + User witness)

For existing project: load current registry from `1_Projects/{{project}}/ICD/`.

### Step 2: Review Interface Status

For each interface, assess current state:

```
INTERFACE REGISTRY — {{Project}}
Updated: {{date}}

| IF-ID | Interface | Status | Owner | Spec Summary | Assumptions | Verify By |
|-------|-----------|--------|-------|-------------|-------------|-----------|
| IF-001-01 | Piezo mounting holes | Frozen | Mech | M4x0.7, 45mm spacing | Vibration <2g | 2026-04-15 |
| IF-001-02 | PCB enclosure fit | Draft | Elec | 80x60x25mm max | IP65 needed | 2026-04-01 |
| IF-002-01 | ADC data format | Agreed | Elec | 12-bit, 50kHz, SPI | Latency <1ms | 2026-05-01 |
| IF-003-01 | Hit zone coordinates | Undefined | — | — | — | — |
| IF-004-01 | Operating temp | Frozen | Sys | -10 to +55 C | MIL-STD-810 | Verified |

STATUS LEVELS:
  Undefined → Draft → Agreed → Frozen
  (Only CEO/lead can approve Freeze)
```

### Step 3: Track Integration Debt

Debt = any gap, inconsistency, or unresolved interface issue:

```
INTEGRATION DEBT TRACKER — {{Project}}
Updated: {{date}}

| Debt-ID | Description | Severity | Owner | Created | Deadline | Trend |
|---------|-------------|----------|-------|---------|----------|-------|
| D-001 | PCB footprint assumes 4-layer but BOM says 2-layer | HIGH | Elec | 2026-03-01 | 2026-03-15 | = |
| D-002 | Tow cable connector spec not agreed | MED | Mech | 2026-02-20 | 2026-03-30 | up |
| D-003 | AI model input format undefined | HIGH | AI | 2026-03-05 | 2026-03-20 | new |

SEVERITY:
  HIGH — Blocks current phase gate
  MED  — Required before next phase gate
  LOW  — Cleanup, no blocking impact
```

### Step 4: Calculate Metrics

```
INTEGRATION DEBT METRICS — {{Project}}

| Metric | Current | Target (Phase 3 End) | Target (Phase 4 End) |
|--------|---------|---------------------|---------------------|
| Total interfaces | __ | — | — |
| % Frozen | __% | 80% | 100% |
| Open debt items | __ | <5 | 0 |
| HIGH severity items | __ | 0 | 0 |
| Avg resolve time | __ days | <14 days | <7 days |
| Trend (3-sync) | [up/down/stable] | down | — |

QUANTIFIED DEBT (track real cost, not just count):

| Debt-ID | Est. Hours to Resolve | Cost of Delay (per week) | Accumulation Rate |
|---------|----------------------|-------------------------|-------------------|
| D-001 | [hours] | [impact if unresolved: VND or schedule days] | [stable/growing] |
| D-002 | [hours] | [impact] | [stable/growing] |
| ... | ... | ... | ... |

TOTALS:
  Total estimated resolution effort: __ hours
  Total weekly delay cost: __ VND or __ schedule days
  Debt accumulation rate: __ new items/sync (avg over last 3 syncs)
  Debt resolution rate: __ resolved items/sync (avg over last 3 syncs)
  Net flow: [accumulating / draining / stable]

  ★ If accumulation rate > resolution rate for 2+ syncs → STRUCTURAL DEBT
    Action: stop adding features, dedicate sync to debt reduction only

ALERTS:
  [RED]    Debt items > 10
  [RED]    Trend UP for 2+ consecutive syncs
  [RED]    Total resolution effort > 40 hours (1 person-week)
  [YELLOW] Any HIGH severity item past deadline
  [YELLOW] % Frozen < 50% at Phase 3 midpoint
  [YELLOW] Accumulation rate > resolution rate
  [GREEN]  All targets met
```

### Step 5: Generate Change History

When interfaces change, log the delta:

```
ICD CHANGE LOG — {{Project}}

| Date | IF-ID | Change | Old Value | New Value | Reason | Approved By |
|------|-------|--------|-----------|-----------|--------|-------------|
| 2026-03-07 | IF-001-02 | Spec update | 80x60mm | 90x65mm | Added EMI shield | CEO |
```

### Step 6: Alert and Escalate

Automatic alerts:
- Debt items > 10 → flag in helix-sync-protocol brief
- Trend UP for 2+ syncs → CEO escalation
- HIGH severity past deadline → block quality gate
- Assumption verification deadline expired → convert to debt item

## Integration

```
helix-integration-debt READS FROM:
  - helix-6flow-mapper → interface points from function structure
  - helix-quality-gate → gate checklist requires ICD status
  - helix-design-journal → interface-related decisions
  - 1_Projects/*/Phase*/ → design artifacts for consistency check

helix-integration-debt WRITES TO:
  - helix-sync-protocol → ICD status summary for sync brief
  - helix-quality-gate → % frozen metric, debt count
  - bridge-knowledge-base → Layer 2 interface documentation
  - 1_Projects/*/ICD/ → interface registry files
```

## Rules

- New ICD entries MUST follow P53 template with parameter codes (A1/B1/C1/D1)
- Every interface MUST have an owner — "unowned" = automatic HIGH debt
- Only CEO or domain lead can approve Freeze status
- Frozen interfaces require formal change request to modify
- Assumptions without verification deadline = incomplete (flag YELLOW)
- AI checks consistency but NEVER resolves conflicts — human judgment required
- Integration debt at Phase 4 start MUST be 0 for gate pass
- Reference: [[Interface Ownership — Đẩy Function Qua Biên Giới Hệ Thống]]

## COD Classification

- Registry scanning and status tracking: Offload (O1) — AI reads and summarizes
- Inconsistency detection: Offload (O2) — AI flags, human investigates
- Debt trend calculation: Offload (O1) — deterministic computation
- Alert generation: Offload (O1) — threshold-based automatic
- Conflict resolution between domains: **Core (C)** — human judgment
- Freeze approval: **Core (C)** — CEO or domain lead decides
- Assumption verification: **Core (C)** — requires physical validation
