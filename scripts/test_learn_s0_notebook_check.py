# -*- coding: utf-8 -*-
"""Test cho skills/learn/learn-teach/scripts/s0_notebook_check.py.

Chạy: python -m pytest scripts/test_learn_s0_notebook_check.py -v

Lỗi gốc: S0 của learn-teach chạy `nlm notebook create` vô điều kiện, nên /book-to-learn
phải dặn CEO trả lời "đã có notebook" bằng tay — lời dặn, không phải cơ chế. Script này
quyết định DÙNG LẠI / ĐƯỢC TẠO / DỪNG trước khi S0 được phép tạo gì.

Ba sự thật đo trên nlm thật (2026-09-19) mà test phải giữ:
  * `nlm notebook get` trả mã thoát 0 CẢ KHI LỖI → phải đọc "status" trong JSON.
  * Notebook đã xoá: status=error, "NOT_FOUND".
  * Lỗi xác thực ("Authentication expired") KHÔNG phải "không có notebook" — tạo mới
    lúc đó chính là cách sinh notebook trùng. Bỏ NOTEBOOKLM_BASE_URL thường chữa được.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, 'skills', 'learn', 'learn-teach', 'scripts', 's0_notebook_check.py')

FAKE = r'''
import json, os, sys
st = json.load(open(os.environ["FAKE_NLM_STATE"], encoding="utf-8"))
log = os.environ["FAKE_NLM_STATE"] + ".log"
open(log, "a", encoding="utf-8").write(" ".join(sys.argv[1:]) + "\n")
a = sys.argv[1:]
if a[:2] == ["alias", "get"]:
    if a[2] in st.get("aliases", {}):
        print(st["aliases"][a[2]]); sys.exit(0)
    print("Error: Alias '%s' not found" % a[2]); sys.exit(1)
if a[:2] == ["notebook", "get"]:
    auth = st.get("auth", "ok")
    if auth == "expired" or (auth == "expired_with_base" and os.environ.get("NOTEBOOKLM_BASE_URL")):
        print(json.dumps({"status": "error", "error": "Failed to get notebook: Authentication expired. Run 'nlm login'"}))
        sys.exit(0)
    nb = st.get("notebooks", {}).get(a[2])
    if nb is None:
        print(json.dumps({"status": "error", "error": "Failed to get notebook: API error (code 5): NOT_FOUND"}))
    else:
        print(json.dumps(dict(nb, notebook_id=a[2])))
    sys.exit(0)
print("unexpected call", a); sys.exit(9)
'''

ID1 = '8d59b091-688a-4419-8072-caad4108ad19'
ID2 = 'e68dc685-6aff-4e65-84c3-5b848b7a0000'


def lam(tmp_path, resources=None, aliases=None, notebooks=None, auth='ok', base_url=None, slug=None):
    ws = tmp_path / 'ws'
    ws.mkdir()
    if resources is not None:
        (ws / 'RESOURCES.md').write_text(resources, encoding='utf-8')
    fake = tmp_path / 'fake_nlm.py'
    fake.write_text(FAKE, encoding='utf-8')
    state = tmp_path / 'state.json'
    state.write_text(json.dumps({'aliases': aliases or {}, 'notebooks': notebooks or {}, 'auth': auth}),
                     encoding='utf-8')
    env = dict(os.environ, NLM_BIN=str(fake), FAKE_NLM_STATE=str(state))
    env.pop('NOTEBOOKLM_BASE_URL', None)
    if base_url:
        env['NOTEBOOKLM_BASE_URL'] = base_url
    cmd = [sys.executable, SCRIPT, str(ws)] + (['--slug', slug] if slug else [])
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', env=env)
    calls = (tmp_path / 'state.json.log').read_text(encoding='utf-8') if (tmp_path / 'state.json.log').exists() else ''
    return p.returncode, p.stdout + p.stderr, calls


RES = '# Tài Nguyên CFMA\n\n**Notebook NLM:** `learn-cfma` — `%s`\n**Cập nhật nguồn lần cuối:** 2026-09-19\n'


def test_resources_co_id_notebook_con_song_la_dung_lai(tmp_path):
    rc, out, _ = lam(tmp_path, resources=RES % ID1, aliases={'learn-cfma': ID1},
                     notebooks={ID1: {'title': 'Learn: CFMA', 'source_count': 7}})
    assert rc == 0, out
    assert 'DÙNG LẠI' in out and ID1 in out and '7 nguồn' in out


def test_chi_co_alias_btl_goc_tro_san(tmp_path):
    """/book-to-learn L4 trỏ alias learn-<slug> vào notebook btl-<slug>-goc, chưa ghi RESOURCES.md."""
    rc, out, _ = lam(tmp_path, aliases={'learn-profit-first': ID2},
                     notebooks={ID2: {'title': 'btl-profit-first-goc', 'source_count': 12}}, slug='profit-first')
    assert rc == 0, out
    assert 'DÙNG LẠI' in out and ID2 in out


def test_khong_co_gi_thi_duoc_tao(tmp_path):
    rc, out, calls = lam(tmp_path, slug='cfma')
    assert rc == 1, out
    assert 'ĐƯỢC TẠO' in out and 'learn-cfma' in out
    assert 'notebook create' not in calls          # script không bao giờ tự tạo


def test_resources_va_alias_tro_hai_notebook_khac_nhau_la_dung(tmp_path):
    rc, out, _ = lam(tmp_path, resources=RES % ID1, aliases={'learn-cfma': ID2},
                     notebooks={ID1: {'title': 'a', 'source_count': 1}, ID2: {'title': 'b', 'source_count': 1}})
    assert rc == 3, out
    assert 'MÂU THUẪN' in out and ID1 in out and ID2 in out


def test_notebook_da_xoa_la_dung_khong_tao_de(tmp_path):
    rc, out, _ = lam(tmp_path, resources=RES % ID1, aliases={'learn-cfma': ID1}, notebooks={})
    assert rc == 3, out
    assert 'ĐÃ XOÁ' in out or 'NOT_FOUND' in out


def test_loi_xac_thuc_khong_bao_gio_la_duoc_tao(tmp_path):
    """Ma thoat 0 + auth loi ma doc thanh 'khong co notebook' thi S0 tao notebook trung."""
    rc, out, _ = lam(tmp_path, resources=RES % ID1, aliases={'learn-cfma': ID1},
                     notebooks={ID1: {'title': 'x', 'source_count': 3}}, auth='expired')
    assert rc == 2, out
    assert 'ĐƯỢC TẠO' not in out
    assert 'KHÔNG ĐO ĐƯỢC' in out


def test_loi_xac_thuc_do_base_url_thi_thu_lai_khong_co_bien(tmp_path):
    rc, out, calls = lam(tmp_path, resources=RES % ID1, aliases={'learn-cfma': ID1},
                         notebooks={ID1: {'title': 'x', 'source_count': 3}},
                         auth='expired_with_base', base_url='https://notebook.google.com')
    assert rc == 0, out
    assert 'NOTEBOOKLM_BASE_URL' in out               # báo cho người dùng biết đã phải bỏ biến
    assert calls.count('notebook get') == 2


def test_notebook_rong_van_dung_lai_nhung_canh_bao(tmp_path):
    rc, out, _ = lam(tmp_path, resources=RES % ID1, notebooks={ID1: {'title': 'x', 'source_count': 0}})
    assert rc == 0, out
    assert '0 nguồn' in out and 'CẢNH BÁO' in out


def test_notebook_ghi_trong_bang_khong_duoc_coi_la_chua_co(tmp_path):
    """Workspace thật (tu-nha-thau…, 2026-09-19): 3 notebook ghi trong BẢNG, không có dòng
    **Notebook NLM:** chuẩn. Bản đầu trả ĐƯỢC TẠO → S0 sẽ dựng notebook thứ tư."""
    res = ('# Tài Nguyên\n\n## Nguồn cấp 2 — notebook NLM\n\n| Notebook | id | Nguồn |\n|---|---|---|\n'
           '| `Book: x` | `%s` | 15 |\n| `rtb-ext` | `%s` | 40 |\n' % (ID1, ID2))
    rc, out, _ = lam(tmp_path, resources=res, slug='x')
    assert rc == 3, out
    assert 'ĐƯỢC TẠO' not in out
    assert ID1 in out and ID2 in out


def test_resources_khong_co_dong_notebook_va_khong_slug_dung_ten_thu_muc(tmp_path):
    rc, out, _ = lam(tmp_path, resources='# Tài Nguyên\n\nchưa có notebook\n')
    assert rc == 1, out
    assert 'learn-ws' in out                          # slug mặc định = tên thư mục workspace
