# -*- coding: utf-8 -*-
"""Ban NLM cho /re-to-book: thay moi ma noi bo cua RE bang «phân tích nội bộ».

  re_nlm_redact.py --book <dir> --src <thu muc chunk> --out <thu muc>

Quet lai --out sau khi ghi (doi chung cua chinh no). book.md khong bi dung.
Ma thoat: 0 sach, 1 con ma sot, 2 loi dau vao.
"""
import argparse
import glob
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from re_provenance import ANCHOR_RE  # noqa: E402

PLACEHOLDER = 'phân tích nội bộ'
_GT_SUFFIX_RE = re.compile(r'\.\d+(?:~\d+)?$')
_FILE_RE = re.compile(r'^(?:RE_|TECH_T)')
_LEAK_RE = re.compile(r'RE_[A-Z0-9]+_')
_TICK_FULL_RE = re.compile(r'`[^`\s][^`]*?\.md#[^`]+`')


class InputError(Exception):
    pass


def codes_from_manifest(manifest):
    codes = set()
    for key, ent in manifest.get('files', {}).items():
        base = key.rsplit('/', 1)[-1]
        if _FILE_RE.match(base):
            codes.add(base[:-3] if base.endswith('.md') else os.path.splitext(base)[0])
        for uid in (ent.get('units') or {}):
            if uid.startswith('row:'):
                codes.add(uid[4:])
            elif uid.startswith('GT-'):
                codes.add(_GT_SUFFIX_RE.sub('', uid))
    return sorted((c for c in codes if c), key=lambda c: (-len(c), c))


def _alt(code):
    esc = re.escape(code)
    if _FILE_RE.match(code):
        return esc + r'(?:\.md)?'
    if code.startswith('GT-'):
        return esc + r'(?:\.\d+(?:~\d+)?)?'
    return esc


def _bare_anchor(m):
    s = m.group(0)
    tail = ''
    while s and s[-1] in '.,;:!?)':
        tail = s[-1] + tail
        s = s[:-1]
    return PLACEHOLDER + tail


def redact(text, codes):
    n = 0
    text, k = _TICK_FULL_RE.subn(PLACEHOLDER, text)
    n += k
    text, k = ANCHOR_RE.subn(_bare_anchor, text)
    n += k
    if codes:
        pat = re.compile(r'(?<![\w-])(?:%s)(?![\w])' % '|'.join(
            _alt(c) for c in sorted(set(codes), key=lambda c: (-len(c), c))))
        text, k = pat.subn(PLACEHOLDER, text)
        n += k
    return text, n


def _scan(text, codes):
    hits = [m.group(0) for m in _LEAK_RE.finditer(text)]
    hits += [m.group(0) for m in ANCHOR_RE.finditer(text)]
    if codes:
        pat = re.compile(r'(?<![\w-])(?:%s)(?![\w])' % '|'.join(re.escape(c) for c in codes))
        hits += [m.group(0) for m in pat.finditer(text)]
    return hits


def _inside(child, parent):
    return child == parent or child.startswith(parent + os.sep)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--book', required=True)
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, OSError, ValueError):
        pass
    try:
        book, src, out = (os.path.abspath(p) for p in (a.book, a.src, a.out))
        if _inside(out, src) or _inside(src, out) or _inside(out, book) or _inside(book, out):
            raise InputError('--out khong duoc trung/nam trong/chua --src hoac thu muc sach')
        mpath = os.path.join(book, '_re_manifest.json')
        try:
            with open(mpath, encoding='utf-8-sig') as f:
                manifest = json.load(f)
        except (OSError, ValueError):
            raise InputError('thieu hoac hong manifest: %s' % mpath)
        files = sorted(glob.glob(os.path.join(src, '*.md')) + glob.glob(os.path.join(src, '*.txt')))
        if not files:
            raise InputError('khong co tep *.md/*.txt trong %s' % src)
        codes = codes_from_manifest(manifest)
        tmp = out + '.tmp'
        if os.path.isdir(tmp):
            shutil.rmtree(tmp)
        os.makedirs(tmp)
        total = 0
        try:
            for p in files:
                with open(p, encoding='utf-8-sig') as f:
                    raw = f.read()
                new, n = redact(raw, codes)
                total += n
                print('%s thay %d' % (os.path.basename(p), n))
                with open(os.path.join(tmp, os.path.basename(p)), 'w', encoding='utf-8', newline='\n') as f:
                    f.write(new)
            if os.path.isdir(out):
                shutil.rmtree(out)
            os.replace(tmp, out)
        except BaseException:
            shutil.rmtree(tmp, ignore_errors=True)
            raise
        print('tong %d' % total)
        bad = []
        for p in sorted(glob.glob(os.path.join(out, '*'))):
            with open(p, encoding='utf-8') as f:
                for h in _scan(f.read(), codes):
                    bad.append('%s: %s' % (os.path.basename(p), h))
        if bad:
            print('CON MA SOT trong %s:' % out)
            for b in bad:
                print('  ' + b)
            return 1
        return 0
    except InputError as e:
        print('loi dau vao: %s' % e, file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        print('loi: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
