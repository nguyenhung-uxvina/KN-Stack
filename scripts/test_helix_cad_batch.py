"""Tests for skills/helix/helix-cad-batch (batch_sweep.py, dxf_layers.py).
Run: python -m pytest scripts/test_helix_cad_batch.py -v"""
import csv
import importlib.util
import os
import textwrap

import pytest

pytest.importorskip("build123d")
ezdxf = pytest.importorskip("ezdxf")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.path.join(ROOT, "skills", "helix", "helix-cad-batch")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(BATCH, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


MODEL = textwrap.dedent('''
    from build123d import Box, Cylinder, Location, export_step
    PARAMS = {"length": 100.0, "width": 40.0, "height": 20.0, "hole_d": 10.0}
    def build(p):
        b = Box(p["length"], p["width"], p["height"]).moved(Location((p["length"]/2, p["width"]/2, p["height"]/2)))
        return b - Cylinder(p["hole_d"]/2, 100).moved(Location((p["length"]*0.7, p["width"]/2, 0)))
    if __name__ == "__main__":
        export_step(build(PARAMS), "model.step")
''')


def _csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); [w.writerow(r) for r in rows]


def test_sweep_builds_and_gates_each_variant(tmp_path):
    B = _load("batch_sweep")
    m = tmp_path / "model.py"; m.write_text(MODEL, encoding="utf-8")
    v = tmp_path / "v.csv"
    _csv(v, [["variant_id", "length", "bbox_x", "bbox_y", "bbox_z"],
             ["A", "100", "100", "40", "20"],
             ["B", "150", "150", "40", "20"],
             ["C_wrong_expect", "120", "999", "40", "20"]])
    res = {r["variant_id"]: r for r in B.sweep(str(m), str(v), str(tmp_path / "out"), stl=True)}
    assert res["A"]["verdict"] == "PASS" and res["B"]["verdict"] == "PASS"
    assert res["B"]["bbox"][0] == pytest.approx(150, abs=0.01)
    assert res["C_wrong_expect"]["verdict"] == "FAIL"
    assert os.path.exists(tmp_path / "out" / "B" / "model.stl")
    assert os.path.exists(tmp_path / "out" / "summary.md")


def test_sweep_rejects_unknown_column(tmp_path):
    B = _load("batch_sweep")
    m = tmp_path / "model.py"; m.write_text(MODEL, encoding="utf-8")
    v = tmp_path / "v.csv"; _csv(v, [["variant_id", "lenght"], ["A", "100"]])
    with pytest.raises(ValueError, match="not in PARAMS"):
        B.sweep(str(m), str(v), str(tmp_path / "out"))


def test_sweep_rejects_non_parametric_model(tmp_path):
    B = _load("batch_sweep")
    m = tmp_path / "model.py"; m.write_text("from build123d import Box\n", encoding="utf-8")
    v = tmp_path / "v.csv"; _csv(v, [["variant_id"], ["A"]])
    with pytest.raises(ValueError, match="PARAMS"):
        B.sweep(str(m), str(v), str(tmp_path / "out"))


def test_layer_rename_moves_entities_and_never_overwrites(tmp_path):
    L = _load("dxf_layers")
    doc = ezdxf.new(); doc.layers.add("Net dam"); doc.layers.add("Net khuat")
    msp = doc.modelspace(); msp.add_line((0, 0), (10, 0), dxfattribs={"layer": "Net dam"})
    src = tmp_path / "a.dxf"; doc.saveas(src)
    mp = tmp_path / "map.csv"; _csv(mp, [["old", "new"], ["Net dam", "0-VISIBLE"], ["Not there", "X"]])
    assert L.main(["--in", str(src), "--map", str(mp), "--out", str(src)]) == 3  # refuses to overwrite
    out = tmp_path / "b.dxf"
    assert L.main(["--in", str(src), "--map", str(mp), "--out", str(out)]) == 0
    d2 = ezdxf.readfile(out)
    assert "0-VISIBLE" in {l.dxf.name for l in d2.layers}
    assert all(e.dxf.layer == "0-VISIBLE" for e in d2.modelspace().query("LINE"))


def test_layer_rename_clash_exit_2(tmp_path):
    L = _load("dxf_layers")
    doc = ezdxf.new(); doc.layers.add("A"); doc.layers.add("B")
    src = tmp_path / "a.dxf"; doc.saveas(src)
    mp = tmp_path / "map.csv"; _csv(mp, [["A", "B"]])
    assert L.main(["--in", str(src), "--map", str(mp), "--out", str(tmp_path / "o.dxf")]) == 2
