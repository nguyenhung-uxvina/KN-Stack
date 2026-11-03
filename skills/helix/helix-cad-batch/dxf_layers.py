#!/usr/bin/env python3
"""
helix-cad-batch / dxf_layers.py — rename DXF layers in bulk from a mapping CSV (old,new), e.g. to bring
supplier drawings onto the workshop layer standard ("Net dam" -> "0-VISIBLE"). Entities follow their layer.

Never overwrites the input: writes --out. --dry-run only reports what would change.
Usage: python dxf_layers.py --in a.dxf --map map.csv --out a_renamed.dxf [--dry-run]
       python dxf_layers.py --in-dir dxf/ --map map.csv --out-dir dxf_renamed/ [--dry-run]
Exit: 0 ok (mapped layers absent from a file are only reported) · 2 name clash · 3 IO error.
"""
import argparse
import csv
import glob
import os
import sys


def load_map(path):
    m = {}
    for row in csv.reader(open(path, encoding="utf-8-sig")):
        if len(row) >= 2 and row[0].strip() and row[0].strip().lower() != "old":
            m[row[0].strip()] = row[1].strip()
    return m


def rename_file(src, dst, mapping, dry=False):
    import ezdxf
    doc = ezdxf.readfile(src)
    have = {l.dxf.name for l in doc.layers}
    report = {"file": os.path.basename(src), "renamed": [], "missing": [], "clash": []}
    for old, new in mapping.items():
        if old not in have:
            report["missing"].append(old); continue
        if new in have and new != old:
            report["clash"].append(f"{old}->{new}"); continue
        report["renamed"].append(f"{old}->{new}")
        if not dry:
            doc.layers.get(old).rename(new)
            have.discard(old); have.add(new)
    if not dry:
        doc.saveas(dst)
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description="Bulk-rename DXF layers from a CSV map.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--in", dest="inp"); g.add_argument("--in-dir")
    ap.add_argument("--map", required=True)
    ap.add_argument("--out"); ap.add_argument("--out-dir")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    try:
        mapping = load_map(a.map)
        pairs = [(a.inp, a.out)] if a.inp else \
            [(p, os.path.join(a.out_dir or "", os.path.basename(p))) for p in sorted(glob.glob(os.path.join(a.in_dir, "*.dxf")))]
        if not a.dry_run:
            for s, d in pairs:
                if not d or os.path.abspath(s) == os.path.abspath(d):
                    raise OSError("refusing to overwrite input; give --out / --out-dir")
            if a.out_dir:
                os.makedirs(a.out_dir, exist_ok=True)
        reports = [rename_file(s, d, mapping, a.dry_run) for s, d in pairs]
    except (OSError, IOError) as e:
        print(f"[IO-ERROR] {e}", file=sys.stderr)
        return 3
    bad = 0
    for r in reports:
        print(f"{r['file']}: renamed {len(r['renamed'])} · missing {r['missing'] or '-'} · clash {r['clash'] or '-'}")
        bad += bool(r["clash"])
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
