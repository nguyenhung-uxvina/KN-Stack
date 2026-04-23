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
  case "$CMD" in
    req|morpho|eval|layout|dfx|bom|gate|mil|plan)
      TIER="MAKE" ;;
    analyst-trap|catchup|reflect|review-plan)
      TIER="CHECK" ;;
    analyze|systems|odi|yckt|research|nlm-query|skill-upgrade|first-principles)
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
