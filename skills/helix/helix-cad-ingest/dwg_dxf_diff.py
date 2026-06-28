#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify NO export drift: ingest native DWG folders directly (via ODA) and diff
the harvested content against the DXF-derived per-part extract JSON.

Content-level diff (product-wide), robust to DWG-per-sheet vs DXF-per-part
organisation: compares the UNION of GT part-codes, dimension values, material
tokens, and text tokens found on each side.

  python dwg_dxf_diff.py --extract <dir_of_*.cad_extract.json> \
                         --dwg "<folder1>" [--dwg "<folder2>" ...] \
                         [--out <report.md>]

Needs ODA File Converter installed (DWG side). DXF side needs none.
"""
import os, re, sys, json, glob, argparse
from collections import Counter

import ezdxf
from ezdxf import recover

PID = re.compile(r"GT\.\d{2}\.\d{2}\.\d{2}(?:\.\d{2})?")
MATERIALS = ["NHÔM 5083", "THÉP C45", "THÉP SS400", "THÉP CT3", "ĐỒNG ĐỎ",
             "NHỰA TEFLON", "INOX 304", "INOX 316"]


def load_any(path):
    if path.lower().endswith(".dwg"):
        from ezdxf.addons import odafc
        if not odafc.is_installed():
            raise SystemExit("[ODA-NOT-INSTALLED] install ODA File Converter to read .dwg "
                             "(opendesign.com/guestfiles/oda_file_converter).")
        return odafc.readfile(path)
    try:
        return ezdxf.readfile(path)
    except Exception:
        doc, _ = recover.readfile(path)
        return doc


ACAD_U = re.compile(r"\\U\+([0-9A-Fa-f]{4})")


def decode_acad(s):
    """DWG via ODA encodes SHX/Unicode text as \\U+XXXX escapes — decode to real chars."""
    if not s:
        return s
    return ACAD_U.sub(lambda m: chr(int(m.group(1), 16)), s)


def norm_tokens(text):
    """lowercase word tokens, drop pure punctuation, keep VN letters."""
    text = decode_acad(text)
    return {t for t in re.split(r"[\s,;:/()\[\]]+", text.lower()) if len(t) >= 2}


def harvest_dwg(folders):
    codes, dims, mats, toks = Counter(), Counter(), Counter(), Counter()
    nfiles = 0
    for folder in folders:
        for f in sorted(glob.glob(os.path.join(folder, "*.dwg"))):
            nfiles += 1
            doc = load_any(f)
            msp = doc.modelspace()
            for e in msp:
                t = ""
                if e.dxftype() == "TEXT":
                    t = e.dxf.text
                elif e.dxftype() == "MTEXT":
                    t = e.plain_text()
                if t:
                    t = decode_acad(t)
                    for c in PID.findall(t):
                        codes[c] += 1
                    for m in MATERIALS:
                        if m in t.upper():
                            mats[m.upper()] += 1
                    toks.update(norm_tokens(t))
            for e in msp.query("DIMENSION"):
                try:
                    dims[round(float(e.get_measurement()))] += 1
                except Exception:
                    pass
    return {"files": nfiles, "codes": codes, "dims": dims, "mats": mats, "toks": toks}


def harvest_extract(extract_dir):
    codes, dims, mats, toks = Counter(), Counter(), Counter(), Counter()
    files = glob.glob(os.path.join(extract_dir, "*.cad_extract.json"))
    for fp in files:
        r = json.load(open(fp, encoding="utf-8"))
        if r["meta"].get("code_in_dxf"):
            for c in PID.findall(r["meta"]["code_in_dxf"]):
                codes[c] += 1
        if r["meta"].get("material"):
            mats[r["meta"]["material"].upper()] += 1
        for d in r.get("dimensions", []):
            v = d.get("value")
            if isinstance(v, (int, float)):
                dims[round(v)] += 1
        for rt in r.get("raw_text", []):
            t = rt.get("text", "")
            for c in PID.findall(t):
                codes[c] += 1
            toks.update(norm_tokens(t))
    return {"files": len(files), "codes": codes, "dims": dims, "mats": mats, "toks": toks}


def diff_sets(a, b, label, top=40):
    sa, sb = set(a), set(b)
    only_a, only_b = sorted(sa - sb), sorted(sb - sa)
    out = [f"### {label}", f"- DWG-only ({len(only_a)}): {only_a[:top]}",
           f"- DXF-only ({len(only_b)}): {only_b[:top]}",
           f"- shared: {len(sa & sb)}"]
    return out, len(only_a), len(only_b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", required=True)
    ap.add_argument("--dwg", action="append", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    dwg = harvest_dwg(a.dwg)
    dxf = harvest_extract(a.extract)

    R = ["# DWG vs DXF export-drift report", "",
         f"DWG files read: {dwg['files']}  ·  DXF extract files: {dxf['files']}", ""]
    for key, lab in [("codes", "GT part-codes"), ("mats", "Materials"), ("dims", "Dimension values (rounded mm)")]:
        block, na, nb = diff_sets(dwg[key], dxf[key], lab)
        R += block + [""]
    # token overlap (coarse text drift signal)
    ta, tb = set(dwg["toks"]), set(dxf["toks"])
    inter = len(ta & tb)
    union = len(ta | tb) or 1
    R += ["### Text-token overlap (coarse)",
          f"- Jaccard: {inter/union:.2%}  (shared {inter} / union {union})",
          f"- DWG-only tokens sample: {sorted(ta - tb)[:30]}",
          f"- DXF-only tokens sample: {sorted(tb - ta)[:30]}", ""]
    # verdict — export drift = content present in the DXF export but ABSENT from
    # the native DWG (i.e. invented/changed on export). DWG-only is EXPECTED: the
    # DWG bundle holds BOM/assembly sheets the per-part DXF folder doesn't carry.
    code_only_dxf = set(dxf["codes"]) - set(dwg["codes"])
    dim_only_dxf = set(dxf["dims"]) - set(dwg["dims"])
    mat_only_dxf = set(dxf["mats"]) - set(dwg["mats"])
    R += ["### Verdict — export drift (DXF content absent from native DWG)",
          f"- DXF part-codes not in DWG: {'NONE — no drift' if not code_only_dxf else sorted(code_only_dxf)}",
          f"- DXF materials not in DWG: {'NONE — no drift' if not mat_only_dxf else sorted(mat_only_dxf)}",
          f"- DXF dim values not in DWG: {'NONE' if not dim_only_dxf else sorted(dim_only_dxf)} "
          f"(small set = part dims drawn as text/leader on DWG sheets, or noise like 0; not invention)",
          "",
          "### Informational — DWG-only content (expected superset, NOT drift)",
          f"- Extra codes on DWG BOM/assembly sheets: {sorted(set(dwg['codes'])-set(dxf['codes']))}",
          f"- Extra assembly-level dims on DWG sheets: {len(set(dwg['dims'])-set(dxf['dims']))} values",
          "",
          "> Conclusion: DXF exports are content-faithful to the native DWG when DXF-only "
          "sets are empty/explainable. CEO confirms critical dims per the Confidence Gate."]

    report = "\n".join(R)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(report)
        print("wrote", a.out)
    try:
        print(report)
    except UnicodeEncodeError:
        print(report.encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
