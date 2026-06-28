---
name: helix-quality-gate
description: Run quality gate reviews for Pahl-Beitz phase transitions (Gate 1 through Gate 4). This skill should be used when the user asks "quality gate", "phase gate", "gate review", "ready for next phase?", "gate 1/2/3/4", or wants to assess if a project can transition between design phases. Provides both auto-check and human judgment items.
---

# Helix Quality Gate — Phase Transition Review

Run the formal gate review for Pahl-Beitz phase transitions. Each gate has auto-check items (AI verifies from project files) and human judgment items (CEO decides). Scores /4.0 with PASS/CONDITIONAL PASS/REVISE/FAIL decision.

## When to Use

- Project approaching end of current phase
- User asks "ready for Phase X?" or "gate review"
- After helix-sync-protocol identifies gate-ready project
- Monthly dashboard flags a project nearing phase boundary
- VN-XUONG-UUV Gate 2 REVISE follow-up checks

## Gate Checklists

### Gate 1: Phase 1 (Task Clarification) to Phase 2 (Conceptual Design)

**Auto-Check:** A1: Reqs count >= 40 (count rows) | A2: D-reqs have test method (scan column) | A3: 6-flow function structure exists (file check) | A4: Cross-domain reqs aligned (no contradictions) | A5: Stakeholder needs in _Project_Brief.md | A6: W-requirements (constraints) identified | A7: PD-requirements have degradation bounds and test sample sizes

**Cross-Domain Sync Check:** S1: Are Mech/Elec/AI domain requirements documented separately? | S2: Are interface requirements identified for all domain boundaries? | S3: Any conflicting assumptions between domains? | S4: ICD v1 updated with requirements allocation?

**Human Judgment:** H1: "Is THIS the right problem to solve?" | H2: "Will Vietnamese MoD buy this?" | H3: "Do we have skills to proceed?"

### Gate 2: Phase 2 (Conceptual) to Phase 3 (Embodiment Design)

**Auto-Check:** A1: >= 3 concepts evaluated | A2: VDI 2225 scoring complete (all cells filled) | A3: Sensitivity analysis done | A4: Coupling/compatibility analysis cross-checked | A5: Selected concept documented in Status.md | A6: ICD draft exists for all 4 IF categories | A7: TRIZ contradictions identified? (if HOQ/ODI exists with (-) contradictions → must be addressed; if no HOQ → CEO waiver acceptable) | A8: Innovation level assessed? (avg ≥ 1.5 recommended; if < 1.5 → WARNING "concept may lack competitive differentiation") | A9: CFMA completed for selected concept? (no function with Rev-SFD ≥ 80)

**Cross-Domain Sync Check:** S1: All domain concept variants compatible with selected system concept? | S2: ICD v2 reflects chosen concept's interface topology? | S3: Shadow assumptions between domains documented? | S4: Clock speed mismatch between domains flagged (AI sprints vs. Mech gates)?

**Human Judgment:** H1: "Does AI give us unfair advantage here?" (ACH) | H2: "Can we build this in Vietnam?" | H3: "What kills us if this fails?"

### Gate 3: Phase 3 (Embodiment) to Phase 4 (Detail Design)

**Auto-Check:** A1: 0 critical DfX issues open | A2: >= 80% ICD frozen | A3: Integration debt trend decreasing | A4: **Geometry-of-record complete** — every fabricable part has a CEO-certified geometry-of-record row in ICD v3 (STEP from helix-cad-bridge OR cad_extract.json from helix-cad-ingest, incl. human-drawn imports); 0 uncertified, 0 missing (BOM-vs-geometry orphans = FAIL) | A5: BOM draft with suppliers | A6: Weight/stability check passed | A7: DfU items DfU-06 to DfU-09 all OK/WARN (no FAIL)

**Cross-Domain Sync Check:** S1: Mech/Elec/AI domain states synchronized (no domain >1 phase behind)? | S2: ICD v3 versions aligned across all domains? | S3: Shadow assumptions validated at last sync point? | S4: AI team testing on real hardware data (not synthetic)?

**Human Judgment:** H1: "Thầy workshop xác nhận: gia công được?" | H2: "Ngân sách đủ cho Phase 4 + prototype?" | H3: "Linh kiện critical có nguồn chưa?"

### Gate 4: Phase 4 (Detail) to Manufacturing/Prototype

**Auto-Check:** A1: All drawings complete (DXF/PDF vs BOM count) AND each drawing traces to a CEO-certified geometry-of-record (STEP `.py` source from helix-cad-bridge, or imported cad_extract.json) — no orphan drawings | A2: BOM final with part numbers | A3: Inspection checklist exists (critical-dim acceptance seeded from the geometry-of-record cad_extract / drawing) | A4: Integration debt = 0 | A5: All ICD frozen (100%, incl. geometry-of-record registry) | A6: Test plan with acceptance criteria | A7: DfU lifecycle document complete (update, rollback, monitoring procedures)

**Cross-Domain Sync Check:** S1: All domains confirm "ready for prototype" independently? | S2: Integration test plan covers all ICD interfaces? | S3: No unresolved cross-domain assumptions remaining? | S4: OTA/update pipeline tested end-to-end (if ACH product)?

**Human Judgment:** H1: "Vật tư đã mua/đặt hàng chưa?" | H2: "Lịch gia công đã xếp chưa?" | H3: "Chế tạo — GO hay NO-GO?"

## Workflow

### Step 1: Identify Gate

Determine which gate to run based on project phase in Status.md.

### Step 2: Run Auto-Checks

For each auto-check item:
1. Read the source file(s)
2. Apply the check logic
3. Score: PASS / FAIL / CONDITIONAL (partial evidence)
4. Record evidence found or evidence missing

### Step 2b: P02 Content Quality Check (from S1 Prompt Library + Defense QC Checklist)

After file-existence checks (Step 2), run P02 5-check sequence on gate-critical artifacts:

```
P02 CONTENT QUALITY — {{project_id}} Gate {{N}}

Target artifacts: [requirements list / concept evaluation / embodiment layout / manufacturing package]

CHECK 1: PHYSICS PLAUSIBILITY
  Are all numerical values in artifacts within physically plausible ranges?
  Product-specific: {{range_limit / velocity_limit / energy_limit}}
  Flag if: value exceeds theoretical maximum OR is suspiciously round
  → PASS / REVISE / REJECT

CHECK 2: STANDARD COMPLIANCE
  Do artifacts comply with applicable standards (MIL-STD, TCVN, STANAG)?
  Flag if: standard cited but not verified, or required standard absent
  → PASS / REVISE / REJECT

CHECK 3: ENVIRONMENTAL VALIDITY
  Are Vietnam operating conditions accounted for?
  (heat 25-55°C, humidity 40-100%, salt air, tropical rain)
  Flag if: artifacts assume ideal/lab conditions
  → PASS / REVISE / REJECT

CHECK 4: SAFETY FLAG
  Do artifacts involve engagement decisions, target classification, weapon parameters?
  If YES: flag for human review regardless of confidence score
  → PASS / REVISE / REJECT

CHECK 5: CONFIDENCE CALIBRATION
  Are AI-generated values justified by evidence quality?
  Flag if: high precision claimed with low-confidence inputs ([L4]/[L5] data)
  → PASS / REVISE / REJECT

P02 VERDICT: [ALL PASS → proceed to H-items / ANY REJECT → gate blocked]
```

This supplements the file-existence auto-checks with content quality assessment. If P02 finds REJECT on any check, the artifact must be revised before gate can pass.

### Step 3: Present Human Judgment Items

List each H-item for CEO review. Do NOT pre-fill answers — wait for human input.

### Step 4: Calculate Score and Decision

```
GATE {{N}} REVIEW — {{Project}}
Date: {{date}}
Phase: {{current}} to {{next}}

--- Auto-Check Results ---
| # | Item | Result | Evidence |
|---|------|--------|----------|
| A1 | | PASS/FAIL/COND | |
| A2 | | PASS/FAIL/COND | |
...

--- Human Judgment ---
| # | Item | CEO Decision | Notes |
|---|------|-------------|-------|
| H1 | | PASS/FAIL | |
| H2 | | PASS/FAIL | |
| H3 | | PASS/FAIL | |

--- Scoring ---
Auto-check score: __/__ items passed
Human judgment: __/__ items passed
Overall score: __/4.0

--- Blockers ---
| # | Blocker | Owner | Resolution Path | Deadline |
|---|---------|-------|----------------|----------|
| | | | | |

--- Decision ---
[ ] PASS (score >= 3.5, no FAIL on H-items)
[ ] CONDITIONAL PASS (score >= 3.0, conditions listed)
[ ] REVISE (score >= 2.5, specific revisions required)
[ ] FAIL (score < 2.5 or any critical blocker)

Conditions/Revisions Required:
1.
2.
```

### Step 5: Record and Distribute

1. Save gate review to `1_Projects/{{project}}/VnV/Gate{{N}}_Review_{{date}}.md`
2. Update Status.md with gate result
3. Feed result to helix-sync-protocol and bridge-knowledge-base

## Integration

```
helix-quality-gate READS FROM:
  - helix-integration-debt → ICD status, debt count
  - helix-6flow-mapper → function structure completeness
  - helix-design-journal → design decisions for traceability
  - 1_Projects/*/Phase*/ → all phase artifacts
  - 1_Projects/*/Status.md → current phase

helix-quality-gate WRITES TO:
  - 1_Projects/*/VnV/ → gate review document
  - 1_Projects/*/Status.md → gate result + score
  - helix-sync-protocol → gate result for next sync
  - bridge-knowledge-base → Layer 2 gate documentation
```

## Step 2c: PLAUSIBLE Review Protocol (from Pattern Library A3)

After P02 content quality checks, run PLAUSIBLE on ALL AI-generated gate artifacts. This is the defense-grade AI output validation layer.

```
PLAUSIBLE REVIEW — {{project_id}} Gate {{N}}
Target: ALL AI-generated artifacts entering this gate

P — PHYSICS: Does it obey physical laws in THIS environment?
    Check: forces, energy, thermal, acoustic — product-specific
    Vietnam: 25-55°C, 40-100% humidity, salt air, tropical rain
    Flag if: value exceeds theoretical maximum OR defies conservation laws
    → PASS / FLAG / REJECT

L — LOGIC: Does the reasoning chain hold end-to-end?
    Check: if A→B→C claimed, verify each link has evidence
    Flag if: conclusion jumps, circular reasoning, unstated premises
    → PASS / FLAG / REJECT

A — ASSUMPTIONS: List ALL hidden assumptions found
    Check: every "assume X" statement — is X validated or guessed?
    Vietnam-specific: manufacturing capability, supply chain, military doctrine
    Flag if: critical assumption has no evidence path
    → PASS / FLAG / REJECT

U — UNITS: Are all units consistent throughout?
    Check: m/mm/cm, degrees/mils/radians, kg/N, °C/°F
    Flag if: unit mismatch found anywhere, even in comments
    → PASS / FLAG / REJECT

S — SCALE: Does it work at 0.1× and 10× expected conditions?
    Check: what happens at min/max operating envelope?
    Flag if: performance degrades non-linearly without explanation
    → PASS / FLAG / REJECT

I — INTEGRATION: Compatible with rest of the system?
    Check: ICD compliance, CDM pattern, domain interfaces
    Flag if: artifact assumes interface not in ICD
    → PASS / FLAG / REJECT

B — BOUNDARY: What happens at min/max/zero/null?
    Check: edge cases, empty inputs, saturation, timeout
    Flag if: no boundary behavior documented
    → PASS / FLAG / REJECT

L — LETHALITY: If WRONG, could someone get hurt?
    Check: engagement decisions, target classification, weapon parameters
    Flag if: ANY safety-critical path without human override
    → PASS / FLAG / REJECT (REJECT = gate blocked)

E — ENDURANCE: Will it still work in 2 years?
    Check: component obsolescence, calibration drift, software rot
    Flag if: design depends on single-source or EOL component
    → PASS / FLAG / REJECT

PLAUSIBLE VERDICT:
  PASS count: __/9
  FLAG count: __/9 (items needing CEO attention)
  REJECT count: __/9 (gate blockers)

  ANY REJECT → Gate blocked until resolved
  ANY FLAG → CEO reviews before gate proceeds
  ALL PASS → Proceed to H-items
```

**When to apply PLAUSIBLE:** Run on AI-generated content only (not CEO-written artifacts). Typical targets: requirements lists, concept evaluations, BOM estimates, stability calculations, DfX reviews.

**Interaction with P02:** P02 checks content quality (5 checks). PLAUSIBLE checks AI output integrity (9 checks). Both must pass before human judgment items are presented.

## VDI 2206 Checkpoint Mapping

The 6 VDI 2206:2021 checkpoints map to HELIX pipeline as follows:

| VDI 2206 Checkpoint | HELIX Equivalent | When |
|---------------------|-----------------|------|
| CP1: Specification | Gate 1 (Phase 1→2) + system-arch SA6 | Requirements + architecture complete |
| CP2: System Design | system-arch SA6 review | Domain allocation + ICD v1 frozen |
| CP3: Domain Design | Gate 2 (Phase 2→3) | Concept selected, domain WPs chosen |
| CP4: Integration | Phase 3 BC (ICD v3 freeze) | Cross-domain integration verified |
| CP5: Verification | Gate 3 (Phase 3→4) | Embodiment evaluated (Rt/Re) |
| CP6: Validation | Gate 4 (Phase 4→prototype) | Manufacturing-ready, field test planned |

**Note:** VDI 2206 checkpoints are "substantive guidance, not rigid gates" (Graessler 2020). Our Gate 1-4 are more formal (scored). The `--checkpoint` mode provides the lightweight VDI 2206-style check.

**NLM Reference:** `Research: VDI 2206 V-Model Mechatronic CPS` (16 sources, notebook `3856a428`)

## Gotchas (from production use)

1. **PLAUSIBLE only on AI-generated artifacts** — Do NOT run on CEO-written documents. PLAUSIBLE checks AI hallucination risk, not human judgment quality. (Source: Session 52 upgrade)
2. **P02 CHECK 5 (Confidence Calibration) catches false precision** — If AI claims "tensile strength = 19.29 MPa" but source is [L5: ASSUMPTION] → FLAG. High precision + low confidence = dangerous. (Source: HDPE research)
3. **Gate 0 H-items can be deferred** — VN-USV-SS-001 Gate 0 got CONDITIONAL PASS with H-items deferred. Acceptable for Phase 0→1 transition. NOT acceptable for Gate 2+. (Source: Session 52 Gate 0 review)
4. **REVISE ≠ FAIL** — VN-XUONG Gate 2 was REVISE (2.75/4.0) with specific revision items R1-R4. Track revisions with deadlines. REVISE means "fix these, then re-review" not "start over." (Source: VN-XUONG precedent)
5. **Cross-domain sync checks are SEPARATE from auto-checks** — S-items verify domain alignment (Mech/Elec/AI). Passing all A-items but failing S-items = integration surprise in next phase. (Source: HELIX v3 upgrade)

## Checkpoints vs Gates (VDI 2221:2019 + VDI 2206:2021)

VDI 2221:2019 and the updated VDI 2206 V-Model introduce a distinction between **checkpoints** and **gates** that the HELIX pipeline implements:

### Gates (Formal Phase Transitions)
- **Gate 1-4** in this skill = formal phase transitions
- Require auto-checks (A-items) + human judgment (H-items) + cross-domain sync (S-items)
- Score-based decision: PASS / CONDITIONAL / REVISE / FAIL
- Gates are project-management milestones that mark phase completion

### Checkpoints (Lightweight Quality Controls)
- **CEO checkpoints after each pipeline block** = VDI 2221:2019 checkpoints
- Lightweight: 1-3 bullet summary + CEO approve/adjust/halt
- No formal scoring — binary proceed/adjust decision
- Checkpoints decouple engineering logic from project organization (VDI 2206:2021)
- Checkpoints are compatible with agile project management

### Assurance (Eigenschaftsabsicherung — VDI 2221:2019)
VDI 2221:2019 groups Verification and Validation under a unified concept: **Assurance** (Eigenschaftsabsicherung). In HELIX:
- **PLAUSIBLE 9-check** = AI output assurance (verification of AI-generated content)
- **P02 5-check** = content quality assurance (verification of artifact quality)
- **CEO judgment H-items** = validation (does the product meet stakeholder needs?)
- **Cross-domain S-items** = integration assurance (domains aligned?)

Assurance is continuous throughout the pipeline (via checkpoints), not just at phase-end gates.

### --checkpoint Mode
For mid-phase quality reviews without full gate formality:
```
/helix-quality-gate {{project}} --checkpoint
```
Runs P02 + PLAUSIBLE on current phase artifacts without A-items, H-items, or scoring. Outputs a health check, not a gate decision. Useful for:
- Mid-sprint confidence check
- Pre-sync preparation
- CEO peace of mind between gates

**NLM Reference:** `Research: VDI 2221 Systematic Design (1986→2019)` (27 sources, notebook `f6e2b21f`)

## Rules

- NEVER auto-pass a gate — human judgment items require CEO input
- Any H-item FAIL = overall cannot be PASS (max CONDITIONAL)
- Score < 2.5 with critical blocker = automatic FAIL
- Gate results are permanent records — never delete, only append
- If gate result is REVISE, specific revision items must be listed with deadlines
- VN-XUONG-UUV precedent: Gate 2 REVISE (2.75/4.0) — revisions R1-R4 tracked
- **MANDATORY:** Run PLAUSIBLE 9-check on ALL AI-generated gate artifacts. Output MUST contain "PLAUSIBLE" section with P/L/A/U/S/I/B/L/E checks.
- **MANDATORY:** For multi-domain products, include S-items (cross-domain sync) in gate output. State domain synchronization status explicitly.
- PLAUSIBLE REJECT on any check = gate blocked (same as A-item FAIL)
- PLAUSIBLE FLAG items require CEO review before H-items presented
- Reference: [[Design Space Collapse — Khi Chỉ Còn Một Concept]]

## COD Classification

- Auto-check execution: Offload (O1) — AI scans files, applies rules
- Score calculation: Offload (O1) — deterministic formula
- Human judgment items: **Core (C)** — CEO decides PASS/FAIL per item
- GO/NO-GO decision: **Core (C)** — CEO accountable for phase transition
- Gate documentation: Offload (O1) — AI formats and stores
- Blocker resolution planning: Offload (O2) — AI proposes, CEO approves
