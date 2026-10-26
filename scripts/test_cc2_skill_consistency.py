"""Test nhat quan cho bo skill helix-cc2: orchestrator <-> references <-> cac khoi.

Task 4 chi kiem phia orchestrator. Vong kiem phia khoi duoc danh dau xfail(strict=True)
trong PENDING; Task 5-8 xoa ten khoi khoi PENDING khi khoi do da duoc viet.
"""
import glob
import os
import re

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
HELIX = os.path.join(REPO, 'skills', 'helix')
ORCH_DIR = os.path.join(HELIX, 'helix-cc2')
ORCH = os.path.join(ORCH_DIR, 'SKILL.md')
REF_DIR = os.path.join(ORCH_DIR, 'references')
VIEW_OPS = os.path.join(REF_DIR, 'view-ops.md')

MODES = ['--project', '--function', '--improve', '--analyze']
OPS = {'zoom-in', 'zoom-out', 'shift', 'state', 'view', 'observe'}

# Khoi -> tep ma khoi ay ghi (khop bang Data Bus cua orchestrator).
BLOCK_OUTPUTS = {
    'helix-cc2-frame': ['{{prefix}}CC2_C0_Frame.md'],
    'helix-cc2-chain': ['{{prefix}}CC2_C1_Chains.md'],
    'helix-cc2-form': ['{{prefix}}CC2_C2_Forms.md'],
    'helix-cc2-param': ['{{prefix}}CC2_C3_Params.md'],
    'helix-cc2-hypo': ['{{prefix}}CC2_C4_Hypotheses.md', '{{prefix}}CC2_C4_Test_Plan.md'],
    'helix-cc2-analyze': ['{{prefix}}CC2_CA_Analysis.md'],
    'helix-cc2-handoff': ['{{prefix}}CC2_C6_Crosscheck.md', '{{prefix}}CC2_Handoff.md'],
}
ORCH_OUTPUTS = ['_pipeline_state.md']

# Khoi chua viet (Task 5-8). Moi task xoa ten khoi cua minh khoi tap nay.
PENDING = {
    'helix-cc2-handoff',
}

VN_CHAR = re.compile(
    '[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]',
    re.IGNORECASE,
)


def _read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def _orch():
    assert os.path.isfile(ORCH), 'thieu orchestrator skills/helix/helix-cc2/SKILL.md'
    return _read(ORCH)


def _frontmatter(text):
    m = re.match(r'^---\r?\n(.*?)\r?\n---\r?\n', text, re.DOTALL)
    assert m, 'thieu khoi frontmatter YAML o dau tep'
    fm = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if km:
            fm[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return fm


def _section(text, heading_re, level):
    """Tra noi dung tu tieu de khop heading_re (muc `level`) toi tieu de cung/cao muc ke tiep."""
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        hm = re.match(r'^(#{1,6})\s+(.*)$', line)
        if hm:
            if inside and len(hm.group(1)) <= level:
                break
            if len(hm.group(1)) == level and re.search(heading_re, hm.group(2)):
                inside = True
                continue
        if inside:
            out.append(line)
    return '\n'.join(out) if inside else None


def _skill_files():
    files = []
    for d in glob.glob(os.path.join(HELIX, 'helix-cc2*')):
        for root, _dirs, names in os.walk(d):
            for n in names:
                if n.endswith('.md') or n.endswith('.py') or n.endswith('.json'):
                    files.append(os.path.join(root, n))
    return files


def _data_bus_rows(text):
    sec = _section(text, r'^Data Bus\b', 2)
    assert sec is not None, 'thieu muc `## Data Bus`'
    rows = []
    for line in sec.splitlines():
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 3 or not line.strip().startswith('|'):
            continue
        if cells[0].startswith('---') or cells[0] == 'Tệp':
            continue
        rows.append((cells[0].strip('`'), cells[1], cells[2]))
    return rows


# --------------------------------------------------------------------------- tests


def test_frontmatter():
    paths = glob.glob(os.path.join(HELIX, 'helix-cc2*', 'SKILL.md'))
    _orch()
    for p in paths:
        fm = _frontmatter(_read(p))
        dirname = os.path.basename(os.path.dirname(p))
        assert fm.get('name') == dirname, f'{p}: name={fm.get("name")!r} != {dirname!r}'
        desc = fm.get('description', '')
        assert 'Triggers on:' in desc, f'{p}: description thieu "Triggers on:"'
        assert VN_CHAR.search(desc), f'{p}: description khong co chu tieng Viet co dau'


def test_du_bon_che_do():
    text = _orch()
    for flag in MODES:
        assert re.search(re.escape(flag) + r'\b', text), f'orchestrator thieu co che do {flag}'


def test_op_khop_view_ops():
    text = _orch()
    sec = _section(text, r'--op', 2) or _section(text, r'--op', 3)
    assert sec is not None, 'orchestrator thieu muc tieu de co chua `--op`'
    orch_ops = set(re.findall(r'^\|\s*`([a-z-]+)`\s*\|', sec, re.MULTILINE))
    ref_ops = set(re.findall(r'^###\s+([a-z-]+)\s*$', _read(VIEW_OPS), re.MULTILINE))
    assert orch_ops == ref_ops == OPS, f'orchestrator={orch_ops} view-ops={ref_ops}'


def test_data_bus_khop_khoi():
    rows = _data_bus_rows(_orch())
    files = [r[0] for r in rows]
    expected = [f for outs in BLOCK_OUTPUTS.values() for f in outs] + ORCH_OUTPUTS
    assert sorted(files) == sorted(expected), f'Data Bus={files}'
    writer = {r[0]: r[1] for r in rows}
    for block, outs in BLOCK_OUTPUTS.items():
        for f in outs:
            assert block in writer[f], f'{f}: cot "Ghi bởi" khong ghi {block}'
    assert 'helix-cc2' in writer['_pipeline_state.md']


@pytest.mark.parametrize('block', [
    pytest.param(b, marks=pytest.mark.xfail(strict=True, reason='block not yet written (Task 5–8)'))
    if b in PENDING else b
    for b in BLOCK_OUTPUTS
])
def test_data_bus_khop_khoi_phia_khoi(block):
    path = os.path.join(HELIX, block, 'SKILL.md')
    assert os.path.isfile(path), f'thieu {path}'
    text = _read(path)
    for f in BLOCK_OUTPUTS[block]:
        assert f in text, f'{block}/SKILL.md khong nhac tep minh ghi: {f}'


def test_khong_duong_dan_cheo():
    _orch()
    for p in _skill_files():
        for i, line in enumerate(_read(p).splitlines(), 1):
            assert '../' not in line, f'{p}:{i}: duong dan cheo "../"'


def test_khong_tro_1_projects():
    _orch()
    for p in _skill_files():
        for i, line in enumerate(_read(p).splitlines(), 1):
            if '1_Projects/' not in line:
                continue
            if 'cấm' in line or 'KHÔNG' in line:
                continue  # dong neu luat cam
            if 'Function_Structure' in line or 'Phase3-Embodiment' in line:
                continue  # dau vao runtime cua --project
            pytest.fail(f'{p}:{i}: tro toi 1_Projects/ ngoai luat cam: {line.strip()}')


def test_tro_references_ton_tai():
    """Moi `helix-cc2:references:<ten>` tro toi tep that; moi `§<tieu de>` ngay sau tro toi tieu de that."""
    text = _orch()
    refs = re.findall(r'helix-cc2:references:([A-Za-z0-9-]+)`?(?:\s*§([^\n]*))?', text)
    assert refs, 'orchestrator khong tro reference nao'
    for name, tail in refs:
        path = os.path.join(REF_DIR, name + '.md')
        assert os.path.isfile(path), f'tro toi reference khong ton tai: {name}'
        if tail:
            heads = [h.strip() for h in re.findall(r'^#{2,3}\s+(.*)$', _read(path), re.MULTILINE)]
            assert any(tail.startswith(h) for h in heads), f'{name}: khong co tieu de khop "§{tail[:40]}"'


def test_cum_tu_eval_tinh():
    """Eval tinh doc rieng orchestrator + references, nen orchestrator phai tu nhac cac y nay (R-PF2)."""
    text = _orch()
    for phrase in ['≥3 chuỗi', 'cc2_sheet_lint', 'CC2_Handoff', 'Phép thử nhỏ nhất để bác bỏ',
                   'Rào cản quan sát', 'tri thức / phỏng đoán / giả định', 'PHIẾU GIẢ THUYẾT',
                   '≤3 chức năng tới hạn', 'quy ước bộ skill']:
        assert phrase in text, f'orchestrator thieu cum: {phrase}'
    assert re.search(r'bằng chứng[^\n]{0,80}yếu', text, re.IGNORECASE), 'thieu cau canh bao bang chung yeu'
    assert re.search(r'≥3 chuỗi[^\n]{0,120}quy ước bộ skill', text), '≥3 chuỗi chua gan nhan quy ước bộ skill'


def test_analyze_khong_phai_re():
    """--analyze chi cho hinh the cua chinh Xuong, khong Purpose Gate/ACCESS LEVEL; doi thu -> /reverse-engineering."""
    sec = _section(_orch(), r'^`--analyze`', 3)
    assert sec is not None, 'thieu muc `### --analyze`'
    assert re.search(r'chính Xưởng', sec), '--analyze chua gioi han vao hinh the cua chinh Xuong'
    assert 'Purpose Gate' in sec and 'ACCESS LEVEL' in sec, '--analyze chua noi khong co Purpose Gate / ACCESS LEVEL'
    assert re.search(r'đối thủ[^\n]*/reverse-engineering', sec), 'thieu tro doi thu/ben khac -> /reverse-engineering'
    assert 'CC2_CA_Analysis.md' in sec, '--analyze -> C4 chua noi C4 doc gia thuyet nhap trong CA'


def test_op_tien_to_f_id():
    """Cu phap dich --op co tien to <F-id>/ tuy chon, bat buoc o che do du an khi >1 chuc nang con mo."""
    sec = _section(_orch(), r'--op', 2)
    assert sec is not None
    assert '[<F-id>/]<chuỗi>[:<phần tử>[→<phần tử>]]' in sec, 'cu phap dich thieu tien to [<F-id>/]'
    assert re.search(r'--op \S+ F\d+/[A-Z]', sec), 'thieu vi du --op voi tien to F-id'
    assert re.search(r'`<F-id>/`[^\n]*bắt buộc', sec), 'chua noi tien to F-id bat buoc o che do du an'
    assert 'current_f' in _orch(), '_pipeline_state.md chua theo doi F-id hien hanh'


def test_cong_va_chay_tiep():
    text = _orch()
    assert '⛔ = dừng, chờ CEO trả lời' in text, 'thieu luat dung o cong'
    assert re.search(r'`--op`, `--from`, `--only`[^\n]*_pipeline_state', text, re.DOTALL) or \
        re.search(r'--op`, `--from`, `--only` không cần cờ chế độ', text), 'thieu luat co phu doc trang thai'
    assert re.search(r'Không bao giờ dựng giả tệp thượng nguồn', text), 'thieu luat --from khi thieu tep thuong nguon'
    assert '<nơi ghi>/<F-id>/' in text, 'thieu thu muc theo chuc nang con'


def _block(name):
    path = os.path.join(HELIX, name, 'SKILL.md')
    assert os.path.isfile(path), f'thieu {path}'
    return _read(path)


def test_c0_c1_tieu_de():
    c0 = _block('helix-cc2-frame')
    for h in ['## Chức năng', '## Thông số chức năng', '## Connector biên', '## Nguyên lý',
              '## Sàng chức năng con', '## Hình thể hiện có']:
        assert h in c0, f'C0 thieu tieu de {h}'
    assert '## Chạy riêng' in c0
    assert 'Nhãn' in c0 and 'Nguồn số' in c0
    assert 'cc2_sheet_lint.py' in c0 and '--kind params' in c0
    c1 = _block('helix-cc2-chain')
    for phrase in ['≥3', '≥2 miền', 'lệch P2 — CEO quyết', 'sửa tối thiểu', 'Khác chuỗi', '## Phép nên làm tiếp', 'Mermaid',
                   '## Chạy riêng']:
        assert phrase in c1, f'C1 thieu cum: {phrase}'


def test_c1_khong_lan_p2():
    c1 = _block('helix-cc2-chain')
    assert 'không dựng ma trận hình thái' in c1
    assert 'VDI 2225' in c1 and 'nguồn ý' in c1


def _unknown_flags(block_text, orch_text):
    """Co `--x` trong khoi ma orchestrator khong co dung nguyen co `--x` (khop ca tu)."""
    bad = []
    for flag in sorted(set(re.findall(r'(?<![\w-])--([a-z][a-z-]*)(?![\w-])', block_text))):
        if not re.search(r'(?<![\w-])--' + re.escape(flag) + r'(?![\w-])', orch_text):
            bad.append('--' + flag)
    return bad


def test_co_la_bat_duoc_tien_to():
    assert _unknown_flags('chay --f <F-id>', 'co --function va --out') == ['--f']
    assert _unknown_flags('chay --function x', 'co --function va --out') == []


def test_khoi_khong_co_co_la():
    orch = _orch()
    for b in BLOCK_OUTPUTS:
        path = os.path.join(HELIX, b, 'SKILL.md')
        if not os.path.isfile(path):
            continue
        assert _unknown_flags(_read(path), orch) == [], f'{b}: co la'


def test_c0_bang_mau_qua_lint():
    import sys
    sys.path.insert(0, HERE)
    from cc2_sheet_lint import lint_param_table
    c0 = _block('helix-cc2-frame')
    sec = c0[c0.index('## Ví dụ ngắn'):c0.index('## Chạy riêng')]
    table = chr(10).join(l for l in sec.splitlines() if l.startswith('|'))
    assert 'Nhãn' in table
    assert lint_param_table(table) == []


def test_c1_vi_du_chua_neu_hai_mien():
    c1 = _block('helix-cc2-chain')
    ex = c1[c1.index('### Ví dụ 2'):c1.index('## Chạy riêng')]
    assert 'chưa nêu' in ex
    doms = {d for d in ['quang', 'âm', 'cơ', 'áp điện', 'điện', 'từ']
            if re.search(r'(?<!\w)' + d + r'(?!\w)', ex)}
    assert len(doms) >= 2, doms
    chains = re.findall(r'^- \*\*[A-Z] —', ex, re.MULTILINE)
    assert len(chains) >= 3
    assert ex.count('Khác chuỗi') >= len(chains)
    ex1 = c1[c1.index('### Ví dụ 1'):c1.index('### Ví dụ 2')]
    assert 'đã nêu: quang→điện' in ex1 and ex1.count('Khác chuỗi') >= 3


# ----------------------------------------------------------------- Task 6: C2 + C3

PARAM_BRIDGE = os.path.join(REF_DIR, 'param-bridge.md')
EMBODIMENT = os.path.join(REF_DIR, 'embodiment-rules.md')


def _table_rows(text):
    """Khoi dong `|` dau tien -> danh sach hang (moi hang la list o), bo dong ---."""
    rows, started = [], False
    for line in text.splitlines():
        if line.lstrip().startswith('|'):
            started = True
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                continue
            rows.append(cells)
        elif started:
            break
    return rows


def _example(text):
    assert '## Ví dụ ngắn' in text, 'thieu muc "## Ví dụ ngắn"'
    tail = text[text.index('## Ví dụ ngắn'):]
    return tail[:tail.index('## Chạy riêng')]


def test_c3_cot_khop_param_bridge():
    ref = _read(PARAM_BRIDGE)
    ref_sec = ref[ref.index('## Khuôn bảng C3'):]
    ref_hdr = _table_rows(ref_sec)[0]
    assert len(ref_hdr) == 8 and ref_hdr[0] == 'Phần tử' and ref_hdr[-1] == 'Nguồn số', ref_hdr
    c3_hdr = _table_rows(_example(_block('helix-cc2-param')))[0]
    assert c3_hdr == ref_hdr, f'C3={c3_hdr} param-bridge={ref_hdr}'
    tpl = _block('helix-cc2-param')
    tpl = tpl[tpl.index('## Khuôn đầu ra'):tpl.index('## Ví dụ ngắn')]
    assert _table_rows(tpl)[0] == ref_hdr, 'bang trong khuon dau ra khong khop param-bridge'


def test_c3_goi_lint():
    c3 = _block('helix-cc2-param')
    assert 'python scripts/cc2_sheet_lint.py' in c3 and 'CC2_C3_Params.md' in c3
    assert re.search(r'cc2_sheet_lint\.py\s+\S*CC2_C3_Params\.md\s+--kind params', c3), 'lenh lint C3 khong day du'
    assert 'báo cáo "đã kiểm" không thay output của lệnh' in c3
    assert re.search(r'Exit ≠ 0[^\n]*không sang C4', c3), 'thieu luat khong sang C4'


def test_c3_bang_mau_qua_lint():
    import sys
    sys.path.insert(0, HERE)
    from cc2_sheet_lint import lint_param_table
    ex = _example(_block('helix-cc2-param'))
    table = chr(10).join(l for l in ex.splitlines() if l.startswith('|'))
    assert len(_table_rows(table)) >= 3, 'bang mau qua it hang'
    assert lint_param_table(table) == []


CRIT_START = 'Tiêu chí NHẠY *(quy ước bộ skill)*:'
CRIT_END = 'lý do «an toàn».'
EXC = 'lý do «an toàn»'


def _crit_paragraph(text):
    assert CRIT_START in text, 'thieu doan tieu chi NHAY'
    i = text.index(CRIT_START)
    j = text.index(CRIT_END, i) + len(CRIT_END)
    para = text[i:j]
    for step in ['(1)', '(2)', '(3)', '(4)']:
        assert step in para, step
    return para


def _nhay_sets(rows):
    """Buoc (1)-(3) tinh tu cot Nhan + hang; ngoai le (4) chi khi co dung cum EXC va Nhan khac tri thuc."""
    rank = {}
    for r in rows:
        m = re.search(r'hạng (\d+)', r[3])
        assert m, f'dong thieu hang: {r[3]}'
        rank[id(r)] = int(m.group(1))
    cands = sorted((rank[id(r)], id(r)) for r in rows if r[6] != 'tri thức')
    top = {k for _, k in cands[:3]}
    exc = {id(r) for r in rows if EXC in r[3] and r[6] != 'tri thức'}
    expected = {rank[k] for k in top | exc}
    actual = {rank[id(r)] for r in rows if r[3].startswith('NHẠY')}
    return actual, expected


def test_nhay_sets_dot_bien():
    hdr = ['p', 'x', 'y']

    def row(chieu, nhan):
        return ['e', 'p', 'f', chieu, '—', 'k', nhan, 'chưa biết']

    base = [row('NHẠY; hạng 2', 'phỏng đoán'), row('hạng 3', 'phỏng đoán')]
    tri = row('hạng 1', 'tri thức')
    # nen: dung theo buoc (1)-(3)
    a, e = _nhay_sets([tri] + [row('NHẠY; hạng 2', 'phỏng đoán'), row('NHẠY; hạng 3', 'phỏng đoán')])
    assert a == e == {2, 3}
    # ca 1: dong tri thuc danh NHAY kem «an toan» phai bi bat
    a, e = _nhay_sets([row('NHẠY; hạng 1; ' + EXC, 'tri thức')] + base)
    assert a != e
    # ca 2: dong co dung cum ngoai le, Nhan phong doan, vuot tran 3 -> hop le
    rows = [row('NHẠY; hạng %d' % k, 'phỏng đoán') for k in (1, 2, 3)] + [row('NHẠY; hạng 4; ' + EXC, 'phỏng đoán')]
    a, e = _nhay_sets(rows)
    assert a == e == {1, 2, 3, 4}
    # ngoai le khong co cum chuan -> bi bat
    rows = [row('NHẠY; hạng %d' % k, 'phỏng đoán') for k in (1, 2, 3)] + [row('NHẠY; hạng 4; an toàn', 'phỏng đoán')]
    a, e = _nhay_sets(rows)
    assert a != e
    # dong NHAY thieu nhung nam trong top 3 -> bi bat
    a, e = _nhay_sets([row('NHẠY; hạng 1', 'phỏng đoán'), row('hạng 2', 'phỏng đoán')])
    assert a != e


def test_c3_nhay_toi_da_3_va_tieu_chi():
    c3 = _block('helix-cc2-param')
    rows = _table_rows(_example(c3))[1:]
    flagged = [r for r in rows if r[3].startswith('NHẠY')]
    assert 1 <= len(flagged) <= 3, len(flagged)
    assert all('NHẠY' not in c for r in rows for i, c in enumerate(r) if i != 3), 'NHAY chi o cot Chieu anh huong'
    for phrase in ['≤3', 'quy ước bộ skill', 'helix-cc2:references:param-bridge']:
        assert phrase in c3, f'C3 thieu cum: {phrase}'
    assert re.search(r'suy ra \(từ', c3)
    assert '`tri thức` không đi với `chưa biết`' in c3
    defn = 'NHẠY = ô "Chiều ảnh hưởng" bắt đầu bằng `NHẠY` (quy ước bộ skill); C4 lấy đúng các dòng này'
    assert defn in c3 and defn in _read(PARAM_BRIDGE), 'dinh nghia NHAY khong dong nhat C3 / param-bridge'
    pb = _read(PARAM_BRIDGE)
    assert _crit_paragraph(c3) == _crit_paragraph(pb), 'doan tieu chi NHAY khong giong nhau'
    actual, expected = _nhay_sets(rows)
    assert any(r[6] == 'tri thức' for r in rows), 'vi du thieu dong tri thuc'
    assert actual == expected, (actual, expected)


def test_c2_tro_embodiment_rules():
    c2 = _block('helix-cc2-form')
    assert 'helix-cc2:references:embodiment-rules' in c2
    assert '| Quy tắc TK | Câu hỏi kiểm | Kết quả | Nhãn |' in c2
    rules = {r[0] for r in _table_rows('| Quy tắc |' + _read(EMBODIMENT).split('| Quy tắc |', 1)[1])[1:]}
    assert len(rules) > 20
    ex = _example(c2)
    used = []
    for l in ex.splitlines():
        if l.startswith('|'):
            first = l.strip().strip('|').split('|')[0].strip()
            if first != 'Quy tắc TK' and not re.fullmatch(r':?-{2,}:?', first):
                used.append(first)
    assert len(used) >= 4, used
    assert used, 'bang vi du C2 trong'
    for u in used:
        assert u in rules, f'quy tac "{u}" khong co trong embodiment-rules'


def test_c2_cau_truc():
    c2 = _block('helix-cc2-form')
    for phrase in ['2–3', 'quy ước bộ skill', 'A-1', 'A-2', 'Mermaid', '## Phép nên làm tiếp', '## Chạy riêng',
                   'Cổng CEO', 'Chuỗi chọn', 'phỏng đoán', 'helix-cc2:references:view-ops', 'CC2_C2_Forms.md',
                   'CC2_C1_Chains.md', '<F-id>/']:
        assert phrase in c2, f'C2 thieu cum: {phrase}'
    ex = _example(c2)
    assert len(re.findall(r'^### Phương án A-\d', ex, re.MULTILINE)) >= 2
    heads = re.findall(r'^### Phương án A-\d', ex, re.MULTILINE)
    sketches = len(re.findall(r'^```(?:mermaid|text)\s*$', ex, re.MULTILINE))
    assert sketches >= len(heads) >= 2, (sketches, heads)
    # moi phuong an co phac rieng: tach theo tieu de
    for part in re.split(r'^### Phương án ', ex, flags=re.MULTILINE)[1:]:
        assert re.search(r'^```(?:mermaid|text)\s*$', part, re.MULTILINE), 'phuong an thieu phac: ' + part[:20]


def test_c2_moi_phuong_an_kiem_it_nhat_2_quy_tac_theo_phan_tu():
    ex = _example(_block('helix-cc2-form'))
    parts = re.split(r'^### Phương án ', ex, flags=re.MULTILINE)[1:]
    assert len(parts) >= 2
    for part in parts:
        rows = []
        for l in part.splitlines():
            if l.startswith('|'):
                cells = [c.strip() for c in l.strip().strip('|').split('|')]
                if cells[0] == 'Quy tắc TK' or re.fullmatch(r':?-{2,}:?', cells[0]):
                    continue
                rows.append(cells)
        assert len(rows) >= 2, part[:20]
        for cells in rows:
            kq = cells[2]
            assert re.search(r'\b(WFP|LSS|Connector|C\d)\b', kq), f'Ket qua khong nho phan tu chuoi: {kq}'
            assert kq.strip().strip('.').lower() not in ('đạt', 'ok'), kq
            assert len(kq.split()) >= 6, f'Ket qua qua ngan, thieu ly do: {kq}'
    c2 = _block('helix-cc2-form')
    assert '≥2 quy tắc' in c2 and 'Cấm ô chỉ' in c2


# ----------------------------------------------------------------- Task 7: C4 + CA

LABELS = ('tri thức', 'phỏng đoán', 'giả định')


def _lint():
    import sys
    sys.path.insert(0, HERE)
    import cc2_sheet_lint
    return cc2_sheet_lint


def _between(text, start, end):
    assert start in text, f'thieu "{start}"'
    tail = text[text.index(start):]
    assert end in tail, f'thieu "{end}" sau "{start}"'
    return tail[:tail.index(end)]


def _sheet_chunks(text):
    """Tach van ban thanh tung khoi phieu: tu dong tieu de PHIEU toi fence/tieu de ke tiep."""
    chunks, cur = [], None
    for line in text.splitlines():
        if re.match(r'^PHIẾU GIẢ THUYẾT\s*[—–-]\s*GT-\d{3}', line.strip()):
            cur = [line]
            chunks.append(cur)
            continue
        if line.strip().startswith('```'):
            cur = None
            continue
        if cur is not None:
            cur.append(line)
    return ['\n'.join(c) for c in chunks]


def _all_tables(text):
    """Moi khoi dong `|` -> list hang (list o), bo dong ---."""
    out, cur = [], None
    for line in text.splitlines():
        if line.lstrip().startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cur is None:
                cur = []
                out.append(cur)
            if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                cur.append(cells)
        else:
            cur = None
    return out


def _route(tin, tam, an_toan=False):
    if an_toan or tam in ('cao', 'trung'):
        return '3'
    return '1–2' if tin == 'cao' else '2'


def _plan_key(mo_cong, duong, tin, tam, gt):
    return (0 if mo_cong else 1, {'3': 0, '2': 1, '1–2': 2}[duong],
            {'cao': 0, 'trung': 1, 'thấp': 2}[tam], {'thấp': 0, 'trung': 1, 'cao': 2}[tin], gt)


def _sheet_meta(chunk):
    gt = re.search(r'GT-\d{3}', chunk).group(0)
    m8 = re.search(r'^\s*8\s+[^:\n]*:\s*(thấp|trung|cao)\s*\([^)]*\)\s*/\s*(thấp|trung|cao)(?!\w)',
                   chunk, re.MULTILINE)
    assert m8, f'{gt}: muc 8 khong doc duoc hai nac'
    m9 = re.search(r'^\s*9\s+(.*)$', chunk, re.MULTILINE)
    assert m9, f'{gt}: thieu muc 9'
    m8line = re.search(r'^\s*8\s+.*$', chunk, re.MULTILINE).group(0)
    return {'gt': gt, 'tin': m8.group(1), 'tam': m8.group(2),
            'mo_cong': 'lặp xuyên cổng' in m9.group(1), 'an_toan': 'an toàn' in m8line}


def test_route_va_thu_tu_dot_bien():
    assert _route('cao', 'thấp') == '1–2' and _route('trung', 'thấp') == '2'
    assert _route('cao', 'trung') == '3' and _route('cao', 'thấp', an_toan=True) == '3'
    a = _plan_key(False, '3', 'trung', 'trung', 'GT-001')
    b = _plan_key(True, '2', 'cao', 'thấp', 'GT-009')
    assert b < a, 'phieu mo lai cong phai len truoc bat ke truc kia'


C4_TPL_H = '## Khuôn đầu ra: `{{prefix}}CC2_C4_Hypotheses.md`'
C4_TPL_P = '## Khuôn đầu ra: `{{prefix}}CC2_C4_Test_Plan.md`'


def test_c4_goi_lint_hypo():
    c4 = _block('helix-cc2-hypo')
    pre = re.search(r'cc2_sheet_lint\.py\s+\S*CC2_C4_Hypotheses\.md\s+--kind hypo --allow-unsigned', c4)
    post = re.search(r'cc2_sheet_lint\.py\s+\S*CC2_C4_Hypotheses\.md\s+--kind hypo[ \t]*$', c4, re.MULTILINE)
    assert pre and post, 'C4 thieu hai luot lint (--allow-unsigned truoc cong, khong co sau ky)'
    gate = c4.find('⛔ **Cổng CEO 3')
    assert gate != -1, 'C4 thieu Cong CEO 3'
    assert pre.start() < gate < post.start(), 'thu tu: lint --allow-unsigned -> Cong CEO 3 -> lint khong co'
    assert 'PRED_UNSIGNED' in c4 and 'AI không điền chữ ký' in c4
    assert re.search(r'Exit ≠ 0[^\n]*không đóng Cổng CEO 3', c4), 'thieu luat exit != 0 khong dong cong 3'
    assert 'báo cáo "đã kiểm" không thay output của lệnh' in c4
    # orchestrator: dong C4 noi dung hai luot
    orch = _orch()
    line = [l for l in orch.splitlines() if l.startswith('- **C4:**')]
    assert line, 'orchestrator thieu dong luat C4'
    i = orch.index(line[0])
    c4rule = orch[i:orch.index('- **C6:**', i)]
    assert '--kind hypo --allow-unsigned' in c4rule and 'PRED_UNSIGNED' in c4rule
    assert re.search(r'--kind hypo`[^\n]*không cờ', c4rule), 'orchestrator chua noi luot lint khong co sau khi ky'
    # khuon: muc 7 de CEO dien
    tpl = _between(c4, C4_TPL_H, C4_TPL_P)
    t7 = re.search(r'^7 .*$', tpl, re.MULTILINE)
    assert t7 and re.search(r'người ký \{\{[^}]*\}\} — ngày \{\{[^}]*\}\}', t7.group(0)), \
        'muc 7 khuon phai de trong cho CEO'
    # ma phieu trong khuon la placeholder -> thay bang ma that de parser nhan phieu
    filled = tpl.replace('GT-{{nnn}}', 'GT-001')
    assert len(_lint().parse_sheets(filled)) == 1
    assert 'PRED_UNSIGNED' in [f.code for f in _lint().lint_sheets(filled)]


def test_c4_phep_thu_bac_bo():
    c4 = _block('helix-cc2-hypo')
    tpl = _between(c4, C4_TPL_H, C4_TPL_P)
    assert re.search(r'^Phép thử nhỏ nhất để bác bỏ: ', tpl, re.MULTILINE)
    ex = _example(c4)
    assert 'minh hoạ đã ký' in ex, 'vi du phai ghi ro la minh hoa da ky'
    chunks = _sheet_chunks(ex)
    assert len(chunks) >= 2
    for ch in chunks:
        m = re.search(r'^Phép thử nhỏ nhất để bác bỏ: (.+)$', ch, re.MULTILINE)
        assert m and len(m.group(1).split()) >= 8, 'phieu thieu dong Phép thử nhỏ nhất để bác bỏ: ' + ch[:30]
    # vi du da ky phai qua lint KHONG co
    assert _lint().lint_sheets(ex) == []


def test_c4_mot_phieu_moi_dong_nhay():
    c4 = _block('helix-cc2-hypo')
    ex = _example(c4)
    inp = _between(ex, '### Đầu vào', '### Phiếu')
    rows = _table_rows(inp)
    pb = _read(PARAM_BRIDGE)
    assert rows[0] == _table_rows(pb[pb.index('## Khuôn bảng C3'):])[0], 'bang dau vao khong theo khuon C3'
    body = rows[1:]
    nhay = {(r[0], r[1]) for r in body if r[3].startswith('NHẠY')}
    assert nhay and len(nhay) < len(body), 'bang dau vao phai co ca dong NHAY va dong khong NHAY'
    chunks = _sheet_chunks(_between(ex, '### Phiếu', '### Kế hoạch thử'))
    refs = []
    for ch in chunks:
        m = re.search(r'^Dòng C3: (.+?) · (.+)$', ch, re.MULTILINE)
        assert m, 'phieu thieu dong "Dòng C3:"'
        refs.append((m.group(1).strip(), m.group(2).strip()))
    assert len(chunks) == len(nhay), (len(chunks), len(nhay))
    assert set(refs) == nhay, (refs, nhay)
    assert 'mỗi dòng `NHẠY` đúng một phiếu' in c4


def test_c4_ke_hoach_thu_theo_dinh_tuyen():
    c4 = _block('helix-cc2-hypo')
    assert 'helix-cc2:references:hypothesis-sheet' in c4 and '§Định tuyến độ tin × tầm ảnh hưởng' in c4
    assert re.search(r'Định tuyến kiểm được \*\(quy ước bộ skill\)\*', c4)
    tplp = _between(c4, C4_TPL_P, '## Ví dụ ngắn')
    ex = _example(c4)
    sheets = _sheet_chunks(_between(ex, '### Phiếu', '### Kế hoạch thử'))
    metas = {m['gt']: m for m in map(_sheet_meta, sheets)}
    plan = _table_rows(ex[ex.index('### Kế hoạch thử'):])
    hdr = plan[0]
    assert _table_rows(tplp)[0] == hdr, 'cot ke hoach vi du khac khuon'
    for col in ['Thứ tự', 'Phiếu', 'Mở lại cổng', 'Đường', 'Độ tin / Tầm ảnh hưởng', 'Loại thử', 'Ngày thử',
                'Người đọc kết quả']:
        assert col in hdr, f'ke hoach thieu cot {col}'
    ix = {c: hdr.index(c) for c in hdr}
    body = plan[1:]
    assert sorted(r[ix['Phiếu']] for r in body) == sorted(metas), 'moi phieu dung mot hang thu'
    keys = []
    for n, r in enumerate(body, 1):
        m = metas[r[ix['Phiếu']]]
        assert r[ix['Thứ tự']] == str(n)
        assert r[ix['Mở lại cổng']].startswith('có') == m['mo_cong'], r
        duong = _route(m['tin'], m['tam'], m['an_toan'])
        assert r[ix['Đường']] == duong, (r, duong)
        assert r[ix['Độ tin / Tầm ảnh hưởng']] == f"{m['tin']} / {m['tam']}", r
        if duong == '3':
            assert r[ix['Loại thử']].startswith('thực nghiệm'), r
        keys.append(_plan_key(m['mo_cong'], duong, m['tin'], m['tam'], m['gt']))
    assert keys == sorted(keys), 'ke hoach khong xep theo dinh tuyen'
    assert [r[ix['Phiếu']] for r in body] != sorted(metas), 'vi du nen co thu tu khac thu tu ma phieu'
    # ngay thu trong ke hoach = ngay thu o muc 5
    for ch in sheets:
        gt = re.search(r'GT-\d{3}', ch).group(0)
        d5 = re.search(r'ngày thử: (\d{4}-\d{2}-\d{2})', ch).group(1)
        row = [r for r in body if r[ix['Phiếu']] == gt][0]
        assert row[ix['Ngày thử']] == d5, (gt, row[ix['Ngày thử']], d5)


def test_c4_analyze_lay_gia_thuyet_ca():
    c4 = _block('helix-cc2-hypo')
    assert 'CC2_C3_Params.md' in c4 and 'CC2_CA_Analysis.md' in c4
    assert re.search(r'`--analyze`[^\n]*## Giả thuyết nháp', c4), 'C4 --analyze chua noi lay muc Giả thuyết nháp cua CA'
    assert re.search(r'`--analyze`[^\n]*`Nguồn CA:`[^\n]*thay cho `Dòng C3:`', c4), \
        'C4 --analyze chua noi dong truy nguoc Nguồn CA:'


def test_c4_cong_3_dung_that():
    c4 = _block('helix-cc2-hypo')
    i = c4.index('⛔ **Cổng CEO 3')
    step = c4[i:c4.index('\n6. ', i)]
    assert 'Dừng. Không chạy bước 6 cho tới khi CEO báo đã ký' in step, 'cong 3 thieu lenh Dung'
    assert re.search(r'PRED_UNSIGNED[^\n]*báo CEO, không sửa mục 7', step)


def test_ca_khong_purpose_gate():
    ca = _block('helix-cc2-analyze')
    hits = [l for l in ca.splitlines() if 'ACCESS LEVEL' in l]
    assert len(hits) == 1, f'ACCESS LEVEL chi duoc o dung mot cau tro RE: {hits}'
    assert '/reverse-engineering' in hits[0] and re.search(r'bên khác|đối thủ', hits[0]), hits[0]
    for l in ca.splitlines():
        if 'Purpose Gate' in l or 'OSINT' in l:
            assert l == hits[0], f'Purpose Gate/OSINT ngoai cau tro RE: {l}'


def test_ca_crosscheck_khong_doc_c1():
    ca = _block('helix-cc2-analyze')
    sec = _section(ca, r'--crosscheck', 2)
    assert sec is not None, 'CA thieu muc ## ... --crosscheck'
    inp = _between(sec, 'Đầu vào được đọc:', '\n\n')
    files = set(re.findall(r'`<thư mục trích>/(CC2_[A-Za-z0-9_]+\.md)`', inp))
    assert files == {'CC2_C0_Frame.md', 'CC2_C2_Forms.md', 'CC2_C3_Params.md'}, files
    # moi dong dau vao la ban trich trong thu muc trich, khong phai tep o <noi ghi>
    bullets = [l for l in inp.splitlines() if l.startswith('- ')]
    assert len(bullets) == 3 and all('`<thư mục trích>/' in b for b in bullets), bullets
    for bad in ('CC2_C1_Chains', 'CC2_C4_Hypotheses', '{{prefix}}'):
        assert bad not in inp, f'{bad} trong dau vao crosscheck'
    for l in sec.splitlines():
        if 'CC2_C1_Chains' in l or 'CC2_C4_Hypotheses' in l:
            assert l.lstrip().startswith('Cấm đọc:'), f'C1/C4 xuat hien ngoai dong cam: {l}'
    cam = [l for l in sec.splitlines() if l.lstrip().startswith('Cấm đọc:')]
    assert cam and 'CC2_C1_Chains' in cam[0] and 'CC2_C4_Hypotheses' in cam[0] and '<nơi ghi>' in cam[0]
    # tham so tuong minh: thu muc trich, X-n, so GT bat dau; C6 cat trich va mo tac tu con moi
    assert '--crosscheck <thư mục trích> <X-n> <n>' in sec
    assert re.search(r'đánh số từ `<n>`', sec) and 'số lớn nhất trong C4' not in sec
    assert re.search(r'C6[^\n]*cắt[^\n]*tác tử con mới', sec), 'chua noi C6 cat ban trich va mo tac tu con moi'
    assert 'không đọc gì ngoài `<thư mục trích>`' in sec
    assert 'người đọc ≠ người lập' in sec
    tables = [t for t in _all_tables(sec) if t and 'Xử lý' in t[0]]
    assert tables, 'crosscheck thieu bang lech co cot Xử lý'
    t = tables[0]
    xi = t[0].index('Xử lý')
    assert len(t) >= 3
    kinds = set()
    for r in t[1:]:
        m = re.match(r'(phiếu nháp GT-\d{3}|dòng sửa C2:)', r[xi])
        assert m, r[xi]
        kinds.add(m.group(1)[:5])
    assert len(kinds) == 2, 'vi du nen co ca phieu nhap va dong sua C2'


def test_ca_dau_ra_va_quy_uoc():
    ca = _block('helix-cc2-analyze')
    for f in ['cad_extract.json', 'helix-cad-ingest', 'CC2_CA_Analysis.md']:
        assert f in ca, f
    assert re.search(r'≤ 2 chức năng con chính[^\n]*≤ 3 tới hạn[^\n]*quy ước bộ skill', ca)
    assert re.search(r'`Vì sao hình học này`[^\n]*quy ước bộ skill', ca)
    ex = _example(ca)
    for h in ['### Mô hình C&C² một trang', '### Vì sao hình học này', '### Rào cản quan sát gặp phải',
              '### Phép nên làm tiếp', '### Giả thuyết nháp']:
        assert h in ex, f'vi du CA thieu {h}'
    model = _between(ex, '### Mô hình C&C² một trang', '### Vì sao hình học này')
    chinh = re.findall(r'^- Chính: ', model, re.MULTILINE)
    toihan = re.findall(r'^- Tới hạn: ', model, re.MULTILINE)
    assert 1 <= len(chinh) <= 2 and len(toihan) <= 3, (chinh, toihan)
    assert re.search(r'^```mermaid\s*$', model, re.MULTILINE)
    vs = _table_rows(_between(ex, '### Vì sao hình học này', '### Rào cản quan sát gặp phải'))
    hdr = vs[0]
    assert 'Nhãn' in hdr and 'Phần tử' in hdr and 'Phép thử nhỏ nhất để bác bỏ' in hdr
    ni, pi = hdr.index('Nhãn'), hdr.index('Phần tử')
    assert len(vs) >= 4
    for r in vs[1:]:
        assert r[ni] in LABELS, r
        assert r[ni] != 'tri thức', 'vi du khong co bang chung -> khong duoc tri thuc'
        assert re.search(r'\b(WFP\d*|LSS\d*|C\d+)\b', r[pi]), r


BARRIER_OPS = {
    'quá nhanh': {'state'}, 'quá chậm': {'state', 'observe'}, 'bị che': {'observe', 'shift'},
    'quá nhỏ / quá lớn': {'zoom-in', 'observe'}, 'sai góc nhìn': {'view'}, 'ngoài biên': {'shift', 'zoom-out'},
}


def test_ca_rao_can_va_phep():
    vo = _read(VIEW_OPS)
    ref_barriers = {r[0] for r in _table_rows(vo[vo.index('## Rào cản quan sát'):])[1:]}
    assert ref_barriers == set(BARRIER_OPS), ref_barriers
    ex = _example(_block('helix-cc2-analyze'))
    rc = _table_rows(_between(ex, '### Rào cản quan sát gặp phải', '### Phép nên làm tiếp'))
    assert rc[0][:3] == ['Rào cản', 'Phần tử', 'Phép phá đề xuất'], rc[0]
    assert len(rc) >= 3
    for r in rc[1:]:
        assert r[0] in BARRIER_OPS, r[0]
        ops = set(re.findall(r'`([a-z-]+)`', r[2]))
        assert ops and ops <= BARRIER_OPS[r[0]], (r[0], ops)
    nxt = _between(ex, '### Phép nên làm tiếp', '### Giả thuyết nháp')
    lines = re.findall(r'^- `?([a-z-]+)`? · ([^·]+) · (.+)$', nxt, re.MULTILINE)
    assert 1 <= len(lines) <= 3
    assert all(op in OPS for op, _, _ in lines)


def test_ca_gia_thuyet_nhap_qua_lint_chua_ky():
    ex = _example(_block('helix-cc2-analyze'))
    draft = ex[ex.index('### Giả thuyết nháp'):]
    L = _lint()
    assert len(L.parse_sheets(draft)) >= 1
    assert L.lint_sheets(draft, allow_unsigned=True) == []
    assert {f.code for f in L.lint_sheets(draft)} == {'PRED_UNSIGNED'}, 'AI khong ky phieu nhap'
    for ch in _sheet_chunks(draft):
        assert re.search(r'^Phép thử nhỏ nhất để bác bỏ: ', ch, re.MULTILINE)


def test_orch_co_crosscheck():
    orch = _orch()
    start = orch.index('Cờ phụ:')
    flags = orch[start:orch.index('```', start)]
    m = re.search(r'^\s*--crosscheck\s+(.+)$', flags, re.MULTILINE)
    assert m and 'C6' in m.group(1) and 'CA' in m.group(1), 'Cờ phụ thieu --crosscheck (chi C6 goi CA)'
