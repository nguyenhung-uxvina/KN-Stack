# leo-ai Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đóng gói 4 skill LEO + MCP server leo-bridge thành một Claude Code plugin portable ở `plugins/leo-ai/`, copy đi đâu cũng chạy.

**Architecture:** Plugin-native files (`plugin.json`, `.mcp.json`, `README.md`, `build.sh`) viết tay và commit. `build.sh` copy `skills/` + `mcp/` từ nguồn canonical KN-Stack (flatten domain, scrub file nhạy cảm) → bản assembled cũng commit để dùng ngay. Một sửa code duy nhất ở `mcp/leo-bridge/server.py` (env override ledger); `.mcp.json` dùng `${CLAUDE_PLUGIN_ROOT}` cho portable.

**Tech Stack:** Bash (build.sh), JSON (manifests), Python 3.12 + FastMCP (server, sẵn có), pytest.

## Global Constraints

- Nguồn canonical KN-Stack là source of truth; plugin là bản copy tái tạo được — KHÔNG sửa logic 6 tool / router / denylist rules.
- `.mcp.json` của plugin PHẢI dùng `${CLAUDE_PLUGIN_ROOT}/mcp/leo-bridge/server.py` (không đường dẫn tương đối cwd).
- build.sh PHẢI loại khỏi bản phân phối: `__pycache__/`, `*.pyc`, `mcp/leo-bridge/tests/`, `mcp/leo-bridge/ledger/ledger.jsonl`, `mcp/leo-bridge/docs/api-access-request-draft.md`. Giữ `denylist.yaml`.
- Skill trong plugin FLATTEN: `skills/leo-assist`, `skills/leo-prompt`, `skills/leo-bridge`, `skills/mentor-getleo-ai` (không giữ `helix/`, `mentors/`).
- Commit format: `[LEO] ...`. Không có rsync trên máy → build.sh dùng `cp` + `find -delete`.
- plugin.json `version` = `1.0.0` (semver riêng, độc lập `VERSION` của KN-Stack).

---

### Task 1: Ledger env override trong canonical server.py

**Files:**
- Modify: `mcp/leo-bridge/server.py:6-17`
- Test: `mcp/leo-bridge/tests/test_server_ledger_env.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `server.LEDGER_DIR` (Path) = `LEO_BRIDGE_LEDGER_DIR` env nếu set, else `<server dir>/ledger`. build.sh (Task 3) copy nguyên `server.py` này ra plugin — không phân nhánh code.

- [ ] **Step 1: Write the failing test**

Create `mcp/leo-bridge/tests/test_server_ledger_env.py`:
```python
import importlib
from pathlib import Path


def test_ledger_dir_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("LEO_BRIDGE_LEDGER_DIR", str(tmp_path))
    import server
    importlib.reload(server)
    assert server.LEDGER_DIR == Path(str(tmp_path))


def test_ledger_dir_default(monkeypatch):
    monkeypatch.delenv("LEO_BRIDGE_LEDGER_DIR", raising=False)
    import server
    importlib.reload(server)
    assert server.LEDGER_DIR.name == "ledger"
```

- [ ] **Step 2: Run test to verify it fails**

Run (from `mcp/leo-bridge/`): `python -m pytest tests/test_server_ledger_env.py -v`
Expected: `test_ledger_dir_env_override` FAILs — `server.LEDGER_DIR` ignores the env var (still points at `<dir>/ledger`).

- [ ] **Step 3: Write minimal implementation**

Edit `mcp/leo-bridge/server.py`. Change the import line (line 6) and the LEDGER_DIR line (line 17):

Line 6 — add `os`:
```python
import os
import sys
```
Line 17 — read env with default:
```python
LEDGER_DIR = Path(os.environ.get("LEO_BRIDGE_LEDGER_DIR", str(Path(__file__).parent / "ledger")))
```

- [ ] **Step 4: Run test to verify it passes**

Run (from `mcp/leo-bridge/`): `python -m pytest tests/test_server_ledger_env.py -v`
Expected: both tests PASS. (If `mcp`/`fastmcp` import errors surface, run `pip install -r requirements.txt` first — the import is required to load `server`.)

- [ ] **Step 5: Commit**

```bash
git add mcp/leo-bridge/server.py mcp/leo-bridge/tests/test_server_ledger_env.py
git commit -m "[LEO] server.py: LEO_BRIDGE_LEDGER_DIR env override for ledger path"
```

---

### Task 2: Plugin-native scaffold (manifest, MCP config, README)

**Files:**
- Create: `plugins/leo-ai/.claude-plugin/plugin.json`
- Create: `plugins/leo-ai/.mcp.json`
- Create: `plugins/leo-ai/README.md`
- Create: `plugins/leo-ai/.gitignore`

**Interfaces:**
- Consumes: nothing.
- Produces: plugin root at `plugins/leo-ai/` with manifest + MCP config. Task 3's build.sh populates `skills/` + `mcp/` beside these files.

- [ ] **Step 1: Create the manifest**

Create `plugins/leo-ai/.claude-plugin/plugin.json`:
```json
{
  "name": "leo-ai",
  "version": "1.0.0",
  "description": "Workshop X x getleo.ai (Leo AI) toolkit - Phase x Mode prompt suite, text-to-CAD prompt builder, classification-gated MCP bridge (6 tools), and Leo advisor mentor. Cloud egress gated by MAT/HAN-CHE classification.",
  "author": { "name": "Workshop X" }
}
```

- [ ] **Step 2: Create the MCP config**

Create `plugins/leo-ai/.mcp.json`:
```json
{
  "mcpServers": {
    "leo-bridge": {
      "command": "python",
      "args": ["${CLAUDE_PLUGIN_ROOT}/mcp/leo-bridge/server.py"]
    }
  }
}
```

- [ ] **Step 3: Create the README**

Create `plugins/leo-ai/README.md`:
```markdown
# leo-ai — Claude Code plugin

Bộ công cụ LEO AI (getleo.ai) của Workshop X, đóng gói portable: 4 skill + MCP server `leo-bridge` (6 tool).

## Cài đặt

1. Copy thư mục `leo-ai/` này vào `~/.claude/plugins/`, **hoặc** chạy `/plugin install <đường-dẫn>/leo-ai`.
2. Cài Python deps cho MCP server (bắt buộc để 6 tool tự động chạy):
   ```bash
   pip install -r mcp/leo-bridge/requirements.txt
   ```
   Không cài Python deps thì 4 skill prompt vẫn dùng được — chỉ mất `leo-bridge` MCP (classify/prompt_build/send/ingest/route/ledger).

## Thành phần

| Skill | Vai trò |
|---|---|
| `leo-assist` | Prompt suite Phase×Mode — doctrine LEO (source of truth) |
| `leo-prompt` | Text-to-CAD prompt generator (concept-only) |
| `leo-bridge` | Orchestrate 6 MCP tool thành vòng khép kín |
| `mentor-getleo-ai` | Advisor "nhân bản tư duy" Leo (NLM-based) |

## Caveat

- **`mentor-getleo-ai` cần NotebookLM MCP + account có notebook Leo.** Máy khác không có NLM access → chỉ đọc được persona/references tĩnh, không query notebook.
- **Wikilink companion** (`[[helix-cad-bridge]]`, `[[LLM Spatial Blindness]]`, `[[leo-assist]]`…) trỏ tới skill có thể không cài kèm → hiển thị như text thường, không lỗi. Companion skills là tuỳ chọn.

## Biến môi trường

- `LEO_BRIDGE_LEDGER_DIR` — đổi nơi lưu ledger (mặc định: `mcp/leo-bridge/ledger/` trong plugin).

## Rebuild (chỉ khi ở trong repo KN-Stack)

```bash
bash build.sh
```
Tái tạo `skills/` + `mcp/` từ nguồn canonical KN-Stack và scrub file nhạy cảm.
```

- [ ] **Step 4: Create .gitignore for runtime ledger**

Create `plugins/leo-ai/.gitignore`:
```gitignore
# runtime ledger data — never commit exchange history
mcp/leo-bridge/ledger/*.jsonl
```

- [ ] **Step 5: Verify JSON validity + CLAUDE_PLUGIN_ROOT**

Run:
```bash
python -c "import json,sys; json.load(open('plugins/leo-ai/.claude-plugin/plugin.json')); d=json.load(open('plugins/leo-ai/.mcp.json')); assert '\${CLAUDE_PLUGIN_ROOT}' in d['mcpServers']['leo-bridge']['args'][0]; print('OK')"
```
Expected: `OK`.

- [ ] **Step 6: Commit**

```bash
git add plugins/leo-ai/.claude-plugin/plugin.json plugins/leo-ai/.mcp.json plugins/leo-ai/README.md plugins/leo-ai/.gitignore
git commit -m "[LEO] Plugin scaffold: plugin.json, .mcp.json (CLAUDE_PLUGIN_ROOT), README"
```

---

### Task 3: build.sh assembler + assembled artifact

**Files:**
- Create: `plugins/leo-ai/build.sh`
- Create (via build.sh, then commit): `plugins/leo-ai/skills/**`, `plugins/leo-ai/mcp/**`

**Interfaces:**
- Consumes: canonical `skills/helix/leo-*`, `skills/mentors/mentor-getleo-ai`, `mcp/leo-bridge` (with Task 1's server.py edit).
- Produces: assembled `plugins/leo-ai/skills/{leo-assist,leo-prompt,leo-bridge,mentor-getleo-ai}` and `plugins/leo-ai/mcp/leo-bridge/` scrubbed of excluded files.

- [ ] **Step 1: Write build.sh**

Create `plugins/leo-ai/build.sh`:
```bash
#!/usr/bin/env bash
# build.sh — assemble the portable leo-ai plugin from KN-Stack canonical sources.
# Idempotent: wipes skills/ + mcp/ then re-copies and scrubs sensitive files.
set -euo pipefail

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
KN_ROOT="$(cd "$PLUGIN_DIR/../.." && pwd)"

echo "== leo-ai plugin build =="
echo "Plugin: $PLUGIN_DIR"
echo "Source: $KN_ROOT"

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
find "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$PLUGIN_DIR/mcp" -type f -name '*.pyc' -delete
rm -rf "$PLUGIN_DIR/mcp/leo-bridge/tests"
rm -f  "$PLUGIN_DIR/mcp/leo-bridge/ledger/ledger.jsonl"
rm -f  "$PLUGIN_DIR/mcp/leo-bridge/docs/api-access-request-draft.md"

# 5. Keep an empty runtime ledger dir under version control
mkdir -p "$PLUGIN_DIR/mcp/leo-bridge/ledger"
touch    "$PLUGIN_DIR/mcp/leo-bridge/ledger/.gitkeep"

# 6. Summary + assert clean
echo "-- skills:"; ls "$PLUGIN_DIR/skills"
if find "$PLUGIN_DIR/skills" "$PLUGIN_DIR/mcp" \( -name '__pycache__' -o -name 'ledger.jsonl' -o -name 'tests' \) | grep -q .; then
  echo "DIRTY: excluded artifact leaked into build"; exit 1
fi
echo "== build clean, done =="
```

- [ ] **Step 2: Make executable and run**

Run:
```bash
chmod +x plugins/leo-ai/build.sh && bash plugins/leo-ai/build.sh
```
Expected: prints `-- skills:` listing `leo-assist  leo-bridge  leo-prompt  mentor-getleo-ai`, then `== build clean, done ==`.

- [ ] **Step 3: Assert structure + exclusions (T1, T5)**

Run:
```bash
test -f plugins/leo-ai/skills/leo-assist/SKILL.md \
 && test -f plugins/leo-ai/skills/mentor-getleo-ai/SKILL.md \
 && test -f plugins/leo-ai/mcp/leo-bridge/server.py \
 && test -f plugins/leo-ai/mcp/leo-bridge/leo_bridge/denylist.yaml \
 && test ! -e plugins/leo-ai/mcp/leo-bridge/tests \
 && test ! -e plugins/leo-ai/mcp/leo-bridge/ledger/ledger.jsonl \
 && test ! -e plugins/leo-ai/mcp/leo-bridge/docs/api-access-request-draft.md \
 && grep -q '^name: leo-assist' plugins/leo-ai/skills/leo-assist/SKILL.md \
 && echo "STRUCT OK"
```
Expected: `STRUCT OK`.

- [ ] **Step 4: Commit build.sh + assembled artifact**

```bash
git add plugins/leo-ai/build.sh plugins/leo-ai/skills plugins/leo-ai/mcp
git commit -m "[LEO] build.sh assembler + assembled leo-ai plugin (4 skills + MCP)"
```

---

### Task 4: End-to-end verification

**Files:**
- Modify: `CHANGELOG.md` (top entry)

**Interfaces:**
- Consumes: assembled `plugins/leo-ai/` from Task 3, Task 1's env override.
- Produces: nothing new — verification + changelog only.

- [ ] **Step 1: Python server import smoke (T2)**

Run (deps must be installed):
```bash
cd plugins/leo-ai/mcp/leo-bridge && python -c "import sys; sys.path.insert(0,'.'); import server; print('IMPORT OK', server.LEDGER_DIR.name)" && cd -
```
Expected: `IMPORT OK ledger`. (If ModuleNotFoundError for `mcp`/`pyyaml`, run `pip install -r requirements.txt` in that dir first, then re-run.)

- [ ] **Step 2: Ledger env override end-to-end (T3)**

Run:
```bash
TMPLEDGER="$(mktemp -d)"; cd plugins/leo-ai/mcp/leo-bridge \
 && LEO_BRIDGE_LEDGER_DIR="$TMPLEDGER" python -c "import sys; sys.path.insert(0,'.'); import server; assert str(server.LEDGER_DIR)=='$TMPLEDGER', server.LEDGER_DIR; print('LEDGER ENV OK ->', server.LEDGER_DIR)"; cd -
```
Expected: `LEDGER ENV OK -> <tmp dir>` (points outside the plugin, not `mcp/leo-bridge/ledger`).

- [ ] **Step 3: Portable copy smoke (T6)**

Run:
```bash
DEST="$(mktemp -d)/leo-ai"; cp -r plugins/leo-ai "$DEST" \
 && test -f "$DEST/.claude-plugin/plugin.json" \
 && test -f "$DEST/mcp/leo-bridge/server.py" \
 && cd "$DEST/mcp/leo-bridge" && python -c "import sys; sys.path.insert(0,'.'); import server; print('PORTABLE OK', server.LEDGER_DIR.name)"; cd -
```
Expected: `PORTABLE OK ledger` — plugin runs from a location outside the KN-Stack repo (`__file__`-relative paths resolve).

- [ ] **Step 4: Add CHANGELOG entry**

Add to the top of `CHANGELOG.md` (below the header), matching the file's existing entry style:
```markdown
## [Unreleased]
### Added
- `plugins/leo-ai/` — portable Claude Code plugin bundling the LEO AI toolkit (leo-assist, leo-prompt, leo-bridge skills + mentor-getleo-ai + leo-bridge MCP server). Copy-anywhere; `build.sh` regenerates from canonical sources. `server.py` gains `LEO_BRIDGE_LEDGER_DIR` env override.
```
(If a `## [Unreleased]` section already exists, add the bullet under its `### Added` instead of duplicating the heading.)

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md
git commit -m "[LEO] CHANGELOG: leo-ai portable plugin"
```

---

## Self-Review notes

- **Spec coverage:** §3 structure → Tasks 2+3; §4.2 .mcp.json → Task 2 Step 2/5; §4.4 ledger override → Task 1; §4.5 build.sh → Task 3; §4.6 README → Task 2 Step 3; §5 security scrub → Task 3 Step 1/3; §6 T1-T6 → T1/T5 (Task 3 Step 3), T2/T6 (Task 4 Step 1/3), T3 (Task 4 Step 2), T4 (Task 2 Step 5), frontmatter (Task 3 Step 3 grep). All covered.
- **Type consistency:** `server.LEDGER_DIR` name/type used identically across Task 1 test, Task 4 Step 1/2/3. `LEO_BRIDGE_LEDGER_DIR` env key spelled identically in server.py edit, README, tests, CHANGELOG.
- **No placeholders:** all file contents and commands are literal.
