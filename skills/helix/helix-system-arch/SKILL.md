---
name: helix-system-arch
description: "VDI 2206 System Design phase for mechatronic products — cross-domain architecture, interface contracts, domain budget allocation, and V&V planning. Inserts between Phase 1 (Task Clarification) and Phase 2 (Conceptual Design). Only for products with Mech+Elec+SW. Pure mechanical products SKIP. Triggers on: 'system architecture', 'system design', 'cross-domain', 'kien truc he thong', 'VDI 2206', 'mechatronic architecture', 'domain allocation', 'interface contract'."
---

# Helix System Arch — VDI 2206 System Design for Mechatronic Products

> **Standard:** VDI 2206:2021 "System Design" process module
> **Position:** Between Phase 1 (Task Clarification) and Phase 2 (Conceptual Design)
> **Purpose:** Establish cross-domain system architecture BEFORE concept search begins
> **Principle:** Prevent [[Siloed Engineering Trap — Tích Hợp Muộn = Tích Hợp Đau]]
> **Galaxy:** [[V-Model Macro-Micro — VDI 2206 Bọc VDI 2221 Cho Hệ Cơ Điện Tử]], [[Concern Logic — V-Model Là Trình Tự Logic Không Phải Timeline]], [[Three Strands — Orange Core + Yellow Requirements + Blue Modeling]]

## When to Use

- Product has ≥2 engineering domains (Mech+Elec, Mech+SW, or Mech+Elec+SW)
- After Phase 1 Task Clarification (Gate 1 passed)
- Before Phase 2 Conceptual Design begins
- **SKIP for:** pure mechanical products, variant designs of existing architecture, production-mature products

## When NOT to Use

- Single-domain products (e.g., purely mechanical towed target body)
- Variant/adaptive designs where architecture is KNOWN from parent product
- Products already in Phase 3+ (use `/helix-p3-integrate` for retroactive integration check instead)

## Standalone Usage
```
/helix-system-arch VN-XUONG-UUV
```

## Input Requirements

Read from `1_Projects/{{project}}/`:
- `Phase1-Task/Requirements_List_v1.md` — D/W requirements with domain tags
- `Phase1-Task/Function_Structure.md` — 6-flow function structure (from `/helix-p1-structure`)
- `Phase1-Task/Essential_Problem.md` — CEO-approved
- `_Project_Brief.md` — product tier, scope
- `Status.md` — current phase, Gate 1 status

## Output

All outputs to: `1_Projects/{{project}}/System-Arch/`

| File | Description |
|------|-------------|
| `SA_Mechatronic_Classification.md` | GO/SKIP decision with rationale |
| `SA_System_Architecture.md` | Block diagram + domain allocation + interface contracts |
| `SA_Domain_Budgets.md` | Weight/power/cost/latency budget per domain |
| `SA_VV_Plan.md` | Verification matrix: requirement × method × system level |
| `SA_Model_Inventory.md` | What models exist, what's needed, at what level |

---

## Workflow (6 Steps)

### Step SA0: Mechatronic Classification Gate

```
MECHATRONIC CLASSIFICATION — {{project_id}}
Date: {{today}}

Product: {{project_name}}
Tier: {{tier}}

DOMAIN SCAN (from Function Structure):
  Mechanical sub-functions:  {{count}} (list: ...)
  Electrical sub-functions:  {{count}} (list: ...)
  Software sub-functions:    {{count}} (list: ...)
  Other (hydraulic/optic):   {{count}} (list: ...)

CLASSIFICATION:
  □ Single-domain (pure mech) → SKIP system-arch, proceed to Phase 2
  □ Light mechatronic (1 dominant + 1 minor domain) → QUICK mode (SA2-SA3 only)
  □ Full mechatronic (2+ significant domains) → FULL system-arch (SA1-SA6)
  □ Cyber-physical (mechatronic + IoT/AI) → FULL + CPS extensions

DECISION: [SKIP / QUICK / FULL]
CEO: confirm classification before proceeding.
```

**STOP. Wait for CEO confirmation.**

---

### Step SA1: System Context Diagram (Black-Box)

Define the system boundary — what's INSIDE vs OUTSIDE:

```
SYSTEM CONTEXT — {{project_id}}

                    ┌─────────────────────┐
  Operator ────────▶│                     │──────▶ Target Effect
  Commands          │                     │
                    │   {{SYSTEM NAME}}   │
  Power ───────────▶│                     │──────▶ Status Data
  Supply            │   (Black Box)       │
                    │                     │──────▶ Waste Heat
  Environment ─────▶│                     │
  (sea state,       └─────────────────────┘
   weather, EMI)

EXTERNAL INTERFACES:
  | IF-ID | External Entity | Direction | Type | Notes |
  |-------|----------------|-----------|------|-------|
  | EX-01 | Operator       | IN        | Signal (commands) | |
  | EX-02 | Power supply   | IN        | Energy (AC/DC) | |
  | EX-03 | Target         | OUT       | Energy (kinetic/acoustic) | |
  | EX-04 | Control station| BIDI      | Data (telemetry) | |
  | ...   | ...            | ...       | ... | |

SYSTEM BOUNDARY DECISIONS:
  INSIDE: [what we design]
  OUTSIDE: [what we interface to but don't design]
  GREY ZONE: [items CEO must decide — e.g., power supply: buy or design?]
```

**Lightweight — NO SysML required.** Markdown table + ASCII diagram is sufficient for WX scale.

---

### Step SA2: System Architecture — Domain Allocation

Transform 6-flow function structure into domain-allocated architecture:

```
SYSTEM ARCHITECTURE — {{project_id}}
Date: {{today}}

┌─────────────────────────────────────────────────────────────┐
│                    SYSTEM LEVEL                              │
│  Overall Function: {{from Essential_Problem}}                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  MECH MODULE  │  │ ELEC MODULE  │  │  SW MODULE   │      │
│  │              │  │              │  │              │      │
│  │  SF-M1: ...  │  │  SF-E1: ...  │  │  SF-S1: ...  │      │
│  │  SF-M2: ...  │──│  SF-E2: ...  │──│  SF-S2: ...  │      │
│  │  SF-M3: ...  │  │  SF-E3: ...  │  │  SF-S3: ...  │      │
│  │              │  │              │  │              │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └────── INTERFACES (ICD v1) ────────┘               │
└─────────────────────────────────────────────────────────────┘
```

**DOMAIN ALLOCATION TABLE:**

```
| SF-ID | Sub-Function | Primary Domain | Secondary Domain | Rationale |
|-------|-------------|---------------|-----------------|-----------|
| SF-01 | {{name}}    | MECH          | —               | Structural |
| SF-02 | {{name}}    | ELEC          | SW              | Sensor + processing |
| SF-03 | {{name}}    | SW            | ELEC            | Algorithm + actuator |
| SF-04 | {{name}}    | SHARED        | MECH+ELEC       | Thermal management |
| ...   | ...         | ...           | ...             | ... |

ALLOCATION CONFLICTS:
  [List any sub-functions where domain allocation is ambiguous]
  CEO: resolve allocation conflicts before SA3.
```

**Key decisions (CEO Core — non-delegable):**
- Which functions are SHARED between domains? (highest integration risk)
- Which domain LEADS for shared functions?
- Any functions that could be ACH-shifted? (link to `/forge-shift`)

**STOP. Wait for CEO approval of architecture.**

---

### Step SA3: Interface Contract Definition (ICD v1)

For EACH interface between domain modules, define the contract:

```
INTERFACE CONTROL DOCUMENT v1 — {{project_id}}
Date: {{today}}

| IF-ID | From | To | Type | Specification | Constraint | Priority |
|-------|------|----|------|--------------|-----------|----------|
| IF-01 | MECH | ELEC | Physical | Mounting holes: M4 × 4, 80mm PCD | ±0.5mm | DEMAND |
| IF-02 | ELEC | SW | Signal | UART 115200 baud, 3.3V logic | <10ms latency | DEMAND |
| IF-03 | SW | ELEC | Command | PWM 50Hz, 1-2ms pulse | Failsafe: 1.5ms center | DEMAND |
| IF-04 | MECH | ELEC | Thermal | Max 15W dissipation, passive cooling | Ambient: 50°C max | WISH |
| IF-05 | SW | MECH | Data | Position feedback: encoder 1024 PPR | Update: 100Hz min | DEMAND |
| ...   | ...  | ... | ...  | ...          | ...       | ... |

CRITICAL INTERFACES (highest integration risk):
  1. IF-{{XX}}: {{why it's critical — e.g., timing, thermal, spatial}}
  2. IF-{{XX}}: {{why}}

UNRESOLVED INTERFACES:
  [List interfaces where specification is TBD]
  [Each must be resolved before Phase 2 concept search]
```

**ICD v1 Rules:**
- D (DEMAND) interfaces = hard constraints for Phase 2 concept search
- W (WISH) interfaces = soft constraints, can be traded off
- Every interface MUST have an owner (which domain is responsible for compliance?)
- Unresolved interfaces → blocking items for Gate SA

---

### Step SA4: Domain Budget Allocation

Split system-level requirements into domain budgets:

```
DOMAIN BUDGETS — {{project_id}}
Date: {{today}}

WEIGHT BUDGET:
  System total target: {{X}} kg (from Req R-{{nn}})
  | Domain | Allocation | Margin | Items |
  |--------|-----------|--------|-------|
  | MECH   | {{X}} kg  | {{Y}}% | Structure, housing, actuators |
  | ELEC   | {{X}} kg  | {{Y}}% | PCBs, cables, connectors, batteries |
  | SW     | 0 kg      | —      | N/A (software has no weight) |
  | TOTAL  | {{X}} kg  | {{Y}}% | |

POWER BUDGET:
  System total available: {{X}} W (from Req R-{{nn}})
  | Domain | Allocation | Peak | Duty Cycle | Items |
  |--------|-----------|------|-----------|-------|
  | MECH   | {{X}} W   | {{Y}} W | {{Z}}% | Motors, actuators |
  | ELEC   | {{X}} W   | {{Y}} W | {{Z}}% | MCU, sensors, comms |
  | SW     | (included in ELEC computation budget) | | |
  | MARGIN | {{X}} W   | | | Reserve for growth |

COST BUDGET:
  System BOM target: {{X}} USD (from Req R-{{nn}} or _Project_Brief)
  | Domain | Allocation | Confidence | Notes |
  |--------|-----------|-----------|-------|
  | MECH   | ${{X}}    | [H/M/L]  | |
  | ELEC   | ${{X}}    | [H/M/L]  | |
  | SW     | ${{X}}    | [H/M/L]  | Dev cost, not per-unit |
  | TOTAL  | ${{X}}    | | |

LATENCY BUDGET (for real-time systems):
  System response requirement: {{X}} ms (from Req R-{{nn}})
  | Stage | Domain | Allocation | Notes |
  |-------|--------|-----------|-------|
  | Sense | ELEC   | {{X}} ms  | Sensor sampling + ADC |
  | Process | SW   | {{X}} ms  | Algorithm + decision |
  | Actuate | ELEC+MECH | {{X}} ms | Driver + mechanical response |
  | TOTAL | | {{X}} ms | Must be < requirement |

BUDGET CONFLICTS:
  [List any budget where total exceeds requirement]
  [These become DESIGN DRIVERS for Phase 2]
```

**CEO: review budgets. Any domain over-allocated? Identify 2-3 budget-critical items that will DRIVE concept selection in Phase 2.**

---

### Step SA5: Verification & Validation Plan (VDI 2206 V&V)

Plan HOW each cross-domain requirement will be verified/validated:

```
V&V PLAN — {{project_id}}
Date: {{today}}

VERIFICATION MATRIX (Did we build the system RIGHT?):
  | Req-ID | Requirement | Level | Method | When | Domain Owner |
  |--------|------------|-------|--------|------|-------------|
  | R-01   | {{text}}   | System | Test (HiL) | Phase 3 | ELEC |
  | R-02   | {{text}}   | Module | Analysis (FEM) | Phase 3 | MECH |
  | R-03   | {{text}}   | Module | Inspection | Phase 4 | MECH |
  | R-04   | {{text}}   | System | Test (field) | Phase 4 | ALL |
  | ...    | ...        | ...   | ...    | ...  | ... |

  Methods: Analysis | Inspection | Demonstration | Test
  Levels: Component | Module | Subsystem | System

VALIDATION PLAN (Did we build the RIGHT system?):
  | Stakeholder Need | Validation Method | When | Pass Criteria |
  |-----------------|-------------------|------|--------------|
  | {{need}}         | Field trial       | Post-Phase 4 | {{criteria}} |
  | {{need}}         | User acceptance   | Phase 3 prototype | {{criteria}} |

PHYSICAL PROTOTYPE PLAN (link to dP/dt):
  | Prototype | Purpose | Domains Tested | Target Date |
  |-----------|---------|---------------|-------------|
  | P1: Bench model | IF-01 to IF-03 integration | MECH+ELEC | {{date}} |
  | P2: Functional | Full system V&V | ALL | {{date}} |
```

**Analyst Trap Guard:** Every V&V entry that says "Analysis" or "Simulation" MUST have a corresponding physical test at a later phase. Models predict; hardware validates.

---

### Step SA6: Architecture Review Gate (CEO Core)

```
═══ SYSTEM ARCHITECTURE REVIEW — {{project_id}} ═══
Date: {{today}}

DELIVERABLES CHECK:
  □ SA_Mechatronic_Classification.md — classification confirmed
  □ SA_System_Architecture.md — block diagram + domain allocation
  □ SA_Domain_Budgets.md — weight/power/cost/latency split
  □ SA_VV_Plan.md — verification matrix complete
  □ SA_Model_Inventory.md — current model state documented
  □ ICD v1 — all critical interfaces specified

ARCHITECTURE QUALITY:
  □ Every sub-function allocated to exactly 1 primary domain
  □ All SHARED functions have a designated lead domain
  □ No unresolved interfaces remain (or explicitly deferred with risk accepted)
  □ Budget totals ≤ requirement targets (or trade-offs documented)
  □ ≥1 physical prototype planned within 30 days

RISK SUMMARY:
  | Risk | Impact | Mitigation |
  |------|--------|-----------|
  | {{risk}} | {{H/M/L}} | {{action}} |

CEO DECISION:
  □ APPROVE — proceed to Phase 2 Conceptual Design with this architecture
  □ ITERATE — specific issues to resolve: [list]
  □ REJECT — fundamental architecture problem: [describe]

═══════════════════════════════════════════════
```

**STOP. CEO approval is MANDATORY before Phase 2 concept search begins.**

---

## QUICK Mode (Light Mechatronic)

For products with 1 dominant + 1 minor domain (e.g., VN-AST-MSL-001: mech dominant, light elec):

```
/helix-system-arch VN-AST-MSL-001 --quick
```

Quick mode runs only:
- SA0: Classification (→ QUICK)
- SA2: Simplified domain allocation (table only, no block diagram)
- SA3: ICD v1 for cross-domain interfaces only
- SA6: Quick review

Skip: SA1 (context diagram), SA4 (budgets), SA5 (V&V plan — use standard Phase 3 approach)

---

## Retroactive Mode

For products already past Phase 1 that never had system architecture:

```
/helix-system-arch VN-XUONG-UUV --retro
```

Retroactive mode:
1. Reads existing Phase 2/3 deliverables to reconstruct implicit architecture
2. Documents AS-IS architecture (what was assumed)
3. Identifies GAPS: interfaces never specified, budgets never split
4. Produces ICD v1.5 (not v1 — acknowledges some decisions already made)
5. Flags shadow assumptions that need verification

**Use case:** VN-XUONG-UUV is in Phase 2 without formal system architecture. Run `--retro` to establish baseline before continuing.

---

## Integration with Existing HELIX Skills

### Upstream: Phase 1 Compile (BE) Routing

After Gate 1 passes, `/helix-p1-compile` should recommend:

```
GATE 1 ROUTING:
  Mechatronic classification: [YES/NO]
  If YES: "Run /helix-system-arch {{project}} before Phase 2"
  If NO: "Proceed directly to /helix-concept-generate {{project}}"
```

### Downstream: Phase 2 Preflight (B0) Verification

`/helix-p2-preflight` adds check:

```
□ SA_System_Architecture.md exists (if mechatronic product)
□ ICD v1 exists with all critical interfaces specified
□ Domain budgets defined
□ OR: product classified as single-domain (system-arch skipped with reason)
```

### Continuous: Phase 3 Integration (BC) Mode Change

`/helix-p3-integrate` shifts from DISCOVERY to VERIFICATION:

```
INTEGRATION MODE: [DISCOVERY / VERIFICATION]

If SA_System_Architecture.md exists:
  MODE = VERIFICATION
  → Compare actual integration against ICD v1 contracts
  → Flag any deviations from domain budgets
  → Verify shadow assumptions from SA phase

If NO system architecture:
  MODE = DISCOVERY (legacy — current behavior)
  → Discover interfaces for the first time (risky, late)
  → ⚠️ Warn: "No system architecture — integration risks elevated"
```

---

## COD Classification

| Task | COD | Notes |
|------|-----|-------|
| SA0: Mechatronic classification | O | AI proposes, CEO confirms |
| SA1: System context diagram | O | AI drafts from requirements |
| SA2: Domain allocation | **C** | CEO decides which domain leads shared functions |
| SA3: Interface specification | O/C | AI drafts, CEO validates critical interfaces |
| SA4: Budget allocation | **C** | CEO decides trade-offs between domains |
| SA5: V&V plan | O | AI generates matrix, CEO adds field knowledge |
| SA6: Architecture review | **C** | CEO MUST approve architecture |

---

## Cross-Domain Risk Map (extends SA3 / SA5)

For each domain pair, classify interface readiness:

|              | Mech     | Elec     | SW/AI    | External |
|--------------|----------|----------|----------|----------|
| **Mech**     | —        | G/Y/R    | G/Y/R    | G/Y/R    |
| **Elec**     |          | —        | G/Y/R    | G/Y/R    |
| **SW/AI**    |          |          | —        | G/Y/R    |
| **External** |          |          |          | —        |

- **G** = All interfaces defined, no TBDs
- **Y** = Interfaces defined, minor TBDs remain
- **R** = TBDs or conflicts blocking integration

Any **R** = blocks Gate 2/3. Hand off debt items to `/helix-integration-debt` for tracking + resolution scheduling.

## Anti-Patterns (What NOT to Do)

1. **Don't buy SysML tools.** Block diagrams in markdown/draw.io are sufficient for WX scale. See [[MBSE-CAx Gap — SysML Không Mô Tả Được Hình Học Giải Pháp Cơ Khí]]
2. **Don't over-specify interfaces.** ICD v1 = critical interfaces only. Details come in Phase 3 (ICD v2→v3)
3. **Don't freeze architecture permanently.** V-Model concern logic allows iteration — if Phase 2 reveals architecture doesn't work, loop back to SA2
4. **Don't run this for pure mechanical products.** SA0 classification gate prevents waste
5. **Don't skip physical prototype planning (SA5).** Analysis ≠ validation. See [[Physical-World Interface — Kiểm Chứng Bằng Thực Tế]]

## References

- VDI/VDE 2206:2021 "Development of mechatronic and cyber-physical systems" — System Design process module
- Graessler & Hentze 2020 "The new V-Model of VDI 2206 and its validation"
- Eigner & Dickopf 2017 "The Evolution of the V-Model: From VDI 2206 to Cybertronic Systems"
- Cambridge 2022 "Integrating model-based design with domain-specific approaches"
- Pahl & Beitz Ch6.3 (Function Structure) — feeds directly into SA2
