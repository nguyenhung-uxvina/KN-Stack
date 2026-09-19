# -*- coding: utf-8 -*-
"""Test cho skills/learn/learn-methodology/scripts/quote_check.py.

Chạy: python -m pytest scripts/test_learn_quote_check.py -v

Mỗi test gắn với một cách mà cổng trích dẫn có thể báo SAI mà không ai thấy:
âm tính giả (trích đúng mà báo không thấy) làm người dùng tắt cổng; dương tính
giả (trích sai mà báo thấy) làm cổng thành trang trí. Hai nhóm dưới đây canh
hai chiều đó.
"""
import importlib.util
import os
import subprocess
import sys
import unicodedata

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'skills', 'learn', 'learn-methodology', 'scripts', 'quote_check.py')

spec = importlib.util.spec_from_file_location('quote_check', SCRIPT)
qc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qc)

SACH = (
    "Chapter 3. The conceptual design phase determines the principle solution.\n"
    "A charge amplifier converts the charge from a piezoelectric sensor into a voltage.\n"
    "The safety factor shall be 7.5 for all lifting points.\n"
    "Thiết kế ý tưởng xác định nguyên lý giải pháp trước khi chọn kích thước.\n"
)


# Nguồn thật luôn dài hơn ngưỡng "gần như rỗng" (20 từ); đệm để test đo đúng thứ nó muốn đo.
DEM = '\n' + 'Filler prose about unrelated matters keeps this fixture realistic in length. ' * 3


def chay(tmp_path, dau_ra, nguon_text=SACH, ten='sach.md', them=()):
    if nguon_text.strip():
        nguon_text += DEM
    src = tmp_path / ten
    src.write_text(nguon_text, encoding='utf-8')
    out = tmp_path / 'out.md'
    out.write_text(dau_ra, encoding='utf-8')
    cmd = [sys.executable, SCRIPT, str(out), '--nguon', str(src), *them]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    return p.returncode, p.stdout + p.stderr


# ---------- trích đúng phải được thấy (chặn âm tính giả) ----------

def test_trich_dung_nguyen_van(tmp_path):
    rc, out = chay(tmp_path, 'Ý cốt lõi. «A charge amplifier converts the charge from a piezoelectric sensor» [ch3]')
    assert rc == 0, out
    assert 'sach.md' in out


def test_nhay_cong_gach_dai_va_hoa_thuong(tmp_path):
    src = 'He said “the design—once frozen—is final” in 1999.'
    rc, out = chay(tmp_path, '«He said "the design-once frozen-is final"»', nguon_text=src)
    assert rc == 0, out


def test_gach_noi_ngat_dong_cua_pdf(tmp_path):
    src = 'The conceptual de-\nsign phase determines the principle solution.'
    rc, out = chay(tmp_path, '«The conceptual design phase determines the principle»', nguon_text=src)
    assert rc == 0, out


def test_tieng_viet_nfd_trong_nguon_nfc_trong_trich(tmp_path):
    src = unicodedata.normalize('NFD', SACH)
    rc, out = chay(tmp_path, '«Thiết kế ý tưởng xác định nguyên lý giải pháp»', nguon_text=src)
    assert rc == 0, out


def test_trich_nhieu_dong(tmp_path):
    rc, out = chay(tmp_path, '«A charge amplifier converts\nthe charge from a piezoelectric sensor»')
    assert rc == 0, out


def test_dau_ba_cham_tach_doan_ca_hai_deu_co(tmp_path):
    rc, out = chay(tmp_path, '«The conceptual design phase determines […] the principle solution»')
    assert rc == 0, out


# ---------- trích sai phải bị bắt (chặn dương tính giả) ----------

def test_sai_mot_tu(tmp_path):
    rc, out = chay(tmp_path, '«A charge amplifier converts the current from a piezoelectric sensor»')
    assert rc == 1
    assert 'KHÔNG THẤY' in out


def test_sai_so_thap_phan(tmp_path):
    """7.5 → 7,5 phải trượt: chuẩn hoá kiểu xoá dấu câu biến cả hai thành '7 5'."""
    rc, out = chay(tmp_path, '«The safety factor shall be 7,5 for all lifting points»')
    assert rc == 1, out


def test_mat_dau_thap_phan(tmp_path):
    rc, out = chay(tmp_path, '«The safety factor shall be 75 for all lifting points»')
    assert rc == 1, out


def test_sai_dau_tieng_viet(tmp_path):
    """Chuẩn hoá kiểu [^a-z0-9] xoá mọi chữ có dấu nên 'lý' và 'lỹ' đều thành rỗng."""
    rc, out = chay(tmp_path, '«Thiết kế ý tưởng xác định nguyên lỹ giải pháp»')
    assert rc == 1, out


def test_dau_ba_cham_mot_doan_bia(tmp_path):
    rc, out = chay(tmp_path, '«The conceptual design phase determines … the final dimensions»')
    assert rc == 1, out


def test_trich_qua_ngan_khong_chung_minh_gi(tmp_path):
    rc, out = chay(tmp_path, '«design phase»')
    assert rc == 1
    assert 'QUÁ NGẮN' in out


def test_khong_co_trich_dan_nao(tmp_path):
    rc, out = chay(tmp_path, 'Feynman: bộ khuếch đại điện tích giống cái xô hứng mưa.')
    assert rc == 1
    assert 'không có trích dẫn' in out.lower()


# ---------- không đo được thì phải nói là không đo được ----------

def test_nguon_rong_la_ma_2(tmp_path):
    rc, out = chay(tmp_path, '«A charge amplifier converts the charge»', nguon_text='   \n')
    assert rc == 2, out


def test_nguon_khong_ton_tai_la_ma_2(tmp_path):
    out = tmp_path / 'out.md'
    out.write_text('«A charge amplifier converts the charge»', encoding='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, str(out), '--nguon', str(tmp_path / 'khong-co.pdf')],
                       capture_output=True, text=True, encoding='utf-8')
    assert p.returncode == 2


# ---------- vị trí ----------

def test_thu_muc_nhieu_chuong_bao_dung_tep(tmp_path):
    d = tmp_path / '_source'
    d.mkdir()
    (d / 'ch01-mo-dau.md').write_text('Nothing relevant lives in this opening chapter at all.', encoding='utf-8')
    (d / 'ch02-y-tuong.md').write_text(SACH, encoding='utf-8')
    out = tmp_path / 'out.md'
    out.write_text('«The safety factor shall be 7.5 for all lifting points»', encoding='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, str(out), '--nguon', str(d)],
                       capture_output=True, text=True, encoding='utf-8')
    assert p.returncode == 0, p.stdout
    assert 'ch02-y-tuong.md' in p.stdout
    assert 'ch01-mo-dau.md' not in p.stdout.split('Tổng')[0]


def _pdf_hai_trang(path, trang1, trang2):
    fitz = pytest.importorskip('fitz')
    doc = fitz.open()
    for t in (trang1, trang2):
        page = doc.new_page()
        # đệm TRƯỚC trang 1 và SAU trang 2 để đoạn cần tìm vẫn vắt đúng qua ranh giới trang
        t = (DEM + t) if t is trang1 else (t + DEM)
        page.insert_textbox(fitz.Rect(50, 50, 550, 800), t, fontsize=11)
    doc.save(str(path))


def test_pdf_bao_trang_pdf(tmp_path):
    pdf = tmp_path / 'sach.pdf'
    _pdf_hai_trang(pdf, 'Opening page with unrelated words only here.',
                   'The safety factor shall be 7.5 for all lifting points.')
    out = tmp_path / 'out.md'
    out.write_text('«The safety factor shall be 7.5 for all lifting points»', encoding='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, str(out), '--nguon', str(pdf)],
                       capture_output=True, text=True, encoding='utf-8')
    assert p.returncode == 0, p.stdout
    assert 'trang PDF 2' in p.stdout


def test_pdf_trich_vat_qua_hai_trang(tmp_path):
    pdf = tmp_path / 'sach.pdf'
    _pdf_hai_trang(pdf, 'The conceptual design phase', 'determines the principle solution.')
    out = tmp_path / 'out.md'
    out.write_text('«The conceptual design phase determines the principle solution»', encoding='utf-8')
    p = subprocess.run([sys.executable, SCRIPT, str(out), '--nguon', str(pdf)],
                       capture_output=True, text=True, encoding='utf-8')
    assert p.returncode == 0, p.stdout
    assert 'trang PDF 1–2' in p.stdout


def test_pdf_doc_bang_hai_thu_vien(tmp_path, monkeypatch):
    """Đo thật 2026-09-19 (Borchert, tr.16): pymupdf bỏ sót cả đoạn mà pypdf đọc được.
    Đọc một thư viện thì trích đúng bị báo KHÔNG THẤY — cổng phải tìm trên hợp của cả hai."""
    pytest.importorskip('fitz')
    pytest.importorskip('pypdf')
    monkeypatch.setattr(qc, '_pdf_fitz', lambda p: ['Only the header survived here. ' + DEM])
    monkeypatch.setattr(qc, '_pdf_pypdf', lambda p: ['The safety factor shall be 7.5 for all lifting points.' + DEM])
    t = qc.Tep(str(tmp_path / 'x.pdf'))
    assert t.tim(qc.norm('The safety factor shall be 7.5 for all lifting points'), False) == 'x.pdf, trang PDF 1'


# ---------- hàm chuẩn hoá ----------

def test_norm_giu_so_thap_phan_bo_dau_cau_cuoi():
    assert qc.norm('Factor 7.5.') == 'factor 7.5'
    assert qc.norm('1,200 units, then') == '1,200 units then'
    assert qc.norm('-3.2 m') == '-3.2 m'
