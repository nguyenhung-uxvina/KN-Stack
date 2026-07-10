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
