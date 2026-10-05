"""Test cho book_map_parse.py — lop DO cua /book-map.

Ba lo hong THAT, do tren 32 cuon trong D:/Workshop_X/3_Resources/Books (2026-10-03):
  L1 Chuong cuoi chay den EOF -> hut phu luc. tu-khong-den-mot Ch.19 22.915 -> 15.565.
  L2 Luat dung co dinh theo muc heading -> principles-ba-tai-san tut con 326 tu/chuong.
  L3 `#` trong khoi ma doc thanh tieu de -> VO 5 CUON, pahl-beitz-tap2 mat 60% sach.
"""
import importlib.util
import io
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

bmp = load('bmp', 'book_map_parse.py')

FAILED = []

def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name +
          (('  -> ' + str(detail)) if detail and not cond else ''))
    if not cond:
        FAILED.append(name)


# --- BI-1: `#` trong khoi ma KHONG phai tieu de
FIX_FENCE = '\n'.join([
    '# Chương 01 — Thật',
    'noi dung',
    '```',
    '# 80% cong viec co phan hoi nhanh -> cung co niem tin',
    '# 20% con lai phan hoi sau nhieu thang',
    '```',
    'noi dung tiep',
    '~~~',
    '# Chương 99 — Trong khoi ngã',
    '~~~',
    '# Chương 02 — Thật nữa',
])

def test_mask():
    lines = FIX_FENCE.split('\n')
    mask = bmp.heading_mask(lines)
    check('mat na: dai bang so dong', len(mask) == len(lines), '%d/%d' % (len(mask), len(lines)))
    check('mat na: dong ngoai khoi la True', mask[0] is True, mask[0])
    check('mat na: dong trong khoi ``` la False', mask[3] is False, mask[3])
    check('mat na: dong trong khoi ~~~ la False', mask[8] is False, mask[8])

    lv = bmp.chapter_levels(FIX_FENCE)
    nums = sorted(h[1] for h in lv.get(1, []))
    check('BI-1: chi thay 2 chuong that, khong thay Ch.99', nums == [1, 2], nums)


# --- BI-2 chuan bi: chon muc NONG NHAT khi khop o hai muc
FIX_TWO_LEVELS = '\n'.join(
    ['# Chương 01 — A'] + ['than'] * 60 +
    ['# Chương 02 — B'] + ['than'] * 60 +
    ['# Phụ lục', '## Mục lục', '## Chương 01 — A', '## Chương 02 — B'])

def test_pick_level():
    lv = bmp.chapter_levels(FIX_TWO_LEVELS)
    check('thay chuong o CA HAI muc', set(lv) == {1, 2}, sorted(lv))
    depth, hits, warn = bmp.pick_level(lv)
    check('BI-2: chon muc nong nhat (H1)', depth == 1, depth)
    check('BI-2: lay dung 2 chuong than', len(hits) == 2, len(hits))
    check('BI-2: khong canh bao cho muc than', warn is None, warn)

    depth2, hits2, warn2 = bmp.pick_level({2: lv[2]})
    check('canh bao khi khoang cach giong MUC LUC',
          warn2 is not None and 'MUC LUC' in warn2.upper(), warn2)

    d3, h3, w3 = bmp.pick_level({})
    check('khong co tieu de: tra None + ly do', d3 is None and h3 is None and w3, w3)


# --- Review Focus 2: CRLF (4/32 cuon that)
def test_crlf():
    lv = bmp.chapter_levels(FIX_FENCE.replace('\n', '\r\n'))
    nums = sorted(h[1] for h in lv.get(1, []))
    check('CRLF: van chi thay 2 chuong that', nums == [1, 2], nums)
    check('CRLF: nguyen dong khong con \\r',
          all('\r' not in h[2] for h in lv.get(1, [])),
          [h[2] for h in lv.get(1, [])])


# --- dau phan cach: do that tren kho co ba dang "—" ":" "·", va so khong dem 0
def test_separators():
    for sep in ('—', ':', '·', '-'):
        txt = '# Chương 7 %s Tên gì đó' % sep
        lv = bmp.chapter_levels(txt)
        check('dau phan cach %r + so khong dem 0' % sep,
              lv.get(1) and lv[1][0][1] == 7, lv)
    lv = bmp.chapter_levels('# Chapter 03 — English title')
    check('nhan ca "Chapter"', lv.get(1) and lv[1][0][1] == 3, lv)


def test_wc():
    check('wc: dem tu tach bang khoang trang', bmp.wc('một hai  ba\nbốn') == 4,
          bmp.wc('một hai  ba\nbốn'))
    check('wc: rong = 0', bmp.wc('   \n ') == 0, bmp.wc('   \n '))


# --- BI-2: chuong KHONG duoc chay den het tep
FIX_BACKMATTER = '\n'.join(
    ['# Chương 01 — A'] + ['than mot'] * 100 +
    ['# Chương 02 — B'] + ['than hai'] * 100 +
    ['# Phụ lục'] + ['phu luc dai'] * 500)

# --- BI-2/L2: H2 dung cho CA chuong LAN tieu muc (principles-ba-tai-san)
FIX_H2_MIXED = '\n'.join(
    ['# Tên sách'] +
    ['## Chương 01: A'] + ['than'] * 40 + ['## Một tiểu mục'] + ['than'] * 40 +
    ['## Chương 02: B'] + ['than'] * 40 + ['## Tiểu mục nữa'] + ['than'] * 40)

def test_parse_chapters():
    p = bmp.parse_chapters(FIX_BACKMATTER)
    ch = p['chapters']
    check('cat chuong: dung 2 chuong', len(ch) == 2, sorted(ch))
    check('BI-2: chuong cuoi KHONG hut phu luc',
          ch[2]['words'] < 250, ch[2]['words'])
    check('cat chuong: lay dung ten', ch[1]['title'] == 'A', ch[1]['title'])

    p2 = bmp.parse_chapters(FIX_H2_MIXED)
    ch2 = p2['chapters']
    check('L2: muc H2 duoc chon', p2['depth'] == 2, p2['depth'])
    check('L2: dung 2 chuong, tieu muc KHONG thanh chuong', len(ch2) == 2, sorted(ch2))
    check('L2: tieu muc H2 KHONG cat dut chuong',
          ch2[1]['words'] > 70, ch2[1]['words'])


def test_mermaid_count():
    txt = '\n'.join(['# Chương 01 — A', '```mermaid', 'graph TD', 'A-->B', '```',
                     'chu', '```python', 'x = 1', '```',
                     '# Chương 02 — B', '```mermaid', 'graph LR', '```'])
    ch = bmp.parse_chapters(txt)['chapters']
    check('dem so do: Ch.01 co 1', ch[1]['mermaid'] == 1, ch[1]['mermaid'])
    check('dem so do: Ch.02 co 1', ch[2]['mermaid'] == 1, ch[2]['mermaid'])
    crlf = bmp.parse_chapters(txt.replace('\n', '\r\n'))['chapters']
    check('CRLF: dem so do khong doi', crlf[1]['mermaid'] == 1, crlf[1]['mermaid'])


# --- Review Focus 3: hai chuong cung so => ghi de IM LANG
def test_duplicate_numbers():
    txt = '\n'.join(['# Chương 05 — Bản thật'] + ['than'] * 60 +
                     ['# Chương 05 — Bản trùng'] + ['than'] * 60)
    p = bmp.parse_chapters(txt)
    check('trung so chuong: bao ra danh sach dups', p['dups'] == [5], p['dups'])
    check('trung so chuong: KHONG mat am tham — giu ca hai',
          len(p['chapters']) == 2, sorted(p['chapters']))


# --- BI-5: cam bien phai so voi mot TONG DOC LAP
def test_coverage():
    p = bmp.parse_chapters(FIX_BACKMATTER)
    cov = bmp.coverage(p, FIX_BACKMATTER)
    check('BI-5: phu < 1 khi sach co phu luc lon', cov < 0.5, cov)
    txt = '# Chương 01 — A\n' + 'một hai ba bốn năm'
    p2 = bmp.parse_chapters(txt)
    check('BI-5: phu ~1 khi sach chi co chuong',
          0.95 <= bmp.coverage(p2, txt) <= 1.0, bmp.coverage(p2, txt))


# --- DOI CHUNG AM 1: tat mat na khoi ma => phu phai TUT
def test_negative_control_mask():
    broken = load('bmp_broken', 'book_map_parse.py')
    broken.heading_mask = lambda lines: [True] * len(lines)   # tat BI-1
    txt = '\n'.join(['# Chương 01 — A'] + ['than'] * 100 +
                     ['```', '# 80% viec', '```'] + ['than'] * 100 +
                     ['# Chương 02 — B'] + ['than'] * 100)
    good = bmp.coverage(bmp.parse_chapters(txt), txt)
    bad = broken.coverage(broken.parse_chapters(txt), txt)
    check('DOI CHUNG AM: tat mat na lam phu tut', bad < good - 0.1,
          'tot=%.2f xau=%.2f' % (good, bad))


# --- Defect L4: duplicate key scheme loses chapter on collision with next number
def test_duplicate_then_next_number():
    """Verify that three duplicates of Ch.05 + real Ch.06 preserves all four chapters."""
    txt = '\n'.join(
        ['# Chương 05 — ban A'] + ['filler'] * 40 +
        ['# Chương 05 — ban B'] + ['filler'] * 40 +
        ['# Chương 05 — ban C'] + ['filler'] * 40 +
        ['# Chương 06 — chuong SAU that'] + ['filler'] * 40)
    p = bmp.parse_chapters(txt)
    ch = p['chapters']
    check('defect L4: tong so chuong = 4 (khong mat)', len(ch) == 4, len(ch))
    titles = sorted(c['title'] for c in ch.values())
    expected_titles = sorted(['ban A', 'ban B', 'ban C', 'chuong SAU that'])
    check('defect L4: ca 4 tieu de co mat', titles == expected_titles, titles)
    check('defect L4: dups = [5] khong co cap', p['dups'] == [5], p['dups'])


# --- Extra test for title separator handling
def test_title_separators():
    """Verify parse_chapters extracts titles cleanly with different separators."""
    test_cases = [
        ('# Chương 01 — Tên A', 'Tên A'),
        ('# Chương 02: Tên B', 'Tên B'),
        ('# Chương 03 · Tên C', 'Tên C'),
        ('# Chương 4 — Tên D', 'Tên D'),  # No zero padding
    ]
    for i, (heading, expected_title) in enumerate(test_cases, 1):
        # Create text with enough body lines to avoid table-of-contents warning
        txt = '\n'.join([heading] + ['filler text line'] * 40 +
                        ['# Chương %d — Dummy' % (i + 1)] + ['filler'] * 40)
        p = bmp.parse_chapters(txt)
        ch = p['chapters']
        actual_title = ch[i]['title'] if i in ch else None
        check('title sep test %d: %r' % (i, heading.split(' ', 3)[3]),
              actual_title == expected_title, actual_title)


def test_crossrefs():
    txt = '\n'.join(
        ['# Chương 01 — A', 'Chương 02 nói rõ hơn. Ch.03 cũng vậy.'] + ['x'] * 40 +
        ['# Chương 02 — B', 'Như Chương 01 đã nêu.'] + ['x'] * 40 +
        ['# Chương 03 — C', 'Không trỏ ai. Chương 99 không tồn tại.'] + ['x'] * 40)
    e = bmp.crossrefs(bmp.parse_chapters(txt))
    check('tham chieu: Ch.01 -> 02 va 03', e[1] == [2, 3], e[1])
    check('tham chieu: Ch.02 -> 01', e[2] == [1], e[2])
    check('tham chieu: bo chuong KHONG ton tai', e[3] == [], e[3])
    check('tham chieu: khong tro chinh no', 1 not in e.get(1, []), e[1])


# Do that: nhan pham vi nam trong THAN sach o 26/28 cuon khong co tep sidecar;
# `_scope_decision.md` chi co 4/32. Than sach la nguon CHINH.
BODY_SCOPE = '\n'.join(['# ⛔ Phạm vi lưu hành', '', '> BẢN NỘI BỘ', '',
                        '# Chương 01 — A'] + ['x'] * 40)
BODY_NOIBO = '\n'.join(['# BẢN NỘI BỘ — Workshop X', '', '# Chương 01 — A'] + ['x'] * 40)
SIDECAR = '\n'.join(['**mức nguyên bản: F2** — Diễn giải ứng dụng',
                     '**phạm vi phát hành: NỘI BỘ** — CEO tham khảo'])

def test_read_scope():
    lab, fid, src = bmp.read_scope(BODY_SCOPE, None)
    check('nguon 1: doc tu THAN sach', src == 'than-sach', src)
    check('nguon 1: nhan co chu NOI BO', 'NỘI BỘ' in lab, lab)

    lab2, fid2, src2 = bmp.read_scope(BODY_NOIBO, None)
    check('nguon 1: nhan dang "BẢN NỘI BỘ"', src2 == 'than-sach', src2)

    plain = '# Chương 01 — A\n' + 'x' * 40
    lab3, fid3, src3 = bmp.read_scope(plain, SIDECAR)
    check('nguon 2: lui ve sidecar', src3 == 'sidecar', src3)
    check('nguon 2: lay dung muc nguyen ban', fid3 == 'F2', fid3)
    check('nguon 2: lay dung nhan', 'NỘI BỘ' in lab3, lab3)

    lab4, fid4, src4 = bmp.read_scope(plain, None)
    check('BI-4: khong khai o dau => nhan BAO TOAN', src4 == 'bao-toan', src4)
    check('BI-4: nhan bao toan noi ro coi nhu NOI BO',
          lab4 == bmp.SCOPE_FALLBACK and 'NỘI BỘ' in lab4, lab4)
    check('BI-4: KHONG BAO GIO tra nhan rong', bool(lab4.strip()), repr(lab4))

    # than sach THANG sidecar khi ca hai co
    lab5, fid5, src5 = bmp.read_scope(BODY_SCOPE, SIDECAR)
    check('than sach uu tien hon sidecar', src5 == 'than-sach', src5)
    check('van lay muc nguyen ban tu sidecar khi than sach khong co',
          fid5 == 'F2', fid5)


# Khuon dan y KHONG nhat quan: do that tren usv-thiet-ke-he-thong, 13/28 chuong
# dung bullet `- `, 15/28 dung dong `Dạy:`. 22/32 cuon co heading `### `,
# 10/32 khong co. Lop nay PHAI suy thoai em, khong duoc bia.
OUTLINE = '\n'.join([
    '## Phần I — Trước khi vẽ gì',
    '### Ch.01 — Biên hệ thống',
    '**Neo** N1 · **Từ** 5.438 (= 5.400 + 38 nhãn nguồn) · **Nguồn** P&B 65%',
    '',
    '- Biên hệ thống không phải sự thật mà là **một lựa chọn**; đổi biên thì',
    '  hàm phụ thành hàm chính (tr.33).',
    '- Ba biên phải được vẽ và đặt tên.',
    '',
    'Hình (3): ba biên lồng nhau · bảng · ô biên',
    'Rủi ro: chương trừu tượng nhất cuốn sách',
    '',
    '### Ch.02 — Bỏ người  ⟵ **CHƯƠNG MỚI**',
    '**Neo** N2 · **Từ** 6.243 · **Nguồn** P&B 35%',
    'Dạy: cách dò chức năng không khai báo.',
    'Rủi ro: 🔴 chương dễ thành khẩu hiệu nhất',
])

def test_parse_outline():
    o = bmp.parse_outline(OUTLINE)
    check('dan y: 2 chuong', sorted(o) == [1, 2], sorted(o))
    check('dan y: ten chuong', o[1]['title'] == 'Biên hệ thống', o[1]['title'])
    check('dan y: phan', o[1]['part'] == (1, 'Trước khi vẽ gì'), o[1]['part'])
    check('dan y: so tu dat ra', o[1]['target'] == 5438, o[1]['target'])
    check('dan y: neo', o[1]['neo'] == 'N1', o[1]['neo'])
    check('dan y: so hinh', o[1]['figs'] == 3, o[1]['figs'])
    check('dan y: 2 bullet, co noi dong tiep', len(o[1]['bullets']) == 2,
          o[1]['bullets'])
    check('dan y: bullet noi lien dong thu hai',
          'hàm chính' in o[1]['bullets'][0], o[1]['bullets'][0])
    check('dan y: co cho 🔴', o[2]['red'] is True, o[2]['red'])
    check('dan y: chuong khong 🔴 thi red=False', o[1]['red'] is False, o[1]['red'])
    check('dan y: nhan CHUONG MOI', o[2]['new'] is True, o[2]['new'])
    check('dan y: ten chuong moi khong con dau ⟵',
          '⟵' not in o[2]['title'], o[2]['title'])
    check('suy thoai em: chuong dung "Dạy:" co 0 bullet, KHONG bia',
          o[2]['bullets'] == [], o[2]['bullets'])


def test_maybe():
    check('maybe: tep thieu tra mac dinh',
          bmp.maybe(os.path.join(HERE, 'khong-co-that.md'), bmp.parse_outline, {}) == {},
          'phai tra {}')
    check('maybe: tep co thi goi fn',
          bmp.maybe(os.path.join(HERE, 'book_map_parse.py'), lambda s: len(s) > 0, False)
          is True)


def test_scope_never_empty():
    """F1: sidecar with whitespace-only phạm vi must not return empty label."""
    sidecar_empty = '\n'.join(['**mức nguyên bản: F2**', '**phạm vi phát hành:    **'])
    plain = '# Chương 01 — A\n' + 'x' * 40
    lab, fid, src = bmp.read_scope(plain, sidecar_empty)
    check('F1: nhan KHONG rong sau strip', len(lab.strip()) > 0, repr(lab))
    check('F1: khong co khai thi bao toan, khong phai sidecar rong',
          src == 'bao-toan', src)


def test_scope_front_matter_only():
    """F2: scope heading in chapter body must be ignored, only front matter checked."""
    txt = '\n'.join(
        ['# Chương 01 — A'] + ['noi dung'] * 40 +
        ['# Chương 02 — Phạm vi lưu hành của sản phẩm đối thủ'] + ['noi dung'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('F2: khong doc sai tieu de chuong thanh khai', src == 'bao-toan', src)
    check('F2: nhan khong phai ten chuong', 'Chương 02' not in lab, lab)


def test_scope_wider_forms():
    """F3: accept wider variations of scope declarations in front matter.

    Fix round 1: khop _SCOPE_KEYWORDS khong du nua — muc do phai co mot
    dong mang token phan loai THAT (_TOKEN_RE) o dau do trong muc. Hinh 1
    gio them mot dong than mang token de van kiem tra duoc dang heading
    ngan ("Phạm vi" khong di kem "phát hành"/"lưu hành") ma khong bia."""
    # Test 1: # ⚠️ Phạm vi (without full phrase) + dong than co token
    txt1 = '\n'.join(['# ⚠️ Phạm vi', '', 'NỘI BỘ Workshop X.', '',
                       '# Chương 01 — A'] + ['x'] * 40)
    lab1, fid1, src1 = bmp.read_scope(txt1, None)
    check('F3 hình 1: heading với Phạm vi', src1 == 'than-sach', src1)
    check('F3 hình 1: nhan khong rong', len(lab1.strip()) > 0, repr(lab1))

    # Test 2: ## ⛔ CẢNH BÁO PHÁT HÀNH (all caps variation)
    txt2 = '\n'.join(['## ⛔ CẢNH BÁO PHÁT HÀNH', '> NỘI BỘ', '', '# Chương 01 — A'] + ['x'] * 40)
    lab2, fid2, src2 = bmp.read_scope(txt2, None)
    check('F3 hình 2: PHÁT HÀNH all caps', src2 == 'than-sach', src2)
    check('F3 hình 2: nhan khong rong', len(lab2.strip()) > 0, repr(lab2))

    # Test 3: blockquote với PHẠM VI PHÁT HÀNH
    txt3 = '\n'.join(['', '> ⚠️ **PHẠM VI PHÁT HÀNH: NỘI BỘ**', '', '# Chương 01 — A'] + ['x'] * 40)
    lab3, fid3, src3 = bmp.read_scope(txt3, None)
    check('F3 hình 3: blockquote PHẠM VI PHÁT HÀNH', src3 == 'than-sach', src3)
    check('F3 hình 3: nhan lay tu blockquote', 'NỘI BỘ' in lab3, lab3)

    # Test 4: blockquote với PHÂN LOẠI
    txt4 = '\n'.join(['', '> ## ⚠️ PHÂN LOẠI: REVIEW — NỘI BỘ', '', '# Chương 01 — A'] + ['x'] * 40)
    lab4, fid4, src4 = bmp.read_scope(txt4, None)
    check('F3 hình 4: blockquote PHÂN LOẠI', src4 == 'than-sach', src4)
    check('F3 hình 4: nhan khong rong', len(lab4.strip()) > 0, repr(lab4))

    # Test 5: prose-only NỘI BỘ (not heading/blockquote) — should fall back
    txt5 = '\n'.join(['Cuốn này là NỘI BỘ và chỉ dành cho CEO.', '', '# Chương 01 — A'] + ['x'] * 40)
    lab5, fid5, src5 = bmp.read_scope(txt5, None)
    check('F3 hình 5: prose-only NỘI BỘ fall back', src5 == 'bao-toan', src5)


def test_scope_blockquote_must_be_adjacent():
    """Finding A: a following blockquote is only the declaration's own
    continuation when it is the NEXT NON-BLANK line after the heading
    (blank lines may be skipped, nothing else). A prose line in between
    means an unrelated blockquote further down must NOT be used.

    Fix round 1: ca hai dong trong 'unrelated' (prose va blockquote SAI)
    khong mang token phan loai THAT, nen theo luat moi chung se bi bo qua
    du gi — doan nay them token vao ngay HEADING de bai test van do dung
    dieu no dinh do (mot dong KHAC khong lien quan khong duoc de bep nhan
    THAT), ma khong vi pham luat "khong bia phan loai"."""
    txt_unrelated = '\n'.join(
        ['# ⚠️ Phạm vi: NỘI BỘ', '', 'Đây là một dòng văn xuôi bình thường.',
         '> **PHÂN LOẠI: SAI — đây là khai báo KHÁC**', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt_unrelated, None)
    check('A: prose chen giua -> KHONG dung blockquote xa',
          'SAI' not in lab and 'KHÁC' not in lab, lab)
    check('A: van dung nhan tu HEADING, khong rong', len(lab.strip()) > 0, repr(lab))

    txt_adjacent = '\n'.join(
        ['# ⚠️ Phạm vi', '', '> **PHÂN LOẠI: REVIEW — NỘI BỘ**', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab2, fid2, src2 = bmp.read_scope(txt_adjacent, None)
    check('A: blockquote LIEN KE ngay sau heading (qua dong trong) -> dung blockquote',
          'REVIEW' in lab2 and 'NỘI BỘ' in lab2, lab2)


def test_scope_label_markup_clean():
    """Finding B: label must never retain stray '#' or '>' markup, even when
    the declaration is a blockquote that itself wraps a heading."""
    txt = '\n'.join(
        ['', '> ## ⚠️ PHÂN LOẠI: REVIEW — NỘI BỘ', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('B: nhan khong bat dau bang # > hoac khoang trang',
          lab[:1] not in ('#', '>', ' ', '\t'), repr(lab))
    check('B: nhan con giu PHÂN LOẠI', 'PHÂN LOẠI' in lab, lab)
    check('B: nhan con giu REVIEW', 'REVIEW' in lab, lab)


# --- Fix round 1 (2026-10-05): loi khai bao THAT nam trong THAN cua muc,
# khong phai tren chinh dong heading/blockquote khop _SCOPE_KEYWORDS.
def test_scope_label_from_section_body():
    """Dang dua-bia-ra: heading la mot TIEU DE muc
    (`# ⛔ Phạm vi lưu hành`, khong tu phan loai), loi khai bao THAT nam o
    mot dong than sau do. Nhan phai la dong do, khong phai tieu de."""
    txt = '\n'.join(
        ['# ⛔ Phạm vi lưu hành', '',
         '**NỘI BỘ XƯỞNG — KHÔNG PHÁT HÀNH RA NGOÀI.**', '',
         'Đây là một đoạn văn xuôi không liên quan, giải thích lý do.', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('section-body: nguon than-sach', src == 'than-sach', src)
    check('section-body: nhan KHONG phai la tieu de muc',
          lab != 'Phạm vi lưu hành' and '⛔' not in lab, lab)
    check('section-body: nhan la dong co token thuc',
          'NỘI BỘ XƯỞNG' in lab, lab)


def test_scope_skips_pipeline_note():
    """Dang khu-pho-6-bang: blockquote ke sau heading la CHU THICH DUONG
    ONG (noi ve frontmatter/md_to_epub), KHONG mang token — phai bi bo qua;
    loi khai bao THAT nam sau mot sub-heading sau hon (`## Quyết định phát
    hành`), van nam TRONG cung muc vi sau hon tieu de mo muc."""
    txt = '\n'.join(
        ['# ⛔ Phạm vi lưu hành', '',
         '> Trang này nằm trong thân sách, không nằm trong frontmatter '
         'mà md_to_epub.py tạo ra.', '',
         '## Quyết định phát hành', '',
         '**CEO ký duyệt 2026-09-15: NỘI BỘ XƯỞNG.**', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('skip pipeline note: nguon than-sach', src == 'than-sach', src)
    check('skip pipeline note: nhan co NỘI BỘ', 'NỘI BỘ' in lab, lab)
    check('skip pipeline note: khong lan chu thich ve frontmatter',
          'frontmatter' not in lab, lab)
    check('skip pipeline note: khong lan chu thich ve md_to_epub',
          'md_to_epub' not in lab, lab)


# Fix round 2 (2026-10-05): _PIPELINE_NOISE_RE bi XOA — no trung voi chinh
# danh sach tu cong do tren kiem, nen cong "qua" ma khong do duoc gi ca.
# Tin hieu THAT la CAU TRUC: token nam TRONG mot doan ma inline (giua hai
# backtick) la mot gia tri bi TRICH DAN, khong phai mot loi KHANG DINH.
def test_scope_token_in_code_span_is_not_a_declaration():
    """Dang hang-rao-song-va-nuoc THAT: mot blockquote trich nguyen van mot
    GIA TRI VI DU co token NAM TRONG backtick — day la TRICH DAN, khong
    phai loi khang dinh. Loi khang dinh THAT nam o mot dong **in dam** sau
    do, trong cung muc. Nhan phai la dong in dam, khong duoc lan chu
    "frontmatter" tu dong backtick."""
    txt = '\n'.join(
        ['# ⛔ Phạm vi lưu hành', '',
         '> `distribution: ⛔ NỘI BỘ` ở frontmatter và 0 trên 70 tệp chứa chữ ấy.', '',
         '**NỘI BỘ XƯỞNG.**', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('code-span: nguon than-sach', src == 'than-sach', src)
    check('code-span: nhan la dong in dam THAT, khong phai trich dan',
          lab == 'NỘI BỘ XƯỞNG.' or '**NỘI BỘ XƯỞNG.**' in lab, lab)
    check('code-span: khong lan chu "frontmatter" tu dong backtick',
          'frontmatter' not in lab, lab)


def test_scope_only_code_span_token_falls_back():
    """Cung blockquote backtick nhu tren, nhung KHONG co dong khang dinh
    nao khac trong muc -> day KHONG phai mot loi khai bao dung (token duy
    nhat nam trong trich dan). Phai lui ve SCOPE_FALLBACK/bao-toan."""
    txt = '\n'.join(
        ['# ⛔ Phạm vi lưu hành', '',
         '> `distribution: ⛔ NỘI BỘ` ở frontmatter và 0 trên 70 tệp chứa chữ ấy.', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('code-span only: lui ve bao-toan', src == 'bao-toan', src)
    check('code-span only: nhan la dung SCOPE_FALLBACK',
          lab == bmp.SCOPE_FALLBACK, lab)


def test_scope_no_token_falls_back():
    """Muc khop tu khoa scope nhung KHONG dong nao trong than co token phan
    loai THAT -> day KHONG phai mot loi khai bao dung. Phai lui ve
    SCOPE_FALLBACK/bao-toan — khong duoc bia phan loai."""
    txt = '\n'.join(
        ['# ⛔ Phạm vi lưu hành', '',
         'Chúng tôi chưa quyết định việc này.', '',
         '# Chương 01 — A'] + ['x'] * 40)
    lab, fid, src = bmp.read_scope(txt, None)
    check('no-token: lui ve bao-toan, KHONG bia phan loai',
          src == 'bao-toan', src)
    check('no-token: nhan la dung SCOPE_FALLBACK',
          lab == bmp.SCOPE_FALLBACK, lab)


def test_scope_class():
    check('scope_class: mot token NỘI BỘ',
          bmp.scope_class('**NỘI BỘ XƯỞNG.**') == 'NỘI BỘ',
          bmp.scope_class('**NỘI BỘ XƯỞNG.**'))
    check('scope_class: REVIEW va NỘI BỘ theo thu tu xuat hien',
          bmp.scope_class('⚠️ PHÂN LOẠI: REVIEW — NỘI BỘ WORKSHOP X')
          == 'REVIEW — NỘI BỘ',
          bmp.scope_class('⚠️ PHÂN LOẠI: REVIEW — NỘI BỘ WORKSHOP X'))
    check('scope_class: mot token SENSITIVE',
          bmp.scope_class('mức SENSITIVE') == 'SENSITIVE',
          bmp.scope_class('mức SENSITIVE'))
    check('scope_class: khong token nao -> CHƯA KHAI',
          bmp.scope_class('Một câu không có từ phân loại nào.') == 'CHƯA KHAI',
          bmp.scope_class('Một câu không có từ phân loại nào.'))
    check('scope_class: SCOPE_FALLBACK luon la CHƯA KHAI du chua chu NỘI BỘ',
          bmp.scope_class(bmp.SCOPE_FALLBACK) == 'CHƯA KHAI',
          bmp.scope_class(bmp.SCOPE_FALLBACK))


# --- DOI CHUNG AM 4: chuong chay den EOF => chuong cuoi PHAI phinh
def test_negative_eof():
    broken = load('bmp_eof', 'book_map_parse.py')
    orig = broken.pick_level
    def no_stop(txt):
        depth, hits, warn = orig(broken.chapter_levels(txt))
        lines = txt.splitlines()
        out = {}
        for k, (ln, num, head) in enumerate(hits):
            end = hits[k + 1][0] if k + 1 < len(hits) else len(lines)
            body = '\n'.join(lines[ln + 1:end])
            out[num] = {'title': '', 'words': broken.wc(body), 'mermaid': 0,
                        'body': body, 'line': ln}
        return {'chapters': out, 'depth': depth, 'warn': warn, 'dups': []}
    txt = '\n'.join(['# Chương 01 — A'] + ['than'] * 100 +
                     ['# Chương 02 — B'] + ['than'] * 100 +
                     ['# Phụ lục'] + ['phu luc'] * 400)
    good = bmp.parse_chapters(txt)['chapters']
    bad = no_stop(txt)['chapters']
    gl = good[max(good)]['words']; bl = bad[max(bad)]['words']
    check('DOI CHUNG AM EOF: de chay den EOF lam chuong cuoi phinh',
          bl > gl * 1.8, 'tot=%d xau=%d' % (gl, bl))


# --- DOI CHUNG AM 5: co dinh luat dung theo depth => sach H2 bi cat vun
def test_negative_fixed_stop():
    broken = load('bmp_fix', 'book_map_parse.py')
    def fixed_stop(txt):
        depth, hits, warn = broken.pick_level(broken.chapter_levels(txt))
        lines = txt.splitlines()
        mask = broken.heading_mask(lines)
        stop = [i for i, L in enumerate(lines)
                if mask[i] and __import__('re').match(r'^#{1,%d} +\S' % depth, L)]
        out = {}
        for ln, num, head in hits:
            nxt = [i for i in stop if i > ln]
            body = '\n'.join(lines[ln + 1:nxt[0] if nxt else len(lines)])
            out[num] = {'title': '', 'words': broken.wc(body), 'mermaid': 0,
                        'body': body, 'line': ln}
        return {'chapters': out, 'depth': depth, 'warn': warn, 'dups': []}
    good = bmp.parse_chapters(FIX_H2_MIXED)['chapters']
    bad = fixed_stop(FIX_H2_MIXED)['chapters']
    check('DOI CHUNG AM luat dung: co dinh theo depth lam sach H2 cat vun',
          bad[1]['words'] < good[1]['words'] / 1.5,
          'tot=%d xau=%d' % (good[1]['words'], bad[1]['words']))


# --- ra TOAN KHO: bo qua neu may khong co kho
CORPUS = r'D:/Workshop_X/3_Resources/Books'

def test_corpus():
    if not os.path.isdir(CORPUS):
        print('SKIP ra toan kho — khong thay %s' % CORPUS)
        return
    books = [s for s in sorted(os.listdir(CORPUS))
             if os.path.exists(os.path.join(CORPUS, s, 'book.md'))]
    check('kho: tim duoc >= 30 cuon', len(books) >= 30, len(books))
    low, nochap = [], []
    for s in books:
        txt = bmp.rd(os.path.join(CORPUS, s, 'book.md'))
        p = bmp.parse_chapters(txt)
        if not p['chapters']:
            nochap.append(s); continue
        cov = bmp.coverage(p, txt)
        if cov < 0.70:
            low.append((s, round(cov, 2)))
    check('kho: moi cuon parse ra it nhat 1 chuong', nochap == [], nochap)
    check('kho: khong cuon nao duoi nguong CHAN 70%%', low == [], low)


# ============================================================
# Fix round 1 (2026-10-05): doi chung am 2 va 4 duoc CEO tu do lai tren
# CHINH cac cuon sach that, va xac nhan ca hai giu nguyen. Doi chung am 3
# (EOF) thi KHONG giu — ty le 'chuong cuoi / trung vi' 1.8x im lang voi
# loi THAT (1.49x) vi loi nam GIUA hai chuong cuoi dai THAT (1.61x/1.48x).
# Cam bien thong ke bi thay bang stray_headings() — dieu kien CAU TRUC.
# ============================================================

# --- DOI CHUNG AM 2 (sach THAT): tau-nhom-han-quoc-phong, tat mat na khoi ma
def test_negative_control_mask_real():
    p = os.path.join(CORPUS, 'tau-nhom-han-quoc-phong', 'book.md')
    if not os.path.exists(p):
        print('SKIP DOI CHUNG AM 2 (sach that) — khong thay %s' % p)
        return
    broken = load('bmp_broken_real', 'book_map_parse.py')
    broken.heading_mask = lambda lines: [True] * len(lines)   # tat BI-1
    txt = bmp.rd(p)
    good = bmp.coverage(bmp.parse_chapters(txt), txt)
    bad = broken.coverage(broken.parse_chapters(txt), txt)
    check('DOI CHUNG AM 2 (sach that tau-nhom-han-quoc-phong): '
          'phu TUT duoi nguong CHAN 70%% khi tat mat na khoi ma',
          bad < 0.70, 'tot=%.3f xau=%.3f' % (good, bad))
    check('DOI CHUNG AM 2 (sach that): phu DUNG phai cao (>90%%) de thay ro do lech',
          good > 0.90, good)


# --- DOI CHUNG AM 4 (sach THAT): principles-ba-tai-san, co dinh luat dung
def test_negative_fixed_stop_real():
    p = os.path.join(CORPUS, 'principles-ba-tai-san', 'book.md')
    if not os.path.exists(p):
        print('SKIP DOI CHUNG AM 4 (sach that) — khong thay %s' % p)
        return
    broken = load('bmp_fix_real', 'book_map_parse.py')
    def fixed_stop(txt):
        depth, hits, warn = broken.pick_level(broken.chapter_levels(txt))
        lines = txt.splitlines()
        mask = broken.heading_mask(lines)
        stop = [i for i, L in enumerate(lines)
                if mask[i] and __import__('re').match(r'^#{1,%d} +\S' % depth, L)]
        out = {}
        for ln, num, head in hits:
            nxt = [i for i in stop if i > ln]
            body = '\n'.join(lines[ln + 1:nxt[0] if nxt else len(lines)])
            out[num] = {'title': '', 'words': broken.wc(body), 'mermaid': 0,
                        'body': body, 'line': ln}
        return {'chapters': out, 'depth': depth, 'warn': warn, 'dups': []}
    txt = bmp.rd(p)
    good = bmp.parse_chapters(txt)['chapters']
    bad = fixed_stop(txt)['chapters']
    gw = sorted(c['words'] for c in good.values())
    bw = sorted(c['words'] for c in bad.values())
    med_g, med_b = gw[len(gw) // 2], bw[len(bw) // 2]
    check('DOI CHUNG AM 4 (sach that principles-ba-tai-san): '
          'trung vi tut ve ~326 tu/chuong khi co dinh luat dung theo depth',
          300 <= med_b <= 360, 'tot=%d xau=%d' % (med_g, med_b))


# --- stray_headings(): don vi, hai nhanh cua BI-2 (depth==1 vs depth>1)
def test_stray_headings_unit():
    bad = {'chapters': {1: {'body': '\n'.join(
                ['# Lạc vào thân — khong duoc o day'] + ['lac'] * 10)}},
           'depth': 1, 'warn': None, 'dups': []}
    check('stray_headings: depth==1, mot H1 lac trong than => 1 vi pham',
          bmp.stray_headings(bad) == 1, bmp.stray_headings(bad))

    good_h2 = {'chapters': {1: {'body': '\n'.join(
                ['## Một tiểu mục cùng cấp'] + ['than'] * 10)}},
               'depth': 2, 'warn': None, 'dups': []}
    check('stray_headings: depth>1, tieu de CUNG muc la tieu muc hop phap '
          '=> 0 vi pham', bmp.stray_headings(good_h2) == 0,
          bmp.stray_headings(good_h2))

    bad_h2 = {'chapters': {1: {'body': '\n'.join(
                ['# Tieu de NONG hon depth lac vao'] + ['than'] * 10)}},
              'depth': 2, 'warn': None, 'dups': []}
    check('stray_headings: depth>1, tieu de NONG HON depth la vi pham => 1',
          bmp.stray_headings(bad_h2) == 1, bmp.stray_headings(bad_h2))

    in_fence = {'chapters': {1: {'body': '\n'.join(
                ['```', '# 80% cong viec trong khoi ma', '```'] + ['than'] * 10)}},
                'depth': 1, 'warn': None, 'dups': []}
    check('stray_headings: # trong khoi ma KHONG duoc dem',
          bmp.stray_headings(in_fence) == 0, bmp.stray_headings(in_fence))

    no_depth = {'chapters': {}, 'depth': None, 'warn': 'x', 'dups': []}
    check('stray_headings: khong co depth => 0, khong crash',
          bmp.stray_headings(no_depth) == 0, bmp.stray_headings(no_depth))


def _no_stop_generic(bmpmod, txt):
    """Tat HOAN TOAN luat dung (bo qua stop[] — moi chuong chi cat o 'hit'
    (tieu de chuong CUNG muc) ke tiep, hoac EOF cho chuong cuoi). Day la
    cach loi 'chuong chay den EOF' THAT xay ra: KHONG chi chuong cuoi — moi
    chuong giua co tieu de NONG HON xen giua hai 'hit' (vd tieu de Phan)
    cung mat bien dung."""
    depth, hits, warn = bmpmod.pick_level(bmpmod.chapter_levels(txt))
    lines = txt.splitlines()
    out = {}
    for k, (ln, num, head) in enumerate(hits):
        end = hits[k + 1][0] if k + 1 < len(hits) else len(lines)
        body = '\n'.join(lines[ln + 1:end])
        out[num] = {'title': '', 'words': bmpmod.wc(body), 'mermaid': 0,
                     'body': body, 'line': ln + 1}
    return {'chapters': out, 'depth': depth, 'warn': warn, 'dups': []}


# --- DOI CHUNG AM 3 (sach THAT, lop DO): stray_headings PHAI bat duoc loi
# EOF-overrun ma ty le bloat KHONG bat duoc. 4 so do that CEO da tu kiem,
# cong do PHAI tai tao dung.
STRAY_EOF_MEASURED = {
    'tu-khong-den-mot': 10,
    'ghi-de-quy-trach-nhiem': 6,
    'usv-thiet-ke-he-thong': 6,
    'finding-alphas': 0,   # chuong cuoi DAI THAT (1.61x) — phai IM LANG
}

def test_stray_headings_eof_corpus():
    if not os.path.isdir(CORPUS):
        print('SKIP stray_headings EOF (sach that) — khong thay %s' % CORPUS)
        return
    for slug, expect in STRAY_EOF_MEASURED.items():
        p = os.path.join(CORPUS, slug, 'book.md')
        if not os.path.exists(p):
            print('SKIP stray_headings EOF %s — khong thay tep' % slug)
            continue
        txt = bmp.rd(p)
        n = bmp.stray_headings(_no_stop_generic(bmp, txt))
        check('stray_headings EOF %s: tai tao dung so do that = %d'
              % (slug, expect), n == expect, n)


# --- Doi chung DUONG (yeu cau #6): stray_headings PHAI im lang tren ma DUNG
def test_stray_headings_positive_corpus():
    if not os.path.isdir(CORPUS):
        print('SKIP stray_headings duong — khong thay %s' % CORPUS)
        return
    books = [s for s in sorted(os.listdir(CORPUS))
             if os.path.exists(os.path.join(CORPUS, s, 'book.md'))]
    viol = []
    for s in books:
        txt = bmp.rd(os.path.join(CORPUS, s, 'book.md'))
        p = bmp.parse_chapters(txt)
        if not p['chapters']:
            continue
        n = bmp.stray_headings(p)
        if n:
            viol.append((s, n))
    check('stray_headings: 0 vi pham tren toan kho voi ma DUNG '
          '(mot cam bien chi bat loi ma khong bao gio im thi vo dung)',
          viol == [], viol)


def test_maybe_bad_encoding():
    """F4: maybe() must catch UnicodeDecodeError and return default."""
    # Create a file with invalid UTF-8 bytes (latin-1 bytes that aren't valid UTF-8)
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.md', delete=False) as f:
        # Write latin-1 encoded text that is NOT valid UTF-8
        f.write(b'Title: \xe9cole')  # latin-1 encoded 'école' — the \xe9 byte is invalid UTF-8
        temp_path = f.name
    try:
        result = bmp.maybe(temp_path, bmp.parse_outline, {})
        check('F4: bad encoding returns default', result == {}, result)
    finally:
        os.unlink(temp_path)


if __name__ == '__main__':
    test_wc(); test_mask(); test_pick_level(); test_crlf(); test_separators()
    test_parse_chapters(); test_mermaid_count(); test_duplicate_numbers()
    test_coverage(); test_negative_control_mask(); test_duplicate_then_next_number(); test_title_separators()
    test_crossrefs(); test_read_scope(); test_parse_outline(); test_maybe()
    test_scope_never_empty(); test_scope_front_matter_only(); test_scope_wider_forms(); test_maybe_bad_encoding()
    test_scope_blockquote_must_be_adjacent(); test_scope_label_markup_clean()
    test_scope_label_from_section_body(); test_scope_skips_pipeline_note()
    test_scope_token_in_code_span_is_not_a_declaration()
    test_scope_only_code_span_token_falls_back()
    test_scope_no_token_falls_back(); test_scope_class()
    test_negative_eof(); test_negative_fixed_stop(); test_corpus()
    test_negative_control_mask_real(); test_negative_fixed_stop_real()
    test_stray_headings_unit(); test_stray_headings_eof_corpus()
    test_stray_headings_positive_corpus()
    print()
    if FAILED:
        print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
        sys.exit(1)
    print('Tat ca PASS')
