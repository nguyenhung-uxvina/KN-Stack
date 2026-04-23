Detect system archetypes in a problem, project, or organizational pattern.

Usage: /archetype [system_description] OR provide details interactively.

1. If $ARGUMENTS provided, use as system description; otherwise ask:
   - What problem or pattern are you observing?
   - Is it recurring? How long has it persisted?
   - What fixes have been tried? Did they work short-term but fail long-term?

2. Test against all 8 classic system archetypes:

```
# SYSTEM ARCHETYPE ANALYSIS — {{system}}
**Date:** {{today}}

---

## ARCHETYPE SCREENING

### 1. Shifting the Burden
**Pattern:** A problem symptom is addressed with a quick fix (symptomatic solution) instead of a fundamental solution. The quick fix weakens the capacity for the fundamental fix over time.
- Quick fix present? {{Y/N — what is it?}}
- Fundamental solution being avoided? {{Y/N — what is it?}}
- Is capacity for fundamental solution eroding? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 2. Limits to Growth
**Pattern:** A reinforcing process of growth hits a balancing constraint that slows or reverses growth.
- Growth engine present? {{Y/N — what drives growth?}}
- Constraint or limit visible? {{Y/N — what is it?}}
- Is the constraint being ignored while pushing growth harder? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 3. Fixes that Fail
**Pattern:** A fix that works short-term but creates side effects that worsen the original problem.
- Short-term fix applied? {{Y/N}}
- Unintended side effects? {{Y/N — what?}}
- Is the original problem worse than before the fix? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 4. Success to the Successful
**Pattern:** Two activities compete for resources. The more successful one gets more resources, starving the other.
- Two competing activities? {{Y/N — what are they?}}
- Is the "winner" getting disproportionate resources? {{Y/N}}
- Is the "loser" being starved? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 5. Tragedy of the Commons
**Pattern:** Individuals use a shared resource for individual gain, depleting it for everyone.
- Shared resource? {{Y/N — what?}}
- Individual incentive to overuse? {{Y/N}}
- Is total demand exceeding capacity? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 6. Escalation
**Pattern:** Two parties each respond to the other's actions with increasing intensity.
- Two competing parties? {{Y/N}}
- Each responding to the other's moves? {{Y/N}}
- Is intensity increasing? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 7. Growth and Underinvestment
**Pattern:** Growth approaches a limit that can be raised by investment, but the investment is not made because performance standards erode.
- Growth approaching a limit? {{Y/N}}
- Investment that could raise the limit? {{Y/N — what?}}
- Are standards being lowered instead of investing? {{Y/N}}
- **Match:** STRONG / WEAK / NO

### 8. Eroding Goals
**Pattern:** When performance falls short of goals, the goals are lowered instead of improving performance.
- Goals being missed? {{Y/N}}
- Are goals being revised downward? {{Y/N}}
- Is effort to improve being reduced? {{Y/N}}
- **Match:** STRONG / WEAK / NO

---

## DIAGNOSIS

**Primary archetype:** {{name}} (STRONG match)
**Secondary archetype:** {{name, if any}} (WEAK match)

**Causal structure:**
{{Draw the archetype's causal loop in text form}}

**Leverage point:**
{{Where to intervene based on the archetype's known intervention strategy}}

---

## ARCHETYPE-SPECIFIC INTERVENTION

| Archetype | Generic Intervention | Specific Action for This Case |
|-----------|---------------------|------------------------------|
| Shifting the Burden | Strengthen fundamental solution, weaken symptomatic fix | |
| Limits to Growth | Identify and remove the constraint (don't push growth harder) | |
| Fixes that Fail | Address root cause, not symptoms | |
| Growth & Underinvestment | Invest in capacity BEFORE performance erodes | |
```

3. Present analysis to user. Do NOT auto-implement interventions.

RULES:
- Most real systems match 1-2 archetypes — finding 4+ matches means the analysis is too loose
- Shifting the Burden is the most common in knowledge work — check it first
- Cross-reference Galaxy: Shifting the Burden, Nested Shifting the Burden, AI Dependency Spiral
- COD: Offload (AI screens archetypes, CEO validates diagnosis)
- If archetype involves AI delegation patterns, explicitly flag R3 (AI Dependency Spiral) risk
