"""pytest cho btl_gate_check.py — cổng máy của /book-to-learn.

Mỗi cổng có ít nhất một ca ĐẠT và các ca TRƯỢT tương ứng với lỗi đã gặp thật
(nhãn quyết định (A)/(B) bị ghi sai, $0 bị thay thành tham số, nguồn NLM status=2
nhưng là trang chặn bot, câu trả lời Feynman do AI điền...).
"""
import importlib.util
import json
import textwrap
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("gc", HERE / "btl_gate_check.py")
gc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gc)


def w(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return path


@pytest.fixture
def env(tmp_path):
    vault = tmp_path / "vault"
    learn = vault / "1_Projects" / "LEARN-demo"
    (vault / "1_Projects" / "VN-TGT-F").mkdir(parents=True)
    ns = SimpleNamespace(
        vault=vault,
        learn=learn,
        skills=tmp_path / "skills",
        books=vault / "3_Resources" / "Books",
        meta=vault / "2_Areas" / "CEO-Self" / "Learning-Meta",
        tmp=tmp_path,
    )
    w(learn / "_pipeline_state.md", """
        ---
        slug: demo
        framework_ung_vien: [Small Plates]
        ---
        """)
    return ns


def run(env, phase, *extra):
    argv = [str(env.learn), phase,
            "--skills-root", str(env.skills),
            "--books-root", str(env.books),
            "--meta-dir", str(env.meta), *extra]
    return gc.main(argv)


def state_text(env):
    return (env.learn / "_pipeline_state.md").read_text(encoding="utf-8")


def wbom(path: Path, text: str) -> Path:
    """Write with a UTF-8 BOM prefix — PowerShell Out-File default on this host."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\xef\xbb\xbf" + textwrap.dedent(text).lstrip("\n").encode("utf-8"))
    return path


GOOD_BRIEF = """
    ---
    van_de_that: Định giá pilot VN-TGT-F khi biên gộp ở mức 10 bộ gần bằng 0
    du_doan_1: Sách khuyên trích lợi nhuận trên mọi khoản thu, kể cả hợp đồng nhỏ
    du_doan_2: Sách không nói gì về hợp đồng quốc phòng dài hạn
    du_doan_3: Framework dễ áp nhất sẽ là tách tài khoản
    dreyfus_truoc: 2
    target: VN-TGT-F
    noi_ap_dung:
    tieu_chi_thanh_cong: Có quyết định giá pilot kèm con số trước ngày 30
    ---
    ## Quyết định
    - Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận
    """


# ---------- helpers ----------

def test_parse_frontmatter_types():
    fm = gc.parse_frontmatter("---\na: x: y\nb: [P, Q R]\nc: true\nd: \"q\"\n---\nbody")
    assert fm == {"a": "x: y", "b": ["P", "Q R"], "c": True, "d": "q"}


def test_table_rows_drops_header_and_separator():
    rows = gc.table_rows("| H1 | H2 |\n|---|---|\n| a | b |\n| c | d |\n")
    assert rows == [["a", "b"], ["c", "d"]]


def test_slugify_vietnamese():
    assert gc.slugify("Đảo công thức: Lợi nhuận trước") == "dao-cong-thuc-loi-nhuan-truoc"


# ---------- CLI ----------

def test_unknown_phase_is_usage_error(env):
    assert run(env, "L9") == 2


def test_missing_state_is_usage_error(env):
    (env.learn / "_pipeline_state.md").unlink()
    assert run(env, "L0") == 2


# ---------- L0 ----------

def test_L0_pass_and_stamp(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    assert run(env, "L0") == 0
    assert "- L0: PASS " in state_text(env)
    assert gc.gate_passed(gc.Ctx.from_args(gc.parse_args([str(env.learn), "L0"])), "L0")


def test_L0_stamp_replaces_not_duplicates(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    run(env, "L0")
    run(env, "L0")
    assert state_text(env).count("- L0: PASS ") == 1


def test_L0_no_stamp_flag(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    assert run(env, "L0", "--no-stamp") == 0
    assert "L0: PASS" not in state_text(env)


def test_L0_fails_without_real_problem(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "van_de_that: Định giá pilot VN-TGT-F khi biên gộp ở mức 10 bộ gần bằng 0", "van_de_that:"))
    assert run(env, "L0") == 1
    assert "van_de_that" in capsys.readouterr().out
    assert "L0: PASS" not in state_text(env)


def test_L0_fails_with_two_predictions(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "du_doan_3: Framework dễ áp nhất sẽ là tách tài khoản", "du_doan_3:"))
    assert run(env, "L0") == 1
    assert "3 dự đoán" in capsys.readouterr().out


def test_L0_fails_bad_dreyfus(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("dreyfus_truoc: 2", "dreyfus_truoc: cao"))
    assert run(env, "L0") == 1


def test_L0_fails_missing_target_project(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target: VN-KHONG-CO"))
    assert run(env, "L0") == 1
    assert "VN-KHONG-CO" in capsys.readouterr().out


def test_L0_passes_without_target_if_noi_ap_dung(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target:")
      .replace("noi_ap_dung:", "noi_ap_dung: Cả Workshop X — dòng tiền công ty"))
    assert run(env, "L0") == 0


def test_L0_fails_without_target_and_noi_ap_dung(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target:"))
    assert run(env, "L0") == 1


@pytest.mark.parametrize("line", [
    "- Định giá pilot: (B)", "- (A)", "- Phương án: B",
    "- chọn A", "- Chọn (A).", "- Quyết định: chọn B",
])
def test_L0_fails_label_only_decision(env, capsys, line):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "- Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận", line))
    assert run(env, "L0") == 1
    assert "bằng chữ" in capsys.readouterr().out


def test_L0_passes_worded_decision_with_chon_verb(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "- Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận",
        "- Chọn A vì giữ thói quen trích lợi nhuận"))
    assert run(env, "L0") == 0


# ---------- BOM (PowerShell Out-File default trên host này) ----------

def test_L0_pass_with_bom_project_brief(env):
    wbom(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    assert run(env, "L0") == 0


def test_state_with_bom_resolves_slug(env):
    wbom(env.learn / "_pipeline_state.md", """
        ---
        slug: demo
        framework_ung_vien: [Small Plates]
        ---
        """)
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    ctx = gc.Ctx.from_args(gc.parse_args([str(env.learn), "L0"]))
    assert ctx.slug == "demo"
    assert run(env, "L0") == 0


# ---------- L1 ----------

def make_L1(env, skill_md="# Demo\nTAP 0–250K USD; nhân sự $150K–$250K\n", level="L5"):
    w(env.skills / "demo" / "SKILL.md", skill_md)
    w(env.skills / "demo" / "chapters" / "ch01-intro.md", "# Ch1\n")
    w(env.books / "demo" / "Leverage_Map.md", f"""
        | Framework | Mức | Lý do | Chương |
        |---|---|---|---|
        | Small Plates | {level} | đổi luật chơi phân bổ | ch02 |
        """)
    w(env.books / "demo" / "Learning_Kit.md", "## Small Plates\n### Chunking\n...\n")


def test_L1_pass(env):
    make_L1(env)
    assert run(env, "L1") == 0


def test_L1_fails_arg_substitution_hazard(env, capsys):
    make_L1(env, skill_md="| Real Revenue | $0–250K |\n")
    assert run(env, "L1") == 1
    assert "$<số>" in capsys.readouterr().out


def test_L1_allows_multi_digit_dollar(env):
    make_L1(env, skill_md="Staffing $150K and $15/MTok\n")
    assert run(env, "L1") == 0


def test_L1_fails_bad_leverage_level(env, capsys):
    make_L1(env, level="L13")
    assert run(env, "L1") == 1
    assert "Small Plates" in capsys.readouterr().out


def test_L1_fails_no_chapters(env):
    make_L1(env)
    (env.skills / "demo" / "chapters" / "ch01-intro.md").unlink()
    assert run(env, "L1") == 1


def test_L1_fails_missing_learning_kit(env):
    make_L1(env)
    (env.books / "demo" / "Learning_Kit.md").unlink()
    assert run(env, "L1") == 1


# ---------- L2 ----------

def make_L2(env, statuses=(2, 2), chars=(80, 90)):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    w(src / "ch02.md", "y" * 100)
    items = [{"id": f"id{i}", "title": f"ch0{i + 1}.md", "type": "generated_text",
              "url": None, "status": s} for i, s in enumerate(statuses)]
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    cdir = env.tmp / "nlm" / "content"
    for i, c in enumerate(chars):
        w(cdir / f"id{i}.json", json.dumps({"content": "z" * c, "title": f"ch0{i + 1}.md",
                                           "source_type": "generated_text", "url": None,
                                           "char_count": c}))
    return ["--nlm-list", str(lst), "--nlm-content-dir", str(cdir)]


def test_L2_pass(env):
    assert run(env, "L2", *make_L2(env)) == 0


def test_L2_fails_without_nlm_list(env, capsys):
    make_L2(env)
    assert run(env, "L2") == 1
    assert "--nlm-list" in capsys.readouterr().out


def test_L2_fails_not_ready(env):
    assert run(env, "L2", *make_L2(env, statuses=(2, 1))) == 1


def test_L2_fails_bot_wall_short_content(env, capsys):
    assert run(env, "L2", *make_L2(env, chars=(80, 30))) == 1
    assert "ch02.md" in capsys.readouterr().out


def test_L2_fails_count_mismatch(env):
    extra = make_L2(env)
    w(env.books / "demo" / "_source" / "ch03.md", "q" * 100)
    assert run(env, "L2", *extra) == 1


def test_L2_fails_malformed_list_json(env, capsys):
    make_L2(env)
    lst = env.tmp / "nlm" / "list.json"
    lst.write_text("{broken json", encoding="utf-8")  # Truncated/invalid JSON
    argv = [str(env.learn), "L2",
            "--skills-root", str(env.skills),
            "--books-root", str(env.books),
            "--meta-dir", str(env.meta),
            "--nlm-list", str(lst),
            "--nlm-content-dir", str(env.tmp / "nlm" / "content")]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "JSON" in out or "không phải" in out
    # Verify no traceback leaked
    assert "Traceback" not in out


def test_L2_fails_malformed_content_json(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    w(src / "ch02.md", "y" * 100)
    items = [{"id": f"id{i}", "title": f"ch0{i + 1}.md", "type": "generated_text",
              "url": None, "status": 2} for i in range(2)]
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    cdir = env.tmp / "nlm" / "content"
    w(cdir / "id0.json", json.dumps({"content": "z" * 80, "char_count": 80}))
    w(cdir / "id1.json", "{broken json")  # Malformed second content file
    argv = [str(env.learn), "L2",
            "--skills-root", str(env.skills),
            "--books-root", str(env.books),
            "--meta-dir", str(env.meta),
            "--nlm-list", str(lst),
            "--nlm-content-dir", str(cdir)]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "id1" in out or "JSON" in out or "không phải" in out
    # Verify no traceback leaked
    assert "Traceback" not in out


def test_L2_fails_duplicate_titles(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    # Two sources with the same title (one ready, one not)
    items = [
        {"id": "id0", "title": "ch01.md", "type": "generated_text", "url": None, "status": 2},
        {"id": "id1", "title": "ch01.md", "type": "generated_text", "url": None, "status": 1},
    ]
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    cdir = env.tmp / "nlm" / "content"
    w(cdir / "id0.json", json.dumps({"content": "z" * 80, "char_count": 80}))
    argv = [str(env.learn), "L2",
            "--skills-root", str(env.skills),
            "--books-root", str(env.books),
            "--meta-dir", str(env.meta),
            "--nlm-list", str(lst),
            "--nlm-content-dir", str(cdir)]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "ch01.md" in out and ("trùng" in out or "nhiều" in out or "duplicate" in out.lower())
