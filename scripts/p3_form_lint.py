#!/usr/bin/env python3
"""p3_form_lint - cong may kiem 4 tep dau ra cua khoi BF (helix-p3-form).

Usage: python -X utf8 scripts/p3_form_lint.py <thu-muc-dau-ra> --prefix <PREFIX> [--quick]
Tep: <P>BF_Form_Variants.md, <P>BF_Benchmark.md, <P>BF_Scoring.md, <P>BF_Form_Selection.md
Exit: 0 sach, 1 co finding, 2 loi dung/doc tep.

Ma loi: MISSING_FILE TOO_FEW_VARIANTS VARIANT_NO_RULE VARIANT_NO_PARAM BAD_LABEL
  BENCH_NO_SOURCE BENCH_NO_DATE BENCH_NO_CHAIN TOO_MANY_BENCH
  CHECKLIST_INCOMPLETE CHECKLIST_SKIP_NO_REASON BAD_CELL QUESTION_NO_REASON
  EMPTY_WEIGHT_NO_FLAG NO_SENSITIVITY CANDIDATE_MISSING
  NO_SELECTION NO_TEST_PLAN NO_PARAM_RANGE
"""
import os
import re
import sys
import unicodedata
from collections import namedtuple

Finding = namedtuple('Finding', 'file line code msg')

CITE_RE = re.compile(r'\[(TKHT|TKKTHT2|TKKTHT|KL9)\s+Ch(\d{2}[a-z]?)'
                     r'(?:\s*§\s*([0-9]{1,2}[a-z]?(?:\.[0-9]+[a-z]?)+))?\]')
LABELS = ('tri thức', 'phỏng đoán', 'giả định')
SRC_RE = re.compile(r'https?://|\b(US|EP|CN|WO|JP|KR|DE)\s?[\d,\s]{5,}\s?[A-Z]\d?\b|[/\\]')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ID_RE = re.compile(r'\b(?:PA|HC)-[A-Za-z0-9]+-\d+\b')
NUM_RE = re.compile(r'^\d+(?:[.,]\d+)?%?$')
SEP_RE = re.compile(r'^\s*\|[\s:|-]+\|?\s*$')
MIN_VARIANTS, MIN_VARIANTS_QUICK, MAX_BENCH = 3, 2, 8

F_HEAD = re.compile(r'^##\s+F-([A-Za-z0-9]+)\b')
PA_HEAD = re.compile(r'^###\s+(PA-[A-Za-z0-9]+-\d+)\b')
HC_HEAD = re.compile(r'^###\s+(HC-([A-Za-z0-9]+)-\d+)\b')
SF_HEAD = re.compile(r'^###\s+F-([A-Za-z0-9]+)\b')


def _read(path):
    with open(path, encoding='utf-8-sig') as f:
        return unicodedata.normalize('NFC', f.read()).splitlines()


def _field(lines, start, end, label):
    """-> (lineno1, value) cua dong 'Label:' trong lines[start:end], hoac None."""
    pat = re.compile(r'^\s*(?:[-*]\s+)?\**' + re.escape(label) + r'\s*:\s*\**\s*(.*?)\s*$')
    for i in range(start, end):
        m = pat.match(lines[i])
        if m:
            return i + 1, m.group(1).strip()
    return None


def _blocks(lines, head_re, lo=0, hi=None):
    """Cac khoi bat dau o dong khop head_re -> [(start, end, match)]."""
    hi = len(lines) if hi is None else hi
    hs = [(i, head_re.match(lines[i])) for i in range(lo, hi) if head_re.match(lines[i])]
    out = []
    for k, (i, m) in enumerate(hs):
        stop = hs[k + 1][0] if k + 1 < len(hs) else hi
        out.append((i, stop, m))
    return out


def _section(lines, title_re):
    """Pham vi (start, end) cua muc '## ...' khop title_re; None neu khong co."""
    for i, ln in enumerate(lines):
        if re.match(r'^##\s+' + title_re, ln):
            for j in range(i + 1, len(lines)):
                if re.match(r'^##\s', lines[j]):
                    return i, j
            return i, len(lines)
    return None


def _label_ok(v):
    return v.strip('`*[]() .') in LABELS


def _cells(row):
    r = row.strip()
    if r.startswith('|'):
        r = r[1:]
    if r.endswith('|'):
        r = r[:-1]
    return [c.strip() for c in r.split('|')]


def lint_variants(path, quick, out):
    rel = os.path.basename(path)
    lines = _read(path)
    ids = {}
    need = MIN_VARIANTS_QUICK if quick else MIN_VARIANTS
    for fs, fe, fm in _blocks(lines, F_HEAD):
        fid = fm.group(1)
        pas = _blocks(lines, PA_HEAD, fs + 1, fe)
        ids[fid] = [m.group(1) for _, _, m in pas]
        if len(pas) < need:
            out.append(Finding(rel, fs + 1, 'TOO_FEW_VARIANTS',
                               f'F-{fid} có {len(pas)} phương án, cần ≥ {need}'))
        for s, e, m in pas:
            pid = m.group(1)
            r = _field(lines, s, e, 'Nguồn quy tắc')
            if not r or not CITE_RE.search(r[1]):
                out.append(Finding(rel, s + 1, 'VARIANT_NO_RULE',
                                   f'{pid}: thiếu trích «Nguồn quy tắc:» dạng [SÁCH ChNN §x.y]'))
            r = _field(lines, s, e, 'Tham số khoá')
            if not r or not r[1]:
                out.append(Finding(rel, s + 1, 'VARIANT_NO_PARAM', f'{pid}: «Tham số khoá:» rỗng'))
            r = _field(lines, s, e, 'Nhãn')
            if not r or not _label_ok(r[1]):
                out.append(Finding(rel, s + 1, 'BAD_LABEL',
                                   f'{pid}: «Nhãn:» phải là tri thức / phỏng đoán / giả định'))
    return ids


def lint_benchmark(path, out):
    rel = os.path.basename(path)
    lines = _read(path)
    ids = {}
    for s, e, m in _blocks(lines, HC_HEAD):
        hid, fid = m.group(1), m.group(2)
        ids.setdefault(fid, []).append(hid)
        r = _field(lines, s, e, 'Nguồn')
        if not r or not SRC_RE.search(r[1]):
            out.append(Finding(rel, s + 1, 'BENCH_NO_SOURCE',
                               f'{hid}: «Nguồn:» không phải URL / số công bố / đường dẫn'))
        r = _field(lines, s, e, 'Truy cập')
        if not r or not DATE_RE.match(r[1]):
            out.append(Finding(rel, s + 1, 'BENCH_NO_DATE', f'{hid}: «Truy cập:» phải là YYYY-MM-DD'))
        r = _field(lines, s, e, 'Nhãn')
        if not r or not _label_ok(r[1]):
            out.append(Finding(rel, s + 1, 'BAD_LABEL',
                               f'{hid}: «Nhãn:» phải là tri thức / phỏng đoán / giả định'))
        r = _field(lines, s, e, 'Chuỗi C&C²')
        if not r or not r[1]:
            out.append(Finding(rel, s + 1, 'BENCH_NO_CHAIN', f'{hid}: «Chuỗi C&C²:» rỗng'))
    for fid, hs in ids.items():
        if len(hs) > MAX_BENCH:
            out.append(Finding(rel, 1, 'TOO_MANY_BENCH', f'F-{fid} có {len(hs)} HC, tối đa {MAX_BENCH}'))
    return ids


def _checklist(lines, rel, out):
    sec = _section(lines, r'Checklist 14 mục')
    if sec is None:
        out.append(Finding(rel, 1, 'CHECKLIST_INCOMPLETE', 'thiếu mục «## Checklist 14 mục»'))
        return
    seen = {}
    for i in range(sec[0] + 1, sec[1]):
        ln = lines[i]
        if not ln.lstrip().startswith('|') or SEP_RE.match(ln):
            continue
        c = _cells(ln)
        if c and c[0].isdigit():
            seen[int(c[0])] = (i + 1, c)
    for n in range(1, 15):
        if n not in seen:
            out.append(Finding(rel, sec[0] + 1, 'CHECKLIST_INCOMPLETE', f'thiếu dòng số {n}'))
            continue
        ln, c = seen[n]
        rest = c[1:]
        skip = [x for x in rest if x.startswith('Bỏ')]
        if skip:
            if not re.search(r'Bỏ\s*[—–-]\s*lý do:\s*\S', skip[0]):
                out.append(Finding(rel, ln, 'CHECKLIST_SKIP_NO_REASON',
                                   f'mục {n}: «Bỏ» thiếu «— lý do: …»'))
        elif not rest or not rest[-1]:
            out.append(Finding(rel, ln, 'CHECKLIST_INCOMPLETE', f'mục {n}: thiếu tiêu chí'))


def _q_cell(v):
    """'ok' | 'noreason' | None neu khong phai o '?(...)'."""
    if not v.startswith('?'):
        return None
    m = re.match(r'^\?\((.*)\)$', v)
    return 'ok' if m and m.group(1).strip() else 'noreason'


def _scoring_tables(lines, rel, ids_by_f, out):
    sec = _section(lines, r'Bảng chấm')
    if sec is None:
        out.append(Finding(rel, 1, 'CANDIDATE_MISSING', 'thiếu mục «## Bảng chấm»'))
        return
    got = {}
    for s, e, m in _blocks(lines, SF_HEAD, sec[0] + 1, sec[1]):
        fid = m.group(1)
        header = None
        for i in range(s + 1, e):
            ln = lines[i]
            if not ln.lstrip().startswith('|') or SEP_RE.match(ln):
                continue
            c = _cells(ln)
            if header is None:
                if c and c[0] == 'Req-ID':
                    header = c
                    got[fid] = {x for cell in c[4:-1] for x in ID_RE.findall(cell)}
                continue
            if len(c) != len(header):
                out.append(Finding(rel, i + 1, 'BAD_CELL',
                                   f'F-{fid}: dòng có {len(c)} ô, tiêu đề có {len(header)}'))
                continue
            dw = c[1].replace('tạm', '').strip()
            if dw not in ('D', 'W'):
                out.append(Finding(rel, i + 1, 'BAD_CELL', f'{c[0]}: D/W «{c[1]}» không hợp lệ'))
                continue
            w = c[3]
            if w == '':
                if '🔴' not in ln:
                    out.append(Finding(rel, i + 1, 'EMPTY_WEIGHT_NO_FLAG',
                                       f'{c[0]}: Trọng số trống mà dòng không có 🔴'))
            elif not NUM_RE.match(w):
                out.append(Finding(rel, i + 1, 'BAD_CELL', f'{c[0]}: Trọng số «{w}» không phải số'))
            for name, v in zip(header[4:-1], c[4:-1]):
                q = _q_cell(v)
                if q == 'noreason':
                    out.append(Finding(rel, i + 1, 'QUESTION_NO_REASON',
                                       f'{c[0]}/{name}: «?(…)» không có lý do'))
                elif q is None:
                    ok = v in ('Đạt', 'Loại') if dw == 'D' else bool(re.fullmatch(r'[0-4]', v))
                    if not ok:
                        out.append(Finding(rel, i + 1, 'BAD_CELL',
                                           f'{c[0]}/{name}: ô «{v}» không hợp lệ cho dòng {dw}'))
        if header is None:
            out.append(Finding(rel, s + 1, 'BAD_CELL', f'F-{fid}: không thấy bảng có cột Req-ID'))
    for fid, want in ids_by_f.items():
        have = got.get(fid)
        if have is None:
            out.append(Finding(rel, sec[0] + 1, 'CANDIDATE_MISSING', f'thiếu bảng «### F-{fid}»'))
            continue
        for x in sorted(set(want) - have):
            out.append(Finding(rel, sec[0] + 1, 'CANDIDATE_MISSING', f'F-{fid}: cột ứng viên thiếu {x}'))


def lint_scoring(path, ids_by_f, out):
    rel = os.path.basename(path)
    lines = _read(path)
    _checklist(lines, rel, out)
    _scoring_tables(lines, rel, ids_by_f, out)
    if _section(lines, r'Độ nhạy') is None:
        out.append(Finding(rel, 1, 'NO_SENSITIVITY', 'thiếu mục «## Độ nhạy»'))


def lint_selection(path, out):
    rel = os.path.basename(path)
    lines = _read(path)
    blocks = _blocks(lines, F_HEAD)
    if not blocks:
        out.append(Finding(rel, 1, 'NO_SELECTION', 'không có mục «## F-<id>»'))
    for s, e, m in blocks:
        fid = m.group(1)
        r = _field(lines, s, e, 'Chọn')
        if not r or not re.search(r'\b(?:PA|HC)-[A-Za-z0-9]+-\d+', r[1]):
            out.append(Finding(rel, s + 1, 'NO_SELECTION', f'F-{fid}: thiếu «Chọn: PA-…/HC-…»'))
        r = _field(lines, s, e, 'Khoảng tham số')
        if not r or not r[1]:
            out.append(Finding(rel, s + 1, 'NO_PARAM_RANGE', f'F-{fid}: «Khoảng tham số:» rỗng'))
        r = _field(lines, s, e, 'Kế hoạch thử')
        if not r or not r[1]:
            out.append(Finding(rel, s + 1, 'NO_TEST_PLAN', f'F-{fid}: «Kế hoạch thử:» rỗng'))


def lint_dir(path, prefix, quick=False):
    out = []
    names = {k: f'{prefix}BF_{k}.md' for k in ('Form_Variants', 'Benchmark', 'Scoring', 'Form_Selection')}
    present = {}
    for k, n in names.items():
        p = os.path.join(path, n)
        if os.path.isfile(p):
            present[k] = p
        else:
            out.append(Finding(n, 0, 'MISSING_FILE', f'thiếu tệp {n}'))
    ids = {}
    if 'Form_Variants' in present:
        for f, v in lint_variants(present['Form_Variants'], quick, out).items():
            ids.setdefault(f, []).extend(v)
    if 'Benchmark' in present:
        for f, v in lint_benchmark(present['Benchmark'], out).items():
            ids.setdefault(f, []).extend(v)
    if 'Scoring' in present:
        lint_scoring(present['Scoring'], ids, out)
    if 'Form_Selection' in present:
        lint_selection(present['Form_Selection'], out)
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    d, prefix, quick, i = None, None, False, 0
    while i < len(argv):
        t = argv[i]
        if t == '--prefix' and i + 1 < len(argv):
            prefix = argv[i + 1]
            i += 2
        elif t == '--quick':
            quick = True
            i += 1
        elif d is None and not t.startswith('--'):
            d = t
            i += 1
        else:
            print(__doc__)
            return 2
    if d is None or prefix is None:
        print(__doc__)
        return 2
    if not os.path.isdir(d):
        print(f'ERROR không có thư mục: {d}', file=sys.stderr)
        return 2
    try:
        fs = lint_dir(d, prefix, quick)
    except (OSError, UnicodeDecodeError) as e:
        print(f'ERROR không đọc được tệp: {e}', file=sys.stderr)
        return 2
    for f in fs:
        print(f'{f.file}:L{f.line} {f.code} {f.msg}')
    if fs:
        print(f'TRƯỢT — {len(fs)} finding')
        return 1
    print('ĐẠT — 4 tệp BF đúng khuôn')
    return 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
