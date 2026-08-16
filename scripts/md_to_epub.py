#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chuyen Markdown sang EPUB, co dung so do mermaid NGAY TREN MAY.

Vi sao can script rieng thay vi goi thang pandoc:

  1. Pandoc khong dung mermaid. No do nguyen ma nguon so do ra thanh khoi chu.
     Trinh doc EPUB khong chay JavaScript nen khong co gi dung chung len.
     -> Tach khoi mermaid, dung bang mermaid-cli thanh PNG, roi nhung vao.

  2. Frontmatter kieu IPARAG lam vo trinh phan tich YAML cua pandoc:
     `tags: [#type/book]` — dau '#' mo comment YAML ngay giua flow sequence
     nen chuoi khong bao gio dong.  -> Tu boc frontmatter truoc khi giao pandoc.

  3. Chu thich HTML an (<!-- ... -->) di thang vao EPUB. EPUB la mot tep zip
     chua HTML: ai giai nen ra deu doc duoc het.  -> Dem va bao so luong.

  4. Dung xong chua chac dung. -> Mo lai EPUB nhu zip, doi chieu so anh, so the
     <img>, tham chieu gay, so do con sot; sai thi thoat khac 0.

AN NINH: so do dung offline tuyet doi. Khong kroki.io, khong mermaid.ink.
Tai lieu noi bo khong duoc roi may. Day la rang buoc cung, khong phai tuy chon.

Dung:
    python md_to_epub.py <input.md> [-o out.epub] [--title T] [--author A]
           [--lang vi] [--strip-comments] [--split-level N] [--scale N]
           [--no-diagrams]

Yeu cau: pandoc. Them mermaid-cli (mmdc) neu tai lieu co so do mermaid.
"""
import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

# Cau hinh mermaid + CSS de THANG trong file nay, khong tach ra file canh skill:
# duong dan tuong doi ra ngoai thu muc skill bi dut duoi junction Windows.
MERMAID_CONFIG = {
    "theme": "default",
    # Nhan 4 o cua quadrantChart mac dinh dai hon be ngang o -> bi cat cut hai
    # mep va chong chu. Ha co chu, noi rong khung thi vua.
    "quadrantChart": {
        "chartWidth": 1200,
        "chartHeight": 900,
        "titleFontSize": 22,
        "quadrantLabelFontSize": 15,
        "xAxisLabelFontSize": 16,
        "yAxisLabelFontSize": 16,
        "pointLabelFontSize": 13,
        "quadrantTextTopPadding": 8,
        "pointTextPadding": 6,
    },
}

EPUB_CSS = """img { max-width: 100%; height: auto; display: block; margin: 1em auto; }
figure { margin: 1.2em 0; page-break-inside: avoid; break-inside: avoid; text-align: center; }
table { border-collapse: collapse; font-size: 0.85em; margin: 1em 0; }
th, td { border: 1px solid #bbb; padding: 0.3em 0.5em; text-align: left; vertical-align: top; }
th { background: #f0f0f0; }
pre { white-space: pre-wrap; word-wrap: break-word; font-size: 0.8em;
      background: #f7f7f7; padding: 0.6em; border-left: 3px solid #ccc; }
blockquote { margin-left: 1em; padding-left: 0.8em; border-left: 3px solid #ccc; font-style: normal; }
"""

MERMAID_RE = re.compile(r'^```mermaid[ \t]*\r?\n(.*?)^```[ \t]*$', re.S | re.M)
COMMENT_RE = re.compile(r'<!--.*?-->', re.S)


class Fail(Exception):
    """Loi doc duoc cho nguoi dung — in ra roi thoat, khong xoe stack trace."""


# --------------------------------------------------------------- phan tich

def strip_frontmatter(text):
    """Boc YAML frontmatter. Tra ve (than_bai, dict_metadata).

    Khong dung thu vien YAML: frontmatter IPARAG co `tags: [#type/...]` lam vo
    moi trinh phan tich YAML dung chuan. Chi vot cac cap `khoa: gia tri` phang,
    du de lay title/author neu co.
    """
    if not text.startswith('---'):
        return text, {}
    end = text.find('\n---', 3)
    if end == -1:
        return text, {}
    head = text[3:end]
    body = text[end + len('\n---'):].lstrip('\n')
    meta = {}
    for line in head.splitlines():
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$', line)
        if m:
            meta[m.group(1)] = m.group(2).strip().strip('"\'')
    return body, meta


def find_mermaid_blocks(text):
    """Danh sach ma nguon cac so do mermaid. Khoi ma tran khong tinh."""
    return [m.group(1).rstrip() for m in MERMAID_RE.finditer(text)]


def count_html_comments(text):
    return text.count('<!--')


def derive_title(body, meta):
    if meta.get('title'):
        return meta['title']
    m = re.search(r'^#\s+(.+)$', body, re.M)
    return m.group(1).strip() if m else 'Khong ten'


# ------------------------------------------------------------- cong cu ngoai

def find_tool(names, env_var=None):
    if env_var and os.environ.get(env_var):
        p = os.environ[env_var]
        if os.path.exists(p) or shutil.which(p):
            return p
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def find_mmdc():
    p = find_tool(['mmdc', 'mmdc.cmd'], env_var='MMDC_BIN')
    if p:
        return p
    # mermaid-cli cai cuc bo trong thu muc dang lam viec
    for rel in (os.path.join('node_modules', '.bin', 'mmdc.cmd'),
                os.path.join('node_modules', '.bin', 'mmdc')):
        if os.path.exists(rel):
            return os.path.abspath(rel)
    return None


def render_diagrams(blocks, work_dir, scale):
    """Dung tung so do thanh PNG trong work_dir/diagrams. Tra ve danh sach ten tep."""
    mmdc = find_mmdc()
    if not mmdc:
        raise Fail(
            'Tai lieu co %d so do mermaid nhung khong tim thay mermaid-cli (mmdc).\n'
            '  Cai:      npm install -g @mermaid-js/mermaid-cli\n'
            '  Hoac tro: dat bien moi truong MMDC_BIN tro toi mmdc\n'
            '  Hoac bo:  them --no-diagrams (so do se thanh khoi chu trong EPUB)'
            % len(blocks))

    diag_dir = os.path.join(work_dir, 'diagrams')
    os.makedirs(diag_dir, exist_ok=True)
    cfg = os.path.join(work_dir, 'mermaid-config.json')
    io.open(cfg, 'w', encoding='utf-8').write(json.dumps(MERMAID_CONFIG))

    names = []
    for i, code in enumerate(blocks, 1):
        stem = 'd%02d' % i
        mmd = os.path.join(diag_dir, stem + '.mmd')
        png = os.path.join(diag_dir, stem + '.png')
        io.open(mmd, 'w', encoding='utf-8', newline='\n').write(code + '\n')
        r = subprocess.run([mmdc, '-i', mmd, '-o', png, '-b', 'white',
                            '-s', str(scale), '-w', '1400', '-c', cfg],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(png):
            raise Fail('Dung so do %s that bai:\n%s' % (stem, (r.stderr or r.stdout)[-600:]))
        names.append('diagrams/%s.png' % stem)
        print('  [%d/%d] %s' % (i, len(blocks), stem))
    return names


# ----------------------------------------------------------------- nghiem thu

def verify(epub_path, expect_png, expect_mermaid_left):
    z = zipfile.ZipFile(epub_path)
    names = z.namelist()
    xhtml = [n for n in names if n.endswith('.xhtml')]
    body = ''.join(z.read(n).decode('utf-8') for n in xhtml)
    png = [n for n in names if n.lower().endswith('.png')]

    srcs = set(re.findall(r'<img[^>]+src="([^"]+)"', body))
    embedded = set(os.path.basename(n) for n in png)
    broken = [s for s in srcs if os.path.basename(s) not in embedded]

    rep = {
        'zip_ok': z.testzip() is None,
        'png': len(png),
        'img_tags': body.count('<img'),
        'broken_refs': len(broken),
        'mermaid_left': body.count('"mermaid"'),
        'chapters': len(xhtml),
        'tables': body.count('<table'),
        'comments': body.count('<!--'),
    }
    problems = []
    if not rep['zip_ok']:
        problems.append('tep zip hong')
    if rep['png'] != expect_png:
        problems.append('anh nhung %d, cho doi %d' % (rep['png'], expect_png))
    if rep['broken_refs']:
        problems.append('%d tham chieu anh gay' % rep['broken_refs'])
    if rep['mermaid_left'] != expect_mermaid_left:
        problems.append('con %d khoi mermaid tran' % rep['mermaid_left'])
    return rep, problems


# ---------------------------------------------------------------------- chay

def convert(src, out, title=None, author=None, lang='vi', strip_comments=False,
            split_level=2, scale=3, no_diagrams=False):
    if not os.path.isfile(src):
        raise Fail('Khong thay tep dau vao: %s' % src)
    if not find_tool(['pandoc']):
        raise Fail('Khong tim thay pandoc. Cai: winget install JohnMacFarlane.Pandoc')

    text = io.open(src, encoding='utf-8').read()
    body, meta = strip_frontmatter(text)

    n_comments = count_html_comments(body)
    if strip_comments:
        body = COMMENT_RE.sub('', body)
        print('Chu thich an  : %d — DA GO khoi ban xuat' % n_comments)
    elif n_comments:
        print('Chu thich an  : %d html comment se NAM TRONG EPUB.' % n_comments)
        print('                EPUB la zip chua HTML — ai giai nen deu doc duoc.')
        print('                Muon go: chay lai voi --strip-comments')
    else:
        print('Chu thich an  : 0')

    blocks = find_mermaid_blocks(body)
    work = tempfile.mkdtemp(prefix='md2epub-')
    try:
        expect_png = 0
        if blocks and not no_diagrams:
            print('So do mermaid : %d — dang dung tren may' % len(blocks))
            imgs = render_diagrams(blocks, work, scale)
            it = iter(imgs)
            body = MERMAID_RE.sub(lambda m: '![](%s)' % next(it), body)
            expect_png = len(imgs)
        elif blocks:
            print('So do mermaid : %d — BO QUA (--no-diagrams), se hien ra chu tran' % len(blocks))
        else:
            print('So do mermaid : 0')

        md = os.path.join(work, 'body.md')
        io.open(md, 'w', encoding='utf-8', newline='\n').write(body)
        css = os.path.join(work, 'epub.css')
        io.open(css, 'w', encoding='utf-8', newline='\n').write(EPUB_CSS)

        cmd = ['pandoc', md, '--from=markdown', '--to=epub3', '--standalone',
               '--toc', '--toc-depth=%d' % split_level,
               '--split-level=%d' % split_level,
               '--css=' + css, '--resource-path=' + work,
               '-M', 'title=' + (title or derive_title(body, meta)),
               '-M', 'lang=' + lang, '-o', out]
        if author or meta.get('author'):
            cmd += ['-M', 'author=' + (author or meta['author'])]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise Fail('pandoc that bai:\n%s' % (r.stderr or r.stdout)[-800:])
    finally:
        shutil.rmtree(work, ignore_errors=True)

    expect_left = len(blocks) if (blocks and no_diagrams) else 0
    rep, problems = verify(out, expect_png, expect_left)

    print('')
    print('NGHIEM THU  %s' % out)
    print('  kich thuoc   : %.1f MB' % (os.path.getsize(out) / 1048576.0))
    print('  tep noi dung : %d' % rep['chapters'])
    print('  anh / <img>  : %d / %d' % (rep['png'], rep['img_tags']))
    print('  tham chieu gay: %d' % rep['broken_refs'])
    print('  mermaid sot  : %d' % rep['mermaid_left'])
    print('  bang         : %d' % rep['tables'])
    print('  chu thich an : %d' % rep['comments'])
    if problems:
        raise Fail('Nghiem thu KHONG dat: ' + '; '.join(problems))
    print('  ket luan     : DAT')
    return rep


def main():
    ap = argparse.ArgumentParser(description='Chuyen Markdown sang EPUB, dung so do mermaid offline.')
    ap.add_argument('input')
    ap.add_argument('-o', '--out')
    ap.add_argument('--title')
    ap.add_argument('--author')
    ap.add_argument('--lang', default='vi')
    ap.add_argument('--strip-comments', action='store_true',
                    help='go het chu thich HTML an khoi ban xuat')
    ap.add_argument('--split-level', type=int, default=2,
                    help='cap tieu de de tach tep va lam muc luc (mac dinh 2)')
    ap.add_argument('--scale', type=int, default=3, help='do phan giai so do (mac dinh 3)')
    ap.add_argument('--no-diagrams', action='store_true',
                    help='bo qua viec dung so do (chay duoc khi may khong co mmdc)')
    a = ap.parse_args()

    out = a.out or os.path.splitext(a.input)[0] + '.epub'
    try:
        convert(a.input, out, title=a.title, author=a.author, lang=a.lang,
                strip_comments=a.strip_comments, split_level=a.split_level,
                scale=a.scale, no_diagrams=a.no_diagrams)
    except Fail as e:
        sys.stderr.write('LOI: %s\n' % e)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
