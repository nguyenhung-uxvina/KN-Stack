---
name: helix-domain-debate
description: Structured 3-domain perspective analysis for cross-domain design questions. Not a standalone pipeline — a method-skill callable by helix-p2-risk (BD coupling), helix-p2-search (BB WP search), helix-p2-develop (BC DQM), helix-p3-integrate (ICD freeze), and reverse-engineering (S2B/S3). Outputs both markdown (CEO-readable) and JSON side-car (machine-readable for downstream blocks). Triggers on "domain debate", "multi-perspective", "3 domain lens", "cross-domain analysis", "Mech vs Elec vs SW", "coupling debate", or "domain perspective". Based on research: Hierarchical Hub Resilience Law + SBCE-Agent Mapping Law + Multi-Agent Selectivity Law.
---

# Helix Domain Debate — Structured 3-Domain Perspective Analysis

A method-skill that runs structured multi-perspective analysis from 3 domain viewpoints (Mechanical, Electrical, AI/Software), then surfaces contradictions and synthesizes a unified recommendation. Called WITHIN other block-skills, not as a standalone pipeline step.

**Research basis:** Multi-Agent Collaborative Conceptual Design (2026-04-22, NLM: multi-agent-design). Key laws: Hierarchical Hub Resilience (CEO-Hub optimal), SBCE-Agent Mapping (parallel set exploration), Multi-Agent Selectivity (only for coupled problems), Cascading Hallucination Trap (contradiction detection mandatory).

## When to Use

- helix-p2-search (BB): multi-perspective WP search for solution-determining SFs
- helix-p2-risk (BD Step D1): cross-domain coupling analysis
- helix-p2-develop (BC): domain-specific criterion estimation for DQM
- helix-p3-integrate: ICD freeze cross-domain validation
- reverse-engineering (S2B): domain-parallel function structure extraction
- Any design question where Mech × Elec × AI/SW coupling is uncertain

## When NOT to Use (Multi-Agent Selectivity Law)

- B0 (Preflight): simple validation, no coupling
- BE (Select): CEO decision, non-delegable
- GREEN complexity SFs: WX has prior art, single agent sufficient
- Detail calculations: 1 expert + verification > debate
- Time-critical decisions: overhead > benefit

## Protocol

### Step 1: Frame the Question

```
DOMAIN DEBATE — {{calling block}} / {{project}}
Date: {{today}}

DESIGN QUESTION: {{specific question requiring cross-domain perspective}}
CONTEXT: {{what's already decided, constraints, dependencies}}
CALLING SKILL: {{helix-p2-risk D1 / helix-p2-search B1 / etc.}}
```

### Step 2: Three Domain Perspectives (Sequential — same turn)

Each perspective uses WX-specific domain knowledge, NOT generic engineering.

```
═══ MECHANICAL PERSPECTIVE ═══
(As WX mechanical specialist with composite layup, CNC Al 6061, towed target + target drone experience, VN tropical maritime environment)

Assessment: {{domain-specific analysis of the question}}
Concerns: {{what worries a mechanical engineer about this}}
Preferred approach: {{what mechanical domain would choose}}
Constraints flagged: {{manufacturing, material, thermal, structural limits}}
Confidence: H/M/L

═══ ELECTRICAL PERSPECTIVE ═══
(As WX electronics specialist with BLDC motor control, ESC, ArduPilot FC, sensor integration, power management, EMC experience)

Assessment: {{domain-specific analysis}}
Concerns: {{EMI, power budget, thermal, signal integrity, component availability}}
Preferred approach: {{what electrical domain would choose}}
Constraints flagged: {{power, EMC, component sourcing, ITAR-free}}
Confidence: H/M/L

═══ AI/SOFTWARE PERSPECTIVE ═══
(As WX embedded AI/SW specialist with ArduPilot, sensor fusion, control algorithms, real-time embedded systems, Python/C++ experience)

Assessment: {{domain-specific analysis}}
Concerns: {{latency, compute budget, algorithm complexity, data availability, update lifecycle}}
Preferred approach: {{what SW domain would choose}}
Constraints flagged: {{real-time constraints, memory, processor capability, ArduPilot limitations}}
Confidence: H/M/L
```

### Step 3: Contradiction Detection (MANDATORY — Cascading Hallucination Trap mitigation)

```
═══ CONTRADICTION TABLE ═══

| # | Topic | Mech Says | Elec Says | AI/SW Says | Severity | Resolution |
|---|-------|-----------|-----------|-----------|----------|-----------|
| 1 | {{topic}} | {{position}} | {{position}} | {{position}} | CRITICAL/MODERATE/MINOR | {{who's right + why}} |

AGREEMENTS (all 3 domains align):
- {{consensus point 1}}
- {{consensus point 2}}

UNRESOLVED CONFLICTS (CEO must decide):
- {{conflict}} — Mech vs Elec: {{trade-off description}}
```

### Step 4: Synthesis + Recommendation

```
═══ SYNTHESIS ═══

INTEGRATED RECOMMENDATION: {{unified position that addresses all 3 domains}}

TRADE-OFFS ACCEPTED:
| Trade-off | Favors | Costs | CEO Rationale Needed? |
|-----------|--------|-------|---------------------|

RISK IF WRONG: {{what happens if synthesis is incorrect}}

CONFIDENCE: H/M/L (overall)
  - Mech: {{H/M/L}}
  - Elec: {{H/M/L}}
  - AI/SW: {{H/M/L}}
  - Cross-domain: {{H/M/L}} (usually lowest)
```

### Step 4.5: JSON Side-Car (MANDATORY — machine-readable output for downstream blocks)

After the markdown synthesis, emit a JSON code block with standardized schema. This enables downstream blocks (BB, BC, BD, RE) to parse structured data instead of extracting from prose.

**The JSON block is appended INSIDE the same markdown output, after Step 4 synthesis.**

````
```json:domain-debate-sidecar
{
  "metadata": {
    "calling_block": "{{helix-p2-search BB / helix-p2-risk BD / etc.}}",
    "project": "{{project ID}}",
    "date": "{{YYYY-MM-DD}}",
    "question": "{{design question verbatim}}",
    "complexity": "{{AMBER / RED}}"
  },
  "perspectives": [
    {
      "domain": "MECH",
      "assessment": "{{1-2 sentence summary}}",
      "concerns": ["{{concern 1}}", "{{concern 2}}"],
      "preferred_approach": "{{what this domain would choose}}",
      "constraints": ["{{constraint 1}}", "{{constraint 2}}"],
      "confidence": "{{H/M/L}}",
      "wp_candidates": ["{{WP if BB context}}", "..."],
      "coupling_scores": {"ELEC": {{0-5}}, "AI_SW": {{0-5}}}
    },
    {
      "domain": "ELEC",
      "assessment": "...",
      "concerns": ["..."],
      "preferred_approach": "...",
      "constraints": ["..."],
      "confidence": "{{H/M/L}}",
      "wp_candidates": ["..."],
      "coupling_scores": {"MECH": {{0-5}}, "AI_SW": {{0-5}}}
    },
    {
      "domain": "AI_SW",
      "assessment": "...",
      "concerns": ["..."],
      "preferred_approach": "...",
      "constraints": ["..."],
      "confidence": "{{H/M/L}}",
      "wp_candidates": ["..."],
      "coupling_scores": {"MECH": {{0-5}}, "ELEC": {{0-5}}}
    }
  ],
  "contradictions": [
    {
      "id": "CON-{{N}}",
      "topic": "{{topic}}",
      "positions": {"MECH": "{{position}}", "ELEC": "{{position}}", "AI_SW": "{{position}}"},
      "severity": "{{CRITICAL / MODERATE / MINOR}}",
      "resolution": "{{who's right + why, or UNRESOLVED}}",
      "resolved": {{true/false}}
    }
  ],
  "agreements": ["{{consensus point 1}}", "{{consensus point 2}}"],
  "unresolved_for_ceo": [
    {
      "conflict": "{{description}}",
      "domains": ["MECH", "ELEC"],
      "trade_off": "{{what CEO must weigh}}"
    }
  ],
  "synthesis": {
    "recommendation": "{{unified position, 1-2 sentences}}",
    "trade_offs": [
      {"trade_off": "{{description}}", "favors": "{{domain}}", "costs": "{{what's sacrificed}}"}
    ],
    "risk_if_wrong": "{{consequence}}",
    "confidence": {
      "MECH": "{{H/M/L}}",
      "ELEC": "{{H/M/L}}",
      "AI_SW": "{{H/M/L}}",
      "cross_domain": "{{H/M/L}}",
      "overall": "{{H/M/L}}"
    }
  }
}
```
````

**Schema rules:**
- `wp_candidates`: populate ONLY when called from BB (WP search). Empty array `[]` otherwise.
- `coupling_scores`: populate ONLY when called from BD (coupling analysis). Omit key otherwise.
- All string values must be concise (< 100 chars). The markdown above has the full prose.
- `contradictions[].resolved: false` → entry MUST appear in `unresolved_for_ceo`.
- JSON must be valid — no trailing commas, no comments. Downstream blocks parse with standard JSON.

**How downstream blocks consume the side-car:**

| Calling Block | Reads From Side-Car | Uses For |
|---------------|-------------------|----------|
| BB (Search) | `perspectives[].wp_candidates` | Merge into unified morphological matrix, tag [HYB] for cross-domain |
| BB (Search) | `contradictions[].severity` | Flag incompatible WP combinations |
| BD (Risk) | `perspectives[].coupling_scores` | Build coupling matrix (3×3 domain scores) |
| BD (Risk) | `contradictions[]` where severity=CRITICAL | Input to CFMA as cross-domain failure modes |
| BC (Develop) | `perspectives[].constraints` | Domain-specific criterion bounds for DQM scoring |
| BC (Develop) | `synthesis.trade_offs` | Weight adjustment evidence for VDI 2225 |
| RE (S2B) | `perspectives[].preferred_approach` | Function-to-domain allocation in decomposition |
| P3 Integrate | `unresolved_for_ceo` | ICD freeze blockers requiring CEO arbitration |

### Step 5: Return to Calling Skill

Output appends to calling skill's output file. Does NOT create separate file.

```
[DOMAIN DEBATE COMPLETE — returned to {{calling block}}]
  Perspectives: 3/3
  Contradictions: {{N}} ({{critical}}/{{moderate}}/{{minor}})
  Unresolved for CEO: {{N}}
  Synthesis confidence: {{H/M/L}}
  Side-car: JSON emitted ✓ ({{N}} perspectives, {{N}} contradictions, {{N}} unresolved)
```

## WX Domain Knowledge Base (embed in perspectives)

### Mechanical — WX Context
- Materials: composite layup (glass/carbon), Al 6061-T6 CNC, HDPE, LW-PLA (prototype only)
- Processes: CNC milling, composite wet layup + vacuum bag, welding (Al 5083/6061), 3D print FDM
- Products: 550 towed targets, 200 target drones, VN-MGM (300), BB-01 (3), VN-AST (2)
- Environment: VN tropical maritime (25-45°C, >80% RH, salt spray, UV, monsoon)
- Standards: MIL-STD-810G environmental, ISO 2768 tolerances

### Electrical — WX Context
- Motors: BLDC (Emax, T-Motor), servos (PowerHD, GDW), ESCs (Emax Formula, Lumenier)
- Power: LiPo/Li-Ion 4S-6S, BEC, PDB, power monitoring
- Sensors: GPS (u-blox), compass, baro, IMU (MPU), pitot
- Control: ArduPilot (Matek/Holybro FC), PWM/DShot outputs
- EMC: MIL-STD-461G awareness, compass-motor isolation
- BB-01 signal chain: Piezo → Charge Amp → Bandpass → Gain → Clamp → ADC

### AI/Software — WX Context
- Autopilot: ArduPilot (Copter/Plane/QuadPlane/Rover)
- Languages: C++ (ArduPilot), Python (tools/scripts), Lua (ArduPilot scripting)
- Real-time: NuttX RTOS (ArduPilot base), FreeRTOS (peripheral MCUs)
- AI: edge inference considerations (CM4, Jetson Nano), ACH design principle
- Sim: Unity (VN-CUAV-SIM), Vega Prime (legacy naval sim)
- Data: MAVLink telemetry, dataflash logs, mission planner GCS

## Rules

1. **Three perspectives mandatory** — never skip a domain, even if "obviously" not relevant
2. **Contradiction table mandatory** — Cascading Hallucination Trap mitigation
3. **WX-specific prompts** — generic "as a mechanical engineer" is insufficient; use WX context above
4. **CEO resolves conflicts** — unresolved contradictions escalate to CEO checkpoint (Core)
5. **Append, don't replace** — output goes INTO calling skill's output, not separate file
6. **Selective application** — only use for AMBER/RED complexity SFs (Multi-Agent Selectivity Law)
7. **Cap at 3 perspectives** — communication overhead scales quadratically; do NOT add more domains
8. **Confidence must be per-domain AND cross-domain** — cross-domain is usually lowest

## Integration

```
helix-domain-debate IS CALLED BY:
  - helix-p2-search (BB): "Run /helix-domain-debate for solution-determining SF WP search"
    → Caller reads: wp_candidates, contradictions[].severity
  - helix-p2-risk (BD Step D1): "Run /helix-domain-debate for coupling analysis"
    → Caller reads: coupling_scores, contradictions[] where CRITICAL
  - helix-p2-develop (BC): "Run /helix-domain-debate for DQM criterion estimation" (ICDM only)
    → Caller reads: constraints, synthesis.trade_offs
  - helix-p3-integrate: "Run /helix-domain-debate for ICD freeze validation"
    → Caller reads: unresolved_for_ceo
  - reverse-engineering S2B: "Run /helix-domain-debate for function-domain allocation"
    → Caller reads: perspectives[].preferred_approach

helix-domain-debate READS:
  - Calling block's context (design question, constraints)
  - WX domain knowledge (embedded above)
  - Pipeline state (what's decided, what's pending)

helix-domain-debate WRITES TO:
  - Calling block's output file (appended section):
    1. Markdown prose (Steps 1-4) — human-readable for CEO
    2. JSON side-car (Step 4.5) — machine-readable for downstream blocks
    3. Return summary (Step 5) — completion confirmation
  - Does NOT update pipeline state or create separate files

helix-domain-debate JSON CONTRACT:
  - Fenced as ```json:domain-debate-sidecar for reliable extraction
  - Downstream blocks extract via: find code block with language tag "json:domain-debate-sidecar"
  - Fields are OPTIONAL by calling context (wp_candidates only for BB, coupling_scores only for BD)
  - All JSON must be valid (parseable by standard JSON parser)
```

## COD Classification

- Domain perspective generation: Offload (O2) — AI simulates 3 domain viewpoints
- Contradiction detection: Offload (O1) — AI surfaces conflicts
- Conflict resolution: **Core (C)** — CEO decides trade-offs
- Synthesis validation: **Core (C)** — CEO approves integrated recommendation
