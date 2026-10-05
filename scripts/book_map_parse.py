# -*- coding: utf-8 -*-
"""Lop DO cua /book-map. Khong biet gi ve HTML.

Moi con so trong tep nay do ngay 2026-10-03 tren 32 cuon co book.md tai
D:/Workshop_X/3_Resources/Books. Xem spec §2.3 de biet ba loi da tra gia.
"""
import io
import re

# Do tren 32 cuon: 27 dung H1, 5 dung H2; dau phan cach co ca "—", ":", "·";
# so chuong co khi khong dem 0 ("Chương 1"); co cuon dung lan hai dau.
CHAP_RE = r'^(#{1,4}) +(?:Chương|Chapter) +(\d{1,3})\b'

# Than chuong cach nhau 200-600 dong; muc luc cuoi sach cach nhau 7-8 dong.
MIN_GAP = 20


def rd(path):
    """Doc UTF-8 TUONG MINH. Mac dinh tren Windows la cp1252."""
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def wc(s):
    """Dem tu kieu `wc -w` o locale UTF-8. KHONG dung che do byte: no thoi
    phong +2,9% (264.885 so voi 257.450 tren usv-thiet-ke-he-thong)."""
    return len(s.split())


def heading_mask(lines):
    """True o dong NGOAI khoi ma.

    BI-1. Trong khoi ma `#` la chu thich chu khong phai tieu de:
    tau-nhom-han-quoc-phong co `# 80% cong viec...` trong so do ASCII, lam
    parser chi thay 37.005 trong 95.731 tu. Loi nay vo 5 cuon.
    """
    out, fence = [], None
    for line in lines:
        m = re.match(r'^\s*(`{3,}|~{3,})', line)
        if m:
            tok = m.group(1)[0] * 3
            if fence is None:
                fence = tok
                out.append(False)
                continue
            if fence == tok:
                fence = None
                out.append(False)
                continue
        out.append(fence is None)
    return out


def chapter_levels(txt):
    """{do_sau: [(so_dong, so_chuong, nguyen_dong)]}. splitlines() chuan hoa
    ca CRLF (4/32 cuon dung CRLF) nen khong con \\r trong nguyen_dong."""
    lines = txt.splitlines()
    mask = heading_mask(lines)
    lv = {}
    for i, line in enumerate(lines):
        if not mask[i]:
            continue
        m = re.match(CHAP_RE, line)
        if m:
            lv.setdefault(len(m.group(1)), []).append((i, int(m.group(2)), line))
    return lv


def pick_level(lv):
    """(depth, hits, warn). Chon muc NONG NHAT: muc luc cuoi sach luon nam
    long sau hon than chuong no liet ke (do that tren ghi-de-quy-trach-nhiem
    8 H1 + 8 H2, va tu-khong-den-mot 19 H2 + 19 H3)."""
    if not lv:
        return None, None, 'khong thay tieu de chuong nao'
    depth = min(lv)
    hits = lv[depth]
    gaps = sorted(b[0] - a[0] for a, b in zip(hits, hits[1:]))
    med = gaps[len(gaps) // 2] if gaps else 10 ** 6
    warn = None
    if med < MIN_GAP:
        warn = ('muc H%d cach nhau trung vi %d dong (< %d) — giong MUC LUC '
                'chu khong phai than chuong' % (depth, med, MIN_GAP))
    return depth, hits, warn
