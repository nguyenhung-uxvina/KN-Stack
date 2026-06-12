---
name: constraint
description: Identifies the binding constraint in a project, organization, or technical subsystem using Theory of Constraints (TOC) and systems thinking, then prescribes a focused exploitation plan. Use when progress feels blocked, throughput is low, or a single bottleneck is suspected. Triggers on: "constraint", "bottleneck", "theory of constraints", "TOC", "ràng buộc", "nút cổ chai", "điểm nghẽn".
---
Identify the scientific binding constraint in a system, project, or organization.

Usage: /constraint [target] OR provide details interactively.

1. If $ARGUMENTS provided, use as target system; otherwise ask:
   - What system are you analyzing? Options:
     a) A specific project (e.g., VN-12.7MM-SIM)
     b) The Workshop X organization (BRIDGE x FORGE x HELIX)
     c) A technical subsystem (e.g., signal chain, mechanical assembly)
     d) A process (e.g., procurement, design review cycle)

2. Based on target type, gather data:
   - **Project:** Read Status.md, blocking constraints, phase progress, flags
   - **Organization:** Read all Status.md files, Area dashboards, CLAUDE.md metrics
   - **Technical:** Read relevant design documents, requirements, test results
   - **Process:** Read SOPs, timelines, dependency maps

3. Apply Theory of Constraints (TOC) + Systems Thinking analysis:

```
# CONSTRAINT ANALYSIS — {{target}}
**Date:** {{today}}

---

## 1. SYSTEM GOAL
{{What is the system trying to achieve? Quantify if possible.}}

## 2. CONSTRAINT IDENTIFICATION

### Method: Five Focusing Steps (Goldratt)
1. **IDENTIFY** the constraint
   - What single factor limits throughput of the entire system?
   - Evidence: {{data points showing this is the bottleneck}}

2. **EXPLOIT** the constraint
   - How to get maximum output from the constraint WITHOUT adding resources?
   - {{specific actions}}

3. **SUBORDINATE** everything else
   - What other activities should slow down or change to support the constraint?
   - {{what to stop doing, what to deprioritize}}

4. **ELEVATE** the constraint
   - If exploit + subordinate aren't enough, what investment breaks the constraint?
   - {{resources, tools, skills, people needed}}

5. **REPEAT** — what becomes the new constraint after this one is broken?
   - {{predicted next bottleneck}}

---

## 3. CONSTRAINT MAP

```
{{ASCII diagram showing the constraint in the system flow}}
{{Mark the bottleneck with [>>>CONSTRAINT<<<]}}
```

---

## 4. LEVERAGE ANALYSIS
| Intervention | Impact | Effort | Leverage Score |
|-------------|--------|--------|---------------|
| {{action 1}} | H/M/L | H/M/L | {{I/E ratio}} |
| {{action 2}} | | | |

**Highest leverage action:** {{the one thing to do first}}

---

## 5. ANTI-PATTERNS CHECK
- [ ] Optimizing non-constraints? (waste of effort)
- [ ] Local optimization breaking global flow?
- [ ] Shifting the Burden archetype present?
- [ ] Multiple constraints confused with single binding constraint?

---

## 6. RECOMMENDATION
**Binding Constraint:** {{one sentence}}
**Exploit Action:** {{immediate, zero-cost action}}
**Elevate Action:** {{investment action if exploit insufficient}}
**Expected Impact:** {{what improves and by how much}}
```

4. Present analysis to user. Do NOT auto-implement recommendations.

RULES:
- There is ONLY ONE binding constraint at a time — resist listing 5 "constraints"
- Use data, not opinions — cite Status.md metrics, phase progress, timelines
- Check for Shifting the Burden archetype — the obvious constraint may be a symptom
- For organizational analysis, use Compound Law: weakest domain × others = compound health
- COD: This is Offload (AI analyzes, CEO validates and decides)
- Link to Galaxy notes if relevant (especially Shifting the Burden, Physical-World Interface)
- If the constraint is a Core task (judgment, decision), flag it — AI cannot resolve Core constraints
