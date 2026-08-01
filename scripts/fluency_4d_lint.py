"""Linter giữ bốn file tham chiếu của plugin fluency-4d khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown để Cowork nạp được).
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "fluency-4d"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
REF_DIR = SKILLS_ROOT / "_shared" / "references"
SKILL_NAMES = ["fluency-4d-preflight", "fluency-4d-review", "fluency-4d-weekly"]

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


# Ledger schema validation
_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d+$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_EXP_RE = re.compile(r"^EXP-\d{3}$")

_GROUPS = {
    "del": ["problem", "platform", "task"],
    "des": ["product", "process", "performance"],
    "dis": ["product", "process", "performance"],
    "dil": ["creation", "transparency", "deployment"],
}
_TOP_KEYS = ["id", "date", "project", "mode", "scores", "weakest", "exp_active", "exp_held"]


def extract_sample_record(text: str) -> dict:
    """Lấy bản ghi mẫu trong khối ```json đầu tiên của ledger-schema.md."""
    m = _JSON_BLOCK_RE.search(text)
    if not m:
        raise ValueError("ledger-schema.md không có khối ```json nào")
    return json.loads(m.group(1))


def validate_ledger_line(obj: dict) -> list[str]:
    """Kiểm một bản ghi sổ điểm. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    for key in _TOP_KEYS:
        if key not in obj:
            errors.append(f"thiếu khóa bắt buộc: {key}")
    if errors:
        return errors

    if not _ID_RE.match(str(obj["id"])):
        errors.append(f"id sai định dạng <YYYY-MM-DD>-<n>: {obj['id']!r}")
    if not _DATE_RE.match(str(obj["date"])):
        errors.append(f"date sai định dạng YYYY-MM-DD: {obj['date']!r}")
    if not str(obj["project"]).strip():
        errors.append("project rỗng")
    if obj["mode"] not in MODES:
        errors.append(f"mode không hợp lệ: {obj['mode']!r} (phải thuộc {sorted(MODES)})")

    scores = obj["scores"]
    if not isinstance(scores, dict):
        errors.append("scores phải là object")
    else:
        if set(scores) != set(_GROUPS):
            errors.append(f"scores sai nhóm: {sorted(scores)} (cần {sorted(_GROUPS)})")
        for group, subs in _GROUPS.items():
            sub = scores.get(group)
            if not isinstance(sub, dict):
                errors.append(f"scores.{group} phải là object")
                continue
            if set(sub) != set(subs):
                errors.append(f"scores.{group} sai khóa con: {sorted(sub)} (cần {sorted(subs)})")
            for name, val in sub.items():
                if val is None:
                    continue
                if not isinstance(val, int) or isinstance(val, bool) or not 0 <= val <= 3:
                    errors.append(f"{group}.{name} phải là số nguyên 0-3 hoặc null, gặp: {val!r}")

    if obj["weakest"] is not None and obj["weakest"] not in CELLS:
        errors.append(f"weakest không phải mã ô hợp lệ: {obj['weakest']!r}")

    exp, held = obj["exp_active"], obj["exp_held"]
    if exp is not None and not _EXP_RE.match(str(exp)):
        errors.append(f"exp_active sai định dạng EXP-###: {exp!r}")
    if held is not None and not isinstance(held, bool):
        errors.append(f"exp_held phải là true/false/null, gặp: {held!r}")
    if (exp is None) != (held is None):
        errors.append("exp_active và exp_held phải cùng null hoặc cùng có giá trị")

    return errors


# Experiment protocol: parser + WIP=1 validator + streak state machine
STREAK_TO_PASS = 3
BREAKS_TO_FAIL = 3
_STATUSES = {"OPEN", "PASSED", "FAILED"}
_EXP_COLS = ["id", "cell", "if_then", "streak", "breaks", "status", "opened", "closed"]


def parse_experiments(text: str) -> list[dict]:
    """Đọc bảng thí nghiệm trong Markdown. Bỏ qua dòng tiêu đề và dòng gạch."""
    rows: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if len(cells) != len(_EXP_COLS):
            continue
        if not re.match(r"^EXP-\d{3}$", cells[0]):
            continue
        row = dict(zip(_EXP_COLS, cells))
        for key in ("streak", "breaks"):
            row[key] = int(row[key]) if row[key].isdigit() else -1
        rows.append(row)
    return rows


def validate_experiments(rows: list[dict]) -> list[str]:
    """Kiểm bảng thí nghiệm. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    seen: set[str] = set()
    open_rows = [r for r in rows if r["status"] == "OPEN"]
    if len(open_rows) > 1:
        errors.append(f"vi phạm WIP=1: có {len(open_rows)} thí nghiệm OPEN ({[r['id'] for r in open_rows]})")
    for r in rows:
        if r["id"] in seen:
            errors.append(f"trùng ID: {r['id']}")
        seen.add(r["id"])
        if r["cell"] not in CELLS:
            errors.append(f"{r['id']}: ô mục tiêu không hợp lệ: {r['cell']!r}")
        if not r["if_then"].startswith("Khi ") or " tôi " not in r["if_then"]:
            errors.append(f"{r['id']}: câu phải ở dạng nếu–thì hành vi 'Khi ... , tôi ...': {r['if_then']!r}")
        if r["status"] not in _STATUSES:
            errors.append(f"{r['id']}: trạng thái lạ: {r['status']!r}")
        if not 0 <= r["streak"] <= STREAK_TO_PASS:
            errors.append(f"{r['id']}: streak ngoài khoảng 0-{STREAK_TO_PASS}: {r['streak']}")
        if not 0 <= r["breaks"] <= BREAKS_TO_FAIL:
            errors.append(f"{r['id']}: đứt ngoài khoảng 0-{BREAKS_TO_FAIL}: {r['breaks']}")
        if r["status"] == "PASSED" and r["streak"] != STREAK_TO_PASS:
            errors.append(f"{r['id']}: PASSED phải có streak = {STREAK_TO_PASS}, gặp {r['streak']}")
        if r["status"] == "FAILED" and r["breaks"] != BREAKS_TO_FAIL:
            errors.append(f"{r['id']}: FAILED phải có đứt = {BREAKS_TO_FAIL}, gặp {r['breaks']}")
        if r["status"] in {"PASSED", "FAILED"} and not r["closed"].strip():
            errors.append(f"{r['id']}: đã đóng nhưng thiếu ngày đóng")
    return errors


# Kiểm chính SKILL.md — không chỉ bốn file tham chiếu.
# Trích dẫn tham chiếu trong SKILL.md luôn ở dạng ../_shared/references/<file>.md
_REF_CITE_RE = re.compile(r"\.\./_shared/references/([A-Za-z0-9._-]+\.md)")
# Đường dẫn sổ điểm, ví dụ: D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger
# Bắt cả dạng gạch chéo ngược (Windows, trong SKILL.md) lẫn gạch chéo xuôi (lệnh bash trong README);
# hai dạng được chuẩn hoá về một trước khi so, nên chỉ lệch THẬT mới báo lỗi.
_LEDGER_PATH_RE = re.compile(r"[A-Za-z]:[\\/][^\s`]*AI-Fluency-Ledger")


def load_skill_sources() -> dict[str, str]:
    """Trả về {tên tương đối: nội dung} của ba SKILL.md."""
    return {
        f"{name}/SKILL.md": (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        for name in SKILL_NAMES
    }


def load_plugin_markdown() -> dict[str, str]:
    """Trả về {tên tương đối: nội dung} của MỌI file .md trong plugin."""
    return {
        p.relative_to(PLUGIN_ROOT).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(PLUGIN_ROOT.rglob("*.md"))
    }


def lint_skills(skills=None, all_markdown=None, ref_exists=None) -> list[str]:
    """Kiểm ba SKILL.md: (a) file tham chiếu được trích dẫn phải tồn tại,
    (b) đường dẫn sổ điểm phải giống hệt nhau ở mọi file .md của plugin.

    Trả danh sách lỗi; rỗng nghĩa là đạt.
    """
    if skills is None:
        skills = load_skill_sources()
    if all_markdown is None:
        all_markdown = load_plugin_markdown()
    if ref_exists is None:
        def ref_exists(filename: str) -> bool:
            return (REF_DIR / filename).is_file()

    errors: list[str] = []

    # (a) Mọi file tham chiếu được SKILL.md trích dẫn phải có thật.
    for name, text in sorted(skills.items()):
        for ref in sorted(set(_REF_CITE_RE.findall(text))):
            if not ref_exists(ref):
                errors.append(f"{name} trích dẫn file tham chiếu không tồn tại: {ref}")

    # (b) Đường dẫn sổ điểm không được trôi lệch giữa các file.
    variants: dict[str, list[str]] = {}
    for name, text in sorted(all_markdown.items()):
        for hit in _LEDGER_PATH_RE.findall(text):
            variants.setdefault(hit.replace("\\", "/"), []).append(name)
    if len(variants) > 1:
        detail = "; ".join(
            f"{path!r} ở {sorted(set(files))}" for path, files in sorted(variants.items())
        )
        errors.append(f"đường dẫn sổ điểm lệch nhau giữa các file: {detail}")

    return errors


def apply_session(row: dict, held: bool) -> dict:
    """Áp kết quả một phiên lên thí nghiệm. Trả bản ghi MỚI."""
    out = dict(row)
    if row["status"] != "OPEN":
        # Thí nghiệm đã đóng (PASSED/FAILED) — phiên sau thuộc thí nghiệm KẾ TIẾP,
        # không được nới thêm streak/breaks trên bản ghi đã kết thúc.
        return out
    if held:
        out["streak"] = row["streak"] + 1
        if out["streak"] >= STREAK_TO_PASS:
            out["streak"] = STREAK_TO_PASS
            out["status"] = "PASSED"
    else:
        out["streak"] = 0
        out["breaks"] = row["breaks"] + 1
        if out["breaks"] >= BREAKS_TO_FAIL:
            out["breaks"] = BREAKS_TO_FAIL
            out["status"] = "FAILED"
    return out
