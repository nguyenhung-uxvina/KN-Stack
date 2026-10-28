# -*- coding: utf-8 -*-
"""Dung ban do sach (bac A) tu mot thu muc sach da qua pipeline.

Mot tep HTML, mo tu dia, KHONG goi mang. Xem spec
docs/superpowers/specs/2026-10-03-book-map-design.md.
"""
import argparse
import html
import importlib.util
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bmp = _load('book_map_parse', 'book_map_parse.py')
mte = _load('md_to_epub', 'md_to_epub.py')      # chi dung count_html_comments

MIN_EDGES = 5          # inside-the-box co 2 canh => an do thi
BLOAT_WARN = 1.8       # CANH BAO hinh dang long, KHONG phai cong chan (spec
                       # §9 R-3) — va fix round 1 (2026-10-05): KHONG bat
                       # duoc loi EOF-overrun. Loi THAT do 1.49x trung vi,
                       # nam GIUA hai chuong cuoi DAI THAT (1.61x/1.48x);
                       # khong nguong nao tren ty le nay tach duoc ca ba.
                       # Cam bien CHAN that cho loi nay la dong 'tieu de
                       # lac trong than chuong' (bmp.stray_headings) duoi.
COV_BLOCK = 0.70
COV_WARN = 0.85


def vn(n):
    return '{:,}'.format(int(n)).replace(',', '.')


def esc(s):
    """Escape HTML TRUOC, roi moi doi dau markdown. Thu tu nguoc lai se de
    the cua TEN CHUONG lot ra — 5/32 cuon co <>&" trong ten chuong."""
    s = html.escape(s, quote=True)
    # `**... *noi* ...**`: regon non-greedy dut giua cau neu khong chan dau don
    s = re.sub(r'\*\*([^*]+(?:\*[^*]+\*[^*]*)*)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'«(.+?)»', r'<i>\1</i>', s)
    s = re.sub(r'`(.+?)`', r'<code>\1</code>', s)
    return s.replace('**', '')


def arc_svg(nums, edges):
    """Do thi cung, SVG tinh san trong Python. Khong thu vien JS (BI-3)."""
    W, H, pad = 1080, 210, 28
    step = (W - 2 * pad) / float(max(len(nums) - 1, 1))
    x = {n: pad + i * step for i, n in enumerate(nums)}
    base = H - 46
    inb = {n: 0 for n in nums}
    for a, ts in edges.items():
        for b in ts:
            if b in inb:
                inb[b] += 1
    s = ['<svg viewBox="0 0 %d %d" class="arc" role="img" aria-label='
         '"Do thi tham chieu cheo giua cac chuong">' % (W, H)]
    for a, ts in edges.items():
        for b in ts:
            if a not in x or b not in x:
                continue
            r = abs(x[b] - x[a]) / 2.0
            up = 1 if b > a else 0
            s.append('<path d="M%.1f,%d A%.1f,%.1f 0 0 %d %.1f,%d" class="%s"/>'
                     % (x[a], base, r, min(r * .75, 120), up, x[b], base,
                        'fw' if up else 'bw'))
    for n in nums:
        s.append('<circle cx="%.1f" cy="%d" r="%.1f" class="nd"/>'
                 % (x[n], base, 3 + min(inb[n], 8) * .9))
        if int(n) % 2 == 1 or inb[n] >= 4:
            s.append('<text x="%.1f" y="%d" class="lb">%02d</text>'
                     % (x[n], base + 18, int(n)))
    s.append('</svg>')
    return '\n'.join(s), inb


CSS = """
:root{--bg:#fbfaf7;--fg:#1b1a17;--mut:#6d6a63;--line:#e2ded5;--card:#fff;
--red:#b3261e;--accent:#1f5c8b;--warn:#8a5a00}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
--bg:#17181a;--fg:#e9e7e2;--mut:#9d9a93;--line:#2d2f33;--card:#1f2124;
--red:#ff8a80;--accent:#7cb3dd;--warn:#d6a455}}
:root[data-theme=dark]{--bg:#17181a;--fg:#e9e7e2;--mut:#9d9a93;--line:#2d2f33;
--card:#1f2124;--red:#ff8a80;--accent:#7cb3dd;--warn:#d6a455}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.55 -apple-system,"Segoe UI",system-ui,sans-serif}
.wrap{max-width:1140px;margin:0 auto;padding:28px 16px 72px}
.scope{display:inline-block;border:1px solid var(--red);color:var(--red);
border-radius:4px;padding:2px 9px;font-size:13px;font-weight:600}
.scopelabel{font-size:12.5px;color:var(--mut);margin:6px 0 0}
h1{font-size:26px;margin:14px 0 6px}
.sub{color:var(--mut);font-size:14px;margin-bottom:26px}
.sub b{color:var(--fg);font-variant-numeric:tabular-nums}
section>h2{font-size:13px;text-transform:uppercase;letter-spacing:.8px;
color:var(--mut);border-bottom:1px solid var(--line);padding-bottom:6px;
margin:34px 0 14px}
.grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(318px,1fr))}
.card{background:var(--card);border:1px solid var(--line);border-radius:7px;
padding:13px 14px;display:flex;flex-direction:column}
.card.red{border-left:3px solid var(--red)}
.cn{font-size:11px;color:var(--mut);letter-spacing:1px;font-weight:600}
.ct{font-size:15px;font-weight:650;margin:3px 0 9px;line-height:1.32}
ul{margin:0 0 10px;padding-left:17px}
li{font-size:13.5px;margin-bottom:5px}
.risk{font-size:12.5px;color:var(--warn);border-top:1px dashed var(--line);
padding-top:8px;margin-top:auto}
.risk.r{color:var(--red)}
ul.summary-anchored{border-left:2px solid var(--accent);margin-left:-3px;
padding-left:14px}
ul.summary-unanchored{border-left:2px dashed var(--warn);margin-left:-3px;
padding-left:14px}
.unanchored-label{color:var(--warn);font-style:italic;font-size:11.5px;
margin:0 0 4px}
.met{display:flex;gap:11px;flex-wrap:wrap;font-size:11.5px;color:var(--mut);
margin-top:9px;font-variant-numeric:tabular-nums}
.met i{font-style:normal}
.met .warn{color:var(--warn);font-weight:600}
.arcbox{background:var(--card);border:1px solid var(--line);border-radius:7px;
padding:8px}
.arc{width:100%;height:auto}
.arc path{fill:none;stroke-width:1}
.arc .fw{stroke:var(--accent);opacity:.42}
.arc .bw{stroke:var(--mut);opacity:.22}
.arc .nd{fill:var(--accent)}
.arc .lb{fill:var(--mut);font-size:9px;text-anchor:middle;
font-family:ui-monospace,monospace}
table{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:10px}
th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line);
vertical-align:top}
th{font-size:11px;text-transform:uppercase;color:var(--mut)}
.note{font-size:12.5px;color:var(--mut);margin-top:8px}
.undone{font-style:italic;opacity:.75}
code{font-family:ui-monospace,monospace;font-size:.9em}
@media(max-width:560px){.wrap{padding:20px 16px 56px}h1{font-size:21px}}
"""


def render_map(parsed, outline, scope, slug, cov, sha, ip, digest):
    ch = parsed['chapters']
    nums = sorted(ch)
    edges = bmp.crossrefs(parsed)
    tot = sum(c['words'] for c in ch.values())
    mer = sum(c['mermaid'] for c in ch.values())
    label, fid, src = scope
    cls = bmp.scope_class(label)

    o = ['<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">',
         '<meta name="viewport" content="width=device-width,initial-scale=1">',
         '<title>Bản đồ sách — %s</title>' % html.escape(slug),
         '<style>%s</style></head><body><div class="wrap">' % CSS,
         # Fix round 1: badge chi mang TOKEN phan loai (scope_class) — nhan
         # prose day du (co khi 114 ky tu, mot cau day trich dan) KHONG
         # vua lam badge. Nhan day du in lai ngay duoi, van thoa BI-4 vi
         # phan loai nam trong THAN trang.
         '<div class="scope">⛔ %s</div>' % esc(cls),
         '<p class="scopelabel">%s</p>' % esc(label),
         '<h1>Bản đồ sách — %s</h1>' % html.escape(slug),
         '<p class="sub">%d chương · <b>%s</b> từ · <b>%d</b> sơ đồ · '
         'mức nguyên bản <b>%s</b> · phủ <b>%.0f%%</b> · ước đọc lại '
         '<b>~%d</b> giờ</p>' % (len(ch), vn(tot), mer, fid, cov * 100,
                                 max(tot // 12000, 1))]

    n_edges = sum(len(v) for v in edges.values())
    if n_edges >= MIN_EDGES:
        svg, inb = arc_svg(nums, edges)
        hot = [kv for kv in sorted(inb.items(), key=lambda kv: -kv[1])[:5] if kv[1]]
        o.append('<section><h2>Đồ thị tham chiếu chéo — đo từ thân sách</h2>'
                 '<div class="arcbox">%s</div>' % svg)
        o.append('<p class="note">Vòng xanh = chương trước trỏ tới chương sau · '
                 'xám = trỏ ngược. Đốm to = bị nhiều chương trỏ tới. Bị trỏ '
                 'nhiều nhất: %s.</p></section>'
                 % ' · '.join('<b>Ch.%02d</b> (%d)' % (int(n), c) for n, c in hot))

    reds = sorted([n for n in nums if outline.get(n, {}).get('red')])
    if reds:
        o.append('<section><h2>Đọc lại trước — theo dòng «Rủi ro» của dàn ý</h2>'
                 '<table class="risktable"><tr><th>Ch.</th><th>Tên</th>'
                 '<th>Vì sao đánh 🔴</th></tr>')
        for n in reds:
            r = re.sub(r'^🔴 *', '', outline[n]['risk'])
            o.append('<tr><td>%02d</td><td>%s</td><td>%s</td></tr>'
                     % (int(n), esc(ch[n]['title']), esc(r)))
        o.append('</table><p class="note">%d/%d chương được chính dàn ý đánh 🔴.'
                 '</p></section>' % (len(reds), len(ch)))

    cur, opened = object(), False
    for n in nums:
        c = ch[n]
        spec_ = outline.get(n, {})
        part = spec_.get('part')
        if part != cur:
            cur = part
            head = ('Phần %d — %s' % (part[0], html.escape(part[1]))) if part \
                   else 'Các chương'
            o.append('%s<section><h2>%s</h2><div class="grid">'
                     % ('</div></section>' if opened else '', head))
            opened = True
        o.append('<div class="card%s">' % (' red' if spec_.get('red') else ''))
        o.append('<div class="cn">CH.%02d%s%s</div>'
                 % (int(n), ' · MỚI' if spec_.get('new') else '',
                    (' · ' + spec_['neo']) if spec_.get('neo') else ''))
        o.append('<div class="ct">%s</div>' % esc(c['title']))
        # Tang 3 (spec 1.2): o tom tat la be mat bia dat duy nhat cua tinh
        # nang nay, nen thu tu uu tien la digest (viet boi agent, co neo
        # dong kiem duoc) -> bullets dan y (lam giau, khong phai tom tat
        # that -> xem parse_outline docstring) -> 'chua tom tat'.
        #
        # `n == int(n)` cung dieu kien nhu o the muc IP duoi: ban TRUNG (key
        # thap phan, vd 5.001) KHONG duoc "muon" digest viet cho ban dau —
        # digest chi gan voi key SO NGUYEN (xem digest_anchor_ok). Thieu
        # dieu kien nay se mac lai dung loi da vo o muc IP (Fix round 2,
        # 2026-10-06): mot chuong TRUNG hien lai tom tat cua ban kia.
        if n == int(n) and digest.get(int(n)):
            o.append('<ul class="summary-anchored">')
            for it in digest[int(n)][:5]:
                o.append('<li>%s</li>' % esc(it['text']))
            o.append('</ul>')
        elif spec_.get('bullets'):
            # Fix round 4 (2026-10-06), F1: bullet dan y la TU LIEU THAM KHAO (xem
            # parse_outline docstring + spec §1.2 R-1), KHONG phai tom tat
            # da qua cong neo — truoc fix nay no hien y nhu dong digest,
            # khong co gi phan biet, du khong agent nao viet lai hay kiem
            # qua. Phai danh dau RO cho nguoi doc bang tieng Viet + class
            # rieng (xem CSS). Van duoc LINT STE o verify() (xem
            # summary_lines_from_page) vi mot cau vung van la cau vung bat
            # ke nguon nao sinh ra no, nhung KHONG co cong neo — bullet dan
            # y khong mang so dong goc nen khong co gi de neo, do KHONG
            # phai bia dat, chi la chua kiem.
            o.append('<p class="note unanchored-label">Từ dàn ý — CHƯA qua '
                     'cổng neo, không phải tóm tắt đã kiểm</p>')
            o.append('<ul class="summary-unanchored">')
            for b in spec_['bullets'][:3]:
                t = re.split(r'(?<=[.;])\s', b)[0]
                if len(t) > 190:
                    t = t[:187].rsplit(' ', 1)[0] + '…'
                o.append('<li>%s</li>' % esc(t))
            o.append('</ul>')
        else:
            o.append('<p class="note undone">chưa tóm tắt</p>')
        tgt = spec_.get('target', 0)
        pc = ((c['words'] - tgt) * 100.0 / tgt) if tgt else 0
        # Spec §3.4: muc IP CHI den tu bang doc duoc bang may (bmp.read_ip_table)
        # — khong bao gio doan tu khoa trong than chuong. Khong co bang thi in
        # 'chua do', khong bia.
        #
        # Fix round 2 (2026-10-06): `n` la so NGUYEN, TRU khi la ban trung —
        # ban trung thu hai tro len mang key THAP PHAN nam CHAT trong
        # (num, num+1), vd 5.001 (xem parse_chapters). `int(5.001) == 5` nen
        # mot phien ban cu se cho chuong trung MUON ca muc IP cua chuong 5 —
        # mot phan loai sach KHONG he dua ra cho noi dung do. `n == int(n)`
        # la True cho so nguyen va False cho moi key thap phan cua ban trung,
        # nen chi tra cuu bang khi n THAT SU la so nguyen; ban trung luon ra
        # 'chua do' — anh xa that su mo ho, khong co cach nao "khon" hon.
        ip_cell = ('<i>mức IP: %s</i>' % esc(ip[int(n)]['level'])
                   if n == int(n) and int(n) in ip
                   else '<i class="undone">mức IP: chưa đo</i>')
        o.append('<div class="met"><i>%s từ</i>%s<i>%d sơ đồ%s</i>'
                 '<i>cần %d ch. khác</i>%s'
                 '</div>'
                 % (vn(c['words']),
                    ('<i%s>đặt %s (%+.0f%%)</i>'
                     % (' class="warn"' if abs(pc) >= 20 else '', vn(tgt), pc))
                    if tgt else '<i class="undone">đặt: chưa đo</i>',
                    c['mermaid'],
                    (' / đặt %d' % spec_['figs']) if spec_.get('figs') else '',
                    len(edges.get(n, [])),
                    ip_cell))
        if spec_.get('risk'):
            o.append('<div class="risk%s">%s</div>'
                     % (' r' if spec_.get('red') else '', esc(spec_['risk'])))
        o.append('</div>')
    o.append('%s<p class="note">Dựng từ <code>book.md</code> sha256 '
             '<code>%s</code>. Lệch sha ⇒ bản đồ này đã cũ.</p>'
             '</div></body></html>'
             % ('</div></section>' if opened else '', sha[:16]))
    return '\n'.join(o)


def build(book_dir, out_path):
    """Ghi tep, tra bang so do. Nem Fail neu khong du dieu kien."""
    import hashlib
    src = os.path.join(book_dir, 'book.md')
    if not os.path.exists(src):
        raise SystemExit('Khong thay %s — day phai la thu muc sach da dung xong.'
                         % src)
    txt = bmp.rd(src)
    if not txt.strip():
        raise SystemExit('%s rong.' % src)
    parsed = bmp.parse_chapters(txt)
    ip = bmp.read_ip_table(txt)
    if not parsed['chapters']:
        raise SystemExit('Khong thay tieu de chuong nao trong %s (%s). Khong '
                         'sinh trang rong.' % (src, parsed['warn']))
    cov = bmp.coverage(parsed, txt)
    outline = bmp.maybe(os.path.join(book_dir, 'Phase3-Outline.md'),
                        bmp.parse_outline, {})
    scope = bmp.read_scope(
        txt, bmp.maybe(os.path.join(book_dir, '_scope_decision.md'),
                       lambda s: s, None))
    sha = hashlib.sha256(txt.encode('utf-8')).hexdigest()
    slug = os.path.basename(book_dir.rstrip('/\\'))
    # Tang 3 (spec 1.2): o tom tat. Python KHONG sinh tom tat — chi doc tep
    # agent da viet (<thu-muc-sach>/_book_map_digest.md), lint theo STE 80%
    # va kiem neo dong. Thieu tep nay thi {} (lop lam giau, suy thoai em).
    digest = bmp.maybe(os.path.join(book_dir, '_book_map_digest.md'),
                       bmp.parse_digest, {})
    page = render_map(parsed, outline, scope, slug, cov, sha, ip, digest)
    with io.open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)

    ws = [parsed['chapters'][n]['words'] for n in sorted(parsed['chapters'])]
    med = sorted(ws)[len(ws) // 2]
    return {'chapters': parsed['chapters'], 'depth': parsed['depth'],
            'warn': parsed['warn'], 'dups': parsed['dups'], 'coverage': cov,
            'scope': scope, 'sha': sha, 'out': out_path, 'ip': ip,
            'mermaid_src': len(re.findall(r'^```mermaid', txt, re.M)),
            'mermaid_page': sum(c['mermaid'] for c in parsed['chapters'].values()),
            'comments': mte.count_html_comments(txt),
            'bloat': (ws[-1] / float(med)) if med else 0,
            'digest': digest,
            'digest_bad': bmp.digest_anchor_ok(digest, parsed),
            'ste_bad': [(n, i['text'], bmp.ste_lint(i['text']))
                        for n, items in digest.items() for i in items
                        if bmp.ste_lint(i['text'])]}


_NET_RE = r'(?:src|href)="https?://'

# Fix round 4 (2026-10-06), F1: hai lop tom tat hien ra HTML giong nhau het — digest da
# neo (summary-anchored) va bullet dan y chua neo (summary-unanchored, xem
# render_map). Gom chung mot regex mo ("anchored|unanchored") de doc CA HAI
# tu TRANG DA DUNG, khong phai tu tep rieng.
_SUMMARY_UL_RE = r'<ul class="summary-(?:anchored|unanchored)">(.*?)</ul>'
_LI_RE = r'<li>(.*?)</li>'


def summary_lines_from_page(h):
    """Tat ca dong tom tat THAT SU hien tren trang — ca hai nguon: digest
    da neo VA bullet dan y chua neo. Tra ve VAN BAN THO (da bo the HTML con,
    da giai ma entity) de ste_lint() do dung.

    F1: 'tom tat vi pham STE' phai lint CAI DANG HIEN TREN TRANG, khong doc
    lai `_book_map_digest.md` rieng. Do that (2026-10-05, 34 cuon): 32/34
    cuon hien tom tat tu bullet dan y (0/34 co tep digest), nen cong cu
    truoc chi do tep digest se LUON bao 'sach' tren van ban CHUA AI LINT
    QUA — 1.402 dong bullet se render, 281 trong so do vi pham tran 25
    tu/dong, ma cong bao 0. Doc truc tiep tu `h` sua dung lo hong do."""
    out = []
    for ul_body in re.findall(_SUMMARY_UL_RE, h, re.S):
        for li in re.findall(_LI_RE, ul_body, re.S):
            t = html.unescape(re.sub(r'<[^>]+>', '', li)).strip()
            if t:
                out.append(t)
    return out


# Fix round 4 (2026-10-06), nho #2: gioi han dem "so do the vs nguon" vao DUNG khoi
# .met — truoc khi co bullet dan y hien tren trang (fix F1 o tren), mot
# bullet 1.402 dong CO KHA NANG mang nguyen van cum "N sơ đồ" (vd mot cau
# dan y trich "3 sơ đồ minh hoa cau truc"), va regex cu quet CA TRANG se
# dem nham cum do vao tong. render_map() LUON in dung MOT <i>N sơ đồ</i>
# ngay dau khoi .met (xem render_map), nen quet rieng tung khoi .met roi
# bat <i>N sơ đồ ngay sau dau mo la an toan voi van ban bullet tu do.
_MET_BLOCK_RE = r'<div class="met">.*?</div>'
_MET_MERMAID_RE = r'<i>(\d+) sơ đồ'


def _mer_page_count(h):
    total = 0
    for block in re.findall(_MET_BLOCK_RE, h, re.S):
        m = re.search(_MET_MERMAID_RE, block)
        if m:
            total += int(m.group(1))
    return total


def verify(out_path, book_dir):
    """(rows, exit_code). rows = [(ten, gia tri, nguong, trang thai)].

    BI-5. Phep do dau tien so voi `wc -w` CA TEP book.md — mot tong tinh
    NGOAI duong ong. Trong phep so sanh TRUOC/SAU vo loi (sua mat na khoi
    ma), day la cam bien duy nhat tut ca 5/5 ca loi khoi ma; hai cam bien
    chi so cac chuong voi nhau bo sot 4/5, va pahl-beitz-tap2 nam o 40% phu
    ma chung bao 'sach'.

    Fix round 4 (2026-10-06), F3: cau 'bat 5/5' dung cho SO SANH truoc/sau, SAI cho
    NGUONG TUYET DOI da chon shipped (COV_BLOCK=0.70, COV_WARN=0.85) — do
    lai 5 cuon do tren MOT luot chay: tau-nhom-han-quoc-phong 38,9% CHAN,
    pahl-beitz-tap2 40,1% CHAN, ai-at-war 76,6% canh bao, cross-design-
    methods 94,0% ok (im lang), kien-truc-tu-hanh-hang-hai 93,7% ok (im
    lang). Hang nay chan ca NANG, canh bao ca VUA, im lang truoc ca NHE —
    khong nguong tuyet doi nao bat het vi mot mat 4% nam duoi moi san se
    chan nham sach hop le gan nhat (76,1%). Hang `tieu de lac trong than
    chuong` (bmp.stray_headings) moi bat dung CA NAM ca nay; hai hang hop
    lai moi phu mat NANG + loi CAU TRUC, khong hang nao mot minh bat mat
    NHE.
    """
    h = bmp.rd(out_path)
    txt = bmp.rd(os.path.join(book_dir, 'book.md'))
    parsed = bmp.parse_chapters(txt)
    ch = parsed['chapters']
    cov = bmp.coverage(parsed, txt)
    ws = [ch[n]['words'] for n in sorted(ch)] or [0]
    med = sorted(ws)[len(ws) // 2] or 1

    net = len(re.findall(_NET_RE, h))
    scripts = len(re.findall(r'<script', h, re.I))
    comments = h.count('<!--')
    # Fix round 3 (2026-10-06), F2: BI-4 doi hoi nhan nam trong THAN trang —
    # mot nhan chi nam trong <title> hay mot attribute se qua duoc phep do
    # cu (tim ca tep). Cat rieng vung <body>...</body> ra roi moi tim; thieu
    # han <body> thi coi la KHONG dat (0), khong lui ve tim ca tep.
    body_m = re.search(r'<body[^>]*>(.*)</body>', h, re.S | re.I)
    # Fix round 4 (2026-10-06), nho #3: mo rong nhan pham vi ra CUNG bo
    # token ma scope reader dung (bmp._TOKEN_RE) — truoc chi khop "NỘI BỘ|
    # CHƯA KHAI", nen mot nhan dung cham dung "MẬT"/"REVIEW"/"SAFE" mot minh
    # (hop le theo bmp._TOKEN_RE va scope_class()) se bi cong nay CHAN nham
    # mot trang da khai pham vi DUNG cach.
    _LABEL_RE = bmp._TOKEN_RE + r'|CHƯA KHAI'
    has_label = int(bool(body_m and re.search(_LABEL_RE, body_m.group(1))))
    cards = h.count('class="card')
    mer_src = len(re.findall(r'^```mermaid', txt, re.M))
    mer_page = _mer_page_count(h)
    stray = bmp.stray_headings(parsed)
    # Tang 3 (spec 1.2, spec 9 R-1): verify() PHAI tu tinh lai cac gia tri
    # nay tu book_dir/trang da dung — khong nhan tu build() — vi day phai
    # dung duoc mot minh (xem docstring module). digest la be mat bia dat
    # duy nhat cua tinh nang nay nen cong neo PHAI CHAN va CHI doc digest —
    # bullet dan y khong mang so dong goc nen khong co gi de neo. Vi pham
    # STE chi la van de van phong, nen CHI canh bao — nhung (fix round 4,
    # F1) phai lint CAI DANG HIEN TREN TRANG (ca digest VA bullet), khong
    # chi tep digest rieng — xem summary_lines_from_page().
    digest = bmp.maybe(os.path.join(book_dir, '_book_map_digest.md'),
                       bmp.parse_digest, {})
    dbad = bmp.digest_anchor_ok(digest, parsed)
    sbad = [1 for line in summary_lines_from_page(h) if bmp.ste_lint(line)]

    rows = [
        ('ty le phu', '%.0f%%' % (cov * 100), '>=70% chan · <85% canh bao',
         'CHAN' if cov < COV_BLOCK else ('canh-bao' if cov < COV_WARN else 'ok')),
        ('goi mang', net, '=0', 'CHAN' if net else 'ok'),
        ('the script', scripts, '=0 o bac A', 'CHAN' if scripts else 'ok'),
        ('chu thich html', comments, '=0', 'CHAN' if comments else 'ok'),
        ('nhan pham vi', has_label, '>=1', 'ok' if has_label else 'CHAN'),
        ('so the vs so chuong', '%d vs %d' % (cards, len(ch)), 'lech 0',
         'ok' if cards == len(ch) else 'CHAN'),
        ('so do the vs nguon', '%d vs %d' % (mer_page, mer_src), 'lech 0',
         'ok' if mer_page == mer_src else 'canh-bao'),
        # Fix round 1 (2026-10-05): dieu kien CAU TRUC, chinh xac — khong
        # phai thong ke. Hang nay BAT duoc loi EOF-overrun ma hang ty le
        # ben duoi KHONG bat duoc (xem docstring bmp.stray_headings). CHAN
        # vi dieu kien nay khong co vung xam: sai 1 dong la loi, khong phai
        # muc do.
        ('tieu de lac trong than chuong', stray, '=0',
         'CHAN' if stray else 'ok'),
        ('chuong cuoi / trung vi', '%.2fx' % (ws[-1] / float(med)),
         '<1.8x (canh bao, hinh dang long — KHONG bat EOF-overrun)',
         'canh-bao' if ws[-1] / float(med) > BLOAT_WARN else 'ok'),
        ('so chuong trung', parsed['dups'] or 0, '=0',
         'canh-bao' if parsed['dups'] else 'ok'),
        # Fix round 4 (2026-10-06), F1: nguong chi noi ro PHAM VI cua hang
        # nay — digest MOI co so dong de neo; bullet dan y khong co, nen
        # KHONG the va KHONG duoc tinh vao hang nay (do khong phai bia dat).
        ('neo tom tat sai', len(dbad), '=0 (chi dong _book_map_digest.md)',
         'CHAN' if dbad else 'ok'),
        # Fix round 4 (2026-10-06), F1: gia tri nay gio linh CA dong digest
        # VA dong bullet dan y dang hien tren trang (xem
        # summary_lines_from_page) — truoc chi doc tep digest rieng, nen
        # tren 32/34 cuon khong co digest, hang nay LUON bao 'sach' tren
        # van ban bullet CHUA AI LINT QUA.
        ('tom tat vi pham STE', len(sbad),
         '=0 (canh bao; linh ca dong bullet dan y chua neo)',
         'canh-bao' if sbad else 'ok'),
    ]
    return rows, (1 if [r for r in rows if r[3] == 'CHAN'] else 0)


def main():
    ap = argparse.ArgumentParser(
        description='Dung ban do sach (mot tep HTML, offline) tu thu muc sach.')
    ap.add_argument('book_dir', help='Thu muc chua book.md')
    ap.add_argument('-o', '--out', help='Noi ra. Mac dinh <thu-muc>/<slug>-map.html')
    ap.add_argument('--verify', action='store_true',
                    help='Chi chay cong nghiem thu tren tep da dung, khong dung lai')
    a = ap.parse_args()
    d = a.book_dir
    slug = os.path.basename(d.rstrip('/\\'))
    out = a.out or os.path.join(d, slug + '-map.html')

    if a.verify:
        if not os.path.exists(out):
            raise SystemExit('Khong thay %s — dung truoc da.' % out)
        rows, code = verify(out, d)
    else:
        rep = build(d, out)
        print('%-16s: %s' % ('sach', slug))
        print('%-16s: H%s %s'
              % ('muc tieu de', rep['depth'],
                 ('CANH BAO: ' + rep['warn']) if rep['warn'] else 'ok'))
        print('%-16s: %d' % ('chuong', len(rep['chapters'])))
        print('%-16s: %s (%s)' % ('pham vi', rep['scope'][0], rep['scope'][2]))
        print('%-16s: %s' % ('-> tep', out))
        print()
        rows, code = verify(out, d)

    print('%-24s %-16s %-28s %s' % ('PHEP DO', 'GIA TRI', 'NGUONG', 'TRANG THAI'))
    for name, val, thr, st in rows:
        print('%-24s %-16s %-28s %s' % (name, val, thr, st))
    if code:
        print('\nCO DONG CHAN — khong giao tep nay.')
    return code


if __name__ == '__main__':
    sys.exit(main())
