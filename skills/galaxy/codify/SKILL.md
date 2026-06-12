---
name: codify
description: "Convert deterministic surface area of any markdown skill into a Python script (stdlib only) + tests, then wire the skill to invoke the script via Bash. Naval code leverage: markdown skills = LLM cost per call; Python scripts = deterministic, ~0.001s, ~$0. Codify candidates: math (opportunity score, FPY, cost rollup, max_builds, ratios), table formatting, file parsing, CSV/JSON export. NEVER codify: judgment, classification, creative content. 4-step pipeline: scan → audit → generate → wire. Flags: --target <skill-path>, --scope <function>, --dry-run, --no-tests. Triggers on: 'codify skill', 'convert skill to script', 'biến skill thành code', 'code leverage', 'python from skill', 'compile skill', 'deterministic script'."
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent"]
---

# codify — Markdown Skill → Python Script (Naval Code Leverage)

> **Role:** Strip the deterministic surface area out of markdown skills, ship it as Python; keep markdown for judgment.
> **Naval principle:** *"Code is permissionless leverage. Run it once, it runs forever."* Each markdown skill costs LLM tokens per invocation. Each Python script costs nothing after first write. For ops executed weekly/daily, the math is overwhelming.
> **Musk lens:** "Don't optimize what should be deleted." For deterministic math/parsing, the markdown narration IS the waste. Codify removes the waste, keeps the judgment.
> **Scope discipline:** Codify is **subtraction**, not addition. We are NOT building a new framework — we are extracting code from existing markdown skills.

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    codify (4-step pipeline)                              │
│                                                                           │
│  Flags: --target <skill-path>  --scope <function>                       │
│         --dry-run  --no-tests  --lang vi|en (audit doc)                 │
│                                                                           │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐                                │
│  │ C1  │───▶│ C2  │───▶│ C3  │───▶│ C4  │                                │
│  │SCAN │    │AUDIT│    │GEN- │    │WIRE │                                │
│  │     │    │CORE │    │ERATE│    │     │                                │
│  └──┬──┘    └──┬──┘    └──┬──┘    └──┬──┘                                │
│     │          │CORE      │          │CEO                                 │
│     ▼          ▼          ▼          ▼                                    │
│  [identify  [classify [emit .py +  [SKILL.md                            │
│   determin-  CODIFY/  test_*.py +  Invocation                            │
│   istic      LLM/     example]    section +                              │
│   ops]       HYBRID]              verify]                                 │
└──────────────────────────────────────────────────────────────────────────┘

Legend: CORE = CEO non-delegable (codification scope decision)
        CEO  = checkpoint after wire

Output: skills/<domain>/<skill>/                  (in target skill folder)
  ├── SKILL.md             (updated with ## Invocation section)
  ├── <script_name>.py     (new — stdlib only)
  ├── test_<script_name>.py (new — basic happy-path + edge cases)
  └── codify_audit.md      (new — what was codified, what stayed markdown)
```

## How to Use

### Codify entire skill (recommended for math-heavy skills)
```
/codify --target skills/forge/forge-job-map
```

### Codify specific function only
```
/codify --target skills/erp/erp-quality --scope fpy_calculation
```

### Dry-run (audit only, no files written)
```
/codify --target skills/forge/forge-cost --dry-run
```

### Without tests (faster, for one-off scripts)
```
/codify --target skills/guard/ratio-check --no-tests
```

## Workflow

### Step C1: Scan (Identify Deterministic Surface Area)

Read target SKILL.md and find operations matching CODIFIABLE patterns:

```
SCAN — {{target_path}}/SKILL.md
Date: {{today}}

DETERMINISTIC OPERATIONS DETECTED:
| # | Operation | Type | LLM Cost Est. | Codification Risk |
|---|-----------|------|---------------|-------------------|
| 1 | Opportunity = Importance + max(I-S, 0) | MATH | medium | LOW |
| 2 | DSO score = Quality × Risk | MATH | low | LOW |
| 3 | FPY = pass / total × 100 | MATH | low | LOW |
| 4 | BOM cost rollup by category | AGGREGATION | medium | LOW |
| 5 | Reorder classification (OK/LOW/BLOCKING) | RULE-BASED | medium | LOW |
| 6 | CSV export of BOM table | I/O | high | LOW |
| 7 | YAML frontmatter validation | PARSING | medium | LOW |
| 8 | Wikilink density per Galaxy note | GRAPH | low | LOW |
| 9 | Markdown report compilation | TEMPLATING | medium | MEDIUM |

OPERATIONS THAT MUST STAY MARKDOWN (LLM):
| # | Operation | Why |
|---|-----------|-----|
| 1 | "Identify solution-determining sub-function" | Judgment, not deterministic |
| 2 | "Classify item as SAFE/REVIEW/SENSITIVE" | Context-dependent, CEO Core |
| 3 | "Generate hook for blog post" | Creative content |
| 4 | "Workshop master review verdict" | Physical inspection |
```

### Step C2: Audit + Codification Plan (CORE — CEO approves scope)

```
CODIFICATION PLAN — {{target}}

PROPOSED SCRIPT: {{script_name}}.py

FUNCTIONS TO CODIFY:
| Function | Inputs | Outputs | Pure? | Stdlib only? |
|----------|--------|---------|-------|--------------|
| compute_opportunity_score(importance, satisfaction) | int×2 | (score:int, class:str) | YES | YES |
| classify_underserved(score) | int | str | YES | YES |
| rollup_bom_cost(rows) | list[dict] | dict[category, total] | YES | YES |

LLM-RETAINED OPERATIONS (stay in SKILL.md):
- Strategy recommendation (DOMINATE/DISRUPT/IMPROVE/RETREAT) — judgment
- HITL safety verification — context-dependent
- VN procurement context interpretation — domain knowledge

INVOCATION PATTERN (LLM uses Bash tool):
  python skills/forge/forge-job-map/opportunity_score.py --input <csv|json>
  → outputs ranked table to stdout (or --output <path>)

COMPLEXITY ESTIMATE:
  Script: ~80-120 lines (stdlib only — argparse, json, csv, statistics)
  Tests: ~50-80 lines (happy path + 3-5 edge cases)
  SKILL.md changes: +20 lines (Invocation section)

CEO:
(1) ✅ Approve scope → generate (C3)
(2) 🔄 Reduce scope (drop function X, keep markdown)
(3) ⏸️ Expand scope (add function Y also)
(4) ❌ Cancel — judgment too complex for codification
```

### Step C3: Generate (.py + test_.py + audit log)

Generate 3 files in target skill folder:

#### File 1: `<script_name>.py`

```python
"""<Skill name> — <function purpose>.

Codified from skills/<domain>/<skill>/SKILL.md on {{today}}.
Stdlib only. Pure functions. CLI via argparse.

Generated by: /codify
"""

from __future__ import annotations
import argparse, json, csv, sys
from dataclasses import dataclass
from pathlib import Path

# ─── Pure functions (the codified surface) ──────────────────────────────

def compute_opportunity_score(importance: int, satisfaction: int) -> int:
    """Opportunity = Importance + max(Importance - Satisfaction, 0)."""
    if not (1 <= importance <= 10 and 1 <= satisfaction <= 10):
        raise ValueError(f"Scores must be 1..10, got I={importance} S={satisfaction}")
    return importance + max(importance - satisfaction, 0)

def classify(score: int, satisfaction: int, hitl: bool = False) -> str:
    """Per forge-job-map rules. HITL-mandatory items never OVERSERVED unless satisfaction≥9."""
    if hitl and satisfaction < 9:
        return "REQUIRED-MAINTAIN"
    if score >= 10: return "UNDERSERVED"
    if score >= 8:  return "SLIGHTLY-UNDERSERVED"
    if score >= 6:  return "SERVED"
    return "OVERSERVED"

# ─── CLI ────────────────────────────────────────────────────────────────

def main() -> int:
    p = argparse.ArgumentParser(description="<script purpose>")
    p.add_argument("--input", required=True, type=Path)
    p.add_argument("--output", type=Path)
    p.add_argument("--format", choices=["table", "json", "csv"], default="table")
    args = p.parse_args()
    # ... read input, apply functions, write output ...
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

#### File 2: `test_<script_name>.py`

```python
"""Tests for <script_name>. Run: python -m unittest test_<script_name>"""
import unittest
from <script_name> import compute_opportunity_score, classify

class TestOpportunityScore(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(compute_opportunity_score(8, 5), 11)  # underserved
        self.assertEqual(compute_opportunity_score(9, 9), 9)   # served
    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            compute_opportunity_score(11, 5)
    def test_classify_hitl(self):
        self.assertEqual(classify(score=5, satisfaction=8, hitl=True), "REQUIRED-MAINTAIN")
        self.assertEqual(classify(score=5, satisfaction=9, hitl=True), "OVERSERVED")
    def test_classify_thresholds(self):
        self.assertEqual(classify(10, 5), "UNDERSERVED")
        self.assertEqual(classify(8, 6), "SLIGHTLY-UNDERSERVED")
        self.assertEqual(classify(6, 7), "SERVED")
        self.assertEqual(classify(3, 9), "OVERSERVED")

if __name__ == "__main__":
    unittest.main()
```

#### File 3: `codify_audit.md`

```markdown
# Codify Audit — <skill name>
Date: {{today}}  Generator: /codify

## Codified
| Function | Source | LOC | Test cases |
|----------|--------|-----|-----------|
| compute_opportunity_score | SKILL.md §opportunity-algorithm | 6 | 2 |
| classify | SKILL.md §classification + safety rule | 8 | 4 |

## Retained in markdown (LLM)
| Operation | Reason |
|-----------|--------|
| Strategy recommendation | Judgment per quadrant + competitive context |
| HITL safety verification | Context: which outcomes are safety-mandatory? CEO Core |
| Job map definition | Requires user conversation |

## Invocation Pattern
LLM calls via Bash tool:
```
python skills/forge/forge-job-map/opportunity_score.py --input outcomes.csv --format table
```

## Cost Impact Estimate
- Before: ~3-5k tokens per invocation for math+formatting (LLM)
- After: <100 tokens (invoke script + parse result)
- Skill called ~12×/year per product, 4 products = 48 invocations/year
- Annual saving: ~200k tokens (≈ $1-3 depending on model)
- More important: deterministic, zero error variance, scriptable in CI
```

### Step C4: Wire (Update SKILL.md, Verify)

Add `## Invocation` section to target SKILL.md, then run the test suite to verify.

```
WIRE — {{target_path}}/SKILL.md

1. Add ## Invocation section after existing workflow:
   - Document Bash invocation pattern
   - Reference test_<script>.py
   - Note: "For deterministic math (e.g., opportunity scoring), call the script.
            For judgment (strategy selection), narrate via LLM."

2. Run tests:
   cd skills/<domain>/<skill>/
   python -m unittest test_<script_name>

3. Verify script executable:
   python <script_name>.py --help

4. CEO Checkpoint:
   ═══ CODIFY COMPLETE — {{target}} ═══
   Files: {{script}}.py ({{loc}} lines) + test_{{script}}.py ({{loc}} lines) + codify_audit.md
   Tests: {{N}} passed
   SKILL.md: +{{N}} lines (Invocation section)
   Estimated saving: {{tokens}}/year

   CEO:
   (1) ✅ Approve → register in codify ledger
   (2) 🔄 Revise (add/remove function from script)
   (3) ⏸️ Abort wire (keep files, no SKILL.md change)
```

After approval, append to `d:/KN-Stack/scripts/_codify_ledger.md`:
| Date | Target | Script | LOC | Tests | LLM saving estimate |

## Codifiability Heuristics (when to use this skill)

### ✅ STRONG CODIFY candidates
- Pure math (opportunity score, FPY, DSO, cost rollup, variance %, ratios)
- Deterministic classification with explicit thresholds (UNDERSERVED if score ≥10)
- Table aggregation (BOM rollup by category, capacity sum per PX)
- File format conversion (markdown table → CSV, JSON → table)
- Format validation (YAML frontmatter schema, naming convention regex)
- Graph metrics (wikilink density, dependency depth)
- Counter / ratio / percentile calculations

### ⚠️ HYBRID candidates (codify the math, keep narrative)
- BOM availability check (script: max_builds calc; markdown: shortage handling decision)
- NCR pattern detection (script: groupby + counts; markdown: root cause hypothesis)
- Stock reorder logic (script: classify OK/LOW/BLOCKING; markdown: PO drafting)
- Skill usage frequency analysis (script: log parse; markdown: insights)

### ❌ DO NOT CODIFY
- Anything requiring CEO judgment (CORE-classified COD)
- Creative content generation (positioning, hooks, blog drafts)
- Context-dependent classification (SAFE/REVIEW/SENSITIVE — depends on audience)
- Workshop master "gia cong duoc" verdict
- Strategic recommendations (DOMINATE/DISRUPT/IMPROVE/RETREAT)
- IP audit verdicts
- Concept selection (P&B Phase 2 BE)
- Workshop or shop-floor physical inspections

### Rule of thumb (Musk-flavored)
> "If a competent technician with the SOP can do it, codify. If only the CEO can do it, leave markdown."

## Python Conventions for KN-Stack

### File Placement
- Script: `skills/<domain>/<skill>/<script_name>.py`
- Test: `skills/<domain>/<skill>/test_<script_name>.py`
- Audit: `skills/<domain>/<skill>/codify_audit.md`
- Ledger: `d:/KN-Stack/scripts/_codify_ledger.md` (append-only)

### Dependencies
- **Stdlib only by default** — argparse, json, csv, dataclasses, pathlib, re, statistics, unittest
- If non-stdlib needed: add `requirements.txt` in same folder, document in audit
- Never install global packages; if user runs script and it fails on import, surface clearly

### Style
- Pure functions where possible (input → output, no side effects)
- Type hints on public functions (`def f(x: int) -> str:`)
- One-line docstrings minimum
- `argparse` CLI with `--input/--output/--format` triad
- `main() -> int` returning exit code; `sys.exit(main())` at bottom
- Errors: raise ValueError with clear message; let CLI surface them
- No `print` for control flow — use return values and `sys.exit`

### Testing
- `unittest` stdlib (no pytest dependency)
- Class per function or per concern
- Minimum: 1 happy path + 1 invalid input + 1 edge case per function
- Run: `python -m unittest test_<script_name>`

### Invocation from LLM
LLM uses Bash tool with absolute path:
```bash
python d:/KN-Stack/skills/forge/forge-job-map/opportunity_score.py --input outcomes.csv
```
LLM parses stdout, narrates result. LLM never re-implements the math.

## Data Bus

| File | Written By | Content |
|------|-----------|---------|
| `<target>/<script>.py` | C3 | Generated Python (stdlib only) |
| `<target>/test_<script>.py` | C3 | Unit tests (unittest) |
| `<target>/codify_audit.md` | C3 | What was codified vs retained |
| `<target>/SKILL.md` | C4 | +Invocation section pointing to script |
| `d:/KN-Stack/scripts/_codify_ledger.md` | C4 | Append-only registry of codifications |

## Integration

```
codify READS FROM:
  - skills/<domain>/<skill>/SKILL.md → target to analyze
  
codify WRITES TO:
  - skills/<domain>/<skill>/<script>.py
  - skills/<domain>/<skill>/test_<script>.py
  - skills/<domain>/<skill>/codify_audit.md
  - skills/<domain>/<skill>/SKILL.md (Invocation section append)
  - d:/KN-Stack/scripts/_codify_ledger.md (append-only)

codify CAN BE INVOKED ON (top candidates):
  - forge-job-map → opportunity_score.py (opp scoring + classification)
  - forge-cost → cost_rollup.py (BOM cost categories + variance)
  - erp-stock → reorder_classifier.py (OK/LOW/BLOCKING + max_builds)
  - erp-quality → fpy.py (FPY + NCR pattern groupby)
  - helix-p4-bom → bom_csv_export.py (markdown table → ERPNext CSV)
  - bridge-dashboard → dashboard_metrics.py (7 metrics aggregation)
  - forge-portfolio → portfolio_rollup.py (per-product status rollup)
  - guard/ratio-check → ratio_calc.py (analytical:physical counter)
  - galaxy/galaxy-links → wikilink_density.py (graph metric on Galaxy)
  - forge-shift → shift_score.py (SHIFT checklist scoring)

codify DOES NOT CODIFY (intentional, per Heuristics):
  - Any skill where COD says Core (C) for the operation
  - Any skill generating creative content (skill-to-public, book-*)
  - Any orchestrator (codebase-to-book, helix-task-clarify, forge-fabrication, helix-detail-finalize)
  - Any judgment-heavy skill (first-principles, decide, paradigm)
```

## Rules

- **C2 Codification scope is CEO Core** — non-delegable. Don't auto-codify based on heuristic match alone.
- **Stdlib only by default** — non-stdlib dependency requires explicit CEO approval (adds maintenance debt).
- **Tests are mandatory unless `--no-tests` flag** — codified script without tests = silent regression risk.
- **Never codify Core-COD operations** — heuristic check before C3.
- **Audit log is the contract** — `codify_audit.md` must list what was codified AND what was intentionally retained, with reasons.
- **SKILL.md retains the WHY** — script holds the HOW. Reading SKILL.md alone must still convey intent.
- **Pure functions preferred** — side-effect functions (file write, stdout) at CLI boundary only.
- **Error messages are user-facing** — they appear to CEO via LLM narration; write them clearly.
- **One script per skill (default)** — don't fragment. If skill has 5 unrelated functions, build 1 script with 5 functions.
- **Append-only ledger** — never rewrite history of codifications.
- **Re-codify safe** — running `/codify` on already-codified skill = regenerate (compare diffs, CEO approves changes).
- **No codify on orchestrators** — pipeline orchestration is inherently LLM-driven (context, judgment, checkpoints). Wait for AGENT primitives to mature instead.

## COD Classification

- C1 Scan + heuristic detection: Offload (O1)
- C2 Audit table draft: Offload (O2)
- **C2 Codification scope decision: Core (C)** — what to extract vs retain
- C3 Script generation: Offload (O1) — mechanical from C2 spec
- C3 Test generation: Offload (O1) — happy path + edge cases per function
- C4 SKILL.md wire: Offload (O1)
- C4 Test execution: Offload (O1) — pass/fail surfaced to CEO
- **C4 Final approval (commit changes): Core (C)** — accountability for new code

## Why This Compounds (Naval Lens — Strongest of All)

```
Markdown skill called 12×/year per product × 4 products = 48 invocations
Average LLM cost per invocation (with context): ~$0.05-0.50
Annual cost per skill: $2.40-24.00 just for one math operation
                      × 10 top-frequency skills codified
                      = $24-240/year saved + zero error variance + scriptable in CI

But the real prize isn't $: it's that codified ops become **CI-testable, version-controlled, auditable, runnable headless**. Markdown ops only execute when an LLM session runs. Python ops run anywhere — git hooks, daily cron, batch jobs, external dashboards.
```

**The compounding is structural:** every codified function becomes a primitive available to other automation. Once `opportunity_score.py` exists, any tool (not just Claude Code) can compute it — Excel, Airtable, ERPNext webhook, daily reports.

This is the moment KN-Stack stops being "an LLM-only system" and becomes "an LLM + code system where each does what it's best at." Naval's permission-less leverage finally compounds.
