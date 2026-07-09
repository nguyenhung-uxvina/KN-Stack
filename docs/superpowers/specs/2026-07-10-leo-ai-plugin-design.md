# Design — `leo-ai` Plugin (đóng gói bộ skill LEO AI, cài bất kỳ đâu)

> Status: approved-pending-review · Date: 2026-07-10 · Branch: `feature/leo-ai-plugin`
> Goal: Đóng gói toàn bộ công cụ LEO AI (getleo.ai) của Workshop X thành **một Claude Code plugin portable** — copy nguyên thư mục là chạy trên bất kỳ máy nào có Claude Code + Python.

## 1. Mục tiêu & phạm vi

Gom **4 skill + 1 MCP server** hiện đang nằm rải trong KN-Stack thành một plugin tự chứa:

| Asset nguồn (canonical) | Loại | Vai trò |
|---|---|---|
| `skills/helix/leo-assist/` (+ `references/`) | skill | Prompt suite Phase×Mode — **source of truth** doctrine LEO |
| `skills/helix/leo-prompt/` | skill | Text-to-CAD prompt generator (concept-only) |
| `skills/helix/leo-bridge/` | skill | Orchestrate 6 MCP tool thành vòng khép kín |
| `skills/mentors/mentor-getleo-ai/` (+ `notebooks/`, `references/`) | mentor skill | Advisor "nhân bản tư duy" Leo (NLM-based) |
| `mcp/leo-bridge/` | MCP server (Python) | 6 tool: classify → prompt_build → send → ingest → route → ledger |

**Ngoài phạm vi (YAGNI):** không tạo marketplace repo riêng, không auto-install Python deps, không sửa logic 6 tool, không đụng các skill companion (`helix-cad-bridge`, v.v.).

## 2. Quyết định đã chốt (từ brainstorming)

| # | Quyết định | Lựa chọn |
|---|---|---|
| D1 | Phạm vi đóng gói | **Cả 4 skill + MCP server** |
| D2 | Cơ chế phân phối | **Thư mục plugin portable** (copy tay / `/plugin install <path>`) |
| D3 | Vị trí + build | **`plugins/leo-ai/` commit sẵn bản assembled + `build.sh` tái tạo** từ nguồn canonical |
| D4 | Ledger runtime | **Trong plugin (mặc định) + env override `LEO_BRIDGE_LEDGER_DIR`** (sửa ~1 dòng `server.py`) |

## 3. Cấu trúc plugin

```
plugins/leo-ai/                       ← copy nguyên thư mục này đi đâu cũng chạy
├── .claude-plugin/
│   └── plugin.json                   ← manifest
├── .mcp.json                         ← leo-bridge qua ${CLAUDE_PLUGIN_ROOT}
├── skills/                           ← FLATTENED (không giữ helix/ mentors/)
│   ├── leo-assist/       (+ references/)
│   ├── leo-prompt/
│   ├── leo-bridge/
│   └── mentor-getleo-ai/ (+ notebooks/ references/)
├── mcp/
│   └── leo-bridge/
│       ├── server.py
│       ├── leo_bridge/   (builder, gate, ledger, parsers, router, templates, transports, denylist.yaml)
│       ├── requirements.txt
│       └── ledger/       (thư mục rỗng có .gitkeep — runtime data sinh tại đây)
├── build.sh                          ← tái tạo skills/ + mcp/ từ KN-Stack canonical
└── README.md                         ← cài đặt + pip deps + caveat
```

**Files plugin-native (viết tay, commit, KHÔNG do build.sh sinh):** `plugin.json`, `.mcp.json`, `build.sh`, `README.md`.
**Files do build.sh sinh (copy từ nguồn):** toàn bộ `skills/` + `mcp/`.

## 4. Chi tiết từng thành phần

### 4.1 `.claude-plugin/plugin.json`
```json
{
  "name": "leo-ai",
  "version": "1.0.0",
  "description": "Workshop X ↔ getleo.ai (Leo AI) toolkit — Phase×Mode prompt suite, text-to-CAD prompt builder, classification-gated MCP bridge (6 tools), and Leo advisor mentor. Cloud egress gated by MẬT/HẠN-CHẾ classification.",
  "author": { "name": "Workshop X" }
}
```
- `version` bám semver riêng của plugin (độc lập với `VERSION` của KN-Stack).

### 4.2 `.mcp.json` (điểm portable then chốt)
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
- Khác bản gốc KN-Stack (`"mcp/leo-bridge/server.py"` — tương đối cwd, **không** portable).
- `${CLAUDE_PLUGIN_ROOT}` được Claude Code thay bằng đường dẫn thật của plugin lúc load → chạy đúng bất kể cwd / vị trí cài.

### 4.3 Portability của Python code (đã sẵn, xác minh)
- `server.py`: `sys.path.insert(0, str(Path(__file__).parent))` + `LEDGER_DIR = Path(__file__).parent / "ledger"` — `__file__`-relative.
- `gate.py`: `DENYLIST_PATH = Path(__file__).parent / "denylist.yaml"` — `__file__`-relative.
- `ledger.py`: nhận `dir_path`, không hardcode cwd.
→ **Không cần sửa** ngoài thay đổi D4 dưới đây.

### 4.4 D4 — Ledger env override (sửa `server.py`)
Đổi 1 dòng:
```python
# cũ
LEDGER_DIR = Path(__file__).parent / "ledger"
# mới
LEDGER_DIR = Path(os.environ.get("LEO_BRIDGE_LEDGER_DIR", Path(__file__).parent / "ledger"))
```
- Thêm `import os` nếu chưa có.
- Mặc định: ghi trong plugin (self-contained). Đặt `LEO_BRIDGE_LEDGER_DIR` → tách data ra ngoài.
- **Lưu ý drift:** sửa này áp cho **cả bản canonical** `mcp/leo-bridge/server.py` (để build.sh copy ra bản đã sửa, không phân nhánh code). build.sh copy nguyên `server.py` từ nguồn.

### 4.5 `build.sh` — tái tạo assembled từ canonical
Hành vi:
1. Xác định `KN_ROOT` (2 cấp trên plugin) và `PLUGIN_DIR`.
2. Xoá sạch `skills/` + `mcp/` trong plugin (tránh file mồ côi).
3. Copy:
   - `$KN_ROOT/skills/helix/leo-assist` → `skills/leo-assist`
   - `$KN_ROOT/skills/helix/leo-prompt` → `skills/leo-prompt`
   - `$KN_ROOT/skills/helix/leo-bridge` → `skills/leo-bridge`
   - `$KN_ROOT/skills/mentors/mentor-getleo-ai` → `skills/mentor-getleo-ai`
   - `$KN_ROOT/mcp/leo-bridge` → `mcp/leo-bridge`
4. **Loại trừ** khi copy: `__pycache__/`, `*.pyc`, `tests/`, `ledger/ledger.jsonl`, `docs/api-access-request-draft.md`.
5. Tạo `mcp/leo-bridge/ledger/.gitkeep`.
6. In summary (số skill copy, kích thước).
- Idempotent: chạy lại luôn cho cùng kết quả.
- Dùng `rsync --exclude` nếu có, fallback `cp` + `find -delete`.

### 4.6 `README.md`
Nội dung tối thiểu:
- **Cài đặt:** copy `leo-ai/` vào `~/.claude/plugins/` **hoặc** `/plugin install <path>`.
- **Prereq Python:** `pip install -r mcp/leo-bridge/requirements.txt` (bắt buộc để MCP `leo-bridge` chạy — nếu không, 4 skill prompt vẫn dùng được, chỉ mất 6 tool tự động).
- **Caveat mentor:** `mentor-getleo-ai` cần **NotebookLM MCP + account có notebook Leo**; máy khác không có → chỉ đọc persona/references tĩnh, không query được.
- **Caveat wikilink:** `[[helix-cad-bridge]]`, `[[LLM Spatial Blindness]]`, `[[leo-assist]]`… trỏ tới skill có thể không cài kèm → hiển thị như text, không lỗi. Companion skills là tuỳ chọn.
- **Env tuỳ chọn:** `LEO_BRIDGE_LEDGER_DIR` để đổi nơi lưu ledger.
- **Rebuild:** chạy `bash build.sh` (chỉ dùng khi ở trong KN-Stack repo, để đồng bộ từ nguồn).

## 5. Bảo mật / dữ liệu nhạy cảm

build.sh **bắt buộc loại** khỏi bản phân phối:
- `mcp/leo-bridge/ledger/ledger.jsonl` — chứa lịch sử trao đổi Leo thật (có thể chạm dữ liệu SP Xưởng).
- `docs/api-access-request-draft.md` — draft nội bộ.
- `__pycache__/`, `tests/` — rác build.

**Giữ lại:** `denylist.yaml` (cần cho gate MẬT — đây là quy tắc chặn, không phải dữ liệu mật).

## 6. Kiểm thử / nghiệm thu

| # | Kiểm tra | Pass khi |
|---|---|---|
| T1 | build.sh chạy sạch | `plugins/leo-ai/skills/` có 4 skill, `mcp/leo-bridge/server.py` tồn tại, KHÔNG có `__pycache__`/`ledger.jsonl`/`tests` |
| T2 | Python server import OK | `python mcp/leo-bridge/server.py` khởi động không lỗi import (deps đã cài) |
| T3 | Ledger env override | Set `LEO_BRIDGE_LEDGER_DIR=/tmp/x`, gọi tool ghi ledger → file sinh tại `/tmp/x`, KHÔNG trong plugin |
| T4 | plugin.json + .mcp.json hợp lệ | JSON parse được; `.mcp.json` dùng `${CLAUDE_PLUGIN_ROOT}` |
| T5 | Frontmatter skill nguyên vẹn | 4 SKILL.md giữ `name:` + `description:` sau copy |
| T6 | Portable smoke | Copy `plugins/leo-ai/` ra thư mục ngoài repo → cấu trúc + đường dẫn `__file__`-relative vẫn giải đúng |

## 7. Việc KHÔNG làm (chốt scope)
- Không đăng plugin lên marketplace công khai.
- Không đóng gói Python runtime/venv (phụ thuộc `python` sẵn trên máy đích).
- Không sửa logic 6 tool, router, denylist rules.
- Không xoá/di chuyển các skill LEO gốc trong KN-Stack (plugin là bản copy song song; KN-Stack vẫn là source of truth qua junction cho máy CEO).
