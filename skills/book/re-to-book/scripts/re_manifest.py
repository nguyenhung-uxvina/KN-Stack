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
from re_units import normalize, split_units, table_item, _FENCE, _GT_HEAD, _HEAD, _ITEM, _ROW  # noqa: E402
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


_FILL_LATER = re.compile(r'\*\(điền sau[^)]*\)\*')
_ROW_LABEL = {'6': ('KẾT QUẢ', '⟨chờ đo⟩'), '7': ('DỰ ĐOÁN VIẾT TRƯỚC', '⟨chờ ký⟩')}


def _cells(line):
    return line.strip().strip('|').split('|')


def _row_content(unit_text):
    """Muc dang hang bang -> van ban cac o noi dung (bo o so + o nhan); khac -> None."""
    first = unit_text.split('\n', 1)[0]
    if not table_item(first):
        return None
    cells = _cells(first)
    return ' | '.join(cells[2:] if len(cells) >= 3 else cells[1:])


def _signed(unit_text):
    content = _row_content(unit_text)
    lines = [content] if content is not None else unit_text.split('\n')
    for ln in lines:
        m = re.search(r'người ký(.*)ngày(.*)$', ln, re.I)
        if m and _alnum(m.group(1)) and re.search(r'\d', m.group(2)):
            return True
    return False


def _result_empty(unit_text):
    body = _row_content(unit_text)
    if body is None:
        body = re.sub(r'^6\.\s*(\*\*[^*]*\*\*)?', '', unit_text, count=1)
    body = _FILL_LATER.sub('', body)
    return not _alnum(body)


def _marker(unit, which):
    """Dau thay the: hang bang giu so cot; muc danh sach giu dang cu."""
    first = unit.text.split('\n', 1)[0]
    num = table_item(first)
    if not num:
        return MARK_UNSIGNED if which == '7' else MARK_EMPTY
    label, mark = _ROW_LABEL[which]
    n = len(_cells(first))
    out = [num, label, mark] + [''] * (n - 3) if n >= 3 else [num, mark]
    return '| ' + ' | '.join(out) + ' |'


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
    gt, in_fence, cur = None, False, None  # cur = [start, id, la_hang_bang]

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
            num = table_item(line)
            is_row = num is not None
            if not is_row:
                if cur is not None and cur[2] and _ROW.match(line):
                    close(i)  # hang bang khac dong muc dang hang
                    continue
                it = _ITEM.match(line)
                num = it.group(1) if it else None
            if num:
                close(i)
                uid = '%s.%s' % (gt, num)
                n = seen.get(uid, 0) + 1
                seen[uid] = n
                cur = [i, uid if n == 1 else '%s~%d' % (uid, n), is_row]
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
                markers[u.id] = _marker(u, '7')
        elif _ITEM6.search(u.id):
            if _result_empty(u.text):
                flags[u.id] = {'cut': False, 'empty_result': True}
                markers[u.id] = _marker(u, '6')
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


def _norm_root(p):
    """Mot cach viet cho mot thu muc: abspath + normcase, bo dau phan cach cuoi."""
    n = os.path.normcase(os.path.abspath(p))
    s = n.rstrip('/\\')
    if not s or s.endswith(':'):
        return n  # goc o dia / goc POSIX: giu nguyen dau phan cach
    return s


def zero_unit_files(manifest):
    """Tep READ/CUT khong tach duoc don vi nao (de canh bao, khong chan)."""
    return sorted(k for k, e in manifest.get('files', {}).items()
                  if e.get('class') in _SNAP_CLASSES and not e.get('units'))


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
    return {'schema': SCHEMA, 'created': now,
            'roots': {k: _norm_root(v) for k, v in roots.items()},
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


# ---------- diff / gaps / index ----------
STATUS_EMPTY = ('chờ đo', 'đã đo')
STATUS_CUT = ('chờ ký', 'đã ký')


def _unit_map(manifest):
    """-> {anchor: (lop tep, ban ghi don vi)} cho moi tep co don vi."""
    out = {}
    for key, ent in manifest.get('files', {}).items():
        for uid, rec in ent.get('units', {}).items():
            out['%s#%s' % (key, uid)] = (ent['class'], rec)
    return out


def diff_manifests(old, new):
    om, nm = _unit_map(old), _unit_map(new)
    added, changed, removed, status, compared = [], [], [], [], 0
    for a in set(om) | set(nm):
        if a in om and a in nm and om[a][0] == nm[a][0]:
            compared += 1
            o, n = om[a][1], nm[a][1]
            if o['sha256'] != n['sha256']:
                changed.append(a)
            if o.get('empty_result') and not n.get('empty_result'):
                status.append({'anchor': a, 'from': STATUS_EMPTY[0], 'to': STATUS_EMPTY[1]})
            if o.get('cut') and not n.get('cut'):
                status.append({'anchor': a, 'from': STATUS_CUT[0], 'to': STATUS_CUT[1]})
        else:
            if a in om:
                removed.append(a)
            if a in nm:
                added.append(a)
    moved = {}
    orr, nrr = old.get('roots', {}), new.get('roots', {})
    for name in sorted(set(orr) & set(nrr)):
        if _norm_root(orr[name]) != _norm_root(nrr[name]):
            moved[name] = [orr[name], nrr[name]]
    os_, ns_ = old.get('sources', {}), new.get('sources', {})
    src = [k for k in set(os_) | set(ns_)
           if k not in os_ or k not in ns_ or os_[k]['sha256'] != ns_[k]['sha256']]
    status.sort(key=lambda d: (d['anchor'], d['to']))
    return {'root_moved': moved, 'added': sorted(added), 'changed': sorted(changed),
            'removed': sorted(removed), 'sources_changed': sorted(src),
            'status_changes': status, 'compared_units': compared}


def _disk_text(manifest, roots, key):
    """Doc lai tep tu dia (loc GapFill nhu build) -> van ban da normalize."""
    name, rel = key.split('/', 1)
    if name not in roots:
        raise InputError('thieu goc ho so: %s' % name)
    text = _safe_text(os.path.join(roots[name], *rel.split('/')))
    if 'gapfill' in manifest['files'][key]:
        text = _gapfill(text)[1]
    return normalize(text)


def _disk_units(manifest, roots, key):
    """Tach lai tep tu dia theo cung luat build -> {unit id: text}."""
    return {u.id: u.text for u in split_units(_disk_text(manifest, roots, key))}


_MO = re.compile(r'(?<!\w)mở(?!\w)', re.I)
_CLOSED = re.compile(r'ĐÃ TRẢ|BÃI BỎ|CHUYỂN|ĐÓNG', re.I)
_STATUS_HEAD = re.compile(r'trạng thái|status', re.I)


def _row_status(text):
    """-> {row id: o cot Trang thai/Status cua bang chua hang; khong co cot => ca hang}.
    Danh so hang trung (~k) nhu split_units."""
    from re_units import _strip_frontmatter, _row_code
    out, seen = {}, {}
    col, prev_table, in_fence = None, False, False
    for ln in normalize(_strip_frontmatter(text)).split('\n'):
        if _FENCE.match(ln):
            in_fence = not in_fence
            prev_table = False
            continue
        is_table = not in_fence and ln.lstrip().startswith('|')
        if is_table and not prev_table:  # dong dau bang = tieu de (tru khi la hang co ma)
            cells = _cells(ln)
            col = None if _row_code(ln) else next(
                (i for i, c in enumerate(cells) if _STATUS_HEAD.search(c)), None)
        prev_table = is_table
        if not is_table:
            continue
        code = _row_code(ln)
        if not code:
            continue
        uid = 'row:' + code
        n = seen.get(uid, 0) + 1
        seen[uid] = n
        if n > 1:
            uid = '%s~%d' % (uid, n)
        cells = _cells(ln)
        out[uid] = cells[col] if col is not None and col < len(cells) else ln
    return out


def _is_open(status):
    return bool(_MO.search(status)) and not _CLOSED.search(status)
_GAP_SECTIONS = ('Nợ chính xác (Precision_Debt)', 'Hàng N-… còn mở',
                 'Stage Progress bị BỎ', 'Còn mở (status)')


def gaps(manifest, roots):
    items, seen = [], set()

    def add(sec, anchor, text):
        if (sec, anchor, text) not in seen:
            seen.add((sec, anchor, text))
            items.append((sec, anchor, text.strip()))

    for key in sorted(manifest['files']):
        ent = manifest['files'][key]
        rows = [u for u in ent.get('units', {}) if u.startswith('row:')]
        if not rows or ent['class'] not in _SNAP_CLASSES:
            continue
        raw = _disk_text(manifest, roots, key)
        texts = {u.id: u.text for u in split_units(raw)}
        status = _row_status(raw)
        is_debt = key.endswith('_Precision_Debt.md')
        for uid in rows:
            t = texts.get(uid, '')
            if is_debt:
                add(_GAP_SECTIONS[0], '%s#%s' % (key, uid), t)
            if uid.startswith('row:N-') and _is_open(status.get(uid, t)):
                add(_GAP_SECTIONS[1], '%s#%s' % (key, uid), t)
    missing = []
    for name in sorted(set(k.split('/', 1)[0] for k in manifest['files']) | set(roots)):
        key = name + '/_pipeline_state.md'
        if key not in manifest['files']:
            missing.append(name)
            continue
        for uid, t in _disk_units(manifest, roots, key).items():
            anchor = '%s#%s' % (key, uid)
            low = uid.lower()
            if 'stage progress' in low:
                for ln in t.split('\n'):
                    if ln.lstrip().startswith('|') and 'BỎ' in ln:
                        add(_GAP_SECTIONS[2], anchor, ln)
            if 'còn mở' in low:
                for ln in t.split('\n'):
                    if re.match(r'^\s*(?:[-*]\s*)?status:', ln):
                        add(_GAP_SECTIONS[3], anchor, ln)
    out = ['# Chỗ trống hồ sơ RE tự khai', '',
           '> Sinh tự động bởi re_manifest.py gaps — không sửa tay.', '']
    for sec in _GAP_SECTIONS:
        out += ['## ' + sec, '']
        sub = [(a, t) for s_, a, t in items if s_ == sec]
        if not sub:
            out.append('- (không có)')
        for a, t in sub:
            out.append('- `%s` — %s' % (a, t.replace('\n', ' ')))
        out.append('')
    for name in missing:
        out.append('- (không có _pipeline_state.md) %s' % name)
    return '\n'.join(out).rstrip() + '\n'


def units_index(manifest, snapshot_dir=None):
    """Bang don vi trich dan duoc. Trich doc tu ban chup (khong tu ho so goc)."""
    out = ['# Bảng đơn vị trích dẫn được', '',
           'chưa gán: %d / tổng %d' % unassigned_count(manifest), '',
           '| anchor | lớp | nhãn | mức tin | 80 ký tự đầu |',
           '|---|---|---|---|---|']
    cache = {}
    for key in sorted(manifest['files']):
        ent = manifest['files'][key]
        if ent['class'] not in _SNAP_CLASSES:
            continue
        for uid, rec in ent['units'].items():
            if rec.get('cut'):
                ex = '⟨chờ ký⟩'
            elif rec.get('empty_result'):
                ex = '⟨chờ đo⟩'
            elif snapshot_dir is None:
                ex = ''
            else:
                if key not in cache:
                    path = os.path.join(snapshot_dir, *key.split('/'))
                    cache[key] = {u.id: u.text for u in split_units(_safe_text(path))}
                t = cache[key].get(uid, '')
                ex = re.sub(r'\s+', ' ', t)[:80].replace('|', '\\|')
            out.append('| %s | %s | %s | %s | %s |' % (
                ('%s#%s' % (key, uid)).replace('|', '\\|'), ent['class'], rec['label'],
                rec.get('confidence') or '-', ex))
    return '\n'.join(out) + '\n'


def _load_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        raise InputError(path)


def _write(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def _main_read(a):
    try:
        if a.cmd == 'diff':
            d = diff_manifests(_load_json(a.old), _load_json(a.new))
            if a.out:
                _write(a.out, json.dumps(d, ensure_ascii=False, indent=1) + '\n')
            print('compared_units: %d' % d['compared_units'])
            for k in ('added', 'changed', 'removed', 'sources_changed', 'status_changes'):
                print('%s: %d' % (k, len(d[k])))
            print('root_moved: %d' % len(d['root_moved']))
            return 0
        m = _load_json(os.path.join(a.book, '_re_manifest.json'))
        p1 = os.path.join(a.book, 'Phase1-Exploration')
        if a.cmd == 'gaps':
            text = gaps(m, m['roots'])
            _write(os.path.join(p1, '_re_gaps.md'), text)
        else:
            snap = os.path.join(a.book, '_re_snapshot')
            if not os.path.isdir(snap):
                raise InputError(snap)
            _write(os.path.join(p1, '_units_index.md'), units_index(m, snap))
            n, total = unassigned_count(m)
            print('chưa gán: %d / tổng %d' % (n, total))
        return 0
    except (OSError, ValueError, KeyError, InputError) as e:
        print('Loi: %s' % e, file=sys.stderr)
        return 2


def unassigned_count(manifest):
    """-> (so don vi trich dan duoc mang nhan 'chua gan', tong so don vi trich dan duoc)."""
    n = total = 0
    for ent in manifest.get('files', {}).values():
        if ent.get('class') not in _SNAP_CLASSES:
            continue
        for rec in (ent.get('units') or {}).values():
            total += 1
            n += rec.get('label') == 'chưa gán'
    return n, total


# ---------- lock / freeze (an ban = dung ban chup da kiem o P1) ----------
LOCK = '_p1_lock.json'


def _file_sha(path):
    return hashlib.sha256(_safe_bytes(path)).hexdigest()


def _atomic_write_bytes(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + '.tmp'
    try:
        with open(tmp, 'wb') as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _main_lock(a):
    """lock: ghi _manifests/_p1_lock.json = created + sha256 cua _re_manifest.json."""
    try:
        mpath = os.path.join(a.book, '_re_manifest.json')
        m = _load_json(mpath)
        lock = {'created': m['created'], 'sha256': _file_sha(mpath)}
        path = os.path.join(a.book, '_manifests', LOCK)
        _atomic_write_bytes(path, (json.dumps(lock, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
        print('khoá P1: %s · %s' % (lock['created'], lock['sha256'][:12]))
        return 0
    except (OSError, ValueError, KeyError, TypeError, InputError) as e:
        print('Loi: %s' % e, file=sys.stderr)
        return 2


def _main_freeze(a):
    """freeze: chep _re_manifest.json -> _manifests/ed<N>.json CHI KHI trung ban khoa P1."""
    try:
        if a.edition < 1:
            raise InputError('--edition phai >= 1')
        mdir = os.path.join(a.book, '_manifests')
        lpath = os.path.join(mdir, LOCK)
        if not os.path.isfile(lpath):
            raise InputError('chua co %s — chay "lock" o checkpoint P1 truoc' % lpath)
        dst = os.path.join(mdir, 'ed%d.json' % a.edition)
        if os.path.exists(dst):
            raise InputError('%s da co — khong ghi de an ban da chot' % dst)
        mpath = os.path.join(a.book, '_re_manifest.json')
        lock = _load_json(lpath)
        m = _load_json(mpath)
        data = _safe_bytes(mpath)
        if (hashlib.sha256(data).hexdigest() != lock['sha256']
                or m.get('created') != lock['created']):
            print('Manifest hiện tại KHÁC bản đã khoá ở P1 (build lại sau P1?) — '
                  'chạy lại check-p1, CEO duyệt lại P1, rồi "lock" trước khi freeze. '
                  'Không ghi %s.' % dst, file=sys.stderr)
            return 1
        _atomic_write_bytes(dst, data)
        print('chốt ấn bản %d: %s' % (a.edition, dst))
        return 0
    except (OSError, ValueError, KeyError, TypeError, InputError) as e:
        print('Loi: %s' % e, file=sys.stderr)
        return 2


def main(argv=None):
    for st in (sys.stdout, sys.stderr):
        try:
            st.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(prog='re_manifest')
    sub = ap.add_subparsers(dest='cmd')
    b = sub.add_parser('build')
    b.add_argument('--re', required=True)
    b.add_argument('--book', required=True)
    b.add_argument('--classes', default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 're_classes.json'))
    d = sub.add_parser('diff')
    d.add_argument('--old', required=True)
    d.add_argument('--new', required=True)
    d.add_argument('--out')
    for nm in ('gaps', 'index', 'lock'):
        sub.add_parser(nm).add_argument('--book', required=True)
    fz = sub.add_parser('freeze')
    fz.add_argument('--book', required=True)
    fz.add_argument('--edition', required=True, type=int)
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.cmd in ('diff', 'gaps', 'index'):
        return _main_read(a)
    if a.cmd == 'lock':
        return _main_lock(a)
    if a.cmd == 'freeze':
        return _main_freeze(a)
    if a.cmd != 'build':
        print('usage: re_manifest.py build|diff|gaps|index|lock|freeze ...', file=sys.stderr)
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
    for k in zero_unit_files(m):
        print('CẢNH BÁO: %s 0 đơn vị' % k)
    return 0


if __name__ == '__main__':
    sys.exit(main())
