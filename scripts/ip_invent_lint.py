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
