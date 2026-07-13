#!/usr/bin/env python3
"""parse_document.py — Convert PDF / Markdown / Word / Excel into a unified, fidelity-oriented JSON document model.

Part of the KN-Stack `extract` domain. The deterministic extraction (PDF text+tables,
DOCX ordered body walk, XLSX cell grid, Markdown block parse) is codified here
(COD: Offload). The `doc-to-json` SKILL.md orchestrates this script and curates/verifies
its output (COD: Core).

Design goal — *giữ nguyên thông tin* (preserve all information):
  * Reading order is preserved (page order for PDF; XML body order for DOCX; sheet+row
    order for XLSX; line order for Markdown).
  * Structure is kept, not flattened: headings carry levels, tables stay 2-D, lists keep
    nesting, Excel cells keep value + formula + type + format, DOCX runs keep bold/italic.
  * Source metadata + a sha256 of the bytes are recorded for traceability.
  * Nothing the parser cannot map is silently dropped — it lands in `warnings`.

Usage:
    python parse_document.py --in <file> [--out <dir>] [--name <slug>] [--text]

Exit codes: 0 ok | 2 bad input | 3 missing dependency (prints install hint).
"""
import argparse
import hashlib
import json
import os
import re
import sys

SCHEMA_VERSION = "1.0"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _dep_missing(pkg, pip_name=None):
    pip_name = pip_name or pkg
    sys.stderr.write(
        "[!] Missing dependency '%s'. Install it with:\n    pip install %s\n"
        % (pkg, pip_name)
    )
    sys.exit(3)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def kebab(s):
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip().lower()
    return re.sub(r"[\s_]+", "-", s) or "document"


def new_envelope(path, fmt):
    st = os.stat(path)
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "path": os.path.abspath(path),
            "filename": os.path.basename(path),
            "format": fmt,
            "bytes": st.st_size,
            "sha256": sha256_of(path),
        },
        "metadata": {},
        "blocks": [],        # unified reading-order stream (PDF / DOCX / MD)
        "sheets": [],        # spreadsheet grids (XLSX)
        "text": "",          # full plain-text dump for grep / quick check
        "stats": {},
        "warnings": [],
    }


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------
def parse_markdown(path, env):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    env["text"] = raw
    lines = raw.split("\n")
    i = 0
    n = len(lines)

    # YAML frontmatter
    if lines and lines[0].strip() == "---":
        end = None
        for j in range(1, n):
            if lines[j].strip() in ("---", "..."):
                end = j
                break
        if end is not None:
            fm = "\n".join(lines[1:end])
            env["metadata"]["frontmatter_raw"] = fm
            env["metadata"]["frontmatter"] = _naive_yaml(fm)
            i = end + 1

    blocks = env["blocks"]
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # blank
        if not stripped:
            i += 1
            continue

        # fenced code
        m = re.match(r"^(```+|~~~+)(.*)$", stripped)
        if m:
            fence = m.group(1)[0]
            lang = m.group(2).strip() or None
            buf = []
            i += 1
            while i < n and not lines[i].strip().startswith(fence * 3):
                buf.append(lines[i])
                i += 1
            i += 1  # closing fence
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(buf)})
            continue

        # ATX heading
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*$", stripped)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2)})
            i += 1
            continue

        # horizontal rule
        if re.match(r"^(\*\s*){3,}$|^(-\s*){3,}$|^(_\s*){3,}$", stripped):
            blocks.append({"type": "rule"})
            i += 1
            continue

        # table (header row followed by a separator row of ---|---)
        if "|" in stripped and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            header = _split_md_row(stripped)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(_split_md_row(lines[i]))
                i += 1
            blocks.append({
                "type": "table", "header": header, "rows": rows,
                "n_rows": len(rows), "n_cols": len(header),
            })
            continue

        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            blocks.append({"type": "blockquote", "text": "\n".join(buf)})
            continue

        # list (consecutive bullet/ordered items, nesting by indent)
        if re.match(r"^\s*([-*+]|\d+[.)])\s+", line):
            items = []
            ordered = bool(re.match(r"^\s*\d+[.)]\s+", line))
            while i < n and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[i]):
                indent = len(lines[i]) - len(lines[i].lstrip())
                text = re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[i])
                items.append({"text": text, "level": indent // 2})
                i += 1
            blocks.append({"type": "list", "ordered": ordered, "items": items})
            continue

        # paragraph (gather until blank or next block-starter)
        buf = []
        while i < n and lines[i].strip() and not re.match(
            r"^(#{1,6}\s|\s*([-*+]|\d+[.)])\s|>|```|~~~)", lines[i]
        ):
            buf.append(lines[i])
            i += 1
        blocks.append({"type": "paragraph", "text": "\n".join(buf)})

    env["stats"] = _block_stats(blocks)
    return env


def _split_md_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _naive_yaml(text):
    """Best-effort flat key: value parse (no external YAML dep). Lists kept as raw string."""
    out = {}
    for ln in text.split("\n"):
        m = re.match(r"^([A-Za-z0-9_.-]+)\s*:\s*(.*)$", ln)
        if m:
            key, val = m.group(1), m.group(2).strip()
            val = val.strip('"\'')
            out[key] = val
    return out


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def parse_pdf(path, env):
    try:
        import pdfplumber
    except ImportError:
        _dep_missing("pdfplumber")

    blocks = env["blocks"]
    pages_meta = []
    text_parts = []
    total_chars = 0

    with pdfplumber.open(path) as pdf:
        if pdf.metadata:
            env["metadata"] = {k: str(v) for k, v in pdf.metadata.items()}
        n_pages = len(pdf.pages)
        for idx, page in enumerate(pdf.pages, start=1):
            ptext = page.extract_text() or ""
            total_chars += len(ptext)
            text_parts.append(ptext)
            try:
                tables = page.extract_tables() or []
            except Exception as e:  # pragma: no cover - pdfplumber edge cases
                tables = []
                env["warnings"].append("page %d table extraction failed: %s" % (idx, e))

            pages_meta.append({
                "page_number": idx,
                "width": round(float(page.width), 2),
                "height": round(float(page.height), 2),
                "char_count": len(ptext),
                "table_count": len(tables),
            })

            # reading-order blocks: paragraphs (blank-line split) then tables
            for para in re.split(r"\n\s*\n", ptext):
                para = para.strip()
                if para:
                    blocks.append({"type": "paragraph", "text": para, "page": idx})
            for t in tables:
                rows = [[("" if c is None else c) for c in row] for row in t]
                header = rows[0] if rows else []
                blocks.append({
                    "type": "table", "page": idx,
                    "header": header, "rows": rows[1:] if len(rows) > 1 else [],
                    "n_rows": max(0, len(rows) - 1), "n_cols": len(header),
                })
            if idx < n_pages:
                blocks.append({"type": "pagebreak", "after_page": idx})

    env["text"] = "\n\n".join(text_parts)
    env["pages"] = pages_meta

    scanned = n_pages > 0 and (total_chars / n_pages) < 20
    repl = env["text"].count("�")
    mojibake_ratio = (repl / max(1, len(env["text"])))
    env["pdf_quality"] = {
        "page_count": n_pages,
        "total_chars": total_chars,
        "avg_chars_per_page": round(total_chars / n_pages, 1) if n_pages else 0,
        "scanned_no_text_layer": scanned,
        "replacement_char_count": repl,
        "mojibake_ratio": round(mojibake_ratio, 4),
        "encoding_warning": mojibake_ratio > 0.02,
    }
    if scanned:
        env["warnings"].append(
            "PDF appears scanned / image-only (low text yield) — read it visually; "
            "OCR is out of scope for this parser."
        )
    if env["pdf_quality"]["encoding_warning"]:
        env["warnings"].append(
            "PDF text contains many replacement chars (possible legacy-font mojibake) — "
            "verify visually; do not trust the extracted text."
        )
    env["stats"] = _block_stats(blocks)
    return env


# ---------------------------------------------------------------------------
# Word (.docx)
# ---------------------------------------------------------------------------
def parse_docx(path, env):
    try:
        import docx  # python-docx
        from docx.text.paragraph import Paragraph
    except ImportError:
        _dep_missing("docx", "python-docx")

    document = docx.Document(path)

    # core properties metadata
    cp = document.core_properties
    md = {}
    for field in ("title", "author", "subject", "keywords", "category",
                  "comments", "last_modified_by", "revision"):
        val = getattr(cp, field, None)
        if val:
            md[field] = str(val)
    for field in ("created", "modified"):
        val = getattr(cp, field, None)
        if val:
            md[field] = val.isoformat()
    env["metadata"] = md

    blocks = env["blocks"]
    text_parts = []
    body = document.element.body

    # Walk body children in document order so paragraphs and tables stay interleaved.
    for child in body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            para = Paragraph(child, document)
            block = _docx_paragraph(para)
            if block is not None:
                blocks.append(block)
                text_parts.append(block.get("text", ""))
        elif tag == "tbl":
            block = _docx_table(child)
            blocks.append(block)
            # text dump: anchor text only (spanned cells are blank), drop empty rows
            for r in [block["header"]] + block["rows"]:
                line = "\t".join(c for c in r if c)
                if line:
                    text_parts.append(line)

    # collapse list-ish runs of paragraphs? keep them explicit instead (fidelity > tidiness)
    env["text"] = "\n".join(t for t in text_parts if t)
    env["stats"] = _block_stats(blocks)
    return env


def _docx_paragraph(para):
    text = para.text
    style = (para.style.name if para.style else "") or ""
    runs = []
    for r in para.runs:
        if not r.text:
            continue
        runs.append({
            "text": r.text,
            "bold": bool(r.bold),
            "italic": bool(r.italic),
            "underline": bool(r.underline),
        })

    m = re.match(r"^Heading\s+(\d+)$", style)
    if m:
        return {"type": "heading", "level": int(m.group(1)), "text": text, "style": style}
    if style.lower().startswith("title"):
        return {"type": "heading", "level": 0, "text": text, "style": style}
    if style.lower().startswith("list"):
        return {"type": "list_item", "text": text, "style": style}
    if not text.strip() and not runs:
        return None  # truly empty paragraph — skip but it carried no info
    block = {"type": "paragraph", "text": text}
    if style and style != "Normal":
        block["style"] = style
    if any(r["bold"] or r["italic"] or r["underline"] for r in runs):
        block["runs"] = runs
    return block


def _tc_text(tc):
    """Text of a <w:tc> cell: its direct paragraphs joined by newline (nested tables ignored)."""
    from docx.oxml.ns import qn
    paras = tc.findall(qn("w:p"))
    out = []
    for p in paras:
        out.append("".join((t.text or "") for t in p.iter(qn("w:t"))))
    return "\n".join(out).strip()


def _docx_table(tbl):
    """Walk a <w:tbl> at the XML level so merged cells are recorded, not duplicated.

    OOXML repeats a merged cell's text across every column/row it spans
    (python-docx's `row.cells` reflects this). We instead keep the full logical
    grid geometry but place the text only at each merge **anchor**; spanned
    positions are blank, and the spans are listed in `merged_cells` as
    'R{r0}C{c0}:R{r1}C{c1}' (0-based) — mirroring the XLSX `merged_cells` model.
    """
    from docx.oxml.ns import qn
    trs = tbl.findall(qn("w:tr"))
    matrix = []            # row -> list (len = grid width) of cell-dict | None
    vactive = {}           # grid_col -> anchor cell dict (open vertical merge)
    n_cols = 0

    for r_idx, tr in enumerate(trs):
        row = []
        c_idx = 0
        for tc in tr.findall(qn("w:tc")):
            tcPr = tc.find(qn("w:tcPr"))
            grid_span = 1
            vmerge = None
            if tcPr is not None:
                gs = tcPr.find(qn("w:gridSpan"))
                if gs is not None:
                    try:
                        grid_span = int(gs.get(qn("w:val")))
                    except (TypeError, ValueError):
                        grid_span = 1
                vm = tcPr.find(qn("w:vMerge"))
                if vm is not None:
                    vmerge = vm.get(qn("w:val")) or "continue"

            if vmerge == "continue":
                anchor = vactive.get(c_idx)
                if anchor is not None:
                    anchor["rowspan"] = r_idx - anchor["r"] + 1
                row.extend([None] * grid_span)
                c_idx += grid_span
                continue

            cell = {"r": r_idx, "c": c_idx, "rowspan": 1,
                    "colspan": grid_span, "text": _tc_text(tc)}
            row.append(cell)
            row.extend([None] * (grid_span - 1))
            if vmerge == "restart":
                vactive[c_idx] = cell
            else:
                vactive.pop(c_idx, None)
            c_idx += grid_span

        matrix.append(row)
        n_cols = max(n_cols, c_idx)

    # text grid (anchor text + blanks) and merge-range list
    def text_grid(rows):
        out = []
        for row in rows:
            line = []
            for j in range(n_cols):
                cell = row[j] if j < len(row) else None
                line.append(cell["text"] if isinstance(cell, dict) else "")
            out.append(line)
        return out

    merged = []
    for row in matrix:
        for cell in row:
            if isinstance(cell, dict) and (cell["rowspan"] > 1 or cell["colspan"] > 1):
                r0, c0 = cell["r"], cell["c"]
                r1 = r0 + cell["rowspan"] - 1
                c1 = c0 + cell["colspan"] - 1
                merged.append("R%dC%d:R%dC%d" % (r0, c0, r1, c1))

    grid = text_grid(matrix)
    header = grid[0] if grid else []
    block = {
        "type": "table",
        "header": header,
        "rows": grid[1:] if len(grid) > 1 else [],
        "n_rows": max(0, len(grid) - 1),
        "n_cols": n_cols,
    }
    if merged:
        block["merged_cells"] = merged
    return block


# ---------------------------------------------------------------------------
# Excel (.xlsx)
# ---------------------------------------------------------------------------
def parse_xlsx(path, env):
    try:
        import openpyxl
    except ImportError:
        _dep_missing("openpyxl")

    # formulas (data_only=False) + cached values (data_only=True) → keep both.
    wb_f = openpyxl.load_workbook(path, data_only=False, read_only=False)
    try:
        wb_v = openpyxl.load_workbook(path, data_only=True, read_only=False)
    except Exception:
        wb_v = None

    props = wb_f.properties
    md = {}
    for field in ("title", "creator", "lastModifiedBy", "subject", "keywords", "category"):
        val = getattr(props, field, None)
        if val:
            md[field] = str(val)
    for field in ("created", "modified"):
        val = getattr(props, field, None)
        if val:
            md[field] = val.isoformat()
    env["metadata"] = md

    text_parts = []
    for ws in wb_f.worksheets:
        ws_v = wb_v[ws.title] if wb_v and ws.title in wb_v.sheetnames else None
        dims = ws.dimensions
        max_row, max_col = ws.max_row, ws.max_column
        cells = []
        grid = []
        for ri, row in enumerate(ws.iter_rows(), start=1):
            grid_row = []
            for cell in row:
                v = cell.value
                cached = None
                if ws_v is not None:
                    try:
                        cached = ws_v.cell(row=cell.row, column=cell.column).value
                    except Exception:
                        cached = None
                display = cached if cached is not None else v
                grid_row.append("" if display is None else display)
                if v is None and cached is None:
                    continue
                rec = {
                    "ref": cell.coordinate,
                    "row": cell.row,
                    "col": cell.column,
                    "type": cell.data_type,  # f=formula s=str n=num b=bool d=date
                }
                if isinstance(v, str) and v.startswith("="):
                    rec["formula"] = v
                    rec["value"] = cached
                else:
                    rec["value"] = _jsonable(v)
                if cell.number_format and cell.number_format != "General":
                    rec["number_format"] = cell.number_format
                cells.append(rec)
            grid.append([_jsonable(x) for x in grid_row])

        merged = [str(rng) for rng in ws.merged_cells.ranges]
        env["sheets"].append({
            "name": ws.title,
            "dimensions": dims,
            "n_rows": max_row,
            "n_cols": max_col,
            "state": ws.sheet_state,        # visible / hidden
            "merged_cells": merged,
            "grid": grid,                   # 2-D values (cached where formulas)
            "cells": cells,                 # non-empty cells w/ formula+type+format
        })
        text_parts.append("# Sheet: %s" % ws.title)
        for grid_row in grid:
            text_parts.append("\t".join("" if c is None else str(c) for c in grid_row))

    env["text"] = "\n".join(text_parts)
    env["stats"] = {
        "sheet_count": len(env["sheets"]),
        "total_cells": sum(len(s["cells"]) for s in env["sheets"]),
        "formula_cells": sum(
            1 for s in env["sheets"] for c in s["cells"] if "formula" in c
        ),
    }
    return env


def _jsonable(v):
    import datetime
    if isinstance(v, (datetime.datetime, datetime.date, datetime.time)):
        return v.isoformat()
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return str(v)


# ---------------------------------------------------------------------------
# shared
# ---------------------------------------------------------------------------
def _block_stats(blocks):
    counts = {}
    for b in blocks:
        counts[b["type"]] = counts.get(b["type"], 0) + 1
    return {"block_count": len(blocks), "block_types": counts}


FORMATS = {
    ".md": ("markdown", parse_markdown),
    ".markdown": ("markdown", parse_markdown),
    ".pdf": ("pdf", parse_pdf),
    ".docx": ("docx", parse_docx),
    ".xlsx": ("xlsx", parse_xlsx),
}


def main():
    ap = argparse.ArgumentParser(description="Convert PDF/MD/Word/Excel → unified JSON.")
    ap.add_argument("--in", dest="infile", required=True, help="source document")
    ap.add_argument("--out", default=".", help="output directory (default: cwd)")
    ap.add_argument("--name", help="output slug (default: derived from filename)")
    ap.add_argument("--text", action="store_true", help="also write <name>.txt full-text dump")
    args = ap.parse_args()

    path = args.infile
    if not os.path.isfile(path):
        sys.stderr.write("[!] Input not found: %s\n" % path)
        sys.exit(2)

    ext = os.path.splitext(path)[1].lower()
    if ext == ".xls":
        sys.stderr.write(
            "[!] Legacy .xls is unsupported. Open in Excel -> Save As .xlsx, then re-run.\n"
        )
        sys.exit(2)
    if ext == ".doc":
        sys.stderr.write(
            "[!] Legacy .doc is unsupported. Open in Word → Save As .docx, then re-run.\n"
        )
        sys.exit(2)
    if ext not in FORMATS:
        sys.stderr.write(
            "[!] Unsupported format '%s'. Supported: .pdf .md .markdown .docx .xlsx\n" % ext
        )
        sys.exit(2)

    fmt, parser = FORMATS[ext]
    env = new_envelope(path, fmt)
    parser(path, env)

    name = args.name or kebab(os.path.splitext(os.path.basename(path))[0])
    os.makedirs(args.out, exist_ok=True)
    out_json = os.path.join(args.out, name + ".json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(env, f, ensure_ascii=False, indent=2)

    if args.text:
        out_txt = os.path.join(args.out, name + ".txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(env.get("text", ""))

    # one-line summary (ascii-safe for legacy Windows consoles)
    if fmt == "xlsx":
        summary = "%d sheets, %d cells (%d formulas)" % (
            env["stats"].get("sheet_count", 0),
            env["stats"].get("total_cells", 0),
            env["stats"].get("formula_cells", 0),
        )
    else:
        bt = env["stats"].get("block_types", {})
        summary = "%d blocks [%s]" % (
            env["stats"].get("block_count", 0),
            ", ".join("%s:%d" % (k, v) for k, v in sorted(bt.items())),
        )
    warn = "  WARNINGS: %d" % len(env["warnings"]) if env["warnings"] else ""
    sys.stdout.write("[ok] %s -> %s | %s%s\n" % (fmt, out_json, summary, warn))


if __name__ == "__main__":
    main()
