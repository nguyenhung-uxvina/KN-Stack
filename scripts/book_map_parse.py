# -*- coding: utf-8 -*-
"""Lop DO cua /book-map. Khong biet gi ve HTML.

Measurements tren corpus (2026-10-05, 34 cuon co book.md tai
D:/Workshop_X/3_Resources/Books): cac so trong tep nay do va kiem chung tren
tap hien tai. Xem spec §2.3 de biet ba loi da tra gia.
"""
import io
import re

# Do that tren 34 cuon: 29 dung H1, 5 dung H2. Dau phan cach co ca "—", ":", "·";
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
    parser chi thay 37.005 trong 95.731 tu. Loi nay vo 5 cuon. Corpus-wide
    (2026-10-05, 34 cuon): 305 dong matching ^#{1,4} +\\S nam trong khoi ma.
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
    ca CRLF (3 cuon trong 34 dung CRLF, 2026-10-05) nen khong con \\r trong
    nguyen_dong."""
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


TITLE_RE = r'^#+ +(?:Chương|Chapter) +\d{1,3} *[—:·-]? *'


def parse_chapters(txt):
    """{'chapters': {num: {...}}, 'depth', 'warn', 'dups'}.

    BI-2. Chuong dung o tieu de ke tiep theo luat PHU THUOC DO SAU:
      depth==1: H1 la muc dinh => trong chuong khong the co H1. Dung o H1 ke tiep.
      depth>1 : co sach dung CUNG muc cho ca chuong lan tieu muc
                (principles-ba-tai-san: `## Chương 01:` va `## Kinh nghiem...`).
                Chi dung o tieu de NONG HON, hoac o chuong ke tiep.
    De chuong cuoi chay den EOF lam no hut ca phu luc: tu-khong-den-mot Ch.19
    phinh +50%, ghi-de-quy-trach-nhiem Ch.08 +49%.
    """
    depth, hits, warn = pick_level(chapter_levels(txt))
    if not hits:
        return {'chapters': {}, 'depth': None, 'warn': warn, 'dups': []}

    lines = txt.splitlines()
    mask = heading_mask(lines)
    chap_lines = set(h[0] for h in hits)
    if depth == 1:
        stop = [i for i, L in enumerate(lines)
                if mask[i] and re.match(r'^# +\S', L)]
    else:
        stop = [i for i, L in enumerate(lines)
                if i in chap_lines
                or (mask[i] and re.match(r'^#{1,%d} +\S' % (depth - 1), L))]

    chapters, seen, dups, dup_count = {}, set(), [], {}
    for ln, num, head in hits:
        nxt = [i for i in stop if i > ln]
        end = nxt[0] if nxt else len(lines)
        body = '\n'.join(lines[ln + 1:end])
        key = num
        if num in seen:
            # Khong ghi de im lang: giu ca hai duoi khoa phu, va bao ra.
            if num not in dups:
                dups.append(num)
            if num not in dup_count:
                dup_count[num] = 1
            else:
                dup_count[num] += 1
            # Use fractional offset: k-th dup of num gets num + k/1000.0
            # This keeps keys strictly inside (num, num+1), so no collision with int chapters
            key = num + dup_count[num] / 1000.0
        seen.add(num)
        # Safety: never overwrite an existing key
        assert key not in chapters, "Key collision at %s — duplicate handling failed" % key
        chapters[key] = {
            'title': re.sub(TITLE_RE, '', head).strip(),
            'words': wc(head) + wc(body),
            'mermaid': len(re.findall(r'^```mermaid', body, re.M)),
            'body': body,
            'line': ln + 1}
    return {'chapters': chapters, 'depth': depth, 'warn': warn, 'dups': dups}


def coverage(parsed, txt):
    """BI-5. So tong tu trong chuong voi `wc -w` CA TEP — mot tong tinh NGOAI
    duong ong. Hai cam bien chi so cac chuong voi nhau (trung vi qua nho,
    chuong cuoi phinh) bo sot 4/5 ca loi L3; cam bien nay bat 5/5.
    pahl-beitz-tap2 nam o 40% phu ma hai cam bien kia bao 'sach'."""
    whole = wc(txt)
    if not whole:
        return 0.0
    return sum(c['words'] for c in parsed['chapters'].values()) / float(whole)


REF_RE = r'(?:Chương|Chapter|Ch\.) *(\d{1,3})'


def crossrefs(parsed):
    """{num: [num khac]}. Chi giu canh tro den chuong CO THAT trong sach —
    `Chương 99` trong mot cuon 28 chuong la mot cach noi, khong phai canh."""
    ch = parsed['chapters']
    edges = {}
    for n, d in ch.items():
        tgt = set()
        for m in re.finditer(REF_RE, d['body']):
            y = int(m.group(1))
            if y in ch and y != n:
                tgt.add(y)
        edges[n] = sorted(tgt)
    return edges


SCOPE_FALLBACK = '⛔ PHẠM VI CHƯA KHAI — coi như NỘI BỘ'

_SIDE_SCOPE_RE = r'\*\*phạm vi phát hành: ([^*]+?)\*\*'
_FIDELITY_RE = r'\*\*mức nguyên bản: (\w+)\*\*'

# Keywords that mark a scope declaration (case-insensitive)
_SCOPE_KEYWORDS = r'(?:phạm vi|phát hành|lưu hành|phân loại|nội bộ)'


def read_scope(book_txt, scope_txt=None):
    """(nhan, muc_nguyen_ban, nguon). Thu tu doc, dung o nguon dau tien.

    BI-4. Than sach la nguon CHINH. Do that tren 34 cuon co book.md tai
    D:/Workshop_X/3_Resources/Books (2026-10-05): 23 khai pham vi trong THAN,
    0 tu sidecar (all 5 co _scope_decision.md cung khai trong than), 11 khong
    khai (8 ko co NỘI BỘ, 3 chi co trong prose). Vi the than sach la uu tien.
    SCOPE_FALLBACK in khi khong khai: tien le do duoc tren ban EPUB dau cua
    10x-easier-than-2x (nhan o frontmatter, 0/70 tep trong zip chua chu ay).
    """
    fid = '?'
    if scope_txt:
        m = re.search(_FIDELITY_RE, scope_txt)
        if m:
            fid = m.group(1)

    lines = book_txt.splitlines()
    mask = heading_mask(lines)

    # Find front matter: search only before first chapter heading
    front_matter_end = len(lines)
    lv = chapter_levels(book_txt)
    if lv:
        depth, hits, _ = pick_level(lv)
        if hits:
            front_matter_end = hits[0][0]

    # Search front matter for scope declaration in headings or blockquotes
    for i in range(front_matter_end):
        line = lines[i]
        if not mask[i]:
            continue

        # Check if this is a heading or blockquote line that matches scope keywords
        is_heading = re.match(r'^#+\s+', line)
        is_blockquote = re.match(r'^>\s*', line)

        if (is_heading or is_blockquote) and re.search(_SCOPE_KEYWORDS, line, re.IGNORECASE):
            # Extract text without leading symbols
            text = re.sub(r'^#+\s+|^>\s*', '', line).strip()
            if text:  # Only if non-empty
                # Check for blockquote on next line (prefer it over heading)
                for nxt in lines[i + 1:min(i + 5, front_matter_end)]:
                    if re.match(r'^>\s*', nxt) and re.search(_SCOPE_KEYWORDS, nxt, re.IGNORECASE):
                        text = re.sub(r'^>\s*', '', nxt).strip()
                        break
                return text, fid, 'than-sach'

    # Fall back to sidecar (only if it has a non-empty scope declaration)
    if scope_txt:
        m = re.search(_SIDE_SCOPE_RE, scope_txt)
        if m:
            label = m.group(1).strip()
            if label:  # F1: must not return empty label
                return label, fid, 'sidecar'

    return SCOPE_FALLBACK, fid, 'bao-toan'


ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
         'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}

_OUT_CHAP_RE = r'^#{2,4} +(?:Ch\.|Chương |Chapter )(\d{1,3}) *[—:·-] *(.*)$'


def parse_outline(txt):
    """{num: {...}} tu Phase3-Outline.md. LOP LAM GIAU — thieu truong nao thi
    de trong, KHONG bia va KHONG suy luan.

    Khuon khong nhat quan: 26 cua 34 cuon co heading `### `, 8 khong (2026-10-05).
    Bullet availability: corpus-wide 488 / 521 chuong (94%) co bullet, nhung
    usv-thiet-ke-he-thong chi 13 / 28. Bullet nay khong phai tom tat (120-150
    ky + dot clauses + page citations), chi la lieu tham khao. Vi vay o tom tat
    KHONG thu hoach duoc tu day — xem spec §1.2.
    """
    ch, part, cur = {}, None, None
    for line in txt.splitlines():
        m = re.match(r'^## +Phần ([IVX]+) *—? *(.*)$', line)
        if m:
            part = (ROMAN.get(m.group(1), 0), m.group(2).strip())
            continue
        m = re.match(_OUT_CHAP_RE, line)
        if m:
            n = int(m.group(1))
            cur = ch[n] = {
                'title': re.sub(r'⟵.*$', '', m.group(2)).strip(),
                'part': part, 'bullets': [], 'risk': '', 'red': False,
                'figs': 0, 'target': 0, 'neo': '', 'new': '⟵' in m.group(2)}
            continue
        if cur is None:
            continue
        if line.startswith('**Neo**') or line.startswith('**Trích**'):
            m = re.search(r'\*\*Từ\*\* *([\d.]+)', line)
            if m:
                cur['target'] = int(m.group(1).replace('.', ''))
            m = re.search(r'\*\*Neo\*\* *(N\d(?: *[·+] *N\d)*)', line)
            if m:
                cur['neo'] = m.group(1)
            continue
        m = re.match(r'^Hình \((\d+)\)', line)
        if m:
            cur['figs'] = int(m.group(1))
            continue
        m = re.match(r'^Rủi ro: *(.*)$', line)
        if m:
            cur['risk'] = m.group(1).strip()
            cur['red'] = '🔴' in line
            continue
        if line.startswith('- '):
            cur['bullets'].append(line[2:].strip())
        elif (line.startswith('  ') and cur['bullets'] and line.strip()
              and not line.lstrip().startswith('- ')):
            cur['bullets'][-1] += ' ' + line.strip()
    return ch


def maybe(path, fn, default):
    """Doc tep neu co, tra `default` neu khong. Lop lam giau khong duoc lam
    sap ca lan chay chi vi thieu mot tep tuy chon."""
    try:
        return fn(rd(path))
    except (OSError, UnicodeDecodeError):
        return default
