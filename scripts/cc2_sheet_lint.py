#!/usr/bin/env python3
"""cc2_sheet_lint - chan phieu gia thuyet (9 muc) va bang tham so thieu nhan cua helix-cc2.

Usage: python scripts/cc2_sheet_lint.py <tep.md> --kind hypo|params [--allow-unsigned]
--allow-unsigned (chi --kind hypo): bo qua DUNG ma PRED_UNSIGNED, de kiem phieu truoc
Cong CEO 3 khi muc 7 chua ky; moi ma khac van chan. Sau khi ky phai chay lai khong co.
Exit: 0 sach, 1 co finding, 2 loi doc tep.
"""
import argparse
import re
import sys
import unicodedata
from collections import namedtuple
from datetime import date

Finding = namedtuple('Finding', 'sheet line code msg')

# Danh sach khoi dau theo CC:2818, nguoi xay duoc them.
EFFECT_WORDS = ('ma sát', 'mòn', 'mài mòn', 'tín hiệu', 'nhiễu', 'độ bền',
                'rò', 'lỏng', 'friction', 'wear')

HEADER_RE = re.compile(r'^PHIẾU GIẢ THUYẾT\s*[—–-]\s*(GT-\d{3})')
ITEM_RE = re.compile(r'^\s*([1-9])\s+(.+)')
DASH = r'[—–-]'
TEST_DATE_RE = re.compile(r'ngày thử:\s*(\d{4}-\d{2}-\d{2})')
SIGN_RE = re.compile(r'người ký\s+(\S.*?)\s*' + DASH + r'\s*ngày\s+(\d{4}-\d{2}-\d{2})')
PLACEHOLDER_RE = re.compile(r'^\{\{.*\}\}$')
LABELS = ('tri thức', 'phỏng đoán', 'giả định')
SOURCE_PREFIXES = ('đo được', 'suy ra (từ', 'chưa biết')


def _nfc(text):
    return unicodedata.normalize('NFC', text)


def parse_sheets(text):
    sheets = []
    cur = None
    for n, raw in enumerate(_nfc(text).splitlines(), 1):
        line = raw.strip()
        m = HEADER_RE.match(line)
        if m:
            cur = {'id': m.group(1), 'items': {}, 'line': n}
            sheets.append(cur)
            continue
        if line.startswith('```'):
            cur = None
            continue
        if cur is None:
            continue
        m = ITEM_RE.match(raw)
        if m:
            k = int(m.group(1))
            cur['items'].setdefault(k, m.group(2).strip())
    return sheets


def _empty(v):
    return v is None or not v.strip() or bool(PLACEHOLDER_RE.match(v.strip()))


FAKE_SIGNERS = ('tbd', 'tên', 'ai', 'claude', 'n/a', 'chưa ký')


def _fake_signer(name):
    n = name.strip()
    return '{{' in n or '<' in n or n.lower() in FAKE_SIGNERS


def _parse_date(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def lint_sheets(text, today=None, allow_unsigned=False):
    sheets = parse_sheets(text)
    if not sheets:
        return [Finding('-', 1, 'NO_SHEETS', 'không có PHIẾU GIẢ THUYẾT — GT-nnn nào')]
    out = []
    for s in sheets:
        sid, ln, it = s['id'], s['line'], s['items']

        def add(code, msg):
            out.append(Finding(sid, ln, code, msg))

        for k in range(1, 10):
            v = it.get(k)
            if k == 4 and v is not None:
                if _empty(v):
                    add('NO_BECAUSE', 'mục 4 (VÌ) trống hoặc placeholder')
                continue
            if _empty(v) and not (k == 6 and v is not None and v.strip() == '{{điền SAU}}'):
                add('MISSING_ITEM', f'mục {k} thiếu hoặc trống')
        v2 = it.get(2)
        if not _empty(v2):
            low = v2.lower()
            hits = [w for w in EFFECT_WORDS
                    if re.search(r'(?<!\w)' + re.escape(w) + r'(?!\w)', low)]
            hits = [w for w in hits if not any(w != o and w in o for o in hits)]
            if hits:
                add('EFFECT_IN_IF', 'mục 2 chứa từ tác dụng: ' + ', '.join(hits))
            if v2.split('|')[0].count('=') > 1:
                add('IF_MULTI_VAR', 'mục 2 (NẾU) có nhiều hơn một biến')
        v5, v7 = it.get(5), it.get(7)
        if not _empty(v7):
            sm = SIGN_RE.search(v7)
            pd = _parse_date(sm.group(2)) if sm else None
            if sm and _fake_signer(sm.group(1)):
                pd = None  # ten nguoi ky la placeholder hoac AI -> chua ky
            tm = TEST_DATE_RE.search(v5) if not _empty(v5) else None
            td = _parse_date(tm.group(1)) if tm else None
            if pd is None:
                if not allow_unsigned:
                    add('PRED_UNSIGNED', 'mục 7 thiếu "người ký <tên> — ngày YYYY-MM-DD"')
            if td is None:
                add('PRED_NOT_BEFORE_TEST', 'mục 5 thiếu "ngày thử: YYYY-MM-DD"')
            elif pd is not None and pd >= td:
                add('PRED_NOT_BEFORE_TEST', f'ngày ký dự đoán {pd} không trước ngày thử {td}')
    return out


def _cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


def lint_param_table(text):
    lines = _nfc(text).splitlines()
    out = []
    found = False
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|'):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                j += 1
            block = lines[i:j]
            hdr = [c.lower() for c in _cells(block[0])]
            if 'nhãn' in hdr and 'nguồn số' in hdr:
                found = True
                rows = 0
                ci, si = hdr.index('nhãn'), hdr.index('nguồn số')
                for off, row in enumerate(block[1:], 1):
                    cells = _cells(row)
                    if all(re.fullmatch(r':?-{2,}:?|', c) for c in cells):
                        continue
                    rows += 1
                    ln = i + off + 1
                    name = cells[0] if cells else '?'
                    lab = (cells[ci] if ci < len(cells) else '').strip().strip('*').lower()
                    src = (cells[si] if si < len(cells) else '').strip().strip('*').lower()
                    if lab not in LABELS:
                        out.append(Finding('BANG', ln, 'LABEL_MISSING',
                                           f'{name}: Nhãn phải là tri thức/phỏng đoán/giả định'))
                    if not src.startswith(SOURCE_PREFIXES):
                        out.append(Finding('BANG', ln, 'SOURCE_MISSING',
                                           f'{name}: Nguồn số phải bắt đầu bằng đo được / suy ra (từ / chưa biết'))
                    elif lab == 'tri thức' and src.startswith('chưa biết'):
                        out.append(Finding('BANG', ln, 'KNOWLEDGE_NO_EVIDENCE',
                                           f'{name}: nhãn tri thức nhưng nguồn chưa biết'))
                if rows == 0:
                    out.append(Finding('BANG', i + 1, 'EMPTY_TABLE',
                                       'bảng có cột Nhãn và Nguồn số nhưng không có dòng dữ liệu'))
            i = j
        else:
            i += 1
    if not found:
        out.append(Finding('BANG', 1, 'NO_TABLE',
                           'không có bảng nào có cả hai cột Nhãn và Nguồn số'))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('path')
    ap.add_argument('--kind', choices=('hypo', 'params'), required=True)
    ap.add_argument('--allow-unsigned', action='store_true',
                    help='chỉ --kind hypo: bỏ qua đúng mã PRED_UNSIGNED (trước Cổng CEO 3)')
    a = ap.parse_args(argv)
    try:
        with open(a.path, encoding='utf-8-sig') as f:
            text = f.read()
    except (OSError, UnicodeDecodeError) as e:
        print(f'ERROR không đọc được tệp: {e}', file=sys.stderr)
        return 2
    if a.allow_unsigned and a.kind != 'hypo':
        print('ERROR --allow-unsigned chỉ dùng với --kind hypo', file=sys.stderr)
        return 2
    fs = lint_sheets(text, allow_unsigned=a.allow_unsigned) if a.kind == 'hypo' else lint_param_table(text)
    for f in fs:
        print(f'{f.sheet}:L{f.line} {f.code} {f.msg}')
    return 1 if fs else 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
