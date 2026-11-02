#!/usr/bin/env python
"""DWG/DXF nhiều tờ (khung in trong modelspace) -> bộ PDF vector.

Codified từ phiên 2026-11-02 (BIA BẮN tự động dấu T, 52 tờ). Skill: skills/extract/dwg-to-pdf.

Pipeline:
  DWG --ODA File Converter--> DXF R2018
      -> giải mã TCVN3 -> Unicode (tự nhận), in hoa chữ của font TCVN3 "H" (romanh.shx, .Vn...H)
      -> đổi mọi text style sang 1 font TTF Unicode (mặc định arial.ttf), gỡ XDATA font
      -> dò khung in (block "Khung in A3/A4", "frame", ...), gán đối tượng theo tâm bbox
      -> mỗi khung = 1 trang đúng khổ (kích thước khung / tỷ lệ chèn)
      -> PDF tổng (bookmark) + Tung-to/*.pdf + DANH-MUC-BAN-VE.md + sheets.json + preview PNG

Dùng:
  python dwg_to_pdf.py <file.dwg|file.dxf> [--out DIR] [--dry-run]
      [--frame-blocks "Khung in A3,Khung in A4"] [--font arial.ttf] [--color]
      [--tcvn3 auto|on|off] [--caps-fonts romanh.shx] [--titles titles.json]
      [--code-regex REGEX] [--name "Tên file tổng"]

Exit: 0 OK | 2 OK nhưng có cảnh báo cần người rà (tên tờ nghi sai, còn chữ lỗi font, trang rỗng)
      1 lỗi | 3 thiếu ODA File Converter
"""
from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import shutil

import subprocess
import sys
import tempfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import ezdxf
import fitz  # PyMuPDF
from ezdxf import bbox
from ezdxf.addons.drawing import Frontend, RenderContext, config, layout, pymupdf
from ezdxf.math import BoundingBox2d
from ezdxf.tools.text import plain_mtext

VERSION = "1.0.0"

# --------------------------------------------------------------------------- TCVN3
# Bảng chuẩn TCVN3 (ABC) -> Unicode, giống decode_tcvn3 trong WX-Pipeline parse_mech_drawing.py
_TCVN3_SRC = ("µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîï"
              "óñòô\xadõøö÷ùúýûüþ¡¢§£¤¥¦")
_TCVN3_DST = ("àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợ"
              "ùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ")
assert len(_TCVN3_SRC) == len(_TCVN3_DST)
# 0xD8 vừa là Ø (đường kính) vừa là TCVN3 'ỉ' -> giữ Ø (Ø100 phổ biến hơn nhiều)
_TCVN3_MAP = {s: d for s, d in zip(_TCVN3_SRC, _TCVN3_DST) if s != "Ø"}
_VIET_LATIN1 = set("àáâãèéêìíòóôõùúýÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝ")
_TCVN3_MARKERS = set(_TCVN3_SRC) - _VIET_LATIN1 - {"Ø"}


def has_marker(s: str) -> bool:
    return any(c in _TCVN3_MARKERS for c in s)


def is_unicode_viet(s: str) -> bool:
    return any(ord(c) > 0xFF for c in s)


def make_decoder(mode: str):
    """full: giải mọi chuỗi không có ký tự > U+00FF (bản vẽ TCVN3 toàn bộ — các chuỗi như
    'Chó thÝch', 'Sè' không mang ký tự đánh dấu nên lối marker-gated bỏ sót).
    marker: chỉ giải chuỗi có ký tự đánh dấu (bản vẽ trộn Unicode + TCVN3).  off: không giải."""
    def full(s):
        if not s or is_unicode_viet(s):
            return s
        return "".join(_TCVN3_MAP.get(c, c) for c in s)

    def marker(s):
        if not s or not has_marker(s):
            return s
        return "".join(_TCVN3_MAP.get(c, c) for c in s)
    return {"full": full, "marker": marker, "off": lambda s: s}[mode]


# --------------------------------------------------------------------------- MTEXT helpers
FCODE = re.compile(r"\\[Ff][^;|]*(\|[^;]*)?;")                      # \Fromant|c0;  \fArial|b0|i0;
MCODE = re.compile(r"(\\[ACcFfHQTWpS][^;]*;|\\[PNLlOoKk~\\{}]|[{}]|%%[A-Za-z])")


def upper_keep_codes(s: str) -> str:
    """In hoa phần chữ, giữ nguyên mã định dạng MTEXT / %%c."""
    return "".join(p if MCODE.fullmatch(p) else p.upper() for p in MCODE.split(s))


def iter_strings(doc):
    for blk in doc.blocks:
        for e in blk:
            t = e.dxftype()
            if t in ("TEXT", "ATTDEF"):
                yield e.dxf.text
            elif t == "MTEXT":
                yield e.text
            elif t == "DIMENSION" and e.dxf.hasattr("text"):
                yield e.dxf.text
            elif t == "INSERT":
                for a in e.attribs:
                    yield a.dxf.text


def style_family(st) -> str:
    try:
        return st.get_xdata("ACAD")[0].value if st.has_xdata("ACAD") else ""
    except Exception:
        return ""


def normalize_text(doc, tcvn3: str, font: str, caps_fonts: set[str], log: dict):
    """Giải mã + in hoa font chữ hoa + đổi font. Trả về tập style chữ hoa."""
    strings = [s for s in iter_strings(doc) if s]
    n_marker = sum(1 for s in strings if has_marker(s))
    n_uni = sum(1 for s in strings if is_unicode_viet(s))
    if tcvn3 == "auto":
        mode = "full" if n_marker > max(5, n_uni) else ("marker" if n_marker else "off")
    else:
        mode = {"on": "full", "off": "off"}[tcvn3]
    log["tcvn3"] = dict(mode=mode, marker_strings=n_marker, unicode_strings=n_uni)
    dec = make_decoder(mode)

    caps = {s.dxf.name.lower() for s in doc.styles
            if (s.dxf.font or "").lower() in caps_fonts
            or (style_family(s).startswith(".Vn") and style_family(s).endswith("H"))}
    caps_inline = "|".join(re.escape(os.path.splitext(f)[0]) for f in caps_fonts) or "romanh"
    upgroup = re.compile(r"\{\\F(?:" + caps_inline + r")[^;]*;([^{}]*)\}", re.I)
    log["caps_styles"] = sorted(caps)

    def is_caps(e):
        return e.dxf.is_supported("style") and e.dxf.get("style", "").lower() in caps

    for blk in doc.blocks:
        for e in blk:
            t = e.dxftype()
            if t in ("TEXT", "ATTDEF"):
                s = dec(e.dxf.text)
                e.dxf.text = upper_keep_codes(s) if is_caps(e) else s
            elif t == "MTEXT":
                s = dec(e.text)
                s = upper_keep_codes(s) if is_caps(e) else upgroup.sub(
                    lambda m: "{" + upper_keep_codes(m.group(1)) + "}", s)
                e.text = FCODE.sub("", s)
            elif t == "DIMENSION" and e.dxf.hasattr("text"):
                e.dxf.text = FCODE.sub("", dec(e.dxf.text))
            elif t == "INSERT":
                for a in e.attribs:
                    s = dec(a.dxf.text)
                    a.dxf.text = upper_keep_codes(s) if is_caps(a) else s
    for st in doc.styles:
        st.dxf.font = font
        if st.dxf.hasattr("bigfont"):
            st.dxf.discard("bigfont")
        if st.has_xdata("ACAD"):          # họ font TTF trong XDATA đè lên .font -> phải gỡ
            st.discard_xdata("ACAD")
    return caps


# --------------------------------------------------------------------------- DWG -> DXF
def find_oda() -> str | None:
    for base in (r"C:\Program Files\ODA", r"C:\Program Files (x86)\ODA"):
        hits = sorted(glob.glob(os.path.join(base, "*", "ODAFileConverter.exe")))
        if hits:
            return hits[-1]
    return shutil.which("ODAFileConverter")


def dwg_to_dxf(src: str, work: str) -> str:
    oda = find_oda()
    if not oda:
        print("THIẾU ODA File Converter — cài: winget install --id ODA.ODAFileConverter", file=sys.stderr)
        sys.exit(3)
    din, dout = os.path.join(work, "in"), os.path.join(work, "dxf")
    os.makedirs(din, exist_ok=True)
    os.makedirs(dout, exist_ok=True)
    shutil.copy2(src, os.path.join(din, "src.dwg"))   # tên ASCII: ODA kén đường dẫn Unicode
    subprocess.run([oda, din, dout, "ACAD2018", "DXF", "0", "1", "*.dwg"], check=False,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    out = os.path.join(dout, "src.dxf")
    if not os.path.exists(out):
        print("ODA không tạo được DXF", file=sys.stderr)
        sys.exit(1)
    return out


# --------------------------------------------------------------------------- frames
ISO = {"A0": (1189, 841), "A1": (841, 594), "A2": (594, 420), "A3": (420, 297), "A4": (297, 210)}
FRAME_NAME = re.compile(r"khung|frame|border|title|A[0-4]\b", re.I)


def paper_name(w: float, h: float) -> str:
    L, S = max(w, h), min(w, h)
    best = min(ISO, key=lambda k: abs(ISO[k][0] - L) + abs(ISO[k][1] - S))
    L0, S0 = ISO[best]
    return best if abs(L0 - L) / L0 < 0.06 and abs(S0 - S) / S0 < 0.06 else f"{round(w)}x{round(h)}"


def detect_frames(msp, names: list[str] | None, cache):
    inserts = [i for i in msp.query("INSERT")]
    if names:
        cand = [i for i in inserts if i.dxf.name in names]
    else:
        # block tên giống khung + tỷ lệ cạnh ≈ √2 (khổ ISO)
        by = collections.defaultdict(list)
        for i in inserts:
            if FRAME_NAME.search(i.dxf.name):
                by[i.dxf.name].append(i)
        cand = []
        for name, ins in by.items():
            b = bbox.extents([ins[0]], cache=cache)
            if not b.has_data:
                continue
            r = max(b.size.x, b.size.y) / max(1e-9, min(b.size.x, b.size.y))
            if 1.30 < r < 1.52:
                cand += ins
    frames = []
    for i in cand:
        b = bbox.extents([i], cache=cache)
        if not b.has_data:
            continue
        sc = abs(i.dxf.xscale) or 1.0
        w, h = b.size.x / sc, b.size.y / sc
        frames.append(dict(handle=i.dxf.handle, block=i.dxf.name, scale=sc,
                           x0=b.extmin.x, y0=b.extmin.y, x1=b.extmax.x, y1=b.extmax.y,
                           w_mm=round(w), h_mm=round(h), paper=paper_name(w, h)))
    # bỏ khung nằm lọt trong khung khác (block khung lồng nhau)
    def inside(a, b):
        return a is not b and a["x0"] >= b["x0"] - 1 and a["x1"] <= b["x1"] + 1 \
            and a["y0"] >= b["y0"] - 1 and a["y1"] <= b["y1"] + 1
    frames = [f for f in frames if not any(inside(f, g) for g in frames)]
    # thứ tự đọc: theo hàng (trên -> dưới), trong hàng trái -> phải
    # (khung khác khổ thường chỉ thẳng mép dưới -> gom hàng theo chồng lấn dọc, không theo mép trên)
    rows = []
    for f in sorted(frames, key=lambda f: -(f["y0"] + f["y1"])):
        h = f["y1"] - f["y0"]
        for r in rows:
            ov = min(f["y1"], r["y1"]) - max(f["y0"], r["y0"])
            if ov >= 0.5 * min(h, r["hmin"]):
                r["items"].append(f)
                r["y0"], r["y1"] = min(r["y0"], f["y0"]), max(r["y1"], f["y1"])
                r["hmin"] = min(r["hmin"], h)
                break
        else:
            rows.append(dict(items=[f], y0=f["y0"], y1=f["y1"], hmin=h))
    rows.sort(key=lambda r: -(r["y0"] + r["y1"]))
    frames = [f for r in rows for f in sorted(r["items"], key=lambda f: f["x0"])]
    return frames


def assign_entities(msp, frames, cache):
    assign = {f["handle"]: [] for f in frames}
    orphans = 0
    for e in msp:
        try:
            b = bbox.extents([e], cache=cache)
        except Exception:
            continue
        if not b.has_data:
            continue
        cx, cy = b.center.x, b.center.y
        hit = [f for f in frames if f["x0"] <= cx <= f["x1"] and f["y0"] <= cy <= f["y1"]]
        if hit:
            f = min(hit, key=lambda f: f["x1"] - f["x0"])
            assign[f["handle"]].append(e)
        else:
            orphans += 1
    return assign, orphans


# --------------------------------------------------------------------------- sheet naming
DEFAULT_CODE = r"\b\d{1,3}\.[A-Z]{1,6}-?\d*[A-Z]?(?:\.\d{2}){1,4}(?:\s*BL)?\b"
MATERIAL_HINT = re.compile(r"^(THÉP|GANG|GỖ|NHÔM|ĐỒNG|INOX|COMPOSITE|NHỰA|CAO SU)\b|SS400|AH36|CT3|C45", re.I)


def texts_of(ents, caps):
    allt, capt = [], []
    for e in ents:
        t = e.dxftype()
        items = []
        if t == "TEXT":
            items = [(e.dxf.text, e.dxf.style)]
        elif t == "MTEXT":
            items = [(plain_mtext(e.text), e.dxf.style)]
        elif t == "INSERT":
            items = [(a.dxf.text, a.dxf.style) for a in e.attribs]
        for s, st in items:
            s = " ".join(s.split())
            if not s:
                continue
            allt.append(s)
            if st.lower() in caps:
                capt.append(s)
    return allt, capt


def name_sheets(frames, assign, caps, code_re):
    rx = re.compile(code_re, re.I)
    per = []
    for f in frames:
        allt, capt = texts_of(assign[f["handle"]], caps)
        per.append((allt, capt))
    # tên sản phẩm = chuỗi chữ hoa lặp ở > nửa số tờ -> loại khỏi ứng viên tên tờ
    freq = collections.Counter(s.upper() for _, capt in per for s in set(capt))
    common = {s for s, n in freq.items() if n > max(2, len(frames) // 2)}
    for f, (allt, capt) in zip(frames, per):
        codes = [m.group(0).upper() for s in (capt or allt) for m in [rx.search(s.upper())] if m]
        if not codes:
            codes = [m.group(0).upper() for s in allt for m in [rx.search(s.upper())] if m]
        f["code"] = re.sub(r"\s+", " ", collections.Counter(codes).most_common(1)[0][0]) if codes else ""
        cand = [s for s in capt if s.upper() not in common and not rx.search(s.upper())
                and len(s) > 2 and not re.fullmatch(r"[\d\s.,:;/()\-x×]+", s)]
        good = [s for s in cand if not MATERIAL_HINT.search(s)]
        f["title"] = max(good or cand, key=len).upper() if (good or cand) else ""
        f["review"] = []
        if not good and cand:
            f["review"].append("tên tờ giống ô vật liệu")
        if not f["title"]:
            f["review"].append("không đọc được tên tờ")
        if not f["code"]:
            f["review"].append("không đọc được ký hiệu")
        f["n_texts"] = len(allt)


# --------------------------------------------------------------------------- render
def render_sheet(doc, msp, f, ents, color: bool) -> bytes:
    cfg = config.Configuration(
        color_policy=config.ColorPolicy.COLOR if color else config.ColorPolicy.BLACK,
        background_policy=config.BackgroundPolicy.WHITE)
    ctx = RenderContext(doc)
    ctx.set_current_layout(msp)
    be = pymupdf.PyMuPdfBackend()
    fe = Frontend(ctx, be, config=cfg)
    # draw_entities không tự đặt nền như draw_layout -> thiếu dòng này trang bị nền ĐEN
    fe.set_background(ctx.current_layout_properties.background_color)
    fe.draw_entities(ents)
    page = layout.Page(f["w_mm"], f["h_mm"], layout.Units.mm, margins=layout.Margins.all(0))
    return be.get_pdf_bytes(page, settings=layout.Settings(fit_page=True),
                            render_box=BoundingBox2d([(f["x0"], f["y0"]), (f["x1"], f["y1"])]))


def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|\r\n]+', "-", s).strip(" .")[:150]


def contact_sheet(pdf: fitz.Document, path: str):
    n = len(pdf)
    cols = 8 if n > 24 else 6
    rows = (n + cols - 1) // cols
    W = fitz.open()
    pg = W.new_page(width=cols * 200, height=rows * 215)
    for i in range(n):
        c, r = i % cols, i // cols
        pg.show_pdf_page(fitz.Rect(c * 200, r * 215, c * 200 + 195, r * 215 + 190), pdf, i)
        pg.insert_text((c * 200 + 3, r * 215 + 205), str(i + 1), fontsize=10)
    pg.get_pixmap(dpi=60).save(path)


# --------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src")
    ap.add_argument("--out")
    ap.add_argument("--name", help="tên file PDF tổng (mặc định = tên file nguồn)")
    ap.add_argument("--frame-blocks", help="tên block khung, phân tách bằng dấu phẩy (mặc định tự dò)")
    ap.add_argument("--font", default="arial.ttf")
    ap.add_argument("--color", action="store_true", help="giữ màu (mặc định in đen trắng)")
    ap.add_argument("--tcvn3", choices=["auto", "on", "off"], default="auto")
    ap.add_argument("--caps-fonts", default="romanh.shx", help="font SHX chữ hoa, phân tách dấu phẩy")
    ap.add_argument("--titles", help="JSON {\"<số tờ>\": \"TÊN\"} ghi đè tên tờ")
    ap.add_argument("--code-regex", default=DEFAULT_CODE)
    ap.add_argument("--dry-run", action="store_true", help="chỉ dò khung + đặt tên, không xuất PDF")
    a = ap.parse_args()

    src = os.path.abspath(a.src)
    stem = os.path.splitext(os.path.basename(src))[0]
    out = a.out or os.path.join(os.path.dirname(src), "PDF-" + stem)
    work = tempfile.mkdtemp(prefix="dwg2pdf_")
    log = dict(version=VERSION, source=src)

    dxf = dwg_to_dxf(src, work) if src.lower().endswith(".dwg") else src
    doc = ezdxf.readfile(dxf)
    msp = doc.modelspace()
    caps = normalize_text(doc, a.tcvn3, a.font, {x.strip().lower() for x in a.caps_fonts.split(",") if x.strip()}, log)

    cache = bbox.Cache()
    names = [x.strip() for x in a.frame_blocks.split(",")] if a.frame_blocks else None
    frames = detect_frames(msp, names, cache)
    if not frames:
        paper = [l for l in doc.layouts if l.name != "Model" and len(l)]
        print("Không tìm thấy khung in trong modelspace."
              + (f" Có {len(paper)} layout paperspace: {[l.name for l in paper]} — dùng --frame-blocks hoặc in layout."
                 if paper else " Chỉ định --frame-blocks."), file=sys.stderr)
        sys.exit(1)
    assign, orphans = assign_entities(msp, frames, cache)
    name_sheets(frames, assign, caps, a.code_regex)
    overrides = json.load(open(a.titles, encoding="utf-8")) if a.titles else {}
    for n, f in enumerate(frames, 1):
        f["page"] = n
        if str(n) in overrides:
            f["title"] = overrides[str(n)]
            f["review"] = [r for r in f["review"] if "tên tờ" not in r]
    log.update(frames=len(frames), orphans=orphans,
               frame_blocks=sorted({f["block"] for f in frames}))

    print(f"Nguồn: {src}")
    print(f"TCVN3: {log['tcvn3']} | style chữ hoa: {log['caps_styles']}")
    print(f"Khung: {len(frames)} ({', '.join(log['frame_blocks'])}) | đối tượng ngoài khung: {orphans}")
    for f in frames:
        flag = ("  ⚠ " + "; ".join(f["review"])) if f["review"] else ""
        print(f"{f['page']:3d}  {f['paper']:<4} 1:{f['scale']:g}  {f['code']:<22} {f['title']}{flag}")
    if a.dry_run:
        shutil.rmtree(work, ignore_errors=True)
        return 2 if any(f["review"] for f in frames) else 0

    os.makedirs(os.path.join(out, "Tung-to"), exist_ok=True)
    book, toc, warn = fitz.open(), [], []
    for f in frames:
        pdf = render_sheet(doc, msp, f, assign[f["handle"]], a.color)
        one = fitz.open("pdf", pdf)
        label = f"{f['page']:02d}. {f['code']} – {f['title']}".replace(" –  ", " ").strip()
        one.set_metadata({"title": label})
        fname = safe_name(f"{f['page']:02d}_{f['code']}_{f['title']}") + ".pdf"
        one.save(os.path.join(out, "Tung-to", fname), garbage=3, deflate=True)
        f["file"] = "Tung-to/" + fname
        book.insert_pdf(one)
        toc.append([1, label, f["page"]])
        # tự kiểm: trang rỗng / còn chữ TCVN3 chưa giải
        pg = book[-1]
        txt = pg.get_text()
        if len(pg.read_contents()) < 2000:
            f["review"].append("trang gần như rỗng")
        if has_marker(txt):
            f["review"].append("còn chữ lỗi font TCVN3")
        print(f"  ✓ {label}", flush=True)
    book.set_toc(toc)
    book.set_metadata({"title": stem, "creator": f"dwg_to_pdf.py {VERSION} (ODA + ezdxf)"})
    total = os.path.join(out, safe_name(a.name or stem) + ".pdf")
    book.save(total, garbage=3, deflate=True)
    contact_sheet(book, os.path.join(out, "_preview.png"))

    rows = "\n".join(f"| {f['page']} | {f['code']} | {f['title']} | {f['paper']} | 1:{f['scale']:g} | "
                     f"{'; '.join(f['review'])} |" for f in frames)
    with open(os.path.join(out, "DANH-MUC-BAN-VE.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Danh mục bản vẽ — {stem}\n\nNguồn: `{src}` — {len(frames)} tờ. "
                 "Cột *Khung* là tỷ lệ khung in, không phải tỷ lệ hình vẽ.\n\n"
                 "| Tờ | Ký hiệu | Tên | Khổ | Khung | Cần rà |\n|---|---|---|---|---|---|\n" + rows + "\n")
    for f in frames:
        for k in ("handle",):
            f.pop(k, None)
    log["sheets"] = frames
    json.dump(log, open(os.path.join(out, "sheets.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    shutil.rmtree(work, ignore_errors=True)

    warn = [f for f in frames if f["review"]]
    print(f"\nPDF tổng : {total} ({os.path.getsize(total) // 1024} KB, {len(book)} trang)")
    print(f"Từng tờ  : {os.path.join(out, 'Tung-to')}")
    print(f"Preview  : {os.path.join(out, '_preview.png')}")
    print(f"Cần rà   : {len(warn)} tờ" + ("".join(f"\n  - tờ {f['page']}: {'; '.join(f['review'])}" for f in warn)))
    return 2 if warn else 0


if __name__ == "__main__":
    sys.exit(main())
