"""pytest cho linter plugin ip-invent."""
import importlib.util
import sys
from pathlib import Path

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


def test_gate_doc_table_has_all_three_verdicts_and_ceo_ownership():
    assert lint.lint_gate_doc(_ref("co-mat-gate.md")) == []


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
    # Vòng 2: đỏ vì lệch nguyên văn hàng 2 (Chưa rõ) cột Xử so với canon,
    # không phải vì trúng nhãn "Chưa rõ" trong thông điệp lỗi.
    assert any("hàng 2" in e and "cột Xử" in e for e in errors), errors


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
    # Vòng 2: đỏ vì lệch nguyên văn hàng 3 (Không thuộc) cột Xử so với canon,
    # không phải vì trúng nhãn "Không thuộc" trong thông điệp lỗi.
    assert any("hàng 3" in e and "cột Xử" in e for e in errors), errors


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
    assert any("3 hàng" in e for e in errors), errors


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
    # dung". Vòng 2: không còn cue-detection, đỏ vì lệch nguyên văn hàng 1
    # cột Xử so với GATE_TABLE_CANON.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung",
        "**KHÔNG DỪNG.** Cứ xử nội dung",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bí mật nhà nước bị phủ định DỪNG ngay trong ô"
    assert any("hàng 1" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_unknown_row_exception_clause_inside_the_cell():
    # M2 (review vòng 1) — cả hai token bắt buộc ("coi như thuộc", "DỪNG")
    # vẫn còn nguyên chuỗi, nhưng bị gắn mệnh đề ngoại lệ ngay trong ô khiến
    # nghĩa đảo ngược hoàn toàn. Vòng 2: đỏ vì lệch nguyên văn hàng 2 cột Xử.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**coi như thuộc** → **DỪNG.**",
        "**coi như thuộc** diện đã rà; **DỪNG** là không cần thiết → chạy tiếp.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng Chưa rõ bị gắn ngoại lệ 'là không cần thiết' ngay trong ô"
    assert any("hàng 2" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_secret_row_trailing_exception_clause():
    # M10 (review vòng 1) — DỪNG vẫn đứng đầu ô, nhưng một mệnh đề "Trừ khi…
    # thì chạy tiếp." nối vào cuối ô làm DỪNG hết hiệu lực trong thực tế.
    # Vòng 2: đỏ vì lệch nguyên văn hàng 1 cột Xử (thừa một câu).
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "sang `workspace-knstack.md`). |",
        "sang `workspace-knstack.md`). Trừ khi CEO thấy gấp thì chạy tiếp. |",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt mệnh đề ngoại lệ nối cuối ô hàng bí mật nhà nước"
    assert any("hàng 1" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_secret_row_extra_bold_markers_around_negation():
    # N7 (review vòng 2) — chỉ thêm 2 dấu `*` so với M1: "**KHÔNG** **DỪNG.**
    # Cứ xử nội dung". _has_effective (đã xoá) từng lọt ca này vì token "DỪNG"
    # còn nguyên bất kể markdown bao quanh. So khớp nguyên văn không quan tâm
    # markdown — chỉ cần khác canon là đỏ.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung",
        "**KHÔNG** **DỪNG.** Cứ xử nội dung",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bí mật nhà nước bị phủ định kiểu tách dấu **"
    assert any("hàng 1" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_secret_row_softened_into_a_recommendation():
    # N1 (review vòng 2) — nới lỏng mệnh lệnh DỪNG thành khuyến nghị không
    # bắt buộc. Không có cue phủ định kiểu "không X" nào ở đây — chỉ so khớp
    # nguyên văn mới bắt được, vì nội dung khác canon dù không mang từ cấm.
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "**DỪNG.** Không xử nội dung, không tóm tắt, không diễn giải.",
        "**Khuyến nghị DỪNG** (không bắt buộc). Không xử nội dung, không tóm tắt, không diễn giải.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt DỪNG bị nới lỏng thành khuyến nghị không bắt buộc"
    assert any("hàng 1" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_secret_row_with_diacritics_stripped():
    # N9 (review vòng 2) — bỏ dấu tiếng Việt. Không mang cue tiếng Việt có
    # dấu nào, và nghĩa bề mặt gần như giữ nguyên — nhưng so khớp nguyên văn
    # không quan tâm nghĩa, chỉ hỏi "có khác canon không".
    original = _ref("co-mat-gate.md")
    mutated = original.replace(
        "Không xử nội dung, không tóm tắt, không diễn giải.",
        "Khong xu noi dung, khong tom tat, khong dien giai.",
        1,
    )
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt hàng bị viết lại không dấu"
    assert any("hàng 1" in e and "cột Xử" in e for e in errors), errors


def test_gate_lint_flags_table_wrapped_in_tilde_fence():
    # N11 (review vòng 2) — cùng ý M11 nhưng dùng fence dấu ngã (~~~) thay vì
    # backtick. _FENCE_RE dùng backreference \1 nên phải khớp cả hai kiểu.
    original = _ref("co-mat-gate.md")
    lines = original.splitlines()
    start, end = _gate_table_line_bounds(lines)
    fenced = ["~~~"] + lines[start:end + 1] + ["~~~"]
    mutated_lines = lines[:start] + fenced + lines[end + 1:]
    mutated = "\n".join(mutated_lines)
    assert mutated != original, "đột biến không khớp được văn bản thật"
    errors = lint.lint_gate_doc(mutated)
    assert errors, "lint phải bắt bảng thật bị bọc trong fence ~~~"
    assert any("3 hàng" in e for e in errors), errors


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
    assert any("3 hàng" in e for e in errors), errors


def test_gate_lint_flags_activation_region_with_inserted_exception_line():
    # N13 (review vòng 2) — giữ NGUYÊN 2 dòng kích hoạt gốc, CHÈN THÊM một
    # dòng "ngoại lệ vận hành". So khớp toàn vùng: bằng nghĩa là bằng, thừa
    # một câu cũng đỏ — không cần hiểu nội dung câu chèn thêm nói gì.
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
    assert any("kích hoạt" in e.lower() for e in errors), errors


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
    assert any("3 hàng" in e for e in errors), errors


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
    assert any("3 hàng" in e for e in errors), errors


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
    assert any("kích hoạt" in e.lower() or "không chạy" in e.lower() for e in errors), errors


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
