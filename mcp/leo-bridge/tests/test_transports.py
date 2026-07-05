import pytest

from leo_bridge import transports


class FakeClip:
    def __init__(self):
        self.buf = ""

    def copy(self, t):
        self.buf = t

    def paste(self):
        return self.buf


@pytest.fixture
def clip(monkeypatch):
    fake = FakeClip()
    monkeypatch.setattr(transports.ClipboardTransport, "_copy", lambda self, t: fake.copy(t))
    monkeypatch.setattr(transports.ClipboardTransport, "_paste", lambda self: fake.paste())
    return fake


def test_send_copies_and_returns_instructions(clip):
    t = transports.ClipboardTransport()
    ins = t.send("[MODE] PART SEARCH ...")
    assert clip.buf.startswith("[MODE]")
    assert "app.getleo.ai" in ins
    assert "leo_ingest" in ins


def test_receive_empty_clipboard_raises(clip):
    t = transports.ClipboardTransport()
    with pytest.raises(transports.TransportError):
        t.receive()


def test_get_transport_defaults_clipboard(monkeypatch):
    monkeypatch.delenv("LEO_API_KEY", raising=False)
    assert transports.get_transport().name == "clipboard"


def test_api_transport_is_stub(monkeypatch):
    monkeypatch.setenv("LEO_API_KEY", "x")
    t = transports.get_transport()
    assert t.name == "api"
    with pytest.raises(NotImplementedError):
        t.send("p")
