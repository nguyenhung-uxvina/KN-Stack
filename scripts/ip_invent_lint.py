"""Linter giữ tầng tham chiếu dùng chung của plugin ip-invent khớp nhau.

Nằm ngoài plugin (plugin phải thuần Markdown + JSON để Cowork nạp được).
"""
from __future__ import annotations

import hashlib
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

GATE_DOC_NAME = "co-mat-gate.md"
GATE_DOC_PATH = REF_DIR / GATE_DOC_NAME
GATE_DOC_REPO_PATH = "plugins/ip-invent/skills/ip-shared/references/co-mat-gate.md"

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


# ═══════════════════════════════════════════════════════════════════════════
# CỔNG: ĐÓNG BĂNG CẢ FILE co-mat-gate.md BẰNG SHA-256
#
# co-mat-gate.md là cổng an ninh trung tâm của plugin — nó quyết định nội dung
# sáng chế nào được phép xử trên bề mặt cloud và nội dung nào phải DỪNG. Nội
# dung đã được CEO duyệt và đóng băng byte-identical.
#
# Vì sao đóng băng CẢ FILE chứ không chỉ hai vùng "có hiệu lực":
#
#   Ba vòng trước lần lượt canh (1) có-mặt-từ-khoá, (2) nguyên văn HAI VÙNG
#   (khối kích hoạt + 3 hàng bảng `## Bước 0′`), (3) thêm chốt cú pháp cho
#   fence hở và heading `## Bước 0` trùng. Cả ba đều bị phá, và luôn theo cùng
#   một khuôn: kẻ tấn công KHÔNG sửa vùng được canh, mà đưa vùng thật ra ngoài
#   tầm soát hoặc dựng một vùng thứ hai có hiệu lực render — fence hở thụt một
#   dấu cách, heading `### Bước 0″`, heading setext (`Bước 0″` + `====`), hàng
#   bảng thứ tư 3 ô hoặc thiếu pipe biên, H1 mồi đặt đầu file. Mỗi lần vá một
#   khuôn cú pháp thì có khuôn cú pháp khác cho cùng hậu quả render, vì thứ có
#   hiệu lực là KẾT QUẢ RENDER chứ không phải bề mặt cú pháp. Và mọi đòn còn
#   lại sống trong phần văn xuôi mà thiết kế hai-vùng cố ý để trống.
#
#   Ranh giới "vùng có hiệu lực / phần còn lại tự do" CHÍNH LÀ bề mặt tấn
#   công. Bỏ ranh giới đó đi thì không còn chỗ nào để trốn: mọi byte của tài
#   liệu đều nằm trong hash.
#
# Chuẩn hoá trước khi băm là BẮT BUỘC, không phải trang trí: repo chạy trên
# Windows với `core.autocrlf=true`, nên cùng một nội dung có CRLF trên đĩa và
# LF trong git blob. Không chuẩn hoá thì hằng số trôi theo checkout.
# ═══════════════════════════════════════════════════════════════════════════

# SHA-256 của TOÀN BỘ co-mat-gate.md, tính trên nội dung đã bỏ BOM và chuẩn
# hoá mọi xuống dòng về "\n" (xem `_normalize_doc` / `gate_doc_digest`).
# Trùng đúng hash của git blob: `git show HEAD:<path> | sha256sum`.
GATE_DOC_SHA256 = "f91286a0af3a97e8f19deb126e091e9f1627d135d1a6efcb2fd0974bb268f872"

# ── Tầng CHẨN ĐOÁN (không phải cổng) ───────────────────────────────────────
# Ba hằng dưới đây KHÔNG quyết định đạt/không đạt — `GATE_DOC_SHA256` làm việc
# đó một mình. Chúng chỉ tồn tại để khi hash lệch, thông điệp lỗi nói được
# *dòng nào* và *vùng nào* đã trôi, thay vì "file đổi rồi, tự tìm đi".
#
# `GATE_DOC_CANON` là bản đã duyệt nguyên văn, dùng để chỉ ra dòng đầu tiên
# khác nhau (hash không tự khôi phục được nội dung mong đợi).
# `GATE_ACTIVATION_CANON` / `GATE_TABLE_CANON` đặt TÊN cho hai vùng nghiệp vụ
# quan trọng nhất — cái mà `GATE_DOC_CANON` không tự nói ra được.
#
# `_check_diagnostic_layer_is_consistent` buộc ba hằng này khớp nhau và khớp
# `GATE_DOC_SHA256`; cập nhật một cái mà quên cái kia thì lint báo lỗi cấu
# hình ngay, không im lặng chẩn đoán sai.

GATE_DOC_CANON = """# Cổng phân loại — chạy khi `surface: cloud`

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
"""

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


def _normalize_doc(text: str) -> str:
    """Bỏ BOM và đưa mọi xuống dòng về "\\n" — KHÔNG đụng gì khác.

    Đây là toàn bộ phép chuẩn hoá trước khi băm. Cố ý hẹp: nó chỉ trung hoà
    hai thứ mà công cụ (git autocrlf, editor Windows) tự ý đổi sau lưng người
    duyệt. Mọi khác biệt còn lại — kể cả một khoảng trắng cuối dòng — vẫn là
    "tài liệu đã đổi".
    """
    if text.startswith("\ufeff"):  # BOM
        text = text[1:]
    return text.replace("\r\n", "\n").replace("\r", "\n")


def gate_doc_digest(text: str) -> str:
    """SHA-256 của co-mat-gate.md sau `_normalize_doc`, dạng hex thường."""
    return hashlib.sha256(_normalize_doc(text).encode("utf-8")).hexdigest()


def _normalize_ws(s: str) -> str:
    """Gộp mọi chuỗi khoảng trắng (kể cả newline) về một dấu cách, rồi bỏ hai
    đầu. CHỈ dùng cho tầng chẩn đoán (dò xem vùng nào còn nguyên chữ), KHÔNG
    dùng cho phép so hash — hash so nguyên văn, không nới lỏng gì.
    """
    return re.sub(r"\s+", " ", s).strip()


def _shorten(s: str, limit: int = 160) -> str:
    return s if len(s) <= limit else s[:limit] + "…"


def _first_differing_line(got: str, want: str) -> tuple[int, str, str]:
    """(số dòng 1-based, dòng mong đợi, dòng thấy) ở chỗ khác nhau đầu tiên.

    Khi một bên hết dòng trước, phần thiếu hiện ra là `<không có dòng này>`.
    """
    absent = "<không có dòng này>"
    got_lines = got.split("\n")
    want_lines = want.split("\n")
    for i in range(max(len(got_lines), len(want_lines))):
        g = got_lines[i] if i < len(got_lines) else absent
        w = want_lines[i] if i < len(want_lines) else absent
        if g != w:
            return i + 1, w, g
    return 0, "", ""  # không có khác biệt — người gọi đã kiểm hash trước


def _drifted_regions(text: str) -> list[str]:
    """Vùng nào của tài liệu đã trôi — CHẨN ĐOÁN, không phải phán quyết.

    Chỉ dò xem chữ nguyên văn của từng vùng còn xuất hiện đúng MỘT lần trong
    tài liệu hay không (sau khi gộp khoảng trắng, vì Markdown word-wrap giữa
    chừng một câu là soft-break). Không xuất hiện = vùng đó bị sửa/xoá; xuất
    hiện nhiều hơn một lần = có bản sao mồi ở đâu đó. Cả hai đều đáng nói ra.
    """
    hay = _normalize_ws(text)
    regions: list[str] = []

    n = hay.count(_normalize_ws(GATE_ACTIVATION_CANON))
    if n == 0:
        regions.append("khối kích hoạt (chữ đã đổi hoặc bị xoá)")
    elif n > 1:
        regions.append(f"khối kích hoạt (xuất hiện {n} lần — có bản sao mồi)")

    for i, (c1, c2) in enumerate(GATE_TABLE_CANON, start=1):
        n1 = hay.count(_normalize_ws(c1))
        n2 = hay.count(_normalize_ws(c2))
        if n1 == 0 or n2 == 0:
            regions.append(f"bảng Bước 0′ hàng {i} (chữ đã đổi hoặc bị xoá)")
        elif n1 > 1 or n2 > 1:
            regions.append(f"bảng Bước 0′ hàng {i} (xuất hiện >1 lần — có bản sao mồi)")

    if not regions:
        regions.append(
            "phần văn xuôi ngoài khối kích hoạt và bảng Bước 0′ "
            "(hai vùng đó còn nguyên chữ)"
        )
    return regions


def _check_diagnostic_layer_is_consistent() -> list[str]:
    """Ba hằng chẩn đoán phải khớp nhau và khớp GATE_DOC_SHA256.

    Chặn đúng một lớp lỗi: người duyệt sửa tài liệu rồi cập nhật hằng này mà
    quên hằng kia. Đây là lỗi CẤU HÌNH của linter, khác hẳn "tài liệu đã trôi".
    """
    errors: list[str] = []
    if gate_doc_digest(GATE_DOC_CANON) != GATE_DOC_SHA256:
        errors.append(
            "LỖI CẤU HÌNH linter: GATE_DOC_CANON không băm ra GATE_DOC_SHA256 — "
            "ai đó đã cập nhật một hằng mà quên hằng kia trong scripts/ip_invent_lint.py. "
            "Sửa cả hai cho khớp bản CEO đã duyệt trước khi tin bất kỳ kết quả lint nào."
        )
    canon_ws = _normalize_ws(GATE_DOC_CANON)
    if _normalize_ws(GATE_ACTIVATION_CANON) not in canon_ws:
        errors.append(
            "LỖI CẤU HÌNH linter: GATE_ACTIVATION_CANON không nằm trong GATE_DOC_CANON."
        )
    for i, (c1, c2) in enumerate(GATE_TABLE_CANON, start=1):
        if _normalize_ws(c1) not in canon_ws or _normalize_ws(c2) not in canon_ws:
            errors.append(
                f"LỖI CẤU HÌNH linter: GATE_TABLE_CANON hàng {i} không nằm trong GATE_DOC_CANON."
            )
    return errors


def lint_gate_doc(text: str) -> list[str]:
    """Phát hiện co-mat-gate.md đã đổi so với bản CEO đã duyệt. Rỗng = y nguyên.

    CÁCH LÀM: băm SHA-256 TOÀN BỘ tài liệu (sau khi bỏ BOM và đưa xuống dòng
    về "\\n") rồi so với hằng `GATE_DOC_SHA256`. Không có vùng nào được miễn:
    tiêu đề, văn xuôi, bảng, khoảng trắng cuối dòng — tất cả nằm trong hash.

    PHẠM VI — nói đủ, không hứa quá và không hứa thiếu:

    - Hàm này bắt MỌI thay đổi, kể cả sửa một lỗi chính tả hay thêm một dấu
      cách. Đó là chủ ý: ba vòng thiết kế trước đều thất bại vì cố phân biệt
      "vùng có hiệu lực" với "phần còn lại tự do", và mỗi lần khoanh vùng lại
      đẻ ra một chỗ trốn mới (fence hở thụt lề, heading `### Bước 0″`, heading
      setext, hàng bảng 3 ô, H1 mồi). Đóng băng cả file làm chỗ trốn biến mất.
    - Hàm này KHÔNG hiểu nghĩa tiếng Việt và KHÔNG phán được một thay đổi là
      lành tính (sửa chính tả) hay đảo nghĩa (vô hiệu hoá cổng). Nó chỉ trả
      lời đúng một câu hỏi: "có đổi không?". Việc phân định lành tính / đảo
      nghĩa thuộc về NGƯỜI DUYỆT, tại thời điểm họ cố ý cập nhật hằng số.
    - Hàm này không kiểm tài liệu có được skill nào thực sự đọc hay không, và
      không thay được việc đọc nội dung khi duyệt.

    HỆ QUẢ VẬN HÀNH: sửa cổng = sửa HAI FILE CÙNG LÚC, có chủ đích —
    `co-mat-gate.md` và `scripts/ip_invent_lint.py` (`GATE_DOC_SHA256` +
    `GATE_DOC_CANON`). Không còn đường sửa tài liệu mà lint vẫn xanh; mọi
    thay đổi cổng đều để lại dấu vết trong diff của cả hai file, kèm lý do
    trong commit message.

    Khi hash lệch, hàm trả về ĐÚNG MỘT lỗi, mang đủ thứ để hành động: vùng
    trôi (`_drifted_regions` — tầng chẩn đoán, xem `GATE_DOC_CANON` /
    `GATE_ACTIVATION_CANON` / `GATE_TABLE_CANON`), dòng đầu tiên khác nhau
    kèm bản mong đợi và bản thấy, và hai đường xử.
    """
    config_errors = _check_diagnostic_layer_is_consistent()
    if config_errors:
        return config_errors

    seen_digest = gate_doc_digest(text)
    if seen_digest == GATE_DOC_SHA256:
        return []

    lineno, want_line, got_line = _first_differing_line(
        _normalize_doc(text), GATE_DOC_CANON
    )
    regions = " · ".join(_drifted_regions(text))

    return [
        f"{GATE_DOC_NAME} đã ĐỔI so với bản CEO đã duyệt "
        f"(SHA-256 thấy {seen_digest}, GATE_DOC_SHA256 mong đợi {GATE_DOC_SHA256}).\n"
        f"  Vùng trôi: {regions}\n"
        f"  Khác nhau đầu tiên ở dòng {lineno}:\n"
        f"    Mong đợi: {_shorten(want_line)!r}\n"
        f"    Thấy:     {_shorten(got_line)!r}\n"
        f"  Xử — nếu ĐỔI CÓ CHỦ ĐÍCH: cập nhật GATE_DOC_SHA256 và GATE_DOC_CANON trong "
        f"scripts/ip_invent_lint.py CÙNG LÚC với sửa tài liệu, và ghi lý do đổi cổng vào "
        f"commit message (đổi cổng phải là hành vi cố ý, có người duyệt).\n"
        f"  Xử — nếu KHÔNG CHỦ ĐÍCH: hoàn nguyên tài liệu về bản đã duyệt "
        f"(`git checkout -- {GATE_DOC_REPO_PATH}`)."
    ]


# ═══════════════════════════════════════════════════════════════════════════
# KHỐI "⛔ BƯỚC 0′" — ĐÓNG BĂNG NGUYÊN VĂN, LẶP CHỦ Ý QUA 6 SKILL.MD
#
# Kế hoạch gốc (task-4-brief.md) định kiểm khối này bằng "cụm bắt buộc có mặt
# trong file" (SKILL_REQUIRED_PHRASES + lint_skill_header) — đúng khuôn mà
# `lint_gate_doc` đã thử ở vòng 1 cho co-mat-gate.md và thua ba vòng liên
# tiếp: bị phá bằng phủ định trong câu ("**KHÔNG DỪNG.**" vẫn chứa từ khoá
# "DỪNG"), bằng cách đưa vùng ra ngoài tầm soát (mục "Bước 0" thứ hai, fence
# hở), rồi bằng đúng một ký tự khi chốt cú pháp được vá. Bài học của vòng 4 ở
# `lint_gate_doc` là: bỏ hẳn khái niệm "cụm bắt buộc" / "vùng có hiệu lực",
# đóng băng NGUYÊN VĂN rồi so sánh chính xác. Khối Bước 0′ áp thẳng kết luận
# đó — không đi lại con đường cụm-từ, dù brief gốc có viết sẵn.
#
# KHÁC VỚI `lint_gate_doc`: `lint_gate_doc` băm CẢ FILE co-mat-gate.md (file
# đó CHỈ chứa nội dung cổng, không có gì khác). Khối Bước 0′ chỉ là MỘT ĐOẠN
# bên trong một SKILL.md lớn hơn nhiều — phần còn lại của mỗi SKILL.md (mô tả
# block, bảng nghiệp vụ, COD, Rules, …) KHÔNG thuộc phạm vi đóng băng này và
# được sửa tự do. Vì vậy phép kiểm ở đây là "khối này có xuất hiện ĐÚNG MỘT
# LẦN, NGUYÊN VĂN, như một đoạn con của file" — dùng đếm số lần xuất hiện của
# `STEP0_BLOCK_CANON` như một substring, KHÔNG băm cả file.
#
# VÌ SAO TRÙNG LẶP QUA 6 FILE LÀ CỐ Ý, KHÔNG PHẢI MÙI XẤU: Markdown SKILL.md
# không có cơ chế `include`/`import`; mỗi skill được nạp và chạy độc lập qua
# junction, và trong Cowork mỗi skill cũng phải tự chứa (không có quyền đọc
# skill khác lúc runtime). CEO đã chốt giữ nguyên trùng lặp — đổi lại lint
# phải bắt được SÁU BẢN SAO lệch nhau. `lint_blocks_identical` biến trùng lặp
# thành một BẤT BIẾN KIỂM ĐƯỢC, không phải một khoản nợ kỹ thuật bị lờ đi.
# ═══════════════════════════════════════════════════════════════════════════

# Nguyên văn khối "Bước 0′" — chép TỪNG KÝ TỰ từ bản CEO đã duyệt
# (.superpowers/sdd/2026-08-08-ip-invent-plugin/task-4-brief.md, Bước 4).
# Đây là NGUỒN CHUẨN DUY NHẤT; sáu SKILL.md mang bản sao byte-identical của nó.
STEP0_BLOCK_CANON = """## ⛔ BƯỚC 0′ — đọc workspace TRƯỚC MỌI VIỆC KHÁC

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
`1b chạy KHÔNG có TRIZ`). Cấm im lặng bỏ qua rồi vẫn in báo cáo trông đầy đủ."""

# Dòng đầu tiên của khối — dùng làm mốc để CHẨN ĐOÁN (dò khối gần giống khi so
# nguyên văn thất bại). KHÔNG dùng cho phép ĐẠT/KHÔNG ĐẠT — phép đó chỉ đếm số
# lần STEP0_BLOCK_CANON xuất hiện nguyên văn.
_STEP0_FIRST_LINE = STEP0_BLOCK_CANON.splitlines()[0]

# Ranh giới "hết khối" dùng cho CHẨN ĐOÁN: heading `##` kế tiếp, hoặc hết file.
_NEXT_MD_HEADING_RE = re.compile(r"\n##[ \t]")

# ── NEO VỊ TRÍ (vá vòng 2, R1/Q1 — hậu tố GỠ Ở VÒNG 3, xem dưới) ────────────
#
# Vòng 1 chỉ đếm `STEP0_BLOCK_CANON` như một substring bất kỳ đâu trong file —
# đúng lớp lỗi X14/X16/N11/N12 đã hạ Task 3 ba vòng: bọc khối trong fence
# (đóng/hở), bọc `<!-- -->`, dời khối xuống cuối file, hay chèn văn xuôi
# trước khối đều để nguyên văn khối còn đó — `count() == 1` vẫn đúng, nên vòng
# 1 xanh oan. Vòng 2 thêm NEO-ĐẦU: khối không chỉ phải tồn tại đúng 1 lần, nó
# còn phải BẮT ĐẦU đúng offset ngay sau tiền tố frontmatter+H1.
#
# Tiền tố (đo được, giống hệt cho cả 6 file thật): `---\n<frontmatter>\n---\n\n
# # <tiêu đề H1>\n\n`. Việc bọc khối trong fence/comment, hay dời nó đi nơi
# khác, đều chèn thêm ký tự vào khoảng "tiền tố → khối" — lệch offset bắt đầu,
# bắt được ngay. Đặt khối trước cả tiêu đề H1 (hoặc trước cả frontmatter) làm
# CHÍNH tiền tố không còn khớp mẫu ở đầu file — cũng bắt được, theo một nhánh
# riêng (không xác định được neo).
#
# VÒNG 2 từng thêm một NEO-CUỐI (`_SUFFIX_ANCHOR = "\n\n> "`) để bắt ca "chèn
# văn xuôi vô hiệu hoá NGAY SAU khối" — ca duy nhất neo-đầu một mình bỏ lọt.
# VÒNG 3 GỠ neo-cuối đó: người soát chỉ ra nó là CHỐT GIẢ — chuỗi "\n\n> " chỉ
# 3 ký tự, kẻ tấn công tự viết ra được, nên dùng chính "\n\n> " làm MỒI rồi
# nối tiếp đòn thật ngay sau (`"\n\n> **LƯU Ý:** ... KHÔNG bắt buộc thi hành."`,
# hay mồi "\n\n> " rồi mở fence/comment nuốt phần còn lại) — cả bốn biến thể
# đều XANH qua neo-cuối. Tệ hơn: neo-cuối tạo ĐÚNG MỘT ca đỏ giả trên nội dung
# HỢP LỆ — đổi đoạn ngay sau khối từ blockquote `>` sang một mục `##` mới (việc
# Task 5/6 rất có thể làm khi gỡ đường dẫn neo cứng) bị chẩn đoán sai thành
# "có fence/comment bọc quanh khối". Một chốt vừa không mua được an ninh thật
# (bẻ được bằng 2 ký tự) vừa tính phí thật ở task sau (đỏ giả) là chốt nên gỡ,
# không phải chốt nên giữ. Xem THẢO LUẬN GIỚI HẠN trong docstring
# `lint_skill_block` — "văn xuôi vô hiệu hoá ngay sau khối" quay lại thành một
# GIỚI HẠN CÓ TUYÊN BỐ, cùng lớp với "vô hiệu hoá ở cuối file" và "vô hiệu hoá
# trong `description:` frontmatter" — phần TỰ DO của SKILL.md mà lint này cố
# ý không đóng băng.
_PREFIX_ANCHOR_RE = re.compile(r"\A---\n.*?\n---\n\n# [^\n]+\n\n", re.DOTALL)


def _anchor_offset(norm_text: str) -> int | None:
    """Offset NGAY SAU tiền tố frontmatter+H1 hợp lệ ở đầu file — vị trí bắt
    buộc khối Bước 0′ phải bắt đầu tại đó. `None` nếu đầu file không khớp mẫu
    tiền tố (cấu trúc frontmatter/H1 đã bị xáo trộn — không có gì để neo vào).
    """
    m = _PREFIX_ANCHOR_RE.match(norm_text)
    return m.end() if m else None


def _position_ok(norm_text: str, block_start: int) -> bool:
    """Khối có bắt đầu ĐÚNG offset neo (ngay sau tiền tố frontmatter+H1)
    không. CHỈ neo-đầu — không còn neo-cuối (gỡ ở vòng 3, xem comment trên).
    """
    anchor = _anchor_offset(norm_text)
    return anchor is not None and block_start == anchor


def _position_error(norm_text: str, block_start: int) -> str:
    """Dựng thông điệp lỗi vị trí — luôn nói rõ CÁI GÌ đang chen vào hoặc khối
    đang ở đâu, và cách xử. Chỉ gọi khi đã biết `not _position_ok(...)`.
    """
    anchor = _anchor_offset(norm_text)

    if anchor is None:
        return (
            "khối '⛔ BƯỚC 0′' có nội dung nguyên văn đúng NHƯNG cấu trúc đầu file "
            "(frontmatter YAML + dòng tiêu đề `# <tên skill> — …`) không khớp mẫu bắt buộc "
            "ngay tại đầu file, nên không xác định được vị trí neo để so.\n"
            "  Xử: khôi phục frontmatter + dòng tiêu đề H1 nguyên bản ở đầu file, đặt khối "
            "Bước 0′ ngay sau dòng trống theo sau tiêu đề đó — không đặt khối trước H1 hay "
            "trước frontmatter."
        )

    if block_start > anchor:
        between = _shorten(norm_text[anchor:block_start])
        return (
            "khối '⛔ BƯỚC 0′' có nội dung nguyên văn đúng NHƯNG KHÔNG bắt đầu ngay sau "
            "frontmatter + tiêu đề H1 — có nội dung khác chen vào giữa (fence, HTML "
            "comment, hoặc bị dời sang vị trí khác trong file).\n"
            f"  Chen vào giữa (offset {anchor}→{block_start}): {between!r}\n"
            "  Xử: xoá phần chen vào / dời khối về lại đúng chỗ — ngay sau dòng trống "
            "theo sau tiêu đề H1, không có gì ở giữa."
        )
    return (
        "khối '⛔ BƯỚC 0′' có nội dung nguyên văn đúng NHƯNG nằm SAI VỊ TRÍ trong file "
        "— bắt đầu TRƯỚC điểm neo (ngay sau frontmatter + tiêu đề H1), ví dụ bị đặt "
        "trước cả tiêu đề H1.\n"
        "  Xử: dời khối về đúng vị trí — ngay sau dòng trống theo sau tiêu đề H1."
    )


def _extract_step0_candidate(norm_text: str) -> str | None:
    """Trích đoạn BẮT ĐẦU TỪ dòng tiêu đề Bước 0′ tới trước heading `##` kế
    tiếp (hoặc hết file). CHỈ dùng để dựng thông điệp CHẨN ĐOÁN khi so nguyên
    văn thất bại — không quyết định đạt/không đạt. `None` nghĩa là không tìm
    thấy cả dòng tiêu đề, tức khối đã bị xoá hẳn chứ không phải chỉ sửa.
    """
    idx = norm_text.find(_STEP0_FIRST_LINE)
    if idx == -1:
        return None
    m = _NEXT_MD_HEADING_RE.search(norm_text, idx + len(_STEP0_FIRST_LINE))
    end = m.start() if m else len(norm_text)
    return norm_text[idx:end].rstrip("\n")


def lint_skill_block(text: str) -> list[str]:
    """Kiểm một SKILL.md mang đúng MỘT bản sao NGUYÊN VĂN của STEP0_BLOCK_CANON,
    BẮT ĐẦU đúng vị trí (ngay sau frontmatter + tiêu đề H1).

    PHẠM VI — nói đủ, không hứa quá, không hứa thiếu:

    - Hàm này bắt MỌI thay đổi NGUYÊN VĂN của khối, kể cả sửa một lỗi chính tả
      hay thêm một dấu cách. Nó KHÔNG hiểu nghĩa tiếng Việt và KHÔNG phán được
      một thay đổi là lành tính (sửa chính tả) hay đảo nghĩa (làm "DỪNG" mất
      hiệu lực). Việc phân định đó thuộc về NGƯỜI DUYỆT, tại thời điểm họ cố ý
      cập nhật STEP0_BLOCK_CANON — cùng lý lẽ đã dùng cho `lint_gate_doc`.
    - Hàm này CŨNG bắt việc khối bị BỌC hoặc DỜI CHỖ TRƯỚC khối dù nội dung
      nguyên văn còn nguyên — xem khối "NEO VỊ TRÍ" phía trên hàm này (neo-đầu
      = khối phải bắt đầu đúng offset ngay sau tiền tố frontmatter+H1). Đây là
      vá vòng 2 sau khi người soát dựng 10 đột biến (bọc fence đóng/hở, bọc
      HTML comment, dời cuối file, đặt trước H1, bọc `~~gạch ngang~~`, bọc
      `<details>`) đều lọt qua vòng 1.
    - **GIỚI HẠN CÓ TUYÊN BỐ (vòng 3, không phải bug):** hàm này KHÔNG bắt một
      câu vô hiệu hoá được chèn vào PHẦN TỰ DO ngay SAU khối — ví dụ
      `"...(hết khối)...\n\n> BỎ QUA khối Bước 0′ ở trên.\n>\n> <intro gốc>"`,
      hay đặt câu vô hiệu hoá ở CUỐI FILE, hay nhét vào `description:` trong
      frontmatter. Vòng 2 từng thử một neo-cuối (`_SUFFIX_ANCHOR = "\n\n> "`)
      để đóng đúng lỗ này, nhưng đó là CHỐT GIẢ: chuỗi 3 ký tự `"\n\n> "` kẻ
      tấn công tự viết ra được và dùng làm MỒI (viết `"\n\n> "` rồi nối đòn
      thật ngay sau, hoặc mồi `"\n\n> "` rồi mở fence/comment nuốt phần còn
      lại) — không mua được an ninh thật. Nó còn tính phí thật: đổi hợp lệ nội
      dung ngay sau khối (vd Task 5/6 thêm một mục `##` mới ở đó) bị lint báo
      NHẦM là "bị fence/comment bọc quanh". Đã gỡ neo-cuối ở vòng 3.
    - **ĐỐI LẬP CÓ CHỦ ĐÍCH với `lint_gate_doc`:** `co-mat-gate.md` băm được
      CẢ FILE vì file đó CHỈ chứa nội dung cổng, không có phần tự do nào để
      giấu đòn. `SKILL.md` thì CÓ phần tự do lớn (mô tả block, bảng nghiệp vụ,
      Output, Gotchas, COD, Rules, …) — phần đó PHẢI sửa được tự do (Task 5/6
      sẽ sửa để gỡ đường dẫn neo cứng), nên không thể đóng băng cả file theo
      kiểu `lint_gate_doc`. Hàm này chỉ đóng băng NỘI DUNG + VỊ TRÍ BẮT ĐẦU của
      khối Bước 0′ — không đóng băng được toàn bộ SKILL.md, và một câu vô hiệu
      hoá đặt trong phần tự do đó sẽ không bị bắt. Đây là ranh giới phạm vi cố
      ý, không phải lỗ hổng bị bỏ sót.
    - Hàm này không kiểm khối có thực sự được model đọc/tuân theo hay không;
      nó chỉ kiểm văn bản trên đĩa.

    HỆ QUẢ VẬN HÀNH: sửa khối Bước 0′ = sửa BẢY CHỖ CÙNG LÚC, có chủ đích —
    `STEP0_BLOCK_CANON` trong file này, và nguyên văn khối trong CẢ SÁU
    SKILL.md. Không còn đường sửa một skill mà lint vẫn xanh — TRỪ việc thêm
    nội dung vào phần tự do ngay sau khối, xem giới hạn ở trên.
    """
    norm = _normalize_doc(text)
    n = norm.count(STEP0_BLOCK_CANON)

    if n == 1:
        block_start = norm.index(STEP0_BLOCK_CANON)
        if _position_ok(norm, block_start):
            return []
        return [_position_error(norm, block_start)]

    if n >= 2:
        return [
            f"khối '⛔ BƯỚC 0′' xuất hiện {n} lần trong SKILL.md này — không rõ khối nào có hiệu lực.\n"
            f"  Xử: xoá (các) bản thừa, chỉ giữ lại ĐÚNG MỘT bản nguyên văn của "
            f"STEP0_BLOCK_CANON (scripts/ip_invent_lint.py)."
        ]

    # n == 0: khối vắng mặt hoặc đã trôi khỏi nguyên văn.
    candidate = _extract_step0_candidate(norm)
    if candidate is None:
        return [
            f"SKILL.md thiếu khối Bước 0′ ('⛔ BƯỚC 0′') — không tìm thấy dòng tiêu đề {_STEP0_FIRST_LINE!r}.\n"
            f"  Xử — nếu khối bị xoá nhầm: dán lại nguyên văn STEP0_BLOCK_CANON "
            f"(scripts/ip_invent_lint.py) ngay sau dòng tiêu đề `# <tên skill> — …`.\n"
            f"  Xử — nếu cố ý bỏ Bước 0′ khỏi skill này: đó là quyết định CEO có chủ đích, "
            f"không phải việc của lint — nói rõ lý do trong commit message."
        ]

    lineno, want_line, got_line = _first_differing_line(candidate, STEP0_BLOCK_CANON)
    return [
        f"khối '⛔ BƯỚC 0′' trong SKILL.md đã ĐỔI so với STEP0_BLOCK_CANON (không còn nguyên văn).\n"
        f"  Khác nhau đầu tiên ở dòng {lineno}:\n"
        f"    Mong đợi: {_shorten(want_line)!r}\n"
        f"    Thấy:     {_shorten(got_line)!r}\n"
        f"  Xử — nếu ĐỔI CÓ CHỦ ĐÍCH: cập nhật STEP0_BLOCK_CANON trong scripts/ip_invent_lint.py "
        f"VÀ sửa lại đúng nguyên văn khối này ở CẢ SÁU SKILL.md CÙNG LÚC.\n"
        f"  Xử — nếu KHÔNG CHỦ ĐÍCH: hoàn nguyên khối về đúng nguyên văn STEP0_BLOCK_CANON."
    ]


def lint_blocks_identical(texts: dict[str, str]) -> list[str]:
    """Chốt R1: sáu bản sao của khối Bước 0′ phải giống hệt nhau, BẮT ĐẦU
    đúng vị trí — VÀ giống hệt `STEP0_BLOCK_CANON`. `texts` là map {tên
    skill: nội dung SKILL.md}, PHẢI đủ và đúng sáu tên trong `SKILL_NAMES` —
    không hơn không kém.

    CÁCH LÀM (nội dung): so từng file với `STEP0_BLOCK_CANON` (không so file
    với file trực tiếp) — vì bằng-với-cùng-một-hằng-số kéo theo bằng-nhau-
    từng-đôi-một (tính bắc cầu), và neo vào MỘT nguồn chuẩn cho thông điệp lỗi
    rõ ràng hơn "file A khác file B" (không nói được ai đúng ai sai).

    CÁCH LÀM (vị trí, vá vòng 2, chỉ neo-đầu sau khi gỡ neo-cuối ở vòng 3):
    dùng lại `_position_ok`/`_position_error` của `lint_skill_block` cho từng
    file — một khối nội dung đúng nhưng bị bọc/dời chỗ TRƯỚC khối vẫn phải bị
    nêu tên ở đây, không chỉ ở hàm kiểm-một-file.

    CÁCH LÀM (arity, vá vòng 2 — Q2): hàm vòng 1 chỉ lặp qua `sorted(texts)`
    mà không đối chiếu `SKILL_NAMES`, nên `{}`, map thiếu file, hay map chỉ
    toàn tên rác đều lặp qua 0 phần tử và trả `[]` — XANH GIẢ. Chốt R1 tuyên
    bố "sáu bản sao", nên hàm phải tự kiểm nó thực sự nhận đủ sáu, KHÔNG suy
    diễn từ độ dài của tham số truyền vào. Kiểm arity TRƯỚC, và tách khỏi kiểm
    nội dung — thiếu/thừa tên là lỗi GỌI HÀM SAI, không phải lỗi của skill nào.

    PHẠM VI: giống `lint_skill_block` — chỉ đóng băng NỘI DUNG + VỊ TRÍ BẮT
    ĐẦU của khối Bước 0′, không đụng phần còn lại (tự do) của SKILL.md; không
    hiểu nghĩa. GIỚI HẠN CÓ TUYÊN BỐ giống hệt `lint_skill_block`: một câu vô
    hiệu hoá chèn vào phần tự do NGAY SAU khối, ở cuối file, hay trong
    `description:` frontmatter — không hàm nào ở đây bắt được. Xem docstring
    `lint_skill_block` để biết lý do (đối lập có chủ đích với `lint_gate_doc`,
    vốn băm được cả file vì không có phần tự do).

    Trả về rỗng nếu cả sáu khớp CẢ nội dung LẪN vị trí bắt đầu; ngược lại mỗi
    lỗi nêu RÕ TÊN SKILL lệch (hoặc lỗi arity nêu rõ tên thiếu/thừa).
    """
    want_names = sorted(SKILL_NAMES)
    got_names = sorted(texts)
    if got_names != want_names:
        missing = [n for n in want_names if n not in got_names]
        extra = [n for n in got_names if n not in want_names]
        return [
            "lint_blocks_identical nhận map KHÔNG khớp SKILL_NAMES — phải truyền ĐỦ và ĐÚNG "
            "sáu tên skill, không hơn không kém, mới so được.\n"
            f"  Thiếu: {missing if missing else '(không thiếu)'}\n"
            f"  Thừa:  {extra if extra else '(không thừa)'}\n"
            "  Xử: dựng map từ đúng SKILL_NAMES (vd `{n: đọc(n) for n in lint.SKILL_NAMES}`), "
            "đừng bỏ sót hay thêm tên ngoài danh sách."
        ]

    errors: list[str] = []
    for name in want_names:
        norm = _normalize_doc(texts[name])
        n = norm.count(STEP0_BLOCK_CANON)
        if n == 1:
            block_start = norm.index(STEP0_BLOCK_CANON)
            if _position_ok(norm, block_start):
                continue
            errors.append(f"{name}: {_position_error(norm, block_start)}")
            continue
        if n >= 2:
            errors.append(
                f"{name}: khối '⛔ BƯỚC 0′' xuất hiện {n} lần — không so được với 5 skill kia "
                f"cho tới khi xoá bản thừa, chỉ giữ ĐÚNG MỘT bản nguyên văn STEP0_BLOCK_CANON."
            )
            continue
        candidate = _extract_step0_candidate(norm)
        if candidate is None:
            errors.append(
                f"{name}: SKILL.md thiếu khối '⛔ BƯỚC 0′' hoàn toàn — không so được với 5 skill kia. "
                f"Dán lại nguyên văn STEP0_BLOCK_CANON."
            )
            continue
        lineno, want_line, got_line = _first_differing_line(candidate, STEP0_BLOCK_CANON)
        errors.append(
            f"{name}: khối '⛔ BƯỚC 0′' lệch so với STEP0_BLOCK_CANON (và do đó lệch so với 5 "
            f"skill kia) tại dòng {lineno} — mong đợi {_shorten(want_line)!r}, "
            f"thấy {_shorten(got_line)!r}. Nếu đổi có chủ đích: sửa STEP0_BLOCK_CANON + "
            f"CẢ SÁU SKILL.md cùng lúc. Nếu không: hoàn nguyên {name}/SKILL.md."
        )
    return errors


# ═══════════════════════════════════════════════════════════════════════════
# THAM CHIẾU DÙNG CHUNG ĐƯỢC TRÍCH TỪ MỘT SKILL.MD
# ═══════════════════════════════════════════════════════════════════════════

_CITED_REF_RE = re.compile(rf"\.\./{SHARED_DIR_NAME}/references/([A-Za-z0-9._-]+\.md)")


def cited_refs(text: str) -> list[str]:
    """Tên file tham chiếu dùng chung mà một SKILL.md trích, theo thứ tự, không lặp."""
    seen: list[str] = []
    for name in _CITED_REF_RE.findall(text):
        if name not in seen:
            seen.append(name)
    return seen
