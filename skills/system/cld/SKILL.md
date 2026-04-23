Generate a Causal Loop Diagram (CLD) for a system, problem, or design challenge.

Usage: /cld [system_description] OR provide details interactively.

1. If $ARGUMENTS provided, use as system description; otherwise ask:
   - What system or problem are you analyzing?
   - What is the behavior you're trying to understand? (growth, oscillation, decline, stagnation)
   - What are the key variables? (list 3-5 to start)

2. Execute CLD analysis:

```
# CAUSAL LOOP DIAGRAM — {{system}}
**Date:** {{today}}

---

## 1. VARIABLE INVENTORY
| # | Variable | Type | Units (if measurable) | Currently | Trend |
|---|----------|------|----------------------|-----------|-------|
| 1 | | Stock/Flow/Auxiliary | | High/Med/Low | up/down/flat |

---

## 2. CAUSAL LINKS
| From | To | Polarity | Delay? | Evidence |
|------|----|----------|--------|----------|
| Variable A | Variable B | + (same direction) | No | {{why this link exists}} |
| Variable B | Variable C | - (opposite direction) | Yes (weeks) | |

---

## 3. FEEDBACK LOOPS IDENTIFIED

### Reinforcing Loops (R) — drive growth or collapse
| Loop | Variables | Behavior | Name |
|------|----------|----------|------|
| R1 | A -> B -> C -> A | {{growing/collapsing}} | "{{descriptive name}}" |

### Balancing Loops (B) — drive toward equilibrium
| Loop | Variables | Behavior | Name |
|------|----------|----------|------|
| B1 | X -> Y -> X | {{stabilizing}} | "{{descriptive name}}" |

---

## 4. CLD TEXT DIAGRAM

```
     +         +
A -------> B -------> C
^                     |
|          -          |
+---------------------+
        R1: "Name"
```

(+ = same direction, - = opposite direction)
(R = reinforcing loop, B = balancing loop)

---

## 5. DOMINANT LOOP ANALYSIS
- Which loop is currently DOMINANT (driving observed behavior)?
- What would shift dominance to a different loop?
- Are there delays that create oscillation risk?

---

## 6. ARCHETYPE CHECK
Does this match a known system archetype?
- [ ] Shifting the Burden
- [ ] Limits to Growth
- [ ] Fixes that Fail
- [ ] Success to the Successful
- [ ] Tragedy of the Commons
- [ ] Escalation
- [ ] Growth and Underinvestment
- [ ] Eroding Goals

If match found: {{archetype name}} — see Galaxy note for implications.

---

## 7. LEVERAGE POINTS
Based on the CLD structure, where would intervention have the most impact?
| Leverage Point | Loop Affected | Action | Risk |
|---------------|--------------|--------|------|
| | R1/B1 | | |
```

3. Present to user. Do NOT save unless asked.

RULES:
- Start with 5-8 variables — CLDs with >12 variables are too complex to be useful
- Every link must have polarity (+ or -) — ambiguous links indicate unclear thinking
- Every loop must have a descriptive name — unnamed loops are forgotten
- Check for delays — they cause oscillation and are often invisible
- COD: Offload (AI draws, CEO validates causal structure)
- Cross-reference Galaxy: Shifting the Burden, Nested Shifting the Burden, AI Dependency Spiral
