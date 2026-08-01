"""Mutation harness cho eval tĩnh của plugin fluency-4d.

Eval tĩnh là regex soi SKILL.md. Chế độ hỏng của nó là **cổng-từ-khoá**: anchor
bắt một chữ quá phổ biến, nên rút ruột SKILL.md mà điểm vẫn xanh. Không có cách
nào phát hiện bằng mắt — phải đo.

Phép đo ở đây là **quét xoá từng dòng**: xoá lần lượt mỗi dòng của SKILL.md rồi
chấm lại toàn bộ assertion. Với mỗi assertion thu được "tập sát thủ" — những dòng
mà mất đi thì assertion đổ.

    tập sát thủ RỖNG   → assertion không neo vào nội dung nào. Cổng chết.
    tập sát thủ QUÁ TO → assertion đổ vì bất cứ thứ gì, không chỉ ra được điều gì.
    dòng không thuộc tập sát thủ nào → nội dung KHÔNG được cổng nào canh.

Vế cuối quan trọng ngang vế đầu: nó chỉ ra chỗ SKILL.md bị rút ruột mà eval im.

Chạy:  python scripts/fluency_4d_mutate.py [--json]
Thoát khác 0 nếu có assertion chết hoặc anchor không duy nhất.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS_DIR = REPO_ROOT / "evals"
SKILLS_ROOT = REPO_ROOT / "plugins" / "fluency-4d" / "skills"
SKILL_NAMES = ["fluency-4d-preflight", "fluency-4d-review", "fluency-4d-weekly"]

# Khoảng hở trong regex eval: [\s\S]{0,N} — dùng để tách các đoạn literal.
_GAP_RE = re.compile(r"\[\\s\\S\]\{\d+,\d+\}")
# Khoảng hở KHÔNG chặn trên: .* , [\s\S]* , [\s\S]+ , {0,} …
_UNBOUNDED_RE = re.compile(r"\[\\s\\S\]\s*[*+]|(?<!\\)\.\s*[*+]|\{\d+,\}")


def load_specs() -> dict[str, dict]:
    """Trả {tên skill: spec eval}."""
    out = {}
    for name in SKILL_NAMES:
        path = EVALS_DIR / f"{name}.json"
        out[name] = json.loads(path.read_text(encoding="utf-8"))
    return out


def load_skill(name: str) -> str:
    return (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")


def score(text: str, assertions: list[dict]) -> set[str]:
    """Trả tập id assertion ĐẠT trên đoạn văn bản này."""
    passed = set()
    for a in assertions:
        if re.search(a["regex"], text):
            passed.add(a["id"])
    return passed


# Độ dài tối thiểu để một đoạn được coi là anchor thực chất. Mảnh ngắn như
# '0', '>', 'không' vốn dĩ lặp khắp file — bắt chúng phải duy nhất là vô nghĩa.
MIN_ANCHOR_LEN = 8
_META = set("[](){}|^$+*?")


def literal_segments(regex: str) -> list[str]:
    """Tách các đoạn literal giữa những khoảng hở [\\s\\S]{0,N}.

    Chỉ giữ đoạn so thẳng được với nội dung file: đoạn nào còn ký tự regex
    CHƯA escape thì bỏ, vì nó không phải chuỗi ký tự thật.
    """
    segs = []
    for raw in _GAP_RE.split(regex):
        out, esc, ok = [], False, True
        for ch in raw:
            if esc:
                out.append(ch); esc = False
            elif ch == "\\":
                esc = True
            elif ch in _META:
                ok = False; break
            else:
                out.append(ch)
        seg = "".join(out)
        if ok and seg:
            segs.append(seg)
    return segs


def substantive_anchors(regex: str) -> list[str]:
    """Các đoạn đủ dài để gánh vai anchor."""
    return [s for s in literal_segments(regex) if len(s.strip()) >= MIN_ANCHOR_LEN]


def audit_uniqueness(text: str, assertions: list[dict]) -> list[tuple[str, str]]:
    """Mỗi assertion phải có ÍT NHẤT MỘT anchor thực chất và duy nhất trong file.

    Đòi mọi đoạn đều duy nhất là sai yêu cầu — regex nào cũng có mảnh nối ngắn.
    Điều thật sự cần là có một chỗ neo không thể khớp nhầm sang đoạn khác.

    Trả [(id assertion, lý do)] cho các assertion không đạt.
    """
    out = []
    for a in assertions:
        anchors = substantive_anchors(a["regex"])
        if not anchors:
            out.append((a["id"], f"không có đoạn literal nào dài ≥ {MIN_ANCHOR_LEN} ký tự"))
            continue
        uniq = [s for s in anchors if text.count(s) == 1]
        if not uniq:
            counts = ", ".join(f"{s.strip()!r}×{text.count(s)}" for s in anchors[:4])
            out.append((a["id"], f"không anchor nào duy nhất trong file ({counts})"))
    return out


def audit_gaps(assertions: list[dict]) -> list[tuple[str, str]]:
    """Khoảng hở không chặn trên = anchor có thể vắt qua cả file."""
    return [
        (a["id"], m.group(0))
        for a in assertions
        for m in _UNBOUNDED_RE.finditer(a["regex"])
    ]


def sweep(text: str, assertions: list[dict]) -> tuple[dict[str, set[int]], list[int]]:
    """Xoá từng dòng, chấm lại. Trả (tập sát thủ theo assertion, các dòng không được canh)."""
    lines = text.splitlines(keepends=True)
    kill: dict[str, set[int]] = {a["id"]: set() for a in assertions}
    for i in range(len(lines)):
        mutant = "".join(lines[:i] + lines[i + 1:])
        for aid in {a["id"] for a in assertions} - score(mutant, assertions):
            kill[aid].add(i)
    guarded = {i for s in kill.values() for i in s}
    unguarded = [
        i for i, ln in enumerate(lines)
        if i not in guarded and ln.strip() and not ln.strip().startswith("```")
    ]
    return kill, unguarded


def run() -> int:
    specs = load_specs()
    failures = 0
    report: dict[str, dict] = {}

    for name, spec in specs.items():
        assertions = spec["assertions"]
        text = load_skill(name)
        lines = text.splitlines()
        base = score(text, assertions)
        missing = sorted({a["id"] for a in assertions} - base)

        kill, unguarded = sweep(text, assertions)
        dead = sorted(aid for aid, s in kill.items() if not s)
        broad = sorted(aid for aid, s in kill.items() if len(s) > 12)
        dupes = audit_uniqueness(text, assertions)
        loose = audit_gaps(assertions)

        print(f"\n=== {name} — {len(assertions)} assertion, {len(lines)} dòng ===")
        print(f"  baseline: {len(base)}/{len(assertions)}" + (f"  KHÔNG ĐẠT: {missing}" if missing else ""))
        print(f"  {'ANCHOR CHẾT: ' + str(dead) if dead else 'anchor chết: không có'}")
        print(f"  {'ANCHOR QUÁ RỘNG: ' + str(broad) if broad else 'anchor quá rộng: không có'}")
        if dupes:
            print("  ANCHOR KHÔNG ĐỦ NEO:")
            for aid, why in dupes:
                print(f"    {aid}: {why}")
        else:
            print("  anchor đủ neo: đạt")
        print(f"  {'KHOẢNG HỞ KHÔNG CHẶN: ' + str(loose) if loose else 'khoảng hở không chặn: không có'}")
        if unguarded:
            print(f"  dòng KHÔNG được assertion nào canh: {len(unguarded)}/{len(lines)}")
            for i in unguarded[:8]:
                print(f"    L{i + 1}: {lines[i][:78]}")
            if len(unguarded) > 8:
                print(f"    … còn {len(unguarded) - 8} dòng")

        failures += len(missing) + len(dead) + len(dupes) + len(loose)
        report[name] = {
            "baseline": f"{len(base)}/{len(assertions)}",
            "missing": missing,
            "dead": dead,
            "broad": broad,
            "weak_anchor": [{"id": a, "why": w} for a, w in dupes],
            "unbounded_gaps": [{"id": a, "gap": g} for a, g in loose],
            "unguarded_lines": [{"line": i + 1, "text": lines[i]} for i in unguarded],
            "kill_sizes": {aid: len(s) for aid, s in sorted(kill.items())},
        }

    if "--json" in sys.argv:
        print("\n" + json.dumps(report, ensure_ascii=False, indent=2))

    print(f"\n{'=' * 60}")
    print("MUTATION: ĐẠT — mọi anchor đều neo vào nội dung duy nhất" if not failures
          else f"MUTATION: {failures} vấn đề cần vá")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
