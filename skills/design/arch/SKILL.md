Manage cross-subsystem integration architecture for a project — Triple Helix (Mech/Elec/SW) coordination, interface governance, and integration debt tracking.

Usage: /arch [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - Which active project? List projects from `1_Projects/*/Status.md`

2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md` — phase, subsystems, blockers
   - System architecture doc (e.g., `Phase3-Embodiment/*System_Architecture*`)
   - ICD tracker (e.g., `Phase3-Embodiment/*ICD*`)
   - BOM if exists (e.g., `Phase3-Embodiment/*BOM*`)
   - Any design review logs or decision journals

3. Generate the Integration Architecture Review:

```
# INTEGRATION ARCHITECTURE — {{project}}
**Date:** {{today}} | **Phase:** {{phase}} | **Review #:** {{increment}}

---

## TRIPLE HELIX STATUS

Each domain runs at its own clock speed. This section tracks alignment.

### Mechanical
- **Current state:** {{what's been designed/built}}
- **Next milestone:** {{what and when}}
- **Blocking on Elec/SW:** {{interface dependency or "None"}}

### Electrical
- **Current state:** {{schematic, PCB, power, sensors}}
- **Next milestone:** {{what and when}}
- **Blocking on Mech/SW:** {{interface dependency or "None"}}

### Software / AI
- **Current state:** {{firmware, algorithms, UI}}
- **Next milestone:** {{what and when}}
- **Blocking on Mech/Elec:** {{interface dependency or "None"}}

### Domain Clock Speeds
| Domain | Iteration Cycle | Current Phase | Sync Needed By |
|--------|----------------|---------------|----------------|
| Mech   | {{weeks}}      | {{status}}    | {{date}}       |
| Elec   | {{weeks}}      | {{status}}    | {{date}}       |
| SW/AI  | {{weeks}}      | {{status}}    | {{date}}       |

---

## INTERFACE GOVERNANCE

### Critical Interfaces (from ICD)
| IF# | From → To | Type | Status | TBD Count | Risk | Owner |
|-----|-----------|------|--------|-----------|------|-------|
{{top 5-10 highest-risk interfaces}}

### Interface Decisions Needed
| # | Interface | Decision | Impact if Delayed | Deadline |
|---|-----------|----------|-------------------|----------|
{{decisions that block integration}}

---

## INTEGRATION DEBT LEDGER

| # | Debt Item | Source | Impact | Effort | Age (weeks) | Trend |
|---|-----------|--------|--------|--------|-------------|-------|
{{list all TBDs, assumptions, unresolved conflicts}}

**Summary:**
- Total debt items: {{N}}
- Critical (blocking build): {{N}}
- Trend vs last review: {{increasing / stable / decreasing}}
- Debt velocity: {{items added vs resolved per week}}

---

## ARCHITECTURE DECISION LOG (since last review)

| # | Decision | Rationale | Alternatives Rejected | Impact on Interfaces |
|---|----------|-----------|----------------------|---------------------|
{{recent architecture-level decisions}}

---

## INTEGRATION RISK MAP

Cross-domain risk heat map:

|              | Mech     | Elec     | SW/AI    | External |
|--------------|----------|----------|----------|----------|
| **Mech**     | —        | {{G/Y/R}} | {{G/Y/R}} | {{G/Y/R}} |
| **Elec**     |          | —        | {{G/Y/R}} | {{G/Y/R}} |
| **SW/AI**    |          |          | —        | {{G/Y/R}} |
| **External** |          |          |          | —        |

G = All interfaces defined, no TBDs
Y = Interfaces defined, minor TBDs remain
R = TBDs or conflicts blocking integration

---

## SYNC POINT PLAN

### Next Sync Point
- **Date:** {{proposed date, within 1-2 weeks}}
- **Agenda:**
  1. {{Mech update — what changed, what's coming}}
  2. {{Elec update — what changed, what's coming}}
  3. {{SW update — what changed, what's coming}}
  4. ICD changes requiring cross-domain agreement
  5. Integration debt triage (resolve or defer?)
- **Required decisions:** {{list decisions that MUST be made at sync}}
- **Output:** Updated ICD + debt ledger

### Sync History
| Date | Decisions Made | Debt Resolved | Debt Added | Net |
|------|---------------|---------------|------------|-----|
{{log of past sync points}}

---

## REUSE & PLATFORM CHECK
- Components shared with other projects: {{list}}
- Interface standards reused: {{list or "none"}}
- IRONMESH platform alignment: {{if applicable}}
- Cross-project ICD conflicts: {{flag if same interface defined differently across projects}}
```

4. Present to user. Offer to:
   a) Save as `1_Projects/{{project}}/Phase3-Embodiment/{{PROJECT}}_Integration_Architecture_v{{N}}.md`
   b) Update the ICD tracker with new findings
   c) Schedule next sync point (add to Status.md)

RULES:
- Integration architecture starts at Phase 2 (function structure → subsystem interfaces) but gets serious in Phase 3
- For Phase 1 projects, generate a LIGHTWEIGHT version: just domain identification + anticipated interfaces
- Triple Helix means domains run CONCURRENTLY, not sequentially — track clock speed mismatches
- Integration debt is the #1 killer of defense prototypes — make it visible and measured
- Every TBD in an ICD is a debt item — no exceptions
- Sync points are NOT status meetings — they are DECISION meetings about interfaces
- Cross-project interfaces are highest risk — flag when one project's decision affects another
- COD: Offload (AI compiles architecture view, CEO validates decisions and resolves conflicts)
- Link to Galaxy notes: Physical-World Interface, 6-Fold Symmetry (if applicable)
- If this is the first /arch run for a project, establish the baseline and set Review #1
- Solo engineer context: sync "meetings" may be internal reviews — still valuable for forcing interface decisions
