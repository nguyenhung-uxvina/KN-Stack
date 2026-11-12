"""helix-cad-ingest / drawing_tables.py — position-aware Perception for title blocks and parts lists (G1, P–C–C).

Why: a drawing set measured 2026-11-05 keeps its title block as a block INSERT whose definition holds only the
static labels, while the per-sheet values (code, name, material, scale) are separate TEXT/MTEXT placed over it; the
parts list (bảng kê) is line-drawn with text cells. Searching all sheet text for a code picks up parts-list rows
and found the sheet code on 0/42 sheets. Every value returned here carries a locator (DXF handle + insertion point).

Pure ezdxf, local, no LLM.
"""
import re

from ezdxf import bbox as ezbbox

TITLE_LABELS = ("tỷ lệ", "tỉ lệ", "khối lượng", "số tờ", "thiết kế", "kiểm tra", "chữ ký", "ngày", "tờ:")
HEADER_KEYS = {
    # two layouts measured on one set: "TT · Ký hiệu · Tên gọi - Quy cách · Số lượng · Vật liệu · Ghi chú"
    # and the TCVN parts-list form "Khổ giấy · Miền · Vị trí · Ký hiệu · Tên gọi · S.lg · Chú thích"
    "tt": ("tt", "stt", "vị trí"),
    "format": ("khổ giấy",),
    "zone": ("miền",),
    "code": ("ký hiệu", "kí hiệu", "ký hiệu bản vẽ", "mã"),
    "name": ("tên gọi", "tên chi tiết", "tên gọi - quy cách", "tên"),
    "qty": ("số lượng", "sl", "sl.", "s.lg", "s.lượng"),
    "material": ("vật liệu", "vl"),
    "note": ("ghi chú", "chú thích"),
}
CODE_RE = re.compile(r"(?i)\b\d{1,3}\.[a-z]{1,4}-?\d{1,3}(?:\.\d{2}){1,3}(?:\s*b[lk])?\b")
SCALE_RE = re.compile(r"^\s*\d+\s*:\s*\d+\s*$")
MAT_RE = re.compile(r"(?i)\b(thép|ss400|ah36|c45|ct3|inox|nhôm|al\s?\d{4}|gang|đồng|gỗ|nhựa|ptfe|teflon|pom|cao su|"
                    r"composite|frp|sợi thủy tinh|sợi thuỷ tinh)\b")


_UESC = re.compile(r"\\U\+([0-9A-Fa-f]{4})")


def decode_uescapes(s):
    """DXF <= R2004 stores non-ASCII as \\U+XXXX (measured on a second 47-sheet set: 'THANH KHUNG \\U+0110\\U+1EE8NG'
    — without decoding, no title-block label matched and the reader found 0/47 codes)."""
    return _UESC.sub(lambda m: chr(int(m.group(1), 16)), s or "")


def entity_text(e):
    """Plain, decoded text of a TEXT / MTEXT / ATTRIB / ATTDEF entity."""
    raw = e.plain_text() if e.dxftype() == "MTEXT" else e.dxf.get("text", "")
    return decode_uescapes(raw)


def _norm(s):
    return re.sub(r"\s+", " ", decode_uescapes(s).strip().lower())


def _text_rec(e, handle):
    t = e.dxftype()
    if t == "TEXT":
        s, h = entity_text(e), e.dxf.get("height", 0.0)
    elif t == "MTEXT":
        s, h = entity_text(e), e.dxf.get("char_height", 0.0)
    else:
        return None
    s = (s or "").replace("\n", " ").strip()
    if not s:
        return None
    p = e.dxf.insert
    return {"text": s, "x": float(p.x), "y": float(p.y), "h": float(h or 0.0), "handle": handle,
            "layer": e.dxf.layer}


def _is_form_block(doc, name):
    """A title-block / parts-list form: its definition carries title labels or parts-list column headers."""
    blk = doc.blocks.get(name)
    if blk is None:
        return False
    n = 0
    for e in blk:
        if e.dxftype() in ("TEXT", "MTEXT"):
            s = _norm(entity_text(e))
            n += any(s.startswith(lb) for lb in TITLE_LABELS) or bool(_header_role(s))
    return n >= 3


def texts(msp, doc=None):
    """Loose TEXT/MTEXT in modelspace, plus (when doc is given) the texts inside title-block / parts-list form
    blocks, transformed to world coordinates — measured: a parts-list header row can live in the form block
    while its rows are loose text. Virtual texts get handle '<insert handle>/v<i>'."""
    out = []
    for e in msp:
        r = _text_rec(e, e.dxf.handle)
        if r:
            out.append(r)
    if doc is not None:
        for ins in msp.query("INSERT"):
            if not _is_form_block(doc, ins.dxf.name):
                continue
            for i, v in enumerate(ins.virtual_entities()):
                r = _text_rec(v, f"{ins.dxf.handle}/v{i}")
                if r:
                    r["virtual"] = True
                    out.append(r)
    return out


def _block_labels(doc, name):
    blk = doc.blocks.get(name)
    if blk is None:
        return 0
    n = 0
    for e in blk:
        if e.dxftype() in ("TEXT", "MTEXT", "ATTDEF"):
            s = _norm(entity_text(e))
            n += any(s.startswith(lb) for lb in TITLE_LABELS)
    return n


def find_title_block(doc):
    """INSERT whose block definition carries >= 3 title-block labels; returns (insert, (x0, y0, x1, y1)) or None."""
    best = None
    for ins in doc.modelspace().query("INSERT"):
        k = _block_labels(doc, ins.dxf.name)
        if k >= 3:
            b = ezbbox.extents([ins])
            area = (b.extmax.x - b.extmin.x) * (b.extmax.y - b.extmin.y)
            if best is None or k > best[0] or (k == best[0] and area < best[1]):
                best = (k, area, ins, (b.extmin.x, b.extmin.y, b.extmax.x, b.extmax.y))
    return (best[2], best[3]) if best else None


def _loc(t):
    return {"handle": t["handle"], "x": round(t["x"], 2), "y": round(t["y"], 2), "layer": t["layer"]}


def read_title_block(doc, txts=None, extra_code_re=None):
    """Fields from text lying inside the title-block INSERT's extents. Returns dict with values + locators."""
    found = find_title_block(doc)
    if not found:
        return {"found": False}
    ins, (x0, y0, x1, y1) = found
    txts = txts if txts is not None else texts(doc.modelspace())   # loose text only: form labels are not values
    inside =[t for t in txts if x0 - 1 <= t["x"] <= x1 + 1 and y0 - 1 <= t["y"] <= y1 + 1]
    code_res = [CODE_RE] + ([extra_code_re] if extra_code_re else [])
    codes = [t for t in inside if any(r.search(t["text"]) for r in code_res)]
    scales = [t for t in inside if SCALE_RE.match(t["text"])]
    mats = [t for t in inside if MAT_RE.search(t["text"]) and not any(r.search(t["text"]) for r in code_res)]
    used = {t["handle"] for t in codes + scales + mats}
    rest = [t for t in inside if t["handle"] not in used and not re.fullmatch(r"[\d\s.,≈~]+", t["text"])
            and len(t["text"]) >= 3]
    name = max(rest, key=lambda t: (t["h"], len(t["text"])), default=None)
    mass = next((t for t in inside if re.fullmatch(r"\s*[≈~]?\s*\d+(?:[.,]\d+)?\s*", t["text"])
                 and t["handle"] not in used), None)

    def pick(lst):
        return None if not lst else {"value": lst[0]["text"].strip(), "locator": _loc(lst[0]),
                                     "alternatives": [x["text"].strip() for x in lst[1:]]}
    code = pick(codes)
    if code:
        m = next(r.search(code["value"]) for r in code_res if r.search(code["value"]))
        code["value"] = m.group().strip()
    return {"found": True, "block": ins.dxf.name, "extents": [round(v, 1) for v in (x0, y0, x1, y1)],
            "code": code, "name": pick([name] if name else []), "material": pick(mats), "scale": pick(scales),
            "mass_candidate": pick([mass] if mass else [])}


def _header_role(s):
    """Exact header match; a key of >= 5 chars may carry a short suffix ("tên gọi - quy cách").
    Measured false hit: the part name "Mã cạnh phao" matched the short key "mã" and cut the table."""
    s = _norm(s)
    for role, keys in HEADER_KEYS.items():
        if any(s == k or (len(k) >= 5 and s.startswith(k + " ") and len(s) <= len(k) + 14) for k in keys):
            return role
    return None


def read_bom_tables(doc, txts=None):
    """Parts-list tables: a header row with >= 4 known column labels, rows stacked above or below it."""
    txts = txts if txts is not None else texts(doc.modelspace(), doc)
    heads = [(t, _header_role(t["text"])) for t in txts]
    heads = [(t, r) for t, r in heads if r]
    rows_by_y = []
    for t, r in heads:
        for grp in rows_by_y:
            if abs(grp[0][0]["y"] - t["y"]) <= max(t["h"], 1.0) * 0.6:
                grp.append((t, r))
                break
        else:
            rows_by_y.append([(t, r)])
    tables = []
    for grp in rows_by_y:
        roles = {}
        for t, r in grp:
            roles.setdefault(r, t)
        if len(roles) < 4 or "name" not in roles:
            continue
        cols = sorted(roles.items(), key=lambda kv: kv[1]["x"])
        xs = [t["x"] for _, t in cols]
        hy = min(t["y"] for _, t in cols)
        h = max(t["h"] for _, t in cols) or 1.0
        bounds = [-1e18] + [(xs[i] + xs[i + 1]) / 2 for i in range(len(xs) - 1)] + [1e18]
        # tight horizontal span: two tables can sit side by side (measured: a parts list left of a second one)
        span = (xs[0] - 3 * h, xs[-1] + 3 * h)
        header_handles = {t["handle"] for _, t in cols}

        def col_of(x):
            for i in range(len(cols)):
                if bounds[i] <= x < bounds[i + 1]:
                    return cols[i][0]
            return None
        cand = [t for t in txts if span[0] <= t["x"] <= span[1] and t["handle"] not in header_handles]
        best = []
        for direction in (+1, -1):
            lines, y, gap = [], hy, 0
            pool = sorted([t for t in cand if (t["y"] - hy) * direction > 0.4 * h], key=lambda t: (t["y"] - hy) * direction)
            ys = []
            for t in pool:
                if ys and abs(t["y"] - ys[-1][0]) <= 0.6 * h:
                    ys[-1][1].append(t)
                else:
                    ys.append([t["y"], [t]])
            prev = hy
            for yy, cell_texts in ys:
                # the first row may sit further from the header (measured: 4 × text height) than rows from each other
                if abs(yy - prev) > (6.0 if prev == hy else 4.0) * h:
                    break
                if sum(bool(_header_role(c["text"])) for c in cell_texts) >= 3:   # another table's header row
                    break
                lines.append(cell_texts)
                prev = yy
            if len(lines) > len(best):
                best = lines
        rows = []
        for cell_texts in best:
            row = {"cells": {}, "locators": {}}
            for c in sorted(cell_texts, key=lambda c: c["x"]):
                role = col_of(c["x"])
                if role is None:
                    continue
                row["cells"][role] = (row["cells"].get(role, "") + " " + c["text"]).strip()
                row["locators"].setdefault(role, _loc(c))
            if len(row["cells"]) >= 2:
                rows.append(row)
        tables.append({"header_y": round(hy, 2), "columns": [r for r, _ in cols], "rows": rows,
                       "header_locator": _loc(cols[0][1])})
    return tables


NICE_SCALES = (0.1, 0.2, 0.25, 0.4, 0.5, 2.0, 2.5, 4.0, 5.0, 10.0)
_COUNT_PREFIX = re.compile(r"(?i)^\s*\d+\s*(?:lỗ|lo|x|×|-)\s*")
_SIZE_AFTER = re.compile(r"(?i)(?:%%c|Ø|⌀|\bR|\bM)\s*(\d+(?:[.,]\d+)?)")
_FIRST_NUM = re.compile(r"-?\d+(?:[.,]\d+)?")


def override_value(text):
    """Numeric value of a dimension text override: drop a count prefix ("4 lỗ Ø12", "4-Ø14"), prefer the number
    after Ø / %%c / R / M, else the first number. Measured: '4 lỗ %%C12' was read as 4."""
    s = _COUNT_PREFIX.sub("", text or "", count=1)
    m = _SIZE_AFTER.search(s) or _FIRST_NUM.search(s)
    return float(m.group(1 if m.re is _SIZE_AFTER else 0).replace(",", ".")) if m else None


def classify_override(value, measured, tol=None):
    """Compare a dimension's displayed text value with its (DIMLFAC-scaled) measurement.
    tol = explicit ± tolerance written in the same dimension text (None if only the general note applies).
    Returns AGREE | WITHIN_TOL | SCALED_VIEW | BREAK_VIEW | TEXT_OVERRIDE.
    General tolerances (e.g. IT14/2) are deliberately NOT applied here — that table belongs to the curated
    standards layer (G2b); without an explicit ± the mismatch is surfaced for a human."""
    if value is None or measured is None or value == 0:
        return "AGREE"
    if abs(measured - value) <= max(0.05, 0.002 * abs(value)):
        return "AGREE"
    if tol is not None and abs(measured - value) <= tol:
        return "WITHIN_TOL"
    ratio = measured / value
    # 2 %: detail views carry rounded text (measured: 36 for 35.6 ×2.5, R41 for 40.6 ×4); 23 vs 22.5 (2.2 %) still flags
    if any(abs(ratio - s) <= 0.02 * s for s in NICE_SCALES):
        return "SCALED_VIEW"
    if measured < 0.9 * value and value - measured > 20:
        return "BREAK_VIEW"
    return "TEXT_OVERRIDE"
