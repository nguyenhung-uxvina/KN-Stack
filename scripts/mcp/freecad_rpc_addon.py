#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
freecad_rpc_addon.py — Máy chủ RPC chạy TRONG FreeCAD (phần "FreeCAD side" của MCP).

Mở một XML-RPC server trên 127.0.0.1:9875 phơi bày các lệnh để Claude (qua MCP bridge
freecad_mcp_server.py) mở file CAD, liệt kê chi tiết, trích xuất qtcn-seed và chạy code
Python trong phiên FreeCAD đang mở — SOI TRỰC TIẾP, tương tác.

Tái dùng logic đã kiểm chứng ở scripts/extract/freecad_extract.py (build_seed).

CHẠY:
  • GUI (khuyến nghị — có ảnh chụp khung nhìn): mở FreeCAD → menu Macro → chạy file này.
    Server chạy nền, FreeCAD vẫn thao tác được.
  • Headless (test/batch, không ảnh chụp):
        freecadcmd freecad_rpc_addon.py         # chạy blocking, Ctrl-C để dừng
        "C:\\Program Files\\FreeCAD 1.1\\bin\\freecadcmd.exe" freecad_rpc_addon.py

Cổng đổi qua env FREECAD_RPC_PORT (mặc định 9875).
"""
import io, os, sys, traceback
from contextlib import redirect_stdout

import FreeCAD  # chạy trong FreeCAD nên luôn có
try:
    import FreeCADGui  # noqa
except Exception:
    FreeCADGui = None

# tái dùng build_seed từ engine trích xuất đã test
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(_HERE, "..", "extract")))
import freecad_extract as fx  # noqa

_STATE = {"last_file": None}


def _open_file(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".fcstd":
        doc = FreeCAD.open(path)
    else:
        import Import
        Import.open(path)
        doc = FreeCAD.ActiveDocument
    _STATE["last_file"] = path
    return doc


class FreeCADRPC:
    """Các lệnh phơi qua XML-RPC. Trả về kiểu chuẩn (dict/list/str/num/bool/None)."""

    def ping(self):
        return {"ok": True, "freecad": ".".join(str(x) for x in FreeCAD.Version()[:3]),
                "gui": bool(FreeCAD.GuiUp), "active_doc": getattr(FreeCAD.ActiveDocument, "Name", None)}

    def open(self, path):
        try:
            doc = _open_file(path)
            return {"ok": True, "doc": doc.Name, "objects": len(doc.Objects), "file": path}
        except Exception as e:
            return {"ok": False, "error": "%s" % e}

    def list_docs(self):
        return {"docs": list(FreeCAD.listDocuments().keys()),
                "active": getattr(FreeCAD.ActiveDocument, "Name", None)}

    def list_parts(self, default_density=None):
        doc = FreeCAD.ActiveDocument
        if doc is None:
            return {"ok": False, "error": "Chưa mở tài liệu nào (gọi open trước)."}
        dens = float(default_density) if default_density else fx.DEFAULT_DENSITY
        seed, raw, meta = fx.build_seed(doc, None, _STATE.get("last_file"), dens)
        # rút gọn cho hiển thị nhanh + kèm seed đầy đủ
        summary = [{"vt": p["vt"], "name": p["name"], "qty": p["qty"],
                    "mass_kg": p["specs"]["est_mass_kg"], "total_mass_kg": p["specs"]["total_mass_kg"],
                    "bbox_mm": p["specs"]["bbox_mm"]} for p in seed["bom"]]
        return {"ok": True, "total_mass_kg": seed["product"]["total_mass_kg"],
                "envelope_mm": seed["product"]["principal_particulars"].get("envelope_mm"),
                "parts": summary, "groups": meta["groups"], "solid_parts": len(raw), "seed": seed}

    def extract_seed(self, out_dir, name="qtcn-seed", default_density=None):
        doc = FreeCAD.ActiveDocument
        if doc is None:
            return {"ok": False, "error": "Chưa mở tài liệu nào."}
        dens = float(default_density) if default_density else fx.DEFAULT_DENSITY
        seed, raw, meta = fx.build_seed(doc, None if name == "qtcn-seed" else name, _STATE.get("last_file"), dens)
        os.makedirs(out_dir, exist_ok=True)
        import json
        path = os.path.join(out_dir, name + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(seed, f, ensure_ascii=False, indent=2)
        return {"ok": True, "path": path, "total_mass_kg": seed["product"]["total_mass_kg"],
                "parts": len(seed["bom"])}

    def run(self, code):
        """Chạy code Python trong phiên FreeCAD (FreeCAD, App, doc sẵn dùng). Trả stdout + biến 'result'."""
        ns = {"FreeCAD": FreeCAD, "App": FreeCAD, "doc": FreeCAD.ActiveDocument, "fx": fx}
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                exec(code, ns)
            res = ns.get("result", None)
            return {"ok": True, "stdout": buf.getvalue(), "result": res if _serializable(res) else repr(res)}
        except Exception:
            return {"ok": False, "stdout": buf.getvalue(), "error": traceback.format_exc()}

    def close(self, name=None):
        doc = FreeCAD.getDocument(name) if name else FreeCAD.ActiveDocument
        if doc is not None:
            FreeCAD.closeDocument(doc.Name)
            return {"ok": True}
        return {"ok": False, "error": "Không có tài liệu để đóng."}

    def screenshot(self, path, width=1024, height=768):
        if not FreeCAD.GuiUp or FreeCADGui is None:
            return {"ok": False, "error": "Cần FreeCAD GUI (ảnh chụp không dùng được ở chế độ headless)."}
        try:
            FreeCADGui.ActiveDocument.ActiveView.fitAll()
            FreeCADGui.ActiveDocument.ActiveView.saveImage(path, int(width), int(height), "White")
            return {"ok": True, "path": path}
        except Exception as e:
            return {"ok": False, "error": "%s" % e}


def _serializable(v):
    return isinstance(v, (str, int, float, bool, type(None), list, dict))


def serve(host="127.0.0.1", port=None, block=True):
    from xmlrpc.server import SimpleXMLRPCServer
    port = int(port or os.environ.get("FREECAD_RPC_PORT", 9875))
    server = SimpleXMLRPCServer((host, port), allow_none=True, logRequests=False)
    server.register_instance(FreeCADRPC())
    FreeCAD.Console.PrintMessage("[freecad-rpc] listening on %s:%d\n" % (host, port))
    print("[freecad-rpc] listening on %s:%d" % (host, port))
    if block:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
    else:
        import threading
        threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# Entry: GUI macro (__name__=='__main__') hoặc headless freecadcmd (sys.argv có tên file).
_entry = (__name__ == "__main__") or any(
    isinstance(t, str) and t.replace("\\", "/").lower().endswith("freecad_rpc_addon.py") for t in sys.argv)
if _entry:
    try:
        serve(block=not FreeCAD.GuiUp)   # GUI: nền (thread); headless: blocking
    except OSError as e:
        FreeCAD.Console.PrintWarning("[freecad-rpc] không khởi động được (cổng bận?): %s\n" % e)
