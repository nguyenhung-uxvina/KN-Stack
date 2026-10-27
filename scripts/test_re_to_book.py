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
