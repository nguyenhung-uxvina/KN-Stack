#!/usr/bin/env python3
"""
helix-cad-redraw / sheet_merge.py — merge one-DXF-per-sheet back into ONE DXF set, each sheet at its original
place, and refresh the sha256 of every sheet + the merged file in the manifest.

Input manifest = the one written by the sheet splitter (autocad-bridge `acad_split_sheets`):
  {"to": [{"to": <no>, "tep": <file>, "do_dich": [dx, dy], ...}, ...]}  (original coord = sheet coord − do_dich)
Sheets not in the manifest (new sheets) are appended after the right-most sheet on the same row.

Gotchas encoded: split sheets keep material/plotstyle handles of the source ⇒ xref import fails — discard them.
After merge, AUDIT the result and COUNT entities; a count that "matches" is not proof — also open the merged
file once (ezdxf Importer once dropped every DIMENSION's geometry block while audit and counts passed).

Usage: python sheet_merge.py <MANIFEST.json> <sheet_dir> <out.dxf> [--update-manifest <sheet_manifest.json>]
Exit: 0 ok (audit 0 errors) · 2 audit errors · 3 usage/IO error.
"""
import argparse
import glob
import hashlib
import json
import os
import sys

import ezdxf
from ezdxf import bbox, xref


def merge(manifest, sheet_dir, out):
    mf = json.load(open(manifest, encoding="utf-8"))
    shift = {r["to"]: r["do_dich"] for r in mf["to"]}
    tdoc = ezdxf.new("R2018", units=4)
    tdoc.header["$MEASUREMENT"] = 1
    msp = tdoc.modelspace()
    table, last = [], None
    for f in sorted(glob.glob(os.path.join(sheet_dir, "[0-9][0-9]_*.dxf"))):
        no = int(os.path.basename(f)[:2])
        sdoc = ezdxf.readfile(f)
        for lay in sdoc.layers:
            lay.dxf.discard("material_handle"); lay.dxf.discard("plotstyle_handle")
        before = {e.dxf.handle for e in msp}
        xref.load_modelspace(sdoc, tdoc)
        new = [e for e in msp if e.dxf.handle not in before]
        if no in shift:
            dx, dy = -shift[no][0], -shift[no][1]
        else:
            dx, dy = last[0] + 400.0, last[1]
        for e in new:
            e.translate(dx, dy, 0)
        b = bbox.extents(new)
        if no in shift and (last is None or b.extmax.x > last[0]):
            last = (b.extmax.x, b.extmin.y)
        table.append((no, os.path.basename(f), len(new)))
    tdoc.saveas(out)
    chk = ezdxf.readfile(out)
    errors = len(chk.audit().errors)
    return table, len(chk.modelspace()), errors


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(argv=None):
    ap = argparse.ArgumentParser(description="merge sheets back into one DXF")
    ap.add_argument("manifest"); ap.add_argument("sheet_dir"); ap.add_argument("out")
    ap.add_argument("--update-manifest", help="sheet-folder manifest to refresh sha256 values in")
    try:
        a = ap.parse_args(argv)
        table, n, errors = merge(a.manifest, a.sheet_dir, a.out)
    except SystemExit:
        return 3
    except (IOError, ezdxf.DXFError, KeyError) as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        return 3
    for row in table:
        print(*row, sep="\t")
    print(f"entities: {n} · audit errors: {errors}")
    if a.update_manifest:
        M = json.load(open(a.update_manifest, encoding="utf-8"))
        for t in M.get("to", []):
            p = os.path.join(a.sheet_dir, t["tep"])
            if os.path.exists(p):
                t["sha256"] = sha(p)
        M["ban_tong_sha256"] = sha(a.out)
        json.dump(M, open(a.update_manifest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 2 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
