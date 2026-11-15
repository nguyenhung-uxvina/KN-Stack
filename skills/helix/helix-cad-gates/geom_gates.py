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
  F3  cylindrical-face counts by diameter (min_faces <= n <= max_faces)          — missing holes / bores
      + unlisted diameters (cyl_exhaustive, default on)                          — extra holes nobody asked for
      NOTE: F3 alone false-passes (a Ø20 shaft head satisfied a Ø19 shaft check) — put probes on every
      feature that matters.
  F4  parametric flex (needs --model):                                            — hardcoded coordinates
      F4_model_matches_step  build(PARAMS) reproduces the STEP under test (else F4 tests a different model)
      F4_param_flex          each PARAMS value ×(1±flex) rebuilds to a valid closed solid AND the geometry
                             actually changes (a build() that ignores its params used to pass)
      F4_relations           param_probes (coordinates written as expressions of PARAMS, e.g. "length-30")
                             still hold in every flexed build (a hole placed at an absolute x used to pass)
  MASS (INFO, never gating): model mass vs title-block mass. Agents must NOT tune dimensions to hit it.

Modes: --mode release (default) turns the SKIPs that hide a thin contract into FAIL — missing probes[],
missing --model (F4), missing param_probes, missing --approved-hash — unless the signed contract carries a
waiver for that rule id. --mode draft keeps them SKIP and reports verdict DRAFT-PASS, which the judge and
CEO gate refuse (they require verdict == "PASS").

Blind spots found 2026-11-05 (mutants M1–M4 in scripts/test_helix_cad_gates.py): build() ignoring params,
absolute hole position, bbox-only contract passing a part with no hole, extra unspecified hole.

Report schema = helix-cad-validate Report (rule_id/status/severity/observed/expected/message/fix_hint/source);
statuses PASS / FAIL / SKIP / INFO; only FAIL gates. Exit: 0 PASS · 2 FAIL · 3 usage/IO error · 4 DRAFT-PASS.

Usage:
  python geom_gates.py --step model.step --contract geometry_contract.json [--model model.py]
                       [--out report] [--approved-hash <sha256>] [--mode release|draft] [--quiet]
"""
import argparse
import ast
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

# SKIPs that, in release mode, mean "the contract/run is too thin to judge" ⇒ FAIL unless waived.
RELEASE_REQUIRED = {
    "F2_probes": "Hợp đồng phát hành phải có probes[] (≥1 / feature quan trọng).",
    "F4_param_flex": "Phát hành phải chạy F4 với --model model.py (hợp đồng PARAMS/build).",
    "F4_relations": "Phát hành phải có param_probes[] để bắt toạ độ tuyệt đối khi kích thước khác đổi.",
}


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


def is_closed_solid(shape):
    return is_valid(shape) and free_edge_count(shape) == 0 and len(shape.solids()) >= 1


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


def geom_signature(shape):
    """bbox min + size, volume, centroid and the principal moments of inertia about the centroid.
    Moving one through-hole changes the centroid; moving two holes symmetrically in opposite directions
    (e.g. both 25 mm from their own end) leaves the centroid fixed but changes the inertia — measured
    2026-11-05 on a two-plate frame: centroid-only signature reported such a parameter as 'inert'."""
    from build123d import CenterOf
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    bb = shape.bounding_box()
    c = shape.center(CenterOf.MASS)
    props = GProp_GProps()
    BRepGProp.VolumeProperties_s(shape.wrapped, props)
    m = props.MatrixOfInertia()
    inertia = [m.Value(i, j) for i in (1, 2, 3) for j in (1, 2, 3)]
    return {"min": [bb.min.X, bb.min.Y, bb.min.Z], "size": [bb.size.X, bb.size.Y, bb.size.Z],
            "volume": float(shape.volume), "centroid": [c.X, c.Y, c.Z], "inertia": inertia}


def same_signature(a, b, tol_mm=1e-3, tol_rel=1e-6):
    vec = all(abs(x - y) <= tol_mm for k in ("min", "size", "centroid") for x, y in zip(a[k], b[k]))
    vol = abs(a["volume"] - b["volume"]) <= tol_rel * max(abs(b["volume"]), 1.0)
    scale = max(max(abs(v) for v in b.get("inertia", [0.0])), 1.0)
    inert = all(abs(x - y) <= tol_rel * scale for x, y in zip(a.get("inertia", []), b.get("inertia", [])))
    return vec and vol and inert


_OPS = {ast.Add: lambda x, y: x + y, ast.Sub: lambda x, y: x - y,
        ast.Mult: lambda x, y: x * y, ast.Div: lambda x, y: x / y}


def eval_expr(expr, params):
    """Evaluate a probe coordinate: a number, or + - * / over numbers and PARAMS names. Nothing else."""
    if isinstance(expr, (int, float)) and not isinstance(expr, bool):
        return float(expr)

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return float(n.value)
        if isinstance(n, ast.Name):
            if n.id not in params:
                raise ValueError(f"'{n.id}' không có trong PARAMS")
            return float(params[n.id])
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        raise ValueError(f"biểu thức không cho phép: {expr!r}")

    return ev(ast.parse(str(expr), mode="eval"))


def probe_misses(shape, probes, params):
    """Descriptions of param_probes whose inside/outside expectation fails on `shape` under `params`."""
    from build123d import Vector
    bad = []
    for p in probes:
        pt = [eval_expr(v, params) for v in p["pt"]]
        inside = bool(shape.is_inside(Vector(*pt)))
        if inside != bool(p["inside"]):
            bad.append(f'{p.get("why", p["pt"])} @({", ".join(f"{v:g}" for v in pt)}) inside={inside}')
    return bad


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
    claimed = set()
    for f in feats:
        tol = float(f.get("tol", 0.3))
        hits = {d: v for d, v in dias.items() if abs(d - f["dia"]) <= tol}
        claimed.update(hits)
        n = sum(hits.values())
        lo, hi = int(f["min_faces"]), f.get("max_faces")
        ok = n >= lo and (hi is None or n <= int(hi))
        allok &= ok
        expect = f">= {lo}" if hi is None else f"{lo}..{int(hi)}"
        msg = "Có đủ." if ok else ("THIẾU feature trụ (lỗ/trục/bậc)." if n < lo
                                   else "THỪA feature trụ so với hợp đồng (max_faces).")
        rep.add(f"F3_{f['what']}", "PASS" if ok else "FAIL", "critical", f"{n} mặt trụ Ø{f['dia']}±{tol}",
                expect, msg, fix="Đối chiếu danh sách feature trong spec; thêm probe để chắc đúng vị trí.",
                source=src)
    if contract.get("cyl_exhaustive", True):
        extra = {d: v for d, v in dias.items() if d not in claimed}
        ok = not extra
        allok &= ok
        rep.add("F3_unlisted", "PASS" if ok else "FAIL", "critical",
                "0" if ok else ", ".join(f"Ø{d}×{v}" for d, v in sorted(extra.items())),
                "mọi mặt trụ thuộc một cyl_features", "Không có mặt trụ ngoài hợp đồng." if ok else
                "Có mặt trụ (lỗ/trục/bo cung) mà hợp đồng không liệt kê — feature thừa hoặc hợp đồng thiếu.",
                fix="Xoá feature thừa; nếu là bo cung/feature hợp lệ thì kỹ sư thêm vào cyl_features "
                    "(hoặc đặt cyl_exhaustive=false) rồi ký lại.", source=src)
    return allok


def check_f4(model_py, contract, rep, src, step_shape=None, timeout=120):
    if not model_py:
        for rid in ("F4_param_flex", "F4_relations"):
            rep.add(rid, "SKIP", "major", "no --model", "model.py with PARAMS/build",
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
    keys = contract.get("f4_params") or [k for k, v in params.items()
                                         if isinstance(v, (int, float)) and not isinstance(v, bool) and v > 0]
    pprobes = contract.get("param_probes", [])
    broken, inert, drift = [], [], []
    allok = True
    with tempfile.TemporaryDirectory() as td:
        base = cad_runner.build_with_params(model_py, os.path.join(td, "base.step"), {}, timeout)
        if not base["ok"]:
            rep.add("F4_param_flex", "FAIL", "critical", "build(PARAMS) lỗi", "dựng được",
                    "build(PARAMS) không dựng được: " + str(base.get("error", ""))[:200], source=model_py)
            return False
        s0 = load_step(base["step"])
        sig0 = geom_signature(s0)
        if step_shape is not None:
            match = same_signature(geom_signature(step_shape), sig0, tol_mm=0.01, tol_rel=1e-4)
            allok &= match
            rep.add("F4_model_matches_step", "PASS" if match else "FAIL", "critical",
                    "khớp" if match else "lệch", "build(PARAMS) == STEP đang kiểm",
                    "model.py sinh đúng STEP đang kiểm." if match else
                    "model.py KHÔNG sinh ra STEP đang kiểm — F4 đang thử một mô hình khác.",
                    fix="Xuất lại STEP từ đúng model.py (cad_runner.py run) rồi chạy cổng.", source=model_py)
        try:
            base_miss = probe_misses(s0, pprobes, params) if pprobes else []
        except (ValueError, ZeroDivisionError, KeyError) as e:
            base_miss = [f"param_probes lỗi: {e}"]
        for k in keys:
            if k not in params:
                broken.append(f"{k}: không có trong PARAMS"); continue
            sigs = []
            for sgn in (+1, -1):
                tag = f"{k}×{1 + sgn * flex:.2f}"
                over = {k: params[k] * (1 + sgn * flex)}
                r = cad_runner.build_with_params(model_py, os.path.join(td, f"{k}_{sgn}.step"), over, timeout)
                if not r["ok"]:
                    broken.append(f"{tag}: dựng lỗi"); continue
                s = load_step(r["step"])
                if not is_closed_solid(s):
                    broken.append(f"{tag}: B-Rep hỏng"); continue
                sigs.append(geom_signature(s))
                if pprobes and not base_miss:
                    try:
                        drift += [f"{tag}: {m}" for m in probe_misses(s, pprobes, dict(params, **over))]
                    except (ValueError, ZeroDivisionError, KeyError) as e:
                        drift.append(f"{tag}: param_probes lỗi: {e}")
            if len(sigs) == 2 and all(same_signature(sg, sig0) for sg in sigs):
                inert.append(k)
    ok = not broken and not inert
    allok &= ok
    why = []
    if broken:
        why.append("Gãy khi sửa kích thước: " + "; ".join(broken[:8]))
    if inert:
        why.append("Tham số KHÔNG tác động lên hình (build() bỏ qua params / số cứng): " + ", ".join(inert[:8]))
    rep.add("F4_param_flex", "PASS" if ok else "FAIL", "critical" if inert else "major",
            f"{len(keys)} tham số × ±{flex:.0%}", "mọi biến thể dựng lại được, kín, và hình có đổi",
            "Cây feature chịu được sửa kích thước." if ok else " · ".join(why),
            fix="Dùng ràng buộc tương đối (vị trí theo tham số), không toạ độ tuyệt đối; tham số không "
                "ảnh hưởng hình thì bỏ khỏi f4_params.", source=model_py)
    if not pprobes:
        rep.add("F4_relations", "SKIP", "major", "0 param_probes", ">=1 param_probe",
                "Không có param_probes — không bắt được feature đứng yên ở toạ độ tuyệt đối khi kích thước khác đổi.",
                fix='Thêm param_probes[]: toạ độ viết theo PARAMS, vd ["length-30", "width/2", "height/2"].',
                source=src)
    else:
        misses = [f"base: {m}" for m in base_miss] + drift
        rok = not misses
        allok &= rok
        rep.add("F4_relations", "PASS" if rok else "FAIL", "critical",
                f"{len(pprobes)} param_probes × {len(keys)} tham số × ±{flex:.0%}",
                "mọi param_probe đúng trong mọi biến thể",
                "Quan hệ vị trí theo tham số được giữ." if rok else "Quan hệ gãy: " + "; ".join(misses[:8]),
                fix="Đặt feature theo biểu thức của PARAMS (vd x = length - 30), không theo số tuyệt đối.",
                source=model_py)
    return allok


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
    check_f4(model_py, contract, rep, src, step_shape=shape)
    mass_info(shape, contract, rep, src)
    return rep


def enforce_release(rep, contract, approved_hash_given):
    """Release mode: SKIPs that hide a thin contract become FAIL unless the SIGNED contract waives them."""
    waivers = contract.get("waivers") or {}
    for c in rep.checks:
        if c["status"] == "SKIP" and c["rule_id"] in RELEASE_REQUIRED:
            reason = str(waivers.get(c["rule_id"], "")).strip()
            if reason:
                c["message"] += f" — MIỄN (ghi trong hợp đồng đã ký): {reason}"
            else:
                c.update(status="FAIL", severity="critical",
                         message=RELEASE_REQUIRED[c["rule_id"]] + " " + c["message"],
                         fix_hint=(c["fix_hint"] + " " if c["fix_hint"] else "") +
                         f'Hoặc kỹ sư ghi waivers["{c["rule_id"]}"] = "<lý do>" rồi ký lại; '
                         "hoặc chạy --mode draft (không mở judge/CEO).")
    if not approved_hash_given:
        rep.add("contract_integrity", "FAIL", "critical", "không có --approved-hash", "sha256 kỹ sư đã ký",
                "Phát hành phải khoá hợp đồng bằng --approved-hash — không thì agent sửa hợp đồng cũng không ai biết.",
                fix="Kỹ sư ký → tính sha256 một lần → truyền --approved-hash; hoặc chạy --mode draft.")


def render_md(contract, rep, verdict, chash, approved_ok, mode="release"):
    L = [f"# helix-cad-gates — {verdict}", "",
         f"- Part: **{contract.get('part_id', '?')}** · Phương pháp chiếu: {contract.get('projection_method', '?')} "
         f"· Classification: {contract.get('classification', '?')} · Mode: **{mode}**",
         f"- Contract sha256 `{chash[:16]}…` · approved-hash: {'PASS' if approved_ok else 'NOT CHECKED / MISMATCH'}",
         f"- Result: **{verdict}** — {len(rep.gating_failed)} FAIL / {len(rep.checks)} checks", "",
         "| Rule | Status | Observed | Expected | Severity |", "|---|---|---|---|---|"]
    for c in rep.checks:
        L.append(f"| {c['rule_id']} | {c['status']} | {c['observed']} | {c['expected']} | {c['severity']} |")
    if rep.gating_failed:
        L += ["", "## ❌ FAIL detail"]
        for c in rep.gating_failed:
            L.append(f"- **{c['rule_id']}**: {c['message']}" + (f"\n  - fix: {c['fix_hint']}" if c["fix_hint"] else ""))
    if verdict == "DRAFT-PASS":
        L += ["", "> ⚠️ DRAFT-PASS: chạy --mode draft, có SKIP không bị ép. KHÔNG mở judge / cổng CEO."]
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
    ap.add_argument("--mode", choices=("release", "draft"), default="release",
                    help="release (default): thin contract / no --model / no hash ⇒ FAIL. draft: SKIP, verdict DRAFT-PASS")
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
    approved_ok = bool(a.approved_hash)
    if a.approved_hash:
        approved_ok = chash == a.approved_hash.strip().lower()
        if not approved_ok:
            rep.add("contract_integrity", "FAIL", "critical", chash[:16] + "…", a.approved_hash[:16] + "…",
                    "geometry_contract KHÔNG khớp hash kỹ sư đã duyệt — có thể bị sửa để cổng xanh.",
                    fix="Khôi phục hợp đồng đã duyệt; chỉ kỹ sư định danh được đổi.", source=a.contract)
    if a.mode == "release":
        enforce_release(rep, contract, bool(a.approved_hash))
    if rep.gating_failed:
        verdict = "FAIL"
    else:
        verdict = "PASS" if a.mode == "release" else "DRAFT-PASS"
    out = {"tool": "helix-cad-gates", "version": "1.1", "checked_at": datetime.now(timezone.utc).isoformat(),
           "part_id": contract.get("part_id"), "step": a.step, "contract_sha256": chash, "mode": a.mode,
           "approved_hash_ok": approved_ok, "verdict": verdict, "n_checks": len(rep.checks),
           "n_fail": len(rep.gating_failed), "checks": rep.checks}
    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    with open(a.out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(contract, rep, verdict, chash, approved_ok, a.mode))
    if not a.quiet:
        print(f"=== helix-cad-gates: {verdict} === ({out['n_fail']} FAIL / {out['n_checks']} checks, mode={a.mode})")
        for c in rep.gating_failed:
            print(f"  FAIL {c['rule_id']}: {c['message']}")
    return {"PASS": 0, "DRAFT-PASS": 4}.get(verdict, 2)   # 4 ≠ 0 so exit-code callers never open on a draft


if __name__ == "__main__":
    sys.exit(main())
