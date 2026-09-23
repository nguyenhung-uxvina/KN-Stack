# -*- coding: utf-8 -*-
"""Neo lại số trang cho MỌI trích dẫn trong mọi tệp, sau khi bản đồ trang được sửa.

Vì sao pha này phải tồn tại. Bản đồ trang có thể sai, và đã sai hai lần trên cùng
một cuốn (neo `2001`; neo lấy từ mục lục làm lệch trang in 1–12 đi +27). Khi sửa
bản đồ, những số trang mà agent đã ghi vào tệp **không tự sửa theo**. Tệ hơn: một
phần agent chạy trước lúc sửa, một phần chạy sau, nên trong cùng một thư mục có
hai hệ số trang mà không gì phân biệt được bằng mắt.

Cách chặn đúng không phải là dặn agent chạy lại, mà là **neo lại bằng máy**: đọc
từng trích trong tệp, tra lại trong kho, và so số trang thật với số trang đang ghi.
Trích là thứ neo được; số trang là thứ suy ra từ nó.

    python reanchor.py <outdir> --glob "Phase1-Exploration/*.md"
    python reanchor.py <outdir> --glob "Phase6-Revised/Ch*.md" --sua

Không có `--sua` thì chỉ BÁO CÁO, không đụng tệp.
Mã thoát: 0 = mọi trích khớp · 1 = có lệch hoặc không tra được.
"""
from __future__ import annotations

import argparse
import glob as _glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quote_locate import Kho  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Trích nằm trong ngoặc kép thẳng hoặc cong. Đòi ≥6 từ: chuỗi ngắn hơn hay là
# thuật ngữ trong ngoặc ("Closed World"), không phải trích dẫn, và tra chúng chỉ
# sinh nhiễu.
NGOAC = re.compile(r'[""«]([^""»\n]{25,400})[""»]|"([^"\n]{25,400})"')
TRANG_GAN = re.compile(r'tr\.?\s*(\d{1,4})', re.IGNORECASE)


VIET = set('ăâđêôơưĂÂĐÊÔƠƯ')
DAU = set('àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ'
          'ÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ')


def la_tieng_viet(q):
    """Chuỗi trong ngoặc kép có phải LỜI CỦA NGƯỜI BIÊN SOẠN không?

    Người viết dùng ngoặc kép cho nhiều việc: trích nguồn, nhấn mạnh, đặt nhãn mục
    ('mất nghĩa / còn nghĩa / biến nghĩa'), gọi tên một khái niệm. Chỉ loại ĐẦU mới
    tra được trong kho. Đem cả ba loại kia đi tra thì cổng báo "không tìm thấy" hàng
    loạt — đo thật lần đầu chạy: 91 báo động, phần lớn là câu tiếng Việt của chính
    agent.

    Dương tính giả ở cổng đắt hơn nó trông: nó làm người đọc mất lòng tin vào cả
    bảng, kể cả những dòng đúng. Đây là lần thứ sáu trong dự án này.
    """
    return any(c in VIET or c in DAU for c in q)


def quet(path, kho):
    ket, bo_viet = [], 0
    for ln, raw in enumerate(io.open(path, encoding='utf-8'), start=1):
        for m in NGOAC.finditer(raw):
            q = m.group(1) or m.group(2)
            if len(q.split()) < 6:
                continue
            if la_tieng_viet(q):
                bo_viet += 1
                continue
            # Trích CÓ LƯỢC BỎ: "the thrust for turbojet engines ... is 12 m".
            # Phép so chuỗi không khớp được một chuỗi có lỗ ở giữa, nên nếu tra cả
            # cụm thì nó báo KHÔNG TÌM THẤY — một dương tính giả trên một trích hoàn
            # toàn hợp lệ. Tách theo dấu lược và tra TỪNG MẢNH; chỉ mảnh nào đủ dài
            # mới tra được, và phải khớp HẾT thì trích mới coi là có thật.
            manh = [x.strip() for x in re.split(r'\.\.\.|…', q) if len(x.split()) >= 4]
            if len(manh) > 1:
                rs = [kho.tra(x) for x in manh]
                if all(x['ok'] for x in rs):
                    r = dict(rs[0]); r['luoc'] = len(manh)
                else:
                    r = {'ok': False, 'ly_do': 'trich CO LUOC BO, manh khong khop het'}
            else:
                r = kho.tra(q)
            ghi = TRANG_GAN.findall(raw)
            ket.append((ln, q, r, ghi))
    return ket, bo_viet


def main(argv=None):
    ap = argparse.ArgumentParser(description='Neo lai so trang cho moi trich dan')
    ap.add_argument('outdir')
    ap.add_argument('--glob', default='Phase1-Exploration/*.md')
    ap.add_argument('--sua', action='store_true', help='ghi de so trang sai (mac dinh chi bao cao)')
    a = ap.parse_args(argv)

    kho = Kho(a.outdir)
    files = sorted(_glob.glob(os.path.join(a.outdir, a.glob)))
    if not files:
        print('!! khong thay tep nao khop %r' % a.glob)
        return 2

    tong = khop = lech = mat = mo_ho = bo_viet_tong = 0
    for f in files:
        ket, bo_viet = quet(f, kho)
        bo_viet_tong += bo_viet
        if not ket:
            continue
        xau = []
        for ln, q, r, ghi in ket:
            tong += 1
            if not r['ok']:
                mat += 1
                xau.append('    dong %-5d KHONG TRA DUOC | %s' % (ln, q[:60]))
            elif ghi and str(r['trang']) in ghi:
                khop += 1
            elif len(set(ghi)) > 1:
                # Dòng có NHIỀU số trang: một là neo của trích, (các) số kia trỏ sang
                # chỗ khác ("... trong khi tr.425 đã ghi ..."). Không có cách nào biết
                # số nào thuộc trích mà không hiểu nghĩa câu. Khai là KHÔNG PHÂN GIẢI
                # ĐƯỢC thay vì đoán — đoán ở đây đẻ ra dương tính giả trên những dòng
                # hoàn toàn đúng, và đó là cách nhanh nhất làm người đọc bỏ cả bảng.
                mo_ho += 1
                xau.append('    dong %-5d nhieu so trang tren dong (%s); that la tr.%s'
                           % (ln, '/'.join(sorted(set(ghi))[:3]), r['trang']))
            elif ghi:
                lech += 1
                xau.append('    dong %-5d ghi tr.%s  NHUNG THAT LA tr.%s | %s'
                           % (ln, ghi[0], r['trang'], q[:48]))
            else:
                khop += 1
        print('  %-44s %3d trich' % (os.path.basename(f), len(ket)))
        for x in xau:
            print(x)

    print('=' * 74)
    print('  tong %d trich ngoai ngu | khop %d | LECH SO TRANG %d | khong tra duoc %d'
          % (tong, khop, lech, mat))
    if mo_ho:
        print('  %d dong co NHIEU so trang — khong phan giai duoc bang may, doc tay.' % mo_ho)
    print('  da BO QUA %d chuoi tieng Viet trong ngoac kep (loi nguoi bien soan,'
          % bo_viet_tong)
    print('    khong phai trich nguon). Khai ra vi bo qua im lang cung la mot vung mu.')
    print('  --- CONG NAY KHONG NHIN THAY GI ---')
    print('  · trich KHONG dong ngoac kep (agent da chuyen thanh dien giai) — dung vay,')
    print('    nhung nghia la con so ben canh chung khong duoc kiem o day.')
    print('  · so trang dung ma trich SAI NGHIA: day la phep so CHUOI, khong phai phep')
    print('    so nghia. Dich sai van "khop".')
    print('  · con so TRONG trich (7.5, -3.2, 10^6): kho da tuoc dau, xem page_raw.py.')
    print('  · trich dan HINH/BANG neo bang so hinh chu khong bang chuoi van.')
    if a.sua:
        print('  !! --sua chua duoc cai dat: sua tay an toan hon khi so luong nho.')
    return 1 if (lech or mat) else 0


if __name__ == '__main__':
    sys.exit(main())
