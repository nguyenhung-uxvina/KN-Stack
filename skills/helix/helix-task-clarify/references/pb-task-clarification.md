# Pahl-Beitz Task Clarification — Phase 1 Reference

Source: P&B Ch5 (Task Clarification) + Ch6.1-6.3 (Abstraction + Function Structure)

## Requirements List Structure (P&B 5.2)

### D/W Classification

| Code | Meaning | Rule | VDI 2225 Weight |
|------|---------|------|-----------------|
| **D** (Demand) | BẮT BUỘC — không thỏa hiệp | Thiếu = FAIL toàn bộ design | Elimination criterion |
| **W+** (Wish — major) | Quan trọng, chấp nhận trade-off | Thiếu = giảm giá trị đáng kể | High weight (3-4) |
| **W** (Wish — medium) | Có giá trị, cân nhắc cost/benefit | Thiếu = giảm sức cạnh tranh | Medium weight (2) |
| **W-** (Wish — minor) | Muốn có, không tốn thêm nhiều | Thiếu = vẫn chấp nhận được | Low weight (1) |

### Requirements List Format

```
┌──────┬────────────────────────┬────────┬──────────┬──────────┐
│ D/W  │ Requirement            │ Value  │ Source   │ Changed  │
├──────┼────────────────────────┼────────┼──────────┼──────────┤
│  D   │ Speed ≥ 25 kn          │ 25 kn  │ Navy     │ -        │
│  W+  │ RCS < 0.5 m²           │ 0.5 m² │ Design   │ v1.1     │
│  W   │ Integrated GPS logging │ -      │ Design   │ -        │
│  W-  │ GPS backup             │ -      │ End-user │ -        │
└──────┴────────────────────────┴────────┴──────────┴──────────┘
```

### Main Heading Checklist (P&B Table 5.1)

| # | Category | Ví dụ |
|---|----------|-------|
| A | Geometry | Dimensions, clearances, connections |
| B | Kinematics | Motion types, speeds, accelerations |
| C | Forces | Load types, magnitudes, directions, frequency |
| D | Energy | Power input/output, efficiency, thermal |
| E | Material | Physical/chemical properties, standards |
| F | Signals | I/O, displays, controls, data formats |
| G | Safety | Protection systems, fail-safe, MIL-STD-882 |
| H | Ergonomics | Operation, height, weight, noise |
| I | Production | Workshop capability, tolerances, quality |
| J | Quality | Standards compliance, testing, certification |
| K | Assembly | Transport, packaging, deployment conditions |
| L | Operation | Maintenance intervals, wear parts, training |
| M | Costs | Target unit cost, LCC, production volume |
| N | Schedule | Milestones, prototype dates, delivery |
| O | Transport | Packaging, shipping dimensions, shock rating |
| P | Maintenance | Intervals, wear parts, 3-level maintenance, spares |
| Q | Recycling/Disposal | Tái sử dụng, thải bỏ, hazmat, battery disposal |

## 5-Step Abstraction (P&B 6.1-6.2)

Mục đích: Loại bỏ solution bias, tìm bài toán thiết yếu (essential problem).

```
Step 1: Omit wishes, focus only on Demands
Step 2: Remove specific numbers → qualitative statements
Step 3: Generalize → remove product-specific terms
Step 4: Express in terms of function (verb + noun)
Step 5: Formulate the essential problem (1-2 sentences)
```

### Ví dụ:
- Step 1: "Must detect bullet impact on steel target"
- Step 2: "Must detect projectile contact with surface"
- Step 3: "Must detect mechanical impulse on structure"
- Step 4: "Sense impulse → Convert to signal → Discriminate"
- Step 5: "Convert mechanical impulse into discriminated electrical signal"

## Function Structure (P&B 6.3)

### 3-Flow System (truyền thống)
- **Energy** (E): Lực, chuyển động, nhiệt, điện
- **Material** (M): Vật liệu, chất lỏng, khí
- **Signal** (S): Dữ liệu, điều khiển, feedback

### 6-Flow System (Workshop X extension)
- **Data** (D): Raw sensor data, measurements
- **Computation** (C): AI inference, algorithms
- **Trust** (T): the **veto record** — who overrode which machine decision, when, on what evidence.
  (Not model calibration/validation; that is a property of the C lane. These were conflated until
  2026-08-21 — the same letter meant two different things in two files. See `helix-6flow-mapper`.)

### Function Verb Library

| Category | Verbs |
|----------|-------|
| Convert | transform, rectify, amplify, modulate |
| Vary | increase, decrease, regulate, control |
| Connect | join, couple, link, unite, attach |
| Channel | guide, direct, route, distribute |
| Store | retain, hold, buffer, accumulate |
| Separate | divide, filter, extract, isolate |
| Sense | detect, measure, monitor, capture |

## Three-Step Refinement (P&B 5.2)

Tool for converting vague requirements into quantified specifications. Invoke for any requirement lacking numeric values.

```
Step 1 (Statement):    Vague customer language
Step 2 (Development): Break into measurable sub-aspects
Step 3 (Refinement):  Assign numbers, units, tolerances

EXAMPLE — Defense product:
  Step 1: "Easy maintenance"
  Step 2: 1. Long interval  2. Easy access  3. Easy to learn
  Step 3: 1.1 MTBF ≥1000h  1.2 Grease every 500h  2.1 Hand-open covers  3.1 L1 training ≤2h

EXAMPLE — Naval system:
  Step 1: "Good sea performance"
  Step 2: 1. Wave tolerance  2. Speed  3. Stability
  Step 3: 1.1 Sea State ≥4  2.1 ≥25 kn  3.1 Roll ≤15°
```

**Rule:** Any requirement using forbidden terms (adequate, sufficient, robust, good, high-quality) → MUST pass through Three-Step Refinement before entering the list.

## Binding Yet Provisional Principle (P&B 5.3.1)

Requirements are commitments but MUST be updated as knowledge grows through design phases.

```
BINDING: Mọi yêu cầu đã ghi = cam kết → cơ sở tiến hành công việc
PROVISIONAL: Chưa thể biết hết lúc đầu → cập nhật khi có thông tin mới

REQUIREMENT TIMING TAGS:
  [CONCEPT]    — concept-defining: phải biết trước Phase 2 (determines concept family)
  [STRUCTURE]  — structure-influencing: phải biết trước Phase 3 (determines subsystem division)
  [EMBODY]     — embodiment-determining: phải biết trước Phase 4 (determines shape/size/config)
  [LATE]       — late-bindable: có thể chờ đến Detail Design

RULE: Tag EVERY requirement with timing. Requirements tagged [LATE] may use placeholder
      values initially — mark as [TBD] with planned resolution date.
```

## Task Source Types (P&B 5.1)

| # | Source Type | Definition | Implications |
|---|-----------|-----------|-------------|
| 1 | Development Order | From product planning or external customer | Formal, contractual, MIL-STD heavy |
| 2 | Definite Order | Specific customer contract with specs | Clear specs, focus compliance |
| 3 | Internal Request | From sales, test, or assembly staff | Problem-driven, failure analysis first |
| 4 | Market Analysis | Identified opportunity, no specific customer | Needs ODI, customer validation |
| 5 | Problem Report | Field failures or deficiencies | Root cause before requirements |
| 6 | Regulatory Change | New standards require redesign | Compliance-driven, constraint-focused |

## Obviously Necessary Items (P&B 5.2)

Prompt to capture requirements so basic they might be skipped:

```
CHECKLIST — "What's so obvious it might be forgotten?"
  □ No injury to operator during normal use
  □ No injury to bystanders during operation
  □ Operable in local climate (VN: tropical, salt air, monsoon)
  □ Corrosion resistance for deployment environment
  □ Can be manufactured with available workshop capability
  □ Can be transported to operational site
  □ Complies with applicable safety regulations
  □ Can be stored without degradation for expected shelf life
  □ Spare parts obtainable within acceptable lead time
```

## Implicit Requirements (P&B 5.2)

Prompt: **"What would the customer reject the design for if absent, even though they never stated it?"**

```
IMPLICIT REQUIREMENT DISCOVERY:
  1. Safety: What failure modes could injure someone?
  2. Environment: What VN conditions are assumed? (humidity, salt, heat)
  3. Maintainability: What would make field repair impossible?
  4. Usability: What would frustrate a typical VN military operator?
  5. Logistics: What would prevent deployment to remote sites?
  6. Training: What would require unreasonable training time?

RULE: Every implicit requirement found → add to Requirements List
      with Source = "Implicit — [discovery method]"
```

## Overall Function Black-Box (P&B 6.3.1)

BEFORE sub-function decomposition, state the overall function as an E/M/S transformation:

```
OVERALL FUNCTION — {{product}}

Energy INPUT:  [power sources, kinetic energy, thermal, ...]
Material INPUT: [raw materials, consumables, ammunition, ...]
Signal INPUT:  [commands, sensor data, user input, ...]

       ┌────────────────────────┐
       │   OVERALL FUNCTION     │
       │   (verb + noun)        │
       │   = Essential Problem  │
       └────────────────────────┘

Energy OUTPUT:  [mechanical action, heat, electrical, ...]
Material OUTPUT: [product, waste, debris, ...]
Signal OUTPUT:  [actuation commands, display, data logs, ...]

SOLUTION-NEUTRAL TEST: Can ≥3 different internal structures achieve this?
If NO → statement is too specific, re-abstract.
```

## Partial Requirements Lists (P&B 5.3.2)

In multi-stakeholder environments, each department provides a partial list:

```
PARTIAL LISTS — {{product}}

| Department/Stakeholder | Focus Area | Partial List Received? |
|----------------------|-----------|----------------------|
| Operations/Users | Ease of use, reliability, training | [Y/N/NA] |
| Procurement | Cost, local content, delivery | [Y/N/NA] |
| Production (WX) | Manufacturability, tolerances, supply | [Y/N/NA] |
| Safety/QC | Fail-safe, hazards, compliance | [Y/N/NA] |
| Maintenance | Intervals, access, spares | [Y/N/NA] |
| Logistics | Transport, packaging, storage | [Y/N/NA] |

AGGREGATION: Merge partial lists → identify conflicts → resolve → Product Requirements List
NOTE: For WX solo-CEO context, CEO fills all roles — but STILL walk through
      each perspective systematically to avoid blind spots.
```

## Solution-Idea Isolation (P&B 5.4)

Solution ideas that emerge during requirements work are VALUABLE but must NOT contaminate the requirements list.

```
RULE: Requirements specify WHAT and HOW WELL — never HOW.
      If a solution idea appears during requirements work:
      1. Record it in Solution_Ideas_Log (separate section/file)
      2. Remove solution-specific language from the requirement
      3. Re-express as performance specification

SOLUTION IDEAS LOG:
| # | Idea | Triggered By Req | Phase 2 Relevance |
|---|------|-----------------|-------------------|
| S1 | [solution idea] | R-xxx | [high/medium/low] |

These ideas feed Phase 2 working principle search — they are NOT lost, just parked.
```

## Department Objection Protocol (P&B 5.4 — 4-Step Compilation Step 4)

Before releasing the Requirements List as "v1.0":

```
STEP 4 — CIRCULATE AND INCORPORATE OBJECTIONS:
  1. Draft compiled → circulate to all stakeholders
  2. Each stakeholder reviews for:
     - Missing requirements from their domain
     - Conflicting requirements with their constraints
     - Unrealistic targets they must implement
  3. Incorporate valid objections → update list
  4. Release as v1.0 with stakeholder sign-off

FOR WX SOLO-CEO: Walk through each stakeholder perspective (Step 0.3)
  and explicitly check: "Would [Production/Safety/Ops/Maintenance] object to any requirement?"
```

## Vietnamese Military Context

- Stakeholder access often limited (→ blocking constraint if ≥2 HIGH stakeholders inaccessible)
- TCVN standard numbers: CEO provides, AI does NOT hallucinate
- Minimum 50 requirements for any defense product
- Every requirement MUST have a test method
