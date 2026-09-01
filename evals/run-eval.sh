#!/bin/bash
# Self-improving skill eval runner
# Usage: bash run-eval.sh <skill-name> [--improve]
#
# 1. Runs the skill via claude -p
# 2. Checks output against evals/<skill>.json binary assertions
# 3. Reports score
# 4. If --improve: asks Claude to improve the skill.md based on failed assertions

set -euo pipefail
export NO_COLOR=1
export PYTHONIOENCODING=utf-8

SKILL_NAME="${1:?Usage: run-eval.sh <skill-name> [--improve] [--model MODEL]}"
IMPROVE=""
MODEL_FLAG=""

# Parse arguments
shift
while [ $# -gt 0 ]; do
  case "$1" in
    --improve) IMPROVE="--improve" ;;
    --model) MODEL_FLAG="--model $2"; shift ;;
    *) ;;
  esac
  shift
done
VAULT_ROOT="$(git rev-parse --show-toplevel)"
EVALS_FILE="$VAULT_ROOT/evals/${SKILL_NAME}.json"
SKILL_DIR="$HOME/.claude/commands"
SKILL_FILE=""

# Find skill file
if [ -f "$SKILL_DIR/${SKILL_NAME}.md" ]; then
  SKILL_FILE="$SKILL_DIR/${SKILL_NAME}.md"
elif [ -f "$SKILL_DIR/${SKILL_NAME}/SKILL.md" ]; then
  SKILL_FILE="$SKILL_DIR/${SKILL_NAME}/SKILL.md"
else
  echo "ERROR: Skill file not found for: $SKILL_NAME"
  exit 1
fi

if [ ! -f "$EVALS_FILE" ]; then
  echo "ERROR: Evals file not found: $EVALS_FILE"
  exit 1
fi

echo "=== Skill Eval: $SKILL_NAME ==="
echo "Skill: $SKILL_FILE"
echo "Evals: $EVALS_FILE"
echo ""

# Step 1: Get skill output (runtime: spawn claude -p; static: read SKILL.md directly)
SKILL_CONTENT=$(cat "$SKILL_FILE")

EVAL_MODE=$(python -c "
import json
e = json.load(open('$EVALS_FILE', encoding='utf-8'))
print(e.get('mode', 'runtime'))
" 2>/dev/null || echo "runtime")

if [ "$EVAL_MODE" = "static" ]; then
  # Two independent widenings of the static audit, kept separate on purpose:
  #   (A) include_references  -> references/*.md          [opt-in]
  #   (B) files: [...]        -> named companion files    [opt-in]
  #       plus top-level *.py next to SKILL.md            [automatic]
  SKILL_DIR_PATH=$(dirname "$SKILL_FILE")
  OUTPUT="$SKILL_CONTENT"
  AUDIT_PARTS="SKILL.md"

  # (A) Opt-in per spec: "include_references": true also audits references/*.md.
  # Opt-in on purpose — turning this on globally would let a keyword in any
  # reference file satisfy an assertion written against SKILL.md, silently
  # weakening every existing static eval.
  INCLUDE_REFS=$(python -c "
import json
e = json.load(open('$EVALS_FILE', encoding='utf-8'))
print('yes' if e.get('include_references') else 'no')
" 2>/dev/null || echo "no")

  if [ "$INCLUDE_REFS" = "yes" ]; then
    REF_DIR="$SKILL_DIR_PATH/references"
    if [ -d "$REF_DIR" ]; then
      REF_COUNT=$(find "$REF_DIR" -maxdepth 1 -name '*.md' | wc -l)
      OUTPUT="$OUTPUT
$(cat "$REF_DIR"/*.md 2>/dev/null)"
      AUDIT_PARTS="$AUDIT_PARTS + $REF_COUNT reference file(s)"
    else
      AUDIT_PARTS="$AUDIT_PARTS (include_references set but no references/ dir)"
    fi
  fi

  # (B) spec-declared extra files (relative to skill dir)
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
  EXTRA_COUNT=0
  while IFS= read -r rel; do
    [ -z "$rel" ] && continue
    if [ -f "$SKILL_DIR_PATH/$rel" ]; then
      OUTPUT="$OUTPUT

===== FILE: $rel =====
$(cat "$SKILL_DIR_PATH/$rel")"
      EXTRA_COUNT=$((EXTRA_COUNT + 1))
    fi
  done <<< "$(echo "$EXTRA_FILES" | awk '!seen[$0]++')"
  [ "$EXTRA_COUNT" -gt 0 ] && AUDIT_PARTS="$AUDIT_PARTS + $EXTRA_COUNT companion file(s)"

  echo "[1/3] Static audit ($AUDIT_PARTS, no subprocess)..."
else
  echo "[1/3] Running skill via claude -p..."
  TEST_INPUT=$(python -c "
import json
e = json.load(open('$EVALS_FILE', encoding='utf-8'))
print(e.get('test_input', ''))
" 2>/dev/null || echo "")

  if [ -n "$TEST_INPUT" ]; then
    echo "Test input: $TEST_INPUT"
    PROMPT="You are executing a skill. Here are the skill instructions:\n\n${SKILL_CONTENT}\n\n---\n\nNow execute the skill with this input: ${TEST_INPUT}\n\nProduce the output as if the user ran: /${SKILL_NAME} ${TEST_INPUT}\nDo NOT ask clarifying questions — generate the best output you can with available context."
  else
    PROMPT="$SKILL_CONTENT"
  fi

  OUTPUT=$(echo -e "$PROMPT" | timeout 600 claude -p $MODEL_FLAG --permission-mode acceptEdits --output-format text 2>/dev/null || echo "TIMEOUT_OR_ERROR")

  if [ "$OUTPUT" = "TIMEOUT_OR_ERROR" ]; then
    echo "ERROR: Skill execution failed or timed out"
    exit 1
  fi
fi

WORD_COUNT=$(echo "$OUTPUT" | wc -w)
echo "Output: $WORD_COUNT words"
echo ""

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
  JUDGE_COUNT=$(python -c "import json,sys;print(len(json.load(open(sys.argv[1]))))" "$EVAL_TMP/judge_checks.json")
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
# Step 2: Check assertions via Python
echo "[2/3] Checking assertions..."
SCORE=$(python -c "
import json, re, sys

evals = json.load(open('$EVALS_FILE', encoding='utf-8'))
output = sys.stdin.read()
word_count = len(output.split())

passed = 0
failed = 0
total = len(evals['assertions'])
results = []

for a in evals['assertions']:
    aid = a['id']
    name = a['name']
    req = a.get('required', False)

    # Check regex-based assertions
    if 'regex' in a:
        match = bool(re.search(a['regex'], output, re.IGNORECASE))
        status = 'PASS' if match else 'FAIL'
    # Check word count assertions
    elif 'max_words' in a:
        match = word_count <= a['max_words']
        status = 'PASS' if match else 'FAIL'
    else:
        status = 'SKIP'
        match = True

    if match:
        passed += 1
    else:
        failed += 1

    req_tag = '*' if req else ' '
    results.append(f'  {aid} [{status}]{req_tag} {name}')

score_pct = (passed / total * 100) if total > 0 else 0
print(f'Score: {passed}/{total} ({score_pct:.0f}%)')
print(f'Required passed: {sum(1 for a in evals[\"assertions\"] if a.get(\"required\") and re.search(a.get(\"regex\",\"\"), output, re.IGNORECASE))} / {evals[\"total_required\"]}')
print()
for r in results:
    print(r)
print()
if score_pct == 100:
    print('RESULT: PERFECT - no improvement needed')
elif passed >= evals.get('passing_score', 4):
    print(f'RESULT: PASS ({passed} >= {evals.get(\"passing_score\", 4)} passing threshold)')
else:
    print(f'RESULT: FAIL ({passed} < {evals.get(\"passing_score\", 4)} passing threshold)')

# Output failed assertions for improvement
if failed > 0:
    print()
    print('FAILED ASSERTIONS:')
    for a in evals['assertions']:
        if 'regex' in a:
            if not re.search(a['regex'], output, re.IGNORECASE):
                print(f'  - {a[\"id\"]}: {a[\"check\"]}')
        elif 'max_words' in a:
            if word_count > a['max_words']:
                print(f'  - {a[\"id\"]}: {a[\"check\"]} (actual: {word_count} words)')
" <<< "$OUTPUT")

echo "$SCORE"
echo ""
fi

# Step 3: If --improve, ask Claude to fix the skill
if [ "$IMPROVE" = "--improve" ]; then
  FAILED=$(echo "$SCORE" | grep -A 100 "FAILED ASSERTIONS:" || echo "")
  if [ -n "$FAILED" ]; then
    echo "[3/3] Requesting skill improvement..."
    IMPROVE_PROMPT="You are improving a Claude Code skill file. The skill was evaluated against binary assertions and some FAILED.

Current skill file:
---
$(cat "$SKILL_FILE")
---

Failed assertions:
$FAILED

Instructions:
1. Read the skill file carefully
2. Identify why each assertion failed (the skill instructions don't guide Claude to produce output matching the assertion)
3. Add specific instructions to the skill file that would make the output pass ALL assertions
4. Output ONLY the improved skill file content (no explanation, no markdown code blocks)
5. Keep all existing functionality — only ADD instructions to fix failed assertions
6. Do NOT remove any existing content"

    IMPROVED=$(echo "$IMPROVE_PROMPT" | timeout 120 claude -p --permission-mode acceptEdits --output-format text 2>/dev/null || echo "")

    if [ -n "$IMPROVED" ] && [ ${#IMPROVED} -gt 100 ]; then
      # Backup original
      cp "$SKILL_FILE" "${SKILL_FILE}.bak"
      # Write improved version
      echo "$IMPROVED" > "$SKILL_FILE"
      echo "Skill updated. Backup at: ${SKILL_FILE}.bak"
      echo "Run eval again to verify improvement."
    else
      echo "Improvement generation failed or too short. No changes made."
    fi
  else
    echo "[3/3] All assertions passed — no improvement needed."
  fi
else
  echo "Run with --improve to auto-fix failed assertions."
fi

echo ""
echo "=== Done ==="
