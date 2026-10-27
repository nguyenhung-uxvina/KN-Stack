# -*- coding: utf-8 -*-
"""P0 cua /re-to-book: chuyen cac thu muc ho so RE tu du an san pham sang du an RE rieng.

plan  : chi doc, ghi ra --out; liet ke di chuyen / sua tu dong / sua tay.
apply : chuyen that, dem lai tep, sua duong dan CHI o tep da duyet. stdlib only.
Thoat 2 khi loi (RefusedError, StalePlanError, CountMismatchError, OSError...).
"""
import argparse
import datetime
import json
import os
import re
import sys

_EXTS = ('.md', '.py', '.json', '.txt')
_SKIP_DIRS = ('.git', '__pycache__')
_UNREADABLE = '⟨không đọc được: mã hoá⟩'
_END = r'(?!\w|-|\.\w)'
_BOM = b'\xef\xbb\xbf'


class RefusedError(Exception):
    pass


class StalePlanError(Exception):
    pass


class CountMismatchError(Exception):
    pass


class PartialMoveError(Exception):
    pass


def _state(moved, rewritten=None, pending=None):
    out = ['Đã chuyển (%d):' % len(moved)]
    out += ['  %s -> %s' % (a, b) for a, b in moved] or ['  (không có)']
    if rewritten is not None:
        out.append('Đã sửa đường dẫn: %s' % (', '.join(rewritten) or '(không có)'))
        out.append('Chưa sửa: %s' % (', '.join(pending) or '(không có)'))
    else:
        out.append('Chưa sửa đường dẫn / README / project: nào.')
    return chr(10).join(out)


def _abs(p):
    return os.path.abspath(p)


def _key(p):
    return os.path.normcase(os.path.abspath(p))


def _is_link(p):
    if os.path.islink(p):
        return True
    ij = getattr(os.path, 'isjunction', None)
    return bool(ij and ij(p))


def _walk(d):
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if not _is_link(os.path.join(root, x))]
        yield root, dirs, files


def _count_files(d):
    return sum(len(fs) for _, _, fs in _walk(d))


def _nested_links(d):
    found = []
    for root, dirs, files in os.walk(d):
        for x in list(dirs) + list(files):
            if _is_link(os.path.join(root, x)):
                found.append(os.path.join(root, x))
        dirs[:] = [x for x in dirs if not _is_link(os.path.join(root, x))]
    return found


def _atomic_write(path, data):
    tmp = path + '.tmp_reconsolidate'
    with open(tmp, 'wb') as f:
        f.write(data)
    os.replace(tmp, path)


def _split_lines(text):
    return re.findall(r'[^\n]*\n|[^\n]+', text)


def _body(line):
    if line.endswith('\n'):
        line = line[:-1]
    if line.endswith('\r'):
        line = line[:-1]
    return line


def _ending(line):
    return line[len(_body(line)):]


def _auto_re(old_project, dossier):
    return re.compile(r'(?<![\w-])' + re.escape(old_project) + r'([\\/])RE([\\/])'
                      + re.escape(dossier) + _END)


def _bare_re(dossier):
    return re.compile(r'(?<![\w-])RE[\\/]' + re.escape(dossier) + _END)


def _scan_files(scan_dirs, skip_trees):
    skip = {_key(t) for t in skip_trees}
    for sd in scan_dirs:
        for root, dirs, files in os.walk(sd):
            dirs[:] = [d for d in dirs
                       if d not in _SKIP_DIRS and _key(os.path.join(root, d)) not in skip
                       and not _is_link(os.path.join(root, d))]
            for f in sorted(files):
                if f.lower().endswith(_EXTS):
                    yield os.path.join(root, f)


def plan(src_root, dossiers, dest_root, scan_dirs, old_project, new_project):
    src_root, dest_root = _abs(src_root), _abs(dest_root)
    moves, trees, states, nested = [], [], [], []
    for d in dossiers:
        s = os.path.join(src_root, d)
        if not os.path.isdir(s):
            raise ValueError('khong co ho so: %s' % s)
        moves.append({'from': s, 'to': os.path.join(dest_root, d), 'file_count': _count_files(s)})
        trees.append(s)
        nested += _nested_links(s)
        for root, _, fs in _walk(s):
            if '_pipeline_state.md' in fs:
                states.append(os.path.join(root, '_pipeline_state.md'))
    autos = [(d, _auto_re(old_project, d)) for d in dossiers]
    bares = [_bare_re(d) for d in dossiers]
    auto_rewrites, manual = [], []
    for path in _scan_files(scan_dirs, trees):
        path = _abs(path)
        try:
            with open(path, 'rb') as f:
                text = f.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            manual.append({'file': path, 'line': 0, 'text': _UNREADABLE})
            continue
        except OSError:
            continue
        for n, raw in enumerate(_split_lines(text), 1):
            line = _body(raw)
            new, hit = line, False
            for d, rx in autos:
                new2 = rx.sub(lambda m, d=d: '%s%sRE%s%s' % (new_project, m.group(1), m.group(2), d), new)
                if new2 != new:
                    hit, new = True, new2
            if hit:
                auto_rewrites.append({'file': path, 'line': n, 'old': line, 'new': new})
            rest = line
            for d, rx in autos:
                rest = rx.sub(lambda m: ' ' * len(m.group(0)), rest)
            if any(b.search(rest) for b in bares):
                manual.append({'file': path, 'line': n, 'text': line})
    return {'src_root': src_root, 'dest_root': dest_root, 'old_project': old_project,
            'new_project': new_project, 'dossiers': list(dossiers), 'moves': moves,
            'auto_rewrites': auto_rewrites, 'manual': manual, 'pipeline_states': states,
            'nested_links': nested}


def _nearest_existing(p):
    p = _abs(p)
    while not os.path.exists(p):
        parent = os.path.dirname(p)
        if parent == p:
            break
        p = parent
    return p


def _verify(rewrites, approved):
    cache = {}
    for rw in rewrites:
        k = _key(rw['file'])
        if k not in approved:
            continue
        if k not in cache:
            try:
                with open(rw['file'], 'rb') as f:
                    cache[k] = [_body(x) for x in _split_lines(f.read().decode('utf-8-sig'))]
            except (OSError, UnicodeDecodeError):
                raise StalePlanError('khong doc duoc: %s' % rw['file'])
        ls = cache[k]
        if rw['line'] < 1 or rw['line'] > len(ls) or ls[rw['line'] - 1] != rw['old']:
            raise StalePlanError('%s dong %s da doi so voi ke hoach' % (rw['file'], rw['line']))


def _write_rewrites(path, items):
    with open(path, 'rb') as f:
        data = f.read()
    lines = _split_lines(data.decode('utf-8-sig'))
    for rw in items:
        i = rw['line'] - 1
        lines[i] = rw['new'] + _ending(lines[i])
    out = ''.join(lines).encode('utf-8')
    _atomic_write(path, (_BOM if data.startswith(_BOM) else b'') + out)


def _fix_project(path, new_project):
    with open(path, 'rb') as f:
        data = f.read()
    text = data.decode('utf-8-sig')
    m = re.match(r'---[ \t]*\r?\n', text)
    if not m:
        return False
    end = re.search(r'\n---[ \t]*(\r?\n|$)', text[m.end() - 1:])
    if not end:
        return False
    fm_end = m.end() - 1 + end.start()
    fm = text[:fm_end]
    new_fm, n = re.subn(r'(?m)^project:[^\r\n]*', lambda _m: 'project: ' + new_project, fm, count=1)
    if not n:
        return False
    _atomic_write(path, (_BOM if data.startswith(_BOM) else b'') + (new_fm + text[fm_end:]).encode('utf-8'))
    return True


def apply(plan, approved_rewrite_files):
    src_root, dest_root = _abs(plan['src_root']), _abs(plan['dest_root'])
    new_project = plan['new_project']
    approved = {_key(f) for f in approved_rewrite_files}
    # (0) ke hoach con khop khong
    _verify(plan['auto_rewrites'], approved)
    # (1) symlink / junction
    for p in [src_root] + [m['from'] for m in plan['moves']] + [dest_root, _nearest_existing(dest_root)]:
        if _is_link(p):
            raise RefusedError('symlink/junction: %s' % p)
    nested = list(plan.get('nested_links', []))
    for m in plan['moves']:
        if os.path.isdir(m['from']):
            nested += _nested_links(m['from'])
    if nested:
        raise RefusedError('liên kết lồng trong hồ sơ: %s' % ', '.join(sorted(set(nested))))
    for m in plan['moves']:
        if not os.path.isdir(m['from']):
            raise RefusedError('khong co ho so nguon: %s' % m['from'])
    # (2) dich da ton tai
    for m in plan['moves']:
        if os.path.lexists(m['to']):
            raise RefusedError('dich da ton tai: %s' % m['to'])
    # (3) chuyen
    os.makedirs(dest_root, exist_ok=True)
    moved, done = [], []
    for m in plan['moves']:
        try:
            os.rename(m['from'], m['to'])
        except OSError as e:
            raise PartialMoveError('Chuyển hồ sơ %s thất bại: %s\n%s' % (m['from'], e, _state(done)))
        moved.append(m['to'])
        done.append((m['from'], m['to']))
    # (4) dem lai
    for m in plan['moves']:
        got = _count_files(m['to'])
        if got != m['file_count']:
            raise CountMismatchError('%s: kế hoạch %d tệp, ở đích %d\n%s'
                                     % (m['to'], m['file_count'], got, _state(done)))
    # (5) sua duong dan o tep da duyet
    by_file = {}
    for rw in plan['auto_rewrites']:
        if _key(rw['file']) in approved:
            by_file.setdefault(rw['file'], []).append(rw)
    rewritten = []
    for path, items in by_file.items():
        try:
            _write_rewrites(path, items)
        except OSError as e:
            pend = [x for x in by_file if x not in rewritten]
            raise PartialMoveError('Sửa đường dẫn %s thất bại: %s\n%s' % (path, e, _state(done, rewritten, pend)))
        rewritten.append(path)
    # (6) project: trong _pipeline_state.md
    no_project = []
    for st in plan.get('pipeline_states', []):
        for m in plan['moves']:
            pre = m['from'] + os.sep
            if st.startswith(pre):
                dst = os.path.join(m['to'], st[len(pre):])
                try:
                    if os.path.exists(dst) and not _fix_project(dst, new_project):
                        no_project.append(dst)
                except OSError as e:
                    raise PartialMoveError('Sửa project: %s thất bại: %s\n%s' % (dst, e, _state(done, rewritten, [])))
                break
    # (7) README
    readme = os.path.join(src_root, 'README.md')
    sec = ['', '## Đã chuyển hồ sơ RE — %s' % datetime.date.today().isoformat(), '']
    sec += ['- `%s` → `%s`' % (os.path.basename(m['from']), m['to']) for m in plan['moves']]
    body = '\n'.join(sec) + '\n'
    if os.path.exists(readme):
        with open(readme, 'rb') as f:
            old = f.read().decode('utf-8-sig')
        with open(readme, 'wb') as f:
            f.write((old + ('' if old.endswith('\n') or not old else '\n') + body).encode('utf-8'))
    else:
        with open(readme, 'wb') as f:
            f.write(('# Hồ sơ RE đã chuyển\n' + body).encode('utf-8'))
    return {'moved': moved, 'rewritten': rewritten, 'readme': readme,
            'pipeline_state_no_project': no_project}


def _print_plan(p):
    print('Di chuyển (%d):' % len(p['moves']))
    for m in p['moves']:
        print('  %s -> %s  [%d tệp]' % (m['from'], m['to'], m['file_count']))
    print('Tự sửa được (%d):' % len(p['auto_rewrites']))
    for r in p['auto_rewrites']:
        print('  %s:%d\n    - %s\n    + %s' % (r['file'], r['line'], r['old'], r['new']))
    print('Phải sửa tay (%d):' % len(p['manual']))
    for r in p['manual']:
        print('  %s:%d  %s' % (r['file'], r['line'], r['text']))


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding='utf-8')
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(prog='re_consolidate')
    sub = ap.add_subparsers(dest='cmd')
    pl = sub.add_parser('plan')
    pl.add_argument('--src-root', required=True)
    pl.add_argument('--dossiers', required=True)
    pl.add_argument('--dest-root', required=True)
    pl.add_argument('--scan', action='append', required=True)
    pl.add_argument('--old-project', required=True)
    pl.add_argument('--new-project', required=True)
    pl.add_argument('--out', required=True)
    ap_ = sub.add_parser('apply')
    ap_.add_argument('--plan', required=True)
    ap_.add_argument('--approve')
    ap_.add_argument('--approve-all-auto', action='store_true')
    ap_.add_argument('--no-rewrite', action='store_true')
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    if a.cmd not in ('plan', 'apply'):
        print('usage: re_consolidate.py plan|apply ...', file=sys.stderr)
        return 2
    try:
        if a.cmd == 'plan':
            scans = [x.strip() for s in a.scan for x in s.split(',') if x.strip()]
            dos = [x.strip() for x in a.dossiers.split(',') if x.strip()]
            p = plan(a.src_root, dos, a.dest_root, scans, a.old_project, a.new_project)
            with open(a.out, 'w', encoding='utf-8') as f:
                json.dump(p, f, ensure_ascii=False, indent=2)
            _print_plan(p)
            return 0
        flags = sum([bool(a.approve), a.approve_all_auto, a.no_rewrite])
        if flags != 1:
            print('apply can dung MOT trong --approve, --approve-all-auto, --no-rewrite', file=sys.stderr)
            return 2
        with open(a.plan, encoding='utf-8') as f:
            p = json.load(f)
        if a.approve:
            files = [x.strip() for x in a.approve.split(',') if x.strip()]
        elif a.approve_all_auto:
            files = sorted({r['file'] for r in p['auto_rewrites']})
        else:
            files = []
        r = apply(p, files)
        print('Đã chuyển %d hồ sơ, sửa %d tệp, README: %s' % (len(r['moved']), len(r['rewritten']), r['readme']))
        for x in r['pipeline_state_no_project']:
            print('Cảnh báo: không có dòng project: trong %s' % x)
        return 0
    except (RefusedError, StalePlanError, CountMismatchError, PartialMoveError, OSError, ValueError, KeyError, TypeError) as e:
        print('Lỗi: %s: %s' % (type(e).__name__, e), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
