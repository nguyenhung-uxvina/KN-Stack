#!/usr/bin/env python3
"""p3_form_ref_check - kiem con tro sach trong references cua helix-p3-form.

Usage: python -X utf8 scripts/p3_form_ref_check.py <thu-muc-references>
           [--sample 0.1 --seed N --out <tep>]
Sach (env ghi de): P3F_BOOK_TKHT, P3F_BOOK_TKKTHT, P3F_BOOK_TKKTHT2, P3F_BOOK_KL9.
TKKTHT/TKKTHT2 la THU MUC chua Ch*_v2.md; TKHT/KL9 la tep book.md.
Exit: 0 sach, 1 co finding, 2 loi doc tep, 3 thieu sach.

Ma loi:
  CHAPTER_NOT_FOUND  [SACH ChNN] ma sach khong co tieu de "Chuong NN"
  SECTION_NOT_FOUND  §x.y khong co tieu de muc trong chuong do
  QUOTE_NOT_FOUND    “...” / «...» (>= 8 tu; doan quanh … >= 4 tu) khong co nguyen van
  UNCITED_ROW        dong bang du lieu khong co trich va khong co [ngoai sach]
  NO_CITATION        tep co < 5 trich nguon
"""
import glob
import os
import random
import re
import sys
import unicodedata
from collections import namedtuple

Finding = namedtuple('Finding', 'file line code msg')

DEFAULT_BOOKS = {
    'TKHT': 'D:/Workshop_X/3_Resources/Books/thiet-ke-hien-than/book.md',
    'TKKTHT': 'D:/Workshop_X/3_Resources/Books/thiet-ke-ky-thuat-he-thong/Phase6-Revised-Tap1',
    'TKKTHT2': 'D:/Workshop_X/3_Resources/Books/thiet-ke-ky-thuat-he-thong/Phase6-Revised-Tap2',
    'KL9': 'D:/Workshop_X/3_Resources/Books/pahl-beitz-konstruktionslehre/book.md',
}
ENV = {k: 'P3F_BOOK_' + k for k in DEFAULT_BOOKS}

CITE_RE = re.compile(r'\[(TKHT|TKKTHT2|TKKTHT|KL9)\s+Ch(\d{2}[a-z]?)'
                     r'(?:\s*§\s*([0-9]{1,2}[a-z]?(?:\.[0-9]+[a-z]?)+))?\]')
HEAD_RE = re.compile(r'^#{1,6}\s+Chương\s+(\d{2}[a-z]?)(?![0-9a-z])', re.M)
SEC_HEAD_RE = re.compile(r'^#{2,4}\s+([0-9]{1,2}[a-z]?(?:\.[0-9]+[a-z]?)*)(?=[\s—–:.-]|$)', re.M)
QUOTE_RE = re.compile(r'“([^“”\n]+)”|«([^«»\n]+)»')
SEP_ROW_RE = re.compile(r'^\s*\|[\s:|-]+\|?\s*$')
OUT_OF_BOOK = '[ngoài sách]'
MIN_QUOTE_WORDS = 8
MIN_FRAGMENT_WORDS = 4
MIN_CITATIONS = 5
SAMPLE_WORDS = 400


def norm(text):
    """NFC + gop khoang trang. KHONG bo dau."""
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', text)).strip()


def _read(path):
    with open(path, encoding='utf-8-sig') as f:
        return unicodedata.normalize('NFC', f.read())


def _book_files(path):
    if os.path.isdir(path):
        return sorted(glob.glob(os.path.join(path, 'Ch*_v2.md')))
    return [path]


def load_book(path):
    """Cat sach (tep hoac thu muc Ch*_v2.md) theo tieu de chuong.
    -> {chapter_id: {'text': str, 'sections': set, 'sec_text': {tok: str}}}"""
    raw = '\n'.join(_read(p) for p in _book_files(path))
    heads = list(HEAD_RE.finditer(raw))
    chapters = {}
    for i, h in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(raw)
        body = raw[h.start():end]
        ch = chapters.setdefault(h.group(1), {'text': '', 'sections': set(), 'sec_text': {}})
        ch['text'] += ' ' + norm(body)
        secs = list(SEC_HEAD_RE.finditer(body))
        for j, s in enumerate(secs):
            send = secs[j + 1].start() if j + 1 < len(secs) else len(body)
            ch['sections'].add(s.group(1))
            ch['sec_text'].setdefault(s.group(1), norm(body[s.start():send]))
    return chapters


def _fragments(q):
    qn = norm(q)
    if '…' in qn:
        frs = [norm(x) for x in qn.split('…')]
        return [x for x in frs if len(x.split()) >= MIN_FRAGMENT_WORDS]
    return [qn] if len(qn.split()) >= MIN_QUOTE_WORDS else []


def _scan(path, books, cites_out=None):
    rel = os.path.basename(path)
    lines = _read(path).splitlines()
    out = []
    n_cite = 0
    for ln, line in enumerate(lines, 1):
        cites = CITE_RE.findall(line)
        n_cite += len(cites)
        for book, ch, sec in cites:
            chap = books[book].get(ch)
            if chap is None:
                out.append(Finding(rel, ln, 'CHAPTER_NOT_FOUND',
                                   f'[{book} Ch{ch}]: sách {book} không có tiêu đề «Chương {ch}»'))
            elif sec and sec not in chap['sections']:
                out.append(Finding(rel, ln, 'SECTION_NOT_FOUND',
                                   f'[{book} Ch{ch} §{sec}]: chương không có tiêu đề mục {sec}'))
        if cites and cites_out is not None:
            cites_out.append((rel, ln, line, cites))
        pairs = sorted({(b, c) for b, c, _ in cites})
        for m in QUOTE_RE.finditer(line):
            q = m.group(1) or m.group(2)
            frs = _fragments(q)
            if not frs:
                continue
            if not pairs:
                out.append(Finding(rel, ln, 'QUOTE_NOT_FOUND',
                                   f'trích «{norm(q)[:40]}…» không có [SÁCH ChNN] trên cùng dòng'))
                continue
            texts = [books[b][c]['text'] for b, c in pairs if c in books[b]]
            for fr in frs:
                if not any(fr in tx for tx in texts):
                    where = ', '.join(f'{b} Ch{c}' for b, c in pairs)
                    out.append(Finding(rel, ln, 'QUOTE_NOT_FOUND',
                                       f'«{fr[:50]}…» không có nguyên văn trong {where}'))
        # dong bang du lieu
        if line.lstrip().startswith('|') and not SEP_ROW_RE.match(line):
            nxt = lines[ln] if ln < len(lines) else ''
            is_header = bool(SEP_ROW_RE.match(nxt))
            if not is_header and not cites and OUT_OF_BOOK not in line:
                out.append(Finding(rel, ln, 'UNCITED_ROW',
                                   'dòng bảng không có trích nguồn và không có [ngoài sách]'))
    if n_cite < MIN_CITATIONS:
        out.append(Finding(rel, 1, 'NO_CITATION',
                           f'chỉ có {n_cite} trích nguồn, cần ≥ {MIN_CITATIONS}'))
    return out


def check_file(path, books):
    return _scan(path, books)


def _ref_files(ref_dir):
    return [os.path.join(ref_dir, n) for n in sorted(os.listdir(ref_dir)) if n.endswith('.md')]


def _target_text(books, book, ch, sec):
    chap = books[book].get(ch)
    if chap is None:
        return '(chương không tồn tại)'
    txt = chap['sec_text'].get(sec) if sec else None
    txt = txt if txt is not None else chap['text'].strip()
    return ' '.join(txt.split()[:SAMPLE_WORDS])


def write_sample(ref_dir, books, frac, seed, out_path):
    rnd = random.Random(seed)
    blocks = []
    for p in _ref_files(ref_dir):
        found = []
        _scan(p, books, found)
        for rel, ln, line, cites in found:
            if rnd.random() < frac:
                parts = [f'=== {rel}:L{ln}', line.strip()]
                for book, ch, sec in cites:
                    parts.append(f'--- {book} Ch{ch}' + (f' §{sec}' if sec else ''))
                    parts.append(_target_text(books, book, ch, sec))
                blocks.append('\n'.join(parts))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(blocks) + ('\n' if blocks else ''))
    return len(blocks)


def _parse(argv):
    a = {'ref_dir': None, 'sample': None, 'seed': None, 'out': None}
    i = 0
    try:
        while i < len(argv):
            t = argv[i]
            if t in ('--sample', '--seed', '--out'):
                v = argv[i + 1]
                a[t[2:]] = float(v) if t == '--sample' else int(v) if t == '--seed' else v
                i += 2
            elif a['ref_dir'] is None and not t.startswith('--'):
                a['ref_dir'] = t
                i += 1
            else:
                return None
    except (IndexError, ValueError):
        return None
    return a if a['ref_dir'] else None


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    a = _parse(argv)
    if a is None:
        print(__doc__)
        return 2
    ref_dir = a['ref_dir']
    paths = {k: os.environ.get(ENV[k], DEFAULT_BOOKS[k]) for k in DEFAULT_BOOKS}
    missing = [f'{k}={p}' for k, p in paths.items()
               if not (os.path.exists(p) and _book_files(p)
                       and all(os.path.isfile(x) for x in _book_files(p)))]
    if missing:
        print('không có sách — không kiểm được: ' + ', '.join(missing))
        return 3
    if not os.path.isdir(ref_dir):
        print(f'ERROR không có thư mục: {ref_dir}', file=sys.stderr)
        return 2
    try:
        books = {k: load_book(p) for k, p in paths.items()}
        fs = []
        for p in _ref_files(ref_dir):
            fs.extend(check_file(p, books))
        if a['sample'] is not None:
            out = a['out'] or 'p3f_sample.txt'
            n = write_sample(ref_dir, books, a['sample'], a['seed'], out)
            print(f'đã ghi {n} dòng mẫu vào {out}')
    except (OSError, UnicodeDecodeError) as e:
        print(f'ERROR không đọc được tệp: {e}', file=sys.stderr)
        return 2
    for f in fs:
        print(f'{f.file}:L{f.line} {f.code} {f.msg}')
    if fs:
        print(f'TRƯỢT — {len(fs)} finding')
        return 1
    print(f'ĐẠT — {len(_ref_files(ref_dir))} tệp, mọi trích nguồn và trích nguyên văn khớp sách')
    return 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
