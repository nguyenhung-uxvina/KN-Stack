import os
import re
import shutil
import sys
import unicodedata

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import p3_form_lint as L  # noqa: E402

GOOD = os.path.join(os.path.dirname(__file__), '..', 'evals', 'fixtures', 'p3_form', 'out_good')
P = 'TST_'
VAR, BEN, SCO, SEL = (P + n for n in ('BF_Form_Variants.md', 'BF_Benchmark.md',
                                      'BF_Scoring.md', 'BF_Form_Selection.md'))


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


def codes(d, quick=False):
    return {f.code for f in L.lint_dir(d, P, quick)}


def test_good_fixture_clean(d):
    assert L.lint_dir(d, P) == []


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
    mut(d, VAR, 'Nguồn quy tắc: [TKHT Ch05b §05b.4], [KL9 Ch08 §13.6]', 'Nguồn quy tắc: kinh nghiệm')
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
    mut(d, SCO, '| 7 | Mục 7 | Tiêu chí kiểm số 7 |\n', '')
    assert 'CHECKLIST_INCOMPLETE' in codes(d)


def test_checklist_blank_criterion(d):
    mut(d, SCO, 'Tiêu chí kiểm số 5 |', ' |')
    assert 'CHECKLIST_INCOMPLETE' in codes(d)


def test_checklist_skip_no_reason(d):
    mut(d, SCO, 'Bỏ — lý do: không có mối ghép hàn', 'Bỏ')
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
    assert L.lint_dir(d, P) == []
    mut(d, SCO, '| W tạm |', '| W lạ |')
    assert 'BAD_CELL' in codes(d)


def test_no_sensitivity(d):
    mut(d, SCO, '## Độ nhạy', '## Khác')
    assert 'NO_SENSITIVITY' in codes(d)


def test_candidate_missing(d):
    t = rd(d, SCO)
    t = t.replace(' PA-1-3 |', '', 1)
    # header loses PA-1-3 while rows keep the cell: BAD_CELL also fires; only the candidate code is asserted
    wr(d, SCO, t)
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
    assert L.lint_dir(d, P) == []


def test_cli_exit_codes(d, capsys):
    assert L.main([d, '--prefix', P]) == 0
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn:')
    assert L.main([d, '--prefix', P]) == 1
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
    fs = L.lint_dir(d, P)
    assert any(f.code == 'NO_SELECTION' and 'không tồn tại' in f.msg for f in fs)
    mut(d, SEL, '- Chọn: PA-2-1', '- Chọn: HC-1-9')
    assert any(f.code == 'NO_SELECTION' and 'không tồn tại' in f.msg for f in L.lint_dir(d, P))


def test_selection_hc_ok(d):
    mut(d, SEL, '- Chọn: PA-1-2', '- Chọn: HC-1-1')
    assert L.lint_dir(d, P) == []


def test_missing_scoring_section(d):
    mut(d, SCO, '## Bảng chấm', '## Khác bảng')
    assert 'NO_SCORING_TABLE' in codes(d)
