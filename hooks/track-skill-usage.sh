#!/bin/bash
# Skill usage tracker — logs /command invocations to _meta/skill-usage.csv
# Triggered by UserPromptSubmit hook (async, non-blocking)
# No jq, no grep -P — pure bash + sed for Windows Git Bash compatibility
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
CSV="$REPO_ROOT/_meta/skill-usage.csv"

# Read stdin JSON
INPUT=$(cat)

# Extract "content" field value using sed
PROMPT=$(echo "$INPUT" | sed -n 's/.*"content"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -z "$PROMPT" ] && PROMPT=$(echo "$INPUT" | sed -n 's/.*"message"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -z "$PROMPT" ] && PROMPT=$(echo "$INPUT" | sed -n 's/.*"prompt"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

# Check if starts with / (slash command)
if [[ "$PROMPT" =~ ^/([a-zA-Z0-9_-]+) ]]; then
  CMD="${BASH_REMATCH[1]}"
  SESSION=$(echo "$INPUT" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  [ -z "$SESSION" ] && SESSION="unknown"
  TIMESTAMP=$(date '+%Y-%m-%d,%H:%M:%S')

  # Classify command tier: MAKE > CHECK > THINK
  # Glob patterns cover skill families; keep in sync with skills/ domains.
  case "$CMD" in
    # MAKE — produce artifacts / move toward physical or production output
    helix-p[1-4]-*|helix-task-clarify|helix-concept-generate|helix-embody-realize|helix-detail-finalize|helix-project-init|helix-draw|forge-fabrication|erp-*|bom|lcc|6flow|icd|arch|init|clarify|concept|embody|detail|layout|dfx|physical-sprint|pr)
      TIER="MAKE" ;;
    # CHECK — verify / gate / review
    analyst-trap|ratio-check|qc|aigate|verify|helix-quality-gate|gate0|gate1|gate2|gate3|bridge-deploy-gate|helix-shadow-dev|catchup|reflect|code-review|review-plan)
      TIER="CHECK" ;;
    # THINK — analysis / strategy / research
    analyze|first-principles|decide|cld|leverage|archetype|constraint|paradigm|research|research-to-skill|skill-from-research|learning|learn-*|forge-job-map|forge-shift|forge-scout|forge-evolve|jobs|odi|opp|seg|outcomes|bridge-judgment|teach|mentor-*|nlm)
      TIER="THINK" ;;
    *)
      TIER="OTHER" ;;
  esac

  # Create header if file doesn't exist
  if [ ! -f "$CSV" ]; then
    echo "date,time,command,tier,session_id" > "$CSV"
  fi

  echo "$TIMESTAMP,$CMD,$TIER,$SESSION" >> "$CSV"
fi
