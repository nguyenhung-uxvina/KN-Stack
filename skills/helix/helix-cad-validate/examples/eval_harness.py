#!/usr/bin/env python3
"""
eval_harness.py — Fixed-scenario eval harness for helix-cad-validate (Mastery Module 4).

Answers KHUNG v1.0 §3.3/§10-GĐ2 + the DEBATE trigger #4 (sửa contract → lo phá thiết kế cũ):
run a FIXED corpus of cases at a checkpoint, record metrics, and refuse a harness change that
regresses. "Chạy bộ kịch bản cố định + ghi metric" là cách DUY NHẤT biết một thay đổi harness có
cải thiện thật hay không (chống 'bay mù') — Anthropic *Demystifying evals*.

Two tiers (never mixed — Anthropic capability vs regression):
  - regression : must stay ~100%. ANY miss => eval FAIL (exit 1). Protects against backsliding;
                 every fixed bug graduates into a regression case here (Improvement Engine).
  - capability : the hill to climb. Misses are REPORTED, do NOT gate. Low pass-rate is expected.

pass@k vs pass^k: helix-cad-validate is DETERMINISTIC, so per-case pass^k == pass@1. We still run
--k reps and assert the verdict is IDENTICAL across reps: any divergence = a non-determinism smell
(the tool must be reproducible to be a safety gate). For an INFERENTIAL judge (helix-design-review),
the same harness runs k>1 and pass^k (all-k-succeed) is the safety-gate metric.

stdlib only, offline. Exit: 0 = all regression pass + reproducible · 1 = regression miss / non-determinism · 3 = IO.

Usage:
  python eval_harness.py --corpus corpus.json [--validator ../validate.py] [--k 1] [--out eval_report] [--quiet]
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

EXIT_VERDICT = {0: "PASS", 2: "FAIL"}  # 3/other => ERROR


def _run_case(validator, base, case, k):
    """Run one case k times; return (verdicts:list, reproducible:bool)."""
    cmd = [sys.executable, validator,
           "--extract", os.path.join(base, case["extract"]),
           "--rules", os.path.join(base, case["rules"]),
           "--quiet", "--out", os.path.join(base, "_eval_tmp")]
    if case.get("mass_props"):
        cmd += ["--mass-props", os.path.join(base, case["mass_props"])]
    if case.get("approved_hash"):
        cmd += ["--approved-hash", case["approved_hash"]]
    verdicts = []
    for _ in range(max(1, k)):
        cp = subprocess.run(cmd, capture_output=True, text=True)
        verdicts.append(EXIT_VERDICT.get(cp.returncode, f"ERROR({cp.returncode})"))
    reproducible = len(set(verdicts)) == 1
    return verdicts, reproducible


def main(argv=None):
    ap = argparse.ArgumentParser(description="Eval harness for helix-cad-validate (Module 4).")
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--validator", help="path to validate.py (default: ../validate.py next to corpus)")
    ap.add_argument("--k", type=int, default=1, help="reps per case (determinism check; pass^k for inferential)")
    ap.add_argument("--out", default="eval_report")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    base = os.path.dirname(os.path.abspath(args.corpus))
    validator = args.validator or os.path.normpath(os.path.join(base, "..", "validate.py"))
    try:
        with open(args.corpus, "r", encoding="utf-8") as f:
            corpus = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"[EVAL IO-ERROR] {e}", file=sys.stderr)
        return 3

    results = []
    for case in corpus.get("cases", []):
        verdicts, repro = _run_case(validator, base, case, args.k)
        got = verdicts[0]
        hit = repro and got == case["expect"]
        results.append({
            "id": case["id"], "tier": case.get("tier", "capability"),
            "expect": case["expect"], "got": got, "reproducible": repro,
            "hit": hit, "origin": case.get("origin", ""), "note": case.get("note", ""),
        })

    reg = [r for r in results if r["tier"] == "regression"]
    cap = [r for r in results if r["tier"] == "capability"]
    reg_miss = [r for r in reg if not r["hit"]]
    nonrepro = [r for r in results if not r["reproducible"]]
    cap_pass = sum(1 for r in cap if r["hit"])

    metrics = {
        "regression": {"n": len(reg), "passed": len(reg) - len(reg_miss),
                       "pass_rate": round((len(reg) - len(reg_miss)) / len(reg), 4) if reg else None},
        "capability": {"n": len(cap), "passed": cap_pass,
                       "pass_rate": round(cap_pass / len(cap), 4) if cap else None},
        "k": args.k, "non_deterministic_cases": [r["id"] for r in nonrepro],
    }
    verdict_fail = bool(reg_miss) or bool(nonrepro)
    out = {
        "tool": "eval_harness", "target": "helix-cad-validate",
        "evaluated_at": datetime.now(timezone.utc).isoformat(),
        "validator": os.path.basename(validator),
        "verdict": "FAIL" if verdict_fail else "PASS",
        "metrics": metrics, "cases": results,
        "gate": "regression suite must be 100% + reproducible",
    }
    with open(os.path.join(base, args.out + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    lines = [f"# eval_harness — {out['verdict']}",
             f"- validator: {out['validator']}  · k={args.k}  · {out['evaluated_at']}",
             f"- regression: {metrics['regression']['passed']}/{metrics['regression']['n']} "
             f"(pass_rate {metrics['regression']['pass_rate']}) — MUST be 1.0",
             f"- capability: {metrics['capability']['passed']}/{metrics['capability']['n']} "
             f"(pass_rate {metrics['capability']['pass_rate']}) — hill to climb", "",
             "| Case | Tier | Expect | Got | k-repro | Hit | Origin |",
             "|---|---|---|---|:-:|:-:|---|"]
    for r in results:
        lines.append(f"| {r['id']} | {r['tier']} | {r['expect']} | {r['got']} | "
                     f"{'✓' if r['reproducible'] else '✗'} | {'✓' if r['hit'] else '✗'} | {r['origin']} |")
    if reg_miss:
        lines += ["", "## ❌ REGRESSION MISS (backslide — harness change rejected)"]
        lines += [f"- {r['id']}: expected {r['expect']} got {r['got']} — {r['note']}" for r in reg_miss]
    if nonrepro:
        lines += ["", "## ⚠ NON-DETERMINISM (a safety gate must be reproducible)"]
        lines += [f"- {r['id']}: verdicts varied across k={args.k} reps" for r in nonrepro]
    with open(os.path.join(base, args.out + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    if not args.quiet:
        print(f"=== EVAL: {out['verdict']} === "
              f"regression {metrics['regression']['passed']}/{metrics['regression']['n']} · "
              f"capability {metrics['capability']['passed']}/{metrics['capability']['n']} · k={args.k}")
        for r in reg_miss:
            print(f"  REGRESSION MISS {r['id']}: expected {r['expect']} got {r['got']}")
        for r in nonrepro:
            print(f"  NON-DETERMINISM {r['id']}: {'/'.join(set())}")
    # cleanup tmp
    for ext in (".json", ".md"):
        p = os.path.join(base, "_eval_tmp" + ext)
        if os.path.isfile(p):
            try: os.remove(p)
            except OSError: pass
    return 1 if verdict_fail else 0


if __name__ == "__main__":
    sys.exit(main())
