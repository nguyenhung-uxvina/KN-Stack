#!/usr/bin/env python3
"""
helix-cad-redraw / notes_strokes.py — keep the loose STROKES inside the technical-notes block (weld symbols).

Why: drafters often draw the weld-fillet triangle in front of "Mối hàn 5 ..." as 2-3 loose LINEs on top of the
notes MTEXT. A redraw script that deletes "geometry" and keeps "text" silently drops them; the text survives,
the symbol does not, and no text/overlap check notices. (The drawing scripts must keep them too: collect
`strokes_in(msp, notes_region(msp))` handles BEFORE deleting.)

Per sheet pair (matched by the 2-digit sheet prefix "NN_*.dxf"): if the ORIGINAL notes MTEXT (starts with
--header) contains --keyword and has small strokes (< --max-size units) inside its region, and the REDRAW has
none there ⇒ MISSING. --write copies the original strokes into the redraw. --skip: sheets where the owner
decided to drop the weld line.

Usage: python notes_strokes.py <orig_dir> <redraw_dir> [--write] [--skip 15 ...]
       [--header "Yêu cầu kỹ thuật"] [--keyword "Mối hàn"] [--max-size 60]
Exit: 0 nothing missing (or written) · 2 missing · 3 usage/IO error.
"""
import argparse
import glob
import os
import sys

import ezdxf
from ezdxf import bbox
from ezdxf.tools.text_size import estimate_mtext_extents


def notes_region(msp, header="Yêu cầu kỹ thuật"):
    for t in msp.query("MTEXT"):
        s = t.plain_text()
        if s.startswith(header):
            w, h = estimate_mtext_extents(t)
            x, y = t.dxf.insert.x, t.dxf.insert.y
            return s, (x - 5, y - h - 5, x + max(w, t.dxf.get("width", 0)) + 5, y + 5)
    return None, None


def strokes_in(msp, region, max_size=60.0):
    if not region:
        return []
    cache = bbox.Cache(); out = []
    for e in msp.query("LINE LWPOLYLINE"):
        b = bbox.extents([e], cache=cache)
        if (b.has_data and b.size.x < max_size and b.size.y < max_size and region[0] <= b.extmin.x and b.extmax.x <= region[2]
                and region[1] <= b.extmin.y and b.extmax.y <= region[3]):
            out.append(e)
    return out


def run(orig_dir, redraw_dir, write=False, skip=(), header="Yêu cầu kỹ thuật", keyword="Mối hàn", max_size=60.0):
    rows, missing = [], []
    for f in sorted(glob.glob(os.path.join(orig_dir, "[0-9][0-9]_*.dxf"))):
        no = int(os.path.basename(f)[:2])
        g = glob.glob(os.path.join(redraw_dir, f"{no:02d}_*.dxf"))
        if no in skip or not g:
            continue
        mo = ezdxf.readfile(f).modelspace()
        s, reg = notes_region(mo, header)
        if not s or keyword not in s:
            continue
        so = strokes_in(mo, reg, max_size)
        dr = ezdxf.readfile(g[0]); mr = dr.modelspace()
        _, reg2 = notes_region(mr, header)
        sr = strokes_in(mr, reg2, max_size)
        state = "OK" if sr else ("MISSING" if so else "orig-has-none")
        rows.append((no, len(so), len(sr), state))
        if state == "MISSING":
            missing.append(no)
            if write:
                for e in so:
                    mr.add_entity(e.copy())
                dr.saveas(g[0])
    return rows, missing


def main(argv=None):
    ap = argparse.ArgumentParser(description="notes-block strokes (weld symbols) gate")
    ap.add_argument("orig_dir"); ap.add_argument("redraw_dir"); ap.add_argument("--write", action="store_true")
    ap.add_argument("--skip", type=int, nargs="*", default=[]); ap.add_argument("--header", default="Yêu cầu kỹ thuật")
    ap.add_argument("--keyword", default="Mối hàn"); ap.add_argument("--max-size", type=float, default=60.0)
    try:
        a = ap.parse_args(argv)
        rows, missing = run(a.orig_dir, a.redraw_dir, a.write, tuple(a.skip), a.header, a.keyword, a.max_size)
    except SystemExit:
        return 3
    except (IOError, ezdxf.DXFError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 3
    for no, a1, a2, st in rows:
        print(f"sheet {no:2d}: orig {a1} strokes · redraw {a2} → {st}")
    print("MISSING:", missing, "(copied)" if a.write and missing else "")
    return 0 if (not missing or a.write) else 2


if __name__ == "__main__":
    sys.exit(main())
