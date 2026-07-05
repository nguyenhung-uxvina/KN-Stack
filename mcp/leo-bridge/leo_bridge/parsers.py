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
