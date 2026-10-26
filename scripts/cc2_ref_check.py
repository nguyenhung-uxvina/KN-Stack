#!/usr/bin/env python3
"""cc2_ref_check - kiem trich nguon cua helix-cc2/references voi hai quyen sach CC/TK.

Usage: python scripts/cc2_ref_check.py <thu-muc-references>
Sach: env CC2_BOOK_CC / CC2_BOOK_TK (mac dinh: D:/Workshop_X/3_Resources/Books/...).
Exit: 0 sach, 1 co finding, 2 loi doc tep, 3 thieu sach (khong kiem duoc).

Ma loi:
  CHAPTER_NOT_FOUND  trich (CC Ch04 ...) ma book.md khong co tieu de chuong 04
  QUOTE_NOT_FOUND    doan «...» >= 8 tu khong co nguyen van trong sach dong do trich
                     (chuan hoa khoang trang + NFC, GIU dau)
  NO_CITATION        tep reference co < 5 trich nguon
"""
import os
import re
import sys
import unicodedata
from collections import namedtuple

Finding = namedtuple('Finding', 'file line code msg')

DEFAULT_BOOKS = {
    'CC': 'D:/Workshop_X/3_Resources/Books/cc2-gia-thuyet-ket-cau/book.md',
    'TK': 'D:/Workshop_X/3_Resources/Books/thiet-ke-hien-than/book.md',
}
ENV = {'CC': 'CC2_BOOK_CC', 'TK': 'CC2_BOOK_TK'}

CITE_RE = re.compile(r'(?<![A-Za-z])(CC|TK)\s+Ch(\d{2}[a-z]?)(?![0-9a-z])')
HEAD_RE = re.compile(r'^#{1,6}\s+Chương\s+(\d{2}[a-z]?)(?![0-9a-z])', re.M)
QUOTE_RE = re.compile(r'«([^«»\n]+)»')
MIN_QUOTE_WORDS = 8
MIN_CITATIONS = 5


def norm(text):
    """NFC + gop khoang trang. KHONG bo dau."""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()


def load_book(path):
    with open(path, encoding='utf-8-sig') as f:
        raw = unicodedata.normalize('NFC', f.read())
    return {'chapters': set(HEAD_RE.findall(raw)), 'text': norm(raw)}


def check_file(path, books):
    rel = os.path.basename(path)
    with open(path, encoding='utf-8-sig') as f:
        lines = unicodedata.normalize('NFC', f.read()).splitlines()
    out = []
    n_cite = 0
    for ln, line in enumerate(lines, 1):
        cites = CITE_RE.findall(line)
        n_cite += len(cites)
        for book, ch in cites:
            if ch not in books[book]['chapters']:
                out.append(Finding(rel, ln, 'CHAPTER_NOT_FOUND',
                                   f'({book} Ch{ch}): sách {book} không có tiêu đề «Chương {ch}»'))
        cited = sorted({b for b, _ in cites})
        for q in QUOTE_RE.findall(line):
            qn = norm(q)
            if len(qn.split()) < MIN_QUOTE_WORDS:
                continue
            if not cited:
                out.append(Finding(rel, ln, 'QUOTE_NOT_FOUND',
                                   f'trích «{qn[:40]}…» không có (CC/TK ChNN) trên cùng dòng'))
            elif not any(qn in books[b]['text'] for b in cited):
                out.append(Finding(rel, ln, 'QUOTE_NOT_FOUND',
                                   f'«{qn[:50]}…» không có nguyên văn trong {"/".join(cited)}'))
    if n_cite < MIN_CITATIONS:
        out.append(Finding(rel, 1, 'NO_CITATION',
                           f'chỉ có {n_cite} trích nguồn, cần ≥ {MIN_CITATIONS}'))
    return out


def check_refs(ref_dir, books):
    loaded = {k: load_book(p) for k, p in books.items()}
    out = []
    for name in sorted(os.listdir(ref_dir)):
        if name.endswith('.md'):
            out.extend(check_file(os.path.join(ref_dir, name), loaded))
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(__doc__)
        return 2
    ref_dir = argv[0]
    books = {k: os.environ.get(ENV[k], DEFAULT_BOOKS[k]) for k in DEFAULT_BOOKS}
    missing = [f'{k}={p}' for k, p in books.items() if not os.path.isfile(p)]
    if missing:
        print('không có sách — không kiểm được: ' + ', '.join(missing))
        return 3
    if not os.path.isdir(ref_dir):
        print(f'ERROR không có thư mục: {ref_dir}', file=sys.stderr)
        return 2
    try:
        fs = check_refs(ref_dir, books)
    except (OSError, UnicodeDecodeError) as e:
        print(f'ERROR không đọc được tệp: {e}', file=sys.stderr)
        return 2
    for f in fs:
        print(f'{f.file}:L{f.line} {f.code} {f.msg}')
    if fs:
        print(f'TRƯỢT — {len(fs)} finding')
        return 1
    n = len([x for x in os.listdir(ref_dir) if x.endswith('.md')])
    print(f'ĐẠT — {n} tệp, mọi trích nguồn và trích nguyên văn khớp sách')
    return 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
