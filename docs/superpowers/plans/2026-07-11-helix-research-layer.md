# HELIX Research Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire deep-research capability into HELIX via a 3-tier dispatcher (`helix-research`), a persistent topic-notebook system (`topic-notebook`), and a harness upgrade (static/checks eval runner + HARNESS_STANDARD.md).

**Architecture:** "Thin dispatcher + registry" (Hướng 1, spec §2): two new skills; existing HELIX blocks receive only short "Research Hook" sections pointing at the dispatcher. Executors are all pre-existing (`/research` v4.1, `nlm` Mode 8, mentor-board, NotebookLM MCP).

**Tech Stack:** Markdown SKILL.md files (house format), bash + Python-stdlib (`run-eval.sh`), NotebookLM MCP tools, Windows directory junctions.

**Spec:** `docs/superpowers/specs/2026-07-11-helix-research-layer-design.md`

## Global Constraints

- Branch: `feature/helix-research-layer`. PR target: `feature/evals-static-mode`.
- NEVER touch the Assay workstream's dirty files: `skills/helix/helix-cad-validate/*`, `evals/helix-cad-validate.json` (read-only OK), `skills/mentors/mentor-chris-brose/SKILL.md`, `CHANGELOG.md`, `VERSION`, `evals/fixtures/`, `temp/`. Stage files explicitly by path — never `git add -A` / `git add .`.
- VERSION/CHANGELOG bump is DEFERRED (dirty [1.6.0] hunks belong to Assay); the PR body must state this.
- Every SKILL.md starts with YAML frontmatter: `name:` (= directory name) and `description:` (what it does + "Triggers on: …" phrases, English + Vietnamese).
- Research Hooks must not change block order, must not add blocks to the 6-block pipelines, must not break ONE BLOCK PER TURN. Core decisions (source approval, T2/T3 launch) stay with CEO.
- AI NEVER fabricates TCVN numbers (rule from `helix-p1-preflight`).
- Vault writes limited to: create `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (approved in spec §4.2). No files in `5_Galaxy/`, no moves.
- Commit format: `[DOMAIN] Brief description`.

---

### Task 1: Patch `evals/run-eval.sh` — support `mode: static` + `checks` format

**Files:**
- Modify: `evals/run-eval.sh`

**Interfaces:**
- Consumes: eval spec JSON. New optional fields: `checks[]` (`{id, desc, assert, regex?, required?}`), `files[]` (paths relative to skill dir, extra static-audit inputs), `passing_score` (for checks: min PASS count; default = all).
- Produces: same CLI (`bash evals/run-eval.sh <skill> [--improve] [--model M]`). Specs with `assertions[]` behave exactly as before. Specs with `checks[]`: checks having `regex` are graded deterministically; checks with only prose `assert` are graded by one `claude -p` LLM-judge call returning strict JSON. Static mode audit input = SKILL.md + `files[]` + top-level `*.py` in the skill dir (this makes the existing `evals/helix-cad-validate.json` runnable WITHOUT modifying it).

- [ ] **Step 1: Verify current failure (the failing test)**

Run: `cd d:/KN-Stack && bash evals/run-eval.sh helix-cad-validate 2>&1 | tail -5`
Expected: FAIL — Python `KeyError: 'assertions'` (spec has only `checks`).

Also record backward-compat baseline: `grep -l '"mode": "static"' evals/*.json` and pick one spec that has `assertions` (e.g. `helix-spec-to-cad.json` if static). Run it and save its score for comparison in Step 4. If no static+assertions spec exists, the compat check in Step 4 is syntax-only (`bash -n`).

- [ ] **Step 2: Patch static-mode input assembly**

In `run-eval.sh`, replace the static branch (currently lines 62-64):

```bash
if [ "$EVAL_MODE" = "static" ]; then
  echo "[1/3] Static audit (reading SKILL.md, no subprocess)..."
  OUTPUT="$SKILL_CONTENT"
fi
```

with:

```bash
if [ "$EVAL_MODE" = "static" ]; then
  echo "[1/3] Static audit (reading SKILL.md + companion files, no subprocess)..."
  OUTPUT="$SKILL_CONTENT"
  SKILL_DIR_PATH=$(dirname "$SKILL_FILE")
  # spec-declared extra files (relative to skill dir)
  EXTRA_FILES=$(python -c "
import json
e = json.load(open('$EVALS_FILE', encoding='utf-8'))
print('\n'.join(e.get('files', [])))
" 2>/dev/null || echo "")
  # top-level .py files in the skill dir (validators live next to SKILL.md)
  for f in "$SKILL_DIR_PATH"/*.py; do
    [ -f "$f" ] && EXTRA_FILES="$EXTRA_FILES
$(basename "$f")"
  done
  while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    if [ -f "$SKILL_DIR_PATH/$rel" ]; then
      OUTPUT="$OUTPUT

===== FILE: $rel =====
$(cat "$SKILL_DIR_PATH/$rel")"
    fi
  done <<< "$(echo "$EXTRA_FILES" | awk '!seen[$0]++')"
fi
```

- [ ] **Step 3: Patch the grader — `checks` branch**

Immediately before `# Step 2: Check assertions via Python` add a format switch, keeping the existing assertions pipeline untouched:

```bash
HAS_CHECKS=$(python -c "
import json
e = json.load(open('$EVALS_FILE', encoding='utf-8'))
print('yes' if 'checks' in e else 'no')
" 2>/dev/null || echo "no")

if [ "$HAS_CHECKS" = "yes" ]; then
  echo "[2/3] Grading checks (regex deterministic + LLM-judge for prose asserts)..."
  EVAL_TMP=$(mktemp -d)
  printf '%s' "$OUTPUT" > "$EVAL_TMP/output.txt"

  # Pass 1: deterministic regex checks; collect prose checks for the judge
  python - "$EVALS_FILE" "$EVAL_TMP" <<'PYEOF'
import json, re, sys
spec = json.load(open(sys.argv[1], encoding='utf-8'))
tmp = sys.argv[2]
output = open(tmp + '/output.txt', encoding='utf-8', errors='replace').read()
det, judge = {}, []
for c in spec['checks']:
    if 'regex' in c:
        det[c['id']] = 'PASS' if re.search(c['regex'], output, re.IGNORECASE) else 'FAIL'
    else:
        judge.append({'id': c['id'], 'desc': c['desc'], 'assert': c['assert']})
json.dump(det, open(tmp + '/det.json', 'w'))
json.dump(judge, open(tmp + '/judge_checks.json', 'w'))
PYEOF

  # Pass 2: single LLM-judge call for prose checks (skipped when none)
  JUDGE_COUNT=$(python -c "import json;print(len(json.load(open('$EVAL_TMP/judge_checks.json'))))")
  if [ "$JUDGE_COUNT" -gt 0 ]; then
    {
      echo "You are a strict auditor. Below is the content under audit, then a JSON list of checks."
      echo "For EACH check decide PASS or FAIL based ONLY on the content. Be literal: if the asserted"
      echo "element is absent, FAIL. Output ONLY a JSON array (no prose, no code fences):"
      echo '[{"id": "...", "verdict": "PASS|FAIL", "reason": "<=20 words"}]'
      echo ""
      echo "===== CONTENT UNDER AUDIT ====="
      cat "$EVAL_TMP/output.txt"
      echo ""
      echo "===== CHECKS ====="
      cat "$EVAL_TMP/judge_checks.json"
    } > "$EVAL_TMP/judge_prompt.txt"
    timeout 300 claude -p $MODEL_FLAG --output-format text < "$EVAL_TMP/judge_prompt.txt" \
      > "$EVAL_TMP/judge_raw.txt" 2>/dev/null || echo "[]" > "$EVAL_TMP/judge_raw.txt"
  else
    echo "[]" > "$EVAL_TMP/judge_raw.txt"
  fi

  # Pass 3: merge + score
  SCORE=$(python - "$EVALS_FILE" "$EVAL_TMP" <<'PYEOF'
import json, re, sys
spec = json.load(open(sys.argv[1], encoding='utf-8'))
tmp = sys.argv[2]
det = json.load(open(tmp + '/det.json'))
raw = open(tmp + '/judge_raw.txt', encoding='utf-8', errors='replace').read()
m = re.search(r'\[.*\]', raw, re.DOTALL)
judged = {}
if m:
    try:
        judged = {v['id']: (v.get('verdict', 'FAIL'), v.get('reason', '')) for v in json.loads(m.group(0))}
    except Exception:
        pass
passed = failed = 0
lines, fails = [], []
for c in spec['checks']:
    cid = c['id']
    if cid in det:
        status, how, reason = det[cid], 'regex', ''
    elif cid in judged:
        status, how = judged[cid][0], 'judge'
        reason = judged[cid][1]
    else:
        status, how, reason = 'FAIL', 'judge', 'no verdict returned (fail-safe)'
    if status == 'PASS':
        passed += 1
    else:
        failed += 1
        fails.append(f"  - {cid}: {c['assert']}" + (f" [{reason}]" if reason else ''))
    req = '*' if c.get('required') else ' '
    lines.append(f"  {cid} [{status}]({how}){req} {c['desc']}")
total = len(spec['checks'])
threshold = spec.get('passing_score', total)
print(f'Score: {passed}/{total} ({passed/total*100:.0f}%)')
print()
print('\n'.join(lines))
print()
if passed == total:
    print('RESULT: PERFECT - no improvement needed')
elif passed >= threshold:
    print(f'RESULT: PASS ({passed} >= {threshold} passing threshold)')
else:
    print(f'RESULT: FAIL ({passed} < {threshold} passing threshold)')
if fails:
    print()
    print('FAILED ASSERTIONS:')
    print('\n'.join(fails))
PYEOF
)
  rm -rf "$EVAL_TMP"
  echo "$SCORE"
  echo ""
else
# ... existing "[2/3] Checking assertions..." block runs unchanged here ...
fi
```

Wrap the ENTIRE existing Step-2 python block (lines 92-159, from `echo "[2/3] Checking assertions..."` through `echo ""` after `echo "$SCORE"`) inside the `else` branch. Do not modify its contents. The Step-3 `--improve` block already keys off `FAILED ASSERTIONS:` in `$SCORE`, so it works for both formats without change.

- [ ] **Step 4: Run tests**

Run: `bash -n evals/run-eval.sh` → Expected: no output (syntax OK).
Run: `bash evals/run-eval.sh helix-cad-validate` → Expected: `[1/3] Static audit`, then `Grading checks`, a per-check list with `(regex)`/`(judge)` tags, and a `RESULT:` line. (Judge verdicts on Assay's mid-edit skill may be PASS or FAIL — the acceptance criterion is that the runner completes and grades, not that the skill scores 10/10.)
Run the baseline spec from Step 1 again → Expected: identical score to baseline (backward compat).

- [ ] **Step 5: Commit**

```bash
git add evals/run-eval.sh
git commit -m "[EVALS] run-eval.sh: support mode=static + checks format (regex deterministic, prose via LLM-judge)"
```

---

### Task 2: Create `topic-notebook` skill

**Files:**
- Create: `skills/galaxy/topic-notebook/SKILL.md`
- Create: `skills/galaxy/topic-notebook/references/registry-schema.md`
- Create: `skills/galaxy/topic-notebook/references/reference-persona.md`

**Interfaces:**
- Produces: `/topic-notebook --register|--add|--query|--refresh|--list|--health` — consumed by `helix-research` (T1 lookups by alias), `helix-project-init` (pin step), Research Hooks.
- Registry lives at `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (created in Task 3).

- [ ] **Step 1: Write `SKILL.md`**

```markdown
---
name: topic-notebook
description: "Persistent topic NotebookLM lifecycle — register/build/query/refresh reference notebooks for recurring workflow topics (standards, VDI methodology, harness doctrine, per-project). Neutral citation-first persona (NOT mentor persona-purity). Unified registry at vault 3_Resources/Topic-Notebooks. Primary T1 LOOKUP executor for /helix-research. Triggers on: 'topic notebook', 'reference notebook', 'notebook chủ đề', 'sổ tay tra cứu', 'đăng ký notebook', 'tra chuẩn MIL-STD', 'query topic notebook', 'notebook thường trực'."
---

# Topic Notebook — Persistent Reference Notebooks

> Harness class: `guide` (knowledge feedforward) + `sensor-inferential` (query answers are propose-only, citation-required).
> Distinct from mentor notebooks (person, persona-purity) and research-sprint notebooks (one-off).

## Operational Envelope

| CAN | CANNOT |
|-----|--------|
| Register existing NLM notebooks into the unified registry | Create Galaxy notes (propose-only, per AI Permissions) |
| Build a new topic notebook AFTER CEO approves seed-sources | Add sources CEO has not approved (source selection = Core) |
| Query registered notebooks, citation-first | Answer from model memory when sources are insufficient |
| Propose refresh candidates | Change a shared mentor notebook's persona |

## Modes

| Mode | Usage |
|------|-------|
| `--register <alias> <nlm-id>` | Register an EXISTING notebook |
| `--add <topic>` | Build a new topic notebook (seed-sources → CEO gate → create → ingest → persona) |
| `--query <alias> "<question>"` | Citation-first lookup |
| `--refresh <alias>` | Propose + ingest new sources (CEO approves) |
| `--list` | Registry table |
| `--health` | Staleness + capacity audit |

## Registry

Single source of truth: `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (append/update per entry; never delete entries — mark `status: retired`). Schema: see `references/registry-schema.md`.

## Workflows

### --register <alias> <nlm-id>
1. `mcp__notebooklm-mcp__notebook_describe` the ID — confirm it exists, capture source count.
2. Ask CEO for 1-line scope if not given.
3. Append entry to registry (schema fields). If the notebook is shared with a mentor (e.g. `harness` ↔ mentor-harness-engineering-council), set `persona: mentor-mode (shared)` and DO NOT reconfigure chat persona.
4. `nlm alias set <alias> <nlm-id>` (best-effort; skip with a note if nlm CLI unavailable).

### --add <topic>
1. Draft seed-sources table, tier-classified S/A/B/C per `research/references/source-tiers.md`. TCVN rows: NEVER fabricate numbers — leave `CEO to supply`.
2. **CEO GATE (Core):** present table; CEO approves/edits source list. STOP until approved.
3. `notebook_create` → `source_add` each approved source (retry: alt-URL → WebFetch-to-text → flag failed).
4. `chat_configure` with `references/reference-persona.md` content.
5. Register (as --register) + report ingest count vs approved count (fail-safe: list every source that failed).

### --query <alias> "<question>"
1. Resolve alias in registry → NLM ID. Unknown alias → show `--list`, stop.
2. `mcp__notebooklm-mcp__notebook_query`. Answer format:
   - Direct answer, each claim with `[source]` citation
   - `Confidence: HIGH/MEDIUM/LOW`
   - **NOT FOUND:** parts of the question the sources do not answer (mandatory when applicable — never fill from model memory)
3. If NOT FOUND is non-empty, propose: `--refresh` with candidate sources, or escalate to `/helix-research` T2.

### --refresh <alias>
1. Propose new source candidates (reuse `/research` Step 1 discovery or CEO-provided URLs), tier-classified.
2. CEO approves (Core) → `source_add` → update registry (`source_count`, `last_refresh`).

### --health
For each registry entry flag: `last_refresh` > 90 days → STALE; `source_count` > 45 → propose facet split per `mentor-board/references/facet-split-strategies.md`; describe-call failure → BROKEN.

## COD
- Register / query / health: **Offload** (auto-OK, report back)
- Seed-source selection, refresh approval, scope definition: **Core (CEO)**
- Notebook naming cleanup: Default (skip unless asked)

## Integration
- `/helix-research` — uses `--query` as Tier-1 LOOKUP executor
- `/helix-project-init` Step 3b — pins aliases into project charter
- `/research` — a finished research-sprint notebook may be promoted via `--register`
- `/nlm` — low-level CLI/MCP plumbing; this skill adds registry + lifecycle + protocol

## Rules
1. Citation-first: every claim carries a source reference. No citation → say NOT FOUND.
2. Registry is append/update only — retired notebooks stay listed with `status: retired`.
3. Shared-with-mentor notebooks: never touch persona (mentor purity).
4. >45 sources → facet split proposal, never silent overflow (NLM cap ~50).
```

- [ ] **Step 2: Write `references/registry-schema.md`**

```markdown
# Topic-Notebook Registry Schema

Location: `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` — append/update only.

Entry format (one `##` section per notebook):

    ## <alias>
    - nlm_id: <uuid>
    - url: https://notebooklm.google.com/notebook/<uuid>
    - scope: <1-line what questions this notebook answers>
    - source_count: <n> (tiers: S:<n> A:<n> B:<n> C:<n> | unknown for registered legacy)
    - persona: reference-mode | mentor-mode (shared with mentor-<name>)
    - status: active | retired
    - created: YYYY-MM-DD · last_refresh: YYYY-MM-DD
    - pinned_projects: [<project-ids or —>]

Rules: alias = kebab-case, unique; date format absolute; retired entries keep their section.
```

- [ ] **Step 3: Write `references/reference-persona.md`**

```markdown
# Reference-Mode Persona (chat_configure payload)

You are a neutral domain expert for Workshop X (Vietnam defense engineering).
Rules:
1. Answer ONLY from the sources in this notebook. Every claim cites its source.
2. When sources do not answer (part of) the question, say exactly which part is
   not covered — never speculate, never fill from general knowledge.
3. Prefer numbers, standard clauses, and tolerances over prose. Metric units only.
4. Quote standard designations exactly as written in the source (never invent
   TCVN/MIL-STD numbers).
5. Answer in the language of the question (Vietnamese or English).
```

- [ ] **Step 4: Create junction + verify**

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\commands\topic-notebook" -Target "d:\KN-Stack\skills\galaxy\topic-notebook"
```
Run: `cd d:/KN-Stack && bash setup.sh --verify` → Expected: all junctions OK (count +1).

- [ ] **Step 5: Commit**

```bash
git add skills/galaxy/topic-notebook
git commit -m "[GALAXY] Add topic-notebook skill — persistent reference notebooks with unified registry"
```

---

### Task 3: Initialize vault registry + `std` seed-sources draft

**Files:**
- Create: `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md` (vault — approved in spec §4.2)
- Create: `skills/galaxy/topic-notebook/references/seed-sources.std.draft.md` (repo)

**Interfaces:**
- Consumes: registry schema from Task 2. Known NLM IDs: VDI 2221 `f6e2b21f`, VDI 2206 `3856a428`, harness `8c7dab78`.
- Produces: 3 active registry entries (`vdi-2221`, `vdi-2206`, `harness`); `std` draft awaiting CEO approval (roadmap trigger).

- [ ] **Step 1: Write the vault registry with 3 entries**

Create `D:\Workshop_X\3_Resources\Topic-Notebooks\_registry.md`:

```markdown
# Topic-Notebook Registry

> Unified registry for persistent topic notebooks. Schema: KN-Stack
> `skills/galaxy/topic-notebook/references/registry-schema.md`. Append/update only.

## vdi-2221
- nlm_id: f6e2b21f
- url: https://notebooklm.google.com/notebook/f6e2b21f
- scope: VDI 2221:2019 systematic design methodology — phases, deliverables, Blatt 1/2
- source_count: unknown (registered legacy)
- persona: reference-mode (unverified — configure on first refresh)
- status: active
- created: 2026-07-11 · last_refresh: 2026-07-11
- pinned_projects: [—]

## vdi-2206
- nlm_id: 3856a428
- url: https://notebooklm.google.com/notebook/3856a428
- scope: VDI 2206 mechatronics V-model — system design phase, domain integration
- source_count: unknown (registered legacy)
- persona: reference-mode (unverified — configure on first refresh)
- status: active
- created: 2026-07-11 · last_refresh: 2026-07-11
- pinned_projects: [—]

## harness
- nlm_id: 8c7dab78
- url: https://notebooklm.google.com/notebook/8c7dab78
- scope: Harness engineering doctrine — Guides/Sensors/Gates, Computational vs Inferential, KHUNG v1.0
- source_count: 13 (mentor seed)
- persona: mentor-mode (shared with mentor-harness-engineering-council — DO NOT reconfigure)
- status: active
- created: 2026-07-11 · last_refresh: 2026-07-11
- pinned_projects: [—]
```

Note: full NLM UUIDs are longer than the 8-char prefixes recorded in skill docs. During execution, run `mcp__notebooklm-mcp__notebook_list` and replace `nlm_id`/`url` with the full UUIDs matched by prefix. If MCP auth fails, keep prefixes and add `- note: id prefix only — resolve full uuid on first query` to each entry.

- [ ] **Step 2: Write `seed-sources.std.draft.md` (CEO approval pending)**

```markdown
# DRAFT seed-sources — topic notebook `std` (MIL-STD / TCVN / STANAG)

> Status: AWAITING CEO APPROVAL (Core). Build via `/topic-notebook --add std` after approval.
> Tier scheme: S = standard/primary · A = authority/OEM · B = professional · C = community.

| # | Source | Tier | URL / access | Note |
|---|--------|------|--------------|------|
| 1 | MIL-STD-810H Environmental Engineering | S | http://everyspec.com/MIL-STD/MIL-STD-0800-0899/MIL-STD-810H_55998/ | Temp/humidity/vibration/salt-fog — P1 CAT 13 |
| 2 | MIL-STD-461G EMI/EMC | S | http://everyspec.com/MIL-STD/MIL-STD-0300-0499/MIL-STD-461G_53571/ | P1 CAT 6 |
| 3 | MIL-STD-882E System Safety | S | http://everyspec.com/MIL-STD/MIL-STD-0800-0899/MIL-STD-882E_41682/ | P1 CAT 7 |
| 4 | MIL-STD-1472H Human Engineering | S | http://everyspec.com/MIL-STD/MIL-STD-1400-1499/MIL-STD-1472H_57041/ | Ergonomics/conscript operators |
| 5 | ASSIST Quick Search (index page) | A | https://quicksearch.dla.mil/qsSearch.aspx | Authoritative status/revision lookup for any MIL-STD |
| 6 | ISO 128 (technical drawing general principles) — summary source | A | CEO to supply licensed copy or authoritative summary | P4 drawing |
| 7 | ISO 2768 general tolerances — summary source | A | CEO to supply licensed copy or authoritative summary | P4 drawing |
| 8 | TCVN <CEO to supply — never fabricated> | S | CEO to supply | Vietnamese national defense standards |
| 9 | STANAG <CEO to select applicable, e.g. 4370 environmental> | S | CEO to supply (NSO public or licensed) | NATO interop where relevant |

Open questions for CEO: which TCVN set applies across products; licensed ISO copies available?
```

- [ ] **Step 3: Verify + commit (repo file only)**

Check both files exist and the registry parses visually (3 `##` sections).

```bash
git add skills/galaxy/topic-notebook/references/seed-sources.std.draft.md
git commit -m "[GALAXY] topic-notebook: std seed-sources draft (CEO approval pending) + vault registry seeded"
```

---

### Task 4: Create `helix-research` skill

**Files:**
- Create: `skills/helix/helix-research/SKILL.md`

**Interfaces:**
- Consumes: `/topic-notebook --query` (T1), `/research` (T2), `/nlm` Mode 8 + `deep-research` plugin (T3), `mentor-board` (judgment escalation), registry aliases, project charter `pinned notebooks`.
- Produces: `/helix-research "<question>"` or `/helix-research --brief <path>`; writes `Research_Response_<brief_id>.md` next to `_pipeline_state.md`. Research Brief + Response schemas below — Research Hooks (Task 5) reference these exact field names.

- [ ] **Step 1: Write `SKILL.md`**

```markdown
---
name: helix-research
description: "HELIX research dispatcher — single entry point for deep research on hard problems across P0-P4. Routes a standardized Research Brief through 3 tiers: T1 LOOKUP (topic-notebook/mentor NLM query, free), T2 SPRINT (/research v4.1 multi-channel with source tiers), T3 DEEP (NLM native Deep Research or deep-research fan-out). AI proposes tier, CEO approves per COD; risk_if_wrong=HIGH forces tier S/A sources; mandatory NOT-FOUND fail-safe (no silent model-memory answers). Triggers on: 'helix research', 'research brief', 'nghiên cứu sâu', 'tra cứu chuẩn', 'nghiên cứu vấn đề khó', 'prior art search', 'knowledge gap research', 'tìm tài liệu kỹ thuật', 'state of the art'."
---

# Helix Research — 3-Tier Research Dispatcher

> Harness class: `guide` (routing) + `sensor-inferential` (responses are cited evidence, propose-only).
> Every HELIX block that needs external knowledge sends a Research Brief here — no block picks its own executor.

## Operational Envelope

| CAN | CANNOT |
|-----|--------|
| Route briefs to T1/T2/T3 and run T1 immediately | Launch T2/T3 without CEO confirmation |
| Compile cited Research Responses | Answer HIGH-risk questions without S/A-tier sources |
| Propose escalation when a tier comes back empty | Fill gaps from model memory silently |
| Write Response files next to `_pipeline_state.md` | Modify pipeline state beyond its ledger line |

## Research Brief (input)

    brief_id: RB-<project>-<seq>          # e.g. RB-VNTGTF-003
    question: <specific research question>
    type: standards | prior-art | working-principle | state-of-the-art | knowledge-gap | market
    phase: P0 | P1 | P2 | P3 | P4
    source_block: <skill that generated it, e.g. helix-p2-firmup>
    risk_if_wrong: LOW | MEDIUM | HIGH    # HIGH => answer must rest on tier S/A sources
    known_sources: [<topic-notebook aliases, from project charter pinned notebooks>]
    deadline: <optional>

Ad-hoc use: `/helix-research "<question>"` — the skill drafts the brief, CEO confirms fields.

## Router

| Tier | Executor | When | COD |
|------|----------|------|-----|
| **T1 LOOKUP** | `/topic-notebook --query <alias>` or mentor NLM `notebook_query` | Lookup question; a registered notebook plausibly covers it (`known_sources` or type→alias map below) | Offload — run immediately, report back |
| **T2 SPRINT** | `/research "<question>"` (v4.1: multi-channel discovery, S/A/B/C tiers, NLM ingest) | New sources needed with tier control; standards/prior-art not covered by a notebook | Offload — **CEO confirms before launch** |
| **T3 DEEP** | `nlm` Mode 8 (NLM Deep Research native, background, token-free) OR `deep-research` plugin (fan-out + adversarial verify, faster, token-heavy) | Open/multi-faceted question, unclear sources; type = knowledge-gap or state-of-the-art | **CEO confirms + picks engine** |

Type→alias defaults for T1: `standards`→`std` (when built; until then T2), methodology→`vdi-2221`/`vdi-2206`, harness→`harness`, plus any charter-pinned alias.

**Routing rules:**
1. Always propose a tier + 1-line rationale. T1 runs immediately; T2/T3 wait for CEO.
2. `risk_if_wrong: HIGH` → final answer must cite tier S/A sources. T1 acceptable only if the notebook's sources are S/A; otherwise escalate to T2.
3. T1 returns NOT FOUND (fully or partially) → auto-propose T2 escalation. NEVER quietly substitute model memory.
4. Judgment questions (trade-off debates, RED subfunctions, doctrine) → route to `/mentor-board` CONSULT/PANEL instead of search. Retrieval ≠ judgment.
5. Patent/prior-art briefs at T2: include Espacenet + Google Patents in the search scope; standards briefs: include ASSIST Quick Search (quicksearch.dla.mil) for MIL-STD status.
6. Two consecutive T3 failures on the same brief → STOP, flag to CEO (roadmap trigger for internal deep-research harness — see HARNESS_STANDARD roadmap).

## Research Response (output)

File: `Research_Response_<brief_id>.md` in the project working folder (next to `_pipeline_state.md`; ad-hoc → current directory).

    # Research Response — <brief_id>
    Question: … · Tier used: T1/T2/T3 · Date: …

    ## Answer
    <each claim followed by [source — tier S/A/B/C]>

    ## NOT FOUND
    <parts of the question the sources did not answer — mandatory section, "—" only if truly complete>

    ## Confidence
    HIGH / MEDIUM / LOW + overall source-tier mix

    ## Next steps (propose-only)
    <escalate tier? add sources to a topic notebook? consult a mentor council?>

Ledger: the calling block appends ONE line to `_pipeline_state.md` Block Ledger:
`Research: <brief_id> → <tier> → <verdict 1-line> (see Research_Response_<brief_id>.md)`.

## COD
- Brief drafting, T1 execution, response compilation: **Offload**
- T2/T3 launch approval, engine choice, accepting a LOW-confidence answer for a HIGH-risk brief: **Core (CEO)**
- Re-running identical briefs: Default (skip — reuse the existing Response)

## Integration
- Called by Research Hooks in: helix-p1-preflight, helix-p1-requirements, helix-p2-frame, helix-p2-firmup, helix-p2-risk (ICDM), helix-domain-debate (escalation)
- Orchestrators list charter-pinned notebooks at Step 1.5 (context enrichment)
- Executors: /topic-notebook, /research, /nlm, /mentor-board, deep-research plugin

## Rules
1. NO block-order changes, no new pipeline blocks — this is a service skill, ONE BLOCK PER TURN untouched.
2. Every Response has a NOT FOUND section. Empty answers are reported, not padded.
3. Citations are per-claim, not per-document.
4. HIGH-risk + no S/A source = no answer; escalate or return NOT FOUND.
```

- [ ] **Step 2: Create junction + verify**

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.claude\commands\helix-research" -Target "d:\KN-Stack\skills\helix\helix-research"
```
Run: `bash setup.sh --verify` → Expected: OK.

- [ ] **Step 3: Commit**

```bash
git add skills/helix/helix-research
git commit -m "[HELIX] Add helix-research — 3-tier research dispatcher (T1 lookup / T2 sprint / T3 deep)"
```

---

### Task 5: Research Hooks — 6 existing HELIX files

**Files:**
- Modify: `skills/helix/helix-p2-firmup/SKILL.md` (insert before the `GROUP C: ROUGH CALCULATIONS` divider, i.e. right after the E-task template block ~line 202)
- Modify: `skills/helix/helix-p1-preflight/SKILL.md` (after line 142 `NOTE: AI lists candidates. CEO CONFIRMS…`)
- Modify: `skills/helix/helix-p1-requirements/SKILL.md` (before `### Step A3b: Seed from Ingested CAD` ~line 115)
- Modify: `skills/helix/helix-p2-frame/SKILL.md` (after line 91 `**Stalled (<3)** = highest-leverage innovation direction for Block BB.`)
- Modify: `skills/helix/helix-p2-risk/SKILL.md` (inside `### ICDM Extension (if --icdm active)` section ~line 222 — append at end of that section, before `## Output`)
- Modify: `skills/helix/helix-domain-debate/SKILL.md` (before `### Step 4: Synthesis + Recommendation` ~line 92)

**Interfaces:**
- Consumes: `/helix-research` Brief schema fields exactly as defined in Task 4 (`brief_id`, `type`, `risk_if_wrong`, `known_sources`).
- Produces: no new outputs — each hook is an optional routing note (10-15 lines). Read each file around the anchor before editing; anchors above were verified 2026-07-11.

- [ ] **Step 1: helix-p2-firmup — L/E executor hook**

Insert:

```markdown
**RESEARCH HOOK (L/E execution):** When CEO marks an L or E task **Offload**, do NOT
"compile options" from model memory. Convert the task brief into a Research Brief and call
`/helix-research`:
- `question` = task Question · `type` = prior-art (L) / market (E) · `phase` = P2
- `source_block` = helix-p2-firmup · `risk_if_wrong` = HIGH if the gap feeds a safety-critical
  or high-weight VDI 2225 criterion, else MEDIUM
- `known_sources` = charter-pinned topic-notebook aliases
The dispatcher proposes T1/T2/T3 (CEO approves T2/T3). Feed the Response's cited findings
back into the gap matrix; anything under **NOT FOUND** stays an open gap for F4 — never
fill it with uncited estimates.
```

- [ ] **Step 2: helix-p1-preflight — standards scan hook**

Insert after the NOTE line:

```markdown
**RESEARCH HOOK (standards):** Before presenting candidates to CEO, query the `std`
topic notebook if registered (`/topic-notebook --query std "applicable standards for
<product class>"`) — cited hits pre-fill the table, and CEO only supplies the gaps.
If `std` is not yet built or returns NOT FOUND, offer a T2 brief via `/helix-research`
(`type: standards`, `risk_if_wrong: HIGH` — defense citations must be tier S/A).
CEO confirmation of applicability remains Core; this hook only reduces the blank-page load.
```

- [ ] **Step 3: helix-p1-requirements — A3 similar-products hook**

Insert before Step A3b:

```markdown
**RESEARCH HOOK (prior art):** After the forge-library pass, if similar-product coverage is
thin (<3 comparable products), offer a Research Brief via `/helix-research`
(`type: prior-art`, `phase: P1`, `source_block: helix-p1-requirements`). Requirements
imported from a Research Response MUST carry the response's citation in their source
column — uncited imports are not allowed.
```

- [ ] **Step 4: helix-p2-frame — TESE hook**

Insert after the Stalled line:

```markdown
**RESEARCH HOOK (state of the art):** TESE scoring above draws on model knowledge, which is
capped at training cutoff. If any trend scores ≤2, or CEO suspects the field moved recently,
raise a Research Brief via `/helix-research` (`type: state-of-the-art`, `phase: P2`) — the
dispatcher will propose T2/T3. Update the trend table only with cited findings; log the
Response file in the ledger line.
```

- [ ] **Step 5: helix-p2-risk — ICDM knowledge-gap hook**

Append at the end of the ICDM Extension section:

```markdown
**RESEARCH HOOK (knowledge gaps):** For every RTA knowledge gap classified NEW, generate one
Research Brief (`type: knowledge-gap`, `phase: P2`, `source_block: helix-p2-risk`,
`risk_if_wrong` = HIGH when the gap sits on a CRITICAL CFMA path) and list the brief_ids in
the gap-closing plan. Gaps with an unanswered brief stay OPEN in the risk register — a plan
line without evidence does not close a gap.
```

- [ ] **Step 6: helix-domain-debate — council escalation**

Insert before Step 4:

```markdown
### Step 3b: Escalation to Real Councils (optional — RED complexity or unresolved contradiction)

The three perspectives above are SIMULATED from the embedded WX knowledge base. When
(a) complexity = RED, or (b) Step 3 contradictions cannot be resolved within this debate,
offer CEO an escalation instead of forcing a synthesis:
- **Judgment question** → `/mentor-board` PANEL or DEBATE with the matching specialist
  council (naval-architect, nswc-hull, torpedo-asw, cdpr-cable-robot, harness-engineering…)
- **Retrieval question** (a fact/benchmark would settle it) → `/helix-research` brief
Record the escalation verdict in the JSON side-car as `"escalated_to"` + summary. Skipping
escalation at RED is a CEO decision (Core), noted in the side-car.
```

- [ ] **Step 7: Verify + commit**

Check: `grep -c "RESEARCH HOOK\|Escalation to Real Councils" skills/helix/helix-p2-firmup/SKILL.md skills/helix/helix-p1-preflight/SKILL.md skills/helix/helix-p1-requirements/SKILL.md skills/helix/helix-p2-frame/SKILL.md skills/helix/helix-p2-risk/SKILL.md skills/helix/helix-domain-debate/SKILL.md` → each ≥1.

```bash
git add skills/helix/helix-p2-firmup/SKILL.md skills/helix/helix-p1-preflight/SKILL.md \
        skills/helix/helix-p1-requirements/SKILL.md skills/helix/helix-p2-frame/SKILL.md \
        skills/helix/helix-p2-risk/SKILL.md skills/helix/helix-domain-debate/SKILL.md
git commit -m "[HELIX] Research Hooks: wire 6 blocks to /helix-research dispatcher"
```

---

### Task 6: Orchestrators + project-init wiring

**Files:**
- Modify: `skills/helix/helix-task-clarify/SKILL.md` (end of `#### 1.5c: CEO Context Enrichment`, before `### Step 2`)
- Modify: `skills/helix/helix-concept-generate/SKILL.md` (same pattern in its Step 1.5)
- Modify: `skills/helix/helix-project-init/SKILL.md` (new `### Step 3b` before `### Step 4: Generate ICD v0 Skeleton`; plus one charter line)

**Interfaces:**
- Consumes: `/topic-notebook --list`, charter `pinned_notebooks` field (introduced here).
- Produces: charter field `Pinned topic notebooks: [aliases]` — read by `helix-research` (`known_sources`).

- [ ] **Step 1: Both orchestrators — add to end of Context Enrichment (identical text)**

```markdown
**Topic notebooks:** List the project's pinned topic-notebook aliases (charter `Pinned
topic notebooks` field; registry: `/topic-notebook --list`). Remind blocks: external-knowledge
needs go through `/helix-research` Research Briefs — no block searches on its own.
```

- [ ] **Step 2: helix-project-init — pin step**

Insert before Step 4:

```markdown
### Step 3b: Pin Topic Notebooks (optional)

Show CEO the topic-notebook registry (`/topic-notebook --list`). CEO picks 0-3 aliases
relevant to this project (e.g. `std`, `vdi-2221`, a per-project notebook). Optionally create
a per-project notebook now (`/topic-notebook --add <project-id>`; seed-source approval is
Core and may be deferred). Write into the charter:

    Pinned topic notebooks: [<alias1>, <alias2>] | [—]

These aliases become `known_sources` defaults for every Research Brief in this project.
```

Also add the line `Pinned topic notebooks: [—]` into the charter template in Step 3 (locate the charter code block and add it near the standards/references fields).

- [ ] **Step 3: Verify + commit**

Check: `grep -l "Pinned topic notebooks" skills/helix/helix-task-clarify/SKILL.md skills/helix/helix-concept-generate/SKILL.md skills/helix/helix-project-init/SKILL.md` → 3 files.

```bash
git add skills/helix/helix-task-clarify/SKILL.md skills/helix/helix-concept-generate/SKILL.md skills/helix/helix-project-init/SKILL.md
git commit -m "[HELIX] Orchestrators + project-init: pinned topic notebooks + research routing note"
```

---

### Task 7: `docs/HARNESS_STANDARD.md`

**Files:**
- Create: `docs/HARNESS_STANDARD.md`

**Interfaces:**
- Consumes: audit findings (spec §1.3), KHUNG HARNESS ENGINEERING v1.0 vocabulary (mentor persona).
- Produces: `harness_class` frontmatter convention for future skills; naming rule (no "Gate/BLOCK" without enforcement); gates roadmap with triggers.

- [ ] **Step 1: Write the document** — six sections per spec §6.2, content:

```markdown
# HARNESS_STANDARD — Guides–Sensors–Gates cho KN-Stack

> v1.0 · 2026-07-11 · Áp dụng cho MỌI skill mới; skill cũ refactor dần theo trigger.
> Nguồn doctrine: KHUNG HARNESS ENGINEERING v1.0 (VN-SIM-TECH) + mentor-harness-engineering-council.

## 1. Vocabulary bắt buộc
- **Guide** (feedforward): hướng dẫn nạp trước — SKILL.md, template, contract, AGENTS.md.
- **Sensor** (feedback): chấm sau khi có output. **Computational** = script tất định (regex/schema/exit-code, chạy máy được); **Inferential** = LLM chấm theo rubric (propose-only).
- **Gate** (cưỡng chế): chặn hành động rủi ro bằng CƠ CHẾ — exit-code, hash-lock, hook chặn. "Cơ chế không phải prompt."
- **Improvement Engine**: mỗi lỗi lặp lại được xác nhận → nâng thành luật Computational (fix-it-once).
- **Fail-safe**: thiếu dữ liệu cho check tới hạn → FAIL/NOT FOUND, không bao giờ silent skip.

## 2. Khai báo class (skill mới BẮT BUỘC)
Frontmatter hoặc dòng đầu body: `Harness class: guide | sensor-computational | sensor-inferential | gate`.
**Quy tắc nhãn:** cấm chữ "Gate/BLOCK/halt" nếu không có cơ chế cưỡng chế thật. Checklist LLM = "review (Inferential, propose-only)". Vi phạm nhãn = defect, sửa như bug.

## 3. Eval bắt buộc
Orchestrator / mega-skill / gate mới → PHẢI có `evals/<skill>.json` cùng PR. Mode `static` + `checks` cho skill không chạy 1-shot; check nào regex-hóa được thì regex (Computational), phần còn lại prose assert (LLM-judge).

## 4. Improvement Engine loop
Mẫu chuẩn: `helix-design-review` (Inferential finding) → kỹ sư xác nhận lặp lại → luật mới trong `design_rules.json` (bump version + re-hash) → `helix-cad-validate` hấp thu. Mọi cặp Sensor-Inferential/Gate-Computational mới theo đúng vòng này.

## 5. Phân loại hiện trạng (audit 2026-07-11)
| Thành phần | Nhãn tự xưng | Class thật | Ghi chú |
|---|---|---|---|
| helix-cad-validate (validate.py) | Gate | **gate** (exit 2, hash-lock, provenance) | Mẫu mực duy nhất |
| helix-design-review | propose-only | sensor-inferential | Đúng nhãn |
| aigate (FORGE-F 7-check) | "Gate/BLOCK" | sensor-inferential | Nhãn quá — không cưỡng chế |
| qc (Defense QC 10-check) | "Gate/halt" | sensor-inferential | Check-02 HITL "halt" chỉ là chữ |
| helix-quality-gate | Gate 1-4 | sensor-inferential + HITL Core | A-items chưa script-hóa |
| hooks (3 bash) | — | sensor-computational (soft) | Đo lường, không chặn |
| run-eval.sh + evals/*.json | — | sensor-computational (nông) | regex keyword-level |

## 6. Roadmap Gates còn thiếu (dựng theo TRIGGER, không dựng trước)
| Gate | Pha | Trigger dựng |
|---|---|---|
| Script-hóa helix-quality-gate P02 A-items | Thiết kế | HARNESS_STANDARD áp 1 quý + gate dùng ≥5 lần/quý |
| AI-QC hàn/NDT false-negative sensor | Chế tạo | forge-fabrication chạy sản phẩm hàn nhôm đầu tiên qua F3 |
| Eval coupon (thử nghiệm vật lý) | Thử nghiệm | Bench test campaign đầu tiên có ≥2 vòng lặp |
| CI gate cấm auto-merge mã AI vào firmware tới hạn | Lập trình | Repo firmware đầu tiên có CI |
| Earned-autonomy gate (cấp quyền theo năng lực đã chứng minh) | Toàn hệ | ≥3 gate Computational vận hành ổn định 1 quý |
| Deep-research harness nội bộ | Research | T3 executor fail lặp ≥3 lần trên cùng loại brief |
```

- [ ] **Step 2: Commit**

```bash
git add docs/HARNESS_STANDARD.md
git commit -m "[DOCS] HARNESS_STANDARD v1.0 — Guides-Sensors-Gates cho toàn workflow + gates roadmap"
```

---

### Task 8: Eval specs for the two new skills + run

**Files:**
- Create: `evals/helix-research.json`
- Create: `evals/topic-notebook.json`

**Interfaces:**
- Consumes: Task-1 runner (`mode: static` + `checks`), SKILL.md contents from Tasks 2/4.
- Produces: two passing evals; dogfoods the new runner path.

- [ ] **Step 1: Write `evals/helix-research.json`** (all-regex → fully deterministic)

```json
{
  "skill": "helix-research",
  "mode": "static",
  "description": "Static audit: helix-research honors the dispatcher contract (3 tiers, COD gates, fail-safe, citations).",
  "checks": [
    {"id": "frontmatter-valid", "desc": "name matches directory; description has Triggers on with VI+EN", "assert": "frontmatter name + bilingual triggers", "regex": "name: helix-research[\\s\\S]*Triggers on:[\\s\\S]*nghiên cứu", "required": true},
    {"id": "three-tiers", "desc": "router defines T1 LOOKUP, T2 SPRINT, T3 DEEP", "assert": "all three tiers present", "regex": "T1 LOOKUP[\\s\\S]*T2 SPRINT[\\s\\S]*T3 DEEP", "required": true},
    {"id": "cod-gate", "desc": "T2/T3 require CEO confirmation", "assert": "CEO confirms before T2/T3 launch", "regex": "CEO confirms? (before|\\+)", "required": true},
    {"id": "high-risk-tier", "desc": "risk_if_wrong HIGH forces S/A sources", "assert": "HIGH risk => tier S/A", "regex": "risk_if_wrong[\\s\\S]*HIGH[\\s\\S]*S/A", "required": true},
    {"id": "fail-safe-notfound", "desc": "mandatory NOT FOUND section, no model-memory fill", "assert": "NOT FOUND mandatory + no silent memory answers", "regex": "NOT FOUND[\\s\\S]*(model memory|mô hình)", "required": true},
    {"id": "citation-per-claim", "desc": "citations are per-claim", "assert": "per-claim citation rule", "regex": "per-claim|each claim", "required": true},
    {"id": "judgment-routing", "desc": "judgment questions route to mentor-board not search", "assert": "mentor-board routing rule", "regex": "mentor-board[\\s\\S]*(judgment|Retrieval)", "required": true},
    {"id": "pipeline-safe", "desc": "no block-order change, ONE BLOCK PER TURN preserved", "assert": "pipeline safety rule", "regex": "ONE BLOCK PER TURN", "required": true}
  ],
  "passing_score": 8
}
```

- [ ] **Step 2: Write `evals/topic-notebook.json`**

```json
{
  "skill": "topic-notebook",
  "mode": "static",
  "description": "Static audit: topic-notebook honors registry, citation-first persona, CEO source gate, capacity rules.",
  "checks": [
    {"id": "frontmatter-valid", "desc": "name matches directory; bilingual triggers", "assert": "frontmatter + triggers", "regex": "name: topic-notebook[\\s\\S]*Triggers on:[\\s\\S]*notebook chủ đề", "required": true},
    {"id": "six-modes", "desc": "register/add/query/refresh/list/health all defined", "assert": "all six modes", "regex": "--register[\\s\\S]*--add[\\s\\S]*--query[\\s\\S]*--refresh[\\s\\S]*--list[\\s\\S]*--health", "required": true},
    {"id": "ceo-source-gate", "desc": "seed-source selection is Core, STOP until approved", "assert": "CEO gate on sources", "regex": "CEO GATE \\(Core\\)|source selection = Core", "required": true},
    {"id": "citation-first", "desc": "every claim cites; NOT FOUND instead of memory", "assert": "citation-first + fail-safe", "regex": "[Cc]itation-first[\\s\\S]*NOT FOUND", "required": true},
    {"id": "registry-path", "desc": "unified vault registry path declared", "assert": "registry path present", "regex": "Topic-Notebooks..?_registry\\.md", "required": true},
    {"id": "mentor-purity", "desc": "shared mentor notebooks keep their persona", "assert": "no persona reconfigure on shared", "regex": "persona.*mentor|mentor.*purity", "required": true},
    {"id": "facet-split", "desc": ">45 sources triggers facet split proposal", "assert": "capacity rule", "regex": ">\\s?45[\\s\\S]*facet", "required": true},
    {"id": "tcvn-no-fabricate", "desc": "TCVN numbers never fabricated", "assert": "TCVN rule", "regex": "NEVER fabricate", "required": true}
  ],
  "passing_score": 8
}
```

- [ ] **Step 3: Run both, fix regex-vs-content drift until PASS**

Run: `bash evals/run-eval.sh helix-research` → Expected: `Score: 8/8` `RESULT: PERFECT`.
Run: `bash evals/run-eval.sh topic-notebook` → Expected: `Score: 8/8` `RESULT: PERFECT`.
If a check fails, first decide which side is wrong (spec regex too strict vs SKILL.md missing the contract element) and fix that side.

- [ ] **Step 4: Commit**

```bash
git add evals/helix-research.json evals/topic-notebook.json
git commit -m "[EVALS] Static checks evals for helix-research + topic-notebook (dogfood checks-mode runner)"
```

---

### Task 9: Final verification + PR

**Files:** none new.

- [ ] **Step 1: Full verification pass**

- `bash setup.sh --verify` → all junctions OK
- `bash setup.sh --status` → skill count +2 (helix 55→56 nominal, galaxy 12→13 nominal — record actual numbers)
- `bash evals/run-eval.sh helix-research && bash evals/run-eval.sh topic-notebook` → both PASS
- `git status` → ONLY the pre-existing Assay dirty files remain unstaged; nothing of ours left over

- [ ] **Step 2: Push + PR**

```bash
git push -u origin feature/helix-research-layer
gh pr create --base feature/evals-static-mode --title "[HELIX] Research layer: 3-tier dispatcher + topic notebooks + checks-mode eval runner" --body "$(cat <<'EOF'
## Summary
- helix-research: 3-tier research dispatcher (T1 notebook lookup / T2 /research sprint / T3 deep research), Research Brief/Response contracts, COD-gated
- topic-notebook: persistent reference notebooks — unified vault registry, citation-first persona, CEO source gate; seeded vdi-2221/vdi-2206/harness + std seed-sources draft
- Research Hooks in 6 HELIX blocks + orchestrators Step 1.5 + project-init pin step
- run-eval.sh: mode=static + checks format (regex deterministic, prose asserts via LLM-judge) — closes the gap where evals/helix-cad-validate.json could not run
- docs/HARNESS_STANDARD.md v1.0 + 2 new static evals (8/8 each)

## Notes
- VERSION/CHANGELOG bump DEFERRED: both files carry uncommitted [1.6.0] hunks from the in-flight Assay workstream; bumping here would stage foreign work. Bump in a follow-up once Assay lands.
- Spec: docs/superpowers/specs/2026-07-11-helix-research-layer-design.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- [ ] **Step 3: Report** — summarize to CEO: what shipped, eval scores, the two pending CEO Core items (approve `std` seed-sources; decide when to bump VERSION/CHANGELOG after Assay lands).
