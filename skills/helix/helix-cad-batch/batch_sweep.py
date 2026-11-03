#!/usr/bin/env python3
"""
helix-cad-batch / batch_sweep.py — build a family of variants from ONE parametric model.py.

Input: model.py honouring the helix-cad-gates PARAMS/build(params) contract + a variants CSV:
    variant_id,L_SHAFT,D_SHAFT,bbox_x,bbox_y,bbox_z
    GT-0301-A,186,28,194,40,40
    GT-0301-B,226,28,234,40,40
Columns matching PARAMS keys override them; optional bbox_x/y/z give the expected envelope for F2.
Each variant: cad_runner.build_with_params -> <out>/<variant_id>/model.step (+ .stl with --stl) ->
geom_gates (F1 always, F2 when bbox_* given) -> summary.csv + summary.md.

Usage: python batch_sweep.py --model model.py --variants variants.csv --out variants_out [--stl] [--tol 0.5]
Exit: 0 all variants PASS · 2 >=1 FAIL · 3 usage/IO error.
"""
import argparse
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATES = os.path.join(os.path.dirname(HERE), "helix-cad-gates")
sys.path.insert(0, GATES)
import cad_runner  # noqa: E402
import geom_gates  # noqa: E402

BBOX_COLS = ("bbox_x", "bbox_y", "bbox_z")


def sweep(model_py, variants_csv, out_dir, stl=False, tol=0.5):
    params = cad_runner.read_params(model_py)
    if not params:
        raise ValueError("model.py does not honour PARAMS/build(params) — batch needs it")
    rows = list(csv.DictReader(open(variants_csv, encoding="utf-8-sig")))
    if not rows or "variant_id" not in rows[0]:
        raise ValueError("variants CSV needs a 'variant_id' column")
    unknown = [c for c in rows[0] if c not in params and c not in BBOX_COLS and c != "variant_id"]
    if unknown:
        raise ValueError(f"columns not in PARAMS: {unknown}")
    results = []
    for r in rows:
        vid = r["variant_id"].strip()
        vdir = os.path.join(out_dir, vid)
        os.makedirs(vdir, exist_ok=True)
        over = {k: float(v) for k, v in r.items() if k in params and str(v).strip() != ""}
        b = cad_runner.build_with_params(model_py, os.path.join(vdir, "model.step"), over)
        res = {"variant_id": vid, **{k: over.get(k, params[k]) for k in params}, "build": "OK" if b["ok"] else "FAIL"}
        if not b["ok"]:
            res.update(verdict="FAIL", detail=b["error"][:200]); results.append(res); continue
        contract = {"part_id": vid, "bbox_tol": tol}
        if all(r.get(c, "").strip() for c in BBOX_COLS):
            contract["bbox"] = [float(r[c]) for c in BBOX_COLS]
        shape = geom_gates.load_step(b["step"])
        rep = geom_gates.Report()
        geom_gates.check_f1(shape, rep, b["step"])
        if "bbox" in contract:
            geom_gates.check_f2(shape, contract, rep, b["step"])  # no probes in a sweep ⇒ F2_probes = SKIP
        fails = [c["rule_id"] for c in rep.gating_failed]
        res.update(bbox=geom_gates.bbox_size(shape), volume_mm3=round(shape.volume),
                   verdict="FAIL" if fails else "PASS", detail=",".join(fails))
        if stl:
            from build123d import export_stl
            export_stl(shape, os.path.join(vdir, "model.stl"))
        json.dump({"checks": rep.checks}, open(os.path.join(vdir, "gates.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        results.append(res)
    keys = list(dict.fromkeys(k for res in results for k in res))
    with open(os.path.join(out_dir, "summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(results)
    with open(os.path.join(out_dir, "summary.md"), "w", encoding="utf-8") as f:
        f.write("| " + " | ".join(keys) + " |\n|" + "---|" * len(keys) + "\n")
        for res in results:
            f.write("| " + " | ".join(str(res.get(k, "")) for k in keys) + " |\n")
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="Parametric variant sweep with per-variant geometry gates.")
    ap.add_argument("--model", required=True)
    ap.add_argument("--variants", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--stl", action="store_true")
    ap.add_argument("--tol", type=float, default=0.5)
    a = ap.parse_args(argv)
    try:
        os.makedirs(a.out, exist_ok=True)
        res = sweep(a.model, a.variants, a.out, a.stl, a.tol)
    except (OSError, ValueError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    nfail = sum(r["verdict"] != "PASS" for r in res)
    print(f"=== helix-cad-batch: {len(res) - nfail}/{len(res)} PASS === summary: {os.path.join(a.out, 'summary.md')}")
    return 0 if nfail == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
