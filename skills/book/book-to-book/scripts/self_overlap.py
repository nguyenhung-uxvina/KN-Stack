# -*- coding: utf-8 -*-
"""Đo sách phái sinh trùng CHÍNH NÓ — chuỗi giống nhau giữa các chương, và trong một chương.

🔴 Vì sao tệp này phải tồn tại: KHÔNG cổng nào khác trong đường ống đo được đại lượng này.

- `fidelity_audit.py` đếm chuỗi trùng với **sách nguồn**. Hai chương cùng chép một câu của nguồn
  thì nó thấy một vi phạm bao phủ, không thấy rằng người đọc gặp câu ấy hai lần.
- `kiem_ngan_sach_trich.py` cộng **theo từng chương**. Ba chương cùng khai một câu ⇒ đếm ba lần,
  và cả ba đều "đạt".
- Phép kiểm tệp kèm trích hai chiều chứng minh *thân khớp sidecar*, không chứng minh gì về trùng lặp.
- Người viết từng chương **không thể** thấy: mỗi agent chỉ đọc chương của mình.

Đo thật trên `usv-thiet-ke-he-thong` (28 chương, 201k từ, 2026-09-30): một người soát dải Ch.20–24
băm tay và tìm ra **15 cặp trùng nguyên văn toàn sách**, trong đó nặng nhất không phải trích tiếng
Anh mà là **một đoạn văn tiếng Việt 27 từ** xuất hiện ở hai chương cách nhau bốn chương, khác nhau
chỉ ở mỹ phẩm. Và một câu của nguồn có mặt ở **ba** chương, cộng một chương trích lại chính nó.

Phân biệt hai loại, vì cách sửa khác nhau:
- **trích nguồn** (chủ yếu ASCII): hai chương cùng dẫn một câu ⇒ chọn một chương giữ, chương kia
  đổi thành diễn giải. Việc này còn hạ được bao phủ ở P7.
- **văn người biên soạn** (có dấu tiếng Việt): tác giả tự lặp lại mình ⇒ viết lại, hoặc trỏ chéo.

Chuỗi xuất hiện ở NHIỀU chương (≥ `--khuon`) được gom riêng thành **khuôn mẫu** thay vì liệt kê
từng cặp: nhãn bắt buộc, dấu bản nội bộ, tiêu đề mục lặp lại theo quy ước. Ngưỡng ấy đo được chứ
không phải một danh sách miễn trừ chép tay — danh sách chép tay thì che mất đúng thứ cần nhìn.

Dùng:
    python self_overlap.py <thu_muc_chuong>
    python self_overlap.py <thu_muc_chuong> --n 12 --khuon 5
    python self_overlap.py <thu_muc_chuong> --ra bao_cao.md

Mã thoát: 0 = không cặp nào · 1 = có cặp trùng · 2 = không đo được (không thấy chương).
"""
from __future__ import annotations

import argparse
import glob
import io
import os
import re
import sys
import unicodedata
from collections import defaultdict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DAU_TV = 'àáâãèéêìíòóôõùúýăđĩũơưạảấầẩẫậắằẳẵặẹẻẽếềểễệỉịọỏốồổỗộớờởỡợụủứừửữựỳỵỷỹ'


def go_khoi(s: str) -> str:
    """Bỏ frontmatter và mọi khối ```…``` — quy ước đo của cuốn sách (xem dem_tu.py).

    Khối mã bị bỏ vì chúng chứa sơ đồ Mermaid và Công cụ tính, vốn CỐ Ý giống nhau giữa các
    chương; tính chúng vào thì báo cáo đầy trùng lặp hợp lệ và không ai đọc nữa.
    """
    if s.startswith('---'):
        h = s.find('\n---', 3)
        if h > 0:
            s = s[h + 4:]
    return re.sub(r'```.*?```', ' ', s, flags=re.S)


def tach_tu(s: str):
    """→ [(từ đã chuẩn hoá, vị trí dòng)]. Giữ dấu tiếng Việt: cần nó để phân loại về sau."""
    s = unicodedata.normalize('NFC', s)
    ra = []
    for i, dong in enumerate(s.split('\n'), 1):
        d = re.sub(r'[*_`>#|\[\]()]', ' ', dong).lower()
        for t in re.findall(r'[0-9a-z' + DAU_TV + r']+', d):
            ra.append((t, i))
    return ra


def la_tieng_viet(chuoi: str) -> bool:
    return any(c in DAU_TV for c in chuoi)


def gop_mach(cap):
    """Gộp các cửa sổ chồng nhau thành MẠCH dài nhất.

    Không gộp thì một đoạn trùng 27 từ hiện ra thành 16 cửa sổ 12-từ chồng nhau, và báo cáo
    đọc như 16 lỗi khác nhau — vừa thổi phồng số lượng vừa giấu mất độ dài thật, mà độ dài
    mới là thứ quyết định nặng nhẹ.
    """
    cap = sorted(cap)
    ra = []
    for a, b in cap:
        if ra and a == ra[-1][1] + 1 and b == ra[-1][3] + 1:
            ra[-1][1], ra[-1][3] = a, b
        else:
            ra.append([a, a, b, b])
    return ra


def main(argv=None):
    ap = argparse.ArgumentParser(description='Do sach phai sinh trung chinh no')
    ap.add_argument('thumuc')
    ap.add_argument('--n', type=int, default=12, help='so tu lien tiep tinh la trung (mac dinh 12)')
    ap.add_argument('--khuon', type=int, default=5,
                    help='chuoi co mat o >= bao nhieu chuong thi coi la KHUON MAU (mac dinh 5)')
    ap.add_argument('--ra', help='ghi bao cao markdown ra tep')
    a = ap.parse_args(argv)

    teps = sorted(glob.glob(os.path.join(a.thumuc, 'Ch*.md')))
    teps = [t for t in teps if not os.path.basename(t).startswith('_')]
    if not teps:
        print('KHONG DO DUOC: khong thay tep chuong Ch*.md trong %s' % a.thumuc)
        return 2

    tu, ten = {}, {}
    for t in teps:
        k = os.path.basename(t)[:4]
        ten[k] = os.path.basename(t)
        tu[k] = tach_tu(go_khoi(io.open(t, encoding='utf-8').read()))

    # băm mọi cửa sổ n-từ
    bam = defaultdict(list)
    for k, ws in tu.items():
        chu = [w for w, _ in ws]
        for i in range(len(chu) - a.n + 1):
            bam[' '.join(chu[i:i + a.n])].append((k, i))

    khuon, cap_ch = [], defaultdict(list)
    for chuoi, vt in bam.items():
        if len(vt) < 2:
            continue
        chuong = {k for k, _ in vt}
        if len(chuong) >= a.khuon:
            khuon.append((chuoi, len(chuong), len(vt)))
            continue
        for x in range(len(vt)):
            for y in range(x + 1, len(vt)):
                (k1, i1), (k2, i2) = vt[x], vt[y]
                if k1 == k2 and abs(i1 - i2) < a.n:
                    continue                      # cùng chương, cửa sổ tự chồng
                key = (k1, k2) if k1 <= k2 else (k2, k1)
                cap_ch[key].append((i1, i2) if key == (k1, k2) else (i2, i1))

    kq = []
    for (k1, k2), cap in cap_ch.items():
        for a1, a2, b1, b2 in gop_mach(cap):
            dai = a2 - a1 + a.n
            noi_dung = ' '.join(w for w, _ in tu[k1][a1:a2 + a.n])
            kq.append({
                'c1': k1, 'c2': k2, 'dai': dai,
                'dong1': tu[k1][a1][1], 'dong2': tu[k2][b1][1],
                'chuoi': noi_dung,
                'loai': 'VIỆT' if la_tieng_viet(noi_dung) else 'ANH',
                'tu_lap': k1 == k2,
            })
    kq.sort(key=lambda r: -r['dai'])

    d = ['=' * 78, 'TRUNG CHINH NO — %d chuong, cua so %d tu' % (len(teps), a.n), '=' * 78]
    viet = [r for r in kq if r['loai'] == 'VIỆT']
    anh = [r for r in kq if r['loai'] == 'ANH']
    lap = [r for r in kq if r['tu_lap']]
    d += ['  mach trung: %d  (VIET %d · ANH %d · tu lap trong mot chuong %d)'
          % (len(kq), len(viet), len(anh), len(lap)),
          '  khuon mau bo qua: %d chuoi (co mat o >= %d chuong)' % (len(khuon), a.khuon), '']
    if kq:
        d += ['%-5s %-5s %5s %-6s %s' % ('ch', 'ch', 'tu', 'loai', 'chuoi'), '-' * 78]
        for r in kq[:60]:
            d.append('%-5s %-5s %5d %-6s %s' % (
                r['c1'] + (':%d' % r['dong1']), r['c2'] + (':%d' % r['dong2']),
                r['dai'], r['loai'], r['chuoi'][:52]))
    print('\n'.join(d))
    print('-' * 78)
    if kq:
        print('  Doc theo LOAI, vi cach sua khac nhau:')
        print('    ANH  = hai chuong cung dan mot cau cua nguon -> chon MOT chuong giu,')
        print('           chuong kia doi thanh dien giai. Viec nay con ha bao phu o P7.')
        print('    VIET = tac gia tu lap lai minh -> viet lai, hoac tro cheo.')
        print('  Do dai mach quan trong hon so luong mach.')
    else:
        print('  Khong mach nao. LUU Y: ket qua rong chi co nghia neu --n hop ly;')
        print('  --n qua lon thi moi sach deu "sach".')

    if a.ra:
        with io.open(a.ra, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# Trùng chính nó — %d chương, cửa sổ %d từ\n\n' % (len(teps), a.n))
            f.write('| ch A | dòng | ch B | dòng | từ | loại | chuỗi |\n|---|--:|---|--:|--:|---|---|\n')
            for r in kq:
                f.write('| %s | %d | %s | %d | %d | %s | %s |\n' % (
                    r['c1'], r['dong1'], r['c2'], r['dong2'], r['dai'], r['loai'],
                    r['chuoi'][:90].replace('|', '\\|')))
            if khuon:
                f.write('\n## Khuôn mẫu đã bỏ qua (≥ %d chương)\n\n' % a.khuon)
                for c, nch, n in sorted(khuon, key=lambda x: -x[1])[:40]:
                    f.write('- %d chương, %d lần: `%s`\n' % (nch, n, c[:90]))
        print('  bao cao: %s' % a.ra)

    return 1 if kq else 0


if __name__ == '__main__':
    sys.exit(main())
