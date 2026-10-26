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

# Tieu de phieu; chap nhan vo markdown `#`/`**` quanh dong.
HEADER_RE = re.compile(r'^(?:#{1,6}\s+)?(?:\*\*)?PHIẾU GIẢ THUYẾT\s*[—–-]\s*(GT-\d{3})')
GT_RE = re.compile(r'GT-\d{3}')
# Dong "giong tieu de" ma HEADER_RE khong doc duoc: mo dau (sau vo markdown) bang "phieu", hoac la tieu de
# markdown / chu dam mo dau bang GT-nnn. Nhac GT-nnn trong muc cua phieu, trong bang hay giua cau thi khong tinh.
HEADER_LIKE_RE = re.compile(r'^[#*>\s]*phiếu\b', re.IGNORECASE)
HEADER_START_RE = re.compile(r'^(?:#{1,6}\s+|\*\*)\s*GT-\d{3}')
LABEL_RE = re.compile(r'^[^:]{1,40}:')
CONTROL_RE = re.compile(r'\|\s*đối chứng', re.IGNORECASE)
ITEM_RE = re.compile(r'^\s*([1-9])\s+(.+)')
DASH = r'[—–-]'
TEST_DATE_RE = re.compile(r'ngày thử:\s*(\d{4}-\d{2}-\d{2})')
SIGN_RE = re.compile(r'người ký\s+(\S.*?)\s*' + DASH + r'\s*ngày\s+(\d{4}-\d{2}-\d{2})')
PLACEHOLDER_RE = re.compile(r'^\{\{[^{}]*\}\}$')
LABELS = ('tri thức', 'phỏng đoán', 'giả định')
SOURCE_PREFIXES = ('đo được', 'suy ra (từ', 'chưa biết')


def _nfc(text):
    return unicodedata.normalize('NFC', text)


def parse_sheets(text, unparsed=None):
    """Tach phieu. `unparsed` (list) nhan (so dong, dong) giong tieu de ma khong doc duoc."""
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
        im = ITEM_RE.match(raw)
        if cur is not None and im:
            k = int(im.group(1))
            cur['items'].setdefault(k, im.group(2).strip())
            continue
        if unparsed is not None and GT_RE.search(line) and not line.startswith('|') and \
                (HEADER_LIKE_RE.match(line) or HEADER_START_RE.match(line)):
            unparsed.append((n, line))
    return sheets


def _content(v):
    """Bo nhan dau muc (`VÌ:`, `8 …:`) de chi con noi dung."""
    if v is None:
        return None
    return LABEL_RE.sub('', v.strip(), count=1).strip()


def _empty(v):
    c = _content(v)
    return c is None or not re.search(r'\w', c) or bool(PLACEHOLDER_RE.match(c))


# Ten nguoi ky la placeholder hoac AI: khop chuoi con, khong phan biet hoa thuong; `ai` khop ca tu.
FAKE_SIGNER_SUBSTR = ('claude', 'trợ lý', '{{', '<', 'tbd', 'chưa ký', 'n/a')
FAKE_SIGNER_WORD_RE = re.compile(r'\bai\b', re.IGNORECASE)


def _fake_signer(name):
    n = _nfc(name).strip().casefold()
    return (any(x in n for x in FAKE_SIGNER_SUBSTR) or bool(FAKE_SIGNER_WORD_RE.search(n))
            or n == 'tên')


def _parse_date(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def lint_sheets(text, today=None, allow_unsigned=False):
    """today: date; co thi ngay ky muc 7 sau today -> PRED_FUTURE_SIGN (CLI truyen date.today())."""
    unparsed = []
    sheets = parse_sheets(text, unparsed)
    out = [Finding(GT_RE.search(l).group(0), n, 'HEADER_UNPARSED',
                   'dòng giống tiêu đề phiếu nhưng không đúng dạng "PHIẾU GIẢ THUYẾT — GT-nnn": ' + l[:60])
           for n, l in unparsed]
    if not sheets:
        return out + [Finding('-', 1, 'NO_SHEETS', 'không có PHIẾU GIẢ THUYẾT — GT-nnn nào')]
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
            if _empty(v) and not (k == 6 and v is not None and _content(v) == '{{điền SAU}}'):
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
            if not CONTROL_RE.search(v2):
                add('NO_CONTROL', 'mục 2 thiếu "| Đối chứng: …"')
        v5, v7 = it.get(5), it.get(7)
        if not _empty(v7):
            pre = _content(v7.split('người ký')[0]).strip(' ;,.—–-')
            if not re.search(r'\w', pre) or PLACEHOLDER_RE.match(pre):
                add('MISSING_ITEM', 'mục 7 thiếu nội dung dự đoán trước "người ký"')
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
            if pd is not None and today is not None and pd > today:
                add('PRED_FUTURE_SIGN', f'ngày ký dự đoán {pd} sau hôm nay {today}')
    return out


def _cells(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]


HEADER_ALIASES = {'nhan': 'nhãn', 'nguon so': 'nguồn số'}


def _hdr_key(cell):
    k = re.sub(r'\s+', ' ', _nfc(cell).strip().strip('*').strip()).casefold()
    return HEADER_ALIASES.get(k, k)


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
            hdr = [_hdr_key(c) for c in _cells(block[0])]
            has_l, has_s = 'nhãn' in hdr, 'nguồn số' in hdr
            if has_l != has_s:
                out.append(Finding('BANG', i + 1, 'PARTIAL_HEADER',
                                   'bảng chỉ có một trong hai cột Nhãn / Nguồn số'))
            if has_l and has_s:
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
    if a.kind == 'hypo':
        fs = lint_sheets(text, today=date.today(), allow_unsigned=a.allow_unsigned)
    else:
        fs = lint_param_table(text)
    for f in fs:
        print(f'{f.sheet}:L{f.line} {f.code} {f.msg}')
    return 1 if fs else 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
