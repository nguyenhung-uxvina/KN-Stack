"""pytest cho linter plugin ip-invent."""
import importlib.util
import sys
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "ip_invent_lint", Path(__file__).with_name("ip_invent_lint.py")
)
lint = importlib.util.module_from_spec(_spec)
sys.modules["ip_invent_lint"] = lint
_spec.loader.exec_module(lint)


def test_shared_dir_carries_plugin_prefix():
    # ~/.claude/commands/ là namespace phẳng dùng chung mọi plugin.
    assert lint.SHARED_DIR_NAME == "ip-shared"


def test_workspace_fields_are_the_canonical_seven():
    assert lint.WORKSPACE_FIELDS == [
        "surface", "root", "output_pattern",
        "scan_sources", "triz_refs", "patent_search", "nlm_notebook",
    ]


def test_parse_active_workspace_reads_the_code_block():
    text = "# Workspace đang bật\n\nblah\n\n```\nworkspace-knstack.md\n```\n\nblah\n"
    assert lint.parse_active_workspace(text) == "workspace-knstack.md"


def test_parse_active_workspace_returns_none_when_absent():
    assert lint.parse_active_workspace("# Không có khối mã nào\n") is None


def _ref(name: str) -> str:
    return (lint.REF_DIR / name).read_text(encoding="utf-8")


def _skill(name: str) -> str:
    return (lint.SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")


def test_active_workspace_points_at_an_existing_profile():
    target = lint.parse_active_workspace(_ref("active-workspace.md"))
    assert target is not None, "active-workspace.md không có khối mã nêu profile"
    assert (lint.REF_DIR / target).is_file(), f"trỏ tới profile không tồn tại: {target}"


def test_knstack_profile_is_local_and_complete():
    text = _ref("workspace-knstack.md")
    assert lint.lint_workspace_profile(text) == []
    assert lint.parse_workspace_profile(text)["surface"] == "local"


def test_cowork_profile_is_cloud_and_declares_none_for_vault_only_tools():
    text = _ref("workspace-cowork.md")
    assert lint.lint_workspace_profile(text) == []
    fields = lint.parse_workspace_profile(text)
    assert fields["surface"] == "cloud"
    # Cowork không có vault, không có skill KN-Stack, không có NLM.
    for f in ("scan_sources", "triz_refs", "patent_search", "nlm_notebook"):
        assert fields[f] == "none", f"{f} phải là none trong profile Cowork"


def test_template_profile_is_complete_but_never_activated():
    text = _ref("workspace-template.md")
    # Template chỉ cần đủ + đúng thứ tự 7 trường; `surface` là chỗ trống ⟨CEO chốt: …⟩
    # nên không kiểm giá trị surface ở đây.
    assert list(lint.parse_workspace_profile(text).keys()) == lint.WORKSPACE_FIELDS
    assert lint.parse_active_workspace(_ref("active-workspace.md")) != "workspace-template.md"


def test_profile_lint_flags_a_missing_field():
    dirty = "| `surface` | `local` |\n| `root` | `X` |\n"
    assert any("thiếu trường" in e for e in lint.lint_workspace_profile(dirty))


def test_profile_lint_flags_bad_surface():
    rows = "\n".join(
        f"| `{f}` | `{'hybrid' if f == 'surface' else 'x'}` |" for f in lint.WORKSPACE_FIELDS
    )
    assert any("surface phải là local|cloud" in e for e in lint.lint_workspace_profile(rows))


def _valid_rows(overrides: dict[str, str] | None = None) -> dict[str, str]:
    base = {
        "surface": "local", "root": "X", "output_pattern": "Y",
        "scan_sources": "none", "triz_refs": "none",
        "patent_search": "none", "nlm_notebook": "none",
    }
    if overrides:
        base.update(overrides)
    return base


def test_profile_lint_flags_an_extra_field():
    fields = _valid_rows()
    lines = [f"| `{k}` | `{v}` |" for k, v in fields.items()]
    lines.append("| `extra_field` | `x` |")
    dirty = "\n".join(lines)
    assert any("trường lạ" in e for e in lint.lint_workspace_profile(dirty))


def test_profile_lint_flags_wrong_order():
    fields = _valid_rows()
    swapped = list(fields.items())
    swapped[0], swapped[1] = swapped[1], swapped[0]  # surface <-> root
    dirty = "\n".join(f"| `{k}` | `{v}` |" for k, v in swapped)
    assert any("sai thứ tự trường" in e for e in lint.lint_workspace_profile(dirty))


# ═══════════════════════════════════════════════════════════════════════════
# CỔNG co-mat-gate.md — đóng băng CẢ FILE bằng SHA-256 (vòng 4)
#
# Ba vòng trước canh BỀ MẶT CÚ PHÁP (fence, heading, hàng bảng) của hai vùng
# "có hiệu lực". Mỗi vòng lại bị phá bằng một khuôn cú pháp khác cho cùng hậu
# quả render. Vòng 4 bỏ hẳn ranh giới "vùng có hiệu lực / phần còn lại tự do"
# — chính ranh giới đó là bề mặt tấn công.
#
# HỆ QUẢ CHO TEST: mọi đột biến bên dưới — của cả bốn vòng — giờ đỏ vì CÙNG
# MỘT lý do (hash lệch) và cho CÙNG MỘT khuôn thông điệp. Cách DỰNG từng đột
# biến giữ nguyên không đổi một chữ: chúng là tài liệu sống về mô hình đe doạ,
# ghi lại từng đòn đã bị chặn. Chỉ assertion về HÌNH DẠNG thông điệp đổi, vì
# các chốt cú pháp sinh ra những thông điệp đó đã bị gỡ.
# ═══════════════════════════════════════════════════════════════════════════


def _assert_gate_drift(errors: list[str], *, region: str | None = None) -> None:
    """Khuôn chung: cổng phải trả ĐÚNG MỘT lỗi, và lỗi đó phải hành động được.

    Đòi hỏi ở đây KHÔNG yếu hơn assertion cũ: vẫn bắt buộc lint đỏ, cộng thêm
    ba yêu cầu mới mà các vòng trước không có — đúng một lỗi (không spam),
    nêu được dòng khác nhau đầu tiên, và nêu được cả hai đường xử.
    """
    assert len(errors) == 1, f"cổng phải trả ĐÚNG MỘT lỗi hành động được, thấy: {errors}"
    msg = errors[0]
    assert "co-mat-gate.md đã ĐỔI so với bản CEO đã duyệt" in msg, msg
    assert "GATE_DOC_SHA256" in msg, msg
    assert "Vùng trôi:" in msg, msg
    assert "Khác nhau đầu tiên ở dòng" in msg, msg
    assert "Mong đợi:" in msg and "Thấy:" in msg, msg
    assert "CÓ CHỦ ĐÍCH" in msg and "KHÔNG CHỦ ĐÍCH" in msg, msg
    assert "git checkout --" in msg, msg
    if region is not None:
        assert region in msg, msg


def test_gate_doc_table_has_all_three_verdicts_and_ceo_ownership():
    assert lint.lint_gate_doc(_ref("co-mat-gate.md")) == []


def test_gate_doc_sha256_constant_has_not_drifted_from_the_approved_file():
    # Chốt chống chép sai hằng: nếu GATE_DOC_SHA256 hoặc GATE_DOC_CANON được
    # gõ sai một ký tự thì test này đỏ ngay, chứ không âm thầm biến cổng thành
    # thứ luôn-đỏ (hoặc tệ hơn, luôn-xanh cho một bản tài liệu khác).
    raw = lint.GATE_DOC_PATH.read_bytes().decode("utf-8")  # GIỮ nguyên CRLF trên đĩa
    assert lint.gate_doc_digest(raw) == lint.GATE_DOC_SHA256
    # So sau chuẩn hoá ở CẢ HAI vế, đúng phép chuẩn hoá mà cổng dùng: `.py` cũng
    # nằm dưới `core.autocrlf`, nên khoá vào LF thô là tự chuốc lỗi liên nền tảng.
    assert lint._normalize_doc(lint.GATE_DOC_CANON) == lint._normalize_doc(raw)
    assert lint.lint_gate_doc(raw) == []


def test_gate_lint_normalizes_line_endings_and_bom():
    # Bẫy thật: repo chạy trên Windows với `core.autocrlf=true`, nên cùng một
    # nội dung có CRLF trên đĩa và LF trong git blob. Không chuẩn hoá thì hằng
    # số trôi theo checkout và cổng đỏ oan trên máy khác.
    lf = _ref("co-mat-gate.md")
    crlf = lf.replace("\n", "\r\n")
    assert crlf != lf, "file thật phải có ít nhất một dòng để phép kiểm này có nghĩa"
    assert lint.lint_gate_doc(lf) == []
    assert lint.lint_gate_doc(crlf) == lint.lint_gate_doc(lf) == []
    assert lint.lint_gate_doc("\ufeff" + lf) == []
    assert lint.lint_gate_doc("\ufeff" + crlf) == []
    assert lint.gate_doc_digest(crlf) == lint.gate_doc_digest(lf) == lint.GATE_DOC_SHA256


def test_gate_lint_flags_unknown_row_flipped_to_continue():
    # Đột biến 1: đảo nghĩa hàng "Chưa rõ" — thay 'coi như thuộc → DỪNG' bằng
    # 'coi như không thuộc → chạy tiếp', giữ nguyên phần còn lại của file.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**coi như thuộc** → **DỪNG.**",
        "**coi như không thuộc** → **chạy tiếp.**",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật — regex/chuỗi cần cập nhật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng Chưa rõ bị đảo nghĩa thành cho chạy tiếp"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 2")


def test_gate_lint_flags_not_applicable_row_flipped_to_stop():
    # Đột biến 2: hàng "Không thuộc" bị đổi cột Xử thành DỪNG — mọi ngả đều
    # dừng thì bảng vô nghĩa. Giữ nguyên phần còn lại của file.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "hoặc đã khóa priority date | Chạy tiếp. |",
        "hoặc đã khóa priority date | DỪNG. |",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật — regex/chuỗi cần cập nhật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng Không thuộc bị đổi thành DỪNG"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 3")


def test_gate_lint_flags_a_deleted_row():
    # Đột biến 3: xoá hẳn hàng "Chưa rõ" khỏi bảng (còn 2 hàng), giữ nguyên
    # phần còn lại của file.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines(keepends=True)
    mutated_lines = [l for l in lines if not l.lstrip().startswith("| **Chưa rõ**")]
    assert len(mutated_lines) == len(lines) - 1, "đột biến không tìm thấy đúng 1 hàng để xoá"
    mutated = "".join(mutated_lines)
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng bị thiếu hàng"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 2")


def _gate_table_line_bounds(lines: list[str]) -> tuple[int, int]:
    """Chỉ số dòng [start, end] (bao gồm cả hai đầu) của khối bảng 3 ngả thật
    trong co-mat-gate.md — dùng để dựng đột biến M7/M11 mà không phải chép
    tay lại toàn bộ khối bảng (rủi ro gõ sai từng gây lỗi ở vòng trước)."""
    start = next(i for i, l in enumerate(lines) if l.strip() == "| Phân loại | Xử |")
    end = start
    while end + 1 < len(lines) and lines[end + 1].startswith("|"):
        end += 1
    return start, end


def test_gate_lint_flags_secret_row_negated_inside_the_cell():
    # M1 (review vòng 1) — token DỪNG còn nguyên nhưng bị phủ định ngay
    # trong ô: "**DỪNG.** Không xử nội dung" -> "**KHÔNG DỪNG.** Cứ xử nội
    # dung".
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung",
        "**KHÔNG DỪNG.** Cứ xử nội dung",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bí mật nhà nước bị phủ định DỪNG ngay trong ô"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 1")


def test_gate_lint_flags_unknown_row_exception_clause_inside_the_cell():
    # M2 (review vòng 1) — cả hai token bắt buộc ("coi như thuộc", "DỪNG")
    # vẫn còn nguyên chuỗi, nhưng bị gắn mệnh đề ngoại lệ ngay trong ô khiến
    # nghĩa đảo ngược hoàn toàn.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**coi như thuộc** → **DỪNG.**",
        "**coi như thuộc** diện đã rà; **DỪNG** là không cần thiết → chạy tiếp.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng Chưa rõ bị gắn ngoại lệ 'là không cần thiết' ngay trong ô"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 2")


def test_gate_lint_flags_secret_row_trailing_exception_clause():
    # M10 (review vòng 1) — DỪNG vẫn đứng đầu ô, nhưng một mệnh đề "Trừ khi…
    # thì chạy tiếp." nối vào cuối ô làm DỪNG hết hiệu lực trong thực tế.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "sang `workspace-knstack.md`). |",
        "sang `workspace-knstack.md`). Trừ khi CEO thấy gấp thì chạy tiếp. |",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt mệnh đề ngoại lệ nối cuối ô hàng bí mật nhà nước"
    _assert_gate_drift(errors)


def test_gate_lint_flags_secret_row_extra_bold_markers_around_negation():
    # N7 (review vòng 2) — chỉ thêm 2 dấu `*` so với M1: "**KHÔNG** **DỪNG.**
    # Cứ xử nội dung". Phép kiểm "token DỪNG còn không" của vòng 1 lọt ca này.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung",
        "**KHÔNG** **DỪNG.** Cứ xử nội dung",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bí mật nhà nước bị phủ định kiểu tách dấu **"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 1")


def test_gate_lint_flags_secret_row_softened_into_a_recommendation():
    # N1 (review vòng 2) — nới lỏng mệnh lệnh DỪNG thành khuyến nghị không
    # bắt buộc. Không có cue phủ định kiểu "không X" nào ở đây.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung, không tóm tắt, không diễn giải.",
        "**Khuyến nghị DỪNG** (không bắt buộc). Không xử nội dung, không tóm tắt, không diễn giải.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt DỪNG bị nới lỏng thành khuyến nghị không bắt buộc"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 1")


def test_gate_lint_flags_secret_row_with_diacritics_stripped():
    # N9 (review vòng 2) — bỏ dấu tiếng Việt. Nghĩa bề mặt gần như giữ
    # nguyên, nhưng hash không quan tâm nghĩa, chỉ hỏi "có khác không".
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "Không xử nội dung, không tóm tắt, không diễn giải.",
        "Khong xu noi dung, khong tom tat, khong dien giai.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bị viết lại không dấu"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 1")


def test_gate_lint_flags_table_wrapped_in_tilde_fence():
    # N11 (review vòng 2) — bảng thật bị bọc trong fence dấu ngã (~~~) nên
    # không còn render ra bảng.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    fenced = ["~~~"] + lines[start:end + 1] + ["~~~"]
    mutated_lines = lines[:start] + fenced + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị bọc trong fence ~~~"
    _assert_gate_drift(errors)


def test_gate_lint_flags_table_wrapped_in_indented_code_block():
    # N12 (review vòng 2) — thụt 4 dấu cách biến bảng thật thành indented
    # code block theo CommonMark, không còn render ra bảng.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    indented = ["    " + ln for ln in lines[start:end + 1]]
    mutated_lines = lines[:start] + indented + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị thụt lề thành indented code block"
    _assert_gate_drift(errors)


def test_gate_lint_flags_activation_region_with_inserted_exception_line():
    # N13 (review vòng 2) — giữ NGUYÊN 2 dòng kích hoạt gốc, CHÈN THÊM một
    # dòng "ngoại lệ vận hành". Thừa một câu cũng là tài liệu đã đổi.
    original = _ref("co-mat-gate.md")
    activation_block = (
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.\n"
        "> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ."
    )
    mutated = original.replace(
        activation_block,
        activation_block
        + "\n> Ngoại lệ vận hành: ở `surface: cloud` cổng này KHÔNG chạy nếu CEO đang gấp.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt vùng kích hoạt bị chèn thêm dòng ngoại lệ"
    _assert_gate_drift(errors)


def test_gate_lint_flags_unclosed_backtick_fence_before_table():
    # X14 (review vòng 3) — mở ``` KHÔNG ĐÓNG ngay trước bảng thật; renderer
    # thật nuốt toàn bộ phần còn lại của file thành code.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    mutated_lines = lines[:start] + ["```"] + lines[start:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt fence ``` không đóng trước bảng"
    _assert_gate_drift(errors)


def test_gate_lint_flags_unclosed_tilde_fence_before_table():
    # X18 (review vòng 3) — cùng cơ chế X14 nhưng dùng ~~~ không đóng.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    mutated_lines = lines[:start] + ["~~~"] + lines[start:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt fence ~~~ không đóng trước bảng"
    _assert_gate_drift(errors)


def test_gate_lint_flags_table_wrapped_in_html_comment():
    # X16 (review vòng 3) — bọc bảng thật trong `<!-- … -->` CÂN ĐỦ CẶP. Bảng
    # vô hình khi render dù lint kiểu "có chứa" vẫn thấy 3 hàng khớp canon.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    wrapped = ["<!--"] + lines[start:end + 1] + ["-->"]
    mutated_lines = lines[:start] + wrapped + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị bọc trong HTML comment"
    _assert_gate_drift(errors)


def test_gate_lint_flags_a_second_step0_prime_section():
    # X6 (review vòng 3) — hai mục `## Bước 0′`: mục đầu giữ bảng canon, mục
    # sau mang bảng nới lỏng "dùng khi gấp" mà lint neo-mục-đầu-tiên không soát.
    original = _ref("co-mat-gate.md")
    duplicate_section = (
        "## Bước 0′ — dùng khi gấp\n\n"
        "| Phân loại | Xử |\n"
        "|---|---|\n"
        "| Thuộc bí mật nhà nước | Chạy tiếp nếu gấp |\n"
        "| Chưa rõ | Chạy tiếp nếu gấp |\n"
        "| Không thuộc | Chạy tiếp |\n\n"
    )
    mutated = original.replace(
        "## Ghi và in lại",
        duplicate_section + "## Ghi và in lại",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt tài liệu có 2 mục '## Bước 0′'"
    _assert_gate_drift(errors)


def test_gate_lint_flags_a_sibling_step0_double_prime_section():
    # X7 (review vòng 3) — thêm mục `## Bước 0″ — ghi đè Bước 0′` (dấu prime
    # ĐÔI) mang bảng đảo nghĩa hoàn toàn, nằm ngoài mục được neo.
    original = _ref("co-mat-gate.md")
    override_section = (
        "## Bước 0″ — ghi đè Bước 0′\n\n"
        "| Phân loại | Xử |\n"
        "|---|---|\n"
        "| Thuộc bí mật nhà nước | Chạy tiếp |\n"
        "| Chưa rõ | Chạy tiếp |\n"
        "| Không thuộc | Chạy tiếp |\n\n"
    )
    mutated = original.replace(
        "## Ghi và in lại",
        override_section + "## Ghi và in lại",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt mục '## Bước 0″' ghi đè Bước 0′ thật"
    _assert_gate_drift(errors)


def test_gate_lint_flags_table_replaced_with_loose_bullets_plus_fenced_decoy():
    # M7 (review vòng 1) — bảng thật bị thay bằng danh sách gạch đầu dòng
    # nới lỏng, rồi một bảng 3 hàng "ví dụ" được dán trong code fence ở cuối
    # file để lừa một phép quét "2 cột bất kỳ trong cả file".
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    bullets = [
        "- Thuộc bí mật nhà nước: chạy tiếp.",
        "- Chưa rõ: chạy tiếp.",
        "- Không thuộc: chạy tiếp.",
    ]
    decoy_fence = [
        "",
        "```",
        "| Phân loại | Xử |",
        "|---|---|",
        "| Thuộc bí mật nhà nước | DỪNG |",
        "| Chưa rõ | coi như thuộc → DỪNG |",
        "| Không thuộc | Chạy tiếp |",
        "```",
    ]
    mutated_lines = lines[:start] + bullets + lines[end + 1:] + decoy_fence
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị thay bằng danh sách + bảng ví dụ trong fence"
    _assert_gate_drift(errors, region="bảng Bước 0′ hàng 1")


def test_gate_lint_flags_real_table_wrapped_in_code_fence():
    # M11 (review vòng 1) — bảng thật nguyên vẹn nhưng bị bọc vào code fence
    # nên Markdown không còn render ra bảng nữa; thủ tục thật vô hiệu.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    fenced = ["```"] + lines[start:end + 1] + ["```"]
    mutated_lines = lines[:start] + fenced + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị bọc trong code fence"
    _assert_gate_drift(errors)


def test_gate_lint_flags_activation_surfaces_swapped():
    # M16 (review vòng 1) — đảo `surface: cloud` <-> `surface: local` giữa
    # hai dòng kích hoạt/tắt: bảng 3 ngả vẫn hoàn hảo nhưng cổng chỉ chạy ở
    # bề mặt an toàn (local) và im lặng đúng ở bề mặt nguy hiểm (cloud).
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.\n"
        "> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.",
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: local`.\n"
        "> Ở `surface: cloud` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt điều kiện kích hoạt bị đảo surface"
    _assert_gate_drift(errors, region="khối kích hoạt")


# ── Đòn vòng 3 để lọt: Y1/Y2/Y4/Y6/Y7/Y8 ───────────────────────────────────
# Sáu đòn này đều lọt qua chốt cú pháp của vòng 3, và mỗi đòn chỉ cần MỘT ký
# tự hoặc một khuôn markdown khác để né đúng một cái neo. Chúng là lý do trực
# tiếp để bỏ ranh giới "vùng có hiệu lực" và đóng băng cả file.


def test_gate_lint_flags_indented_unclosed_fence_before_table():
    # Y1 — fence hở THỤT MỘT DẤU CÁCH. `_unclosed_markup_errors` của vòng 3
    # neo `^(?:```|~~~)` (MULTILINE) nên một dấu cách ở đầu dòng là đủ để nó
    # không đếm được, trong khi CommonMark vẫn mở fence với thụt lề ≤3 cách.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, _end = _gate_table_line_bounds(lines)
    mutated_lines = lines[:start] + [" ```"] + lines[start:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt fence hở thụt một dấu cách trước bảng"
    _assert_gate_drift(errors)


_INVERTED_TABLE = (
    "| Phân loại | Xử |\n"
    "|---|---|\n"
    "| Thuộc bí mật nhà nước | Chạy tiếp |\n"
    "| Chưa rõ | coi như KHÔNG thuộc → Chạy tiếp |\n"
    "| Không thuộc | Chạy tiếp |\n"
)


def test_gate_lint_flags_h3_step0_override_section():
    # Y2 — heading `### Bước 0″` (BA dấu #) mang bảng đảo nghĩa, dán ở CUỐI
    # file. Chốt vòng 3 đếm `^##[ \t]*Bước 0` nên chỉ thấy heading đúng HAI dấu
    # `#`; và mục này nằm sau mục `##` cuối cùng nên cũng ngoài vùng bảng được
    # soát. Người đọc thì vẫn thấy một mục "Bước 0" thứ hai ghi đè thủ tục thật.
    # (Xác nhận: bản lint vòng 3 trả [] cho đúng đột biến này.)
    original = _ref("co-mat-gate.md")
    mutated = original + "\n### Bước 0″ — ghi đè Bước 0′ khi gấp\n\n" + _INVERTED_TABLE
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt mục '### Bước 0″' ghi đè Bước 0′"
    _assert_gate_drift(errors)


def test_gate_lint_flags_setext_step0_override_section():
    # Y4 — heading SETEXT (`Bước 0″` rồi một dòng `====`), dán ở cuối file.
    # Render ra heading thật nhưng không có ký tự `#` nào, nên MỌI chốt đếm
    # heading kiểu ATX của vòng 3 đều mù hoàn toàn.
    # (Xác nhận: bản lint vòng 3 trả [] cho đúng đột biến này.)
    original = _ref("co-mat-gate.md")
    mutated = (
        original
        + "\nBước 0″ — thủ tục rút gọn\n=========================\n\n"
        + _INVERTED_TABLE
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt heading setext 'Bước 0″' mang bảng đảo nghĩa"
    _assert_gate_drift(errors)


def test_gate_lint_flags_decoy_h1_carrying_canon_while_real_activation_is_swapped():
    # Y6 — H1 MỒI đặt ở ĐẦU FILE mang đúng nguyên văn khối kích hoạt canon rồi
    # đóng lại bằng một heading `##`, còn khối kích hoạt THẬT (dưới H1 thật) bị
    # đảo `cloud` ⇄ `local`. Vòng 3 cắt vùng kích hoạt bằng "giữa H1 ĐẦU TIÊN
    # và heading `##` đầu tiên", nên nó đọc trúng bản mồi, thấy khớp canon và
    # im lặng — cổng thật đã đảo chiều: chạy ở `local` (an toàn), tắt ở `cloud`
    # (nguy hiểm). (Xác nhận: bản lint vòng 3 trả [] cho đúng đột biến này.)
    original = _ref("co-mat-gate.md")
    swapped = original.replace(
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.\n"
        "> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.",
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: local`.\n"
        "> Ở `surface: cloud` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.",
        1,
    )
    assert swapped != original, "đột biến không khớp được văn bản thật"
    decoy_h1 = (
        "# Ghi chú biên tập (không phải thủ tục)\n\n"
        "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.\n"
        "> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.\n\n"
        "## Hết ghi chú\n\n"
    )
    mutated = decoy_h1 + swapped
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt H1 mồi mang canon che khối kích hoạt thật bị đảo"
    _assert_gate_drift(errors)


def test_gate_lint_flags_a_fourth_table_row_with_three_cells():
    # Y7 — hàng bảng THỨ TƯ có BA ô. Parser vòng 3 bỏ qua mọi dòng `len(cells)
    # != 2`, nên hàng này vô hình với lint; GFM thì vẫn render nó thành một
    # hàng thật (ô thừa bị cắt), thêm một ngả "gấp thì chạy tiếp" vào thủ tục.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    _start, end = _gate_table_line_bounds(lines)
    extra_row = "| **Gấp** — CEO yêu cầu nhanh | Chạy tiếp. | ghi chú nội bộ |"
    mutated_lines = lines[:end + 1] + [extra_row] + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bảng thứ tư có 3 ô"
    _assert_gate_drift(errors)


def test_gate_lint_flags_a_fourth_table_row_without_edge_pipes():
    # Y8 — hàng bảng thứ tư THIẾU pipe đầu/cuối. Parser vòng 3 đòi dòng vừa
    # startswith("|") vừa endswith("|") nên bỏ qua; GFM vẫn render thành hàng.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    _start, end = _gate_table_line_bounds(lines)
    extra_row = "**Gấp** — CEO yêu cầu nhanh | Chạy tiếp."
    mutated_lines = lines[:end + 1] + [extra_row] + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bảng thiếu pipe đầu/cuối"
    _assert_gate_drift(errors)


# ── Y9/Y10/Y11: ba báo động giả của vòng 3 đã hết ──────────────────────────
# Ba ca này KHÔNG viết dưới dạng "sửa file rồi kỳ vọng xanh" — thiết kế vòng 4
# bắt MỌI sửa đổi đều đỏ, nên một test như thế sẽ vừa sai ý nghĩa vừa mâu
# thuẫn với chính cổng. Chúng khẳng định đúng điều thật sự cần: CƠ CHẾ GÂY ĐỎ
# GIẢ đã bị gỡ, và tài liệu bị sửa nay đỏ vì "đã đổi so với bản duyệt" chứ
# không phải vì một cáo buộc cú pháp bịa ra. Test chết nếu ai đó dựng lại chốt
# cú pháp cũ.


def test_no_unbalanced_html_comment_alarm_from_a_prose_arrow():
    # Y9 — vòng 3 đếm `<!--` so với `-->` trên TOÀN văn bản, nên một mũi tên
    # `-->` trong văn xuôi (không phải comment) đủ để lint đỏ với lý do BỊA:
    # "HTML comment không cân". Bộ đếm đó đã bị gỡ cùng cả tầng canh cú pháp.
    assert not hasattr(lint, "_unclosed_markup_errors"), (
        "chốt cú pháp _unclosed_markup_errors đã bị dựng lại — nó là nguồn của báo "
        "động giả Y9/Y11 và thừa hẳn khi cả file đã đóng băng bằng hash"
    )
    assert not hasattr(lint, "_HTML_COMMENT_RE"), "_HTML_COMMENT_RE đã bị dựng lại"

    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "## Ghi và in lại",
        "Ghi nhớ đường đi: Chưa rõ --> coi như thuộc --> DỪNG.\n\n## Ghi và in lại",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    _assert_gate_drift(errors)
    assert not any("comment" in e.lower() for e in errors), (
        f"lint vẫn cáo buộc HTML comment lệch cặp vì một mũi tên trong văn xuôi: {errors}"
    )


def test_no_duplicate_step0_alarm_from_a_fenced_example():
    # Y10 — vòng 3 đếm heading `## Bước 0` trên TOÀN văn bản, kể cả bên trong
    # một code fence ĐÃ ĐÓNG, nên một ví dụ minh hoạ trong fence bị buộc tội
    # "2 mục Bước 0" dù nó không render thành heading nào.
    assert not hasattr(lint, "_STEP0_HEADING_RE"), (
        "chốt đếm heading _STEP0_HEADING_RE đã bị dựng lại — nó là nguồn của báo "
        "động giả Y10 và thừa hẳn khi cả file đã đóng băng bằng hash"
    )
    assert not hasattr(lint, "_STEP0_SECTION_RE"), "_STEP0_SECTION_RE đã bị dựng lại"
    assert not hasattr(lint, "parse_gate_table_rows"), (
        "parse_gate_table_rows đã bị dựng lại — parser bảng chỉ tồn tại để phục vụ "
        "tầng canh cú pháp đã gỡ"
    )

    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "## Ghi và in lại",
        "Ví dụ trình bày (chỉ minh hoạ):\n\n"
        "```markdown\n## Bước 0′ — chạy TRƯỚC khi đụng nội dung\n```\n\n## Ghi và in lại",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    _assert_gate_drift(errors)
    assert not any("mục" in e and "Bước 0" in e and "thấy 2" in e for e in errors), (
        f"lint vẫn cáo buộc trùng mục Bước 0 vì một ví dụ trong fence đã đóng: {errors}"
    )


def test_no_unclosed_fence_alarm_from_a_four_backtick_wrapper():
    # Y11 — fence 4-backtick bọc fence 3-backtick là cú pháp CommonMark hợp lệ
    # để trình bày code fence lồng nhau. Vòng 3 khớp cặp bằng backreference
    # `\1` trên đúng ba ký tự nên đếm sót và kêu "fence không đóng đủ cặp".
    assert not hasattr(lint, "_FENCE_RE"), (
        "chốt cú pháp _FENCE_RE đã bị dựng lại — nó là nguồn của báo động giả Y11"
    )
    assert not hasattr(lint, "_strip_code_fences"), "_strip_code_fences đã bị dựng lại"

    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "## Ghi và in lại",
        "Cách trình bày một khối mã trong tài liệu:\n\n"
        "````markdown\n```\nví dụ khối mã\n```\n````\n\n## Ghi và in lại",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    _assert_gate_drift(errors)
    assert not any("fence" in e.lower() for e in errors), (
        f"lint vẫn cáo buộc fence không đóng vì wrapper 4-backtick hợp lệ: {errors}"
    )


def test_profile_lint_flags_a_duplicate_row_even_when_dict_would_hide_it():
    # Bằng chứng lỗi gốc: 7 hàng đúng + 1 hàng `surface` dư dán ở cuối, giá trị
    # dư vẫn hợp lệ (`cloud`). Trước khi vá, dict comprehension nuốt hàng dư
    # (khoá sau đè khoá trước) và lint_workspace_profile trả về [] — im lặng
    # hoàn toàn dù sai khung bảng "bảy hàng" mà workspace-template.md hứa.
    fields = _valid_rows()
    lines = [f"| `{k}` | `{v}` |" for k, v in fields.items()]
    lines.append("| `surface` | `cloud` |")
    dirty = "\n".join(lines)
    errors = lint.lint_workspace_profile(dirty)
    assert any("hàng trùng" in e for e in errors), errors
    assert errors != []


# ═══════════════════════════════════════════════════════════════════════════
# KHỐI "⛔ BƯỚC 0′" TRONG 6 SKILL.MD — ĐÓNG BĂNG NGUYÊN VĂN (không kiểm cụm từ)
#
# Task 3 (cổng co-mat-gate.md) đi con đường "kiểm có-mặt-cụm-từ" trước và thua
# ba vòng liên tiếp trước phủ định, đưa vùng ra ngoài tầm soát, và một ký tự
# lệch. Task 4 áp thẳng kết luận đó cho khối "Bước 0′": lint không hỏi "các cụm
# bắt buộc có mặt không", nó hỏi "khối này có xuất hiện ĐÚNG MỘT LẦN, NGUYÊN VĂN
# byte-identical với STEP0_BLOCK_CANON hay không". Không có khái niệm "cụm bắt
# buộc" nào ở đây nữa — SKILL_REQUIRED_PHRASES/lint_skill_header của brief gốc
# bị bỏ có chủ đích (xem docstring lint_skill_block trong ip_invent_lint.py).
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.parametrize("name", [
    "ip-invent", "ip-criteria", "ip-harvest", "ip-screen", "ip-claim", "ip-dossier",
])
def test_every_skill_carries_the_stop_latch_block_verbatim(name):
    assert lint.lint_skill_block(_skill(name)) == []


def test_the_six_stop_latch_blocks_are_byte_identical_to_each_other_and_to_canon():
    texts = {name: _skill(name) for name in lint.SKILL_NAMES}
    assert lint.lint_blocks_identical(texts) == []


def test_step0_block_canon_actually_occurs_in_all_six_files():
    # Chốt hằng-không-lệch: nếu STEP0_BLOCK_CANON bị chép sai một ký tự khi
    # dựng hằng, test này đỏ ngay — tách khỏi test lint ở trên để thông điệp
    # lỗi nói rõ đây là lỗi CHÉP HẰNG, không phải lỗi của skill nào.
    for name in lint.SKILL_NAMES:
        norm = lint._normalize_doc(_skill(name))
        assert norm.count(lint.STEP0_BLOCK_CANON) == 1, (
            f"STEP0_BLOCK_CANON không xuất hiện đúng 1 lần trong {name}/SKILL.md — "
            "hằng trong ip_invent_lint.py có thể đã chép sai."
        )


@pytest.mark.parametrize("name", [
    "ip-invent", "ip-criteria", "ip-harvest", "ip-screen", "ip-claim", "ip-dossier",
])
def test_every_cited_shared_reference_actually_exists(name):
    for ref in lint.cited_refs(_skill(name)):
        assert (lint.REF_DIR / ref).is_file(), f"{name} trỏ tới file không tồn tại: {ref}"


def test_cited_refs_finds_relative_shared_paths():
    text = "đọc `../ip-shared/references/active-workspace.md` rồi `../ip-shared/references/co-mat-gate.md`"
    assert lint.cited_refs(text) == ["active-workspace.md", "co-mat-gate.md"]


def test_stop_latch_block_lint_normalizes_crlf_and_bom():
    # Bẫy thật (đã vấp ở Task 3): repo Windows core.autocrlf=true, cùng nội dung
    # có CRLF trên đĩa và LF trong git blob. Không chuẩn hoá thì lint trôi theo
    # checkout.
    lf = _skill("ip-invent")
    crlf = lf.replace("\n", "\r\n")
    assert crlf != lf, "file thật phải có ít nhất một dòng để phép kiểm này có nghĩa"
    assert lint.lint_skill_block(lf) == []
    assert lint.lint_skill_block(crlf) == lint.lint_skill_block(lf) == []
    assert lint.lint_skill_block("﻿" + lf) == []
    assert lint.lint_skill_block("﻿" + crlf) == []


def _delete_block(text: str) -> str:
    return text.replace(lint.STEP0_BLOCK_CANON, "", 1)


def _mutate_block(text: str, old: str, new: str) -> str:
    mutated_block = lint.STEP0_BLOCK_CANON.replace(old, new, 1)
    assert mutated_block != lint.STEP0_BLOCK_CANON, f"đột biến không khớp: {old!r} không có trong canon"
    return text.replace(lint.STEP0_BLOCK_CANON, mutated_block, 1)


def _duplicate_block(text: str) -> str:
    return text.replace(
        lint.STEP0_BLOCK_CANON,
        lint.STEP0_BLOCK_CANON + "\n\n" + lint.STEP0_BLOCK_CANON,
        1,
    )


def test_mutation_block_deleted_entirely_is_flagged():
    original = _skill("ip-criteria")
    mutated = _delete_block(original)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_skill_block(mutated)
    assert errors, "lint phải bắt khối Bước 0′ bị xoá hẳn"
    assert any("thiếu khối Bước 0′" in e for e in errors), errors

    texts = {name: _skill(name) for name in lint.SKILL_NAMES}
    texts["ip-criteria"] = mutated
    id_errors = lint.lint_blocks_identical(texts)
    assert any("ip-criteria" in e for e in id_errors), id_errors


def test_mutation_one_word_changed_in_one_file_is_flagged_by_both_checks():
    # 5 file kia GIỮ NGUYÊN — chỉ ip-harvest bị đổi.
    original = _skill("ip-harvest")
    mutated = _mutate_block(original, "profile đó.", "profile do.")
    assert mutated != original, "đột biến không khớp được văn bản thật"

    errors = lint.lint_skill_block(mutated)
    assert errors, "lint_skill_block phải bắt một chữ bị đổi trong khối"

    texts = {name: _skill(name) for name in lint.SKILL_NAMES}
    texts["ip-harvest"] = mutated
    id_errors = lint.lint_blocks_identical(texts)
    assert any("ip-harvest" in e for e in id_errors), id_errors
    # 5 skill còn lại không được bị nêu tên — chúng vẫn nguyên vẹn.
    for other in ("ip-invent", "ip-criteria", "ip-screen", "ip-claim", "ip-dossier"):
        assert not any(e.startswith(f"{other}:") for e in id_errors), id_errors


def test_mutation_block_inserted_twice_in_one_file_is_flagged():
    original = _skill("ip-screen")
    mutated = _duplicate_block(original)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_skill_block(mutated)
    assert errors, "lint phải bắt khối Bước 0′ bị chèn 2 lần"
    assert any("2 lần" in e for e in errors), errors


def test_mutation_stop_latch_softened_into_a_default_fallback_is_flagged():
    original = _skill("ip-claim")
    mutated = _mutate_block(
        original,
        "**Đọc không được thì DỪNG**",
        "Đọc không được thì dùng giá trị mặc định",
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_skill_block(mutated)
    assert errors, "lint phải bắt chốt DỪNG bị nới lỏng thành 'dùng giá trị mặc định'"


def test_mutation_one_extra_space_inside_the_block_is_flagged():
    # Chứng minh so sánh là BYTE-LEVEL, không phải "gần giống": chỉ thêm 1 dấu
    # cách vào giữa khối, không đổi từ nào.
    original = _skill("ip-dossier")
    mutated = _mutate_block(original, "không chạy gì.", "không chạy  gì.")
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_skill_block(mutated)
    assert errors, "lint phải bắt một dấu cách thừa chèn giữa khối"
