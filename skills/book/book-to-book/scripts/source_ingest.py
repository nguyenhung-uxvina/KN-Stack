# -*- coding: utf-8 -*-
"""Dựng KHO NGỮ LIỆU GỐC cho /book-to-book — sự thật nền của mọi phép đo về sau.

Vì sao tồn tại
--------------
`notebook-to-book` lấy nội dung sách qua NotebookLM. Đo trên lần chạy Cross 5e
(2026-09-07): để NLM tự do ở P1 thì **18/378 trích dẫn không đối chiếu được** —
NLM sửa chữ rồi vẫn đóng ngoặc kép. Bài học đã trả giá: *có PDF trong tay thì
đừng đi vòng qua NLM.* Script này đọc thẳng tệp gốc, nên mọi trích dẫn ở các pha
sau đều có chỗ để đối chiếu, và `fidelity_audit.py` có mẫu số thật để tính
tỷ lệ nguyên bản.

Nó làm ba việc, không làm gì khác:
  1. Rút text từ PDF / EPUB / MD / TXT.
  2. Chuẩn hoá, xử **bốn nguồn âm tính giả** đã từng làm báo sai 7% trong khi
     thật là 0% (xem `norm()`).
  3. Dựng bảng ánh xạ *trang in → vị trí trong kho* từ running header, để mọi
     trích dẫn về sau trả được số trang in — số mà người đọc kiểm lại được.

Chạy
----
    python source_ingest.py <tệp nguồn> -o <output_dir> [--label Cross] [--offset auto|N]

Sinh ra trong `<output_dir>/_source/`:
    <label>.corpus.txt   kho đã chuẩn hoá, nối liền (một dòng)
    <label>.pagemap.json [[vị_trí_ký_tự, trang_in], ...]
    <label>.meta.json    {words, pages, offset_mode, sha256, path, ...}

Mã thoát: 0 = xong · 2 = không đọc được nguồn / nguồn rỗng.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import sys
import unicodedata
import zipfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Ligature, nháy cong, gạch ngang unicode, non-breaking space, dấu lược.
LIG = {
    'ﬀ': 'ff', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬃ': 'ffi', 'ﬄ': 'ffl',
    '‘': "'", '’': "'", '“': '"', '”': '"',
    '–': '-', '—': '-', '−': '-', ' ': ' ', '…': '...',
}


def norm(s: str) -> str:
    """Chuẩn hoá để so chuỗi. Thứ tự các bước KHÔNG đổi được.

    Bốn nguồn âm tính giả mà hàm này tồn tại để chặn (đo trên P&B 629 trang:
    43 ca trượt lượt đầu, 36 trong đó là giả):

      1. PDF ngắt từ bằng gạch nối + xuống dòng: ``de-\\nsign``. Phải gỡ gạch nối
         TRƯỚC khi gộp khoảng trắng — gỡ gạch mà để xuống dòng thành dấu cách
         sẽ ra ``de sign`` và trượt.
      2. Ligature ``ﬁ ﬂ`` và nháy cong.
      3. Dấu nhấn Markdown, ký hiệu hạ chỉ, ký tự lạ — gộp hết về khoảng trắng.
      4. (xử ở nơi khác) Câu vắt qua chỗ ngắt trang: vì thế kho được NỐI LIỀN
         thành một chuỗi, không bao giờ dò theo từng trang.

    Giữ chữ cái Unicode nên tiếng Việt có dấu vẫn so được — `[^a-z0-9]` kiểu cũ
    sẽ nghiền nát tiếng Việt và cho âm tính giả im lặng.
    """
    s = unicodedata.normalize('NFKC', s)
    for k, v in LIG.items():
        s = s.replace(k, v)
    s = s.replace('­', '')                 # soft hyphen
    s = re.sub(r'[-‐‑]\s*\n\s*', '', s)   # ngắt từ qua dòng
    s = s.lower()
    s = re.sub(r'[^0-9a-zÀ-ɏḀ-ỿ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def words(s: str) -> int:
    return len(s.split()) if s else 0


# ---------------------------------------------------------------- đọc nguồn

def read_pdf(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit('!! thiếu pypdf — cài: pip install pypdf')
    reader = PdfReader(path)
    return [(pg.extract_text() or '') for pg in reader.pages]


def _strip_html(html: str) -> str:
    html = re.sub(r'(?is)<(script|style).*?</\1>', ' ', html)
    html = re.sub(r'(?i)<br\s*/?>|</p>|</div>|</h[1-6]>', '\n', html)
    html = re.sub(r'(?s)<[^>]+>', ' ', html)
    for ent, ch in (('&nbsp;', ' '), ('&amp;', '&'), ('&lt;', '<'),
                    ('&gt;', '>'), ('&quot;', '"'), ('&#39;', "'")):
        html = html.replace(ent, ch)
    return html


def read_epub(path):
    """EPUB = zip chứa HTML. Đọc theo thứ tự spine của OPF; hỏng thì theo tên tệp."""
    out = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        opf = next((n for n in names if n.lower().endswith('.opf')), None)
        order = []
        if opf:
            try:
                x = z.read(opf).decode('utf-8', 'replace')
                base = os.path.dirname(opf)
                manifest = {}
                for tag in re.findall(r'<item\b[^>]*>', x):
                    mid = re.search(r'\bid="([^"]+)"', tag)
                    href = re.search(r'\bhref="([^"]+)"', tag)
                    if mid and href:
                        manifest[mid.group(1)] = href.group(1)
                for idref in re.findall(r'<itemref\b[^>]*idref="([^"]+)"', x):
                    href = manifest.get(idref)
                    if not href:
                        continue
                    full = os.path.normpath(os.path.join(base, href)).replace('\\', '/')
                    if full in names:
                        order.append(full)
            except Exception:
                order = []
        if not order:
            order = sorted(n for n in names
                           if n.lower().endswith(('.xhtml', '.html', '.htm')))
        for n in order:
            out.append(_strip_html(z.read(n).decode('utf-8', 'replace')))
    return out


def read_plain(path):
    txt = io.open(path, encoding='utf-8', errors='replace').read()
    # Tách theo dấu ngắt trang nếu có, không thì coi cả tệp là một "trang".
    parts = txt.split('\f')
    return parts if len(parts) > 1 else [txt]


def load_source(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return read_pdf(path), 'pdf'
    if ext == '.epub':
        return read_epub(path), 'epub'
    if ext in ('.md', '.txt'):
        return read_plain(path), 'text'
    sys.exit('!! định dạng %s chưa đọc được. Chạy /doc-to-md để chuyển sang .md '
             'rồi nạp lại bản .md đó.' % (ext or '(không đuôi)'))


# ------------------------------------------------------- số trang in (header)

PAGENUM = re.compile(r'(?<![0-9])([0-9]{1,4})(?![0-9])')


def anchor_printed_page(raw: str):
    """Rút số trang in từ running header/footer của MỘT trang.

    Header P&B dạng ``12.2 Experiences of Applying… 569`` hoặc ``198 6 Conceptual
    Design`` — số in nằm ở đầu hoặc cuối của dòng đầu/dòng cuối. Trang mở chương
    thường KHÔNG có header; trả None để lượt nội suy lo.
    """
    lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        return None
    cands = []
    for l in (lines[0], lines[-1]) if len(lines) > 1 else (lines[0],):
        # Dòng chạy đầu/cuối trang KHÔNG BAO GIỜ chứa dấu '='. Bảng đổi đơn vị thì có,
        # và nó bắt đầu bằng một chữ số nên trông y hệt số trang.
        # Đo thật (Sadraey 2026-09-15): hai trang cuối mục Ký hiệu — đánh số La Mã
        # xxix và xxx — kết bằng dòng đổi đơn vị mở đầu bằng '1'. Bộ dò nhận chúng
        # làm trang in 1, nên trang in 1 THẬT (pdf idx 28) bị ba trang cùng nhận.
        # Lọc đồng thuận độ lệch KHÔNG cứu được ca này: độ lệch −25/−26 mà hai neo
        # giả hàm ý đều có thật ở chỗ khác trong sách.
        if '=' in l:
            continue
        m = PAGENUM.match(l) or PAGENUM.search(l[-8:])
        if m:
            n = int(m.group(1))
            if 1 <= n <= 3000:
                cands.append(n)
    return cands[0] if cands else None


def build_pagemap(raw_pages, mode, kind='pdf'):
    """Trả (danh sách (chỉ_số_0based, số_neo), số_neo_dò_được, độ_lệch, loại_neo).

    `mode` = 'auto' (dò header, nội suy chỗ thiếu) hoặc số nguyên = độ lệch cố
    định (trang in = trang pdf - N). Độ lệch thật thường KHÔNG đều (P&B đo được
    +17 rồi +12), nên 'auto' là mặc định và độ lệch cố định chỉ dùng khi đã kiểm
    tay vài mốc.

    🔴 CHỈ PDF MỚI CÓ SỐ TRANG IN. EPUB/MD không có khái niệm trang: chạy bộ dò
    running header trên chúng thì nó bắt phải con số đầu tiên trông giống số
    trang — đo thật trên "Inside the Box": nó nhặt **1989** (một năm trong văn
    bản) rồi đánh số cả cuốn từ 1989 đến 2010. Một số trang SAI tệ hơn không có
    số trang: không có thì người viết biết là mình không có neo; có số giả thì
    trích dẫn mang neo sai ra ngoài mà không ai nghi ngờ.
    """
    n = len(raw_pages)
    if kind != 'pdf':
        return [(i, i + 1) for i in range(n)], 0, None, 'muc'
    if mode != 'auto':
        off = int(mode)
        return [(i, i + 1 - off) for i in range(n)], n, off, 'trang_in'

    # ── Luật ĐỒNG THUẬN ĐỘ LỆCH (thay luật đơn điệu cũ) ────────────────────────
    # Số trang chạy thật cho độ lệch (trang_in − chỉ_số_pdf) **lặp lại hàng trăm
    # lần**; số bắt nhầm từ MỤC LỤC hay bảng biểu cho độ lệch tản mác. Lọc theo
    # đồng thuận bắt được cả hai loại rác mà luật cũ không bắt được.
    #
    # Vì sao bỏ luật đơn điệu: nó xét mỗi neo so với **neo liền trước**, nên một
    # neo rác nhận sớm sẽ loại sạch các neo THẬT phía sau. Đo thật hai lần trên
    # cùng cuốn "Aircraft Design" (2026-09-15):
    #   · neo `2001` (một năm ở trang bìa) ⇒ loại 752/753 neo thật;
    #   · neo `2·7·12` (số trang tham chiếu trong MỤC LỤC, pdf idx 6–12) ⇒ loại
    #     các neo thật `1·3·6·9·12` ở pdf idx 27–39, khiến trang in 1–12 bị gán
    #     thành 28–39 (lệch +27). Lỗi chỉ nằm ở 1,5% cuốn sách nên phép kiểm tay
    #     40 trang NGẪU NHIÊN không đụng vào — phải lấy mẫu ở MÉP mới thấy.
    cands = []
    for i, raw in enumerate(raw_pages):
        p = anchor_printed_page(raw)
        if p is None:
            continue
        # Trang in không thể vượt chỉ số trang PDF: bìa và front matter chỉ đẩy
        # trang PDF chạy trước trang in, không bao giờ ngược lại.
        if p > i + 1:
            continue
        cands.append((i, p))

    dem = {}
    for i, p in cands:
        dem[p - i] = dem.get(p - i, 0) + 1
    # Ngưỡng: một độ lệch THẬT phải lặp nhiều lần. Giữ cả nhiều độ lệch cùng lúc —
    # độ lệch thật hay đổi giữa sách (P&B đo được +17 rồi +12) nên khoá vào đúng
    # một giá trị là sai; thứ cần loại là những độ lệch chỉ xuất hiện lác đác.
    nguong = max(5, int(0.02 * n))
    tot = {o for o, c in dem.items() if c >= nguong}
    anchors = [(i, p) for i, p in cands if (p - i) in tot]

    pages = []
    for i in range(n):
        before = [a for a in anchors if a[0] <= i]
        after = [a for a in anchors if a[0] > i]
        if before:
            j, p = before[-1]
            pages.append((i, p + (i - j)))
        elif after:
            # TRƯỚC neo đầu tiên là front matter (bìa, mục lục, lời tựa) — phần này
            # đánh số LA MÃ hoặc không đánh số. Nội suy ngược ra số Ả-rập ở đây sinh
            # ra những "trang −4", và một số trang vô nghĩa vẫn bị đem đi trích dẫn
            # y như số thật. Trả None: không có số thì nói là không có.
            j, p = after[0]
            lui = p - (j - i)
            pages.append((i, lui if lui >= 1 else None))
        else:
            pages.append((i, i + 1))
    # Dò được quá ít neo thì số trang chỉ là suy diễn. Dán nhãn thôi là KHÔNG ĐỦ:
    # bản vá trước chỉ đổi tên loại neo mà vẫn ghi nguyên dãy số nội suy vào pagemap,
    # nên người viết ở P4 vẫn thấy "tr.2417" và vẫn trích dẫn nó. Nhãn không ngăn
    # được một con số bị đem đi dùng — chỉ có việc KHÔNG SINH RA con số ấy mới ngăn.
    # Dưới ngưỡng ⇒ trả về TRANG PDF VẬT LÝ: kiểm được bằng cách mở tệp đếm tới,
    # trong khi số nội suy từ một neo rác thì không kiểm được bằng gì.
    if len(anchors) < max(3, 0.3 * n):
        return [(i, i + 1) for i in range(n)], len(anchors), None, 'trang_pdf'
    return pages, len(anchors), None, 'trang_in'


# ------------------------------------------------------------------- chạy

def ingest(path, outdir, label, offset_mode):
    raw_pages, kind = load_source(path)
    pages, n_anchor, fixed_off, loai_neo = build_pagemap(raw_pages, offset_mode, kind)
    printed = dict(pages)

    parts, index, pos = [], [], 0
    for i, raw in enumerate(raw_pages):
        t = norm(raw)
        if not t:
            continue
        index.append([pos, printed.get(i, i + 1)])
        parts.append(t)
        pos += len(t) + 1
    corpus = ' '.join(parts)

    # Sàn khác nhau theo loại nguồn: PDF/EPUB ít chữ gần như chắc chắn là bản
    # SCAN (ảnh, không có lớp text) hoặc bị DRM; .md/.txt ít chữ thì chỉ là tệp
    # rỗng. Cả hai đều phải dừng — kho rỗng mà chạy tiếp thì mọi tỷ lệ về sau
    # bằng 0, và 0 ở đó đọc y hệt "sạch".
    san = 20 if kind == 'text' else 200
    if words(corpus) < san:
        if kind == 'text':
            print('!! kho ngữ liệu chỉ %d từ — nguồn rỗng hoặc sai tệp.' % words(corpus))
        else:
            print('!! kho ngữ liệu chỉ %d từ trên %d trang — nguồn nhiều khả năng là bản '
                  'SCAN (ảnh, không có lớp text) hoặc bị DRM. Không đo được tỷ lệ nguyên '
                  'bản trên nguồn này; chạy OCR trước (xem /doc-to-md luật 6) rồi nạp lại '
                  'bản .md.' % (words(corpus), len(raw_pages)))
        return 2

    sdir = os.path.join(outdir, '_source')
    os.makedirs(sdir, exist_ok=True)
    io.open(os.path.join(sdir, label + '.corpus.txt'), 'w',
            encoding='utf-8', newline='\n').write(corpus)
    io.open(os.path.join(sdir, label + '.pagemap.json'), 'w',
            encoding='utf-8', newline='\n').write(json.dumps(index))

    # pageindex = ánh xạ chỉ_số_trang_PDF → trang_in. KHÁC pagemap (vị trí ký tự →
    # trang in). `page_raw.py` cần nó để mở ĐÚNG trang PDF lấy văn bản THÔ — đường
    # duy nhất kiểm được một CON SỐ, vì kho đã chuẩn hoá thì mất dấu trừ, dấu thập
    # phân và số mũ. Ghi ngay ở đây thay vì bắt chạy một script riêng về sau: một
    # bước phụ thuộc trí nhớ là một bước sẽ bị quên.
    io.open(os.path.join(sdir, label + '.pageindex.json'), 'w',
            encoding='utf-8', newline='\n').write(
        json.dumps({'kind': loai_neo, 'anchors': n_anchor,
                    'map': [[i, p] for i, p in pages]}))

    meta = {
        'label': label,
        'path': os.path.abspath(path),
        'kind': kind,
        'pages': len(raw_pages),
        'pages_with_text': len(parts),
        'words': words(corpus),
        'chars': len(corpus),
        'offset_mode': 'auto' if offset_mode == 'auto' else int(offset_mode),
        'header_anchors': n_anchor if offset_mode == 'auto' else None,
        'page_kind': loai_neo,
        'sha256': hashlib.sha256(io.open(path, 'rb').read()).hexdigest(),
    }
    io.open(os.path.join(sdir, label + '.meta.json'), 'w',
            encoding='utf-8', newline='\n').write(
        json.dumps(meta, ensure_ascii=False, indent=2))

    print('=' * 76)
    print('KHO NGỮ LIỆU GỐC — %s' % label)
    print('=' * 76)
    print('  nguồn        : %s (%s)' % (os.path.basename(path), kind))
    print('  trang        : %d (có text: %d)' % (meta['pages'], meta['pages_with_text']))
    print('  TỪ GỐC       : %d   ← mẫu số của mọi tỷ lệ nguyên bản về sau' % meta['words'])
    if loai_neo == 'muc':
        print('  neo           : theo MỤC (%d mục) — %s KHÔNG có số trang in.'
              % (len(parts), kind.upper()))
        print('                 Trích dẫn về sau neo bằng "mục k/%d", KHÔNG được ghi '
              '"tr.N".' % len(parts))
        print('                 Cần số trang in thì phải có bản PDF của đúng lần xuất bản ấy.')
    elif offset_mode == 'auto':
        pct = 100.0 * n_anchor / max(len(raw_pages), 1)
        print('  neo trang in : %d/%d trang (%.0f%%) — còn lại nội suy'
              % (n_anchor, len(raw_pages), pct))
        if loai_neo == 'trang_pdf':
            print('  🔴 TỪ CHỐI SINH SỐ TRANG IN. Dưới 30%% trang có running header đọc '
                  'được (%d/%d), nên mọi "số trang in" sẽ là nội suy từ quá ít neo.'
                  % (n_anchor, len(raw_pages)))
            print('                 Neo thay thế: **TRANG PDF VẬT LÝ** (1..%d). Trích dẫn '
                  'về sau ghi "tr.PDF N",' % len(parts))
            print('                 KHÔNG được ghi "tr.N" như số trang in — hai thứ lệch '
                  'nhau đúng bằng độ dày front matter.')
            print('                 Muốn số trang in thật: kiểm tay 3-4 mốc rồi chạy lại '
                  'với --offset N.')
        if index:
            print('  mốc kiểm     : pdf tr.1 → in tr.%s · pdf tr.%d → in tr.%s'
                  % (index[0][1], len(parts), index[-1][1]))
    else:
        print('  độ lệch      : cố định %d (trang in = trang pdf - %d)'
              % (meta['offset_mode'], meta['offset_mode']))
    print('  ghi vào      : %s' % sdir)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Dựng kho ngữ liệu gốc cho /book-to-book')
    ap.add_argument('source', help='tệp sách gốc (.pdf/.epub/.md/.txt)')
    ap.add_argument('-o', '--outdir', required=True, help='thư mục Data Bus của cuốn sách')
    ap.add_argument('--label', default=None, help='nhãn nguồn (mặc định: tên tệp)')
    ap.add_argument('--offset', default='auto',
                    help="'auto' (dò running header) hoặc số nguyên: trang in = trang pdf - N")
    a = ap.parse_args(argv)

    if not os.path.isfile(a.source):
        print('!! không thấy tệp nguồn: %s' % a.source)
        return 2
    label = a.label or re.sub(r'[^0-9A-Za-z]+', '-',
                              os.path.splitext(os.path.basename(a.source))[0])[:40].strip('-')
    return ingest(a.source, a.outdir, label, a.offset)


if __name__ == '__main__':
    sys.exit(main())
