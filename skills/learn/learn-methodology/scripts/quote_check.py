# -*- coding: utf-8 -*-
"""Cổng trích dẫn cho /learn-methodology --source: mọi «…» trong đầu ra có thật trong sách không.

Vì sao là script chứ không phải lời dặn
---------------------------------------
Ở chế độ --source, giá trị duy nhất của đầu ra là nó BÁM SÁCH. Một phép so sánh
Feynman hay một từ viết tắt Mnemonic thì AI được tự nghĩ; nhưng câu "sách nói X"
thì phải có X trong sách. Dặn "hãy trích nguyên văn" không đủ: NLM sửa chữ rồi vẫn
đóng ngoặc (đo trên Cross 5e: 18/378 trích dẫn không đối chiếu được), và agent tự
chép từ trí nhớ thì trông y hệt chép từ sách. Chỉ đối chiếu máy mới tách được hai
thứ đó.

Vì sao không dùng lại quote_locate.py của book-to-book
------------------------------------------------------
Hàm norm() ở đó xoá mọi ký tự ngoài [a-z0-9]. Với sách tiếng Anh thì ổn, nhưng:
  * sách tiếng Việt: "nguyên lý" và "nguyên lỹ" đều thành "nguy n l" → trích sai dấu vẫn qua;
  * con số: "7.5" và "7,5" đều thành "7 5" → trích sai số vẫn qua.
norm() dưới đây giữ chữ Unicode và giữ dấu thập phân/nghìn nằm GIỮA hai chữ số.

Dùng
----
    python quote_check.py <đầu ra .md> --nguon <tệp|thư mục> [--nguon ...] [--min-tu 5]

Nguồn nhận: .md .txt .pdf .epub, hoặc thư mục chứa chúng (đệ quy) — ví dụ
`BOOK/_source/` do /book-to-learn L2 sinh, hoặc thư mục dump nội dung nguồn NLM.

Quy ước trong đầu ra: trích dẫn nguyên văn đặt trong «…». Được lược bằng […] hoặc …;
mỗi đoạn ≥ 2 từ giữa các chỗ lược đều phải có trong nguồn.

Mã thoát: 0 = mọi trích dẫn đều thấy · 1 = có trích không thấy / quá ngắn / không có
trích nào · 2 = không đo được (nguồn không đọc được, rỗng, hoặc PDF không có lớp chữ).
"""
from __future__ import annotations

import argparse
import bisect
import html
import io
import os
import re
import sys
import unicodedata
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DUOI = ('.md', '.txt', '.pdf', '.epub')
MAP = {
    '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"',
    '\u2013': '-', '\u2014': '-', '\u2212': '-', '\u00a0': ' ',
}
LUOC = re.compile(r'\[\s*(?:…|\.\.\.)\s*\]|…|\.\.\.')


def norm(s: str, noi_gach=False) -> str:
    """Chuẩn hoá để so chuỗi. Thứ tự các bước KHÔNG đổi được."""
    s = unicodedata.normalize('NFKC', s)          # NFD → NFC (tiếng Việt), ligature ﬁ → fi
    s = s.replace('\u00ad', '')                    # soft hyphen
    for a, b in MAP.items():
        s = s.replace(a, b)
    s = re.sub(r'(?<=\w)-[ \t]*\r?\n\s*(?=\w)', '', s)   # PDF ngắt từ: de-\nsign → design
    if noi_gach:
        s = re.sub(r'(?<=\w)-(?=\w)', '', s)       # self-reliance → selfreliance (khớp bản vừa nối)
    s = s.lower()
    s = re.sub(r'(?<=\d)\.(?=\d)', '\x00', s)      # 7.5 giữ nguyên
    s = re.sub(r'(?<=\d),(?=\d)', '\x01', s)       # 1,200 giữ nguyên
    s = re.sub(r'(^|\s)-(?=\d)', '\\1\x02', s)     # -3.2 giữ dấu trừ
    s = re.sub(r'[^\w\s\x00\x01\x02]|_', ' ', s)
    s = s.replace('\x00', '.').replace('\x01', ',').replace('\x02', '-')
    return ' '.join(s.split())


# ---------------------------------------------------------------- đọc nguồn

def _pdf_fitz(path):
    import fitz  # pymupdf
    with fitz.open(path) as doc:
        return [p.get_text() for p in doc]


def _pdf_pypdf(path):
    from pypdf import PdfReader
    return [(p.extract_text() or '') for p in PdfReader(path).pages]


def _doc_pdf(path):
    """Đọc bằng CẢ HAI thư viện, mỗi trang là hợp của hai bản.

    Đo thật 2026-09-19 trên Borchert, The Very Long Game, tr.16: pymupdf trả 343 từ
    nhưng thiếu nguyên đoạn "First, a regional perspective suggests…" mà pypdf đọc
    được. Đọc một thư viện thì trích dẫn đúng bị báo KHÔNG THẤY, và người dùng sẽ học
    cách lờ cổng đi. Chỉ cần có mặt, không cần thứ tự, nên ghép hai bản là an toàn.
    """
    ban = []
    for doc in (_pdf_fitz, _pdf_pypdf):
        try:
            ban.append(doc(path))
        except ImportError:
            continue
    if not ban:
        raise SystemExit('KHÔNG ĐO ĐƯỢC: cần pymupdf hoặc pypdf để đọc %s' % path)
    so_trang = max(len(b) for b in ban)
    return ['\n'.join(b[i] for b in ban if i < len(b)) for i in range(so_trang)]


def _doc_epub(path):
    out = []
    with zipfile.ZipFile(path) as z:
        for n in sorted(z.namelist()):
            if n.lower().endswith(('.xhtml', '.html', '.htm')):
                t = z.read(n).decode('utf-8', errors='replace')
                t = re.sub(r'<(script|style)[\s\S]*?</\1>', ' ', t, flags=re.I)
                t = re.sub(r'<[^>]+>', ' ', t)
                out.append((n, html.unescape(t)))
    return out


class Tep:
    """Một tệp nguồn: văn bản đã chuẩn hoá nối liền + bảng vị trí → đơn vị (trang/chương)."""

    def __init__(self, path):
        self.path = path
        self.ten = os.path.basename(path)
        ext = os.path.splitext(path)[1].lower()
        if ext == '.pdf':
            don_vi = [('trang PDF %d' % (i + 1), t) for i, t in enumerate(_doc_pdf(path))]
            self.kieu = 'pdf'
        elif ext == '.epub':
            don_vi = _doc_epub(path)
            self.kieu = 'epub'
        else:
            don_vi = [('', io.open(path, encoding='utf-8-sig', errors='replace').read())]
            self.kieu = 'text'
        self.ban = {}
        for noi in (False, True):
            dau, nhan, phan = [], [], []
            vt = 0
            for ten, t in don_vi:
                n = norm(t, noi)
                if not n:
                    continue
                dau.append(vt)
                nhan.append(ten)
                phan.append(n)
                vt += len(n) + 1
            self.ban[noi] = (' '.join(phan), dau, nhan)
        self.so_tu = len(self.ban[False][0].split())
        self.so_don_vi = len(don_vi)

    def tim(self, doan, noi):
        van, dau, nhan = self.ban[noi]
        i = (' ' + van + ' ').find(' ' + doan + ' ')
        if i < 0:
            return None
        a = nhan[bisect.bisect_right(dau, i) - 1]
        b = nhan[bisect.bisect_right(dau, i + len(doan) - 1) - 1]
        if not a:
            return self.ten
        if a == b:
            return '%s, %s' % (self.ten, a)
        if self.kieu == 'pdf':
            return '%s, %s–%s' % (self.ten, a, b.replace('trang PDF ', ''))
        return '%s, %s → %s' % (self.ten, a, b)


def nap_nguon(duong_dan):
    tep = []
    for p in duong_dan:
        if os.path.isdir(p):
            for goc, _, ds in os.walk(p):
                for f in sorted(ds):
                    if f.lower().endswith(DUOI):
                        tep.append(os.path.join(goc, f))
        elif os.path.isfile(p):
            tep.append(p)
        else:
            raise SystemExit('KHÔNG ĐO ĐƯỢC: không thấy nguồn %s' % p)
    if not tep:
        raise SystemExit('KHÔNG ĐO ĐƯỢC: không có tệp %s nào trong nguồn' % '/'.join(DUOI))
    out = []
    for p in sorted(tep):
        t = Tep(p)
        if t.kieu == 'pdf' and t.so_don_vi and t.so_tu < 5 * t.so_don_vi:
            print('CẢNH BÁO %s: %d trang mà chỉ %d từ — PDF scan không lớp chữ? Cần OCR trước.'
                  % (t.ten, t.so_don_vi, t.so_tu))
        out.append(t)
    if sum(t.so_tu for t in out) < 20:
        raise SystemExit('KHÔNG ĐO ĐƯỢC: nguồn gần như rỗng (%d từ). PDF scan thì OCR trước; '
                         'notebook NLM thì dump nội dung nguồn ra tệp trước.'
                         % sum(t.so_tu for t in out))
    return out


# ---------------------------------------------------------------- kiểm

def kiem(trich, kho, min_tu):
    """→ (trạng thái, vị trí|ghi chú). Trạng thái: OK | KHÔNG THẤY | QUÁ NGẮN."""
    doan = [norm(d) for d in LUOC.split(trich)]
    tong = sum(len(d.split()) for d in doan)
    if tong < min_tu:
        return 'QUÁ NGẮN', '%d từ < %d — quá ngắn để chứng minh là trích từ sách' % (tong, min_tu)
    can = [(d, norm(g, True)) for d, g in zip(doan, LUOC.split(trich)) if len(d.split()) >= 2]
    vi_tri = None
    for d, d_noi in can:
        thay = None
        for t in kho:
            thay = t.tim(d, False) or t.tim(d_noi, True)
            if thay:
                break
        if not thay:
            return 'KHÔNG THẤY', ('đoạn «%s»' % _cat(d)) if len(can) > 1 else ''
        vi_tri = vi_tri or thay
    return 'OK', vi_tri


def _cat(s, n=70):
    s = ' '.join(s.split())
    return s if len(s) <= n else s[:n - 1] + '…'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Đối chiếu trích dẫn «…» với sách gốc')
    ap.add_argument('dau_ra', help='tệp đầu ra của /learn-methodology (.md)')
    ap.add_argument('--nguon', action='append', required=True,
                    help='tệp .md/.txt/.pdf/.epub hoặc thư mục; lặp lại cho cụm sách')
    ap.add_argument('--min-tu', type=int, default=5, help='số từ tối thiểu mỗi trích dẫn (mặc định 5)')
    a = ap.parse_args(argv)

    try:
        kho = nap_nguon(a.nguon)
        van = io.open(a.dau_ra, encoding='utf-8-sig').read()
    except SystemExit as e:
        print(e)
        return 2
    except (OSError, zipfile.BadZipFile, RuntimeError, ValueError) as e:
        print('KHÔNG ĐO ĐƯỢC: %s' % e)
        return 2

    trich = re.findall(r'«(.*?)»', van, flags=re.S)
    print('quote_check — %d trích dẫn · nguồn: %d tệp, %d từ'
          % (len(trich), len(kho), sum(t.so_tu for t in kho)))
    if not trich:
        print('KHÔNG CÓ TRÍCH DẪN NÀO trong %s. Chế độ --source bắt buộc mỗi khẳng định '
              'lấy từ sách có trích nguyên văn trong «…».' % a.dau_ra)
        return 1

    dem = {'OK': 0, 'KHÔNG THẤY': 0, 'QUÁ NGẮN': 0}
    for q in trich:
        tt, ghi = kiem(q, kho, a.min_tu)
        dem[tt] += 1
        print('%-10s «%s»%s' % (tt, _cat(q), (' → ' if tt == 'OK' else ' — ') + ghi if ghi else ''))
    print('Tổng: %d/%d thấy · %d không thấy · %d quá ngắn'
          % (dem['OK'], len(trich), dem['KHÔNG THẤY'], dem['QUÁ NGẮN']))
    return 0 if dem['OK'] == len(trich) else 1


if __name__ == '__main__':
    sys.exit(main())
