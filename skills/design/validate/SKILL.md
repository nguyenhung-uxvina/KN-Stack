Design a validation plan for a product, subsystem, or design assumption.

Usage: /validate [target] OR provide details interactively.

1. If $ARGUMENTS provided, use as validation target; otherwise ask:
   - What are you validating? Options:
     a) A full product (generate V&V plan)
     b) A specific subsystem or component
     c) A design assumption or hypothesis
     d) A physical prototype test
   - What project does this belong to?
   - What phase are you in? (affects validation depth)

2. Read relevant project artifacts:
   - Requirements list (what must be verified)
   - Status.md (current phase, existing test plans)
   - Any existing VnV documents in the project's VnV/ folder

3. Generate the validation plan:

```
# VALIDATION PLAN — {{target}}
**Project:** {{project}}  |  **Date:** {{today}}  |  **Phase:** {{phase}}

---

## 1. VALIDATION OBJECTIVES
{{What questions does this validation answer?}}
{{What decisions depend on the results?}}

---

## 2. REQUIREMENTS TRACEABILITY

| Req ID | Requirement | Verification Method | Pass Criteria | Priority |
|--------|-------------|-------------------|---------------|----------|
| | | I/A/D/T | | H/M/L |

**Verification Methods:**
- **I** = Inspection (visual, dimensional)
- **A** = Analysis (calculation, simulation)
- **D** = Demonstration (functional test, show it works)
- **T** = Test (measured against quantitative criteria)

---

## 3. TEST MATRIX

| Test # | Test Name | Type | Setup | Measurements | Pass/Fail Criteria | Duration | Cost Est. |
|--------|-----------|------|-------|-------------|-------------------|----------|-----------|

---

## 4. TEST INFRASTRUCTURE

### Equipment Required
| Item | Available? | Source | Lead Time | Cost |
|------|-----------|--------|-----------|------|

### Test Fixtures / Jigs
| Fixture | Description | Reusable? | Design Needed? |
|---------|------------|-----------|---------------|

### Instrumentation
| Instrument | Specification | Available? |
|-----------|--------------|-----------|

---

## 5. GO/NO-GO CRITERIA
| # | Criterion | Threshold | Rationale |
|---|----------|-----------|-----------|
| GO-1 | | | |
| GO-2 | | | |

**Decision rule:** ALL Go criteria must pass. Any FAIL → redesign or scope change.

---

## 6. SCHEDULE
| Phase | Activity | Duration | Dependencies |
|-------|----------|----------|-------------|
| Prep | Procure + build test setup | | |
| Execute | Run tests | | |
| Analyze | Process results | | |
| Decide | Go/No-Go review | | |

**Total validation timeline:** {{days/weeks}}
**Critical path item:** {{longest lead time item}}

---

## 7. RISK TO VALIDATION
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Equipment delay | Schedule slip | Order early, identify alternatives |
| Test failure | Redesign needed | Define fallback approach |

---

## 8. DATA CAPTURE PLAN
- What data to record (measurements, photos, video)
- Data format and storage location
- Who reviews results (CEO = Core decision)
```

4. Present plan to user for review. Do NOT auto-execute.
5. Save to `1_Projects/{{project}}/VnV/{{PROJECT_NAME}}_Validation_Plan_{{target}}_v1.0.md`

RULES:
- Every Demand requirement needs a verification method — flag gaps
- Physical tests are ALWAYS preferred over analysis alone (Physical-World Interface principle)
- Go/No-Go criteria must be QUANTITATIVE — "works well" is not acceptable
- Test infrastructure must be assessed for availability — don't assume equipment exists
- COD: Offload (AI designs plan, CEO decides on scope and budget)
- For Tier 1 projects: validation plan must fit within 30-day physical gate
- Reusable test fixtures are preferred (amortize across products)
- Link to existing test plans (e.g., Doc 014 magnetic brake test for VN-12.7MM-SIM)
