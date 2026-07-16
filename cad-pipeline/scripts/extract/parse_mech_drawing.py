#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_mech_drawing.py — Codified parser for mechanical-drawing extraction.

Backs the `mech-drawing-extract` skill (extract domain). Reads an engineering
drawing supplied as a PDF and/or a DXF and emits a single structured JSON file
describing everything machine-recoverable from the files: title-block text,
dimensions, tolerances/GD&T hints, notes, layers, entity inventory, drawing
extents and units. The skill (LLM) then interprets that JSON into a curated
human-readable .md datasheet — the script never guesses, it only reports what
the bytes contain plus a confidence-friendly inventory.

Naval code-leverage: the deterministic, repeatable parsing (DXF entity walk,
PDF word/table extraction, title-block region heuristics) is done once in code
instead of re-derived by the model on every run.

Usage:
    python parse_mech_drawing.py --dxf part.dxf --pdf part.pdf \
        --out ./extracted --name bracket-A

    python parse_mech_drawing.py --pdf only.pdf --out ./extracted
    python parse_mech_drawing.py --dxf only.dxf --out ./extracted --md
    python parse_mech_drawing.py --dwg part.dwg --out ./extracted   # needs ODA File Converter

Dependencies (install on demand; both are optional per-format):
    pip install ezdxf pdfplumber

DWG input additionally needs the free ODA File Converter on the machine
(ezdxf cannot read DWG natively); install it with:
    winget install --id ODA.ODAFileConverter
DWG geometry is converted to DXF in memory and reported under the same
"dxf" key as a native DXF (stamped converted_from_dwg=true).

Exit codes:
    0  success (JSON written)
    2  no input file given / inputs missing
    3  a required library for a requested format is not installed
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# ----------------------------------------------------------------------------
# Regex heuristics shared across PDF + DXF text
# ----------------------------------------------------------------------------

# Linear tolerance like  25 ±0.05   or  25.0+/-0.1
RE_TOL_SYM = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:±|\+/-|\+-)\s*(\d+(?:[.,]\d+)?)")
# Bilateral tolerance like  50 +0.02 -0.01  (two signed values)
RE_TOL_BILAT = re.compile(r"(\d+(?:[.,]\d+)?)\s*\+(\d+(?:[.,]\d+)?)\s*-(\d+(?:[.,]\d+)?)")
# Diameter / radius callouts
RE_DIA = re.compile(r"[Ø⌀∅]\s*\d+(?:[.,]\d+)?")
RE_RAD = re.compile(r"\bR\s*\d+(?:[.,]\d+)?")
# ISO fit / limit grades. Hole fits = UPPERCASE letters (H7, F7) — M and R are
# excluded because uppercase M is a thread (M8) and uppercase R a radius (R5).
# Shaft fits = lowercase letters (h7, m6, r6) — here m/r ARE included because
# lowercase has no thread/radius collision. So Ø40m6 and Ø30h7 are caught while
# M12 (thread) and R23 (radius) are not. No internal whitespace ("25  R5" ≠ fit).
RE_FIT = re.compile(r"\b\d{0,3}(?:[HGFJKNPSEU]|[hgfjknpsmru])\d{1,2}\b")
# Toleranced bore/shaft = diameter WITH a fit grade, e.g. Ø25H7, Ø40 m6, Ø30h7.
# Highest-value spec for machined parts — keep the diameter and fit together.
RE_DIA_FIT = re.compile(r"[Ø⌀∅]\s*\d+(?:[.,]\d+)?\s*(?:[HGFJKNPSEU]|[hgfjknpsmru])\d{1,2}\b")
# Chamfer callout, e.g. C1, C0.5, C2, C1,5. Single leading digit so the steel
# grade "C45" (THÉP C45) and "CT1/CT2" are NOT mistaken for chamfers.
RE_CHAMFER = re.compile(r"\bC\s*\d(?:[.,]\d+)?\b")
# Thread callouts, e.g. M8, M10x1.25, M6-6H
RE_THREAD = re.compile(r"\bM\d+(?:[.,]\d+)?(?:\s*[xX]\s*\d+(?:[.,]\d+)?)?(?:-\w+)?\b")
# Surface finish — Ra / Rz / Rt / Rq (µm)
RE_RA = re.compile(r"\bR[aztq]\s*\d+(?:[.,]\d+)?", re.IGNORECASE)
# GD&T frame leading symbols (unicode geometric tolerancing chars)
GDT_SYMBOLS = "⏤⏥○⌭⌒⌓⌔∠⊥∥⌖◎⫽⌯⌰"
RE_GDT = re.compile(f"[{GDT_SYMBOLS}]")

# Common title-block field labels (English + Vietnamese)
TITLE_LABELS = [
    "drawing no", "drawing number", "dwg no", "dwg", "part no", "part number",
    "part name", "title", "scale", "material", "mat", "finish", "treatment",
    "rev", "revision", "sheet", "weight", "mass", "drawn", "checked",
    "approved", "date", "tolerance", "general tolerance", "unit", "units",
    # Vietnamese
    "ban ve", "bản vẽ", "so ban ve", "số bản vẽ", "ten chi tiet", "tên chi tiết",
    "ten ban ve", "tên bản vẽ", "vat lieu", "vật liệu", "ty le", "tỷ lệ",
    "khoi luong", "khối lượng", "nguoi ve", "người vẽ", "kiem tra", "kiểm tra",
    "phe duyet", "phê duyệt", "ngay", "ngày", "dung sai", "dung sai chung",
    "phien ban", "phiên bản", "lan sua", "lần sửa", "do nham", "độ nhám",
    "xu ly be mat", "xử lý bề mặt", "don vi", "đơn vị",
]


def _norm_num(s: str) -> str:
    return s.replace(",", ".").strip()


# AutoCAD DTEXT/TEXT inline control codes. %%c/%%d/%%p carry meaning (Ø/°/±) and
# must be decoded; %%u/%%o/%%k are formatting toggles (underline/overline/strike)
# that otherwise leak as junk — e.g. "%%U1" surfaces "U1" and gets mis-read as an
# ISO fit grade. plain_mtext() handles MTEXT; DTEXT needs this explicit pass.
_DTEXT_REPL = (("%%c", "Ø"), ("%%C", "Ø"), ("%%d", "°"), ("%%D", "°"),
               ("%%p", "±"), ("%%P", "±"), ("%%%", "%"))


def clean_dtext(s: str) -> str:
    """Decode meaningful AutoCAD %% codes and drop formatting toggles."""
    if not s:
        return s
    for code, ch in _DTEXT_REPL:
        s = s.replace(code, ch)
    # toggles: %%u %%o %%k (any case) — remove the marker, keep the text
    s = re.sub(r"%%[uokUOK]", "", s)
    return s


# ----------------------------------------------------------------------------
# TCVN3 (ABC / .VnTime) legacy-font decoding
# ----------------------------------------------------------------------------
# Legacy Vietnamese CAD/Office files store text in the TCVN3 8-bit charset:
# Vietnamese diacritic letters live in the cp1252 high-byte range, so ezdxf
# (reading with the DXF's ANSI_1252 codepage) yields mojibake like
# "thÐp hép" for "thép hộp". The byte→Unicode table below is the canonical
# TCVN3 mapping (validated char-for-char against real VTI drawings).
#
# Critically, a single drawing often MIXES TCVN3 text (old BOM rows) with
# already-correct Unicode (newer title-block templates). The Latin-1 letters
# à á é ê ù … are valid in BOTH, so blanket decoding corrupts the clean
# strings. We therefore decode a string ONLY if it contains a TCVN3 "marker"
# char — a Latin-1 symbol / non-Vietnamese letter that cannot appear in clean
# Vietnamese (® · ¸ ª Ð Þ …). Clean Unicode strings have none and pass through.
_TCVN3_SRC = ("µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîï"
              "óñòô\xadõøö÷ùúýûüþ¡¢§£¤¥¦")
_TCVN3_DST = ("àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
              "ùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ")
assert len(_TCVN3_SRC) == len(_TCVN3_DST)
# Byte 0xD8 is BOTH the diameter symbol Ø and TCVN3 'ỉ'. Ø is ubiquitous in
# drawings (and clean_dtext produces it from %%C), whereas 'ỉ' is rare in part
# names — so we never remap Ø (keeping "Ø100" intact beats decoding a rare ỉ).
_TCVN3_PROTECT = {"Ø"}
_TCVN3_MAP = {s: d for s, d in zip(_TCVN3_SRC, _TCVN3_DST)
              if s not in _TCVN3_PROTECT}
# Real precomposed Vietnamese Latin-1 letters — ambiguous (valid in clean text
# too), so their presence ALONE does not prove a string is TCVN3.
_VIET_LATIN1 = set("àáâãèéêìíòóôõùúýÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝ")
# Marker set: TCVN3 source chars that are NOT real Vietnamese letters → an
# unambiguous "this string is TCVN3-garbled" signal.
_TCVN3_MARKERS = set(_TCVN3_SRC) - _VIET_LATIN1 - _TCVN3_PROTECT


def decode_tcvn3(s: str) -> str:
    """Decode a TCVN3-garbled string to Unicode; pass clean strings through.

    Returns ``s`` unchanged unless it carries a TCVN3 marker char (avoids
    corrupting strings that are already correct Unicode)."""
    if not s or not any(c in _TCVN3_MARKERS for c in s):
        return s
    return "".join(_TCVN3_MAP.get(c, c) for c in s)


def mojibake_ratio(text: str) -> float:
    """Fraction of letters in the Latin Extended-B range (U+0180–024F).

    Legacy Vietnamese CAD fonts (TCVN3/VNI) export a garbled PDF text layer
    full of these chars (e.g. 'TǌM Cũ SȆ' for 'TẤM CƠ SỞ'). Correct Vietnamese
    uses precomposed Latin Extended Additional (U+1E00–1EFF) instead, so a high
    ratio here is a reliable mojibake signal."""
    letters = [c for c in text if c.isalpha()]
    if not letters:
        return 0.0
    sus = sum(1 for c in letters if 0x0180 <= ord(c) <= 0x024F)
    return sus / len(letters)


def scan_text_for_specs(text: str) -> dict:
    """Pull dimension/tolerance/GD&T/thread/finish signals out of free text."""
    tols = []
    for m in RE_TOL_BILAT.finditer(text):
        tols.append({
            "type": "bilateral",
            "nominal": _norm_num(m.group(1)),
            "upper": "+" + _norm_num(m.group(2)),
            "lower": "-" + _norm_num(m.group(3)),
            "raw": m.group(0).strip(),
        })
    for m in RE_TOL_SYM.finditer(text):
        tols.append({
            "type": "symmetric",
            "nominal": _norm_num(m.group(1)),
            "tolerance": "±" + _norm_num(m.group(2)),
            "raw": m.group(0).strip(),
        })
    return {
        "tolerances": tols,
        "diameters": sorted({m.group(0).strip() for m in RE_DIA.finditer(text)}),
        "diameter_fits": sorted({re.sub(r"\s+", "", m.group(0))
                                 for m in RE_DIA_FIT.finditer(text)}),
        "radii": sorted({m.group(0).strip() for m in RE_RAD.finditer(text)}),
        "iso_fits": sorted({m.group(0).strip() for m in RE_FIT.finditer(text)}),
        "threads": sorted({m.group(0).strip() for m in RE_THREAD.finditer(text)}),
        "chamfers": sorted({re.sub(r"\s+", "", m.group(0))
                            for m in RE_CHAMFER.finditer(text)}),
        "surface_finish_ra": sorted({m.group(0).strip() for m in RE_RA.finditer(text)}),
        "gdt_frames_detected": len(RE_GDT.findall(text)),
    }


def find_title_block_fields(lines: list[str]) -> list[dict]:
    """Heuristic: lines that contain a known label followed by a value."""
    found = []
    for ln in lines:
        low = ln.lower()
        for label in TITLE_LABELS:
            if label in low:
                # value = text after the label / after a separator
                idx = low.find(label)
                tail = ln[idx + len(label):].lstrip(" :\t-=").strip()
                if tail:
                    found.append({"label": label, "value": tail, "source_line": ln.strip()})
                break
    return found


# ----------------------------------------------------------------------------
# DXF parsing (ezdxf)
# ----------------------------------------------------------------------------

INSUNITS = {
    0: "unitless", 1: "inch", 2: "feet", 4: "mm", 5: "cm", 6: "m",
    8: "microinch", 9: "mil", 10: "yard", 11: "angstrom", 12: "nm",
    13: "micron", 14: "dm", 21: "us_survey_foot",
}


def parse_dxf(path: str) -> dict:
    """Read a native DXF file and walk it into the JSON dict."""
    try:
        import ezdxf
    except ImportError:
        raise RuntimeError("ezdxf not installed. Run: pip install ezdxf")
    doc = ezdxf.readfile(path)
    return _walk_dxf_doc(doc, os.path.basename(path))


def parse_dwg(path: str) -> dict:
    """Read a DWG by converting it to DXF via the ODA File Converter.

    ezdxf cannot read DWG natively, so DWG support is delegated to the free
    ODA File Converter through the ezdxf ``odafc`` addon. The converted
    in-memory DXF document is walked by the *exact same* code path as a native
    DXF, so the JSON contract is identical (geometry lands under
    ``result["dxf"]``); we only stamp ``converted_from_dwg`` so the reader
    knows the geometry arrived via conversion.
    """
    try:
        import ezdxf
        from ezdxf.addons import odafc
    except ImportError:
        raise RuntimeError("ezdxf not installed. Run: pip install ezdxf")
    # ezdxf only checks the unversioned default path; winget/MSI installs land in
    # a versioned folder (e.g. "ODAFileConverter 27.1.0"). Locate the real exe
    # and point ezdxf at it before checking, so a standard install just works.
    if not odafc.is_installed():
        for base in (r"C:\Program Files\ODA", r"C:\Program Files (x86)\ODA"):
            if not os.path.isdir(base):
                continue
            import glob
            hits = sorted(glob.glob(os.path.join(base, "*", "ODAFileConverter.exe")))
            if hits:
                ezdxf.options.set("odafc-addon", "win_exec_path", f'"{hits[-1]}"')
                break
    if not odafc.is_installed():
        raise RuntimeError(
            "DWG support requires the ODA File Converter (free) - ezdxf cannot "
            "read DWG natively.\n"
            "  Install via winget:  winget install --id ODA.ODAFileConverter\n"
            "  or download:         https://www.opendesign.com/guestfiles/oda_file_converter\n"
            "  Then re-run with --dwg. Alternatively, open the DWG in your CAD "
            "app, 'Save As' DXF, and pass --dxf instead."
        )
    try:
        doc = odafc.readfile(path)
    except Exception as e:  # ODAFCError / UnsupportedVersion / conversion failure
        raise RuntimeError(
            f"ODA File Converter failed to read {os.path.basename(path)}: {e}"
        )
    result = _walk_dxf_doc(doc, os.path.basename(path))
    result["converted_from_dwg"] = True
    result["original_dwg"] = os.path.basename(path)
    return result


def _walk_dxf_doc(doc, source_file: str) -> dict:
    """Walk an ezdxf Drawing (native DXF or DWG-converted) into the JSON dict.

    Shared by ``parse_dxf`` and ``parse_dwg`` so both formats produce an
    identical structure.
    """
    msp = doc.modelspace()

    # units
    insunits = int(doc.header.get("$INSUNITS", 0))
    units = INSUNITS.get(insunits, f"code_{insunits}")

    # extents — prefer header $EXTMIN/$EXTMAX, but those carry an uninitialized
    # sentinel (±1e20) on drawings that were never audited/zoom-extents'd, so
    # validate and fall back to computing the entity bounding box.
    def _valid(pt) -> bool:
        return pt is not None and all(abs(c) < 1e19 for c in (pt[0], pt[1]))

    extents = None
    emin = doc.header.get("$EXTMIN")
    emax = doc.header.get("$EXTMAX")
    if _valid(emin) and _valid(emax):
        lo, hi = emin, emax
    else:
        lo = hi = None
        try:
            from ezdxf import bbox
            cache = bbox.extents(msp)
            if cache.has_data:
                lo, hi = cache.extmin, cache.extmax
        except Exception:
            lo = hi = None
    if lo is not None and hi is not None:
        extents = {
            "min": [round(lo[0], 4), round(lo[1], 4)],
            "max": [round(hi[0], 4), round(hi[1], 4)],
            "width": round(hi[0] - lo[0], 4),
            "height": round(hi[1] - lo[1], 4),
        }

    # layers
    layers = [{"name": ly.dxf.name, "color": getattr(ly.dxf, "color", None)}
              for ly in doc.layers]

    # helper to strip MTEXT/dimension inline formatting codes (\fFont|..;text)
    try:
        from ezdxf.tools.text import plain_mtext as _plain
    except Exception:
        def _plain(s):  # noqa: ANN001
            return s

    # entity inventory + text harvest
    entity_counts: dict[str, int] = {}
    texts: list[str] = []            # free TEXT/MTEXT — title block + notes corpus
    dim_texts: list[str] = []        # cleaned dimension override text (specs corpus)
    dimensions: list[dict] = []
    blocks_inserted: dict[str, int] = {}
    block_attributes: list[dict] = []  # title-block / callout fields live here

    for e in msp:
        et = e.dxftype()
        entity_counts[et] = entity_counts.get(et, 0) + 1

        if et == "TEXT":
            t = clean_dtext(e.dxf.text)
            if t:
                texts.append(t)
        elif et == "MTEXT":
            try:
                t = e.plain_text()
            except Exception:
                t = _plain(e.text)
            if t:
                texts.append(t)
        elif et == "DIMENSION":
            raw = e.dxf.text or ""
            cleaned = _plain(raw).strip()
            d = {"raw_text": raw, "text": cleaned}
            try:
                d["measurement"] = round(float(e.get_measurement()), 4)
            except Exception:
                d["measurement"] = None
            d["style"] = getattr(e.dxf, "dimstyle", None)
            dimensions.append(d)
            # override text often carries the real tolerance, e.g. "4250±3"
            if cleaned and cleaned not in ("<>", ""):
                dim_texts.append(cleaned)
        elif et == "INSERT":
            name = getattr(e.dxf, "name", "?")
            blocks_inserted[name] = blocks_inserted.get(name, 0) + 1
            # block ATTRIBs = title-block fields, surface-finish callouts, etc.
            try:
                for a in e.attribs:
                    tag = getattr(a.dxf, "tag", "")
                    val = getattr(a.dxf, "text", "")
                    if val:
                        block_attributes.append({"block": name, "tag": tag, "value": val})
                        texts.append(val)  # feed value into title-block + spec scan
            except Exception:
                pass

    # scan definitions of inserted blocks — surface-finish symbols (Rz/Ra) and
    # title-block templates frequently live inside the block, not in modelspace.
    block_def_text: dict[str, list[str]] = {}
    for name in blocks_inserted:
        blk = doc.blocks.get(name) if hasattr(doc.blocks, "get") else None
        if blk is None:
            continue
        collected = []
        for be in blk:
            bt = be.dxftype()
            if bt == "TEXT" and be.dxf.text:
                collected.append(clean_dtext(be.dxf.text))
            elif bt == "MTEXT":
                try:
                    t = be.plain_text()
                except Exception:
                    t = _plain(be.text)
                if t:
                    collected.append(t)
            elif bt == "ATTDEF":
                v = getattr(be.dxf, "text", "")
                if v:
                    collected.append(v)
        if collected:
            block_def_text[name] = collected

    # TCVN3 decode pass — turn legacy-font mojibake (e.g. "thÐp hép") into
    # clean Unicode ("thép hộp") for the human-facing text. Marker-gated so
    # already-Unicode strings (title block) are left untouched. Raw originals
    # are preserved for traceability.
    texts_raw = list(texts)
    tcvn3_hits = 0

    def _decode_list(lst: list) -> list:
        nonlocal tcvn3_hits
        out = []
        for s in lst:
            d = decode_tcvn3(s)
            if d != s:
                tcvn3_hits += 1
            out.append(d)
        return out

    texts = _decode_list(texts)
    dim_texts = _decode_list(dim_texts)
    for _name, _vals in block_def_text.items():
        block_def_text[_name] = _decode_list(_vals)
    for _ba in block_attributes:
        _d = decode_tcvn3(_ba["value"])
        if _d != _ba["value"]:
            _ba["value_raw"] = _ba["value"]
            _ba["value"] = _d
            tcvn3_hits += 1
    for _dim in dimensions:
        _dim["text"] = decode_tcvn3(_dim.get("text", ""))

    # specs scanned over free text + dimension override text + attrib values +
    # inserted-block definition text
    block_def_flat = [t for vals in block_def_text.values() for t in vals]
    spec_corpus = "\n".join(texts + dim_texts + block_def_flat)
    specs = scan_text_for_specs(spec_corpus)
    # dimension measurements feed the spec view too
    specs["dxf_dimension_measurements"] = [d["measurement"] for d in dimensions
                                           if d.get("measurement") is not None]

    return {
        "file": source_file,
        "dxf_version": doc.dxfversion,
        "units": units,
        "insunits_code": insunits,
        "extents": extents,
        "layer_count": len(layers),
        "layers": layers,
        "entity_counts": entity_counts,
        "entity_total": sum(entity_counts.values()),
        "dimension_count": len(dimensions),
        "dimensions": dimensions,
        "blocks_inserted": blocks_inserted,
        "block_attributes": block_attributes,
        "block_definition_text": block_def_text,
        "text_objects": len(texts),
        "raw_text": texts,
        "raw_text_original": texts_raw if tcvn3_hits else None,
        "tcvn3": {"detected": tcvn3_hits > 0, "decoded_count": tcvn3_hits},
        "title_block_candidates": find_title_block_fields(texts),
        "specs": specs,
    }


# ----------------------------------------------------------------------------
# PDF parsing (pdfplumber)
# ----------------------------------------------------------------------------

def parse_pdf(path: str) -> dict:
    try:
        import pdfplumber
    except ImportError:
        raise RuntimeError("pdfplumber not installed. Run: pip install pdfplumber")

    pages_out = []
    all_lines: list[str] = []
    all_tables: list[list] = []

    with pdfplumber.open(path) as pdf:
        for pi, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            lines = [ln for ln in text.splitlines() if ln.strip()]
            all_lines.extend(lines)

            tables = page.extract_tables() or []
            all_tables.extend(tables)

            # Title block heuristic: words in bottom-right quadrant
            tb_words = []
            try:
                w, h = page.width, page.height
                for word in page.extract_words():
                    if word["x0"] > w * 0.5 and word["top"] > h * 0.6:
                        tb_words.append(word["text"])
            except Exception:
                pass

            pages_out.append({
                "page": pi + 1,
                "size": [round(page.width, 1), round(page.height, 1)],
                "line_count": len(lines),
                "lines": lines,
                "tables": tables,
                "title_block_region_words": tb_words,
            })

    all_text = "\n".join(all_lines)
    specs = scan_text_for_specs(all_text)

    mb = round(mojibake_ratio(all_text), 3)
    total_lines = len(all_lines)

    return {
        "file": os.path.basename(path),
        "page_count": len(pages_out),
        "pages": pages_out,
        "tables": all_tables,
        "title_block_candidates": find_title_block_fields(all_lines),
        "specs": specs,
        "mojibake_ratio": mb,
        "encoding_warning": mb > 0.10,
        "scanned_no_text_layer": total_lines == 0,
        "text_quality_note": (
            "Garbled text layer (legacy VN font) — read this PDF visually, trust the DXF."
            if mb > 0.10 else
            "No extractable text — likely a scanned/raster PDF; needs OCR or visual reading."
            if total_lines == 0 else "OK"
        ),
    }


# ----------------------------------------------------------------------------
# Merge + output
# ----------------------------------------------------------------------------

def merge_specs(*specs: dict) -> dict:
    """Union the spec lists across sources (de-duplicated)."""
    set_keys = ("diameters", "diameter_fits", "radii", "iso_fits", "threads",
                "chamfers", "surface_finish_ra")
    merged = {"tolerances": [], "gdt_frames_detected": 0}
    for k in set_keys:
        merged[k] = set()
    seen_tol = set()
    for s in specs:
        if not s:
            continue
        for t in s.get("tolerances", []):
            key = t.get("raw", json.dumps(t, sort_keys=True))
            if key not in seen_tol:
                seen_tol.add(key)
                merged["tolerances"].append(t)
        for k in set_keys:
            merged[k].update(s.get(k, []))
        merged["gdt_frames_detected"] += s.get("gdt_frames_detected", 0)
    for k in set_keys:
        merged[k] = sorted(merged[k])
    return merged


def basic_markdown(result: dict) -> str:
    """A plain MD dump (the skill produces the curated datasheet; this is the
    fallback / starting point for --md)."""
    out = [f"# Mechanical Drawing Extract — {result['name']}", ""]
    out.append(f"- Extracted: {result['extracted_at']}")
    out.append(f"- Sources: {', '.join(result['sources']) or 'none'}")
    out.append("")
    sp = result.get("specs_merged", {})
    out.append("## Spec summary (machine-detected)")
    out.append(f"- Tolerances: {len(sp.get('tolerances', []))}")
    out.append(f"- Toleranced bores/shafts (Ø+fit): {', '.join(sp.get('diameter_fits', [])) or '—'}")
    out.append(f"- Diameters: {', '.join(sp.get('diameters', [])) or '—'}")
    out.append(f"- Threads: {', '.join(sp.get('threads', [])) or '—'}")
    out.append(f"- ISO fits: {', '.join(sp.get('iso_fits', [])) or '—'}")
    out.append(f"- Chamfers: {', '.join(sp.get('chamfers', [])) or '—'}")
    out.append(f"- Surface finish: {', '.join(sp.get('surface_finish_ra', [])) or '—'}")
    out.append(f"- GD&T frames detected: {sp.get('gdt_frames_detected', 0)}")
    out.append("")
    if result.get("dxf"):
        d = result["dxf"]
        out.append("## DXF")
        if d.get("converted_from_dwg"):
            out.append(f"- Source: converted from DWG ({d.get('original_dwg')}) "
                       "via ODA File Converter")
        out.append(f"- Units: {d['units']} | Layers: {d['layer_count']} | "
                   f"Entities: {d['entity_total']} | Dimensions: {d['dimension_count']}")
        if d.get("extents"):
            ex = d["extents"]
            out.append(f"- Extents: {ex['width']} × {ex['height']} {d['units']}")
        out.append("")
    if result.get("pdf"):
        p = result["pdf"]
        out.append("## PDF")
        out.append(f"- Pages: {p['page_count']} | Tables: {len(p['tables'])}")
        if p.get("encoding_warning") or p.get("scanned_no_text_layer"):
            out.append(f"- ⚠️ {p.get('text_quality_note')}")
        out.append("")
    out.append("> NOTE: This is the raw machine dump. The skill rewrites this "
               "into a curated engineering datasheet with interpreted title "
               "block, dimension table, and confidence flags.")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Parse mechanical drawing PDF/DXF to JSON.")
    ap.add_argument("--dxf", help="Path to .dxf file")
    ap.add_argument("--dwg", help="Path to .dwg file (converted to DXF via the "
                                  "ODA File Converter; needs it installed)")
    ap.add_argument("--pdf", help="Path to .pdf file")
    ap.add_argument("--out", default=".", help="Output directory (default: cwd)")
    ap.add_argument("--name", help="Part/drawing name (default: derived from input)")
    ap.add_argument("--md", action="store_true", help="Also write a basic .md dump")
    args = ap.parse_args()

    if not args.dxf and not args.dwg and not args.pdf:
        print("ERROR: provide at least one of --dxf, --dwg or --pdf", file=sys.stderr)
        return 2

    if args.dxf and args.dwg:
        print("ERROR: pass either --dxf or --dwg for the geometry source, not both",
              file=sys.stderr)
        return 2

    for p in (args.dxf, args.dwg, args.pdf):
        if p and not os.path.isfile(p):
            print(f"ERROR: file not found: {p}", file=sys.stderr)
            return 2

    src = args.dxf or args.dwg or args.pdf
    name = args.name or os.path.splitext(os.path.basename(src))[0]

    result = {
        "name": name,
        "extracted_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "sources": [],
        "dxf": None,
        "pdf": None,
    }

    try:
        if args.dxf:
            result["dxf"] = parse_dxf(args.dxf)
            result["sources"].append(os.path.basename(args.dxf))
        elif args.dwg:
            result["dxf"] = parse_dwg(args.dwg)
            result["sources"].append(os.path.basename(args.dwg))
        if args.pdf:
            result["pdf"] = parse_pdf(args.pdf)
            result["sources"].append(os.path.basename(args.pdf))
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3

    result["specs_merged"] = merge_specs(
        (result["dxf"] or {}).get("specs"),
        (result["pdf"] or {}).get("specs"),
    )

    os.makedirs(args.out, exist_ok=True)
    json_path = os.path.join(args.out, f"{name}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Wrote {json_path}")

    if args.md:
        md_path = os.path.join(args.out, f"{name}.raw.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(basic_markdown(result))
        print(f"Wrote {md_path}")

    # short stdout summary for the skill / human
    sp = result["specs_merged"]
    print(f"  sources={len(result['sources'])} "
          f"tolerances={len(sp['tolerances'])} "
          f"bore_fits={len(sp['diameter_fits'])} "
          f"threads={len(sp['threads'])} "
          f"fits={len(sp['iso_fits'])} "
          f"chamfers={len(sp['chamfers'])} "
          f"gdt={sp['gdt_frames_detected']}")
    pdf = result.get("pdf")
    if pdf and (pdf.get("encoding_warning") or pdf.get("scanned_no_text_layer")):
        # Plain ASCII — stdout may be a legacy codepage (cp1252) that can't
        # encode the warning emoji; the flag also lives in the JSON regardless.
        print(f"  [!] PDF: {pdf.get('text_quality_note')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
