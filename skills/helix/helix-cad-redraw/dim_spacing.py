#!/usr/bin/env python3
"""
helix-cad-redraw / dim_spacing.py — deterministic DIMENSION-LINE SPACING gate + fixer for 2D DXF sheets.

Why: a redraw can pass "no overlapping text" and still put dimension lines on (or 1-3 mm from) the outline.
ISO 129 / TCVN wants the first dimension line ~7-10 mm (paper) off the outline and tiers spaced so text reads.

Paper mm = model units / paper_scale. paper_scale = |xscale| of the title-frame INSERT (name matches
--frame-regex), or --paper-scale. Linear/aligned dims only (dimtype 0/1).

  check  : report every linear dim whose line is < --min mm (paper) from its nearer measured point.   exit 0/2
  fix    : move such dims out to --target mm (paper), then keep tiers readable. Overwrites --out (or input).

  F-ORIENT first: measured points running against the dim direction are swapped (ezdxf otherwise flips the
           arrows and overshoots the dim line by one arrow length at both ends).
Fix rules (each one is a failure that actually happened on a real redraw — see references/redraw-rules.md):
  MATCH    'the original' of a dim = same value, parallel, BOTH measured points within 5 mm (paper) — value
           alone, or a 20 mm window, matched the wrong one of several equal values.
  F-ORIG   with --orig: a dim the ORIGINAL also placed ACROSS the part (< 1 mm) is kept (deliberate).
  F-TIER   with --orig: if the original placed the same value farther than --target, reuse that distance
           (spreading everything to exactly --target collapsed a 2-tier stack into one line).
  F-ORIGSIDE with --orig: the original drew the same value, same direction, far enough ⇒ take its SIDE too
           (heuristics once pushed a handle dimension into the handle the original dimensioned from outside).
  F-SIDE   otherwise outward = away from nearby geometry centroid, BUT flip when the other side has fewer strokes whose
           BOX crosses the band between the measured point and the new line (centroid picked the side through
           the part; counting stroke centres missed the part body, whose centre lies far from the edge).
  F-CARRY  when a dim moves out by d, parallel dims further out on the same side whose spans overlap move by the
           same d (keeps the original tier spacing) — unless that would put them < --min from their OWN
           measured points or between them (carry once dragged a dim onto its own extension points).
  F-STACK  then any two parallel, span-overlapping dims closer than --tier-gap mm push the longer one out one
           tier. --tier-gap defaults to 4 mm (2.5 mm text + gap; originals routinely stack at ~4.4 mm, and a
           7 mm threshold cascaded a 3-tier stack into the view title).
  F-FRAME-IN a dim already crossing the border (placed by the drawing script) is pulled inside if it can stay
           >= --min from its points; otherwise `check` keeps reporting it.
  F-FRAME  a target outside the sheet border flips side; if both sides leave the border the dim is left as is
           (and reported). `check` also lists dims whose rendered geometry is outside the border.
  Text: only discard text_midpoint on dims this tool moves; never set dimtype bit 128 by hand (ezdxf clears it
  on render) — use DimStyleOverride.set_location() in the drawing script instead.

Usage:
  python dim_spacing.py check <dxf> [<dxf> ...] [--min 5] [--paper-scale K] [--json]
  python dim_spacing.py fix <dxf> [--orig <original.dxf>] [--out <dxf>] [--target 7] [--min 5] [--tier-gap 4]
Exit: 0 ok · 2 close dims remain (check) · 3 usage/IO error.
"""
import argparse
import json
import math
import re
import sys

import ezdxf
from ezdxf import bbox

import os  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # sibling text_overlap.py

FRAME_RE = r"(?i)^(khung ?ten|title)"


def paper_scale(msp, frame_regex=FRAME_RE, override=None):
    if override:
        return float(override)
    rx = re.compile(frame_regex)
    for e in msp.query("INSERT"):
        if rx.search(e.dxf.name):
            return abs(e.dxf.xscale) or 1.0
    return 1.0


def frame_box(msp, frame_regex=FRAME_RE):
    """Inner drawing border = the SMALLEST closed outline (closed LWPOLYLINE with >= 4 vertices, or a paper-frame
    INSERT) that contains the title block (5 mm paper tolerance — title blocks often poke ~2 mm past the border) (INSERT matching frame_regex). No title block ⇒ None (no guard).
    ('Largest closed polyline' picked part outlines on sheets whose border lives inside a block.)"""
    rx = re.compile(frame_regex)
    tb = None
    for i in msp.query("INSERT"):
        if rx.search(i.dxf.name):
            b = bbox.extents([i])
            if b.has_data:
                tb = (b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y); tol = 5.0 * (abs(i.dxf.xscale) or 1.0); break
    if tb is None:
        return None
    best = None
    cands = [e for e in msp.query("LWPOLYLINE") if e.closed and len(e) >= 4] +             [i for i in msp.query("INSERT") if not rx.search(i.dxf.name)]
    for e in cands:
        b = bbox.extents([e])
        if not b.has_data:
            continue
        box = (b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y)
        if box[0] <= tb[0] + tol and box[1] <= tb[1] + tol and box[2] >= tb[2] - tol and box[3] >= tb[3] - tol:
            area = (box[2] - box[0]) * (box[3] - box[1])
            if best is None or area < best[0]:
                best = (area, box)
    return best[1] if best else None


def dim_extent(e):
    """Extent of a dim's rendered geometry; MTEXT via estimate (ezdxf bbox of width-less MTEXT is wrong)."""
    from text_overlap import mtext_box
    xs, ys = [], []
    for v in e.virtual_entities():
        if v.dxftype() == "MTEXT":
            r = mtext_box(v)
            if r:
                xs += [r[0], r[2]]; ys += [r[1], r[3]]
            continue
        try:
            b = bbox.extents([v])
        except Exception:
            continue
        if b.has_data:
            xs += [b.extmin.x, b.extmax.x]; ys += [b.extmin.y, b.extmax.y]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


def _inside_box(pt, box, tol=0.0):
    return box is None or (box[0] - tol <= pt[0] <= box[2] + tol and box[1] - tol <= pt[1] <= box[3] + tol)


def outside_frame(path, frame_regex=FRAME_RE):
    """Dims whose rendered geometry leaves the sheet border. A spacing fix once pushed a 3-tier stack's outer
    dim ABOVE the border; no gap/overlap check looks there."""
    doc = ezdxf.readfile(path); m = doc.modelspace(); fb = frame_box(m, frame_regex); k = paper_scale(m, frame_regex)
    if fb is None:
        return []
    out = []
    for e in m.query("DIMENSION"):
        x = dim_extent(e)
        if x and not (_inside_box(x[:2], fb, 0.2 * k) and _inside_box(x[2:], fb, 0.2 * k)):
            # kind: "outward" = the dim line/text sits beyond the border (fix: pull in, or move the view);
            # "view" = the measured feature itself is within 2 mm of the border, or not a linear dim
            # (arrows/extensions/radius text poke out) — fix the VIEW position in the drawing script.
            kind = "view"
            if _linear(e):
                d = e.dxf
                pts_in = all(_inside_box((p.x, p.y), fb, -2.0 * k) for p in (d.defpoint2, d.defpoint3))
                kind = "outward" if pts_in else "view"
            out.append({"value": value(doc, e), "handle": e.dxf.handle, "kind": kind})
    return out


def _linear(e):
    return e.dxftype() == "DIMENSION" and (e.dimtype & 7) in (0, 1) and e.dxf.hasattr("defpoint2") and e.dxf.hasattr("defpoint3")


def direction(e):
    d = e.dxf
    if (e.dimtype & 7) == 0:
        a = math.radians(d.get("angle", 0))
        return (math.cos(a), math.sin(a))
    v = (d.defpoint3.x - d.defpoint2.x, d.defpoint3.y - d.defpoint2.y)
    L = math.hypot(*v) or 1.0
    return (v[0] / L, v[1] / L)


def value(doc, e):
    try:
        st = e.dxf.dimstyle
        lf = doc.dimstyles.get(st).dxf.get("dimlfac", 1) if st in doc.dimstyles else 1
        return round(e.get_measurement() * lf, 1)
    except Exception:
        return None


def gap(e, k):
    """Paper-mm distance from the dimension line to the NEARER measured point."""
    d = e.dxf; u = direction(e); n = (-u[1], u[0])
    return min(abs((p.x - d.defpoint.x) * n[0] + (p.y - d.defpoint.y) * n[1]) for p in (d.defpoint2, d.defpoint3)) / k


def _frame(e):
    d = e.dxf; u = direction(e); n = (-u[1], u[0])
    s = d.defpoint.x * n[0] + d.defpoint.y * n[1]
    q = sorted(p.x * u[0] + p.y * u[1] for p in (d.defpoint2, d.defpoint3))
    near = min((d.defpoint2, d.defpoint3), key=lambda p: abs((p.x * n[0] + p.y * n[1]) - s))
    side = 1 if s - (near.x * n[0] + near.y * n[1]) >= 0 else -1
    return u, n, s, q[0], q[1], side


def check(path, min_mm=5.0, k=None, frame_regex=FRAME_RE):
    doc = ezdxf.readfile(path); m = doc.modelspace(); k = paper_scale(m, frame_regex, k)
    out = []
    for e in m.query("DIMENSION"):
        if _linear(e):
            g = gap(e, k)
            if g < min_mm:
                out.append({"value": value(doc, e), "text": e.dxf.get("text", ""), "gap_mm": round(g, 1), "handle": e.dxf.handle})
    return out


def reversed_points(e):
    """True when defpoint2 -> defpoint3 runs AGAINST the dimension direction. ezdxf then draws the arrows
    flipped (pointing in from outside) and the dimension line overshoots both extension lines by one arrow
    length — which is what pushed dims past the sheet border on sheets whose part sits near the border."""
    if not _linear(e):
        return False
    u = direction(e); d = e.dxf
    return ((d.defpoint3.x - d.defpoint2.x) * u[0] + (d.defpoint3.y - d.defpoint2.y) * u[1]) < -1e-9


def flipped_arrows(e, k, doc):
    """True when the RENDERED dim line runs past BOTH extension lines by ~one arrow length although the dim is
    long enough for inside arrows (> 2 arrows + gap) — the ezdxf signature of reversed measured points.
    Measures the block, so AutoCAD-made dims and legit arrows-outside small dims are not flagged."""
    if not _linear(e):
        return False
    arrows = [abs(v.dxf.xscale) for v in e.virtual_entities() if v.dxftype() == "INSERT"]
    if not arrows:
        return False                                                       # ticks / no arrows: nothing to flip
    asz = max(arrows) / k                                                  # rendered arrow size, paper mm
    u, n, s, q0, q1, _ = _frame(e)
    from text_overlap import mtext_box
    tw = 0.0
    for v in e.virtual_entities():
        if v.dxftype() == "MTEXT":
            r = mtext_box(v)
            if r:
                tw = max(tw, max(r[2] - r[0], r[3] - r[1]) / k)
    if (q1 - q0) / k <= 2 * asz + tw + 2.0:
        return False                                                       # arrows (and text) outside is legit here
    lo_over = hi_over = 0.0
    for v in e.virtual_entities():
        if v.dxftype() != "LINE":
            continue
        a, b = v.dxf.start, v.dxf.end
        da = (b.x - a.x) * u[0] + (b.y - a.y) * u[1]; L = math.hypot(b.x - a.x, b.y - a.y)
        if L < 1e-9 or abs(abs(da) - L) > 1e-6 * max(L, 1) or abs((a.x * n[0] + a.y * n[1]) - s) > 0.5 * k:
            continue
        lo, hi = sorted((a.x * u[0] + a.y * u[1], b.x * u[0] + b.y * u[1]))
        lo_over = max(lo_over, (q0 - lo) / k); hi_over = max(hi_over, (hi - q1) / k)
    return lo_over > 0.6 * asz and hi_over > 0.6 * asz


def orient(e):
    """Swap the measured points if reversed and re-render. Skips hand-placed text (bit 128): re-rendering it
    loses the position (R9) — those are reported instead. Returns True if swapped."""
    if not reversed_points(e) or (e.dimtype & 128):
        return False
    d = e.dxf
    p2, p3 = d.defpoint2, d.defpoint3
    d.defpoint2, d.defpoint3 = p3, p2
    e.override().render()
    return True


def _rerender(e, discard_text=True):
    if discard_text and e.dxf.hasattr("text_midpoint"):
        e.dxf.discard("text_midpoint")
    e.dxf.dimtype = e.dxf.dimtype & ~128
    e.override().render()


def _stack(m, k, target, tier_gap, rounds=12, fb=None):
    dims = [e for e in m.query("DIMENSION") if _linear(e)]
    moved = 0
    for _ in range(rounds):
        changed = False
        for i, a in enumerate(dims):
            for b in dims[i + 1:]:
                ua, na, sa, a0, a1, ha = _frame(a); ub, nb, sb, b0, b1, hb = _frame(b)
                dot_u = ua[0] * ub[0] + ua[1] * ub[1]; dot_n = na[0] * nb[0] + na[1] * nb[1]
                if abs(dot_u) < 0.999 or ha * dot_n * hb < 0:
                    continue
                if dot_n < 0:
                    sb, b0, b1 = -sb, -b1, -b0
                if min(a1, b1) - max(a0, b0) < 2 * k or abs(sa - sb) >= tier_gap * k:
                    continue
                longer, shorter = (a, b) if (a1 - a0) >= (b1 - b0) else (b, a)
                u, n, s, _, _, h = _frame(longer); _, n2, s2, _, _, _ = _frame(shorter)
                s2 = s2 if (n[0] * n2[0] + n[1] * n2[1]) > 0 else -s2
                dl = (s2 + h * target * k) - s
                d = longer.dxf
                nxt = (d.defpoint.x + dl * n[0], d.defpoint.y + dl * n[1])
                if not _inside_box(nxt, fb):                                       # F-FRAME
                    continue
                d.defpoint = (nxt[0], nxt[1], 0)
                _rerender(longer); moved += 1; changed = True
        if not changed:
            break
    return moved


def _pull_inside(m, k, min_mm, fb):
    """A dim whose rendered geometry crosses the sheet border is pulled back toward its points by the overshoot
    (+1 mm), as long as it stays >= min_mm from them. Redraw scripts placed outer tiers 1-2 mm past the border."""
    if fb is None:
        return 0
    n_in = 0
    for e in m.query("DIMENSION"):
        if not _linear(e):
            continue
        pulled = False
        for _ in range(4):                     # re-measure: the re-rendered text can be taller than the old block's
            x = dim_extent(e)
            if not x or (_inside_box(x[:2], fb, 0.2 * k) and _inside_box(x[2:], fb, 0.2 * k)):
                break
            u, n, s, _, _, side = _frame(e)
            cs = [(x[0], x[1]), (x[2], x[1]), (x[2], x[3]), (x[0], x[3])]
            fcs = [(fb[0], fb[1]), (fb[2], fb[1]), (fb[2], fb[3]), (fb[0], fb[3])]
            over = max(side * (px * n[0] + py * n[1]) for px, py in cs) - max(side * (px * n[0] + py * n[1]) for px, py in fcs)
            if over <= 0:
                break                          # crosses along the line, not outward
            dl = -side * (over + 1.0 * k)
            old = e.dxf.defpoint
            e.dxf.defpoint = (old.x + dl * n[0], old.y + dl * n[1], 0)
            if gap(e, k) < min_mm:
                e.dxf.defpoint = old
                break
            _rerender(e); pulled = True
        n_in += pulled
    return n_in


def fix(path, orig=None, out=None, target=7.0, min_mm=5.0, tier_gap=4.0, k=None, frame_regex=FRAME_RE):
    doc = ezdxf.readfile(path); m = doc.modelspace(); k = paper_scale(m, frame_regex, k)
    orig_dims = []                     # (value, gap_mm, u, n, side, mid) of every linear dim of the ORIGINAL
    if orig:
        dg = ezdxf.readfile(orig); mg = dg.modelspace(); kg = paper_scale(mg, frame_regex)
        for e in mg.query("DIMENSION"):
            if _linear(e):
                uo, no_, _, _, _, sd = _frame(e)
                p2o, p3o = e.dxf.defpoint2, e.dxf.defpoint3
                orig_dims.append((value(dg, e), gap(e, kg), uo, no_, sd, ((p2o.x, p2o.y), (p3o.x, p3o.y))))

    def off(t, pts):                   # worst endpoint offset, order-insensitive
        a, b = t[5]
        return min(max(math.dist(a, pts[0]), math.dist(b, pts[1])), max(math.dist(a, pts[1]), math.dist(b, pts[0])))

    def counterpart(v, u, pts):
        """The ORIGINAL dim that is this one: same value, parallel, BOTH measured points within 5 mm (paper).
        Value alone matched the wrong one of several 100s; a 20 mm midpoint window still swapped two equal
        dims on neighbouring views and put one onto another view's text."""
        c = [t for t in orig_dims if t[0] == v and abs(t[2][0] * u[0] + t[2][1] * u[1]) > 0.999 and off(t, pts) < 5 * k]
        return min(c, key=lambda t: off(t, pts)) if c else None
    centers, boxes = [], []
    cache = bbox.Cache()
    for e in m:
        if e.dxftype() in ("LINE", "ARC", "CIRCLE", "LWPOLYLINE", "ELLIPSE", "SPLINE"):
            try:
                b = bbox.extents([e], cache=cache)
            except Exception:
                continue
            if not b.has_data:
                continue
            if b.size.x < 150 * k and b.size.y < 150 * k:
                centers.append((b.center.x, b.center.y))
                boxes.append((b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y))   # sheet frame/border excluded
    fb = frame_box(m, frame_regex)
    n_orient = sum(orient(e) for e in m.query("DIMENSION"))                     # F-ORIENT (before anything is measured)
    moved_set, n_fix, n_carry = set(), 0, 0
    for e in list(m.query("DIMENSION")):
        if not _linear(e):
            continue
        g = gap(e, k); v = value(doc, e)
        if g >= min_mm:
            continue
        d = e.dxf; u = direction(e); n = (-u[1], u[0]); p2, p3 = d.defpoint2, d.defpoint3
        mx, my = (p2.x + p3.x) / 2, (p2.y + p3.y) / 2
        twin = counterpart(v, u, ((p2.x, p2.y), (p3.x, p3.y)))
        if twin and twin[1] < 1.0 and g < 1.0:                                   # F-ORIG
            continue
        same = [twin] if twin and min_mm <= twin[1] < 40 else []
        near = [c for c in centers if math.hypot(c[0] - mx, c[1] - my) < 30 * k] or centers or [(mx, my)]
        cx, cy = sum(c[0] for c in near) / len(near), sum(c[1] for c in near) / len(near)
        side = 1 if ((mx - cx) * n[0] + (my - cy) * n[1]) >= 0 else -1
        q0 = sorted(p.x * u[0] + p.y * u[1] for p in (p2, p3))
        dist = max(target, same[0][1] if same else 0) * k                         # F-TIER

        def strokes(h):                                                          # F-SIDE
            # count strokes whose BOX crosses the band the new dim line would sweep (point -> new line, over
            # the span). Counting only stroke CENTRES missed the part body itself (its centre lies far away).
            r = max((p2, p3), key=lambda p: h * (p.x * n[0] + p.y * n[1]))
            a = r.x * n[0] + r.y * n[1]; b = a + h * dist
            lo, hi = min(a, b) + 0.5 * k, max(a, b) - 0.01 * k
            hit = 0
            for x0, y0, x1, y1 in boxes:
                cs = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
                nn = [x * n[0] + y * n[1] for x, y in cs]; uu = [x * u[0] + y * u[1] for x, y in cs]
                if min(nn) < hi and max(nn) > lo and min(uu) < q0[1] - 0.01 * k and max(uu) > q0[0] + 0.01 * k:
                    hit += 1
            return hit
        if same:                                                                 # F-ORIGSIDE: the original's side wins
            _, _, _, n0, sd0, _ = same[0]
            side = sd0 * (1 if (n0[0] * n[0] + n0[1] * n[1]) > 0 else -1)
        elif strokes(-side) < strokes(side):
            side = -side
        def target_pt(h):
            ref = max((p2, p3), key=lambda p: h * (p.x * n[0] + p.y * n[1]))
            return (ref.x + h * dist * n[0], ref.y + h * dist * n[1])
        new = target_pt(side)
        if not _inside_box(new, fb):                                             # F-FRAME: never leave the border
            side = -side; new = target_pt(side)
            if not _inside_box(new, fb):
                continue
        t = (d.defpoint.x - new[0]) * u[0] + (d.defpoint.y - new[1]) * u[1]
        s_old = d.defpoint.x * n[0] + d.defpoint.y * n[1]
        d.defpoint = (new[0] + t * u[0], new[1] + t * u[1], 0)
        delta = (d.defpoint.x * n[0] + d.defpoint.y * n[1]) - s_old
        _rerender(e); moved_set.add(id(e)); n_fix += 1
        if delta * side > 0:                                                     # F-CARRY
            for o in m.query("DIMENSION"):
                if o is e or not _linear(o) or id(o) in moved_set:
                    continue
                uo = direction(o)
                if abs(uo[0] * u[0] + uo[1] * u[1]) < 0.999:
                    continue
                so = o.dxf.defpoint.x * n[0] + o.dxf.defpoint.y * n[1]
                qo = sorted(pp.x * u[0] + pp.y * u[1] for pp in (o.dxf.defpoint2, o.dxf.defpoint3))
                if (so - s_old) * side <= 0 or abs(so - s_old) > 40 * k or min(q0[1], qo[1]) - max(q0[0], qo[0]) < 2 * k:
                    continue
                old_dp = o.dxf.defpoint
                o.dxf.defpoint = (old_dp.x + delta * n[0], old_dp.y + delta * n[1], 0)
                sn = [pp.x * n[0] + pp.y * n[1] for pp in (o.dxf.defpoint2, o.dxf.defpoint3)]
                if gap(o, k) < min_mm or min(sn) < so + delta < max(sn) or not _inside_box(o.dxf.defpoint, fb):   # carry guard
                    o.dxf.defpoint = old_dp
                    continue
                _rerender(o); moved_set.add(id(o)); n_carry += 1
    n_stack = _stack(m, k, target, tier_gap, fb=fb)                                       # F-STACK
    n_in = _pull_inside(m, k, min_mm, fb)                                         # F-FRAME-IN
    doc.saveas(out or path)
    return {"oriented": n_orient, "moved": n_fix, "carried": n_carry, "stacked": n_stack, "pulled_inside": n_in}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check"); c.add_argument("dxf", nargs="+"); c.add_argument("--min", type=float, default=5.0)
    c.add_argument("--orig-dir", help="folder of the ORIGINAL sheets (same file names): flipped-arrow flags the original "
                                      "also has (AutoCAD's own arrows-outside choice) are not counted")
    c.add_argument("--paper-scale", type=float); c.add_argument("--frame-regex", default=FRAME_RE); c.add_argument("--json", action="store_true")
    f = sub.add_parser("fix"); f.add_argument("dxf"); f.add_argument("--orig"); f.add_argument("--out")
    f.add_argument("--target", type=float, default=7.0); f.add_argument("--min", type=float, default=5.0)
    f.add_argument("--tier-gap", type=float, default=4.0); f.add_argument("--paper-scale", type=float)
    f.add_argument("--frame-regex", default=FRAME_RE)
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 3
    try:
        if a.cmd == "check":
            bad = 0; rep = {}
            for p in a.dxf:
                r = check(p, a.min, a.paper_scale, a.frame_regex); o = outside_frame(p, a.frame_regex)
                dd = ezdxf.readfile(p); kk = paper_scale(dd.modelspace(), a.frame_regex, a.paper_scale)
                rv = [value(dd, e) for e in dd.modelspace().query("DIMENSION") if flipped_arrows(e, kk, dd)]
                if a.orig_dir and rv:
                    op = os.path.join(a.orig_dir, os.path.basename(p))
                    if os.path.exists(op):
                        od = ezdxf.readfile(op); ok_ = paper_scale(od.modelspace(), a.frame_regex)
                        for v in [value(od, e) for e in od.modelspace().query("DIMENSION") if flipped_arrows(e, ok_, od)]:
                            if v in rv:
                                rv.remove(v)
                rep[p] = {"close": r, "outside_frame": o, "reversed": rv}; bad += bool(r or o or rv)
                if not a.json:
                    print(f"{p}: {len(r)} dims < {a.min:g} mm" + (": " + "; ".join(f"{x['value']}@{x['gap_mm']}" for x in r[:12]) if r else "")
                          + (f" · {len(o)} OUTSIDE FRAME: " + "; ".join(f"{x['value']}({x['kind']})" for x in o[:8]) if o else "")
                          + (f" · {len(rv)} FLIPPED ARROWS (reversed points): " + "; ".join(map(str, rv[:8])) if rv else ""))
            if a.json:
                print(json.dumps(rep, ensure_ascii=False, indent=1))
            return 2 if bad else 0
        r = fix(a.dxf, a.orig, a.out, a.target, a.min, a.tier_gap, a.paper_scale, a.frame_regex)
        print(json.dumps(r))
        return 0
    except (IOError, ezdxf.DXFError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
