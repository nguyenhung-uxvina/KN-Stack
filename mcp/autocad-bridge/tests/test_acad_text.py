"""Test hàm thuần + quét DXF ngoại tuyến. Không cần AutoCAD.  Chạy: python -m pytest mcp/autocad-bridge/tests -v

Mọi mã chi tiết, tên chi tiết, kích thước ở đây là DỮ LIỆU MẪU — không lấy từ hồ sơ thật.
"""
import sys
from pathlib import Path

import ezdxf
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acad_text import (clean_mtext, format_measurement, is_balloon, name_matches_file,  # noqa: E402
                       parse_sl_label, render_dim_text, title_fields)
from dxf_scan import dxf_summary, file_index, scan_folder  # noqa: E402

BS = "\\"


# --- clean_mtext: các dạng mã MText thường gặp trong bản vẽ TCVN -----------------
@pytest.mark.parametrize("raw, want", [
    (BS + "fTCVN 7284|b0|i1;" + BS + "H100.0000;KHUNG ĐỠ MẪU", "KHUNG ĐỠ MẪU"),
    (BS + "fTCVN 7284|b0|i1;Gân tăng cứng" + BS + "P" + BS + "fTCVN 7284|b0|i1;chi tiết 1",
     "Gân tăng cứng chi tiết 1"),
    ("Đ" + BS + "U+01AF" + BS + "U+1EE2C THỬ", "ĐƯỢC THỬ"),
    ("%%c30h7", "Ø30h7"),
    ("4200%%p2", "4200±2"),
    ("{" + BS + "C1;đỏ}", "đỏ"),
    ("a" + BS + "S1^2;b", "a1/2b"),
    ("", ""),
])
def test_clean_mtext(raw, want):
    assert clean_mtext(raw) == want


def test_clean_mtext_keeps_paragraphs_when_asked():
    assert clean_mtext("a" + BS + "Pb", para_sep="\n") == "a\nb"


# --- chữ kích thước -------------------------------------------------------------
def test_format_measurement_suppresses_zeros_and_uses_separator():
    assert format_measurement(212.5, precision=2, decimal_sep=",") == "212,5"
    assert format_measurement(4200.0000000006, precision=2) == "4200"


@pytest.mark.parametrize("override, meas, want", [
    ("", 300.0000000000036, "300"),
    ("<>", 120.0, "120"),
    (BS + "fTCVN 7284|b0|i1;<>±2", 4200.000000000006, "4200±2"),
    ("900", 512.3, "900"),             # override cứng — số đo hình học bị bỏ qua (hình cắt rút gọn)
])
def test_render_dim_text(override, meas, want):
    assert render_dim_text(override, meas) == want


# --- nhãn SL / bóng số ----------------------------------------------------------
def test_parse_sl_label_full():
    assert parse_sl_label("SL 02; TL 1/2; VL NHÔM 5083") == {"qty": 2, "scale": "1/2", "material": "NHÔM 5083"}


def test_parse_sl_label_without_material():
    assert parse_sl_label("SL 01; TL 1/4") == {"qty": 1, "scale": "1/4", "material": None}


@pytest.mark.parametrize("text", ["Tấm đỡ CT3", "SLOT 3", "1 : 20"])
def test_parse_sl_label_rejects_non_labels(text):
    assert parse_sl_label(text) is None


def test_is_balloon():
    assert is_balloon("10") and not is_balloon("1 : 20") and not is_balloon("100")


# --- khung tên ------------------------------------------------------------------
def test_title_fields_maps_cells_with_insert_scale():
    o, s = (1000.0, -500.0), 20.0
    at = lambda lx, ly: (o[0] + lx * s, o[1] + ly * s)  # noqa: E731
    texts = [(*at(220, 117), "KHUNG ĐỠ MẪU"), (*at(267, 129), "SP.10.02.01"), (*at(275, 111), "12"),
             (*at(293, 112), "1 : 20"), (*at(256, 101), "01"), (*at(292, 101), "05"), (*at(207, 96), "NHÔM 5083")]
    f = title_fields(texts, o, s)
    assert f == {"name": "KHUNG ĐỠ MẪU", "material": "NHÔM 5083", "code": "SP.10.02.01", "mass": "12",
                 "scale": "1 : 20", "sheet": "01", "sheets": "05"}


# --- DXF ngoại tuyến ------------------------------------------------------------
def _make_sheet(path, code, name, extra=()):
    doc = ezdxf.new("R2010")
    blk = doc.blocks.new("Title Blocks KHUNG TÊN BẢN VẼ LẮP")
    blk.add_line((0, 0), (300, 0))
    msp = doc.modelspace()
    msp.add_blockref(blk.name, (0, 0), dxfattribs={"xscale": 1, "yscale": 1})
    msp.add_text(name, dxfattribs={"insert": (220, 117)})
    msp.add_text(code, dxfattribs={"insert": (267, 129)})
    msp.add_text("NHÔM 5083", dxfattribs={"insert": (207, 96)})
    for t, xy in extra:
        msp.add_mtext(t, dxfattribs={"insert": xy})
    msp.add_circle((10, 10), 3.3)
    msp.add_circle((90, 10), 3.3)
    doc.saveas(path)


def test_file_index():
    assert file_index("4.1.2  khung do") == "4.1.2"
    assert file_index("4.cum do-tong lap") == "4"
    assert file_index("ban ve") == ""


def test_dxf_summary_reads_title_labels_holes(tmp_path):
    p = tmp_path / "4.1.2 khung.dxf"
    _make_sheet(p, "SP.10.02.01", "KHUNG ĐỠ MẪU", [("SL 08; TL 1/3; VL NHÔM 5083", (10, 400))])
    s = dxf_summary(str(p))
    assert s["index"] == "4.1.2"
    assert s["title"]["code"] == "SP.10.02.01" and s["title"]["material"] == "NHÔM 5083"
    assert s["part_labels"][0]["qty"] == 8
    assert s["holes"]["Ø6.6"]["count"] == 2


def test_scan_folder_balloons_exclude_title_block_numbers(tmp_path):
    # tờ lắp: bóng số 1, 2 trên hình; «60» là ô khối lượng trong khung tên — không phải bóng số
    _make_sheet(tmp_path / "4.cum do-tong lap.dxf", "SP.10.02.00 BL", "CỤM ĐỠ",
                [("1", (900, 900)), ("2", (950, 900)), ("60", (275, 111))])
    row = scan_folder(str(tmp_path))["rows"][0]
    assert row["assembly"] and row["balloons"] == "1,2" and row["mass"] == "60"


def test_scan_folder_warns_when_title_block_is_empty(tmp_path):
    doc = ezdxf.new("R2010")
    doc.blocks.new("TITLE_BLOCKS_KHUNG_TEN")
    doc.modelspace().add_blockref("TITLE_BLOCKS_KHUNG_TEN", (0, 0))
    doc.saveas(tmp_path / "4.1.4 khung.dxf")
    assert "khung tên rỗng" in scan_folder(str(tmp_path))["rows"][0]["warn"]


@pytest.mark.parametrize("stem, name, ok", [
    ("4.3 tam de", "VÀNH ĐỠ", False),                         # khung tên chép nguyên từ tờ khác
    ("4.9 co cau chan", "VÀNH ĐỠ", False),
    ("4.2.1  vanh do", "VÀNH ĐỠ", True),
    ("4.7 hop 40x80", "KHUNG HỘP 40x80x4", True),
    ("2.7 ccu chan", "CỮ CHẶN", True),                        # lỗi gõ tên tệp vẫn khớp nhờ từ chung
    ("2.2 tai ga", "", True),                                 # tên trống ⇒ không kết luận
])
def test_name_matches_file(stem, name, ok):
    assert name_matches_file(stem, name) is ok


def test_scan_folder_flags_copied_title_with_same_name(tmp_path):
    _make_sheet(tmp_path / "4.2.1 vanh do.dxf", "SP.10.01.03", "VÀNH ĐỠ")
    _make_sheet(tmp_path / "4.3 tam de.dxf", "SP.10.01.03", "VÀNH ĐỠ")
    rows = {r["index"]: r for r in scan_folder(str(tmp_path))["rows"]}
    assert "tên tệp" in rows["4.3"]["warn"] and rows["4.2.1"]["warn"] == ""


def test_scan_folder_flags_duplicate_sheet_number(tmp_path):
    for stem in ("4.1.2 khung do", "4.1.6 khung do"):
        _make_sheet(tmp_path / f"{stem}.dxf", "SP.10.02.01", "KHUNG ĐỠ MẪU",
                    [("02", (256, 101)), ("05", (292, 101))])
    out = scan_folder(str(tmp_path))
    assert out["duplicate_sheets"] == [{"code": "SP.10.02.01", "sheet": "02/05",
                                        "files": ["4.1.2 khung do.dxf", "4.1.6 khung do.dxf"]}]
    assert all("trùng số tờ" in r["warn"] for r in out["rows"])


def test_scan_folder_flags_same_code_different_name_only(tmp_path):
    _make_sheet(tmp_path / "4.1 khung.dxf", "SP.10.02.01", "KHUNG ĐỠ MẪU")
    _make_sheet(tmp_path / "4.1.2 khung.dxf", "SP.10.02.01", "KHUNG ĐỠ MẪU")   # cùng chi tiết, tờ 2 ⇒ hợp lệ
    _make_sheet(tmp_path / "2.3 tai.dxf", "SP.10.01.03", "TAI BẮT")
    _make_sheet(tmp_path / "4.2 vanh.dxf", "SP.10.01.03", "VÀNH ĐỠ")             # chép khung tên ⇒ phải báo
    out = scan_folder(str(tmp_path), csv_out=str(tmp_path / "bom.csv"))
    assert [r["index"] for r in out["rows"]] == ["2.3", "4.1", "4.1.2", "4.2"]
    assert out["duplicate_codes"] == ["SP.10.01.03"]
    assert (tmp_path / "bom.csv").exists()
