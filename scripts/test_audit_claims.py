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


# ── 2D master vs 3D witness (helix-cad-crosscheck) ──

XC_PASS = {"version": "1.0", "verdict": "PASS",
           "checks": [{"rule_id": "X2_visible", "status": "PASS", "locator": "top"},
                      {"rule_id": "X2_modelled_not_drawn", "status": "INFO", "attribution": "simplified",
                       "locator": "top:m3"}]}
MUT_OK = {"baseline_verdict": "PASS", "total": 4, "caught": 4, "attribution_right": 4, "mutants": []}


def test_crosscheck_mapping_keeps_attribution():
    rep = {"checks": [{"rule_id": "X2_drawn_not_modelled", "status": "FAIL", "attribution": "model", "locator": "top:8C"},
                      {"rule_id": "X2_drawn_not_modelled", "status": "CONTESTED", "attribution": "drawing",
                       "locator": "side:A0"},
                      {"rule_id": "X2_modelled_not_drawn", "status": "INFO", "attribution": "simplified"}]}
    c = A.from_crosscheck(rep, "P", "x")
    assert [x["status"] for x in c] == ["FAIL", "CONTESTED", "ADVISORY"]
    assert "quy cho: drawing" in c[1]["message"] and c[1]["locator"].startswith("side:A0")
    assert len({x["claim_id"] for x in c}) == 3


def test_mutate_mapping():
    assert statuses(A.from_mutate(MUT_OK, "P", "m"), "L6_positive_control") == ["PASS"]
    wrong = dict(MUT_OK, attribution_right=3)
    assert statuses(A.from_mutate(wrong, "P", "m"), "L6_positive_control") == ["FAIL"]
    esc = dict(MUT_OK, caught=3, mutants=[{"name": "D1_move_circle_y", "caught": False}])
    assert statuses(A.from_mutate(esc, "P", "m"), "L6_escaped") == ["FAIL"]
    assert statuses(A.from_mutate({"baseline_verdict": "FAIL"}, "P", "m"), "L6_positive_control") == ["NEEDS_EVIDENCE"]


def test_reconstruct_profile_needs_positive_control(tmp_path):
    base = {"gates": w(tmp_path, "g.json", GATES_PASS), "crosscheck": w(tmp_path, "x.json", XC_PASS)}
    rec = A.collect("P", base, "reconstruct")
    assert rec["machine_verdict"] == "BLOCKED" and statuses(rec["claims"], "required_input_mutate") == ["ABSTAINED"]
    rec = A.collect("P", dict(base, mutate=w(tmp_path, "m.json", MUT_OK)), "reconstruct")
    assert rec["machine_verdict"] == "READY_FOR_HUMAN_RELEASE"


def test_cli_accepts_crosscheck_inputs(tmp_path):
    out = str(tmp_path / "o")
    assert A.main(["collect", "--part", "P", "--gates", w(tmp_path, "g.json", GATES_PASS),
                   "--crosscheck", w(tmp_path, "x.json", XC_PASS), "--mutate", w(tmp_path, "m.json", MUT_OK),
                   "--profile", "reconstruct", "--out", out]) == 0


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


# ── G2a cross-sheet rules (synthetic set) ──

def sheet(idx, code, name, material=None, bom=(), texts=(), fname=None):
    tb = {"found": True, "code": {"value": code}, "name": {"value": name} if name else None,
          "material": {"value": material} if material else None}
    ex = {"meta": {"file_index": idx, "code_in_dxf": code, "name": name, "material": material, "title_block": tb},
          "bom": [dict(r) for r in bom], "raw_text": [{"text": t} for t in texts], "dimensions": [], "holes": [],
          "conflicts": [], "missing": []}
    return (fname or f"{idx}_x.cad_extract.json", ex)


def rules(claims, rule):
    return [c for c in claims if c["rule_id"] == rule]


def test_g2a_bom_code_and_name():
    s = [sheet("1", "99.TS-01.05.00 BL", "CỤM A", bom=[
            {"code": "99.TS-01.05.01", "name": "Thanh treo 1", "qty": "02"},
            {"code": "99.TS-01.05.02", "name": "Thanh treo 3", "qty": "01"},      # wrong code: sheet 3 is "Bia 10"
            {"code": "99.TS-01.05.09", "name": "Không có tờ", "qty": "01"},
            {"code": "Bu lông M8", "name": None, "qty": "16"},                   # standard part spilled into code col
            {"code": "99.TS-01.05.00", "name": "Cụm A", "qty": "01"}]),          # assembly listed without ' BL'
         sheet("2", "99.TS-01.05.01", "THANH TREO 1"), sheet("3", "99.TS-01.05.02", "BIA 10")]
    c = A.set_check(s)
    assert [x["observed"] for x in rules(c, "bom_name_matches_sheet")] == ["Thanh treo 3"]
    assert [x["observed"] for x in rules(c, "bom_code_matches_sheet")] == ["99.TS-01.05.09"]


def test_g2a_material_same_with_standard_is_consistent():
    s = [sheet("1", "99.TS-01.05.00 BL", "CỤM A", bom=[
            {"code": "99.TS-01.05.01", "name": "Thanh 1", "material": "Thép SS400"},
            {"code": "99.TS-01.05.02", "name": "Thanh 2", "material": "Thép Hợp kim SS400"}]),
         sheet("2", "99.TS-01.05.01", "THANH 1", "THÉP SS400 JIS G3101"),
         sheet("3", "99.TS-01.05.02", "THANH 2", "THÉP SS400 JIS G3101")]
    assert [x["observed"] for x in rules(A.set_check(s), "material_consistent")] == ["Thép Hợp kim SS400"]


def test_g2a_title_vs_yckt_material_and_quantity():
    s = [sheet("1", "99.TS-01.00.00", "BỐ TRÍ", bom=[{"code": "99.TS-01.08.00", "name": "Thanh chống", "qty": "02"},
                                                    {"code": "99.TS-01.09.00", "name": "Mã cạnh", "qty": "08"}]),
         sheet("2", "99.TS-01.08.00", "THANH CHỐNG", "THÉP AH36",
               texts=["Yêu cầu kỹ thuật: - Vật liệu: Thép tấm s8. - Số lượng: 12 chiếc."]),
         sheet("3", "99.TS-01.09.00", "MÃ CẠNH", "THÉP SS400", texts=["- Số lượng: 08 chiếc."])]
    c = A.set_check(s)
    assert [x["part_id"] for x in rules(c, "qty_matches_parent")] == ["2"]
    assert [x["part_id"] for x in rules(c, "material_consistent")] == ["2"]


def test_g2a_code_case_mixed_set_flags_all_convention_flags_offenders():
    s = [sheet("1", "99.ts-01.01.00", "A"), sheet("2", "99.ts-01.02.00", "B"), sheet("3", "99.TS-01.03.00", "C")]
    assert len(rules(A.set_check(s), "part_code_format")) == 3
    assert [x["part_id"] for x in rules(A.set_check(s, "upper"), "part_code_format")] == ["1", "2"]
    uni = [sheet("1", "99.TS-01.01.00", "A"), sheet("2", "99.TS-01.02.00", "B")]
    assert rules(A.set_check(uni), "part_code_format") == []


def test_g2a_continuation_sheets_are_not_duplicates():
    s = [sheet("7", "99.TS-01.01.00", "THÂN PHAO", fname="07_x.cad_extract.json"),
         sheet("8", "99.TS-01.01.00", None, fname="08_THAN_to02-03.cad_extract.json"),
         sheet("10", "99.TS-01.02.00", "DẦM"), sheet("11", "99.TS-01.02.00", "DẦM CUỐI")]
    dup = rules(A.set_check(s), "part_code_unique")
    assert sorted(x["part_id"] for x in dup) == ["10", "11"]


def test_g2a_group_code_row_not_compared_to_first_sheet():
    """Measured false claim: a row "14.00; 14.01; 14.03 — Cụm thiết bị" was compared with sheet 14.00's name."""
    s = [sheet("1", "99.TS-01.00.00", "BỐ TRÍ", bom=[
            {"code": "99.TS-01.14.00", "code_cell": "99.TS-01.14.00; 14.01; 14.03", "code_group": True,
             "name": "Cụm thiết bị trên bia", "qty": "03"}]),
         sheet("39", "99.TS-01.14.00", "MẠCH CẢM BIẾN")]
    assert rules(A.set_check(s), "bom_name_matches_sheet") == []


def test_g2a_quantity_compared_with_sum_over_parents():
    """Measured false claim: a part used once in each of two assemblies, YCKT says 02."""
    s = [sheet("13", "99.TS-01.05.00 BL", "CỤM 1", bom=[{"code": "99.TS-01.05.02", "name": "Thanh", "qty": "01"}]),
         sheet("22", "99.TS-01.06.00 BL", "CỤM 2", bom=[{"code": "99.TS-01.05.02", "name": "Thanh", "qty": "01"}]),
         sheet("15", "99.TS-01.05.02", "THANH", texts=["- Số lượng: 02 chiếc."]),
         sheet("29", "99.TS-01.07.01", "GIỮ SỐ", texts=["- Số lượng: 02 chiếc."]),
         sheet("28", "99.TS-01.07.00 BL", "CỤM 3", bom=[{"code": "99.TS-01.07.01", "name": "Giữ số", "qty": "01"}])]
    assert [x["part_id"] for x in rules(A.set_check(s), "qty_matches_parent")] == ["29"]
