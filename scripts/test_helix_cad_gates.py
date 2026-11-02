"""Mutation tests for skills/helix/helix-cad-gates (geom_gates.py + cad_runner.py).

Every failure mode measured in the GIÁ TRƯỢT test (2026-11-02) has a broken fixture here; each gate must
FAIL on exactly its mutant and PASS on the good part. Run: python -m pytest scripts/test_helix_cad_gates.py -v
"""
import importlib.util
import json
import os
import textwrap

import pytest

pytest.importorskip("build123d")
from build123d import Box, Cylinder, Location, Shell, export_step  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATES_DIR = os.path.join(ROOT, "skills", "helix", "helix-cad-gates")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(GATES_DIR, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


G = _load("geom_gates")

CONTRACT = {
    "part_id": "TEST-BLOCK", "projection_method": "first-angle", "bbox": [100, 40, 20], "bbox_tol": 0.5,
    "material": "AL5083", "title_kg": 0.2,
    "cyl_features": [{"what": "hole_d10", "dia": 10, "min_faces": 1}],
    "probes": [{"why": "hole open at x=70", "pt": [70, 20, 10], "inside": False},
               {"why": "solid at x=30", "pt": [30, 20, 10], "inside": True}],
}

GOOD_MODEL = textwrap.dedent('''
    from build123d import Box, Cylinder, Location, export_step
    PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0, "hole_d": 10.0, "hole_x": 70.0}
    def build(p):
        b = Box(p["length"], p["width"], p["height"]).moved(Location((p["length"]/2, p["width"]/2, p["height"]/2)))
        h = Cylinder(p["hole_d"]/2, p["height"]*2).moved(Location((p["hole_x"], p["width"]/2, p["height"]/2)))
        return b - h
    if __name__ == "__main__":
        export_step(build(PARAMS), "model.step")
''')


def block(hole_x=70.0, hole=True, size=(100, 40, 20)):
    L, W, H = size
    b = Box(L, W, H).moved(Location((L / 2, W / 2, H / 2)))
    if hole:
        b = b - Cylinder(5, 100).moved(Location((hole_x, W / 2, H / 2)))
    return b


def write_step(tmp_path, shape, name="model.step"):
    p = str(tmp_path / name)
    export_step(shape, p)
    return p


def statuses(rep):
    return {c["rule_id"]: c["status"] for c in rep.checks}


def test_good_part_passes_f1_f2_f3(tmp_path):
    rep = G.run_gates(write_step(tmp_path, block()), CONTRACT)
    s = statuses(rep)
    assert s["F1_closed_brep"] == "PASS" and s["F2_bbox_per_axis"] == "PASS"
    assert s["F2_probes"] == "PASS" and s["F3_hole_d10"] == "PASS"
    assert not rep.gating_failed


def test_open_shell_fails_f1(tmp_path):
    faces = block().faces()
    rep = G.run_gates(write_step(tmp_path, Shell(faces[:-1])), CONTRACT)
    assert statuses(rep)["F1_closed_brep"] == "FAIL"


def test_axis_swap_flagged(tmp_path):
    rep = G.run_gates(write_step(tmp_path, block(hole=False, size=(20, 40, 100))), CONTRACT)
    f2 = next(c for c in rep.checks if c["rule_id"] == "F2_bbox_per_axis")
    assert f2["status"] == "FAIL" and "ĐẢO TRỤC" in f2["message"]


def test_right_diameter_wrong_place_caught_only_by_probe(tmp_path):
    """The P4 case: F3 (diameter count) passes, the position probe must fail."""
    rep = G.run_gates(write_step(tmp_path, block(hole_x=30.0)), CONTRACT)
    s = statuses(rep)
    assert s["F3_hole_d10"] == "PASS"
    assert s["F2_probes"] == "FAIL"


def test_missing_hole_fails_f3(tmp_path):
    rep = G.run_gates(write_step(tmp_path, block(hole=False)), CONTRACT)
    assert statuses(rep)["F3_hole_d10"] == "FAIL"


def test_no_probes_is_skip_not_silent_pass(tmp_path):
    c = dict(CONTRACT, probes=[])
    rep = G.run_gates(write_step(tmp_path, block()), c)
    assert statuses(rep)["F2_probes"] == "SKIP"


def test_mass_is_info_never_gating(tmp_path):
    c = dict(CONTRACT, title_kg=99.0)  # absurd title mass must not close the gate
    rep = G.run_gates(write_step(tmp_path, block()), c)
    assert statuses(rep)["MASS_vs_title"] == "INFO"
    assert not rep.gating_failed


def test_f4_param_model_passes(tmp_path):
    m = tmp_path / "model.py"
    m.write_text(GOOD_MODEL, encoding="utf-8")
    rep = G.run_gates(write_step(tmp_path, block()), CONTRACT, model_py=str(m))
    assert statuses(rep)["F4_param_flex"] == "PASS"


def test_f4_hardcoded_model_fails(tmp_path):
    m = tmp_path / "model.py"
    m.write_text("from build123d import Box, export_step\nexport_step(Box(100,40,20), 'model.step')\n",
                 encoding="utf-8")
    rep = G.run_gates(write_step(tmp_path, block()), CONTRACT, model_py=str(m))
    assert statuses(rep)["F4_param_flex"] == "FAIL"


def test_f4_fragile_fillet_fails(tmp_path):
    """Fillet radius hardcoded near half the height: -10% height breaks the rebuild."""
    m = tmp_path / "model.py"
    m.write_text(textwrap.dedent('''
        from build123d import Box, fillet, Axis, export_step
        PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0}
        def build(p):
            b = Box(p["length"], p["width"], p["height"])
            return fillet(b.edges().filter_by(Axis.X), radius=9.9)
        if __name__ == "__main__":
            export_step(build(PARAMS), "model.step")
    '''), encoding="utf-8")
    rep = G.run_gates(write_step(tmp_path, block()), CONTRACT, model_py=str(m))
    assert statuses(rep)["F4_param_flex"] == "FAIL"


def test_contract_hash_mismatch_closes_gate(tmp_path):
    step = write_step(tmp_path, block())
    cpath = tmp_path / "contract.json"
    cpath.write_text(json.dumps(CONTRACT), encoding="utf-8")
    rc = G.main(["--step", step, "--contract", str(cpath), "--out", str(tmp_path / "r"),
                 "--approved-hash", "0" * 64, "--quiet"])
    assert rc == 2
    rep = json.load(open(str(tmp_path / "r.json"), encoding="utf-8"))
    assert any(c["rule_id"] == "contract_integrity" and c["status"] == "FAIL" for c in rep["checks"])


def test_cli_exit_codes(tmp_path):
    cpath = tmp_path / "contract.json"
    cpath.write_text(json.dumps(CONTRACT), encoding="utf-8")
    assert G.main(["--step", write_step(tmp_path, block()), "--contract", str(cpath),
                   "--out", str(tmp_path / "ok"), "--quiet"]) == 0
    assert G.main(["--step", str(tmp_path / "missing.step"), "--contract", str(cpath), "--quiet"]) == 3
