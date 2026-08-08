"""Linter giữ tầng tham chiếu dùng chung của plugin ip-invent khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown + JSON để Cowork nạp được).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "ip-invent"
SKILLS_ROOT = PLUGIN_ROOT / "skills"

# Tên thư mục tham chiếu dùng chung. Phải mang tiền tố plugin: nó được junction
# THẲNG vào ~/.claude/commands/ — một namespace phẳng dùng chung cho mọi plugin.
# Tên chung như "_shared" sẽ bị plugin nạp sau va vào và setup.sh bỏ qua im lặng.
SHARED_DIR_NAME = "ip-shared"
REF_DIR = SKILLS_ROOT / SHARED_DIR_NAME / "references"

SKILL_NAMES = [
    "ip-invent", "ip-criteria", "ip-harvest",
    "ip-screen", "ip-claim", "ip-dossier",
]

WORKSPACE_FIELDS = [
    "surface", "root", "output_pattern",
    "scan_sources", "triz_refs", "patent_search", "nlm_notebook",
]

VALID_SURFACES = {"local", "cloud"}

_CODE_BLOCK_RE = re.compile(r"^```\s*$\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
_PROFILE_ROW_RE = re.compile(r"^\|\s*`([a-z_]+)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)


def parse_active_workspace(text: str) -> str | None:
    """Tên file profile nêu trong khối mã đầu tiên của active-workspace.md."""
    m = _CODE_BLOCK_RE.search(text)
    if not m:
        return None
    name = m.group(1).strip()
    return name or None


def parse_workspace_rows(text: str) -> list[tuple[str, str]]:
    """Từng hàng thô `| `trường` | giá trị |` theo đúng thứ tự xuất hiện, GIỮ hàng trùng.

    Dùng cho lint — `parse_workspace_profile` gom về dict nên nuốt mất hàng
    trùng (khoá sau đè khoá trước); hàm này giữ nguyên để lint chấm được cả
    hàng trùng, hàng thừa, sai thứ tự.
    """
    return [(k, v.strip("` ")) for k, v in _PROFILE_ROW_RE.findall(text)]


def parse_workspace_profile(text: str) -> dict[str, str]:
    """Bảng `| `trường` | giá trị |` của một file workspace-*.md → dict."""
    return dict(parse_workspace_rows(text))


def lint_workspace_profile(text: str) -> list[str]:
    """Kiểm một file workspace-*.md. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    rows = parse_workspace_rows(text)
    found = [k for k, _ in rows]

    seen: set[str] = set()
    duplicates: list[str] = []
    for f in found:
        if f in seen and f not in duplicates:
            duplicates.append(f)
        seen.add(f)
    if duplicates:
        errors.append(f"profile có hàng trùng: {duplicates}")

    if found != WORKSPACE_FIELDS:
        unique_found = list(dict.fromkeys(found))
        missing = [f for f in WORKSPACE_FIELDS if f not in found]
        extra = [f for f in unique_found if f not in WORKSPACE_FIELDS]
        if missing:
            errors.append(f"profile thiếu trường: {missing}")
        if extra:
            errors.append(f"profile có trường lạ: {extra}")
        if not missing and not extra and not duplicates:
            errors.append(f"profile sai thứ tự trường: {found}")

    surface = dict(rows).get("surface")
    if surface is not None and surface not in VALID_SURFACES:
        errors.append(f"surface phải là local|cloud, thấy: {surface!r}")
    return errors
