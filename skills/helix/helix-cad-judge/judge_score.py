#!/usr/bin/env python3
"""
helix-cad-judge / judge_score.py — DETERMINISTIC verdict from an LLM judge's answers to SIGNED questions.

Design (CADCodeVerify, arXiv 2410.05340, adapted): binary verification questions are derived from the spec, the
judge answers each one Yes / No / Unclear with reasoning from rendered views. Measured there: answers correct only
64.6–68.2 %, "Unclear" 26.6 % (Table 9). So here:
  * the questions are written ONCE, reviewed and signed by the engineer, and stored in geometry_contract.json
    (`judge_questions[]`) — covered by the same --approved-hash as the geometry gate; the judge cannot pick
    easy questions for itself;
  * the judge agent writes only judge_answers.json; it never writes the verdict;
  * this script computes the verdict: an answer without reasoning + evidence (a rendered view or a model.py line
    that exists) is downgraded to "unclear"; any "unclear" goes to a human; findings outside the signed questions
    are shown to the CEO but never change the verdict.

Preconditions (refuse ⇒ exit 3): cad_gates_report.json verdict == "PASS" (DRAFT-PASS refused) and its
contract_sha256 == sha256(contract) == --approved-hash.

Verdict: block (a block-severity question answered "no") > needs_human (any "unclear") > comment-only
(a comment-severity "no") > pass.
Exit: 0 pass / comment-only · 2 block · 5 needs_human · 3 refused / usage / IO error.

Usage:
  python judge_score.py --contract geometry_contract.json --gates cad_gates_report.json \
                        --answers judge_answers.json --model model.py --approved-hash <sha256> [--out judge_verdict]
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone

VIEWS = {"Front", "Back", "Left", "Right", "Top", "Bottom", "Iso"}
ANSWERS = {"yes", "no", "unclear"}
SEVERITIES = {"block", "comment"}
MAX_QUESTIONS = 12
EXIT = {"pass": 0, "comment-only": 0, "block": 2, "needs_human": 5}


class Refused(Exception):
    pass


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_questions(contract):
    qs = contract.get("judge_questions") or []
    if not qs:
        raise Refused("Hợp đồng chưa có judge_questions[] — kỹ sư soạn + ký câu hỏi trước "
                      "(references/question-rules.md).")
    if len(qs) > MAX_QUESTIONS:
        raise Refused(f"{len(qs)} câu hỏi > {MAX_QUESTIONS} — tách chi tiết hoặc gộp câu trùng.")
    seen = set()
    for q in qs:
        qid = str(q.get("id", "")).strip()
        if not qid or qid in seen:
            raise Refused(f"judge_questions: id rỗng hoặc trùng ({qid!r}).")
        seen.add(qid)
        if not str(q.get("q", "")).strip() or not str(q.get("spec_line", "")).strip():
            raise Refused(f"{qid}: thiếu 'q' hoặc 'spec_line' (câu hỏi phải bám một dòng spec).")
        if q.get("severity") not in SEVERITIES:
            raise Refused(f"{qid}: severity phải là block|comment.")
    return qs


def check_preconditions(contract_path, gates, approved_hash):
    chash = _sha256(contract_path)
    if not approved_hash or chash != approved_hash.strip().lower():
        raise Refused("geometry_contract KHÔNG khớp --approved-hash (hoặc thiếu) — câu hỏi có thể đã bị sửa.")
    if gates.get("verdict") != "PASS":
        raise Refused(f"Cổng hình học verdict = {gates.get('verdict')!r} ≠ 'PASS' — judge không chạy "
                      "(DRAFT-PASS cũng bị từ chối).")
    if gates.get("contract_sha256") != chash:
        raise Refused("cad_gates_report được chấm với hợp đồng KHÁC hợp đồng đang dùng cho judge.")
    return chash


def grade_answer(q, a, n_lines):
    """Return (final_answer, note). Downgrade to 'unclear' when the answer is not backed by evidence."""
    if a is None:
        return "unclear", "THIẾU câu trả lời"
    ans = str(a.get("answer", "")).strip().lower()
    if ans not in ANSWERS:
        return "unclear", f"answer không hợp lệ ({a.get('answer')!r})"
    if ans == "unclear":
        return "unclear", "judge trả 'Không rõ'"
    if not str(a.get("reasoning", "")).strip():
        return "unclear", f"'{ans}' không kèm lập luận"
    view, line = a.get("view"), a.get("code_line")
    view_ok = view in VIEWS
    line_ok = isinstance(line, int) and not isinstance(line, bool) and 1 <= line <= n_lines
    if view is not None and not view_ok:
        return "unclear", f"view {view!r} không có trong bản render"
    if line is not None and not line_ok:
        return "unclear", f"code_line {line!r} không tồn tại trong model.py ({n_lines} dòng)"
    if not (view_ok or line_ok):
        return "unclear", f"'{ans}' không có chứng cứ (view hoặc code_line)"
    return ans, ""


def score(contract, gates, answers, n_lines):
    qs = check_questions(contract)
    by_id = {}
    dup = set()
    for a in answers.get("answers", []):
        qid = str(a.get("id", ""))
        if qid in by_id:
            dup.add(qid)
        by_id[qid] = a
    known = {q["id"] for q in qs}
    rows = []
    for q in qs:
        a = None if q["id"] in dup else by_id.get(q["id"])
        final, note = grade_answer(q, a, n_lines)
        if q["id"] in dup:
            note = "trả lời TRÙNG — coi là Không rõ"
        rows.append({"id": q["id"], "q": q["q"], "severity": q["severity"], "spec_line": q["spec_line"],
                     "raw_answer": (a or {}).get("answer"), "answer": final, "note": note,
                     "view": (a or {}).get("view"), "code_line": (a or {}).get("code_line"),
                     "reasoning": (a or {}).get("reasoning", "")})
    unknown = sorted(set(by_id) - known)
    if any(r["answer"] == "no" and r["severity"] == "block" for r in rows):
        verdict = "block"
    elif any(r["answer"] == "unclear" for r in rows):
        verdict = "needs_human"
    elif any(r["answer"] == "no" for r in rows):
        verdict = "comment-only"
    else:
        verdict = "pass"
    extra = [dict(f, scope="ngoài câu hỏi đã ký — KHÔNG đổi verdict") for f in answers.get("extra_findings", [])]
    return verdict, rows, unknown, extra


def render_md(part_id, verdict, rows, unknown, extra):
    mark = {"yes": "✅ Có", "no": "❌ Không", "unclear": "❓ Không rõ"}
    L = [f"# helix-cad-judge — {verdict}", "", f"- Part: **{part_id}** · verdict tính bằng `judge_score.py` "
         "từ câu trả lời — không phải lời agent tự kết luận.", "",
         "| Q | Câu hỏi (đã ký) | Mức | Trả lời | Chứng cứ | Ghi chú |", "|---|---|---|---|---|---|"]
    for r in rows:
        ev = " · ".join(x for x in (r["view"] or "", f"L{r['code_line']}" if r["code_line"] else "") if x)
        L.append(f"| {r['id']} | {r['q']} | {r['severity']} | {mark[r['answer']]} | {ev or '—'} | {r['note']} |")
    if unknown:
        L += ["", f"⚠️ Bỏ qua câu trả lời cho id không có trong hợp đồng: {', '.join(unknown)}"]
    if extra:
        L += ["", "## Phát hiện ngoài câu hỏi đã ký (CEO xem, không đổi verdict)"]
        L += [f"- {f.get('what', '?')} — {f.get('view', '')} L{f.get('code_line', '?')}: {f.get('evidence', '')}"
              for f in extra]
    L += ["", "## CEO (CORE)",
          "- `block` ⇒ (1) Re-run khối dựng kèm các câu ❌ · (2) Bỏ qua có lý do · (3) Dừng",
          "- `needs_human` ⇒ kỹ sư tự xem render cho từng câu ❓ rồi ghi kết quả vào `_pipeline_state.md`",
          "- Judge là LLM: đúng ~65–68 % trong CADCodeVerify. PASS ở đây KHÔNG thay chữ ký kỹ sư."]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic verdict from judge answers to signed questions.")
    ap.add_argument("--contract", required=True)
    ap.add_argument("--gates", required=True, help="cad_gates_report.json (must be verdict PASS)")
    ap.add_argument("--answers", required=True, help="judge_answers.json written by the judge agent")
    ap.add_argument("--model", required=True, help="model.py — code_line evidence is checked against it")
    ap.add_argument("--approved-hash", required=True)
    ap.add_argument("--out", default="judge_verdict")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    try:
        contract, gates, answers = _load(a.contract), _load(a.gates), _load(a.answers)
        with open(a.model, encoding="utf-8") as f:
            n_lines = len(f.read().splitlines())
        chash = check_preconditions(a.contract, gates, a.approved_hash)
        verdict, rows, unknown, extra = score(contract, gates, answers, n_lines)
    except Refused as e:
        print(f"[REFUSED] {e}", file=sys.stderr)
        return 3
    except (OSError, json.JSONDecodeError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    out = {"tool": "helix-cad-judge", "version": "2.0", "checked_at": datetime.now(timezone.utc).isoformat(),
           "part_id": contract.get("part_id"), "contract_sha256": chash, "verdict": verdict,
           "n_questions": len(rows), "n_no": sum(r["answer"] == "no" for r in rows),
           "n_unclear": sum(r["answer"] == "unclear" for r in rows),
           "n_downgraded": sum(bool(r["note"]) and r["raw_answer"] in ("yes", "no") for r in rows),
           "questions": rows, "ignored_answer_ids": unknown, "extra_findings": extra}
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(contract.get("part_id", "?"), verdict, rows, unknown, extra))
    if not a.quiet:
        print(f"=== helix-cad-judge: {verdict} === ({out['n_no']} không / {out['n_unclear']} không rõ / "
              f"{len(rows)} câu, {out['n_downgraded']} câu bị hạ vì thiếu chứng cứ)")
    return EXIT[verdict]


if __name__ == "__main__":
    sys.exit(main())
