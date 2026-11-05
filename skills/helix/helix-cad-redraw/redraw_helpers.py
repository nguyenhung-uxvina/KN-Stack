#!/usr/bin/env python3
"""
helix-cad-redraw / redraw_helpers.py — ezdxf helpers for redraw scripts. Each helper exists because the naive
way silently produced a wrong sheet (see references/redraw-rules.md, rule numbers in brackets).

  place_dim_text(dim, xy, leader)   user text position that SURVIVES render [R9]
                                    (setting dimtype bit 128 + text_midpoint by hand: render() clears the bit and
                                    the text jumps back to the middle)
  fix_180(dim)                      linear dim at angle 180° ⇒ 0° (same measurement) and points re-ordered along +x —
                                    re-rendered 180° dims put their text upside-down [R10]; reversed points flip arrows [R18]
  stretch(msp, box, f)              move vertices inside a box: LINE, LWPOLYLINE, HATCH boundary (polyline and
                                    line edges) and DIMENSION defpoints together [R11]
  explode_named(msp, names)         explode INSERTs first — geometry hidden in a block (a mirrored copy too) is
                                    not reached by stretch [R11]
  rerender_dims(msp, keep)          re-render every dim after geometry edits: the block (*D…) still shows the OLD
                                    extension lines until render() [R12]
  scale_region(msp, box, k, anchor, dim_factor)
                                    redraw a detail view at its true scale: geometry ×k about anchor, TEXT/MTEXT
                                    keep height (a second label line follows the line above it, keeping the
                                    original line spacing), HATCH keeps pattern scale, dims get defpoints×k,
                                    text "<>" and dimlfac override so they MEASURE the true value [R13]
  keep_handles(msp, regions)        handles to protect before a script deletes geometry (notes strokes) [R7]
"""
import ezdxf  # noqa: F401  (callers pass ezdxf objects)
from ezdxf import bbox
from ezdxf.math import Matrix44, Vec3


def place_dim_text(dim, xy, leader=False):
    ov = dim.override()
    ov.set_location((xy[0], xy[1]), leader=leader)
    ov.render()
    return dim


def fix_180(dim):
    if (dim.dimtype & 7) == 0 and abs(dim.dxf.get("angle", 0) - 180.0) < 0.1:
        dim.dxf.angle = 0.0
        d = dim.dxf                                    # keep defpoint2 -> defpoint3 along +x, else arrows flip (R18)
        if d.defpoint3.x < d.defpoint2.x:
            d.defpoint2, d.defpoint3 = d.defpoint3, d.defpoint2
        return True
    return False


def _inside(p, box):
    return box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]


def stretch(msp, box, f):
    """f(x, y) -> (x', y') or None. Returns number of changed vertices/entities."""
    n = 0
    for e in list(msp):
        t = e.dxftype()
        if t == "LINE":
            for key in ("start", "end"):
                p = e.dxf.get(key)
                if _inside(p, box):
                    q = f(p.x, p.y)
                    if q:
                        e.dxf.set(key, Vec3(q[0], q[1], p.z)); n += 1
        elif t == "LWPOLYLINE":
            pts = list(e.get_points("xyseb")); changed = False
            for i, q in enumerate(pts):
                if _inside(q, box):
                    r = f(q[0], q[1])
                    if r:
                        pts[i] = (r[0], r[1], *q[2:]); changed = True
            if changed:
                e.set_points(pts, "xyseb"); n += 1
        elif t == "HATCH":
            for path in e.paths:
                if hasattr(path, "vertices"):
                    vs = list(path.vertices); changed = False
                    for i, q in enumerate(vs):
                        if _inside(q, box):
                            r = f(q[0], q[1])
                            if r:
                                vs[i] = (r[0], r[1], *q[2:]); changed = True
                    if changed:
                        path.vertices = vs; n += 1
                else:
                    for ed in path.edges:
                        if ed.EDGE_TYPE == "LineEdge":
                            for key in ("start", "end"):
                                p = getattr(ed, key)
                                if _inside(p, box):
                                    r = f(p[0], p[1])
                                    if r:
                                        setattr(ed, key, (r[0], r[1])); n += 1
        elif t == "DIMENSION":
            for key in ("defpoint2", "defpoint3", "defpoint4"):
                if e.dxf.hasattr(key) and _inside(e.dxf.get(key), box):
                    p = e.dxf.get(key); q = f(p.x, p.y)
                    if q:
                        e.dxf.set(key, Vec3(q[0], q[1], p.z)); n += 1
    return n


def explode_named(msp, names):
    n = 0
    for i in list(msp.query("INSERT")):
        if i.dxf.name in names:
            i.explode(); n += 1
    return n


def rerender_dims(msp, keep=lambda e: False):
    n = 0
    for e in msp.query("DIMENSION"):
        if keep(e):
            continue
        if e.dxf.hasattr("text_midpoint"):
            e.dxf.discard("text_midpoint")
        e.dxf.dimtype = e.dxf.dimtype & ~128
        e.override().render(); n += 1
    return n


def scale_region(msp, box, k, anchor, dim_factor=None):
    M = Matrix44.translate(-anchor[0], -anchor[1], 0) @ Matrix44.scale(k, k, 1) @ Matrix44.translate(anchor[0], anchor[1], 0)
    texts, measured = [], []
    for e in list(msp):
        try:
            b = bbox.extents([e])
        except Exception:
            continue
        if not b.has_data or not _inside((b.center.x, b.center.y), box):
            continue
        t = e.dxftype()
        if t in ("TEXT", "MTEXT"):
            texts.append((e, Vec3(e.dxf.insert)))
        elif t == "DIMENSION":
            for key in ("defpoint", "defpoint2", "defpoint3", "defpoint4"):
                if e.dxf.hasattr(key):
                    e.dxf.set(key, M.transform(e.dxf.get(key)))
            fix_180(e)
            # hand-placed text of a small detail does NOT survive scaling (it floats away from its dim line):
            # drop it and let the renderer place the text, after fix_180 so it reads upright.
            if e.dxf.hasattr("text_midpoint"):
                e.dxf.discard("text_midpoint")
            e.dxf.dimtype = e.dxf.dimtype & ~128
            e.dxf.text = "<>"
            ov = e.override()
            if dim_factor:
                ov.update({"dimlfac": dim_factor}); ov.commit()      # stored in XDATA, survives re-render in CAD
            ov.render()
            measured.append(round(e.get_measurement() * (dim_factor or 1), 2))
        elif t == "HATCH":
            ps = e.dxf.get("pattern_scale", 1) if not e.dxf.solid_fill else None
            e.transform(M)
            if ps is not None and e.pattern:
                e.set_pattern_fill(e.dxf.pattern_name, scale=ps, angle=e.dxf.get("pattern_angle", 0))
        else:
            e.transform(M)
    new = {}
    for e, p0 in sorted(texts, key=lambda c: -c[1].y):
        parents = [(e2, q0) for e2, q0 in texts if e2 is not e and 0 < q0.y - p0.y < 50 and abs(q0.x - p0.x) < 120 and id(e2) in new]
        if parents:
            e2, q0 = min(parents, key=lambda c: c[1].y - p0.y)
            new[id(e)] = new[id(e2)] + (p0 - q0)
        else:
            new[id(e)] = M.transform(p0)
        e.dxf.insert = new[id(e)]
    return measured


def keep_handles(msp, regions, max_size=60.0):
    from notes_strokes import strokes_in
    out = set()
    for reg in regions:
        out |= {e.dxf.handle for e in strokes_in(msp, reg, max_size)}
    return out
