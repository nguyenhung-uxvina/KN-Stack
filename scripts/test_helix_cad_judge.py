"""Tests for skills/helix/helix-cad-judge/judge_score.py — deterministic verdict from answers to signed questions.

Each rule has a mutant that would slip through if the rule were missing. Pure JSON, no build123d.
Run: python -m pytest scripts/test_helix_cad_judge.py -v
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location(
    "judge_score", os.path.join(ROOT, "skills", "helix", "helix-cad-judge", "judge_score.py"))
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)

QUESTIONS = [
    {"id": "Q1", "q": "Lỗ ở đầu +X tròn?", "spec_line": "Lỗ thông Ø10 cách đầu +X 30", "severity": "block"},
    {"id": "Q2", "q": "Vát ở mép ngoài mặt +Z?", "spec_line": "Vát 1x45 cạnh ngoài mặt trên", "severity": "comment"},
]
MODEL = "\n".join(f"line_{i}" for i in range(1, 21)) + "\n"   # 20 lines


def yes(qid, **kw):
    return dict({"id": qid, "answer": "yes", "view": "Iso", "code_line": 5, "reasoning": "thấy rõ"}, **kw)


def setup(tmp_path, answers, questions=QUESTIONS, gates_verdict="PASS", tamper_gates_hash=False):
    contract = {"part_id": "T", "bbox": [100, 40, 20], "judge_questions": questions}
    cp = tmp_path / "contract.json"
    cp.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")
    sha = J._sha256(str(cp))
    gp = tmp_path / "gates.json"
    gp.write_text(json.dumps({"verdict": gates_verdict, "contract_sha256": "0" * 64 if tamper_gates_hash else sha}),
                  encoding="utf-8")
    ap = tmp_path / "answers.json"
    ap.write_text(json.dumps(answers, ensure_ascii=False), encoding="utf-8")
    mp = tmp_path / "model.py"
    mp.write_text(MODEL, encoding="utf-8")
    return cp, gp, ap, mp, sha


def run(tmp_path, answers, approved=None, **kw):
    cp, gp, ap, mp, sha = setup(tmp_path, answers, **kw)
    rc = J.main(["--contract", str(cp), "--gates", str(gp), "--answers", str(ap), "--model", str(mp),
                 "--approved-hash", approved or sha, "--out", str(tmp_path / "v"), "--quiet"])
    out = tmp_path / "v.json"
    return rc, (json.load(open(out, encoding="utf-8")) if out.exists() else None)


def test_all_yes_with_evidence_passes(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")]})
    assert rc == 0 and v["verdict"] == "pass"


def test_block_question_no_blocks(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", answer="no"), yes("Q2")]})
    assert rc == 2 and v["verdict"] == "block"


def test_comment_question_no_is_comment_only(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2", answer="no")]})
    assert rc == 0 and v["verdict"] == "comment-only"


def test_unclear_goes_to_human(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", answer="unclear"), yes("Q2")]})
    assert rc == 5 and v["verdict"] == "needs_human"


def test_block_beats_unclear(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", answer="no"), yes("Q2", answer="unclear")]})
    assert v["verdict"] == "block"


def test_missing_answer_is_unclear_not_pass(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1")]})
    assert v["verdict"] == "needs_human"
    assert next(q for q in v["questions"] if q["id"] == "Q2")["note"] == "THIẾU câu trả lời"


def test_yes_without_reasoning_downgraded(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", reasoning=""), yes("Q2")]})
    assert v["verdict"] == "needs_human" and v["n_downgraded"] == 1


def test_yes_without_any_evidence_downgraded(tmp_path):
    a = {"id": "Q1", "answer": "yes", "reasoning": "chắc chắn"}
    rc, v = run(tmp_path, {"answers": [a, yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_no_without_evidence_cannot_block(tmp_path):
    """An unsupported 'no' must not block either — it becomes unclear (human), not a silent pass."""
    a = {"id": "Q1", "answer": "no", "reasoning": "có vẻ vuông"}
    rc, v = run(tmp_path, {"answers": [a, yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_code_line_out_of_range_downgraded(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", view=None, code_line=999), yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_invented_view_downgraded(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", view="Section A-A"), yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_duplicate_answers_are_unclear(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q1", answer="no"), yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_invalid_answer_word_downgraded(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1", answer="mostly"), yes("Q2")]})
    assert v["verdict"] == "needs_human"


def test_extra_findings_never_change_verdict(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")],
                           "extra_findings": [{"what": "lỗ thừa", "view": "Iso", "code_line": 3}]})
    assert v["verdict"] == "pass" and len(v["extra_findings"]) == 1


def test_answer_for_unknown_question_ignored(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2"), yes("Q99", answer="no")]})
    assert v["verdict"] == "pass" and v["ignored_answer_ids"] == ["Q99"]


def test_refuse_when_gates_not_pass(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")]}, gates_verdict="FAIL")
    assert rc == 3 and v is None


def test_refuse_draft_pass(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")]}, gates_verdict="DRAFT-PASS")
    assert rc == 3 and v is None


def test_refuse_when_gates_used_other_contract(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")]}, tamper_gates_hash=True)
    assert rc == 3 and v is None


def test_refuse_when_hash_mismatch(tmp_path):
    rc, v = run(tmp_path, {"answers": [yes("Q1"), yes("Q2")]}, approved="f" * 64)
    assert rc == 3 and v is None


def test_refuse_without_signed_questions(tmp_path):
    rc, v = run(tmp_path, {"answers": []}, questions=[])
    assert rc == 3 and v is None


def test_refuse_question_without_spec_line(tmp_path):
    bad = [dict(QUESTIONS[0], spec_line="")]
    rc, v = run(tmp_path, {"answers": [yes("Q1")]}, questions=bad)
    assert rc == 3 and v is None
