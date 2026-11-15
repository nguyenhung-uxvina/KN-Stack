"""Khuôn của /book-to-learn phải khớp tên trường mà btl_gate_check đọc,
và khuôn TRỐNG phải TRƯỢT cổng (khuôn không được tự đạt)."""
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
T = ROOT / "skills" / "book" / "book-to-learn" / "references" / "templates"
_spec = importlib.util.spec_from_file_location("gc", HERE / "btl_gate_check.py")
gc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gc)


def keys(name):
    return set(gc.parse_frontmatter((T / name).read_text(encoding="utf-8")))


@pytest.mark.parametrize("name,expected", [
    ("pipeline-state.md", "STATE_KEYS"),
    ("mission.md", "BRIEF_KEYS"),
    ("feynman.md", "FEYNMAN_KEYS"),
    ("experiment-card.md", "CARD_KEYS"),
    ("aar.md", "AAR_KEYS"),
])
def test_template_has_checker_keys(name, expected):
    assert set(getattr(gc, expected)) <= keys(name)


def test_aar_template_headings():
    secs = gc.sections((T / "aar.md").read_text(encoding="utf-8"))
    assert all(h in secs for h in gc.AAR_HEADINGS)


def test_cycles_row_keys_match():
    row = json.loads((T / "cycles-row.json").read_text(encoding="utf-8"))
    assert set(row) == set(gc.CYCLE_KEYS)


def test_no_arg_substitution_hazard_in_templates():
    for p in T.iterdir():
        assert not gc.ARG_SUBST.search(p.read_text(encoding="utf-8")), p.name


@pytest.mark.parametrize("phase,files", [
    ("L0", {"mission.md": "_Project_Brief.md"}),
    ("L5", {"experiment-card.md": "Experiment_Card.md"}),
])
def test_blank_template_fails_gate(tmp_path, phase, files):
    learn = tmp_path / "vault" / "1_Projects" / "LEARN-demo"
    learn.mkdir(parents=True)
    state = (T / "pipeline-state.md").read_text(encoding="utf-8").replace("slug:", "slug: demo", 1)
    (learn / "_pipeline_state.md").write_text(state, encoding="utf-8")
    for src, dst in files.items():
        shutil.copy(T / src, learn / dst)
    assert gc.main([str(learn), phase, "--no-stamp", "--skills-root", str(tmp_path)]) == 1
