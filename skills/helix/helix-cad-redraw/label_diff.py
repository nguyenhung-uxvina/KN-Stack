#!/usr/bin/env python3
"""
helix-cad-redraw / label_diff.py — what TEXT did the redraw lose or add, sheet by sheet (original ↔ redraw).

Compares the multiset of labels (TEXT, MTEXT outside --skip-layer and outside the notes block) and of dimension
texts as SHOWN on paper (override text, else measured × dimlfac). Every "lost" item must be explained (owner
decision) and every "added" one must come from a written number — never from a guess.

Usage: python label_diff.py <orig_dir> <redraw_dir> <sheet no> [...] [--skip-layer L] [--header "Yêu cầu kỹ thuật"]
Exit: 0 identical · 2 differences listed · 3 usage/IO error.
"""
import argparse
import glob
import os
import re
import sys
from collections import Counter

import ezdxf


def dim_text(doc, e):
    t = e.dxf.get("text", "")
    if t not in ("", "<>") and "<>" not in t:
        s = t
    else:
        try:
            v = e.get_measurement()
            st = e.dxf.dimstyle
            lf = doc.dimstyles.get(st).dxf.get("dimlfac", 1) if st in doc.dimstyles else 1
            k = e.dimtype & 7
            if k in (0, 1, 3, 4):
                s = f"{v * lf:.1f}".rstrip("0").rstrip(".")
            elif k in (2, 5):
                s = f"{v:.0f}°"
            else:
                return None
        except Exception:
            return None
        s = t.replace("<>", s) if "<>" in t else s
    s = re.sub(r"\\[A-Za-z][^;]*;|[{}]", "", s).replace("%%C", "Ø").replace("%%c", "Ø").replace("∅", "Ø").replace("%%P", "±")
    return s.strip()


def collect(path, skip_layers=(), header="Yêu cầu kỹ thuật"):
    doc = ezdxf.readfile(path); m = doc.modelspace()
    labels, dims = Counter(), Counter()
    for e in m:
        t = e.dxftype()
        if t == "TEXT" and e.dxf.layer not in skip_layers:
            labels[e.dxf.text.strip()] += 1
        elif t == "MTEXT" and e.dxf.layer not in skip_layers:
            s = e.plain_text().strip()
            if s and not s.startswith(header):
                labels[s.replace("\n", " ")] += 1
        elif t == "DIMENSION":
            s = dim_text(doc, e)
            if s:
                dims[s] += 1
    return labels, dims


def main(argv=None):
    ap = argparse.ArgumentParser(description="label/dimension text diff original vs redraw")
    ap.add_argument("orig_dir"); ap.add_argument("redraw_dir"); ap.add_argument("sheets", type=int, nargs="+")
    ap.add_argument("--skip-layer", action="append", default=[]); ap.add_argument("--header", default="Yêu cầu kỹ thuật")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 3
    diff = 0
    for no in a.sheets:
        fo = glob.glob(os.path.join(a.orig_dir, f"{no:02d}_*.dxf")); fr = glob.glob(os.path.join(a.redraw_dir, f"{no:02d}_*.dxf"))
        if not fo or not fr:
            continue
        lo, do = collect(fo[0], tuple(a.skip_layer), a.header); lr, dr = collect(fr[0], tuple(a.skip_layer), a.header)
        parts = [sorted((lo - lr).elements()), sorted((lr - lo).elements()), sorted((do - dr).elements()), sorted((dr - do).elements())]
        diff += any(parts)
        print(f"--- sheet {no}: labels lost {parts[0]} | added {parts[1]}")
        print(f"            dims lost {parts[2]} | added {parts[3]}")
    return 2 if diff else 0


if __name__ == "__main__":
    sys.exit(main())
