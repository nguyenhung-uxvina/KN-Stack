---
name: helix-p3-integrate
description: "Block C of Phase 3 pipeline — cross-domain integration check (Mech×Elec×AI), ICD v2→v3 freeze, thermal/EMC analysis, shadow assumption validation, design principle compliance. P&B 7.4 + WX extensions. Can run standalone. Triggers on: 'integration check', 'ICD freeze', 'ICD v3', 'thermal analysis', 'shadow assumptions', 'cross-domain'."
---

# Block C: Integration — ICD v3 Freeze + Cross-Domain Verification

> **P&B:** 7.4 (Principles applied to integration) + WX extensions | **Pipeline:** helix-embody-realize → Block BC
> **Input:** `BB_DfX_Review.md`, `BA_Preliminary_Layout.md`, ICD v2 | **Output:** `BC_Integration_Check.md`, `BC_ICD_v3.md`, `BC_Shadow_Assumptions.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Verify cross-domain interfaces (Mech x Elec x AI) | Redesign layout (= flag to BA for revision) |
| Freeze ICD v2 → v3 (with CEO approval) | Generate BOM (= BD) |
| Run thermal/EMC analysis | Evaluate embodiment quality Rt/Re (= BE) |
| Validate shadow assumptions across domains | Freeze ICD without explicit CEO approval |
| Log requirements deltas from integration findings | Skip shadow assumption check |

**Multi-Agent Mode:** NO — integration check is a verification task. Domain-debate already ran in Phase 2 BD; this block verifies those assumptions held through embodiment.
**CEO Checkpoint:** ICD v3 freeze = Core decision. CEO approves frozen interfaces — commitment with downstream consequences.

## Workflow

### Step C0: Integration Mode Detection (VDI 2206)

```
INTEGRATION MODE — {{project_id}}

Check: Does System-Arch/ folder exist?
  □ YES → MODE = VERIFICATION
    SA_System_Architecture.md found → verify against ICD v1 contracts
    SA_Domain_Budgets.md found → check actual vs allocated budgets
    "Integration is VERIFICATION of existing architecture, not first-time discovery."
  □ NO → MODE = DISCOVERY (legacy)
    "⚠️ No system architecture — discovering interfaces for the first time."
    "Integration risks elevated. Consider running /helix-system-arch --retro"

MODE: [VERIFICATION / DISCOVERY]
```

If VERIFICATION mode: Step C1 compares actual embodiment against SA contracts.
If DISCOVERY mode: Step C1 runs as original (discover interfaces from scratch).

### Step C1: Cross-Domain Interface Verification

```
INTEGRATION CHECK — {{project}}
Date: {{today}}

| IF-ID | Interface | Physical Clearance | Signal Integrity | Power Budget | Thermal | Status |
|-------|-----------|-------------------|-----------------|-------------|---------|--------|

THERMAL CHECK:
  Heat sources: [component + watts]
  Dissipation: [path description]
  Margin: [adequate/marginal/insufficient]
  Worst-case ambient: {{temp}}°C

EMC PRELIMINARY:
  Sensitive signals near power: [Y/N — flag if Y]
  Shielding planned: [Y/N]
  Grounding scheme: [single-point / multi-point / hybrid]
```

For single-domain (pure mechanical): "Integration: single-domain — verify mechanical interfaces only."

### Step C2: Shadow Assumption Validation (P55)

```
SHADOW ASSUMPTIONS — {{project}}

| SA-ID | Domain Making | About Domain | Assumption | Verified? | If Wrong |
|-------|-------------|-------------|-----------|----------|---------|

Unverified SA at ICD freeze = hidden integration debt → D-xxx in Phase 4.
```

### Step C3: ICD v2 → v3 Freeze

```
ICD v3 FREEZE REVIEW — {{project}}

| IF-ID | v2 Spec | v3 Change | Justification | CEO Approved? |
|-------|---------|----------|--------------|--------------|

ICD v3 FREEZE CHECKLIST (P&B):
□ All interface signals defined (type, range, protocol)
□ Mechanical interfaces dimensioned (tolerances specified)
□ Power budgets balanced (supply ≥ demand + margin)
□ Thermal analysis complete (worst-case ambient)
□ EMC zones identified
□ Software API contracts frozen (if applicable)
□ Shadow assumptions all verified OR explicitly accepted as risks
□ Geometry-of-record registered for every fabricable part (see Geometry Interface table below)

STATUS: [FROZEN / PENDING — {{items remaining}}]
```

### Step C3a: Geometry-of-Record Registry (ICD geometry interface)
> The ICD freezes not only signal/mechanical-tolerance interfaces but the **geometry interface** — the authoritative shape of each fabricable part. This is the receiving slot the CAD trio writes into: [[helix-cad-bridge]] registers a STEP, [[helix-cad-ingest]] registers a `cad_extract.json`, and [[helix-cad-roundtrip]] threads either one here. Both forms occupy the **same per-part slot** — geometry-of-record.

```
GEOMETRY-OF-RECORD — {{project}} (frozen at ICD v3)

| Part ID | Source type | Artifact | Rev | CEO-certified? | Spatial-Blindness gate |
|---------|-------------|----------|-----|----------------|------------------------|
|         | STEP (cad-bridge) / cad_extract.json (cad-ingest, incl. human-drawn import) | path | r{{n}} | [Y/N] | [render-verified / dim-certified] |

Rules:
- Every part on the BOM tree MUST have a geometry-of-record row before ICD v3 freezes.
- CEO-certified = bridge Step 5 render-verify OR ingest Step 6 / roundtrip D4-D5 reconcile.
  An UNCERTIFIED geometry-of-record blocks the freeze (AI never self-certifies — [[LLM Spatial Blindness]]).
- Rev-locked: a part re-issued (STEP→drawing, or design change) bumps its rev here.
- A part whose geometry is deferred to Phase 4 = [LATE], explicitly listed, not silently absent.
```

**Rule:** ICD v3 freeze requires EXPLICIT CEO approval — no silent freeze. Geometry-of-record completeness (every fabricable part has a CEO-certified row) is part of that approval.

### Step CX: Requirements Backflow at Integration (VDI 2221:2019)

ICD v3 freeze often reveals new interface requirements or changes to existing requirements. Check:

```
REQUIREMENTS BACKFLOW — Block BC (Integration)
Date: {{today}}

□ New interface requirements discovered during ICD v3 development?
□ Existing requirements conflicting with frozen interfaces?
□ Domain budget overruns requiring requirement relaxation?
□ Shadow assumption validation revealing unstated requirements?

If YES → append to {{prefix}}Requirements_Delta_Log.md
→ Flag at CEO checkpoint: "⚠️ Integration revealed N requirement changes"
```

### Step C3b: MBSE-CAx Gap Warning (VDI 2206 FM-4)

> **VDI 2206 Research Finding:** "SysML cannot efficiently capture geometric information needed for mechanical solution principles." The gap between system-level MBSE and domain-specific CAD remains an OPEN PROBLEM (Cambridge 2022, Tier A). See [[MBSE-CAx Gap — SysML Không Mô Tả Được Hình Học Giải Pháp Cơ Khí]].

For mechatronic products (SA_System_Architecture.md exists):
```
MBSE-CAx GAP CHECK — {{project_id}}
Date: {{today}}

□ System architecture (SA) defines interfaces in FUNCTIONAL terms
□ Embodiment layout (BA) realizes interfaces in PHYSICAL terms
□ Any SA interface specification that CANNOT be verified in CAD?
  If YES → list: [IF-ID, functional spec, why CAD can't capture it]
  → These interfaces need PHYSICAL PROTOTYPE verification (not just model)

□ Any domain using different modeling tools with no data bridge?
  MECH: [CAD tool] ↔ ELEC: [ECAD tool] ↔ SW: [IDE]
  Data exchange: [manual / automated / none]
  If "none" or "manual" → integration risk elevated, flag for CEO
```

### Step C4: Cross-Domain Sync S5

```
SYNC S5 — {{project}}

FIRST HARDWARE AVAILABLE FOR AI TESTING:
  Date: [target]
  What: [test coupon / dev board / partial assembly]
  AI test plan: [what needs to validate on hardware]

DOMAIN ALIGNMENT:
  Mech: [status / key decision]
  Elec: [status / key decision]
  AI/SW: [status / key decision]
```

## Output
Save to `1_Projects/{{project}}/Phase3-Embodiment/`:
- `BC_Integration_Check.md`
- `BC_ICD_v3.md` (includes the Geometry-of-Record registry — Step C3a)
- `BC_Shadow_Assumptions.md`

## CEO Checkpoint
```
═══ BLOCK BC INTEGRATION COMPLETE ═══
Interfaces: {{N}} verified, {{M}} issues found
Shadow assumptions: {{N}} total, {{K}} unverified
ICD v3: [FROZEN / PENDING {{items}}]
Thermal: [OK / MARGINAL / INSUFFICIENT]

CEO:
(1) ✅ Approve ICD v3 freeze → tiếp tục Block BD (BOM)
(2) 🔄 Fix interface issues first
(3) ⚠️ Accept unverified assumptions as risks
(4) ⏸️ Dừng — ICD not ready to freeze
```

## COD
- Interface verification: Offload (O2)
- Shadow assumption extraction: Offload (O2)
- Geometry-of-record registry compilation (collect STEP/cad_extract rows): Offload (O2)
- **ICD v3 freeze approval: Core (C)** — commitment with consequences
- **Unverified assumption acceptance: Core (C)** — risk decision
- **Geometry-of-record CEO certification (per part): Core (C)** — [[LLM Spatial Blindness]] gate, blocks freeze if any part uncertified
