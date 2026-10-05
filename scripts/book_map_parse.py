# -*- coding: utf-8 -*-
"""Lop DO cua /book-map. Khong biet gi ve HTML.

Measurements tren corpus (2026-10-05, 34 cuon co book.md tai
D:/Workshop_X/3_Resources/Books): cac so trong tep nay do va kiem chung tren
tap hien tai. Xem spec §2.3 de biet ba loi da tra gia.
"""
import io
import re

# Do that (2026-10-05, 34 cuon): 29 dung H1, 5 dung H2. Dau phan cach co ca "—", ":", "·";
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


def stray_headings(parsed):
    """Dem tieu de (ngoai khoi ma) con SOT trong THAN mot chuong du le ra
    phai lam dut chuong do — mot dieu kien CAU TRUC, khong phai thong ke.

    Fix round 1 (2026-10-05): cam bien ty le 'chuong cuoi / trung vi'
    (BLOAT_WARN=1.8x o md_to_html.py) KHONG tach duoc loi EOF-overrun nay.
    Do that tren tu-khong-den-mot: loi THAT (chuong cuoi chay den EOF, hut
    phu luc) do duoc ti le 1.49x trung vi — nam NGAY GIUA hai chuong cuoi
    DAI THAT, khong phai loi (mot cuon khac 1.61x, mot cuon nua 1.48x).
    Khong co nguong nao tren ty le do tach duoc ca ba: nguong phai < 1.49
    (de bat loi) VA > 1.61 (de im voi chuong dai THAT) cung luc — hai dieu
    kien nay mau thuan nhau, cam bien thong ke vo nghia o day. (Nguong
    1.8x duoc nang tu 1.5x truoc do CHINH VI finding-alphas 1.61x, tuc la
    hanh dong sua false-positive da lam cam bien mu voi true-positive.)

    Thay bang dieu kien CAU TRUC theo dung hai nhanh cua BI-2 (`depth` =
    muc chuong do pick_level chon):
      depth == 1: KHONG tieu de H1 (`^# `) nao duoc nam trong than chuong —
                  H1 la muc dinh, moi H1 deu la mot diem dung hop le.
      depth  > 1: CHI tieu de NONG HON depth (level < depth) la vi pham.
                  Tieu de CUNG muc (level == depth) la tieu muc hop phap —
                  principles-ba-tai-san dung H2 cho CA chuong LAN tieu muc;
                  dem ca tieu de cung muc se ra 91 vi pham GIA tren chinh
                  cuon do (do that).
    Di qua heading_mask() truoc khi dem: mot `#` trong khoi ma (vd so do
    ASCII) KHONG duoc tinh la tieu de.

    Fix round 2 (2026-10-06): loi L1 lich su la "CHI chuong CUOI chay den
    EOF" (mot chuong, khong lam vo chuong giua). Duoi dang HEP, dung dang
    cua loi do, cam bien nay tra ve 4 tren tu-khong-den-mot, 3 tren
    ghi-de-quy-trach-nhiem, va 0 tren cac cuon khong co phu luc de hut —
    vd usv-thiet-ke-he-thong, bloat ratio chi 1.08x nen khong co gi de
    chuong cuoi "hut" ca; 0 o day la DUNG, khong phai bo sot. Mot dang
    RONG hon (ca luat dung bien mat, lam chuong GIUA cung vo — xem
    test_negative_eof_broad_real_file) cho so cao hon (10/6/6/0) vi do la
    mot loi NANG HON loi L1 thuc; dung de minh hoa cam bien van bat duoc
    loi nang hon, khong phai chu ky cua L1.
    """
    depth = parsed['depth']
    if not depth:
        return 0
    total = 0
    for c in parsed['chapters'].values():
        lines = c['body'].splitlines()
        mask = heading_mask(lines)
        for i, line in enumerate(lines):
            if not mask[i]:
                continue
            m = re.match(r'^(#+) +\S', line)
            if not m:
                continue
            level = len(m.group(1))
            violation = (level == 1) if depth == 1 else (level < depth)
            if violation:
                total += 1
    return total


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

# Fix round 1 (2026-10-05): tu PHAN LOAI THAT — khong phai moi dong "trong
# muc scope keyword" deu la mot loi khai bao dung. Mot dong chi dung khi no
# mang MOT trong cac tu nay.
_TOKEN_RE = r'NỘI BỘ|MẬT|SENSITIVE|REVIEW|SAFE'

def _strip_code_spans(text):
    """Bo CAC doan ma inline (giua hai dau backtick) — CHI dung de DO token,
    khong bao gio dung cho nhan tra ve.

    Fix round 2 (2026-10-05): _PIPELINE_NOISE_RE (danh sach tu "frontmatter
    | md_to_epub | TỆP NGUỒN") bi XOA — no trung voi chinh danh sach tu cong
    do kiem, nen cong do "qua" chi vi code suy dung CHINH may tu cong tim,
    khong do duoc gi ca. Tin hieu THAT la CAU TRUC, khong phai tu: hang-rao-
    song-va-nuoc trich nguyen van mot GIA TRI VI DU (`distribution: ⛔ NỘI
    BỘ`) — token nam TRONG mot doan ma inline, nghia la tac gia dang TRICH
    DAN mot gia tri truong, khong phai dang KHANG DINH pham vi cua chinh
    cuon sach. Mot loi khang dinh THAT viet bang prose hoac **in dam**,
    khong bao giam trong backtick. Vi vay: bo doan ma inline TRUOC khi tim
    token; neu token duy nhat cua dong nam trong do, dong xem nhu KHONG co
    token, va phep quet tiep tuc sang dong sau."""
    return re.sub(r'`[^`]*`', '', text)


def _strip_scope_markers(text):
    """Bo lan luot dau blockquote '>' va dau heading '#' o DAU chuoi, lap lai
    cho den khi khong con dau nao, roi strip khoang trang. Finding B:
    mot lan the '> ## ...' chi bo duoc '>', con '##' sot lai."""
    while True:
        new = re.sub(r'^>\s*', '', text)
        new = re.sub(r'^#+\s*', '', new)
        if new == text:
            break
        text = new
    return text.strip()


def read_scope(book_txt, scope_txt=None):
    """(nhan, muc_nguyen_ban, nguon). Thu tu doc, dung o nguon dau tien.

    BI-4. Than sach la nguon CHINH. Do that tren 34 cuon co book.md tai
    D:/Workshop_X/3_Resources/Books (2026-10-05): 23 khai pham vi trong THAN,
    0 tu sidecar (all 5 co _scope_decision.md cung khai trong than), 11 khong
    khai (8 ko co NỘI BỘ, 3 chi co trong prose). Vi the than sach la uu tien.
    SCOPE_FALLBACK in khi khong khai: tien le do duoc tren ban EPUB dau cua
    10x-easier-than-2x (nhan o frontmatter, 0/70 tep trong zip chua chu ay).

    Finding A: mot blockquote chi duoc coi la PHAN TIEP cua mot heading khi
    no la dong KHONG-TRANG ke tiep ngay sau heading (duoc phep bo qua dong
    trong, khong gi khac) — rockefeller-habits tung bi vo vi lookahead cu
    quet qua xa va vo mot blockquote KHONG lien quan 4 dong sau. Khi chinh
    dong khop la mot blockquote (vd `> ## ⚠️ PHÂN LOẠI...`), dong do CHINH LA
    loi khai bao — khong duoc tiep tuc tim xa hon.

    Fix round 1 (2026-10-05): mot heading/blockquote khop _SCOPE_KEYWORDS
    KHONG co nghia no la loi khai bao — do that tren 34 cuon: 10/23 cuon
    "khai trong than" thuc ra tra ve mot TIEU DE muc (`⛔ Phạm vi lưu hành`,
    khong co tu phan loai nao) hoac CHU THICH DUONG ONG ve cach md_to_epub.py
    xu ly frontmatter — khong phai loi khai bao thuc. Loi khai bao THAT nam
    trong THAN cua muc, co khi sau mot sub-heading sau hon (`## Quyết định
    phát hành`). Vi vay: mot heading mo ra mot MUC (den heading ke tiep CUNG
    hoac NONG hon, hoac het front matter); quet MUC do THEO THU TU, lay dong
    DAU TIEN mang mot token phan loai thuc (_TOKEN_RE). Khong tim thay token
    nao trong ca muc -> day KHONG phai loi khai bao dung — tiep tuc quet
    phan con lai cua front matter, cuoi cung lui ve sidecar roi SCOPE_FALLBACK.
    Khong duoc BIA mot phan loai ma sach khong noi ra.

    Mot dong CO token van co the la CHU THICH DUONG ONG: hang-rao-song-va-nuoc
    trich nguyen van mot gia tri VI DU co token (`` `distribution: ⛔ NỘI BỘ`
    ở frontmatter ``) de giai thich vi sao md_to_epub.py boc frontmatter —
    dong do bi loai boi _PIPELINE_NOISE_RE, loi khai bao THAT nam o dong sau
    (`## Quyết định phát hành` -> `> ## ⛔ NỘI BỘ XƯỞNG`).

    Do lai tren cung 34 cuon sau fix: phan bo nguon KHONG doi (23 than-sach /
    11 bao-toan) — ca 23 cuon than-sach deu co mot token THAT o dau do trong
    muc, chi la khong luon nam tren chinh dong heading/blockquote dau tien.
    `khong co tu phan loai: []` va `ro chu thich duong ong: []` tren toan bo
    corpus (do ngay 2026-10-05).
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

    # Search front matter for scope declaration in headings or blockquotes.
    # A heading/blockquote matching _SCOPE_KEYWORDS only OPENS a candidate
    # declaration section — it is accepted only if some line inside that
    # section carries a real classification token (_TOKEN_RE). Otherwise we
    # keep scanning rest of front matter instead of inventing a label.
    i = 0
    while i < front_matter_end:
        line = lines[i]
        if not mask[i]:
            i += 1
            continue

        is_heading = bool(re.match(r'^#+\s+', line))
        is_blockquote = bool(re.match(r'^>\s*', line))

        if not (is_heading or is_blockquote):
            i += 1
            continue
        if not re.search(_SCOPE_KEYWORDS, line, re.IGNORECASE):
            i += 1
            continue

        if is_heading:
            # Section runs until the next heading at the SAME or SHALLOWER
            # depth (a deeper sub-heading, e.g. `## Quyết định phát hành`
            # under a `#` heading, stays INSIDE the section), or until
            # front matter ends.
            level = len(re.match(r'^(#+)', line).group(1))
            end = front_matter_end
            for j in range(i + 1, front_matter_end):
                if not mask[j]:
                    continue
                hm = re.match(r'^(#+)\s', lines[j])
                if hm and len(hm.group(1)) <= level:
                    end = j
                    break
            section = range(i, end)
        else:
            # Standalone blockquote (no governing heading): a one-line
            # candidate section — it is already its own continuation.
            end = i + 1
            section = range(i, end)

        found = None
        for k in section:
            if not mask[k]:
                continue
            cand = _strip_scope_markers(lines[k])
            if not cand:
                continue
            # Token must survive with inline code spans removed — a token
            # that lives ONLY inside `backticks` is a quoted field value,
            # not this book's own assertion. The returned label stays the
            # ORIGINAL (markers-stripped) line — only the probe is pruned.
            probe = _strip_code_spans(cand)
            if not re.search(_TOKEN_RE, probe, re.IGNORECASE):
                continue
            found = cand
            break
        if found:
            return found, fid, 'than-sach'

        # Matched the keyword but no line in the section carries a real
        # token — not a usable declaration. Keep scanning past this
        # section rather than falling back immediately: a later heading
        # may carry the real one.
        i = end

    # Fall back to sidecar (only if it has a non-empty scope declaration)
    if scope_txt:
        m = re.search(_SIDE_SCOPE_RE, scope_txt)
        if m:
            label = m.group(1).strip()
            if label:  # F1: must not return empty label
                return label, fid, 'sidecar'

    return SCOPE_FALLBACK, fid, 'bao-toan'


def scope_class(label):
    """Rut cac token phan loai THAT tu nhan (xem _TOKEN_RE), theo THU TU
    xuat hien, IN HOA, khong lap. Khong tim thay token nao -> 'CHƯA KHAI'.

    Dung de ve BADGE ngan — nhan prose co the dai toi 114 ky tu (mot cau
    day trich dan), khong phai BADGE. SCOPE_FALLBACK duoc kiem rieng bang
    danh tinh: ban than hang chu cua no co doan "coi như NỘI BỘ" nen mot
    phep quet token don gian se nham tra ve 'NỘI BỘ' — day la mot nhan BAO
    TOAN, KHONG phai mot loi khai bao, va phai luon doc la 'CHƯA KHAI'."""
    if label == SCOPE_FALLBACK:
        return 'CHƯA KHAI'
    toks = []
    for m in re.finditer(_TOKEN_RE, label, re.IGNORECASE):
        t = m.group(0).upper()
        if t not in toks:
            toks.append(t)
    return ' — '.join(toks) if toks else 'CHƯA KHAI'


ROMAN = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
         'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}

_OUT_CHAP_RE = r'^#{2,4} +(?:Ch\.|Chương |Chapter )(\d{1,3}) *[—:·-] *(.*)$'


def parse_outline(txt):
    """{num: {...}} tu Phase3-Outline.md. LOP LAM GIAU — thieu truong nao thi
    de trong, KHONG bia va KHONG suy luan.

    Khuon khong nhat quan: 26 cua 34 cuon co heading `### `, 8 khong (2026-10-05).
    Bullet availability (2026-10-05, 34 cuon): corpus-wide 488 / 521 chuong
    (94%) co bullet, nhung usv-thiet-ke-he-thong chi 13 / 28. Bullet nay
    khong phai tom tat (120-150
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


_IP_HEAD_RE = r'^#+ +.*[Xx]ếp mức IP'

# Cot 1: so chuong (hoac dai so chuong) roi BO QUA phan con lai cua o — do
# that (Fix round 1, 2026-10-06) tren hang-rao-song-va-nuoc/khu-pho-6-bang:
# o Chuong mang CA so CA ten chuong tren cung mot dong ("01 Ba câu hỏi…",
# "01 · Sáu bằng…"), khong phai so/dai so THUAN nhu performance-by-design-ntb
# ("01–14"). `\**` cho phep mot cap **in dam** boc QUANH CA O (vd
# "**09 · Thứ không ai…**" trong khu-pho-6-bang) — vi `[^|]*` o cuoi da an
# toan voi moi ky tu con lai (ke ca dau `-`/`**` lam phan ten chuong), tien
# to `\**` chi can xu ly dau sao MO truoc chinh con so.
_IP_ROW_RE = (r'^\| *\**(\d{1,3}) *(?:[–—-] *(\d{1,3}))? *[^|]*\| *'
              r'([^|]+?) *\| *([^|]*?) *\|')

# Cot 2 PHAI mang mot token phan loai THAT — day la diem phan biet CHINH,
# khong phai cot 1. Mot bang do luc/goc nam canh bang IP co cot dau cung la
# so se KHONG BAO GIO co SAFE/REVIEW/SENSITIVE/MẬT o cot thu hai, nen doi hoi
# nay la an toan: no khong mo rong pham vi "doan tu khoa trong THAN CHUONG"
# (spec 3.4) — day van la doc MOT BANG da o dang may doc duoc, chi la kiem
# cot thu hai co mang token hay khong truoc khi tin no la mot dong IP.
_IP_LEVEL_TOKEN_RE = r'SAFE|REVIEW|SENSITIVE|MẬT'


def read_ip_table(book_txt):
    """{num: {'level','why'}} tu bang `Xep muc IP theo chuong` trong THAN sach.

    Spec 3.4 CAM do muc IP bang tu khoa. Phase7-Audit-Log.md xep muc trong
    van xuoi va hai agent KHONG dong y nhau (IP-B xep Ch.07/09/10/12/13 la
    SAFE, IP-A xep ca nam SENSITIVE), ban hop nhat ra 28/28 SENSITIVE ma
    chinh log goi la 'thoai hoa'. Day la lop loi 'dat ten cot theo thu minh
    muon no do'. Nen: chi doc bang DA o dang doc duoc bang may; khong co
    bang thi tra {} va the in 'chua do'.

    Ca viec tim heading MO bang lan diem KET MUC deu di qua heading_mask()
    truoc khi khop `#` — mot `#` nam trong khoi ma (vd chu thich ASCII) o
    ca truoc hoac giua bang khong duoc coi la tieu de thuc.

    Fix round 1 (2026-10-06): do that tren kho cho thay "3/32 cuon" ban dau
    la SAI theo kieu chinh cai da tra gia nhieu lan trong plan nay — dem
    duoc tieu de `Xếp mức IP` khac voi dem duoc mot BANG DOC DUOC BANG MAY;
    voi regex cu (cot 1 chi nhan so/dai so thuan) chi 1/3 cuon khop. Hai
    cuon con lai (hang-rao-song-va-nuoc, khu-pho-6-bang) co cot 1 mang CA so
    CA ten chuong — da MO RONG cot 1 de nhan dang nay, nhung PHAN BIET bang
    cot 2: mot dong chi duoc nhan la dong IP khi cot 2 mang mot token phan
    loai THAT (_IP_LEVEL_TOKEN_RE). Dieu kien nay dong luon mot lo hong AM
    trong chinh regex ban dau — cot 2 cu la `([^|]+?)` KHONG rang buoc gi,
    nen mot dong do luc/goc tinh cờ nam trong MUC bang IP (vd `| 03 | 12° |
    400 |`) se bi nhan nham level la "12°". Muc THAT luon giu nguyen nhu
    tac gia viet (ke ca emoji/in dam) — khong chuan hoa — vi do la cai CEO
    da ky duyet, khong phai cai ham nay suy dien ra.
    """
    lines = book_txt.splitlines()
    mask = heading_mask(lines)
    start = None
    for i, line in enumerate(lines):
        if mask[i] and re.match(_IP_HEAD_RE, line):
            start = i
            break
    if start is None:
        return {}

    out = {}
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if mask[i] and re.match(r'^#+ +\S', line):      # het muc
            break
        m = re.match(_IP_ROW_RE, line)
        if not m:
            continue
        level = m.group(3).strip()
        if not re.search(_IP_LEVEL_TOKEN_RE, level, re.IGNORECASE):
            continue                        # cot 2 khong co token: khong phai dong IP
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        if hi < lo or hi - lo > 200:        # dong rac, khong phai dai chuong
            continue
        for k in range(lo, hi + 1):
            out[k] = {'level': level, 'why': m.group(4).strip()}
    return out


def maybe(path, fn, default):
    """Doc tep neu co, tra `default` neu khong. Lop lam giau khong duoc lam
    sap ca lan chay chi vi thieu mot tep tuy chon."""
    try:
        return fn(rd(path))
    except (OSError, UnicodeDecodeError):
        return default
