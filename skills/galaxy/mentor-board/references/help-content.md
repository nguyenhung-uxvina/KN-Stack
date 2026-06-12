# mentor-board — Help Content (Canonical)

This file is read by `mentor-board` SKILL.md when `--help` is invoked. Single source of truth — update help by editing here, not SKILL.md.

## Full Cheat Sheet (`/mentor-board --help`)

```
═══════════════════════════════════════════════════════════════════════════════
mentor-board — Hội Đồng Cố Vấn AI (DMIR-driven, 7 mentors)
═══════════════════════════════════════════════════════════════════════════════

🚀 QUICK START
  /mentor-board "<your problem>"
  → AI sẽ ask clarifying questions, propose mentors + mode, CEO confirm, then run

📚 ENTRY MODES (default smart router handles most cases)
  /mentor-board                       Registry view (advisor list)
  /mentor-board "<problem>"           INTAKE — clarify, route, consult
  /mentor-board --help                This help
  /mentor-board --help <mode>         Detailed help for specific mode

🎯 4 CONSULTATION MODES (INTAKE picks one, or direct via flag)
  --consult <leader> "<problem>"      Tư vấn 1 mentor (5-frame DMIR report)
  --panel <leaders|preset> "<prob>"   Multi mentors parallel + synthesis (explore)
  --debate <leaders|preset> "<prob>"  3-round argument (tension/disagreement)
  --decide <leaders|preset> "<prob>" --options "A;B;C"   Decision matrix

  Presets: capital · scaling · ai-strategy · manufacturing · founder-wisdom · people · all

👥 BOARD MANAGEMENT
  --list                              Detailed registry table
  --suggest                           AI proposes new mentors (≥5 consults required)
  --add <leader>                      Create new mentor (~2h pipeline, 5 gates)
  --remove <leader>                   Archive mentor (not delete)
  --rename <old> <new>                Rename folder + NLM notebook
  --check-new --all                   Bulk: new content scan all mentors
  --sync --all                        Bulk: refresh all mentors

🔁 DMIR CLOSURE (the compound learning step)
  --retro <consult-id>                Fill Frame 6 R-step after taking action

💡 EXAMPLES
  /mentor-board "Should I take VC funding?"
    → INTAKE asks: deadline? options? sacred constraints?
    → proposes Musk + Munger + Marks (capital preset)
    → CEO confirms → routes to --debate

  /mentor-musk "How to scale BB-01 fabrication 10x?"
    → direct single consult, 5-frame DMIR report

  /mentor-board --decide capital "Allocate 500M VND" \
    --options "Hire AI eng; Buy GPU; Bank reserve"
    → 3 capital mentors × 3 options = decision matrix

  /mentor-board --retro 20260520-musk-vc-funding
    → close DMIR R-step, update Musk's reliability log

📂 OUTPUTS LIVE IN
  D:/Workshop_X/2_Areas/CEO-Self/Mentor-Consultations/    Per-consult markdown
  D:/Workshop_X/3_Resources/Mentor-Board/_registry.md     Ledger
  D:/Workshop_X/3_Resources/Mentor-Board/<leader>/        Per-mentor profiles

📖 DEEP REFERENCES
  galaxy/mentor-board/references/dmir-template.md         5-frame template
  galaxy/mentor-board/references/intake-protocol.md       Smart router logic
  galaxy/mentor-board/references/debate-protocol.md       Debate rounds
  galaxy/mentor-board/references/decide-matrix.md         Decision matrix
  galaxy/mentor-board/references/preset-clusters.md       Preset definitions
  galaxy/mentor-board/references/retro-template.md        DMIR R-step format
  galaxy/mentor-board/references/facet-split-strategies.md Multi-notebook split
═══════════════════════════════════════════════════════════════════════════════
```

## Per-Mode Drilldown (`/mentor-board --help <mode>`)

### `--help intake`

```
INTAKE — Smart Router (default entry, ~5-10 min)
Trigger: /mentor-board "<problem>" without mode flag

Flow:
  I1 Parse problem
  I2 Ask 6 clarifying questions (decision/deadline/options/constraints/worst/domain) — CEO answers
  I3 AI proposes mentor list (★★★/★★/★) with rationale + flags missing-from-board mentors
  I4 AI proposes mode (CONSULT/PANEL/DEBATE/DECIDE) based on heuristics
  I5 CEO confirms or adjusts (add/remove/swap mode/refine problem/cancel)
  I6 Route to confirmed pipeline

Output: consult file with intake_context frontmatter

Why: 70% of consultation quality = problem framing. INTAKE forces it.
```

### `--help consult`

```
CONSULT — single mentor (5-frame DMIR, ~10 min)
Trigger: /mentor-<leader> "<problem>" OR /mentor-board --consult <leader> "<problem>"

Flow:
  C1 Parse problem + optional context — CEO
  C2 Load profile + facet list
  C3 Query NLM with 5-frame DMIR template (cross-facet if multi)
  C4 Write output to Mentor-Consultations/
  C5 Frame 6 R-section starts empty (filled via --retro)
  C6 Provide NLM URL for follow-up

5 Frames (DMIR mapping):
  F1 Diagnosis (D) — root issue per leader's lens
  F2 Framework (M) — their decision model
  F3 Rejection (M) — what they'd REJECT in CEO's default
  F4 Adaptation (I) — VN/WX context (KEEP/ADAPT/NOT-APPLICABLE)
  F5 Action (I) — 3 measurable steps (week-1, week-2-4, quarter)
  F6 Reflect (R) — filled via --retro after CEO acts
```

### `--help panel`

```
PANEL — parallel 5-frame + synthesis (~15-20 min)
Trigger: /mentor-board --panel <leaders|preset> "<problem>"

Best for: exploring, no concrete options yet, want diversity of views

Flow:
  P1 Parse leaders + problem
  P2 CEO context — CEO
  P3 Parallel Task subagents per leader run 5-frame DMIR consult on their notebook
  P4 Compose comparison matrix + Frame 6 synthesis:
     - Where they AGREE (consensus)
     - Where they DIFFER (productive tension)
     - CEO Decision Lens
     - 3 Action Steps — CEO synthesis (Core)
  P5 Save to Mentor-Consultations/<date>-panel-<slug>.md
```

### `--help debate`

```
DEBATE — 3-round argument (~30 min, the tranh luận mode)
Trigger: /mentor-board --debate <leaders|preset> "<problem>"

Best for: real tension between views, need to surface assumptions

Flow:
  Round 1 (Position): parallel — each mentor 5-frame DMIR on problem
  Round 2 (Rebuttal): parallel — each mentor sees others' Round 1 outputs,
                       rebuts strongest opposing view with citation
  Round 3 (Convergence): parallel — each updates view (or stays firm with reason)
  Synthesis: AI identifies productive tensions + "What CEO Must Decide"

Output: full transcript + synthesis. Frame 6 R-section ready for --retro.

NOTE: agents see other mentors' OUTPUTS only, never their notebooks.
```

### `--help decide`

```
DECIDE — option scoring matrix (~20 min)
Trigger: /mentor-board --decide <leaders|preset> "<problem>" --options "A; B; C"

Best for: CEO has concrete options A/B/C, need structured comparison

Options: ≥2, ≤5 (more = decision fatigue, fewer = not real decision)

Flow:
  Dc1 Parse leaders + options. CEO confirms framing.
  Dc2 Per mentor × per option: parallel scoring query
      (score 1-10 + rationale + risk + reverse-condition)
  Dc3 Aggregate matrix:
      - Reliability weights (from each mentor's reliability_log per problem class)
      - Weighted average per option
      - Strong reject flags (score ≤ 3)
      - Consensus risk identification
      - Reverse conditions
  Dc4 DMIR closure (D-M-I, R empty)
  Dc5 CEO final pick — Core
```

### `--help add`

```
ADD — create new mentor-<leader> skill (~2h, 5 CEO gates)
Trigger: /mentor-board --add <leader>

Flow:
  A1 Resolve leader name (slug form: "naval-ravikant")
  A2 Discover Tier 1/2/3 sources (Web + YouTube + Authority)
  A3 CEO reviews + selects sources — Core
  A3.5 IF >45 sources: facet split (temporal/topical/hybrid) — Core
  A4 Create NLM notebook(s), ingest, set persona
  A5 8-query foundational extraction
  A6 Studio artifacts (Briefing + Audio VN + Quiz + Flashcards)
  A7 Generate skills/mentors/mentor-<leader>/SKILL.md from template
  A8 Run setup.sh --install (deploy junction)
  A9 Append to _registry.md — CEO approve close

Output: callable /mentor-<leader> skill + vault profile
```

### `--help retro`

```
RETRO — DMIR R-step closure (~5-10 min, compound learning)
Trigger: /mentor-board --retro <consult-id>

Why: every consult has Frame 6 R-section that starts empty. --retro fills it
     after CEO takes action and outcome is known.

Flow:
  Re1 Read original consult file
  Re2 CEO inputs (Core honesty):
      - Action taken (concrete)
      - Outcome (factual)
      - Prediction match: HIT / MISS / PARTIAL
      - What learned about leader's framework applicability to WX
  Re3 Append to Frame 6 R-section (preserves history)
  Re4 Update mentor's reliability_log.md
  Re5 Pattern detection: 5+ misses same class → warning + CEO action

This is the compounding asset. Mentor reliability becomes empirical over time.
```

### `--help suggest`

```
SUGGEST — AI proposes new mentors (~5 min)
Trigger: /mentor-board --suggest

Requires: ≥5 consultations in last 30 days (cold-start guard)

Flow:
  S1 Scan recent consultations + reliability_log
  S2 Extract problem classes + identify gaps (low coverage or low reliability)
  S3 Propose 3-5 candidates (name + primary works + gap they fill + setup effort)
  S4 CEO accepts → routes to --add — Core
```

## Per-Mentor `--help` Template

(rendered by per-mentor skills, not by mentor-board)

```
═══════════════════════════════════════════════════════════════════════════════
mentor-<leader> — <Full Name> advisor skill
═══════════════════════════════════════════════════════════════════════════════

📌 PROFILE
  Specialties: <comma-separated tags from profile.md>
  Last refresh: <date>  |  Reliability: <%> (<N> retros logged)
  Facets: <count> (<facet names>)

🎯 MODES
  /mentor-<leader>                    Show this profile + recent consults
  /mentor-<leader> --help             This cheat sheet
  /mentor-<leader> "<problem>"        CONSULT (5-frame DMIR, queries ALL facets)
  /mentor-<leader> --facet <name> "<p>"   CONSULT scoped to 1 facet
  /mentor-<leader> --facet auto "<p>"     CONSULT — AI picks best facet
  /mentor-<leader> --facets           List facets với source counts + last_refresh
  /mentor-<leader> --refresh          Refresh all facets
  /mentor-<leader> --refresh --facet X    Refresh single facet
  /mentor-<leader> --check-new        Scan new content (no ingest)
  /mentor-<leader> --history          Past 10 consultations
  /mentor-<leader> --reliability      Hits/misses per problem class

💡 USE WITH ORCHESTRATOR
  /mentor-board --debate <leader>,<other> "..."   Pair với mentor khác
  /mentor-board --panel <preset includes leader> "..."  Auto-included in preset
═══════════════════════════════════════════════════════════════════════════════
```
