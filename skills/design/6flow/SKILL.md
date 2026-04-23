Generate a 6-flow function structure for a product or subsystem.

Usage: /6flow [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What product or subsystem are you analyzing?
   - What is the overall function? (solution-neutral statement)
   - What are the inputs and outputs?

2. Read project artifacts if they exist:
   - `1_Projects/{{project}}/Status.md`
   - Existing function structure from Phase 1 or Phase 2

3. Generate the 6-flow function structure:

```
# 6-FLOW FUNCTION STRUCTURE — {{product}}
**Date:** {{today}}

---

## OVERALL FUNCTION
{{Verb + Object + Qualifier — solution-neutral}}

## 6-FLOW DECOMPOSITION

### Direct Flows (what the product DOES)
| Flow | Description | Input | Output |
|------|-------------|-------|--------|
| **D — Drive** | Primary energy conversion / force generation | | |
| **C — Control** | Regulation, feedback, decision logic | | |
| **T — Transmit** | Transfer of forces, motion, signals | | |

### Enabling Flows (what SUPPORTS the product)
| Flow | Description | Input | Output |
|------|-------------|-------|--------|
| **E — Energy** | Power supply, distribution, storage | | |
| **M — Material** | Physical media, consumables, structure | | |
| **S — Signal** | Information, sensing, communication | | |

---

## FUNCTION STRUCTURE DIAGRAM

```
INPUT                                                    OUTPUT
  |                                                        |
  +--[D: Drive]--+--[T: Transmit]--+--[C: Control]---->  |
  |              |                  |                      |
  +--[E: Energy supply]            |                      |
  +--[M: Material/Structure]       |                      |
  +--[S: Signal/Sensing]-----------+                      |
```

---

## SUB-FUNCTION TABLE

| ID | Sub-function | Flow Type | Level | Parent | Requirements Traced |
|----|-------------|-----------|-------|--------|-------------------|
| F1.1 | | D/C/T/E/M/S | L1 | — | |
| F1.1.1 | | | L2 | F1.1 | |

---

## FLOW INTERACTION MATRIX
Which flows interact? (mark X)

|   | D | C | T | E | M | S |
|---|---|---|---|---|---|---|
| D | — | | | | | |
| C | | — | | | | |
| T | | | — | | | |
| E | | | | — | | |
| M | | | | | — | |
| S | | | | | | — |

**Critical interactions:** {{flows with highest coupling — candidates for interface control}}

---

## TRIPLE HELIX CHECK
- [ ] Every D-flow sub-function has a controlling C-flow?
- [ ] Every S-flow has a defined signal path (sensor -> processor -> actuator)?
- [ ] Energy budget accounts for all E-flow consumers?
- [ ] Material flows include maintenance/consumables?
```

4. Present to user for review. Save to:
   `1_Projects/{{project}}/Phase1-Task/{{PROJECT_NAME}}_6Flow_Function_Structure_v1.0.md`
   Or Phase2-Concept/ if refining an existing structure.

RULES:
- Solution-neutral: describe WHAT, not HOW
- Every sub-function must trace to >=1 requirement
- D-C-T are the core product functions; E-M-S enable them
- If a flow type has zero sub-functions, question whether the analysis is complete
- Reference: Pahl-Beitz Chapter 5 (function structure) + Triple Helix extension
