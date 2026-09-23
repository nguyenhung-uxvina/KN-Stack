# -*- coding: utf-8 -*-
"""Lấy văn bản THÔ của một trang in — đường DUY NHẤT để kiểm một CON SỐ.

🔴 Vì sao tệp này phải tồn tại. Kho ngữ liệu (`*.corpus.txt`) được chuẩn hoá để so
chuỗi: `norm()` hạ chữ thường rồi **xoá mọi ký tự không phải chữ-số**. Việc đó làm
phép đối chiếu trích dẫn chạy ổn định, nhưng nó **phá huỷ mọi con số**:

    "7.5"      → "7 5"        (mất dấu thập phân)
    "-3.2"     → "3 2"        (MẤT DẤU TRỪ — im lặng, và đổi dấu một tham số thiết kế)
    "3×10^6"   → "3x10 6"     (mất số mũ)
    "0.30 m"   → "0 30 m"     → người đọc thấy "30 m"

Đo thật trên cuốn này (2026-09-15): agent cụm C9 đọc kho ra `clearance say 30 m`,
phải tự đoán bản gốc là 0,30 m. Nó đoán đúng — nhưng lần sau có thể đoán sai, và
một con số sai không kèm dấu hiệu nào thì không cổng nào ở hạ nguồn bắt được.

**Luật rút ra: kho ngữ liệu đối chiếu CHỮ, PDF gốc đối chiếu SỐ.** Mọi con số vào
sách phái sinh phải đi qua tệp này, không được lấy thẳng từ corpus hay từ lát cắt
`chapters/*.txt`.

Dùng:
    python page_raw.py <outdir> --trang 524
    python page_raw.py <outdir> --trang 524-526 --nhan Sadraey
    python page_raw.py <outdir> --tim "clearance"      # dò cụm chữ, trả trang chứa nó
"""
from __future__ import annotations

import argparse
import glob
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def _nap(outdir, nhan=None):
    sdir = os.path.join(outdir, '_source')
    metas = sorted(glob.glob(os.path.join(sdir, '*.meta.json')))
    if not metas:
        raise SystemExit('KHONG DO DUOC: khong thay *.meta.json trong %s' % sdir)
    for mp in metas:
        lab = os.path.basename(mp)[:-len('.meta.json')]
        if nhan and lab != nhan:
            continue
        meta = json.load(io.open(mp, encoding='utf-8'))
        ip = os.path.join(sdir, lab + '.pageindex.json')
        if not os.path.isfile(ip):
            raise SystemExit(
                'thieu %s. Tep nay do source_ingest.py sinh; ban kho cu thi chay lai '
                'ingest, hoac dung script dung pageindex rieng.' % ip)
        return lab, meta, json.load(io.open(ip, encoding='utf-8'))
    raise SystemExit('khong thay nhan %r' % nhan)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Van ban THO cua mot trang in (de kiem SO)')
    ap.add_argument('outdir')
    ap.add_argument('--trang', help='so trang in, hoac dai "a-b"')
    ap.add_argument('--tim', help='cum chu can do (khong dau ngoac), tra ve trang chua no')
    ap.add_argument('--nhan', help='nhan nguon (mac dinh: nguon dau tien)')
    a = ap.parse_args(argv)

    lab, meta, pidx = _nap(a.outdir, a.nhan)
    if meta['kind'] != 'pdf':
        raise SystemExit('nguon %r khong phai PDF — khong co trang in de tra.' % lab)
    from pypdf import PdfReader
    r = PdfReader(meta['path'])
    m = pidx['map']
    tra = {}
    for i, p in m:
        tra.setdefault(p, i)

    if a.tim:
        pat = re.compile(re.escape(a.tim), re.IGNORECASE)
        thay = 0
        for i, p in m:
            t = r.pages[i].extract_text() or ''
            if pat.search(t):
                thay += 1
                for ln in t.splitlines():
                    if pat.search(ln):
                        print('  tr.%-4s | %s' % (p, ' '.join(ln.split())[:100]))
                if thay >= 12:
                    print('  … dung o 12 trang dau; thu hep cum chu de xem het.')
                    break
        if not thay:
            print('  KHONG THAY %r trong van ban tho.' % a.tim)
        return 0

    if not a.trang:
        raise SystemExit('can --trang hoac --tim')
    if '-' in a.trang.lstrip('-'):
        x, y = a.trang.split('-', 1)
        ds = range(int(x), int(y) + 1)
    else:
        ds = [int(a.trang)]
    for p in ds:
        if p not in tra:
            print('  !! khong co trang in %s trong %s' % (p, lab))
            continue
        t = r.pages[tra[p]].extract_text() or ''
        print('=' * 74)
        print('  %s — TRANG IN %s  (pdf idx %d)  [VAN BAN THO, chua chuan hoa]' % (lab, p, tra[p]))
        print('=' * 74)
        print(t)
    return 0


if __name__ == '__main__':
    sys.exit(main())
