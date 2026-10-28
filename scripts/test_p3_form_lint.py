import os
import re
import shutil
import sys
import unicodedata

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import p3_form_lint as L  # noqa: E402

FIX = os.path.join(os.path.dirname(__file__), '..', 'evals', 'fixtures', 'p3_form')
GOOD = os.path.join(FIX, 'out_good')
DRAFT_SEL = os.path.join(FIX, 'sel_draft')
REFS = os.path.join(FIX, 'lint_refs')
P = 'TST_'
VAR, BEN, SCO, SEL = (P + n for n in ('BF_Form_Variants.md', 'BF_Benchmark.md',
                                      'BF_Scoring.md', 'BF_Form_Selection.md'))
RULE_LINE = 'Nguồn quy tắc: TKHT-R901 [TKHT Ch05b §05b.4], KL-R901 [KL9 Ch08 §13.6]'


@pytest.fixture
def d(tmp_path):
    out = tmp_path / 'out'
    shutil.copytree(GOOD, out)
    return str(out)


def rd(d, n):
    with open(os.path.join(d, n), encoding='utf-8') as f:
        return f.read()


def wr(d, n, t):
    with open(os.path.join(d, n), 'w', encoding='utf-8', newline='\n') as f:
        f.write(t)


def mut(d, n, old, new, count=1):
    t = rd(d, n)
    assert old in t, f'mutation target not found: {old!r}'
    wr(d, n, t.replace(old, new, count))


def lint(d, quick=False, draft=False, refs=REFS):
    return L.lint_dir(d, P, quick, draft=draft, refs=refs)


def codes(d, quick=False, draft=False, refs=REFS):
    return {f.code for f in lint(d, quick, draft, refs)}


def test_good_fixture_clean(d):
    assert lint(d) == []


def test_missing_file(d):
    os.remove(os.path.join(d, SEL))
    assert 'MISSING_FILE' in codes(d)


def test_too_few_variants(d):
    t = rd(d, VAR)
    t = re.sub(r'### PA-1-3.*?(?=## F-2)', '', t, flags=re.S)
    wr(d, VAR, t)
    assert 'TOO_FEW_VARIANTS' in codes(d)


def test_quick_allows_two_variants(d):
    t = rd(d, VAR)
    wr(d, VAR, re.sub(r'### PA-1-3.*?(?=## F-2)', '', t, flags=re.S))
    assert 'TOO_FEW_VARIANTS' not in codes(d, quick=True)
    t = rd(d, VAR)
    wr(d, VAR, re.sub(r'### PA-1-2.*?(?=## F-2)', '', t, flags=re.S))
    assert 'TOO_FEW_VARIANTS' in codes(d, quick=True)


def test_variant_no_rule(d):
    mut(d, VAR, RULE_LINE, 'Nguồn quy tắc: kinh nghiệm')
    assert 'VARIANT_NO_RULE' in codes(d)


def test_variant_no_param(d):
    mut(d, VAR, 'Tham số khoá: M24, cấp bền 8.8, n=1', 'Tham số khoá:')
    assert 'VARIANT_NO_PARAM' in codes(d)


def test_bad_label_variant(d):
    mut(d, VAR, 'Nhãn: tri thức', 'Nhãn: chắc chắn')
    assert 'BAD_LABEL' in codes(d)


def test_bad_label_benchmark(d):
    mut(d, BEN, 'Nhãn: phỏng đoán', 'Nhãn: ước chừng')
    assert 'BAD_LABEL' in codes(d)


def test_bench_no_date(d):
    mut(d, BEN, 'Truy cập: 2026-10-20', 'Truy cập: hôm qua')
    assert 'BENCH_NO_DATE' in codes(d)


def test_bench_no_chain(d):
    mut(d, BEN, 'Chuỗi C&C²: WFP1 → Connector → WFP2', 'Chuỗi C&C²:')
    assert 'BENCH_NO_CHAIN' in codes(d)


def test_too_many_bench(d):
    extra = ''.join(f'### HC-1-{n} — X\n- Nguồn: https://x.org\n- Truy cập: 2026-10-20\n'
                    f'- Nhãn: giả định\n- Chuỗi C&C²: a\n\n' for n in range(3, 10))
    t = rd(d, BEN)
    wr(d, BEN, t.replace('## F-2', extra + '## F-2', 1))
    assert 'TOO_MANY_BENCH' in codes(d)


@pytest.mark.parametrize('src,ok', [
    ('US 9,097,498 B2', True), ('CN116753779A', True), ('https://example.org/x', True),
    ('RE/ArtixGear/x.md', True), (r'RE\ArtixGear\x.md', True), ('báo chí', False)])
def test_benchmark_source_forms(d, src, ok):
    mut(d, BEN, 'Nguồn: https://example.com/a', 'Nguồn: ' + src)
    assert ('BENCH_NO_SOURCE' not in codes(d)) is ok


def test_checklist_incomplete(d):
    t = rd(d, SCO)
    wr(d, SCO, re.sub(r'^\| 7 \|.*\n', '', t, count=1, flags=re.M))
    assert 'CHECKLIST_INCOMPLETE' in codes(d)


def test_checklist_blank_criterion(d):
    mut(d, SCO, 'Tiêu chí kiểm số 5 |', ' |')
    assert 'CHECKLIST_INCOMPLETE' in codes(d)


def test_checklist_skip_no_reason(d):
    mut(d, SCO, 'Bỏ — lý do: không có mốc giao hàng ràng buộc', 'Bỏ')
    assert 'CHECKLIST_SKIP_NO_REASON' in codes(d)


def test_bad_cell_d_and_w(d):
    mut(d, SCO, '| D | DP-1 | 1 | Đạt | Đạt | Loại', '| D | DP-1 | 1 | Đạt | Đạt | Có')
    assert 'BAD_CELL' in codes(d)


def test_bad_cell_w_range(d):
    mut(d, SCO, '| W | DP-2 | 3 | 3 | 4 |', '| W | DP-2 | 3 | 7 | 4 |')
    assert 'BAD_CELL' in codes(d)


def test_question_cell_requires_reason(d):
    mut(d, SCO, '?(chưa có số liệu)', '?()')
    assert 'QUESTION_NO_REASON' in codes(d)


def test_empty_weight_requires_red_flag(d):
    mut(d, SCO, '🔴 CEO chốt trọng số', 'CEO chốt trọng số')
    assert 'EMPTY_WEIGHT_NO_FLAG' in codes(d)


def test_provisional_dw_ok(d):
    assert 'W tạm' in rd(d, SCO)
    assert lint(d) == []
    mut(d, SCO, '| W tạm |', '| W lạ |')
    assert 'BAD_CELL' in codes(d)


def test_no_sensitivity(d):
    mut(d, SCO, '## Độ nhạy', '## Khác')
    assert 'NO_SENSITIVITY' in codes(d)


def test_candidate_missing(d):
    mut(d, SCO, '| Req-ID | D/W | DP | Trọng số | PA-1-1 | PA-1-2 | PA-1-3 |',
        '| Req-ID | D/W | DP | Trọng số | PA-1-1 | PA-1-2 |')
    # header loses PA-1-3 while rows keep the cell: BAD_CELL also fires; only the candidate code is asserted
    assert 'CANDIDATE_MISSING' in codes(d)


def test_no_selection(d):
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn:')
    assert 'NO_SELECTION' in codes(d)


def test_no_test_plan(d):
    mut(d, SEL, '- Kế hoạch thử: kéo thử 3 mẫu', '- Kế hoạch thử:')
    assert 'NO_TEST_PLAN' in codes(d)


def test_no_param_range(d):
    mut(d, SEL, '- Khoảng tham số: M20–M24', '- Khoảng tham số:')
    assert 'NO_PARAM_RANGE' in codes(d)


def test_lint_nfd_bom(d):
    for n in os.listdir(d):
        t = unicodedata.normalize('NFD', rd(d, n))
        with open(os.path.join(d, n), 'w', encoding='utf-8-sig', newline='\n') as f:
            f.write(t)
    assert lint(d) == []


def test_cli_exit_codes(d, capsys):
    assert L.main([d, '--prefix', P, '--refs', REFS]) == 0
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn:')
    assert L.main([d, '--prefix', P, '--refs', REFS]) == 1
    assert L.main([]) == 2


def test_bad_weight_not_number(d):
    mut(d, SCO, '| W | DP-2 | 3 |', '| W | DP-2 | nhiều |')
    assert 'BAD_CELL' in codes(d)


def test_selection_must_name_candidate(d):
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn: cái thứ hai')
    assert 'NO_SELECTION' in codes(d)


def test_empty_variants_fails_closed(d):
    wr(d, VAR, '# Phương án hình thể\n')
    assert 'TOO_FEW_VARIANTS' in codes(d)


def test_empty_benchmark_no_bench(d):
    wr(d, BEN, '# Chuẩn đối sánh\n')
    assert 'NO_BENCH' in codes(d)


def test_selection_missing_f_block(d):
    t = rd(d, SEL)
    wr(d, SEL, re.sub(r'## F-2.*', '', t, flags=re.S))
    assert 'NO_SELECTION' in codes(d)


def test_selection_unknown_candidate(d):
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn: PA-2-1')
    fs = lint(d)
    assert any(f.code == 'NO_SELECTION' and 'không tồn tại' in f.msg for f in fs)
    mut(d, SEL, '- Chọn: PA-2-1', '- Chọn: HC-1-9')
    assert any(f.code == 'NO_SELECTION' and 'không tồn tại' in f.msg for f in lint(d))


def test_selection_hc_ok(d):
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn: HC-1-1')
    assert lint(d) == []


def test_missing_scoring_section(d):
    mut(d, SCO, '## Bảng chấm\n\n### F-1\n\n| Req-ID', '## Khác bảng\n\n### F-1\n\n| Req-ID')
    assert 'NO_SCORING_TABLE' in codes(d)


F2_PA_ONLY = """### F-2

| Req-ID | D/W | DP | Trọng số | PA-2-1 | PA-2-2 | PA-2-3 | Ghi chú |
|---|---|---|---|---|---|---|---|
| R-21 | D | DP-1 | 1 | Đạt | Đạt | Loại | |
| R-22 | W | DP-2 | 3 | 3 | 4 | 2 | |

"""

ITEMS = ['Function', 'Working principle', 'Layout', 'Safety', 'Ergonomics', 'Production',
         'Quality control', 'Assembly', 'Transport', 'Operation', 'Maintenance', 'Recycling',
         'Costs', 'Schedules']


def ck_table(fid, cands):
    out = [f'### F-{fid}', '', '| # | Mục | Tiêu chí | ' + ' | '.join(cands) + ' |',
           '|' + '---|' * (3 + len(cands))]
    for n, name in enumerate(ITEMS, 1):
        out.append(f'| {n} | {name} | Tiêu chí kiểm số {n} | ' + ' | '.join(['Đạt'] * len(cands)) + ' |')
    return '\n'.join(out) + '\n\n'


def _drop_hc_f2(d, reason_line):
    """F-2 khong con HC nao: Benchmark chi giu dong ly do, checklist va bang cham F-2 chi co cot PA."""
    t = rd(d, BEN)
    wr(d, BEN, t[:t.index('### HC-2-1')] + reason_line)
    t = rd(d, SCO)
    b = t.index('## Bảng chấm')
    s, e = t.index('### F-2', b), t.index('## Độ nhạy')
    t = t[:s] + F2_PA_ONLY + t[e:]
    s = t.index('### F-2')
    t = t[:s] + ck_table(2, ['PA-2-1', 'PA-2-2', 'PA-2-3']) + t[t.index('## Bảng chấm'):]
    wr(d, SCO, t)


def test_no_hc_with_reason_ok(d):
    _drop_hc_f2(d, '- Không tìm thấy HC — lý do: đã tìm tầng 1 (RE/, FTO_*), tầng 2 (Exa web), '
                   'tầng 3 (Exa patents) — không có lời giải cùng chức năng\n')
    assert lint(d) == []


def test_no_hc_reason_empty_fails(d):
    _drop_hc_f2(d, '- Không tìm thấy HC — lý do:\n')
    assert 'NO_BENCH' in codes(d)


def test_no_hc_without_line_fails(d):
    _drop_hc_f2(d, '')
    assert 'NO_BENCH' in codes(d)


# --- I3: checklist 14 muc theo tung chuc nang ---

def test_checklist_table_per_function(d):
    t = rd(d, SCO)
    s = t.index('### F-2')
    wr(d, SCO, t[:s] + t[t.index('## Bảng chấm'):])
    assert any(f.code == 'CHECKLIST_INCOMPLETE' and 'F-2' in f.msg for f in lint(d))


def test_checklist_no_tables_at_all(d):
    t = rd(d, SCO)
    s = t.index('### F-1')
    wr(d, SCO, t[:s] + t[t.index('## Bảng chấm'):])
    fs = [f for f in lint(d) if f.code == 'CHECKLIST_INCOMPLETE']
    assert {'F-1', 'F-2'} <= {m for f in fs for m in re.findall(r'F-\d', f.msg)}


def test_checklist_candidate_missing(d):
    mut(d, SCO, '| # | Mục | Tiêu chí | PA-1-1 | PA-1-2 | PA-1-3 | HC-1-1 | HC-1-2 |',
        '| # | Mục | Tiêu chí | PA-1-1 | PA-1-2 | PA-1-3 | HC-1-1 |')
    assert 'CHECKLIST_CANDIDATE_MISSING' in codes(d)


@pytest.mark.parametrize('old,new', [
    ('| Không đạt |', '| Kém |'),
    ('| Không đạt |', '| |'),
    ('| Không đạt |', '| — |'),
    ('| — | — | — | — | — |', '| Đạt | — | — | — | — |'),
])
def test_checklist_bad_cell(d, old, new):
    mut(d, SCO, old, new)
    assert 'BAD_CELL' in codes(d)


def test_checklist_question_needs_reason(d):
    mut(d, SCO, '?(chưa thử)', '?()')
    assert 'QUESTION_NO_REASON' in codes(d)


def test_checklist_row_count_per_function(d):
    t = rd(d, SCO)
    s = t.index('### F-2')
    tail = re.sub(r'^\| 12 \|.*\n', '', t[s:], count=1, flags=re.M)
    wr(d, SCO, t[:s] + tail)
    assert any(f.code == 'CHECKLIST_INCOMPLETE' and 'F-2' in f.msg and '12' in f.msg for f in lint(d))


# --- m1: dong D khong can trong so ---

def test_d_row_blank_weight_ok(d):
    assert '| R-14 | D | DP-4 | |' in rd(d, SCO)
    assert lint(d) == []
    mut(d, SCO, '| R-14 | D | DP-4 | | Đạt | Đạt | Đạt | Đạt | Đạt |',
        '| R-14 | W | DP-4 | | 1 | 1 | 1 | 1 | 1 |')
    assert 'EMPTY_WEIGHT_NO_FLAG' in codes(d)


# --- m2: PA/HC dung khoi F ---

def test_pa_under_wrong_f_block(d):
    mut(d, VAR, '### PA-1-3 — Phương án 3', '### PA-2-9 — Phương án 3')
    assert 'ID_BLOCK_MISMATCH' in codes(d)


def test_hc_under_wrong_f_block(d):
    mut(d, BEN, '### HC-1-2 — Sản phẩm 2', '### HC-2-7 — Sản phẩm 2')
    assert 'ID_BLOCK_MISMATCH' in codes(d)


# --- I1: ma quy tac + con tro sach phai co trong references ---

def test_rule_code_missing(d):
    mut(d, VAR, RULE_LINE, 'Nguồn quy tắc: [TKHT Ch05b §05b.4], [KL9 Ch08 §13.6]')
    assert 'RULE_CODE_MISSING' in codes(d)


def test_rule_code_unknown(d):
    mut(d, VAR, 'TKHT-R901 [TKHT Ch05b §05b.4]', 'TKHT-R999 [TKHT Ch05b §05b.4]')
    assert 'RULE_CODE_UNKNOWN' in codes(d)


@pytest.mark.parametrize('line', [
    'Nguồn quy tắc: TKHT-R901 [TKHT Ch99 §99.9]',
    'Nguồn quy tắc: TKHT-R901 [KL9 Ch08 §13.6]',
    'Nguồn quy tắc: TKHT-R901 [TKHT Ch05b §05b.4], [TKHT Ch99 §99.9]',
])
def test_citation_not_in_rule(d, line):
    mut(d, VAR, RULE_LINE, line)
    assert 'CITATION_NOT_IN_RULE' in codes(d)


@pytest.mark.parametrize('bad', [
    '[TKHT Ch99 §99.9, tr.12]',
    '[TKHT Ch99 §99]',
    '[TKHT Ch99 § 99.9 ]',
    '[tkht Ch99 §99.9]',
    '[TKKTHT Ch99 §1.1; KL9 Ch01 §1.1]',
])
def test_citation_malformed(d, bad):
    mut(d, VAR, RULE_LINE, f'Nguồn quy tắc: PB-R901, PB-M901 [TKKTHT Ch22 §1.2] {bad}')
    assert 'CITATION_MALFORMED' in codes(d)


def test_citation_wellformed_pair_ok(d):
    mut(d, VAR, RULE_LINE, 'Nguồn quy tắc: PB-R901, PB-M901 [TKKTHT Ch22 §1.2], [TKKTHT2 Ch13]')
    assert lint(d) == []


def test_citation_any_code_on_line_ok(d):
    mut(d, VAR, RULE_LINE, 'Nguồn quy tắc: PB-R901, PB-M901 [TKKTHT Ch22 §1.2] [TKKTHT2 Ch13]')
    assert lint(d) == []


def test_real_references(d):
    good = 'Nguồn quy tắc: TKHT-R300 [TKHT Ch13b §13b.9], PB-R175 [TKKTHT Ch22 §1.2]'
    wr(d, VAR, rd(d, VAR).replace(RULE_LINE, good))
    assert lint(d, refs=None) == []
    mut(d, VAR, good, 'Nguồn quy tắc: TKHT-R300 [TKHT Ch99 §99.9]')
    assert 'CITATION_NOT_IN_RULE' in codes(d, refs=None)


def test_cli_refs_missing_dir(d, tmp_path):
    assert L.main([d, '--prefix', P, '--refs', str(tmp_path / 'khong-co')]) == 2


# --- I2: Selection nhap / chinh thuc ---

def _use_draft(d):
    shutil.copy(os.path.join(DRAFT_SEL, SEL), os.path.join(d, SEL))


def test_draft_selection_ok_in_draft_mode(d):
    _use_draft(d)
    assert lint(d, draft=True) == []
    assert L.main([d, '--prefix', P, '--refs', REFS, '--draft']) == 0


def test_draft_selection_fails_final(d):
    _use_draft(d)
    assert {'SELECTION_DRAFT', 'NO_GATE2_DATE', 'NO_CEO_REASON'} <= codes(d)
    assert L.main([d, '--prefix', P, '--refs', REFS]) == 1


def test_draft_mode_rejects_candidate_id(d):
    _use_draft(d)
    mut(d, SEL, '- Chọn: (chờ CEO)', '- Chọn: PA-1-2 (đề xuất — chờ CEO)')
    assert 'SELECTION_DRAFT' in codes(d, draft=True)


def test_draft_mode_still_needs_fields(d):
    _use_draft(d)
    mut(d, SEL, '- Chọn: (chờ CEO)', '- Chọn:')
    assert 'NO_SELECTION' in codes(d, draft=True)
    _use_draft(d)
    mut(d, SEL, '- Kế hoạch thử: kéo thử 3 mẫu (nháp)', '- Kế hoạch thử:')
    assert 'NO_TEST_PLAN' in codes(d, draft=True)


def test_final_good_fails_draft_mode(d):
    assert 'SELECTION_DRAFT' in codes(d, draft=True)


@pytest.mark.parametrize('new', ['- Chọn: PA-1-2 — Phương án 2 (đề xuất — chờ CEO)',
                                 '- Chọn: PA-1-2 — Phương án 2 (chờ CEO)'])
def test_final_rejects_pending(d, new):
    mut(d, SEL, '- Chọn: PA-1-2 — Phương án 2', new)
    assert 'SELECTION_DRAFT' in codes(d)


@pytest.mark.parametrize('new', ['- Chọn: PA-1-2', '- Chọn: PA-1-2 —', '- Chọn: PA-1-2 - Phương án 2'])
def test_final_requires_name(d, new):
    mut(d, SEL, '- Chọn: PA-1-2 — Phương án 2', new)
    assert 'SELECTION_NO_NAME' in codes(d)


def test_final_requires_ceo_reason(d):
    mut(d, SEL, '- Lý do CEO: hai bu lông chia tải, thay được tại bãi bắn', '- Lý do CEO:')
    assert 'NO_CEO_REASON' in codes(d)
    mut(d, SEL, '- Lý do CEO:\n', '')
    assert 'NO_CEO_REASON' in codes(d)


@pytest.mark.parametrize('new', ['', 'Cổng CEO 2 — ngày hôm nay',
                                 'Cổng CEO 2 — ngày 2026-10-27\nCổng CEO 2 — ngày 2026-10-28'])
def test_final_requires_gate2_date(d, new):
    mut(d, SEL, 'Cổng CEO 2 — ngày 2026-10-27 · lint p3_form_lint: exit 0', new)
    assert 'NO_GATE2_DATE' in codes(d)
