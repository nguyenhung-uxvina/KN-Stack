import pytest

from leo_bridge import router


def _exchange(unverified=True):
    return {
        "exchange_id": "LEO-20260704-001",
        "mode": "A",
        "raw": "kết quả Leo dài...",
        "parsed": {"parts": [{"raw_cells": ["6205-2RS", "SKF", "6205-2RS1"]}]},
        "checklist": [{"item": "PN đã đối chiếu?", "status": "UNVERIFIED" if unverified else "VERIFIED"}],
    }


def test_no_confirm_blocked(tmp_path):
    with pytest.raises(router.RouteBlockedError):
        router.write_route(_exchange(), "journal_md", str(tmp_path / "j.md"))


def test_unverified_blocked_from_parts_master(tmp_path):
    with pytest.raises(router.RouteBlockedError) as e:
        router.write_route(_exchange(unverified=True), "parts_master_csv",
                           str(tmp_path / "staging.csv"), confirm=True)
    assert "UNVERIFIED" in str(e.value)


def test_verified_writes_parts_csv(tmp_path):
    p = tmp_path / "staging.csv"
    out = router.write_route(_exchange(unverified=False), "parts_master_csv", str(p), confirm=True)
    content = p.read_text(encoding="utf-8-sig")
    assert "6205-2RS1" in content
    assert "LEO-20260704-001" in content
    assert out == str(p)


def test_journal_allows_unverified_with_label(tmp_path):
    p = tmp_path / "journal.md"
    router.write_route(_exchange(unverified=True), "journal_md", str(p), confirm=True)
    content = p.read_text(encoding="utf-8")
    assert "UNVERIFIED" in content
    assert "LEO-20260704-001" in content


def test_propose_routes_for_parts():
    routes = router.propose_routes("A", {"parts": [{"raw_cells": ["x"]}]})
    types = {r["target_type"] for r in routes}
    assert "parts_master_csv" in types and "journal_md" in types


def test_invalid_target_type_creates_no_dirs(tmp_path):
    target_path = tmp_path / "sub" / "x.csv"
    with pytest.raises(router.RouteBlockedError):
        router.write_route(_exchange(unverified=False), "evil_target", str(target_path), confirm=True)
    assert not (tmp_path / "sub").exists()


def test_csv_formula_injection_neutralized(tmp_path):
    exchange = {
        "exchange_id": "LEO-20260704-002",
        "mode": "A",
        "raw": "kết quả Leo dài...",
        "parsed": {"parts": [{"raw_cells": ['=HYPERLINK("http://x")', "vendor"]}]},
        "checklist": [{"item": "PN đã đối chiếu?", "status": "VERIFIED"}],
    }
    p = tmp_path / "staging.csv"
    router.write_route(exchange, "parts_master_csv", str(p), confirm=True)
    import csv
    with p.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    part_raw = rows[1][3]
    assert not part_raw.startswith("=")
    assert part_raw.startswith("'=HYPERLINK")
