# -*- coding: utf-8 -*-
"""Kiem hai script cong cua /book-to-book bang DOT BIEN HAI CHIEU.

Vi sao viet kieu nay
--------------------
Cong do chinh tac gia dung len ma tu kiem thi no tan cong dung cho tac gia dang
phong. Phep thu o day luon di theo CAP: mot mau THAT phai do, mot mau BIA phai
truot. Bon nhanh trich dan (that / bia / luoc that / nua that nua bia) tung bat
duoc bug ghep nham hai trich dan lien nhau.

Va mot lop kiem rieng cho dang hong NGUY HIEM NHAT: cong tra ket qua RONG ma doc
y het "sach" (thieu kho ngu lieu, khong thay ban thao, sai bo loc ten tep).
Nhung ca do phai ra ma thoat 2, khong bao gio 0.

Chay:  python scripts/test_book_to_book.py
"""
import importlib.util
import io
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, '..', 'skills', 'book', 'book-to-book', 'scripts')
SKILL = os.path.abspath(SKILL)
sys.path.insert(0, SKILL)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILL, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


si = _load('source_ingest')
fa = _load('fidelity_audit')
ql = _load('quote_locate')
so = _load('self_overlap')
fs = _load('frontmatter_sync')

NL = chr(10)
FAILED = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  -> ' + detail) if detail and not cond else ''))
    if not cond:
        FAILED.append(name)


# --------------------------------------------------------------- du lieu mau

SOURCE_TEXT = """Engineering Design Methods 5e

12 Objectives Tree

The designer is often tempted to go on collecting information instead of making
proposals. It is perfectly legitimate to conceive a preliminary solution and then
abstract this by developing and completing the function structure by a process of
iteration. A method is a lifebelt and not a straitjacket, and the designer should
feel free to move between problem and solution as understanding grows.

13 Function Analysis

The problem and the solution co-evolve, which means that the most expensive
failure in design is not choosing the wrong option but going to collect more
information instead of proposing something concrete and testable today.

14 Morphological Charts

A morphological chart sets out the range of means by which each subfunction may
be achieved, and the designer combines one means from each row into a candidate
overall solution. The chart is a generator of variety, not a decision procedure,
and the number of theoretical combinations grows far faster than the number of
combinations worth drawing. Practical work therefore prunes the chart early,
using compatibility between neighbouring means as the first filter.

15 Value Engineering

Value engineering asks what each component contributes relative to what it costs,
and it treats cost as a design variable rather than an outcome reported after the
fact. The weakness of the technique in practice is that teams apply it late, when
the architecture is already frozen and only trimming remains available to them.
"""

SCOPE_OK = """---
type: scope-decision
---

# Quyet dinh pham vi — sach phai sinh

muc nguyen ban: {level}
pham vi phat hanh: NOI BO — CEO tham khao va hoc tap, khong phat hanh ra ngoai
khoa phat tan: may CEO + vault, KHONG TAI LEN dich vu ngoai
CEO ky ngay: 2026-09-14

## Vi sao muc nay

Fixture test. Day la ban khai bao dung de kiem cong, khong phai quyet dinh that.
Van ban duoc noi dai de vuot san MIN_BYTES cua cong — cong coi tep duoi 400 byte
la "tao cho co" va tu choi doc, dung nhu cach databus_check.py xu ly hien vat rong.

## He qua da chap nhan

- Sach nay khong roi may CEO va vault.
- Moi tep giao ra mang dau BAN NOI BO.
- Muon doi pham vi thi phai chay lai cong o tran khac, khong sua tay con so.
"""


def lam_kho(root, text=SOURCE_TEXT, label='Nguon'):
    src = os.path.join(root, 'source.txt')
    io.open(src, 'w', encoding='utf-8', newline='\n').write(text)
    rc = si.main([src, '-o', root, '--label', label])
    return rc


def lam_khai_bao(root, level='F2'):
    io.open(os.path.join(root, '_scope_decision.md'), 'w',
            encoding='utf-8', newline='\n').write(SCOPE_OK.format(level=level))


def lam_chuong(root, ten, than, dau=True):
    d = os.path.join(root, 'Phase6-Revised')
    os.makedirs(d, exist_ok=True)
    head = '# %s\n\n> BẢN NỘI BỘ — CEO tham khảo, không phát hành\n\n' % ten if dau \
        else '# %s\n\n' % ten
    # don cho du MIN_BYTES=400 de khong bi cong coi la "tep rong"
    chen = '\n\nDien giai cua nguoi viet, khong phai loi nguon. ' * 12
    io.open(os.path.join(d, ten + '.md'), 'w', encoding='utf-8',
            newline='\n').write(head + than + chen)


def chay(root, level='F2', **kw):
    args = [root, '--level', level]
    for k, v in kw.items():
        args += ['--' + k.replace('_', '-'), str(v)]
    return fa.main(args)


# ------------------------------------------------------------------ kiem tra

def t_chuan_hoa():
    """Bon nguon am tinh gia — sua het moi doc duoc ket qua."""
    check('norm: ngat tu qua dong (de-\\nsign -> design)',
          'design' in si.norm('de-\nsign of things'))
    check('norm: ligature fi/fl',
          si.norm('ﬁrst ﬂow') == 'first flow', si.norm('ﬁrst ﬂow'))
    check('norm: nhay cong + gach ngang unicode',
          si.norm('“a—b”') == 'a b', si.norm('“a—b”'))
    check('norm: GIU tieng Viet co dau (regex [^a-z0-9] cu se nghien nat)',
          si.norm('Thiết kế đồng tiến hoá') == 'thiết kế đồng tiến hoá',
          si.norm('Thiết kế đồng tiến hoá'))


def t_ingest():
    root = tempfile.mkdtemp(prefix='b2b-ingest-')
    try:
        rc = lam_kho(root)
        check('ingest: ma thoat 0', rc == 0, 'rc=%s' % rc)
        import json
        meta = json.loads(io.open(os.path.join(root, '_source', 'Nguon.meta.json'),
                                  encoding='utf-8').read())
        check('ingest: dem duoc tu goc (mau so cua moi ty le)', meta['words'] > 80,
              str(meta.get('words')))
        check('ingest: co sha256 de doi chieu ve sau', len(meta.get('sha256', '')) == 64)
        check('ingest: ghi du 3 tep', all(os.path.isfile(os.path.join(root, '_source', f))
              for f in ('Nguon.corpus.txt', 'Nguon.pagemap.json', 'Nguon.meta.json')))
        # nguon SCAN (rong text) phai dung han, khong duoc coi la kho hop le
        rc2 = lam_kho(root, text='abc', label='Scan')
        check('ingest: nguon rong/scan -> ma thoat 2, khong im lang', rc2 == 2, 'rc=%s' % rc2)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_bon_nhanh_trich_dan():
    """That / bia / luoc that / nua that nua bia — phai phan biet duoc ca bon."""
    root = tempfile.mkdtemp(prefix='b2b-quote-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F3')
        that = 'A method is a lifebelt and not a straitjacket'
        bia = 'A method is a cage that every good designer must break out of'
        luoc = 'The designer is often tempted ... instead of making proposals'
        nua = 'The problem and the solution co-evolve ... which no author ever wrote here'
        lam_chuong(root, 'Ch01', 'Nguoi viet dan: "%s".' % that)
        lam_chuong(root, 'Ch02', 'Nguoi viet dan: "%s".' % bia)
        lam_chuong(root, 'Ch03', 'Nguoi viet dan: "%s".' % luoc)
        lam_chuong(root, 'Ch04', 'Nguoi viet dan: "%s".' % nua)
        rc = chay(root, 'F3')
        rep = io.open(os.path.join(root, 'Phase7-Fidelity-Report.md'), encoding='utf-8').read()
        check('trich BIA -> truot (ma thoat 1)', rc == 1, 'rc=%s' % rc)
        check('trich THAT -> khong bi bao la bia', 'Ch01' not in rep.split('## 🔴 Trích')[1][:400]
              if '## 🔴 Trích' in rep else False)
        check('trich LUOC that -> khong bi bao la bia',
              'Ch03' not in rep.split('## 🔴 Trích')[1][:400] if '## 🔴 Trích' in rep else False)
        check('trich NUA THAT NUA BIA -> bi bat', 'NỬA BỊA' in rep or 'Ch04' in rep)
        check('bao cao duoc ghi ra tep (hien vat cho Data Bus)', len(rep) > 500)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_nguyen_van_ngoai_ngoac():
    """Vung mu cua cong trich dan cu: chep dung chu ma KHONG dong ngoac."""
    root = tempfile.mkdtemp(prefix='b2b-unquoted-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F1')
        chep = ('It is perfectly legitimate to conceive a preliminary solution and then '
                'abstract this by developing and completing the function structure by a '
                'process of iteration.')
        lam_chuong(root, 'Ch01', chep)
        rc = chay(root, 'F1')
        rep = io.open(os.path.join(root, 'Phase7-Fidelity-Report.md'), encoding='utf-8').read()
        check('chep khong ngoac -> bi bat', 'NGOÀI ngoặc' in rep)
        check('chep khong ngoac -> vuot tran F1 (ma thoat 1)', rc == 1, 'rc=%s' % rc)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_tran_theo_muc():
    """Cung mot ban thao: F1 truot, F3 do. Tran phai thuc su rang buoc."""
    root = tempfile.mkdtemp(prefix='b2b-level-')
    try:
        lam_kho(root)
        chep = ('It is perfectly legitimate to conceive a preliminary solution and then '
                'abstract this by developing and completing the function structure.')
        lam_chuong(root, 'Ch01', 'Nguoi viet dan: "%s"' % chep)
        lam_khai_bao(root, 'F1')
        rc1 = chay(root, 'F1')
        lam_khai_bao(root, 'F3')
        rc3 = chay(root, 'F3')
        check('cung ban thao: F1 truot', rc1 == 1, 'rc=%s' % rc1)
        check('cung ban thao: F3 do', rc3 == 0, 'rc=%s' % rc3)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_f4_mu():
    """F4 khong duoc bao 'sach' bang mot con so thap — phai tuyen la MU."""
    root = tempfile.mkdtemp(prefix='b2b-f4-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F4')
        lam_chuong(root, 'Ch01', 'Ban dich tieng Viet cua toan bo chuong, khong khop chuoi '
                                 'voi ban goc tieng Anh nen cam bien khong thay gi.')
        rc = chay(root, 'F4')
        rep = io.open(os.path.join(root, 'Phase7-Fidelity-Report.md'), encoding='utf-8').read()
        check('F4: khong truot vi mat do', rc == 0, 'rc=%s' % rc)
        check('F4: bao cao tuyen ro la MU, khong phai sach', 'KHÔNG CÓ NGHĨA' in rep and 'MÙ' in rep)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_cac_dang_hong_im_lang():
    """Moi ca duoi day tung (hoac de) doc y het 'sach'. Tat ca phai ra ma thoat 2."""
    # 1. thieu khai bao P0
    root = tempfile.mkdtemp(prefix='b2b-noscope-')
    try:
        lam_kho(root)
        lam_chuong(root, 'Ch01', 'noi dung')
        check('thieu _scope_decision.md -> ma thoat 2', chay(root, 'F2') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 2. khai F3 nhung chay audit o F2
    root = tempfile.mkdtemp(prefix='b2b-mismatch-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F3')
        lam_chuong(root, 'Ch01', 'noi dung')
        check('khai F3 ma audit F2 -> ma thoat 2 (khong am tham chay theo co)',
              chay(root, 'F2') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 3. thieu kho ngu lieu goc
    root = tempfile.mkdtemp(prefix='b2b-nocorpus-')
    try:
        lam_khai_bao(root, 'F2')
        lam_chuong(root, 'Ch01', 'noi dung')
        check('thieu kho goc -> ma thoat 2, KHONG bao 0%', chay(root, 'F2') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 4. khong thay ban thao nao (loi bo loc ten tep da tung xay ra)
    root = tempfile.mkdtemp(prefix='b2b-nodraft-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F2')
        check('khong thay ban thao -> ma thoat 2, khong phai "0 vi pham"',
              chay(root, 'F2') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 5. khai bao khong co pham vi NOI BO
    root = tempfile.mkdtemp(prefix='b2b-noscope2-')
    try:
        lam_kho(root)
        io.open(os.path.join(root, '_scope_decision.md'), 'w', encoding='utf-8').write(
            'muc nguyen ban: F2\nCEO ky ngay: 2026-09-14\n' + 'x' * 400)
        lam_chuong(root, 'Ch01', 'noi dung')
        check('khai bao thieu "pham vi phat hanh: NOI BO" -> ma thoat 2',
              chay(root, 'F2') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # 6. F3/F4 thieu dong khoa phat tan
    root = tempfile.mkdtemp(prefix='b2b-nolock-')
    try:
        lam_kho(root)
        io.open(os.path.join(root, '_scope_decision.md'), 'w', encoding='utf-8').write(
            'muc nguyen ban: F4\npham vi phat hanh: NOI BO\nCEO ky ngay: 2026-09-14\n' + 'x' * 400)
        lam_chuong(root, 'Ch01', 'noi dung')
        check('F4 thieu dong khoa phat tan -> ma thoat 2', chay(root, 'F4') == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_dau_noi_bo():
    root = tempfile.mkdtemp(prefix='b2b-stamp-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F2')
        lam_chuong(root, 'Ch01', 'Noi dung tu viet, khong trich gi.', dau=False)
        rc = chay(root, 'F2')
        rep = io.open(os.path.join(root, 'Phase7-Fidelity-Report.md'), encoding='utf-8').read()
        check('thieu dau BAN NOI BO -> truot', rc == 1, 'rc=%s' % rc)
        check('bao cao neu dich danh tep thieu dau', 'Ch01' in rep)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_bao_cao_cu():
    """Dang hong hay gap nhat: do xong roi SUA TIEP, bao cao cu van nam do voi dau do."""
    root = tempfile.mkdtemp(prefix='b2b-stale-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F2')
        lam_chuong(root, 'Ch01', 'Noi dung tu viet.')
        check('audit chay xong', chay(root, 'F2') == 0)
        check('--verify ngay sau khi do -> 0',
              fa.main([root, '--level', 'F2', '--verify']) == 0)
        lam_chuong(root, 'Ch01', 'Noi dung tu viet, da sua them mot doan moi.')
        check('sua chuong sau khi do -> --verify truot',
              fa.main([root, '--level', 'F2', '--verify']) == 1)
        chay(root, 'F2')
        lam_chuong(root, 'Ch02', 'Chuong moi them vao sau khi do.')
        check('them chuong moi sau khi do -> --verify truot',
              fa.main([root, '--level', 'F2', '--verify']) == 1)
        check('--verify khi chua do lan nao -> ma thoat 2',
              fa.main([tempfile.mkdtemp(prefix='b2b-none-'), '--level', 'F2', '--verify']) == 2)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_cau_quy_ket_tran():
    root = tempfile.mkdtemp(prefix='b2b-claim-')
    try:
        lam_kho(root)
        lam_khai_bao(root, 'F2')
        lam_chuong(root, 'Ch01', 'Cross cho rằng thang 6-3-1 la bat buoc voi moi nhom.')
        chay(root, 'F2', nguon='Cross')
        rep = io.open(os.path.join(root, 'Phase7-Fidelity-Report.md'), encoding='utf-8').read()
        check('cau quy ket khong neo -> bi liet ke', 'Cross cho rằng' in rep)
        check('bao cao luon co muc vung mu', 'KHÔNG NHÌN THẤY GÌ' in rep)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_khoi_sau_sach():
    """Chuong cuoi KHONG duoc nuot phu luc.

    Lop loi that (performance-by-design-v2, 2026-09-23): bang bao Chuong 17 =
    19.930 tu trong khi chuong ay co 4.963 — phan con lai la ba phu luc. Sai theo
    huong AN TOAN GIA: mau so phinh ra nen mat do chuong cuoi trong thap hon that.

    Cap dot bien:
      THAT phai do  — phu luc SAU chuong cuoi thanh hang rieng, tong tu khong doi
      BIA phai truot — chu "Phu luc" nhac GIUA than sach khong duoc cat chuong
    """
    than = '\n\nNoi dung than chuong. ' * 40
    phu = '\n\nBang tra va ky hieu. ' * 40
    sach = ('# Chương 01 — Mo dau\n> BẢN NỘI BỘ\n' + than +
            '\n# Chương 02 — Chuong cuoi\n> BẢN NỘI BỘ\n' + than +
            '\n# Phụ lục\n\n' +                     # dong phan cach, khong co dau
            '\n# Phụ lục A — Ky hieu\n> BẢN NỘI BỘ\n' + phu)
    kh = fa.tach_chuong(sach, 'book.md')
    ten = [n for n, _, _ in kh]
    ch02 = [d for n, d, _ in kh if n.startswith('Chương 02')][0]

    check('phu luc thanh hang rieng', any('sau sách' in n for n in ten), repr(ten))
    check('chuong cuoi khong nuot phu luc', 'Bang tra' not in ch02)
    check('dong phan cach khong thanh khoi rieng',
          sum(1 for n in ten if 'Phụ lục' in n) == 1, repr(ten))
    # Bat bien dat nhat: khong duoc ROI chu nao, vi moi ty le deu chia cho tong nay.
    tong = sum(len(fa.norm(d).split()) for _, d, _ in kh)
    check('tong tu bao toan sau khi tach',
          tong == len(fa.norm(sach[sach.index('# Chương 01'):]).split()), str(tong))
    # Moi khoi tra ve deu phai du dai de cong "thieu dau" khong bao dong gia.
    check('khong khoi nao ngan hon nguong phan cach',
          all(len(fa.norm(d).split()) >= fa.TU_TOI_THIEU_KHOI for _, d, _ in kh))

    # --- doi chung am: "Phu luc" giua than sach KHONG duoc cat chuong ---
    giua = ('# Chương 01 — Mo dau\n> BẢN NỘI BỘ\n' + than +
            '\n## Phụ lục cua chuong nay\n' + than +
            '\n# Chương 02 — Chuong cuoi\n> BẢN NỘI BỘ\n' + than)
    kh2 = fa.tach_chuong(giua, 'book.md')
    check('"Phu luc" giua than sach khong cat chuong',
          len(kh2) == 2 and not any('sau sách' in n for n, _, _ in kh2),
          repr([n for n, _, _ in kh2]))


def t_snap_pagemap():
    """Moc trang phai duoc dich ve dung cho so trang xuat hien trong kho.

    Lop loi that (Pahl & Beitz, 2026-09-26): chi 56/617 moc roi dung vao so trang cua
    no; lech trung vi -18 ky tu. Mot trich nam gan ranh gioi bi gan LUI MOT TRANG, im
    lang. Ca that: trich la gach dau dong DAU TIEN cua tr.250 nhung cong cu tra tr.249.

    Cap dot bien:
      THAT phai do  — moc lech duoc keo ve, trich dau trang tra dung so trang
      BIA phai truot — moc dung roi thi khong duoc dich; don dieu phai duoc giu
    """
    # Trang 10 bat dau o offset 40; trang 11 bat dau o offset 80 trong van ban nay.
    text = ('10 mo dau trang muoi ' + 'x ' * 9 +
            '11 dau trang muoi mot ' + 'y ' * 9)
    off10 = text.index('10 ')
    off11 = text.index('11 ')

    # pagemap LECH: moc trang 11 bi ghi muon 12 ky tu (roi vao giua 'y y y...')
    pm_lech = [(off10, 10), (off11 + 12, 11)]
    snap = ql.snap_pagemap(text, pm_lech)
    check('moc lech duoc keo ve dung so trang', snap[1][0] == off11,
          'ky vong %d, nhan %d' % (off11, snap[1][0]))

    # pagemap DUNG: khong duoc dich di dau
    pm_dung = [(off10, 10), (off11, 11)]
    check('moc dung khong bi dich', ql.snap_pagemap(text, pm_dung) == pm_dung)

    # doi chung am: so trang KHONG co trong van ban -> giu nguyen moc, khong doan
    pm_vang = [(off10, 10), (off11, 99)]
    check('so trang khong xuat hien -> giu nguyen moc',
          ql.snap_pagemap(text, pm_vang)[1][0] == off11)

    # don dieu: neu keo ve se lam moc lui qua moc truoc thi PHAI bo qua
    pm_nguoc = [(off11, 11), (off11 + 4, 10)]
    ra = ql.snap_pagemap(text, pm_nguoc)
    check('giu tinh don dieu, tha khong dich con hon dich sai',
          ra[1][0] >= ra[0][0], repr(ra))


def t_lop_chu_tach_tu():
    """Lop chu PDF tach MOT tu thanh hai -> cong bao HONG cho cau CO IN TRONG SACH.

    Lop loi that (usv-thiet-ke-he-thong, 2026-09-30): trich 'Avoid electrolytes
    altogether.' co in o tr.333 Pahl & Beitz, nhung lop chu PDF luu 'electroly tes'
    nen phep so chuoi truot. Day la AM TINH GIA, va hau qua khong phai mot dong bao
    loi — nguoi viet tuong minh chep sai, bo ngoac kep, va mot trich dan THAT bien
    mat im lang.

    Khac gach-noi-ngat-dong (norm() da xu): o day khong co gach noi nao de bam.

    Do tren hai kho cuon USV: 23 ca / 264k tu — nho, nhung 9 ca nam tren 'deadrise',
    dung thuat ngu trung tam cua nguon, nen xac suat vap cao hon con so 23 goi ra.

    Cap dot bien:
      THAT phai do  — chu in dung, kho bi tach -> tim thay, co co tach_chu, DUNG trang
      BIA phai truot — bo khoang trang khong duoc bien mot cau bia thanh cau that
    """
    root = tempfile.mkdtemp(prefix='b2b-tachtu-')
    try:
        # kho co mot tu bi tach ('electroly tes') y nhu lop chu PDF that
        lam_kho(root, SOURCE_TEXT + '\n\nJoints must avoid electroly tes altogether '
                                    'in the region of dissimilar metals.\n')
        kho = ql.Kho(root)

        # THAT: nguoi viet go DUNG chinh ta -> luot chinh truot, luot phu phai cuu
        r = kho.tra('avoid electrolytes altogether in the region')
        check('chu in dung + kho bi tach -> van tim thay', r['ok'], repr(r))
        check('phai khai ro da dung luot phu (de con bat mo anh)',
              r.get('tach_chu') is True, repr(r))

        # doi chung am 1: bia han, du dai -> bo khoang trang khong duoc cuu
        r = kho.tra('avoid all galvanic couples altogether in every welded region')
        check('AM: cau bia -> van truot du da bo khoang trang', not r['ok'], repr(r))

        # doi chung am 2: that nhung SAI MOT CHU -> phai truot
        r = kho.tra('avoid electrolytes altogezher in the region')
        check('AM: sai mot chu -> truot', not r['ok'], repr(r))

        # doi chung am 3: ghep bua qua ranh gioi tu, duoi nguong -> truot
        r = kho.tra('electrolytesaltogether in')
        check('AM: ghep qua ranh gioi tu, duoi nguong -> truot', not r['ok'], repr(r))

        # KHONG HOI QUY: trich binh thuong phai do o luot CHINH, khong qua luot phu
        r = kho.tra('A method is a lifebelt and not a straitjacket')
        check('trich thuong van do o luot chinh', r['ok'] and not r.get('tach_chu'), repr(r))
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_trung_chinh_no():
    """Sach phai sinh trung CHINH NO — dai luong khong cong nao khac do duoc.

    Lop loi that (usv-thiet-ke-he-thong, 2026-09-30): 228 mach trung >=12 tu giua cac chuong,
    dai nhat 35 tu. Vi sao khong cong nao cu thay:
      - fidelity_audit dem chuoi trung voi NGUON, khong dem sach trung chinh no
      - kiem_ngan_sach_trich cong THEO CHUONG -> 3 chuong cung khai mot cau thi ca 3 "dat"
      - nguoi viet tung chuong khong the thay: moi agent chi doc chuong cua minh

    Cap dot bien:
      THAT phai do  — doan lap lai o hai chuong bi bat, do dai dung
      BIA phai truot — van ban khac nhau khong bi bao trung; khuon mau (>=N chuong) khong keu
    """
    root = tempfile.mkdtemp(prefix='b2b-trung-')
    try:
        d = os.path.join(root, 'ch')
        os.makedirs(d)
        lap = ('mot vi du co hai con so do duoc hinh 7 122 ve hai phuong an cung mot vo '
               'dong co dien han cung khuon kho ')
        khac = 'chuong nay noi ve mot chuyen hoan toan khac khong lap lai gi cua ai '
        nhan = 'than gia dinh tg 1 khong phai thong so san pham '   # khuon mau, 6 chuong
        for i in range(1, 7):
            than = nhan + khac * 3
            if i in (2, 5):
                than += lap                      # dung 2 chuong lap doan nay
            io.open(os.path.join(d, 'Ch%02d.md' % i), 'w',
                    encoding='utf-8', newline='\n').write('# Ch%02d\n\n' % i + than)

        rc = so.main([d, '--n', '12', '--khuon', '5'])
        check('trung o hai chuong -> ma thoat 1', rc == 1, 'rc=%s' % rc)

        # do truc tiep qua ham de kiem do dai + phan loai
        kho = {}
        for i in (2, 5):
            t = io.open(os.path.join(d, 'Ch%02d.md' % i), encoding='utf-8').read()
            kho[i] = [w for w, _ in so.tach_tu(so.go_khoi(t))]
        check('go_khoi bo frontmatter va khoi ```',
              'bi bo' not in so.go_khoi('---\na: 1\n---\nthan\n```\nbi bo\n```\n'))
        check('gop_mach gop cua so chong nhau thanh MOT mach',
              so.gop_mach([(0, 5), (1, 6), (2, 7)]) == [[0, 2, 5, 7]],
              repr(so.gop_mach([(0, 5), (1, 6), (2, 7)])))
        check('gop_mach KHONG gop hai cho roi nhau',
              len(so.gop_mach([(0, 5), (9, 40)])) == 2)
        check('phan loai tieng Viet vs tieng Anh',
              so.la_tieng_viet('thong so san pham') is False
              and so.la_tieng_viet('thân giả định') is True)

        # doi chung am 1: khong chuong nao lap -> ma thoat 0
        # 🔴 Khuon dau cua phep thu nay SAI: no lap cung mot cau 3 lan TRONG mot chuong,
        # va cong bat dung (tu lap trong chuong la mot ca that — Ch.22 trich lai chinh no).
        # Giu ghi chu nay: doi chung am phai SACH theo DUNG dai luong cam bien do.
        root2 = tempfile.mkdtemp(prefix='b2b-trung0-')
        d2 = os.path.join(root2, 'ch')
        os.makedirs(d2)
        for i in range(1, 7):
            # moi chuong mot van ban RIENG, va KHONG lap lai gi trong chinh no
            rieng = ' '.join('ch%dtu%d' % (i, j) for j in range(40))
            io.open(os.path.join(d2, 'Ch%02d.md' % i), 'w', encoding='utf-8',
                    newline='\n').write('# Ch%02d\n\n' % i + nhan + rieng)
        rc2 = so.main([d2, '--n', '12', '--khuon', '5'])
        check('AM: khong chuong nao lap -> ma thoat 0', rc2 == 0, 'rc=%s' % rc2)
        shutil.rmtree(root2, ignore_errors=True)

        # doi chung am 2: khong thay chuong -> ma thoat 2, KHONG phai 0
        root3 = tempfile.mkdtemp(prefix='b2b-trung2-')
        rc3 = so.main([root3, '--n', '12'])
        check('AM: khong thay chuong -> ma thoat 2 (khong doc nhu "sach")', rc3 == 2, 'rc=%s' % rc3)
        shutil.rmtree(root3, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def t_frontmatter_sinh_tu_than():
    """Ba truong trich dan phai SINH tu than chuong, khong phai agent viet tay.

    Lop loi that (usv-thiet-ke-he-thong, 2026-09-30): ba truong quote_budget / quote_used /
    quotes_ok TRONG NHU do cong cu sinh — nguoi dieu phoi con noi voi ba agent rang chung do cong
    cu sinh, nen ca ba tu choi sua khi thay sai. Kiem lai: KHONG script nao nhac toi chung.
    Hau qua do duoc: Ch.22 khai "P&B 233/240 — dat"; do tu THAN ra "246/240 — VUOT". Loi khai che
    dung mot cho vuot ngan sach, va con lam HAI vong ra soat doc lap tin Ch.22 thuan P&B.

    Cap dot bien:
      THAT phai do  — trich *"..."* trong than duoc dem, dung nguon, dung tong tu
      BIA phai truot — chuoi tieng Viet trong ngoac nhon KHONG tinh la trich nguon; khoi ``` bi
                       loai; thieu dan y ra ma thoat 2, khong bao gio 0
    """
    root = tempfile.mkdtemp(prefix='b2b-fm-')
    try:
        lam_kho(root)
        d = os.path.join(root, 'Phase6-Revised')
        os.makedirs(d)
        dany = '### Ch.01 - thu@**Từ** 5.000 - **Trích** Nguon 40@'.replace('@', NL)
        io.open(os.path.join(root, 'Phase3-Outline.md'), 'w',
                encoding='utf-8', newline=NL).write(dany)
        that = 'A method is a lifebelt and not a straitjacket'   # 9 tu, co that trong kho mau
        than = (
            '---@chapter: 1@quote_budget: SAI@quote_used: SAI@quotes_ok: 99/99@---@'
            '# Ch01@@'
            'Nguoi viet dan: *"' + that + '"*.@'
            'Mot thuat ngu tieng Viet: «than gia dinh TG-1 khong phai thong so».@'
            '```@trong khoi ma: *"' + that + '"*@```@').replace('@', NL)
        io.open(os.path.join(d, 'Ch01.md'), 'w', encoding='utf-8', newline=NL).write(than)

        rc = fs.main([root, '--chuong', 'Phase6-Revised', '--ghi'])
        ra = io.open(os.path.join(d, 'Ch01.md'), encoding='utf-8').read()
        check('doc ngan sach tu DAN Y, khong chep tay', 'quote_budget: Nguon 40' in ra, ra[:160])
        check('dem trich *"..."* trong than, dung so tu', 'quote_used: Nguon 9' in ra, ra[:160])
        check('chuoi tieng Viet KHONG tinh la trich nguon', 'quotes_ok: 1/1' in ra, ra[:160])
        check('khoi ``` bi loai — khong dem hai lan', 'Nguon 18' not in ra)
        check('trong ngan sach -> ma thoat 0', rc == 0, 'rc=%s' % rc)

        io.open(os.path.join(root, 'Phase3-Outline.md'), 'w', encoding='utf-8',
                newline=NL).write(dany.replace('Nguon 40', 'Nguon 5'))
        check('AM: vuot ngan sach -> ma thoat 1',
              fs.main([root, '--chuong', 'Phase6-Revised']) == 1)

        root2 = tempfile.mkdtemp(prefix='b2b-fm2-')
        check('AM: thieu dan y -> ma thoat 2 (khong doc nhu "sach")', fs.main([root2]) == 2)
        shutil.rmtree(root2, ignore_errors=True)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    print('=' * 70)
    print('KIEM CONG /book-to-book — dot bien hai chieu')
    print('=' * 70)
    for f in (t_chuan_hoa, t_ingest, t_bon_nhanh_trich_dan, t_nguyen_van_ngoai_ngoac,
              t_tran_theo_muc, t_f4_mu, t_cac_dang_hong_im_lang, t_dau_noi_bo,
              t_bao_cao_cu, t_cau_quy_ket_tran, t_khoi_sau_sach, t_snap_pagemap,
              t_lop_chu_tach_tu, t_trung_chinh_no,
              t_frontmatter_sinh_tu_than):
        print('\n-- %s' % f.__name__)
        f()
    print('\n' + '=' * 70)
    if FAILED:
        print('THAT BAI %d: %s' % (len(FAILED), ' | '.join(FAILED)))
        return 1
    print('TAT CA DEU DO')
    return 0


if __name__ == '__main__':
    sys.exit(main())
