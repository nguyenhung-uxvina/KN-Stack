#!/usr/bin/env bash
# build.sh — assemble the portable leo-ai plugin from KN-Stack canonical sources.
# Idempotent: wipes skills/ + mcp/ then re-copies and scrubs sensitive files.
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
KN_ROOT="$(cd "$PLUGIN_DIR/../.." && pwd)"

echo "== leo-ai plugin build =="
echo "Plugin: $PLUGIN_DIR"
echo "Source: $KN_ROOT"

# 0. Guard: refuse to wipe when canonical sources are absent (this plugin folder
#    may BE the only copy — e.g. repo layouts where KN-Stack canonical trees moved).
for src in "$KN_ROOT/skills/helix/leo-assist" "$KN_ROOT/skills/helix/leo-prompt" \
           "$KN_ROOT/skills/helix/leo-bridge" "$KN_ROOT/skills/mentors/mentor-getleo-ai" \
           "$KN_ROOT/mcp/leo-bridge"; do
  if [ ! -d "$src" ]; then
    echo "ABORT: canonical source missing: $src"
    echo "       (plugin trees NOT touched — this folder may be the canonical copy)"
    exit 1
  fi
done

# 1. Clean generated trees (plugin-native files untouched)
rm -rf "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp"
mkdir -p "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp"

# 2. Copy skills (flattened — drop helix/ and mentors/ domain dirs)
cp -r "$KN_ROOT/skills/helix/leo-assist"         "$PLUGIN_DIR/skills/leo-assist"
cp -r "$KN_ROOT/skills/helix/leo-prompt"         "$PLUGIN_DIR/skills/leo-prompt"
cp -r "$KN_ROOT/skills/helix/leo-bridge"         "$PLUGIN_DIR/skills/leo-bridge"
cp -r "$KN_ROOT/skills/mentors/mentor-getleo-ai" "$PLUGIN_DIR/skills/mentor-getleo-ai"

# 3. Copy MCP server
cp -r "$KN_ROOT/mcp/leo-bridge" "$PLUGIN_DIR/mcp/leo-bridge"

# 4. Scrub excluded / sensitive files
find "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp" -type d \( -name '__pycache__' -o -name '.pytest_cache' \) -prune -exec rm -rf {} +
find "$PLUGIN_DIR/mcp" -type f -name '*.pyc' -delete
rm -rf "$PLUGIN_DIR/mcp/leo-bridge/tests"
rm -f  "$PLUGIN_DIR/mcp/leo-bridge/ledger/ledger.jsonl"
rm -f  "$PLUGIN_DIR/mcp/leo-bridge/docs/api-access-request-draft.md"
rmdir "$PLUGIN_DIR/mcp/leo-bridge/docs" 2>/dev/null || true

# 5. Keep an empty runtime ledger dir under version control
mkdir -p "$PLUGIN_DIR/mcp/leo-bridge/ledger"
touch    "$PLUGIN_DIR/mcp/leo-bridge/ledger/.gitkeep"

# 6. Summary + assert clean
echo "-- skills:"; ls "$PLUGIN_DIR/skills"
if find "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp" \( -name '__pycache__' -o -name '.pytest_cache' -o -name '*.pyc' -o -name 'ledger.jsonl' -o -name 'tests' -o -name 'api-access-request-draft.md' \) | grep -q .; then
  echo "DIRTY: excluded artifact leaked into build"; exit 1
fi
echo "== build clean, done =="
