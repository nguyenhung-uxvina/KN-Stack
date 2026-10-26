"""Test cho cc2_sheet_lint.py - chan phieu gia thuyet va bang tham so thieu nhan."""
import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'cc2_sheet_lint.py')


def load():
    spec = importlib.util.spec_from_file_location('cc2_sheet_lint', SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['cc2_sheet_lint'] = mod
    spec.loader.exec_module(mod)
    return mod


L = load()

PHIEU_TOT = """PHIẾU GIẢ THUYẾT — GT-001
1 Tiêu đề: GT-001 chiều rộng khe dẫn hướng — điểm chạm lệch khi khe hẹp
2 NẾU: chiều rộng khe w = 3 mm | Đối chứng: w = 6 mm
3 THÌ: điểm chạm lệch dưới 2 mm
4 VÌ: khe hẹp ép tấm về một phía (giả định về tiếp xúc)
5 Phép thử: bàn thử 3 lần; ngày thử: 2026-11-10
6 {{điền SAU}}
7 Dự đoán: lệch < 2 mm; người ký CEO — ngày 2026-11-01
8 ĐỘ TIN / TẦM ẢNH HƯỞNG: trung (cơ chế quen, chưa đo) / thấp (đổi khe rẻ); bác bỏ nếu lệch >= 2 mm
9 NẾU BỊ BÁC: lặp trong pha — giữ khe 6 mm, không mở lại cổng nào
"""


def codes(text):
    return [f.code for f in L.lint_sheets(text)]


def bo_dong(text, prefix):
    return ''.join(l + '\n' for l in text.splitlines() if not l.startswith(prefix))


def thay(text, prefix, moi):
    return ''.join((moi if l.startswith(prefix) else l) + '\n' for l in text.splitlines())


def test_phieu_tot_sach():
    assert L.lint_sheets(PHIEU_TOT) == []


def test_lint_tep_rong_la_loi():
    assert [f.code for f in L.lint_sheets("# không có gì")] == ['NO_SHEETS']


def test_thieu_muc_4():
    t = bo_dong(PHIEU_TOT, '4 ')
    assert 'MISSING_ITEM' in codes(t) or 'NO_BECAUSE' in codes(t)
    assert 'MISSING_ITEM' in codes(t)


def test_muc_4_placeholder_la_no_because():
    assert 'NO_BECAUSE' in codes(thay(PHIEU_TOT, '4 ', '4 {{điền}}'))


def test_muc_khac_placeholder_la_missing():
    assert 'MISSING_ITEM' in codes(thay(PHIEU_TOT, '8 ', '8 {{điền}}'))


def test_tac_dung_o_neu():
    assert 'EFFECT_IN_IF' in codes(thay(PHIEU_TOT, '2 ', '2 NẾU: ma sát giảm | Đối chứng: w = 6 mm'))


def test_hai_bien():
    assert 'IF_MULTI_VAR' in codes(thay(PHIEU_TOT, '2 ', '2 NẾU: w = 3 mm, d = 20 mm | Đối chứng: w = 6 mm'))


def test_lint_du_doan_cung_ngay_thu():
    t = thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký CEO — ngày 2026-11-10')
    assert 'PRED_NOT_BEFORE_TEST' in codes(t)
    t2 = thay(PHIEU_TOT, '5 ', '5 Phép thử: bàn thử 3 lần')
    assert 'PRED_NOT_BEFORE_TEST' in codes(t2)


def test_du_doan_khong_ky():
    assert 'PRED_UNSIGNED' in codes(thay(PHIEU_TOT, '7 ', '7 Dự đoán: lệch < 2 mm'))


def test_lint_nhan_phieu_voi_gach_khac():
    for dash in ('-', '–', '—'):
        t = PHIEU_TOT.replace('—', dash, 1)
        t = ''.join('  ' + l + '\n' if l[:1].isdigit() else l + '\n' for l in t.splitlines())
        s = L.parse_sheets(t)
        assert len(s) == 1 and sorted(s[0]['items']) == list(range(1, 10)), dash
        assert L.lint_sheets(t) == [], dash


def test_phieu_trong_fence():
    t = "```\n" + PHIEU_TOT + "```\n7 khong thuoc phieu\n"
    s = L.parse_sheets(t)
    assert len(s) == 1 and 'khong thuoc' not in s[0]['items'][7]


def test_hai_phieu_tach_nhau():
    t = PHIEU_TOT + "\n" + PHIEU_TOT.replace('GT-001', 'GT-002')
    assert [s['id'] for s in L.parse_sheets(t)] == ['GT-001', 'GT-002']


BANG = """| Tham số | Nhãn | Nguồn số |
|---|---|---|
| w | tri thức | đo được (bàn thử 2026-10-01) |
| d | phỏng đoán | suy ra (từ w) |
| h | giả định | chưa biết |
"""


def test_bang_tot_sach():
    assert L.lint_param_table(BANG) == []


def test_bang_thieu_nhan():
    t = BANG + "| k |  | đo được (x) |\n"
    assert 'LABEL_MISSING' in [f.code for f in L.lint_param_table(t)]


def test_bang_nguon_sai():
    t = BANG + "| k | giả định | theo catalog |\n"
    assert 'SOURCE_MISSING' in [f.code for f in L.lint_param_table(t)]


def test_tri_thuc_chua_biet():
    t = BANG + "| k | tri thức | chưa biết |\n"
    assert 'KNOWLEDGE_NO_EVIDENCE' in [f.code for f in L.lint_param_table(t)]


def test_bang_khac_bi_bo_qua():
    t = "| a | b |\n|---|---|\n| 1 | 2 |\n"
    assert [f.code for f in L.lint_param_table(t)] == ["NO_TABLE"]


def chay(path, kind):
    return subprocess.run([sys.executable, SCRIPT, path, '--kind', kind],
                          capture_output=True, text=True, encoding='utf-8')


def test_cli_exit_code():
    with tempfile.TemporaryDirectory() as d:
        sach = os.path.join(d, 'a.md')
        rong = os.path.join(d, 'b.md')
        with open(sach, 'w', encoding='utf-8') as f:
            f.write(PHIEU_TOT)
        with open(rong, 'w', encoding='utf-8') as f:
            f.write('')
        assert chay(sach, 'hypo').returncode == 0
        r = chay(rong, 'hypo')
        assert r.returncode == 1 and 'NO_SHEETS' in r.stdout
        assert chay(os.path.join(d, 'khong-co.md'), 'hypo').returncode == 2


def test_tron_khong_phai_tac_dung():
    t = thay(PHIEU_TOT, '2 ', '2 NẾU: đường kính lỗ tròn d = 5 mm | Đối chứng: d = 8 mm')
    assert 'EFFECT_IN_IF' not in codes(t)


def test_wear_trong_swear_khong_tinh():
    t = thay(PHIEU_TOT, '2 ', '2 NẾU: wearable d = 5 mm')
    assert 'EFFECT_IN_IF' not in codes(t)


def test_mon_va_mai_mon_mot_finding():
    t = thay(PHIEU_TOT, '2 ', '2 NẾU: mài mòn giảm | Đối chứng: w = 6 mm')
    assert codes(t).count('EFFECT_IN_IF') == 1


def test_mot_bang_o_neu_mot_bang_o_doi_chung_sach():
    assert 'IF_MULTI_VAR' not in codes(PHIEU_TOT)


def test_params_khong_co_bang():
    assert [f.code for f in L.lint_param_table("# trống\n")] == ['NO_TABLE']
    assert [f.code for f in L.lint_param_table("")] == ['NO_TABLE']
    assert [f.code for f in L.lint_param_table("| a | b |\n|---|---|\n| 1 | 2 |\n")] == ['NO_TABLE']


def test_params_bang_khong_du_lieu():
    t = "| Tham số | Nhãn | Nguồn số |\n|---|---|---|\n"
    assert [f.code for f in L.lint_param_table(t)] == ['EMPTY_TABLE']


def test_cli_params_tep_rong_exit_1():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'r.md')
        open(p, 'w', encoding='utf-8').close()
        assert chay(p, 'params').returncode == 1


def test_cli_bom_exit_0():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'bom.md')
        with open(p, 'w', encoding='utf-8-sig') as f:
            f.write(PHIEU_TOT)
        assert chay(p, 'hypo').returncode == 0


def test_cli_utf8_hong_exit_2():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'bad.md')
        with open(p, 'wb') as f:
            f.write(b'PHI\xf4U \xff\xfe')
        r = chay(p, 'hypo')
        assert r.returncode == 2 and 'Traceback' not in r.stderr


# ------------------------------------------------- --allow-unsigned (truoc Cong CEO 3)

CHUA_KY = '7 DỰ ĐOÁN VIẾT TRƯỚC: lệch < 2 mm; người ký {{tên}} — ngày {{YYYY-MM-DD}}'


def test_allow_unsigned_bo_qua_dung_pred_unsigned():
    t = thay(PHIEU_TOT, '7 ', CHUA_KY)
    assert codes(t) == ['PRED_UNSIGNED']
    assert L.lint_sheets(t, allow_unsigned=True) == []


def test_ten_placeholder_la_chua_ky():
    t = thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký {{tên}} — ngày 2026-11-01')
    assert 'PRED_UNSIGNED' in codes(t)


def test_allow_unsigned_van_bat_ma_khac():
    t = bo_dong(thay(PHIEU_TOT, '7 ', CHUA_KY), '4 ')
    assert 'MISSING_ITEM' in [f.code for f in L.lint_sheets(t, allow_unsigned=True)]
    t2 = thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký CEO — ngày 2026-11-10')
    assert 'PRED_NOT_BEFORE_TEST' in [f.code for f in L.lint_sheets(t2, allow_unsigned=True)]
    t3 = thay(thay(PHIEU_TOT, '7 ', CHUA_KY), '5 ', '5 Phép thử: bàn thử 3 lần')
    assert [f.code for f in L.lint_sheets(t3, allow_unsigned=True)] == ['PRED_NOT_BEFORE_TEST']


def chay_co(path, *extra):
    return subprocess.run([sys.executable, SCRIPT, path, '--kind', 'hypo', *extra],
                          capture_output=True, text=True, encoding='utf-8')


def test_cli_allow_unsigned():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'chua-ky.md')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(thay(PHIEU_TOT, '7 ', CHUA_KY))
        assert chay_co(p, '--allow-unsigned').returncode == 0
        r = chay_co(p)
        assert r.returncode == 1 and 'PRED_UNSIGNED' in r.stdout
        q = os.path.join(d, 'thieu-muc.md')
        with open(q, 'w', encoding='utf-8') as f:
            f.write(bo_dong(thay(PHIEU_TOT, '7 ', CHUA_KY), '3 '))
        r = chay_co(q, '--allow-unsigned')
        assert r.returncode == 1 and 'MISSING_ITEM' in r.stdout
