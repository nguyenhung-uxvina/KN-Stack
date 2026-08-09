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
# xoá rồi viết lại bằng chữ khác, việc soát vùng đóng băng bên dưới không với
# tới.
GATE_OWNERSHIP_PHRASES = [
    "Điều 60.2",
    "quyết định của CEO, không phải kết luận pháp lý",
]

# ═══════════════════════════════════════════════════════════════════════════
# ĐÓNG BĂNG NGUYÊN VĂN. co-mat-gate.md là cổng an ninh trung tâm — nội dung
# của nó đã được CEO duyệt và đóng băng byte-identical (xem task-3-report.md,
# vòng sửa 1 và 2). Hai hằng số dưới đây lấy TRỰC TIẾP từ bản đã duyệt đó.
#
# lint_gate_doc SO KHỚP TOÀN VÙNG với hai hằng này — không phân tích ngữ
# nghĩa, không đoán "diễn đạt lại có lành tính hay không". Vòng review trước
# thử một danh sách "cue phủ định" để phân biệt hai thứ đó (_NEGATION_CUES,
# _has_effective — đã XOÁ); không có regex nào làm được việc phân biệt ngữ
# nghĩa đó, và 14/15 đột biến mới của vòng review kế tiếp phá được nó
# (thêm 2 dấu `*`, chèn chữ giữa cue, bỏ dấu tiếng Việt, nới lỏng mệnh lệnh,
# fence `~~~`, thụt lề 4 dấu cách, chèn thêm dòng ngoại lệ...). Danh sách từ
# cấm không bao giờ đóng được lớp lỗi này — chỉ so khớp NGUYÊN VĂN mới đóng
# được.
#
# Muốn đổi nội dung cổng: sửa CẢ HAI file cùng lúc (co-mat-gate.md + hai hằng
# số này) — đó phải là hành vi CỐ Ý của người duyệt, không phải trượt qua
# lint.
# ═══════════════════════════════════════════════════════════════════════════

# Nguyên khối 2 dòng kích hoạt/tắt — từ sau tiêu đề `# Cổng phân loại…` đến
# trước heading `## Vì sao…`.
GATE_ACTIVATION_CANON = (
    "> Kích hoạt: chỉ khi profile workspace đang bật khai `surface: cloud`.\n"
    "> Ở `surface: local` cổng này KHÔNG chạy, hành vi pipeline giữ nguyên như cũ."
)

# 3 hàng bảng của mục `## Bước 0′…`, ĐÚNG THỨ TỰ: (cột Phân loại, cột Xử).
GATE_TABLE_CANON: list[tuple[str, str]] = [
    (
        "Thuộc / nghi thuộc **bí mật nhà nước — bí mật quân sự**",
        "**DỪNG.** Không xử nội dung, không tóm tắt, không diễn giải. Chỉ CEO quay về **Claude Code local** (đổi `active-workspace.md` sang `workspace-knstack.md`).",
    ),
    (
        "**Chưa rõ** — chưa có văn bản xác định",
        "**coi như thuộc** → **DỪNG.** Bám đúng nguyên tắc `ip-dossier` đã có: *\"Chưa có văn bản xác định bí mật nhà nước ⇒ coi như CHƯA RÕ\"*. Mặc định thận trọng, nên bấm bừa không mở được cổng.",
    ),
    (
        "**Không thuộc** — dân dụng, hoặc lưỡng dụng đã tách phần MẬT, hoặc đã khóa priority date",
        "Chạy tiếp.",
    ),
]

_TABLE_SEP_RE = re.compile(r"^:?-+:?$")

# Fence backtick (```) hoặc dấu ngã (~~~) — \1 buộc mở/đóng cùng kiểu, đúng
# quy tắc CommonMark. Nội dung trong đó không render thành bảng/đoạn văn
# Markdown thật, dù đang bọc bảng thật (làm mất hiệu lực) hay chứa bảng "ví
# dụ" dán thêm (không phải thủ tục thật).
_FENCE_RE = re.compile(r"^(```|~~~)[^\n]*\n.*?\n\1[ \t]*$", re.MULTILINE | re.DOTALL)

# Bảng 3 ngả chỉ có hiệu lực trong đúng mục Bước 0′ — một bảng/danh sách khác
# hình dạng ở heading khác trong file không phải là thủ tục thật đang chạy.
_STEP0_SECTION_RE = re.compile(r"^##[ \t]*Bước 0′.*?(?=^##[ \t]|\Z)", re.MULTILINE | re.DOTALL)

# Heading H1 đầu file, dùng để cắt vùng kích hoạt (giữa H1 và H2 đầu tiên).
# `[ \t]+` sau `#` loại trừ heading H2 (`##…`) — sau "##" ký tự kế tiếp là
# "#" chứ không phải khoảng trắng nên không khớp nhầm.
_ACTIVATION_SECTION_RE = re.compile(r"^#[ \t]+.*?\n(.*?)(?=^##[ \t])", re.MULTILINE | re.DOTALL)


def _strip_code_fences(text: str) -> str:
    """Bỏ nội dung không render thành Markdown thường: code fence backtick
    (```) hoặc dấu ngã (~~~), VÀ khối thụt lề ≥4 dấu cách/tab (indented code
    block — CommonMark coi đây cũng là code, không phải bảng hay đoạn văn
    thật). Áp dụng cho cả vùng kích hoạt lẫn vùng bảng.
    """
    text = _FENCE_RE.sub("", text)
    lines = text.split("\n")
    kept = [ln for ln in lines if not (ln.startswith("    ") or ln.startswith("\t"))]
    return "\n".join(kept)


def _extract_step0_section(text: str) -> str:
    """Phần dưới heading '## Bước 0′…' đến heading `##` kế tiếp (hoặc hết file)."""
    m = _STEP0_SECTION_RE.search(text)
    return m.group(0) if m else ""


def _extract_activation_region(text: str) -> str:
    """Phần giữa tiêu đề H1 đầu file và heading H2 đầu tiên (`## Vì sao…`)."""
    m = _ACTIVATION_SECTION_RE.search(text)
    return m.group(1).strip("\n") if m else ""


def _normalize_ws(s: str) -> str:
    """Gộp mọi chuỗi khoảng trắng (kể cả newline) về một dấu cách, rồi bỏ hai
    đầu. Markdown coi một newline đơn trong cùng đoạn văn là soft-break — chỉ
    hiển thị ra khoảng trắng, không phải xuống dòng thật — nên so khớp
    nguyên văn phải gộp theo đúng cách người đọc thấy, KHÔNG sửa nội dung
    file cho khớp regex.
    """
    return re.sub(r"\s+", " ", s).strip()


def _shorten(s: str, limit: int = 160) -> str:
    return s if len(s) <= limit else s[:limit] + "…"


def parse_gate_table_rows(text: str) -> list[tuple[str, str]]:
    """Hàng thô `| Phân loại | Xử |` của bảng Bước 0′, GIỮ hàng trùng và thứ tự.

    Chỉ quét bên trong mục '## Bước 0′…', sau khi đã bỏ mọi code fence/khối
    thụt lề (xem `_extract_step0_section` / `_strip_code_fences`) — một bảng
    "ví dụ" dán ở heading khác hoặc trong fence, hoặc bảng thật bị bọc để
    không còn render, đều không được tính là hàng thật. Bỏ header (`Phân
    loại`) và hàng phân cách markdown (`|---|---|`). Không gom dict — cùng lý
    do `parse_workspace_rows` không gom: gom sẽ nuốt hàng trùng hoặc hàng
    thiếu, làm phép đếm "đúng N hàng" phía dưới vô hiệu.
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


def lint_gate_doc(text: str) -> list[str]:
    """Phát hiện co-mat-gate.md đã TRÔI khỏi bản CEO đã duyệt.

    Phạm vi thật của hàm này, nói rõ để không hứa quá: nó KHÔNG hiểu nghĩa
    tiếng Việt và KHÔNG tự phán được một diễn đạt mới là lành tính hay đảo
    nghĩa — việc đó thuộc về người duyệt, tại thời điểm họ cố ý cập nhật
    `GATE_ACTIVATION_CANON` / `GATE_TABLE_CANON` cùng lúc với sửa tài liệu.
    Việc hàm này làm chỉ đơn giản là SO KHỚP TOÀN VÙNG: vùng kích hoạt và
    từng hàng bảng phải BẰNG (sau khi gộp khoảng trắng) đúng hằng số đã đóng
    băng — thừa/thiếu/hoán vị/sửa một chữ đều là "trôi khỏi bản duyệt" và bị
    báo lỗi, bất kể nội dung mới nghe có hợp lý đến đâu.

    Vì sao đi theo hướng này thay vì phân tích ngữ nghĩa: `evals/ip-invent.
    json` ghi một mutation test đã bắt được IP-DISCLOSE từng là cổng-đếm-từ-
    khoá bị đảo nghĩa vẫn xanh. Vòng vá đầu của chính lint này thử thu hẹp
    phép đếm-từ-khoá xuống một ô (`_has_effective`) — vẫn bị phá (14/15 đột
    biến: thêm `**`, chèn chữ giữa cue, bỏ dấu, nới lỏng mệnh lệnh, đổi kiểu
    fence, thụt lề, chèn dòng ngoại lệ). Không có danh sách từ cấm nào đóng
    được lớp lỗi "diễn đạt lại" — chỉ so khớp nguyên văn mới đóng được, vì nó
    không cố phân biệt "lành tính" với "đảo nghĩa", nó chỉ hỏi "có đổi không".
    """
    errors: list[str] = []

    normalized = _normalize_ws(text)
    for phrase in GATE_OWNERSHIP_PHRASES:
        if phrase not in normalized:
            errors.append(f"co-mat-gate.md thiếu mệnh đề: {phrase!r}")

    fence_free = _strip_code_fences(text)

    activation_seen = _normalize_ws(_extract_activation_region(fence_free))
    activation_want = _normalize_ws(GATE_ACTIVATION_CANON)
    if activation_seen != activation_want:
        errors.append(
            "vùng kích hoạt cổng lệch khỏi bản đã duyệt (co-mat-gate.md đã trôi khỏi "
            "canon — nếu đổi có chủ đích, cập nhật GATE_ACTIVATION_CANON cùng lúc). "
            f"Mong đợi: {_shorten(activation_want)!r} | Thấy: {_shorten(activation_seen)!r}"
        )

    rows = parse_gate_table_rows(text)
    if len(rows) != len(GATE_TABLE_CANON):
        errors.append(
            f"bảng phân loại Bước 0′ phải có đúng {len(GATE_TABLE_CANON)} hàng khớp "
            f"bản đã duyệt, thấy {len(rows)} hàng"
        )
        return errors  # khung bảng đã sai thì không còn gì để so nguyên văn

    for i, ((got_c1, got_c2), (want_c1, want_c2)) in enumerate(zip(rows, GATE_TABLE_CANON), start=1):
        got_c1n, got_c2n = _normalize_ws(got_c1), _normalize_ws(got_c2)
        want_c1n, want_c2n = _normalize_ws(want_c1), _normalize_ws(want_c2)
        if got_c1n != want_c1n:
            errors.append(
                f"hàng {i} cột Phân loại lệch bản đã duyệt "
                f"(Mong đợi: {_shorten(want_c1n)!r} | Thấy: {_shorten(got_c1n)!r})"
            )
        if got_c2n != want_c2n:
            errors.append(
                f"hàng {i} cột Xử lệch bản đã duyệt "
                f"(Mong đợi: {_shorten(want_c2n)!r} | Thấy: {_shorten(got_c2n)!r})"
            )

    return errors
