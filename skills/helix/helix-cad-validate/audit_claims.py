#!/usr/bin/env python3
"""
helix-cad-validate / audit_claims.py — one claim record for every HELIX drawing/model check (G0 of the
P–C–C audit roadmap, Chen & Cheng 2026, IJCIM 10.1080/0951192X.2026.2714117).

Stdlib only, local, no LLM. It does not re-check anything: it converts the reports HELIX already writes into
typed claims with a deterministic claim_id, maps "not enough evidence" to explicit safe states instead of
PASS/FAIL, and computes ONE machine verdict. The machine never releases: its best verdict is
READY_FOR_HUMAN_RELEASE; RELEASED exists only in a release record a named human signs.

Inputs (any subset):  helix-cad-ingest  <part>.cad_extract.json   (Perception)
                      helix-cad-validate validate report .json    (Cognition, data rules)
                      helix-cad-gates    cad_gates_report .json   (Cognition, geometry)
                      helix-cad-judge    judge_verdict .json      (LLM, advisory / needs-human only)

States: PASS · FAIL · ADVISORY (visible, never blocks) · NEEDS_EVIDENCE · NEEDS_RECOGNITION_REVIEW ·
        NEEDS_RULE_REVIEW · NEEDS_CONTEXT · CONTESTED · NEEDS_HUMAN_RELEASE · ABSTAINED.
Every state except PASS and ADVISORY blocks.

Subcommands
  collect      --part ID [--extract F] [--validate F] [--gates F] [--judge F] [--profile full|model|drawing]
               --out PREFIX          -> PREFIX.json + PREFIX.md ; exit 0 READY_FOR_HUMAN_RELEASE · 2 BLOCKED · 3 IO
  set-check    --extracts F [F ...] --out PREFIX   -> cross-sheet claims (duplicate part codes)
  check-report --claims F --report F.md            -> exit 2 if a finding line cites no existing claim_id
  spec         --spec spec.md                      -> exit 2 if unresolved '?' or an unanswered question section
  release      --claims F --signer "Name" --note "..." --out F
               -> writes a release record ONLY if the claims are READY; the signer is a person, typed by that person
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

VERSION = "1.0"
STATES = ("PASS", "FAIL", "ADVISORY", "NEEDS_EVIDENCE", "NEEDS_RECOGNITION_REVIEW", "NEEDS_RULE_REVIEW",
          "NEEDS_CONTEXT", "CONTESTED", "NEEDS_HUMAN_RELEASE", "ABSTAINED")
NON_BLOCKING = {"PASS", "ADVISORY"}
PROFILES = {"full": ("extract", "validate", "gates", "judge"), "model": ("gates", "judge"),
            "drawing": ("extract", "validate")}
ID_RE = re.compile(r"\[(C-[0-9a-f]{10})\]")


def claim_id(tool, part, rule, locator):
    return "C-" + hashlib.sha1(f"{tool}|{part}|{rule}|{locator}".encode("utf-8")).hexdigest()[:10]


def mk(tool, part, rule, status, message, locator="", observed="", expected="", severity="", source="",
       tool_version=""):
    assert status in STATES, status
    return {"claim_id": claim_id(tool, part, rule, locator), "part_id": part, "tool": tool,
            "tool_version": tool_version, "rule_id": rule, "locator": locator, "observed": str(observed),
            "expected": str(expected), "severity": severity, "status": status, "message": message,
            "source": source}


def _load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ── Perception: helix-cad-ingest extract ─────────────────────────────────────────────────────────────────

def from_extract(ex, part, src):
    out, tool = [], "helix-cad-ingest"
    ver = str(ex.get("meta", {}).get("tool", ""))
    for i, c in enumerate(ex.get("conflicts", [])):
        t = c.get("type", "?")
        if t == "BREAK-VIEW":   # ingest already resolves this by rule (dimension text wins over shortened geometry)
            out.append(mk(tool, part, "break_view", "ADVISORY", c.get("detail", ""), f"conflicts[{i}]",
                          source=src, tool_version=ver))
        else:
            out.append(mk(tool, part, f"conflict_{t}", "CONTESTED", c.get("detail", ""), f"conflicts[{i}]",
                          source=src, tool_version=ver))
    for i, m in enumerate(ex.get("missing", [])):
        if "KHÔNG tin cậy" in m or "copy-paste" in m:
            st, rule = "NEEDS_CONTEXT", "title_block_code_untrusted"
        elif "ARC" in m or "OCR" in m:
            st, rule = "NEEDS_RECOGNITION_REVIEW", "unrecognised_geometry"
        else:
            st, rule = "NEEDS_EVIDENCE", "missing"
        out.append(mk(tool, part, rule, st, m, f"missing[{i}]", source=src, tool_version=ver))
    if not ex.get("meta", {}).get("material"):
        out.append(mk(tool, part, "material_present", "NEEDS_EVIDENCE", "Bản vẽ không ghi vật liệu.",
                      "meta.material", observed="(none)", expected="vật liệu ghi trên khung tên / YCKT",
                      source=src, tool_version=ver))
    d_values = [d.get("value") for d in ex.get("dimensions", []) if d.get("source_tag") == "D"]
    for i, h in enumerate(ex.get("holes", [])):
        if h.get("source_tag") != "D" and not any(
                isinstance(v, (int, float)) and abs(v - h.get("dia", -1)) <= 0.05 for v in d_values):
            out.append(mk(tool, part, "hole_dia_undimensioned", "NEEDS_EVIDENCE",
                          f"Lỗ Ø{h.get('dia')} ×{h.get('count', 1)} chỉ đo được từ hình học, bản vẽ không ghi kích thước.",
                          f"holes[{i}]", observed=f"Ø{h.get('dia')} (G)", expected="kích thước ghi (D)",
                          source=src, tool_version=ver))
    return out


def set_check(extracts):
    """extracts: list of (path, extract). Duplicate part codes across different sheets -> NEEDS_CONTEXT."""
    seen = {}
    for path, ex in extracts:
        m = ex.get("meta", {})
        code = m.get("code_in_dxf") or m.get("part_id")
        if code:
            seen.setdefault(code, []).append((m.get("file_index") or os.path.basename(path), path))
    out = []
    for code, sheets in sorted(seen.items()):
        if len({s for s, _ in sheets}) > 1:
            names = ", ".join(s for s, _ in sheets)
            for sheet, path in sheets:
                out.append(mk("helix-cad-ingest", str(sheet), "part_code_unique", "NEEDS_CONTEXT",
                              f"Mã {code} xuất hiện trên {len(sheets)} tờ: {names}.", f"meta.code_in_dxf={code}",
                              observed=code, expected="mã duy nhất trong bộ", source=path))
    return out


# ── Cognition: validate + gates ──────────────────────────────────────────────────────────────────────────

def from_validate(rep, part, src):
    out, tool, ver = [], "helix-cad-validate", str(rep.get("version", ""))
    for i, c in enumerate(rep.get("checks", [])):
        s = c.get("status")
        if s == "FAIL":
            obs = str(c.get("observed", ""))
            if obs == "(none)":
                st = "NEEDS_EVIDENCE"
            elif "conf=" in obs or "uncertified" in str(c.get("message", "")).lower():
                st = "NEEDS_RECOGNITION_REVIEW"
            else:
                st = "FAIL"
        elif s == "PASS":
            st = "PASS"
        elif s == "SKIP":
            st = "NEEDS_EVIDENCE"
        else:
            st = "ADVISORY"
        out.append(mk(tool, part, c.get("rule_id", "?"), st, c.get("message", ""), f"checks[{i}]",
                      c.get("observed", ""), c.get("expected", ""), c.get("severity", ""),
                      c.get("source", "") or src, ver))
    return out


def from_gates(rep, part, src):
    out, tool, ver = [], "helix-cad-gates", f'{rep.get("version", "")}/{rep.get("mode", "")}'
    for i, c in enumerate(rep.get("checks", [])):
        st = {"PASS": "PASS", "FAIL": "FAIL", "SKIP": "NEEDS_EVIDENCE", "INFO": "ADVISORY"}.get(c.get("status"), "ADVISORY")
        out.append(mk(tool, part, c.get("rule_id", "?"), st, c.get("message", ""), f"checks[{i}]",
                      c.get("observed", ""), c.get("expected", ""), c.get("severity", ""),
                      c.get("source", "") or src, ver))
    return out


# ── LLM: judge (never PASS on its own authority beyond its signed questions; never blocks via extras) ────

def from_judge(v, part, src):
    out, tool, ver = [], "helix-cad-judge", str(v.get("version", ""))
    for q in v.get("questions", []):
        a, sev = q.get("answer"), q.get("severity")
        if a == "yes":
            st = "PASS"
        elif a == "no":
            st = "FAIL" if sev == "block" else "ADVISORY"
        else:
            st = "NEEDS_HUMAN_RELEASE"
        ev = " · ".join(x for x in (q.get("view") or "", f"L{q['code_line']}" if q.get("code_line") else "") if x)
        out.append(mk(tool, part, q.get("id", "?"), st, q.get("q", ""), f"question {q.get('id')} {ev}".strip(),
                      a, "yes", sev, src, ver))
    for i, f in enumerate(v.get("extra_findings", [])):
        out.append(mk(tool, part, "extra_finding", "ADVISORY", f.get("what", ""), f"extra_findings[{i}]",
                      f.get("evidence", ""), "", "comment", src, ver))
    return out


# ── aggregate ───────────────────────────────────────────────────────────────────────────────────────────

def collect(part, inputs, profile):
    claims = []
    conv = {"extract": from_extract, "validate": from_validate, "gates": from_gates, "judge": from_judge}
    for kind in ("extract", "validate", "gates", "judge"):
        if inputs.get(kind):
            claims += conv[kind](_load(inputs[kind]), part, inputs[kind])
    for kind in PROFILES[profile]:
        if not inputs.get(kind):
            claims.append(mk("audit_claims", part, f"required_input_{kind}", "ABSTAINED",
                             f"Hồ sơ '{profile}' bắt buộc có báo cáo {kind} nhưng không được cung cấp.",
                             f"--{kind}", expected="có báo cáo"))
    ids = [c["claim_id"] for c in claims]
    dup = {i for i in ids if ids.count(i) > 1}
    for c in claims:   # identical tool/rule/locator twice = two different observations; keep both, mark contested
        if c["claim_id"] in dup and c["status"] in NON_BLOCKING:
            c["status"] = "CONTESTED"
    blocking = [c for c in claims if c["status"] not in NON_BLOCKING]
    verdict = "BLOCKED" if blocking else "READY_FOR_HUMAN_RELEASE"
    counts = {s: sum(c["status"] == s for c in claims) for s in STATES if any(c["status"] == s for c in claims)}
    return {"tool": "audit_claims", "version": VERSION, "created_at": datetime.now(timezone.utc).isoformat(),
            "part_id": part, "profile": profile, "inputs": {k: v for k, v in inputs.items() if v},
            "machine_verdict": verdict, "n_claims": len(claims), "n_blocking": len(blocking),
            "by_status": counts, "claims": claims}


def render_md(rec):
    L = [f"# Audit claims — {rec['part_id']} — {rec['machine_verdict']}", "",
         f"- Hồ sơ: `{rec['profile']}` · {rec['n_claims']} claim · {rec['n_blocking']} chặn · "
         + " · ".join(f"{k} {v}" for k, v in rec["by_status"].items()),
         "- Máy không phát hành. READY_FOR_HUMAN_RELEASE chỉ nghĩa là không còn claim chặn; người ký mới phát hành.", ""]
    blocking = [c for c in rec["claims"] if c["status"] not in NON_BLOCKING]
    adv = [c for c in rec["claims"] if c["status"] == "ADVISORY"]
    if blocking:
        L += ["## Claim chặn", "", "| Claim | Trạng thái | Công cụ · luật | Vị trí | Nội dung |", "|---|---|---|---|---|"]
        L += [f"| [{c['claim_id']}] | {c['status']} | {c['tool']} · {c['rule_id']} | {c['locator']} | "
              f"{c['message'].replace('|', '/')} |" for c in blocking]
        L.append("")
    if adv:
        L += ["## Ghi nhận (không chặn)", ""]
        L += [f"- [{c['claim_id']}] {c['tool']} · {c['rule_id']}: {c['message']}" for c in adv]
        L.append("")
    npass = sum(c["status"] == "PASS" for c in rec["claims"])
    L += [f"_{npass} claim PASS không liệt kê; xem tệp .json._"]
    return "\n".join(L)


def check_report(rec, text):
    """Every finding line (bullet or table body row) must cite an existing claim_id."""
    known = {c["claim_id"] for c in rec["claims"]}
    bad = []
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        is_row = s.startswith("|") and not re.fullmatch(r"\|[\s:|-]+\|?", s)
        is_bullet = s.startswith(("- ", "* "))
        if not (is_row or is_bullet):
            continue
        if is_row and n > 1 and re.search(r"(?i)\bclaim\b", s) and not ID_RE.search(s):
            continue   # table header row
        ids = ID_RE.findall(s)
        if not ids:
            if is_bullet and (s.startswith("- Hồ sơ") or s.startswith("- Máy không phát hành")):
                continue
            bad.append((n, "không trích claim_id", s[:100]))
        else:
            for i in ids:
                if i not in known:
                    bad.append((n, f"claim_id {i} không có trong bản ghi", s[:100]))
    return bad


SPEC_Q_HEAD = re.compile(r"^#{1,6}\s*Câu hỏi(?! đã được CEO trả lời)", re.I)


def check_spec(text):
    """Unresolved markers that must be rewritten as statements before any build agent starts."""
    bad = []
    for n, line in enumerate(text.splitlines(), 1):
        if "**?**" in line or re.search(r"\|\s*\?\s*\|", line):
            bad.append((n, "còn nhãn '?' chưa thành quyết định", line.strip()[:110]))
        if SPEC_Q_HEAD.match(line.strip()):
            bad.append((n, "còn mục câu hỏi chưa trả lời", line.strip()[:110]))
        if re.match(r"^#{1,6}\s*Câu hỏi đã được CEO trả lời", line.strip()):
            bad.append((n, "câu hỏi đã trả lời nhưng chưa viết lại thành khẳng định (agent chỉ đọc spec)",
                        line.strip()[:110]))
    return bad


def release(rec, signer, note):
    if rec.get("machine_verdict") != "READY_FOR_HUMAN_RELEASE":
        raise ValueError(f"Không phát hành: machine_verdict = {rec.get('machine_verdict')} "
                         f"({rec.get('n_blocking')} claim chặn).")
    if not signer or not signer.strip():
        raise ValueError("Thiếu người ký (--signer).")
    body = json.dumps(rec["claims"], ensure_ascii=False, sort_keys=True).encode("utf-8")
    return {"tool": "audit_claims", "version": VERSION, "part_id": rec["part_id"], "status": "RELEASED",
            "signer": signer.strip(), "note": note or "", "signed_at": datetime.now(timezone.utc).isoformat(),
            "claims_sha256": hashlib.sha256(body).hexdigest(), "n_claims": rec["n_claims"]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="HELIX audit claim records (P–C–C G0).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("collect")
    c.add_argument("--part", required=True)
    for k in ("extract", "validate", "gates", "judge"):
        c.add_argument(f"--{k}")
    c.add_argument("--profile", choices=sorted(PROFILES), default="full")
    c.add_argument("--out", required=True)
    s = sub.add_parser("set-check")
    s.add_argument("--extracts", nargs="+", required=True)
    s.add_argument("--out", required=True)
    r = sub.add_parser("check-report")
    r.add_argument("--claims", required=True)
    r.add_argument("--report", required=True)
    sp = sub.add_parser("spec")
    sp.add_argument("--spec", required=True)
    rl = sub.add_parser("release")
    rl.add_argument("--claims", required=True)
    rl.add_argument("--signer", required=True)
    rl.add_argument("--note", default="")
    rl.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    try:
        if a.cmd == "collect":
            rec = collect(a.part, {k: getattr(a, k) for k in ("extract", "validate", "gates", "judge")}, a.profile)
            json.dump(rec, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            open(a.out + ".md", "w", encoding="utf-8").write(render_md(rec))
            print(f"=== audit_claims: {rec['machine_verdict']} === ({rec['n_blocking']} chặn / {rec['n_claims']} claim)")
            return 0 if rec["machine_verdict"] == "READY_FOR_HUMAN_RELEASE" else 2
        if a.cmd == "set-check":
            claims = set_check([(p, _load(p)) for p in a.extracts])
            rec = {"tool": "audit_claims", "version": VERSION, "part_id": "SET", "profile": "set",
                   "machine_verdict": "BLOCKED" if claims else "READY_FOR_HUMAN_RELEASE",
                   "n_claims": len(claims), "n_blocking": len(claims),
                   "by_status": {"NEEDS_CONTEXT": len(claims)} if claims else {}, "claims": claims}
            json.dump(rec, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            open(a.out + ".md", "w", encoding="utf-8").write(render_md(rec))
            print(f"=== set-check: {len(claims)} claim NEEDS_CONTEXT ===")
            return 2 if claims else 0
        if a.cmd == "check-report":
            bad = check_report(_load(a.claims), open(a.report, encoding="utf-8").read())
            for n, why, s_ in bad:
                print(f"  L{n}: {why}: {s_}")
            print(f"=== check-report: {'DRIFT' if bad else 'OK'} ({len(bad)}) ===")
            return 2 if bad else 0
        if a.cmd == "spec":
            bad = check_spec(open(a.spec, encoding="utf-8").read())
            for n, why, s_ in bad:
                print(f"  L{n}: {why}: {s_}")
            print(f"=== spec: {'BLOCKED' if bad else 'OK'} ({len(bad)}) ===")
            return 2 if bad else 0
        if a.cmd == "release":
            rec = release(_load(a.claims), a.signer, a.note)
            json.dump(rec, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print(f"=== release record written for {rec['part_id']} by {rec['signer']} ===")
            return 0
    except ValueError as e:
        print(f"[REFUSED] {e}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    return 3


if __name__ == "__main__":
    sys.exit(main())
