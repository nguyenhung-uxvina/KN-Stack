# ip-invent Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Đóng gói 6 skill IP (`ip-invent` + 5 block) thành plugin `plugins/ip-invent/` tự chứa, chạy được cả trong Claude Code (qua junction) lẫn Cowork (cây plugin nguyên vẹn), với cổng phân loại bí mật nhà nước thay cho lệnh cấm cloud chung chung.

**Architecture:** Dời hẳn `skills/ip/*` sang `plugins/ip-invent/skills/` — một nguồn chuẩn duy nhất, không `build.sh`, không bản sao. Một thư mục tham chiếu dùng chung `ip-shared/references/` mang tầng trỏ workspace (đổi môi trường = sửa một dòng) và thủ tục cổng phân loại. Sáu `SKILL.md` chỉ trỏ tới tầng trỏ bằng đường dẫn tương đối `../ip-shared/references/…`, không file nào biết tên vault. Lint + test nằm NGOÀI plugin ở `scripts/` để plugin thuần Markdown + JSON.

**Tech Stack:** Markdown + JSON (plugin) · Python 3 + pytest (lint/test, ngoài plugin) · Bash (`setup.sh`, `evals/run-eval.sh`) · Windows junction qua PowerShell.

## Global Constraints

- Plugin **thuần Markdown + JSON**. Không Python, không hook, không MCP bên trong `plugins/ip-invent/`.
- Thư mục tham chiếu dùng chung tên **`ip-shared`** — KHÔNG dùng `_shared`/`common`/`refs`. `~/.claude/commands/` là namespace phẳng dùng chung mọi plugin; tên chung chung sẽ đụng nhau.
- Sáu `SKILL.md` trỏ tầng trỏ bằng **đường dẫn tương đối `../ip-shared/references/…`** — đúng chuỗi này resolve được ở cả hai kiểu triển khai (junction rời + cây plugin nguyên vẹn). Không `SKILL.md` nào được sửa theo môi trường.
- **Không đổi logic 5 block**, không đụng nội dung pháp lý, không sửa bảng đối chiếu QĐ 431 ↔ QĐ 12/2025.
- **Không gỡ chữ "CEO"** khỏi `SKILL.md` — plugin dùng cho chính CEO, không phát cho tổ chức khác.
- Allowlist đường dẫn được phép giữ nguyên trong `SKILL.md`: **`_meta/decisions.md`** và **`_meta/learnings.md`** (tương đối trong dự án, resolve từ `output_pattern`). Không nới thêm mục nào.
- Bảy trường workspace, đúng tên, đúng thứ tự: `surface` · `root` · `output_pattern` · `scan_sources` · `triz_refs` · `patent_search` · `nlm_notebook`.
- Khi một trường = `none`, block liên quan chạy **chế độ giảm và phải in dòng khai báo**. Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ.
- Commit format `[IP] <mô tả>`, kết thúc bằng `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- Không commit thẳng vào `main`. Làm trên nhánh hiện tại `feature/ip-patent-pipeline`.

## File Structure

| File | Trách nhiệm |
|---|---|
| `plugins/ip-invent/.claude-plugin/plugin.json` | Manifest plugin (name/description/version/author) |
| `plugins/ip-invent/README.md` | Import Cowork · quyền cần cấp · junction Claude Code · đổi workspace · bảo trì |
| `plugins/ip-invent/skills/ip-invent/SKILL.md` | Orchestrator (git mv) |
| `plugins/ip-invent/skills/ip-criteria/SKILL.md` | B0 thước đo chức danh (git mv) |
| `plugins/ip-invent/skills/ip-harvest/SKILL.md` | B1 tìm ứng viên (git mv) |
| `plugins/ip-invent/skills/ip-screen/SKILL.md` | B2 rà hai trục + routing (git mv) |
| `plugins/ip-invent/skills/ip-claim/SKILL.md` | B3 khung claim (git mv) |
| `plugins/ip-invent/skills/ip-dossier/SKILL.md` | B4 bộ đơn + handoff (git mv) |
| `plugins/ip-invent/skills/ip-shared/references/active-workspace.md` | Tầng trỏ — nêu tên profile đang bật, một dòng |
| `plugins/ip-invent/skills/ip-shared/references/workspace-knstack.md` | Profile local: vault Workshop X |
| `plugins/ip-invent/skills/ip-shared/references/workspace-cowork.md` | Profile cloud: Cowork |
| `plugins/ip-invent/skills/ip-shared/references/workspace-template.md` | Khuôn rỗng, không bao giờ bật |
| `plugins/ip-invent/skills/ip-shared/references/co-mat-gate.md` | Thủ tục cổng phân loại khi `surface: cloud` |
| `plugins/ip-invent/templates/_pipeline_state.md` | Khuôn ledger — plugin không tự dựng sổ |
| `scripts/ip_invent_lint.py` | Hàm lint thuần (parse tầng trỏ, 7 trường, chốt, đường dẫn) |
| `scripts/test_ip_invent.py` | pytest cho linter + khớp-chéo file thật |
| `setup.sh` | Lấy bản plugin-aware từ `feature/fluency-4d-plugin` |
| `evals/ip-invent.json` | v1.2 — thêm assertion cổng phân loại + tầng trỏ |
| `CLAUDE.md`, `VERSION`, `CHANGELOG.md` | Cập nhật bản đồ và phiên bản |

**Không sửa** `evals/run-eval.sh`: nó resolve skill qua `$HOME/.claude/commands/<name>/SKILL.md`, tức là qua junction. Junction đúng thì eval chạy nguyên như cũ. Đây là điểm phải xác nhận ở Task 1 chứ không giả định.

---

### Task 1: Dựng khung plugin, dời 6 skill, junction chạy được

**Files:**
- Create: `plugins/ip-invent/.claude-plugin/plugin.json`
- Move: `skills/ip/{ip-invent,ip-criteria,ip-harvest,ip-screen,ip-claim,ip-dossier}/` → `plugins/ip-invent/skills/`
- Modify: `setup.sh` (thay bằng bản plugin-aware từ nhánh `feature/fluency-4d-plugin`)

**Interfaces:**
- Consumes: không có (task đầu)
- Produces: 7 junction dưới `~/.claude/commands/` — `ip-invent`, `ip-criteria`, `ip-harvest`, `ip-screen`, `ip-claim`, `ip-dossier`, `ip-shared`. Mọi task sau dựa vào đường dẫn `plugins/ip-invent/skills/<name>/SKILL.md`.

- [ ] **Bước 1: Xác nhận diff `setup.sh` vẫn là phép cộng sạch**

```bash
cd /d/KN-Stack
git diff --stat HEAD feature/fluency-4d-plugin -- setup.sh
```

Kỳ vọng: `1 file changed, 119 insertions(+)` — **0 dòng xoá**. Nếu thấy có dòng xoá (`-`), DỪNG và báo: nhánh fluency đã đổi khác, phải port tay từng hunk thay vì lấy nguyên file.

- [ ] **Bước 2: Lấy `setup.sh` plugin-aware, ghi lại commit nguồn**

```bash
git checkout feature/fluency-4d-plugin -- setup.sh
git rev-parse --short feature/fluency-4d-plugin   # ghi lại hash này cho CHANGELOG ở Task 8
grep -c "plugin_skill_dirs" setup.sh              # kỳ vọng: >= 4
```

- [ ] **Bước 3: Dời 6 thư mục skill**

```bash
mkdir -p plugins/ip-invent/.claude-plugin plugins/ip-invent/skills plugins/ip-invent/templates
for s in ip-invent ip-criteria ip-harvest ip-screen ip-claim ip-dossier; do
  git mv "skills/ip/$s" "plugins/ip-invent/skills/$s"
done
rmdir skills/ip
ls plugins/ip-invent/skills/     # kỳ vọng: 6 thư mục
```

- [ ] **Bước 4: Viết manifest**

Tạo `plugins/ip-invent/.claude-plugin/plugin.json`:

```json
{
  "name": "ip-invent",
  "description": "Pipeline sở hữu trí tuệ TẤN CÔNG — từ ý tưởng đến bộ đơn nộp Cục SHTT, sáu skill: ip-invent orchestrator chỉ huy ip-criteria (thước đo chức danh) → ip-harvest (tìm ứng viên) → ip-screen (rà hai trục + routing sáng chế/GPHI/nộp kép/MẬT) → ip-claim (khung claim) → ip-dossier (bộ đơn + handoff đại diện SHTT). Advisory-only, không thay đại diện sở hữu công nghiệp. Có cổng bộc lộ, cổng phân loại bí mật nhà nước, cổng Điều 14 nộp nước ngoài, cổng Điều 10a tác giả-AI.",
  "version": "0.1.0",
  "author": {
    "name": "Workshop X"
  }
}
```

- [ ] **Bước 5: Tạo thư mục shared rỗng để `setup.sh` có cái mà junction**

`setup.sh --install` chỉ junction các thư mục **đã tồn tại** dưới `plugins/*/skills/`. Nội dung thật viết ở Task 2; bây giờ chỉ cần thư mục có mặt.

```bash
mkdir -p plugins/ip-invent/skills/ip-shared/references
printf '# placeholder — nội dung viết ở Task 2\n' > plugins/ip-invent/skills/ip-shared/references/.keep.md
```

- [ ] **Bước 6: Dựng junction và kiểm**

```bash
bash setup.sh --install
bash setup.sh --verify
```

Kỳ vọng: `--verify` báo plugin skill dirs đều xanh, trong đó có `ip-shared`. Nếu `ip-shared` không xuất hiện → DỪNG, kiểm lại `plugin_skill_dirs()` trong `setup.sh` có bắt thư mục không mang `SKILL.md` hay không.

- [ ] **Bước 7: Xác nhận eval runner vẫn tìm được skill sau khi dời**

```bash
bash evals/run-eval.sh ip-invent
bash evals/run-eval.sh ip-screen
```

Kỳ vọng: cả hai PASS đúng như trước khi dời (ip-invent 14/14 required, ip-screen 13/13 required). `run-eval.sh` resolve qua `$HOME/.claude/commands/<name>/SKILL.md` nên junction đúng là đủ — **không sửa `run-eval.sh`**. Nếu báo `Skill file not found` → junction chưa dựng, quay lại Bước 6.

- [ ] **Bước 8: Commit**

```bash
git add -A plugins/ skills/ setup.sh
git commit -m "$(cat <<'EOF'
[IP] Dời skills/ip -> plugins/ip-invent, setup.sh biết junction plugin

Dời hẳn 6 skill IP thành plugin tự chứa: một nguồn chuẩn duy nhất, không
build.sh, không bản sao song song. setup.sh lấy từ feature/fluency-4d-plugin
(diff là 119 dòng thêm thuần, 0 dòng xoá) để biết đi vào plugins/*/skills/
và junction cả thư mục tham chiếu dùng chung.

evals/run-eval.sh không phải sửa: nó resolve skill qua junction.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Tầng trỏ workspace + linter đọc được nó

**Files:**
- Create: `scripts/ip_invent_lint.py`
- Create: `scripts/test_ip_invent.py`
- Create: `plugins/ip-invent/skills/ip-shared/references/active-workspace.md`
- Create: `plugins/ip-invent/skills/ip-shared/references/workspace-knstack.md`
- Create: `plugins/ip-invent/skills/ip-shared/references/workspace-cowork.md`
- Create: `plugins/ip-invent/skills/ip-shared/references/workspace-template.md`
- Delete: `plugins/ip-invent/skills/ip-shared/references/.keep.md`

**Interfaces:**
- Consumes: cây thư mục từ Task 1.
- Produces:
  - `ip_invent_lint.REPO_ROOT: Path`, `PLUGIN_ROOT: Path`, `SKILLS_ROOT: Path`, `REF_DIR: Path`
  - `ip_invent_lint.SHARED_DIR_NAME: str = "ip-shared"`
  - `ip_invent_lint.SKILL_NAMES: list[str]` — 6 tên skill
  - `ip_invent_lint.WORKSPACE_FIELDS: list[str]` — 7 trường đúng thứ tự
  - `ip_invent_lint.parse_active_workspace(text: str) -> str | None` — trả tên file profile trong khối mã, `None` nếu không có
  - `ip_invent_lint.parse_workspace_profile(text: str) -> dict[str, str]` — bảng `| \`trường\` | giá trị |` → dict
  - `ip_invent_lint.lint_workspace_profile(text: str) -> list[str]` — danh sách lỗi, rỗng = đạt

- [ ] **Bước 1: Viết test cho `parse_active_workspace` (chưa có module → phải fail)**

Tạo `scripts/test_ip_invent.py`:

```python
"""pytest cho linter plugin ip-invent."""
import importlib.util
import sys
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "ip_invent_lint", Path(__file__).with_name("ip_invent_lint.py")
)
lint = importlib.util.module_from_spec(_spec)
sys.modules["ip_invent_lint"] = lint
_spec.loader.exec_module(lint)


def test_shared_dir_carries_plugin_prefix():
    # ~/.claude/commands/ là namespace phẳng dùng chung mọi plugin.
    assert lint.SHARED_DIR_NAME == "ip-shared"


def test_workspace_fields_are_the_canonical_seven():
    assert lint.WORKSPACE_FIELDS == [
        "surface", "root", "output_pattern",
        "scan_sources", "triz_refs", "patent_search", "nlm_notebook",
    ]


def test_parse_active_workspace_reads_the_code_block():
    text = "# Workspace đang bật\n\nblah\n\n```\nworkspace-knstack.md\n```\n\nblah\n"
    assert lint.parse_active_workspace(text) == "workspace-knstack.md"


def test_parse_active_workspace_returns_none_when_absent():
    assert lint.parse_active_workspace("# Không có khối mã nào\n") is None
```

- [ ] **Bước 2: Chạy để chắc là fail**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: lỗi khi nạp module — `FileNotFoundError` hoặc `ModuleNotFoundError` cho `ip_invent_lint.py`.

- [ ] **Bước 3: Viết `scripts/ip_invent_lint.py` phần tầng trỏ**

```python
"""Linter giữ tầng tham chiếu dùng chung của plugin ip-invent khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown + JSON để Cowork nạp được).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "ip-invent"
SKILLS_ROOT = PLUGIN_ROOT / "skills"

# Tên thư mục tham chiếu dùng chung. Phải mang tiền tố plugin: nó được junction
# THẲNG vào ~/.claude/commands/ — một namespace phẳng dùng chung cho mọi plugin.
# Tên chung như "_shared" sẽ bị plugin nạp sau va vào và setup.sh bỏ qua im lặng.
SHARED_DIR_NAME = "ip-shared"
REF_DIR = SKILLS_ROOT / SHARED_DIR_NAME / "references"

SKILL_NAMES = [
    "ip-invent", "ip-criteria", "ip-harvest",
    "ip-screen", "ip-claim", "ip-dossier",
]

WORKSPACE_FIELDS = [
    "surface", "root", "output_pattern",
    "scan_sources", "triz_refs", "patent_search", "nlm_notebook",
]

VALID_SURFACES = {"local", "cloud"}

_CODE_BLOCK_RE = re.compile(r"^```\s*$\n(.*?)^```\s*$", re.MULTILINE | re.DOTALL)
_PROFILE_ROW_RE = re.compile(r"^\|\s*`([a-z_]+)`\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)


def parse_active_workspace(text: str) -> str | None:
    """Tên file profile nêu trong khối mã đầu tiên của active-workspace.md."""
    m = _CODE_BLOCK_RE.search(text)
    if not m:
        return None
    name = m.group(1).strip()
    return name or None


def parse_workspace_profile(text: str) -> dict[str, str]:
    """Bảng `| `trường` | giá trị |` của một file workspace-*.md → dict."""
    return {k: v.strip("` ") for k, v in _PROFILE_ROW_RE.findall(text)}


def lint_workspace_profile(text: str) -> list[str]:
    """Kiểm một file workspace-*.md. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    found = list(parse_workspace_profile(text).keys())
    if found != WORKSPACE_FIELDS:
        missing = [f for f in WORKSPACE_FIELDS if f not in found]
        extra = [f for f in found if f not in WORKSPACE_FIELDS]
        if missing:
            errors.append(f"profile thiếu trường: {missing}")
        if extra:
            errors.append(f"profile có trường lạ: {extra}")
        if not missing and not extra:
            errors.append(f"profile sai thứ tự trường: {found}")
    surface = parse_workspace_profile(text).get("surface")
    if surface is not None and surface not in VALID_SURFACES:
        errors.append(f"surface phải là local|cloud, thấy: {surface!r}")
    return errors
```

- [ ] **Bước 4: Chạy test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: 4 PASS.

- [ ] **Bước 5: Viết test cho ba file workspace thật (chưa có file → phải fail)**

Thêm vào cuối `scripts/test_ip_invent.py`:

```python
def _ref(name: str) -> str:
    return (lint.REF_DIR / name).read_text(encoding="utf-8")


def test_active_workspace_points_at_an_existing_profile():
    target = lint.parse_active_workspace(_ref("active-workspace.md"))
    assert target is not None, "active-workspace.md không có khối mã nêu profile"
    assert (lint.REF_DIR / target).is_file(), f"trỏ tới profile không tồn tại: {target}"


def test_knstack_profile_is_local_and_complete():
    text = _ref("workspace-knstack.md")
    assert lint.lint_workspace_profile(text) == []
    assert lint.parse_workspace_profile(text)["surface"] == "local"


def test_cowork_profile_is_cloud_and_declares_none_for_vault_only_tools():
    text = _ref("workspace-cowork.md")
    assert lint.lint_workspace_profile(text) == []
    fields = lint.parse_workspace_profile(text)
    assert fields["surface"] == "cloud"
    # Cowork không có vault, không có skill KN-Stack, không có NLM.
    for f in ("scan_sources", "triz_refs", "patent_search", "nlm_notebook"):
        assert fields[f] == "none", f"{f} phải là none trong profile Cowork"


def test_template_profile_is_complete_but_never_activated():
    text = _ref("workspace-template.md")
    # Template chỉ cần đủ + đúng thứ tự 7 trường; `surface` là chỗ trống ⟨CEO chốt: …⟩
    # nên không kiểm giá trị surface ở đây.
    assert list(lint.parse_workspace_profile(text).keys()) == lint.WORKSPACE_FIELDS
    assert lint.parse_active_workspace(_ref("active-workspace.md")) != "workspace-template.md"


def test_profile_lint_flags_a_missing_field():
    dirty = "| `surface` | `local` |\n| `root` | `X` |\n"
    assert any("thiếu trường" in e for e in lint.lint_workspace_profile(dirty))


def test_profile_lint_flags_bad_surface():
    rows = "\n".join(
        f"| `{f}` | `{'hybrid' if f == 'surface' else 'x'}` |" for f in lint.WORKSPACE_FIELDS
    )
    assert any("surface phải là local|cloud" in e for e in lint.lint_workspace_profile(rows))
```

- [ ] **Bước 6: Chạy, phải fail vì chưa có file**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: 4 test cũ PASS, các test mới FAIL với `FileNotFoundError`.

- [ ] **Bước 7: Viết `active-workspace.md`**

````markdown
# Workspace đang bật

Sáu `SKILL.md` của plugin đọc **file này TRƯỚC**, rồi mới mở file profile nêu bên dưới.
**Không `SKILL.md` nào được gọi tên file profile trực tiếp** — đổi môi trường phải là sửa một
dòng ở đây, không phải sửa sáu file.

```
workspace-knstack.md
```

Profile có sẵn trong cùng thư mục:

| File | Môi trường | `surface` |
|---|---|---|
| `workspace-knstack.md` | Claude Code trên máy có KN-Stack + vault Workshop X | `local` |
| `workspace-cowork.md` | Claude Cowork | `cloud` |
| `workspace-template.md` | Khuôn rỗng cho môi trường thứ ba — **không bao giờ được bật** | — |
````

- [ ] **Bước 8: Viết `workspace-knstack.md`**

```markdown
# Workspace — KN-Stack / vault Workshop X

Bề mặt local trên máy CEO. Cổng phân loại KHÔNG kích hoạt ở profile này.

| Trường | Giá trị |
|---|---|
| `surface` | `local` |
| `root` | `D:\Workshop_X\` |
| `output_pattern` | `<root>\1_Projects\<project>\IP\` |
| `scan_sources` | `1_Projects/*/` (_Project_Brief.md, Status.md, Patent_Draft_*.md) · `2_Areas/HELIX*/` + design journal · RE report (reverse-engineering, reverse-mc) · `_meta/decisions.md` · FTO Record QP-02-06 |
| `triz_refs` | `D:\KN-Stack\skills\helix\helix-concept-generate\references\` (triz-40-principles.md, triz-sufield-76solutions.md) |
| `patent_search` | `/research --patents` |
| `nlm_notebook` | `ip-vn` |
```

- [ ] **Bước 9: Viết `workspace-cowork.md`**

```markdown
# Workspace — Claude Cowork

Bề mặt **cloud**. Cổng phân loại trong `co-mat-gate.md` KÍCH HOẠT ở profile này.

Cowork không có vault Workshop X, không có skill KN-Stack, không có NotebookLM — nên bốn trường
công cụ đều `none`. Block nào cần chúng phải chạy **chế độ giảm và in dòng khai báo**.

| Trường | Giá trị |
|---|---|
| `surface` | `cloud` |
| `root` | thư mục làm việc của phiên Cowork |
| `output_pattern` | `<root>/IP/<project>/` |
| `scan_sources` | `none` |
| `triz_refs` | `none` |
| `patent_search` | `none` |
| `nlm_notebook` | `none` |
```

- [ ] **Bước 10: Viết `workspace-template.md`**

```markdown
# Workspace — KHUÔN RỖNG (không bao giờ được bật)

Chép file này thành `workspace-<tên môi trường>.md`, điền đủ bảy trường, rồi đổi **đúng một dòng**
trong khối mã của `active-workspace.md`. Không đụng `SKILL.md` nào.

Giữ nguyên khung bảng: bảy hàng, đúng tên trường, đúng thứ tự. Lint kiểm cả ba thứ đó.

| Trường | Giá trị |
|---|---|
| `surface` | `⟨CEO chốt: local hoặc cloud⟩` |
| `root` | `⟨CEO chốt: gốc làm việc⟩` |
| `output_pattern` | `⟨CEO chốt: nơi ghi đầu ra⟩` |
| `scan_sources` | `⟨CEO chốt: nguồn B1-1a quét, hoặc none⟩` |
| `triz_refs` | `⟨CEO chốt: đường dẫn TRIZ, hoặc none⟩` |
| `patent_search` | `⟨CEO chốt: công cụ tra patent, hoặc none⟩` |
| `nlm_notebook` | `⟨CEO chốt: notebook luật công khai, hoặc none⟩` |
```

> `surface` ở template cố ý là chuỗi `⟨CEO chốt: …⟩` chứ không phải `local`/`cloud` — đó là lý do
> `test_template_profile_is_complete_but_never_activated` chỉ kiểm **đủ và đúng thứ tự bảy trường**,
> không gọi `lint_workspace_profile`.

- [ ] **Bước 11: Xoá placeholder, chạy test, phải xanh**

```bash
cd /d/KN-Stack
rm plugins/ip-invent/skills/ip-shared/references/.keep.md
python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: toàn bộ PASS.

- [ ] **Bước 12: Commit**

```bash
git add scripts/ip_invent_lint.py scripts/test_ip_invent.py plugins/ip-invent/skills/ip-shared/
git commit -m "$(cat <<'EOF'
[IP] Tầng trỏ workspace cho plugin ip-invent + linter

Bảy trường (surface/root/output_pattern/scan_sources/triz_refs/
patent_search/nlm_notebook) khai trong workspace-*.md; active-workspace.md
nêu profile đang bật bằng một dòng. Đổi môi trường không đụng SKILL.md nào.

Profile Cowork khai none cho bốn trường công cụ vì Cowork không có vault,
không có skill KN-Stack, không có NLM.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Cổng phân loại `co-mat-gate.md`

**Files:**
- Create: `plugins/ip-invent/skills/ip-shared/references/co-mat-gate.md`
- Modify: `scripts/ip_invent_lint.py` (thêm `lint_gate_doc`)
- Modify: `scripts/test_ip_invent.py`

**Interfaces:**
- Consumes: `lint.REF_DIR` và helper test `_ref(name)` từ Task 2.
- Produces: `ip_invent_lint.GATE_REQUIRED_PHRASES: list[str]` · `ip_invent_lint.lint_gate_doc(text: str) -> list[str]`

- [ ] **Bước 1: Viết test (chưa có hàm + chưa có file → fail)**

Thêm vào `scripts/test_ip_invent.py`:

```python
def test_gate_doc_states_all_three_verdicts_and_ceo_ownership():
    assert lint.lint_gate_doc(_ref("co-mat-gate.md")) == []


def test_gate_doc_lint_flags_missing_unknown_defaults_to_secret():
    dirty = "\n".join(p for p in lint.GATE_REQUIRED_PHRASES if p != "Chưa rõ")
    assert any("Chưa rõ" in e for e in lint.lint_gate_doc(dirty))


def test_gate_doc_lint_flags_dropping_ceo_ownership():
    dirty = "\n".join(
        p for p in lint.GATE_REQUIRED_PHRASES
        if p != "quyết định của CEO, không phải kết luận pháp lý"
    )
    assert any("CEO" in e for e in lint.lint_gate_doc(dirty))
```

- [ ] **Bước 2: Chạy, phải fail**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k gate -v
```

Kỳ vọng: FAIL với `AttributeError: module 'ip_invent_lint' has no attribute 'lint_gate_doc'`.

- [ ] **Bước 3: Thêm `lint_gate_doc` vào `scripts/ip_invent_lint.py`**

```python
# Cụm chữ mà co-mat-gate.md bắt buộc mang. Đây là các mệnh đề quyết định hành vi,
# không phải trang trí: bỏ bất kỳ cụm nào là đổi nghĩa cổng.
GATE_REQUIRED_PHRASES = [
    "bí mật nhà nước",
    "Chưa rõ",
    "coi như thuộc",
    "DỪNG",
    "Claude Code local",
    "Điều 60.2",
    "quyết định của CEO, không phải kết luận pháp lý",
    "kèm căn cứ",
]


def lint_gate_doc(text: str) -> list[str]:
    """Kiểm co-mat-gate.md mang đủ mệnh đề quyết định hành vi."""
    return [
        f"co-mat-gate.md thiếu mệnh đề: {p!r}"
        for p in GATE_REQUIRED_PHRASES
        if p.lower() not in text.lower()
    ]
```

- [ ] **Bước 4: Viết `co-mat-gate.md`**

```markdown
# Cổng phân loại — chạy khi `surface: cloud`

> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.
> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ.

## Vì sao có cổng này

Rào cứng #2 của `ip-invent` từng gộp hai thứ khác hẳn nhau vào một câu cấm. Tách ra:

- **Bí mật nhà nước — bí mật quân sự.** Cấm tuyệt đối đưa ra bất kỳ dịch vụ ngoài nào, không
  ngoại lệ, bất kể có bộc lộ công khai hay không. Đây là cái cổng thật.
- **Chưa bộc lộ nhưng không thuộc bí mật nhà nước.** Điều 60.2 Luật SHTT: bộc lộ cho *"một số
  người có hạn được biết và có nghĩa vụ giữ bí mật"* **không** làm mất tính mới. Dịch vụ có nghĩa
  vụ bảo mật theo hợp đồng rơi vào diện đó.

Việc coi một bề mặt cloud cụ thể là "có nghĩa vụ bảo mật" là **quyết định của CEO, không phải kết
luận pháp lý** của skill này — cùng tinh thần cổng advisory-only đã có trong `ip-invent`.

## Bước 0′ — chạy TRƯỚC khi đụng nội dung ứng viên bất kỳ

Hỏi CEO phân loại từng ứng viên, **kèm căn cứ** (văn bản/quyết định nào nói thế). Không nhận câu
trả lời trống, không suy diễn hộ.

| Phân loại | Xử |
|---|---|
| Thuộc / nghi thuộc **bí mật nhà nước — bí mật quân sự** | **DỪNG.** Không xử nội dung, không tóm tắt, không diễn giải. Chỉ CEO quay về **Claude Code local** (đổi `active-workspace.md` sang `workspace-knstack.md`). |
| **Chưa rõ** — chưa có văn bản xác định | **coi như thuộc** → **DỪNG.** Bám đúng nguyên tắc `ip-dossier` đã có: *"Chưa có văn bản xác định bí mật nhà nước ⇒ coi như CHƯA RÕ"*. Mặc định thận trọng, nên bấm bừa không mở được cổng. |
| **Không thuộc** — dân dụng, hoặc lưỡng dụng đã tách phần MẬT, hoặc đã khóa priority date | Chạy tiếp. |

## Ghi và in lại

- Ghi trạng thái cổng vào ledger `_pipeline_state.md`, mục **Cờ ràng buộc**.
- **Mỗi block in lại ở đầu báo cáo:** `Bề mặt: <surface> · Cổng phân loại: <trạng thái> · Căn cứ: <…>`
  CEO không bao giờ được đọc một đầu ra mà không biết nó chạy trên bề mặt nào.

## Cái cổng này KHÔNG làm

- Không thay cơ quan có thẩm quyền xác định danh mục bí mật nhà nước.
- Không kết luận một giải pháp "an toàn để đưa lên cloud" — nó chỉ chặn, không cấp phép.
- Không thay cổng bộc lộ (Điều 60) và cổng Điều 14 nộp nước ngoài. Ba cổng độc lập, phải qua cả ba.
```

- [ ] **Bước 5: Chạy test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: toàn bộ PASS.

- [ ] **Bước 6: Commit**

```bash
git add plugins/ip-invent/skills/ip-shared/references/co-mat-gate.md scripts/
git commit -m "$(cat <<'EOF'
[IP] Cổng phân loại bí mật nhà nước cho bề mặt cloud

Tách hai thứ rào cứng #2 từng gộp: bí mật nhà nước cấm tuyệt đối ra dịch vụ
ngoài; còn chưa-bộc-lộ-nhưng-không-MẬT thì Điều 60.2 cho phép bộc lộ có
nghĩa vụ bảo mật. Mặc định "chưa rõ" = coi như thuộc = DỪNG, nên bấm bừa
không mở được cổng.

Ghi thẳng rằng đây là quyết định của CEO, không phải kết luận pháp lý của AI.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Chốt Bước 0′ vào cả 6 SKILL.md

**Files:**
- Modify: cả 6 file `plugins/ip-invent/skills/<name>/SKILL.md`
- Modify: `scripts/ip_invent_lint.py` (thêm `lint_skill_header`)
- Modify: `scripts/test_ip_invent.py`

**Interfaces:**
- Consumes: `lint.SKILL_NAMES`, `lint.SKILLS_ROOT`, `lint.SHARED_DIR_NAME` từ Task 2.
- Produces: `ip_invent_lint.SKILL_REQUIRED_PHRASES: list[str]` · `ip_invent_lint.lint_skill_header(text: str) -> list[str]` · `ip_invent_lint.cited_refs(text: str) -> list[str]`

- [ ] **Bước 1: Viết test (fail)**

Thêm vào `scripts/test_ip_invent.py`:

```python
import pytest


def _skill(name: str) -> str:
    return (lint.SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("name", [
    "ip-invent", "ip-criteria", "ip-harvest", "ip-screen", "ip-claim", "ip-dossier",
])
def test_every_skill_carries_the_stop_latch_and_gate_hook(name):
    assert lint.lint_skill_header(_skill(name)) == []


@pytest.mark.parametrize("name", [
    "ip-invent", "ip-criteria", "ip-harvest", "ip-screen", "ip-claim", "ip-dossier",
])
def test_every_cited_shared_reference_actually_exists(name):
    for ref in lint.cited_refs(_skill(name)):
        assert (lint.REF_DIR / ref).is_file(), f"{name} trỏ tới file không tồn tại: {ref}"


def test_header_lint_flags_dropping_the_stop_latch():
    dirty = "\n".join(
        p for p in lint.SKILL_REQUIRED_PHRASES if p != "Đọc không được thì DỪNG"
    )
    assert any("DỪNG" in e for e in lint.lint_skill_header(dirty))


def test_cited_refs_finds_relative_shared_paths():
    text = "đọc `../ip-shared/references/active-workspace.md` rồi `../ip-shared/references/co-mat-gate.md`"
    assert lint.cited_refs(text) == ["active-workspace.md", "co-mat-gate.md"]
```

- [ ] **Bước 2: Chạy, phải fail**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k "skill or refs or latch" -v
```

Kỳ vọng: `AttributeError: module 'ip_invent_lint' has no attribute 'lint_skill_header'`.

- [ ] **Bước 3: Thêm vào `scripts/ip_invent_lint.py`**

```python
# Cụm chữ mà MỖI SKILL.md phải mang ở khối Bước 0'.
SKILL_REQUIRED_PHRASES = [
    "../ip-shared/references/active-workspace.md",
    "../ip-shared/references/co-mat-gate.md",
    "Đọc không được thì DỪNG",
    "Bề mặt:",
]

_CITED_REF_RE = re.compile(rf"\.\./{SHARED_DIR_NAME}/references/([A-Za-z0-9._-]+\.md)")


def cited_refs(text: str) -> list[str]:
    """Tên file tham chiếu dùng chung mà một SKILL.md trích, theo thứ tự, không lặp."""
    seen: list[str] = []
    for name in _CITED_REF_RE.findall(text):
        if name not in seen:
            seen.append(name)
    return seen


def lint_skill_header(text: str) -> list[str]:
    """Kiểm một SKILL.md mang đủ chốt Bước 0'."""
    return [
        f"SKILL.md thiếu chốt: {p!r}"
        for p in SKILL_REQUIRED_PHRASES
        if p.lower() not in text.lower()
    ]
```

- [ ] **Bước 4: Chèn khối Bước 0′ vào cả 6 SKILL.md**

Chèn **ngay sau khối frontmatter `---` và dòng tiêu đề `# <tên skill> — …`**, trước mọi mục khác. Dùng **đúng văn bản này** trong cả sáu file (lint so khớp từng cụm):

````markdown
## ⛔ BƯỚC 0′ — đọc workspace TRƯỚC MỌI VIỆC KHÁC

Đọc `../ip-shared/references/active-workspace.md` → lấy tên file profile → đọc profile đó.
**Đọc không được thì DỪNG**, báo *"không đọc được tầng trỏ workspace"*, **không đoán, không chạy
tiếp bằng giá trị mặc định**. Một báo cáo trông đầy đủ mà chạy không có workspace là lỗi tệ hơn
không chạy gì.

Nếu profile khai `surface: cloud` → chạy cổng phân loại trong
`../ip-shared/references/co-mat-gate.md` **trước khi đụng nội dung ứng viên bất kỳ**.

In ở đầu mọi báo cáo:

```
Bề mặt: <surface> · Cổng phân loại: <trạng thái> · Căn cứ: <…>
```

Trường workspace nào bằng `none` → chạy **chế độ giảm** và **in dòng khai báo** (ví dụ
`1b chạy KHÔNG có TRIZ`). Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ.
````

Với `ip-invent`, đặt khối này **trước** mục `## ⛔ BA RÀO CỨNG` hiện có.

- [ ] **Bước 5: Chạy test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: toàn bộ PASS, gồm 6 + 6 test parametrize.

- [ ] **Bước 6: Commit**

```bash
git add plugins/ip-invent/skills/ scripts/
git commit -m "$(cat <<'EOF'
[IP] Chốt Bước 0' vào cả 6 SKILL.md — đọc workspace hoặc DỪNG

Mỗi skill đọc tầng trỏ trước mọi việc khác; đọc không được thì dừng thay vì
chạy tiếp bằng mặc định. Đây là mode lỗi đã bắt được ở fluency-4d: thiếu
junction shared -> skill chạy không rubric mà vẫn in báo cáo trông đủ.

Lint kiểm thêm: mọi ../ip-shared/references/*.md được trích phải tồn tại thật.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Gỡ đường dẫn neo cứng — `ip-invent` và `ip-harvest`

**Files:**
- Modify: `plugins/ip-invent/skills/ip-invent/SKILL.md` (dòng 19, 23, 106, 180–181 theo đánh số trước khi chèn Bước 0′)
- Modify: `plugins/ip-invent/skills/ip-harvest/SKILL.md` (dòng 3, 18–22, 56, 59, 133)
- Modify: `scripts/ip_invent_lint.py` (thêm `lint_paths`)
- Modify: `scripts/test_ip_invent.py`

**Interfaces:**
- Consumes: `lint.SKILLS_ROOT` từ Task 2.
- Produces: `ip_invent_lint.PATH_ALLOWLIST: list[str]` · `ip_invent_lint.FORBIDDEN_PATH_RE: re.Pattern` · `ip_invent_lint.lint_paths(text: str) -> list[str]`

- [ ] **Bước 1: Viết test cho `lint_paths` trên chuỗi tổng hợp (fail)**

Thêm vào `scripts/test_ip_invent.py`:

```python
def test_path_lint_flags_root_anchored_vault_paths():
    assert any("1_Projects" in e for e in lint.lint_paths("ghi vào `1_Projects/<proj>/IP/`"))
    assert any("2_Areas" in e for e in lint.lint_paths("quét `2_Areas/HELIX*/`"))
    assert any("3_Resources" in e for e in lint.lint_paths("xem `3_Resources/abc.md`"))


def test_path_lint_flags_absolute_windows_paths():
    assert any("D:" in e for e in lint.lint_paths(r"mở `D:\Workshop_X\x.md`"))


def test_path_lint_flags_cross_skill_references_outside_the_plugin():
    assert any("skills/" in e for e in lint.lint_paths(
        "TRIZ: skills/helix/helix-concept-generate/references/triz-40-principles.md"
    ))


def test_path_lint_allows_project_relative_meta_files():
    assert lint.lint_paths("ghi vào `_meta/decisions.md`; bài học vào `_meta/learnings.md`") == []


def test_path_lint_allows_workspace_placeholders():
    assert lint.lint_paths("ghi vào `<output_pattern>`; quét `<scan_sources>`") == []


def test_ip_invent_and_ip_harvest_have_no_hardcoded_paths():
    for name in ("ip-invent", "ip-harvest"):
        assert lint.lint_paths(_skill(name)) == [], f"{name} còn đường dẫn neo cứng"
```

- [ ] **Bước 2: Chạy, phải fail**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k path -v
```

Kỳ vọng: `AttributeError: ... has no attribute 'lint_paths'`.

- [ ] **Bước 3: Thêm `lint_paths` vào `scripts/ip_invent_lint.py`**

```python
# Đường dẫn được phép giữ nguyên trong SKILL.md: chúng TƯƠNG ĐỐI TRONG DỰ ÁN,
# resolve từ output_pattern chứ không từ gốc vault. Không nới thêm mục nào.
PATH_ALLOWLIST = ["_meta/decisions.md", "_meta/learnings.md"]

# Cấm: đường dẫn tuyệt đối, đường dẫn neo ở gốc vault, và tham chiếu chéo
# sang cây skills/ của KN-Stack (dangling khi plugin rời repo).
FORBIDDEN_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\[A-Za-z0-9_\\.-]+"
    r"|(?<![\w/])(?:1_Projects|2_Areas|3_Resources|4_Archives|5_Galaxy)/"
    r"|(?<![\w/])skills/[A-Za-z0-9_-]+/)"
)


def lint_paths(text: str) -> list[str]:
    """Bắt đường dẫn neo cứng trong một SKILL.md."""
    scrubbed = text
    for allowed in PATH_ALLOWLIST:
        scrubbed = scrubbed.replace(allowed, "«allowed»")
    hits: list[str] = []
    for m in FORBIDDEN_PATH_RE.finditer(scrubbed):
        hit = m.group(0)
        if hit not in hits:
            hits.append(hit)
    return [f"đường dẫn neo cứng, phải đi qua tầng trỏ: {h!r}" for h in hits]
```

- [ ] **Bước 4: Chạy, 5 test chuỗi tổng hợp xanh, test file thật vẫn đỏ**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k path -v
```

Kỳ vọng: 5 PASS, `test_ip_invent_and_ip_harvest_have_no_hardcoded_paths` FAIL và liệt kê đúng các đường dẫn còn lại.

- [ ] **Bước 5: Sửa `ip-invent/SKILL.md` — bốn chỗ**

| Chỗ | Từ | Thành |
|---|---|---|
| Rào cứng #1, câu ghi đầu ra | ``ghi vào `1_Projects/<proj>/IP/` `` | ``ghi vào `<output_pattern>` khai trong profile workspace`` |
| Rào cứng #2 | ``Nghiên cứu **luật công khai** thì được (notebook `ip-vn`)`` | ``Nghiên cứu **luật công khai** thì được (notebook `<nlm_notebook>`, bỏ qua nếu `none`)`` |
| Step 1 parse, dòng `OUTPUT` | `OUTPUT : 1_Projects/<project>/IP/   (mặc định; phân loại MẬT)` | `OUTPUT : <output_pattern>   (từ profile workspace; phân loại MẬT)` |
| Mục `## NLM reference` | ``Notebook `ip-vn` … `3_Resources/Deep-Content-Analyzer-Outputs/RESEARCH_…md` `` | ``Notebook `<nlm_notebook>` — **chỉ nguồn luật công khai**; `none` thì bỏ qua mục này và **in dòng khai báo** *"chạy KHÔNG có notebook luật"*. Nghiên cứu nền: file `RESEARCH_ip-sang-che-gphi-chuc-danh_2026-08-06.md` trong `<root>` (nếu profile có).`` |

Giữ nguyên rào cứng #2 phần *"KHÔNG đưa nội dung giải pháp chưa bộc lộ vào… cloud"* nhưng **thêm một dòng** trỏ sang cổng: `Chi tiết tách bí-mật-nhà-nước ↔ chưa-bộc-lộ: xem `../ip-shared/references/co-mat-gate.md`.`

Giữ nguyên dòng `_meta/decisions.md` và `_meta/learnings.md` — nằm trong allowlist.

- [ ] **Bước 6: Sửa `ip-harvest/SKILL.md` — năm chỗ**

| Chỗ | Từ | Thành |
|---|---|---|
| `description` (frontmatter) | `1a THU HOẠCH quét vault (1_Projects, design journal, RE report, _meta/decisions.md)` | `1a THU HOẠCH quét các nguồn khai trong profile workspace (hồ sơ dự án, design journal, RE report, _meta/decisions.md)` |
| Bảng "Nơi quét" (5 hàng đầu) | các ô `1_Projects/*/`, `2_Areas/HELIX*/` | thay bảng bằng: **"Quét đúng các nguồn khai ở trường `scan_sources` của profile workspace"** + bảng giữ nguyên cột "Tìm gì" nhưng cột "Nguồn" mô tả bằng lời (`hồ sơ dự án`, `khu vực thiết kế + design journal`, `RE report`, `_meta/decisions.md`, `FTO Record QP-02-06`, `sản phẩm đã triển khai`) |
| Điều kiện 1b, dòng patent map | `(qua /research --patents)` | ``(qua `<patent_search>`; `none` → bỏ bước này và **in dòng khai báo**)`` |
| Điều kiện 1b, dòng TRIZ | `3. TRIZ: skills/helix/helix-concept-generate/references/triz-40-principles.md + triz-sufield-76solutions.md` | ``3. TRIZ: các file ở `<triz_refs>`; `none` → **in dòng khai báo** `1b chạy KHÔNG có TRIZ` và sinh phương án bằng phân tích vùng trống thuần`` |
| Rules, dòng cuối | ``Kết quả **MẬT** → `1_Projects/<proj>/IP/` `` | ``Kết quả **MẬT** → `<output_pattern>` `` |

Thêm vào mục Rules của `ip-harvest` **một luật mới** (spec yêu cầu, chưa có ở đâu khác):

```markdown
- **`scan_sources: none` KHÔNG phải là "1a chạy xong không thấy gì".** Không quét được ≠ quét xong
  không có. Gặp `none` thì B1 **dừng**, in dòng khai báo, báo CEO nạp ứng viên tay — **không tự
  nhảy sang 1b**. 1b chỉ chạy khi 1a *chạy được* và không đủ ứng viên sạch.
```

- [ ] **Bước 7: Chạy test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

Kỳ vọng: toàn bộ PASS.

- [ ] **Bước 8: Chạy lại eval để chắc chưa làm vỡ assertion cũ**

```bash
bash evals/run-eval.sh ip-invent
```

Kỳ vọng: vẫn 14/14 required. Nếu tụt, xem assertion nào neo vào chuỗi vừa sửa và ghi lại để xử ở Task 8 — **không nới `passing_score` để né**.

- [ ] **Bước 9: Commit**

```bash
git add plugins/ip-invent/skills/ip-invent/SKILL.md plugins/ip-invent/skills/ip-harvest/SKILL.md scripts/
git commit -m "$(cat <<'EOF'
[IP] ip-invent + ip-harvest: đường dẫn đi qua tầng trỏ, không neo cứng nữa

Vá ba tham chiếu dangling sẵn khi plugin rời KN-Stack: TRIZ trỏ sang
skills/helix, /research --patents, và file RESEARCH trong 3_Resources.
Cả ba giờ là trường workspace; none thì chạy chế độ giảm và PHẢI khai.

Thêm luật: scan_sources=none không phải "1a không thấy gì" — B1 dừng và báo,
không tự nhảy sang 1b.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Gỡ đường dẫn neo cứng — bốn skill còn lại

**Files:**
- Modify: `plugins/ip-invent/skills/ip-screen/SKILL.md` (dòng 69, 146, 231 theo đánh số gốc)
- Modify: `plugins/ip-invent/skills/ip-dossier/SKILL.md` (dòng 191 theo đánh số gốc)
- Verify: `plugins/ip-invent/skills/ip-criteria/SKILL.md`, `plugins/ip-invent/skills/ip-claim/SKILL.md` (đã sạch, chỉ xác nhận)
- Modify: `scripts/test_ip_invent.py`

**Interfaces:**
- Consumes: `lint.lint_paths` từ Task 5.
- Produces: không có API mới — chỉ mở rộng phạm vi kiểm sang cả 6 skill.

- [ ] **Bước 1: Thay test hai-file bằng test sáu-file (fail)**

Trong `scripts/test_ip_invent.py`, **xoá** `test_ip_invent_and_ip_harvest_have_no_hardcoded_paths` và thay bằng:

```python
@pytest.mark.parametrize("name", [
    "ip-invent", "ip-criteria", "ip-harvest", "ip-screen", "ip-claim", "ip-dossier",
])
def test_no_skill_carries_a_hardcoded_path(name):
    assert lint.lint_paths(_skill(name)) == []
```

- [ ] **Bước 2: Chạy, phải fail đúng hai file**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k hardcoded -v
```

Kỳ vọng: 4 PASS (`ip-invent`, `ip-harvest` đã sửa ở Task 5; `ip-criteria`, `ip-claim` vốn sạch), 2 FAIL (`ip-screen`, `ip-dossier`).

- [ ] **Bước 3: Sửa `ip-screen/SKILL.md` — ba chỗ**

| Chỗ | Từ | Thành |
|---|---|---|
| Pre-search prior art | ``Gọi `/research --patents <từng dấu hiệu>` `` | ``Gọi `<patent_search> <từng dấu hiệu>`; `none` → **in dòng khai báo** *"pre-search KHÔNG chạy được, trục I chấm thiếu bằng chứng prior art"* và **hạ độ tin** của kết luận trục I`` |
| Ghi chú sáng chế MẬT | ``chưa có trong notebook `ip-vn` `` | ``chưa có trong notebook `<nlm_notebook>` `` |
| Rules, dòng cuối | ``Kết quả **MẬT** → `1_Projects/<proj>/IP/` `` | ``Kết quả **MẬT** → `<output_pattern>` `` |

Giữ nguyên `/research --patents` trong `description` frontmatter — đó là tên công cụ, không phải đường dẫn vault, và `lint_paths` không đụng tới. Giữ nguyên dòng `_meta/decisions.md` (allowlist).

- [ ] **Bước 4: Sửa `ip-dossier/SKILL.md` — một chỗ**

| Chỗ | Từ | Thành |
|---|---|---|
| Mục `## Output` | ``Ghi vào `1_Projects/<project>/IP/`: `` | ``Ghi vào `<output_pattern>`: `` |

Giữ nguyên dòng `<_meta/decisions.md | design journal | biên bản>` (allowlist).

- [ ] **Bước 5: Xác nhận `ip-criteria` và `ip-claim` vốn sạch**

```bash
cd /d/KN-Stack && python -c "
import importlib.util, sys
from pathlib import Path
s = importlib.util.spec_from_file_location('l', 'scripts/ip_invent_lint.py')
l = importlib.util.module_from_spec(s); sys.modules['l'] = l; s.loader.exec_module(l)
for n in ('ip-criteria', 'ip-claim'):
    t = (l.SKILLS_ROOT / n / 'SKILL.md').read_text(encoding='utf-8')
    print(n, l.lint_paths(t))
"
```

Kỳ vọng: cả hai in `[]`. Nếu không rỗng → sửa theo cùng khuôn bảng ở Bước 3 rồi chạy lại.

- [ ] **Bước 6: Chạy toàn bộ test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

- [ ] **Bước 7: Chạy cả hai eval**

```bash
bash evals/run-eval.sh ip-invent
bash evals/run-eval.sh ip-screen
```

Kỳ vọng: ip-invent 14/14, ip-screen 13/13 required.

- [ ] **Bước 8: Commit**

```bash
git add plugins/ip-invent/skills/ scripts/test_ip_invent.py
git commit -m "$(cat <<'EOF'
[IP] ip-screen + ip-dossier: nốt đường dẫn neo cứng qua tầng trỏ

Sáu SKILL.md giờ không file nào biết tên vault. ip-criteria và ip-claim vốn
đã sạch, chỉ xác nhận. Test mở rộng thành parametrize cả sáu file.

patent_search=none ở ip-screen không im lặng: pre-search không chạy được thì
trục I phải khai thiếu bằng chứng và hạ độ tin, không chấm như thường.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Khuôn ledger + README

**Files:**
- Create: `plugins/ip-invent/templates/_pipeline_state.md`
- Create: `plugins/ip-invent/README.md`
- Modify: `scripts/ip_invent_lint.py` (thêm `lint_ledger_template`)
- Modify: `scripts/test_ip_invent.py`

**Interfaces:**
- Consumes: `lint.PLUGIN_ROOT` từ Task 2.
- Produces: `ip_invent_lint.LEDGER_ROWS: list[str]` · `ip_invent_lint.lint_ledger_template(text: str) -> list[str]`

- [ ] **Bước 1: Viết test (fail)**

```python
def test_ledger_template_carries_all_five_blocks_and_the_gate_flag():
    text = (lint.PLUGIN_ROOT / "templates" / "_pipeline_state.md").read_text(encoding="utf-8")
    assert lint.lint_ledger_template(text) == []


def test_ledger_lint_flags_a_missing_block_row():
    dirty = "\n".join(r for r in lint.LEDGER_ROWS if r != "B3 ip-claim")
    assert any("B3" in e for e in lint.lint_ledger_template(dirty))


def test_readme_marks_cowork_import_as_unverified():
    text = (lint.PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    assert "CHƯA KIỂM CHỨNG" in text


def test_readme_and_skills_agree_on_the_shared_dir_name():
    text = (lint.PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
    assert lint.SHARED_DIR_NAME in text
    assert "_shared" not in text.replace(lint.SHARED_DIR_NAME, "")
```

- [ ] **Bước 2: Chạy, phải fail**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -k "ledger or readme" -v
```

- [ ] **Bước 3: Thêm `lint_ledger_template` vào `scripts/ip_invent_lint.py`**

```python
LEDGER_ROWS = [
    "B0 ip-criteria", "B1 ip-harvest", "B2 ip-screen",
    "B3 ip-claim", "B4 ip-dossier",
]

# Cờ ràng buộc bắt buộc có trong ledger — mỗi cờ là một cổng chặn thật.
LEDGER_FLAGS = ["Bộc lộ", "Điều 10a", "Điều 14", "thẩm định nhanh", "Cổng phân loại"]


def lint_ledger_template(text: str) -> list[str]:
    """Kiểm khuôn ledger mang đủ 5 hàng block và 5 cờ ràng buộc."""
    errors = [f"ledger thiếu hàng: {r!r}" for r in LEDGER_ROWS if r not in text]
    errors += [f"ledger thiếu cờ: {f!r}" for f in LEDGER_FLAGS if f.lower() not in text.lower()]
    return errors
```

- [ ] **Bước 4: Viết `plugins/ip-invent/templates/_pipeline_state.md`**

```markdown
# IP Pipeline State — <project>

Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>
Bề mặt: <local | cloud> · Cổng phân loại: <chưa chạy | không thuộc | DỪNG> · Căn cứ: <…>
Đích chức danh: 431 | 12-2025 | cả hai
Phân loại: MẬT

| Block | Trạng thái | Ngày | CEO duyệt | Kết quả chính |
|-------|-----------|------|-----------|---------------|
| B0 ip-criteria | | | | đường chọn: |
| B1 ip-harvest  | | | | N ứng viên: |
| B2 ip-screen   | | | | routing: |
| B3 ip-claim    | | | | khung: |
| B4 ip-dossier  | | | | |

## Cờ ràng buộc

- [ ] **Cổng phân loại**: bề mặt cloud → đã chạy `co-mat-gate.md`, có căn cứ, không phải "chưa rõ"
- [ ] **Bộc lộ**: chưa khóa priority date → cấm công khai
- [ ] **Điều 10a**: đã ghi xuất xứ đóng góp người/AI
- [ ] **Điều 14**: có ý định nộp nước ngoài? → cần phép BQP/BCA TRƯỚC
- [ ] **Trần thẩm định nhanh**: ≤10 điểm YCBH, ≤02 điểm độc lập

## Chế độ giảm đã khai

<liệt kê mọi trường workspace = none và block nào đã chạy thiếu — trống nghĩa là chạy đủ>
```

- [ ] **Bước 5: Viết `plugins/ip-invent/README.md`**

Chín mục, theo đúng thứ tự này. Sáu mục đầu viết theo đặc tả bên dưới; ba mục cuối chép nguyên văn ba khối cho sẵn.

| # | Mục | Nội dung phải có |
|---|---|---|
| 1 | `# ip-invent` + một đoạn mở | Plugin Claude tự chứa (Markdown/JSON thuần, không Python/hook/MCP) dựng hồ sơ sở hữu trí tuệ **tấn công**: ý tưởng → bộ đơn giao đại diện SHTT. Nêu là **cặp đối xứng của QP-02-06 FTO** — FTO tránh claim người khác, plugin này dựng claim của mình. |
| 2 | `## Plugin làm gì` | Bảng 6 hàng: `ip-invent` (orchestrator thin-commander, một-block-một-lượt, ledger là kênh duy nhất) · `ip-criteria` B0 CHẶN (thước đo "cái gì được tính", QĐ 431 ↔ QĐ 12/2025) · `ip-harvest` B1 (thu hoạch trước, sinh mới sau; 4 trường bắt buộc/ứng viên) · `ip-screen` B2 (hai trục, cấm bình quân; routing 4 đường gồm sáng chế MẬT) · `ip-claim` B3 (2–3 khung claim, đếm điểm độc lập vs trần thẩm định nhanh) · `ip-dossier` B4 (bộ đơn theo Phụ lục I hiện hành + handoff). Mỗi hàng nêu **CEO checkpoint** của block đó. |
| 3 | `## Ba cổng chặn` | Cổng bộc lộ (Điều 60, chưa khóa priority date → cấm công khai) · cổng phân loại bí mật nhà nước (`co-mat-gate.md`, chỉ chạy khi `surface: cloud`) · cổng advisory-only (không thay đại diện SHTT / cơ quan xét chức danh / cơ quan xác định bí mật nhà nước). Ghi rõ **ba cổng độc lập, phải qua cả ba**. |
| 4 | `## Luật nền đổi rất nhanh` | Chuỗi NĐ 65/2023 → 15/2026 → 33/2026 → 100/2026 và Luật SHTT 50/2005 sđ 36/2009, 42/2019, 07/2022, 93/2025, 131/2025. Câu chốt: mọi đầu ra có quy cách/biểu mẫu/thời hạn/phí **phải in dòng** `Chuỗi sửa đổi kiểm tại: <ngày> — nguồn: <văn bản mới nhất>`. |
| 5 | `## Tầng trỏ workspace` | Bảng 7 trường (`surface`/`root`/`output_pattern`/`scan_sources`/`triz_refs`/`patent_search`/`nlm_notebook`) + ba profile có sẵn. Câu chốt: đổi môi trường = **sửa đúng một dòng** trong `active-workspace.md`, không đụng `SKILL.md` nào. Nêu luật `none` = **chạy chế độ giảm và phải in dòng khai báo**. |
| 6 | `## Khởi tạo ledger` | Plugin **không tự dựng sổ**. Chép `templates/_pipeline_state.md` vào `<output_pattern>` trước lần chạy đầu của mỗi dự án. Nêu ledger là **kênh duy nhất** giữa các block — không truyền ngầm qua hội thoại. |
| 7 | `## Import vào Cowork` | chép nguyên khối cho sẵn bên dưới |
| 8 | `## Dùng trong Claude Code` | chép nguyên khối cho sẵn bên dưới |
| 9 | `## Bảo trì` | chép nguyên khối cho sẵn bên dưới |

Ba khối chép nguyên văn:

```markdown
## Import vào Cowork

> ⚠️ **CHƯA KIỂM CHỨNG.** Hai cách dưới đây chép theo khuôn plugin `fluency-4d`; chưa lần nào
> chạy thật trong Cowork. Chạy được rồi thì sửa mục này cho đúng, đừng để nguyên câu hứa.

Copy nguyên thư mục `plugins/ip-invent/` (gồm `.claude-plugin/plugin.json` + `skills/` +
`templates/`) vào thư mục plugin của Cowork, hoặc trỏ marketplace của Cowork tới repo `KN-Stack`.
Sau khi import, xác nhận **sáu skill xuất hiện**: `ip-invent`, `ip-criteria`, `ip-harvest`,
`ip-screen`, `ip-claim`, `ip-dossier`.

Copy **nguyên cây**, đừng copy lẻ từng thư mục skill: `skills/ip-shared/references/` phải nằm cạnh
sáu thư mục skill thì `../ip-shared/references/…` trong `SKILL.md` mới resolve được.

Sau khi import, **đổi `active-workspace.md` sang `workspace-cowork.md`** — nếu quên, plugin chạy
với profile `local` và sẽ đi tìm vault không tồn tại.
```

```markdown
## Dùng trong Claude Code

Bảy thư mục được junction vào `~/.claude/commands/`. **Junction `ip-shared` là BẮT BUỘC, không
phải tuỳ chọn.** Khi chạy qua junction, mỗi skill nằm trực tiếp dưới `~/.claude/commands/`, nên
`..` không còn là `skills/` của plugin mà là chính `~/.claude/commands/`. Thiếu junction thứ bảy
thì `../ip-shared/references/` không tồn tại — nhưng chốt Bước 0′ trong cả sáu `SKILL.md` sẽ
**DỪNG** thay vì chạy tiếp âm thầm.

    bash setup.sh --install    # tạo junction còn thiếu
    bash setup.sh --verify     # kỳ vọng: 7 plugin skill dirs verified

⚠️ `bash setup.sh --unlink` gỡ **cả bảy** junction cùng các skill khác. Sau `--unlink` chạy lại
`--install`; đừng dựng tay từng cái rồi quên `ip-shared`.
```

```markdown
## Bảo trì

Sau mỗi lần sửa bất kỳ file nào trong `skills/ip-shared/references/` hoặc bất kỳ `SKILL.md` nào:

    python -m pytest scripts/test_ip_invent.py -v
    bash evals/run-eval.sh ip-invent
    bash evals/run-eval.sh ip-screen

Bộ test nằm ngoài plugin (ở `scripts/`) vì plugin phải thuần Markdown + JSON. Nó kiểm: bảy trường
workspace đủ và đúng thứ tự · mọi `../ip-shared/references/*.md` được trích tồn tại thật · cả sáu
`SKILL.md` mang chốt Bước 0′ · không `SKILL.md` nào còn đường dẫn neo cứng.
```

- [ ] **Bước 6: Chạy test, phải xanh**

```bash
cd /d/KN-Stack && python -m pytest scripts/test_ip_invent.py -v
```

- [ ] **Bước 7: Commit**

```bash
git add plugins/ip-invent/templates/ plugins/ip-invent/README.md scripts/
git commit -m "$(cat <<'EOF'
[IP] Khuôn ledger + README plugin ip-invent

Ledger thêm dòng Bề mặt/Cổng phân loại và mục "Chế độ giảm đã khai" để
trường workspace=none không biến mất khỏi hồ sơ.

README ghi thẳng rằng cách import Cowork CHƯA KIỂM CHỨNG, thay vì hứa suông.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: Eval v1.2, bản đồ repo, phiên bản

**Files:**
- Modify: `evals/ip-invent.json`
- Modify: `CLAUDE.md`
- Modify: `VERSION`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: toàn bộ Task 1–7.
- Produces: deliverable cuối — repo nhất quán, eval bảo vệ được hai cơ chế mới.

- [ ] **Bước 1: Ghi lại số hiện tại làm mốc**

```bash
cd /d/KN-Stack && python -c "
import json; d=json.load(open('evals/ip-invent.json',encoding='utf-8'))
print('assertions', len(d['assertions']), 'required', sum(1 for a in d['assertions'] if a.get('required')), 'total_required', d['total_required'], 'passing_score', d['passing_score'])
"
```

Kỳ vọng: `assertions 15 required 14 total_required 14 passing_score 15`.

- [ ] **Bước 2: Thêm hai assertion vào `evals/ip-invent.json`**

Thêm vào cuối mảng `assertions`:

```json
{
  "id": "IP-WORKSPACE",
  "name": "reads_pointer_layer_or_stops",
  "check": "orchestrator đọc tầng trỏ workspace TRƯỚC mọi việc khác và DỪNG nếu đọc không được — đảo thành 'đọc không được thì dùng mặc định' phải fail",
  "regex": "\\.\\./ip-shared/references/active-workspace\\.md[\\s\\S]{0,400}Đọc không được thì DỪNG",
  "required": true
},
{
  "id": "IP-COMAT",
  "name": "cloud_surface_triggers_classification_gate",
  "check": "surface cloud kích hoạt cổng phân loại trước khi đụng nội dung ứng viên",
  "regex": "surface[^\\n]{0,40}cloud[\\s\\S]{0,300}co-mat-gate\\.md[\\s\\S]{0,300}trước khi đụng nội dung",
  "required": true
}
```

Và **bump hai số**: `"total_required": 16`, `"passing_score": 17`. Đổi `"version"` thành `"1.2"` và nối vào cuối `description`:

```
v1.2: thêm IP-WORKSPACE + IP-COMAT sau khi đóng gói thành plugin — tầng trỏ workspace và cổng phân loại bí mật nhà nước là hai cơ chế mới, không có assertion thì chúng có thể bị gỡ mà eval vẫn xanh.
```

- [ ] **Bước 3: Chạy eval, phải đạt mức mới**

```bash
bash evals/run-eval.sh ip-invent
```

Kỳ vọng: `Required passed: 16 / 16`. Nếu IP-COMAT fail → chỉnh **văn bản khối Bước 0′ trong `ip-invent/SKILL.md`** cho khớp regex, **không nới regex để né**.

- [ ] **Bước 4: Cập nhật `CLAUDE.md`**

- Trong cây `skills/`: **xoá** khối `├── ip/ (6) — Sở hữu trí tuệ TẤN CÔNG …` (6 dòng mô tả kèm theo).
- Sửa dòng đếm domain: `15 domains` → `14 domains`; sửa tổng số skill cho khớp `bash setup.sh --status`.
- Thêm mục mới sau cây `skills/`:

```markdown
├── plugins/          ← plugin tự chứa, copy-anywhere (setup.sh --install junction cả hai)
│   ├── ip-invent/    — Sở hữu trí tuệ TẤN CÔNG: orchestrator + 5 block
│   │                   (ip-criteria/harvest/screen/claim/dossier) + ip-shared/references.
│   │                   Cặp đối xứng của QP-02-06 FTO — FTO tránh claim người khác, plugin này
│   │                   dựng claim của mình. B0 ip-criteria là CHẶN: dựng thước đo "cái gì được
│   │                   tính" (QĐ 431/QĐ-BQP ↔ QĐ 12/2025/QĐ-TTg) TRƯỚC khi rà ứng viên. Luật nền
│   │                   đổi rất nhanh (NĐ 65/2023 → 15/2026 → 33/2026 → 100/2026) nên mọi đầu ra
│   │                   có quy cách PHẢI in ngày kiểm chuỗi sửa đổi.
│   │                   Chạy được cả trong Cowork qua tầng trỏ workspace + cổng phân loại.
│   └── leo-ai/       — MCP leo-bridge + 4 skill LEO
```

- Trong mục **Evals**, thêm dòng: `Plugin có lint riêng ngoài plugin: python -m pytest scripts/test_ip_invent.py -v`

- [ ] **Bước 5: Bump `VERSION` và ghi `CHANGELOG.md`**

`VERSION` hiện là **1.7.0**, nên số kế tiếp là `1.8.0`. Nhưng các nhánh chưa merge hay giành cùng
một số — `CHANGELOG.md` đã có tiền lệ ghi rõ chuyện đó ở mục 1.7.0 (số 1.6.0 bị
`feature/fluency-4d-dmir` lấy mất). Kiểm trước khi lấy:

```bash
cd /d/KN-Stack
cat VERSION                                              # kỳ vọng: 1.7.0
git log --all --oneline -S'## [1.8.0]' -- CHANGELOG.md   # rỗng = 1.8.0 còn trống
```

Nếu lệnh thứ hai **rỗng** → lấy `1.8.0`. Nếu **có kết quả** → lấy số nhỏ nhất còn trống (`1.9.0`, …)
và thêm một dòng `>` ngay dưới tiêu đề, đúng khuôn dòng chú ở mục `[1.7.0]`, nêu nhánh nào đã dùng
số bị bỏ qua. Thay `<ver>` bên dưới bằng số đã chốt.

```markdown
## [<ver>] — 2026-08-08

### Added
- **Plugin `ip-invent`** — 6 skill IP dời từ `skills/ip/` sang `plugins/ip-invent/skills/`,
  một nguồn chuẩn duy nhất, không `build.sh`. Chạy được cả trong Claude Code (7 junction) lẫn
  Cowork (cây plugin nguyên vẹn).
- **Tầng trỏ workspace** `ip-shared/references/active-workspace.md` + 3 profile
  (`knstack` local · `cowork` cloud · `template`). Đổi môi trường = sửa một dòng, không đụng
  `SKILL.md` nào.
- **Cổng phân loại** `co-mat-gate.md` — kích hoạt khi `surface: cloud`. Tách bí-mật-nhà-nước
  (cấm tuyệt đối) khỏi chưa-bộc-lộ-nhưng-không-MẬT (Điều 60.2 cho phép bộc lộ có nghĩa vụ bảo
  mật). Mặc định "chưa rõ" = coi như thuộc = DỪNG.
- `scripts/ip_invent_lint.py` + `scripts/test_ip_invent.py` — lint tham chiếu, đường dẫn, chốt.
- `evals/ip-invent.json` v1.2: IP-WORKSPACE + IP-COMAT, `total_required` 14 → 16.

### Fixed
- Ba tham chiếu dangling sẵn trong `skills/ip/` khi rời KN-Stack: TRIZ trỏ sang
  `skills/helix/…`, `/research --patents`, và file RESEARCH trong `3_Resources/`. Cả ba giờ là
  trường workspace; `none` thì block chạy chế độ giảm và **phải in dòng khai báo**.
- `ip-harvest`: `scan_sources: none` không còn bị hiểu nhầm là "1a chạy xong không thấy gì" —
  B1 dừng và báo CEO thay vì tự nhảy sang 1b.

### Changed
- `setup.sh` lấy bản plugin-aware từ `feature/fluency-4d-plugin` (commit `<hash ghi ở Task 1 Bước 2>`)
  — biết đi vào `plugins/*/skills/*/` và junction cả thư mục tham chiếu dùng chung.
```

- [ ] **Bước 6: Chạy toàn bộ kiểm chứng, đúng thứ tự spec**

```bash
cd /d/KN-Stack
bash setup.sh --verify
python -m pytest scripts/test_ip_invent.py -v
bash evals/run-eval.sh ip-invent
bash evals/run-eval.sh ip-screen
bash setup.sh --status
```

Kỳ vọng: 7 junction xanh · test toàn PASS · ip-invent 16/16 · ip-screen 13/13 · `--status` in số skill khớp con số vừa ghi vào `CLAUDE.md`.

- [ ] **Bước 7: Chạy thật `/ip-criteria` qua junction**

Trong một phiên Claude Code, gọi `/ip-criteria --target 431`.

Kỳ vọng: skill in dòng `Bề mặt: local · Cổng phân loại: …` ở đầu báo cáo, rồi chạy B0 bình thường. Chọn B0 vì nó thuần **luật công khai**, không đụng nội dung ứng viên nào.

Nếu skill không in dòng `Bề mặt:` → junction `ip-shared` hỏng hoặc khối Bước 0′ chèn sai chỗ. Kiểm `bash setup.sh --verify` trước, rồi kiểm vị trí khối trong `SKILL.md`.

- [ ] **Bước 8: Commit**

```bash
git add evals/ip-invent.json CLAUDE.md VERSION CHANGELOG.md
git commit -m "$(cat <<'EOF'
[IP] eval v1.2 + bản đồ repo + bump VERSION cho plugin ip-invent

Hai assertion mới (IP-WORKSPACE, IP-COMAT) khoá hai cơ chế mới lại: không có
chúng thì tầng trỏ và cổng phân loại có thể bị gỡ mà eval vẫn xanh.
total_required 14 -> 16, passing_score 15 -> 17.

CLAUDE.md: skills/ip gỡ khỏi cây skills, mô tả chuyển sang mục plugins/.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Ghi chú cho người triển khai

**Số dòng trong Task 5 và 6 là đánh số TRƯỚC khi chèn khối Bước 0′ ở Task 4.** Sau Task 4 mọi dòng dịch xuống ~20 dòng. Đừng nhảy tới số dòng — tìm theo **chuỗi văn bản** nêu ở cột "Từ" của bảng.

**Đừng nới ngưỡng để né test đỏ.** Ba chỗ dễ cám dỗ: `passing_score` trong eval, `PATH_ALLOWLIST` trong lint, và regex của IP-COMAT. Cả ba đều là chốt cố ý; test đỏ nghĩa là nội dung sai, không phải chốt sai.

**Nhánh `feature/fluency-4d-plugin` chưa merge.** Task 1 lấy `setup.sh` từ đó một lần và ghi hash vào CHANGELOG. Merge hai nhánh là việc riêng, ngoài phạm vi kế hoạch này.
