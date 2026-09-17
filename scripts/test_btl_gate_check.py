"""pytest cho btl_gate_check.py — cổng máy của /book-to-learn.

Mỗi cổng có ít nhất một ca ĐẠT và các ca TRƯỢT tương ứng với lỗi đã gặp thật
(nhãn quyết định (A)/(B) bị ghi sai, $0 bị thay thành tham số, nguồn NLM status=2
nhưng là trang chặn bot, câu trả lời Feynman do AI điền...).
"""
import importlib.util
import json
import os
import subprocess
import sys
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


# ---------- C1: cp1252 stdout on Windows (Git Bash pipe) ----------

def _run_cli_cp1252(env, *extra):
    """Chạy CLI thật (subprocess, không import) với PYTHONIOENCODING=cp1252
    và PYTHONUTF8 KHÔNG đặt — mô phỏng đúng host bị lỗi thật."""
    script = HERE / "btl_gate_check.py"
    child_env = dict(os.environ)
    child_env["PYTHONIOENCODING"] = "cp1252"
    child_env.pop("PYTHONUTF8", None)
    argv = [sys.executable, str(script), str(env.learn), *extra,
            "--skills-root", str(env.skills), "--books-root", str(env.books),
            "--meta-dir", str(env.meta)]
    return subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", env=child_env)


def test_cli_cp1252_stdout_failing_l0_no_crash(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "van_de_that: Định giá pilot VN-TGT-F khi biên gộp ở mức 10 bộ gần bằng 0", "van_de_that:"))
    proc = _run_cli_cp1252(env, "L0")
    assert proc.returncode == 1
    assert "FAIL" in proc.stdout
    assert "Traceback" not in proc.stderr


def test_cli_cp1252_stdout_missing_state_exits_2(env):
    (env.learn / "_pipeline_state.md").unlink()
    proc = _run_cli_cp1252(env, "L0")
    assert proc.returncode == 2
    assert "Traceback" not in proc.stderr


# ---------- I2: tệp không phải UTF-8 (UnicodeDecodeError) ----------

def test_state_file_non_utf8_exits_2(env, capsys):
    (env.learn / "_pipeline_state.md").write_bytes(b"---\nslug: demo\n---\n\xff\xfe kh\xf4ng UTF-8")
    assert run(env, "L0") == 2
    assert "UTF-8" in capsys.readouterr().out


def test_L0_non_utf8_project_brief_fails_not_crashes(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)  # valid first, then corrupt bytes
    (env.learn / "_Project_Brief.md").write_bytes(b"---\nvan_de_that: x\n---\n\xff\xfe kh\xf4ng UTF-8")
    assert run(env, "L0") == 1
    out = capsys.readouterr().out
    assert "UTF-8" in out
    assert "Traceback" not in out


# ---------- M12: LEARN-dir quá nông để suy vault bằng parents[1] ----------

def test_shallow_learn_dir_exits_2_asks_for_vault(env, capsys):
    argv = ["D:/LEARN-shallow-test-btl", "L0",
            "--skills-root", str(env.skills), "--books-root", str(env.books), "--meta-dir", str(env.meta)]
    assert gc.main(argv) == 2
    assert "--vault" in capsys.readouterr().out


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


# ---------- I2: list.json/content json có hình dạng sai (không phải mảng/object) ----------

def test_L2_fails_list_json_is_null(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    lst = w(env.tmp / "nlm" / "list.json", "null")
    argv = [str(env.learn), "L2", "--skills-root", str(env.skills), "--books-root", str(env.books),
            "--meta-dir", str(env.meta), "--nlm-list", str(lst),
            "--nlm-content-dir", str(env.tmp / "nlm" / "content")]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "mảng" in out
    assert "Traceback" not in out


def test_L2_fails_list_json_elements_not_objects(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    lst = w(env.tmp / "nlm" / "list.json", json.dumps([1]))
    argv = [str(env.learn), "L2", "--skills-root", str(env.skills), "--books-root", str(env.books),
            "--meta-dir", str(env.meta), "--nlm-list", str(lst),
            "--nlm-content-dir", str(env.tmp / "nlm" / "content")]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "không phải object" in out
    assert "Traceback" not in out


def test_L2_fails_item_without_id(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    items = [{"title": "ch01.md", "type": "generated_text", "url": None, "status": 2}]  # no "id"
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    argv = [str(env.learn), "L2", "--skills-root", str(env.skills), "--books-root", str(env.books),
            "--meta-dir", str(env.meta), "--nlm-list", str(lst),
            "--nlm-content-dir", str(env.tmp / "nlm" / "content")]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "'id'" in out or "thiếu" in out
    assert "Traceback" not in out


def test_L2_fails_content_json_is_list(env, capsys):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    items = [{"id": "id0", "title": "ch01.md", "type": "generated_text", "url": None, "status": 2}]
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    cdir = env.tmp / "nlm" / "content"
    w(cdir / "id0.json", json.dumps([]))
    argv = [str(env.learn), "L2", "--skills-root", str(env.skills), "--books-root", str(env.books),
            "--meta-dir", str(env.meta), "--nlm-list", str(lst), "--nlm-content-dir", str(cdir)]
    assert gc.main(argv) == 1
    out = capsys.readouterr().out
    assert "object JSON" in out
    assert "Traceback" not in out


# ---------- L3 ----------

CEO_APPROVAL = "CEO đã xem và đồng ý danh sách nguồn trước khi nạp lên notebook btl-demo-mo-rong."


def make_claims(env, row="| 1 | Trích lợi nhuận trước khi chi | SUPPORTED | Michalowicz 2014 | tr.19 |",
                 ceo_approval=CEO_APPROVAL):
    section = f"\n## CEO duyệt nguồn\n{ceo_approval}\n" if ceo_approval is not None else ""
    w(env.books / "demo" / "Claims.md", f"""
        | # | Luận điểm | Nhãn | Nguồn | Vị trí |
        |---|---|---|---|---|
        {row}
        """ + section)


def test_L3_pass(env):
    make_claims(env)
    assert run(env, "L3") == 0


@pytest.mark.parametrize("row", [
    "| 1 | X | TRUE | Nguồn A | tr.3 |",
    "| 1 | X | SUPPORTED | Nguồn A | ✅ |",
    "| 1 | X | CONTESTED |  | tr.3 |",
    "| 1 | X | CẦN-CHUYỂN-VN | Nguồn A | — |",
])
def test_L3_fails_bad_row(env, row):
    make_claims(env, row)
    assert run(env, "L3") == 1


# ---------- L3: I8(a) mục "## CEO duyệt nguồn" bắt buộc có nội dung ----------

def test_L3_fails_missing_ceo_duyet_section(env, capsys):
    make_claims(env, ceo_approval=None)
    assert run(env, "L3") == 1
    assert "CEO duyệt nguồn" in capsys.readouterr().out


def test_L3_fails_ceo_duyet_section_only_html_comment(env, capsys):
    # Đúng như khuôn templates/claims.md để trống: chỉ có HTML comment hướng
    # dẫn CEO — chưa phải CEO thật sự ghi bằng lời.
    make_claims(env, ceo_approval="<!-- CEO ghi bằng lời đã xem và đồng ý danh sách nguồn -->")
    assert run(env, "L3") == 1
    assert "CEO duyệt nguồn" in capsys.readouterr().out


def test_L3_pass_with_ceo_duyet_section_after_comment(env):
    make_claims(env, ceo_approval="<!-- hướng dẫn -->\nCEO đã xem và đồng ý danh sách nguồn.")
    assert run(env, "L3") == 0


def test_L3_blank_template_still_fails(env):
    """templates/claims.md để trống (không dòng luận điểm nào) vẫn phải trượt."""
    tpl = HERE.parent / "skills" / "book" / "book-to-learn" / "references" / "templates" / "claims.md"
    w(env.books / "demo" / "Claims.md", tpl.read_text(encoding="utf-8"))
    assert run(env, "L3") == 1


# ---------- L4 ----------

ANSWER = " ".join(["từ"] * 45)


def make_feynman(env, tac_gia="CEO", answer=ANSWER, level="3", name="Small Plates"):
    w(env.learn / "learn" / f"feynman-{gc.slugify(name)}.md", f"""
        ---
        framework: {name}
        tac_gia: {tac_gia}
        ---
        ## Q1 — Hiểu
        > Giải thích Small Plates trong 60 giây cho một người không học kế toán.
        {answer}
        ## Q2 — Áp dụng
        > Áp vào VN-TGT-F thì tài khoản nào mở trước?
        {ANSWER}
        ## Q3 — Tầng hệ thống
        > Nó cắt vòng lặp nào, điểm nghẽn nào?
        {ANSWER}
        ## Rubric tự chấm
        | Chỉ báo hành vi | Mức |
        |---|---|
        | Tự tính được tỉ lệ phân bổ từ số thật | {level} |
        """)


def test_L4_pass(env):
    make_feynman(env)
    assert run(env, "L4") == 0


def test_L4_fails_missing_file(env, capsys):
    assert run(env, "L4") == 1
    assert "feynman-small-plates.md" in capsys.readouterr().out


def test_L4_fails_ai_author(env):
    make_feynman(env, tac_gia="AI")
    assert run(env, "L4") == 1


def test_L4_fails_short_answer(env, capsys):
    make_feynman(env, answer="ngắn quá")
    assert run(env, "L4") == 1
    assert "Q1" in capsys.readouterr().out


def test_L4_fails_rubric_level(env):
    make_feynman(env, level="7")
    assert run(env, "L4") == 1


def test_L4_fails_without_candidates(env):
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: []\n---\n")
    assert run(env, "L4") == 1


# ---------- M9: framework_ung_vien ghi dạng danh sách nhiều dòng ----------

def test_L4_fails_multiline_list_hints_inline_form(env, capsys):
    w(env.learn / "_pipeline_state.md",
      "---\nslug: demo\nframework_ung_vien:\n- Small Plates\n- RIFA\n---\n")
    assert run(env, "L4") == 1
    out = capsys.readouterr().out
    assert "[a, b]" in out and "inline" in out


def test_L4_fails_truly_empty_candidates_keeps_original_message(env, capsys):
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: []\n---\n")
    assert run(env, "L4") == 1
    assert "đang rỗng" in capsys.readouterr().out


def test_L4_fails_missing_framework_key(env, capsys):
    w(env.learn / "learn" / "feynman-small-plates.md", f"""
        ---
        tac_gia: CEO
        ---
        ## Q1 — Hiểu
        > Question
        {ANSWER}
        ## Q2 — Áp dụng
        > Question
        {ANSWER}
        ## Q3 — Tầng hệ thống
        > Question
        {ANSWER}
        ## Rubric tự chấm
        | Chỉ báo | Mức |
        |---|---|
        | Test | 3 |
        """)
    assert run(env, "L4") == 1
    assert "framework" in capsys.readouterr().out


def test_L4_fails_wrong_framework_name(env, capsys):
    make_feynman(env, name="Small Plates")
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: [Different Framework]\n---\n")
    assert run(env, "L4") == 1
    assert "L4" in capsys.readouterr().out


def test_L4_pass_case_insensitive_framework_match(env):
    make_feynman(env, name="Small Plates")
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: [small plates]\n---\n")
    assert run(env, "L4") == 0


# ---------- Regression tests: previously uncovered --------

def test_L3_fails_header_only_claims_table(env):
    w(env.books / "demo" / "Claims.md", """
        | # | Luận điểm | Nhãn | Nguồn | Vị trí |
        |---|---|---|---|---|
        """)
    assert run(env, "L3") == 1


def test_L4_fails_feynman_no_q_headings(env, capsys):
    w(env.learn / "learn" / "feynman-small-plates.md", f"""
        ---
        framework: Small Plates
        tac_gia: CEO
        ---
        This file has no Q headings at all.
        {ANSWER}
        """)
    assert run(env, "L4") == 1
    assert "Q1" in capsys.readouterr().out


def test_L4_fails_rubric_fractional_level(env):
    make_feynman(env, level="4/5")
    assert run(env, "L4") == 1


# ---------- L5 ----------

GOOD_CARD = """
    ---
    framework: Small Plates
    gia_thuyet: Trích 5% mỗi khoản thu pilot không làm chậm chi trả nhà cung cấp
    chi_so: Số ngày trễ hạn thanh toán nhà cung cấp
    baseline: 0
    nguong: ≤ 2 ngày trễ trong 16 ngày chạy
    nguoi_chiu_trach_nhiem: CEO
    ngay_bat_dau: 2026-09-20
    ngay_ket_thuc: 2026-10-06
    du_doan: Không trễ ngày nào
    don_vi_framework: công ty
    don_vi_thi_nghiem: công ty
    muc_tin_cay_du_lieu: L3 — số kế toán thật
    ceo_duyet: 2026-09-19
    ---
    """


def pass_gates(env, *phases):
    for ph in phases:
        env.learn.joinpath("_pipeline_state.md").write_text(
            state_text(env).rstrip("\n") + f"\n- {ph}: PASS 2026-09-18T09:00\n", encoding="utf-8")


def make_L5_ready(env):
    """L4/L3 đã có dấu PASS *và* thật sự vẫn qua nếu re-chạy (I3) —
    feynman + Claims.md hợp lệ đi kèm dấu PASS."""
    make_feynman(env)
    make_claims(env)
    pass_gates(env, "L3", "L4")


def test_L5_pass(env):
    make_L5_ready(env)
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 0


@pytest.mark.parametrize("old,new", [
    ("baseline: 0", "baseline: chưa đo"),
    ("ngay_ket_thuc: 2026-10-06", "ngay_ket_thuc: 2026-10-07"),
    ("don_vi_thi_nghiem: công ty", "don_vi_thi_nghiem: dòng sản phẩm"),
    ("ceo_duyet: 2026-09-19", "ceo_duyet:"),
    ("framework: Small Plates", "framework: RIFA"),
    ("muc_tin_cay_du_lieu: L3 — số kế toán thật", "muc_tin_cay_du_lieu: cao"),
    ("nguoi_chiu_trach_nhiem: CEO", "nguoi_chiu_trach_nhiem:"),
])
def test_L5_fails_bad_card(env, old, new):
    make_L5_ready(env)
    w(env.learn / "Experiment_Card.md", GOOD_CARD.replace(old, new))
    assert run(env, "L5") == 1


def test_L5_fails_without_feynman_gate(env, capsys):
    pass_gates(env, "L3")
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 1
    assert "L4" in capsys.readouterr().out


def test_L5_quick_skips_claims_but_not_feynman(env):
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: [Small Plates]\nquick: true\n---\n")
    make_feynman(env)
    pass_gates(env, "L4")
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 0


# ---------- I3: cổng L5 phải re-chạy L4/L3 thật, không chỉ tin dấu PASS cũ ----------

def test_L5_fails_when_L4_stamp_stale_after_new_framework(env, capsys):
    """L4 PASS thật (chỉ có Small Plates), rồi CEO thêm framework mới vào
    framework_ung_vien mà chưa có Feynman cho nó — dấu PASS cũ của L4 không
    còn phản ánh đúng thực tế, L5 phải bắt được và trượt."""
    make_L5_ready(env)
    assert "- L4: PASS " in state_text(env)  # L4 thật sự PASS trước khi bị làm cũ
    w(env.learn / "_pipeline_state.md",
      state_text(env).replace("framework_ung_vien: [Small Plates]",
                               "framework_ung_vien: [Small Plates, RIFA]"))
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 1
    out = capsys.readouterr().out
    assert "feynman-rifa.md" in out or "RIFA" in out
    assert "đã có dấu PASS nhưng nay lại trượt" in out


def test_L5_fails_when_L3_stamp_stale_after_claims_broken(env, capsys):
    """L3 PASS thật, rồi Claims.md bị xoá mục CEO duyệt nguồn (regressed) —
    dấu PASS L3 cũ không còn đúng, L5 phải bắt được."""
    make_L5_ready(env)
    make_claims(env, ceo_approval=None)  # ghi đè Claims.md, xoá mục CEO duyệt nguồn
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 1
    out = capsys.readouterr().out
    assert "đã có dấu PASS nhưng nay lại trượt" in out


# ---------- L7 ----------

GOOD_AAR = """
    ---
    quyet_dinh: adapt
    ---
    ## Định xảy ra gì
    Không trễ thanh toán.
    ## Thực tế ra sao
    Trễ 1 ngày vào kỳ 25.
    ## Vì sao khác
    Khoản thu lệch lịch 10/25.
    ## Lần sau làm gì
    Dời ngày phân bổ theo lịch thu thật.
    """


def cycle_row(**over):
    row = {"slug": "demo", "opened": "2026-09-17", "closed": "2026-10-17", "target": "VN-TGT-F",
           "dreyfus_before": 2, "dreyfus_after": 3, "leverage_reached": "L5", "perkins": "strategic",
           "applied": True, "decision": "adapt", "prediction_hits": 1, "prediction_total": 3,
           "days_to_competence": 11, "techniques": {"feynman": 5}, "illusion_gap": 0.25,
           "book_type": "text", "failure_points": [], "next_book_hint": "The Goal"}
    row.update(over)
    return row


def make_L7(env, row, aar=GOOD_AAR):
    w(env.learn / "AAR.md", aar)
    w(env.meta / "cycles.jsonl", json.dumps({"slug": "other"}) + "\n" + json.dumps(row, ensure_ascii=False) + "\n")


GOOD_RUN_LOG = """
    | Ngày | Quan sát | Số đo | Điểm nghẽn còn đó? |
    |---|---|---|---|
    | 2026-09-25 | Không trễ thanh toán | 0 ngày trễ | Không |
    """


def test_L7_pass(env):
    pass_gates(env, "L5")
    w(env.learn / "Run_Log.md", GOOD_RUN_LOG)
    make_L7(env, cycle_row())
    assert run(env, "L7") == 0


def test_L7_unapplied_cycle_can_close(env):
    make_L7(env, cycle_row(applied=False))
    assert run(env, "L7") == 0


# ---------- I8(b): applied=true đòi Run_Log.md có số đo ở cột 'Số đo' ----------

def test_L7_fails_applied_missing_run_log(env, capsys):
    pass_gates(env, "L5")
    make_L7(env, cycle_row())  # applied=True mặc định, không tạo Run_Log.md
    assert run(env, "L7") == 1
    assert "Run_Log" in capsys.readouterr().out


def test_L7_fails_applied_run_log_no_so_do_column(env, capsys):
    pass_gates(env, "L5")
    w(env.learn / "Run_Log.md", "| Ngày | Quan sát |\n|---|---|\n| 2026-09-25 | ok |\n")
    make_L7(env, cycle_row())
    assert run(env, "L7") == 1
    assert "Số đo" in capsys.readouterr().out


def test_L7_fails_applied_run_log_so_do_cells_empty(env, capsys):
    pass_gates(env, "L5")
    w(env.learn / "Run_Log.md",
      "| Ngày | Quan sát | Số đo | Điểm nghẽn còn đó? |\n|---|---|---|---|\n"
      "| 2026-09-25 | ok | — | Không |\n")
    make_L7(env, cycle_row())
    assert run(env, "L7") == 1
    assert "Số đo" in capsys.readouterr().out


def test_L7_fails_applied_without_L5(env, capsys):
    make_L7(env, cycle_row(applied=True))
    assert run(env, "L7") == 1
    assert "applied" in capsys.readouterr().out


@pytest.mark.parametrize("over", [
    {"decision": "maybe"}, {"dreyfus_after": "3"}, {"applied": "yes"},
    {"days_to_competence": True}, {"perkins": "genius"}, {"leverage_reached": "L0"},
])
def test_L7_fails_bad_cycle_row(env, over):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(**over))
    assert run(env, "L7") == 1


def test_L7_fails_missing_row(env):
    pass_gates(env, "L5")
    w(env.learn / "AAR.md", GOOD_AAR)
    w(env.meta / "cycles.jsonl", json.dumps({"slug": "other"}) + "\n")
    assert run(env, "L7") == 1


def test_L7_fails_bad_aar(env):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(), aar=GOOD_AAR.replace("quyet_dinh: adapt", "quyet_dinh: có lẽ"))
    assert run(env, "L7") == 1


def test_L7_fails_empty_aar_section(env):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(), aar=GOOD_AAR.replace("Khoản thu lệch lịch 10/25.", ""))
    assert run(env, "L7") == 1


# ---------- I2: dòng cycles.jsonl là JSON hợp lệ nhưng không phải object ----------

def test_L7_fails_cycle_row_not_object(env, capsys):
    pass_gates(env, "L5")
    w(env.learn / "AAR.md", GOOD_AAR)
    w(env.meta / "cycles.jsonl", json.dumps([1]) + "\n")
    assert run(env, "L7") == 1
    out = capsys.readouterr().out
    assert "không phải object" in out
    assert "Traceback" not in out


def test_L7_fails_corrupt_last_cycle_line(env, capsys):
    """Corrupt last line after valid row must FAIL, not silently use old row."""
    pass_gates(env, "L5")
    w(env.learn / "AAR.md", GOOD_AAR)
    # Valid old row + corrupt last line
    w(env.meta / "cycles.jsonl", 
      json.dumps({"slug": "other"}) + "\n" +
      json.dumps(cycle_row(), ensure_ascii=False) + "\n" +
      "{broken json\n")
    assert run(env, "L7") == 1
    out = capsys.readouterr().out
    assert "JSON" in out or "hợp lệ" in out


def test_L5_framework_case_insensitive(env):
    """Framework matching should ignore case differences."""
    make_L5_ready(env)
    w(env.learn / "Experiment_Card.md", GOOD_CARD.replace("framework: Small Plates", "framework: small plates"))
    assert run(env, "L5") == 0
