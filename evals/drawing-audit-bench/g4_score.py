"""G4 — score the HELIX drawing-audit chain against adjudicated drawing errors (P–C–C roadmap, stage G4).

Inputs (all local; real drawings and truth never go in the repo):
  --orig DIR    ingest outputs (<sheet>.cad_extract.json) of the drawings BEFORE correction
  --fixed DIR   ingest outputs of the same drawings AFTER the adjudicated correction
  --truth F     list of {id, sheet (int), cls, layer, ...}; sheet = leading integer of the extract file name
Measures
  1. Perception coverage — share of sheets where ingest found a part code, a material, BOM rows.
  2. Recall per error class on --orig: strict = a blocking claim on that sheet from a rule mapped to the class;
     lenient = any blocking claim on that sheet.
  3. Burden on --fixed: blocking claims per corrected sheet (residual issues or false positives — reported, not judged).
Usage: python -I -X utf8 evals/drawing-audit-bench/g4_score.py --orig D --fixed D --truth F --out PREFIX"""
import argparse
import glob
import importlib.util
import json
import os
import re
from collections import Counter, defaultdict

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_spec = importlib.util.spec_from_file_location(
    "audit_claims", os.path.join(REPO, "skills", "helix", "helix-cad-validate", "audit_claims.py"))
A = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(A)

# which claim rules count as "detecting" a class (strict recall)
CLASS_RULES = {
    "C1": {"part_code_unique", "bom_code_matches_sheet", "bom_name_matches_sheet"},
    "C2": {"part_code_unique", "title_block_code_untrusted", "part_code_format"},
    "C3": {"material_present", "material_consistent", "material_known"},
    "C4": {"qty_matches_parent"},
    "C5": set(),
}


def sheet_no(path):
    m = re.match(r"(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else None


def load_dir(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.cad_extract.json"))):
        out[sheet_no(p)] = (p, json.load(open(p, encoding="utf-8")))
    return out


def claims_for(exs):
    by_sheet = defaultdict(list)
    for s, (p, ex) in exs.items():
        by_sheet[s] += [c for c in A.from_extract(ex, str(s), p) if c["status"] not in A.NON_BLOCKING]
    for c in A.set_check([(p, ex) for p, ex in exs.values()]):
        s = sheet_no(c["source"])
        by_sheet[s].append(c)
    return by_sheet


def coverage(exs):
    n = len(exs) or 1
    code = sum(bool(ex.get("meta", {}).get("code_in_dxf") or ex.get("meta", {}).get("part_id")) for _, ex in exs.values())
    mat = sum(bool(ex.get("meta", {}).get("material")) for _, ex in exs.values())
    bom = sum(bool(ex.get("bom")) for _, ex in exs.values())
    return {"sheets": len(exs), "with_code": code, "with_material": mat, "with_bom_rows": bom,
            "pct_code": round(100 * code / n, 1), "pct_material": round(100 * mat / n, 1), "pct_bom": round(100 * bom / n, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--orig", required=True)
    ap.add_argument("--fixed", required=True)
    ap.add_argument("--truth", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    orig, fixed = load_dir(a.orig), load_dir(a.fixed)
    truth = json.load(open(a.truth, encoding="utf-8"))
    co, cf = claims_for(orig), claims_for(fixed)
    rows = defaultdict(lambda: {"n": 0, "strict": 0, "lenient": 0})
    for t in truth:
        k = (t["cls"], t["layer"])
        rows[k]["n"] += 1
        cl = co.get(t["sheet"], [])
        if cl:
            rows[k]["lenient"] += 1
        if any(c["rule_id"] in CLASS_RULES.get(t["cls"], set()) for c in cl):
            rows[k]["strict"] += 1
    # discrimination: a useful rule flags far more sheets before correction than after
    def flagged(cs):
        f = defaultdict(set)
        for s, v in cs.items():
            for c in v:
                f[c["rule_id"]].add(s)
        return f
    fo, ff = flagged(co), flagged(cf)
    disc = {r: {"orig_sheets": len(fo.get(r, ())), "fixed_sheets": len(ff.get(r, ()))} for r in sorted(set(fo) | set(ff))}
    burden = {s: len(v) for s, v in cf.items()}
    rule_mix = Counter(c["rule_id"] for v in cf.values() for c in v)
    res = {"coverage_orig": coverage(orig), "coverage_fixed": coverage(fixed),
           "recall": {f"{k[0]}/{k[1]}": v for k, v in sorted(rows.items())},
           "total": {"n": len(truth), "strict": sum(v["strict"] for v in rows.values()),
                     "lenient": sum(v["lenient"] for v in rows.values())},
           "burden_fixed": {"sheets": len(fixed), "blocking_claims": sum(burden.values()),
                            "per_sheet_mean": round(sum(burden.values()) / max(len(fixed), 1), 2),
                            "by_rule": dict(rule_mix.most_common())},
           "discrimination": disc}
    json.dump(res, open(a.out + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    L = ["# G4 — kết quả chuỗi kiểm bản vẽ trên lỗi đã phân xử", "",
         "## 1. Độ phủ Perception (ingest)", "", "| Bộ | Tờ | Có mã | Có vật liệu | Có bảng kê |", "|---|---|---|---|---|"]
    for name, c in (("gốc", res["coverage_orig"]), ("đã sửa", res["coverage_fixed"])):
        L.append(f"| {name} | {c['sheets']} | {c['with_code']} ({c['pct_code']}%) | {c['with_material']} ({c['pct_material']}%) | "
                 f"{c['with_bom_rows']} ({c['pct_bom']}%) |")
    L += ["", "## 2. Tỉ lệ bắt lỗi trên bộ gốc", "", "| Lớp / tầng nên bắt | Số lỗi | Bắt chặt | Bắt lỏng |", "|---|---|---|---|"]
    for k, v in res["recall"].items():
        L.append(f"| {k} | {v['n']} | {v['strict']} ({round(100 * v['strict'] / v['n'])}%) | {v['lenient']} ({round(100 * v['lenient'] / v['n'])}%) |")
    t = res["total"]
    L.append(f"| **Tổng** | {t['n']} | {t['strict']} ({round(100 * t['strict'] / t['n'])}%) | {t['lenient']} ({round(100 * t['lenient'] / t['n'])}%) |")
    b = res["burden_fixed"]
    L += ["", "## 3. Claim chặn còn lại trên bộ đã sửa", "",
          f"{b['blocking_claims']} claim trên {b['sheets']} tờ (trung bình {b['per_sheet_mean']}/tờ). Theo luật: "
          + ", ".join(f"{k} {v}" for k, v in b["by_rule"].items()),
          "", "## 4. Phân biệt: số tờ bị luật báo, trước và sau khi sửa", "",
          "| Luật | Tờ gốc bị báo | Tờ đã sửa bị báo |", "|---|---|---|"]
    L += [f"| {r} | {v['orig_sheets']} | {v['fixed_sheets']} |" for r, v in res["discrimination"].items()]
    L += ["", "Luật báo cùng số tờ trước và sau = không phân biệt được lỗi (báo theo loại tờ, không theo lỗi)."]
    open(a.out + ".md", "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
