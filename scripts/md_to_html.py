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
BLOAT_WARN = 1.8       # CANH BAO, khong phai cong chan (spec §9 R-3)
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


def render_map(parsed, outline, scope, slug, cov, sha):
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
        if spec_.get('bullets'):
            o.append('<ul>')
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
        o.append('<div class="met"><i>%s từ</i>%s<i>%d sơ đồ%s</i>'
                 '<i>cần %d ch. khác</i><i class="undone">mức IP: chưa đo</i>'
                 '</div>'
                 % (vn(c['words']),
                    ('<i%s>đặt %s (%+.0f%%)</i>'
                     % (' class="warn"' if abs(pc) >= 20 else '', vn(tgt), pc))
                    if tgt else '<i class="undone">đặt: chưa đo</i>',
                    c['mermaid'],
                    (' / đặt %d' % spec_['figs']) if spec_.get('figs') else '',
                    len(edges.get(n, []))))
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
    page = render_map(parsed, outline, scope, slug, cov, sha)
    with io.open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)

    ws = [parsed['chapters'][n]['words'] for n in sorted(parsed['chapters'])]
    med = sorted(ws)[len(ws) // 2]
    return {'chapters': parsed['chapters'], 'depth': parsed['depth'],
            'warn': parsed['warn'], 'dups': parsed['dups'], 'coverage': cov,
            'scope': scope, 'sha': sha, 'out': out_path,
            'mermaid_src': len(re.findall(r'^```mermaid', txt, re.M)),
            'mermaid_page': sum(c['mermaid'] for c in parsed['chapters'].values()),
            'comments': mte.count_html_comments(txt),
            'bloat': (ws[-1] / float(med)) if med else 0}


def main():
    ap = argparse.ArgumentParser(
        description='Dung ban do sach (mot tep HTML, offline) tu thu muc sach.')
    ap.add_argument('book_dir', help='Thu muc chua book.md')
    ap.add_argument('-o', '--out', help='Noi ra. Mac dinh <thu-muc>/<slug>-map.html')
    a = ap.parse_args()
    d = a.book_dir
    slug = os.path.basename(d.rstrip('/\\'))
    out = a.out or os.path.join(d, slug + '-map.html')
    rep = build(d, out)
    print('%-16s: %s' % ('sach', slug))
    print('%-16s: H%s %s' % ('muc tieu de', rep['depth'],
                             ('CANH BAO: ' + rep['warn']) if rep['warn'] else 'ok'))
    print('%-16s: %d' % ('chuong', len(rep['chapters'])))
    print('%-16s: %.0f%%' % ('ty le phu', rep['coverage'] * 100))
    print('%-16s: %s (%s)' % ('pham vi', rep['scope'][0], rep['scope'][2]))
    print('%-16s: %s' % ('-> tep', out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
