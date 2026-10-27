import os
import subprocess
import sys
import unicodedata
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import p3_form_ref_check as m  # noqa: E402

FIX = Path(__file__).resolve().parent.parent / 'evals' / 'fixtures' / 'p3_form'
BOOKS_DIR = FIX / 'books'
PAD = ' '.join(['[TKHT Ch05]'] * 5)  # du 5 trich de khong dinh NO_CITATION


@pytest.fixture(scope='module')
def books():
    return {
        'TKHT': m.load_book(str(BOOKS_DIR / 'tkht.md')),
        'TKKTHT': m.load_book(str(BOOKS_DIR / 'tkktht')),
        'TKKTHT2': m.load_book(str(BOOKS_DIR / 'tkktht2')),
        'KL9': m.load_book(str(BOOKS_DIR / 'kl9.md')),
    }


def run(tmp_path, books, body, pad=True, raw=None):
    p = tmp_path / 'ref.md'
    if raw is not None:
        p.write_bytes(raw)
    else:
        p.write_text(body + ('\n' + PAD if pad else ''), encoding='utf-8')
    return m.check_file(str(p), books)


def codes(fs):
    return [f.code for f in fs]


def test_valid_citations_pass(tmp_path, books):
    body = '[TKHT Ch05 §05.4] [TKKTHT Ch16 §3.1] [KL9 Ch08 §13.6]'
    assert run(tmp_path, books, body) == []
    assert m.check_file(str(FIX / 'refs' / 'valid.md'), books) == []


def test_chapter_not_found(tmp_path, books):
    assert codes(run(tmp_path, books, '[TKHT Ch99]')) == ['CHAPTER_NOT_FOUND']


def test_section_not_found(tmp_path, books):
    assert codes(run(tmp_path, books, '[TKKTHT Ch16 §9.9]')) == ['SECTION_NOT_FOUND']


def test_letter_suffix_chapter(tmp_path, books):
    assert run(tmp_path, books, '[TKHT Ch05b §05b.4]') == []
    assert codes(run(tmp_path, books, '[TKHT Ch05 §05b.4]')) == ['SECTION_NOT_FOUND']


def test_tap2_citation(tmp_path, books):
    assert run(tmp_path, books, '[TKKTHT2 Ch13]') == []
    assert codes(run(tmp_path, books, '[TKKTHT2 Ch16]')) == ['CHAPTER_NOT_FOUND']


Q_OK = 'Hình thể của mối nối quyết định đường truyền lực qua toàn bộ kết cấu'


@pytest.mark.parametrize('l,r', [('“', '”'), ('«', '»')])
def test_quote_found_and_not_found(tmp_path, books, l, r):
    assert run(tmp_path, books, f'{l}{Q_OK}{r} [TKHT Ch05]') == []
    bad = Q_OK.replace('quyết', 'quyệt')
    assert codes(run(tmp_path, books, f'{l}{bad}{r} [TKHT Ch05]')) == ['QUOTE_NOT_FOUND']


def test_short_quote_not_checked(tmp_path, books):
    assert run(tmp_path, books, '“bịa bịa bịa” [TKHT Ch05]') == []


def test_ellipsis_quote_tail_fabricated(tmp_path, books):
    head = 'Hình thể của mối nối quyết định'
    tail_ok = 'qua toàn bộ kết cấu chịu tải chính'
    assert run(tmp_path, books, f'“{head} … {tail_ok}” [TKHT Ch05]') == []
    tail_bad = 'bịa hoàn toàn không có trong sách'
    assert codes(run(tmp_path, books, f'“{head} … {tail_bad}” [TKHT Ch05]')) == ['QUOTE_NOT_FOUND']


def test_uncited_row(tmp_path, books):
    body = '| Cột 1 | Cột 2 |\n|---|:---:|\n| a | b |\n| c | [ngoài sách] |\n| d | [TKHT Ch05] |'
    fs = run(tmp_path, books, body)
    assert codes(fs) == ['UNCITED_ROW']
    assert fs[0].line == 3


def test_no_citation(tmp_path, books):
    assert codes(run(tmp_path, books, '[TKHT Ch05]', pad=False)) == ['NO_CITATION']


def test_nfd_and_bom_input(tmp_path, books):
    text = f'“{Q_OK}” [TKHT Ch05 §05.4]\n{PAD}\n'
    raw = b'\xef\xbb\xbf' + unicodedata.normalize('NFD', text).encode('utf-8')
    assert run(tmp_path, books, '', raw=raw) == []


def test_bom_first_line_row_is_checked(tmp_path, books):
    raw = (b'\xef\xbb\xbf| x | y |\n' + PAD.encode('utf-8') + b'\n')
    fs = run(tmp_path, books, "", raw=raw)
    assert codes(fs) == ['UNCITED_ROW'] and fs[0].line == 1


def test_section_token_needs_boundary(tmp_path, books):
    assert codes(run(tmp_path, books, '[TKHT Ch05 §05.9]')) == ['SECTION_NOT_FOUND']


def test_load_book_shape(books):
    assert set(books['TKHT']) == {'05', '05b'}
    assert '05b.4' in books['TKHT']['05b']['sections']
    assert '05b.4' not in books['TKHT']['05']['sections']
    assert '13.6.2' in books['KL9']['08']['sections']
    assert '3.1' in books['TKKTHT']['16']['sections']


def _env(tmp_path, **over):
    env = dict(os.environ)
    env.update({
        'P3F_BOOK_TKHT': str(BOOKS_DIR / 'tkht.md'),
        'P3F_BOOK_TKKTHT': str(BOOKS_DIR / 'tkktht'),
        'P3F_BOOK_TKKTHT2': str(BOOKS_DIR / 'tkktht2'),
        'P3F_BOOK_KL9': str(BOOKS_DIR / 'kl9.md'),
        'PYTHONUTF8': '1',
    })
    env.update(over)
    return env


def cli(args, env):
    return subprocess.run([sys.executable, '-X', 'utf8', m.__file__] + args,
                          capture_output=True, text=True, encoding='utf-8', env=env)


def test_cli_clean_exit0(tmp_path):
    r = cli([str(FIX / 'refs')], _env(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr


def test_cli_finding_exit1(tmp_path):
    d = tmp_path / 'refs'
    d.mkdir()
    (d / 'a.md').write_text('[TKHT Ch99]\n' + PAD, encoding='utf-8')
    assert cli([str(d)], _env(tmp_path)).returncode == 1


def test_missing_book_exit3(tmp_path):
    r = cli([str(FIX / 'refs')], _env(tmp_path, P3F_BOOK_TKHT=str(tmp_path / 'nope.md')))
    assert r.returncode == 3


def test_missing_book_dir_exit3(tmp_path):
    (tmp_path / 'empty').mkdir()
    r = cli([str(FIX / 'refs')], _env(tmp_path, P3F_BOOK_TKKTHT=str(tmp_path / 'empty')))
    assert r.returncode == 3


def test_sample_writes_file(tmp_path):
    out = tmp_path / 's.txt'
    r = cli([str(FIX / 'refs'), '--sample', '1.0', '--seed', '1', '--out', str(out)], _env(tmp_path))
    assert r.returncode == 0, r.stdout + r.stderr
    txt = out.read_text(encoding='utf-8')
    assert 'Hình thể của mối nối' in txt
    assert 'valid.md' in txt
