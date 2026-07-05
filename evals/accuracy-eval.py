#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Accuracy eval harness for extraction skills (helix-cad-ingest).

Unlike the STATIC evals (which regex-grep the SKILL.md text) and RUNTIME evals
(which pipe test_input to `claude -p`), an ACCURACY eval runs the real
extraction pipeline on a drawing whose answers are known, then scores the
extracted values against a golden Q&A set — the measurement layer the CAD
pipeline was missing (see the ConstructIQ "Drawing Analyser" method: index
once, query from text, grade against ground truth).

It is deterministic and 100% LOCAL: it shells out to the skill's own
`ingest.py` (no reimplementation), reads the emitted `cad_extract.json`, and
resolves each question's `query` against it.

Spec format (evals/<skill>.accuracy.json):
{
  "skill": "helix-cad-ingest",
  "mode": "accuracy",
  "fixture": { "generator": "fixtures/gen_fixture_dxf.py",
               "dxf": "fixtures/sample_part.dxf",
               "classification": "HẠN-CHẾ" },
  "ingest_script": "skills/helix/helix-cad-ingest/ingest.py",
  "passing_score": 95,          // accuracy % required to PASS
  "questions": [
    { "id": "Q01", "question": "Vật liệu?",
      "query": "meta.material", "expected": "NHÔM 5083", "match": "exact",
      "required": true },
    { "id": "Q05", "question": "Số lỗ Ø6.6?",
      "query": "holes[dia=6.6].count", "expected": 4, "match": "exact",
      "confidence_query": "holes[dia=6.6].confidence", "min_confidence": "HIGH" }
  ]
}

Query mini-language (resolved against the extract JSON):
  meta.material            dotted path
  holes[dia=6.6].count     filter a list by field==value, then take a field
  dimensions[0].value      list index then field
  holes[]|sum-of:count     take a list, aggregate a field: sum-of / max-of / min-of
  holes[]|count            length of a list
  meta.product             scalar

match modes: exact (default) · approx (numeric, uses `tolerance`) ·
             contains (substring) · regex

Exit: 0 = accuracy >= passing_score ; 2 = below threshold ; 3 = harness/IO error.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

CONF_RANK = {"LOW": 0, "MED": 1, "HIGH": 2}
_SEG_RE = re.compile(r"^([A-Za-z_][\w]*)?(\[.*\])?$")


def _apply_bracket(current, key, spec):
    """Apply a [...] bracket op to current[key] (or current if key is '')."""
    target = current if key == "" else (current or {}).get(key)
    inner = spec[1:-1].strip()
    if inner == "":                       # [] -> the whole list
        return target
    if "=" in inner:                      # [field=value] -> filter
        f, v = (s.strip() for s in inner.split("=", 1))
        return [it for it in (target or []) if str(it.get(f)) == v]
    return (target or [])[int(inner)]     # [index]


def _split_path(path):
    """Split on '.' but NOT inside [...] (a filter value like dia=6.6 has a dot)."""
    toks, buf, depth = [], [], 0
    for ch in path:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "." and depth == 0:
            toks.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    toks.append("".join(buf))
    return toks


def _walk(data, path):
    current = data
    for tok in _split_path(path):
        m = _SEG_RE.match(tok)
        if not m:
            raise ValueError(f"bad query segment: {tok!r}")
        key, bracket = m.group(1) or "", m.group(2)
        if bracket:
            current = _apply_bracket(current, key, bracket)
        elif isinstance(current, list):    # map a field over a list
            current = [(it or {}).get(key) for it in current]
        else:
            current = (current or {}).get(key)
    return current


def resolve(data, query):
    agg = None
    if "|" in query:
        query, agg = (s.strip() for s in query.split("|", 1))
    value = _walk(data, query)
    if agg == "count":
        return len(value or [])
    if agg and agg.startswith(("sum-of:", "max-of:", "min-of:")):
        op, field = agg.split(":", 1)
        nums = [(it or {}).get(field) for it in (value or [])]
        nums = [n for n in nums if isinstance(n, (int, float))]
        if not nums:
            return None
        return {"sum-of": sum, "max-of": max, "min-of": min}[op](nums)
    if agg:
        raise ValueError(f"unknown aggregate: {agg!r}")
    # no explicit aggregate: unwrap a 1-element list to a scalar
    if isinstance(value, list) and len(value) == 1:
        return value[0]
    return value


def compare(actual, expected, match, tolerance):
    if match == "approx":
        try:
            return abs(float(actual) - float(expected)) <= float(tolerance or 0)
        except (TypeError, ValueError):
            return False
    if match == "contains":
        return actual is not None and str(expected) in str(actual)
    if match == "regex":
        return actual is not None and bool(re.search(str(expected), str(actual)))
    # exact: compare numerically when both look numeric, else string
    try:
        return float(actual) == float(expected)
    except (TypeError, ValueError):
        return str(actual) == str(expected)


def run_ingest(repo, specdir, spec, workdir):
    # fixture paths are relative to the spec file (they live beside it in evals/);
    # ingest_script is relative to the repo root.
    dxf = os.path.join(specdir, spec["fixture"]["dxf"])
    if not os.path.exists(dxf):                     # regenerate from committed generator
        gen = os.path.join(specdir, spec["fixture"]["generator"])
        subprocess.run([sys.executable, gen], check=True,
                       env={**os.environ, "PYTHONUTF8": "1"})
    script = os.path.join(repo, spec.get(
        "ingest_script", "skills/helix/helix-cad-ingest/ingest.py"))
    subprocess.run(
        [sys.executable, script, dxf, "--out", workdir,
         "--classification", spec["fixture"].get("classification", "MẬT")],
        check=True, env={**os.environ, "PYTHONUTF8": "1"})
    base = os.path.splitext(os.path.basename(dxf))[0]
    with open(os.path.join(workdir, f"{base}.cad_extract.json"), encoding="utf-8") as f:
        return json.load(f)


def grade(extract, questions):
    rows, passed, req_total, req_passed = [], 0, 0, 0
    for q in questions:
        req = q.get("required", False)
        req_total += 1 if req else 0
        try:
            actual = resolve(extract, q["query"])
            ok = compare(actual, q["expected"], q.get("match", "exact"), q.get("tolerance"))
        except Exception as ex:                       # noqa: BLE001 — report, don't crash
            actual, ok = f"<error: {type(ex).__name__}: {ex}>", False
        conf_note = ""
        if ok and q.get("min_confidence"):
            conf = resolve(extract, q["confidence_query"])
            need = CONF_RANK[q["min_confidence"]]
            got = CONF_RANK.get(str(conf), -1)
            if got < need:
                ok = False
                conf_note = f" [conf {conf} < {q['min_confidence']}]"
            else:
                conf_note = f" [conf {conf}]"
        passed += 1 if ok else 0
        req_passed += 1 if (ok and req) else 0
        rows.append((q["id"], "PASS" if ok else "FAIL", req,
                     q.get("question", ""), actual, q["expected"], conf_note))
    return rows, passed, req_passed, req_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="path to <skill>.accuracy.json")
    ap.add_argument("--repo", default=None, help="repo root (default: two levels up from spec)")
    a = ap.parse_args()

    spec = json.load(open(a.spec, encoding="utf-8"))
    specdir = os.path.dirname(os.path.abspath(a.spec))
    repo = a.repo or os.path.dirname(specdir)
    total = len(spec["questions"])
    passing = spec.get("passing_score", 95)

    with tempfile.TemporaryDirectory() as workdir:
        try:
            extract = run_ingest(repo, specdir, spec, workdir)
        except subprocess.CalledProcessError as ex:
            print(f"HARNESS ERROR: ingest failed ({ex})")
            return 3
        rows, passed, req_passed, req_total = grade(extract, spec["questions"])

    acc = (passed / total * 100) if total else 0
    print(f"=== Accuracy Eval: {spec['skill']} ===")
    print(f"Fixture: {spec['fixture']['dxf']}  (ground truth self-generated)")
    print(f"Accuracy: {passed}/{total} ({acc:.1f}%)   Required: {req_passed}/{req_total}")
    print()
    for qid, status, req, question, actual, expected, conf in rows:
        tag = "*" if req else " "
        detail = "" if status == "PASS" else f"  got={actual!r} want={expected!r}"
        print(f"  {qid} [{status}]{tag} {question}{conf}{detail}")
    print()
    ok = acc >= passing and req_passed == req_total
    print(f"RESULT: {'PASS' if ok else 'FAIL'} "
          f"(threshold {passing}% + all required)")
    return 0 if ok else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as ex:                            # noqa: BLE001
        print(f"HARNESS ERROR: {type(ex).__name__}: {ex}")
        sys.exit(3)
