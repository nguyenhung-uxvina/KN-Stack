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


# ---------- từ khoá kích hoạt không giẫm lên skill khác ----------
import glob as _glob

# Từ quá chung (kéo skill vào mọi câu hỏi) hoặc tên skill có sẵn của Claude Code.
CAM = {'explain', 'giải thích', 'journal', 'schedule', 'practice', 'rubric', 'how am i doing',
       'learning path', 'how to learn', 'lộ trình', 'lộ trình học', 'study plan', 'plan my',
       'loop', 'review', 'plan', 'learn', 'học'}


def _mo_ta():
    out = {}
    for f in _glob.glob(os.path.join(ROOT, 'skills', '**', 'SKILL.md'), recursive=True) + \
            _glob.glob(os.path.join(ROOT, 'plugins', '**', 'SKILL.md'), recursive=True):
        t = open(f, encoding='utf-8', errors='replace').read()
        m = re.search(r'^---\s*\n(.*?)\n---', t, re.S)
        if m:
            out[os.path.basename(os.path.dirname(f))] = ' '.join(m.group(1).split())
    return out


def _tu_khoa(mo_ta):
    """Các cụm trong ngoặc kép/đơn SAU chữ 'Triggers on' — chỉ đó mới là từ khoá kích hoạt."""
    m = re.search(r'Triggers? (?:on|when)\b(.*)', mo_ta, re.I | re.S)
    if not m:
        return set()
    return {x.strip().lower() for x in re.findall(r'["\'‘“]([^"\'’”]{2,60})["\'’”]', m.group(1))}


def test_learn_khong_dung_tu_khoa_qua_chung():
    md = _mo_ta()
    loi = {s: sorted(_tu_khoa(md[s]) & CAM) for s in md if s.startswith('learn-')}
    assert not any(loi.values()), 'từ khoá quá chung / trùng tên skill có sẵn: %s' % {k: v for k, v in loi.items() if v}


def test_learn_khong_trung_tu_khoa_skill_khac():
    md = _mo_ta()
    cua_khac = {}
    for s, d in md.items():
        if not s.startswith('learn-'):
            for k in _tu_khoa(d):
                cua_khac.setdefault(k, []).append(s)
    trung = {s: {k: cua_khac[k] for k in _tu_khoa(md[s]) if k in cua_khac}
             for s in md if s.startswith('learn-')}
    assert not any(trung.values()), 'trùng từ khoá: %s' % {k: v for k, v in trung.items() if v}


def test_learn_methodology_va_practice_track_noi_ranh_gioi():
    """Description phải chỉ sang skill hàng xóm, để bộ định tuyến chọn đúng khi yêu cầu lớn hơn."""
    md = _mo_ta()
    assert '/learning' in md['learn-methodology'] and '/book-to-learn' in md['learn-methodology']
    assert '/schedule' in md['learn-practice'] and '/cycle' in md['learn-practice']
    assert '/journal' in md['learn-track']


# ---------- đường dẫn mà SKILL.md nhắc tới phải tồn tại ----------

def test_duong_dan_script_va_reference_ton_tai():
    """SKILL.md trỏ tới script/reference của skill khác (learn-practice → quote_check của
    learn-methodology). Đổi tên hay dời tệp mà quên sửa chỗ trỏ thì skill hỏng im lặng."""
    thieu = []
    tep = [(s, ('SKILL.md',)) for s in ('learn-methodology', 'learn-practice', 'learn-track', 'learn-teach')]
    tep.append(('learn-teach', ('references', 'SOURCING.md')))
    for s, duong in tep:
        md = _doc(s, *duong)
        for rel in re.findall(r'<KN-Stack>/([\w./-]+\.py)', md):
            if not os.path.isfile(os.path.join(ROOT, rel)):
                thieu.append((s, rel))
        for sk, ref in re.findall(r'`([\w-]+):references:([\w-]+)`', md):
            # skill được tham chiếu có thể ở domain khác (vd. research ở skills/galaxy/)
            if not _glob.glob(os.path.join(ROOT, '*', '**', sk, 'references', ref + '.md'), recursive=True):
                thieu.append((s, '%s:references:%s' % (sk, ref)))
    assert not thieu, thieu
