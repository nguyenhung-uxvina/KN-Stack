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
                      helix-cad-crosscheck crosscheck .json       (2D master vs 3D witness, with attribution)
                      helix-cad-crosscheck mutate .json           (L6 positive control of the crosscheck)

States: PASS · FAIL · ADVISORY (visible, never blocks) · NEEDS_EVIDENCE · NEEDS_RECOGNITION_REVIEW ·
        NEEDS_RULE_REVIEW · NEEDS_CONTEXT · CONTESTED · NEEDS_HUMAN_RELEASE · ABSTAINED.
Every state except PASS and ADVISORY blocks.

Subcommands
  collect      --part ID [--extract F] [--validate F] [--gates F] [--judge F] [--crosscheck F] [--mutate F]
               [--profile full|model|drawing|reconstruct]
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
            "drawing": ("extract", "validate"),
            # 3D built FROM a 2D drawing: the drawing is master, the model is checked against it, and a
            # crosscheck "0 lỗi" counts only with its positive control (planted faults caught + attributed right)
            "reconstruct": ("gates", "crosscheck", "mutate")}
KINDS = ("extract", "validate", "gates", "judge", "crosscheck", "mutate")
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


def _key(code):
    return re.sub(r"\s+", " ", (code or "").strip()).upper()


def _nname(s):
    """Name for comparison: case-folded, punctuation and spacing collapsed."""
    return re.sub(r"[\s\-–,.;:()]+", " ", (s or "").casefold()).strip()


def _nmat(s):
    return re.sub(r"\s+", " ", (s or "").casefold().replace("{", "").replace("}", "")).strip(" .")


CONT_RE = re.compile(r"(?i)t[oờ]\s*0?\d+\s*-\s*0?\d+")      # continuation sheet marker in a file name ("tờ 02-03")
QTY_RE = re.compile(r"(?i)số\s*lượng\s*:\s*(\d+)")
YCKT_MAT_RE = re.compile(r"(?i)vật\s*liệu\s*:\s*([^.;\n]+)")
CODE_LIKE = re.compile(r"(?i)\b\d{1,3}\.[a-z]{1,4}-?\d{1,3}(?:\.\d{2}){1,3}(?:\s*b[lk])?\b")
BL_SUFFIX = re.compile(r"(?i)\s*\bB[LK]\s*$")


def _sheet_of(path, ex):
    return str(ex.get("meta", {}).get("file_index") or os.path.basename(path))


def _tb(ex, field):
    """Title-block value (G1) when present — the fallback heuristics of older ingest are not used for G2a."""
    v = ((ex.get("meta", {}).get("title_block") or {}).get(field) or {}).get("value")
    return v if v else None


def _same_material(a, b):
    """Same material when one description's words are contained in the other's (measured: 'Thép SS400' vs
    'THÉP SS400 JIS G3101' is the same steel written with its standard)."""
    ta, tb = set(_nmat(a).split()), set(_nmat(b).split())
    return ta <= tb or tb <= ta


def _sheet_texts(ex):
    return " \n ".join(r.get("text", "") for r in ex.get("raw_text", []))


def set_check(extracts, code_case=None):
    """Cross-sheet claims for one drawing set. extracts: list of (path, extract).
    part_code_unique   same code on two different parts (continuation sheets excluded)         -> NEEDS_CONTEXT
    part_code_format   code written differently from the set's dominant form (case, spacing)    -> CONTESTED   (G2a)
    bom_code_matches_sheet  parts-list code with no sheet in the set                            -> NEEDS_CONTEXT (G2a)
    bom_name_matches_sheet  parts-list row name != title-block name of the sheet with that code -> CONTESTED   (G2a)
    material_consistent     title-block material != YCKT "Vật liệu:" on the same sheet, or
                            parts-list material != material of the referenced sheet             -> CONTESTED   (G2a)
    qty_matches_parent      "Số lượng: N" on a sheet not found among the parents' list quantities -> CONTESTED  (G2a)
    """
    tool, out = "audit_claims/G2a", []
    sheets = {}
    for path, ex in extracts:
        m = ex.get("meta", {})
        code = m.get("code_in_dxf") or m.get("part_id")
        has_tb = bool((m.get("title_block") or {}).get("found"))
        sheets[_sheet_of(path, ex)] = {"path": path, "ex": ex, "code": code, "key": _key(code),
                                       "name": _tb(ex, "name") if has_tb else m.get("name"),
                                       "material": _tb(ex, "material") if has_tb else m.get("material")}
    by_key, by_base = {}, {}
    for s, d in sheets.items():
        if d["key"]:
            by_key.setdefault(d["key"], []).append(s)
            by_base.setdefault(BL_SUFFIX.sub("", d["key"]), []).append(s)

    def lookup(rk):
        """Sheet(s) for a parts-list code; an assembly code may be drawn as '<code> BL' (bản vẽ lắp)."""
        return by_key.get(rk) or by_base.get(BL_SUFFIX.sub("", rk))

    # 1. duplicates (continuation sheets of one part are not duplicates)
    for k, ss in sorted(by_key.items()):
        if len(ss) < 2:
            continue
        names = {_nname(sheets[s]["name"]) for s in ss if sheets[s]["name"]}
        cont = len(names) <= 1 and any(CONT_RE.search(os.path.basename(sheets[s]["path"])) for s in ss)
        if cont:
            continue
        for s in ss:
            out.append(mk(tool, s, "part_code_unique", "NEEDS_CONTEXT",
                          f"Mã {k} xuất hiện trên {len(ss)} tờ: {', '.join(ss)}.", f"meta.code_in_dxf={k}",
                          observed=sheets[s]["code"], expected="mã duy nhất trong bộ", source=sheets[s]["path"]))

    # 2. code format. With a declared convention (project config, e.g. code_case="upper") flag what breaks it.
    #    Without one, a MIXED set is inconsistent as a whole: flag every sheet — measured: the majority form
    #    can be the wrong one (37/42 sheets lower-case), so "dominant form = right" flagged the correct sheets.
    def shape(c):
        return "upper" if c == c.upper() else ("lower" if c == c.lower() else "mixed")
    shapes = {s: shape(d["code"].strip()) for s, d in sheets.items() if d["code"]}
    counts = {k: list(shapes.values()).count(k) for k in set(shapes.values())}
    for s, sh in shapes.items():
        if code_case:
            bad, why = sh != code_case, f"quy ước dự án: {code_case}"
        else:
            bad, why = len(counts) > 1, "bộ dùng lẫn " + ", ".join(f"{k} {v} tờ" for k, v in sorted(counts.items()))
        if bad:
            out.append(mk(tool, s, "part_code_format", "CONTESTED",
                          f"Mã khung tên '{sheets[s]['code'].strip()}' ({sh}) — {why}.", "meta.title_block.code",
                          observed=sheets[s]["code"].strip(), expected=code_case or "một dạng thống nhất",
                          source=sheets[s]["path"]))

    # 3. parts-list rows vs referenced sheets
    parent_qty = {}     # code -> list of quantities, one per parent row
    for s, d in sheets.items():
        for i, r in enumerate(d["ex"].get("bom", [])):
            rk = _key(r.get("code"))
            if not rk or not CODE_LIKE.fullmatch(rk):      # standard / bought-in rows carry no part code
                continue
            group = bool(r.get("code_group"))              # "14.00; 14.01; 14.03": the row names the group
            if r.get("qty") and not group and str(r["qty"]).strip().isdigit():
                parent_qty.setdefault(BL_SUFFIX.sub("", rk), []).append(int(r["qty"]))
            loc = f"bom[{i}]"
            hit = lookup(rk)
            if not hit:
                out.append(mk(tool, s, "bom_code_matches_sheet", "NEEDS_CONTEXT",
                              f"Bảng kê ghi mã {rk} («{r.get('name')}») nhưng bộ không có tờ mang mã này.", loc,
                              observed=rk, expected="mã có tờ trong bộ", source=d["path"]))
                continue
            if group:   # measured false claim: the group's name was compared with the first code's sheet only
                continue
            child = sheets[hit[0]]
            if r.get("name") and child["name"] and _nname(r["name"]) != _nname(child["name"]):
                out.append(mk(tool, s, "bom_name_matches_sheet", "CONTESTED",
                              f"Bảng kê: {rk} là «{r['name']}», nhưng tờ {hit[0]} mang mã này tên «{child['name']}».",
                              loc, observed=r["name"], expected=child["name"], source=d["path"]))
            if r.get("material") and child["material"] and not _same_material(r["material"], child["material"]):
                out.append(mk(tool, s, "material_consistent", "CONTESTED",
                              f"Bảng kê: vật liệu của {rk} là «{r['material']}», khung tên tờ {hit[0]} ghi «{child['material']}».",
                              loc, observed=r["material"], expected=child["material"], source=d["path"]))

    # 4. per sheet: title-block material vs YCKT; stated quantity vs parents (YCKT is often one MTEXT, so read
    #    all sheet text — measured: process_notes kept only lines starting with '-')
    for s, d in sheets.items():
        notes = _sheet_texts(d["ex"])
        mm = YCKT_MAT_RE.search(notes)
        if mm and d["material"] and not _same_material(mm.group(1), d["material"]):
            out.append(mk(tool, s, "material_consistent", "CONTESTED",
                          f"Khung tên ghi vật liệu «{d['material']}», YCKT ghi «{mm.group(1).strip()}».",
                          "meta.material vs process_notes", observed=mm.group(1).strip(), expected=d["material"],
                          source=d["path"]))
        mq = QTY_RE.search(notes)
        pk = BL_SUFFIX.sub("", d["key"]) if d["key"] else None
        # consistent when the sheet's total equals the SUM over parents (a part used in two assemblies, measured:
        # 1 + 1 = YCKT 2) or equals one parent row
        if mq and pk in parent_qty and int(mq.group(1)) not in set(parent_qty[pk]) | {sum(parent_qty[pk])}:
            out.append(mk(tool, s, "qty_matches_parent", "CONTESTED",
                          f"YCKT ghi số lượng {mq.group(1)}, bảng kê cụm cha ghi {parent_qty[pk]} (tổng {sum(parent_qty[pk])}).",
                          "raw_text 'Số lượng:'", observed=mq.group(1), expected=parent_qty[pk], source=d["path"]))
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


# ── 2D master vs 3D witness: helix-cad-crosscheck ──────────────────────────────────────────────────────

def from_crosscheck(rep, part, src):
    """CONTESTED = the drawing contradicts itself (another view arbitrates) -> a 2D fix proposal for a human;
    FAIL = the model does not follow the drawing. Both block."""
    out, tool, ver = [], "helix-cad-crosscheck", str(rep.get("version", ""))
    for i, c in enumerate(rep.get("checks", [])):
        st = {"PASS": "PASS", "FAIL": "FAIL", "CONTESTED": "CONTESTED", "INFO": "ADVISORY"}.get(c.get("status"),
                                                                                              "ADVISORY")
        att = c.get("attribution", "")
        msg = c.get("message", "") + (f" [quy cho: {att}]" if att else "")
        loc = f'{c.get("locator") or ""} checks[{i}]'.strip()
        out.append(mk(tool, part, c.get("rule_id", "?"), st, msg, loc, c.get("observed", ""),
                      c.get("expected", ""), c.get("severity", "") or att, src, ver))
    return out


def from_mutate(r, part, src):
    tool = "helix-cad-crosscheck/mutate"
    if r.get("baseline_verdict") not in ("PASS", "PASS_GEOMETRY"):
        return [mk(tool, part, "L6_positive_control", "NEEDS_EVIDENCE",
                   "Đối chứng dương chưa chạy được: bộ gốc chưa PASS.", "baseline", r.get("baseline_verdict"), "PASS",
                   source=src)]
    tot, caught, right = r.get("total", 0), r.get("caught", 0), r.get("attribution_right", 0)
    if not tot:
        return [mk(tool, part, "L6_positive_control", "NEEDS_EVIDENCE", "Không cấy được lỗi nào.", "mutants",
                   "0", "≥ 1", source=src)]
    out = [mk(tool, part, "L6_positive_control", "PASS" if caught == tot and right == tot else "FAIL",
              "Lỗi cấy bị bắt và quy đúng bên (bản vẽ/mô hình)", "mutants",
              f"bắt {caught}/{tot}, quy đúng {right}/{tot}", f"{tot}/{tot}", source=src)]
    for m in r.get("mutants", []):
        if m.get("caught") is False:
            out.append(mk(tool, part, "L6_escaped", "FAIL", f"Lỗi cấy {m['name']} lọt qua bộ kiểm",
                          f"mutant {m['name']}", "không bắt", "bắt", source=src))
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
    conv = {"extract": from_extract, "validate": from_validate, "gates": from_gates, "judge": from_judge,
            "crosscheck": from_crosscheck, "mutate": from_mutate}
    for kind in KINDS:
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
    for k in KINDS:
        c.add_argument(f"--{k}")
    c.add_argument("--profile", choices=sorted(PROFILES), default="full")
    c.add_argument("--out", required=True)
    s = sub.add_parser("set-check")
    s.add_argument("--extracts", nargs="+", required=True)
    s.add_argument("--code-case", choices=("upper", "lower"), help="project convention for part codes (optional)")
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
            rec = collect(a.part, {k: getattr(a, k) for k in KINDS}, a.profile)
            json.dump(rec, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            open(a.out + ".md", "w", encoding="utf-8").write(render_md(rec))
            print(f"=== audit_claims: {rec['machine_verdict']} === ({rec['n_blocking']} chặn / {rec['n_claims']} claim)")
            return 0 if rec["machine_verdict"] == "READY_FOR_HUMAN_RELEASE" else 2
        if a.cmd == "set-check":
            claims = set_check([(p, _load(p)) for p in a.extracts], a.code_case)
            rec = {"tool": "audit_claims", "version": VERSION, "part_id": "SET", "profile": "set",
                   "machine_verdict": "BLOCKED" if claims else "READY_FOR_HUMAN_RELEASE",
                   "n_claims": len(claims), "n_blocking": len(claims),
                   "by_status": {st: sum(c["status"] == st for c in claims) for st in STATES
                                 if any(c["status"] == st for c in claims)}, "claims": claims}
            json.dump(rec, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            open(a.out + ".md", "w", encoding="utf-8").write(render_md(rec))
            print(f"=== set-check: {len(claims)} claim chặn ===")
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
