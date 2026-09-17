#!/usr/bin/env python3
"""Cổng máy cho /book-to-learn.

Dùng: python scripts/btl_gate_check.py <LEARN-dir> <L0|L1|L2|L3|L4|L5|L7> [tuỳ chọn]

Exit 0 = đạt (và ghi dấu vào _pipeline_state.md, trừ khi --no-stamp),
1 = trượt (in từng dòng FAIL), 2 = dùng sai.

Lý do tồn tại: chỗ nào hệ thống chỉ NÓI phải làm mà không có gì BẮT BUỘC,
chỗ đó thủng. Orchestrator không được đánh dấu một pha xong nếu script chưa exit 0.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date, datetime
from pathlib import Path

PHASES = ("L0", "L1", "L2", "L3", "L4", "L5", "L7")

STATE_KEYS = ("slug", "framework_ung_vien", "quick", "notebook_goc", "notebook_mo_rong", "started")
BRIEF_KEYS = ("van_de_that", "du_doan_1", "du_doan_2", "du_doan_3", "dreyfus_truoc",
              "target", "noi_ap_dung", "tieu_chi_thanh_cong")


# ---------------------------------------------------------------- đọc tệp

def read(path) -> str:
    return Path(path).read_text(encoding="utf-8")


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        elif value.startswith("[") and value.endswith("]"):
            value = [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
        elif value.lower() in ("true", "false"):
            value = value.lower() == "true"
        out[key] = value
    return out


def sections(text: str) -> dict:
    out, current, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m or re.match(r"^#\s", line):
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = (m.group(1) if m else None), []
            continue
        if current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def section_starting(text: str, prefix: str) -> str:
    for heading, content in sections(text).items():
        if heading.startswith(prefix):
            return content
    return ""


def table_rows(text: str) -> list:
    rows, last_was_row = [], False
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            last_was_row = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if any(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            if last_was_row and rows:
                rows.pop()  # dòng ngay trên vạch phân cách là tiêu đề
            last_was_row = False
            continue
        rows.append(cells)
        last_was_row = True
    return rows


def slugify(name: str) -> str:
    s = name.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def words(text: str) -> int:
    return len([t for t in re.split(r"\s+", text) if t])


def is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def parse_day(value):
    try:
        return date.fromisoformat(str(value).strip())
    except ValueError:
        return None


# ---------------------------------------------------------------- ngữ cảnh

class Ctx:
    def __init__(self, learn_dir, vault, books_root, skills_root, meta_dir,
                 nlm_list=None, nlm_content_dir=None):
        self.learn_dir = Path(learn_dir)
        self.vault = Path(vault)
        self.books_root = Path(books_root)
        self.skills_root = Path(skills_root)
        self.meta_dir = Path(meta_dir)
        self.nlm_list = Path(nlm_list) if nlm_list else None
        self.nlm_content_dir = Path(nlm_content_dir) if nlm_content_dir else None

    @classmethod
    def from_args(cls, a):
        learn = Path(a.learn_dir).resolve()
        vault = Path(a.vault).resolve() if a.vault else learn.parents[1]
        return cls(
            learn, vault,
            a.books_root or vault / "3_Resources" / "Books",
            a.skills_root or Path.home() / ".claude" / "skills",
            a.meta_dir or vault / "2_Areas" / "CEO-Self" / "Learning-Meta",
            a.nlm_list, a.nlm_content_dir,
        )

    @property
    def state_path(self) -> Path:
        return self.learn_dir / "_pipeline_state.md"

    @property
    def state(self) -> dict:
        return parse_frontmatter(read(self.state_path)) if self.state_path.exists() else {}

    @property
    def slug(self) -> str:
        return str(self.state.get("slug", "")).strip()

    @property
    def frameworks(self) -> list:
        fws = self.state.get("framework_ung_vien", [])
        return fws if isinstance(fws, list) else []


def gate_passed(ctx: Ctx, phase: str) -> bool:
    if not ctx.state_path.exists():
        return False
    return re.search(rf"^- {phase}: PASS ", read(ctx.state_path), re.M) is not None


def stamp(ctx: Ctx, phase: str, now: datetime) -> None:
    text = read(ctx.state_path)
    line = f"- {phase}: PASS {now:%Y-%m-%dT%H:%M}"
    pattern = rf"^- {phase}: PASS .*$"
    if re.search(pattern, text, re.M):
        text = re.sub(pattern, line, text, flags=re.M)
    else:
        if "## Gates" not in text:
            text = text.rstrip("\n") + "\n\n## Gates\n"
        text = text.rstrip("\n") + "\n" + line + "\n"
    ctx.state_path.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- các cổng

LABEL_ONLY = re.compile(r"\s*[-*]?\s*(?:[^:]*:\s*)?\(?[A-Z]\)?\s*\.?\s*")


def check_L0(ctx: Ctx) -> list:
    p = ctx.learn_dir / "_Project_Brief.md"
    if not p.exists():
        return ["L0: thiếu _Project_Brief.md"]
    text = read(p)
    fm = parse_frontmatter(text)
    errs = []
    if not str(fm.get("van_de_that", "")).strip():
        errs.append("L0: van_de_that rỗng — cần một vấn đề/quyết định thật của Workshop X")
    if any(not str(fm.get(f"du_doan_{i}", "")).strip() for i in (1, 2, 3)) or "du_doan_4" in fm:
        errs.append("L0: cần đúng 3 dự đoán (du_doan_1..du_doan_3)")
    if str(fm.get("dreyfus_truoc", "")).strip() not in {"1", "2", "3", "4", "5"}:
        errs.append("L0: dreyfus_truoc phải là số 1–5")
    target = str(fm.get("target", "")).strip()
    if target:
        if not (ctx.vault / "1_Projects" / target).is_dir():
            errs.append(f"L0: dự án đích không tồn tại: 1_Projects/{target}")
    elif not str(fm.get("noi_ap_dung", "")).strip():
        errs.append("L0: không có target thì noi_ap_dung phải khác rỗng")
    for line in sections(text).get("Quyết định", "").splitlines():
        if line.strip() and LABEL_ONLY.fullmatch(line):
            errs.append(f"L0: quyết định phải ghi bằng chữ, không bằng nhãn: '{line.strip()}'")
    return errs


CHECKS = {"L0": check_L0}


# ---------------------------------------------------------------- CLI

def parse_args(argv):
    ap = argparse.ArgumentParser(prog="btl_gate_check")
    ap.add_argument("learn_dir")
    ap.add_argument("phase")
    ap.add_argument("--vault")
    ap.add_argument("--books-root")
    ap.add_argument("--skills-root")
    ap.add_argument("--meta-dir")
    ap.add_argument("--nlm-list", help="tệp JSON từ `nlm source list <notebook> -j`")
    ap.add_argument("--nlm-content-dir", help="thư mục chứa <source_id>.json từ `nlm source content <id> -j`")
    ap.add_argument("--no-stamp", action="store_true")
    return ap.parse_args(argv)


def main(argv=None) -> int:
    a = parse_args(sys.argv[1:] if argv is None else argv)
    if a.phase not in CHECKS:
        print(f"Pha không hợp lệ: {a.phase}. Dùng một trong: {', '.join(sorted(CHECKS))}")
        return 2
    ctx = Ctx.from_args(a)
    if not ctx.slug:
        print(f"Thiếu {ctx.state_path} hoặc thiếu trường slug")
        return 2
    errs = CHECKS[a.phase](ctx)
    for e in errs:
        print("FAIL " + e)
    if errs:
        return 1
    print(f"PASS {a.phase}")
    if not a.no_stamp:
        stamp(ctx, a.phase, datetime.now())
    return 0


if __name__ == "__main__":
    sys.exit(main())
