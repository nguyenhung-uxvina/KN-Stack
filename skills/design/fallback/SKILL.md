Design a fallback architecture for a product or critical subsystem.

Usage: /fallback [product_or_subsystem] OR provide details interactively.

1. If $ARGUMENTS provided, use as target; otherwise ask:
   - What product or subsystem needs a fallback architecture?
   - What is the primary design approach? (the "Plan A")
   - What failure modes are you protecting against?
   - What is the consequence of total failure? (safety, mission, financial)

2. Read project artifacts if they exist:
   - `1_Projects/{{project}}/Status.md`
   - Risk register from Phase 2 or Phase 3
   - Concept evaluation (was there a runner-up concept?)

3. Generate fallback architecture:

```
# FALLBACK ARCHITECTURE — {{target}}
**Date:** {{today}}  |  **Project:** {{project}}

---

## 1. PRIMARY APPROACH (Plan A)
| Aspect | Description |
|--------|-------------|
| Design | {{current selected approach}} |
| TRL | {{current TRL}} |
| Key risk | {{what could go wrong}} |
| Failure consequence | Safety / Mission-critical / Financial / Schedule |

---

## 2. FAILURE MODE ANALYSIS
| # | Failure Mode | Probability | Severity | Detection | Trigger for Fallback |
|---|-------------|-------------|----------|-----------|---------------------|
| FM-1 | | H/M/L | H/M/L | H/M/L | {{measurable trigger}} |

---

## 3. FALLBACK OPTIONS

### Option F1: Graceful Degradation
- What: Reduce capability but maintain core function
- How: {{specific technical approach}}
- Cost to implement: {{additional cost}}
- Performance loss: {{what you give up}}

### Option F2: Alternative Technology
- What: Switch to runner-up concept from Phase 2
- How: {{which concept, what changes needed}}
- Cost to switch: {{time + money}}
- Schedule impact: {{weeks/months}}

### Option F3: COTS Replacement
- What: Replace custom design with commercial off-the-shelf
- How: {{specific COTS product/approach}}
- Cost: {{typically higher unit cost, lower NRE}}
- Trade-off: {{local content impact, performance delta}}

---

## 4. FALLBACK DECISION MATRIX
| Criterion | Weight | F1 Degrade | F2 Alt Tech | F3 COTS |
|-----------|--------|-----------|-------------|---------|
| Implementation speed | 25% | | | |
| Cost | 20% | | | |
| Performance retained | 25% | | | |
| Risk of fallback failing | 15% | | | |
| Local content impact | 15% | | | |

**Recommended fallback:** {{option}} — activate if {{trigger}}

---

## 5. ACTIVATION PROTOCOL
1. **Trigger:** {{specific measurable condition, e.g., "brake test GO-2 FAIL"}}
2. **Decision maker:** CEO (Core — not delegatable)
3. **Switch cost:** {{time + money to activate fallback}}
4. **Point of no return:** {{date/event after which switching is too expensive}}

---

## 6. PREEMPTIVE ACTIONS
| Action | Purpose | Cost | When |
|--------|---------|------|------|
| {{e.g., "Source alternative brake"}} | Reduce switch time | {{cost}} | Now / At trigger |
```

4. Present to user. Save to:
   `1_Projects/{{project}}/Phase3-Embodiment/{{PROJECT_NAME}}_Fallback_{{subsystem}}_v1.0.md`

RULES:
- Every critical subsystem with TRL <6 SHOULD have a fallback
- Fallback triggers must be MEASURABLE — "if it doesn't work" is not a trigger
- Always include "point of no return" — switching has a deadline
- Runner-up concepts from Phase 2 are natural fallback candidates
- COD: Offload (AI designs architecture, CEO decides activation)
- Preemptive actions reduce switching cost — recommend them proactively
