"""Tests for skills/helix/helix-cad-crosscheck (crosscheck.py + mutate.py).

Fixture: plate 100 x 60 x 8 with a through hole Ø10 at (70, 40), drawn at 1:2 in two views (top + left side with
hidden lines). Each case breaks ONE thing — the model or ONE view of the drawing — and checks both the verdict and
the attribution (model vs drawing), because the attribution decides whether the model or the 2D gets fixed.
Run: python -m pytest scripts/test_helix_cad_crosscheck.py -v
"""
import copy
import importlib.util
import json
import os

import numpy as np
import pytest

pytest.importorskip("build123d")
ezdxf = pytest.importorskip("ezdxf")
from build123d import Box, Cylinder, Pos  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XC_DIR = os.path.join(ROOT, "skills", "helix", "helix-cad-crosscheck")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(XC_DIR, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


X = _load("crosscheck")

K = 2.0                      # drawing scale 1:2
TOP0 = (20.0, 30.0)          # sheet position of model (x=0, y=0) in the top view
SIDE0 = (100.0, 30.0)        # sheet position of model (y=60, z=0) in the side view (screen right = -Y)

REG = {
    "part_id": "TEST-PLATE",
    "views": [
        {"id": "top", "region": [15, 25, 75, 65], "scale": K, "look_dir": [0, 0, -1], "up": [0, 1, 0],
         "layers_visible": ["V"], "layers_hidden": ["H"], "hidden_lines": "partial"},
        {"id": "side", "region": [95, 25, 140, 40], "scale": K, "look_dir": [1, 0, 0], "up": [0, 0, 1],
         "layers_visible": ["V"], "layers_hidden": ["H"], "hidden_lines": "full"},
    ],
}


def plate(hole_xy=(70, 40), extra_hole=None):
    s = Pos(50, 30, 4) * Box(100, 60, 8) - Pos(hole_xy[0], hole_xy[1], 4) * Cylinder(5, 20)
    if extra_hole:
        s = s - Pos(extra_hole[0], extra_hole[1], 4) * Cylinder(2, 20)
    return s


def drawing(hole_top=(70, 40), hole_side_y=40, dim_text="<>", extra=None):
    doc = ezdxf.new("R2018", setup=True)
    for n in ("V", "H"):
        doc.layers.add(n)
    m = doc.modelspace()
    x0, y0 = TOP0
    m.add_lwpolyline([(x0, y0), (x0 + 50, y0), (x0 + 50, y0 + 30), (x0, y0 + 30)], close=True, dxfattribs={"layer": "V"})
    m.add_circle((x0 + hole_top[0] / K, y0 + hole_top[1] / K), 5 / K, dxfattribs={"layer": "V"})
    st = doc.dimstyles.new("K2", dxfattribs={"dimlfac": K})
    d = m.add_linear_dim(base=(x0 + 25, y0 - 3), p1=(x0, y0), p2=(x0 + 50, y0), dimstyle="K2", text=dim_text,
                         dxfattribs={"layer": "D"})
    d.render()
    sx, sy = SIDE0
    m.add_lwpolyline([(sx, sy), (sx + 30, sy), (sx + 30, sy + 4), (sx, sy + 4)], close=True, dxfattribs={"layer": "V"})
    for yy in (hole_side_y - 5, hole_side_y + 5):
        xs = sx + (60 - yy) / K
        m.add_line((xs, sy), (xs, sy + 4), dxfattribs={"layer": "H"})
    if extra:
        extra(m)
    return doc


def run(shape, doc, reg=REG):
    r = copy.deepcopy(reg)
    r["_tol"] = dict(X.DEFAULTS)
    r.setdefault("simplifications", [])
    for v in r["views"]:
        v.setdefault("kind", "projection")
    rep, _ = X.run(shape, doc, r)
    return rep


def blocking(rep):
    return [c for c in rep["checks"] if c["status"] in ("FAIL", "CONTESTED")]


# ── frame convention: our projection == OCC HLR projection ─────────────────────────────────────────────

@pytest.mark.parametrize("look,up", [((0, 0, -1), (0, 1, 0)), ((1, 0, 0), (0, 0, 1)), ((0, 1, 0), (0, 0, 1)),
                                     ((0, -1, 0), (0, 0, 1)), ((-1, 0, 0), (0, 0, 1))])
def test_frame_matches_hlr(look, up):
    s = plate()
    proj = X.project_model(s, {"look_dir": look, "up": up}, 0.5)
    hlr = np.vstack([a for _, a in proj["visible"]])
    mine = X.to_view(np.vstack([a for _, a in proj["edges3d"]]), proj)
    assert np.allclose(hlr.min(0), mine.min(0), atol=1e-3) and np.allclose(hlr.max(0), mine.max(0), atol=1e-3)
    circles = X.model_circles(s, {"look_dir": look})
    if abs(look[2]) == 1:
        c = X.to_view([circles[0]["p"]], proj)[0]
        hc = [e for e in s.project_to_viewport(tuple(proj["c"] - np.array(look) * 1e4), up, tuple(proj["c"]))[0]
              if str(e.geom_type).endswith("CIRCLE")][0].arc_center
        assert np.allclose(c, [hc.X, hc.Y], atol=1e-3)


# ── behaviour ───────────────────────────────────────────────────────────────────────────────────────────

def test_consistent_passes():
    rep = run(plate(), drawing())
    assert rep["verdict"] == "PASS", [c for c in blocking(rep)]
    assert not rep["drawing_fix_proposals"]


def test_model_hole_moved_is_attributed_to_model():
    # both views of the drawing agree on y=40; the model has y=42 -> fix the MODEL
    rep = run(plate(hole_xy=(70, 42)), drawing())
    assert rep["verdict"] == "FAIL"
    assert rep["by_attribution"]["model"] >= 1
    drawn = [c for c in rep["checks"] if c["rule_id"] == "X2_drawn_not_modelled" and c["view"] == "top"]
    assert drawn and all(c["attribution"] == "model" for c in drawn)


def test_one_view_wrong_is_attributed_to_drawing():
    # top view draws the hole 1 mm off in Y; the side view also sees Y and agrees with the model
    # -> the drawing contradicts itself: propose a 2D fix, do not FAIL the model
    rep = run(plate(), drawing(hole_top=(70, 41)))
    assert rep["verdict"] == "CONTESTED"
    assert rep["by_attribution"]["model"] == 0 and rep["by_attribution"]["drawing"] >= 1
    assert any(p["view"] == "top" and p["witness_views"] == ["side"] for p in rep["drawing_fix_proposals"])


def test_disagreement_no_other_view_can_see_defaults_to_model():
    # top view draws the hole 1 mm off in X; the side view cannot see X -> nobody can arbitrate,
    # the drawing is master -> the MODEL must follow (never blame the drawing on one view's word)
    rep = run(plate(), drawing(hole_top=(71, 40)))
    assert rep["verdict"] == "FAIL"
    assert rep["by_attribution"]["drawing"] == 0 and not rep["drawing_fix_proposals"]


def test_hidden_view_wrong_is_attributed_to_drawing():
    # side view hidden lines 2 mm off; top view and model agree
    rep = run(plate(), drawing(hole_side_y=42))
    assert rep["by_attribution"]["model"] == 0
    assert rep["verdict"] == "CONTESTED"
    assert any(p["view"] == "side" and p["witness_views"] == ["top"] for p in rep["drawing_fix_proposals"])


def test_dashed_linetype_on_visible_layer_counts_as_hidden():
    # side-view hidden lines drawn on the VISIBLE layer with a DASHED linetype override (and once via a dashed layer)
    def build(by_layer):
        doc = drawing(hole_side_y=200)                          # real hidden lines moved off the part -> replaced below
        m = doc.modelspace()
        for e in [e for e in m if e.dxf.layer == "H"]:
            m.delete_entity(e)
        if by_layer:
            doc.layers.add("VD", linetype="DASHED")
        sx, sy = SIDE0
        for yy in (35, 45):
            xs = sx + (60 - yy) / K
            att = {"layer": "VD"} if by_layer else {"layer": "V", "linetype": "DASHED"}
            m.add_line((xs, sy), (xs, sy + 4), dxfattribs=att)
        return doc
    for by_layer in (False, True):
        reg = copy.deepcopy(REG)
        if by_layer:
            reg["views"][1]["layers_visible"] = ["V", "VD"]
        dv = X.read_view(build(by_layer), reg["views"][1])
        assert len(dv["hidden"]) == 2 and all(len(it["pts"]) >= 2 for it in dv["hidden"])
        rep = run(plate(), build(by_layer), reg)
        assert rep["verdict"] == "PASS", blocking(rep)
    # opt-out keeps the old behaviour: dashed line on a visible layer is compared as visible
    reg = copy.deepcopy(REG); reg["views"][1]["hidden_by_linetype"] = False
    assert not X.read_view(build(False), reg["views"][1])["hidden"]


def test_wrong_declared_scale_is_flagged_as_scale():
    reg = copy.deepcopy(REG)
    reg["views"][0]["scale"] = 2.2
    rep = run(plate(), drawing(), reg)
    x1 = [c for c in rep["checks"] if c["rule_id"] == "X1_extents" and c["view"] == "top"][0]
    assert x1["status"] == "CONTESTED" and "tỉ số" in x1["fix_hint"]


def test_dimension_text_override_is_contested():
    rep = run(plate(), drawing(dim_text="102"))
    x5 = [c for c in rep["checks"] if c["rule_id"] == "X5_dim_text"]
    assert x5 and x5[0]["status"] == "CONTESTED" and x5[0]["attribution"] == "drawing"
    assert any(p["action"] == "fix_dimension_text" for p in rep["drawing_fix_proposals"])


def test_undrawn_model_feature_fails_unless_declared_simplification():
    shape = plate(extra_hole=(20, 20))
    rep = run(shape, drawing())
    assert rep["verdict"] == "FAIL"
    m = [c for c in rep["checks"] if c["rule_id"] == "X2_modelled_not_drawn" and c["view"] == "top"]
    assert m and m[0]["attribution"] == "model"
    reg = copy.deepcopy(REG)
    reg["simplifications"] = [{"view": "*", "side": "model", "region_view": [-35, -15, -25, -5],
                               "reason": "lỗ thoát khí không vẽ (test)"}]
    rep2 = run(shape, drawing(), reg)
    m2 = [c for c in rep2["checks"] if c["rule_id"] == "X2_modelled_not_drawn" and c["view"] == "top"]
    assert m2 and all(c["status"] == "INFO" and c["attribution"] == "simplified" for c in m2)


def test_annotation_on_geometry_layer_becomes_layer_fix_not_model_fail():
    # pilot 2026-11-11: a GD&T frame drawn on the outline layer, sticking out past the part edge
    def frame(m):
        x0, y0 = TOP0
        m.add_lwpolyline([(x0 + 40, y0 + 5), (x0 + 56, y0 + 5), (x0 + 56, y0 + 8), (x0 + 40, y0 + 8)], close=True,
                         dxfattribs={"layer": "V"})
    rep = run(plate(), drawing(extra=frame))
    drawn = [c for c in rep["checks"] if c["rule_id"] == "X2_drawn_not_modelled"]
    assert rep["verdict"] == "FAIL" and drawn and any("annotations[]" in c["message"] for c in drawn)
    reg = copy.deepcopy(REG)
    reg["views"][0]["annotations"] = [{"region": [x - 0.5 if i < 2 else x + 0.5 for i, x in
                                                  enumerate((TOP0[0] + 40, TOP0[1] + 5, TOP0[0] + 56, TOP0[1] + 8))],
                                       "reason": "khung dung sai trên lớp nét"}]
    rep2 = run(plate(), drawing(extra=frame), reg)
    assert rep2["verdict"] == "CONTESTED" and rep2["by_attribution"]["model"] == 0
    assert any(c["rule_id"] == "X8_annotation_on_geometry_layer" for c in rep2["checks"])
    assert any(p["action"] == "move_to_annotation_layer" for p in rep2["drawing_fix_proposals"])


def test_annotation_by_handle_keeps_real_holes_inside_it():
    # pilot 2026-11-11: a purchased box outline on the hidden layer drawn AROUND real holes of the part
    holder = {}

    def box(m):
        x0, y0 = TOP0
        holder["h"] = m.add_lwpolyline([(x0 + 28, y0 + 13), (x0 + 42, y0 + 13), (x0 + 42, y0 + 27), (x0 + 28, y0 + 27)],
                                       close=True, dxfattribs={"layer": "H"}).dxf.handle
    doc = drawing(extra=box)
    assert run(plate(), doc)["verdict"] != "PASS"
    reg = copy.deepcopy(REG)
    reg["views"][0]["layers_hidden"] = ["H"]
    reg["views"][0]["annotations"] = [{"handles": [holder["h"]], "reason": "đường bao hàng mua (test)"}]
    rep = run(plate(), doc, reg)
    assert rep["by_attribution"]["model"] == 0
    assert [c["rule_id"] for c in blocking(rep)] == ["X8_annotation_on_geometry_layer"]
    # the real hole inside the box outline is still compared (not swallowed by the declaration)
    assert not any(c["rule_id"].startswith(("X2", "X4")) and c["status"] in ("FAIL", "CONTESTED") for c in rep["checks"])
    assert rep["counts"]["PASS"] >= 5


def test_crossview_extent_mismatch():
    def longer_side(m):
        sx, sy = SIDE0
        m.add_line((sx + 30, sy), (sx + 31, sy), dxfattribs={"layer": "V"})   # side outline 2 mm longer in Y
    rep = run(plate(), drawing(extra=longer_side))
    x7 = [c for c in rep["checks"] if c["rule_id"] == "X7_crossview"]
    assert any(c["status"] == "CONTESTED" and c["attribution"] == "drawing" for c in x7)


def test_empty_view_region_fails_not_crashes():
    reg = copy.deepcopy(REG)
    reg["views"][0]["region"] = [500, 500, 600, 600]
    rep = run(plate(), drawing(), reg)
    assert any(c["rule_id"] == "X2_visible" and c["status"] == "FAIL" for c in rep["checks"])


def test_cli_exit_codes(tmp_path):
    from build123d import export_step
    step = str(tmp_path / "m.step")
    export_step(plate(), step)
    dxf = str(tmp_path / "d.dxf")
    drawing().saveas(dxf)
    reg = str(tmp_path / "r.json")
    json.dump(REG, open(reg, "w", encoding="utf-8"))
    assert X.main(["--step", step, "--dxf", dxf, "--registry", reg, "--out", str(tmp_path / "o")]) == 0
    export_step(plate(hole_xy=(70, 42)), step)
    assert X.main(["--step", step, "--dxf", dxf, "--registry", reg, "--out", str(tmp_path / "o")]) == 2
    assert X.main(["--step", step, "--dxf", dxf, "--registry", str(tmp_path / "none.json"), "--out", "x"]) == 3


# ── L6 positive control (mutate.py) ─────────────────────────────────────────────────────────────────────

MODEL_PY = '''
from build123d import Box, Cylinder, Pos, export_step
PARAMS = {"L": 100.0, "W": 60.0, "T": 8.0, "hole_x": 70.0, "hole_y": 40.0, "hole_d": 10.0}
def build(p):
    return (Pos(p["L"] / 2, p["W"] / 2, p["T"] / 2) * Box(p["L"], p["W"], p["T"])
            - Pos(p["hole_x"], p["hole_y"], p["T"] / 2) * Cylinder(p["hole_d"] / 2, 3 * p["T"]))
if __name__ == "__main__":
    export_step(build(PARAMS), "model.step")
'''


def test_mutate_catches_every_planted_fault(tmp_path):
    from build123d import export_step
    M = _load("mutate")
    step, dxf, reg, mpy = (str(tmp_path / n) for n in ("m.step", "d.dxf", "r.json", "model.py"))
    export_step(plate(), step)
    drawing().saveas(dxf)
    json.dump(REG, open(reg, "w", encoding="utf-8"))
    open(mpy, "w", encoding="utf-8").write(MODEL_PY)
    r = M.run(step, dxf, reg, model_py=mpy)
    assert r["baseline_verdict"] == "PASS"
    names = {m["name"] for m in r["mutants"]}
    assert {"D2_enlarge_circle", "D5_dim_text"} <= names
    assert any(n.startswith("D1_move_circle_") for n in names) and any(n.startswith("D3_shift_edge_") for n in names)
    escaped = [m["name"] for m in r["mutants"] if m["caught"] is False]
    assert not escaped, escaped
    # strict: a planted fault must be blamed on ONE side only - a model fault must not spawn 2D fix proposals
    wrong = [(m["name"], m["attributed_to"]) for m in r["mutants"]
             if m["caught"] and m["attributed_to"] != [m["expected_attribution"]]]
    assert not wrong, wrong


def test_mutate_refuses_dirty_baseline(tmp_path):
    from build123d import export_step
    M = _load("mutate")
    step, dxf, reg = (str(tmp_path / n) for n in ("m.step", "d.dxf", "r.json"))
    export_step(plate(hole_xy=(70, 42)), step)
    drawing().saveas(dxf)
    json.dump(REG, open(reg, "w", encoding="utf-8"))
    r = M.run(step, dxf, reg)
    assert r["baseline_verdict"] != "PASS" and not r["mutants"]
