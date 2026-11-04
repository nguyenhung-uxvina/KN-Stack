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
    assert G.main(["--step", write_step(tmp_path, block()), "--contract", str(cpath), "--mode", "draft",
                   "--out", str(tmp_path / "ok"), "--quiet"]) == 4
    assert G.main(["--step", str(tmp_path / "missing.step"), "--contract", str(cpath), "--quiet"]) == 3


# ── Blind spots found 2026-11-05 (CADCodeVerify review): each mutant used to PASS ─────────────────────────

RELATIVE_PROBES = [{"why": "hole 30 from +X end", "pt": ["length-30", "width/2", "height/2"], "inside": False},
                   {"why": "solid 30 from -X end", "pt": [30, "width/2", "height/2"], "inside": True}]

IGNORES_PARAMS = textwrap.dedent('''
    from build123d import Box, Cylinder, Location, export_step
    PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0, "hole_x": 70.0}
    def build(p):
        b = Box(100, 40, 20).moved(Location((50, 20, 10)))
        return b - Cylinder(5, 40).moved(Location((70, 20, 10)))
    if __name__ == "__main__":
        export_step(build(PARAMS), "model.step")
''')

HOLE_ABSOLUTE = textwrap.dedent('''
    from build123d import Box, Cylinder, Location, export_step
    PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0}
    def build(p):
        b = Box(p["length"], p["width"], p["height"]).moved(Location((p["length"]/2, p["width"]/2, p["height"]/2)))
        return b - Cylinder(5, 40).moved(Location((70, 20, 10)))
    if __name__ == "__main__":
        export_step(build(PARAMS), "model.step")
''')

HOLE_RELATIVE = textwrap.dedent('''
    from build123d import Box, Cylinder, Location, export_step
    PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0}
    def build(p):
        b = Box(p["length"], p["width"], p["height"]).moved(Location((p["length"]/2, p["width"]/2, p["height"]/2)))
        return b - Cylinder(5, 2*p["height"]).moved(Location((p["length"]-30, p["width"]/2, p["height"]/2)))
    if __name__ == "__main__":
        export_step(build(PARAMS), "model.step")
''')


def _model(tmp_path, src):
    m = tmp_path / "model.py"
    m.write_text(src, encoding="utf-8")
    return str(m)


def test_M1_build_ignoring_params_fails_f4(tmp_path):
    rep = G.run_gates(write_step(tmp_path, block()), CONTRACT, model_py=_model(tmp_path, IGNORES_PARAMS))
    f4 = next(c for c in rep.checks if c["rule_id"] == "F4_param_flex")
    assert f4["status"] == "FAIL" and "KHÔNG tác động" in f4["message"]


def test_M2_absolute_hole_fails_f4_relations(tmp_path):
    c = dict(CONTRACT, param_probes=RELATIVE_PROBES)
    rep = G.run_gates(write_step(tmp_path, block()), c, model_py=_model(tmp_path, HOLE_ABSOLUTE))
    s = statuses(rep)
    assert s["F4_param_flex"] == "PASS"          # rebuilds fine and geometry changes …
    assert s["F4_relations"] == "FAIL"           # … but the hole does not follow the end face


def test_M2_control_relative_hole_passes(tmp_path):
    """Positive control: the same part with the hole written as length-30 must PASS all of F4."""
    c = dict(CONTRACT, param_probes=RELATIVE_PROBES)
    rep = G.run_gates(write_step(tmp_path, block()), c, model_py=_model(tmp_path, HOLE_RELATIVE))
    s = statuses(rep)
    assert s["F4_model_matches_step"] == "PASS" and s["F4_param_flex"] == "PASS" and s["F4_relations"] == "PASS"
    assert not rep.gating_failed


def test_f4_model_must_match_step(tmp_path):
    rep = G.run_gates(write_step(tmp_path, block(hole_x=30.0)), CONTRACT, model_py=_model(tmp_path, HOLE_RELATIVE))
    assert statuses(rep)["F4_model_matches_step"] == "FAIL"


def _cli(tmp_path, contract, extra=(), shape=None, name="r"):
    cpath = tmp_path / "contract.json"
    cpath.write_text(json.dumps(contract), encoding="utf-8")
    step = write_step(tmp_path, shape if shape is not None else block())
    rc = G.main(["--step", step, "--contract", str(cpath), "--out", str(tmp_path / name), "--quiet", *extra])
    return rc, json.load(open(str(tmp_path / (name + ".json")), encoding="utf-8")), G._sha256(str(cpath))


def test_M3_thin_contract_fails_in_release(tmp_path):
    """bbox-only contract + a plain box with NO hole: used to give verdict PASS."""
    thin = {"part_id": "T", "bbox": [100, 40, 20], "bbox_tol": 0.5}
    rc, rep, _ = _cli(tmp_path, thin, shape=block(hole=False))
    assert rc == 2 and rep["verdict"] == "FAIL"
    failed = {c["rule_id"] for c in rep["checks"] if c["status"] == "FAIL"}
    assert {"F2_probes", "F4_param_flex", "contract_integrity"} <= failed


def test_M3_draft_mode_never_reports_plain_pass(tmp_path):
    thin = {"part_id": "T", "bbox": [100, 40, 20], "bbox_tol": 0.5}
    rc, rep, _ = _cli(tmp_path, thin, extra=("--mode", "draft"), shape=block(hole=False))
    assert rc == 4 and rep["verdict"] == "DRAFT-PASS"   # ≠ 0 and ≠ "PASS" ⇒ judge / s2c-validate stay closed


def test_release_full_contract_passes(tmp_path):
    full = dict(CONTRACT, param_probes=RELATIVE_PROBES)
    cpath = tmp_path / "contract.json"
    cpath.write_text(json.dumps(full), encoding="utf-8")
    sha = G._sha256(str(cpath))
    step = write_step(tmp_path, block())
    rc = G.main(["--step", step, "--contract", str(cpath), "--model", _model(tmp_path, HOLE_RELATIVE),
                 "--approved-hash", sha, "--out", str(tmp_path / "r"), "--quiet"])
    rep = json.load(open(str(tmp_path / "r.json"), encoding="utf-8"))
    assert rc == 0 and rep["verdict"] == "PASS", [c for c in rep["checks"] if c["status"] == "FAIL"]


def test_release_waiver_in_signed_contract_keeps_skip(tmp_path):
    c = dict(CONTRACT, waivers={"F4_param_flex": "chi tiết mua sẵn, không có model.py",
                                "F4_relations": "như trên"})
    cpath = tmp_path / "contract.json"
    cpath.write_text(json.dumps(c), encoding="utf-8")
    rc = G.main(["--step", write_step(tmp_path, block()), "--contract", str(cpath),
                 "--approved-hash", G._sha256(str(cpath)), "--out", str(tmp_path / "r"), "--quiet"])
    rep = json.load(open(str(tmp_path / "r.json"), encoding="utf-8"))
    s = {x["rule_id"]: x["status"] for x in rep["checks"]}
    assert rc == 0 and s["F4_param_flex"] == "SKIP" and "MIỄN" in next(
        x["message"] for x in rep["checks"] if x["rule_id"] == "F4_param_flex")


def test_M4_extra_unspecified_hole_fails_f3(tmp_path):
    extra = block() - Cylinder(3, 100).moved(Location((15, 10, 10)))
    rep = G.run_gates(write_step(tmp_path, extra), CONTRACT)
    f3u = next(c for c in rep.checks if c["rule_id"] == "F3_unlisted")
    assert f3u["status"] == "FAIL" and "Ø6" in f3u["observed"]


def test_M4_max_faces_catches_duplicate_hole(tmp_path):
    two = block() - Cylinder(5, 100).moved(Location((40, 20, 10)))
    c = dict(CONTRACT, cyl_features=[{"what": "hole_d10", "dia": 10, "min_faces": 1, "max_faces": 1}])
    rep = G.run_gates(write_step(tmp_path, two), c)
    assert statuses(rep)["F3_hole_d10"] == "FAIL"


def test_eval_expr_rejects_code():
    with pytest.raises(ValueError):
        G.eval_expr("__import__('os').getcwd()", {"length": 1})
    assert G.eval_expr("length-30", {"length": 100}) == 70.0
