---
name: helix-shadow-dev
description: Validate cross-domain shadow assumptions — each domain maintains a model of what other domains are doing. Run at sync points to catch misalignment before it becomes integration debt. This skill should be used when the user asks about "shadow assumptions", "cross-domain assumptions", "assumption validation", "what does domain X assume about domain Y?", "gia dinh an", or wants to check if domains are aligned on shared assumptions.
---

# Helix Shadow Dev — Cross-Domain Assumption Model Validation

Each domain (Mech/Elec/AI) carries assumptions about the other domains. These "shadow models" diverge silently — by the time the mismatch surfaces, it's integration debt. This skill makes shadow assumptions explicit and forces validation at sync points.

## When to Use

- Before every helix-sync-protocol meeting (automated prep)
- After any major design decision that impacts another domain
- When helix-quality-gate flags "unverified cross-domain assumptions"
- When a domain reports unexpected constraint from another domain
- User asks "are our domains aligned?" or "shadow assumptions"

## The Problem

```
WHAT HAPPENS WITHOUT SHADOW-DEV:

  AI domain assumes: "Compute module fits in 10W thermal envelope"
  Mech domain assumes: "No active cooling needed — AI stays under 5W"
  Reality: AI inference needs 12W → thermal crisis at integration

  This took 6 weeks to discover. Could have been caught in 5 minutes
  if both domains had written down their assumption about the other.
```

## Workflow

### Step 1: Collect Shadow Assumptions Per Domain (using P47 A-Check Method)

Apply PLAUSIBLE "A — Assumptions Audit" methodology (from S1 P47) systematically:

```
EXTRACTION METHOD (from P47 A-Check):
  For EACH design artifact in the project:
    1. Read the artifact
    2. List ALL hidden assumptions found
    3. For each assumption: WHAT → WHERE (file:line or section) → VALID? / NEEDS VERIFICATION
    4. Classify: same-domain (internal) vs cross-domain (shadow)
    5. Cross-domain assumptions → feed into Shadow Assumption Matrix below
```

For each active project, scan design artifacts and extract what each domain assumes about the others:

```
SHADOW ASSUMPTION MATRIX — {{project_id}}
Date: {{today}}
Phase: {{current_phase}}

MECHANICAL DOMAIN assumes about:
| SA-ID | About Domain | Assumption | Source (where stated/implied) | Verified? | Verify By |
|-------|-------------|-----------|------------------------------|-----------|-----------|
| SA-M01 | Elec | "PCB fits in 80x60mm envelope" | DfX_Review.md line 42 | [Y/N] | [date] |
| SA-M02 | AI | "Compute dissipation < 8W" | Thermal estimate note | [Y/N] | [date] |
| SA-M03 | Elec | "Single connector for power+data" | ICD v2 IF-001-03 | [Y/N] | [date] |

ELECTRICAL DOMAIN assumes about:
| SA-ID | About Domain | Assumption | Source | Verified? | Verify By |
|-------|-------------|-----------|--------|-----------|-----------|
| SA-E01 | Mech | "Mounting holes M4 at 45mm spacing" | ICD v2 IF-001-01 | [Y/N] | [date] |
| SA-E02 | AI | "Data format: 12-bit SPI at 50kHz" | Software spec v0.1 | [Y/N] | [date] |
| SA-E03 | Mech | "IP65 achieved by enclosure, not conformal coat" | Assumed | [Y/N] | [date] |

AI/SW DOMAIN assumes about:
| SA-ID | About Domain | Assumption | Source | Verified? | Verify By |
|-------|-------------|-----------|--------|-----------|-----------|
| SA-A01 | Elec | "Sensor latency < 1ms end-to-end" | Algorithm requirement | [Y/N] | [date] |
| SA-A02 | Mech | "Camera FOV unobstructed by structure" | Concept drawing v2 | [Y/N] | [date] |
| SA-A03 | Elec | "GPU available (Jetson Orin / CM4)" | BOM draft v0.1 | [Y/N] | [date] |
```

### Step 2: Cross-Check for Contradictions

Compare shadow assumptions across domains:

```
CONTRADICTION CHECK — {{project_id}}

| Pair | Domain A Assumes | Domain B Assumes | Match? | Action |
|------|-----------------|-----------------|--------|--------|
| SA-M02 vs SA-A03 | "Compute < 8W" | "GPU = Jetson Orin (15W)" | CONFLICT | Resolve at sync |
| SA-E01 vs SA-M01 | "M4 at 45mm" | "M4 at 45mm" | MATCH | Verified ✓ |
| SA-E03 vs SA-M01 | "IP65 by enclosure" | Not stated | GAP | Mech to confirm |

CONFLICT = both domains have stated positions that contradict → MUST resolve
GAP = one domain assumes, the other hasn't stated → MUST clarify
MATCH = both domains agree → mark as verified
```

### Step 3: Classify and Prioritize

```
SHADOW ASSUMPTION STATUS — {{project_id}}

| Status | Count | Action |
|--------|-------|--------|
| VERIFIED (both domains confirmed) | __ | None — document in ICD |
| CONFLICT (contradictory assumptions) | __ | MUST resolve at next sync — blocks gate |
| GAP (one-sided assumption) | __ | Request confirmation from other domain |
| EXPIRED (past verification deadline) | __ | Escalate — convert to debt item |

PRIORITY ORDER:
  1. CONFLICT items — resolve before any design work continues
  2. EXPIRED items — investigate immediately
  3. GAP items — request clarification (set 7-day deadline)
  4. VERIFIED items — document in ICD, remove from tracker
```

### Step 4: Feed Results to Sync Protocol

Output feeds directly into helix-sync-protocol sync brief:
- CONFLICT items → top of integration discussion agenda
- GAP items → action items with owner and deadline
- EXPIRED items → flag as RED in sync brief
- VERIFIED items → update ICD, mark resolved

## Integration

```
helix-shadow-dev READS FROM:
  - 1_Projects/*/Phase*/ → design artifacts for assumption extraction
  - helix-integration-debt → ICD status, existing assumptions
  - helix-concept-generate → Step 5b Assumption Register (if exists)
  - helix-design-journal → decisions that create new assumptions

helix-shadow-dev WRITES TO:
  - helix-sync-protocol → contradiction/gap report for sync brief
  - helix-integration-debt → expired assumptions → debt items
  - helix-quality-gate → unresolved assumptions block gate pass
```

## Rules

- Shadow assumptions MUST be extracted from actual artifacts — not from memory
- AI extracts and cross-checks but NEVER resolves conflicts — human judgment
- Any CONFLICT item unresolved for >2 syncs → automatic RED flag
- Expired verification deadlines convert to integration debt items automatically
- At Gate reviews, ALL shadow assumptions relevant to that phase must be VERIFIED
- Solo CEO context: when 1 person plays all domains, shadow-dev prevents "assuming I'll remember"

## COD Classification

- Assumption extraction from artifacts: Offload (O1) — AI scans files
- Contradiction detection: Offload (O1) — pattern matching
- Gap identification: Offload (O1) — missing-pair detection
- Conflict resolution: **Core (C)** — engineering judgment required
- Verification of physical assumptions: **Core (C)** — requires test or supplier confirmation
- Deadline setting for verification: Offload (O2) — AI proposes, CEO approves
