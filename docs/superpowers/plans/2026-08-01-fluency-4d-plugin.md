# Plugin `fluency-4d` Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Xây plugin `fluency-4d` tự chứa — huấn luyện viên AI Fluency chấm 12 ô 4D trên phiên làm việc thật, ghi sổ điểm trong vault, kê thí nghiệm hành vi WIP=1.

**Architecture:** Ba skill Markdown mỏng (`preflight`, `review`, `weekly`) đọc chung bốn file tham chiếu (`rubric-core.md`, `profile-workshop-x.md`, `ledger-schema.md`, `experiment-protocol.md`). Bản thân plugin **không có code**. Một linter Python nằm ở `scripts/` (trong repo, KHÔNG trong plugin) giữ bốn file tham chiếu khớp nhau và validate sổ điểm — đây là bộ test tự động của kế hoạch này.

**Tech Stack:** Markdown thuần cho plugin · Python 3.12 + pytest 9.1.1 cho linter · `evals/run-eval.sh` (chế độ `static`, chấm regex) cho audit SKILL.md · junction Windows để eval runner nhìn thấy skill.

**Spec:** `docs/superpowers/specs/2026-08-01-fluency-4d-plugin-design.md`

## Global Constraints

- Mọi file trong `plugins/fluency-4d/` là Markdown hoặc JSON. **Không Python, không hook, không MCP** trong plugin.
- 12 mã ô cố định, đúng thứ tự này ở mọi nơi: `del.problem`, `del.platform`, `del.task`, `des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`, `dil.creation`, `dil.transparency`, `dil.deployment`.
- Ba chế độ phiên: `automation`, `augmentation`, `agency`.
- Thang điểm: số nguyên `0`–`3`, hoặc `null` (= `n/a`). Không có giá trị nào khác.
- `rubric-core.md` **không được** chứa chuỗi "Workshop X", tên dự án, hay tên skill KN-Stack nào.
- `profile-workshop-x.md` **không được** định nghĩa lại thang điểm (không chứa "thang điểm", "0–3", "0-3").
- Sổ điểm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`.
- Ngôn ngữ nội dung: tiếng Việt. Mã ô, khóa JSON, trạng thái (`OPEN`/`PASSED`/`FAILED`): tiếng Anh.
- Nhánh làm việc: `feature/fluency-4d-plugin`. Commit format `[LEARN] <mô tả>`. Không commit thẳng `main`.
- Ghi file bằng UTF-8 **không BOM** (PowerShell `Set-Content -Encoding utf8` chèn BOM — dùng Write tool hoặc `[IO.File]::WriteAllText`).

## File Structure

| File | Trách nhiệm |
|---|---|
| `plugins/fluency-4d/.claude-plugin/plugin.json` | Manifest plugin |
| `plugins/fluency-4d/README.md` | Cách import vào Cowork, quyền truy cập sổ |
| `plugins/fluency-4d/skills/_shared/references/rubric-core.md` | 12 ô + thang điểm + 3 chốt chống nịnh. Trung lập ngành |
| `plugins/fluency-4d/skills/_shared/references/profile-workshop-x.md` | Tín hiệu / cờ đỏ / ví dụ cho từng ô. Thay được |
| `plugins/fluency-4d/skills/_shared/references/ledger-schema.md` | Schema JSONL + bản mẫu sao chép được |
| `plugins/fluency-4d/skills/_shared/references/experiment-protocol.md` | Luật WIP=1, nếu–thì, streak, nghiệm thu |
| `plugins/fluency-4d/skills/fluency-4d-preflight/SKILL.md` | Cổng trước khi giao việc |
| `plugins/fluency-4d/skills/fluency-4d-review/SKILL.md` | Mổ xẻ 6 bước |
| `plugins/fluency-4d/skills/fluency-4d-weekly/SKILL.md` | Tổng hợp tuần |
| `scripts/fluency_4d_lint.py` | Linter: parse rubric/profile/ledger/experiments, validate |
| `scripts/test_fluency_4d.py` | pytest cho linter |
| `evals/fluency-4d-review.json` | Eval tĩnh SKILL.md review |
| `evals/fluency-4d-preflight.json` | Eval tĩnh SKILL.md preflight |
| `evals/fluency-4d-weekly.json` | Eval tĩnh SKILL.md weekly |
| `evals/fixtures/fluency-4d-session.md` | Hội thoại mẫu cài sẵn 3 lỗi |

---

### Task 1: Khung plugin + `rubric-core.md` + linter mã ô

**Files:**
- Create: `plugins/fluency-4d/.claude-plugin/plugin.json`
- Create: `plugins/fluency-4d/skills/_shared/references/rubric-core.md`
- Create: `scripts/fluency_4d_lint.py`
- Test: `scripts/test_fluency_4d.py`

**Interfaces:**
- Consumes: *(không có — task đầu)*
- Produces: `CELLS: list[str]` (12 mã, đúng thứ tự), `MODES: set[str]`, `PLUGIN_ROOT: Path`, `REF_DIR: Path`, `parse_rubric_cells(text: str) -> list[str]`, `lint_rubric(text: str) -> list[str]` (trả danh sách lỗi, rỗng = đạt)

- [ ] **Step 1: Viết test thất bại**

Tạo `scripts/test_fluency_4d.py`:

```python
"""pytest cho linter plugin fluency-4d."""
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "fluency_4d_lint", Path(__file__).with_name("fluency_4d_lint.py")
)
lint = importlib.util.module_from_spec(_spec)
sys.modules["fluency_4d_lint"] = lint
_spec.loader.exec_module(lint)

RUBRIC = (lint.REF_DIR / "rubric-core.md").read_text(encoding="utf-8")


def test_cells_are_the_canonical_twelve():
    assert lint.CELLS == [
        "del.problem", "del.platform", "del.task",
        "des.product", "des.process", "des.performance",
        "dis.product", "dis.process", "dis.performance",
        "dil.creation", "dil.transparency", "dil.deployment",
    ]


def test_rubric_declares_all_twelve_cells_in_order():
    assert lint.parse_rubric_cells(RUBRIC) == lint.CELLS


def test_rubric_stays_vendor_neutral():
    assert lint.lint_rubric(RUBRIC) == []


def test_rubric_lint_flags_workshop_x_leakage():
    dirty = RUBRIC + "\n\nÁp dụng cho Workshop X.\n"
    assert any("Workshop X" in e for e in lint.lint_rubric(dirty))


def test_rubric_lint_flags_missing_cell():
    stripped = RUBRIC.replace("`dil.deployment`", "`dil.deploy`", 1)
    assert lint.lint_rubric(stripped)
```

- [ ] **Step 2: Chạy test để xác nhận nó fail**

Run: `cd /d/KN-Stack && python -m pytest scripts/test_fluency_4d.py -v`
Expected: FAIL — `FileNotFoundError` hoặc `ModuleNotFoundError` vì `fluency_4d_lint.py` chưa tồn tại.

- [ ] **Step 3: Viết `scripts/fluency_4d_lint.py`**

```python
"""Linter giữ bốn file tham chiếu của plugin fluency-4d khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown để Cowork nạp được).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "fluency-4d"
REF_DIR = PLUGIN_ROOT / "skills" / "_shared" / "references"

CELLS = [
    "del.problem", "del.platform", "del.task",
    "des.product", "des.process", "des.performance",
    "dis.product", "dis.process", "dis.performance",
    "dil.creation", "dil.transparency", "dil.deployment",
]
MODES = {"automation", "augmentation", "agency"}

# Mã ô trong rubric nằm ở cột đầu của bảng, bọc backtick: | `del.problem` | ...
_RUBRIC_CELL_RE = re.compile(r"^\|\s*`([a-z]{3}\.[a-z]+)`\s*\|", re.MULTILINE)

# Chuỗi cấm trong rubric-core.md — rubric phải trung lập ngành.
_RUBRIC_FORBIDDEN = ["Workshop X", "Pahl-Beitz", "analyst-trap", "ratio-check", "BQP", "MẬT"]


def parse_rubric_cells(text: str) -> list[str]:
    """Trả về danh sách mã ô rubric khai báo, theo đúng thứ tự xuất hiện."""
    return _RUBRIC_CELL_RE.findall(text)


def lint_rubric(text: str) -> list[str]:
    """Kiểm rubric-core.md. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    found = parse_rubric_cells(text)
    if found != CELLS:
        missing = [c for c in CELLS if c not in found]
        extra = [c for c in found if c not in CELLS]
        if missing:
            errors.append(f"rubric thiếu ô: {missing}")
        if extra:
            errors.append(f"rubric có ô lạ: {extra}")
        if not missing and not extra:
            errors.append(f"rubric sai thứ tự ô: {found}")
    for bad in _RUBRIC_FORBIDDEN:
        if bad in text:
            errors.append(f"rubric-core.md phải trung lập ngành, tìm thấy: {bad!r}")
    return errors
```

- [ ] **Step 4: Viết `plugin.json`**

```json
{
  "name": "fluency-4d",
  "description": "Huấn luyện viên AI Fluency tại chỗ theo khung 4D (Delegation, Description, Discernment, Diligence). Chấm 12 ô năng lực trên phiên làm việc thật, ghi sổ điểm, kê thí nghiệm hành vi. Ba lối vào: preflight trước khi giao việc, review cuối phiên, weekly tổng hợp xu hướng.",
  "version": "0.1.0",
  "author": {
    "name": "Workshop X"
  }
}
```

- [ ] **Step 5: Viết `rubric-core.md`**

Bố cục bắt buộc (linter phụ thuộc vào bảng ở mục 2):

````markdown
# Rubric lõi — AI Fluency 4D

> Khung gốc: *The AI Fluency Framework* — Rick Dakan, Joseph Feller, Anthropic.
> CC BY-NC-SA 4.0. File này là bản chuyển khung gốc sang dạng chấm được, trung lập ngành.
> Mọi tín hiệu riêng của một tổ chức nằm ở `profile-*.md`, không nằm ở đây.

## 1. Chế độ phiên

Trước khi chấm, xác định phiên chạy ở chế độ nào — Delegation phải chấm theo chế độ:

| Mã | Chế độ | Nghĩa |
|---|---|---|
| `automation` | Automation | AI thực thi tác vụ cụ thể theo chỉ dẫn |
| `augmentation` | Augmentation | Người và AI cùng nghĩ, cùng làm |
| `agency` | Agency | AI làm việc độc lập thay mặt người; người định hình tri thức và hành vi, không định hình từng hành động |

Giao ở chế độ Agency nhưng mô tả kiểu Automation → đó là lỗi **Delegation**, không phải lỗi Description.

## 2. Mười hai ô chấm

| Mã ô | Thành phần | Câu hỏi chấm |
|---|---|---|
| `del.problem` | Problem Awareness | Đã hiểu rõ mục tiêu và bản chất công việc TRƯỚC khi kéo AI vào chưa? |
| `del.platform` | Platform Awareness | Có biết công cụ/mô hình này làm được gì, không làm được gì? |
| `del.task` | Task Delegation | Chia việc giữa người và AI có tận dụng đúng thế mạnh mỗi bên? |
| `des.product` | Product Description | Đã nói rõ cần tạo ra cái gì: đầu ra, định dạng, người đọc, văn phong? |
| `des.process` | Process Description | Đã chỉ định AI tiếp cận theo cách nào? |
| `des.performance` | Performance Description | Đã nói rõ muốn AI hành xử ra sao: gọn hay chi tiết, phản biện hay thuận theo? |
| `dis.product` | Product Discernment | Có đánh giá chất lượng đầu ra: chính xác, phù hợp, mạch lạc, đúng trọng tâm? |
| `dis.process` | Process Discernment | Có soi cách AI đi đến kết quả: lỗi suy luận, bỏ sót, lập luận sai chỗ? |
| `dis.performance` | Performance Discernment | Có đánh giá cách AI hành xử trong lúc hợp tác — kiểu giao tiếp đó có phục vụ mình không? |
| `dil.creation` | Creation Diligence | Chọn công cụ và cách dùng có cân nhắc chưa? |
| `dil.transparency` | Transparency Diligence | Có nói rõ phần AI tham gia với những người cần biết? |
| `dil.deployment` | Deployment Diligence | Có kiểm chứng và đứng tên chịu trách nhiệm cho thứ mình đem dùng hoặc chia sẻ? |

## 3. Thang điểm

| Điểm | Nghĩa |
|---|---|
| `3` | Chủ động, nhất quán, trích dẫn được bằng chứng |
| `2` | Có làm nhưng thiếu hoặc không nhất quán |
| `1` | Chỉ xảy ra khi AI hoặc hoàn cảnh nhắc, không tự phát |
| `0` | Có cơ hội rõ ràng mà bỏ qua, hậu quả quan sát được trong phiên |
| `null` | `n/a` — phiên không tạo cơ hội để quan sát. **Khác `0`.** |

`0` là cáo buộc: phải chỉ được cơ hội bị bỏ lỡ VÀ hậu quả. Không chỉ được cả hai → đó là `null`.

## 4. Ba chốt chống nịnh

Người chấm là một nửa của chính cuộc hợp tác đang bị chấm. Ba chốt này là bắt buộc:

1. **Không bằng chứng, không điểm.** Mọi ô ≠ `3` phải kèm trích dẫn nguyên văn từ phiên. Không trích dẫn được → chấm `null`, không được đoán.
2. **Bắt buộc tìm điểm đau.** Báo cáo phải nêu ít nhất một ô ≤ `1`, hoặc tuyên bố thẳng "không tìm thấy ô nào dưới 2" kèm lý do. Im lặng bỏ qua là vi phạm.
3. **Chấm trước, khen sau.** Điểm và trích dẫn ra trước. Phần ghi nhận điểm mạnh chỉ được viết sau khi điểm đã chốt, để không neo.
````

- [ ] **Step 6: Chạy test để xác nhận pass**

Run: `cd /d/KN-Stack && python -m pytest scripts/test_fluency_4d.py -v`
Expected: PASS 5/5.

- [ ] **Step 7: Commit**

```bash
git add plugins/fluency-4d/.claude-plugin/plugin.json \
        plugins/fluency-4d/skills/_shared/references/rubric-core.md \
        scripts/fluency_4d_lint.py scripts/test_fluency_4d.py
git commit -m "[LEARN] fluency-4d: khung plugin + rubric lõi 12 ô + linter"
```

---

### Task 2: `profile-workshop-x.md` + kiểm khớp rubric↔profile

**Files:**
- Create: `plugins/fluency-4d/skills/_shared/references/profile-workshop-x.md`
- Modify: `scripts/fluency_4d_lint.py` (thêm `parse_profile`, `lint_profile`)
- Test: `scripts/test_fluency_4d.py` (thêm test)

**Interfaces:**
- Consumes: `CELLS`, `REF_DIR` từ Task 1
- Produces: `parse_profile(text: str) -> dict[str, dict[str, str]]` — khóa ngoài là mã ô, khóa trong là `"tin_hieu"` / `"co_do"` / `"vi_du"`; `lint_profile(text: str) -> list[str]`

- [ ] **Step 1: Viết test thất bại**

Thêm vào `scripts/test_fluency_4d.py`:

```python
PROFILE = (lint.REF_DIR / "profile-workshop-x.md").read_text(encoding="utf-8")


def test_profile_covers_every_rubric_cell():
    assert sorted(lint.parse_profile(PROFILE)) == sorted(lint.CELLS)


def test_profile_blocks_have_three_required_fields():
    for cell, block in lint.parse_profile(PROFILE).items():
        assert block["tin_hieu"].strip(), f"{cell} thiếu Tín hiệu"
        assert block["co_do"].strip(), f"{cell} thiếu Cờ đỏ"
        assert block["vi_du"].strip(), f"{cell} thiếu Ví dụ ngành"


def test_profile_is_clean():
    assert lint.lint_profile(PROFILE) == []


def test_profile_lint_flags_scale_redefinition():
    dirty = PROFILE + "\n## Thang điểm\nDùng thang 0-3 riêng.\n"
    assert any("thang điểm" in e.lower() for e in lint.lint_profile(dirty))


def test_profile_lint_flags_missing_cell():
    dirty = PROFILE.replace("## dil.deployment", "## dil.xxx", 1)
    assert any("dil.deployment" in e for e in lint.lint_profile(dirty))
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: FAIL — `AttributeError: module 'fluency_4d_lint' has no attribute 'parse_profile'`.

- [ ] **Step 3: Thêm parser vào `scripts/fluency_4d_lint.py`**

Nối vào cuối file:

```python
_PROFILE_BLOCK_RE = re.compile(
    r"^##\s+([a-z]{3}\.[a-z]+)\s*$(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_FIELD_RE = {
    "tin_hieu": re.compile(r"\*\*Tín hiệu:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
    "co_do": re.compile(r"\*\*Cờ đỏ:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
    "vi_du": re.compile(r"\*\*Ví dụ ngành:\*\*(.*?)(?=\*\*|\Z)", re.DOTALL),
}

# Profile chỉ bổ sung tín hiệu; không được định nghĩa lại thang điểm.
_PROFILE_FORBIDDEN = ["thang điểm", "0–3", "0-3"]


def parse_profile(text: str) -> dict[str, dict[str, str]]:
    """Trả về {mã ô: {tin_hieu, co_do, vi_du}} từ một file profile."""
    out: dict[str, dict[str, str]] = {}
    for cell, body in _PROFILE_BLOCK_RE.findall(text):
        fields = {}
        for key, rx in _FIELD_RE.items():
            m = rx.search(body)
            fields[key] = m.group(1).strip() if m else ""
        out[cell] = fields
    return out


def lint_profile(text: str) -> list[str]:
    """Kiểm một file profile khớp rubric. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    blocks = parse_profile(text)
    for cell in CELLS:
        if cell not in blocks:
            errors.append(f"profile thiếu khối cho ô: {cell}")
            continue
        for key, label in (("tin_hieu", "Tín hiệu"), ("co_do", "Cờ đỏ"), ("vi_du", "Ví dụ ngành")):
            if not blocks[cell][key].strip():
                errors.append(f"profile ô {cell} thiếu trường: {label}")
    for cell in blocks:
        if cell not in CELLS:
            errors.append(f"profile có ô lạ: {cell}")
    low = text.lower()
    for bad in _PROFILE_FORBIDDEN:
        if bad in low:
            errors.append(f"profile không được định nghĩa lại thang điểm, tìm thấy: {bad!r}")
    return errors
```

- [ ] **Step 4: Viết `profile-workshop-x.md`**

Mở đầu file:

```markdown
# Lớp hiệu chỉnh — Workshop X

> File này KHÔNG định nghĩa lại thang điểm. Thang điểm nằm ở `rubric-core.md`.
> Ở đây chỉ có: tín hiệu cần soi, cờ đỏ, ví dụ ngành — cho từng ô trong 12 ô.
> Muốn phát cho người khác: chép file này thành `profile-<tên>.md`, giữ nguyên
> khung `## <mã ô>` + ba trường, rồi đổi dòng trỏ trong ba SKILL.md.
```

Rồi đúng 12 khối theo thứ tự dưới đây. Mỗi khối là `## <mã ô>` + ba trường in đậm, không thêm trường nào khác:

```markdown
## del.problem

**Tín hiệu:** Task đã được phân loại COD (Core / Offload / Default) trước khi giao chưa? Mục tiêu và tiêu chí "xong" đã rõ trước khi mở phiên chưa?

**Cờ đỏ:** Việc thuộc Core (phán đoán thiết kế, quyết định gate, chọn phương án) mà đem giao trọn — chấm thấp bất kể kết quả tốt. Tỷ trọng thời gian Core vượt trần 60%.

**Ví dụ ngành:** "Chọn concept mặt bia nào" là Core. "Lập ma trận hình thái cho 4 concept" là Offload.

## del.platform

**Tín hiệu:** Chọn đúng tầng model cho loại việc — hạng nặng cho kiến trúc, gate review, thiết kế hệ thống; hạng nhẹ cho đọc file, soạn tài liệu, chạy test. Có tra xem KN-Stack đã có skill cho việc này chưa.

**Cờ đỏ:** Làm tay một việc đã có skill sẵn. Dùng model đắt cho việc đọc file. Giao việc cần công cụ ngoài (CAD, ERP) cho phiên không có công cụ đó.

**Ví dụ ngành:** Cần soi bản vẽ trước khi cấp phát xưởng — đã có `helix-cad-validate`, đừng dựng lại quy trình kiểm bằng tay.

## del.task

**Tín hiệu:** Việc được chia theo phase Pahl-Beitz hoặc theo khối giao được, mỗi khối có đầu vào–đầu ra rõ. Phần phán đoán thiết kế được giữ lại đích danh.

**Cờ đỏ:** Quăng cả cục "làm giúp anh cái này". Giao một lần cả bốn phase. Không nói phần nào tự làm.

**Ví dụ ngành:** Phase 2 concept: giao sinh ma trận hình thái và chấm sơ bộ, giữ lại quyết định chốt concept.

## des.product

**Tín hiệu:** Nói rõ đầu ra là gì, định dạng nào, ai đọc, và tiêu chí "xong" đo được. Mọi đại lượng vật lý dùng hệ mét.

**Cờ đỏ:** "Cứ làm đi rồi tính." Không nêu người đọc. Xuất hiện inch, pound, psi mà không quy đổi.

**Ví dụ ngành:** "Báo cáo 2 trang cho hội đồng nghiệm thu, có bảng so sánh 2 vật liệu, kết luận 1 dòng, xong = trả lời được câu hỏi chọn cái nào và vì sao."

## des.process

**Tín hiệu:** Chỉ định khung làm việc sẵn có — 3-Gate, VDI 2225, ODI, phase Pahl-Beitz, ACH — thay vì để AI tự chế quy trình.

**Cờ đỏ:** Bài toán chọn phương án mà không nhắc VDI 2225. Bài toán nhu cầu người dùng mà không nhắc ODI. AI tự bịa ra một khung lạ và không bị chặn.

**Ví dụ ngành:** "Chấm 4 concept theo VDI 2225, trọng số lấy từ danh mục yêu cầu Phase 1."

## des.performance

**Tín hiệu:** Nói rõ muốn AI phản biện hay thừa hành, gọn hay chi tiết, được phép hỏi lại đến đâu.

**Cờ đỏ:** Không bao giờ yêu cầu phản biện, rồi ngạc nhiên vì AI gật theo mọi thứ. Nhận một chuỗi đồng ý liên tiếp mà không thấy lạ.

**Ví dụ ngành:** "Đóng vai hội đồng nghiệm thu khó tính, tìm chỗ hồ sơ này sẽ bị bắt bẻ."

## dis.product

**Tín hiệu:** Có kiểm số trước khi dùng — chạy ratio-check, đòi bằng chứng vật lý (kết quả test, ảnh, số đo), hỏi nguồn cho mọi con số then chốt.

**Cờ đỏ:** Nhận một con số kỹ thuật rồi đưa thẳng vào hồ sơ mà không hỏi nguồn. Chấp nhận "khoảng", "ước tính" cho tham số đi vào quyết định.

**Ví dụ ngành:** AI đưa giới hạn chảy 245 MPa cho SS400 — hỏi tiêu chuẩn nào, bản nào, dày bao nhiêu, trước khi dùng để tính.

## dis.process

**Tín hiệu:** Soi cách AI đi tới kết luận — nguồn có phân tier S/A/B/C không, có kiểm chéo ít nhất hai nguồn độc lập cho khẳng định quan trọng không.

**Cờ đỏ:** Kết luận dựa trên một nguồn duy nhất. Trích dẫn không kiểm được. Suy luận nhảy bước mà không bị hỏi.

**Ví dụ ngành:** Kết luận về sản phẩm đối thủ chỉ dựa trên một trang marketing — chưa đủ tier để đưa vào hồ sơ cạnh tranh.

## dis.performance

**Tín hiệu:** Bắt được lúc AI trôi sang analyst-trap — đẻ thêm phân tích, khung, tài liệu thay vì đẩy tới dữ liệu vật lý — và kéo lại.

**Cờ đỏ:** Phiên kết thúc với thêm ba tài liệu phân tích và không có hành động vật lý nào. AI đề xuất "nghiên cứu thêm" và được chấp nhận không phản biện.

**Ví dụ ngành:** Đang bí ở khâu chọn vật liệu, AI đề xuất lập thêm ma trận đánh giá — câu hỏi đúng là "chỗ này cần thêm phân tích hay cần một mẫu thử?"

## dil.creation

**Tín hiệu:** Không đưa dữ liệu MẬT, không đưa giá nhà cung cấp, không đưa thông tin định danh đối tác vào prompt. Cân nhắc phiên này chạy ở đâu, ai đọc được.

**Cờ đỏ:** Dán bảng báo giá có tên nhà cung cấp. Dán nội dung có dấu mật. Đưa thông số khí tài nhạy cảm vào dịch vụ ngoài. **Bất kỳ cái nào cũng là điểm `0` và bật cờ đỏ.**

**Ví dụ ngành:** Cần so sánh chi phí thì dùng "nhà cung cấp A / B" với giá tương đối, không dùng tên và giá thật.

## dil.transparency

**Tín hiệu:** Tài liệu giao ra ngoài — BQP, hội đồng, đối tác — có ghi rõ phần nào AI tham gia và người ký đã kiểm.

**Cờ đỏ:** Nộp hồ sơ do AI soạn phần lớn mà không ghi nhận gì. Để người đọc mặc định đó là công sức thủ công.

**Ví dụ ngành:** Thuyết minh đề tài KHCN: nêu rõ phần tổng hợp tài liệu có AI hỗ trợ, phần số liệu thử nghiệm là đo thật.

## dil.deployment

**Tín hiệu:** Chạy test trước khi mở PR, không commit thẳng `main`, tự đọc lại và đứng tên chịu trách nhiệm cho thứ đem dùng.

**Cờ đỏ:** Commit thẳng `main`. Mở PR chưa chạy test. Ký vào tài liệu chưa đọc hết. Đem kết quả AI đi họp mà chưa tự kiểm.

**Ví dụ ngành:** Bản vẽ chế tạo do AI sinh phải qua `helix-cad-validate` và mắt người trước khi xuống xưởng cắt.
```

- [ ] **Step 5: Chạy test để xác nhận pass**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: PASS 10/10.

- [ ] **Step 6: Commit**

```bash
git add plugins/fluency-4d/skills/_shared/references/profile-workshop-x.md \
        scripts/fluency_4d_lint.py scripts/test_fluency_4d.py
git commit -m "[LEARN] fluency-4d: lớp hiệu chỉnh Workshop X + kiểm khớp rubric-profile"
```

---

### Task 3: `ledger-schema.md` + validator dòng JSONL

**Files:**
- Create: `plugins/fluency-4d/skills/_shared/references/ledger-schema.md`
- Modify: `scripts/fluency_4d_lint.py` (thêm `SAMPLE_RE`, `extract_sample_record`, `validate_ledger_line`)
- Test: `scripts/test_fluency_4d.py`

**Interfaces:**
- Consumes: `CELLS`, `MODES`, `REF_DIR`
- Produces: `validate_ledger_line(obj: dict) -> list[str]`, `extract_sample_record(text: str) -> dict` (lấy bản mẫu JSON đầu tiên trong khối ```json của `ledger-schema.md`)

- [ ] **Step 1: Viết test thất bại**

```python
import copy
import json

LEDGER_DOC = (lint.REF_DIR / "ledger-schema.md").read_text(encoding="utf-8")


def _good_record():
    return copy.deepcopy(lint.extract_sample_record(LEDGER_DOC))


def test_sample_record_in_doc_is_valid():
    assert lint.validate_ledger_line(_good_record()) == []


def test_sample_record_has_every_cell():
    rec = _good_record()
    flat = {f"{g}.{k}" for g, sub in rec["scores"].items() for k in sub}
    assert flat == set(lint.CELLS)


def test_rejects_missing_top_level_key():
    rec = _good_record()
    del rec["weakest"]
    assert any("weakest" in e for e in lint.validate_ledger_line(rec))


def test_rejects_score_out_of_range():
    rec = _good_record()
    rec["scores"]["del"]["problem"] = 4
    assert any("del.problem" in e for e in lint.validate_ledger_line(rec))


def test_accepts_null_as_na():
    rec = _good_record()
    rec["scores"]["del"]["problem"] = None
    assert lint.validate_ledger_line(rec) == []


def test_rejects_unknown_mode():
    rec = _good_record()
    rec["mode"] = "collaboration"
    assert any("mode" in e for e in lint.validate_ledger_line(rec))


def test_rejects_bad_id_format():
    rec = _good_record()
    rec["id"] = "2026-08-01"
    assert any("id" in e for e in lint.validate_ledger_line(rec))


def test_rejects_weakest_not_a_cell():
    rec = _good_record()
    rec["weakest"] = "des.speed"
    assert any("weakest" in e for e in lint.validate_ledger_line(rec))


def test_exp_active_and_exp_held_must_agree():
    rec = _good_record()
    rec["exp_active"] = None
    assert any("exp_held" in e for e in lint.validate_ledger_line(rec))
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: FAIL — `AttributeError: ... 'extract_sample_record'`.

- [ ] **Step 3: Thêm validator vào `scripts/fluency_4d_lint.py`**

```python
import json

_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.DOTALL)
_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-\d+$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_EXP_RE = re.compile(r"^EXP-\d{3}$")

_GROUPS = {
    "del": ["problem", "platform", "task"],
    "des": ["product", "process", "performance"],
    "dis": ["product", "process", "performance"],
    "dil": ["creation", "transparency", "deployment"],
}
_TOP_KEYS = ["id", "date", "project", "mode", "scores", "weakest", "exp_active", "exp_held"]


def extract_sample_record(text: str) -> dict:
    """Lấy bản ghi mẫu trong khối ```json đầu tiên của ledger-schema.md."""
    m = _JSON_BLOCK_RE.search(text)
    if not m:
        raise ValueError("ledger-schema.md không có khối ```json nào")
    return json.loads(m.group(1))


def validate_ledger_line(obj: dict) -> list[str]:
    """Kiểm một bản ghi sổ điểm. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    for key in _TOP_KEYS:
        if key not in obj:
            errors.append(f"thiếu khóa bắt buộc: {key}")
    if errors:
        return errors

    if not _ID_RE.match(str(obj["id"])):
        errors.append(f"id sai định dạng <YYYY-MM-DD>-<n>: {obj['id']!r}")
    if not _DATE_RE.match(str(obj["date"])):
        errors.append(f"date sai định dạng YYYY-MM-DD: {obj['date']!r}")
    if not str(obj["project"]).strip():
        errors.append("project rỗng")
    if obj["mode"] not in MODES:
        errors.append(f"mode không hợp lệ: {obj['mode']!r} (phải thuộc {sorted(MODES)})")

    scores = obj["scores"]
    if not isinstance(scores, dict):
        errors.append("scores phải là object")
    else:
        if set(scores) != set(_GROUPS):
            errors.append(f"scores sai nhóm: {sorted(scores)} (cần {sorted(_GROUPS)})")
        for group, subs in _GROUPS.items():
            sub = scores.get(group)
            if not isinstance(sub, dict):
                errors.append(f"scores.{group} phải là object")
                continue
            if set(sub) != set(subs):
                errors.append(f"scores.{group} sai khóa con: {sorted(sub)} (cần {sorted(subs)})")
            for name, val in sub.items():
                if val is None:
                    continue
                if not isinstance(val, int) or isinstance(val, bool) or not 0 <= val <= 3:
                    errors.append(f"{group}.{name} phải là số nguyên 0-3 hoặc null, gặp: {val!r}")

    if obj["weakest"] is not None and obj["weakest"] not in CELLS:
        errors.append(f"weakest không phải mã ô hợp lệ: {obj['weakest']!r}")

    exp, held = obj["exp_active"], obj["exp_held"]
    if exp is not None and not _EXP_RE.match(str(exp)):
        errors.append(f"exp_active sai định dạng EXP-###: {exp!r}")
    if held is not None and not isinstance(held, bool):
        errors.append(f"exp_held phải là true/false/null, gặp: {held!r}")
    if (exp is None) != (held is None):
        errors.append("exp_active và exp_held phải cùng null hoặc cùng có giá trị")

    return errors
```

- [ ] **Step 4: Viết `ledger-schema.md`**

````markdown
# Schema sổ điểm

Sổ nằm ở: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`

```
AI-Fluency-Ledger/
├── sessions.jsonl        ← mỗi lần mổ xẻ = 1 dòng, CHỈ APPEND
├── experiments.md        ← thí nghiệm hành vi
└── weekly/2026-W31.md    ← báo cáo tuần
```

## Bản mẫu — sao chép nguyên khung này

```json
{"id":"2026-08-01-1","date":"2026-08-01","project":"VN-TGT-F","mode":"augmentation","scores":{"del":{"problem":2,"platform":3,"task":1},"des":{"product":2,"process":0,"performance":null},"dis":{"product":1,"process":2,"performance":3},"dil":{"creation":3,"transparency":null,"deployment":2}},"weakest":"des.process","exp_active":"EXP-014","exp_held":true}
```

## Luật

| Khóa | Kiểu | Luật |
|---|---|---|
| `id` | chuỗi | `<YYYY-MM-DD>-<số thứ tự phiên trong ngày>` |
| `date` | chuỗi | `YYYY-MM-DD` |
| `project` | chuỗi | Mã dự án hoặc chủ đề phiên. Không để rỗng |
| `mode` | chuỗi | `automation` · `augmentation` · `agency` |
| `scores` | object | Đúng 4 nhóm `del`/`des`/`dis`/`dil`, mỗi nhóm đúng 3 khóa con. **Mọi khóa luôn có mặt**, kể cả khi `null` |
| giá trị điểm | số / null | Số nguyên `0`–`3`, hoặc `null` (= `n/a`) |
| `weakest` | chuỗi / null | Một trong 12 mã ô, hoặc `null` nếu không có ô nào ≤ 2 |
| `exp_active` | chuỗi / null | `EXP-###` của thí nghiệm đang mở |
| `exp_held` | bool / null | Phiên này có giữ được thí nghiệm không |

**Ràng buộc chéo:** `exp_active` và `exp_held` phải cùng `null` hoặc cùng có giá trị.

**Trích dẫn bằng chứng KHÔNG vào file này** — xuống dòng và ký tự đặc biệt sẽ làm hỏng JSONL. Bằng chứng nằm trong báo cáo mổ xẻ in ra màn hình. Sổ chỉ giữ con số.

**Chỉ append.** Không sửa, không xóa dòng cũ. Chấm sai thì ghi dòng mới cùng ngày với số thứ tự kế tiếp và ghi chú trong báo cáo.
````

- [ ] **Step 5: Chạy test để xác nhận pass**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: PASS 19/19.

- [ ] **Step 6: Commit**

```bash
git add plugins/fluency-4d/skills/_shared/references/ledger-schema.md \
        scripts/fluency_4d_lint.py scripts/test_fluency_4d.py
git commit -m "[LEARN] fluency-4d: schema sổ điểm JSONL + validator"
```

---

### Task 4: `experiment-protocol.md` + parser/streak

**Files:**
- Create: `plugins/fluency-4d/skills/_shared/references/experiment-protocol.md`
- Modify: `scripts/fluency_4d_lint.py` (thêm `parse_experiments`, `validate_experiments`, `apply_session`)
- Modify: `docs/superpowers/specs/2026-08-01-fluency-4d-plugin-design.md` §7 (bổ sung cột `đứt`)
- Test: `scripts/test_fluency_4d.py`

**Interfaces:**
- Consumes: `CELLS`
- Produces: `parse_experiments(text: str) -> list[dict]` (khóa: `id`, `cell`, `if_then`, `streak`, `breaks`, `status`, `opened`, `closed`), `validate_experiments(rows: list[dict]) -> list[str]`, `apply_session(row: dict, held: bool) -> dict` (trả bản ghi MỚI, không sửa tại chỗ)

**Sửa spec:** Spec §7 mô tả bảng 7 cột nhưng luật "đứt 3 lần → FAILED" không đếm được nếu thiếu chỗ lưu. Bảng có **8 cột**, thêm `đứt`. Cập nhật spec trong task này.

- [ ] **Step 1: Viết test thất bại**

```python
EXP_DOC = (lint.REF_DIR / "experiment-protocol.md").read_text(encoding="utf-8")


def test_sample_table_parses():
    rows = lint.parse_experiments(EXP_DOC)
    assert rows, "experiment-protocol.md phải có bảng mẫu"
    assert rows[0]["id"].startswith("EXP-")
    assert rows[0]["cell"] in lint.CELLS


def test_sample_table_is_valid():
    assert lint.validate_experiments(lint.parse_experiments(EXP_DOC)) == []


def test_wip_one_enforced():
    rows = [
        {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
         "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""},
        {"id": "EXP-002", "cell": "dis.product", "if_then": "Khi nhận số, tôi hỏi nguồn.",
         "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-02", "closed": ""},
    ]
    assert any("WIP" in e for e in lint.validate_experiments(rows))


def test_if_then_form_required():
    rows = [{"id": "EXP-001", "cell": "des.product", "if_then": "Chú ý Description hơn.",
             "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}]
    assert any("nếu–thì" in e for e in lint.validate_experiments(rows))


def test_passed_requires_streak_three():
    rows = [{"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
             "streak": 2, "breaks": 0, "status": "PASSED", "opened": "2026-08-01", "closed": "2026-08-04"}]
    assert any("PASSED" in e for e in lint.validate_experiments(rows))


def test_streak_increments_on_hold():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    assert lint.apply_session(row, held=True)["streak"] == 2


def test_third_hold_passes_the_experiment():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 2, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=True)
    assert out["streak"] == 3 and out["status"] == "PASSED"


def test_break_resets_streak_and_counts():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 2, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=False)
    assert out["streak"] == 0 and out["breaks"] == 1 and out["status"] == "OPEN"


def test_third_break_fails_the_experiment():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 2, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    out = lint.apply_session(row, held=False)
    assert out["breaks"] == 3 and out["status"] == "FAILED"


def test_apply_session_does_not_mutate_input():
    row = {"id": "EXP-001", "cell": "des.product", "if_then": "Khi giao task, tôi nêu tiêu chí xong.",
           "streak": 1, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    lint.apply_session(row, held=True)
    assert row["streak"] == 1
```

- [ ] **Step 2: Chạy test để xác nhận fail**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: FAIL — `AttributeError: ... 'parse_experiments'`.

- [ ] **Step 3: Thêm vào `scripts/fluency_4d_lint.py`**

```python
STREAK_TO_PASS = 3
BREAKS_TO_FAIL = 3
_STATUSES = {"OPEN", "PASSED", "FAILED"}
_EXP_COLS = ["id", "cell", "if_then", "streak", "breaks", "status", "opened", "closed"]


def parse_experiments(text: str) -> list[dict]:
    """Đọc bảng thí nghiệm trong Markdown. Bỏ qua dòng tiêu đề và dòng gạch."""
    rows: list[dict] = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("`") for c in line.strip("|").split("|")]
        if len(cells) != len(_EXP_COLS):
            continue
        if not re.match(r"^EXP-\d{3}$", cells[0]):
            continue
        row = dict(zip(_EXP_COLS, cells))
        for key in ("streak", "breaks"):
            row[key] = int(row[key]) if row[key].isdigit() else -1
        rows.append(row)
    return rows


def validate_experiments(rows: list[dict]) -> list[str]:
    """Kiểm bảng thí nghiệm. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    seen: set[str] = set()
    open_rows = [r for r in rows if r["status"] == "OPEN"]
    if len(open_rows) > 1:
        errors.append(f"vi phạm WIP=1: có {len(open_rows)} thí nghiệm OPEN ({[r['id'] for r in open_rows]})")
    for r in rows:
        if r["id"] in seen:
            errors.append(f"trùng ID: {r['id']}")
        seen.add(r["id"])
        if r["cell"] not in CELLS:
            errors.append(f"{r['id']}: ô mục tiêu không hợp lệ: {r['cell']!r}")
        if not r["if_then"].startswith("Khi ") or " tôi " not in r["if_then"]:
            errors.append(f"{r['id']}: câu phải ở dạng nếu–thì hành vi 'Khi ... , tôi ...': {r['if_then']!r}")
        if r["status"] not in _STATUSES:
            errors.append(f"{r['id']}: trạng thái lạ: {r['status']!r}")
        if not 0 <= r["streak"] <= STREAK_TO_PASS:
            errors.append(f"{r['id']}: streak ngoài khoảng 0-{STREAK_TO_PASS}: {r['streak']}")
        if not 0 <= r["breaks"] <= BREAKS_TO_FAIL:
            errors.append(f"{r['id']}: đứt ngoài khoảng 0-{BREAKS_TO_FAIL}: {r['breaks']}")
        if r["status"] == "PASSED" and r["streak"] != STREAK_TO_PASS:
            errors.append(f"{r['id']}: PASSED phải có streak = {STREAK_TO_PASS}, gặp {r['streak']}")
        if r["status"] == "FAILED" and r["breaks"] != BREAKS_TO_FAIL:
            errors.append(f"{r['id']}: FAILED phải có đứt = {BREAKS_TO_FAIL}, gặp {r['breaks']}")
        if r["status"] in {"PASSED", "FAILED"} and not r["closed"].strip():
            errors.append(f"{r['id']}: đã đóng nhưng thiếu ngày đóng")
    return errors


def apply_session(row: dict, held: bool) -> dict:
    """Áp kết quả một phiên lên thí nghiệm. Trả bản ghi MỚI."""
    out = dict(row)
    if held:
        out["streak"] = row["streak"] + 1
        if out["streak"] >= STREAK_TO_PASS:
            out["streak"] = STREAK_TO_PASS
            out["status"] = "PASSED"
    else:
        out["streak"] = 0
        out["breaks"] = row["breaks"] + 1
        if out["breaks"] >= BREAKS_TO_FAIL:
            out["breaks"] = BREAKS_TO_FAIL
            out["status"] = "FAILED"
    return out
```

- [ ] **Step 4: Viết `experiment-protocol.md`**

```markdown
# Giao thức thí nghiệm hành vi

## Luật

1. **WIP = 1.** Chỉ một thí nghiệm `OPEN` tại một thời điểm. Phát hiện 5 điểm yếu vẫn chỉ kê 1. Ràng buộc cứng, không phải gợi ý.
2. **Dạng nếu–thì.** Câu phải bắt đầu bằng "Khi " và chứa " tôi ", mô tả hành vi quan sát được. Cấm viết kiểu "chú ý Description hơn".
3. **Cách đo.** Mỗi phiên sau ghi `exp_held: true/false` vào sổ.
4. **Nghiệm thu.** Giữ 3 phiên liên tiếp → `PASSED`, đóng, mở thí nghiệm mới.
5. **Đứt.** Streak về 0, số lần đứt +1. Đứt lần thứ 3 → `FAILED`.
6. **Sau `FAILED`.** Kê thí nghiệm NHỎ HƠN nhắm cùng ô. Cấm chép lại nguyên văn câu cũ.

## Bảng `experiments.md`

| ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng |
|---|---|---|---|---|---|---|---|
| `EXP-001` | `des.product` | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi. | 3 | 0 | PASSED | 2026-08-01 | 2026-08-05 |
| `EXP-002` | `dis.product` | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng. | 1 | 0 | OPEN | 2026-08-06 |  |

## Ví dụ tốt và xấu

| Xấu | Tốt |
|---|---|
| Chú ý Description hơn | Khi giao task > 30 phút, tôi nêu tiêu chí "xong" trước khi bấm gửi |
| Kiểm chứng kỹ hơn | Khi nhận một con số từ AI, tôi hỏi nguồn trước khi dùng |
| Delegation tốt hơn | Khi mở phiên, tôi nói rõ task này là Core hay Offload trước câu hỏi đầu tiên |
```

- [ ] **Step 5: Cập nhật spec §7**

Trong `docs/superpowers/specs/2026-08-01-fluency-4d-plugin-design.md`, sửa dòng mô tả bảng thành:

```
**Bảng `experiments.md`:** `ID | ô mục tiêu | câu nếu–thì | streak | đứt | trạng thái | ngày mở | ngày đóng`
```

Thêm ngay dưới đó: `Cột `đứt` đếm số lần streak bị phá; đạt 3 → `FAILED`.`

- [ ] **Step 6: Chạy test để xác nhận pass**

Run: `python -m pytest scripts/test_fluency_4d.py -v`
Expected: PASS 29/29.

- [ ] **Step 7: Commit**

```bash
git add plugins/fluency-4d/skills/_shared/references/experiment-protocol.md \
        docs/superpowers/specs/2026-08-01-fluency-4d-plugin-design.md \
        scripts/fluency_4d_lint.py scripts/test_fluency_4d.py
git commit -m "[LEARN] fluency-4d: giao thức thí nghiệm WIP=1 + máy trạng thái streak"
```

---

### Task 5: `fluency-4d-review/SKILL.md` + eval tĩnh

**Files:**
- Create: `plugins/fluency-4d/skills/fluency-4d-review/SKILL.md`
- Create: `evals/fluency-4d-review.json`
- Test: `bash evals/run-eval.sh fluency-4d-review`

**Interfaces:**
- Consumes: bốn file tham chiếu từ Task 1–4
- Produces: SKILL.md chứa 6 bước, 3 chốt chống nịnh, WIP=1, ngoại lệ cờ đỏ Diligence — các mốc regex mà eval bám vào

**Ràng buộc runner:** `evals/run-eval.sh` tìm skill ở `$HOME/.claude/commands/<tên>/SKILL.md`. Phải tạo junction trước khi chạy eval.

- [ ] **Step 1: Viết eval trước (đây là "test thất bại")**

Tạo `evals/fluency-4d-review.json`:

```json
{
  "skill": "fluency-4d-review",
  "version": "1.0",
  "description": "Binary assertions cho skill mổ xẻ phiên theo khung 4D",
  "mode": "static",
  "total_required": 10,
  "passing_score": 10,
  "assertions": [
    {"id": "4DR-CELLS", "name": "twelve_cells", "check": "liệt kê đủ 12 mã ô, mốc đầu và mốc cuối", "regex": "del\\.problem[\\s\\S]*dil\\.deployment", "required": true},
    {"id": "4DR-SCALE", "name": "scale_with_na", "check": "thang 0-3 và null tách bạch khỏi 0", "regex": "null[^\\n]*n/a|n/a[^\\n]*khác", "required": true},
    {"id": "4DR-EVIDENCE", "name": "no_evidence_no_score", "check": "chốt 1: không trích dẫn được thì chấm null", "regex": "[Kk]hông bằng chứng, không điểm", "required": true},
    {"id": "4DR-PAIN", "name": "must_find_pain", "check": "chốt 2: bắt buộc nêu ô ≤ 1 hoặc tuyên bố rõ", "regex": "ít nhất một ô ≤ ?1|không tìm thấy ô nào dưới 2", "required": true},
    {"id": "4DR-ORDER", "name": "score_before_praise", "check": "chốt 3: chấm trước, khen sau", "regex": "[Cc]hấm trước, khen sau", "required": true},
    {"id": "4DR-6STEPS", "name": "six_steps", "check": "quy trình có đủ 6 bước đánh số", "regex": "Bước 6", "required": true},
    {"id": "4DR-VERIFY-FIRST", "name": "experiment_verified_first", "check": "nghiệm thu thí nghiệm đang mở TRƯỚC khi kê mới", "regex": "nghiệm thu[\\s\\S]{0,120}trước", "required": true},
    {"id": "4DR-WIP", "name": "wip_one", "check": "còn thí nghiệm OPEN thì không kê mới", "regex": "WIP ?= ?1", "required": true},
    {"id": "4DR-REDFLAG", "name": "diligence_red_flag", "check": "Diligence = 0 bật cờ đỏ, không vào vòng thí nghiệm", "regex": "cờ đỏ", "required": true},
    {"id": "4DR-LEDGER", "name": "append_ledger", "check": "append đúng 1 dòng vào sessions.jsonl, bằng chứng không vào JSONL", "regex": "sessions\\.jsonl", "required": true}
  ]
}
```

- [ ] **Step 2: Tạo junction rồi chạy eval để xác nhận fail**

```powershell
New-Item -ItemType Junction -Path "C:\Users\Admin\.claude\commands\fluency-4d-review" -Target "D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-review"
```

Run: `bash evals/run-eval.sh fluency-4d-review`
Expected: `ERROR: Skill file not found for: fluency-4d-review` (junction trỏ tới thư mục chưa có `SKILL.md`).

- [ ] **Step 3: Viết `fluency-4d-review/SKILL.md`**

```markdown
---
name: fluency-4d-review
description: Mổ xẻ phiên làm việc vừa xong theo khung AI Fluency 4D — chấm 12 ô năng lực bằng bằng chứng trích dẫn từ chính phiên, nghiệm thu thí nghiệm hành vi đang mở, kê thí nghiệm mới, ghi một dòng vào sổ điểm. Triggers on "4d review", "mổ xẻ phiên", "chấm phiên", "review fluency", "phiên vừa rồi thế nào", "đánh giá cách tôi làm việc với AI", "chấm 4D".
---

# /fluency-4d-review — Mổ xẻ phiên theo khung 4D

**COD:** Offload (AI chấm + ghi sổ) · Core (CEO nhận thí nghiệm và thực thi)

Đọc trước khi chấm:
- `../_shared/references/rubric-core.md` — 12 ô, thang điểm, ba chốt chống nịnh
- `../_shared/references/profile-workshop-x.md` — tín hiệu và cờ đỏ cho từng ô
- `../_shared/references/ledger-schema.md` — schema dòng sổ
- `../_shared/references/experiment-protocol.md` — luật WIP=1 và streak

Sổ điểm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\`

## Ba chốt bắt buộc

1. **Không bằng chứng, không điểm.** Mọi ô ≠ 3 phải kèm trích dẫn nguyên văn từ phiên này. Không trích dẫn được → chấm `null` (n/a). Cấm suy đoán.
2. **Bắt buộc tìm điểm đau.** Báo cáo phải nêu ít nhất một ô ≤ 1, hoặc nói thẳng "không tìm thấy ô nào dưới 2" kèm lý do.
3. **Chấm trước, khen sau.** In bảng điểm và trích dẫn xong mới được viết phần ghi nhận điểm mạnh.

`null` là "phiên không tạo cơ hội quan sát" — **khác** `0` là "có cơ hội mà bỏ qua, hậu quả thấy được".

## Sáu bước

**Bước 1 — Trích bằng chứng.** Đọc lại phiên hội thoại đang trong ngữ cảnh (không đi tìm file log). Trích nguyên văn các đoạn liên quan tới từng ô.

**Bước 2 — Chấm 12 ô.** Theo `rubric-core.md`, soi tín hiệu trong `profile-workshop-x.md`. Ghi chế độ phiên: automation / augmentation / agency. Thứ tự: `del.problem`, `del.platform`, `del.task`, `des.product`, `des.process`, `des.performance`, `dis.product`, `dis.process`, `dis.performance`, `dil.creation`, `dil.transparency`, `dil.deployment`.

**Bước 3 — Nghiệm thu thí nghiệm đang mở TRƯỚC.** Đọc `experiments.md`. Nếu có dòng `OPEN`: phiên này giữ được hay đứt? Giữ → streak +1 (đủ 3 → `PASSED`, ghi ngày đóng). Đứt → streak về 0, cột `đứt` +1 (đủ 3 → `FAILED`). Làm xong bước này rồi mới đi tiếp.

**Bước 4 — Chọn ô yếu nhất.** Điểm thấp nhất. Hòa → ô xuất hiện làm `weakest` nhiều lần nhất trong `sessions.jsonl` 30 ngày gần nhất. Vẫn hòa → thứ tự ưu tiên `dil` > `dis` > `des` > `del`.

**Bước 5 — Kê hoặc giữ thí nghiệm.** **WIP = 1.** Còn dòng `OPEN` sau Bước 3 → giữ nguyên, KHÔNG kê mới, kể cả khi Bước 4 tìm được ô yếu nặng hơn; chỉ nói một dòng rằng ô đó đang xếp hàng. Không còn dòng `OPEN` → kê đúng một thí nghiệm dạng nếu–thì ("Khi …, tôi …"), nhắm ô ở Bước 4. Nếu thí nghiệm vừa `FAILED` → kê cái NHỎ HƠN cho cùng ô, cấm chép lại câu cũ.

**Bước 6 — Ghi sổ.** Append đúng một dòng vào `sessions.jsonl` theo `ledger-schema.md`; cập nhật `experiments.md`. Trích dẫn bằng chứng KHÔNG được đưa vào `sessions.jsonl` — nó chỉ nằm trong báo cáo in ra màn hình.

## Ngoại lệ cờ đỏ

Bất kỳ ô `dil.*` nào chấm `0` — rò rỉ dữ liệu MẬT, dán giá nhà cung cấp, commit thẳng `main` — thì **không** đi vào vòng thí nghiệm. Đặt cảnh báo **CỜ ĐỎ** lên đầu báo cáo, nêu việc phải xử ngay trong phiên. Vòng thí nghiệm dành cho thói quen dài hạn, không dành cho sự cố cần xử lý ngay.

## Khuôn báo cáo

```
## Mổ xẻ phiên <id> — <dự án> — chế độ <mode>

[CỜ ĐỎ nếu có, đặt trên cùng]

### Điểm
| Ô | Điểm | Bằng chứng |
|---|---|---|
| del.problem | 2 | "…trích nguyên văn…" |
… đủ 12 dòng …

### Điểm đau
<ô ≤ 1 và vì sao> HOẶC "không tìm thấy ô nào dưới 2 vì …"

### Thí nghiệm
<nghiệm thu cái đang mở> → <kê mới HOẶC giữ nguyên vì WIP=1>

### Ghi nhận
<điểm mạnh — chỉ viết sau khi điểm đã chốt>

### Đã ghi sổ
<dòng JSONL vừa append>
```
```

- [ ] **Step 4: Chạy eval để xác nhận pass**

Run: `bash evals/run-eval.sh fluency-4d-review`
Expected: `Score: 10/10 (100%)` và `RESULT: PERFECT`.

- [ ] **Step 5: Commit**

```bash
git add plugins/fluency-4d/skills/fluency-4d-review/SKILL.md evals/fluency-4d-review.json
git commit -m "[LEARN] fluency-4d: skill mổ xẻ 6 bước + eval tĩnh 10/10"
```

---

### Task 6: `fluency-4d-preflight/SKILL.md` + eval tĩnh

**Files:**
- Create: `plugins/fluency-4d/skills/fluency-4d-preflight/SKILL.md`
- Create: `evals/fluency-4d-preflight.json`
- Test: `bash evals/run-eval.sh fluency-4d-preflight`

**Interfaces:**
- Consumes: `rubric-core.md`, `profile-workshop-x.md`, `experiments.md`
- Produces: SKILL.md có hai cổng (Delegation, Description) + hành vi chặn khi task là Core

- [ ] **Step 1: Viết eval trước**

Tạo `evals/fluency-4d-preflight.json`:

```json
{
  "skill": "fluency-4d-preflight",
  "version": "1.0",
  "description": "Binary assertions cho cổng preflight 4D",
  "mode": "static",
  "total_required": 7,
  "passing_score": 7,
  "assertions": [
    {"id": "4DP-GATE-DEL", "name": "delegation_gate", "check": "cổng Delegation hỏi C/O/D và chế độ", "regex": "Core ?/ ?Offload ?/ ?Default|COD", "required": true},
    {"id": "4DP-MODE", "name": "mode_choice", "check": "buộc chọn chế độ tương tác", "regex": "automation[\\s\\S]{0,60}augmentation[\\s\\S]{0,60}agency", "required": true},
    {"id": "4DP-BLOCK", "name": "blocks_core_delegation", "check": "task là Core mà định giao thì chặn và hỏi lại", "regex": "chặn", "required": true},
    {"id": "4DP-GATE-DES", "name": "description_gate", "check": "cổng Description phủ sản phẩm/quy trình/vai", "regex": "sản phẩm[\\s\\S]{0,200}quy trình[\\s\\S]{0,200}vai", "required": true},
    {"id": "4DP-EXP", "name": "reminds_open_experiment", "check": "nhắc lại thí nghiệm đang mở", "regex": "thí nghiệm đang mở|OPEN", "required": true},
    {"id": "4DP-NOWRITE", "name": "writes_nothing", "check": "preflight không ghi vào sổ", "regex": "[Kk]hông ghi", "required": true},
    {"id": "4DP-OUTPUT", "name": "returns_brief", "check": "trả về phiếu giao việc đã viết lại", "regex": "phiếu giao việc", "required": true}
  ]
}
```

- [ ] **Step 2: Tạo junction rồi chạy eval để xác nhận fail**

```powershell
New-Item -ItemType Junction -Path "C:\Users\Admin\.claude\commands\fluency-4d-preflight" -Target "D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-preflight"
```

Run: `bash evals/run-eval.sh fluency-4d-preflight`
Expected: `ERROR: Skill file not found for: fluency-4d-preflight`.

- [ ] **Step 3: Viết `fluency-4d-preflight/SKILL.md`**

```markdown
---
name: fluency-4d-preflight
description: Cổng kiểm trước khi giao một việc lớn cho AI — ép qua cổng Delegation (việc này Core hay Offload, chạy chế độ nào, giữ lại phần nào) và cổng Description (tiêu chí xong, quy trình, vai AI), rồi trả về phiếu giao việc đã viết lại. Triggers on "4d preflight", "preflight", "trước khi giao việc", "chuẩn bị giao task", "kiểm trước khi giao", "giao việc này cho AI thế nào".
---

# /fluency-4d-preflight — Cổng trước khi giao việc

**COD:** Core (CEO quyết C/O/D) · Offload (AI viết lại phiếu giao việc)

Đọc: `../_shared/references/rubric-core.md`, `../_shared/references/profile-workshop-x.md`.
Thí nghiệm: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\experiments.md`

**Không ghi gì vào sổ điểm.** Đây là cổng, không phải phép đo.

## Bước 0 — Nhắc thí nghiệm đang mở

Đọc `experiments.md`, tìm dòng trạng thái `OPEN`. In lại đúng một dòng câu nếu–thì đó để CEO giữ trong đầu suốt phiên sắp tới. Không có dòng `OPEN` → nói "chưa có thí nghiệm nào đang chạy" rồi đi tiếp.

## Cổng 1 — Delegation

Hỏi và chốt, không đoán hộ:

1. **Việc này là Core / Offload / Default?** (COD). Core = phán đoán thiết kế, quyết định gate, chọn phương án, nhập dữ liệu vật lý thật.
2. **Chế độ nào?** `automation` (AI thực thi tác vụ cụ thể) · `augmentation` (cùng nghĩ cùng làm) · `agency` (AI chạy độc lập, CEO định hình tri thức và hành vi).
3. **Giữ lại phần nào cho mình?** Nêu đích danh phần không giao.

**Nếu CEO phân loại là Core mà vẫn định giao trọn cho AI → chặn.** Nói rõ vì sao đó là Core, đề xuất tách: phần phán đoán giữ lại, phần chuẩn bị dữ liệu giao đi. Chỉ đi tiếp khi CEO hoặc đổi phân loại, hoặc đồng ý tách.

## Cổng 2 — Description

Ba câu, thiếu câu nào thì hỏi:

1. **Sản phẩm** — đầu ra là gì, định dạng nào, ai đọc, tiêu chí "xong" đo được là gì?
2. **Quy trình** — theo khung nào (3-Gate, VDI 2225, ODI, Pahl-Beitz phase nào), hay để AI tự chọn cách?
3. **Vai** — AI phản biện hay thừa hành, gọn hay chi tiết, được phép hỏi lại bao nhiêu?

## Đầu ra — phiếu giao việc

```
## Phiếu giao việc
- Phân loại: <C/O/D> · Chế độ: <mode>
- Giữ lại: <phần CEO tự làm>
- Thí nghiệm đang chạy: <câu nếu–thì hoặc "chưa có">

### Prompt đã viết lại
<đoạn văn giao việc hoàn chỉnh, dán được ngay, đủ sản phẩm + quy trình + vai>
```
```

- [ ] **Step 4: Chạy eval để xác nhận pass**

Run: `bash evals/run-eval.sh fluency-4d-preflight`
Expected: `Score: 7/7 (100%)`.

- [ ] **Step 5: Commit**

```bash
git add plugins/fluency-4d/skills/fluency-4d-preflight/SKILL.md evals/fluency-4d-preflight.json
git commit -m "[LEARN] fluency-4d: cổng preflight Delegation+Description + eval 7/7"
```

---

### Task 7: `fluency-4d-weekly/SKILL.md` + eval tĩnh

**Files:**
- Create: `plugins/fluency-4d/skills/fluency-4d-weekly/SKILL.md`
- Create: `evals/fluency-4d-weekly.json`
- Test: `bash evals/run-eval.sh fluency-4d-weekly`

**Interfaces:**
- Consumes: `sessions.jsonl`, `experiments.md`
- Produces: SKILL.md có cửa sổ 7 ngày, chốt dữ liệu mỏng (< 3 phiên), chọn 1 D ưu tiên, ghi `weekly/<năm>-W<tuần>.md`

- [ ] **Step 1: Viết eval trước**

Tạo `evals/fluency-4d-weekly.json`:

```json
{
  "skill": "fluency-4d-weekly",
  "version": "1.0",
  "description": "Binary assertions cho tổng hợp tuần 4D",
  "mode": "static",
  "total_required": 7,
  "passing_score": 7,
  "assertions": [
    {"id": "4DW-WINDOW", "name": "seven_day_window", "check": "cửa sổ 7 ngày và so với cửa sổ liền trước", "regex": "7 ngày", "required": true},
    {"id": "4DW-NULLSKIP", "name": "null_excluded_from_mean", "check": "tính trung bình bỏ qua null", "regex": "bỏ qua `?null`?|không tính `?null`?", "required": true},
    {"id": "4DW-THIN", "name": "thin_data_gate", "check": "dưới 3 phiên thì không kết luận xu hướng", "regex": "dữ liệu mỏng", "required": true},
    {"id": "4DW-PERSIST", "name": "persistent_weak_cell", "check": "phát hiện ô yếu dai dẳng từ 2 tuần trở lên", "regex": "≥ ?2 tuần|2 tuần liên tiếp", "required": true},
    {"id": "4DW-ONE-D", "name": "one_priority_d", "check": "chốt đúng 1 D ưu tiên cho tuần tới", "regex": "1 D ưu tiên|một D ưu tiên", "required": true},
    {"id": "4DW-STREAK", "name": "experiment_status", "check": "báo cáo tình trạng streak thí nghiệm", "regex": "streak", "required": true},
    {"id": "4DW-FILE", "name": "writes_weekly_file", "check": "ghi ra weekly/<năm>-W<tuần>.md", "regex": "weekly/", "required": true}
  ]
}
```

- [ ] **Step 2: Tạo junction rồi chạy eval để xác nhận fail**

```powershell
New-Item -ItemType Junction -Path "C:\Users\Admin\.claude\commands\fluency-4d-weekly" -Target "D:\KN-Stack\plugins\fluency-4d\skills\fluency-4d-weekly"
```

Run: `bash evals/run-eval.sh fluency-4d-weekly`
Expected: `ERROR: Skill file not found for: fluency-4d-weekly`.

- [ ] **Step 3: Viết `fluency-4d-weekly/SKILL.md`**

```markdown
---
name: fluency-4d-weekly
description: Tổng hợp sổ điểm AI Fluency 4D theo tuần — trung bình từng ô trong cửa sổ 7 ngày, so với tuần trước, phát hiện ô yếu dai dẳng, báo tình trạng thí nghiệm, chốt một D ưu tiên cho tuần tới. Triggers on "4d weekly", "tổng hợp tuần 4d", "xu hướng fluency", "tuần này tôi tiến bộ chưa", "báo cáo tuần 4d", "fluency weekly".
---

# /fluency-4d-weekly — Tổng hợp tuần

**COD:** Offload (AI tổng hợp) · Core (CEO chốt D ưu tiên)

Đọc: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\sessions.jsonl` và `experiments.md`.
Ghi: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\weekly/<năm>-W<số tuần ISO>.md`

## Năm bước

**Bước 1 — Lấy cửa sổ.** Đọc `sessions.jsonl`, lọc bản ghi trong 7 ngày gần nhất. Lấy thêm cửa sổ 7 ngày liền trước để so sánh.

**Bước 2 — Chốt dữ liệu mỏng.** Cửa sổ hiện tại có dưới 3 phiên → in thẳng "**dữ liệu mỏng, không kết luận xu hướng**", liệt kê các phiên đã có rồi DỪNG. Không vẽ xu hướng, không chốt D ưu tiên, không đoán. Đây là chốt cứng.

**Bước 3 — Trung bình từng ô.** Với mỗi ô trong 12 ô, tính trung bình các điểm, **bỏ qua `null`** (n/a không phải 0, kéo trung bình xuống là sai). Ghi kèm số lần được chấm — trung bình từ 1 mẫu phải nói rõ là 1 mẫu. So với cửa sổ trước: ↑ / ↓ / =.

**Bước 4 — Ô yếu dai dẳng.** Ô nào trung bình ≤ 1.5 trong ≥ 2 tuần liên tiếp → đánh dấu dai dẳng. Đọc `experiments.md`, báo tình trạng streak của thí nghiệm đang chạy và các thí nghiệm đã đóng trong tuần.

**Bước 5 — Chốt 1 D ưu tiên.** Đúng một D (không phải một ô) cho tuần tới, kèm lý do bằng số. Ghi file `weekly/<năm>-W<tuần>.md`.

## Khuôn báo cáo

```
# Tuần <năm>-W<tuần> — AI Fluency 4D
Số phiên: <n> · Chế độ hay dùng: <mode>

## Trung bình từng ô
| Ô | TB tuần này (n mẫu) | Tuần trước | Xu hướng |
|---|---|---|---|
… đủ 12 dòng, ô không có mẫu ghi "—" …

## Ô yếu dai dẳng
<danh sách, kèm số tuần liên tiếp>

## Thí nghiệm
<ID đang chạy · streak x/3 · đứt y/3> · <đã PASSED/FAILED trong tuần>

## 1 D ưu tiên tuần tới
<Delegation | Description | Discernment | Diligence> — vì <lý do bằng số>
```
```

- [ ] **Step 4: Chạy eval để xác nhận pass**

Run: `bash evals/run-eval.sh fluency-4d-weekly`
Expected: `Score: 7/7 (100%)`.

- [ ] **Step 5: Commit**

```bash
git add plugins/fluency-4d/skills/fluency-4d-weekly/SKILL.md evals/fluency-4d-weekly.json
git commit -m "[LEARN] fluency-4d: tổng hợp tuần + chốt dữ liệu mỏng + eval 7/7"
```

---

### Task 8: Fixture hội thoại + chạy thật đầu-cuối + README

**Files:**
- Create: `evals/fixtures/fluency-4d-session.md`
- Create: `plugins/fluency-4d/README.md`
- Create: `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\{sessions.jsonl,experiments.md,weekly\}`
- Modify: `scripts/test_fluency_4d.py` (test vòng đời sổ)
- Modify: `CLAUDE.md`, `CHANGELOG.md`, `VERSION`

**Interfaces:**
- Consumes: cả ba SKILL.md, cả bốn file tham chiếu, toàn bộ linter
- Produces: *(task cuối)*

- [ ] **Step 1: Viết fixture hội thoại cài sẵn 3 lỗi**

Tạo `evals/fixtures/fluency-4d-session.md` — một hội thoại người–AI mô phỏng, cài đúng ba lỗi biết trước:

```markdown
# Fixture — phiên có lỗi biết trước

Dùng để kiểm `fluency-4d-review` có bắt đúng lỗi không. Kỳ vọng:
`des.product` ≤ 1 · `dis.product` ≤ 1 · `dil.creation` = 0 (CỜ ĐỎ).

---

**CEO:** Làm cho anh cái báo cáo về vật liệu mặt bia đi.

**AI:** Anh muốn báo cáo dạng nào, cho ai đọc, dài bao nhiêu ạ?

**CEO:** Cứ làm đi, xong rồi tính.

**AI:** [soạn báo cáo 3 trang so sánh SS400 và thép không gỉ 316]
Khối lượng riêng SS400 khoảng 7850 kg/m³, giới hạn chảy khoảng 245 MPa.
Chi phí gia công ước tính cao hơn 316 khoảng 40%.

**CEO:** Ok đưa vào hồ sơ luôn.

**CEO:** À tiện thể, bên Công ty Thép Đông Á báo giá 32.500 đ/kg cho lô
SS400 dày 2mm, còn Hòa Phát báo 29.800 đ/kg. Em tính giúp anh phương án rẻ nhất.

**AI:** [tính toán dựa trên hai mức giá vừa nhận]
```

Ba lỗi cài sẵn: (1) từ chối nêu định dạng/người đọc/tiêu chí xong → `des.product`; (2) nhận số 245 MPa và "cao hơn 40%" rồi đưa thẳng vào hồ sơ không hỏi nguồn → `dis.product`; (3) dán giá nhà cung cấp đích danh vào prompt → `dil.creation` = 0, cờ đỏ.

- [ ] **Step 2: Chạy `fluency-4d-review` thật lên fixture**

```bash
cd /d/KN-Stack
cat evals/fixtures/fluency-4d-session.md | claude -p "Đây là toàn bộ nội dung một phiên làm việc. Áp dụng skill fluency-4d-review lên phiên này. In báo cáo, KHÔNG ghi file." --permission-mode plan --output-format text
```

Kiểm bằng mắt, phải thấy đủ ba điều:
- `des.product` chấm ≤ 1 kèm trích dẫn "Cứ làm đi, xong rồi tính"
- `dis.product` chấm ≤ 1 kèm trích dẫn "Ok đưa vào hồ sơ luôn"
- **CỜ ĐỎ** `dil.creation` = 0 nằm ở ĐẦU báo cáo, nhắc giá nhà cung cấp

Không đạt cả ba → quay lại Task 5 sửa `SKILL.md` (thường là phần tín hiệu trong `profile-workshop-x.md` chưa đủ cụ thể), rồi chạy lại. Đây là cổng thật, không bỏ qua được.

- [ ] **Step 3: Viết test vòng đời sổ**

Thêm vào `scripts/test_fluency_4d.py`:

```python
def test_ledger_lifecycle_four_sessions():
    """Bốn phiên liên tiếp: streak 1→2→3→PASSED, mọi dòng sổ hợp lệ."""
    sample = lint.extract_sample_record(LEDGER_DOC)
    exp = {"id": "EXP-001", "cell": "des.product",
           "if_then": "Khi giao task > 30 phút, tôi nêu tiêu chí xong trước khi bấm gửi.",
           "streak": 0, "breaks": 0, "status": "OPEN", "opened": "2026-08-01", "closed": ""}
    streaks = []
    for day, held in enumerate([True, True, True, True], start=1):
        rec = dict(sample)
        rec["id"] = f"2026-08-0{day}-1"
        rec["date"] = f"2026-08-0{day}"
        rec["exp_active"] = exp["id"]
        rec["exp_held"] = held
        assert lint.validate_ledger_line(rec) == [], rec["id"]
        if exp["status"] == "OPEN":
            exp = lint.apply_session(exp, held=held)
        streaks.append((exp["streak"], exp["status"]))
    assert streaks == [(1, "OPEN"), (2, "OPEN"), (3, "PASSED"), (3, "PASSED")]
```

- [ ] **Step 4: Chạy toàn bộ test**

Run: `cd /d/KN-Stack && python -m pytest scripts/test_fluency_4d.py -v`
Expected: PASS 30/30.

- [ ] **Step 5: Tạo thư mục sổ trong vault**

```powershell
New-Item -ItemType Directory -Force -Path "D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\weekly"
```

Tạo `sessions.jsonl` rỗng và `experiments.md` chỉ có dòng tiêu đề bảng (8 cột như `experiment-protocol.md`). Ghi UTF-8 không BOM.

- [ ] **Step 6: Viết `plugins/fluency-4d/README.md`**

Nội dung bắt buộc có:
- Plugin làm gì, ba lối vào và khi nào dùng cái nào
- **Import vào Cowork:** copy nguyên thư mục `plugins/fluency-4d/` vào thư mục plugin của Cowork, hoặc trỏ marketplace tới repo này; xác nhận ba skill xuất hiện
- **Quyền cần cấp:** đọc/ghi `D:\Workshop_X\2_Areas\CEO-Self\AI-Fluency-Ledger\` — không có quyền này thì `review` và `weekly` không chạy được
- **Dùng trong Claude Code:** ba lệnh junction ở Task 5–7
- **Đổi profile:** chép `profile-workshop-x.md` → `profile-<tên>.md`, giữ khung `## <mã ô>` + ba trường, đổi dòng trỏ trong ba SKILL.md
- **Bảo trì:** `python -m pytest scripts/test_fluency_4d.py` sau mỗi lần sửa file tham chiếu
- Ghi nhận bản quyền khung gốc: Dakan, Feller, Anthropic — CC BY-NC-SA 4.0

- [ ] **Step 7: Cập nhật sổ sách repo**

- `CLAUDE.md`: thêm `plugins/fluency-4d/` vào cây thư mục với mô tả một dòng.
- `CHANGELOG.md`: mục mới cho phiên bản kế tiếp — "Thêm plugin `fluency-4d`: huấn luyện viên AI Fluency 4D (3 skill, 4 file tham chiếu, 3 eval tĩnh, linter + 30 test)".
- `VERSION`: bump minor.

- [ ] **Step 8: Chạy lại toàn bộ cổng**

```bash
cd /d/KN-Stack
python -m pytest scripts/test_fluency_4d.py -v
bash evals/run-eval.sh fluency-4d-review
bash evals/run-eval.sh fluency-4d-preflight
bash evals/run-eval.sh fluency-4d-weekly
```
Expected: 30/30 pytest · 10/10 · 7/7 · 7/7.

- [ ] **Step 9: Commit**

```bash
git add evals/fixtures/fluency-4d-session.md plugins/fluency-4d/README.md \
        scripts/test_fluency_4d.py CLAUDE.md CHANGELOG.md VERSION
git commit -m "[LEARN] fluency-4d: fixture kiểm hành vi, README import Cowork, sổ sách repo"
```

---

## Kiểm sau khi xong

| Yêu cầu spec | Task |
|---|---|
| §3 kiến trúc 3 skill + 4 tham chiếu | 1, 2, 3, 4, 5, 6, 7 |
| §3 rubric trung lập / profile không định nghĩa lại thang | 1 (`lint_rubric`), 2 (`lint_profile`) |
| §4 12 ô + 3 chế độ + thang 0–3/null | 1 |
| §4 ba chốt chống nịnh | 1 (rubric), 5 (SKILL + eval) |
| §5 profile 12 khối × 3 trường | 2 |
| §6 schema JSONL + đường dẫn sổ | 3, 8 |
| §7 WIP=1, nếu–thì, streak 3, đứt 3 | 4 |
| §8.1 preflight hai cổng | 6 |
| §8.2 review 6 bước + ngoại lệ cờ đỏ | 5 |
| §8.3 weekly + chốt dữ liệu mỏng | 7 |
| §9 eval tĩnh · fixture · vòng đời sổ · README | 5, 6, 7, 8 |
