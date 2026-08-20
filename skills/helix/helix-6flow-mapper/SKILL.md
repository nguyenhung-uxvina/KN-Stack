---
name: helix-6flow-mapper
description: Generate and refine the 6-flow function structure — Pahl-Beitz Energy/Material/Signal, with the Signal flow split out into Data and Computation for separate tracing, plus an added Trust flow for human override authority. This skill should be used when the user asks for "function structure", "6-flow", "cấu trúc chức năng", "energy material signal", "6 flow mapping", or needs to decompose a product into sub-functions with domain assignment. A tracing convention for AI-embedded products, not a claim that Pahl-Beitz omitted data or computation.
---

# Helix 6-Flow Mapper — Extended Function Structure for ACH Products

Map product functions using Workshop X's 6-flow convention. Pahl-Beitz uses three flows — Energy, Material, Signal — and its Signal flow **already covers** data, databases and microprocessor processing. This skill splits that Signal flow into three separately-traced lanes (Signal / Data / Computation) and adds a fourth concern, Trust, so that AI-embedded products get one lane per failure mode instead of one lane for all three.

**The split is a tracing convention, not a gap in the source.** See "Honest provenance" below before repeating any novelty claim.

## When to Use

- Phase 1 Task Clarification: building initial function structure
- Phase 2 Conceptual Design: refining functions before concept generation
- When helix-quality-gate Gate 1 requires function structure completeness
- When forge-shift needs to identify WHERE AI replaces hardware
- User asks "what are the sub-functions?" or "show me the function structure"

## The 6 Flows

| # | Flow | Status vs Pahl-Beitz | What It Carries | Why We Trace It Separately |
|---|------|---------------------|----------------|----------------------------|
| E | Energy | in the book | Power, force, heat, motion | Physical actuation and power budget |
| M | Material | in the book | Parts, fluids, consumables | Physical logistics and maintenance |
| S | Signal | in the book | Analog sensor output, commands | Instrumentation boundary |
| D | Data | **split out of Signal** (p.30, p.175) | Digital packets, stored records | Different reliability and integrity requirements than an analog signal |
| C | Computation | **split out of Signal** (p.179, p.449) | AI inference, algorithm output | Shows WHERE ACH operates; inference fails differently from transmission |
| T | Trust | **added** (book mentions it once, p.449) | Human approval, override authority | Forces oversight points to be designed, not assumed |

**How to use the split:** trace a lane per failure mode. A corrupted packet (D), a wrong inference on a correct packet (C), and an operator who cannot intervene (T) are three different faults with three different countermeasures. Pahl-Beitz would call all three "signal" faults. Splitting them is what this skill buys you.

## Honest provenance — read before claiming novelty

Verified against the 3rd English edition PDF, 2026-08-20:

| Claim you might be tempted to make | What the book actually says |
|---|---|
| "P&B has no Data flow" | p.30 lists flows as *"Signals: magnitude, display, control impulse, **data, information** …"* |
| "P&B stops at the ADC" | p.175: *"Storing signals (e.g. in **databases**)"*; p.179: *"…to **process signals using microprocessors**"* |
| "P&B ignores computation" | p.449: *"These data are then **transferred to a computer system for processing**"* |
| "Human override is our idea" | p.449: *"**Humans can intervene, if necessary, to override the system.**"* — one sentence, not a traced flow |
| "Three flows was arbitrary" | p.29 grounds them in Weizsäcker's energy / matter / information — and names **time** as a fourth fundamental quantity, which this skill does *not* add |

**What is genuinely ours:** treating these as *separately traced lanes with their own failure modes*, and promoting Trust from a remark to a design obligation. **AI inference** as a distinct concern is also genuinely outside a 2007 text.

**What is not ours:** the observation that digital data and computation belong in a function structure. That is on page 30.

⚠️ This table exists because the earlier version of this skill claimed a "unique advantage over traditional 3-flow methodology" and asserted "Signal flow ends at the ADC" — both false as descriptions of the source. A skill description routes AI behaviour; a false premise in it propagates. If you want to restore a novelty claim, **measure it first**: run 3-flow and 6-flow side by side on one real product and count the faults each catches.

## Workflow

### Step 1: Gather Requirements

Read project requirements list and _Project_Brief.md:
1. Identify the overall function ("Tổng chức năng")
2. Extract input/output flows from requirements
3. Note any existing function decomposition

### Step 2: Decompose into Sub-Functions

Break overall function into sub-functions. For each, identify which of the 6 flows pass through it.

```
6-FLOW FUNCTION TABLE — {{Project}}
Overall Function: {{description}}
Date: {{date}}

| F-ID | Sub-Function | E | M | S | D | C | T | Domain |
|------|-------------|---|---|---|---|---|---|--------|
| F-01 | Detect projectile impact | x | | x | | | | Mech+Elec |
| F-02 | Convert impact to signal | x | | x | | | | Elec |
| F-03 | Digitize signal | | | x | x | | | Elec |
| F-04 | Classify hit/miss | | | | x | x | | AI |
| F-05 | Display result to operator | x | | | x | | x | Elec+AI |
| F-06 | Allow manual override | | | | | | x | Human |
| F-07 | Log training session | | | | x | | | SW |
| F-08 | Withstand environment | x | x | | | | | Mech |
| F-09 | Mount on target frame | | x | | | | | Mech |

FLOW KEY:
  E = Energy passes through    M = Material passes through
  S = Signal (analog)           D = Data (digital)
  C = Computation (AI/algo)     T = Trust (human oversight)

DOMAIN: Mech / Elec / AI / SW / Human / System
```

### Step 3: Identify ACH Opportunities

Scan for functions where C (Computation) flow exists:
- These are ACH candidates — AI replaces or augments hardware
- Flag each with: "Could commodity sensor + AI replace specialized hardware here?"
- Feed candidates to forge-shift for SHIFT assessment

```
ACH OPPORTUNITY FLAGS — {{Project}}

| F-ID | Function | Current Solution | ACH Alternative | forge-shift? |
|------|----------|-----------------|----------------|-------------|
| F-04 | Classify hit/miss | Threshold comparator | ML classifier | Pending |
```

### Step 4: Identify Interface Points

Where flows cross domain boundaries = interface points:

```
INTERFACE POINTS — {{Project}}

| From F-ID | To F-ID | Crossing | Flow(s) | Maps to ICD |
|-----------|---------|----------|---------|-------------|
| F-02 | F-03 | Elec→Elec | S→D | IF-002 (signal to data) |
| F-03 | F-04 | Elec→AI | D | IF-002 |
| F-04 | F-05 | AI→Elec | D | IF-002 |
| F-05 | F-06 | System→Human | T | IF-004 |
```

Feed interface points to helix-integration-debt for ICD initialization.

### Step 5: Identify Trust Gates

Every function with T (Trust) flow = mandatory human oversight point:

```
TRUST GATES — {{Project}}

| F-ID | Function | Trust Type | Oversight Mechanism | Fallback Level |
|------|----------|-----------|--------------------|----|
| F-05 | Display result | Inform | Operator sees result | — |
| F-06 | Manual override | Override | Operator can reject AI decision | Level 2 |
```

### Step 6: Render Clean Diagram (ASCII)

```
                    ┌─────────────────────────────────────────┐
    Impact ──E,S──→ │ F-01: Detect │──S──→│ F-02: Convert │──S──→│ F-03: Digitize │
                    └──────────────┘      └───────────────┘      └────────────────┘
                                                                        │ D
                                                                        v
    Operator ←─D,T─ │ F-05: Display │←─D──│ F-04: Classify │←─────────┘
         │          └───────────────┘      └────────────────┘
         │ T                                      │ C (ACH)
         v                                        │
    │ F-06: Override │                    (AI model inference)
    └────────────────┘
```

Present diagram for human review. Human corrects missing functions or flows.

## Integration

```
helix-6flow-mapper READS FROM:
  - 1_Projects/*/Phase1*/ → requirements, constraints
  - 1_Projects/*/_Project_Brief.md → overall function description
  - forge-scout → existing ACH opportunity scan

helix-6flow-mapper WRITES TO:
  - helix-integration-debt → interface points for ICD initialization
  - helix-quality-gate → Gate 1 requires function structure
  - forge-shift → ACH opportunity candidates (C-flow functions)
  - 1_Projects/*/Phase1*/ or Phase2*/ → function structure document
```

## Rules

- Every product MUST have at least one T (Trust) flow — no fully autonomous systems
- Computation flow without Trust flow on its output = design error (flag RED)
- Signal and Data are DIFFERENT flows — do not merge them
- Function decomposition should reach 8-15 sub-functions for typical WX products
- Human reviews and corrects the function table — AI draft is starting point only
- Domain assignment drives team allocation and ICD structure
- Reference: [[Phán đoán không thể uỷ thác cho AI]] — Trust flow embodies this principle

## Triple Helix Validation Check (after drafting)

Before handoff to Phase 2, verify completeness:
- [ ] Every D-flow sub-function has a controlling C-flow?
- [ ] Every S-flow has a defined signal path (sensor → processor → actuator)?
- [ ] Energy budget accounts for all E-flow consumers?
- [ ] Material flows include maintenance/consumables?

Any unchecked item = incomplete function structure, return to drafting.

## COD Classification

- Initial 6-flow draft from requirements: Offload (O2) — AI generates, human reviews
- ACH opportunity flagging: Offload (O2) — AI identifies, forge-shift evaluates
- Interface point extraction: Offload (O1) — deterministic from domain boundaries
- ASCII diagram rendering: Offload (O1) — formatting task
- Function review and correction: **Core (C)** — human validates completeness
- Domain assignment (Mech/Elec/AI): **Core (C)** — human decides team structure
- Trust gate placement: **Core (C)** — human determines oversight requirements
