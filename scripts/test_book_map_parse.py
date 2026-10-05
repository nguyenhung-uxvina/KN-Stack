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


if __name__ == '__main__':
    test_wc(); test_mask(); test_pick_level(); test_crlf(); test_separators()
    print()
    if FAILED:
        print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
        sys.exit(1)
    print('Tat ca PASS')
