Track and manage Interface Control Documents and integration debt across subsystems.

Usage: /icd [project_name] OR provide details interactively.

1. If $ARGUMENTS provided, use as project name; otherwise ask:
   - What project? (project code or name)
   - Which subsystems or interfaces are you tracking?

2. Read project artifacts:
   - `1_Projects/{{project}}/Status.md`
   - Phase 3 ICD document (if exists)
   - System architecture document

3. Generate or update the ICD tracker:

```
# INTERFACE CONTROL TRACKER — {{project}}
**Date:** {{today}}  |  **Total Interfaces:** {{N}}  |  **Resolved:** {{N}}  |  **TBD:** {{N}}

---

## INTERFACE MATRIX

| IF# | From | To | Type | Status | Owner | TBD Items | Risk |
|-----|------|----|------|--------|-------|-----------|------|
| IF-001 | Subsystem A | Subsystem B | Mech/Elec/SW/Data | Defined/TBD/Conflict | {{who}} | {{count}} | H/M/L |

### Interface Types:
- **Mech**: Physical mounting, alignment, envelope, thermal
- **Elec**: Power, signal, connector, pinout, protocol
- **SW**: API, data format, timing, version
- **Data**: Units, coordinate frames, update rates

---

## INTEGRATION DEBT

| # | Debt Item | Interface | Impact | Effort to Resolve | Priority |
|---|-----------|-----------|--------|-------------------|----------|
| 1 | {{TBD or assumption}} | IF-xxx | H/M/L | Hours/Days | Now/Soon/Later |

**Total integration debt:** {{count}} items
**Critical debt (blocking build):** {{count}} items

---

## INTERFACE RISK HEAT MAP

|           | Sub-A | Sub-B | Sub-C | Sub-D |
|-----------|-------|-------|-------|-------|
| **Sub-A** |   —   |  G/Y/R |  G/Y/R |  G/Y/R |
| **Sub-B** |       |   —   |  G/Y/R |  G/Y/R |
| **Sub-C** |       |       |   —   |  G/Y/R |
| **Sub-D** |       |       |       |   —   |

G = Green (defined, no TBDs)
Y = Yellow (defined, minor TBDs)
R = Red (TBDs or conflicts blocking integration)

---

## ACTIONS NEEDED
| # | Action | Interface | Owner | Deadline |
|---|--------|-----------|-------|----------|
```

4. Present tracker to user. Save to:
   `1_Projects/{{project}}/Phase3-Embodiment/{{PROJECT_NAME}}_ICD_Tracker_v1.0.md`

RULES:
- Every subsystem pair must have an explicit interface entry -- even if "no interface"
- TBD items are integration DEBT -- they must be tracked and resolved before build
- Interface ownership must be assigned -- unowned interfaces are the #1 integration failure mode
- COD: Offload (AI tracks, CEO resolves conflicts and assigns ownership)
- Update this tracker at every design review session
