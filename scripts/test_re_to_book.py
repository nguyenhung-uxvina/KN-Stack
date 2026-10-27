# -*- coding: utf-8 -*-
"""Kiem cac script cua /re-to-book (pytest)."""
import importlib.util
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, '..', 'skills', 'book', 're-to-book', 'scripts'))
sys.path.insert(0, SKILL)


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(SKILL, name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ru = _load('re_units')


def test_normalize_crlf_bom_nfd_equal():
    a = '﻿Phỏng đoán\r\nx  \r\n'
    b = unicodedata.normalize('NFD', 'Phỏng đoán\nx\n')
    assert ru.normalize(a) == ru.normalize(b)


def test_gt_card_items_become_units():
    t = '# T\n\n## GT-3DS-001 — Góc nhận\n\n1. **Tiêu đề:** a\n6. **KẾT QUẢ + khuyến nghị:** *(điền sau)*\n7. **DỰ ĐOÁN VIẾT TRƯỚC:** ___ — người ký ___ — ngày ___\n'
    ids = [u.id for u in ru.split_units(t)]
    assert 'GT-3DS-001.1' in ids and 'GT-3DS-001.6' in ids and 'GT-3DS-001.7' in ids


def test_coded_row_is_own_unit_and_excluded_from_section_hash():
    base = '## Nợ\n\nchữ\n\n| Mã | Nội dung |\n|---|---|\n| N-013 | 26 vs 24 |\n'
    edited = base.replace('26 vs 24', '26 vs 24 (đã đóng)')
    u1 = {u.id: u.sha256 for u in ru.split_units(base)}
    u2 = {u.id: u.sha256 for u in ru.split_units(edited)}
    assert u1['Nợ'] == u2['Nợ'] and u1['row:N-013'] != u2['row:N-013']


def test_duplicate_headings_get_stable_suffix():
    ids = [u.id for u in ru.split_units('## Ghi chú\na\n## Ghi chú\nb\n')]
    assert ids == ['Ghi chú', 'Ghi chú~2']


def test_headingless_file_is_single_file_unit():
    us = ru.split_units('chỉ có chữ\nhai dòng\n')
    assert [(u.id, u.kind) for u in us] == [('file', 'file')]


def test_bold_code_in_first_cell_recognised():
    assert 'row:C-3' in [u.id for u in ru.split_units('| **C-3** | cờ IP |\n')]


rl = _load('re_labels')


def U(text): return ru.Unit(id='x', kind='section', text=text, sha256='')


def test_inline_weakest_label_wins():
    assert rl.resolve(U('đã biết … nhưng phỏng đoán về khe'), None, None).label == 'conjecture'


def test_file_cap_inherited_and_caps_inline():
    cap = rl.file_cap(ru.split_units('Mọi phần tử mang nhãn ≤ phỏng đoán.\n## A\nđã biết: 730 mm\n## B\nkhông nhãn\n'))
    assert cap == 'conjecture'
    assert rl.resolve(U('đã biết: 730 mm'), cap, None).label == 'conjecture'
    l = rl.resolve(U('không nhãn'), cap, None)
    assert (l.label, l.source) == ('conjecture', 'kế thừa: tệp')


def test_no_label_anywhere_is_unassigned():
    assert rl.resolve(U('730 mm'), None, None).label == 'chưa gán'


def test_ceiling_lowest_letter_and_caps_confidence():
    st = '---\nconfidence_ceiling: theo miền — M hình học; M–H môi trường; L bố trí màn\n---\n'
    c = rl.ceiling_from_state(st)
    assert c == 'L'
    l = rl.resolve(U('phỏng đoán, mức H'), None, c)
    assert (l.confidence, l.label) == ('L', 'conjecture')


def test_ceiling_does_not_create_knowledge_label():
    assert rl.resolve(U('730 mm'), None, 'M').label == 'chưa gán'


def test_bare_symbol_cell_is_not_confidence():
    l = rl.resolve(U('| L | 730 | mm |'), None, None)
    assert (l.confidence, l.confidence_source) == (None, 'không có')
    l = rl.resolve(U('| H | 12 | mm |'), None, 'M')
    assert (l.confidence, l.confidence_source) == ('M', 'kế thừa: trần miền')


def test_confidence_column_cell_is_read():
    t = '| Mã | Nội dung | Mức tin |\n|---|---|---|\n| a | x | M |\n| b | y | H |\n'
    l = rl.resolve(U(t), None, None)
    assert (l.confidence, l.confidence_source) == ('M', 'tại chỗ')


def test_end_to_end_encoding_invariance():
    src = ('---\nk: v\n---\nMở đầu\n\n## Mục đầu\n\nchữ Việt\n\n'
           '## GT-3DS-001 — Góc nhận\n\n1. **Tiêu đề:** a\n6. **KẾT QUẢ:** b\n\n'
           '## Nợ\n\n| Mã | Nội dung |\n|---|---|\n| N-013 | 26 vs 24 |\n')
    a = '\ufeff' + src.replace('\n', '\r\n')
    b = unicodedata.normalize('NFD', src)
    ka = [(u.id, u.sha256) for u in ru.split_units(a)]
    kb = [(u.id, u.sha256) for u in ru.split_units(b)]
    assert ka == kb and len(ka) >= 5
