#!/usr/bin/env python3
"""
helix-cad-ingest / render_dxf.py — DXF sheet -> PNG that reads like an AutoCAD plot.

Why: matplotlib cannot draw the TCVN 7284 fonts or the AIGDT symbol font, so a naive render shows
Vietnamese as boxes and Ø as the letter "n" (AIGDT maps n -> Ø). An agent reading that image misreads
"n40" as a label, not Ø40. This script fixes fonts IN MEMORY (the source DXF is never modified):
  - every text style -> arial.ttf (has Vietnamese glyphs)
  - "{\\fAIGDT...;[\\l]n}" -> "Ø"; other inline font switches removed
Measured on GIÁ TRƯỢT 2026-11-02: before the fix Ø40 / Ø28h7 / Ø5.5 rendered as n40 / n28h7 / n5.5.

Usage: python render_dxf.py --in part.dxf --out part.png [--dpi 150]
       python render_dxf.py --in-dir dxf/ --out-dir png/
Exit: 0 ok · 3 IO error.
"""
import argparse
import glob
import os
import re
import sys

AIGDT_DIA = re.compile(r"\{?\\fAIGDT[^;]*;(\\[lL])?n\}?")
FONT_SWITCH = re.compile(r"\\f[^;]*;")


def clean_text(t):
    return FONT_SWITCH.sub("", AIGDT_DIA.sub("Ø", t)) if t else t


def fix_fonts(doc, font="arial.ttf"):
    for st in doc.styles:
        st.dxf.font = font
    for layout in [doc.modelspace()] + list(doc.blocks):
        for e in layout:
            t = e.dxftype()
            if t == "DIMENSION" and e.dxf.hasattr("text"):
                e.dxf.text = clean_text(e.dxf.text)
            elif t == "MTEXT":
                e.text = clean_text(e.text)
            elif t == "TEXT":
                e.dxf.text = clean_text(e.dxf.text)


def render(src, dst, dpi=150):
    import ezdxf
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    doc = ezdxf.readfile(src)
    fix_fonts(doc)
    fig = plt.figure(figsize=(16, 11), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)
    Frontend(RenderContext(doc), MatplotlibBackend(ax), config=cfg).draw_layout(doc.modelspace(), finalize=True)
    fig.savefig(dst, dpi=dpi, facecolor="white")
    plt.close(fig)
    return dst


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render DXF to PNG with TCVN/AIGDT font fixes.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--in", dest="inp"); g.add_argument("--in-dir")
    ap.add_argument("--out"); ap.add_argument("--out-dir")
    ap.add_argument("--dpi", type=int, default=150)
    a = ap.parse_args(argv)
    try:
        if a.inp:
            pairs = [(a.inp, a.out or os.path.splitext(a.inp)[0] + ".png")]
        else:
            os.makedirs(a.out_dir, exist_ok=True)
            pairs = [(p, os.path.join(a.out_dir, os.path.splitext(os.path.basename(p))[0] + ".png"))
                     for p in sorted(glob.glob(os.path.join(a.in_dir, "*.dxf")))]
        for s, d in pairs:
            print(render(s, d, a.dpi))
    except (OSError, IOError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
