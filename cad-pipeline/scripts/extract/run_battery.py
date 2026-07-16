#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_battery.py — Battery hồi quy cho harness trích xuất (Gate G3 + fixture cài lỗi)

Chạy toàn bộ kiểm chứng "chứng minh script đúng" trước khi phát hành/commit:
  1. Fixture cài lỗi chủ đích (cad-pipeline/golden/fixtures/): seed tốt phải PASS, seed xấu phải
     FAIL đúng 7 lỗi, seed vỡ cấu trúc phải bị SCHEMA chặn, cross 2 nguồn phải bắt lệch.
  2. Golden set giải tích (cad-pipeline/golden/step/): --regen trích lại actual-seed bằng freecadcmd
     (kiểm cả extractor); không --regen thì so actual đã có (chỉ kiểm validator).

Được gọi bởi pre-commit hook (cad-pipeline/scripts/hooks/pre-commit) khi thay đổi chạm
cad-pipeline/scripts/extract/ | schemas/ | golden/. Chạy tay:  python cad-pipeline/scripts/extract/run_battery.py [--regen]
Exit 0 = tất cả đạt · 1 = có mục hỏng (CẤM phát hành) · 3 = thiếu môi trường.
"""
import argparse, glob, json, os, subprocess, sys, tempfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
VALIDATOR = os.path.join(HERE, "validate_qtcn_seed.py")
EXTRACTOR = os.path.join(HERE, "freecad_extract.py")
FIX = os.path.join(REPO, "golden", "fixtures")
GOLD = os.path.join(REPO, "golden", "step")
FREECADCMD = os.environ.get("FREECADCMD", r"C:\Program Files\FreeCAD 1.1\bin\freecadcmd.exe")

def run_validator(args, tmp, tag):
    rep = os.path.join(tmp, tag + ".validation.json")
    p = subprocess.run([sys.executable, VALIDATOR] + args + ["--report", rep],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    counts = {}
    try:
        with open(rep, encoding="utf-8-sig") as f:
            counts = json.load(f).get("counts", {})
    except Exception:
        pass
    return p.returncode, counts

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regen", action="store_true",
                    help="trích lại actual-seed golden bằng freecadcmd (kiểm cả extractor)")
    a = ap.parse_args()

    if not os.path.isdir(FIX):
        sys.stderr.write("[!] Thiếu cad-pipeline/golden/fixtures/\n"); sys.exit(3)
    tmp = tempfile.mkdtemp(prefix="wx-battery-")
    fails = []

    def expect(tag, args, want_exit, want_fail_count=None):
        code, counts = run_validator(args, tmp, tag)
        ok = (code == want_exit) and (want_fail_count is None or counts.get("FAIL") == want_fail_count)
        mark = "OK " if ok else "HỎNG"
        extra = " (FAIL=%s, kỳ vọng %s)" % (counts.get("FAIL"), want_fail_count) if want_fail_count else ""
        print("  [%s] %-22s exit=%d (kỳ vọng %d)%s" % (mark, tag, code, want_exit, extra))
        if not ok:
            fails.append(tag)

    f = lambda n: os.path.join(FIX, n)
    print("— Fixture cài lỗi chủ đích —")
    expect("seed-good", ["--seed", f("seed_good.json")], 0)
    expect("seed-bad-7fail", ["--seed", f("seed_bad.json")], 2, want_fail_count=7)
    expect("schema-broken", ["--seed", f("seed_broken_schema.json")], 2)
    expect("cross-mismatch", ["--cross", f("seed_inventor.json"), f("seed_good.json")], 2)
    expect("determinism", ["--determinism", f("seed_good.json"), f("seed_good.json")], 0)

    # --- Rhino HU-rules (nếu có rhino3dm + fixture) ---
    rh_good = os.path.join(REPO, "golden", "rhino", "fixture-good.3dm")
    rh_bad = os.path.join(REPO, "golden", "rhino", "fixture-bad.3dm")
    try:
        import rhino3dm  # noqa: F401
        have_rhino = True
    except ImportError:
        have_rhino = False
        print("— Rhino: thiếu rhino3dm, bỏ qua (pip install rhino3dm) —")
    if have_rhino and os.path.exists(rh_good):
        print("— Rhino HU-rules (rhino_check) —")
        for tag, path, want in (("rhino-good", rh_good, 0), ("rhino-bad", rh_bad, 2)):
            p = subprocess.run([sys.executable, os.path.join(HERE, "rhino_check.py"),
                                "--file", path, "--out", tmp],
                               capture_output=True, text=True, encoding="utf-8", errors="replace")
            ok = p.returncode == want
            print("  [%s] %-22s exit=%d (kỳ vọng %d)" % ("OK " if ok else "HỎNG", tag, p.returncode, want))
            if not ok:
                fails.append(tag)

    print("— Golden set giải tích (G3) —")
    if a.regen:
        if not os.path.exists(FREECADCMD):
            sys.stderr.write("[!] Không thấy freecadcmd tại %s (đặt env FREECADCMD) — bỏ regen, so actual cũ\n"
                             % FREECADCMD)
        else:
            for case in sorted(os.listdir(GOLD)):
                cdir = os.path.join(GOLD, case)
                steps = glob.glob(os.path.join(cdir, "source", "*.step"))
                if not steps:
                    continue
                env = dict(os.environ, FC_FILE=steps[0], FC_OUT=cdir, FC_NAME="actual-seed")
                p = subprocess.run([FREECADCMD, EXTRACTOR], env=env, capture_output=True,
                                   text=True, encoding="utf-8", errors="replace")
                if p.returncode != 0:
                    print("  [HỎNG] regen %s: freecadcmd exit %d" % (case, p.returncode))
                    fails.append("regen-" + case)
            print("  (đã trích lại actual-seed cho các case golden)")
    expect("golden-G3", ["--golden", GOLD], 0)

    print("KẾT QUẢ: %s" % ("ĐẠT TOÀN BỘ — được phát hành" if not fails
                           else "HỎNG %d mục: %s — CẤM phát hành (G3)" % (len(fails), ", ".join(fails))))
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
