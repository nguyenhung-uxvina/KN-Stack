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


def parse_gate_table_rows(text: str) -> list[tuple[str, str]]:
    """Hàng thô `| Phân loại | Xử |` của bảng Bước 0′, GIỮ hàng trùng và thứ tự.

    Bỏ header (`Phân loại`) và hàng phân cách markdown (`|---|---|`). Không
    gom dict — cùng lý do parse_workspace_rows không gom: gom sẽ nuốt hàng
    trùng hoặc hàng thiếu, làm phép đếm "đúng 3 hàng" phía dưới vô hiệu.
    """
    rows: list[tuple[str, str]] = []
    for line in text.splitlines():
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


def lint_gate_doc(text: str) -> list[str]:
    """Kiểm co-mat-gate.md bằng QUAN HỆ giữa ô với ô của bảng 3 ngả, không
    phải bằng việc đếm token có mặt ở đâu đó trong file.

    Vì sao đổi cách kiểm: `evals/ip-invent.json` (trường description) ghi
    nguyên văn một mutation test đã bắt được IP-DISCLOSE từng là cổng-đếm-từ-
    khoá — một cổng bộc lộ bị ĐẢO NGHĨA vẫn xanh vì các token rải rác nơi khác
    thoả mãn phép match không giới hạn. Kiểm có-mặt chuỗi chỉ chặn được XOÁ,
    không chặn được ĐẢO NGHĨA. Bảng 3 ngả ở đây là chỗ đảo-nghĩa nguy hiểm
    nhất trong tài liệu (một hàng bị đổi Xử là đổi hành vi cổng), nên nó phải
    được chấm theo quan hệ cột-với-cột của TỪNG hàng.
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
        if "dừng" not in xu.lower():
            errors.append("hàng bí mật nhà nước: cột Xử phải mang DỪNG")

    if len(unknown_rows) == 1:
        _, xu = unknown_rows[0]
        if "coi như thuộc" not in xu.lower():
            errors.append("hàng Chưa rõ: cột Xử phải mang 'coi như thuộc'")
        if "dừng" not in xu.lower():
            errors.append("hàng Chưa rõ: cột Xử phải mang DỪNG")

    if len(na_rows) == 1:
        _, xu = na_rows[0]
        if "dừng" in xu.lower():
            errors.append("hàng Không thuộc: cột Xử KHÔNG được mang DỪNG")

    return errors
