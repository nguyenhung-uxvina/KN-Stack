"""Parse leo-mode-templates.md (leo-assist = source of truth) → dict mode → template.

KHÔNG copy nội dung template vào đây. Format file đổi → TemplateFormatError (fail loudly).
"""
import os
import re
from pathlib import Path

# templates.py lives at <root>/mcp/leo-bridge/leo_bridge/templates.py.
# <root> differs by layout: canonical KN-Stack has skills/helix/leo-assist/,
# the flattened leo-ai plugin has skills/leo-assist/. Resolve both; env wins.
_ROOT = Path(__file__).resolve().parents[3]
_CANDIDATES = [
    _ROOT / "skills" / "leo-assist" / "references" / "leo-mode-templates.md",         # flattened plugin
    _ROOT / "skills" / "helix" / "leo-assist" / "references" / "leo-mode-templates.md",  # canonical KN-Stack
]
_ENV_PATH = os.environ.get("LEO_TEMPLATES_PATH")
TEMPLATES_PATH = Path(_ENV_PATH) if _ENV_PATH else next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[-1])

# Recipe (multi-mode orchestration) lives in leo-phase-templates.md, not mode-templates.
_RECIPE_CANDIDATES = [
    _ROOT / "skills" / "leo-assist" / "references" / "leo-phase-templates.md",         # flattened plugin
    _ROOT / "skills" / "helix" / "leo-assist" / "references" / "leo-phase-templates.md",  # canonical KN-Stack
]
_ENV_RECIPE_PATH = os.environ.get("LEO_PHASE_TEMPLATES_PATH")
RECIPES_PATH = Path(_ENV_RECIPE_PATH) if _ENV_RECIPE_PATH else next(
    (p for p in _RECIPE_CANDIDATES if p.exists()), _RECIPE_CANDIDATES[-1])

EXPECTED_MODES = ["A", "B", "B-HF", "C", "D", "E1", "E2", "E3", "F"]
# Capture A–F, letter+digit (E1/E2/E3), and the B-HF human-factors sub-mode.
HEADING_RE = re.compile(r"^#{2,3}\s+([A-F](?:-HF|\d)?)[.\s]", re.MULTILINE)
RECIPE_HEADING_RE = re.compile(r"^#{2,3}\s+RECIPE\b.*?leo-part-brief", re.MULTILINE | re.IGNORECASE)
# Bounds every section (including the last mode section) — any heading of any
# kind ends the previous section, not just the next MODE heading. Without this,
# a mode section with a missing fence could silently absorb the fenced block of
# a later non-mode section (e.g. F absorbing "## Router meta-prompt").
ANY_HEADING_RE = re.compile(r"^#{2,3}\s", re.MULTILINE)
BLOCK_RE = re.compile(r"```\n(.*?)```", re.DOTALL)


class TemplateFormatError(Exception):
    pass


def load_templates(path=TEMPLATES_PATH) -> dict:
    p = Path(path)
    if not p.exists():
        raise TemplateFormatError(f"Không thấy template leo-assist tại {p}")
    text = p.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    all_heading_starts = [m.start() for m in ANY_HEADING_RE.finditer(text)]
    matches = list(HEADING_RE.finditer(text))
    for m in matches:
        end = next((s for s in all_heading_starts if s > m.start()), len(text))
        block = BLOCK_RE.search(text[m.start():end])
        if block:
            out[m.group(1)] = block.group(1).rstrip()
    missing = [x for x in EXPECTED_MODES if x not in out]
    if missing:
        raise TemplateFormatError(
            f"leo-mode-templates.md thiếu template mode {missing} — "
            "format đã đổi, cập nhật leo_bridge/templates.py parser."
        )
    unexpected = [k for k in out if k not in EXPECTED_MODES]
    if unexpected:
        raise TemplateFormatError(
            f"leo-mode-templates.md có key không mong đợi {unexpected} — "
            "format đã đổi (VD: heading intro '## E.' vô tình có fence), "
            "cập nhật leo_bridge/templates.py parser hoặc bỏ fence thừa."
        )
    return out


def load_recipe(name: str = "leo-part-brief", path=RECIPES_PATH) -> str:
    """Đọc scaffold recipe đa-mode (vd leo-part-brief) từ leo-phase-templates.md.
    Recipe = orchestration nhiều mode, KHÔNG phải template 1 mode. Fail loudly nếu đổi format."""
    p = Path(path)
    if not p.exists():
        raise TemplateFormatError(f"Không thấy phase-templates tại {p}")
    text = p.read_text(encoding="utf-8")
    m = RECIPE_HEADING_RE.search(text)
    if not m:
        raise TemplateFormatError(
            f"Không thấy heading RECIPE '{name}' trong {p.name} — "
            "format đã đổi, cập nhật RECIPE_HEADING_RE."
        )
    block = BLOCK_RE.search(text[m.start():])
    if not block:
        raise TemplateFormatError(
            f"RECIPE '{name}' thiếu fenced block (```) ngay sau heading — cập nhật parser."
        )
    return block.group(1).rstrip()
