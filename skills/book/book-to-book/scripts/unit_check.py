# -*- coding: utf-8 -*-
"""KIỂM QUY ĐỔI ĐƠN VỊ — vùng mù mà cổng nguyên bản không nhìn thấy.

Vì sao tồn tại
--------------
Cổng `fidelity_audit.py` kiểm **trích dẫn có tồn tại trong kho gốc hay không**. Nó
mù hoàn toàn với **số học**. Bài học đã trả giá ở bộ sách P&B (2026-08-27): bản
thảo viết *"hai trăm tám mươi ba trang cách nhau"* giữa tr.273 và tr.456 — thật là
**183** — và **lặp 2 lần ở 2 chỗ**, tức là lỗi tính chứ không phải lỗi gõ.

> **Không lượt soát nào của đường ống làm phép trừ.** File này làm phép trừ.

Sách dịch từ nguồn Anh-Mỹ đầy đơn vị đế quốc, và người dịch phải quy đổi bằng tay ở
hàng chục chỗ. Mỗi lần quy đổi là một cơ hội sai — và cái sai ấy **đọc rất trôi**,
vì không ai nhẩm lại foot sang mét khi đang đọc.

Đo cái gì
---------
Bắt mọi cặp `<số> <đơn vị mét hệ> (<số> <đơn vị đế quốc>)` và ngược lại, quy đổi
lại, so với sai số cho phép. Mặc định 2% — đủ rộng cho việc làm tròn có chủ ý
("khoảng 60 cm"), đủ chặt để bắt lỗi thật (nhầm hệ số, lệch dấu thập phân).

Chạy
----
    python unit_check.py <thư mục chứa .md> [--sai-so 0.02]

Mã thoát: 0 = mọi quy đổi khớp · 1 = có quy đổi sai · 2 = không thấy tệp nào.
Mã 1 KHÔNG tự động nghĩa là lỗi — có thể là làm tròn có chủ ý. Nhưng nó nghĩa là
**phải có người nhìn**, và đó chính là điều cần.
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# he so ve don vi chuan (met, kg, lit, do C xu ly rieng)
HE_SO = {
    'mm': 0.001, 'cm': 0.01, 'm': 1.0, 'km': 1000.0,
    'in': 0.0254, 'inch': 0.0254, 'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
    'mile': 1609.34, 'miles': 1609.34,
    'g': 0.001, 'kg': 1.0, 'lb': 0.453592, 'pound': 0.453592, 'pounds': 0.453592,
    'ml': 0.001, 'lít': 1.0, 'lit': 1.0, 'l': 1.0, 'gallon': 3.78541,
}
NHOM = {
    'dai': {'mm', 'cm', 'm', 'km', 'in', 'inch', 'ft', 'foot', 'feet', 'mile', 'miles'},
    'khoi_luong': {'g', 'kg', 'lb', 'pound', 'pounds'},
    'the_tich': {'ml', 'lít', 'lit', 'l', 'gallon'},
}

DV = '|'.join(sorted(HE_SO, key=len, reverse=True))
SO = r'[0-9]+(?:[.,][0-9]+)?'
# dang "8,90 m (29 ft 2,5 in)" hoac "38,6 cm (15,2 inch)" hoac "−23°C (−10°F)"
CAP = re.compile(
    r'(?P<a_so>' + SO + r')\s*(?P<a_dv>' + DV + r')\b[^()\n]{0,24}\('
    r'(?P<b>[^)\n]{1,40})\)', re.IGNORECASE)
NHIET = re.compile(
    r'(?P<a>[-−–]?' + SO + r')\s*°\s*C\b[^()\n]{0,24}\(\s*(?P<b>[-−–]?' + SO + r')\s*°\s*F', re.I)


def so(s):
    return float(s.replace('−', '-').replace('–', '-').replace(',', '.'))


def doc_ve(chuoi):
    """Doc mot ve co the gom nhieu don vi: '29 ft 2,5 in' -> (met, nhom)."""
    tong, nhom = 0.0, None
    found = False
    for m in re.finditer(r'(' + SO + r')\s*(' + DV + r')\b', chuoi, re.I):
        dv = m.group(2).lower()
        g = next((k for k, v in NHOM.items() if dv in v), None)
        if nhom and g != nhom:
            return None, None
        nhom = g
        tong += so(m.group(1)) * HE_SO[dv]
        found = True
    return (tong, nhom) if found else (None, None)


def kiem(root, sai_so):
    files = sorted(glob.glob(os.path.join(root, '*.md')))
    if not files:
        print('!! khong thay tep .md nao trong %s' % root)
        return 2
    tong, lech = 0, []
    for f in files:
        ten = os.path.basename(f)[:4]
        t = io.open(f, encoding='utf-8').read()

        for m in CAP.finditer(t):
            a = so(m.group('a_so')) * HE_SO[m.group('a_dv').lower()]
            nhom_a = next((k for k, v in NHOM.items()
                           if m.group('a_dv').lower() in v), None)
            b, nhom_b = doc_ve(m.group('b'))
            if b is None or nhom_a != nhom_b:
                continue          # ngoac khong phai quy doi -> bo qua
            tong += 1
            if a <= 0:
                continue
            d = abs(a - b) / a
            if d > sai_so:
                lech.append((ten, m.group(0)[:70], a, b, d))

        for m in NHIET.finditer(t):
            c, fh = so(m.group('a')), so(m.group('b'))
            tong += 1
            c_dung = (fh - 32) * 5.0 / 9.0
            if abs(c - c_dung) > 1.0:      # 1 do C
                lech.append((ten, m.group(0)[:70], c, c_dung, abs(c - c_dung)))

    print('=' * 74)
    print('KIỂM QUY ĐỔI ĐƠN VỊ — %s' % os.path.abspath(root))
    print('=' * 74)
    print('  cặp quy đổi tìm thấy : %d' % tong)
    print('  sai số cho phép      : %.0f%% (nhiệt độ: 1°C)' % (sai_so * 100))
    print('  LỆCH                 : %d' % len(lech))
    if lech:
        print()
        for ten, txt, a, b, d in lech:
            print('  !! %s | %s' % (ten, txt.replace('\n', ' ')))
            print('       khai %.4g  vs  quy đổi lại %.4g   (lệch %.1f%%)'
                  % (a, b, d * 100 if d < 1 else d))
    print()
    print('  🕳️ Phép này KHÔNG nhìn thấy: số học trong văn xuôi (hiệu, tổng, phần trăm),')
    print('     con số tự khai không kèm quy đổi, và đơn vị viết bằng chữ ("hai mươi inch").')
    print('     Bài học P&B: lỗi trừ 456−273 lặp 2 lần vẫn lọt mọi lượt soát.')
    return 1 if lech else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Kiểm quy đổi đơn vị trong bản thảo dịch')
    ap.add_argument('root', help='thư mục chứa các tệp .md')
    ap.add_argument('--sai-so', type=float, default=0.02, help='sai số cho phép (mặc định 0.02)')
    a = ap.parse_args(argv)
    return kiem(a.root, a.sai_so)


if __name__ == '__main__':
    sys.exit(main())
