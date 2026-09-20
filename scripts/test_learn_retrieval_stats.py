# -*- coding: utf-8 -*-
"""Test cho skills/learn/learn-track/scripts/retrieval_stats.py.

Chạy: python -m pytest scripts/test_learn_retrieval_stats.py -v

Script này tồn tại để Progress Tracker của learn-track lấy bằng chứng từ phép đo
(sổ hồi tưởng của learn-teach) thay vì để AI tự chấm trình độ người học. Nên hai
thứ quan trọng nhất: đếm đúng ô "chắc mà sai", và KHÔNG âm thầm bỏ dòng hỏng —
một dòng bị bỏ im lặng làm tỉ lệ đẹp hơn thật.
"""
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'skills', 'learn', 'learn-track', 'scripts', 'retrieval_stats.py')

spec = importlib.util.spec_from_file_location('retrieval_stats', SCRIPT)
rs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rs)

SO = """# Sổ Hồi Tưởng — CFMA

**Cập nhật:** 2026-09-19 · **Hiệu chỉnh tổng:** quá tự tin 1/4 lượt

| # | Mục | Bài | Đoán | Thực | Bậc | Đến hạn | Ghi chú |
|---|-----|-----|------|------|-----|---------|---------|
| 1 | Vì sao CFMA phân tích theo chức năng | 01 | C | ✓ | 3 | 2026-09-25 | |
| 2 | D cao nghĩa là gì | 01 | C | ✗ | 1 | 2026-09-18 | **ảo giác** |
| 3 | Khi nào được dùng tổng SFD | 02 | T | ✓ | 2 | 2026-09-19 | dưới tự tin |
| 4 | Rev SFD khác SFD ở đâu | 02 | V | ✗ | 1 | 2026-09-20 | |
| 5 | Thang F đo theo đơn vị gì | 02 | | | 1 | 2026-09-21 | chưa ôn |

**Đã bỏ qua:** 2026-09-10 — bỏ 2 mục
"""


def ghi(tmp_path, noi_dung=SO, ten='RETRIEVAL.md'):
    p = tmp_path / ten
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(noi_dung, encoding='utf-8')
    return p


def chay(*args):
    p = subprocess.run([sys.executable, SCRIPT, *map(str, args)],
                       capture_output=True, text=True, encoding='utf-8')
    return p.returncode, p.stdout + p.stderr


def test_dem_co_ban(tmp_path):
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path))), '2026-09-19')
    assert s['tong'] == 5
    assert s['da_on'] == 4
    assert s['dung'] == 2
    assert s['o']['C✗'] == 1 and s['o']['T✓'] == 1 and s['o']['C✓'] == 1 and s['o']['V✗'] == 1


def test_den_han_tinh_ca_hom_nay_va_qua_han(tmp_path):
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path))), '2026-09-19')
    assert sorted(s['den_han']) == ['2', '3']


def test_theo_bai(tmp_path):
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path))), '2026-09-19')
    b = s['theo_bai']
    assert b['01'] == {'muc': 2, 'da_on': 2, 'dung': 1, 'chac_sai': 1, 'bac_tb': 2.0}
    assert b['02']['muc'] == 3 and b['02']['da_on'] == 2 and b['02']['chac_sai'] == 0


def test_chac_ma_sai_dem_dung_chieu(tmp_path):
    """Soát PR: fixture cũ có 1 hàng C+✓ và 1 hàng C+✗ trong CÙNG bài 01, nên đảo cực tính
    ('C','✗')→('C','✓') vẫn ra 1 — cột chac_sai của bảng-theo-bài không bị ghim."""
    so = SO.replace('| 2 | D cao nghĩa là gì | 01 | C | ✗ |', '| 2 | D cao nghĩa là gì | 03 | C | ✓ |')
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path, so))), '2026-09-19')
    assert s['theo_bai']['03']['chac_sai'] == 0      # bài chỉ có C+✓
    assert s['theo_bai']['01']['chac_sai'] == 0
    assert s['o']['C✓'] == 2 and s['o']['C✗'] == 0


def test_thieu_cot_thu_tu_van_chay_duoc(tmp_path):
    """Soát PR: cổng tiêu đề chỉ đòi Mục/Đoán/Thực, nhưng thong_ke đọc r['#'] vô điều kiện →
    sổ không có cột '#' mà có mục quá hạn ⇒ KeyError + mã 1 (mã 1 nghĩa là 'đã liệt kê dòng
    hỏng' — ở đây chỉ có traceback)."""
    so = ('# Sổ\n\n| Mục | Bài | Đoán | Thực | Bậc | Đến hạn |\n|---|---|---|---|---|---|\n'
          '| Vì sao X | 01 | C | ✓ | 2 | 2026-09-01 |\n')
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 0, out
    assert 'Traceback' not in out
    assert 'Đến hạn hoặc quá hạn: 1' in out


def test_giu_cho_o_cot_bac_va_den_han(tmp_path):
    """Soát PR: TRONG chỉ áp cho Đoán/Thực; '—' ở cột Bậc/Đến hạn bị coi là dòng hỏng và
    chặn cả Progress Tracker vì một ô giữ chỗ hợp lệ."""
    so = SO.replace('| 5 | Thang F đo theo đơn vị gì | 02 | | | 1 | 2026-09-21 | chưa ôn |',
                    '| 5 | Thang F đo theo đơn vị gì | 02 | — | — | — | — | chưa ôn |')
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 0, out


def test_o_in_dam_van_doc_duoc(tmp_path):
    """Soát PR: _chuan() (bỏ **) áp cho Đoán mà không áp cho Thực. Sổ thật dùng in đậm trong
    bảng, nên '**✗**' rất dễ xảy ra — và đó đúng là ô 'chắc mà sai' cần bắt nhất."""
    so = SO.replace('| 2 | D cao nghĩa là gì | 01 | C | ✗ |', '| 2 | D cao nghĩa là gì | 01 | C | **✗** |')
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 0, out
    assert 'chắc✗ 1' in out


def test_cli_in_ra_o_chac_ma_sai_va_nhan_anh_chup(tmp_path):
    rc, out = chay(ghi(tmp_path), '--hom-nay', '2026-09-19')
    assert rc == 0, out
    assert 'D cao nghĩa là gì' in out            # liệt kê tên mục chắc-mà-sai
    assert 'lần hồi tưởng gần nhất' in out       # nói rõ đây là ảnh chụp, không phải lịch sử
    assert 'không đo năng lực làm' in out


def test_cot_dao_thu_tu_van_doc_dung(tmp_path):
    so = SO.replace('| # | Mục | Bài | Đoán | Thực | Bậc | Đến hạn | Ghi chú |',
                    '| # | Bài | Mục | Thực | Đoán | Bậc | Đến hạn | Ghi chú |')
    # đảo nội dung hàng cho khớp tiêu đề mới
    so = so.replace('| 1 | Vì sao CFMA phân tích theo chức năng | 01 | C | ✓ |',
                    '| 1 | 01 | Vì sao CFMA phân tích theo chức năng | ✓ | C |')
    rows = [r for r in rs.doc_so(str(ghi(tmp_path, so)))['hang'] if r['#'] == '1']
    assert rows[0]['doan'] == 'C' and rows[0]['thuc'] == '✓' and rows[0]['bai'] == '01'


def test_dong_hong_khong_bi_bo_im_lang(tmp_path):
    so = SO.replace('| 4 | Rev SFD khác SFD ở đâu | 02 | V | ✗ |', '| 4 | Rev SFD khác SFD ở đâu | 02 | chắc lắm | có |')
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 1, out
    assert 'KHÔNG ĐỌC ĐƯỢC' in out and '#4' in out


def test_on_ma_khong_ghi_doan_van_tinh_vao_ty_le_nho(tmp_path):
    """Sổ thật (icdm, 15/08): Đoán = '—', Thực = ✗ — ĐÃ ôn mà không ghi đoán trước.
    Loại dòng đó ra thì tỉ lệ báo 'đã hồi tưởng 0/6' — sai. Phải tính vào tỉ lệ nhớ,
    chỉ bỏ khỏi hiệu chỉnh, và nói rõ lượt đó không đo được ảo giác."""
    so = SO.replace('| 4 | Rev SFD khác SFD ở đâu | 02 | V | ✗ |', '| 4 | Rev SFD khác SFD ở đâu | 02 | — | ✗ |')
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path, so))), '2026-09-19')
    assert s['da_on'] == 4 and s['dung'] == 2
    assert s['thieu_doan'] == ['4']
    assert s['o']['V✗'] == 0
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 0, out
    assert 'không ghi đoán' in out


def test_gach_ngang_ca_hai_cot_la_chua_on(tmp_path):
    so = SO.replace('| 5 | Thang F đo theo đơn vị gì | 02 | | |', '| 5 | Thang F đo theo đơn vị gì | 02 | — | — |')
    s = rs.thong_ke(rs.doc_so(str(ghi(tmp_path, so))), '2026-09-19')
    assert s['tong'] == 5 and s['da_on'] == 4


def test_doan_ma_chua_co_thuc_la_hong(tmp_path):
    so = SO.replace('| 5 | Thang F đo theo đơn vị gì | 02 | | |', '| 5 | Thang F đo theo đơn vị gì | 02 | C | |')
    rc, out = chay(ghi(tmp_path, so), '--hom-nay', '2026-09-19')
    assert rc == 1 and '#5' in out, out


def test_nhan_thu_muc_workspace_va_learn_con(tmp_path):
    ghi(tmp_path, ten='learn/RETRIEVAL.md')          # bố cục LEARN/learn/ của /book-to-learn
    rc, out = chay(tmp_path, '--hom-nay', '2026-09-19')
    assert rc == 0, out


def test_khong_co_so_la_ma_2(tmp_path):
    rc, out = chay(tmp_path)
    assert rc == 2
    assert 'không thấy RETRIEVAL.md' in out.lower() or 'KHÔNG THẤY' in out


def test_so_khong_co_bang_la_ma_2(tmp_path):
    rc, out = chay(ghi(tmp_path, '# Sổ trống\n\nChưa có mục nào.\n'))
    assert rc == 2, out
