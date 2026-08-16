"""pytest cho linter plugin fluency-4d."""
import importlib.util
import re
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


def test_profile_blocks_have_four_required_fields():
    for cell, block in lint.parse_profile(PROFILE).items():
        assert block["tin_hieu"].strip(), f"{cell} thiếu Tín hiệu"
        assert block["co_do"].strip(), f"{cell} thiếu Cờ đỏ"
        assert block["vi_du"].strip(), f"{cell} thiếu Ví dụ ngành"
        assert block["cai_tien"].strip(), f"{cell} thiếu Cách cải tiến tại chỗ"


def test_profile_lint_flags_missing_improvement_field():
    """Negative: mất trường cải tiến tại chỗ thì lớp riêng của tổ chức rỗng."""
    dirty = re.sub(r"\*\*Cách cải tiến tại chỗ:\*\*[^\n]*",
                   "**Cách cải tiến tại chỗ:**", PROFILE, count=1)
    errors = lint.lint_profile(dirty)
    assert any("Cách cải tiến tại chỗ" in e for e in errors), errors


def test_profile_is_clean():
    assert lint.lint_profile(PROFILE) == []


def test_profile_lint_flags_scale_redefinition():
    dirty = PROFILE + "\n## Thang điểm\nDùng thang 0-3 riêng.\n"
    assert any("thang điểm" in e.lower() for e in lint.lint_profile(dirty))


def test_profile_lint_flags_missing_cell():
    dirty = PROFILE.replace("## dil.deployment", "## dil.xxx", 1)
    assert any("dil.deployment" in e for e in lint.lint_profile(dirty))


ACTIVE = (lint.REF_DIR / "active-profile.md").read_text(encoding="utf-8")
TEMPLATE = (lint.REF_DIR / "profile-template.md").read_text(encoding="utf-8")
QUANDOC = (lint.REF_DIR / "profile-quan-doc.md").read_text(encoding="utf-8")


def test_active_profile_points_at_a_real_profile():
    assert lint.lint_active_profile(ACTIVE) == []


def test_active_pointer_names_exactly_one_file():
    name = lint.parse_active_profile(ACTIVE)
    assert name and name.startswith("profile-") and name.endswith(".md"), name
    assert (lint.REF_DIR / name).is_file()


def test_active_profile_rejects_the_blank_template():
    """Khuôn rỗng bật lên = chấm điểm theo 48 ô trống mà báo cáo vẫn ra đủ hình."""
    dirty = ACTIVE.replace("profile-workshop-x.md", "profile-template.md", 1)
    errors = lint.lint_active_profile(dirty)
    assert any("khuôn rỗng" in e for e in errors), errors


def test_active_profile_rejects_a_draft_with_open_todos():
    """Chốt chính của tầng trỏ: profile còn ô ⟨CEO chốt: …⟩ thì KHÔNG được bật.

    Bật một profile chưa điền xong nghĩa là chấm điểm theo tín hiệu chưa ai chốt —
    báo cáo vẫn ra đủ hình, nên lỗi này im lặng nếu không có cổng chặn.

    Nháp được bơm vào qua `read` thay vì trỏ tới một file thật: file thật rồi sẽ
    được điền xong (profile-quan-doc đã điền xong 2026-08-02), lúc đó test mất răng
    mà không ai biết.
    """
    dirty = ACTIVE.replace("profile-workshop-x.md", "profile-nhap.md", 1)
    draft = TEMPLATE  # khuôn rỗng = nháp cực đoan, mọi trường đều còn ô chờ điền
    errors = lint.lint_active_profile(dirty, read=lambda name: draft)
    assert any("⟨CEO chốt" in e for e in errors), errors


def test_active_profile_rejects_missing_file():
    dirty = ACTIVE.replace("profile-workshop-x.md", "profile-khong-co-that.md", 1)
    errors = lint.lint_active_profile(dirty)
    assert any("không tồn tại" in e for e in errors), errors


def test_template_is_entirely_unfilled():
    """Khuôn phải rỗng đủ 48 ô — 12 mã ô × 4 trường. Thiếu ô nào là khuôn đã bị điền sẵn."""
    assert sorted(lint.parse_profile(TEMPLATE)) == sorted(lint.CELLS)
    for cell, block in lint.parse_profile(TEMPLATE).items():
        for key in ("tin_hieu", "co_do", "vi_du", "cai_tien"):
            assert "⟨CEO chốt:" in block[key], f"{cell}/{key} đã bị điền sẵn trong khuôn"


def test_quandoc_profile_is_complete_and_activatable():
    """CEO chốt đủ 12 cờ đỏ ngày 2026-08-02 → profile này bật được.

    Trước đó nó là nháp với 12 trường Cờ đỏ bỏ trống. Cờ đỏ là tuyên bố hành vi nào
    không chấp nhận được trong xưởng — AI soạn tín hiệu/ví dụ/cách cải tiến, nhưng
    không soạn trường này.
    """
    assert lint.count_todo(QUANDOC) == 0, "còn ô chờ điền — chưa bật được"
    assert lint.lint_profile(QUANDOC) == []
    blocks = lint.parse_profile(QUANDOC)
    assert sorted(blocks) == sorted(lint.CELLS)


def test_every_profile_keeps_the_four_field_frame():
    """Mọi profile phải cùng khung — kể cả khuôn rỗng và profile mới thêm sau này.

    Quét cả thư mục thay vì liệt kê tên file: profile thứ tư thêm vào mà sai khung
    thì phải đỏ ngay, không đợi ai nhớ ra viết thêm test.
    """
    files = sorted(lint.REF_DIR.glob("profile-*.md"))
    assert len(files) >= 3, [f.name for f in files]
    for f in files:
        text = f.read_text(encoding="utf-8")
        assert lint.lint_profile(text, allow_draft=True) == [], f.name


PLAYBOOK = (lint.REF_DIR / "improvement-playbook.md").read_text(encoding="utf-8")


def test_playbook_covers_every_rubric_cell():
    assert sorted(lint.parse_playbook(PLAYBOOK)) == sorted(lint.CELLS)


def test_playbook_blocks_have_four_required_fields():
    for cell, block in lint.parse_playbook(PLAYBOOK).items():
        assert block["cach"].strip(), f"{cell} thiếu Cách cải tiến"
        assert block["dau_hieu"].strip(), f"{cell} thiếu Dấu hiệu đã ăn"
        assert block["bay"].strip(), f"{cell} thiếu Bẫy thường gặp"
        assert block["ceo"].strip(), f"{cell} thiếu CEO phải tự chốt"


def test_playbook_is_clean():
    assert lint.lint_playbook(PLAYBOOK) == []


def test_playbook_stays_vendor_neutral():
    """Playbook là tầng lõi — ví dụ riêng tổ chức thuộc về profile, không thuộc đây."""
    for bad in lint._RUBRIC_FORBIDDEN:
        assert bad not in PLAYBOOK, f"playbook lẫn tín hiệu riêng ngành: {bad!r}"


def test_playbook_lint_flags_deleted_row():
    """Negative: xoá một mục playbook thì lint phải kêu.

    Weekly bị cấm tự chế cách cải tiến, nên mục biến mất KHÔNG được AI ứng biến bù.
    Mất mục = mất thật, và cổng phải bắt trước khi tới tay người dùng.
    """
    dirty = PLAYBOOK.replace("## dis.process", "## dis.xxx", 1)
    errors = lint.lint_playbook(dirty)
    assert any("dis.process" in e for e in errors), errors


def test_playbook_lint_flags_missing_ceo_field():
    """Negative: mất trường 'CEO phải tự chốt' = mất ranh giới không uỷ thác được."""
    dirty = re.sub(r"\*\*CEO phải tự chốt:\*\*[^\n]*",
                   "**CEO phải tự chốt:**", PLAYBOOK, count=1)
    errors = lint.lint_playbook(dirty)
    assert any("CEO phải tự chốt" in e for e in errors), errors


def test_weekly_cites_the_playbook():
    """Weekly trước đây không trích dẫn file tham chiếu nào nên nằm ngoài mọi guard
    đường dẫn. Trích dẫn playbook kéo nó vào cùng vòng canh với hai skill kia."""
    text = (lint.SKILLS_ROOT / "fluency-4d-weekly" / "SKILL.md").read_text(encoding="utf-8")
    cited = {ref for _, ref in lint._REF_CITE_RE.findall(text)}
    assert "improvement-playbook.md" in cited, cited


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


def _superseded_row(**over):
    row = {"id": "EXP-001", "cell": "dil.transparency",
           "if_then": "Khi tôi đẩy một PR ra ngoài, tôi ghi một dòng nêu phần AI đã tham gia.",
           "streak": 1, "breaks": 1, "status": "SUPERSEDED",
           "opened": "2026-08-01", "closed": "2026-08-02"}
    row.update(over)
    return row


def test_superseded_is_a_valid_status():
    assert lint.validate_experiments([_superseded_row()]) == []


def test_superseded_requires_close_date():
    assert any("ngày đóng" in e for e in lint.validate_experiments([_superseded_row(closed="")]))


def test_superseded_rejected_when_it_should_be_passed():
    errs = lint.validate_experiments([_superseded_row(streak=3)])
    assert any("SUPERSEDED" in e for e in errs), errs


def test_superseded_rejected_when_it_should_be_failed():
    errs = lint.validate_experiments([_superseded_row(breaks=3)])
    assert any("SUPERSEDED" in e for e in errs), errs


def test_superseded_does_not_block_a_new_open_row():
    """Đóng sớm rồi mở cái mới không được tính là vi phạm WIP=1."""
    rows = [_superseded_row(),
            {"id": "EXP-002", "cell": "des.performance",
             "if_then": "Khi phiên có quyết định lớn, tôi giao vai phản biện đích danh.",
             "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-02", "closed": ""}]
    assert lint.validate_experiments(rows) == []


def test_superseded_row_absorbs_no_further_sessions():
    """Phiên sau khi đã đóng sớm thuộc thí nghiệm KẾ TIẾP, không nới streak bản ghi cũ."""
    assert lint.apply_session(_superseded_row(), held=True) == _superseded_row()


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


SKILLS = lint.load_skill_sources()
PLUGIN_MD = lint.load_plugin_markdown()
SEED_EXP = (lint.PLUGIN_ROOT / "templates" / "experiments.md").read_text(encoding="utf-8")


def test_all_three_skills_are_loaded():
    assert sorted(SKILLS) == [f"{n}/SKILL.md" for n in lint.SKILL_NAMES]


def test_skills_are_clean():
    assert lint.lint_skills() == []


def test_skills_cite_at_least_one_shared_reference():
    cited = {r for text in SKILLS.values() for _, r in lint._REF_CITE_RE.findall(text)}
    assert cited, "không SKILL.md nào trích dẫn thư mục tham chiếu — regex đã chết"
    assert "rubric-core.md" in cited


def test_cited_dirs_are_all_the_shared_dir():
    """Mọi citation phải trỏ đúng thư mục dùng chung, không chỉ đúng tên file."""
    dirs = {d for text in SKILLS.values() for d, _ in lint._REF_CITE_RE.findall(text)}
    assert dirs == {lint.SHARED_DIR_NAME}, f"thư mục lạ trong citation: {dirs}"


def test_citations_resolve_relative_to_skill_dir():
    """Copy trần: '..' trỏ thư mục cha thật, nên citation phải resolve từ chính skill dir.

    Kiểm này khác `test_skills_are_clean` — chỗ kia hỏi 'file có tồn tại ở REF_DIR
    không', chỗ này hỏi 'đi từ skill dir theo đúng chuỗi ../ có tới file không'.
    Chỉ kiểm này bắt được lỗi cây thư mục bị dựng sai hình khi đem plugin đi nơi khác.
    """
    for name in lint.SKILL_NAMES:
        skill_dir = lint.SKILLS_ROOT / name
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        for ref_dir, ref in sorted(set(lint._REF_CITE_RE.findall(text))):
            target = (skill_dir / ".." / ref_dir / "references" / ref).resolve()
            assert target.is_file(), f"{name}: ../{ref_dir}/references/{ref} không resolve được"


def test_lint_skills_flags_missing_reference_file():
    """Negative: SKILL.md trỏ tới file tham chiếu không tồn tại."""
    dirty = dict(SKILLS)
    dirty["fluency-4d-review/SKILL.md"] += (
        f"\n- `../{lint.SHARED_DIR_NAME}/references/khong-co-that.md`\n"
    )
    errors = lint.lint_skills(skills=dirty, all_markdown=PLUGIN_MD)
    assert any("khong-co-that.md" in e for e in errors)


def test_lint_skills_flags_stale_shared_dir_in_skill():
    """Negative — chế độ hỏng đã trả giá ở PR #16: tên file đúng, THƯ MỤC đã chết.

    Trước khi siết, ca này xanh 43/43: regex nướng cứng tên thư mục nên citation
    trỏ thư mục không tồn tại vẫn cho ra tên file có thật và vẫn được coi là đạt.
    """
    dirty = {
        name: text.replace(f"../{lint.SHARED_DIR_NAME}/", "../_shared/")
        for name, text in SKILLS.items()
    }
    assert dirty != SKILLS, "fixture không đổi được gì — citation đã không còn ở dạng ../"
    errors = lint.lint_skills(skills=dirty, all_markdown=PLUGIN_MD)
    assert any("sai thư mục dùng chung" in e for e in errors)


def test_lint_skills_flags_stale_shared_dir_in_readme():
    """Negative: đổi tên nửa vời — SKILL.md sửa rồi nhưng README còn trỏ tên cũ."""
    dirty = dict(PLUGIN_MD)
    key = "README.md"
    assert key in dirty
    dirty[key] = dirty[key].replace(f"{lint.SHARED_DIR_NAME}/references/", "_shared/references/")
    errors = lint.lint_skills(skills=SKILLS, all_markdown=dirty)
    assert any("thư mục tham chiếu lạ" in e for e in errors)


def test_lint_skills_flags_reference_that_vanishes():
    """Negative: file tham chiếu có thật biến mất khỏi đĩa."""
    errors = lint.lint_skills(
        skills=SKILLS, all_markdown=PLUGIN_MD, ref_exists=lambda fn: False
    )
    assert any("rubric-core.md" in e for e in errors)


def test_lint_skills_flags_drifted_ledger_path():
    """Negative: đường dẫn sổ điểm lệch một ký tự ở một file."""
    dirty = dict(PLUGIN_MD)
    key = "skills/fluency-4d-weekly/SKILL.md"
    assert key in dirty
    dirty[key] = dirty[key].replace("CEO-Self", "CEO_Self")
    errors = lint.lint_skills(skills=SKILLS, all_markdown=dirty)
    assert any("lệch nhau" in e for e in errors)


def test_ledger_path_appears_in_every_skill():
    for name, text in SKILLS.items():
        assert lint._LEDGER_PATH_RE.search(text), f"{name} không nhắc đường dẫn sổ điểm"


def test_seed_experiments_header_matches_protocol():
    """Bản mẫu ledger phải mang ĐÚNG dòng tiêu đề 8 cột mà parse_experiments đọc được."""
    header = "| ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng |"
    assert header in EXP_DOC
    assert header in SEED_EXP
    cols = [c.strip() for c in header.strip("|").split("|")]
    assert len(cols) == len(lint._EXP_COLS) == 8


def test_seed_experiments_is_empty_but_usable():
    assert lint.parse_experiments(SEED_EXP) == []
    row = "| `EXP-001` | `des.product` | Khi giao task, tôi nêu tiêu chí xong. | 0 | 0 | OPEN | 2026-08-01 |  |"
    rows = lint.parse_experiments(SEED_EXP + row + "\n")
    assert len(rows) == 1
    assert lint.validate_experiments(rows) == []


def test_ledger_lifecycle_four_sessions():
    """Bốn phiên liên tiếp: streak 1→2→3→PASSED, mọi dòng sổ hợp lệ."""
    sample = lint.extract_sample_record(LEDGER_DOC)
    exp = {"id": "EXP-001", "cell": "des.product",
           "if_then": "Khi giao task > 30 phút, tôi nêu tiêu chí xong trước khi bấm gửi.",
           "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    streaks = []
    for day, held in enumerate([True, True, True, True], start=1):
        rec = dict(sample)
        rec["id"] = f"2026-08-0{day}-1"
        rec["date"] = f"2026-08-0{day}"
        rec["exp_active"] = exp["id"]
        rec["exp_held"] = held
        assert lint.validate_ledger_line(rec) == [], rec["id"]
        if exp["status"] == "OPEN":
            exp = lint.apply_session(exp, held=held)
        streaks.append((exp["streak"], exp["status"]))
    assert streaks == [(1, "OPEN"), (2, "OPEN"), (3, "PASSED"), (3, "PASSED")]


def test_ledger_lifecycle_same_broken_fixture_fails():
    """Spec §9.3: chạy lại CÙNG một fixture 4 lần thì phải ra FAILED, không phải PASSED.

    Fixture cài sẵn chính lỗi mà thí nghiệm nhắm tới, nên hành vi đứt mọi lần chạy.
    Nhánh PASSED ở test trên là fixture ĐÃ SỬA — hai phép thử khác nhau, đừng gộp.
    """
    sample = lint.extract_sample_record(LEDGER_DOC)
    exp = {"id": "EXP-001", "cell": "dil.creation",
           "if_then": "Khi soạn prompt so sánh chi phí, tôi thay tên và giá thật bằng nhà cung cấp A/B.",
           "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    states = []
    for day in range(1, 5):
        rec = dict(sample)
        rec["id"] = f"2026-08-0{day}-1"
        rec["date"] = f"2026-08-0{day}"
        rec["exp_active"] = exp["id"]
        rec["exp_held"] = False  # fixture chứa sẵn lỗi → đứt, mọi lần
        assert lint.validate_ledger_line(rec) == [], rec["id"]
        if exp["status"] == "OPEN":
            exp = lint.apply_session(exp, held=False)
        states.append((exp["breaks"], exp["status"]))
    assert states == [(1, "OPEN"), (2, "OPEN"), (3, "FAILED"), (3, "FAILED")]
    assert exp["streak"] == 0, "streak không được nhích khi hành vi đứt mọi lần"
