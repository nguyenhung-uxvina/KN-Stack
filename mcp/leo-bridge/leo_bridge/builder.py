"""Sinh prompt Leo theo mode A–F — ép 5 nguyên tắc leo-assist, từ chối prompt mơ hồ."""
from . import templates as _templates

REQUIRED_FIELDS = {
    "A": ["FUNCTION", "ENVELOPE", "SPEC", "SOURCE"],
    "B": ["QUESTION", "CONTEXT"],
    "C": ["GOAL", "KNOWNS", "UNKNOWN"],
    "D": ["SUBJECT", "PROCESS", "STANDARDS"],
    "E1": ["IDEA", "KNOWNS"],
    "E2": ["DOCTYPE", "SOURCE", "STRUCTURE", "FIELDS"],
    "E3": ["PART"],
    "F": ["PART", "REQUIREMENTS", "PROCESS"],
}


class BuildError(Exception):
    pass


def build_prompt(mode, params, classification="THƯỜNG", assumptions=None, tpl_map=None):
    mode = (mode or "").upper()
    if mode not in REQUIRED_FIELDS:
        raise BuildError(f"Mode không hợp lệ: '{mode}'. Hợp lệ: {sorted(REQUIRED_FIELDS)}")
    missing = [f for f in REQUIRED_FIELDS[mode] if not str(params.get(f, "")).strip()]
    if missing:
        raise BuildError(
            f"Mode {mode} thiếu tham số bắt buộc: {missing}. "
            "KHÔNG sinh prompt mơ hồ — cấp giá trị ĐỊNH LƯỢNG (tải+đơn vị, kích thước interface thật)."
        )
    tpl = (tpl_map or _templates.load_templates())[mode]
    upper_params = {k.upper(): v for k, v in params.items()}
    lines = []
    for line in tpl.splitlines():
        stripped = line.strip()
        if stripped.startswith("[Phân loại"):
            lines.append(f"[Phân loại: {classification}]")
            continue
        if stripped.startswith("[GIẢ ĐỊNH]"):
            items = assumptions or ["(chưa khai báo — CEO bổ sung trước khi gửi)"]
            lines.append("[GIẢ ĐỊNH] " + " · ".join(items))
            continue
        filled = next(
            (f"[{fld}] {val}" for fld, val in upper_params.items()
             if stripped.startswith(f"[{fld}]")),
            None,
        )
        lines.append(filled if filled is not None else line)
    return "\n".join(lines)
