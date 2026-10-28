# book-to-learn Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `book-to-learn` orchestrator skill (L0–L7, ~30-day cycle) plus a machine gate checker, templates, references, and a static eval, so the CEO can learn a book and ship ≥1 measured application to Workshop X.

**Architecture:** A thin orchestrator `SKILL.md` delegates to existing skills (`book-to-skill`, `book-notebook` logic, `/research`, `/analyze`, `learn-*`, DMIR skills, `galaxy-gate`). All CEO gates and artifact contracts are enforced by one stdlib-only Python script `scripts/btl_gate_check.py`, whose field names are shared with the templates and verified by tests. Runtime data lives in the Obsidian vault (`D:\Workshop_X`), never in the repo.

**Tech Stack:** Python 3.12 stdlib + pytest; Markdown skills; JSON static eval run by `evals/run-eval.sh`.

**Spec:** `docs/superpowers/specs/2026-09-17-book-to-learn-design.md` (read it before starting any task).

## Global Constraints

- Worktree `D:\KN-Stack-btl`, branch `feature/book-to-learn`. All paths below are relative to that worktree.
- **Do NOT edit** `VERSION`, `CHANGELOG.md`, `scripts/_codify_ledger.md`, or the skill counts in `CLAUDE.md`. Changelog text goes in the PR description under `## CHANGELOG`.
- Commit message format: `[BOOK] <brief description>`, ending with the line `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- Python: stdlib only (no PyYAML) + pytest for tests. Always read/write files with `encoding="utf-8"`.
- **No `$` followed by a single digit** (regex `\$[0-9](?![0-9])`) anywhere in any `SKILL.md`. Claude Code substitutes `$0`…`$9` with the skill's arguments. Observed 2026-09-17: `$0–250K` became `Instant–250K`, `$3/MTok` became `Mike/MTok`, while `$15` and `$150K` stayed intact. (The spec says `\$[0-9]`; this tighter regex is the verified behavior.)
- DMIR = **Diagnose–Model–Intervene–Reflect**. Never present the reference documents' unsourced figures ("70% change initiatives fail", "15x faster", "ROI 10–50x", simulated case results) as fact.
- `learn-teach` has `disable-model-invocation: true` → the orchestrator must ask the CEO to run `/learn-teach` themselves. It cannot invoke it.
- Never call `chat_configure(goal=custom)`; never share `btl-*` notebooks publicly.
- Test fixtures are built programmatically with pytest `tmp_path` (the spec mentions `evals/fixtures/btl/`; programmatic fixtures replace that folder).
- Real `nlm` JSON shapes (captured 2026-09-17):
  - `nlm source list <nb> -j` → JSON array of `{"id","title","type","url","status"}`; ready = `status == 2`.
  - `nlm source content <id> -j` → object `{"content","title","source_type","url","char_count"}`.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/btl_gate_check.py` | Parse vault artifacts; one check function per gated phase (L0, L1, L2, L3, L4, L5, L7); stamp passes into `_pipeline_state.md`; CLI |
| `scripts/test_btl_gate_check.py` | pytest: pass + fail cases per phase, CLI behavior, stamping |
| `skills/book/book-to-learn/references/templates/*` | Blank artifacts CEO/AI fill; field names MUST equal checker constants |
| `scripts/test_btl_templates.py` | pytest: template keys ⊇ checker constants; blank templates FAIL gates |
| `skills/book/book-to-learn/references/dmir-unified.md` | Condensed DMIR (4 phases, leverage ladder, archetypes, AAR, learning-how-to-learn toolkit) + sources + caveats |
| `skills/book/book-to-learn/references/phase-contracts.md` | Per phase: inputs, outputs, skills called, exact gate command |
| `skills/book/book-to-learn/SKILL.md` | Orchestrator instructions |
| `evals/book-to-learn.json` | Static binary assertions on SKILL.md |
| `scripts/test_btl_eval.py` | Mutation test: deleting lines matched by each required assertion makes that assertion fail |

---

### Task 1: Gate checker core + L0

**Files:**
- Create: `scripts/btl_gate_check.py`
- Test: `scripts/test_btl_gate_check.py`

**Interfaces:**
- Produces (used by all later tasks):
  - `parse_frontmatter(text: str) -> dict` — values are `str`, `bool` (`true`/`false`), or `list[str]` (`[a, b]`)
  - `sections(text: str) -> dict[str, str]` — `## Heading` → body text
  - `table_rows(text: str) -> list[list[str]]` — data rows of markdown tables, header and separator rows removed
  - `slugify(name: str) -> str` — ASCII kebab-case, Vietnamese diacritics removed, `đ`→`d`
  - `class Ctx` with attributes `learn_dir, vault, books_root, skills_root, meta_dir, nlm_list, nlm_content_dir: Path|None`, and properties `state: dict`, `slug: str`
  - `gate_passed(ctx: Ctx, phase: str) -> bool`
  - `stamp(ctx: Ctx, phase: str, now: datetime) -> None`
  - `CHECKS: dict[str, Callable[[Ctx], list[str]]]` — empty list = pass
  - `main(argv: list[str]) -> int` — 0 pass, 1 fail, 2 usage error
  - Constants: `BRIEF_KEYS`, `STATE_KEYS`

- [ ] **Step 1: Write the failing tests**

Create `scripts/test_btl_gate_check.py`:

```python
"""pytest cho btl_gate_check.py — cổng máy của /book-to-learn.

Mỗi cổng có ít nhất một ca ĐẠT và các ca TRƯỢT tương ứng với lỗi đã gặp thật
(nhãn quyết định (A)/(B) bị ghi sai, $0 bị thay thành tham số, nguồn NLM status=2
nhưng là trang chặn bot, câu trả lời Feynman do AI điền...).
"""
import importlib.util
import json
import textwrap
from pathlib import Path
from types import SimpleNamespace

import pytest

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("gc", HERE / "btl_gate_check.py")
gc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gc)


def w(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")
    return path


@pytest.fixture
def env(tmp_path):
    vault = tmp_path / "vault"
    learn = vault / "1_Projects" / "LEARN-demo"
    (vault / "1_Projects" / "VN-TGT-F").mkdir(parents=True)
    ns = SimpleNamespace(
        vault=vault,
        learn=learn,
        skills=tmp_path / "skills",
        books=vault / "3_Resources" / "Books",
        meta=vault / "2_Areas" / "CEO-Self" / "Learning-Meta",
        tmp=tmp_path,
    )
    w(learn / "_pipeline_state.md", """
        ---
        slug: demo
        framework_ung_vien: [Small Plates]
        ---
        """)
    return ns


def run(env, phase, *extra):
    argv = [str(env.learn), phase,
            "--skills-root", str(env.skills),
            "--books-root", str(env.books),
            "--meta-dir", str(env.meta), *extra]
    return gc.main(argv)


def state_text(env):
    return (env.learn / "_pipeline_state.md").read_text(encoding="utf-8")


GOOD_BRIEF = """
    ---
    van_de_that: Định giá pilot VN-TGT-F khi biên gộp ở mức 10 bộ gần bằng 0
    du_doan_1: Sách khuyên trích lợi nhuận trên mọi khoản thu, kể cả hợp đồng nhỏ
    du_doan_2: Sách không nói gì về hợp đồng quốc phòng dài hạn
    du_doan_3: Framework dễ áp nhất sẽ là tách tài khoản
    dreyfus_truoc: 2
    target: VN-TGT-F
    noi_ap_dung:
    tieu_chi_thanh_cong: Có quyết định giá pilot kèm con số trước ngày 30
    ---
    ## Quyết định
    - Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận
    """


# ---------- helpers ----------

def test_parse_frontmatter_types():
    fm = gc.parse_frontmatter("---\na: x: y\nb: [P, Q R]\nc: true\nd: \"q\"\n---\nbody")
    assert fm == {"a": "x: y", "b": ["P", "Q R"], "c": True, "d": "q"}


def test_table_rows_drops_header_and_separator():
    rows = gc.table_rows("| H1 | H2 |\n|---|---|\n| a | b |\n| c | d |\n")
    assert rows == [["a", "b"], ["c", "d"]]


def test_slugify_vietnamese():
    assert gc.slugify("Đảo công thức: Lợi nhuận trước") == "dao-cong-thuc-loi-nhuan-truoc"


# ---------- CLI ----------

def test_unknown_phase_is_usage_error(env):
    assert run(env, "L9") == 2


def test_missing_state_is_usage_error(env):
    (env.learn / "_pipeline_state.md").unlink()
    assert run(env, "L0") == 2


# ---------- L0 ----------

def test_L0_pass_and_stamp(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    assert run(env, "L0") == 0
    assert "- L0: PASS " in state_text(env)
    assert gc.gate_passed(gc.Ctx.from_args(gc.parse_args([str(env.learn), "L0"])), "L0")


def test_L0_stamp_replaces_not_duplicates(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    run(env, "L0")
    run(env, "L0")
    assert state_text(env).count("- L0: PASS ") == 1


def test_L0_no_stamp_flag(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF)
    assert run(env, "L0", "--no-stamp") == 0
    assert "L0: PASS" not in state_text(env)


def test_L0_fails_without_real_problem(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "van_de_that: Định giá pilot VN-TGT-F khi biên gộp ở mức 10 bộ gần bằng 0", "van_de_that:"))
    assert run(env, "L0") == 1
    assert "van_de_that" in capsys.readouterr().out
    assert "L0: PASS" not in state_text(env)


def test_L0_fails_with_two_predictions(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "du_doan_3: Framework dễ áp nhất sẽ là tách tài khoản", "du_doan_3:"))
    assert run(env, "L0") == 1
    assert "3 dự đoán" in capsys.readouterr().out


def test_L0_fails_bad_dreyfus(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("dreyfus_truoc: 2", "dreyfus_truoc: cao"))
    assert run(env, "L0") == 1


def test_L0_fails_missing_target_project(env, capsys):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target: VN-KHONG-CO"))
    assert run(env, "L0") == 1
    assert "VN-KHONG-CO" in capsys.readouterr().out


def test_L0_passes_without_target_if_noi_ap_dung(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target:")
      .replace("noi_ap_dung:", "noi_ap_dung: Cả Workshop X — dòng tiền công ty"))
    assert run(env, "L0") == 0


def test_L0_fails_without_target_and_noi_ap_dung(env):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace("target: VN-TGT-F", "target:"))
    assert run(env, "L0") == 1


@pytest.mark.parametrize("line", ["- Định giá pilot: (B)", "- (A)", "- Phương án: B"])
def test_L0_fails_label_only_decision(env, capsys, line):
    w(env.learn / "_Project_Brief.md", GOOD_BRIEF.replace(
        "- Định giá pilot: chọn giá vốn cộng 5% để giữ thói quen trích lợi nhuận", line))
    assert run(env, "L0") == 1
    assert "bằng chữ" in capsys.readouterr().out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v`
Expected: collection ERROR — `FileNotFoundError` for `btl_gate_check.py`.

- [ ] **Step 3: Write the implementation**

Create `scripts/btl_gate_check.py`:

```python
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
```

Note: `PHASES` lists all gated phases. `CHECKS` grows in Tasks 2–5; the CLI validates against `CHECKS`, so an unknown phase still returns 2.

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v`
Expected: all PASS.

In `test_L0_pass_and_stamp`, `Ctx.from_args(parse_args([learn, "L0"]))` defaults skills-root to the home directory. That is fine because `gate_passed` only reads the state file.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add scripts/btl_gate_check.py scripts/test_btl_gate_check.py
git commit -m "[BOOK] btl_gate_check: lõi đọc tệp, ghi dấu cổng, cổng L0

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 2: Gate L1 (skill tri thức, Leverage_Map, Learning_Kit)

**Files:**
- Modify: `scripts/btl_gate_check.py` (add `check_L1`, register in `CHECKS`)
- Modify: `scripts/test_btl_gate_check.py` (append tests)

**Interfaces:**
- Consumes: `Ctx`, `read`, `table_rows`, `CHECKS` from Task 1
- Produces: `check_L1(ctx) -> list[str]`; constant `ARG_SUBST = re.compile(r"\$[0-9](?![0-9])")`
- Artifact contracts:
  - `<skills_root>/<slug>/SKILL.md` + `<skills_root>/<slug>/chapters/*.md`
  - `<books_root>/<slug>/Leverage_Map.md` — table `| Framework | Mức | Lý do | Chương |`; `Mức` ∈ `L1`…`L12`
  - `<books_root>/<slug>/Learning_Kit.md` — non-empty

- [ ] **Step 1: Write the failing tests** (append to `scripts/test_btl_gate_check.py`)

```python
# ---------- L1 ----------

def make_L1(env, skill_md="# Demo\nTAP 0–250K USD; nhân sự $150K–$250K\n", level="L5"):
    w(env.skills / "demo" / "SKILL.md", skill_md)
    w(env.skills / "demo" / "chapters" / "ch01-intro.md", "# Ch1\n")
    w(env.books / "demo" / "Leverage_Map.md", f"""
        | Framework | Mức | Lý do | Chương |
        |---|---|---|---|
        | Small Plates | {level} | đổi luật chơi phân bổ | ch02 |
        """)
    w(env.books / "demo" / "Learning_Kit.md", "## Small Plates\n### Chunking\n...\n")


def test_L1_pass(env):
    make_L1(env)
    assert run(env, "L1") == 0


def test_L1_fails_arg_substitution_hazard(env, capsys):
    make_L1(env, skill_md="| Real Revenue | $0–250K |\n")
    assert run(env, "L1") == 1
    assert "$<số>" in capsys.readouterr().out


def test_L1_allows_multi_digit_dollar(env):
    make_L1(env, skill_md="Staffing $150K and $15/MTok\n")
    assert run(env, "L1") == 0


def test_L1_fails_bad_leverage_level(env, capsys):
    make_L1(env, level="L13")
    assert run(env, "L1") == 1
    assert "Small Plates" in capsys.readouterr().out


def test_L1_fails_no_chapters(env):
    make_L1(env)
    (env.skills / "demo" / "chapters" / "ch01-intro.md").unlink()
    assert run(env, "L1") == 1


def test_L1_fails_missing_learning_kit(env):
    make_L1(env)
    (env.books / "demo" / "Learning_Kit.md").unlink()
    assert run(env, "L1") == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -k L1 -v`
Expected: FAIL — `run` returns 2 because `L1` is not in `CHECKS`.

- [ ] **Step 3: Implement** — add to `scripts/btl_gate_check.py` above `CHECKS`, then replace the `CHECKS` line:

```python
ARG_SUBST = re.compile(r"\$[0-9](?![0-9])")
LEVEL = re.compile(r"L([1-9]|1[0-2])")


def check_L1(ctx: Ctx) -> list:
    errs = []
    skill_dir = ctx.skills_root / ctx.slug
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"L1: thiếu {skill_md}"]
    if not list((skill_dir / "chapters").glob("*.md")):
        errs.append("L1: skill không có chương nào trong chapters/")
    for i, line in enumerate(read(skill_md).splitlines(), 1):
        if ARG_SUBST.search(line):
            errs.append(f"L1: SKILL.md dòng {i} có '$<số>' — Claude Code sẽ thay bằng tham số: {line.strip()[:80]}")
    lever = ctx.books_root / ctx.slug / "Leverage_Map.md"
    if not lever.exists():
        errs.append("L1: thiếu Leverage_Map.md")
    else:
        rows = table_rows(read(lever))
        if not rows:
            errs.append("L1: Leverage_Map.md không có dòng framework nào")
        for r in rows:
            if len(r) < 2 or not LEVEL.fullmatch(r[1]):
                errs.append(f"L1: framework '{r[0]}' thiếu mức đòn bẩy L1–L12")
    kit = ctx.books_root / ctx.slug / "Learning_Kit.md"
    if not kit.exists() or not read(kit).strip():
        errs.append("L1: thiếu hoặc rỗng Learning_Kit.md")
    return errs


CHECKS = {"L0": check_L0, "L1": check_L1}
```

- [ ] **Step 4: Run all tests**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add scripts/btl_gate_check.py scripts/test_btl_gate_check.py
git commit -m "[BOOK] btl_gate_check: cổng L1 — skill, bẫy \$<số>, Leverage_Map, Learning_Kit

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 3: Gate L2 (NotebookLM toàn văn theo chương)

**Files:**
- Modify: `scripts/btl_gate_check.py`
- Modify: `scripts/test_btl_gate_check.py`

**Interfaces:**
- Consumes: `Ctx.nlm_list`, `Ctx.nlm_content_dir`, `Ctx.books_root`, `read`
- Produces: `check_L2(ctx) -> list[str]`
- Contract: `_source/` files are uploaded with **title = filename**. The orchestrator saves `nlm source list <nb> -j > <dir>/list.json` and, for each id, `nlm source content <id> -j > <dir>/content/<id>.json`.

- [ ] **Step 1: Write the failing tests** (append)

```python
# ---------- L2 ----------

def make_L2(env, statuses=(2, 2), chars=(80, 90)):
    src = env.books / "demo" / "_source"
    w(src / "ch01.md", "x" * 100)
    w(src / "ch02.md", "y" * 100)
    items = [{"id": f"id{i}", "title": f"ch0{i + 1}.md", "type": "generated_text",
              "url": None, "status": s} for i, s in enumerate(statuses)]
    lst = w(env.tmp / "nlm" / "list.json", json.dumps(items))
    cdir = env.tmp / "nlm" / "content"
    for i, c in enumerate(chars):
        w(cdir / f"id{i}.json", json.dumps({"content": "z" * c, "title": f"ch0{i + 1}.md",
                                           "source_type": "generated_text", "url": None,
                                           "char_count": c}))
    return ["--nlm-list", str(lst), "--nlm-content-dir", str(cdir)]


def test_L2_pass(env):
    assert run(env, "L2", *make_L2(env)) == 0


def test_L2_fails_without_nlm_list(env, capsys):
    make_L2(env)
    assert run(env, "L2") == 1
    assert "--nlm-list" in capsys.readouterr().out


def test_L2_fails_not_ready(env):
    assert run(env, "L2", *make_L2(env, statuses=(2, 1))) == 1


def test_L2_fails_bot_wall_short_content(env, capsys):
    assert run(env, "L2", *make_L2(env, chars=(80, 30))) == 1
    assert "ch02.md" in capsys.readouterr().out


def test_L2_fails_count_mismatch(env):
    extra = make_L2(env)
    w(env.books / "demo" / "_source" / "ch03.md", "q" * 100)
    assert run(env, "L2", *extra) == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -k L2 -v`
Expected: FAIL (exit 2, `L2` not in `CHECKS`).

- [ ] **Step 3: Implement** (add above `CHECKS`, update `CHECKS`)

```python
def check_L2(ctx: Ctx) -> list:
    src = ctx.books_root / ctx.slug / "_source"
    files = sorted(p for p in src.glob("*") if p.is_file()) if src.is_dir() else []
    if not files:
        return ["L2: _source/ trống — chưa tách chương"]
    if not ctx.nlm_list or not ctx.nlm_list.exists():
        return ["L2: cần --nlm-list (JSON của `nlm source list <notebook> -j`) — không tin kết quả in ra của `source add`"]
    items = json.loads(read(ctx.nlm_list))
    by_title = {i.get("title"): i for i in items}
    errs = []
    ready = [i for i in items if i.get("status") == 2]
    if len(ready) != len(files):
        errs.append(f"L2: {len(ready)} nguồn sẵn sàng ≠ {len(files)} tệp chương")
    for f in files:
        item = by_title.get(f.name)
        if not item:
            errs.append(f"L2: không thấy nguồn '{f.name}' trên notebook")
            continue
        if item.get("status") != 2:
            errs.append(f"L2: nguồn '{f.name}' chưa sẵn sàng (status={item.get('status')})")
            continue
        cpath = ctx.nlm_content_dir / f"{item['id']}.json" if ctx.nlm_content_dir else None
        if not cpath or not cpath.exists():
            errs.append(f"L2: thiếu nội dung đã tải cho '{f.name}' (nlm source content {item['id']} -j)")
            continue
        got = json.loads(read(cpath)).get("char_count", 0)
        need = len(read(f)) * 0.5
        if got < need:
            errs.append(f"L2: nguồn '{f.name}' chỉ {got} ký tự < 50% tệp gốc ({len(read(f))}) — nghi trang chặn bot")
    return errs


CHECKS = {"L0": check_L0, "L1": check_L1, "L2": check_L2}
```

- [ ] **Step 4: Run all tests** — `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v` → all PASS.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add scripts/btl_gate_check.py scripts/test_btl_gate_check.py
git commit -m "[BOOK] btl_gate_check: cổng L2 — đối chiếu nguồn NLM theo status và độ dài nội dung

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 4: Gates L3 (Claims) and L4 (cổng Feynman)

**Files:**
- Modify: `scripts/btl_gate_check.py`
- Modify: `scripts/test_btl_gate_check.py`

**Interfaces:**
- Consumes: `table_rows`, `parse_frontmatter`, `section_starting`, `words`, `slugify`, `Ctx.frameworks`
- Produces: `check_L3`, `check_L4`; constants `CLAIM_LABELS = {"SUPPORTED", "CONTESTED", "CẦN-CHUYỂN-VN"}`, `FEYNMAN_KEYS = ("framework", "tac_gia")`, `MIN_ANSWER_WORDS = 40`
- Contracts:
  - `<books_root>/<slug>/Claims.md` — table `| # | Luận điểm | Nhãn | Nguồn | Vị trí |`
  - `<learn_dir>/learn/feynman-<slugify(framework)>.md` — frontmatter `framework`, `tac_gia: CEO`; headings starting `Q1`, `Q2`, `Q3` (question as `>` blockquote lines, answer below); heading starting `Rubric` with table whose last column is 1–5

- [ ] **Step 1: Write the failing tests** (append)

```python
# ---------- L3 ----------

def make_claims(env, row="| 1 | Trích lợi nhuận trước khi chi | SUPPORTED | Michalowicz 2014 | tr.19 |"):
    w(env.books / "demo" / "Claims.md", f"""
        | # | Luận điểm | Nhãn | Nguồn | Vị trí |
        |---|---|---|---|---|
        {row}
        """)


def test_L3_pass(env):
    make_claims(env)
    assert run(env, "L3") == 0


@pytest.mark.parametrize("row", [
    "| 1 | X | TRUE | Nguồn A | tr.3 |",
    "| 1 | X | SUPPORTED | Nguồn A | ✅ |",
    "| 1 | X | CONTESTED |  | tr.3 |",
    "| 1 | X | CẦN-CHUYỂN-VN | Nguồn A | — |",
])
def test_L3_fails_bad_row(env, row):
    make_claims(env, row)
    assert run(env, "L3") == 1


# ---------- L4 ----------

ANSWER = " ".join(["từ"] * 45)


def make_feynman(env, tac_gia="CEO", answer=ANSWER, level="3", name="Small Plates"):
    w(env.learn / "learn" / f"feynman-{gc.slugify(name)}.md", f"""
        ---
        framework: {name}
        tac_gia: {tac_gia}
        ---
        ## Q1 — Hiểu
        > Giải thích Small Plates trong 60 giây cho một người không học kế toán.
        {answer}
        ## Q2 — Áp dụng
        > Áp vào VN-TGT-F thì tài khoản nào mở trước?
        {ANSWER}
        ## Q3 — Tầng hệ thống
        > Nó cắt vòng lặp nào, điểm nghẽn nào?
        {ANSWER}
        ## Rubric tự chấm
        | Chỉ báo hành vi | Mức |
        |---|---|
        | Tự tính được tỉ lệ phân bổ từ số thật | {level} |
        """)


def test_L4_pass(env):
    make_feynman(env)
    assert run(env, "L4") == 0


def test_L4_fails_missing_file(env, capsys):
    assert run(env, "L4") == 1
    assert "feynman-small-plates.md" in capsys.readouterr().out


def test_L4_fails_ai_author(env):
    make_feynman(env, tac_gia="AI")
    assert run(env, "L4") == 1


def test_L4_fails_short_answer(env, capsys):
    make_feynman(env, answer="ngắn quá")
    assert run(env, "L4") == 1
    assert "Q1" in capsys.readouterr().out


def test_L4_fails_rubric_level(env):
    make_feynman(env, level="7")
    assert run(env, "L4") == 1


def test_L4_fails_without_candidates(env):
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: []\n---\n")
    assert run(env, "L4") == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -k "L3 or L4" -v`
Expected: FAIL (exit 2).

- [ ] **Step 3: Implement** (add above `CHECKS`, update `CHECKS`)

```python
CLAIM_LABELS = {"SUPPORTED", "CONTESTED", "CẦN-CHUYỂN-VN"}
EMPTY_CELL = {"", "-", "—", "✅", "✓"}
FEYNMAN_KEYS = ("framework", "tac_gia")
MIN_ANSWER_WORDS = 40


def check_L3(ctx: Ctx) -> list:
    p = ctx.books_root / ctx.slug / "Claims.md"
    if not p.exists():
        return ["L3: thiếu Claims.md"]
    rows = table_rows(read(p))
    if not rows:
        return ["L3: Claims.md không có luận điểm nào"]
    errs = []
    for r in rows:
        if len(r) < 5:
            errs.append(f"L3: dòng thiếu cột (cần #, Luận điểm, Nhãn, Nguồn, Vị trí): {r}")
            continue
        num, claim, label, source, where = r[:5]
        if label not in CLAIM_LABELS:
            errs.append(f"L3: luận điểm {num} có nhãn '{label}' — chỉ nhận {sorted(CLAIM_LABELS)}")
        if source in EMPTY_CELL or where in EMPTY_CELL:
            errs.append(f"L3: luận điểm {num} thiếu nguồn hoặc vị trí (dấu ✅ không phải trích dẫn)")
    return errs


def check_L4(ctx: Ctx) -> list:
    if not ctx.frameworks:
        return ["L4: framework_ung_vien trong _pipeline_state.md đang rỗng — CEO chọn sau L1"]
    errs = []
    for fw in ctx.frameworks:
        name = f"feynman-{slugify(fw)}.md"
        p = ctx.learn_dir / "learn" / name
        if not p.exists():
            errs.append(f"L4: thiếu learn/{name} cho framework '{fw}'")
            continue
        text = read(p)
        if str(parse_frontmatter(text).get("tac_gia", "")).strip() != "CEO":
            errs.append(f"L4: {name} phải có tac_gia: CEO — AI không được điền câu trả lời Feynman")
        for q in ("Q1", "Q2", "Q3"):
            answer = "\n".join(l for l in section_starting(text, q).splitlines()
                               if not l.lstrip().startswith(">"))
            if words(answer) < MIN_ANSWER_WORDS:
                errs.append(f"L4: {name} {q} chỉ {words(answer)} từ < {MIN_ANSWER_WORDS}")
        rubric = table_rows(section_starting(text, "Rubric"))
        if not rubric:
            errs.append(f"L4: {name} thiếu bảng Rubric tự chấm")
        for r in rubric:
            if r[-1] not in {"1", "2", "3", "4", "5"}:
                errs.append(f"L4: {name} rubric '{r[0]}' có mức '{r[-1]}' — cần 1–5")
    return errs


CHECKS = {"L0": check_L0, "L1": check_L1, "L2": check_L2, "L3": check_L3, "L4": check_L4}
```

- [ ] **Step 4: Run all tests** — `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v` → all PASS.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add scripts/btl_gate_check.py scripts/test_btl_gate_check.py
git commit -m "[BOOK] btl_gate_check: cổng L3 (Claims có nguồn) và cổng Feynman L4

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 5: Gates L5 (thẻ thí nghiệm) and L7 (AAR + sổ meta)

**Files:**
- Modify: `scripts/btl_gate_check.py`
- Modify: `scripts/test_btl_gate_check.py`

**Interfaces:**
- Consumes: `gate_passed`, `parse_frontmatter`, `sections`, `parse_day`, `is_int`, `Ctx.frameworks`, `Ctx.state`
- Produces: `check_L5`, `check_L7`; constants `CARD_KEYS`, `MAX_RUN_DAYS = 16`, `AAR_HEADINGS`, `AAR_KEYS = ("quyet_dinh",)`, `DECISIONS = {"keep", "adapt", "drop"}`, `CYCLE_KEYS: dict[str, type|tuple]`
- Contracts:
  - `<learn_dir>/Experiment_Card.md` frontmatter = `CARD_KEYS`
  - `<learn_dir>/AAR.md` frontmatter `quyet_dinh`, headings = `AAR_HEADINGS`
  - `<meta_dir>/cycles.jsonl` — last object with `slug == ctx.slug` must match `CYCLE_KEYS`

- [ ] **Step 1: Write the failing tests** (append)

```python
# ---------- L5 ----------

GOOD_CARD = """
    ---
    framework: Small Plates
    gia_thuyet: Trích 5% mỗi khoản thu pilot không làm chậm chi trả nhà cung cấp
    chi_so: Số ngày trễ hạn thanh toán nhà cung cấp
    baseline: 0
    nguong: ≤ 2 ngày trễ trong 16 ngày chạy
    nguoi_chiu_trach_nhiem: CEO
    ngay_bat_dau: 2026-09-20
    ngay_ket_thuc: 2026-10-06
    du_doan: Không trễ ngày nào
    don_vi_framework: công ty
    don_vi_thi_nghiem: công ty
    muc_tin_cay_du_lieu: L3 — số kế toán thật
    ceo_duyet: 2026-09-19
    ---
    """


def pass_gates(env, *phases):
    for ph in phases:
        env.learn.joinpath("_pipeline_state.md").write_text(
            state_text(env).rstrip("\n") + f"\n- {ph}: PASS 2026-09-18T09:00\n", encoding="utf-8")


def test_L5_pass(env):
    pass_gates(env, "L3", "L4")
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 0


@pytest.mark.parametrize("old,new", [
    ("baseline: 0", "baseline: chưa đo"),
    ("ngay_ket_thuc: 2026-10-06", "ngay_ket_thuc: 2026-10-07"),
    ("don_vi_thi_nghiem: công ty", "don_vi_thi_nghiem: dòng sản phẩm"),
    ("ceo_duyet: 2026-09-19", "ceo_duyet:"),
    ("framework: Small Plates", "framework: RIFA"),
    ("muc_tin_cay_du_lieu: L3 — số kế toán thật", "muc_tin_cay_du_lieu: cao"),
    ("nguoi_chiu_trach_nhiem: CEO", "nguoi_chiu_trach_nhiem:"),
])
def test_L5_fails_bad_card(env, old, new):
    pass_gates(env, "L3", "L4")
    w(env.learn / "Experiment_Card.md", GOOD_CARD.replace(old, new))
    assert run(env, "L5") == 1


def test_L5_fails_without_feynman_gate(env, capsys):
    pass_gates(env, "L3")
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 1
    assert "L4" in capsys.readouterr().out


def test_L5_quick_skips_claims_but_not_feynman(env):
    w(env.learn / "_pipeline_state.md", "---\nslug: demo\nframework_ung_vien: [Small Plates]\nquick: true\n---\n")
    pass_gates(env, "L4")
    w(env.learn / "Experiment_Card.md", GOOD_CARD)
    assert run(env, "L5") == 0


# ---------- L7 ----------

GOOD_AAR = """
    ---
    quyet_dinh: adapt
    ---
    ## Định xảy ra gì
    Không trễ thanh toán.
    ## Thực tế ra sao
    Trễ 1 ngày vào kỳ 25.
    ## Vì sao khác
    Khoản thu lệch lịch 10/25.
    ## Lần sau làm gì
    Dời ngày phân bổ theo lịch thu thật.
    """


def cycle_row(**over):
    row = {"slug": "demo", "opened": "2026-09-17", "closed": "2026-10-17", "target": "VN-TGT-F",
           "dreyfus_before": 2, "dreyfus_after": 3, "leverage_reached": "L5", "perkins": "strategic",
           "applied": True, "decision": "adapt", "prediction_hits": 1, "prediction_total": 3,
           "days_to_competence": 11, "techniques": {"feynman": 5}, "illusion_gap": 0.25,
           "book_type": "text", "failure_points": [], "next_book_hint": "The Goal"}
    row.update(over)
    return row


def make_L7(env, row, aar=GOOD_AAR):
    w(env.learn / "AAR.md", aar)
    w(env.meta / "cycles.jsonl", json.dumps({"slug": "other"}) + "\n" + json.dumps(row, ensure_ascii=False) + "\n")


def test_L7_pass(env):
    pass_gates(env, "L5")
    make_L7(env, cycle_row())
    assert run(env, "L7") == 0


def test_L7_unapplied_cycle_can_close(env):
    make_L7(env, cycle_row(applied=False))
    assert run(env, "L7") == 0


def test_L7_fails_applied_without_L5(env, capsys):
    make_L7(env, cycle_row(applied=True))
    assert run(env, "L7") == 1
    assert "applied" in capsys.readouterr().out


@pytest.mark.parametrize("over", [
    {"decision": "maybe"}, {"dreyfus_after": "3"}, {"applied": "yes"},
    {"days_to_competence": True}, {"perkins": "genius"}, {"leverage_reached": "L0"},
])
def test_L7_fails_bad_cycle_row(env, over):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(**over))
    assert run(env, "L7") == 1


def test_L7_fails_missing_row(env):
    pass_gates(env, "L5")
    w(env.learn / "AAR.md", GOOD_AAR)
    w(env.meta / "cycles.jsonl", json.dumps({"slug": "other"}) + "\n")
    assert run(env, "L7") == 1


def test_L7_fails_bad_aar(env):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(), aar=GOOD_AAR.replace("quyet_dinh: adapt", "quyet_dinh: có lẽ"))
    assert run(env, "L7") == 1


def test_L7_fails_empty_aar_section(env):
    pass_gates(env, "L5")
    make_L7(env, cycle_row(), aar=GOOD_AAR.replace("Khoản thu lệch lịch 10/25.", ""))
    assert run(env, "L7") == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -k "L5 or L7" -v`
Expected: FAIL (exit 2).

- [ ] **Step 3: Implement** (add above `CHECKS`, replace `CHECKS`)

```python
CARD_KEYS = ("framework", "gia_thuyet", "chi_so", "baseline", "nguong", "nguoi_chiu_trach_nhiem",
             "ngay_bat_dau", "ngay_ket_thuc", "du_doan", "don_vi_framework", "don_vi_thi_nghiem",
             "muc_tin_cay_du_lieu", "ceo_duyet")
MAX_RUN_DAYS = 16
AAR_HEADINGS = ("Định xảy ra gì", "Thực tế ra sao", "Vì sao khác", "Lần sau làm gì")
AAR_KEYS = ("quyet_dinh",)
DECISIONS = {"keep", "adapt", "drop"}
PERKINS = {"tacit", "aware", "strategic", "reflective"}
CYCLE_KEYS = {
    "slug": str, "opened": str, "closed": str, "target": (str, type(None)),
    "dreyfus_before": int, "dreyfus_after": int, "leverage_reached": str, "perkins": str,
    "applied": bool, "decision": str, "prediction_hits": int, "prediction_total": int,
    "days_to_competence": int, "techniques": dict, "illusion_gap": (int, float),
    "book_type": str, "failure_points": list, "next_book_hint": str,
}


def check_L5(ctx: Ctx) -> list:
    errs = []
    if not gate_passed(ctx, "L4"):
        errs.append("L5: cổng Feynman L4 chưa qua")
    if not ctx.state.get("quick") and not gate_passed(ctx, "L3"):
        errs.append("L5: L3 (Claims) chưa qua — hoặc đặt quick: true và chấp nhận nhãn CHƯA KIỂM")
    p = ctx.learn_dir / "Experiment_Card.md"
    if not p.exists():
        return errs + ["L5: thiếu Experiment_Card.md"]
    fm = parse_frontmatter(read(p))
    for k in CARD_KEYS:
        if not str(fm.get(k, "")).strip():
            errs.append(f"L5: thẻ thiếu ô {k}")
    if str(fm.get("framework", "")).strip() and fm.get("framework") not in ctx.frameworks:
        errs.append(f"L5: framework '{fm.get('framework')}' không nằm trong framework_ung_vien")
    if str(fm.get("baseline", "")).strip() and not re.fullmatch(r"-?\d+(?:[.,]\d+)?", str(fm["baseline"]).strip()):
        errs.append(f"L5: baseline phải là con số, đang là '{fm['baseline']}'")
    start, end = parse_day(fm.get("ngay_bat_dau", "")), parse_day(fm.get("ngay_ket_thuc", ""))
    if not start or not end:
        errs.append("L5: ngay_bat_dau/ngay_ket_thuc phải là ngày ISO YYYY-MM-DD")
    elif not 0 <= (end - start).days <= MAX_RUN_DAYS:
        errs.append(f"L5: thời lượng {(end - start).days} ngày — phải trong 0–{MAX_RUN_DAYS}")
    uf, ut = str(fm.get("don_vi_framework", "")).strip(), str(fm.get("don_vi_thi_nghiem", "")).strip()
    if uf and ut and uf.casefold() != ut.casefold():
        errs.append(f"L5: đơn vị phân tích lệch — framework '{uf}' ≠ thí nghiệm '{ut}'")
    trust = str(fm.get("muc_tin_cay_du_lieu", "")).strip()
    if trust and not re.match(r"L[1-5]\b", trust):
        errs.append("L5: muc_tin_cay_du_lieu phải bắt đầu bằng L1–L5")
    if str(fm.get("ceo_duyet", "")).strip() and not parse_day(fm.get("ceo_duyet")):
        errs.append("L5: ceo_duyet phải là ngày ISO")
    return errs


def check_L7(ctx: Ctx) -> list:
    errs = []
    aar = ctx.learn_dir / "AAR.md"
    if not aar.exists():
        errs.append("L7: thiếu AAR.md")
    else:
        text = read(aar)
        if parse_frontmatter(text).get("quyet_dinh") not in DECISIONS:
            errs.append(f"L7: quyet_dinh phải thuộc {sorted(DECISIONS)}")
        secs = sections(text)
        for h in AAR_HEADINGS:
            if not secs.get(h, "").strip():
                errs.append(f"L7: AAR thiếu hoặc rỗng mục '{h}'")
    ledger = ctx.meta_dir / "cycles.jsonl"
    rows = []
    if ledger.exists():
        for line in read(ledger).splitlines():
            if line.strip():
                obj = json.loads(line)
                if obj.get("slug") == ctx.slug:
                    rows.append(obj)
    if not rows:
        return errs + [f"L7: cycles.jsonl chưa có dòng cho slug '{ctx.slug}'"]
    row = rows[-1]
    for k, typ in CYCLE_KEYS.items():
        if k not in row:
            errs.append(f"L7: dòng meta thiếu '{k}'")
            continue
        v = row[k]
        ok = is_int(v) if typ is int else (isinstance(v, typ) and not (isinstance(v, bool) and typ != bool))
        if not ok:
            errs.append(f"L7: '{k}' sai kiểu: {v!r}")
    if row.get("decision") not in DECISIONS:
        errs.append("L7: decision phải là keep/adapt/drop")
    if row.get("perkins") not in PERKINS:
        errs.append(f"L7: perkins phải thuộc {sorted(PERKINS)}")
    if not LEVEL.fullmatch(str(row.get("leverage_reached", ""))):
        errs.append("L7: leverage_reached phải là L1–L12")
    for k in ("dreyfus_before", "dreyfus_after"):
        if is_int(row.get(k)) and not 1 <= row[k] <= 5:
            errs.append(f"L7: {k} phải 1–5")
    if row.get("applied") is True and not gate_passed(ctx, "L5"):
        errs.append("L7: applied=true nhưng thẻ thí nghiệm L5 chưa qua cổng — ghi applied=false")
    return errs


CHECKS = {"L0": check_L0, "L1": check_L1, "L2": check_L2, "L3": check_L3,
          "L4": check_L4, "L5": check_L5, "L7": check_L7}
```

- [ ] **Step 4: Run all tests** — `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py -v` → all PASS. If `test_L7_fails_bad_cycle_row[over3]` (`days_to_competence: True`) passes unexpectedly, confirm the int branch uses `is_int`.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add scripts/btl_gate_check.py scripts/test_btl_gate_check.py
git commit -m "[BOOK] btl_gate_check: cổng L5 (thẻ thí nghiệm DMIR) và L7 (AAR + sổ meta)

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 6: Templates + consistency test

**Files:**
- Create: `skills/book/book-to-learn/references/templates/pipeline-state.md`
- Create: `skills/book/book-to-learn/references/templates/mission.md`
- Create: `skills/book/book-to-learn/references/templates/leverage-map.md`
- Create: `skills/book/book-to-learn/references/templates/claims.md`
- Create: `skills/book/book-to-learn/references/templates/learning-kit.md`
- Create: `skills/book/book-to-learn/references/templates/feynman.md`
- Create: `skills/book/book-to-learn/references/templates/experiment-card.md`
- Create: `skills/book/book-to-learn/references/templates/run-log.md`
- Create: `skills/book/book-to-learn/references/templates/aar.md`
- Create: `skills/book/book-to-learn/references/templates/cycles-row.json`
- Test: `scripts/test_btl_templates.py`

**Interfaces:**
- Consumes: `STATE_KEYS`, `BRIEF_KEYS`, `FEYNMAN_KEYS`, `CARD_KEYS`, `AAR_KEYS`, `AAR_HEADINGS`, `CYCLE_KEYS`, `CHECKS`, `main`
- Produces: templates copied by the orchestrator (Task 8) into the vault

- [ ] **Step 1: Write the failing test**

Create `scripts/test_btl_templates.py`:

```python
"""Khuôn của /book-to-learn phải khớp tên trường mà btl_gate_check đọc,
và khuôn TRỐNG phải TRƯỢT cổng (khuôn không được tự đạt)."""
import importlib.util
import json
import shutil
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
T = ROOT / "skills" / "book" / "book-to-learn" / "references" / "templates"
_spec = importlib.util.spec_from_file_location("gc", HERE / "btl_gate_check.py")
gc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gc)


def keys(name):
    return set(gc.parse_frontmatter((T / name).read_text(encoding="utf-8")))


@pytest.mark.parametrize("name,expected", [
    ("pipeline-state.md", "STATE_KEYS"),
    ("mission.md", "BRIEF_KEYS"),
    ("feynman.md", "FEYNMAN_KEYS"),
    ("experiment-card.md", "CARD_KEYS"),
    ("aar.md", "AAR_KEYS"),
])
def test_template_has_checker_keys(name, expected):
    assert set(getattr(gc, expected)) <= keys(name)


def test_aar_template_headings():
    secs = gc.sections((T / "aar.md").read_text(encoding="utf-8"))
    assert all(h in secs for h in gc.AAR_HEADINGS)


def test_cycles_row_keys_match():
    row = json.loads((T / "cycles-row.json").read_text(encoding="utf-8"))
    assert set(row) == set(gc.CYCLE_KEYS)


def test_no_arg_substitution_hazard_in_templates():
    for p in T.iterdir():
        assert not gc.ARG_SUBST.search(p.read_text(encoding="utf-8")), p.name


@pytest.mark.parametrize("phase,files", [
    ("L0", {"mission.md": "_Project_Brief.md"}),
    ("L5", {"experiment-card.md": "Experiment_Card.md"}),
])
def test_blank_template_fails_gate(tmp_path, phase, files):
    learn = tmp_path / "vault" / "1_Projects" / "LEARN-demo"
    learn.mkdir(parents=True)
    state = (T / "pipeline-state.md").read_text(encoding="utf-8").replace("slug:", "slug: demo", 1)
    (learn / "_pipeline_state.md").write_text(state, encoding="utf-8")
    for src, dst in files.items():
        shutil.copy(T / src, learn / dst)
    assert gc.main([str(learn), phase, "--no-stamp", "--skills-root", str(tmp_path)]) == 1
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_templates.py -v`
Expected: FAIL (`FileNotFoundError` on templates).

- [ ] **Step 3: Create the templates** (exact content)

`skills/book/book-to-learn/references/templates/pipeline-state.md`:
```markdown
---
slug:
framework_ung_vien: []
quick: false
notebook_goc:
notebook_mo_rong:
started:
---
# Trạng thái chu kỳ book-to-learn

Sửa `framework_ung_vien` sau L1 (có thể chỉnh sau L3). Thẻ L5 chỉ được dùng framework trong danh sách này.
Dòng dưới "## Gates" do `scripts/btl_gate_check.py` ghi — không tự tay thêm.

## Gates
```

`skills/book/book-to-learn/references/templates/mission.md`:
```markdown
---
created:
updated:
type: project
status: active
tags: [#type/project, #status/active, #topic/learning]
van_de_that:
du_doan_1:
du_doan_2:
du_doan_3:
dreyfus_truoc:
target:
noi_ap_dung:
tieu_chi_thanh_cong:
---
# LEARN — <tên sách>

## Vì sao cuốn này, vì sao bây giờ
<!-- Nối với vấn đề thật ở van_de_that. Không có vấn đề thật thì không mở chu kỳ. -->

## Lập kế hoạch siêu nhận thức (DMIR-R trước chu kỳ)
- Tôi đã biết gì về chủ đề này:
- Giả định ngầm của tôi:
- Thành công đo bằng gì (lặp lại tieu_chi_thanh_cong bằng số):

## Quyết định
<!-- Ghi quyết định bằng CHỮ ĐẦY ĐỦ. Cấm dòng chỉ có nhãn (A)/(B). -->
```

`skills/book/book-to-learn/references/templates/leverage-map.md`:
```markdown
# Leverage Map — <tên sách>

Mức đòn bẩy Meadows: L12 tham số · L11 buffer · L10 cấu trúc stock/flow · L9 độ trễ · L8 vòng cân bằng · L7 vòng tăng cường · L6 dòng thông tin · L5 luật chơi · L4 tự tổ chức · L3 mục tiêu · L2 paradigm · L1 vượt paradigm.

| Framework | Mức | Lý do | Chương |
|---|---|---|---|
```

`skills/book/book-to-learn/references/templates/claims.md`:
```markdown
# Claims — <tên sách>

Nhãn: SUPPORTED (có bằng chứng độc lập) · CONTESTED (có phản biện đáng kể) · CẦN-CHUYỂN-VN (đúng ở bối cảnh gốc, chưa kiểm ở VN/quốc phòng).
Mỗi dòng bắt buộc có Nguồn và Vị trí (trang/chương/URL + đoạn). Dấu ✅ không phải trích dẫn.

| # | Luận điểm | Nhãn | Nguồn | Vị trí |
|---|---|---|---|---|
```

`skills/book/book-to-learn/references/templates/learning-kit.md`:
```markdown
# Learning Kit — <tên sách>

Soạn từ `/analyze` Phần 3 cho từng framework ứng viên. Câu hỏi Feynman ở đây KHÔNG kèm đáp án — CEO tự trả lời ở cổng L4.

## <Framework>
### Chunking — cây phụ thuộc
<!-- Ghi rõ chỗ thứ tự phụ thuộc khác thứ tự tác giả trình bày. -->
### Feynman — 3 câu hỏi
- Q1 Hiểu:
- Q2 Áp dụng vào Workshop X:
- Q3 Tầng hệ thống (vòng lặp/điểm nghẽn/đòn bẩy):
### Mnemonic
### Rubric hành vi (1–5)
| Chỉ báo hành vi | 1 | 3 | 5 |
|---|---|---|---|
### Drill
### Câu hỏi journal (≥1 về vòng lặp phản hồi, ≥1 về cách học)
```

`skills/book/book-to-learn/references/templates/feynman.md`:
```markdown
---
framework:
tac_gia: CEO
---
# Cổng Feynman

CEO tự viết. Mỗi câu trả lời ≥ 40 từ, không thuật ngữ. Câu hỏi để dạng trích dẫn (>), trả lời ngay dưới.

## Q1 — Hiểu
>

## Q2 — Áp dụng
>

## Q3 — Tầng hệ thống
>

## Rubric tự chấm
| Chỉ báo hành vi | Mức |
|---|---|
```

`skills/book/book-to-learn/references/templates/experiment-card.md`:
```markdown
---
framework:
gia_thuyet:
chi_so:
baseline:
nguong:
nguoi_chiu_trach_nhiem:
ngay_bat_dau:
ngay_ket_thuc:
du_doan:
don_vi_framework:
don_vi_thi_nghiem:
muc_tin_cay_du_lieu:
ceo_duyet:
---
# Thẻ thí nghiệm — DMIR

## D — Diagnose
- Ranh giới hệ:
- Archetype (từ /archetype):
- Mô hình tư duy cần chất vấn:

## M — Model
- CLD (từ /cld): <đường dẫn>
- Biến 1: hiện tại → mục tiêu
- Biến 2: hiện tại → mục tiêu
- Biến 3: hiện tại → mục tiêu

## I — Intervene
- Điểm nghẽn (từ /constraint):
- Mức đòn bẩy của can thiệp (từ /leverage):
- Can thiệp cụ thể:
- Nhãn Claims của framework (SUPPORTED/CONTESTED/CẦN-CHUYỂN-VN/CHƯA KIỂM) và rủi ro:

## R — Dự đoán ghi trước
<!-- Lặp lại du_doan ở trên bằng con số; không sửa sau khi ceo_duyet. -->
```

`skills/book/book-to-learn/references/templates/run-log.md`:
```markdown
# Run Log — <slug>

| Ngày | Quan sát | Số đo | Điểm nghẽn còn đó? |
|---|---|---|---|
```

`skills/book/book-to-learn/references/templates/aar.md`:
```markdown
---
quyet_dinh:
---
# AAR — <slug>

<!-- quyet_dinh: keep | adapt | drop -->

## Định xảy ra gì

## Thực tế ra sao

## Vì sao khác

## Lần sau làm gì

## Vòng kép
- Mục tiêu (L3) có sai không:
- Mô hình tư duy (L2) nào bị lật:

## Ứng viên Galaxy
<!-- Chỉ ĐỀ XUẤT. Chạy galaxy-gate và đối chiếu 5_Galaxy trước. AI không tự tạo ghi chú. -->

## Lỗi của chính pipeline → skill-backlog.md
```

`skills/book/book-to-learn/references/templates/cycles-row.json`:
```json
{"slug": "", "opened": "", "closed": "", "target": null, "dreyfus_before": 0, "dreyfus_after": 0, "leverage_reached": "", "perkins": "", "applied": false, "decision": "", "prediction_hits": 0, "prediction_total": 3, "days_to_competence": 0, "techniques": {}, "illusion_gap": 0.0, "book_type": "", "failure_points": [], "next_book_hint": ""}
```

- [ ] **Step 4: Run tests**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_templates.py scripts/test_btl_gate_check.py -v`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add skills/book/book-to-learn/references/templates scripts/test_btl_templates.py
git commit -m "[BOOK] book-to-learn: khuôn tạo tác + test khớp tên trường với cổng máy

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 7: References — dmir-unified.md and phase-contracts.md

**Files:**
- Create: `skills/book/book-to-learn/references/dmir-unified.md`
- Create: `skills/book/book-to-learn/references/phase-contracts.md`

**Interfaces:**
- Consumes: template file names (Task 6), CLI flags (Tasks 1–5)
- Produces: files referenced by path from SKILL.md (Task 8)

- [ ] **Step 1: Create `dmir-unified.md`** (exact content)

```markdown
# DMIR hợp nhất — tham chiếu cho /book-to-learn

## Nguồn và cảnh báo
- Nguồn: 3 tài liệu CEO cung cấp 2026-09-17 — *D-M-I-R × ODI × Engineering Design (Pahl & Beitz)* v1.0; *The D-M-I-R Unified Model for Systemic Change: A Deep Dive*; *Unified Model for Systemic Change (D–M–I–R) — Deep Research & Playbook v1.0 (02/11/2025)*. Bối cảnh vault: `2_Areas/CEO-Self/Learning-Architecture/DMIR_Skill_Architecture_v2.md`.
- Chỉ dùng **cấu trúc, câu hỏi, template**. Các con số trong tài liệu gốc không có nguồn kiểm được ("70% nỗ lực thay đổi thất bại", "nhanh hơn 15 lần", "ROI 10–50x", các case ghi "giả lập") — **không trích như sự thật**.
- Tên: **Diagnose–Model–Intervene–Reflect**. `1_Projects/BB-01_LOMAH/References/dmir1…4` dùng Diagnose–Measure–Improve–Review — biến thể khác, không trộn.
- DMIR là **tầng meta**, không phải framework thứ tư cạnh BRIDGE/FORGE/HELIX.

## Bốn pha
| Pha | Trường phái | Câu hỏi chính | Skill KN-Stack | Đòn bẩy hay chạm |
|---|---|---|---|---|
| D | Systems Thinking | Ranh giới hệ ở đâu? Archetype nào đang chạy? Mô hình tư duy ngầm nào sinh ra hành vi này? | `/archetype`, `/cld` | L1–L4, L6 |
| M | System Dynamics | Stock nào, flow nào, trễ bao lâu, vòng R/B nào trội? Biến then chốt hiện tại → mục tiêu? | `/cld`, `/sdmodel` (chỉ khi CEO yêu cầu) | L7–L10 |
| I | Theory of Constraints | Điểm nghẽn là gì? Khai thác → phối thuộc → nâng cấp → quay lại? Can thiệp ở mức đòn bẩy nào? | `/constraint`, `/leverage` | L5, L10 |
| R | Meta-learning | Định xảy ra gì / thực tế / vì sao khác / lần sau? Mục tiêu (L3) và mô hình tư duy (L2) có sai? | `/reflect`, `/paradigm` | L1–L3 |

## DMIR bản nhẹ cho chu kỳ 30 ngày
- D + M tối đa 2 phiên. M = 1 CLD + 3 biến có số hiện tại → mục tiêu. Không dựng mô hình SD trừ khi CEO yêu cầu.
- I = một can thiệp, một chỉ số, baseline là số, thời lượng ≤ 16 ngày, dự đoán ghi trước.
- R = AAR 4 câu + vòng kép + cập nhật sổ meta.

## Thang đòn bẩy Meadows
L12 tham số · L11 buffer · L10 cấu trúc stock/flow · L9 độ trễ · L8 vòng cân bằng · L7 vòng tăng cường · L6 dòng thông tin · L5 luật chơi · L4 tự tổ chức · L3 mục tiêu · L2 paradigm · L1 vượt paradigm.
Qua các chu kỳ, mục tiêu là leo dần: L10 → L6 → L5 → L3 → L2.
Ví dụ gán mức cho framework của sách (Profit First): tỉ lệ phân bổ % = L12; "Doanh thu − Lợi nhuận = Chi phí" = L5; hỏi "lành mạnh?" thay vì "to cỡ nào?" = L3.

## Archetype cần nhận diện (D)
Fixes That Fail · Shifting the Burden · Limits to Growth · Success to the Successful · Escalation · Tragedy of the Commons · Drift to Low Performance · Seeking the Wrong Goal (Goodhart) · Rule Beating · Policy Resistance.

## Năm bước tập trung TOC (I)
1 Xác định điểm nghẽn · 2 Khai thác (chưa thêm năng lực) · 3 Phối thuộc mọi thứ khác theo điểm nghẽn · 4 Nâng cấp (tốn tiền — làm sau 2 và 3) · 5 Điểm nghẽn dời thì quay lại bước 1, tránh quán tính.

## AAR và học vòng kép (R)
- AAR: Định xảy ra gì · Thực tế ra sao · Vì sao khác · Lần sau làm gì.
- Vòng đơn: sửa hành động trong giả định cũ. Vòng kép: chất vấn mục tiêu và luật chơi. Deutero-learning: học từ chính các lần học.
- Mức siêu nhận thức Perkins: tacit → aware → strategic → reflective.

## Học cách học (meta-learning trong từng cuốn)
Nguồn: `3_Resources/Tools & Software/Skills/deep-content-analyzer-v3/` Phần 3 (KN-Stack: `/analyze`) và `5_Skills_AI_Cant_Replace_Multi_Framework_Analysis.md`.

| Kỹ thuật | Tiêu chí chất lượng | Skill |
|---|---|---|
| Chunking | Ghi chỗ thứ tự phụ thuộc ≠ thứ tự trình bày | `learn-methodology` |
| Feynman | 60 giây + phép so sánh + 3 câu: hiểu → áp dụng → tầng hệ thống | `learn-methodology` |
| Mnemonic | Mỗi chữ là một hành động | `learn-methodology` |
| Rubric | Chỉ báo hành vi, không phải kiến thức | `learn-track` |
| Drill | Nhắm framework đòn bẩy cao nhất hoặc chỗ hay sai | `learn-practice` |
| Interleaving | Không hai khối liền nhau cùng chủ đề; khối sách xen việc thật | `learn-practice` |
| Journal | ≥1 câu về vòng lặp phản hồi, ≥1 câu về cách học | `learn-track` |
| Ôn giãn cách + đoán trước | Lệch đoán–thực ghi thành số | `learn-teach` |

## Meta-learning là một stock
- Đơn vị: tốc độ thích nghi — trong skill đo bằng `days_to_competence` (L0 → thẻ L5 được duyệt).
- Dòng vào: luyện tập siêu nhận thức có chủ đích; trải nghiệm đa dạng. Dòng ra: tự mãn.
- Vòng R4 lợi thế học tập cộng dồn: học nhanh → sớm có năng lực → việc thú vị hơn → đa dạng hơn → học nhanh hơn. Mức đòn bẩy L2.

## Khi KHÔNG dùng DMIR đầy đủ
Vấn đề đơn giản, nhân quả rõ; khủng hoảng cần hành động ngay (làm trước, DMIR sau); ràng buộc thật là ý chí chính trị bên ngoài.
```

- [ ] **Step 2: Create `phase-contracts.md`** (exact content)

````markdown
# Hợp đồng từng pha — /book-to-learn

Biến dùng dưới đây: `VAULT=D:\Workshop_X`, `SLUG=<slug>`, `LEARN=$VAULT/1_Projects/LEARN-<slug>`, `BOOK=$VAULT/3_Resources/Books/<slug>`, `KN=D:\KN-Stack`.
Cổng máy: `python "$KN/scripts/btl_gate_check.py" "$LEARN" <pha> [cờ]` — exit 0 mới được đánh dấu xong.

| Pha | Đầu vào | Đầu ra | Gọi | Lệnh cổng |
|---|---|---|---|---|
| L0 | file sách, `--target` | `LEARN/_Project_Brief.md` (khuôn `mission.md`), `LEARN/_pipeline_state.md` (khuôn `pipeline-state.md`, điền slug, started) | đọc `Status.md` dự án đích | `btl_gate_check.py "$LEARN" L0` |
| L1 | file sách | `~/.claude/skills/<slug>/`, `BOOK/Leverage_Map.md`, `BOOK/Learning_Kit.md` | `book-to-skill` (DEPTH=study), `/analyze` Phần 3 | `… L1` |
| L2 | `BOOK/_source/*` (mỗi chương một tệp, tên tệp = title nguồn) | notebook `btl-<slug>-goc`, `LEARN/_nlm/list.json`, `LEARN/_nlm/content/<id>.json` | `nlm notebook create`, `nlm source add --file`, `nlm source list -j`, `nlm source content -j` | `… L2 --nlm-list "$LEARN/_nlm/list.json" --nlm-content-dir "$LEARN/_nlm/content"` |
| L3 | câu hỏi 4 hướng | notebook `btl-<slug>-mo-rong`, `BOOK/Claims.md` | `/research` ×4 | `… L3` |
| L4 | `framework_ung_vien` | `LEARN/learn/` (bài học, RETRIEVAL.md), `LEARN/learn/feynman-<framework>.md` | `learn-methodology`, `learn-practice`, `learn-track`; CEO tự gõ `/learn-teach` | `… L4` |
| L5 | Claims, Leverage_Map, dữ liệu thật dự án đích | `LEARN/Experiment_Card.md` | `/archetype`, `/cld`, `/constraint`, `/leverage` | `… L5` |
| L6 | thẻ đã duyệt | `LEARN/Run_Log.md`, cảnh báo trong `LEARN/Status.md` | — | (không có cổng máy) |
| L7 | Run_Log, thẻ | `LEARN/AAR.md`, dòng `VAULT/2_Areas/CEO-Self/Learning-Meta/cycles.jsonl`, `calibration.md`, `transfer-map.md`, `skill-backlog.md` | `/reflect`, `/paradigm`, `galaxy-gate` | `… L7` |

## Tải JSON cho cổng L2

```bash
mkdir -p "$LEARN/_nlm/content"
nlm source list "$NOTEBOOK_GOC" -j > "$LEARN/_nlm/list.json"
python - "$LEARN" <<'PY'
import json, subprocess, sys, pathlib
learn = pathlib.Path(sys.argv[1])
for item in json.loads((learn / "_nlm" / "list.json").read_text(encoding="utf-8")):
    out = learn / "_nlm" / "content" / f"{item['id']}.json"
    out.write_text(subprocess.run(["nlm", "source", "content", item["id"], "-j"],
                                  capture_output=True, text=True, encoding="utf-8").stdout,
                   encoding="utf-8")
PY
```
````

- [ ] **Step 3: Verify no arg-substitution hazard and paths exist**

Run:
```bash
cd /d/KN-Stack-btl && python - <<'PY'
import re, pathlib
for p in pathlib.Path("skills/book/book-to-learn/references").glob("*.md"):
    t = p.read_text(encoding="utf-8")
    assert not re.search(r"\$[0-9](?![0-9])", t), p
    for tpl in re.findall(r"`([a-z-]+\.(?:md|json))`", t):
        if tpl in {"mission.md","pipeline-state.md","feynman.md","experiment-card.md","aar.md","claims.md","learning-kit.md","leverage-map.md","run-log.md","cycles-row.json"}:
            assert (pathlib.Path("skills/book/book-to-learn/references/templates")/tpl).exists(), tpl
print("ok")
PY
```
Expected: `ok`.

- [ ] **Step 4: Commit**

```bash
cd /d/KN-Stack-btl && git add skills/book/book-to-learn/references/dmir-unified.md skills/book/book-to-learn/references/phase-contracts.md
git commit -m "[BOOK] book-to-learn: tham chiếu DMIR hợp nhất (có cảnh báo số chưa kiểm) + hợp đồng từng pha

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 8: Orchestrator SKILL.md + static eval + mutation test

**Files:**
- Create: `skills/book/book-to-learn/SKILL.md`
- Create: `evals/book-to-learn.json`
- Test: `scripts/test_btl_eval.py`

**Interfaces:**
- Consumes: everything above (paths, flags, template names, gate commands)
- Produces: the invocable skill `/book-to-learn`

- [ ] **Step 1: Write the eval spec and the mutation test first**

Create `evals/book-to-learn.json`:

```json
{
  "skill": "book-to-learn",
  "version": "1.0",
  "description": "Binary assertions for /book-to-learn — orchestrator học sách → ứng dụng đo được trong ~30 ngày",
  "mode": "static",
  "test_input": "book to learn Profit First target VN-TGT-F",
  "assertions": [
    {"id": "BTL-PHASES", "name": "phases_L0_to_L7", "check": "defines phases L0..L7", "regex": "L7 Retro", "required": true},
    {"id": "BTL-GATE", "name": "gate_script", "check": "calls the machine gate checker", "regex": "btl_gate_check\\.py", "required": true},
    {"id": "BTL-L0", "name": "real_problem_block", "check": "L0 blocks without a real Workshop X problem", "regex": "vấn đề thật", "required": true},
    {"id": "BTL-FEYNMAN", "name": "feynman_gate", "check": "Feynman gate before L5, CEO-authored", "regex": "cổng Feynman", "required": true},
    {"id": "BTL-CARD", "name": "experiment_card", "check": "L5 produces an experiment card", "regex": "Experiment_Card\\.md", "required": true},
    {"id": "BTL-DMIR", "name": "dmir_definition", "check": "DMIR = Diagnose-Model-Intervene-Reflect", "regex": "Diagnose.{1,3}Model.{1,3}Intervene.{1,3}Reflect", "required": true},
    {"id": "BTL-DMIR-SKILLS", "name": "dmir_skills", "check": "delegates to DMIR skills", "regex": "/archetype.{0,40}/cld", "required": true},
    {"id": "BTL-TOC", "name": "toc_skills", "check": "uses constraint and leverage skills", "regex": "/constraint.{0,40}/leverage", "required": true},
    {"id": "BTL-LEARN-M", "name": "learn_methodology", "check": "uses learn-methodology", "regex": "learn-methodology", "required": true},
    {"id": "BTL-LEARN-P", "name": "learn_practice", "check": "uses learn-practice", "regex": "learn-practice", "required": true},
    {"id": "BTL-LEARN-T", "name": "learn_track", "check": "uses learn-track", "regex": "learn-track", "required": true},
    {"id": "BTL-TEACH-MANUAL", "name": "learn_teach_manual", "check": "CEO runs /learn-teach manually", "regex": "tự gõ `?/learn-teach", "required": true},
    {"id": "BTL-ANALYZE", "name": "analyze_meta_learning", "check": "uses /analyze part 3", "regex": "/analyze", "required": true},
    {"id": "BTL-META", "name": "meta_ledger", "check": "writes cycles.jsonl", "regex": "cycles\\.jsonl", "required": true},
    {"id": "BTL-NO-PERSONA", "name": "no_nlm_persona", "check": "forbids chat_configure custom goal", "regex": "chat_configure", "required": true},
    {"id": "BTL-NO-PUBLIC", "name": "no_public_share", "check": "notebooks never shared publicly", "regex": "không bao giờ share public", "required": true},
    {"id": "BTL-GROUNDING", "name": "sources_used_check", "check": "rejects answers with sources_used 0", "regex": "sources_used", "required": true},
    {"id": "BTL-QUICK", "name": "quick_flag_limits", "check": "--quick cannot skip L0/Feynman/L5/L7", "regex": "--quick", "required": true},
    {"id": "BTL-GALAXY", "name": "galaxy_gate", "check": "Galaxy candidates via galaxy-gate", "regex": "galaxy-gate", "required": true},
    {"id": "BTL-REFS", "name": "references", "check": "links reference files", "regex": "references/(dmir-unified|phase-contracts)\\.md", "required": true},
    {"id": "BTL-VN-NUMBERS", "name": "source_context_numbers", "check": "book figures stay in source context", "regex": "CẦN-CHUYỂN-VN", "required": false}
  ],
  "passing_score": 20,
  "total_required": 20,
  "total_optional": 1
}
```

Create `scripts/test_btl_eval.py`:

```python
"""Kiểm chính eval book-to-learn bằng đột biến: với mỗi assertion bắt buộc,
xoá khỏi SKILL.md mọi dòng khớp regex của NÓ thì assertion đó phải trượt.
(Chọn câu để xoá bằng tay luôn sót vì mỗi luật nằm 3–4 chỗ.)"""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "book" / "book-to-learn" / "SKILL.md"
EVAL = json.loads((ROOT / "evals" / "book-to-learn.json").read_text(encoding="utf-8"))
REQUIRED = [a for a in EVAL["assertions"] if a["required"]]


def test_counts_consistent():
    assert EVAL["total_required"] == len(REQUIRED)
    assert EVAL["total_optional"] == len(EVAL["assertions"]) - len(REQUIRED)


def test_all_required_pass_on_skill():
    text = SKILL.read_text(encoding="utf-8")
    missing = [a["id"] for a in REQUIRED if not re.search(a["regex"], text, re.I)]
    assert missing == []


@pytest.mark.parametrize("a", REQUIRED, ids=[a["id"] for a in REQUIRED])
def test_mutation_kills_assertion(a):
    text = SKILL.read_text(encoding="utf-8")
    rx = re.compile(a["regex"], re.I)
    mutated = "\n".join(l for l in text.splitlines() if not rx.search(l))
    assert not rx.search(mutated), f"{a['id']} regex spans lines — mutation cannot remove it"


def test_no_arg_substitution_hazard():
    for i, line in enumerate(SKILL.read_text(encoding="utf-8").splitlines(), 1):
        assert not re.search(r"\$[0-9](?![0-9])", line), f"SKILL.md dòng {i}: {line}"
```

- [ ] **Step 2: Run to verify fail**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_eval.py -v`
Expected: FAIL — `FileNotFoundError` for SKILL.md.

- [ ] **Step 3: Create `skills/book/book-to-learn/SKILL.md`** (exact content)

````markdown
---
name: book-to-learn
description: "Orchestrator học một cuốn sách đến mức ỨNG DỤNG ĐO ĐƯỢC vào Workshop X trong chu kỳ ~30 ngày: L0 mission (vấn đề thật + 3 dự đoán) → L1 trích cấu trúc (book-to-skill, /analyze) → L2 NotebookLM toàn văn theo chương → L3 mở rộng 4 hướng (phản biện, bối cảnh VN, bản mới, tri thức sẵn có) → L4 học cách học (chunking, Feynman, drill, interleaving, journal, rubric, ôn giãn cách) + cổng Feynman → L5 thẻ thí nghiệm DMIR → L6 chạy thật → L7 AAR + sổ meta-learning xuyên sách. Mọi cổng do scripts/btl_gate_check.py kiểm. Triggers on: 'book to learn', 'học sách', 'học một cuốn sách', 'áp dụng sách vào công việc', 'đọc hiểu thực hành ứng dụng', 'biến sách thành hành động', 'meta-learning sách', 'learn from book', 'apply book to business'."
argument-hint: "<file|thư mục sách> [--slug X] [--target <dự án>] [--notebook <id>] [--from Ln] [--only Ln] [--resume] [--quick]"
---

# /book-to-learn — Học sách đến ứng dụng đo được

> **Đích:** một chu kỳ chỉ XONG khi có ≥1 thí nghiệm ứng dụng vào vấn đề thật của Workshop X, được CEO duyệt, chạy thật, đo được, đóng vòng DMIR-R. Chu kỳ không có thí nghiệm vẫn đóng, nhưng ghi `applied:false` — không bao giờ gọi là "xong".
> **Spec:** `docs/superpowers/specs/2026-09-17-book-to-learn-design.md` · **Hợp đồng pha:** [references/phase-contracts.md](references/phase-contracts.md) · **DMIR + học cách học:** [references/dmir-unified.md](references/dmir-unified.md)

## Quy tắc cứng (đọc trước khi làm bất cứ gì)

1. **Cổng máy.** Không đánh dấu pha nào xong khi `python D:/KN-Stack/scripts/btl_gate_check.py <LEARN-dir> <pha>` chưa exit 0. Script tự ghi dấu vào `_pipeline_state.md`. Không tự tay thêm dòng `PASS`.
2. **DMIR = Diagnose–Model–Intervene–Reflect** (tầng meta). Bản nhẹ: D+M tối đa 2 phiên; `/sdmodel` chỉ khi CEO yêu cầu. Không trích các con số chưa có nguồn của tài liệu DMIR như sự thật.
3. **NotebookLM:** cấm `chat_configure` với goal tuỳ chỉnh (persona làm mất nền truy hồi). Mỗi truy vấn mở conversation mới; loại câu trả lời có `sources_used` = 0; số liệu NLM trả về phải grep lại trong `_source/` với `LC_ALL=C.UTF-8`, thử nhiều cách viết, và tự kiểm lại mình trước khi kết luận NLM sai. Hai lỗi nhanh liên tiếp (4–6 giây) → dừng, nghi hạn mức. Không tin kết quả in ra của `nlm source add`.
4. **Bản quyền:** notebook `btl-*` không bao giờ share public; `_source/` chỉ nằm trong vault; không chép nguyên văn dài. Chương bị loại khỏi NLM: không ghi lý do loại vào manifest hay truy vấn.
5. **Số liệu sách giữ bối cảnh gốc** (tiền tệ, luật, quy mô). Dùng ở VN phải có dòng CẦN-CHUYỂN-VN trong Claims.
6. **Quyết định CEO ghi bằng chữ đầy đủ**, không bằng nhãn (A)/(B).
7. **Galaxy:** chỉ đề xuất; qua `galaxy-gate` và đối chiếu `5_Galaxy` trước. AI không tự tạo ghi chú.
8. **Sửa ở tệp nguồn** (Brief, Claims, Learning_Kit), không vá vào tệp dựng ra.
9. **Không viết ký hiệu đô-la liền một chữ số** trong bất kỳ SKILL.md nào sinh ra (bộ nạp skill thay nó bằng tham số) — viết "USD 0–250K".

## Đường dẫn

```
VAULT = D:\Workshop_X
LEARN = VAULT\1_Projects\LEARN-<slug>\          chu kỳ học (dự án PARA)
BOOK  = VAULT\3_Resources\Books\<slug>\         tri thức bền: _source/, Leverage_Map.md, Claims.md, Learning_Kit.md
SKILL = ~\.claude\skills\<slug>\                skill tri thức
META  = VAULT\2_Areas\CEO-Self\Learning-Meta\   cycles.jsonl, calibration.md, transfer-map.md, skill-backlog.md
TPL   = D:\KN-Stack\skills\book\book-to-learn\references\templates\
```

## Phân tích lệnh

- Đối số đầu: đường dẫn sách (hoặc bỏ trống khi có `--notebook` / `--resume`).
- `--slug`: mặc định kebab-case từ tên sách.
- `--target <dự án>`: thư mục trong `1_Projects`.
- `--resume`: đọc `LEARN/_pipeline_state.md`, chạy pha đầu tiên chưa có dòng PASS.
- `--from Ln` / `--only Ln`: bắt đầu tại / chỉ chạy pha đó (vẫn chạy cổng).
- `--quick`: bỏ L3 và đặt `quick: true`. **Không bỏ được L0, cổng Feynman L4, L5, L7.** Mọi framework bị gắn nhãn CHƯA KIỂM trong thẻ L5.

## Các pha

| Pha | Ngày | COD | Cổng |
|---|---|---|---|
| L0 Mission | 0 | C | chặn cứng nếu thiếu vấn đề thật |
| L1 Trích | 1–2 | O | máy |
| L2 NLM | 2 | O | máy |
| L3 Mở rộng | 3–6 | O, C duyệt nguồn | máy + CEO |
| L4 Học + cổng Feynman | 3–10 | O+C | máy (câu trả lời do CEO viết) |
| L5 Thiết kế thí nghiệm | 8–12 | O soạn, C chọn | máy + CEO duyệt |
| L6 Chạy thật | 12–28 | C | nhắc trễ hạn |
| L7 Retro | 28–30 | O soạn, C quyết | máy + CEO |

L0 → L1 → L2 chạy liền. L3 (máy, nền) song song L4 (phiên CEO). L5 cần L3 và cổng Feynman.

### L0 Mission — vấn đề thật trước, sách sau
1. Nếu có `--target`: đọc `VAULT/1_Projects/<target>/Status.md` trước.
2. Tạo `LEARN/`; chép `TPL/pipeline-state.md` → `LEARN/_pipeline_state.md` (điền `slug`, `started`); chép `TPL/mission.md` → `LEARN/_Project_Brief.md`; chép `TPL/run-log.md` → `LEARN/Run_Log.md`; tạo `LEARN/Status.md` theo chuẩn dự án Tier 3.
3. Hỏi CEO (một câu một lần): vấn đề/quyết định thật của Workshop X mà cuốn sách phải phục vụ → `van_de_that`; 3 dự đoán về nội dung sách → `du_doan_1..3`; tự chấm Dreyfus 1–5 → `dreyfus_truoc`; `target` hoặc `noi_ap_dung`; tiêu chí thành công bằng số.
4. Không có vấn đề thật → DỪNG, không mở chu kỳ.
5. Cổng: `python D:/KN-Stack/scripts/btl_gate_check.py "LEARN" L0`

### L1 Trích cấu trúc
1. Chạy `book-to-skill` với DEPTH=study, lưu vào `SKILL`. Nếu skill đã có: rà theo quy tắc 9 và dùng lại.
2. Chép `TPL/leverage-map.md` → `BOOK/Leverage_Map.md`; gán mỗi framework một mức L1–L12 kèm lý do (xem thang trong dmir-unified.md).
3. Chạy `/analyze` Phần 3 (Meta-Learning) cho các framework đáng áp dụng; chép `TPL/learning-kit.md` → `BOOK/Learning_Kit.md`. Câu hỏi Feynman **không kèm đáp án**.
4. Cổng: `… L1`. Sau đó CEO chọn `framework_ung_vien` trong `_pipeline_state.md`.

### L2 NotebookLM — toàn văn theo chương
1. Tách chương vào `BOOK/_source/ch<NN>-<slug>.md`.
2. Tạo notebook `btl-<slug>-goc` (hoặc dùng `--notebook`); `nlm source add --file` từng chương. Ghi id vào `notebook_goc`.
3. Tải JSON theo `references/phase-contracts.md` mục "Tải JSON cho cổng L2".
4. Truy vấn thử 1 câu có đáp án biết trước trong một conversation mới; kiểm `sources_used` > 0.
5. Cổng: `… L2 --nlm-list "LEARN/_nlm/list.json" --nlm-content-dir "LEARN/_nlm/content"`

### L3 Mở rộng 4 hướng
1. Soạn 4 câu hỏi `/research`: (a) phản biện & bằng chứng, case thất bại, chỗ tác giả đổi quan điểm; (b) chuyển bối cảnh VN — luật, thuế, chuẩn, quốc phòng; (c) bản mới & tác phẩm sau của tác giả; (d) nối tri thức sẵn có — `5_Galaxy`, `mentor-board`, sách đã học (`META/transfer-map.md`).
2. **CEO duyệt danh sách nguồn trước khi nạp** vào notebook `btl-<slug>-mo-rong` (tách khỏi notebook gốc).
3. Chép `TPL/claims.md` → `BOOK/Claims.md`; mỗi luận điểm chính của sách một dòng với nhãn SUPPORTED / CONTESTED / CẦN-CHUYỂN-VN, nguồn và vị trí.
4. Cổng: `… L3`

### L4 Học cách học + cổng Feynman
Chỉ cho `framework_ung_vien`. Trình tự:
1. **Chunking** và **Feynman** — `learn-methodology` (dùng Learning_Kit).
2. **Drill** và **interleaving** — `learn-practice`; khối học sách xen khối việc thật của Workshop X, không hai khối liền nhau cùng chủ đề.
3. **Journal** và **rubric hành vi** — `learn-track`; journal có ≥1 câu về vòng lặp phản hồi, ≥1 câu về cách học.
4. Bài học tương tác + ôn giãn cách + đoán-trước-rồi-thử: `learn-teach` có `disable-model-invocation`, nên **CEO tự gõ `/learn-teach`** trong thư mục `LEARN/learn/` (MISSION đã có sẵn từ L0).
5. Nhịp micro-DMIR hằng tuần: D thứ Hai (khái niệm nào đang chặn việc thật) → M thứ Ba (vòng phản hồi học của tôi nhanh hay chậm) → I thứ Tư–Sáu (áp một khía cạnh) → R cuối tuần (journal).
6. **Cổng Feynman:** với mỗi framework ứng viên, chép `TPL/feynman.md` → `LEARN/learn/feynman-<framework>.md`. **CEO tự viết** 3 câu trả lời (≥ 40 từ mỗi câu) và tự chấm rubric. AI không điền. Cổng: `… L4`

### L5 Thiết kế thí nghiệm — DMIR
Chép `TPL/experiment-card.md` → `LEARN/Experiment_Card.md`.
1. **D:** `/archetype` rồi `/cld` trên tình huống thật của dự án đích (số thật, không số giả định).
2. **M:** 3 biến có giá trị hiện tại → mục tiêu. Tối đa 2 phiên cho D+M.
3. **I:** `/constraint` rồi `/leverage`; chọn một can thiệp; ghi mức đòn bẩy; framework phải nằm trong `framework_ung_vien`; nêu nhãn Claims và rủi ro nếu CONTESTED/CẦN-CHUYỂN-VN/CHƯA KIỂM.
4. Điền đủ ô: giả thuyết, chỉ số, baseline là số, ngưỡng, người chịu trách nhiệm, ngày bắt đầu/kết thúc (≤ 16 ngày), dự đoán ghi trước, đơn vị phân tích của framework = của thí nghiệm, mức tin cậy dữ liệu L1–L5.
5. CEO duyệt → điền `ceo_duyet`. Chỉ khi CEO đồng ý mới thêm một dòng liên kết tới thẻ vào dự án đích.
6. Cổng: `… L5`

### L6 Chạy thật
Mỗi ngày 10 và 25: nhắc CEO ghi `LEARN/Run_Log.md` và hỏi "điểm nghẽn còn đó không?". Quá `ngay_ket_thuc` chưa có số đo → ghi cảnh báo vào `LEARN/Status.md`.

### L7 Retro — AAR, vòng kép, sổ meta
1. Chép `TPL/aar.md` → `LEARN/AAR.md`; `/reflect` soạn 4 mục AAR từ Run_Log; `/paradigm` cho mục vòng kép (mục tiêu L3, mô hình tư duy L2).
2. CEO quyết `quyet_dinh`: keep / adapt / drop.
3. Nối một dòng vào `META/cycles.jsonl` (tạo tệp nếu chưa có) theo `TPL/cycles-row.json`: Dreyfus trước/sau (CEO chấm lại), mức đòn bẩy chạm tới, Perkins, `applied`, `decision`, số dự đoán trúng/3, `days_to_competence` (L0 → ngày `ceo_duyet`), điểm hữu ích từng kỹ thuật học 1–5, `illusion_gap` (lệch đoán–thực trong RETRIEVAL.md), `book_type`, điểm rơi, gợi ý sách kế tiếp. Thẻ L5 chưa qua cổng → `applied:false`.
4. Cập nhật (tạo mới nếu chưa có, kể cả thư mục `META/` và `cycles.jsonl`) `META/calibration.md` (dự đoán vs thực tế), `META/transfer-map.md` (framework sách này ↔ sách trước; kỹ thuật học nào hợp loại sách nào), `META/skill-backlog.md` (lỗi của chính pipeline này).
5. Ứng viên Galaxy: đối chiếu `5_Galaxy` trước, chạy `galaxy-gate`, chỉ đề xuất.
6. Gợi ý cuốn kế tiếp từ `transfer-map.md` và lỗ hổng năng lực lộ ra; CEO chọn.
7. Cổng: `… L7`. Xong chu kỳ → đề xuất chuyển `LEARN-<slug>` sang `4_Archives` (hỏi CEO trước).

## Báo cáo cuối mỗi phiên
- Pha vừa qua cổng (dán dòng PASS/FAIL của script).
- Việc CEO cần làm tiếp, kèm COD.
- Ngày của mốc kế tiếp (L5 duyệt, ngày kết thúc thí nghiệm, ngày retro).
````

- [ ] **Step 4: Run tests and the eval runner**

Run: `cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_eval.py scripts/test_btl_templates.py scripts/test_btl_gate_check.py -v`
Expected: all PASS.

Run: `cd /d/KN-Stack-btl && bash evals/run-eval.sh book-to-learn`
Expected: `Required passed: 20 / 20`. If the runner resolves the skill path from the main checkout instead of the worktree, run it with the worktree as cwd, and if it still fails report the path it printed. Do not edit `run-eval.sh`.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack-btl && git add skills/book/book-to-learn/SKILL.md evals/book-to-learn.json scripts/test_btl_eval.py
git commit -m "[BOOK] book-to-learn: orchestrator SKILL.md + eval static 20 assertion + test đột biến

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>"
```

---

### Task 9: Full verification + PR description (no push without CEO approval)

**Files:**
- Create (untracked, not committed): `C:\Users\Admin\AppData\Local\Temp\claude\d--KN-Stack\9d366432-63a3-467b-874a-c54bd11b4b79\scratchpad\pr-book-to-learn.md`

- [ ] **Step 1: Run the full check suite**

```bash
cd /d/KN-Stack-btl && python -m pytest scripts/test_btl_gate_check.py scripts/test_btl_templates.py scripts/test_btl_eval.py -v
bash evals/run-eval.sh book-to-learn
bash setup.sh --status
git status --short
git diff origin/feature/evals-static-mode --stat
```
Expected: all tests PASS; eval `20 / 20`; `--status` counts the book domain one higher than before; `git status` clean; the diff touches only `docs/superpowers/{specs,plans}`, `scripts/btl_*`, `scripts/test_btl_*`, `skills/book/book-to-learn/**`, `evals/book-to-learn.json`. Do **not** run `setup.sh --install` from the worktree — junctions would point at `D:\KN-Stack-btl`.

- [ ] **Step 2: Confirm forbidden files untouched**

```bash
cd /d/KN-Stack-btl && git diff origin/feature/evals-static-mode --name-only | grep -E "^(VERSION|CHANGELOG\.md|CLAUDE\.md|scripts/_codify_ledger\.md)$" && echo "VIOLATION" || echo "clean"
```
Expected: `clean`.

- [ ] **Step 3: Write the PR description to the scratchpad**

Content:
```markdown
## Tóm tắt
Thêm `/book-to-learn`: orchestrator học một cuốn sách đến mức ứng dụng đo được vào Workshop X trong ~30 ngày (L0–L7), gọi lại book-to-skill, NLM, /research, /analyze, learn-*, bộ DMIR, galaxy-gate. Mọi cổng do `scripts/btl_gate_check.py` kiểm bằng máy.

## Kiểm thử
- pytest: `scripts/test_btl_gate_check.py`, `scripts/test_btl_templates.py`, `scripts/test_btl_eval.py` — PASS
- `bash evals/run-eval.sh book-to-learn` — 20/20 bắt buộc
- Định dạng JSON `nlm source list -j` / `nlm source content -j` lấy từ notebook thật ngày 2026-09-17

## Việc của người merge
- Chạy `bash setup.sh --install` trên checkout chính sau khi merge
- Cập nhật số skill domain book trong CLAUDE.md
- Dán mục CHANGELOG dưới đây và chọn số version

## CHANGELOG
### Added
- `book-to-learn` (skills/book): orchestrator L0–L7 học sách → thí nghiệm ứng dụng DMIR → AAR + sổ meta-learning xuyên sách (`2_Areas/CEO-Self/Learning-Meta/cycles.jsonl`).
- `scripts/btl_gate_check.py`: cổng máy L0/L1/L2/L3/L4/L5/L7 — chặn thiếu vấn đề thật, bẫy `$<số>` trong SKILL.md, nguồn NLM rỗng/chặn bot, Claims không nguồn, câu trả lời Feynman không do CEO viết, thẻ thí nghiệm thiếu baseline số/quá 16 ngày/lệch đơn vị phân tích, `applied:true` khi chưa qua L5.
- Eval static `evals/book-to-learn.json` + test đột biến.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

- [ ] **Step 4: Report to CEO and STOP**

Report test output, eval score, and the PR draft path. Ask for approval before `git push -u origin feature/book-to-learn` and `gh pr create --base feature/evals-static-mode`.
````
