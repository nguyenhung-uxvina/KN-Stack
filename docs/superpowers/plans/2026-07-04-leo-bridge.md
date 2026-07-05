# leo-bridge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** MCP server local (`leo-bridge`) + skill wrapper khép kín vòng prompt → getleo.ai → kết quả → verify → route vào skill nội bộ, với gate MẬT hard-block.

**Architecture:** Python package `mcp/leo-bridge/` gồm gate deterministic (denylist), template parser đọc leo-assist làm source of truth, ledger JSONL, transport layer tách riêng (clipboard bây giờ, API stub), parsers heuristic theo mode, router propose-only. FastMCP expose 6 tools qua stdio.

**Tech Stack:** Python 3.12 · `mcp` SDK 1.27 (FastMCP) · `pyperclip` (PowerShell fallback) · `pyyaml` · pytest.

**Spec:** `docs/superpowers/specs/2026-07-04-leo-bridge-design.md` — đọc trước khi làm.

## Global Constraints

- 100% local — server KHÔNG được thực hiện network call nào (ApiTransport chỉ là stub raise NotImplementedError).
- Gate MẬT: deterministic (regex/denylist), KHÔNG dựa LLM; hard block, KHÔNG có override gửi nguyên bản.
- Propose-only: mọi ghi file đích cần `confirm=true`; số liệu `UNVERIFIED` bị chặn vào `parts_master_csv`.
- Template leo-assist là single source of truth — parse runtime từ `skills/helix/leo-assist/references/leo-mode-templates.md`, KHÔNG copy nội dung template vào server; format đổi → fail loudly.
- Encoding: mọi file đọc/ghi `encoding="utf-8"` (CSV: `utf-8-sig`). Tiếng Việt trong string phải giữ nguyên diacritics.
- Git: branch `feature/helix-leo-bridge` (đã checkout), commit format `[HELIX] …`, footer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. KHÔNG commit `CHANGELOG.md`/`VERSION`/`CLAUDE.md` chung với code — working tree đang có WIP không liên quan của feature khác trong các file này (xem Task 12).
- Chạy test: `python -m pytest mcp/leo-bridge/tests -v` từ repo root `d:\KN-Stack`.
- Windows: đường dẫn trong code dùng `pathlib.Path`, không hardcode `d:\`.

---

### Task 1: Scaffold + Gate MẬT (`gate.py` + `denylist.yaml`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/__init__.py` (rỗng)
- Create: `mcp/leo-bridge/leo_bridge/denylist.yaml`
- Create: `mcp/leo-bridge/leo_bridge/gate.py`
- Create: `mcp/leo-bridge/tests/conftest.py`
- Test: `mcp/leo-bridge/tests/test_gate.py`

**Interfaces:**
- Produces: `gate.classify(text: str, denylist: dict | None = None) -> ClassifyResult` với `ClassifyResult(verdict: str["THUONG"|"MAT"], hits: list[Hit(term, category)], redacted: str | None)`; `gate.load_denylist(path) -> dict`. Task 8 (server) và Task 3 (builder) dùng.

- [ ] **Step 1: Tạo scaffold + conftest**

`mcp/leo-bridge/leo_bridge/__init__.py`: file rỗng.

`mcp/leo-bridge/tests/conftest.py`:
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
```

- [ ] **Step 2: Viết failing test**

`mcp/leo-bridge/tests/test_gate.py`:
```python
from leo_bridge import gate


def test_generic_bearing_is_thuong():
    r = gate.classify("Tìm bạc đạn SKF 6205 chịu tải hướng kính 2 kN, trục Ø25")
    assert r.verdict == "THUONG"
    assert r.hits == []
    assert r.redacted is None


def test_uuv_context_is_mat_with_redaction():
    r = gate.classify("Chọn bạc lót cho GIÁ TRƯỢT UUV, tải 3 kN")
    assert r.verdict == "MAT"
    terms = {h.term.lower() for h in r.hits}
    assert "uuv" in terms
    assert "giá trượt" in terms
    assert "UUV" not in r.redacted
    assert "[REDACTED]" in r.redacted
    assert "3 kN" in r.redacted  # thông số kỹ thuật giữ nguyên


def test_product_code_and_english_terms_hit():
    r = gate.classify("bracket for V-SMASH-127 towed radar target winch")
    assert r.verdict == "MAT"
    cats = {h.category for h in r.hits}
    assert "product_code" in cats


def test_drawing_pattern_hits():
    r = gate.classify("theo bản vẽ TN-03-02-000 revision B")
    assert r.verdict == "MAT"


def test_load_denylist_missing_key_fails():
    import pytest
    with pytest.raises(ValueError):
        gate._validate_denylist({"product_codes": []})
```

> Prereq: `pip show pyyaml` — nếu chưa có, `pip install pyyaml` trước khi chạy test.

- [ ] **Step 3: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_gate.py -v`
Expected: FAIL/ERROR — `ModuleNotFoundError` hoặc `AttributeError` (gate chưa tồn tại).

- [ ] **Step 4: Viết `denylist.yaml`**

`mcp/leo-bridge/leo_bridge/denylist.yaml`:
```yaml
# denylist.yaml — Computational Sensor cho gate MẬT của leo-bridge.
# CEO bổ sung tự do. Quy tắc match:
#   product_codes + defense_terms: KHÔNG phân biệt hoa thường, khớp nguyên từ (word boundary).
#   codenames: PHÂN BIỆT hoa thường (tránh false positive từ generic: "sentinel", "verdict"...).
#   drawing_patterns: regex Python.
# LƯU Ý false-positive đã né: "đạn" đứng riêng KHÔNG có (vì "bạc đạn" = bearing);
#   "Axis"/"Scout"/"Nexus" không đưa vào (từ tiếng Anh quá phổ biến trong cơ khí) —
#   các sản phẩm đó luôn đi kèm mã VN-* nên đã bị chặn qua product_codes.

product_codes:
  - BB-01
  - TARGET-DRONE-001
  - V-SMASH
  - V-ACS
  - V-CAM-HQ
  - VN-TGT
  - VN-12.7MM-SIM
  - VN-AST-MSL
  - VN-CUAV-SIM
  - VN-CUAS
  - VN-RWS127
  - VN-MGM
  - VN-AICC
  - VN-RCE-VSN
  - VN-PONTOON
  - VN-XUONG-UUV
  - VN-FWTP
  - VN-USV-SS
  - VN-SST
  - VN-TLS
  - VN-ALPB
  - VSN-1500
  - VSN-HKN

codenames:
  - THANH TRI
  - Bastion
  - Sentinel
  - Verdict
  - Kairos
  - LOMAH

defense_terms:
  - khí tài
  - giá trượt
  - ngư lôi
  - đạn dược
  - viên đạn
  - bia tập bắn
  - quốc phòng
  - vũ khí
  - hỏa lực
  - phóng lôi
  - BQP
  - torpedo
  - fire control
  - FCS
  - weapon
  - munition
  - warship
  - UUV
  - USV
  - C-UAS
  - counter-uav
  - radar target
  - towed target

drawing_patterns:
  - 'TN-\d{2}-\d{2}-\d{3}'
  - 'WX-[A-Z]{2,4}-\d{3}'
```

- [ ] **Step 5: Viết `gate.py`**

`mcp/leo-bridge/leo_bridge/gate.py`:
```python
"""Computational Sensor — gate MẬT cho leo-bridge. Deterministic, KHÔNG LLM, hard block."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

DENYLIST_PATH = Path(__file__).parent / "denylist.yaml"
REQUIRED_KEYS = ("product_codes", "codenames", "defense_terms", "drawing_patterns")


@dataclass
class Hit:
    term: str
    category: str


@dataclass
class ClassifyResult:
    verdict: str  # "THUONG" | "MAT"
    hits: list = field(default_factory=list)
    redacted: str | None = None


def _validate_denylist(data: dict) -> dict:
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"denylist.yaml thiếu mục {missing}")
    return data


def load_denylist(path=DENYLIST_PATH) -> dict:
    return _validate_denylist(yaml.safe_load(Path(path).read_text(encoding="utf-8")))


def _term_regex(term: str, case_sensitive: bool) -> re.Pattern:
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.compile(rf"(?<!\w){re.escape(term)}(?!\w)", flags)


def classify(text: str, denylist: dict | None = None) -> ClassifyResult:
    dl = denylist or load_denylist()
    spans: list[tuple[int, int]] = []
    hits: dict[str, Hit] = {}

    def scan(terms, category, case_sensitive=False):
        for term in terms or []:
            for m in _term_regex(term, case_sensitive).finditer(text):
                spans.append((m.start(), m.end()))
                hits.setdefault(term, Hit(term, category))

    scan(dl["product_codes"], "product_code")
    scan(dl["codenames"], "codename", case_sensitive=True)
    scan(dl["defense_terms"], "defense_term")
    for pat in dl["drawing_patterns"]:
        for m in re.finditer(pat, text):
            spans.append((m.start(), m.end()))
            hits.setdefault(pat, Hit(pat, "drawing_pattern"))

    if not hits:
        return ClassifyResult("THUONG")
    return ClassifyResult("MAT", list(hits.values()), _redact(text, spans))


def _redact(text: str, spans: list[tuple[int, int]]) -> str:
    merged: list[list[int]] = []
    for s, e in sorted(spans):
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    out, prev = [], 0
    for s, e in merged:
        out.append(text[prev:s])
        out.append("[REDACTED]")
        prev = e
    out.append(text[prev:])
    return "".join(out)
```

- [ ] **Step 6: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_gate.py -v`
Expected: 5 PASS. Nếu `test_uuv_context_is_mat_with_redaction` fail vì "giá trượt" viết hoa "GIÁ TRƯỢT": defense_terms match IGNORECASE nên phải pass — debug regex nếu không.

- [ ] **Step 7: Commit**
```bash
git add mcp/leo-bridge/
git commit -m "[HELIX] leo-bridge: gate MAT deterministic (denylist + redaction)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 2: Template loader (`templates.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/templates.py`
- Test: `mcp/leo-bridge/tests/test_templates.py`

**Interfaces:**
- Consumes: file thật `skills/helix/leo-assist/references/leo-mode-templates.md` (headings `## A.`…`## F.`, `### E1.`–`### E3.`, mỗi section 1 fenced code block).
- Produces: `templates.load_templates(path=TEMPLATES_PATH) -> dict[str, str]` keys `A,B,C,D,E1,E2,E3,F`; `templates.TemplateFormatError`; hằng `templates.TEMPLATES_PATH`.

- [ ] **Step 1: Viết failing test**

`mcp/leo-bridge/tests/test_templates.py`:
```python
import pytest

from leo_bridge import templates


def test_load_real_templates_has_all_modes():
    t = templates.load_templates()
    assert set(t) == {"A", "B", "C", "D", "E1", "E2", "E3", "F"}
    assert "[FUNCTION]" in t["A"]
    assert "[KNOWNS]" in t["C"]
    assert "[GIẢ ĐỊNH]" in t["A"]


def test_missing_mode_fails_loudly(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_text("## A. ONLY\n```\n[MODE] x\n```\n", encoding="utf-8")
    with pytest.raises(templates.TemplateFormatError):
        templates.load_templates(bad)
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_templates.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `templates.py`**

`mcp/leo-bridge/leo_bridge/templates.py`:
```python
"""Parse leo-mode-templates.md (leo-assist = source of truth) → dict mode → template.

KHÔNG copy nội dung template vào đây. Format file đổi → TemplateFormatError (fail loudly).
"""
import re
from pathlib import Path

# .../KN-Stack/mcp/leo-bridge/leo_bridge/templates.py → parents[3] = KN-Stack
TEMPLATES_PATH = (
    Path(__file__).resolve().parents[3]
    / "skills" / "helix" / "leo-assist" / "references" / "leo-mode-templates.md"
)
EXPECTED_MODES = ["A", "B", "C", "D", "E1", "E2", "E3", "F"]
HEADING_RE = re.compile(r"^#{2,3}\s+([A-F]\d?)[.\s]", re.MULTILINE)
BLOCK_RE = re.compile(r"```\n(.*?)```", re.DOTALL)


class TemplateFormatError(Exception):
    pass


def load_templates(path=TEMPLATES_PATH) -> dict:
    p = Path(path)
    if not p.exists():
        raise TemplateFormatError(f"Không thấy template leo-assist tại {p}")
    text = p.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    matches = list(HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = BLOCK_RE.search(text[m.start():end])
        if block:
            out[m.group(1)] = block.group(1).rstrip()
    missing = [x for x in EXPECTED_MODES if x not in out]
    if missing:
        raise TemplateFormatError(
            f"leo-mode-templates.md thiếu template mode {missing} — "
            "format đã đổi, cập nhật leo_bridge/templates.py parser."
        )
    return out
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_templates.py -v`
Expected: 2 PASS.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/templates.py mcp/leo-bridge/tests/test_templates.py
git commit -m "[HELIX] leo-bridge: runtime template parser doc leo-assist (fail loudly)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 3: Prompt builder (`builder.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/builder.py`
- Test: `mcp/leo-bridge/tests/test_builder.py`

**Interfaces:**
- Consumes: `templates.load_templates()` (Task 2).
- Produces: `builder.build_prompt(mode: str, params: dict, classification: str = "THƯỜNG", assumptions: list[str] | None = None, tpl_map: dict | None = None) -> str`; `builder.BuildError`; `builder.REQUIRED_FIELDS: dict[str, list[str]]`.

- [ ] **Step 1: Viết failing test**

`mcp/leo-bridge/tests/test_builder.py`:
```python
import pytest

from leo_bridge import builder


def test_mode_a_fills_fields_and_assumptions():
    p = builder.build_prompt(
        "A",
        {
            "FUNCTION": "đỡ trục quay Ø25, tải hướng kính",
            "ENVELOPE": "OD ≤ 52 mm, rộng ≤ 15 mm, lỗ Ø25 H7",
            "SPEC": "tải 2 kN, 3000 rpm, nhiệt ≤ 80°C",
            "SOURCE": "kho vendor 120M",
        },
        assumptions=["tải tĩnh", "bôi trơn mỡ"],
    )
    assert "[FUNCTION] đỡ trục quay Ø25, tải hướng kính" in p
    assert "[Phân loại: THƯỜNG]" in p
    assert "[GIẢ ĐỊNH] tải tĩnh · bôi trơn mỡ" in p
    # 5 nguyên tắc: search-before-generate giữ nguyên từ template [ASK]
    assert "tái dùng" in p or "thiết kế mới" in p


def test_missing_required_field_raises_with_names():
    with pytest.raises(builder.BuildError) as e:
        builder.build_prompt("C", {"GOAL": "tính FoS"})
    assert "KNOWNS" in str(e.value)
    assert "UNKNOWN" in str(e.value)


def test_invalid_mode_raises():
    with pytest.raises(builder.BuildError):
        builder.build_prompt("Z", {})
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_builder.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `builder.py`**

`mcp/leo-bridge/leo_bridge/builder.py`:
```python
"""Sinh prompt Leo theo mode A–F — ép 5 nguyên tắc leo-assist, từ chối prompt mơ hồ."""
from . import templates as _templates

REQUIRED_FIELDS = {
    "A": ["FUNCTION", "ENVELOPE", "SPEC", "SOURCE"],
    "B": ["QUESTION", "CONTEXT"],
    "C": ["GOAL", "KNOWNS", "UNKNOWN"],
    "D": ["SUBJECT", "PROCESS", "STANDARDS"],
    "E1": ["IDEA", "KNOWNS"],
    "E2": ["DOCTYPE", "SOURCE", "STRUCTURE", "FIELDS"],
    "E3": ["PART"],
    "F": ["PART", "REQUIREMENTS", "PROCESS"],
}


class BuildError(Exception):
    pass


def build_prompt(mode, params, classification="THƯỜNG", assumptions=None, tpl_map=None):
    mode = (mode or "").upper()
    if mode not in REQUIRED_FIELDS:
        raise BuildError(f"Mode không hợp lệ: '{mode}'. Hợp lệ: {sorted(REQUIRED_FIELDS)}")
    missing = [f for f in REQUIRED_FIELDS[mode] if not str(params.get(f, "")).strip()]
    if missing:
        raise BuildError(
            f"Mode {mode} thiếu tham số bắt buộc: {missing}. "
            "KHÔNG sinh prompt mơ hồ — cấp giá trị ĐỊNH LƯỢNG (tải+đơn vị, kích thước interface thật)."
        )
    tpl = (tpl_map or _templates.load_templates())[mode]
    upper_params = {k.upper(): v for k, v in params.items()}
    lines = []
    for line in tpl.splitlines():
        stripped = line.strip()
        if stripped.startswith("[Phân loại"):
            lines.append(f"[Phân loại: {classification}]")
            continue
        if stripped.startswith("[GIẢ ĐỊNH]"):
            items = assumptions or ["(chưa khai báo — CEO bổ sung trước khi gửi)"]
            lines.append("[GIẢ ĐỊNH] " + " · ".join(items))
            continue
        filled = next(
            (f"[{fld}] {val}" for fld, val in upper_params.items()
             if stripped.startswith(f"[{fld}]")),
            None,
        )
        lines.append(filled if filled is not None else line)
    return "\n".join(lines)
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_builder.py -v`
Expected: 3 PASS.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/builder.py mcp/leo-bridge/tests/test_builder.py
git commit -m "[HELIX] leo-bridge: prompt builder ep 5 nguyen tac, tu choi prompt thieu tham so

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 4: Ledger JSONL (`ledger.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/ledger.py`
- Test: `mcp/leo-bridge/tests/test_ledger.py`

**Interfaces:**
- Produces: `class Ledger(dir_path)` với `.new_id() -> str` (`LEO-YYYYMMDD-NNN`), `.append(exchange_id, event, **fields) -> dict`, `.get(exchange_id) -> dict` (merge mọi event, KeyError nếu không có), `.list(status=None) -> list[dict]`. Events chuẩn: `created`(status=SENT) / `ingested`(status=INGESTED) / `verified` / `routed`(status=ROUTED).

- [ ] **Step 1: Viết failing test**

`mcp/leo-bridge/tests/test_ledger.py`:
```python
import pytest

from leo_bridge.ledger import Ledger


def test_new_id_increments_per_day(tmp_path):
    led = Ledger(tmp_path)
    id1 = led.new_id()
    led.append(id1, "created", status="SENT", mode="A")
    id2 = led.new_id()
    assert id1.startswith("LEO-")
    assert id1.endswith("-001")
    assert id2.endswith("-002")


def test_get_merges_events_latest_wins(tmp_path):
    led = Ledger(tmp_path)
    ex = led.new_id()
    led.append(ex, "created", status="SENT", mode="C", prompt="p")
    led.append(ex, "ingested", status="INGESTED", raw="kết quả")
    rec = led.get(ex)
    assert rec["status"] == "INGESTED"
    assert rec["prompt"] == "p"
    assert rec["raw"] == "kết quả"


def test_get_unknown_raises(tmp_path):
    with pytest.raises(KeyError):
        Ledger(tmp_path).get("LEO-19700101-999")


def test_list_filters_status(tmp_path):
    led = Ledger(tmp_path)
    a = led.new_id(); led.append(a, "created", status="SENT", mode="A")
    b = led.new_id(); led.append(b, "created", status="SENT", mode="B")
    led.append(b, "ingested", status="INGESTED")
    assert {r["exchange_id"] for r in led.list("SENT")} == {a}
    assert len(led.list()) == 2
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_ledger.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `ledger.py`**

`mcp/leo-bridge/leo_bridge/ledger.py`:
```python
"""Ledger JSONL append-only — traceability mọi exchange Leo (prompt, classification, verify, route)."""
import json
from datetime import datetime
from pathlib import Path


class Ledger:
    def __init__(self, dir_path):
        self.dir = Path(dir_path)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / "ledger.jsonl"

    def _read_all(self) -> list[dict]:
        if not self.file.exists():
            return []
        return [
            json.loads(line)
            for line in self.file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def new_id(self) -> str:
        prefix = f"LEO-{datetime.now().strftime('%Y%m%d')}-"
        n = sum(
            1 for r in self._read_all()
            if r["exchange_id"].startswith(prefix) and r.get("event") == "created"
        )
        return f"{prefix}{n + 1:03d}"

    def append(self, exchange_id: str, event: str, **fields) -> dict:
        rec = {
            "exchange_id": exchange_id,
            "event": event,
            "ts": datetime.now().isoformat(timespec="seconds"),
            **fields,
        }
        with self.file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return rec

    def get(self, exchange_id: str) -> dict:
        merged: dict = {}
        for r in self._read_all():
            if r["exchange_id"] == exchange_id:
                merged.update(r)
        if not merged:
            raise KeyError(f"Không có exchange {exchange_id} trong ledger")
        return merged

    def list(self, status: str | None = None) -> list[dict]:
        by_id: dict[str, dict] = {}
        for r in self._read_all():
            by_id.setdefault(r["exchange_id"], {}).update(r)
        rows = list(by_id.values())
        return [r for r in rows if status is None or r.get("status") == status]
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_ledger.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/ledger.py mcp/leo-bridge/tests/test_ledger.py
git commit -m "[HELIX] leo-bridge: JSONL ledger append-only cho traceability exchange

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 5: Transports (`transports.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/transports.py`
- Test: `mcp/leo-bridge/tests/test_transports.py`

**Interfaces:**
- Produces: `ClipboardTransport` với `.name = "clipboard"`, `.send(prompt) -> str` (instructions), `.receive() -> str` (raise `TransportError` nếu clipboard rỗng); `ApiTransport` (stub — `__init__` raise `TransportError` nếu thiếu `LEO_API_KEY`, send/receive raise `NotImplementedError`); `get_transport() -> Transport` (API nếu có env key, ngược lại clipboard); `TransportError`.

- [ ] **Step 1: Viết failing test (mock pyperclip — KHÔNG đụng clipboard thật)**

`mcp/leo-bridge/tests/test_transports.py`:
```python
import pytest

from leo_bridge import transports


class FakeClip:
    def __init__(self):
        self.buf = ""

    def copy(self, t):
        self.buf = t

    def paste(self):
        return self.buf


@pytest.fixture
def clip(monkeypatch):
    fake = FakeClip()
    monkeypatch.setattr(transports.ClipboardTransport, "_copy", lambda self, t: fake.copy(t))
    monkeypatch.setattr(transports.ClipboardTransport, "_paste", lambda self: fake.paste())
    return fake


def test_send_copies_and_returns_instructions(clip):
    t = transports.ClipboardTransport()
    ins = t.send("[MODE] PART SEARCH ...")
    assert clip.buf.startswith("[MODE]")
    assert "app.getleo.ai" in ins
    assert "leo_ingest" in ins


def test_receive_empty_clipboard_raises(clip):
    t = transports.ClipboardTransport()
    with pytest.raises(transports.TransportError):
        t.receive()


def test_get_transport_defaults_clipboard(monkeypatch):
    monkeypatch.delenv("LEO_API_KEY", raising=False)
    assert transports.get_transport().name == "clipboard"


def test_api_transport_is_stub(monkeypatch):
    monkeypatch.setenv("LEO_API_KEY", "x")
    t = transports.get_transport()
    assert t.name == "api"
    with pytest.raises(NotImplementedError):
        t.send("p")
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_transports.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `transports.py`**

`mcp/leo-bridge/leo_bridge/transports.py`:
```python
"""Transport layer — hybrid-ready.

ClipboardTransport: bán tự động (CEO dán vào app.getleo.ai). Đường duy nhất hiện nay.
ApiTransport: STUB — implement khi Leo cấp API access (getleo.ai/api, business-only).
KHÔNG bao giờ thêm browser automation (Cloudflare + ToS + khóa account — spec §8).
"""
import os
import subprocess


class TransportError(Exception):
    pass


class ClipboardTransport:
    name = "clipboard"

    def send(self, prompt: str) -> str:
        self._copy(prompt)
        return (
            "Prompt đã nằm trong clipboard. Các bước: "
            "(1) Mở app.getleo.ai, dán (Ctrl+V) và gửi. "
            "(2) Chờ kết quả, bôi đen TOÀN BỘ kết quả, Ctrl+C. "
            "(3) Gọi leo_ingest với exchange_id để parse + verify."
        )

    def receive(self) -> str:
        text = self._paste()
        if not text or not text.strip():
            raise TransportError("Clipboard rỗng — copy TOÀN BỘ kết quả Leo trước khi gọi leo_ingest.")
        return text

    def _copy(self, text: str) -> None:
        try:
            import pyperclip
            pyperclip.copy(text)
        except Exception:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "$input | Set-Clipboard"],
                input=text, text=True, capture_output=True,
            )
            if p.returncode != 0:
                raise TransportError(f"Không copy được vào clipboard: {p.stderr.strip()}")

    def _paste(self) -> str:
        try:
            import pyperclip
            return pyperclip.paste()
        except Exception:
            p = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard -Raw"],
                text=True, capture_output=True,
            )
            if p.returncode != 0:
                raise TransportError(f"Không đọc được clipboard: {p.stderr.strip()}")
            return p.stdout


class ApiTransport:
    name = "api"

    def __init__(self):
        if not os.environ.get("LEO_API_KEY"):
            raise TransportError("LEO_API_KEY chưa có — Leo chưa cấp API access.")

    def send(self, prompt: str) -> str:
        raise NotImplementedError("ApiTransport: implement khi Leo cấp API docs (đã gửi request — xem docs/api-access-request-draft.md).")

    def receive(self) -> str:
        raise NotImplementedError("ApiTransport: implement khi Leo cấp API docs.")


def get_transport():
    if os.environ.get("LEO_API_KEY"):
        return ApiTransport()
    return ClipboardTransport()
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_transports.py -v`
Expected: 4 PASS.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/transports.py mcp/leo-bridge/tests/test_transports.py
git commit -m "[HELIX] leo-bridge: clipboard transport + API stub (hybrid-ready)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 6: Result parsers (`parsers.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/parsers.py`
- Test: `mcp/leo-bridge/tests/test_parsers.py`

**Interfaces:**
- Produces: `parsers.parse_result(mode: str, text: str) -> tuple[dict, list[dict]]` — `(parsed, checklist)`. `parsed` keys: `mode, citations: list[str], has_citations: bool, numbers: list[{value, unit, line}]`; mode A/E3 thêm `parts: list[{raw_cells: list[str]}]`; mode D thêm `flags: list[str]`; mode F thêm `candidates: list[str]`. `checklist` item: `{"item": str, "status": "UNVERIFIED"}`. `parsers.ParseError` khi text quá ngắn (<80 ký tự).

- [ ] **Step 1: Viết failing test**

`mcp/leo-bridge/tests/test_parsers.py`:
```python
import pytest

from leo_bridge import parsers

CALC_RESULT = """Để tính ứng suất uốn cho trục Ø25:
Công thức: sigma = M*c/I (theo Shigley's Mechanical Engineering Design, ch.3 [1])
Với M = 45 Nm, c = 12.5 mm, I = 19175 mm^4
=> sigma = 29.3 MPa. FoS = 250/29.3 = 8.5 (thép C45, Sy = 250 MPa theo datasheet [2])
Nguồn: [1] Shigley 11th ed. [2] https://matweb.com/c45
"""

PART_RESULT = """Tìm thấy 3 ứng viên phù hợp envelope Ø25 H7:
| Part | Vendor | PN | Khớp |
|---|---|---|---|
| Bạc đạn 6205-2RS | SKF | 6205-2RS1 | 95% |
| Bạc đạn 6205 ZZ | NSK | 6205ZZCM | 93% |
Kết luận: tái dùng 6205-2RS1, không cần thiết kế mới.
Nguồn: ISO 15242, catalog SKF https://skf.com/6205
"""

NO_CITE_RESULT = """Ứng suất khoảng 30 MPa, FoS tầm 8, dùng thép C45 là được.
Không cần kiểm tra thêm gì cả, thiết kế này ổn với tải đã cho nhé anh.
"""


def test_calc_result_extracts_numbers_and_citations():
    parsed, checklist = parsers.parse_result("C", CALC_RESULT)
    assert parsed["has_citations"] is True
    units = {n["unit"] for n in parsed["numbers"]}
    assert "MPa" in units and "Nm" in units
    # mỗi số 1 mục checklist, mặc định UNVERIFIED
    assert all(c["status"] == "UNVERIFIED" for c in checklist)
    assert len(checklist) >= len(parsed["numbers"])


def test_part_result_parses_table_rows():
    parsed, checklist = parsers.parse_result("A", PART_RESULT)
    assert len(parsed["parts"]) == 2
    assert "SKF" in parsed["parts"][0]["raw_cells"]


def test_no_citation_flagged_red():
    parsed, checklist = parsers.parse_result("C", NO_CITE_RESULT)
    assert parsed["has_citations"] is False
    assert any("KHÔNG cite" in c["item"] for c in checklist)


def test_too_short_raises():
    with pytest.raises(parsers.ParseError):
        parsers.parse_result("A", "ok")
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_parsers.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `parsers.py`**

`mcp/leo-bridge/leo_bridge/parsers.py`:
```python
"""Parse kết quả Leo (free text từ clipboard) → structured + verify checklist.

Heuristic có chủ đích — KHÔNG đoán mò: text quá ngắn/không hợp lệ → ParseError.
Mọi số liệu mặc định UNVERIFIED (doctrine: số Leo là điểm khởi đầu, CEO verify).
"""
import re

MIN_RESULT_LEN = 80

CITATION_RE = re.compile(
    r"(https?://\S+|\[\d+\]|ISO\s?\d{3,5}|ASME\s?[A-Z0-9.]+|MIL-[A-Z]+-\d+|TCVN\s?\d+|DIN\s?\d+|AWS\s?[A-Z0-9.]+)"
)
NUMBER_UNIT_RE = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(kN|N[m·]?m?|MPa|GPa|mm|cm|kg|°C|rpm|Hz|µm|%)(?![\w/])"
)
ITEM_RE = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s+(\S.*)$")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|\s*$", re.MULTILINE)


class ParseError(Exception):
    pass


def parse_result(mode: str, text: str) -> tuple[dict, list[dict]]:
    mode = (mode or "").upper()
    if not text or len(text.strip()) < MIN_RESULT_LEN:
        raise ParseError(
            f"Nội dung quá ngắn (<{MIN_RESULT_LEN} ký tự) — không giống kết quả Leo. "
            "Copy TOÀN BỘ kết quả rồi gọi lại leo_ingest."
        )
    citations = sorted(set(CITATION_RE.findall(text)))
    numbers = [
        {"value": m.group(1), "unit": m.group(2), "line": text[: m.start()].count("\n") + 1}
        for m in NUMBER_UNIT_RE.finditer(text)
    ]
    parsed: dict = {
        "mode": mode,
        "citations": citations,
        "has_citations": bool(citations),
        "numbers": numbers,
    }
    if mode in ("A", "E3"):
        parsed["parts"] = _parse_parts(text)
    elif mode == "D":
        parsed["flags"] = _parse_items(text)
    elif mode == "F":
        parsed["candidates"] = _parse_items(text)
    return parsed, _build_checklist(parsed)


def _parse_items(text: str) -> list[str]:
    return [m.group(1).strip() for line in text.splitlines() if (m := ITEM_RE.match(line))]


def _parse_parts(text: str) -> list[dict]:
    parts = []
    for row in TABLE_ROW_RE.findall(text):
        cells = [c.strip() for c in row.split("|")]
        joined = "".join(cells)
        if not joined or set(joined) <= set("-: "):
            continue  # dòng kẻ bảng
        if cells[0].lower() in ("part", "tên", "#", "stt"):
            continue  # header
        parts.append({"raw_cells": cells})
    if not parts:
        parts = [{"raw_cells": [item]} for item in _parse_items(text)]
    return parts


def _build_checklist(parsed: dict) -> list[dict]:
    items = []
    if not parsed["has_citations"]:
        items.append({
            "item": "⚠️ Leo KHÔNG cite nguồn nào — không dùng cho quyết định chịu lực/an toàn",
            "status": "UNVERIFIED",
        })
    for n in parsed["numbers"]:
        items.append({
            "item": f"Số liệu {n['value']} {n['unit']} (dòng {n['line']}) — đã mở nguồn xác minh?",
            "status": "UNVERIFIED",
        })
    for p in parsed.get("parts", []):
        items.append({
            "item": f"Part: {' | '.join(p['raw_cells'])[:80]} — PN/vendor đã đối chiếu datasheet?",
            "status": "UNVERIFIED",
        })
    return items
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_parsers.py -v`
Expected: 4 PASS. Nếu `test_part_result_parses_table_rows` đếm 3 thay vì 2: kiểm tra header/dòng kẻ đã bị lọc.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/parsers.py mcp/leo-bridge/tests/test_parsers.py
git commit -m "[HELIX] leo-bridge: parsers theo mode + verify checklist (UNVERIFIED mac dinh)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 7: Router propose-only (`router.py`)

**Files:**
- Create: `mcp/leo-bridge/leo_bridge/router.py`
- Test: `mcp/leo-bridge/tests/test_router.py`

**Interfaces:**
- Consumes: exchange dict từ `Ledger.get()` (keys: `exchange_id, mode, raw, parsed, checklist`).
- Produces: `router.propose_routes(mode, parsed) -> list[{target_type, description}]`; `router.write_route(exchange: dict, target_type: str, target_path: str, confirm: bool = False) -> str` (đường dẫn đã ghi); `router.RouteBlockedError`. `target_type` hợp lệ: `parts_master_csv` (staging CSV — CEO merge tay vào parts_master thật), `journal_md`, `calc_md`.

- [ ] **Step 1: Viết failing test**

`mcp/leo-bridge/tests/test_router.py`:
```python
import pytest

from leo_bridge import router


def _exchange(unverified=True):
    return {
        "exchange_id": "LEO-20260704-001",
        "mode": "A",
        "raw": "kết quả Leo dài...",
        "parsed": {"parts": [{"raw_cells": ["6205-2RS", "SKF", "6205-2RS1"]}]},
        "checklist": [{"item": "PN đã đối chiếu?", "status": "UNVERIFIED" if unverified else "VERIFIED"}],
    }


def test_no_confirm_blocked(tmp_path):
    with pytest.raises(router.RouteBlockedError):
        router.write_route(_exchange(), "journal_md", str(tmp_path / "j.md"))


def test_unverified_blocked_from_parts_master(tmp_path):
    with pytest.raises(router.RouteBlockedError) as e:
        router.write_route(_exchange(unverified=True), "parts_master_csv",
                           str(tmp_path / "staging.csv"), confirm=True)
    assert "UNVERIFIED" in str(e.value)


def test_verified_writes_parts_csv(tmp_path):
    p = tmp_path / "staging.csv"
    out = router.write_route(_exchange(unverified=False), "parts_master_csv", str(p), confirm=True)
    content = p.read_text(encoding="utf-8-sig")
    assert "6205-2RS1" in content
    assert "LEO-20260704-001" in content
    assert out == str(p)


def test_journal_allows_unverified_with_label(tmp_path):
    p = tmp_path / "journal.md"
    router.write_route(_exchange(unverified=True), "journal_md", str(p), confirm=True)
    content = p.read_text(encoding="utf-8")
    assert "UNVERIFIED" in content
    assert "LEO-20260704-001" in content


def test_propose_routes_for_parts():
    routes = router.propose_routes("A", {"parts": [{"raw_cells": ["x"]}]})
    types = {r["target_type"] for r in routes}
    assert "parts_master_csv" in types and "journal_md" in types
```

- [ ] **Step 2: Chạy test xác nhận FAIL**

Run: `python -m pytest mcp/leo-bridge/tests/test_router.py -v`
Expected: FAIL — module không tồn tại.

- [ ] **Step 3: Viết `router.py`**

`mcp/leo-bridge/leo_bridge/router.py`:
```python
"""Propose-only routing — chỉ ghi khi CEO confirm; chặn UNVERIFIED vào BOM/parts_master.

parts_master_csv = file STAGING do CEO cấp đường dẫn — CEO merge tay vào parts_master
thật (không blind-append vào BOM production).
"""
import csv
from datetime import datetime
from pathlib import Path

BOM_TARGETS = {"parts_master_csv"}
NOTE_TARGETS = {"journal_md", "calc_md"}


class RouteBlockedError(Exception):
    pass


def propose_routes(mode: str, parsed: dict) -> list[dict]:
    routes = []
    if parsed.get("parts"):
        routes.append({
            "target_type": "parts_master_csv",
            "description": "Append part rows vào STAGING CSV (BOM mua ngoài — mọi mục phải VERIFIED trước)",
        })
    if mode in ("B", "C"):
        routes.append({
            "target_type": "calc_md",
            "description": "Lưu calc sheet markdown (mục UNVERIFIED được gắn nhãn rõ)",
        })
    routes.append({
        "target_type": "journal_md",
        "description": "Ghi design journal (luôn được phép, gắn nhãn UNVERIFIED nếu có)",
    })
    return routes


def write_route(exchange: dict, target_type: str, target_path: str, confirm: bool = False) -> str:
    if not confirm:
        raise RouteBlockedError("Propose-only: cần CEO ra lệnh rõ (confirm=true) mới ghi.")
    unverified = [c for c in exchange.get("checklist", []) if c.get("status") == "UNVERIFIED"]
    if target_type in BOM_TARGETS and unverified:
        raise RouteBlockedError(
            f"{len(unverified)} mục UNVERIFIED — CẤM ghi vào parts_master/BOM. "
            "Verify từng mục (leo_route verified_items=[...]) rồi gọi lại."
        )
    path = Path(target_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if target_type == "parts_master_csv":
        _append_parts_csv(path, exchange)
    elif target_type in NOTE_TARGETS:
        _append_note_md(path, exchange, unverified)
    else:
        raise RouteBlockedError(
            f"target_type '{target_type}' không hỗ trợ. Hợp lệ: {sorted(BOM_TARGETS | NOTE_TARGETS)}"
        )
    return str(path)


def _append_parts_csv(path: Path, exchange: dict) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "exchange_id", "source", "part_raw"])
        for p in exchange.get("parsed", {}).get("parts", []):
            w.writerow([
                datetime.now().strftime("%Y-%m-%d"),
                exchange["exchange_id"],
                "leo",
                " | ".join(p["raw_cells"]),
            ])


def _append_note_md(path: Path, exchange: dict, unverified: list) -> None:
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    label = f" — ⚠️ {len(unverified)} mục UNVERIFIED (không dùng cho BOM/bản vẽ)" if unverified else ""
    entry = (
        f"\n## Leo {exchange['exchange_id']} ({stamp}){label}\n"
        f"Mode: {exchange.get('mode')}\n\n{exchange.get('raw', '').strip()}\n"
    )
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
```

- [ ] **Step 4: Chạy test xác nhận PASS**

Run: `python -m pytest mcp/leo-bridge/tests/test_router.py -v`
Expected: 5 PASS.

- [ ] **Step 5: Commit**
```bash
git add mcp/leo-bridge/leo_bridge/router.py mcp/leo-bridge/tests/test_router.py
git commit -m "[HELIX] leo-bridge: propose-only router, chan UNVERIFIED vao parts_master

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 8: MCP server (`server.py`) + `.mcp.json` + `.gitignore`

**Files:**
- Create: `mcp/leo-bridge/server.py`
- Create: `.mcp.json` (repo root — chưa tồn tại)
- Modify: `.gitignore` (thêm ledger runtime)
- Test: smoke test `python mcp/leo-bridge/server.py --selftest` (không cần pytest — server là wiring mỏng, logic đã test ở Task 1–7)

**Interfaces:**
- Consumes: toàn bộ Task 1–7 (`gate.classify`, `builder.build_prompt`, `templates.load_templates`, `Ledger`, `get_transport`, `parsers.parse_result`, `router.propose_routes/write_route`).
- Produces: 6 MCP tools `leo_classify, leo_prompt_build, leo_send, leo_ingest, leo_route, leo_ledger` qua stdio, server name `leo-bridge`.

- [ ] **Step 1: Viết `server.py`**

`mcp/leo-bridge/server.py`:
```python
"""leo-bridge MCP server — cầu nối bán tự động Workshop X ↔ getleo.ai.

100% local: không network call. Transport = clipboard (API stub chờ Leo cấp access).
Doctrine: gate MẬT hard-block (2 lần) · propose-only · mọi số Leo = UNVERIFIED tới khi CEO verify.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from mcp.server.fastmcp import FastMCP

from leo_bridge import builder, gate, parsers, router, templates
from leo_bridge.ledger import Ledger
from leo_bridge.transports import get_transport

LEDGER_DIR = Path(__file__).parent / "ledger"

mcp = FastMCP("leo-bridge")
_ledger = Ledger(LEDGER_DIR)


@mcp.tool()
def leo_classify(task_text: str) -> dict:
    """Gate MẬT (bước 1, bắt buộc): phân loại THUONG/MAT bằng denylist deterministic.
    MAT → trả bản redacted để CEO viết lại prompt trừu tượng hóa (chức năng + thông số generic,
    KHÔNG tên khí tài). Hard block — không có override gửi nguyên bản."""
    r = gate.classify(task_text)
    return {
        "verdict": r.verdict,
        "hits": [{"term": h.term, "category": h.category} for h in r.hits],
        "redacted": r.redacted,
        "next": "THUONG → leo_prompt_build. MAT → trừu tượng hóa rồi classify lại.",
    }


@mcp.tool()
def leo_prompt_build(mode: str, params: dict, assumptions: list[str] | None = None) -> dict:
    """Sinh prompt Leo theo mode A/B/C/D/E1/E2/E3/F từ template leo-assist (source of truth).
    Ép 5 nguyên tắc: load case định lượng, interface thật, process, cite bắt buộc,
    search-before-generate. Thiếu tham số bắt buộc → lỗi liệt kê rõ."""
    c = gate.classify(" ".join(str(v) for v in params.values()))
    classification = "THƯỜNG" if c.verdict == "THUONG" else "MẬT→generic/COTS only"
    prompt = builder.build_prompt(mode, params, classification, assumptions)
    return {
        "prompt": prompt,
        "gate_verdict": c.verdict,
        "gate_hits": [h.term for h in c.hits],
        "warning": None if c.verdict == "THUONG" else
            "Params chứa context MẬT — leo_send SẼ CHẶN. Trừu tượng hóa trước.",
    }


@mcp.tool()
def leo_send(prompt: str, mode: str, note: str = "") -> dict:
    """Gate lần 2 (defense-in-depth, hard block) → copy prompt vào clipboard →
    tạo exchange_id + ghi ledger. CEO dán vào app.getleo.ai."""
    r = gate.classify(prompt)
    if r.verdict == "MAT":
        return {
            "status": "BLOCKED",
            "reason": "Prompt chứa context MẬT — TUYỆT ĐỐI không gửi lên Leo cloud (spec §2, doctrine leo-assist).",
            "hits": [h.term for h in r.hits],
            "redacted_suggestion": r.redacted,
            "action": "Thay tên khí tài/mã dự án bằng chức năng + thông số generic rồi leo_send lại.",
        }
    ex_id = _ledger.new_id()
    transport = get_transport()
    instructions = transport.send(prompt)
    _ledger.append(ex_id, "created", status="SENT", mode=mode.upper(), note=note,
                   transport=transport.name, classification="THUONG", prompt=prompt)
    return {"status": "SENT", "exchange_id": ex_id, "instructions": instructions}


@mcp.tool()
def leo_ingest(exchange_id: str) -> dict:
    """Đọc kết quả Leo từ clipboard → parse theo mode → verify checklist
    (mọi số/part = UNVERIFIED) → đề xuất đích. PROPOSE-ONLY: không ghi gì."""
    ex = _ledger.get(exchange_id)
    raw = get_transport().receive()
    parsed, checklist = parsers.parse_result(ex["mode"], raw)
    routes = router.propose_routes(ex["mode"], parsed)
    _ledger.append(exchange_id, "ingested", status="INGESTED",
                   raw=raw, parsed=parsed, checklist=checklist)
    return {
        "exchange_id": exchange_id,
        "parsed": parsed,
        "verify_checklist": checklist,
        "proposed_routes": routes,
        "note": "Propose-only. CEO mở nguồn verify từng mục → leo_route(verified_items=[...], confirm=true).",
    }


@mcp.tool()
def leo_route(exchange_id: str, target_type: str, target_path: str,
              confirm: bool = False, verified_items: list[int] | None = None) -> dict:
    """Ghi kết quả đã duyệt vào đích (parts_master_csv STAGING / journal_md / calc_md).
    confirm=true = CEO đã ra lệnh rõ. verified_items = index checklist CEO ĐÃ mở nguồn xác minh.
    Mục UNVERIFIED bị CHẶN vào parts_master_csv."""
    ex = _ledger.get(exchange_id)
    checklist = ex.get("checklist", [])
    if verified_items:
        for i in verified_items:
            if 0 <= i < len(checklist):
                checklist[i]["status"] = "VERIFIED"
        _ledger.append(exchange_id, "verified", checklist=checklist)
        ex["checklist"] = checklist
    written = router.write_route(ex, target_type, target_path, confirm=confirm)
    _ledger.append(exchange_id, "routed", status="ROUTED",
                   target_type=target_type, target_path=written)
    return {"status": "ROUTED", "written": written}


@mcp.tool()
def leo_ledger(action: str = "list", exchange_id: str = "", status: str = "") -> dict:
    """Traceability. action=list (lọc status tùy chọn) | show (cần exchange_id) | pending
    (SENT chưa ingest + INGESTED chưa route)."""
    if action == "show":
        return _ledger.get(exchange_id)
    if action == "pending":
        return {"rows": _ledger.list("SENT") + _ledger.list("INGESTED")}
    rows = _ledger.list(status or None)
    return {"rows": [
        {k: r.get(k) for k in ("exchange_id", "status", "mode", "ts", "note")} for r in rows
    ]}


def _selftest() -> None:
    t = templates.load_templates()
    assert set(t) == {"A", "B", "C", "D", "E1", "E2", "E3", "F"}, f"templates: {sorted(t)}"
    assert gate.classify("bạc đạn SKF 6205 chịu 2 kN").verdict == "THUONG"
    assert gate.classify("bạc lót cho UUV").verdict == "MAT"
    p = builder.build_prompt("B", {"QUESTION": "dung sai H7/g6 cho trục Ø25?",
                                   "CONTEXT": "thép C45, lắp trượt"})
    assert "[QUESTION] dung sai H7/g6" in p
    print("selftest OK — 8 templates, gate + builder hoạt động. Tools: leo_classify, "
          "leo_prompt_build, leo_send, leo_ingest, leo_route, leo_ledger")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        mcp.run()
```

- [ ] **Step 2: Chạy smoke test**

Run: `python mcp/leo-bridge/server.py --selftest`
Expected: in ra `selftest OK — 8 templates, gate + builder hoạt động. Tools: ...`, exit 0.

- [ ] **Step 3: Tạo `.mcp.json` + cập nhật `.gitignore`**

`.mcp.json` (repo root, file mới):
```json
{
  "mcpServers": {
    "leo-bridge": {
      "command": "python",
      "args": ["mcp/leo-bridge/server.py"]
    }
  }
}
```

`.gitignore` — thêm vào cuối file:
```
# leo-bridge runtime ledger (traceability data, không phải source)
mcp/leo-bridge/ledger/
```

- [ ] **Step 4: Commit**
```bash
git add mcp/leo-bridge/server.py .mcp.json .gitignore
git commit -m "[HELIX] leo-bridge: FastMCP server 6 tools + dang ky .mcp.json

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 9: Skill wrapper `leo-bridge` + cập nhật `leo-assist`

**Files:**
- Create: `skills/helix/leo-bridge/SKILL.md`
- Modify: `skills/helix/leo-assist/SKILL.md` (chèn section trước `## Vòng kết hợp (Leo ⨉ bộ skill nội bộ)`)

**Interfaces:**
- Consumes: 6 MCP tools từ Task 8 (tên chính xác: `leo_classify, leo_prompt_build, leo_send, leo_ingest, leo_route, leo_ledger`).
- Produces: skill `/leo-bridge` cho AI routing; junction làm skill có hiệu lực ngay (không cần deploy thêm).

- [ ] **Step 1: Viết `skills/helix/leo-bridge/SKILL.md`**

```markdown
---
name: leo-bridge
description: "Vòng khép kín bán tự động Workshop X ↔ getleo.ai qua MCP server local (mcp/leo-bridge). 6 tools: leo_classify (gate MẬT hard-block + redaction) → leo_prompt_build (template leo-assist mode A–F, ép 5 nguyên tắc) → leo_send (gate lần 2 + clipboard + ledger) → CEO dán vào app.getleo.ai → leo_ingest (parse + verify checklist UNVERIFIED) → leo_route (propose-only, chặn UNVERIFIED vào parts_master) + leo_ledger (traceability). Transport hybrid-ready: clipboard bây giờ, API stub chờ getleo.ai cấp access. Triggers on: 'leo bridge', 'gửi leo', 'hỏi leo', 'kết nối leo', 'leo mcp', 'ask leo', 'send to leo', 'leo exchange', 'leo ledger', 'ingest leo', 'kết quả leo', 'đem kết quả leo về'."
---

# leo-bridge — Vòng khép kín Leo AI (MCP)

> **Role:** Orchestrate 6 MCP tools của server `leo-bridge` thành vòng khép kín. Doctrine + template = [[leo-assist]] (source of truth); skill này là CÁCH THI HÀNH programmatic.
> **Prereq:** MCP server `leo-bridge` trong `.mcp.json`. Kiểm tra: tool `leo_ledger` gọi được.

## Vòng chuẩn (mọi tác vụ Leo)

```
1. leo_classify(task)        → MAT? → CEO trừu tượng hóa (dùng redacted làm gợi ý) → classify lại
2. leo_prompt_build(mode, params, assumptions)   ← mode theo bảng Phase×Mode của leo-assist
3. leo_send(prompt, mode)    → exchange_id; prompt đã trong clipboard
4. [CEO] dán vào app.getleo.ai → copy TOÀN BỘ kết quả
5. leo_ingest(exchange_id)   → parsed + verify_checklist (mọi số = UNVERIFIED) + proposed_routes
6. [CEO] mở nguồn cite, xác minh từng mục checklist
7. leo_route(exchange_id, target_type, target_path, confirm=true, verified_items=[...])
```

## Chọn mode + tham số
- Mode A–F + phase: theo [[leo-assist]] (bảng Phase×Mode). Tham số bắt buộc từng mode: tool tự báo nếu thiếu — cấp giá trị ĐỊNH LƯỢNG (tải + đơn vị, kích thước interface thật).
- Sinh hình học concept (mesh) → [[leo-prompt]], KHÔNG qua bridge (Leo không sinh CAD production).

## Targets của leo_route
| target_type | Đích | Ràng buộc |
|---|---|---|
| `parts_master_csv` | STAGING CSV (CEO merge tay vào parts_master thật) | CHẶN nếu còn mục UNVERIFIED |
| `calc_md` | Calc sheet markdown | UNVERIFIED được, gắn nhãn |
| `journal_md` | Design journal | UNVERIFIED được, gắn nhãn |

Skill tiêu thụ tiếp: part rows → [[forge-fabrication]] (BOM mua ngoài) · calc → [[helix-p3-dfx]] verify · spec text → [[helix-p1-requirements]].

## Gotchas
- **Gate chạy 2 lần** (classify + send) — prompt viết tay không qua build vẫn bị chặn nếu MẬT. Không có override.
- **BLOCKED ≠ lỗi:** dùng `redacted_suggestion` làm khung, thay [REDACTED] bằng mô tả chức năng generic.
- **Clipboard rỗng / kết quả <80 ký tự** → ingest từ chối; copy lại toàn bộ kết quả Leo.
- **Ledger** = `mcp/leo-bridge/ledger/ledger.jsonl` (gitignored). `leo_ledger("pending")` xem exchange dở dang.

## COD
- Vòng tools (build/send/ingest/route): Offload (O)
- **Trừu tượng hóa prompt MẬT: Core (C)** — CEO quyết định ngữ nghĩa
- **Verify cite từng mục checklist: Core (C)** — số Leo là điểm khởi đầu, người chốt
- **confirm=true cho leo_route: Core (C)** — propose-only doctrine
```

- [ ] **Step 2: Cập nhật `leo-assist` SKILL.md**

Edit `skills/helix/leo-assist/SKILL.md` — old_string:
```
## Vòng kết hợp (Leo ⨉ bộ skill nội bộ)
```
new_string:
```
## Programmatic path — [[leo-bridge]] (MCP)
Vòng thủ công ở trên nay có bản khép kín qua MCP server local `mcp/leo-bridge` (6 tools: classify → prompt_build → send → ingest → route → ledger; gate MẬT hard-block 2 lần; propose-only). Dùng [[leo-bridge]] khi muốn ledger + verify checklist + route tự động; leo-assist vẫn là source of truth cho template + doctrine.

## Vòng kết hợp (Leo ⨉ bộ skill nội bộ)
```

- [ ] **Step 3: Kiểm tra frontmatter + junction**

Run: `bash setup.sh --verify`
Expected: junctions resolve OK (skill mới nằm trong `skills/helix/` được junction domain cover — nếu setup.sh báo thiếu junction cho skill mới, chạy `bash setup.sh --install` theo hướng dẫn script).

- [ ] **Step 4: Commit**
```bash
git add skills/helix/leo-bridge/ skills/helix/leo-assist/SKILL.md
git commit -m "[HELIX] Add leo-bridge skill wrapper + leo-assist programmatic path

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 10: Draft email xin API access

**Files:**
- Create: `mcp/leo-bridge/docs/api-access-request-draft.md`

**Interfaces:** standalone deliverable — CEO review rồi tự gửi từ vnsimtech@gmail.com.

- [ ] **Step 1: Viết draft**

`mcp/leo-bridge/docs/api-access-request-draft.md`:
```markdown
# Draft — Leo AI API access request

> CEO review rồi tự gửi. Kênh: form tại https://www.getleo.ai/api hoặc email hello@getleo.ai.
> Nguyên tắc: KHÔNG nhắc defense/khí tài/BQP. Định vị: công ty kỹ thuật cơ khí VN.

**To:** hello@getleo.ai
**Subject:** API access request — engineering workflow integration (Workshop X, Vietnam)

Hi Leo AI team,

We are Workshop X, a mechanical engineering and prototyping company based in
Vietnam (26 engineers and technicians across mechanical, electronics, and
embedded software teams). Several of our engineers already use Leo through
the web app, primarily for standard-part search, citation-backed engineering
calculations, and standards Q&A.

We are building an internal engineering-assistant workflow (prompt
orchestration, BOM building, and design-documentation tooling) and would like
to integrate Leo programmatically instead of copy-pasting between tools. Our
main use cases for the API:

1. Part search & reuse — querying your 120M+ vendor-part index from our
   internal BOM tooling.
2. Citation-backed calculations and standards Q&A — routing engineers'
   sizing questions to Leo and capturing the cited sources for our design
   records.
3. Documentation drafts — datasheet/spec text generation feeding our
   internal review pipeline.

Could you share:
- What capabilities the API currently exposes (part search, calculations, Q&A)?
- Authentication model and rate limits;
- Pricing for a team of 5–10 engineer seats;
- API documentation or a sandbox we could evaluate.

Happy to jump on a call for a demo of our intended integration.

Best regards,
[CEO name]
Workshop X — Vietnam
vnsimtech@gmail.com
```

- [ ] **Step 2: Commit**
```bash
git add mcp/leo-bridge/docs/
git commit -m "[HELIX] leo-bridge: draft email xin Leo API access (khong nhac defense)

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 11: Eval spec `evals/leo-bridge.json`

**Files:**
- Create: `evals/leo-bridge.json`

**Interfaces:** theo format static-mode hiện có (xem `evals/helix-cad-validate.json`).

- [ ] **Step 1: Viết eval spec**

`evals/leo-bridge.json`:
```json
{
  "skill": "leo-bridge",
  "mode": "static",
  "description": "Audit leo-bridge SKILL.md + mcp/leo-bridge server cho harness contract: gate MAT deterministic hard-block, propose-only, template source-of-truth, transport hybrid, traceability.",
  "checks": [
    {
      "id": "frontmatter-valid",
      "desc": "Frontmatter name == directory, description co 'Triggers on:' VI + EN.",
      "assert": "name: leo-bridge present; description includes 'Triggers on:' with Vietnamese and English trigger phrases."
    },
    {
      "id": "gate-deterministic-hard-block",
      "desc": "Gate MAT la denylist regex, khong LLM, khong override; chay 2 lan (classify + send).",
      "assert": "gate.py uses re + yaml only (no LLM/network import); leo_send re-runs gate.classify and returns BLOCKED for MAT with no bypass parameter; SKILL states gate chay 2 lan, khong co override."
    },
    {
      "id": "no-network",
      "desc": "Server 100% local; ApiTransport chi la stub.",
      "assert": "no requests/httpx/urllib network call in leo_bridge/ or server.py; ApiTransport.send/receive raise NotImplementedError; no browser automation (playwright/selenium) anywhere."
    },
    {
      "id": "propose-only",
      "desc": "Khong ghi dich khi thieu confirm; UNVERIFIED bi chan vao parts_master.",
      "assert": "router.write_route raises RouteBlockedError when confirm falsy; BOM_TARGETS blocked while any checklist item UNVERIFIED; SKILL marks confirm=true as Core (C)."
    },
    {
      "id": "template-source-of-truth",
      "desc": "Template parse runtime tu leo-assist, khong copy; format doi -> fail loudly.",
      "assert": "templates.py reads skills/helix/leo-assist/references/leo-mode-templates.md at runtime; TemplateFormatError raised when expected modes missing; no template text duplicated in mcp/leo-bridge."
    },
    {
      "id": "verify-checklist-default-unverified",
      "desc": "Moi so lieu/part tu Leo mac dinh UNVERIFIED; khong cite -> flag do.",
      "assert": "parsers._build_checklist marks every number/part UNVERIFIED; missing citations adds explicit warning item; SKILL marks verify cite as Core (C)."
    },
    {
      "id": "traceability",
      "desc": "Moi exchange co ID + ledger JSONL append-only day du prompt/result/verify/route.",
      "assert": "Ledger.append writes JSONL with exchange_id/event/ts; leo_send, leo_ingest, leo_route all append events; ledger dir gitignored."
    }
  ]
}
```

- [ ] **Step 2: Commit**
```bash
git add evals/leo-bridge.json
git commit -m "[HELIX] Add leo-bridge static eval spec

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
```

---

### Task 12: Full test run + VERSION/CHANGELOG reconciliation

**Files:**
- Modify (có điều kiện — xem Step 2): `VERSION`, `CHANGELOG.md`

- [ ] **Step 1: Chạy toàn bộ test + selftest lần cuối**

Run:
```bash
python -m pytest mcp/leo-bridge/tests -v && python mcp/leo-bridge/server.py --selftest
```
Expected: tất cả PASS (≥23 tests) + selftest OK. Bất kỳ FAIL nào → sửa trước khi tiếp.

- [ ] **Step 2: Kiểm tra WIP không liên quan trong VERSION/CHANGELOG**

Run: `git diff VERSION CHANGELOG.md CLAUDE.md`

- **Nếu diff RỖNG** (WIP của feature spec-to-cad đã được commit/dọn ở nơi khác): đọc `VERSION` hiện tại, bump minor (ví dụ `1.2.0` → `1.3.0`), thêm entry đầu `CHANGELOG.md`:
  ```markdown
  ## [1.3.0] - 2026-07-04
  ### Added
  - `leo-bridge` MCP server (`mcp/leo-bridge/`): vòng khép kín bán tự động Workshop X ↔ getleo.ai — 6 tools (classify/prompt_build/send/ingest/route/ledger), gate MẬT deterministic hard-block 2 lần, clipboard transport + API stub (hybrid-ready), propose-only routing chặn UNVERIFIED vào parts_master, ledger JSONL traceability.
  - Skill `helix/leo-bridge` (wrapper orchestrate vòng MCP) + programmatic path trong `leo-assist`.
  - `evals/leo-bridge.json` (static) + draft email xin Leo API access.
  - `.mcp.json` đăng ký server (repo root).
  ```
  Rồi commit:
  ```bash
  git add VERSION CHANGELOG.md
  git commit -m "[HELIX] Bump v1.3.0: leo-bridge MCP server + skill

  Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>"
  ```
- **Nếu diff CÓ thay đổi không liên quan** (WIP spec-to-cad): KHÔNG commit 2 file này. Vẫn thêm entry CHANGELOG + bump VERSION trong working tree (để CEO có sẵn), nhưng ghi vào báo cáo cuối: "VERSION/CHANGELOG có WIP của feature/helix-spec-to-cad chưa commit — entry leo-bridge đã thêm sẵn trong working tree, CEO reconcile khi merge."

- [ ] **Step 3: Báo cáo hoàn thành**

Tổng kết cho CEO: số test pass, tools đã expose, đường dẫn skill/eval/email draft, trạng thái VERSION/CHANGELOG, và nhắc: (1) restart Claude Code để `.mcp.json` nạp server, (2) gửi email API access, (3) chạy thử vòng đầu tiên với 1 part search THƯỜNG thật.
