---
name: bridge-signal-extract
description: Extract actionable signals from design reviews, test events, customer interactions, and meeting transcripts. This skill should be used when the user wants to capture insights from any interaction, transcribe meeting notes, log design review decisions, or process field feedback. Replaces manual note-taking with structured extraction. Triggers on keywords like extract, transcribe, log meeting, capture insights, design review, test report.
---

# Bridge Signal Extract — Turn Interactions into Data

Extract structured, actionable signals from 4 source types. Stop losing ~40 decisions/week to unstructured meetings.

## When to Use

- After a design review meeting
- After a test event (lab or field)
- After a customer or field interaction
- After a cross-domain sync meeting
- When processing voice transcripts from Tana/StenoAI

## Workflow

### Step 1: Identify Source Type

| Source | Signal Density | Protocol |
|--------|---------------|----------|
| Design Reviews | Highest (~10 decisions/review) | AI prepares agenda, records, extracts within 24h |
| Test Events | High (anomalies are top signal) | AI generates test protocol, extracts within 48h |
| Customer/Field | Medium (unstructured, needs form) | User inputs structured form, AI classifies |
| Cross-Domain Sync | Medium (patterns across products) | AI auto-extracts from helix-sync output |

### Step 2: Extract Signals

For each source, extract into these categories:

**Decisions Made:**
- What was decided
- Why (rationale)
- Alternatives considered and rejected
- Who decided

**Assumptions Stated:**
- Verified assumptions (with evidence source)
- Unverified assumptions (flag for validation)

**Interface Changes:**
- Any ICD parameter changes
- Route to integration debt tracker

**Action Items:**
- Owner, deadline, expected outcome
- Link to project/product

**Risk Flags:**
- Any statement like "I'm worried about X"
- Classify: technical, schedule, resource, safety
- Severity: RED (immediate) / YELLOW (trending) / GREEN (monitor)

**Anomalies (test events only):**
- Unexpected behavior description
- Pattern match: "similar to anomaly in Product B?"
- Root cause hypotheses ranked by likelihood

### Step 3: Validate with Human

Present extracted signals to user for 5-minute validation:
- Correct any misinterpretations
- Add context AI missed
- Confirm priority and routing

NEVER auto-route without human validation. Signal quality degrades if AI misinterprets context.

### Step 4: Route Signals

| Signal Type | Route To |
|-------------|----------|
| Design decisions | KB Layer 2 + design journal |
| Assumptions | Requirements list (verify/update) |
| Interface changes | ICD tracker |
| Action items | Project Status.md |
| Risk flags | bridge-risk-radar |
| Anomalies | KB Layer 2 + validation plan |
| Tacit insights | Galaxy note candidates |
| Cross-product patterns | KB Layer 3 |

### Step 5: Output Format

Generate a structured Signal Report:

```
## Signal Report
**Source:** [Design Review / Test Event / Customer / Sync]
**Date:** YYYY-MM-DD
**Product:** [product name]
**Participants:** [names]

### Decisions (N items)
| # | Decision | Rationale | Alternatives Rejected |
|---|----------|-----------|----------------------|

### Assumptions (N items)
| # | Assumption | Status | Evidence |
|---|-----------|--------|----------|

### Action Items (N items)
| # | Action | Owner | Deadline |
|---|--------|-------|----------|

### Risk Flags (N items)
| # | Risk | Severity | Category |
|---|------|----------|----------|

### Galaxy Candidates (N items)
| # | Insight | Why Galaxy-worthy |
|---|---------|-------------------|
```

## Integration Points

- Feeds into: bridge-knowledge-base (KB Layer 2+3)
- Feeds into: bridge-risk-radar (risk flags)
- Feeds into: bridge-flywheel (insight generation count)
- Receives from: HELIX sync protocol summaries
- Receives from: User input (meeting notes, test data, field reports)

## Metrics

- Signal capture rate: % of design reviews with extraction (target: 100%)
- Extraction latency: hours from event to structured output (target: 24h)
- Validation rate: % of extractions human-validated (target: 100%)

## COD Classification

- Extraction: Offload (O2) — AI extracts, human validates
- Routing: Offload (O1) — AI routes to correct location
- Validation: Core (C) — human confirms interpretation
- Galaxy candidate judgment: Core (C) — human decides worthiness
