---
name: triz-40-principles
description: TRIZ 40 Inventive Principles + Contradiction Matrix reference for innovative concept generation
---

# TRIZ 40 Inventive Principles — Quick Reference

## Principles (Altshuller 1946-2005)

| # | Principle | Description | WX Example |
|---|-----------|-------------|------------|
| 1 | Segmentation | Divide into independent parts | Modular trainer sections |
| 2 | Taking out | Separate interfering part | External compressor (VN-12.7MM-SIM) |
| 3 | Local quality | Change uniform to non-uniform structure | Masselotte on piston (local mass) |
| 4 | Asymmetry | Change symmetrical to asymmetrical | Offset mount point |
| 5 | Merging | Combine identical objects/operations | Multi-weapon trainer |
| 6 | Universality | One object performs several functions | Sensor doubles as structural element |
| 7 | Nesting | Place one object inside another | Cable drum inside UUV (VN-XUONG) |
| 8 | Anti-weight | Compensate weight with lift/buoyancy | Foam-filled HDPE hull |
| 9 | Preliminary anti-action | Pre-stress to counter expected stress | Pre-tensioned mooring line |
| 10 | Preliminary action | Pre-arrange objects for convenient use | Pre-loaded magazine simulator |
| 11 | Beforehand cushioning | Prepare emergency means in advance | Fallback Level 0-3 (ACH) |
| 12 | Equipotentiality | Eliminate need to raise/lower | Level sensor array |
| 13 | The other way around | Invert the action | Target moves, not shooter |
| 14 | Spheroidality | Replace linear with rotary motion | Rotating target carousel |
| 15 | Dynamicity | Make rigid parts movable/adaptive | Extendable recoil stroke |
| 16 | Partial or excessive action | Do slightly more/less than required | Over-engineer wall thickness (HDPE tropical) |
| 17 | Another dimension | Move to 2D or 3D | 3-screen wrap-around display |
| 18 | Mechanical vibration | Use oscillation/resonance | Piezo vibration sensing (BB-01) |
| 19 | Periodic action | Replace continuous with periodic | Burst-mode recoil simulation |
| 20 | Continuity of useful action | Eliminate idle time | Continuous data capture during training |
| 21 | Skipping/rushing through | Conduct process at high speed | High-speed ADC sampling |
| 22 | Blessing in disguise | Use harmful factor beneficially | Recoil energy → haptic feedback |
| 23 | Feedback | Introduce or improve feedback | Real-time scoring display |
| 24 | Intermediary | Use intermediate object | Charge amplifier between piezo and ADC |
| 25 | Self-service | Object services itself | Self-calibrating sensor |
| 26 | Copying | Use cheaper copy instead of original | Simulator replaces live fire |
| 27 | Cheap short-living | Replace expensive durable with cheap disposable | Consumable target panels |
| 28 | Mechanics substitution | Replace mechanical with other fields | Pneumatic replaces electric motor |
| 29 | Pneumatics and hydraulics | Use gas/liquid instead of solid | Pneumatic recoil system |
| 30 | Flexible shells and thin films | Use flexible membranes | Flexible cable routing |
| 31 | Porous materials | Make object porous | Perforated target backing |
| 32 | Color changes | Change color/transparency | Hit indicator LED |
| 33 | Homogeneity | Objects interacting should be same material | All-HDPE hull construction |
| 34 | Discarding and recovering | Make portions disappear after use | Biodegradable target elements |
| 35 | Parameter changes | Change physical state/concentration/flexibility | Adjust gas pressure for force control |
| 36 | Phase transitions | Use volume change during phase transition | — |
| 37 | Thermal expansion | Use thermal expansion/contraction | Temperature-compensated calibration |
| 38 | Strong oxidants | Replace normal air with enriched/ionized | — |
| 39 | Inert atmosphere | Replace normal environment with inert | Sealed electronics enclosure |
| 40 | Composite materials | Replace homogeneous with composite | Carbon-fiber reinforced mount |

## Contradiction Matrix (Abridged — Defense Training Relevant Parameters)

To use: identify IMPROVING parameter and WORSENING parameter → matrix gives 3-4 suggested principles.

**39 Engineering Parameters (Altshuller):**

| # | Parameter | # | Parameter |
|---|-----------|---|-----------|
| 1 | Weight of moving object | 21 | Power |
| 2 | Weight of stationary object | 22 | Loss of energy |
| 5 | Area of moving object | 25 | Loss of time |
| 9 | Speed | 27 | Reliability |
| 10 | Force | 30 | Object-generated harmful factors |
| 11 | Stress/pressure | 32 | Ease of manufacture |
| 12 | Shape | 33 | Ease of operation |
| 13 | Stability of object composition | 34 | Ease of repair |
| 14 | Strength | 35 | Adaptability/versatility |
| 17 | Temperature | 36 | Device complexity |
| 19 | Use of energy by moving object | 39 | Productivity |

**Key Contradiction Pairs (Defense Training):**

| Improving ↓ / Worsening → | Reliability (27) | Cost/Complexity (36) | Force (10) | Adaptability (35) |
|---------------------------|-----------------|---------------------|-----------|-------------------|
| Reliability (27) | — | 11,28,1,35 | 15,3,32 | 1,13,35 |
| Force (10) | 15,3,32 | 36,35,21 | — | 15,35,2 |
| Adaptability (35) | 1,13,35 | 15,29,37,28 | 15,35,2 | — |
| Ease of operation (33) | 25,2,13,15 | 12,26,1,32 | — | 15,34,1,16 |
| Productivity (39) | 1,35,10,38 | 10,37,14 | 28,15,10,36 | 35,28,2,24 |

(Full 39×39 matrix: see Altshuller 2005 or TRIZ NLM notebook `nlm query triz`)

## Workshop X Applied Examples

| Principle | Product | Application |
|-----------|---------|------------|
| #2 Taking out | VN-12.7MM-SIM | External compressor (separate from mount) |
| #3 Local quality | VN-12.7MM-SIM | Masselotte on piston (local mass addition for recoil profile) |
| #7 Nesting | VN-XUONG-UUV | Cable drum inside UUV (collapsed 9→1 sub-functions) |
| #8 Anti-weight | VN-AST-MSL-001 | Foam-filled HDPE hull (buoyancy + structure) |
| #15 Dynamicity | VN-12.7MM-SIM | Two-Channel recoil (separate brake + pneumatic) |
| #26 Copying | All trainers | Simulator replaces live fire (core business model) |
| #28 Mechanics sub. | VN-12.7MM-SIM | Pneumatic replaces electric motor (patent freedom) |
| #29 Pneumatics | VN-12.7MM-SIM | Gas pressure for force control |
| #33 Homogeneity | VN-AST-MSL-001 | All-HDPE construction (weld compatibility) |
| #35 Parameter change | VN-12.7MM-SIM | Adjust gas pressure instead of motor speed |
