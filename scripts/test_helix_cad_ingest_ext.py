"""Tests for the helix-cad-ingest extensions: render_dxf.clean_text (TCVN/AIGDT), measure_geometry (G tags),
config loading, source_tag on dimensions. Run: python -m pytest scripts/test_helix_cad_ingest_ext.py -v"""
import importlib.util
import json
import os

import pytest

ezdxf = pytest.importorskip("ezdxf")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ING = os.path.join(ROOT, "skills", "helix", "helix-cad-ingest")


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ING, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.mark.parametrize("raw,want", [
    (r"\A1;{\fAIGDT|b0|i0;\ln}\fTCVN 7284|b0|i1;40", r"\A1;Ø40"),          # GIÁ TRƯỢT P1 Ø40
    (r" \fAIGDT|b0|i0;n\fTCVN 7284|b0|i1;5.5 thru", " Ø5.5 thru"),          # P1 cross hole
    (r"{\fAIGDT|b0|i0;\ln}\fTCVN 7284|b0|i1;<>\fTCVN 7284|b0|i1;h7", "Ø<>h7"),
    (r"\fTCVN 7284|b0|i1;<>±1", "<>±1"),
    ("", ""),
])
def test_clean_text_aigdt_and_tcvn(raw, want):
    assert _load("render_dxf").clean_text(raw) == want


def _two_view_dxf(path):
    doc = ezdxf.new()
    doc.layers.add("Net dam"); doc.layers.add("Duong tam")
    msp = doc.modelspace()
    # view 1: 115 x 50 rectangle at origin; view 2: 50 x 50 square with a Ø11 circle, 200 mm to the right
    for (x0, y0, w, h) in [(0, 0, 115, 50), (200, 0, 50, 50)]:
        pts = [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h), (x0, y0)]
        for a, b in zip(pts, pts[1:]):
            msp.add_line(a, b, dxfattribs={"layer": "Net dam"})
    msp.add_circle((225, 25), 5.5, dxfattribs={"layer": "Net dam"})
    msp.add_line((-20, 25), (400, 25), dxfattribs={"layer": "Duong tam"})  # centre line must NOT merge views
    msp.add_linear_dim(base=(0, -10), p1=(0, 0), p2=(115, 0), dxfattribs={"layer": "Dim"}).render()
    doc.saveas(path)


def test_measure_geometry_separates_views_and_tags_G(tmp_path):
    ing = _load("ingest")
    p = str(tmp_path / "two_view.dxf"); _two_view_dxf(p)
    g = ing.measure_geometry(p)
    sizes = sorted((v["width"], v["height"]) for v in g["views"])
    assert sizes == [(50.0, 50.0), (115.0, 50.0)]
    assert all(v["source_tag"] == "G" for v in g["views"])
    assert any(11.0 in v["circle_dias"] for v in g["views"])


def test_extract_tags_dimensions_D_and_holes_G(tmp_path):
    ing = _load("ingest")
    p = str(tmp_path / "two_view.dxf"); _two_view_dxf(p)
    rec = ing.extract(p, "KHÔNG-NHẠY-CẢM")
    assert rec["dimensions"] and all(d["source_tag"] == "D" for d in rec["dimensions"])
    assert rec["holes"] and all(h["source_tag"] == "G" for h in rec["holes"])


def test_config_overrides_part_id_and_product(tmp_path):
    ing = _load("ingest")
    cfg = tmp_path / "cfg.json"
    cfg.write_text(json.dumps({"part_id_regex": r"WX-\d{3}", "materials": ["NHÔM 6061"],
                               "product_markers": {"VN-TGT-F": ["MẶT BIA"]}}), encoding="utf-8")
    ing.load_config(str(cfg))
    doc = ezdxf.new(); msp = doc.modelspace()
    msp.add_text("WX-123"); msp.add_text("NHÔM 6061"); msp.add_text("MẶT BIA")
    p = str(tmp_path / "c.dxf"); doc.saveas(p)
    m = ing.extract(p, "X")["meta"]
    assert (m["part_id"], m["material"], m["product"]) == ("WX-123", "NHÔM 6061", "VN-TGT-F")


def test_mass_parsed_only_when_label_and_value_share_a_text(tmp_path):
    ing = _load("ingest")
    doc = ezdxf.new(); msp = doc.modelspace(); msp.add_text("Khối lượng: 4.6 kg")
    p = str(tmp_path / "m.dxf"); doc.saveas(p)
    m = ing.extract(p, "X")["meta"]
    assert m["mass_kg"] == 4.6 and m["mass_source_tag"] == "T"
