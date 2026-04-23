---
name: triz-sufield-76solutions
description: TRIZ Su-Field Analysis + 76 Standard Solutions for improving selected concepts after VDI 2225 evaluation
---

# TRIZ Su-Field Analysis — Solution Improver Reference

## What is Su-Field?

Su-Field (Substance-Field) analysis models interactions between:
- **S1:** Object being acted upon (e.g., target in simulator, trainee's muscle memory)
- **S2:** Tool/agent acting (e.g., recoil system, scoring algorithm)
- **F:** Field enabling interaction (e.g., mechanical, electromagnetic, thermal, informational)

## Su-Field Model Types

| Model | Notation | Meaning | Action |
|-------|----------|---------|--------|
| Complete | S2 →F→ S1 | System works (useful action) | Optimize |
| Incomplete | S2 →?→ S1 | Missing or weak field | Complete the su-field |
| Harmful | S2 →F→ S1 (×) | Harmful side effect exists | Eliminate harmful action |
| Insufficient | S2 →F(↓)→ S1 | Action too weak | Strengthen or replace field |
| Excessive | S2 →F(↑)→ S1 | Action too strong/uncontrollable | Add control element |

## 76 Standard Solutions (5 Classes)

### Class 1: Building/Destroying Su-Fields (13 solutions)

| # | Solution | When to Use | WX Example |
|---|----------|-------------|------------|
| 1.1.1 | Complete incomplete su-field: add S2 + F | Missing interaction | Add sensor (S2) + signal (F) to detect hit |
| 1.1.2 | Add internal additive to S1 or S2 | Improve existing interaction | Masselotte inside piston (local mass) |
| 1.1.3 | Add external additive | Can't modify S1 or S2 | External compressor for pneumatic recoil |
| 1.1.4 | Use environment as additive | Resource from surroundings | Use ambient temperature for calibration |
| 1.2.1 | Introduce S3 between S1 and S2 | Eliminate harmful action | Vibration isolator between mount and frame |
| 1.2.2 | Add modified S1' or S2' | Neutralize harmful field | Backing plate absorbs excess force |
| 1.2.3 | Introduce compensating F2 | Counter harmful field | Damper counters recoil overshoot |
| 1.2.4 | Use F to eliminate harmful F | Use field against itself | Anti-vibration mount |
| 1.2.5 | Disconnect S1 from harmful F | Shield/isolate | Sealed electronics from salt spray |

### Class 2: Developing Su-Fields (23 solutions)

| # | Solution | When to Use |
|---|----------|-------------|
| 2.1.1 | Replace uncontrolled F with controllable F | Need precision control |
| 2.1.2 | Add second S2 to improve controllability | One actuator insufficient |
| 2.2.1 | Segment S2 to increase controllability | Coarse control → fine control |
| 2.2.2 | Make F non-uniform (e.g., gradient) | Need varying effect |
| 2.3.1 | Use resonance to amplify effect | Insufficient force/signal |
| 2.3.2 | Match F frequency to natural frequency of S1 | Efficiency improvement |
| 2.4.1 | Use ferromagnetic substance + magnetic field | Need controllable mechanical action |
| 2.4.2-12 | Various electromagnetic and thermal approaches | Domain-specific |

### Class 3: System Transitions (6 solutions)

| # | Solution | When to Use |
|---|----------|-------------|
| 3.1.1 | Transition to bi-system | Single system insufficient |
| 3.1.2 | Transition to poly-system | Multiple identical needed |
| 3.1.3 | Transition from macro to micro level | Miniaturize |
| 3.2.1 | Combine with anti-system | Need opposite action too |
| 3.2.2 | Combine macro + micro in same system | Different scales needed |
| 3.2.3 | Use phase transition of substance | Temperature-dependent behavior |

### Class 4: Detection and Measurement (6 solutions)

| # | Solution | When to Use |
|---|----------|-------------|
| 4.1.1 | Replace direct measurement with indirect | Can't measure directly |
| 4.1.2 | Add detectable additive to S1 | Need to track/sense |
| 4.1.3 | Use copy instead of original for measurement | Original too expensive/dangerous |
| 4.2.1 | Use resonance for detection | Need high sensitivity |
| 4.3.1 | Use successive detection | Single measurement insufficient |
| 4.5.1 | Change direction of measurement | Improve accuracy |

### Class 5: Helpers — Standards for Applying Standards (17 solutions)

| # | Solution | When to Use |
|---|----------|-------------|
| 5.1.1 | Introduce substance under void condition | Can't add substance |
| 5.1.2 | Use field instead of substance | Substance undesirable |
| 5.1.3 | Use external additive temporarily | Permanent change unwanted |
| 5.1.4 | Use very small amount of very active additive | Cost/weight constraint |
| 5.2.1-4 | Field derivatives (gradient, pulsed, combined) | Standard field insufficient |
| 5.3.1-5 | Phase transition applications | Need reversible changes |
| 5.4.1-2 | Use phenomena (self-organization, etc.) | Advanced effects |
| 5.5.1-3 | Obtain substances/fields by decomposition | Use what you have |

## Decision Flowchart — Which Class to Use

```
Problem identified (VDI 2225 score < 5/10)
    │
    ├── Missing interaction? ──────────→ Class 1.1 (Build su-field)
    │
    ├── Harmful side effect? ──────────→ Class 1.2 (Destroy harmful action)
    │
    ├── Action too weak? ──────────────→ Class 2 (Develop su-field)
    │
    ├── Single system at limit? ───────→ Class 3 (System transition)
    │
    ├── Can't detect/measure? ─────────→ Class 4 (Detection)
    │
    └── Can't add substance/field? ────→ Class 5 (Helpers)
```

## Workshop X Application Pattern

When helix-concept-generate Step 4 (VDI 2225) reveals a weak criterion (< 5/10):

1. **Identify** the sub-function causing the low score
2. **Model** as su-field:
   - S1 = what is being acted upon (trainee, target, projectile sim)
   - S2 = what is acting (mechanism, sensor, algorithm)
   - F = field type (mechanical, electrical, informational, thermal)
3. **Classify** the problem (incomplete / harmful / insufficient / excessive)
4. **Look up** matching solution class → get 2-3 candidate solutions
5. **Apply** → modify concept → re-evaluate with VDI 2225
6. **Compare** OWV before vs after (must improve, no criterion < 4/10)

## Field Types for Defense Training Products

| Field | Examples in WX Products |
|-------|------------------------|
| Mechanical | Recoil force, vibration, weight, friction |
| Pneumatic | Gas pressure, air flow, pneumatic actuation |
| Electrical | Sensor signals, power supply, electromagnetic |
| Informational | Scoring data, AI inference, display feedback |
| Thermal | Heat from firing sim, tropical environment, electronics cooling |
| Acoustic | Gunshot sound simulation, noise feedback |
| Optical | Laser scoring, visual display, RCS reflection |
