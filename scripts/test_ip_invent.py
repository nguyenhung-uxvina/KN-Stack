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
