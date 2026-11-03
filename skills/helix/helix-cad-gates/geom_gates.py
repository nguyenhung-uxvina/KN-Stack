#!/usr/bin/env python3
"""
helix-cad-gates / geom_gates.py — deterministic GEOMETRY gates for an AI-built STEP, checked against an
engineer-approved geometry contract (spec), not against a reference model.

Why spec, not reference STEP: at use time there is no ground-truth model (RealCADBench: "paired vendor CAD is
usually unavailable"). The contract is what the engineer signed; this script measures the STEP against it.

Gates (measured failure modes, CAD-CUA 2026 + GIÁ TRƯỢT test 2026-11-02):
  F1  closed, valid B-Rep (BRepCheck valid, 0 free edges, >=1 solid)          — open shell / non-manifold
  F2  bbox per axis within tol; flags axis_swap when only the ORDER is wrong;   — projection axis swap
      position probes (point-in-solid) catch mirror images and wrong placement   — first-angle mirror
  F3  cylindrical-face counts by diameter (>= min_faces)                         — missing holes / bores
      NOTE: F3 alone false-passes (a Ø20 shaft head satisfied a Ø19 shaft check) — put probes on every
      feature that matters.
  F4  parametric flex: each PARAMS value ×(1±flex) must rebuild to a valid closed solid (needs --model)
                                                                                  — hardcoded coordinates
  MASS (INFO, never gating): model mass vs title-block mass. Agents must NOT tune dimensions to hit it.

Report schema = helix-cad-validate Report (rule_id/status/severity/observed/expected/message/fix_hint/source);
statuses PASS / FAIL / SKIP / INFO; only FAIL gates. Exit: 0 PASS · 2 FAIL · 3 usage/IO error.

Usage:
  python geom_gates.py --step model.step --contract geometry_contract.json [--model model.py]
                       [--out report] [--approved-hash <sha256>] [--quiet]
"""
import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cad_runner  # noqa: E402

DENSITY_KG_MM3 = {"C45": 7.85e-6, "STEEL": 7.85e-6, "CT3": 7.85e-6, "SS400": 7.85e-6,
                  "INOX304": 7.93e-6, "SUS304": 7.93e-6, "INOX316": 8.0e-6,
                  "AL5083": 2.66e-6, "AL6061": 2.70e-6, "AL": 2.70e-6,
                  "PTFE": 2.2e-6, "TEFLON": 2.2e-6, "POM": 1.41e-6, "DELRIN": 1.41e-6}


class Report:
    """Same record shape as helix-cad-validate/validate.py:Report (kept local to avoid a cross-skill import)."""

    def __init__(self):
        self.checks = []

    def add(self, rule_id, status, severity, observed, expected, message, fix="", source=""):
        self.checks.append({"rule_id": rule_id, "status": status, "severity": severity, "observed": observed,
                            "expected": expected, "message": message, "fix_hint": fix, "source": source})

    @property
    def gating_failed(self):
        return [c for c in self.checks if c["status"] == "FAIL"]


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def _norm_mat(m):
    return "".join(ch for ch in str(m or "").upper() if ch.isalnum())


def load_step(path):
    from build123d import import_step
    return import_step(path)


def free_edge_count(shape):
    from OCP.ShapeAnalysis import ShapeAnalysis_FreeBounds
    from OCP.TopAbs import TopAbs_EDGE
    from OCP.TopExp import TopExp_Explorer
    fb = ShapeAnalysis_FreeBounds(shape.wrapped, 1e-3, False, False)
    n = 0
    for comp in (fb.GetClosedWires(), fb.GetOpenWires()):
        ex = TopExp_Explorer(comp, TopAbs_EDGE)
        while ex.More():
            n += 1
            ex.Next()
    return n


def is_valid(shape):
    from OCP.BRepCheck import BRepCheck_Analyzer
    return bool(BRepCheck_Analyzer(shape.wrapped).IsValid())


def cyl_dias(shape):
    from build123d import GeomType
    c = Counter()
    for f in shape.faces():
        if f.geom_type == GeomType.CYLINDER:
            c[round(2 * f.radius, 2)] += 1
    return c


def bbox_size(shape):
    bb = shape.bounding_box()
    return [round(bb.size.X, 3), round(bb.size.Y, 3), round(bb.size.Z, 3)]


def check_f1(shape, rep, src):
    valid, fe, ns = is_valid(shape), free_edge_count(shape), len(shape.solids())
    ok = valid and fe == 0 and ns >= 1
    rep.add("F1_closed_brep", "PASS" if ok else "FAIL", "critical",
            f"valid={valid}, free_edges={fe}, solids={ns}", "valid=True, free_edges=0, solids>=1",
            "B-Rep kín, hợp lệ." if ok else "B-Rep hở / không hợp lệ (open shell, non-manifold hoặc không có solid).",
            fix="Đóng biên dạng sketch; tránh fillet tự cắt; fuse các thành phần thành 1 solid.", source=src)
    return ok


def check_f2(shape, contract, rep, src):
    got, want = bbox_size(shape), contract["bbox"]
    tol = float(contract.get("bbox_tol", 1.0))
    per_axis = [abs(g - w) <= tol for g, w in zip(got, want)]
    ok = all(per_axis)
    swap = (not ok) and all(abs(a - b) <= tol for a, b in zip(sorted(got), sorted(want)))
    msg = "Hộp bao khớp từng trục." if ok else (
        "ĐẢO TRỤC: đủ kích thước nhưng sai trục — đọc nhầm hình chiếu / quy ước trục." if swap
        else "Hộp bao sai kích thước.")
    rep.add("F2_bbox_per_axis", "PASS" if ok else "FAIL", "critical", f"{got}", f"{want} ±{tol}", msg,
            fix=f"Quy ước: {contract.get('axis_convention', 'front view = XZ, X ngang, Z đứng')}; "
                f"phương pháp chiếu: {contract.get('projection_method', '?')}.", source=src)
    probes = contract.get("probes", [])
    if not probes:
        rep.add("F2_probes", "SKIP", "major", "0 probes", ">=1 probe per critical feature",
                "Hợp đồng không có điểm dò — không bắt được ảnh gương / sai vị trí.",
                fix="Thêm probes[] vào geometry_contract (điểm phải có / không có vật liệu).", source=src)
        return ok
    from build123d import Vector
    if not shape.solids() or not hasattr(shape, "is_inside"):
        rep.add("F2_probes", "FAIL", "critical", "không có solid", f"{len(probes)}/{len(probes)}",
                "Không dò được điểm: hình không phải solid kín (xem F1).", fix="Sửa F1 trước.", source=src)
        return False
    bad = []
    for p in probes:
        inside = bool(shape.is_inside(Vector(*p["pt"])))
        if inside != bool(p["inside"]):
            bad.append(f'{p.get("why", p["pt"])} (got inside={inside})')
    pok = not bad
    rep.add("F2_probes", "PASS" if pok else "FAIL", "critical", f"{len(probes) - len(bad)}/{len(probes)} đúng",
            f"{len(probes)}/{len(probes)}", "Mọi điểm dò đúng." if pok else "Sai: " + "; ".join(bad),
            fix="Kiểm hướng (gương), vị trí và Ø của feature tại các điểm dò sai.", source=src)
    return ok and pok


def check_f3(shape, contract, rep, src):
    feats = contract.get("cyl_features", [])
    if not feats:
        rep.add("F3_features", "SKIP", "major", "-", "cyl_features[]", "Hợp đồng không liệt kê feature trụ.",
                source=src)
        return True
    dias = cyl_dias(shape)
    allok = True
    for f in feats:
        tol = float(f.get("tol", 0.3))
        n = sum(v for d, v in dias.items() if abs(d - f["dia"]) <= tol)
        ok = n >= int(f["min_faces"])
        allok &= ok
        rep.add(f"F3_{f['what']}", "PASS" if ok else "FAIL", "critical", f"{n} mặt trụ Ø{f['dia']}±{tol}",
                f">= {f['min_faces']}", "Có đủ." if ok else "THIẾU feature trụ (lỗ/trục/bậc).",
                fix="Đối chiếu danh sách feature trong spec; thêm probe để chắc đúng vị trí.", source=src)
    return allok


def check_f4(model_py, contract, rep, src, timeout=120):
    if not model_py:
        rep.add("F4_param_flex", "SKIP", "major", "no --model", "model.py with PARAMS/build",
                "Không có mã nguồn — không thử uốn tham số.", source=src)
        return True
    params = cad_runner.read_params(model_py)
    if not params:
        rep.add("F4_param_flex", "FAIL", "critical", "no PARAMS/build(params)", "PARAMS dict + build(params)",
                "model.py KHÔNG theo hợp đồng PARAMS/build(params) — không thử uốn tham số được "
                "(có thể vẫn dùng hằng số có tên; cổng không suy đoán, chỉ đo hợp đồng).",
                fix="Đưa mọi kích thước vào PARAMS; build(params) chỉ đọc từ params.", source=model_py)
        return False
    flex = float(contract.get("f4_flex", 0.10))
    keys = contract.get("f4_params") or [k for k, v in params.items() if isinstance(v, (int, float)) and v > 0]
    broken = []
    with tempfile.TemporaryDirectory() as td:
        for k in keys:
            if k not in params:
                broken.append(f"{k}: không có trong PARAMS"); continue
            for sgn in (+1, -1):
                out = os.path.join(td, f"{k}_{'p' if sgn > 0 else 'm'}.step")
                r = cad_runner.build_with_params(model_py, out, {k: params[k] * (1 + sgn * flex)}, timeout)
                if not r["ok"]:
                    broken.append(f"{k}×{1 + sgn * flex:.2f}: dựng lỗi"); continue
                s = load_step(out)
                if not (is_valid(s) and free_edge_count(s) == 0 and len(s.solids()) >= 1):
                    broken.append(f"{k}×{1 + sgn * flex:.2f}: B-Rep hỏng")
    ok = not broken
    rep.add("F4_param_flex", "PASS" if ok else "FAIL", "major", f"{len(keys)} tham số × ±{flex:.0%}",
            "mọi biến thể dựng lại được, kín", "Cây feature chịu được sửa kích thước." if ok
            else "Gãy khi sửa kích thước: " + "; ".join(broken[:8]),
            fix="Dùng ràng buộc tương đối (vị trí theo tham số), không toạ độ tuyệt đối.", source=model_py)
    return ok


def mass_info(shape, contract, rep, src):
    rho = DENSITY_KG_MM3.get(_norm_mat(contract.get("material")))
    title = contract.get("title_kg")
    if not rho or not title:
        rep.add("MASS_vs_title", "SKIP", "info", "-", "material + title_kg", "Thiếu vật liệu hoặc KL khung tên.",
                source=src)
        return
    kg = shape.volume * rho
    dev = 100 * (kg - title) / title
    rep.add("MASS_vs_title", "INFO", "info", f"{kg:.3f} kg", f"{title} kg (khung tên)",
            f"Lệch {dev:+.1f}% — CHỈ THÔNG TIN. Không được chỉnh kích thước để khớp số này.", source=src)


def run_gates(step, contract, model_py=None, src=None):
    rep = Report()
    src = src or step
    shape = load_step(step)
    check_f1(shape, rep, src)
    check_f2(shape, contract, rep, src)
    check_f3(shape, contract, rep, src)
    check_f4(model_py, contract, rep, src)
    mass_info(shape, contract, rep, src)
    return rep


def render_md(contract, rep, verdict, chash, approved_ok):
    L = [f"# helix-cad-gates — {verdict}", "",
         f"- Part: **{contract.get('part_id', '?')}** · Phương pháp chiếu: {contract.get('projection_method', '?')} "
         f"· Classification: {contract.get('classification', '?')}",
         f"- Contract sha256 `{chash[:16]}…` · approved-hash: {'PASS' if approved_ok else 'NOT CHECKED / MISMATCH'}",
         f"- Result: **{verdict}** — {len(rep.gating_failed)} FAIL / {len(rep.checks)} checks", "",
         "| Rule | Status | Observed | Expected | Severity |", "|---|---|---|---|---|"]
    for c in rep.checks:
        L.append(f"| {c['rule_id']} | {c['status']} | {c['observed']} | {c['expected']} | {c['severity']} |")
    if rep.gating_failed:
        L += ["", "## ❌ FAIL detail"]
        for c in rep.gating_failed:
            L.append(f"- **{c['rule_id']}**: {c['message']}" + (f"\n  - fix: {c['fix_hint']}" if c["fix_hint"] else ""))
    L += ["", "## Cổng người (BẮT BUỘC)",
          "> PASS = mô hình khớp HỢP ĐỒNG đã duyệt, KHÔNG có nghĩa hợp đồng đúng hay chi tiết an toàn.",
          "> CEO/kỹ sư xem render (Spatial Blindness gate) và ký.", "",
          "- [ ] Kỹ sư định danh: ______________________  Ngày: __________"]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deterministic geometry gates (F1–F4 + mass info) vs a signed contract.")
    ap.add_argument("--step", required=True)
    ap.add_argument("--contract", required=True, help="geometry_contract.json (engineer-approved)")
    ap.add_argument("--model", help="model.py honouring PARAMS/build(params) — enables F4")
    ap.add_argument("--out", default="cad_gates_report")
    ap.add_argument("--approved-hash")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args(argv)
    try:
        contract = json.load(open(a.contract, encoding="utf-8"))
        if not os.path.exists(a.step):
            raise OSError(f"no STEP: {a.step}")
    except (OSError, json.JSONDecodeError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    chash = _sha256(a.contract)
    rep = run_gates(a.step, contract, a.model)
    approved_ok = True
    if a.approved_hash:
        approved_ok = chash == a.approved_hash.strip().lower()
        if not approved_ok:
            rep.add("contract_integrity", "FAIL", "critical", chash[:16] + "…", a.approved_hash[:16] + "…",
                    "geometry_contract KHÔNG khớp hash kỹ sư đã duyệt — có thể bị sửa để cổng xanh.",
                    fix="Khôi phục hợp đồng đã duyệt; chỉ kỹ sư định danh được đổi.", source=a.contract)
    verdict = "FAIL" if rep.gating_failed else "PASS"
    out = {"tool": "helix-cad-gates", "version": "1.0", "checked_at": datetime.now(timezone.utc).isoformat(),
           "part_id": contract.get("part_id"), "step": a.step, "contract_sha256": chash,
           "approved_hash_ok": approved_ok, "verdict": verdict, "n_checks": len(rep.checks),
           "n_fail": len(rep.gating_failed), "checks": rep.checks}
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(contract, rep, verdict, chash, approved_ok))
    if not a.quiet:
        print(f"=== helix-cad-gates: {verdict} === ({out['n_fail']} FAIL / {out['n_checks']} checks)")
        for c in rep.gating_failed:
            print(f"  FAIL {c['rule_id']}: {c['message']}")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
