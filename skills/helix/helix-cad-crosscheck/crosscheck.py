#!/usr/bin/env python3
"""
helix-cad-crosscheck / crosscheck.py — check a 3D model BACK against the 2D drawing it was built from.

The 2D drawing is the master. The 3D model is a witness: every declared drawing view is re-projected from the model
(OpenCascade hidden-line removal, parallel projection) and compared with the DXF entities of that view. A mismatch is
the MODEL's by default (it must follow the drawing). It is blamed on the DRAWING only when the drawing contradicts
itself, i.e. another view that SEES the direction of the disagreement agrees with the model and not with this view:
  * default / no other view can see the disagreement direction  -> attribution "model"      -> FAIL (fix the model)
  * another view arbitrates along that axis, siding with model   -> attribution "drawing"    -> CONTESTED (2D fix proposal)
  * a declared simplification covers it                          -> attribution "simplified" -> INFO
One view's word never overrides the drawing: a hole drawn 1 mm off in X in the plan, with only a side view (which
cannot see X), stays a model FAIL. "unknown" (CONTESTED, human) is left for configuration errors (empty view region)
and X7 cases where two views disagree with each other AND with the model.
Numbers are computed here, never by an LLM. Layers (research 2026-11-11, RESEARCH_kiem-nhat-quan-2d-3d):
  X1 view extents (L1) · X2 visible edges both ways (L2) · X3 hidden edges (L2) · X4 holes (L3)
  X5 dimension text vs drawn geometry (L3, 2D self-consistency) · X6 dimension feet on model geometry (L3)
  X7 extents shared by two views (2D vs 2D) · X0 model properties (L1, INFO unless the registry states expected values)
Simplifications (L5) come from the registry; seeded-fault control (L6) is mutate.py.

Usage
  python crosscheck.py --step model.step --dxf sheet.dxf --registry views.json --out xcheck_report [--png-dir DIR]
Exit 0 PASS · 2 FAIL/CONTESTED · 3 IO/config error.  Report format = helix-cad-gates (checks[] with rule_id/status),
plus `attribution` per check and drawing_fix_proposals[] for audit_claims and the drawing-fix agent.
"""
import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np

VERSION = "1.0"
BIG = 10000.0


# ── small vector helpers ────────────────────────────────────────────────────────────────────────────────

def _unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("zero vector")
    return v / n


def view_frame(look_dir, up):
    """Screen axes for a viewer looking along look_dir: right = d x up, up' = right x d (OCC HLR uses the same)."""
    d = _unit(look_dir)
    r = _unit(np.cross(d, _unit(up)))
    u = _unit(np.cross(r, d))
    return d, r, u


# ── registry ────────────────────────────────────────────────────────────────────────────────────────────

DEFAULTS = {"tol": 0.2, "tol_dia": 0.1, "step": 0.25, "min_cluster": 1.0, "witness_ratio": 0.6, "pair_max": 5.0}


def load_registry(path):
    with open(path, encoding="utf-8") as f:
        reg = json.load(f)
    if not reg.get("views"):
        raise ValueError("registry has no views[]")
    for v in reg["views"]:
        for k in ("id", "region", "scale", "look_dir", "up"):
            if k not in v:
                raise ValueError(f"view {v.get('id', '?')}: missing '{k}'")
        v.setdefault("kind", "projection")
        v.setdefault("layers_visible", ["0"])
        v.setdefault("layers_hidden", [])
        v.setdefault("hidden_lines", "partial")       # full | partial | none
    tol = dict(DEFAULTS)
    tol.update(reg.get("tolerances", {}))
    reg["_tol"] = tol
    reg.setdefault("simplifications", [])
    return reg


# ── DXF side ────────────────────────────────────────────────────────────────────────────────────────────

GEOM_TYPES = {"LINE", "ARC", "CIRCLE", "LWPOLYLINE", "POLYLINE", "SPLINE", "ELLIPSE"}


def _flat_entities(msp):
    for e in msp:
        t = e.dxftype()
        if t == "INSERT":
            try:
                for ve in e.virtual_entities():
                    if ve.dxftype() in GEOM_TYPES or ve.dxftype() == "DIMENSION":
                        yield ve, e.dxf.handle
            except Exception:
                continue
        elif t in GEOM_TYPES or t == "DIMENSION":
            yield e, e.dxf.handle


def _in_region(pts, reg):
    x0, y0, x1, y1 = reg
    pts = np.asarray(pts)
    inside = (pts[:, 0] >= x0) & (pts[:, 0] <= x1) & (pts[:, 1] >= y0) & (pts[:, 1] <= y1)
    return inside.mean() >= 0.5


_DASHED = ("DASH", "HIDDEN", "ACAD_ISO02", "ACAD_ISO03")


def _is_dashed(doc, e, layer):
    """Kiểu đường thực của thực thể (BYLAYER ⇒ kiểu đường của lớp) thuộc họ nét đứt / nét khuất."""
    lt = str(e.dxf.get("linetype", "BYLAYER") or "BYLAYER").upper()
    if lt == "BYLAYER":
        try:
            lt = str(doc.layers.get(layer).dxf.linetype).upper()
        except Exception:
            return False
    return any(k in lt for k in _DASHED)


def read_view(doc, view):
    """Polylines (sheet units) of one view, split into visible / hidden by layer; circles; dimensions."""
    from ezdxf import path as ezpath
    vis_l, hid_l = set(view["layers_visible"]), set(view["layers_hidden"])
    ann_regions = [a["region"] for a in view.get("annotations", []) if a.get("region")]
    ann_handles = {str(h).upper() for a in view.get("annotations", []) for h in a.get("handles", [])}
    out = {"visible": [], "hidden": [], "circles": [], "dims": [], "annotations": []}
    for e, handle in _flat_entities(doc.modelspace()):
        t = e.dxftype()
        if t == "DIMENSION":
            try:
                p = e.dxf.defpoint
                pts = [(p.x, p.y)]
                for k in ("defpoint2", "defpoint3"):
                    if e.dxf.hasattr(k):
                        q = getattr(e.dxf, k)
                        pts.append((q.x, q.y))
                if _in_region(pts, view["region"]):
                    out["dims"].append((e, pts))
            except Exception:
                pass
            continue
        layer = e.dxf.layer
        kind = "visible" if layer in vis_l else "hidden" if layer in hid_l else None
        if kind is None:
            continue
        if kind == "visible" and view.get("hidden_by_linetype", True) and _is_dashed(doc, e, layer):
            kind = "hidden"           # nét đứt (kiểu đường theo thực thể hoặc theo lớp) = nét khuất, dù nằm trên lớp nét thấy
        try:
            pts = [(q.x, q.y) for q in ezpath.make_path(e).flattening(distance=0.02)]
        except Exception:
            continue
        if len(pts) < 2 or not _in_region(pts, view["region"]):
            continue
        if str(handle).upper() in ann_handles or any(_in_region(pts, r) for r in ann_regions):
            # declared annotation / neighbouring-part outline drawn on a geometry layer
            out["annotations"].append({"handle": handle, "type": t, "layer": layer, "pts": np.asarray(pts, float)})
            continue
        out[kind].append({"handle": handle, "type": t, "pts": np.asarray(pts, float)})
        if t == "CIRCLE" and kind == "visible":
            c = e.dxf.center
            out["circles"].append({"handle": handle, "c": np.array([c.x, c.y]), "r": float(e.dxf.radius)})
    return out


# ── model side ──────────────────────────────────────────────────────────────────────────────────────────

def load_shape(step):
    from build123d import import_step
    return import_step(step)


def section_cut(shape, view):
    """kind == 'section': keep the material behind the cutting plane (viewer side removed)."""
    from build123d import Keep, Plane, split
    sec = view.get("section") or {}
    pt = sec.get("point")
    if pt is None:
        raise ValueError(f"view {view['id']}: section needs section.point")
    d = _unit(view["look_dir"])
    return split(shape, bisect_by=Plane(origin=tuple(pt), z_dir=tuple(-d)), keep=Keep.BOTTOM)


def _sample_edges(edges, step):
    """List of (edge_index, Nx2 or Nx3 array)."""
    res = []
    for i, e in enumerate(edges):
        L = e.length
        if L <= 1e-9:
            continue
        n = max(2, int(math.ceil(L / step)) + 1)
        ps = e.positions([k / (n - 1) for k in range(n)])
        res.append((i, np.array([[p.X, p.Y, p.Z] for p in ps], float)))
    return res


def project_model(shape, view, step):
    """HLR in the view frame. Returns centre c, frame, visible/hidden 2D samples, 3D edge samples (model units)."""
    d, r, u = view_frame(view["look_dir"], view["up"])
    bb = shape.bounding_box()
    c = np.array([(bb.min.X + bb.max.X) / 2, (bb.min.Y + bb.max.Y) / 2, (bb.min.Z + bb.max.Z) / 2])
    origin = tuple(c - d * BIG)
    vis, hid = shape.project_to_viewport(origin, tuple(u), tuple(c))
    vis_s = [(i, a[:, :2]) for i, a in _sample_edges(vis, step)]
    hid_s = [(i, a[:, :2]) for i, a in _sample_edges(hid, step)]
    e3 = _sample_edges(shape.edges(), step)
    return {"c": c, "d": d, "r": r, "u": u, "visible": vis_s, "hidden": hid_s, "edges3d": e3}


def to_view(pts3, proj):
    q = np.asarray(pts3, float) - proj["c"]
    return np.stack([q @ proj["r"], q @ proj["u"]], axis=1)


def model_circles(shape, view):
    """Full cylinders whose axis is parallel to the view direction -> (centre_3d, radius)."""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.BRepTools import BRepTools
    from OCP.GeomAbs import GeomAbs_Cylinder
    d = _unit(view["look_dir"])
    groups = {}
    for f in shape.faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        if ad.GetType() != GeomAbs_Cylinder:
            continue
        cyl = ad.Cylinder()
        ax = cyl.Axis()
        a = np.array([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
        if abs(abs(a @ d) - 1) > 1e-4:
            continue
        p = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()])
        p = p - (p @ d) * d                       # drop the depth component
        umin, umax, _, _ = BRepTools.UVBounds_s(f.wrapped)
        key = (round(p[0], 3), round(p[1], 3), round(p[2], 3), round(cyl.Radius(), 4))
        g = groups.setdefault(key, {"p": p, "r": cyl.Radius(), "span": 0.0})
        g["span"] = max(g["span"], umax - umin) if (umax - umin) >= 2 * math.pi - 1e-3 else g["span"] + (umax - umin)
    return [g for g in groups.values() if g["span"] >= 2 * math.pi - 1e-2]


# ── comparison helpers ──────────────────────────────────────────────────────────────────────────────────

def _densify(poly, step):
    out = [poly[0]]
    for a, b in zip(poly[:-1], poly[1:]):
        L = float(np.linalg.norm(b - a))
        n = max(1, int(math.ceil(L / step)))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return np.asarray(out)


def _tree(points):
    from scipy.spatial import cKDTree
    return cKDTree(points) if len(points) else None


def _nn(tree, pts):
    if tree is None:
        return np.full(len(pts), np.inf)
    dist, _ = tree.query(pts)
    return dist


def drawing_points(items, k, t, step):
    """Sheet polylines -> model-unit samples in the view frame: q = sheet * k - t."""
    out = []
    for it in items:
        pts = it["pts"] * k - t
        out.append((it["handle"], _densify(pts, step)))
    return out


FIT_OPTS = ("icp", "centre", "min", "max")


def fit_candidates(dxf_vis_sheet, model_vis, k, tol):
    """Per screen axis, candidate offsets t (q_model = sheet*k - t): ICP (median), bbox centre, min side, max side.
    Returns (D, tree, cand) with cand[i][opt]."""
    D = np.vstack([_densify(it["pts"] * k, 0.5) for it in dxf_vis_sheet])
    M = np.vstack([a for _, a in model_vis])
    tree = _tree(M)
    t0 = (D.min(0) + D.max(0)) / 2 - (M.min(0) + M.max(0)) / 2
    t = t0.copy()
    for _ in range(12):
        q = D - t
        dist, idx = tree.query(q)
        sel = dist < 5.0
        if sel.sum() < 3:
            break
        dt = np.median(q[sel] - M[idx[sel]], axis=0)
        t = t + dt
        if np.linalg.norm(dt) < tol / 50:
            break
    lo, hi = D.min(0) - M.min(0), D.max(0) - M.max(0)
    cand = [{"icp": t[i], "centre": t0[i], "min": lo[i], "max": hi[i]} for i in range(2)]
    return D, tree, cand


def fit_offset(dxf_vis_sheet, model_vis, k, tol, anchor=None, proj=None):
    """Single-view fit (kept for callers outside run()). Anchor fixes t; else the max-inlier candidate."""
    if anchor:
        m = to_view([anchor["model"]], proj)[0]
        s = np.array(anchor["sheet"], float) * k
        return s - m, "anchor"
    D, tree, cand = fit_candidates(dxf_vis_sheet, model_vis, k, tol)
    best = None
    for a in FIT_OPTS:
        for b in FIT_OPTS:
            c = np.array([cand[0][a], cand[1][b]])
            n = int((tree.query(D - c)[0] <= tol).sum())
            if best is None or n > best[0]:
                best = (n, c, f"auto-{a}/{b}")
    return best[1], best[2]


def joint_fit(items, tol):
    """Joint translation fit for all views. The median ICP stalls at HALF an error when one edge is wrong (points
    on edges along an axis give zero residual on it) and smears that half over every hole; fitting each view alone
    can align opposite sides of the same world axis in two views, and cross-view arbitration then compares two
    different frames. So: one alignment choice (icp / centre / min / max, in WORLD terms) per world axis, shared by
    every view that sees it, chosen to maximise the drawing points matched within tol over all views.
    items: {vid: {"proj", "D", "tree", "cand"}} (views with an anchor are left out). Returns {vid: (t, how)}."""
    keys, vmap = [], {}
    for vid, it in items.items():
        ax_keys = []
        for i in range(2):
            vec = it["proj"]["r"] if i == 0 else it["proj"]["u"]
            j = int(np.argmax(np.abs(vec)))
            key, sgn = (("w", j), 1.0 if vec[j] > 0 else -1.0) if abs(abs(vec[j]) - 1) < 1e-6 else ((vid, i), 1.0)
            if key not in keys:
                keys.append(key)
            ax_keys.append((key, sgn))
        vmap[vid] = ax_keys

    def screen_opt(opt, sgn):
        return {"min": "max", "max": "min"}.get(opt, opt) if sgn < 0 else opt

    cache = {}
    for vid, it in items.items():
        for a in FIT_OPTS:
            for b in FIT_OPTS:
                c = np.array([it["cand"][0][a], it["cand"][1][b]])
                cache[vid, a, b] = (int((it["tree"].query(it["D"] - c)[0] <= tol).sum()), c)
    import itertools
    best = None
    for combo in itertools.product(FIT_OPTS, repeat=len(keys)):
        choice = dict(zip(keys, combo))
        tot = 0
        for vid, ax_keys in vmap.items():
            (k0, s0), (k1, s1) = ax_keys
            tot += cache[vid, screen_opt(choice[k0], s0), screen_opt(choice[k1], s1)][0]
        if best is None or tot > best[0]:
            best = (tot, choice)
    out = {}
    for vid, ax_keys in vmap.items():
        (k0, s0), (k1, s1) = ax_keys
        a, b = screen_opt(best[1][k0], s0), screen_opt(best[1][k1], s1)
        out[vid] = (cache[vid, a, b][1], f"joint-{a}/{b}")
    return out


def clusters(samples, dist, tol, step, min_len):
    """Runs of consecutive unmatched samples per entity -> clusters with length and bbox."""
    res, off = [], 0
    for key, pts in samples:
        n = len(pts)
        bad = dist[off:off + n] > tol
        off += n
        i = 0
        while i < n:
            if not bad[i]:
                i += 1
                continue
            j = i
            while j < n and bad[j]:
                j += 1
            seg = pts[i:j]
            L = float(np.sum(np.linalg.norm(np.diff(seg, axis=0), axis=1))) if len(seg) > 1 else 0.0
            if L >= min_len:
                res.append({"key": key, "pts": seg, "len": L, "max_dev": float(np.max(dist[off - n + i: off - n + j])),
                            "bbox": [float(seg[:, 0].min()), float(seg[:, 1].min()), float(seg[:, 0].max()),
                                     float(seg[:, 1].max())]})
            i = j
    return res


def _shared_axes(pa, pb):
    """World axes seen by both views: list of (world_axis_vec, idx_in_a, sign_a, idx_in_b, sign_b)."""
    out = []
    for ax in np.eye(3):
        ia = [(i, s) for i, s in ((0, pa["r"] @ ax), (1, pa["u"] @ ax)) if abs(abs(s) - 1) < 1e-6]
        ib = [(i, s) for i, s in ((0, pb["r"] @ ax), (1, pb["u"] @ ax)) if abs(abs(s) - 1) < 1e-6]
        if ia and ib:
            out.append((ax, ia[0][0], ia[0][1], ib[0][0], ib[0][1]))
    return out


def _world_interval(pts, proj, idx, sign, ax):
    w = proj["c"] @ ax + sign * pts[:, idx]
    return float(w.min()), float(w.max())


def _const_at(arrays_or_clusters, proj, idx, sign, ax, coord, tol):
    """True if one of the polylines is (almost) constant along ax at world coordinate `coord`."""
    for a in arrays_or_clusters:
        pts = a["pts"] if isinstance(a, dict) else a
        lo, hi = _world_interval(pts, proj, idx, sign, ax)
        if hi - lo <= tol and abs((lo + hi) / 2 - coord) <= tol:
            return True
    return False


def _is_whole(V, cl, side):
    """Does _feature_band return the whole feature (true ends) rather than an unmatched run trimmed near corners?"""
    h = "_h" if cl.get("hidden") else ""
    if side == "model":
        return cl["key"] in V["medges" + h]
    return V["dents" + h].get(cl["key"], (None,))[0] in ("CIRCLE", "ARC", "ELLIPSE", "LINE")


def _seen_extent(arrays, proj, idx, sign, ax, lo, hi, tol):
    """Does view W show a feature occupying [lo, hi] along world axis ax?
    - one edge spanning [lo, hi] (circle seen face-on, line along ax), or two edges constant at lo and hi
      (hole seen side-on);
    - for a degenerate band (an edge constant along ax = a silhouette), an edge that starts or ends there
      (the circle's extreme in the other view)."""
    if _const_at(arrays, proj, idx, sign, ax, lo, tol) and _const_at(arrays, proj, idx, sign, ax, hi, tol):
        return True
    degenerate = hi - lo <= tol
    for a in arrays:
        pts = a["pts"] if isinstance(a, dict) else a
        l2, h2 = _world_interval(pts, proj, idx, sign, ax)
        if abs(l2 - lo) <= tol and abs(h2 - hi) <= tol:
            return True
        if degenerate and (abs(l2 - lo) <= tol or abs(h2 - lo) <= tol):
            return True
    return False


def _feature_band(V, cl, side):
    """Whole feature behind a cluster: the full model HLR edge, or the full DXF line/circle/arc; else the fragment
    (a polyline may be a whole outline, so only its unmatched run is used)."""
    h = "_h" if cl.get("hidden") else ""
    if side == "model":
        return V["medges" + h].get(cl["key"], cl["pts"])
    typ, pts = V["dents" + h].get(cl["key"], (None, None))
    return pts if typ in ("CIRCLE", "ARC", "ELLIPSE", "LINE") else cl["pts"]


def _in_simplification(cl, view_id, reg, side):
    for s in reg["simplifications"]:
        if s.get("view", "*") not in ("*", view_id):
            continue
        if s.get("side", "both") not in ("both", side):
            continue
        bx = s.get("region_view")
        if bx is None:
            return s
        x0, y0, x1, y1 = bx
        b = cl["bbox"]
        if b[0] >= x0 - 1e-6 and b[1] >= y0 - 1e-6 and b[2] <= x1 + 1e-6 and b[3] <= y1 + 1e-6:
            return s
    return None


# ── report ──────────────────────────────────────────────────────────────────────────────────────────────

class Report:
    def __init__(self):
        self.checks, self.proposals = [], []

    def add(self, rule, status, view, message, observed="", expected="", attribution="", severity="",
            locator="", fix="", data=None):
        c = {"rule_id": rule, "status": status, "view": view, "message": message, "observed": observed,
             "expected": expected, "attribution": attribution, "severity": severity, "locator": locator,
             "fix_hint": fix}
        if data:
            c["data"] = data
        self.checks.append(c)
        return c


STATUS_OF = {"model": "FAIL", "drawing": "CONTESTED", "unknown": "CONTESTED", "simplified": "INFO"}


def _fmt_box(b, nd=1):
    return "[" + ", ".join(f"{x:.{nd}f}" for x in b) + "]"


# ── main check ──────────────────────────────────────────────────────────────────────────────────────────

def run(step, dxf, registry):
    import ezdxf
    reg = load_registry(registry) if isinstance(registry, str) else registry
    T = reg["_tol"]
    shape = load_shape(step) if isinstance(step, str) else step
    doc = ezdxf.readfile(dxf) if isinstance(dxf, str) else dxf
    rep = Report()

    # X0 model properties (L1)
    vol, area = float(shape.volume), float(shape.area)
    ctr = shape.center()
    rep.add("X0_model_props", "INFO", "*", "Thuộc tính mô hình (CAx-IF GVP)",
            observed=f"V={vol:.1f} mm3; A={area:.1f} mm2; G=({ctr.X:.2f}, {ctr.Y:.2f}, {ctr.Z:.2f})")
    exp = reg.get("expected") or {}
    if "volume_mm3" in exp:
        dev = abs(vol - exp["volume_mm3"]) / exp["volume_mm3"] * 100
        lim = exp.get("tolerance_pct", 0.5)
        rep.add("X0_volume", "PASS" if dev <= lim else "FAIL", "*", "Thể tích so giá trị khai trong sổ hình chiếu",
                observed=f"{vol:.1f} ({dev:.2f} %)", expected=f"{exp['volume_mm3']} ± {lim} %",
                attribution="" if dev <= lim else "model")

    views = {}
    for v in reg["views"]:
        k = float(v["scale"])
        sh = section_cut(shape, v) if v["kind"] == "section" else shape
        proj = project_model(sh, v, T["step"])
        dv = read_view(doc, v)
        if not dv["visible"]:
            rep.add("X2_visible", "FAIL", v["id"], "Không có nét thấy nào của hình chiếu trong vùng/lớp khai báo",
                    attribution="unknown", locator=f"region {v['region']}", fix="Kiểm region, layers_visible")
            continue
        views[v["id"]] = {"v": v, "k": k, "proj": proj, "dv": dv, "shape": sh}
        # X8: annotation drawn on a geometry layer (declared in the registry) -> not geometry, but a 2D fix:
        # the layer is what downstream tools (nesting, CAM, ingest) trust to mean "edge of the part"
        reasons = "; ".join(a.get("reason", "") for a in v.get("annotations", []))
        for it in dv["annotations"]:
            b = [float(it["pts"][:, 0].min()), float(it["pts"][:, 1].min()),
                 float(it["pts"][:, 0].max()), float(it["pts"][:, 1].max())]
            rep.add("X8_annotation_on_geometry_layer", "CONTESTED", v["id"],
                    f"Chú thích vẽ trên lớp nét hình học '{it['layer']}' ({it['type']}). {reasons}",
                    observed=f"thực thể DXF {it['handle']} vùng tờ {_fmt_box(b)}", expected="lớp chú thích/kích thước",
                    attribution="drawing", locator=f"{v['id']}:{it['handle']}",
                    fix="Chuyển thực thể sang lớp chú thích (kích thước / ký hiệu)")
            rep.proposals.append({"claim_rule": "X8_annotation_on_geometry_layer", "view": v["id"],
                                  "action": "move_to_annotation_layer", "dxf_handle": it["handle"],
                                  "region_sheet": b, "witness_views": [], "reason": reasons})

    # joint translation fit across views (anchors fix their own view)
    to_fit = {}
    for vid, V in views.items():
        v = V["v"]
        if v.get("anchor"):
            V["t"], V["how"] = fit_offset(V["dv"]["visible"], V["proj"]["visible"], V["k"], T["tol"], v["anchor"],
                                          V["proj"])
        else:
            D, tree, cand = fit_candidates(V["dv"]["visible"], V["proj"]["visible"], V["k"], T["tol"])
            to_fit[vid] = {"proj": V["proj"], "D": D, "tree": tree, "cand": cand}
    for vid, (t, how) in joint_fit(to_fit, T["tol"]).items():
        views[vid]["t"], views[vid]["how"] = t, how
    for V in views.values():
        V["Dv"] = drawing_points(V["dv"]["visible"], V["k"], V["t"], T["step"])
        V["Dh"] = drawing_points(V["dv"]["hidden"], V["k"], V["t"], T["step"])

    # pre-compute drawing trees per view (visible + hidden) for witness tests
    for V in views.values():
        allD = [a for _, a in V["Dv"]] + [a for _, a in V["Dh"]]
        V["treeD"] = _tree(np.vstack(allD)) if allD else None
        Mv = np.vstack([a for _, a in V["proj"]["visible"]]) if V["proj"]["visible"] else np.zeros((0, 2))
        Mh = np.vstack([a for _, a in V["proj"]["hidden"]]) if V["proj"]["hidden"] else np.zeros((0, 2))
        V["Mv"], V["Mh"] = Mv, Mh
        V["treeMv"], V["treeMall"] = _tree(Mv), _tree(np.vstack([Mv, Mh]) if len(Mh) else Mv)

    for vid, V in views.items():
        v, k, proj, dv = V["v"], V["k"], V["proj"], V["dv"]
        tol, step, mlen = T["tol"], T["step"], T["min_cluster"]

        # X1 extents (L1)
        Dall = np.vstack([a for _, a in V["Dv"]])
        dw, dh = Dall.max(0) - Dall.min(0)
        mw, mh = V["Mv"].max(0) - V["Mv"].min(0)
        ok = abs(dw - mw) <= tol and abs(dh - mh) <= tol
        hint = ""
        if not ok and mw > 0 and mh > 0:
            rw, rh = dw / mw, dh / mh
            off = abs(rw - 1) > tol / mw and abs(rh - 1) > tol / mh
            if off and abs(rw - rh) < max(tol / mw, tol / mh, 0.002):
                hint = f"Cả hai chiều lệch cùng tỉ số {rw:.3f}: sổ khai tỉ lệ sai hoặc hình vẽ sai tỉ lệ."
        # same rule as X2: the drawing is blamed only if, on EVERY mismatching screen axis, another view that sees
        # that world axis draws the model's extent (the drawing contradicts itself)
        wit_x1 = []
        if not ok and not hint:
            arbitrated = True
            for i_ax, (dl, ml) in enumerate(((dw, mw), (dh, mh))):
                if abs(dl - ml) <= tol:
                    continue
                vec = proj["r"] if i_ax == 0 else proj["u"]
                found = False
                for wid, W in views.items():
                    if wid == vid:
                        continue
                    for ax, ia, sa, ib, sb in _shared_axes(proj, W["proj"]):
                        if abs(abs(ax @ vec) - 1) > 1e-6:
                            continue
                        DW = np.vstack([a for _, a in W["Dv"]])
                        lo, hi = _world_interval(DW, W["proj"], ib, sb, ax)
                        if abs((hi - lo) - ml) <= tol:
                            found = True
                            wit_x1.append(wid)
                arbitrated &= found
            if not arbitrated:
                wit_x1 = []
        att_x1 = "" if ok else ("drawing" if hint or wit_x1 else "model")
        fix_x1 = hint or (f"Hình {', '.join(sorted(set(wit_x1)))} vẽ đúng kích thước bao của mô hình — kiểm hình này"
                          if wit_x1 else "Mô hình theo kích thước bao của bản vẽ (gốc)")
        rep.add("X1_extents", "PASS" if ok else ("CONTESTED" if att_x1 == "drawing" else "FAIL"), vid,
                "Kích thước bao hình chiếu: bản vẽ (quy về mm thật) so mô hình chiếu",
                observed=f"{dw:.2f} × {dh:.2f}", expected=f"{mw:.2f} × {mh:.2f} ± {tol}",
                attribution=att_x1, fix=fix_x1,
                data={"fit": V["how"], "offset": [float(x) for x in V["t"]], "witness_views": sorted(set(wit_x1))})

        # X2 visible edges, both directions (L2)
        dD = _nn(V["treeMv"], np.vstack([a for _, a in V["Dv"]]))
        cl_d = clusters(V["Dv"], dD, tol, step, mlen)
        dM = _nn(_tree(Dall), V["Mv"])
        cl_m = clusters(proj["visible"], dM, tol, step, mlen)
        V["cl_d"], V["cl_m"] = cl_d, cl_m
        V["medges"] = {i: arr for i, arr in proj["visible"]}
        V["medges_h"] = {i: arr for i, arr in proj["hidden"]}
        V["dents"] = {it["handle"]: (it["type"], it["pts"] * k - V["t"]) for it in dv["visible"]}
        V["dents_h"] = {it["handle"]: (it["type"], it["pts"] * k - V["t"]) for it in dv["hidden"]}
        V["cl_mh"] = []
        allDtree = V["treeD"]
        if v["hidden_lines"] == "full" and proj["hidden"]:
            MH = np.vstack([a for _, a in proj["hidden"]])
            dMh = _nn(allDtree, MH)
            dMh[_nn(V["treeMv"], MH) <= tol] = 0.0     # hidden edge under a visible one: the visible line covers it
            V["cl_mh"] = clusters(proj["hidden"], dMh, tol, step, mlen)
            for c_ in V["cl_mh"]:
                c_["hidden"] = True
        # model HLR edges (visible + hidden) that the drawing shows: evidence for other views
        V["edges_ok"] = []
        for _, a in proj["visible"] + (proj["hidden"] if V["Dh"] else []):
            # a witness edge must be drawn over most of its length AND at both ends: an edge whose end moved
            # (a sloped edge after a step height changed) would otherwise witness the wrong coordinate
            if allDtree is not None:
                dd_ = _nn(allDtree, a)
                if (dd_ <= tol).mean() >= T["witness_ratio"] and dd_[0] <= tol and dd_[-1] <= tol:
                    V["edges_ok"].append(a)
        # drawing entities split at polyline vertices: an outline polyline is ONE entity whose ends say nothing,
        # but its vertices are where the drawing puts edges (witness tests use these segments)
        V["dsegs"] = []
        for kind_ in ("visible", "hidden"):
            for it in dv[kind_]:
                q = it["pts"] * k - V["t"]
                if it["type"] in ("LWPOLYLINE", "POLYLINE") and len(q) > 2:
                    V["dsegs"] += [q[i:i + 2] for i in range(len(q) - 1)]
                else:
                    V["dsegs"].append(q)
        if V["Dh"]:   # hidden drawn lines with no model edge at all: used as support when attributing other views
            dH = _nn(V["treeMall"], np.vstack([a for _, a in V["Dh"]]))
            V["cl_dh"] = clusters(V["Dh"], dH, tol, step, mlen)
            for c_ in V["cl_dh"]:
                c_["hidden"] = True
        else:
            V["cl_dh"] = []
        V["cov"] = (1 - (dD > tol).mean(), 1 - (dM > tol).mean())

    # attribution needs every view's clusters -> second pass.
    # Rule (drawing = master): a mismatch is the MODEL's, unless another view that SEES the direction of the
    # disagreement agrees with the model and contradicts this view - then the drawing contradicts itself.
    def _arr(seq):
        return [a[1] if isinstance(a, tuple) else a for a in seq]

    def _ctr(b):
        return (b.min(0) + b.max(0)) / 2

    def pair_of(V, cl, side):
        other = "model" if side == "drawing" else "drawing"
        pool = (V["cl_m"] + V["cl_mh"]) if side == "drawing" else (V["cl_d"] + V["cl_dh"])
        c0, f0 = _ctr(_feature_band(V, cl, side)), _ctr(cl["pts"])
        best, best_f = None, None
        for o in pool:
            ob = _feature_band(V, o, other)
            dd = float(np.linalg.norm(_ctr(ob) - c0))
            if dd <= T["pair_max"] and (best is None or dd < best[0]):
                best = (dd, ob, _is_whole(V, o, other))
            # fallback: a displaced part of a long edge - the unmatched RUNS sit side by side even when the whole
            # edges' centres are far apart (pilot 2026-11-11, sloped edge whose foot moved) -> pair by the runs
            df = float(np.linalg.norm(_ctr(o["pts"]) - f0))
            if df <= T["pair_max"] and (best_f is None or df < best_f[0]):
                best_f = (df, o["pts"], False)
        best = best or best_f
        return best[1:] if best else (None, False)

    def attribute(V, cl, side):
        vid, proj, tol = V["v"]["id"], V["proj"], T["tol"]
        others = [W for wid, W in views.items() if wid != vid]
        band = _feature_band(V, cl, side)
        # 1) another view shows the same disagreement -> two drawing views agree with each other -> model
        for W in others:
            pool = (W["cl_d"] + W["cl_dh"]) if side == "drawing" else (W["cl_m"] + W["cl_mh"])
            for ax, ia, sa, ib, sb in _shared_axes(proj, W["proj"]):
                lo, hi = _world_interval(band, proj, ia, sa, ax)
                if _const_at(pool, W["proj"], ib, sb, ax, lo, tol) or _const_at(pool, W["proj"], ib, sb, ax, hi, tol):
                    return "model", [], (f"Hình {W['v']['id']} cũng vẽ như vậy mà mô hình không có"
                                         if side == "drawing" else f"Hình {W['v']['id']} cũng không có — mô hình thừa")
        ob, ob_whole = pair_of(V, cl, side)
        if ob is not None:
            # a trimmed run loses up to tol+step at each end near a corner: compare ends only when both are whole
            whole = ob_whole and _is_whole(V, cl, side)
            # 2) displaced/resized feature: arbitrate only along axes where drawing and model disagree
            mband, dband = (ob, band) if side == "drawing" else (band, ob)
            for W in others:
                drawW = W["dsegs"]
                for ax, ia, sa, ib, sb in _shared_axes(proj, W["proj"]):
                    mlo, mhi = _world_interval(mband, proj, ia, sa, ax)
                    dlo, dhi = _world_interval(dband, proj, ia, sa, ax)
                    # a straight run constant along ax (polyline side seen across) is not shortened along ax by
                    # trimming: its coordinate is trustworthy even when it is only a fragment
                    flat = mhi - mlo <= tol and dhi - dlo <= tol
                    if whole or flat:
                        agree = abs(mlo - dlo) <= tol and abs(mhi - dhi) <= tol
                    else:
                        agree = abs((mlo + mhi) - (dlo + dhi)) / 2 <= tol
                    if agree:
                        continue                      # no disagreement along this axis: W cannot arbitrate
                    if not (whole or flat):   # fragment: its ends are not the feature's ends -> nothing to look for
                        continue
                    seen_m = _seen_extent(W["edges_ok"], W["proj"], ib, sb, ax, mlo, mhi, tol)
                    seen_d = _seen_extent(drawW, W["proj"], ib, sb, ax, dlo, dhi, tol)
                    if seen_m and not seen_d:
                        name = "XYZ"[int(np.argmax(np.abs(ax)))]
                        return "drawing", [W["v"]["id"]], (f"Hình {W['v']['id']} (thấy phương {name}) khớp mô hình, "
                                                           f"hình {vid} lệch — bản vẽ tự mâu thuẫn")
            return "model", [], "Không hình nào khác phân xử được phương lệch — theo bản vẽ (gốc)"
        # 3) present on one side only
        for W in others:
            drawW = W["dsegs"]
            for ax, ia, sa, ib, sb in _shared_axes(proj, W["proj"]):
                lo, hi = _world_interval(band, proj, ia, sa, ax)
                if side == "model":
                    if _seen_extent(W["edges_ok"], W["proj"], ib, sb, ax, lo, hi, tol):
                        return "drawing", [W["v"]["id"]], f"Hình {W['v']['id']} có đặc trưng này, hình {vid} thiếu nét"
                elif (W["v"]["hidden_lines"] == "full" and hi - lo > tol
                      and not _const_at(drawW, W["proj"], ib, sb, ax, lo, tol)
                      and not _const_at(drawW, W["proj"], ib, sb, ax, hi, tol)):
                    return "drawing", [W["v"]["id"]], (f"Hình {W['v']['id']} vẽ đủ nét khuất mà không có đặc trưng "
                                                       f"này — chỉ hình {vid} có")
        return "model", [], ("Chỉ bản vẽ có nét này — mô hình phải theo bản vẽ (gốc)" if side == "drawing"
                             else "Không hình chiếu nào của bản vẽ có đặc trưng này")

    for vid, V in views.items():
        v, proj, dv, tol, mlen = V["v"], V["proj"], V["dv"], T["tol"], T["min_cluster"]
        n_bad = 0
        groups = [("X2_drawn_not_modelled", V["cl_d"], "drawing", "Nét vẽ không có trên mô hình"),
                  ("X2_modelled_not_drawn", V["cl_m"], "model", "Cạnh mô hình không có trên bản vẽ"),
                  ("X3_hidden_drawn_not_modelled", V["cl_dh"], "drawing", "Nét khuất vẽ không có trên mô hình"),
                  ("X3_hidden_modelled_not_drawn", V["cl_mh"], "model", "Cạnh khuất mô hình không có trên bản vẽ")]
        for rule, cls, side, label in groups:
            for cl in cls:
                s_ = _in_simplification(cl, vid, reg, side)
                if s_:
                    att, wit, why = "simplified", [], s_.get("reason", "")
                else:
                    att, wit, why = attribute(V, cl, side)
                    if side == "drawing" and len(V["Mv"]):
                        lo_m, hi_m = V["Mv"].min(0), V["Mv"].max(0)
                        bb = np.array(cl["bbox"])
                        if (bb[:2] < lo_m - tol).any() or (bb[2:] > hi_m + tol).any():
                            why += (" Nét ra ngoài đường bao mô hình: nếu là chú thích vẽ trên lớp nét, kỹ sư khai "
                                    "annotations[] trong sổ hình chiếu (thành đề xuất sửa lớp trên bản vẽ).")
                n_bad += att != "simplified"
                if side == "drawing":
                    obs, loc = f"thực thể DXF {cl['key']} vùng {_fmt_box(cl['bbox'])}", f"{vid}:{cl['key']}"
                    fix = ("Dựng thêm/sửa đặc trưng trên mô hình theo bản vẽ" if att == "model"
                           else "Kiểm lại nét này trên bản vẽ (thừa hoặc sai vị trí)")
                else:
                    obs, loc = f"vùng {_fmt_box(cl['bbox'])} (mm, hệ hình chiếu)", f"{vid}:m{cl['key']}"
                    fix = ("Bỏ/sửa đặc trưng trên mô hình theo bản vẽ" if att == "model"
                           else "Bổ sung/sửa nét trên hình này")
                c = rep.add(rule, STATUS_OF[att], vid,
                            f"{label} ({cl['len']:.1f} mm, lệch tới {cl['max_dev']:.2f} mm). {why}",
                            observed=obs, expected=f"≤ {tol} mm", attribution=att, locator=loc,
                            fix="" if att == "simplified" else fix, data={"witness_views": wit} if wit else None)
                if att == "drawing":
                    rep.proposals.append({"claim_rule": c["rule_id"], "view": vid,
                                          "action": "check_or_remove" if side == "drawing" else "add_missing_line",
                                          "dxf_handle": cl["key"] if side == "drawing" else None,
                                          "region_view_mm": cl["bbox"], "witness_views": wit, "reason": why})
        cov_d, cov_m = V["cov"]
        rep.add("X2_visible", "PASS" if n_bad == 0 else "INFO", vid,
                "Nét thấy: tỉ lệ trùng hai chiều (bản vẽ→mô hình / mô hình→bản vẽ)",
                observed=f"{cov_d * 100:.1f} % / {cov_m * 100:.1f} %; {len(V['cl_d']) + len(V['cl_m'])} cụm lệch",
                expected=f"0 cụm lệch > {mlen} mm", data={"offset_mm": [float(x) for x in V["t"]], "fit": V["how"]})

        # X3 hidden edges
        if V["Dh"]:
            Dh = np.vstack([a for _, a in V["Dh"]])
            ok_h = _nn(V["treeMall"], Dh) <= tol
            ratio = float(ok_h.mean())
            st = "PASS" if ratio >= 0.95 else "INFO"     # the X3_hidden_* clusters above carry status + attribution
            rep.add("X3_hidden", st, vid, "Nét khuất trên bản vẽ nằm trên cạnh mô hình (thấy hoặc khuất)",
                    observed=f"{ratio * 100:.1f} %", expected="≥ 95 %", severity="" if st == "PASS" else "xem X3_hidden_*")
        elif v["hidden_lines"] == "full" and len(V["Mh"]):
            rep.add("X3_hidden", "CONTESTED", vid, "Sổ khai hình vẽ đủ nét khuất nhưng không có nét nào trên lớp khuất",
                    attribution="drawing", fix="Kiểm layers_hidden hoặc khai hidden_lines")

        # X4 holes / bosses along the view direction (L3)
        mc = model_circles(V["shape"], v)
        mpts = [(to_view([g["p"]], proj)[0], g["r"]) for g in mc]
        dcirc = [(cc["c"] * V["k"] - V["t"], cc["r"] * V["k"], cc["handle"]) for cc in dv["circles"]]
        used = set()
        for c2, r2, h in dcirc:
            best, bi = None, None
            for i, (p, r) in enumerate(mpts):
                if i in used:
                    continue
                dd = float(np.linalg.norm(c2 - p))
                if best is None or dd + abs(r2 - r) < best[0] + abs(r2 - best[1]):
                    best, bi = (dd, r), i
            if best and best[0] <= T["tol"] and abs(2 * r2 - 2 * best[1]) <= T["tol_dia"]:
                used.add(bi)
                continue
            msg = (f"Lỗ Ø{2 * r2:.2f} tại ({c2[0]:.2f}, {c2[1]:.2f}) không khớp lỗ mô hình"
                   + (f"; gần nhất Ø{2 * best[1]:.2f} cách {best[0]:.2f} mm" if best else "; mô hình không có lỗ nào"))
            rep.add("X4_hole", "INFO", v["id"], msg, observed=f"DXF {h}",
                    expected=f"tâm ≤ {T['tol']} mm, Ø ≤ {T['tol_dia']} mm", locator=f"{v['id']}:{h}",
                    severity="xem X2")
        for i, (p, r) in enumerate(mpts):
            if i not in used:
                rep.add("X4_hole", "INFO", v["id"], f"Lỗ mô hình Ø{2 * r:.2f} tại ({p[0]:.2f}, {p[1]:.2f}) không có trên hình",
                        locator=f"{v['id']}:m{i}", severity="xem X2")
        rep.add("X4_holes", "PASS" if len(used) == len(dcirc) == len(mpts) else "INFO", v["id"],
                "Lỗ/trụ theo phương nhìn: khớp tâm và Ø", observed=f"{len(used)} khớp / {len(dcirc)} vẽ / {len(mpts)} mô hình")

        # X5 dimension text vs drawn geometry, X6 dimension feet on model geometry
        try:
            ingest_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "helix-cad-ingest")
            sys.path.insert(0, ingest_dir)
            from drawing_tables import classify_override, override_value   # noqa: E402
        except Exception:
            classify_override = override_value = None
        n5 = n6 = 0
        for e, pts in dv["dims"]:
            h = e.dxf.handle
            txt = (e.dxf.text or "") if e.dxf.hasattr("text") else ""
            try:
                lf = float(e.override().get("dimlfac", 1.0) or 1.0)
                meas = float(e.get_measurement()) * lf
            except Exception:
                meas = None
            if txt not in ("", "<>") and override_value and meas is not None:
                val = override_value(txt.replace("<>", f"{meas:g}"))
                cls = classify_override(val, meas) if val is not None else "AGREE"
                if cls not in ("AGREE", "WITHIN_TOL"):
                    n5 += 1
                    c = rep.add("X5_dim_text", "CONTESTED", v["id"],
                                f"Chữ kích thước '{txt}' khác số đo của chính nét kích thước ({meas:.2f}) — {cls}",
                                observed=txt, expected=f"{meas:.2f}", attribution="drawing", locator=f"{v['id']}:{h}",
                                fix="Sửa chữ hoặc sửa nét; chữ là số xưởng gia công theo")
                    rep.proposals.append({"claim_rule": c["rule_id"], "view": v["id"], "action": "fix_dimension_text",
                                          "dxf_handle": h, "text": txt, "measured": round(meas, 3), "class": cls})
            dt = getattr(e.dxf, "dimtype", 0) & 7
            if dt in (0, 1) and len(pts) >= 3:
                feet = np.array(pts[1:3]) * V["k"] - V["t"]
                dist = _nn(V["treeMall"], feet)
                if np.any(dist > T["tol"]):
                    n6 += 1
                    rep.add("X6_dim_anchor", "INFO", v["id"],
                            f"Chân kích thước không chạm cạnh mô hình (lệch {float(dist.max()):.2f} mm)",
                            locator=f"{v['id']}:{h}", severity="xem X2", observed=txt or "<>")
        rep.add("X5_dim_texts", "PASS" if n5 == 0 else "INFO", v["id"], "Chữ kích thước khớp nét kích thước",
                observed=f"{len(dv['dims']) - n5}/{len(dv['dims'])}")
        rep.add("X6_dim_anchors", "PASS" if n6 == 0 else "INFO", v["id"], "Chân kích thước nằm trên hình học mô hình",
                observed=f"{len(dv['dims']) - n6}/{len(dv['dims'])} (chỉ kích thước thẳng)")

    # X7 extents shared by two views (2D vs 2D)
    ids = list(views)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            A, B = views[ids[i]], views[ids[j]]
            DA = np.vstack([a for _, a in A["Dv"]])
            DB = np.vstack([a for _, a in B["Dv"]])
            for ax, ia, sa, ib, sb in _shared_axes(A["proj"], B["proj"]):
                la, lb = float(np.ptp(DA[:, ia])), float(np.ptp(DB[:, ib]))
                name = "XYZ"[int(np.argmax(np.abs(ax)))]
                ok = abs(la - lb) <= T["tol"]
                mm = float(np.ptp(A["Mv"][:, ia]))
                att = "" if ok else ("drawing" if (abs(la - mm) <= T["tol"]) != (abs(lb - mm) <= T["tol"]) else "unknown")
                c = rep.add("X7_crossview", "PASS" if ok else "CONTESTED", f"{ids[i]}|{ids[j]}",
                            f"Chiều {name} chung của hai hình chiếu",
                            observed=f"{ids[i]} {la:.2f} · {ids[j]} {lb:.2f} · mô hình {mm:.2f}",
                            expected=f"bằng nhau ± {T['tol']}", attribution=att,
                            fix="" if ok else "Hai hình của cùng bản vẽ không cùng kích thước theo trục chung")
                if not ok:
                    bad = ids[i] if abs(la - mm) > T["tol"] else ids[j]
                    rep.proposals.append({"claim_rule": c["rule_id"], "view": bad, "action": "fix_view_extent",
                                          "axis": name, "values": {ids[i]: la, ids[j]: lb, "model": mm}})

    blocking = [c for c in rep.checks if c["status"] in ("FAIL", "CONTESTED")]
    verdict = "PASS" if not blocking else ("FAIL" if any(c["status"] == "FAIL" for c in blocking) else "CONTESTED")
    return {"tool": "helix-cad-crosscheck", "version": VERSION, "created_at": datetime.now(timezone.utc).isoformat(),
            "step": step if isinstance(step, str) else "<shape>", "dxf": dxf if isinstance(dxf, str) else "<doc>",
            "part_id": reg.get("part_id", ""), "master": "drawing", "verdict": verdict,
            "counts": {s: sum(c["status"] == s for c in rep.checks) for s in ("PASS", "FAIL", "CONTESTED", "INFO")},
            "by_attribution": {a: sum(c.get("attribution") == a for c in blocking) for a in ("model", "drawing", "unknown")},
            "checks": rep.checks, "drawing_fix_proposals": rep.proposals}, views


# ── outputs ─────────────────────────────────────────────────────────────────────────────────────────────

def render_md(rep):
    L = [f"# Kiểm ngược 3D → 2D — {rep['part_id']} — {rep['verdict']}", "",
         "Bản vẽ 2D là gốc; mô hình 3D được chiếu lại từng hình và so với bản vẽ. "
         "FAIL = sửa mô hình. CONTESTED = bản vẽ tự mâu thuẫn hoặc chưa phân định được — người quyết, xem đề xuất sửa 2D.", "",
         f"- Đếm: {rep['counts']} · quy trách nhiệm (chỉ mục chặn): {rep['by_attribution']}", "",
         "| Luật | Trạng thái | Hình | Quy cho | Nội dung | Quan sát | Kỳ vọng |", "|---|---|---|---|---|---|---|"]
    for c in rep["checks"]:
        L.append(f"| {c['rule_id']} | {c['status']} | {c['view']} | {c.get('attribution', '')} | {c['message']} | "
                 f"{c['observed']} | {c['expected']} |")
    if rep["drawing_fix_proposals"]:
        L += ["", "## Đề xuất kiểm/sửa bản vẽ 2D (chờ người duyệt — máy không sửa bản vẽ)", ""]
        for i, p in enumerate(rep["drawing_fix_proposals"], 1):
            L.append(f"{i}. `{p['action']}` · hình {p['view']} · " + json.dumps(
                {k: v for k, v in p.items() if k not in ("action", "view")}, ensure_ascii=False))
    L += ["", "Máy không phát hành và không sửa bản vẽ. Ô ký kỹ sư: ____________________"]
    return "\n".join(L) + "\n"


def render_png(views, out_dir, part=""):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for vid, V in views.items():
        fig, ax = plt.subplots(figsize=(9, 7))
        for _, a in V["proj"]["visible"]:
            ax.plot(a[:, 0], a[:, 1], color="#9ec5ff", lw=2.2)
        for _, a in V["Dv"]:
            ax.plot(a[:, 0], a[:, 1], color="#444444", lw=0.6)
        for _, a in V["Dh"]:
            ax.plot(a[:, 0], a[:, 1], color="#888888", lw=0.5, ls="--")
        for it in V["dv"].get("annotations", []):     # X8: declared annotation on a geometry layer
            a = it["pts"] * V["k"] - V["t"]
            ax.plot(a[:, 0], a[:, 1], color="#9b30d9", lw=1.6)
        for cl in V.get("cl_d", []):
            ax.plot(cl["pts"][:, 0], cl["pts"][:, 1], color="red", lw=2.0)
        for cl in V.get("cl_m", []):
            ax.plot(cl["pts"][:, 0], cl["pts"][:, 1], color="blue", lw=2.0)
        ax.set_aspect("equal")
        ax.set_title(f"{part} — hình {vid}: xanh nhạt = mô hình chiếu · đen = bản vẽ · "
                     f"ĐỎ = vẽ mà mô hình không có · XANH = mô hình có mà không vẽ · TÍM = chú thích trên lớp nét (X8)",
                     fontsize=7)
        ten = "".join("_" if c in '<>:"/\\|?*' else c for c in str(vid))        # Windows: «:» trong tên hình (vd «Tiết diện (1:5)») ⇒ tệp rỗng ADS
        p = os.path.join(out_dir, f"xcheck_{ten}.png")
        fig.savefig(p, dpi=160, bbox_inches="tight")
        plt.close(fig)
        paths.append(p)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", required=True)
    ap.add_argument("--dxf", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True, help="prefix -> .json + .md")
    ap.add_argument("--png-dir")
    a = ap.parse_args(argv)
    try:
        rep, views = run(a.step, a.dxf, a.registry)
    except (OSError, ValueError, KeyError) as ex:
        print(f"LỖI: {ex}", file=sys.stderr)
        return 3
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(rep))
    if a.png_dir:
        render_png(views, a.png_dir, rep["part_id"])
    print(f"{rep['verdict']} · {rep['counts']} · quy cho {rep['by_attribution']} · {len(rep['drawing_fix_proposals'])} đề xuất 2D")
    return 0 if rep["verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
