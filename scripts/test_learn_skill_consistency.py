# -*- coding: utf-8 -*-
"""Test nhất quán cho các skill learn-* — những lỗi "trông đúng khi liếc qua".

Chạy: python -m pytest scripts/test_learn_skill_consistency.py -v

Ba lỗi dưới đây đã nằm trong skill mà không ai thấy, vì đọc lướt thì đúng:
  1. Lịch mẫu của learn-practice vi phạm chính luật 1 của nó (A→A, B→B ở tuần 1).
  2. learn-practice gọi DMIR là định dạng viết yêu cầu (DMIR = Diagnose–Model–Intervene–Reflect).
  3. learn-methodology và learn-teach dùng hai thang ôn giãn cách khác nhau.
Regex eval chỉ kiểm được "có chữ X"; mấy test này kiểm được "đúng luật".
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARN = os.path.join(ROOT, 'skills', 'learn')


def _doc(*p):
    with open(os.path.join(LEARN, *p), encoding='utf-8') as f:
        return f.read()


def _cac_buoi(skill_md):
    """Chuỗi buổi của lịch mẫu theo thứ tự thời gian: [('Mon AM', 'A'), ('Mon PM', 'A+B'), ...]."""
    khoi = re.search(r'### Schedule Template.*?```(.*?)```', skill_md, re.S).group(1)
    buoi = []
    for dong in khoi.splitlines():
        for nhan, noi_dung in re.findall(r'(\w{3} [AP]M):\s*(.*?)(?=\s{2,}\w{3} [AP]M:|$)', dong):
            if 'Mixed 3-topic' in noi_dung:
                chu_de = 'A+B+C'
            else:
                m = re.search(r'(?:Topic|Mixed)\s+([A-C](?:\+[A-C])*)', noi_dung)
                chu_de = m.group(1) if m else None
            buoi.append((nhan, chu_de))
    return buoi


def test_lich_mau_co_du_ba_tuan_co_buoi():
    buoi = _cac_buoi(_doc('learn-practice', 'SKILL.md'))
    assert len(buoi) == 18, buoi          # tuần 1–3 × 6 buổi; tuần 4 không có chủ đề
    assert all(c for _, c in buoi), buoi


def test_luat_1_khong_hai_buoi_don_lien_nhau_cung_chu_de():
    """Luật 1: cùng một chủ đề ĐƠN không ở hai buổi liền nhau, kể cả qua ngày/tuần.
    Buổi trộn được đứng cạnh chủ đề của chính nó (luật 1 ghi rõ ngoại lệ này)."""
    buoi = _cac_buoi(_doc('learn-practice', 'SKILL.md'))
    vi_pham = [(a, b) for a, b in zip(buoi, buoi[1:])
               if '+' not in a[1] and '+' not in b[1] and a[1] == b[1]]
    assert not vi_pham, 'lịch mẫu vi phạm luật 1: %s' % vi_pham


def test_moi_chu_de_duoc_hoc_moi_tuan_1():
    buoi = _cac_buoi(_doc('learn-practice', 'SKILL.md'))[:6]
    assert {c for _, c in buoi if '+' not in c} == {'A', 'B', 'C'}, buoi


def test_dmir_khong_phai_dinh_dang_viet_yeu_cau():
    md = _doc('learn-practice', 'SKILL.md')
    dong = [d for d in md.splitlines() if 'Requirements writing' in d]
    assert dong, 'mất mục Requirements writing'
    assert all('DMIR' not in d for d in dong), dong
    assert any('ODI' in d for d in dong), dong


def _thang(md):
    m = re.search(r'\*\*\s*1\s*·\s*3\s*·\s*7\s*·\s*16\s*·\s*35\s*(?:days|ngày)\s*\*\*', md)
    return m.group(0) if m else None


def test_mot_thang_on_cho_ca_hai_skill():
    teach = _doc('learn-teach', 'references', 'RETRIEVAL.md')
    meth = _doc('learn-methodology', 'SKILL.md')
    assert _thang(teach), 'RETRIEVAL.md đổi thang ôn — cập nhật learn-methodology cho khớp'
    assert _thang(meth), 'learn-methodology không dùng thang 1·3·7·16·35 của learn-teach'
    assert 'Day 21' not in meth, 'còn sót thang cũ 0·1·3·7·21'
    assert re.search(r'down two rungs', meth), 'thiếu luật trượt lùi hai bậc'
