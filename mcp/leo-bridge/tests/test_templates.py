import pytest

from leo_bridge import templates


def test_load_real_templates_has_all_modes():
    t = templates.load_templates()
    assert set(t) == {"A", "B", "C", "D", "E1", "E2", "E3", "F"}
    assert "[FUNCTION]" in t["A"]
    assert "[KNOWNS]" in t["C"]
    assert "[GIẢ ĐỊNH]" in t["A"]


def test_missing_mode_fails_loudly(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("## A. ONLY\n```\n[MODE] x\n```\n", encoding="utf-8")
    with pytest.raises(templates.TemplateFormatError):
        templates.load_templates(bad)
