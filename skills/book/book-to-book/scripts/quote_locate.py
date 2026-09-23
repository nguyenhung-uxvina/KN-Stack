# -*- coding: utf-8 -*-
"""Tra một trích dẫn trong kho ngữ liệu → có thật không, và ở TRANG IN nào.

Vì sao cần công cụ này thay vì để agent tự ghi số trang: agent đọc một lát cắt
`_source/chapters/chNN.txt` thì **không nhìn thấy số trang** — lát cắt là văn bản
trần. Bảo nó ghi "tr.N" nghĩa là bảo nó đoán, và số trang đoán trông y hệt số trang
đọc được. Đây đúng là lớp lỗi đã trả giá hai lần trong dự án này (bịa `1989`, bịa
`2001`), nên lần này chặn bằng công cụ chứ không bằng lời nhắc.

Dùng:
    # tra một câu
    python quote_locate.py <outdir> --tim "the design process is iterative"

    # kiểm cả tệp: mỗi dòng một trích dẫn (bỏ dòng trống và dòng bắt đầu bằng #)
    python quote_locate.py <outdir> --tep candidates.txt

Mã thoát: 0 = mọi trích tìm thấy · 1 = có trích KHÔNG tìm thấy · 2 = không đo được.
"""
from __future__ import annotations

import argparse
import bisect
import glob
import io
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def norm(s: str) -> str:
    """PHẢI khớp với source_ingest.norm — nếu lệch thì mọi phép tra đều vô nghĩa."""
    s = unicodedata.normalize('NFKC', s)
    s = s.replace('\u00ad', '')
    s = re.sub(r'-\s*\n\s*', '', s)          # gạch nối bị ngắt dòng
    s = s.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('ﬀ', 'ff')
    s = s.replace('\u2019', "'").replace('\u2018', "'")
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2013', '-').replace('\u2014', '-')
    s = re.sub(r'[*_`]', '', s)               # nhấn mạnh markdown
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return ' '.join(s.split())


class Kho:
    def __init__(self, outdir):
        sdir = os.path.join(outdir, '_source')
        cps = sorted(glob.glob(os.path.join(sdir, '*.corpus.txt')))
        if not cps:
            raise SystemExit('KHONG DO DUOC: khong thay kho ngu lieu trong %s. '
                             'Chay source_ingest.py truoc.' % sdir)
        self.nguon = []
        for cp in cps:
            nhan = os.path.basename(cp)[:-len('.corpus.txt')]
            text = norm(io.open(cp, encoding='utf-8').read())
            pmp = os.path.join(sdir, nhan + '.pagemap.json')
            pm = json.load(io.open(pmp, encoding='utf-8')) if os.path.isfile(pmp) else []
            mp = os.path.join(sdir, nhan + '.meta.json')
            meta = json.load(io.open(mp, encoding='utf-8')) if os.path.isfile(mp) else {}
            self.nguon.append({
                'nhan': nhan, 'text': text, 'pm': pm,
                'offs': [o for o, _ in pm],
                'kind': meta.get('page_kind', 'trang_in'),
            })

    def trang(self, n, pos):
        """char offset → số trang in. Lưu ý: offset của pagemap tính trên kho ĐÃ chuẩn
        hoá bởi source_ingest; norm() ở đây phải cho cùng kết quả (xem docstring norm)."""
        if not n['offs']:
            return None
        k = bisect.bisect_right(n['offs'], pos) - 1
        return n['pm'][max(k, 0)][1]

    def tra(self, q):
        t = norm(q)
        if len(t.split()) < 3:
            return {'ok': False, 'ly_do': 'trich qua ngan (<3 tu) — khong tra duoc'}
        for n in self.nguon:
            pos = n['text'].find(t)
            if pos >= 0:
                lan = n['text'].count(t)
                return {'ok': True, 'nhan': n['nhan'], 'trang': self.trang(n, pos),
                        'loai': n['kind'], 'so_tu': len(t.split()), 'so_lan': lan}
        return {'ok': False, 'ly_do': 'KHONG THAY trong bat ky kho nao', 'so_tu': len(t.split())}


def main(argv=None):
    ap = argparse.ArgumentParser(description='Tra trich dan trong kho ngu lieu goc')
    ap.add_argument('outdir')
    ap.add_argument('--tim', help='mot trich dan')
    ap.add_argument('--tep', help='tep, moi dong mot trich dan')
    a = ap.parse_args(argv)

    kho = Kho(a.outdir)
    qs = []
    if a.tim:
        qs.append(a.tim)
    if a.tep:
        for l in io.open(a.tep, encoding='utf-8'):
            l = l.strip()
            if l and not l.startswith('#'):
                qs.append(l)
    if not qs:
        raise SystemExit('can --tim hoac --tep')

    hong = 0
    for q in qs:
        r = kho.tra(q)
        if r['ok']:
            tr = ('tr.%s' % r['trang']) if r['loai'] == 'trang_in' else ('tr.PDF %s' % r['trang'])
            canh = '' if r['so_lan'] == 1 else '  [xuat hien %d lan — kiem dung cho]' % r['so_lan']
            print('  OK    %-4s %-10s %2d tu  | %s%s' % (tr, r['nhan'], r['so_tu'], q[:56], canh))
        else:
            hong += 1
            print('  HONG  %s | %s' % (r['ly_do'], q[:70]))
    print('-' * 74)
    print('  tim thay %d / hong %d  (tong %d)' % (len(qs) - hong, hong, len(qs)))
    if hong:
        print('  HONG khong phai lúc nào cũng = bia. Ba nguyên nhân thật hay gặp:')
        print('    1. trich CHEP TAY sai mot chu   2. trich vat qua hai trang')
        print('    3. trich lay tu sach NEN ma minh chua nap (--source2)')
        print('  Nhung cho tới khi truy ra nguyên nhân thì KHONG duoc dong ngoac kep.')
    return 1 if hong else 0


if __name__ == '__main__':
    sys.exit(main())
