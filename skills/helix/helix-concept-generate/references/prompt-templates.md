# S1 Prompt Templates — Phase 2 Conceptual Design (Mega-Skill)

Source: `3_Resources/SOPs/S1_prompt_library.md` v5.2
AI-Orchestration: S1 (Schema v3.0) · S3 (QC Gate) · S5 (Audit Trail)

## Applicable P-Templates

| P# | Name | When to Use in Phase 2 | Block |
|----|------|----------------------|-------|
| P01 | Structured Defense Task Delegation | Master template cho ALL Phase 2 sub-tasks | ALL |
| P02 | Defense AI QC Review Gate | MANDATORY on morphological matrix + VDI 2225 + firming up | E1 |
| P03 | Engineering Document Generation | Concept documentation, handoff package | E4 |
| P05 | Physics Plausibility Check | Verify working principles physically valid | B1, C2 |
| P06 | Context Window Scoping | When morphological matrix > 8 sub-functions | B3 |
| P08 | Procurement Narrative Draft | When presenting concept to military stakeholder | E3 |

## P02 QC Check (MANDATORY — Run at Block E1)

Run before presenting concepts to CEO:

```
CHECK 1 — COHERENCE: Do concept combinations form physically compatible systems?     [PASS/FAIL]
  Verify: 8-type compatibility (energy, geometric, material, signal, temporal, environmental, manufacturing, supply chain)
  Evidence: Compatibility matrix from Step B4

CHECK 2 — STANDARDS: Are referenced solution principles based on real standards/papers? [PASS/FAIL]
  Verify: Each WP has source citation (M1-M7 method + specific reference)
  Evidence: Working principles search table from Step B1

CHECK 3 — ENVIRONMENT: Do concepts work in Vietnam conditions?                        [PASS/FAIL]
  Verify: MIL-STD-810 tropical (25-45°C, 40-100% humidity, salt air)
  Evidence: Environmental compatibility in Step B4

CHECK 4 — SAFETY: Any safety-critical sub-function changes?                           [PASS/FAIL]
  Verify: CFMA SFD scores for safety-related functions (Step D4)
  Evidence: Rev-SFD < 80 for all safety functions

CHECK 5 — CONFIDENCE: VDI 2225 scores justified? Weight sources documented?            [PASS/FAIL]
  Verify: Weights traced to ODI/requirements (Step C3)
  Evidence: Sensitivity analysis shows ranking robust (Step D5)
```

**Rule:** If ANY check = FAIL → fix before CEO presentation. No exceptions.
**S3 Compliance:** P02 output MUST appear in final deliverable as Block E1.

## P05 Physics Plausibility (Apply at Steps B1 and C2)

For each working principle and firming-up calculation:

```
1. UNIT CONSISTENCY — all units match across interfaces?
2. ORDER OF MAGNITUDE — values within physically reasonable range?
3. BOUNDARY CONDITIONS — behavior at extremes (0, max, failure)?
4. ENERGY/MOMENTUM CONSERVATION — no free energy claims?
5. ENVIRONMENTAL ADJUSTMENT — Vietnam 25-45°C, 40-100% humidity, salt spray
```

**Rule:** UNCERTAIN on safety-critical values → treat as FAIL.

## P06 Context Window Scoping (Apply at Step B3)

When morphological matrix has > 8 sub-functions:

```
CHUNKING STRATEGY:
  Option A: Group by domain (Mechanical SFs → Electrical SFs → AI SFs)
  Option B: Group by flow (Energy chain → Material chain → Signal chain)
  Option C: Focus on solution-determining SF + 2 nearest neighbors

Present A/B/C options to user before processing.
Mandatory checkpoint saves between chunks.
```

## Schema v3.0 Fields for Phase 2 Tasks

```yaml
TASK: [pre-flight / search WP / morphological matrix / pugh screening / firm up / VDI 2225 / TRIZ improve / coupling / CFMA / sensitivity / CEO selection]
CONTEXT: Product={{name}}, Phase=2, Design_Type=[Original/Adaptive/Variant], Block=[0/A/B/C/D/E]
CONSTRAINTS:
  hard_limits:
    - ≥3 concept variants
    - ACH column mandatory in morphological matrix
    - VDI 2225 threshold ≥ 0.6
    - P02 QC gate must PASS
    - Human-sourced (H) principles required
    - Firming up before VDI scoring
  reject_conditions:
    - Function structure unavailable
    - Requirements not D/W classified
    - Single concept submission
    - Auto-selecting winner
    - Skipping P02 QC gate
  prohibited_actions:
    - Select concept for CEO
    - Omit coupling analysis
    - Use gut-feel weights when ODI exists
    - Omit ACH column
    - Score vague/unfirmed concepts
TOOLS_ALLOWED: [Read, Grep, Glob, WebSearch]
HITL_CHECKPOINT:
  essential_problem: "CEO approves before morphological matrix (Block A)"
  human_creative_input: "CEO adds novel WPs (Step B6)"
  concept_selection: "IMMEDIATE — CEO decides (Step E3)"
  assumption_register: true
  triz_improvement: true
SAFETY_OVERRIDE: "Safety-critical sub-function → Level 2+ fallback required"
SUCCESS_CRITERIA:
  pre_flight_pass: true
  solution_determining_sf_identified: true
  morphological_matrix_complete: true
  minimum_3_concepts: true
  pugh_screening_done: true
  firming_up_done: true
  vdi_2225_8_steps: true
  weak_spot_analysis: true
  coupling_analysis: true
  p02_qc_pass: true
  ceo_selects: true
FALLBACK_PROTOCOL:
  spec_ambiguous: "List ALL interpretations — ASK CEO"
  hardware_mismatch: "Suggest VN-manufacturable alternatives"
  vdi_ranking_sensitive: "Flag [RANKING-SENSITIVE to Cx]"
  coupling_too_high: "Suggest concept simplification"
  firming_up_insufficient: "Identify data gaps; propose experiments"
  unknown_error: "SAFE_STATE — save [INCOMPLETE]; halt"
EXECUTION_META:
  VERSION: "helix-concept-generate v3.0 (mega-skill)"
  LOG_LEVEL: "detailed"
```

## P-Template Integration Points by Block

| Block | Step | P-Template | Trigger |
|-------|------|-----------|---------|
| 0 | Pre-Flight | P01 | Task delegation for input verification |
| A | A1 (Solution-Determining SF) | P05 | Physics check on SF cascade analysis |
| A | A2 (TRIZ) | P01 | Structured delegation of contradiction analysis |
| B | B1 (WP Search) | P01, P05 | Task delegation + physics plausibility per WP |
| B | B3 (Morphological Matrix) | P06 | Context scoping if >8 SFs |
| C | C2 (Firming Up) | P05 | Physics plausibility on rough calculations |
| C | C4 (VDI 2225) | P01 | Structured evaluation delegation |
| D | D4 (CFMA) | P01 | Structured CFMA generation |
| E | E1 (QC Gate) | **P02** | **MANDATORY** — 5-check quality gate |
| E | E3 (CEO Selection) | P08 | Procurement narrative if military stakeholder |
| E | E4 (Handoff) | P03 | Engineering document generation for deliverables |
