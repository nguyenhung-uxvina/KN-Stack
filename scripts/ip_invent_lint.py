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


def parse_workspace_rows(text: str) -> list[tuple[str, str]]:
    """Từng hàng thô `| `trường` | giá trị |` theo đúng thứ tự xuất hiện, GIỮ hàng trùng.

    Dùng cho lint — `parse_workspace_profile` gom về dict nên nuốt mất hàng
    trùng (khoá sau đè khoá trước); hàm này giữ nguyên để lint chấm được cả
    hàng trùng, hàng thừa, sai thứ tự.
    """
    return [(k, v.strip("` ")) for k, v in _PROFILE_ROW_RE.findall(text)]


def parse_workspace_profile(text: str) -> dict[str, str]:
    """Bảng `| `trường` | giá trị |` của một file workspace-*.md → dict."""
    return dict(parse_workspace_rows(text))


def lint_workspace_profile(text: str) -> list[str]:
    """Kiểm một file workspace-*.md. Trả danh sách lỗi; rỗng nghĩa là đạt."""
    errors: list[str] = []
    rows = parse_workspace_rows(text)
    found = [k for k, _ in rows]

    seen: set[str] = set()
    duplicates: list[str] = []
    for f in found:
        if f in seen and f not in duplicates:
            duplicates.append(f)
        seen.add(f)
    if duplicates:
        errors.append(f"profile có hàng trùng: {duplicates}")

    if found != WORKSPACE_FIELDS:
        unique_found = list(dict.fromkeys(found))
        missing = [f for f in WORKSPACE_FIELDS if f not in found]
        extra = [f for f in unique_found if f not in WORKSPACE_FIELDS]
        if missing:
            errors.append(f"profile thiếu trường: {missing}")
        if extra:
            errors.append(f"profile có trường lạ: {extra}")
        if not missing and not extra and not duplicates:
            errors.append(f"profile sai thứ tự trường: {found}")

    surface = dict(rows).get("surface")
    if surface is not None and surface not in VALID_SURFACES:
        errors.append(f"surface phải là local|cloud, thấy: {surface!r}")
    return errors


# Hai mệnh đề quyền-sở-hữu-quyết-định bắt buộc có mặt trong co-mat-gate.md.
# Chỉ hai cái này kiểm bằng có-mặt chuỗi là đủ, vì chúng là TUYÊN BỐ đứng độc
# lập (không phải một quan hệ giữa hai ô bảng) — đảo nghĩa chúng đồng nghĩa
# xoá rồi viết lại bằng chữ khác, việc soát bảng 3-ngả bên dưới không với tới.
GATE_OWNERSHIP_PHRASES = [
    "Điều 60.2",
    "quyết định của CEO, không phải kết luận pháp lý",
]

_TABLE_SEP_RE = re.compile(r"^:?-+:?$")

# Nội dung trong code fence không render thành bảng Markdown thật (fence bọc
# quanh bảng thật) và không phải thủ tục đang có hiệu lực (fence chứa bảng
# "ví dụ" dán thêm) — bỏ trước khi tìm hàng, ở CẢ HAI hướng.
_FENCE_RE = re.compile(r"^```[^\n]*\n.*?\n```[ \t]*$", re.MULTILINE | re.DOTALL)

# Bảng 3 ngả chỉ có hiệu lực trong đúng mục Bước 0′ — một bảng/danh sách khác
# hình dạng ở heading khác trong file không phải là thủ tục thật đang chạy.
_STEP0_SECTION_RE = re.compile(r"^##[ \t]*Bước 0′.*?(?=^##[ \t]|\Z)", re.MULTILINE | re.DOTALL)

# Dấu hiệu phủ định/ngoại lệ NẰM NGAY TRONG Ô đủ để vô hiệu hoá một tuyên bố
# DỪNG hay coi-như-thuộc — kiểm "token có mặt trong ô" vẫn là kiểm có-mặt
# chuỗi, chỉ thu hẹp phạm vi từ cả file xuống một ô; "KHÔNG DỪNG" hay "DỪNG
# là không cần thiết" vẫn giữ nguyên token nên lọt nếu không có danh sách này.
_NEGATION_CUES = [
    "không dừng",
    "không coi như thuộc",
    "là không cần thiết",
    "trừ khi",
    "ngoại lệ",
]
# "chạy tiếp" chỉ tính là phủ định khi xét ô của hàng ĐÁNG LẼ PHẢI DỪNG (bí
# mật nhà nước / Chưa rõ). Ở hàng Không thuộc, "Chạy tiếp." chính là nội dung
# ĐÚNG — không được liệt cue này vào đó, nếu không lint sẽ tự mâu thuẫn.
_CONTINUE_CUE = "chạy tiếp"

_ACTIVATION_CUE = "kích hoạt"
_DEACTIVATION_CUE = "không chạy"


def _strip_code_fences(text: str) -> str:
    """Bỏ toàn bộ nội dung trong code fence (```…```)."""
    return _FENCE_RE.sub("", text)


def _extract_step0_section(text: str) -> str:
    """Phần dưới heading '## Bước 0′…' đến heading `##` kế tiếp (hoặc hết file)."""
    m = _STEP0_SECTION_RE.search(text)
    return m.group(0) if m else ""


def parse_gate_table_rows(text: str) -> list[tuple[str, str]]:
    """Hàng thô `| Phân loại | Xử |` của bảng Bước 0′, GIỮ hàng trùng và thứ tự.

    Chỉ quét bên trong mục '## Bước 0′…', sau khi đã bỏ mọi code fence (xem
    `_extract_step0_section` / `_strip_code_fences`) — một bảng "ví dụ" dán ở
    heading khác hoặc trong fence, hoặc bảng thật bị bọc vào fence để không
    còn render, đều không được tính là hàng thật. Bỏ header (`Phân loại`) và
    hàng phân cách markdown (`|---|---|`). Không gom dict — cùng lý do
    `parse_workspace_rows` không gom: gom sẽ nuốt hàng trùng hoặc hàng
    thiếu, làm phép đếm "đúng 3 hàng" phía dưới vô hiệu.
    """
    section = _extract_step0_section(_strip_code_fences(text))
    rows: list[tuple[str, str]] = []
    for line in section.splitlines():
        line = line.strip()
        if not line.startswith("|") or not line.endswith("|") or len(line) < 2:
            continue
        cells = [c.strip() for c in line[1:-1].split("|")]
        if len(cells) != 2:
            continue
        c1, c2 = cells
        if _TABLE_SEP_RE.fullmatch(c1) and _TABLE_SEP_RE.fullmatch(c2):
            continue  # hàng phân cách markdown
        if c1.lower() == "phân loại":
            continue  # hàng header
        rows.append((c1, c2))
    return rows


def _is_undermined(cell: str, *, reject_continue: bool = False) -> bool:
    """True nếu ô mang dấu hiệu phủ định/ngoại lệ đủ vô hiệu hoá một tuyên bố
    DỪNG hay coi-như-thuộc NẰM TRONG CHÍNH ô đó."""
    low = cell.lower()
    if any(cue in low for cue in _NEGATION_CUES):
        return True
    if reject_continue and _CONTINUE_CUE in low:
        return True
    return False


def _has_effective(cell: str, token: str, *, reject_continue: bool = False) -> bool:
    """True nếu `token` có mặt trong ô VÀ không bị phủ định/ngoại lệ hoá."""
    return token in cell.lower() and not _is_undermined(cell, reject_continue=reject_continue)


def lint_gate_doc(text: str) -> list[str]:
    """Kiểm co-mat-gate.md bằng QUAN HỆ giữa ô với ô của bảng 3 ngả — có
    HIỆU LỰC, không phải bằng việc đếm token có mặt ở đâu đó.

    Vì sao đổi cách kiểm: `evals/ip-invent.json` (trường description) ghi
    nguyên văn một mutation test đã bắt được IP-DISCLOSE từng là cổng-đếm-từ-
    khoá — một cổng bộc lộ bị ĐẢO NGHĨA vẫn xanh vì các token rải rác nơi khác
    thoả mãn phép match không giới hạn. Vòng review đầu của chính lint này lặp
    lại đúng lớp lỗi đó ở phạm vi hẹp hơn: kiểm "DỪNG có mặt trong ô" vẫn là
    kiểm có-mặt chuỗi, nên "KHÔNG DỪNG" hay "DỪNG là không cần thiết → chạy
    tiếp" vẫn xanh vì token còn nguyên. `_has_effective` đóng lỗ đó bằng cách
    đòi token có mặt VÀ không bị một cue phủ định/ngoại lệ nào trong CHÍNH ô
    đó vô hiệu hoá. Bảng cũng chỉ được soát trong đúng mục Bước 0′ sau khi bỏ
    code fence — một bảng "ví dụ" ở chỗ khác hoặc bảng thật bị bọc fence đều
    không phải thủ tục đang có hiệu lực. Điều kiện KÍCH HOẠT (`surface:
    cloud` mới chạy, `surface: local` thì không) cũng được kiểm theo CẶP GHÉP
    — cả hai giá trị đều có mặt ở cả hai chiều nên chỉ đếm có-mặt không phân
    biệt được cổng bị đảo hướng.
    """
    errors: list[str] = []

    # Markdown coi một newline đơn trong cùng đoạn văn là soft-break — hiển
    # thị ra khoảng trắng, không phải xuống dòng thật. co-mat-gate.md có câu
    # bị word-wrap giữa chừng một cụm bắt buộc; gộp mọi chuỗi khoảng trắng
    # (kể cả newline) về một dấu cách trước khi so khớp cho đúng cách người
    # đọc thấy, KHÔNG sửa nội dung file cho khớp regex.
    normalized = re.sub(r"\s+", " ", text)
    for phrase in GATE_OWNERSHIP_PHRASES:
        if phrase not in normalized:
            errors.append(f"co-mat-gate.md thiếu mệnh đề: {phrase!r}")

    # Điều kiện KÍCH HOẠT: một dòng phải ghép 'kích hoạt' với `surface:
    # cloud` (không phải local); một dòng khác phải ghép 'KHÔNG chạy' với
    # `surface: local` (không phải cloud). Kiểm CẶP GHÉP trên từng dòng,
    # không phải bốn chuỗi rời — nếu không thì đảo `cloud`⇄`local` giữa hai
    # dòng vẫn để cả bốn chuỗi có mặt đâu đó, lint không phân biệt được.
    lines = text.splitlines()
    activation_ok = any(
        _ACTIVATION_CUE in ln.lower()
        and "surface: cloud" in ln.lower()
        and "surface: local" not in ln.lower()
        for ln in lines
    )
    if not activation_ok:
        errors.append(
            "dòng kích hoạt cổng phải ghép 'Kích hoạt' với `surface: cloud` "
            "(không phải `surface: local`)"
        )
    deactivation_ok = any(
        _DEACTIVATION_CUE in ln.lower()
        and "surface: local" in ln.lower()
        and "surface: cloud" not in ln.lower()
        for ln in lines
    )
    if not deactivation_ok:
        errors.append(
            "dòng 'KHÔNG chạy' phải ghép với `surface: local` "
            "(không phải `surface: cloud`)"
        )

    rows = parse_gate_table_rows(text)
    if len(rows) != 3:
        errors.append(f"bảng phân loại Bước 0′ phải có đúng 3 hàng, thấy {len(rows)}")
        return errors  # khung bảng đã sai thì không còn gì để so quan hệ

    secret_rows = [r for r in rows if "bí mật nhà nước" in r[0].lower()]
    unknown_rows = [r for r in rows if "chưa rõ" in r[0].lower()]
    na_rows = [r for r in rows if "không thuộc" in r[0].lower()]

    for label, matches in (
        ("bí mật nhà nước", secret_rows),
        ("Chưa rõ", unknown_rows),
        ("Không thuộc", na_rows),
    ):
        if len(matches) != 1:
            errors.append(
                f"bảng phân loại phải có đúng 1 hàng khớp {label!r}, thấy {len(matches)}"
            )

    if len(secret_rows) == 1:
        _, xu = secret_rows[0]
        if not _has_effective(xu, "dừng", reject_continue=True):
            errors.append(
                "hàng bí mật nhà nước: cột Xử phải mang DỪNG có hiệu lực "
                "(không bị phủ định/gắn ngoại lệ trong chính ô đó)"
            )

    if len(unknown_rows) == 1:
        _, xu = unknown_rows[0]
        if not _has_effective(xu, "coi như thuộc", reject_continue=True):
            errors.append("hàng Chưa rõ: cột Xử phải mang 'coi như thuộc' có hiệu lực")
        if not _has_effective(xu, "dừng", reject_continue=True):
            errors.append("hàng Chưa rõ: cột Xử phải mang DỪNG có hiệu lực")

    if len(na_rows) == 1:
        _, xu = na_rows[0]
        if _has_effective(xu, "dừng"):
            errors.append("hàng Không thuộc: cột Xử KHÔNG được mang DỪNG có hiệu lực")

    return errors
