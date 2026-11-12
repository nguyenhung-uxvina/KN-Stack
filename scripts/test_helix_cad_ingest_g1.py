"""G1 Perception tests for helix-cad-ingest (drawing_tables.py + ingest.extract wiring). Synthetic DXF only.
Each case reproduces a failure measured on a real 42-sheet set (2026-11-05): title block as INSERT with
per-sheet values as loose text, two parts lists side by side, DIMLFAC 0.5, text overrides vs geometry.
Run: python -m pytest scripts/test_helix_cad_ingest_g1.py -v
"""
import importlib.util
import os
import sys

import ezdxf
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ING = os.path.join(ROOT, "skills", "helix", "helix-cad-ingest")
sys.path.insert(0, ING)
DT = importlib.import_module("drawing_tables")
spec = importlib.util.spec_from_file_location("ingest_mod", os.path.join(ING, "ingest.py"))
INGEST = importlib.util.module_from_spec(spec)
spec.loader.exec_module(INGEST)


def title_block_doc(code="99.TS-01.02.03", name="TẤM THỬ NGHIỆM", material="THÉP SS400", scale="1:5",
                    bom_code_row="99.TS-01.02.09"):
    doc = ezdxf.new("R2013")
    blk = doc.blocks.new("khung ten")
    blk.add_line((0, 0), (180, 0))
    blk.add_line((0, 0), (0, 56))
    for i, lb in enumerate(("Tỷ lệ", "Khối lượng", "Thiết kế", "Kiểm tra", "Vẽ")):
        blk.add_mtext(lb, dxfattribs={"insert": (5 + 30 * i, 50), "char_height": 2.5})
    msp = doc.modelspace()
    msp.add_blockref("khung ten", (200, 0))
    msp.add_text(code, dxfattribs={"insert": (330, 40), "height": 3.5})
    msp.add_text(name, dxfattribs={"insert": (260, 30), "height": 5})
    msp.add_text(material, dxfattribs={"insert": (260, 8), "height": 3})
    msp.add_text(scale, dxfattribs={"insert": (360, 25), "height": 3})
    # a parts-list row OUTSIDE the title block carrying another code — must not be taken as the sheet code
    msp.add_text(bom_code_row, dxfattribs={"insert": (40, 120), "height": 3})
    return doc


def bom_doc():
    doc = ezdxf.new("R2013")
    msp = doc.modelspace()
    h = 3.0
    hdr = ["TT", "Ký hiệu", "Tên gọi - Quy cách", "Số lượng", "Vật liệu", "Ghi chú"]
    xs_left = [10, 25, 60, 110, 130, 160]
    xs_right = [190, 205, 240, 290, 310, 340]          # second table immediately to the right
    for xs, y0, rows in ((xs_left, 10, [("1", "99.TS-01.01.01", "Thanh A", "02", "Thép SS400", ""),
                                         ("2", "99.TS-01.01.02", "Thanh B", "04", "Thép SS400", ""),
                                         ("3", "", "Bu lông M8", "16", "Inox 304", "Mua ngoài")]),
                         (xs_right, 40, [("4", "99.TS-01.01.04", "Tấm C", "01", "Thép AH36", "")])):
        for x, t in zip(xs, hdr):
            msp.add_text(t, dxfattribs={"insert": (x, y0), "height": h})
        for i, row in enumerate(rows, 1):
            for x, t in zip(xs, row):
                if t:
                    msp.add_text(t, dxfattribs={"insert": (x, y0 + 6 * i), "height": h})
    return doc


def save(doc, tmp_path, name="t.dxf"):
    p = str(tmp_path / name)
    doc.saveas(p)
    return p


# ── title block ──

def test_title_block_fields_by_position():
    tb = DT.read_title_block(title_block_doc())
    assert tb["found"]
    assert tb["code"]["value"] == "99.TS-01.02.03"
    assert tb["material"]["value"] == "THÉP SS400"
    assert tb["scale"]["value"] == "1:5"
    assert tb["name"]["value"] == "TẤM THỬ NGHIỆM"
    assert tb["code"]["locator"]["handle"]


def test_sheet_code_not_taken_from_parts_list_row(tmp_path):
    rec = INGEST.extract(save(title_block_doc(), tmp_path), "TEST")
    assert rec["meta"]["code_in_dxf"] == "99.TS-01.02.03" and rec["meta"]["code_source"] == "title_block"


def test_no_title_block_falls_back(tmp_path):
    doc = ezdxf.new("R2013")
    doc.modelspace().add_text("chỉ có chữ", dxfattribs={"insert": (0, 0), "height": 3})
    rec = INGEST.extract(save(doc, tmp_path), "TEST")
    assert rec["meta"]["title_block"]["found"] is False


# ── parts list ──

def test_two_side_by_side_parts_lists_kept_apart():
    tables = DT.read_bom_tables(bom_doc())
    assert len(tables) == 2
    left = {r["cells"].get("tt"): r["cells"] for r in tables[0]["rows"]} if tables[0]["header_y"] == 10 else \
        {r["cells"].get("tt"): r["cells"] for r in tables[1]["rows"]}
    assert set(left) == {"1", "2", "3"}
    assert left["2"]["code"] == "99.TS-01.01.02" and left["2"]["qty"] == "04" and left["3"]["note"] == "Mua ngoài"


def test_bom_rows_reach_extract_with_locators(tmp_path):
    rec = INGEST.extract(save(bom_doc(), tmp_path), "TEST")
    assert len(rec["bom"]) == 4
    r = next(x for x in rec["bom"] if x["name"] == "Tấm C")
    assert r["code"] == "99.TS-01.01.04" and r["material"] == "Thép AH36" and r["locator"]["name"]["handle"]


def test_tcvn_parts_list_rows_below_header_and_part_name_starting_with_ma():
    """TCVN form: Khổ giấy · Miền · Vị trí · Ký hiệu · Tên gọi · S.lg · Chú thích, rows run DOWN, the first row
    sits 4 text-heights below the header, and a part called "Mã …" must not be read as a header (measured)."""
    doc = ezdxf.new("R2013")
    msp = doc.modelspace()
    h = 30.0
    for x, t in zip((230, 290, 360, 750, 1415, 1790, 1940),
                    ("Khổ giấy", "Miền", "Vị trí", "Ký hiệu", "Tên gọi", "S.lg", "Chú thích")):
        msp.add_text(t, dxfattribs={"insert": (x, 2843), "height": h})
    msp.add_text("TÀI LIỆU", dxfattribs={"insert": (1415, 2723), "height": h})
    for i, (code, name, q) in enumerate((("99.TS-01.08.00", "Thanh chống", "02"), ("99.TS-01.09.00", "Mã cạnh phao", "08"),
                                         ("99.TS-01.11.00", "Chốt tháo", "02"))):
        y = 2643 - 80 * i
        for x, t in ((230, "A4"), (750, code), (1100, name), (1780, q)):
            msp.add_text(t, dxfattribs={"insert": (x, y), "height": h})
    rows = DT.read_bom_tables(doc)[0]["rows"]
    assert [r["cells"].get("name") for r in rows] == ["Thanh chống", "Mã cạnh phao", "Chốt tháo"]
    assert rows[1]["cells"]["qty"] == "08"


# ── dimensions ──

def dim_doc(override="", lf=1.0, length=100.0):
    doc = ezdxf.new("R2013", setup=True)
    msp = doc.modelspace()
    # explicit dimstyle + DIMLFAC: ezdxf's default "EZDXF" style carries DIMLFAC = 100
    d = msp.add_linear_dim(base=(0, 20), p1=(0, 0), p2=(length, 0), text=override, dimstyle="Standard",
                           override={"dimlfac": lf})
    d.render()
    return doc


@pytest.mark.parametrize("override,lf,length,expect_value,expect_conflict", [
    ("", 0.5, 300.0, 150.0, None),                      # DIMLFAC: drawn ×2, shows 150
    ("%%C14", 1.0, 12.52, 14.0, "TEXT-OVERRIDE"),        # says Ø14, drawn 12.52
    ("600±20", 1.0, 607.4, 600.0, None),                 # inside its own explicit tolerance
    ("76", 1.0, 190.0, 76.0, None),                      # detail drawn ×2.5
    ("1300", 1.0, 850.0, 1300.0, "BREAK-VIEW"),          # broken view
])
def test_dimension_classification(tmp_path, override, lf, length, expect_value, expect_conflict):
    rec = INGEST.extract(save(dim_doc(override, lf, length), tmp_path), "TEST")
    d = rec["dimensions"][0]
    assert abs(d["value"] - expect_value) < 0.01, d
    types = [c["type"] for c in rec["conflicts"]]
    if expect_conflict:
        assert types == [expect_conflict]
        assert rec["conflicts"][0]["locator"]["handle"]
    else:
        assert types == []


def test_override_value_parsing():
    assert DT.override_value("4 lỗ %%C12") == 12.0
    assert DT.override_value("4-%%C14") == 14.0
    assert DT.override_value("R41") == 41.0
    assert DT.override_value("600±20") == 600.0
    assert DT.override_value("22,5") == 22.5


def test_classify_override_unit():
    assert DT.classify_override(36, 88.939) == "SCALED_VIEW"     # ×2.5 with rounded text
    assert DT.classify_override(41, 162.25) == "SCALED_VIEW"     # ×4 with rounded text
    assert DT.classify_override(14, 12.52) == "TEXT_OVERRIDE"
    assert DT.classify_override(76, 190.0) == "SCALED_VIEW"
    assert DT.classify_override(600, 607.4, 20) == "WITHIN_TOL"
    assert DT.classify_override(23, 56.3) == "TEXT_OVERRIDE"   # 2.448× is not a drafting scale
    assert DT.classify_override(150, 150.0) == "AGREE"


def test_unicode_escaped_title_block_and_values():
    r"""DXF <= R2004 writes 'Tỷ lệ' as 'T\U+1EF7 l\U+1EC7'. Measured on a second set: 0/47 codes until decoded."""
    def esc(s):
        return "".join(c if ord(c) < 128 else r"\U+%04X" % ord(c) for c in s)
    doc = ezdxf.new("R2013")
    blk = doc.blocks.new("khung ten")
    blk.add_line((0, 0), (180, 0))      # frame lines give the block its extents
    blk.add_line((0, 0), (0, 56))
    for i, lb in enumerate(("Tỷ lệ", "Khối lượng", "Thiết kế", "Kiểm tra")):
        blk.add_mtext(esc(lb), dxfattribs={"insert": (5 + 30 * i, 50), "char_height": 2.5})
    msp = doc.modelspace()
    msp.add_blockref("khung ten", (200, 0))
    msp.add_text("99.TS-01.05.01", dxfattribs={"insert": (330, 40), "height": 3.5})
    msp.add_text(esc("THANH KHUNG ĐỨNG 1"), dxfattribs={"insert": (260, 30), "height": 5})
    msp.add_text(esc("THÉP KẾT CẤU"), dxfattribs={"insert": (260, 8), "height": 3})
    tb = DT.read_title_block(doc)
    assert tb["found"] and tb["name"]["value"] == "THANH KHUNG ĐỨNG 1" and tb["material"]["value"] == "THÉP KẾT CẤU"
    assert DT.decode_uescapes(r"THANH KHUNG \U+0110\U+1EE8NG") == "THANH KHUNG ĐỨNG"
