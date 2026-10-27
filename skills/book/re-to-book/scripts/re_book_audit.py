# -*- coding: utf-8 -*-
"""Kiem P7 cho /re-to-book: GT chua do/chua ky, nhan phong doan/gia dinh, phu Idea_Log.

  gt              --book <dir>
  labels          --book <dir> [--stage P6|P4]
  idea-candidates --book <dir> --re <dir,dir>
  idea-coverage   --book <dir> --re <dir,dir>
  all             --book <dir> --re <dir,dir>
Ma thoat: 0 sach, 1 co phat hien, 2 thieu/hong dau vao.
"""
import argparse
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import re_provenance  # noqa: E402
from re_provenance import InputError  # noqa: E402
from re_units import normalize, split_units  # noqa: E402

OVERLAP = 'Phase7-IdeaLog-Overlap.md'
CAND_HEAD = '## Gợi ý từ vựng (không phải kết luận)'
VERDICTS = ('trùng', 'không trùng', 'một phần')
UNASSIGNED = 'chưa gán'
UNASSIGNED_MARK = 'chưa gán nhãn'
LABEL_VN = {'conjecture': 'phỏng đoán', 'assumption': 'giả định', UNASSIGNED: UNASSIGNED}
LABEL_DECISIONS = '_label_decisions.md'
DECIDABLE = ('knowledge', 'conjecture', 'assumption')
_NUM_HEAD = re.compile(r'^#{2,3}\s+(\d+\.\d+)')

_GT_KEY = re.compile(r'^(GT-.+)\.([67])(?:~\d+)?$')
_HEAD = re.compile(r'^(#{1,6})\s+(.*)$')
_TOKEN = re.compile(r'\d+(?:[,.]\d+)?\s?(?:nm|mm|m|kHz|Hz|ms|µs|dB)(?!\w)')
_GT_ANY = re.compile(r'(?<![\w-])GT-[A-Z0-9]+(?:-[A-Z0-9]+)*(?![\w-])')
_GT_UNIT = re.compile(r'^(GT-.+)\.\d(?:~\d+)?$')
_H12 = re.compile(r'^#{1,2}\s')
_SPLIT_ANCHOR = re.compile(r'^(.*?\.md)#(.+)$', re.S)


def _paragraphs(text):
    return [p for p in re.split(r'\n\s*\n', normalize(text)) if p.strip()]


def _mention(card):
    return re.compile(r'(?<![\w-])%s(?![\w-])' % re.escape(card))


def _gt_rules(manifest):
    """-> {card: {'result': bool, 'pred': bool}}"""
    rules = {}
    for ent in manifest.get('files', {}).values():
        for uid, rec in (ent.get('units') or {}).items():
            m = _GT_KEY.match(uid)
            if not m:
                continue
            r = rules.setdefault(m.group(1), {'result': False, 'pred': False})
            if m.group(2) == '6' and rec.get('empty_result'):
                r['result'] = True
            if m.group(2) == '7' and rec.get('cut'):
                r['pred'] = True
    return rules


def gt_cards(manifest):
    """Moi ma phieu GT co don vi trong manifest."""
    cards = set()
    for ent in manifest.get('files', {}).values():
        for uid in (ent.get('units') or {}):
            m = _GT_UNIT.match(uid)
            if m:
                cards.add(m.group(1))
    return cards


def gt_summary(manifest):
    """-> (so phieu, so phieu cho do, so phieu cho ky)"""
    rules = _gt_rules(manifest)
    return (len(gt_cards(manifest)), sum(r['result'] for r in rules.values()),
            sum(r['pred'] for r in rules.values()))


def gt_leaks(chapters, manifest):
    errs = []
    known = gt_cards(manifest)
    for ch in sorted(chapters):
        for i, para in enumerate(_paragraphs(chapters[ch]), 1):
            for gid in sorted(set(_GT_ANY.findall(para)) - known):
                errs.append('%s đoạn %d: %s không có trong manifest' % (ch, i, gid))
    for card, r in sorted(_gt_rules(manifest).items()):
        rx = _mention(card)
        for ch in sorted(chapters):
            for i, para in enumerate(_paragraphs(chapters[ch]), 1):
                if not rx.search(para):
                    continue
                low = para.lower()
                if r['result'] and 'chờ đo' not in low:
                    errs.append('%s đoạn %d: nhắc %s (chưa có kết quả đo) mà không có ⟨chờ đo⟩' % (ch, i, card))
                if r['pred'] and 'dự đoán' in low and 'chờ ký' not in low:
                    errs.append('%s đoạn %d: nhắc dự đoán của %s (chưa ký) mà không có ⟨chờ ký⟩' % (ch, i, card))
    return errs


def _fence(line):
    return line.lstrip().startswith(('```', '~~~'))


def _section_text(text, sec_key):
    """Van ban muc co tieu de chua so muc; None neu khong thay."""
    num = sec_key.lstrip('§').strip()
    rx = re.compile(r'(?<![\w.])%s(?![\w]|\.\d)' % re.escape(num))
    lines = normalize(text).split('\n')
    start = level = None
    in_fence = False
    for i, ln in enumerate(lines):
        if _fence(ln):
            in_fence = not in_fence
        m = None if in_fence else _HEAD.match(ln)
        if m and rx.search(m.group(2)):
            start, level = i, len(m.group(1))
            break
    if start is None:
        return None
    end = len(lines)
    in_fence = False
    for j in range(start + 1, len(lines)):
        if _fence(lines[j]):
            in_fence = not in_fence
        m = None if in_fence else _HEAD.match(lines[j])
        if m and len(m.group(1)) <= level:
            end = j
            break
    return '\n'.join(lines[start:end])


def _numbered_headings(text):
    """So muc NN.x cua moi tieu de ##/### ngoai rao ma."""
    out, in_fence = [], False
    for ln in normalize(text).split('\n'):
        if _fence(ln):
            in_fence = not in_fence
            continue
        m = None if in_fence else _NUM_HEAD.match(ln)
        if m and m.group(1) not in out:
            out.append(m.group(1))
    return out


def load_label_decisions(book):
    """Phase1-Exploration/_label_decisions.md: | <neo> | <knowledge|conjecture|assumption> |.
    Thieu tep => {} (chua co quyet dinh nao)."""
    p = os.path.join(book, 'Phase1-Exploration', LABEL_DECISIONS)
    if not os.path.isfile(p):
        return {}
    with open(p, encoding='utf-8-sig') as f:
        text = normalize(f.read())
    out = {}
    for ln in text.split('\n'):
        if not ln.lstrip().startswith('|'):
            continue
        cells = _cells(ln)
        if len(cells) < 2:
            continue
        anchor = cells[0].replace('`', '').strip()
        label = cells[1].replace('*', '').strip().lower()
        if label in DECIDABLE and _SPLIT_ANCHOR.match(anchor):
            out[anchor] = label
    return out


def label_gaps(chapters, prov, manifest, decisions=None):
    errs = []
    files = manifest.get('files', {})
    decisions = decisions or {}
    for ch in sorted(set(chapters) - set(prov)):
        errs.append('%s: không có provenance' % ch)
    for ch in sorted(prov):
        secs = (prov[ch] or {}).get('sections', {})
        if ch not in chapters:
            errs.append('%s: không thấy chương' % ch)
            continue
        have = {k.lstrip('§').strip() for k in secs}
        for num in _numbered_headings(chapters[ch]):
            if num not in have:
                errs.append('%s §%s: không có provenance' % (ch, num))
        for sec, anchors in secs.items():
            body = _section_text(chapters[ch], sec)
            if body is None:
                errs.append('%s %s: không thấy mục trong chương' % (ch, sec))
                continue
            seen = set()
            for a in anchors:
                m = _SPLIT_ANCHOR.match(normalize(a).strip())
                if not m:
                    continue
                rec = (files.get(m.group(1), {}).get('units') or {}).get(m.group(2))
                label = (rec or {}).get('label')
                if label == UNASSIGNED:
                    label = decisions.get('%s#%s' % (m.group(1), m.group(2)), UNASSIGNED)
                vn = LABEL_VN.get(label)
                if not vn or a in seen:
                    continue
                seen.add(a)
                if '⟨' + vn not in body:
                    show = UNASSIGNED_MARK if label == UNASSIGNED else vn
                    errs.append('%s %s: thiếu ⟨%s⟩ (%s)' % (ch, sec, show, a))
    return errs


def _idea_rows(roots):
    """-> [(code, text)] doc thang tu Idea_Log tren dia (lop BLOCK, chi doi chieu)."""
    out = []
    for name in sorted(roots):
        for p in sorted(glob.glob(os.path.join(roots[name], '*_Idea_Log.md'))):
            with open(p, encoding='utf-8-sig') as f:
                units = split_units(normalize(f.read()))
            out.extend((u.id[4:], u.text) for u in units if u.id.startswith('row:'))
    return out


def idea_ids(roots):
    return sorted({c for c, _ in _idea_rows(roots)})


def _cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def idea_coverage(table_md, ids):
    in_cand = False
    verdicts = {}
    code_col = verd_col = None
    for ln in normalize(table_md).split('\n'):
        if _H12.match(ln):
            in_cand = ln.strip().startswith(CAND_HEAD)
            continue
        if in_cand or not ln.lstrip().startswith('|'):
            continue
        cells = _cells(ln)
        if code_col is None:
            low = [c.lower() for c in cells]
            if 'mã' in low and 'kết luận' in low:
                code_col, verd_col = low.index('mã'), low.index('kết luận')
            continue
        if all(re.fullmatch(r':?-{2,}:?', c) for c in cells if c):
            continue
        if len(cells) <= max(code_col, verd_col):
            continue
        code = cells[code_col].replace('**', '').replace('`', '').strip()
        verdicts[code] = cells[verd_col].replace('*', '').strip().lower()
    errs = []
    if code_col is None:
        return ['%s: không thấy bảng có cột "Mã" và "Kết luận"' % OVERLAP]
    for i in ids:
        if i not in verdicts:
            errs.append('%s: thiếu dòng cho mã %s' % (OVERLAP, i))
        elif verdicts[i] not in VERDICTS:
            errs.append('%s: mã %s có kết luận "%s" không hợp lệ (cần: %s)'
                        % (OVERLAP, i, verdicts[i], ' | '.join(VERDICTS)))
    return errs


def _tokens(text):
    return {re.sub(r'\s', '', t).replace(',', '.').lower() for t in _TOKEN.findall(text)}


def _shingles(text, n=5):
    t = re.sub(r'\s+', ' ', normalize(text).lower())
    return {t[i:i + n] for i in range(len(t) - n + 1)}


def idea_candidates(chapters, roots):
    """Goi y tu vung; KHONG chep noi dung Idea_Log vao dau ra."""
    lines = []
    for code, text in _idea_rows(roots):
        body = re.sub(r'^\s*\|\s*[^|]*\|', '', text, count=1).replace('|', ' ')
        toks, sh = _tokens(body), _shingles(body)
        for ch in sorted(chapters):
            for i, para in enumerate(_paragraphs(chapters[ch]), 1):
                common = sorted(toks & _tokens(para))
                ratio = (len(sh & _shingles(para)) / len(sh)) if sh else 0.0
                if len(common) >= 2 or ratio >= 0.25:
                    lines.append('- %s · %s · đoạn %d · token trùng: %s · tỉ lệ shingle %.2f'
                                 % (code, ch, i, ', '.join(common) or '—', ratio))
    return '\n'.join(lines) + ('\n' if lines else '')


def _merge_candidates(existing, body):
    """Thay/chen muc goi y o dau tep, giu phan con lai."""
    block = CAND_HEAD + '\n\n' + (body if body else '(không có gợi ý)\n')
    if existing is None:
        return block
    lines = existing.replace('\r\n', '\n').split('\n')
    for i, ln in enumerate(lines):
        if ln.strip() == CAND_HEAD:
            j = i + 1
            while j < len(lines) and not _H12.match(lines[j]):
                j += 1
            rest = '\n'.join(lines[j:])
            head = '\n'.join(lines[:i])
            return (head + '\n' if head.strip() else '') + block + ('\n' + rest if rest else '')
    if lines and lines[0].startswith('# '):
        rest = '\n'.join(lines[1:]).lstrip('\n')
        return lines[0] + '\n\n' + block + ('\n' + rest if rest else '')
    return block + '\n' + existing


# ---------- CLI ----------
def _load_json(path):
    try:
        with open(path, encoding='utf-8-sig') as f:
            return json.load(f)
    except (OSError, ValueError):
        raise InputError('không đọc được %s' % path)


def _chapters(book, stage=None):
    p6, p4 = (os.path.join(book, d) for d in ('Phase6-Revised', 'Phase4-Chapters'))
    if stage == 'P6':
        d = p6
    elif stage == 'P4':
        d = p4
    else:
        d = p6 if glob.glob(os.path.join(p6, 'Ch*.md')) else p4
    files = sorted(glob.glob(os.path.join(d, 'Ch*.md')))
    if not files:
        raise InputError('không có Ch*.md trong %s' % d)
    out = {}
    for p in files:
        with open(p, encoding='utf-8-sig') as f:
            out[os.path.splitext(os.path.basename(p))[0]] = f.read()
    return out, d


def _roots(arg):
    roots = {}
    for d in (x.strip() for x in arg.split(',') if x.strip()):
        ab = os.path.abspath(d)
        if not os.path.isdir(ab):
            raise InputError('không phải thư mục: %s' % d)
        roots[os.path.basename(ab)] = ab
    if not roots:
        raise InputError('--re trống')
    return roots


def _manifest(book):
    return _load_json(os.path.join(book, '_re_manifest.json'))


def _report(title, errs):
    print('[%s] %s' % (title, 'sạch' if not errs else '%d phát hiện' % len(errs)))
    for e in errs:
        print('  ' + e)
    return 1 if errs else 0


def _run_gt(a):
    chapters, _ = _chapters(a.book)
    man = _manifest(a.book)
    n, k, m = gt_summary(man)
    print('kiểm %d phiếu GT (%d chờ đo, %d chờ ký)' % (n, k, m))
    return _report('gt', gt_leaks(chapters, man))


def _run_labels(a):
    chapters, d = _chapters(a.book, getattr(a, 'stage', None))
    prov = {ch: {'chapter': ch, 'sections': secs} for _n, ch, secs in re_provenance.load_prov(d)}
    return _report('labels', label_gaps(chapters, prov, _manifest(a.book),
                                        load_label_decisions(a.book)))


def _require_ids(a):
    ids = idea_ids(_roots(a.re))
    if not ids:
        raise InputError('không tìm thấy Idea_Log trong các hồ sơ --re')
    return ids


def _run_coverage(a):
    ids = _require_ids(a)
    p = os.path.join(a.book, OVERLAP)
    if not os.path.isfile(p):
        raise InputError('thiếu %s' % p)
    with open(p, encoding='utf-8-sig') as f:
        return _report('idea-coverage', idea_coverage(f.read(), ids))


def _run_candidates(a):
    _require_ids(a)
    chapters, _ = _chapters(a.book)
    body = idea_candidates(chapters, _roots(a.re))
    p = os.path.join(a.book, OVERLAP)
    old = None
    if os.path.isfile(p):
        with open(p, encoding='utf-8-sig') as f:
            old = f.read()
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(_merge_candidates(old, body).rstrip('\n') + '\n')
    print('[idea-candidates] đã ghi %s (%d gợi ý; chỉ là gợi ý từ vựng, CEO kết luận)'
          % (p, body.count('\n')))
    return 0


def _run_all(a):
    code = 0
    for name, fn in (('gt', _run_gt), ('labels', _run_labels), ('idea-coverage', _run_coverage)):
        try:
            code = max(code, fn(a))
        except InputError as e:
            print('[%s] lỗi đầu vào: %s' % (name, e))
            code = 2
    try:
        _chs, d = _chapters(a.book)
        code = max(code, _report('provenance', re_provenance.check(d, _manifest(a.book))))
    except InputError as e:
        print('[provenance] lỗi đầu vào: %s' % e)
        code = 2
    return code


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding='utf-8', errors='replace')
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name, need_re in (('gt', False), ('labels', False), ('idea-candidates', True),
                          ('idea-coverage', True), ('all', True)):
        sp = sub.add_parser(name)
        sp.add_argument('--book', required=True)
        if need_re:
            sp.add_argument('--re', required=True)
        if name == 'labels':
            sp.add_argument('--stage', choices=('P6', 'P4'))
    try:
        a = ap.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    fn = {'gt': _run_gt, 'labels': _run_labels, 'idea-candidates': _run_candidates,
          'idea-coverage': _run_coverage, 'all': _run_all}[a.cmd]
    try:
        return fn(a)
    except (OSError, ValueError, KeyError, TypeError, AttributeError, InputError) as e:
        print('Lỗi đầu vào: %s' % e, file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
