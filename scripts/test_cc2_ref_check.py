"""Test cho cc2_ref_check.py - kiem trich nguon va trich nguyen van cua helix-cc2/references."""
import importlib.util
import os
import re
import subprocess
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPT = os.path.join(HERE, 'cc2_ref_check.py')
REF_DIR = os.path.join(REPO, 'skills', 'helix', 'helix-cc2', 'references')

REAL_CC = os.environ.get('CC2_BOOK_CC', 'D:/Workshop_X/3_Resources/Books/cc2-gia-thuyet-ket-cau/book.md')
REAL_TK = os.environ.get('CC2_BOOK_TK', 'D:/Workshop_X/3_Resources/Books/thiet-ke-hien-than/book.md')
HAS_BOOKS = os.path.isfile(REAL_CC) and os.path.isfile(REAL_TK)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


R = _load('cc2_ref_check', SCRIPT)

CAU = 'Shift dời trọng tâm từ WFP1 sang WFP2 theo câu hỏi'
BA_TRICH_THEM = '\n'.join(f'- quy tắc phụ {i} (CC Ch04)' for i in range(4)) + '\n'


@pytest.fixture
def books(tmp_path):
    cc = tmp_path / 'cc.md'
    cc.write_text('# Mở đầu\n\n## Chương 04 — Phân tích\n\nTrong chương này, ' + CAU
                  + ', không theo thói quen.\n', encoding='utf-8')
    tk = tmp_path / 'tk.md'
    tk.write_text('# Chương 06 — Truyền lực\n\nNội dung.\n', encoding='utf-8')
    return {'CC': str(cc), 'TK': str(tk)}


def _ref(tmp_path, body):
    d = tmp_path / 'refs'
    d.mkdir(exist_ok=True)
    (d / 'a.md').write_text(body, encoding='utf-8')
    return str(d)


def _codes(fs):
    return [f.code for f in fs]


def test_trich_dung_qua(tmp_path, books):
    d = _ref(tmp_path, f'- «{CAU}» (CC Ch04)\n' + BA_TRICH_THEM)
    assert R.check_refs(d, books) == []


def test_trich_duoi_bia_bi_bat(tmp_path, books):
    bia = CAU.replace('theo câu hỏi', 'theo mọi trường hợp')
    d = _ref(tmp_path, f'- «{bia}» (CC Ch04)\n' + BA_TRICH_THEM)
    assert _codes(R.check_refs(d, books)) == ['QUOTE_NOT_FOUND']


def test_trich_bo_dau_bi_bat(tmp_path, books):
    # giu dau: ban khong dau KHONG duoc coi la khop
    import unicodedata
    khong_dau = ''.join(c for c in unicodedata.normalize('NFD', CAU)
                        if unicodedata.category(c) != 'Mn')
    d = _ref(tmp_path, f'- «{khong_dau}» (CC Ch04)\n' + BA_TRICH_THEM)
    assert 'QUOTE_NOT_FOUND' in _codes(R.check_refs(d, books))


def test_trich_sai_sach_bi_bat(tmp_path, books):
    d = _ref(tmp_path, f'- «{CAU}» (TK Ch06)\n' + BA_TRICH_THEM)
    assert 'QUOTE_NOT_FOUND' in _codes(R.check_refs(d, books))


def test_trich_ca_hai_sach_chap_nhan_mot(tmp_path, books):
    d = _ref(tmp_path, f'- «{CAU}» (TK Ch06; CC Ch04)\n' + BA_TRICH_THEM)
    assert R.check_refs(d, books) == []


def test_trich_ngan_khong_kiem(tmp_path, books):
    d = _ref(tmp_path, '- «câu bịa ngắn» (CC Ch04)\n' + BA_TRICH_THEM)
    assert R.check_refs(d, books) == []


def test_chuong_khong_co(tmp_path, books):
    d = _ref(tmp_path, '- quy tắc (CC Ch99)\n' + BA_TRICH_THEM)
    assert _codes(R.check_refs(d, books)) == ['CHAPTER_NOT_FOUND']


def test_chuong_hau_to_chu(tmp_path):
    tk = tmp_path / 'tk.md'
    tk.write_text('# Chương 05b — Nổi\n', encoding='utf-8')
    cc = tmp_path / 'cc.md'
    cc.write_text('# Chương 04 — X\n', encoding='utf-8')
    d = _ref(tmp_path, '- a (TK Ch05b)\n- b (TK Ch05)\n' + BA_TRICH_THEM)
    fs = R.check_refs(d, {'CC': str(cc), 'TK': str(tk)})
    assert _codes(fs) == ['CHAPTER_NOT_FOUND'] and 'Ch05' in fs[0].msg and fs[0].line == 2


def test_it_trich(tmp_path, books):
    d = _ref(tmp_path, '- a (CC Ch04)\n- b (TK Ch06)\n')
    assert _codes(R.check_refs(d, books)) == ['NO_CITATION']


def test_khong_co_sach_thi_skip(tmp_path, books):
    d = _ref(tmp_path, f'- «{CAU}» (CC Ch04)\n' + BA_TRICH_THEM)
    env = dict(os.environ, CC2_BOOK_CC=str(tmp_path / 'khong.md'),
               CC2_BOOK_TK=str(tmp_path / 'khong2.md'), PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, d], capture_output=True, text=True,
                       encoding='utf-8', env=env)
    assert p.returncode == 3
    assert 'ĐẠT' not in p.stdout
    assert 'không có sách' in p.stdout + p.stderr


def test_cli_exit_1_khi_co_finding(tmp_path, books):
    d = _ref(tmp_path, '- a (CC Ch99)\n' + BA_TRICH_THEM)
    env = dict(os.environ, CC2_BOOK_CC=books['CC'], CC2_BOOK_TK=books['TK'],
               PYTHONIOENCODING='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, d], capture_output=True, text=True,
                       encoding='utf-8', env=env)
    assert p.returncode == 1 and 'CHAPTER_NOT_FOUND' in p.stdout


@pytest.mark.skipif(not HAS_BOOKS, reason='không có sách thật CC/TK trên máy này')
def test_refs_that():
    assert os.path.isdir(REF_DIR)
    names = sorted(f for f in os.listdir(REF_DIR) if f.endswith('.md'))
    assert names == sorted(['cc2-core.md', 'view-ops.md', 'synthesis-moves.md',
                            'embodiment-rules.md', 'param-bridge.md',
                            'hypothesis-sheet.md', 'multidomain.md'])
    assert R.check_refs(REF_DIR, {'CC': REAL_CC, 'TK': REAL_TK}) == []


def _read(name):
    with open(os.path.join(REF_DIR, name), encoding='utf-8') as f:
        return f.read()


def test_refs_khong_tro_ra_ngoai():
    for name in os.listdir(REF_DIR):
        t = _read(name)
        assert '../' not in t, name
        assert '1_Projects' not in t, name


def test_tieu_de_bat_buoc():
    need = {
        'cc2-core.md': ['## Từ vựng', '## Bảy bước dựng mô hình', '## Giới hạn dùng và bằng chứng',
                        '## Phạm vi cứng', '## Hai loại nhãn', 'dựng C&C²', 'chỉ bảng tham số',
                        'không áp dụng'],
        'view-ops.md': ['### zoom-in', '### zoom-out', '### shift', '### state', '### view',
                        '### observe', '## Rào cản quan sát'],
        'embodiment-rules.md': ['| Quy tắc | Câu hỏi kiểm hình thể | Tham số bị khoá | Nguồn |'],
        'param-bridge.md': ['| Phần tử | Tham số hình thể | Thông số chức năng | Chiều ảnh hưởng '
                            '| Ước lượng | Khoảng chọn | Nhãn | Nguồn số |'],
        'multidomain.md': ['C&C²: không áp dụng, vì'],
    }
    for name, items in need.items():
        t = _read(name)
        for it in items:
            assert it in t, f'{name}: thiếu {it!r}'
    vo = _read('view-ops.md')
    for op in ('zoom-in', 'zoom-out', 'shift', 'state', 'view', 'observe'):
        sec = vo.split(f'### {op}', 1)[1].split('\n##', 1)[0]
        for k in ('Khi nào:', 'Làm gì với mô hình:', 'Dấu hiệu dùng sai:'):
            assert k in sec, f'view-ops {op}: thiếu {k}'
    er = _read('embodiment-rules.md')
    for n in range(4, 17):
        assert re.search(rf'\|\s*TK Ch{n:02d}[a-z]?\s*[|§]', er), f'embodiment-rules thiếu TK Ch{n:02d}'


def test_phieu_mau_qua_lint():
    L = _load('cc2_sheet_lint', os.path.join(HERE, 'cc2_sheet_lint.py'))
    t = _read('hypothesis-sheet.md')
    fences = re.findall(r'```text\n(.*?)```', t, flags=re.S)
    filled = [f for f in fences if 'PHIẾU GIẢ THUYẾT' in f and '{{' not in f]
    assert filled, 'không có phiếu mẫu đã điền trong fence ```text'
    for f in filled:
        assert L.lint_sheets(f) == []
