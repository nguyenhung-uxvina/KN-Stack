# -*- coding: utf-8 -*-
r"""CONG DATA BUS — chan pipeline sach khong cho qua pha khi thieu hien vat.

Vi sao ton tai
--------------
Bang Data Bus trong SKILL.md da DAC TA du P5-Review, P6-Revised, P8-Manifest tu dau.
Ngay 2026-08-23, mot lan chay that (pahl-beitz-tap2, 18 chuong, 186k tu) bao cao
"P5 OK · P6 OK · P8 OK" ma KHONG co file nao trong ba. Ra soat va hieu chinh duoc lam
TAI CHO tren Phase4, phat hien chi ghi vao _pipeline_state.md. CEO hoi "khong thay thu
muc Phase6?" moi lo ra.

Dac ta ton tai != dac ta duoc thi hanh. File nay bien no thanh mot lenh.

Chay
----
    python databus_check.py <output_dir> --phase P5
    python databus_check.py <output_dir> --all
Ma thoat != 0 = THIEU HIEN VAT. Orchestrator KHONG duoc trinh checkpoint khi != 0.
"""
import os, sys, glob, argparse

# (pha, mo ta, [cac duong dan bat buoc], [cac duong dan it nhat mot])
SPEC = [
    ('P1', 'Tham do', [], ['Phase1-Exploration/P1_Synthesis.md']),
    ('P2', 'Dinh vi', ['Phase2-Positioning.md'], []),
    ('P3', 'Outline', ['Phase3-Outline.md'], []),
    ('P4', 'Viet', [], ['Phase4-Chapters/Ch*_Draft.md', 'Phase4-Drafts/Ch*_Draft.md']),
    ('P5', 'Ra soat', ['Phase5-Review.md'], []),
    ('P6', 'Hieu chinh', [], ['Phase6-Revised/Ch*.md', 'Phase6-Revise.md']),
    ('P7', 'Kiem IP', [], ['Phase7-Audit-Log.md', 'Phase7-DoiNgoai/*.md']),
    ('P8', 'Notebook', [], ['Phase8-Notebook-Manifest.md', 'Phase8-Notebook.md']),
    ('P9', 'CEO insight', ['Phase9-CEO-Insights.md'], []),
]

# hien vat rong = coi nhu khong co (chan "tao file cho co")
MIN_BYTES = 400


def has(root, pat):
    hits = [p for p in glob.glob(os.path.join(root, pat))
            if os.path.isfile(p) and os.path.getsize(p) >= MIN_BYTES]
    return hits


def check(root, phases):
    thieu, mong, ok = [], [], []
    for ph, ten, must, anyof in SPEC:
        if phases and ph not in phases:
            continue
        found = []
        miss = []
        for pat in must:
            h = has(root, pat)
            (found if h else miss).extend(h or [pat])
        if anyof:
            h = []
            for pat in anyof:
                h += has(root, pat)
            if h:
                found += h
            else:
                miss.append(' | '.join(anyof))
        # file ton tai nhung qua nho
        for pat in must + anyof:
            for p in glob.glob(os.path.join(root, pat)):
                if os.path.isfile(p) and os.path.getsize(p) < MIN_BYTES:
                    mong.append('%s: %s chi %d byte' % (ph, os.path.basename(p),
                                                        os.path.getsize(p)))
        if miss:
            thieu.append((ph, ten, miss))
        else:
            ok.append((ph, ten, len(found)))

    print('=' * 76)
    print('CONG DATA BUS — %s' % os.path.abspath(root))
    print('=' * 76)
    for ph, ten, n in ok:
        print('  [OK  ] %-3s %-14s %d hien vat' % (ph, ten, n))
    for x in mong:
        print('  [CANH] ' + x)
    for ph, ten, miss in thieu:
        print('  [CHAN] %-3s %-14s THIEU: %s' % (ph, ten, '; '.join(miss)))
    print('=' * 76)
    if thieu:
        print('THIEU %d pha. Orchestrator KHONG duoc trinh checkpoint.' % len(thieu))
        print('Lam ra hien vat truoc — dung ghi phat hien vao _pipeline_state.md roi bao xong.')
    else:
        print('DU HIEN VAT — duoc phep trinh checkpoint.')
    return 1 if thieu else 0


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('output_dir')
    ap.add_argument('--phase', action='append', default=[])
    ap.add_argument('--all', action='store_true')
    a = ap.parse_args()
    if not os.path.isdir(a.output_dir):
        print('KHONG CO THU MUC: ' + a.output_dir)
        sys.exit(2)
    sys.exit(check(a.output_dir, [] if a.all else a.phase))
