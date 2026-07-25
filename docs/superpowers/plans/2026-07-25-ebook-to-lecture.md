# /ebook-to-md + /ebook-lecture Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Biến một file PDF ebook thành bộ Markdown tách theo chương, nạp vào NotebookLM, rồi bàn giao `/learn-lecture` sản xuất bài giảng.

**Architecture:** Ba script Python độc lập trong `D:\KN-Stack\scripts\` (map → ocr → assemble/verify), mỗi script chạy được riêng qua argparse, cộng hai SKILL.md điều phối chúng. Logic thuần (chọn cấp bookmark, dựng khoảng trang, dọn text, tách đoạn) tách khỏi lời gọi PaddleOCR để test được mà không cần nạp model. OCR ghi cache từng trang nên job 2–4 h đứt giữa chừng chỉ mất một trang.

**Tech Stack:** Python 3.12 (venv `d:\GitHub\PaddleOCR\.venv`), pypdfium2 (đọc bookmark + render trang), PaddleX PP-StructureV3 (layout→Markdown), pytest, MCP `notebooklm-mcp`.

## Global Constraints

- Spec nguồn: `D:\KN-Stack\docs\superpowers\specs\2026-07-25-ebook-to-lecture-design.md`. Mọi hành vi không nói trong plan này thì theo spec.
- Nhánh git: `feature/ebook-to-lecture` trong repo `D:\KN-Stack`. **Không commit vào `main`.** Commit format `[KN-STACK] <mô tả>`.
- Python interpreter cho MỌI lệnh chạy script và test: `d:\GitHub\PaddleOCR\.venv\Scripts\python.exe`. Không dùng `python` hệ thống.
- Env bắt buộc khi chạy bất kỳ lệnh nào chạm PaddleOCR: `PADDLE_PDX_CACHE_HOME=D:\tmp\paddlex_cache`.
- Vault root: `D:\Workshop_X` (ổ D:, không phải E:).
- Engine OCR: **PP-StructureV3**, không fallback sang text-layer extraction.
- Ngưỡng tách đoạn mặc định: **50 KB**.
- Tiếng Việt cho nội dung hướng tới CEO (SKILL.md, ChapterMap.md, QC report); tiếng Anh cho tên hàm, biến, commit message.
- Windows: mọi script phải ghi/đọc file với `encoding='utf-8'` tường minh — mặc định của Windows là cp1252 và sẽ làm hỏng tiếng Việt.

---

## File Structure

| File | Trách nhiệm |
|---|---|
| `scripts/ebook_map.py` | Đọc bookmark PDF → chọn cấp chương → dựng khoảng trang → đọc/ghi `ChapterMap.md`. Không chạm PaddleOCR. |
| `scripts/ebook_ocr.py` | Render từng trang → PP-StructureV3 → `pages/page-NNNN.md`. Resume bằng cách bỏ qua file đã có. Chỗ duy nhất import paddle. |
| `scripts/ebook_assemble.py` | Ghép `pages/` theo ChapterMap → `chapters/*.md`; dọn artifact OCR; tách chương quá ngưỡng. Không chạm PaddleOCR. |
| `scripts/ebook_verify.py` | Đọc `chapters/` + `ocr.log` → bảng QC + cảnh báo. Không chạm PaddleOCR. |
| `scripts/tests/test_ebook_map.py` | Test cho `ebook_map.py` |
| `scripts/tests/test_ebook_ocr.py` | Test cho phần thuần của `ebook_ocr.py` (chọn trang, parse range, đường dẫn) |
| `scripts/tests/test_ebook_assemble.py` | Test cho `ebook_assemble.py` |
| `scripts/tests/test_ebook_verify.py` | Test cho `ebook_verify.py` |
| `skills/extract/ebook-to-md/SKILL.md` | Block: điều phối 4 script theo luồng E0–E4, gate CEO ở E1 |
| `skills/learn/ebook-lecture/SKILL.md` | Orchestrator: gọi block trên → NLM ingest → bàn giao `/learn-lecture` |
| `evals/ebook-to-md.json`, `evals/ebook-lecture.json` | Binary assertion eval, format giống `evals/learn-lecture.json` |

Bốn script cùng đọc/ghi một cây thư mục sách (spec §4); `ChapterMap.md` là interface giữa chúng, không truyền state qua biến.

---

### Task 1: Chapter map từ bookmark PDF

**Files:**
- Create: `D:\KN-Stack\scripts\ebook_map.py`
- Create: `D:\KN-Stack\scripts\tests\test_ebook_map.py`

**Interfaces:**
- Consumes: không (task đầu)
- Produces:
  - `slugify(text: str, maxlen: int = 40) -> str`
  - `read_toc(pdf_path: str) -> tuple[list[dict], int]` — trả `([{level:int, title:str, page:int}], total_pages)`, `page` đánh số từ 1
  - `select_chapter_level(toc: list[dict]) -> int | None`
  - `build_chapters(toc: list[dict], level: int, total_pages: int) -> list[dict]` — mỗi chương `{n, part, title, start, end, file, status}`
  - `render_chaptermap(chapters: list[dict], meta: dict) -> str`
  - `parse_chaptermap(text: str) -> tuple[dict, list[dict]]`

- [ ] **Step 1: Cài pytest vào venv**

```powershell
$env:PIP_CACHE_DIR = "D:\tmp\pip-cache"
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pip install pytest
```

- [ ] **Step 2: Viết test thất bại**

Tạo `D:\KN-Stack\scripts\tests\test_ebook_map.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ebook_map import (
    build_chapters,
    parse_chaptermap,
    render_chaptermap,
    select_chapter_level,
    slugify,
)


def test_slugify_strips_vietnamese_diacritics():
    assert slugify("Chương 1: Mở đầu") == "chuong-1-mo-dau"
    assert slugify("Đánh giá & Kết luận") == "danh-gia-ket-luan"


def test_slugify_truncates_without_trailing_dash():
    assert slugify("a" * 60, maxlen=10) == "a" * 10
    assert not slugify("mot hai ba bon nam sau bay", maxlen=12).endswith("-")


def test_select_level_zero_when_top_level_has_chapters():
    toc = [{"level": 0, "title": f"Chuong {i}", "page": i} for i in range(1, 7)]
    assert select_chapter_level(toc) == 0


def test_select_level_one_when_top_level_is_parts():
    # Ebook chia Phần → Chương: 2 mục level 0, 8 mục level 1
    toc = [{"level": 0, "title": "Phan I", "page": 1}]
    toc += [{"level": 1, "title": f"Chuong {i}", "page": i + 1} for i in range(1, 5)]
    toc += [{"level": 0, "title": "Phan II", "page": 20}]
    toc += [{"level": 1, "title": f"Chuong {i}", "page": 20 + i} for i in range(5, 9)]
    assert select_chapter_level(toc) == 1


def test_select_level_none_when_no_bookmarks():
    assert select_chapter_level([]) is None


def test_build_chapters_derives_contiguous_page_ranges():
    toc = [
        {"level": 0, "title": "Mo dau", "page": 1},
        {"level": 0, "title": "Than bai", "page": 15},
        {"level": 0, "title": "Ket luan", "page": 39},
    ]
    ch = build_chapters(toc, level=0, total_pages=42)
    assert [(c["start"], c["end"]) for c in ch] == [(1, 14), (15, 38), (39, 42)]
    assert ch[0]["file"] == "01-mo-dau.md"
    assert ch[2]["n"] == 3
    assert all(c["status"] == "⬜" for c in ch)


def test_build_chapters_records_part_for_nested_level():
    toc = [
        {"level": 0, "title": "Phan I", "page": 1},
        {"level": 1, "title": "Chuong 1", "page": 1},
        {"level": 1, "title": "Chuong 2", "page": 10},
        {"level": 0, "title": "Phan II", "page": 20},
        {"level": 1, "title": "Chuong 3", "page": 20},
    ]
    ch = build_chapters(toc, level=1, total_pages=30)
    assert [c["part"] for c in ch] == ["Phan I", "Phan I", "Phan II"]
    assert [(c["start"], c["end"]) for c in ch] == [(1, 9), (10, 19), (20, 30)]


def test_build_chapters_clamps_when_bookmarks_share_a_page():
    toc = [
        {"level": 0, "title": "A", "page": 5},
        {"level": 0, "title": "B", "page": 5},
    ]
    ch = build_chapters(toc, level=0, total_pages=8)
    assert ch[0]["start"] == 5 and ch[0]["end"] == 5
    assert ch[1]["start"] == 5 and ch[1]["end"] == 8


def test_chaptermap_roundtrip():
    meta = {
        "created": "2026-07-25",
        "updated": "2026-07-25",
        "source_pdf": r"D:\books\x.pdf",
        "total_pages": 42,
        "engine": "PP-StructureV3",
    }
    chapters = [
        {"n": 1, "part": "", "title": "Mo dau", "start": 1, "end": 14,
         "file": "01-mo-dau.md", "status": "⬜"},
        {"n": 2, "part": "Phan II", "title": "Ket | luan", "start": 15, "end": 42,
         "file": "02-ket-luan.md", "status": "✅"},
    ]
    text = render_chaptermap(chapters, meta)
    meta2, chapters2 = parse_chaptermap(text)
    assert meta2["total_pages"] == 42
    assert meta2["source_pdf"] == r"D:\books\x.pdf"
    assert chapters2 == chapters


def test_parse_chaptermap_survives_pipe_in_title():
    # Tiêu đề có dấu | phải được escape khi render và khôi phục khi parse
    chapters = [{"n": 1, "part": "", "title": "A | B", "start": 1, "end": 2,
                 "file": "01-a-b.md", "status": "⬜"}]
    meta = {"created": "2026-07-25", "updated": "2026-07-25", "source_pdf": "x.pdf",
            "total_pages": 2, "engine": "PP-StructureV3"}
    _, parsed = parse_chaptermap(render_chaptermap(chapters, meta))
    assert parsed[0]["title"] == "A | B"
```

- [ ] **Step 3: Chạy test cho chắc là fail**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_map.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'ebook_map'`

- [ ] **Step 4: Viết `scripts/ebook_map.py`**

```python
"""ebook_map.py — build a chapter map for a PDF ebook from its bookmarks.

Part of the ebook-to-md skill (KN-Stack). Reads the PDF outline, picks the
bookmark level that represents chapters, derives page ranges, and writes
ChapterMap.md — the CEO-approved contract that ebook_assemble.py consumes.

Usage:
    python ebook_map.py --pdf <book.pdf> --out <book-dir> [--level N]

Dependencies (pip): pypdfium2, PyYAML  (both already in the PaddleOCR venv)
"""
import argparse
import os
import re
import unicodedata
from datetime import date

COLUMNS = ["#", "Phần", "Chương", "Trang", "Số trang", "File", "Trạng thái"]
STATUS_PENDING = "⬜"


def slugify(text: str, maxlen: int = 40) -> str:
    """'Chương 1: Mở đầu' -> 'chuong-1-mo-dau'. ASCII-only, safe as a filename."""
    s = unicodedata.normalize("NFD", text.lower().strip())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("đ", "d")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def read_toc(pdf_path: str):
    """Return ([{level, title, page}], total_pages). Page numbers are 1-based."""
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(pdf_path)
    items = []
    for bm in doc.get_toc():
        dest = bm.get_dest()
        if dest is None:
            continue
        title = (bm.get_title() or "").strip()
        if not title:
            continue
        items.append({"level": bm.level, "title": title, "page": dest.get_index() + 1})
    return items, len(doc)


def select_chapter_level(toc):
    """Level 0 is usually chapters — unless the book splits Parts at level 0."""
    if not toc:
        return None
    n0 = sum(1 for t in toc if t["level"] == 0)
    n1 = sum(1 for t in toc if t["level"] == 1)
    if n0 < 3 and n1 >= 3:
        return 1
    return 0


def build_chapters(toc, level, total_pages):
    """Turn the flat bookmark list into chapters with contiguous page ranges."""
    picked, current_part = [], ""
    for t in toc:
        if level > 0 and t["level"] == level - 1:
            current_part = t["title"]
        elif t["level"] == level:
            picked.append((t, current_part))

    chapters = []
    for i, (t, part) in enumerate(picked):
        start = t["page"]
        end = picked[i + 1][0]["page"] - 1 if i + 1 < len(picked) else total_pages
        if end < start:
            end = start
        chapters.append({
            "n": i + 1,
            "part": part,
            "title": t["title"],
            "start": start,
            "end": end,
            "file": f"{i + 1:02d}-{slugify(t['title'])}.md",
            "status": STATUS_PENDING,
        })
    return chapters


def _esc(s: str) -> str:
    return str(s).replace("|", "\\|")


def _unesc(s: str) -> str:
    return s.replace("\\|", "|")


def render_chaptermap(chapters, meta) -> str:
    """Render the frontmatter + table that the CEO approves and E3 consumes."""
    lines = [
        "---",
        f"created: {meta['created']}",
        f"updated: {meta['updated']}",
        "type: sop",
        "status: active",
        "tags: [#type/sop, #status/active, #topic/learning]",
        f"source_pdf: {meta['source_pdf']}",
        f"total_pages: {meta['total_pages']}",
        f"engine: {meta['engine']}",
        "---",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "|" + "|".join(["---"] * len(COLUMNS)) + "|",
    ]
    for c in chapters:
        pages = f"{c['start']}-{c['end']}"
        lines.append(
            f"| {c['n']} | {_esc(c['part'])} | {_esc(c['title'])} | {pages} | "
            f"{c['end'] - c['start'] + 1} | {c['file']} | {c['status']} |"
        )
    return "\n".join(lines) + "\n"


def parse_chaptermap(text: str):
    """Inverse of render_chaptermap. Returns (meta, chapters)."""
    meta, body = {}, text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        for line in fm.strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    if "total_pages" in meta:
        meta["total_pages"] = int(meta["total_pages"])

    chapters = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [_unesc(c.strip()) for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) != len(COLUMNS) or cells[0] in ("#", "---"):
            continue
        if not cells[0].isdigit():
            continue
        start, end = (int(x) for x in cells[3].split("-"))
        chapters.append({
            "n": int(cells[0]), "part": cells[1], "title": cells[2],
            "start": start, "end": end, "file": cells[5], "status": cells[6],
        })
    return meta, chapters


def main():
    ap = argparse.ArgumentParser(description="Build ChapterMap.md from PDF bookmarks")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True, help="book directory in the vault")
    ap.add_argument("--level", type=int, default=None, help="force bookmark level")
    args = ap.parse_args()

    toc, total_pages = read_toc(args.pdf)
    level = args.level if args.level is not None else select_chapter_level(toc)
    if level is None:
        print(f"NO_BOOKMARKS total_pages={total_pages}")
        return 2

    chapters = build_chapters(toc, level, total_pages)
    today = date.today().isoformat()
    meta = {"created": today, "updated": today, "source_pdf": os.path.abspath(args.pdf),
            "total_pages": total_pages, "engine": "PP-StructureV3"}

    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "ChapterMap.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(render_chaptermap(chapters, meta))
    print(f"OK level={level} chapters={len(chapters)} total_pages={total_pages} -> {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 5: Chạy test cho pass**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_map.py -v
```

Expected: PASS — 10 test.

- [ ] **Step 6: Chạy thật trên một PDF có bookmark**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_map.py `
  --pdf "D:\Workshop_X\3_Resources\2407_Borchert_TVLG_Introduction.pdf" `
  --out "D:\tmp\ebook-test\borchert"
```

Expected: `OK level=1 chapters=... total_pages=40`. PDF này có 18 bookmark, level 0 chỉ 1 mục (tên sách) còn level 1 là các chương — đúng ca kiểm tra rule chọn cấp. Mở `D:\tmp\ebook-test\borchert\ChapterMap.md` xác nhận khoảng trang liền mạch, không chồng lấn.

- [ ] **Step 7: Commit**

```bash
cd /d/KN-Stack
git add scripts/ebook_map.py scripts/tests/test_ebook_map.py
git commit -m "[KN-STACK] Add ebook_map: PDF bookmarks -> ChapterMap.md"
```

---

### Task 2: OCR từng trang, resume được

**Files:**
- Create: `D:\KN-Stack\scripts\ebook_ocr.py`
- Create: `D:\KN-Stack\scripts\tests\test_ebook_ocr.py`

**Interfaces:**
- Consumes: `ebook_map.parse_chaptermap` (đọc `total_pages` để biết phạm vi mặc định)
- Produces:
  - `page_md_path(out_dir: str, page: int) -> str` — `<out_dir>/pages/page-0042.md`
  - `parse_page_range(spec: str | None, total_pages: int) -> list[int]`
  - `pages_todo(out_dir: str, pages: list[int], force: bool = False) -> list[int]`
  - `format_progress(page: int, done: int, total: int, secs: float, conf: float, eta_s: float) -> str`
  - `run_ocr(pdf: str, out_dir: str, pages: list[int], dpi: int = 200, use_hpi: bool = True) -> int`

- [ ] **Step 1: Cài dependency cho PP-StructureV3 và HPI**

PP-StructureV3 cần nhóm `doc-parser`, không có trong bản cài `ocr-core` hiện tại.
Đã kiểm chứng 2026-07-25 — chạy `create_pipeline("PP-StructureV3")` trên venv hiện tại
báo lỗi, đây là trạng thái "trước" mà bước này phải xóa bỏ:

```
paddlex.utils.deps.DependencyError: `PP-StructureV3` requires additional dependencies.
To install them, run `pip install "paddlex[ocr]==<PADDLEX_VERSION>"` ...
```

```powershell
$env:PIP_CACHE_DIR = "D:\tmp\pip-cache"
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pip install -e "D:\GitHub\PaddleOCR[doc-parser]"
d:\GitHub\PaddleOCR\.venv\Scripts\paddleocr.exe install_hpi_deps cpu
```

Xác nhận:

```powershell
$env:PADDLE_PDX_CACHE_HOME="D:\tmp\paddlex_cache"
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -c "from paddlex import create_pipeline; create_pipeline('PP-StructureV3'); print('SV3_OK')"
```

Expected: in ra `SV3_OK` (lần đầu sẽ tải model, vài phút). HPI cài lỗi → ghi lại lỗi, tiếp tục với `--no-hpi`; đây là tối ưu tốc độ, không phải điều kiện chạy.

- [ ] **Step 2: Viết test thất bại**

Tạo `D:\KN-Stack\scripts\tests\test_ebook_ocr.py` — chỉ test phần thuần, không nạp model:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ebook_ocr import format_progress, page_md_path, pages_todo, parse_page_range


def test_page_md_path_is_zero_padded():
    assert page_md_path("D:/book", 42).replace("\\", "/") == "D:/book/pages/page-0042.md"
    assert page_md_path("D:/book", 7).replace("\\", "/") == "D:/book/pages/page-0007.md"


def test_parse_page_range_none_means_whole_book():
    assert parse_page_range(None, 5) == [1, 2, 3, 4, 5]


def test_parse_page_range_span_and_single():
    assert parse_page_range("2-4", 10) == [2, 3, 4]
    assert parse_page_range("7", 10) == [7]


def test_parse_page_range_clamps_to_book():
    assert parse_page_range("8-99", 10) == [8, 9, 10]


def test_parse_page_range_rejects_reversed():
    try:
        parse_page_range("9-3", 10)
    except ValueError:
        return
    raise AssertionError("expected ValueError for reversed range")


def test_pages_todo_skips_already_written(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "page-0002.md").write_text("done", encoding="utf-8")
    assert pages_todo(str(tmp_path), [1, 2, 3]) == [1, 3]


def test_pages_todo_force_redoes_everything(tmp_path):
    pages_dir = tmp_path / "pages"
    pages_dir.mkdir()
    (pages_dir / "page-0002.md").write_text("done", encoding="utf-8")
    assert pages_todo(str(tmp_path), [1, 2, 3], force=True) == [1, 2, 3]


def test_format_progress_is_one_parseable_line():
    line = format_progress(page=12, done=3, total=40, secs=41.2, conf=0.993, eta_s=1520)
    assert line.count("\n") == 0
    assert "page 12" in line and "3/40" in line
    assert "41.2s" in line and "0.993" in line and "eta=25m" in line
```

- [ ] **Step 3: Chạy test cho chắc là fail**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_ocr.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'ebook_ocr'`

- [ ] **Step 4: Viết `scripts/ebook_ocr.py`**

```python
"""ebook_ocr.py — OCR a PDF ebook one page at a time with PP-StructureV3.

Part of the ebook-to-md skill (KN-Stack). Each page is rendered to PNG, parsed
by PP-StructureV3, and written to pages/page-NNNN.md. Pages already on disk are
skipped, so a job that dies at hour 3 resumes losing at most one page.

Usage:
    python ebook_ocr.py --pdf <book.pdf> --out <book-dir> [--pages 5-40]
                        [--dpi 200] [--no-hpi] [--force]

Dependencies (pip): pypdfium2, paddlex[doc-parser]  (PaddleOCR venv)
Env: PADDLE_PDX_CACHE_HOME=D:\\tmp\\paddlex_cache
"""
import argparse
import os
import sys
import time
from datetime import datetime


def page_md_path(out_dir: str, page: int) -> str:
    return os.path.join(out_dir, "pages", f"page-{page:04d}.md")


def parse_page_range(spec, total_pages: int):
    """'2-4' -> [2,3,4]; '7' -> [7]; None -> every page. Clamped to the book."""
    if spec is None:
        return list(range(1, total_pages + 1))
    if "-" in spec:
        a, b = (int(x) for x in spec.split("-", 1))
        if b < a:
            raise ValueError(f"reversed page range: {spec}")
    else:
        a = b = int(spec)
    a = max(1, a)
    b = min(total_pages, b)
    return list(range(a, b + 1))


def pages_todo(out_dir: str, pages, force: bool = False):
    if force:
        return list(pages)
    return [p for p in pages if not os.path.exists(page_md_path(out_dir, p))]


def format_progress(page: int, done: int, total: int, secs: float,
                    conf: float, eta_s: float) -> str:
    stamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return (f"{stamp} page {page} {done}/{total} {secs:.1f}s "
            f"conf={conf:.3f} eta={int(eta_s // 60)}m")


def _mean_confidence(res) -> float:
    """Average text-line confidence of a PP-StructureV3 page result, 0.0 if absent."""
    try:
        scores = res["overall_ocr_res"]["rec_scores"]
    except (KeyError, TypeError):
        return 0.0
    return sum(scores) / len(scores) if scores else 0.0


def run_ocr(pdf: str, out_dir: str, pages, dpi: int = 200, use_hpi: bool = True) -> int:
    """OCR the given pages. Returns the number of pages actually processed."""
    import pypdfium2 as pdfium
    from paddlex import create_pipeline

    os.makedirs(os.path.join(out_dir, "pages"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "images"), exist_ok=True)
    log_path = os.path.join(out_dir, "ocr.log")

    pipe = create_pipeline("PP-StructureV3", use_hpip=use_hpi)
    doc = pdfium.PdfDocument(pdf)

    total, done, elapsed = len(pages), 0, 0.0
    for page in pages:
        t0 = time.time()
        png = os.path.join(out_dir, "pages", f"page-{page:04d}.png")
        doc[page - 1].render(scale=dpi / 72).to_pil().save(png)

        results = list(pipe.predict(png))
        md = results[0].markdown["markdown_texts"] if results else ""
        with open(page_md_path(out_dir, page), "w", encoding="utf-8") as f:
            f.write(md)
        conf = _mean_confidence(results[0]) if results else 0.0
        os.remove(png)

        done += 1
        secs = time.time() - t0
        elapsed += secs
        eta = (elapsed / done) * (total - done)
        line = format_progress(page, done, total, secs, conf, eta)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")
        print(line, flush=True)
    return done


def main():
    ap = argparse.ArgumentParser(description="Per-page OCR of a PDF ebook")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pages", default=None, help="e.g. 5-40 or 7; default whole book")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--no-hpi", action="store_true")
    ap.add_argument("--force", action="store_true", help="redo pages already on disk")
    args = ap.parse_args()

    import pypdfium2 as pdfium
    total_pages = len(pdfium.PdfDocument(args.pdf))

    wanted = parse_page_range(args.pages, total_pages)
    todo = pages_todo(args.out, wanted, force=args.force)
    print(f"START pages_wanted={len(wanted)} pages_todo={len(todo)}", flush=True)
    if not todo:
        print("DONE nothing to do (all pages cached)")
        return 0

    done = run_ocr(args.pdf, args.out, todo, dpi=args.dpi, use_hpi=not args.no_hpi)
    print(f"DONE processed={done}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Chạy test cho pass**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_ocr.py -v
```

Expected: PASS — 8 test.

- [ ] **Step 6: Chạy thật 2 trang, kiểm resume**

```powershell
$env:PADDLE_PDX_CACHE_HOME="D:\tmp\paddlex_cache"
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_ocr.py `
  --pdf "D:\GitHub\PaddleOCR\langchain-paddleocr\tests\data\sample_pdf.pdf" `
  --out "D:\tmp\ebook-test\sample" --pages 2-3
```

Expected: 2 dòng tiến độ, `DONE processed=2`, có `pages\page-0002.md` và `page-0003.md` với nội dung tiếng Anh về wiki, không còn file `.png` sót lại.

Chạy lại đúng lệnh đó — expected: `pages_todo=0` và `DONE nothing to do (all pages cached)`. Đây là bằng chứng resume hoạt động.

- [ ] **Step 7: Commit**

```bash
cd /d/KN-Stack
git add scripts/ebook_ocr.py scripts/tests/test_ebook_ocr.py
git commit -m "[KN-STACK] Add ebook_ocr: resumable per-page PP-StructureV3 OCR"
```

---

### Task 3: Ghép trang thành chương, dọn artifact, tách đoạn

**Files:**
- Create: `D:\KN-Stack\scripts\ebook_assemble.py`
- Create: `D:\KN-Stack\scripts\tests\test_ebook_assemble.py`

**Interfaces:**
- Consumes: `ebook_map.parse_chaptermap`, `ebook_map.render_chaptermap`, `ebook_map.slugify`, `ebook_ocr.page_md_path`
- Produces:
  - `strip_running_headers(pages: list[str], min_repeat: int = 3) -> list[str]`
  - `join_hyphens(text: str) -> str`
  - `drop_page_numbers(text: str) -> str`
  - `clean_pages(pages: list[str]) -> str`
  - `split_oversized(text: str, limit_bytes: int) -> list[tuple[str, str]]` — `[(suffix_title, chunk_text)]`, một phần tử nghĩa là không cần tách
  - `chapter_frontmatter(book: str, chapter: dict, today: str) -> str`
  - `assemble(out_dir: str, limit_kb: int = 50) -> list[dict]` — ghi `chapters/`, trả danh sách chương đã cập nhật

- [ ] **Step 1: Viết test thất bại**

Tạo `D:\KN-Stack\scripts\tests\test_ebook_assemble.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ebook_assemble import (
    chapter_frontmatter,
    clean_pages,
    drop_page_numbers,
    join_hyphens,
    split_oversized,
    strip_running_headers,
)


def test_strip_running_headers_removes_repeated_first_line():
    pages = [f"Sổ tay kỹ thuật\n\nNội dung trang {i}" for i in range(1, 5)]
    out = strip_running_headers(pages)
    assert all("Sổ tay kỹ thuật" not in p for p in out)
    assert "Nội dung trang 3" in out[2]


def test_strip_running_headers_keeps_line_repeated_only_twice():
    pages = ["Đầu đề\n\nA", "Đầu đề\n\nB", "Khác\n\nC", "Khác lần nữa\n\nD"]
    out = strip_running_headers(pages, min_repeat=3)
    assert out[0].startswith("Đầu đề")


def test_strip_running_headers_removes_repeated_last_line():
    pages = [f"Nội dung {i}\n\n© Workshop X 2026" for i in range(1, 6)]
    out = strip_running_headers(pages)
    assert all("Workshop X" not in p for p in out)


def test_join_hyphens_reconnects_split_words():
    assert join_hyphens("thiết bị đo lư-\nờng") == "thiết bị đo lường"


def test_join_hyphens_leaves_real_hyphens_alone():
    assert join_hyphens("máy bay không - người lái") == "máy bay không - người lái"
    assert join_hyphens("PP-StructureV3") == "PP-StructureV3"


def test_drop_page_numbers_removes_standalone_digit_lines():
    assert drop_page_numbers("Nội dung\n\n42\n\nTiếp theo") == "Nội dung\n\nTiếp theo"


def test_drop_page_numbers_keeps_digits_inside_text():
    assert "42" in drop_page_numbers("Khối lượng 42 kg")


def test_clean_pages_joins_with_blank_line():
    assert clean_pages(["A", "B"]) == "A\n\nB"


def test_split_oversized_returns_single_chunk_when_small():
    out = split_oversized("## Mục 1\n\nngắn", limit_bytes=10_000)
    assert len(out) == 1
    assert out[0][1] == "## Mục 1\n\nngắn"


def test_split_oversized_splits_on_level_two_headings():
    text = "## Một\n\n" + "a" * 600 + "\n\n## Hai\n\n" + "b" * 600
    out = split_oversized(text, limit_bytes=800)
    assert len(out) == 2
    assert out[0][0] == "Một" and out[1][0] == "Hai"
    assert "a" * 600 in out[0][1] and "b" * 600 in out[1][1]


def test_split_oversized_falls_back_to_paragraphs_without_headings():
    text = "\n\n".join("x" * 300 for _ in range(6))
    out = split_oversized(text, limit_bytes=800)
    assert len(out) > 1
    assert all(len(chunk.encode("utf-8")) <= 1200 for _, chunk in out)
    assert out[0][0].startswith("phần ")


def test_chapter_frontmatter_carries_page_range():
    fm = chapter_frontmatter("Sách A", {"n": 3, "title": "Chương 3", "start": 20,
                                        "end": 34}, "2026-07-25")
    assert fm.startswith("---\n") and fm.rstrip().endswith("---")
    assert "book: Sách A" in fm
    assert "chapter: 3" in fm
    assert "pages: 20-34" in fm
    assert "#type/article" in fm
```

- [ ] **Step 2: Chạy test cho chắc là fail**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_assemble.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'ebook_assemble'`

- [ ] **Step 3: Viết `scripts/ebook_assemble.py`**

```python
"""ebook_assemble.py — join OCR'd pages into chapter Markdown files.

Part of the ebook-to-md skill (KN-Stack). Reads ChapterMap.md (the CEO-approved
contract) plus pages/page-NNNN.md, strips OCR artefacts, and writes
chapters/NN-<slug>.md. Chapters over the size limit are split into sections so
NotebookLM retrieves them accurately.

Usage:
    python ebook_assemble.py --out <book-dir> [--chunk-kb 50] [--book "Tên sách"]

Dependencies (pip): none beyond the standard library
"""
import argparse
import os
import re
import sys
from collections import Counter
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ebook_map import parse_chaptermap, render_chaptermap, slugify  # noqa: E402
from ebook_ocr import page_md_path  # noqa: E402


def strip_running_headers(pages, min_repeat: int = 3):
    """Drop the first/last line when it repeats across >= min_repeat pages."""
    def edge(text, idx):
        lines = [ln for ln in text.strip().splitlines() if ln.strip()]
        return lines[idx].strip() if lines else None

    firsts = Counter(e for e in (edge(p, 0) for p in pages) if e)
    lasts = Counter(e for e in (edge(p, -1) for p in pages) if e)
    drop_first = {k for k, v in firsts.items() if v >= min_repeat}
    drop_last = {k for k, v in lasts.items() if v >= min_repeat}

    out = []
    for p in pages:
        lines = p.strip().splitlines()
        while lines and (not lines[0].strip() or lines[0].strip() in drop_first):
            if lines[0].strip() in drop_first:
                lines.pop(0)
            else:
                lines.pop(0)
                break
        while lines and (not lines[-1].strip() or lines[-1].strip() in drop_last):
            if lines[-1].strip() in drop_last:
                lines.pop()
            else:
                lines.pop()
                break
        out.append("\n".join(lines).strip())
    return out


def join_hyphens(text: str) -> str:
    """'lư-\\nờng' -> 'lường'. Only when the hyphen ends a line mid-word."""
    return re.sub(r"(\w)-\n(\w)", r"\1\2", text)


def drop_page_numbers(text: str) -> str:
    """Remove lines that are nothing but a page number."""
    lines = [ln for ln in text.splitlines() if not re.fullmatch(r"\s*\d{1,4}\s*", ln)]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def clean_pages(pages) -> str:
    stripped = strip_running_headers(pages)
    return drop_page_numbers(join_hyphens("\n\n".join(p for p in stripped if p.strip())))


def split_oversized(text: str, limit_bytes: int):
    """Split a chapter that exceeds limit_bytes. Returns [(section_title, text)]."""
    if len(text.encode("utf-8")) <= limit_bytes:
        return [("", text)]

    parts = re.split(r"^(##\s+.+)$", text, flags=re.MULTILINE)
    if len(parts) > 1:
        chunks, head = [], parts[0].strip()
        for i in range(1, len(parts), 2):
            title = parts[i].lstrip("#").strip()
            body = (parts[i] + parts[i + 1]).strip()
            if not chunks and head:
                body = head + "\n\n" + body
            chunks.append((title, body))
        if chunks:
            return chunks

    # No level-2 headings: pack paragraphs up to the limit
    chunks, buf, n = [], [], 0
    for para in text.split("\n\n"):
        size = len(para.encode("utf-8")) + 2
        if buf and n + size > limit_bytes:
            chunks.append((f"phần {len(chunks) + 1}", "\n\n".join(buf)))
            buf, n = [], 0
        buf.append(para)
        n += size
    if buf:
        chunks.append((f"phần {len(chunks) + 1}", "\n\n".join(buf)))
    return chunks


def chapter_frontmatter(book: str, chapter: dict, today: str) -> str:
    return (
        "---\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "type: article\n"
        "status: active\n"
        "tags: [#type/article, #status/active, #topic/learning]\n"
        f"book: {book}\n"
        f"chapter: {chapter['n']}\n"
        f"pages: {chapter['start']}-{chapter['end']}\n"
        "---\n"
    )


def assemble(out_dir: str, limit_kb: int = 50, book: str = None):
    """Build chapters/ from pages/ per ChapterMap.md. Returns updated chapter rows."""
    map_path = os.path.join(out_dir, "ChapterMap.md")
    with open(map_path, encoding="utf-8") as f:
        meta, chapters = parse_chaptermap(f.read())

    book = book or os.path.basename(os.path.normpath(out_dir))
    today = date.today().isoformat()
    limit = limit_kb * 1024
    ch_dir = os.path.join(out_dir, "chapters")
    os.makedirs(ch_dir, exist_ok=True)

    produced = []
    for ch in chapters:
        pages = []
        missing = 0
        for p in range(ch["start"], ch["end"] + 1):
            path = page_md_path(out_dir, p)
            if os.path.exists(path):
                with open(path, encoding="utf-8") as f:
                    pages.append(f.read())
            else:
                missing += 1
        body = clean_pages(pages)
        parts = split_oversized(body, limit)

        for i, (title, chunk) in enumerate(parts, start=1):
            if len(parts) == 1:
                name = ch["file"]
                heading = ch["title"]
            else:
                name = f"{ch['n']:02d}.{i}-{slugify(title or f'phan-{i}')}.md"
                heading = f"{ch['title']} ({title})" if title else f"{ch['title']} (phần {i})"
            with open(os.path.join(ch_dir, name), "w", encoding="utf-8") as f:
                f.write(chapter_frontmatter(book, ch, today))
                f.write(f"\n# {heading}\n\n{chunk}\n")
            produced.append({"file": name, "chapter": ch["n"],
                             "bytes": len(chunk.encode("utf-8"))})

        ch["status"] = "⚠" if missing else "✅"
        if len(parts) > 1:
            ch["file"] = ", ".join(p["file"] for p in produced if p["chapter"] == ch["n"])

    meta["updated"] = today
    with open(map_path, "w", encoding="utf-8") as f:
        f.write(render_chaptermap(chapters, meta))
    return produced


def main():
    ap = argparse.ArgumentParser(description="Assemble OCR pages into chapter files")
    ap.add_argument("--out", required=True, help="book directory in the vault")
    ap.add_argument("--chunk-kb", type=int, default=50)
    ap.add_argument("--book", default=None, help="book title for frontmatter")
    args = ap.parse_args()

    produced = assemble(args.out, limit_kb=args.chunk_kb, book=args.book)
    for p in produced:
        print(f"{p['file']}\t{p['bytes'] / 1024:.1f} KB")
    print(f"OK files={len(produced)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Chạy test cho pass**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_assemble.py -v
```

Expected: PASS — 12 test.

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack
git add scripts/ebook_assemble.py scripts/tests/test_ebook_assemble.py
git commit -m "[KN-STACK] Add ebook_assemble: pages -> cleaned chapter Markdown"
```

---

### Task 4: Báo cáo QC

**Files:**
- Create: `D:\KN-Stack\scripts\ebook_verify.py`
- Create: `D:\KN-Stack\scripts\tests\test_ebook_verify.py`

**Interfaces:**
- Consumes: `ebook_map.parse_chaptermap`
- Produces:
  - `parse_ocr_log(text: str) -> dict[int, float]` — `{page: confidence}`
  - `has_unclosed_table(text: str) -> bool`
  - `chapter_warnings(chars: int, avg_conf: float, unclosed: bool, missing: int) -> list[str]`
  - `render_qc(rows: list[dict]) -> str`

- [ ] **Step 1: Viết test thất bại**

Tạo `D:\KN-Stack\scripts\tests\test_ebook_verify.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ebook_verify import (
    chapter_warnings,
    has_unclosed_table,
    parse_ocr_log,
    render_qc,
)


def test_parse_ocr_log_extracts_confidence_per_page():
    log = (
        "2026-07-25T12:00:00 page 1 1/40 41.2s conf=0.993 eta=25m\n"
        "2026-07-25T12:00:45 page 2 2/40 39.8s conf=0.871 eta=24m\n"
    )
    assert parse_ocr_log(log) == {1: 0.993, 2: 0.871}


def test_parse_ocr_log_last_entry_wins_after_rerun():
    log = (
        "2026-07-25T12:00:00 page 3 1/2 40.0s conf=0.500 eta=1m\n"
        "2026-07-25T13:00:00 page 3 1/1 40.0s conf=0.990 eta=0m\n"
    )
    assert parse_ocr_log(log) == {3: 0.990}


def test_parse_ocr_log_ignores_noise_lines():
    assert parse_ocr_log("START pages_wanted=40\nDONE processed=40\n") == {}


def test_has_unclosed_table_detects_dangling_row():
    assert has_unclosed_table("| a | b |\n|---|---|\n| 1 | 2 |") is False
    assert has_unclosed_table("| a | b |\n|---|---|\n| 1 | 2") is True


def test_chapter_warnings_flags_short_chapter():
    w = chapter_warnings(chars=120, avg_conf=0.99, unclosed=False, missing=0)
    assert any("ngắn bất thường" in x for x in w)


def test_chapter_warnings_flags_low_confidence():
    w = chapter_warnings(chars=9000, avg_conf=0.80, unclosed=False, missing=0)
    assert any("confidence" in x for x in w)


def test_chapter_warnings_flags_missing_pages_and_tables():
    w = chapter_warnings(chars=9000, avg_conf=0.99, unclosed=True, missing=2)
    assert any("bảng" in x for x in w)
    assert any("thiếu 2 trang" in x for x in w)


def test_chapter_warnings_clean_chapter_has_none():
    assert chapter_warnings(chars=9000, avg_conf=0.99, unclosed=False, missing=0) == []


def test_render_qc_marks_rows_and_totals():
    rows = [
        {"n": 1, "title": "Mở đầu", "pages": "1-14", "chars": 9000,
         "avg_conf": 0.99, "images": 2, "warnings": []},
        {"n": 2, "title": "Rỗng", "pages": "15-16", "chars": 0,
         "avg_conf": 0.0, "images": 0, "warnings": ["chương rỗng"]},
    ]
    out = render_qc(rows)
    assert "✅" in out and "⚠" in out
    assert "chương rỗng" in out
    assert "2/2 chương" in out or "1/2 chương đạt" in out
```

- [ ] **Step 2: Chạy test cho chắc là fail**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\test_ebook_verify.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'ebook_verify'`

- [ ] **Step 3: Viết `scripts/ebook_verify.py`**

```python
"""ebook_verify.py — QC report for an assembled ebook.

Part of the ebook-to-md skill (KN-Stack). Cross-checks chapters/ against
ChapterMap.md and ocr.log, then prints a table the CEO reads before the book
goes into NotebookLM. Never silently swallows a bad chapter.

Usage:
    python ebook_verify.py --out <book-dir>

Dependencies (pip): none beyond the standard library
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ebook_map import parse_chaptermap  # noqa: E402

MIN_CHARS = 500
MIN_CONF = 0.85


def parse_ocr_log(text: str):
    """Return {page: confidence}; a re-run of the same page overwrites the old value."""
    out = {}
    for line in text.splitlines():
        m = re.search(r"\bpage (\d+)\b.*\bconf=([0-9.]+)", line)
        if m:
            out[int(m.group(1))] = float(m.group(2))
    return out


def has_unclosed_table(text: str) -> bool:
    """True when a Markdown table row starts with | but never closes — sign of a
    table cut at a page boundary."""
    for line in text.splitlines():
        s = line.rstrip()
        if s.startswith("|") and not s.endswith("|"):
            return True
    return False


def chapter_warnings(chars: int, avg_conf: float, unclosed: bool, missing: int):
    w = []
    if chars == 0:
        w.append("chương rỗng — nghi map sai hoặc trang scan hỏng")
    elif chars < MIN_CHARS:
        w.append(f"ngắn bất thường ({chars} ký tự)")
    if 0 < avg_conf < MIN_CONF:
        w.append(f"confidence thấp ({avg_conf:.3f})")
    if unclosed:
        w.append("bảng bị cắt ở ranh giới trang — cần sửa tay")
    if missing:
        w.append(f"thiếu {missing} trang chưa OCR")
    return w


def render_qc(rows) -> str:
    lines = [
        "| # | Chương | Trang | Ký tự | Conf | Ảnh | Kết quả |",
        "|---|--------|-------|-------|------|-----|---------|",
    ]
    ok = 0
    for r in rows:
        mark = "⚠" if r["warnings"] else "✅"
        ok += 0 if r["warnings"] else 1
        note = "; ".join(r["warnings"]) if r["warnings"] else ""
        lines.append(
            f"| {r['n']} | {r['title']} | {r['pages']} | {r['chars']} | "
            f"{r['avg_conf']:.3f} | {r['images']} | {mark} {note} |"
        )
    lines.append("")
    lines.append(f"**{ok}/{len(rows)} chương đạt.**")
    return "\n".join(lines)


def collect_rows(out_dir: str):
    with open(os.path.join(out_dir, "ChapterMap.md"), encoding="utf-8") as f:
        _, chapters = parse_chaptermap(f.read())

    log_path = os.path.join(out_dir, "ocr.log")
    conf_by_page = {}
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as f:
            conf_by_page = parse_ocr_log(f.read())

    ch_dir = os.path.join(out_dir, "chapters")
    rows = []
    for ch in chapters:
        files = [x.strip() for x in ch["file"].split(",")]
        text = ""
        for name in files:
            p = os.path.join(ch_dir, name)
            if os.path.exists(p):
                with open(p, encoding="utf-8") as f:
                    text += f.read()
        page_range = list(range(ch["start"], ch["end"] + 1))
        confs = [conf_by_page[p] for p in page_range if p in conf_by_page]
        missing = sum(1 for p in page_range if p not in conf_by_page)
        avg_conf = sum(confs) / len(confs) if confs else 0.0
        rows.append({
            "n": ch["n"], "title": ch["title"], "pages": f"{ch['start']}-{ch['end']}",
            "chars": len(text), "avg_conf": avg_conf,
            "images": text.count("!["),
            "warnings": chapter_warnings(len(text), avg_conf,
                                         has_unclosed_table(text), missing),
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description="QC report for an assembled ebook")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    print(render_qc(collect_rows(args.out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Chạy test cho pass**

```powershell
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe -m pytest scripts\tests\ -v
```

Expected: PASS toàn bộ 4 file test (39 test).

- [ ] **Step 5: Commit**

```bash
cd /d/KN-Stack
git add scripts/ebook_verify.py scripts/tests/test_ebook_verify.py
git commit -m "[KN-STACK] Add ebook_verify: QC report with explicit warnings"
```

---

### Task 5: SKILL.md cho `/ebook-to-md`

**Files:**
- Create: `D:\KN-Stack\skills\extract\ebook-to-md\SKILL.md`
- Create: `D:\KN-Stack\evals\ebook-to-md.json`

**Interfaces:**
- Consumes: cả 4 script từ Task 1–4 (gọi qua dòng lệnh, đúng chữ ký ở phần Usage của mỗi script)
- Produces: skill `/ebook-to-md <đường-dẫn-pdf>`, mà `/ebook-lecture` ở Task 6 gọi lại

- [ ] **Step 1: Viết SKILL.md**

Tạo `D:\KN-Stack\skills\extract\ebook-to-md\SKILL.md`. Frontmatter phải có `name: ebook-to-md` và description chứa "Triggers on:" với cụm EN lẫn VI. Nội dung theo spec §5, gồm đủ: bảng Operational Envelope, 5 bước E0–E4, CEO GATE chặn giữa E1 và E2, bảng lỗi spec §7, mục COD spec §8.

Các lệnh chính xác skill phải gọi (dán nguyên vào SKILL.md để agent không phải đoán):

```powershell
# E1 MAP
$env:PADDLE_PDX_CACHE_HOME="D:\tmp\paddlex_cache"
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe D:\KN-Stack\scripts\ebook_map.py `
  --pdf "<pdf>" --out "<book-dir>"

# E2 OCR — LUÔN chạy nền (run_in_background), 2-4 giờ
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe D:\KN-Stack\scripts\ebook_ocr.py `
  --pdf "<pdf>" --out "<book-dir>"

# E3 ASSEMBLE
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe D:\KN-Stack\scripts\ebook_assemble.py `
  --out "<book-dir>" --chunk-kb 50 --book "<tên sách>"

# E4 VERIFY
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe D:\KN-Stack\scripts\ebook_verify.py `
  --out "<book-dir>"
```

Quy tắc bắt buộc ghi trong RULES của skill:
- `<book-dir>` = `D:\Workshop_X\3_Resources\Books & Articles\<book-slug>\`
- **KHÔNG chạy E2 trước khi CEO duyệt ChapterMap** — đây là gate Core, sai map = mất 2–4 h
- E2 luôn `run_in_background`; theo dõi bằng cách đọc `ocr.log`, KHÔNG poll bằng cách chạy lại script
- `ebook_map.py` trả `NO_BOOKMARKS` → chạy `ebook_ocr.py --pages 1-8` lấy mục lục, đọc rồi soạn ChapterMap tay theo đúng format `render_chaptermap`
- KHÔNG tự sửa file trong `chapters/` sau khi CEO đã duyệt QC

- [ ] **Step 2: Viết eval JSON**

Tạo `D:\KN-Stack\evals\ebook-to-md.json` theo đúng schema của `evals/learn-lecture.json` (`skill`, `version`, `description`, `mode: "static"`, `test_input`, `total_required`, `passing_score`, `assertions[]` với `id`/`name`/`check`/`regex`/`required`). Tối thiểu 8 assertion:

| id | Kiểm |
|---|---|
| `E2M-FRONTMATTER` | `name: ebook-to-md` + Triggers on song ngữ |
| `E2M-PHASES` | đủ E0 PREFLIGHT → E1 MAP → E2 OCR → E3 ASSEMBLE → E4 VERIFY |
| `E2M-GATE` | có gate CEO duyệt ChapterMap TRƯỚC E2 |
| `E2M-VENV` | dùng `d:\GitHub\PaddleOCR\.venv` chứ không phải `python` trần |
| `E2M-CACHE` | set `PADDLE_PDX_CACHE_HOME` |
| `E2M-BG` | E2 chạy nền |
| `E2M-VAULT` | ghi vào `3_Resources\Books & Articles` trên ổ D: |
| `E2M-NOBOOKMARK` | có nhánh xử lý PDF không bookmark |

- [ ] **Step 3: Tạo junction và xác nhận skill nạp được**

```powershell
New-Item -ItemType Junction -Path "C:\Users\Admin\.claude\commands\ebook-to-md" `
  -Target "D:\KN-Stack\skills\extract\ebook-to-md"
Get-Content "C:\Users\Admin\.claude\commands\ebook-to-md\SKILL.md" -TotalCount 5
```

Expected: in ra frontmatter — junction trỏ đúng.

- [ ] **Step 4: Commit**

```bash
cd /d/KN-Stack
git add skills/extract/ebook-to-md/SKILL.md evals/ebook-to-md.json
git commit -m "[KN-STACK] Add /ebook-to-md skill + eval"
```

---

### Task 6: SKILL.md cho `/ebook-lecture`

**Files:**
- Create: `D:\KN-Stack\skills\learn\ebook-lecture\SKILL.md`
- Create: `D:\KN-Stack\evals\ebook-lecture.json`

**Interfaces:**
- Consumes: `/ebook-to-md` (Task 5); MCP `notebooklm-mcp`; bàn giao sang `/learn-lecture` có sẵn
- Produces: skill `/ebook-lecture <pdf | book-slug>` + `Ingest-Manifest.md` trong thư mục sách

- [ ] **Step 1: Viết SKILL.md**

Tạo `D:\KN-Stack\skills\learn\ebook-lecture\SKILL.md` theo spec §6, luồng L0–L6. Kế thừa nguyên các gotcha NLM đã kiểm chứng trong `/learn-lecture` — chép sang, đừng để agent tự phát hiện lại:

- Auth NLM ~20 phút. `refresh_auth` fail → HALT, báo CEO chạy `nlm login` (interactive, Claude không tự chạy được). MCP `server_info` trả `auth_status: configured` từ CACHE CŨ — **không tin nó**; kiểm auth thật bằng CLI `nlm source content <sid>`.
- `source_add` nhiều chương phải nằm **trong cùng một message** để chạy song song; tuần tự vừa chậm vừa dễ dính rate limit.
- Notebook trùng title → CEO chọn (tạo mới / dùng lại / dừng), **không tự đè**.
- L6 chỉ **in lệnh** `/learn-lecture "<tên notebook>"`, không tự gọi.

`Ingest-Manifest.md` ghi: notebook_id, notebook_url, ngày, bảng `| # | File chương | KB | source_id | Trạng thái |`, và 2 câu query mẫu cho CEO test ở L5.

- [ ] **Step 2: Viết eval JSON**

Tạo `D:\KN-Stack\evals\ebook-lecture.json`, cùng schema, tối thiểu 8 assertion:

| id | Kiểm |
|---|---|
| `EBL-FRONTMATTER` | `name: ebook-lecture` + Triggers on song ngữ |
| `EBL-FLOW` | đủ L0 MD → L1 AUTH → L2 CREATE → L3 INGEST → L4 VERIFY → L5 TEST → L6 HANDOFF |
| `EBL-AUTH-HALT` | auth fail → HALT + hướng dẫn `nlm login`, không bypass |
| `EBL-SERVERINFO` | cảnh báo `server_info` trả cache cũ, không tin |
| `EBL-PARALLEL` | `source_add` song song trong 1 message |
| `EBL-NO-OVERWRITE` | notebook trùng → CEO quyết, không tự đè |
| `EBL-MANIFEST` | ghi `Ingest-Manifest.md` với source_id từng chương |
| `EBL-HANDOFF` | KHÔNG tự chạy `/learn-lecture`, chỉ in lệnh |

- [ ] **Step 3: Tạo junction**

```powershell
New-Item -ItemType Junction -Path "C:\Users\Admin\.claude\commands\ebook-lecture" `
  -Target "D:\KN-Stack\skills\learn\ebook-lecture"
Get-Content "C:\Users\Admin\.claude\commands\ebook-lecture\SKILL.md" -TotalCount 5
```

- [ ] **Step 4: Commit**

```bash
cd /d/KN-Stack
git add skills/learn/ebook-lecture/SKILL.md evals/ebook-lecture.json
git commit -m "[KN-STACK] Add /ebook-lecture orchestrator skill + eval"
```

---

### Task 7: Smoke test đầu-cuối khâu PDF→MD

**Files:**
- Modify: không sửa code trừ khi test lộ lỗi
- Test: chạy tay trên 2 PDF thật

**Interfaces:**
- Consumes: toàn bộ Task 1–5
- Produces: bằng chứng pipeline chạy được, ghi vào `evals/eval-log.md`

- [ ] **Step 1: Ca không có bookmark (sample_pdf, 4 trang)**

```powershell
$env:PADDLE_PDX_CACHE_HOME="D:\tmp\paddlex_cache"
$B = "D:\tmp\ebook-test\sample"
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_map.py `
  --pdf "D:\GitHub\PaddleOCR\langchain-paddleocr\tests\data\sample_pdf.pdf" --out $B
```

Expected: `NO_BOOKMARKS total_pages=4` và exit code 2 — file này `get_toc()` trả 0 entry, đúng ca cần test. Soạn tay `$B\ChapterMap.md` một chương phủ trang 1-4, rồi chạy tiếp OCR → assemble → verify.

- [ ] **Step 2: Ca có bookmark (Borchert, 40 trang)**

```powershell
$env:PADDLE_PDX_CACHE_HOME="D:\tmp\paddlex_cache"
$B = "D:\tmp\ebook-test\borchert"
cd D:\KN-Stack
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_map.py `
  --pdf "D:\Workshop_X\3_Resources\2407_Borchert_TVLG_Introduction.pdf" --out $B
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_ocr.py `
  --pdf "D:\Workshop_X\3_Resources\2407_Borchert_TVLG_Introduction.pdf" --out $B --pages 6-9
```

Expected: map ra level=1 với các chương của sách; OCR 4 trang xong, `ocr.log` có 4 dòng `conf=`.

- [ ] **Step 3: Kiểm resume bằng cách giết job**

Chạy `ebook_ocr.py --pages 10-20` ở nền, đợi ~2 trang rồi dừng tiến trình. Chạy lại đúng lệnh đó.

Expected: dòng `START` báo `pages_todo` nhỏ hơn `pages_wanted` đúng bằng số trang đã xong.

- [ ] **Step 4: Kiểm ngưỡng tách đoạn**

```powershell
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_assemble.py --out $B --chunk-kb 2
d:\GitHub\PaddleOCR\.venv\Scripts\python.exe scripts\ebook_verify.py --out $B
```

Expected: `--chunk-kb 2` ép tách → xuất hiện file dạng `NN.M-*.md`, ChapterMap cột File liệt kê nhiều file, QC in bảng có dòng ⚠ cho các chương chưa OCR (trang thiếu) — chứng tỏ cảnh báo không bị nuốt.

- [ ] **Step 5: Ghi kết quả vào eval-log và commit**

Thêm một mục vào `D:\KN-Stack\evals\eval-log.md`: ngày, 2 ca test, số trang, thời gian thực tế/trang (có HPI và không), lỗi gặp phải.

```bash
cd /d/KN-Stack
git add evals/eval-log.md
git commit -m "[KN-STACK] Log ebook-to-md smoke test results"
```

---

## Self-Review

**Spec coverage** — mọi mục của spec đều có task:

| Spec | Task |
|---|---|
| §5 E0 PREFLIGHT | Task 2 Step 1 (deps + HPI), Task 5 (skill mô tả bước) |
| §5 E1 MAP + chọn cấp bookmark | Task 1 |
| §5 CEO GATE | Task 5 (RULES + eval `E2M-GATE`) |
| §5 E2 OCR per-page + resume | Task 2 |
| §5 E3 ASSEMBLE + dọn artifact + tách đoạn | Task 3 |
| §5 E4 VERIFY | Task 4 |
| §6 L0–L6 orchestrator NLM | Task 6 |
| §7 bảng lỗi | Task 5 + Task 6 (nội dung SKILL.md) |
| §8 COD | Task 5 + Task 6 |
| §9 môi trường | Task 2 Step 1 + Global Constraints |
| §10 kiểm thử | Task 7 |

**Đã sửa khi tự soát:**
- Ngưỡng tách đoạn ưu tiên (a) heading cấp 2, (b) bookmark cấp sâu, (c) ranh giới trang — bookmark cấp sâu (b) hiện KHÔNG được `split_oversized` dùng vì nó chỉ nhận `text`. Chấp nhận có ý thức: (a) và (c) phủ mọi trường hợp, thêm (b) đòi truyền toc xuống làm rối interface mà lợi ích biên. Ghi lại ở đây để không bị coi là bỏ sót spec.
- `ebook_verify.collect_rows` đọc cột File có thể chứa nhiều tên cách nhau bởi dấu phẩy (do Task 3 ghi vậy) — đã khớp giữa hai module.
- `format_progress` với `eta_s=1520` cho `eta=25m` (1520//60 = 25), khớp test.

**Ngoài phạm vi plan này** (spec §11): EPUB/MOBI, dịch sách, tự sinh Galaxy note, tự chạy `/learn-lecture`.
