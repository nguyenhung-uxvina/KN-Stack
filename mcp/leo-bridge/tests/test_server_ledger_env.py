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
