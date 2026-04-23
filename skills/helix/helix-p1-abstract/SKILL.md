---
name: helix-p1-abstract
description: "Block C of Phase 1 pipeline — run 5-step P&B abstraction to find essential problem, build TVDT (Target Values Decision Table) for top 10-15 requirements. P&B 6.1-6.2 + Weiss & Hari 2015. Can run standalone. Triggers on: 'abstraction', 'essential problem', 'TVDT', 'target values', 'ban chat van de'."
---

# Block C: Abstraction — Essential Problem + TVDT

> **P&B:** 6.1-6.2 (Abstraction) + 5.3 (TVDT extension) | **Pipeline:** helix-task-clarify → Block BC
> **Input:** `BB_Requirements_List_v1.md` | **Output:** `BC_Abstraction.md`, `BC_Essential_Problem.md`, `BC_TVDT.md`
> **Galaxy:** [[Solution-Determining Subfunction]], [[Phán đoán không thể uỷ thác cho AI]]

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Run 5-step P&B abstraction | Decompose into sub-functions (= BD) |
| Propose essential problem statement | Approve essential problem (= CEO Core) |
| Build TVDT for top 10-15 requirements | Search working principles (= Phase 2 BB) |
| Verify solution-free formulation | Include specific technologies in EP |
| Flag if EP contains solution bias | Skip abstraction for "obvious" products |

**Multi-Agent Mode:** NO — abstraction is a sequential reasoning task, single agent with CEO validation.
**CEO Checkpoint:** Essential problem approval = Core, non-delegable. CEO validates the abstraction is solution-free.

## Standalone Usage
```
/helix-p1-abstract VN-XUONG-UUV
```

## Input Requirements
- `BB_Requirements_List_v1.md` — validated D/W requirements
- `BB_Failure_Derived_Reqs.md` — failure context

## Workflow

### Step C1: 5-Step Pahl-Beitz Abstraction

AI executes the abstraction, CEO validates:

```
5-STEP ABSTRACTION — {{project_id}}
Date: {{today}}

Step 1: ELIMINATE personal preferences and implicit assumptions
  Removed: [list brand names, vendor assumptions, solution preferences stripped]

Step 2: OMIT requirements not essential to core function
  Omitted: [list W- requirements and cosmetic items separated]
  Retained: [all D + W+ requirements forming core]

Step 3: TRANSFORM quantitative → qualitative
  | Quantitative | Qualitative |
  |-------------|-------------|
  | "≥50 kN recoil absorption" | "withstand firing forces" |
  | "360° azimuth" | "aim in any direction" |

Step 4: GENERALIZE to broader problem class
  "This is fundamentally a problem of ___"

Step 5: FORMULATE the Essential Problem (1-2 sentences)
  ┌──────────────────────────────────────────────────────────┐
  │ ESSENTIAL PROBLEM:                                        │
  │ "{{solution-neutral statement of core need}}"             │
  └──────────────────────────────────────────────────────────┘

SOLUTION-NEUTRAL TEST:
  Can ≥3 fundamentally different solutions satisfy this EP?
  1. {{solution approach A}}
  2. {{solution approach B}}
  3. {{solution approach C}}
  → If YES: EP is solution-neutral ✅
  → If only 1-2: EP is too specific → re-abstract
```

### Step C2: CEO Validates Essential Problem (Core — Non-Delegable)

Present EP to CEO. This is a JUDGMENT call:
- Does EP capture the TRUE need, not just the stated need?
- Is it abstract enough to enable exploration, but specific enough to guide design?
- Does it match the IFR from Block BB?

**CEO approves, refines, or rejects EP.**

### Step C3: TVDT — Target Values Decision Table (Weiss & Hari 2015)

For top 10-15 most important/controversial D-requirements:

```
TVDT — {{project_id}}
Date: {{today}}

| # | Requirement | Units | Weight | Trade-offs (conflicting req IDs) | Benchmarks (Now / Comp-A / Comp-B) | Target Value | Implication |
|---|------------|-------|--------|--------------------------------|-----------------------------------|-------------|-------------|
| 1 | [req] | [unit] | [H/M/L] | [conflicting R-IDs] | [current / competitor A / B] | [v1.0 target] | [●/○/△] |

IMPLICATION SYMBOLS:
  ● Critical — prime driver (cost, schedule, or concept selection)
  ○ Important — significant effect but not primary
  △ Minor — achievable, proven

TRADE-OFF CONFLICTS:
| Req-A | Req-B | Conflict | CEO Resolution |
|-------|-------|---------|---------------|

ACTION ITEMS (unresolved trade-offs):
| # | Action | Owner | Deadline | Status |
```

**CEO decides target values** — this directly feeds VDI 2225 weights in Phase 2.

**Skip condition:** < 5 D-requirements (very simple product) → skip TVDT.

### ICDM Extension (if --icdm active)
- C-K Theory expansion on essential problem
- Design space mapping (known vs unknown)
- Innovation opportunity framing

## Output

Save to `1_Projects/{{project}}/Phase1-Task/`:
- `BC_Abstraction.md` — 5-step process with intermediate results
- `BC_Essential_Problem.md` — CEO-approved EP (standalone for Phase 2 input)
- `BC_TVDT.md` — Target Values Decision Table (if applicable)

## CEO Checkpoint

```
═══ BLOCK BC ABSTRACTION COMPLETE ═══
Essential Problem: "{{EP statement}}"
Solution-neutral: [YES — 3 solutions identified / NO — needs re-work]
TVDT: {{N}} requirements with target values set
Trade-off conflicts: {{N}} resolved, {{M}} open

CEO:
(1) ✅ Approve EP + TVDT → tiếp tục Block BD (Function Structure)
(2) 🔄 Refine essential problem statement
(3) 🔄 Adjust TVDT target values
(4) ⏸️ Dừng — cần competitor data cho TVDT benchmarks
```

## COD
- 5-step abstraction execution: Offload (O2) — AI runs steps
- **Essential problem validation: Core (C) — CEO judgment**
- TVDT template + competitor data: Offload (O2) — AI populates
- **Target value decisions: Core (C) — CEO chooses**
- **Trade-off resolution: Core (C) — CEO decides**
