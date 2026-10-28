#!/usr/bin/env python3
"""p3_form_lint - cong may kiem 4 tep dau ra cua khoi BF (helix-p3-form).

Usage: python -X utf8 scripts/p3_form_lint.py <thu-muc-dau-ra> --prefix <PREFIX>
         [--quick] [--draft] [--refs <thu-muc-references>]
Tep: <P>BF_Form_Variants.md, <P>BF_Benchmark.md, <P>BF_Scoring.md, <P>BF_Form_Selection.md
Exit: 0 sach, 1 co finding, 2 loi dung/doc tep.

--refs: thu muc references cua helix-p3-form (mac dinh
<thu muc script>/../skills/helix/helix-p3-form/references). Moi dong «Nguồn quy tắc:»
phai co >=1 ma (TKHT-R|PB-R|PB-M|KL-R)nnn co trong references, va moi con tro
[SACH ChNN §x.y] tren dong phai nam trong dong bang cua mot ma tren cung dong.
Moi «[TKHT|TKKTHT|TKKTHT2|KL9 …]» (khong phan biet hoa thuong) phai khop CHINH XAC khuon
CITE_RE (vd «[TKHT Ch13b §13b.9]»); sai khuon (thua «, tr.12», «§99» thieu phan thap phan,
khoang trang thua, viet thuong, nhieu sach trong mot dau []) -> CITATION_MALFORMED.

--draft: Selection nhap truoc Cong CEO 2 — «Chọn: (chờ CEO)», KHONG ghi ma ung vien.
Mac dinh (chinh thuc, sau Cong CEO 2): «Chọn: <PA-/HC-id> — <ten>», «Lý do CEO:» khong
rong moi F, va dung mot dong «Cổng CEO 2 — ngày YYYY-MM-DD»; cam «chờ CEO»/«đề xuất».

Checklist: «## Checklist 14 mục» co mot bang «### F-<id>» moi chuc nang:
| # | Mục | Tiêu chí | <moi PA/HC cua F> |, dong 1–14; o ung vien ∈ {Đạt, Không đạt, ?(ly do)};
dong bo: Tiêu chí = «Bỏ — lý do: …», moi o ung vien «—».
Bang cham: dong D duoc de trong Trọng số; dong W trong thi phai co 🔴.
PA/HC phai nam duoi «## F-<id>» trung F trong ma (ID_BLOCK_MISMATCH).

Loi ra NO_BENCH co ly do: chuc nang khong co HC nao van sach neu trong khoi
«## F-<id> — …» cua <P>BF_Benchmark.md co dong
«Không tìm thấy HC — lý do: <ly do khong rong>» (cho phep tien to «- »).
Ly do rong -> NO_BENCH. Khi khong co HC, bang cham cua F do chi can cot PA.

Ma loi: MISSING_FILE TOO_FEW_VARIANTS VARIANT_NO_RULE VARIANT_NO_PARAM BAD_LABEL
  RULE_CODE_MISSING RULE_CODE_UNKNOWN CITATION_NOT_IN_RULE CITATION_MALFORMED ID_BLOCK_MISMATCH
  BENCH_NO_SOURCE BENCH_NO_DATE BENCH_NO_CHAIN TOO_MANY_BENCH
  CHECKLIST_INCOMPLETE CHECKLIST_SKIP_NO_REASON CHECKLIST_CANDIDATE_MISSING
  BAD_CELL QUESTION_NO_REASON EMPTY_WEIGHT_NO_FLAG NO_SENSITIVITY CANDIDATE_MISSING
  NO_SELECTION NO_TEST_PLAN NO_PARAM_RANGE NO_BENCH NO_SCORING_TABLE
  SELECTION_DRAFT SELECTION_NO_NAME NO_CEO_REASON NO_GATE2_DATE
"""
import os
import re
import sys
import unicodedata
from collections import namedtuple

Finding = namedtuple('Finding', 'file line code msg')

CITE_RE = re.compile(r'\[(TKHT|TKKTHT2|TKKTHT|KL9)\s+Ch(\d{2}[a-z]?)'
                     r'(?:\s*§\s*([0-9]{1,2}[a-z]?(?:\.[0-9]+[a-z]?)+))?\]')
BOOKISH_RE = re.compile(r'\[(?:TKHT|TKKTHT2?|KL9)\b[^\]]*\]', re.I)
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
CODE_RE = re.compile(r'\b(?:TKHT-R|PB-R|PB-M|KL-R)\d{3}\b')
CODE_ROW_RE = re.compile(r'^\|\s*((?:TKHT-R|PB-R|PB-M|KL-R)\d{3})\s*\|')
GATE2_RE = re.compile(r'^\s*\**\s*Cổng CEO 2\s*[—–-]\s*ngày\b\s*(.*)$')
GATE2_OK = re.compile(r'^\d{4}-\d{2}-\d{2}\b')
PICK_RE = re.compile(r'^((?:PA|HC)-[A-Za-z0-9]+-\d+)\s+—\s*(.*?)\s*$')
PENDING_RE = re.compile(r'chờ CEO|đề xuất', re.I)
CK_CELLS = ('Đạt', 'Không đạt')
DEFAULT_REFS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '..', 'skills', 'helix', 'helix-p3-form', 'references')
NOHC_RE = re.compile(r'^\s*(?:[-*]\s+)?\**Không tìm thấy HC\s*[—–-]\s*lý do\s*:\s*\**\s*(.*?)\s*$')


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


def load_rule_index(refs):
    """{ma: set((sach, chuong, muc))} tu cac dong bang «| MA | …» trong refs/*.md."""
    if not os.path.isdir(refs):
        raise FileNotFoundError(f'không có thư mục references: {refs}')
    idx = {}
    for n in sorted(os.listdir(refs)):
        if not n.endswith('.md'):
            continue
        for ln in _read(os.path.join(refs, n)):
            m = CODE_ROW_RE.match(ln)
            if m:
                idx.setdefault(m.group(1), set()).update(CITE_RE.findall(ln))
    return idx


def _fmt_cite(c):
    b, ch, s = c
    return f'[{b} Ch{ch}' + (f' §{s}' if s else '') + ']'


def _check_rule_line(rel, lineno, pid, value, idx, out):
    for tok in BOOKISH_RE.findall(value):
        if not CITE_RE.fullmatch(tok):
            out.append(Finding(rel, lineno, 'CITATION_MALFORMED',
                               f'{pid}: {tok} sai khuôn, phải là [SÁCH ChNN §x.y]'))
    found = list(dict.fromkeys(CODE_RE.findall(value)))
    if not found:
        out.append(Finding(rel, lineno, 'RULE_CODE_MISSING',
                           f'{pid}: «Nguồn quy tắc:» thiếu mã quy tắc (TKHT-R|PB-R|PB-M|KL-R)nnn'))
        return
    for c in found:
        if c not in idx:
            out.append(Finding(rel, lineno, 'RULE_CODE_UNKNOWN',
                               f'{pid}: mã {c} không có trong references'))
    known = [c for c in found if c in idx]
    if not known:
        return
    allowed = set().union(*(idx[c] for c in known))
    for c in CITE_RE.findall(value):
        if c not in allowed:
            out.append(Finding(rel, lineno, 'CITATION_NOT_IN_RULE',
                               f'{pid}: {_fmt_cite(c)} không nằm trong dòng của {", ".join(known)}'))


def _id_blocks(lines, rel, head_re, out):
    """PA/HC phai nam duoi «## F-<id>» trung voi F trong ma cua no."""
    cur = None
    for i, ln in enumerate(lines):
        fm = F_HEAD.match(ln)
        if fm:
            cur = fm.group(1)
            continue
        m = head_re.match(ln)
        if m:
            own = re.match(r'(?:PA|HC)-([A-Za-z0-9]+)-', m.group(1)).group(1)
            if own != cur:
                where = f'«## F-{cur}»' if cur else 'ngoài mọi khối «## F-»'
                out.append(Finding(rel, i + 1, 'ID_BLOCK_MISMATCH',
                                   f'{m.group(1)} nằm ở {where}, phải ở «## F-{own}»'))


def lint_variants(path, quick, out, idx=None):
    rel = os.path.basename(path)
    lines = _read(path)
    ids = {}
    need = MIN_VARIANTS_QUICK if quick else MIN_VARIANTS
    fblocks = _blocks(lines, F_HEAD)
    _id_blocks(lines, rel, PA_HEAD, out)
    if not fblocks:
        out.append(Finding(rel, 1, 'TOO_FEW_VARIANTS', 'không có khối «## F-<id>» nào — không có phương án'))
    for fs, fe, fm in fblocks:
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
            if r and idx is not None:
                _check_rule_line(rel, r[0], pid, r[1], idx, out)
            r = _field(lines, s, e, 'Tham số khoá')
            if not r or not r[1]:
                out.append(Finding(rel, s + 1, 'VARIANT_NO_PARAM', f'{pid}: «Tham số khoá:» rỗng'))
            r = _field(lines, s, e, 'Nhãn')
            if not r or not _label_ok(r[1]):
                out.append(Finding(rel, s + 1, 'BAD_LABEL',
                                   f'{pid}: «Nhãn:» phải là tri thức / phỏng đoán / giả định'))
    return ids


def lint_benchmark(path, f_ids, out):
    rel = os.path.basename(path)
    lines = _read(path)
    ids = {}
    _id_blocks(lines, rel, HC_HEAD, out)
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
    nohc = {}
    for s, e, m in _blocks(lines, F_HEAD):
        for i in range(s + 1, e):
            mm = NOHC_RE.match(lines[i])
            if mm:
                nohc[m.group(1)] = (i + 1, mm.group(1).strip('* '))
                break
    for fid in f_ids:
        if not ids.get(fid):
            r = nohc.get(fid)
            if r and r[1]:
                continue
            if r:
                out.append(Finding(rel, r[0], 'NO_BENCH',
                                   f'F-{fid}: «Không tìm thấy HC — lý do:» rỗng'))
            else:
                out.append(Finding(rel, 1, 'NO_BENCH',
                                   f'F-{fid} không có HC nào (cần 1–{MAX_BENCH}, hoặc dòng '
                                   f'«Không tìm thấy HC — lý do: …» trong «## F-{fid}»)'))
    for fid, hs in ids.items():
        if len(hs) > MAX_BENCH:
            out.append(Finding(rel, 1, 'TOO_MANY_BENCH', f'F-{fid} có {len(hs)} HC, tối đa {MAX_BENCH}'))
    return ids


def _checklist(lines, rel, ids_by_f, out):
    sec = _section(lines, r'Checklist 14 mục')
    if sec is None:
        out.append(Finding(rel, 1, 'CHECKLIST_INCOMPLETE', 'thiếu mục «## Checklist 14 mục»'))
        return
    got = set()
    for s, e, m in _blocks(lines, SF_HEAD, sec[0] + 1, sec[1]):
        fid = m.group(1)
        got.add(fid)
        header, seen = None, {}
        for i in range(s + 1, e):
            ln = lines[i]
            if not ln.lstrip().startswith('|') or SEP_RE.match(ln):
                continue
            c = _cells(ln)
            if header is None:
                if len(c) >= 3 and c[0] == '#':
                    header = c
                continue
            if len(c) != len(header):
                out.append(Finding(rel, i + 1, 'BAD_CELL',
                                   f'checklist F-{fid}: dòng có {len(c)} ô, tiêu đề có {len(header)}'))
                continue
            if not c[0].isdigit() or not 1 <= int(c[0]) <= 14:
                out.append(Finding(rel, i + 1, 'CHECKLIST_INCOMPLETE',
                                   f'checklist F-{fid}: số mục «{c[0]}» ngoài 1–14'))
                continue
            seen[int(c[0])] = (i + 1, c)
        if header is None:
            out.append(Finding(rel, s + 1, 'CHECKLIST_INCOMPLETE',
                               f'checklist F-{fid}: không thấy bảng «# | Mục | Tiêu chí | …»'))
            continue
        cols = {x for cell in header[3:] for x in ID_RE.findall(cell)}
        for x in sorted(set(ids_by_f.get(fid, [])) - cols):
            out.append(Finding(rel, s + 1, 'CHECKLIST_CANDIDATE_MISSING',
                               f'checklist F-{fid}: thiếu cột ứng viên {x}'))
        for n in range(1, 15):
            if n not in seen:
                out.append(Finding(rel, s + 1, 'CHECKLIST_INCOMPLETE',
                                   f'checklist F-{fid}: thiếu dòng số {n}'))
                continue
            ln, c = seen[n]
            crit, cand = c[2], c[3:]
            if crit.startswith('Bỏ'):
                if not re.match(r'^Bỏ\s*[—–-]\s*lý do:\s*\S', crit):
                    out.append(Finding(rel, ln, 'CHECKLIST_SKIP_NO_REASON',
                                       f'checklist F-{fid} mục {n}: «Bỏ» thiếu «— lý do: …»'))
                if any(v != '—' for v in cand):
                    out.append(Finding(rel, ln, 'BAD_CELL',
                                       f'checklist F-{fid} mục {n}: dòng bỏ thì mọi ô ứng viên là «—»'))
                continue
            if not crit:
                out.append(Finding(rel, ln, 'CHECKLIST_INCOMPLETE',
                                   f'checklist F-{fid} mục {n}: thiếu tiêu chí'))
            for name, v in zip(header[3:], cand):
                q = _q_cell(v)
                if q == 'noreason':
                    out.append(Finding(rel, ln, 'QUESTION_NO_REASON',
                                       f'checklist F-{fid} mục {n}/{name}: «?(…)» không có lý do'))
                elif q is None and v not in CK_CELLS:
                    out.append(Finding(rel, ln, 'BAD_CELL',
                                       f'checklist F-{fid} mục {n}/{name}: ô «{v}» phải là '
                                       f'Đạt / Không đạt / ?(lý do)'))
    for fid in ids_by_f:
        if fid not in got:
            out.append(Finding(rel, sec[0] + 1, 'CHECKLIST_INCOMPLETE',
                               f'thiếu bảng checklist «### F-{fid}»'))


def _q_cell(v):
    """'ok' | 'noreason' | None neu khong phai o '?(...)'."""
    if not v.startswith('?'):
        return None
    m = re.match(r'^\?\((.*)\)$', v)
    return 'ok' if m and m.group(1).strip() else 'noreason'


def _scoring_tables(lines, rel, ids_by_f, out):
    sec = _section(lines, r'Bảng chấm')
    if sec is None:
        out.append(Finding(rel, 1, 'NO_SCORING_TABLE', 'thiếu mục «## Bảng chấm»'))
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
                if dw == 'W' and '🔴' not in ln:
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
    _checklist(lines, rel, ids_by_f, out)
    _scoring_tables(lines, rel, ids_by_f, out)
    if _section(lines, r'Độ nhạy') is None:
        out.append(Finding(rel, 1, 'NO_SENSITIVITY', 'thiếu mục «## Độ nhạy»'))


def lint_selection(path, ids_by_f, out, draft=False):
    rel = os.path.basename(path)
    lines = _read(path)
    blocks = _blocks(lines, F_HEAD)
    if not blocks:
        out.append(Finding(rel, 1, 'NO_SELECTION', 'không có mục «## F-<id>»'))
    have = {m.group(1) for _, _, m in blocks}
    for fid in ids_by_f:
        if fid not in have:
            out.append(Finding(rel, 1, 'NO_SELECTION', f'F-{fid}: thiếu khối «## F-{fid}»'))
    if not draft:
        g2 = [(i + 1, GATE2_RE.match(ln).group(1)) for i, ln in enumerate(lines) if GATE2_RE.match(ln)]
        if len(g2) != 1:
            out.append(Finding(rel, 1, 'NO_GATE2_DATE',
                               f'cần đúng một dòng «Cổng CEO 2 — ngày YYYY-MM-DD» (đang có {len(g2)})'))
        elif not GATE2_OK.match(g2[0][1]):
            out.append(Finding(rel, g2[0][0], 'NO_GATE2_DATE',
                               '«Cổng CEO 2 — ngày …» phải ghi ngày YYYY-MM-DD'))
    for s, e, m in blocks:
        fid = m.group(1)
        r = _field(lines, s, e, 'Chọn')
        v = r[1] if r else ''
        picked = ID_RE.findall(v)
        if draft:
            if picked:
                out.append(Finding(rel, r[0], 'SELECTION_DRAFT',
                                   f'F-{fid}: bản nháp (--draft) không ghi mã ứng viên trong «Chọn:» '
                                   f'— ghi «Chọn: (chờ CEO)»'))
            elif not PENDING_RE.search(v):
                out.append(Finding(rel, s + 1, 'NO_SELECTION',
                                   f'F-{fid}: bản nháp cần «Chọn: (chờ CEO)»'))
        else:
            if PENDING_RE.search(v):
                out.append(Finding(rel, r[0], 'SELECTION_DRAFT',
                                   f'F-{fid}: «Chọn:» còn «chờ CEO»/«đề xuất» — chưa qua Cổng CEO 2'))
            if picked and fid in ids_by_f:
                bad = [x for x in picked if x not in ids_by_f[fid]]
                if bad:
                    out.append(Finding(rel, s + 1, 'NO_SELECTION',
                                       f'F-{fid}: ứng viên không tồn tại: {", ".join(bad)}'))
            if not re.match(r'(?:PA|HC)-[A-Za-z0-9]+-\d+\b', v):
                out.append(Finding(rel, s + 1, 'NO_SELECTION', f'F-{fid}: thiếu «Chọn: PA-…/HC-…»'))
            else:
                pm = PICK_RE.match(v)
                if not pm or not pm.group(2):
                    out.append(Finding(rel, r[0], 'SELECTION_NO_NAME',
                                       f'F-{fid}: «Chọn:» phải là «<mã> — <tên phương án>»'))
            rr = _field(lines, s, e, 'Lý do CEO')
            if not rr or not rr[1]:
                out.append(Finding(rel, s + 1, 'NO_CEO_REASON', f'F-{fid}: «Lý do CEO:» rỗng'))
        r = _field(lines, s, e, 'Khoảng tham số')
        if not r or not r[1]:
            out.append(Finding(rel, s + 1, 'NO_PARAM_RANGE', f'F-{fid}: «Khoảng tham số:» rỗng'))
        r = _field(lines, s, e, 'Kế hoạch thử')
        if not r or not r[1]:
            out.append(Finding(rel, s + 1, 'NO_TEST_PLAN', f'F-{fid}: «Kế hoạch thử:» rỗng'))


def lint_dir(path, prefix, quick=False, draft=False, refs=None):
    out = []
    idx = load_rule_index(DEFAULT_REFS if refs is None else refs)
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
        for f, v in lint_variants(present['Form_Variants'], quick, out, idx).items():
            ids.setdefault(f, []).extend(v)
    f_ids = list(ids)
    if 'Benchmark' in present:
        for f, v in lint_benchmark(present['Benchmark'], f_ids, out).items():
            ids.setdefault(f, []).extend(v)
    if 'Scoring' in present:
        lint_scoring(present['Scoring'], ids, out)
    if 'Form_Selection' in present:
        lint_selection(present['Form_Selection'], ids, out, draft)
    return out


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    d, prefix, quick, draft, refs, i = None, None, False, False, None, 0
    while i < len(argv):
        t = argv[i]
        if t == '--prefix' and i + 1 < len(argv):
            prefix = argv[i + 1]
            i += 2
        elif t == '--refs' and i + 1 < len(argv):
            refs = argv[i + 1]
            i += 2
        elif t == '--quick':
            quick = True
            i += 1
        elif t == '--draft':
            draft = True
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
    if refs is not None and not os.path.isdir(refs):
        print(f'ERROR không có thư mục references: {refs}', file=sys.stderr)
        return 2
    try:
        fs = lint_dir(d, prefix, quick, draft, refs)
    except (OSError, UnicodeDecodeError) as e:
        print(f'ERROR không đọc được tệp: {e}', file=sys.stderr)
        return 2
    for f in fs:
        print(f'{f.file}:L{f.line} {f.code} {f.msg}')
    if fs:
        print(f'TRƯỢT — {len(fs)} finding')
        return 1
    print('ĐẠT — 4 tệp BF đúng khuôn' + (' (nháp, --draft)' if draft else ''))
    return 0


if __name__ == '__main__':
    for st in (sys.stdout, sys.stderr):
        if hasattr(st, 'reconfigure'):
            st.reconfigure(encoding='utf-8')
    sys.exit(main())
