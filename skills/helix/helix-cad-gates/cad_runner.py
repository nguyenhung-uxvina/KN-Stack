#!/usr/bin/env python3
"""
helix-cad-gates / cad_runner.py — run an AI-written code-CAD script in an isolated child process.

Contract for every model.py (helix-cad-bridge Step 3, helix-cad-reconstruct, helix-cad-batch):
  PARAMS = {"length": 186.0, ...}      # named numeric dimensions, mm — the ONLY place numbers live
  def build(params) -> build123d.Shape  # pure: geometry from params, no file I/O
  if __name__ == "__main__": export_step(build(PARAMS), "model.step")

Why a child process: the script is model-written code. It runs with `python -I` (no user site, no cwd on
sys.path), a timeout, and its own working directory — so a planted module or an endless loop cannot take
the caller down. 100% local; no network.

Usage:
  python cad_runner.py run   --model model.py [--workdir DIR] [--timeout 120]
  python cad_runner.py build --model model.py --out variant.step [--set length=204.6 --set dia=30]
Exit codes: 0 = STEP written, 2 = script failed / no STEP, 3 = usage/IO error.
"""
import argparse
import json
import os
import subprocess
import sys

DRIVER = r'''
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("model_under_test", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
if not isinstance(getattr(mod, "PARAMS", None), dict) or not callable(getattr(mod, "build", None)):
    print(json.dumps({"ok": False, "error": "NO_PARAMS_CONTRACT: model.py must define PARAMS dict and build(params)"}))
    sys.exit(2)
params = dict(mod.PARAMS)
for k, v in json.loads(sys.argv[3]).items():
    if k not in params:
        print(json.dumps({"ok": False, "error": f"UNKNOWN_PARAM: {k}"})); sys.exit(2)
    params[k] = v
from build123d import export_step
shape = mod.build(params)
export_step(shape, sys.argv[2])
print(json.dumps({"ok": True, "params": params}))
'''


def _run(cmd, cwd, timeout):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"TIMEOUT after {timeout}s"


def run_script(model_py, workdir=None, timeout=120):
    """Execute model.py as a script (its __main__ must write model.step into workdir)."""
    model_py = os.path.abspath(model_py)
    workdir = os.path.abspath(workdir or os.path.dirname(model_py))
    step = os.path.join(workdir, "model.step")
    before = os.path.getmtime(step) if os.path.exists(step) else None
    rc, out, err = _run([sys.executable, "-I", "-X", "utf8", model_py], workdir, timeout)
    fresh = os.path.exists(step) and os.path.getmtime(step) != before
    return {"ok": rc == 0 and fresh, "returncode": rc, "step": step if fresh else None,
            "stderr_tail": err[-1500:], "stdout_tail": out[-500:]}


def read_params(model_py, timeout=60):
    """Return the PARAMS dict of model.py (None if it does not honour the contract)."""
    code = ("import importlib.util,json,sys;s=importlib.util.spec_from_file_location('m',sys.argv[1]);"
            "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
            "p=getattr(m,'PARAMS',None);print(json.dumps(p if isinstance(p,dict) and callable(getattr(m,'build',None)) else None))")
    rc, out, err = _run([sys.executable, "-I", "-X", "utf8", "-c", code, os.path.abspath(model_py)],
                        os.path.dirname(os.path.abspath(model_py)), timeout)
    if rc != 0:
        return None
    try:
        return json.loads(out.strip().splitlines()[-1])
    except (ValueError, IndexError):
        return None


def build_with_params(model_py, out_step, overrides=None, timeout=120):
    """Rebuild via build(PARAMS ⊕ overrides) and export to out_step. Used by F4 and helix-cad-batch."""
    out_step = os.path.abspath(out_step)
    if os.path.exists(out_step):
        os.remove(out_step)
    rc, out, err = _run([sys.executable, "-I", "-X", "utf8", "-c", DRIVER, os.path.abspath(model_py), out_step,
                         json.dumps(overrides or {})], os.path.dirname(out_step), timeout)
    info = {}
    for line in reversed(out.strip().splitlines()):
        try:
            info = json.loads(line); break
        except ValueError:
            continue
    ok = rc == 0 and os.path.exists(out_step) and info.get("ok", False)
    return {"ok": ok, "step": out_step if ok else None, "error": info.get("error") or (err[-800:] if not ok else ""),
            "params": info.get("params")}


def _parse_sets(pairs):
    o = {}
    for s in pairs or []:
        k, _, v = s.partition("=")
        o[k.strip()] = float(v)
    return o


def main(argv=None):
    ap = argparse.ArgumentParser(description="Run a code-CAD model.py in an isolated child process.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("--model", required=True); r.add_argument("--workdir")
    r.add_argument("--timeout", type=int, default=120)
    b = sub.add_parser("build"); b.add_argument("--model", required=True); b.add_argument("--out", required=True)
    b.add_argument("--set", action="append"); b.add_argument("--timeout", type=int, default=120)
    a = ap.parse_args(argv)
    if not os.path.exists(a.model):
        print(f"[IO-ERROR] no such model: {a.model}", file=sys.stderr); return 3
    res = run_script(a.model, a.workdir, a.timeout) if a.cmd == "run" else \
        build_with_params(a.model, a.out, _parse_sets(a.set), a.timeout)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return 0 if res["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
