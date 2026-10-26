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
    'helix-cc2-frame', 'helix-cc2-chain', 'helix-cc2-form', 'helix-cc2-param',
    'helix-cc2-hypo', 'helix-cc2-analyze', 'helix-cc2-handoff',
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
