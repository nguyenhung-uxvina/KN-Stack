---
name: helix-p2-frame
description: "Block A of Phase 2 pipeline — identify solution-determining subfunction, run TRIZ contradiction analysis, check TESE stalled trends for innovation targeting. Can run standalone or as part of /helix-concept-generate pipeline. Triggers on: 'problem frame', 'solution-determining', 'TRIZ contradiction', 'essential problem', 'TESE trend'."
---

# Block A: Problem Framing — Solution-Determining SF + TRIZ + TESE

> **P&B:** 6.2 + TRIZ | **Pipeline:** helix-concept-generate → Block BA
> **Input:** `B0_Preflight_Report.md` + Phase 1 deliverables | **Output:** `BA_Problem_Frame.md`
> **Galaxy:** [[Solution-Determining Subfunction]], [[TRIZ × Pahl-Beitz]], [[TESE Stalled Trend]]
> **Reference:** `helix-concept-generate/references/triz-40-principles.md`

## Operational Envelope
> Source: [[Operational Envelope Law]], Multi-Agent Research 2026-04-22

| DO (within envelope) | DON'T (outside envelope) |
|---------------------|------------------------|
| Identify solution-determining SF | Search for working principles (= BB) |
| Run TRIZ contradiction analysis | Propose solutions (= BB) |
| Check TESE stalled trends | Skip SF identification |
| Score SF importance with 3-domain lens | Auto-select SF without CEO review |

**Multi-Agent Mode:** LIGHT — 3 domain lenses (Mech/Elec/AI-SW) for SF importance scoring only
**CEO Checkpoint:** Block boundary (output: BA_Problem_Frame.md). CEO confirms SF selection.

## Standalone Usage
```
/helix-p2-frame VN-XUONG-UUV
```

## Input Requirements
- `1_Projects/{{project}}/Phase2-Concept/B0_Preflight_Report.md` — design type
- `1_Projects/{{project}}/Phase1-Task/Function_Structure.md` — sub-functions
- `1_Projects/{{project}}/Phase1-Task/Essential_Problem.md`
- Optional: HOQ from `/forge-job-map`

## Workflow

### Step A1: Solution-Determining Subfunction Identification

> **Galaxy:** [[Solution-Determining Subfunction — Không Phải Mọi Function Đều Bằng Nhau]]

```
SOLUTION-DETERMINING SF ANALYSIS — {{project_id}}
Date: {{today}}

| SF-ID | Sub-Function | Cascade Score (1-5) | Novelty (1-5) | Constraint Density | Solution-Determining? |
|-------|-------------|--------------------|--------------|--------------------|----------------------|

SOLUTION-DETERMINING SF: SF-{{XX}} — "{{name}}"
RATIONALE: {{why this SF determines the rest}}

DECOMPOSITION STRATEGY:
  - SF-{{XX}} (solution-determining): DEEP — all 7 methods, ≥5 WPs
  - {{novel SFs}}: MEDIUM — ≥3 methods, ≥3 WPs
  - {{known SFs}}: SHALLOW — catalogue lookup, ≥2 WPs
```

**Rule:** Solve solution-determining SF FIRST. Its WP choice cascades through entire design.

### Step A2: TRIZ Contradiction Analysis (Mayda & Borklu 2014)

**Reference:** `helix-concept-generate/references/triz-40-principles.md`

1. **Import contradictions** from HOQ correlation roof or CEO manual input
2. **Map to TRIZ parameters** (39 engineering parameters)
3. **Look up contradiction matrix** → suggested principles (3-4 per contradiction)
4. **Generate Essential Problem Definitions:**
   ```
   P1: "The system should be designed as {{principle-driven direction}}"
   ```
5. **Innovation Level Tagging** (Altshuller 1-5)

**Skip condition:** No HOQ AND no CEO contradictions → skip. Log: "TRIZ skipped."

### Step A3: TESE Stalled Trend Check (Original design only)

Score product against 8 Altshuller evolution trends:

| Trend | Name | Score (1-5) | Stalled? | Defense Ceiling |
|-------|------|------------|---------|-----------------|
| 1 | Wholeness | | | |
| 2 | Energy Flow Efficiency | | | |
| 3 | Rhythm Coordination | | | |
| 4 | Ideality | | | |
| 5 | Uneven Development (bottleneck) | | | |
| 6 | Super-system Transition | | | ACH advances this |
| 7 | Macro → Micro | | | ≤3 unless field-proven |
| 8 | Dynamicity | | | VN manufacturing limit |

**Stalled (<3)** = highest-leverage innovation direction for Block BB.

**RESEARCH HOOK (state of the art):** TESE scoring above draws on model knowledge, which is
capped at training cutoff. If any trend scores ≤2, or CEO suspects the field moved recently,
raise a Research Brief via `/helix-research` (`type: state-of-the-art`, `phase: P2`) — the
dispatcher will propose T2/T3. Update the trend table only with cited findings; log the
Response file in the ledger line.

**Skip condition:** Adaptive/Variant designs → skip.

### ICDM Extension (if --icdm active)

- Add C-K Theory expansion on essential problems
- Add Design Thinking empathy mapping overlay
- Generate innovation potential score per SF

## Output

Save to `1_Projects/{{project}}/Phase2-Concept/BA_Problem_Frame.md`:

```markdown
# BA Problem Frame — {{project}}
Date: {{today}}

## Solution-Determining SF
SF-{{XX}}: {{name}}
Cascade: {{rationale}}
Strategy: DEEP({{SF list}}) / MEDIUM({{SF list}}) / SHALLOW({{SF list}})

## TRIZ Contradictions (if applicable)
[contradiction table + essential problem definitions P1, P2, ...]

## TESE Analysis (if Original design)
[8-trend table + stalled trends identified]

## Innovation Guidance for Block BB
- Priority search areas: {{based on stalled trends + contradictions}}
- Innovation level target: {{2-3 for defense, higher for breakthrough}}
- Essential problems to satisfy: P1, P2, ...
```

## CEO Checkpoint

```
═══ BLOCK BA PROBLEM FRAMING COMPLETE ═══
Solution-Determining SF: {{name}}
Essential Problems: {{count}} defined
TESE Stalled: {{trends}}

CEO:
(1) ✅ Approve → tiếp tục Block BB (Solution Search)
(2) 🔄 Điều chỉnh SF identification hoặc TRIZ problems
(3) ⏸️ Dừng — cần thêm HOQ data
```

## COD
- SF cascade analysis: Offload (O2) — AI assists
- SF identification decision: **Core (C)** — CEO judgment
- TRIZ mapping: Offload (O2) — AI looks up matrix
- Problem definition approval: **Core (C)** — CEO approves
