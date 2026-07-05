import pytest

from leo_bridge import parsers

CALC_RESULT = """Để tính ứng suất uốn cho trục Ø25:
Công thức: sigma = M*c/I (theo Shigley's Mechanical Engineering Design, ch.3 [1])
Với M = 45 Nm, c = 12.5 mm, I = 19175 mm^4
=> sigma = 29.3 MPa. FoS = 250/29.3 = 8.5 (thép C45, Sy = 250 MPa theo datasheet [2])
Nguồn: [1] Shigley 11th ed. [2] https://matweb.com/c45
"""

PART_RESULT = """Tìm thấy 3 ứng viên phù hợp envelope Ø25 H7:
| Part | Vendor | PN | Khớp |
|---|---|---|---|
| Bạc đạn 6205-2RS | SKF | 6205-2RS1 | 95% |
| Bạc đạn 6205 ZZ | NSK | 6205ZZCM | 93% |
Kết luận: tái dùng 6205-2RS1, không cần thiết kế mới.
Nguồn: ISO 15242, catalog SKF https://skf.com/6205
"""

NO_CITE_RESULT = """Ứng suất khoảng 30 MPa, FoS tầm 8, dùng thép C45 là được.
Không cần kiểm tra thêm gì cả, thiết kế này ổn với tải đã cho nhé anh.
"""


def test_calc_result_extracts_numbers_and_citations():
    parsed, checklist = parsers.parse_result("C", CALC_RESULT)
    assert parsed["has_citations"] is True
    units = {n["unit"] for n in parsed["numbers"]}
    assert "MPa" in units and "Nm" in units
    # mỗi số 1 mục checklist, mặc định UNVERIFIED
    assert all(c["status"] == "UNVERIFIED" for c in checklist)
    assert len(checklist) >= len(parsed["numbers"])


def test_part_result_parses_table_rows():
    parsed, checklist = parsers.parse_result("A", PART_RESULT)
    assert len(parsed["parts"]) == 2
    assert "SKF" in parsed["parts"][0]["raw_cells"]


def test_no_citation_flagged_red():
    parsed, checklist = parsers.parse_result("C", NO_CITE_RESULT)
    assert parsed["has_citations"] is False
    assert any("KHÔNG cite" in c["item"] for c in checklist)


def test_too_short_raises():
    with pytest.raises(parsers.ParseError):
        parsers.parse_result("A", "ok")
