# FreeCAD MCP — Claude soi & trích xuất CAD tương tác

Cho phép Claude **mở file CAD trong FreeCAD, soi trực tiếp và trích xuất `qtcn-seed.json`**
(nền tảng cho `qtcn` / `product-dossier`). Bổ sung cho engine headless
[`freecad_extract.py`](../extract/freecad_extract.py): headless = batch tất định; MCP = tương tác.

## Kiến trúc (2 tiến trình)

```
Claude Code ──stdio──> freecad_mcp_server.py ──XML-RPC:9875──> freecad_rpc_addon.py (TRONG FreeCAD)
   (MCP tool)            (bridge, cần: pip install mcp)          (phơi ping/open/list_parts/extract_seed/run/screenshot)
```

- **freecad_rpc_addon.py** chạy TRONG FreeCAD (GUI macro hoặc headless), mở XML-RPC server.
  Tái dùng `build_seed()` đã kiểm chứng (khối lượng thật, dedup container, gộp instance).
- **freecad_mcp_server.py** do Claude Code khởi động (qua `.mcp.json`), proxy sang RPC.

## Cài đặt (một lần)

1. **MCP SDK cho bridge:** `pip install mcp`
2. **`.mcp.json`** đã có sẵn ở gốc repo → Claude Code tự nạp server `freecad` khi mở project.
   Kiểm tra: `/mcp` trong Claude Code, hoặc `claude mcp list`.

## Dùng

1. **Bật RPC trong FreeCAD:**
   - *GUI (khuyến nghị, có ảnh chụp):* mở FreeCAD → **Macro → Macros… → chạy** `scripts/mcp/freecad_rpc_addon.py`.
     Server chạy nền; FreeCAD vẫn thao tác được. Thấy log `[freecad-rpc] listening on 127.0.0.1:9875`.
   - *Headless (không ảnh chụp):*
     ```
     "C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe" scripts/mcp/freecad_rpc_addon.py
     ```
2. **Trong Claude Code** dùng các tool:
   - `freecad_ping` — kiểm tra kết nối.
   - `freecad_open` `<path.step>` — mở file.
   - `freecad_list_parts` — BOM + khối lượng thật + envelope + seed đầy đủ.
   - `freecad_extract_seed` `<out_dir>` — ghi `qtcn-seed.json` → cắm vào `qtcn --seed` / `product-dossier`.
   - `freecad_run` `<python>` — soi tùy biến trong phiên FreeCAD (đo mặt, đọc thuộc tính…).
   - `freecad_screenshot` `<path.png>` — ảnh khung nhìn (chỉ GUI).
   - `freecad_close` — đóng tài liệu.

## Ghi chú
- Cổng đổi qua env `FREECAD_RPC_PORT` (addon) và `FREECAD_RPC_URL` (bridge, trong `.mcp.json`).
- DWG cần **ODA File Converter** khai trong FreeCAD *Preferences → Import-Export → DWG*.
- `freecad_run` thực thi code trong FreeCAD — chỉ dùng nội bộ, tin cậy (không phơi ra ngoài).
- Bảo mật: RPC chỉ bind `127.0.0.1` (localhost).

## Đã kiểm
- **Addon RPC (headless, freecadcmd):** ping/open/list_parts/extract_seed chạy end-to-end trên
  fixture STEP → total_mass 115,492 kg (khớp CLI). Xem changelog dưới.
- **MCP bridge:** cần `pip install mcp` để chạy; handshake do Claude Code thực hiện lúc runtime.
