#!/usr/bin/env python3
"""
helix-cad-redraw / written_vs_drawn.py — list INTERNAL INCONSISTENCIES of an original sheet BEFORE redrawing:
dimensions whose written number differs from what the geometry measures.

Why: originals routinely carry overrides typed over the measured value (e.g. written 500 on a 540 plate,
a 300 depth measured to a different face, a "120" leg that measures 138) and detail views labelled "1:2"
whose dimension factor says otherwise. A redraw must not silently pick one: list them, the owner decides each one IN WORDS
(not by option letter), and the decision is recorded next to the sheet.

For every DIMENSION: shown = numeric part of the override text (or the measured value when the text is "" / "<>"),
measured = get_measurement() × dimlfac(style). Flags:
  MISMATCH  |shown − measured| > --tol (and > 0.2 %)  — written ≠ drawn
  FACTOR    text overrides on one sheet imply a constant factor ≠ 1 (e.g. 0.4 ⇒ the detail is drawn 2.5×):
            compare with the scale written in the view label yourself.
  ROUNDED   measured has a fraction but the style shows 0 decimals (22.5 shows as "22"; 612.5 as "613").

Usage: python written_vs_drawn.py <dxf> [--tol 0.5] [--json]
Exit: 0 consistent · 2 inconsistencies listed · 3 usage/IO error.
"""
import argparse
import json
import re
import sys
from collections import Counter

import ezdxf

NUM = re.compile(r"(?<![\w.])(\d+(?:[.,]\d+)?)")


def _plain(t):
    t = re.sub(r"\\[A-Za-z][^;\\]*;|[{}]", "", t)
    return t.replace("%%C", "Ø").replace("%%c", "Ø").replace("%%P", "±").replace("%%p", "±")


def scan(path, tol=0.5):
    doc = ezdxf.readfile(path); m = doc.modelspace()
    rows, factors = [], Counter()
    for e in m.query("DIMENSION"):
        k = e.dimtype & 7
        if k not in (0, 1, 3, 4):
            continue
        try:
            meas = e.get_measurement()
        except Exception:
            continue
        st = e.dxf.dimstyle
        sty = doc.dimstyles.get(st) if st in doc.dimstyles else None
        lf = sty.dxf.get("dimlfac", 1) if sty else 1
        dec = sty.dxf.get("dimdec", 4) if sty else 4
        meas *= lf
        txt = e.dxf.get("text", "")
        flags, shown = [], None
        if txt not in ("", "<>") and "<>" not in txt:
            mnum = NUM.search(_plain(txt))
            if mnum:
                shown = float(mnum.group(1).replace(",", "."))
                if abs(shown - meas) > tol and abs(shown - meas) > 0.002 * max(abs(meas), 1):
                    flags.append("MISMATCH")
                    if meas:
                        factors[round(shown / meas, 2)] += 1
        elif dec == 0 and abs(meas - round(meas)) >= 0.05:
            flags.append("ROUNDED")
        if flags:
            rows.append({"handle": e.dxf.handle, "text": _plain(txt), "shown": shown, "measured": round(meas, 2), "flags": flags})
    common = [f for f, c in factors.items() if c >= 3 and f not in (1.0,)]
    for r in rows:
        if r["shown"] and r["measured"] and round(r["shown"] / r["measured"], 2) in common:
            r["flags"].append("FACTOR")
    return {"rows": rows, "implied_factors": {str(f): factors[f] for f in common}}


def main(argv=None):
    ap = argparse.ArgumentParser(description="written vs drawn dimension audit")
    ap.add_argument("dxf"); ap.add_argument("--tol", type=float, default=0.5); ap.add_argument("--json", action="store_true")
    try:
        a = ap.parse_args(argv)
        r = scan(a.dxf, a.tol)
    except SystemExit:
        return 3
    except (IOError, ezdxf.DXFError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 3
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        for x in r["rows"]:
            print(f"{'/'.join(x['flags']):16} shown={x['shown']!s:>8} measured={x['measured']:>9}  «{x['text'][:30]}»")
        if r["implied_factors"]:
            print("implied factors (detail drawn at another scale?):", r["implied_factors"])
    return 2 if r["rows"] else 0


if __name__ == "__main__":
    sys.exit(main())
