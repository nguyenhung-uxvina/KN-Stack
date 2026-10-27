# -*- coding: utf-8 -*-
"""Manifest + ban chup loc cua cac ho so RE cho /re-to-book. stdlib only.

build: phan lop tung tep, bam don vi, gan nhan tri thuc, ghi ban chup da loc
(khong co Idea_Log, cong phap ly, du doan chua ky).
"""
import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from re_units import normalize, split_units, _FENCE, _GT_HEAD, _HEAD, _ITEM  # noqa: E402
import re_labels  # noqa: E402

SCHEMA = 1
MARK_UNSIGNED = '7. **DỰ ĐOÁN VIẾT TRƯỚC:** ⟨chờ ký⟩'
MARK_EMPTY = '6. **KẾT QUẢ + khuyến nghị:** ⟨chờ đo⟩'
_SNAP_CLASSES = ('READ', 'CUT')
_ITEM7 = re.compile(r'\.7(~\d+)?$')
_ITEM6 = re.compile(r'\.6(~\d+)?$')


class InputError(Exception):
    pass


class UnclassifiedError(Exception):
    def __init__(self, files):
        super().__init__('unclassified: %s' % ', '.join(files))
        self.files = list(files)


def _read_text(path):
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')


def _read_bytes(path):
    with open(path, 'rb') as f:
        return f.read()


def _safe_text(path):
    try:
        return _read_text(path)
    except (OSError, UnicodeDecodeError):
        raise InputError(path)


def _safe_bytes(path):
    try:
        return _read_bytes(path)
    except OSError:
        raise InputError(path)


def _sha(text):
    return hashlib.sha256(normalize(text).encode('utf-8')).hexdigest()


def load_classes(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)['classes']


def classify(rel, classes):
    for c in classes:
        for p in c['patterns']:
            if fnmatch.fnmatchcase(rel, p):
                return c['class']
    return None


# ---------- GapFill ----------
_GF_HEAD = re.compile(r'^##\s+GF-')
_GF_OK = re.compile(r'\*\*Trạng thái:\*\*\s*đã duyệt')


def _frontmatter(text):
    t = text.replace('﻿', '').replace('\r\n', '\n').replace('\r', '\n')
    if t.startswith('---\n'):
        m = re.search(r'^---[ \t]*$', t[4:], re.M)
        if m:
            return t[4:4 + m.start()]
    return ''


def _gapfill(text):
    """-> (mode, filtered_text, approved_headings, excluded_headings).
    mode: 'all' | 'partial' | 'none'."""
    t = normalize(text)
    fm = normalize(_frontmatter(text))
    for ln in fm.split('\n'):
        if re.match(r'status:', ln) and 'đã duyệt' in ln:
            return 'all', t, [], []
    keep, approved, excluded = [], [], []
    state = {'block': [], 'head': None, 'gf': False}

    def flush():
        block = state['block']
        if not state['gf']:
            keep.extend(block)
        elif any(_GF_OK.search(x) for x in block):
            keep.extend(block)
            approved.append(state['head'])
        else:
            excluded.append(state['head'])

    for ln in t.split('\n'):
        if _GF_HEAD.match(ln):
            flush()
            state.update(block=[ln], head=ln.strip(), gf=True)
        else:
            state['block'].append(ln)
    flush()
    if not approved:
        return 'none', '', [], excluded
    return 'partial', normalize('\n'.join(keep)), approved, excluded


# ---------- GT cut rules ----------
def _alnum(s):
    return re.search(r'[^\W_]', s) is not None


def _signed(unit_text):
    for ln in unit_text.split('\n'):
        m = re.search(r'người ký(.*)ngày(.*)$', ln, re.I)
        if m and _alnum(m.group(1)) and re.search(r'\d', m.group(2)):
            return True
    return False


def _result_empty(unit_text):
    body = re.sub(r'^6\.\s*(\*\*[^*]*\*\*)?', '', unit_text, count=1)
    body = body.replace('*(điền sau)*', '')
    return not _alnum(body)


def _item_spans(lines):
    """Quet dong goc, phan tich the GT nhu split_units.
    -> list[(start, end, id)] ; end loai tru dong trong cuoi."""
    start = 0
    if lines and lines[0] == '---':
        for k in range(1, len(lines)):
            if re.match(r'^---[ \t]*$', lines[k]):
                start = k + 1
                break
    spans, seen = [], {}
    gt, in_fence, cur = None, False, None  # cur = [start, id]

    def close(end):
        nonlocal cur
        if cur is not None:
            e = end
            while e > cur[0] + 1 and not lines[e - 1].strip():
                e -= 1
            spans.append((cur[0], e, cur[1]))
            cur = None

    for i in range(start, len(lines)):
        line = lines[i]
        if _FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        g = _GT_HEAD.match(line)
        if g:
            close(i)
            gt = g.group(1)
            continue
        if _HEAD.match(line):
            close(i)
            gt = None
            continue
        if gt:
            it = _ITEM.match(line)
            if it:
                close(i)
                uid = '%s.%s' % (gt, it.group(1))
                n = seen.get(uid, 0) + 1
                seen[uid] = n
                cur = [i, uid if n == 1 else '%s~%d' % (uid, n)]
    close(len(lines))
    return spans


def _apply_cuts(text, units):
    """-> (snapshot_text, flags{unit_id: {...}}). text da normalize.
    Quyet dinh cat theo don vi; ap dung bang quet dong tren van ban goc."""
    flags, markers = {}, {}
    for u in units:
        if u.kind != 'gt_item':
            continue
        if _ITEM7.search(u.id):
            if not _signed(u.text):
                flags[u.id] = {'cut': True}
                markers[u.id] = MARK_UNSIGNED
        elif _ITEM6.search(u.id):
            if _result_empty(u.text):
                flags[u.id] = {'cut': False, 'empty_result': True}
                markers[u.id] = MARK_EMPTY
    lines = text.split('\n')
    done = set()
    for s, e, uid in reversed(_item_spans(lines)):
        if uid in markers:
            lines[s:e] = [markers[uid]]
            done.add(uid)
    for uid in markers:
        if uid not in done:
            raise InputError('khong dat duoc don vi %s' % uid)
    return '\n'.join(lines), flags


# ---------- build ----------
def _walk(root):
    def _err(e):
        raise InputError(getattr(e, 'filename', None) or root)
    for d, dirs, files in os.walk(root, onerror=_err):
        dirs.sort()
        for fn in sorted(files):
            full = os.path.join(d, fn)
            yield full, os.path.relpath(full, root).replace(os.sep, '/')


def build_manifest(roots, classes_path):
    classes = load_classes(classes_path)
    files, sources, unclassified, plan = {}, {}, [], []
    for name, root in roots.items():
        for full, rel in _walk(root):
            if rel.endswith('_Book_GapFill.md'):
                cls = 'GAPFILL'
            else:
                cls = classify(rel, classes)
            if cls is None:
                unclassified.append('%s/%s' % (name, rel))
            else:
                plan.append((name, full, rel, cls))
    if unclassified:
        raise UnclassifiedError(unclassified)

    ceilings = {}
    for name, root in roots.items():
        sp = os.path.join(root, '_pipeline_state.md')
        ceilings[name] = (re_labels.ceiling_from_state(_safe_text(sp))
                          if os.path.isfile(sp) else None)

    for name, full, rel, cls in plan:
        key = '%s/%s' % (name, rel)
        extra, text = {}, None
        if cls == 'GAPFILL':
            text = _safe_text(full)
            mode, filtered, approved, excluded = _gapfill(text)
            if mode == 'none':
                cls = 'BLOCK'
            else:
                cls = 'READ'
                if mode == 'partial':
                    extra = {'gapfill': {'approved': approved, 'excluded': excluded}}
                    text = filtered
        if cls in ('SOURCE', 'IGNORE'):
            b = _safe_bytes(full)
            sources[key] = {'size': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
            continue
        try:
            mtime = os.stat(full).st_mtime
        except OSError:
            raise InputError(full)
        if cls == 'BLOCK':
            files[key] = {'class': 'BLOCK',
                          'sha256': hashlib.sha256(_safe_bytes(full)).hexdigest(),
                          'mtime': mtime}
            continue
        if text is None:
            text = _safe_text(full)
        ent = {'class': cls, 'sha256': _sha(text), 'mtime': mtime}
        ent.update(extra)
        norm = normalize(text)
        units = split_units(norm)
        flags = _apply_cuts(norm, units)[1] if cls in _SNAP_CLASSES else {}
        cap = re_labels.file_cap(units)
        ud = {}
        for u in units:
            lb = re_labels.resolve(u, cap, ceilings[name])
            rec = {'sha256': u.sha256, 'kind': u.kind, 'label': lb.label,
                   'label_source': lb.source, 'confidence': lb.confidence,
                   'confidence_source': lb.confidence_source, 'cut': False}
            rec.update(flags.get(u.id, {}))
            ud[u.id] = rec
        ent['units'] = ud
        files[key] = ent
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
    return {'schema': SCHEMA, 'created': now, 'roots': dict(roots),
            'files': files, 'sources': sources}


def _snapshot_text(ent, text):
    if 'gapfill' in ent:
        text = _gapfill(text)[1]
    norm = normalize(text)
    if ent['class'] in _SNAP_CLASSES:
        return _apply_cuts(norm, split_units(norm))[0]
    return norm


def write_snapshot(manifest, out_dir):
    out_abs = os.path.abspath(out_dir)
    for r in manifest['roots'].values():
        ra = os.path.abspath(r)
        if ra == out_abs or ra.startswith(out_abs + os.sep):
            raise InputError(out_dir)
    tmp_dir = out_dir.rstrip('/\\') + '.tmp'
    try:
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)
        n = 0
        for key, ent in manifest['files'].items():
            if ent['class'] not in _SNAP_CLASSES:
                continue
            name, rel = key.split('/', 1)
            src = os.path.join(manifest['roots'][name], *rel.split('/'))
            raw = _safe_text(src)
            base = _gapfill(raw)[1] if 'gapfill' in ent else raw
            if _sha(base) != ent['sha256']:
                raise InputError(src)
            dst = os.path.join(tmp_dir, name, *rel.split('/'))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'w', encoding='utf-8', newline='\n') as f:
                f.write(_snapshot_text(ent, raw) + '\n')
            n += 1
        os.makedirs(tmp_dir, exist_ok=True)
        old_dir = tmp_dir[:-len('.tmp')] + '.old'
        if os.path.isdir(old_dir):
            shutil.rmtree(old_dir)
        had = os.path.isdir(out_dir)
        if had:
            os.replace(out_dir, old_dir)
        try:
            os.replace(tmp_dir, out_dir)
        except BaseException:
            if had:
                os.replace(old_dir, out_dir)
            raise
        if had:
            shutil.rmtree(old_dir, ignore_errors=True)
    except BaseException:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise
    return n


def _stage_manifest(manifest, path):
    tmp = path + '.tmp'
    try:
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=1)
            f.write('\n')
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return tmp


def main(argv=None):
    ap = argparse.ArgumentParser(prog='re_manifest')
    sub = ap.add_subparsers(dest='cmd')
    b = sub.add_parser('build')
    b.add_argument('--re', required=True)
    b.add_argument('--book', required=True)
    b.add_argument('--classes', default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 're_classes.json'))
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.cmd != 'build':
        print('usage: re_manifest.py build --re <dir>[,<dir>] --book <dir>', file=sys.stderr)
        return 2
    roots = {}
    for d in [x.strip() for x in a.re.split(',') if x.strip()]:
        name = os.path.basename(os.path.abspath(d))
        if name in roots:
            print('trung ten ho so: %s' % name, file=sys.stderr)
            return 2
        if not os.path.isdir(d):
            print('khong phai thu muc: %s' % d, file=sys.stderr)
            return 2
        roots[name] = d
    if not roots or not os.path.isdir(a.book):
        print('thieu --re hoac --book khong ton tai', file=sys.stderr)
        return 2
    mpath = os.path.join(a.book, '_re_manifest.json')
    staged = None
    try:
        m = build_manifest(roots, a.classes)
        staged = _stage_manifest(m, mpath)
        n = write_snapshot(m, os.path.join(a.book, '_re_snapshot'))
        try:
            os.replace(staged, mpath)
        except OSError as e:
            print('Loi: ban chup da doi nhung manifest chua ghi duoc: %s' % e, file=sys.stderr)
            os.remove(staged)
            return 2
        staged = None
    except (OSError, ValueError, KeyError) as e:
        if staged and os.path.exists(staged):
            os.remove(staged)
        print('Loi: %s' % e, file=sys.stderr)
        return 2
    except UnclassifiedError as e:
        print('Tep chua phan lop (%d):' % len(e.files), file=sys.stderr)
        for f in e.files:
            print('  ' + f, file=sys.stderr)
        return 2
    except InputError as e:
        if staged and os.path.exists(staged):
            os.remove(staged)
        print('Loi doc tep: %s' % e, file=sys.stderr)
        return 2
    counts = {}
    for e in m['files'].values():
        counts[e['class']] = counts.get(e['class'], 0) + 1
    counts['SOURCE+IGNORE'] = len(m['sources'])
    for k in sorted(counts):
        print('%-14s %d' % (k, counts[k]))
    print('snapshot: %d tep' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
