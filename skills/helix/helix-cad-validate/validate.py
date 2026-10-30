#!/usr/bin/env python3
"""
helix-cad-validate / validate.py — Deterministic design-rule validator (Computational Sensor + Gate).

BƯỚC 1 of the harness-engineering validator (per mentor-harness-engineering-council DEBATE 2026-06-25):
the thin, deterministic, CPU-only gate for the DESIGN phase. NO LLM, NO network — 100% local,
air-gapped-safe (stdlib only). It reads a CAD extract (from helix-cad-ingest) + an optional mass-props
file (from helix-cad-bridge) and scores them PASS/FAIL against a versioned design_rules.json contract.

Harness principles encoded:
  - "Cơ chế, không phải prompt": rules are deterministic checks, not prompt text.
  - Gate khóa quyền sửa rào của chính nó: the contract is READ-ONLY here; its SHA-256 is recorded,
    and --approved-hash refuses to run on a contract that doesn't match the engineer-approved hash
    (stops an agent silently editing rules to turn the gate green).
  - Fail-safe: a missing/low-confidence value feeding a CRITICAL rule => FAIL (never silent SKIP).
  - PASS ≠ an toàn: PASS only means "đạt chuẩn tối thiểu". Kỹ sư định danh still signs the final gate.

Exit codes: 0 = PASS (all gating checks pass), 2 = FAIL (>=1 gating check failed),
            3 = usage/IO error. (Non-zero => CI/handoff gate stays CLOSED.)

Usage:
  python validate.py --extract part.cad_extract.json --rules design_rules.json [--mass-props mp.json]
                     [--out report] [--approved-hash <sha256>] [--quiet]
"""
import argparse
import csv
import hashlib
import io
import json
import os
import sys
from datetime import datetime, timezone

CONF_RANK = {"LOW": 0, "MED": 1, "HIGH": 2}

# collection-method provenance rank (taxonomy B, from helix-cad-ingest).
# A value's method must out-rank a rule's min_method to pass that gate.
METHOD_RANK = {
    "ocr": 0, "title-block": 1,
    "schedule-table": 2, "dim-override": 2,
    "dim-measured": 3, "geometry-counted": 3,
    "human-certified": 4,
}


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm(s):
    return str(s or "").strip().lower()


def _conf_ok(conf, min_conf):
    return CONF_RANK.get(str(conf or "LOW").upper(), 0) >= CONF_RANK.get(str(min_conf or "HIGH").upper(), 2)


def _method_ok(method, min_method):
    """True if the value's collection method out-ranks the rule's min_method.
    Fail-safe: unknown/missing method (e.g. an assumed default) ranks below all."""
    if not min_method:
        return True                       # rule does not gate on method
    return METHOD_RANK.get(str(method or ""), -1) >= METHOD_RANK.get(str(min_method), 4)


class Report:
    def __init__(self):
        self.checks = []

    def add(self, rule_id, status, severity, observed, expected, message, fix="", source=""):
        self.checks.append({
            "rule_id": rule_id, "status": status, "severity": severity,
            "observed": observed, "expected": expected, "message": message,
            "fix_hint": fix, "source": source,
        })

    @property
    def failed(self):
        return [c for c in self.checks if c["status"] == "FAIL"]

    @property
    def gating_failed(self):
        # any FAIL gates (critical + major). warnings/skips do not gate.
        return [c for c in self.failed]


def _thickness_rows(extract):
    """Collect (value_mm, confidence, method, source) thickness candidates from bom + dimensions."""
    rows = []
    for b in extract.get("bom", []) or []:
        t = b.get("thickness_mm")
        if t is not None:
            rows.append((float(t), "MED", "schedule-table", f"bom:{b.get('code') or b.get('item')}"))
    for d in extract.get("dimensions", []) or []:
        p = _norm(d.get("param"))
        if any(k in p for k in ("thickness", "độ dày", "do day", "dày", "tôn", "plate")):
            try:
                rows.append((float(d.get("value")), d.get("confidence", "LOW"),
                             d.get("method"), d.get("source") or f"dim:{d.get('param')}"))
            except (TypeError, ValueError):
                pass
    return rows


def _materials(extract):
    mats = []
    if extract.get("meta", {}).get("material"):
        mats.append((extract["meta"]["material"], "meta.material"))
    for b in extract.get("bom", []) or []:
        if b.get("material"):
            mats.append((b["material"], f"bom:{b.get('code') or b.get('item')}"))
    return mats


def _load_master_csv(path):
    """Authoritative parts master (from authoritative_bom.py masters/*.csv).
    Returns (by_code, name_to_codes) or None if unreadable. stdlib-only, LOCAL."""
    if not path or not os.path.isfile(path):
        return None
    try:
        with io.open(path, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError:
        return None
    if not rows or "code" not in (rows[0].keys()):
        return None
    by_code = {(_norm(r.get("code"))): r for r in rows if r.get("code")}
    name_to_codes = {}
    for r in rows:
        nm = _norm(r.get("name"))
        if nm:
            name_to_codes.setdefault(nm, set()).add(_norm(r.get("code")))
    return by_code, name_to_codes


def _all_text(extract):
    """All free text where notes / weld std / load class may live."""
    parts = list(extract.get("process_notes", []) or [])
    for d in extract.get("dimensions", []) or []:
        parts.append(str(d.get("note") or ""))
    for b in extract.get("blocks", []) or []:
        parts.append(json.dumps(b.get("attribs", {}), ensure_ascii=False))
    for b in extract.get("bom", []) or []:
        parts.append(str(b.get("name") or ""))
        parts.append(str(b.get("item") or ""))
    return "\n".join(parts).lower()


def run_checks(extract, rules, mass_props):
    r = Report()
    rs = rules.get("rules", {})

    # 0. Unresolved CONFLICT in the extract blocks (cad-ingest flagged dxf vs pdf disagreement)
    cb = rs.get("conflicts_block", {})
    if cb.get("enabled", True):
        conflicts = extract.get("conflicts", []) or []
        if conflicts:
            r.add("conflicts_block", "FAIL", cb.get("severity", "critical"),
                  f"{len(conflicts)} conflict(s)", "0 unresolved",
                  "Bản vẽ còn CONFLICT chưa giải (dxf vs pdf). Gate đóng tới khi kỹ sư giải quyết.",
                  fix="Giải quyết từng conflict trong cad_extract.conflicts[], re-ingest.",
                  source="extract.conflicts")
        else:
            r.add("conflicts_block", "PASS", cb.get("severity", "critical"),
                  "0", "0", "Không còn conflict chưa giải.")

    # 0c. BOM authoritative master — part code resolvable + not a stale title-block code.
    # Đóng "BOM=0": nguồn sự thật = parts_master CSV (kỹ sư ký), KHÔNG phải title-block DXF.
    bm = rs.get("bom_master")
    if bm and bm.get("enabled", True):
        sev = bm.get("severity", "critical")
        master = _load_master_csv(bm.get("master_csv"))
        meta = extract.get("meta", {}) or {}
        code = _norm(meta.get("code_in_dxf") or meta.get("part_id"))
        name = _norm(meta.get("name"))
        # bom_present: master phải có và không rỗng (fail-safe).
        if master is None:
            if bm.get("required", True):
                r.add("bom_present", "FAIL", sev, "(no master)", bm.get("master_csv", "parts_master.csv"),
                      "Thiếu/không đọc được parts_master authoritative — BOM=0, không thể chứng nhận.",
                      fix="Tạo masters/parts_master.<PRODUCT>.csv (authoritative_bom.py) rồi trỏ master_csv.",
                      source="bom_master.master_csv")
        else:
            by_code, name_to_codes = master
            r.add("bom_present", "PASS", sev, f"{len(by_code)} mã", "master non-empty",
                  "Có parts_master authoritative.", source=bm.get("master_csv"))
            roots = set(_norm(x) for x in bm.get("ignore_codes", []))
            if not code:
                r.add("bom_reconciled", "SKIP", sev, "(no code)", "code_in_dxf/part_id",
                      "Extract không có mã chi tiết để đối chiếu.")
            elif code in roots:
                r.add("bom_reconciled", "PASS", sev, code, "root/ignored", "Mã gốc cụm — bỏ qua đối chiếu.")
            elif code not in by_code:
                r.add("bom_reconciled", "FAIL", sev, code, "in master",
                      f"Mã '{code}' không có trong parts_master (part ma / mã sai).",
                      fix="Sửa mã theo master, hoặc bổ sung part vào master (kỹ sư ký).",
                      source="meta.code_in_dxf")
            elif name and name in name_to_codes and code not in name_to_codes[name]:
                owner = sorted(name_to_codes[name])
                r.add("bom_reconciled", "FAIL", sev, f"{code} = \"{meta.get('name')}\"",
                      f"\"{meta.get('name')}\" = {owner}",
                      f"STALE-CODE: tên '{meta.get('name')}' ở master thuộc mã {owner}, không phải {code} "
                      f"(mã khung tên copy-paste cũ).",
                      fix="Dùng mã master cho tên này; cập nhật title-block.", source="meta")
            else:
                r.add("bom_reconciled", "PASS", sev, code, "khớp master", "Mã+tên khớp parts_master.", source="meta")

    # 1. Material whitelist
    m = rs.get("materials")
    if m:
        allowed = [_norm(x) for x in m.get("allowed", [])]
        forbidden = [_norm(x) for x in m.get("forbidden", [])]
        sev = m.get("severity", "critical")
        mats = _materials(extract)
        if not mats and m.get("required", True):
            r.add("materials", "FAIL", sev, "(none)", f"one of {m.get('allowed')}",
                  "Không tìm thấy vật liệu trong extract — không thể chứng nhận.",
                  fix="Bổ sung material vào meta/BOM rồi re-ingest.", source="meta/bom")
        for val, src in mats:
            n = _norm(val)
            if any(fb and fb in n for fb in forbidden):
                r.add("materials", "FAIL", sev, val, f"NOT in {m.get('forbidden')}",
                      f"Vật liệu cấm: {val}.", fix="Đổi sang vật liệu whitelist.", source=src)
            elif allowed and not any(a in n for a in allowed):
                r.add("materials", "FAIL", sev, val, f"one of {m.get('allowed')}",
                      f"Vật liệu '{val}' ngoài whitelist.", fix="Đổi sang vật liệu cho phép.", source=src)
            else:
                r.add("materials", "PASS", sev, val, f"in {m.get('allowed')}",
                      f"Vật liệu '{val}' hợp lệ.", source=src)

    # 2. Plate thickness min (confidence-gated)
    pt = rs.get("plate_thickness_mm")
    if pt:
        sev = pt.get("severity", "critical")
        tmin = pt.get("min")
        min_conf = pt.get("min_confidence", rs.get("confidence_gate", {}).get("min_for_critical", "HIGH"))
        min_method = pt.get("min_method", rs.get("method_gate", {}).get("min_for_critical"))
        rows = _thickness_rows(extract)
        if not rows and pt.get("required", True):
            r.add("plate_thickness_mm", "FAIL", sev, "(none)", f">= {tmin} mm",
                  "Không có dữ liệu độ dày tấm — fail-safe.", source="bom/dim")
        for val, conf, method, src in rows:
            if tmin is not None and val < float(tmin):
                r.add("plate_thickness_mm", "FAIL", sev, f"{val} mm", f">= {tmin} mm",
                      f"Độ dày {val}mm < tối thiểu {tmin}mm.", fix=f"Tăng độ dày >= {tmin}mm.", source=src)
            elif not _conf_ok(conf, min_conf):
                r.add("plate_thickness_mm", "FAIL", sev, f"{val} mm (conf={conf})",
                      f"conf >= {min_conf}",
                      f"Độ dày {val}mm độ tin cậy {conf} < {min_conf} — chưa được chứng nhận cho rule tới hạn.",
                      fix="CEO/kỹ sư xác nhận giá trị (re-export vector PDF / certify).", source=src)
            elif not _method_ok(method, min_method):
                r.add("plate_thickness_mm", "FAIL", sev, f"{val} mm (method={method})",
                      f"method >= {min_method}",
                      f"Độ dày {val}mm lấy bằng '{method}' — dưới nguồn tối thiểu '{min_method}' cho rule tới hạn.",
                      fix="Đo lại từ hình học / kỹ sư chứng thực (human-certified).", source=src)
            else:
                r.add("plate_thickness_mm", "PASS", sev, f"{val} mm (conf={conf}, method={method})",
                      f">= {tmin} mm", f"Độ dày {val}mm đạt.", source=src)

    # 3. Mass max (prefer mass_props, then meta.mass_kg)
    ms = rs.get("mass_kg")
    if ms:
        sev = ms.get("severity", "major")
        mmax = ms.get("max")
        mass = None
        src = ""
        if mass_props and mass_props.get("mass_kg") is not None:
            mass, src = float(mass_props["mass_kg"]), "mass_props"
        elif extract.get("meta", {}).get("mass_kg") is not None:
            mass, src = float(extract["meta"]["mass_kg"]), "meta.mass_kg"
        if mass is None and ms.get("required", False):
            r.add("mass_kg", "FAIL", sev, "(none)", f"<= {mmax} kg",
                  "Không có khối lượng — fail-safe.", source="mass_props/meta")
        elif mass is not None:
            if mmax is not None and mass > float(mmax):
                r.add("mass_kg", "FAIL", sev, f"{mass} kg", f"<= {mmax} kg",
                      f"Khối lượng {mass}kg > giới hạn {mmax}kg.", fix="Giảm khối lượng / xét lại tải.", source=src)
            else:
                r.add("mass_kg", "PASS", sev, f"{mass} kg", f"<= {mmax} kg", "Khối lượng đạt.", source=src)

    # 4. Safety factor min
    sf = rs.get("safety_factor")
    if sf:
        sev = sf.get("severity", "critical")
        smin = sf.get("min")
        val = None
        if mass_props and mass_props.get("safety_factor") is not None:
            val = float(mass_props["safety_factor"])
        elif extract.get("meta", {}).get("safety_factor") is not None:
            val = float(extract["meta"]["safety_factor"])
        if val is None:
            (r.add("safety_factor", "FAIL", sev, "(none)", f">= {smin}",
                   "Thiếu hệ số an toàn cho rule tới hạn — fail-safe.",
                   fix="Bổ sung hệ số an toàn (FEA/tính tay) vào mass_props.", source="mass_props/meta")
             if sf.get("required", True) else
             r.add("safety_factor", "SKIP", sev, "(none)", f">= {smin}", "Không có dữ liệu (rule không bắt buộc)."))
        elif smin is not None and val < float(smin):
            r.add("safety_factor", "FAIL", sev, f"{val}", f">= {smin}",
                  f"Hệ số an toàn {val} < {smin}.", fix="Tăng tiết diện/giảm tải.", source="mass_props")
        else:
            r.add("safety_factor", "PASS", sev, f"{val}", f">= {smin}", "Hệ số an toàn đạt.", source="mass_props")

    # 5. Tolerance max (confidence-gated)
    tol = rs.get("tolerance_mm")
    if tol:
        sev = tol.get("severity", "major")
        tmax = tol.get("max")
        min_conf = tol.get("min_confidence", "MED")
        min_method = tol.get("min_method", rs.get("method_gate", {}).get("min_for_critical"))
        for t in extract.get("tolerances", []) or []:
            try:
                v = abs(float(t.get("value")))
            except (TypeError, ValueError):
                continue
            conf = t.get("confidence", "LOW")
            method = t.get("method")
            src = t.get("source") or f"tol:{t.get('rule')}"
            if tmax is not None and v > float(tmax):
                r.add("tolerance_mm", "FAIL", sev, f"±{v} mm", f"<= ±{tmax} mm",
                      f"Dung sai ±{v}mm vượt ±{tmax}mm.", fix="Siết dung sai hoặc xét chế tạo.", source=src)
            elif not _conf_ok(conf, min_conf):
                r.add("tolerance_mm", "FAIL", sev, f"±{v} mm (conf={conf})", f"conf >= {min_conf}",
                      f"Dung sai conf {conf} < {min_conf}.", fix="Xác nhận giá trị.", source=src)
            elif not _method_ok(method, min_method):
                r.add("tolerance_mm", "FAIL", sev, f"±{v} mm (method={method})", f"method >= {min_method}",
                      f"Dung sai lấy bằng '{method}' — dưới nguồn tối thiểu '{min_method}'.",
                      fix="Đo lại / kỹ sư chứng thực.", source=src)
            else:
                r.add("tolerance_mm", "PASS", sev, f"±{v} mm", f"<= ±{tmax} mm", "Dung sai đạt.", source=src)

    # 6. Mandatory components present
    mc = rs.get("mandatory_components")
    if mc:
        sev = mc.get("severity", "critical")
        text = _all_text(extract)
        for item in mc.get("items", []):
            toks = item if isinstance(item, list) else [item]
            if any(_norm(tok) in text for tok in toks):
                r.add("mandatory_components", "PASS", sev, "present", item,
                      f"Có thành phần bắt buộc: {item}.")
            else:
                r.add("mandatory_components", "FAIL", sev, "absent", item,
                      f"Thiếu thành phần bắt buộc: {item}.",
                      fix=f"Bổ sung '{item}' vào thiết kế/BOM.", source="bom/notes")

    # 7. Weld standard required
    ws = rs.get("weld_standard")
    if ws:
        sev = ws.get("severity", "critical")
        text = _all_text(extract)
        need = ws.get("required_any", [])
        if any(_norm(s) in text for s in need):
            r.add("weld_standard", "PASS", sev, "found", f"one of {need}", "Có viện dẫn chuẩn hàn.")
        else:
            r.add("weld_standard", "FAIL", sev, "(none)", f"one of {need}",
                  "Không thấy viện dẫn chuẩn hàn (ISO 9606-2 / AWS D1.2).",
                  fix="Ghi chuẩn hàn vào general notes / WPS.", source="notes")

    # 8. Load class required / forbidden
    lc = rs.get("load_class")
    if lc:
        sev = lc.get("severity", "critical")
        text = _all_text(extract)
        for fb in lc.get("forbidden", []):
            if _norm(fb) in text:
                r.add("load_class", "FAIL", sev, fb, f"NOT {fb}",
                      f"Phát hiện hạng tải CẤM: {fb}.", fix="Dùng đúng hạng tải doctrine.", source="notes")
        req = lc.get("required", [])
        if req:
            if any(_norm(s) in text for s in req):
                r.add("load_class", "PASS", sev, "found", f"one of {req}", "Hạng tải đúng doctrine.")
            else:
                r.add("load_class", "FAIL", sev, "(none)", f"one of {req}",
                      f"Không thấy hạng tải yêu cầu {req}.", fix=f"Khai báo hạng tải {req}.", source="notes")

    return r


def render_md(extract, rules, report, contract_hash, approved_ok, verdict):
    meta = extract.get("meta", {})
    rmeta = rules.get("meta", {})
    lines = []
    lines.append(f"# helix-cad-validate — {verdict}")
    lines.append("")
    lines.append(f"- Part: **{meta.get('part_id') or meta.get('name','?')}** · Product: {meta.get('product','?')} "
                 f"· Classification: {meta.get('classification','?')}")
    lines.append(f"- Contract: {rmeta.get('product','?')} rev {rmeta.get('rev','?')} "
                 f"v{rmeta.get('contract_version','?')} · sha256 `{contract_hash[:16]}…`")
    lines.append(f"- Contract approved-hash check: {'PASS' if approved_ok else 'NOT CHECKED / MISMATCH'}")
    fails = report.gating_failed
    lines.append(f"- Result: **{verdict}** — {len(fails)} FAIL / {len(report.checks)} checks")
    lines.append("")
    lines.append("| Rule | Status | Observed | Expected | Severity | Source |")
    lines.append("|---|---|---|---|---|---|")
    for c in report.checks:
        lines.append(f"| {c['rule_id']} | {c['status']} | {c['observed']} | {c['expected']} "
                     f"| {c['severity']} | {c['source']} |")
    if fails:
        lines.append("")
        lines.append("## ❌ FAIL detail (gate đóng — sửa rồi chạy lại)")
        for c in fails:
            lines.append(f"- **{c['rule_id']}** ({c['severity']}): {c['message']}")
            if c["fix_hint"]:
                lines.append(f"  - fix: {c['fix_hint']}")
    lines.append("")
    lines.append("## Cổng kỹ sư định danh (BẮT BUỘC — không AI)")
    lines.append("> PASS của validator = ĐẠT CHUẨN TỐI THIỂU, **KHÔNG** đồng nghĩa an toàn xuất xưởng.")
    lines.append("> Kết luận kết cấu/mỏi/FEA và phê duyệt cuối phải do kỹ sư định danh ký.")
    lines.append("")
    lines.append(f"- [ ] Kỹ sư định danh: ______________________  Ngày: __________")
    lines.append(f"- Engineer of record (contract): {rmeta.get('engineer_of_record','(chưa gán)')}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic design-rule validator (Computational Sensor + Gate).")
    ap.add_argument("--extract", required=True, help="cad_extract.json from helix-cad-ingest")
    ap.add_argument("--rules", required=True, help="design_rules.json contract")
    ap.add_argument("--mass-props", help="optional mass-props json from helix-cad-bridge")
    ap.add_argument("--out", default="cad_validate_report", help="output basename (.json + .md)")
    ap.add_argument("--approved-hash", help="engineer-approved sha256 of the contract; mismatch => FAIL")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args(argv)

    try:
        extract = _load(args.extract)
        rules = _load(args.rules)
        mass_props = _load(args.mass_props) if args.mass_props else None
    except (OSError, json.JSONDecodeError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3

    contract_hash = _sha256(args.rules)
    approved_ok = True
    report = run_checks(extract, rules, mass_props)

    # Gate khóa quyền sửa rào của chính nó: contract must match engineer-approved hash.
    if args.approved_hash:
        approved_ok = (contract_hash == args.approved_hash.strip().lower())
        if not approved_ok:
            report.add("contract_integrity", "FAIL", "critical", contract_hash[:16] + "…",
                       args.approved_hash[:16] + "…",
                       "design_rules.json KHÔNG khớp hash kỹ sư đã duyệt — có thể bị sửa trái phép.",
                       fix="Khôi phục contract đã duyệt; chỉ kỹ sư định danh được đổi luật.",
                       source=args.rules)

    verdict = "FAIL" if report.gating_failed else "PASS"
    out_json = {
        "tool": "helix-cad-validate",
        "version": "1.0",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "part_id": extract.get("meta", {}).get("part_id"),
        "product": extract.get("meta", {}).get("product"),
        "contract": {"product": rules.get("meta", {}).get("product"),
                     "rev": rules.get("meta", {}).get("rev"),
                     "contract_version": rules.get("meta", {}).get("contract_version"),
                     "sha256": contract_hash, "approved_hash_ok": approved_ok},
        "verdict": verdict,
        "n_checks": len(report.checks),
        "n_fail": len(report.gating_failed),
        "checks": report.checks,
        "gate": "OPEN (handoff/freeze allowed pending engineer sign-off)" if verdict == "PASS"
                else "CLOSED (handoff to forge-fabrication / ICD freeze BLOCKED)",
    }
    with open(args.out + ".json", "w", encoding="utf-8") as f:
        json.dump(out_json, f, ensure_ascii=False, indent=2)
    with open(args.out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(extract, rules, report, contract_hash, approved_ok, verdict))

    if not args.quiet:
        print(f"=== helix-cad-validate: {verdict} === "
              f"({out_json['n_fail']} FAIL / {out_json['n_checks']} checks)  gate={out_json['gate']}")
        for c in report.gating_failed:
            print(f"  FAIL [{c['severity']}] {c['rule_id']}: {c['message']}")

    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
