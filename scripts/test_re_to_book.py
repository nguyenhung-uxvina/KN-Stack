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


def test_section_id_drops_backticks_so_anchor_can_be_quoted():
    us = ru.split_units('# T\n\n## Layer 2 — xem `RE_X_S1B.md`\n\nnoi dung\n')
    ids = [u.id for u in us]
    assert 'Layer 2 — xem RE_X_S1B.md' in ids and not any('`' in i for i in ids)


def test_row_code_with_trailing_note_in_code_cell():
    t = ('# N\n\n| Mã | Nội dung |\n|---|---|\n| N-008 | a |\n'
         '| N-009 ✅ ĐÃ TRẢ 2026-10-25 (hình) | b |\n')
    ids = [u.id for u in ru.split_units(t)]
    assert 'row:N-008' in ids and 'row:N-009' in ids


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


def test_dossier_scoped_pattern_targets_one_dossier_only(tmp_path):
    a = make_dossier(tmp_path / 'a'); b = make_dossier(tmp_path / 'b')
    for d in (a, b):
        with open(os.path.join(d, 'TECH_T1_Domain_Definition.md'), 'w', encoding='utf-8') as f:
            f.write('# T1\n\n## Mien\n\nx\n')
    import json
    with open(CLASSES, encoding='utf-8') as f:
        base = json.load(f)
    base['classes'].insert(0, {'class': 'IGNORE', 'patterns': ['Old/TECH_T1_*.md']})
    cp = tmp_path / 'proj_classes.json'; cp.write_text(json.dumps(base), encoding='utf-8')
    m = rm.build_manifest({'Old': a, 'New': b}, str(cp))
    assert 'Old/TECH_T1_Domain_Definition.md' not in m['files']
    assert 'Old/TECH_T1_Domain_Definition.md' in m['sources']
    assert m['files']['New/TECH_T1_Domain_Definition.md']['class'] == 'READ'
    assert rm.classify('TECH_T1_x.md', base['classes']) == 'READ'


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
    assert m['roots']['Demo'] == rm._norm_root(str(tmp_path / 'Demo'))
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
    assert d['root_moved'] == {'Demo': [rm._norm_root(root), rm._norm_root(str(moved))]}
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


# ---------- Task 6: re_book_audit ----------
ra = _load('re_book_audit')

_GT_M = {'files': {'Demo/RE_D_Hypotheses.md': {'class': 'CUT', 'units': {
    'GT-D-001.6': {'empty_result': True, 'cut': False}, 'GT-D-001.7': {'cut': True}}}}}


def test_gt_mention_without_pending_marker_flagged():
    m = _GT_M
    bad = {'Ch08': 'GT-D-001 cho thấy f giảm 3 lần.\n\nĐoạn khác.'}
    ok = {'Ch08': 'GT-D-001: kết quả ⟨chờ đo⟩.'}
    assert ra.gt_leaks(bad, m) and not ra.gt_leaks(ok, m)


def test_unsigned_prediction_mention_flagged():
    assert ra.gt_leaks({'Ch08': 'GT-D-001 ⟨chờ đo⟩; dự đoán 55 nấc.'}, _GT_M)
    assert not ra.gt_leaks({'Ch08': 'GT-D-001 ⟨chờ đo⟩; dự đoán 55 nấc ⟨chờ ký⟩.'}, _GT_M)


def test_gt_prefix_id_does_not_match():
    assert not any('chờ' in e for e in ra.gt_leaks({'Ch08': 'GT-D-0010 cho thấy f giảm.'}, _GT_M))


def test_conjecture_section_without_marker_flagged():
    m = {'files': {'Demo/a.md': {'class': 'READ', 'units': {'Khung': {'label': 'conjecture'}}}}}
    prov = {'Ch03': {'chapter': 'Ch03', 'sections': {'§03.2': ['Demo/a.md#Khung']}}}
    ch = {'Ch03': '## 03.2 Khung\nKhung rộng 730 mm.\n## 03.3 Khác\n⟨phỏng đoán⟩\n'}
    assert ra.label_gaps(ch, prov, m) == ['Ch03 §03.3: không có provenance',
                                          'Ch03 §03.2: thiếu ⟨phỏng đoán⟩ (Demo/a.md#Khung)']


def test_label_marker_prefix_accepted_and_missing_section_error():
    m = {'files': {'Demo/a.md': {'class': 'READ', 'units': {'Khung': {'label': 'conjecture'}}}}}
    prov = {'Ch03': {'chapter': 'Ch03', 'sections': {'§03.2': ['Demo/a.md#Khung']}}}
    assert ra.label_gaps({'Ch03': '## 03.2 Khung\nrộng ⟨phỏng đoán · M⟩\n'}, prov, m) == []
    errs = ra.label_gaps({'Ch03': '## 03.21 Khác\nx\n'}, prov, m)
    assert errs == ['Ch03 §03.21: không có provenance', 'Ch03 §03.2: không thấy mục trong chương']


def test_idea_coverage_requires_every_id_with_verdict():
    table = '| Mã | Chương | Kết luận |\n|---|---|---|\n| YT-001 | Ch08 | trùng |\n| YT-002 | — | |\n'
    errs = ra.idea_coverage(table, ['YT-001', 'YT-002', 'YT-003'])
    assert any('YT-002' in e for e in errs) and any('YT-003' in e for e in errs) and not any('YT-001' in e for e in errs)


def test_idea_coverage_column_order_and_bad_verdict():
    table = '| Kết luận | Mã |\n|---|---|\n| Không trùng | YT-001 |\n| có lẽ | YT-002 |\n'
    errs = ra.idea_coverage(table, ['YT-001', 'YT-002'])
    assert len(errs) == 1 and 'YT-002' in errs[0]


def test_idea_candidates_numeric_unit_overlap(tmp_path):
    root = make_dossier(tmp_path)
    out = ra.idea_candidates({'Ch08': 'Bộ lọc 890 nm với cửa sổ 20 nm.'}, {'Demo': root})
    assert 'YT-001' in out and 'Ch08' in out
    assert 'lọc 890 nm, cửa sổ' not in out


def _audit_book(tmp_path, chapter_text='## 01.1 Khung\nChương không nhắc gì ⟨phỏng đoán⟩.\n'):
    root = make_dossier(tmp_path)
    book = tmp_path / 'book'
    (book / 'Phase4-Chapters').mkdir(parents=True)
    (book / 'Phase4-Chapters' / 'Ch01.md').write_text(chapter_text, encoding='utf-8')
    (book / 'Phase4-Chapters' / 'Ch01.provenance.json').write_text(
        '{"chapter": "Ch01", "sections": {"§01.1": ["Demo/RE_D_S1A_Deconstruction.md#Khung"]}}', encoding='utf-8')
    m = rm.build_manifest({'Demo': root}, CLASSES)
    (book / '_re_manifest.json').write_text(json.dumps(m, ensure_ascii=False), encoding='utf-8')
    return root, book


def test_cli_no_idea_log_is_input_error(tmp_path):
    root, book = _audit_book(tmp_path)
    os.remove(os.path.join(root, 'RE_D_Idea_Log.md'))
    (book / 'Phase7-IdeaLog-Overlap.md').write_text('| Mã | Kết luận |\n|---|---|\n', encoding='utf-8')
    assert ra.main(['idea-coverage', '--book', str(book), '--re', root]) == 2
    assert ra.main(['all', '--book', str(book), '--re', root]) == 2


def test_cli_idea_candidates_preserves_verdict_table(tmp_path):
    root, book = _audit_book(tmp_path, '## 01.1 Khung\nBộ lọc 890 nm với cửa sổ 20 nm.\n')
    f = book / 'Phase7-IdeaLog-Overlap.md'
    f.write_text('# Overlap\n\n## Gợi ý từ vựng (không phải kết luận)\n\n- cũ\n\n## Kết luận\n\n'
                 '| Mã | Kết luận |\n|---|---|\n| YT-001 | trùng |\n', encoding='utf-8')
    assert ra.main(['idea-candidates', '--book', str(book), '--re', root]) == 0
    t = f.read_text(encoding='utf-8')
    assert '- cũ' not in t and 'YT-001 · Ch01' in t and '| YT-001 | trùng |' in t
    assert t.count('## Gợi ý từ vựng') == 1
    assert ra.main(['idea-coverage', '--book', str(book), '--re', root]) == 0
    f.unlink()
    assert ra.main(['idea-candidates', '--book', str(book), '--re', root]) == 0
    assert f.exists()


def test_cli_all_exit_is_max(tmp_path):
    root, book = _audit_book(tmp_path)
    f = book / 'Phase7-IdeaLog-Overlap.md'
    f.write_text('| Mã | Kết luận |\n|---|---|\n| YT-001 | không trùng |\n', encoding='utf-8')
    assert ra.main(['all', '--book', str(book), '--re', root]) == 0
    (book / 'Phase4-Chapters' / 'Ch01.md').write_text('GT-D-001 cho thấy gì đó.\n', encoding='utf-8')
    assert ra.main(['gt', '--book', str(book)]) == 1
    assert ra.main(['all', '--book', str(book), '--re', root]) == 1
    f.unlink()
    assert ra.main(['all', '--book', str(book), '--re', root]) == 2


def test_gt_unknown_id_flagged_and_summary():
    assert ra.gt_summary(_GT_M) == (1, 1, 1)
    errs = ra.gt_leaks({'Ch08': 'GT-X-9 cho thấy gì đó.'}, _GT_M)
    assert errs == ['Ch08 đoạn 1: GT-X-9 không có trong manifest']
    assert ra.gt_summary({'files': {}}) == (0, 0, 0)
    assert ra.gt_leaks({'Ch08': 'không nhắc'}, {'files': {}}) == []


def test_cli_gt_prints_count_line(tmp_path, capsys):
    root, book = _audit_book(tmp_path)
    assert ra.main(['gt', '--book', str(book)]) == 0
    assert 'kiểm 1 phiếu GT (1 chờ đo, 1 chờ ký)' in capsys.readouterr().out


def test_gt_prefix_id_not_matched_as_known_card():
    errs = ra.gt_leaks({'Ch08': 'GT-D-0010 cho thấy f giảm.'}, _GT_M)
    assert errs == ['Ch08 đoạn 1: GT-D-0010 không có trong manifest']


def test_chapter_without_provenance_flagged():
    m = {'files': {}}
    prov = {'Ch01': {'chapter': 'Ch01', 'sections': {}}}
    assert ra.label_gaps({'Ch01': 'x', 'Ch02': 'y'}, prov, m) == ['Ch02: không có provenance']


def test_candidate_section_end_rule_consistent():
    NL = chr(10)
    tbl = '| Mã | Kết luận |' + NL + '|---|---|' + NL
    t = (NL.join(['# Overlap', '', '## Gợi ý từ vựng (không phải kết luận)', '', '### Phụ', ''])
         + NL + tbl + '| YT-001 | trùng |' + NL + NL + '## Kết luận' + NL + NL + tbl + '| YT-002 | trùng |' + NL)
    assert ra.idea_coverage(t, ['YT-001']) != []
    assert ra.idea_coverage(t, ['YT-002']) == []
    out = ra._merge_candidates(t, '- moi' + NL)
    assert '- moi' in out and 'YT-001' not in out and '| YT-002 | trùng |' in out


rr = _load('re_nlm_redact')


def test_redact_codes_longest_first_and_boundaries():
    codes = ['RE_3DS_Hypotheses', 'GT-3DS-001', 'N-013']
    t, n = rr.redact('Xem RE_3DS_Hypotheses.md, GT-3DS-001 và N-013; không đụng N-0130 hay ABN-013.', codes)
    assert n == 3 and 'RE_3DS' not in t and 'N-0130' in t and 'ABN-013' in t


def test_redact_anchor_with_space_in_backticks_fully_removed():
    t, n = rr.redact('Nguồn `Demo/RE_D_Hypotheses.md#Góc nhận` và Demo/RE_D_Idea_Log.md#YT-1.', [])
    assert 'Demo/' not in t and 'RE_D' not in t and '`' not in t
    assert t.count('phân tích nội bộ') == 2 and n == 2 and t.endswith('.')


def test_redact_gt_id_consumes_item_suffix():
    t, n = rr.redact('GT-D-001.7~2 và GT-D-001.', ['GT-D-001'])
    assert t == 'phân tích nội bộ và phân tích nội bộ.' and n == 2


def _book(tmp_path, chunk_text):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    book = tmp_path / 'Book'; book.mkdir()
    import json
    (book / '_re_manifest.json').write_text(json.dumps(m), encoding='utf-8')
    src = tmp_path / 'chunks'; src.mkdir()
    (src / 'c1.md').write_text(chunk_text, encoding='utf-8')
    return m, str(book), str(src)


def test_codes_include_block_file_stem_rows_and_gt_ids(tmp_path):
    m, _, _ = _book(tmp_path, 'x')
    codes = rr.codes_from_manifest(m)
    assert 'RE_D_Idea_Log' in codes and 'N-001' in codes and 'GT-D-001' in codes
    assert codes == sorted(set(codes), key=lambda c: (-len(c), c))


def test_cli_clean_run(tmp_path):
    _, book, src = _book(tmp_path, 'Xem RE_D_Hypotheses.md, GT-D-001.7 và N-001 `Demo/RE_D_Precision_Debt.md#row:N-001`.\n')
    out = str(tmp_path / 'out')
    assert rr.main(['--book', book, '--src', src, '--out', out]) == 0
    t = open(os.path.join(out, 'c1.md'), encoding='utf-8').read()
    assert 'RE_D' not in t and 'N-001' not in t and 'GT-D-001' not in t and 'phân tích nội bộ' in t
    assert 'RE_D' in open(os.path.join(src, 'c1.md'), encoding='utf-8').read()


def test_cli_rescan_fails_if_code_survives(tmp_path, monkeypatch):
    _, book, src = _book(tmp_path, 'Có N-001 ở đây.\n')
    monkeypatch.setattr(rr, 'redact', lambda text, codes: (text, 0))
    assert rr.main(['--book', book, '--src', src, '--out', str(tmp_path / 'out')]) == 1


def test_cli_out_inside_src_or_book_is_2(tmp_path):
    _, book, src = _book(tmp_path, 'x\n')
    assert rr.main(['--book', book, '--src', src, '--out', os.path.join(src, 'o')]) == 2
    assert rr.main(['--book', book, '--src', src, '--out', book]) == 2
    assert rr.main(['--book', book, '--src', src, '--out', src]) == 2


def test_cli_missing_manifest_or_empty_src_is_2(tmp_path):
    _, book, src = _book(tmp_path, 'x\n')
    os.remove(os.path.join(src, 'c1.md'))
    assert rr.main(['--book', book, '--src', src, '--out', str(tmp_path / 'o')]) == 2
    assert rr.main(['--book', str(tmp_path / 'none'), '--src', src, '--out', str(tmp_path / 'o')]) == 2


def test_cli_failed_rescan_leaves_out_absent_even_if_previous_existed(tmp_path, monkeypatch):
    _, book, src = _book(tmp_path, 'Có N-001 ở đây.\n')
    out = tmp_path / 'out'; out.mkdir(); (out / 'old.md').write_text('sạch', encoding='utf-8')
    monkeypatch.setattr(rr, 'redact', lambda text, codes: (text, 0))
    assert rr.main(['--book', book, '--src', src, '--out', str(out)]) == 1
    assert not out.exists() and not (tmp_path / 'out.tmp').exists()


def test_cli_hyphen_prefixed_code_is_reported(tmp_path):
    _, book, src = _book(tmp_path, 'mã x-GT-D-001 sót\n')
    out = tmp_path / 'out'
    assert rr.main(['--book', book, '--src', src, '--out', str(out)]) == 1
    assert not out.exists()


def test_cli_nfd_chunk_is_normalised_before_redaction(tmp_path):
    import unicodedata
    _, book, src = _book(tmp_path, unicodedata.normalize('NFD', 'Phân tích N-001 ở đây\n'))
    out = tmp_path / 'out'
    assert rr.main(['--book', book, '--src', src, '--out', str(out)]) == 0
    t = (out / 'c1.md').read_text(encoding='utf-8')
    assert 'N-001' not in t and unicodedata.is_normalized('NFC', t)


# ---------------------------------------------------------------- re_consolidate (P0)
rc = _load('re_consolidate')


_WIN_STATUS = r'xem D:\W\1_Projects\BB-02_LOMAH\RE\Demo\a.md' + '\nvà RE/Demo/a.md\n'


def _vault(tmp_path, status=_WIN_STATUS):
    proj = tmp_path / 'BB-02_LOMAH'
    d = proj / 'RE' / 'Demo'
    d.mkdir(parents=True)
    (d / 'a.md').write_text('x', encoding='utf-8')
    (d / '_pipeline_state.md').write_text('---\nproject: BB-02_LOMAH\nx: 1\n---\nbody\n', encoding='utf-8')
    (proj / 'Status.md').write_bytes(status.encode('utf-8'))
    return proj, tmp_path / 'RE-X' / 'RE'


def _plan(proj, dest, dossiers=('Demo',)):
    return rc.plan(str(proj / 'RE'), list(dossiers), str(dest), [str(proj)], 'BB-02_LOMAH', 'RE-X')


def test_plan_splits_auto_and_manual_refs(tmp_path):
    proj = tmp_path / 'BB-02_LOMAH'
    (proj / 'RE' / 'Demo').mkdir(parents=True)
    (proj / 'RE' / 'Demo' / 'a.md').write_text('x', encoding='utf-8')
    (proj / 'Status.md').write_text(_WIN_STATUS, encoding='utf-8')
    p = rc.plan(str(proj / 'RE'), ['Demo'], str(tmp_path / 'RE-X' / 'RE'), [str(proj)], 'BB-02_LOMAH', 'RE-X')
    assert p['auto_rewrites'][0]['new'].endswith(r'RE-X\RE\Demo\a.md') and p['manual'][0]['line'] == 2
    assert p['moves'][0]['file_count'] == 1


def test_plan_prefix_dossier_not_matched(tmp_path):
    proj, dest = _vault(tmp_path, 'BB-02_LOMAH/RE/Demo2/x\nRE/Demo2/y\n')
    p = _plan(proj, dest)
    assert p['auto_rewrites'] == [] and p['manual'] == []


def test_apply_moves_counts_rewrites_only_approved_and_writes_readme(tmp_path):
    proj, dest = _vault(tmp_path)
    st = proj / 'Status.md'
    p = _plan(proj, dest)
    r = rc.apply(p, [str(st)])
    assert (dest / 'Demo' / 'a.md').read_text(encoding='utf-8') == 'x'
    assert not (proj / 'RE' / 'Demo').exists()
    lines = st.read_text(encoding='utf-8').splitlines()
    assert lines[0] == r'xem D:\W\1_Projects\RE-X\RE\Demo\a.md' and lines[1] == 'và RE/Demo/a.md'
    assert 'project: RE-X' in (dest / 'Demo' / '_pipeline_state.md').read_text(encoding='utf-8')
    readme = proj / 'RE' / 'README.md'
    assert os.path.exists(r['readme']) and 'Demo' in readme.read_text(encoding='utf-8')
    assert r['moved'] and r['rewritten']


def test_apply_unapproved_file_untouched(tmp_path):
    proj, dest = _vault(tmp_path)
    before = (proj / 'Status.md').read_bytes()
    r = rc.apply(_plan(proj, dest), [])
    assert (proj / 'Status.md').read_bytes() == before and r['rewritten'] == []


def test_apply_refuses_symlinked_src(tmp_path):
    proj, dest = _vault(tmp_path)
    link = tmp_path / 'link_RE'
    try:
        os.symlink(str(proj / 'RE'), str(link), target_is_directory=True)
    except (OSError, NotImplementedError):
        pytest.skip('khong tao duoc symlink')
    p = _plan(proj, dest)
    p['src_root'] = str(link)
    with pytest.raises(rc.RefusedError):
        rc.apply(p, [])
    assert (proj / 'RE' / 'Demo' / 'a.md').exists() and not dest.exists()


def test_apply_refuses_junction_src(tmp_path, monkeypatch):
    proj, dest = _vault(tmp_path)
    p = _plan(proj, dest)
    src = os.path.abspath(str(proj / 'RE'))
    monkeypatch.setattr(os.path, 'isjunction',
                        lambda x: os.path.abspath(x) == src, raising=False)
    with pytest.raises(rc.RefusedError):
        rc.apply(p, [])
    assert (proj / 'RE' / 'Demo' / 'a.md').exists() and not dest.exists()


def test_apply_refuses_existing_destination(tmp_path):
    proj, dest = _vault(tmp_path)
    (dest / 'Demo').mkdir(parents=True)
    with pytest.raises(rc.RefusedError):
        rc.apply(_plan(proj, dest), [])
    assert (proj / 'RE' / 'Demo' / 'a.md').exists()


def test_apply_stale_plan_raises_before_move(tmp_path):
    proj, dest = _vault(tmp_path)
    st = proj / 'Status.md'
    p = _plan(proj, dest)
    st.write_text('da sua\n', encoding='utf-8')
    with pytest.raises(rc.StalePlanError):
        rc.apply(p, [str(st)])
    assert (proj / 'RE' / 'Demo' / 'a.md').exists() and not dest.exists()


def test_apply_crlf_preserved(tmp_path):
    proj, dest = _vault(tmp_path, 'a BB-02_LOMAH/RE/Demo/x\r\nlast\r\n')
    st = proj / 'Status.md'
    rc.apply(_plan(proj, dest), [str(st)])
    assert st.read_bytes() == 'a RE-X/RE/Demo/x\r\nlast\r\n'.encode('utf-8')


def test_apply_readme_appended_when_present(tmp_path):
    proj, dest = _vault(tmp_path)
    (proj / 'RE' / 'README.md').write_text('# Cu\n', encoding='utf-8')
    rc.apply(_plan(proj, dest), [])
    t = (proj / 'RE' / 'README.md').read_text(encoding='utf-8')
    assert t.startswith('# Cu\n') and 'Demo' in t


def test_cli_plan_creates_missing_out_parent(tmp_path):
    proj, dest = _vault(tmp_path)
    out = tmp_path / 'Book' / '_p0' / 'plan.json'
    assert not out.parent.exists()
    assert rc.main(['plan', '--src-root', str(proj / 'RE'), '--dossiers', 'Demo',
                    '--dest-root', str(dest), '--scan', str(proj),
                    '--old-project', 'BB-02_LOMAH', '--new-project', 'RE-X',
                    '--out', str(out)]) == 0
    assert out.is_file() and not dest.exists()


def test_cli_apply_requires_approve_flag(tmp_path):
    proj, dest = _vault(tmp_path)
    out = tmp_path / 'plan.json'
    assert rc.main(['plan', '--src-root', str(proj / 'RE'), '--dossiers', 'Demo',
                    '--dest-root', str(dest), '--scan', str(proj),
                    '--old-project', 'BB-02_LOMAH', '--new-project', 'RE-X',
                    '--out', str(out)]) == 0
    assert not dest.exists()
    assert rc.main(['apply', '--plan', str(out)]) == 2
    assert (proj / 'RE' / 'Demo').exists()
    assert rc.main(['apply', '--plan', str(out), '--no-rewrite']) == 0
    assert (dest / 'Demo' / 'a.md').exists()


def _vault2(tmp_path):
    proj, dest = _vault(tmp_path)
    d2 = proj / 'RE' / 'Other'
    d2.mkdir()
    (d2 / 'b.md').write_text('y', encoding='utf-8')
    return proj, dest


def _save(tmp_path, p):
    f = tmp_path / 'p2.json'
    f.write_text(json.dumps(p), encoding='utf-8')
    return str(f)


def test_plan_mixed_line_lists_bare_as_manual(tmp_path):
    proj, dest = _vault(tmp_path, 'BB-02_LOMAH/RE/Demo/a.md et RE/Demo/b.md\n')
    p = _plan(proj, dest)
    assert len(p['auto_rewrites']) == 1 and len(p['manual']) == 1 and p['manual'][0]['line'] == 1


def test_partial_move_reports_moved_and_failed(tmp_path, monkeypatch):
    proj, dest = _vault2(tmp_path)
    p = _plan(proj, dest, ('Demo', 'Other'))
    real = os.rename

    def fake(a, b, *x, **k):
        if os.path.basename(a) == 'Other':
            raise OSError('khoa tep')
        return real(a, b, *x, **k)
    monkeypatch.setattr(os, 'rename', fake)
    with pytest.raises(rc.PartialMoveError) as e:
        rc.apply(p, [])
    msg = str(e.value)
    assert 'Demo' in msg and 'Other' in msg and 'khoa tep' in msg
    assert not (proj / 'RE' / 'README.md').exists()


def test_cli_partial_move_prints_message_exit2(tmp_path, monkeypatch, capsys):
    proj, dest = _vault2(tmp_path)
    p = _plan(proj, dest, ('Demo', 'Other'))
    real = os.rename

    def fake(a, b, *x, **k):
        if os.path.basename(a) == 'Other':
            raise OSError('hong')
        return real(a, b, *x, **k)
    monkeypatch.setattr(os, 'rename', fake)
    assert rc.main(['apply', '--plan', _save(tmp_path, p), '--no-rewrite']) == 2
    err = capsys.readouterr().err
    assert 'PartialMoveError' in err and 'Demo' in err and 'Other' in err


def test_nested_link_refused_nothing_moved(tmp_path, monkeypatch):
    proj, dest = _vault(tmp_path)
    sub = proj / 'RE' / 'Demo' / 'sub'
    sub.mkdir()
    (sub / 'z.md').write_text('z', encoding='utf-8')
    target = os.path.abspath(str(sub))
    monkeypatch.setattr(os.path, 'isjunction', lambda x: os.path.abspath(x) == target, raising=False)
    p = _plan(proj, dest)
    assert p['nested_links']
    with pytest.raises(rc.RefusedError):
        rc.apply(p, [])
    assert (proj / 'RE' / 'Demo' / 'a.md').exists() and not dest.exists()


# ================================================================ final fix wave
# ---------- C1: phieu GT dang bang ----------
TABLE_HYP = (
    '# Phiếu trung tính\n\n'
    '## GT-T-001 — Bàn thử trung tính\n\n'
    '| # | Mục | Nội dung |\n|---|---|---|\n'
    '| 1 | Tiêu đề | Một câu hỏi trung tính |\n'
    '| 2 | **NẾU** | điều kiện A |\n'
    '| 3 | **THÌ** | hệ quả B |\n'
    '| 4 | **VÌ** | lý do C |\n'
    '| 5 | KIỂM | quy trình D |\n'
    '| 6 | KẾT QUẢ | *(điền sau buổi thử)* |\n'
    '| 7 | **DỰ ĐOÁN VIẾT TRƯỚC** | giá trị XA — người ký: ____ — ngày: ____ |\n'
    '| 8 | Độ tin | trung bình |\n'
    '| 9 | Nếu bị bác | quay lại |\n\n'
    '**Đối chứng dương:** đoạn văn sau bảng.\n\n'
    '## GT-T-002 — Phiếu dạng danh sách\n\n'
    '1. **Tiêu đề:** a\n'
    '6. **KẾT QUẢ + khuyến nghị:** *(điền sau 2026-11-04)*\n'
    '7. **DỰ ĐOÁN VIẾT TRƯỚC:** giá trị XB — người ký ___ — ngày ___\n\n'
    '## GT-T-003 — Bảng hai\n\n'
    '| # | Mục | Nội dung |\n|---|---|---|\n'
    '| 6 | **KẾT QUẢ** | *(điền sau khi thử)* |\n'
    '| **7** | **DỰ ĐOÁN VIẾT TRƯỚC** | giá trị XC — người ký: ____ — ngày: ____ *(ghi chú)* |\n\n'
    '## Tham chiếu\n\nx\n')


def _table_dossier(tmp_path, text=TABLE_HYP):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_Hypotheses.md').write_text(text, encoding='utf-8')
    return root


def test_table_gt_rows_are_items_and_ids_agree_with_spans():
    ids = [u.id for u in ru.split_units(TABLE_HYP)]
    for n in range(1, 10):
        assert 'GT-T-001.%d' % n in ids
    assert 'GT-T-003.6' in ids and 'GT-T-003.7' in ids and 'GT-T-002.7' in ids
    lines = ru.normalize(TABLE_HYP).split('\n')
    span_ids = [uid for _s, _e, uid in rm._item_spans(lines)]
    assert span_ids == [i for i in ids if i.startswith('GT-') and not i.endswith('.0')]


def test_table_gt_duplicate_row_numbering_matches():
    t = ('## GT-T-009 — x\n\n| # | Mục | Nội dung |\n|---|---|---|\n'
         '| 7 | DỰ ĐOÁN VIẾT TRƯỚC | a — người ký: ____ — ngày: ____ |\n'
         '| 7 | DỰ ĐOÁN VIẾT TRƯỚC | b — người ký: ____ — ngày: ____ |\n')
    ids = [u.id for u in ru.split_units(t)]
    assert 'GT-T-009.7' in ids and 'GT-T-009.7~2' in ids
    assert [x for _s, _e, x in rm._item_spans(ru.normalize(t).split('\n'))] == ['GT-T-009.7', 'GT-T-009.7~2']


def test_table_unsigned_prediction_never_reaches_snapshot(tmp_path):
    root = _table_dossier(tmp_path)
    m = rm.build_manifest({'Demo': root}, CLASSES)
    u = m['files']['Demo/RE_D_Hypotheses.md']['units']
    for card in ('GT-T-001', 'GT-T-002', 'GT-T-003'):
        assert u[card + '.7']['cut'] is True, card
        assert u[card + '.6'].get('empty_result') is True, card
    out = tmp_path / 'snap'; rm.write_snapshot(m, str(out))
    s = (out / 'Demo' / 'RE_D_Hypotheses.md').read_text(encoding='utf-8')
    assert 'XA' not in s and 'XB' not in s and 'XC' not in s
    assert s.count('| 7 | DỰ ĐOÁN VIẾT TRƯỚC | ⟨chờ ký⟩ |') == 2
    assert s.count('| 6 | KẾT QUẢ | ⟨chờ đo⟩ |') == 2
    assert '| 8 | Độ tin | trung bình |' in s and 'Đối chứng dương' in s


def test_table_marker_keeps_column_count():
    u = ru.Unit(id='GT-T-001.7', kind='gt_item',
                text='| 7 | DỰ ĐOÁN VIẾT TRƯỚC | x | y |', sha256='')
    assert rm._marker(u, '7') == '| 7 | DỰ ĐOÁN VIẾT TRƯỚC | ⟨chờ ký⟩ |  |'
    u6 = ru.Unit(id='GT-T-001.6', kind='gt_item', text='| 6 | KẾT QUẢ | *(điền sau)* |', sha256='')
    assert rm._marker(u6, '6') == '| 6 | KẾT QUẢ | ⟨chờ đo⟩ |'


def test_table_signed_prediction_kept_and_filled_result_kept(tmp_path):
    t = TABLE_HYP.replace('XA — người ký: ____ — ngày: ____', 'XA — người ký: Kỹ sư B — ngày: 01/11')
    t = t.replace('| 6 | KẾT QUẢ | *(điền sau buổi thử)* |', '| 6 | KẾT QUẢ | đạt, 3 nấc |')
    m = rm.build_manifest({'Demo': _table_dossier(tmp_path, t)}, CLASSES)
    u = m['files']['Demo/RE_D_Hypotheses.md']['units']
    assert u['GT-T-001.7']['cut'] is False and not u['GT-T-001.6'].get('empty_result')


def test_table_empty_variants_underscore_dash():
    for cell in ('*(điền sau)*', '___', '—', '', '*(điền sau 2026-11-04)*'):
        assert rm._result_empty('| 6 | KẾT QUẢ | %s |' % cell), cell
    assert not rm._result_empty('| 6 | KẾT QUẢ | đạt |')
    assert rm._result_empty('6. **KẾT QUẢ + khuyến nghị:** *(điền sau 2026-11-04)*')


def test_gt_counts_mixed_list_and_table_cards(tmp_path):
    m = rm.build_manifest({'Demo': _table_dossier(tmp_path)}, CLASSES)
    assert ra.gt_summary(m) == (3, 3, 3)


def test_chapter_stating_result_of_empty_table_card_flagged(tmp_path):
    m = rm.build_manifest({'Demo': _table_dossier(tmp_path)}, CLASSES)
    errs = ra.gt_leaks({'Ch05': 'GT-T-001 cho thấy phân biệt được 3 nấc.'}, m)
    assert any('GT-T-001' in e and 'chờ đo' in e for e in errs)
    assert ra.gt_leaks({'Ch05': 'GT-T-001: kết quả ⟨chờ đo⟩.'}, m) == []


def test_filling_table_row6_reports_status_change(tmp_path):
    root = _table_dossier(tmp_path); old = rm.build_manifest({'Demo': root}, CLASSES)
    p = tmp_path / 'Demo' / 'RE_D_Hypotheses.md'
    p.write_text(TABLE_HYP.replace('*(điền sau buổi thử)*', 'đạt — phân biệt 3 nấc'), encoding='utf-8')
    d = rm.diff_manifests(old, rm.build_manifest({'Demo': root}, CLASSES))
    assert {'anchor': 'Demo/RE_D_Hypotheses.md#GT-T-001.6', 'from': 'chờ đo', 'to': 'đã đo'} in d['status_changes']


# ---------- I1: provenance rong ----------
def test_check_empty_sections_or_empty_list_flagged(tmp_path):
    m = rm.build_manifest({'Demo': make_dossier(tmp_path)}, CLASSES)
    e1 = _prov(tmp_path / 'e1', 'Ch01', {})
    assert rp.check(str(e1), m) == ['Ch01.provenance.json: không có neo']
    e2 = _prov(tmp_path / 'e2', 'Ch01', {'§01.1': ['Demo/RE_D_S1A_Deconstruction.md#Khung'], '§01.2': []})
    assert rp.check(str(e2), m) == ['Ch01.provenance.json:§01.2: không có neo']


def test_label_gaps_numbered_heading_without_provenance_entry():
    m = {'files': {}}
    prov = {'Ch04': {'chapter': 'Ch04', 'sections': {'§04.1': []}}}
    ch = {'Ch04': '# 4 Tên\n## 04.1 A\nx\n### 04.2 B\ny\n```\n## 04.9 trong rào\n```\n'}
    assert ra.label_gaps(ch, prov, m) == ['Ch04 §04.2: không có provenance']


# ---------- I2: phieu GT tran phong doan ----------
def test_gt_item_capped_at_conjecture():
    u = ru.Unit(id='GT-T-001.4', kind='gt_item', text='VÌ: đã biết từ sáng chế', sha256='')
    l = rl.resolve(u, None, None)
    assert (l.label, l.source) == ('conjecture', 'kế thừa: phiếu GT')
    u0 = ru.Unit(id='GT-T-001.0', kind='gt_item', text='## GT-T-001 — x', sha256='')
    assert rl.resolve(u0, None, None).label == 'conjecture'
    ua = ru.Unit(id='GT-T-001.2', kind='gt_item', text='giả định: tải đều', sha256='')
    assert rl.resolve(ua, None, None).label == 'assumption'


def test_manifest_gt_units_never_knowledge(tmp_path):
    m = rm.build_manifest({'Demo': _table_dossier(tmp_path)}, CLASSES)
    for uid, rec in m['files']['Demo/RE_D_Hypotheses.md']['units'].items():
        if uid.startswith('GT-'):
            assert rec['label'] in ('conjecture', 'assumption'), uid


# ---------- I3: chua gan ----------
_UA_M = {'files': {'Demo/a.md': {'class': 'READ', 'units': {'Khung': {'label': 'chưa gán'}}}}}
_UA_P = {'Ch03': {'chapter': 'Ch03', 'sections': {'§03.2': ['Demo/a.md#Khung']}}}


def test_unassigned_anchor_needs_marker_or_decision():
    bare = {'Ch03': '## 03.2 Khung\nKhung rộng.\n'}
    assert ra.label_gaps(bare, _UA_P, _UA_M) == ['Ch03 §03.2: thiếu ⟨chưa gán nhãn⟩ (Demo/a.md#Khung)']
    marked = {'Ch03': '## 03.2 Khung\nKhung rộng ⟨chưa gán nhãn⟩.\n'}
    assert ra.label_gaps(marked, _UA_P, _UA_M) == []
    assert ra.label_gaps(bare, _UA_P, _UA_M, {'Demo/a.md#Khung': 'knowledge'}) == []
    assert ra.label_gaps(bare, _UA_P, _UA_M, {'Demo/a.md#Khung': 'conjecture'}) == [
        'Ch03 §03.2: thiếu ⟨phỏng đoán⟩ (Demo/a.md#Khung)']


def test_label_decisions_file_parsed_and_used_by_cli(tmp_path):
    root, book = _audit_book(tmp_path, '## 01.1 Khung\nKhung rộng.\n')
    man = json.loads((book / '_re_manifest.json').read_text(encoding='utf-8'))
    man['files']['Demo/RE_D_S1A_Deconstruction.md']['units']['Khung']['label'] = 'chưa gán'
    (book / '_re_manifest.json').write_text(json.dumps(man, ensure_ascii=False), encoding='utf-8')
    assert ra.main(['labels', '--book', str(book)]) == 1
    p1 = book / 'Phase1-Exploration'; p1.mkdir()
    (p1 / '_label_decisions.md').write_text(
        '| neo | nhãn |\n|---|---|\n| `Demo/RE_D_S1A_Deconstruction.md#Khung` | knowledge |\n', encoding='utf-8')
    assert ra.load_label_decisions(str(book)) == {'Demo/RE_D_S1A_Deconstruction.md#Khung': 'knowledge'}
    assert ra.main(['labels', '--book', str(book)]) == 0


def test_index_prints_unassigned_count(tmp_path, capsys):
    root = make_dossier(tmp_path); book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    capsys.readouterr()
    assert rm.main(['index', '--book', str(book)]) == 0
    m = json.loads((book / '_re_manifest.json').read_text(encoding='utf-8'))
    units = [r for e in m['files'].values() if e['class'] in ('READ', 'CUT') for r in e['units'].values()]
    n = sum(r['label'] == 'chưa gán' for r in units)
    assert 'chưa gán: %d / tổng %d' % (n, len(units)) in capsys.readouterr().out


# ---------- I4: gaps hang mo ----------
def test_gaps_open_rows_case_and_status_column(tmp_path):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_S1B_Notes.md').write_text(
        '# N\n\n| Mã | Nội dung | Trạng thái |\n|---|---|---|\n'
        '| N-060 | việc A | MỞ |\n'
        '| N-061 | mở rộng phạm vi | BÃI BỎ |\n'
        '| N-062 | mở rộng khung | đã đóng |\n'
        '| N-063 | việc B | Mở — chờ thử |\n'
        '| N-064 | việc C | ĐÃ TRẢ (mở lại?) |\n', encoding='utf-8')
    g = rm.gaps(rm.build_manifest({'Demo': root}, CLASSES), {'Demo': root})
    assert 'row:N-060' in g and 'row:N-063' in g
    assert 'row:N-061' not in g and 'row:N-062' not in g and 'row:N-064' not in g


def test_gaps_whole_row_when_no_status_column_ci(tmp_path):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_S1B_Notes.md').write_text(
        '# N\n\n| Mã | Nội dung |\n|---|---|\n| N-070 | CÒN MỞ |\n| N-071 | BÃI BỎ — mở rộng |\n', encoding='utf-8')
    g = rm.gaps(rm.build_manifest({'Demo': root}, CLASSES), {'Demo': root})
    assert 'row:N-070' in g and 'row:N-071' not in g


# ---------- I5: lock / freeze ----------
def _built_book(tmp_path):
    root = make_dossier(tmp_path); book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    return root, book


def test_freeze_without_lock_is_2_and_with_lock_copies(tmp_path):
    root, book = _built_book(tmp_path)
    assert rm.main(['freeze', '--book', str(book), '--edition', '1']) == 2
    assert rm.main(['lock', '--book', str(book)]) == 0
    lock = json.loads((book / '_manifests' / '_p1_lock.json').read_text(encoding='utf-8'))
    m = json.loads((book / '_re_manifest.json').read_text(encoding='utf-8'))
    assert lock['created'] == m['created'] and len(lock['sha256']) == 64
    assert rm.main(['freeze', '--book', str(book), '--edition', '1']) == 0
    assert (book / '_manifests' / 'ed1.json').read_bytes() == (book / '_re_manifest.json').read_bytes()
    assert rm.main(['freeze', '--book', str(book), '--edition', '1']) == 2


def test_freeze_refuses_manifest_rebuilt_after_lock(tmp_path, capsys):
    root, book = _built_book(tmp_path)
    assert rm.main(['lock', '--book', str(book)]) == 0
    p = tmp_path / 'Demo' / 'RE_D_S1A_Deconstruction.md'
    p.write_text(p.read_text(encoding='utf-8') + '\nthêm\n', encoding='utf-8')
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    capsys.readouterr()
    assert rm.main(['freeze', '--book', str(book), '--edition', '1']) == 1
    assert 'P1' in capsys.readouterr().err
    assert not (book / '_manifests' / 'ed1.json').exists()


def test_lock_without_manifest_is_2(tmp_path):
    book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['lock', '--book', str(book)]) == 2


# ---------- Minors ----------
def test_impact_writes_out_before_printing(tmp_path, monkeypatch):
    pf = _prov(tmp_path / 'pf', 'Ch01', {'§01.1': ['Demo/a.md#Khung']})
    dj = tmp_path / 'd.json'
    dj.write_text(json.dumps({'changed': ['Demo/a.md#Khung'], 'added': [], 'removed': [], 'status_changes': []}), encoding='utf-8')
    out = tmp_path / 'imp.json'

    def boom(_r):
        assert out.exists()
        raise UnicodeEncodeError('cp1252', '', 0, 1, 'x')
    monkeypatch.setattr(rp, '_report', boom)
    rp.main(['impact', '--prov', str(pf), '--diff', str(dj), '--out', str(out)])
    assert out.exists() and json.loads(out.read_text(encoding='utf-8'))['sections']['Ch01']


def test_root_spelling_variants_not_moved(tmp_path):
    root = make_dossier(tmp_path)
    a = rm.build_manifest({'Demo': root}, CLASSES)
    b = rm.build_manifest({'Demo': root.replace('\\', '/') + '/'}, CLASSES)
    assert rm.diff_manifests(a, b)['root_moved'] == {}
    assert a['roots']['Demo'] == rm._norm_root(root)


def test_impact_status_change_linked_by_card(tmp_path):
    pf = _prov(tmp_path / 'pf', 'Ch05', {'§05.1': ['Demo/h.md#GT-T-001.3']})
    diff = {'changed': [], 'added': [], 'removed': [],
            'status_changes': [{'anchor': 'Demo/h.md#GT-T-001.6', 'from': 'chờ đo', 'to': 'đã đo'},
                               {'anchor': 'Demo/h.md#GT-T-0010.6', 'from': 'chờ đo', 'to': 'đã đo'}]}
    r = rp.impact(str(pf), diff)
    assert r['status_changes'][0]['chapters'] == ['Ch05'] and r['status_changes'][1]['chapters'] == []


def test_redact_generic_yt_and_rescan_gt_n(tmp_path):
    t, n = rr.redact('ý YT-LS-012 và YT-9 ở đây', [])
    assert 'YT-' not in t and n == 2
    assert rr._scan('còn GT-ZZ-7 sót', []) and rr._scan('và N-123 sót', []) and rr._scan('YT-77', [])
    assert not rr._scan('N-1234 không phải mã', [])


def test_build_warns_zero_unit_read_file(tmp_path, capsys):
    root = make_dossier(tmp_path)
    (tmp_path / 'Demo' / 'RE_D_S1B_Empty.md').write_text('\n\n', encoding='utf-8')
    book = tmp_path / 'Book'; book.mkdir()
    assert rm.main(['build', '--re', root, '--book', str(book)]) == 0
    assert 'CẢNH BÁO: Demo/RE_D_S1B_Empty.md 0 đơn vị' in capsys.readouterr().out
