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


def _rows(rep_rows):
    return {r[0]: r for r in rep_rows}

def test_verify_passes_clean():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('verify: sach lanh thi thoat 0', code == 0, code)
        for k in ('ty le phu', 'goi mang', 'the script', 'chu thich html',
                  'nhan pham vi', 'so the vs so chuong', 'so do the vs nguon',
                  'tieu de lac trong than chuong'):
            check('verify: co phep do %r' % k, k in r, sorted(r))
        check('verify: khong co dong CHAN',
              not [x for x in rows if x[3] == 'CHAN'],
              [x for x in rows if x[3] == 'CHAN'])


# --- DOI CHUNG AM 2: tiem the CDN => cong PHAI chan
def test_negative_cdn():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        io.open(out, 'w', encoding='utf-8').write(h.replace(
            '</head>', '<script src="https://cdn.jsdelivr.net/npm/x"></script></head>'))
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('DOI CHUNG AM CDN: cong thoat khac 0', code != 0, code)
        check('DOI CHUNG AM CDN: phep do goi mang bao CHAN',
              r['goi mang'][3] == 'CHAN', r['goi mang'])


# --- DOI CHUNG AM 3: bo nhan pham vi => cong PHAI chan
def test_negative_scope_label():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        io.open(out, 'w', encoding='utf-8').write(
            h.replace('NỘI BỘ', 'khong co gi').replace('CHƯA KHAI', 'khong co gi'))
        rows, code = mth.verify(out, d)
        check('DOI CHUNG AM nhan: cong thoat khac 0', code != 0, code)
        check('DOI CHUNG AM nhan: phep do nhan bao CHAN',
              _rows(rows)['nhan pham vi'][3] == 'CHAN',
              _rows(rows)['nhan pham vi'])


# --- Fix round 1 (2026-10-05): DOI CHUNG AM 3 (EOF) tren SACH THAT —
# khong phai tren bloat-ratio (hang do KHONG bat duoc loi nay — xem BLOAT_WARN),
# ma tren hang CAU TRUC moi 'tieu de lac trong than chuong'. Nam o LOP
# md_to_html vi day la hang trong bang verify(), khong phai ham DO thuan.
REAL_CORPUS = r'D:/Workshop_X/3_Resources/Books'

def test_negative_eof_real():
    book_dir = os.path.join(REAL_CORPUS, 'tu-khong-den-mot')
    if not os.path.exists(os.path.join(book_dir, 'book.md')):
        print('SKIP DOI CHUNG AM EOF (sach that) — khong thay %s'
              % book_dir)
        return
    # Mot ban RIENG cua md_to_html, chi TAT luat dung tren CHINH ban rieng
    # do (khong dung lai luc nao den ma san xuat) — mo phong dung loi
    # 'chuong chay den EOF': bo qua stop[], chi cat o 'hit' ke tiep/EOF.
    broken = load('mth_eof_real', 'md_to_html.py')
    def no_stop(txt):
        depth, hits, warn = broken.bmp.pick_level(broken.bmp.chapter_levels(txt))
        lines = txt.splitlines()
        out = {}
        for k, (ln, num, head) in enumerate(hits):
            end = hits[k + 1][0] if k + 1 < len(hits) else len(lines)
            body = '\n'.join(lines[ln + 1:end])
            out[num] = {'title': '', 'words': broken.bmp.wc(body), 'mermaid': 0,
                        'body': body, 'line': ln + 1}
        return {'chapters': out, 'depth': depth, 'warn': warn, 'dups': []}
    broken.bmp.parse_chapters = no_stop
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, 'tkdm-map.html')
        broken.build(book_dir, out)   # chi doc book_dir, ghi ra tmp — khong dong vao kho
        rows, code = broken.verify(out, book_dir)
        r = _rows(rows)
        check('DOI CHUNG AM EOF (sach that tu-khong-den-mot): cong thoat khac 0',
              code != 0, code)
        check('DOI CHUNG AM EOF (sach that): hang CAU TRUC moi bao CHAN',
              r['tieu de lac trong than chuong'][3] == 'CHAN',
              r['tieu de lac trong than chuong'])
        bloat_ratio = float(r['chuong cuoi / trung vi'][1].rstrip('x'))
        check('DOI CHUNG AM EOF (sach that): minh hoa vi sao can hang CAU '
              'TRUC — bloat ratio KHONG vuot 1.8x tren CHINH loi nay '
              '(do that ~1.49x)', bloat_ratio < 1.8,
              r['chuong cuoi / trung vi'])


# --- Review Focus 4: dau vao thieu / rong / 0 chuong
def run_cli(*args):
    return subprocess.run([sys.executable, SCRIPT] + list(args),
                          capture_output=True, text=True, encoding='utf-8')

def test_bad_input():
    with tempfile.TemporaryDirectory() as tmp:
        r1 = run_cli(os.path.join(tmp, 'khong-co-that'))
        check('thu muc thieu: thoat khac 0', r1.returncode != 0, r1.returncode)
        check('thu muc thieu: khong Traceback', 'Traceback' not in r1.stderr,
              r1.stderr[-300:])

        d2 = os.path.join(tmp, 'rong')
        os.makedirs(d2)
        io.open(os.path.join(d2, 'book.md'), 'w', encoding='utf-8').write('   \n')
        r2 = run_cli(d2)
        check('book.md rong: thoat khac 0', r2.returncode != 0, r2.returncode)
        check('book.md rong: khong Traceback', 'Traceback' not in r2.stderr,
              r2.stderr[-300:])

        d3 = os.path.join(tmp, 'khong-chuong')
        os.makedirs(d3)
        io.open(os.path.join(d3, 'book.md'), 'w', encoding='utf-8').write(
            '# Lời mở\n\nkhong co chuong nao ca\n')
        r3 = run_cli(d3)
        check('0 chuong: thoat khac 0', r3.returncode != 0, r3.returncode)
        check('0 chuong: KHONG sinh trang rong',
              not os.path.exists(os.path.join(d3, 'khong-chuong-map.html')),
              'da sinh trang rong')
        check('0 chuong: khong Traceback', 'Traceback' not in r3.stderr,
              r3.stderr[-300:])


if __name__ == '__main__':
    test_escape(); test_render_and_gates(); test_hide_empty_sections()
    test_arc_svg_renders()
    test_crlf_render(); test_vietnamese_path()
    test_verify_passes_clean(); test_negative_cdn()
    test_negative_scope_label(); test_negative_eof_real()
    test_bad_input()
    print()
    if FAILED:
        print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
        sys.exit(1)
    print('Tat ca PASS')
