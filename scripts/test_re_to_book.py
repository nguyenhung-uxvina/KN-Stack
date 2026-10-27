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


# ---------------- Task 3 fix round 2 ----------------
def test_read_file_with_coded_table_then_paragraph_snapshot_equals_original(tmp_path):
    root = make_dossier(tmp_path)
    body = ('## Bảng\n\n| Mã | Nội dung |\n|---|---|\n| ABC-1 | a |\n| ABC-2 | b |\n\n'
            'Đoạn văn sau bảng.\n\n## Tiếp\n\nxyz\n')
    (tmp_path / 'Demo' / 'RE_D_S1B_Table.md').write_text(body, encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES)
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_S1B_Table.md').read_text(encoding='utf-8')
    assert s == ru.normalize(body) + '\n'


def test_cut_with_coded_row_between_items(tmp_path):
    body = ('## GT-D-001 — X\n\n1. **Tiêu đề:** a\n| ABC-1 | hàng |\n'
            '6. **KẾT QUẢ + khuyến nghị:** đã đo 3 mm\n| ABC-2 | hàng hai |\n'
            '7. **DỰ ĐOÁN VIẾT TRƯỚC:** BÍ_MẬT — người ký ___ — ngày ___\n\nĐuôi.\n\n## Sau\n\ntext\n')
    root = _hyp(tmp_path, body)
    m = rm.build_manifest({'Demo': root}, CLASSES)
    assert m['files']['Demo/RE_D_Hypotheses.md']['units']['GT-D-001.7']['cut'] is True
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_Hypotheses.md').read_text(encoding='utf-8')
    assert 'BÍ_MẬT' not in s and '⟨chờ ký⟩' in s and 'ABC-2' in s and 'đã đo 3 mm' in s
    assert 'Đuôi.' not in s and '## Sau' in s  # doan duoi thuoc muc 7, bi cat cung


def test_swap_failure_restores_old_snapshot(tmp_path, monkeypatch):
    root = make_dossier(tmp_path)
    book = tmp_path / 'Book'; book.mkdir()
    old = book / '_re_snapshot'; old.mkdir(); (old / 'keep.txt').write_text('cu', encoding='utf-8')
    real = os.replace

    def boom(src, dst, *a, **k):
        if str(src).endswith('.tmp') and str(dst).endswith('_re_snapshot'):
            raise OSError('swap hong')
        return real(src, dst, *a, **k)
    monkeypatch.setattr(rm.os, 'replace', boom)
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 2
    assert (old / 'keep.txt').read_text(encoding='utf-8') == 'cu'
    assert not (book / '_re_manifest.json').exists()
    assert not (book / '_re_snapshot.tmp').exists() and not (book / '_re_snapshot.old').exists()


# ---------------- Task 4: diff / gaps / index ----------------
import json  # noqa: E402
import shutil  # noqa: E402


def test_root_move_is_not_content_change(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    moved = tmp_path / 'X' / 'Demo'; moved.parent.mkdir(); shutil.move(root, moved)
    new = rm.build_manifest({'Demo': str(moved)}, CLASSES)
    d = rm.diff_manifests(old, new)
    assert d['root_moved'] == {'Demo': [root, str(moved)]}
    assert d['changed'] == d['added'] == d['removed'] == [] and d['compared_units'] > 0


def test_result_filled_reports_status_change(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    p = tmp_path / 'Demo' / 'RE_D_Hypotheses.md'
    p.write_text(p.read_text(encoding='utf-8').replace('*(điền sau)*', 'f = 3,1 — đạt'), encoding='utf-8')
    d = rm.diff_manifests(old, rm.build_manifest({'Demo': root}, CLASSES))
    assert 'Demo/RE_D_Hypotheses.md#GT-D-001.6' in d['changed']
    assert {'anchor': 'Demo/RE_D_Hypotheses.md#GT-D-001.6', 'from': 'chờ đo', 'to': 'đã đo'} in d['status_changes']


def test_prediction_signed_reports_status_change(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    p = tmp_path / 'Demo' / 'RE_D_Hypotheses.md'
    p.write_text(p.read_text(encoding='utf-8').replace('ngày ___', 'ngày 2026-10-01'), encoding='utf-8')
    d = rm.diff_manifests(old, rm.build_manifest({'Demo': root}, CLASSES))
    a = 'Demo/RE_D_Hypotheses.md#GT-D-001.7'
    assert a in d['changed']
    assert {'anchor': a, 'from': 'chờ ký', 'to': 'đã ký'} in d['status_changes']


def test_heading_rename_is_removed_plus_added(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    p = tmp_path / 'Demo' / 'RE_D_S1A_Deconstruction.md'
    p.write_text(p.read_text(encoding='utf-8').replace('## Khung', '## Khung đo'), encoding='utf-8')
    d = rm.diff_manifests(old, rm.build_manifest({'Demo': root}, CLASSES))
    assert 'Demo/RE_D_S1A_Deconstruction.md#Khung' in d['removed']
    assert 'Demo/RE_D_S1A_Deconstruction.md#Khung đo' in d['added']


def test_new_source_pdf_detected(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    (tmp_path / 'Demo' / '_source' / 'b.pdf').write_bytes(b'%PDF-new')
    assert 'Demo/_source/b.pdf' in rm.diff_manifests(old, rm.build_manifest({'Demo': root}, CLASSES))['sources_changed']


def test_class_change_counts_units_as_removed_and_added(tmp_path):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    new = json.loads(json.dumps(old))
    k = 'Demo/RE_D_S1A_Deconstruction.md'
    new['files'][k] = {'class': 'BLOCK', 'sha256': 'x', 'mtime': 0}
    d = rm.diff_manifests(old, new)
    assert k + '#Khung' in d['removed']
    d2 = rm.diff_manifests(new, old)
    assert k + '#Khung' in d2['added'] and k + '#Khung' not in d2['changed']


def test_no_changes_still_reports_compared_units(tmp_path):
    root = make_dossier(tmp_path); m = rm.build_manifest({'Demo': root}, CLASSES)
    d = rm.diff_manifests(m, m)
    assert d['compared_units'] > 0 and d['changed'] == d['added'] == d['removed'] == []
    assert d['status_changes'] == [] and d['sources_changed'] == [] and d['root_moved'] == {}
    assert rm.diff_manifests({'files': {}, 'roots': {}, 'sources': {}},
                             {'files': {}, 'roots': {}, 'sources': {}})['compared_units'] == 0


def test_cli_diff_exit_0_with_changes_and_prints_compared(tmp_path, capsys):
    root = make_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    (tmp_path / 'Demo' / '_source' / 'b.pdf').write_bytes(b'%PDF-new')
    new = rm.build_manifest({'Demo': root}, CLASSES)
    o, n, out = tmp_path / 'o.json', tmp_path / 'n.json', tmp_path / 'd.json'
    o.write_text(json.dumps(old), encoding='utf-8'); n.write_text(json.dumps(new), encoding='utf-8')
    assert rm.main(['diff', '--old', str(o), '--new', str(n), '--out', str(out)]) == 0
    assert 'compared_units' in capsys.readouterr().out
    assert json.loads(out.read_text(encoding='utf-8'))['sources_changed'] == ['Demo/_source/b.pdf']
    assert rm.main(['diff', '--old', str(o), '--new', str(tmp_path / 'none.json')]) == 2


def test_gaps_lists_precision_debt_rows(tmp_path):
    root = make_dossier(tmp_path); m = rm.build_manifest({'Demo': root}, CLASSES)
    assert 'Demo/RE_D_Precision_Debt.md#row:N-001' in rm.gaps(m, {'Demo': root})


def test_gaps_open_rows_stage_bo_status_and_missing_state(tmp_path):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_S1B_Notes.md').write_text(
        '# N\n\n| Mã | Nội dung |\n|---|---|\n| N-050 | còn mở |\n| N-051 | đã đóng |\n', encoding='utf-8')
    (tmp_path / 'Demo' / '_pipeline_state.md').write_text(
        '---\nconfidence_ceiling: M\n---\n## Stage Progress\n| Stage | Status |\n|---|---|\n'
        '| 3 | BỎ |\n| 4 | XONG |\n\n## Còn mở\n- status: chờ đo GT-D-001\n', encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES)
    g = rm.gaps(m, {'Demo': root})
    assert 'RE_D_S1B_Notes.md#row:N-050' in g and 'row:N-051' not in g
    assert '_pipeline_state.md#Stage Progress' in g and '| 3 | BỎ |' in g and '| 4 | XONG |' not in g
    assert '_pipeline_state.md#Còn mở' in g and 'status: chờ đo GT-D-001' in g
    (tmp_path / 'Demo' / '_pipeline_state.md').unlink()
    m2 = rm.build_manifest({'Demo': root}, CLASSES)
    assert '- (không có _pipeline_state.md) Demo' in rm.gaps(m2, {'Demo': root})


def test_index_uses_cho_ky_and_snapshot_excerpt(tmp_path):
    root = make_dossier(tmp_path); m = rm.build_manifest({'Demo': root}, CLASSES)
    snap = tmp_path / 'snap'; rm.write_snapshot(m, str(snap))
    t = rm.units_index(m, str(snap))
    assert '| Demo/RE_D_Hypotheses.md#GT-D-001.7 |' in t and '⟨chờ ký⟩' in t and 'Nguyễn A' not in t
    assert '⟨chờ đo⟩' in t
    assert 'RE_D_Idea_Log' not in t and '_pipeline_state' not in t
    assert 'phỏng đoán về khung' in t


def test_cli_gaps_and_index_write_files_and_missing_exit_2(tmp_path):
    root = make_dossier(tmp_path); book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['gaps', '--book', str(book)]) == 2
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    assert rm.main(['gaps', '--book', str(book)]) == 0
    assert rm.main(['index', '--book', str(book)]) == 0
    assert (book / 'Phase1-Exploration' / '_re_gaps.md').is_file()
    assert (book / 'Phase1-Exploration' / '_units_index.md').is_file()
    shutil.rmtree(book / '_re_snapshot')
    assert rm.main(['index', '--book', str(book)]) == 2


rp = _load('re_provenance')


def _prov(d, name, sections, chapter=None):
    d.mkdir(exist_ok=True)
    (d / (name + '.provenance.json')).write_text(
        json.dumps({'chapter': chapter or name, 'sections': sections}, ensure_ascii=False), encoding='utf-8')
    return d


def test_check_flags_dead_and_blocked_anchors(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    pd = _prov(tmp_path / 'p', 'Ch01', {'§01.1': [
        'Demo/RE_D_S1A_Deconstruction.md#Khung', 'Demo/RE_D_S1A_Deconstruction.md#Không có',
        'Demo/RE_D_Idea_Log.md#row:YT-001']})
    errs = rp.check(str(pd), m)
    assert len(errs) == 2 and any('Không có' in e for e in errs) and any('Idea_Log' in e for e in errs)


def test_check_accepts_valid_and_rejects_bad_file_and_input(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    ok = _prov(tmp_path / 'ok', 'Ch01', {'§01.1': ['Demo/RE_D_S1A_Deconstruction.md#Khung']})
    assert rp.check(str(ok), m) == []
    nofile = _prov(tmp_path / 'nf', 'Ch01', {'§01.1': ['Demo/nope.md#x']})
    assert len(rp.check(str(nofile), m)) == 1
    with pytest.raises(rp.InputError):
        rp.check(str(tmp_path / 'missing_dir'), m)
    (tmp_path / 'e').mkdir()
    with pytest.raises(rp.InputError):
        rp.check(str(tmp_path / 'e'), m)
    bad = tmp_path / 'bad'; bad.mkdir()
    (bad / 'Ch02.provenance.json').write_text('{oops', encoding='utf-8')
    with pytest.raises(rp.InputError, match='Ch02'):
        rp.check(str(bad), m)
    nos = tmp_path / 'nos'; nos.mkdir()
    (nos / 'Ch03.provenance.json').write_text('{"chapter": "Ch03"}', encoding='utf-8')
    with pytest.raises(rp.InputError, match='Ch03'):
        rp.check(str(nos), m)


def test_check_cli_exit_codes(tmp_path):
    book = tmp_path / 'Book'; book.mkdir()
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    (book / '_re_manifest.json').write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    good = _prov(tmp_path / 'g', 'Ch01', {'§01.1': ['Demo/RE_D_S1A_Deconstruction.md#Khung']})
    bad = _prov(tmp_path / 'b', 'Ch01', {'§01.1': ['Demo/RE_D_S1A_Deconstruction.md#Nope']})
    assert rp.main(['check', '--prov', str(good), '--book', str(book)]) == 0
    assert rp.main(['check', '--prov', str(bad), '--book', str(book)]) == 1
    (tmp_path / 'none').mkdir()
    assert rp.main(['check', '--prov', str(tmp_path / 'none'), '--book', str(book)]) == 2
    assert rp.main(['check', '--prov', str(good), '--book', str(tmp_path / 'nobook')]) == 2


def test_impact_maps_changed_unit_to_section_and_lists_unanchored(tmp_path):
    diff = {'changed': ['Demo/a.md#Khung'], 'added': ['Demo/a.md#Mới'], 'removed': [], 'status_changes': [],
            'root_moved': {}, 'sources_changed': [], 'compared_units': 3}
    pf = _prov(tmp_path / 'pf', 'Ch01', {'§01.1': ['Demo/a.md#Khung']})
    r = rp.impact(str(pf), diff)
    assert r['sections'] == {'Ch01': {'§01.1': ['Demo/a.md#Khung']}} and r['unanchored_new'] == ['Demo/a.md#Mới']


def test_impact_removed_status_and_root_moved(tmp_path):
    pf = _prov(tmp_path / 'pf', 'Ch02', {'§02.1': ['Demo/a.md#Cũ', 'Demo/a.md#S'], '§02.2': ['Demo/a.md#Cũ']})
    diff = {'changed': [], 'added': [], 'removed': ['Demo/a.md#Cũ'],
            'status_changes': [{'anchor': 'Demo/a.md#S', 'from': 'x', 'to': 'y'},
                               {'anchor': 'Demo/z.md#Q', 'from': 'x', 'to': 'y'}],
            'root_moved': {'Demo': ['a', 'b']}, 'sources_changed': [], 'compared_units': 1}
    r = rp.impact(str(pf), diff)
    assert r['sections'] == {'Ch02': {'§02.1': ['Demo/a.md#Cũ'], '§02.2': ['Demo/a.md#Cũ']}}
    assert r['status_changes'][0]['chapters'] == ['Ch02'] and r['status_changes'][1]['chapters'] == []
    assert r['unanchored_new'] == []


def test_impact_cli_writes_out_and_exit_2_on_missing(tmp_path):
    pf = _prov(tmp_path / 'pf', 'Ch01', {'§01.1': ['Demo/a.md#Khung']})
    dj = tmp_path / 'd.json'
    dj.write_text(json.dumps({'changed': ['Demo/a.md#Khung'], 'added': [], 'removed': [], 'status_changes': []}), encoding='utf-8')
    out = tmp_path / 'o' / 'imp.json'
    assert rp.main(['impact', '--prov', str(pf), '--diff', str(dj), '--out', str(out)]) == 0
    assert json.loads(out.read_text(encoding='utf-8'))['sections']['Ch01']
    assert rp.main(['impact', '--prov', str(pf), '--diff', str(tmp_path / 'x.json')]) == 2


def _p1_book(tmp_path):
    book = tmp_path / 'Book'; (book / 'Phase1-Exploration').mkdir(parents=True)
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    (book / '_re_manifest.json').write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    return book, book / 'Phase1-Exploration'


def test_check_p1_requires_anchor_per_exploration_file(tmp_path):
    book, p1 = _p1_book(tmp_path)
    (p1 / 'A_Exploration.md').write_text('# A\n\nkhông có neo nào\n', encoding='utf-8')
    assert rp.main(['check-p1', '--book', str(book)]) == 1
    m = json.loads((book / '_re_manifest.json').read_text(encoding='utf-8'))
    errs = rp.check_p1(str(p1), m)
    assert len(errs) == 1 and 'A_Exploration.md' in errs[0]


def test_check_p1_backticked_anchor_with_space_and_bare_anchor(tmp_path):
    book, p1 = _p1_book(tmp_path)
    d = tmp_path / 'Demo'
    (d / 'RE_D_S1A_Deconstruction.md').write_text(
        '# S1A\n\n## Khung\n\nx\n\n## Khung đo\n\ny\n', encoding='utf-8')
    m = rm.build_manifest({'Demo': str(d)}, CLASSES)
    (book / '_re_manifest.json').write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    (p1 / 'A_Exploration.md').write_text(
        'Xem `Demo/RE_D_S1A_Deconstruction.md#Khung đo` và Demo/RE_D_S1A_Deconstruction.md#Khung.\n', encoding='utf-8')
    (p1 / 'P1_Synthesis.md').write_text('Tổng hợp `Demo/RE_D_S1A_Deconstruction.md#Khung`\n', encoding='utf-8')
    assert rp.main(['check-p1', '--book', str(book)]) == 0
    (p1 / 'P1_Synthesis.md').write_text('sai `Demo/RE_D_S1A_Deconstruction.md#Không có`\n', encoding='utf-8')
    assert rp.main(['check-p1', '--book', str(book)]) == 1


def test_check_p1_no_exploration_files_is_input_error(tmp_path):
    book, p1 = _p1_book(tmp_path)
    (p1 / 'P1_Synthesis.md').write_text('x', encoding='utf-8')
    assert rp.main(['check-p1', '--book', str(book)]) == 2


def test_anchor_re_exported_exactly():
    assert rp.ANCHOR_RE.pattern == r'[\w.\-]+/[^\s#`|]+\.md#[^\s`|\]]+'
