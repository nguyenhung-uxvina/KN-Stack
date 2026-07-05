#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
helix-cad-ingest — local DXF reader.
Parses a DXF (or a folder of DXF) 100% LOCAL with ezdxf and emits
<name>.cad_extract.json + <name>.cad_extract.md per part, per the skill's
fixed schema. Defense-safe: no network. Run offline.

Usage:
  python ingest.py "path/to/part.dxf"
  python ingest.py "path/to/dxf_folder"  --out "path/to/out"  --classification "MẬT"

Every measured value carries source + confidence. Uncertain reads go to
`missing`, never dropped. break-view (geometry != dim override) -> conflicts.
"""
import sys, os, re, io, json, argparse
from collections import Counter

import ezdxf
from ezdxf import recover

# --- known materials (extend as needed) ---
MATERIALS = [
    "NHÔM 5083", "THÉP C45", "THÉP SS400", "THÉP CT3", "THÉP CT1",
    "ĐỒNG ĐỎ", "NHỰA TEFLON", "INOX 304", "INOX 316",
]
PART_ID_RE = re.compile(r"GT\.\d{2}\.\d{2}\.\d{2}(?:\.\d{2})?(?:\s*B[KL])?")
SCALE_RE   = re.compile(r"\b\d+\s*:\s*\d+\b")
NUM_RE     = re.compile(r"-?\d+(?:[.,]\d+)?")
TOL_RE     = re.compile(r"±\s*(\d+(?:[.,]\d+)?)")

# --- collection-method provenance (taxonomy B) -> default confidence ---
# Every extracted value carries HOW it was obtained. Trust derives from method:
# a computed geometry measurement outranks a human-typed value (title-block codes
# are copy-paste-prone — the stale-code failure this set actually hit).
METHOD_CONF = {
    "geometry-counted": "HIGH",   # counted from native geometry entities (CIRCLE…)
    "dim-measured":     "HIGH",   # DIMENSION.get_measurement() on true-scale geometry
    "dim-override":     "MED",    # draftsman-typed value on a dim (human-entered)
    "schedule-table":   "MED",    # BOM / parts-list row
    "title-block":      "MED",    # TEXT in the title block (human-typed)
    "ocr":              "LOW",    # raster -> Tesseract (not wired in this DXF-only reader)
    "human-certified":  "HIGH",   # CEO/engineer certified -> top rank (set downstream)
}


def clean_inline(s: str) -> str:
    """Strip MTEXT/dim inline format codes -> plain text."""
    if not s:
        return ""
    s = re.sub(r"\\f[^;]*;", "", s)          # font \fName|...;
    s = re.sub(r"\\[A-Za-z][^;\\]*;", "", s)  # \A1; \H2.5x; \C3; etc.
    s = re.sub(r"\\[A-Za-z]", "", s)          # bare codes
    s = s.replace("\\P", " ").replace("{", "").replace("}", "")
    return s.strip()


def load(path):
    """Load DXF directly, or DWG via the ODA File Converter (ezdxf odafc add-on).
    DWG = native source-of-truth; DXF = export. Prefer DWG when ODA is available."""
    if path.lower().endswith(".dwg"):
        from ezdxf.addons import odafc
        if not odafc.is_installed():
            raise SystemExit(
                "[ODA-NOT-INSTALLED] Reading .dwg needs the ODA File Converter (free).\n"
                "  Install: download 'ODA File Converter' from opendesign.com (free account),\n"
                "  install to the default path C:\\Program Files\\ODA\\ODAFileConverter\\,\n"
                "  then re-run. ezdxf auto-detects it. Or export the DWG to DXF R2013 and pass the .dxf.\n"
                f"  Expected exe: {odafc.get_win_exec_path()}")
        return odafc.readfile(path), "odafc(dwg)"   # converts DWG->DXF in a temp dir, then loads
    try:
        return ezdxf.readfile(path), "readfile"
    except Exception:
        doc, _aud = recover.readfile(path)
        return doc, "recover"


def num(s):
    m = NUM_RE.search(s or "")
    return float(m.group().replace(",", ".")) if m else None


def extract(path, classification):
    doc, mode = load(path)
    msp = doc.modelspace()
    units = {0: "unitless", 1: "in", 4: "mm", 6: "m"}.get(
        doc.header.get("$INSUNITS", 0), str(doc.header.get("$INSUNITS")))

    # ---- text harvest (keep raw, lose nothing) ----
    raw_text = []
    for e in msp:
        if e.dxftype() == "TEXT":
            t = e.dxf.text.strip()
        elif e.dxftype() == "MTEXT":
            t = e.plain_text().strip()
        else:
            continue
        if t:
            raw_text.append({"layer": e.dxf.layer, "text": t})

    joined = " \n ".join(r["text"] for r in raw_text)

    # ---- meta heuristics ----
    pid = PART_ID_RE.search(joined)
    part_id = pid.group().strip() if pid else None
    material = next((m for m in MATERIALS if m in joined), None)
    scale_m = SCALE_RE.search(joined)
    scale = scale_m.group().replace(" ", "") if scale_m else None

    # candidate name: short uppercase line, not code/material/scale/note/number
    name = None
    for r in raw_text:
        t = r["text"]
        if t.startswith("-") or "\n" in t:
            continue
        if PART_ID_RE.search(t) or SCALE_RE.search(t):
            continue
        if t in MATERIALS:
            continue
        if NUM_RE.fullmatch(t.replace(" ", "")):
            continue
        letters = [c for c in t if c.isalpha()]
        if 3 <= len(t) <= 40 and letters and sum(c.isupper() for c in letters) / len(letters) > 0.6:
            name = t
            break

    notes = [r["text"] for r in raw_text if r["text"].lstrip().startswith("-")]
    process_notes = []
    for blk in notes:
        for ln in re.split(r"\n|(?<=\.)\s+-", blk):
            ln = ln.strip(" -")
            if ln:
                process_notes.append(ln)

    # ---- dimensions + break-view detection ----
    dimensions, conflicts = [], []
    for e in msp.query("DIMENSION"):
        try:
            meas = round(float(e.get_measurement()), 2)
        except Exception:
            meas = None
        ovr = clean_inline(e.dxf.get("text", ""))
        if ovr in ("", "<>"):
            # value read straight from the geometry entity measurement
            value, tol, method, note = meas, "IT14/2", "dim-measured", ""
        else:
            # value is a draftsman-typed override on the dimension (human-entered)
            value = num(ovr)
            tolm = TOL_RE.search(ovr)
            tol = "±" + tolm.group(1) if tolm else "IT14/2"
            method, note = "dim-override", ""
            if isinstance(meas, (int, float)) and value and abs(meas - value) > max(2.0, 0.02 * value):
                note = f"break-view: geometry={meas} vs drawn={value}{(' '+tol) if tol!='IT14/2' else ''}"
                conflicts.append({"type": "BREAK-VIEW",
                                  "detail": f"{value}{tol}: geometry measured {meas} (rút gọn cắt), lấy {value}"})
        dimensions.append({"param": "", "value": value, "unit": "mm",
                           "tolerance": tol, "method": method, "source": "DIMENSION",
                           "confidence": METHOD_CONF[method], "note": note})

    # ---- holes ----
    holes = []
    circ = Counter(round(e.dxf.radius * 2, 1) for e in msp.query("CIRCLE"))
    for dia, n in sorted(circ.items()):
        pts = [[round(e.dxf.center.x), round(e.dxf.center.y)]
               for e in msp.query("CIRCLE") if round(e.dxf.radius * 2, 1) == dia]
        holes.append({"dia": dia, "count": n, "pattern": "", "positions": pts,
                      "method": "geometry-counted", "source": "CIRCLE",
                      "confidence": METHOD_CONF["geometry-counted"], "note": ""})
    n_arc = len(msp.query("ARC"))
    missing = []
    if n_arc:
        missing.append(f"{n_arc} ARC entities (lỗ/bo góc vẽ bằng cung) chưa quy thành lỗ tự động — cần đối chiếu PDF")

    # ---- layers / blocks ----
    used = Counter(e.dxf.layer for e in msp)
    layers = [{"name": l.dxf.name, "color": l.dxf.color, "entity_count": used.get(l.dxf.name, 0)}
              for l in doc.layers if used.get(l.dxf.name, 0)]
    bins = Counter(e.dxf.name for e in msp.query("INSERT"))
    blocks = [{"name": k, "count": v, "attribs": {}} for k, v in bins.most_common()]

    # confidence on inferred meta
    if name is None:
        missing.append("Tên chi tiết không suy ra được tự động — xem raw_text")

    # filename is the RELIABLE part index; DXF title-block codes are often
    # stale (copy-paste) in this source set — keep both, flag mismatch.
    fname = os.path.basename(path)
    fidx_m = re.match(r"\s*([\d.]+)", fname)
    file_index = fidx_m.group(1).rstrip(".") if fidx_m else None
    if part_id:
        missing.append(f"code_in_dxf={part_id} từ khung tên — KHÔNG tin cậy (nguồn copy-paste); dùng file_index={file_index} làm khoá chi tiết")

    rec = {
        "meta": {
            "file_index": file_index,
            "code_in_dxf": part_id, "code_confidence": "LOW",
            "part_id": part_id, "name": name, "assembly": None,
            "product": "GIÁ TRƯỢT UUV" if "TRƯỢT" in joined or "TRŪȊT" in joined else None,
            "material": material, "mass_kg": None, "scale": scale,
            "org": "Viện Kỹ thuật Hải quân" if "HẢI QUÂN" in joined.upper() else None,
            "date": None, "classification": classification,
            "dxf_version": f"{doc.dxfversion} ({doc.acad_release})", "units": units,
            "source_files": {"dxf": os.path.basename(path), "pdf": None},
            "ingested": None, "tool": "helix-cad-ingest",
            # collection-method per title-block field (scalars kept above for
            # backward compat; provenance is additive). code stays LOW via
            # code_confidence — a stale copy-paste code is below title-block default.
            "provenance": {
                "part_id": "title-block", "code_in_dxf": "title-block",
                "name": "title-block", "material": "title-block", "scale": "title-block",
            },
        },
        "dimensions": dimensions,
        # default general tolerance is an ASSUMPTION, not an extraction -> method null,
        # LOW confidence, fail-safe for any min_method gate until parsed/certified.
        "tolerances": [{"rule": "default", "value": "IT14/2", "method": None,
                        "source": "assumed-default", "confidence": "LOW",
                        "note": "giả định mặc định — chưa parse từ general-note; cần xác nhận"}],
        "gdt": [],
        "holes": holes,
        "surface_finish": {"value": "Rz20" if "Rz20" in joined else None,
                           "method": "title-block", "source": "Surface Texture block",
                           "confidence": METHOD_CONF["title-block"]},
        "layers": layers,
        "blocks": blocks,
        "bom": [],
        "process_notes": process_notes,
        "conflicts": conflicts,
        "missing": missing,
        "raw_text": raw_text,
        "_load_mode": mode,
    }
    return rec


def to_md(r):
    m = r["meta"]
    L = []
    L.append(f"# CAD Extract — [{m['file_index'] or '?'}] {m['name'] or m['source_files']['dxf']}".rstrip())
    L.append("")
    L.append(f"> Nguồn: `{m['source_files']['dxf']}` · DXF {m['dxf_version']} · đơn vị {m['units']}")
    L.append(f"> ⚠️ code_in_dxf=`{m['code_in_dxf']}` (khung tên — LOW, có thể là mã copy-paste cũ); khoá tin cậy = file_index `{m['file_index']}`")
    L.append(f"> Phân loại: **{m['classification']}** — parse 100% LOCAL · skill helix-cad-ingest")
    L.append("")
    L.append("## Title")
    L.append("| Trường | Giá trị |")
    L.append("|---|---|")
    for k in ("part_id", "name", "material", "scale", "product", "org"):
        if m.get(k):
            L.append(f"| {k} | {m[k]} |")
    L.append("")
    if r["dimensions"]:
        L.append("## Kích thước (cần CEO chứng thực)")
        L.append("| Value | Tol | Method | Conf | Note |")
        L.append("|---|---|---|---|---|")
        for d in r["dimensions"]:
            L.append(f"| {d['value']} | {d['tolerance']} | {d.get('method','?')} | {d['confidence']} | {d['note']} |")
        L.append("")
    if r["holes"]:
        L.append("## Lỗ")
        for h in r["holes"]:
            L.append(f"- Ø{h['dia']} × {h['count']}  ({h['confidence']})")
        L.append("")
    if r["process_notes"]:
        L.append("## Ghi chú công nghệ")
        for n in r["process_notes"]:
            L.append(f"- {n}")
        L.append("")
    if r["conflicts"]:
        L.append("## ⚠️ Conflicts")
        for c in r["conflicts"]:
            L.append(f"- **[{c['type']}]** {c['detail']}")
        L.append("")
    if r["missing"]:
        L.append("## Missing / cần xác nhận")
        for x in r["missing"]:
            L.append(f"- {x}")
        L.append("")
    return "\n".join(L)


def process(path, outdir, classification):
    rec = extract(path, classification)
    base = os.path.splitext(os.path.basename(path))[0]  # filename = unique reliable key
    stem = os.path.join(outdir, f"{base}.cad_extract")
    with io.open(stem + ".json", "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    with io.open(stem + ".md", "w", encoding="utf-8") as f:
        f.write(to_md(rec))
    nd, nh, nc = len(rec["dimensions"]), len(rec["holes"]), len(rec["conflicts"])
    m = rec["meta"]
    return f"{os.path.basename(path):40} idx={m['file_index'] or '?':8} code_in_dxf={m['code_in_dxf'] or '?':16} dims={nd} holes={nh} confl={nc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--out", default=None, help="output dir (default: alongside source)")
    ap.add_argument("--classification", default="MẬT")
    ap.add_argument("--prefer", default="dwg", choices=["dwg", "dxf"],
                    help="when a folder has both <stem>.dwg and .dxf, which to ingest (default: dwg = native source)")
    a = ap.parse_args()

    targets = []
    if os.path.isdir(a.path):
        cad = [f for f in sorted(os.listdir(a.path)) if f.lower().endswith((".dxf", ".dwg"))]
        # de-duplicate by stem, honoring --prefer (DWG = source-of-truth by default)
        by_stem = {}
        for f in cad:
            stem, ext = os.path.splitext(f)
            ext = ext.lower().lstrip(".")
            if stem not in by_stem or ext == a.prefer:
                by_stem[stem] = f
        targets = [os.path.join(a.path, by_stem[s]) for s in sorted(by_stem)]
    else:
        targets = [a.path]

    for t in targets:
        outdir = a.out or os.path.dirname(t) or "."
        os.makedirs(outdir, exist_ok=True)
        try:
            line = process(t, outdir, a.classification)
        except Exception as ex:
            line = f"{os.path.basename(t):40} -> ERROR {type(ex).__name__}: {ex}"
        try:
            print(line)
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode())


if __name__ == "__main__":
    main()
