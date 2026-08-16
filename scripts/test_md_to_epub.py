"""Test cho md_to_epub.py — chuyen Markdown sang EPUB, dung so do mermaid offline.

Bon lo hong that, gap khi chuyen cuon "Tu Khong Den Mot" (2026-08-16):
  1. Frontmatter `tags: [#type/book]` — dau '#' mo comment YAML giua flow
     sequence -> pandoc chet voi "did not find expected node content".
  2. Khoi ```mermaid do ra chu tran trong EPUB (trinh doc khong chay JS)
     -> 42 so do bien thanh ma nguon.
  3. 118 chu thich HTML an lot nguyen vao EPUB ma khong ai bao.
  4. Giao file hong ma tuong xong — phai mo lai zip doi chieu moi biet.
"""
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, 'md_to_epub.py')

spec = importlib.util.spec_from_file_location('mte', SCRIPT)
mte = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mte)

FAILED = []


def check(name, cond, detail=''):
    print(('PASS ' if cond else 'FAIL ') + name + (('  -> ' + detail) if detail and not cond else ''))
    if not cond:
        FAILED.append(name)


FIXTURE = """---
created: 2026-08-16
type: book
tags: [#type/book, #status/active]
---

# Sach Thu Nghiem

<!-- P7: chu thich bien tap an thu nhat -->

## Chuong 01: Mo dau

Doan van co **dam** va *nghieng*.

<!-- P5: chu thich bien tap an thu hai -->

```mermaid
flowchart LR
    A[Thep tam] --> B[Dap khuon]
    B --> C[Ban thu]
```

| Cot A | Cot B |
|---|---|
| 1 | 2 |

## Chuong 02: Ket

```
// Ma gia — khong phai so do
1. Lay dieu bat dinh dat nhat
```
"""


def write_fixture(d):
    p = os.path.join(d, 'sach.md')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(FIXTURE)
    return p


def epub_facts(path):
    """Mo EPUB nhu zip, tra ve cac con so nghiem thu duoc."""
    z = zipfile.ZipFile(path)
    names = z.namelist()
    xhtml = [n for n in names if n.endswith('.xhtml')]
    body = ''.join(z.read(n).decode('utf-8') for n in xhtml)
    return {
        'zip_ok': z.testzip() is None,
        'png': len([n for n in names if n.lower().endswith('.png')]),
        'img_tags': body.count('<img'),
        'mermaid_left': body.count('"mermaid"'),
        'comments': body.count('<!--'),
        'tables': body.count('<table'),
        'pre': body.count('<pre'),
        'body': body,
    }


def run_cli(*args):
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = 'utf-8'
    return subprocess.run([sys.executable, SCRIPT] + list(args),
                          capture_output=True, text=True, encoding='utf-8', env=env)


# ---------------------------------------------------------------- unit level

body, meta = mte.strip_frontmatter(FIXTURE)
check('frontmatter: bo sach khoi than bai',
      not body.startswith('---') and 'type/book' not in body,
      repr(body[:60]))
check('frontmatter: dau # trong flow sequence khong lam vo ham',
      isinstance(meta, dict), repr(meta))
check('frontmatter: than bai bat dau bang H1',
      body.lstrip().startswith('# Sach Thu Nghiem'), repr(body.lstrip()[:40]))

check('dem so do mermaid', len(mte.find_mermaid_blocks(FIXTURE)) == 1,
      str(len(mte.find_mermaid_blocks(FIXTURE))))
check('khoi ma tran KHONG bi tinh la so do',
      'Ma gia' not in ''.join(mte.find_mermaid_blocks(FIXTURE)))
check('dem chu thich an', mte.count_html_comments(FIXTURE) == 2,
      str(mte.count_html_comments(FIXTURE)))

# ------------------------------------------------------------------ end to end

with tempfile.TemporaryDirectory() as d:
    src = write_fixture(d)

    # --- ca 1: chay mac dinh, co dung so do
    out = os.path.join(d, 'mac-dinh.epub')
    r = run_cli(src, '-o', out)
    check('CLI: chay xong khong loi', r.returncode == 0,
          (r.stdout + r.stderr)[-500:])

    if os.path.exists(out):
        f = epub_facts(out)
        check('EPUB: zip toan ven', f['zip_ok'])
        check('so do mermaid thanh anh PNG nhung trong', f['png'] == 1, str(f['png']))
        check('co dung 1 the <img>', f['img_tags'] == 1, str(f['img_tags']))
        check('KHONG con khoi mermaid tran', f['mermaid_left'] == 0, str(f['mermaid_left']))
        check('bang duoc giu', f['tables'] == 1, str(f['tables']))
        check('khoi ma tran van la <pre>', f['pre'] == 1, str(f['pre']))
        check('frontmatter khong lot vao than bai', 'type/book' not in f['body'])
        check('mac dinh GIU chu thich an', f['comments'] == 2, str(f['comments']))
        check('bao cao noi ro so chu thich an', '2' in r.stdout and 'comment' in r.stdout.lower(),
              r.stdout[-300:])
    else:
        check('EPUB: file duoc tao', False, 'khong thay ' + out)

    # --- ca 2: --strip-comments phai don sach chu thich
    out2 = os.path.join(d, 'sach-clean.epub')
    r2 = run_cli(src, '-o', out2, '--strip-comments')
    check('CLI --strip-comments: chay xong', r2.returncode == 0,
          (r2.stdout + r2.stderr)[-500:])
    if os.path.exists(out2):
        f2 = epub_facts(out2)
        check('--strip-comments: sach chu thich an', f2['comments'] == 0, str(f2['comments']))
        check('--strip-comments: so do van con', f2['png'] == 1, str(f2['png']))

    # --- ca 3: --no-diagrams phai chay duoc khi may KHONG co mmdc
    out3 = os.path.join(d, 'khong-so-do.epub')
    r3 = run_cli(src, '-o', out3, '--no-diagrams')
    check('CLI --no-diagrams: chay xong', r3.returncode == 0,
          (r3.stdout + r3.stderr)[-500:])
    if os.path.exists(out3):
        f3 = epub_facts(out3)
        check('--no-diagrams: khong nhung anh', f3['png'] == 0, str(f3['png']))

    # --- ca 4: dau vao khong ton tai phai bao loi ro, khong no stack trace
    r4 = run_cli(os.path.join(d, 'khong-co-that.md'))
    check('dau vao thieu: thoat khac 0', r4.returncode != 0, str(r4.returncode))
    check('dau vao thieu: bao loi doc duoc, khong Traceback',
          'Traceback' not in r4.stderr, r4.stderr[-300:])

print()
if FAILED:
    print('%d FAILED: %s' % (len(FAILED), ', '.join(FAILED)))
    sys.exit(1)
print('Tat ca PASS')
