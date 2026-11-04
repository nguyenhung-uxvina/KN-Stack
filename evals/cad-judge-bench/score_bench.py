"""Score the 10 judge runs against the answer key (CADCodeVerify Table 9 style + case verdicts).
Usage: python evals/cad-judge-bench/score_bench.py <out_dir>   (same out_dir as make_cases.py)"""
import importlib.util
import json
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else sys.exit(__doc__)
CASES, KEY = os.path.join(ROOT, "jb_cases"), os.path.join(ROOT, "jb_key")
spec = importlib.util.spec_from_file_location(
    "judge_score", os.path.join(REPO, "skills", "helix", "helix-cad-judge", "judge_score.py"))
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)

key = json.load(open(os.path.join(KEY, "key.json"), encoding="utf-8"))
raw, fin = Counter(), Counter()
rows = []
per_q = {}
for case, k in sorted(key.items()):
    d = os.path.join(CASES, case)
    contract = json.load(open(os.path.join(d, "geometry_contract.json"), encoding="utf-8"))
    ap = os.path.join(d, "judge_answers.json")
    if not os.path.exists(ap):
        rows.append((case, k["name"], k["gates_verdict"], k["expect"], "NO ANSWERS", "")); continue
    answers = json.load(open(ap, encoding="utf-8"))
    n_lines = len(open(os.path.join(d, "model.py"), encoding="utf-8").read().splitlines())
    verdict, qrows, unknown, extra = J.score(contract, {}, answers, n_lines)
    misses = []
    for r in qrows:
        t = k["truth"][r["id"]]
        if t is None:
            continue
        ra = str(r["raw_answer"] or "missing").lower()
        cat = "correct" if ra == t else ("unclear" if ra in ("unclear", "missing") else "wrong")
        raw[cat] += 1
        fcat = "correct" if r["answer"] == t else ("unclear" if r["answer"] == "unclear" else "wrong")
        fin[fcat] += 1
        per_q.setdefault(r["id"], Counter())[fcat] += 1
        if fcat != "correct":
            misses.append(f"{r['id']}:{ra}->{r['answer']}(truth {t})")
    rows.append((case, k["name"], k["gates_verdict"], k["expect"], verdict, "; ".join(misses), len(extra)))

n = sum(raw.values())
print(f"Answers scored: {n} (n/a excluded)")
for lab, c in (("raw (agent)", raw), ("after judge_score", fin)):
    print(f"  {lab:<18} correct {c['correct']}/{n} = {100*c['correct']/n:.1f}% · wrong {c['wrong']} "
          f"({100*c['wrong']/n:.1f}%) · unclear {c['unclear']} ({100*c['unclear']/n:.1f}%)")
print("\n| case | seeded | gates | expected | judge verdict | misses | extra |")
for r in rows:
    print("| " + " | ".join(str(x) for x in r) + " |")
print("\nper question (final):", {q: dict(c) for q, c in sorted(per_q.items())})
