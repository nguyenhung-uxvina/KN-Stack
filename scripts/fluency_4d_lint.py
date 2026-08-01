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


_PROFILE_BLOCK_RE = re.compile(
    r"^##\s+([a-z]{3}\.[a-z]+)\s*$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_FIELD_RE = {
    "tin_hieu": re.compile(r"\*\*Tín hiệu:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
    "co_do": re.compile(r"\*\*Cờ đỏ:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
    "vi_du": re.compile(r"\*\*Ví dụ ngành:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
}


def parse_profile(text: str) -> dict[str, dict[str, str]]:
    """Trả về {mã ô: {tin_hieu, co_do, vi_du}} từ một file profile."""
    out: dict[str, dict[str, str]] = {}
    for cell, body in _PROFILE_BLOCK_RE.findall(text):
        fields = {}
        for key, rx in _FIELD_RE.items():
            m = rx.search(body)
            fields[key] = m.group(1).strip() if m else ""
        out[cell] = fields
    return out


def lint_profile(text: str) -> list[str]:
    """Kiểm một file profile khớp rubric. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    blocks = parse_profile(text)
    for cell in CELLS:
        if cell not in blocks:
            errors.append(f"profile thiếu khối cho ô: {cell}")
            continue
        for key, label in (("tin_hieu", "Tín hiệu"), ("co_do", "Cờ đỏ"), ("vi_du", "Ví dụ ngành")):
            if not blocks[cell][key].strip():
                errors.append(f"profile ô {cell} thiếu trường: {label}")
    for cell in blocks:
        if cell not in CELLS:
            errors.append(f"profile có ô lạ: {cell}")

    # Profile không được định nghĩa lại thang điểm.
    # Flag "thang điểm" nếu nó trong heading (^#+ .*thang điểm) hoặc file chứa "0-3" hoặc "0–3"
    if re.search(r"^#+\s+.*thang\s+điểm", text, re.IGNORECASE | re.MULTILINE):
        errors.append("profile không được định nghĩa lại thang điểm")
    if "0-3" in text or "0–3" in text:
        errors.append("profile không được định nghĩa lại thang điểm (tìm thấy '0-3' hoặc '0–3')")

    return errors
