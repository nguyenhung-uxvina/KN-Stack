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
7 Dự đoán: lệch < 2 mm; người ký CEO — ngày 2026-10-01
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


def test_nguoi_ky_gia_la_chua_ky():
    for ten in ('AI', 'ai', ' Claude ', 'TBD', 'tên', 'n/a', 'chưa ký', '<tên>', '{{tên}}'):
        t = thay(PHIEU_TOT, '7 ', f'7 Dự đoán: x; người ký {ten} — ngày 2026-11-01')
        assert 'PRED_UNSIGNED' in codes(t), ten


def test_nguoi_ky_that_sach():
    t = thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký Nguyễn Văn A — ngày 2026-11-01')
    assert codes(t) == []




# ------------------------------------------------- final-fix wave: C1 + I2

from datetime import date

REF_SHEET = os.path.join(os.path.dirname(HERE), 'skills', 'helix', 'helix-cc2', 'references', 'hypothesis-sheet.md')

KHUNG = """PHIẾU GIẢ THUYẾT — GT-001
1 Tiêu đề: GT-001 chiều rộng khe dẫn hướng
2 NẾU: chiều rộng khe w = 3 mm | Đối chứng: w = 6 mm
3 THÌ:
4 VÌ:
5 KIỂM: bàn thử 3 lần; ngày thử: 2026-11-10
6 KẾT QUẢ + khuyến nghị: {{điền SAU}}
7 DỰ ĐOÁN VIẾT TRƯỚC: lệch < 2 mm; người ký CEO — ngày 2026-10-01
8 …:
9 …:
"""


def test_khung_nhan_trong_bi_chan():
    cs = codes(KHUNG)
    assert 'NO_BECAUSE' in cs
    msgs = [f.msg for f in L.lint_sheets(KHUNG) if f.code == 'MISSING_ITEM']
    for k in (3, 8, 9):
        assert any(f'mục {k} ' in m for m in msgs), (k, msgs)


def test_cli_khung_exit_1():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'khung.md')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(KHUNG)
        r = chay(p, 'hypo')
        assert r.returncode == 1 and 'NO_BECAUSE' in r.stdout and 'MISSING_ITEM' in r.stdout


def test_muc_6_dien_sau_co_nhan_van_sach():
    t = thay(PHIEU_TOT, '6 ', '6 KẾT QUẢ + khuyến nghị: {{điền SAU}}')
    assert codes(t) == []


def test_muc_7_khong_du_doan_truoc_nguoi_ky():
    for v in ('7 DỰ ĐOÁN VIẾT TRƯỚC: người ký CEO — ngày 2026-10-01',
              '7 DỰ ĐOÁN VIẾT TRƯỚC: ; người ký CEO — ngày 2026-10-01',
              '7 người ký CEO — ngày 2026-10-01'):
        assert 'MISSING_ITEM' in codes(thay(PHIEU_TOT, '7 ', v)), v


def test_phieu_mau_reference_sach():
    with open(REF_SHEET, encoding='utf-8') as f:
        text = f.read()
    sample = text[text.index('## Phiếu mẫu đã điền'):]
    assert len(L.parse_sheets(sample)) == 1
    assert L.lint_sheets(sample, today=date.today()) == []


def test_tieu_de_markdown_duoc_nhan():
    for h in ('### PHIẾU GIẢ THUYẾT — GT-001', '**PHIẾU GIẢ THUYẾT — GT-001**', '## PHIẾU GIẢ THUYẾT - GT-001'):
        t = thay(PHIEU_TOT, 'PHIẾU', h)
        assert [s['id'] for s in L.parse_sheets(t)] == ['GT-001'], h
        assert codes(t) == [], h


def test_tieu_de_khong_doc_duoc():
    for h in ('PHIẾU GIẢ THUYẾT GT-002', 'Phiếu giả thuyết: GT-002', '### GT-002 góc móc'):
        t = PHIEU_TOT + '\n' + h + '\n1 Tiêu đề: x\n'
        assert 'HEADER_UNPARSED' in codes(t), h
    # nhac GT-nnn trong muc cua phieu hay trong bang thi khong phai tieu de
    t = PHIEU_TOT + '\n| GT-001 | 3 |\nXem GT-001 ở trên.\n'
    assert 'HEADER_UNPARSED' not in codes(t)


def test_tieu_de_hong_khong_co_phieu_nao():
    cs = codes('### Phiếu GT-001\n1 Tiêu đề: x\n')
    assert 'HEADER_UNPARSED' in cs and 'NO_SHEETS' in cs


def test_nguoi_ky_gia_chuoi_con():
    for ten in ('AI soạn', 'Claude (nháp)', 'trợ lý AI', 'TBD sau', '{{tên — CEO điền}}', '<tên>', 'N/A',
                'chưa ký, chờ CEO', 'ai'):
        t = thay(PHIEU_TOT, '7 ', f'7 Dự đoán: x; người ký {ten} — ngày 2026-10-01')
        assert 'PRED_UNSIGNED' in codes(t), ten


def test_ten_that_co_ai_trong_chu_sach():
    for ten in ('Mai', 'Hải', 'Nguyễn Văn A', 'Trần Thị Mai', 'Lại Văn Bình'):
        t = thay(PHIEU_TOT, '7 ', f'7 Dự đoán: x; người ký {ten} — ngày 2026-10-01')
        assert codes(t) == [], ten


def test_ngay_ky_tuong_lai():
    t = thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký CEO — ngày 2026-10-30')
    assert 'PRED_FUTURE_SIGN' in [f.code for f in L.lint_sheets(t, today=date(2026, 10, 26))]
    assert 'PRED_FUTURE_SIGN' not in [f.code for f in L.lint_sheets(t, today=date(2026, 10, 30))]
    assert 'PRED_FUTURE_SIGN' not in codes(t)  # khong truyen today thi khong kiem


def test_cli_truyen_today():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 'tl.md')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(thay(PHIEU_TOT, '7 ', '7 Dự đoán: x; người ký CEO — ngày 2999-01-01')
                    .replace('ngày thử: 2026-11-10', 'ngày thử: 2999-02-01'))
        r = chay(p, 'hypo')
        assert r.returncode == 1 and 'PRED_FUTURE_SIGN' in r.stdout, r.stdout


def test_khong_doi_chung():
    for v in ('2 NẾU: chiều rộng khe w = 3 mm', '2 NẾU: w = 3 mm; đối chứng w = 6 mm', '2 NẾU: w = 3 mm | 6 mm'):
        assert 'NO_CONTROL' in codes(thay(PHIEU_TOT, '2 ', v)), v
    assert 'NO_CONTROL' not in codes(thay(PHIEU_TOT, '2 ', '2 NẾU: w = 3 mm | đối chứng: w = 6 mm'))
    assert 'NO_CONTROL' not in codes(PHIEU_TOT)


def test_bang_tieu_de_khong_dau_va_hoa():
    t = BANG.replace('| Tham số | Nhãn | Nguồn số |', '| Tham số | Nhan | Nguon so |')
    assert L.lint_param_table(t) == []
    t2 = BANG.replace('| Tham số | Nhãn | Nguồn số |', '| Tham số | **NHÃN** | NGUỒN SỐ |')
    assert L.lint_param_table(t2) == []
    import unicodedata
    t3 = unicodedata.normalize('NFD', BANG)
    assert L.lint_param_table(t3) == []


def test_bang_mot_cot_la_partial():
    t = "| Tham số | Nhãn | Nguồn |\n|---|---|---|\n| w | tri thức | catalog |\n"
    cs = [f.code for f in L.lint_param_table(t)]
    assert 'PARTIAL_HEADER' in cs, cs
    t2 = BANG + "\n| Tham số | Nguồn số |\n|---|---|\n| k | chưa biết |\n"
    assert [f.code for f in L.lint_param_table(t2)] == ['PARTIAL_HEADER']
