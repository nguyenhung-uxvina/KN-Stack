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


@pytest.mark.parametrize("line", ["- Định giá pilot: (B)", "- (A)", "- Phương án: B"])
def test_L0_fails_label_only_decision(env, capsys, line):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "- Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận", line))
    assert run(env, "L0") == 1
    assert "bằng chữ" in capsys.readouterr().out
