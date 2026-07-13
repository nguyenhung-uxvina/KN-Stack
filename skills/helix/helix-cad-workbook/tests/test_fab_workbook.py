import json
import os
import subprocess
import sys

import openpyxl
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(SKILL, "..", "..", ".."))
FIX = os.path.join(REPO, "evals", "fixtures", "cad-workbook")
sys.path.insert(0, SKILL)

import fab_workbook as fw  # noqa: E402


@pytest.fixture()
def master_path(tmp_path):
    p = str(tmp_path / "WX-MASTER-DATA.xlsx")
    fw.init_master(p)
    return p


def test_init_master_seed(master_path):
    wb = openpyxl.load_workbook(master_path)
    for s in ["_META"] + fw.MASTER_SHEETS:
        assert s in wb.sheetnames
    ws = wb["MATERIALS"]
    header = [c.value for c in ws[1]]
    assert header[:5] == ["item_code", "item_name", "material_class", "uom", "rate"]
    rates = {r[0].value: r[4].value for r in ws.iter_rows(min_row=2)}
    assert rates["MAT-SS400"] == 18500


def test_load_extracts_and_bom():
    extracts = fw.load_extracts(FIX)
    assert [e["meta"]["part_id"] for _, e in extracts] == ["P-001", "P-002", "P-003"]
    bom = fw.load_master_bom(FIX)
    assert bom["p-001"]["qty"] == "2"
    assert bom["p-003"]["material"] == ""


def test_resolve_param():
    extracts = dict((e["meta"]["part_id"], e) for _, e in fw.load_extracts(FIX))
    bom = fw.load_master_bom(FIX)
    v, conf = fw.resolve_param(extracts["P-001"], bom.get("p-001"), "mass_kg")
    assert v == 4.2 and conf == "MED"
    v, _ = fw.resolve_param(extracts["P-001"], bom.get("p-001"), "qty")
    assert v == "2"
    v, _ = fw.resolve_param(extracts["P-003"], bom.get("p-003"), "material")
    assert v in (None, "")


def test_helpers(master_path):
    master = fw.load_master(master_path)
    assert fw.ops_from_process("laser+chấn") == ["laser", "chan"]
    assert fw.material_class("SS400", master) == "thep_tam"
    assert fw.material_code("NHÔM 5083", master) == "MAT-5083"
    assert fw.material_code("titan", master) == ""


def test_build_parts_bom(tmp_path, master_path):
    out = str(tmp_path / "FIXTURE_FAB-DB.xlsx")
    fw.main([FIX, "--master", master_path, "--project", "FIXTURE", "--out", out])
    wb = openpyxl.load_workbook(out)
    for s in ["_META", "PARTS", "BOM"] + fw.MASTER_SHEETS:
        assert s in wb.sheetnames
    parts = {r[0].value: r for r in wb["PARTS"].iter_rows(min_row=2)}
    assert parts["P-001"][6].value == 4.2          # mass_kg
    assert parts["P-001"][7].value == 2            # qty
    bom_header = [c.value for c in wb["BOM"][1]]
    assert bom_header == ["item_code", "item_name", "description", "qty_per_unit",
                          "uom", "material", "spec", "process"]
