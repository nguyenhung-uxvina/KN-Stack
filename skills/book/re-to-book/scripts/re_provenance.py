# -*- coding: utf-8 -*-
"""Neo xuat xu cho /re-to-book: ChNN.provenance.json, check, impact, check-p1.

  check    --prov <dir> --book <dir>
  impact   --prov <dir> --diff <json> [--out <json>]
  check-p1 --book <dir>
Ma thoat: 0 sach, 1 co phat hien, 2 loi dau vao.
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from re_units import normalize  # noqa: E402

ANCHOR_RE = re.compile(r'[\w.\-]+/[^\s#`|]+\.md#[^\s`|\]]+')
_TICK_RE = re.compile(r'`([^`\s][^`]*?\.md#[^`]+)`')
_SPLIT_RE = re.compile(r'^(.*?\.md)#(.+)$', re.S)
OK_CLASSES = ('READ', 'CUT')


class InputError(Exception):
    pass


def _norm_anchor(a):
    return normalize(a).strip()


def anchor_error(anchor, manifest):
    """None neu hop le, nguoc lai ly do."""
    m = _SPLIT_RE.match(_norm_anchor(anchor))
    if not m:
        return 'neo sai dang'
    key, uid = m.group(1), m.group(2)
    ent = manifest.get('files', {}).get(key)
    if ent is None:
        return 'tep khong co trong manifest'
    if ent.get('class') not in OK_CLASSES:
        return 'lop %s khong duoc neo' % ent.get('class')
    if uid not in ent.get('units', {}):
        return 'khong co don vi'
    return None


def load_prov(prov_dir):
    """-> [(ten tep, chapter, sections)] ; loi dau vao => InputError."""
    if not os.path.isdir(prov_dir):
        raise InputError('khong phai thu muc: %s' % prov_dir)
    files = sorted(glob.glob(os.path.join(prov_dir, '*.provenance.json')))
    if not files:
        raise InputError('không có tệp provenance trong %s' % prov_dir)
    out = []
    for p in files:
        name = os.path.basename(p)
        try:
            with open(p, encoding='utf-8-sig') as f:
                d = json.load(f)
        except (OSError, ValueError):
            raise InputError('tep provenance hong: %s' % name)
        secs = d.get('sections') if isinstance(d, dict) else None
        if not isinstance(secs, dict) or not all(isinstance(v, list) for v in secs.values()):
            raise InputError('tep provenance thieu "sections": %s' % name)
        out.append((name, d.get('chapter') or name.split('.')[0], secs))
    return out


def check(prov_dir, manifest):
    errs = []
    for name, _ch, secs in load_prov(prov_dir):
        for sec, anchors in secs.items():
            for a in anchors:
                why = anchor_error(a, manifest)
                if why:
                    errs.append('%s:%s: %s (%s)' % (name, sec, a, why))
    return errs


def impact(prov_dir, diff):
    prov = load_prov(prov_dir)
    cite = {}  # neo -> [(chapter, sec)]
    for _n, ch, secs in prov:
        for sec, anchors in secs.items():
            for a in anchors:
                cite.setdefault(_norm_anchor(a), []).append((ch, sec))
    sections = {}
    for a in set(diff.get('changed', [])) | set(diff.get('removed', [])) | set(diff.get('added', [])):
        for ch, sec in cite.get(_norm_anchor(a), []):
            lst = sections.setdefault(ch, {}).setdefault(sec, [])
            if a not in lst:
                lst.append(a)
    sections = {ch: {s: sorted(v) for s, v in sorted(ss.items())}
                for ch, ss in sorted(sections.items())}
    unanchored = sorted(a for a in diff.get('added', []) if _norm_anchor(a) not in cite)
    status = []
    for s in diff.get('status_changes', []):
        chs = sorted({ch for ch, _ in cite.get(_norm_anchor(s['anchor']), [])})
        status.append({'anchor': s['anchor'], 'from': s['from'], 'to': s['to'], 'chapters': chs})
    return {'sections': sections, 'unanchored_new': unanchored, 'status_changes': status}


def extract_anchors(text):
    """Neo trong span backtick (id co the co dau cach) + neo tran (id khong dau cach)."""
    text = normalize(text)
    found = [m.group(1).strip() for m in _TICK_RE.finditer(text)]
    rest = re.sub(r'`[^`]*`', ' ', text)
    found += [m.group(0).rstrip('.,;:!?)') for m in ANCHOR_RE.finditer(rest)]
    return found


def check_p1(exploration_dir, manifest):
    if not os.path.isdir(exploration_dir):
        raise InputError('khong phai thu muc: %s' % exploration_dir)
    explo = sorted(glob.glob(os.path.join(exploration_dir, '*_Exploration.md')))
    if not explo:
        raise InputError('không có *_Exploration.md trong %s' % exploration_dir)
    targets = list(explo)
    syn = os.path.join(exploration_dir, 'P1_Synthesis.md')
    if os.path.isfile(syn):
        targets.append(syn)
    errs = []
    for p in targets:
        name = os.path.basename(p)
        with open(p, encoding='utf-8-sig') as f:
            anchors = extract_anchors(f.read())
        if p in explo and not anchors:
            errs.append('%s: không có neo nào' % name)
        for a in anchors:
            why = anchor_error(a, manifest)
            if why:
                errs.append('%s: %s (%s)' % (name, a, why))
    return errs


def _load_json(path):
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, ValueError):
        raise InputError('khong doc duoc: %s' % path)


def _report(r):
    print('%-8s %-10s %s' % ('Chuong', 'Muc', 'Neo doi'))
    for ch, ss in r['sections'].items():
        for sec, anchors in ss.items():
            print('%-8s %-10s %s' % (ch, sec, '; '.join(anchors)))
    if not r['sections']:
        print('(khong muc nao bi anh huong)')
    print('unanchored_new: %d' % len(r['unanchored_new']))
    for a in r['unanchored_new']:
        print('  ' + a)
    for s in r['status_changes']:
        print('status: %s %s->%s chuong: %s' % (s['anchor'], s['from'], s['to'],
                                                ','.join(s['chapters']) or '-'))


def main(argv=None):
    ap = argparse.ArgumentParser(prog='re_provenance')
    sub = ap.add_subparsers(dest='cmd')
    c = sub.add_parser('check')
    c.add_argument('--prov', required=True)
    c.add_argument('--book', required=True)
    i = sub.add_parser('impact')
    i.add_argument('--prov', required=True)
    i.add_argument('--diff', required=True)
    i.add_argument('--out')
    p = sub.add_parser('check-p1')
    p.add_argument('--book', required=True)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if not a.cmd:
        print('usage: re_provenance.py check|impact|check-p1 ...', file=sys.stderr)
        return 2
    try:
        if a.cmd == 'impact':
            r = impact(a.prov, _load_json(a.diff))
            text = json.dumps(r, ensure_ascii=False, indent=1) + '\n'
            _report(r)
            if a.out:
                os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
                with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
                    f.write(text)
            else:
                sys.stdout.write(text)
            return 0
        m = _load_json(os.path.join(a.book, '_re_manifest.json'))
        if a.cmd == 'check':
            errs = check(a.prov, m)
        else:
            errs = check_p1(os.path.join(a.book, 'Phase1-Exploration'), m)
    except (OSError, ValueError, KeyError, InputError) as e:
        print('Loi: %s' % e, file=sys.stderr)
        return 2
    for e in errs:
        print(e)
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
