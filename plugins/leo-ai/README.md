# leo-ai — Claude Code plugin

Bộ công cụ LEO AI (getleo.ai) của Workshop X, đóng gói portable: 4 skill + MCP server `leo-bridge` (6 tool).

## Cài đặt

> ⚠️ **Đừng** copy thẳng vào `~/.claude/plugins/` — đó là cache do marketplace quản lý, không phải chỗ thả folder. Dùng 1 trong 3 cách dưới.

Trước tiên, luôn cài Python deps cho MCP server (bắt buộc để 6 tool tự động chạy):
```bash
pip install -r mcp/leo-bridge/requirements.txt
python mcp/leo-bridge/server.py --selftest   # kiểm tra: phải in "selftest OK — 8 templates ... 6 tools"
```
Bỏ bước này thì 4 skill prompt vẫn dùng được — chỉ mất `leo-bridge` MCP (classify/prompt_build/send/ingest/route/ledger). Nếu `python` không có trong PATH (Windows hay chỉ có `py`), sửa `command` trong `.mcp.json` thành `py`.

**Cách A — skills-directory plugin (khuyến nghị, zero-config, tự nạp mọi session):**
```bash
cp -r <folder này> ~/.claude/skills/leo-ai
# hoặc junction (Windows): cmd //c mklink /J "%USERPROFILE%\.claude\skills\leo-ai" "D:\...\leo-ai"
```
Khởi động lại Claude Code → `/plugin` sẽ thấy `leo-ai@skills-dir`. Chỉ hiệu lực từ session sau.

**Cách B — marketplace (hiện trong `/plugin list`, có `/plugin update`):**
```
/plugin marketplace add <đường-dẫn tới folder này>
/plugin install leo-ai@workshop-x-leo
```
(Folder này đã có `.claude-plugin/marketplace.json` nên `marketplace add` trỏ thẳng vào chính nó.)

**Cách C — session tạm thời (không cài gì):**
```bash
claude --plugin-dir "<đường-dẫn tới folder này>"
```

Sau khi cài, nếu MCP `leo-bridge` chưa chạy: `/reload-plugins` hoặc khởi động lại Claude Code.

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
