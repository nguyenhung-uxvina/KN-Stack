#!/usr/bin/env bash
# IPARAG Stop Hook — Compound learning reminder
# Fires once per day max. Checks if learnings were logged today.
# Exit 0 always (non-blocking).

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo ".")"
TODAY=$(date +%Y-%m-%d)
FLAG="$REPO_ROOT/.claude/hooks/.learnings-reminded-${TODAY}"

# Already reminded today? Exit silently.
if [ -f "$FLAG" ]; then
  exit 0
fi

# Check if today's date appears in learnings.md
LEARNINGS_FILE="$REPO_ROOT/_meta/learnings.md"
if [ -f "$LEARNINGS_FILE" ] && grep -q "\[$TODAY\]" "$LEARNINGS_FILE" 2>/dev/null; then
  # Learnings already logged today — no reminder needed
  exit 0
fi

# No learnings logged today — output reminder
cat <<EOF
⚠️ No learnings logged today ($TODAY).
Before ending, append ≥1 insight to _meta/learnings.md:
Format: [$TODAY] [topic] — [insight] → [action taken]
EOF

# Set flag so we don't remind again today
touch "$FLAG"

# Clean up old flags (keep last 2 days)
find "$REPO_ROOT/.claude/hooks/" -name ".learnings-reminded-*" -mtime +2 -delete 2>/dev/null

exit 0
