"""pytest cho linter plugin fluency-4d."""
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "fluency_4d_lint", Path(__file__).with_name("fluency_4d_lint.py")
)
lint = importlib.util.module_from_spec(_spec)
sys.modules["fluency_4d_lint"] = lint
_spec.loader.exec_module(lint)

RUBRIC = (lint.REF_DIR / "rubric-core.md").read_text(encoding="utf-8")


def test_cells_are_the_canonical_twelve():
    assert lint.CELLS == [
        "del.problem", "del.platform", "del.task",
        "des.product", "des.process", "des.performance",
        "dis.product", "dis.process", "dis.performance",
        "dil.creation", "dil.transparency", "dil.deployment",
    ]


def test_rubric_declares_all_twelve_cells_in_order():
    assert lint.parse_rubric_cells(RUBRIC) == lint.CELLS


def test_rubric_stays_vendor_neutral():
    assert lint.lint_rubric(RUBRIC) == []


def test_rubric_lint_flags_workshop_x_leakage():
    dirty = RUBRIC + "\n\nÁp dụng cho Workshop X.\n"
    assert any("Workshop X" in e for e in lint.lint_rubric(dirty))


def test_rubric_lint_flags_missing_cell():
    stripped = RUBRIC.replace("`dil.deployment`", "`dil.deploy`", 1)
    assert lint.lint_rubric(stripped)
