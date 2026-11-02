"""Test lõi: ComWorker (1 luồng STA + timeout), retry chỉ cho đọc, PathPolicy, CommandPolicy, Ledger, plan token."""
import _winapi
import asyncio
import json
import sys
import threading
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.com_worker import ComWorker, com_read, com_write  # noqa: E402
from core.errors import BridgeError  # noqa: E402
from core.ledger import Ledger  # noqa: E402
from core.plan import PlanTokens  # noqa: E402
from core.policy import CommandPolicy, PathPolicy  # noqa: E402
from fake_acad import busy_error  # noqa: E402


def run(coro):
    return asyncio.run(coro)


# ============================== ComWorker ==============================
def test_worker_runs_every_job_on_one_thread_one_at_a_time():
    w = ComWorker(timeout=5)
    active, peak, threads = [0], [0], set()
    lock = threading.Lock()

    def job():
        with lock:
            active[0] += 1
            peak[0] = max(peak[0], active[0])
        threads.add(threading.get_ident())
        time.sleep(0.05)
        with lock:
            active[0] -= 1
        return 1

    async def main():
        return await asyncio.gather(*(w.run(job) for _ in range(5)))

    assert run(main()) == [1] * 5
    assert peak[0] == 1 and len(threads) == 1
    assert threading.get_ident() not in threads


def test_worker_timeout_while_running_reports_unknown_commit_and_recovers():
    w = ComWorker(timeout=5)
    with pytest.raises(BridgeError) as ei:
        run(w.run(lambda: time.sleep(0.6), timeout=0.1))
    assert ei.value.code == "UNKNOWN_COMMIT"
    assert run(w.run(lambda: "after", timeout=2)) == "after"      # luồng mới thay luồng bị kẹt


def test_worker_timeout_before_start_reports_not_started_and_never_runs():
    w = ComWorker(timeout=5)
    ran = []

    async def main():
        slow = asyncio.ensure_future(w.run(lambda: time.sleep(0.5), timeout=3))
        await asyncio.sleep(0.05)
        with pytest.raises(BridgeError) as ei:
            await w.run(lambda: ran.append(1), timeout=0.1)
        await slow
        await asyncio.sleep(0.6)
        return ei.value.code

    assert run(main()) == "ACAD_TIMEOUT"
    assert ran == []


# ============================== retry đọc / ghi ==============================
def test_com_read_retries_busy_then_succeeds():
    calls = []

    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise busy_error()
        return "ok"

    assert com_read(fn, budget=2, backoff=0.01) == "ok" and len(calls) == 3


def test_com_read_gives_up_after_budget_with_acad_busy():
    def fn():
        raise busy_error()

    with pytest.raises(BridgeError) as ei:
        com_read(fn, budget=0.05, backoff=0.01)
    assert ei.value.code == "ACAD_BUSY"


def test_com_write_never_retries_and_reports_partial():
    calls = []

    def fn():
        calls.append(1)
        raise busy_error()

    with pytest.raises(BridgeError) as ei:
        com_write(fn, partial=["2A1"])
    assert len(calls) == 1
    assert ei.value.code == "ACAD_BUSY" and ei.value.data["partial"] == ["2A1"]


# ============================== PathPolicy ==============================
@pytest.fixture
def ws(tmp_path):
    root = tmp_path / "Workspace"
    (root / "drawings").mkdir(parents=True)
    (root / "output").mkdir()
    install = tmp_path / "Workspace" / "AutoCAD 2025"
    install.mkdir()
    pol = PathPolicy(read_roots=[root], write_roots=[root / "output"], deny_roots=[install])
    return tmp_path, root, pol


def test_read_inside_read_root_is_allowed(ws):
    _, root, pol = ws
    assert pol.check_read(root / "drawings" / "a.dxf") == (root / "drawings" / "a.dxf").resolve()


@pytest.mark.parametrize("rel", ["outside/a.dxf", "Workspace-evil/a.dxf", "Workspace/drawings/../../x.dxf"])
def test_read_outside_or_prefix_trick_or_traversal_is_denied(ws, rel):
    tmp, _, pol = ws
    with pytest.raises(BridgeError) as ei:
        pol.check_read(tmp / rel)
    assert ei.value.code == "PATH_DENIED"


def test_deny_root_wins_even_inside_read_root(ws):
    _, root, pol = ws
    with pytest.raises(BridgeError):
        pol.check_read(root / "AutoCAD 2025" / "Support" / "acad.dxf")


def test_empty_roots_deny_everything(tmp_path):
    with pytest.raises(BridgeError):
        PathPolicy(read_roots=[], write_roots=[], deny_roots=[]).check_read(tmp_path / "a.dxf")


@pytest.mark.parametrize("bad", [r"\\server\share\a.dxf", r"\\?\C:\x\a.dxf", "a.dxf:hidden"])
def test_unc_device_and_ads_paths_are_denied(ws, bad):
    _, root, pol = ws
    p = bad if bad.startswith("\\") else str(root / "drawings" / bad)
    with pytest.raises(BridgeError):
        pol.check_read(p)


def test_write_needs_write_root_not_just_read_root(ws):
    _, root, pol = ws
    pol.check_write(root / "output" / "bom.csv")
    with pytest.raises(BridgeError):
        pol.check_write(root / "drawings" / "bom.csv")


def test_extension_not_allowed_is_denied(ws):
    _, root, pol = ws
    with pytest.raises(BridgeError):
        pol.check_write(root / "output" / "acad.lsp")
    with pytest.raises(BridgeError):
        pol.check_read(root / "drawings" / "evil.fas")


def test_junction_escaping_the_root_is_denied(ws):
    tmp, root, pol = ws
    target = tmp / "secret"
    target.mkdir()
    _winapi.CreateJunction(str(target), str(root / "drawings" / "link"))
    with pytest.raises(BridgeError):
        pol.check_read(root / "drawings" / "link" / "a.dxf")


# ============================== CommandPolicy ==============================
@pytest.mark.parametrize("verb, args, want", [
    ("ZOOM", ["E"], "_ZOOM _E "),
    ("_.zoom", ["e"], "_ZOOM _E "),
    ("REGEN", [], "_REGEN "),
])
def test_command_allow_list_builds_canonical_string(verb, args, want):
    assert CommandPolicy().build(verb, args) == want


@pytest.mark.parametrize("verb, args", [
    ("SHELL", []), ("NETLOAD", []), ("APPLOAD", []),
    ("ZOOM", ["E", "SHELL"]),          # chuỗi phím: tham số thừa thành lệnh mới
    ("ZOOM", ["X"]),
    ("(command", ["\"SHELL\""]),
    ("ZOOM", ["E\nSHELL"]),
    ("REGEN", ["(load \"x\")"]),
])
def test_command_outside_allow_list_is_denied(verb, args):
    with pytest.raises(BridgeError) as ei:
        CommandPolicy().build(verb, args)
    assert ei.value.code == "COMMAND_DENIED"


# ============================== Ledger ==============================
def test_ledger_chains_records_and_detects_tampering(tmp_path):
    lg = Ledger(tmp_path / "ledger.jsonl")
    lg.record("acad_open", {"path": r"D:\MAT\secret.dxf"}, target="abc", outcome="ok")
    lg.record("acad_save", {"path": ""}, target="abc", outcome="CONFIRM_REQUIRED")
    assert lg.verify() is True
    text = (tmp_path / "ledger.jsonl").read_text(encoding="utf-8")
    assert "secret.dxf" not in text                     # chỉ băm tham số, không ghi nội dung
    lines = text.splitlines()
    rec = json.loads(lines[0])
    rec["outcome"] = "forged"
    lines[0] = json.dumps(rec)
    (tmp_path / "ledger.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert lg.verify() is False


# ============================== Plan token ==============================
def test_plan_token_roundtrip_and_binding():
    pt = PlanTokens(ttl=60)
    tok = pt.issue("save", "doc1", 3, {"path": ""})
    assert pt.verify(tok, "save", "doc1", 3, {"path": ""})
    assert not pt.verify(tok, "close_discard", "doc1", 3, {"path": ""})
    assert not pt.verify(tok, "save", "doc2", 3, {"path": ""})
    assert not pt.verify(tok, "save", "doc1", 4, {"path": ""})      # bản vẽ đổi sau bước thử
    assert not pt.verify(tok + "0", "save", "doc1", 3, {"path": ""})


def test_plan_token_expires():
    pt = PlanTokens(ttl=0.05)
    tok = pt.issue("save", "doc1", 0, {})
    time.sleep(0.1)
    assert not pt.verify(tok, "save", "doc1", 0, {})
