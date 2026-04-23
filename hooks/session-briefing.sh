#!/usr/bin/env bash
# IPARAG SessionStart Hook — Smart-filtered briefing
# Reads vault state, surfaces only warnings and relevant context.
# Exit 0 always (non-blocking).
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"
META_DIR="$REPO_ROOT/_meta"
PROJECTS_DIR="$REPO_ROOT/1_Projects"

# Step 0: Read source from stdin JSON (startup|resume|compact)
INPUT=$(cat)
SOURCE=$(echo "$INPUT" | grep -o '"source":"[^"]*"' | head -1 | sed 's/"source":"//;s/"//' || echo "startup")

# Collect warnings
WARNINGS=""
LEARNINGS_BLOCK=""
PROGRESS_LINE=""

# Step 1: Read dP/dt from system-health.md
if [ -f "$META_DIR/system-health.md" ]; then
  if grep -q "dP/dt.*unknown\|dP/dt.*0\|Chưa đo" "$META_DIR/system-health.md" 2>/dev/null; then
    WARNINGS="${WARNINGS}⚠️ dP/dt status unclear — check Physical-Validation-Log\n"
  fi
fi

# Step 2: Read learnings (skip on compact)
if [ "$SOURCE" != "compact" ] && [ -f "$META_DIR/learnings.md" ]; then
  RECENT=$(grep "^\[" "$META_DIR/learnings.md" 2>/dev/null | tail -10 || true)
  if [ -n "$RECENT" ]; then
    LEARNINGS_BLOCK="\n### Recent Learnings (last 10)\n$RECENT"
  fi
fi

# Step 3: Check project Status.md staleness (skip on compact)
if [ "$SOURCE" != "compact" ] && [ -d "$PROJECTS_DIR" ]; then
  SEVEN_DAYS_AGO=$(date -d "7 days ago" +%s 2>/dev/null || date -v-7d +%s 2>/dev/null || echo "0")
  STALE_PROJECTS=""

  for status_file in "$PROJECTS_DIR"/*/Status.md; do
    [ -f "$status_file" ] || continue
    FILE_MOD=$(stat -c %Y "$status_file" 2>/dev/null || stat -f %m "$status_file" 2>/dev/null || echo "0")
    if [ "$FILE_MOD" -lt "$SEVEN_DAYS_AGO" ] 2>/dev/null; then
      PROJECT_NAME=$(basename "$(dirname "$status_file")")
      DAYS_OLD=$(( ($(date +%s) - FILE_MOD) / 86400 ))
      STALE_PROJECTS="${STALE_PROJECTS}⚠️ ${PROJECT_NAME} Status.md stale (${DAYS_OLD} days)\n"
    fi
  done

  if [ -n "$STALE_PROJECTS" ]; then
    WARNINGS="${WARNINGS}${STALE_PROJECTS}"
  fi
fi

# Step 3b: Read Active Projects from vault-map.md (skip on compact)
PROJECTS_TABLE=""
if [ "$SOURCE" != "compact" ] && [ -f "$META_DIR/vault-map.md" ]; then
  PROJECTS_TABLE=$(sed -n '/## Active Projects/,/^$/p' "$META_DIR/vault-map.md" | grep "^|" || true)
fi

# Step 4: Check MAKE:THINK ratio from skill-usage.csv (7-day window)
RATIO_WARNING=""
if [ -f "$META_DIR/skill-usage.csv" ]; then
  SEVEN_DAYS_AGO_DATE=$(date -d "7 days ago" +%Y-%m-%d 2>/dev/null || date -v-7d +%Y-%m-%d 2>/dev/null || echo "")
  if [ -n "$SEVEN_DAYS_AGO_DATE" ]; then
    MAKE_COUNT=$(awk -F',' -v since="$SEVEN_DAYS_AGO_DATE" '$1 >= since && $4 == "MAKE" {c++} END {print c+0}' "$META_DIR/skill-usage.csv" 2>/dev/null || echo "0")
    THINK_COUNT=$(awk -F',' -v since="$SEVEN_DAYS_AGO_DATE" '$1 >= since && $4 == "THINK" {c++} END {print c+0}' "$META_DIR/skill-usage.csv" 2>/dev/null || echo "0")
    CHECK_COUNT=$(awk -F',' -v since="$SEVEN_DAYS_AGO_DATE" '$1 >= since && $4 == "CHECK" {c++} END {print c+0}' "$META_DIR/skill-usage.csv" 2>/dev/null || echo "0")
    if [ "$THINK_COUNT" -gt "$MAKE_COUNT" ] 2>/dev/null && [ "$THINK_COUNT" -gt 0 ] 2>/dev/null; then
      RATIO_WARNING="⚠️ MAKE:THINK ratio (7d): ${MAKE_COUNT}:${THINK_COUNT} — Analyst Trap risk. Ưu tiên /req /morpho /layout\n"
      WARNINGS="${WARNINGS}${RATIO_WARNING}"
    fi
  fi
fi

# Step 4b: Check for progress.md (WIP)
if [ -f "$REPO_ROOT/progress.md" ]; then
  PROGRESS_LINE="\n📋 WIP detected — run /catchup to resume"
fi

# Step 5: Compose output
TODAY=$(date +%Y-%m-%d)

if [ -z "$WARNINGS" ] && [ -z "$PROGRESS_LINE" ]; then
  LEARNINGS_COUNT=$(grep -c "^\[" "$META_DIR/learnings.md" 2>/dev/null || echo "0")
  echo "✅ System healthy. ${LEARNINGS_COUNT} learnings loaded."
else
  echo "<session-briefing>"
  echo "## IPARAG Session Briefing — $TODAY"
  if [ -n "$WARNINGS" ]; then
    echo ""
    echo "### Alerts"
    echo -e "$WARNINGS"
  fi
  if [ -n "$LEARNINGS_BLOCK" ]; then
    echo -e "$LEARNINGS_BLOCK"
  fi
  if [ -n "$PROJECTS_TABLE" ]; then
    echo ""
    echo "### Active Projects"
    echo "$PROJECTS_TABLE"
  fi
  if [ -n "$PROGRESS_LINE" ]; then
    echo -e "$PROGRESS_LINE"
  fi
  echo "</session-briefing>"
fi

exit 0
