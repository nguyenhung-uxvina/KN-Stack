#!/usr/bin/env python3
"""
helix-cad-crosscheck / mutate.py — L6 positive control: is crosscheck able to SEE the errors it claims to check?

A clean "0 lỗi" from a checker is only worth something if the same checker, on the same part, catches errors that
were planted on purpose (Galaxy: Đối Chứng Dương). For one (model, drawing, registry) that PASSES, this script
plants one known fault at a time in a COPY and re-runs crosscheck:

  drawing faults (must be caught; attributed to the drawing ONLY if, in the passing baseline, another view
  witnesses that feature along the planted direction - else the drawing is not self-contradictory and the
  right answer is 'model', because the drawing is master):
    D1 move a visible circle by 1 mm (model units)   D2 enlarge a visible circle by Ø+0.5 mm
    D3 move one straight edge 1 mm across itself   D4 delete the longest visible line/arc
    D5 change a dimension text to measured + 1
  model faults (only with --model model.py following the PARAMS/build contract; should be attributed to the model):
    M1..Mn  each numeric PARAM + 1 mm (up to --max-params)

Usage
  python mutate.py --step model.step --dxf sheet.dxf --registry views.json --out mutate_report [--model model.py]
Exit 0 = baseline geometry PASS (pending X8 layer fixes allowed) and every planted fault caught AND attributed to
the expected side · 2 = otherwise · 3 = IO.
"""
import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import crosscheck as X  # noqa: E402

DELTA = 1.0
# claims that are not about geometry: excluded drawing entities (declared annotations) - a pending layer fix
# must not stop the positive control of the geometry comparison
NON_GEOMETRY = {"X8_annotation_on_geometry_layer"}


def _blocking(rep):
    return [c for c in rep["checks"] if c["status"] in ("FAIL", "CONTESTED") and c["rule_id"] not in NON_GEOMETRY]


def _views_entities(doc, reg):
    """Visible-layer entities of every view, with their view and scale."""
    out = []
    for v in reg["views"]:
        dv = X.read_view(doc, v)
        for it in dv["visible"]:
            out.append((v, it))
    return out


def _entity(doc, handle):
    return doc.entitydb.get(handle)


def _ext(p):
    a = p[1]["pts"]
    return float((a.max(0) - a.min(0)).max())


def _frame(v):
    _, r, u = X.view_frame(v["look_dir"], v["up"])
    return r, u


def _witnessed(bviews, vid, handle, world_vecs, tol):
    """In the (passing) baseline, does another view show this entity's feature along one of world_vecs?
    Only then can a fault planted on it be blamed on the drawing; otherwise the drawing is not self-contradictory
    and the right answer is 'model' (the drawing is master). Uses the baseline, never the mutated run."""
    V = bviews.get(vid)
    if not V or handle not in V["dents"]:
        return False
    band = V["dents"][handle][1]
    for W in bviews.values():
        if W is V:
            continue
        for ax, ia, sa, ib, sb in X._shared_axes(V["proj"], W["proj"]):
            if not any(abs(abs(ax @ w) - 1) < 1e-6 for w in world_vecs):
                continue
            lo, hi = X._world_interval(band, V["proj"], ia, sa, ax)
            if X._seen_extent(W["edges_ok"], W["proj"], ib, sb, ax, lo, hi, tol):
                return True
    return False


def _pick_dir(v, bviews, handle, tol):
    """Sheet direction to displace along: one another view witnesses (expected 'drawing'), else x ('model')."""
    r, u = _frame(v)
    for sheet_dir, vec in (((1.0, 0.0), r), ((0.0, 1.0), u)):
        if _witnessed(bviews, v["id"], handle, [vec], tol):
            return sheet_dir, "drawing"
    return (1.0, 0.0), "model"


def _edge_candidates(doc, v):
    """Axis-aligned straight edges of a view: (length, handle, seg_index or None, sheet p0, sheet p1).
    seg_index is the LWPOLYLINE segment; None = a LINE entity."""
    out = []
    for e, h in X._flat_entities(doc.modelspace()):
        if e.dxf.layer not in v["layers_visible"] or e.dxf.handle != h:
            continue
        if e.dxftype() == "LINE":
            segs = [(None, (e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y))]
        elif e.dxftype() == "LWPOLYLINE":
            pts = e.get_points("xyb")
            n = len(pts)
            segs = [(i, pts[i][:2], pts[(i + 1) % n][:2]) for i in range(n if e.closed else n - 1) if pts[i][2] == 0]
        else:
            continue
        for i, a, b in segs:
            if not X._in_region([a, b], v["region"]):
                continue
            dx, dy = b[0] - a[0], b[1] - a[1]
            if abs(dx) < 1e-6 or abs(dy) < 1e-6:
                out.append((float(np.hypot(dx, dy)), h, i, np.array(a, float), np.array(b, float)))
    return out


def _edge_witnessed(bviews, v, p0, p1, sheet_dir, tol):
    V = bviews.get(v["id"])
    if not V:
        return False
    band = np.array([p0, p1]) * V["k"] - V["t"]
    r, u = _frame(v)
    vec = r if sheet_dir[0] else u
    for W in bviews.values():
        if W is V:
            continue
        for ax, ia, sa, ib, sb in X._shared_axes(V["proj"], W["proj"]):
            if abs(abs(ax @ vec) - 1) > 1e-6:
                continue
            lo, hi = X._world_interval(band, V["proj"], ia, sa, ax)
            if X._seen_extent(W["edges_ok"], W["proj"], ib, sb, ax, lo, hi, tol):
                return True
    return False


def drawing_mutants(dxf_path, reg, bviews):
    import ezdxf
    base = ezdxf.readfile(dxf_path)
    ents = _views_entities(base, reg)
    picks = []
    circ = [(v, it) for v, it in ents if it["type"] == "CIRCLE"]
    lines = [(v, it) for v, it in ents if it["type"] in ("LINE", "ARC", "LWPOLYLINE", "POLYLINE")]
    if circ:
        v, it = max(circ, key=_ext)
        picks.append(("D1_move_circle", v, it["handle"]))
        picks.append(("D2_enlarge_circle", v, it["handle"]))
    tol = reg["_tol"]["tol"]
    edges = []
    for v in reg["views"]:
        for L, h, i, a, b in _edge_candidates(base, v):
            sd = (0.0, 1.0) if abs(a[1] - b[1]) < 1e-6 else (1.0, 0.0)
            edges.append((_edge_witnessed(bviews, v, a, b, sd, tol), L, v, h, i, sd))
    if edges:
        wit, L, v, h, i, sd = max(edges, key=lambda x: (x[0], x[1]))
        picks.append(("D3_shift_edge", v, (h, i, sd, "drawing" if wit else "model")))
    if lines:
        simple = [(v2, i2) for v2, i2 in lines if i2["type"] in ("LINE", "ARC")]
        if simple:
            v2, i2 = max(simple, key=_ext)
            picks.append(("D4_delete_line", v2, i2["handle"]))
    for v in reg["views"]:
        dims = X.read_view(base, v)["dims"]
        if dims:
            picks.append(("D5_dim_text", v, dims[0][0].dxf.handle))
            break
    for name, v, h in picks:
        doc = ezdxf.readfile(dxf_path)
        if name == "D3_shift_edge":
            h, seg, sd, expected = h
            e = _entity(doc, h)
            d = DELTA / float(v["scale"])
            if e.dxftype() == "LINE":
                e.translate(sd[0] * d, sd[1] * d, 0)
            else:
                pts = [list(p) for p in e.get_points("xyseb")]
                for j in (seg, (seg + 1) % len(pts)):
                    pts[j][0] += sd[0] * d
                    pts[j][1] += sd[1] * d
                e.set_points(pts, format="xyseb")
            yield name + ("_x" if sd[0] else "_y"), v["id"], h, doc, expected
            continue
        e = _entity(doc, h)
        if e is None:      # inside a block: skip with a note
            yield name, v["id"], h, None, ""
            continue
        d = DELTA / float(v["scale"])
        tol = reg["_tol"]["tol"]
        expected = "drawing"
        if name in ("D2_enlarge_circle", "D4_delete_line"):
            expected = "drawing" if _witnessed(bviews, v["id"], h, list(_frame(v)), tol) else "model"
        if name == "D1_move_circle":
            sd, expected = _pick_dir(v, bviews, h, tol)
            c = e.dxf.center
            e.dxf.center = (c.x + sd[0] * d, c.y + sd[1] * d, c.z)
            name += "_x" if sd[0] else "_y"
        elif name == "D2_enlarge_circle":
            e.dxf.radius = e.dxf.radius + 0.25 / float(v["scale"])
        elif name == "D4_delete_line":
            doc.modelspace().delete_entity(e)
        elif name == "D5_dim_text":
            lf = float(e.override().get("dimlfac", 1.0) or 1.0)
            e.dxf.text = f"{e.get_measurement() * lf + 1:g}"
        yield name, v["id"], h, doc, expected


def model_mutants(model_py, max_params):
    """Yield (name, step_path) with one PARAM + 1 mm, built in an isolated subprocess (cad_runner contract)."""
    # read PARAMS in an isolated subprocess (AI-written code never runs in this process — helix-cad-gates rule)
    probe = ("import json, runpy; g = runpy.run_path(%r, run_name='_probe'); "
             "print(json.dumps({k: v for k, v in g.get('PARAMS', {}).items() "
             "if isinstance(v, (int, float)) and not isinstance(v, bool)}))" % model_py)
    r = subprocess.run([sys.executable, "-I", "-c", probe], capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise ValueError(f"không đọc được PARAMS: {r.stderr[-300:]}")
    params = json.loads(r.stdout.strip().splitlines()[-1])
    for k in list(params)[:max_params]:
        tmp = tempfile.mkdtemp(prefix="xc_mut_")
        out = os.path.join(tmp, "m.step")
        drv = os.path.join(tmp, "drv.py")
        with open(drv, "w", encoding="utf-8") as f:
            f.write("import sys, runpy\n"
                    f"g = runpy.run_path({model_py!r}, run_name='_mut')\n"
                    "p = dict(g['PARAMS'])\n"
                    f"p[{k!r}] = p[{k!r}] + {DELTA}\n"
                    "from build123d import export_step\n"
                    f"export_step(g['build'](p), {out!r})\n")
        r = subprocess.run([sys.executable, "-I", drv], capture_output=True, text=True, timeout=300)
        yield f"M_{k}+{DELTA:g}", (out if r.returncode == 0 and os.path.exists(out) else None), r.stderr[-300:]


def run(step, dxf, registry, model_py=None, max_params=6):
    reg = X.load_registry(registry)
    base, bviews = X.run(step, dxf, copy.deepcopy(reg))
    res = {"tool": "helix-cad-crosscheck/mutate", "baseline_verdict": base["verdict"], "mutants": []}
    if _blocking(base):
        res["note"] = "Bộ gốc chưa PASS — đối chứng dương vô nghĩa khi gốc còn lỗi; sửa gốc trước."
        return res
    if base["verdict"] != "PASS":
        res["baseline_verdict"] = "PASS_GEOMETRY"
        res["note"] = "Hình học PASS; còn đề xuất sửa lớp chú thích (X8) — không ảnh hưởng đối chứng hình học."
    for name, vid, h, doc, expected in drawing_mutants(dxf, reg, bviews):
        if doc is None:
            res["mutants"].append({"name": name, "view": vid, "handle": h, "caught": None, "note": "thực thể trong khối"})
            continue
        rep, _ = X.run(step, doc, copy.deepcopy(reg))
        blk = _blocking(rep)
        res["mutants"].append({"name": name, "view": vid, "handle": h, "caught": bool(blk),
                               "attributed_to": sorted({c.get("attribution", "") for c in blk}),
                               "expected_attribution": expected, "rules": sorted({c["rule_id"] for c in blk}),
                               "blocking": [[c["rule_id"], c["view"], c.get("attribution", ""), c["message"][:160]] for c in blk]})
    if model_py:
        for name, mstep, err in model_mutants(model_py, max_params):
            if not mstep:
                res["mutants"].append({"name": name, "caught": None, "note": f"không dựng được: {err}"})
                continue
            rep, _ = X.run(mstep, dxf, copy.deepcopy(reg))
            blk = _blocking(rep)
            res["mutants"].append({"name": name, "caught": bool(blk),
                                   "attributed_to": sorted({c.get("attribution", "") for c in blk}),
                                   "expected_attribution": "model", "rules": sorted({c["rule_id"] for c in blk}),
                                   "blocking": [[c["rule_id"], c["view"], c.get("attribution", ""), c["message"][:160],
                                                 c.get("observed", "")[:80]] for c in blk]})
    done = [m for m in res["mutants"] if m["caught"] is not None]
    res["caught"] = sum(m["caught"] for m in done)
    res["total"] = len(done)
    # strict: blamed on exactly the expected side (a model fault must not also spawn a 2D fix proposal)
    res["attribution_right"] = sum(1 for m in done if m["caught"] and m["attributed_to"] == [m["expected_attribution"]])
    return res


def render_md(r):
    L = [f"# Đối chứng dương (L6) — bộ gốc {r['baseline_verdict']}", ""]
    if r.get("note"):
        L.append(r["note"])
    if r.get("total") is not None:
        L.append(f"- Bắt được {r['caught']}/{r['total']} lỗi cấy · quy đúng bên {r['attribution_right']}/{r['total']}")
    L += ["", "| Lỗi cấy | Hình | Bắt | Quy cho | Mong đợi | Luật báo |", "|---|---|---|---|---|---|"]
    for m in r["mutants"]:
        L.append(f"| {m['name']} | {m.get('view', '')} | {m['caught']} | {', '.join(m.get('attributed_to', []))} | "
                 f"{m.get('expected_attribution', '')} | {', '.join(m.get('rules', [])) or m.get('note', '')} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", required=True)
    ap.add_argument("--dxf", required=True)
    ap.add_argument("--registry", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model")
    ap.add_argument("--max-params", type=int, default=6)
    a = ap.parse_args(argv)
    try:
        r = run(a.step, a.dxf, a.registry, a.model, a.max_params)
    except (OSError, ValueError) as ex:
        print(f"LỖI: {ex}", file=sys.stderr)
        return 3
    json.dump(r, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(a.out + ".md", "w", encoding="utf-8").write(render_md(r))
    ok = (r["baseline_verdict"] in ("PASS", "PASS_GEOMETRY") and r.get("total")
          and r.get("caught") == r.get("total") == r.get("attribution_right"))
    line = [x for x in render_md(r).splitlines() if x.startswith("- Bắt được")]
    print(line[0] if line else r.get("note", ""))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
