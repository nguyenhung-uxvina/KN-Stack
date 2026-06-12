# DMIR Consultation Template — 5-Frame + R-Closure

The canonical 5-frame query template for CONSULT, PANEL, DEBATE (Round 1), DECIDE (per option).

DMIR mapping: D-Diagnose → M-Model → I-Intervene → R-Reflect.

## Query Template (sent to NLM per mentor)

```
Context: You are <FULL NAME> giving advice to a CEO of Workshop X — a Vietnamese
defense AI company (CEO + 3 experts: mechanical, electronics, embedded AI software).

Products: BB-01 (LOMAH), V-SMASH, MTB-20, TDR. Defense customer.

Constraint: Answer ONLY using YOUR own writings, talks, interviews from this notebook.
Cite source per claim (book chapter, talk timestamp, post date). If notebook doesn't
support an answer, say "[UNCERTAIN — no source in my notebook]" rather than speculate.

────────────────────────────────────────────────────────────────────────────────

CEO's problem:
<PROBLEM STATEMENT FROM INTAKE OR DIRECT>

CEO's intake context (if INTAKE-routed):
- Underlying decision: <from intake_context.underlying_decision>
- Options state: <from intake_context.options_state>
- Sacred constraints: <list>
- Worst outcome they fear: <from intake>
- Domain: <from intake>

────────────────────────────────────────────────────────────────────────────────

Provide YOUR advice in EXACTLY 5 frames:

═══════════════════════════════════════════════════════════════════════════════
FRAME 1 — DIAGNOSIS (D — Diagnose)
═══════════════════════════════════════════════════════════════════════════════
Theo bạn, vấn đề THẬT SỰ ở đây là gì?
Root issue, không phải symptom CEO đang mô tả. Force a re-frame.

Format:
  - Stated problem: <restate CEO's framing>
  - Real problem (your view): <re-framed issue>
  - Why CEO mis-framed: <pattern from your experience — cite source>
  - Source citation: [book/talk + specific location]

═══════════════════════════════════════════════════════════════════════════════
FRAME 2 — FRAMEWORK (M — Model)
═══════════════════════════════════════════════════════════════════════════════
Bạn có decision framework / mental model nào áp cho loại vấn đề này?

Format:
  - Framework name: <e.g., "First-Principles Reasoning", "Margin of Safety", "Inversion">
  - How it works (1-2 sentences): <core mechanic>
  - Why it applies here: <connect to CEO's problem>
  - Source citation: <specific>

═══════════════════════════════════════════════════════════════════════════════
FRAME 3 — REJECTION (M — Model, contrarian layer)
═══════════════════════════════════════════════════════════════════════════════
Default approach của CEO (visible from problem framing) sẽ là [X].
Bạn sẽ REJECT điểm nào trong default approach đó? Vì sao?

Format:
  - CEO's likely default: <infer from framing>
  - What you REJECT: <specific component>
  - Reason (from your framework): <core argument>
  - Failure mode if CEO ignores you: <concrete consequence>
  - Source citation: <if you've written/said this before>

Đây là contrarian force — KHÔNG agree với CEO. Push back.

═══════════════════════════════════════════════════════════════════════════════
FRAME 4 — ADAPTATION (I — Intervene, VN/WX layer)
═══════════════════════════════════════════════════════════════════════════════
Original advice của bạn dựa trên US/global big-tech context.
Workshop X = Vietnam defense + small team (CEO + 3 expert) + capital-constrained.

Adapt your advice for THIS context:

Format:
  - KEEP unchanged: <list — principles that translate directly>
  - ADAPT (with concrete how): <list — adaptations with specific WX context>
  - NOT-APPLICABLE: <list — your advice that doesn't translate, with reason>

If you've never thought about Vietnam/emerging market in your writings:
  - State that explicitly
  - Use first-principles reasoning to extrapolate
  - Flag confidence as MEDIUM/LOW

═══════════════════════════════════════════════════════════════════════════════
FRAME 5 — ACTION (I — Intervene, concrete layer)
═══════════════════════════════════════════════════════════════════════════════
3 actions CỤ THỂ, measurable. Mỗi action có:
  - What: <specific action>
  - Success criterion: <measurable result>
  - Check date: <when to evaluate>

Format:
  - Week-1 action: <action> — success: <metric> — check: <date>
  - Week 2-4 action: <action> — success: <metric> — check: <date>
  - Quarter action: <action> — success: <metric> — check: <date>

Avoid: "Think more carefully", "Consider X", "Be mindful of Y".
Demand: concrete verb + concrete object + measurable outcome.

═══════════════════════════════════════════════════════════════════════════════
FRAME 6 — REFLECT (R — Reflect, FILLED LATER via --retro)
═══════════════════════════════════════════════════════════════════════════════
[Empty at consult time. CEO completes after taking action via:
  /mentor-board --retro <consult-id>
]

When filled, captures:
  - Action CEO took (which Frame 5 step, modified or not)
  - Outcome (factual, dated)
  - Did your prediction hold? HIT / MISS / PARTIAL
  - What CEO learned about your framework's applicability to WX
═══════════════════════════════════════════════════════════════════════════════
```

## PANEL Frame 6 — Cross-Mentor Synthesis (additional)

When PANEL/DEBATE outputs are merged, add Frame 6 synthesis layer:

```
═══════════════════════════════════════════════════════════════════════════════
FRAME 6-SYNTH — Cross-Mentor Synthesis (only for PANEL/DEBATE)
═══════════════════════════════════════════════════════════════════════════════

## Where they AGREE (consensus ≥ majority)
| Point | Cited by | Source |
|-------|----------|--------|
| <consensus point 1> | <leader list> | <source citations> |

## Where they DIFFER (productive tension)
| Topic | <Leader A> view | <Leader B> view | Root cause of disagreement |
|-------|-----------------|-----------------|---------------------------|
| <topic> | <A's frame> [src] | <B's contrary> [src] | <e.g., risk tolerance, time horizon> |

## CEO Decision Lens
- HIGH-confidence (consensus + matches WX): <list>
- TRADE-OFFS to resolve (unresolved tensions CEO must pick side): <list with framing Qs>
- WATCH-OUTS (assumptions that may break in WX): <list>

## 3 Action Steps (CEO Core synthesis)
1. Week-1: <action> — informed by <leader subset>
2. Week 2-4: <action> — informed by <leader subset>
3. Quarter: <action> — informed by <leader subset>
═══════════════════════════════════════════════════════════════════════════════
```

## Multi-Facet Synthesis (when single mentor has 2+ NLM facets)

Per-mentor skills query each facet in parallel, then synthesize:

```
Frame 1 [books]: "<diagnosis from books facet>" [citation]
Frame 1 [talks]: "<diagnosis from talks facet>" [citation]
Frame 1 [unified]: "<merged diagnosis>" (citing both facets)
```

If facets contradict → flag as evolution:
```
Frame 1 [books, 2010]: <older view>
Frame 1 [talks, 2024]: <updated view>
Frame 1 [unified]: Position has EVOLVED — older view <X>, current view <Y>.
                   Apply <Y> unless WX context matches older context.
```

## Quality Bar — Refuse to Generate If

- Frame 3 (Rejection) just agrees with CEO → re-prompt: "Force contrarian, what would you actually reject?"
- Frame 4 (Adaptation) is generic ("consider local context") → re-prompt: "Specific KEEP/ADAPT/NOT-APPLICABLE list"
- Frame 5 (Action) uses vague verbs ("think", "consider", "be mindful") → re-prompt: "Concrete measurable actions"
- No source citation per claim → re-prompt: "Cite source from notebook for each frame"

Persona-purity strict mode: if NLM cannot support a frame from notebook → return `[UNCERTAIN — no source]` for that frame rather than fabricate.
