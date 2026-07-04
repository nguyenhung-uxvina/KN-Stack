"""Parse leo-mode-templates.md (leo-assist = source of truth) → dict mode → template.

KHÔNG copy nội dung template vào đây. Format file đổi → TemplateFormatError (fail loudly).
"""
import re
from pathlib import Path

# .../KN-Stack/mcp/leo-bridge/leo_bridge/templates.py → parents[3] = KN-Stack
TEMPLATES_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills" / "helix" / "leo-assist" / "references" / "leo-mode-templates.md"
)
EXPECTED_MODES = ["A", "B", "C", "D", "E1", "E2", "E3", "F"]
HEADING_RE = re.compile(r"^#{2,3}\s+([A-F]\d?)[.\s]", re.MULTILINE)
BLOCK_RE = re.compile(r"```\n(.*?)```", re.DOTALL)


class TemplateFormatError(Exception):
    pass


def load_templates(path=TEMPLATES_PATH) -> dict:
    p = Path(path)
    if not p.exists():
        raise TemplateFormatError(f"Không thấy template leo-assist tại {p}")
    text = p.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    matches = list(HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = BLOCK_RE.search(text[m.start():end])
        if block:
            out[m.group(1)] = block.group(1).rstrip()
    missing = [x for x in EXPECTED_MODES if x not in out]
    if missing:
        raise TemplateFormatError(
            f"leo-mode-templates.md thiếu template mode {missing} — "
            "format đã đổi, cập nhật leo_bridge/templates.py parser."
        )
    return out
