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


def test_missing_fence_in_last_mode_fails_loudly(tmp_path):
    """F has no fence, so its span must NOT reach into the later
    '## Router meta-prompt' section and silently steal that block."""
    bad = tmp_path / "bad.md"
    bad.write_text(
        "## A. X\n```\n[MODE] a\n```\n"
        "## B. X\n```\n[MODE] b\n```\n"
        "## C. X\n```\n[MODE] c\n```\n"
        "## D. X\n```\n[MODE] d\n```\n"
        "### E1. X\n```\n[MODE] e1\n```\n"
        "### E2. X\n```\n[MODE] e2\n```\n"
        "### E3. X\n```\n[MODE] e3\n```\n"
        "## F. X\n"
        "no fence here at all\n"
        "## Router meta-prompt\n```\n[MODE] router\n```\n",
        encoding="utf-8",
    )
    with pytest.raises(templates.TemplateFormatError) as excinfo:
        templates.load_templates(bad)
    assert "F" in str(excinfo.value)


def test_unexpected_mode_key_fails_loudly(tmp_path):
    """A fenced block under an intro heading like '## E.' must not silently
    leak into the returned dict under an unexpected key ('E')."""
    bad = tmp_path / "bad.md"
    bad.write_text(
        "## A. X\n```\n[MODE] a\n```\n"
        "## B. X\n```\n[MODE] b\n```\n"
        "## C. X\n```\n[MODE] c\n```\n"
        "## D. X\n```\n[MODE] d\n```\n"
        "## E. INTRO\n```\n[MODE] e_intro\n```\n"
        "### E1. X\n```\n[MODE] e1\n```\n"
        "### E2. X\n```\n[MODE] e2\n```\n"
        "### E3. X\n```\n[MODE] e3\n```\n"
        "## F. X\n```\n[MODE] f\n```\n",
        encoding="utf-8",
    )
    with pytest.raises(templates.TemplateFormatError) as excinfo:
        templates.load_templates(bad)
    assert "E" in str(excinfo.value)
