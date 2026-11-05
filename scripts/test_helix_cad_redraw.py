"""Tests for skills/helix/helix-cad-redraw — every rule in references/redraw-rules.md that has a script gets a
synthetic fixture here (made-up parts, no project data). Run: python -m pytest scripts/test_helix_cad_redraw.py -v

Paper scale 1 (no title-frame INSERT) ⇒ model units = paper mm.
"""
import importlib.util
import json
import os
import sys

import pytest

ezdxf = pytest.importorskip("ezdxf")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(ROOT, "skills", "helix", "helix-cad-redraw")
sys.path.insert(0, RD)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(RD, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


DS = _load("dim_spacing")
TO = _load("text_overlap")
NS = _load("notes_strokes")
WD = _load("written_vs_drawn")
LD = _load("label_diff")
SM = _load("sheet_merge")
RH = _load("redraw_helpers")


def plate(msp, w=100, h=50):
    msp.add_lwpolyline([(0, 0), (w, 0), (w, h), (0, h)], close=True)


def hdim(msp, x0, x1, y_pts, y_line):
    msp.add_linear_dim(base=(x0, y_line), p1=(x0, y_pts), p2=(x1, y_pts), angle=0).render()


def save(doc, tmp_path, name):
    p = str(tmp_path / name)
    doc.saveas(p)
    return p


def dim_lines(path):
    m = ezdxf.readfile(path).modelspace()
    return sorted((round(e.get_measurement(), 1), round(e.dxf.defpoint.y, 2)) for e in m.query("DIMENSION"))


# ---------------- dim_spacing ----------------
def test_check_reports_close_dim(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m); hdim(m, 0, 100, 50, 52)
    r = DS.check(save(d, tmp_path, "a.dxf"))
    assert len(r) == 1 and r[0]["gap_mm"] == 2.0


def test_fix_moves_out_to_target_and_outward(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m); hdim(m, 0, 100, 50, 52)
    p = save(d, tmp_path, "a.dxf")
    DS.fix(p)
    (v, y), = dim_lines(p)
    assert y == pytest.approx(57.0, abs=0.01)            # 7 mm ABOVE the top edge, not into the plate
    assert DS.check(p) == []


def test_fix_keeps_original_tier_distance(tmp_path):
    """F-TIER: the original put this value 14 mm out — reuse it instead of collapsing to 7."""
    o = ezdxf.new("R2018"); mo = o.modelspace(); plate(mo); hdim(mo, 0, 100, 50, 64)
    n = ezdxf.new("R2018"); mn = n.modelspace(); plate(mn); hdim(mn, 0, 100, 50, 52)
    po, pn = save(o, tmp_path, "o.dxf"), save(n, tmp_path, "n.dxf")
    DS.fix(pn, orig=po)
    assert dim_lines(pn)[0][1] == pytest.approx(64.0, abs=0.01)


def test_fix_keeps_deliberate_across_dim(tmp_path):
    """F-ORIG: original also drew this value across the part (< 1 mm) — keep."""
    o = ezdxf.new("R2018"); mo = o.modelspace(); plate(mo); hdim(mo, 0, 100, 25, 25.3)
    n = ezdxf.new("R2018"); mn = n.modelspace(); plate(mn); hdim(mn, 0, 100, 25, 25.3)
    po, pn = save(o, tmp_path, "o.dxf"), save(n, tmp_path, "n.dxf")
    DS.fix(pn, orig=po)
    assert dim_lines(pn)[0][1] == pytest.approx(25.3, abs=0.01)


def test_stack_separates_two_tiers_on_same_line(tmp_path):
    """F-STACK: two parallel overlapping dims both close ⇒ both go to 7 mm ⇒ longer pushed one tier out."""
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
    hdim(m, 0, 100, 50, 52); hdim(m, 20, 80, 50, 53)
    p = save(d, tmp_path, "a.dxf"); DS.fix(p)
    lines = dict(dim_lines(p))
    assert lines[100.0] - lines[60.0] >= 4.0 - 1e-6         # longer is outer, readable gap
    assert DS.check(p) == []


def test_carry_keeps_original_tier_spacing(tmp_path):
    """F-CARRY: inner tier moved +5 ⇒ outer tier 4.4 mm above moves +5 too (no cascade, spacing kept)."""
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
    hdim(m, 0, 100, 50, 52); hdim(m, 0, 90, 50, 56.4)        # tiers 4.4 mm apart, as originals often draw
    p = save(d, tmp_path, "a.dxf"); r = DS.fix(p)
    lines = dict(dim_lines(p))
    assert r["carried"] == 1
    assert lines[100.0] == pytest.approx(57.0, abs=0.01)
    assert lines[90.0] == pytest.approx(61.4, abs=0.01)


def test_carry_guard_never_drags_dim_onto_its_own_points(tmp_path):
    """carry guard: an 'outer' dim (already visited, 9 mm BELOW its own points at y=75) must not be carried up
    to 4 mm from them. It is created FIRST so the main loop has passed it — exactly how the real case slipped."""
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
    m.add_lwpolyline([(30, 75), (70, 75), (70, 80), (30, 80)], close=True)
    m.add_linear_dim(base=(30, 66), p1=(30, 75), p2=(70, 75), angle=0).render()      # 40, 9 mm under its points
    hdim(m, 0, 100, 50, 52)                                                          # inner tier, moves +5
    p = save(d, tmp_path, "a.dxf"); DS.fix(p)
    assert DS.check(p) == []
    assert dict(dim_lines(p))[40.0] == pytest.approx(66.0, abs=0.01)


def test_side_flips_away_from_strokes(tmp_path):
    """F-SIDE: strokes above pull the centroid up, so 'away from centroid' = DOWN into the part; the band
    below holds 3 strokes, the band above none ⇒ go up."""
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
    for x in (40, 45, 50, 55, 60):
        m.add_line((x, 64), (x + 2, 66))                                            # clutter above (outside band)
    for x in (20, 50, 80):
        m.add_line((x, 45), (x + 4, 45))                                            # inner strokes below the edge
    hdim(m, 0, 100, 50, 48)                                                          # 2 mm under the top edge
    p = save(d, tmp_path, "a.dxf"); DS.fix(p)
    assert dict(dim_lines(p))[100.0] == pytest.approx(57.0, abs=0.01)


def test_original_side_beats_heuristics(tmp_path):
    """F-ORIGSIDE: same fixture where the heuristic goes UP; the original put this value 9 mm BELOW ⇒ follow it."""
    def sheet(y_line):
        d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
        for x in (20, 50, 80):
            m.add_line((x, 45), (x + 4, 45))
        hdim(m, 0, 100, 50, y_line)
        return d
    po = save(sheet(41), tmp_path, "o.dxf"); pn = save(sheet(48), tmp_path, "n.dxf")
    DS.fix(pn, orig=po)
    assert dict(dim_lines(pn))[100.0] == pytest.approx(41.0, abs=0.01)


def test_counterpart_by_place(tmp_path):
    """MATCH: the original has a 100 placed 20 mm out on ANOTHER plate far away; this plate's 100 must not
    inherit that distance (value alone matched the wrong dim)."""
    o = ezdxf.new("R2018"); mo = o.modelspace(); plate(mo)
    mo.add_lwpolyline([(0, 52), (100, 52), (100, 60), (0, 60)], close=True)
    hdim(mo, 0, 100, 60, 80)                                  # the OTHER 100: 8 mm up, 20 mm out — not this dim
    po = save(o, tmp_path, "o.dxf")
    n = ezdxf.new("R2018"); m = n.modelspace(); plate(m); hdim(m, 0, 100, 50, 52)
    pn = save(n, tmp_path, "n.dxf")
    DS.fix(pn, orig=po)
    assert dict(dim_lines(pn))[100.0] == pytest.approx(57.0, abs=0.01)


def test_cli_check_exit_codes(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m); hdim(m, 0, 100, 50, 52)
    p = save(d, tmp_path, "a.dxf")
    assert DS.main(["check", p]) == 2
    assert DS.main(["fix", p]) == 0
    assert DS.main(["check", p]) == 0
    assert DS.main(["nope"]) == 3


# ---------------- text_overlap ----------------
def test_overlap_and_duplicate_on_skipped_layer(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_text("ABCDEF", height=5, dxfattribs={"insert": (0, 0)}); m.add_text("XYZ", height=5, dxfattribs={"insert": (2, 1)})
    for v in ("≈ 0,32", "≈ 0,33"):                           # stacked title-block cell on a skipped layer
        m.add_mtext(v, dxfattribs={"insert": (200, 10), "layer": "TITLE", "char_height": 3})
    p = save(d, tmp_path, "a.dxf")
    r = TO.check(p, skip_layers=("TITLE",))
    assert r["overlaps"] and r["duplicates"]
    assert TO.main([p, "--skip-layer", "TITLE"]) == 2


def test_clean_sheet_passes(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_text("A1", height=5, dxfattribs={"insert": (0, 0)}); m.add_text("B2", height=5, dxfattribs={"insert": (100, 0)})
    assert TO.main([save(d, tmp_path, "a.dxf")]) == 0


# ---------------- notes_strokes ----------------
def _notes_sheet(with_strokes):
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_mtext("Yêu cầu kỹ thuật:\\P- Mối hàn   5 đảm bảo ngấu.", dxfattribs={"insert": (0, 100), "char_height": 3.5, "width": 120})
    if with_strokes:
        m.add_line((14, 94), (17, 97)); m.add_line((17, 97), (14, 97))
    plate(m)
    return d


def test_notes_strokes_missing_then_written(tmp_path):
    (tmp_path / "o").mkdir(); (tmp_path / "r").mkdir()
    _notes_sheet(True).saveas(str(tmp_path / "o" / "05_PART.dxf")); _notes_sheet(False).saveas(str(tmp_path / "r" / "05_PART.dxf"))
    rows, missing = NS.run(str(tmp_path / "o"), str(tmp_path / "r"))
    assert missing == [5]
    NS.run(str(tmp_path / "o"), str(tmp_path / "r"), write=True)
    assert NS.run(str(tmp_path / "o"), str(tmp_path / "r"))[1] == []
    assert NS.run(str(tmp_path / "o"), str(tmp_path / "r"), skip=(5,))[0] == []


# ---------------- written_vs_drawn ----------------
def test_written_vs_drawn_flags(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace()
    st = d.dimstyles.duplicate_entry("Standard", "D0"); st.dxf.dimdec = 0
    m.add_linear_dim(base=(0, 10), p1=(0, 0), p2=(540, 0), text="500").render()               # MISMATCH
    m.add_linear_dim(base=(0, -10), p1=(0, -20), p2=(22.5, -20), dimstyle="D0").render()        # ROUNDED
    for i, real in enumerate((150, 25, 75)):                                                    # factor 0.4 detail
        m.add_linear_dim(base=(0, 40 + 10 * i), p1=(0, 30 + 10 * i), p2=(real, 30 + 10 * i), text=f"{real * 0.4:g}").render()
    r = WD.scan(save(d, tmp_path, "a.dxf"))
    flags = [f for row in r["rows"] for f in row["flags"]]
    assert "MISMATCH" in flags and "ROUNDED" in flags and "FACTOR" in flags
    assert "0.4" in r["implied_factors"]


# ---------------- label_diff ----------------
def test_label_diff_lost_label(tmp_path, capsys):
    (tmp_path / "o").mkdir(); (tmp_path / "r").mkdir()
    a = ezdxf.new("R2018"); a.modelspace().add_text("Thép tấm s5", dxfattribs={"insert": (0, 0)}); a.saveas(str(tmp_path / "o" / "07_X.dxf"))
    b = ezdxf.new("R2018"); b.saveas(str(tmp_path / "r" / "07_X.dxf"))
    assert LD.main([str(tmp_path / "o"), str(tmp_path / "r"), "7"]) == 2
    assert "Thép tấm s5" in capsys.readouterr().out


# ---------------- redraw_helpers ----------------
def _dim_text_insert(dim):
    for v in dim.get_geometry_block():
        if v.dxftype() == "MTEXT":
            return v.dxf.insert, v.dxf.get("rotation", 0)
    return None, None


def test_place_dim_text_survives_render(tmp_path):
    d = ezdxf.new("R2018"); m = d.modelspace(); plate(m)
    m.add_linear_dim(base=(120, 0), p1=(100, 0), p2=(100, 50), angle=90).render()
    e = list(m.query("DIMENSION"))[0]
    RH.place_dim_text(e, (115, 10))
    p = save(d, tmp_path, "a.dxf")
    e2 = list(ezdxf.readfile(p).modelspace().query("DIMENSION"))[0]
    ins, _ = _dim_text_insert(e2)
    assert abs(ins.y - 10) < 1.0                          # stays low, not back at the middle (25)


def test_fix_180_reads_upright():
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_linear_dim(base=(0, 10), p1=(30, 0), p2=(0, 0), angle=180).render()
    e = list(m.query("DIMENSION"))[0]
    assert RH.fix_180(e)
    e.override().render()
    _, rot = _dim_text_insert(e)
    assert -90 < (rot or 0) <= 90


def test_stretch_moves_lines_hatch_and_dims_together():
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_line((0, 0), (100, 0))
    h = m.add_hatch(); h.paths.add_polyline_path([(0, 0), (100, 0), (100, 5), (0, 5)], is_closed=True)
    m.add_linear_dim(base=(0, 20), p1=(0, 0), p2=(100, 0)).render()
    n = RH.stretch(m, (90, -1, 110, 6), lambda x, y: (x - 10, y) if abs(x - 100) < 0.5 else None)
    assert n >= 3
    e = list(m.query("DIMENSION"))[0]
    assert e.get_measurement() == pytest.approx(90.0)
    assert RH.rerender_dims(m) == 1


def test_scale_region_true_scale_and_text_spacing():
    d = ezdxf.new("R2018"); m = d.modelspace()
    m.add_line((0, 0), (0, 60))
    m.add_linear_dim(base=(10, 0), p1=(0, 0), p2=(0, 60), angle=90).render()       # drawn 60, real value 60*1.6*0.25 = 24
    t1 = m.add_text("Lớp vỏ", height=2.5, dxfattribs={"insert": (20, 30)})
    t2 = m.add_text("(3mm)", height=2.5, dxfattribs={"insert": (20, 26)})
    got = RH.scale_region(m, (-5, -5, 40, 70), 1.6, (0, 60), dim_factor=0.25)
    assert got == [pytest.approx(24.0)]
    assert t1.dxf.height == 2.5 and t2.dxf.height == 2.5
    assert (t1.dxf.insert.y - t2.dxf.insert.y) == pytest.approx(4.0)         # second line follows the first


# ---------------- sheet_merge ----------------
def test_sheet_merge_places_and_audits(tmp_path):
    sd = tmp_path / "s"; sd.mkdir()
    for no in (1, 2):
        d = ezdxf.new("R2018"); d.modelspace().add_line((0, 0), (10, 0)); d.saveas(str(sd / f"{no:02d}_S.dxf"))
    mf = {"to": [{"to": 1, "tep": "01_S.dxf", "do_dich": [0, 0]}, {"to": 2, "tep": "02_S.dxf", "do_dich": [-500, 0]}]}
    mp = tmp_path / "MANIFEST.json"; mp.write_text(json.dumps(mf), encoding="utf-8")
    out = str(tmp_path / "set.dxf")
    assert SM.main([str(mp), str(sd), out, "--update-manifest", str(mp)]) == 0
    xs = sorted(round(e.dxf.start.x) for e in ezdxf.readfile(out).modelspace().query("LINE"))
    assert xs == [0, 500]
    assert "ban_tong_sha256" in json.loads(mp.read_text(encoding="utf-8"))


def _title(doc, msp):
    """Title block INSERT named like the real ones; paper scale 1. Placed inside the border corner."""
    blk = doc.blocks.new("khung ten"); blk.add_lwpolyline([(0, 0), (40, 0), (40, 10), (0, 10)], close=True)
    msp.add_blockref("khung ten", (100, -45))


def test_frame_guard_and_outside_report(tmp_path):
    """F-FRAME: plate top edge 3 mm under the sheet border — going up would leave the border ⇒ go down;
    `check` reports any dim already outside the border."""
    d = ezdxf.new("R2018"); m = d.modelspace(); _title(d, m)
    m.add_lwpolyline([(-50, -50), (150, -50), (150, 53), (-50, 53)], close=True)   # sheet border
    m.add_lwpolyline([(0, 0), (100, 0), (100, 50), (0, 50)], close=True)
    hdim(m, 0, 100, 50, 52)
    p = save(d, tmp_path, "a.dxf"); DS.fix(p)
    assert dict(dim_lines(p))[100.0] < 53
    d2 = ezdxf.new("R2018"); m2 = d2.modelspace(); _title(d2, m2)
    m2.add_lwpolyline([(-50, -50), (150, -50), (150, 60), (-50, 60)], close=True)
    hdim(m2, 0, 100, 50, 75)
    p2 = save(d2, tmp_path, "b.dxf")
    assert DS.outside_frame(p2) and DS.main(["check", p2]) == 2


def test_pull_inside_border(tmp_path):
    """F-FRAME-IN: a script put the dim 14 mm out, its text past the border ⇒ pulled inside, still >= 5 mm."""
    d = ezdxf.new("R2018"); m = d.modelspace(); _title(d, m)
    m.add_lwpolyline([(-50, -50), (150, -50), (150, 64.2), (-50, 64.2)], close=True)   # line inside, text out
    plate(m); hdim(m, 0, 100, 50, 64)
    p = save(d, tmp_path, "a.dxf")
    assert DS.outside_frame(p)
    r = DS.fix(p)
    assert r["pulled_inside"] == 1 and DS.outside_frame(p) == [] and DS.check(p) == []
