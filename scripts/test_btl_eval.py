"""Kiểm chính eval book-to-learn bằng đột biến: tách SKILL.md thành frontmatter
+ thân bài; với mỗi assertion bắt buộc, xoá khỏi THÂN BÀI (giữ nguyên
frontmatter) mọi dòng góp phần vào một khớp của regex đó trên TOÀN VĂN BẢN,
rồi assertion đó phải trượt trên văn bản đã ghép lại.

Tách frontmatter riêng để bắt lỗi assertion chỉ khớp nhờ từ khoá trong
description/argument-hint (frontmatter) chứ không nhờ nội dung hành vi thật
sự trong thân bài — nếu regex còn khớp sau khi thân bài đã bị xoá sạch phần
liên quan, nghĩa là frontmatter MỘT MÌNH đã đủ làm assertion đạt, không phải
điều pipeline thật sự bắt buộc.

Dùng vị trí khớp (không chỉ so từng dòng) để việc xoá đúng cho cả regex
xuyên nhiều dòng như `Cổng Feynman[\\s\\S]*### L5` — xoá mọi dòng mà khớp đi
qua, kể cả khi khớp bắt đầu trong frontmatter (frontmatter vẫn được giữ,
chỉ phần thân bài bị xoá)."""
import bisect
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "book" / "book-to-learn" / "SKILL.md"
EVAL = json.loads((ROOT / "evals" / "book-to-learn.json").read_text(encoding="utf-8"))
REQUIRED = [a for a in EVAL["assertions"] if a["required"]]

FRONTMATTER_RE = re.compile(r"\A(---\n.*?\n---\n)(.*)\Z", re.S)


def split_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    assert m, "SKILL.md phải bắt đầu bằng frontmatter --- ... ---"
    return m.group(1), m.group(2)


def _line_starts(text):
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)
    return starts


def _line_of(starts, pos):
    return bisect.bisect_right(starts, pos) - 1


def _lines_touched(full_text, rx):
    """Chỉ số dòng (0-based, trên full_text) bị chạm bởi bất kỳ khớp nào của rx."""
    starts = _line_starts(full_text)
    touched = set()
    for m in rx.finditer(full_text):
        a, b = m.start(), max(m.start(), m.end() - 1)
        touched.update(range(_line_of(starts, a), _line_of(starts, b) + 1))
    return touched


def mutate_body(frontmatter, body, rx):
    """Xoá khỏi body mọi dòng bị chạm bởi một khớp của rx trên (frontmatter+body);
    frontmatter luôn được giữ nguyên vẹn."""
    full = frontmatter + body
    touched = _lines_touched(full, rx)
    fm_line_count = frontmatter.count("\n")
    body_lines = body.splitlines(keepends=True)
    kept = [line for i, line in enumerate(body_lines) if (fm_line_count + i) not in touched]
    return frontmatter + "".join(kept)


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
    frontmatter, body = split_frontmatter(text)
    rx = re.compile(a["regex"], re.I)
    mutated = mutate_body(frontmatter, body, rx)
    assert not rx.search(mutated), (
        f"{a['id']} vẫn khớp sau khi xoá mọi dòng thân bài liên quan tới regex của nó — "
        f"assertion này có thể chỉ đạt nhờ frontmatter (description/argument-hint), "
        f"không phải nội dung hành vi trong thân bài"
    )


def test_no_arg_substitution_hazard():
    for i, line in enumerate(SKILL.read_text(encoding="utf-8").splitlines(), 1):
        assert not re.search(r"\$[0-9](?![0-9])", line), f"SKILL.md dòng {i}: {line}"
