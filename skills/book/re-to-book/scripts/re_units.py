# -*- coding: utf-8 -*-
"""Tach ho so RE (markdown) thanh don vi co bam (sha256) de neo/kiem drift.

Luat tach: xem SKILL /re-to-book. stdlib only.
"""
import hashlib
import re
import unicodedata
from dataclasses import dataclass

ROW_CODE = re.compile(r'^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-\d+[a-z]?$')

_GT_HEAD = re.compile(r'^##\s+(GT-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*)(?![A-Za-z0-9-])')
_HEAD = re.compile(r'^(#{2,3})\s+(.*?)\s*#*\s*$')
_ITEM = re.compile(r'^([1-9])\.\s')
_ROW = re.compile(r'^\s*\|\s*([^|]*?)\s*\|')
_FENCE = re.compile(r'^\s*(```|~~~)')


def normalize(text: str) -> str:
    t = text.replace('﻿', '')
    t = unicodedata.normalize('NFC', t)
    t = t.replace('\r\n', '\n').replace('\r', '\n')
    t = '\n'.join(ln.rstrip() for ln in t.split('\n'))
    return t.strip()


@dataclass
class Unit:
    id: str
    kind: str  # 'section'|'gt_item'|'row'|'file'|'preamble'
    text: str
    sha256: str


def _sha(text: str) -> str:
    return hashlib.sha256(normalize(text).encode('utf-8')).hexdigest()


def _strip_frontmatter(text: str) -> str:
    t = text.replace('﻿', '').replace('\r\n', '\n').replace('\r', '\n')
    if t.startswith('---\n'):
        m = re.search(r'^---[ \t]*$', t[4:], re.M)
        if m:
            return t[4 + m.end():].lstrip('\n')
    return t


def _row_code(line: str):
    m = _ROW.match(line)
    if not m:
        return None
    cell = m.group(1).replace('**', '').replace('`', '').strip()
    # o ma co the kem ghi chu sau ma ("N-009 ✅ ĐÃ TRẢ …") — lay tu dau tien
    tok = cell.split()[0] if cell else ''
    return tok if ROW_CODE.match(tok) else None


def table_item(line):
    """So muc 1-9 neu dong la hang bang co o dau la mot chu so (bo **, dau cach)."""
    m = _ROW.match(line)
    if not m:
        return None
    cell = m.group(1).replace('**', '').strip()
    return cell if re.fullmatch(r'[1-9]', cell) else None


def split_units(text: str) -> list:
    body = _strip_frontmatter(text)
    # entries: [id, kind, lines]; thu tu theo luc xuat hien
    entries = []
    cur = ['_preamble', 'preamble', []]
    entries.append(cur)
    gt = None  # id phieu GT dang mo
    gt_entry = None  # muc .0 cua phieu dang mo
    in_row_item = False  # cur la muc dang hang bang
    in_fence = False
    has_heading = False
    has_row = False

    for line in body.split('\n'):
        if _FENCE.match(line):
            in_fence = not in_fence
            cur[2].append(line)
            continue
        if not in_fence:
            g = _GT_HEAD.match(line)
            h = _HEAD.match(line)
            if g:
                has_heading = True
                gt = g.group(1)
                cur = gt_entry = [gt + '.0', 'gt_item', [line]]
                in_row_item = False
                entries.append(cur)
                continue
            if h:
                has_heading = True
                gt = None
                in_row_item = False
                # bo backtick: neo dat trong backtick, ma don vi khong duoc chua backtick
                title = normalize(h.group(2)).replace('`', '').strip()
                cur = [title, 'section', [line]]
                entries.append(cur)
                continue
            if gt:
                ti = table_item(line)
                if ti:
                    cur = ['%s.%s' % (gt, ti), 'gt_item', [line]]
                    in_row_item = True
                    entries.append(cur)
                    continue
                if in_row_item and _ROW.match(line):
                    # hang bang khac dong muc dang hang; ve lai muc .0
                    cur, in_row_item = gt_entry, False
            code = _row_code(line)
            if code:
                has_row = True
                entries.append(['row:' + code, 'row', [line]])
                continue
            if gt:
                it = _ITEM.match(line)
                if it:
                    cur = ['%s.%s' % (gt, it.group(1)), 'gt_item', [line]]
                    in_row_item = False
                    entries.append(cur)
                    continue
        cur[2].append(line)

    out = []
    seen = {}
    for uid, kind, lines in entries:
        txt = normalize('\n'.join(lines))
        if kind == 'preamble' and not txt:
            continue
        if kind == 'preamble' and not has_heading and not has_row:
            uid, kind = 'file', 'file'
        n = seen.get(uid, 0) + 1
        seen[uid] = n
        if n > 1:
            uid = '%s~%d' % (uid, n)
        out.append(Unit(id=uid, kind=kind, text=txt, sha256=_sha(txt)))
    return out
