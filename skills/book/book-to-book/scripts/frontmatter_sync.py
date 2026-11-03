# -*- coding: utf-8 -*-
"""Sinh ba trường trích dẫn trong frontmatter chương — thay cho việc agent viết tay.

🔴 Vì sao tệp này phải tồn tại. Ba trường `quote_budget`, `quote_used`, `quotes_ok` trông như do
công cụ sinh, và người điều phối đã **nói với ba agent rằng chúng do công cụ sinh** — nên cả ba
từ chối sửa khi thấy chúng sai. Kiểm lại: **không script nào trong đường ống nhắc tới ba trường
đó**. Chúng do agent viết tay, không ai kiểm, và đã gây hậu quả đo được:

- Ch.22 khai `PahlBeitz 240`, **không có dòng Blount**, trong khi thân bài dựa vào Blount tr.273.
  **Hai vòng rà soát độc lập đọc lời khai ấy và kết luận Ch.22 thuần P&B** — một trong hai suýt
  xếp một khẳng định đúng thành lỗi.
- Ch.28 khai `quotes_ok: 14/14 · PahlBeitz 196`; đếm thật trong thân là **16 trích / ~206 từ**,
  trong đó một trích Blount 18 từ **chưa bao giờ được đếm**.
- Ch.14 khai `P&B 59 · Blount 228`; thật là **P&B 71 (VƯỢT ngân sách 60)** — lời khai che đúng
  chỗ vượt.

Một con số không ai kiểm **tệ hơn không có số**, vì nó được dùng làm bằng chứng.

## Sự thật nền, và vì sao chọn nó

- **Ngân sách** đọc từ `Phase3-Outline.md` (`**Trích** P&B N · Blount M`) — cùng nguồn với
  `kiem_ngan_sach_trich.py`. Không chép tay.
- **Lượng dùng** đếm từ **THÂN CHƯƠNG**, không từ tệp kèm trích. Lý do: sidecar là một lời khai
  khác, và nó **lệch được** — đo trên cuốn usv-thiet-ke-he-thong sau P6: Ch.28 có 14 dòng sidecar
  nhưng 15 trích trong thân. `kiem_ngan_sach_trich.py` chạy trên sidecar nên nó đo lời khai; tệp
  này đo hiện vật.
- **Nguồn của từng trích** do `quote_locate.Kho` quyết, tức đối chiếu với kho ngữ liệu. Không suy
  từ nhãn nguồn của chương: Ch.22 khai thuần P&B mà mượn Blount.

## Quy ước nhận trích (đo trên cuốn thật, không đặt ra)

Trích nguồn tiếng Anh viết **`*"…"*`** — nghiêng, ngoặc kép thẳng. Đếm trên Ch.28: 15 chuỗi khớp
mẫu này, cả 15 không dấu tiếng Việt. `«…»` là **thuật ngữ tiếng Việt** (14 chuỗi, 100% có dấu),
KHÔNG phải trích nguồn — gộp chúng vào là thổi phồng lượng trích và làm cổng bao phủ kêu oan.
Khối ``` bị loại, đúng quy ước đo của `dem_tu.py`.

Dùng:
    python frontmatter_sync.py <thư mục sách>              # chỉ BÁO, không ghi
    python frontmatter_sync.py <thư mục sách> --ghi        # ghi vào frontmatter
    python frontmatter_sync.py <thư mục sách> --chuong Phase6-Revised

Mã thoát: 0 = mọi chương khớp và trong ngân sách · 1 = có chương vượt ngân sách hoặc lời khai lệch
· 2 = không đo được (thiếu dàn ý / kho ngữ liệu / không thấy chương).
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TRICH = re.compile(r'\*"([^"\n]{12,})"\*')
DAU_TV = 'àáâãèéêìíòóôõùúýăđĩũơưạảảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'


def go_khoi(s: str) -> str:
    if s.startswith('---'):
        h = s.find('\n---', 3)
        if h > 0:
            s = s[h + 4:]
    return re.sub(r'```.*?```', ' ', s, flags=re.S)


def doc_ngan_sach(outline: str):
    """Ch -> {nguồn: số từ}. Đọc thẳng từ dàn ý — chép tay là chỗ con số đi lạc."""
    ns = {}
    for m in re.finditer(r'^### Ch\.(\d\d)\b.*?\n(.*?)(?=^### |\Z)', outline, re.M | re.S):
        d = re.search(r'\*\*Trích\*\*\s*([^\n]+)', m.group(2))
        if not d:
            continue
        # Nhận BẤT KỲ tên nguồn nào, không mã hoá cứng «P&B|Blount».
        # Bản đầu của tệp này chỉ nhận hai tên ấy, nên với một cuốn sách có nguồn khác nó trả
        # ngân sách RỖNG mà không báo gì — và ngân sách rỗng đọc y hệt «chương không có trích».
        b = {}
        for x in re.finditer(r'([A-Za-zÀ-ỹ&][\w&À-ỹ.]*)\s+([0-9]+)', d.group(1)):
            b[x.group(1)] = int(x.group(2))
        if b:
            ns[int(m.group(1))] = b
    return ns


def main(argv=None):
    ap = argparse.ArgumentParser(description='Sinh truong trich dan trong frontmatter')
    ap.add_argument('thumuc')
    ap.add_argument('--chuong', default='Phase6-Revised',
                    help='thu muc chua chuong (mac dinh Phase6-Revised, lui ve Phase4-Chapters)')
    ap.add_argument('--ghi', action='store_true', help='ghi vao frontmatter (mac dinh chi bao)')
    a = ap.parse_args(argv)

    op = os.path.join(a.thumuc, 'Phase3-Outline.md')
    if not os.path.isfile(op):
        print('KHONG DO DUOC: khong thay Phase3-Outline.md')
        return 2
    ns = doc_ngan_sach(io.open(op, encoding='utf-8').read())
    if not ns:
        print('KHONG DO DUOC: dan y khong cap dong "**Trích** P&B N · Blount M"')
        return 2

    cdir = os.path.join(a.thumuc, a.chuong)
    if not os.path.isdir(cdir):
        cdir = os.path.join(a.thumuc, 'Phase4-Chapters')
    teps = sorted(f for f in glob.glob(os.path.join(cdir, 'Ch*.md'))
                  if not os.path.basename(f).startswith('_'))
    if not teps:
        print('KHONG DO DUOC: khong thay chuong trong %s' % cdir)
        return 2

    try:
        from quote_locate import Kho
        kho = Kho(a.thumuc)
    except SystemExit as e:
        print('KHONG DO DUOC: %s' % e)
        return 2

    NHAN = {'PahlBeitz': 'P&B'}
    xau = 0
    print('=' * 78)
    print('FRONTMATTER — sinh tu THAN CHUONG, doi chieu kho ngu lieu')
    print('=' * 78)
    print('%-5s %-10s %6s %10s   %s' % ('ch', 'nguon', 'dung', 'ngan sach', 'trang thai'))
    print('-' * 78)
    for t in teps:
        n = int(os.path.basename(t)[2:4])
        s = io.open(t, encoding='utf-8').read()
        than = go_khoi(s)
        dung, hong = {}, 0
        for q in TRICH.findall(than):
            if any(c in DAU_TV for c in q.lower()):
                continue                      # tieng Viet trong ngoac: khong phai trich nguon
            r = kho.tra(q)
            if r['ok']:
                nh = NHAN.get(r['nhan'], r['nhan'])
                dung[nh] = dung.get(nh, 0) + r['so_tu']
            else:
                hong += 1
        bud = ns.get(n, {})
        tong_q = sum(1 for q in TRICH.findall(than)
                     if not any(c in DAU_TV for c in q.lower()))
        for nguon in sorted(set(list(bud) + list(dung))):
            d, b = dung.get(nguon, 0), bud.get(nguon)
            if b is None:
                print('%-5s %-10s %6d %10s   🔴 DAN Y KHONG CAP NGAN SACH NGUON NAY' % ('Ch%02d' % n, nguon, d, '—'))
                xau += 1
            else:
                v = d > b
                if v:
                    xau += 1
                print('%-5s %-10s %6d %10d   %s' % ('Ch%02d' % n, nguon, d, b, '🔴 VUOT' if v else 'dat'))
        if hong:
            xau += 1
            print('%-5s %-10s %6s %10s   🔴 %d trich KHONG tra duoc trong kho' % ('Ch%02d' % n, '', '', '', hong))

        moi_bud = ' · '.join('%s %d' % (k, v) for k, v in sorted(bud.items()))
        moi_use = ' · '.join('%s %d' % (k, v) for k, v in sorted(dung.items())) or '—'
        moi_ok = '%d/%d' % (tong_q - hong, tong_q)
        if a.ghi:
            s2 = s
            for khoa, gt in (('quote_budget', moi_bud), ('quote_used', moi_use), ('quotes_ok', moi_ok)):
                if re.search(r'(?m)^%s:.*$' % khoa, s2):
                    s2 = re.sub(r'(?m)^%s:.*$' % khoa, '%s: %s' % (khoa, gt), s2, count=1)
            if s2 != s:
                io.open(t, 'w', encoding='utf-8', newline='\n').write(s2)
    print('-' * 78)
    if a.ghi:
        print('  da GHI lai ba truong cho %d chuong.' % len(teps))
    else:
        print('  chi BAO — them --ghi de ghi vao frontmatter.')
    print('  Luu y: lượng dùng đếm từ THÂN CHƯƠNG, không từ tệp kèm trích.')
    print('  kiem_ngan_sach_trich.py đo SIDECAR; hai con số lệch nhau nghĩa là sidecar đã lạc.')
    return 1 if xau else 0


if __name__ == '__main__':
    sys.exit(main())
