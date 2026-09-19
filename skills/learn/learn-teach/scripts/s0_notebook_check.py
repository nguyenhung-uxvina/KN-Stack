# -*- coding: utf-8 -*-
"""Cổng trước khi S0 được tạo notebook: DÙNG LẠI / ĐƯỢC TẠO / DỪNG.

Vì sao tồn tại
--------------
S0 của learn-teach từng chạy `nlm notebook create` vô điều kiện. /book-to-learn L4 đã
trỏ sẵn alias `learn-<slug>` vào notebook toàn văn `btl-<slug>-goc` và chép sẵn
RESOURCES.md, rồi phải DẶN CEO trả lời "đã có notebook" để S0 khỏi dựng notebook thứ
hai. Lời dặn không phải cơ chế. Script này đọc cả hai chỗ trỏ (RESOURCES.md, alias) và
hỏi NLM notebook còn sống không, trước khi bất cứ thứ gì được tạo.

Ba sự thật đo trên nlm thật (2026-09-19):
  * `nlm notebook get -j` trả mã thoát 0 CẢ KHI LỖI — phải đọc "status" trong JSON.
  * Notebook đã xoá → "NOT_FOUND". Lỗi xác thực → "Authentication expired".
  * Lỗi xác thực KHÔNG có nghĩa "không có notebook". Coi nó là "được tạo" chính là
    cách sinh notebook trùng. Bỏ NOTEBOOKLM_BASE_URL thường chữa được (đảo chiều so
    với trước 17/09) — script tự thử lại một lần không có biến đó.

Dùng
----
    python s0_notebook_check.py <thư mục workspace> [--slug X]

Mã thoát: 0 = DÙNG LẠI (in id) · 1 = ĐƯỢC TẠO (không có gì trỏ tới notebook nào) ·
2 = KHÔNG ĐO ĐƯỢC (NLM không trả lời được — KHÔNG tạo) · 3 = DỪNG, hỏi người dùng
(hai chỗ trỏ mâu thuẫn, hoặc trỏ tới notebook đã xoá).
Script không bao giờ tự tạo hay sửa gì.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

UUID = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def _nlm(args, bo_base_url=False):
    ben_ngoai = os.environ.get('NLM_BIN')        # test đặt một nlm giả
    cmd = [sys.executable, ben_ngoai] if ben_ngoai else ['nlm']
    env = dict(os.environ)
    if bo_base_url:
        env.pop('NOTEBOOKLM_BASE_URL', None)
    p = subprocess.run(cmd + args, capture_output=True, text=True, encoding='utf-8',
                       errors='replace', env=env)
    return p.returncode, (p.stdout or '') + (p.stderr or '')


def doc_resources(ws):
    """→ (alias, id của dòng **Notebook NLM:**, mọi UUID khác nhắc trong tệp)."""
    p = os.path.join(ws, 'RESOURCES.md')
    if not os.path.isfile(p):
        return None, None, []
    van = io.open(p, encoding='utf-8-sig').read()
    alias = nid = None
    for dong in van.splitlines():
        if 'Notebook NLM' in dong:
            a = re.search(r'`(learn-[\w-]+)`', dong)
            m = re.search(UUID, dong)
            alias, nid = (a.group(1) if a else None), (m.group(0) if m else None)
            break
    # Workspace thật (tu-nha-thau…) ghi 3 notebook trong BẢNG, không có dòng chuẩn. Chỉ
    # đọc dòng chuẩn thì báo "chưa có" → S0 dựng notebook thứ tư. Mọi UUID đều phải tính.
    khac = [u for u in dict.fromkeys(re.findall(UUID, van)) if u != nid]
    return alias, nid, khac


def alias_get(ten):
    rc, out = _nlm(['alias', 'get', ten])
    m = re.search(UUID, out)
    if rc == 0 and m:
        return m.group(0), None
    if rc == 1 and 'not found' in out.lower():
        return None, None
    return None, 'nlm alias get %s trả mã %d: %s' % (ten, rc, out.strip()[:200])


def notebook_get(nid):
    """→ ('song', info) | ('xoa', msg) | ('loi', msg). Thử lại không NOTEBOOKLM_BASE_URL khi lỗi xác thực."""
    lan_thu = [False] + ([True] if os.environ.get('NOTEBOOKLM_BASE_URL') else [])
    msg = ''
    for bo in lan_thu:
        _, out = _nlm(['notebook', 'get', nid, '-j'], bo_base_url=bo)
        try:
            j = json.loads(out[out.find('{'):]) if '{' in out else {}
        except ValueError:
            j = {}
        if j.get('notebook_id'):
            j['_bo_base_url'] = bo
            return 'song', j
        msg = j.get('error') or out.strip()[:200]
        if 'NOT_FOUND' in msg:
            return 'xoa', msg
    return 'loi', msg


def main(argv=None):
    ap = argparse.ArgumentParser(description='Cổng trước khi S0 tạo notebook')
    ap.add_argument('ws', help='thư mục workspace learn-teach')
    ap.add_argument('--slug', default=None)
    a = ap.parse_args(argv)

    ws = os.path.abspath(a.ws)
    alias_res, id_res, uuid_khac = doc_resources(ws)
    slug = a.slug or (alias_res[len('learn-'):] if alias_res else os.path.basename(ws).lower())
    alias = alias_res or 'learn-' + slug

    id_alias, loi = alias_get(alias)
    if loi:
        print('KHÔNG ĐO ĐƯỢC: %s\nKHÔNG tạo notebook. Sửa nlm (xem /nlm-refresh) rồi chạy lại.' % loi)
        return 2
    print('RESOURCES.md: %s · alias %s: %s' % (id_res or 'không ghi notebook', alias, id_alias or 'chưa có'))

    ids = {i for i in (id_res, id_alias) if i}
    if len(ids) > 1:
        print('MÂU THUẪN: RESOURCES.md trỏ %s, alias %s trỏ %s. DỪNG — hỏi người dùng giữ notebook '
              'nào; không tạo cái thứ ba.' % (id_res, alias, id_alias))
        return 3
    if not ids and uuid_khac:
        print('DỪNG: RESOURCES.md không có dòng **Notebook NLM:** chuẩn nhưng nhắc tới %d id: %s. '
              'Hỏi người dùng notebook nào là notebook thường trực, rồi ghi dòng chuẩn + '
              '`nlm alias set %s <id>`. Không tạo notebook mới.' % (len(uuid_khac), ', '.join(uuid_khac), alias))
        return 3
    if not ids:
        print('ĐƯỢC TẠO: không chỗ nào trỏ tới notebook cho workspace này. Tạo notebook, rồi '
              '`nlm alias set %s <id>` và ghi dòng **Notebook NLM:** vào RESOURCES.md.' % alias)
        return 1

    nid = ids.pop()
    tt, info = notebook_get(nid)
    if tt == 'xoa':
        print('ĐÃ XOÁ: %s trỏ tới notebook %s nhưng NLM báo NOT_FOUND. DỪNG — hỏi người dùng '
              '(dựng lại từ RESOURCES.md hay bỏ); đừng lặng lẽ tạo mới.' % (alias, nid))
        return 3
    if tt == 'loi':
        print('KHÔNG ĐO ĐƯỢC: không hỏi được NLM notebook %s còn sống không — %s\n'
              'KHÔNG tạo notebook: lỗi xác thực không có nghĩa là không có notebook.' % (nid, info))
        return 2

    n = info.get('source_count')
    print('DÙNG LẠI: %s — "%s" · %s nguồn' % (nid, info.get('title', '?'), n if n is not None else '?'))
    if info.get('_bo_base_url'):
        print('Lưu ý: chỉ trả lời được khi BỎ biến NOTEBOOKLM_BASE_URL — các lệnh nlm sau cũng chạy không có biến này.')
    if n == 0:
        print('CẢNH BÁO: notebook 0 nguồn — dùng lại, nhưng S0 phải nạp nguồn đã duyệt trước khi soạn bài.')
    if not id_alias:
        print('Thiếu alias → chạy `nlm alias set %s %s`.' % (alias, nid))
    if not id_res:
        print('RESOURCES.md chưa ghi notebook → thêm dòng: **Notebook NLM:** `%s` — `%s`' % (alias, nid))
    return 0


if __name__ == '__main__':
    sys.exit(main())
