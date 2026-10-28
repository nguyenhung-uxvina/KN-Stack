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
            pm = snap_pagemap(text, pm)      # xem docstring snap_pagemap
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
        # Lượt phụ — lớp chữ PDF tách MỘT từ thành hai: 'electroly tes', 'dead rise'.
        # Khác gạch-nối-ngắt-dòng (norm() đã xử): ở đây không có gạch nối nào để bám,
        # nên phép so chuỗi báo HONG cho một câu CÓ IN TRONG SÁCH — âm tính giả.
        # Đo trên hai kho cuốn USV: 23 ca / 264k từ, nhưng 9 ca nằm trên 'deadrise'
        # — thuật ngữ trung tâm của nguồn, nên xác suất vấp cao hơn con số 23 gợi ra.
        # Bỏ HẾT khoảng trắng hai bên rồi so lại.
        #
        # Ngưỡng 20 ký tự đặt bằng phép đo, không bằng phỏng đoán: 4.000 cụm 3–5 từ ghép
        # bừa từ 400 từ phổ biến nhất của kho (lượt chính đều trượt) cho **0 ca khớp bừa**
        # ở mọi ngưỡng thử từ 0 đến 40. Cái chặn dương tính giả là luật ≥3 từ cộng với độ
        # đặc hiệu của chuỗi chữ, không phải ngưỡng này. Ngưỡng chỉ để một trích rất ngắn
        # gồm toàn từ ngắn không lọt. Thử 40 trước thì chặn đúng ca đã đẻ ra bản vá
        # ('avoidelectrolytesaltogether' = 27 ký tự) — nên đừng nâng lại mà không đo.
        tl = t.replace(' ', '')
        if len(tl) >= 20:
            for n in self.nguon:
                lt, idx = self._liet(n)
                pos = lt.find(tl)
                if pos >= 0:
                    return {'ok': True, 'nhan': n['nhan'], 'trang': self.trang(n, idx[pos]),
                            'loai': n['kind'], 'so_tu': len(t.split()),
                            'so_lan': lt.count(tl), 'tach_chu': True}
        return {'ok': False, 'ly_do': 'KHONG THAY trong bat ky kho nao', 'so_tu': len(t.split())}

    def _liet(self, n):
        """Kho bỏ hết khoảng trắng + bảng ánh xạ vị trí về kho gốc (để còn tra ra trang).
        Dựng một lần cho mỗi nguồn, và chỉ khi lượt tra chính đã thất bại."""
        if 'liet' not in n:
            buf, idx = [], []
            for i, c in enumerate(n['text']):
                if c != ' ':
                    buf.append(c)
                    idx.append(i)
            n['liet'], n['liet_idx'] = ''.join(buf), idx
        return n['liet'], n['liet_idx']


def snap_pagemap(text, pm):
    """Dịch mốc trang về đúng chỗ số trang in xuất hiện trong kho.

    🔴 Vì sao. Mốc do `source_ingest` ghi KHÔNG trùng chỗ trang thật sự bắt đầu: đo trên
    Pahl & Beitz (2026-09-26) chỉ **56/617** mốc rơi đúng vào số trang của nó; lệch trung
    vị −18 ký tự, biên độ −178..+195. Trang chuẩn hoá dài ~1.600 ký tự, nên một trích nằm
    gần ranh giới bị gán **lùi một trang**, im lặng.

    Ca thật đã bắt được: trích "clear specification of the operating conditions…" là gạch
    đầu dòng ĐẦU TIÊN của trang in 250 (đọc từ ảnh), công cụ trả tr.249 — mốc trang 250 rơi
    vào GIỮA TỪ (`clear specific|ation`), còn header "250 7 embodiment design" thì nằm trong
    vùng gán cho 249. Một agent đã phải mở ảnh mới phát hiện.

    Cách sửa: với mỗi mốc, tìm lần xuất hiện của **chính số trang ấy** như một token riêng,
    gần mốc nhất trong cửa sổ ±300 ký tự, rồi dịch mốc về đó. Thận trọng: chỉ dịch khi tìm
    thấy, và chỉ khi kết quả vẫn giữ tính đơn điệu — số trang in chạy trong body text (ví dụ
    "250 mm") có thể bẫy phép dò.

    Đo trên 86 trích thật của cuốn usv-thiet-ke-he-thong: sửa đúng **1** ca sai, **không
    đụng** 85 ca còn lại. Không có dương tính giả.
    """
    ra, truoc = [], -1
    for off, tr in pm:
        if tr is None:
            ra.append((off, tr))
            continue
        lo = max(0, off - 300)
        cua_so = text[lo:off + 300]
        tot = None
        for m in re.finditer(r'(?<![0-9])' + re.escape(str(tr)) + r'(?![0-9])', cua_so):
            d = (lo + m.start()) - off
            if tot is None or abs(d) < abs(tot):
                tot = d
        moi = off + tot if tot is not None else off
        if moi <= truoc:          # giữ đơn điệu — thà không dịch còn hơn dịch sai
            moi = off
        truoc = moi
        ra.append((moi, tr))
    return ra


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

    hong = tach = 0
    for q in qs:
        r = kho.tra(q)
        if r['ok']:
            tr = ('tr.%s' % r['trang']) if r['loai'] == 'trang_in' else ('tr.PDF %s' % r['trang'])
            canh = '' if r['so_lan'] == 1 else '  [xuat hien %d lan — kiem dung cho]' % r['so_lan']
            if r.get('tach_chu'):
                canh += '  [LOP CHU TACH TU — MO ANH trang nay truoc khi dong ngoac kep]'
                tach += 1
            print('  OK    %-4s %-10s %2d tu  | %s%s' % (tr, r['nhan'], r['so_tu'], q[:56], canh))
        else:
            hong += 1
            print('  HONG  %s | %s' % (r['ly_do'], q[:70]))
    print('-' * 74)
    print('  tim thay %d / hong %d  (tong %d)' % (len(qs) - hong, hong, len(qs)))
    if tach:
        print('  %d trich chi tim thay SAU KHI bo khoang trang — lop chu PDF tach mot tu' % tach)
        print('  thanh hai. Chu IN TRONG SACH la dung; lop chu thi khong. Bat buoc mo anh')
        print('  trang do va doi chieu truoc khi dong ngoac kep quanh no.')
    if hong:
        print('  HONG khong phai lúc nào cũng = bia. Ba nguyên nhân thật hay gặp:')
        print('    1. trich CHEP TAY sai mot chu   2. trich vat qua hai trang')
        print('    3. trich lay tu sach NEN ma minh chua nap (--source2)')
        print('  Nhung cho tới khi truy ra nguyên nhân thì KHONG duoc dong ngoac kep.')
    return 1 if hong else 0


if __name__ == '__main__':
    sys.exit(main())
