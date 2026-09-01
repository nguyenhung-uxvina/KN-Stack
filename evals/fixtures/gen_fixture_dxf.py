#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate a deterministic DXF fixture with KNOWN ground truth for the
accuracy eval of helix-cad-ingest.

Why self-generated: an accuracy eval needs a drawing whose answers are
unarguably correct. We AUTHOR the geometry/text here, so every ground-truth
value in `helix-cad-ingest.accuracy.json` traces to a line in THIS file — no
human measurement, no fabricated numbers, no defense drawing exposed. It is
the honest stand-in that lets the harness itself be verified before the CEO
points it at the real GIÁ TRƯỢT set.

Ground truth authored below (keep in sync with the accuracy spec):
  material   = "NHÔM 5083"           (TEXT)
  code_in_dxf ~ GT.01.02.03          (TEXT, matches PART_ID_RE)
  scale      = "1:2"                 (TEXT)
  units      = mm                    ($INSUNITS = 4)
  product    ~ contains "TRƯỢT"      (TEXT triggers meta.product)
  holes Ø6.6 = 4                     (4 CIRCLE r=3.3)
  holes Ø12  = 2                     (2 CIRCLE r=6.0)
  total holes = 6 ; distinct diameters = 2
  linear dim = 100.0 mm              (1 DIMENSION)
  process_notes = 2                  (2 TEXT lines starting with "-")

Run:  python gen_fixture_dxf.py            -> writes sample_part.dxf here
"""
import os

import ezdxf


def build(path):
    doc = ezdxf.new("R2013", setup=True)
    doc.header["$INSUNITS"] = 4  # mm — drives meta.units
    msp = doc.modelspace()

    # --- title-block TEXT (layer KHUNG_TEN) ---
    tb = [
        ("GT.01.02.03", (0, 0)),      # part code (LOW-confidence per ingest rule)
        ("GIÁ ĐỠ TRƯỢT UUV", (0, 5)),  # name + triggers meta.product ("TRƯỢT")
        ("NHÔM 5083", (0, 10)),        # material (whitelist match)
        ("1:2", (0, 15)),              # scale
    ]
    for txt, pos in tb:
        msp.add_text(txt, dxfattribs={"layer": "KHUNG_TEN"}).set_placement(pos)

    # --- process notes: TEXT lines starting with "-" become process_notes ---
    for i, note in enumerate([
        "- Vát mép 0.5x45 các cạnh sắc",
        "- Làm sạch ba via sau phay",
    ]):
        msp.add_text(note, dxfattribs={"layer": "GHI_CHU"}).set_placement((0, 25 + 5 * i))

    # --- holes: 4x Ø6.6 (r=3.3), 2x Ø12 (r=6.0), layer LO ---
    for x, y in [(10, 10), (70, 10), (10, 50), (70, 50)]:
        msp.add_circle((x, y), 3.3, dxfattribs={"layer": "LO"})
    for x, y in [(40, 20), (40, 40)]:
        msp.add_circle((x, y), 6.0, dxfattribs={"layer": "LO"})

    # --- one linear dimension = 100.0 mm, layer KICH_THUOC ---
    dim = msp.add_linear_dim(base=(0, -10), p1=(0, 0), p2=(100, 0),
                             dxfattribs={"layer": "KICH_THUOC"})
    dim.render()

    doc.saveas(path)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_part.dxf")
    build(out)
    print(f"wrote {out}")
