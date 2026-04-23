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
EVALS_FILE="$VAULT_ROOT/_meta/evals/${SKILL_NAME}.json"
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

# Step 1: Run the skill
echo "[1/3] Running skill..."
SKILL_CONTENT=$(cat "$SKILL_FILE")

# Extract test_input from evals JSON (if present)
TEST_INPUT=$(python -c "
import json, sys
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

WORD_COUNT=$(echo "$OUTPUT" | wc -w)
echo "Output: $WORD_COUNT words"
echo ""

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
