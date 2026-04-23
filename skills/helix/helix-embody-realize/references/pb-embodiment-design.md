# Pahl-Beitz Embodiment Design — Phase 3 Reference

Source: P&B Ch7.1-7.4 (Steps, Basic Rules, Principles)

## 15-Step Embodiment Process (P&B 7.1 canonical)

```
PRELIMINARY PHASE (explore layouts)
  [1]  Identify embodiment-determining requirements (size, arrangement, material)
  [2]  Identify spatial constraints → clearance drawings
  [3]  Identify main function carriers
  [4]  Develop preliminary layouts for main function carriers
  [5]  Select suitable preliminary layouts
       ↕ Iterate [4]↔[5]

DETAILED PHASE (develop chosen layout)
  [6]  Develop layouts for remaining main function carriers
  [7]  Search for solutions to auxiliary functions (support, sealing, cooling…)
  [8]  Develop detailed layouts for main function carriers
  [9]  Develop detailed layouts for auxiliary function carriers
       ↕ Iterate [6]↔[9]

EVALUATION & FIX
  [10] Evaluate against technical-economic criteria (Rt/Re + S-diagram)
  [11] Fix preliminary overall layout → frozen baseline
  [12] Optimize and complete form designs, eliminate weak spots
  [13] Check for errors and disturbing factors   ← "ERROR-AND-DISTURBING-FACTOR SEARCH"
  [14] Prepare preliminary parts list and production documents
  [15] Fix definitive layout → approved for detail design / Gate 3
```

**WX extensions** (not in P&B):
- Step 10½: ICD v3 freeze (after CEO approval)
- Step 15½: Phase gate review

**Key insight:** NOT linear — "many actions must be performed simultaneously, additions in one area have repercussions on other areas."

**Block mapping:** B0=[1-2], BA=[3-5], BA½=[early error check on layout], BB=[Basic Rules + Principles + DfX], BC=[6-7 + ICD], BD=[14], BE=[10-13, 15]

## 3 Basic Rules (P&B 7.3)

### Rule 1: CLARITY (Rõ ràng)
- Every function must be clearly assignable to a component
- Force flow must be traceable through structure
- No ambiguous load paths
- **PASS/FAIL criteria:**
  - Force path traced from input → output? (Y/N)
  - Double-fits checked — no over-constrained joints? (Y/N)
  - Thermal path defined for heat-generating components? (Y/N)

### Rule 2: SIMPLICITY (Đơn giản)
- Minimum number of components
- Standard parts wherever possible
- Simple shapes preferred over complex
- **PASS/FAIL criteria:**
  - Part count vs target: ______ / ______ (ratio ≤ 1.2 = PASS)
  - Standard parts ratio: ______% (≥ 60% = PASS)
  - Any custom part replaceable by COTS? (list candidates)

### Rule 3: SAFETY (An toàn)
- **3-level hierarchy (P&B 7.3.3):**
  1. **Direct safety:** safe-life / fail-safe / redundancy — hazard eliminated by design
  2. **Indirect safety:** stored energy principle — protective devices contain failure
  3. **Warnings:** labels, interlocks, procedures — last resort only
- **PASS/FAIL:** Each critical function must have safety level assigned (1/2/3). Level 3 alone = FAIL for Severity I-II hazards.
- **Defense mandate:** MIL-STD-882 system safety analysis

## Design Principles (P&B 7.4)

### 7.4.1 Force Transmission
- Short, direct force paths
- Matched cross-sections (no sudden area changes)
- Avoid bending — prefer tension/compression
- **Defense example:** Recoil path through mount structure

### 7.4.2 Division of Tasks
- One function per component (where practical)
- Separate adjustable functions from fixed ones
- **ACH extension (DfU):** Separate AI-updateable from hardware-fixed

### 7.4.3 Self-Help
- Use internal forces to assist function
- Self-locking, self-centering, self-sealing
- **Defense example:** NC (normally-closed) valve = auto-surface on fault

### 7.4.4 Stability & Bi-stability
- Stable equilibrium preferred
- Bi-stable for switching functions
- Avoid neutral equilibrium (unpredictable)

### 7.4.5 Fault-Free Design
- Fail-safe: safe state on failure
- Fail-operational: continue with degraded performance
- Redundancy: parallel paths for critical functions

## 5 Principles Rapid Audit (P&B 7.4)

Run after Basic Rules, before detailed DfX. Each question = Y/N + evidence.

| # | Principle | Audit Question |
|---|-----------|---------------|
| 1 | Force Transmission (7.4.1) | Force paths short and direct? Uniform strength (no sudden area changes)? |
| 2 | Division of Tasks (7.4.2) | Each part serves one primary function? Adjustable separated from fixed? |
| 3 | Self-Help (7.4.3) | Any passive reinforcement opportunity exploited? (self-lock, self-center, self-seal) |
| 4 | Stability (7.4.4) | Operating point in stable equilibrium? No neutral-equilibrium mechanisms? |
| 5 | Fault-Free (7.4.5) | Each critical function has fail-safe or redundant path? Verified per FMEA? |

**Scoring:** 5/5 Y = PASS. Any N on #1 or #5 = WARN (must address before Gate 3).

## DfX Checklist (Workshop X extended)

| DfX | Mô tả | Key Questions |
|-----|--------|---------------|
| DfM | Manufacturing | Workshop có gia công được? Dung sai đạt không? |
| DfA | Assembly | Lắp ráp được bằng tay? Thứ tự lắp rõ ràng? |
| DfR | Reliability | MTBF target? Single point failures? |
| DfT | Test | Test access? Built-in test points? |
| DfU | Update (AI) | Model swap path? OTA update? Sensor recalibration? |
| DfC | Cost | Target unit cost? Volume pricing? |
| DfMa | Maintenance | Tool access? Wear part replacement? |
| **DfCorrosion** | **Corrosion (--maritime BLOCKING)** | **Galvanic series check? Crevice sealing? Drainage designed? Dissimilar metals isolated?** |
| **DfThermal** | **Thermal management** | **CTE mismatch between mating materials? Max ΔT in service? Thermal path to ambient?** |
| **DfDurability** | **Durability / Fatigue** | **Repeated load cycles? Fatigue life vs service life? Shock/vibration rating?** |
| **DfWear** | **Wear** | **Sliding surfaces identified? Wear allowance in dims? Replaceable wear parts?** |
| **DfTransport** | **Transport / Packaging** | **Lifting points rated? Fits standard vehicle/container? Packaging protects critical surfaces?** |
| **DfQC** | **Quality Control / Inspection** | **Key dimensions measurable with available gauges? Go/no-go feasible? Inspection access without disassembly? Test points accessible?** |
| DfCreep | Creep / Relaxation (polymers) | Sustained load at elevated temp? Creep derating applied? (VN tropical: HDPE shear modulus -80% at 65°C → over-engineer wall or use black PE100) |
| DfAesthetics | Aesthetics (OPTIONAL) | Surface finish spec? Color scheme consistent? Branding placement? (cosmetic — LOW severity) |
| DfRecycling | Recycling / End-of-Life (OPTIONAL) | Material separation possible at EOL? Hazardous materials identified and labeled? (future export markets) |

**Maritime rule:** DfCorrosion is **BLOCKING** for any product with `--maritime` flag or sea environment. FAIL = cannot proceed to Gate 3.

**Polymer rule:** DfCreep is **WARN** for any product using HDPE, nylon, UHMWPE, or polymer composites under sustained load. VN tropical surface temp = 65°C → mandatory derating check.

## Weak Spot Identification Method (P&B 7.6 + Step 12)

**Value Profile Chart** — primary method for finding weak spots:

1. List all evaluation criteria (rows)
2. Plot individual criterion scores as bar chart (0-4 scale)
3. Mark criteria scoring ≤ 2 when others score 3-4 → these are **weak spots**
4. Look for "unbalanced profiles" with extreme variation

```
Criterion        0   1   2   3   4
─────────────────┼───┼───┼───┼───┼
Weight           │   │   │   │ █ │    ← OK (3)
Corrosion resist │   │   │ █ │   │    ← WEAK SPOT (2)
Assembly ease    │   │   │   │   │ █  ← OK (4)
Cost             │   │ █ │   │   │    ← WEAK SPOT (1) ⚠️
Thermal          │   │   │   │ █ │    ← OK (3)
```

**Elimination strategies:**

| Score | Action |
|-------|--------|
| 0 (demand not met) | **Return to Phase 2** — working principle cannot fulfill demand |
| 1 | Major redesign within embodiment, or return to Phase 2 |
| 2 | Targeted improvement — specific DfX action |
| 3-4 | No action needed |

**Return-to-concept trigger (P&B 7.6):**
- Any demand criterion = 0 → MUST return
- ≥ 3 demand criteria = 1 → RECOMMEND return
- Weak spots fundamental to working principle → return
- Economic viability compromised beyond recovery → return

## Error and Disturbing Factor Search (P&B Step 13)

Named check run AFTER weak spot elimination (Step 12), BEFORE parts list (Step 14).

**Errors** = design faults that violate requirements:
- Force path discontinuities
- Tolerance stack-up violations
- Missing retention (parts can loosen/fall)
- Thermal expansion not accommodated

**Disturbing factors** = external influences causing malfunction:
- Temperature extremes (VN: -5°C to +65°C)
- Humidity / salt spray (maritime products)
- Vibration / shock (vehicle-mounted, weapon-fired)
- EMI (near weapon systems, radar)
- Dust / sand ingress (field deployment)
- Human error (assembly, operation)

**Checklist (adapted from P&B Fig 7.148):**
- [ ] Function: unambiguous in all conditions?
- [ ] Layout: material/energy minimized? Simplified?
- [ ] Safety: 3-level hierarchy applied?
- [ ] Ergonomics: operation instructions clear?
- [ ] Production: QC facilitated?
- [ ] Assembly: sequence clear, no special tools?
- [ ] Transport: simplified, lifting points defined?
- [ ] Maintenance: parts replacement feasible?
- [ ] Costs: reduced across design, production, testing?

## Material Selection Quick Reference (Defense)

| Application | Material | Lý do |
|------------|----------|-------|
| Marine structure | Al 5083 | Seawater corrosion resistance |
| Hull/float | HDPE PE100 | Cheap, weldable, impact resistant |
| Precision mount | Steel 4140 | Strength-to-weight, machinability |
| Electronics housing | Al 6061-T6 | EMI shielding, heat dissipation |
| Wear surfaces | UHMWPE | Self-lubricating, abrasion resistant |
| Fasteners (marine) | SS 316 | Corrosion resistance |

## ICD v3 Freeze Checklist

- [ ] All interface signals defined (type, range, protocol)
- [ ] Mechanical interfaces dimensioned (tolerances specified)
- [ ] Power budgets balanced (supply ≥ demand + margin)
- [ ] Thermal analysis complete (worst-case ambient)
- [ ] EMC zones identified
- [ ] Software interfaces versioned (API contracts frozen)

## Phase 3 Documentation Package Template (P&B 7.7)

What a complete Phase 3 output looks like — checklist for Block BE compile:

```
Phase3-Embody/
├── _pipeline_state.md              ← pipeline tracking
├── {{prefix}}B0_Preflight_Report.md   ← embodiment-determining reqs, spatial constraints
├── {{prefix}}Preliminary_Layout.md    ← CEO layout + sketches/CAD screenshots
│   ├── Key dimensions table
│   ├── Material selections with rationale
│   ├── Main function carrier descriptions
│   └── [if maritime] Weight_Estimate.md + Stability_Check.md
├── {{prefix}}DfX_Review.md           ← 16 DfX items (13 standard + 3 optional), each OK/WARN/FAIL
│   ├── Basic Rules Audit (Clarity/Simplicity/Safety) with PASS/FAIL
│   ├── 5 Principles Rapid Audit (5 Y/N)
│   └── PLAUSIBLE 9-check
├── {{prefix}}Basic_Rules_Audit.md     ← detailed audit results
├── {{prefix}}Integration_Check.md     ← Mech×Elec×AI coupling matrix
├── {{prefix}}ICD_v3.md               ← FROZEN interfaces (CEO-approved)
├── {{prefix}}Shadow_Assumptions.md    ← cross-domain assumptions validated
├── {{prefix}}BOM_Draft.md            ← preliminary BOM with cost + VN sourcing
├── {{prefix}}Long_Lead_Items.md       ← items needing early procurement
├── {{prefix}}Embodiment_Evaluation.md ← Rt/Re scores, S-diagram, value profile chart
│   ├── Weak spot list + elimination actions taken
│   ├── Error-and-disturbing-factor search results
│   └── Return-to-concept assessment (all D ≥ 1? ≤ 2 scores of 1?)
├── {{prefix}}P02_QC_Gate.md          ← QC gate pass/fail
└── {{prefix}}Deliverables_Index.md    ← master index linking all above
```

**Minimum viable package** (for Gate 3 readiness):
- Preliminary Layout (with CEO approval signature)
- DfX Review (no unresolved FAIL at severity H)
- ICD v3 (frozen)
- BOM Draft (cost within envelope)
- Embodiment Evaluation (Rt ≥ 0.6, Re ≥ 0.6, no D=0)
