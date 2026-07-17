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

# Densities kg/m^3 for bottom-up mass reconciliation. Substring match on material name
# (same style as _materials); extend via the contract's mass_reconciliation.densities_kg_m3.
_DENSITY = {
    "5083": 2660, "5086": 2660, "5754": 2660, "5052": 2680,
    "6061": 2700, "6082": 2700, "6005": 2700, "6063": 2700,
    "nhôm": 2700, "nhom": 2700, "aluminum": 2700, "aluminium": 2700, "al ": 2700,
    "ss400": 7850, "s235": 7850, "s355": 7850, "ct3": 7850,
    "thép": 7850, "thep": 7850, "mild steel": 7850, "steel": 7850,
    "316": 8000, "304": 8000, "inox": 8000, "stainless": 8000,
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
    """Collect (value_mm, confidence, source) thickness candidates from bom + dimensions."""
    rows = []
    for b in extract.get("bom", []) or []:
        t = b.get("thickness_mm")
        if t is not None:
            rows.append((float(t), "MED", f"bom:{b.get('code') or b.get('item')}"))
    for d in extract.get("dimensions", []) or []:
        p = _norm(d.get("param"))
        if any(k in p for k in ("thickness", "độ dày", "do day", "dày", "tôn", "plate")):
            try:
                rows.append((float(d.get("value")), d.get("confidence", "LOW"),
                             d.get("source") or f"dim:{d.get('param')}"))
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


def _density_for(material, table):
    """Density (kg/m^3) by substring match on material name; None if unknown."""
    n = _norm(material)
    if not n:
        return None
    for key, rho in table.items():
        if key in n:
            return rho
    return None


def _bottomup_mass(extract, mass_props, densities):
    """Bottom-up mass for reconciliation. Returns (mass_kg|None, source, complete:bool, detail).

    Priority: explicit mass_props.bottom_up_kg (computed upstream by helix-cad-bridge / aggregate)
    → else compute from BOM rows that carry area_m2 + thickness_mm + a known material density.
    `complete` is False if any BOM row is missing area/thickness/density (partial sum ≠ trustworthy
    total) so the caller can fail-safe. validate.py never invents plate areas the extract lacks."""
    if mass_props and mass_props.get("bottom_up_kg") is not None:
        try:
            return float(mass_props["bottom_up_kg"]), "mass_props.bottom_up_kg", True, "provided"
        except (TypeError, ValueError):
            return None, "mass_props.bottom_up_kg", False, "unpar. value"
    bom = extract.get("bom", []) or []
    if not bom:
        return None, "bom", False, "no BOM rows and no mass_props.bottom_up_kg"
    total, used, missing = 0.0, 0, []
    for b in bom:
        area, th = b.get("area_m2"), b.get("thickness_mm")
        rho = _density_for(b.get("material"), densities)
        qty = b.get("qty") or 1
        tag = b.get("code") or b.get("item") or b.get("name") or "?"
        if area is None or th is None or rho is None:
            missing.append(tag)
            continue
        try:
            total += float(qty) * float(area) * (float(th) / 1000.0) * rho
            used += 1
        except (TypeError, ValueError):
            missing.append(tag)
    complete = used > 0 and not missing
    detail = f"{used} part(s) summed" + (f"; incomplete: {missing}" if missing else "")
    return (total if used > 0 else None), "bom(area×thk×ρ)", complete, detail


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
        rows = _thickness_rows(extract)
        if not rows and pt.get("required", True):
            r.add("plate_thickness_mm", "FAIL", sev, "(none)", f">= {tmin} mm",
                  "Không có dữ liệu độ dày tấm — fail-safe.", source="bom/dim")
        for val, conf, src in rows:
            if tmin is not None and val < float(tmin):
                r.add("plate_thickness_mm", "FAIL", sev, f"{val} mm", f">= {tmin} mm",
                      f"Độ dày {val}mm < tối thiểu {tmin}mm.", fix=f"Tăng độ dày >= {tmin}mm.", source=src)
            elif not _conf_ok(conf, min_conf):
                r.add("plate_thickness_mm", "FAIL", sev, f"{val} mm (conf={conf})",
                      f"conf >= {min_conf}",
                      f"Độ dày {val}mm độ tin cậy {conf} < {min_conf} — chưa được chứng nhận cho rule tới hạn.",
                      fix="CEO/kỹ sư xác nhận giá trị (re-export vector PDF / certify).", source=src)
            else:
                r.add("plate_thickness_mm", "PASS", sev, f"{val} mm (conf={conf})", f">= {tmin} mm",
                      f"Độ dày {val}mm đạt.", source=src)

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

    # 3b. Mass reconciliation — bottom-up Σ mass vs a reference (lightship) estimate, within tolerance.
    # The physics Sanity-Check for boats: a bottom-up sum (plates+weld+outfit) that drifts from the
    # naval-architect lightship estimate flags a mis-extraction / missing part / wrong material.
    # Deterministic: compares two numbers with a % tolerance. Default ±5% assembly, ±3% critical part.
    mr = rs.get("mass_reconciliation")
    if mr:
        sev = mr.get("severity", "critical")
        ref = mr.get("reference_kg")
        scope = _norm(mr.get("scope", "assembly"))
        tol_pct = mr.get("part_tolerance_pct", 3.0) if scope == "part" else mr.get("tolerance_pct", 5.0)
        densities = dict(_DENSITY)
        densities.update(mr.get("densities_kg_m3", {}) or {})
        bu, src, complete, detail = _bottomup_mass(extract, mass_props, densities)
        required = mr.get("required", True)
        if ref is None:
            r.add("mass_reconciliation", "FAIL" if required else "SKIP", sev,
                  "(no reference_kg)", "reference_kg in contract",
                  "Thiếu khối lượng tham chiếu (lightship) trong contract — không thể đối chiếu.",
                  fix="Kỹ sư định danh khai reference_kg (ước tính lightship/naval-architect).",
                  source="contract.mass_reconciliation")
        elif bu is None:
            r.add("mass_reconciliation", "FAIL" if required else "SKIP", sev,
                  "(no bottom-up)", f"{ref} kg ±{tol_pct}%",
                  "Không có khối lượng bottom-up (mass_props.bottom_up_kg hoặc BOM có area_m2) — fail-safe."
                  if required else "Không có dữ liệu bottom-up (rule không bắt buộc).",
                  fix="Cấp mass_props.bottom_up_kg (helix-cad-bridge) hoặc BOM kèm area_m2+material+thickness.",
                  source="mass_props/bom")
        elif not complete and mr.get("require_complete", True):
            r.add("mass_reconciliation", "FAIL", sev, f"{bu:.1f} kg ({detail})", "bottom-up ĐỦ part",
                  f"Bottom-up chưa đủ part ({detail}) — tổng thiếu, đối chiếu không tin cậy (fail-safe).",
                  fix="Bổ sung area_m2+material+thickness cho part thiếu, hoặc dùng mass_props.bottom_up_kg đã tính đủ.",
                  source=src)
        else:
            dev = abs(bu - float(ref)) / float(ref) * 100.0
            obs = f"{bu:.1f} kg vs ref {ref} kg (Δ {dev:.1f}%)"
            exp = f"±{tol_pct}% ({scope})"
            if dev > float(tol_pct):
                r.add("mass_reconciliation", "FAIL", sev, obs, exp,
                      f"Lệch khối lượng {dev:.1f}% > ±{tol_pct}% — dấu hiệu sai trích xuất / thiếu part / vật liệu sai.",
                      fix="Rà part thiếu-thừa, vật liệu/độ dày sai; hoặc kỹ sư hiệu chỉnh lightship estimate.",
                      source=src)
            else:
                r.add("mass_reconciliation", "PASS", sev, obs, exp,
                      f"Bottom-up khớp lightship trong ±{tol_pct}%.", source=src)

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
        for t in extract.get("tolerances", []) or []:
            try:
                v = abs(float(t.get("value")))
            except (TypeError, ValueError):
                continue
            conf = t.get("confidence", "LOW")
            src = t.get("source") or f"tol:{t.get('rule')}"
            if tmax is not None and v > float(tmax):
                r.add("tolerance_mm", "FAIL", sev, f"±{v} mm", f"<= ±{tmax} mm",
                      f"Dung sai ±{v}mm vượt ±{tmax}mm.", fix="Siết dung sai hoặc xét chế tạo.", source=src)
            elif not _conf_ok(conf, min_conf):
                r.add("tolerance_mm", "FAIL", sev, f"±{v} mm (conf={conf})", f"conf >= {min_conf}",
                      f"Dung sai conf {conf} < {min_conf}.", fix="Xác nhận giá trị.", source=src)
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

    # 9. DFA part-count (producibility — Boothroyd-Dewhurst Design for Assembly).
    # Tất định: trần số chi tiết + tỷ lệ mối ghép rời (fastener = ứng viên loại #1 của DFMA);
    # DFA index = essential/total CHỈ khi BOM mang cờ dfa_essential (3 câu Boothroyd — kỹ sư trả
    # lời ở embodiment; Sensor KHÔNG phán). advisory:true => WARN (gate mở); false => FAIL (gate đóng).
    dfa = rs.get("dfa_part_count")
    if dfa:
        sev = dfa.get("severity", "major")
        st = "WARN" if dfa.get("advisory", True) else "FAIL"
        bom = extract.get("bom", []) or []
        kws = [_norm(k) for k in dfa.get("fastener_keywords", [])]
        if not bom:
            if dfa.get("required", False):
                r.add("dfa_part_count", st, sev, "(no BOM)", "assembly BOM",
                      "Không có BOM để tính DFA — " + ("cảnh báo" if st == "WARN" else "fail-safe") + ".",
                      fix="Cấp BOM cụm (extract.bom[]) với qty + tên part.", source="extract.bom")
        else:
            total = fasteners = essential = 0.0
            flagged = 0
            for b in bom:
                try:
                    qty = float(b.get("qty") or 1)
                except (TypeError, ValueError):
                    qty = 1.0
                total += qty
                tag = _norm(b.get("name") or b.get("item") or b.get("code"))
                if kws and any(k in tag for k in kws):
                    fasteners += qty
                fl = b.get("dfa_essential")
                if isinstance(fl, bool):
                    flagged += 1
                    if fl:
                        essential += qty
            mp = dfa.get("max_parts")
            if mp is not None:
                ok = total <= float(mp)
                r.add("dfa_part_count.max_parts", "PASS" if ok else st, sev,
                      f"{int(total)} parts", f"<= {mp}",
                      "Số chi tiết trong trần DFA." if ok else
                      f"Số chi tiết {int(total)} > trần {mp} — gộp cụm / bớt part.",
                      fix="" if ok else "Gộp chi tiết chức năng liền, loại part thừa (3 câu Boothroyd).",
                      source="extract.bom")
            mfr = dfa.get("max_fastener_ratio")
            if mfr is not None and total > 0:
                ratio = fasteners / total
                ok = ratio <= float(mfr)
                r.add("dfa_part_count.fastener_ratio", "PASS" if ok else st, sev,
                      f"{ratio:.0%} ({int(fasteners)}/{int(total)})", f"<= {float(mfr):.0%}",
                      "Tỷ lệ mối ghép rời đạt." if ok else
                      f"Tỷ lệ mối ghép rời {ratio:.0%} > {float(mfr):.0%} — thay bằng snap-fit/hàn/liền khối.",
                      fix="" if ok else "Giảm bu lông/vít; ghép tích hợp (DFMA: fastener = ứng viên loại #1).",
                      source="extract.bom")
            mdi = dfa.get("min_dfa_index")
            if mdi is not None:
                if flagged < len(bom) and dfa.get("require_complete", True):
                    r.add("dfa_part_count.dfa_index", st, sev,
                          f"{flagged}/{len(bom)} rows có cờ", "mọi row có dfa_essential",
                          "Chưa đủ cờ dfa_essential (3 câu Boothroyd) để tính DFA index — "
                          + ("cảnh báo" if st == "WARN" else "fail-safe") + ".",
                          fix="Gán dfa_essential (true/false) cho mọi row: chuyển động? / vật liệu khác? / cần rời để tháo-lắp?",
                          source="extract.bom")
                elif total > 0:
                    idx = essential / total
                    ok = idx >= float(mdi)
                    r.add("dfa_part_count.dfa_index", "PASS" if ok else st, sev,
                          f"{idx:.2f} ({int(essential)}/{int(total)})", f">= {mdi}",
                          "DFA index đạt." if ok else
                          f"DFA index {idx:.2f} < {mdi} — nhiều part không thiết yếu.",
                          fix="" if ok else "Loại/gộp part có dfa_essential=false.", source="extract.bom")

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
