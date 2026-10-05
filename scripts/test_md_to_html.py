"""Test cho md_to_html.py — ket xuat ban do sach bac A.

Bon ca bien do that tren 32 cuon (2026-10-03):
  - 5/32 cuon co <>&" trong TEN CHUONG (tau-nhom-han-quoc-phong Ch.01 la
    `"Nhom chi la thep nhe hon."`) -> khong escape thi trang vo.
  - 4/32 cuon dung CRLF.
  - 2/32 cuon khong khai pham vi o dau -> phai in nhan bao toan.
  - inside-the-box co 0 so do va 2 canh phu thuoc -> phai AN muc, khong in
    khung trong.

R-2 (ruling truoc khi thuc thi): test_render_and_gates dem 'class="card'
(KHONG dong dau ngoac) de khop voi cong --verify sau nay, vi cong do cung
dem nhu vay va se bo sot the 'class="card red"' neu dem 'class="card"'.
Mot test va mot cong chung ten phai do cung mot thu.

R-3: them test_arc_svg_renders — khong test nao trong brief goi arc_svg vi
BOOK fixture chi sinh 1 canh (< MIN_EDGES=5) nen muc do thi bi AN va ham
khong bao gio chay. Fixture rieng duoi day co 6 chuong, >=30 dong than moi
chuong (de pick_level khong bao 'MUC LUC'), va duoc noi de crossrefs tra ve
>= 5 canh tong.
"""
import importlib.util
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'md_to_html.py')

def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

mth = load('mth', 'md_to_html.py')

FAILED = []

def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name +
          (('  -> ' + str(detail)) if detail and not cond else ''))
    if not cond:
        FAILED.append(name)


BOOK = '\n'.join(
    ['# BẢN NỘI BỘ — Workshop X', '',
     '# Phần I — Mở', '',
     '# Chương 01 — "Nhôm chỉ là thép nhẹ hơn." & <script>alert(1)</script>'] +
    ['Chương 02 nói rõ hơn.'] * 50 +
    ['```mermaid', 'graph TD', 'A-->B', '```'] +
    ['# Chương 02 — Bình thường'] + ['than hai'] * 50 +
    ['# Phụ lục'] + ['phu luc'] * 20)

def mkbook(tmp, body=BOOK, outline=None, scope=None):
    d = os.path.join(tmp, 'sach-thu')
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, 'book.md'), 'w', encoding='utf-8').write(body)
    if outline is not None:
        io.open(os.path.join(d, 'Phase3-Outline.md'), 'w',
                encoding='utf-8').write(outline)
    if scope is not None:
        io.open(os.path.join(d, '_scope_decision.md'), 'w',
                encoding='utf-8').write(scope)
    return d


# --- Review Focus 1: ten chuong co <>&"
def test_escape():
    out = mth.esc('A & B < C > D "E"')
    for bad in ('<C', '>D'):
        check('escape: bo %r khoi dau ra' % bad, bad not in out, out)
    check('escape: & thanh &amp;', '&amp;' in out, out)
    check('escape: " thanh &quot;', '&quot;' in out, out)
    check('escape: **in dam** thanh <b>', mth.esc('**x**') == '<b>x</b>',
          mth.esc('**x**'))
    check('escape: *in nghieng* thanh <i>', mth.esc('*x*') == '<i>x</i>',
          mth.esc('*x*'))
    # Loi da gap: `**... *noi* ...**` lam regon non-greedy dut giua cau
    nested = mth.esc('**chức năng *nổi* một nút**')
    check('escape: ** long * khong de sot dau **', '**' not in nested, nested)


def test_render_and_gates():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        rep = mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()

        check('BI-3: khong goi tai nguyen mang',
              'src="http' not in h and 'href="http' not in h, 'co URL ngoai')
        check('bac A: khong co <script>', '<script' not in h.lower(), 'co script')
        check('khong co chu thich HTML', '<!--' not in h, 'co <!--')
        check('BI-4: nhan pham vi trong THAN trang', 'NỘI BỘ' in h, 'thieu nhan')
        # R-2: dem 'class="card' (khong dong dau ngoac) de khop cong --verify,
        # vi cong do khong dong dau ngoac va se bo sot the 'class="card red"'.
        check('so the chuong == so chuong parse duoc',
              h.count('class="card') == len(rep['chapters']),
              '%d vs %d' % (h.count('class="card'), len(rep['chapters'])))
        check('Review Focus 1: thay <script> cua TEN CHUONG da bi escape',
              '&lt;script&gt;' in h, 'ten chuong chua escape')
        check('dem so do tren the == dem trong book.md',
              rep['mermaid_page'] == rep['mermaid_src'],
              '%s vs %s' % (rep['mermaid_page'], rep['mermaid_src']))


# --- inside-the-box: 0 so do, 2 canh => phai AN muc
def test_hide_empty_sections():
    with tempfile.TemporaryDirectory() as tmp:
        thin = '\n'.join(['# Chương 01 — A'] + ['than'] * 40 +
                          ['# Chương 02 — B'] + ['than'] * 40)
        d = mkbook(tmp, body=thin)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        check('an do thi khi qua it canh', 'class="arcbox"' not in h,
              'in khung do thi trong')
        check('an bang 🔴 khi dan y khong co dong Rủi ro',
              'class="risktable"' not in h, 'in bang rui ro trong')
        check('BI-4: khong khai pham vi => nhan bao toan',
              'CHƯA KHAI' in h, 'thieu nhan bao toan')


# --- R-3: arc_svg phai thuc su chay khi co >= MIN_EDGES canh
ARC_TITLES = ['Mở đầu', 'Nền tảng', 'Triển khai', 'Kiểm chứng', 'Mở rộng', 'Kết']
ARC_REFS = {1: [3, 5], 2: [4, 6], 3: [1]}  # tong 5 canh >= MIN_EDGES=5

def _arc_book():
    parts = []
    for n in range(1, 7):
        head = '# Chương %02d — %s' % (n, ARC_TITLES[n - 1])
        body = ['nội dung thân chương dài để vượt ngưỡng MUC_LUC.'] * 28
        for t in ARC_REFS.get(n, []):
            body.append('Xem thêm Chương %d để biết chi tiết liên quan.' % t)
        while len(body) < 30:
            body.append('nội dung thân chương dài để vượt ngưỡng MUC_LUC.')
        parts.append('\n'.join([head] + body))
    return '\n'.join(parts)


def test_arc_svg_renders():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, body=_arc_book())
        out = os.path.join(tmp, 'map.html')
        rep = mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        check('arc_svg: hien khung do thi khi >= MIN_EDGES canh',
              'class="arcbox"' in h, 'thieu arcbox')
        check('arc_svg: co it nhat 1 duong cung <path d=',
              '<path d=' in h, 'khong co path nao')
        check('arc_svg: so <circle> == so chuong',
              h.count('<circle') == len(rep['chapters']),
              '%d vs %d' % (h.count('<circle'), len(rep['chapters'])))
        check('arc_svg: van khong co <script>', '<script' not in h.lower(),
              'co script')
        check('arc_svg: van khong goi tai nguyen mang',
              'src="http' not in h and 'href="http' not in h, 'co URL ngoai')


# --- Review Focus 5: duong dan co dau tieng Viet + khoang trang
def test_vietnamese_path():
    with tempfile.TemporaryDirectory() as tmp:
        d = os.path.join(tmp, 'Sách Thử Nghiệm — bản nháp')
        os.makedirs(d)
        io.open(os.path.join(d, 'book.md'), 'w', encoding='utf-8').write(BOOK)
        out = os.path.join(d, 'bản đồ.html')
        rep = mth.build(d, out)
        check('duong dan co dau: dung duoc', os.path.exists(out), out)
        check('duong dan co dau: slug giu nguyen dau',
              'Sách' in os.path.basename(d), d)
        h = io.open(out, encoding='utf-8').read()
        check('duong dan co dau: ten sach tren trang doc duoc',
              'Thử Nghiệm' in h, 'mat dau trong tieu de')
        check('duong dan co dau: van ra 2 chuong', len(rep['chapters']) == 2,
              sorted(rep['chapters']))


def test_crlf_render():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, body=BOOK.replace('\n', '\r\n'))
        out = os.path.join(tmp, 'map.html')
        rep = mth.build(d, out)
        check('CRLF: van ra dung 2 chuong', len(rep['chapters']) == 2,
              sorted(rep['chapters']))
        h = io.open(out, encoding='utf-8').read()
        check('CRLF: khong con \\r trong ten chuong tren trang',
              '\r' not in h, 'con \\r')


if __name__ == '__main__':
    test_escape(); test_render_and_gates(); test_hide_empty_sections()
    test_arc_svg_renders()
    test_crlf_render(); test_vietnamese_path()
    print()
    if FAILED:
        print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
        sys.exit(1)
    print('Tat ca PASS')
