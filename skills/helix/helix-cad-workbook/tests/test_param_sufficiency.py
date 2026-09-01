import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
VALIDATE = os.path.join(REPO, "skills", "helix", "helix-cad-validate", "validate.py")
FIX = os.path.join(REPO, "evals", "fixtures", "cad-workbook")
RULES = os.path.join(FIX, "design_rules.param.json")


def run_validate(extract, tmp_path):
    return subprocess.run(
        [sys.executable, VALIDATE, "--extract", os.path.join(FIX, extract),
         "--rules", RULES, "--out", str(tmp_path / "rep"), "--quiet"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"))


def test_pass_when_sufficient(tmp_path):
    r = run_validate("P-001_rev0.cad_extract.json", tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    rep = json.load(open(str(tmp_path / "rep") + ".json", encoding="utf-8"))
    ids = {c["rule_id"]: c["status"] for c in rep["checks"] if c["rule_id"] == "param_sufficiency"}
    assert ids and "FAIL" not in ids.values()


def test_fail_when_missing_material(tmp_path):
    r = run_validate("P-003_rev0.cad_extract.json", tmp_path)
    assert r.returncode == 2
    rep = json.load(open(str(tmp_path / "rep") + ".json", encoding="utf-8"))
    fails = [c for c in rep["checks"] if c["rule_id"] == "param_sufficiency" and c["status"] == "FAIL"]
    assert any("material" in c["observed"] for c in fails)
    assert any("mass_kg" in c["observed"] for c in fails)


def test_fail_safe_missing_requirements(tmp_path):
    bad = tmp_path / "rules_bad.json"
    rules = json.load(open(RULES, encoding="utf-8"))
    rules["rules"]["param_sufficiency"]["requirements_json"] = "KHONG_TON_TAI.json"
    bad.write_text(json.dumps(rules), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, VALIDATE, "--extract", os.path.join(FIX, "P-001_rev0.cad_extract.json"),
         "--rules", str(bad), "--out", str(tmp_path / "rep2"), "--quiet"],
        cwd=REPO, capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONUTF8="1"))
    assert r.returncode == 2   # fail-safe: thiếu requirements = FAIL, không SKIP
