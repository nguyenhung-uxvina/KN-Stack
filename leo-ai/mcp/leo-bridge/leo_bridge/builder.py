"""Sinh prompt Leo theo mode A–F — ép 5 nguyên tắc leo-assist, từ chối prompt mơ hồ."""
from . import templates as _templates

REQUIRED_FIELDS = {
    "A": ["FUNCTION", "ENVELOPE", "SPEC", "SOURCE"],
    "B": ["QUESTION", "CONTEXT"],
    "B-HF": ["BODY PART", "POPULATION", "POSTURE"],
    "C": ["GOAL", "KNOWNS", "UNKNOWN"],
    "D": ["SUBJECT", "PROCESS", "STANDARDS"],
    "E1": ["IDEA", "KNOWNS"],
    "E2": ["DOCTYPE", "SOURCE", "STRUCTURE", "FIELDS"],
    "E3": ["PART"],
    "F": ["PART", "REQUIREMENTS", "PROCESS"],
}

# Recipe = orchestration nhiều mode (không phải 1 template mode). Emit qua build_recipe.
RECIPE_ALIASES = {"BRIEF", "RECIPE", "LEO-PART-BRIEF"}


class BuildError(Exception):
    pass


def build_recipe(params, classification="THƯỜNG", assumptions=None, recipe=None):
    """Sinh scaffold recipe đa-mode leo-part-brief (1 chi tiết nhỏ THƯỜNG hoàn chỉnh).
    Đây là KẾ HOẠCH nhiều bước — CEO chạy từng bước = 1 leo_prompt_build mode tương ứng.
    KHÔNG gửi nguyên khối qua leo_send."""
    upper = {k.upper(): v for k, v in params.items()}
    part = str(upper.get("PART", "")).strip()
    if not part:
        raise BuildError(
            "Recipe leo-part-brief cần [PART]: mô tả 1 dòng chi tiết cần thiết kế "
            "(vd 'tay đỡ cổ tay kẹp ống tay cầm Ø28–32, tải ngang ~150 N')."
        )
    body = recipe if recipe is not None else _templates.load_recipe()
    giadinh = " · ".join(assumptions) if assumptions else "(chưa khai báo — CEO bổ sung, gồm số cần ĐO thật)"
    header = (
        "# RECIPE leo-part-brief — KẾ HOẠCH nhiều bước; chạy TỪNG bước = 1 leo_prompt_build mode tương ứng\n"
        f"[Phân loại: {classification}]\n"
        f"[PART] {part}\n"
        f"[GIẢ ĐỊNH] {giadinh}\n"
    )
    return header + "\n" + body


def build_prompt(mode, params, classification="THƯỜNG", assumptions=None, tpl_map=None):
    mode = (mode or "").upper()
    if mode in RECIPE_ALIASES:
        return build_recipe(params, classification, assumptions)
    if mode not in REQUIRED_FIELDS:
        raise BuildError(f"Mode không hợp lệ: '{mode}'. Hợp lệ: {sorted(REQUIRED_FIELDS)} (hoặc BRIEF = recipe).")
    upper_params = {k.upper(): v for k, v in params.items()}
    missing = [f for f in REQUIRED_FIELDS[mode] if not str(upper_params.get(f, "")).strip()]
    if missing:
        raise BuildError(
            f"Mode {mode} thiếu tham số bắt buộc: {missing}. "
            "KHÔNG sinh prompt mơ hồ — cấp giá trị ĐỊNH LƯỢNG (tải+đơn vị, kích thước interface thật)."
        )
    tpl = (tpl_map or _templates.load_templates())[mode]
    lines = []
    skip_continuations = False
    for line in tpl.splitlines():
        stripped = line.strip()
        if skip_continuations:
            if stripped.startswith("["):
                skip_continuations = False
            else:
                continue
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
        if filled is not None:
            lines.append(filled)
            skip_continuations = True
        else:
            lines.append(line)
    return "\n".join(lines)
