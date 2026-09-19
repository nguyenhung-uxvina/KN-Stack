# -*- coding: utf-8 -*-
"""Số đo từ sổ hồi tưởng RETRIEVAL.md của /learn-teach → bằng chứng cho Progress Tracker.

Vì sao là script
----------------
Progress Tracker của learn-track từng để AI "điền nháp mức hiện tại, người học sửa".
Đó là đúng cái ảo giác mà learn-teach sinh ra để bắt: cảm giác "mình ở mức 3" (của
AI hay của người học) không phải phép đo. Sổ hồi tưởng thì là phép đo: người học
đoán trước (C/V/T), rồi hồi tưởng nguội (✓/✗). Script này chỉ đếm — không suy ra
mức trình độ. Mức do người học tự chấm, nhìn vào số.

Hai giới hạn phải in ra mỗi lần, vì người đọc số sẽ quên:
  * Sổ chỉ giữ lần hồi tưởng GẦN NHẤT mỗi mục, không giữ lịch sử.
  * Sổ đo trí nhớ, không đo năng lực làm — chiều "kiểm chứng vật lý" cần bằng chứng khác.

Dùng
----
    python retrieval_stats.py <RETRIEVAL.md | thư mục workspace> [--hom-nay YYYY-MM-DD]

Thư mục: tìm `RETRIEVAL.md` rồi `learn/RETRIEVAL.md` (bố cục LEARN/learn/ của /book-to-learn).

Mã thoát: 0 = đọc hết · 1 = có dòng không đọc được (được liệt kê, KHÔNG bị bỏ im lặng —
bỏ im lặng làm tỉ lệ đẹp hơn thật) · 2 = không thấy sổ / sổ không có bảng.
"""
from __future__ import annotations

import argparse
import datetime as dt
import io
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DOAN = {'c': 'C', 'chắc': 'C', 'v': 'V', 'vừa': 'V', 't': 'T', 'thấp': 'T'}
THUC = {'✓': '✓', '✔': '✓', '✗': '✗', '✘': '✗', 'x': '✗', '×': '✗'}
TRONG = {'—', '–', '-', '…', 'n/a'}          # ô giữ chỗ = chưa có giá trị
COT = {'#': '#', 'mục': 'muc', 'bài': 'bai', 'đoán': 'doan', 'thực': 'thuc',
       'bậc': 'bac', 'đến hạn': 'han', 'ghi chú': 'ghi_chu'}


def _chuan(s):
    return ' '.join(unicodedata.normalize('NFC', s).replace('*', '').split()).lower()


def _o(dong):
    return [c.strip() for c in dong.strip().strip('|').split('|')]


def tim_so(duong):
    if os.path.isfile(duong):
        return duong
    for p in (os.path.join(duong, 'RETRIEVAL.md'), os.path.join(duong, 'learn', 'RETRIEVAL.md')):
        if os.path.isfile(p):
            return p
    raise SystemExit('KHÔNG THẤY RETRIEVAL.md ở %s (đã tìm ./ và ./learn/). '
                     'Chưa có sổ hồi tưởng thì chưa có phép đo — xem /learn-teach.' % duong)


def doc_so(path):
    van = io.open(path, encoding='utf-8-sig').read()
    dong = van.splitlines()
    m = re.search(r'\*\*Cập nhật:\*\*\s*([0-9-]+)', unicodedata.normalize('NFC', van))
    for i, d in enumerate(dong):
        if not d.strip().startswith('|'):
            continue
        tieu_de = [COT.get(_chuan(c)) for c in _o(d)]
        if not {'muc', 'doan', 'thuc'} <= set(tieu_de):
            continue
        hang, hong = [], []
        for stt, d2 in enumerate(dong[i + 2:], 1):
            if not d2.strip().startswith('|'):
                break
            o = _o(d2)
            r = {k: (o[j] if j < len(o) else '') for j, k in enumerate(tieu_de) if k}
            # Cột '#' không bắt buộc ở cổng tiêu đề, nên đừng đọc nó vô điều kiện: sổ thiếu
            # cột này + có mục quá hạn ⇒ KeyError, traceback, và mã 1 (mã 1 nghĩa là "đã
            # liệt kê dòng hỏng" — trong khi chẳng liệt kê gì).
            if not r.get('#'):
                r['#'] = str(stt)
            loi = _kiem_hang(r)
            (hong if loi else hang).append(dict(r, loi=loi) if loi else r)
        return {'path': path, 'cap_nhat': m.group(1) if m else None, 'hang': hang, 'hong': hong}
    raise SystemExit('KHÔNG THẤY bảng sổ hồi tưởng (cần cột Mục, Đoán, Thực) trong %s' % path)


def _kiem_hang(r):
    """Chuẩn hoá tại chỗ; trả về lý do hỏng hoặc '' nếu đọc được."""
    # _chuan cho CẢ HAI cột: sổ thật dùng in đậm trong bảng, nên "**✗**" rất dễ xảy ra —
    # và đó đúng là ô "chắc mà sai", thứ cần bắt nhất.
    d, t = _chuan(r.get('doan', '')), _chuan(r.get('thuc', ''))
    d = '' if d in TRONG else d
    t = '' if t in TRONG else t
    if d and d not in DOAN:
        return 'Đoán "%s" không phải C/V/T' % r['doan']
    if t and t not in THUC:
        return 'Thực "%s" không phải ✓/✗' % r['thuc']
    if d and not t:
        return 'có Đoán mà chưa có Thực — lượt ôn chưa chấm xong'
    # Thực mà không Đoán: ĐÃ ôn, chỉ thiếu bước đoán trước (sổ icdm 15/08). Tính vào tỉ lệ
    # nhớ, bỏ khỏi hiệu chỉnh — loại cả dòng thì tỉ lệ nhớ báo sai.
    r['doan'], r['thuc'] = DOAN.get(d), THUC.get(t)
    # Ký hiệu giữ chỗ hợp lệ ở MỌI cột, không chỉ Đoán/Thực — một ô "—" ở cột Bậc từng
    # làm cả Progress Tracker bị chặn.
    b = r.get('bac', '').strip()
    b = '' if _chuan(b) in TRONG else b
    if b and not b.isdigit():
        return 'Bậc "%s" không phải số' % b
    r['bac'] = int(b) if b else None
    h = r.get('han', '').strip()
    h = '' if _chuan(h) in TRONG else h
    if h:
        try:
            dt.date.fromisoformat(h)
        except ValueError:
            return 'Đến hạn "%s" không phải YYYY-MM-DD' % h
    r['han'] = h or None
    r['bai'] = r.get('bai', '').strip() or '—'
    return ''


def thong_ke(so, hom_nay):
    hang = so['hang']
    on = [r for r in hang if r['thuc']]
    o = {k: 0 for k in ('C✓', 'C✗', 'V✓', 'V✗', 'T✓', 'T✗')}
    co_doan = [r for r in on if r['doan']]
    for r in co_doan:
        o[r['doan'] + r['thuc']] += 1
    theo_bai = {}
    for r in hang:
        b = theo_bai.setdefault(r['bai'], {'muc': 0, 'da_on': 0, 'dung': 0, 'chac_sai': 0, '_bac': []})
        b['muc'] += 1
        b['da_on'] += bool(r['thuc'])
        b['dung'] += r['thuc'] == '✓'
        b['chac_sai'] += (r['doan'], r['thuc']) == ('C', '✗')
        if r['bac'] is not None:
            b['_bac'].append(r['bac'])
    for b in theo_bai.values():
        ds = b.pop('_bac')
        b['bac_tb'] = round(sum(ds) / len(ds), 1) if ds else None
    return {
        'tong': len(hang), 'da_on': len(on), 'dung': sum(r['thuc'] == '✓' for r in on), 'o': o,
        'co_doan': len(co_doan), 'thieu_doan': [r['#'] for r in on if not r['doan']],
        'chac_sai': [r for r in on if (r['doan'], r['thuc']) == ('C', '✗')],
        'den_han': [r['#'] for r in hang if r['han'] and r['han'] <= hom_nay],
        'theo_bai': theo_bai,
    }


def _pt(a, b):
    return '%d/%d (%d%%)' % (a, b, round(100 * a / b)) if b else '0/0 (—)'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Số đo từ sổ hồi tưởng RETRIEVAL.md')
    ap.add_argument('duong', help='RETRIEVAL.md hoặc thư mục workspace')
    ap.add_argument('--hom-nay', default=dt.date.today().isoformat())
    a = ap.parse_args(argv)
    try:
        so = doc_so(tim_so(a.duong))
    except SystemExit as e:
        print(e)
        return 2
    s = thong_ke(so, a.hom_nay)
    o = s['o']
    print('retrieval_stats — %s · %d mục · sổ cập nhật %s · hôm nay %s'
          % (so['path'], s['tong'], so['cap_nhat'] or '?', a.hom_nay))
    print('⚠ Ảnh chụp lần hồi tưởng gần nhất của mỗi mục (sổ không giữ lịch sử). '
          'Sổ đo trí nhớ, không đo năng lực làm.')
    print()
    print('Đã hồi tưởng: %s · nhớ đúng: %s' % (_pt(s['da_on'], s['tong']), _pt(s['dung'], s['da_on'])))
    print('Hiệu chỉnh: chắc✓ %d · chắc✗ %d (ảo giác) · vừa✓ %d · vừa✗ %d · thấp✓ %d (dưới tự tin) · thấp✗ %d'
          % (o['C✓'], o['C✗'], o['V✓'], o['V✗'], o['T✓'], o['T✗']))
    print('Quá tự tin: %s lượt có ghi đoán' % _pt(o['C✗'], s['co_doan']))
    if s['thieu_doan']:
        print('⚠ %d mục đã ôn mà không ghi đoán trước (#%s) — tính vào tỉ lệ nhớ, KHÔNG đo được '
              'ảo giác thành thạo ở các lượt đó. Lượt sau: đoán C/V/T trước khi trả lời.'
              % (len(s['thieu_doan']), ', #'.join(s['thieu_doan'])))
    print('Đến hạn hoặc quá hạn: %d mục%s' % (len(s['den_han']),
          (' (#' + ', #'.join(s['den_han']) + ')') if s['den_han'] else ''))
    print()
    print('| Bài | Mục | Đã ôn | Nhớ đúng | Chắc mà sai | Bậc TB |')
    print('|---|---|---|---|---|---|')
    for bai, b in sorted(s['theo_bai'].items()):
        print('| %s | %d | %d | %d | %d | %s |' % (bai, b['muc'], b['da_on'], b['dung'], b['chac_sai'],
                                               b['bac_tb'] if b['bac_tb'] is not None else '—'))
    if s['chac_sai']:
        print()
        print('Chắc mà sai (ưu tiên dạy lại bằng cách biểu diễn khác):')
        for r in s['chac_sai']:
            print('  #%s [bài %s] %s' % (r['#'], r['bai'], r['muc']))
    if so['hong']:
        print()
        for r in so['hong']:
            print('KHÔNG ĐỌC ĐƯỢC #%s: %s — sửa sổ rồi chạy lại; số ở trên CHƯA tính dòng này'
                  % (r.get('#', '?'), r['loi']))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
