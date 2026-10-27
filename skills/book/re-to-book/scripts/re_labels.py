# -*- coding: utf-8 -*-
"""Nhan tri thuc (knowledge/conjecture/assumption) + tran muc tin (L/M/H).

Tran mien chi chi phoi MUC TIN, khong sinh nhan tri thuc. stdlib only.
"""
import re
from dataclasses import dataclass

from re_units import Unit, normalize

LABEL_RANK = {'knowledge': 3, 'conjecture': 2, 'assumption': 1}
CONF_RANK = {'L': 1, 'M': 2, 'H': 3}

_W = r'(?<!\w)(?:%s)(?!\w)'
_VOCAB = [
    ('knowledge', re.compile(_W % r'đã biết|tri thức|knowledge', re.I)),
    ('conjecture', re.compile(_W % r'phỏng đoán|conjecture', re.I)),
    ('assumption', re.compile(_W % r'giả định|assumption', re.I)),
]
_FILE_CAP = re.compile(
    r'mọi\s.{0,60}?(?:≤|tối đa|không quá|chỉ)\s*(phỏng đoán|giả định)', re.I | re.S)
_CONF_INLINE = re.compile(r'(?i:mức)\s+([LMH])\b')
_CONF_HEAD = re.compile(r'mức tin|confidence', re.I)
_CEIL_LINE = re.compile(r'^confidence_ceiling:[ \t]*(.*)$', re.M)
_LETTER = re.compile(r'\b([LMH])\b')


@dataclass
class Label:
    label: str
    source: str
    confidence: str
    confidence_source: str


def file_cap(units):
    """Tuyen bo cap tep trong _preamble hoac muc dau."""
    for u in units[:2]:
        if u.kind not in ('preamble', 'file', 'section', 'gt_item'):
            continue
        m = _FILE_CAP.search(normalize(u.text))
        if m:
            return 'conjecture' if m.group(1).lower() == 'phỏng đoán' else 'assumption'
        if u.kind == 'preamble':
            continue
        break
    return None


def ceiling_from_state(state_text):
    t = state_text.replace('﻿', '').replace('\r\n', '\n')
    if not t.startswith('---\n'):
        return None
    end = re.search(r'^---[ \t]*$', t[4:], re.M)
    if not end:
        return None
    fm = t[4:4 + end.start()]
    m = _CEIL_LINE.search(normalize(fm))
    if not m:
        return None
    letters = _LETTER.findall(m.group(1))
    if not letters:
        return None
    return min(letters, key=CONF_RANK.get)


def _table_conf(text):
    """Chi nhan o L/M/H nam duoi cot co tieu de 'Muc tin'/'confidence'."""
    out, col = [], None
    for ln in text.split('\n'):
        if not ln.lstrip().startswith('|'):
            col = None
            continue
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        if col is None:
            for i, c in enumerate(cells):
                if _CONF_HEAD.search(c):
                    col = i
            continue
        if col < len(cells) and cells[col] in CONF_RANK:
            out.append(cells[col])
    return out


def _low(rank_map, vals):
    return min(vals, key=rank_map.get)


def resolve(unit: Unit, cap, ceiling) -> Label:
    text = normalize(unit.text)
    found = [name for name, rx in _VOCAB if rx.search(text)]
    if found:
        label, source = _low(LABEL_RANK, found), 'tại chỗ'
        if cap and LABEL_RANK[label] > LABEL_RANK[cap]:
            label = cap
    elif cap:
        label, source = cap, 'kế thừa: tệp'
    else:
        label, source = 'chưa gán', 'chưa gán'

    letters = _CONF_INLINE.findall(text) + _table_conf(text)
    if letters:
        conf, csrc = _low(CONF_RANK, letters), 'tại chỗ'
        if ceiling and CONF_RANK[conf] > CONF_RANK[ceiling]:
            conf, csrc = ceiling, 'kế thừa: trần miền'
    elif ceiling:
        conf, csrc = ceiling, 'kế thừa: trần miền'
    else:
        conf, csrc = None, 'không có'
    return Label(label, source, conf, csrc)
