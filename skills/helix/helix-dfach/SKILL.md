---
name: helix-dfach
description: ACH-specific Design-for-X checklist — covers commodity hardware selection, AI compensation path, sensor-to-data pipeline, edge inference constraints, and model update lifecycle. This skill should be used when the user asks about "DfACH", "design for ACH", "ACH checklist", "AI hardware design", "thiet ke cho ACH", "commodity hardware + AI", or needs to verify that a product correctly applies the ACH (AI-Compensates-Hardware) principle in its physical design.
---

# Helix DfACH — Design for AI-Compensates-Hardware

ACH products use deliberately simple/commodity hardware compensated by AI software. This DfX checklist ensures the physical design actually supports the ACH principle — not just bolting AI onto a conventional design.

## When to Use

- During Phase 3 Embodiment Design for any ACH product (after forge-shift GO)
- When helix-embody-realize runs DfX review — DfACH is the ACH-specific extension
- Before Gate 3 for any product flagged as ACH in FORGE portfolio
- When user asks "is our hardware actually ACH-compatible?"

## The ACH Design Principle

```
CONVENTIONAL:  Expensive precision hardware → accurate results
ACH:           Commodity hardware + AI compensation → equivalent or better results
                at lower cost, with software-upgradable performance

KEY INSIGHT: The hardware must be DESIGNED for AI compensation.
             You can't just add AI to any hardware and call it ACH.
```

## DfACH Checklist

### Section A: Commodity Hardware Selection

```
DfACH-A — HARDWARE COMMODITY CHECK
Purpose: Verify hardware is truly commodity (available, replaceable, cost-effective)

| Item | Check | Status | Notes |
|------|-------|--------|-------|
| A-01 | Primary sensor is COTS (commercial off-the-shelf)? | [OK/WARN/FAIL] | |
| A-02 | Sensor available from ≥ 2 Vietnam-accessible suppliers? | [OK/WARN/FAIL] | |
| A-03 | Hardware precision is intentionally LOWER than spec requires? | [OK/WARN/FAIL] | |
|      | (AI compensates the gap — this is the ACH value proposition) | | |
| A-04 | Replacement hardware same form factor (swap without redesign)? | [OK/WARN/FAIL] | |
| A-05 | Total hardware cost < 60% of equivalent precision system? | [OK/WARN/FAIL] | |
| A-06 | No single custom-fabricated sensor in critical path? | [OK/WARN/FAIL] | |

If A-03 = FAIL → this is NOT an ACH product. It's conventional design with AI added.
```

### Section B: AI Compensation Path

```
DfACH-B — AI COMPENSATION ARCHITECTURE
Purpose: Verify AI has a viable path to compensate for hardware limitations

| Item | Check | Status | Notes |
|------|-------|--------|-------|
| B-01 | Hardware limitation clearly defined (what AI compensates for)? | [OK/WARN/FAIL] | |
|      | Example: "Camera resolution 720p → AI upscales to detect at 2km" | | |
| B-02 | AI compensation path validated in simulation/lab? | [OK/WARN/FAIL] | |
| B-03 | Fallback exists if AI compensation fails (forge-fallback output)? | [OK/WARN/FAIL] | |
| B-04 | Performance envelope documented (where AI can/cannot compensate)? | [OK/WARN/FAIL] | |
|      | Example: "Compensates up to 50% occlusion, fails at >70%" | | |
| B-05 | Training data representative of operational conditions? | [OK/WARN/FAIL] | |
| B-06 | AI model validated on actual hardware sensor output (not synthetic)? | [OK/WARN/FAIL] | |
```

### Section C: Sensor-to-Data Pipeline

```
DfACH-C — DATA PIPELINE DESIGN
Purpose: Verify physical design supports data flow from sensor to AI to output

| Item | Check | Status | Notes |
|------|-------|--------|-------|
| C-01 | Sensor mounting provides consistent, repeatable data quality? | [OK/WARN/FAIL] | |
|      | (vibration isolation, thermal stability, alignment tolerance) | | |
| C-02 | Data bus bandwidth sufficient for raw sensor data? | [OK/WARN/FAIL] | |
| C-03 | Preprocessing hardware (ADC, FPGA) matched to AI input requirements? | [OK/WARN/FAIL] | |
| C-04 | Data timestamp accuracy sufficient for fusion (if multi-sensor)? | [OK/WARN/FAIL] | |
| C-05 | Field data collection port for training data capture? | [OK/WARN/FAIL] | |
|      | (DfU-08 from embody-realize — cross-reference) | | |
| C-06 | Data pipeline latency end-to-end within operational requirement? | [OK/WARN/FAIL] | |
```

### Section D: Edge Inference Constraints

```
DfACH-D — COMPUTE PLATFORM DESIGN
Purpose: Verify physical design supports AI inference within power/thermal/size envelope

| Item | Check | Status | Notes |
|------|-------|--------|-------|
| D-01 | Compute platform selected (e.g., Jetson, RPi CM4, custom SBC)? | [OK/WARN/FAIL] | |
| D-02 | Power budget allocated for compute (separate from sensor/comms)? | [OK/WARN/FAIL] | |
| D-03 | Thermal design handles worst-case compute load? | [OK/WARN/FAIL] | |
|      | (MIL-STD-810 +55°C ambient + full inference load) | | |
| D-04 | Inference time < operational response requirement? | [OK/WARN/FAIL] | |
| D-05 | Compute module physically accessible for upgrade (DfU-03)? | [OK/WARN/FAIL] | |
| D-06 | Computational headroom ≥ 30% for future model growth (DfU-07)? | [OK/WARN/FAIL] | |
| D-07 | AI dependency stack (framework, CUDA, OS) documented (DfU-10)? | [OK/WARN/FAIL] | |
```

### Section E: Model Update Lifecycle

```
DfACH-E — CONTINUOUS IMPROVEMENT DESIGN
Purpose: ACH products improve over time — verify design supports this

| Item | Check | Status | Notes |
|------|-------|--------|-------|
| E-01 | OTA update mechanism designed and tested (DfU-05)? | [OK/WARN/FAIL] | |
| E-02 | Model rollback mechanism in place (DfU-06)? | [OK/WARN/FAIL] | |
| E-03 | Field monitoring endpoint active (DfU-09)? | [OK/WARN/FAIL] | |
| E-04 | Retraining pipeline designed (data → label → train → validate → deploy)? | [OK/WARN/FAIL] | |
| E-05 | Version control for deployed models (track which model on which unit)? | [OK/WARN/FAIL] | |
| E-06 | Performance regression detection (model update didn't make things worse)? | [OK/WARN/FAIL] | |
```

### Section F: P05 Physics Plausibility on ACH Compensation Claims

After completing Sections A-E, run P05 (from S1 Prompt Library) on the AI compensation path:

```
P05 PHYSICS CHECK ON ACH COMPENSATION — {{project_id}}

INPUT: DfACH Section B answers (B-01 to B-06)

CHECK 1: UNIT CONSISTENCY
  AI compensation claim uses correct units throughout?
  Example: "upscale 720p to detect at 2km" → verify pixel pitch × focal length → angular resolution

CHECK 2: ORDER OF MAGNITUDE
  Is the claimed compensation physically plausible for this sensor class?
  Example: "compensate 50% occlusion" — is there enough signal remaining?

CHECK 3: BOUNDARY CONDITIONS
  At worst-case operational conditions (MIL-STD-810 extremes), does compensation still work?
  Example: "works at 25°C" but what about 55°C + dust + vibration?

CHECK 4: ENERGY/INFORMATION CONSERVATION
  AI cannot create information that doesn't exist in sensor data.
  Example: "enhance beyond diffraction limit" = physically impossible

CHECK 5: ENVIRONMENTAL ADJUSTMENT
  Vietnam-specific: tropical heat, humidity, salt air, monsoon rain
  Does the compensation degrade gracefully or fail catastrophically?

VERDICT:
  ALL PASS → ACH compensation claim is physically defensible
  ANY FAIL → Compensation claim overstated. Revise B-01/B-04 before proceeding.
  UNCERTAIN on safety-critical → treat as FAIL per P05 rules
```

## Summary and Scoring

```
DfACH SUMMARY — {{project_id}}
Date: {{today}}

| Section | Items | OK | WARN | FAIL |
|---------|-------|----|------|------|
| A — Commodity Hardware | 6 | __ | __ | __ |
| B — AI Compensation | 6 | __ | __ | __ |
| C — Data Pipeline | 6 | __ | __ | __ |
| D — Edge Inference | 7 | __ | __ | __ |
| E — Update Lifecycle | 6 | __ | __ | __ |
| TOTAL | 31 | __ | __ | __ |

ACH READINESS SCORE: __/31 OK items

BANDS:
  25-31 OK: ACH-READY — proceed to Gate 3
  18-24 OK: ACH-PARTIAL — address WARN/FAIL items before gate
  <18 OK: ACH-NOT-READY — fundamental design issues, return to Phase 2/3

CRITICAL FAILS (any of these = BLOCK):
  A-03 FAIL → Not actually ACH (hardware is precision, not commodity)
  B-03 FAIL → No fallback (safety risk)
  D-03 FAIL → Thermal crisis (hardware failure risk)
  E-02 FAIL → No rollback (field bricking risk)
```

## Integration

```
helix-dfach READS FROM:
  - forge-shift → ACH go/no-go decision, compensation path defined
  - forge-fallback → fallback architecture (B-03 cross-reference)
  - helix-embody-realize → DfU items (D-05 to E-03 cross-reference)
  - forge-validate → performance envelope data (B-04)

helix-dfach WRITES TO:
  - helix-quality-gate → DfACH score feeds Gate 3 auto-check
  - helix-embody-realize → DfACH FAIL items → DfX issues to resolve
  - forge-library → commodity hardware specs cataloged for reuse
  - bridge-risk-radar → ACH-specific risks identified
```

## Rules

- DfACH is MANDATORY for any product flagged ACH in FORGE portfolio
- Non-ACH products skip this checklist entirely
- A-03 is the ACH litmus test — if hardware is already precision, there's no ACH value
- Cross-reference DfU items from embody-realize — don't duplicate, link
- B-06 is often the most delayed item (needs real hardware for testing)
- Solo CEO context: DfACH forces systematic check that "ACH" isn't just a label

## COD Classification

- Running checklist against design artifacts: Offload (O2) — AI evaluates
- Cross-referencing DfU and FORGE outputs: Offload (O1) — AI links data
- Scoring and band calculation: Offload (O1) — deterministic
- Hardware commodity assessment: **Core (C)** — requires market knowledge
- AI compensation path validation: **Core (C)** — requires domain expertise
- Fallback adequacy judgment: **Core (C)** — safety-critical decision
