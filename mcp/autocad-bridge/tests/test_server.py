"""Test server qua đúng đường MCP (tool manager), với AutoCAD giả. Không cần AutoCAD thật."""
import asyncio
import json
import sys
from pathlib import Path

import pytest
from mcp.server.fastmcp.exceptions import ToolError

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.com_worker import ComWorker  # noqa: E402
from core.ledger import Ledger  # noqa: E402
from core.policy import PathPolicy  # noqa: E402
from fake_acad import FakeApp  # noqa: E402
from server import build_server  # noqa: E402


@pytest.fixture
def env(tmp_path):
    root = tmp_path / "Workspace"
    (root / "drawings").mkdir(parents=True)
    (root / "output").mkdir()
    app = FakeApp()
    pol = PathPolicy([root], [root / "output"], [tmp_path / "AutoCAD 2025"])
    ledger = Ledger(tmp_path / "ledger.jsonl")

    def make(profile="draft"):
        return build_server(app_getter=lambda: app, policy=pol, worker=ComWorker(timeout=5), ledger=ledger,
                            profile=profile, read_budget=2.0)
    return app, root, make, ledger


def call(srv, tool_name, /, **args):
    return asyncio.run(srv._tool_manager.call_tool(tool_name, args, convert_result=False))


def fail(srv, tool_name, /, **args) -> dict:
    with pytest.raises(ToolError) as ei:
        call(srv, tool_name, **args)
    msg = str(ei.value)
    return json.loads(msg[msg.index("{"):])


# --- 1. lỗi vẽ trùng khi AutoCAD bận giữa chừng ---------------------------------
def test_busy_after_create_does_not_draw_twice_and_reports_partial(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    doc.fail_once("SetLayer")
    err = fail(make(), "acad_add_line", x1=0, y1=0, x2=10, y2=0, layer="L1", expected_document="a.dwg")
    assert err["code"] == "ACAD_BUSY"
    assert doc.ModelSpace.Count == 1
    assert err["data"]["partial"] == [doc.ModelSpace.Item(0).Handle]


def test_read_tool_retries_when_busy(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "drawings" / "a.dwg"))
    doc.ModelSpace.AddLine((0, 0, 0), (1, 0, 0))
    doc.fail_once("Count", times=2)
    res = call(make(), "acad_entities", limit=10)
    assert res["ok"] and res["data"]["total"] == 1


# --- 3. gắn đúng bản vẽ -------------------------------------------------------------
def test_write_refused_when_active_document_is_not_the_expected_one(env):
    app, root, make, _ = env
    a = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    app.add_doc("b.dwg", str(root / "output" / "b.dwg"))           # người dùng bấm sang tab b
    err = fail(make(), "acad_add_line", x1=0, y1=0, x2=1, y2=1, expected_document="a.dwg")
    assert err["code"] == "DOCUMENT_CHANGED"
    assert a.ModelSpace.Count == 0


def test_every_result_carries_target_receipt(env):
    app, root, make, _ = env
    app.add_doc("a.dwg", str(root / "drawings" / "a.dwg"))
    res = call(make(), "acad_layers")
    assert res["_target"]["name"] == "a.dwg" and len(res["_target"]["doc_id"]) == 12


# --- 6. chính sách đường dẫn trên tool ---------------------------------------------
def test_write_refused_on_read_only_document(env):
    app, root, make, _ = env
    app.add_doc("a.dwg", str(root / "output" / "a.dwg"), read_only=True)
    assert fail(make(), "acad_add_circle", cx=0, cy=0, radius=5, expected_document="a.dwg")["code"] == "READ_ONLY_TARGET"


def test_write_refused_on_document_outside_write_root(env):
    app, root, make, _ = env
    app.add_doc("src.dwg", str(root / "drawings" / "src.dwg"))      # bản vẽ nguồn: chỉ đọc theo chính sách
    assert fail(make(), "acad_add_circle", cx=0, cy=0, radius=5, expected_document="src.dwg")["code"] == "PATH_DENIED"


def test_write_allowed_on_new_unsaved_drawing(env):
    app, _, make, _ = env
    doc = app.add_doc("Drawing1.dwg", "")
    res = call(make(), "acad_add_circle", cx=0, cy=0, radius=5, expected_document="Drawing1.dwg")
    assert res["ok"] and doc.ModelSpace.Count == 1


def test_read_refused_on_active_document_outside_read_root(env):
    app, root, make, _ = env
    app.add_doc("x.dwg", str(root.parent / "elsewhere" / "x.dwg"))
    assert fail(make(), "acad_layers")["code"] == "PATH_DENIED"


def test_open_and_offline_tools_respect_policy(env):
    app, root, make, _ = env
    srv = make()
    outside = root.parent / "elsewhere"
    assert fail(srv, "acad_open", path=str(outside / "a.dxf"))["code"] == "PATH_DENIED"
    assert fail(srv, "acad_dxf_summary", path=str(outside / "a.dxf"))["code"] == "PATH_DENIED"
    assert fail(srv, "acad_scan_folder", folder=str(root / "drawings"),
                csv_out=str(root / "drawings" / "bom.csv"))["code"] == "PATH_DENIED"


# --- 4. phong bì + cắt danh sách ----------------------------------------------------
def test_list_results_report_truncation(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "drawings" / "a.dwg"))
    for i in range(3):
        doc.ModelSpace.AddLine((0, i, 0), (1, i, 0))
    res = call(make(), "acad_entities", limit=1)
    assert res["ok"] and res["data"]["truncated"] is True and res["data"]["total"] == 3
    assert len(res["data"]["entities"]) == 1


# --- 8. undo mark + token xác nhận --------------------------------------------------
def test_write_is_wrapped_in_one_undo_mark(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    call(make(), "acad_add_line", x1=0, y1=0, x2=1, y2=1, layer="L1", expected_document="a.dwg")
    ops = [c for c in doc.calls if c in ("StartUndoMark", "AddLine", "SetLayer", "EndUndoMark")]
    assert ops == ["StartUndoMark", "AddLine", "SetLayer", "EndUndoMark"]


def test_overwrite_save_needs_token_bound_to_revision(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    srv = make()
    first = call(srv, "acad_save", expected_document="a.dwg")
    assert first["ok"] is False and first["status"] == "confirm_required" and "Save" not in doc.calls
    call(srv, "acad_add_line", x1=0, y1=0, x2=1, y2=1, expected_document="a.dwg")       # bản vẽ đổi sau bước thử
    assert fail(srv, "acad_save", expected_document="a.dwg", plan_token=first["plan_token"])["code"] == "CONFIRM_REQUIRED"
    second = call(srv, "acad_save", expected_document="a.dwg")
    assert call(srv, "acad_save", expected_document="a.dwg", plan_token=second["plan_token"])["ok"]
    assert doc.calls.count("Save") == 1


def test_save_as_new_file_in_output_needs_no_token(env):
    app, root, make, _ = env
    doc = app.add_doc("Drawing1.dwg", "")
    res = call(make(), "acad_save", expected_document="Drawing1.dwg", path=str(root / "output" / "new.dwg"))
    assert res["ok"] and "SaveAs" in doc.calls


def test_save_as_dxf_keeps_dxf_extension_and_document_stays_addressable(env):
    app, root, make, _ = env
    doc = app.add_doc("Drawing1.dwg", "")
    srv = make()
    dest = str(root / "output" / "flat.dxf")
    res = call(srv, "acad_save", expected_document="Drawing1.dwg", path=dest)
    assert res["ok"] and doc.FullName == dest and res["_target"]["path"] == dest
    assert call(srv, "acad_save", expected_document=dest)["status"] == "confirm_required"   # vẫn tìm được theo đường dẫn


def test_busy_read_after_successful_save_still_reports_success_once(env):
    # smoke AutoCAD 2025: SaveAs thành công rồi lời gọi đọc tên bản vẽ bị từ chối ⇒ từng báo ACAD_BUSY sai
    app, root, make, _ = env
    doc = app.add_doc("Drawing1.dwg", "")
    doc.busy_reads_after_save = 2
    res = call(make(), "acad_save", expected_document="Drawing1.dwg", path=str(root / "output" / "s.dxf"))
    assert res["ok"] is True and doc.calls.count("SaveAs") == 1


def test_command_waits_until_autocad_finishes_it(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    doc.variables["_command_duration"] = 3
    res = call(make(), "acad_command", verb="REGEN", expected_document="a.dwg")
    assert res["ok"] and res["data"]["completed"] is True and doc.command_runs_for == 0


def test_transient_lost_typeinfo_after_close_is_retried_for_reads(env):
    app, root, make, _ = env
    app.add_doc("a.dwg", str(root / "drawings" / "a.dwg"))
    app.lost_typeinfo = 2
    assert call(make(), "acad_list_documents")["ok"]


def test_unexpected_exception_still_returns_coded_error(env):
    app, root, make, _ = env
    app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    app.lost_typeinfo = 99                                   # không hồi phục ⇒ phải ra lỗi có mã, không phải lỗi thô
    err = fail(make(), "acad_activate", name="a.dwg")
    assert err["code"] == "COM_ERROR"


def test_failed_tool_leaves_no_unretrieved_future(env):
    import gc
    app, root, make, _ = env
    app.add_doc("x.dwg", str(root.parent / "elsewhere" / "x.dwg"))
    srv = make()
    seen = []

    async def main():
        asyncio.get_running_loop().set_exception_handler(lambda loop, ctx: seen.append(ctx.get("message")))
        with pytest.raises(ToolError):
            await srv._tool_manager.call_tool("acad_layers", {}, convert_result=False)
        gc.collect()
        await asyncio.sleep(0.05)

    asyncio.run(main())
    assert seen == []


def test_close_discard_needs_token(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    doc.Saved = False
    srv = make()
    dry = call(srv, "acad_close", name="a.dwg", discard=True)
    assert dry["status"] == "confirm_required" and doc in app._docs
    assert call(srv, "acad_close", name="a.dwg", discard=True, plan_token=dry["plan_token"])["ok"]
    assert doc not in app._docs


# --- 5. allow-list lệnh ---------------------------------------------------------------
def test_command_allow_list_on_tool(env):
    app, root, make, _ = env
    doc = app.add_doc("a.dwg", str(root / "output" / "a.dwg"))
    srv = make()
    assert fail(srv, "acad_command", verb="SHELL", expected_document="a.dwg")["code"] == "COMMAND_DENIED"
    call(srv, "acad_command", verb="ZOOM", args=["E"], expected_document="a.dwg")
    assert doc.sent == ["_ZOOM _E "]


# --- 7. sổ kiểm toán --------------------------------------------------------------------
def test_every_call_is_ledgered_without_paths(env):
    app, root, make, ledger = env
    app.add_doc("a.dwg", str(root / "drawings" / "a.dwg"))
    srv = make()
    call(srv, "acad_layers")
    fail(srv, "acad_open", path=str(root.parent / "elsewhere" / "secret.dxf"))
    lines = ledger.path.read_text(encoding="utf-8").splitlines()
    assert [json.loads(x)["outcome"] for x in lines] == ["ok", "PATH_DENIED"]
    assert "secret.dxf" not in ledger.path.read_text(encoding="utf-8") and ledger.verify()


# --- 10. annotation + profile -----------------------------------------------------------
def _tools(srv):
    return {t.name: t for t in srv._tool_manager.list_tools()}


def test_annotations_mark_read_only_and_destructive_tools(env):
    _, _, make, _ = env
    t = _tools(make())
    assert t["acad_layers"].annotations.readOnlyHint is True
    assert t["acad_add_line"].annotations.readOnlyHint is False
    assert t["acad_save"].annotations.destructiveHint is True
    assert all(x.annotations is not None for x in t.values())


def test_read_profile_hides_write_tools(env):
    _, _, make, _ = env
    t = _tools(make("read"))
    assert "acad_layers" in t and "acad_add_line" not in t and "acad_save" not in t and "acad_command" not in t
