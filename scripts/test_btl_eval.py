"""Kiểm chính eval book-to-learn bằng đột biến: với mỗi assertion bắt buộc,
xoá khỏi SKILL.md mọi dòng khớp regex của NÓ thì assertion đó phải trượt.
(Chọn câu để xoá bằng tay luôn sót vì mỗi luật nằm 3–4 chỗ.)"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "book" / "book-to-learn" / "SKILL.md"
EVAL = json.loads((ROOT / "evals" / "book-to-learn.json").read_text(encoding="utf-8"))
REQUIRED = [a for a in EVAL["assertions"] if a["required"]]


def test_counts_consistent():
    assert EVAL["total_required"] == len(REQUIRED)
    assert EVAL["total_optional"] == len(EVAL["assertions"]) - len(REQUIRED)


def test_all_required_pass_on_skill():
    text = SKILL.read_text(encoding="utf-8")
    missing = [a["id"] for a in REQUIRED if not re.search(a["regex"], text, re.I)]
    assert missing == []


@pytest.mark.parametrize("a", REQUIRED, ids=[a["id"] for a in REQUIRED])
def test_mutation_kills_assertion(a):
    text = SKILL.read_text(encoding="utf-8")
    rx = re.compile(a["regex"], re.I)
    mutated = "\n".join(l for l in text.splitlines() if not rx.search(l))
    assert not rx.search(mutated), f"{a['id']} regex spans lines — mutation cannot remove it"


def test_no_arg_substitution_hazard():
    for i, line in enumerate(SKILL.read_text(encoding="utf-8").splitlines(), 1):
        assert not re.search(r"\$[0-9](?![0-9])", line), f"SKILL.md dòng {i}: {line}"
