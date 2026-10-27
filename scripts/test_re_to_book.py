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


# ---------------- Task 3: re_manifest ----------------
import pytest  # noqa: E402

rm = _load('re_manifest')
CLASSES = os.path.join(SKILL, 're_classes.json')


def make_dossier(tmp_path):
    d = tmp_path / 'Demo'
    (d / '_source').mkdir(parents=True)
    (d / '_analysis').mkdir()

    def w(n, s):
        (d / n).write_text(s, encoding='utf-8')
    w('RE_D_Hypotheses.md', '# Gia thuyet\n\n## GT-D-001 — Goc nhan\n\n1. **Tiêu đề:** a\n'
      '6. **KẾT QUẢ + khuyến nghị:** *(điền sau)*\n'
      '7. **DỰ ĐOÁN VIẾT TRƯỚC:** bia lệch 2 mm — người ký Nguyễn A — ngày ___\n')
    w('RE_D_Precision_Debt.md', '# Nợ chính xác\n\n| Mã | Nội dung |\n|---|---|\n| N-001 | sai số 0,5 mm |\n')
    w('RE_D_Idea_Log.md', '# Idea\n\n| YT-001 | lọc 890 nm, cửa sổ 20 nm |\n')
    w('RE_D_S0_Legal_Gate.md', '# Legal\n\nnội dung pháp lý\n')
    w('RE_D_S1A_Deconstruction.md', '# S1A\n\n## Khung\n\nphỏng đoán về khung\n')
    w('_pipeline_state.md', '---\nconfidence_ceiling: M\n---\n# state\n')
    (d / '_source' / 'a.pdf').write_bytes(b'%PDF-1.4 abc')
    w('_analysis/x.py', 'print(1)\n')
    return str(d)


def test_build_classifies_and_snapshot_excludes_blocked(tmp_path):
    root = make_dossier(tmp_path)
    m = rm.build_manifest({'Demo': root}, CLASSES)
    assert m['files']['Demo/RE_D_Idea_Log.md']['class'] == 'BLOCK'
    assert 'units' not in m['files']['Demo/RE_D_Idea_Log.md']
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    assert not (out / 'Demo' / 'RE_D_Idea_Log.md').exists()
    assert not (out / 'Demo' / 'RE_D_S0_Legal_Gate.md').exists()
    assert (out / 'Demo' / 'RE_D_S1A_Deconstruction.md').exists()


def test_half_signed_prediction_is_cut(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    u = m['files']['Demo/RE_D_Hypotheses.md']['units']
    assert u['GT-D-001.7']['cut'] is True and u['GT-D-001.6']['empty_result'] is True
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_Hypotheses.md').read_text(encoding='utf-8')
    assert '⟨chờ ký⟩' in s and '⟨chờ đo⟩' in s and 'Nguyễn A' not in s


def test_unclassified_file_stops_with_exit_2_and_writes_nothing(tmp_path):
    root = make_dossier(tmp_path); (tmp_path / 'Demo' / 'la.md').write_text('x', encoding='utf-8')
    book = tmp_path / 'Book'; book.mkdir()
    rc = rm.main(['build', '--re', str(root), '--book', str(book)])
    assert rc == 2 and not (book / '_re_manifest.json').exists()
    assert not (book / '_re_snapshot').exists()


def test_manifest_keys_are_relative_to_dossier_name(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    assert all(k.startswith('Demo/') and '\\' not in k for k in m['files'])
    assert m['roots']['Demo'] == str(tmp_path / 'Demo')
    assert 'Demo/_source/a.pdf' in m['sources'] and 'Demo/_analysis/x.py' in m['sources']


def test_gapfill_only_approved_items_reach_snapshot(tmp_path):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_Book_GapFill.md').write_text(
        '---\nstatus: chờ CEO duyệt\n---\n## GF-001\n**Trạng thái:** đã duyệt\nA\n## GF-002\n**Trạng thái:** chờ\nB\n', encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES); out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_Book_GapFill.md').read_text(encoding='utf-8')
    assert 'GF-001' in s and 'GF-002' not in s
    ent = m['files']['Demo/RE_D_Book_GapFill.md']
    assert 'GF-002' not in ' '.join(ent['units']) and ent['gapfill']['excluded'] == ['## GF-002']


def test_gapfill_without_approval_is_blocked(tmp_path):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_Book_GapFill.md').write_text(
        '---\nstatus: nháp\n---\n## GF-001\n**Trạng thái:** chờ\nA\n', encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES)
    assert m['files']['Demo/RE_D_Book_GapFill.md']['class'] == 'BLOCK'


def test_signed_prediction_is_kept(tmp_path):
    root = make_dossier(tmp_path)
    p = tmp_path / 'Demo' / 'RE_D_Hypotheses.md'
    p.write_text(p.read_text(encoding='utf-8').replace('ngày ___', 'ngày 2026-10-01'), encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES)
    assert m['files']['Demo/RE_D_Hypotheses.md']['units']['GT-D-001.7']['cut'] is False


def test_ceiling_from_own_dossier_state(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    u = m['files']['Demo/RE_D_S1A_Deconstruction.md']['units']['Khung']
    assert u['confidence'] == 'M' and u['label'] == 'conjecture'


def test_cli_ok_and_duplicate_basenames(tmp_path):
    root = make_dossier(tmp_path)
    book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    assert (book / '_re_manifest.json').exists() and (book / '_re_snapshot' / 'Demo').is_dir()
    assert rm.main(['build', '--re', root + ',' + root, '--book', str(book)]) == 2


def test_vanished_file_raises_input_error(tmp_path, monkeypatch):
    root = make_dossier(tmp_path)
    real = rm._read_text

    def flaky(p):
        if p.endswith('RE_D_S1A_Deconstruction.md'):
            raise FileNotFoundError(p)
        return real(p)
    monkeypatch.setattr(rm, '_read_text', flaky)
    with pytest.raises(rm.InputError):
        rm.build_manifest({'Demo': root}, CLASSES)


# ---------------- Task 3 fix round 1 ----------------
def _hyp(tmp_path, body):
    root = make_dossier(tmp_path)
    p = tmp_path / 'Demo' / 'RE_D_Hypotheses.md'
    p.write_text(body, encoding='utf-8')
    return root


def test_duplicate_item7_and_item6_are_cut(tmp_path):
    body = ('## GT-D-001 — X\n\n'
            '6. **KẾT QUẢ + khuyến nghị:** *(điền sau)*\n'
            '7. **DỰ ĐOÁN VIẾT TRƯỚC:** A — người ký Ba Ca — ngày 2026-10-01\n'
            '6. **KẾT QUẢ + khuyến nghị:** *(điền sau)*\n'
            '7. **DỰ ĐOÁN VIẾT TRƯỚC:** bia lệch BÍ_MẬT — người ký ___ — ngày ___\n')
    root = _hyp(tmp_path, body)
    m = rm.build_manifest({'Demo': root}, CLASSES)
    u = m['files']['Demo/RE_D_Hypotheses.md']['units']
    assert u['GT-D-001.7']['cut'] is False and u['GT-D-001.7~2']['cut'] is True
    assert u['GT-D-001.6~2']['empty_result'] is True
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_Hypotheses.md').read_text(encoding='utf-8')
    assert 'BÍ_MẬT' not in s and s.count('⟨chờ ký⟩') == 1 and s.count('⟨chờ đo⟩') == 2
    assert 'Ba Ca' in s


def test_signed_requires_signer_and_digit_date(tmp_path):
    for tail, cut in [('người ký ___ — ngày 2026-10-01', True),
                      ('người ký Nguyễn A — ngày ___ (dd/mm)', True),
                      ('người ký Nguyễn A — ngày 01/10/2026', False)]:
        body = '## GT-D-001 — X\n\n7. **DỰ ĐOÁN VIẾT TRƯỚC:** p — %s\n' % tail
        sub = tmp_path / str(abs(hash(tail)))
        sub.mkdir()
        m = rm.build_manifest({'Demo': _hyp(sub, body)}, CLASSES)
        assert m['files']['Demo/RE_D_Hypotheses.md']['units']['GT-D-001.7']['cut'] is cut


def test_apply_cuts_unplaceable_raises():
    u = ru.Unit('GT-D-001.7', 'gt_item', '7. **DỰ ĐOÁN VIẾT TRƯỚC:** x', 'h')
    with pytest.raises(rm.InputError):
        rm._apply_cuts('khac han', [u])


def test_snapshot_failure_midway_keeps_previous_snapshot_and_no_manifest(tmp_path, monkeypatch):
    root = make_dossier(tmp_path)
    book = tmp_path / 'Book'; book.mkdir()
    old = book / '_re_snapshot'; old.mkdir(); (old / 'keep.txt').write_text('cu', encoding='utf-8')
    real = rm._read_text
    seen = {'n': 0}

    def flaky(p):
        if p.endswith('RE_D_S1A_Deconstruction.md'):
            seen['n'] += 1
            if seen['n'] >= 2:
                raise FileNotFoundError(p)
        return real(p)
    monkeypatch.setattr(rm, '_read_text', flaky)
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 2
    assert not (book / '_re_manifest.json').exists()
    assert not (book / '_re_manifest.json.tmp').exists()
    assert (old / 'keep.txt').exists() and not (old / 'Demo').exists()
    assert not (book / '_re_snapshot.tmp').exists()


def test_bad_classes_json_exit_2(tmp_path):
    root = make_dossier(tmp_path)
    book = tmp_path / 'Book'; book.mkdir()
    bad = tmp_path / 'bad.json'; bad.write_text('{ khong json', encoding='utf-8')
    assert rm.main(['build', '--re', root, '--book', str(book), '--classes', str(bad)]) == 2
    assert rm.main(['build', '--re', root, '--book', str(book),
                    '--classes', str(tmp_path / 'none.json')]) == 2
    assert not (book / '_re_manifest.json').exists()


def test_re_dot_uses_abspath_name(tmp_path, monkeypatch):
    root = make_dossier(tmp_path)
    book = tmp_path / 'Book'; book.mkdir()
    monkeypatch.chdir(root)
    assert rm.main(['build', '--re', '.', '--book', str(book)]) == 0
    assert (book / '_re_snapshot' / 'Demo').is_dir()
