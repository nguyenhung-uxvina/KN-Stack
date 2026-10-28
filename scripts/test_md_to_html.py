"""Test cho md_to_html.py — ket xuat ban do sach bac A.

Bon ca bien do that tren 32 cuon (2026-10-03; CRLF do lai 2026-10-05 tren
34 cuon — xem F2):
  - 5/32 cuon co <>&" trong TEN CHUONG (tau-nhom-han-quoc-phong Ch.01 la
    `"Nhom chi la thep nhe hon."`) -> khong escape thi trang vo.
  - 3/34 cuon dung CRLF (do lai 2026-10-05; so cu "4/32" da bi RUT LAI).
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
import re
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
                  'tieu de lac trong than chuong', 'neo tom tat sai',
                  'tom tat vi pham STE'):
            check('verify: co phep do %r' % k, k in r, sorted(r))
        check('verify: khong co dong CHAN',
              not [x for x in rows if x[3] == 'CHAN'],
              [x for x in rows if x[3] == 'CHAN'])
        check('verify: khong co tep digest thi "neo tom tat sai" = ok',
              r['neo tom tat sai'][3] == 'ok', r['neo tom tat sai'])
        check('verify: khong co tep digest thi "tom tat vi pham STE" = ok',
              r['tom tat vi pham STE'][3] == 'ok', r['tom tat vi pham STE'])


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


# --- Fix round 3 (2026-10-06), F3: 4/10 hang chua co doi chung am la mot
# hang khong ai tung thay no bao do — mot stub tra ve 0 se qua duoc ca bon.
# Moi doi chung tao bang cach TAM hoac fixture, KHONG de loi trong ma SX.

# --- the script
def test_negative_script_tag():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        io.open(out, 'w', encoding='utf-8').write(
            h.replace('</body>', '<script>alert(1)</script></body>'))
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('DOI CHUNG AM the script: cong thoat khac 0', code != 0, code)
        check('DOI CHUNG AM the script: hang "the script" bao CHAN',
              r['the script'][3] == 'CHAN', r['the script'])


# --- chu thich html
def test_negative_html_comment():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        io.open(out, 'w', encoding='utf-8').write(
            h.replace('</body>', '<!-- ghi chu noi bo --></body>'))
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('DOI CHUNG AM chu thich: cong thoat khac 0', code != 0, code)
        check('DOI CHUNG AM chu thich: hang "chu thich html" bao CHAN',
              r['chu thich html'][3] == 'CHAN', r['chu thich html'])


# --- so chuong trung: fixture co 2 chuong cung so
DUP_BOOK = '\n'.join(
    ['# Chương 05 — Bản thật'] + ['than'] * 60 +
    ['# Chương 05 — Bản trùng'] + ['than'] * 60 +
    ['# Chương 06 — Khác'] + ['than'] * 60)

def test_negative_duplicate_chapter_numbers():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, body=DUP_BOOK)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('DOI CHUNG AM trung so: hang "so chuong trung" bao canh-bao',
              r['so chuong trung'][3] == 'canh-bao', r['so chuong trung'])
        check('DOI CHUNG AM trung so: gia tri ghi dung so chuong trung (5)',
              r['so chuong trung'][1] == [5], r['so chuong trung'])


# --- Fix round 2 (2026-10-06): chuong TRUNG KHONG duoc "muon" muc IP cua
# ban song sinh. parse_chapters cho ban trung thu hai mot key THAP PHAN nam
# CHAT trong (num, num+1) — vd 5.001 — va `int(5.001) == 5`, nen mot phien
# ban cu (tra cuu bang `int(n) in ip`) se cho CA HAI the cung hien thi muc
# cua chuong 5, du sach chi tung xep muc cho MOT noi dung. Day la dung mot
# cua: "bia mot phan loai sach khong dua ra" — chinh cai spec 3.4 cam, chi
# la den qua cua khac (anh xa key, khong phai doan tu khoa). Anh xa that su
# MO HO khi trung so, nen cau tra loi trung thuc la "chua do" cho CA HAI
# ban, khong co cach "khon" nao chon dung mot ban de giu muc.
DUP_IP_BOOK = '\n'.join(
    ['# ⛔ Phạm vi lưu hành', '', '> BẢN NỘI BỘ', '',
     '## Xếp mức IP theo chương', '',
     '| Chương | Mức | Vì sao |',
     '|---|---|---|',
     '| 05 | 🔴 SENSITIVE | ly do that. |',
     '',
     '# Chương 05 — Bản thật'] + ['than'] * 40 +
    ['# Chương 05 — Bản trùng'] + ['than'] * 40)

def test_ip_badge_not_inherited_by_duplicate():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, body=DUP_IP_BOOK)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        cells = [re.sub(r'<[^>]+>', '', c) for c in
                 re.findall(r'<i(?: class="undone")?>mức IP: (.*?)</i>', h, re.S)]
        check('trung so + bang IP: dung 2 the mang muc IP',
              len(cells) == 2, cells)
        check('trung so + bang IP: dung MOT the giu muc that cua bang',
              cells.count('🔴 SENSITIVE') == 1, cells)
        check('trung so + bang IP: ban trung KHONG duoc "muon" muc — phai '
              'la chua do, khong duoc hien lai muc cua ban kia',
              cells.count('chưa đo') == 1, cells)

        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('trung so + bang IP: cong "so chuong trung" van bao canh-bao '
              '(hai tin hieu — the va cong — phai dong thuan)',
              r['so chuong trung'][3] == 'canh-bao', r['so chuong trung'])
        check('trung so + bang IP: cong ghi dung so chuong trung (5)',
              r['so chuong trung'][1] == [5], r['so chuong trung'])


# --- F1: so do the vs nguon phai do TU TRANG (h), khong phai tu book.md lai
# lan nua — tam CHINH so dem da IN RA TRANG (khong dong vao book.md) va kiem
# hang nay PHAI lech. Day la doi chung CHUNG MINH F1 that su da sua: no THAT
# BAI tren ma TRUOC fix round 3 (xem report) vi mer_page khi do tinh tu `ch`
# (nguon lai), khong tu `h` — tam trang khong lam no doi.
def test_negative_mermaid_page_tamper():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        before_rows, _ = mth.verify(out, d)
        before = _rows(before_rows)['so do the vs nguon']
        tampered = re.sub(r'\d+ sơ đồ', '0 sơ đồ', h)
        io.open(out, 'w', encoding='utf-8').write(tampered)
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('DOI CHUNG AM so do: truoc tam, hang khop (ok)',
              before[3] == 'ok', before)
        check('DOI CHUNG AM so do: cong van thoat 0 (canh-bao, khong CHAN)',
              code == 0, code)
        check('DOI CHUNG AM so do: sau khi xoa so dem TREN TRANG (book.md '
              'khong doi), hang "so do the vs nguon" PHAI bao canh-bao',
              r['so do the vs nguon'][3] == 'canh-bao',
              r['so do the vs nguon'])
        check('DOI CHUNG AM so do: gia tri phia trang phai tut ve 0',
              r['so do the vs nguon'][1].startswith('0 vs '),
              r['so do the vs nguon'])


# --- Fix round 4 (2026-10-06), F1: bullet dan y hien tren trang PHAI duoc
# danh dau RO la chua qua cong neo, VA phai bi lint STE nhu dong digest —
# truoc fix nay hai dieu nay deu KHONG xay ra (bullet hien giong digest het,
# "tom tat vi pham STE" chi do tep digest rieng nen luon bao sach tren
# 32/34 cuon khong co digest).
OUTLINE_LONG_BULLET = '\n'.join([
    '### Ch.01 — Tên chương',
    '- ' + ' '.join(['từ'] * 30) + '.',
])

def test_summary_from_outline_bullets_is_marked_and_linted():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, outline=OUTLINE_LONG_BULLET)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        check('F1: bullet dan y duoc danh dau class rieng summary-unanchored',
              'class="summary-unanchored"' in h, 'thieu class')
        check('F1: co nhan tieng Viet canh bao chua qua cong neo',
              'CHƯA qua cổng neo' in h, 'thieu nhan')
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('F1: "tom tat vi pham STE" bat dong bullet qua 25 tu, canh-bao',
              r['tom tat vi pham STE'][3] == 'canh-bao', r['tom tat vi pham STE'])
        check('F1: "neo tom tat sai" van ok — bullet khong mang so dong goc '
              'de neo, nen khong tinh vao hang nay',
              r['neo tom tat sai'][3] == 'ok', r['neo tom tat sai'])
        check('F1: cong KHONG CHAN — day la van phong, khong phai bia dat',
              code == 0, code)


# --- Fix round 4 (2026-10-06), nho #2: mot bullet dan y chua dung cum
# "N sơ đồ" (vd trich dan "3 sơ đồ minh họa cấu trúc") KHONG duoc lam phinh
# "so do the vs nguon" — hang nay chi duoc doc tu khoi .met, khong doc ca
# trang.
OUTLINE_FAKE_DIAGRAM_PHRASE = '\n'.join([
    '### Ch.01 — Tên chương',
    '- Chương vẽ đúng 3 sơ đồ minh họa cấu trúc biên hệ thống rõ ràng.',
])

def test_mermaid_count_not_inflated_by_bullet_text():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, outline=OUTLINE_FAKE_DIAGRAM_PHRASE)
        out = os.path.join(tmp, 'map.html')
        rep = mth.build(d, out)
        h = io.open(out, encoding='utf-8').read()
        check('nho #2: bullet co cum "3 sơ đồ" that su xuat hien tren trang',
              '3 sơ đồ' in h, 'khong thay cum trong bullet')
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('nho #2: "so do the vs nguon" KHONG bi phinh boi van ban bullet',
              r['so do the vs nguon'][1] == '%d vs %d'
              % (rep['mermaid_page'], rep['mermaid_src']),
              r['so do the vs nguon'])
        check('nho #2: hang van khop (ok) — cum trong bullet khong duoc dem',
              r['so do the vs nguon'][3] == 'ok', r['so do the vs nguon'])


# --- Fix round 4 (2026-10-06), nho #3: nhan pham vi phai nhan dien CA cac
# token don le MẬT/SENSITIVE/REVIEW/SAFE (cung bo token ma scope reader
# dung — bmp._TOKEN_RE), khong chi "NỘI BỘ"/"CHƯA KHAI" — truoc fix nay mot
# nhan dung dan nhu "MẬT." mot minh se bi hang nay CHAN NHAM du day la mot
# loi khai bao pham vi HOP LE.
MAT_ONLY_BOOK = '\n'.join(
    ['# ⛔ Phạm vi lưu hành', '', '**MẬT.**', '',
     '# Chương 01 — A'] + ['x'] * 40)

def test_scope_label_widened_tokens():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp, body=MAT_ONLY_BOOK)
        out = os.path.join(tmp, 'map.html')
        mth.build(d, out)
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('nho #3: nhan "MẬT" mot minh (khong co NỘI BỘ) van duoc nhan '
              'dien, KHONG bi CHAN nham', r['nhan pham vi'][3] == 'ok',
              r['nhan pham vi'])
        check('nho #3: cong khong CHAN tren mot trang da khai pham vi dung',
              code == 0, code)
    # Doi chung am: cong hien tai (truoc fix) VAN phai CHAN khi thuc su
    # thieu nhan — xem test_negative_scope_label o tren, van giu nguyen.


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


REPO = os.path.dirname(HERE)

# --- Task 10 (spec 1.2, spec 9 R-1): hai hang cong moi — "neo tom tat sai"
# PHAI CHAN (be mat bia dat duy nhat cua tinh nang), "tom tat vi pham STE"
# CHI canh bao (van phong lung cung khong phai bia dat). Hai thu nay KHONG
# duoc lam lan nhau: mot cau bia phai lam cong thoat != 0, mot cau vung ve
# thi khong.
def test_ste_lint_does_not_block():
    with tempfile.TemporaryDirectory() as tmp:
        d = mkbook(tmp)
        out = os.path.join(tmp, 'map.html')
        digest_path = os.path.join(d, '_book_map_digest.md')

        # Dong vi pham STE (qua 25 tu) nhung neo DUNG (L10 nam trong Ch.01,
        # xem BOOK: tieu de Ch.01 o dong 5, Ch.02 o dong 60).
        long_line = ' '.join(['từ'] * 30) + '.'
        io.open(digest_path, 'w', encoding='utf-8').write(
            '## Ch.01 L10\n' + long_line)
        # Fix round 4 (2026-10-06), F1: verify() lint dong tom tat tu CHINH
        # trang da dung (xem summary_lines_from_page), khong con doc
        # _book_map_digest.md rieng — nen phai build() LAI sau khi ghi
        # digest de trang mang noi dung moi truoc khi verify() doc no.
        mth.build(d, out)
        rows, code = mth.verify(out, d)
        r = _rows(rows)
        check('STE vi pham: hang "tom tat vi pham STE" bao canh-bao, KHONG CHAN',
              r['tom tat vi pham STE'][3] == 'canh-bao', r['tom tat vi pham STE'])
        check('STE vi pham: hang "neo tom tat sai" van ok (neo dung)',
              r['neo tom tat sai'][3] == 'ok', r['neo tom tat sai'])
        check('STE vi pham: cong KHONG CHAN vi day chi la van phong',
              code == 0, code)

        # Dong neo SAI (bia dat) — phai CHAN, du van ban STE sach.
        io.open(digest_path, 'w', encoding='utf-8').write(
            '## Ch.01 L999999\nCâu bịa không neo được vào book.md.')
        mth.build(d, out)
        rows2, code2 = mth.verify(out, d)
        r2 = _rows(rows2)
        check('neo sai: hang "neo tom tat sai" bao CHAN',
              r2['neo tom tat sai'][3] == 'CHAN', r2['neo tom tat sai'])
        check('neo sai: hang "tom tat vi pham STE" van ok (van ban sach)',
              r2['tom tat vi pham STE'][3] == 'ok', r2['tom tat vi pham STE'])
        check('neo sai: cong CHAN (thoat khac 0) vi day la bia dat',
              code2 != 0, code2)

        os.remove(digest_path)


def test_skill_wiring():
    sk = os.path.join(REPO, 'skills', 'ops', 'book-map', 'SKILL.md')
    check('skill: co tep SKILL.md', os.path.exists(sk), sk)
    if os.path.exists(sk):
        s = io.open(sk, encoding='utf-8').read()
        check('skill: frontmatter co name dung thu muc',
              'name: book-map' in s, s[:200])
        check('skill: description co "Triggers on:"', 'Triggers on:' in s, '')
        check('skill: tro dung script', 'md_to_html.py' in s, '')
        check('skill: noi ro rang buoc offline',
              'offline' in s.lower(), '')
    for f in ('codebase-to-book', 'notebook-to-book', 'book-to-book'):
        p = os.path.join(REPO, 'skills', 'book', f, 'SKILL.md')
        s = io.open(p, encoding='utf-8').read()
        check('%s: co pha P7.6' % f, 'P7.6' in s, '')
        check('%s: P7.6 khong chan pha sau' % f,
              'không chặn' in s.split('P7.6', 1)[-1][:2000], '')


if __name__ == '__main__':
    test_escape(); test_render_and_gates(); test_hide_empty_sections()
    test_arc_svg_renders()
    test_crlf_render(); test_vietnamese_path()
    test_verify_passes_clean(); test_negative_cdn()
    test_negative_scope_label(); test_negative_eof_real()
    test_negative_script_tag(); test_negative_html_comment()
    test_negative_duplicate_chapter_numbers()
    test_ip_badge_not_inherited_by_duplicate()
    test_negative_mermaid_page_tamper()
    test_ste_lint_does_not_block()
    test_summary_from_outline_bullets_is_marked_and_linted()
    test_mermaid_count_not_inflated_by_bullet_text()
    test_scope_label_widened_tokens()
    test_bad_input()
    test_skill_wiring()
    print()
    if FAILED:
        print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
        sys.exit(1)
    print('Tat ca PASS')
