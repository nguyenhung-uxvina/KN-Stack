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
PROFILE = (lint.REF_DIR / "profile-workshop-x.md").read_text(encoding="utf-8")


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


def test_modes_constant_is_canonical():
    assert lint.MODES == {"automation", "augmentation", "agency"}


def test_profile_covers_every_rubric_cell():
    assert sorted(lint.parse_profile(PROFILE)) == sorted(lint.CELLS)


def test_profile_blocks_have_three_required_fields():
    for cell, block in lint.parse_profile(PROFILE).items():
        assert block["tin_hieu"].strip(), f"{cell} thiếu Tín hiệu"
        assert block["co_do"].strip(), f"{cell} thiếu Cờ đỏ"
        assert block["vi_du"].strip(), f"{cell} thiếu Ví dụ ngành"


def test_profile_is_clean():
    assert lint.lint_profile(PROFILE) == []


def test_profile_lint_flags_scale_redefinition():
    dirty = PROFILE + "\n## Thang điểm\nDùng thang 0-3 riêng.\n"
    assert any("thang điểm" in e.lower() for e in lint.lint_profile(dirty))


def test_profile_lint_flags_missing_cell():
    dirty = PROFILE.replace("## dil.deployment", "## dil.xxx", 1)
    assert any("dil.deployment" in e for e in lint.lint_profile(dirty))


import copy
import json

LEDGER_DOC = (lint.REF_DIR / "ledger-schema.md").read_text(encoding="utf-8")


def _good_record():
    return copy.deepcopy(lint.extract_sample_record(LEDGER_DOC))


def test_sample_record_in_doc_is_valid():
    assert lint.validate_ledger_line(_good_record()) == []


def test_sample_record_has_every_cell():
    rec = _good_record()
    flat = {f"{g}.{k}" for g, sub in rec["scores"].items() for k in sub}
    assert flat == set(lint.CELLS)


def test_rejects_missing_top_level_key():
    rec = _good_record()
    del rec["weakest"]
    assert any("weakest" in e for e in lint.validate_ledger_line(rec))


def test_rejects_score_out_of_range():
    rec = _good_record()
    rec["scores"]["del"]["problem"] = 4
    assert any("del.problem" in e for e in lint.validate_ledger_line(rec))


def test_accepts_null_as_na():
    rec = _good_record()
    rec["scores"]["del"]["problem"] = None
    assert lint.validate_ledger_line(rec) == []


def test_rejects_unknown_mode():
    rec = _good_record()
    rec["mode"] = "collaboration"
    assert any("mode" in e for e in lint.validate_ledger_line(rec))


def test_rejects_bad_id_format():
    rec = _good_record()
    rec["id"] = "2026-08-01"
    assert any("id" in e for e in lint.validate_ledger_line(rec))


def test_rejects_weakest_not_a_cell():
    rec = _good_record()
    rec["weakest"] = "des.speed"
    assert any("weakest" in e for e in lint.validate_ledger_line(rec))


def test_exp_active_and_exp_held_must_agree():
    rec = _good_record()
    rec["exp_active"] = None
    assert any("exp_held" in e for e in lint.validate_ledger_line(rec))


EXP_DOC = (lint.REF_DIR / "experiment-protocol.md").read_text(encoding="utf-8")


def test_sample_table_parses():
    rows = lint.parse_experiments(EXP_DOC)
    assert rows, "experiment-protocol.md phải có bảng mẫu"
    assert rows[0]["id"].startswith("EXP-")
    assert rows[0]["cell"] in lint.CELLS


def test_sample_table_is_valid():
    assert lint.validate_experiments(lint.parse_experiments(EXP_DOC)) == []


def test_wip_one_enforced():
    rows = [
        {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
         "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""},
        {"id": "EXP-002", "cell": "dis.product", "if_then": "Khi nhận số, tôi hỏi nguồn.",
         "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-02", "closed": ""},
    ]
    assert any("WIP" in e for e in lint.validate_experiments(rows))


def test_if_then_form_required():
    rows = [{"id": "EXP-001", "cell": "des.product", "if_then": "Chú ý Description hơn.",
             "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}]
    assert any("nếu–thì" in e for e in lint.validate_experiments(rows))


def test_passed_requires_streak_three():
    rows = [{"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
             "streak": 2, "breaks": 0, "status": "PASSED", "opened": "2026-08-01", "closed": "2026-08-04"}]
    assert any("PASSED" in e for e in lint.validate_experiments(rows))


def test_streak_increments_on_hold():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    assert lint.apply_session(row, held=True)["streak"] == 2


def test_third_hold_passes_the_experiment():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 2, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=True)
    assert out["streak"] == 3 and out["status"] == "PASSED"


def test_break_resets_streak_and_counts():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 2, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=False)
    assert out["streak"] == 0 and out["breaks"] == 1 and out["status"] == "OPEN"


def test_third_break_fails_the_experiment():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 2, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=False)
    assert out["breaks"] == 3 and out["status"] == "FAILED"


def test_apply_session_does_not_mutate_input():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    lint.apply_session(row, held=True)
    assert row["streak"] == 1


def test_hold_does_not_reset_breaks():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 0, "breaks": 2, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=True)
    assert out["streak"] == 1 and out["breaks"] == 2


def test_apply_session_ignores_passed_row():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 3, "breaks": 0, "status": "PASSED", "opened": "2026-08-01", "closed": "2026-08-04"}
    for held in (True, False):
        out = lint.apply_session(row, held=held)
        assert out["streak"] == 3 and out["breaks"] == 0 and out["status"] == "PASSED"
        assert out is not row


def test_apply_session_ignores_failed_row():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 0, "breaks": 3, "status": "FAILED", "opened": "2026-08-01", "closed": "2026-08-04"}
    for held in (True, False):
        out = lint.apply_session(row, held=held)
        assert out["streak"] == 0 and out["breaks"] == 3 and out["status"] == "FAILED"
        assert out is not row
