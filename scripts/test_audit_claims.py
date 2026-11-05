"""Tests for skills/helix/helix-cad-validate/audit_claims.py (P–C–C G0 claim records). Stdlib only, synthetic data.
Run: python -m pytest scripts/test_audit_claims.py -v
"""
import importlib.util
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "audit_claims", os.path.join(ROOT, "skills", "helix", "helix-cad-validate", "audit_claims.py"))
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)


def extract(**kw):
    base = {"meta": {"part_id": "TEST.01", "code_in_dxf": "TEST.01", "file_index": "1", "material": "STEEL"},
            "dimensions": [{"value": 70.0, "source_tag": "D"}, {"value": 9.0, "source_tag": "D"}],
            "holes": [{"dia": 9.0, "count": 4, "source_tag": "G"}], "conflicts": [], "missing": []}
    for k, v in kw.items():
        if k == "meta":
            base["meta"] = dict(base["meta"], **v)
        else:
            base[k] = v
    return base


def statuses(claims, rule):
    return [c["status"] for c in claims if c["rule_id"] == rule]


def w(tmp_path, name, obj):
    p = tmp_path / name
    p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    return str(p)


GATES_PASS = {"version": "1.1", "mode": "release", "verdict": "PASS",
              "checks": [{"rule_id": "F1_closed_brep", "status": "PASS"}, {"rule_id": "MASS_vs_title", "status": "INFO"}]}
VALIDATE_PASS = {"version": "1.0", "checks": [{"rule_id": "materials", "status": "PASS", "observed": "STEEL"}]}
JUDGE_PASS = {"version": "2.0", "questions": [{"id": "Q1", "q": "?", "severity": "block", "answer": "yes",
                                               "view": "Iso", "code_line": 3}], "extra_findings": []}


# ── Perception: the three error kinds found on a real drawing set (2026-11-05) ──

def test_missing_material_needs_evidence():
    c = A.from_extract(extract(meta={"material": None}), "P", "x")
    assert statuses(c, "material_present") == ["NEEDS_EVIDENCE"]


def test_undimensioned_hole_needs_evidence():
    c = A.from_extract(extract(holes=[{"dia": 22.0, "count": 1, "source_tag": "G"}]), "P", "x")
    assert statuses(c, "hole_dia_undimensioned") == ["NEEDS_EVIDENCE"]


def test_dimensioned_hole_is_not_flagged():
    c = A.from_extract(extract(), "P", "x")   # Ø9 measured AND a D dimension of 9 exists
    assert statuses(c, "hole_dia_undimensioned") == []


def test_duplicate_part_code_across_sheets_needs_context():
    a = extract(meta={"code_in_dxf": "TEST.07", "file_index": "2.6"})
    b = extract(meta={"code_in_dxf": "TEST.07", "file_index": "4.10"})
    c = A.set_check([("a.json", a), ("b.json", b), ("c.json", extract(meta={"code_in_dxf": "TEST.09"}))])
    assert len(c) == 2 and {x["status"] for x in c} == {"NEEDS_CONTEXT"}


def test_break_view_is_advisory_other_conflict_contested():
    c = A.from_extract(extract(conflicts=[{"type": "BREAK-VIEW", "detail": "1300 vs 850"},
                                          {"type": "TEXT-VS-GEOMETRY", "detail": "Ø14 vs 12.5"}]), "P", "x")
    assert statuses(c, "break_view") == ["ADVISORY"]
    assert statuses(c, "conflict_TEXT-VS-GEOMETRY") == ["CONTESTED"]


def test_missing_list_mapping():
    c = A.from_extract(extract(missing=["3 ARC entities chưa quy thành lỗ", "code_in_dxf từ khung tên — KHÔNG tin cậy",
                                        "Tên chi tiết không suy ra được"]), "P", "x")
    assert statuses(c, "unrecognised_geometry") == ["NEEDS_RECOGNITION_REVIEW"]
    assert statuses(c, "title_block_code_untrusted") == ["NEEDS_CONTEXT"]
    assert statuses(c, "missing") == ["NEEDS_EVIDENCE"]


# ── Cognition ──

def test_validate_failsafe_vs_confidence_vs_real_fail():
    rep = {"checks": [{"rule_id": "materials", "status": "FAIL", "observed": "(none)"},
                      {"rule_id": "plate_thickness_mm", "status": "FAIL", "observed": "5 mm (conf=LOW)"},
                      {"rule_id": "mass_kg", "status": "FAIL", "observed": "12 kg"}]}
    c = A.from_validate(rep, "P", "v")
    assert [x["status"] for x in c] == ["NEEDS_EVIDENCE", "NEEDS_RECOGNITION_REVIEW", "FAIL"]


def test_gates_skip_is_needs_evidence_info_is_advisory():
    rep = {"checks": [{"rule_id": "F2_probes", "status": "SKIP"}, {"rule_id": "MASS_vs_title", "status": "INFO"},
                      {"rule_id": "F1_closed_brep", "status": "FAIL"}]}
    assert [x["status"] for x in A.from_gates(rep, "P", "g")] == ["NEEDS_EVIDENCE", "ADVISORY", "FAIL"]


# ── LLM ──

def test_judge_mapping():
    v = {"questions": [{"id": "Q1", "severity": "block", "answer": "no"}, {"id": "Q2", "severity": "comment", "answer": "no"},
                       {"id": "Q3", "severity": "block", "answer": "unclear"}, {"id": "Q4", "severity": "block", "answer": "yes"}],
         "extra_findings": [{"what": "gân vát 10 mm"}]}
    c = A.from_judge(v, "P", "j")
    assert [x["status"] for x in c] == ["FAIL", "ADVISORY", "NEEDS_HUMAN_RELEASE", "PASS", "ADVISORY"]


# ── aggregate ──

def test_full_profile_missing_judge_abstains(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract()), "validate": w(tmp_path, "v.json", VALIDATE_PASS),
                          "gates": w(tmp_path, "g.json", GATES_PASS)}, "full")
    assert rec["machine_verdict"] == "BLOCKED"
    assert statuses(rec["claims"], "required_input_judge") == ["ABSTAINED"]


def test_all_clean_is_ready_never_released(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract()), "validate": w(tmp_path, "v.json", VALIDATE_PASS),
                          "gates": w(tmp_path, "g.json", GATES_PASS), "judge": w(tmp_path, "j.json", JUDGE_PASS)}, "full")
    assert rec["machine_verdict"] == "READY_FOR_HUMAN_RELEASE"
    assert "RELEASED" not in json.dumps(rec)


def test_one_blocking_claim_blocks(tmp_path):
    """Only NEEDS_EVIDENCE (missing material) may be blocking here — every required input is present."""
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract(meta={"material": None})),
                          "validate": w(tmp_path, "v.json", VALIDATE_PASS)}, "drawing")
    blocking = [c["status"] for c in rec["claims"] if c["status"] not in ("PASS", "ADVISORY")]
    assert blocking == ["NEEDS_EVIDENCE"] and rec["machine_verdict"] == "BLOCKED"


def test_claim_ids_deterministic_and_unique():
    c1 = A.from_extract(extract(missing=["a", "b"]), "P", "x")
    c2 = A.from_extract(extract(missing=["a", "b"]), "P", "x")
    assert [x["claim_id"] for x in c1] == [x["claim_id"] for x in c2]
    assert len({x["claim_id"] for x in c1}) == len(c1)


def test_cli_exit_codes(tmp_path):
    e = w(tmp_path, "e.json", extract(meta={"material": None}))
    assert A.main(["collect", "--part", "P", "--extract", e, "--profile", "drawing", "--out", str(tmp_path / "c")]) == 2
    assert A.main(["collect", "--part", "P", "--extract", str(tmp_path / "nope.json"), "--out", str(tmp_path / "d")]) == 3


# ── report drift ──

def test_generated_report_passes_check(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract(meta={"material": None},
                                                                     conflicts=[{"type": "BREAK-VIEW", "detail": "x"}]))}, "drawing")
    assert A.check_report(rec, A.render_md(rec)) == []


def test_report_line_without_claim_id_is_drift(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract(meta={"material": None}))}, "drawing")
    md = A.render_md(rec) + "\n- Tấm dày 6 mm là sai (agent tự kết luận)\n"
    assert any("không trích claim_id" in why for _, why, _ in A.check_report(rec, md))


def test_report_citing_unknown_claim_is_drift(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract())}, "drawing")
    md = "- [C-0123456789] lỗi bịa\n"
    assert any("không có trong bản ghi" in why for _, why, _ in A.check_report(rec, md))


# ── spec gate ──

def test_spec_with_question_mark_label_blocked():
    s = "| 6 | Vạt mũi | \"18\"? | **?** | không khớp |\n"
    assert A.check_spec(s)


def test_spec_with_unanswered_section_blocked():
    assert A.check_spec("## Câu hỏi cho CEO\n1. Góc cắt?\n")


def test_spec_answered_but_not_rewritten_blocked():
    assert A.check_spec("## Câu hỏi đã được CEO trả lời 05/11 — dựng đúng phương án nháp\n2. \"18\" là gì?\n")


def test_clean_spec_passes():
    s = "## Hình học\n| 1 | Dài | 145 | D | |\n## Quyết định CEO\n- KHÔNG dựng vạt \"18\".\n"
    assert A.check_spec(s) == []


# ── release ──

def test_release_refused_when_blocked(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract(meta={"material": None}))}, "drawing")
    with pytest.raises(ValueError):
        A.release(rec, "Kỹ sư A", "")


def test_release_requires_signer_and_hashes_claims(tmp_path):
    rec = A.collect("P", {"extract": w(tmp_path, "e.json", extract()), "validate": w(tmp_path, "v.json", VALIDATE_PASS)}, "drawing")
    with pytest.raises(ValueError):
        A.release(rec, "  ", "")
    r = A.release(rec, "Kỹ sư A", "ok")
    assert r["status"] == "RELEASED" and len(r["claims_sha256"]) == 64 and r["signer"] == "Kỹ sư A"
