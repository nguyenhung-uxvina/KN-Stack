import pytest

from leo_bridge.ledger import Ledger


def test_new_id_increments_per_day(tmp_path):
    led = Ledger(tmp_path)
    id1 = led.new_id()
    led.append(id1, "created", status="SENT", mode="A")
    id2 = led.new_id()
    assert id1.startswith("LEO-")
    assert id1.endswith("-001")
    assert id2.endswith("-002")


def test_get_merges_events_latest_wins(tmp_path):
    led = Ledger(tmp_path)
    ex = led.new_id()
    led.append(ex, "created", status="SENT", mode="C", prompt="p")
    led.append(ex, "ingested", status="INGESTED", raw="kết quả")
    rec = led.get(ex)
    assert rec["status"] == "INGESTED"
    assert rec["prompt"] == "p"
    assert rec["raw"] == "kết quả"


def test_get_unknown_raises(tmp_path):
    with pytest.raises(KeyError):
        Ledger(tmp_path).get("LEO-19700101-999")


def test_list_filters_status(tmp_path):
    led = Ledger(tmp_path)
    a = led.new_id(); led.append(a, "created", status="SENT", mode="A")
    b = led.new_id(); led.append(b, "created", status="SENT", mode="B")
    led.append(b, "ingested", status="INGESTED")
    assert {r["exchange_id"] for r in led.list("SENT")} == {a}
    assert len(led.list()) == 2
