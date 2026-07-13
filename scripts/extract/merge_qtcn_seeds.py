#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_qtcn_seeds.py — Gộp seed 2D (parse_mech_drawing/extract_to_qtcn_seed) và seed 3D
(freecad_extract) của CÙNG sản phẩm thành 1 seed đầy đủ cho /qtcn --seed.

- 2D mạnh: drawing_no + dung sai + section/plate + tên bảng kê (có dấu).
- 3D mạnh: khối lượng THẬT + SL solid + bbox + vật liệu suy theo tên.

Khớp bằng **tên mờ** (bỏ dấu tiếng Việt + token) vì 2 nguồn phân rã khác mức; ghép greedy
duy nhất theo điểm khớp. KHÔNG ép: phần chỉ có ở một nguồn được giữ lại + gắn cờ provenance.
Báo cáo rõ số khớp / chỉ-2D / chỉ-3D — người dùng rà phần lệch.

Dùng: python merge_qtcn_seeds.py --seed2d <2d.json> --seed3d <3d.json> --out <merged.json>
                                  [--threshold 0.6]
Không cần thư viện ngoài.
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata

STOP = {"lien", "ket", "cua", "va", "cac"}   # token đệm bỏ khi so khớp
# alias 3D-base -> gợi ý tên 2D (khớp mà fuzzy dễ trượt do đặt tên khác hẳn)
ALIAS = {"cot bia": "cot lien ket canh hung dan"}


def strip_accents(s):
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def norm(s):
    s = strip_accents(s).lower()
    s = re.sub(r"\(.*?\)", " ", s)      # bỏ phần trong ngoặc
    s = re.sub(r"[0-9]", " ", s)        # bỏ số (instance/kích thước)
    s = re.sub(r"[^a-z\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def toks(s):
    return {t for t in norm(s).split() if t and t not in STOP}


def head(s):
    """Danh từ đầu (lớp chi tiết: dam/cot/canh/nep/ma/bich/tai/than/gia…) — khóa phân biệt."""
    t = norm(s).split()
    return t[0] if t else ""


def score(a, b):
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return 0.0
    ratio = difflib.SequenceMatcher(None, na, nb).ratio()
    ta, tb = toks(a), toks(b)
    jac = len(ta & tb) / len(ta | tb) if (ta | tb) else 0.0   # Jaccard phạt từ phân biệt thừa
    return max(ratio, jac)


def best_matches(bom3, bom2, threshold):
    """Ghép greedy duy nhất 3D<->2D: BẮT BUỘC cùng danh từ đầu (hoặc alias) + điểm ≥ ngưỡng."""
    pairs = []
    for i, p3 in enumerate(bom3):
        n3 = p3["name"]
        for j, p2 in enumerate(bom2):
            n2 = p2["name"]
            alias_ok = bool(ALIAS.get(norm(n3))) and norm(ALIAS[norm(n3)]) == norm(n2)
            if head(n3) != head(n2) and not alias_ok:
                continue                       # khác lớp chi tiết (dầm≠bích, cánh≠mã) -> bỏ
            sc = max(score(n3, n2), 0.95 if alias_ok else 0.0)
            if sc >= threshold:
                pairs.append((sc, i, j))
    pairs.sort(reverse=True)
    m3, m2, matched = {}, {}, []
    for sc, i, j in pairs:
        if i in m3 or j in m2:
            continue
        m3[i], m2[j] = j, i
        matched.append((i, j, round(sc, 2)))
    return matched, m3, m2


def merged_record(vt, p2, p3, sc):
    s2 = (p2 or {}).get("specs", {}) if p2 else {}
    s3 = (p3 or {}).get("specs", {}) if p3 else {}
    status = "both" if (p2 and p3) else ("2d_only" if p2 else "3d_only")
    q2, q3 = (p2 or {}).get("qty"), (p3 or {}).get("qty")
    rec = {
        "vt": vt,
        "name": (p2 or p3)["name"],                 # ưu tiên tên 2D (có dấu, cấp bản vẽ)
        "name_3d": p3["name"] if p3 else None,
        "match": status, "match_score": sc,
        "drawing_no": (p2 or {}).get("drawing_no"),
        "qty_2d": q2, "qty_3d": q3,
        "qty_note": ("khớp" if str(q2 or "").strip("0 cáitấm") == str(q3 or "") or _qeq(q2, q3)
                     else "LỆCH (%s vs %s) — rà" % (q2, q3)) if (p2 and p3) else None,
        "material_2d": (p2 or {}).get("material"),
        "material_3d": (p3 or {}).get("material"),
        "specs": {
            # từ 2D (bản vẽ)
            "sections": s2.get("sections", []),
            "plate_mm": s2.get("plate_mm"),
            "tolerances": s2.get("tolerances", []),
            "key_dims": s2.get("key_dims", []),
            "sheets": s2.get("sheets", []),
            # từ 3D (khối lượng)
            "est_mass_kg": s3.get("est_mass_kg"),
            "total_mass_kg": s3.get("total_mass_kg"),
            "mass_varies": s3.get("mass_varies"),
            "unit_mass_range_kg": s3.get("unit_mass_range_kg"),
            "bbox_mm": s3.get("bbox_mm"),
            "volume_cm3": s3.get("volume_cm3"),
            "density_g_cm3": s3.get("density_g_cm3"),
            "material_source": s3.get("material_source"),
        },
    }
    return rec


def _qeq(a, b):
    """so SL: '44'=='44', '04'==4, '02 cái'==2."""
    def num(x):
        m = re.search(r"\d+", str(x or ""))
        return int(m.group()) if m else None
    na, nb = num(a), num(b)
    return na is not None and na == nb


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Gộp seed 2D + 3D -> 1 seed đầy đủ")
    ap.add_argument("--seed2d", required=True)
    ap.add_argument("--seed3d", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--threshold", type=float, default=0.72)
    ap.add_argument("--force", action="store_true",
                    help="bỏ qua Gate G1 (seed chưa validate/FAIL) — chỉ dùng khi ghi đè có chủ đích")
    a = ap.parse_args()

    # --- Gate G1 CƯỠNG CHẾ (WX-QT-EXTRACT-SENSOR-01 §4.1): script tiêu thụ từ chối
    #     seed chưa validated. Máy chặn, không phụ thuộc người nhớ chạy validator. ---
    try:
        from validate_qtcn_seed import require_validated
        ok = all([require_validated(a.seed2d, a.force), require_validated(a.seed3d, a.force)])
        if not ok:
            sys.exit(4)
    except ImportError:
        sys.stderr.write("[!] Không import được validate_qtcn_seed (gate bỏ qua — chạy lẻ ngoài repo)\n")

    j2 = json.load(open(a.seed2d, encoding="utf-8"))
    j3 = json.load(open(a.seed3d, encoding="utf-8"))
    bom2, bom3 = j2.get("bom", []), j3.get("bom", [])

    matched, m3, m2 = best_matches(bom3, bom2, a.threshold)
    out_bom, n = [], 0
    match2_by = {j: (i, sc) for i, j, sc in matched}
    match3_by = {i: (j, sc) for i, j, sc in matched}

    # 1) cặp khớp + phần chỉ-2D (đi theo thứ tự BOM 2D — cấp bản vẽ, có drawing_no)
    for j, p2 in enumerate(bom2):
        n += 1
        if j in match2_by:
            i, sc = match2_by[j]
            out_bom.append(merged_record("M%d" % n, p2, bom3[i], sc))
        else:
            out_bom.append(merged_record("M%d" % n, p2, None, None))
    # 2) phần chỉ-3D (bích/mã/tai/thanh profile — chưa có trong BOM bản vẽ)
    for i, p3 in enumerate(bom3):
        if i in match3_by:
            continue
        n += 1
        out_bom.append(merged_record("M%d" % n, None, p3, None))

    both = sum(1 for r in out_bom if r["match"] == "both")
    only2 = sum(1 for r in out_bom if r["match"] == "2d_only")
    only3 = sum(1 for r in out_bom if r["match"] == "3d_only")
    qmis = [r for r in out_bom if r["match"] == "both" and r["qty_note"] and "LỆCH" in r["qty_note"]]

    prod = dict(j2.get("product", {}))
    # lấy total_mass_kg thật từ 3D nếu 2D không có
    prod.setdefault("total_mass_kg", None)
    if j3.get("product", {}).get("total_mass_kg") is not None:
        prod["total_mass_kg_3d"] = j3["product"]["total_mass_kg"]

    merged = {
        "schema": "qtcn-seed-merged/v1",
        "product": prod,
        "sources": {"seed2d": a.seed2d, "seed3d": a.seed3d,
                    "engine2d": j2.get("engine", "2d/dxf"), "engine3d": j3.get("engine", "freecad")},
        "match_summary": {"both": both, "only_2d": only2, "only_3d": only3,
                          "qty_mismatch": len(qmis), "threshold": a.threshold},
        "bom": out_bom,
        "consumables": j2.get("consumables", []) or j3.get("consumables", []),
        "relationships": [],
        "flags": {**j3.get("flags", {}), **j2.get("flags", {}),
                  "merged_2d_3d": True},
        "_note": "Gộp 2D(bản vẽ: drawing_no/dung sai/section)+3D(khối lượng thật/SL solid). "
                 "match=both đã có cả hai; 2d_only=chi tiết cấp bản vẽ chưa map solid (dầm/cánh là cụm hàn "
                 "từ thanh+nẹp bên 3D); 3d_only=solid con (bích/mã/tai/thanh profile) chưa có dòng bản vẽ. "
                 "RÀ các dòng qty_note='LỆCH' và phần only_* trước khi dùng.",
    }
    json.dump(merged, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    sys.stdout.write("[ok] merged -> %s\n" % a.out)
    sys.stdout.write("  both=%d  only_2d=%d  only_3d=%d  qty_mismatch=%d  (threshold=%.2f)\n"
                     % (both, only2, only3, len(qmis), a.threshold))
    sys.stdout.write("  matched pairs:\n")
    for r in out_bom:
        if r["match"] == "both":
            sys.stdout.write("    %-26s <=> %-18s score=%.2f  qty %s/%s  %s\n"
                             % (r["name"][:26], (r["name_3d"] or "")[:18], r["match_score"],
                                r["qty_2d"], r["qty_3d"], r["qty_note"]))


if __name__ == "__main__":
    main()
