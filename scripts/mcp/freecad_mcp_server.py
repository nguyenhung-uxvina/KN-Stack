#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freecad_mcp_server.py — MCP bridge (Claude  ↔  FreeCAD RPC addon).

Phơi các MCP tool cho Claude, mỗi tool proxy sang XML-RPC của freecad_rpc_addon.py
(đang chạy TRONG FreeCAD trên 127.0.0.1:9875). Đây là phần Claude khởi động; addon là
phần chạy trong FreeCAD. Hai tiến trình tách rời.

Phụ thuộc:  pip install mcp        (MCP Python SDK / FastMCP)
Chạy (Claude Code tự khởi động qua .mcp.json):
    python scripts/mcp/freecad_mcp_server.py
Cổng RPC đổi qua env FREECAD_RPC_URL (mặc định http://127.0.0.1:9875).

LUỒNG DÙNG: (1) mở FreeCAD, chạy macro freecad_rpc_addon.py → RPC lên.
            (2) Claude gọi freecad_open → freecad_list_parts → freecad_extract_seed
                → seed cắm vào qtcn --seed / product-dossier.
"""
import os
import xmlrpc.client

try:
    from mcp.server.fastmcp import FastMCP
except Exception as e:  # pragma: no cover
    raise SystemExit(
        "[!] Thiếu MCP SDK. Cài: pip install mcp\n    (chi tiết: %s)" % e)

RPC_URL = os.environ.get("FREECAD_RPC_URL", "http://127.0.0.1:9875")
mcp = FastMCP("freecad")


def _rpc():
    return xmlrpc.client.ServerProxy(RPC_URL, allow_none=True)


def _call(method, *args):
    try:
        return getattr(_rpc(), method)(*args)
    except ConnectionRefusedError:
        return {"ok": False, "error": "Không kết nối được FreeCAD RPC tại %s. "
                "Hãy mở FreeCAD và chạy macro scripts/mcp/freecad_rpc_addon.py." % RPC_URL}
    except Exception as e:
        return {"ok": False, "error": "%s: %s" % (type(e).__name__, e)}


@mcp.tool()
def freecad_ping() -> dict:
    """Kiểm tra FreeCAD RPC còn sống; trả phiên bản FreeCAD, có GUI không, tài liệu đang mở."""
    return _call("ping")


@mcp.tool()
def freecad_open(path: str) -> dict:
    """Mở một file CAD (STEP/IGES/FCStd; DWG cần ODA) trong FreeCAD. Trả số object."""
    return _call("open", path)


@mcp.tool()
def freecad_list_parts(default_density: float = 0.0) -> dict:
    """Liệt kê chi tiết của tài liệu đang mở: BOM (VT, tên, SL), khối lượng thật, bbox,
    envelope, và seed đầy đủ (qtcn-seed/v1). default_density>0 để ép ρ khi thiếu vật liệu."""
    return _call("list_parts", default_density or None)


@mcp.tool()
def freecad_extract_seed(out_dir: str, name: str = "qtcn-seed", default_density: float = 0.0) -> dict:
    """Ghi qtcn-seed.json (nền tảng QTCN, khối lượng thật) từ tài liệu đang mở vào out_dir."""
    return _call("extract_seed", out_dir, name, default_density or None)


@mcp.tool()
def freecad_run(code: str) -> dict:
    """Chạy code Python trong phiên FreeCAD (biến sẵn: FreeCAD/App, doc, fx). Trả stdout +
    biến 'result'. Dùng để soi/đo tùy biến (vd tính diện tích một mặt, đọc thuộc tính)."""
    return _call("run", code)


@mcp.tool()
def freecad_screenshot(path: str, width: int = 1024, height: int = 768) -> dict:
    """Lưu ảnh khung nhìn hiện tại ra PATH (chỉ khi FreeCAD chạy ở chế độ GUI)."""
    return _call("screenshot", path, width, height)


@mcp.tool()
def freecad_close() -> dict:
    """Đóng tài liệu FreeCAD đang mở."""
    return _call("close")


if __name__ == "__main__":
    mcp.run()
