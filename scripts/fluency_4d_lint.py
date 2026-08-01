"""Linter giữ bốn file tham chiếu của plugin fluency-4d khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown để Cowork nạp được).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "fluency-4d"
REF_DIR = PLUGIN_ROOT / "skills" / "_shared" / "references"

CELLS = [
    "del.problem", "del.platform", "del.task",
    "des.product", "des.process", "des.performance",
    "dis.product", "dis.process", "dis.performance",
    "dil.creation", "dil.transparency", "dil.deployment",
]
MODES = {"automation", "augmentation", "agency"}

# Mã ô trong rubric nằm ở cột đầu của bảng, bọc backtick: | `del.problem` | ...
_RUBRIC_CELL_RE = re.compile(r"^\|\s*`([a-z]{3}\.[a-z]+)`\s*\|", re.MULTILINE)

# Chuỗi cấm trong rubric-core.md — rubric phải trung lập ngành.
_RUBRIC_FORBIDDEN = ["Workshop X", "Pahl-Beitz", "analyst-trap", "ratio-check", "BQP", "MẬT"]


def parse_rubric_cells(text: str) -> list[str]:
    """Trả về danh sách mã ô rubric khai báo, theo đúng thứ tự xuất hiện."""
    return _RUBRIC_CELL_RE.findall(text)


def lint_rubric(text: str) -> list[str]:
    """Kiểm rubric-core.md. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    found = parse_rubric_cells(text)
    if found != CELLS:
        missing = [c for c in CELLS if c not in found]
        extra = [c for c in found if c not in CELLS]
        if missing:
            errors.append(f"rubric thiếu ô: {missing}")
        if extra:
            errors.append(f"rubric có ô lạ: {extra}")
        if not missing and not extra:
            errors.append(f"rubric sai thứ tự ô: {found}")
    for bad in _RUBRIC_FORBIDDEN:
        if bad in text:
            errors.append(f"rubric-core.md phải trung lập ngành, tìm thấy: {bad!r}")
    return errors
