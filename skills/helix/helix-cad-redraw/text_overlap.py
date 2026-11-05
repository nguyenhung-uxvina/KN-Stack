#!/usr/bin/env python3
"""
helix-cad-redraw / text_overlap.py — deterministic TEXT OVERLAP + DUPLICATE-TEXT gate for 2D DXF sheets.

Two checks:
  OVERLAP    bounding boxes of TEXT, MTEXT and the text inside every DIMENSION, shrunk 15% per axis (touching
             edges are not overlap). MTEXT boxes are ESTIMATED (estimate_mtext_extents + attachment + rotation):
             ezdxf bbox of an MTEXT without width is wrong, and width=100000 explodes it.
  DUPLICATE  two TEXT/MTEXT on ANY layer with the same insert point (< 1 unit) — including layers skipped by
             OVERLAP. Why: a drawing script re-run on an already-redrawn sheet stacked the title-block "mass"
             cell 2-3 times (once with an old and a new value on top of each other) on 14 sheets, and the
             overlap check never saw it because the title-block layer was excluded.

Skips for OVERLAP only: --skip-layer (repeatable; e.g. the title-block layer whose cells are packed by design)
and MTEXT starting with --skip-prefix (the technical-notes block).

Usage: python text_overlap.py <dxf> [<dxf> ...] [--skip-layer L ...] [--skip-prefix P ...] [--json]
Exit: 0 clean · 2 overlap/duplicate found · 3 usage/IO error.
"""
import argparse
import json
import math
import sys

import ezdxf
from ezdxf import bbox
from ezdxf.tools.text_size import estimate_mtext_extents


def mtext_box(m):
    try:
        w, h = estimate_mtext_extents(m)
    except Exception:
        return None
    if w <= 0 or h <= 0:
        return None
    ap = m.dxf.get("attachment_point", 1)
    col, row = (ap - 1) % 3, (ap - 1) // 3
    x0 = -w * (0, 0.5, 1)[col]; y1 = h * (0, 0.5, 1)[row]
    rot = math.radians(m.get_rotation() if hasattr(m, "get_rotation") else m.dxf.get("rotation", 0))
    ix, iy = m.dxf.insert.x, m.dxf.insert.y
    pts = [(x0, y1), (x0 + w, y1), (x0 + w, y1 - h), (x0, y1 - h)]
    xs = [ix + x * math.cos(rot) - y * math.sin(rot) for x, y in pts]
    ys = [iy + x * math.sin(rot) + y * math.cos(rot) for x, y in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _label(v):
    return (v.dxf.text if v.dxftype() == "TEXT" else v.plain_text()).replace("\n", " ").strip()


def text_boxes(msp, skip_layers=(), skip_prefix=()):
    cache = bbox.Cache(); out = []
    for e in msp:
        t = e.dxftype()
        if t in ("TEXT", "MTEXT"):
            if e.dxf.layer in skip_layers or any(_label(e).startswith(p) for p in skip_prefix):
                continue
            items = [e]
        elif t == "DIMENSION":
            items = [v for v in e.virtual_entities() if v.dxftype() in ("TEXT", "MTEXT")]
        else:
            continue
        for v in items:
            if v.dxftype() == "MTEXT":
                b = mtext_box(v)
            else:
                try:
                    bb = bbox.extents([v], cache=cache)
                except Exception:
                    continue
                if not bb.has_data or bb.size.x <= 0:
                    continue
                b = (bb.extmin.x, bb.extmin.y, bb.extmax.x, bb.extmax.y)
            if b is None:
                continue
            mx, my = (b[2] - b[0]) * 0.075, (b[3] - b[1]) * 0.075
            out.append((_label(v)[:24], (b[0] + mx, b[1] + my, b[2] - mx, b[3] - my)))
    return out


def _hit(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def check(path, skip_layers=(), skip_prefix=()):
    m = ezdxf.readfile(path).modelspace()
    boxes = text_boxes(m, skip_layers, skip_prefix)
    overlaps = [(boxes[i][0], boxes[j][0]) for i in range(len(boxes)) for j in range(i + 1, len(boxes)) if _hit(boxes[i][1], boxes[j][1])]
    tt = [(_label(e), e.dxf.insert) for e in m.query("TEXT MTEXT")]
    dups = [(tt[i][0][:24], tt[j][0][:24]) for i in range(len(tt)) for j in range(i + 1, len(tt))
            if tt[i][0] and tt[j][0] and (tt[i][1] - tt[j][1]).magnitude < 1.0]
    return {"texts": len(boxes), "overlaps": overlaps, "duplicates": dups}


def main(argv=None):
    ap = argparse.ArgumentParser(description="text overlap + duplicate gate")
    ap.add_argument("dxf", nargs="+"); ap.add_argument("--skip-layer", action="append", default=[])
    ap.add_argument("--skip-prefix", action="append", default=[]); ap.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 3
    bad, rep = 0, {}
    try:
        for p in a.dxf:
            r = check(p, tuple(a.skip_layer), tuple(a.skip_prefix)); rep[p] = r
            bad += bool(r["overlaps"] or r["duplicates"])
            if not a.json:
                msg = "; ".join([f"«{x}»×«{y}»" for x, y in r["overlaps"][:6]] + [f"DUP «{x}»/«{y}»" for x, y in r["duplicates"][:6]])
                print(f"{p}: {r['texts']} texts · {len(r['overlaps'])} overlaps · {len(r['duplicates'])} duplicates" + (": " + msg if msg else ""))
    except (IOError, ezdxf.DXFError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
