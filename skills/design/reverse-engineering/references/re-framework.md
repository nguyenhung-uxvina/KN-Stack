# RE Framework Reference — 3D-A-R-D + VDI 2206 Inverted V-Model

## 3D-A-R-D Cycle (Core Framework)

```
FORWARD DESIGN (P&B):           REVERSE ENGINEERING:
Requirements                     Physical Artifact
    ↓                                ↑
Conceptual Design                Requirements Reconstruction
    ↓                                ↑
Embodiment Design                Functional Abstraction
    ↓                                ↑
Detail Design                    Deconstruction
    ↓                                ↑
Manufacturing                    Document / Measure
```

**3D** = Deconstruct (physical analysis) → Decode (requirements) → Document (dossier)
**A** = Abstract (solution-neutral function structure)
**R** = Reconstruct (P&B forward design with VN constraints)
**D** = Deploy (V&V + production transfer)

Key difference from forward design: RE begins from physical artifact or incomplete documentation (often foreign product needing localization) and must reconstruct intent before redesign.

---

## VDI 2206 Inverted V-Model for Mechatronic RE

```
FORWARD V-MODEL (Design):              REVERSE V-MODEL (RE):
Requirements                            Integrated Artifact
    ↓                                        ↑
System Design → Domain Design          Domain Decomposition
    ↓ Mech/Elec/Sw/Ctrl                    ↑ Mech/Elec/Sw/Ctrl
Implementation                          Physical Examination
    ↓                                        ↑
Integration → V&V                      Behavioral Testing
                                             ↑
                                       Requirements Reconstruction
```

**Key insight:** In mechatronic systems, function is NOT 1-to-1 with component. One function is distributed across Mech + Elec + Sw + Ctrl domains. Example: target drone autopilot stability = actuator (mech) + IMU (elec) + control algorithm (sw) + PID tuning (ctrl).

---

## Domain Decomposition Template

### Domain 1 — Mechanical
| Sub-category | What to catalog |
|-------------|----------------|
| Structural | Frame, housing, brackets, chassis |
| Kinematic | Bearings, gears, linkages, actuators (mech part) |
| Thermal | Heatsinks, thermal pads, cooling paths |
| Sealing | O-rings, gaskets, potting compound |
| Vibration/Shock | Isolators, dampers, resilient mounts |

### Domain 2 — Electronic
| Sub-category | What to catalog |
|-------------|----------------|
| Power electronics | PSU, DC-DC converters, BMS, power switching |
| Signal conditioning | Amplifiers, filters, ADC/DAC, multiplexers |
| Processing | MCU, FPGA, DSP, SoC (identify part numbers) |
| Memory | RAM, Flash, EEPROM (size, interface) |
| Communication | UART/SPI/CAN transceivers, Ethernet PHY, RF |
| Sensors | IMU, GPS, magnetometer, pressure, temp, encoders |
| Actuators (elec) | Motor drivers, servo controllers, solenoid drivers |
| Interconnects | PCB layers, connectors, cables, harness |

### Domain 3 — Software
| Sub-category | What to catalog |
|-------------|----------------|
| Bootloader/BSP | Init sequence, hardware abstraction |
| RTOS/OS | Real-time constraints, scheduler type |
| Device drivers | Per sensor/actuator interface |
| Middleware | Comm stacks, filesystems, protocols |
| Application logic | Main functionality, mission logic |
| Control algorithms | PID, Kalman, state machines, planners |
| Safety/monitoring | Watchdog, BIT/BITE, failsafe logic |

### Domain 4 — Control
| Sub-category | What to catalog |
|-------------|----------------|
| Inner loops | Motor current/speed (1-10 kHz) |
| Middle loops | Velocity/rate control (100-500 Hz) |
| Outer loops | Position/attitude (10-100 Hz) |
| Supervisory | Mode management (variable rate) |
| Safety logic | Fault detection, recovery, termination |
| State machines | Operational modes, transitions, timing |

---

## Cross-Domain Hidden Dependencies

| Coupling | Source → Victim | Effect |
|----------|----------------|--------|
| Thermal → Electronic | Heat affects sensor accuracy, IC reliability |
| Vibration → Sensors | Amplifies sensor noise, false readings |
| EMI → Electronic/Software | Corrupts communication, false triggers |
| Power → All | Brownouts cause soft failures across domains |
| Timing → Control | Latency cascade destabilizes control loops |

---

## Control Law Reverse — System Identification Tests

| Test Type | Input Signal | What It Reveals |
|-----------|-------------|----------------|
| Step response | Step input | Time constants, damping, overshoot |
| Impulse response | Impulse | Transfer function characteristics |
| Frequency sweep | Chirp | Bode plot, resonances, bandwidth |
| PRBS | Pseudo-random | MIMO system identification |
| Sine wave | Single freq | Specific frequency response point |

### Common Model Structures
- First-order: `G(s) = K/(τs+1)` — simple actuators
- Second-order: `G(s) = ω²/(s²+2ζωs+ω²)` — most control loops
- With delay: `G(s)·e^(-Ts)` — computation/comm delay
- State-space: `ẋ = Ax + Bu; y = Cx` — complex MIMO

### PID Indicators
- Steady-state accuracy → integrator present?
- Phase lead → derivative present?
- Robustness to parameter changes → tuning quality

---

## RE Maturity Levels

### Understanding Depth (L1-L5)
| Level | Description | Indicator |
|-------|------------|-----------|
| L1 Surface | Know what it does | Can describe external behavior |
| L2 Structural | Know what's inside | Can list components |
| L3 Functional | Know how it works | Can explain mechanisms |
| L4 Causal | Know WHY designed this way | Can justify design choices |
| L5 Generative | Could design equivalent | Can propose alternatives |

**Target: L4-L5 before committing to redesign.**

### Model Fidelity (F1-F5)
| Level | Description |
|-------|------------|
| F1 | Correct topology, wrong values |
| F2 | Correct for specific operating point |
| F3 | Correct over operating envelope |
| F4 | Correct including environmental effects |
| F5 | Correct including aging/wear effects |

**Target: F3 minimum, F4 preferred for defense.**

---

## Defense RE Context — Vietnam Specifics

### VN Legal Framework
- Luat Cong nghiep Quoc phong 2024
- Law 32/2021/QH15 procurement
- IP Law Vietnam 2022 amendments
- Technology transfer agreement requirements

### VN Acceptance Testing
1. Thu nghiem xuat xuong (factory acceptance)
2. Thu nghiem nghiem thu cap Bo (ministry acceptance)
3. Thu nghiem chien dau / su dung (operational trials)

### VN Test Facilities
- Vien Cong nghe va Chien luoc Bien (naval)
- Vien Ky thuat Khong quan (aerial)
- Vien KHCN Quan su (general defense)

### ITAR-Free Component Sourcing Priority
1. Domestic (VN) — highest priority
2. Friendly nations (non-sanctioning)
3. Commercial off-the-shelf (dual-use safe)
4. NEVER from restricted/sanctioned sources

### VDI 2225 Weights for Defense RE
| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Technical performance | 35% | Function, reliability, margins |
| Manufacturability | 25% | VN capability, tooling, skills |
| Sovereignty | 20% | ITAR-free, domestic %, resilience |
| Cost | 10% | Unit, lifecycle, tooling |
| Time-to-deploy | 10% | Development + qualification |

---

## Software RE Redevelopment Options

| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| A: Full independent | Clean IP, tailored | Slow, expensive | Critical unique functions |
| B: Open-source adapt | Proven, community | Dependencies | Standard functions |
| C: COTS commercial | Supported, rich | Export control, cost | Non-critical subsystems |
| D: Hybrid | Balanced | Complexity | Most real projects |

### Open-Source Candidates for Defense Mechatronic
- Flight control: ArduPilot / PX4
- Robotics: ROS / ROS2
- RTOS: NuttX / Zephyr / FreeRTOS
- MBSE: Eclipse Papyrus (SysML)
- Physics: OpenModelica
- Control: Scilab / Python (scipy.signal)

---

## Integration Risk Categories (MECHA mode)

| # | Category | Key Concern | MIL-STD |
|---|----------|-------------|---------|
| 1 | Timing & Latency | Sensor→processor→actuator chain | — |
| 2 | Resource Contention | CPU, memory, bus, power budgets | — |
| 3 | EMC | Motor noise, switching PSU, RF | MIL-STD-461G |
| 4 | Thermal | Hotspots, cooling, cycling fatigue | MIL-STD-810G |
| 5 | Tolerance Stack-up | Optical/PCB/antenna alignment | — |
| 6 | SW-HW Coupling | ADC resolution, motor params in SW | — |
| 7 | Control Stability | New dynamics → retune control | — |

### Bottom-Up Integration Test Sequence
1. Component qualification (2 weeks)
2. Domain integration (3 weeks)
3. Two-domain integration (2 weeks)
4. Three-domain integration (2 weeks)
5. Full system integration + debug (4 weeks)
6. Environmental qualification (2 weeks)
7. Mission qualification (2 weeks)
Total: ~17 weeks for target drone class complexity

### Early Warning Signs of Integration Failure
- Intermittent failures → usually EMC or timing
- Works in lab, fails in field → environmental
- Works with original, fails with redesigned → interface mismatch
- Software timeouts increasing → resource contention
- Behavior changes with temperature → thermal or tolerance
