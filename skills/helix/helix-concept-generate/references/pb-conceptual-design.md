# Pahl-Beitz Conceptual Design — Phase 2 Reference (Ch6 Complete)

Source: P&B Engineering Design, Chapter 6 (Sections 6.1–6.5.3)
Supplementary: Ch6 Meta-Learning Analysis files, Galaxy permanent notes

---

## 6.1 Steps of Conceptual Design — Overview

The conceptual design phase transforms the **essential problem** (from Phase 1 abstraction) into **principle solutions** ready for embodiment. It presupposes:
- Requirements list with D/W classification
- Function structure with sub-functions identified
- Essential problem CEO-approved

**Phase 2 Steps (sequential with iteration loops):**
1. Abstract to identify essential problems (verify from Phase 1)
2. Establish function structures
3. Search for working principles
4. Combine working principles
5. Select suitable combinations
6. Firm up into principle solution variants
7. Evaluate against technical and economic criteria
8. Select and decide (CEO)

**Key insight (VDI 2221 Evolution):** This is NOT waterfall. Feedback loops between steps are EXPECTED. Real engineers skip, reverse, and parallelize. P&B is an adaptive framework to CONFIGURE, not a recipe to FOLLOW.

---

## 6.2 Abstracting — 5-Step Process

Verify essential problem passes all 5 steps:

| Step | Action | Test |
|------|--------|------|
| 1 | Eliminate personal preferences | No brand names or suppliers in problem statement |
| 2 | Omit non-functional requirements | Focus on WHAT, not HOW |
| 3 | Transform quantitative → qualitative | Core function in general terms |
| 4 | Generalize results | Not locked to one solution class |
| 5 | Formulate solution-neutral | ≥3 fundamentally different solutions satisfy this |

**5 Crux Questions:**
1. What is the REAL purpose of this system?
2. What are the genuine vs. fictitious constraints?
3. What functions MUST the system perform?
4. What are the boundary conditions?
5. What is the essential problem stripped of all assumptions?

**Constraint Classification Gate (B0/BA deliverable):**
For each constraint in the requirements list, CEO must classify:
- **GENUINE** — physics, regulation, or immovable resource limit (keep)
- **FICTITIOUS** — assumed from habit, prior product, or unquestioned tradition (challenge or remove)
Document classification in B0_Preflight_Report. Fictitious constraints that survive review become WISH, not DEMAND.

**Solution-Neutral Verification (BA deliverable):**
The essential problem statement MUST pass this test: list ≥3 fundamentally different solution classes that satisfy it. If only 1-2 → the statement is too specific → re-abstract. Document the ≥3 solution classes in Problem_Frame.md as evidence.

---

## 6.3 Establishing Function Structures

### 6.3.1 Overall Function

- Represented as: INPUT → TRANSFORMATION → OUTPUT
- Three essential flow types: **Energy, Material, Signal**
- Workshop X extension: + **Data, Computation, Trust** (6-flow)
- System boundary determines overall function — same system, different boundary = different function
- **Solution-neutral test:** List ≥3 different solutions. If only 1 → function too specific

### 6.3.2 Breaking Down into Subfunctions

**Decomposition depth depends on design type:**
| Type | Strategy | Depth |
|------|----------|-------|
| Original | Deep everywhere — full WP search per SF | Maximum |
| Adaptive | Deep on NOVEL SFs, shallow on known | Selective |
| Variant | Minimal — focus on changed parameters | Minimum |

**Key concepts:**
- **Main flows first, auxiliary flows second** — main flows carry core function, auxiliary enable it
- **Solution-determining subfunction:** ONE SF exists where WP choice cascades through entire design. Identify and solve FIRST.
  - **Identification method:** Score each SF on two axes: (1) How many other SFs are constrained by this SF's WP choice? (cascade count, 0-N) (2) How many fundamentally different WPs exist for this SF? (solution breadth). The SF with highest cascade × lowest breadth = solution-determining. Document in Problem_Frame.md.
- **Generally valid functions** enable access to design catalogues (standardized terminology)
  - **Catalogue routing:** When a SF uses a generally-valid function verb (Convert, Transmit, Store, etc.), search design catalogues (Roth, Koller, VDI classification) BEFORE brainstorming. This grounds BB search in proven physical effects rather than improvisation.
- **Task-specific functions** used when no generally-valid equivalent exists

**Function verb library:** Convert, Transform, Transmit, Store, Separate, Connect, Channel, Rectify, Amplify, Reduce, Sense, Display, Process, Control

### 6.3.3 Practical Application — 11 Guidelines

1. Function structure depends on problem interpretation
2. Detail degree depends on task novelty + designer experience
   - **Enumerate-first rule (§6.3.3 G2):** If function relationships are unclear, enumerate subfunctions WITHOUT logical/physical connections first. Arrange by extent of realization, then add connections in a second pass. Do not force a connected structure prematurely.
3. Need not aim for full completeness if suitable variants exist
4. Should lead to effective solution search without premature solution bias
5. Several forms of representation possible
6. Physical structure follows from function structure (modular alignment)
7. **Function structure can be VARIED** to find better solutions (not frozen)
   - **CARS Variation Methods (§6.3.3 G7):** 4 systematic methods to generate structurally distinct function structures:
     - **C**ombine/Break: Merge or split subfunctions (e.g., combine "Deploy" + "Control" into single module)
     - **A**rrange: Change sequence/arrangement of subfunctions
     - **R**econnect: Switch series/parallel/bridge connections between SFs
     - **S**hift boundary: Move system boundary (include/exclude functions)
   - Mandate ≥2 function structure variants using CARS before proceeding to WP search
   - Different structures produce genuinely different architectures, not just column-swap variants in morpho matrix
8. Individual subfunctions & relationships clearly identified
9. Task-specific functions help when no generally-valid functions exist
10. Generally-valid functions enable access to catalogues
11. Each subfunction treated as equally important
   - **G11 Guard (§6.3.3):** ALL subfunctions from the function structure MUST appear as rows in the morphological matrix. No SF may be marked "secondary" or deprioritized. Auxiliary SFs (safety, thermal, control) are equally important — a system that fires but overheats is useless. B0 preflight MUST verify this before BB proceeds.

---

## 6.4 Searching for Working Principles

### 6.4.1 Seven Search Methods (prioritized)

| # | Method | Description | Reliability | Priority |
|---|--------|-------------|------------|----------|
| M1 | Literature/standards | Handbooks, MIL-STD, patents, design catalogues | HIGH | ALWAYS START HERE |
| M2 | Natural systems | Biomimicry, physical phenomena | MEDIUM | Creative input |
| M3 | Known technical systems | Competitor analysis, teardown, existing products | HIGH | Proven solutions |
| M4 | Analogies | Cross-domain transfer from adjacent industries | CREATIVE | Innovation driver |
| M5 | Physical process analysis | Physical effects catalogs (Koller, Roth) — see catalogue below | HIGH | Systematic |
| M6 | Classification schemes | Design catalogues, Zwicky morphological method | HIGH | Systematic |
| M7 | TRIZ inventive principles | 40 principles, contradiction matrix | HIGH | Innovation Level 2+ |

### Working Principle 3-Component Rule (§6.4.1)

Each working principle in the morphological matrix MUST specify 3 components:
- **[Effect]** — the physical effect or principle exploited (e.g., piezoelectric effect, electromagnetic induction)
- **[Geometry hint]** — brief geometric characteristics (size, motion type, arrangement)
- **[Material hint]** — material state or type (solid/liquid/gas, rigid/flexible, specific material)

**Hybrid WPs:** When a WP combines ≥2 physical effects, mark as **[HYB]** in the matrix cell. Example: `[HYB] Piezo+strain | disc+bridge | PZT+steel`

Stopping at physical effect alone makes it impossible to assess compatibility or feasibility.

### M5 Physical Effects Catalogue (Koller/Roth — defense-relevant subset)

**Usage:** For each SF, look up the sub-function verb → find applicable physical effects → derive WPs with geometry+material. This is the systematic backbone of BB search — do NOT skip in favor of brainstorming alone.

| Sub-function Verb | Physical Effect | Working Principle (Effect+Geometry+Material) |
|-------------------|----------------|----------------------------------------------|
| **Sense** force | Piezoelectric effect | PZT disc + charge amp + steel housing |
| Sense force | Resistive strain | Strain gauge + Wheatstone bridge + steel beam |
| Sense force | Capacitive | Parallel plates + dielectric + MEMS silicon |
| **Sense** position | Hall effect | Hall sensor + magnet + PCB mount |
| Sense position | Optical encoder | LED + disc + photodetector |
| Sense position | Inductive (LVDT) | Coil + ferrite core + aluminum housing |
| **Absorb** energy | Viscous damping | Hydraulic buffer + orifice + steel cylinder |
| Absorb energy | Elastic deformation | Spring-damper + steel coil + rubber mount |
| Absorb energy | Friction | Brake pad + disc + cast iron caliper |
| **Convert** motion | Electromagnetic induction | DC servo + gearbox + aluminum frame |
| Convert motion | Hydraulic pressure | Cylinder + piston + steel manifold |
| Convert motion | Pneumatic pressure | Air cylinder + solenoid valve + aluminum |
| Convert rotation→linear | Screw thread | Ball screw + nut + steel shaft |
| Convert rotation→linear | Rack and pinion | Gear + rack + steel housing |
| **Transmit** signal | Electromagnetic wave | LoRa 433MHz, WiFi, 4G |
| Transmit signal | Optical fiber | Glass fiber + transceiver + ruggedized connector |
| Transmit signal | Wired electrical | Shielded cable + MIL-spec connector |
| **Store** energy | Electrochemical | LiFePO4 cell + BMS + aluminum case |
| Store energy | Mechanical (spring) | Torsion spring + steel + preload mechanism |
| Store energy | Pneumatic (pressure) | Air tank + regulator + steel vessel |
| **Separate** material | Filtration | Mesh filter + housing + stainless steel |
| **Connect** parts | Fastener (bolt) | M8 bolt + nut + washer + steel |
| Connect parts | Welding | Fillet weld + 5083 aluminum + MIG |
| Connect parts | Adhesive | Epoxy + surface prep + composite bond |

*Each WP includes all 3 components per the 3-Component Rule. For full Koller/Roth catalogues, consult P&B Appendix or VDI design catalogue databases.*

### Compatibility Analysis — 8 Types

Before combining WPs, verify pairwise compatibility:

| Type | Check | Example Issue |
|------|-------|---------------|
| 1. Energy flow | Same voltage/power level? | 24V motor + 5V controller |
| 2. Geometric | Fit in same space? No interference? | Actuator too large for housing |
| 3. Material | Compatible materials? CTE match? | Aluminum-steel galvanic corrosion |
| 4. Signal/control | Same protocol? Timing? Bandwidth? | SPI sensor + I2C bus |
| 5. Temporal | Sequence compatible? Latency OK? | Slow sensor + fast control loop |
| 6. Environmental | All survive same conditions? | MIL-STD-810 tropical salt vibration |
| 7. Manufacturing | All producible in VN workshop? | CNC 5-axis part + manual welding |
| 8. Supply chain | All components available? No single-source? | Sanctioned country supplier |

### Pre-Morpho Hard Filter (§6.4.2)

Before DSO ranking, apply a binary DEMAND filter to each WP:
- For each WP: **Does it violate any DEMAND requirement? YES → eliminate immediately.**
- Only WPs that pass ALL demands proceed to DSO scoring.
- Document eliminated WPs and which demand they violated.

This prevents wasting DSO scoring effort on infeasible solutions.

### DSO Pre-Ranking (Combinatorial Explosion Management)

When N SFs × M WPs = too many combinations:
- Score each WP: Performance (1-4) × Risk (1-4) = DSO Score (1-16)
- ≥12 = Strong (prioritize), 6-11 = Viable, ≤5 = Weak (exclude)
- Rearrange table: best WPs left → left-path = strongest baseline
- Reduces evaluation effort by ~90%

### 6.4.2 Combining Working Principles — Morphological Matrix

**Format:**

```
┌─────────────────┬──────────┬──────────┬──────────┬──────────┐
│ Sub-function     │ Sol. 1   │ Sol. 2   │ Sol. 3   │ ACH Sol. │
├─────────────────┼──────────┼──────────┼──────────┼──────────┤
│ F1: Detect       │ Piezo    │ MEMS     │ Laser    │ AI+Cam   │
│ F2: Transmit     │ LoRa     │ WiFi     │ Cable    │ Edge+4G  │
│ F3: Process      │ MCU      │ FPGA     │ SBC      │ Jetson   │
│ F4: Display      │ LED      │ LCD      │ Sound    │ AR       │
└─────────────────┴──────────┴──────────┴──────────┴──────────┘
       Concept A: ─────┐─────┐─────┐─────┐
       Concept B: ┐─────────┐─────┐─────────┐
       Concept C: ┐─────┐─────────┐─────┐
```

**Rules:**
- ACH column MUST be present for every sub-function (Workshop X unique)
- **Recommended column grouping (§6.4.2):** Group morpho columns by energy domain (mechanical / electrical / software / passive) to reveal compatibility patterns and domain coupling. P&B treats this as standard practice for multi-domain systems — apply for all Original designs, optional for Variant.
- Only combine COMPATIBLE working principles (check 8 types above)
- Check physical + geometric + E-M-S flow continuity
- ≥3 concept variants REQUIRED
- Working structure documentation: describe how WPs work as integrated system
- Principle sketches: hand-drawn preferred at this stage (freedom to explore)

**Source marking:** (L)=Library, (S)=Standards, (A)=ACH, (H)=Human, (T)=TRIZ

---

## 6.5 Developing Concepts

### Time Distribution (P&B 6.5.3) — Pipeline Budget Guide
- B0+BA+BB (Searching & Combining): **25%** of Phase 2 effort
- BC (Calculating & Representing — firming up): **60%** ← majority of effort. If BC feels rushed, the pipeline is over-investing in search.
- BC+BE (Evaluation & Selection): **15%**
- **Warning:** If BB takes longer than BC, the balance is inverted — too much searching, not enough calculating. Flag to CEO.

### Two-Stage Evaluation (Galaxy insight)

**Stage A — Pugh Matrix (fast screening):**
- Use 4-6 most important criteria (≥70% QFD weight coverage)
- Compare relatively (+/S/-) against datum
- Eliminate concepts with negative NET scores
- **Purpose:** Reduce field to top 2-3 before investing in VDI 2225

**Stage B — VDI 2225 (deep evaluation):**
- Full criteria set (15-30 criteria, ≥95% coverage)
- Score 0-4, multiply by weights
- Technical Value ≥ 0.6 required

### 6.5.1 Firming Up into Principle Solution Variants

**7 Firming Up Methods:**
| Method | Description | When to Use |
|--------|-------------|-------------|
| F1. Rough calculations | Simplified assumptions, ±30% accuracy | ALWAYS — minimum for every concept |
| F2. Principle sketches | Hand-drawn, showing key dimensions | Novel/critical elements |
| F3. Quick experiments | Bench tests, proof-of-concept | Solution-determining SFs |
| F4. Physical models | Mockups, 3D prints | Spatial/ergonomic verification |
| F5. Simulation | FEA, CFD (only if F1-F4 insufficient) | Complex physics |
| F6. Literature data | Published performance data | Standard components |
| F7. Market research | Existing product benchmarks | COTS solutions |

**Properties to estimate per concept:**
- Performance (key metric)
- Reliability (MTBF estimate)
- Fault susceptibility
- Approximate size (L×W×H)
- Weight estimate
- Cost estimate (rough ±30%)
- Service life
- VN manufacturability
- ACH readiness (if applicable)

**Detail level decisions (P&B 6.5.3):**
- HIGH detail: Novel principles, critical interfaces, safety-critical elements
- LOW detail: Standard COTS, well-understood subsystems
- Working principles → hand sketching (freedom). Principle solutions → CAD (efficiency)

**Key rule:** Firming up ≠ detail design. Just enough to COMPARE. Over-detailing at Phase 2 wastes time.

**Iteration Exit Condition (§6.5.1):** If firming up reveals a concept fails feasibility (violates a DEMAND, physically impossible, cost-prohibitive), trigger a formal "Back to BB" loop:
1. Document which concept failed and why
2. CEO approves the loop (not automatic)
3. Return to morphological matrix with new constraint knowledge
4. May need 2-3 selection-firming cycles for complex systems — this is EXPECTED, not failure

### 6.5.2 VDI 2225 Evaluation — 8-Step Process

**Scoring Scale:**

| Score | Meaning | Keyword |
|-------|---------|---------|
| 0 | Absolutely unsatisfactory | Unacceptable |
| 1 | Just tolerable | Poor |
| 2 | Adequate | Sufficient |
| 3 | Good | Satisfactory |
| 4 | Very good (ideal) | Excellent |

**Tendency signs:** 2↑ = almost 3, 3↓ = barely 3
**Uncertainty marks:** 3? = uncertain, need more data

**8 Steps:**
1. **Identify evaluation criteria** — from requirements list + checklist (Function, WP, Embodiment, Safety, Ergonomics, Production, QC, Assembly, Transport, Operation, Maintenance, Recycling, Costs). Optimal: 15-30 criteria. Must be independent.
2. **Weight criteria** — ODI scores (best) > D/W classification > expert judgment
3. **Compile evaluation parameters** — define what 0 and 4 look like for each criterion
4. **Assess values (scoring)** — score 0-4 with tendency signs and uncertainty marks
5. **Determine overall value** — x_t = Σ(w_i × s_i) / (4 × Σw_i), threshold ≥ 0.6
6. **Compare** — Rt-Re S-diagram (**MANDATORY output** in VDI_2225_Evaluation.md: plot all concepts on x_t vs x_e axes, draw diagonal + threshold lines. Above diagonal = good value, below = over-engineered. This visualization is required — numeric scores alone are insufficient.)
7. **Estimate uncertainties** — for scores marked ?, what range? Does it change ranking?
8. **Search for weak spots** — score ≤1 = WEAK, 2+ below average = RELATIVE WEAK, high ? = RISK

**Weight Sources (priority order):**
1. ODI opportunity scores: ≥15→4, 12-15→3, 10-12→2, <10→1
2. Requirements D/W classification: D→4, W1→3, W2→1
3. Expert judgment (least preferred, document rationale)

**Evaluation Formula:**
```
Technical Value:  x_t = Σ(w_i × s_i) / (4 × Σw_i)
Economic Value:   x_e = Σ(w_j × s_j) / (4 × Σw_j)

x_t, x_e ∈ [0, 1]
Threshold: x ≥ 0.6 (below = eliminate)
```

**S-Diagram:**
```
x_e ↑
1.0 │         ○ Ideal
    │       /
    │     /  ● Concept A
    │   /      ● Concept B
0.6 │─/─────── Threshold
    │/  ● Concept C (eliminate)
    └──────────────────→ x_t
   0.0   0.6        1.0
```

**Weak Spot Detection:**
- Score ≤ 1 on ANY criterion → WEAK SPOT (potential project killer)
- Score 2+ below concept average → RELATIVE WEAK SPOT
- High uncertainty (?) on high-weight criterion → RISK SPOT

**Golden Rule:** "Balanced 75% > Unbalanced 85%"
A concept with all 3s (balanced) is SAFER than one with mix of 4s and 1s.

**Value Profile Analysis:** Plot bar chart per criterion to visualize balance vs. imbalance.

### 6.5.3 Practical Application

**Handoff to Embodiment requires:**
- Selected concept with CEO rationale documented
- Weak spots identified with mitigation plans
- Traceability: every Phase 1 requirement → concept feature
- ICD v2 with concept-specific interfaces
- Rough calculations and sketches from firming up
- Action items from CFMA tracked into Phase 3
- **Resource/team implications (§6.5.3 Organizational Transition):**
  - Team expansion needs (new specialists, skill gaps)
  - Supplier engagement required for selected concept
  - Budget reallocation based on concept cost envelope
  - Reporting/review structure changes for Phase 3

**Stakeholder presentation format:**
- Engineering team: Full VDI 2225 data + coupling analysis
- Management/CEO: Summary ranking + risk assessment + cost implications
- End users (military): Performance envelope + operational context

---

## Coupling Analysis (Workshop X Extension)

### Cross-Domain Coupling Matrix

| | Mech | Elec | AI/SW |
|---|---|---|---|
| **Mech** | — | Mounting, EMC | Sensor placement |
| **Elec** | Power budget | — | Data interface |
| **AI/SW** | Actuator control | Compute hardware | — |

**Coupling severity:**
- LOW: Interface spec sufficient
- MEDIUM: Joint design review needed
- HIGH: Co-design required (→ integration risk)

**Thresholds (total coupling score 0-40):**
- < 15: Low risk — domains work independently
- 15-25: Medium — need regular sync points
- > 25: High — consider simplification
